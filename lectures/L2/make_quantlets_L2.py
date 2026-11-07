"""
make_quantlets_L2.py -- one Quantlet per chart of Lecture 2 (EMQA)
===================================================================
Writes Quantlets/L2/EMQA_L2_<chart>/ for every chart shown in the Lecture 2 decks (lectures/L2/build_L2.py):
    Metainfo.txt                description (with the real data period), keywords, data used
    EMQA_L2_<chart>.ipynb       self-contained English notebook, executed: loads only the data it needs, computes, draws
    <chart>.png                 the chart
    saved results (some)        small .csv/.npz with the LEAR, GBM, MLP and QRA forecasts the chart needs, taken from
                                lectures/L2/cache (the engine of analysis_L2.py); each such notebook has RUN_ALL = False
                                and the full recomputation code under `if RUN_ALL:`

The notebooks never import the lecture modules: the model functions are copied verbatim from analysis_L2.py (extracted
with the ast module), so they run exactly the code behind the slides. The expert ARX models are cheap (seconds) and are
always recomputed; LEAR (about 2.5 s per day and window), the monthly machine-learning refits and QRA are loaded.

After execution every number the notebook prints is compared with lectures/L2/L2_numbers.json (the numbers on the
slides); a mismatch is reported and makes the script exit with an error.

Run (after analysis_L2.py):  python3 lectures/L2/make_quantlets_L2.py            [chart names to build only these]
"""

import ast
import hashlib
import json
import os
import pickle
import re
import sys

import nbformat
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_quantlet import Quantlet  # noqa: E402

SRC = open(os.path.join(HERE, "analysis_L2.py"), encoding="utf-8").read()
TREE = ast.parse(SRC)
NUM = json.load(open(os.path.join(HERE, "L2_numbers.json"), encoding="utf-8"))
DATA = os.path.join(REPO, "data", "clean")
TZ = "Europe/Brussels"


def fsrc(*names):
    """Source of top-level functions of analysis_L2.py, verbatim, in the given order."""
    out = []
    for nm in names:
        node = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == nm)
        out.append(ast.get_source_segment(SRC, node))
    return "\n\n\n".join(out)


# =============================================================================
# 1. Saved results: the heavy forecasts of the engine (lectures/L2/cache), cut to what each chart needs
# =============================================================================
PD_ = pd.read_csv(os.path.join(DATA, "power_da_prices_daily_cet.csv"), parse_dates=["date_cet"]).set_index("date_cet")
G_ = pd.read_csv(os.path.join(DATA, "generation_ro_mw_daily_cet.csv"), parse_dates=["date_cet"]).set_index("date_cet")
_last = min(PD_["RO"].dropna().index.max(), G_["hydro_run_of_river"].dropna().index.max())
END = pd.Timestamp(((_last + pd.Timedelta(days=1)).to_period("M").to_timestamp() - pd.Timedelta(days=1)).date())
N_TEST, N_BURN = 365, 182
TEST0 = END - pd.Timedelta(days=N_TEST - 1)
FC0 = TEST0 - pd.Timedelta(days=N_BURN)
FDAYS = pd.date_range(FC0, END, freq="D")
TDAYS = pd.date_range(TEST0, END, freq="D")
assert NUM["design"]["test_start"] == str(TEST0.date()) and NUM["design"]["burn_start"] == str(FC0.date())


def data_hash():
    """Same key as analysis_L2.py: the cache must belong to the current data and engine."""
    h = hashlib.sha256(b"L2-engine-v4")
    for f in ["power_da_prices_hourly_utc.csv", "generation_ro_mw_hourly_utc.csv", "generation_ro_mw_daily_cet.csv",
              "crossborder_ro_mw_daily_cet.csv", "eua_daily.csv"]:
        h.update(open(os.path.join(DATA, f), "rb").read())
    h.update(str(END.date()).encode())
    return h.hexdigest()[:16]


with open(os.path.join(HERE, "cache", "forecasts.pkl"), "rb") as fh:
    FC = pickle.load(fh)
with open(os.path.join(HERE, "cache", "qra.pkl"), "rb") as fh:
    QC = pickle.load(fh)
KEY = data_hash()
assert FC["key"] == KEY and QC["key"] == KEY, "cache out of date: run python3 lectures/L2/analysis_L2.py first"
POS_T = np.arange(N_BURN, N_BURN + N_TEST)                      # test days inside FDAYS
QRA_T = np.sort(QC["q"][POS_T], axis=2)                          # as in analysis_L2.py: rearranged, test year


def series(name, days="test"):
    if name in ("gbm", "mlp"):
        assert days == "test"
        return FC[name]
    x = FC["point"][name]
    return x[POS_T] if days == "test" else x


def save_csv(folder, fname, cols, days="test"):
    """Long format: one row per (date, hour), one column per series; full precision (read back with round_trip)."""
    dd = TDAYS if days == "test" else FDAYS
    df = pd.DataFrame({"date": np.repeat(dd.strftime("%Y-%m-%d"), 24), "hour": np.tile(np.arange(24), len(dd))})
    for c in cols:
        df[c] = series(c, days).ravel()
    os.makedirs(folder, exist_ok=True)
    df.to_csv(os.path.join(folder, fname), index=False, float_format="%.17g")


def save_npz(folder, fname, **arrs):
    os.makedirs(folder, exist_ok=True)
    np.savez_compressed(os.path.join(folder, fname), **arrs)


# =============================================================================
# 2. Code blocks shared by the notebooks (only the blocks a chart needs are put in its notebook)
# =============================================================================
SETUP = r'''import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

# course chart style: transparent background, no grid, legend at the bottom outside the axes
plt.rcParams.update({
    "figure.facecolor": "none", "axes.facecolor": "none", "savefig.transparent": True,
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#222222", "axes.labelcolor": "#222222", "xtick.color": "#222222", "ytick.color": "#222222",
    "text.color": "#222222", "font.size": 11, "axes.titlesize": 11.5, "axes.labelsize": 11,
    "legend.fontsize": 10.5, "legend.frameon": False, "lines.linewidth": 1.4, "font.family": "DejaVu Sans"})
PAL = {"RO": "#2a78d6", "DE_LU": "#eb6834", "HU": "#1baf7a", "BG": "#eda100",
       "c5": "#e87ba4", "c6": "#008300", "c7": "#6250d6", "c8": "#e34948"}   # fixed colour per entity


def legend_bottom(fig, handles=None, labels=None, ncol=4, y=0.0):
    """Legend centred under the axes, outside the plotting area."""
    if handles is None:
        handles, labels = [], []
        for ax in fig.axes:
            for hh, ll in zip(*ax.get_legend_handles_labels()):
                if ll not in labels:
                    handles.append(hh)
                    labels.append(ll)
    if handles:
        fig.legend(handles, labels, loc="lower center", ncol=ncol, bbox_to_anchor=(0.5, y),
                   frameon=False, handlelength=2.0, columnspacing=1.2)'''

CUTOFF = r'''TZ = "Europe/Brussels"
PD = pd.read_csv(DATA + "power_da_prices_daily_cet.csv", parse_dates=["date_cet"]).set_index("date_cet")
_hydro = pd.read_csv(DATA + "generation_ro_mw_daily_cet.csv", usecols=["date_cet", "hydro_run_of_river"],
                     parse_dates=["date_cet"]).set_index("date_cet")["hydro_run_of_river"]
# cut-off = last complete month covered by the prices and the Romanian generation data
_raw_last = min(PD["RO"].dropna().index.max(), _hydro.dropna().index.max())
END = pd.Timestamp(((_raw_last + pd.Timedelta(days=1)).to_period("M").to_timestamp() - pd.Timedelta(days=1)).date())
START = pd.Timestamp("2022-01-01")
N_TEST, N_BURN = 365, 182                                  # test year; burn-in (its forecasts only feed QRA, CP, HS)
TEST0 = END - pd.Timedelta(days=N_TEST - 1)
FC0 = TEST0 - pd.Timedelta(days=N_BURN)
FDAYS = pd.date_range(FC0, END, freq="D")                  # burn-in + test days
TDAYS = pd.date_range(TEST0, END, freq="D")                # test days
print("cut-off:", END.date(), "| test year:", TEST0.date(), "to", END.date())'''


def panel(lr=True, cols_price=("RO",)):
    """Day x 24-hour panels (CET delivery day, Assignment 1 DST convention) of the price, and of load and wind+solar."""
    c = fsrc("day_matrix") + "\n\n\n"
    c += ('HP = pd.read_csv(DATA + "power_da_prices_hourly_utc.csv", index_col=0, usecols=["timestamp_utc", '
          + ", ".join(f'"{z}"' for z in cols_price) + "])\n")
    c += 'PM, DST = day_matrix(HP["RO"].dropna())\nCAL = pd.date_range(START, END, freq="D")\nPM, DST = PM.reindex(CAL), DST.reindex(CAL)\n'
    if lr:
        c += ('GH = pd.read_csv(DATA + "generation_ro_mw_hourly_utc.csv", index_col=0, usecols=["timestamp_utc", "load", "wind_onshore", "solar"])\n'
              'LM, _ = day_matrix(GH["load"].dropna())\nRM, _ = day_matrix((GH["wind_onshore"] + GH["solar"]).dropna())\n'
              "LM, RM = LM.reindex(CAL), RM.reindex(CAL)\n"
              'assert not PM.isna().any().any() and not LM.isna().any().any() and not RM.isna().any().any(), "panel has gaps"\n'
              "L_, R_ = LM.values.astype(float), RM.values.astype(float)\n")
    else:
        c += 'assert not PM.isna().any().any(), "panel has gaps"\n'
    c += ("P_ = PM.values.astype(float)\nDOW = CAL.dayofweek.values\nIDX = {t: i for i, t in enumerate(CAL)}\n"
          "TI_ROWS = np.array([IDX[t] for t in TDAYS])              # panel rows of the test days\n"
          "A = P_[TI_ROWS]                                          # actual prices of the test year, days x 24\n"
          "# naive benchmark: same hour of d-7 on Monday, Saturday, Sunday, of d-1 otherwise\n"
          "NAIVE = np.array([P_[i - 7] if DOW[i] in (0, 5, 6) else P_[i - 1] for i in TI_ROWS])\n"
          'print("panel:", CAL[0].date(), "to", CAL[-1].date(), len(CAL), "days x 24 hours")')
    return c


ARX_FUNCS = "from scipy import stats\n\n\n" + fsrc("shift_rows", "mad_scale", "arx_day")
ARX_RUN = ('ARX_W = (56, 84, 112, 714, 721, 728)                     # calibration windows (days)\n'
           "# one forecast per test day and window, re-estimated every day (a few seconds)\n"
           "ARX = {T: np.array([arx_day(P_, L_, R_, None, i, T)[0] for i in TI_ROWS]) for T in ARX_W}\n"
           "AW_ARX = np.mean([ARX[T] for T in ARX_W], 0)            # average across windows\n"
           'print("ARX ready")')


def saved_loader(chart):
    return (f'QL = REPO + "Quantlets/L2/EMQA_L2_{chart}/"          # saved results of this Quantlet\n\n\n'
            "def load_npz(path):\n"
            '    if path.startswith("http"):\n'
            "        import io\n        import urllib.request\n"
            "        return np.load(io.BytesIO(urllib.request.urlopen(path).read()))\n"
            "    return np.load(path)\n\n\n"
            "def load_csv(name, days):\n"
            '    S = pd.read_csv(QL + name, parse_dates=["date"], float_precision="round_trip")\n'
            '    assert (pd.DatetimeIndex(S["date"].drop_duplicates()) == days).all()\n'
            "    return S")


