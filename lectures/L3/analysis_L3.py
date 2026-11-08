"""
analysis_L3.py -- Lecture 3 "Volatility of energy prices" (EMQA)
================================================================
Reads the real series in repo/data/clean (see data/SOURCES.md), estimates every volatility model shown on the slides and writes
    lectures/L3/L3_numbers.json        all results (the deck builder reads ONLY this file)
    lectures/L3/charts/en/*.pdf        figures with English labels
    lectures/L3/charts/ro/*.pdf        the same figures with Romanian labels
Run:  python3 lectures/L3/analysis_L3.py

Design
  * Power: daily base price (mean of all MTUs of the CET/CEST delivery day), panel 2019-01-01 to the cut-off (last complete
    month); no missing day for Romania in this period. Two measures of the daily change, on the full calendar:
        r_t = 100 ln(P_t / P_{t-1})   (percent; undefined if a price is <= 0, then left missing)
        u_t = P_t - P_{t-1}           (EUR/MWh; defined for any sign)
  * Two-step modelling: (1) mean equation by OLS: constant + AR(1..7) + six day-of-week dummies, removes the weekly calendar;
    (2) volatility models on the residuals with zero mean: GARCH(1,1), GJR-GARCH(1,1,1), EGARCH(1,1,1), normal or Student-t.
  * Markets (Brent, EUA, equities): log returns on trading days. Brent BZ=F: the first trading day of every month (contract
    roll) is dropped (rule 9). Equities: dividend-adjusted closes, days with zero volume dropped. TTF: only monthly averages
    are free (World Bank), used for a monthly volatility only.
  * Intraday variation from hourly prices (15-min MTUs averaged to the hour after 1 Oct 2025): RV_d = sqrt(sum_h dP_{d,h}^2).
  * Test year = last 365 days to the cut-off: one-day-ahead variance forecasts, all models re-estimated every day on an
    expanding window that ends the day before (mean equation included). Proxy = squared out-of-sample residual.
  * No simulated data in this lecture.
"""

import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from arch import arch_model
from joblib import Parallel, delayed
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
from statsmodels.tsa.stattools import acf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import emqa_plot as ep  # noqa: E402
from emqa_plot import PAL, legend_bottom, save  # noqa: E402

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter, MaxNLocator  # noqa: E402

