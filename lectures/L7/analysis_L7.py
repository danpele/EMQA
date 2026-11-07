"""
analysis_L7.py -- Lecture 7 "Machine learning for energy markets" (EMQA)
=========================================================================
Reads the real series in repo/data/clean (see data/SOURCES.md) and the benchmark forecasts of Lecture 2
(lectures/L2/cache/forecasts.pkl, written by analysis_L2.py), runs every machine-learning model shown on the slides and writes
    lectures/L7/L7_numbers.json        all results (the deck builder reads ONLY this file)
    lectures/L7/charts/en/*.pdf        figures with English labels
    lectures/L7/charts/ro/*.pdf        the same figures with Romanian labels
    lectures/L7/cache/ml.pkl           all forecasts, searches and explanations (recomputed when data or engine change)
Run:  python3 lectures/L7/analysis_L7.py            (add --fresh to ignore the cache; about 20 minutes on 16 cores)

Design (identical to Lecture 2, so that every number is comparable with the L2 benchmarks)
  * Target: Romanian day-ahead price (OPCOM PZU), hourly, CET/CEST delivery day; after 1 Oct 2025 the hour is the mean of its
    four quarter-hours. Panel 2022-01-01 to the cut-off (last complete month). DST: 24 columns (epftoolbox convention).
  * Gate-closure information set for day d (12:00 CET on d-1): prices up to d-1; realised load, wind+solar, hydro, nuclear,
    net imports up to d-2; carbon at the d-2 close. Test year = the last 365 days (same as L2).
  * Three chronological samples: training = all days from 2022-01-08 to the start of the validation year; validation year =
    the 365 days before the test year (hyperparameter search only, quarterly refits); test year (monthly refits on an
    expanding window, as the ML models of L2). The test year is never used to choose anything.
  * Random search (Bergstra & Bengio, 2012): 24 random configurations + the L2 configuration, for the neural network (DNN,
    PyTorch, 24 outputs, Lago et al. 2021 style) and for gradient boosting (XGBoost). Inside each fit, the number of epochs of
    the DNN is chosen on the last 15% of the training days (chronological early stopping), then the network is refitted on all
    training days. Seeds fixed; 4 seeds averaged for the final DNN.
  * Foundation models: Chronos-Bolt (small) and Chronos-2, zero-shot, context = the last 2048 hourly prices up to the end of d-1.
  * Explanations: exact SHAP values of the boosted trees (XGBoost pred_contribs) and permutation importance of the DNN input
    blocks on the test year.  Spikes / negative prices: XGBoost and logistic classifiers, persistence and AW-LEAR as scores.
  * Pitfalls measured on the same test year: look-ahead (same-day realised load and wind+solar), shuffled cross-validation,
    data snooping (choosing the configuration on the test year), retraining frequency and window.
  * Leakage self-check: forecasts recomputed with all data after gate closure deleted or replaced by nonsense are identical.
There is no simulated series in this lecture.
"""

import hashlib
import json
import os
import pickle
import sys
import time
import warnings

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import emqa_plot as ep  # noqa: E402
from emqa_plot import PAL  # noqa: E402

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

warnings.filterwarnings("ignore")
ep.style()
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "data", "clean")
TZ = "Europe/Brussels"
ENGINE_VERSION = "L7-engine-v3"
FRESH = "--fresh" in sys.argv
N = {"charts": {}}
SEED = 20261106
N_JOBS = min(16, os.cpu_count() or 4)
MON_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MON_RO = ["ian.", "feb.", "mar.", "apr.", "mai", "iun.", "iul.", "aug.", "sep.", "oct.", "nov.", "dec."]


def d(ts):
    return pd.Timestamp(ts).strftime("%Y-%m-%d")


def fl(x, k=4):
    if x is None:
        return None
    x = float(x)
    return None if np.isnan(x) else round(x, k)


# =============================================================================
# 0. Load data and cut-off (same rule and same panel as Lecture 2)
# =============================================================================
PD = ep.prices_daily()
G = ep.generation_ro_daily()
CB = ep.crossborder_ro_daily()
_raw_last = min(PD["RO"].dropna().index.max(), G["hydro_run_of_river"].dropna().index.max())
END = pd.Timestamp(((_raw_last + pd.Timedelta(days=1)).to_period("M").to_timestamp() - pd.Timedelta(days=1)).date())
N["cutoff"] = {"end": d(END), "year": END.year, "month": int(END.month), "download": "2026-11-04"}
START = pd.Timestamp("2022-01-01")


def day_matrix(s):
    """UTC-indexed hourly series -> CET delivery day x 24 hours (Assignment 1 / epftoolbox DST convention) + DST flag."""
    s = s.copy()
    s.index = pd.to_datetime(s.index, utc=True).tz_convert(TZ)
    df = pd.DataFrame({"v": s.values, "day": s.index.tz_localize(None).normalize(), "h": s.index.hour})
    m = df.groupby(["day", "h"])["v"].mean().unstack("h").reindex(columns=range(24))     # 25-h day: doubled hour averaged
    days = m.index
    nh = ((((days + pd.Timedelta(days=1)).tz_localize(TZ)) - days.tz_localize(TZ)) / pd.Timedelta(hours=1)).astype(int)
    dst = pd.Series(np.asarray(nh != 24), index=days)
    for dd in days[dst.values]:
        if pd.isna(m.loc[dd, 2]):
            m.loc[dd, 2] = 0.5 * (m.loc[dd, 1] + m.loc[dd, 3])                              # 23-h day: h02 = mean(h01, h03)
    m = m.dropna(how="any")
    return m, dst.reindex(m.index)


HP = pd.read_csv(os.path.join(DATA, "power_da_prices_hourly_utc.csv"), index_col=0)
GH = pd.read_csv(os.path.join(DATA, "generation_ro_mw_hourly_utc.csv"), index_col=0)
PM_ALL, _ = day_matrix(HP["RO"].dropna())                       # full history since 2015 (spike thresholds only)
PM, DST = day_matrix(HP["RO"].dropna())
LM, _ = day_matrix(GH["load"].dropna())
RM, _ = day_matrix((GH["wind_onshore"] + GH["solar"]).dropna())
CAL = pd.date_range(START, END, freq="D")
PM, LM, RM, DST = PM.reindex(CAL), LM.reindex(CAL), RM.reindex(CAL), DST.reindex(CAL)
assert not PM.isna().any().any() and not LM.isna().any().any() and not RM.isna().any().any(), "panel has gaps"
N["data"] = {"start": d(START), "end": d(END), "n_days": len(CAL)}

EUA = pd.read_csv(os.path.join(DATA, "eua_daily.csv"), parse_dates=["date"]).set_index("date")["eua_etc_co2l_eur_per_unit"]
CAL_EX = pd.date_range(START - pd.Timedelta(days=30), END, freq="D")
FUND_RAW = pd.DataFrame({
    "hydro": (G["hydro_run_of_river"] + G["hydro_water_reservoir"]).reindex(CAL_EX),
    "nuclear": G["nuclear"].reindex(CAL_EX),
    "netimp": CB["sum"].reindex(CAL_EX),
    "eua": EUA.reindex(CAL_EX)})
FUND_AVAIL = FUND_RAW.ffill().shift(2).reindex(CAL)          # carried forward from the past only, then lagged 2 days
assert not FUND_AVAIL.isna().any().any()

N_TEST, N_VAL = 365, 365
TEST0 = END - pd.Timedelta(days=N_TEST - 1)
VAL0 = TEST0 - pd.Timedelta(days=N_VAL)
TDAYS = pd.date_range(TEST0, END, freq="D")
VDAYS = pd.date_range(VAL0, TEST0 - pd.Timedelta(days=1), freq="D")
P_ = PM.values.astype(float)
L_ = LM.values.astype(float)
R_ = RM.values.astype(float)
F_ = FUND_AVAIL.values.astype(float)
DOW = CAL.dayofweek.values
IDX = {t: i for i, t in enumerate(CAL)}
PLAGS, XLAGS = (1, 2, 3, 7), (2, 3, 7)
FIRST = 7                                                       # first usable target row (needs the price of d-7)
N["design"] = {"train_start": d(CAL[FIRST]), "train_end": d(VAL0 - pd.Timedelta(days=1)), "val_start": d(VAL0),
               "val_end": d(VDAYS[-1]), "test_start": d(TEST0), "test_end": d(END), "n_test": N_TEST, "n_val": N_VAL,
               "n_train_days_val": int(IDX[VAL0] - FIRST), "n_train_days_last": int(IDX[TDAYS[-1].replace(day=1)] - FIRST),
               "n_dst_test": int(DST.loc[TDAYS].sum())}


def shift_rows(A, k):
    out = np.full_like(A, np.nan)
    out[k:] = A[:-k]
    return out


def mad_scale(x):
    x = np.asarray(x, float).ravel()
    m = np.median(x)
    s = stats.median_abs_deviation(x, scale="normal")
    return m, (s if s > 0 else 1.0)


def blocks_of(days, freq="M"):
    """(first row, last row) of each calendar month (or quarter) of a day range."""
    out = []
    for _, g in pd.Series(days, index=days).groupby(days.to_period(freq)):
        out.append((IDX[g.index[0]], IDX[g.index[-1]]))
    return out


MB = blocks_of(TDAYS, "M")                                      # 12 monthly refits in the test year (as in L2)
_vm = blocks_of(VDAYS, "M")                                     # validation year: 4 blocks of 3 months, refit at the start of each
VB = [(_vm[k][0], _vm[k + 2][1]) for k in range(0, 12, 3)]


# =============================================================================
# 1. Benchmarks of Lecture 2 (read from its cache, checked against L2_numbers.json)
# =============================================================================
with open(os.path.join(REPO, "lectures", "L2", "cache", "forecasts.pkl"), "rb") as fh:
    FC2 = pickle.load(fh)
with open(os.path.join(REPO, "lectures", "L2", "L2_numbers.json")) as fh:
    N2 = json.load(fh)
N_BURN2 = N2["design"]["n_burn"]
assert N2["design"]["test_start"] == d(TEST0) and N2["design"]["test_end"] == d(END), "L7 and L2 test years differ"
A = P_[[IDX[t] for t in TDAYS]]                                 # actual prices, test year (365 x 24)
B = {k: v[N_BURN2:] for k, v in FC2["point"].items()}
B["aw_arx"] = np.mean([B[f"arx{T}"] for T in (56, 84, 112, 714, 721, 728)], 0)
B["aw_lear"] = np.mean([B[f"lear{T}"] for T in (364, 546, 728)], 0)
B["gbm2"], B["mlp2"] = FC2["gbm"], FC2["mlp"]
B["ens4"] = np.mean([B["aw_arx"], B["aw_lear"], B["gbm2"], B["mlp2"]], 0)
for k2, k7 in [("aw_lear", "aw_lear"), ("naive", "naive"), ("ens_all", "ens4"), ("gbm", "gbm2"), ("mlp", "mlp2")]:
    assert abs(np.mean(np.abs(A - B[k7])) - N2["acc"][k2]["mae"]) < 0.006, f"L2 cache and L2_numbers differ for {k2}"


# =============================================================================
# 2. Model engines
# =============================================================================
# ---------------------------------------------------------------- deep neural network (PyTorch), 24 outputs
def dnn_inputs(Pa, La, Ra, Fa, rows, sc, cfg):
    """Input vector of day d (rows): asinh-scaled prices of d-1, d-2, (d-3), d-7 (24 h each), load and wind+solar of d-2, d-3, d-7,
    the 4 daily fundamentals of d-2 and day-of-week dummies. Returns the matrix and the column range of each block."""
    m, s, mL, sL, mR, sR = sc
    cols, names = [], []
    for k in PLAGS:
        if k == 3 and not cfg["p3"]:
            continue
        cols.append(np.arcsinh((shift_rows(Pa, k)[rows] - m) / s))
        names += [f"price d-{k}"] * 24
    if cfg["load"]:
        for k in XLAGS:
            cols.append(np.arcsinh((shift_rows(La, k)[rows] - mL) / sL))
            names += ["load"] * 24
    if cfg["res"]:
        for k in XLAGS:
            cols.append(np.arcsinh((shift_rows(Ra, k)[rows] - mR) / sR))
            names += ["wind+solar"] * 24
    if cfg["fund"]:
        cols.append(Fa[rows])
        names += ["hydro", "nuclear", "net imports", "carbon"]
    cols.append(np.eye(7)[DOW[rows]])
    names += ["day of week"] * 7
    return np.column_stack(cols), np.array(names)


def _net(n_in, cfg):
    import torch.nn as nn
    act = nn.ReLU if cfg["act"] == "relu" else nn.Softplus
    layers, prev = [], n_in
    for h in [cfg["n1"]] + ([cfg["n2"]] if cfg["n2"] else []):
        layers += [nn.Linear(prev, h), act(), nn.Dropout(cfg["drop"])]
        prev = h
    layers.append(nn.Linear(prev, 24))
    return nn.Sequential(*layers)


