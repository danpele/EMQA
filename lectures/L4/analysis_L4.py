"""
analysis_L4.py -- Lecture 4 "Risk management for energy prices: VaR, ES, backtesting, limits and collateral" (EMQA)
=================================================================================================================
Reads the real series in repo/data/clean (see data/SOURCES.md), computes every number shown on the slides and writes
    lectures/L4/L4_numbers.json        all results (the deck builder reads ONLY this file)
    lectures/L4/charts/en/*.pdf        figures with English labels
    lectures/L4/charts/ro/*.pdf        the same figures with Romanian labels
    lectures/L4/cache/engine.pkl       the rolling VaR/ES forecasts (recomputed when the data or the engine change)
Run:  python3 lectures/L4/analysis_L4.py            (add --fresh to ignore the cache)

Design
  * Risk factor: the daily change of the day-ahead base price, X_t = P_t - P_{t-1} (EUR/MWh), on the full calendar
    (a change next to a missing day stays missing; no multi-day jumps). Prices can be negative, so no log returns.
  * Position: a supplier that buys a flat block on the day-ahead market and budgets it at yesterday's price;
    loss per MWh = X_t (a price rise is a loss). 100 MW flat = 2,400 MWh per day.
  * Forecast for day t uses prices up to t-1 only (known at 12:00 CET on t-1, gate closure).
  * Methods: historical simulation (HS, 365 days), normal and Student-t (365 days), filtered historical simulation (FHS:
    weekday mean + GARCH(1,1) volatility, refitted every 21 days on 730 days, empirical standardised residuals) and
    conditional extreme value theory (EVT: same filter, generalised Pareto tail above the 90% residual quantile).
  * Backtest 2017-01-01 to the cut-off: Kupiec, Christoffersen, Basel traffic light (250 days), Acerbi-Szekely Z2 for ES
    with p-values simulated from each model's own predictive distribution.
  * Collateral: (a) initial margin of an ICE Brent futures lot as a 99% 2-day historical VaR (EMIR RTS 153/2013 Art. 24-28),
    roll days dropped; (b) OPCOM day-ahead guarantee sized by a quantile forecast of tomorrow's base price (quantile
    regression, then one-sided conformal widening).
  * Seeds fixed. There is no simulated data series; simulation is used only to obtain p-values of the ES test.
"""

import hashlib
import json
import os
import pickle
import sys
import warnings

import numpy as np
import pandas as pd
from arch import arch_model
from joblib import Parallel, delayed
from scipy import stats
from statsmodels.regression.quantile_regression import QuantReg

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import emqa_plot as ep  # noqa: E402
from emqa_plot import PAL, legend_bottom, save  # noqa: E402

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter, NullFormatter  # noqa: E402

warnings.filterwarnings("ignore")
ep.style()
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "data", "clean")
ENGINE_VERSION = "L4-engine-v2"
FRESH = "--fresh" in sys.argv
N = {"charts": {}}
SEED = 20261106
MON_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MON_RO = ["ian.", "feb.", "mar.", "apr.", "mai", "iun.", "iul.", "aug.", "sep.", "oct.", "nov.", "dec."]
METHODS = ["hs", "normal", "t", "fhs", "evt"]
LEVELS = (0.95, 0.975, 0.99)
W_HS = 365          # window of HS, normal, Student-t (days of available changes)
W_G = 730           # estimation window of the GARCH filter
REFIT = 21          # refit every 21 days
U_EVT = 0.90        # EVT threshold = 90% quantile of the standardised residuals
M_SIM = 2000        # simulated paths for the Z2 p-values
Q_MW = 100          # supplier position, MW flat
BUDGET = 250_000    # daily VaR budget of the trading desk, EUR (a teaching assumption)


def d(ts):
    return pd.Timestamp(ts).strftime("%Y-%m-%d")


def fl(x, k=4):
    if x is None:
        return None
    x = float(x)
    return None if np.isnan(x) else round(x, k)


# =============================================================================
# 0. Load data and cut-off (last complete month, as in Lectures 1-2)
# =============================================================================
PD = ep.prices_daily()
_raw_last = PD["RO"].dropna().index.max()
END = pd.Timestamp(((_raw_last + pd.Timedelta(days=1)).to_period("M").to_timestamp() - pd.Timedelta(days=1)).date())
START = pd.Timestamp("2015-01-01")
T0 = pd.Timestamp("2017-01-01")                     # first backtest day
CAL = pd.date_range(START, END, freq="D")
P = PD[["RO", "DE_LU", "HU"]].reindex(CAL)            # missing CET days stay missing
X = P.diff()                                          # full calendar: a change next to a gap is NaN
N["cutoff"] = {"end": d(END), "download": "2026-11-04", "year": END.year}
N["data"] = {"start": d(START), "end": d(END), "n_days": len(CAL), "t0": d(T0),
             "n_missing_ro": int(P["RO"].isna().sum()), "n_x_ro": int(X["RO"].notna().sum()),
             "n_x_de": int(X["DE_LU"].notna().sum()), "n_test": int(((CAL >= T0)).sum()),
             "n_test_valid_ro": int(X["RO"][T0:].notna().sum())}


def dist_facts(x, cal_end=None):
    """Moments and tail counts of a series of daily changes."""
    x = x.dropna()
    m, s = x.mean(), x.std()
    z3 = m + 3 * s
    zmax = (x.max() - m) / s
    lp = stats.norm.logsf(zmax) / np.log(10)                    # log10 P(Z > zmax)
    return {"n": int(len(x)), "mean": fl(m, 3), "sd": fl(s, 3), "skew": fl(stats.skew(x), 3),
            "exkurt": fl(stats.kurtosis(x), 2), "q99": fl(x.quantile(0.99), 2), "q01": fl(x.quantile(0.01), 2),
            "q99_normal": fl(m + stats.norm.ppf(0.99) * s, 2),
            "n_3sd_up": int((x > z3).sum()), "n_3sd_down": int((x < m - 3 * s).sum()),
            "exp_3sd": fl(len(x) * stats.norm.sf(3), 2), "max": fl(x.max(), 2), "max_date": d(x.idxmax()),
            "min": fl(x.min(), 2), "min_date": d(x.idxmin()), "max_z": fl(zmax, 1),
            "max_logyears": int(np.floor(-lp - np.log10(365.25)))}


# =============================================================================
# 1. Distribution of daily price changes; the normal curve and crisis days
# =============================================================================
N["dist"] = {z: dist_facts(X[z][START:END]) for z in ["RO", "DE_LU"]}
# a "budget" built on the normal curve with 2015-2020 data, applied to 2021-2022 and 2023-2026
pre = X["RO"]["2015-01-01":"2020-12-31"].dropna()
m0, s0 = pre.mean(), pre.std()
lim99 = m0 + stats.norm.ppf(0.99) * s0
nb = {"m": fl(m0, 2), "s": fl(s0, 2), "lim99": fl(lim99, 2), "n_pre": int(len(pre)),
      "n_pre_exc": int((pre > lim99).sum()), "exp_pre": fl(0.01 * len(pre), 1)}
for lab, a, b in [("crisis", "2021-01-01", "2022-12-31"), ("after", "2023-01-01", d(END))]:
    xx = X["RO"][a:b].dropna()
    nb[f"n_{lab}"] = int(len(xx))
    nb[f"exc_{lab}"] = int((xx > lim99).sum())
    nb[f"exp_{lab}"] = fl(0.01 * len(xx), 1)
    nb[f"ratio_{lab}"] = fl((xx > lim99).sum() / (0.01 * len(xx)), 1)
N["normlim"] = nb

