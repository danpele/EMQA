"""
make_quantlets_L7.py -- one Quantlet per chart of Lecture 7 (Machine learning for energy markets)
=================================================================================================
Writes Quantlets/L7/EMQA_L7_<chart>/ for every chart shown in lecture7.pdf (main part and appendix):
    Metainfo.txt, EMQA_L7_<chart>.ipynb (self-contained, executed), <chart>.png
    and, for the charts that need the machine-learning models, <chart>_results.npz: the saved model outputs that the
    chart needs (forecasts, probabilities, SHAP values, validation errors), so that the notebook runs on Google Colab
    (CPU) in seconds. Each such notebook has a switch RUN_ALL = False; with RUN_ALL = True it recomputes those outputs
    from the data with the full code of lectures/L7/analysis_L7.py (copied into the notebook; slow: hours on one core).

How the saved outputs are produced: this script executes analysis_L7.py up to its chart section, reading only its cache
(lectures/L7/cache/ml.pkl, leak.pkl; it stops if the cache is stale), checks that the numbers it recomputes equal
L7_numbers.json, then saves the arrays. After executing each notebook it checks that every number the notebook prints
equals the value in L7_numbers.json (the value on the slide).

Run from the repository root:  python3 lectures/L7/make_quantlets_L7.py   [chart ...]   (about 5 minutes)
"""
import ast
import json
import os
import sys
import textwrap

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "lectures", "common"))
from emqa_quantlet import Quantlet  # noqa: E402

A7 = os.path.join(HERE, "analysis_L7.py")
A2 = os.path.join(REPO, "lectures", "L2", "analysis_L2.py")
J = json.load(open(os.path.join(HERE, "L7_numbers.json"), encoding="utf-8"))
ONLY = sys.argv[1:]


# =============================================================================
# 1. Results of the analysis (from its cache), checked against L7_numbers.json
# =============================================================================
def run_analysis():
    src = open(A7, encoding="utf-8").read()
    src = src[:src.index("# Charts: one set per language")]
    src = src.replace('if C is None:\n    C = {"key": KEY}', 'if C is None:\n    raise RuntimeError("lectures/L7/cache/ml.pkl is stale: run analysis_L7.py first")', 1)
    src = src.replace("if LK is None:\n", "if LK is None:\n    raise RuntimeError('lectures/L7/cache/leak.pkl is stale: run analysis_L7.py first')\n", 1)
    ns = {"__file__": A7, "__name__": "analysis_L7_results"}
    exec(compile(src, A7, "exec"), ns)
    bad = []

    def cmp(a, b, path):
        if isinstance(b, dict):
            for k in b:
                if k != "charts":
                    cmp(a.get(k), b[k], path + k + ".")
        elif isinstance(b, list):
            for i, (x, y) in enumerate(zip(a, b)):
                cmp(x, y, path + str(i) + ".")
        else:
            x = a.item() if hasattr(a, "item") else a
            if isinstance(b, float) or isinstance(x, float):
                if x is None or b is None or abs(float(x) - float(b)) > 1e-9:
                    bad.append((path, x, b))
            elif str(x) != str(b):
                bad.append((path, x, b))
    cmp(ns["N"], J, "")
    if bad:
        raise RuntimeError(f"the cached results differ from L7_numbers.json: {bad[:10]}")
    print("analysis results loaded from the cache; identical to L7_numbers.json")
    return ns


def source_of(path, names):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    out = []
    for n in names:
        node = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == n)
        out.append(ast.get_source_segment(src, node))
    return "\n\n\n".join(out)


def get(d, key):
    for k in key.split("."):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d


# =============================================================================
# 2. Code blocks shared by the notebooks (each notebook gets only those it needs)
# =============================================================================
STYLE = r'''import io
import urllib.request

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats

# course chart style: transparent background, no gridlines, legend at the bottom outside the axes
plt.rcParams.update({
    "figure.facecolor": "none", "axes.facecolor": "none", "savefig.transparent": True,
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#222222", "axes.labelcolor": "#222222", "xtick.color": "#222222", "ytick.color": "#222222",
    "text.color": "#222222", "font.size": 11, "axes.titlesize": 11.5, "axes.labelsize": 11,
    "legend.fontsize": 10.5, "legend.frameon": False, "lines.linewidth": 1.4, "font.family": "DejaVu Sans"})
PAL = {"RO": "#2a78d6", "DE_LU": "#eb6834", "HU": "#1baf7a", "BG": "#eda100",
       "c5": "#e87ba4", "c6": "#008300", "c7": "#6250d6", "c8": "#e34948"}


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
        fig.legend(handles, labels, loc="lower center", ncol=ncol, bbox_to_anchor=(0.5, y), frameon=False,
                   handlelength=2.0, columnspacing=1.2)


def save_chart(fig, name, bottom=0.17):
    fig.tight_layout(rect=(0, bottom, 1, 1))
    plt.savefig(name + ".png", dpi=150, bbox_inches="tight", transparent=True)
    plt.show()


def show(label, value, fmt=""):
    """Print a number that appears on the slide."""
    print(f"{label}: {format(value, fmt)}")'''

LABCOL = r'''LAB = {"naive": "Naive", "aw_arx": "AW-ARX", "aw_lear": "AW-LEAR", "ens4": "Ens. of 4 (L2)", "gbm2": "GBM (L2)",
       "mlp2": "MLP (L2)", "xgb": "XGBoost", "dnn": "DNN", "bolt": "Chronos-Bolt", "chr2": "Chronos-2", "ens_ld": "LEAR+DNN",
       "ens_lx": "LEAR+XGBoost", "ens_ldx": "LEAR+DNN+XGBoost", "ens_t4": "Ens. of 4, tuned ML",
       "ens_t5": "Ens. of 5 (with Chronos-2)", "ens_lc": "LEAR+Chronos-2"}
COL = {"naive": "#9a9a9a", "aw_arx": PAL["HU"], "aw_lear": PAL["RO"], "ens4": PAL["c5"], "gbm2": "#c9a14a", "mlp2": "#a99be0",
       "xgb": PAL["BG"], "dnn": PAL["c7"], "bolt": "#6b6b6b", "chr2": PAL["c8"], "ens_ld": PAL["c6"], "ens_lx": PAL["c6"],
       "ens_ldx": PAL["DE_LU"], "ens_t4": PAL["DE_LU"], "ens_t5": PAL["DE_LU"], "ens_lc": "#7a1f1f"}'''

FNAME = r'''FNAME = {"P(d-1,h)": "price d-1, same hour", "P(d-2,h)": "price d-2, same hour", "P(d-3,h)": "price d-3, same hour",
         "P(d-7,h)": "price d-7, same hour", "P(d-1,23)": "price d-1, 23:00", "min P(d-1)": "min. price d-1",
         "max P(d-1)": "max. price d-1", "mean P(d-1)": "mean price d-1", "L(d-2,h)": "load d-2, same hour",
         "L(d-7,h)": "load d-7, same hour", "RES(d-2,h)": "wind+solar d-2, same hour", "RES(d-7,h)": "wind+solar d-7, same hour",
         "mean L(d-2)": "mean load d-2", "mean RES(d-2)": "mean wind+solar d-2", "hydro(d-2)": "hydro d-2",
         "nuclear(d-2)": "nuclear d-2", "net imports(d-2)": "net imports d-2", "EUA(d-2)": "carbon price d-2",
         "hour": "hour of day", "day of week": "day of week"}'''


def prices_block():
    return ("TZ = \"Europe/Brussels\"\n\n\n" + source_of(A7, ["day_matrix"]) + r'''


# Romanian day-ahead price (OPCOM PZU), hourly; after 1 Oct 2025 the hour is the mean of its four quarter-hours
HP = pd.read_csv(DATA + "power_da_prices_hourly_utc.csv", usecols=["timestamp_utc", "RO"], index_col=0)
PM_ALL, DST = day_matrix(HP["RO"].dropna())          # all CET delivery days since 2015 x 24 hours
# sample of the lecture: 2022-01-01 to the cut-off 2026-10-31 (last complete month at the download of 2026-11-04)
START, END = pd.Timestamp("2022-01-01"), pd.Timestamp("2026-10-31")
CAL = pd.date_range(START, END, freq="D")
PM = PM_ALL.reindex(CAL)
assert not PM.isna().any().any(), "panel has gaps"
P_ = PM.values.astype(float)
DOW = CAL.dayofweek.values
IDX = {t: i for i, t in enumerate(CAL)}
FIRST = 7                                             # first usable target row (needs the price of d-7)
TEST0 = END - pd.Timedelta(days=364)                  # test year = the last 365 days (as in Lecture 2)
VAL0 = TEST0 - pd.Timedelta(days=365)                 # validation year = the 365 days before it
TDAYS = pd.date_range(TEST0, END, freq="D")
VDAYS = pd.date_range(VAL0, TEST0 - pd.Timedelta(days=1), freq="D")
rows_all = np.array([IDX[t] for t in TDAYS])
A = P_[rows_all]                                      # actual prices of the test year (365 days x 24 hours), EUR/MWh
print("panel", CAL[0].date(), "to", CAL[-1].date(), "| test year", TEST0.date(), "to", END.date(), A.shape)''')


THRESH = r'''THR_Q = 0.90


def spike_threshold(t):
    """Spike threshold for delivery days of the month starting at t: 90th percentile of the hourly prices of the 365 days before t."""
    w = PM_ALL.loc[t - pd.Timedelta(days=365):t - pd.Timedelta(days=1)].values.ravel()
    return float(np.quantile(w, THR_Q))


_TH = {}


def theta_of(t):
    """threshold of the delivery month of day t (known at the start of the month)"""
    ms = t.replace(day=1)
    if ms not in _TH:
        _TH[ms] = spike_threshold(ms)
    return _TH[ms]


TH_T = np.array([theta_of(t) for t in TDAYS])
Y_SP = (A > TH_T[:, None]).astype(int)                # spike hours of the test year
Y_NG = (A <= 0).astype(int)                           # hours with price <= 0'''

LBAR = r'''# cost-loss rule: C = assumed cost of acting; L-bar = mean excess over the threshold in spike hours of the VALIDATION year
C_ACT = 30.0
vrows = np.array([IDX[t] for t in VDAYS])
PV, THV = P_[vrows], np.array([theta_of(t) for t in VDAYS])[:, None]
LBAR = float((PV - THV)[PV > THV].mean())
CUT = C_ACT / LBAR'''

LOADER = r'''QL = "{name}"


def load_results(fname):
    """Saved outputs of the full computation, stored in this Quantlet folder (local copy, else the public repository)."""
    if os.path.isfile(fname):
        return dict(np.load(fname, allow_pickle=False))
    raw = urllib.request.urlopen(REPO + "Quantlets/L7/" + QL + "/" + fname).read()
    return dict(np.load(io.BytesIO(raw), allow_pickle=False))'''

DM = source_of(A7, ["nw_var", "dm"])

ENGINE_FUNCS = {
    "base": ["shift_rows", "mad_scale", "blocks_of"],
    "dnn": ["dnn_inputs", "_net", "_train", "dnn_block", "dnn_predict_from"],
    "xgb": ["gbm_rows", "_xgb", "xgb_block"],
    "shuffled": ["xgb_cv_shuffled"],
    "clf": ["spike_threshold", "clf_rows", "clf_block"],
    "chronos": ["chronos_forecasts"],
    "space": ["dnn_space", "xgb_space"],
    "timing": ["lear_timing"],
}
ENGINE_L2 = {"lear": ["lear_design", "lear_day"], "arx": ["arx_day"], "gbm2": ["gbm_month"], "mlp2": ["mlp_design", "mlp_month"]}