def _train(X, Y, cfg, seed, epochs, Xv=None, yv_eur=None, m=0.0, s=1.0, patience=25):
    """Mini-batch Adam on the mean absolute error of the asinh price; L1 penalty on the input layer (Lago et al. 2021).
    With a validation block: returns the epoch with the lowest validation MAE (EUR/MWh) and the learning curves."""
    import torch
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    Xt, Yt = torch.tensor(X, dtype=torch.float32), torch.tensor(Y, dtype=torch.float32)
    net = _net(X.shape[1], cfg)
    opt = torch.optim.Adam(net.parameters(), lr=cfg["lr"], weight_decay=cfg["wd"])
    first = net[0].weight
    curve_tr, curve_v, best, best_ep, since = [], [], np.inf, 1, 0
    for ep_ in range(1, epochs + 1):
        net.train()
        perm = rng.permutation(len(X))
        for b0 in range(0, len(X), cfg["batch"]):
            ix = perm[b0:b0 + cfg["batch"]]
            opt.zero_grad()
            loss = (net(Xt[ix]) - Yt[ix]).abs().mean() + cfg["l1"] * first.abs().sum() / first.numel()
            loss.backward()
            opt.step()
        if Xv is not None:
            net.eval()
            with torch.no_grad():
                ptr = m + s * np.sinh(net(Xt).numpy())
                pv = m + s * np.sinh(net(torch.tensor(Xv, dtype=torch.float32)).numpy())
            curve_tr.append(float(np.mean(np.abs(ptr - (m + s * np.sinh(Y))))))
            v = float(np.mean(np.abs(pv - yv_eur)))
            curve_v.append(v)
            if v < best - 1e-9:
                best, best_ep, since = v, ep_, 0
            else:
                since += 1
                if since >= patience:
                    break
    net.eval()
    return net, best_ep, curve_tr, curve_v


def dnn_block(Pa, La, Ra, Fa, i0, i1, cfg, seeds=(1,), max_ep=300, keep=False, lo=FIRST):
    """Fit on target rows lo..i0-1 (all before the block), forecast rows i0..i1.
    Step 1: transforms from rows up to the start of the early-stopping block; train on the first 85% of the training days,
    early-stop on the last 15% (chronological). Step 2: transforms from all training rows; refit for the chosen number of
    epochs on all training days; forecast. Seeds averaged."""
    import torch
    torch.set_num_threads(1)
    t0 = time.perf_counter()
    tr = np.arange(lo, i0)
    cut = int(len(tr) * 0.85)
    v0 = tr[cut]
    sc0 = (*mad_scale(Pa[lo:v0]), *mad_scale(La[lo:v0 - 1]), *mad_scale(Ra[lo:v0 - 1]))
    X0, _ = dnn_inputs(Pa, La, Ra, Fa, tr, sc0, cfg)
    Y0 = np.arcsinh((Pa[tr] - sc0[0]) / sc0[1])
    mu0, sg0 = X0[:cut].mean(0), X0[:cut].std(0)
    sg0[sg0 == 0] = 1
    sc = (*mad_scale(Pa[tr]), *mad_scale(La[lo:i0 - 1]), *mad_scale(Ra[lo:i0 - 1]))
    X, names = dnn_inputs(Pa, La, Ra, Fa, tr, sc, cfg)
    Y = np.arcsinh((Pa[tr] - sc[0]) / sc[1])
    mu, sg = X.mean(0), X.std(0)
    sg[sg == 0] = 1
    te = np.arange(i0, i1 + 1)
    Xte, _ = dnn_inputs(Pa, La, Ra, Fa, te, sc, cfg)
    preds, epochs, curves, models = [], [], [], []
    for sd in seeds:
        _, best_ep, ctr, cv = _train((X0[:cut] - mu0) / sg0, Y0[:cut], cfg, sd, max_ep, (X0[cut:] - mu0) / sg0,
                                     Pa[tr[cut:]], sc0[0], sc0[1])
        net, _, _, _ = _train((X - mu) / sg, Y, cfg, sd, best_ep)
        with torch.no_grad():
            preds.append(sc[0] + sc[1] * np.sinh(net(torch.tensor((Xte - mu) / sg, dtype=torch.float32)).numpy()))
        epochs.append(best_ep)
        curves.append((ctr, cv))
        if keep:
            models.append({k: v.clone() for k, v in net.state_dict().items()})
    out = {"pred": np.mean(preds, 0), "epochs": epochs, "sec": time.perf_counter() - t0, "n_seeds": len(seeds)}
    if keep:
        out.update({"models": models, "mu": mu, "sg": sg, "sc": sc, "names": names, "curves": curves})
    return out


def dnn_predict_from(state, cfg, X, mu, sg, sc):
    import torch
    torch.set_num_threads(1)
    preds = []
    for st in state:
        net = _net(X.shape[1], cfg)
        net.load_state_dict(st)
        net.eval()
        with torch.no_grad():
            preds.append(sc[0] + sc[1] * np.sinh(net(torch.tensor((X - mu) / sg, dtype=torch.float32)).numpy()))
    return np.mean(preds, 0)


# ---------------------------------------------------------------- gradient boosting (XGBoost), one model for all hours
XGB_NAMES = ["P(d-1,h)", "P(d-2,h)", "P(d-3,h)", "P(d-7,h)", "P(d-1,23)", "min P(d-1)", "max P(d-1)", "mean P(d-1)",
             "L(d-2,h)", "L(d-7,h)", "RES(d-2,h)", "RES(d-7,h)", "mean L(d-2)", "mean RES(d-2)", "hydro(d-2)", "nuclear(d-2)",
             "net imports(d-2)", "EUA(d-2)", "hour", "day of week"]


def gbm_rows(Pa, La, Ra, Fa, rows, leak=False):
    """Long-format features for (day, hour) pairs (the 20 features of the L2 GBM). leak=True adds the realised load and
    wind+solar of the delivery hour itself (NOT known at gate closure: used only to measure the look-ahead pitfall)."""
    P1, P2, P3, P7 = (shift_rows(Pa, k) for k in PLAGS)
    L2_, L7_, R2_, R7_ = shift_rows(La, 2), shift_rows(La, 7), shift_rows(Ra, 2), shift_rows(Ra, 7)
    feats = []
    for h in range(24):
        f = [P1[rows, h], P2[rows, h], P3[rows, h], P7[rows, h], P1[rows, 23], P1[rows].min(1), P1[rows].max(1),
             P1[rows].mean(1), L2_[rows, h], L7_[rows, h], R2_[rows, h], R7_[rows, h], L2_[rows].mean(1),
             R2_[rows].mean(1), Fa[rows], np.full(len(rows), h), DOW[rows]]
        if leak:
            f += [La[rows, h], Ra[rows, h]]
        feats.append(np.column_stack(f))
    return np.stack(feats, 1)                                  # n_days x 24 x p


def _xgb(cfg, seed):
    import xgboost as xgb
    return xgb.XGBRegressor(n_estimators=cfg["n_est"], learning_rate=cfg["eta"], max_depth=cfg["depth"],
                            min_child_weight=cfg["mcw"], subsample=cfg["sub"], colsample_bytree=cfg["col"],
                            reg_lambda=cfg["lam"], objective=cfg["obj"], tree_method="hist", n_jobs=1, random_state=seed,
                            max_leaves=cfg.get("leaves", 0), grow_policy=cfg.get("grow", "depthwise"))


def xgb_block(Pa, La, Ra, Fa, i0, i1, cfg, seed=SEED, lo=FIRST, leak=False, shap=False):
    """Fit on target rows lo..i0-1, forecast rows i0..i1. Target = asinh((P-m)/s), m and s from the training prices."""
    t0 = time.perf_counter()
    tr = np.arange(lo, i0)
    m, s = mad_scale(Pa[tr])
    p = len(XGB_NAMES) + (2 if leak else 0)
    Xtr = gbm_rows(Pa, La, Ra, Fa, tr, leak).reshape(-1, p)
    ytr = np.arcsinh((Pa[tr] - m) / s).ravel()
    mdl = _xgb(cfg, seed).fit(Xtr, ytr)
    te = np.arange(i0, i1 + 1)
    Xte = gbm_rows(Pa, La, Ra, Fa, te, leak).reshape(-1, p)
    y = mdl.predict(Xte).reshape(len(te), 24)
    out = {"pred": m + s * np.sinh(y), "sec": time.perf_counter() - t0}
    if shap:
        import xgboost as xgb
        con = mdl.get_booster().predict(xgb.DMatrix(Xte), pred_contribs=True)      # exact SHAP values (Lundberg et al. 2020)
        out.update({"shap": con.reshape(len(te), 24, p + 1), "m": m, "s": s, "X": Xte.reshape(len(te), 24, p)})
    return out


def xgb_cv_shuffled(Pa, La, Ra, Fa, cfg, k_fold=5, seed=SEED):
    """The pitfall: random K-fold over all days (future days end up in the training folds). Out-of-fold forecasts."""
    from sklearn.model_selection import KFold
    rows = np.arange(FIRST, len(Pa))
    out = np.full((len(Pa), 24), np.nan)
    for tr_i, te_i in KFold(k_fold, shuffle=True, random_state=seed).split(rows):
        tr, te = rows[tr_i], rows[te_i]
        m, s = mad_scale(Pa[tr])
        mdl = _xgb(cfg, seed).fit(gbm_rows(Pa, La, Ra, Fa, tr).reshape(-1, len(XGB_NAMES)), np.arcsinh((Pa[tr] - m) / s).ravel())
        out[te] = m + s * np.sinh(mdl.predict(gbm_rows(Pa, La, Ra, Fa, te).reshape(-1, len(XGB_NAMES))).reshape(len(te), 24))
    return out


# ---------------------------------------------------------------- spikes and negative prices: classifiers
THR_Q = 0.90


def spike_threshold(t):
    """Spike threshold for delivery days of the month starting at t: 90th percentile of the hourly prices of the 365 days before t."""
    w = PM_ALL.loc[t - pd.Timedelta(days=365):t - pd.Timedelta(days=1)].values.ravel()
    return float(np.quantile(w, THR_Q))


MONTH_START = {}
for _t in CAL:
    MONTH_START.setdefault(_t.to_period("M"), _t.replace(day=1))
THETA = np.array([spike_threshold(MONTH_START[t.to_period("M")]) for t in CAL])      # threshold per delivery day (known at month start)


def clf_rows(Pa, La, Ra, Fa, rows, theta):
    X = gbm_rows(Pa, La, Ra, Fa, rows)
    th = np.repeat(theta[rows][:, None, None], 24, 1)
    return np.concatenate([X, th], 2)


CLF_NAMES = XGB_NAMES + ["threshold"]
CLF_CFG = {"n_est": 400, "eta": 0.05, "depth": 4, "mcw": 20, "sub": 0.8, "col": 0.8, "lam": 1.0}


def clf_block(Pa, La, Ra, Fa, theta, i0, i1, event, seed=SEED):
    """P(event) for rows i0..i1; event = 'spike' (price > threshold of its month) or 'neg' (price <= 0).
    XGBoost and a logistic regression (standardised features, one-hot hour and weekday), fitted on rows before the month."""
    import xgboost as xgb
    from sklearn.linear_model import LogisticRegression
    tr = np.arange(FIRST, i0)
    te = np.arange(i0, i1 + 1)
    Xtr, Xte = clf_rows(Pa, La, Ra, Fa, tr, theta).reshape(-1, len(CLF_NAMES)), clf_rows(Pa, La, Ra, Fa, te, theta).reshape(-1, len(CLF_NAMES))
    lab = (lambda r: (Pa[r] > theta[r][:, None])) if event == "spike" else (lambda r: (Pa[r] <= 0))
    ytr = lab(tr).ravel().astype(int)
    c = CLF_CFG
    mdl = xgb.XGBClassifier(n_estimators=c["n_est"], learning_rate=c["eta"], max_depth=c["depth"], min_child_weight=c["mcw"],
                            subsample=c["sub"], colsample_bytree=c["col"], reg_lambda=c["lam"], tree_method="hist", n_jobs=1,
                            random_state=seed, objective="binary:logistic").fit(Xtr, ytr)
    px = mdl.predict_proba(Xte)[:, 1].reshape(len(te), 24)

    def lin(X):
        num = np.delete(X, [18, 19], 1)
        return num, np.column_stack([np.eye(24)[X[:, 18].astype(int)], np.eye(7)[X[:, 19].astype(int)]])
    ntr, dtr = lin(Xtr)
    nte, dte = lin(Xte)
    mu, sg = ntr.mean(0), ntr.std(0)
    sg[sg == 0] = 1
    lr = LogisticRegression(C=1.0, max_iter=3000).fit(np.column_stack([(ntr - mu) / sg, dtr]), ytr)
    pl = lr.predict_proba(np.column_stack([(nte - mu) / sg, dte]))[:, 1].reshape(len(te), 24)
    return {"xgb": px, "logit": pl, "share_train": float(ytr.mean())}


# ---------------------------------------------------------------- foundation models (zero-shot)
CTX = 2048