# last 365 days: empirical VaR/ES illustration
last = X["RO"][END - pd.Timedelta(days=364):END].dropna()
v99 = np.quantile(last, 0.99)
v975 = np.quantile(last, 0.975)
N["lastyear"] = {"start": d(END - pd.Timedelta(days=364)), "n": int(len(last)), "var99": fl(v99, 2), "var95": fl(np.quantile(last, 0.95), 2),
                 "var975": fl(v975, 2), "es975": fl(last[last >= v975].mean(), 2), "es99": fl(last[last >= v99].mean(), 2),
                 "n_ge_var99": int((last >= v99).sum()), "n_ge_var975": int((last >= v975).sum()),
                 "var99_eur": fl(v99 * 24 * Q_MW, 0), "es975_eur": fl(last[last >= v975].mean() * 24 * Q_MW, 0)}
# subadditivity on real data: supplier buying 100 MW in RO and 100 MW in DE-LU (last year), VaR and ES
xd = X["DE_LU"][END - pd.Timedelta(days=364):END].reindex(last.index)
both = (last + xd).dropna()
ro_, de_ = last.reindex(both.index), xd.reindex(both.index)


def es_emp(x, a):
    q = np.quantile(x, a)
    return x[x >= q].mean()


N["subadd"] = {"var_ro": fl(np.quantile(ro_, 0.99), 2), "var_de": fl(np.quantile(de_, 0.99), 2),
               "var_sum": fl(np.quantile(both, 0.99), 2), "es_ro": fl(es_emp(ro_, 0.975), 2), "es_de": fl(es_emp(de_, 0.975), 2),
               "es_sum": fl(es_emp(both, 0.975), 2), "corr": fl(np.corrcoef(ro_, de_)[0, 1], 2)}


# =============================================================================
# 2. Rolling VaR / ES engine (forecast for day t uses changes up to t-1)
# =============================================================================
def var_es_normal(w, a):
    m, s = np.mean(w), np.std(w, ddof=1)
    z = stats.norm.ppf(a)
    return m + s * z, m + s * stats.norm.pdf(z) / (1 - a)


def fit_t(w):
    nu, loc, sc = stats.t.fit(w)
    if nu < 2.2:
        nu = 2.2
        _, loc, sc = stats.t.fit(w, f0=nu)
    return nu, loc, sc


def var_es_t(par, a):
    nu, loc, sc = par
    q = stats.t.ppf(a, nu)
    es = stats.t.pdf(q, nu) / (1 - a) * (nu + q ** 2) / (nu - 1)
    return loc + sc * q, loc + sc * es


def var_es_hs(w, a):
    q = np.quantile(w, a)
    return q, w[w >= q].mean()


def gpd_tail(z, u_q=U_EVT):
    """Peaks over threshold on standardised residuals: threshold u, GPD shape xi and scale beta (MLE, location 0)."""
    u = np.quantile(z, u_q)
    exc = z[z > u] - u
    xi, _, beta = stats.genpareto.fit(exc, floc=0)
    return u, xi, beta, len(exc), len(z)


def var_es_evt(tail, a):
    u, xi, beta, nu_, n = tail
    r = (n / nu_) * (1 - a)
    if abs(xi) < 1e-6:
        v = u - beta * np.log(r)
        return v, v + beta
    v = u + beta / xi * (r ** (-xi) - 1)
    return v, (v + beta - xi * u) / (1 - xi)


def garch_filter(e):
    """GARCH(1,1) with zero mean on the de-meaned changes (QMLE, normal); returns parameters and in-sample sigma."""
    res = arch_model(e, mean="Zero", vol="GARCH", p=1, q=1, dist="normal", rescale=False).fit(disp="off")
    om, al, be = res.params["omega"], res.params["alpha[1]"], res.params["beta[1]"]
    return float(om), float(al), float(be), np.asarray(res.conditional_volatility)


def run_zone(x, zone, seed=SEED):
    """Rolling one-day-ahead VaR/ES of a buyer's loss X_t for every day from T0 to END, five methods."""
    rng = np.random.default_rng(seed)
    days = pd.date_range(T0, END, freq="D")
    xs = x.copy()
    out = {m: {a: {"var": np.full(len(days), np.nan), "es": np.full(len(days), np.nan)} for a in LEVELS} for m in METHODS}
    sig = np.full(len(days), np.nan)
    mu_d = np.full(len(days), np.nan)
    z2c = {m: [] for m in METHODS}                   # per-day simulated Z2 contributions (M_SIM) and observed one
    z2o = {m: np.full(len(days), np.nan) for m in METHODS}
    tailinfo = []
    a_es = 0.975
    state = None
    for k, t in enumerate(days):
        hist = xs[:t - pd.Timedelta(days=1)].dropna()
        w = hist.values[-W_HS:]
        # ---- unconditional methods
        tpar = fit_t(w)
        for a in LEVELS:
            out["hs"][a]["var"][k], out["hs"][a]["es"][k] = var_es_hs(w, a)
            out["normal"][a]["var"][k], out["normal"][a]["es"][k] = var_es_normal(w, a)
            out["t"][a]["var"][k], out["t"][a]["es"][k] = var_es_t(tpar, a)
        # ---- filter: refit every REFIT days
        if k % REFIT == 0:
            hw = hist[-W_G:]
            mdow = hw.groupby(hw.index.dayofweek).mean()
            e = (hw - mdow.reindex(hw.index.dayofweek).values).values
            om, al, be, sw = garch_filter(e)
            z = e / sw
            state = {"om": om, "al": al, "be": be, "mdow": mdow, "z": np.sort(z), "tail": gpd_tail(z),
                     "s2": sw[-1] ** 2, "e": e[-1], "tlast": hw.index[-1]}
            tailinfo.append((d(t), state["tail"][1], state["tail"][2]))
        # advance sigma from the last day used to t-1, then one step to t
        while state["tlast"] < t - pd.Timedelta(days=1):
            nxt = state["tlast"] + pd.Timedelta(days=1)
            state["s2"] = state["om"] + state["al"] * state["e"] ** 2 + state["be"] * state["s2"]
            xv = xs.get(nxt, np.nan)
            state["e"] = (xv - state["mdow"][nxt.dayofweek]) if not np.isnan(xv) else 0.0
            if np.isnan(xv):          # missing day: expected shock (sigma^2 itself) instead of e^2
                state["e"] = np.sqrt(state["s2"])
            state["tlast"] = nxt
        s_t = np.sqrt(state["om"] + state["al"] * state["e"] ** 2 + state["be"] * state["s2"])
        m_t = state["mdow"][t.dayofweek]
        sig[k], mu_d[k] = s_t, m_t
        z = state["z"]
        for a in LEVELS:
            qz = np.quantile(z, a)
            out["fhs"][a]["var"][k] = m_t + s_t * qz
            out["fhs"][a]["es"][k] = m_t + s_t * z[z >= qz].mean()
            ve, ee = var_es_evt(state["tail"], a)
            out["evt"][a]["var"][k], out["evt"][a]["es"][k] = m_t + s_t * ve, m_t + s_t * ee
        # ---- Z2 contributions: simulated from each model's own predictive distribution, and observed
        xt = xs.get(t, np.nan)
        u, xi, beta, nu_, n_ = state["tail"]
        sims = {"hs": rng.choice(w, M_SIM), "normal": np.mean(w) + np.std(w, ddof=1) * rng.standard_normal(M_SIM),
                "t": tpar[1] + tpar[2] * rng.standard_t(tpar[0], M_SIM),
                "fhs": m_t + s_t * rng.choice(z, M_SIM)}
        zb = rng.choice(z[z <= u], M_SIM)
        up = rng.random(M_SIM) < nu_ / n_
        zb[up] = u + stats.genpareto.rvs(xi, scale=beta, size=up.sum(), random_state=rng)
        sims["evt"] = m_t + s_t * zb
        for mth in METHODS:
            v, es = out[mth][a_es]["var"][k], out[mth][a_es]["es"][k]
            ls = sims[mth]
            z2c[mth].append(np.where(ls > v, ls, 0.0) / es)
            if not np.isnan(xt):
                z2o[mth][k] = (xt if xt > v else 0.0) / es
    return {"days": days, "out": out, "sig": sig, "mu": mu_d, "z2c": {m: np.array(v, dtype=np.float32) for m, v in z2c.items()},
            "z2o": z2o, "tail": tailinfo, "zone": zone}