def forecast_block(chart, lear=True, days="test", nz=False, ml=False, qra=False, helpers=False):
    """Cell with RUN_ALL = False (load the saved forecasts) and the full recomputation code under `if RUN_ALL:`."""
    rows = "TI_ROWS" if days == "test" else "F_ROWS"
    mins = []
    if lear:
        mins.append("LEAR(728) roughly 15 min" if nz else "LEAR roughly 45 min" if days == "test" else "LEAR roughly 70 min")
    if ml:
        mins.append("GBM and MLP roughly 10 min")
    if qra:
        mins.append("QRA roughly 10 min")
    c = ("RUN_ALL = False   # True: recompute the forecasts from the data (" + ", ".join(mins) +
         " on one core; joblib uses all cores)\n\n")
    c += saved_loader(chart) + "\n\n\n"
    if days != "test":
        c += "F_ROWS = np.array([IDX[t] for t in FDAYS])              # panel rows of the burn-in + test days\n"
    if helpers:                                                    # notebooks without the ARX code need these two
        c += "from scipy import stats\n\n\n" + fsrc("shift_rows", "mad_scale") + "\n\n\n"
    if lear:
        c += ("PLAGS, XLAGS = (1, 2, 3, 7), (2, 3, 7)                   # price lags; lags of load and wind+solar (days)\n"
              "LEAR_W = (364, 546, 728)\n\n\n" + fsrc("lear_design", "lear_day") + "\n\n\n")
    if ml:
        c += ("SEED = 20261105\n"
              "GBM_NAMES = " + re.search(r"GBM_NAMES = (\[.*?\])", SRC, re.S).group(1) + "\n\n\n" +
              fsrc("gbm_rows", "gbm_month", "mlp_design", "mlp_month", "month_blocks") + "\n\n\n")
    if qra:
        c += ("import statsmodels.api as sm\nfrom statsmodels.regression.quantile_regression import QuantReg\n"
              "TAUS = np.arange(1, 100) / 100                           # 99 quantile levels\n"
              "W_QRA = 182                                              # QRA calibration: the previous 182 forecast days\n"
              "WEEK0 = list(range(N_BURN, len(FDAYS), 7))               # QRA refitted weekly\n\n\n" + fsrc("qra_hour") + "\n\n\n")
    c += "if RUN_ALL:\n    from joblib import Parallel, delayed\n"
    if lear:
        if nz:
            c += (f"    _r = Parallel(n_jobs=-1)(delayed(lear_day)(P_, L_, R_, i, 728) for i in {rows})\n"
                  "    LEAR_NZ = np.array([r[1] for r in _r])              # days x 24 hours x 247 regressors: kept or not\n")
        else:
            c += (f"    _r = Parallel(n_jobs=-1)(delayed(lear_day)(P_, L_, R_, i, T) for T in LEAR_W for i in {rows})\n"
                  f"    _n = len({rows})\n"
                  "    LEAR = {T: np.array([r[0] for r in _r[k * _n:(k + 1) * _n]]) for k, T in enumerate(LEAR_W)}\n")
    if ml:
        c += ("    # daily fundamentals, value usable for day d = last observation on or before d-2 (past only)\n"
              '    G = pd.read_csv(DATA + "generation_ro_mw_daily_cet.csv", parse_dates=["date_cet"]).set_index("date_cet")\n'
              '    CB = pd.read_csv(DATA + "crossborder_ro_mw_daily_cet.csv", parse_dates=["date_cet"]).set_index("date_cet")\n'
              '    EUA = pd.read_csv(DATA + "eua_daily.csv", parse_dates=["date"]).set_index("date")["eua_etc_co2l_eur_per_unit"]\n'
              '    CAL_EX = pd.date_range(START - pd.Timedelta(days=30), END, freq="D")\n'
              '    FUND_RAW = pd.DataFrame({"hydro": (G["hydro_run_of_river"] + G["hydro_water_reservoir"]).reindex(CAL_EX),\n'
              '                             "nuclear": G["nuclear"].reindex(CAL_EX), "netimp": CB["sum"].reindex(CAL_EX),\n'
              '                             "eua": EUA.reindex(CAL_EX)})\n'
              "    F_ = FUND_RAW.ffill().shift(2).reindex(CAL).values.astype(float)\n"
              "    MB = month_blocks(TDAYS)                                # monthly refits on an expanding window\n"
              "    GBM = np.vstack([g[0] for g in Parallel(n_jobs=-1)(delayed(gbm_month)(P_, L_, R_, F_, a, b) for a, b in MB)])\n"
              "    MLP = np.vstack([m[0] for m in Parallel(n_jobs=-1)(delayed(mlp_month)(P_, L_, R_, F_, a, b) for a, b in MB)])\n")
    if qra:
        c += ("    # QRA regresses the actual price on the AW-ARX and AW-LEAR forecasts of the previous 182 days\n"
              "    FA = np.mean([np.array([arx_day(P_, L_, R_, None, i, T)[0] for i in F_ROWS]) for T in ARX_W], 0)\n"
              "    FL_ = np.mean([LEAR[T] for T in LEAR_W], 0)\n"
              "    ACT_F = P_[F_ROWS]\n"
              "    QRA = np.stack(Parallel(n_jobs=-1)(delayed(qra_hour)(h) for h in range(24)), 1)\n"
              "    QRA = np.sort(QRA[N_BURN:], axis=2)                     # test year; rearranged: no quantile crossing\n")
    c += "else:\n"
    return c


# =============================================================================
# 3. One Quantlet per chart
# =============================================================================
CHARTS = {}


def chart(name):
    def deco(f):
        CHARTS[name] = f
        return f
    return deco


def period(name):
    return NUM["charts"][name]["period_en"].replace("\\%", "%")


def source(name):
    return NUM["charts"][name]["source_en"]


def checks_cell(checks):
    """Print every number of the slide; the make script compares them with L2_numbers.json."""
    lines = ['print("Numbers on the slide")']
    for lab, expr, key, fmt in checks:
        lines.append(f"print(f'  {lab}: {{{expr}:{fmt}}}')")
    return "\n".join(lines)


def new(name, desc, keywords, datafile, title):
    return Quantlet(k=2, chart=name, description=desc + f" Data: {period(name)}. Source: {source(name)}.",
                    keywords=keywords, datafile=datafile, title=title)


SAVE = "fig.tight_layout(rect=(0, {b}, 1, 1))\nplt.savefig('{n}.png', dpi=150, bbox_inches='tight', transparent=True)\nplt.show()"


def save(n, b):
    return SAVE.format(n=n, b=b)


@chart("split_timeline")
def q_split_timeline():
    n = "split_timeline"
    q = new(n, "Chronological design of the forecasting study: the daily base price of Romania (OPCOM day-ahead market), "
               "with the 728-day calibration window of the first forecast, the 182-day burn-in and the 365-day test year. "
               "Models are re-estimated every day on the window ending the day before; data are never shuffled.",
            "electricity price forecasting, day-ahead market, Romania, OPCOM, backtest, calibration window, burn-in, test period",
            "Hourly day-ahead prices of Romania (power_da_prices_hourly_utc.csv); daily prices and Romanian generation "
            "(only to fix the cut-off, the last complete month)",
            "Calibration, burn-in, test: time runs one way, data are never shuffled")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF)
    q.md("## Price panel: one row per CET delivery day, 24 hourly columns\n\nAfter 1 October 2025 each hour is the mean of its four "
         "quarter-hours; on DST days the missing spring hour is the mean of its neighbours and the doubled autumn hour is averaged.")
    q.code(panel(lr=False))
    q.md("## The chart")
    q.code("import matplotlib.dates as mdates\n\n"
           "DAILY = pd.Series(PM.mean(1).values, index=CAL)          # daily base price = mean of the 24 hours\n"
           "fig, ax = plt.subplots(figsize=(6.4, 2.1))\n"
           "c0 = FC0 - pd.Timedelta(days=728)\n"
           'ax.axvspan(c0, FC0 - pd.Timedelta(days=1), color=PAL["HU"], alpha=0.12, lw=0, label="calibration window, 728 days (first forecast)")\n'
           'ax.axvspan(FC0, TEST0 - pd.Timedelta(days=1), color=PAL["BG"], alpha=0.25, lw=0, label="burn-in, 182 days")\n'
           'ax.axvspan(TEST0, END, color=PAL["DE_LU"], alpha=0.18, lw=0, label="test, 365 days")\n'
           'ax.plot(DAILY.index, DAILY.values, color=PAL["RO"], lw=0.8, label="Romania, daily base price")\n'
           'ax.set_ylabel("EUR/MWh")\nax.set_xlim(CAL[0], END)\n'
           'ax.xaxis.set_major_locator(mdates.YearLocator())\nax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))\n'
           "legend_bottom(fig, ncol=2)\n" + save(n, 0.24))
    ck = [("first day of the data", "str(CAL[0].date())", "data.start", "s"),
          ("days in the panel", "len(CAL)", "data.n_days", "d"),
          ("first burn-in day", "str(FC0.date())", "design.burn_start", "s"),
          ("first test day", "str(TEST0.date())", "design.test_start", "s"),
          ("last test day", "str(END.date())", "design.test_end", "s"),
          ("test days", "len(TDAYS)", "design.n_test", "d")]
    q.code(checks_cell(ck))
    return q, ck


@chart("horizon_naive")
def q_horizon_naive():
    n = "horizon_naive"
    q = new(n, "Mean absolute error (MAE) of the simplest forecast of the Romanian day-ahead price, the price of the same hour "
               "k days earlier, for k = 1 to 14 on the test year: older information gives larger errors, except at the weekly "
               "lags k = 7 and 14 (same weekday).",
            "electricity price forecasting, naive forecast, forecast horizon, weekly seasonality, MAE, Romania, OPCOM",
            "Hourly day-ahead prices of Romania (power_da_prices_hourly_utc.csv); daily prices and Romanian generation (cut-off only)",
            "Older information, larger error, except at the weekly lag")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Price panel").code(panel(lr=False))
    q.md(r"## MAE of the forecast $\hat P_{d,h}=P_{d-k,h}$ on the test year")
    q.code("hz = {k: float(np.mean(np.abs(A - P_[TI_ROWS - k]))) for k in range(1, 15)}\n"
           'for k, v in hz.items():\n    print(f"k = {k:2d}: MAE {v:.2f} EUR/MWh")')
    q.md("## The chart")
    q.code("from matplotlib.patches import Patch\n\n"
           "fig, ax = plt.subplots(figsize=(6.4, 1.9))\nks = list(range(1, 15))\n"
           'ax.bar(ks, [hz[k] for k in ks], color=[PAL["DE_LU"] if k % 7 == 0 else PAL["RO"] for k in ks], width=0.7)\n'
           'hnd = [Patch(color=PAL["RO"], label="same hour, k days earlier"), Patch(color=PAL["DE_LU"], label="k = 7, 14 (same weekday)")]\n'
           'ax.set_xticks(ks)\nax.set_xlabel("age of the information k (days)")\nax.set_ylabel("MAE\\n(EUR/MWh)", fontsize=8)\n'
           "legend_bottom(fig, handles=hnd, labels=[h.get_label() for h in hnd], ncol=2)\n" + save(n, 0.2))
    ck = [(f"MAE k = {k}", f"hz[{k}]", f"horizon.{k}", ".2f") for k in range(1, 15)]
    q.code(checks_cell(ck))
    return q, ck


LEAR_MD = ("## Forecasts\n\nLEAR (LASSO-estimated autoregression, 247 candidate regressors, $\\lambda$ by AIC) is re-estimated every day "
           "for each hour and for the windows 364, 546 and 728 days; AW-LEAR is the average across the three windows. "
           "This takes about 2.5 s per day and window, so the forecasts computed by `lectures/L2/analysis_L2.py` are loaded from "
           "the file saved next to this notebook. Set `RUN_ALL = True` to recompute them with the code below.")
ML_MD = (" GBM (gradient boosting) and MLP (a 24-output neural network, 4 seeds) are refitted every month on an expanding "
         "window that ends before the month.")
ARX_MD = ("The expert ARX model (one OLS regression per hour, Assignment 1 specification) is cheap and is recomputed here for "
          "the six calibration windows 56, 84, 112, 714, 721 and 728 days; AW-ARX is their average.")