FULL_PANEL = r'''# ---- full information set at gate closure (12:00 CET on d-1), as in lectures/L7/analysis_L7.py
from joblib import Parallel, delayed
GH = pd.read_csv(DATA + "generation_ro_mw_hourly_utc.csv", index_col=0)
LM, _ = day_matrix(GH["load"].dropna())
RM, _ = day_matrix((GH["wind_onshore"] + GH["solar"]).dropna())
L_, R_ = LM.reindex(CAL).values.astype(float), RM.reindex(CAL).values.astype(float)
G = pd.read_csv(DATA + "generation_ro_mw_daily_cet.csv", parse_dates=["date_cet"]).set_index("date_cet")
CB = pd.read_csv(DATA + "crossborder_ro_mw_daily_cet.csv", parse_dates=["date_cet"]).set_index("date_cet")
EUA = pd.read_csv(DATA + "eua_daily.csv", parse_dates=["date"]).set_index("date")["eua_etc_co2l_eur_per_unit"]
CAL_EX = pd.date_range(START - pd.Timedelta(days=30), END, freq="D")
FUND_RAW = pd.DataFrame({"hydro": (G["hydro_run_of_river"] + G["hydro_water_reservoir"]).reindex(CAL_EX),
                         "nuclear": G["nuclear"].reindex(CAL_EX), "netimp": CB["sum"].reindex(CAL_EX), "eua": EUA.reindex(CAL_EX)})
F_ = FUND_RAW.ffill().shift(2).reindex(CAL).values.astype(float)      # past only, lagged 2 days
MB = blocks_of(TDAYS, "M")                                           # 12 monthly refits in the test year
_vm = blocks_of(VDAYS, "M")
VB = [(_vm[k][0], _vm[k + 2][1]) for k in range(0, 12, 3)]           # validation year: 4 quarterly refits
FC = {}'''

PARTS = {
    "naive": 'FC["naive"] = np.array([P_[i - 7] if DOW[i] in (0, 5, 6) else P_[i - 1] for i in rows_all])   # Lecture 2 naive rule',
    "lear": '''def _aw_lear(i):
    return np.mean([lear_day(P_, L_, R_, i, T)[0] for T in LEAR_W], 0)
FC["aw_lear"] = np.array(Parallel(n_jobs=-1)(delayed(_aw_lear)(i) for i in rows_all))      # AW-LEAR (Lecture 2), daily recalibration''',
    "arx": '''def _aw_arx(i):
    return np.mean([arx_day(P_, L_, R_, F_, i, T)[0] for T in ARX_W], 0)
FC["aw_arx"] = np.array(Parallel(n_jobs=-1)(delayed(_aw_arx)(i) for i in rows_all))''',
    "gbm2": 'FC["gbm2"] = np.vstack([g[0] for g in Parallel(n_jobs=-1)(delayed(gbm_month)(P_, L_, R_, F_, a, b) for a, b in MB)])',
    "mlp2": 'FC["mlp2"] = np.vstack([g[0] for g in Parallel(n_jobs=-1)(delayed(mlp_month)(P_, L_, R_, F_, a, b) for a, b in MB)])',
    "dnn": '''res_dnn = Parallel(n_jobs=-1)(delayed(dnn_block)(P_, L_, R_, F_, a, b, CFG_DNN, (1, 2, 3, 4), keep=True) for a, b in MB)
FC["dnn"] = np.vstack([r["pred"] for r in res_dnn])                  # DNN, 4 seeds averaged, monthly refits''',
    "xgb": '''res_xgb = Parallel(n_jobs=-1)(delayed(xgb_block)(P_, L_, R_, F_, a, b, CFG_XGB, shap=True) for a, b in MB)
FC["xgb"] = np.vstack([r["pred"] for r in res_xgb])                  # XGBoost, monthly refits''',
    "chr2": '''# needs: pip install chronos-forecasting
chr2 = chronos_forecasts(P_, rows_all, "amazon/chronos-2")
FC["chr2"], FC["chr2_q10"], FC["chr2_q90"] = chr2["median"], chr2["q"][:, :, 0], chr2["q"][:, :, 2]''',
    "bolt": '''bolt = chronos_forecasts(P_, rows_all, "amazon/chronos-bolt-small")
FC["bolt"] = bolt["median"]''',
    "theta": '''MONTH_START = {}
for _t in CAL:
    MONTH_START.setdefault(_t.to_period("M"), _t.replace(day=1))
THETA = np.array([spike_threshold(MONTH_START[t.to_period("M")]) for t in CAL])''',
    "spike": '''res_sp = Parallel(n_jobs=-1)(delayed(clf_block)(P_, L_, R_, F_, THETA, a, b, "spike") for a, b in MB)
FC["spike_xgb"], FC["spike_logit"] = np.vstack([r["xgb"] for r in res_sp]), np.vstack([r["logit"] for r in res_sp])''',
    "neg": '''res_ng = Parallel(n_jobs=-1)(delayed(clf_block)(P_, L_, R_, F_, THETA, a, b, "neg") for a, b in MB)
FC["neg_xgb"], FC["neg_logit"] = np.vstack([r["xgb"] for r in res_ng]), np.vstack([r["logit"] for r in res_ng])''',
    "search": '''DNN_SPACE, XGB_SPACE = dnn_space(), xgb_space()
AV = P_[[IDX[t] for t in VDAYS]]
_jobs = [(c, b) for c in range(len(DNN_SPACE)) for b in VB]
_r = Parallel(n_jobs=-1)(delayed(dnn_block)(P_, L_, R_, F_, a, b_, DNN_SPACE[c]) for c, (a, b_) in _jobs)
FC["val_dnn"] = np.array([np.mean(np.abs(AV - np.vstack([_r[c * len(VB) + j]["pred"] for j in range(len(VB))]))) for c in range(len(DNN_SPACE))])
FC["sec_search"] = sum(x["sec"] for x in _r)
_jobs = [(c, b) for c in range(len(XGB_SPACE)) for b in VB]
_r = Parallel(n_jobs=-1)(delayed(xgb_block)(P_, L_, R_, F_, a, b_, XGB_SPACE[c]) for c, (a, b_) in _jobs)
FC["val_xgb"] = np.array([np.mean(np.abs(AV - np.vstack([_r[c * len(VB) + j]["pred"] for j in range(len(VB))]))) for c in range(len(XGB_SPACE))])
FC["sec_search"] += sum(x["sec"] for x in _r)''',
    "snoop": '''_jobs = [(c, b) for c in range(len(DNN_SPACE)) for b in MB]
_r = Parallel(n_jobs=-1)(delayed(dnn_block)(P_, L_, R_, F_, a, b_, DNN_SPACE[c]) for c, (a, b_) in _jobs)
FC["test_dnn"] = np.array([np.mean(np.abs(A - np.vstack([_r[c * len(MB) + j]["pred"] for j in range(len(MB))]))) for c in range(len(DNN_SPACE))])
_jobs = [(c, b) for c in range(len(XGB_SPACE)) for b in MB]
_r = Parallel(n_jobs=-1)(delayed(xgb_block)(P_, L_, R_, F_, a, b_, XGB_SPACE[c]) for c, (a, b_) in _jobs)
FC["test_xgb"] = np.array([np.mean(np.abs(A - np.vstack([_r[c * len(MB) + j]["pred"] for j in range(len(MB))]))) for c in range(len(XGB_SPACE))])''',
}


def engine_cell(ns, groups, l2=(), extra=""):
    cfg_dnn = {k: v for k, v in ns["CFG_DNN"].items() if k != "lr_s"}
    head = (f"import os\nimport time\n\n# constants of lectures/L7/analysis_L7.py\nSEED = {ns['SEED']}\n"
            "PLAGS, XLAGS = (1, 2, 3, 7), (2, 3, 7)            # price lags (days) and lags of load, wind+solar (>= 2 days)\n"
            f"XGB_NAMES = {ns['XGB_NAMES']!r}\n"
            f"# configurations chosen by random search on the validation year (Quantlet EMQA_L7_search)\n"
            f"CFG_DNN = {cfg_dnn!r}\nCFG_XGB = {ns['CFG_XGB']!r}\n")
    if "clf" in groups:
        head += f"THR_Q = 0.90\nCLF_NAMES = XGB_NAMES + [\"threshold\"]\nCLF_CFG = {ns['CLF_CFG']!r}\n"
    if "chronos" in groups:
        head += f"CTX = {ns['CTX']}                                     # context: the last 2048 hourly prices up to the end of d-1\n"
    if l2:
        head += ("SEED_L2 = 20261105                                # seed of Lecture 2\nARX_W, LEAR_W = (56, 84, 112, 714, 721, 728), (364, 546, 728)\n"
                 "GBM_NAMES = XGB_NAMES\n")
    names = [f for g in ["base"] + list(groups) for f in ENGINE_FUNCS[g]]
    body = source_of(A7, names)
    if l2:
        b2 = source_of(A2, [f for g in l2 for f in ENGINE_L2[g]]).replace("seed=SEED)", "seed=SEED_L2)")
        body += "\n\n\n# ---- benchmarks of Lecture 2 (lectures/L2/analysis_L2.py)\n" + b2
    return head + extra + "\n\n" + body


def runall_cell(parts, saved, load_keys_note=""):
    code = "\n".join([FULL_PANEL] + [PARTS[p] for p in parts])
    return ("if RUN_ALL:\n" + textwrap.indent(code, "    ") +
            f"\nelse:\n    FC = load_results(\"{saved}\")\n" +
            "    assert list(FC.get(\"days\", TDAYS.strftime(\"%Y-%m-%d\"))) == list(TDAYS.strftime(\"%Y-%m-%d\"))\n" +
            "print(sorted(k for k in FC if k != \"days\"))")


RUNALL_MD = ("## Model outputs: saved, or recomputed with `RUN_ALL = True`\n\n"
             "The models of this chart take {cost} to refit, more than a free Colab session allows. "
             "With `RUN_ALL = False` the notebook loads their saved outputs (`{saved}`, produced by `lectures/L7/analysis_L7.py`); "
             "with `RUN_ALL = True` it recomputes them from the data with the code below, which is the code of the lecture.")