def data_hash():
    h = hashlib.md5()
    h.update(ENGINE_VERSION.encode())
    h.update(pd.util.hash_pandas_object(X[["RO", "DE_LU"]].fillna(-9999)).values.tobytes())
    return h.hexdigest()


os.makedirs(os.path.join(HERE, "cache"), exist_ok=True)
CACHE = os.path.join(HERE, "cache", "engine.pkl")
H_ = data_hash()
ENG = None
if not FRESH and os.path.exists(CACHE):
    with open(CACHE, "rb") as fh:
        c_ = pickle.load(fh)
    if c_.get("hash") == H_:
        ENG = c_["eng"]
if ENG is None:
    print("running the VaR/ES engine (two zones in parallel; a few minutes)...")
    res = Parallel(n_jobs=2)(delayed(run_zone)(X[z], z, SEED + i) for i, z in enumerate(["RO", "DE_LU"]))
    ENG = {r["zone"]: r for r in res}
    with open(CACHE, "wb") as fh:
        pickle.dump({"hash": H_, "eng": ENG}, fh)
DAYS = ENG["RO"]["days"]


# =============================================================================
# 3. Backtests: Kupiec, Christoffersen, Basel traffic light, Acerbi-Szekely Z2
# =============================================================================
def kupiec(hits, p0):
    n, x = len(hits), int(np.sum(hits))
    ph = x / n
    ll0 = (n - x) * np.log(1 - p0) + x * np.log(p0)
    ll1 = (n - x) * np.log(1 - ph) + (x * np.log(ph) if x > 0 else 0.0) if 0 < ph < 1 else 0.0
    lr = -2 * (ll0 - ll1)
    return lr, float(stats.chi2.sf(lr, 1))


def christoffersen(hits):
    h = np.asarray(hits, int)
    a, b = h[:-1], h[1:]
    n00, n01 = int(np.sum((a == 0) & (b == 0))), int(np.sum((a == 0) & (b == 1)))
    n10, n11 = int(np.sum((a == 1) & (b == 0))), int(np.sum((a == 1) & (b == 1)))
    p01 = n01 / max(n00 + n01, 1)
    p11 = n11 / max(n10 + n11, 1)
    p = (n01 + n11) / (n00 + n01 + n10 + n11)

    def ll(q, k0, k1):
        return (k0 * np.log(1 - q) if k0 else 0.0) + (k1 * np.log(q) if k1 else 0.0)
    lr = -2 * (ll(p, n00 + n10, n01 + n11) - ll(p01, n00, n01) - ll(p11, n10, n11))
    return lr, float(stats.chi2.sf(lr, 1)), {"n00": n00, "n01": n01, "n10": n10, "n11": n11, "p01": p01, "p11": p11}


def zone_of(c):
    return "green" if c <= 4 else ("yellow" if c <= 9 else "red")


PERIODS = [("calm", "2017-01-01", "2020-12-31"), ("crisis", "2021-01-01", "2022-12-31"), ("after", "2023-01-01", d(END))]
BT = {}
HITS = {}
for zone in ["RO", "DE_LU"]:
    E = ENG[zone]
    x = X[zone].reindex(DAYS).values
    ok = ~np.isnan(x)
    BT[zone] = {}
    for m in METHODS:
        BT[zone][m] = {}
        for a in (0.95, 0.99):
            v = E["out"][m][a]["var"]
            hits = (x[ok] > v[ok]).astype(int)
            HITS[(zone, m, a)] = pd.Series(np.where(ok, (x > v).astype(float), np.nan), index=DAYS)
            lr_uc, p_uc = kupiec(hits, 1 - a)
            lr_ind, p_ind, _ = christoffersen(hits)
            r = {"n": int(ok.sum()), "x": int(hits.sum()), "exp": fl((1 - a) * ok.sum(), 1), "rate": fl(100 * hits.mean(), 2),
                 "lr_uc": fl(lr_uc, 2), "p_uc": fl(p_uc, 4), "lr_ind": fl(lr_ind, 2), "p_ind": fl(p_ind, 4),
                 "lr_cc": fl(lr_uc + lr_ind, 2), "p_cc": fl(stats.chi2.sf(lr_uc + lr_ind, 2), 4),
                 "mean_var": fl(np.nanmean(v), 2)}
            for lab, a_, b_ in PERIODS:
                hs_ = HITS[(zone, m, a)][a_:b_].dropna()
                r[f"rate_{lab}"] = fl(100 * hs_.mean(), 2)
                r[f"x_{lab}"] = int(hs_.sum())
            if a == 0.99:
                c250 = HITS[(zone, m, a)].fillna(0).rolling(250).sum().iloc[249:]
                zs = c250.map(zone_of)
                r["share_green"] = fl(100 * (zs == "green").mean(), 1)
                r["share_yellow"] = fl(100 * (zs == "yellow").mean(), 1)
                r["share_red"] = fl(100 * (zs == "red").mean(), 1)
                r["max250"] = int(c250.max())
                r["max250_date"] = d(c250.idxmax())
            BT[zone][m]["a95" if a == 0.95 else "a99"] = r
        # Z2 (ES 97.5%): full period and sub-periods; p-value = share of simulated Z2 >= observed
        BT[zone][m]["z2"] = {}
        for lab, a_, b_ in [("all", d(T0), d(END))] + PERIODS:
            sel = (DAYS >= a_) & (DAYS <= b_) & ok
            T_ = sel.sum()
            obs = np.nansum(E["z2o"][m][sel]) / (T_ * 0.025) - 1
            sim = E["z2c"][m][sel].sum(0) / (T_ * 0.025) - 1
            BT[zone][m]["z2"][lab] = {"z2": fl(obs, 3), "p": fl(np.mean(sim >= obs), 4), "T": int(T_)}
        BT[zone][m]["es_mean"] = fl(np.nanmean(E["out"][m][0.975]["es"]), 2)
N["bt"] = BT
N["levels_note"] = {"basel_green": 4, "basel_yellow": 9}
# Basel traffic light: probabilities of the zones for a correct 99% model over 250 days (binomial)
N["basel"] = {"p_green": fl(100 * stats.binom.cdf(4, 250, 0.01), 2), "p_yellow": fl(100 * (stats.binom.cdf(9, 250, 0.01) - stats.binom.cdf(4, 250, 0.01)), 2),
              "p_red": fl(100 * stats.binom.sf(9, 250, 0.01), 3)}