@chart("mape_fail")
def q_mape_fail():
    n = "mape_fail"
    save_csv(Quantlet(2, n, "", "", "").folder, "forecasts_test.csv", ["lear364", "lear546", "lear728"])
    q = new(n, "Absolute percentage error of the AW-LEAR forecast of the Romanian day-ahead price, hour by hour, against the "
               "actual price on the test year (log scale): near zero and negative prices the percentage error explodes, so the "
               "mean absolute percentage error (MAPE) is dominated by a few hours with |price| < 5 EUR/MWh.",
            "MAPE, percentage error, negative prices, forecast evaluation, LEAR, LASSO, electricity price forecasting, Romania",
            "Hourly day-ahead prices of Romania; hourly load, wind and solar of Romania (generation_ro_mw_hourly_utc.csv); "
            "saved LEAR forecasts of the test year (forecasts_test.csv, from lectures/L2/analysis_L2.py)",
            "Why percentage errors fail near zero and negative prices")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md(LEAR_MD)
    q.code(forecast_block(n, helpers=True) +
           '    S = load_csv("forecasts_test.csv", TDAYS)\n'
           '    LEAR = {T: S[f"lear{T}"].values.reshape(-1, 24) for T in LEAR_W}\n'
           "AW_LEAR = np.mean([LEAR[T] for T in LEAR_W], 0)\n"
           'print("AW-LEAR MAE on the test year: %.2f EUR/MWh" % np.mean(np.abs(A - AW_LEAR)))')
    q.md("## Absolute percentage errors")
    q.code("_ape = np.abs(A - AW_LEAR) / np.abs(A)\n_ape[~np.isfinite(_ape)] = np.nan      # price exactly 0: undefined\n"
           "small = np.abs(A) < 5\n"
           "MAPE = np.nanmean(_ape) * 100\nMAPE_EXCL5 = np.nanmean(_ape[~small]) * 100\n"
           "SHARE_SMALL = np.nansum(_ape[small]) / np.nansum(_ape) * 100\nN_SMALL = int(small.sum())")
    q.md("## The chart")
    q.code("fig, ax = plt.subplots(figsize=(6.4, 2.1))\n"
           "x_, y_ = A.ravel(), (_ape.ravel() * 100)\nok = np.isfinite(y_) & (y_ > 0)\n"
           'ax.axvspan(-5, 5, color=PAL["c8"], alpha=0.15, lw=0, label="|price| < 5 EUR/MWh")\n'
           'ax.scatter(np.clip(x_[ok], -120, 620), y_[ok], s=1.5, color=PAL["RO"], alpha=0.35, lw=0, label="one hour of the test year, AW-LEAR")\n'
           'ax.axhline(100, color="#222222", lw=0.7, ls="--", label="error = 100% of the price")\n'
           'ax.set_yscale("log")\nax.set_yticks([1e-2, 1, 1e2, 1e4, 1e6])\nax.set_yticklabels(["0.01", "1", "100", "10$^4$", "10$^6$"])\n'
           'ax.set_xlabel("actual price, EUR/MWh")\nax.set_ylabel("absolute % error")\n'
           "legend_bottom(fig, ncol=3)\n" + save(n, 0.22))
    ck = [("MAPE of AW-LEAR, %", "MAPE", "mape.aw_lear", ".1f"),
          ("MAPE without |price| < 5, %", "MAPE_EXCL5", "mape.aw_lear_excl5", ".1f"),
          ("hours with |price| < 5 EUR/MWh", "N_SMALL", "mape.n_small", "d"),
          ("share of the MAPE from these hours, %", "SHARE_SMALL", "mape.share_from_small", ".1f")]
    q.code(checks_cell(ck))
    return q, ck


DMSRC = fsrc("nw_var", "dm")


@chart("dm_matrix")
def q_dm_matrix():
    n = "dm_matrix"
    save_csv(Quantlet(2, n, "", "", "").folder, "forecasts_test.csv", ["lear364", "lear546", "lear728", "gbm", "mlp"])
    q = new(n, "Chessboard of one-sided Diebold-Mariano (DM) tests between ten forecasts of the Romanian day-ahead price on the "
               "test year (naive, seasonal naive, ARX(728), AW-ARX, LEAR(728), AW-LEAR, GBM, MLP and two ensembles): each cell is "
               "the p-value of the hypothesis that the column model is not more accurate than the row model (multivariate DM "
               "on the daily mean absolute error, Newey-West variance with 7 lags).",
            "Diebold-Mariano test, forecast comparison, Newey-West, ARX, LEAR, gradient boosting, neural network, ensemble, "
            "electricity price forecasting, Romania",
            "Hourly day-ahead prices, load, wind and solar of Romania; saved LEAR, GBM and MLP forecasts of the test year "
            "(forecasts_test.csv, from lectures/L2/analysis_L2.py; the GBM and MLP also use daily hydro, nuclear, net imports "
            "and the EUA price)",
            "The DM chessboard: which model beats which on the Romanian test year")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md("## Expert ARX forecasts\n\n" + ARX_MD).code(ARX_FUNCS).code(ARX_RUN)
    q.md(LEAR_MD + ML_MD)
    q.code(forecast_block(n, ml=True) +
           '    S = load_csv("forecasts_test.csv", TDAYS)\n'
           '    LEAR = {T: S[f"lear{T}"].values.reshape(-1, 24) for T in LEAR_W}\n'
           '    GBM, MLP = S["gbm"].values.reshape(-1, 24), S["mlp"].values.reshape(-1, 24)\n'
           "M = {\"naive\": NAIVE, \"snaive\": P_[TI_ROWS - 7], \"arx728\": ARX[728], \"aw_arx\": AW_ARX, \"lear728\": LEAR[728],\n"
           "     \"aw_lear\": np.mean([LEAR[T] for T in LEAR_W], 0), \"gbm\": GBM, \"mlp\": MLP}\n"
           'M["ens_lm"] = 0.5 * (M["aw_lear"] + M["mlp"])\n'
           'M["ens_all"] = np.mean([M["aw_arx"], M["aw_lear"], M["gbm"], M["mlp"]], 0)\n'
           'for k, v in M.items():\n    print(f"{k:8s} MAE {np.mean(np.abs(A - v)):.2f} EUR/MWh")')
    q.md(r"## Diebold-Mariano tests: $\Delta_d$ = daily mean |error| of A minus that of B; small $p$ = B more accurate")
    q.code("from scipy import stats\n\n\n" + DMSRC + "\n\n\n"
           'DM_MODELS = ["naive", "snaive", "arx728", "aw_arx", "lear728", "aw_lear", "gbm", "mlp", "ens_lm", "ens_all"]\n'
           "E = {k: A - M[k] for k in DM_MODELS}\n"
           "DMP = np.full((len(DM_MODELS), len(DM_MODELS)), np.nan)\n"
           "for a_, ka in enumerate(DM_MODELS):\n    for b_, kb in enumerate(DM_MODELS):\n        if a_ != b_:\n"
           "            DMP[a_, b_] = dm(E[ka], E[kb])[1]\n"
           "N_SIG = int(sum(DMP[0, j] < 0.05 for j in range(1, len(DM_MODELS))))\n"
           'st1, p1 = dm(E["naive"], E["aw_lear"])\nst2, p2 = dm(E["aw_lear"], E["ens_all"])\nst3, p3 = dm(E["aw_arx"], E["aw_lear"])')
    q.md("## The chart")
    q.code("from matplotlib.colors import LinearSegmentedColormap\n\n"
           'LAB = {"naive": "Naive", "snaive": "Seasonal naive", "arx728": "ARX(728)", "aw_arx": "AW-ARX", "lear728": "LEAR(728)",\n'
           '       "aw_lear": "AW-LEAR", "gbm": "GBM", "mlp": "MLP", "ens_lm": "Ens. LEAR+MLP", "ens_all": "Ens. 4 models"}\n'
           'cmap = LinearSegmentedColormap.from_list("dm", ["#0b6e2e", "#7fc97f", "#ffe08a", "#f4a259", "#d7301f", "#5a0000"])\n'
           "fig, ax = plt.subplots(figsize=(6.4, 2.7))\n"
           "Z = np.where(np.isnan(DMP), np.nan, np.minimum(DMP, 0.10))\n"
           'im = ax.imshow(np.ma.masked_invalid(Z), cmap=cmap, vmin=0, vmax=0.10, aspect="auto")\n'
           'ax.set_xticks(range(len(DM_MODELS)))\nax.set_xticklabels([LAB[k] for k in DM_MODELS], rotation=40, ha="right", fontsize=9)\n'
           "ax.set_yticks(range(len(DM_MODELS)))\nax.set_yticklabels([LAB[k] for k in DM_MODELS], fontsize=9)\n"
           'ax.set_xlabel("is the column model more accurate than the row model?", fontsize=9.5)\n'
           'for a_ in range(len(DM_MODELS)):\n    ax.add_patch(plt.Rectangle((a_ - 0.5, a_ - 0.5), 1, 1, color="#ffffff"))\n'
           'cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)\ncb.set_label("p-value, capped at 0.10", fontsize=9)\n'
           "ax.spines[:].set_visible(False)\n" + save(n, 0.0))
    ck = [("models beating the naive at 5%", "N_SIG", "dm.n_sig_vs_naive", "d"),
          ("other models", "len(DM_MODELS) - 1", "dm.n_others", "d"),
          ("test days", "len(TDAYS)", "dm.n_days", "d"),
          ("DM naive vs AW-LEAR", "st1", "dm.naive_lear.stat", ".2f"),
          ("p naive vs AW-LEAR", "p1", "dm.naive_lear.p", ".4f"),
          ("DM AW-ARX vs AW-LEAR", "st3", "dm.arx_lear.stat", ".2f"),
          ("p AW-ARX vs AW-LEAR", "p3", "dm.arx_lear.p", ".4f"),
          ("DM AW-LEAR vs Ens. 4 models", "st2", "dm.lear_ens.stat", ".2f"),
          ("p AW-LEAR vs Ens. 4 models", "p2", "dm.lear_ens.p", ".4f")]
    q.code(checks_cell(ck))
    return q, ck


@chart("arx_coef")
def q_arx_coef():
    n = "arx_coef"
    q = new(n, "Coefficients of the expert ARX(728) model of the Romanian day-ahead price (asinh scale), averaged over the 365 "
               "daily estimations of the test year, hour by hour: the weight of the same hour yesterday peaks at midday, night "
               "hours lean on the last hour of the previous day, and the two-day-old load and wind + solar stay close to zero.",
            "ARX, autoregression, expert model, hourly regression, coefficients, asinh transformation, electricity price, Romania",
            "Hourly day-ahead prices of Romania; hourly load, wind and solar generation of Romania (generation_ro_mw_hourly_utc.csv)",
            "The ARX coefficients change with the hour of the day")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md("## Expert ARX(728), re-estimated every day of the test year (one OLS regression per hour)").code(ARX_FUNCS)
    q.code("CO = np.array([arx_day(P_, L_, R_, None, i, 728)[1] for i in TI_ROWS])   # days x 24 hours x 12 coefficients\n"
           "coef_mean = CO.mean(0)\n"
           'CNAMES = ["const", "Y1", "Y2", "Y7", "Y1_23", "Ymin", "Ymax", "L", "R", "Mon", "Sat", "Sun"]\n'
           "# hour 23 has one regressor less (Y(d-1,23) would appear twice), so it is left out, as on the slide\n"
           'print(pd.DataFrame(coef_mean[:23], columns=CNAMES).round(3).to_string())')
    q.md("## The chart")
    q.code("fig, ax = plt.subplots(figsize=(6.4, 2.0))\nhh = np.arange(23)\n"
           'for j, c, lab, ls in [(1, PAL["RO"], "$Y_{d-1,h}$", "-"), (2, PAL["HU"], "$Y_{d-2,h}$", "--"), (3, PAL["DE_LU"], "$Y_{d-7,h}$", "-."),\n'
           '                      (7, "#222222", "load $\\\\tilde L_{d,h}$", "-"), (8, PAL["BG"], "wind+solar $\\\\tilde R_{d,h}$", "-")]:\n'
           '    ax.plot(hh, coef_mean[:23, j], color=c, ls=ls, marker="o", ms=3, label=lab)\n'
           'ax.axhline(0, color="#222222", lw=0.5)\nax.set_xticks(range(0, 23, 2))\nax.set_xlabel("hour h (CET)")\n'
           'ax.set_ylabel("mean coefficient")\nlegend_bottom(fig, ncol=5)\n' + save(n, 0.2))
    ck = [("hour of the largest Y(d-1,h) coefficient", "int(np.argmax(coef_mean[:23, 1]))", "arxcoef.Y1.argmax", "d"),
          ("largest Y(d-1,h) coefficient", "coef_mean[:23, 1].max()", "arxcoef.Y1.max", ".3f"),
          ("hour of the smallest Y(d-1,h) coefficient", "int(np.argmin(coef_mean[:23, 1]))", "arxcoef.Y1.argmin", "d"),
          ("smallest Y(d-1,h) coefficient", "coef_mean[:23, 1].min()", "arxcoef.Y1.min", ".3f"),
          ("largest Y(d-1,23) coefficient", "coef_mean[:23, 4].max()", "arxcoef.Y1_23.max", ".3f")]
    q.code(checks_cell(ck))
    return q, ck