def chronos_forecasts(Pa, rows, model):
    """Zero-shot: context = the last CTX hourly prices up to the end of d-1 (all known at gate closure), horizon 24 h."""
    import torch
    from chronos import BaseChronosPipeline
    torch.set_num_threads(1)                                    # one core, as for the other models (timing)
    pipe = BaseChronosPipeline.from_pretrained(model, device_map="cpu")
    t0 = time.perf_counter()
    ctx = np.stack([Pa[:i].ravel()[-CTX:] for i in rows]).astype("float32")
    x = torch.tensor(ctx)
    if "chronos-2" in model:
        x = x[:, None, :]
    q, _ = pipe.predict_quantiles(x, prediction_length=24, quantile_levels=[0.1, 0.5, 0.9])
    q = (torch.stack([x_.reshape(24, 3) for x_ in q]) if isinstance(q, list) else q).numpy().reshape(len(rows), 24, 3)
    return {"median": q[:, :, 1], "q": q, "sec": time.perf_counter() - t0}


# =============================================================================
# 3. Search spaces (random search, fixed seed) -- configuration 0 = the setting of Lecture 2
# =============================================================================
def dnn_space(n=24, seed=SEED):
    rng = np.random.default_rng(seed)
    out = [{"n1": 128, "n2": 64, "act": "relu", "drop": 0.0, "lr": 1e-3, "wd": 1e-3, "l1": 0.0, "batch": 64,
            "load": True, "res": True, "fund": True, "p3": True}]
    for _ in range(n):
        out.append({"n1": int(rng.choice([64, 128, 256, 512])), "n2": int(rng.choice([0, 32, 64, 128, 256])),
                    "act": str(rng.choice(["relu", "softplus"])), "drop": float(rng.choice([0.0, 0.1, 0.2, 0.3])),
                    "lr": float(rng.choice([3e-4, 1e-3, 3e-3])), "wd": float(rng.choice([0.0, 1e-5, 1e-4, 1e-3])),
                    "l1": float(rng.choice([0.0, 1e-3, 1e-2, 1e-1])), "batch": int(rng.choice([32, 64, 128])),
                    "load": bool(rng.random() < 0.5), "res": bool(rng.random() < 0.5), "fund": bool(rng.random() < 0.5),
                    "p3": bool(rng.random() < 0.5)})
    return out


def xgb_space(n=24, seed=SEED + 1):
    rng = np.random.default_rng(seed)
    out = [{"n_est": 500, "eta": 0.05, "depth": 0, "leaves": 31, "grow": "lossguide", "mcw": 40, "sub": 1.0, "col": 1.0,
            "lam": 1.0, "obj": "reg:squarederror"}]
    for _ in range(n):
        out.append({"n_est": int(rng.choice([300, 600, 1000, 1500])), "eta": float(rng.choice([0.02, 0.05, 0.1])),
                    "depth": int(rng.choice([3, 4, 5, 6, 8])), "mcw": int(rng.choice([1, 5, 20, 50])),
                    "sub": float(rng.choice([0.6, 0.8, 1.0])), "col": float(rng.choice([0.6, 0.8, 1.0])),
                    "lam": float(rng.choice([0.1, 1.0, 10.0])),
                    "obj": str(rng.choice(["reg:squarederror", "reg:absoluteerror", "reg:pseudohubererror"]))})
    return out


DNN_SPACE, XGB_SPACE = dnn_space(), xgb_space()


# =============================================================================
# 4. Run (or load) the engine
# =============================================================================
def data_hash():
    h = hashlib.sha256(ENGINE_VERSION.encode())
    for f in ["power_da_prices_hourly_utc.csv", "generation_ro_mw_hourly_utc.csv", "generation_ro_mw_daily_cet.csv",
              "crossborder_ro_mw_daily_cet.csv", "eua_daily.csv"]:
        h.update(open(os.path.join(DATA, f), "rb").read())
    h.update(d(END).encode())
    h.update(json.dumps([DNN_SPACE, XGB_SPACE], sort_keys=True).encode())
    return h.hexdigest()[:16]


def vstack_blocks(res):
    return np.vstack([r["pred"] for r in res])


