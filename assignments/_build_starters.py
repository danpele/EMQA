"""Builds the starter notebooks in English and Romanian from ONE source (this file).
python3 _build_starters.py  ->  A1/A1_starter_EN.ipynb, A1/A1_starter_RO.ipynb, A2/A2_starter_EN.ipynb, A2/A2_starter_RO.ipynb
The starters load data and show the expected structure; they contain no solutions."""
import os

import nbformat as nbf

HERE = os.path.dirname(os.path.abspath(__file__))

SETUP = r'''
import os, sys, json, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.abspath(".."))      # folder that contains emqa_assign.py
import emqa_assign as ea
pd.set_option("display.width", 160)
'''


def M(en, ro):
    return ("md", {"en": en, "ro": ro})


def C(code):
    return ("code", code)


A1 = [
    M("# EMQA Assignment 1 — starter notebook\n"
      "**Day-ahead price forecasting and volatility for a Romanian bidding desk** (lectures 1–3).\n\n"
      "Read the brief (`A1_brief_EN.pdf`) first. This notebook loads the data and shows the structure "
      "you must follow. Replace every `TODO`. Do not change the names of the required objects "
      "(`F`, `T5`, `T6`, `T7`, `MY_NUMBERS`): the instructor's checker reads them.\n\n"
      "Rules in one line: run top-to-bottom with *Restart & Run All*; no hard-coded dates; "
      "no information after gate closure (12:00 CET on day d−1); every number in your memo comes from this notebook.",
      "# Tema 1 EMQA — notebook de pornire\n"
      "**Prognoza prețului PZU și volatilitatea, pentru biroul de ofertare al unei companii românești** "
      "(cursurile 1–3).\n\n"
      "Citiți întîi enunțul (`A1_brief_RO.pdf`). Acest notebook încarcă datele și arată structura pe care "
      "trebuie să o urmați. Înlocuiți fiecare `TODO`. Nu schimbați numele obiectelor cerute "
      "(`F`, `T5`, `T6`, `T7`, `MY_NUMBERS`): scriptul de verificare al profesorului le citește.\n\n"
      "Regulile pe scurt: notebook-ul rulează de la cap la coadă cu *Restart & Run All*; fără date calendaristice "
      "introduse direct în cod; nicio informație de după închiderea porții (12:00 CET în ziua d−1); fiecare număr din "
      "memoriu provine din acest notebook."),
    M("## 0. Your personal parameters", "## 0. Parametrii personali"),
    C("STUDENT_ID = 'TODO-your-student-ID'   # team: 'ID1+ID2'\n"
      "MODE = 'personal'                     # the instructor will also run MODE = 'latest' (unseen hold-out)\n"
      + SETUP + r'''
p = ea.params(STUDENT_ID, 1)
if MODE == "latest":
    p = ea.latest_window(p)
print(json.dumps(p, indent=1))
display(ea.data_version())          # rule R3: record the data version
'''),
    M("## 1. Data\n"
      "`P`: prices (EUR/MWh), `L`: load (MW), `R`: wind + solar (MW); one row per CET delivery day, "
      "columns `h00`…`h23` (CET hours). After 2025-10-01 each hourly value is the mean of four quarter-hours.\n\n"
      "**Information set (gate closure, 12:00 CET on *d−1*).**\n"
      "- prices: every day up to *d−1* (the *d−1* auction cleared on *d−2*);\n"
      "- realised load `L` and wind+solar `R`: only up to day *d−2* (day *d−1* is not yet metered); as a proxy for the TSO's forecasts use "
      "`L`, `R` of day *d−2* at the same hour (and *d−3*, *d−7* as further lags);\n"
      "- transformations and scalers: fitted on these data only.\n\n"
      "`ea.leakage_check` enforces this rule: it hides `P` from day *d* and `L`, `R` from day *d−1* onwards.",
      "## 1. Date\n"
      "`P`: prețuri (EUR/MWh), `L`: consum (MW), `R`: eolian + solar (MW); un rînd pe zi de livrare CET, "
      "coloanele `h00`…`h23` (ore CET). După 2025-10-01 fiecare valoare orară este media celor patru sferturi de oră.\n\n"
      "**Setul de informații (închiderea porții, ora 12:00 CET în ziua *d−1*).**\n"
      "- prețurile: toate zilele pînă în *d−1* (licitația pentru ziua *d−1* s-a încheiat în *d−2*);\n"
      "- consumul `L` și producția eoliană+solară `R` realizate: numai pînă în ziua *d−2* (ziua *d−1* nu este încă măsurată); ca substitut (proxy) pentru prognozele OTS folosiți "
      "`L`, `R` din ziua *d−2*, la aceeași oră (și *d−3*, *d−7* ca decalaje suplimentare);\n"
      "- transformările și standardizările: estimate numai pe aceste date.\n\n"
      "`ea.leakage_check` verifică această regulă: ascunde `P` începînd cu ziua *d* și `L`, `R` începînd cu ziua *d−1*."),
    C(r'''
P, L, R = ea.panel("RO")
t0, t1 = pd.Timestamp(p["test_start"]), pd.Timestamp(p["test_end"])
test = pd.date_range(t0, t1, freq="D")                                         # evaluation days
fdays = pd.date_range(t0 - pd.Timedelta(days=p["burn_in_days"]), t1, freq="D")  # burn-in + test: forecast ALL of these
print(P.shape, P.index.min().date(), "->", P.index.max().date())
print("test:", test[0].date(), "->", test[-1].date(), "| forecast days incl. burn-in:", len(fdays))
display(P.loc[test[:3]].round(1))
'''),
    M("## Task 1 — The test window (table T1 + one figure)",
      "## Sarcina 1 — Fereastra de test (tabelul T1 + o figură)"),
    C(r'''
# TODO: compute on the test window: mean, std, min, max, number of negative hours,
#       number of negative MTUs (rows of ea.quarter_hours("RO"): hourly before 2025-10-01, 15-min after), share of days with 15-min MTU.
T1 = pd.Series(dtype=float)
# TODO: figure: daily base price 2023 -> end of test, test window shaded; y-axis "EUR/MWh".
'''),
    M("## Task 2 — Naive benchmarks\n"
      "Every forecasting function has the same signature `f(P, L, R, day) -> 24 numbers` so that "
      "`ea.leakage_check` can test it.",
      "## Sarcina 2 — Modele de referință naive\n"
      "Fiecare funcție de prognoză are aceeași semnătură `f(P, L, R, day) -> 24 de numere`, ca "
      "`ea.leakage_check` să o poată testa."),
    C(r'''
def naive_weron(P, L, R, day):
    """Mon, Sat, Sun: prices of d-7; Tue-Fri: prices of d-1 (same hour)."""
    # TODO
    raise NotImplementedError

def seasonal_naive(P, L, R, day):
    """prices of d-7, same hour"""
    # TODO
    raise NotImplementedError
'''),
    M("## Task 3 — Expert ARX, rolling calibration windows and averaging\n"
      "Skeleton of the rolling loop (the brief, section *Worked example*, shows one day by hand).",
      "## Sarcina 3 — Modelul expert ARX, ferestre de calibrare glisante și medierea lor\n"
      "Scheletul buclei glisante (enunțul, secțiunea *Exemplu rezolvat*, arată o zi calculată de mînă)."),
    C(r'''
def arx_forecast(P, L, R, day, T):
    """Expert ARX, one regression per hour h, calibrated on the T days d-T..d-1.
    Regressors (transformed prices, see brief): P[d-1,h], P[d-2,h], P[d-7,h], P[d-1,h23],
    min(P[d-1,:]), max(P[d-1,:]), L[d-2,h], R[d-2,h], Monday, Saturday, Sunday dummies, constant.
    L and R: only rows up to d-2 (day d-1 is not yet metered at gate closure), also for their mean and standard deviation."""
    i = P.index.get_loc(day)
    cal = np.arange(i - T, i)          # calibration TARGET days: rows i-T ... i-1 (all before `day`)
    # 1) variance-stabilising transform with median and MAD of the prices in rows (cal[0]-7) ... (i-1)
    # 2) for each hour h: build X_cal (T x 12) and y_cal (T), least squares
    # 3) build x_day from price rows i-1, i-2, i-7 and L/R row i-2 only; predict; back-transform
    # TODO
    raise NotImplementedError

# F = {"Naive (Weron)": DataFrame(fdays x 24), ..., "ARX(56)": ..., "AW-ARX(6 windows)": ...}
F = {}
# TODO: fill F for every model, for all days in fdays
# ea.leakage_check(lambda P, L, R, d: arx_forecast(P, L, R, d, 56), P, L, R, test[0])
'''),
    M("## Task 4 — LEAR (LASSO-estimated autoregression)", "## Sarcina 4 — LEAR (autoregresie estimată cu LASSO)"),
    C(r'''
from sklearn.linear_model import LassoLarsIC
def lear_forecast(P, L, R, day, T=p["lear_window"]):
    """247 regressors: prices d-1, d-2, d-3, d-7 (4 x 24), load and wind+solar proxies of d-2, d-3, d-7
    (2 x 3 x 24), 7 day-of-week dummies. One LassoLarsIC(criterion='aic') per hour."""
    # TODO
    raise NotImplementedError
'''),
    M("## Task 5 — Accuracy and Diebold–Mariano tests\nRequired tables: `T5` (one row per model) and two DM p-value matrices.",
      "## Sarcina 5 — Acuratețe și testele Diebold–Mariano\nTabele cerute: `T5` (un rînd pe model) și două matrice de valori p DM."),
    C(r'''
T5 = pd.DataFrame(columns=["MAE", "RMSE", "rMAE", "MAE_focus", "RMSE_focus", "rMAE_focus"])   # + per-year columns
# TODO: per calendar year and per quarter; DM (multivariate, |e|, Newey-West variance with 7 lags)
'''),
    M("## Task 6 — Probabilistic forecasts (HS and CP)", "## Sarcina 6 — Prognoze probabilistice (HS și CP)"),
    C(r'''
QS = np.arange(1, 100) / 100          # the 99 percentiles
# Q[model] : array (n_test_days, 24, 99); errors of the previous p["error_window"] days, same hour
T6 = pd.DataFrame(columns=["APS", "APS_focus", "cov50", "cov90", "cov90_focus", "Kupiec90_focus_p", "width90_focus"])
# TODO
'''),
    M("## Task 7 — Volatility (GARCH, GJR-GARCH, EGARCH with Student-t errors)",
      "## Sarcina 7 — Volatilitate (GARCH, GJR-GARCH, EGARCH cu erori Student-t)"),
    C(r'''
from arch import arch_model
daily = ea.daily_prices()["RO"].dropna()
# r_t = 100 * (asinh(P_t) - asinh(P_{t-1}));  remove day-of-week means estimated on the estimation sample only
# estimation sample: [test_start - p["garch_years"] years, test_start);  test: 1-day-ahead variance forecasts
T7 = pd.DataFrame()
# TODO
'''),
    M("## Task 8 — Numbers for the memo and hand-reconciliation table\n"
      "Every number you quote in the memo must be in `MY_NUMBERS` (rule R5).",
      "## Sarcina 8 — Numerele pentru memoriu și tabelul de reconciliere manuală\n"
      "Orice număr citat în memoriu trebuie să existe în `MY_NUMBERS` (regula R5)."),
    C(r'''
MY_NUMBERS = {"params": p}
# TODO: add T1, T5, DM, T6, T7 tables (as dicts), the reconciliation rows for p["check_days"] x p["check_hour"],
#       and your decision.
with open(f"my_numbers_A1_{p['student_id']}_{MODE}.json", "w") as fh:
    json.dump(MY_NUMBERS, fh, indent=1, default=str)
'''),
    M("## Self-check before submitting", "## Autoverificare înainte de predare"),
    C(r'''
checks = {
    "forecasts exist for every model": len(F) >= 10,
    "forecasts cover burn-in + test": all(f.index.equals(fdays) for f in F.values()) if F else False,
    "no missing forecasts": all(not f.isna().any().any() for f in F.values()) if F else False,
    "T5 filled": len(T5) > 0, "T6 filled": len(T6) > 0, "T7 filled": len(T7) > 0,
}
for k, v in checks.items():
    print(("OK   " if v else "FAIL ") + k)
'''),
]