@chart("per_hour_single")
def q_per_hour_single():
    n = "per_hour_single"
    q = new(n, "Hourly mean absolute error (MAE) on the test year of the expert ARX(728) model of the Romanian day-ahead price "
               "estimated as one regression per hour, against one pooled regression for all hours (hour intercepts, common "
               "slopes) and the naive benchmark.",
            "ARX, per-hour model, pooled model, multivariate, univariate, MAE by hour, electricity price forecasting, Romania",
            "Hourly day-ahead prices of Romania; hourly load, wind and solar generation of Romania (generation_ro_mw_hourly_utc.csv)",
            "One model per hour beats one model for all hours")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md("## Expert ARX(728): one model per hour, and one pooled model for all hours").code(ARX_FUNCS)
    q.code("ARX728 = np.array([arx_day(P_, L_, R_, None, i, 728)[0] for i in TI_ROWS])\n"
           'ARX728_SINGLE = np.array([arx_day(P_, L_, R_, None, i, 728, "single")[0] for i in TI_ROWS])\n'
           "BYHOUR = {k: np.mean(np.abs(A - v), 0) for k, v in [(\"naive\", NAIVE), (\"single\", ARX728_SINGLE), (\"arx728\", ARX728)]}\n"
           "SINGLE_WORSE = int((BYHOUR[\"single\"] > BYHOUR[\"arx728\"]).sum())")
    q.md("## The chart")
    q.code("fig, ax = plt.subplots(figsize=(6.4, 1.9))\nh24 = np.arange(24)\n"
           'ax.plot(h24, BYHOUR["naive"], color="#9a9a9a", ls=":", marker="o", ms=3, label="Naive")\n'
           'ax.plot(h24, BYHOUR["single"], color=PAL["DE_LU"], marker="s", ms=3, label="ARX(728), one model for all hours")\n'
           'ax.plot(h24, BYHOUR["arx728"], color=PAL["HU"], marker="o", ms=3, label="ARX(728), one model per hour")\n'
           'ax.set_xticks(range(0, 24, 2))\nax.set_xlabel("hour h (CET)")\nax.set_ylabel("MAE, EUR/MWh")\n'
           "legend_bottom(fig, ncol=3)\n" + save(n, 0.2))
    ck = [("MAE, one model per hour", "np.mean(np.abs(A - ARX728))", "acc.arx728.mae", ".2f"),
          ("MAE, one pooled model", "np.mean(np.abs(A - ARX728_SINGLE))", "acc.arx728_single.mae", ".2f"),
          ("hours where the pooled model is worse", "SINGLE_WORSE", "byhour.single_worse_h", "d")]
    q.code(checks_cell(ck))
    return q, ck


MFMT = ('import matplotlib.dates as mdates\nfrom matplotlib.ticker import FuncFormatter\n'
        'MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]\n\n\n'
        "def mfmt(ax, step=1):\n"
        "    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=step))\n"
        "    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: MON[mdates.num2date(v).month - 1] +\n"
        '                                               (f"\\n{mdates.num2date(v).year}" if mdates.num2date(v).month == 1 else "")))\n\n\n'
        'TM = TDAYS.to_period("M")\nMONTHS_T = sorted(set(TM))\nxm = [pd.Timestamp(str(mm)) for mm in MONTHS_T]\n\n\n'
        "def bymonth(F):\n    return np.array([np.mean(np.abs(A[TM == mm] - F[TM == mm])) for mm in MONTHS_T])\n")


@chart("vst")
def q_vst():
    n = "vst"
    q = new(n, "Variance-stabilising transformation of electricity prices: left, the asinh transformation of the price, "
               "standardised with the median and the median absolute deviation of the last 735 days, against a plain z-score; "
               "right, monthly mean absolute error of the expert ARX(728) model of the Romanian day-ahead price estimated on raw "
               "and on asinh-transformed prices.",
            "variance-stabilising transformation, asinh, area hyperbolic sine, median absolute deviation, ARX, price spikes, "
            "negative prices, electricity price forecasting, Romania",
            "Hourly day-ahead prices of Romania; hourly load, wind and solar generation of Romania (generation_ro_mw_hourly_utc.csv)",
            "The asinh transformation tames spikes and negative prices")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md("## Expert ARX(728) on raw and on asinh-transformed prices").code(ARX_FUNCS)
    q.code("ARX728 = np.array([arx_day(P_, L_, R_, None, i, 728)[0] for i in TI_ROWS])\n"
           'ARX728_RAW = np.array([arx_day(P_, L_, R_, None, i, 728, "raw")[0] for i in TI_ROWS])\n'
           "mae = lambda F: np.mean(np.abs(A - F))\nrmse = lambda F: np.sqrt(np.mean((A - F) ** 2))\n"
           "# median m and scale s (1.4826 x MAD) of the last calibration window, for the left panel\n"
           "m_last, s_last = mad_scale(P_[IDX[END] - 735:IDX[END]])\n"
           'print(f"m = {m_last:.2f}, s = {s_last:.2f} EUR/MWh")')
    q.md("## The chart").code(MFMT)
    q.code('fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0), gridspec_kw={"width_ratios": [1, 1.25]})\n'
           "pg = np.linspace(-150, 650, 400)\n"
           'axs[0].plot(pg, (pg - m_last) / s_last, color="#9a9a9a", ls="--", label="z-score (no transform)")\n'
           'axs[0].plot(pg, np.arcsinh((pg - m_last) / s_last), color=PAL["RO"], label="asinh")\n'
           'axs[0].set_xlabel("price, EUR/MWh")\naxs[0].set_ylabel("model scale")\n'
           'axs[1].plot(xm, bymonth(ARX728_RAW), color="#9a9a9a", ls="--", marker="s", ms=3, label="ARX(728) on raw prices")\n'
           'axs[1].plot(xm, bymonth(ARX728), color=PAL["RO"], marker="o", ms=3, label="ARX(728) on asinh prices")\n'
           'axs[1].set_ylabel("MAE, EUR/MWh")\nmfmt(axs[1], 2)\nlegend_bottom(fig, ncol=2)\n' + save(n, 0.26))
    ck = [("MAE, raw prices", "mae(ARX728_RAW)", "acc.arx728_raw.mae", ".2f"),
          ("MAE, asinh", "mae(ARX728)", "acc.arx728.mae", ".2f"),
          ("RMSE, raw prices", "rmse(ARX728_RAW)", "acc.arx728_raw.rmse", ".2f"),
          ("RMSE, asinh", "rmse(ARX728)", "acc.arx728.rmse", ".2f")]
    q.code(checks_cell(ck))
    return q, ck


@chart("lear_sel")
def q_lear_sel():
    n = "lear_sel"
    nz = FC["lear_nz"][POS_T]
    save_npz(Quantlet(2, n, "", "", "").folder, "lear_nz_test.npz", nz=nz)
    q = new(n, "Share of the 247 candidate regressors kept by the LASSO in the LEAR(728) model of the Romanian day-ahead price, "
               "by group of regressors (prices of d-1, d-2, d-3 and d-7, load, wind + solar, day of week) and by hour, over the "
               "365 daily estimations of the test year.",
            "LEAR, LASSO, variable selection, sparsity, AIC, autoregression, electricity price forecasting, Romania",
            "Hourly day-ahead prices of Romania; hourly load, wind and solar generation of Romania (generation_ro_mw_hourly_utc.csv); "
            "saved LASSO selection of the test year (lear_nz_test.npz, from lectures/L2/analysis_L2.py)",
            "What LEAR keeps: yesterday's same hour and the weekday, rarely the lagged fundamentals")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md("## LASSO selection\n\nLEAR(728) is re-estimated every day of the test year for each hour; the LASSO keeps a "
         "regressor when its coefficient is not zero. The 247 columns are, in order: price of d-1, d-2, d-3, d-7 (24 hours "
         "each), load and wind + solar of d-2, d-3, d-7 (24 hours each), 7 day-of-week dummies. The selection computed by "
         "`lectures/L2/analysis_L2.py` is loaded from the file saved next to this notebook (`RUN_ALL = True` recomputes it, "
         "about 15 min on one core).")
    q.code(forecast_block(n, nz=True, helpers=True) +
           '    LEAR_NZ = load_npz(QL + "lear_nz_test.npz")["nz"]\n'
           'print("regressors kept per hour and day: mean %.1f of %d" % (LEAR_NZ.sum(2).mean(), LEAR_NZ.shape[2]))')
    q.code('GROUPS = {"p1_same": None, "p1_other": None, "p2": (24, 48), "p3": (48, 72), "p7": (72, 96), "load": (96, 168),\n'
           '          "res": (168, 240), "dow": (240, 247)}\n'
           "SEL = np.zeros((len(GROUPS), 24))\n"
           "for gi, (g, rg) in enumerate(GROUPS.items()):\n    for h in range(24):\n"
           '        if g == "p1_same":\n            SEL[gi, h] = LEAR_NZ[:, h, h].mean()\n'
           '        elif g == "p1_other":\n            SEL[gi, h] = LEAR_NZ[:, h, [j for j in range(24) if j != h]].mean()\n'
           "        else:\n            SEL[gi, h] = LEAR_NZ[:, h, rg[0]:rg[1]].mean()")
    q.md("## The chart")
    q.code('GLAB = ["P(d-1), same hour", "P(d-1), other hours", "P(d-2)", "P(d-3)", "P(d-7)", "Load (d-2,d-3,d-7)",\n'
           '        "Wind+solar (d-2,d-3,d-7)", "Day of week"]\n'
           'fig, ax = plt.subplots(figsize=(6.4, 2.3))\nim = ax.imshow(SEL * 100, aspect="auto", cmap="Blues", vmin=0, vmax=100)\n'
           'ax.set_yticks(range(len(GLAB)))\nax.set_yticklabels(GLAB, fontsize=8.5)\nax.set_xticks(range(0, 24, 2))\n'
           'ax.set_xlabel("hour h (CET)")\ncb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)\n'
           'cb.set_label("% of regressors kept", fontsize=9)\nax.spines[:].set_visible(False)\n' + save(n, 0.02))
    ck = [("kept, P(d-1) same hour, %", "SEL[0].mean() * 100", "lear.p1_same", ".1f"),
          ("kept, day of week, %", "SEL[7].mean() * 100", "lear.dow", ".1f"),
          ("kept, load, %", "SEL[5].mean() * 100", "lear.load", ".1f"),
          ("kept, wind + solar, %", "SEL[6].mean() * 100", "lear.res", ".1f"),
          ("kept, P(d-7), %", "SEL[4].mean() * 100", "lear.p7", ".1f"),
          ("regressors kept, mean per hour and day", "LEAR_NZ.sum(2).mean()", "lear.nnz_mean", ".1f")]
    q.code(checks_cell(ck))
    return q, ck