warnings.filterwarnings("ignore")
ep.style()
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "data", "clean")
TZ = "Europe/Brussels"
N = {"charts": {}}
MON_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MON_RO = ["ian.", "feb.", "mar.", "apr.", "mai", "iun.", "iul.", "aug.", "sep.", "oct.", "nov.", "dec."]
DOWN = {"en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "ro": ["lun.", "mar.", "mie.", "joi", "vin.", "sîm.", "dum."]}


def d(ts):
    return pd.Timestamp(ts).strftime("%Y-%m-%d")


def fl(x, k=4):
    if x is None:
        return None
    x = float(x)
    return None if not np.isfinite(x) else round(x, k)


# =============================================================================
# 0. Load data and cut-off (last complete month of the Romanian day-ahead price)
# =============================================================================
PD = ep.prices_daily()
_raw_last = PD["RO"].dropna().index.max()
END = pd.Timestamp(((_raw_last + pd.Timedelta(days=1)).to_period("M").to_timestamp() - pd.Timedelta(days=1)).date())
START = pd.Timestamp("2019-01-01")
CAL = pd.date_range(START, END, freq="D")
N["cutoff"] = {"end": d(END), "download": "2026-11-04"}
N["data"] = {"start": d(START), "end": d(END), "n_days": len(CAL), "y0": START.year, "y1": END.year}

FU = ep.fuels_daily()
EUA = pd.read_csv(os.path.join(DATA, "eua_daily.csv"), parse_dates=["date"]).set_index("date")["eua_etc_co2l_eur_per_unit"]
EQ = pd.read_csv(os.path.join(DATA, "ro_energy_equities_daily.csv"), parse_dates=["date"]).set_index("date")
TTF = ep.ttf_monthly()
GEN = ep.generation_ro_daily()

PR = {z: PD[z].reindex(CAL) for z in ["RO", "HU", "DE_LU", "BG"]}
assert not PR["RO"].isna().any(), "RO daily price has gaps in the panel"


# =============================================================================
# 1. Daily changes: percent (log) and EUR/MWh; non-positive prices
# =============================================================================
def pct_change(p):
    """100 * log change on the full calendar; missing if either price is <= 0 or missing (no multi-day jumps)."""
    lp = np.log(p.where(p > 0))
    return 100 * lp.diff()


R_PCT = {z: pct_change(PR[z]) for z in PR}
R_EUR = {z: PR[z].diff() for z in PR}
nonpos = {z: int((PR[z] <= 0).sum()) for z in PR}
N["nonpos"] = {"daily": nonpos, "ro_min": fl(PR["RO"].min(), 2), "ro_min_date": d(PR["RO"].idxmin()),
               "de_min": fl(PR["DE_LU"].min(), 2), "de_min_date": d(PR["DE_LU"].idxmin())}
NAT = pd.read_csv(os.path.join(DATA, "power_da_prices_native_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
NAT.index = NAT.index.tz_convert(TZ)
_nat = NAT.loc[str(START.date()):str(END.date())]
for z in ["RO", "DE_LU"]:
    neg = _nat[z] < 0
    N["nonpos"][f"neg_heq_{z}"] = fl((neg * _nat["mtu_minutes"] / 60).sum(), 2)
    N["nonpos"][f"neg_days_{z}"] = int(neg.groupby(_nat.index.tz_localize(None).normalize()).any().sum())
# a near-zero day blows up the log change: largest |r| for Germany, where daily base prices touch zero
_rde = R_PCT["DE_LU"].dropna()
N["nonpos"]["de_maxabs_pct"] = fl(_rde.abs().max(), 1)
N["nonpos"]["de_maxabs_date"] = d(_rde.abs().idxmax())
N["nonpos"]["de_maxabs_p0"] = fl(PR["DE_LU"].shift(1).loc[_rde.abs().idxmax()], 2)
N["nonpos"]["de_maxabs_p1"] = fl(PR["DE_LU"].loc[_rde.abs().idxmax()], 2)
# asinh change vs log change for prices well above 1 EUR/MWh
N["nonpos"]["asinh_vs_log_100_120"] = fl(100 * (np.arcsinh(120) - np.arcsinh(100)), 3)
N["nonpos"]["log_100_120"] = fl(100 * np.log(1.2), 3)

rr = R_PCT["RO"].dropna()
N["ret"] = {"n": int(len(rr)), "sd": fl(rr.std(), 2), "mean": fl(rr.mean(), 3), "max": fl(rr.max(), 1), "max_date": d(rr.idxmax()),
            "min": fl(rr.min(), 1), "min_date": d(rr.idxmin()), "n_abs50": int((rr.abs() > 50).sum()),
            "sd_eur": fl(R_EUR["RO"].std(), 2)}


# =============================================================================
# 2. Mean equation: constant + AR(1..7) + day-of-week dummies (OLS); residuals = the shocks that GARCH models
# =============================================================================
def mean_design(y, lags=7):
    X = pd.DataFrame({f"L{k}": y.shift(k) for k in range(1, lags + 1)}, index=y.index)
    for j in range(1, 7):
        X[f"D{j}"] = (y.index.dayofweek == j).astype(float)
    X.insert(0, "const", 1.0)
    return X


def mean_fit(y, lags=7):
    """OLS mean equation on the full calendar; returns (residual series, fitted model)."""
    X = mean_design(y, lags)
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    m = sm.OLS(df["y"], df.drop(columns="y")).fit()
    return m.resid, m


E_PCT, M_PCT = mean_fit(R_PCT["RO"])
E_EUR, M_EUR = mean_fit(R_EUR["RO"])
_dow = rr.groupby(rr.index.dayofweek).mean()
_dowe = R_EUR["RO"].groupby(R_EUR["RO"].index.dayofweek).mean()
N["mean"] = {"r2_pct": fl(M_PCT.rsquared, 3), "r2_eur": fl(M_EUR.rsquared, 3), "n": int(M_PCT.nobs),
             "dow_pct": {DOWN["en"][k]: fl(v, 2) for k, v in _dow.items()},
             "dow_eur": {DOWN["en"][k]: fl(v, 2) for k, v in _dowe.items()},
             "sd_raw": fl(rr.loc[E_PCT.index].std(), 2), "sd_res": fl(E_PCT.std(), 2),
             "var_cut": fl(100 * (1 - E_PCT.var() / rr.loc[E_PCT.index].var()), 1)}

# =============================================================================
# 3. Stylised facts: clustering (Ljung-Box, ARCH-LM) and fat tails
# =============================================================================
lb_e = acorr_ljungbox(E_PCT, [10])
lb_e2 = acorr_ljungbox(E_PCT ** 2, [10])
lb_u2 = acorr_ljungbox(E_EUR ** 2, [10])
lm = het_arch(E_PCT, nlags=10)
lmu = het_arch(E_EUR, nlags=10)
z_ = (E_PCT - E_PCT.mean()) / E_PCT.std()
N["facts"] = {"lb_e": fl(lb_e["lb_stat"].iloc[0], 1), "lb_e_p": fl(lb_e["lb_pvalue"].iloc[0], 3),
              "lb_e2": fl(lb_e2["lb_stat"].iloc[0], 1), "lb_u2": fl(lb_u2["lb_stat"].iloc[0], 1),
              "lm": fl(lm[0], 1), "lm_p": fl(lm[1], 6), "lmu": fl(lmu[0], 1),
              "kurt": fl(E_PCT.kurt(), 2), "skew": fl(E_PCT.skew(), 2), "kurt_eur": fl(E_EUR.kurt(), 2),
              "n_4sd": int((z_.abs() > 4).sum()), "n_4sd_norm": fl(len(z_) * 2 * stats.norm.sf(4), 2), "n": int(len(z_)),
              "acf_e2_1": fl(acf(E_PCT ** 2, nlags=1)[1], 3), "acf_e_1": fl(acf(E_PCT, nlags=1)[1], 3)}


# =============================================================================
# 4. Volatility by year and by market (annualised): power sqrt(365) (auction every day), markets sqrt(252)
# =============================================================================
def mkt_returns(px, drop_roll=False, vol=None):
    px = px.dropna()
    if vol is not None:
        px = px[vol.reindex(px.index).fillna(0) > 0]
    r = 100 * np.log(px).diff().dropna()
    n_roll = 0
    if drop_roll:   # first trading day of each month: front-month contract changes (cross-contract jump, not a price move)
        first = r.index.to_series().groupby(r.index.to_period("M")).transform("min") == r.index
        n_roll = int(first.sum())
        r = r[~first]
    return r, n_roll


BRENT, n_roll = mkt_returns(FU["brent_usd_bbl"].loc[str(START - pd.Timedelta(days=10)):str(END)], drop_roll=True)
BRENT = BRENT.loc[START:END]
EUAR, _ = mkt_returns(EUA.loc[:str(END)])
SNP, _ = mkt_returns(EQ["SNP_adjclose_ron"].loc[str(START - pd.Timedelta(days=10)):str(END)], vol=EQ["SNP_volume"])
SNP = SNP.loc[START:END]
H2O, _ = mkt_returns(EQ["H2O_adjclose_ron"].loc[:str(END)], vol=EQ["H2O_volume"])
TTFm = 100 * np.log(TTF["ttf_eur_mwh"]).diff().loc[str(START):str(END)].dropna()
N["mkt"] = {"brent_n_roll": n_roll, "brent_start": d(BRENT.index[0]), "eua_start": d(EUAR.index[0]), "h2o_start": d(H2O.index[0]),
            "brent_n": len(BRENT), "eua_n": len(EUAR), "snp_n": len(SNP), "h2o_n": len(H2O)}
YEARS = list(range(START.year, END.year + 1))
SER = {"RO": (E_PCT, 365), "HU": (mean_fit(R_PCT["HU"].dropna().reindex(CAL))[0], 365), "EUA": (EUAR, 252), "BRENT": (BRENT, 252),
       "TTF": (TTFm, 12), "SNP": (SNP, 252), "H2O": (H2O, 252)}
# HU: the 2 days with a non-positive base price leave their changes missing; the AR terms then drop the next 7 days too
VOLY = {}
for k, (s, a) in SER.items():
    VOLY[k] = {}
    for y in YEARS:
        x = s[s.index.year == y]
        VOLY[k][str(y)] = fl(x.std() * np.sqrt(a), 0) if len(x) >= (10 if k == "TTF" else 100) else None
N["voly"] = VOLY
N["voly"]["RO_eur"] = {str(y): fl(E_EUR[E_EUR.index.year == y].std(), 1) for y in YEARS}
N["voly"]["RO_lvl"] = {str(y): fl(PR["RO"][PR["RO"].index.year == y].mean(), 1) for y in YEARS}
N["voly"]["RO_pct_d"] = {str(y): fl(E_PCT[E_PCT.index.year == y].std(), 1) for y in YEARS}
N["voly"]["ratio_eur_22_19"] = fl(N["voly"]["RO_eur"]["2022"] / N["voly"]["RO_eur"]["2019"], 1)
N["voly"]["ratio_pct_22_19"] = fl(N["voly"]["RO_pct_d"]["2022"] / N["voly"]["RO_pct_d"]["2019"], 2)
N["voly"]["RO_full_ann"] = fl(E_PCT.std() * np.sqrt(365), 0)
N["voly"]["BRENT_full_ann"] = fl(BRENT.std() * np.sqrt(252), 0)
N["voly"]["EUA_full_ann"] = fl(EUAR.std() * np.sqrt(252), 0)
N["voly"]["ratio_ro_brent"] = fl(E_PCT.std() * np.sqrt(365) / (BRENT.std() * np.sqrt(252)), 1)


# =============================================================================
# 5. GARCH family, full sample
# =============================================================================
def fit(e, vol="GARCH", o=0, dist="t"):
    return arch_model(np.asarray(e, float), mean="Zero", vol=vol, p=1, o=o, q=1, dist=dist, rescale=False).fit(disp="off", show_warning=False)


def persistence(res, vol="GARCH", o=0):
    p = res.params
    if vol == "EGARCH":
        return float(p["beta[1]"])
    return float(p["alpha[1]"] + p["beta[1]"] + (0.5 * p["gamma[1]"] if o else 0))


def half_life(ph):
    return np.log(0.5) / np.log(ph) if 0 < ph < 1 else None


def summary(res, vol="GARCH", o=0, ann=365):
    p, t_ = res.params, res.tvalues
    ph = persistence(res, vol, o)
    out = {"ll": fl(res.loglikelihood, 1), "aic": fl(res.aic, 1), "bic": fl(res.bic, 1), "pers": fl(ph, 4),
           "hl": fl(half_life(ph), 1), "n": int(res.nobs)}
    for k in p.index:
        kk = k.replace("[1]", "")
        out[kk] = fl(p[k], 4)
        out[kk + "_t"] = fl(t_[k], 2)
        out[kk + "_se"] = fl(res.std_err[k], 4)
    if vol == "GARCH" and ph < 1:
        out["uvar"] = fl(p["omega"] / (1 - ph), 3)
        out["usd"] = fl(np.sqrt(p["omega"] / (1 - ph)), 2)
        out["usd_ann"] = fl(np.sqrt(p["omega"] / (1 - ph) * ann), 0)
    z = res.std_resid
    lbz = acorr_ljungbox(z ** 2, [10])
    out["lbz2"] = fl(lbz["lb_stat"].iloc[0], 1)
    out["lbz2_p"] = fl(lbz["lb_pvalue"].iloc[0], 3)
    return out


SPEC = {"garch_n": ("GARCH", 0, "normal"), "garch_t": ("GARCH", 0, "t"), "gjr_n": ("GARCH", 1, "normal"), "gjr_t": ("GARCH", 1, "t"),
        "egarch_n": ("EGARCH", 1, "normal"), "egarch_t": ("EGARCH", 1, "t")}
FITS = {}
G = {}
for unit, e in [("pct", E_PCT), ("eur", E_EUR)]:
    G[unit] = {}
    for k, (v, o, ds) in SPEC.items():
        res = fit(e, v, o, ds)
        FITS[(unit, k)] = res
        G[unit][k] = summary(res, v, o)
    best = min(SPEC, key=lambda k: G[unit][k]["bic"])
    G[unit]["best_bic"] = best
N["garch"] = G
# conditional volatility (GARCH-t) as series
CV = {u: pd.Series(FITS[(u, "garch_t")].conditional_volatility, index=(E_PCT if u == "pct" else E_EUR).index) for u in ["pct", "eur"]}
N["garch"]["cv"] = {"pct_max": fl(CV["pct"].max(), 1), "pct_max_date": d(CV["pct"].idxmax()), "pct_min": fl(CV["pct"].min(), 1),
                    "eur_max": fl(CV["eur"].max(), 1), "eur_max_date": d(CV["eur"].idxmax()), "eur_min": fl(CV["eur"].min(), 1),
                    "eur_min_date": d(CV["eur"].idxmin()), "eur_last": fl(CV["eur"].iloc[-1], 1), "pct_last": fl(CV["pct"].iloc[-1], 1)}

# across markets: GARCH(1,1)-t and the GJR asymmetry
XM = {"RO_pct": (E_PCT, 365), "RO_eur": (E_EUR, 365), "HU_pct": (SER["HU"][0], 365), "EUA": (EUAR - EUAR.mean(), 252),
      "BRENT": (BRENT - BRENT.mean(), 252), "SNP": (SNP - SNP.mean(), 252)}
# H2O (Hidroelectrica) is listed only since July 2023: its GARCH estimate sits on the boundary alpha + beta = 1, so it is
# shown in the yearly volatility table only
N["xm"] = {}
for k, (e, a) in XM.items():
    e = e.dropna()
    g_, j_ = fit(e), fit(e, o=1)
    s_ = summary(g_, ann=a)
    N["xm"][k] = {"alpha": s_["alpha"], "beta": s_["beta"], "pers": s_["pers"], "hl": s_["hl"], "nu": s_["nu"],
                  "gamma": fl(j_.params["gamma[1]"], 3), "gamma_t": fl(j_.tvalues["gamma[1]"], 1), "n": int(len(e)),
                  "start": d(e.index[0]), "end": d(e.index[-1]), "usd_ann": s_.get("usd_ann")}
# half-life in calendar weeks for markets (5 trading days a week) and days for power
N["xm"]["BRENT"]["hl_weeks"] = fl(N["xm"]["BRENT"]["hl"] / 5, 1)
N["xm"]["EUA"]["hl_weeks"] = fl(N["xm"]["EUA"]["hl"] / 5, 1)
N["xm"]["RO_eur"]["hl_weeks"] = fl(N["xm"]["RO_eur"]["hl"] / 7, 1)

# news impact curves (GJR-t)
NIC = {}
for u in ["pct", "eur"]:
    p = FITS[(u, "gjr_t")].params
    ph = p["alpha[1]"] + 0.5 * p["gamma[1]"] + p["beta[1]"]
    s2 = p["omega"] / (1 - ph)
    sd = np.sqrt(s2)
    x = np.linspace(-4 * sd, 4 * sd, 201)
    NIC[u] = (x, np.sqrt(p["omega"] + p["beta[1]"] * s2 + (p["alpha[1]"] + p["gamma[1]"] * (x < 0)) * x ** 2), sd)
    up = np.sqrt(p["omega"] + p["beta[1]"] * s2 + p["alpha[1]"] * (2 * sd) ** 2)
    dn = np.sqrt(p["omega"] + p["beta[1]"] * s2 + (p["alpha[1]"] + p["gamma[1]"]) * (2 * sd) ** 2)
    N["garch"][u]["nic_up2"] = fl(up, 2)
    N["garch"][u]["nic_dn2"] = fl(dn, 2)
    N["garch"][u]["nic_2sd"] = fl(2 * sd, 1)

# volatility rises with the price level (monthly, EUR/MWh)
_m = pd.DataFrame({"sd": E_EUR.groupby(E_EUR.index.to_period("M")).std(), "lvl": PR["RO"].groupby(PR["RO"].index.to_period("M")).mean()}).dropna()
_ll = sm.OLS(np.log(_m["sd"]), sm.add_constant(np.log(_m["lvl"]))).fit()
_mp = pd.DataFrame({"sd": E_PCT.groupby(E_PCT.index.to_period("M")).std(), "lvl": _m["lvl"]}).dropna()
_lp = sm.OLS(np.log(_mp["sd"]), sm.add_constant(np.log(_mp["lvl"]))).fit()
N["level"] = {"slope": fl(_ll.params.iloc[1], 2), "r2": fl(_ll.rsquared, 2), "n": len(_m), "slope_pct": fl(_lp.params.iloc[1], 2),
              "r2_pct": fl(_lp.rsquared, 2), "corr": fl(np.corrcoef(np.log(_m["sd"]), np.log(_m["lvl"]))[0, 1], 2)}

# =============================================================================
# 6. Regimes: two-state Markov switching on the EUR/MWh shocks (and on percent, for contrast); sub-period persistence
# =============================================================================
np.random.seed(20261106)
MS = {}
for u, e in [("eur", E_EUR), ("pct", E_PCT)]:
    m = MarkovRegression(e.values, k_regimes=2, trend="c", switching_variance=True).fit(search_reps=20, disp=False)
    s2 = m.params[-2:]
    hi = int(np.argmax(s2))
    lo = 1 - hi
    P_ = m.regime_transition[:, :, 0]          # P_[i, j] = Pr(s_t = i | s_{t-1} = j)
    MS[u] = (m, hi, pd.Series(m.smoothed_marginal_probabilities[:, hi], index=e.index))
    N.setdefault("ms", {})[u] = {"sd_hi": fl(np.sqrt(s2[hi]), 1), "sd_lo": fl(np.sqrt(s2[lo]), 1), "p_hh": fl(P_[hi, hi], 3),
                                 "p_ll": fl(P_[lo, lo], 3), "dur_hi": fl(1 / (1 - P_[hi, hi]), 1), "dur_lo": fl(1 / (1 - P_[lo, lo]), 1),
                                 "share_hi": fl(100 * (MS[u][2] > 0.5).mean(), 1),
                                 "by_year": {str(y): fl(100 * (MS[u][2][MS[u][2].index.year == y] > 0.5).mean(), 0) for y in YEARS}}
_ph = MS["eur"][2]
_runs = (_ph > 0.5).astype(int)
_g = (_runs.diff() != 0).cumsum()
_spells = _runs.groupby(_g).agg(["first", "size"])
_long = _spells[_spells["first"] == 1].sort_values("size", ascending=False)
_gl = _long.index[0]
_idx = _runs[_g == _gl].index
N["ms"]["eur"]["longest_start"] = d(_idx[0])
N["ms"]["eur"]["longest_end"] = d(_idx[-1])
N["ms"]["eur"]["longest_days"] = int(len(_idx))
N["ms"]["eur"]["n_spells"] = int(len(_long))
N["ms"]["eur"]["last_prob"] = fl(_ph.iloc[-1], 2)
N["ms"]["eur"]["share_2026_q3q4"] = fl(100 * (_ph.loc["2026-07-01":] > 0.5).mean(), 0)

SUB = [("2019-01-01", "2020-12-31"), ("2021-01-01", "2022-12-31"), ("2023-01-01", str(END.date())), (str(START.date()), str(END.date()))]
N["sub"] = {}
for u, e in [("pct", E_PCT), ("eur", E_EUR)]:
    N["sub"][u] = []
    for a, b in SUB:
        res = fit(e.loc[a:b])
        s_ = summary(res)
        N["sub"][u].append({"a": a, "b": b, "alpha": s_["alpha"], "beta": s_["beta"], "pers": s_["pers"], "hl": s_["hl"],
                            "usd": s_.get("usd"), "n": s_["n"]})

# =============================================================================
# 7. Intraday variation from hourly prices; HAR model
# =============================================================================
HP = ep.prices_hourly()["RO"].dropna()
HP = HP.loc[str(START.date()):str(END.date())]
_h = pd.DataFrame({"p": HP.values, "day": HP.index.tz_localize(None).normalize()})
_h["dp"] = _h.groupby("day")["p"].diff()
_gh = _h.groupby("day")
RV = pd.DataFrame({"rv": np.sqrt(_gh["dp"].apply(lambda x: (x ** 2).sum(min_count=1))), "n": _gh["p"].count(),
                   "rng": _gh["p"].max() - _gh["p"].min(), "lvl": _gh["p"].mean()}).reindex(CAL)
assert RV["rv"].notna().all()
RV["rel"] = RV["rv"] / RV["lvl"].abs()
SOL = GEN["solar"].reindex(CAL)
N["rv"] = {"by_year": {str(y): fl(RV["rv"][RV.index.year == y].mean(), 1) for y in YEARS},
           "rel_by_year": {str(y): fl(RV["rel"][RV.index.year == y].median(), 2) for y in YEARS},
           "rng_by_year": {str(y): fl(RV["rng"][RV.index.year == y].mean(), 1) for y in YEARS},
           "n_days": int(RV["rv"].notna().sum()), "n_23": int((RV["n"] == 23).sum()), "n_25": int((RV["n"] == 25).sum()),
           "corr_daily_abs": fl(np.corrcoef(RV["rv"].iloc[1:], E_EUR.reindex(CAL).abs().iloc[1:].fillna(0))[0, 1], 2)}
_mm = pd.DataFrame({"rel": RV["rel"].resample("MS").median(), "sol": SOL.resample("MS").mean()}).dropna()
N["rv"]["corr_rel_solar_m"] = fl(np.corrcoef(_mm["rel"], _mm["sol"])[0, 1], 2)
N["rv"]["sol_2019"] = fl(SOL[SOL.index.year == 2019].mean(), 0)
N["rv"]["sol_last"] = fl(SOL[SOL.index.year == END.year].mean(), 0)
N["rv"]["rel_ratio"] = fl(N["rv"]["rel_by_year"][str(END.year)] / N["rv"]["rel_by_year"]["2019"], 1)
_peak_y = max(YEARS, key=lambda y: N["rv"]["rel_by_year"][str(y)])
N["rv"]["rel_peak_year"] = _peak_y


def har_design(rv):
    lr = np.log(rv)
    return pd.DataFrame({"y": lr, "d": lr.shift(1), "w": lr.shift(1).rolling(7).mean(), "m": lr.shift(1).rolling(30).mean()})


TEST0 = END - pd.Timedelta(days=364)
TDAYS = pd.date_range(TEST0, END, freq="D")
HD = har_design(RV["rv"]).dropna()
_tr = HD.loc[:TEST0 - pd.Timedelta(days=1)]
HAR = sm.OLS(_tr["y"], sm.add_constant(_tr[["d", "w", "m"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 7})
# out of sample: re-estimated every day on the expanding window
_pred = []
for t in TDAYS:
    tr = HD.loc[:t - pd.Timedelta(days=1)]
    b = np.linalg.lstsq(sm.add_constant(tr[["d", "w", "m"]]).values, tr["y"].values, rcond=None)[0]
    s2 = np.var(tr["y"].values - sm.add_constant(tr[["d", "w", "m"]]).values @ b)
    _pred.append(np.exp(np.r_[1.0, HD.loc[t, ["d", "w", "m"]].values] @ b + 0.5 * s2))
HARF = pd.Series(_pred, index=TDAYS)
_act = RV["rv"].loc[TDAYS]
_naive = RV["rv"].shift(1).loc[TDAYS]
N["har"] = {"b0": fl(HAR.params["const"], 3), "bd": fl(HAR.params["d"], 3), "bw": fl(HAR.params["w"], 3), "bm": fl(HAR.params["m"], 3),
            "bd_t": fl(HAR.tvalues["d"], 1), "bw_t": fl(HAR.tvalues["w"], 1), "bm_t": fl(HAR.tvalues["m"], 1),
            "r2": fl(HAR.rsquared, 2), "n": int(HAR.nobs), "mae_har": fl((HARF - _act).abs().mean(), 1),
            "mae_naive": fl((_naive - _act).abs().mean(), 1), "gain": fl(100 * (1 - (HARF - _act).abs().mean() / (_naive - _act).abs().mean()), 1),
            "persist": fl(HAR.params["d"] + HAR.params["w"] + HAR.params["m"], 3)}
N["design"] = {"test_start": d(TEST0), "test_end": d(END), "n_test": len(TDAYS)}


# =============================================================================
# 8. Forecasting volatility on the test year: rolling one-day-ahead forecasts, QLIKE and MSE, DM tests
# =============================================================================
VMODELS = ["hist30", "ewma", "garch", "gjr", "egarch"]


def one_day(y, t):
    """All volatility forecasts for day t from data up to t-1 (mean equation re-estimated on the same window)."""
    X = mean_design(y)
    df = pd.concat([y.rename("y"), X], axis=1)
    tr = df.loc[:t - pd.Timedelta(days=1)].dropna()
    Xt, yt = tr.drop(columns="y").values, tr["y"].values
    b = np.linalg.lstsq(Xt, yt, rcond=None)[0]
    e_tr = yt - Xt @ b
    yhat = float(df.loc[t].drop("y").values @ b)
    out = {"y": float(df.loc[t, "y"]), "yhat": yhat, "e": float(df.loc[t, "y"]) - yhat}
    out["hist30"] = float(np.mean(e_tr[-30:] ** 2))
    s2 = float(np.var(e_tr[:30]))
    for x in e_tr:                                   # RiskMetrics exponentially weighted moving average, lambda = 0.94
        s2 = 0.94 * s2 + 0.06 * x ** 2
    out["ewma"] = s2
    for nm, vol, o in [("garch", "GARCH", 0), ("gjr", "GARCH", 1), ("egarch", "EGARCH", 1)]:
        res = fit(e_tr, vol, o)
        out[nm] = float(res.forecast(horizon=1, reindex=False).variance.values[-1, 0])
        if nm == "garch":
            out["nu"] = float(res.params["nu"])
    return out


def qlike(proxy, h):
    x = proxy / h
    return x - np.log(x) - 1


def nw_var(x, lags=7):
    x = x - x.mean()
    n = len(x)
    v = x @ x / n
    for k in range(1, lags + 1):
        v += 2 * (1 - k / (lags + 1)) * (x[k:] @ x[:-k]) / n
    return v


def dm(la, lb, lags=7):
    """One-sided DM test: H1 = model b has lower expected loss than model a."""
    dl = np.asarray(la) - np.asarray(lb)
    st = dl.mean() / np.sqrt(nw_var(dl, lags) / len(dl))
    return st, 1 - stats.norm.cdf(st)


ROLL = {}
N["fc"] = {}
for u, y in [("pct", R_PCT["RO"]), ("eur", R_EUR["RO"])]:
    res = Parallel(n_jobs=-1)(delayed(one_day)(y.loc[START:END], t) for t in TDAYS)
    R = pd.DataFrame(res, index=TDAYS)
    ROLL[u] = R
    px = R["e"] ** 2
    L = {k: qlike(px, R[k]) for k in VMODELS}
    N["fc"][u] = {k: {"qlike": fl(L[k].mean(), 3), "mse": fl(((px - R[k]) ** 2).mean(), 0),
                      "dm_vs_garch": fl(dm(L["garch"], L[k])[0], 2) if k != "garch" else None,
                      "p_beats_hist": fl(dm(L["hist30"], L[k])[1], 3) if k != "hist30" else None} for k in VMODELS}
    N["fc"][u]["best"] = min(VMODELS, key=lambda k: N["fc"][u][k]["qlike"])
    N["fc"][u]["gain_garch_vs_hist"] = fl(100 * (1 - L["garch"].mean() / L["hist30"].mean()), 1)
    N["fc"][u]["gain_best_vs_hist"] = fl(100 * (1 - L[N["fc"][u]["best"]].mean() / L["hist30"].mean()), 1)
    N["fc"][u]["p_garch_vs_hist"] = fl(dm(L["hist30"], L["garch"])[1], 3)
    N["fc"][u]["p_garch_vs_ewma"] = fl(dm(L["ewma"], L["garch"])[1], 3)
    b_ = N["fc"][u]["best"]
    N["fc"][u]["p_best_vs_garch"] = fl(dm(L["garch"], L[b_])[1], 3) if b_ != "garch" else None
    # 90% one-day band from the GARCH-t forecast (standardised t quantile)
    nu = R["nu"]
    q = stats.t.ppf(0.95, nu) * np.sqrt((nu - 2) / nu)
    out_ = (R["e"].abs() > q * np.sqrt(R["garch"]))
    N["fc"][u]["band_out"] = int(out_.sum())
    N["fc"][u]["band_out_pct"] = fl(100 * out_.mean(), 1)
    qn = stats.norm.ppf(0.95)
    N["fc"][u]["band_out_hist"] = int((R["e"].abs() > qn * np.sqrt(R["hist30"])).sum())
    N["fc"][u]["band_out_hist_pct"] = fl(100 * (R["e"].abs() > qn * np.sqrt(R["hist30"])).mean(), 1)
N["fc"]["n"] = len(TDAYS)
# QLIKE punishes under-forecasting risk more than over-forecasting it: true sigma 20, forecasts 10 and 40
N["qex"] = {"under": fl(qlike(400.0, 100.0), 2), "over": fl(qlike(400.0, 1600.0), 2)}
N["qex"]["ratio"] = fl(N["qex"]["under"] / N["qex"]["over"], 1)
N["qex"]["mse_under"] = fl((400.0 - 100.0) ** 2, 0)
N["qex"]["mse_over"] = fl((400.0 - 1600.0) ** 2, 0)
# the "ghost" of a large shock in the 30-day historical variance: it leaves the window abruptly 30 days later
_R = ROLL["eur"]
_ts = _R["e"].abs().idxmax()
_k = _R.index.get_loc(_ts)
N["ghost"] = {"date": d(_ts), "shock": fl(_R["e"].loc[_ts], 1), "garch_before": fl(np.sqrt(_R["garch"].iloc[_k]), 1),
              "garch_after": fl(np.sqrt(_R["garch"].iloc[_k + 1]), 1), "hist_after": fl(np.sqrt(_R["hist30"].iloc[_k + 1]), 1),
              "garch_10": fl(np.sqrt(_R["garch"].iloc[_k + 10]), 1), "hist_10": fl(np.sqrt(_R["hist30"].iloc[_k + 10]), 1),
              "hist_30": fl(np.sqrt(_R["hist30"].iloc[_k + 30]), 1), "hist_31": fl(np.sqrt(_R["hist30"].iloc[_k + 31]), 1),
              "garch_30": fl(np.sqrt(_R["garch"].iloc[_k + 30]), 1)} if _k + 31 < len(_R) else None

# =============================================================================
# 9. Case study: autumn 2026. Term structure of the forecast at the cut-off; 2026 vs 2022
# =============================================================================
TS = {}
res = FITS[("eur", "garch_t")]
f = res.forecast(horizon=60, reindex=False).variance.values[-1]
p = res.params
lr = p["omega"] / (1 - p["alpha[1]"] - p["beta[1]"])
TS["eur"] = (f, lr)
N["ts"] = {"eur": {"s1": fl(np.sqrt(f[0]), 1), "s10": fl(np.sqrt(f[9]), 1), "s30": fl(np.sqrt(f[29]), 1), "s60": fl(np.sqrt(f[59]), 1),
                   "lr": fl(np.sqrt(lr), 1), "lim1": fl(stats.norm.ppf(0.95) * np.sqrt(f[0]), 0), "lim30": fl(stats.norm.ppf(0.95) * np.sqrt(f[29]), 0)}}
# Brent: returns are close to uncorrelated, so the h-day variance is the sum of the daily variance forecasts.
# Two forecast dates: the day of the highest 2026 conditional volatility (model estimated with data up to that day only) and the cut-off.
z95 = stats.norm.ppf(0.95)
_gb = fit(BRENT - BRENT.mean())
_cvb = pd.Series(_gb.conditional_volatility, index=BRENT.index) * np.sqrt(252)
BPEAK = _cvb.loc[str(END.year)].idxmax()
N["ts"]["brent"] = {}
for tag, t_end in [("peak", BPEAK), ("end", BRENT.index[-1])]:
    xb = BRENT.loc[:t_end]
    gb = fit(xb - xb.mean())
    fb = gb.forecast(horizon=60, reindex=False).variance.values[-1]
    pb = gb.params
    lrb = pb["omega"] / (1 - pb["alpha[1]"] - pb["beta[1]"])
    TS["brent_" + tag] = (fb, lrb)
    N["ts"]["brent"][tag] = {"date": d(t_end), "s1": fl(np.sqrt(fb[0]), 2), "lr": fl(np.sqrt(lrb), 2), "s1_ann": fl(np.sqrt(fb[0] * 252), 0),
                             "lr_ann": fl(np.sqrt(lrb * 252), 0), "band20": fl(z95 * np.sqrt(fb[:20].sum()), 1),
                             "band20_sqrt": fl(z95 * np.sqrt(20 * fb[0]), 1), "band20_lr": fl(z95 * np.sqrt(20 * lrb), 1)}
    N["ts"]["brent"][tag]["over"] = fl(100 * (np.sqrt(20 * fb[0]) / np.sqrt(fb[:20].sum()) - 1), 0)
N["case"] = {"p_last": fl(PR["RO"].iloc[-1], 1), "p_oct": fl(PR["RO"].loc[f"{END.year}-{END.month:02d}"].mean(), 1),
             "p_jan": fl(PR["RO"].loc[f"{END.year}-01"].mean(), 1)}
_mon = pd.DataFrame({"p": PR["RO"], "e": E_EUR.reindex(CAL), "r": E_PCT.reindex(CAL)}).resample("MS").agg({"p": "mean", "e": "std", "r": "std"})
_y26 = _mon.loc[f"{END.year}-01-01":]
_y22 = _mon.loc["2022-01-01":"2022-12-31"]
N["case"]["peak_month"] = _y26["p"].idxmax().strftime("%Y-%m")
N["case"]["peak_p"] = fl(_y26["p"].max(), 1)
N["case"]["peak_sd"] = fl(_y26["e"].max(), 1)
N["case"]["peak_sd_month"] = _y26["e"].idxmax().strftime("%Y-%m")
N["case"]["sd_22_max"] = fl(_y22["e"].max(), 1)
N["case"]["sd_22_max_month"] = _y22["e"].idxmax().strftime("%Y-%m")
N["case"]["p_22_max"] = fl(_y22["p"].max(), 1)
N["case"]["p_22_max_month"] = _y22["p"].idxmax().strftime("%Y-%m")
N["case"]["r_26_mean"] = fl(_y26["r"].mean(), 1)
N["case"]["r_22_mean"] = fl(_y22["r"].mean(), 1)
N["case"]["r_19_mean"] = fl(_mon.loc["2019"]["r"].mean(), 1)
N["case"]["e_26_mean"] = fl(_y26["e"].mean(), 1)
N["case"]["e_19_mean"] = fl(_mon.loc["2019"]["e"].mean(), 1)
_b = FU["brent_usd_bbl"]
N["case"]["brent_feb"] = fl(_b.loc[f"{END.year}-02"].mean(), 1)
N["case"]["brent_mar"] = fl(_b.loc[f"{END.year}-03"].mean(), 1)
N["case"]["brent_oct"] = fl(_b.loc[f"{END.year}-10"].mean(), 1)
N["case"]["ttf_feb"] = fl(TTF["ttf_eur_mwh"].loc[f"{END.year}-02"].iloc[0], 1)
N["case"]["ttf_oct"] = fl(TTF["ttf_eur_mwh"].loc[f"{END.year}-10"].iloc[0], 1)
# Brent GARCH-t conditional vol in 2026 vs 2025 (full-sample model)
N["case"]["brent_cv_2025"] = fl(_cvb.loc["2025"].mean(), 0)
N["case"]["brent_cv_2026max"] = fl(_cvb.loc[str(END.year)].max(), 0)
N["case"]["brent_cv_2026max_date"] = d(_cvb.loc[str(END.year)].idxmax())
# test-year band in EUR/MWh: share of days outside, by half-year
_R = ROLL["eur"]
_nu = _R["nu"]
_q = stats.t.ppf(0.95, _nu) * np.sqrt((_nu - 2) / _nu)
_out = (_R["e"].abs() > _q * np.sqrt(_R["garch"]))
N["case"]["band_out_first"] = fl(100 * _out.loc[:f"{END.year}-04-30"].mean(), 1)
N["case"]["band_out_last"] = fl(100 * _out.loc[f"{END.year}-05-01":].mean(), 1)
N["case"]["band_w_first"] = fl((_q * np.sqrt(_R["garch"])).loc[:f"{END.year}-04-30"].mean(), 0)
N["case"]["band_w_last"] = fl((_q * np.sqrt(_R["garch"])).loc[f"{END.year}-09-01":].mean(), 0)
N["case"]["band_w_last_hist"] = fl((stats.norm.ppf(0.95) * np.sqrt(_R["hist30"])).loc[f"{END.year}-09-01":].mean(), 0)

# =============================================================================
# 10. Case study C3 (research of our group): headline numbers computed by the case notebook (copied, not retyped)
# =============================================================================
with open(os.path.join(REPO, "cases", "C3_energy_stocks", "numbers.json")) as fh:
    N["c3"] = json.load(fh)

# =============================================================================
# Charts: one set per language
# =============================================================================
SRC = {"en": {"ec": "energy-charts.info (Fraunhofer ISE); OPCOM day-ahead prices for Romania, via ENTSO-E",
              "ecs": "energy-charts.info (Fraunhofer ISE); OPCOM prices; ENTSO-E solar generation (Transelectrica data for Romania)",
              "x": "energy-charts.info (OPCOM, via ENTSO-E); Yahoo Finance (Brent BZ=F, SparkChange EUA ETC); EODHD (BVB shares)",
              "own": "energy-charts.info (OPCOM, via ENTSO-E); own estimates"},
       "ro": {"ec": "energy-charts.info (Fraunhofer ISE); prețurile PZU (OPCOM), prin ENTSO-E",
              "ecs": "energy-charts.info (Fraunhofer ISE); prețuri OPCOM; producția solară ENTSO-E (date Transelectrica pentru România)",
              "x": "energy-charts.info (OPCOM, prin ENTSO-E); Yahoo Finance (Brent BZ=F, titlul SparkChange EUA ETC); EODHD (acțiuni BVB)",
              "own": "energy-charts.info (OPCOM, prin ENTSO-E); estimări proprii"}}


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


def out(fig, lang, name, bottom=0.17, also_x=()):
    comma_axes(fig, lang, also_x)
    os.makedirs(os.path.join(HERE, "charts", lang), exist_ok=True)
    save(fig, os.path.join(HERE, "charts", lang, name + ".pdf"), bottom=bottom)


def yfmt(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def mfmt(ax, lang, step=1):
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=step))
    M_ = MON_RO if lang == "ro" else MON_EN
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: M_[mdates.num2date(v).month - 1] +
                                               (f"\n{mdates.num2date(v).year}" if mdates.num2date(v).month == 1 or p == 0 else "")))


C_PCT, C_EUR = PAL["RO"], PAL["c7"]
C_MKT = {"RO": PAL["RO"], "HU": PAL["HU"], "EUA": PAL["c6"], "BRENT": PAL["c8"], "TTF": PAL["c5"], "SNP": "#8c6d31", "H2O": PAL["BG"]}
CRISIS = (pd.Timestamp("2021-09-01"), pd.Timestamp("2022-12-31"))
lab_m = {"hist30": ("30-day hist.", "istoric 30 zile"), "ewma": ("EWMA 0.94", "EWMA 0,94"), "garch": ("GARCH-t", "GARCH-t"),
         "gjr": ("GJR-t", "GJR-t"), "egarch": ("EGARCH-t", "EGARCH-t")}
for lang in ["en", "ro"]:
    T = (lambda en, ro: en) if lang == "en" else (lambda en, ro: ro)
    # 1 price and daily change
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.1), sharex=True, gridspec_kw={"height_ratios": [1, 1.2]})
    axs[0].plot(PR["RO"].index, PR["RO"].values, color=PAL["RO"], lw=0.6)
    axs[0].set_ylabel("EUR/MWh", fontsize=9.5)
    axs[1].plot(rr.index, rr.values, color=C_PCT, lw=0.35)
    axs[1].set_ylabel(T("change, %", "variația, %"), fontsize=9.5)
    for ax in axs:
        ax.axvspan(*CRISIS, color=PAL["c8"], alpha=0.08, lw=0)
    yfmt(axs[1])
    from matplotlib.patches import Patch
    legend_bottom(fig, handles=[plt.Line2D([], [], color=PAL["RO"], lw=1.2), plt.Line2D([], [], color=C_PCT, lw=0.6),
                                Patch(color=PAL["c8"], alpha=0.15)],
                  labels=[T("daily base price", "prețul de bază"), T("change $r_t$ (log, %)", "variația $r_t$ (log., %)"),
                          T("crisis: Sep 2021–Dec 2022", "criza: sep. 2021–dec. 2022")], ncol=3)
    for ax in axs:
        ax.yaxis.set_major_locator(MaxNLocator(3))
    out(fig, lang, "returns_ro", bottom=0.12)
    # 2 weekday calendar
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0), gridspec_kw={"width_ratios": [1.5, 1]})
    axs[0].bar(range(7), _dow.values, color=[PAL["c8"] if v < 0 else PAL["RO"] for v in _dow.values], width=0.65)
    axs[0].axhline(0, color="#222222", lw=0.6)
    axs[0].set_xticks(range(7))
    axs[0].set_xticklabels(DOWN[lang], fontsize=9)
    axs[0].set_ylabel(T("mean change, %", "variația medie, %"), fontsize=9)
    axs[1].bar([0, 1], [N["mean"]["sd_raw"], N["mean"]["sd_res"]], color=["#9a9a9a", C_PCT], width=0.55)
    axs[1].set_xticks([0, 1])
    axs[1].set_xticklabels([T("raw change", "variația brută"), T("after the mean\nequation", "după ecuația\nmediei")], fontsize=9)
    axs[1].set_ylabel(T("std. dev., %", "abaterea standard, %"), fontsize=9)
    out(fig, lang, "dow_effect", bottom=0.02)
    # 3 volatility in two units by year
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1))
    x = np.arange(len(YEARS))
    axs[0].bar(x, [N["voly"]["RO_pct_d"][str(y)] for y in YEARS], color=C_PCT, width=0.65)
    axs[0].set_ylabel("%", fontsize=9.5)
    axs[1].bar(x, [N["voly"]["RO_eur"][str(y)] for y in YEARS], color=C_EUR, width=0.65)
    axs[1].set_ylabel("EUR/MWh", fontsize=9.5)
    for ax in axs:
        ax.set_xticks(x)
        ax.set_xticklabels([str(y) for y in YEARS], fontsize=8.5, rotation=45, ha="right", rotation_mode="anchor")
    axs[0].set_title(T("std. dev. of the % shocks $\\varepsilon_t$", "abaterea standard, $\\varepsilon_t$ (%)"), fontsize=9.5)
    axs[1].set_title(T("std. dev. of the EUR/MWh shocks $u_t$", "abaterea standard, $u_t$ (EUR/MWh)"), fontsize=9.5)
    out(fig, lang, "vol_units", bottom=0.02)
    # 4 ACF of shocks and squared shocks
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0), sharey=True)
    K = 30
    ci = 1.96 / np.sqrt(len(E_PCT))
    for ax, s_, ttl in [(axs[0], E_PCT, T("shocks $\\varepsilon_t$", "șocurile $\\varepsilon_t$")),
                        (axs[1], E_PCT ** 2, T("squared shocks $\\varepsilon_t^2$", "pătratul șocurilor $\\varepsilon_t^2$"))]:
        a_ = acf(s_, nlags=K)[1:]
        ax.bar(range(1, K + 1), a_, color=C_PCT, width=0.6)
        ax.axhspan(-ci, ci, color="#9a9a9a", alpha=0.25, lw=0)
        ax.axhline(0, color="#222222", lw=0.5)
        ax.set_title(ttl, fontsize=10)
        ax.set_xlabel(T("lag (days)", "decalajul (zile)"), fontsize=9)
    axs[0].set_ylabel(T("autocorrelation", "autocorelația"), fontsize=9)
    legend_bottom(fig, handles=[Patch(color="#9a9a9a", alpha=0.4)], labels=[T("95% band if no autocorrelation", "banda de 95% în lipsa autocorelației")], ncol=1)
    out(fig, lang, "acf_clust", bottom=0.12)
    # 5 fat tails: density of standardised shocks, log scale
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    nu_ = G["pct"]["garch_t"]["nu"]
    zz = FITS[("pct", "garch_t")].std_resid
    bins = np.linspace(-8, 8, 65)
    hcount, edges = np.histogram(np.clip(zz, -8, 8), bins=bins, density=True)
    ax.bar(0.5 * (edges[1:] + edges[:-1]), hcount, width=edges[1] - edges[0], color=C_PCT, alpha=0.55, lw=0,
           label=T("standardised shocks, Romania", "șocuri standardizate, România"))
    xs = np.linspace(-8, 8, 400)
    ax.plot(xs, stats.norm.pdf(xs), color="#222222", lw=1.0, ls="--", label=T("normal", "normală"))
    sc = np.sqrt((nu_ - 2) / nu_)
    ax.plot(xs, stats.t.pdf(xs / sc, nu_) / sc, color=PAL["DE_LU"], lw=1.2, label=T(f"Student-t, $\\nu$ = {nu_:.1f}", f"Student-t, $\\nu$ = {nu_:.1f}".replace(".", ",")))
    ax.set_yscale("log")
    ax.set_ylim(1e-4, 1)
    ax.set_yticks([1e-4, 1e-2, 1])
    ax.set_yticklabels([T(s_, s_.replace(".", ",")) for s_ in ["0.0001", "0.01", "1"]])
    ax.minorticks_off()
    ax.set_xlabel(T("standardised shock $z_t$", "șocul standardizat $z_t$"), fontsize=9)
    ax.set_ylabel(T("density (log)", "densitatea (log)"), fontsize=9)
    ax._keep_y = True
    legend_bottom(fig, ncol=3)
    out(fig, lang, "tails", bottom=0.17, also_x=[ax])
    # 6 GARCH conditional volatility, two units
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.1), sharex=True)
    axs[0].plot(CV["pct"].index, CV["pct"].values, color=C_PCT, lw=0.6)
    axs[0].set_ylabel("%", fontsize=9.5)
    axs[1].plot(CV["eur"].index, CV["eur"].values, color=C_EUR, lw=0.6)
    axs[1].set_ylabel("EUR/MWh", fontsize=9.5)
    for ax in axs:
        ax.axvspan(*CRISIS, color=PAL["c8"], alpha=0.08, lw=0)
    yfmt(axs[1])
    legend_bottom(fig, handles=[plt.Line2D([], [], color=C_PCT), plt.Line2D([], [], color=C_EUR), Patch(color=PAL["c8"], alpha=0.15)],
                  labels=["GARCH-t $\\hat\\sigma_t$, %", "GARCH-t $\\hat\\sigma_t$, EUR/MWh",
                          T("energy crisis", "criza energetică")], ncol=3)
    for ax in axs:
        ax.yaxis.set_major_locator(MaxNLocator(3))
    out(fig, lang, "cond_vol", bottom=0.12)
    # 7 decay of a volatility shock (half-life)
    fig, ax = plt.subplots(figsize=(6.4, 2.1))
    hh = np.arange(0, 121)
    for k, lab_, c_ in [("RO_pct", T("Romania, %", "România, %"), C_PCT), ("RO_eur", T("Romania, EUR/MWh", "România, EUR/MWh"), C_EUR),
                        ("BRENT", "Brent", C_MKT["BRENT"]), ("EUA", "EUA", C_MKT["EUA"]), ("SNP", "OMV Petrom", C_MKT["SNP"])]:
        ph = N["xm"][k]["pers"]
        ax.plot(hh, 100 * ph ** hh, color=c_, lw=1.3, label=lab_ + f" ({fl(N['xm'][k]['hl'], 1)})".replace(".", "," if lang == "ro" else "."))
    ax.axhline(50, color="#222222", lw=0.6, ls=":")
    ax.set_xlabel(T("days after the shock (trading days for markets, calendar days for power)",
                    "zile după șoc (zile de tranzacționare pentru piețe, zile calendaristice pentru energie)"), fontsize=9)
    ax.set_ylabel(T("% left", "% rămas"), fontsize=9)
    ax.set_xlim(0, 120)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "halflife", bottom=0.26)
    # 8 news impact curves
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1))
    for ax, u, c_, xl in [(axs[0], "pct", C_PCT, T("shock $\\varepsilon_{t-1}$, %", "șocul $\\varepsilon_{t-1}$, %")),
                          (axs[1], "eur", C_EUR, T("shock $u_{t-1}$, EUR/MWh", "șocul $u_{t-1}$, EUR/MWh"))]:
        x_, s_, sd_ = NIC[u]
        ax.plot(x_[x_ < 0], s_[x_ < 0], color=PAL["c8"], lw=1.5)
        ax.plot(x_[x_ >= 0], s_[x_ >= 0], color=PAL["HU"], lw=1.5)
        ax.set_xlabel(xl, fontsize=9)
    axs[0].set_ylabel(T("next-day $\\sigma_t$", "$\\sigma_t$ de mîine"), fontsize=9)
    axs[0].set_title(T("percent", "în procente"), fontsize=9.5)
    axs[1].set_title("EUR/MWh", fontsize=9.5)
    legend_bottom(fig, handles=[plt.Line2D([], [], color=PAL["c8"], lw=1.5), plt.Line2D([], [], color=PAL["HU"], lw=1.5)],
                  labels=[T("price fell yesterday", "prețul a scăzut ieri"), T("price rose yesterday", "prețul a crescut ieri")], ncol=2)
    out(fig, lang, "nic", bottom=0.15, also_x=list(axs))
    # 9 volatility vs price level (monthly)
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    yrs = _m.index.year
    for y in YEARS:
        msk = yrs == y
        ax.scatter(_m["lvl"][msk], _m["sd"][msk], s=14, color=ep.SERIES[(y - START.year) % 8], label=str(y), lw=0)
    xx = np.linspace(_m["lvl"].min(), _m["lvl"].max(), 50)
    ax.plot(xx, np.exp(_ll.params.iloc[0]) * xx ** _ll.params.iloc[1], color="#222222", lw=0.9, ls="--",
            label=T("log-log fit", "dreapta log-log"))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks([30, 50, 100, 200, 400])
    ax.set_xticklabels(["30", "50", "100", "200", "400"])
    ax.set_yticks([5, 10, 20, 50, 100])
    ax.set_yticklabels(["5", "10", "20", "50", "100"])
    ax.minorticks_off()
    ax.set_xlabel(T("monthly mean price, EUR/MWh (log scale)", "prețul mediu lunar, EUR/MWh (scară log.)"), fontsize=9)
    ax.set_ylabel(T("monthly $\\hat\\sigma(u)$,\nEUR/MWh", "$\\hat\\sigma(u)$ lunar,\nEUR/MWh"), fontsize=9)
    fig.legend(*ax.get_legend_handles_labels(), loc="lower center", ncol=9, bbox_to_anchor=(0.5, 0.0), frameon=False,
               fontsize=9.5, handlelength=1.0, columnspacing=0.8, handletextpad=0.2, markerscale=1.3)
    out(fig, lang, "vol_level", bottom=0.12)
    # 10 Markov-switching regime probability
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.1), sharex=True, gridspec_kw={"height_ratios": [1, 1]})
    axs[0].plot(PR["RO"].index, PR["RO"].values, color=PAL["RO"], lw=0.6)
    axs[0].set_ylabel("EUR/MWh", fontsize=9.5)
    axs[1].fill_between(_ph.index, 0, _ph.values, color=C_EUR, alpha=0.6, lw=0)
    axs[1].set_ylabel(T("prob.", "prob."), fontsize=9.5)
    axs[1].set_ylim(0, 1)
    axs[1].set_yticks([0, 0.5, 1])
    axs[0].yaxis.set_major_locator(MaxNLocator(3))
    yfmt(axs[1])
    legend_bottom(fig, handles=[plt.Line2D([], [], color=PAL["RO"]), Patch(color=C_EUR, alpha=0.6)],
                  labels=[T("daily base price", "prețul zilnic de bază"), T("probability of the turbulent regime (smoothed)", "probabilitatea regimului agitat (netezită)")], ncol=2)
    out(fig, lang, "ms_regime", bottom=0.12)
    # 11 intraday variation vs solar
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.1), sharex=True)
    rm = RV["rel"].resample("MS").median()
    axs[0].plot(rm.index, rm.values, color=PAL["RO"], lw=1.2)
    axs[0].set_ylabel(T("RV / price", "RV / preț"), fontsize=9.5)
    sm_ = SOL.resample("MS").mean()
    axs[1].plot(sm_.index, sm_.values, color=PAL["BG"], lw=1.2)
    axs[1].set_ylabel(T("solar, MW", "solar, MW"), fontsize=9.5)
    yfmt(axs[1])
    legend_bottom(fig, handles=[plt.Line2D([], [], color=PAL["RO"], lw=1.2), plt.Line2D([], [], color=PAL["BG"], lw=1.2)],
                  labels=[T("RV / daily price (monthly median)", "RV / prețul zilei (mediana lunară)"),
                          T("solar output (monthly mean)", "producția solară (media lunară)")], ncol=2)
    for ax in axs:
        ax.yaxis.set_major_locator(MaxNLocator(3))
    out(fig, lang, "rv_solar", bottom=0.12)
    # 12 HAR forecast on the test year
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    ax.plot(_act.index, _act.values, color="#9a9a9a", lw=0.7, label=T("realised intraday variation $RV_d$", "variația intrazilnică realizată $RV_d$"))
    ax.plot(HARF.index, HARF.values, color=PAL["RO"], lw=1.1, label=T("HAR forecast made on $d-1$", "prognoza HAR făcută în ziua $d-1$"))
    ax.set_ylabel("EUR/MWh", fontsize=9.5)
    mfmt(ax, lang, 2)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "har_fc", bottom=0.2)
    # 13 test-year forecast vs realised absolute shock (EUR)
    R = ROLL["eur"]
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    ax.bar(R.index, R["e"].abs(), color="#b5b5b5", width=1.0, label=T("realised $|u_t|$", "$|u_t|$ realizat"))
    ax.plot(R.index, np.sqrt(R["garch"]), color=C_EUR, lw=1.2, label=T("GARCH-t $\\hat\\sigma_t$, forecast on $t-1$", "GARCH-t $\\hat\\sigma_t$, prognoză din $t-1$"))
    ax.plot(R.index, np.sqrt(R["hist30"]), color=PAL["BG"], lw=1.0, ls="--", label=T("30-day historical", "istoric 30 de zile"))
    ax.set_ylabel("EUR/MWh", fontsize=9.5)
    mfmt(ax, lang, 2)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "fc_test", bottom=0.2)
    # 14 case: one-day 90% band in EUR/MWh on the test year
    fig, ax = plt.subplots(figsize=(6.4, 2.1))
    pm_ = PR["RO"].shift(1).loc[TDAYS] + R["yhat"]
    w_ = _q * np.sqrt(R["garch"])
    ax.fill_between(TDAYS, pm_ - w_, pm_ + w_, color=C_EUR, alpha=0.25, lw=0, label=T("90% GARCH-t band (set on $t-1$)", "banda GARCH-t de 90% (din $t-1$)"))
    ax.plot(TDAYS, PR["RO"].loc[TDAYS], color=PAL["RO"], lw=0.8, label=T("base price", "prețul de bază"))
    oo = _out[_out]
    ax.scatter(oo.index, PR["RO"].loc[oo.index], s=9, color=PAL["c8"], zorder=3, label=T("outside the band", "în afara benzii"))
    ax.set_ylabel("EUR/MWh", fontsize=9.5)
    mfmt(ax, lang, 2)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "case_band", bottom=0.13)
    # 15 case: term structure at the cut-off
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1))
    h_ = np.arange(1, 61)
    f_, lr_ = TS["eur"]
    axs[0].plot(h_, np.sqrt(f_), color=C_EUR, lw=1.4, label=T("GARCH-t forecast, Romania", "prognoza GARCH-t, România"))
    axs[0].axhline(np.sqrt(lr_), color="#222222", lw=0.8, ls="--", label=T("long-run level", "nivelul de lungă durată"))
    axs[0].set_xlabel(T("days ahead $h$", "zile înainte, $h$"), fontsize=9)
    axs[0].set_ylabel("EUR/MWh", fontsize=9)
    axs[0].set_ylim(0, 1.25 * np.sqrt(lr_))
    axs[0].set_title(T("Romania: daily $\\sigma$ forecast", "România: $\\sigma$ zilnic prognozat"), fontsize=9.5)
    hb = np.arange(1, 41)
    fb_, lrb_ = TS["brent_peak"]
    z95 = stats.norm.ppf(0.95)
    axs[1].plot(hb, z95 * np.sqrt(np.cumsum(fb_[:40])), color=C_MKT["BRENT"], lw=1.4, label=T("GARCH-t band, Brent", "banda GARCH-t, Brent"))
    axs[1].plot(hb, z95 * np.sqrt(hb * fb_[0]), color=PAL["BG"], lw=1.1, ls="-.", label=T("today's $\\sigma\\times\\sqrt{h}$", "$\\sigma$ de azi $\\times\\sqrt{h}$"))
    axs[1].plot(hb, z95 * np.sqrt(hb * lrb_), color="#222222", lw=0.8, ls="--")
    axs[1].set_xlabel(T("horizon $h$ (trading days)", "orizontul $h$ (zile de tranzacționare)"), fontsize=9)
    axs[1].set_ylabel("$\\pm$%", fontsize=9)
    axs[1].set_title(T(f"Brent, {MON_EN[BPEAK.month - 1]} {BPEAK.day}, {BPEAK.year}: 90% band over $h$ days",
                       f"Brent, {BPEAK.day} {MON_RO[BPEAK.month - 1]} {BPEAK.year}: banda de 90% pe $h$ zile"), fontsize=9.5)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "term_structure", bottom=0.27)