# =============================================================================
# 3. The Quantlets
# =============================================================================
def build(ns):
    TD = ns["TDAYS"].strftime("%Y-%m-%d").to_numpy().astype("U10")
    M, C = ns["M"], ns["C"]
    period = {k: f"{v['period_en']}. Source: {v['source_en']}" for k, v in J["charts"].items()}
    D = J["design"]
    test = f"test year {D['test_start']} to {D['test_end']}"
    PRICES = "hourly Romanian day-ahead prices (OPCOM PZU, via energy-charts.info), data/clean/power_da_prices_hourly_utc.csv"
    Q = {}

    def fc(*keys, **extra):
        out = {"days": TD}
        for k in keys:
            out[k] = M[k]
        out.update(extra)
        return out

    # ------------------------------------------------------------------ 1 split_ml
    Q["split_ml"] = dict(
        title="Three samples in time order: training, validation, test",
        desc=("Daily base price of the Romanian day-ahead market with the three chronological samples of Lecture 7: training days from "
              f"{D['train_start']} (grows each month), the validation year {D['val_start']} to {D['val_end']} used only to choose "
              f"hyperparameters, and the {test} (as in Lecture 2), never used to choose anything."),
        kw="electricity price, day-ahead market, Romania, OPCOM, train validation test split, chronological split, machine learning, time series",
        data=PRICES, saved=None, needs_data=True,
        code=[("## Daily base price and the three samples", r'''DAILY = pd.Series(PM.mean(1).values, index=CAL)       # daily base price = mean of the 24 hourly prices
fig, ax = plt.subplots(figsize=(6.4, 2.1))
ax.axvspan(CAL[FIRST], VAL0 - pd.Timedelta(days=1), color=PAL["HU"], alpha=0.12, lw=0, label="training (grows each month)")
ax.axvspan(VAL0, TEST0 - pd.Timedelta(days=1), color=PAL["BG"], alpha=0.28, lw=0, label="validation year: choose hyperparameters")
ax.axvspan(TEST0, END, color=PAL["DE_LU"], alpha=0.2, lw=0, label="test year (as in Lecture 2)")
ax.plot(DAILY.index, DAILY.values, color=PAL["RO"], lw=0.8, label="Romania, daily base price")
ax.set_ylabel("EUR/MWh")
ax.set_xlim(CAL[0], END)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
legend_bottom(fig, ncol=2)
save_chart(fig, "split_ml", bottom=0.26)''')],
        checks=[("Training starts", "design.train_start", "", "str(CAL[FIRST].date())"),
                ("Training ends (search)", "design.train_end", "", "str((VAL0 - pd.Timedelta(days=1)).date())"),
                ("Validation year starts", "design.val_start", "", "str(VAL0.date())"),
                ("Validation year ends", "design.val_end", "", "str(VDAYS[-1].date())"),
                ("Test year starts", "design.test_start", "", "str(TEST0.date())"),
                ("Test year ends", "design.test_end", "", "str(END.date())"),
                ("Days in the panel", "data.n_days", "d", "len(CAL)")])

    # ------------------------------------------------------------------ 2 search
    Q["search"] = dict(
        title="Random search cuts the validation error of both models",
        desc=("Validation-year mean absolute error (MAE) of the 25 hyperparameter configurations (24 random + the Lecture 2 setting) "
              "of the deep neural network (DNN) and of XGBoost, sorted, with the chosen configuration, the Lecture 2 setting and the "
              f"naive benchmark. Romanian day-ahead prices, validation year {D['val_start']} to {D['val_end']}, quarterly refits."),
        kw="random search, hyperparameter tuning, validation, neural network, XGBoost, gradient boosting, electricity price forecasting, MAE",
        data=PRICES + "; saved validation MAE of the 25 configurations of each model (search_results.npz, from lectures/L7/cache/ml.pkl); "
             "RUN_ALL also uses load, wind and solar generation, hydro, nuclear, net imports and the EUA price from data/clean",
        saved={"val_dnn": ns["VAL_DNN"], "val_xgb": ns["VAL_XGB"], "sec_search": np.array(ns["sec"]["search"])},
        cost="about 2 hours on 16 cores (25 configurations x 2 models x 4 refits)",
        engine=(["dnn", "xgb", "space"], ()), parts=["search"],
        pre=r'''# naive benchmark on the validation year (Lecture 2 rule: Monday, Saturday, Sunday use d-7, other days d-1)
vr = np.array([IDX[t] for t in VDAYS])
AV = P_[vr]
naive_val = np.mean(np.abs(AV - np.where(np.isin(DOW[vr], [0, 5, 6])[:, None], P_[vr - 7], P_[vr - 1])))''',
        code=[("## Validation MAE of every configuration", r'''VAL_DNN, VAL_XGB = FC["val_dnn"], FC["val_xgb"]
BEST_DNN, BEST_XGB = int(np.argmin(VAL_DNN)), int(np.argmin(VAL_XGB))     # chosen: lowest validation MAE
fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2), sharey=True)
for ax, V, best_, nm in [(axs[0], VAL_DNN, BEST_DNN, "DNN"), (axs[1], VAL_XGB, BEST_XGB, "XGBoost")]:
    o = np.argsort(V)
    ax.plot(range(1, len(V) + 1), V[o], "o", color="#9a9a9a", ms=4, label="one configuration")
    ax.plot([1], [V[best_]], "o", color=PAL["DE_LU"], ms=7, label="chosen (lowest validation MAE)")
    r0 = int(np.where(o == 0)[0][0]) + 1
    ax.plot([r0], [V[0]], "s", color=PAL["RO"], ms=6, label="setting of Lecture 2")
    ax.axhline(naive_val, color="#222222", ls=":", lw=1.0, label="naive, validation year")
    ax.set_title(nm, fontsize=10)
    ax.set_xlabel("rank on the validation year", fontsize=9.5)
axs[0].set_ylabel("MAE, validation\nyear (EUR/MWh)", fontsize=9.5)
legend_bottom(fig, ncol=2)
save_chart(fig, "search", bottom=0.27)''')],
        checks=[("Configurations per model", "search.n_cfg", "d", "len(VAL_DNN)"),
                ("DNN: chosen configuration", "search.dnn.best", "d", "BEST_DNN"),
                ("DNN: best validation MAE", "search.dnn.val_best", ".2f", "VAL_DNN.min()"),
                ("DNN: Lecture 2 setting, validation MAE", "search.dnn.val_l2", ".2f", "VAL_DNN[0]"),
                ("DNN: rank of the Lecture 2 setting", "search.dnn.rank_l2", "d", "int((VAL_DNN < VAL_DNN[0]).sum() + 1)"),
                ("XGBoost: chosen configuration", "search.xgb.best", "d", "BEST_XGB"),
                ("XGBoost: best validation MAE", "search.xgb.val_best", ".2f", "VAL_XGB.min()"),
                ("XGBoost: Lecture 2 setting, validation MAE", "search.xgb.val_l2", ".2f", "VAL_XGB[0]"),
                ("XGBoost: rank of the Lecture 2 setting", "search.xgb.rank_l2", "d", "int((VAL_XGB < VAL_XGB[0]).sum() + 1)"),
                ("Naive model, validation MAE", "search.naive_val", ".2f", "naive_val")])

    # ------------------------------------------------------------------ 3 learning_curve
    cv = ns["_curve"]
    Q["learning_curve"] = dict(
        title="Early stopping: stop when the error on recent days stops falling",
        desc=("Learning curves of the chosen deep neural network (DNN), refit for the last test month "
              f"({J['curve']['month']}, seed 1): MAE in EUR/MWh on the first 85% of the training days and on the last 15% "
              "(chronological early-stopping block), by epoch, with the epoch kept. Romanian day-ahead prices from "
              f"{D['train_start']} to {J['design']['test_end'][:7]}-01 (training sample of that refit)."),
        kw="early stopping, learning curve, overfitting, neural network, epochs, electricity price forecasting, Romania",
        data=PRICES + "; saved learning curves of the chosen DNN (learning_curve_results.npz, from lectures/L7/cache/ml.pkl)",
        saved={"curve_train": np.array(cv[0]), "curve_val": np.array(cv[1])},
        cost="about 10 minutes on one core (one refit of the network with early stopping)",
        engine=(["dnn"], ()), parts=[],
        runall_extra='''_r = dnn_block(P_, L_, R_, F_, MB[-1][0], MB[-1][1], CFG_DNN, (1,), keep=True)
FC["curve_train"], FC["curve_val"] = np.array(_r["curves"][0][0]), np.array(_r["curves"][0][1])''',
        code=[("## Training and early-stopping error by epoch", r'''ctr, cvl = FC["curve_train"], FC["curve_val"]
best_ep = int(np.argmin(cvl) + 1)
fig, ax = plt.subplots(figsize=(6.4, 1.95))
ee = np.arange(1, len(ctr) + 1)
ax.plot(ee, ctr, color=PAL["RO"], label="training days (first 85%)")
ax.plot(ee, cvl, color=PAL["DE_LU"], label="early-stopping block (last 15%)")
ax.axvline(best_ep, color="#222222", ls="--", lw=0.9, label="epoch kept")
ax.set_xlabel("epoch (one pass over the training days)")
ax.set_ylabel("MAE, EUR/MWh")
legend_bottom(fig, ncol=3)
save_chart(fig, "learning_curve", bottom=0.22)''')],
        checks=[("Refit for month", "curve.month", "", "str(TDAYS[-1].to_period('M'))"),
                ("Epoch kept (lowest early-stopping MAE)", "curve.best_ep", "d", "best_ep"),
                ("Epochs run (patience 25)", "curve.n_ep", "d", "len(cvl)"),
                ("Lowest early-stopping MAE, EUR/MWh", "curve.v_best", ".2f", "cvl.min()"),
                ("Training MAE at the last epoch", "curve.tr_end", ".2f", "ctr[-1]"),
                ("Early-stopping MAE at the last epoch", "curve.v_end", ".2f", "cvl[-1]")])

    # ------------------------------------------------------------------ 4 monthly_ml
    MAEFN = "def mae(F):\n    return np.mean(np.abs(A - F))"
    Q["monthly_ml"] = dict(
        title="Month by month, the combination beats AW-LEAR",
        desc=("Monthly mean absolute error (MAE, EUR/MWh) of AW-LEAR (Lecture 2 benchmark), the tuned XGBoost, the tuned deep neural network "
              f"(DNN) and their equal-weight combination LEAR+DNN+XGBoost on the Romanian day-ahead prices, {test}, monthly refits."),
        kw="forecast combination, ensemble, LEAR, XGBoost, neural network, MAE by month, electricity price forecasting, Romania",
        data=PRICES + "; saved test-year forecasts of AW-LEAR, XGBoost and the DNN (monthly_ml_results.npz, from lectures/L2/cache/forecasts.pkl and lectures/L7/cache/ml.pkl)",
        saved=fc("aw_lear", "xgb", "dnn"),
        cost="several hours on one core (AW-LEAR: 365 days x 3 windows x 24 LASSO paths; DNN: 12 refits x 4 seeds)",
        engine=(["dnn", "xgb"], ("lear",)), parts=["lear", "dnn", "xgb"],
        code=[("## Monthly MAE", MAEFN + r'''


M = {k: FC[k] for k in ["aw_lear", "xgb", "dnn"]}
M["ens_ldx"] = (M["aw_lear"] + M["dnn"] + M["xgb"]) / 3             # equal weights, fixed in advance
TM = TDAYS.to_period("M")
MONTHS_T = sorted(set(TM))
BYMONTH = {k: np.array([np.mean(np.abs(A[TM == mm] - M[k][TM == mm])) for mm in MONTHS_T]) for k in M}
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
xm = [pd.Timestamp(str(mm)) for mm in MONTHS_T]
fig, ax = plt.subplots(figsize=(6.4, 1.95))
for k, ls, mk in [("aw_lear", "-", "o"), ("xgb", "--", "s"), ("dnn", "-.", "^"), ("ens_ldx", "-", "D")]:
    ax.plot(xm, BYMONTH[k], color=COL[k], ls=ls, marker=mk, ms=3.5, lw=1.6 if k == "ens_ldx" else 1.1, label=LAB[k])
ax.set_ylabel("MAE, EUR/MWh")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: MON[mdates.num2date(v).month - 1] +
                                               (f"\n{mdates.num2date(v).year}" if mdates.num2date(v).month == 1 else "")))
legend_bottom(fig, ncol=4)
save_chart(fig, "monthly_ml", bottom=0.22)''')],
        checks=[("MAE AW-LEAR, EUR/MWh", "acc.aw_lear.mae", ".2f", "mae(M['aw_lear'])"),
                ("MAE XGBoost", "acc.xgb.mae", ".2f", "mae(M['xgb'])"),
                ("MAE DNN", "acc.dnn.mae", ".2f", "mae(M['dnn'])"),
                ("MAE LEAR+DNN+XGBoost", "acc.ens_ldx.mae", ".2f", "mae(M['ens_ldx'])"),
                ("Months XGBoost beats AW-LEAR", "bymonth.n_xgb_beats_lear", "d", "int((BYMONTH['xgb'] < BYMONTH['aw_lear']).sum())"),
                ("Months DNN beats AW-LEAR", "bymonth.n_dnn_beats_lear", "d", "int((BYMONTH['dnn'] < BYMONTH['aw_lear']).sum())"),
                ("Months the combination beats AW-LEAR", "bymonth.n_ldx_beats_lear", "d", "int((BYMONTH['ens_ldx'] < BYMONTH['aw_lear']).sum())"),
                ("Worst month of AW-LEAR", "bymonth.worst_month", "", "str(MONTHS_T[int(np.argmax(BYMONTH['aw_lear']))])")])

    # ------------------------------------------------------------------ 5 dm_matrix
    Q["dm_matrix"] = dict(
        title="DM tests: combinations with ML beat AW-LEAR significantly",
        desc=("Matrix of one-sided Diebold-Mariano (DM) p-values (H1: the column model is more accurate than the row model; loss = daily "
              "mean absolute error; Newey-West variance, 7 lags) for 11 forecasts of the Romanian day-ahead price: naive, AW-LEAR, the "
              "Lecture 2 ensemble, XGBoost, DNN, Chronos-Bolt, Chronos-2 and four combinations; "
              f"{test}, 365 days."),
        kw="Diebold-Mariano test, forecast evaluation, forecast combination, LEAR, XGBoost, neural network, Chronos, foundation model, electricity price",
        data=PRICES + "; saved test-year forecasts of naive, AW-ARX, AW-LEAR, GBM and MLP of Lecture 2, XGBoost, DNN, Chronos-Bolt and Chronos-2 (dm_matrix_results.npz)",
        saved=fc("naive", "aw_arx", "aw_lear", "gbm2", "mlp2", "xgb", "dnn", "bolt", "chr2"),
        cost="several hours on one core (all benchmarks of Lecture 2, the DNN, XGBoost and two foundation models)",
        engine=(["dnn", "xgb", "chronos"], ("lear", "arx", "gbm2", "mlp2")),
        parts=["naive", "lear", "arx", "gbm2", "mlp2", "dnn", "xgb", "chr2", "bolt"],
        code=[("## Combinations and Diebold-Mariano tests", MAEFN + "\n\n\n" + DM + r'''


M = dict(FC)
M["ens4"] = np.mean([M["aw_arx"], M["aw_lear"], M["gbm2"], M["mlp2"]], 0)       # ensemble of 4 of Lecture 2
M["ens_ldx"] = (M["aw_lear"] + M["dnn"] + M["xgb"]) / 3
M["ens_t4"] = np.mean([M["aw_arx"], M["aw_lear"], M["dnn"], M["xgb"]], 0)
M["ens_lc"] = 0.5 * (M["aw_lear"] + M["chr2"])
M["ens_t5"] = np.mean([M["aw_arx"], M["aw_lear"], M["dnn"], M["xgb"], M["chr2"]], 0)
E = {k: A - v for k, v in M.items() if k != "days"}
DM_MODELS = ["naive", "aw_lear", "ens4", "xgb", "dnn", "bolt", "chr2", "ens_ldx", "ens_t4", "ens_lc", "ens_t5"]
DMP = np.full((len(DM_MODELS), len(DM_MODELS)), np.nan)
for a_, ka in enumerate(DM_MODELS):
    for b_, kb in enumerate(DM_MODELS):
        if a_ != b_:
            DMP[a_, b_] = dm(E[ka], E[kb])[1]''' + "\n\n" + r'''from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list("dm", ["#0b6e2e", "#7fc97f", "#ffe08a", "#f4a259", "#d7301f", "#5a0000"])
fig, ax = plt.subplots(figsize=(6.4, 2.75))
Z = np.where(np.isnan(DMP), np.nan, np.minimum(DMP, 0.10))
im = ax.imshow(np.ma.masked_invalid(Z), cmap=cmap, vmin=0, vmax=0.10, aspect="auto")
ax.set_xticks(range(len(DM_MODELS)))
ax.set_xticklabels([LAB[k] for k in DM_MODELS], rotation=35, ha="right", fontsize=8.5)
ax.set_yticks(range(len(DM_MODELS)))
ax.set_yticklabels([LAB[k] for k in DM_MODELS], fontsize=8.5)
ax.set_xlabel("is the column model more accurate than the row model?", fontsize=9.5)
for a_ in range(len(DM_MODELS)):
    ax.add_patch(plt.Rectangle((a_ - 0.5, a_ - 0.5), 1, 1, color="#ffffff"))
cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
cb.set_label("p-value, capped at 0.10", fontsize=9)
ax.spines[:].set_visible(False)
save_chart(fig, "dm_matrix", bottom=0.0)''')],
        checks=[("DM p-value, AW-LEAR vs LEAR+DNN+XGBoost", "dm.aw_lear__ens_ldx.p", ".4f", "dm(E['aw_lear'], E['ens_ldx'])[1]"),
                ("MAE AW-ARX + AW-LEAR + DNN + XGBoost", "acc.ens_t4.mae", ".2f", "mae(M['ens_t4'])"),
                ("DM p-value, ensemble of 4 (L2) vs tuned ensemble of 4", "dm.ens4__ens_t4.p", ".4f", "dm(E['ens4'], E['ens_t4'])[1]"),
                ("DM p-value, Chronos-2 vs LEAR+Chronos-2", "dm.chr2__ens_lc.p", ".4f", "dm(E['chr2'], E['ens_lc'])[1]"),
                ("Models significantly better than AW-LEAR (5%)", "dm.n_beat_lear", "d",
                 "int(sum(DMP[DM_MODELS.index('aw_lear'), j] < 0.05 for j in range(len(DM_MODELS))))")])

    # ------------------------------------------------------------------ 6 combo_weight
    Q["combo_weight"] = dict(
        title="Averaging works because the errors are not identical",
        desc=("Mean absolute error of the combination w x (machine-learning forecast) + (1 - w) x AW-LEAR for w from 0 to 1, with XGBoost "
              "and with the DNN, and the equal-weight point actually used. Illustration only: the weight is not chosen on the test year. "
              f"Romanian day-ahead prices, {test}."),
        kw="forecast combination, combination weight, error correlation, Bates and Granger, LEAR, XGBoost, neural network, electricity price",
        data=PRICES + "; saved test-year forecasts of AW-LEAR, XGBoost and the DNN (combo_weight_results.npz)",
        saved=fc("aw_lear", "xgb", "dnn"),
        cost="several hours on one core (AW-LEAR, DNN with 4 seeds, XGBoost; 12 monthly refits)",
        engine=(["dnn", "xgb"], ("lear",)), parts=["lear", "dnn", "xgb"],
        code=[("## Error correlation and MAE as a function of the weight", r'''M = {k: FC[k] for k in ["aw_lear", "xgb", "dnn"]}
E = {k: A - v for k, v in M.items()}
corr = {k: np.corrcoef(E["aw_lear"].ravel(), E[k].ravel())[0, 1] for k in ["dnn", "xgb"]}
WGRID = np.linspace(0, 1, 21)
WCURVE = {k: np.array([np.mean(np.abs(A - (w * M[k] + (1 - w) * M["aw_lear"]))) for w in WGRID]) for k in ["dnn", "xgb"]}
fig, ax = plt.subplots(figsize=(6.4, 1.95))
for k, ls in [("xgb", "-"), ("dnn", "--")]:
    ax.plot(WGRID, WCURVE[k], color=COL[k], ls=ls, label=f"AW-LEAR and {LAB[k]}")
ax.plot([0.5, 0.5], [WCURVE["xgb"][10], WCURVE["dnn"][10]], "o", color="#222222", ms=4, label="equal weights (used)")
ax.set_xlabel("weight w of the machine-learning model")
ax.set_ylabel("MAE, EUR/MWh")
legend_bottom(fig, ncol=3)
save_chart(fig, "combo_weight", bottom=0.22)''')],
        checks=[("Error correlation AW-LEAR vs DNN", "combo.corr.dnn", ".2f", "corr['dnn']"),
                ("Error correlation AW-LEAR vs XGBoost", "combo.corr.xgb", ".2f", "corr['xgb']"),
                ("Best weight seen afterwards, XGBoost", "combo.w_best_xgb", ".2f", "WGRID[np.argmin(WCURVE['xgb'])]"),
                ("Best weight seen afterwards, DNN", "combo.w_best_dnn", ".2f", "WGRID[np.argmin(WCURVE['dnn'])]"),
                ("MAE at that weight, XGBoost", "combo.mae_wbest_xgb", ".2f", "WCURVE['xgb'].min()")])

    # ------------------------------------------------------------------ 7 cost_gain
    sec = ns["sec"]
    Q["cost_gain"] = dict(
        title="Compute cost: daily LEAR is the expensive model, ML costs minutes",
        desc=("Compute time for the whole test year (minutes on one core, log scale) against the mean absolute error of AW-LEAR, XGBoost, "
              "the DNN, Chronos-Bolt, Chronos-2 and two combinations; times measured on one core of the author's 18-core laptop. "
              f"Romanian day-ahead prices, {test}."),
        kw="compute cost, forecast accuracy, LEAR, XGBoost, neural network, Chronos, foundation model, total cost of ownership",
        data=PRICES + "; saved test-year forecasts and measured compute times of each model (cost_gain_results.npz)",
        saved=fc("aw_lear", "xgb", "dnn", "bolt", "chr2", sec_aw_lear=np.array(sec["aw_lear"]), sec_xgb=np.array(sec["xgb"]),
                 sec_dnn=np.array(sec["dnn"]), sec_bolt=np.array(sec["bolt"]), sec_chr2=np.array(sec["chr2"]), sec_search=np.array(sec["search"])),
        cost="several hours on one core (the timing is part of the result)",
        engine=(["dnn", "xgb", "chronos", "space", "timing"], ("lear",)), parts=["lear", "dnn", "xgb", "chr2", "bolt", "search"],
        runall_extra='''FC["sec_aw_lear"] = lear_timing() * len(TDAYS)                      # 8 days timed, scaled to the year
FC["sec_xgb"], FC["sec_dnn"] = sum(r["sec"] for r in res_xgb), sum(r["sec"] for r in res_dnn)
FC["sec_chr2"], FC["sec_bolt"] = chr2["sec"], bolt["sec"]''',
        code=[("## Minutes of compute against accuracy", MAEFN + r'''


M = {k: FC[k] for k in ["aw_lear", "xgb", "dnn", "bolt", "chr2"]}
M["ens_ldx"] = (M["aw_lear"] + M["dnn"] + M["xgb"]) / 3
M["ens_lc"] = 0.5 * (M["aw_lear"] + M["chr2"])
sec = {k: float(FC["sec_" + k]) for k in ["aw_lear", "xgb", "dnn", "bolt", "chr2", "search"]}
sec["ens_ldx"] = sec["aw_lear"] + sec["xgb"] + sec["dnn"]
sec["ens_lc"] = sec["aw_lear"] + sec["chr2"]
fig, ax = plt.subplots(figsize=(6.4, 2.2))
for k in ["aw_lear", "xgb", "dnn", "bolt", "chr2", "ens_ldx", "ens_lc"]:
    ax.plot(max(sec[k], 1) / 60, mae(M[k]), "o", color=COL[k], ms=6)
    off = {"aw_lear": (6, 4), "ens_ldx": (6, -2), "ens_lc": (6, -9), "xgb": (6, 2), "dnn": (6, -9), "bolt": (6, 2), "chr2": (6, -9)}[k]
    ax.annotate(LAB[k], (max(sec[k], 1) / 60, mae(M[k])), textcoords="offset points", xytext=off, fontsize=8)
ax.set_xscale("log")
ax.set_xlabel("compute time for the test year, minutes on one core (log scale)", fontsize=9.5)
ax.set_ylabel("MAE, EUR/MWh")
xl = ax.get_xlim()
ax.set_xlim(xl[0], xl[1] * 4)
save_chart(fig, "cost_gain", bottom=0.02)''')],
        checks=[("AW-LEAR, minutes", "cost.aw_lear", ".1f", "sec['aw_lear'] / 60"),
                ("XGBoost, minutes", "cost.xgb", ".1f", "sec['xgb'] / 60"),
                ("DNN, minutes", "cost.dnn", ".1f", "sec['dnn'] / 60"),
                ("Chronos-2, minutes", "cost.chr2", ".1f", "sec['chr2'] / 60"),
                ("Chronos-Bolt, minutes", "cost.bolt", ".1f", "sec['bolt'] / 60"),
                ("Hyperparameter search, minutes", "cost.search", ".1f", "sec['search'] / 60"),
                ("MAE AW-LEAR", "acc.aw_lear.mae", ".2f", "mae(M['aw_lear'])"),
                ("MAE Chronos-2", "acc.chr2.mae", ".2f", "mae(M['chr2'])"),
                ("MAE LEAR+DNN+XGBoost", "acc.ens_ldx.mae", ".2f", "mae(M['ens_ldx'])")])

    # ------------------------------------------------------------------ 8 shap_global
    SH = ns["SH"]
    xgb_runall = '''SH = np.concatenate([r["shap"] for r in res_xgb], 0)       # exact SHAP values, 365 days x 24 hours x (20 features + bias)
XS = np.concatenate([r["X"] for r in res_xgb], 0)'''
    Q["shap_global"] = dict(
        title="What drives the trees: yesterday's price at the same hour",
        desc=("Share of the mean absolute SHAP value of the 10 most important of the 20 inputs of the tuned XGBoost model, coloured by "
              "group (prices, load, wind+solar, other fundamentals, calendar); exact tree SHAP values on the "
              f"{test}, 8760 hours, XGBoost refitted monthly, Romanian day-ahead prices."),
        kw="SHAP, Shapley values, explainable AI, feature importance, XGBoost, gradient boosting, electricity price forecasting, Romania",
        data="saved exact SHAP values of the tuned XGBoost on the test year (shap_global_results.npz, from lectures/L7/cache/ml.pkl); "
             "RUN_ALL recomputes them from data/clean (prices, load, wind and solar, hydro, nuclear, net imports, EUA)",
        saved={"days": TD, "shap": SH[:, :, :-1]},
        cost="about 30 minutes on one core (12 monthly refits of XGBoost with 1500 trees)",
        engine=(["xgb"], ()), parts=["xgb"], runall_extra=xgb_runall + '\nFC["shap"] = SH[:, :, :-1]',
        code=[("## Share of the mean |SHAP value| by input", FNAME + r'''


SHV = FC["shap"]                                                     # 365 x 24 x 20 (asinh scale of the price)
mabs = np.abs(SHV).reshape(-1, len(XGB_NAMES)).mean(0)
share = mabs / mabs.sum() * 100
GROUPS = {"price": [0, 1, 2, 3, 4, 5, 6, 7], "load": [8, 9, 12], "res": [10, 11, 13], "fund": [14, 15, 16, 17], "cal": [18, 19]}
GCOL = {"price": PAL["RO"], "load": "#222222", "res": PAL["BG"], "fund": PAL["HU"], "cal": "#9a9a9a"}
top = np.argsort(-share)
fig, ax = plt.subplots(figsize=(6.4, 2.2))
o = top[:10][::-1]
gof = {j: g for g, ix in GROUPS.items() for j in ix}
ax.barh(range(len(o)), share[o], color=[GCOL[gof[j]] for j in o], height=0.7)
ax.set_yticks(range(len(o)))
ax.set_yticklabels([FNAME[XGB_NAMES[j]] for j in o], fontsize=8.5)
ax.set_xlabel("share of the mean |SHAP value|, %", fontsize=9.5)
from matplotlib.patches import Patch
hnd = [Patch(color=GCOL[g], label=lb) for g, lb in [("price", "prices"), ("load", "load"), ("res", "wind+solar"),
                                                    ("fund", "other fundamentals"), ("cal", "calendar")]]
legend_bottom(fig, handles=hnd, labels=[h_.get_label() for h_ in hnd], ncol=5)
save_chart(fig, "shap_global", bottom=0.12)''')],
        checks=[("Input 1", "shap.top.0", "", "XGB_NAMES[top[0]]"), ("Input 1, share %", "shap.top_share.0", ".1f", "share[top[0]]"),
                ("Input 2", "shap.top.1", "", "XGB_NAMES[top[1]]"), ("Input 2, share %", "shap.top_share.1", ".1f", "share[top[1]]"),
                ("Input 3", "shap.top.2", "", "XGB_NAMES[top[2]]"), ("Input 3, share %", "shap.top_share.2", ".1f", "share[top[2]]"),
                ("Group prices, %", "shap.groups.price", ".1f", "share[GROUPS['price']].sum()"),
                ("Group load, %", "shap.groups.load", ".1f", "share[GROUPS['load']].sum()"),
                ("Group wind+solar, %", "shap.groups.res", ".1f", "share[GROUPS['res']].sum()"),
                ("Group other fundamentals, %", "shap.groups.fund", ".1f", "share[GROUPS['fund']].sum()"),
                ("Group calendar, %", "shap.groups.cal", ".1f", "share[GROUPS['cal']].sum()")])

    # ------------------------------------------------------------------ 9 shap_res
    rj = ns["res_j"]
    Q["shap_res"] = dict(
        title="Wind and solar lower the price only in the hours when they are large",
        desc=("SHAP dependence plot of the input wind+solar generation on d-2 at the same hour in the tuned XGBoost model: one point per test "
              "hour, SHAP value (asinh price scale) against the generation in GW, sunny hours 09-16 highlighted; "
              f"{test}, 8760 hours, Romania."),
        kw="SHAP dependence, explainable AI, wind and solar, renewable generation, merit order effect, XGBoost, electricity price, Romania",
        data="saved input values and SHAP values of wind+solar d-2 for the 8760 test hours (shap_res_results.npz, from lectures/L7/cache/ml.pkl); "
             "RUN_ALL recomputes them from data/clean",
        saved={"days": TD, "x_res": ns["XS"][:, :, rj], "shap_res": SH[:, :, rj]},
        cost="about 30 minutes on one core (12 monthly refits of XGBoost with 1500 trees)",
        engine=(["xgb"], ()), parts=["xgb"],
        runall_extra=xgb_runall + '\n_j = XGB_NAMES.index("RES(d-2,h)")\nFC["x_res"], FC["shap_res"] = XS[:, :, _j], SH[:, :, _j]',
        code=[("## SHAP value of wind+solar d-2 against its level", r'''xr, sr = FC["x_res"], FC["shap_res"]
fig, ax = plt.subplots(figsize=(6.4, 2.0))
day_h = np.zeros_like(xr, bool)
day_h[:, 9:17] = True
for msk, c, lb in [(~day_h, "#5b6fa8", "hours 17-08"), (day_h, PAL["BG"], "hours 09-16 (sun)")]:
    ax.scatter(xr[msk] / 1000, sr[msk], s=1.2, alpha=0.35, color=c, lw=0, label=lb, rasterized=True)
ax.axhline(0, color="#222222", lw=0.6)
ax.set_xlabel("wind+solar on d-2, same hour (GW)")
ax.set_ylabel("SHAP value\n(asinh scale)", fontsize=9.5)
legend_bottom(fig, ncol=2)
for lh in fig.legends[0].legend_handles:
    lh.set_sizes([20])
    lh.set_alpha(1)
save_chart(fig, "shap_res", bottom=0.22)''')],
        checks=[("Correlation of wind+solar d-2 with its SHAP value", "shap.res_corr", ".2f", "np.corrcoef(xr.ravel(), sr.ravel())[0, 1]")])

    # ------------------------------------------------------------------ 10 perm_dnn
    PI = ns["PI"]
    Q["perm_dnn"] = dict(
        title="The neural network relies even more on yesterday's prices",
        desc=("Permutation importance of the input blocks of the tuned deep neural network (DNN): increase in the test-year MAE (EUR/MWh) "
              "when one block (prices of d-1, d-2, d-3, d-7, load, wind+solar, fundamentals, day of week) is shuffled across the test days; "
              f"mean of 5 random permutations, {test}, Romanian day-ahead prices."),
        kw="permutation importance, explainable AI, neural network, feature importance, electricity price forecasting, Romania",
        data="saved permutation importance of each input block (perm_dnn_results.npz, computed by lectures/L7/analysis_L7.py with the 48 "
             "trained networks of the test year); RUN_ALL retrains the networks from data/clean and recomputes it",
        saved={"block": np.array(list(PI.keys()), dtype="U20"), "increase": np.array(list(PI.values()))},
        cost="about 2 hours on one core (12 monthly refits x 4 seeds of the DNN, then 5 permutations x 8 blocks)",
        engine=(["dnn"], ()), parts=["dnn"],
        runall_extra=r'''A_DNN = FC["dnn"]
BLOCKS_DNN = ["price d-1", "price d-2", "price d-3", "price d-7", "load", "wind+solar", "fund", "day of week"]
rng = np.random.default_rng(SEED)
perms = [rng.permutation(len(TDAYS)) for _ in range(5)]
names0 = res_dnn[0]["names"]
blk_cols = {b: np.where(np.isin(names0, ["hydro", "nuclear", "net imports", "carbon"] if b == "fund" else [b]))[0] for b in BLOCKS_DNN}
blk_cols = {b: c for b, c in blk_cols.items() if len(c)}
XM = [dnn_inputs(P_, L_, R_, F_, rows_all, r_["sc"], CFG_DNN)[0] for r_ in res_dnn]
def perm_mae(b, pm):
    out = []
    for j, (a_, b_) in enumerate(MB):
        X = XM[j].copy()
        X[:, blk_cols[b]] = XM[j][pm][:, blk_cols[b]]
        sl = slice(a_ - MB[0][0], b_ - MB[0][0] + 1)
        out.append(dnn_predict_from(res_dnn[j]["models"], CFG_DNN, X[sl], res_dnn[j]["mu"], res_dnn[j]["sg"], res_dnn[j]["sc"]))
    return np.mean(np.abs(A - np.vstack(out)))
_base = np.mean(np.abs(A - A_DNN))
FC["block"] = np.array(list(blk_cols))
FC["increase"] = np.array([np.mean([perm_mae(b, pm) for pm in perms]) - _base for b in blk_cols])''',
        code=[("## Increase in MAE when a block is shuffled", r'''PI = dict(zip(FC["block"], FC["increase"]))
BNAME = {"price d-1": "prices d-1", "price d-2": "prices d-2", "price d-3": "prices d-3", "price d-7": "prices d-7",
         "load": "load d-2, d-3, d-7", "wind+solar": "wind+solar d-2, d-3, d-7", "fund": "hydro, nuclear, imports, carbon",
         "day of week": "day of week"}
fig, ax = plt.subplots(figsize=(6.4, 2.0))
bl = sorted(PI, key=PI.get)
ax.barh(range(len(bl)), [PI[b] for b in bl], height=0.65,
        color=[PAL["RO"] if b.startswith("price") else (PAL["BG"] if b == "wind+solar" else ("#222222" if b == "load" else
               (PAL["HU"] if b == "fund" else "#9a9a9a"))) for b in bl])
ax.set_yticks(range(len(bl)))
ax.set_yticklabels([BNAME[b] for b in bl], fontsize=8.5)
ax.set_xlabel("increase in MAE when the block is shuffled, EUR/MWh", fontsize=9.5)
save_chart(fig, "perm_dnn", bottom=0.02)''')],
        checks=[("Prices d-1, EUR/MWh", "perm.price_d1", ".2f", "PI['price d-1']"),
                ("Prices d-7", "perm.price_d7", ".2f", "PI['price d-7']"),
                ("Day of week", "perm.day_of_week", ".2f", "PI['day of week']"),
                ("Load", "perm.load", ".2f", "PI['load']"),
                ("Wind+solar", "perm.wind_solar", "+.2f", "PI['wind+solar']"),
                ("Most important block", "perm.top", "", "max(PI, key=PI.get)")])

    # ------------------------------------------------------------------ 11 events_hour
    Q["events_hour"] = dict(
        title="Spikes come in the evening, negative prices at midday",
        desc=("Share of test days with a price spike (price above the 90th percentile of the hourly prices of the 12 months before the "
              "delivery month) and with a price <= 0, by hour of the day (CET), Romanian day-ahead market, "
              f"{test}."),
        kw="price spikes, negative prices, intraday profile, day-ahead market, Romania, OPCOM, battery storage, extreme prices",
        data=PRICES + " (since 2015, for the rolling spike thresholds)", saved=None,
        code=[("## Spike threshold and events by hour", THRESH + r'''


h24 = np.arange(24)
fig, ax = plt.subplots(figsize=(6.4, 1.9))
ax.bar(h24 - 0.2, Y_SP.mean(0) * 100, width=0.4, color=PAL["c8"], label="spike: price above the 90th percentile of the last 12 months")
ax.bar(h24 + 0.2, Y_NG.mean(0) * 100, width=0.4, color=PAL["HU"], label="price $\\leq$ 0")
ax.set_xticks(range(0, 24, 2))
ax.set_xlabel("hour h (CET)")
ax.set_ylabel("% of test days")
legend_bottom(fig, ncol=1)
save_chart(fig, "events_hour", bottom=0.26)''')],
        checks=[("Lowest monthly threshold, EUR/MWh", "spike.theta_min", ".1f", "TH_T.min()"),
                ("Highest monthly threshold, EUR/MWh", "spike.theta_max", ".1f", "TH_T.max()"),
                ("Spike hours, % of test hours", "spike.share_test", ".1f", "Y_SP.mean() * 100"),
                ("Spike hours", "spike.n_test", "d", "int(Y_SP.sum())"),
                ("Hour with most spikes", "spike.peak_h", "d", "int(np.argmax(Y_SP.mean(0)))"),
                ("Share of days with a spike at that hour, %", "spike.peak_h_share", ".1f", "Y_SP.mean(0).max() * 100"),
                ("Hours with price <= 0", "neg.n_test", "d", "int(Y_NG.sum())"),
                ("Days with a price <= 0", "neg.n_days", "d", "int(Y_NG.any(1).sum())"),
                ("Hour with most prices <= 0", "neg.peak_h", "d", "int(np.argmax(Y_NG.mean(0)))")])

    # ------------------------------------------------------------------ 12 roc
    CS, CN = ns["CS"], ns["CN"]
    PERSIST = r'''past = np.stack([P_[rows_all - k] for k in range(1, 8)], 0)           # prices of d-1 ... d-7, same hour
CS = {"xgb": FC["spike_xgb"], "logit": FC["spike_logit"], "persist": (past > TH_T[None, :, None]).mean(0),
      "lear": FC["aw_lear"] - TH_T[:, None]}                          # AW-LEAR: a score, not a probability'''
    Q["roc"] = dict(
        title="Persistence detects spikes, but not negative prices",
        desc=("Receiver operating characteristic (ROC) curves of four scores for price spikes and for prices <= 0: XGBoost and logistic "
              "classifiers refitted monthly, persistence (share of events at the same hour in the last 7 days) and the AW-LEAR point "
              f"forecast. Romanian day-ahead prices, {test}, 8760 hours."),
        kw="ROC curve, AUC, classification, price spikes, negative prices, XGBoost, logistic regression, persistence, electricity price",
        data=PRICES + "; saved test-year probabilities of the XGBoost and logistic classifiers and the AW-LEAR forecasts (roc_results.npz)",
        saved={"days": TD, "spike_xgb": CS["xgb"], "spike_logit": CS["logit"], "neg_xgb": CN["xgb"], "neg_logit": CN["logit"], "aw_lear": M["aw_lear"]},
        cost="several hours on one core (AW-LEAR; 24 classifier refits)",
        engine=(["xgb", "clf"], ("lear",)), parts=["lear", "theta", "spike", "neg"],
        code=[("## Scores and ROC curves", THRESH + "\n\n\n" + PERSIST + r'''
CN = {"xgb": FC["neg_xgb"], "logit": FC["neg_logit"], "persist": (past <= 0).mean(0), "lear": -FC["aw_lear"]}
from sklearn.metrics import roc_auc_score, roc_curve
fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.35), sharey=True)
for ax, Y_, CC, ttl in [(axs[0], Y_SP, CS, "spikes"), (axs[1], Y_NG, CN, "prices $\\leq$ 0")]:
    for k, c, ls, lb in [("xgb", PAL["BG"], "-", "XGBoost"), ("logit", PAL["c7"], "--", "logistic regression"),
                         ("persist", "#9a9a9a", ":", "persistence (last 7 days)"), ("lear", PAL["RO"], "-.", "AW-LEAR point forecast")]:
        fpr, tpr, _ = roc_curve(Y_.ravel(), CC[k].ravel())
        ax.plot(fpr, tpr, color=c, ls=ls, lw=1.3, label=lb)
    ax.plot([0, 1], [0, 1], color="#222222", lw=0.5)
    ax.set_title(ttl, fontsize=10)
    ax.set_xlabel("false alarm rate", fontsize=9.5)
axs[0].set_ylabel("share of events\ncaught", fontsize=9.5)
legend_bottom(fig, ncol=2)
save_chart(fig, "roc", bottom=0.26)
auc = lambda y, p: roc_auc_score(y.ravel(), p.ravel())''')],
        checks=[(f"Spikes, AUC {k}", f"spike.{k}.auc", ".3f", f"auc(Y_SP, CS['{k}'])") for k in ["xgb", "logit", "persist", "lear"]] +
               [(f"Prices <= 0, AUC {k}", f"neg.{k}.auc", ".3f", f"auc(Y_NG, CN['{k}'])") for k in ["xgb", "logit", "persist", "lear"]])

    # ------------------------------------------------------------------ 13 decision
    Q["decision"] = dict(
        title="Cost-loss rule: act when the spike probability exceeds C/L",
        desc=("Value over the test year (thousand EUR per MW of flexible load) of moving 1 MWh out of every hour in which the XGBoost spike "
              "probability exceeds an action threshold, against the threshold, with the cost-loss threshold C/L (C = 30 EUR/MWh, assumed; "
              f"L = mean excess over the spike threshold in the validation year) and 0.5. Romanian day-ahead prices, {test}."),
        kw="cost-loss decision, decision threshold, spike probability, demand response, flexibility, value of forecasts, electricity price",
        data=PRICES + "; saved test-year spike probabilities of the XGBoost and logistic classifiers (decision_results.npz)",
        saved={"days": TD, "spike_xgb": CS["xgb"], "spike_logit": CS["logit"]},
        cost="about 30 minutes on one core (12 monthly refits of the spike classifiers)",
        engine=(["xgb", "clf"], ()), parts=["theta", "spike"],
        code=[("## Value of acting, by threshold", THRESH + "\n\n" + LBAR + r'''
VALUE = A - TH_T[:, None] - C_ACT                                   # gain of moving 1 MWh out of the hour, EUR


def act_value(pi, cut):
    return float(VALUE[pi > cut].sum())


past = np.stack([P_[rows_all - k] for k in range(1, 8)], 0)
persist = (past > TH_T[None, :, None]).mean(0)
CUTS = np.linspace(0.02, 0.98, 49)
VCURVE = np.array([act_value(FC["spike_xgb"], c) for c in CUTS]) / 1000
fig, ax = plt.subplots(figsize=(6.4, 1.95))
ax.plot(CUTS, VCURVE, color=PAL["BG"], label="act when XGBoost probability > threshold")
ax.axvline(CUT, color=PAL["DE_LU"], ls="--", lw=1.0, label="cost-loss threshold C/L")
ax.axvline(0.5, color="#9a9a9a", ls=":", lw=1.0, label="threshold 0.5")
ax.set_xlim(0.1, 1.0)
ax.set_ylim(min(0, VCURVE[CUTS >= 0.1].min()) - 3, VCURVE.max() * 1.25)
ax.axhline(0, color="#222222", lw=0.5)
ax.set_xlabel("action threshold (probability of a spike)")
ax.set_ylabel("value, thousand\nEUR per MW", fontsize=9.5)
legend_bottom(fig, ncol=3)
save_chart(fig, "decision", bottom=0.22)''')],
        checks=[("Mean loss of a missed spike L, EUR/MWh", "decision.Lbar", ".1f", "LBAR"),
                ("Cost-loss threshold C/L", "decision.cut", ".3f", "CUT"),
                ("Value at C/L, thousand EUR per MW", "decision.v_cut", ".1f", "act_value(FC['spike_xgb'], CUT) / 1000"),
                ("Value at 0.5", "decision.v_half", ".1f", "act_value(FC['spike_xgb'], 0.5) / 1000"),
                ("Value with persistence at C/L", "decision.v_persist", ".1f", "act_value(persist, CUT) / 1000"),
                ("Value with the logistic classifier at C/L", "decision.v_logit", ".1f", "act_value(FC['spike_logit'], CUT) / 1000"),
                ("Value with perfect foresight", "decision.v_perfect", ".1f", "VALUE[VALUE > 0].sum() / 1000"),
                ("Alerts at C/L (hours)", "decision.n_alerts_cut", "d", "int((FC['spike_xgb'] > CUT).sum())"),
                ("Best threshold seen afterwards", "decision.best_cut", ".2f", "CUTS[np.argmax(VCURVE)]")])

    # ------------------------------------------------------------------ 14 snooping
    Q["snooping"] = dict(
        title="Data snooping: choosing on the test year fakes a win over LEAR",
        desc=("Test-year MAE against validation-year MAE of the 25 configurations of the DNN and of XGBoost (one seed each), with the "
              "configuration chosen honestly on the validation year, the one that would be chosen on the test year (data snooping) and "
              f"AW-LEAR. Romanian day-ahead prices, validation year {D['val_start']} to {D['val_end']} and {test}."),
        kw="data snooping, model selection, overfitting, validation, test set, neural network, XGBoost, LEAR, Spearman correlation",
        data=PRICES + "; saved validation and test MAE of the 25 configurations of each model and the AW-LEAR forecasts (snooping_results.npz)",
        saved={"days": TD, "val_dnn": ns["VAL_DNN"], "val_xgb": ns["VAL_XGB"], "test_dnn": ns["TEST_DNN"], "test_xgb": ns["TEST_XGB"], "aw_lear": M["aw_lear"]},
        cost="about 5 hours on 16 cores (25 configurations x 2 models, on the validation year and on the test year)",
        engine=(["dnn", "xgb", "space"], ("lear",)), parts=["lear", "search", "snoop"],
        code=[("## Validation against test error of every configuration", r'''from scipy import stats
VAL_DNN, VAL_XGB, TEST_DNN, TEST_XGB = FC["val_dnn"], FC["val_xgb"], FC["test_dnn"], FC["test_xgb"]
BEST_DNN, BEST_XGB = int(np.argmin(VAL_DNN)), int(np.argmin(VAL_XGB))
LEAR_MAE = np.mean(np.abs(A - FC["aw_lear"]))
fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.3))
for ax, V, Tt, best_, nm in [(axs[0], VAL_DNN, TEST_DNN, BEST_DNN, "DNN"), (axs[1], VAL_XGB, TEST_XGB, BEST_XGB, "XGBoost")]:
    ax.plot(V, Tt, "o", color="#9a9a9a", ms=4, label="one configuration")
    ax.plot(V[best_], Tt[best_], "o", color=PAL["DE_LU"], ms=7, label="chosen on validation (honest)")
    jb = int(np.argmin(Tt))
    ax.plot(V[jb], Tt[jb], "*", color=PAL["c8"], ms=10, label="best on the test year (snooping)")
    ax.axhline(LEAR_MAE, color=PAL["RO"], ls="--", lw=1.0, label="AW-LEAR, test year")
    ax.set_title(nm, fontsize=10)
    ax.set_xlabel("MAE, validation year", fontsize=9.5)
axs[0].set_ylabel("MAE, test year", fontsize=9.5)
legend_bottom(fig, ncol=2)
save_chart(fig, "snooping", bottom=0.27)''')],
        checks=[("DNN chosen on validation, test MAE", "search.dnn.test_chosen", ".2f", "TEST_DNN[BEST_DNN]"),
                ("DNN best on the test year (snooping)", "search.dnn.test_best", ".2f", "TEST_DNN.min()"),
                ("AW-LEAR, test MAE", "acc.aw_lear.mae", ".2f", "LEAR_MAE"),
                ("DNN settings below AW-LEAR on the test year", "search.dnn.n_test_below_lear", "d", "int((TEST_DNN < LEAR_MAE).sum())"),
                ("Spearman correlation validation-test, DNN", "search.dnn.spearman", ".2f", "stats.spearmanr(VAL_DNN, TEST_DNN)[0]"),
                ("XGBoost chosen on validation, test MAE", "search.xgb.test_chosen", ".2f", "TEST_XGB[BEST_XGB]"),
                ("XGBoost best on the test year", "search.xgb.test_best", ".2f", "TEST_XGB.min()"),
                ("Spearman correlation validation-test, XGBoost", "search.xgb.spearman", ".2f", "stats.spearmanr(VAL_XGB, TEST_XGB)[0]")])

    # ------------------------------------------------------------------ 15 pit_leak
    PF = ns["PF"]
    Q["pit_leak"] = dict(
        title="Look-ahead: two invalid evaluations flatter XGBoost",
        desc=("Test-year MAE of the tuned XGBoost evaluated honestly (monthly refits on past days), with shuffled 5-fold cross-validation "
              "(future days in the training folds) and with the realised load and wind+solar of the delivery day as inputs (not known at "
              f"gate closure), against AW-LEAR. Romanian day-ahead prices, {test}."),
        kw="look-ahead bias, data leakage, cross-validation, walk-forward evaluation, XGBoost, electricity price forecasting, pitfalls",
        data=PRICES + "; saved test-year forecasts of the three XGBoost evaluations and of AW-LEAR (pit_leak_results.npz)",
        saved={"days": TD, "honest": PF["honest"], "shuffled": PF["shuffled"], "leak": PF["leak"], "aw_lear": M["aw_lear"]},
        cost="about 1.5 hours on one core (three evaluations of XGBoost with 1500 trees)",
        engine=(["xgb", "shuffled"], ("lear",)), parts=["lear", "xgb"],
        runall_extra='''FC["honest"] = FC["xgb"]
FC["leak"] = np.vstack(Parallel(n_jobs=-1)(delayed(xgb_block)(P_, L_, R_, F_, a, b, CFG_XGB, leak=True)["pred"] for a, b in MB))
FC["shuffled"] = xgb_cv_shuffled(P_, L_, R_, F_, CFG_XGB)[rows_all]''',
        code=[("## Honest and invalid evaluations", MAEFN + r'''


pit = {k: mae(FC[k]) for k in ["honest", "shuffled", "leak"]}
LEAR_MAE = mae(FC["aw_lear"])
fig, ax = plt.subplots(figsize=(6.4, 1.6))
kk = [("honest", "honest, monthly refits", PAL["BG"]), ("shuffled", "shuffled 5-fold validation", PAL["c8"]),
      ("leak", "+ load, RES of day d", PAL["c8"])]
ax.barh(range(3), [pit[k] for k, _, _ in kk], color=[c for _, _, c in kk], height=0.6)
ax.set_yticks(range(3))
ax.set_yticklabels([lb for _, lb, _ in kk], fontsize=8.5)
ax.invert_yaxis()
ax.axvline(LEAR_MAE, color=PAL["RO"], ls="--", lw=0.9, label="AW-LEAR, honest")
ax.set_xlim(20, max(pit.values()) + 0.8)
ax.set_xlabel("MAE on the test year, EUR/MWh (axis does not start at 0)", fontsize=9.5)
legend_bottom(fig, ncol=1)
save_chart(fig, "pit_leak", bottom=0.2)''')],
        checks=[("Honest, MAE", "pit.honest", ".2f", "pit['honest']"),
                ("Shuffled 5-fold, MAE", "pit.shuffled", ".2f", "pit['shuffled']"),
                ("Apparent gain of shuffling, %", "pit.shuf_gain", ".1f", "(1 - pit['shuffled'] / pit['honest']) * 100"),
                ("Load and RES of day d, MAE", "pit.leak", ".2f", "pit['leak']"),
                ("Apparent gain of look-ahead inputs, %", "pit.leak_gain", ".1f", "(1 - pit['leak'] / pit['honest']) * 100")])

    # ------------------------------------------------------------------ 16 pit_retrain
    Q["pit_retrain"] = dict(
        title="Retraining: a model frozen for a year loses accuracy",
        desc=("Test-year MAE of the tuned XGBoost by retraining frequency (monthly, quarterly, once before the test year) and window "
              f"(all past days, last 730 or 365 days), against AW-LEAR. Romanian day-ahead prices, {test}."),
        kw="retraining frequency, rolling window, expanding window, concept drift, XGBoost, electricity price forecasting, model maintenance",
        data=PRICES + "; saved test-year forecasts of XGBoost under five retraining schemes and of AW-LEAR (pit_retrain_results.npz)",
        saved={"days": TD, **{k: PF[k] for k in ["honest", "quarterly", "once", "roll730", "roll365"]}, "aw_lear": M["aw_lear"]},
        cost="about 2 hours on one core (five retraining schemes of XGBoost with 1500 trees)",
        engine=(["xgb"], ("lear",)), parts=["lear", "xgb"],
        runall_extra='''FC["honest"] = FC["xgb"]
FC["quarterly"] = np.vstack(Parallel(n_jobs=-1)(delayed(xgb_block)(P_, L_, R_, F_, a, b, CFG_XGB)["pred"] for a, b in blocks_of(TDAYS, "Q")))
FC["once"] = xgb_block(P_, L_, R_, F_, MB[0][0], MB[-1][1], CFG_XGB)["pred"]
FC["roll365"] = np.vstack(Parallel(n_jobs=-1)(delayed(xgb_block)(P_, L_, R_, F_, a, b, CFG_XGB, lo=a - 365)["pred"] for a, b in MB))
FC["roll730"] = np.vstack(Parallel(n_jobs=-1)(delayed(xgb_block)(P_, L_, R_, F_, a, b, CFG_XGB, lo=a - 730)["pred"] for a, b in MB))''',
        code=[("## MAE by retraining scheme", MAEFN + r'''


pit = {k: mae(FC[k]) for k in ["honest", "quarterly", "once", "roll730", "roll365"]}
LEAR_MAE = mae(FC["aw_lear"])
TM = TDAYS.to_period("M")
MONTHS_T = sorted(set(TM))
loss_m = [np.mean(np.abs(A[TM == mm] - FC["once"][TM == mm])) - np.mean(np.abs(A[TM == mm] - FC["honest"][TM == mm])) for mm in MONTHS_T]
fig, ax = plt.subplots(figsize=(6.4, 1.8))
kk2 = [("honest", "monthly, all past days"), ("quarterly", "quarterly, all past days"), ("once", "once, before the test year"),
       ("roll730", "monthly, last 730 days"), ("roll365", "monthly, last 365 days")]
ax.barh(range(len(kk2)), [pit[k] for k, _ in kk2], color=[PAL["BG"]] + [PAL["c7"]] * 4, height=0.6)
ax.set_yticks(range(len(kk2)))
ax.set_yticklabels([lb for _, lb in kk2], fontsize=8.5)
ax.invert_yaxis()
ax.axvline(LEAR_MAE, color=PAL["RO"], ls="--", lw=0.9, label="AW-LEAR")
ax.set_xlim(min(min(pit.values()), LEAR_MAE) - 1.5, max(pit.values()) + 0.8)
ax.set_xlabel("MAE on the test year, EUR/MWh (axis does not start at 0)", fontsize=9.5)
legend_bottom(fig, ncol=1)
save_chart(fig, "pit_retrain", bottom=0.2)
''')],
        checks=[("Monthly, all past days, MAE", "pit.honest", ".2f", "pit['honest']"),
                ("Quarterly, MAE", "pit.quarterly", ".2f", "pit['quarterly']"),
                ("Once before the test year, MAE", "pit.once", ".2f", "pit['once']"),
                ("Loss of the frozen model, %", "pit.once_loss", ".1f", "(pit['once'] / pit['honest'] - 1) * 100"),
                ("Extra MAE of the frozen model, first 3 months", "pit.once_first_q", ".2f", "np.mean(loss_m[:3])"),
                ("Extra MAE of the frozen model, last 3 months", "pit.once_last_q", ".2f", "np.mean(loss_m[-3:])"),
                ("Monthly, last 730 days, MAE", "pit.roll730", ".2f", "pit['roll730']"),
                ("Monthly, last 365 days, MAE", "pit.roll365", ".2f", "pit['roll365']")])

    # ------------------------------------------------------------------ 17 case_week
    cs = J["case"]
    Q["case_week"] = dict(
        title="Case study: every model saw the spike, none its size",
        desc=("Studiu de caz around the highest hourly price of the test year: hourly Romanian day-ahead price, the AW-LEAR, XGBoost and "
              "Chronos-2 forecasts and the spike threshold (top), and the XGBoost spike probability with the cost-loss threshold C/L and the "
              f"actual spike hours (bottom); week {cs['week_start']} to {cs['week_end']}."),
        kw="case study, price spike, extreme price, spike probability, early warning, LEAR, XGBoost, Chronos, Romania, day-ahead market",
        data=PRICES + "; saved test-year forecasts of AW-LEAR, XGBoost, DNN, Chronos-2 and the XGBoost spike probabilities (case_week_results.npz)",
        saved={"days": TD, "aw_lear": M["aw_lear"], "xgb": M["xgb"], "dnn": M["dnn"], "chr2": M["chr2"], "spike_xgb": CS["xgb"]},
        cost="several hours on one core (AW-LEAR, DNN, XGBoost, Chronos-2 and the spike classifier)",
        engine=(["dnn", "xgb", "clf", "chronos"], ("lear",)), parts=["lear", "dnn", "xgb", "chr2", "theta", "spike"],
        code=[("## The highest price of the test year and its week", THRESH + "\n\n" + LBAR + r'''
kd, kh = np.unravel_index(np.argmax(A), A.shape)                    # day and hour of the highest price
CDAY = TDAYS[kd]
CWS = slice(max(0, kd - 3), min(len(TDAYS), max(0, kd - 3) + 7))    # the week around it
alerts = FC["spike_xgb"][CWS] > CUT
DAYN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
nd = CWS.stop - CWS.start
xs_ = pd.date_range(TDAYS[CWS.start], periods=24 * nd, freq="h")
fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.75), sharex=True, gridspec_kw={"height_ratios": [1.7, 1]})
axs[0].plot(xs_, A[CWS].ravel(), color="#222222", lw=1.4, label="actual price")
for k, ls in [("aw_lear", "-"), ("xgb", "--"), ("chr2", "-.")]:
    axs[0].plot(xs_, FC[k][CWS].ravel(), color=COL[k], ls=ls, lw=1.0, label=LAB[k])
axs[0].plot(xs_, np.repeat(TH_T[CWS], 24), color="#6b6b6b", lw=0.9, ls=":", label="spike threshold")
axs[0].set_ylabel("EUR/MWh")
axs[1].fill_between(xs_, 0, Y_SP[CWS].ravel(), step="mid", color=PAL["c8"], alpha=0.18, lw=0, label="actual spike hour")
axs[1].plot(xs_, FC["spike_xgb"][CWS].ravel(), color=PAL["BG"], lw=1.1, label="spike probability, XGBoost")
axs[1].axhline(CUT, color=PAL["DE_LU"], ls="--", lw=0.8, label="C/L")
axs[1].set_ylim(0, 1)
axs[1].set_ylabel("probability", fontsize=9.5)
axs[1].xaxis.set_major_locator(mdates.DayLocator())
axs[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda v, p: f"{DAYN[mdates.num2date(v).weekday()]} {mdates.num2date(v).day}"))
legend_bottom(fig, ncol=4)
save_chart(fig, "case_week", bottom=0.16)''')],
        checks=[("Day of the highest price", "case.day", "", "str(CDAY.date())"), ("Hour (CET)", "case.hour", "d", "int(kh)"),
                ("Price, EUR/MWh", "case.price", ".2f", "A[kd, kh]"),
                ("AW-LEAR forecast", "case.aw_lear", ".0f", "FC['aw_lear'][kd, kh]"), ("XGBoost forecast", "case.xgb", ".0f", "FC['xgb'][kd, kh]"),
                ("DNN forecast", "case.dnn", ".0f", "FC['dnn'][kd, kh]"), ("Chronos-2 forecast", "case.chr2", ".0f", "FC['chr2'][kd, kh]"),
                ("Spike probability, XGBoost", "case.p_xgb", ".3f", "FC['spike_xgb'][kd, kh]"),
                ("Week starts", "case.week_start", "", "str(TDAYS[CWS.start].date())"), ("Week ends", "case.week_end", "", "str(TDAYS[CWS.stop - 1].date())"),
                ("Spike hours in the week", "case.w_spike_h", "d", "int(Y_SP[CWS].sum())"),
                ("Alerts at C/L in the week", "case.w_alerts", "d", "int(alerts.sum())"),
                ("Correct alerts", "case.w_hits", "d", "int((alerts & (Y_SP[CWS] == 1)).sum())")])

    # ------------------------------------------------------------------ 18 shap_local
    kd, kh = ns["kd"], ns["kh"]
    Q["shap_local"] = dict(
        title="Case study: the trees followed the extreme evening of the day before",
        desc=("Local SHAP explanation of the XGBoost forecast for the highest price of the test year "
              f"({cs['day']}, hour {cs['hour']}:00 CET): waterfall from the average forecast of the model to the forecast, with the seven "
              "largest contributions and the sum of the other 13, rescaled to EUR/MWh (proportional allocation), and the actual price. "
              "Romanian day-ahead market."),
        kw="SHAP, local explanation, waterfall chart, explainable AI, XGBoost, price spike, case study, electricity price, Romania",
        data=PRICES + "; saved SHAP values, inputs and price scaling of the XGBoost model for that hour (shap_local_results.npz)",
        saved={"day": np.array(cs["day"]), "hour": np.array(int(kh)), "phi": ns["SH"][kd, kh, :-1], "phi0": np.array(ns["SH"][kd, kh, -1]),
               "x": ns["XS"][kd, kh], "m": np.array(ns["MS"][kd]), "s": np.array(ns["SS"][kd])},
        cost="about 30 minutes on one core (12 monthly refits of XGBoost with 1500 trees)",
        engine=(["xgb"], ()), parts=["xgb"],
        runall_extra=xgb_runall + '''
MS = np.array([r["m"] for r in res_xgb for _ in range(r["pred"].shape[0])])      # median and MAD of the asinh transform
SS = np.array([r["s"] for r in res_xgb for _ in range(r["pred"].shape[0])])
_kd, _kh = np.unravel_index(np.argmax(A), A.shape)
FC.update({"day": np.array(str(TDAYS[_kd].date())), "hour": np.array(int(_kh)), "phi": SH[_kd, _kh, :-1], "phi0": np.array(SH[_kd, _kh, -1]),
           "x": XS[_kd, _kh], "m": np.array(MS[_kd]), "s": np.array(SS[_kd])})''',
        code=[("## From SHAP values on the asinh scale to EUR/MWh", FNAME + r'''


kd, kh = np.unravel_index(np.argmax(A), A.shape)                    # highest price of the test year
assert str(TDAYS[kd].date()) == str(FC["day"]) and kh == int(FC["hour"])
phi, y0, m_, s_ = FC["phi"], float(FC["phi0"]), float(FC["m"]), float(FC["s"])
yhat = y0 + phi.sum()                                               # forecast on the asinh scale
P0, PH = m_ + s_ * np.sinh(y0), m_ + s_ * np.sinh(yhat)            # average forecast and forecast, EUR/MWh
phi_eur = phi * (PH - P0) / (yhat - y0)                             # proportional allocation (Appendix C of the lecture)
ordr = np.argsort(-np.abs(phi_eur))
DAYN = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
fig, ax = plt.subplots(figsize=(6.4, 2.3))
top = list(ordr[:7])
rest = phi_eur.sum() - phi_eur[top].sum()
vals = [phi_eur[j] for j in top] + [rest]
lv = lambda j: DAYN[int(FC["x"][j])] if XGB_NAMES[j] == "day of week" else f"{FC['x'][j]:,.0f}".replace(",", " ")
labs = [f"{FNAME[XGB_NAMES[j]]}: {lv(j)}" for j in top] + ["other 13 features"]
cum = P0
for i_, v in enumerate(vals):
    ax.barh(i_, v, left=cum, color=PAL["c8"] if v > 0 else PAL["HU"], height=0.6)
    cum += v
ax.axvline(P0, color="#9a9a9a", ls=":", lw=1.0, label=f"average forecast of the model ({P0:.0f})")
ax.axvline(PH, color=PAL["BG"], ls="--", lw=1.0, label=f"XGBoost forecast ({PH:.0f})")
ax.axvline(A[kd, kh], color="#222222", lw=1.2, label=f"actual price ({A[kd, kh]:.0f})")
ax.set_xlim(0, max(A[kd, kh], PH) * 1.04)
ax.set_yticks(range(len(vals)))
ax.set_yticklabels(labs, fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("EUR/MWh")
legend_bottom(fig, ncol=3)
save_chart(fig, "shap_local", bottom=0.17)''')],
        checks=[("Average forecast of the model, EUR/MWh", "case.base_eur", ".0f", "P0"),
                ("XGBoost forecast", "case.xgb_eur", ".0f", "PH"),
                ("Actual price", "case.price", ".2f", "A[kd, kh]"),
                ("Largest contribution", "case.top_feat.0", "", "XGB_NAMES[ordr[0]]"),
                ("Its contribution, EUR/MWh", "case.top_eur.0", "+.0f", "phi_eur[ordr[0]]"),
                ("Second contribution", "case.top_feat.1", "", "XGB_NAMES[ordr[1]]"),
                ("Its contribution, EUR/MWh", "case.top_eur.1", "+.0f", "phi_eur[ordr[1]]")])

    # ------------------------------------------------------------------ 19 foundation_hour
    Q["foundation_hour"] = dict(
        title="Chronos-2 beats AW-LEAR in every hour of the day",
        desc=("Mean absolute error by hour of the day (CET) of the naive model, AW-LEAR and two pretrained time-series foundation models "
              "used zero-shot (Chronos-Bolt small and Chronos-2; context = the last 2048 hourly prices up to the end of d-1). Romanian "
              f"day-ahead prices, {test}."),
        kw="foundation model, Chronos, Chronos-2, zero-shot forecasting, time series, LEAR, electricity price forecasting, MAE by hour",
        data=PRICES + "; saved test-year forecasts of the naive model, AW-LEAR, Chronos-Bolt and Chronos-2 with its 10% and 90% quantiles (foundation_hour_results.npz)",
        saved={"days": TD, "naive": M["naive"], "aw_lear": M["aw_lear"], "bolt": M["bolt"], "chr2": M["chr2"],
               "chr2_q10": C["chronos2"]["q"][:, :, 0], "chr2_q90": C["chronos2"]["q"][:, :, 2]},
        cost="several hours on one core (AW-LEAR; Chronos-2 and Chronos-Bolt run in about 10 minutes)",
        engine=(["chronos"], ("lear",)), parts=["naive", "lear", "chr2", "bolt"],
        code=[("## MAE by hour of the day", MAEFN + "\n\n\n" + DM + r'''


E = {k: A - FC[k] for k in ["naive", "bolt", "chr2", "aw_lear"]}
BYHOUR = {k: np.mean(np.abs(e), 0) for k, e in E.items()}
cov80 = ((A >= FC["chr2_q10"]) & (A <= FC["chr2_q90"])).mean() * 100      # coverage of the 10%-90% band
h24 = np.arange(24)
fig, ax = plt.subplots(figsize=(6.4, 1.9))
for k, ls, mk in [("naive", ":", "o"), ("bolt", "--", "s"), ("chr2", "-", "^"), ("aw_lear", "-", "o")]:
    ax.plot(h24, BYHOUR[k], color=COL[k], ls=ls, marker=mk, ms=3, label=LAB[k])
ax.set_xticks(range(0, 24, 2))
ax.set_xlabel("hour h (CET)")
ax.set_ylabel("MAE, EUR/MWh")
legend_bottom(fig, ncol=4)
save_chart(fig, "foundation_hour", bottom=0.22)''')],
        checks=[("MAE Chronos-2, EUR/MWh", "acc.chr2.mae", ".2f", "mae(FC['chr2'])"),
                ("MAE Chronos-Bolt", "acc.bolt.mae", ".2f", "mae(FC['bolt'])"),
                ("MAE AW-LEAR", "acc.aw_lear.mae", ".2f", "mae(FC['aw_lear'])"),
                ("Hours in which Chronos-2 beats AW-LEAR", "found.chr2_beats_lear_h", "d", "int((BYHOUR['chr2'] < BYHOUR['aw_lear']).sum())"),
                ("DM p-value, AW-LEAR vs Chronos-2", "dm.aw_lear__chr2.p", ".4f", "dm(E['aw_lear'], E['chr2'])[1]"),
                ("DM p-value, AW-LEAR vs Chronos-Bolt", "dm.aw_lear__bolt.p", ".4f", "dm(E['aw_lear'], E['bolt'])[1]"),
                ("Coverage of the 10%-90% band of Chronos-2, %", "found.cov80", ".1f", "cov80")])
    for k, v in Q.items():
        v["desc"] = v["desc"].rstrip(".") + ". Data: " + period[k] + "."
    return Q