@chart("windows")
def q_windows():
    n = "windows"
    save_csv(Quantlet(2, n, "", "", "").folder, "forecasts_test.csv", ["lear364", "lear546", "lear728"])
    q = new(n, "Mean absolute error on the test year of the expert ARX model of the Romanian day-ahead price for six calibration "
               "windows (56 to 728 days) and of LEAR for three windows (364, 546, 728 days), against the average of the forecasts "
               "across windows (AW) and the naive benchmark.",
            "calibration window, averaging across windows, forecast combination, ARX, LEAR, MAE, electricity price forecasting, Romania",
            "Hourly day-ahead prices of Romania; hourly load, wind and solar generation of Romania; saved LEAR forecasts of the "
            "test year (forecasts_test.csv, from lectures/L2/analysis_L2.py)",
            "Averaging across windows beats the best single window")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md("## Expert ARX forecasts\n\n" + ARX_MD).code(ARX_FUNCS).code(ARX_RUN)
    q.md(LEAR_MD)
    q.code(forecast_block(n) +
           '    S = load_csv("forecasts_test.csv", TDAYS)\n'
           '    LEAR = {T: S[f"lear{T}"].values.reshape(-1, 24) for T in LEAR_W}\n'
           "AW_LEAR = np.mean([LEAR[T] for T in LEAR_W], 0)\n"
           "mae = lambda F: np.mean(np.abs(A - F))\n"
           'MAE = {**{f"arx{T}": mae(ARX[T]) for T in ARX_W}, "aw_arx": mae(AW_ARX),\n'
           '       **{f"lear{T}": mae(LEAR[T]) for T in LEAR_W}, "aw_lear": mae(AW_LEAR), "naive": mae(NAIVE)}\n'
           'for k, v in MAE.items():\n    print(f"{k:8s} MAE {v:.2f} EUR/MWh")')
    q.md("## The chart")
    q.code('fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0), sharey=True, gridspec_kw={"width_ratios": [7, 4]})\n'
           'ka = [f"arx{T}" for T in ARX_W] + ["aw_arx"]\n'
           'axs[0].bar(range(7), [MAE[k] for k in ka], color=[PAL["HU"]] * 6 + [PAL["DE_LU"]], width=0.7)\n'
           'axs[0].set_xticks(range(7))\naxs[0].set_xticklabels([str(T) for T in ARX_W] + ["AW"])\naxs[0].set_title("ARX", fontsize=10)\n'
           'kl = [f"lear{T}" for T in LEAR_W] + ["aw_lear"]\n'
           'axs[1].bar(range(4), [MAE[k] for k in kl], color=[PAL["RO"]] * 3 + [PAL["DE_LU"]], width=0.7)\n'
           'axs[1].set_xticks(range(4))\naxs[1].set_xticklabels([str(T) for T in LEAR_W] + ["AW"])\naxs[1].set_title("LEAR", fontsize=10)\n'
           'for ax in axs:\n    ax.axhline(MAE["naive"], color="#9a9a9a", ls=":", lw=1.2)\n'
           'axs[0].plot([], [], color="#9a9a9a", ls=":", label="naive benchmark")\n'
           'axs[0].bar([], [], color=PAL["DE_LU"], label="average across windows (AW)")\n'
           'axs[0].set_ylabel("MAE, EUR/MWh")\naxs[0].set_ylim(0, MAE["naive"] * 1.12)\n'
           'fig.text(0.5, 0.17, "calibration window T (days)", ha="center", fontsize=10)\n'
           "legend_bottom(fig, ncol=2)\n" + save(n, 0.22))
    ck = ([(f"MAE ARX({T})", f'MAE["arx{T}"]', f"acc.arx{T}.mae", ".2f") for T in (56, 84, 112, 714, 721, 728)] +
          [("MAE AW-ARX", 'MAE["aw_arx"]', "acc.aw_arx.mae", ".2f")] +
          [(f"MAE LEAR({T})", f'MAE["lear{T}"]', f"acc.lear{T}.mae", ".2f") for T in (364, 546, 728)] +
          [("MAE AW-LEAR", 'MAE["aw_lear"]', "acc.aw_lear.mae", ".2f"), ("MAE naive", 'MAE["naive"]', "acc.naive.mae", ".2f")])
    q.code(checks_cell(ck))
    return q, ck


ML_LOAD = ('    S = load_csv("forecasts_test.csv", TDAYS)\n'
           '    LEAR = {T: S[f"lear{T}"].values.reshape(-1, 24) for T in LEAR_W}\n'
           '    GBM, MLP = S["gbm"].values.reshape(-1, 24), S["mlp"].values.reshape(-1, 24)\n'
           "AW_LEAR = np.mean([LEAR[T] for T in LEAR_W], 0)\n"
           "ENS_ALL = np.mean([AW_ARX, AW_LEAR, GBM, MLP], 0)         # equal-weight ensemble of the four models\n"
           'for k, v in [("AW-ARX", AW_ARX), ("AW-LEAR", AW_LEAR), ("GBM", GBM), ("MLP", MLP), ("Ens. 4 models", ENS_ALL)]:\n'
           '    print(f"{k:14s} MAE {np.mean(np.abs(A - v)):.2f} EUR/MWh")')
ML_DATAFILE = ("Hourly day-ahead prices of Romania; hourly load, wind and solar generation of Romania; saved LEAR, GBM and MLP "
               "forecasts of the test year (forecasts_test.csv, from lectures/L2/analysis_L2.py; the GBM and MLP also use daily "
               "hydro, nuclear, net imports and the EUA price)")


def ml_quantlet(n, q):
    save_csv(q.folder, "forecasts_test.csv", ["lear364", "lear546", "lear728", "gbm", "mlp"])
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md("## Expert ARX forecasts\n\n" + ARX_MD).code(ARX_FUNCS).code(ARX_RUN)
    q.md(LEAR_MD + ML_MD).code(forecast_block(n, ml=True) + ML_LOAD)


@chart("ml_hour")
def q_ml_hour():
    n = "ml_hour"
    q = new(n, "Hourly mean absolute error on the test year of four forecasts of the Romanian day-ahead price: AW-LEAR, gradient "
               "boosting (GBM), a neural network (MLP) and the equal-weight ensemble of AW-ARX, AW-LEAR, GBM and MLP.",
            "machine learning, gradient boosting, neural network, ensemble, LEAR, MAE by hour, electricity price forecasting, Romania",
            ML_DATAFILE, "Hour by hour: machine learning helps inside the ensemble, not alone")
    ml_quantlet(n, q)
    q.code('BYHOUR = {k: np.mean(np.abs(A - v), 0) for k, v in [("aw_lear", AW_LEAR), ("gbm", GBM), ("mlp", MLP), ("ens_all", ENS_ALL)]}')
    q.md("## The chart")
    q.code('COL = {"aw_lear": PAL["RO"], "gbm": PAL["BG"], "mlp": PAL["c7"], "ens_all": PAL["DE_LU"]}\n'
           'LAB = {"aw_lear": "AW-LEAR", "gbm": "GBM", "mlp": "MLP", "ens_all": "Ens. 4 models"}\n'
           "fig, ax = plt.subplots(figsize=(6.4, 1.9))\nh24 = np.arange(24)\n"
           'for k, ls in [("aw_lear", "-"), ("gbm", "--"), ("mlp", "-."), ("ens_all", "-")]:\n'
           '    ax.plot(h24, BYHOUR[k], color=COL[k], ls=ls, marker="o", ms=3, lw=1.6 if k == "ens_all" else 1.2, label=LAB[k])\n'
           'ax.set_xticks(range(0, 24, 2))\nax.set_xlabel("hour h (CET)")\nax.set_ylabel("MAE, EUR/MWh")\n'
           "legend_bottom(fig, ncol=4)\n" + save(n, 0.2))
    ck = [("hours GBM beats AW-LEAR", 'int((BYHOUR["gbm"] < BYHOUR["aw_lear"]).sum())', "byhour.gbm_beats_lear_h", "d"),
          ("hours MLP beats AW-LEAR", 'int((BYHOUR["mlp"] < BYHOUR["aw_lear"]).sum())', "byhour.mlp_beats_lear_h", "d"),
          ("hours the ensemble beats AW-LEAR", 'int((BYHOUR["ens_all"] < BYHOUR["aw_lear"]).sum())', "byhour.ens_beats_lear_h", "d"),
          ("hardest hour for AW-LEAR (CET)", 'int(np.argmax(BYHOUR["aw_lear"]))', "byhour.lear_worst_h", "d"),
          ("AW-LEAR MAE in that hour", 'BYHOUR["aw_lear"].max()', "byhour.lear_worst", ".2f")]
    q.code(checks_cell(ck))
    return q, ck


WEEKS = ('# Mondays whose week ends inside the test year\nmons = [t for t in TDAYS if t.dayofweek == 0 and t + pd.Timedelta(days=6) <= END]\n'
         "TPOS = {t: k for k, t in enumerate(TDAYS)}                # row of a test day\n")


@chart("qra_week")
def q_qra_week():
    n = "qra_week"
    q = new(n, "One week of hourly probabilistic forecasts of the Romanian day-ahead price by quantile regression averaging (QRA) "
               "on the AW-ARX and AW-LEAR point forecasts: 50% and 90% intervals, the QRA median and the actual price, for the "
               "last full week of the test year without a clock change.",
            "probabilistic forecasting, quantile regression averaging, QRA, prediction interval, LEAR, ARX, electricity price, Romania",
            "Hourly day-ahead prices of Romania; hourly load, wind and solar generation of Romania; saved QRA quantiles of the "
            "test year (qra_week.npz: the 99 quantiles of the week and the median of every test hour, from lectures/L2/analysis_L2.py)",
            "A week of QRA intervals in Romania: wide in the evening, narrow at night")
    pw_mons = [t for t in TDAYS if t.dayofweek == 0 and t + pd.Timedelta(days=6) <= END]
    # DST flag of the test days from the numbers file (same rule as the notebook recomputes)
    dst_days = set(pd.to_datetime(NUM["design"]["dst_test"]))
    pw = max(t for t in pw_mons if not any((t + pd.Timedelta(days=j)) in dst_days for j in range(7)))
    k0 = TDAYS.get_loc(pw)
    save_npz(q.folder, "qra_week.npz", week=QRA_T[k0:k0 + 7], median=QRA_T[:, :, 49], week_start=np.array(str(pw.date())))
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md("## Expert ARX functions (used by the recomputation)\n\n" + ARX_MD).code(ARX_FUNCS + "\n\n\nARX_W = (56, 84, 112, 714, 721, 728)")
    q.md("## Quantile regression averaging (QRA)\n\nFor each hour, 99 quantile regressions of the actual price on the AW-ARX and "
         "AW-LEAR forecasts of the previous 182 days (burn-in + test), refitted every week; the quantiles are then sorted (no "
         "crossing). This needs the LEAR forecasts of 547 days and 24 x 99 quantile regressions per week, so the quantiles computed "
         "by `lectures/L2/analysis_L2.py` are loaded from the file saved next to this notebook (the week shown and the median of "
         "every test hour). `RUN_ALL = True` recomputes everything.")
    q.code("# the week of the chart: last full Monday-Sunday week of the test year without a clock change\n" + WEEKS +
           "PW = max(t for t in mons if not DST.loc[t:t + pd.Timedelta(days=6)].any())\n"
           "pw = slice(TPOS[PW], TPOS[PW] + 7)\n"
           'print("week:", PW.date(), "to", (PW + pd.Timedelta(days=6)).date())')
    q.code(forecast_block(n, days="all", qra=True) +
           '    Z = load_npz(QL + "qra_week.npz")\n'
           '    assert str(Z["week_start"]) == str(PW.date())\n'
           '    QW, QMED = Z["week"], Z["median"]                          # week x 24 x 99 quantiles; test days x 24\n'
           "if RUN_ALL:\n    QW, QMED = QRA[pw], QRA[:, :, 49]\n"
           'print("QRA median, MAE on the test year: %.2f EUR/MWh" % np.mean(np.abs(A - QMED)))')
    q.md("## The chart")
    q.code("import matplotlib.dates as mdates\nfrom matplotlib.ticker import FuncFormatter\n\n"
           'DAYN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]\n'
           'xt = pd.date_range(PW, periods=168, freq="h")\nqw = QW.reshape(168, 99)\n'
           "fig, ax = plt.subplots(figsize=(6.4, 2.0))\n"
           'ax.fill_between(xt, qw[:, 4], qw[:, 94], color=PAL["RO"], alpha=0.18, lw=0, label="90% interval")\n'
           'ax.fill_between(xt, qw[:, 24], qw[:, 74], color=PAL["RO"], alpha=0.38, lw=0, label="50% interval")\n'
           'ax.plot(xt, qw[:, 49], color=PAL["RO"], lw=1.0, label="QRA median")\n'
           'ax.plot(xt, A[pw].ravel(), color="#222222", lw=1.0, label="actual price")\n'
           'ax.set_ylabel("EUR/MWh")\nax.xaxis.set_major_locator(mdates.DayLocator())\n'
           'ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{DAYN[mdates.num2date(v).weekday()]} {mdates.num2date(v).day}"))\n'
           "legend_bottom(fig, ncol=4)\n" + save(n, 0.2))
    ck = [("first day of the week", "str(PW.date())", "weeks.prob", "s"),
          ("last day of the week", "str((PW + pd.Timedelta(days=6)).date())", "weeks.prob_end", "s"),
          ("MAE of the QRA median, test year", "np.mean(np.abs(A - QMED))", "prob.mae_median_qra", ".2f")]
    q.code(checks_cell(ck))
    return q, ck