def lear_timing(n_days=8):
    """Compute cost of AW-LEAR: one day = 3 calibration windows x 24 LASSO paths (single core)."""
    from sklearn.linear_model import LassoLarsIC

    def lear_design(Pa, La, Ra, lo, i):
        m, s = mad_scale(Pa[lo - 7:i])
        mL, sL = mad_scale(La[lo - 7:i - 1])
        mR, sR = mad_scale(Ra[lo - 7:i - 1])
        rows = slice(lo, i + 1)
        bl = [np.arcsinh((shift_rows(Pa, k)[rows] - m) / s) for k in PLAGS]
        bl += [np.arcsinh((shift_rows(La, k)[rows] - mL) / sL) for k in XLAGS]
        bl += [np.arcsinh((shift_rows(Ra, k)[rows] - mR) / sR) for k in XLAGS]
        bl.append(np.eye(7)[DOW[rows]])
        return np.column_stack(bl), np.arcsinh((Pa[rows] - m) / s)
    t0 = time.perf_counter()
    for t in TDAYS[::max(1, len(TDAYS) // n_days)][:n_days]:
        i = IDX[t]
        for T in (364, 546, 728):
            X, Y = lear_design(P_, L_, R_, i - T, i)
            mu, sd = X[:-1].mean(0), X[:-1].std(0)
            sd[sd == 0] = 1
            for h in range(24):
                LassoLarsIC(criterion="aic", max_iter=2000).fit(((X - mu) / sd)[:-1], Y[:-1, h])
    return (time.perf_counter() - t0) / n_days


CACHE = os.path.join(HERE, "cache", "ml.pkl")
os.makedirs(os.path.dirname(CACHE), exist_ok=True)
KEY = data_hash()
C = None
if not FRESH and os.path.exists(CACHE):
    with open(CACHE, "rb") as fh:
        tmp = pickle.load(fh)
    if tmp.get("key") == KEY:
        C = tmp
if C is None:
    C = {"key": KEY}
    T0 = time.time()
    # 4.1 hyperparameter search on the validation year (quarterly refits, 1 seed)
    jobs = [(c, b) for c in range(len(DNN_SPACE)) for b in VB]
    r = Parallel(n_jobs=N_JOBS)(delayed(dnn_block)(P_, L_, R_, F_, a, b_, DNN_SPACE[c]) for c, (a, b_) in jobs)
    C["dnn_val_pred"] = [np.vstack([r[c * len(VB) + j]["pred"] for j in range(len(VB))]) for c in range(len(DNN_SPACE))]
    C["dnn_val_sec"] = [sum(r[c * len(VB) + j]["sec"] for j in range(len(VB))) for c in range(len(DNN_SPACE))]
    jobs = [(c, b) for c in range(len(XGB_SPACE)) for b in VB]
    r = Parallel(n_jobs=N_JOBS)(delayed(xgb_block)(P_, L_, R_, F_, a, b_, XGB_SPACE[c]) for c, (a, b_) in jobs)
    C["xgb_val_pred"] = [np.vstack([r[c * len(VB) + j]["pred"] for j in range(len(VB))]) for c in range(len(XGB_SPACE))]
    C["xgb_val_sec"] = [sum(r[c * len(VB) + j]["sec"] for j in range(len(VB))) for c in range(len(XGB_SPACE))]
    print("search done", round(time.time() - T0))
    # 4.2 data snooping experiment: every configuration also run on the test year (monthly refits, 1 seed); never used to choose
    jobs = [(c, b) for c in range(len(DNN_SPACE)) for b in MB]
    r = Parallel(n_jobs=N_JOBS)(delayed(dnn_block)(P_, L_, R_, F_, a, b_, DNN_SPACE[c]) for c, (a, b_) in jobs)
    C["dnn_test_all"] = [np.vstack([r[c * len(MB) + j]["pred"] for j in range(len(MB))]) for c in range(len(DNN_SPACE))]
    C["dnn_test_all_sec"] = [[r[c * len(MB) + j]["sec"] for j in range(len(MB))] for c in range(len(DNN_SPACE))]
    jobs = [(c, b) for c in range(len(XGB_SPACE)) for b in MB]
    r = Parallel(n_jobs=N_JOBS)(delayed(xgb_block)(P_, L_, R_, F_, a, b_, XGB_SPACE[c]) for c, (a, b_) in jobs)
    C["xgb_test_all"] = [np.vstack([r[c * len(MB) + j]["pred"] for j in range(len(MB))]) for c in range(len(XGB_SPACE))]
    C["xgb_test_all_sec"] = [[r[c * len(MB) + j]["sec"] for j in range(len(MB))] for c in range(len(XGB_SPACE))]
    print("snooping runs done", round(time.time() - T0))
    with open(CACHE, "wb") as fh:
        pickle.dump(C, fh)

# chosen configurations: lowest MAE on the validation year (the test year plays no role)
AV = P_[[IDX[t] for t in VDAYS]]
VAL_DNN = np.array([np.mean(np.abs(AV - p)) for p in C["dnn_val_pred"]])
VAL_XGB = np.array([np.mean(np.abs(AV - p)) for p in C["xgb_val_pred"]])
BEST_DNN, BEST_XGB = int(np.argmin(VAL_DNN)), int(np.argmin(VAL_XGB))
CFG_DNN, CFG_XGB = DNN_SPACE[BEST_DNN], XGB_SPACE[BEST_XGB]

rows_all = np.array([IDX[t] for t in TDAYS])
STEPS = {
    "dnn_main": lambda: Parallel(n_jobs=N_JOBS)(delayed(dnn_block)(P_, L_, R_, F_, a, b_, CFG_DNN, (1, 2, 3, 4), keep=True) for a, b_ in MB),
    "xgb_main": lambda: Parallel(n_jobs=N_JOBS)(delayed(xgb_block)(P_, L_, R_, F_, a, b_, CFG_XGB, shap=True) for a, b_ in MB),
    # retraining frequency and window (XGBoost, chosen configuration)
    "xgb_quarterly": lambda: Parallel(n_jobs=N_JOBS)(delayed(xgb_block)(P_, L_, R_, F_, a, b_, CFG_XGB) for a, b_ in blocks_of(TDAYS, "Q")),
    "xgb_once": lambda: [xgb_block(P_, L_, R_, F_, MB[0][0], MB[-1][1], CFG_XGB)],
    "xgb_roll365": lambda: Parallel(n_jobs=N_JOBS)(delayed(xgb_block)(P_, L_, R_, F_, a, b_, CFG_XGB, lo=a - 365) for a, b_ in MB),
    "xgb_roll730": lambda: Parallel(n_jobs=N_JOBS)(delayed(xgb_block)(P_, L_, R_, F_, a, b_, CFG_XGB, lo=a - 730) for a, b_ in MB),
    # look-ahead pitfall: same-day realised load and wind+solar as features; shuffled cross-validation
    "xgb_leak": lambda: Parallel(n_jobs=N_JOBS)(delayed(xgb_block)(P_, L_, R_, F_, a, b_, CFG_XGB, leak=True) for a, b_ in MB),
    "xgb_shuffled": lambda: xgb_cv_shuffled(P_, L_, R_, F_, CFG_XGB),
    # classifiers of spikes and negative prices
    "clf_spike": lambda: Parallel(n_jobs=N_JOBS)(delayed(clf_block)(P_, L_, R_, F_, THETA, a, b_, "spike") for a, b_ in MB),
    "clf_neg": lambda: Parallel(n_jobs=N_JOBS)(delayed(clf_block)(P_, L_, R_, F_, THETA, a, b_, "neg") for a, b_ in MB),
    # foundation models, zero-shot
    "chronos_bolt": lambda: chronos_forecasts(P_, rows_all, "amazon/chronos-bolt-small"),
    "chronos2": lambda: chronos_forecasts(P_, rows_all, "amazon/chronos-2"),
    "lear_sec_day": lear_timing,
    "chronos2_val": lambda: chronos_forecasts(P_, np.array([IDX[t] for t in VDAYS]), "amazon/chronos-2"),
    "bolt_val": lambda: chronos_forecasts(P_, np.array([IDX[t] for t in VDAYS]), "amazon/chronos-bolt-small"),
}
for name, fn in STEPS.items():
    if name not in C:
        t0_ = time.time()
        C[name] = fn()
        print(name, "done in", round(time.time() - t0_), "s")
        with open(CACHE, "wb") as fh:
            pickle.dump(C, fh)
print("engine ready; chosen DNN config", BEST_DNN, CFG_DNN, "| chosen XGB config", BEST_XGB, CFG_XGB)


# =============================================================================
# 5. Point forecasts on the test year: accuracy, Diebold-Mariano, combinations
# =============================================================================
M = {k: B[k] for k in ["naive", "aw_arx", "aw_lear", "gbm2", "mlp2", "ens4"]}
M["dnn"] = vstack_blocks(C["dnn_main"])
M["xgb"] = vstack_blocks(C["xgb_main"])
M["dnn1"] = C["dnn_test_all"][BEST_DNN]                         # chosen DNN, one seed (as in the search)
M["dnn0"] = C["dnn_test_all"][0]                                # the L2 network re-implemented, one seed
M["xgb0"] = C["xgb_test_all"][0]
M["bolt"] = C["chronos_bolt"]["median"]
M["chr2"] = C["chronos2"]["median"]
M["ens_ld"] = 0.5 * (M["aw_lear"] + M["dnn"])
M["ens_lx"] = 0.5 * (M["aw_lear"] + M["xgb"])
M["ens_ldx"] = (M["aw_lear"] + M["dnn"] + M["xgb"]) / 3
M["ens_t4"] = np.mean([M["aw_arx"], M["aw_lear"], M["dnn"], M["xgb"]], 0)
M["ens_lc"] = 0.5 * (M["aw_lear"] + M["chr2"])
M["ens_t5"] = np.mean([M["aw_arx"], M["aw_lear"], M["dnn"], M["xgb"], M["chr2"]], 0)
ORDER = ["naive", "aw_arx", "aw_lear", "ens4", "gbm2", "mlp2", "xgb0", "dnn0", "xgb", "dnn", "bolt", "chr2",
         "ens_ld", "ens_lx", "ens_ldx", "ens_t4", "ens_lc", "ens_t5"]
E = {k: A - M[k] for k in ORDER}


def acc(F):
    e = A - F
    return {"mae": np.mean(np.abs(e)), "rmse": np.sqrt(np.mean(e ** 2))}


NAIVE_MAE = acc(M["naive"])["mae"]
LEAR_MAE = acc(M["aw_lear"])["mae"]
N["acc"] = {}
for k in ORDER:
    a_ = acc(M[k])
    N["acc"][k] = {"mae": fl(a_["mae"], 2), "rmse": fl(a_["rmse"], 2), "rmae": fl(a_["mae"] / NAIVE_MAE, 3),
                   "vs_lear": fl((1 - a_["mae"] / LEAR_MAE) * 100, 1)}
N["acc"]["dnn1"] = {"mae": fl(acc(M["dnn1"])["mae"], 2)}
best = min(ORDER, key=lambda k: N["acc"][k]["mae"])
N["best"] = {"key": best, "mae": N["acc"][best]["mae"], "rmae": N["acc"][best]["rmae"], "vs_lear": N["acc"][best]["vs_lear"]}
N["test"] = {"n_hours": int(A.size), "mean": fl(A.mean(), 2), "max": fl(A.max(), 2)}


def nw_var(x, lags=7):
    x = x - x.mean()
    n = len(x)
    v = x @ x / n
    for k in range(1, lags + 1):
        v += 2 * (1 - k / (lags + 1)) * (x[k:] @ x[:-k]) / n
    return v


def dm(ea, eb, lags=7):
    """One-sided DM test (as in L2): H1 = model b more accurate than model a; loss = daily mean |error| over 24 hours."""
    dlt = np.mean(np.abs(ea), 1) - np.mean(np.abs(eb), 1)
    stat = dlt.mean() / np.sqrt(nw_var(dlt, lags) / len(dlt))
    return stat, 1 - stats.norm.cdf(stat)


DM_MODELS = ["naive", "aw_lear", "ens4", "xgb", "dnn", "bolt", "chr2", "ens_ldx", "ens_t4", "ens_lc", "ens_t5"]
DMP = np.full((len(DM_MODELS), len(DM_MODELS)), np.nan)
for a_, ka in enumerate(DM_MODELS):
    for b_, kb in enumerate(DM_MODELS):
        if a_ != b_:
            DMP[a_, b_] = dm(E[ka], E[kb])[1]
N["dm"] = {}
for ka, kb in [("aw_lear", "xgb"), ("xgb", "aw_lear"), ("aw_lear", "dnn"), ("dnn", "aw_lear"), ("aw_lear", "ens_ld"),
               ("aw_lear", "ens_lx"), ("aw_lear", "ens_ldx"), ("aw_lear", "ens_t4"), ("ens4", "ens_t4"), ("ens4", "ens_ldx"),
               ("naive", "chr2"), ("aw_lear", "chr2"), ("chr2", "aw_lear"), ("gbm2", "xgb"), ("mlp2", "dnn"), ("naive", "bolt"),
               ("bolt", "naive"), ("ens4", "ens_t5"), ("ens_t4", "ens_t5"),
               ("chr2", "ens_lc"), ("chr2", "ens_t5"), ("aw_lear", "ens4"), ("aw_lear", "aw_arx"), ("aw_lear", "ens_t5"),
               ("aw_lear", "gbm2"), ("aw_lear", "mlp2"), ("aw_lear", "bolt"), ("ens4", "chr2"), ("ens_t4", "chr2"), ("bolt", "chr2")]:
    s_, p_ = dm(E[ka], E[kb])
    N["dm"][f"{ka}__{kb}"] = {"stat": fl(s_, 2), "p": fl(p_, 4)}
N["dm"]["n_beat_lear"] = int(sum(DMP[DM_MODELS.index("aw_lear"), j] < 0.05 for j in range(len(DM_MODELS))))

# combinations: error correlation and the weight curve (illustration only: the weight is NOT chosen on the test year)
cor = {}
for k in ["dnn", "xgb", "chr2"]:
    cor[k] = fl(np.corrcoef(E["aw_lear"].ravel(), E[k].ravel())[0, 1], 2)
cor["dnn_xgb"] = fl(np.corrcoef(E["dnn"].ravel(), E["xgb"].ravel())[0, 1], 2)
WGRID = np.linspace(0, 1, 21)
WCURVE = {k: np.array([np.mean(np.abs(A - (w * M[k] + (1 - w) * M["aw_lear"]))) for w in WGRID]) for k in ["dnn", "xgb"]}
N["combo"] = {"corr": cor, "sd_lear": fl(E["aw_lear"].std(), 2), "sd_dnn": fl(E["dnn"].std(), 2), "sd_xgb": fl(E["xgb"].std(), 2),
              "w_best_xgb": fl(WGRID[np.argmin(WCURVE["xgb"])], 2), "w_best_dnn": fl(WGRID[np.argmin(WCURVE["dnn"])], 2),
              "mae_wbest_xgb": fl(WCURVE["xgb"].min(), 2)}
# expected MAE ratio if errors were Gaussian with this correlation: sqrt((1+rho)/2) for equal variances
N["combo"]["theory_ratio_xgb"] = fl(np.sqrt((E["aw_lear"].var() + E["xgb"].var() + 2 * np.cov(E["aw_lear"].ravel(), E["xgb"].ravel())[0, 1]) / 4)
                                    / E["aw_lear"].std(), 3)

# by month and by hour
TM = TDAYS.to_period("M")
MONTHS_T = sorted(set(TM))
BYMONTH = {k: np.array([np.mean(np.abs(E[k][TM == mm])) for mm in MONTHS_T]) for k in ORDER}
BYHOUR = {k: np.mean(np.abs(E[k]), 0) for k in ORDER}
N["bymonth"] = {"n_xgb_beats_lear": int((BYMONTH["xgb"] < BYMONTH["aw_lear"]).sum()),
                "n_dnn_beats_lear": int((BYMONTH["dnn"] < BYMONTH["aw_lear"]).sum()),
                "n_ldx_beats_lear": int((BYMONTH["ens_ldx"] < BYMONTH["aw_lear"]).sum()),
                "worst_month": str(MONTHS_T[int(np.argmax(BYMONTH["aw_lear"]))]),
                "n_months": len(MONTHS_T)}
N["byhour"] = {"xgb_beats_lear_h": int((BYHOUR["xgb"] < BYHOUR["aw_lear"]).sum()),
               "dnn_beats_lear_h": int((BYHOUR["dnn"] < BYHOUR["aw_lear"]).sum()),
               "ldx_beats_lear_h": int((BYHOUR["ens_ldx"] < BYHOUR["aw_lear"]).sum()),
               "chr2_worst_h": int(np.argmax(BYHOUR["chr2"]))}

# =============================================================================
# 6. Hyperparameter search, early stopping, data snooping
# =============================================================================
TEST_DNN = np.array([np.mean(np.abs(A - p)) for p in C["dnn_test_all"]])
TEST_XGB = np.array([np.mean(np.abs(A - p)) for p in C["xgb_test_all"]])
naive_val = np.mean(np.abs(AV - np.where(np.isin(DOW[[IDX[t] for t in VDAYS]], [0, 5, 6])[:, None],
                                          P_[[IDX[t] - 7 for t in VDAYS]], P_[[IDX[t] - 1 for t in VDAYS]])))
EPOCHS = np.concatenate([r_["epochs"] for r_ in C["dnn_main"]])
N["search"] = {"n_cfg": len(DNN_SPACE), "n_random": len(DNN_SPACE) - 1, "n_val_refits": len(VB),
               "naive_val": fl(naive_val, 2),
               "dnn": {"best": BEST_DNN, "val_best": fl(VAL_DNN.min(), 2), "val_l2": fl(VAL_DNN[0], 2), "val_worst": fl(VAL_DNN.max(), 2),
                       "rank_l2": int((VAL_DNN < VAL_DNN[0]).sum() + 1), "test_chosen": fl(TEST_DNN[BEST_DNN], 2),
                       "test_best": fl(TEST_DNN.min(), 2), "test_best_cfg": int(np.argmin(TEST_DNN)),
                       "test_l2": fl(TEST_DNN[0], 2), "test_worst": fl(TEST_DNN.max(), 2),
                       "snoop_gain": fl(TEST_DNN[BEST_DNN] - TEST_DNN.min(), 2),
                       "snoop_pct": fl((TEST_DNN[BEST_DNN] - TEST_DNN.min()) / TEST_DNN[BEST_DNN] * 100, 1),
                       "rank_chosen_on_test": int((TEST_DNN < TEST_DNN[BEST_DNN]).sum() + 1),
                       "spearman": fl(stats.spearmanr(VAL_DNN, TEST_DNN)[0], 2),
                       "n_test_below_lear": int((TEST_DNN < LEAR_MAE).sum()),
                       "epochs_med": int(np.median(EPOCHS)), "epochs_min": int(EPOCHS.min()), "epochs_max": int(EPOCHS.max()),
                       "cfg": CFG_DNN, "n_inputs": int(len(C["dnn_main"][0]["names"])),
                       "n_params": int(sum(v.numel() for v in C["dnn_main"][0]["models"][0].values()))},
               "xgb": {"best": BEST_XGB, "val_best": fl(VAL_XGB.min(), 2), "val_l2": fl(VAL_XGB[0], 2), "val_worst": fl(VAL_XGB.max(), 2),
                       "rank_l2": int((VAL_XGB < VAL_XGB[0]).sum() + 1), "test_chosen": fl(TEST_XGB[BEST_XGB], 2),
                       "test_best": fl(TEST_XGB.min(), 2), "test_best_cfg": int(np.argmin(TEST_XGB)), "test_l2": fl(TEST_XGB[0], 2),
                       "test_worst": fl(TEST_XGB.max(), 2),
                       "snoop_gain": fl(TEST_XGB[BEST_XGB] - TEST_XGB.min(), 2),
                       "snoop_pct": fl((TEST_XGB[BEST_XGB] - TEST_XGB.min()) / TEST_XGB[BEST_XGB] * 100, 1),
                       "rank_chosen_on_test": int((TEST_XGB < TEST_XGB[BEST_XGB]).sum() + 1),
                       "spearman": fl(stats.spearmanr(VAL_XGB, TEST_XGB)[0], 2),
                       "n_test_below_lear": int((TEST_XGB < LEAR_MAE).sum()), "cfg": CFG_XGB}}
N["search"]["dnn"]["cfg"]["lr_s"] = f"{CFG_DNN['lr']:.0e}".replace("e-0", "e-")
_curve = C["dnn_main"][-1]["curves"][0]
N["curve"] = {"best_ep": int(np.argmin(_curve[1]) + 1), "n_ep": len(_curve[1]), "month": str(MONTHS_T[-1]),
              "tr_end": fl(_curve[0][-1], 2), "v_best": fl(min(_curve[1]), 2), "v_end": fl(_curve[1][-1], 2)}

# =============================================================================
# 7. Compute cost (single core, measured on this machine) versus gain
# =============================================================================
sec = {"naive": 0.0, "aw_lear": C["lear_sec_day"] * len(TDAYS),
       "xgb": sum(r_["sec"] for r_ in C["xgb_main"]), "dnn": sum(r_["sec"] for r_ in C["dnn_main"]),
       "bolt": C["chronos_bolt"]["sec"], "chr2": C["chronos2"]["sec"]}
sec["ens_ldx"] = sec["aw_lear"] + sec["xgb"] + sec["dnn"]
sec["ens_lx"] = sec["aw_lear"] + sec["xgb"]
sec["ens_lc"] = sec["aw_lear"] + sec["chr2"]
sec["search"] = float(np.sum(C["dnn_val_sec"]) + np.sum(C["xgb_val_sec"]))
N["found"] = {"val_chr2": fl(np.mean(np.abs(AV - C["chronos2_val"]["median"])), 2),
              "val_bolt": fl(np.mean(np.abs(AV - C["bolt_val"]["median"])), 2),
              "cov80": fl(((A >= C["chronos2"]["q"][:, :, 0]) & (A <= C["chronos2"]["q"][:, :, 2])).mean() * 100, 1),
              "ctx_days": CTX // 24, "ctx": CTX, "chr2_beats_lear_h": int((BYHOUR["chr2"] < BYHOUR["aw_lear"]).sum()),
              "chr2_beats_lear_m": int((BYMONTH["chr2"] < BYMONTH["aw_lear"]).sum())}
N["cost"] = {k: fl(v / 60, 1) for k, v in sec.items()}
N["cost"]["lear_day_s"] = fl(C["lear_sec_day"], 1)
N["cost"]["dnn_refit_s"] = fl(sec["dnn"] / len(MB) / 4, 1)
N["cost"]["xgb_refit_s"] = fl(sec["xgb"] / len(MB), 1)
N["cost"]["cores"] = os.cpu_count()

# =============================================================================
# 8. Explanations: SHAP values of the boosted trees, permutation importance of the DNN input blocks
# =============================================================================
SH = np.concatenate([r_["shap"] for r_ in C["xgb_main"]], 0)               # 365 x 24 x (20 + bias)
XS = np.concatenate([r_["X"] for r_ in C["xgb_main"]], 0)
MS = np.array([r_["m"] for r_ in C["xgb_main"] for _ in range(r_["pred"].shape[0])])
SS = np.array([r_["s"] for r_ in C["xgb_main"] for _ in range(r_["pred"].shape[0])])
mabs = np.abs(SH[:, :, :-1]).reshape(-1, len(XGB_NAMES)).mean(0)
share = mabs / mabs.sum() * 100
GROUPS = {"price": [0, 1, 2, 3, 4, 5, 6, 7], "load": [8, 9, 12], "res": [10, 11, 13], "fund": [14, 15, 16, 17], "cal": [18, 19]}
N["shap"] = {"top": [XGB_NAMES[j] for j in np.argsort(-share)[:5]], "top_share": [fl(share[j], 1) for j in np.argsort(-share)[:5]],
             "groups": {g: fl(share[ix].sum(), 1) for g, ix in GROUPS.items()},
             "check": fl(np.max(np.abs(SH.sum(2) - np.arcsinh((M["xgb"] - MS[:, None]) / SS[:, None]))), 6)}
# RES(d-2,h) dependence: contribution by level of wind+solar, solar hours vs others
res_j = XGB_NAMES.index("RES(d-2,h)")
N["shap"]["res_corr"] = fl(np.corrcoef(XS[:, :, res_j].ravel(), SH[:, :, res_j].ravel())[0, 1], 2)

# first split of the first tree of the last monthly refit (for the tree slide)

_a, _b = MB[-1]
_tr = np.arange(FIRST, _a)
_m, _s = mad_scale(P_[_tr])
_mdl = _xgb(CFG_XGB, SEED).fit(gbm_rows(P_, L_, R_, F_, _tr).reshape(-1, len(XGB_NAMES)), np.arcsinh((P_[_tr] - _m) / _s).ravel())
_td = _mdl.get_booster().trees_to_dataframe()
_root = _td[(_td.Tree == 0) & (_td.Node == 0)].iloc[0]
N["tree"] = {"feat": XGB_NAMES[int(_root.Feature[1:])], "split": fl(_root.Split, 1), "n_trees": int(_td.Tree.nunique()),
             "n_leaves_t0": int(((_td.Tree == 0) & (_td.Feature == "Leaf")).sum()), "n_rows": int(len(_tr) * 24),
             "month": str(MONTHS_T[-1])}
assert np.allclose(_m + _s * np.sinh(_mdl.predict(gbm_rows(P_, L_, R_, F_, np.arange(_a, _b + 1)).reshape(-1, len(XGB_NAMES)))).reshape(-1, 24),
                   M["xgb"][_a - MB[0][0]:], atol=1e-3)

# DNN permutation importance by input block (5 random permutations of the test days, block by block)
BLOCKS_DNN = ["price d-1", "price d-2", "price d-3", "price d-7", "load", "wind+solar", "fund", "day of week"]
rng = np.random.default_rng(SEED)
perms = [rng.permutation(len(TDAYS)) for _ in range(5)]
names0 = C["dnn_main"][0]["names"]
blk_cols = {b: np.where(np.isin(names0, ["hydro", "nuclear", "net imports", "carbon"] if b == "fund" else [b]))[0] for b in BLOCKS_DNN}
blk_cols = {b: c for b, c in blk_cols.items() if len(c)}
XM = []
for j, (a_, b_) in enumerate(MB):
    r_ = C["dnn_main"][j]
    XM.append(dnn_inputs(P_, L_, R_, F_, rows_all, r_["sc"], CFG_DNN)[0])
base_chk = np.vstack([dnn_predict_from(C["dnn_main"][j]["models"], CFG_DNN, XM[j][a_ - MB[0][0]:b_ - MB[0][0] + 1],
                                       C["dnn_main"][j]["mu"], C["dnn_main"][j]["sg"], C["dnn_main"][j]["sc"]) for j, (a_, b_) in enumerate(MB)])
assert np.max(np.abs(base_chk - M["dnn"])) < 1e-3


def perm_mae(b, pm):
    out = []
    for j, (a_, b_) in enumerate(MB):
        X = XM[j].copy()
        X[:, blk_cols[b]] = XM[j][pm][:, blk_cols[b]]
        sl = slice(a_ - MB[0][0], b_ - MB[0][0] + 1)
        out.append(dnn_predict_from(C["dnn_main"][j]["models"], CFG_DNN, X[sl], C["dnn_main"][j]["mu"], C["dnn_main"][j]["sg"],
                                    C["dnn_main"][j]["sc"]))
    return np.mean(np.abs(A - np.vstack(out)))


PI = {b: float(np.mean([perm_mae(b, pm) for pm in perms]) - acc(M["dnn"])["mae"]) for b in blk_cols}
N["perm"] = {b.replace(" ", "_").replace("+", "_").replace("-", ""): fl(v, 2) for b, v in PI.items()}
N["perm"]["top"] = max(PI, key=PI.get)

# =============================================================================
# 9. Spikes and negative prices
# =============================================================================
from sklearn.metrics import roc_auc_score, roc_curve  # noqa: E402

TH_T = THETA[rows_all]
Y_SP = (A > TH_T[:, None]).astype(int)
Y_NG = (A <= 0).astype(int)
CS = {"xgb": np.vstack([r_["xgb"] for r_ in C["clf_spike"]]), "logit": np.vstack([r_["logit"] for r_ in C["clf_spike"]])}
CN = {"xgb": np.vstack([r_["xgb"] for r_ in C["clf_neg"]]), "logit": np.vstack([r_["logit"] for r_ in C["clf_neg"]])}
past = np.stack([P_[rows_all - k] for k in range(1, 8)], 0)                      # prices of d-1..d-7, same hour
CS["persist"] = (past > TH_T[None, :, None]).mean(0)
CN["persist"] = (past <= 0).mean(0)
CS["lear"] = M["aw_lear"] - TH_T[:, None]                                        # a score, not a probability
CN["lear"] = -M["aw_lear"]


def cls_metrics(y, p, prob=True, cut=0.5):
    y, p = y.ravel(), p.ravel()
    yhat = p > (cut if prob else 0.0)
    tp, fp, fn = int((yhat & (y == 1)).sum()), int((yhat & (y == 0)).sum()), int((~yhat & (y == 1)).sum())
    prec = tp / (tp + fp) if tp + fp else np.nan
    rec = tp / (tp + fn) if tp + fn else np.nan
    out = {"auc": fl(roc_auc_score(y, p), 3), "prec": fl(prec, 3), "rec": fl(rec, 3),
           "f1": fl(2 * prec * rec / (prec + rec), 3) if tp else 0.0}
    if prob:
        out["brier"] = fl(np.mean((p - y) ** 2), 4)
    return out


N["spike"] = {"theta_min": fl(TH_T.min(), 1), "theta_max": fl(TH_T.max(), 1), "share_test": fl(Y_SP.mean() * 100, 1),
              "n_test": int(Y_SP.sum()), "share_train_last": fl(C["clf_spike"][-1]["share_train"] * 100, 1),
              "brier_clim": fl(np.mean((Y_SP.mean() - Y_SP) ** 2), 4)}
N["neg"] = {"share_test": fl(Y_NG.mean() * 100, 1), "n_test": int(Y_NG.sum()), "share_train_last": fl(C["clf_neg"][-1]["share_train"] * 100, 1),
            "n_days": int(Y_NG.any(1).sum())}
for k in ["xgb", "logit", "persist", "lear"]:
    N["spike"][k] = cls_metrics(Y_SP, CS[k], prob=k != "lear")
    N["neg"][k] = cls_metrics(Y_NG, CN[k], prob=k != "lear")
# hour profile of the spikes
N["spike"]["peak_h"] = int(np.argmax(Y_SP.mean(0)))
N["spike"]["peak_h_share"] = fl(Y_SP.mean(0).max() * 100, 1)
N["neg"]["peak_h"] = int(np.argmax(Y_NG.mean(0)))

# cost-loss decision: move 1 MWh out of an alerted hour to an hour priced at the threshold; value = P - theta - C
C_ACT = 30.0                                                                       # assumed cost of acting, EUR/MWh (definition)
vrows = np.array([IDX[t] for t in VDAYS])
PV, THV = P_[vrows], THETA[vrows][:, None]
LBAR = float((PV - THV)[PV > THV].mean())                                          # mean excess in spike hours, validation year
VALUE = A - TH_T[:, None] - C_ACT


def act_value(pi, cut):
    return float(VALUE[pi > cut].sum())


CUTS = np.linspace(0.02, 0.98, 49)
VCURVE = np.array([act_value(CS["xgb"], c) for c in CUTS]) / 1000
N["decision"] = {"C": C_ACT, "Lbar": fl(LBAR, 1), "cut": fl(C_ACT / LBAR, 3), "v_cut": fl(act_value(CS["xgb"], C_ACT / LBAR) / 1000, 1),
                 "v_half": fl(act_value(CS["xgb"], 0.5) / 1000, 1), "v_perfect": fl(VALUE[VALUE > 0].sum() / 1000, 1),
                 "v_persist": fl(act_value(CS["persist"], C_ACT / LBAR) / 1000, 1),
                 "v_logit": fl(act_value(CS["logit"], C_ACT / LBAR) / 1000, 1),
                 "v_always_spike": fl(VALUE[Y_SP == 1].sum() / 1000, 1),
                 "n_alerts_cut": int((CS["xgb"] > C_ACT / LBAR).sum()), "n_alerts_half": int((CS["xgb"] > 0.5).sum()),
                 "best_cut": fl(CUTS[np.argmax(VCURVE)], 2)}

# =============================================================================
# 10. Studiu de caz: the highest price of the test year
# =============================================================================
kd, kh = np.unravel_index(np.argmax(A), A.shape)
CDAY = TDAYS[kd]
N["case"] = {"day": d(CDAY), "hour": int(kh), "price": fl(A[kd, kh], 2), "theta": fl(TH_T[kd], 1),
             "p_xgb": fl(CS["xgb"][kd, kh], 3), "p_logit": fl(CS["logit"][kd, kh], 3), "p_persist": fl(CS["persist"][kd, kh], 3),
             "day_mean": fl(A[kd].mean(), 2), "n_spike_h": int(Y_SP[kd].sum()),
             "prev_max": fl(P_[IDX[CDAY] - 1].max(), 2), "prev_mean": fl(P_[IDX[CDAY] - 1].mean(), 2)}
for k in ["naive", "aw_lear", "xgb", "dnn", "chr2", "ens_ldx", "ens4"]:
    N["case"][k] = fl(M[k][kd, kh], 2)
    N["case"]["mae_" + k] = fl(np.mean(np.abs(E[k][kd])), 2)
CW0 = max(0, kd - 3)
CWS = slice(CW0, min(len(TDAYS), CW0 + 7))
N["case"]["week_start"], N["case"]["week_end"] = d(TDAYS[CWS.start]), d(TDAYS[CWS.stop - 1])
for k in ["naive", "aw_lear", "xgb", "dnn", "ens_ldx", "ens4", "chr2"]:
    N["case"]["wmae_" + k] = fl(np.mean(np.abs(E[k][CWS])), 2)
N["case"]["wmean"] = fl(A[CWS].mean(), 2)
N["case"]["w_spike_h"] = int(Y_SP[CWS].sum())
N["case"]["w_alerts"] = int((CS["xgb"][CWS] > C_ACT / LBAR).sum())
N["case"]["w_hits"] = int(((CS["xgb"][CWS] > C_ACT / LBAR) & (Y_SP[CWS] == 1)).sum())
# local explanation of the XGBoost forecast at the peak hour, rescaled to EUR/MWh (proportional allocation, Appendix)
phi = SH[kd, kh, :-1]
y0 = SH[kd, kh, -1]
yhat = y0 + phi.sum()
m_, s_ = MS[kd], SS[kd]
P0, PH = m_ + s_ * np.sinh(y0), m_ + s_ * np.sinh(yhat)
phi_eur = phi * (PH - P0) / (yhat - y0)
ordr = np.argsort(-np.abs(phi_eur))
N["case"]["base_eur"] = fl(P0, 2)
N["case"]["xgb_eur"] = fl(PH, 2)
N["case"]["top_feat"] = [XGB_NAMES[j] for j in ordr[:3]]
N["case"]["top_eur"] = [fl(phi_eur[j], 1) for j in ordr[:3]]
N["case"]["top_val"] = [fl(XS[kd, kh, j], 1) for j in ordr[:3]]
N["case"]["load_d2_h"] = fl(XS[kd, kh, XGB_NAMES.index("L(d-2,h)")], 0)
N["case"]["res_d2_h"] = fl(XS[kd, kh, XGB_NAMES.index("RES(d-2,h)")], 0)
N["case"]["load_d_h"] = fl(L_[IDX[CDAY], kh], 0)
N["case"]["res_d_h"] = fl(R_[IDX[CDAY], kh], 0)

# =============================================================================
# 11. Pitfalls on the same test year
# =============================================================================
PF = {"honest": M["xgb"], "leak": vstack_blocks(C["xgb_leak"]), "shuffled": C["xgb_shuffled"][rows_all],
      "quarterly": vstack_blocks(C["xgb_quarterly"]), "once": vstack_blocks(C["xgb_once"]),
      "roll365": vstack_blocks(C["xgb_roll365"]), "roll730": vstack_blocks(C["xgb_roll730"])}
PIT_RAW = {k: acc(v)["mae"] for k, v in PF.items()}            # unrounded MAEs: the percentages below use these
N["pit"] = {k: fl(v, 2) for k, v in PIT_RAW.items()}
N["pit"]["leak_gain"] = fl((1 - PIT_RAW["leak"] / PIT_RAW["honest"]) * 100, 1)
N["pit"]["shuf_gain"] = fl((1 - PIT_RAW["shuffled"] / PIT_RAW["honest"]) * 100, 1)
N["pit"]["leak_rmae"] = fl(N["pit"]["leak"] / NAIVE_MAE, 3)
N["pit"]["shuf_rmae"] = fl(N["pit"]["shuffled"] / NAIVE_MAE, 3)
N["pit"]["once_loss"] = fl((PIT_RAW["once"] / PIT_RAW["honest"] - 1) * 100, 1)
N["pit"]["n_quarters"] = len(C["xgb_quarterly"])
sl_q = [np.mean(np.abs(A[TM == mm] - PF["once"][TM == mm])) - np.mean(np.abs(A[TM == mm] - PF["honest"][TM == mm])) for mm in MONTHS_T]
N["pit"]["once_last_q"] = fl(np.mean(sl_q[-3:]), 2)
N["pit"]["once_first_q"] = fl(np.mean(sl_q[:3]), 2)

# =============================================================================
# 12. Leakage self-check: recompute with everything after gate closure deleted (NaN) or replaced by nonsense (1e4)
# =============================================================================
def corrupt(i, fill=np.nan):
    Pc, Lc, Rc = P_.copy(), L_.copy(), R_.copy()
    Pc[i:] = fill
    Lc[i - 1:] = fill
    Rc[i - 1:] = fill
    raw = FUND_RAW.copy()
    raw.loc[CAL[i - 1]:] = fill
    return Pc, Lc, Rc, raw.ffill().shift(2).reindex(CAL).values.astype(float)


def pert(j, fill):
    a_, b_ = MB[j]
    Pc, Lc, Rc, Fc = corrupt(a_, fill)
    k0 = a_ - MB[0][0]
    dx = np.max(np.abs(xgb_block(Pc, Lc, Rc, Fc, a_, a_, CFG_XGB)["pred"][0] - M["xgb"][k0]))
    dd = np.max(np.abs(dnn_block(Pc, Lc, Rc, Fc, a_, a_, CFG_DNN, (1, 2, 3, 4))["pred"][0] - M["dnn"][k0]))
    dc = np.max(np.abs(clf_block(Pc, Lc, Rc, Fc, THETA, a_, a_, "spike")["xgb"][0] - CS["xgb"][k0]))
    return dx, dd, dc


LCACHE = os.path.join(HERE, "cache", "leak.pkl")
LK = None
if not FRESH and os.path.exists(LCACHE):
    with open(LCACHE, "rb") as fh:
        tmp = pickle.load(fh)
    if tmp.get("key") == KEY:
        LK = tmp["r"]
if LK is None:
    LK = Parallel(n_jobs=N_JOBS)(delayed(pert)(j, f_) for j in range(len(MB)) for f_ in (np.nan, 1e4))
    with open(LCACHE, "wb") as fh:
        pickle.dump({"key": KEY, "r": LK}, fh)
mx = np.max(np.array(LK), 0)
assert mx[0] < 1e-6 and mx[1] < 1e-3 and mx[2] < 1e-6, f"leakage self-check failed: {mx}"
# foundation model: the context is built from rows strictly before the delivery day (assert on the code path)
for i in rows_all[::30]:
    assert len(P_[:i].ravel()[-CTX:]) == CTX and i - 1 < i
N["leak"] = {"n_months": len(MB), "n_runs": len(LK), "max_xgb": float(mx[0]), "max_dnn": float(mx[1]), "max_clf": float(mx[2]),
             "passed": True}
print("leakage self-check PASSED", N["leak"])

# group research: case study C7 numbers (computed by the case notebook; copied, not retyped)
with open(os.path.join(REPO, "cases", "C7_spike_early_warning", "numbers.json")) as fh:
    N["c7"] = json.load(fh)
N["l2"] = {"aw_lear": N2["acc"]["aw_lear"]["mae"], "ens_all": N2["acc"]["ens_all"]["mae"], "gbm": N2["acc"]["gbm"]["mae"],
           "mlp": N2["acc"]["mlp"]["mae"], "naive": N2["acc"]["naive"]["mae"], "ens_rmae": N2["acc"]["ens_all"]["rmae"],
           "lear_rmae": N2["acc"]["aw_lear"]["rmae"]}

# =============================================================================
# Charts: one set per language
# =============================================================================
LAB = {"naive": ("Naive", "Naiv"), "aw_arx": ("AW-ARX", "AW-ARX"), "aw_lear": ("AW-LEAR", "AW-LEAR"),
       "ens4": ("Ens. of 4 (L2)", "Ans. de 4 (cursul 2)"), "gbm2": ("GBM (L2)", "GBM (cursul 2)"), "mlp2": ("MLP (L2)", "MLP (cursul 2)"),
       "xgb": ("XGBoost", "XGBoost"), "dnn": ("DNN", "DNN"), "bolt": ("Chronos-Bolt", "Chronos-Bolt"), "chr2": ("Chronos-2", "Chronos-2"),
       "ens_ld": ("LEAR+DNN", "LEAR+DNN"), "ens_lx": ("LEAR+XGBoost", "LEAR+XGBoost"), "ens_ldx": ("LEAR+DNN+XGBoost", "LEAR+DNN+XGBoost"),
       "ens_t4": ("Ens. of 4, tuned ML", "Ans. de 4, ML optimizat"), "ens_t5": ("Ens. of 5 (with Chronos-2)", "Ans. de 5 (cu Chronos-2)"),
       "ens_lc": ("LEAR+Chronos-2", "LEAR+Chronos-2")}
COL = {"naive": "#9a9a9a", "aw_arx": PAL["HU"], "aw_lear": PAL["RO"], "ens4": PAL["c5"], "gbm2": "#c9a14a", "mlp2": "#a99be0",
       "xgb": PAL["BG"], "dnn": PAL["c7"], "bolt": "#6b6b6b", "chr2": PAL["c8"], "ens_ld": PAL["c6"], "ens_lx": PAL["c6"],
       "ens_ldx": PAL["DE_LU"], "ens_t4": PAL["DE_LU"], "ens_t5": PAL["DE_LU"], "ens_lc": "#7a1f1f"}
SRC = {"en": {"ec": "energy-charts.info (Fraunhofer ISE): OPCOM prices",
              "ecf": "energy-charts.info (Fraunhofer ISE); Yahoo Finance (EUA)"},
       "ro": {"ec": "energy-charts.info (Fraunhofer ISE): prețuri OPCOM",
              "ecf": "energy-charts.info (Fraunhofer ISE); Yahoo Finance (EUA)"}}
FNAME = {"en": {"P(d-1,h)": "price d-1, same hour", "P(d-2,h)": "price d-2, same hour", "P(d-3,h)": "price d-3, same hour",
                "P(d-7,h)": "price d-7, same hour", "P(d-1,23)": "price d-1, 23:00", "min P(d-1)": "min. price d-1",
                "max P(d-1)": "max. price d-1", "mean P(d-1)": "mean price d-1", "L(d-2,h)": "load d-2, same hour",
                "L(d-7,h)": "load d-7, same hour", "RES(d-2,h)": "wind+solar d-2, same hour", "RES(d-7,h)": "wind+solar d-7, same hour",
                "mean L(d-2)": "mean load d-2", "mean RES(d-2)": "mean wind+solar d-2", "hydro(d-2)": "hydro d-2",
                "nuclear(d-2)": "nuclear d-2", "net imports(d-2)": "net imports d-2", "EUA(d-2)": "carbon price d-2",
                "hour": "hour of day", "day of week": "day of week"},
         "ro": {"P(d-1,h)": "preț d-1, aceeași oră", "P(d-2,h)": "preț d-2, aceeași oră", "P(d-3,h)": "preț d-3, aceeași oră",
                "P(d-7,h)": "preț d-7, aceeași oră", "P(d-1,23)": "preț d-1, ora 23", "min P(d-1)": "preț minim d-1",
                "max P(d-1)": "preț maxim d-1", "mean P(d-1)": "preț mediu d-1", "L(d-2,h)": "consum d-2, aceeași oră",
                "L(d-7,h)": "consum d-7, aceeași oră", "RES(d-2,h)": "eolian+solar d-2, aceeași oră",
                "RES(d-7,h)": "eolian+solar d-7, aceeași oră", "mean L(d-2)": "consum mediu d-2",
                "mean RES(d-2)": "eolian+solar mediu d-2", "hydro(d-2)": "hidro d-2", "nuclear(d-2)": "nuclear d-2",
                "net imports(d-2)": "import net d-2", "EUA(d-2)": "preț CO$_2$ d-2", "hour": "ora din zi", "day of week": "ziua săptămînii"}}
BNAME = {"en": {"price d-1": "prices d-1", "price d-2": "prices d-2", "price d-3": "prices d-3", "price d-7": "prices d-7",
                "load": "load d-2, d-3, d-7", "wind+solar": "wind+solar d-2, d-3, d-7", "fund": "hydro, nuclear, imports, carbon",
                "day of week": "day of week"},
         "ro": {"price d-1": "prețuri d-1", "price d-2": "prețuri d-2", "price d-3": "prețuri d-3", "price d-7": "prețuri d-7",
                "load": "consum d-2, d-3, d-7", "wind+solar": "eolian+solar d-2, d-3, d-7", "fund": "hidro, nuclear, import, CO$_2$",
                "day of week": "ziua săptămînii"}}
GCOL = {"price": PAL["RO"], "load": "#222222", "res": PAL["BG"], "fund": PAL["HU"], "cal": "#9a9a9a"}


def legend_bottom(fig, handles=None, labels=None, ncol=4):
    """Course legend (bottom, outside the axes, no frame) with compact spacing so that it fits the 6.4-inch width;
    out() moves it just below the lowest axis label."""
    if handles is None:
        handles, labels = [], []
        for ax in fig.axes:
            for hh, ll in zip(*ax.get_legend_handles_labels()):
                if ll not in labels:
                    handles.append(hh)
                    labels.append(ll)
    if handles:
        fig.legend(handles, labels, loc="upper center", ncol=ncol, frameon=False, handlelength=1.6, handletextpad=0.5,
                   columnspacing=1.0, borderaxespad=0.1)


def chart(name, src_key, period_en, period_ro):
    N["charts"][name] = {"source_en": SRC["en"][src_key], "source_ro": SRC["ro"][src_key], "period_en": period_en, "period_ro": period_ro}


def comma_axes(fig, lang, also_x=()):
    if lang != "ro":
        return
    f_ = FuncFormatter(lambda v, p: f"{v:g}".replace(".", ",").replace("-", "−"))
    for ax in fig.axes:
        if ax.get_yscale() == "linear" and not getattr(ax, "_keep_y", False):
            ax.yaxis.set_major_formatter(f_)
    for ax in also_x:
        ax.xaxis.set_major_formatter(f_)


def out(fig, lang, name, bottom=None, also_x=()):
    """Save one chart: the axes use the whole figure height and the legend (if any) is placed just below the lowest
    axis label, outside the axes, so that no height is lost between the plot and its legend."""
    comma_axes(fig, lang, also_x)
    os.makedirs(os.path.join(HERE, "charts", lang), exist_ok=True)
    fig.tight_layout(pad=0.3)
    if fig.legends:
        fig.canvas.draw()
        r = fig.canvas.get_renderer()
        y0 = min(ax.get_tightbbox(r).y0 for ax in fig.axes) / fig.bbox.height
        lg = fig.legends[0]
        lg.set_loc("upper center")
        lg.set_bbox_to_anchor((0.5, y0 - 0.01), transform=fig.transFigure)
    fig.savefig(os.path.join(HERE, "charts", lang, name + ".pdf"), transparent=True, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def mfmt(ax, lang, step=1):
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=step))
    mon = MON_RO if lang == "ro" else MON_EN
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: mon[mdates.num2date(v).month - 1] +
                                               (f"\n{mdates.num2date(v).year}" if mdates.num2date(v).month == 1 else "")))