# quiz: 7 exceedances in 250 days at 99%
N["quiz"] = {"k7_lr": fl(kupiec(np.r_[np.ones(7), np.zeros(243)], 0.01)[0], 2), "k7_p": fl(kupiec(np.r_[np.ones(7), np.zeros(243)], 0.01)[1], 3)}
# exceedances of the 99% VaR in the window of the var_paths chart
VP0, VP1 = "2021-07-01", "2023-06-30"
N["vp"] = {m: int(HITS[("RO", m, 0.99)][VP0:VP1].sum()) for m in METHODS}
N["vp"]["n"] = int(HITS[("RO", "hs", 0.99)][VP0:VP1].notna().sum())
N["vp"]["exp"] = fl(0.01 * N["vp"]["n"], 1)

# average of the forecasts made for the last month of the sample (a single day would mix in the weekday mean of FHS/EVT), RO
LM_ = (DAYS >= END.replace(day=1))
N["last"] = {m: {"var95": fl(np.mean(ENG["RO"]["out"][m][0.95]["var"][LM_]), 2), "var99": fl(np.mean(ENG["RO"]["out"][m][0.99]["var"][LM_]), 2),
                 "es975": fl(np.mean(ENG["RO"]["out"][m][0.975]["es"][LM_]), 2),
                 "var99_eur": fl(np.mean(ENG["RO"]["out"][m][0.99]["var"][LM_]) * 24 * Q_MW / 1000, 0),
                 "es975_eur": fl(np.mean(ENG["RO"]["out"][m][0.975]["es"][LM_]) * 24 * Q_MW / 1000, 0)} for m in METHODS}
N["last"]["month"] = END.strftime("%Y-%m")
N["last"]["n"] = int(LM_.sum())
# GARCH filter and EVT tail at the last refit
ti = ENG["RO"]["tail"]
N["evt"] = {"xi_last": fl(ti[-1][1], 3), "beta_last": fl(ti[-1][2], 3), "refit_last": ti[-1][0], "n_refits": len(ti),
            "xi_med": fl(np.median([q[1] for q in ti]), 3), "xi_min": fl(min(q[1] for q in ti), 3), "xi_max": fl(max(q[1] for q in ti), 3),
            "u_q": U_EVT, "share_xi_pos": fl(100 * np.mean([q[1] > 0 for q in ti]), 0)}
# unconditional GPD on raw changes (whole sample), for the tail chart
xr = X["RO"].dropna().values
u_raw = np.quantile(xr, 0.95)
xi_r, _, be_r = stats.genpareto.fit(xr[xr > u_raw] - u_raw, floc=0)
N["evt"].update({"u_raw": fl(u_raw, 2), "xi_raw": fl(xi_r, 3), "beta_raw": fl(be_r, 2), "n_exc_raw": int((xr > u_raw).sum()),
                 "tail_index": fl(1 / xi_r if xi_r > 0 else np.nan, 2)})
sig = pd.Series(ENG["RO"]["sig"], index=DAYS)
N["garch"] = {"sig_max": fl(sig.max(), 2), "sig_max_date": d(sig.idxmax()), "sig_min": fl(sig.min(), 2), "sig_min_date": d(sig.idxmin()),
              "sig_last": fl(sig.iloc[-1], 2)}

# =============================================================================
# 4. Horizon: square-root-of-time scaling vs empirical h-day quantiles
# =============================================================================
HOR = {}
for zone in ["RO", "DE_LU"]:
    p = P[zone]
    q1 = (p.shift(-1) - p).dropna().quantile(0.99)
    HOR[zone] = {h: float((p.shift(-h) - p).dropna().quantile(0.99) / q1) for h in range(1, 21)}
    v1 = (p.shift(-1) - p).var()
    HOR[zone + "_vr"] = {h: float((p.shift(-h) - p).var() / (h * v1)) for h in range(1, 21)}
N["horizon"] = {"ro10": fl(HOR["RO"][10], 2), "de10": fl(HOR["DE_LU"][10], 2), "sqrt10": fl(np.sqrt(10), 2),
                "ro5": fl(HOR["RO"][5], 2), "sqrt5": fl(np.sqrt(5), 2), "vr10_ro": fl(HOR["RO_vr"][10], 2),
                "vr10_de": fl(HOR["DE_LU_vr"][10], 2),
                "ac1_ro": fl(X["RO"].autocorr(1), 3), "ac7_ro": fl(X["RO"].autocorr(7), 3)}

# =============================================================================
# 5. Collateral (a): initial margin of an ICE Brent futures lot, 99% 2-day HS (EMIR RTS 153/2013)
# =============================================================================
F = ep.fuels_daily()["brent_usd_bbl"].dropna()
F = F[:END]
ym = F.index.to_period("M")
roll = pd.Series(np.r_[False, ym[1:] != ym[:-1]], index=F.index)     # first trading day of each month
r2 = F / F.shift(2) - 1
r2[(roll | roll.shift(1, fill_value=False))] = np.nan                  # a 2-day window that contains a roll is dropped
r1 = F.diff()
r1[roll] = np.nan
LOT = 1000
absr = r2.abs()
q1y = absr.rolling(250, min_periods=200).quantile(0.99)
qlong = absr.expanding(min_periods=250).quantile(0.99)
IM1 = LOT * F * q1y
IML = LOT * F * qlong
IMA = np.maximum(IM1, IML)
im = pd.DataFrame({"im1": IM1, "iml": IML, "ima": IMA, "F": F})["2016-01-01":]
fut2 = (F.shift(-2) - F).abs() * LOT                                    # loss over the next two trading days, either side
fut2[(roll.shift(-1, fill_value=False) | roll.shift(-2, fill_value=False))] = np.nan
cov = pd.DataFrame({"l": fut2, "im1": IM1, "ima": IMA}).dropna()["2016-01-01":]
pre_ = im["2021-06-01":"2022-02-23"]
war_ = im["2022-02-24":"2022-12-31"]
chg20 = (im["im1"] / im["im1"].shift(20) - 1)
N["brent"] = {"start": d(F.index[0]), "end": d(F.index[-1]), "n_roll": int(roll.sum()),
              "im1_min": fl(im["im1"].min(), 0), "im1_min_date": d(im["im1"].idxmin()),
              "im1_max": fl(im["im1"].max(), 0), "im1_max_date": d(im["im1"].idxmax()),
              "im1_prewar": fl(im["im1"]["2022-02-23":].iloc[0], 0), "im1_war_max": fl(war_["im1"].max(), 0),
              "im1_war_max_date": d(war_["im1"].idxmax()),
              "ratio_war": fl(war_["im1"].max() / im["im1"]["2022-02-23":].iloc[0], 2),
              "ima_prewar": fl(im["ima"]["2022-02-23":].iloc[0], 0), "ima_war_max": fl(war_["ima"].max(), 0),
              "ratio_war_apc": fl(war_["ima"].max() / im["ima"]["2022-02-23":].iloc[0], 2),
              "max20": fl(100 * chg20.max(), 0), "max20_date": d(chg20.idxmax()),
              "exc1": fl(100 * (cov["l"] > cov["im1"]).mean(), 2), "exca": fl(100 * (cov["l"] > cov["ima"]).mean(), 2),
              "n_cov": int(len(cov)), "im1_last": fl(im["im1"].iloc[-1], 0), "ima_last": fl(im["ima"].iloc[-1], 0),
              "F_last": fl(F.iloc[-1], 2), "F_max": fl(F["2022"].max(), 2), "F_max_date": d(F["2022"].idxmax())}