@chart("prob_rel")
def q_prob_rel():
    n = "prob_rel"
    q = new(n, "Reliability of three probabilistic forecasts of the Romanian day-ahead price on the test year (99 quantiles each): "
               "share of actual prices below the tau-quantile minus tau, for quantile regression averaging (QRA), conformal "
               "prediction (CP) and historical simulation (HS); all three are too narrow in the tails. The Kupiec statistic "
               "tests the coverage of the 90% interval.",
            "probabilistic forecasting, reliability, calibration, quantile regression averaging, conformal prediction, historical "
            "simulation, Kupiec test, pinball loss, electricity price, Romania",
            "Hourly day-ahead prices of Romania; hourly load, wind and solar generation of Romania; saved LEAR forecasts of the "
            "burn-in and test days (forecasts.csv) and QRA quantiles of the test year (qra_test.npz, single precision), from "
            "lectures/L2/analysis_L2.py",
            "All three methods are too narrow in the tails")
    save_csv(q.folder, "forecasts.csv", ["lear364", "lear546", "lear728"], days="all")
    save_npz(q.folder, "qra_test.npz", q=QRA_T.astype(np.float32))
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md("## Expert ARX functions (used by the recomputation)\n\n" + ARX_MD).code(ARX_FUNCS + "\n\n\nARX_W = (56, 84, 112, 714, 721, 728)")
    q.md("## Point forecasts and QRA quantiles\n\nCP and HS are built here from the AW-LEAR errors of the previous 112 days; "
         "AW-LEAR (burn-in + test) and the QRA quantiles of the test year (99 quantile regressions per hour, refitted weekly on the "
         "previous 182 days) are loaded from the files saved next to this notebook. The QRA quantiles are stored in single "
         "precision to keep the file small; every number below is identical to the full-precision results. "
         "`RUN_ALL = True` recomputes everything.")
    q.code(forecast_block(n, days="all", qra=True) +
           '    S = load_csv("forecasts.csv", FDAYS)\n'
           '    LEAR = {T: S[f"lear{T}"].values.reshape(-1, 24) for T in LEAR_W}\n'
           '    QRA = load_npz(QL + "qra_test.npz")["q"].astype(float)       # test days x 24 hours x 99 quantiles\n'
           "FL_ = np.mean([LEAR[T] for T in LEAR_W], 0)                 # AW-LEAR, burn-in + test days\n"
           "ACT_F = P_[F_ROWS]")
    q.md("## Conformal prediction (CP) and historical simulation (HS) around AW-LEAR")
    q.code("W_ERR = 112\nERR_L = ACT_F - FL_\nCPQ = np.zeros((len(TDAYS), 24, len(TAUS)))\nHSQ = np.zeros_like(CPQ)\n"
           "for k, t in enumerate(range(N_BURN, len(FDAYS))):\n"
           "    win = ERR_L[t - W_ERR:t]                                 # errors of the previous 112 days, same hour\n"
           "    for j, tau in enumerate(TAUS):\n"
           "        HSQ[k, :, j] = FL_[t] + np.quantile(win, tau, axis=0)\n"
           "        CPQ[k, :, j] = FL_[t] + np.sign(tau - 0.5) * np.quantile(np.abs(win), abs(2 * tau - 1), axis=0)")
    q.md("## Scores: pinball loss, coverage, Kupiec test, reliability")
    q.code("from scipy import stats\n\n\n" + fsrc("nw_var", "prob_scores") + "\n\n\n"
           'PROB = {"qra": prob_scores(QRA), "cp": prob_scores(CPQ), "hs": prob_scores(HSQ)}\n'
           'print(pd.DataFrame({k: {kk: v for kk, v in r.items() if kk != "rel"} for k, r in PROB.items()}).round(4).to_string())')
    q.md("## The chart")
    q.code("fig, ax = plt.subplots(figsize=(6.4, 1.9))\n"
           'for k, c, lab in [("qra", PAL["RO"], "QRA"), ("cp", PAL["DE_LU"], "conformal (CP)"), ("hs", PAL["HU"], "historical simulation (HS)")]:\n'
           '    ax.plot(TAUS * 100, (np.array(PROB[k]["rel"]) - TAUS) * 100, color=c, label=lab)\n'
           'ax.axhline(0, color="#222222", lw=0.7)\nax.set_xlabel("quantile level $\\\\tau$, %")\n'
           'ax.set_ylabel("actual share below\\nminus $\\\\tau$, pp")\nlegend_bottom(fig, ncol=3)\n' + save(n, 0.2))
    ck = []
    for k, lab in [("qra", "QRA"), ("cp", "CP"), ("hs", "HS")]:
        ck += [(f"Kupiec statistic, {lab}", f'PROB["{k}"]["kupiec"]', f"prob.{k}.kupiec", ".2f"),
               (f"coverage of the 90% interval, {lab}, %", f'PROB["{k}"]["c90"]', f"prob.{k}.c90", ".2f"),
               (f"coverage of the 50% interval, {lab}, %", f'PROB["{k}"]["c50"]', f"prob.{k}.c50", ".2f"),
               (f"mean width of the 90% interval, {lab}", f'PROB["{k}"]["w90"]', f"prob.{k}.w90", ".2f"),
               (f"average pinball loss, {lab}", f'PROB["{k}"]["aps"]', f"prob.{k}.aps", ".2f")]
    q.code(checks_cell(ck))
    return q, ck


@chart("coint_daily")
def q_coint_daily():
    n = "coint_daily"
    q = new(n, "Daily base day-ahead prices of Romania (OPCOM) and Hungary (HUPX) and their spread: the two coupled markets are "
               "cointegrated (Engle-Granger and Johansen tests) and shocks to the spread die out within about a day.",
            "cointegration, Engle-Granger, Johansen trace test, market coupling, price spread, half-life, Romania, Hungary, "
            "day-ahead electricity prices",
            "Daily and hourly day-ahead prices of Romania, Hungary and Germany-Luxembourg (power_da_prices_daily_cet.csv, "
            "power_da_prices_hourly_utc.csv); Romanian generation (cut-off only)",
            "Romania and Hungary: coupled markets, a spread that keeps closing")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF)
    q.md("## Unit roots and cointegration, daily prices since 2022")
    q.code("import statsmodels.api as sm\nfrom statsmodels.tsa.stattools import adfuller, coint\n"
           "from statsmodels.tsa.vector_ar.vecm import coint_johansen\n\n\n" + fsrc("adf_p") + "\n\n\n"
           'DLY = PD.loc[START:END, ["RO", "HU", "DE_LU"]].dropna()\nco = {}\n'
           'for z in ["RO", "HU", "DE_LU"]:\n    co[f"adf_{z}"] = adf_p(DLY[z])\n'
           'for z in ["HU", "DE_LU"]:\n'
           '    eg = coint(DLY["RO"], DLY[z], trend="c", autolag="aic")\n'
           '    ols = sm.OLS(DLY["RO"], sm.add_constant(DLY[z])).fit()\n'
           "    u = ols.resid\n    phi = sm.OLS(u.values[1:], u.values[:-1]).fit().params[0]   # AR(1) of the spread residual\n"
           '    jo = coint_johansen(DLY[["RO", z]].values, det_order=0, k_ar_diff=6)\n'
           '    co[z] = {"eg": eg[0], "eg_cv5": eg[2][1], "beta": ols.params[z], "hl": np.log(0.5) / np.log(phi),\n'
           '             "tr0": jo.lr1[0], "tr0_cv": jo.cvt[0, 1], "tr1": jo.lr1[1], "tr1_cv": jo.cvt[1, 1],\n'
           '             "sd_spread": (DLY["RO"] - DLY[z]).std(), "mean_spread": (DLY["RO"] - DLY[z]).mean()}\n'
           'print(pd.DataFrame({z: co[z] for z in ["HU", "DE_LU"]}).round(3).to_string())')
    q.md("## Hours with identical prices in the test year (coupled, uncongested border)")
    q.code('HP = pd.read_csv(DATA + "power_da_prices_hourly_utc.csv", index_col=0, usecols=["timestamp_utc", "RO", "HU"])\n'
           "HP.index = pd.to_datetime(HP.index, utc=True).tz_convert(TZ)\n"
           "hpt = HP.loc[str(TEST0.date()):str(END.date())]\n"
           'EQ_HU = (np.abs(hpt["RO"] - hpt["HU"]) < 0.01).mean() * 100')
    q.md("## The chart")
    q.code('fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.4), sharex=True, gridspec_kw={"height_ratios": [1.5, 1]})\n'
           'axs[0].plot(DLY.index, DLY["HU"], color=PAL["HU"], lw=0.7, label="Hungary (HUPX)")\n'
           'axs[0].plot(DLY.index, DLY["RO"], color=PAL["RO"], lw=0.7, label="Romania (OPCOM PZU)")\n'
           'axs[0].set_ylabel("EUR/MWh")\n'
           'axs[1].plot(DLY.index, DLY["RO"] - DLY["HU"], color=PAL["c8"], lw=0.6, label="spread RO - HU")\n'
           'axs[1].axhline(0, color="#222222", lw=0.5)\naxs[1].set_ylabel("EUR/MWh")\naxs[1].set_xlim(DLY.index[0], DLY.index[-1])\n'
           "legend_bottom(fig, ncol=3)\n" + save(n, 0.15))
    ck = [("first day", "str(DLY.index.min().date())", "coint.start", "s"),
          ("mean spread RO - HU", 'co["HU"]["mean_spread"]', "coint.HU.mean_spread", ".2f"),
          ("standard deviation of the spread RO - HU", 'co["HU"]["sd_spread"]', "coint.HU.sd_spread", ".2f"),
          ("mean spread RO - DE-LU", 'co["DE_LU"]["mean_spread"]', "coint.DE_LU.mean_spread", ".2f"),
          ("standard deviation of the spread RO - DE-LU", 'co["DE_LU"]["sd_spread"]', "coint.DE_LU.sd_spread", ".2f"),
          ("hours RO = HU in the test year, %", "EQ_HU", "coint.eq_hu_test", ".1f"),
          ("beta RO on HU", 'co["HU"]["beta"]', "coint.HU.beta", ".3f"),
          ("Engle-Granger statistic", 'co["HU"]["eg"]', "coint.HU.eg", ".2f"),
          ("Engle-Granger 5% critical value", 'co["HU"]["eg_cv5"]', "coint.HU.eg_cv5", ".2f"),
          ("half-life of a spread shock, days", 'co["HU"]["hl"]', "coint.HU.hl", ".1f"),
          ("Johansen trace r = 0", 'co["HU"]["tr0"]', "coint.HU.tr0", ".2f"),
          ("Johansen trace r <= 1", 'co["HU"]["tr1"]', "coint.HU.tr1", ".2f"),
          ("ADF p-value, Romanian price level", 'co["adf_RO"]', "coint.adf_RO", ".4f")]
    q.code(checks_cell(ck))
    return q, ck


