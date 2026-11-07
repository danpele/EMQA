"""
analysis_L1.py -- Lecture 1 "Energy markets and their data" (EMQA)
===================================================================
Reads the real series in repo/data/clean (see data/SOURCES.md), computes every number shown on the
slides and writes
    lectures/L1/L1_numbers.json        all results (the deck builder reads ONLY this file)
    lectures/L1/charts/en/*.pdf        figures with English labels
    lectures/L1/charts/ro/*.pdf        the same figures with Romanian labels
Run:  python3 lectures/L1/analysis_L1.py

Conventions
  * Data cut-off = last complete calendar month common to prices and generation.
  * Energy = sum over reported hourly intervals of mean MW x 1 h; coverage (share of hours reported) is
    stored next to every total. Missing values are never treated as zero and never interpolated.
  * Counts of events (negative prices, spikes) are in hour-equivalents: a 15-min MTU counts 0.25 h.
    Quantiles and means over mixed 60/15-min periods are duration-weighted.
  * Daily differences are taken on the full calendar, so a gap gives a missing change (no multi-day jumps).
  * The only simulated series is the white-noise / AR(1) / random-walk illustration (fixed seed).
"""

import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.seasonal import STL, seasonal_decompose
from statsmodels.tsa.stattools import acf, adfuller, kpss, pacf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
import emqa_plot as ep  # noqa: E402
from emqa_plot import PAL, ZONE_LS, legend_bottom, save  # noqa: E402

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

warnings.filterwarnings("ignore")
ep.style()
N = {"charts": {}}
ZONES = ["RO", "BG", "HU", "DE_LU"]
ZL = {"RO": "RO", "BG": "BG", "HU": "HU", "DE_LU": "DE-LU"}
MON_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MON_RO = ["ian.", "feb.", "mar.", "apr.", "mai", "iun.", "iul.", "aug.", "sep.", "oct.", "nov.", "dec."]


def d(ts):
    return pd.Timestamp(ts).strftime("%Y-%m-%d")


def fl(x, k=4):
    if x is None:
        return None
    x = float(x)
    return None if np.isnan(x) else round(x, k)


def wquantile(x, w, q):
    """Duration-weighted quantile."""
    o = np.argsort(x)
    x, w = np.asarray(x)[o], np.asarray(w)[o]
    c = (np.cumsum(w) - 0.5 * w) / w.sum()
    return float(np.interp(q, c, x))


# =============================================================================
# 0. Load data and cut-off
# =============================================================================
P = ep.prices_daily()
X = ep.prices_native()          # native MTU prices, CET/CEST index
H = ep.prices_hourly()          # hourly (15-min averaged to the hour after Oct 2025), CET/CEST index
G = ep.generation_ro_daily()
GH = ep.generation_ro_hourly()  # hourly UTC, mean MW per hour
BGH = ep.generation_bg_hourly()
CB = ep.crossborder_ro_daily()
F = ep.fuels_daily()
TTF = ep.ttf_monthly()

_raw_last = min(P["RO"].dropna().index.max(), G["hydro_run_of_river"].dropna().index.max())
END = pd.Timestamp(((_raw_last + pd.Timedelta(days=1)).to_period("M").to_timestamp() - pd.Timedelta(days=1)).date())
Y = END.year
N["cutoff"] = {"end": d(END), "raw_price_last": d(P["RO"].dropna().index.max()),
               "raw_gen_last": d(G["hydro_run_of_river"].dropna().index.max()), "year": Y, "month": int(END.month)}
END_UTC = (pd.Timestamp(END.date()) + pd.Timedelta(days=1)).tz_localize("Europe/Brussels").tz_convert("UTC")
P, G, CB, F, TTF = P.loc[:END], G.loc[:END], CB.loc[:END], F.loc[:END], TTF.loc[:END]
X, H = X.loc[:str(END.date())], H.loc[:str(END.date())]
GH, BGH = GH.loc[GH.index < END_UTC], BGH.loc[BGH.index < END_UTC]
N["data"] = {"price_first": d(P["RO"].dropna().index.min()), "bg_first": d(P["BG"].dropna().index.min()),
             "brent_first": d(F["brent_usd_bbl"].dropna().index.min()), "download": "2026-11-04",
             "n_mtu_15": int((X["mtu_minutes"] == 15).sum()), "n_mtu_60": int((X["mtu_minutes"] == 60).sum())}
PF = P.asfreq("D")              # full calendar: gaps stay NaN, differences across gaps are missing
# OPCOM aggregated PZU curves (real order book, one day): the merit order and the clearing price
_CDIR = os.path.join(HERE, "..", "..", "data", "clean")
CURVES = pd.read_csv(os.path.join(_CDIR, "opcom_pzu_curves.csv"))
with open(os.path.join(_CDIR, "opcom_pzu_curves_meta.json")) as _f:
    CMETA = json.load(_f)
N["merit"] = {"day": CURVES["delivery_date"].iloc[0]}
for _iv in CMETA["intervals"]:
    _k = "mid" if _iv["opcom_interval"] == 45 else "eve"
    _lab = _iv["interval_label"]
    _s = CURVES[(CURVES["interval"] == _lab) & (CURVES["side"] == "supply")]
    _p, _q = _iv["official_clearing_price_eur_mwh"], _iv["curve_cleared_quantity_mw"]
    # price the supply curve asks for 100 MW more than the cleared quantity (steepness near the crossing)
    _up = _s.loc[_s["quantity_mw"] >= _q + 100, "price_eur_mwh"].min()
    N["merit"][_k] = {"label": _lab, "price": _p, "q": _q,
                      "q_le0": fl(_s.loc[_s["price_eur_mwh"] <= 0, "quantity_mw"].max(), 0),
                      "p_plus100": fl(_up, 0), "net_imp": fl(-_iv["net_export_mw"], 0),
                      "n_sup": int(len(_s)), "n_dem": int(((CURVES["interval"] == _lab) & (CURVES["side"] == "demand")).sum())}
# one day of Romanian load: most recent Wednesday (CET) with all 24 hours reported -> power (MW) vs energy (MWh)
_ld = GH["load"].tz_convert("Europe/Brussels")
_cnt = _ld.groupby(_ld.index.date).count()
_wed = [k for k, v in _cnt.items() if v == 24 and pd.Timestamp(k).dayofweek == 2]
DAYLOAD_DAY = max(_wed)
DAYLOAD = _ld[_ld.index.date == DAYLOAD_DAY]
N["dayload"] = {"day": str(DAYLOAD_DAY), "mwh": int(round(DAYLOAD.sum())), "mean_mw": int(round(DAYLOAD.mean())),
                "max_mw": int(round(DAYLOAD.max())), "min_mw": int(round(DAYLOAD.min())),
                "max_h": int(DAYLOAD.idxmax().hour), "min_h": int(DAYLOAD.idxmin().hour)}
_ro = PF["RO"].loc[PF["RO"].first_valid_index():]
_bg = PF["BG"].loc[PF["BG"].first_valid_index():]
N["data"]["ro_missing"] = [d(x) for x in _ro[_ro.isna()].index]
N["data"]["ro_missing_n"] = int(_ro.isna().sum())
N["data"]["bg_missing_n"] = int(_bg.isna().sum())
N["data"]["bg_missing_last"] = d(_bg[_bg.isna()].index.max())

# =============================================================================
# 1. Romanian generation mix: energy from reported hours, with coverage
# =============================================================================
GRP = {"Hydro": ["hydro_run_of_river", "hydro_water_reservoir"], "Coal": ["brown_coal_lignite", "hard_coal"],
       "Nuclear": ["nuclear"], "Gas": ["gas"], "Wind": ["wind_onshore"], "Solar": ["solar"], "Biomass": ["biomass"]}
yr = GH.index.year
full_years = [y for y in sorted(set(yr)) if y < Y]
mix, cov = {}, {}
for k, cols_ in GRP.items():
    s_ = GH[cols_].sum(axis=1, min_count=len(cols_))          # a group is reported only if all its parts are
    mix[k] = s_.groupby(yr).sum() / 1e6
    cov[k] = s_.notna().groupby(yr).mean()
mix, cov = pd.DataFrame(mix), pd.DataFrame(cov)
load_twh = GH["load"].groupby(yr).sum() / 1e6
imp_twh = (CB["sum"] * 24 / 1e6).groupby(CB.index.year).sum()   # cross-border: daily means, all days reported
share = mix.div(mix.sum(axis=1), axis=0) * 100
N["mix"] = {"first": full_years[0], "last": full_years[-1], "min_cov_full": fl(cov.loc[full_years].min().min() * 100, 1)}
for y in full_years:
    e = {k: {"twh": fl(mix.loc[y, k], 2), "share": fl(share.loc[y, k], 1), "cov": fl(cov.loc[y, k] * 100, 1)} for k in GRP}
    e.update({"total_twh": fl(mix.loc[y].sum(), 2), "load_twh": fl(load_twh.loc[y], 2), "netimp_twh": fl(imp_twh.loc[y], 2)})
    N["mix"][str(y)] = e
N["mix"]["coal_change_pct"] = fl((mix.loc[full_years[-1], "Coal"] / mix.loc[full_years[0], "Coal"] - 1) * 100, 1)
N["mix"]["solar_x"] = fl(mix.loc[full_years[-1], "Solar"] / mix.loc[full_years[0], "Solar"], 1)


def lfl_block(cols_, y0, y1):
    """Jan..cut-off month of y1 vs the same months of y0, over hours reported in BOTH years."""
    s_ = GH[cols_].sum(axis=1, min_count=len(cols_))
    a = s_[(s_.index.year == y1) & (s_.index.month <= END.month)]
    b_ = s_[(s_.index.year == y0) & (s_.index.month <= END.month)]
    A = pd.Series(a.values, index=a.index.strftime("%m-%d %H"))
    B = pd.Series(b_.values, index=b_.index.strftime("%m-%d %H"))
    A, B = A[~A.index.duplicated()], B[~B.index.duplicated()]
    j = pd.concat([A.rename("a"), B.rename("b")], axis=1)
    both = j.dropna()
    return {"ytd": fl(both["a"].sum() / 1e6, 2), "prev": fl(both["b"].sum() / 1e6, 2),
            "chg": fl((both["a"].sum() / both["b"].sum() - 1) * 100, 1), "cov": fl(len(both) / len(j) * 100, 1),
            "cov_own": fl(A.notna().mean() * 100, 1), "ytd_own": fl(A.sum() / 1e6, 2)}


L = {k: lfl_block(c_, Y - 1, Y) for k, c_ in GRP.items()}
L["load"] = lfl_block(["load"], Y - 1, Y)
tot_a, tot_b = sum(L[k]["ytd"] for k in GRP), sum(L[k]["prev"] for k in GRP)
for k in GRP:
    L[k]["share_ytd"] = fl(L[k]["ytd"] / tot_a * 100, 1)
    L[k]["share_prev"] = fl(L[k]["prev"] / tot_b * 100, 1)