s26 = im["2026-01-01":"2026-06-30"]
pre26 = im["2026-02-27":].iloc[0]
N["brent"].update({"im1_pre26": fl(pre26["im1"], 0), "ima_pre26": fl(pre26["ima"], 0), "im1_max26": fl(s26["im1"].max(), 0),
                   "im1_max26_date": d(s26["im1"].idxmax()), "ima_max26": fl(s26["ima"].max(), 0),
                   "ratio26": fl(s26["im1"].max() / pre26["im1"], 2), "ratio26_apc": fl(s26["ima"].max() / pre26["ima"], 2),
                   "F_pre26": fl(F["2026-02-27"], 2), "F_max26": fl(F["2026-03-01":"2026-06-30"].max(), 2),
                   "F_max26_date": d(F["2026-03-01":"2026-06-30"].idxmax())})
vm = r1 * LOT * 100                                                      # variation margin of a seller of 100 lots: pays when price rises
N["brent"].update({"vm_max": fl(vm.max() / 1e6, 2), "vm_max_date": d(vm.idxmax()),
                   "vm10_max": fl(vm.rolling(10).sum().max() / 1e6, 1), "vm10_max_date": d(vm.rolling(10).sum().idxmax())})

# =============================================================================
# 6. Collateral (b): the OPCOM day-ahead guarantee sized by a quantile forecast of tomorrow's base price
# =============================================================================
TAUS = (0.95, 0.99)
PR = P["RO"]


def qr_forecast(t, taus=TAUS, w=365):
    """Quantile regression of P_t on P_{t-1}, P_{t-7} and weekday dummies, last w days before t."""
    idx = pd.date_range(t - pd.Timedelta(days=w), t - pd.Timedelta(days=1), freq="D")
    df = pd.DataFrame({"y": PR.reindex(idx), "p1": PR.shift(1).reindex(idx), "p7": PR.shift(7).reindex(idx)})
    for j in range(6):
        df[f"d{j}"] = (idx.dayofweek == j).astype(float)
    df = df.dropna()
    Xm = np.column_stack([np.ones(len(df)), df[["p1", "p7"] + [f"d{j}" for j in range(6)]].values])
    xt = np.r_[1.0, PR.get(t - pd.Timedelta(days=1), np.nan), PR.get(t - pd.Timedelta(days=7), np.nan),
               [(t.dayofweek == j) * 1.0 for j in range(6)]]
    out = {}
    warnings.filterwarnings("ignore")
    for tau in taus:
        b = QuantReg(df["y"].values, Xm).fit(q=tau, max_iter=5000).params
        out[tau] = float(xt @ b)
    return out


QCACHE = os.path.join(HERE, "cache", "qr.pkl")
QH = hashlib.md5((ENGINE_VERSION + "qr").encode() + pd.util.hash_pandas_object(PR.fillna(-9999)).values.tobytes()).hexdigest()
QRF = None
if not FRESH and os.path.exists(QCACHE):
    with open(QCACHE, "rb") as fh:
        c_ = pickle.load(fh)
    if c_.get("hash") == QH:
        QRF = c_["qr"]
if QRF is None:
    print("quantile regressions...")
    QD = pd.date_range("2016-01-01", END, freq="D")
    rr = Parallel(n_jobs=-1)(delayed(qr_forecast)(t) for t in QD)
    QRF = pd.DataFrame({tau: [r_[tau] for r_ in rr] for tau in TAUS}, index=QD)
    with open(QCACHE, "wb") as fh:
        pickle.dump({"hash": QH, "qr": QRF}, fh)

# one-sided conformal widening: add the tau-quantile of the last 365 out-of-sample residuals P_s - q_s (s < t)
CQ = {}
for tau in TAUS:
    res_ = PR.reindex(QRF.index) - QRF[tau]
    corr = res_.shift(1).rolling(365, min_periods=300).quantile(tau)
    CQ[tau] = QRF[tau] + corr
GUAR = {}
for tau in TAUS:
    a_ = tau
    fhs_q = PR.shift(1).reindex(DAYS) + pd.Series(ENG["RO"]["out"]["fhs"][a_]["var"], index=DAYS)
    df = pd.DataFrame({"p": PR.reindex(DAYS), "qr": QRF[tau].reindex(DAYS), "cqr": CQ[tau].reindex(DAYS), "fhs": fhs_q}).dropna()
    g = {}
    for k_ in ["qr", "cqr", "fhs"]:
        g[k_] = {"cov": fl(100 * (df["p"] <= df[k_]).mean(), 2)}
        for lab, a1, b1 in PERIODS:
            s_ = df[a1:b1]
            g[k_][f"cov_{lab}"] = fl(100 * (s_["p"] <= s_[k_]).mean(), 2)
            g[k_][f"miss_{lab}"] = int((s_["p"] > s_[k_]).sum())
            g[k_][f"g_{lab}"] = fl(s_[k_].mean() * 24 * Q_MW / 1e6, 3)
        g[k_]["g_mean"] = fl(df[k_].mean() * 24 * Q_MW / 1e6, 3)
        g[k_]["miss"] = int((df["p"] > df[k_]).sum())
        lr, pp = kupiec((df["p"] > df[k_]).astype(int).values, 1 - tau)
        g[k_]["kupiec_p"] = fl(pp, 4)
    g["n"] = int(len(df))
    g["extra_cost_pct"] = fl(100 * (df["cqr"].mean() / df["qr"].mean() - 1), 1)
    GUAR["a95" if tau == 0.95 else "a99"] = g
    if tau == 0.99:
        GDF = df
N["guar"] = GUAR

# position limit from a daily VaR budget: Q_max = budget / (24 * VaR99), FHS
v99 = pd.Series(ENG["RO"]["out"]["fhs"][0.99]["var"], index=DAYS)
qmax = BUDGET / (24 * v99)
N["limit"] = {"budget": BUDGET, "q_2019": fl(qmax["2019"].median(), 0), "v_2019": fl(v99["2019"].median(), 2),
              "q_min": fl(qmax.min(), 0), "q_min_date": d(qmax.idxmin()), "v_max": fl(v99.max(), 2),
              "q_last": fl(qmax.iloc[-1], 0), "v_last": fl(v99.iloc[-1], 2), "q_jun26": fl(qmax["2026-06"].median(), 0),
              "v_jun26": fl(v99["2026-06"].median(), 2)}

# =============================================================================
# 7. Positions: a supplier's monthly procurement cost and a producer's revenue
# =============================================================================
HP = ep.prices_hourly()["RO"]
HP.index = HP.index.tz_convert("UTC")
GL = ep.generation_ro_hourly()["load"]
GL.index = pd.to_datetime(GL.index, utc=True)
hl = pd.DataFrame({"p": HP, "l": GL}).dropna()
hl["m"] = hl.index.tz_convert("Europe/Brussels").tz_localize(None).to_period("M")
mon = hl.groupby("m").apply(lambda g: pd.Series({"lwp": (g.p * g.l).sum() / g.l.sum(), "base": g.p.mean(), "hours": len(g)}))
mon = mon[(mon.index >= pd.Period("2015-02", "M")) & (mon.index <= pd.Period(END, "M"))]
mon["o"] = mon["lwp"] / mon["lwp"].shift(1) - 1                          # supplier: cost overrun vs last month's price
mon["eur"] = Q_MW * mon["hours"] * (mon["lwp"] - mon["lwp"].shift(1))    # EUR, 100 MW average volume shaped like national load
mon["ob"] = mon["base"] / mon["base"].shift(1) - 1                       # producer selling flat: revenue change
mon = mon.dropna()
o_pre = mon["o"][mon.index <= pd.Period("2020-12", "M")]
mu_o, sd_o = o_pre.mean(), o_pre.std()
lim_o = mu_o + stats.norm.ppf(0.99) * sd_o
lim_o95 = mu_o + stats.norm.ppf(0.95) * sd_o
post = mon[mon.index >= pd.Period("2021-01", "M")]
worst = mon["o"].idxmax()
N["supplier"] = {"n": int(len(mon)), "start": str(mon.index[0]), "end": str(mon.index[-1]), "n_pre": int(len(o_pre)),
                 "mu_pre": fl(100 * mu_o, 2), "sd_pre": fl(100 * sd_o, 2), "lim99": fl(100 * lim_o, 1), "lim95": fl(100 * lim_o95, 1),
                 "n_post": int(len(post)), "exc99_post": int((post["o"] > lim_o).sum()), "exp99_post": fl(0.01 * len(post), 2),
                 "exc95_post": int((post["o"] > lim_o95).sum()), "exp95_post": fl(0.05 * len(post), 2),
                 "worst": str(worst), "worst_pct": fl(100 * mon.loc[worst, "o"], 1), "worst_eur": fl(mon.loc[worst, "eur"] / 1e6, 2),
                 "q95_all": fl(100 * mon["o"].quantile(0.95), 1), "es95_all": fl(100 * mon["o"][mon["o"] >= mon["o"].quantile(0.95)].mean(), 1),
                 "q95_eur": fl(mon["eur"].quantile(0.95) / 1e6, 2),
                 "es95_eur": fl(mon["eur"][mon["eur"] >= mon["eur"].quantile(0.95)].mean() / 1e6, 2),
                 "sd_all": fl(100 * mon["o"].std(), 1), "lim99_all_normal": fl(100 * (mon["o"].mean() + 2.326 * mon["o"].std()), 1)}