@chart("coint_monthly")
def q_coint_monthly():
    n = "coint_monthly"
    q = new(n, "Monthly mean day-ahead price of Romania against its long-run level implied by the TTF gas price (cointegrating "
               "regression), and the deviation from that level against hydro generation in excess of its calendar-month mean: "
               "months with more hydro than usual sit below the gas-implied level (error-correction model).",
            "cointegration, error-correction model, gas price, TTF, hydro generation, Engle-Granger, Johansen, half-life, Romania",
            "Daily day-ahead prices of Romania (power_da_prices_daily_cet.csv); hourly hydro generation of Romania "
            "(generation_ro_mw_hourly_utc.csv); monthly TTF gas price (ttf_monthly.csv, World Bank Pink Sheet)",
            "Power, gas and hydro: the Lecture 1 regression is not spurious")
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF)
    q.md("## Monthly series: price, TTF gas and hydro (CET/CEST calendar months)")
    q.code('GH = pd.read_csv(DATA + "generation_ro_mw_hourly_utc.csv", index_col=0, usecols=["timestamp_utc", "hydro_run_of_river", "hydro_water_reservoir"])\n'
           "GH.index = pd.to_datetime(GH.index, utc=True)\n"
           'hyd = GH[["hydro_run_of_river", "hydro_water_reservoir"]].sum(axis=1, min_count=2)\n'
           'END_UTC = (END + pd.Timedelta(days=1)).tz_localize(TZ).tz_convert("UTC")\nhyd = hyd[hyd.index < END_UTC]\n'
           'hyd_m = hyd.tz_convert(TZ).resample("MS").sum(min_count=600) / 1e6     # TWh per month (a month needs 600 hours)\n'
           "hyd_m.index = hyd_m.index.tz_localize(None)\n"
           'TTF = pd.read_csv(DATA + "ttf_monthly.csv")\nTTF.index = pd.PeriodIndex(TTF["month"], freq="M").to_timestamp()\n'
           'MD = pd.concat([PD["RO"].loc[:END].resample("MS").mean().rename("price"), TTF["ttf_eur_mwh"].rename("ttf"),\n'
           '                hyd_m.rename("hydro")], axis=1).dropna()\n'
           'MD["hydro_ds"] = MD["hydro"] - MD.groupby(MD.index.month)["hydro"].transform("mean")   # hydro minus its calendar-month mean\n'
           'print(MD.index.min().strftime("%Y-%m"), "to", MD.index.max().strftime("%Y-%m"), len(MD), "months")')
    q.md("## Cointegration and error-correction model")
    q.code("import statsmodels.api as sm\nfrom statsmodels.tsa.stattools import coint\n"
           "from statsmodels.tsa.vector_ar.vecm import coint_johansen\n\n"
           'eg1 = coint(MD["price"], MD["ttf"], trend="c", autolag="aic")\n'
           'lr_ = sm.OLS(MD["price"], sm.add_constant(MD[["ttf"]])).fit()        # long-run level from gas\nu_ = lr_.resid\n'
           'jo = coint_johansen(MD[["price", "ttf"]].values, det_order=0, k_ar_diff=2)\n'
           "JO_RANK = (1 if jo.lr1[1] <= jo.cvt[1, 1] else 2) if jo.lr1[0] > jo.cvt[0, 1] else 0\n"
           'ecm_df = pd.DataFrame({"dp": MD["price"].diff(), "u1": u_.shift(1), "dttf": MD["ttf"].diff(), "hyd": MD["hydro_ds"]}).dropna()\n'
           'ecm = sm.OLS(ecm_df["dp"], sm.add_constant(ecm_df[["u1", "dttf", "hyd"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 6})\n'
           'al = ecm.params["u1"]\nprint(ecm.summary().tables[1])')
    q.md("## The chart")
    q.code('fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1), gridspec_kw={"width_ratios": [1.5, 1]})\n'
           'axs[0].plot(MD.index, MD["price"], color=PAL["RO"], lw=1.0, label="Romania, monthly price")\n'
           'axs[0].plot(MD.index, lr_.fittedvalues, color=PAL["DE_LU"], lw=1.0, ls="--", label="long-run level from TTF gas")\n'
           'axs[0].set_ylabel("EUR/MWh")\n'
           'axs[1].scatter(MD["hydro_ds"], u_, s=8, color=PAL["RO"], alpha=0.7, label="one month")\n'
           'bb = np.polyfit(MD["hydro_ds"], u_, 1)\nxx = np.linspace(MD["hydro_ds"].min(), MD["hydro_ds"].max(), 10)\n'
           'axs[1].plot(xx, np.polyval(bb, xx), color="#222222", lw=1.0)\naxs[1].axhline(0, color="#222222", lw=0.4)\n'
           'axs[1].set_xlabel("hydro vs its monthly mean, TWh", fontsize=9.5)\naxs[1].set_ylabel("price minus long-run", fontsize=9)\n'
           "legend_bottom(fig, ncol=3)\n" + save(n, 0.2))
    ck = [("first month", 'MD.index.min().strftime("%Y-%m")', "coint_m.start", "s"),
          ("last month", 'MD.index.max().strftime("%Y-%m")', "coint_m.end", "s"),
          ("Engle-Granger statistic, price on TTF", "eg1[0]", "coint_m.eg1", ".2f"),
          ("Engle-Granger 5% critical value", "eg1[2][1]", "coint_m.eg1_cv5", ".2f"),
          ("Johansen rank", "JO_RANK", "coint_m.jo_rank", "d"),
          ("beta on TTF", 'lr_.params["ttf"]', "coint_m.beta", ".3f"),
          ("implied gas-plant efficiency, %", '100 / lr_.params["ttf"]', "coint_m.eff", ".1f"),
          ("alpha (speed of return)", "al", "coint_m.alpha", ".3f"),
          ("half-life, months", "np.log(0.5) / np.log(1 + al)", "coint_m.hl", ".1f"),
          ("delta, EUR/MWh per TWh of extra hydro", 'ecm.params["hyd"]', "coint_m.d_hyd", ".2f"),
          ("t-statistic of delta", 'ecm.tvalues["hyd"]', "coint_m.d_hyd_t", ".2f")]
    q.code(checks_cell(ck))
    return q, ck


@chart("monthly_mae")
def q_monthly_mae():
    n = "monthly_mae"
    q = new(n, "Monthly mean absolute error over the test year of four forecasts of the Romanian day-ahead price: naive, AW-ARX, "
               "AW-LEAR and the equal-weight ensemble of AW-ARX, AW-LEAR, GBM and MLP.",
            "forecast evaluation, monthly MAE, LEAR, ARX, ensemble, naive benchmark, electricity price forecasting, Romania",
            ML_DATAFILE, "Case study (a): a year of forecasts, month by month")
    ml_quantlet(n, q)
    q.code(MFMT + "\nBYMONTH = {k: bymonth(v) for k, v in [(\"naive\", NAIVE), (\"aw_arx\", AW_ARX), (\"aw_lear\", AW_LEAR), (\"ens_all\", ENS_ALL)]}\n"
           'print(pd.DataFrame(BYMONTH, index=[str(m) for m in MONTHS_T]).round(2).to_string())')
    q.md("## The chart")
    q.code('COL = {"naive": "#9a9a9a", "aw_arx": PAL["HU"], "aw_lear": PAL["RO"], "ens_all": PAL["DE_LU"]}\n'
           'LAB = {"naive": "Naive", "aw_arx": "AW-ARX", "aw_lear": "AW-LEAR", "ens_all": "Ens. 4 models"}\n'
           "fig, ax = plt.subplots(figsize=(6.4, 1.9))\n"
           'for k, ls, mk in [("naive", ":", "o"), ("aw_arx", "--", "s"), ("aw_lear", "-", "o"), ("ens_all", "-", "D")]:\n'
           "    ax.plot(xm, BYMONTH[k], color=COL[k], ls=ls, marker=mk, ms=3.5, label=LAB[k])\n"
           'ax.set_ylabel("MAE, EUR/MWh")\nmfmt(ax, 1)\nlegend_bottom(fig, ncol=4)\n' + save(n, 0.2))
    ck = [("months AW-LEAR beats naive", 'int((BYMONTH["aw_lear"] < BYMONTH["naive"]).sum())', "bymonth.n_months_lear_beats_naive", "d"),
          ("best month", 'str(MONTHS_T[int(np.argmin(BYMONTH["aw_lear"]))])', "bymonth.best_month", "s"),
          ("AW-LEAR MAE in the best month", 'BYMONTH["aw_lear"].min()', "bymonth.best_mae", ".2f"),
          ("worst month", 'str(MONTHS_T[int(np.argmax(BYMONTH["aw_lear"]))])', "bymonth.worst_month", "s"),
          ("AW-LEAR MAE in the worst month", 'BYMONTH["aw_lear"].max()', "bymonth.worst_mae", ".2f")]
    q.code(checks_cell(ck))
    return q, ck


@chart("stress_week")
def q_stress_week():
    n = "stress_week"
    q = new(n, "Hourly Romanian day-ahead price in the stress week of the test year (the Monday-Sunday week with the highest mean "
               "price) against the naive, AW-LEAR and ensemble forecasts: every model lags the jump in level by a day.",
            "stress week, price spike, forecast error, LEAR, ensemble, naive benchmark, electricity price forecasting, Romania",
            ML_DATAFILE, "Case study (b): the stress week")
    ml_quantlet(n, q)
    q.md("## The stress week: highest mean price, Monday to Sunday")
    q.code(WEEKS + "SW = max(mons, key=lambda t: A[TPOS[t]:TPOS[t] + 7].mean())\nsw = slice(TPOS[SW], TPOS[SW] + 7)\n"
           'M = {"naive": NAIVE, "aw_arx": AW_ARX, "aw_lear": AW_LEAR, "gbm": GBM, "mlp": MLP, "ens_all": ENS_ALL}\n'
           "SMAE = {k: np.mean(np.abs(A[sw] - v[sw])) for k, v in M.items()}\n"
           'print("week:", SW.date(), "to", (SW + pd.Timedelta(days=6)).date())')
    q.md("## The chart")
    q.code("import matplotlib.dates as mdates\nfrom matplotlib.ticker import FuncFormatter\n\n"
           'DAYN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]\n'
           'COL = {"naive": "#9a9a9a", "aw_lear": PAL["RO"], "ens_all": PAL["DE_LU"]}\n'
           'LAB = {"naive": "Naive", "aw_lear": "AW-LEAR", "ens_all": "Ens. 4 models"}\n'
           'xs_ = pd.date_range(SW, periods=168, freq="h")\nfig, ax = plt.subplots(figsize=(6.4, 2.0))\n'
           'ax.plot(xs_, A[sw].ravel(), color="#222222", lw=1.3, label="actual price")\n'
           'for k, ls in [("naive", ":"), ("aw_lear", "-"), ("ens_all", "--")]:\n'
           "    ax.plot(xs_, M[k][sw].ravel(), color=COL[k], ls=ls, lw=1.0, label=LAB[k])\n"
           'ax.set_ylabel("EUR/MWh")\nax.xaxis.set_major_locator(mdates.DayLocator())\n'
           'ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{DAYN[mdates.num2date(v).weekday()]} {mdates.num2date(v).day}"))\n'
           "legend_bottom(fig, ncol=4)\n" + save(n, 0.2))
    ck = ([("first day of the week", "str(SW.date())", "weeks.stress", "s"),
           ("mean price of the week", "A[sw].mean()", "weeks.stress_mean", ".2f"),
           ("highest hourly price of the week", "A[sw].max()", "weeks.stress_max", ".2f")] +
          [(f"MAE {k} in the week", f'SMAE["{k}"]', f"weeks.stress_mae.{k}", ".2f")
           for k in ["naive", "aw_arx", "aw_lear", "gbm", "mlp", "ens_all"]])
    q.code(checks_cell(ck))
    return q, ck