N["mix"]["lfl"] = L
N["mix"]["lfl_tot"] = {"ytd": fl(tot_a, 2), "prev": fl(tot_b, 2)}
imp_d = CB["sum"] * 24 / 1e6
N["mix"]["lfl_imp"] = {"ytd": fl(imp_d.loc[str(Y)].sum(), 2), "prev": fl(imp_d.loc[f"{Y - 1}-01-01":f"{Y - 1}-{END:%m-%d}"].sum(), 2)}
nu = GH["nuclear"].loc[str(Y)]
N["nuclear"] = {MON_EN[m - 1]: {"mw": fl(g_.mean(), 0), "cov": fl(g_.notna().mean() * 100, 0)} for m, g_ in nu.groupby(nu.index.month)}
gn = G.loc[str(Y), "nuclear"]
N["nuclear"]["missing_days"] = int(gn.isna().sum())
N["nuclear"]["first_missing"] = d(gn[gn.isna()].index.min())
N["nuclear"]["last_missing"] = d(gn[gn.isna()].index.max())
N["nuclear"]["first_zero"] = d(gn[gn < 1].index.min())
N["nuclear"]["zero_days_aug"] = int((G.loc[f"{Y}-08", "nuclear"] < 1).sum())
N["nuclear"]["zero_days_oct"] = int((G.loc[f"{Y}-10", "nuclear"] < 1).sum())
gm = G.loc[f"{Y}-05", "nuclear"]
N["nuclear"]["may_zero_days"] = int((gm < 1).sum())
N["nuclear"]["may_zero_first"] = d(gm[gm < 1].index.min())
N["nuclear"]["may_zero_last"] = d(gm[gm < 1].index.max())
hyd_d = G["hydro_run_of_river"] + G["hydro_water_reservoir"]
hm_ = hyd_d.resample("MS").mean()
cmp_ = {m: (hm_.loc[f"{Y}-{m:02d}"].iloc[0], hm_.loc[f"{Y - 1}-{m:02d}"].iloc[0]) for m in range(1, END.month + 1)}
N["nuclear"]["hydro_jul_up"] = bool(cmp_[7][0] > cmp_[7][1])
N["nuclear"]["hydro_below_from"] = MON_EN[min(m for m in range(7, END.month + 1) if all(cmp_[k][0] < cmp_[k][1] for k in range(m, END.month + 1))) - 1]
N["nuclear"]["hydro_aug_oct_chg"] = fl((sum(cmp_[m][0] for m in range(8, END.month + 1)) / sum(cmp_[m][1] for m in range(8, END.month + 1)) - 1) * 100, 1)

# =============================================================================
# 2. Daily prices: statistics, by year
# =============================================================================
stat = {}
for z in ZONES:
    s = P[z].dropna()
    ds = PF[z].diff().dropna()
    stat[z] = {"n": int(len(s)), "mean": fl(s.mean(), 2), "median": fl(s.median(), 2), "sd": fl(s.std(), 2),
               "skew": fl(stats.skew(s), 2), "exkurt": fl(stats.kurtosis(s), 2), "min": fl(s.min(), 2),
               "max": fl(s.max(), 2), "max_date": d(s.idxmax()), "d_sd": fl(ds.std(), 2),
               "d_exkurt": fl(stats.kurtosis(ds), 2), "d_jb": fl(stats.jarque_bera(ds).statistic, 0)}
N["stats"] = stat
N["byyear"] = {}
for z in ZONES:
    s = P[z].dropna()
    ds = PF[z].diff()
    N["byyear"][z] = {str(y): {"mean": fl(g_.mean(), 1), "sd_d": fl(ds.loc[g_.index].std(), 1)} for y, g_ in s.groupby(s.index.year)}

# =============================================================================
# 3. Seasonality
# =============================================================================
hh = H.copy()
hh["hour"] = hh.index.hour
prof = {y: hh.loc[str(y)].groupby("hour")[["RO", "DE_LU"]].mean() for y in [2019, 2025]}
N["season"] = {"intraday": {}}
for y in prof:
    for z in ["RO", "DE_LU"]:
        pr = prof[y][z]
        N["season"]["intraday"][f"{z}_{y}"] = {"min_h": int(pr.idxmin()), "min": fl(pr.min(), 1), "max_h": int(pr.idxmax()),
                                               "max": fl(pr.max(), 1), "ratio_19_13": fl(pr.loc[19] / pr.loc[13], 2)}
wk = P.loc["2023-01-01":, ["RO", "DE_LU"]].dropna().copy()
iso = wk.index.isocalendar()
key = iso["year"].astype(str) + "-" + iso["week"].astype(str)
full = (key.map(key.value_counts()) == 7).values
wk, key = wk[full], key[full]
dow = (wk - wk.groupby(key.values).transform("mean")).groupby(wk.index.dayofweek).mean()
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
N["season"]["weekly"] = {z: {DAYS[i]: fl(dow.loc[i, z], 1) for i in range(7)} for z in ["RO", "DE_LU"]}
N["season"]["weekly"].update({"start": d(wk.index.min()), "end": d(wk.index.max()), "n_weeks": int(len(set(key)))})
mm = G.loc["2016":str(full_years[-1])].resample("MS").mean()
pm = P["RO"].loc["2016":str(full_years[-1])].resample("MS").mean()
ratio = pm / pm.groupby(pm.index.year).transform("mean")
mprof = pd.DataFrame({"load": mm["load"].groupby(mm.index.month).mean() / 1000,
                      "hydro": (mm["hydro_run_of_river"] + mm["hydro_water_reservoir"]).groupby(mm.index.month).mean() / 1000,
                      "solar": mm["solar"].groupby(mm.index.month).mean() / 1000,
                      "price_ratio": ratio.groupby(ratio.index.month).median()})
N["season"]["annual"] = {"load_max_m": int(mprof["load"].idxmax()), "load_min_m": int(mprof["load"].idxmin()),
                         "hydro_max_m": int(mprof["hydro"].idxmax()), "price_max_m": int(mprof["price_ratio"].idxmax()),
                         "price_max": fl(mprof["price_ratio"].max(), 2), "price_min_m": int(mprof["price_ratio"].idxmin()),
                         "price_min": fl(mprof["price_ratio"].min(), 2)}

# =============================================================================
# 4. Negative prices and spikes (hour-equivalents; duration-weighted quantiles)
# =============================================================================
hrs = X["mtu_minutes"] / 60.0
N["neg"] = {"hours": {}, "n_mtu": {}, "lfl_prev": {}}
for z in ZONES:
    m_ = X[z].notna()
    N["neg"]["hours"][z] = {str(y): fl(v, 2) for y, v in ((X[z] < 0) & m_).mul(hrs).groupby(X.index.year).sum().items()}
    N["neg"]["n_mtu"][z] = {str(y): int(v) for y, v in ((X[z] < 0) & m_).groupby(X.index.year).sum().items()}
    ly = X.loc[f"{Y - 1}-01-01":f"{Y - 1}-{END:%m-%d}"]
    N["neg"]["lfl_prev"][z] = fl(((ly[z] < 0) & ly[z].notna()).mul(ly["mtu_minutes"] / 60).sum(), 2)
ro = X["RO"].dropna()
N["neg"]["ro_first"] = d(ro[ro < 0].index.min())
r24 = X.loc["2024-01-01":, ["RO", "mtu_minutes"]].dropna()
negh = (r24["RO"] < 0) * r24["mtu_minutes"] / 60
hneg = negh.groupby(r24.index.hour).sum()
N["neg"]["ro_share_10_16"] = fl(hneg.loc[10:15].sum() / hneg.sum() * 100, 1)
N["neg"]["ro_share_weekend"] = fl(negh[r24.index.dayofweek >= 5].sum() / negh.sum() * 100, 1)
hm = ((X["RO"] < 0) & X["RO"].notna()).mul(hrs).loc["2023-01-01":]
hm = hm.groupby([hm.index.year, hm.index.month]).sum().unstack(0)
N["neg"]["share_apr_may"] = fl(hm.loc[[4, 5]].sum().sum() / hm.sum().sum() * 100, 1)
N["neg"]["share_jun_aug"] = fl(hm.loc[[6, 7, 8]].sum().sum() / hm.sum().sum() * 100, 1)
N["neg"]["solar_twh"] = {str(y): fl(mix.loc[y, "Solar"], 2) for y in full_years}

# logit: day with >= 1 negative RO MTU on REALISED fundamentals + weekend + year effects (descriptive, not a bidding model)
nd = ((X["RO"] < 0) & X["RO"].notna()).groupby(X.index.normalize().tz_localize(None)).max().astype(float)
jj = pd.concat([nd.rename("neg"), (G["solar"] / 1000).rename("solar"), (G["wind_onshore"] / 1000).rename("wind"),
                ((G["hydro_run_of_river"] + G["hydro_water_reservoir"]) / 1000).rename("hydro"),
                (G["load"] / 1000).rename("load")], axis=1).loc["2024-01-01":].dropna()
jj["wkend"] = (jj.index.dayofweek >= 5).astype(float)
for y in sorted(set(jj.index.year))[1:]:
    jj[f"y{y}"] = (jj.index.year == y).astype(float)
jj["resid"] = jj["load"] - jj["solar"] - jj["wind"]          # residual load: demand left after wind and solar (GW)
# (month dummies are not used: several months never have a negative price, which makes the logit separate)
xc = ["resid", "hydro", "wkend"] + [c for c in jj.columns if c.startswith("y")]
lp = sm.Logit(jj["neg"], sm.add_constant(jj[xc])).fit(disp=0)
N["logit"] = {"n": int(len(jj)), "start": d(jj.index.min()), "end": d(jj.index.max()), "n_neg": int(jj["neg"].sum()),
              "pr2": fl(lp.prsquared, 3), "base_year": int(jj.index.year.min()),
              "coef": {k: {"b": fl(lp.params[k], 3), "z": fl(lp.tvalues[k], 2), "p": fl(lp.pvalues[k], 4),
                           "or": fl(np.exp(lp.params[k]), 2)} for k in lp.params.index}}

sp = {}
for z in ["RO", "DE_LU"]:
    s = X[[z, "mtu_minutes"]].dropna()
    out_ = {}
    for y, g_ in s.groupby(s.index.year):
        w = g_["mtu_minutes"].values / 60
        q1, q3 = wquantile(g_[z].values, w, 0.25), wquantile(g_[z].values, w, 0.75)
        thr = q3 + 3 * (q3 - q1)
        out_[str(y)] = {"thr": fl(thr, 1), "hours": fl(((g_[z] > thr) * w).sum(), 2)}
    sp[z] = out_
N["spikes"] = {"tukey": sp, "ro_max": fl(ro.max(), 2), "ro_max_ts": ro.idxmax().strftime("%Y-%m-%d %H:%M")}

