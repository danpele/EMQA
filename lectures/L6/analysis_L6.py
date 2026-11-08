"""
analysis_L6.py -- Lecture 6 "Renewables and storage: cannibalisation, negative prices and batteries" (EMQA)
=========================================================================================================
Reads the real series in repo/data/clean (data/SOURCES.md; the 15-min generation files and the installed capacity come
from data/download_L6.py), computes every number shown on the slides and writes
    lectures/L6/L6_numbers.json        all results (the deck builder reads ONLY this file)
    lectures/L6/charts/en/*.pdf        figures with English labels
    lectures/L6/charts/ro/*.pdf        the same figures with Romanian labels
    lectures/L6/cache/battery.pkl      battery optimisation results (recomputed when the price data change)
Run:  python3 lectures/L6/analysis_L6.py        (add --fresh to ignore the cache)

Conventions (lectures/README.md, rule 3)
  * Cut-off = last complete month. Calendar = CET/CEST (Europe/Brussels) delivery day. Missing values stay missing.
  * Prices: hourly MTU to 30 Sep 2025, 15-min MTU from 1 Oct 2025 (SDAC). Energy = sum of mean MW x interval length.
  * Generation on the price grid: hourly price -> hourly mean of the generation; 15-min price -> the 15-min generation
    (Romania, Hungary); Bulgaria publishes hourly generation only, so after 1 Oct 2025 its hourly generation is paired
    with each of the four quarter-hours (stated on the slide).
  * Counts of events in hour-equivalents (a 15-min MTU = 0.25 h); means of prices are duration-weighted means of signed prices.
  * Battery: 1 MW, 1 / 2 / 4 h of storage, round-trip efficiency 85%, at most one full cycle per day, empty at the start and
    at the end of each delivery day (Cole & Karmakar, 2023, NREL); linear programme per day (scipy HiGHS).
  * No simulated data in this lecture.
"""

import hashlib
import json
import os
import pickle
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import sparse
from scipy.optimize import linprog

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
FRESH = "--fresh" in sys.argv
N = {"charts": {}}
ZONES = ["RO", "BG", "HU", "DE_LU"]
MON_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MON_RO = ["ian.", "feb.", "mar.", "apr.", "mai", "iun.", "iul.", "aug.", "sep.", "oct.", "nov.", "dec."]
ETA, CYCLES, DURS = 0.85, 1.0, (1, 2, 4)       # battery assumptions (NREL 2023 update): 85% round trip, 1 cycle/day
R_DISC, LIFE = 0.08, 15                         # discount rate (assumption) and lifetime in years (NREL 2023 update)


def d(ts):
    return pd.Timestamp(ts).strftime("%Y-%m-%d")


def fl(x, k=4):
    if x is None:
        return None
    x = float(x)
    return None if np.isnan(x) else round(x, k)