DAYN = {"en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "ro": ["lun.", "mar.", "mie.", "joi", "vin.", "sîm.", "dum."]}
DAILY = pd.Series(PM.mean(1).values, index=CAL)
xm = [pd.Timestamp(str(mm)) for mm in MONTHS_T]
h24 = np.arange(24)
for lang in ["en", "ro"]:
    T = (lambda en, ro: en) if lang == "en" else (lambda en, ro: ro)
    L = lambda k: LAB[k][0 if lang == "en" else 1]  # noqa: E731
    # 1 three chronological samples
    fig, ax = plt.subplots(figsize=(6.4, 1.45))
    ax.axvspan(CAL[FIRST], VAL0 - pd.Timedelta(days=1), color=PAL["HU"], alpha=0.12, lw=0,
               label=T("training (grows each month)", "antrenare (crește în fiecare lună)"))
    ax.axvspan(VAL0, TEST0 - pd.Timedelta(days=1), color=PAL["BG"], alpha=0.28, lw=0,
               label=T("validation year: choose hyperparameters", "anul de validare: alegerea hiperparametrilor"))
    ax.axvspan(TEST0, END, color=PAL["DE_LU"], alpha=0.2, lw=0, label=T("test year (as in Lecture 2)", "anul de test (ca în cursul 2)"))
    ax.plot(DAILY.index, DAILY.values, color=PAL["RO"], lw=0.8, label=T("Romania, daily base price", "România, prețul zilnic de bază"))
    ax.set_ylabel("EUR/MWh")
    ax.set_xlim(CAL[0], END)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, ncol=2)
    out(fig, lang, "split_ml", bottom=0.26)
    # 2 random search on the validation year
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.75), sharey=True)
    for ax, V, best_, nm in [(axs[0], VAL_DNN, BEST_DNN, "DNN"), (axs[1], VAL_XGB, BEST_XGB, "XGBoost")]:
        o = np.argsort(V)
        ax.plot(range(1, len(V) + 1), V[o], "o", color="#9a9a9a", ms=4, label=T("one configuration", "o configurație"))
        ax.plot([1], [V[best_]], "o", color=PAL["DE_LU"], ms=7, label=T("chosen (lowest validation MAE)", "aleasă (MAE minimă la validare)"))
        r0 = int(np.where(o == 0)[0][0]) + 1
        ax.plot([r0], [V[0]], "s", color=PAL["RO"], ms=6, label=T("setting of Lecture 2", "setarea din cursul 2"))
        ax.axhline(naive_val, color="#222222", ls=":", lw=1.0, label=T("naive, validation year", "modelul naiv, anul de validare"))
        ax.set_title(nm, fontsize=10)
        ax.set_xlabel(T("rank on the validation year", "locul în clasamentul de validare"), fontsize=9.5)
    axs[0].set_ylabel(T("MAE, validation\nyear (EUR/MWh)", "MAE la validare\n(EUR/MWh)"), fontsize=9.5)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "search", bottom=0.27)
    # 3 learning curve (chosen DNN, last refit, seed 1)
    fig, ax = plt.subplots(figsize=(6.4, 1.45))
    ee = np.arange(1, len(_curve[0]) + 1)
    ax.plot(ee, _curve[0], color=PAL["RO"], label=T("training days (first 85%)", "antrenare (primele 85%)"))
    ax.plot(ee, _curve[1], color=PAL["DE_LU"], label=T("early-stopping block (last 15%)", "oprire timpurie (ultimele 15%)"))
    ax.axvline(N["curve"]["best_ep"], color="#222222", ls="--", lw=0.9, label=T("epoch kept", "epoca păstrată"))
    ax.set_xlabel(T("epoch (one pass over the training days)", "epoca (o parcurgere a zilelor de antrenare)"))
    ax.set_ylabel("MAE\n(EUR/MWh)", fontsize=10)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "learning_curve", bottom=0.22)
    # 4 monthly MAE
    fig, ax = plt.subplots(figsize=(6.4, 1.45))
    for k, ls, mk in [("aw_lear", "-", "o"), ("xgb", "--", "s"), ("dnn", "-.", "^"), ("ens_ldx", "-", "D")]:
        ax.plot(xm, BYMONTH[k], color=COL[k], ls=ls, marker=mk, ms=3.5, lw=1.6 if k == "ens_ldx" else 1.1, label=L(k))
    ax.set_ylabel("MAE\n(EUR/MWh)", fontsize=10)
    mfmt(ax, lang, 1)
    legend_bottom(fig, ncol=4)
    out(fig, lang, "monthly_ml", bottom=0.22)
    # 5 DM chessboard
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("dm", ["#0b6e2e", "#7fc97f", "#ffe08a", "#f4a259", "#d7301f", "#5a0000"])
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    Z = np.where(np.isnan(DMP), np.nan, np.minimum(DMP, 0.10))
    im = ax.imshow(np.ma.masked_invalid(Z), cmap=cmap, vmin=0, vmax=0.10, aspect="auto")
    ax.set_xticks(range(len(DM_MODELS)))      # columns numbered as the rows, so that the labels need no rotation
    ax.set_xticklabels([str(i + 1) for i in range(len(DM_MODELS))], fontsize=9.5)
    ax.set_yticks(range(len(DM_MODELS)))
    ax.set_yticklabels([f"{L(k)} ({i + 1})" for i, k in enumerate(DM_MODELS)], fontsize=9)
    ax.set_xlabel(T("column model (numbered as the rows): is it more accurate than the row model?",
                    "modelul din coloană (numerotat ca rîndurile): este mai precis decît cel din rînd?"), fontsize=9.5)
    for a_ in range(len(DM_MODELS)):
        ax.add_patch(plt.Rectangle((a_ - 0.5, a_ - 0.5), 1, 1, color="#ffffff"))
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label(T("p-value,\ncapped at 0.10", "valoarea p,\nplafonată la 0,10"), fontsize=9.5)
    cb.set_ticks([0, 0.05, 0.10])
    cb.ax._keep_y = True
    cb.ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:.2f}".replace(".", "," if lang == "ro" else ".")))
    ax.spines[:].set_visible(False)
    ax._keep_y = True
    out(fig, lang, "dm_matrix", bottom=0.0)
    # 6 combination weight (illustration)
    fig, ax = plt.subplots(figsize=(6.4, 1.45))
    for k, ls in [("xgb", "-"), ("dnn", "--")]:
        ax.plot(WGRID, WCURVE[k], color=COL[k], ls=ls, label=T(f"AW-LEAR and {L(k)}", f"AW-LEAR și {L(k)}"))
    ax.plot([0.5, 0.5], [WCURVE["xgb"][10], WCURVE["dnn"][10]], "o", color="#222222", ms=4, label=T("equal weights (used)", "ponderi egale (folosite)"))
    ax.set_xlabel(T("weight w of the machine-learning model", "ponderea w a modelului de învățare automată"))
    ax.set_ylabel("MAE\n(EUR/MWh)", fontsize=10)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "combo_weight", bottom=0.22, also_x=[ax])
    # 7 compute cost versus accuracy
    fig, ax = plt.subplots(figsize=(6.4, 1.6))
    for k in ["aw_lear", "xgb", "dnn", "bolt", "chr2", "ens_ldx", "ens_lc"]:
        ax.plot(max(sec[k], 1) / 60, N["acc"][k]["mae"], "o", color=COL[k], ms=6)
        off = {"aw_lear": (7, 0), "ens_ldx": (7, 0), "ens_lc": (7, 0), "xgb": (7, 0), "dnn": (7, 0), "bolt": (7, 0), "chr2": (7, 0)}[k]
        ax.annotate(L(k), (max(sec[k], 1) / 60, N["acc"][k]["mae"]), textcoords="offset points", xytext=off, fontsize=9.5, va="center")
    ax.set_xscale("log")
    ax.set_xlabel(T("compute time for the test year, minutes on one core (log scale)", "timpul de calcul pentru anul de test, minute pe un nucleu (scară log.)"), fontsize=9.5)
    ax.set_ylabel("MAE\n(EUR/MWh)", fontsize=10)
    xl, yl = ax.get_xlim(), ax.get_ylim()
    ax.set_xlim(xl[0], xl[1] * 12)
    ax.set_ylim(yl[0] - 0.25, yl[1] + 0.15)
    out(fig, lang, "cost_gain", bottom=0.02)
    # 8 SHAP global
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    o = np.argsort(-share)[:10][::-1]
    gof = {j: g for g, ix in GROUPS.items() for j in ix}
    ax.barh(range(len(o)), share[o], color=[GCOL[gof[j]] for j in o], height=0.7)
    ax.set_yticks(range(len(o)))
    ax.set_yticklabels([FNAME[lang][XGB_NAMES[j]] for j in o], fontsize=9)
    ax.set_xlabel(T("share of the mean |SHAP value|, %", "ponderea în media valorilor |SHAP|, %"), fontsize=9.5)
    from matplotlib.patches import Patch
    hnd = [Patch(color=GCOL[g], label=lb) for g, lb in [("price", T("prices", "prețuri")), ("load", T("load", "consum")),
                                                        ("res", T("wind+solar", "eolian+solar")), ("fund", T("other fundamentals", "alte variabile fundamentale")),
                                                        ("cal", T("calendar", "calendar"))]]
    legend_bottom(fig, handles=hnd, labels=[h_.get_label() for h_ in hnd], ncol=5 if lang == "en" else 3)
    ax._keep_y = True
    out(fig, lang, "shap_global", bottom=0.12, also_x=[ax])
    # 9 SHAP dependence of wind+solar d-2
    fig, ax = plt.subplots(figsize=(6.4, 1.5))
    xr, sr = XS[:, :, res_j], SH[:, :, res_j]
    day_h = np.zeros_like(xr, bool)
    day_h[:, 9:17] = True
    for msk, c, lb in [(~day_h, "#5b6fa8", T("hours 17-08", "orele 17-08")), (day_h, PAL["BG"], T("hours 09-16 (sun)", "orele 09-16 (soare)"))]:
        ax.scatter(xr[msk] / 1000, sr[msk], s=1.2, alpha=0.35, color=c, lw=0, label=lb, rasterized=True)
    ax.axhline(0, color="#222222", lw=0.6)
    ax.set_xlabel(T("wind+solar on d-2, same hour (GW)", "producția eoliană și solară din d-2, aceeași oră (GW)"))
    ax.set_ylabel(T("SHAP value\n(asinh scale)", "valoarea SHAP\n(scara asinh)"), fontsize=9.5)
    lg = legend_bottom(fig, ncol=2)
    for lh in fig.legends[0].legend_handles:
        lh.set_sizes([20])
        lh.set_alpha(1)
    out(fig, lang, "shap_res", bottom=0.22, also_x=[ax])
    # 10 DNN permutation importance
    fig, ax = plt.subplots(figsize=(6.4, 1.7))
    bl = sorted(PI, key=PI.get)
    ax.barh(range(len(bl)), [PI[b] for b in bl], color=[PAL["RO"] if b.startswith("price") else (PAL["BG"] if b == "wind+solar" else ("#222222" if b == "load" else (PAL["HU"] if b == "fund" else "#9a9a9a"))) for b in bl], height=0.65)
    ax.set_yticks(range(len(bl)))
    ax.set_yticklabels([BNAME[lang][b] for b in bl], fontsize=9.5)
    ax.set_xlabel(T("increase in MAE when the block is shuffled, EUR/MWh", "creșterea MAE la permutarea blocului, EUR/MWh"), fontsize=9.5)
    ax._keep_y = True
    out(fig, lang, "perm_dnn", bottom=0.02, also_x=[ax])
    # 11 events by hour
    fig, ax = plt.subplots(figsize=(6.4, 1.45))
    ax.bar(h24 - 0.2, Y_SP.mean(0) * 100, width=0.4, color=PAL["c8"], label=T("spike: price above the 90th percentile of the last 12 months", "vîrf: preț peste percentila 90 a ultimelor 12 luni"))
    ax.bar(h24 + 0.2, Y_NG.mean(0) * 100, width=0.4, color=PAL["HU"], label=T("price $\\leq$ 0", "preț $\\leq$ 0"))
    ax.set_xticks(range(0, 24, 2))
    ax.set_xlabel(T("hour h (CET)", "ora h (CET)"))
    ax.set_ylabel(T("% of\ntest days", "% din zilele\nde test"), fontsize=10)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "events_hour", bottom=0.26)
    # 12 ROC curves
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.85), sharey=True)
    for ax, Y_, CC, ttl in [(axs[0], Y_SP, CS, T("spikes", "vîrfuri")), (axs[1], Y_NG, CN, T("prices $\\leq$ 0", "prețuri $\\leq$ 0"))]:
        for k, c, ls, lb in [("xgb", PAL["BG"], "-", "XGBoost"), ("logit", PAL["c7"], "--", T("logistic regression", "regresie logistică")),
                             ("persist", "#9a9a9a", ":", T("persistence (last 7 days)", "persistență (ultimele 7 zile)")),
                             ("lear", PAL["RO"], "-.", T("AW-LEAR point forecast", "prognoza punctuală AW-LEAR"))]:
            fpr, tpr, _ = roc_curve(Y_.ravel(), CC[k].ravel())
            ax.plot(fpr, tpr, color=c, ls=ls, lw=1.3, label=lb)
        ax.plot([0, 1], [0, 1], color="#222222", lw=0.5)
        ax.set_title(ttl, fontsize=10)
        ax.set_xlabel(T("false alarm rate", "rata alarmelor false"), fontsize=9.5)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}".replace(".", "," if lang == "ro" else ".")))
        ax.set_yticks([0, 0.5, 1])
    axs[0].set_ylabel(T("share of events\ncaught", "evenimente\nsemnalate"), fontsize=9.5)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "roc", bottom=0.26)
    # 13 value of acting by threshold
    fig, ax = plt.subplots(figsize=(6.4, 1.45))
    ax.plot(CUTS, VCURVE, color=PAL["BG"], label=T("act if XGBoost probability > threshold", "reacție dacă probabilitatea XGBoost > prag"))
    ax.axvline(C_ACT / LBAR, color=PAL["DE_LU"], ls="--", lw=1.0, label=T("threshold C/L", "pragul C/L"))
    ax.axvline(0.5, color="#9a9a9a", ls=":", lw=1.0, label=T("threshold 0.5", "pragul 0,5"))
    ax.set_xlim(0.1, 1.0)
    ax.set_ylim(min(0, VCURVE[CUTS >= 0.1].min()) - 3, VCURVE.max() * 1.25)
    ax.axhline(0, color="#222222", lw=0.5)
    ax.set_xlabel(T("action threshold (probability of a spike)", "pragul de reacție (probabilitatea unui vîrf)"))
    ax.set_ylabel(T("value\n(10$^3$ EUR/MW)", "valoare\n(10$^3$ EUR/MW)"), fontsize=10)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "decision", bottom=0.22, also_x=[ax])
    # 14 data snooping
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.65))
    for ax, V, Tt, best_, nm in [(axs[0], VAL_DNN, TEST_DNN, BEST_DNN, "DNN"), (axs[1], VAL_XGB, TEST_XGB, BEST_XGB, "XGBoost")]:
        ax.plot(V, Tt, "o", color="#9a9a9a", ms=4, label=T("one configuration", "o configurație"))
        ax.plot(V[best_], Tt[best_], "o", color=PAL["DE_LU"], ms=7, label=T("chosen on validation (honest)", "aleasă la validare (corect)"))
        jb = int(np.argmin(Tt))
        ax.plot(V[jb], Tt[jb], "*", color=PAL["c8"], ms=11, zorder=5, label=T("best on the test year (snooping)", "cea mai bună pe anul de test (selecție abuzivă)"))
        ax.axhline(LEAR_MAE, color=PAL["RO"], ls="--", lw=1.0, label=T("AW-LEAR, test year", "AW-LEAR, anul de test"))
        ax.set_ylim(min(LEAR_MAE, Tt.min()) - 0.4, Tt.max() + 0.3)
        ax.set_title(nm, fontsize=10)
        ax.set_xlabel(T("MAE, validation year", "MAE, anul de validare"), fontsize=9.5)
    axs[0].set_ylabel(T("MAE, test year", "MAE, anul de test"), fontsize=9.5)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "snooping", bottom=0.27, also_x=list(axs))
    # 15 look-ahead pitfalls
    fig, ax = plt.subplots(figsize=(6.4, 1.25))
    kk = [("honest", T("honest, monthly refits", "corect, reestimare lunară"), PAL["BG"]),
          ("shuffled", T("shuffled 5-fold validation", "5 subeșantioane amestecate"), PAL["c8"]),
          ("leak", T("+ load, RES of day d", "+ consum, RES din ziua d"), PAL["c8"])]
    ax.barh(range(3), [N["pit"][k] for k, _, _ in kk], color=[c for _, _, c in kk], height=0.6)
    ax.set_yticks(range(3))
    ax.set_yticklabels([lb for _, lb, _ in kk], fontsize=9.5)
    ax.invert_yaxis()
    ax.axvline(LEAR_MAE, color=PAL["RO"], ls="--", lw=0.9, label=T("AW-LEAR, honest", "AW-LEAR, evaluare corectă"))
    ax.set_xlim(20, max(N["pit"][k] for k, _, _ in kk) + 0.8)
    ax.set_xlabel(T("MAE on the test year, EUR/MWh (axis does not start at 0)", "MAE în anul de test, EUR/MWh (axa nu începe de la 0)"), fontsize=9.5)
    ax._keep_y = True
    legend_bottom(fig, ncol=1)
    out(fig, lang, "pit_leak", bottom=0.2, also_x=[ax])
    # 15b retraining frequency and window
    fig, ax = plt.subplots(figsize=(6.4, 1.5))
    kk2 = [("honest", T("monthly, all past days", "lunar, toate zilele anterioare")), ("quarterly", T("quarterly, all past days", "trimestrial, toate zilele anterioare")),
           ("once", T("once, before the test year", "o singură dată, înainte de anul de test")),
           ("roll730", T("monthly, last 730 days", "lunar, ultimele 730 de zile")), ("roll365", T("monthly, last 365 days", "lunar, ultimele 365 de zile"))]
    ax.barh(range(len(kk2)), [N["pit"][k] for k, _ in kk2], color=[PAL["BG"]] + [PAL["c7"]] * 4, height=0.6)
    ax.set_yticks(range(len(kk2)))
    ax.set_yticklabels([lb for _, lb in kk2], fontsize=9.5)
    ax.invert_yaxis()
    ax.axvline(LEAR_MAE, color=PAL["RO"], ls="--", lw=0.9, label="AW-LEAR")
    lo_, hi_ = min(N["pit"][k] for k, _ in kk2), max(N["pit"][k] for k, _ in kk2)
    ax.set_xlim(min(lo_, LEAR_MAE) - 1.5, hi_ + 0.8)
    ax.set_xlabel(T("MAE on the test year, EUR/MWh (axis does not start at 0)", "MAE în anul de test, EUR/MWh (axa nu începe de la 0)"), fontsize=9.5)
    ax._keep_y = True
    legend_bottom(fig, ncol=1)
    out(fig, lang, "pit_retrain", bottom=0.2, also_x=[ax])
    # 16 case-study week
    cw = slice(CWS.start, CWS.stop)
    nd = cw.stop - cw.start
    xs_ = pd.date_range(TDAYS[cw.start], periods=24 * nd, freq="h")
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.05), sharex=True, gridspec_kw={"height_ratios": [1.6, 1]})
    axs[0].plot(xs_, A[cw].ravel(), color="#222222", lw=1.4, label=T("actual price", "prețul realizat"))
    for k, ls in [("aw_lear", "-"), ("xgb", "--"), ("chr2", "-.")]:
        axs[0].plot(xs_, M[k][cw].ravel(), color=COL[k], ls=ls, lw=1.0, label=L(k))
    axs[0].plot(xs_, np.repeat(TH_T[cw], 24), color="#6b6b6b", lw=0.9, ls=":", label=T("spike threshold", "pragul de vîrf"))
    axs[0].set_ylabel("EUR/MWh")
    axs[1].fill_between(xs_, 0, Y_SP[cw].ravel(), step="mid", color=PAL["c8"], alpha=0.18, lw=0, label=T("actual spike hour", "oră cu vîrf"))
    axs[1].plot(xs_, CS["xgb"][cw].ravel(), color=PAL["BG"], lw=1.1, label=T("spike probability", "probabilitatea vîrfului"))
    axs[1].axhline(C_ACT / LBAR, color=PAL["DE_LU"], ls="--", lw=0.8, label="C/L")
    axs[1].set_ylim(0, 1)
    axs[1].set_ylabel(T("XGBoost\nprobability", "probabilitate\nXGBoost"), fontsize=9.5)
    axs[1].xaxis.set_major_locator(mdates.DayLocator())
    axs[1].xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{DAYN[lang][mdates.num2date(v).weekday()]} {mdates.num2date(v).day}"))
    legend_bottom(fig, ncol=4)
    out(fig, lang, "case_week", bottom=0.16)
    # 17 local explanation at the peak hour (EUR/MWh)
    fig, ax = plt.subplots(figsize=(6.4, 1.95))
    top = list(ordr[:7])
    rest = phi_eur.sum() - phi_eur[top].sum()
    vals = [phi_eur[j] for j in top] + [rest]
    def _v(x):
        t_ = f"{x:,.0f}".replace(",", "\u2009")
        return t_
    def _lv(j):
        if XGB_NAMES[j] == "day of week":
            return DAYN[lang][int(XS[kd, kh, j])]
        return _v(XS[kd, kh, j])
    labs = [f"{FNAME[lang][XGB_NAMES[j]]}: {_lv(j)}" for j in top] + [T("other 13 features", "celelalte 13 variabile")]
    cum = P0
    for i_, v in enumerate(vals):
        ax.barh(i_, v, left=cum, color=PAL["c8"] if v > 0 else PAL["HU"], height=0.6)
        cum += v
    ax.axvline(P0, color="#9a9a9a", ls=":", lw=1.0, label=T(f"model average ({P0:.0f})", f"media modelului ({P0:.0f})"))
    ax.axvline(PH, color=PAL["BG"], ls="--", lw=1.0, label=T(f"XGBoost forecast ({PH:.0f})", f"prognoza XGBoost ({PH:.0f})"))
    ax.axvline(A[kd, kh], color="#222222", lw=1.2, label=T(f"actual price ({A[kd, kh]:.0f})", f"prețul realizat ({A[kd, kh]:.0f})"))
    ax.set_xlim(0, max(A[kd, kh], PH) * 1.04)
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(labs, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("EUR/MWh")
    legend_bottom(fig, ncol=3)
    ax._keep_y = True
    out(fig, lang, "shap_local", bottom=0.17, also_x=[ax])
    # 18 foundation models by hour
    fig, ax = plt.subplots(figsize=(6.4, 1.45))
    for k, ls, mk in [("naive", ":", "o"), ("bolt", "--", "s"), ("chr2", "-", "^"), ("aw_lear", "-", "o")]:
        ax.plot(h24, BYHOUR[k], color=COL[k], ls=ls, marker=mk, ms=3, label=L(k))
    ax.set_xticks(range(0, 24, 2))
    ax.set_xlabel(T("hour h (CET)", "ora h (CET)"))
    ax.set_ylabel("MAE\n(EUR/MWh)", fontsize=10)
    legend_bottom(fig, ncol=4)
    out(fig, lang, "foundation_hour", bottom=0.22)

ped, prd = f"test year {d(TEST0)} to {d(END)}", f"anul de test {d(TEST0)} - {d(END)}"
chart("split_ml", "ec", f"daily base price, {d(START)} to {d(END)}", f"preț zilnic de bază, {d(START)} - {d(END)}")
chart("search", "ecf", f"validation year {d(VAL0)} to {d(VDAYS[-1])}, quarterly refits",
      f"anul de validare {d(VAL0)} - {d(VDAYS[-1])}, reestimare trimestrială")
chart("learning_curve", "ecf", f"chosen DNN, refit for {MONTHS_T[-1]}, seed 1", f"rețeaua DNN aleasă, reestimarea pentru {MONTHS_T[-1]}, inițializarea 1")
chart("monthly_ml", "ecf", ped, prd)
chart("dm_matrix", "ecf", f"{ped}, {len(TDAYS)} days; one-sided p-values", f"{prd}, {len(TDAYS)} de zile; valori p unilaterale")
chart("combo_weight", "ecf", f"{ped}; illustration, the weight is not chosen on the test year", f"{prd}; ilustrare, ponderea nu se alege pe anul de test")
chart("cost_gain", "ecf", f"{ped}; one processor core", f"{prd}; un nucleu de procesor")
chart("shap_global", "ecf", f"{ped}, {A.size} hours", f"{prd}, {A.size} de ore")
chart("shap_res", "ecf", f"{ped}, {A.size} hours", f"{prd}, {A.size} de ore")
chart("perm_dnn", "ecf", ped, prd)
chart("events_hour", "ec", ped, prd)
chart("roc", "ecf", f"{ped}, {A.size} hours", f"{prd}, {A.size} de ore")
chart("decision", "ecf", f"{ped}; 1 MW of flexible load", f"{prd}; 1 MW de consum flexibil")
chart("snooping", "ecf", f"validation and {ped}", f"anul de validare și {prd}")
chart("pit_leak", "ecf", ped, prd)
chart("pit_retrain", "ecf", ped, prd)
chart("case_week", "ecf", f"{N['case']['week_start']} to {N['case']['week_end']}, hourly", f"{N['case']['week_start']} - {N['case']['week_end']}, date orare")
chart("shap_local", "ecf", f"{N['case']['day']}, hour {N['case']['hour']}:00 CET; contributions rescaled to EUR/MWh (Appendix C)",
      f"{N['case']['day']}, ora {N['case']['hour']}:00 CET; contribuții exprimate în EUR/MWh (anexa C)")
chart("foundation_hour", "ec", f"{ped}; zero-shot, context = last {CTX} hourly prices", f"{prd}; fără reantrenare, context = ultimele {CTX} de prețuri orare")

with open(os.path.join(HERE, "L7_numbers.json"), "w") as fh:
    json.dump(N, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("wrote L7_numbers.json and", len(N["charts"]), "charts x 2 languages")