# =============================================================================
# 5. Transformations, tails, volatility clustering
# =============================================================================
y26 = X.loc[str(Y), "RO"].dropna()                    # current year to cut-off: all 15-min, consistent resolution
med = float(y26.median())
mad = float(stats.median_abs_deviation(y26, scale="normal"))
z26 = np.arcsinh((y26 - med) / mad)
N["trans"] = {"n": int(len(y26)), "n_le0": int((y26 <= 0).sum()), "n_eq0": int((y26 == 0).sum()), "min": fl(y26.min(), 2), "share_le0": fl((y26 <= 0).mean() * 100, 2),
              "median": fl(med, 2), "mad": fl(mad, 2), "skew_level": fl(stats.skew(y26), 2),
              "kurt_level": fl(stats.kurtosis(y26), 2), "skew_asinh": fl(stats.skew(z26), 2), "kurt_asinh": fl(stats.kurtosis(z26), 2)}
b = F["brent_usd_bbl"].dropna()
# The continuous front-month series switches contract on the first trading day of each month (ICE Brent expires on the
# last business day of the second month before delivery); that day's change mixes price and roll, so it is dropped.
ROLL = b.groupby(b.index.to_period("M")).head(1).index
rb_all = np.log(b).diff().dropna() * 100
rb = rb_all.drop(rb_all.index.intersection(ROLL))                 # log returns, roll days removed
rs = (b.pct_change() * 100).dropna()
rs = rs.drop(rs.index.intersection(ROLL))                         # simple % changes, roll days removed
tpar = stats.t.fit(rb)
vol = rb.rolling(21).std() * np.sqrt(252)
N["tails"] = {"n": int(len(rb)), "start": d(rb.index.min()), "end": d(rb.index.max()), "sd": fl(rb.std(), 3),
              "skew": fl(stats.skew(rb), 2), "exkurt": fl(stats.kurtosis(rb), 2), "jb": fl(stats.jarque_bera(rb).statistic, 0),
              "t_df": fl(tpar[0], 2), "n_4sd": int((rb.abs() > 4 * rb.std()).sum()),
              "n_4sd_normal": fl(len(rb) * 2 * stats.norm.sf(4), 2),
              "lb_r": fl(acorr_ljungbox(rb, lags=[10], return_df=True)["lb_stat"].iloc[0], 1),
              "lb_r2": fl(acorr_ljungbox(rb ** 2, lags=[10], return_df=True)["lb_stat"].iloc[0], 1),
              "ro_lb2": fl(acorr_ljungbox(PF["RO"].diff().dropna() ** 2, lags=[7], return_df=True)["lb_stat"].iloc[0], 1),
              "vol_max": fl(vol.max(), 1), "vol_max_date": vol.idxmax().strftime("%Y-%m"), "vol_median": fl(vol.median(), 1),
              "n_roll": int(len(rb_all) - len(rb))}

# =============================================================================
# 6. Simulation (concept only), ACF/PACF, naive benchmark
# =============================================================================
rng = np.random.default_rng(20261104)
TS = 500
eps = rng.standard_normal(TS)
ar = np.zeros(TS)
for t in range(1, TS):
    ar[t] = 0.9 * ar[t - 1] + eps[t]
SIM = {"wn": eps, "ar": ar, "rw": np.cumsum(eps)}
N["sim"] = {"T": TS, "seed": 20261104}
for k_, s_ in SIM.items():
    r_ = acf(s_, nlags=30, fft=True)
    N["sim"][k_] = {"acf1": fl(r_[1], 2), "acf10": fl(r_[10], 2)}
N["sim"]["ar_theory_acf10"] = fl(0.9 ** 10, 2)

sA = P["RO"].loc["2023-01-01":].dropna()
K = 42
rA = acf(sA, nlags=K, fft=True)
pA = pacf(sA, nlags=K, method="ywm")
TA = len(sA)
bart = 1.96 * np.sqrt((1 + 2 * np.concatenate([[0], np.cumsum(rA[1:K] ** 2)])) / TA)
rdA = acf(PF["RO"].loc["2023-01-01":].diff().dropna(), nlags=14, fft=True)
N["acf"] = {"daily": {"T": TA, "start": d(sA.index.min()), "end": d(sA.index.max()), "band": fl(1.96 / np.sqrt(TA), 3),
                      "r1": fl(rA[1], 3), "r7": fl(rA[7], 3), "r42": fl(rA[K], 3), "p1": fl(pA[1], 3),
                      "p7": fl(pA[7], 3), "p8": fl(pA[8], 3), "d_r7": fl(rdA[7], 3)}}
hs = H.loc["2024-01-01":"2024-12-31", "RO"].dropna()
Kh = 24 * 8
rh = acf(hs, nlags=Kh, fft=True)
N["acf"]["hourly"] = {"T": int(len(hs)), "r12": fl(rh[12], 3), "r24": fl(rh[24], 3), "r168": fl(rh[168], 3)}

nv = {}
for z in ["RO", "DE_LU"]:
    hz = H[z].dropna()
    tab = pd.DataFrame({"p": hz.values, "date": hz.index.tz_localize(None).normalize(), "hour": hz.index.hour})
    tab = tab.groupby(["date", "hour"])["p"].mean().unstack("hour")
    lag1 = tab.shift(1, freq="D").reindex(tab.index)
    lag7 = tab.shift(7, freq="D").reindex(tab.index)
    naive = lag1.copy()
    msk = np.isin(tab.index.dayofweek, [0, 5, 6])
    naive[msk] = lag7[msk]
    nv[z] = {}
    for y in range(2019, Y + 1):
        i_ = tab.index.year == y
        nv[z][str(y)] = {"naive": fl((tab[i_] - naive[i_]).stack().abs().mean(), 2),
                         "lag1": fl((tab[i_] - lag1[i_]).stack().abs().mean(), 2),
                         "lag7": fl((tab[i_] - lag7[i_]).stack().abs().mean(), 2),
                         "mean": fl(tab[i_].stack().mean(), 2)}
for z in nv:
    nv[z]["n_best"] = int(sum(nv[z][y]["naive"] < min(nv[z][y]["lag1"], nv[z][y]["lag7"]) for y in nv[z]))
    nv[z]["n_years"] = len([y for y in nv[z] if y != "n_best"])
N["naive"] = nv
N["naive"]["years"] = [str(y) for y in range(2019, Y + 1)]

# =============================================================================
# 7. Unit-root / stationarity tests (one verdict per series)
# =============================================================================
hydro_m = GH[["hydro_run_of_river", "hydro_water_reservoir"]].sum(axis=1, min_count=2).resample("MS").sum(min_count=600) / 1e6
hydro_m.index = hydro_m.index.tz_localize(None)
hydro_m = hydro_m.loc[:str(full_years[-1])].dropna()
hydro_ds = hydro_m - hydro_m.groupby(hydro_m.index.month).transform("mean")      # monthly means removed first
series = [("ro_lvl", P["RO"].dropna()), ("ro_d", PF["RO"].diff().dropna()), ("de_lvl", P["DE_LU"].dropna()),
          ("br_lvl", np.log(b)), ("br_r", np.log(b).diff().dropna()), ("hy_ds", hydro_ds)]
N["unit"] = {"order": [k for k, _ in series]}
for k, x in series:
    a = adfuller(x, regression="c", autolag="AIC")
    kp = kpss(x, regression="c", nlags="auto")
    dec_ = {(True, False): "stationary", (False, True): "unit_root", (True, True): "conflict",
            (False, False): "inconclusive"}[(a[1] < 0.05, kp[1] < 0.05)]
    N["unit"][k] = {"T": int(len(x)), "first": d(x.index.min()), "last": d(x.index.max()), "adf": fl(a[0], 2),
                    "adf_p": fl(a[1], 4), "adf_lags": int(a[2]), "kpss": fl(kp[0], 3), "kpss_p": fl(kp[1], 3),
                    "kpss_p_trunc": "lt" if kp[1] <= 0.01 else ("gt" if kp[1] >= 0.1 else "in"), "decision": dec_}
x = P["RO"].loc["2023-01-01":].dropna()
N["unit"]["ro_2023"] = {"adf_p": fl(adfuller(x, regression="c", autolag="AIC")[1], 4),
                        "kpss": fl(kpss(x, regression="c", nlags="auto")[0], 3)}

# =============================================================================
# 8. Decomposition (monthly RO load) and smoothing (Brent)
# =============================================================================
lm = GH["load"].resample("MS").mean()
lm.index = lm.index.tz_localize(None)
lm = (lm.loc["2016-01-01":f"{full_years[-1]}-12-01"] / 1000).asfreq("MS")
w = np.r_[1 / 24, np.repeat(1 / 12, 11), 1 / 24]
cma = lm.rolling(13, center=True).apply(lambda v: float(np.dot(v, w)), raw=True)
det = lm - cma
raw_idx = det.groupby(det.index.month).mean()
sidx = raw_idx - raw_idx.mean()
sd_ = seasonal_decompose(lm, model="additive", period=12)
assert np.allclose(sd_.trend.dropna().values, cma.dropna().values)
stl = STL(lm, period=12, seasonal=13, robust=True).fit()
y0s, y1s = str(lm.index[0].year), str(full_years[-1])
N["decomp"] = {"start": lm.index[0].strftime("%Y-%m"), "end": lm.index[-1].strftime("%Y-%m"), "T": int(len(lm)),
               "sidx": {MON_EN[i]: fl(sidx.loc[i + 1], 3) for i in range(12)}, "raw_mean": fl(raw_idx.mean(), 4),
               "ex": {"date": lm.index[6].strftime("%Y-%m"), "y_first": fl(lm.iloc[0], 3), "y_last": fl(lm.iloc[12], 3),
                      "sum_mid": fl(lm.iloc[1:12].sum(), 3), "cma": fl(cma.iloc[6], 3), "y": fl(lm.iloc[6], 3),
                      "detr": fl(det.iloc[6], 3)},
               "cl_amp": fl(sidx.max() - sidx.min(), 2),
               "stl_amp_first": fl(stl.seasonal.loc[y0s].max() - stl.seasonal.loc[y0s].min(), 2),
               "stl_amp_last": fl(stl.seasonal.loc[y1s].max() - stl.seasonal.loc[y1s].min(), 2),
               "fs": fl(max(0, 1 - np.var(stl.resid) / np.var(stl.resid + stl.seasonal)), 3)}
bs = b.loc["2024-01-01":]
HL = 10
alpha_hl = 1 - 2 ** (-1 / HL)
ses = SimpleExpSmoothing(bs.values, initialization_method="estimated").fit()
N["smooth"] = {"start": d(bs.index.min()), "end": d(bs.index.max()), "hl": HL, "alpha_hl": fl(alpha_hl, 4),
               "alpha_ses": fl(ses.params["smoothing_level"], 4)}

# =============================================================================
# 9. Case (a) hydro
# =============================================================================
hy_a = mix["Hydro"].loc[full_years]
dfm = pd.concat([hydro_m.rename("hydro"), P["RO"].resample("MS").mean().rename("price"),
                 TTF["ttf_eur_mwh"].rename("ttf")], axis=1).dropna()