# =============================================================================
# 0. Load data and cut-off
# =============================================================================
PX = ep.prices_native()                                   # Brussels-time index, 60-min to Sep 2025 then 15-min
PX["dur"] = PX["mtu_minutes"] / 60.0
_last = min(PX["RO"].dropna().index.max().tz_localize(None), pd.Timestamp("2099-01-01"))
GN = {}
for c in ("ro", "bg", "hu"):
    g = pd.read_csv(os.path.join(DATA, f"generation_{c}_mw_native_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
    g.index = g.index.tz_convert(TZ)
    GN[c.upper()] = g
_glast = GN["RO"]["solar"].dropna().index.max().tz_localize(None)
_raw_last = min(_last, _glast)
END = pd.Timestamp(((_raw_last + pd.Timedelta(days=1)).to_period("M").to_timestamp() - pd.Timedelta(days=1)).date())
END_X = (END + pd.Timedelta(days=1)).tz_localize(TZ)     # exclusive end (00:00 of the first day after the cut-off)
N["cutoff"] = {"end": d(END), "year": END.year, "month": int(END.month), "download": "2026-11-06",
               "ltm_start": d((END + pd.Timedelta(days=1)) - pd.DateOffset(years=1)), "ltm_end": d(END)}
Y = END.year
N["Y"], N["YP"] = Y, Y - 1
PX = PX[PX.index < END_X]
MTU15 = pd.Timestamp("2025-10-01").tz_localize(TZ)
LTM0 = pd.Timestamp(N["cutoff"]["ltm_start"]).tz_localize(TZ)
CAP = pd.read_csv(os.path.join(DATA, "installed_capacity_yearly.csv"))
YEARS = list(range(2019, Y + 1))
N["data"] = {"first_year": YEARS[0], "n_mtu15": int((PX["mtu_minutes"] == 15).sum()), "mtu15_start": "2025-10-01",
             "ytd_label_en": f"Jan--{MON_EN[END.month - 1]} {Y}", "ytd_label_ro": f"ian.--{MON_RO[END.month - 1].rstrip('.')}. {Y}"}


def hfloor(idx):
    """Start of the clock hour, computed in UTC (no ambiguity on the autumn DST day)."""
    return idx.tz_convert("UTC").floor("1h").tz_convert(TZ)


def on_price_grid(zone, gen):
    """Generation columns on the price grid of `zone`: hourly mean for hourly prices; 15-min value for 15-min prices
    (hourly value repeated when the source is hourly, as for Bulgaria). Returns a DataFrame aligned to PX.index."""
    g = GN[gen].drop(columns=["mtu_minutes"]).copy()
    hourly = g.resample("1h").mean()
    out = hourly.reindex(hfloor(PX.index)).set_axis(PX.index)
    q15 = PX["mtu_minutes"] == 15
    if (GN[gen]["mtu_minutes"] == 15).loc[GN[gen].index >= MTU15].all():
        g15 = g.resample("15min").mean()
        out.loc[q15] = g15.reindex(PX.index[q15]).values
    return out


GR = {z: on_price_grid(z, z) for z in ("RO", "BG", "HU")}
LOC_YEAR = PX.index.year
LOC_MONTH = PX.index.to_period("M")


def wmean(p, w):
    m = p.notna() & w.notna()
    return float((p[m] * w[m]).sum() / w[m].sum()) if w[m].sum() > 0 else np.nan


# =============================================================================
# 1. Context: installed capacity and metered output
# =============================================================================
cap = CAP[CAP["type"].str.startswith("Solar")]
N["cap"] = {"solar": {z: {str(int(r.year)): fl(r.gw, 2) for r in cap[cap.country == z].itertuples()} for z in ("RO", "BG", "HU")},
            "wind": {z: {str(int(r.year)): fl(r.gw, 2) for r in CAP[(CAP.country == z) & (CAP.type == "Wind onshore")].itertuples()}
                     for z in ("RO", "BG", "HU")},
            "last_year": int(CAP["year"].max())}
N["cap"]["solar_ro_x"] = fl(N["cap"]["solar"]["RO"][str(N["cap"]["last_year"])] / N["cap"]["solar"]["RO"]["2019"], 1)
ro = GR["RO"]
twh = {}
for y in YEARS:
    m = (LOC_YEAR == y)
    twh[str(y)] = {"solar": fl((ro["solar"][m] * PX["dur"][m]).sum() / 1e6, 2), "wind": fl((ro["wind_onshore"][m] * PX["dur"][m]).sum() / 1e6, 2),
                   "load": fl((ro["load"][m] * PX["dur"][m]).sum() / 1e6, 2)}
# like-for-like Jan..cut-off month
lfl = {}
for y in (Y - 1, Y):
    m = (LOC_YEAR == y) & (PX.index.month <= END.month)
    lfl[str(y)] = {"solar": fl((ro["solar"][m] * PX["dur"][m]).sum() / 1e6, 2), "wind": fl((ro["wind_onshore"][m] * PX["dur"][m]).sum() / 1e6, 2)}
lfl["solar_chg"] = fl((lfl[str(Y)]["solar"] / lfl[str(Y - 1)]["solar"] - 1) * 100, 1)
N["twh"], N["twh_lfl"] = twh, lfl
_mx = ro["solar"][LOC_YEAR == Y]
N["twh"]["solar_max_mw"] = fl(_mx.max(), 0)
N["twh"]["solar_max_ts"] = _mx.idxmax().strftime("%Y-%m-%d %H:%M")
N["twh"]["solar_share_load_ytd"] = fl(twh[str(Y)]["solar"] / twh[str(Y)]["load"] * 100, 1)
N["twh"]["solar_share_load_2019"] = fl(twh["2019"]["solar"] / twh["2019"]["load"] * 100, 1)

# =============================================================================
# 2. Merit-order effect on the real OPCOM aggregated curves (one day, two quarter-hours)
# =============================================================================
CURVES = pd.read_csv(os.path.join(DATA, "opcom_pzu_curves.csv"))
CMETA = json.load(open(os.path.join(DATA, "opcom_pzu_curves_meta.json")))


def curve_fns(lab):
    """Cumulative supply S(p) (MW offered at prices <= p) and demand D(p) (MW bid at prices >= p), piecewise linear in
    the published points; ties in price are separated by 1e-7 EUR/MWh so the functions are single-valued."""
    s = CURVES[(CURVES["interval"] == lab) & (CURVES["side"] == "supply")]
    dm = CURVES[(CURVES["interval"] == lab) & (CURVES["side"] == "demand")]
    ps = s["price_eur_mwh"].values + np.arange(len(s)) * 1e-7
    pdm = dm["price_eur_mwh"].values[::-1] + np.arange(len(dm)) * 1e-7
    qs, qd = s["quantity_mw"].values, dm["quantity_mw"].values[::-1]
    return (lambda p: np.interp(p, ps, qs)), (lambda p: np.interp(p, pdm, qd))


def clear(S, D, xs=0.0, xd=0.0, p_s=0.0):
    """Clearing price after adding xs MW of supply offered at p_s and xd MW of demand bid at any price: lowest p with
    S(p) + xs*1[p >= p_s] >= D(p) + xd (bisection on the monotone excess supply)."""
    lo, hi = -600.0, 4000.0
    for _ in range(70):
        m_ = 0.5 * (lo + hi)
        if S(m_) + xs * (m_ >= p_s) - D(m_) - xd >= 0:
            hi = m_
        else:
            lo = m_
    return hi


XGRID = np.arange(0, 401, 5)
N["merit"] = {"day": CURVES["delivery_date"].iloc[0]}
MERIT = {}
for iv in CMETA["intervals"]:
    k = "mid" if iv["opcom_interval"] == 45 else "eve"
    S, D_ = curve_fns(iv["interval_label"])
    P0 = iv["official_clearing_price_eur_mwh"]
    q0 = iv["curve_cleared_quantity_mw"]
    sup = np.array([clear(S, D_, xs=x) if x > 0 else P0 for x in XGRID])
    dem = np.array([clear(S, D_, xd=x) if x > 0 else P0 for x in XGRID])
    MERIT[k] = (sup, dem)
    lo_ = clear(S, D_)                              # lowest price consistent with the curves (official = inside the range)
    N["merit"][k] = {"price": P0, "q": q0, "p_curve_low": fl(lo_, 2),
                     "depth_1_to_p": fl(S(P0) - S(1.0), 0),       # MW offered between 1 EUR/MWh and the clearing price
                     "q_le0": fl(CURVES[(CURVES["interval"] == iv["interval_label"]) & (CURVES["side"] == "supply") &
                                         (CURVES["price_eur_mwh"] <= 0)]["quantity_mw"].max(), 0), "net_imp": fl(-iv["net_export_mw"], 0),
                     "sup": {str(x): fl(v, 2) for x, v in zip(XGRID, sup) if x in (25, 50, 100, 200, 300)},
                     "dem": {str(x): fl(v, 2) for x, v in zip(XGRID, dem) if x in (25, 50, 100, 200, 300)},
                     "x_below50": int(XGRID[np.argmax(sup < 50)]) if (sup < 50).any() else None}
# a battery fleet of X MW charging in the midday quarter-hour and discharging in the evening one
N["merit"]["spread0"] = fl(N["merit"]["eve"]["price"] - N["merit"]["mid"]["price"], 2)
for x in (50, 100, 200):
    N["merit"][f"spread_bat{x}"] = fl(N["merit"]["eve"]["sup"][str(x)] - N["merit"]["mid"]["dem"][str(x)], 2)

# =============================================================================
# 3. Price and residual load: hourly regression (coupled market), 2023 to the cut-off
# =============================================================================
H = pd.DataFrame({"P": PX["RO"], "dur": PX["dur"], "load": ro["load"], "wind": ro["wind_onshore"], "solar": ro["solar"]})
H = H[H.index >= pd.Timestamp("2023-01-01").tz_localize(TZ)]
HH = (H[["P", "load", "wind", "solar"]].mul(H["dur"], axis=0).groupby(hfloor(H.index)).sum()
      .div(H["dur"].groupby(hfloor(H.index)).sum(), axis=0)).dropna()           # hourly means (15-min prices averaged to the hour)
HH = HH[HH.index < END_X]
for c in ("load", "wind", "solar"):
    HH[c] = HH[c] / 1000.0                                             # GW
HH["resid"] = HH["load"] - HH["wind"] - HH["solar"]
fe = pd.get_dummies(pd.DataFrame({"m": HH.index.strftime("%Y-%m"), "h": HH.index.hour.astype(str), "w": HH.index.dayofweek.astype(str)}),
                    drop_first=True).astype(float)
fe.index = HH.index
X1 = sm.add_constant(pd.concat([HH[["load", "wind", "solar"]], fe], axis=1))
R1 = sm.OLS(HH["P"], X1).fit(cov_type="HAC", cov_kwds={"maxlags": 48})
X2 = sm.add_constant(pd.concat([HH[["resid"]], fe], axis=1))
R2 = sm.OLS(HH["P"], X2).fit(cov_type="HAC", cov_kwds={"maxlags": 48})
N["reg"] = {"start": d(HH.index.min()), "end": d(END), "n": int(len(HH)), "r2": fl(R1.rsquared, 3), "r2_resid": fl(R2.rsquared, 3),
            "n_fe_months": int(HH.index.strftime("%Y-%m").nunique())}
for c in ("load", "wind", "solar"):
    N["reg"][c] = {"b": fl(R1.params[c], 2), "se": fl(R1.bse[c], 2), "t": fl(R1.tvalues[c], 1)}
N["reg"]["resid"] = {"b": fl(R2.params["resid"], 2), "se": fl(R2.bse["resid"], 2), "t": fl(R2.tvalues["resid"], 1)}
_sol_ytd = HH["solar"][HH.index.year == Y]
N["reg"]["solar_babs"] = fl(-R1.params["solar"], 1)
N["reg"]["solar_mean_day_gw"] = fl(_sol_ytd[(_sol_ytd.index.hour >= 11) & (_sol_ytd.index.hour < 15)].mean(), 2)
N["reg"]["solar_effect_midday"] = fl(R1.params["solar"] * N["reg"]["solar_mean_day_gw"], 1)
# binned price vs residual load for the chart
BINS = np.arange(-2.0, 9.01, 0.5)
RBIN = {}
for y in (2023, Y - 1, Y):
    s_ = HH[HH.index.year == y]
    b_ = pd.cut(s_["resid"], BINS)
    g_ = s_.groupby(b_, observed=True)["P"].agg(["mean", "count"])
    g_ = g_[g_["count"] >= 20]
    RBIN[y] = (np.array([iv.mid for iv in g_.index]), g_["mean"].values)
    N["reg"][f"share_resid_below2_{y}"] = fl((s_["resid"] < 2).mean() * 100, 1)
N["reg"]["p_resid_low"] = {str(y): fl(HH[(HH.index.year == y) & (HH["resid"] < 2)]["P"].mean(), 1) for y in (2023, Y - 1, Y)}
N["reg"]["p_resid_high"] = {str(y): fl(HH[(HH.index.year == y) & (HH["resid"] > 6)]["P"].mean(), 1) for y in (2023, Y - 1, Y)}

# =============================================================================
# 4. Capture prices and capture rates
# =============================================================================
def capture(zone, tech, mask):
    p, w = PX[zone], GR[zone if zone != "DE_LU" else "RO"][tech] * PX["dur"]
    m = mask & p.notna() & w.notna()
    base_m = mask & p.notna()
    cp = float((p[m] * w[m]).sum() / w[m].sum())
    base = float((p[base_m] * PX["dur"][base_m]).sum() / PX["dur"][base_m].sum())
    return cp, base, float(w[m].sum())


CAPT = {}
for z in ("RO", "BG", "HU"):
    for tech in ("solar", "wind_onshore"):
        for y in YEARS:
            m = pd.Series(LOC_YEAR == y, index=PX.index)
            if GR[z][tech][m].notna().sum() < 0.9 * m.sum():
                continue
            cp, base, e = capture(z, tech, m)
            CAPT[(z, tech, y)] = (cp, base, cp / base, e)
N["capt"] = {}
for (z, tech, y), (cp, base, cr, e) in CAPT.items():
    N["capt"].setdefault(z, {}).setdefault("solar" if tech == "solar" else "wind", {})[str(y)] = {
        "cp": fl(cp, 1), "base": fl(base, 1), "cr": fl(cr, 3), "crp": fl(cr * 100, 1), "disc": fl(base - cp, 1), "twh": fl(e / 1e6, 2)}
cr_ro = N["capt"]["RO"]["solar"]
N["capt"]["RO"]["solar_first_below1"] = next(int(y) for y in cr_ro if cr_ro[y]["cr"] < 1 and int(y) >= 2023) if any(
    cr_ro[y]["cr"] < 1 for y in cr_ro) else None
_w = [N["capt"]["RO"]["wind"][y]["crp"] for y in N["capt"]["RO"]["wind"]]
N["capt"]["RO"]["wind_min"], N["capt"]["RO"]["wind_max"] = min(_w), max(_w)
N["capt"]["RO"]["solar_min_year"] = min(cr_ro, key=lambda y: cr_ro[y]["cr"])
# covariance identity check: CR = 1 + Cov(P, g) / (mean P * mean g)  (duration weights)
m = pd.Series(LOC_YEAR == Y, index=PX.index) & PX["RO"].notna() & ro["solar"].notna()
p_, g_, w_ = PX["RO"][m], ro["solar"][m], PX["dur"][m]
mp, mg = np.average(p_, weights=w_), np.average(g_, weights=w_)
cov_ = np.average((p_ - mp) * (g_ - mg), weights=w_)
N["capt"]["cov"] = {"mp": fl(mp, 1), "mg": fl(mg, 0), "cov": fl(cov_, 0), "cr": fl(1 + cov_ / (mp * mg), 3),
                    "corr": fl(np.corrcoef(p_, g_)[0, 1], 3)}
# monthly cannibalisation: capture rate vs solar share of load (energy), RO / BG / HU
MON = {}
for z in ("RO", "BG", "HU"):
    rows = []
    for per in pd.period_range("2019-01", END.strftime("%Y-%m"), freq="M"):
        mk = pd.Series(LOC_MONTH == per, index=PX.index)
        s_ = GR[z]["solar"][mk]
        if s_.notna().sum() < 0.9 * mk.sum() or PX[z][mk].notna().sum() < 0.9 * mk.sum():
            continue
        cp, base, e = capture(z, "solar", mk)
        ld = (GR[z]["load"][mk] * PX["dur"][mk]).sum()
        rows.append((per.to_timestamp(), cp / base * 100, e / ld * 100, base))
    MON[z] = pd.DataFrame(rows, columns=["month", "cr", "share", "base"]).set_index("month")
mr = MON["RO"]
Rc = sm.OLS(mr["cr"], sm.add_constant(mr["share"])).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
mrb = mr[mr["base"] > 0]
N["cannib"] = {"b": fl(Rc.params["share"], 2), "se": fl(Rc.bse["share"], 2), "a": fl(Rc.params["const"], 1), "r2": fl(Rc.rsquared, 2),
               "n": int(len(mr)), "start": d(mr.index.min()), "end": d(mr.index.max()),
               "share_max": fl(mr["share"].max(), 1), "share_max_month": mr["share"].idxmax().strftime("%Y-%m"),
               "cr_min": fl(mr["cr"].min(), 1), "cr_min_month": mr["cr"].idxmin().strftime("%Y-%m")}
N["cannib"]["bneg"] = fl(-Rc.params["share"], 1)
for z in ("BG", "HU"):
    rz = sm.OLS(MON[z]["cr"], sm.add_constant(MON[z]["share"])).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
    N["cannib"][z] = {"b": fl(rz.params["share"], 2), "se": fl(rz.bse["share"], 2), "n": int(len(MON[z]))}
# solar energy sold in the cheapest hours of each year
LOR = {}
N["cheap"] = {}
for y in YEARS:
    m = (LOC_YEAR == y) & PX["RO"].notna().values & ro["solar"].notna().values
    p_, g_, w_ = PX["RO"][m].values, ro["solar"][m].values, PX["dur"][m].values
    o = np.argsort(p_, kind="stable")
    tsh = np.cumsum(w_[o]) / w_.sum()
    esh = np.cumsum((g_ * w_)[o]) / (g_ * w_).sum()
    LOR[y] = (tsh, esh)
    k10 = np.searchsorted(tsh, 0.10)
    N["cheap"][str(y)] = {"e_in_cheap10": fl(esh[k10] * 100, 1),
                          "e_le0": fl((g_ * w_)[p_ <= 0].sum() / (g_ * w_).sum() * 100, 1),
                          "e_neg": fl((g_ * w_)[p_ < 0].sum() / (g_ * w_).sum() * 100, 1),
                          "p10": fl(p_[o][k10], 1)}

# =============================================================================
# 5. Negative prices
# =============================================================================
N["neg"] = {"hours": {}, "depth": {}, "lfl": {}}
for z in ZONES:
    N["neg"]["hours"][z], N["neg"]["depth"][z] = {}, {}
    for y in YEARS:
        m = (LOC_YEAR == y) & (PX[z] < 0).values
        N["neg"]["hours"][z][str(y)] = fl(PX["dur"][m].sum(), 2)
        N["neg"]["depth"][z][str(y)] = fl(wmean(PX[z][m], PX["dur"][m]), 1) if m.any() else None
    for y in (Y - 1, Y):
        m = (LOC_YEAR == y) & (PX.index.month <= END.month) & (PX[z] < 0).values
        N["neg"]["lfl"].setdefault(z, {})[str(y)] = fl(PX["dur"][m].sum(), 2)
    N["neg"]["lfl"][z]["x"] = fl(N["neg"]["lfl"][z][str(Y)] / N["neg"]["lfl"][z][str(Y - 1)], 2) if N["neg"]["lfl"][z][str(Y - 1)] else None
_ny = PX["RO"][(LOC_YEAR == Y)]
N["neg"]["ro_min"] = fl(_ny.min(), 2)
N["neg"]["ro_min_ts"] = _ny.idxmin().strftime("%Y-%m-%d %H:%M")
# solar output in negative intervals and the value of switching off (curtailment) when the price is negative
CURT = {}
for y in (2023, 2024, 2025, Y):
    m = (LOC_YEAR == y) & PX["RO"].notna().values & ro["solar"].notna().values
    p_, e_ = PX["RO"][m], ro["solar"][m] * PX["dur"][m]
    rev, rev_c = (p_ * e_).sum(), (p_.clip(lower=0) * e_).sum()
    CURT[y] = {"rev_mwh": fl(rev / e_.sum(), 2), "rev_curt_mwh": fl(rev_c / e_[p_ >= 0].sum(), 2),
               "gain_mwh_all": fl((rev_c - rev) / e_.sum(), 2), "e_neg_pct": fl(e_[p_ < 0].sum() / e_.sum() * 100, 1),
               "cost_neg_meur": fl(-(p_[p_ < 0] * e_[p_ < 0]).sum() / 1e6, 2)}
N["curt"] = {str(k): v for k, v in CURT.items()}
# 15-min MTU: negative quarter-hours hidden inside hours with a non-negative average
q = PX.loc[PX.index >= MTU15, ["RO", "dur"]].copy()
q["hm"] = q["RO"].groupby(hfloor(q.index)).transform("mean")
negq = q["RO"] < 0
N["neg"]["q15"] = {"n_negq": int(negq.sum()), "h_negq": fl(negq.sum() * 0.25, 2),
                   "n_hidden": int((negq & (q["hm"] >= 0)).sum()), "n_neg_hours_avg": int((q.groupby(hfloor(q.index))["RO"].mean() < 0).sum()),
                   "start": "2025-10-01", "end": d(END)}
N["neg"]["q15"]["hidden_pct"] = fl(N["neg"]["q15"]["n_hidden"] / max(N["neg"]["q15"]["n_negq"], 1) * 100, 1)
# negative hour-equivalents by month (RO), for the case study
NEGM = PX.loc[PX["RO"] < 0, "dur"].groupby(PX.index[PX["RO"] < 0].to_period("M")).sum()
_ny_m = NEGM[[p.year == Y for p in NEGM.index]]
N["neg"]["top_month"] = str(_ny_m.idxmax())
N["neg"]["top_month_h"] = fl(_ny_m.max(), 2)

# =============================================================================
# 6. Intraday shape and daily spreads
# =============================================================================
qq = PX.loc[(PX.index >= LTM0) & (PX.index >= MTU15), ["RO", "HU", "BG", "DE_LU"]].copy()
qq["slot"] = qq.index.hour * 4 + qq.index.minute // 15
SEAS = {"winter": [12, 1, 2], "spring": [3, 4, 5], "summer": [6, 7, 8], "autumn": [9, 10, 11]}
PROF = {s: qq[qq.index.month.isin(ms)].groupby("slot")["RO"].mean() for s, ms in SEAS.items()}
N["shape"] = {}
for s, pr in PROF.items():
    N["shape"][s] = {"min": fl(pr.min(), 1), "min_t": f"{pr.idxmin() // 4:02d}:{pr.idxmin() % 4 * 15:02d}", "max": fl(pr.max(), 1),
                     "max_t": f"{pr.idxmax() // 4:02d}:{pr.idxmax() % 4 * 15:02d}", "range": fl(pr.max() - pr.min(), 1)}


def day_groups(zone, start=None, end=None, hourly=False):
    """Prices per CET delivery day (complete days only: 23/24/25 hours or 92/96/100 quarter-hours)."""
    s = PX[[zone, "dur"]]
    if start is not None:
        s = s[s.index >= start]
    if end is not None:
        s = s[s.index < end]
    if hourly:
        s = s.groupby(hfloor(s.index)).agg({zone: "mean", "dur": "sum"})
    out = {}
    for dd, g in s.groupby(s.index.tz_localize(None).normalize()):
        if g[zone].notna().all() and abs(g["dur"].sum() - round(g["dur"].sum())) < 1e-9 and round(g["dur"].sum()) in (23, 24, 25):
            out[dd] = (g[zone].values.astype(float), g["dur"].values.astype(float))
    return out


def tbk(p, dur, k):
    """Top-k minus bottom-k hours spread of one day (duration-weighted means of the k most expensive / cheapest hours)."""
    o = np.argsort(p)
    def avg(idx):
        w, acc, tot = dur[idx], 0.0, 0.0
        for i_, wi in zip(idx, w):
            take = min(wi, k - tot)
            if take <= 0:
                break
            acc += p[i_] * take
            tot += take
        return acc / tot
    return avg(o[::-1]) - avg(o)


SPR = {}
for z in ZONES:
    dg = day_groups(z, start=pd.Timestamp("2019-01-01").tz_localize(TZ), hourly=True)
    SPR[z] = pd.Series({dd: tbk(p, w, 2) for dd, (p, w) in dg.items()})
N["spread"] = {z: {str(y): fl(SPR[z][SPR[z].index.year == y].mean(), 1) for y in YEARS} for z in ZONES}
SPRM = {z: SPR[z].groupby(SPR[z].index.to_period("M")).mean() for z in ZONES}

# =============================================================================
# 7. Battery arbitrage: linear programme per delivery day
# =============================================================================
def battery_day(p, dur, E, P=1.0, eta=ETA, cycles=CYCLES):
    """Optimal charge c_t and discharge d_t (MW) of a P-MW / E-MWh battery for one day of prices p_t (EUR/MWh) and
    interval lengths dur_t (h). max sum_t p_t (d_t - c_t) dur_t  s.t.  s_t = s_{t-1} + sqrt(eta) c_t dur_t - d_t dur_t / sqrt(eta),
    0 <= s_t <= E, s_0 = s_T = 0, 0 <= c_t, d_t <= P, sum_t d_t dur_t / sqrt(eta) <= cycles * E.  Returns (c, d)."""
    n = len(p)
    r = np.sqrt(eta)
    cost = np.concatenate([p * dur, -p * dur, np.zeros(n)])
    I = sparse.identity(n, format="csr")
    Lw = sparse.diags([np.ones(n), -np.ones(n - 1)], [0, -1], format="csr")         # s_t - s_{t-1}
    A_eq = sparse.hstack([-r * sparse.diags(dur), sparse.diags(dur / r), Lw], format="csr")
    A_eq = sparse.vstack([A_eq, sparse.hstack([sparse.csr_matrix((1, 2 * n)), sparse.csr_matrix(([1.0], ([0], [n - 1])), shape=(1, n))])])
    b_eq = np.zeros(n + 1)
    A_ub = sparse.hstack([sparse.csr_matrix((1, n)), sparse.csr_matrix(dur / r), sparse.csr_matrix((1, n))], format="csr")
    bounds = [(0, P)] * (2 * n) + [(0, E)] * n
    res = linprog(cost, A_ub=A_ub, b_ub=[cycles * E], A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    x = res.x
    del I
    return x[:n], x[n:2 * n]


def revenue(p, dur, c, dd_):
    return float(np.sum(p * (dd_ - c) * dur))


def run_battery(dg, E, forecast=None):
    """Daily revenue (EUR per MW) with perfect foresight, or with the schedule optimised on `forecast` (dict day -> prices)."""
    out = {}
    for day, (p, w) in dg.items():
        if forecast is None:
            c, dch = battery_day(p, w, E)
        else:
            f = forecast.get(day)
            if f is None or len(f) != len(p):
                continue
            c, dch = battery_day(f, w, E)
        out[day] = revenue(p, w, c, dch)
    return pd.Series(out)


def yesterday(dg):
    """Forecast for day d = the prices of day d-1 (known at gate closure on d-1)."""
    return {day: dg[day - pd.Timedelta(days=1)][0] for day in dg if (day - pd.Timedelta(days=1)) in dg}


def week_ago_mean(dg):
    """Forecast for day d = mean profile of days d-1 ... d-7 with the same number of intervals (known at gate closure)."""
    out = {}
    for day in dg:
        past = [dg[day - pd.Timedelta(days=j)][0] for j in range(1, 8) if (day - pd.Timedelta(days=j)) in dg and
                len(dg[day - pd.Timedelta(days=j)][0]) == len(dg[day][0])]
        if len(past) >= 5:
            out[day] = np.mean(past, axis=0)
    return out


CACHE = os.path.join(HERE, "cache", "battery.pkl")
os.makedirs(os.path.dirname(CACHE), exist_ok=True)
KEY = hashlib.md5(pd.util.hash_pandas_object(PX[ZONES].fillna(-9999)).values.tobytes() + b"L6-bat-v2").hexdigest()
if os.path.exists(CACHE) and not FRESH:
    BAT = pickle.load(open(CACHE, "rb"))
    if BAT.get("key") != KEY:
        BAT = None
else:
    BAT = None
if BAT is None:
    print("battery optimisation (several thousand daily linear programmes) ...")
    BAT = {"key": KEY}
    T0 = pd.Timestamp("2019-01-01").tz_localize(TZ)
    dg_ro = day_groups("RO", start=T0)
    for E in DURS:
        BAT[("RO", E, "pf")] = run_battery(dg_ro, E)
    ltm_native = {z: day_groups(z, start=LTM0) for z in ZONES}
    ltm_hourly = {z: day_groups(z, start=LTM0, hourly=True) for z in ZONES}
    dg_ro_ext = day_groups("RO", start=LTM0 - pd.Timedelta(days=8))
    for E in DURS:
        BAT[("RO", E, "ltm_hourly")] = run_battery(ltm_hourly["RO"], E)
        BAT[("RO", E, "ltm_yday")] = run_battery(ltm_native["RO"], E, yesterday(dg_ro_ext))
        BAT[("RO", E, "ltm_wk")] = run_battery(ltm_native["RO"], E, week_ago_mean(dg_ro_ext))
    for z in ("BG", "HU", "DE_LU"):
        BAT[(z, 2, "ltm")] = run_battery(ltm_native[z], 2)
    T1 = pd.Timestamp("2024-01-01").tz_localize(TZ)
    for z in ("BG", "HU"):
        BAT[(z, 2, "pf24")] = run_battery(day_groups(z, start=T1), 2)
    pickle.dump(BAT, open(CACHE, "wb"))

LTM_DAYS = lambda s: s[s.index >= LTM0.tz_localize(None)]  # noqa: E731
N["bat"] = {"eta": ETA, "cycles": CYCLES, "r": R_DISC, "life": LIFE, "pf": {}, "ltm": {}, "reg": {}}
for E in DURS:
    s = BAT[("RO", E, "pf")]
    N["bat"]["pf"][str(E)] = {str(y): fl(s[s.index.year == y].sum() / 1000, 1) for y in YEARS if y < Y}
    lt = LTM_DAYS(s)
    hr = BAT[("RO", E, "ltm_hourly")]
    yd, wk = BAT[("RO", E, "ltm_yday")], BAT[("RO", E, "ltm_wk")]
    common = lt.index.intersection(yd.index).intersection(wk.index)
    N["bat"]["ltm"][str(E)] = {"pf": fl(lt.sum() / 1000, 1), "n_days": int(len(lt)), "per_day": fl(lt.mean(), 0),
                               "hourly": fl(hr.reindex(lt.index).sum() / 1000, 1),
                               "gain15": fl((lt.sum() / hr.reindex(lt.index).sum() - 1) * 100, 1),
                               "yday_pct": fl(yd[common].sum() / lt[common].sum() * 100, 1),
                               "wk_pct": fl(wk[common].sum() / lt[common].sum() * 100, 1),
                               "wk": fl(wk[common].sum() / 1000, 1), "yday": fl(yd[common].sum() / 1000, 1),
                               "n_common": int(len(common)), "loss_days_wk": int((wk[common] < 0).sum()),
                               "per_mwh": fl(lt.sum() / E / 1000, 1)}
    # break-even capital cost (EUR per kW) supported by this revenue: annuity factor, no O&M
    af = (1 - (1 + R_DISC) ** -LIFE) / R_DISC
    N["bat"]["ltm"][str(E)]["capex_pf_kw"] = fl(lt.sum() * 365 / len(lt) * af / 1000, 0)
    N["bat"]["ltm"][str(E)]["capex_wk_kw"] = fl(wk[common].sum() * 365 / len(common) * af / 1000, 0)
    N["bat"]["ltm"][str(E)]["capex_wk_kwh"] = fl(N["bat"]["ltm"][str(E)]["capex_wk_kw"] / E, 0)
N["bat"]["x_4v2"] = fl(N["bat"]["ltm"]["4"]["pf"] / N["bat"]["ltm"]["2"]["pf"], 2)
N["bat"]["x_ltm_vs_prev"] = fl((N["bat"]["ltm"]["2"]["pf"] / N["bat"]["pf"]["2"][str(Y - 1)] - 1) * 100, 1)
N["bat"]["af"] = fl((1 - (1 + R_DISC) ** -LIFE) / R_DISC, 2)
N["bat"]["pf_first"] = YEARS[0]
N["bat"]["pf_last"] = Y - 1
for z in ("RO", "BG", "HU", "DE_LU"):
    s = LTM_DAYS(BAT[("RO", 2, "pf")]) if z == "RO" else BAT[(z, 2, "ltm")]
    N["bat"]["reg"][z] = fl(s.sum() / 1000, 1)
_rb = pd.concat([LTM_DAYS(BAT[("RO", 2, "pf")]), BAT[("BG", 2, "ltm")]], axis=1).dropna()
N["bat"]["corr_ro_bg"] = fl(_rb.corr().iloc[0, 1], 2)
_rh = pd.concat([LTM_DAYS(BAT[("RO", 2, "pf")]), BAT[("HU", 2, "ltm")]], axis=1).dropna()
N["bat"]["corr_ro_hu"] = fl(_rh.corr().iloc[0, 1], 2)
# monthly 2h revenue, RO and BG, 2024 to the cut-off, and the battery fleets (mean discharge MW) from the generation data
BM = {"RO": BAT[("RO", 2, "pf")], "BG": BAT[("BG", 2, "pf24")], "HU": BAT[("HU", 2, "pf24")]}
BMM = {z: s[s.index >= pd.Timestamp("2024-01-01")].groupby(s[s.index >= pd.Timestamp("2024-01-01")].index.to_period("M")).mean() for z, s in BM.items()}
FLEET = {}
for z in ("RO", "BG"):
    b = GN[z]["battery"] if "battery" in GN[z] else None
    FLEET[z] = b[b.index >= pd.Timestamp("2024-01-01").tz_localize(TZ)].groupby(b[b.index >= pd.Timestamp("2024-01-01").tz_localize(TZ)].index.to_period("M")).mean()
    fb = b.dropna()
    N["bat"][f"fleet_{z}_first"] = d(fb.index.min()) if len(fb) else None
    _ly = b[(b.index >= pd.Timestamp(f"{Y}-01-01").tz_localize(TZ)) & (b.index < END_X)]
    N["bat"][f"fleet_{z}_max"] = fl(_ly.max(), 0)
    _q = b[(b.index.month.isin([6, 7, 8])) & (b.index.year == Y)]
    N["bat"][f"fleet_{z}_mean_summer"] = fl(_q.mean(), 0)
_bgc = GN["BG"]["battery_consumption"].dropna()
N["bat"]["fleet_BG_charge_max"] = fl(-_bgc.min(), 0) if len(_bgc) else None
for z in ("RO", "BG"):
    for y in (Y - 1, Y):
        s = BMM[z][[p.year == y and p.month in (5, 6, 7, 8, 9) for p in BMM[z].index]]
        N["bat"][f"m_{z}_{y}"] = fl(s.mean(), 0)                     # mean daily revenue May-Sep, EUR per MW
# best 2h day of the last 12 months and its schedule, for the example chart
_lt2 = LTM_DAYS(BAT[("RO", 2, "pf")])

# =============================================================================
# 8. Case study: the month of the year with the most negative hours
# =============================================================================
CM = pd.Period(N["neg"]["top_month"])
cm_mask = pd.Series(LOC_MONTH == CM, index=PX.index)
cp_, base_, _ = capture("RO", "solar", cm_mask)
cpw_, _, _ = capture("RO", "wind_onshore", cm_mask)
_d2 = BAT[("RO", 2, "pf")]
_d2m = _d2[[pd.Period(t, "M") == CM for t in _d2.index]]
N["case"] = {"month": str(CM), "cr_solar": fl(cp_ / base_ * 100, 1), "cp_solar": fl(cp_, 1), "base": fl(base_, 1),
             "cr_wind": fl(cpw_ / base_ * 100, 1), "neg_h": N["neg"]["top_month_h"],
             "bat2_day": fl(_d2m.mean(), 0), "bat2_day_ltm": fl(_lt2.mean(), 0),
             "solar_twh": fl((ro["solar"][cm_mask] * PX["dur"][cm_mask]).sum() / 1e6, 2),
             "e_neg_pct": fl((ro["solar"][cm_mask & (PX["RO"] < 0)] * PX["dur"][cm_mask & (PX["RO"] < 0)]).sum() /
                             (ro["solar"][cm_mask] * PX["dur"][cm_mask]).sum() * 100, 1)}
# the Monday-to-Sunday week of that month with the most negative hours
_mons = sorted({(t - pd.Timedelta(days=t.dayofweek)).normalize() for t in PX.index[cm_mask].tz_localize(None)})
def _negw(m0):
    msk = (PX.index.tz_localize(None) >= m0) & (PX.index.tz_localize(None) < m0 + pd.Timedelta(days=7))
    return PX["dur"][msk & (PX["RO"] < 0).values].sum()
WK0 = max(_mons, key=_negw)
WK1 = WK0 + pd.Timedelta(days=7)
wmask = (PX.index.tz_localize(None) >= WK0) & (PX.index.tz_localize(None) < WK1)
N["case"]["week"] = d(WK0)
N["case"]["week_end"] = d(WK1 - pd.Timedelta(days=1))
N["case"]["week_neg_h"] = fl(PX["dur"][wmask & (PX["RO"] < 0).values].sum(), 2)
N["case"]["week_min"] = fl(PX["RO"][wmask].min(), 2)
N["case"]["week_max"] = fl(PX["RO"][wmask].max(), 2)
_wk2 = _d2[(_d2.index >= WK0) & (_d2.index < WK1)]
N["case"]["week_bat2"] = fl(_wk2.sum(), 0)
N["case"]["week_bat2_mean_day"] = fl(_wk2.mean(), 0)
_ws = ro["solar"][wmask]
N["case"]["week_solar_max"] = fl(_ws.max(), 0)
_wcp, _wb, _ = capture("RO", "solar", pd.Series(wmask, index=PX.index))
N["case"]["week_cr"] = fl(_wcp / _wb * 100, 1)
N["case"]["week_cp"] = fl(_wcp, 1)
N["case"]["week_base"] = fl(_wb, 1)
WEEK_SCHED = []
for k_ in range(7):
    day = WK0 + pd.Timedelta(days=k_)
    msk = (PX.index.tz_localize(None) >= day) & (PX.index.tz_localize(None) < day + pd.Timedelta(days=1))
    p, w = PX["RO"][msk].values, PX["dur"][msk].values
    c, dch = battery_day(p, w, 2)
    WEEK_SCHED.append(pd.DataFrame({"p": p, "net": dch - c}, index=PX.index[msk]))
WEEK_SCHED = pd.concat(WEEK_SCHED)

# =============================================================================
# Charts: one set per language
# =============================================================================
SRC = {"en": {"ec": "energy-charts.info (Fraunhofer ISE); OPCOM day-ahead prices for Romania, via ENTSO-E",
              "ecg": "energy-charts.info (Fraunhofer ISE); OPCOM prices; ENTSO-E solar, wind and load (Transelectrica data for Romania)",
              "reg": "energy-charts.info (Fraunhofer ISE); day-ahead prices of OPCOM (RO), IBEX (BG), HUPX (HU), EPEX SPOT (DE-LU), via ENTSO-E",
              "regg": "energy-charts.info (Fraunhofer ISE); day-ahead prices (OPCOM, IBEX, HUPX); ENTSO-E solar output and load",
              "cap": "energy-charts.info (Fraunhofer ISE), installed capacity from ENTSO-E; ENTSO-E solar output (Transelectrica data)",
              "opc": "OPCOM, PZU aggregated curves (XML), own computation",
              "bat": "energy-charts.info; day-ahead prices via ENTSO-E; ENTSO-E battery output (BG, RO); own optimisation",
              "rogb": "energy-charts.info (Fraunhofer ISE): cross-border physical flows of Romania (ENTSO-E); day-ahead prices of OPCOM (RO) and IBEX (BG)"},
       "ro": {"ec": "energy-charts.info (Fraunhofer ISE); prețurile PZU ale OPCOM pentru România, prin ENTSO-E",
              "ecg": "energy-charts.info (Fraunhofer ISE); prețuri OPCOM; producția solară și eoliană și consumul, ENTSO-E (date Transelectrica)",
              "reg": "energy-charts.info (Fraunhofer ISE); prețurile pieței pentru ziua următoare: OPCOM (RO), IBEX (BG), HUPX (HU), EPEX SPOT (DE-LU), prin ENTSO-E",
              "regg": "energy-charts.info (Fraunhofer ISE); prețuri pentru ziua următoare (OPCOM, IBEX, HUPX); producția solară și consumul, ENTSO-E",
              "cap": "energy-charts.info (Fraunhofer ISE), puterea instalată din ENTSO-E; producția solară, ENTSO-E (date Transelectrica)",
              "opc": "OPCOM, curbele agregate PZU (XML), calcule proprii",
              "bat": "energy-charts.info; prețuri PZU prin ENTSO-E; producția bateriilor, ENTSO-E (BG, RO); optimizare proprie",
              "rogb": "energy-charts.info (Fraunhofer ISE): fluxurile fizice transfrontaliere ale României (ENTSO-E); prețurile pentru ziua următoare OPCOM (RO) și IBEX (BG)"}}


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


def legend_space(fig, pad=0.035):
    """Fraction of the figure height taken by the bottom legend, plus a small gap: the axes (and their x-label) start
    just above the legend, so no empty band is left between the x-label and the legend."""
    fig.canvas.draw()
    h = max([lg.get_window_extent().height for lg in fig.legends] or [0.0]) / fig.bbox.height
    return h + pad


def out(fig, lang, name, bottom=None, also_x=()):
    comma_axes(fig, lang, also_x)
    os.makedirs(os.path.join(HERE, "charts", lang), exist_ok=True)
    save(fig, os.path.join(HERE, "charts", lang, name + ".pdf"), bottom=legend_space(fig))


def yfmt(ax, lang):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


ZN = {"en": {"RO": "Romania", "BG": "Bulgaria", "HU": "Hungary", "DE_LU": "Germany-Lux."},
      "ro": {"RO": "România", "BG": "Bulgaria", "HU": "Ungaria", "DE_LU": "Germania-Lux."}}
YL = {y: str(y) for y in YEARS}
for lang in ["en", "ro"]:
    T = (lambda en, ro_: en) if lang == "en" else (lambda en, ro_: ro_)
    YL[Y] = T(f"{Y}*", f"{Y}*")
    ytd = T(f"* {Y} = Jan-{MON_EN[END.month - 1]}", f"* {Y} = ian.-{MON_RO[END.month - 1].rstrip('.')}.")
    # 1 installed solar capacity and Romanian solar output
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.85))
    cy = list(range(2019, N["cap"]["last_year"] + 1))
    wdt = 0.27
    for i, z in enumerate(("RO", "BG", "HU")):
        axs[0].bar(np.array(cy) + (i - 1) * wdt, [N["cap"]["solar"][z][str(y)] for y in cy], width=wdt, color=PAL[z], label=ZN[lang][z])
    axs[0].set_ylabel(T("installed solar\n(GW)", "putere solară\ninstalată (GW)"), fontsize=9)
    ep.year_ticks(axs[0], cy, rotate=True, fontsize=8.5)
    axs[1].bar(range(len(YEARS)), [twh[str(y)]["solar"] for y in YEARS], color=PAL["RO"], width=0.6)
    ep.year_ticks(axs[1], YEARS, x=range(len(YEARS)), star=Y, rotate=True, fontsize=8.5)
    axs[1].set_ylabel(T("RO solar output\n(TWh)", "producția solară\nRO (TWh)"), fontsize=9)
    axs[1].text(0.02, 0.92, ytd, transform=axs[1].transAxes, fontsize=8.5)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "solar_growth", bottom=0.2)

    # 2 merit-order effect on the OPCOM curves
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.9), sharey=True)
    for ax, k in zip(axs, ("mid", "eve")):
        sup, dem = MERIT[k]
        ax.plot(XGRID, sup, color=PAL["RO"], lw=1.6, label=T("+X MW of supply at 0 EUR/MWh", "+X MW oferiți la 0 EUR/MWh"))
        ax.plot(XGRID, dem, color=PAL["DE_LU"], lw=1.6, ls="--", label=T("+X MW of demand at any price", "+X MW ceruți la orice preț"))
        ax.set_title({"mid": T("12:00-12:15 Romanian time", "12:00-12:15, ora României"),
                      "eve": T("20:00-20:15 Romanian time", "20:00-20:15, ora României")}[k], fontsize=10)
        ax.set_xlabel(T("X, MW added", "X, MW adăugați"))
        ax.set_ylim(-20, 650)
    axs[0].set_ylabel(T("clearing price\n(EUR/MWh)", "prețul de\nînchidere\n(EUR/MWh)"), fontsize=9)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "merit_shift", bottom=0.27)

    # 3 price vs residual load (binned)
    fig, ax = plt.subplots(figsize=(6.4, 1.85))
    for y, col, ls in ((2023, "#9a9a9a", ":"), (Y - 1, PAL["HU"], "--"), (Y, PAL["RO"], "-")):
        x_, y_ = RBIN[y]
        ax.plot(x_, y_, color=col, ls=ls, marker="o", ms=3, lw=1.4, label=YL[y] if y != Y else T(f"{Y} (Jan-{MON_EN[END.month - 1]})", f"{Y} (ian.-{MON_RO[END.month - 1].rstrip('.')}.)"))
    ax.axhline(0, color="#222222", lw=0.6)
    ax.set_xlabel(T("residual load = load - wind - solar, GW (hourly)", "consumul rezidual = consum - eolian - solar, GW (orar)"))
    ax.set_ylabel(T("mean price\n(EUR/MWh)", "prețul mediu\n(EUR/MWh)"), fontsize=9)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "resid_price", bottom=0.22, also_x=[ax])

    # 4 capture rates by year, solar and wind, RO
    fig, ax = plt.subplots(figsize=(6.4, 1.85))
    xs = np.arange(len(YEARS))
    ax.bar(xs - 0.2, [N["capt"]["RO"]["solar"][str(y)]["crp"] for y in YEARS], width=0.38, color=PAL["BG"], label=T("solar", "solar"))
    ax.bar(xs + 0.2, [N["capt"]["RO"]["wind"][str(y)]["crp"] for y in YEARS], width=0.38, color=PAL["HU"], label=T("wind", "eolian"))
    ax.axhline(100, color="#222222", lw=0.8, ls="--", label=T("100% = baseload price", "100% = prețul de bază"))
    for i, y in enumerate(YEARS):
        ax.text(i - 0.2, N["capt"]["RO"]["solar"][str(y)]["crp"] - 4, f"{N['capt']['RO']['solar'][str(y)]['crp']:.0f}", ha="center", va="top",
                fontsize=8, color="white")
    ax.set_xticks(xs)
    ax.set_xticklabels([YL[y] for y in YEARS])
    ax.set_ylim(0, 125)
    ax.set_ylabel(T("capture rate (%)", "rata de captare (%)"), fontsize=9)
    ax.text(1.0, 1.02, ytd, transform=ax.transAxes, fontsize=8, ha="right")
    legend_bottom(fig, ncol=3)
    out(fig, lang, "capture_rates", bottom=0.2)

    # 5 cannibalisation: monthly capture rate vs solar share of load
    fig, ax = plt.subplots(figsize=(6.4, 1.85))
    for z, mk in (("HU", "s"), ("BG", "^"), ("RO", "o")):
        ax.scatter(MON[z]["share"], MON[z]["cr"], s=16 if z == "RO" else 14, color=PAL[z], marker=mk, alpha=0.85 if z == "RO" else 0.65,
                   lw=0, label=ZN[lang][z])
    xx = np.linspace(0, mr["share"].max() * 1.02, 50)
    ax.plot(xx, Rc.params["const"] + Rc.params["share"] * xx, color=PAL["RO"], lw=1.2, label=T("Romania, fit", "România, regresie"))
    ax.axhline(100, color="#222222", lw=0.6, ls="--")
    ax.set_xlabel(T("solar output as % of load in the month", "producția solară, % din consumul lunii"))
    ax.set_ylabel(T("solar capture\nrate (%)", "rata de\ncaptare (%)"), fontsize=9)
    legend_bottom(fig, ncol=4)
    for h_ in fig.legends[-1].legend_handles:          # legend markers readable
        if hasattr(h_, "set_sizes"):
            h_.set_sizes([30])
    out(fig, lang, "cannibal", bottom=0.26, also_x=[ax])

    # 6 regional solar capture rates
    fig, ax = plt.subplots(figsize=(6.4, 1.8))
    for z in ("RO", "BG", "HU"):
        ys = [y for y in YEARS if str(y) in N["capt"][z]["solar"]]
        ax.plot([str(YL[y]) for y in ys], [N["capt"][z]["solar"][str(y)]["crp"] for y in ys], color=PAL[z], ls=ep.ZONE_LS[z], marker="o", ms=4,
                label=ZN[lang][z])
    ax.axhline(100, color="#222222", lw=0.6, ls="--")
    ax.set_ylabel(T("solar capture\nrate (%)", "rata de captare\nsolară (%)"), fontsize=9)
    ax.text(1.0, 1.02, ytd, transform=ax.transAxes, fontsize=8, ha="right")
    legend_bottom(fig, ncol=3)
    out(fig, lang, "capture_region", bottom=0.2)

    # 7 solar energy vs cheapest hours (Lorenz-type curve)
    fig, ax = plt.subplots(figsize=(6.4, 1.85))
    for y, col, ls in ((2019, "#9a9a9a", ":"), (2023, PAL["HU"], "-."), (Y - 1, PAL["BG"], "--"), (Y, PAL["RO"], "-")):
        tsh, esh = LOR[y]
        ax.plot(tsh * 100, esh * 100, color=col, ls=ls, lw=1.5, label=YL[y])
    ax.plot([0, 100], [0, 100], color="#222222", lw=0.6)
    ax.axvline(10, color=PAL["c8"], lw=0.8, ls="--")
    ax.set_xlabel(T("hours of the year ranked from the cheapest, cumulative %", "orele anului ordonate de la cea mai ieftină, % cumulat"))
    ax.set_ylabel(T("solar energy,\ncum. %", "energie solară,\n% cumulat"), fontsize=9)
    ax.set_yticks([0, 50, 100])
    legend_bottom(fig, ncol=4)
    out(fig, lang, "cheap_hours", bottom=0.23, also_x=[ax])

    # 8 negative hour-equivalents by year and zone
    fig, ax = plt.subplots(figsize=(6.4, 1.85))
    yy = [y for y in YEARS if y >= 2022]
    for i, z in enumerate(ZONES):
        ax.bar(np.arange(len(yy)) + (i - 1.5) * 0.2, [N["neg"]["hours"][z][str(y)] for y in yy], width=0.2, color=PAL[z], label=ZN[lang][z])
    ax.set_xticks(range(len(yy)))
    ax.set_xticklabels([YL[y] for y in yy])
    ax.set_ylabel(T("negative hours\n(hour-equiv.)", "ore negative\n(ore echiv.)"), fontsize=9)
    ax.text(0.01, 0.9, ytd, transform=ax.transAxes, fontsize=8)
    legend_bottom(fig, ncol=4)
    out(fig, lang, "neg_hours", bottom=0.2)

    # 9 intraday shape, 15-min, last 12 months, by season
    fig, ax = plt.subplots(figsize=(6.4, 1.85))
    SL = {"winter": T("winter", "iarna"), "spring": T("spring", "primăvara"),
          "summer": T("summer", "vara"), "autumn": T("autumn", "toamna")}      # months: in the chart caption
    SC = {"winter": PAL["c7"], "spring": PAL["HU"], "summer": PAL["DE_LU"], "autumn": PAL["BG"]}
    for s_, pr in PROF.items():
        ax.step(np.arange(96) / 4, pr.values, where="post", color=SC[s_], lw=1.3, label=SL[s_])
    ax.axhline(0, color="#222222", lw=0.6)
    ax.set_xticks(range(0, 25, 3))
    ax.set_xlabel(T("time of day (CET), 96 quarter-hours", "ora din zi (CET), 96 de sferturi de oră"))
    ax.set_ylabel(T("mean price\n(EUR/MWh)", "prețul mediu\n(EUR/MWh)"), fontsize=9)
    legend_bottom(fig, ncol=4)
    out(fig, lang, "shape15")

    # 10 monthly mean of the daily top-2 minus bottom-2 spread
    fig, ax = plt.subplots(figsize=(6.4, 1.8))
    for z in ZONES:
        s = SPRM[z]
        ax.plot(s.index.to_timestamp(), s.values, color=PAL[z], ls=ep.ZONE_LS[z], lw=1.2, label=ZN[lang][z])
    ax.set_ylabel(T("daily spread\n(EUR/MWh)", "diferența zilnică\n(EUR/MWh)"), fontsize=9)
    ax.set_ylim(0, 400)
    ax.set_yticks([0, 100, 200, 300, 400])
    yfmt(ax, lang)
    ax.set_xlim(pd.Timestamp("2019-01-01"), pd.Timestamp(END))
    legend_bottom(fig, ncol=4)
    out(fig, lang, "spreads", bottom=0.2)

    # 11 battery revenue by year and duration (perfect foresight)
    fig, ax = plt.subplots(figsize=(6.4, 1.8))
    yb = list(range(YEARS[0], Y)) + ["LTM"]
    for i, (E, col) in enumerate(zip(DURS, (PAL["HU"], PAL["RO"], PAL["c7"]))):
        vals = [N["bat"]["pf"][str(E)][str(y)] for y in yb[:-1]] + [N["bat"]["ltm"][str(E)]["pf"]]
        ax.bar(np.arange(len(yb)) + (i - 1) * 0.27, vals, width=0.27, color=col, label=T(f"{E} h of storage", f"{E} h de stocare"))
    ax.set_xticks(range(len(yb)))
    ax.set_xticklabels([str(y) for y in yb[:-1]] + [T("last\n12 months", "ultimele\n12 luni")], fontsize=8.5)
    ax.set_ylabel(T("thousand EUR\nper MW-year", "mii EUR\npe MW și an"), fontsize=9)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "bat_years", bottom=0.2)

    # 12 one week of the case study: 15-min price and 2h battery schedule; solar and wind
    fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.5), sharex=True, gridspec_kw={"height_ratios": [1.3, 1]})
    ws = WEEK_SCHED
    tt = ws.index.tz_localize(None)
    axs[0].step(tt, ws["p"], where="post", color=PAL["RO"], lw=0.9, label=T("RO price, 15-min", "prețul RO, 15 minute"))
    ch = ws["net"] < -1e-6
    dc = ws["net"] > 1e-6
    axs[0].fill_between(tt, ws["p"].min(), ws["p"].max(), where=ch.values, step="post", color=PAL["c7"], alpha=0.25, lw=0,
                        label=T("2h battery charging", "bateria de 2 h se încarcă"))
    axs[0].fill_between(tt, ws["p"].min(), ws["p"].max(), where=dc.values, step="post", color=PAL["DE_LU"], alpha=0.3, lw=0,
                        label=T("2h battery discharging", "bateria de 2 h se descarcă"))
    axs[0].axhline(0, color="#222222", lw=0.6)
    axs[0].set_ylabel("EUR/MWh", fontsize=9.5)
    gw = ro.loc[ws.index, ["solar", "wind_onshore"]] / 1000
    axs[1].plot(tt, gw["solar"], color=PAL["BG"], lw=1.1, label=T("solar, GW", "solar, GW"))
    axs[1].plot(tt, gw["wind_onshore"], color=PAL["HU"], lw=1.1, label=T("wind, GW", "eolian, GW"))
    axs[1].set_ylabel("GW", fontsize=9.5)
    axs[1].xaxis.set_major_locator(mdates.DayLocator())
    dn = {"en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "ro": ["lun.", "mar.", "mie.", "joi", "vin.", "sîm.", "dum."]}[lang]
    axs[1].xaxis.set_major_formatter(FuncFormatter(lambda v, p: dn[mdates.num2date(v).weekday()] + " " + str(mdates.num2date(v).day)))
    legend_bottom(fig, ncol=3)
    out(fig, lang, "case_week", bottom=0.2)

    # 13 regional battery revenue, monthly 2h, RO / BG / HU + battery fleets
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.9))
    for z in ("RO", "BG", "HU"):
        s = BMM[z]
        axs[0].plot(s.index.to_timestamp(), s.values, color=PAL[z], ls=ep.ZONE_LS[z], lw=1.3, label=ZN[lang][z])
    axs[0].set_ylabel(T("2h battery, EUR\nper MW per day", "bateria de 2 h,\nEUR/MW pe zi"), fontsize=8.5)
    for ax in axs:
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.set_xlim(pd.Timestamp("2024-01-01"), pd.Timestamp(END))
    for z in ("RO", "BG"):
        s = FLEET[z].dropna()
        axs[1].plot(s.index.to_timestamp(), s.values, color=PAL[z], ls=ep.ZONE_LS[z], lw=1.3)
    axs[1].set_ylabel(T("battery output\n(MW, monthly)", "descărcarea\nbateriilor (MW)"), fontsize=8.5)

    legend_bottom(fig, ncol=3)
    out(fig, lang, "bat_region", bottom=0.22)

    # 14 battery strategies, last 12 months: perfect foresight, hourly, two forecast rules
    fig, ax = plt.subplots(figsize=(6.4, 1.85))
    lab = [T("perfect foresight,\n15-min", "informație perfectă,\n15 minute"), T("perfect foresight,\nhourly averages", "informație perfectă,\nmedii orare"),
           T("rule: mean of\nlast 7 days", "regula: media\nultimelor 7 zile"), T("rule: yesterday's\nprices", "regula: prețurile\nde ieri")]
    for i, (E, col) in enumerate(zip(DURS, (PAL["HU"], PAL["RO"], PAL["c7"]))):
        b = N["bat"]["ltm"][str(E)]
        vals = [b["pf"], b["hourly"], b["wk"] * b["n_days"] / b["n_common"], b["yday"] * b["n_days"] / b["n_common"]]
        ax.bar(np.arange(4) + (i - 1) * 0.27, vals, width=0.27, color=col, label=T(f"{E} h", f"{E} h"))
    ax.set_xticks(range(4))
    ax.set_xticklabels(lab, fontsize=8.5)
    ax.set_ylabel(T("thousand EUR\nper MW", "mii EUR\npe MW"), fontsize=9)
    legend_bottom(fig, ncol=3)
    out(fig, lang, "bat_rules", bottom=0.2)