# producer: lower tail of the flat (base) price change, monthly and daily
xr_ = X["RO"].dropna()
N["producer"] = {"m_q05": fl(100 * mon["ob"].quantile(0.05), 1), "m_q95": fl(100 * mon["ob"].quantile(0.95), 1),
                 "m_min": fl(100 * mon["ob"].min(), 1), "m_min_month": str(mon["ob"].idxmin()),
                 "m_max": fl(100 * mon["ob"].max(), 1), "m_max_month": str(mon["ob"].idxmax()),
                 "d_q01": fl(xr_.quantile(0.01), 2), "d_q99": fl(xr_.quantile(0.99), 2),
                 "d_es_lo": fl(-xr_[xr_ <= xr_.quantile(0.025)].mean(), 2), "d_es_hi": fl(xr_[xr_ >= xr_.quantile(0.975)].mean(), 2),
                 "skew": N["dist"]["RO"]["skew"]}

# =============================================================================
# 8. Case study: autumn 2026 (June to the cut-off)
# =============================================================================
C0 = pd.Timestamp("2026-06-01")
cs = {}
xc = X["RO"][C0:END]
for m in METHODS:
    hh = HITS[("RO", m, 0.99)][C0:END].dropna()
    cs[m] = {"x99": int(hh.sum()), "x95": int(HITS[("RO", m, 0.95)][C0:END].dropna().sum())}
cs["n"] = int(len(xc.dropna()))
cs["exp99"] = fl(0.01 * cs["n"], 2)
cs["exp95"] = fl(0.05 * cs["n"], 2)
cs["p_jun"] = fl(PR["2026-06"].mean(), 2)
cs["p_oct"] = fl(PR["2026-10"].mean(), 2)
cs["p_max"] = fl(PR[C0:END].max(), 2)
cs["p_max_date"] = d(PR[C0:END].idxmax())
cs["xmax"] = fl(xc.max(), 2)
cs["xmax_date"] = d(xc.idxmax())
f99 = pd.Series(ENG["RO"]["out"]["fhs"][0.99]["var"], index=DAYS)
h99 = pd.Series(ENG["RO"]["out"]["hs"][0.99]["var"], index=DAYS)
cs["fhs_jun"] = fl(f99["2026-06"].mean(), 2)
cs["fhs_oct"] = fl(f99["2026-10"].mean(), 2)
cs["hs_jun"] = fl(h99["2026-06"].mean(), 2)
cs["hs_oct"] = fl(h99["2026-10"].mean(), 2)
cs["g_jun"] = fl(GDF["cqr"]["2026-06"].mean() * 24 * Q_MW / 1e6, 3)
cs["g_oct"] = fl(GDF["cqr"]["2026-10"].mean() * 24 * Q_MW / 1e6, 3)
cs["g_miss"] = int((GDF["p"] > GDF["cqr"])[C0:END].sum())
cs["qr_miss"] = int((GDF["p"] > GDF["qr"])[C0:END].sum())
for mm in ["2026-08", "2026-09", "2026-10"]:
    pm = pd.Period(mm, "M")
    cs["o_" + mm[-2:]] = fl(100 * mon.loc[pm, "o"], 1)
    cs["eur_" + mm[-2:]] = fl(mon.loc[pm, "eur"] / 1e6, 2)
cs["lim99"] = N["supplier"]["lim99"]
cs["brent_oct"] = fl(F["2026-10"].mean(), 2)
cs["de_oct"] = fl(P["DE_LU"]["2026-10"].mean(), 2)
cs["ttf_oct"] = fl(ep.ttf_monthly()["ttf_eur_mwh"]["2026-10"].iloc[0], 2)
cs["ttf_jun"] = fl(ep.ttf_monthly()["ttf_eur_mwh"]["2026-06"].iloc[0], 2)
cs["z2_after_fhs"] = BT["RO"]["fhs"]["z2"]["after"]["z2"]
N["case"] = cs

# =============================================================================
# 9. Case-study headline numbers (computed by the case notebook C4; copied, not retyped)
# =============================================================================
with open(os.path.join(REPO, "cases", "C4_risk_meter", "numbers.json")) as fh:
    N["c4"] = json.load(fh)

# =============================================================================
# Charts: one set per language
# =============================================================================
LAB = {"hs": ("HS", "HS"), "normal": ("Normal", "Normală"), "t": ("Student-t", "Student-t"), "fhs": ("FHS", "FHS"),
       "evt": ("EVT", "EVT")}
COL = {"hs": PAL["BG"], "normal": PAL["c5"], "t": PAL["c7"], "fhs": PAL["RO"], "evt": PAL["DE_LU"]}
SRC = {"en": {"ec": "energy-charts.info (Fraunhofer ISE); OPCOM (RO) and EPEX SPOT (DE-LU) day-ahead prices, via ENTSO-E",
              "eco": "energy-charts.info (Fraunhofer ISE); OPCOM day-ahead prices for Romania, via ENTSO-E; own estimates",
              "ecl": "energy-charts.info (Fraunhofer ISE); OPCOM prices; ENTSO-E load (Transelectrica data for Romania)",
              "yf": "Yahoo Finance (ICE Brent front-month BZ=F); own computation"},
       "ro": {"ec": "energy-charts.info (Fraunhofer ISE); prețurile PZU ale OPCOM (RO) și EPEX SPOT (DE-LU), prin ENTSO-E",
              "eco": "energy-charts.info (Fraunhofer ISE); prețurile PZU ale OPCOM, prin ENTSO-E; estimări proprii",
              "ecl": "energy-charts.info (Fraunhofer ISE); prețuri OPCOM; consumul ENTSO-E (date Transelectrica pentru România)",
              "yf": "Yahoo Finance (contractul futures Brent ICE cu scadența cea mai apropiată, BZ=F); calcule proprii"}}


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


def legend_room(fig, overlap_in=0.08):
    """Bottom margin (fraction of the figure height) that just fits the bottom legend: tight_layout adds its own pad
    (about 0.16 in) above the margin, so the margin stops overlap_in below the legend's top edge; no empty band is left
    between the x-axis labels and the legend, and the plotting area stays as tall as possible on the slide."""
    fig.canvas.draw()
    top = max(lg.get_window_extent().y1 for lg in fig.legends) / fig.dpi
    return max(top - overlap_in, 0.05) / fig.get_figheight()