ols = sm.OLS(dfm["price"], sm.add_constant(dfm[["hydro", "ttf"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
dfm["spread"] = dfm["price"] - P["DE_LU"].resample("MS").mean().reindex(dfm.index)
ols2 = sm.OLS(dfm["spread"], sm.add_constant(dfm[["hydro"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
N["hydro"] = {"y2023": fl(hy_a.loc[2023], 2), "y2025": fl(hy_a.loc[2025], 2),
              "chg_pct": fl((hy_a.loc[2025] / hy_a.loc[2023] - 1) * 100, 1), "max_year": int(hy_a.idxmax()),
              "min_year": int(hy_a.idxmin()), "cov2023": fl(cov.loc[2023, "Hydro"] * 100, 1), "cov2025": fl(cov.loc[2025, "Hydro"] * 100, 1),
              "netimp2023": fl(imp_twh.loc[2023], 2), "netimp2025": fl(imp_twh.loc[2025], 2),
              "mean_1525": fl(hy_a.loc[2015:2025].mean(), 2), "vs_mean_pct": fl((hy_a.loc[2025] / hy_a.loc[2015:2025].mean() - 1) * 100, 1),
              "reg": {"n": int(ols.nobs), "r2": fl(ols.rsquared, 3), "start": dfm.index.min().strftime("%Y-%m"),
                      "end": dfm.index.max().strftime("%Y-%m"),
                      **{k: {"b": fl(ols.params[k], 2), "se": fl(ols.bse[k], 2), "t": fl(ols.tvalues[k], 2)} for k in ["const", "hydro", "ttf"]}},
              "spread_b": fl(ols2.params["hydro"], 2), "spread_t": fl(ols2.tvalues["hydro"], 2)}

# =============================================================================
# 10. Case (b) June 2025, Brent
# =============================================================================
p12, p13, p23, p24 = (b.loc[x_] for x_ in ["2025-06-12", "2025-06-13", "2025-06-23", "2025-06-24"])
win = b.loc["2025-06-13":"2025-06-23"]
sd24 = rb.loc["2024"].std()
N["iran"] = {"p12": fl(p12, 2), "p13": fl(p13, 2), "chg13": fl((p13 / p12 - 1) * 100, 1),
             "z13": fl(np.log(p13 / p12) * 100 / sd24, 1), "peak": fl(win.max(), 2), "peak_date": d(win.idxmax()),
             "p23": fl(p23, 2), "p24": fl(p24, 2), "chg24_peak": fl((p24 / win.max() - 1) * 100, 1),
             "chg24_12": fl((p24 / p12 - 1) * 100, 1)}

# =============================================================================
# 11. Case (c) separation, summer 2024
# =============================================================================
jul = P.loc["2024-07", ZONES].mean()
g16 = P.loc["2024-07-16", ZONES]
hj = H.loc["2024-07-01":"2024-07-31", ZONES].dropna()
s24 = P.loc["2024-06-01":"2024-09-30", "RO"]
h3 = H.loc[str(s24.idxmax().date()), "RO"]
hd16 = H.loc["2024-07-16", ZONES]
N["sep"] = {"jul": {z: fl(jul[z], 2) for z in ZONES}, "d16": {z: fl(g16[z], 2) for z in ZONES},
            "d16_gap": fl(g16["RO"] - g16["DE_LU"], 2),
            "eq_ro_bg": fl((np.abs(hj["RO"] - hj["BG"]) < 0.01).mean() * 100, 1),
            "eq_ro_hu": fl((np.abs(hj["RO"] - hj["HU"]) < 0.01).mean() * 100, 1),
            "eq_ro_de": fl((np.abs(hj["RO"] - hj["DE_LU"]) < 0.01).mean() * 100, 1),
            "peak": fl(s24.max(), 2), "peak_date": d(s24.idxmax()), "de_on_peak": fl(P.loc[s24.idxmax(), "DE_LU"], 2),
            "peak_hour": int(h3.idxmax().hour), "peak_hour_v": fl(h3.max(), 2),
            "d16_ro_max": fl(hd16["RO"].max(), 2), "d16_ro_max_h": int(hd16["RO"].idxmax().hour),
            "d16_de_min": fl(hd16["DE_LU"].min(), 2), "d16_de_min_h": int(hd16["DE_LU"].idxmin().hour)}
for y in [2023, 2024]:
    N["sep"][f"hydro_ja_{y}"] = fl(hydro_m.loc[f"{y}-07-01":f"{y}-08-01"].sum(), 2)
    N["sep"][f"imp_ja_{y}"] = fl(CB.loc[f"{y}-07-01":f"{y}-08-31", "sum"].mean(), 0)

# =============================================================================
# 12. Case (e) the current year so far
# =============================================================================
pY = P.loc[str(Y), ZONES]
pPrev = P.loc[f"{Y - 1}-01-01":f"{Y - 1}-{END:%m-%d}", ZONES]
xY = X.loc[str(Y)]
mY = pY.resample("MS").mean()
bY = b.loc[str(Y)]
bm = bY.resample("MS").mean()
mar = b.loc[f"{Y}-03"]
mar_first, mar_end = mar.iloc[0], mar.iloc[-1]                     # same (May) contract within March
rY, rsY = rb.loc[str(Y)], rs.loc[str(Y)]
N["cy"] = {"mean": {z: fl(pY[z].mean(), 2) for z in ZONES}, "mean_prev": {z: fl(pPrev[z].mean(), 2) for z in ZONES},
           "chg": {z: fl((pY[z].mean() / pPrev[z].mean() - 1) * 100, 1) for z in ZONES},
           "lm": {z: fl(mY[z].iloc[-1], 1) for z in ZONES},
           "lm_prev": {z: fl(P.loc[f"{Y - 1}-{END:%m}", z].mean(), 1) for z in ZONES},
           "spread_ytd": fl(pY["RO"].mean() - pY["DE_LU"].mean(), 1), "spread_prev": fl(pPrev["RO"].mean() - pPrev["DE_LU"].mean(), 1),
           "ro_max_day": fl(pY["RO"].max(), 2), "ro_max_day_date": d(pY["RO"].idxmax()),
           "ro_min_day": fl(pY["RO"].min(), 2), "ro_min_day_date": d(pY["RO"].idxmin()),
           "ro_max_mtu": fl(xY["RO"].max(), 2), "ro_max_mtu_ts": xY["RO"].idxmax().strftime("%Y-%m-%d %H:%M"),
           "ro_min_mtu": fl(xY["RO"].min(), 2), "ro_min_mtu_ts": xY["RO"].idxmin().strftime("%Y-%m-%d %H:%M"),
           "de_min_mtu": fl(xY["DE_LU"].min(), 2), "de_min_mtu_ts": xY["DE_LU"].idxmin().strftime("%Y-%m-%d %H:%M"),
           "brent": {"jan_avg": fl(bm.iloc[0], 2), "last_avg": fl(bm.iloc[-1], 2), "max": fl(bY.max(), 2), "max_date": d(bY.idxmax()),
                     "mar_first": fl(mar_first, 2), "mar_first_date": d(mar.index[0]), "mar_end": fl(mar_end, 2),
                     "mar_end_date": d(mar.index[-1]), "mar_pct": fl((mar_end / mar_first - 1) * 100, 1),
                     "roll_apr": fl((b.loc[f"{Y}-04"].iloc[0] / mar_end - 1) * 100, 1),
                     "max_move": fl(rsY.loc[rsY.abs().idxmax()], 2), "max_move_date": d(rsY.abs().idxmax()),
                     "vol_ytd": fl(rY.std() * np.sqrt(252), 1), "vol_prev": fl(rb.loc[str(Y - 1)].std() * np.sqrt(252), 1)}}

# =============================================================================
# 13. Case (f) Romania vs Bulgaria evenings and Bulgaria's batteries (local time Europe/Bucharest = Europe/Sofia)
# =============================================================================
XL = X.copy()
XL.index = XL.index.tz_convert("Europe/Bucharest")
wloc = XL["mtu_minutes"] / 60
day = XL.index.tz_localize(None).normalize()
spread = {}
HLc = H.copy()
HLc.index = HLc.index.tz_convert("Europe/Bucharest")      # hourly means: same resolution in every year
hday = HLc.index.tz_localize(None).normalize()
for z in ["RO", "BG", "HU"]:
    g_ = HLc[z].groupby(hday)
    rng_ = (g_.max() - g_.min())[g_.count() >= 20]
    spread[z] = {str(y): fl(rng_[rng_.index.year == y].mean(), 1) for y in [2024, 2025, Y]}


def wmean(z, mask):
    v, ww = XL.loc[mask, z], wloc[mask]
    ok = v.notna()
    return float((v[ok] * ww[ok]).sum() / ww[ok].sum())


ev, mid = {}, {}
for y in [2023, 2024, 2025, Y]:
    base = (XL.index.year == y) & (XL.index.month >= 4) & (XL.index.month <= 9)
    ev[str(y)] = {z: fl(wmean(z, base & (XL.index.hour >= 19) & (XL.index.hour <= 21)), 1) for z in ["RO", "BG", "HU"]}
    mid[str(y)] = {z: fl(wmean(z, base & (XL.index.hour >= 11) & (XL.index.hour <= 14)), 1) for z in ["RO", "BG", "HU"]}
evm = XL[(XL.index.hour >= 19) & (XL.index.hour <= 21)].loc["2023-01-01":]
evw = evm["mtu_minutes"] / 60
mk = evm.index.tz_localize(None).to_period("M")
ev_sp = ((evm["RO"] - evm["BG"]) * evw).groupby(mk).sum() / evw.groupby(mk).sum()
bat = BGH[["battery", "battery_consumption"]].copy()
bat.index = bat.index.tz_convert("Europe/Bucharest")
bat_first = bat.dropna(how="all").index.min()
bb = bat.loc[bat_first:]
batm = bb.groupby(bb.index.tz_localize(None).to_period("M")).mean()
rob = GH["battery"]
N["bat"] = {"spread": spread, "evening": ev, "midday": mid, "bg_first": bat_first.strftime("%Y-%m-%d"),
            "bg_dis": {str(k): fl(v, 0) for k, v in batm["battery"].items()},
            "bg_ch": {str(k): fl(-v, 0) for k, v in batm["battery_consumption"].items()},
            "ro_bat": {str(y): fl(rob[rob.index.year == y].mean(), 0) for y in [2025, Y]},
            "ro_bat_first": d(rob.dropna().index.min()),
            "ev_gap": {y: fl(ev[y]["RO"] - ev[y]["BG"], 1) for y in ev},
            "mid_gap": {y: fl(mid[y]["RO"] - mid[y]["BG"], 1) for y in mid},
            "ev_sp_cy": {k.strftime("%b"): fl(v, 1) for k, v in ev_sp.items() if k.year == Y},
            "gap_open": next((k.strftime("%Y-%m") for k, v in ev_sp.items() if k.year == Y and v > 15), "none")}

# =============================================================================
# Charts: one set per language
# =============================================================================
TXT = {
    "en": {"load": "Load (consumption)", "twh": "TWh per year (full years)", "gen_title": "Generation by source, TWh",
           "share": "% of Romania's generation", "ytd_title": "Jan-{m} {y0} vs {y1} (hours reported in both)",
           "src": {"Hydro": "Hydro", "Nuclear": "Nuclear", "Coal": "Coal", "Gas": "Gas", "Wind": "Wind", "Solar": "Solar", "Biomass": "Biomass"},
           "zone": {"RO": "Romania (OPCOM PZU)", "BG": "Bulgaria (IBEX)", "HU": "Hungary (HUPX)", "DE_LU": "Germany-Luxembourg"},
           "eurmwh7": "EUR/MWh, 7-day mean", "hour_cet": "Hour of day (CET/CEST)", "mean_price": "Mean price, EUR/MWh",
           "gw": "Mean power, GW", "ro_month": "Romania: load and generation by month", "hydro": "Hydro (run-of-river + reservoir)",
           "solar": "Solar", "price_month": "RO day-ahead price by month", "pratio": "RO price / annual mean (median over years)",
           "neg_title": "Negative day-ahead prices per year", "neg_h": "Hours < 0 (hour-equivalents)", "neg_when": "RO, by hour of day (2024 to date)",
           "neg_hro": "Hours < 0", "ytd": "YTD", "neg_month": "RO negative-price hours by month",
           "neg_mh": "Negative hours, RO", "solar_y": "RO solar generation, TWh (metered)", "rohourly": "RO hourly price, 2024",
           "thr": "Spike threshold Q3 + 3 IQR = {v} EUR/MWh", "level": "Level $p_t$, EUR/MWh", "mtus": "Number of MTUs",
           "asinh": "Variance-stabilised: asinh", "tv": "transformed value", "allmtu": "RO 15-min prices, Jan-{m} {y}",
           "qq": "Q-Q plot", "nq": "Normal quantile", "eq": "Empirical quantile", "brent_r": "Brent daily log return (standardised)",
           "normal": "Normal distribution", "studt": "Student-t, fitted df = {v}", "dens": "Density (log scale)", "stdr": "standardised return",
           "ret": "Brent daily log return, %", "vol": "21-day volatility, % a year", "pa": "% a year",
           "wn": "White noise", "ar": "AR(1), $\\phi=0.9$", "rw": "Random walk", "lag": "lag $k$", "sacf": "sample ACF",
           "acf_t": "ACF, RO daily price (level)", "pacf_t": "PACF, RO daily price (level)", "lagd": "lag (days)", "lagh": "lag (hours)",
           "bartlett": "Bartlett band", "wnband": "white-noise band $\\pm1.96/\\sqrt{T}$", "sacfpacf": "sample ACF / PACF",
           "acfh": "sample ACF, RO hourly price 2024", "loadm": "RO load, GW", "tr_cl": "Trend, classical",
           "tr_stl": "Trend, STL", "se_cl": "Season, classical", "se_stl": "Season, STL", "re_cl": "Remainder, classical",
           "re_stl": "Remainder, STL", "brent": "Brent front-month, USD/bbl", "sma": "simple moving average, 20 trading days",
           "ewma": "EWMA, half-life {h} days ($\\alpha$ = {a})", "h23": "Hydro 2023 (wet)", "h25": "Hydro 2025 (dry)",
           "hmean": "Hydro mean 2015-2025", "twhm": "TWh per month", "hro": "RO hydro generation", "hvp": "Hydro vs PZU, monthly",
           "hx": "Hydro, TWh per month", "hy": "RO price, EUR/MWh", "month_pt": "one month", "bclose": "Brent close, USD/bbl",
           "a13": "13 Jun: Israel strikes Iran", "apk": "peak close", "a24": "24 Jun: ceasefire in effect",
           "sum24": "Summer 2024, daily base", "d16": "16 July 2024, hourly", "hcest": "Hour (CEST)",
           "dailyb": "Daily base, EUR/MWh", "evsp": "RO - BG, 19-22 h EET, EUR/MWh",
           "bdis": "BG battery discharge, MW", "bch": "BG battery charging, MW", "mw": "MW",
           "upto": "{y} (to {m})", "nucl": "Nuclear", "naive": "naive", "mae": "MAE, EUR/MWh", "noreport": "Sep: not reported"},
    "ro": {"load": "Consum", "twh": "TWh pe an (ani compleți)", "gen_title": "Producție pe surse, TWh",
           "share": "% din producția României", "ytd_title": "ian.-{m} {y0} vs {y1} (ore raportate în ambii ani)",
           "src": {"Hydro": "Hidro", "Nuclear": "Nuclear", "Coal": "Cărbune", "Gas": "Gaze", "Wind": "Eolian", "Solar": "Solar", "Biomass": "Biomasă"},
           "zone": {"RO": "România (OPCOM PZU)", "BG": "Bulgaria (IBEX)", "HU": "Ungaria (HUPX)", "DE_LU": "Germania-Luxemburg"},
           "eurmwh7": "EUR/MWh, medie pe 7 zile", "hour_cet": "Ora din zi (CET/CEST)", "mean_price": "Preț mediu, EUR/MWh",
           "gw": "Putere medie, GW", "ro_month": "România: consum și producție pe luni", "hydro": "Hidro (pe firul apei + lacuri)",
           "solar": "Solar", "price_month": "Prețul PZU pe luni", "pratio": "Preț RO / media anuală (mediana pe ani)",
           "neg_title": "Prețuri negative pe an", "neg_h": "Ore < 0 (echivalent-ore)", "neg_when": "RO, pe ore (din 2024)",
           "neg_hro": "Ore < 0", "ytd": "parțial", "neg_month": "Ore cu preț negativ în RO, pe luni",
           "neg_mh": "Ore negative, RO", "solar_y": "Producție solară RO, TWh (măsurată)", "rohourly": "Preț orar RO, 2024",
           "thr": "Prag de vîrf Q3 + 3 IQR = {v} EUR/MWh", "level": "Nivel $p_t$, EUR/MWh", "mtus": "Număr de intervale",
           "asinh": "Varianță stabilizată: asinh", "tv": "valoare transformată", "allmtu": "Prețuri RO de 15 min, ian.-{m} {y}",
           "qq": "Grafic Q-Q", "nq": "Cuantilă normală", "eq": "Cuantilă empirică", "brent_r": "Randament logaritmic zilnic Brent (standardizat)",
           "normal": "Distribuția normală", "studt": "Student-t, grade de libertate = {v}", "dens": "Densitate (scară logaritmică)",
           "stdr": "randament standardizat", "ret": "Randament logaritmic zilnic Brent, %", "vol": "Volatilitate pe 21 de zile, % pe an",
           "pa": "% pe an", "wn": "Zgomot alb", "ar": "AR(1), $\\phi=0{,}9$", "rw": "Mers aleator", "lag": "decalaj $k$",
           "sacf": "ACF de selecție", "acf_t": "ACF, preț zilnic RO (nivel)", "pacf_t": "PACF, preț zilnic RO (nivel)",
           "lagd": "decalaj (zile)", "lagh": "decalaj (ore)", "bartlett": "Banda Bartlett", "wnband": "banda de zgomot alb $\\pm1{,}96/\\sqrt{T}$",
           "sacfpacf": "ACF / PACF de selecție", "acfh": "ACF de selecție, preț orar RO 2024", "loadm": "Consum RO, GW",
           "tr_cl": "Trend, clasic", "tr_stl": "Trend, STL", "se_cl": "Sezon, clasic",
           "se_stl": "Sezon, STL", "re_cl": "Rest, clasic", "re_stl": "Rest, STL", "brent": "Brent (primul contract futures), USD/bbl",
           "sma": "medie mobilă simplă, 20 de zile de tranzacționare", "ewma": "EWMA, timp de înjumătățire {h} zile ($\\alpha$ = {a})",
           "h23": "Hidro 2023 (an ploios)", "h25": "Hidro 2025 (an secetos)", "hmean": "Medie hidro 2015-2025", "twhm": "TWh pe lună",
           "hro": "Producția hidro în România", "hvp": "Hidro vs PZU, lunar", "hx": "Hidro, TWh pe lună", "hy": "Preț RO, EUR/MWh",
           "month_pt": "o lună", "bclose": "Brent, preț de închidere, USD/bbl", "a13": "13 iun.: Israelul atacă Iranul",
           "apk": "maximul", "a24": "24 iun.: armistițiul intră în vigoare", "sum24": "Vara 2024, preț de bază zilnic",
           "d16": "16 iulie 2024, orar", "hcest": "Ora (CEST)", "dailyb": "Preț de bază zilnic, EUR/MWh",
           "evsp": "RO - BG, 19-22 EET, EUR/MWh", "bdis": "Descărcare baterii BG, MW",
           "bch": "Încărcare baterii BG, MW", "mw": "MW", "upto": "{y} (pînă în {m})", "nucl": "Nuclear", "naive": "naiv", "mae": "MAE, EUR/MWh",
           "noreport": "sep.: neraportat"},
}
MON1 = {"en": ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"], "ro": ["I", "F", "M", "A", "M", "I", "I", "A", "S", "O", "N", "D"]}
SRC_TXT = {"en": {"ec": "energy-charts.info (Fraunhofer ISE); prices from the exchanges OPCOM (RO), IBEX (BG), HUPX (HU), EPEX SPOT (DE-LU), via ENTSO-E",
                  "ecg": "energy-charts.info (Fraunhofer ISE); ENTSO-E (Transelectrica data for Romania)", "yf": "Yahoo Finance (BZ=F)",
                  "opc": "OPCOM, PZU aggregated curves",
                  "ecyf": "energy-charts.info (OPCOM prices); Yahoo Finance (BZ=F)",
                  "sim": "simulation, numpy, seed 20261104"},
           "ro": {"ec": "energy-charts.info (Fraunhofer ISE); prețuri de la bursele OPCOM (RO), IBEX (BG), HUPX (HU), EPEX SPOT (DE-LU), prin ENTSO-E",
                  "ecg": "energy-charts.info (Fraunhofer ISE); ENTSO-E (date Transelectrica pentru România)", "yf": "Yahoo Finance (BZ=F)",
                  "opc": "OPCOM, curbele agregate PZU",
                  "ecyf": "energy-charts.info (prețuri OPCOM); Yahoo Finance (BZ=F)",
                  "sim": "simulare, numpy, seed = 20261104"}}


def num(v, lang, k=1):
    s = f"{v:.{k}f}"
    return s.replace(".", ",") if lang == "ro" else s


def chart(name, src_key, period_en, period_ro):
    N["charts"][name] = {"source_en": SRC_TXT["en"][src_key], "source_ro": SRC_TXT["ro"][src_key],
                         "period_en": period_en, "period_ro": period_ro}


def comma_y(fig, lang, also_x=()):
    """Romanian charts: decimal comma and true minus on numeric linear axes."""
    if lang != "ro":
        return
    f_ = FuncFormatter(lambda v, p: f"{v:g}".replace(".", ",").replace("-", "−"))
    from matplotlib.ticker import FixedFormatter
    for ax in fig.axes:
        if ax.get_yscale() == "linear" and not getattr(ax, "_keep_y", False):
            ax.yaxis.set_major_formatter(f_)
    for ax in also_x:
        ax.xaxis.set_major_formatter(f_)


def out(fig, lang, name, bottom=0.17, also_x=()):
    comma_y(fig, lang, also_x)
    os.makedirs(os.path.join(HERE, "charts", lang), exist_ok=True)
    save(fig, os.path.join(HERE, "charts", lang, name + ".pdf"), bottom=bottom)


def month_fmt(ax, lang):
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    if lang == "ro":
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: MON_RO[mdates.num2date(v).month - 1]))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))


ORDER = ["Hydro", "Nuclear", "Coal", "Gas", "Wind", "Solar", "Biomass"]
SCOL = {"Hydro": PAL["RO"], "Nuclear": PAL["c7"], "Coal": "#5b4a3a", "Gas": PAL["DE_LU"], "Wind": PAL["HU"],
        "Solar": PAL["BG"], "Biomass": PAL["c6"]}

for lang in ["en", "ro"]:
    T = TXT[lang]
    mlast = (MON_EN if lang == "en" else MON_RO)[END.month - 1]
    # mix
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.5), gridspec_kw={"width_ratios": [1.45, 1]})
    bot = np.zeros(len(full_years))
    for k in ORDER:
        axs[0].bar(full_years, mix.loc[full_years, k].values, bottom=bot, color=SCOL[k], label=T["src"][k], width=0.72,
                   edgecolor="white", lw=0.8)
        bot += mix.loc[full_years, k].values
    axs[0].plot(full_years, load_twh.loc[full_years], "k_", ms=17, mew=2.2, label=T["load"])
    axs[0].set_ylabel(T["twh"])
    axs[0].set_xticks(full_years)
    axs[0].set_xticklabels([str(y)[2:] for y in full_years])
    sh = pd.DataFrame({0: [L[k]["share_prev"] for k in ORDER], 1: [L[k]["share_ytd"] for k in ORDER]}, index=ORDER)
    bot = np.zeros(2)
    for k in ORDER:
        axs[1].bar([0, 1], sh.loc[k].values, bottom=bot, color=SCOL[k], width=0.55, edgecolor="white", lw=0.8)
        for i_ in range(2):
            if sh.loc[k].values[i_] > 4:
                axs[1].text(i_, bot[i_] + sh.loc[k].values[i_] / 2, f"{sh.loc[k].values[i_]:.0f}%", ha="center",
                            va="center", fontsize=9, color="white")
        bot += sh.loc[k].values
    axs[1].set_xticks([0, 1])
    axs[1].set_xticklabels([str(Y - 1), str(Y)])
    axs[1].set_ylabel(T["share"])
    axs[1].set_title(T["ytd_title"].format(m=mlast, y0=Y - 1, y1=Y), fontsize=10)
    legend_bottom(fig, ncol=4)
    out(fig, lang, "mix_ro_annual", bottom=0.22)
    # prices
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    for z in ["DE_LU", "HU", "BG", "RO"]:
        s = P[z].dropna().rolling(7, min_periods=7).mean()
        ax.plot(s.index, s, color=PAL[z], ls=ZONE_LS[z], lw=1.0, label=T["zone"][z])
    ax.set_ylabel(T["eurmwh7"])
    legend_bottom(fig, ncol=2)
    out(fig, lang, "prices_daily_4zones")
    # intraday
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2))
    for ax, z in zip(axs, ["RO", "DE_LU"]):
        for y, ls in [(2019, "--"), (2025, "-")]:
            ax.plot(prof[y].index, prof[y][z], color=PAL[z], ls=ls, marker="o", ms=3.5, label=f"{ZL[z]} {y}")
        ax.set_title(T["zone"][z])
        ax.set_xlabel(T["hour_cet"])
        ax.set_xticks(range(0, 24, 3))
    axs[0].set_ylabel(T["mean_price"])
    legend_bottom(fig, ncol=4)
    out(fig, lang, "profile_intraday")
    # annual
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.3))
    for c, col, lab in [("load", "#222222", T["load"]), ("hydro", PAL["RO"], T["hydro"]), ("solar", PAL["BG"], T["solar"])]:
        axs[0].plot(range(1, 13), mprof[c], color=col, marker="o", ms=4, label=lab)
    axs[0].set_ylabel(T["gw"])
    axs[0].set_title(T["ro_month"])
    axs[1].bar(range(1, 13), mprof["price_ratio"], color=PAL["RO"], width=0.65, label=T["pratio"])
    axs[1].axhline(1.0, color="#222222", lw=0.8)
    axs[1].set_ylim(0.6, 1.4)
    axs[1].set_title(T["price_month"])
    for ax in axs:
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(MON1[lang])
    legend_bottom(fig, ncol=4)
    out(fig, lang, "profile_annual")
    # spikes
    fig, ax = plt.subplots(figsize=(6.4, 2.52))
    s24h = H.loc["2024", "RO"].copy()
    s24h.index = s24h.index.tz_localize(None)
    ax.plot(s24h.index, s24h, color=PAL["RO"], lw=0.5, label=T["rohourly"])
    thr24 = sp["RO"]["2024"]["thr"]
    ax.axhline(thr24, color=PAL["c8"], lw=1.0, ls="--", label=T["thr"].format(v=num(thr24, lang, 0)))
    ax.axhline(0, color="#222222", lw=0.6)
    ax.set_ylabel("EUR/MWh")
    month_fmt(ax, lang)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "spikes_ro_2024")
    # negative per year + by hour
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.4), gridspec_kw={"width_ratios": [1.35, 1]})
    yrs = list(range(2018, Y + 1))
    for i, z in enumerate(ZONES):
        axs[0].bar(np.array(yrs) + (i - 1.5) * 0.2, [N["neg"]["hours"][z][str(y)] for y in yrs], width=0.2, color=PAL[z],
                   label=T["zone"][z])
    axs[0].set_ylabel(T["neg_h"])
    axs[0].set_xticks(yrs)
    axs[0].set_xticklabels([(str(y)[2:] if y % 2 == 0 else "") if y < Y else f"{str(y)[2:]}\n{T['ytd']}" for y in yrs])
    axs[1].bar(hneg.index, hneg.values, color=PAL["RO"], width=0.75)
    axs[1].set_xlabel(T["hour_cet"])
    axs[1].set_ylabel(T["neg_hro"])
    axs[1].set_title(T["neg_when"])
    axs[1].set_xticks(range(0, 24, 6))
    legend_bottom(fig, ncol=2)
    out(fig, lang, "negative_prices", bottom=0.3)
    # negative by month + solar
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2))
    bot_ = np.zeros(12)
    for i_, y_ in enumerate(hm.columns):
        v_ = hm[y_].reindex(range(1, 13)).fillna(0.0).values     # months after the cut-off have no bar
        axs[0].bar(range(1, 13), v_, bottom=bot_, color=ep.SERIES[i_], width=0.7, edgecolor="white", lw=0.6,
                   label=f"{y_}" + (f" ({T['ytd']})" if y_ == Y else ""))
        bot_ += v_
    axs[0].set_xticks(range(1, 13))
    axs[0].set_xticklabels(MON1[lang])
    axs[0].set_ylabel(T["neg_mh"])
    axs[0].set_title(T["neg_month"])
    sy = [y for y in full_years if y >= 2018]
    axs[1].bar(sy, [mix.loc[y, "Solar"] for y in sy], color=PAL["BG"], width=0.6)
    axs[1].set_xticks(sy)
    axs[1].set_xticklabels([str(y)[2:] for y in sy])
    axs[1].set_title(T["solar_y"])
    legend_bottom(fig, ncol=4)
    out(fig, lang, "negative_solar")
    # asinh
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.8))
    axs[0].hist(y26.clip(upper=450), bins=np.arange(-150, 455, 5), color=PAL["RO"], label=T["allmtu"].format(m=mlast, y=Y))
    axs[0].axvline(0, color="#222222", lw=0.8)
    axs[0].set_xlim(-150, 450)
    axs[0].set_xlabel(T["level"])
    axs[0].set_ylabel(T["mtus"])
    axs[1].hist(z26, bins=120, color=PAL["HU"])
    axs[1].set_xlabel(T["tv"])
    axs[1].set_title(T["asinh"])
    legend_bottom(fig, ncol=1)
    out(fig, lang, "asinh_ro", also_x=[axs[1]])
    # tails
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0))
    zz = (rb - rb.mean()) / rb.std()
    osm, osr = stats.probplot(zz, dist="norm", fit=False)
    axs[0].plot(osm, osr, "o", ms=2.5, color=PAL["RO"], label=T["brent_r"])
    axs[0].plot([-4.5, 4.5], [-4.5, 4.5], color=PAL["c8"], lw=1.2, label=T["normal"])
    axs[0].set_xlabel(T["nq"])
    axs[0].set_ylabel(T["eq"])
    axs[0].set_title(T["qq"])
    xs = np.linspace(-8, 8, 400)
    sc = np.sqrt(tpar[0] / (tpar[0] - 2))
    axs[1].hist(zz, bins=150, density=True, color=PAL["RO"], alpha=0.55)
    axs[1].plot(xs, stats.norm.pdf(xs), color=PAL["c8"], lw=1.4)
    axs[1].plot(xs, stats.t(tpar[0]).pdf(xs * sc) * sc, color=PAL["c7"], lw=1.4, ls="--", label=T["studt"].format(v=num(tpar[0], lang)))
    axs[1].set_xlim(-6, 6)
    axs[1].set_yscale("log")
    axs[1].set_ylim(1e-4, 1)
    axs[1].set_title(T["dens"])
    axs[1].set_xlabel(T["stdr"])
    legend_bottom(fig, ncol=3)
    out(fig, lang, "tails_brent")
    # volatility clustering
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.3), sharex=True)
    axs[0].plot(rb.index, rb, color=PAL["RO"], lw=0.6, label=T["ret"])
    axs[1].plot(vol.index, vol, color=PAL["DE_LU"], lw=1.0, label=T["vol"])
    axs[0].set_ylabel("%")
    axs[1].set_ylabel(T["pa"])
    legend_bottom(fig, ncol=2)
    out(fig, lang, "volclust_brent")
    # simulation (teaching only)
    fig, axs = plt.subplots(2, 3, figsize=(6.4, 2.4), gridspec_kw={"height_ratios": [1.3, 1]})
    for j, (k_, col) in enumerate([("wn", PAL["RO"]), ("ar", PAL["HU"]), ("rw", PAL["DE_LU"])]):
        axs[0, j].plot(SIM[k_], color=col, lw=0.8)
        axs[0, j].set_title(T[k_], fontsize=10.5)
        r_ = acf(SIM[k_], nlags=30, fft=True)
        axs[1, j].bar(range(31), r_, color=col, width=0.5)
        for sgn in (1, -1):
            axs[1, j].axhline(sgn * 1.96 / np.sqrt(TS), color="#222222", ls="--", lw=0.8)
        axs[1, j].set_ylim(-0.3, 1.05)
        axs[1, j].set_xlabel(T["lag"])
    axs[1, 0].set_ylabel(T["sacf"])
    out(fig, lang, "sim_wn_ar_rw", bottom=0.0)
    # ACF / PACF daily
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.9))
    axs[0].bar(range(1, K + 1), rA[1:], color=PAL["RO"], width=0.55, label=T["sacfpacf"])
    axs[0].plot(range(1, K + 1), bart, color=PAL["c8"], ls="--", lw=1.1, label=T["bartlett"])
    axs[0].plot(range(1, K + 1), -bart, color=PAL["c8"], ls="--", lw=1.1)
    axs[1].bar(range(1, K + 1), pA[1:], color=PAL["RO"], width=0.55)
    for ax in axs:
        for sgn in (1, -1):
            ax.axhline(sgn * 1.96 / np.sqrt(TA), color=PAL["c7"], ls=":", lw=1.3,
                       label=T["wnband"] if (sgn == 1 and ax is axs[0]) else None)
        ax.axhline(0, color="#222222", lw=0.6)
        ax.set_xticks([1, 7, 14, 21, 28, 35, 42])
        ax.set_xlabel(T["lagd"])
    axs[0].set_title(T["acf_t"])
    axs[1].set_title(T["pacf_t"])
    legend_bottom(fig, ncol=3)
    out(fig, lang, "acf_pacf_ro_daily")
    # ACF hourly
    fig, ax = plt.subplots(figsize=(6.4, 1.5))
    ax.bar(range(1, Kh + 1), rh[1:], color=PAL["RO"], width=0.8, label=T["acfh"])
    for sgn in (1, -1):
        ax.axhline(sgn * 1.96 / np.sqrt(len(hs)), color=PAL["c7"], ls=":", lw=1.3, label=T["wnband"] if sgn == 1 else None)
    ax.set_xticks(range(0, Kh + 1, 24))
    ax.set_xlabel(T["lagh"])
    legend_bottom(fig, ncol=2)
    out(fig, lang, "acf_ro_hourly")
    # decomposition (remainder panel left to the notebook)
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.6), sharex=True)
    axs[0].plot(lm.index, lm, color="#222222", lw=1.1, label=T["loadm"])
    axs[0].plot(cma.index, cma, color=PAL["RO"], lw=1.8, label=T["tr_cl"])
    axs[0].plot(stl.trend.index, stl.trend, color=PAL["DE_LU"], lw=1.4, ls="--", label=T["tr_stl"])
    axs[1].plot(sd_.seasonal.index, sd_.seasonal, color=PAL["RO"], lw=1.4, label=T["se_cl"])
    axs[1].plot(stl.seasonal.index, stl.seasonal, color=PAL["DE_LU"], lw=1.2, ls="--", label=T["se_stl"])
    for ax in axs:
        ax.set_ylabel("GW")
    legend_bottom(fig, ncol=3)
    out(fig, lang, "decomp_load", bottom=0.2)
    # smoothing
    fig, ax = plt.subplots(figsize=(6.4, 1.9))
    ax.plot(bs.index, bs, color="#222222", lw=0.9, label=T["brent"])
    ax.plot(bs.index, bs.rolling(20).mean(), color=PAL["RO"], lw=1.6, label=T["sma"])
    ax.plot(bs.index, bs.ewm(alpha=alpha_hl, adjust=False).mean(), color=PAL["DE_LU"], lw=1.6, ls="--",
            label=T["ewma"].format(h=HL, a=num(alpha_hl, lang, 3)))
    ax.set_ylabel("USD/bbl")
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    if lang == "ro":
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{MON_RO[mdates.num2date(v).month - 1]} {mdates.num2date(v).year}"))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    legend_bottom(fig, ncol=3)
    out(fig, lang, "smooth_brent")
    # hydro case
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2), gridspec_kw={"width_ratios": [1.5, 1]})
    hy_avg = hydro_m.loc["2015":"2025"].groupby(hydro_m.loc["2015":"2025"].index.month).mean()
    axs[0].plot(range(1, 13), hydro_m.loc["2023"].values, color=PAL["RO"], marker="o", ms=4, label=T["h23"])
    axs[0].plot(range(1, 13), hydro_m.loc["2025"].values, color=PAL["DE_LU"], marker="s", ms=4, ls="--", label=T["h25"])
    axs[0].plot(range(1, 13), hy_avg.values, color="#222222", lw=1.0, ls=":", label=T["hmean"])
    axs[0].set_xticks(range(1, 13))
    axs[0].set_xticklabels(MON1[lang])
    axs[0].set_ylabel(T["twhm"])
    axs[0].set_title(T["hro"])
    axs[1].scatter(dfm["hydro"], dfm["price"], s=14, color=PAL["RO"], label=T["month_pt"])
    axs[1].set_xlabel(T["hx"])
    axs[1].set_ylabel(T["hy"])
    axs[1].set_title(T["hvp"])
    legend_bottom(fig, ncol=4)
    out(fig, lang, "hydro_case", also_x=[axs[1]])
    # June 2025
    bw = b.loc["2025-06-02":"2025-07-04"]
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    ax.plot(bw.index, bw, color=PAL["RO"], marker="o", ms=4, label=T["bclose"])
    for dt_, txt, dx, dy, ha in [("2025-06-13", T["a13"], -12, 6, "right"), (str(win.idxmax().date()), T["apk"], 10, 4, "left"),
                                 ("2025-06-24", T["a24"], 10, -16, "left")]:
        ax.annotate(txt, (pd.Timestamp(dt_), b.loc[dt_]), xytext=(dx, dy), textcoords="offset points",
                    ha=ha, fontsize=9.5, arrowprops=dict(arrowstyle="-", lw=0.6))
    ax.set_ylabel("USD/bbl")
    if lang == "ro":
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{mdates.num2date(v).day} {MON_RO[mdates.num2date(v).month - 1]}"))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%-d %b"))
    legend_bottom(fig, ncol=1)
    out(fig, lang, "iran_brent")
    # separation 2024
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2), gridspec_kw={"width_ratios": [1.6, 1]})
    ss = P.loc["2024-06-01":"2024-09-30", ZONES]
    for z in ["DE_LU", "HU", "BG", "RO"]:
        axs[0].plot(ss.index, ss[z], color=PAL[z], ls=ZONE_LS[z], lw=1.2, label=T["zone"][z])
        axs[1].plot(hd16.index.hour, hd16[z], color=PAL[z], ls=ZONE_LS[z], lw=1.4)
    axs[0].set_ylabel(T["dailyb"])
    month_fmt(axs[0], lang)
    axs[0].set_title(T["sum24"])
    axs[1].axhline(0, color="#222222", lw=0.6)
    axs[1].set_xlabel(T["hcest"])
    axs[1].set_ylabel("EUR/MWh")
    axs[1].set_xticks(range(0, 24, 4))
    axs[1].set_title(T["d16"])
    legend_bottom(fig, ncol=4)
    out(fig, lang, "separation_2024")
    # current year: prices
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.5), sharex=True, gridspec_kw={"height_ratios": [1.6, 1]})
    for z in ["DE_LU", "HU", "BG", "RO"]:
        axs[0].plot(pY.index, pY[z], color=PAL[z], ls=ZONE_LS[z], lw=1.0, label=T["zone"][z])
    axs[0].set_ylabel(T["dailyb"])
    axs[1].plot(bY.index, bY, color=PAL["c7"], lw=1.3, label=T["brent"])
    axs[1].set_ylabel("USD/bbl")
    month_fmt(axs[1], lang)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "cy_prices", bottom=0.24)
    # current year: generation (months without reported data stay empty)
    fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.1))
    for ax, (ttl, cols_) in zip(axs, [(T["src"]["Hydro"], ["hydro_run_of_river", "hydro_water_reservoir"]), (T["nucl"], ["nuclear"]),
                                      (T["solar"], ["solar"])]):
        a_ = GH.loc[str(Y - 1), cols_].sum(axis=1, min_count=len(cols_))
        c_ = GH.loc[str(Y), cols_].sum(axis=1, min_count=len(cols_))
        ma, mc = a_.groupby(a_.index.month).mean() / 1000, c_.groupby(c_.index.month).mean() / 1000
        ax.plot(ma.index, ma.values, color="#222222", ls="--", marker="o", ms=3.5, label=str(Y - 1))
        ax.plot(mc.index, mc.values, color=PAL["RO"], marker="s", ms=3.5, label=T["upto"].format(y=Y, m=mlast))
        ax.set_title(ttl, fontsize=10.5)
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(MON1[lang])
        ax.set_ylim(bottom=0)
    axs[1].annotate(T["noreport"], (9, 0.12), ha="center", fontsize=8.5, rotation=90, va="bottom")
    axs[0].set_ylabel(T["gw"])
    legend_bottom(fig, ncol=2)
    out(fig, lang, "cy_generation")
    # share of generation: 2015, 2025, and Jan..cut-off of the current year (hours reported in both years)
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    yy = np.arange(len(ORDER))
    for i_, (lab_, vals_, col_) in enumerate([("2015", [share.loc[2015, k] for k in ORDER], "#9aa7b8"),
                                              (str(full_years[-1]), [share.loc[full_years[-1], k] for k in ORDER], PAL["RO"]),
                                              (T["upto"].format(y=Y, m=mlast), [L[k]["share_ytd"] for k in ORDER], PAL["DE_LU"])]):
        ax.barh(yy + (i_ - 1) * 0.27, vals_, height=0.26, color=col_, label=lab_)
    ax.set_yticks(yy)
    ax.set_yticklabels([T["src"][k] for k in ORDER])
    ax.invert_yaxis()
    ax._keep_y = True
    ax.set_xlabel(T["share"])
    legend_bottom(fig, ncol=3)
    out(fig, lang, "mix_shares", bottom=0.12)
    # one day of load: the area under the MW curve is the day's energy in MWh
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    hh = np.arange(24)
    ax.step(np.append(hh, 24), np.append(DAYLOAD.values, DAYLOAD.values[-1]), where="post", color=PAL["RO"], lw=1.6)
    ax.fill_between(np.append(hh, 24), np.append(DAYLOAD.values, DAYLOAD.values[-1]), step="post", color=PAL["RO"], alpha=0.18)
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25, 3))
    ax.set_ylim(0, DAYLOAD.max() * 1.15)
    ax.set_xlabel("ora (CET)" if lang == "ro" else "hour (CET)")
    ax.set_ylabel("MW")
    _txt = (f"aria = {N['dayload']['mwh']:,} MWh = energia zilei".replace(",", ".") if lang == "ro"
            else f"area = {N['dayload']['mwh']:,} MWh = the day's energy")
    ax.text(12, DAYLOAD.mean() * 0.5, _txt, ha="center", fontsize=9.5)
    out(fig, lang, "day_load", bottom=0.22)
    # merit order on the real OPCOM curves: midday vs evening quarter-hour of the same day
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.5), sharey=True)
    for ax, k_ in zip(axs, ["mid", "eve"]):
        m_ = N["merit"][k_]
        for side_, col_ in [("supply", PAL["RO"]), ("demand", "#222222")]:
            c_ = CURVES[(CURVES["interval"] == m_["label"]) & (CURVES["side"] == side_)]
            lab_ = {"supply": {"ro": "oferta (vînzare)", "en": "supply (sell)"}, "demand": {"ro": "cererea (cumpărare)", "en": "demand (buy)"}}[side_][lang]
            ax.plot(c_["quantity_mw"] / 1000, c_["price_eur_mwh"].clip(-190, 660), color=col_, lw=1.4, label=lab_)
        ax.axhline(m_["price"], color="#b2182b", ls="--", lw=0.9)
        ax.plot([m_["q"] / 1000], [m_["price"]], "o", color="#b2182b", ms=5)
        ptxt = f"{m_['price']:.2f}".replace(".", ",") if lang == "ro" else f"{m_['price']:.2f}"
        ax.annotate(("preț " if lang == "ro" else "price ") + ptxt, (0.05, m_["price"]), textcoords="offset points", xytext=(0, 4),
                    fontsize=8.5, color="#b2182b")
        ttl_ = {"mid": {"ro": "12:00-12:15 (amiază)", "en": "12:00-12:15 (midday)"},
                "eve": {"ro": "20:00-20:15 (seară)", "en": "20:00-20:15 (evening)"}}[k_][lang]
        ax.set_title(ttl_, fontsize=10)
        ax.set_ylim(-220, 720)
        ax.set_xlim(0, 4)
        ax.text(0.05, -175, ("ofertă la orice preț (-600)" if lang == "ro" else "sell at any price (-600)").replace("-", "−"),
                fontsize=7.5, color=PAL["RO"], va="bottom")
        ax.text(0.05, 675, "cerere la orice preț (+4000)" if lang == "ro" else "buy at any price (+4000)", fontsize=7.5, color="#222222",
                va="bottom")
        ax.set_xlabel("cantitate cumulată (GW)" if lang == "ro" else "cumulative quantity (GW)")
    axs[0].set_ylabel("EUR/MWh")
    legend_bottom(fig, ncol=2)
    out(fig, lang, "merit_opcom", bottom=0.27)
    # extremes of the current year: RO daily base price and Brent, with the highest and lowest days marked
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.3))
    ro_ = pY["RO"].dropna()
    axs[0].plot(ro_.index, ro_.values, color=PAL["RO"], lw=0.9)
    for dt_, col_ in [(ro_.idxmax(), "#b2182b"), (ro_.idxmin(), "#2166ac")]:
        axs[0].plot([dt_], [ro_[dt_]], "o", color=col_, ms=5)
        axs[0].annotate(f"{ro_[dt_]:.0f}".replace(".", ","), (dt_, ro_[dt_]), textcoords="offset points",
                        xytext=(6, -3 if col_ == "#2166ac" else -10), fontsize=8.5, color=col_)
    axs[0].set_title("RO, preț de bază zilnic (EUR/MWh)" if lang == "ro" else "RO daily base price (EUR/MWh)", fontsize=10)
    b_ = bY.dropna()
    axs[1].plot(b_.index, b_.values, color="#222222", lw=0.9)
    axs[1].plot([b_.idxmax()], [b_.max()], "o", color="#b2182b", ms=5)
    axs[1].annotate(f"{b_.max():.1f}".replace(".", ",") if lang == "ro" else f"{b_.max():.1f}", (b_.idxmax(), b_.max()),
                    textcoords="offset points", xytext=(-38, -4), fontsize=8.5, color="#b2182b")
    axs[1].set_title("Țiței Brent, închidere (USD/bbl)" if lang == "ro" else "Brent close (USD/bbl)", fontsize=10)
    for ax in axs:
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m.%Y" if lang == "ro" else "%b %Y"))
        ax.tick_params(axis="x", labelsize=8)
    out(fig, lang, "cy_extremes", bottom=0.14)
    # naive benchmark: RO, last three years
    fig, ax = plt.subplots(figsize=(6.4, 1.8))
    yrs_ = [str(y) for y in range(Y - 2, Y + 1)]
    for i_, (k_, lab_, col_) in enumerate([("naive", T["naive"], PAL["RO"]), ("lag1", "d-1", PAL["HU"]), ("lag7", "d-7", PAL["DE_LU"])]):
        ax.bar(np.arange(3) + (i_ - 1) * 0.26, [nv["RO"][y][k_] for y in yrs_], width=0.25, color=col_, label=lab_)
    ax.set_xticks(range(3))
    ax.set_xticklabels([y if y != str(Y) else f"{Y} ({T['ytd']})" for y in yrs_])
    ax.set_ylabel(T["mae"])
    legend_bottom(fig, ncol=3)
    out(fig, lang, "naive_bar", bottom=0.12)
    # RO-BG evening spread and BG batteries
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.3), sharex=True, gridspec_kw={"height_ratios": [1.4, 1]})
    xi = ev_sp.index.to_timestamp()
    axs[0].bar(xi, ev_sp.values, width=20, color=[PAL["RO"] if v >= 0 else PAL["c8"] for v in ev_sp.values], label=T["evsp"])
    axs[0].axhline(0, color="#222222", lw=0.6)
    axs[0].set_ylabel("EUR/MWh")
    bi = batm.index.to_timestamp()
    axs[1].bar(bi - pd.Timedelta(days=5), batm["battery"].values, width=9, color=PAL["HU"], label=T["bdis"])
    axs[1].bar(bi + pd.Timedelta(days=5), -batm["battery_consumption"].values, width=9, color=PAL["BG"], label=T["bch"])
    axs[1].set_ylabel(T["mw"])
    axs[1].set_xlim(pd.Timestamp("2022-12-15"), pd.Timestamp(END) + pd.Timedelta(days=20))
    axs[1].xaxis.set_major_locator(mdates.YearLocator())
    axs[1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, ncol=3)
    out(fig, lang, "bg_battery", bottom=0.14)