A2 = [
    M("# EMQA Assignment 2 — starter notebook\n"
      "**Risk, contracts and forecast-driven decisions for your role** (lectures 4–7).\n\n"
      "Read the brief (`A2_brief_EN.pdf`) first. Choose the role closest to your company "
      "(B battery, H hydro, R solar, S supplier/industrial consumer). Public data only: do not use, and do not disclose, "
      "confidential company data.",
      "# Tema 2 EMQA — notebook de pornire\n"
      "**Risc, contracte și decizii bazate pe prognoze pentru rolul dumneavoastră** (cursurile 4–7).\n\n"
      "Citiți întîi enunțul (`A2_brief_RO.pdf`). Alegeți rolul cel mai apropiat de compania dumneavoastră "
      "(B baterie, H hidro, R solar, S furnizor/consumator industrial). Numai date publice: nu folosiți și nu divulgați "
      "date confidențiale ale companiei."),
    C("STUDENT_ID = 'TODO-your-student-ID'\nROLE = 'B'          # B, H, R or S\nMODE = 'personal'\n" + SETUP + r'''
p = ea.params(STUDENT_ID, 2, ROLE)
if MODE == "latest":
    p = ea.latest_window(p)
print(json.dumps(p, indent=1))
display(ea.data_version())
P, L, R = ea.panel("RO")
t0, t1 = pd.Timestamp(p["test_start"]), pd.Timestamp(p["test_end"])
s0, s1 = pd.Timestamp(p["selection_start"]), pd.Timestamp(p["selection_end"])
sel = pd.date_range(s0, s1, freq="D")     # (2) SELECTION: choose rule, alpha, w*, K, PPA prices, toll here only
test = pd.date_range(t0, t1, freq="D")    # (3) TEST: choices frozen; report results here only
fdays = pd.date_range(s0 - pd.Timedelta(days=p["burn_in_days"]), t1, freq="D")   # (1) burn-in + selection + test: forecast ALL of these
print("selection:", s0.date(), "->", s1.date(), "| test:", t0.date(), "->", t1.date())
'''),
    M("## Task 1 — Exposure profile (normalised public data)\n"
      "Use exactly the profile definition of your role in the brief (Table 1). Example below for each role.",
      "## Sarcina 1 — Profilul expunerii (date publice normalizate)\n"
      "Folosiți exact definiția profilului rolului dumneavoastră din enunț (tabelul 1). Mai jos, cîte un exemplu pentru fiecare rol."),
    C(r'''
if ROLE == "H":
    res = ea.day_matrix("hydro_water_reservoir")[ea.HOURS] * p["fleet_share"]   # MW = MWh per hour
    ror = ea.day_matrix("hydro_run_of_river")[ea.HOURS] * p["fleet_share"]
    Q = (res + ror).reindex(P.index)
elif ROLE == "R":
    s = ea.day_matrix("solar")[ea.HOURS]
    peak_ref = s.max(axis=1).rolling(365, min_periods=180).max().shift(2)       # trailing peak up to d-2 (metered at gate closure)
    Q = (s.div(peak_ref, axis=0).clip(upper=1) * p["pv_mwp"]).reindex(P.index)
elif ROLE == "S":
    l = ea.day_matrix("load")[ea.HOURS]
    ref = l.mean(axis=1).rolling(365, min_periods=180).mean().shift(2)     # trailing mean up to d-2
    Q = (l.div(ref, axis=0) * p["avg_load_mw"]).reindex(P.index)
else:
    Q = None   # battery: no exogenous volume; see Task 3
# TODO: monthly table 2023 -> test end: volume (MWh), cash flow (EUR), base price, capture price, capture rate
# TODO: clean spark spread table for the months of your test window (brief, eq. 1)
'''),
    M("## Task 2 — Probabilistic forecasts: LEAR (from Assignment 1) vs one machine-learning model",
      "## Sarcina 2 — Prognoze probabilistice: LEAR (din tema 1) vs un model de învățare automată"),
    C(r'''
F = {}        # "Naive", "LEAR", "<your ML model>"  -> DataFrame (fdays x 24)
Q99 = {}      # "<model> + CP" / "+ HS"            -> array (len(sel) + len(test), 24, 99): selection AND test days
T2 = pd.DataFrame(columns=["MAE", "RMSE", "APS", "cov50", "cov90"])
# TODO   (optional bonus: a foundation model such as Chronos-2 or TabPFN; record its version and pre-training cutoff)
'''),
    M("## Task 3 — Decision and decision ledger\nEvaluate every signal on the selection period, choose and FREEZE the rule (and alpha) there, "
      "then report all signals on the test period. One ledger row per test day. Required columns below.",
      "## Sarcina 3 — Decizia și registrul deciziilor\nEvaluați fiecare semnal pe perioada de selecție, alegeți și ÎNGHEȚAȚI acolo regula (și alpha), "
      "apoi raportați toate semnalele pe perioada de test. Un rînd în registru pe zi de test. Coloanele cerute sînt mai jos."),
    C(r'''
LEDGER_COLUMNS = ["date", "info_cutoff", "forecast_used", "decision", "volume_MWh", "settlement_price_summary",
                  "cash_flow_EUR", "baseline_cash_flow_EUR", "difference_EUR"]
ledger = pd.DataFrame(columns=LEDGER_COLUMNS)
# TODO: strategies: oracle (perfect foresight, upper bound only), naive, point forecast, (B and R) quantile rule for each alpha in p["risk_knob"]
def select_fn(P, L, R):
    """Your EX ANTE choices, computed from the SELECTION period only (days in `sel`). Return a dict, e.g.
    {"rule": "LEAR point", "alpha": None, "w_star": ..., "K": ..., "toll": ...}."""
    # TODO
    raise NotImplementedError
# ea.selection_check(select_fn, P, L, R, p)      # must print PASSED
'''),
    M("## Task 4 — Energy risk: price-volume decomposition, role risk, imbalance volume, RO-HU basis, CFaR",
      "## Sarcina 4 — Riscul energetic: descompunerea preț-volum, riscul rolului, volumul dezechilibrelor, baza RO-HU, CFaR"),
    C(r'''
# X: daily cash flow of your BASELINE exposure (brief, Table 1), from 2022 to test end (kEUR; battery: EUR)
HU = ea.day_matrix("HU")[ea.HOURS].reindex(P.index)      # Hungarian prices for the RO-HU basis
T4 = {}
# TODO: (a) monthly decomposition vs m-12, corr(volume, base price); (b) role risk; (c) imbalance volume with Q~[d,h] = Q[d-2,h] (last metered day);
#       (d) RO-HU spread statistics and figure; (e) monthly CFaR95 and daily CFaR95 / ES-type number
'''),
    M("## Task 5 — VaR and ES of your cash flow, Kupiec and Christoffersen backtests",
      "## Sarcina 5 — VaR și ES ale fluxului de numerar, testele Kupiec și Christoffersen"),
    C(r'''
T5 = pd.DataFrame(columns=["method", "alpha", "breaches", "expected", "Kupiec_p", "Christoffersen_p",
                           "mean_VaR", "mean_ES", "ES_gap_mean", "ES_gap_CI90"])
# TODO: HS, Normal, Monte Carlo AR(1,7)-GARCH(1,1)-t; window p["var_window"]; alphas p["alphas"]
#       information at gate closure: X only up to day d-2 (two-day-ahead forecast)
'''),
    M("## Task 6 — Contract or hedge design", "## Sarcina 6 — Proiectarea contractului sau a acoperirii riscului"),
    C("T6 = pd.DataFrame()\n# TODO (role-specific, see brief; H and S also with settlement on the HU base price)\n"
      "# K, w*, the PPA prices and the toll are fixed on the SELECTION period (select_fn); the table is computed on the TEST period\n"),
    M("## Task 7 — Robustness and adverse scenario", "## Sarcina 7 — Robustețe și scenariu advers"),
    C("ADVERSE = {}\n# TODO\n"),
    M("## Numbers for the memo", "## Numerele pentru memoriu"),
    C(r'''
MY_NUMBERS = {"params": p}
# TODO: add every table and number quoted in the memo, and the reconciliation of p["check_days"]
ledger.to_csv(f"ledger_{p['student_id']}_{ROLE}_{MODE}.csv", index=False)
with open(f"my_numbers_A2_{p['student_id']}_{ROLE}_{MODE}.json", "w") as fh:
    json.dump(MY_NUMBERS, fh, indent=1, default=str)
'''),
]


def build(cells, lang):
    n = nbf.v4.new_notebook()
    out = []
    for kind, content in cells:
        if kind == "md":
            out.append(nbf.v4.new_markdown_cell(content[lang]))
        else:
            out.append(nbf.v4.new_code_cell(content.strip("\n")))
    n.cells = out
    n.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    n.metadata["language_info"] = {"name": "python"}
    return n


if __name__ == "__main__":
    for name, cells in [("A1", A1), ("A2", A2)]:
        os.makedirs(os.path.join(HERE, name), exist_ok=True)
        for lang in ("en", "ro"):
            fn = os.path.join(HERE, name, f"{name}_starter_{lang.upper()}.ipynb")
            nbf.write(build(cells, lang), fn)
            print("written", fn)