def out(fig, lang, name, bottom=None, also_x=()):
    comma_axes(fig, lang, also_x)
    os.makedirs(os.path.join(HERE, "charts", lang), exist_ok=True)
    save(fig, os.path.join(HERE, "charts", lang, name + ".pdf"), bottom=legend_room(fig) if bottom is None else bottom)


def mfmt(ax, lang, step=1):
    # quarterly ticks fall on Jan/Apr/Jul/Oct, so every January (with its year) gets a label
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(1, 13, step)) if step > 1 else mdates.MonthLocator())
    M_ = MON_RO if lang == "ro" else MON_EN
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: M_[mdates.num2date(v).month - 1] +
                                               (f"\n{mdates.num2date(v).year}" if mdates.num2date(v).month == 1 or p == 0 else "")))


for lang in ["en", "ro"]:
    T = (lambda en, ro: en) if lang == "en" else (lambda en, ro: ro)
    L = lambda k: LAB[k][0 if lang == "en" else 1]  # noqa: E731
    # 1 price level and daily change
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.2), sharex=True, gridspec_kw={"height_ratios": [1, 1]})
    axs[0].plot(P.index, P["RO"], color=PAL["RO"], lw=0.6, label=T("Romania, daily base price $P_t$", "România, prețul zilnic de bază $P_t$"))
    axs[0].set_ylabel("EUR/MWh", fontsize=10)
    axs[1].plot(X.index, X["RO"], color=PAL["DE_LU"], lw=0.5, label=T("daily change $X_t = P_t - P_{t-1}$", "variația zilnică $X_t = P_t - P_{t-1}$"))
    axs[1].set_ylabel("EUR/MWh", fontsize=10)
    axs[1].xaxis.set_major_locator(mdates.YearLocator())
    axs[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axs[1].tick_params(axis="x", labelsize=10)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "price_changes")
    # 2 tails: empirical survival of standardised changes vs normal
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    zz = np.linspace(0, 10, 200)
    for z_, ls in [("RO", "-"), ("DE_LU", "--")]:
        s_ = X[z_].dropna()
        zs = np.sort(((s_ - s_.mean()) / s_.std()).values)
        surv = 1 - np.arange(1, len(zs) + 1) / (len(zs) + 1)
        sel = zs > 0
        ax.plot(zs[sel], surv[sel], color=PAL[z_], ls=ls, lw=1.3,
                label=T("Romania", "România") if z_ == "RO" else T("Germany-Luxembourg", "Germania-Luxemburg"))
    ax.plot(zz, stats.norm.sf(zz), color="#222222", lw=1.0, ls=":", label=T("normal distribution", "repartiția normală"))
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 1)
    ax.set_xlim(0, 10)
    ax.set_xlabel(T("size of the daily rise, in standard deviations", "mărimea creșterii zilnice, în abateri standard"))
    ax.set_ylabel(T("share of days", "proporția zilelor"))
    ax.set_yticks([1e-4, 1e-2, 1])
    ax.set_yticks([1e-3, 1e-1], minor=True)
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_yticklabels(["0.0001", "0.01", "1"] if lang == "en" else ["0,0001", "0,01", "1"])
    legend_bottom(fig, ncol=3)
    out(fig, lang, "tails", also_x=[ax])
    # 3 GPD tail fit on the standardised residuals of the last refit (RO)
    E_ = ENG["RO"]
    k_ = len(DAYS) - 1
    hist = X["RO"][:END - pd.Timedelta(days=1)].dropna()[-W_G:]
    md_ = hist.groupby(hist.index.dayofweek).mean()
    e_ = (hist - md_.reindex(hist.index.dayofweek).values).values
    om, al, be, sw = garch_filter(e_)
    z_ = np.sort(e_ / sw)
    u, xi, beta, nu_, n_ = gpd_tail(z_)
    fig, ax = plt.subplots(figsize=(6.4, 2.4))
    zt = z_[z_ > u]
    sv = 1 - (np.searchsorted(z_, zt, side="left")) / len(z_)
    ax.scatter(zt, sv, s=7, color=PAL["RO"], label=T("residuals above $u$ (data)", "reziduuri peste $u$ (date)"), zorder=3)
    gx = np.linspace(u, zt.max() * 1.15, 200)
    ax.plot(gx, (nu_ / n_) * stats.genpareto.sf(gx - u, xi, scale=beta), color=PAL["DE_LU"], lw=1.4,
            label=T("generalised Pareto fit", "ajustarea Pareto generalizată"))
    ax.plot(gx, stats.norm.sf(gx), color="#222222", ls=":", lw=1.0, label=T("normal curve", "curba normală"))
    ax.set_yscale("log")
    ax.set_xlim(u - 0.1, gx[-1] + 0.1)
    ax.set_ylim(stats.norm.sf(gx[-1]) / 3, 0.3)
    _yt = [10.0 ** -k for k in range(1, 9, 2) if 10.0 ** -k >= stats.norm.sf(gx[-1]) / 3]
    ax.set_yticks(_yt)
    ax.set_yticklabels([T(f"{v:.{k}f}", f"{v:.{k}f}".replace(".", ",")) for v, k in zip(_yt, range(1, 9, 2))])
    ax.minorticks_off()
    ax.set_xlabel(T("standardised residual $z$", "reziduul standardizat $z$"))
    ax.set_ylabel("$P(Z > z)$")
    ax._keep_y = True
    legend_bottom(fig, ncol=3)
    out(fig, lang, "gpd_tail", also_x=[ax])
    # 4 VaR paths 2021-2026, 99%
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    a0, a1 = pd.Timestamp("2021-07-01"), pd.Timestamp("2023-06-30")
    xs_ = X["RO"][a0:a1]
    ax.plot(xs_.index, xs_.values, color="#bbbbbb", lw=0.5, label=T("daily change $X_t$", "variația zilnică $X_t$"))
    for m in ["hs", "normal", "fhs"]:
        v = pd.Series(E_["out"][m][0.99]["var"], index=DAYS)[a0:a1]
        ax.plot(v.index, v.values, color=COL[m], lw=0.9, label=T("99% VaR, ", "VaR 99%, ") + L(m))
    hh = HITS[("RO", "fhs", 0.99)][a0:a1]
    hd = hh[hh == 1].index
    ax.scatter(hd, X["RO"].reindex(hd), s=9, color=PAL["c8"], zorder=4, label=T("exceedance of FHS VaR", "depășire a VaR FHS"))
    ax.set_ylabel("EUR/MWh")
    ax.set_ylim(-180, 280)
    mfmt(ax, lang, 3)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "var_paths")
    # 5 horizon scaling
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    hs_ = list(range(1, 21))
    ax.plot(hs_, np.sqrt(hs_), color="#222222", ls=":", lw=1.2, label=T("square-root-of-time rule", "regula rădăcinii pătrate"))
    ax.plot(hs_, [HOR["RO"][h] for h in hs_], color=PAL["RO"], marker="o", ms=3, lw=1.2, label=T("Romania (data)", "România (date)"))
    ax.plot(hs_, [HOR["DE_LU"][h] for h in hs_], color=PAL["DE_LU"], marker="s", ms=3, lw=1.2, ls="--", label=T("Germany-Luxembourg (data)", "Germania-Luxemburg (date)"))
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.set_xlabel(T("horizon $h$ (days)", "orizontul $h$ (zile)"))
    ax.set_ylabel(T("$h$-day / 1-day\n99% quantile", "cuantila de 99%:\n$h$ zile / 1 zi"), fontsize=10)
    ax.set_ylim(0.8, 4.8)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "horizon")
    # 6 traffic light: rolling 250-day exceedance count at 99%
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    for m in METHODS:
        c = HITS[("RO", m, 0.99)].fillna(0).rolling(250).sum()
        ax.plot(c.index, c.values, color=COL[m], lw=1.0, label=L(m))
    ax.axhspan(-0.5, 4.5, color=PAL["c6"], alpha=0.10, lw=0)
    ax.axhspan(4.5, 9.5, color=PAL["BG"], alpha=0.15, lw=0)
    ax.axhspan(9.5, 40, color=PAL["c8"], alpha=0.10, lw=0)
    ytop = max(25, max(BT["RO"][m]["a99"]["max250"] for m in METHODS) + 2)
    tr = ax.get_yaxis_transform()                 # x in axes units, y in data units: labels in the right margin
    for y_, lab_, c_ in [(2, T("green", "verde"), PAL["c6"]), (7, T("yellow", "galben"), "#9a6a00"),
                         ((9.5 + ytop) / 2, T("red", "roșu"), PAL["c8"])]:
        ax.text(1.01, y_, lab_, transform=tr, fontsize=9.5, color=c_, va="center", ha="left", clip_on=False)
    ax.set_xlim(DAYS[249] - pd.Timedelta(days=30), DAYS[-1] + pd.Timedelta(days=30))
    ax.set_ylim(0, ytop)
    ax.set_ylabel(T("exceedances,\nlast 250 days", "depășiri în\nultimele 250 de zile"), fontsize=10)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, ncol=5)
    out(fig, lang, "traffic")
    # 7 Brent initial margin per lot
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    ax.plot(im.index, im["im1"] / 1000, color=PAL["RO"], lw=1.0, label=T("99% 2-day HS, 12-month lookback", "HS 99% pe 2 zile, istoric de 12 luni"))
    ax.plot(im.index, im["ima"] / 1000, color=PAL["DE_LU"], lw=1.0, ls="--", label=T("floor: lookback since 2015 (anti-procyclical)", "prag: istoric din 2015 (anticiclic)"))
    ax.set_ylabel(T("IM, thousand\nUSD per lot", "IM, mii USD\npe lot"), fontsize=10)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, ncol=2)
    out(fig, lang, "brent_im")
    # 8 coverage of the guarantee rule (99%) by period
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    labs = [T("2017-2020", "2017-2020"), T("2021-2022", "2021-2022"), T("2023-" + str(END.year), "2023-" + str(END.year))]
    ww = 0.26
    for j, (k_, lab_, c_) in enumerate([("qr", T("quantile regression", "regresie cuantilică"), PAL["BG"]),
                                         ("cqr", T("+ conformal widening", "+ lărgire conformală"), PAL["RO"]),
                                         ("fhs", "FHS", PAL["DE_LU"])]):
        vals = [GUAR["a99"][k_][f"cov_{p_[0]}"] for p_ in PERIODS]
        ax.bar(np.arange(3) + (j - 1) * ww, vals, width=ww, color=c_, label=lab_)
    ax.axhline(99, color="#222222", lw=0.9, ls=":", label=T("target 99%", "ținta 99%"))
    ax.set_xticks(range(3))
    ax.set_xticklabels(labs)
    ax.set_ylim(90, 100.5)
    ax.set_ylabel(T("coverage, % of days", "acoperirea,\n% din zile"), fontsize=10)
    legend_bottom(fig, ncol=4)
    out(fig, lang, "coverage")
    # 9 supplier monthly overrun
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    xm = mon.index.to_timestamp()
    above = (mon["o"] > lim_o).values
    ax.bar(xm[~above], 100 * mon["o"][~above], width=22, color=PAL["RO"],
           label=T("cost overrun: monthly change of the load-weighted price", "depășirea costului: variația lunară a prețului ponderat cu consumul"))
    ax.bar(xm[above], 100 * mon["o"][above], width=22, color=PAL["c8"], label=T("above the limit", "peste limită"))
    ax.axhline(100 * lim_o, color="#222222", lw=0.9, ls="--", label=T("normal 99% limit, 2015-2020 data", "limita normală de 99%, date 2015-2020"))
    ax.set_ylabel("%")
    ax.tick_params(axis="x", labelsize=10)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, ncol=2)
    out(fig, lang, "supplier_month")
    # 10 case study: autumn 2026
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    cc = pd.date_range(C0, END, freq="D")
    ax.plot(cc, PR.reindex(cc), color="#222222", lw=1.2, label=T("base price $P_t$", "prețul de bază $P_t$"))
    for m, ls in [("hs", "--"), ("fhs", "-")]:
        band = PR.shift(1).reindex(cc) + pd.Series(E_["out"][m][0.99]["var"], index=DAYS).reindex(cc)
        ax.plot(cc, band, color=COL[m], lw=1.0, ls=ls, label=T("P(t-1) + 99% VaR, ", "P(t-1) + VaR 99%, ") + L(m))
    ax.plot(cc, GDF["cqr"].reindex(cc), color=PAL["HU"], lw=0.9, ls="-.", label=T("guarantee limit (conformal 99%)", "limita garanției (conformal 99%)"))
    hd = HITS[("RO", "fhs", 0.99)].reindex(cc)
    hd = hd[hd == 1].index
    ax.scatter(hd, PR.reindex(hd), s=14, color=PAL["c8"], zorder=4, label=T("FHS exceedance", "depășire FHS"))
    ax.set_ylabel("EUR/MWh")
    mfmt(ax, lang)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "case2026")