mE, mR = MON_EN[END.month - 1], MON_RO[END.month - 1]
fy0, fy1 = full_years[0], full_years[-1]
chart("cy_extremes", "ecyf", f"{Y}-01-01 to {d(END)}, daily",
      f"{Y}-01-01 - {d(END)}, zilnic")
chart("merit_opcom", "opc", f"{N['merit']['day']}, Romanian time; quantities include blocks, hourly orders and net flows",
      f"{N['merit']['day']}, ora României; cantitățile includ blocurile, ordinele orare și fluxurile nete")
chart("day_load", "ecg", f"Romania, load on {N['dayload']['day']} (CET day, 24 hourly values)",
      f"România, consumul din {N['dayload']['day']} (zi CET, 24 de valori orare)")
chart("mix_ro_annual", "ecg", f"{fy0}-{fy1} full years (left); Jan-{mE} {Y - 1} and {Y}, hours reported in both years (right); cut-off {d(END)}",
      f"{fy0}-{fy1} ani compleți (stînga); ian.-{mR} {Y - 1} și {Y}, ore raportate în ambii ani (dreapta); date pînă la {d(END)}")
chart("prices_daily_4zones", "ec", f"{N['data']['price_first']} to {d(END)} (BG from {N['data']['bg_first']})",
      f"{N['data']['price_first']} - {d(END)} (BG din {N['data']['bg_first']})")
