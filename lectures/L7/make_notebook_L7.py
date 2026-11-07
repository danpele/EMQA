"""
make_notebook_L7.py -- writes and executes the student notebooks of Lecture 7 (EMQA)
=====================================================================================
    notebooks/L7_notebook.ipynb      (English)
    notebooks/L7_notebook_ro.ipynb   (Romanian)
Same code in both; only the text differs. The model functions are copied verbatim from analysis_L7.py (extracted with the
ast module), so the notebook runs exactly the code behind the slides. Section numbers (§) match the "Experiment yourself"
pointers on the slides.

The full experiment (25 + 25 settings searched on the validation year, every setting re-run on the test year, monthly refits,
foundation models) takes about 10 minutes on 16 cores; it is cached by analysis_L7.py in lectures/L7/cache/ml.pkl. By default
the notebook READS that cache for the heavy runs and re-runs live one monthly refit of every model, checking that it
reproduces the cached forecasts; set RUN_ALL = True in §1 to recompute everything from scratch.
Run:  python3 lectures/L7/make_notebook_L7.py
"""

import ast
import os
import sys

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from colab_cell import add_colab_cell  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NBDIR = os.path.abspath(os.path.join(HERE, "..", "..", "notebooks"))
SRC = open(os.path.join(HERE, "analysis_L7.py"), encoding="utf-8").read()
TREE = ast.parse(SRC)


def fsrc(*names):
    """Source of top-level functions of analysis_L7.py, in the given order."""
    out = []
    for nm in names:
        node = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == nm)
        out.append(ast.get_source_segment(SRC, node))
    return "\n\n\n".join(out)