P0, P1 = d(T0), d(END)
chart("price_changes", "eco", f"daily, {d(START)} to {P1} (CET delivery days)", f"date zilnice, {d(START)} - {P1} (zile de livrare CET)")
chart("tails", "ec", f"daily changes, {d(START)} to {P1}", f"variații zilnice, {d(START)} - {P1}")
chart("gpd_tail", "eco", f"GARCH-filtered changes, the {W_G} days before {P1}", f"variații filtrate GARCH, cele {W_G} de zile dinainte de {P1}")
chart("var_paths", "eco", "forecasts for 2021-07-01 to 2023-06-30", "prognoze pentru 2021-07-01 - 2023-06-30")
chart("horizon", "ec", f"daily base prices, {d(START)} to {P1}", f"prețuri zilnice de bază, {d(START)} - {P1}")
chart("traffic", "eco", f"backtest {P0} to {P1}, 99\\% VaR", f"testare retrospectivă {P0} - {P1}, VaR 99\\%")
chart("brent_im", "yf", f"trading days 2016-01-01 to {d(F.index[-1])}; contract-roll days dropped; 1 lot = 1,000 bbl",
      f"zile de tranzacționare 2016-01-01 - {d(F.index[-1])}; fără zilele de schimbare a contractului; 1 lot = 1.000 bbl")
chart("coverage", "eco", f"forecasts {P0} to {P1}, 99\\% quantile", f"prognoze {P0} - {P1}, cuantila de 99\\%")
chart("supplier_month", "ecl", f"monthly, {N['supplier']['start']} to {N['supplier']['end']}", f"lunar, {N['supplier']['start']} - {N['supplier']['end']}")
chart("case2026", "eco", f"daily, {d(C0)} to {P1}", f"date zilnice, {d(C0)} - {P1}")

with open(os.path.join(HERE, "L4_numbers.json"), "w") as fh:
    json.dump(N, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("wrote L4_numbers.json and", len(N["charts"]), "charts x 2 languages")