chart("profile_intraday", "ec", "calendar years 2019 and 2025, hourly", "anii 2019 și 2025, date orare")
chart("profile_annual", "ec", f"monthly means 2016-{fy1}", f"medii lunare 2016-{fy1}")
chart("spikes_ro_2024", "ec", "2024, hourly (CET/CEST)", "2024, date orare (CET/CEST)")
chart("negative_prices", "ec", f"2018 to {d(END)}; a 15-min MTU counts 0.25 h", f"2018 - {d(END)}; un interval de 15 min = 0,25 h")
chart("negative_solar", "ec", f"Jan 2023 to {d(END)} (left); 2018-{fy1} (right)", f"ian. 2023 - {d(END)} (stînga); 2018-{fy1} (dreapta)")
chart("asinh_ro", "ec", f"all 15-min MTUs, {Y}-01-01 to {d(END)}", f"toate intervalele de 15 min, {Y}-01-01 - {d(END)}")
chart("tails_brent", "yf", f"{N['tails']['start']} to {N['tails']['end']}", f"{N['tails']['start']} - {N['tails']['end']}")
chart("volclust_brent", "yf", f"{N['tails']['start']} to {N['tails']['end']}", f"{N['tails']['start']} - {N['tails']['end']}")
chart("sim_wn_ar_rw", "sim", f"T = {TS}, N(0,1) shocks", f"T = {TS}, șocuri N(0,1)")
chart("acf_pacf_ro_daily", "ec", f"{N['acf']['daily']['start']} to {N['acf']['daily']['end']}, T = {TA}",
      f"{N['acf']['daily']['start']} - {N['acf']['daily']['end']}, T = {TA}")