ped, prd = f"{d(TEST0)} to {d(END)}", f"{d(TEST0)} - {d(END)}"
pe, pr_ = f"{d(START)} to {d(END)}", f"{d(START)} - {d(END)}"
chart("returns_ro", "ec", f"daily, {pe}, CET delivery days", f"date zilnice, {pr_}, zile de livrare CET")
chart("dow_effect", "ec", f"daily, {pe}", f"date zilnice, {pr_}")
chart("vol_units", "ec", f"residuals of the mean equation, {pe}", f"reziduurile ecuației mediei, {pr_}")
chart("acf_clust", "ec", f"residuals of the mean equation, {pe}", f"reziduurile ecuației mediei, {pr_}")
chart("tails", "own", f"GARCH(1,1)-t on percent changes, {pe}", f"GARCH(1,1)-t pe variațiile procentuale, {pr_}")
chart("cond_vol", "own", f"GARCH(1,1)-t, {pe}", f"GARCH(1,1)-t, {pr_}")
chart("halflife", "x", "GARCH(1,1)-t, each series over its own sample (table on the slide)",
      "GARCH(1,1)-t, fiecare serie pe propriul eșantion (tabelul de pe diapozitiv)")
chart("nic", "own", f"GJR(1,1)-t, {pe}", f"GJR(1,1)-t, {pr_}")
chart("vol_level", "ec", f"monthly, {pe}", f"date lunare, {pr_}")
chart("ms_regime", "own", f"two-regime Markov-switching model on EUR/MWh shocks, {pe}", f"model Markov cu două regimuri, pe șocurile în EUR/MWh, {pr_}")
chart("rv_solar", "ecs", f"hourly prices, monthly values, {pe}", f"prețuri orare, valori lunare, {pr_}")
chart("har_fc", "ec", f"test year {ped}; HAR re-estimated daily", f"anul de test {prd}; HAR reestimat zilnic")
chart("fc_test", "own", f"test year {ped}; models re-estimated daily", f"anul de test {prd}; modele reestimate zilnic")
chart("case_band", "own", f"test year {ped}", f"anul de test {prd}")
chart("term_structure", "x", f"GARCH(1,1)-t forecasts made with data up to {d(END)}", f"prognoze GARCH(1,1)-t făcute cu datele pînă la {d(END)}")

with open(os.path.join(HERE, "L3_numbers.json"), "w") as fh:
    json.dump(N, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("wrote L3_numbers.json and", len(N["charts"]), "charts x 2 languages")
