"""
analysis_L5.py -- Lecture 5 "Energy derivatives and hedging" (EMQA)
===================================================================
Reads the real series in repo/data/clean (data/SOURCES.md, including the Lecture 5 section written by data/download_L5.py)
and writes
    lectures/L5/L5_numbers.json        every number shown on the slides (the deck builder reads ONLY this file)
    lectures/L5/charts/en/*.pdf        figures with English labels
    lectures/L5/charts/ro/*.pdf        the same figures with Romanian labels
Run:  python3 lectures/L5/analysis_L5.py

Data and conventions
  * Romanian forward prices = OPCOM PCCB-LE-flex auction results (physical bilateral contracts), one closing price per
    traded session, lei/MWh converted to EUR with the ECB EUR/RON fixing of the auction date. Only baseload ('banda LD')
    products with standard delivery periods (month, quarter, half-year, calendar year) enter the curve and premium analysis.
  * Spot = OPCOM day-ahead (PZU) price via energy-charts; delivery-period averages = mean of the daily base prices
    (CET days), computed only when every day of the period is present.
  * Cut-off = last complete month; forward auctions after the cut-off are not used.
  * Gas = TTF monthly (World Bank); carbon = EEX primary-auction EUA price (monthly mean), and the SparkChange ETC proxy
    for months after the last EEX file (2026); coal = World Bank South African export coal (USD/t, 6000 kcal/kg).
  * TTF futures = individual NYMEX contract months (no continuous series, hence no roll days; README rule 9).
  * No simulated series in this lecture. Seeds fixed for the block bootstrap.
"""

import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import norm

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
N = {"charts": {}}
SEED = 20261106
MON_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MON_RO = ["ian.", "feb.", "mar.", "apr.", "mai", "iun.", "iul.", "aug.", "sep.", "oct.", "nov.", "dec."]

# conversion factors and technical assumptions (definitions, stated on the slides)
ETA_GAS, ETA_COAL = 0.50, 0.38            # efficiency of a combined-cycle gas plant and of a hard-coal plant (assumed)
EF_GAS, EF_COAL = 0.202, 0.341            # t CO2 per MWh thermal (IPCC 2006: 56.1 and 94.6 t CO2/TJ)
COAL_MWH_T = 6.978                        # MWh thermal per tonne of 6000 kcal/kg coal (6000*4.1868/3600)


def d(ts):
    return pd.Timestamp(ts).strftime("%Y-%m-%d")


def fl(x, k=4):
    if x is None:
        return None
    x = float(x)
    return None if np.isnan(x) else round(x, k)


# =============================================================================
# 0. Load data, cut-off
# =============================================================================
PD = ep.prices_daily()
_raw_last = PD["RO"].dropna().index.max()
END = pd.Timestamp(((_raw_last + pd.Timedelta(days=1)).to_period("M").to_timestamp() - pd.Timedelta(days=1)).date())
N["cutoff"] = {"end": d(END), "end_ym": END.strftime("%Y-%m"), "download": "2026-11-06"}

FW = pd.read_csv(os.path.join(DATA, "opcom_forward_trades.csv"),
                 parse_dates=["auction_date", "delivery_start", "delivery_end"])
FW = FW[FW["auction_date"] <= END].copy()
RATES = pd.read_csv(os.path.join(DATA, "ecb_ron_estr_daily.csv"), parse_dates=["date"]).set_index("date")
TTFM = ep.ttf_monthly()
TTFC = pd.read_csv(os.path.join(DATA, "ttf_futures_contracts_daily.csv"), parse_dates=["date"]).set_index("date")
TTFC = TTFC.loc[:END]
EUA = pd.read_csv(os.path.join(DATA, "eua_daily.csv"), parse_dates=["date"]).set_index("date")
COAL = pd.read_csv(os.path.join(DATA, "coal_monthly.csv"))
COAL.index = pd.PeriodIndex(COAL["month"], freq="M").to_timestamp()
FUEL = ep.fuels_daily()


def kind_of(s, e):
    """Standard delivery period of a product: M (month), Q (quarter), H (half-year), Y (calendar year), else 'other'."""
    if s.day != 1 or (e + pd.Timedelta(days=1)).day != 1:
        return "other"
    n = (e.year - s.year) * 12 + e.month - s.month + 1
    if n == 1:
        return "M"
    if n == 3 and s.month in (1, 4, 7, 10):
        return "Q"
    if n == 6 and s.month in (1, 7):
        return "H"
    if n == 12 and s.month == 1:
        return "Y"
    return "other"


FW["kind"] = [kind_of(s, e) for s, e in zip(FW["delivery_start"], FW["delivery_end"])]
FW["lead_m"] = ((FW["delivery_start"].dt.year - FW["auction_date"].dt.year) * 12 +
                FW["delivery_start"].dt.month - FW["auction_date"].dt.month)
BASE = FW[(FW["profile"] == "banda LD") & (FW["kind"] != "other")].copy()


def vwap(df):
    return float(np.average(df["price_eur_mwh"], weights=df["mwh"])) if len(df) else np.nan


def realised(s, e, col="RO"):
    """Mean day-ahead base price over [s, e] (CET days); NaN unless every day is present."""
    x = PD.loc[s:e, col]
    full = len(x) == (e - s).days + 1 and x.notna().all()
    return float(x.mean()) if full else np.nan


N["data"] = {"fw_first": d(FW["auction_date"].min()), "fw_last": d(FW["auction_date"].max()), "fw_n": int(len(FW)),
             "fw_twh": fl(FW["mwh"].sum() / 1e6, 2), "base_n": int(len(BASE)),
             "base_share": fl(100 * FW.loc[FW["profile"] == "banda LD", "mwh"].sum() / FW["mwh"].sum(), 1),
             "spot_start": d(PD["RO"].first_valid_index()), "spot_end": d(END),
             "eurron_end": fl(RATES["eurron_ecb"].loc[:END].dropna().iloc[-1], 4)}

# =============================================================================
# 1. The Romanian forward market: volumes, products, who sells and who buys
# =============================================================================
FW["year"] = FW["auction_date"].dt.year
vol = FW.pivot_table(index="year", columns="kind", values="mwh", aggfunc="sum").fillna(0) / 1e6
N["volume"] = {str(y): fl(vol.loc[y].sum(), 2) for y in vol.index}
N["volume"]["max_year"] = int(vol.sum(1).idxmax())
N["volume"]["min_year"] = int(vol.sum(1).idxmin())
N["volume"]["n_sessions"] = {str(y): int((FW["year"] == y).sum()) for y in vol.index}
N["volume"]["y_share_base"] = fl(100 * BASE.loc[BASE["kind"] == "Y", "mwh"].sum() / BASE["mwh"].sum(), 1)
sel = FW.groupby("seller")["mwh"].sum().sort_values(ascending=False)
buy = FW.groupby("buyer")["mwh"].sum().sort_values(ascending=False)
PROD3 = ["SOCIETATEA COMPLEXUL ENERGETIC OLTENIA S.A.", "SOCIETATEA NATIONALA NUCLEARELECTRICA S.A.", "S.C. HIDROELECTRICA S.A."]
N["who"] = {"sell_top3_share": fl(100 * sel.loc[PROD3].sum() / FW["mwh"].sum(), 1),
            "sell_oltenia": fl(100 * sel.loc[PROD3[0]] / FW["mwh"].sum(), 1),
            "sell_snn": fl(100 * sel.loc[PROD3[1]] / FW["mwh"].sum(), 1),
            "sell_hidro": fl(100 * sel.loc[PROD3[2]] / FW["mwh"].sum(), 1),
            "buy_top1_share": fl(100 * buy.iloc[0] / FW["mwh"].sum(), 1), "n_buyers": int(FW["buyer"].nunique()),
            "n_sellers": int(FW["seller"].nunique())}