chart("acf_ro_hourly", "ec", f"2024, hourly, T = {len(hs)}", f"2024, date orare, T = {len(hs)}")
chart("decomp_load", "ecg", f"{N['decomp']['start']} to {N['decomp']['end']}, monthly mean load",
      f"{N['decomp']['start']} - {N['decomp']['end']}, consum mediu lunar")
chart("smooth_brent", "yf", f"{N['smooth']['start']} to {N['smooth']['end']}", f"{N['smooth']['start']} - {N['smooth']['end']}")
chart("hydro_case", "ecg", f"monthly, 2015-01 to {fy1}-12", f"lunar, 2015-01 - {fy1}-12")
chart("iran_brent", "yf", "2025-06-02 to 2025-07-04, trading days", "2025-06-02 - 2025-07-04, zile de tranzacționare")
chart("separation_2024", "ec", "2024-06-01 to 2024-09-30 daily (left); 2024-07-16 hourly (right)",
      "2024-06-01 - 2024-09-30 zilnic (stînga); 2024-07-16 orar (dreapta)")
chart("cy_prices", "ec", f"{Y}-01-01 to {d(END)}, daily; Brent: Yahoo Finance (BZ=F)", f"{Y}-01-01 - {d(END)}, zilnic; Brent: Yahoo Finance (BZ=F)")
chart("cy_generation", "ecg", f"monthly means of reported hours, {Y - 1}-01 to {END:%Y-%m}",
      f"medii lunare pe orele raportate, {Y - 1}-01 - {END:%Y-%m}")
chart("mix_shares", "ecg", f"2015, {fy1} full years; Jan-{mE} {Y}, hours reported in both {Y - 1} and {Y}",
      f"2015, {fy1} ani compleți; ian.-{mR} {Y}, ore raportate și în {Y - 1}, și în {Y}")
chart("naive_bar", "ec", f"hourly day-ahead prices, {Y - 2}-01 to {END:%Y-%m}", f"prețuri PZU orare, {Y - 2}-01 - {END:%Y-%m}")
chart("bg_battery", "ecg", f"2023-01 to {END:%Y-%m}, local time; BG battery series reported from {N['bat']['bg_first']}",
      f"2023-01 - {END:%Y-%m}, ora locală; seria bateriilor BG raportată din {N['bat']['bg_first']}")

with open(os.path.join(HERE, "L1_numbers.json"), "w") as fh:
    json.dump(N, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("wrote L1_numbers.json and", len(N["charts"]), "charts x 2 languages")
