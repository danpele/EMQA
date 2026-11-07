"""
make_notebook_L2.py -- writes and executes the student notebooks of Lecture 2 (EMQA)
=====================================================================================
    notebooks/L2_notebook.ipynb      (English)
    notebooks/L2_notebook_ro.ipynb   (Romanian)
Same code in both; only the text differs. The model functions are copied verbatim from analysis_L2.py (extracted with
the ast module), so the notebook runs exactly the code behind the slides. Paths are relative to notebooks/ (data in
../data/clean). Section numbers match the "Experiment yourself" pointers on the slides. The forecasting engine (§1) runs
in parallel with joblib and takes a few minutes on a laptop with several cores.
Run:  python3 lectures/L2/make_notebook_L2.py
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
SRC = open(os.path.join(HERE, "analysis_L2.py"), encoding="utf-8").read()
TREE = ast.parse(SRC)


def fsrc(*names):
    """Source of top-level functions of analysis_L2.py, in the given order."""
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
        "# Energy Markets Quantitative Analysis — Lecture 2: Forecasting electricity prices\n"
        "Prof. dr. Daniel Traian Pele — Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting\n\n"
        "This notebook reproduces the forecasts, numbers and charts of Lecture 2 from the real data in `../data/clean` "
        "(see `../data/SOURCES.md`). Section numbers (§) match the *Experiment yourself* pointers on the slides.\n\n"
        "**Rules used everywhere.** Forecast of delivery day *d* made at 12:00 CET on *d−1*: prices known up to *d−1*, realised "
        "load, wind, solar, hydro, nuclear and flows only up to *d−2*, carbon at the *d−2* close. Chronological order, no shuffling, "
        "no random validation split; every transformation is fitted inside the calibration window. Seeds are fixed.",
        "# Analiza cantitativă a piețelor de energie — Cursul 2: Prognoza prețurilor energiei electrice\n"
        "Prof. dr. Daniel Traian Pele — Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică\n\n"
        "Acest notebook Jupyter reproduce prognozele, numerele și graficele din Cursul 2 pe datele reale din `../data/clean` "
        "(vezi `../data/SOURCES.md`). Numerele secțiunilor (§) corespund indicațiilor *Încercați singuri* de pe diapozitive.\n\n"
        "**Reguli folosite peste tot.** Prognoza pentru ziua de livrare *d* se face la ora 12:00 CET în ziua *d−1*: prețurile sînt "
        "cunoscute pînă în *d−1*, consumul, producția eoliană, solară, hidro, nucleară și fluxurile realizate numai pînă în *d−2*, "
        "carbonul la închiderea din *d−2*. Ordine cronologică, fără amestecarea datelor, fără eșantion de validare aleator; orice "
        "transformare se estimează în fereastra de calibrare. Valorile inițiale (seed) sînt fixate.")))

    # ---------------------------------------------------------------- §1
    C.append(md(T("## §1 Data, information set and the forecasting engine",
                  "## §1 Date, setul de informații și motorul de prognoză")))
    C.append(code(
        "import numpy as np, pandas as pd, matplotlib.pyplot as plt, statsmodels.api as sm, json, time, warnings\n"
        "from scipy import stats\nfrom joblib import Parallel, delayed\n"
        "from statsmodels.regression.quantile_regression import QuantReg\n"
        "from statsmodels.tsa.stattools import adfuller, coint\nfrom statsmodels.tsa.vector_ar.vecm import coint_johansen\n"
        "warnings.filterwarnings('ignore')\n"
        "DATA = '../data/clean/'\nTZ = 'Europe/Brussels'\nSEED = 20261105\n\n"
        "PD = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "G = pd.read_csv(DATA + 'generation_ro_mw_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "CB = pd.read_csv(DATA + 'crossborder_ro_mw_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "HP = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', index_col=0)\n"
        "GH = pd.read_csv(DATA + 'generation_ro_mw_hourly_utc.csv', index_col=0)\n"
        "EUA = pd.read_csv(DATA + 'eua_daily.csv', parse_dates=['date']).set_index('date')['eua_etc_co2l_eur_per_unit']\n"
        "raw_last = min(PD['RO'].dropna().index.max(), G['hydro_run_of_river'].dropna().index.max())\n"
        "END = pd.Timestamp(((raw_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())\n"
        "START = pd.Timestamp('2022-01-01')\nprint('cut-off (last complete month):', END.date())"))
    C.append(md(T("**Panel.** One row per CET delivery day, 24 hourly columns (after 1 Oct 2025 each hour is the mean of its four "
                  "quarter-hours). DST convention of Assignment 1: the missing spring hour is the mean of its neighbours, the doubled "
                  "autumn hour is averaged.",
                  "**Panelul.** Un rînd pe zi de livrare CET, 24 de coloane orare (după 1 octombrie 2025, fiecare oră este media celor "
                  "patru sferturi de oră). Convenția DST din tema 1: ora lipsă din martie este media orelor vecine, ora dublată din "
                  "octombrie este mediată.")))
    C.append(code(fsrc("day_matrix") + "\n\n\n"
                  "PM, DST = day_matrix(HP['RO'].dropna())\nLM, _ = day_matrix(GH['load'].dropna())\n"
                  "RM, _ = day_matrix((GH['wind_onshore'] + GH['solar']).dropna())\n"
                  "CAL = pd.date_range(START, END, freq='D')\n"
                  "PM, LM, RM, DST = PM.reindex(CAL), LM.reindex(CAL), RM.reindex(CAL), DST.reindex(CAL)\n"
                  "assert not PM.isna().any().any() and not LM.isna().any().any() and not RM.isna().any().any()\n"
                  "# daily fundamentals: value usable for day d = last observation on or before d-2 (past only)\n"
                  "CAL_EX = pd.date_range(START - pd.Timedelta(days=30), END, freq='D')\n"
                  "FUND_RAW = pd.DataFrame({'hydro': (G['hydro_run_of_river'] + G['hydro_water_reservoir']).reindex(CAL_EX),\n"
                  "                         'nuclear': G['nuclear'].reindex(CAL_EX), 'netimp': CB['sum'].reindex(CAL_EX),\n"
                  "                         'eua': EUA.reindex(CAL_EX)})\n"
                  "FUND_AVAIL = FUND_RAW.ffill().shift(2).reindex(CAL)\n"
                  "N_TEST, N_BURN = 365, 182\nTEST0 = END - pd.Timedelta(days=N_TEST - 1)\nFC0 = TEST0 - pd.Timedelta(days=N_BURN)\n"
                  "FDAYS = pd.date_range(FC0, END, freq='D'); TDAYS = pd.date_range(TEST0, END, freq='D')\n"
                  "P_, L_, R_, F_ = (x.values.astype(float) for x in (PM, LM, RM, FUND_AVAIL))\n"
                  "DOW = CAL.dayofweek.values; IDX = {t: i for i, t in enumerate(CAL)}\nPLAGS, XLAGS = (1, 2, 3, 7), (2, 3, 7)\n"
                  "print('panel', CAL[0].date(), '-', CAL[-1].date(), len(CAL), 'days | test', TEST0.date(), '-', END.date(),\n"
                  "      '| burn-in from', FC0.date(), '| DST days in test:', [t.date() for t in TDAYS[DST.loc[TDAYS].values]])\n"
                  "daily = PM.mean(1)\nfig, ax = plt.subplots(figsize=(10, 3))\n"
                  "ax.axvspan(FC0 - pd.Timedelta(days=728), FC0, color='g', alpha=0.1, label='728-day window (first forecast)')\n"
                  "ax.axvspan(FC0, TEST0, color='orange', alpha=0.25, label='burn-in'); ax.axvspan(TEST0, END, color='r', alpha=0.15, label='test')\n"
                  "ax.plot(daily, lw=0.8, label='RO daily base price'); ax.set_ylabel('EUR/MWh'); ax.legend(ncol=4, loc='upper left'); plt.show()"))
    C.append(md(T("**The models** (functions copied from `analysis_L2.py`): naive and seasonal naive, expert ARX (Assignment 1 "
                  "specification) for six windows and four variants, LEAR with 247 regressors and $\\lambda$ by AIC, gradient "
                  "boosting and a 24-output neural network refitted monthly. Each function only uses rows available at gate closure; "
                  "§10 checks it.",
                  "**Modelele** (funcții copiate din `analysis_L2.py`): naiv și naiv sezonier, ARX expert (specificația din tema 1) "
                  "pentru șase ferestre și patru variante, LEAR cu 247 de regresori și $\\lambda$ ales prin AIC, gradient boosting și o "
                  "rețea neuronală cu 24 de ieșiri, reestimate lunar. Fiecare funcție folosește numai rîndurile disponibile la "
                  "închiderea porții; §10 verifică acest lucru.")))
    C.append(code("ARX_W = (56, 84, 112, 714, 721, 728)\nLEAR_W = (364, 546, 728)\n"
                  "GBM_NAMES = ['P(d-1,h)', 'P(d-2,h)', 'P(d-3,h)', 'P(d-7,h)', 'P(d-1,23)', 'min P(d-1)', 'max P(d-1)', 'mean P(d-1)',\n"
                  "             'L(d-2,h)', 'L(d-7,h)', 'RES(d-2,h)', 'RES(d-7,h)', 'mean L(d-2)', 'mean RES(d-2)', 'hydro(d-2)', 'nuclear(d-2)',\n"
                  "             'net imports(d-2)', 'EUA(d-2)', 'hour', 'day of week']\n\n\n" +
                  fsrc("shift_rows", "mad_scale", "arx_day", "lear_design", "lear_day", "point_day", "run_chunk", "gbm_rows",
                       "gbm_month", "mlp_design", "mlp_month", "month_blocks")))
    C.append(code(
        "t0 = time.time()\nii = [IDX[t] for t in FDAYS]\n"
        "res = Parallel(n_jobs=-1)(delayed(run_chunk)(P_, L_, R_, F_, ii[k::16]) for k in range(16))\n"
        "allr = {}\nfor r_ in res: allr.update(r_)\n"
        "names = [k for k in allr[ii[0]] if k not in ('arx_coef', 'lear_nz')]\n"
        "PT = {k: np.array([allr[i][k] for i in ii]) for k in names}\n"
        "ARX_COEF = np.array([allr[i]['arx_coef'] for i in ii]); LEAR_NZ = np.array([allr[i]['lear_nz'] for i in ii])\n"
        "MB = month_blocks(TDAYS)\n"
        "G_RES = Parallel(n_jobs=-1)(delayed(gbm_month)(P_, L_, R_, F_, a, b) for a, b in MB)\n"
        "M_RES = Parallel(n_jobs=-1)(delayed(mlp_month)(P_, L_, R_, F_, a, b) for a, b in MB)\n"
        "print('engine done in %.0f s' % (time.time() - t0))\n\n"
        "POS = {t: k for k, t in enumerate(FDAYS)}; TI = np.array([POS[t] for t in TDAYS])\n"
        "ACT_F = P_[ii]; A = ACT_F[TI]\n"
        "PT['aw_arx'] = np.mean([PT[f'arx{T}'] for T in ARX_W], 0); PT['aw_lear'] = np.mean([PT[f'lear{T}'] for T in LEAR_W], 0)\n"
        "M = {k: v[TI] for k, v in PT.items()}\n"
        "M['gbm'] = np.vstack([g[0] for g in G_RES]); M['mlp'] = np.vstack([m[0] for m in M_RES])\n"
        "M['ens_lm'] = 0.5 * (M['aw_lear'] + M['mlp']); M['ens_all'] = np.mean([M['aw_arx'], M['aw_lear'], M['gbm'], M['mlp']], 0)\n"
        "print('test hours:', A.size, '| mean price %.2f EUR/MWh' % A.mean())"))

    # ---------------------------------------------------------------- §2
    C.append(md(T("## §2 Benchmarks, horizons, error measures and the Diebold–Mariano test",
                  "## §2 Modele de referință, orizonturi, măsuri ale erorii și testul Diebold–Mariano")))
    C.append(code(
        "dw = TDAYS.dayofweek.values; lag1 = P_[np.array([IDX[t] for t in TDAYS]) - 1]\n"
        "for nm, msk in [('Mon/Sat/Sun', np.isin(dw, [0, 5, 6])), ('Tue-Fri', ~np.isin(dw, [0, 5, 6]))]:\n"
        "    print(nm, '| MAE d-1 %.2f | MAE d-7 %.2f' % (np.abs(A[msk] - lag1[msk]).mean(), np.abs(A[msk] - M['snaive'][msk]).mean()))\n"
        "hz = {k: np.abs(A - P_[np.array([IDX[t] for t in TDAYS]) - k]).mean() for k in range(1, 15)}\n"
        "plt.figure(figsize=(9, 2.5)); plt.bar(list(hz), list(hz.values())); plt.xlabel('k (days)'); plt.ylabel('MAE'); plt.show()\n"
        "print({k: round(v, 2) for k, v in hz.items()})"))
    C.append(code(
        "def acc(F):\n"
        "    e = A - F; den = np.abs(A) + np.abs(F); nz = np.abs(A) > 0\n"
        "    return {'MAE': np.abs(e).mean(), 'RMSE': np.sqrt((e ** 2).mean()),\n"
        "            'sMAPE %': (2 * np.abs(e[den > 0]) / den[den > 0]).mean() * 100, 'MAPE %': (np.abs(e[nz]) / np.abs(A[nz])).mean() * 100}\n"
        "ORDER = ['naive', 'snaive', 'arx56', 'arx84', 'arx112', 'arx714', 'arx721', 'arx728', 'aw_arx', 'arx728_noexog', 'arx728_fund',\n"
        "         'arx728_raw', 'arx728_single', 'lear364', 'lear546', 'lear728', 'aw_lear', 'gbm', 'mlp', 'ens_lm', 'ens_all']\n"
        "TAB = pd.DataFrame({k: acc(M[k]) for k in ORDER}).T\nTAB['rMAE'] = TAB['MAE'] / TAB.loc['naive', 'MAE']\nprint(TAB.round(3))"))
    C.append(code(
        "ape = np.abs(A - M['aw_lear']) / np.abs(A); ape[~np.isfinite(ape)] = np.nan; small = np.abs(A) < 5\n"
        "print('MAPE AW-LEAR %.1f%% | without |P|<5: %.1f%% | share from |P|<5: %.1f%% (%d hours)' % (\n"
        "      np.nanmean(ape) * 100, np.nanmean(ape[~small]) * 100, np.nansum(ape[small]) / np.nansum(ape) * 100, small.sum()))\n"
        "plt.figure(figsize=(9, 3)); plt.scatter(A.ravel(), ape.ravel() * 100, s=1); plt.yscale('log'); plt.xlabel('price'); plt.ylabel('APE %'); plt.show()"))
    C.append(code(
        fsrc("nw_var", "dm") + "\n\n\n"
        "DM_MODELS = ['naive', 'snaive', 'arx728', 'aw_arx', 'lear728', 'aw_lear', 'gbm', 'mlp', 'ens_lm', 'ens_all']\n"
        "E = {k: A - M[k] for k in ORDER}\n"
        "DMP = pd.DataFrame([[np.nan if a == b else dm(E[a], E[b])[1] for b in DM_MODELS] for a in DM_MODELS], index=DM_MODELS, columns=DM_MODELS)\n"
        "print('p-values: is the COLUMN model more accurate than the ROW model?'); print(DMP.round(3))\n"
        "for a, b in [('naive', 'aw_lear'), ('aw_arx', 'aw_lear'), ('aw_lear', 'ens_all')]:\n"
        "    print(a, 'vs', b, 'DM = %.2f, p = %.4f' % dm(E[a], E[b]))"))

    # ---------------------------------------------------------------- §3
    C.append(md(T("## §3 The expert ARX model: coefficients, exogenous variables, one model per hour, VST",
                  "## §3 Modelul expert ARX: coeficienți, variabile exogene, un model pe oră, VST")))
    C.append(code(
        "co = ARX_COEF[TI].mean(0)\ncnames = ['const', 'Y(d-1,h)', 'Y(d-2,h)', 'Y(d-7,h)', 'Y(d-1,23)', 'Ymin', 'Ymax', 'L(d-2)', 'RES(d-2)', 'Mon', 'Sat', 'Sun']\n"
        "pd.DataFrame(co[:23], columns=cnames)[['Y(d-1,h)', 'Y(d-2,h)', 'Y(d-7,h)', 'L(d-2)', 'RES(d-2)']].plot(marker='o', figsize=(9, 3)); plt.xlabel('hour'); plt.show()\n"
        "print(TAB.loc[['arx728_noexog', 'arx728', 'arx728_fund', 'arx728_single', 'arx728_raw'], ['MAE', 'RMSE', 'rMAE']].round(3))\n"
        "bh = pd.DataFrame({k: np.abs(A - M[k]).mean(0) for k in ['naive', 'arx728', 'arx728_single']})\n"
        "print('hours where one pooled model is worse:', int((bh['arx728_single'] > bh['arx728']).sum()), 'of 24'); bh.plot(marker='o', figsize=(9, 3)); plt.show()"))

    # ---------------------------------------------------------------- §4
    C.append(md(T("## §4 LEAR: which of the 247 regressors does the LASSO keep?", "## §4 LEAR: ce regresori din cei 247 păstrează LASSO?")))
    C.append(code(
        "NZ = LEAR_NZ[TI]; nnz = NZ.sum(2)\n"
        "print('non-zero coefficients: mean %.1f, min %d, max %d of %d' % (nnz.mean(), nnz.min(), nnz.max(), NZ.shape[2]))\n"
        "groups = {'P(d-1) same hour': [None], 'P(d-1) other hours': [None], 'P(d-2)': range(24, 48), 'P(d-3)': range(48, 72),\n"
        "          'P(d-7)': range(72, 96), 'load': range(96, 168), 'wind+solar': range(168, 240), 'day of week': range(240, 247)}\n"
        "SEL = pd.DataFrame(index=groups, columns=range(24), dtype=float)\n"
        "for g, cols in groups.items():\n"
        "    for h in range(24):\n"
        "        c = [h] if g == 'P(d-1) same hour' else ([j for j in range(24) if j != h] if g == 'P(d-1) other hours' else list(cols))\n"
        "        SEL.loc[g, h] = NZ[:, h, c].mean() * 100\n"
        "print(SEL.mean(1).round(1)); plt.figure(figsize=(9, 3)); plt.imshow(SEL.values, aspect='auto', cmap='Blues');\n"
        "plt.yticks(range(len(groups)), list(groups)); plt.colorbar(); plt.show()"))

    # ---------------------------------------------------------------- §5
    C.append(md(T("## §5 Calibration windows and combinations", "## §5 Ferestre de calibrare și combinații")))
    C.append(code(
        "print(TAB.loc[[f'arx{T}' for T in ARX_W] + ['aw_arx'] + [f'lear{T}' for T in LEAR_W] + ['aw_lear'], ['MAE', 'rMAE']].round(3))\n"
        "TM = TDAYS.to_period('M')\nbym = pd.DataFrame({k: [np.abs(A[TM == m] - M[k][TM == m]).mean() for m in sorted(set(TM))] for k in ORDER}, index=sorted(set(TM)))\n"
        "print('ensemble of 4 better than AW-LEAR in', int((bym['ens_all'] < bym['aw_lear']).sum()), 'of 12 months')\n"
        "print('scoreboard'); print(TAB.loc[['naive', 'snaive', 'arx56', 'arx728', 'aw_arx', 'arx728_single', 'arx728_raw', 'lear364',\n"
        "      'lear728', 'aw_lear', 'gbm', 'mlp', 'ens_lm', 'ens_all'], ['MAE', 'RMSE', 'sMAPE %', 'rMAE']].round(3))\n"
        "nodst = ~DST.loc[TDAYS].values; print('AW-LEAR MAE without DST days: %.2f' % np.abs(A[nodst] - M['aw_lear'][nodst]).mean())"))

    # ---------------------------------------------------------------- §6
    C.append(md(T("## §6 Machine learning: gradient boosting and a neural network (preview of Lecture 7)",
                  "## §6 Învățare automată: gradient boosting și o rețea neuronală (introducere la cursul 7)")))
    C.append(code(
        "bh = pd.DataFrame({k: np.abs(A - M[k]).mean(0) for k in ['aw_lear', 'gbm', 'mlp', 'ens_all']})\n"
        "print('hours better than AW-LEAR:', {k: int((bh[k] < bh['aw_lear']).sum()) for k in ['gbm', 'mlp', 'ens_all']})\n"
        "print('MLP epochs chosen on the chronological validation block:', [m[1] for m in M_RES])\n"
        "bh.plot(marker='o', figsize=(9, 3)); plt.ylabel('MAE'); plt.show()\n"
        "c2 = json.load(open('../cases/C2_load_forecasting/numbers.json'))\n"
        "print('case study C2 (load): MAPE GBM %.2f, Chronos %.2f, MLP %.2f, linear %.2f, SARIMA %.2f, naive 48h %.2f' % (\n"
        "      c2['gbmMAPE'], c2['chronosMAPE'], c2['mlpMAPE'], c2['linMAPE'], c2['sarimaMAPE'], c2['naiveMAPE']))"))

    # ---------------------------------------------------------------- §7
    C.append(md(T("## §7 Probabilistic forecasts: QRA, conformal prediction, historical simulation",
                  "## §7 Prognoze probabilistice: QRA, predicție conformală, simulare istorică")))
    C.append(code(
        "TAUS = np.arange(1, 100) / 100; W_QRA, W_ERR = 182, 112\nFA, FL_ = PT['aw_arx'], PT['aw_lear']\n"
        "WEEK0 = list(range(N_BURN, len(FDAYS), 7))\n\n\n" + fsrc("qra_hour") + "\n\n\n"
        "QRA = np.sort(np.stack(Parallel(n_jobs=-1)(delayed(qra_hour)(h) for h in range(24)), 1)[TI], axis=2)\n"
        "ERR_L = ACT_F - FL_\nCPQ = np.zeros((len(TDAYS), 24, 99)); HSQ = np.zeros_like(CPQ)\n"
        "for k, t in enumerate(TI):\n"
        "    win = ERR_L[t - W_ERR:t]\n"
        "    for j, tau in enumerate(TAUS):\n"
        "        HSQ[k, :, j] = FL_[t] + np.quantile(win, tau, axis=0)\n"
        "        CPQ[k, :, j] = FL_[t] + np.sign(tau - 0.5) * np.quantile(np.abs(win), abs(2 * tau - 1), axis=0)\n\n\n" +
        fsrc("prob_scores") + "\n\n\n"
        "for nm, Qx in [('QRA', QRA), ('CP', CPQ), ('HS', HSQ)]:\n"
        "    r = prob_scores(Qx); print(nm, {k: round(v, 3) for k, v in r.items() if k != 'rel'})\n"
        "    plt.plot(TAUS, np.array(r['rel']) - TAUS, label=nm)\n"
        "plt.axhline(0, color='k'); plt.legend(); plt.xlabel('tau'); plt.ylabel('share below - tau'); plt.show()\n"
        "c = np.corrcoef((A - M['aw_lear']).T); print('error correlation 12-13 h %.2f, 3-19 h %.2f' % (c[12, 13], c[3, 19]))"))

    # ---------------------------------------------------------------- §8
    C.append(md(T("## §8 Cointegration: Romania–Hungary (daily) and power–gas–hydro (monthly)",
                  "## §8 Cointegrare: România–Ungaria (zilnic) și energie–gaze–hidro (lunar)")))
    C.append(code(
        "DLY = PD.loc[START:END, ['RO', 'HU', 'DE_LU']].dropna()\n"
        "for z in ['RO', 'HU', 'DE_LU']: print('ADF p, level', z, round(adfuller(DLY[z], autolag='AIC')[1], 4))\n"
        "for z in ['HU', 'DE_LU']:\n"
        "    eg = coint(DLY['RO'], DLY[z], trend='c', autolag='aic'); jo = coint_johansen(DLY[['RO', z]].values, det_order=0, k_ar_diff=6)\n"
        "    u = sm.OLS(DLY['RO'], sm.add_constant(DLY[z])).fit().resid; phi = sm.OLS(u.values[1:], u.values[:-1]).fit().params[0]\n"
        "    print(z, 'Engle-Granger %.2f (5%% cv %.2f) | Johansen trace %s vs %s | half-life %.1f days' % (\n"
        "          eg[0], eg[2][1], jo.lr1.round(2), jo.cvt[:, 1].round(2), np.log(0.5) / np.log(phi)))\n"
        "hyd = GH[['hydro_run_of_river', 'hydro_water_reservoir']].sum(axis=1, min_count=2); hyd.index = pd.to_datetime(hyd.index, utc=True)\n"
        "hyd = hyd[hyd.index < (END + pd.Timedelta(days=1)).tz_localize(TZ).tz_convert('UTC')]\n"
        "hyd_m = hyd.tz_convert(TZ).resample('MS').sum(min_count=600) / 1e6; hyd_m.index = hyd_m.index.tz_localize(None)\n"
        "TTF = pd.read_csv(DATA + 'ttf_monthly.csv'); TTF.index = pd.PeriodIndex(TTF['month'], freq='M').to_timestamp()\n"
        "MD = pd.concat([PD['RO'].loc[:END].resample('MS').mean().rename('price'), TTF['ttf_eur_mwh'].rename('ttf'), hyd_m.rename('hydro')], axis=1).dropna()\n"
        "MD['hydro_ds'] = MD['hydro'] - MD.groupby(MD.index.month)['hydro'].transform('mean')\n"
        "eg1 = coint(MD['price'], MD['ttf'], trend='c', autolag='aic'); lr = sm.OLS(MD['price'], sm.add_constant(MD[['ttf']])).fit()\n"
        "ecm_df = pd.DataFrame({'dp': MD['price'].diff(), 'u1': lr.resid.shift(1), 'dttf': MD['ttf'].diff(), 'hyd': MD['hydro_ds']}).dropna()\n"
        "ecm = sm.OLS(ecm_df['dp'], sm.add_constant(ecm_df[['u1', 'dttf', 'hyd']])).fit(cov_type='HAC', cov_kwds={'maxlags': 6})\n"
        "print('price-TTF Engle-Granger %.2f (cv %.2f); beta %.3f (efficiency %.1f%%)' % (eg1[0], eg1[2][1], lr.params['ttf'], 100 / lr.params['ttf']))\n"
        "print(ecm.summary().tables[1])"))

    # ---------------------------------------------------------------- §9
    C.append(md(T("## §9 Case studies: month by month, the stress week, 15-minute prices, battery and flexible buyer",
                  "## §9 Studii de caz: lună cu lună, săptămîna de criză, prețuri pe 15 minute, baterie și cumpărător flexibil")))
    C.append(code(
        "bym[['naive', 'aw_arx', 'aw_lear', 'ens_all']].plot(marker='o', figsize=(9, 3)); plt.ylabel('MAE'); plt.show()\n"
        "mons = [t for t in TDAYS if t.dayofweek == 0 and t + pd.Timedelta(days=6) <= END]\n"
        "SW = max(mons, key=lambda t: A[POS[t] - N_BURN:POS[t] - N_BURN + 7].mean()); sw = slice(POS[SW] - N_BURN, POS[SW] - N_BURN + 7)\n"
        "print('stress week from', SW.date(), {k: round(np.abs(A[sw] - M[k][sw]).mean(), 2) for k in ['naive', 'aw_lear', 'gbm', 'ens_all']})\n"
        "X = pd.read_csv(DATA + 'power_da_prices_native_utc.csv', index_col=0)['RO'].dropna(); X.index = pd.to_datetime(X.index, utc=True).tz_convert(TZ)\n"
        "X = X.loc[str((TEST0 - pd.Timedelta(days=40)).date()):str(END.date())]\n"
        "ALLQ = {d: g.values for d, g in X.groupby(X.index.tz_localize(None).normalize()) if len(g) == 96}\n"
        "QD = [t for t in TDAYS if t in ALLQ and not DST.loc[t]]\nQ = np.array([ALLQ[t] for t in QD])\n"
        "flat = np.repeat(np.array([M['aw_lear'][POS[t] - N_BURN] for t in QD]), 4, axis=1)\n"
        "shape = np.array([np.mean([ALLQ[t - pd.Timedelta(days=j)] - np.repeat(ALLQ[t - pd.Timedelta(days=j)].reshape(24, 4).mean(1), 4)\n"
        "                           for j in range(1, 29) if t - pd.Timedelta(days=j) in ALLQ], 0) for t in QD])\n"
        "print('15-min MAE: flat %.2f, with intra-hour shape %.2f (%d days)' % (np.abs(Q - flat).mean(), np.abs(Q - flat - shape).mean(), len(QD)))\n\n\n" +
        fsrc("battery", "flex") + "\n\n\n"
        "ND = ~DST.loc[TDAYS].values; AN = A[ND]   # DST days left out: their 24 columns are not 24 physical hours\n"
        "for k in ['naive', 'aw_arx', 'aw_lear', 'gbm', 'ens_all']:\n"
        "    b_ = battery(M[k][ND], AN).sum()\n"
        "    print(k, 'battery %.0f EUR per MW (%.1f%% of perfect) | flexible buyer %.2f EUR/MWh' % (\n"
        "          b_, b_ / battery(AN, AN).sum() * 100, flex(M[k][ND], AN)[0].sum() / (4 * len(AN))))\n"
        "print('fixed 8-12 h block %.2f EUR/MWh' % (flex(AN, AN)[1].sum() / (4 * len(AN))))"))

    # ---------------------------------------------------------------- §10
    C.append(md(T("## §10 Leakage self-check\n(a) every input is public before 12:00 CET on *d−1*; (b) forecasts recomputed after deleting all "
                  "prices from *d* and all fundamentals from *d−1* must not change.",
                  "## §10 Autoverificarea scurgerii de informație\n(a) fiecare intrare este publică înainte de ora 12:00 CET din *d−1*; "
                  "(b) prognozele recalculate după ștergerea tuturor prețurilor din *d* și a tuturor fundamentalelor din *d−1* nu "
                  "trebuie să se schimbe.")))
    C.append(code(
        fsrc("avail_time") + "\n\n\n"
        "REG = [('P', k, 'price') for k in PLAGS] + [('L', k, 'realised') for k in XLAGS] + [('R', k, 'realised') for k in XLAGS] + \\\n"
        "      [('fund_' + c, 2, 'close' if c == 'eua' else 'realised') for c in FUND_RAW.columns]\n"
        "n = 0\nfor t in FDAYS:\n    cut = t - pd.Timedelta(days=1) + pd.Timedelta(hours=12)\n"
        "    for blk, lag, src in REG:\n        assert avail_time(src, lag, t) <= cut, (blk, lag, t); n += 1\n"
        "print('timestamp audit passed:', n, 'checks')\n\n\n" + fsrc("corrupt") + "\n\n\n"
        "for t in [TDAYS[0], TDAYS[-1]]:\n"
        "    i = IDX[t]; r = point_day(*corrupt(i), i)\n"
        "    d_ = max(np.max(np.abs(np.asarray(r[k]) - PT[k][POS[t]])) for k in names)\n"
        "    print(t.date(), 'max change after deleting future data: %.2e' % d_); assert d_ < 1e-6\n"
        "a0, _ = MB[-1]; i = IDX[TDAYS[-1]]\n"
        "print('GBM change %.2e' % np.max(np.abs(gbm_month(*corrupt(i), a0, i)[0][-1] - M['gbm'][-1])))\n"
        "print('leakage self-check PASSED')"))
    return C


def build(lang):
    nb = nbformat.v4.new_notebook()
    nb.cells = cells(lang)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    name = "L2_notebook.ipynb" if lang == "en" else "L2_notebook_ro.ipynb"
    add_colab_cell(nb, lang)
    ExecutePreprocessor(timeout=3600, kernel_name="python3").preprocess(nb, {"metadata": {"path": NBDIR}})
    os.makedirs(NBDIR, exist_ok=True)
    with open(os.path.join(NBDIR, name), "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("executed and wrote", name)


if __name__ == "__main__":
    for lang in (sys.argv[1:] or ["en", "ro"]):
        build(lang)