ytd_en, ytd_ro = N["data"]["ytd_label_en"], N["data"]["ytd_label_ro"]
ltm_en = f"last 12 months {N['cutoff']['ltm_start']} to {d(END)}"
ltm_ro = f"ultimele 12 luni, {N['cutoff']['ltm_start']} - {d(END)}"
chart("solar_growth", "cap", f"installed capacity at year end 2019-{N['cap']['last_year']}; output 2019 to {d(END)}",
      f"puterea instalată la sfîrșitul anilor 2019-{N['cap']['last_year']}; producția 2019 - {d(END)}")
chart("merit_shift", "opc", f"delivery day {N['merit']['day']}; cross-border flows, blocks and hourly orders held at their accepted values",
      f"ziua de livrare {N['merit']['day']}; fluxurile transfrontaliere, blocurile și ordinele orare rămîn la valorile acceptate")
chart("resid_price", "ecg", f"hourly, 2023-01-01 to {d(END)}; bins of 0.5 GW with at least 20 hours",
      f"orar, 2023-01-01 - {d(END)}; intervale de 0,5 GW cu cel puțin 20 de ore")
chart("capture_rates", "ecg", f"2019 to {d(END)}; hourly to Sep 2025, 15-min from Oct 2025",
      f"2019 - {d(END)}; date orare pînă în sep. 2025, la 15 minute din oct. 2025")