# =============================================================================
# 2. Forward curve today, calendar products by trade date, forward premium ex post
# =============================================================================
CURVE_FROM = (END - pd.DateOffset(months=2) + pd.Timedelta(days=1)).normalize()
cur = BASE[(BASE["auction_date"] >= CURVE_FROM) & (BASE["delivery_start"] > END)]
curve = (cur.groupby(["delivery_start", "delivery_end", "kind"])
         .apply(lambda g: pd.Series({"F": vwap(g), "n": len(g), "twh": g["mwh"].sum() / 1e6})).reset_index())
N["curve"] = {"from": d(CURVE_FROM), "to": d(END), "n_products": int(len(curve)), "n_sessions": int(len(cur)),
              "items": [{"start": d(r.delivery_start), "end": d(r.delivery_end), "kind": r.kind, "F": fl(r.F, 2), "n": int(r.n)}
                        for r in curve.itertuples()]}
cal = curve[curve["kind"] == "Y"].sort_values("delivery_start")
N["curve"]["cal_next"] = {"year": int(cal["delivery_start"].iloc[0].year), "F": fl(cal["F"].iloc[0], 2), "n": int(cal["n"].iloc[0])}
mth = curve[curve["kind"] == "M"].sort_values("delivery_start")
N["curve"]["m_front"] = ({"ym": mth["delivery_start"].iloc[0].strftime("%Y-%m"), "F": fl(mth["F"].iloc[0], 2)}
                         if len(mth) else None)
q1 = curve[(curve["kind"] == "Q")].sort_values("delivery_start")
N["curve"]["q_front"] = ({"start": d(q1["delivery_start"].iloc[0]), "F": fl(q1["F"].iloc[0], 2)} if len(q1) else None)
last3 = PD.loc[END - pd.DateOffset(months=3) + pd.Timedelta(days=1):END, "RO"]
N["curve"]["spot_last3"] = fl(last3.mean(), 2)
N["curve"]["spot_lastm"] = fl(PD.loc[END.replace(day=1):END, "RO"].mean(), 2)