# =============================================================================
# 4. Write, execute and check every Quantlet
# =============================================================================
def write_one(chart, q, ns):
    name = f"EMQA_L7_{chart}"
    folder = os.path.join(REPO, "Quantlets", "L7", name)
    os.makedirs(folder, exist_ok=True)
    Ql = Quantlet(k=7, chart=chart, title=q["title"], description=q["desc"], keywords=q["kw"], datafile=q["data"])
    Ql.md(q["desc"] + "\n\nThe numbers printed at the end are those on the slide of Lecture 7.")
    Ql.md("## Setup: chart style and helpers").code(STYLE + ("\n\n" + LABCOL if "LAB[" in "".join(c for _, c in q["code"]) else ""))
    Ql.md("## Data: Romanian day-ahead prices, CET delivery day x 24 hours").code(prices_block())
    saved = q.get("saved")
    if saved is not None:
        fname = f"{chart}_results.npz"
        np.savez_compressed(os.path.join(folder, fname), **saved)
        size = os.path.getsize(os.path.join(folder, fname))
        assert size < 5e6, (chart, size)
        groups, l2 = q["engine"]
        if q.get("pre"):
            Ql.code(q["pre"])
        Ql.md(RUNALL_MD.format(cost=q["cost"], saved=fname))
        Ql.code("RUN_ALL = False      # True: recompute the model outputs from the data (needs torch, xgboost, scikit-learn"
                + (", chronos-forecasting" if "chronos" in groups else "") + ")")
        Ql.md("Code of the models (copied from `lectures/L7/analysis_L7.py`" + (" and `lectures/L2/analysis_L2.py`" if l2 else "") +
              "); defining the functions takes no time.")
        Ql.code(engine_cell(ns, groups, l2) + "\n\n\n" + LOADER.format(name=name))
        code = runall_cell(q["parts"], fname)
        if q.get("runall_extra"):
            code = code.replace("\nelse:\n", "\n" + textwrap.indent(q["runall_extra"], "    ") + "\nelse:\n", 1)
        Ql.code(code)
    for md, c in q["code"]:
        Ql.md(md).code(c)
    Ql.md("## Numbers on the slide").code("\n".join(f"show({lab!r}, {expr}, {fmt!r})" for lab, _, fmt, expr in q["checks"]))
    Ql.write(execute=True)
    # check: every printed number equals the value in L7_numbers.json
    import nbformat
    nb = nbformat.read(os.path.join(folder, name + ".ipynb"), as_version=4)
    text = "".join(o.get("text", "") for o in nb.cells[-1].outputs)
    miss = []
    for lab, key, fmt, _ in q["checks"]:
        exp = f"{lab}: {format(get(J, key), fmt)}"
        if exp not in text.splitlines():
            got = [ln for ln in text.splitlines() if ln.startswith(lab + ":")]
            miss.append((key, exp, got))
    return miss, len(q["checks"])


if __name__ == "__main__":
    ns = run_analysis()
    Q = build(ns)
    report = {}
    for chart, q in Q.items():
        if ONLY and chart not in ONLY:
            continue
        report[chart] = write_one(chart, q, ns)
    print("\nQuantlet                    numbers checked   mismatches")
    bad = 0
    for chart, (miss, n) in report.items():
        print(f"EMQA_L7_{chart:<20s} {n:>8d}   {len(miss)}")
        for m in miss:
            print("    MISMATCH", m)
        bad += len(miss)
    print("all numbers equal L7_numbers.json" if not bad else f"{bad} mismatches")