chart("cannibal", "regg", f"monthly, {N['cannib']['start'][:7]} to {N['cannib']['end'][:7]}; Hungary from Oct 2019",
      f"lunar, {N['cannib']['start'][:7]} - {N['cannib']['end'][:7]}; Ungaria din oct. 2019")
chart("capture_region", "regg", f"2019 (Hungary 2020) to {d(END)}; Bulgaria: hourly solar output",
      f"2019 (Ungaria 2020) - {d(END)}; Bulgaria: producție solară orară")
chart("cheap_hours", "ecg", f"each calendar year; {Y} to {d(END)}", f"fiecare an calendaristic; {Y} pînă la {d(END)}")
chart("neg_hours", "reg", f"2022 to {d(END)}; a 15-min interval counts 0.25 h", f"2022 - {d(END)}; un interval de 15 minute contează 0,25 h")
chart("shape15", "ec", f"{ltm_en}, 15-min prices, CET; winter = Dec-Feb, spring = Mar-May, summer = Jun-Aug, autumn = Sep-Nov",
      f"{ltm_ro}, prețuri pe 15 minute, ora CET; iarna = dec.-feb., primăvara = mar.-mai, vara = iun.-aug., toamna = sep.-nov.")
chart("spreads", "reg", f"daily, hourly prices (15-min averaged), monthly means, 2019 to {d(END)}",
      f"zilnic, prețuri orare (media sferturilor), medii lunare, 2019 - {d(END)}")