@chart("mtu15")
def q_mtu15():
    n = "mtu15"
    q = new(n, "Romanian day-ahead price for the 96 quarter-hours of the test day with the largest intra-hour variation, against "
               "the hourly AW-LEAR forecast held flat within each hour and the same forecast plus the mean intra-hour shape of "
               "the 28 previous days (15-minute market time unit since 1 October 2025).",
            "15-minute market time unit, MTU, quarter-hour prices, intra-hour profile, SDAC, LEAR, electricity price forecasting, Romania",
            "Hourly and 15-minute day-ahead prices of Romania (power_da_prices_hourly_utc.csv, power_da_prices_native_utc.csv); "
            "hourly load, wind and solar of Romania; saved LEAR forecasts of the test year (forecasts_test.csv, from "
            "lectures/L2/analysis_L2.py)",
            "Case study (c): forecasting 96 quarter-hours since 1 October 2025")
    save_csv(q.folder, "forecasts_test.csv", ["lear364", "lear546", "lear728"])
    q.code(SETUP).md("## Data and cut-off").code(CUTOFF).md("## Panels of price, load and wind + solar").code(panel())
    q.md(LEAR_MD)
    q.code(forecast_block(n, helpers=True) +
           '    S = load_csv("forecasts_test.csv", TDAYS)\n'
           '    LEAR = {T: S[f"lear{T}"].values.reshape(-1, 24) for T in LEAR_W}\n'
           "AW_LEAR = np.mean([LEAR[T] for T in LEAR_W], 0)")
    q.md("## Quarter-hour prices and the shaped forecast")
    q.code('XN = pd.read_csv(DATA + "power_da_prices_native_utc.csv", usecols=["timestamp_utc", "RO"], parse_dates=["timestamp_utc"]).set_index("timestamp_utc")\n'
           "XN.index = XN.index.tz_convert(TZ)\n"
           '_xn = XN.loc[str((TEST0 - pd.Timedelta(days=40)).date()):str(END.date()), "RO"]\n'
           "ALLQ = {dd: g.values for dd, g in _xn.groupby(_xn.index.tz_localize(None).normalize()) if len(g) == 96}   # days with 96 quarter-hours\n"
           "TPOS = {t: k for k, t in enumerate(TDAYS)}\n"
           "QDAYS = [t for t in TDAYS if t in ALLQ and not DST.loc[t]]\n"
           "Q = np.array([ALLQ[t] for t in QDAYS])                         # days x 96 quarter-hours\n"
           "hourly_mean = Q.reshape(len(QDAYS), 24, 4).mean(2)\n"
           "dev = Q - np.repeat(hourly_mean, 4, axis=1)                    # intra-hour deviation from the hourly mean\n"
           "flat = np.repeat(np.array([AW_LEAR[TPOS[t]] for t in QDAYS]), 4, axis=1)\n"
           "shape = np.zeros_like(Q)\nfor k, t in enumerate(QDAYS):\n"
           "    past = [ALLQ[t - pd.Timedelta(days=j)] for j in range(1, 29) if (t - pd.Timedelta(days=j)) in ALLQ]   # days d-28..d-1\n"
           "    shape[k] = np.mean([p - np.repeat(p.reshape(24, 4).mean(1), 4) for p in past], 0)\n"
           "shaped = flat + shape\n"
           "QDAY = QDAYS[int(np.argmax(np.abs(dev).mean(1)))]                 # day with the largest intra-hour variation\n"
           "MAE_FLAT, MAE_SHAPED = np.mean(np.abs(Q - flat)), np.mean(np.abs(Q - shaped))")
    q.md("## The chart")
    q.code("qk = QDAYS.index(QDAY)\nxq = np.arange(96) / 4\nfig, ax = plt.subplots(figsize=(6.4, 2.0))\n"
           'ax.step(xq, Q[qk], where="post", color="#222222", lw=1.1, label="actual 15-min price")\n'
           'ax.step(xq, flat[qk], where="post", color=PAL["RO"], lw=1.0, ls="--", label="hourly AW-LEAR, flat")\n'
           'ax.step(xq, shaped[qk], where="post", color=PAL["DE_LU"], lw=1.0, label="+ intra-hour shape (28 past days)")\n'
           'ax.set_xticks(range(0, 25, 2))\nax.set_xlabel("hour (CET)")\nax.set_ylabel("EUR/MWh")\n'
           "legend_bottom(fig, ncol=3)\n" + save(n, 0.2))
    ck = [("test days with 96 quarter-hours, without DST", "len(QDAYS)", "mtu15.n_days", "d"),
          ("quarter-hour MAE, flat", "MAE_FLAT", "mtu15.mae_flat", ".2f"),
          ("quarter-hour MAE, shaped", "MAE_SHAPED", "mtu15.mae_shaped", ".2f"),
          ("gain of the shape, %", "(1 - MAE_SHAPED / MAE_FLAT) * 100", "mtu15.gain_pct", ".1f"),
          ("day shown", "str(QDAY.date())", "mtu15.day", "s")]
    q.code(checks_cell(ck))
    return q, ck


@chart("battery")
def q_battery():
    n = "battery"
    q = new(n, "Economic value of forecasts of the Romanian day-ahead price on the test year: left, profit of a 1 MW / 2 MWh "
               "battery (one daily cycle chosen on the forecast, round-trip efficiency 90%) with perfect foresight, the ensemble, "
               "AW-LEAR, GBM, AW-ARX and the naive forecast; right, price paid by a flexible 4-hour consumer who places its "
               "process on the forecast, against a fixed 8-12 h block.",
            "value of forecasts, battery arbitrage, demand flexibility, perfect foresight, LEAR, ensemble, electricity price, Romania",
            ML_DATAFILE, "Case study (d): what a better forecast is worth")
    ml_quantlet(n, q)
    q.md("## Battery and flexible consumer, valued at the actual prices (days with a clock change left out)")
    q.code(fsrc("battery", "flex") + "\n\n\n"
           "NODST = ~DST.loc[TDAYS].values\nAN = A[NODST]\n"
           'M = {"naive": NAIVE, "aw_arx": AW_ARX, "aw_lear": AW_LEAR, "gbm": GBM, "ens_all": ENS_ALL}\n'
           "BAT = {k: battery(v[NODST], AN) for k, v in M.items()}\nBAT[\"perfect\"] = battery(AN, AN)\n"
           "FLX = {k: flex(v[NODST], AN)[0] for k, v in M.items()}\nFLX[\"perfect\"], FLX_BASE = flex(AN, AN)\n"
           'print(pd.DataFrame({"battery, EUR": {k: v.sum() for k, v in BAT.items()},\n'
           '                    "flexible buyer, EUR/MWh": {k: v.sum() / (4 * len(v)) for k, v in FLX.items()}}).round(2).to_string())')
    q.md("## The chart")
    q.code('COL = {"naive": "#9a9a9a", "aw_arx": PAL["HU"], "aw_lear": PAL["RO"], "gbm": PAL["BG"], "ens_all": PAL["DE_LU"], "perfect": "#222222"}\n'
           'LAB = {"naive": "Naive", "aw_arx": "AW-ARX", "aw_lear": "AW-LEAR", "gbm": "GBM", "ens_all": "Ens. 4 models", "perfect": "Perfect foresight"}\n'
           "fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1))\n"
           'kb = ["perfect", "ens_all", "aw_lear", "gbm", "aw_arx", "naive"]\n'
           "axs[0].barh(range(len(kb)), [BAT[k].sum() / 1000 for k in kb], color=[COL[k] for k in kb], height=0.65)\n"
           "axs[0].set_yticks(range(len(kb)))\naxs[0].set_yticklabels([LAB[k] for k in kb], fontsize=9)\naxs[0].invert_yaxis()\n"
           'axs[0].set_xlabel("battery profit, thousand EUR per MW", fontsize=9.5)\n'
           "vf = [FLX[k].sum() / (4 * len(FLX[k])) for k in kb] + [FLX_BASE.sum() / (4 * len(FLX_BASE))]\n"
           'axs[1].barh(range(len(vf)), vf, color=[COL[k] for k in kb] + ["#5b4a3a"], height=0.65)\n'
           'axs[1].set_yticks(range(len(vf)))\naxs[1].set_yticklabels([LAB[k] for k in kb] + ["fixed 8-12 h"], fontsize=9)\naxs[1].invert_yaxis()\n'
           'axs[1].set_xlabel("flexible buyer, EUR/MWh paid", fontsize=9.5)\n' + save(n, 0.02))
    ck = [("days without a clock change", "int(NODST.sum())", "battery.n_days", "d"),
          ("battery profit with the ensemble, EUR per MW", 'BAT["ens_all"].sum()', "battery.ens_all.eur", ".0f"),
          ("share of perfect foresight, %", 'BAT["ens_all"].sum() / BAT["perfect"].sum() * 100', "battery.ens_all.pct", ".1f"),
          ("battery profit with naive, EUR per MW", 'BAT["naive"].sum()', "battery.naive.eur", ".0f"),
          ("battery profit with perfect foresight, EUR per MW", 'BAT["perfect"].sum()', "battery.perfect.eur", ".0f"),
          ("flexible buyer with AW-LEAR, EUR/MWh", 'FLX["aw_lear"].sum() / (4 * len(FLX["aw_lear"]))', "flex.aw_lear.eur_mwh", ".2f"),
          ("fixed 8-12 h block, EUR/MWh", "FLX_BASE.sum() / (4 * len(FLX_BASE))", "flex.base_eur_mwh", ".2f")]
    q.code(checks_cell(ck))
    return q, ck


# =============================================================================
# 4. Build, execute, compare the printed numbers with L2_numbers.json
# =============================================================================
def jget(key):
    v = NUM
    for p in key.split("."):
        v = v[p]
    return v


def compare(q, ck):
    nb = nbformat.read(os.path.join(q.folder, q.name + ".ipynb"), 4)
    text = "".join(o.get("text", "") for c in nb.cells if c.cell_type == "code" for o in c.get("outputs", []))
    bad = []
    for lab, _, key, fmt in ck:
        m = re.search(r"^  " + re.escape(lab) + r": (.*)$", text, re.M)
        got = m.group(1).strip() if m else None
        ref = format(jget(key), fmt)
        if got != ref:
            bad.append((q.chart, lab, key, got, ref))
    return bad


def built_charts():
    """Charts included in the decks: \\includegraphics of charts/en/<name>.pdf in the generated lecture2.tex."""
    tex = open(os.path.join(HERE, "lecture2.tex"), encoding="utf-8").read()
    return list(dict.fromkeys(re.findall(r"charts/en/([A-Za-z0-9_]+)\.pdf", tex)))


def main(only):
    shown = built_charts()
    missing = [c for c in shown if c not in CHARTS]
    assert not missing, f"no Quantlet defined for {missing}"
    names = only or shown
    bad = []
    for nm in names:
        q, ck = CHARTS[nm]()
        q.write(execute=True)
        b = compare(q, ck)
        print(f"  {len(ck)} numbers checked against L2_numbers.json, {len(b)} mismatches")
        bad += b
    if bad:
        print("\nMISMATCHES (chart, label, key, notebook, slide):")
        for b in bad:
            print("  ", b)
        sys.exit(1)
    print(f"\n{len(names)} Quantlets written; every printed number equals L2_numbers.json")


if __name__ == "__main__":
    main(sys.argv[1:])
