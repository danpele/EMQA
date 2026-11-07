"""
make_notebook_L4.py -- writes and executes the student notebooks of Lecture 4 (EMQA)
=====================================================================================
    notebooks/L4_notebook.ipynb      (English)
    notebooks/L4_notebook_ro.ipynb   (Romanian)
Same code in both; only the text differs. The risk functions are copied verbatim from analysis_L4.py (extracted with
the ast module), so the notebook runs exactly the code behind the slides. Paths are relative to notebooks/ (data in
../data/clean). Section numbers match the "Experiment yourself" pointers on the slides. The rolling VaR/ES engine (§3)
runs the two zones in parallel and takes two to three minutes on a laptop.
Run:  python3 lectures/L4/make_notebook_L4.py
"""

import ast
import os
import sys

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

HERE = os.path.dirname(os.path.abspath(__file__))
NBDIR = os.path.abspath(os.path.join(HERE, "..", "..", "notebooks"))
SRC = open(os.path.join(HERE, "analysis_L4.py"), encoding="utf-8").read()
TREE = ast.parse(SRC)


def fsrc(*names):
    """Source of top-level functions of analysis_L4.py, in the given order."""
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
        "# Energy Markets Quantitative Analysis — Lecture 4: Risk management for energy prices\n"
        "Prof. dr. Daniel Traian Pele — Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting\n\n"
        "This notebook reproduces the numbers and charts of Lecture 4 from the real data in `../data/clean` (see `../data/SOURCES.md`). "
        "Section numbers (§) match the *Experiment yourself* pointers on the slides.\n\n"
        "**Conventions.** Risk factor: the daily change of the day-ahead base price, $X_t=P_t-P_{t-1}$ (EUR/MWh), on the full calendar "
        "(a change next to a missing day stays missing). Position: a supplier that buys a flat block and budgets it at yesterday's price, "
        "so a price rise is a loss. The forecast for day $t$ uses prices up to $t-1$ only. Cut-off: last complete month.",
        "# Analiza cantitativă a piețelor de energie — Cursul 4: Managementul riscului de preț pe piețele de energie\n"
        "Prof. dr. Daniel Traian Pele — Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică\n\n"
        "Acest notebook Jupyter reproduce cifrele și graficele din cursul 4 pe datele reale din `../data/clean` (vezi `../data/SOURCES.md`). "
        "Numerele secțiunilor (§) corespund indicațiilor *Exercițiu practic* de pe diapozitive.\n\n"
        "**Convenții.** Factorul de risc este variația zilnică a prețului de bază pe piața pentru ziua următoare, $X_t=P_t-P_{t-1}$ (EUR/MWh), "
        "calculată pe calendarul complet (variația vecină cu o zi lipsă rămîne lipsă). Poziția: un furnizor care cumpără o bandă constantă și "
        "își bugetează costul la prețul de ieri; o creștere de preț este, deci, o pierdere. Prognoza pentru ziua $t$ folosește numai prețurile "
        "pînă în ziua $t-1$. Perioada analizată se încheie cu ultima lună completă.")))

    # ---------------------------------------------------------------- §1
    C.append(md(T("## §1 Data and the risk factor", "## §1 Datele și factorul de risc")))
    C.append(code(
        "import numpy as np, pandas as pd, matplotlib.pyplot as plt, json, warnings\n"
        "from scipy import stats\nfrom arch import arch_model\nfrom joblib import Parallel, delayed\n"
        "from statsmodels.regression.quantile_regression import QuantReg\n"
        "warnings.filterwarnings('ignore')\n"
        "DATA = '../data/clean/'\nSEED = 20261106\n\n"
        "PD = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "raw_last = PD['RO'].dropna().index.max()\n"
        "END = pd.Timestamp(((raw_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())\n"
        "START, T0 = pd.Timestamp('2015-01-01'), pd.Timestamp('2017-01-01')\n"
        "CAL = pd.date_range(START, END, freq='D')\n"
        "P = PD[['RO', 'DE_LU']].reindex(CAL)       # missing days stay missing\n"
        "X = P.diff()                               # a change next to a gap is NaN\n"
        "print('cut-off:', END.date(), '| missing RO days:', int(P['RO'].isna().sum()), '| valid RO changes:', int(X['RO'].notna().sum()))\n"
        "fig, ax = plt.subplots(2, 1, figsize=(10, 4), sharex=True)\n"
        "ax[0].plot(P['RO'], lw=0.6); ax[0].set_ylabel('P_t, EUR/MWh')\n"
        "ax[1].plot(X['RO'], lw=0.5, color='C1'); ax[1].set_ylabel('X_t, EUR/MWh'); plt.show()"))

    # ---------------------------------------------------------------- §2
    C.append(md(T("## §2 Distribution, VaR and ES, and a limit built on the normal curve\n"
                  "VaR$_\\alpha$ = the $\\alpha$-quantile of the loss; ES$_\\alpha$ = the mean loss at or beyond it.",
                  "## §2 Repartiția variațiilor, VaR și ES și o limită calculată cu repartiția normală\n"
                  "VaR$_\\alpha$ = cuantila de ordin $\\alpha$ a pierderii; ES$_\\alpha$ = pierderea medie la nivelul VaR sau dincolo de el.")))
    C.append(code(
        fsrc("fl", "d", "dist_facts") + "\n\n\n"
        "for z in ['RO', 'DE_LU']:\n    print(z, dist_facts(X[z]))\n\n"
        "# empirical VaR and ES of the last 365 days, 100 MW flat = 2,400 MWh per day\n"
        "last = X['RO'][END - pd.Timedelta(days=364):END].dropna()\n"
        "v99, v975 = np.quantile(last, 0.99), np.quantile(last, 0.975)\n"
        "print('VaR99 %.2f EUR/MWh = %.0f EUR for 100 MW | VaR97.5 %.2f | ES97.5 %.2f' % (v99, v99 * 2400, v975, last[last >= v975].mean()))\n\n"
        "# a normal 99% limit estimated on 2015-2020 and its breaches afterwards\n"
        "pre = X['RO']['2015':'2020'].dropna(); lim = pre.mean() + stats.norm.ppf(0.99) * pre.std()\n"
        "for a, b in [('2015', '2020'), ('2021', '2022'), ('2023', str(END.year))]:\n"
        "    x_ = X['RO'][a:b].dropna(); print(a, '-', b, 'breaches', int((x_ > lim).sum()), 'expected %.1f' % (0.01 * len(x_)))"))

    # ---------------------------------------------------------------- §3
    C.append(md(T("## §3 Five ways to estimate VaR and ES, rolling one day ahead\n"
                  "HS and parametric (normal, Student-$t$) on the last 365 days; FHS = weekday mean + GARCH(1,1) volatility (refitted every "
                  "21 days on 730 days) + empirical standardised residuals; EVT = the same filter + generalised Pareto tail above the 90% "
                  "residual quantile. The engine also simulates each model's own predictive distribution for the ES test (§4).",
                  "## §3 Cinci moduri de a estima VaR și ES, cu o zi înainte, pe fereastră glisantă\n"
                  "HS și metodele parametrice (normală, Student-$t$) pe ultimele 365 de zile; FHS = media zilei din săptămînă + volatilitatea "
                  "GARCH(1,1) (reestimată la fiecare 21 de zile pe 730 de zile) + reziduurile standardizate empirice; EVT = același filtru + "
                  "coada Pareto generalizată peste cuantila de 90% a reziduurilor. Motorul simulează și repartiția prognozată de fiecare model, "
                  "necesară testului ES (§4).")))
    C.append(code(
        "METHODS = ['hs', 'normal', 't', 'fhs', 'evt']\nLEVELS = (0.95, 0.975, 0.99)\n"
        "W_HS, W_G, REFIT, U_EVT, M_SIM = 365, 730, 21, 0.90, 2000\n\n\n" +
        fsrc("var_es_normal", "fit_t", "var_es_t", "var_es_hs", "gpd_tail", "var_es_evt", "garch_filter", "run_zone") + "\n\n\n"
        "res = Parallel(n_jobs=2)(delayed(run_zone)(X[z], z, SEED + i) for i, z in enumerate(['RO', 'DE_LU']))\n"
        "ENG = {r['zone']: r for r in res}; DAYS = ENG['RO']['days']\n"
        "LM_ = DAYS >= END.replace(day=1)\n"
        "tab = pd.DataFrame({m: {'VaR95': ENG['RO']['out'][m][0.95]['var'][LM_].mean(), 'VaR99': ENG['RO']['out'][m][0.99]['var'][LM_].mean(),\n"
        "                        'ES97.5': ENG['RO']['out'][m][0.975]['es'][LM_].mean()} for m in METHODS}).T\n"
        "print('mean of the forecasts for', END.strftime('%Y-%m'), '(EUR/MWh)'); print(tab.round(2))"))
    C.append(code(
        "# 99% VaR paths in the crisis, and the square-root-of-time check\n"
        "a0, a1 = '2021-07-01', '2023-06-30'\nfig, ax = plt.subplots(figsize=(10, 3.5))\n"
        "ax.plot(X['RO'][a0:a1], color='0.7', lw=0.5, label='X_t')\n"
        "for m in ['hs', 'normal', 'fhs']:\n"
        "    ax.plot(pd.Series(ENG['RO']['out'][m][0.99]['var'], index=DAYS)[a0:a1], lw=0.9, label='VaR99 ' + m)\n"
        "ax.legend(ncol=4); plt.show()\n"
        "for z in ['RO', 'DE_LU']:\n"
        "    p = P[z]; q1 = (p.shift(-1) - p).dropna().quantile(0.99)\n"
        "    print(z, '10-day / 1-day 99%% quantile: %.2f (sqrt(10) = %.2f)' % ((p.shift(-10) - p).dropna().quantile(0.99) / q1, np.sqrt(10)))"))

    # ---------------------------------------------------------------- §4
    C.append(md(T("## §4 Backtesting: Kupiec, Christoffersen, Basel traffic light, Acerbi–Székely $Z_2$",
                  "## §4 Testarea retrospectivă: Kupiec, Christoffersen, semaforul Basel, Acerbi–Székely $Z_2$")))
    C.append(code(
        fsrc("kupiec", "christoffersen", "zone_of") + "\n\n\n"
        "rows = []\n"
        "for z in ['RO', 'DE_LU']:\n"
        "    E = ENG[z]; x = X[z].reindex(DAYS).values; ok = ~np.isnan(x)\n"
        "    for m in METHODS:\n"
        "        r = {'zone': z, 'method': m}\n"
        "        for a in (0.95, 0.99):\n"
        "            h = (x[ok] > E['out'][m][a]['var'][ok]).astype(int)\n"
        "            r[f'rate{a}'] = 100 * h.mean(); r[f'kupiec_p{a}'] = kupiec(h, 1 - a)[1]\n"
        "        r['christ_p0.99'] = christoffersen(h)[1]\n"
        "        c250 = pd.Series(np.where(ok, (x > E['out'][m][0.99]['var']).astype(float), 0.0)).rolling(250).sum().iloc[249:]\n"
        "        r['red_days_%'] = 100 * (c250.map(zone_of) == 'red').mean()\n"
        "        T_ = ok.sum(); obs = np.nansum(E['z2o'][m][ok]) / (T_ * 0.025) - 1\n"
        "        sim = E['z2c'][m][ok].sum(0) / (T_ * 0.025) - 1\n"
        "        r['Z2'] = obs; r['Z2_p'] = np.mean(sim >= obs)\n"
        "        rows.append(r)\n"
        "print(pd.DataFrame(rows).round(3).to_string(index=False))"))

    # ---------------------------------------------------------------- §5
    C.append(md(T("## §5 Exchange margins: a 99% two-day historical VaR on ICE Brent (EMIR RTS 153/2013)\n"
                  "Contract-roll days (first trading day of each month) are dropped from the returns.",
                  "## §5 Marjele la bursă: VaR istorică de 99% pe două zile pentru Brent ICE (RTS EMIR 153/2013)\n"
                  "Zilele de schimbare a contractului (prima zi de tranzacționare a fiecărei luni) sînt eliminate din randamente.")))
    C.append(code(
        "F = pd.read_csv(DATA + 'fuels_daily.csv', parse_dates=['date']).set_index('date')['brent_usd_bbl'].dropna()[:END]\n"
        "ym = F.index.to_period('M'); roll = pd.Series(np.r_[False, ym[1:] != ym[:-1]], index=F.index)\n"
        "r2 = F / F.shift(2) - 1; r2[(roll | roll.shift(1, fill_value=False))] = np.nan\n"
        "IM1 = 1000 * F * r2.abs().rolling(250, min_periods=200).quantile(0.99)       # 12-month lookback\n"
        "IML = 1000 * F * r2.abs().expanding(min_periods=250).quantile(0.99)          # floor: all data since 2015\n"
        "IMA = np.maximum(IM1, IML)\n"
        "pre = pd.Timestamp('2026-02-27')\n"
        "print('IM per lot on %s: %.0f USD (12 months), %.0f (with floor)' % (pre.date(), IM1[pre], IMA[pre]))\n"
        "print('max Jan-Jun 2026: %.0f (x%.2f), with floor %.0f (x%.2f)' % (IM1['2026-01':'2026-06'].max(), IM1['2026-01':'2026-06'].max() / IM1[pre],\n"
        "      IMA['2026-01':'2026-06'].max(), IMA['2026-01':'2026-06'].max() / IMA[pre]))\n"
        "vm = F.diff(); vm[roll] = np.nan; vm = vm * 1000 * 100                          # seller of 100 lots pays when the price rises\n"
        "print('largest one-day VM for 100 lots sold: %.2f million USD on %s' % (vm.max() / 1e6, vm.idxmax().date()))\n"
        "ax = (pd.DataFrame({'IM 12 months': IM1, 'IM with floor': IMA})['2016':] / 1000).plot(figsize=(10, 3)); ax.set_ylabel('thousand USD per lot'); plt.show()"))

    # ---------------------------------------------------------------- §6
    C.append(md(T("## §6 The day-ahead guarantee from a quantile forecast, and position limits\n"
                  "Quantile regression of $P_t$ on $P_{t-1}$, $P_{t-7}$ and weekday dummies (last 365 days), then a one-sided conformal "
                  "correction: the $\\tau$-quantile of the last 365 out-of-sample errors.",
                  "## §6 Garanția pentru piața pentru ziua următoare dintr-o prognoză a cuantilei și limitele de poziție\n"
                  "Regresia cuantilică a lui $P_t$ pe $P_{t-1}$, $P_{t-7}$ și variabilele zilei din săptămînă (ultimele 365 de zile), apoi o "
                  "corecție conformală unilaterală: cuantila de ordin $\\tau$ a ultimelor 365 de erori din afara eșantionului.")))
    C.append(code(
        "PR = P['RO']; TAUS = (0.95, 0.99)\n\n\n" + fsrc("qr_forecast") + "\n\n\n"
        "QD = pd.date_range('2016-01-01', END, freq='D')\n"
        "rr = Parallel(n_jobs=-1)(delayed(qr_forecast)(t) for t in QD)\n"
        "QRF = pd.DataFrame({tau: [r_[tau] for r_ in rr] for tau in TAUS}, index=QD)\n"
        "for tau in TAUS:\n"
        "    cq = QRF[tau] + (PR.reindex(QD) - QRF[tau]).shift(1).rolling(365, min_periods=300).quantile(tau)\n"
        "    fq = PR.shift(1).reindex(DAYS) + pd.Series(ENG['RO']['out']['fhs'][tau]['var'], index=DAYS)\n"
        "    df = pd.DataFrame({'p': PR.reindex(DAYS), 'qr': QRF[tau].reindex(DAYS), 'cqr': cq.reindex(DAYS), 'fhs': fq}).dropna()\n"
        "    print(tau, {k: round(100 * (df['p'] <= df[k]).mean(), 2) for k in ['qr', 'cqr', 'fhs']},\n"
        "          'mean guarantee for 100 MW, million EUR/day: %.3f' % (df['cqr'].mean() * 2400 / 1e6))\n"
        "v99 = pd.Series(ENG['RO']['out']['fhs'][0.99]['var'], index=DAYS)\n"
        "qmax = 250_000 / (24 * v99)          # MW for a daily VaR budget of 250,000 EUR (an assumption)\n"
        "print('position limit, MW: 2019 median %.0f | minimum %.0f on %s | last %.0f' % (qmax['2019'].median(), qmax.min(), qmax.idxmin().date(), qmax.iloc[-1]))"))

    # ---------------------------------------------------------------- §7
    C.append(md(T("## §7 A supplier's monthly cost-at-risk and a producer's tail",
                  "## §7 Costul lunar la risc al unui furnizor și coada producătorului")))
    C.append(code(
        "HP = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')['RO']\n"
        "GL = pd.read_csv(DATA + 'generation_ro_mw_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')['load']\n"
        "hl = pd.DataFrame({'p': HP, 'l': GL}).dropna()\n"
        "hl['m'] = hl.index.tz_convert('Europe/Brussels').tz_localize(None).to_period('M')\n"
        "mon = hl.groupby('m').apply(lambda g: pd.Series({'lwp': (g.p * g.l).sum() / g.l.sum(), 'base': g.p.mean(), 'hours': len(g)}))\n"
        "mon = mon[(mon.index >= pd.Period('2015-02', 'M')) & (mon.index <= pd.Period(END, 'M'))]\n"
        "mon['o'] = mon['lwp'] / mon['lwp'].shift(1) - 1\n"
        "mon['eur'] = 100 * mon['hours'] * (mon['lwp'] - mon['lwp'].shift(1))\n"
        "mon = mon.dropna()\n"
        "pre = mon['o'][mon.index <= pd.Period('2020-12', 'M')]; lim = pre.mean() + stats.norm.ppf(0.99) * pre.std()\n"
        "post = mon[mon.index >= pd.Period('2021-01', 'M')]\n"
        "print('normal 99%% limit %.1f%% | exceeded %d times since 2021 (%.1f expected)' % (100 * lim, (post['o'] > lim).sum(), 0.01 * len(post)))\n"
        "print('worst month', mon['o'].idxmax(), '%.1f%%, %.2f million EUR' % (100 * mon['o'].max(), mon.loc[mon['o'].idxmax(), 'eur'] / 1e6))\n"
        "xr = X['RO'].dropna()\n"
        "print('daily 99%% quantile (supplier) %.2f | 1%% quantile (producer) %.2f | skewness %.2f' % (xr.quantile(0.99), xr.quantile(0.01), stats.skew(xr)))\n"
        "ax = (100 * mon['o']).plot(kind='bar', figsize=(12, 3), width=0.8); ax.axhline(100 * lim, ls='--', color='k')\n"
        "ax.set_xticks(range(0, len(mon), 12)); ax.set_xticklabels([str(p_) for p_ in mon.index[::12]]); plt.show()"))

    # ---------------------------------------------------------------- §8
    C.append(md(T("## §8 Case study: autumn 2026 — market risk vs liquidity",
                  "## §8 Studiu de caz: toamna anului 2026 — riscul de piață și riscul de lichiditate")))
    C.append(code(
        "C0 = pd.Timestamp('2026-06-01'); x = X['RO'].reindex(DAYS)\n"
        "for m in METHODS:\n"
        "    v = pd.Series(ENG['RO']['out'][m][0.99]['var'], index=DAYS)\n"
        "    print(m, '99%% exceedances since %s: %d (expected %.1f)' % (C0.date(), int((x[C0:] > v[C0:]).sum()), 0.01 * x[C0:].notna().sum()))\n"
        "print('mean price June %.2f, October %.2f EUR/MWh' % (PR['2026-06'].mean(), PR['2026-10'].mean()))\n"
        "print('FHS VaR99 June %.2f, October %.2f' % (v99['2026-06'].mean(), v99['2026-10'].mean()))\n"
        "print('guarantee (conformal 99%%) for 100 MW, million EUR/day: June %.3f, October %.3f' % (cq['2026-06'].mean() * 2400 / 1e6, cq['2026-10'].mean() * 2400 / 1e6))\n"
        "print(mon.loc[pd.Period('2026-08', 'M'):, ['o', 'eur']])\n"
        "cc = pd.date_range(C0, END)\n"
        "fig, ax = plt.subplots(figsize=(10, 3.2)); ax.plot(cc, PR.reindex(cc), color='k', label='P_t')\n"
        "ax.plot(cc, PR.shift(1).reindex(cc) + v99.reindex(cc), label='P(t-1) + VaR99 FHS'); ax.plot(cc, cq.reindex(cc), ls='-.', label='guarantee limit')\n"
        "ax.legend(); plt.show()"))
    return C


def build(lang):
    nb = nbformat.v4.new_notebook()
    nb.cells = cells(lang)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    name = "L4_notebook.ipynb" if lang == "en" else "L4_notebook_ro.ipynb"
    ExecutePreprocessor(timeout=3600, kernel_name="python3").preprocess(nb, {"metadata": {"path": NBDIR}})
    os.makedirs(NBDIR, exist_ok=True)
    with open(os.path.join(NBDIR, name), "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("executed and wrote", name)


if __name__ == "__main__":
    for lang in (sys.argv[1:] or ["en", "ro"]):
        build(lang)
