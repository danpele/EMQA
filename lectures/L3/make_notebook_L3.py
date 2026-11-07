"""
make_notebook_L3.py -- writes and executes the student notebooks of Lecture 3 (EMQA)
=====================================================================================
    notebooks/L3_notebook.ipynb      (English)
    notebooks/L3_notebook_ro.ipynb   (Romanian)
Same code in both; only the text differs. The model functions are copied verbatim from analysis_L3.py (extracted with
the ast module), so the notebook runs exactly the code behind the slides. Paths are relative to notebooks/ (data in
../data/clean). Section numbers match the "Experiment yourself" pointers on the slides. The rolling evaluation (§7) runs
in parallel with joblib and takes well under a minute on a laptop with several cores.
Run:  python3 lectures/L3/make_notebook_L3.py
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
SRC = open(os.path.join(HERE, "analysis_L3.py"), encoding="utf-8").read()
TREE = ast.parse(SRC)


def fsrc(*names):
    """Source of top-level functions of analysis_L3.py, in the given order."""
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
        "# Energy Markets Quantitative Analysis — Lecture 3: Volatility of energy prices\n"
        "Prof. dr. Daniel Traian Pele — Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting\n\n"
        "This notebook reproduces the models, numbers and charts of Lecture 3 from the real data in `../data/clean` "
        "(see `../data/SOURCES.md`). Section numbers (§) match the *Experiment yourself* pointers on the slides.\n\n"
        "**Conventions.** Romanian day-ahead (PZU) daily base price = mean of all market time units of the CET delivery day; panel "
        "2019-01-01 to the last complete month. Daily changes on the full calendar, in percent (log) and in EUR/MWh. Brent: the first "
        "trading day of each month (contract roll) is dropped. Every volatility model is estimated on the shocks left after a mean "
        "equation (constant, 7 autoregressive lags, day of the week).",
        "# Analiza cantitativă a piețelor de energie — Cursul 3: Volatilitatea prețurilor energiei\n"
        "Prof. dr. Daniel Traian Pele — Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică\n\n"
        "Acest notebook Jupyter reproduce modelele, cifrele și graficele din cursul 3 pe datele reale din `../data/clean` "
        "(vezi `../data/SOURCES.md`). Numerele secțiunilor (§) corespund indicațiilor *Exercițiu practic* de pe diapozitive.\n\n"
        "**Convenții.** Prețul zilnic de bază PZU din România = media tuturor intervalelor zilei de livrare (ora Europei Centrale, CET); "
        "perioada 1 ianuarie 2019 – ultima lună completă. Variațiile zilnice se calculează pe calendarul complet, în procente (logaritmic) și "
        "în EUR/MWh. Brent: se elimină prima zi de tranzacționare a fiecărei luni (schimbarea contractului). Toate modelele de volatilitate se "
        "estimează pe șocurile rămase după ecuația mediei (constantă, 7 decalaje autoregresive, ziua săptămînii).")))

    # ---------------------------------------------------------------- §1
    C.append(md(T("## §1 Data, daily changes and the weekly calendar",
                  "## §1 Datele, variațiile zilnice și calendarul săptămînal")))
    C.append(code(
        "import numpy as np, pandas as pd, matplotlib.pyplot as plt, statsmodels.api as sm, warnings\n"
        "from scipy import stats\nfrom arch import arch_model\nfrom joblib import Parallel, delayed\n"
        "from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch\n"
        "from statsmodels.tsa.stattools import acf\n"
        "from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression\n"
        "warnings.filterwarnings('ignore')\nDATA = '../data/clean/'\nTZ = 'Europe/Brussels'\n\n"
        "PD = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "FU = pd.read_csv(DATA + 'fuels_daily.csv', parse_dates=['date']).set_index('date')\n"
        "EUA = pd.read_csv(DATA + 'eua_daily.csv', parse_dates=['date']).set_index('date')['eua_etc_co2l_eur_per_unit']\n"
        "EQ = pd.read_csv(DATA + 'ro_energy_equities_daily.csv', parse_dates=['date']).set_index('date')\n"
        "GEN = pd.read_csv(DATA + 'generation_ro_mw_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "raw_last = PD['RO'].dropna().index.max()\n"
        "END = pd.Timestamp(((raw_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())\n"
        "START = pd.Timestamp('2019-01-01')\nCAL = pd.date_range(START, END, freq='D')\n"
        "PR = {z: PD[z].reindex(CAL) for z in ['RO', 'HU', 'DE_LU']}\n"
        "print('cut-off (last complete month):', END.date(), '| days:', len(CAL), '| missing RO days:', PR['RO'].isna().sum())"))
    C.append(code(fsrc("pct_change", "mean_design", "mean_fit") + "\n\n\n"
                  "R_PCT = {z: pct_change(PR[z]) for z in PR}\nR_EUR = {z: PR[z].diff() for z in PR}\n"
                  "print('days with base price <= 0:', {z: int((PR[z] <= 0).sum()) for z in PR})\n"
                  "rde = R_PCT['DE_LU'].dropna(); print('largest |log change| in DE-LU: %.0f%% on %s' % (rde.abs().max(), rde.abs().idxmax().date()))\n"
                  "rr = R_PCT['RO'].dropna()\n"
                  "print('mean change by weekday, %:', rr.groupby(rr.index.dayofweek).mean().round(1).to_dict())\n"
                  "E_PCT, M_PCT = mean_fit(R_PCT['RO']); E_EUR, M_EUR = mean_fit(R_EUR['RO'])\n"
                  "print('mean equation R2: %.3f (%%), %.3f (EUR/MWh); std %.1f%% -> %.1f%%' % (M_PCT.rsquared, M_EUR.rsquared, rr.loc[E_PCT.index].std(), E_PCT.std()))\n"
                  "fig, ax = plt.subplots(2, 1, figsize=(10, 4), sharex=True)\n"
                  "ax[0].plot(PR['RO'], lw=0.6); ax[0].set_ylabel('EUR/MWh'); ax[1].plot(rr, lw=0.3); ax[1].set_ylabel('r_t, %'); plt.show()"))

    # ---------------------------------------------------------------- §2
    C.append(md(T("## §2 Stylised facts: clustering, fat tails, two units, volatility by market",
                  "## §2 Faptele stilizate: gruparea volatilității, cozi groase, două unități de măsură, volatilitatea pe piețe")))
    C.append(code(
        "print('Ljung-Box Q(10): shocks %.1f, squared shocks %.1f (critical 18.31)' % (acorr_ljungbox(E_PCT, [10])['lb_stat'].iloc[0],\n"
        "      acorr_ljungbox(E_PCT ** 2, [10])['lb_stat'].iloc[0]))\n"
        "print('ARCH-LM(10): %.1f, p = %.2g' % het_arch(E_PCT, nlags=10)[:2])\n"
        "z = (E_PCT - E_PCT.mean()) / E_PCT.std()\n"
        "print('excess kurtosis %.1f, skewness %.2f, |z|>4: %d (normal: %.2f)' % (E_PCT.kurt(), E_PCT.skew(), (z.abs() > 4).sum(), len(z) * 2 * stats.norm.sf(4)))\n"
        "fig, ax = plt.subplots(1, 2, figsize=(10, 3), sharey=True)\n"
        "ax[0].bar(range(1, 31), acf(E_PCT, nlags=30)[1:]); ax[0].set_title('ACF of shocks')\n"
        "ax[1].bar(range(1, 31), acf(E_PCT ** 2, nlags=30)[1:]); ax[1].set_title('ACF of squared shocks'); plt.show()\n"
        "by = pd.DataFrame({'sd_pct': E_PCT.groupby(E_PCT.index.year).std(), 'sd_eur': E_EUR.groupby(E_EUR.index.year).std(),\n"
        "                   'mean_price': PR['RO'].groupby(PR['RO'].index.year).mean()})\nprint(by.round(1))"))
    C.append(code(
        fsrc("mkt_returns") + "\n\n\n"
        "BRENT, n_roll = mkt_returns(FU['brent_usd_bbl'].loc[str(START - pd.Timedelta(days=10)):str(END)], drop_roll=True); BRENT = BRENT.loc[START:END]\n"
        "EUAR, _ = mkt_returns(EUA.loc[:str(END)])\n"
        "SNP, _ = mkt_returns(EQ['SNP_adjclose_ron'].loc[str(START - pd.Timedelta(days=10)):str(END)], vol=EQ['SNP_volume']); SNP = SNP.loc[START:END]\n"
        "print('Brent roll days dropped:', n_roll)\n"
        "ann = pd.DataFrame({'RO power': E_PCT.groupby(E_PCT.index.year).std() * np.sqrt(365),\n"
        "                    'EUA': EUAR.groupby(EUAR.index.year).std() * np.sqrt(252), 'Brent': BRENT.groupby(BRENT.index.year).std() * np.sqrt(252),\n"
        "                    'OMV Petrom': SNP.groupby(SNP.index.year).std() * np.sqrt(252)})\nprint('annualised volatility, %'); print(ann.round(0))"))

    # ---------------------------------------------------------------- §3
    C.append(md(T("## §3 GARCH(1,1) with Student-t shocks; persistence and half-life",
                  "## §3 GARCH(1,1) cu șocuri de tip Student; persistența și timpul de înjumătățire")))
    C.append(code(
        fsrc("fit", "persistence", "half_life") + "\n\n\n"
        "for unit, e in [('percent', E_PCT), ('EUR/MWh', E_EUR)]:\n"
        "    for dist in ['normal', 't']:\n"
        "        r = fit(e, dist=dist); ph = persistence(r)\n"
        "        print(unit, dist, 'loglik %.1f BIC %.1f alpha+beta %.3f half-life %.1f days' % (r.loglikelihood, r.bic, ph, half_life(ph) or np.inf))\n"
        "g_pct, g_eur = fit(E_PCT), fit(E_EUR)\nprint(g_eur.summary())\n"
        "fig, ax = plt.subplots(2, 1, figsize=(10, 4), sharex=True)\n"
        "ax[0].plot(E_PCT.index, g_pct.conditional_volatility, lw=0.6); ax[0].set_ylabel('sigma, %')\n"
        "ax[1].plot(E_EUR.index, g_eur.conditional_volatility, lw=0.6, color='C4'); ax[1].set_ylabel('sigma, EUR/MWh'); plt.show()"))
    C.append(code(
        "hl = {}\nfor k, e in [('RO %', E_PCT), ('RO EUR/MWh', E_EUR), ('Brent', BRENT - BRENT.mean()), ('EUA', EUAR - EUAR.mean()), ('OMV Petrom', SNP - SNP.mean())]:\n"
        "    ph = persistence(fit(e.dropna())); hl[k] = (round(ph, 3), round(half_life(ph), 1))\n"
        "print('(alpha+beta, half-life in days):', hl)\nh = np.arange(121)\n"
        "for k, (ph, _) in hl.items():\n    plt.plot(h, 100 * ph ** h, label=k)\n"
        "plt.axhline(50, ls=':', c='k'); plt.ylabel('% of the shock left'); plt.legend(); plt.show()"))

    # ---------------------------------------------------------------- §4
    C.append(md(T("## §4 Asymmetry: GJR and EGARCH, news impact curve, volatility and price level",
                  "## §4 Asimetria: GJR și EGARCH, curba de impact a șocurilor, volatilitatea și nivelul prețului")))
    C.append(code(
        "for unit, e in [('percent', E_PCT), ('EUR/MWh', E_EUR)]:\n"
        "    gj, eg = fit(e, o=1), fit(e, vol='EGARCH', o=1)\n"
        "    print(unit, 'GJR gamma %.3f (t %.1f) | EGARCH gamma %.3f (t %.1f) | BIC: GJR %.1f, EGARCH %.1f' % (\n"
        "          gj.params['gamma[1]'], gj.tvalues['gamma[1]'], eg.params['gamma[1]'], eg.tvalues['gamma[1]'], gj.bic, eg.bic))\n"
        "p = fit(E_EUR, o=1).params; ph = p['alpha[1]'] + p['gamma[1]'] / 2 + p['beta[1]']; s2 = p['omega'] / (1 - ph)\n"
        "x = np.linspace(-4, 4, 201) * np.sqrt(s2)\n"
        "plt.plot(x, np.sqrt(p['omega'] + p['beta[1]'] * s2 + (p['alpha[1]'] + p['gamma[1]'] * (x < 0)) * x ** 2))\n"
        "plt.xlabel('shock u(t-1), EUR/MWh'); plt.ylabel('next-day sigma'); plt.title('news impact curve, GJR-t'); plt.show()\n"
        "m = pd.DataFrame({'sd': E_EUR.groupby(E_EUR.index.to_period('M')).std(), 'lvl': PR['RO'].groupby(PR['RO'].index.to_period('M')).mean()}).dropna()\n"
        "ll = sm.OLS(np.log(m['sd']), sm.add_constant(np.log(m['lvl']))).fit()\n"
        "print('log monthly sd(u) on log mean price: slope %.2f, R2 %.2f' % (ll.params.iloc[1], ll.rsquared))\n"
        "plt.loglog(m['lvl'], m['sd'], 'o', ms=3); plt.xlabel('monthly mean price'); plt.ylabel('monthly sd of u'); plt.show()"))

    # ---------------------------------------------------------------- §5
    C.append(md(T("## §5 Regimes: Markov switching and persistence by period",
                  "## §5 Regimuri: modelul Markov și persistența pe perioade")))
    C.append(code(
        "np.random.seed(20261106)\n"
        "ms = MarkovRegression(E_EUR.values, k_regimes=2, trend='c', switching_variance=True).fit(search_reps=20, disp=False)\n"
        "hi = int(np.argmax(ms.params[-2:])); P_ = ms.regime_transition[:, :, 0]\n"
        "print('sd calm / turbulent: %.1f / %.1f EUR/MWh; expected durations:' % tuple(np.sqrt(np.sort(ms.params[-2:]))), np.round(ms.expected_durations, 1))\n"
        "prob = pd.Series(ms.smoothed_marginal_probabilities[:, hi], index=E_EUR.index)\n"
        "print('share of turbulent days by year, %:', (100 * (prob > 0.5).groupby(prob.index.year).mean()).round(0).to_dict())\n"
        "fig, ax = plt.subplots(2, 1, figsize=(10, 4), sharex=True); ax[0].plot(PR['RO'], lw=0.6); ax[1].fill_between(prob.index, 0, prob, color='C4'); plt.show()\n"
        "for a, b in [('2019-01-01', '2020-12-31'), ('2021-01-01', '2022-12-31'), ('2023-01-01', str(END.date()))]:\n"
        "    print(a[:4], '-', b[:4], 'alpha+beta: %.3f (%%), %.3f (EUR/MWh)' % (persistence(fit(E_PCT.loc[a:b])), persistence(fit(E_EUR.loc[a:b]))))"))

    # ---------------------------------------------------------------- §6
    C.append(md(T("## §6 Intraday variation from hourly prices; solar; the HAR model",
                  "## §6 Variația intrazilnică din prețurile orare; producția solară; modelul HAR")))
    C.append(code(
        "HP = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')['RO'].dropna()\n"
        "HP.index = HP.index.tz_convert(TZ); HP = HP.loc[str(START.date()):str(END.date())]\n"
        "h = pd.DataFrame({'p': HP.values, 'day': HP.index.tz_localize(None).normalize()}); h['dp'] = h.groupby('day')['p'].diff()\n"
        "g = h.groupby('day')\n"
        "RV = pd.DataFrame({'rv': np.sqrt(g['dp'].apply(lambda x: (x ** 2).sum(min_count=1))), 'lvl': g['p'].mean()}).reindex(CAL)\n"
        "RV['rel'] = RV['rv'] / RV['lvl'].abs()\n"
        "print(pd.DataFrame({'mean RV': RV['rv'].groupby(RV.index.year).mean(), 'median RV/price': RV['rel'].groupby(RV.index.year).median(),\n"
        "                    'solar MW': GEN['solar'].reindex(CAL).groupby(CAL.year).mean()}).round(2))\n\n\n" +
        fsrc("har_design") + "\n\n\n"
        "TEST0 = END - pd.Timedelta(days=364); TDAYS = pd.date_range(TEST0, END)\n"
        "HD = har_design(RV['rv']).dropna(); tr = HD.loc[:TEST0 - pd.Timedelta(days=1)]\n"
        "har = sm.OLS(tr['y'], sm.add_constant(tr[['d', 'w', 'm']])).fit(cov_type='HAC', cov_kwds={'maxlags': 7}); print(har.params.round(3), 'R2 %.2f' % har.rsquared)\n"
        "pred = []\nfor t in TDAYS:\n    tr = HD.loc[:t - pd.Timedelta(days=1)]; X = sm.add_constant(tr[['d', 'w', 'm']]).values\n"
        "    b = np.linalg.lstsq(X, tr['y'].values, rcond=None)[0]; s2 = np.var(tr['y'].values - X @ b)\n"
        "    pred.append(np.exp(np.r_[1.0, HD.loc[t, ['d', 'w', 'm']].values] @ b + 0.5 * s2))\n"
        "HARF = pd.Series(pred, index=TDAYS); act = RV['rv'].loc[TDAYS]\n"
        "print('test-year MAE: HAR %.1f, yesterday %.1f EUR/MWh' % ((HARF - act).abs().mean(), (RV['rv'].shift(1).loc[TDAYS] - act).abs().mean()))\n"
        "plt.figure(figsize=(10, 3)); plt.plot(act, c='grey', lw=0.7); plt.plot(HARF, lw=1.1); plt.show()"))

    # ---------------------------------------------------------------- §7
    C.append(md(T("## §7 Forecasting and evaluating volatility: rolling forecasts, QLIKE, DM test, multi-step\n"
                  "Every model is re-estimated every day of the test year on the data up to the day before (mean equation included).",
                  "## §7 Prognoza și evaluarea volatilității: prognoze glisante, QLIKE, testul DM, prognoze pe mai mulți pași\n"
                  "Fiecare model este reestimat în fiecare zi a anului de test, pe datele pînă în ziua precedentă (inclusiv ecuația mediei).")))
    C.append(code(
        fsrc("one_day", "qlike", "nw_var", "dm") + "\n\n\n"
        "VMODELS = ['hist30', 'ewma', 'garch', 'gjr', 'egarch']\nROLL = {}\n"
        "for u, y in [('pct', R_PCT['RO']), ('eur', R_EUR['RO'])]:\n"
        "    R = pd.DataFrame(Parallel(n_jobs=-1)(delayed(one_day)(y.loc[START:END], t) for t in TDAYS), index=TDAYS); ROLL[u] = R\n"
        "    px = R['e'] ** 2; L = {k: qlike(px, R[k]) for k in VMODELS}\n"
        "    print(u, {k: round(L[k].mean(), 3) for k in VMODELS})\n"
        "    print('   p (beats 30-day history):', {k: round(dm(L['hist30'], L[k])[1], 3) for k in VMODELS[1:]})\n"
        "R = ROLL['eur']; plt.figure(figsize=(10, 3)); plt.bar(R.index, R['e'].abs(), color='lightgrey', width=1)\n"
        "plt.plot(np.sqrt(R['garch']), label='GARCH-t'); plt.plot(np.sqrt(R['hist30']), '--', label='30-day history'); plt.legend(); plt.show()"))
    C.append(code(
        "gb = fit(BRENT - BRENT.mean()); cvb = pd.Series(gb.conditional_volatility, index=BRENT.index) * np.sqrt(252)\n"
        "peak = cvb.loc[str(END.year)].idxmax(); xb = BRENT.loc[:peak]; gp = fit(xb - xb.mean())\n"
        "f = gp.forecast(horizon=40, reindex=False).variance.values[-1]; z95 = stats.norm.ppf(0.95)\n"
        "print('Brent on', peak.date(), ': 20-day 90%% band GARCH +/-%.1f%%, sigma*sqrt(20) +/-%.1f%%' % (z95 * np.sqrt(f[:20].sum()), z95 * np.sqrt(20 * f[0])))\n"
        "hh = np.arange(1, 41); plt.plot(hh, z95 * np.sqrt(np.cumsum(f)), label='GARCH'); plt.plot(hh, z95 * np.sqrt(hh * f[0]), '-.', label='sigma*sqrt(h)')\n"
        "plt.xlabel('h (trading days)'); plt.ylabel('90% band, +/-%'); plt.legend(); plt.show()"))

    # ---------------------------------------------------------------- §8
    C.append(md(T("## §8 Case study: Romanian power in 2026\nOne-day 90% band from GARCH-t on the test year, and the forecast at the cut-off. "
                  "Case study C3 (energy shares and oil, DCC-GARCH) has its own notebook in `../cases/C3_energy_stocks/`.",
                  "## §8 Studiu de caz: prețul energiei electrice din România în 2026\nBanda de 90% pentru ziua următoare, calculată cu GARCH-t "
                  "în anul de test, și prognoza la sfîrșitul perioadei. Studiul de caz C3 (acțiuni energetice și petrol, DCC-GARCH) are propriul "
                  "notebook Jupyter în `../cases/C3_energy_stocks/`.")))
    C.append(code(
        "R = ROLL['eur']; q = stats.t.ppf(0.95, R['nu']) * np.sqrt((R['nu'] - 2) / R['nu']); w = q * np.sqrt(R['garch'])\n"
        "out = R['e'].abs() > w\nprint('days outside the 90%% band: %d of %d (%.1f%%)' % (out.sum(), len(out), 100 * out.mean()))\n"
        "center = PR['RO'].shift(1).loc[TDAYS] + R['yhat']\n"
        "plt.figure(figsize=(10, 3)); plt.fill_between(TDAYS, center - w, center + w, alpha=0.3); plt.plot(PR['RO'].loc[TDAYS], lw=0.8)\n"
        "plt.scatter(out[out].index, PR['RO'].loc[out[out].index], c='r', s=8); plt.show()\n"
        "f = g_eur.forecast(horizon=30, reindex=False).variance.values[-1]\n"
        "p = g_eur.params; lr = p['omega'] / (1 - p['alpha[1]'] - p['beta[1]'])\n"
        "print('sigma for the next day %.1f EUR/MWh, long-run %.1f; one-day 90%% limit +/-%.0f EUR/MWh' % (np.sqrt(f[0]), np.sqrt(lr), stats.norm.ppf(0.95) * np.sqrt(f[0])))"))
    return C


def build(lang):
    nb = nbformat.v4.new_notebook()
    nb.cells = cells(lang)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    name = "L3_notebook.ipynb" if lang == "en" else "L3_notebook_ro.ipynb"
    add_colab_cell(nb, lang)
    ExecutePreprocessor(timeout=3600, kernel_name="python3").preprocess(nb, {"metadata": {"path": NBDIR}})
    os.makedirs(NBDIR, exist_ok=True)
    with open(os.path.join(NBDIR, name), "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("executed and wrote", name)


if __name__ == "__main__":
    for lang in (sys.argv[1:] or ["en", "ro"]):
        build(lang)