# calendar-year products by trade date
CY = BASE[BASE["kind"] == "Y"].copy()
CY["dy"] = CY["delivery_start"].dt.year
calt = {}
for y, g in CY.groupby("dy"):
    if len(g) < 5:
        continue
    calt[str(y)] = {"n": int(len(g)), "vwap": fl(vwap(g), 2), "min": fl(g["price_eur_mwh"].min(), 2),
                    "max": fl(g["price_eur_mwh"].max(), 2), "first": d(g["auction_date"].min()), "last": d(g["auction_date"].max()),
                    "realised": fl(realised(pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y}-12-31")), 2),
                    "argmax": d(g.loc[g["price_eur_mwh"].idxmax(), "auction_date"])}
N["cal"] = calt


def premium_table(base):
    """Ex-post forward premium of every baseload product fully delivered by the cut-off: F - realised mean spot."""
    b = base[base["delivery_end"] <= END].copy()
    b["S"] = [realised(s, e) for s, e in zip(b["delivery_start"], b["delivery_end"])]
    b = b.dropna(subset=["S"])
    b["prem"] = b["price_eur_mwh"] - b["S"]
    b["lr"] = np.log(b["S"] / b["price_eur_mwh"])
    b["T"] = ((b["delivery_start"] + (b["delivery_end"] - b["delivery_start"]) / 2) - b["auction_date"]).dt.days / 365.25
    return b


def nw_t(x, lags=3):
    x = np.asarray(x, float)
    r = sm.OLS(x, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return float(r.params[0]), float(r.bse[0]), float(r.tvalues[0]), float(r.pvalues[0])


PT = premium_table(BASE)
# monthly products traded in the month before delivery: one F per delivery month
M1 = PT[(PT["kind"] == "M") & (PT["lead_m"] == 1)]
MP = M1.groupby("delivery_start").apply(lambda g: pd.Series({"F": vwap(g), "S": g["S"].iloc[0], "n": len(g)}))
MP["prem"] = MP["F"] - MP["S"]
mu, se, tt, pp = nw_t(MP["prem"])
# all products, one row per (delivery period, kind): VWAP
PP = PT.groupby(["delivery_start", "delivery_end", "kind"]).apply(
    lambda g: pd.Series({"F": vwap(g), "S": g["S"].iloc[0], "mwh": g["mwh"].sum(), "n": len(g)})).reset_index()
PP["prem"] = PP["F"] - PP["S"]
PP["dyear"] = PP["delivery_start"].dt.year
N["prem"] = {"m1": {"n": int(len(MP)), "first": MP.index.min().strftime("%Y-%m"), "last": MP.index.max().strftime("%Y-%m"),
                    "mean": fl(mu, 2), "se": fl(se, 2), "t": fl(tt, 2), "p": fl(pp, 3), "median": fl(MP["prem"].median(), 2),
                    "pos_share": fl(100 * (MP["prem"] > 0).mean(), 1)},
             "all": {"n": int(len(PP)), "n_sessions": int(len(PT)), "w_mean": fl(np.average(PP["prem"], weights=PP["mwh"]), 2),
                     "pos_share": fl(100 * (PP["prem"] > 0).mean(), 1)}}
for lab, msk in [("pre", PP["dyear"] <= 2021), ("crisis", PP["dyear"] == 2022), ("post", PP["dyear"] >= 2023)]:
    g = PP[msk]
    N["prem"][lab] = {"n": int(len(g)), "mean": fl(g["prem"].mean(), 2), "w_mean": fl(np.average(g["prem"], weights=g["mwh"]), 2),
                      "pos_share": fl(100 * (g["prem"] > 0).mean(), 1)}
gm = MP[MP.index >= "2023-01-01"]
if len(gm) >= 6:
    a, b_, c_, p_ = nw_t(gm["prem"])
    N["prem"]["m1_post"] = {"n": int(len(gm)), "mean": fl(a, 2), "t": fl(c_, 2), "p": fl(p_, 3)}
# terminal volatility of ln(S/F) per sqrt(year), monthly products, one-month lead
z = M1["lr"] / np.sqrt(M1["T"])
N["termvol"] = {"n": int(len(M1)), "all": fl(z.std(ddof=1), 4), "mean_T_days": fl(365.25 * M1["T"].mean(), 1)}
zp = z[M1["delivery_start"] >= "2023-01-01"]
N["termvol"]["post"] = fl(zp.std(ddof=1), 4)
N["termvol"]["n_post"] = int(len(zp))

# =============================================================================
# 3. The 2021-2022 crisis and the summer 2024 spike: forward-hedged vs spot
# =============================================================================
c22 = CY[CY["dy"] == 2022]
S22 = realised(pd.Timestamp("2022-01-01"), pd.Timestamp("2022-12-31"))
h = {}
for lab, a0, a1 in [("h20", "2020-01-01", "2020-12-31"), ("h21a", "2021-01-01", "2021-06-30"), ("h21b", "2021-07-01", "2021-12-31")]:
    g = c22[(c22["auction_date"] >= a0) & (c22["auction_date"] <= a1)]
    h[lab] = {"n": int(len(g)), "vwap": fl(vwap(g), 2), "twh": fl(g["mwh"].sum() / 1e6, 2)}
F22 = vwap(c22)
N["crisis"] = {"S22": fl(S22, 2), "F22": fl(F22, 2), "n": int(len(c22)), "twh": fl(c22["mwh"].sum() / 1e6, 2),
               "gap": fl(S22 - F22, 2), "ratio": fl(S22 / F22, 2), "eur_per_mw": fl((S22 - F22) * 8760, 0),
               "eur_per_mw_m": fl((S22 - F22) * 8760 / 1e6, 3), "parts": h,
               "S22_max_m": fl(PD.loc["2022", "RO"].resample("MS").mean().max(), 2),
               "S22_max_m_ym": PD.loc["2022", "RO"].resample("MS").mean().idxmax().strftime("%Y-%m"),
               "c23_max": calt["2023"]["max"], "c23_argmax": calt["2023"]["argmax"],
               "S21": fl(realised(pd.Timestamp("2021-01-01"), pd.Timestamp("2021-12-31")), 2)}
# summer 2024: products for July 2024 / Q3 2024
j24 = PP[(PP["delivery_start"] == "2024-07-01")]
N["s24"] = {"S_jul": fl(realised(pd.Timestamp("2024-07-01"), pd.Timestamp("2024-07-31")), 2),
            "S_q3": fl(realised(pd.Timestamp("2024-07-01"), pd.Timestamp("2024-09-30")), 2),
            "max_day": fl(PD.loc["2024-06":"2024-08", "RO"].max(), 2),
            "max_day_date": d(PD.loc["2024-06":"2024-08", "RO"].idxmax()),
            "F_q3": fl(j24.loc[j24["kind"] == "Q", "F"].iloc[0], 2) if (j24["kind"] == "Q").any() else None,
            "F_jul": fl(j24.loc[j24["kind"] == "M", "F"].iloc[0], 2) if (j24["kind"] == "M").any() else None}
hp = ep.prices_native()
x24 = hp.loc["2024-06-01":"2024-08-31", "RO"]
N["s24"]["max_h"] = fl(x24.max(), 2)
N["s24"]["max_h_ts"] = x24.idxmax().strftime("%Y-%m-%d %H:%M")

# =============================================================================
# 4. Spreads: spark, clean spark, dark, clean dark (monthly); hourly spark optionality
# =============================================================================
m_idx = pd.date_range("2015-01-01", END.replace(day=1), freq="MS")
PM = PD[["RO", "HU", "DE_LU"]].resample("MS").mean().reindex(m_idx)
NDM = PD[["RO", "HU", "DE_LU"]].resample("MS").count().reindex(m_idx)
full_m = NDM.eq(pd.Series(m_idx.days_in_month, index=m_idx), axis=0)
PM = PM.where(full_m)
eua_a = EUA["eua_eex_auction_eur_t"].dropna().resample("MS").mean()
eua_e = EUA["eua_etc_co2l_eur_per_unit"].dropna().resample("MS").mean()
EUAM = eua_a.reindex(m_idx).fillna(eua_e.reindex(m_idx).where(m_idx > eua_a.index.max()))
EUA_SRC_SWITCH = (eua_a.index.max() + pd.DateOffset(months=1)).strftime("%Y-%m")
GAS = TTFM["ttf_eur_mwh"].reindex(m_idx)
fxm = FUEL["eurusd_ecb"].resample("MS").mean().reindex(m_idx)
COALE = (COAL["coal_southafrica_usd_t"].reindex(m_idx) / fxm) / COAL_MWH_T


def spreads(p, gas, coal, eua):
    """Spark, clean spark, dark and clean dark spreads in EUR per MWh of electricity."""
    ss = p - gas / ETA_GAS
    css = ss - EF_GAS / ETA_GAS * eua
    ds = p - coal / ETA_COAL
    cds = ds - EF_COAL / ETA_COAL * eua
    return ss, css, ds, cds


SPR = {}
for z_ in ["RO", "DE_LU"]:
    ss, css, ds, cds = spreads(PM[z_], GAS, COALE, EUAM)
    SPR[z_] = pd.DataFrame({"ss": ss, "css": css, "ds": ds, "cds": cds})
yrs = SPR["RO"].groupby(SPR["RO"].index.year).mean()
yde = SPR["DE_LU"].groupby(SPR["DE_LU"].index.year).mean()
N["spread"] = {"eta_gas": ETA_GAS, "eta_coal": ETA_COAL, "ef_gas": EF_GAS, "ef_coal": EF_COAL,
               "cf_gas": fl(EF_GAS / ETA_GAS, 3), "cf_coal": fl(EF_COAL / ETA_COAL, 3), "coal_mwh_t": COAL_MWH_T,
               "eua_switch": EUA_SRC_SWITCH, "first": m_idx[0].strftime("%Y-%m"), "last": m_idx[-1].strftime("%Y-%m"),
               "css_ro": {str(y): fl(yrs.loc[y, "css"], 2) for y in yrs.index},
               "cds_ro": {str(y): fl(yrs.loc[y, "cds"], 2) for y in yrs.index},
               "css_de": {str(y): fl(yde.loc[y, "css"], 2) for y in yde.index},
               "cds_de": {str(y): fl(yde.loc[y, "cds"], 2) for y in yde.index},
               "css_ro_neg_m": int((SPR["RO"]["css"] < 0).sum()), "n_m": int(SPR["RO"]["css"].notna().sum()),
               "css_de_neg_m": int((SPR["DE_LU"]["css"] < 0).sum()),
               "css_ro_max": fl(SPR["RO"]["css"].max(), 2), "css_ro_max_ym": SPR["RO"]["css"].idxmax().strftime("%Y-%m"),
               "css_ro_min": fl(SPR["RO"]["css"].min(), 2), "css_ro_min_ym": SPR["RO"]["css"].idxmin().strftime("%Y-%m"),
               "gap_ro_de": fl((SPR["RO"]["css"] - SPR["DE_LU"]["css"]).mean(), 2),
               "lastm": {"p": fl(PM["RO"].iloc[-1], 2), "gas": fl(GAS.iloc[-1], 2), "eua": fl(EUAM.iloc[-1], 2),
                         "coal": fl(COALE.iloc[-1], 2), "css": fl(SPR["RO"]["css"].iloc[-1], 2), "ss": fl(SPR["RO"]["ss"].iloc[-1], 2),
                         "cds": fl(SPR["RO"]["cds"].iloc[-1], 2), "ym": m_idx[-1].strftime("%Y-%m"),
                         "fuel": fl(GAS.iloc[-1] / ETA_GAS, 2), "co2": fl(EF_GAS / ETA_GAS * EUAM.iloc[-1], 2)},
               "switch_eua": None}
# fuel-switch carbon price: CSS = CDS  <=>  EUA* = (gas/eta_g - coal/eta_c) / (ef_c/eta_c - ef_g/eta_g)
sw = (GAS / ETA_GAS - COALE / ETA_COAL) / (EF_COAL / ETA_COAL - EF_GAS / ETA_GAS)
N["spread"]["switch_eua"] = fl(sw.iloc[-1], 2)
N["spread"]["switch_eua_ym"] = m_idx[-1].strftime("%Y-%m")
N["spread"]["gas_cheaper_m"] = int((SPR["RO"]["css"] > SPR["RO"]["cds"]).sum())

# hourly optionality over the last 12 complete months: a 1 MW gas plant as a strip of hourly call options
H0 = (END - pd.DateOffset(months=12) + pd.Timedelta(days=1)).normalize()
HP = pd.read_csv(os.path.join(DATA, "power_da_prices_native_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
HP.index = HP.index.tz_convert("Europe/Brussels")
HH = HP.loc[str(H0.date()):str(END.date())].copy()
HH["w"] = HH["mtu_minutes"] / 60.0                       # hour-equivalent of each market time unit
mkey = HH.index.tz_localize(None).to_period("M").to_timestamp()
cost = (GAS / ETA_GAS + EF_GAS / ETA_GAS * EUAM)
HH["c"] = cost.reindex(mkey).values
opt = {}
for z_ in ["RO", "DE_LU"]:
    s_ = (HH[z_] - HH["c"])
    ok = s_.notna()
    w = HH.loc[ok, "w"]
    s_ = s_[ok]
    opt[z_] = {"hours": fl(w.sum(), 1), "itm_share": fl(100 * w[s_ > 0].sum() / w.sum(), 1),
               "flex_eur": fl((np.maximum(s_, 0) * w).sum(), 0), "base_eur": fl((s_ * w).sum(), 0),
               "flex_per_mwh": fl((np.maximum(s_, 0) * w).sum() / w.sum(), 2), "mean_css": fl((s_ * w).sum() / w.sum(), 2)}
    opt[z_]["ratio"] = fl(opt[z_]["flex_eur"] / max(opt[z_]["base_eur"], 1), 2) if opt[z_]["base_eur"] > 0 else None
N["opt"] = {"from": d(H0), "to": d(END), "RO": opt["RO"], "DE_LU": opt["DE_LU"]}

# =============================================================================
# 5. Minimum-variance hedge ratio and basis risk (monthly averages, RO vs HU and DE)
# =============================================================================
def hedge_ratio(dS, dF, B=2000, block=6, seed=SEED):
    """h* = Cov(dS, dF)/Var(dF) by OLS; HAC (Newey-West, 3 lags) standard error; moving-block bootstrap 95% interval."""
    X = sm.add_constant(dF.values)
    r = sm.OLS(dS.values, X).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    rng = np.random.default_rng(seed)
    n = len(dS)
    hs = []
    for _ in range(B):
        idx = np.concatenate([np.arange(s, s + block) for s in rng.integers(0, n - block + 1, size=n // block + 1)])[:n]
        a, b = dS.values[idx], dF.values[idx]
        hs.append(np.cov(a, b)[0, 1] / np.var(b, ddof=1))
    lo, hi = np.percentile(hs, [2.5, 97.5])
    return {"h": float(r.params[1]), "se": float(r.bse[1]), "lo": float(lo), "hi": float(hi), "r2": float(r.rsquared),
            "rho": float(np.corrcoef(dS, dF)[0, 1]), "n": int(n)}


dP = PM.diff().dropna()
HR = {}
for z_ in ["HU", "DE_LU"]:
    full = hedge_ratio(dP["RO"], dP[z_])
    ins = dP.loc[:"2020-12-01"]
    oos = dP.loc["2021-01-01":]
    h_in = hedge_ratio(ins["RO"], ins[z_])
    v0 = oos["RO"].var()
    vr_h = 1 - (oos["RO"] - h_in["h"] * oos[z_]).var() / v0
    vr_1 = 1 - (oos["RO"] - oos[z_]).var() / v0
    h_oos = hedge_ratio(oos["RO"], oos[z_])
    HR[z_] = {k: fl(v, 4) for k, v in full.items()}
    HR[z_].update({"h_in": fl(h_in["h"], 4), "h_in_lo": fl(h_in["lo"], 3), "h_in_hi": fl(h_in["hi"], 3),
                   "r2_in": fl(h_in["r2"], 3), "vr_oos_h": fl(100 * vr_h, 1), "vr_oos_1": fl(100 * vr_1, 1),
                   "h_oos": fl(h_oos["h"], 4), "h_oos_lo": fl(h_oos["lo"], 3), "h_oos_hi": fl(h_oos["hi"], 3),
                   "n_in": int(len(ins)), "n_oos": int(len(oos))})
HR["HU"]["q20"] = fl(20 * HR["HU"]["h"], 1)
N["hedge"] = {"first": dP.index.min().strftime("%Y-%m"), "last": dP.index.max().strftime("%Y-%m"), "HU": HR["HU"],
              "DE_LU": HR["DE_LU"], "sd_dro": fl(dP["RO"].std(), 2), "sd_dhu": fl(dP["HU"].std(), 2), "sd_dde": fl(dP["DE_LU"].std(), 2),
              "B": 2000, "block": 6}
# basis
BAS = pd.DataFrame({"HU": PM["RO"] - PM["HU"], "DE_LU": PM["RO"] - PM["DE_LU"]})
bas = {}
for z_ in ["HU", "DE_LU"]:
    b = BAS[z_].dropna()
    bas[z_] = {"mean": fl(b.mean(), 2), "sd": fl(b.std(), 2), "max": fl(b.max(), 2), "max_ym": b.idxmax().strftime("%Y-%m"),
               "min": fl(b.min(), 2), "min_ym": b.idxmin().strftime("%Y-%m"),
               "sd_pre": fl(b[:"2020-12-01"].std(), 2), "sd_post": fl(b["2021-01-01":].std(), 2),
               "mean_post": fl(b["2023-01-01":].mean(), 2)}
# hourly price convergence RO = HU (|diff| < 0.01 EUR/MWh), duration-weighted, by year
NP = HP.loc[:str(END.date())].copy()
NP["w"] = NP["mtu_minutes"] / 60
okc = NP["RO"].notna() & NP["HU"].notna()
NP = NP[okc]
conv = (NP["w"] * ((NP["RO"] - NP["HU"]).abs() < 0.01)).groupby(NP.index.year).sum() / NP["w"].groupby(NP.index.year).sum() * 100
convd = (NP["w"] * ((NP["RO"] - NP["DE_LU"]).abs() < 0.01)).groupby(NP.index.year).sum() / NP["w"].groupby(NP.index.year).sum() * 100
bas["conv_hu"] = {str(y): fl(v, 1) for y, v in conv.items()}
bas["conv_de"] = {str(y): fl(v, 1) for y, v in convd.items()}
_mx = BAS["DE_LU"].idxmax()
bas["DE_LU"]["max_ro"] = fl(PM.loc[_mx, "RO"], 2)
bas["DE_LU"]["max_de"] = fl(PM.loc[_mx, "DE_LU"], 2)
N["basis"] = bas

# =============================================================================
# 6. Shape risk: load-weighted price and solar capture price relative to the baseload average
# =============================================================================
GH = pd.read_csv(os.path.join(DATA, "generation_ro_mw_hourly_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
PH = pd.read_csv(os.path.join(DATA, "power_da_prices_hourly_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
J = pd.concat([PH["RO"], GH["load"], GH["solar"]], axis=1).loc[:str(END.date()) + " 21:00"].dropna()
J = J[J.index >= "2015-01-05"]
J["y"] = J.index.tz_convert("Europe/Brussels").year


def profile_factor(g):
    base = g["RO"].mean()
    return pd.Series({"base": base, "load_w": (g["RO"] * g["load"]).sum() / g["load"].sum(),
                      "solar_w": (g["RO"] * g["solar"]).sum() / g["solar"].sum() if g["solar"].sum() > 0 else np.nan})


PF = J.groupby("y").apply(profile_factor)
PF["f_load"] = PF["load_w"] / PF["base"]
PF["f_solar"] = PF["solar_w"] / PF["base"]
N["shape"] = {"years": [int(y) for y in PF.index], "f_load": {str(y): fl(v, 3) for y, v in PF["f_load"].items()},
              "f_solar": {str(y): fl(v, 3) for y, v in PF["f_solar"].items()},
              "load_prem": {str(y): fl(PF.loc[y, "load_w"] - PF.loc[y, "base"], 2) for y in PF.index},
              "solar_disc": {str(y): fl(PF.loc[y, "base"] - PF.loc[y, "solar_w"], 2) for y in PF.index},
              "last_year": int(PF.index.max()), "solar_min": fl(PF["f_solar"].min(), 3), "solar_min_y": int(PF["f_solar"].idxmin()),
              "n_hours": int(len(J))}

# =============================================================================
# 7. Options: Black-76 with real inputs; Samuelson effect in TTF futures
# =============================================================================
def black76(F, K, T, r, sigma, kind="call"):
    """Black (1976) price of a European option on a forward/futures F; returns price, delta, vega (per 1 vol point)."""
    d1 = (np.log(F / K) + 0.5 * sigma ** 2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    disc = np.exp(-r * T)
    if kind == "call":
        p, delta = disc * (F * norm.cdf(d1) - K * norm.cdf(d2)), disc * norm.cdf(d1)
    else:
        p, delta = disc * (K * norm.cdf(-d2) - F * norm.cdf(-d1)), -disc * norm.cdf(-d1)
    vega = disc * F * norm.pdf(d1) * np.sqrt(T) / 100
    return float(p), float(delta), float(vega), float(d1), float(d2)


# Samuelson effect: same calendar window, contracts with different delivery months (single contracts, no rolls)
def ann_vol(s, window=None):
    """Annualised volatility of daily log returns between consecutive trading days (gaps <= 4 calendar days)."""
    s = s.dropna()
    r_ = np.log(s).diff().dropna()
    gap = s.index.to_series().diff().dt.days.reindex(r_.index)
    r_ = r_[gap <= 4]
    return r_ if window is None else r_.rolling(window).std() * np.sqrt(252)


W12 = (END - pd.DateOffset(months=12) + pd.Timedelta(days=1)).normalize()
sam = {"w_from": d(W12), "w_to": d(END)}
for col in TTFC.columns:
    r_ = ann_vol(TTFC[col])
    sam[col] = {"v12": fl(r_.loc[W12:END].std() * np.sqrt(252) * 100, 1), "v22": fl(r_.loc["2022"].std() * np.sqrt(252) * 100, 1),
                "n": int(len(r_)), "first": d(r_.index.min())}
_ld = TTFC["2026-12"].dropna().index[-1]                  # last trading day to the cut-off
N["ttfcurve"] = {c: fl(TTFC.loc[_ld, c], 2) for c in TTFC.columns if pd.notna(TTFC.loc[_ld, c])}   # contracts quoted that day
N["ttfcurve"]["date"] = d(_ld)
ROLLV = pd.DataFrame({c: ann_vol(TTFC[c], 60) for c in ["2026-12", "2027-05"]})
N["sam"] = sam
z26 = TTFC["2026-12"].dropna()
dz = z26.diff().dropna()
N["margin"] = {"max_abs": fl(dz.abs().max(), 2), "max_date": d(dz.abs().idxmax()), "pos_mwh": 10 * 744,
               "call_eur": fl(dz.abs().max() * 10 * 744, 0), "last": fl(z26.iloc[-1], 2), "last_date": d(z26.index[-1]),
               "n": int(len(z26)), "first": d(z26.index[0]), "min": fl(z26.min(), 2), "max": fl(z26.max(), 2),
               "max_date_p": d(z26.idxmax()), "q99_abs": fl(dz.abs().quantile(0.99), 2)}
# volatility inputs
v60 = ann_vol(TTFC["2027-01"]).iloc[-60:].std() * np.sqrt(252)


def cal_vol(g, max_gap=30):
    """Volatility of a calendar forward from irregular auction days: daily VWAP, sigma^2 = sum (d ln F)^2 / sum dt,
    using only pairs of auction days at most max_gap calendar days apart."""
    dv = g.groupby("auction_date").apply(vwap)
    dl = np.log(dv).diff().dropna()
    dt = dv.index.to_series().diff().dt.days.dropna() / 365.25
    m = dt <= max_gap / 365.25
    return dl[m], dt[m]


CV = {}
DL, DT = [], []
for y in [END.year - 1, END.year, END.year + 1]:
    dl, dt = cal_vol(CY[CY["dy"] == y])
    CV[str(y)] = {"sig": fl(np.sqrt((dl ** 2).sum() / dt.sum()), 4), "n": int(len(dl))}
    DL.append(dl)
    DT.append(dt)
sig_cal = float(np.sqrt(sum((x ** 2).sum() for x in DL) / sum(x.sum() for x in DT)))
N["calvol"] = {"pooled": fl(sig_cal, 4), "n": int(sum(len(x) for x in DL)), "by": CV, "max_gap": 30}
R_ = RATES["estr_pct"].loc[:END].dropna()
r0 = R_.iloc[-1] / 100
F0 = N["curve"]["cal_next"]["F"]
EXPIRY = pd.Timestamp(f"{END.year}-12-15")
T0 = (EXPIRY - END).days / 365.25
sig_term = N["termvol"]["all"]
opts = {"F": F0, "r": fl(r0 * 100, 3), "T": fl(T0, 4), "T_days": int((EXPIRY - END).days), "expiry": d(EXPIRY),
        "sig_gas": fl(v60, 4), "sig_cal": fl(sig_cal, 4), "sig_term": fl(sig_term, 4), "estr_date": d(R_.index[-1])}
for lab, sg in [("g", v60), ("c", sig_cal)]:
    c, dc, vc, d1, d2 = black76(F0, F0, T0, r0, sg, "call")
    p, dp, vp, _, _ = black76(F0, F0, T0, r0, sg, "put")
    c110, dc110, _, _, _ = black76(F0, 1.1 * F0, T0, r0, sg, "call")
    p90, dp90, _, _, _ = black76(F0, 0.9 * F0, T0, r0, sg, "put")
    opts[lab] = {"call": fl(c, 2), "put": fl(p, 2), "delta_c": fl(dc, 3), "delta_p": fl(dp, 3), "vega": fl(vc, 3),
                 "d1": fl(d1, 3), "d2": fl(d2, 3), "call110": fl(c110, 2), "put90": fl(p90, 2), "collar": fl(c110 - p90, 2),
                 "call_pct": fl(100 * c / F0, 1), "call110_pct": fl(100 * c110 / F0, 1), "delta_c110": fl(dc110, 3),
                 "parity": fl(c - p - np.exp(-r0 * T0) * (F0 - F0), 6)}
opts["K110"] = fl(1.1 * F0, 2)
opts["K90"] = fl(0.9 * F0, 2)
opts["mw_year"] = fl(opts["c"]["call110"] * 8760, 0)
N["bs"] = opts

# =============================================================================
# 8. Case study: a Romanian supplier and a producer, 2026 (Jan to the cut-off) and 2025
# =============================================================================
c26 = CY[CY["dy"] == END.year]
F26 = vwap(c26)
mm = pd.date_range(f"{END.year}-01-01", END.replace(day=1), freq="MS")
S26 = pd.Series([realised(m_, m_ + pd.offsets.MonthEnd(0)) for m_ in mm], index=mm)
hrs = pd.Series([((m_ + pd.offsets.MonthEnd(0) + pd.Timedelta(days=1)).tz_localize("Europe/Brussels") -
                  m_.tz_localize("Europe/Brussels")) / pd.Timedelta(hours=1) for m_ in mm], index=mm)
# cap strip bought on the last auction quarter of the previous year: K = VWAP of that quarter, sigma = terminal vol
REFQ0 = pd.Timestamp(f"{END.year - 1}-10-01")
ref = c26[c26["auction_date"] >= REFQ0]
if len(ref) == 0:
    ref = c26[c26["auction_date"] >= pd.Timestamp(f"{END.year - 1}-07-01")]
Fref = vwap(ref)
BUYD = pd.Timestamp(f"{END.year - 1}-12-15")
rb = RATES["estr_pct"].loc[:BUYD].dropna().iloc[-1] / 100
prem_m = pd.Series([black76(Fref, Fref, ((m_ + pd.Timedelta(days=14)) - BUYD).days / 365.25, rb, sig_term)[0] for m_ in mm], index=mm)
STRAT = pd.DataFrame({"spot": S26, "fwd": F26, "half": 0.5 * F26 + 0.5 * S26,
                      "cap": S26 - np.maximum(S26 - Fref, 0) + prem_m})
w_ = hrs / hrs.sum()
cs = {"F26": fl(F26, 2), "n26": int(len(c26)), "twh26": fl(c26["mwh"].sum() / 1e6, 3), "first26": d(c26["auction_date"].min()),
      "last26": d(c26["auction_date"].max()), "Fref": fl(Fref, 2), "nref": int(len(ref)), "ref_from": d(ref["auction_date"].min()),
      "months": len(mm), "m_last": mm[-1].strftime("%Y-%m"), "prem_mean": fl(prem_m.mean(), 2), "r_buy": fl(rb * 100, 3)}
for k in STRAT:
    x = STRAT[k]
    cs[k] = {"mean": fl((x * w_).sum(), 2), "sd": fl(x.std(), 2), "max": fl(x.max(), 2), "min": fl(x.min(), 2),
             "eur_mw": fl((x * hrs).sum(), 0)}
cs["spot_max_ym"] = S26.idxmax().strftime("%Y-%m")
cs["save_fwd"] = fl(cs["spot"]["eur_mw"] - cs["fwd"]["eur_mw"], 0)
cs["save_cap"] = fl(cs["spot"]["eur_mw"] - cs["cap"]["eur_mw"], 0)
cs["n_cap_pay"] = int((S26 > Fref).sum())
cs["n_fwd_win"] = int((S26 > F26).sum())
N["case"] = cs
# producer: calendar 2025 sold forward vs spot 2025
c25 = CY[CY["dy"] == END.year - 1]
S25 = realised(pd.Timestamp(f"{END.year - 1}-01-01"), pd.Timestamp(f"{END.year - 1}-12-31"))
N["prod"] = {"F25": fl(vwap(c25), 2), "S25": fl(S25, 2), "n25": int(len(c25)), "twh25": fl(c25["mwh"].sum() / 1e6, 2),
             "gap": fl(vwap(c25) - S25, 2), "eur_mw": fl((vwap(c25) - S25) * 8760, 0),
             "share_top3": fl(100 * c25.loc[c25["seller"].isin(PROD3), "mwh"].sum() / c25["mwh"].sum(), 1),
             "gap22": fl(F22 - S22, 2), "loss": fl(S25 - vwap(c25), 2), "loss_mw": fl((S25 - vwap(c25)) * 8760, 0),
             "loss22": fl(S22 - F22, 2)}

# =============================================================================
# Charts
# =============================================================================
SRC = {"en": {"fw": "OPCOM, PCCB-LE-flex results; ECB (EUR/RON)",
              "fws": "OPCOM (PCCB-LE-flex results; day-ahead prices via energy-charts.info); ECB",
              "spr": "energy-charts.info; World Bank (TTF, coal); EEX and SparkChange ETC (EUA); ECB",
              "hr": "energy-charts.info: day-ahead prices of OPCOM, HUPX, EPEX SPOT",
              "sh": "energy-charts.info: OPCOM prices; ENTSO-E load and solar output",
              "ttf": "Yahoo Finance, NYMEX TTF futures",
              "bs": "OPCOM PCCB-LE-flex; ECB (€STR); Black-76"},
       "ro": {"fw": "OPCOM, rezultatele PCCB-LE-flex; BCE (EUR/RON)",
              "fws": "OPCOM (rezultatele PCCB-LE-flex; prețuri PZU, prin energy-charts.info); BCE",
              "spr": "energy-charts.info; Banca Mondială (TTF, cărbune); EEX și SparkChange ETC (EUA); BCE",
              "hr": "energy-charts.info: prețurile PZU ale OPCOM, HUPX, EPEX SPOT",
              "sh": "energy-charts.info: prețuri OPCOM; consum și producție solară ENTSO-E",
              "ttf": "Yahoo Finance, contracte futures NYMEX TTF",
              "bs": "OPCOM PCCB-LE-flex; BCE (€STR); Black-76"}}


def de_(n):
    """Romanian 'de' after counts ending in 20-99 or 00."""
    n = int(n)
    s = f"{n:,}".replace(",", "\\,")
    return f"{s} de" if n >= 20 and (n % 100 >= 20 or n % 100 == 0) else s


def chart(name, src_key, period_en, period_ro):
    N["charts"][name] = {"source_en": SRC["en"][src_key], "source_ro": SRC["ro"][src_key], "period_en": period_en, "period_ro": period_ro}


def _dec_formatter(axis):
    """Decimal-comma tick labels with the same number of decimals on every tick of the axis."""
    lo, hi = sorted(axis.get_view_interval())
    locs = [v for v in axis.get_ticklocs() if lo - 1e-9 <= v <= hi + 1e-9]
    dec = max([len(f"{v:g}".split(".")[1]) if "." in f"{v:g}" else 0 for v in locs] or [0])
    return FuncFormatter(lambda v, p: f"{v:.{dec}f}".replace(".", ",").replace("-", "\u2212"))


def comma_axes(fig, lang, also_x=()):
    if lang != "ro":
        return
    fig.canvas.draw()
    for ax in fig.axes:
        if ax.get_yscale() == "linear" and not getattr(ax, "_keep_y", False):
            ax.yaxis.set_major_formatter(_dec_formatter(ax.yaxis))
    for ax in also_x:
        ax.xaxis.set_major_formatter(_dec_formatter(ax.xaxis))


def out(fig, lang, name, also_x=()):
    """Save one chart; the space kept under the axes is exactly the height of the bottom legend (if any)."""
    comma_axes(fig, lang, also_x)
    fig.canvas.draw()
    W, H = fig.bbox.width, fig.bbox.height
    bottom = 0.0
    for lg in fig.legends:
        ext = lg.get_window_extent()
        bottom = max(bottom, ext.height / H + 0.035)
        if ext.width > W * 1.001:
            print(f"  WARNING {name} [{lang}]: legend wider than the figure ({ext.width / fig.dpi:.2f} in)")
    os.makedirs(os.path.join(HERE, "charts", lang), exist_ok=True)
    save(fig, os.path.join(HERE, "charts", lang, name + ".pdf"), bottom=bottom)


def legend_compact(fig, ncol):
    """Course bottom legend with shorter handles and column gaps, for many short entries."""
    legend_bottom(fig, ncol=ncol)
    h, l_ = fig.legends[-1].legend_handles, [t_.get_text() for t_ in fig.legends[-1].get_texts()]
    fig.legends[-1].remove()
    fig.legend(h, l_, loc="lower center", ncol=ncol, bbox_to_anchor=(0.5, 0.0), frameon=False,
               handlelength=1.0, handletextpad=0.4, columnspacing=0.9)


KCOL = {"M": PAL["RO"], "Q": PAL["HU"], "H": PAL["BG"], "Y": PAL["DE_LU"], "other": "#9a9a9a"}
SPOT_M = PD["RO"].loc[:END].resample("MS").mean()
for lang in ["en", "ro"]:
    T = (lambda en, ro: en) if lang == "en" else (lambda en, ro: ro)
    KL = {"M": T("month", "lună"), "Q": T("quarter", "trimestru"), "H": T("half-year", "semestru"), "Y": T("calendar year", "an calendaristic"),
          "other": T("other periods", "alte perioade")}
    # 1 volumes
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    bot = np.zeros(len(vol))
    for k in ["Y", "H", "Q", "M", "other"]:
        if k in vol:
            ax.bar(vol.index, vol[k].values, bottom=bot, color=KCOL[k], width=0.7, label=KL[k])
            bot += vol[k].values
    ax.set_ylabel("TWh")
    ax.set_xticks(vol.index)
    ax.set_xticklabels([str(y) + ("*" if y == END.year else "") for y in vol.index])
    legend_compact(fig, ncol=5)
    out(fig, lang, "fw_volume")
    # 2 crisis: calendar-2022 forward trades vs monthly spot
    fig, ax = plt.subplots(figsize=(6.4, 2.1))
    sm_ = SPOT_M.loc["2020-01-01":"2022-12-01"]
    ax.plot(sm_.index + pd.Timedelta(days=14), sm_.values, color=PAL["RO"], lw=1.4, label=T("Romania, monthly mean day-ahead", "România, media lunară PZU"))
    ax.scatter(c22["auction_date"], c22["price_eur_mwh"], s=9, color=PAL["DE_LU"], zorder=3,
               label=T("forward for Cal-22 baseload, one auction", "forward pentru banda 2022, o licitație"))
    ax.hlines(S22, pd.Timestamp("2022-01-01"), pd.Timestamp("2022-12-31"), color="#222222", lw=1.2, ls="--",
              label=T("realised 2022 average", "media realizată în 2022"))
    ax.hlines(F22, pd.Timestamp("2022-01-01"), pd.Timestamp("2022-12-31"), color=PAL["DE_LU"], lw=1.2, ls="--",
              label=T("volume-weighted forward", "forward mediu ponderat"))
    ax.set_ylabel("EUR/MWh")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, ncol=2)
    out(fig, lang, "crisis_cal22")
    # 3 calendar products by trade date + realised
    fig, ax = plt.subplots(figsize=(6.4, 2.05))
    cols_ = [PAL["RO"], PAL["HU"], PAL["DE_LU"], PAL["c7"], PAL["BG"], PAL["c5"], PAL["c6"]]
    for i, y in enumerate([y for y in sorted(calt) if int(y) <= END.year + 1]):
        g = CY[CY["dy"] == int(y)]
        ax.scatter(g["auction_date"], g["price_eur_mwh"], s=7, color=cols_[i % len(cols_)], label=T(f"Cal-{y[2:]}", y))
        if calt[y]["realised"] is not None and int(y) <= END.year - 1:
            ax.hlines(calt[y]["realised"], pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y}-12-31"), color=cols_[i % len(cols_)], lw=2.0)
    ax.set_ylabel("EUR/MWh")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_compact(fig, ncol=7)
    out(fig, lang, "cal_by_trade")
    # 4 forward curve today
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    sp = SPOT_M.loc[END - pd.DateOffset(months=23):]
    ax.step(sp.index, sp.values, where="post", color=PAL["RO"], lw=1.3, label=T("realised monthly mean day-ahead price", "media lunară realizată a prețului PZU"))
    for r in curve.sort_values("kind").itertuples():
        ax.hlines(r.F, r.delivery_start, r.delivery_end + pd.Timedelta(days=1), color=KCOL[r.kind], lw=2.4)
    from matplotlib.lines import Line2D
    hnd = [Line2D([], [], color=PAL["RO"], lw=1.3)] + [Line2D([], [], color=KCOL[k], lw=2.4) for k in ["M", "Q", "H", "Y"] if (curve["kind"] == k).any()]
    lab = [T("realised monthly mean (PZU)", "media lunară realizată (PZU)")] + [T("forward, ", "forward, ") + KL[k] for k in ["M", "Q", "H", "Y"] if (curve["kind"] == k).any()]
    ax.axvline(END + pd.Timedelta(days=1), color="#222222", lw=0.8, ls=":")
    ax.set_ylabel("EUR/MWh")
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: (MON_EN if lang == "en" else MON_RO)[mdates.num2date(v).month - 1] + f"\n{mdates.num2date(v).year}"))
    legend_bottom(fig, handles=hnd, labels=lab, ncol=2)
    out(fig, lang, "fwd_curve")
    # 5 forward premium of one-month-ahead monthly products
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    ax.bar(MP.index, MP["prem"], width=25, color=[PAL["DE_LU"] if v > 0 else PAL["RO"] for v in MP["prem"]])
    ax.axhline(0, color="#222222", lw=0.6)
    from matplotlib.patches import Patch
    hnd = [Patch(color=PAL["DE_LU"], label=T("F above realised spot (premium paid)", "F peste spotul realizat (primă plătită)")),
           Patch(color=PAL["RO"], label=T("F below realised spot", "F sub spotul realizat"))]
    ax.set_ylabel(T("F minus realised,\nEUR/MWh", "F minus realizat,\nEUR/MWh"), fontsize=10)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, handles=hnd, labels=[h_.get_label() for h_ in hnd], ncol=2)
    out(fig, lang, "premium")
    # 6 clean spark and clean dark spreads
    fig, ax = plt.subplots(figsize=(6.4, 2.2))
    ax.plot(SPR["RO"].index, SPR["RO"]["css"], color=PAL["RO"], lw=1.3, label=T("clean spark, Romania", "clean spark, România"))
    ax.plot(SPR["DE_LU"].index, SPR["DE_LU"]["css"], color=PAL["DE_LU"], lw=1.1, ls=":", label=T("clean spark, Germany", "clean spark, Germania"))
    ax.plot(SPR["RO"].index, SPR["RO"]["cds"], color=PAL["c7"], lw=1.1, ls="--", label=T("clean dark, Romania", "clean dark, România"))
    ax.axhline(0, color="#222222", lw=0.6)
    ax.set_ylabel(T("EUR per MWh\nof electricity", "EUR pe MWh de\nenergie electrică"), fontsize=10)
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_compact(fig, ncol=3)
    out(fig, lang, "spreads")
    # 7 hourly spark duration curve
    fig, ax = plt.subplots(figsize=(6.4, 2.3))
    for z_, col, ls in [("RO", PAL["RO"], "-"), ("DE_LU", PAL["DE_LU"], ":")]:
        s_ = (HH[z_] - HH["c"]).dropna()
        w = HH.loc[s_.index, "w"]
        o = np.argsort(-s_.values)
        ax.plot(np.cumsum(w.values[o]), s_.values[o], color=col, ls=ls, lw=1.4,
                label=T("Romania", "România") if z_ == "RO" else T("Germany", "Germania"))
    ax.axhline(0, color="#222222", lw=0.6)
    ax.set_ylim(-250, 400)
    ax.set_xlabel(T("hours of the last 12 months, sorted from the highest spread", "orele ultimelor 12 luni, ordonate descrescător după spread"))
    ax.set_ylabel(T("clean spark,\nEUR/MWh", "clean spark,\nEUR/MWh"), fontsize=10)
    legend_bottom(fig, ncol=2)
    out(fig, lang, "spark_hourly", also_x=[ax])
    # 8 hedge scatter
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.95), sharey=True)
    for ax, z_, col, nm in [(axs[0], "HU", PAL["HU"], T("Hungary", "Ungaria")), (axs[1], "DE_LU", PAL["DE_LU"], T("Germany", "Germania"))]:
        ax.scatter(dP[z_], dP["RO"], s=8, color=col, alpha=0.8)
        xx = np.linspace(dP[z_].min(), dP[z_].max(), 10)
        ax.plot(xx, HR[z_]["h"] * xx, color="#222222", lw=1.0)
        ax.set_xlabel(f"Δ {nm}, EUR/MWh", fontsize=10)
        ax.text(0.03, 0.92, f"h* = {HR[z_]['h']:.2f}".replace(".", "," if lang == "ro" else ".") + f",  R² = {HR[z_]['r2']:.2f}".replace(".", "," if lang == "ro" else "."),
                transform=ax.transAxes, fontsize=10)
    axs[0].set_ylabel(T("Δ Romania,\nEUR/MWh", "Δ România,\nEUR/MWh"), fontsize=10)
    out(fig, lang, "hedge_scatter", also_x=list(axs))
    # 9 basis + convergence
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.05), gridspec_kw={"width_ratios": [1.6, 1]})
    axs[0].plot(BAS.index, BAS["HU"], color=PAL["HU"], lw=1.2, label=T("Romania minus Hungary", "România minus Ungaria"))
    axs[0].plot(BAS.index, BAS["DE_LU"], color=PAL["DE_LU"], lw=1.0, ls=":", label=T("Romania minus Germany", "România minus Germania"))
    axs[0].axhline(0, color="#222222", lw=0.6)
    axs[0].set_ylabel(T("monthly basis,\nEUR/MWh", "baza lunară,\nEUR/MWh"), fontsize=10)
    axs[0].xaxis.set_major_locator(mdates.YearLocator(3))
    axs[0].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    yy = [int(y) for y in conv.index]
    axs[1].bar([y - 0.2 for y in yy], conv.values, width=0.4, color=PAL["HU"])
    axs[1].bar([y + 0.2 for y in yy], convd.values, width=0.4, color=PAL["DE_LU"])
    axs[1].set_ylabel(T("% of hours with\nthe same price", "% din ore cu\nacelași preț"), fontsize=10)
    axs[1].set_xticks([2015, 2020, 2025])
    legend_bottom(fig, ncol=2)
    out(fig, lang, "basis")
    # 10 shape factors
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    ax.plot(PF.index, PF["f_load"], marker="o", ms=3.5, color=PAL["RO"], lw=1.3, label=T("load-weighted / baseload price", "preț ponderat cu consumul / bandă"))
    ax.plot(PF.index, PF["f_solar"], marker="s", ms=3.5, color=PAL["BG"], lw=1.3, label=T("solar capture / baseload price", "preț capturat de solar / bandă"))
    ax.axhline(1, color="#222222", lw=0.6)
    ax.set_xticks(PF.index)
    ax.set_xticklabels([str(y)[2:] + ("*" if y == END.year else "") for y in PF.index])
    ax.set_ylabel(T("ratio", "raport"))
    legend_bottom(fig, ncol=2)
    out(fig, lang, "shape")
    # 11 Samuelson: rolling 60-day volatility of the December and May contracts
    fig, ax = plt.subplots(figsize=(6.4, 2.0))
    for col, cc, ls in [("2026-12", PAL["RO"], "-"), ("2027-05", PAL["DE_LU"], ":")]:
        v = ROLLV[col].dropna() * 100
        ax.plot(v.index, v.values, color=cc, ls=ls, lw=1.3,
                label=T("TTF contract for ", "contractul TTF pentru ") + (MON_EN if lang == "en" else MON_RO)[int(col[5:]) - 1] + " " + col[:4])
    ax.set_ylabel(T("volatility,\n% per year", "volatilitate,\n% pe an"), fontsize=10)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    legend_bottom(fig, ncol=2)
    out(fig, lang, "samuelson")
    # 12 collar / cap payoff with real inputs
    fig, ax = plt.subplots(figsize=(6.4, 2.05))
    FT = np.linspace(0.75 * F0, 1.3 * F0, 200)
    cT, pT = opts["c"]["call110"] * np.exp(r0 * T0), opts["c"]["put90"] * np.exp(r0 * T0)
    ax.plot(FT, FT, color="#9a9a9a", lw=1.2, label=T("unhedged", "neacoperit"))
    ax.plot(FT, np.full_like(FT, F0), color=PAL["HU"], lw=1.4, label=T("forward at F", "forward la F"))
    ax.plot(FT, np.minimum(FT, 1.1 * F0) + cT, color=PAL["DE_LU"], lw=1.4, ls="--", label=T("cap at 1.1 F", "plafon la 1,1 F"))
    ax.plot(FT, np.clip(FT, 0.9 * F0, 1.1 * F0) + cT - pT, color=PAL["c7"], lw=1.4, ls="-.", label=T("collar 0.9 F to 1.1 F", "collar 0,9 F - 1,1 F"))
    ax.set_xlabel(T("forward price at expiry $F_T$, EUR/MWh", "prețul forward la scadență $F_T$, EUR/MWh"))
    ax.set_ylabel(T("effective price,\nEUR/MWh", "preț efectiv,\nEUR/MWh"), fontsize=10)
    legend_compact(fig, ncol=4)
    out(fig, lang, "collar", also_x=[ax])
    # 13 case study 2026
    fig, ax = plt.subplots(figsize=(6.4, 2.1))
    xm = STRAT.index + pd.Timedelta(days=14)
    ax.plot(xm, STRAT["spot"], marker="o", ms=3.5, color="#9a9a9a", lw=1.3, label=T("unhedged (spot)", "neacoperit (spot)"))
    ax.plot(xm, STRAT["fwd"], color=PAL["HU"], lw=1.6, label=T(f"100% forward Cal-{str(END.year)[2:]}", f"100% forward pentru {END.year}"))
    ax.plot(xm, STRAT["half"], color=PAL["RO"], lw=1.2, ls=":", label=T("50% forward + 50% spot", "50% forward + 50% spot"))
    ax.plot(xm, STRAT["cap"], color=PAL["DE_LU"], lw=1.3, ls="--", marker="s", ms=3, label=T("monthly caps at K", "plafoane lunare la K"))
    ax.set_ylabel(T("cost, EUR/MWh", "cost, EUR/MWh"))
    ax.set_xticks(xm)
    ax.set_xticklabels([(MON_EN if lang == "en" else MON_RO)[m_.month - 1] for m_ in STRAT.index])
    legend_bottom(fig, ncol=2)
    out(fig, lang, "case2026")

chart("fw_volume", "fw", f"{len(FW):,} traded auctions, {d(FW['auction_date'].min())} to {d(END)}; *{END.year} to the cut-off",
      f"{de_(len(FW))} licitații încheiate, {d(FW['auction_date'].min())} - {d(END)}; *{END.year} pînă la data-limită")
chart("crisis_cal22", "fws", f"{len(c22)} auctions for 2022 baseload; spot 2020-2022", f"{de_(len(c22))} licitații pentru banda 2022; spot 2020-2022")
chart("cal_by_trade", "fws", f"calendar-year baseload auctions to {d(END)}; thick line = realised mean", f"licitații pentru ani calendaristici, pînă la {d(END)}; linia groasă = media realizată")
chart("fwd_curve", "fws", f"{len(cur)} auctions {d(CURVE_FROM)} to {d(END)}", f"{de_(len(cur))} licitații, {d(CURVE_FROM)} - {d(END)}")
chart("premium", "fws", f"{len(MP)} delivery months, {MP.index.min():%Y-%m} to {MP.index.max():%Y-%m}", f"{de_(len(MP))} luni de livrare, {MP.index.min():%Y-%m} - {MP.index.max():%Y-%m}")
chart("spreads", "spr", f"monthly, {m_idx[0]:%Y-%m} to {m_idx[-1]:%Y-%m}", f"lunar, {m_idx[0]:%Y-%m} - {m_idx[-1]:%Y-%m}")
chart("spark_hourly", "spr", f"{d(H0)} to {d(END)}, hourly", f"{d(H0)} - {d(END)}, date orare")
chart("hedge_scatter", "hr", f"monthly changes, {dP.index.min():%Y-%m} to {dP.index.max():%Y-%m}", f"variații lunare, {dP.index.min():%Y-%m} - {dP.index.max():%Y-%m}")
chart("basis", "hr", f"{m_idx[0]:%Y-%m} to {m_idx[-1]:%Y-%m}; right: |difference| < 0.01 EUR/MWh", f"{m_idx[0]:%Y-%m} - {m_idx[-1]:%Y-%m}; dreapta: diferență sub 0,01 EUR/MWh")
chart("shape", "sh", f"hourly, {J.index.min().year} to {d(END)}; *to the cut-off", f"date orare, {J.index.min().year} - {d(END)}; *pînă la data-limită")
chart("samuelson", "ttf", f"daily closes to {d(END)}, rolling 60 trading days", f"prețuri zilnice pînă la {d(END)}, fereastră mobilă de 60 de zile")
chart("collar", "bs", f"F = Cal-{str(END.year + 1)[2:]} baseload, auctions {d(CURVE_FROM)} to {d(END)}", f"F = banda pentru {END.year + 1}, licitații {d(CURVE_FROM)} - {d(END)}")
chart("case2026", "fws", f"{END.year}-01 to {END:%Y-%m}; 1 MW baseload", f"{END.year}-01 - {END:%Y-%m}; 1 MW în bandă")

with open(os.path.join(HERE, "L5_numbers.json"), "w") as fh:
    json.dump(N, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("wrote L5_numbers.json and", len(N["charts"]), "charts x 2 languages")