def cells(lang):
    def T(en, ro):
        return en if lang == "en" else ro

    md, code = nbformat.v4.new_markdown_cell, nbformat.v4.new_code_cell
    C = []
    C.append(md(T(
        "# Energy Markets Quantitative Analysis — Lecture 7: Machine learning for energy markets\n"
        "Prof. dr. Daniel Traian Pele — Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting\n\n"
        "This notebook reproduces the models, numbers and charts of Lecture 7 from the real data in `../data/clean` "
        "(see `../data/SOURCES.md`) and the benchmark forecasts of Lecture 2 (`../lectures/L2/cache/forecasts.pkl`). "
        "Section numbers (§) match the *Experiment yourself* pointers on the slides.\n\n"
        "**Rules used everywhere.** The forecast for delivery day *d* is made at 12:00 CET on *d−1*: prices are known up to *d−1*; "
        "realised load, wind, solar, hydro, nuclear and flows only up to *d−2*; carbon at the *d−2* close. Three samples in time "
        "order: training, a validation year (to choose settings) and the test year of Lecture 2 (to report). Seeds are fixed.\n\n"
        "**Running time.** By default the heavy runs are read from the cache written by `analysis_L7.py`; each section re-runs one "
        "monthly refit live and checks that it reproduces the cache. Set `RUN_ALL = True` in §1 to recompute everything (about 10 "
        "minutes on 16 cores).",
        "# Analiza cantitativă a piețelor de energie — Cursul 7: Învățarea automată pe piețele de energie\n"
        "Prof. dr. Daniel Traian Pele — Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică\n\n"
        "Acest notebook Jupyter reproduce modelele, cifrele și graficele din cursul 7, pe datele reale din `../data/clean` "
        "(vezi `../data/SOURCES.md`) și pe prognozele de referință din cursul 2 (`../lectures/L2/cache/forecasts.pkl`). "
        "Numerele secțiunilor (§) corespund indicațiilor *Exercițiu practic* de pe diapozitive.\n\n"
        "**Reguli folosite peste tot.** Prognoza pentru ziua de livrare *d* se face la ora 12:00 CET în ziua *d−1*: prețurile sînt "
        "cunoscute pînă în *d−1*; consumul, producția eoliană, solară, hidro, nucleară și fluxurile realizate, numai pînă în *d−2*; "
        "prețul certificatelor de emisii, la închiderea din *d−2*. Trei eșantioane în ordine cronologică: antrenare, un an de validare "
        "(pentru alegerea setărilor) și anul de test din cursul 2 (pentru raportare). Valorile inițiale (seed) sînt fixate.\n\n"
        "**Timpul de calcul.** Implicit, calculele lungi sînt citite din fișierul cache scris de `analysis_L7.py`; fiecare secțiune "
        "reface live o reestimare lunară și verifică faptul că reproduce cache-ul. Setați `RUN_ALL = True` în §1 pentru a recalcula "
        "totul (circa 10 minute pe 16 nuclee).")))

    # ---------------------------------------------------------------- §1
    C.append(md(T("## §1 Data, information set and the three samples", "## §1 Date, setul de informații și cele trei eșantioane")))
    C.append(code(
        "import numpy as np, pandas as pd, matplotlib.pyplot as plt, pickle, json, time, warnings\n"
        "from scipy import stats\nfrom joblib import Parallel, delayed\nwarnings.filterwarnings('ignore')\n"
        "RUN_ALL = False          # True: recompute every search and forecast (about 10 minutes on 16 cores)\n"
        "DATA = '../data/clean/'\nTZ = 'Europe/Brussels'\nSEED = 20261106\nN_JOBS = -1\n\n"
        "PD = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "G = pd.read_csv(DATA + 'generation_ro_mw_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "CB = pd.read_csv(DATA + 'crossborder_ro_mw_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "HP = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', index_col=0)\n"
        "GH = pd.read_csv(DATA + 'generation_ro_mw_hourly_utc.csv', index_col=0)\n"
        "EUA = pd.read_csv(DATA + 'eua_daily.csv', parse_dates=['date']).set_index('date')['eua_etc_co2l_eur_per_unit']\n"
        "raw_last = min(PD['RO'].dropna().index.max(), G['hydro_run_of_river'].dropna().index.max())\n"
        "END = pd.Timestamp(((raw_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())\n"
        "START = pd.Timestamp('2022-01-01')\nprint('cut-off (last complete month):', END.date())"))
    C.append(code(fsrc("day_matrix", "shift_rows", "mad_scale") + "\n\n\n"
                  "PM_ALL, _ = day_matrix(HP['RO'].dropna())\nPM, DST = day_matrix(HP['RO'].dropna())\n"
                  "LM, _ = day_matrix(GH['load'].dropna())\nRM, _ = day_matrix((GH['wind_onshore'] + GH['solar']).dropna())\n"
                  "CAL = pd.date_range(START, END, freq='D')\nPM, LM, RM = PM.reindex(CAL), LM.reindex(CAL), RM.reindex(CAL)\n"
                  "CAL_EX = pd.date_range(START - pd.Timedelta(days=30), END, freq='D')\n"
                  "FUND_RAW = pd.DataFrame({'hydro': (G['hydro_run_of_river'] + G['hydro_water_reservoir']).reindex(CAL_EX),\n"
                  "                         'nuclear': G['nuclear'].reindex(CAL_EX), 'netimp': CB['sum'].reindex(CAL_EX), 'eua': EUA.reindex(CAL_EX)})\n"
                  "FUND_AVAIL = FUND_RAW.ffill().shift(2).reindex(CAL)        # past values only, lagged 2 days\n"
                  "P_, L_, R_, F_ = (x.values.astype(float) for x in (PM, LM, RM, FUND_AVAIL))\n"
                  "DOW = CAL.dayofweek.values; IDX = {t: i for i, t in enumerate(CAL)}\n"
                  "PLAGS, XLAGS = (1, 2, 3, 7), (2, 3, 7)\nFIRST = 7\n"
                  "TEST0 = END - pd.Timedelta(days=364); VAL0 = TEST0 - pd.Timedelta(days=365)\n"
                  "TDAYS = pd.date_range(TEST0, END, freq='D'); VDAYS = pd.date_range(VAL0, TEST0 - pd.Timedelta(days=1), freq='D')\n"
                  "print('training from', CAL[FIRST].date(), '| validation', VAL0.date(), '-', VDAYS[-1].date(), '| test', TEST0.date(), '-', END.date())"))
    C.append(code(fsrc("blocks_of") + "\n\n\n"
                  "MB = blocks_of(TDAYS, 'M')                         # 12 monthly refits in the test year\n"
                  "_vm = blocks_of(VDAYS, 'M'); VB = [(_vm[k][0], _vm[k + 2][1]) for k in range(0, 12, 3)]   # 4 refits in the validation year\n"
                  "A = P_[[IDX[t] for t in TDAYS]]; AV = P_[[IDX[t] for t in VDAYS]]\n"
                  "fig, ax = plt.subplots(figsize=(10, 3))\n"
                  "ax.axvspan(CAL[FIRST], VAL0, color='g', alpha=0.1, label='training'); ax.axvspan(VAL0, TEST0, color='orange', alpha=0.25, label='validation year')\n"
                  "ax.axvspan(TEST0, END, color='r', alpha=0.15, label='test year'); ax.plot(PM.mean(1), lw=0.8, label='RO daily base price')\n"
                  "ax.set_ylabel('EUR/MWh'); ax.legend(ncol=4, loc='upper left'); plt.show()"))
    C.append(md(T("**Benchmarks of Lecture 2.** The forecasts of the naive model, AW-ARX, AW-LEAR and of the ensemble of 4 are read from "
                  "the cache of Lecture 2 (same test year, same information set) and checked against its published MAE.",
                  "**Modelele de referință din cursul 2.** Prognozele modelului naiv, AW-ARX, AW-LEAR și ale ansamblului de 4 modele sînt citite "
                  "din fișierul cache al cursului 2 (același an de test, același set de informații) și verificate față de MAE publicată.")))
    C.append(code(
        "FC2 = pickle.load(open('../lectures/L2/cache/forecasts.pkl', 'rb'))\nN2 = json.load(open('../lectures/L2/L2_numbers.json'))\n"
        "nb = N2['design']['n_burn']\nB = {k: v[nb:] for k, v in FC2['point'].items()}\n"
        "B['aw_arx'] = np.mean([B[f'arx{T}'] for T in (56, 84, 112, 714, 721, 728)], 0)\n"
        "B['aw_lear'] = np.mean([B[f'lear{T}'] for T in (364, 546, 728)], 0)\nB['gbm2'], B['mlp2'] = FC2['gbm'], FC2['mlp']\n"
        "B['ens4'] = np.mean([B['aw_arx'], B['aw_lear'], B['gbm2'], B['mlp2']], 0)\n"
        "mae = lambda F: np.mean(np.abs(A - F))\n"
        "for k in ['naive', 'aw_arx', 'aw_lear', 'ens4']: print(f'{k:8s} MAE {mae(B[k]):6.2f}')\n"
        "assert abs(mae(B['aw_lear']) - N2['acc']['aw_lear']['mae']) < 0.006"))

    # ---------------------------------------------------------------- §2
    C.append(md(T("## §2 Deep neural network: architecture, training, early stopping and random search",
                  "## §2 Rețeaua neuronală profundă: arhitectură, antrenare, oprire timpurie și căutare aleatoare")))
    C.append(md(T("The functions below are copied from `analysis_L7.py`. `dnn_block` fits on all days before the block, chooses the number "
                  "of epochs on the last 15% of the training days (chronological early stopping), refits on all days and forecasts the block.",
                  "Funcțiile de mai jos sînt copiate din `analysis_L7.py`. `dnn_block` estimează rețeaua pe toate zilele dinaintea blocului, alege "
                  "numărul de epoci pe ultimele 15% din zilele de antrenare (oprire timpurie, în ordine cronologică), reestimează pe toate zilele "
                  "și prognozează blocul.")))
    C.append(code(fsrc("dnn_inputs", "_net", "_train", "dnn_block", "dnn_predict_from", "dnn_space")))
    C.append(code(
        "DNN_SPACE = dnn_space()\nCACHE = '../lectures/L7/cache/ml.pkl'\n"
        "if RUN_ALL:\n"
        "    r = Parallel(n_jobs=N_JOBS)(delayed(dnn_block)(P_, L_, R_, F_, a, b, cfg) for cfg in DNN_SPACE for a, b in VB)\n"
        "    DNN_VAL = [np.vstack([r[c * 4 + j]['pred'] for j in range(4)]) for c in range(len(DNN_SPACE))]\n"
        "else:\n"
        "    Cc = pickle.load(open(CACHE, 'rb'))\n    DNN_VAL = Cc['dnn_val_pred']\n"
        "VAL_DNN = np.array([np.mean(np.abs(AV - p)) for p in DNN_VAL])\nBEST_DNN = int(np.argmin(VAL_DNN)); CFG_DNN = DNN_SPACE[BEST_DNN]\n"
        "print('validation MAE: best %.2f (setting %d), Lecture 2 setting %.2f' % (VAL_DNN.min(), BEST_DNN, VAL_DNN[0]))\nprint('chosen:', CFG_DNN)\n"
        "plt.figure(figsize=(8, 2.5)); plt.plot(np.sort(VAL_DNN), 'o'); plt.ylabel('validation MAE'); plt.xlabel('rank'); plt.show()"))
    C.append(md(T("**Live check.** Refit the chosen network for the last test month with 4 seeds and compare with the cache; then draw the "
                  "learning curve of seed 1.",
                  "**Verificare live.** Reestimăm rețeaua aleasă pentru ultima lună de test, cu 4 inițializări, și comparăm cu cache-ul; apoi "
                  "desenăm curba de învățare pentru inițializarea 1.")))
    C.append(code(
        "a, b = MB[-1]\nt0 = time.time(); r = dnn_block(P_, L_, R_, F_, a, b, CFG_DNN, (1, 2, 3, 4), keep=True)\n"
        "print('refit in %.1f s, epochs kept per seed:' % (time.time() - t0), r['epochs'])\n"
        "if not RUN_ALL:\n    print('max |live - cached| = %.5f EUR/MWh' % np.max(np.abs(r['pred'] - Cc['dnn_main'][-1]['pred'])))\n"
        "ctr, cv = r['curves'][0]\nplt.figure(figsize=(8, 2.5)); plt.plot(ctr, label='training days (first 85%)'); plt.plot(cv, label='early-stopping block (last 15%)')\n"
        "plt.axvline(np.argmin(cv), ls='--', color='k'); plt.ylabel('MAE, EUR/MWh'); plt.xlabel('epoch'); plt.legend(); plt.show()"))

    # ---------------------------------------------------------------- §3
    C.append(md(T("## §3 Gradient boosting (XGBoost)", "## §3 Gradient boosting (XGBoost)")))
    C.append(code("XGB_NAMES = " + repr(["P(d-1,h)", "P(d-2,h)", "P(d-3,h)", "P(d-7,h)", "P(d-1,23)", "min P(d-1)", "max P(d-1)", "mean P(d-1)",
                                         "L(d-2,h)", "L(d-7,h)", "RES(d-2,h)", "RES(d-7,h)", "mean L(d-2)", "mean RES(d-2)", "hydro(d-2)",
                                         "nuclear(d-2)", "net imports(d-2)", "EUA(d-2)", "hour", "day of week"]) + "\n\n\n" +
                  fsrc("gbm_rows", "_xgb", "xgb_block", "xgb_space")))
    C.append(code(
        "XGB_SPACE = xgb_space()\n"
        "if RUN_ALL:\n"
        "    r = Parallel(n_jobs=N_JOBS)(delayed(xgb_block)(P_, L_, R_, F_, a, b, cfg) for cfg in XGB_SPACE for a, b in VB)\n"
        "    XGB_VAL = [np.vstack([r[c * 4 + j]['pred'] for j in range(4)]) for c in range(len(XGB_SPACE))]\n"
        "else:\n    XGB_VAL = Cc['xgb_val_pred']\n"
        "VAL_XGB = np.array([np.mean(np.abs(AV - p)) for p in XGB_VAL])\nBEST_XGB = int(np.argmin(VAL_XGB)); CFG_XGB = XGB_SPACE[BEST_XGB]\n"
        "print('validation MAE: best %.2f, Lecture 2 setting %.2f' % (VAL_XGB.min(), VAL_XGB[0])); print('chosen:', CFG_XGB)\n"
        "a, b = MB[-1]; r = xgb_block(P_, L_, R_, F_, a, b, CFG_XGB)\n"
        "if not RUN_ALL: print('max |live - cached| = %.6f' % np.max(np.abs(r['pred'] - Cc['xgb_main'][-1]['pred'])))\n"
        "tr = np.arange(FIRST, a); m, s = mad_scale(P_[tr])\n"
        "mdl = _xgb(CFG_XGB, SEED).fit(gbm_rows(P_, L_, R_, F_, tr).reshape(-1, 20), np.arcsinh((P_[tr] - m) / s).ravel())\n"
        "td = mdl.get_booster().trees_to_dataframe(); root = td[(td.Tree == 0) & (td.Node == 0)].iloc[0]\n"
        "print('first question of the first tree:', XGB_NAMES[int(root.Feature[1:])], '<', round(root.Split, 1))"))

    # ---------------------------------------------------------------- §4
    C.append(md(T("## §4 Foundation models (Chronos), zero-shot", "## §4 Modele fundaționale (Chronos), fără reantrenare")))
    C.append(md(T("Needs the `chronos-forecasting` package and the model weights (downloaded once from Hugging Face). The context is the "
                  "last 2048 hourly prices up to the end of *d−1*; nothing after gate closure.",
                  "Necesită pachetul `chronos-forecasting` și ponderile modelului (descărcate o singură dată de pe Hugging Face). Contextul "
                  "este format din ultimele 2048 de prețuri orare, pînă la sfîrșitul zilei *d−1*; nimic de după închiderea licitației.")))
    C.append(code("CTX = 2048\n\n\n" + fsrc("chronos_forecasts")))
    C.append(code(
        "rows_all = np.array([IDX[t] for t in TDAYS])\n"
        "if RUN_ALL:\n    CHR2 = chronos_forecasts(P_, rows_all, 'amazon/chronos-2'); BOLT = chronos_forecasts(P_, rows_all, 'amazon/chronos-bolt-small')\n"
        "else:\n    CHR2, BOLT = Cc['chronos2'], Cc['chronos_bolt']\n"
        "try:\n    live = chronos_forecasts(P_, rows_all[:7], 'amazon/chronos-2')\n"
        "    print('first 7 test days, max |live - cached| = %.3f EUR/MWh' % np.max(np.abs(live['median'] - CHR2['median'][:7])))\n"
        "except Exception as e:\n    print('Chronos not available here, using the cache:', e)\n"
        "for k, F in [('naive', B['naive']), ('Chronos-Bolt', BOLT['median']), ('Chronos-2', CHR2['median']), ('AW-LEAR', B['aw_lear'])]:\n"
        "    print(f'{k:13s} MAE {mae(F):6.2f}')\n"
        "plt.figure(figsize=(8, 2.5))\n"
        "for k, F in [('naive', B['naive']), ('Chronos-2', CHR2['median']), ('AW-LEAR', B['aw_lear'])]: plt.plot(np.mean(np.abs(A - F), 0), marker='o', label=k)\n"
        "plt.xlabel('hour'); plt.ylabel('MAE'); plt.legend(); plt.show()"))

    # ---------------------------------------------------------------- §5
    C.append(md(T("## §5 Honest comparison: scoreboard, Diebold–Mariano tests, combinations, compute cost",
                  "## §5 Comparație corectă: clasament, teste Diebold–Mariano, combinații, cost de calcul")))
    C.append(code(fsrc("nw_var", "dm") + "\n\n\n"
                  "M = dict(B)\n"
                  "if RUN_ALL:\n"
                  "    M['dnn'] = np.vstack(Parallel(n_jobs=N_JOBS)(delayed(lambda a, b: dnn_block(P_, L_, R_, F_, a, b, CFG_DNN, (1, 2, 3, 4))['pred'])(a, b) for a, b in MB))\n"
                  "    M['xgb'] = np.vstack(Parallel(n_jobs=N_JOBS)(delayed(lambda a, b: xgb_block(P_, L_, R_, F_, a, b, CFG_XGB)['pred'])(a, b) for a, b in MB))\n"
                  "else:\n"
                  "    M['dnn'] = np.vstack([r['pred'] for r in Cc['dnn_main']]); M['xgb'] = np.vstack([r['pred'] for r in Cc['xgb_main']])\n"
                  "M['bolt'], M['chr2'] = BOLT['median'], CHR2['median']\n"
                  "M['ens_ldx'] = (M['aw_lear'] + M['dnn'] + M['xgb']) / 3\nM['ens_t4'] = np.mean([M['aw_arx'], M['aw_lear'], M['dnn'], M['xgb']], 0)\n"
                  "M['ens_lc'] = 0.5 * (M['aw_lear'] + M['chr2'])\n"
                  "E = {k: A - v for k, v in M.items()}\n"
                  "rows = []\nfor k in ['naive', 'aw_arx', 'aw_lear', 'ens4', 'gbm2', 'mlp2', 'xgb', 'dnn', 'bolt', 'chr2', 'ens_ldx', 'ens_t4', 'ens_lc']:\n"
                  "    rows.append([k, mae(M[k]), np.sqrt(np.mean(E[k] ** 2)), mae(M[k]) / mae(M['naive']), dm(E['aw_lear'], E[k])[1] if k != 'aw_lear' else np.nan])\n"
                  "print(pd.DataFrame(rows, columns=['model', 'MAE', 'RMSE', 'rMAE', 'DM p vs AW-LEAR']).round(3).to_string(index=False))"))
    C.append(code("w = np.linspace(0, 1, 21)\nplt.figure(figsize=(8, 2.5))\n"
                  "for k in ['dnn', 'xgb']: plt.plot(w, [mae(x * M[k] + (1 - x) * M['aw_lear']) for x in w], label='AW-LEAR + ' + k)\n"
                  "plt.xlabel('weight of the ML model (illustration: not chosen on the test year)'); plt.ylabel('MAE'); plt.legend(); plt.show()\n"
                  "print('error correlation with AW-LEAR:', {k: round(np.corrcoef(E['aw_lear'].ravel(), E[k].ravel())[0, 1], 2) for k in ['dnn', 'xgb', 'chr2']})\n"
                  "if not RUN_ALL:\n"
                  "    print('compute time for the test year, minutes on one core: XGBoost %.1f, DNN %.1f, Chronos-2 %.1f, AW-LEAR %.1f' % (\n"
                  "        sum(r['sec'] for r in Cc['xgb_main']) / 60, sum(r['sec'] for r in Cc['dnn_main']) / 60, Cc['chronos2']['sec'] / 60, Cc['lear_sec_day'] * 365 / 60))"))

    # ---------------------------------------------------------------- §6
    C.append(md(T("## §6 Explaining the forecasts: SHAP values and permutation importance",
                  "## §6 Explicarea prognozelor: valori SHAP și importanța prin permutare")))
    C.append(code(
        "import xgboost as xgb\nR6 = [xgb_block(P_, L_, R_, F_, a, b, CFG_XGB, shap=True) for a, b in MB] if RUN_ALL else Cc['xgb_main']\n"
        "SH = np.concatenate([r['shap'] for r in R6], 0)        # days x 24 x (20 inputs + bias), asinh scale\n"
        "share = np.abs(SH[:, :, :-1]).reshape(-1, 20).mean(0); share = share / share.sum() * 100\n"
        "o = np.argsort(-share)[:10][::-1]\nplt.figure(figsize=(8, 3)); plt.barh(range(10), share[o]); plt.yticks(range(10), [XGB_NAMES[j] for j in o])\n"
        "plt.xlabel('share of mean |SHAP|, %'); plt.show()\n"
        "XS = np.concatenate([r['X'] for r in R6], 0); j = XGB_NAMES.index('RES(d-2,h)')\n"
        "plt.figure(figsize=(8, 2.5)); plt.scatter(XS[:, :, j].ravel() / 1000, SH[:, :, j].ravel(), s=1, alpha=0.3)\n"
        "plt.xlabel('wind+solar d-2, same hour (GW)'); plt.ylabel('SHAP value'); plt.show()"))
    C.append(code(
        "if not RUN_ALL:\n"
        "    rows_all = np.array([IDX[t] for t in TDAYS]); XM = [dnn_inputs(P_, L_, R_, F_, rows_all, r['sc'], CFG_DNN) for r in Cc['dnn_main']]\n"
        "    names = XM[0][1]; base = mae(M['dnn']); rng = np.random.default_rng(SEED); perms = [rng.permutation(len(TDAYS)) for _ in range(5)]\n"
        "    def perm_block(cols_):\n"
        "        out = []\n"
        "        for pm in perms:\n"
        "            F = []\n"
        "            for jm, (a, b) in enumerate(MB):\n"
        "                X = XM[jm][0].copy(); X[:, cols_] = XM[jm][0][pm][:, cols_]; r = Cc['dnn_main'][jm]\n"
        "                F.append(dnn_predict_from(r['models'], CFG_DNN, X[a - MB[0][0]:b - MB[0][0] + 1], r['mu'], r['sg'], r['sc']))\n"
        "            out.append(mae(np.vstack(F)) - base)\n"
        "        return np.mean(out)\n"
        "    for blk in ['price d-1', 'price d-7', 'load', 'wind+solar', 'day of week']:\n"
        "        print(f'{blk:12s} {perm_block(np.where(names == blk)[0]):+6.2f} EUR/MWh')"))

    # ---------------------------------------------------------------- §7
    C.append(md(T("## §7 Spikes and negative prices: classifiers, ROC curves and the cost–loss rule",
                  "## §7 Vîrfuri și prețuri negative: clasificatori, curbe ROC și regula cost–pierdere")))
    C.append(code("THR_Q = 0.90\n\n\n" + fsrc("spike_threshold") + "\n\n\n"
                  "MONTH_START = {}\nfor _t in CAL:\n    MONTH_START.setdefault(_t.to_period('M'), _t.replace(day=1))\n"
                  "THETA = np.array([spike_threshold(MONTH_START[t.to_period('M')]) for t in CAL])\n"
                  "CLF_NAMES = XGB_NAMES + ['threshold']\nCLF_CFG = {'n_est': 400, 'eta': 0.05, 'depth': 4, 'mcw': 20, 'sub': 0.8, 'col': 0.8, 'lam': 1.0}\n\n\n" +
                  fsrc("clf_rows", "clf_block")))
    C.append(code(
        "from sklearn.metrics import roc_auc_score, roc_curve\n"
        "RS = Parallel(n_jobs=N_JOBS)(delayed(clf_block)(P_, L_, R_, F_, THETA, a, b, 'spike') for a, b in MB) if RUN_ALL else Cc['clf_spike']\n"
        "PS = np.vstack([r['xgb'] for r in RS]); PL = np.vstack([r['logit'] for r in RS])\n"
        "TH = THETA[rows_all]; Y = (A > TH[:, None]).astype(int)\n"
        "persist = (np.stack([P_[rows_all - k] for k in range(1, 8)]) > TH[None, :, None]).mean(0)\n"
        "print('spike share in the test year: %.1f%%' % (100 * Y.mean()))\n"
        "for k, sc in [('XGBoost', PS), ('logistic', PL), ('persistence', persist), ('AW-LEAR - theta', M['aw_lear'] - TH[:, None])]:\n"
        "    print(f'{k:16s} AUC {roc_auc_score(Y.ravel(), sc.ravel()):.3f}')\n"
        "a, b = MB[-1]; live = clf_block(P_, L_, R_, F_, THETA, a, b, 'spike')\n"
        "if not RUN_ALL: print('live refit, max |difference| in probability:', np.max(np.abs(live['xgb'] - Cc['clf_spike'][-1]['xgb'])))\n"
        "# cost-loss rule: act if probability > C / Lbar, value = sum over alerts of (P - theta - C)\n"
        "C_ACT = 30.0; vr = np.array([IDX[t] for t in VDAYS]); PV, THV = P_[vr], THETA[vr][:, None]\n"
        "LBAR = (PV - THV)[PV > THV].mean(); cut = C_ACT / LBAR; VALUE = A - TH[:, None] - C_ACT\n"
        "print('C/L = %.3f; value per MW and year: %.1f thousand EUR (perfect foresight %.1f)' % (cut, VALUE[PS > cut].sum() / 1000, VALUE[VALUE > 0].sum() / 1000))"))

    # ---------------------------------------------------------------- §8
    C.append(md(T("## §8 Case study: the highest price of the test year", "## §8 Studiu de caz: cel mai mare preț din anul de test")))
    C.append(code(
        "kd, kh = np.unravel_index(np.argmax(A), A.shape)\nprint('day', TDAYS[kd].date(), 'hour', kh, 'price %.2f' % A[kd, kh])\n"
        "for k in ['naive', 'aw_lear', 'xgb', 'dnn', 'chr2']: print(f'{k:8s} forecast {M[k][kd, kh]:7.1f}')\n"
        "print('spike probability (XGBoost): %.3f' % PS[kd, kh])\n"
        "phi = SH[kd, kh, :-1]; y0 = SH[kd, kh, -1]; m_, s_ = R6[[i for i, (a, b) in enumerate(MB) if a <= rows_all[kd] <= b][0]]['m'], R6[[i for i, (a, b) in enumerate(MB) if a <= rows_all[kd] <= b][0]]['s']\n"
        "P0, PH = m_ + s_ * np.sinh(y0), m_ + s_ * np.sinh(y0 + phi.sum()); phi_eur = phi * (PH - P0) / phi.sum()\n"
        "for j in np.argsort(-np.abs(phi_eur))[:5]: print(f'{XGB_NAMES[j]:18s} value {XS[kd, kh, j]:8.1f}  contribution {phi_eur[j]:+7.1f} EUR/MWh')"))

    # ---------------------------------------------------------------- §9
    C.append(md(T("## §9 Pitfalls: look-ahead, shuffled cross-validation, data snooping, retraining",
                  "## §9 Capcane: informația din viitor, validarea încrucișată amestecată, alegerea pe anul de test, reestimarea")))
    C.append(code(
        "a, b = MB[-1]\nhon = xgb_block(P_, L_, R_, F_, a, b, CFG_XGB)['pred']; lk = xgb_block(P_, L_, R_, F_, a, b, CFG_XGB, leak=True)['pred']\n"
        "Am = P_[a:b + 1]\nprint('last month: honest MAE %.2f, with same-day load and wind+solar %.2f' % (np.mean(np.abs(Am - hon)), np.mean(np.abs(Am - lk))))\n"
        "if not RUN_ALL:\n"
        "    for k in ['xgb_leak', 'xgb_quarterly', 'xgb_once', 'xgb_roll365', 'xgb_roll730']:\n"
        "        print(f'{k:14s} MAE {mae(np.vstack([r[\"pred\"] for r in Cc[k]])):6.2f}')\n"
        "    print('shuffled 5-fold   MAE %.2f' % mae(Cc['xgb_shuffled'][rows_all]))\n"
        "    TD = np.array([mae(p) for p in Cc['dnn_test_all']])\n"
        "    print('DNN: chosen on validation %.2f; best of %d settings on the test year %.2f (snooping)' % (TD[BEST_DNN], len(TD), TD.min()))\n"
        "    print('Spearman correlation validation vs test: %.2f' % stats.spearmanr(VAL_DNN, TD)[0])"))

    # ---------------------------------------------------------------- §10
    C.append(md(T("## §10 Leakage self-check", "## §10 Verificarea scurgerii de informație")))
    C.append(code(
        "def corrupt(i, fill=np.nan):\n"
        "    Pc, Lc, Rc = P_.copy(), L_.copy(), R_.copy(); Pc[i:] = fill; Lc[i - 1:] = fill; Rc[i - 1:] = fill\n"
        "    raw = FUND_RAW.copy(); raw.loc[CAL[i - 1]:] = fill\n"
        "    return Pc, Lc, Rc, raw.ffill().shift(2).reindex(CAL).values.astype(float)\n"
        "a = MB[-1][0]\nfor fill in (np.nan, 1e4):\n"
        "    g = xgb_block(*corrupt(a, fill), a, a, CFG_XGB)['pred'][0]\n"
        "    print('fill', fill, '-> max |difference| XGBoost: %.2e' % np.max(np.abs(g - M['xgb'][a - MB[0][0]])))"))
    C.append(md(T(
        "## Exercises\n1. Change the validation year to the 6 months before the test year: does the chosen setting change? Does the test MAE?\n"
        "2. Add AW-ARX to the LEAR + Chronos-2 combination. Is the gain significant (DM test)?\n"
        "3. Set the action cost C to 60 EUR/MWh in §7. How many alerts are left, and what is the value per MW?\n"
        "4. Replace the spike threshold (90th percentile) by a fixed 200 EUR/MWh. How do the AUC values change?",
        "## Exerciții\n1. Folosiți ca an de validare doar cele 6 luni dinaintea anului de test: se schimbă setarea aleasă? Dar MAE pe anul de test?\n"
        "2. Adăugați AW-ARX la combinația LEAR + Chronos-2. Este cîștigul semnificativ (testul DM)?\n"
        "3. Setați costul reacției C la 60 EUR/MWh în §7. Cîte alerte rămîn și care este valoarea pe MW?\n"
        "4. Înlocuiți pragul de vîrf (percentila 90) cu un prag fix de 200 EUR/MWh. Cum se modifică valorile AUC?")))
    return C


def build(lang):
    nb = nbformat.v4.new_notebook()
    nb.cells = cells(lang)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    add_colab_cell(nb, lang)
    ExecutePreprocessor(timeout=3600, kernel_name="python3").preprocess(nb, {"metadata": {"path": NBDIR}})
    out = os.path.join(NBDIR, "L7_notebook.ipynb" if lang == "en" else "L7_notebook_ro.ipynb")
    nbformat.write(nb, out)
    print("wrote", out)


if __name__ == "__main__":
    for lg in ("en", "ro"):
        build(lg)
