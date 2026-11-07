"""
analysis_L2.py -- Lecture 2 "Forecasting electricity prices" (EMQA)
===================================================================
Reads the real series in repo/data/clean (see data/SOURCES.md), runs every forecast shown on the slides and writes
    lectures/L2/L2_numbers.json        all results (the deck builder reads ONLY this file)
    lectures/L2/charts/en/*.pdf        figures with English labels
    lectures/L2/charts/ro/*.pdf        the same figures with Romanian labels
    lectures/L2/cache/forecasts.pkl    the point and quantile forecasts (recomputed when the data or the engine change)
Run:  python3 lectures/L2/analysis_L2.py            (add --fresh to ignore the cache)

Design (strict time-series discipline)
  * Target: Romanian day-ahead price (OPCOM PZU), hourly, CET/CEST delivery day; after 1 Oct 2025 the hour is the mean of
    its four quarter-hours (as in Assignment 1). Panel 2022-01-01 to the cut-off (last complete month), no missing day.
  * DST: the epftoolbox / Assignment 1 convention keeps 24 columns: the missing spring hour h02 = mean(h01, h03), the
    doubled autumn hour is averaged. The two DST days of the test year are kept; the MAE without them is also reported.
  * Test = the last 365 days to the cut-off; burn-in = the 182 days before it (their forecasts feed QRA and conformal
    intervals only). Chronological order everywhere: no shuffling, no K-fold, no random validation split.
  * Gate-closure information set for day d (forecast made at 12:00 CET on d-1):
      prices up to d-1;  realised load, wind+solar, hydro, nuclear, cross-border flows up to d-2 (lags >= 2 days);
      carbon (EUA, SparkChange ETC proxy) at the d-2 close.  No day-ahead load/RES forecasts are used (none in the data).
  * Every transformation (asinh median/MAD, z-scores, LASSO lambda by AIC) is computed inside the calibration window,
    from rows available at gate closure. ML models are refitted monthly on an expanding window ending before the month.
  * Leakage self-check (section 8): (a) a timestamp audit of every feature against the 12:00 CET cut-off;
    (b) a perturbation test: forecasts recomputed with all prices from d and all fundamentals from d-1 set to NaN must be
    identical to the stored forecasts.
  * Seeds fixed (numpy, scikit-learn). There is no simulated series in this lecture.
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
import statsmodels.api as sm
from joblib import Parallel, delayed
from scipy import stats
from statsmodels.regression.quantile_regression import QuantReg
from statsmodels.tsa.stattools import adfuller, coint, kpss
from statsmodels.tsa.vector_ar.vecm import coint_johansen

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import emqa_plot as ep  # noqa: E402
from emqa_plot import PAL, legend_bottom, save  # noqa: E402

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

warnings.filterwarnings("ignore")
ep.style()
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "data", "clean")
TZ = "Europe/Brussels"
ENGINE_VERSION = "L2-engine-v4"
FRESH = "--fresh" in sys.argv
N = {"charts": {}}
SEED = 20261105
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
# 0. Load data and cut-off (same rule as Lecture 1)
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
PM, DST = day_matrix(HP["RO"].dropna())
LM, _ = day_matrix(GH["load"].dropna())
RM, _ = day_matrix((GH["wind_onshore"] + GH["solar"]).dropna())
CAL = pd.date_range(START, END, freq="D")
PM, LM, RM, DST = PM.reindex(CAL), LM.reindex(CAL), RM.reindex(CAL), DST.reindex(CAL)
assert not PM.isna().any().any() and not LM.isna().any().any() and not RM.isna().any().any(), "panel has gaps"
N["data"] = {"start": d(START), "end": d(END), "n_days": len(CAL)}

# daily fundamentals (CET day means), value usable for day d = last observation on or before d-2 (past only)
EUA = pd.read_csv(os.path.join(DATA, "eua_daily.csv"), parse_dates=["date"]).set_index("date")["eua_etc_co2l_eur_per_unit"]
CAL_EX = pd.date_range(START - pd.Timedelta(days=30), END, freq="D")
FUND_RAW = pd.DataFrame({
    "hydro": (G["hydro_run_of_river"] + G["hydro_water_reservoir"]).reindex(CAL_EX),
    "nuclear": G["nuclear"].reindex(CAL_EX),
    "netimp": CB["sum"].reindex(CAL_EX),
    "eua": EUA.reindex(CAL_EX)})
FUND_AVAIL = FUND_RAW.ffill().shift(2).reindex(CAL)          # carried forward from the past only, then lagged 2 days
N["data"]["fund_ffill"] = {k: int(FUND_RAW[k].reindex(CAL).isna().sum()) for k in FUND_RAW}

N_TEST, N_BURN = 365, 182
TEST0 = END - pd.Timedelta(days=N_TEST - 1)
FC0 = TEST0 - pd.Timedelta(days=N_BURN)
FDAYS = pd.date_range(FC0, END, freq="D")
TDAYS = pd.date_range(TEST0, END, freq="D")
N["design"] = {"test_start": d(TEST0), "test_end": d(END), "n_test": N_TEST, "burn_start": d(FC0), "n_burn": N_BURN,
               "dst_test": [d(x) for x in TDAYS[DST.loc[TDAYS].values]], "n_dst_test": int(DST.loc[TDAYS].sum()),
               "cal_first": d(START)}

# =============================================================================
# 1. Feature blocks. Row t of every lagged block holds information for target day t.
#    Price lag k = row t-k (k >= 1); realised lag k = row t-k (k >= 2); fundamentals already lagged 2 days.
# =============================================================================
P_ = PM.values.astype(float)
L_ = LM.values.astype(float)
R_ = RM.values.astype(float)
F_ = FUND_AVAIL.values.astype(float)
DOW = CAL.dayofweek.values
IDX = {t: i for i, t in enumerate(CAL)}
PLAGS, XLAGS = (1, 2, 3, 7), (2, 3, 7)
# registry used by the timestamp audit: (block, lag in days, source)
FEATURE_REGISTRY = ([("P", k, "price") for k in PLAGS] + [("L", k, "realised") for k in XLAGS] +
                    [("R", k, "realised") for k in XLAGS] + [("fund_" + c, 2, "realised" if c != "eua" else "close")
                                                             for c in FUND_RAW.columns])


def shift_rows(A, k):
    out = np.full_like(A, np.nan)
    out[k:] = A[:-k]
    return out


def mad_scale(x):
    x = np.asarray(x, float).ravel()
    m = np.median(x)
    s = stats.median_abs_deviation(x, scale="normal")
    return m, (s if s > 0 else 1.0)


def arx_day(Pa, La, Ra, Fa, i, T, kind="asinh"):
    """Expert ARX (Assignment 1, Ziel & Weron 2018 style), one regression per hour; target day = row i.
    Calibration targets rows i-T..i-1; VST median/MAD from price rows i-T-7..i-1; L,R z-scores from rows i-T-7..i-2."""
    P1, P2, P7 = shift_rows(Pa, 1), shift_rows(Pa, 2), shift_rows(Pa, 7)
    lo = i - T
    if kind == "raw":
        m, s = 0.0, 1.0
        f = lambda x: x  # noqa: E731
        finv = f
    else:
        m, s = mad_scale(Pa[lo - 7:i])
        f = lambda x: np.arcsinh((x - m) / s)  # noqa: E731
        finv = lambda y: m + s * np.sinh(y)  # noqa: E731
    rows = slice(lo, i + 1)
    Y, Y1, Y2, Y7 = f(Pa[rows]), f(P1[rows]), f(P2[rows]), f(P7[rows])
    mu_l, sd_l = np.mean(La[lo - 7:i - 1]), np.std(La[lo - 7:i - 1])
    mu_r, sd_r = np.mean(Ra[lo - 7:i - 1]), np.std(Ra[lo - 7:i - 1])
    Lz = (shift_rows(La, 2)[rows] - mu_l) / sd_l
    Rz = (shift_rows(Ra, 2)[rows] - mu_r) / sd_r
    dw = DOW[rows]
    dmy = np.column_stack([dw == 0, dw == 5, dw == 6]).astype(float)
    extra = None
    if kind == "fund":
        Fr = Fa[rows]
        extra = (Fr - np.nanmean(Fr[:-1], axis=0)) / np.nanstd(Fr[:-1], axis=0)
    n = T + 1
    out, coefs = np.zeros(24), np.zeros((24, 12))
    if kind == "single":                                          # one pooled regression, common slopes, hour intercepts
        Xs, ys = [], []
        for h in range(24):
            hd = np.zeros((n, 24))
            hd[:, h] = 1
            Xs.append(np.column_stack([hd, Y1[:, h], Y2[:, h], Y7[:, h], Y1[:, 23], Y1.min(1), Y1.max(1), Lz[:, h], Rz[:, h], dmy]))
            ys.append(Y[:, h])
        Xs, ys = np.stack(Xs, 1), np.stack(ys, 1)                 # n x 24 x p
        Xc, yc = Xs[:-1].reshape(-1, Xs.shape[2]), ys[:-1].ravel()
        b = np.linalg.lstsq(Xc, yc, rcond=None)[0]
        return finv(Xs[-1] @ b), None
    for h in range(24):
        cols = [np.ones(n), Y1[:, h], Y2[:, h], Y7[:, h], Y1[:, 23], Y1.min(1), Y1.max(1)]
        if kind != "noexog":
            cols += [Lz[:, h], Rz[:, h]]
        cols += [dmy[:, 0], dmy[:, 1], dmy[:, 2]]
        X = np.column_stack(cols)
        if h == 23:
            X = np.delete(X, 4, axis=1)                           # Y_{d-1,23} appears twice for h = 23
        if extra is not None:
            X = np.column_stack([X, extra])
        b = np.linalg.lstsq(X[:-1], Y[:-1, h], rcond=None)[0]
        out[h] = X[-1] @ b
        if kind == "asinh" and h != 23 and X.shape[1] == 12:
            coefs[h] = b
    return finv(out), coefs


def lear_design(Pa, La, Ra, lo, i):
    """LEAR regressors (Assignment 1: 247 columns) for rows lo..i, with transforms fitted on rows available at gate closure."""
    m, s = mad_scale(Pa[lo - 7:i])
    mL, sL = mad_scale(La[lo - 7:i - 1])
    mR, sR = mad_scale(Ra[lo - 7:i - 1])
    rows = slice(lo, i + 1)
    blocks = [np.arcsinh((shift_rows(Pa, k)[rows] - m) / s) for k in PLAGS]
    blocks += [np.arcsinh((shift_rows(La, k)[rows] - mL) / sL) for k in XLAGS]
    blocks += [np.arcsinh((shift_rows(Ra, k)[rows] - mR) / sR) for k in XLAGS]
    blocks.append(np.eye(7)[DOW[rows]])
    X = np.column_stack(blocks)
    Y = np.arcsinh((Pa[rows] - m) / s)
    return X, Y, m, s


def lear_day(Pa, La, Ra, i, T):
    from sklearn.linear_model import LassoLarsIC
    lo = i - T
    X, Y, m, s = lear_design(Pa, La, Ra, lo, i)
    mu, sd = X[:-1].mean(0), X[:-1].std(0)
    sd[sd == 0] = 1.0
    Xs = (X - mu) / sd
    out, nz = np.zeros(24), np.zeros((24, X.shape[1]), bool)
    for h in range(24):
        mdl = LassoLarsIC(criterion="aic", max_iter=2000).fit(Xs[:-1], Y[:-1, h])
        out[h] = mdl.predict(Xs[-1:])[0]
        nz[h] = mdl.coef_ != 0
    return m + s * np.sinh(out), nz


ARX_W = (56, 84, 112, 714, 721, 728)
LEAR_W = (364, 546, 728)


def point_day(Pa, La, Ra, Fa, i, lear=True):
    """All classical point forecasts for target row i."""
    r = {"naive": Pa[i - 7] if DOW[i] in (0, 5, 6) else Pa[i - 1], "snaive": Pa[i - 7]}
    for T in ARX_W:
        r[f"arx{T}"], c = arx_day(Pa, La, Ra, Fa, i, T)
        if T == 728:
            r["arx_coef"] = c
    r["arx728_raw"] = arx_day(Pa, La, Ra, Fa, i, 728, "raw")[0]
    r["arx728_noexog"] = arx_day(Pa, La, Ra, Fa, i, 728, "noexog")[0]
    r["arx728_fund"] = arx_day(Pa, La, Ra, Fa, i, 728, "fund")[0]
    r["arx728_single"] = arx_day(Pa, La, Ra, Fa, i, 728, "single")[0]
    if lear:
        for T in LEAR_W:
            r[f"lear{T}"], nz = lear_day(Pa, La, Ra, i, T)
            if T == 728:
                r["lear_nz"] = nz
    return r


def run_chunk(Pa, La, Ra, Fa, ii):
    return {i: point_day(Pa, La, Ra, Fa, i) for i in ii}


# ---------------------------------------------------------------- machine learning (monthly refit, expanding window)
def gbm_rows(Pa, La, Ra, Fa, rows):
    """Long-format features for (day, hour) pairs: same-hour lags, daily aggregates, fundamentals, calendar."""
    P1, P2, P3, P7 = (shift_rows(Pa, k) for k in PLAGS)
    L2, L7, R2, R7 = shift_rows(La, 2), shift_rows(La, 7), shift_rows(Ra, 2), shift_rows(Ra, 7)
    feats = []
    for h in range(24):
        f = np.column_stack([P1[rows, h], P2[rows, h], P3[rows, h], P7[rows, h], P1[rows, 23], P1[rows].min(1), P1[rows].max(1),
                             P1[rows].mean(1), L2[rows, h], L7[rows, h], R2[rows, h], R7[rows, h], L2[rows].mean(1),
                             R2[rows].mean(1), Fa[rows], np.full(len(rows), h), DOW[rows]])
        feats.append(f)
    return np.stack(feats, 1)                                  # n_days x 24 x p


GBM_NAMES = ["P(d-1,h)", "P(d-2,h)", "P(d-3,h)", "P(d-7,h)", "P(d-1,23)", "min P(d-1)", "max P(d-1)", "mean P(d-1)",
             "L(d-2,h)", "L(d-7,h)", "RES(d-2,h)", "RES(d-7,h)", "mean L(d-2)", "mean RES(d-2)", "hydro(d-2)", "nuclear(d-2)",
             "net imports(d-2)", "EUA(d-2)", "hour", "day of week"]


def gbm_month(Pa, La, Ra, Fa, i0, i1, seed=SEED):
    """Fit on targets rows 7..i0-1 (all before the month), forecast rows i0..i1 (the month)."""
    from sklearn.ensemble import HistGradientBoostingRegressor
    tr = np.arange(7, i0)
    m, s = mad_scale(Pa[tr])
    Xtr = gbm_rows(Pa, La, Ra, Fa, tr).reshape(-1, len(GBM_NAMES))
    ytr = np.arcsinh((Pa[tr] - m) / s).ravel()
    mdl = HistGradientBoostingRegressor(max_iter=500, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=40,
                                        l2_regularization=1.0, early_stopping=False, random_state=seed,
                                        categorical_features=[18, 19]).fit(Xtr, ytr)
    te = np.arange(i0, i1 + 1)
    pr = mdl.predict(gbm_rows(Pa, La, Ra, Fa, te).reshape(-1, len(GBM_NAMES))).reshape(len(te), 24)
    return m + s * np.sinh(pr), mdl


def mlp_design(Pa, La, Ra, Fa, rows, m, s, mL, sL, mR, sR):
    blocks = [np.arcsinh((shift_rows(Pa, k)[rows] - m) / s) for k in PLAGS]
    blocks += [np.arcsinh((shift_rows(La, k)[rows] - mL) / sL) for k in XLAGS]
    blocks += [np.arcsinh((shift_rows(Ra, k)[rows] - mR) / sR) for k in XLAGS]
    blocks += [Fa[rows], np.eye(7)[DOW[rows]]]
    return np.column_stack(blocks)


def mlp_month(Pa, La, Ra, Fa, i0, i1, seeds=(1, 2, 3, 4), max_ep=150):
    """Multi-output network (24 outputs, Lago et al. 2021 style DNN, small). Epochs chosen on a CHRONOLOGICAL validation
    block (last 15% of the training days); then refitted on all training days with that number of epochs."""
    from sklearn.neural_network import MLPRegressor
    tr = np.arange(7, i0)
    cut = int(len(tr) * 0.85)
    v0 = tr[cut]                                                # first validation day: transforms frozen at its gate closure
    m0, s0 = mad_scale(Pa[7:v0])
    mL0, sL0 = mad_scale(La[7:v0 - 1])
    mR0, sR0 = mad_scale(Ra[7:v0 - 1])
    X0 = mlp_design(Pa, La, Ra, Fa, tr, m0, s0, mL0, sL0, mR0, sR0)
    Y0 = np.arcsinh((Pa[tr] - m0) / s0)
    m, s = mad_scale(Pa[tr])                                    # final refit: everything available before the month
    mL, sL = mad_scale(La[7:i0 - 1])
    mR, sR = mad_scale(Ra[7:i0 - 1])
    X = mlp_design(Pa, La, Ra, Fa, tr, m, s, mL, sL, mR, sR)
    Y = np.arcsinh((Pa[tr] - m) / s)
    te = np.arange(i0, i1 + 1)
    Xte = mlp_design(Pa, La, Ra, Fa, te, m, s, mL, sL, mR, sR)
    preds, epochs = [], []
    for sd in seeds:
        mu, sg = X0[:cut].mean(0), X0[:cut].std(0)
        sg[sg == 0] = 1
        net = MLPRegressor(hidden_layer_sizes=(128, 64), alpha=1e-3, learning_rate_init=1e-3, batch_size=64, random_state=sd)
        best, best_ep = np.inf, 1
        for ep_ in range(1, max_ep + 1):
            net.partial_fit((X0[:cut] - mu) / sg, Y0[:cut])
            v = np.mean(np.abs(m0 + s0 * np.sinh(net.predict((X0[cut:] - mu) / sg)) - Pa[tr[cut:]]))
            if v < best:
                best, best_ep = v, ep_
        mu, sg = X.mean(0), X.std(0)
        sg[sg == 0] = 1
        net = MLPRegressor(hidden_layer_sizes=(128, 64), alpha=1e-3, learning_rate_init=1e-3, batch_size=64, random_state=sd)
        for _ in range(best_ep):
            net.partial_fit((X - mu) / sg, Y)
        preds.append(m + s * np.sinh(net.predict((Xte - mu) / sg)))
        epochs.append(best_ep)
    return np.mean(preds, 0), epochs


def month_blocks(days):
    out = []
    for _, g in pd.Series(days, index=days).groupby(days.to_period("M")):
        out.append((IDX[g.index[0]], IDX[g.index[-1]]))
    return out


# ---------------------------------------------------------------- run (or load) the engine
def data_hash():
    h = hashlib.sha256(ENGINE_VERSION.encode())
    for f in ["power_da_prices_hourly_utc.csv", "generation_ro_mw_hourly_utc.csv", "generation_ro_mw_daily_cet.csv",
              "crossborder_ro_mw_daily_cet.csv", "eua_daily.csv"]:
        h.update(open(os.path.join(DATA, f), "rb").read())
    h.update(d(END).encode())
    return h.hexdigest()[:16]


CACHE = os.path.join(HERE, "cache", "forecasts.pkl")
KEY = data_hash()
FC = None
if not FRESH and os.path.exists(CACHE):
    with open(CACHE, "rb") as fh:
        tmp = pickle.load(fh)
    if tmp.get("key") == KEY:
        FC = tmp
if FC is None:
    t0 = time.time()
    ii = [IDX[t] for t in FDAYS]
    chunks = [ii[k::16] for k in range(16)]
    res = Parallel(n_jobs=16)(delayed(run_chunk)(P_, L_, R_, F_, c) for c in chunks)
    allr = {}
    for r_ in res:
        allr.update(r_)
    names = [k for k in allr[ii[0]] if k not in ("arx_coef", "lear_nz")]
    FC = {"key": KEY, "point": {k: np.array([allr[i][k] for i in ii]) for k in names},
          "arx_coef": np.array([allr[i]["arx_coef"] for i in ii]), "lear_nz": np.array([allr[i]["lear_nz"] for i in ii])}
    t_cls = time.time() - t0
    mb = month_blocks(TDAYS)
    g_res = Parallel(n_jobs=12)(delayed(gbm_month)(P_, L_, R_, F_, a, b) for a, b in mb)
    m_res = Parallel(n_jobs=12)(delayed(mlp_month)(P_, L_, R_, F_, a, b) for a, b in mb)
    FC["gbm"] = np.vstack([g[0] for g in g_res])
    FC["mlp"] = np.vstack([m_[0] for m_ in m_res])
    FC["mlp_epochs"] = [m_[1] for m_ in m_res]
    imp = g_res[-1][1]
    FC["gbm_last"] = imp
    FC["timing"] = {"classical_s": t_cls, "total_s": time.time() - t0}
    with open(CACHE, "wb") as fh:
        pickle.dump(FC, fh)
print("engine ready", FC.get("timing"))

# =============================================================================
# 2. Point forecasts on the test year: accuracy
# =============================================================================
FI = [IDX[t] for t in FDAYS]
ACT_F = P_[FI]                                                  # actual prices on burn-in + test days
POS = {t: k for k, t in enumerate(FDAYS)}
TI = np.array([POS[t] for t in TDAYS])
A = ACT_F[TI]
PT = dict(FC["point"])
PT["aw_arx"] = np.mean([PT[f"arx{T}"] for T in ARX_W], 0)
PT["aw_lear"] = np.mean([PT[f"lear{T}"] for T in LEAR_W], 0)
M = {k: v[TI] for k, v in PT.items()}
M["gbm"], M["mlp"] = FC["gbm"], FC["mlp"]
M["ens_lm"] = 0.5 * (M["aw_lear"] + M["mlp"])
M["ens_all"] = np.mean([M["aw_arx"], M["aw_lear"], M["gbm"], M["mlp"]], 0)
ORDER = ["naive", "snaive", "arx56", "arx84", "arx112", "arx714", "arx721", "arx728", "aw_arx", "arx728_noexog",
         "arx728_fund", "arx728_raw", "arx728_single", "lear364", "lear546", "lear728", "aw_lear", "gbm", "mlp",
         "ens_lm", "ens_all"]
NODST = ~DST.loc[TDAYS].values


def acc(F, rows=slice(None), hrs=slice(None)):
    a, f = A[rows][:, hrs], F[rows][:, hrs]
    e = a - f
    nz = np.abs(a) > 0
    den = np.abs(a) + np.abs(f)
    return {"mae": np.mean(np.abs(e)), "rmse": np.sqrt(np.mean(e ** 2)),
            "smape": np.mean(2 * np.abs(e[den > 0]) / den[den > 0]) * 100,          # pairs with price = forecast = 0 have no sMAPE
            "mape": np.mean(np.abs(e[nz]) / np.abs(a[nz])) * 100}


ACC = {}
for k in ORDER:
    r = acc(M[k])
    r["rmae"] = r["mae"] / acc(M["naive"])["mae"]
    r["mae_nodst"] = acc(M[k], NODST)["mae"]
    ACC[k] = {kk: fl(v, 4 if kk == "rmae" else 2) for kk, v in r.items()}
N["acc"] = ACC
N["test"] = {"mean": fl(A.mean(), 2), "sd": fl(A.std(), 2), "min": fl(A.min(), 2), "max": fl(A.max(), 2),
             "n_neg": int((A < 0).sum()), "n_le0": int((A <= 0).sum()), "n_abs5": int((np.abs(A) < 5).sum()),
             "n_zero": int((A == 0).sum()), "n_hours": int(A.size)}
best = min([k for k in ORDER if k not in ("naive", "snaive")], key=lambda k: ACC[k]["mae"])
N["best"] = {"key": best, "mae": ACC[best]["mae"], "rmae": ACC[best]["rmae"],
             "gain_pct": fl((1 - ACC[best]["rmae"]) * 100, 1)}
N["gain"] = {k: fl((1 - ACC[k]["rmae"]) * 100, 1) for k in ORDER}
N["best_classical"] = min(["aw_arx", "aw_lear", "lear364", "lear546", "lear728", "arx728"], key=lambda k: ACC[k]["mae"])

# MAPE breakdown: where does it explode?
_ape = np.abs(A - M["aw_lear"]) / np.abs(A)
_ape[~np.isfinite(_ape)] = np.nan
small = np.abs(A) < 5
N["mape"] = {"aw_lear": fl(np.nanmean(_ape) * 100, 1), "aw_lear_excl5": fl(np.nanmean(_ape[~small]) * 100, 1),
             "share_from_small": fl(np.nansum(_ape[small]) / np.nansum(_ape) * 100, 1), "max_ape": fl(np.nanmax(_ape) * 100, 0),
             "n_small": int(small.sum())}

# horizons: naive "same hour k days earlier" (information age) on the test year
hz = {}
for k in range(1, 15):
    hz[k] = float(np.mean(np.abs(A - P_[np.array([IDX[t] for t in TDAYS]) - k])))
N["horizon"] = {str(k): fl(v, 2) for k, v in hz.items()}
N["horizon"]["best_k"] = int(min(hz, key=hz.get))

# by hour and by month
BYHOUR = {k: np.mean(np.abs(A - M[k]), 0) for k in ORDER}
TM = TDAYS.to_period("M")
MONTHS_T = sorted(set(TM))
BYMONTH = {k: np.array([np.mean(np.abs(A[TM == mm] - M[k][TM == mm])) for mm in MONTHS_T]) for k in ORDER}
N["bymonth"] = {"months": [str(mm) for mm in MONTHS_T],
                "worst_month": str(MONTHS_T[int(np.argmax(BYMONTH["aw_lear"]))]),
                "worst_mae": fl(BYMONTH["aw_lear"].max(), 2), "best_month": str(MONTHS_T[int(np.argmin(BYMONTH["aw_lear"]))]),
                "best_mae": fl(BYMONTH["aw_lear"].min(), 2),
                "n_months_lear_beats_naive": int((BYMONTH["aw_lear"] < BYMONTH["naive"]).sum()),
                "n_months_ens_beats_lear": int((BYMONTH["ens_all"] < BYMONTH["aw_lear"]).sum())}
TQ = TDAYS.to_period("Q")
QUARTERS = sorted(set(TQ))
N["byq"] = {"q": [str(q_) for q_ in QUARTERS], "ndays": [int((TQ == q_).sum()) for q_ in QUARTERS]}
for k in ["naive", "aw_arx", "aw_lear", "gbm", "mlp", "ens_all"]:
    N["byq"][k] = [fl(np.mean(np.abs(A[TQ == q_] - M[k][TQ == q_])), 2) for q_ in QUARTERS]
hm_ = BYHOUR
N["byhour"] = {"single_worse_h": int((hm_["arx728_single"] > hm_["arx728"]).sum()),
               "gbm_beats_lear_h": int((hm_["gbm"] < hm_["aw_lear"]).sum()),
               "mlp_beats_lear_h": int((hm_["mlp"] < hm_["aw_lear"]).sum()),
               "ens_beats_lear_h": int((hm_["ens_all"] < hm_["aw_lear"]).sum()),
               "lear_worst_h": int(np.argmax(hm_["aw_lear"])), "lear_worst": fl(hm_["aw_lear"].max(), 2),
               "lear_best_h": int(np.argmin(hm_["aw_lear"])), "lear_best": fl(hm_["aw_lear"].min(), 2),
               "naive_worst_h": int(np.argmax(hm_["naive"]))}

# weekday breakdown of the naive rule (why d-7 on Mon/Sat/Sun)
dw_ = TDAYS.dayofweek.values
lag1 = P_[np.array([IDX[t] for t in TDAYS]) - 1]
N["naive_dow"] = {}
for nm, msk in [("monsatsun", np.isin(dw_, [0, 5, 6])), ("tuefri", ~np.isin(dw_, [0, 5, 6]))]:
    N["naive_dow"][nm] = {"lag1": fl(np.mean(np.abs(A[msk] - lag1[msk])), 2), "lag7": fl(np.mean(np.abs(A[msk] - M["snaive"][msk])), 2)}

# ARX coefficients (ARX(728), mean over the test days, hours 0..22)
CO = FC["arx_coef"][TI]                                     # days x 24 x 12
coef_mean = CO.mean(0)
CNAMES = ["const", "Y1", "Y2", "Y7", "Y1_23", "Ymin", "Ymax", "L", "R", "Mon", "Sat", "Sun"]
N["arxcoef"] = {c: {"min": fl(coef_mean[:23, j].min(), 3), "max": fl(coef_mean[:23, j].max(), 3),
                    "argmin": int(np.argmin(coef_mean[:23, j])), "argmax": int(np.argmax(coef_mean[:23, j]))}
                for j, c in enumerate(CNAMES)}
N["arxcoef"]["R_neg_hours"] = int((coef_mean[:23, 8] < 0).sum())

# LEAR selection
NZ = FC["lear_nz"][TI]                                      # days x 24 x 247
GROUPS = {"p1_same": None, "p1_other": None, "p2": (24, 48), "p3": (48, 72), "p7": (72, 96), "load": (96, 168),
          "res": (168, 240), "dow": (240, 247)}
SEL = np.zeros((len(GROUPS), 24))
for gi, (g, rg) in enumerate(GROUPS.items()):
    for h in range(24):
        if g == "p1_same":
            SEL[gi, h] = NZ[:, h, h].mean()
        elif g == "p1_other":
            SEL[gi, h] = NZ[:, h, [j for j in range(24) if j != h]].mean()
        else:
            SEL[gi, h] = NZ[:, h, rg[0]:rg[1]].mean()
nnz = NZ.sum(2)
N["lear"] = {"n_reg": int(NZ.shape[2]), "nnz_mean": fl(nnz.mean(), 1), "nnz_min": int(nnz.min()), "nnz_max": int(nnz.max()),
             "p1_same": fl(SEL[0].mean() * 100, 1), "p7": fl(SEL[4].mean() * 100, 1), "load": fl(SEL[5].mean() * 100, 1),
             "res": fl(SEL[6].mean() * 100, 1), "dow": fl(SEL[7].mean() * 100, 1),
             "nnz_share": fl(nnz.mean() / NZ.shape[2] * 100, 1)}


# =============================================================================
# 3. Diebold-Mariano tests (multivariate: daily mean |e| over 24 h; Newey-West variance, 7 lags; one-sided)
# =============================================================================
def nw_var(x, lags=7):
    x = x - x.mean()
    n = len(x)
    v = x @ x / n
    for k in range(1, lags + 1):
        v += 2 * (1 - k / (lags + 1)) * (x[k:] @ x[:-k]) / n
    return v


def dm(ea, eb, lags=7):
    dlt = np.mean(np.abs(ea), 1) - np.mean(np.abs(eb), 1)
    stat = dlt.mean() / np.sqrt(nw_var(dlt, lags) / len(dlt))
    return stat, 1 - stats.norm.cdf(stat)


DM_MODELS = ["naive", "snaive", "arx728", "aw_arx", "lear728", "aw_lear", "gbm", "mlp", "ens_lm", "ens_all"]
E = {k: A - M[k] for k in ORDER}
DMP = np.full((len(DM_MODELS), len(DM_MODELS)), np.nan)
for a_, ka in enumerate(DM_MODELS):
    for b_, kb in enumerate(DM_MODELS):
        if a_ != b_:
            DMP[a_, b_] = dm(E[ka], E[kb])[1]
st_, p_ = dm(E["naive"], E["aw_lear"])
st2, p2 = dm(E["aw_lear"], E["ens_all"])
st3, p3 = dm(E["aw_arx"], E["aw_lear"])
st4, p4 = dm(E["aw_lear"], E["gbm"])
N["dm"] = {"naive_lear": {"stat": fl(st_, 2), "p": fl(p_, 4)}, "lear_ens": {"stat": fl(st2, 2), "p": fl(p2, 4)},
           "arx_lear": {"stat": fl(st3, 2), "p": fl(p3, 4)}, "lear_gbm": {"stat": fl(st4, 2), "p": fl(p4, 4)},
           "n_sig_vs_naive": int(sum(DMP[0, j] < 0.05 for j in range(1, len(DM_MODELS)))),
           "n_models": len(DM_MODELS), "n_others": len(DM_MODELS) - 1, "n_days": int(len(TDAYS)),
           "ens_beats_all": bool(all(DMP[j, DM_MODELS.index("ens_all")] < 0.05 for j in range(len(DM_MODELS))
                                     if DM_MODELS[j] != "ens_all"))}
_e = E["aw_lear"]
_c = np.corrcoef(_e.T)
N["path"] = {"corr_12_13": fl(_c[12, 13], 2), "corr_03_19": fl(_c[3, 19], 2), "corr_mean": fl(_c[np.triu_indices(24, 1)].mean(), 2)}

# =============================================================================
# 4. Probabilistic forecasts: QRA (on AW-ARX and AW-LEAR), conformal (CP) and historical simulation (HS) on AW-LEAR
# =============================================================================
TAUS = np.arange(1, 100) / 100
W_QRA, W_ERR = 182, 112
FA, FL_ = PT["aw_arx"], PT["aw_lear"]                     # burn-in + test, FDAYS order
WEEK0 = list(range(N_BURN, len(FDAYS), 7))


def qra_hour(h):
    import warnings as _w
    _w.filterwarnings("ignore")                                 # iteration-limit warnings at the extreme quantiles
    out = np.full((len(FDAYS), len(TAUS)), np.nan)
    for w in WEEK0:
        tr = np.arange(w - W_QRA, w)
        assert tr.max() < w and tr.min() >= 0                     # past forecasts only
        X = sm.add_constant(np.column_stack([FA[tr, h], FL_[tr, h]]))
        y = ACT_F[tr, h]
        te = np.arange(w, min(w + 7, len(FDAYS)))
        Xt = sm.add_constant(np.column_stack([FA[te, h], FL_[te, h]]), has_constant="add")
        for j, tau in enumerate(TAUS):
            b = QuantReg(y, X).fit(q=tau, max_iter=5000).params
            out[te, j] = Xt @ b
    return out


QCACHE = os.path.join(HERE, "cache", "qra.pkl")
QRA = None
if not FRESH and os.path.exists(QCACHE):
    with open(QCACHE, "rb") as fh:
        tmp = pickle.load(fh)
    if tmp.get("key") == KEY:
        QRA = tmp["q"]
if QRA is None:
    qh = Parallel(n_jobs=16)(delayed(qra_hour)(h) for h in range(24))
    QRA = np.stack(qh, 1)                                      # FDAYS x 24 x 99
    with open(QCACHE, "wb") as fh:
        pickle.dump({"key": KEY, "q": QRA}, fh)
QRA = np.sort(QRA[TI], axis=2)                                 # rearrangement: no quantile crossing

ERR_L = ACT_F - FL_
CPQ = np.zeros((len(TDAYS), 24, len(TAUS)))
HSQ = np.zeros_like(CPQ)
for k, t in enumerate(TI):
    win = ERR_L[t - W_ERR:t]                                     # errors of the previous W days, same hour
    for j, tau in enumerate(TAUS):
        HSQ[k, :, j] = FL_[t] + np.quantile(win, tau, axis=0)
        CPQ[k, :, j] = FL_[t] + np.sign(tau - 0.5) * np.quantile(np.abs(win), abs(2 * tau - 1), axis=0)


def prob_scores(Q):
    y = A[:, :, None]
    ps = (((y < Q).astype(float) - TAUS[None, None, :]) * (Q - y)).mean()
    lo50, hi50, lo90, hi90 = Q[:, :, 24], Q[:, :, 74], Q[:, :, 4], Q[:, :, 94]
    c50 = ((A >= lo50) & (A <= hi50)).mean()
    inside90 = (A >= lo90) & (A <= hi90)
    n, x = inside90.size, int((~inside90).sum())
    ph = x / n
    lr = -2 * ((n - x) * np.log(0.9) + x * np.log(0.1) - ((n - x) * np.log(1 - ph) + x * np.log(ph)))
    rel = [((A <= Q[:, :, j]).mean()) for j in range(len(TAUS))]
    g_ = (~inside90).mean(axis=1) - 0.1                         # daily miss share: robust to dependence within the day
    z_ = g_.mean() / np.sqrt(nw_var(g_, 7) / len(g_))
    return {"aps": ps, "c50": c50 * 100, "c90": inside90.mean() * 100, "w90": (hi90 - lo90).mean(), "kupiec": lr,
            "kupiec_p": 1 - stats.chi2.cdf(lr, 1), "hac_z": z_, "hac_p": 2 * stats.norm.sf(abs(z_)), "rel": rel}


PROB = {"qra": prob_scores(QRA), "cp": prob_scores(CPQ), "hs": prob_scores(HSQ)}
N["prob"] = {k: {kk: fl(v, 4 if kk in ("kupiec_p", "hac_p") else 2) for kk, v in r.items() if kk != "rel"} for k, r in PROB.items()}
N["prob"]["w_qra"], N["prob"]["w_err"] = W_QRA, W_ERR
N["prob"]["best"] = min(["qra", "cp", "hs"], key=lambda k: PROB[k]["aps"])
N["prob"]["mae_median_qra"] = fl(np.mean(np.abs(A - QRA[:, :, 49])), 2)


# =============================================================================
# 5. Cointegration
# =============================================================================
def adf_p(x):
    return adfuller(x, regression="c", autolag="AIC")[1]


DLY = PD.loc[START:END, ["RO", "HU", "DE_LU"]].dropna()
co = {"start": d(DLY.index.min()), "end": d(DLY.index.max()), "T": int(len(DLY))}
for z in ["RO", "HU", "DE_LU"]:
    co[f"adf_{z}"] = fl(adf_p(DLY[z]), 4)
    co[f"adfd_{z}"] = fl(adf_p(DLY[z].diff().dropna()), 4)
for z in ["HU", "DE_LU"]:
    eg = coint(DLY["RO"], DLY[z], trend="c", autolag="aic")
    ols = sm.OLS(DLY["RO"], sm.add_constant(DLY[z])).fit()
    u = ols.resid
    phi = sm.OLS(u.values[1:], u.values[:-1]).fit().params[0]
    jo = coint_johansen(DLY[["RO", z]].values, det_order=0, k_ar_diff=6)
    co[z] = {"eg": fl(eg[0], 2), "eg_p": fl(eg[1], 4), "eg_cv5": fl(eg[2][1], 2), "beta": fl(ols.params[z], 3),
             "alpha": fl(ols.params["const"], 2), "phi": fl(phi, 3), "hl": fl(np.log(0.5) / np.log(phi), 1),
             "tr0": fl(jo.lr1[0], 2), "tr0_cv": fl(jo.cvt[0, 1], 2), "tr1": fl(jo.lr1[1], 2), "tr1_cv": fl(jo.cvt[1, 1], 2),
             "rank": int((jo.lr1 > jo.cvt[:, 1]).sum()) if jo.lr1[0] > jo.cvt[0, 1] else 0,
             "sd_spread": fl((DLY["RO"] - DLY[z]).std(), 2), "mean_spread": fl((DLY["RO"] - DLY[z]).mean(), 2)}
hp_ = HP.copy()
hp_.index = pd.to_datetime(hp_.index, utc=True).tz_convert(TZ)
hpt = hp_.loc[str(TEST0.date()):str(END.date())]
co["eq_hu_test"] = fl((np.abs(hpt["RO"] - hpt["HU"]) < 0.01).mean() * 100, 1)
co["eq_de_test"] = fl((np.abs(hpt["RO"] - hpt["DE_LU"]) < 0.01).mean() * 100, 1)
N["coint"] = co

# monthly: price, TTF gas, hydro (Lecture 1 promise)
GHu = GH.copy()
GHu.index = pd.to_datetime(GHu.index, utc=True)
hyd = GHu[["hydro_run_of_river", "hydro_water_reservoir"]].sum(axis=1, min_count=2)
END_UTC = (END + pd.Timedelta(days=1)).tz_localize(TZ).tz_convert("UTC")
hyd = hyd[hyd.index < END_UTC]
hyd_m = hyd.tz_convert(TZ).resample("MS").sum(min_count=600) / 1e6     # CET/CEST calendar months, as the prices
hyd_m.index = hyd_m.index.tz_localize(None)
TTF = ep.ttf_monthly()
MD = pd.concat([PD["RO"].loc[:END].resample("MS").mean().rename("price"), TTF["ttf_eur_mwh"].rename("ttf"),
                hyd_m.rename("hydro")], axis=1).dropna()
MD["hydro_ds"] = MD["hydro"] - MD.groupby(MD.index.month)["hydro"].transform("mean")
cm = {"start": MD.index.min().strftime("%Y-%m"), "end": MD.index.max().strftime("%Y-%m"), "T": int(len(MD)),
      "adf_price": fl(adf_p(MD["price"]), 4), "adf_ttf": fl(adf_p(MD["ttf"]), 4), "adf_hyds": fl(adf_p(MD["hydro_ds"]), 4),
      "adf_dprice": fl(adf_p(MD["price"].diff().dropna()), 4), "adf_dttf": fl(adf_p(MD["ttf"].diff().dropna()), 4)}
eg1 = coint(MD["price"], MD["ttf"], trend="c", autolag="aic")
eg2 = coint(MD["price"], MD[["ttf", "hydro"]], trend="c", autolag="aic")
lr_ = sm.OLS(MD["price"], sm.add_constant(MD[["ttf"]])).fit()
u_ = lr_.resid
jo = coint_johansen(MD[["price", "ttf"]].values, det_order=0, k_ar_diff=2)
ecm_df = pd.DataFrame({"dp": MD["price"].diff(), "u1": u_.shift(1), "dttf": MD["ttf"].diff(), "hyd": MD["hydro_ds"]}).dropna()
ecm = sm.OLS(ecm_df["dp"], sm.add_constant(ecm_df[["u1", "dttf", "hyd"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
al = ecm.params["u1"]
cm.update({"eg1": fl(eg1[0], 2), "eg1_p": fl(eg1[1], 4), "eg1_cv5": fl(eg1[2][1], 2), "eg2": fl(eg2[0], 2), "eg2_p": fl(eg2[1], 4),
           "eg2_cv5": fl(eg2[2][1], 2), "beta": fl(lr_.params["ttf"], 3), "const": fl(lr_.params["const"], 2),
           "tr0": fl(jo.lr1[0], 2), "tr0_cv": fl(jo.cvt[0, 1], 2), "tr1": fl(jo.lr1[1], 2), "tr1_cv": fl(jo.cvt[1, 1], 2),
           "alpha": fl(al, 3), "alpha_t": fl(ecm.tvalues["u1"], 2), "hl": fl(np.log(0.5) / np.log(1 + al), 1),
           "g_dttf": fl(ecm.params["dttf"], 3), "g_dttf_t": fl(ecm.tvalues["dttf"], 2),
           "d_hyd": fl(ecm.params["hyd"], 2), "d_hyd_t": fl(ecm.tvalues["hyd"], 2), "ecm_n": int(ecm.nobs),
           "ecm_r2": fl(ecm.rsquared, 3)})
cm["eff"] = fl(100 / lr_.params["ttf"], 1)                # 1/beta: MWh of gas per MWh of power, as an efficiency
cm["eg1_reject"] = bool(eg1[1] < 0.05)
cm["eg2_reject"] = bool(eg2[1] < 0.05)
cm["jo_rank"] = (1 if jo.lr1[1] <= jo.cvt[1, 1] else 2) if jo.lr1[0] > jo.cvt[0, 1] else 0
N["coint_m"] = cm

# =============================================================================
# 6. Case studies on the test year: 15-minute MTU, battery and flexible consumer
# =============================================================================
XN_ALL = ep.prices_native()
_xn = XN_ALL.loc[str((TEST0 - pd.Timedelta(days=40)).date()):str(END.date()), "RO"]
ALLQ = {}
for dd, g in _xn.groupby(_xn.index.tz_localize(None).normalize()):
    if len(g) == 96:
        ALLQ[dd] = g.values
QDAYS = [t for t in TDAYS if t in ALLQ and not DST.loc[t]]
Q = np.array([ALLQ[t] for t in QDAYS])                         # days x 96 quarter-hours
hourly_mean = Q.reshape(len(QDAYS), 24, 4).mean(2)
dev = Q - np.repeat(hourly_mean, 4, axis=1)                   # intra-hour deviation from the hourly mean
fl_lear = np.array([M["aw_lear"][POS[t] - N_BURN] for t in QDAYS])
flat = np.repeat(fl_lear, 4, axis=1)
shape = np.zeros_like(Q)
for k, t in enumerate(QDAYS):
    past = [ALLQ[t - pd.Timedelta(days=j)] for j in range(1, 29) if (t - pd.Timedelta(days=j)) in ALLQ]   # days d-28..d-1
    shape[k] = np.mean([p - np.repeat(p.reshape(24, 4).mean(1), 4) for p in past], 0)
shaped = flat + shape
N["mtu15"] = {"n_days": len(QDAYS), "mae_flat": fl(np.mean(np.abs(Q - flat)), 2), "mae_shaped": fl(np.mean(np.abs(Q - shaped)), 2),
              "mae_hourly": fl(np.mean(np.abs(hourly_mean - fl_lear)), 2), "intra_mad": fl(np.mean(np.abs(dev)), 2),
              "gain_pct": fl((1 - np.mean(np.abs(Q - shaped)) / np.mean(np.abs(Q - flat))) * 100, 1),
              "mae_shape_only": fl(np.mean(np.abs(dev - shape)), 2)}
_ix = int(np.argmax(np.abs(dev).mean(1)))
QDAY = QDAYS[_ix]
N["mtu15"]["day"] = d(QDAY)
N["mtu15"]["day_intra"] = fl(np.abs(dev[_ix]).mean(), 2)


def battery(F, Aa, eta=0.9):
    """1 MW / 2 MWh battery, one cycle a day: charge in a 2-hour block, discharge in a later 2-hour block, both chosen on the
    forecast; trade only if the forecast spread pays the losses. Profit in EUR, valued at actual prices."""
    prof = np.zeros(len(F))
    for k in range(len(F)):
        f, a = F[k], Aa[k]
        bestv, bs = 0.0, None
        for i in range(0, 21):
            for j in range(i + 2, 23):
                v = eta * (f[j] + f[j + 1]) - (f[i] + f[i + 1])
                if v > bestv:
                    bestv, bs = v, (i, j)
        if bs:
            i, j = bs
            prof[k] = eta * (a[j] + a[j + 1]) - (a[i] + a[i + 1])
    return prof


def flex(F, Aa, L=4, fixed=8):
    """Flexible process of 1 MW for L consecutive hours a day: start chosen on the forecast; cost in EUR at actual prices."""
    cost, base = np.zeros(len(F)), np.zeros(len(F))
    for k in range(len(F)):
        s = int(np.argmin([F[k][i:i + L].sum() for i in range(24 - L + 1)]))
        cost[k] = Aa[k][s:s + L].sum()
        base[k] = Aa[k][fixed:fixed + L].sum()
    return cost, base


BATK = ["naive", "aw_arx", "aw_lear", "gbm", "ens_all"]
AN = A[NODST]                                                    # DST days left out: their 24 columns are not 24 physical hours
BAT = {k: battery(M[k][NODST], AN) for k in BATK}
BAT["perfect"] = battery(AN, AN)
FLX = {k: flex(M[k][NODST], AN)[0] for k in BATK}
FLX["perfect"], FLX_BASE = flex(AN, AN)
N["battery"] = {k: {"eur": fl(v.sum(), 0), "pct": fl(v.sum() / BAT["perfect"].sum() * 100, 1),
                    "loss_days": int((v < 0).sum())} for k, v in BAT.items()}
N["battery"]["eta"] = 0.9
N["battery"]["n_days"] = int(NODST.sum())
N["flex"] = {k: {"eur": fl(v.sum(), 0), "save": fl((FLX_BASE.sum() - v.sum()), 0), "eur_mwh": fl(v.sum() / (4 * len(v)), 2)}
             for k, v in FLX.items()}
N["flex"]["base_eur_mwh"] = fl(FLX_BASE.sum() / (4 * len(FLX_BASE)), 2)
N["flex"]["base_eur"] = fl(FLX_BASE.sum(), 0)

# stress week (highest mean price, Monday to Sunday) and the week for the probabilistic chart (last full week without DST)
mons = [t for t in TDAYS if t.dayofweek == 0 and t + pd.Timedelta(days=6) <= END]
SW = max(mons, key=lambda t: A[POS[t] - N_BURN:POS[t] - N_BURN + 7].mean())
PW = max(t for t in mons if not DST.loc[t:t + pd.Timedelta(days=6)].any())
sw = slice(POS[SW] - N_BURN, POS[SW] - N_BURN + 7)
N["weeks"] = {"stress": d(SW), "stress_end": d(SW + pd.Timedelta(days=6)), "prob": d(PW), "prob_end": d(PW + pd.Timedelta(days=6)),
              "stress_mean": fl(A[sw].mean(), 2), "stress_max": fl(A[sw].max(), 2),
              "stress_mae": {k: fl(np.mean(np.abs(A[sw] - M[k][sw])), 2) for k in ["naive", "aw_arx", "aw_lear", "gbm", "mlp", "ens_all"]}}

# =============================================================================
# 7. Leakage self-check
#    (a) timestamp audit: every input of the forecast for day d must be public before 12:00 CET on d-1
#    (b) perturbation: recompute forecasts with prices from d and fundamentals from d-1 set to NaN; they must not change
# =============================================================================
def avail_time(src, lag, t):
    row = t - pd.Timedelta(days=lag)
    if src == "price":        # the auction for delivery day `row` closes 12:00 CET on row-1; results published about 13:00
        return row - pd.Timedelta(days=1) + pd.Timedelta(hours=13)
    if src == "realised":     # metered day `row` is complete at 24:00 of `row`
        return row + pd.Timedelta(days=1)
    if src == "close":        # carbon ETC close on trading day `row` (London, 16:30 local = 17:30 CET)
        return row + pd.Timedelta(hours=17, minutes=30)
    raise ValueError(src)


AUDIT = FEATURE_REGISTRY + [("VST median/MAD, latest price row", 1, "price"), ("z-score of load/RES, latest row", 2, "realised"),
                            ("asinh of load/RES (LEAR), latest row", 2, "realised")]
n_chk, worst = 0, pd.Timedelta(days=-99)
for t in FDAYS:
    cut = t - pd.Timedelta(days=1) + pd.Timedelta(hours=12)
    for blk, lag, src in AUDIT:
        a_t = avail_time(src, lag, t)
        assert a_t <= cut, f"leak: {blk} lag {lag} for {t.date()}"
        worst = max(worst, a_t - cut)
        n_chk += 1
for i0, i1 in month_blocks(TDAYS):                              # ML: last training target row i0-1 must be public at the cut-off of i0
    assert avail_time("price", 1, CAL[i0]) <= CAL[i0] - pd.Timedelta(hours=12)
    n_chk += 1
for w in WEEK0:                                                 # QRA: fitted on forecast days strictly before the week
    assert max(range(w - W_QRA, w)) < w
    n_chk += 1
leak = {"n_timestamp_checks": n_chk, "margin_h": fl(-worst / pd.Timedelta(hours=1), 1)}


def corrupt(i, fill=np.nan):
    """Data as a function sees them if everything after gate closure is deleted (fill=NaN) or replaced by nonsense (finite fill)."""
    Pc, Lc, Rc = P_.copy(), L_.copy(), R_.copy()
    Pc[i:] = fill                                               # prices of day d and later unknown
    Lc[i - 1:] = fill                                           # realised quantities of d-1 and later unknown
    Rc[i - 1:] = fill
    raw = FUND_RAW.copy()
    raw.loc[CAL[i - 1]:] = fill
    return Pc, Lc, Rc, raw.ffill().shift(2).reindex(CAL).values.astype(float)


PERT_DAYS = list(TDAYS[::30]) + [TDAYS[-1]]                  # classical models: 14 days across the test year


def pert_classical(t, fill):
    i = IDX[t]
    r = point_day(*corrupt(i, fill), i)
    out = 0.0
    for k, v in FC["point"].items():
        dv = np.max(np.abs(np.asarray(r[k]) - v[POS[t]]))
        assert np.all(np.isfinite(r[k])) and dv < 1e-6, f"perturbation changed {k} on {t.date()}: {dv}"
        out = max(out, dv)
    assert np.array_equal(r["lear_nz"], FC["lear_nz"][POS[t]])
    return out, len(FC["point"])


def pert_ml(a0, fill):                                          # first day of every monthly refit: the day most exposed to a leak
    g_ = gbm_month(*corrupt(a0, fill), a0, a0)[0][0]
    m_ = mlp_month(*corrupt(a0, fill), a0, a0)[0][0]
    k_ = POS[CAL[a0]] - N_BURN
    return max(np.max(np.abs(g_ - M["gbm"][k_])), np.max(np.abs(m_ - M["mlp"][k_])))


jobs = [(t, f_) for t in PERT_DAYS for f_ in (np.nan, 1e4)]
rc = Parallel(n_jobs=16)(delayed(pert_classical)(t, f_) for t, f_ in jobs)
rm = Parallel(n_jobs=12)(delayed(pert_ml)(a0, f_) for a0, _ in month_blocks(TDAYS) for f_ in (np.nan, 1e4))
assert max(rm) < 1e-6, max(rm)
leak.update({"pert_days": [d(t) for t in PERT_DAYS], "n_pert_days": len(PERT_DAYS), "n_ml_months": len(month_blocks(TDAYS)),
             "n_series": len(FC["point"]) + 2, "n_recomputed": int(sum(r_[1] for r_ in rc) + 2 * len(rm)),
             "max_abs_diff": float(max(max(r_[0] for r_ in rc), max(rm))), "passed": True})
N["leak"] = leak
print("leakage self-check PASSED:", leak)

# =============================================================================
# 8. Case-study headline numbers (computed by the case notebooks; copied, not retyped)
# =============================================================================
for c_, fol in [("c2", "C2_load_forecasting"), ("c7", "C7_spike_early_warning"), ("c1", "C1_crisis_2024")]:
    with open(os.path.join(REPO, "cases", fol, "numbers.json")) as fh:
        N[c_] = json.load(fh)
N["c2"]["testStartISO"] = d(pd.Timestamp(N["c2"]["testStart"]))
N["ml"] = {"gbm_trees": 500, "mlp_epochs_med": int(np.median(np.concatenate([np.array(e) for e in FC["mlp_epochs"]]))),
           "mlp_epochs_min": int(np.min(np.concatenate([np.array(e) for e in FC["mlp_epochs"]]))),
           "mlp_epochs_max": int(np.max(np.concatenate([np.array(e) for e in FC["mlp_epochs"]]))),
           "n_refits": len(month_blocks(TDAYS)), "mlp_seeds": 4, "first_train": d(CAL[7])}

# =============================================================================
# Charts: one set per language
# =============================================================================
LAB = {"naive": ("Naive", "Naiv"), "snaive": ("Seasonal naive", "Naiv sezonier"), "arx728": ("ARX(728)", "ARX(728)"),
       "aw_arx": ("AW-ARX", "AW-ARX"), "lear728": ("LEAR(728)", "LEAR(728)"), "aw_lear": ("AW-LEAR", "AW-LEAR"),
       "gbm": ("GBM", "GBM"), "mlp": ("MLP", "MLP"), "ens_lm": ("Ens. LEAR+MLP", "Ans. LEAR+MLP"),
       "ens_all": ("Ens. 4 models", "Ans. 4 modele"), "perfect": ("Perfect foresight", "Informație perfectă")}
COL = {"naive": "#9a9a9a", "snaive": "#c4c4c4", "aw_arx": PAL["HU"], "arx728": PAL["HU"], "aw_lear": PAL["RO"],
       "lear728": PAL["RO"], "gbm": PAL["BG"], "mlp": PAL["c7"], "ens_all": PAL["DE_LU"], "ens_lm": PAL["c5"], "perfect": "#222222"}
SRC = {"en": {"ec": "energy-charts.info (Fraunhofer ISE); OPCOM day-ahead prices for Romania, via ENTSO-E",
              "ecl": "energy-charts.info (Fraunhofer ISE); OPCOM prices; ENTSO-E load, wind and solar (Transelectrica data for Romania)",
              "ecf": "energy-charts.info (Fraunhofer ISE); OPCOM prices; ENTSO-E generation and flows (Transelectrica data for Romania); "
                     "Yahoo Finance (SparkChange EUA ETC)",
              "hu": "energy-charts.info (Fraunhofer ISE); prices of OPCOM (RO), HUPX (HU) and EPEX SPOT (DE-LU), via ENTSO-E",
              "m": "energy-charts.info (OPCOM prices; ENTSO-E hydro generation, Transelectrica data); World Bank Pink Sheet (TTF)",
              "q": "energy-charts.info (Fraunhofer ISE); OPCOM 15-minute day-ahead prices for Romania, via ENTSO-E"},
       "ro": {"ec": "energy-charts.info (Fraunhofer ISE); prețurile PZU ale OPCOM pentru România, prin ENTSO-E",
              "ecl": "energy-charts.info (Fraunhofer ISE); prețuri OPCOM; consum, producție eoliană și solară: ENTSO-E (date Transelectrica)",
              "ecf": "energy-charts.info (Fraunhofer ISE); prețuri OPCOM; producție și fluxuri: ENTSO-E (date Transelectrica); "
                     "Yahoo Finance (SparkChange EUA ETC)",
              "hu": "energy-charts.info (Fraunhofer ISE); prețurile OPCOM (RO), HUPX (HU) și EPEX SPOT (DE-LU), prin ENTSO-E",
              "m": "energy-charts.info (prețuri OPCOM; producția hidro ENTSO-E, date Transelectrica); Banca Mondială, Pink Sheet (TTF)",
              "q": "energy-charts.info (Fraunhofer ISE); prețuri PZU pe 15 minute (OPCOM), prin ENTSO-E"}}


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


def layout_check(fig, name, lang):
    """Warn when a y-label is taller than its axes (it gets clipped) or the figure grows wider than 6.6 in."""
    fig.canvas.draw()
    rr = fig.canvas.get_renderer()
    for ax in fig.axes:
        lab = ax.yaxis.label
        if lab.get_text() and lab.get_window_extent(rr).height > ax.get_window_extent(rr).height * 1.08:
            print(f"  [layout] {name} ({lang}): y-label '{lab.get_text()}' taller than its axes")
    w = fig.get_tightbbox(rr).width
    if w > 6.6:
        print(f"  [layout] {name} ({lang}): figure {w:.2f} in wide")


def out(fig, lang, name, bottom=0.17, also_x=()):
    comma_axes(fig, lang, also_x)
    os.makedirs(os.path.join(HERE, "charts", lang), exist_ok=True)
    fig.tight_layout(rect=(0, bottom, 1, 1))
    layout_check(fig, name, lang)
    save(fig, os.path.join(HERE, "charts", lang, name + ".pdf"), bottom=bottom)


def num(v, lang, k=1):
    s = f"{v:.{k}f}"
    return s.replace(".", ",") if lang == "ro" else s


def mfmt(ax, lang, step=1):
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=step))
    if lang == "ro":
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: MON_RO[mdates.num2date(v).month - 1] +
                                                   (f"\n{mdates.num2date(v).year}" if mdates.num2date(v).month == 1 else "")))
    else:
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: MON_EN[mdates.num2date(v).month - 1] +
                                                   (f"\n{mdates.num2date(v).year}" if mdates.num2date(v).month == 1 else "")))


DAYN = {"en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "ro": ["lun.", "mar.", "mie.", "joi", "vin.", "sîm.", "dum."]}
GLAB = {"en": ["P(d-1), same hour", "P(d-1), other hours", "P(d-2)", "P(d-3)", "P(d-7)", "Load (d-2,d-3,d-7)",
               "Wind+solar (d-2,d-3,d-7)", "Day of week"],
        "ro": ["P(d-1), aceeași oră", "P(d-1), alte ore", "P(d-2)", "P(d-3)", "P(d-7)", "Consum (d-2,d-3,d-7)",
               "Eolian+solar (d-2,d-3,d-7)", "Ziua săptămînii"]}
DAILY = pd.Series(PM.mean(1).values, index=CAL)
for lang in ["en", "ro"]:
    T = (lambda en, ro: en) if lang == "en" else (lambda en, ro: ro)
    L = lambda k: LAB[k][0 if lang == "en" else 1]  # noqa: E731
    # 1 chronological design
    fig, ax = plt.subplots(figsize=(6.4, 2.1))
    c0 = FC0 - pd.Timedelta(days=728)
    ax.axvspan(c0, FC0 - pd.Timedelta(days=1), color=PAL["HU"], alpha=0.12, lw=0, label=T("calibration window, 728 days (first forecast)", "calibrare, 728 de zile (prima prognoză)"))
    ax.axvspan(FC0, TEST0 - pd.Timedelta(days=1), color=PAL["BG"], alpha=0.25, lw=0, label=T("burn-in, 182 days", "rodaj (burn-in), 182 de zile"))
    ax.axvspan(TEST0, END, color=PAL["DE_LU"], alpha=0.18, lw=0, label=T("test, 365 days", "test, 365 de zile"))
    ax.plot(DAILY.index, DAILY.values, color=PAL["RO"], lw=0.8, label=T("Romania, daily base price", "România, prețul zilnic de bază"))
    ax.set_ylabel("EUR/MWh")
    ax.set_xlim(CAL[0], END)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, ncol=2)
    out(fig, lang, "split_timeline", bottom=0.24)
    # 2 horizons
    fig, ax = plt.subplots(figsize=(6.4, 1.9))
    ks = list(range(1, 15))
    ax.bar(ks, [hz[k] for k in ks], color=[PAL["DE_LU"] if k % 7 == 0 else PAL["RO"] for k in ks], width=0.7)
    from matplotlib.patches import Patch
    hnd = [Patch(color=PAL["RO"], label=T("same hour, k days earlier", "aceeași oră, cu k zile înainte")),
           Patch(color=PAL["DE_LU"], label=T("k = 7, 14 (same weekday)", "k = 7, 14 (aceeași zi a săptămînii)"))]
    ax.set_xticks(ks)
    ax.set_xlabel(T("age of the information k (days)", "vechimea informației k (zile)"))
    ax.set_ylabel("MAE,\nEUR/MWh")
    legend_bottom(fig, handles=hnd, labels=[h_.get_label() for h_ in hnd], ncol=2)
    out(fig, lang, "horizon_naive", bottom=0.16)
    # 3 MAPE fails near zero
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    x_, y_ = A.ravel(), (_ape.ravel() * 100)
    ok = np.isfinite(y_) & (y_ > 0)
    ax.axvspan(-5, 5, color=PAL["c8"], alpha=0.15, lw=0, label=T("|price| < 5 EUR/MWh", "|preț| < 5 EUR/MWh"))
    ax.scatter(np.clip(x_[ok], -120, 620), y_[ok], s=1.5, color=PAL["RO"], alpha=0.35, lw=0,
               label=T("one hour, AW-LEAR", "o oră, AW-LEAR"))
    ax.axhline(100, color="#222222", lw=0.7, ls="--", label=T("error = 100%", "eroare = 100%"))
    ax.set_yscale("log")
    ax.set_yticks([1e-2, 1, 1e2, 1e4, 1e6])
    ax.set_yticklabels(["0.01", "1", "100", "10$^4$", "10$^6$"] if lang == "en" else ["0,01", "1", "100", "10$^4$", "10$^6$"])
    ax.set_xlabel(T("actual price, EUR/MWh", "prețul realizat, EUR/MWh"))
    ax.set_ylabel(T("absolute\n% error", "eroarea\nprocentuală, %"), fontsize=10)
    legend_bottom(fig, ncol=3)
    for h_ in getattr(fig.legends[-1], "legend_handles", None) or fig.legends[-1].legendHandles:
        if hasattr(h_, "set_sizes"):           # make the scatter marker visible in the legend
            h_.set_sizes([30])
            h_.set_alpha(1)
    out(fig, lang, "mape_fail", bottom=0.15, also_x=[ax])
    # 4 DM chessboard
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("dm", ["#0b6e2e", "#7fc97f", "#ffe08a", "#f4a259", "#d7301f", "#5a0000"])
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    Z = np.where(np.isnan(DMP), np.nan, np.minimum(DMP, 0.10))
    im = ax.imshow(np.ma.masked_invalid(Z), cmap=cmap, vmin=0, vmax=0.10, aspect="auto")
    ax.set_xticks(range(len(DM_MODELS)))
    ax.set_xticklabels([str(i + 1) for i in range(len(DM_MODELS))], fontsize=10)
    ax.set_yticks(range(len(DM_MODELS)))
    ax.set_yticklabels([f"{L(k)} ({i + 1})" for i, k in enumerate(DM_MODELS)], fontsize=10)
    ax.tick_params(length=0)
    ax.set_xlabel(T("column j: is model (j) more accurate than the row model?",
                    "coloana j: este modelul (j) mai precis decît modelul din rînd?"), fontsize=10)
    for a_ in range(len(DM_MODELS)):
        ax.add_patch(plt.Rectangle((a_ - 0.5, a_ - 0.5), 1, 1, color="#ffffff"))
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label(T("p-value", "valoarea p"), fontsize=9.5)
    cb.set_ticks([0, 0.02, 0.04, 0.06, 0.08, 0.10])
    cb.set_ticklabels([num(v, lang, 2) for v in [0, 0.02, 0.04, 0.06, 0.08]] + ["$\\geq$" + num(0.10, lang, 2)])
    cb.ax.tick_params(labelsize=9.5)
    cb.ax._keep_y = True
    ax._keep_y = True
    ax.spines[:].set_visible(False)
    out(fig, lang, "dm_matrix", bottom=0.0)
    # 5 ARX coefficients by hour
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    hh = np.arange(23)
    for j, c, lab, ls in [(1, PAL["RO"], "$Y_{d-1,h}$", "-"), (2, PAL["HU"], "$Y_{d-2,h}$", "--"), (3, PAL["DE_LU"], "$Y_{d-7,h}$", "-."),
                          (7, "#222222", T("load $\\tilde L_{d,h}$", "consum $\\tilde L_{d,h}$"), "-"),
                          (8, PAL["BG"], T("wind+solar $\\tilde R_{d,h}$", "eolian+solar $\\tilde R_{d,h}$"), "-")]:
        ax.plot(hh, coef_mean[:23, j], color=c, ls=ls, marker="o", ms=3, label=lab)
    ax.axhline(0, color="#222222", lw=0.5)
    ax.set_xticks(range(0, 23, 2))
    ax.set_xlabel(T("hour h (CET)", "ora h (CET)"))
    ax.set_ylabel(T("mean\ncoefficient", "coeficient\nmediu"))
    legend_bottom(fig, ncol=5)
    out(fig, lang, "arx_coef", bottom=0.16)
    # 6 per-hour vs single model
    fig, ax = plt.subplots(figsize=(6.4, 1.9))
    h24 = np.arange(24)
    ax.plot(h24, BYHOUR["naive"], color=COL["naive"], ls=":", marker="o", ms=3, label=L("naive"))
    ax.plot(h24, BYHOUR["arx728_single"], color=PAL["DE_LU"], marker="s", ms=3, label=T("one ARX(728) for all hours", "un ARX(728) pentru toate orele"))
    ax.plot(h24, BYHOUR["arx728"], color=PAL["HU"], marker="o", ms=3, label=T("one ARX(728) per hour", "cîte un ARX(728) pe oră"))
    ax.set_xticks(range(0, 24, 2))
    ax.set_xlabel(T("hour h (CET)", "ora h (CET)"))
    ax.set_ylabel("MAE,\nEUR/MWh")
    legend_bottom(fig, ncol=3)
    out(fig, lang, "per_hour_single", bottom=0.16)
    # 7 VST
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0), gridspec_kw={"width_ratios": [1, 1.25]})
    m_last, s_last = mad_scale(P_[IDX[END] - 735:IDX[END]])
    pg = np.linspace(-150, 650, 400)
    axs[0].plot(pg, (pg - m_last) / s_last, color="#9a9a9a", ls="--", label=T("z-score (no transform)", "standardizare (fără transformare)"))
    axs[0].plot(pg, np.arcsinh((pg - m_last) / s_last), color=PAL["RO"], label="asinh")
    axs[0].set_xlabel(T("price, EUR/MWh", "preț, EUR/MWh"))
    axs[0].set_ylabel(T("model\nscale", "scara\nmodelului"))
    xm = [pd.Timestamp(str(mm)) for mm in MONTHS_T]
    axs[1].plot(xm, BYMONTH["arx728_raw"], color="#9a9a9a", ls="--", marker="s", ms=3, label=T("ARX(728) on raw prices", "ARX(728) pe prețuri netransformate"))
    axs[1].plot(xm, BYMONTH["arx728"], color=PAL["RO"], marker="o", ms=3, label=T("ARX(728) on asinh prices", "ARX(728) pe prețuri asinh"))
    axs[1].set_ylabel("MAE,\nEUR/MWh")
    mfmt(axs[1], lang, 2)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "vst", bottom=0.26, also_x=[axs[0]])
    # 8 LEAR selection heatmap
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    im = ax.imshow(SEL * 100, aspect="auto", cmap="Blues", vmin=0, vmax=100)
    ax.set_yticks(range(len(GLAB[lang])))
    ax.set_yticklabels(GLAB[lang], fontsize=10)
    ax.set_xticks(range(0, 24, 2))
    ax.set_xlabel(T("hour h (CET)", "ora h (CET)"))
    cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label(T("% of regressors kept", "regresori păstrați, %"), fontsize=10)
    ax.spines[:].set_visible(False)
    ax._keep_y = True
    out(fig, lang, "lear_sel", bottom=0.02)
    # 9 calibration windows
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0), sharey=True, gridspec_kw={"width_ratios": [7, 4]})
    ka = [f"arx{T_}" for T_ in ARX_W] + ["aw_arx"]
    axs[0].bar(range(7), [ACC[k]["mae"] for k in ka], color=[PAL["HU"]] * 6 + [PAL["DE_LU"]], width=0.7)
    axs[0].set_xticks(range(7))
    axs[0].set_xticklabels([str(T_) for T_ in ARX_W] + ["AW"])
    axs[0].set_title("ARX", fontsize=10)
    kl = [f"lear{T_}" for T_ in LEAR_W] + ["aw_lear"]
    axs[1].bar(range(4), [ACC[k]["mae"] for k in kl], color=[PAL["RO"]] * 3 + [PAL["DE_LU"]], width=0.7)
    axs[1].set_xticks(range(4))
    axs[1].set_xticklabels([str(T_) for T_ in LEAR_W] + ["AW"])
    axs[1].set_title("LEAR", fontsize=10)
    for ax in axs:
        ax.axhline(ACC["naive"]["mae"], color="#9a9a9a", ls=":", lw=1.2)
    axs[0].plot([], [], color="#9a9a9a", ls=":", label=T("naive benchmark", "modelul naiv de referință"))
    axs[0].add_patch(plt.Rectangle((0, 0), 0, 0, color=PAL["DE_LU"], label=T("average across windows (AW)", "media prognozelor pe ferestre (AW)")))
    axs[0].set_ylabel("MAE,\nEUR/MWh")
    axs[0].set_ylim(0, ACC["naive"]["mae"] * 1.12)
    fig.text(0.5, 0.17, T("calibration window T (days)", "fereastra de calibrare T (zile)"), ha="center", fontsize=10)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "windows", bottom=0.22)
    # 10 ML by hour
    fig, ax = plt.subplots(figsize=(6.4, 1.9))
    for k, ls in [("aw_lear", "-"), ("gbm", "--"), ("mlp", "-."), ("ens_all", "-")]:
        ax.plot(h24, BYHOUR[k], color=COL[k], ls=ls, marker="o", ms=3, lw=1.6 if k == "ens_all" else 1.2, label=L(k))
    ax.set_xticks(range(0, 24, 2))
    ax.set_xlabel(T("hour h (CET)", "ora h (CET)"))
    ax.set_ylabel("MAE,\nEUR/MWh")
    legend_bottom(fig, ncol=4)
    out(fig, lang, "ml_hour", bottom=0.16)
    # 11 QRA week
    pw = slice(POS[PW] - N_BURN, POS[PW] - N_BURN + 7)
    xt = pd.date_range(PW, periods=168, freq="h")
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    qw = QRA[pw].reshape(168, 99)
    ax.fill_between(xt, qw[:, 4], qw[:, 94], color=PAL["RO"], alpha=0.18, lw=0, label=T("90% interval", "interval 90%"))
    ax.fill_between(xt, qw[:, 24], qw[:, 74], color=PAL["RO"], alpha=0.38, lw=0, label=T("50% interval", "interval 50%"))
    ax.plot(xt, qw[:, 49], color=PAL["RO"], lw=1.0, label=T("QRA median", "mediana QRA"))
    ax.plot(xt, A[pw].ravel(), color="#222222", lw=1.0, label=T("actual price", "prețul realizat"))
    ax.set_ylabel("EUR/MWh")
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{DAYN[lang][mdates.num2date(v).weekday()]} {mdates.num2date(v).day}"))
    legend_bottom(fig, ncol=4)
    out(fig, lang, "qra_week", bottom=0.17)
    # 12 reliability (calibration) of the quantiles
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    for k, c, lab in [("qra", PAL["RO"], "QRA"), ("cp", PAL["DE_LU"], T("conformal (CP)", "predicție conformală (CP)")),
                      ("hs", PAL["HU"], T("historical simulation (HS)", "simulare istorică (HS)"))]:
        ax.plot(TAUS * 100, (np.array(PROB[k]["rel"]) - TAUS) * 100, color=c, label=lab)
    ax.axhline(0, color="#222222", lw=0.7)
    ax.set_xlabel(T("quantile level $\\tau$, %", "nivelul cuantilei $\\tau$, %"))
    ax.set_ylabel(T("coverage\nerror, pp", "eroarea de\nacoperire, pp"))
    legend_bottom(fig, ncol=3)
    out(fig, lang, "prob_rel", bottom=0.15)
    # 13 cointegration, daily RO vs HU
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.5), sharex=True, gridspec_kw={"height_ratios": [1.2, 1]})
    axs[0].plot(DLY.index, DLY["HU"], color=PAL["HU"], lw=0.7, label=T("Hungary (HUPX)", "Ungaria (HUPX)"))
    axs[0].plot(DLY.index, DLY["RO"], color=PAL["RO"], lw=0.7, label=T("Romania (OPCOM PZU)", "România (OPCOM PZU)"))
    axs[1].plot(DLY.index, DLY["RO"] - DLY["HU"], color=PAL["c8"], lw=0.6, label=T("spread RO - HU", "diferența RO - HU"))
    axs[1].axhline(0, color="#222222", lw=0.5)
    for ax in axs:
        ax.set_ylabel("EUR/MWh")
    axs[1].set_xlim(DLY.index[0], DLY.index[-1])
    axs[1].xaxis.set_major_locator(mdates.YearLocator())
    axs[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, ncol=3)
    out(fig, lang, "coint_daily", bottom=0.15)
    # 14 cointegration, monthly price vs gas, and hydro
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1), gridspec_kw={"width_ratios": [1.5, 1]})
    axs[0].plot(MD.index, MD["price"], color=PAL["RO"], lw=1.0, label=T("Romania, monthly price", "România, prețul lunar"))
    axs[0].plot(MD.index, lr_.fittedvalues, color=PAL["DE_LU"], lw=1.0, ls="--", label=T("long-run level from TTF gas", "nivel de echilibru (gaze TTF)"))
    axs[0].set_ylabel("EUR/MWh")
    axs[0].xaxis.set_major_locator(mdates.YearLocator(3))
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axs[1].scatter(MD["hydro_ds"], u_, s=8, color=PAL["RO"], alpha=0.7, label=T("one month", "o lună"))
    bb = np.polyfit(MD["hydro_ds"], u_, 1)
    xx = np.linspace(MD["hydro_ds"].min(), MD["hydro_ds"].max(), 10)
    axs[1].plot(xx, np.polyval(bb, xx), color="#222222", lw=1.0)
    axs[1].axhline(0, color="#222222", lw=0.4)
    axs[1].set_xlabel(T("hydro vs its monthly mean, TWh", "hidro față de media lunii, TWh"), fontsize=9.5)
    axs[1].set_ylabel(T("price minus\nlong-run level", "abaterea de la\nechilibru"), fontsize=9.5)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "coint_monthly", bottom=0.13, also_x=[axs[1]])
    # 15 monthly MAE over the test year
    fig, ax = plt.subplots(figsize=(6.4, 1.9))
    for k, ls, mk in [("naive", ":", "o"), ("aw_arx", "--", "s"), ("aw_lear", "-", "o"), ("ens_all", "-", "D")]:
        ax.plot(xm, BYMONTH[k], color=COL[k], ls=ls, marker=mk, ms=3.5, label=L(k))
    ax.set_ylabel("MAE,\nEUR/MWh")
    mfmt(ax, lang, 1)
    legend_bottom(fig, ncol=4)
    out(fig, lang, "monthly_mae", bottom=0.2)
    # 16 stress week
    xs_ = pd.date_range(SW, periods=168, freq="h")
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    ax.plot(xs_, A[sw].ravel(), color="#222222", lw=1.3, label=T("actual price", "prețul realizat"))
    for k, ls in [("naive", ":"), ("aw_lear", "-"), ("ens_all", "--")]:
        ax.plot(xs_, M[k][sw].ravel(), color=COL[k], ls=ls, lw=1.0, label=L(k))
    ax.set_ylabel("EUR/MWh")
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{DAYN[lang][mdates.num2date(v).weekday()]} {mdates.num2date(v).day}"))
    legend_bottom(fig, ncol=4)
    out(fig, lang, "stress_week", bottom=0.17)
    # 17 15-minute MTU
    qk = QDAYS.index(QDAY)
    xq = np.arange(96) / 4
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    ax.step(xq, Q[qk], where="post", color="#222222", lw=1.1, label=T("actual 15-min price", "preț realizat, 15 min"))
    ax.step(xq, flat[qk], where="post", color=PAL["RO"], lw=1.0, ls="--", label=T("hourly AW-LEAR, flat", "AW-LEAR orar, constant"))
    ax.step(xq, shaped[qk], where="post", color=PAL["DE_LU"], lw=1.0, label=T("+ intra-hour shape", "+ profil intraorar"))
    ax.set_xticks(range(0, 25, 2))
    ax.set_xlabel(T("hour (CET)", "ora (CET)"))
    ax.set_ylabel("EUR/MWh")
    legend_bottom(fig, ncol=3)
    out(fig, lang, "mtu15", bottom=0.16)
    # 18 battery and flexible buyer: value of the forecast
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1))
    kb = ["perfect", "ens_all", "aw_lear", "gbm", "aw_arx", "naive"]
    axs[0].barh(range(len(kb)), [BAT[k].sum() / 1000 for k in kb], color=[COL[k] for k in kb], height=0.65)
    axs[0].set_yticks(range(len(kb)))
    axs[0].set_yticklabels([L(k) for k in kb], fontsize=10)
    axs[0].invert_yaxis()
    axs[0].set_xlabel(T("battery profit,\nthousand EUR per MW", "profitul bateriei,\nmii EUR pe MW"), fontsize=10)
    kf = ["perfect", "ens_all", "aw_lear", "gbm", "aw_arx", "naive"]
    vf = [FLX[k].sum() / (4 * len(FLX[k])) for k in kf] + [FLX_BASE.sum() / (4 * len(FLX_BASE))]
    axs[1].barh(range(len(vf)), vf, color=[COL[k] for k in kf] + ["#5b4a3a"], height=0.65)
    axs[1].set_yticks(range(len(vf)))
    axs[1].set_yticklabels([L(k) for k in kf] + [T("fixed 8-12 h", "bloc fix 8-12")], fontsize=10)
    axs[1].invert_yaxis()
    axs[1].set_xlabel(T("flexible buyer:\nmean price paid, EUR/MWh", "cumpărătorul flexibil:\npreț mediu, EUR/MWh"), fontsize=10)
    for ax in axs:
        ax._keep_y = True
    out(fig, lang, "battery", bottom=0.02, also_x=list(axs))

ped, prd = f"{d(TEST0)} to {d(END)}", f"{d(TEST0)} - {d(END)}"
chart("split_timeline", "ec", f"daily base price, {d(START)} to {d(END)}, CET delivery days", f"preț zilnic de bază, {d(START)} - {d(END)}, zile de livrare CET")
chart("horizon_naive", "ec", f"test year {ped}, hourly", f"anul de test {prd}, date orare")
chart("mape_fail", "ecl", f"test year {ped}, {N['test']['n_hours']} hours", f"anul de test {prd}, {N['test']['n_hours']} de ore")
chart("dm_matrix", "ecf", f"test year {ped}, {len(TDAYS)} days; one-sided p-values", f"anul de test {prd}, {len(TDAYS)} de zile; valori p unilaterale")
chart("arx_coef", "ecl", f"ARX(728), mean over the {len(TDAYS)} daily fits of the test year", f"ARX(728), media celor {len(TDAYS)} de estimări zilnice din anul de test")
chart("per_hour_single", "ecl", f"test year {ped}", f"anul de test {prd}")
chart("vst", "ecl", f"left, median and scale of the last window; right, test year {ped}", f"stînga, mediana și scala din ultima fereastră; dreapta, anul de test {prd}")
chart("lear_sel", "ecl", f"LEAR(728), {len(TDAYS)} daily fits of the test year", f"LEAR(728), {len(TDAYS)} de estimări zilnice din anul de test")
chart("windows", "ecl", f"test year {ped}", f"anul de test {prd}")
chart("ml_hour", "ecf", f"test year {ped}; ML refitted monthly", f"anul de test {prd}; modelele ML reestimate lunar")
chart("qra_week", "ecl", f"week {d(PW)} to {d(PW + pd.Timedelta(days=6))}, hourly", f"săptămîna {d(PW)} - {d(PW + pd.Timedelta(days=6))}, date orare")
chart("prob_rel", "ecl", f"test year {ped}, 99 quantiles", f"anul de test {prd}, 99 de cuantile")
chart("coint_daily", "hu", f"daily base prices, {co['start']} to {co['end']}", f"prețuri zilnice de bază, {co['start']} - {co['end']}")
chart("coint_monthly", "m", f"monthly, {cm['start']} to {cm['end']}", f"lunar, {cm['start']} - {cm['end']}")
chart("monthly_mae", "ecf", f"test year {ped}", f"anul de test {prd}")
chart("stress_week", "ecf", f"week {d(SW)} to {d(SW + pd.Timedelta(days=6))}, hourly", f"săptămîna {d(SW)} - {d(SW + pd.Timedelta(days=6))}, date orare")
chart("mtu15", "q", f"{d(QDAY)}, 96 quarter-hours (CET)", f"{d(QDAY)}, 96 de sferturi de oră (CET)")
chart("battery", "ecf", f"test year {ped}; 1 MW / 2 MWh, round-trip efficiency 90\\%", f"anul de test {prd}; 1 MW / 2 MWh, randament 90\\%")

with open(os.path.join(HERE, "L2_numbers.json"), "w") as fh:
    json.dump(N, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("wrote L2_numbers.json and", len(N["charts"]), "charts x 2 languages")