chart("bat_years", "bat", f"1 MW, round trip 85\\%, max one cycle a day; 2019-{Y - 1} and {ltm_en}",
      f"1 MW, randament 85\\%, cel mult un ciclu pe zi; 2019-{Y - 1} și {ltm_ro}")
chart("case_week", "ecg", f"week {N['case']['week']} to {N['case']['week_end']}, 15-min, CET", f"săptămîna {N['case']['week']} - {N['case']['week_end']}, 15 minute, ora CET")
chart("bat_region", "bat", f"2h battery, perfect foresight, 2024-01 to {d(END)[:7]}; battery output as reported to ENTSO-E",
      f"baterie de 2 h, informație perfectă, 2024-01 - {d(END)[:7]}; producția bateriilor raportată la ENTSO-E")
chart("bat_rules", "bat", f"{ltm_en}; 1 MW, round trip 85\\%; forecast rules on {N['bat']['ltm']['2']['n_common']} common days, scaled to the full period",
      f"{ltm_ro}; 1 MW, randament 85\\%; regulile de prognoză pe {N['bat']['ltm']['2']['n_common']} de zile comune, scalate la întreaga perioadă")

# =============================================================================
# 9. Case study: summer of the last year, Romania and Bulgaria (cross-border flows and prices by hour of the day)
# =============================================================================
# energy-charts physical flows per border, MW; sign: + = net import into Romania (data/SOURCES.md)
CB = pd.read_csv(os.path.join(DATA, "crossborder_ro_mw_hourly_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
CB.index = pd.to_datetime(CB.index, utc=True).tz_convert("Europe/Bucharest")
PH = pd.read_csv(os.path.join(DATA, "power_da_prices_hourly_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
PH.index = pd.to_datetime(PH.index, utc=True).tz_convert("Europe/Bucharest")
SUMMER = (CB.index.year == Y) & CB.index.month.isin([6, 7, 8])
RG = CB.loc[SUMMER, ["bulgaria", "hungary", "serbia", "sum"]].join(PH[["RO", "BG"]], how="left")
RGH = RG.groupby(RG.index.hour).mean()
_days = RG.index.normalize().unique()
_mid = RG[RG.index.hour.isin([12, 13, 14])].groupby(RG[RG.index.hour.isin([12, 13, 14])].index.normalize())["bulgaria"].mean()
_eve = RG[RG.index.hour.isin([19, 20, 21, 22])].groupby(RG[RG.index.hour.isin([19, 20, 21, 22])].index.normalize())["bulgaria"].mean()
_hx = int(RGH["sum"].idxmin())
_hm = int(RGH["sum"].idxmax())
_hb = int(RGH["bulgaria"].idxmax())
N["rogb"] = {"year": Y, "start": d(RG.index.min()), "end": d(RG.index.max()), "n_days": int(len(_days)),
             "exp_h": _hx, "exp_mw": fl(-RGH["sum"].min(), 0), "imp_h": _hm, "imp_mw": fl(RGH["sum"].max(), 0),
             "bg_eve_h": _hb, "bg_eve_mw": fl(RGH["bulgaria"].max(), 0),
             "days_bg_eve_imp": int((_eve > 0).sum()), "days_bg_mid_exp": int((_mid < 0).sum()), "n_days_mid": int((_mid < 0).sum()),
             "hu_mid_mw": fl(-RGH.loc[12, "hungary"], 0), "rs_mid_mw": fl(-RGH.loc[12, "serbia"], 0),
             "bg_mid_mw": fl(RGH.loc[12, "bulgaria"], 0),
             "p_ro_eve": fl(RGH.loc[_hb, "RO"], 1), "p_bg_eve": fl(RGH.loc[_hb, "BG"], 1),
             "p_gap_eve": fl(RGH.loc[_hb, "RO"] - RGH.loc[_hb, "BG"], 1),
             "p_ro_mid": fl(RGH.loc[13, "RO"], 1), "p_bg_mid": fl(RGH.loc[13, "BG"], 1),
             "n_h_gap10": int(((RG["RO"] - RG["BG"]) > 10).sum()), "n_h": int(RG["RO"].notna().sum())}
N["rogb"]["share_h_gap10"] = fl(N["rogb"]["n_h_gap10"] / N["rogb"]["n_h"] * 100, 1)
ROGB_H = RGH
for lang in ["en", "ro"]:
    T = (lambda en, ro_: en) if lang == "en" else (lambda en, ro_: ro_)
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.95))
    hh = ROGB_H.index.values
    axs[0].axhline(0, color="#222222", lw=0.6)
    axs[0].plot(hh, ROGB_H["sum"] / 1000, color=PAL["RO"], lw=1.8, label=T("Romania (all borders; RO price)", "România (toate granițele; preț RO)"))
    axs[0].plot(hh, ROGB_H["bulgaria"] / 1000, color=PAL["BG"], lw=1.6, ls="--", label=T("Bulgaria (RO-BG border; BG price)", "Bulgaria (granița RO-BG; preț BG)"))
    axs[0].set_ylabel(T("net import, GW\n(< 0: export)", "import net, GW\n(< 0: export)"), fontsize=8.5)
    axs[0].set_title(T("cross-border flows", "fluxuri transfrontaliere"), fontsize=9.5)
    axs[1].plot(hh, ROGB_H["RO"], color=PAL["RO"], lw=1.8)
    axs[1].plot(hh, ROGB_H["BG"], color=PAL["BG"], lw=1.6, ls="--")
    axs[1].set_title(T("day-ahead prices", "prețuri PZU"), fontsize=9.5)
    axs[1].set_ylabel(T("day-ahead price\n(EUR/MWh)", "preț PZU\n(EUR/MWh)"), fontsize=8.5)
    for ax in axs:
        ax.set_xticks([0, 6, 12, 18, 23])
        ax.set_xlabel(T("hour of the day (Romanian time)", "ora din zi (ora României)"), fontsize=8.5)
    legend_bottom(fig, ncol=2)
    fig.subplots_adjust(wspace=0.45)
    out(fig, lang, "rogb_summer", bottom=0.27)
chart("rogb_summer", "rogb", f"hourly means, {N['rogb']['start']} to {N['rogb']['end']}; Moldova and Ukraine borders only partly reported",
      f"medii orare, {N['rogb']['start']} - {N['rogb']['end']}; granițele cu Moldova și Ucraina sînt raportate doar parțial")

with open(os.path.join(HERE, "L6_numbers.json"), "w") as fh:
    json.dump(N, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("wrote L6_numbers.json and", len(N["charts"]), "charts x 2 languages")
