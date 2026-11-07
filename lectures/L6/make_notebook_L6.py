"""
make_notebook_L6.py -- writes and executes the student notebooks of Lecture 6 (EMQA)
=====================================================================================
    notebooks/L6_notebook.ipynb      (English)
    notebooks/L6_notebook_ro.ipynb   (Romanian)
Same code in both; only the text differs. The functions are copied verbatim from analysis_L6.py (extracted with the ast
module), so the notebook runs exactly the code behind the slides. Paths are relative to notebooks/ (data in ../data/clean;
run data/download_L6.py once for the 15-minute generation files). Section numbers match the "Experiment yourself" pointers.
Run:  python3 lectures/L6/make_notebook_L6.py
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
SRC = open(os.path.join(HERE, "analysis_L6.py"), encoding="utf-8").read()
TREE = ast.parse(SRC)


def fsrc(*names):
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
        "# Energy Markets Quantitative Analysis — Lecture 6: Renewables and storage\n"
        "Prof. dr. Daniel Traian Pele — Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting\n\n"
        "This notebook reproduces the numbers and charts of Lecture 6 from the real data in `../data/clean` (see `../data/SOURCES.md`; "
        "run `python3 data/download_L6.py` once for the 15-minute generation files). Section numbers (§) match the *Experiment yourself* "
        "pointers on the slides.\n\n"
        "**Conventions.** CET/CEST delivery days; cut-off = last complete month; energy = mean MW × interval length; a 15-minute interval "
        "counts 0.25 h; missing values stay missing.",
        "# Analiza cantitativă a piețelor de energie — Cursul 6: Surse regenerabile și stocare\n"
        "Prof. dr. Daniel Traian Pele — Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică\n\n"
        "Acest notebook Jupyter reproduce cifrele și graficele din cursul 6 pe datele reale din `../data/clean` (vezi `../data/SOURCES.md`; "
        "rulați o dată `python3 data/download_L6.py` pentru fișierele de producție pe 15 minute). Numerele secțiunilor (§) corespund "
        "indicațiilor *Exercițiu practic* de pe diapozitive.\n\n"
        "**Convenții.** Zile de livrare după ora Europei Centrale (CET); perioada se încheie cu ultima lună completă; energia = puterea "
        "medie (MW) × durata intervalului; un interval de 15 minute contează 0,25 h; valorile lipsă rămîn lipsă.")))

    # §1
    C.append(md(T("## §1 Data and the solar boom", "## §1 Datele și creșterea producției solare")))
    C.append(code(
        "import numpy as np, pandas as pd, matplotlib.pyplot as plt, statsmodels.api as sm, json, warnings\n"
        "from scipy import sparse\nfrom scipy.optimize import linprog\nwarnings.filterwarnings('ignore')\n"
        "DATA = '../data/clean/'\nTZ = 'Europe/Brussels'\nETA, CYCLES, DURS = 0.85, 1.0, (1, 2, 4)\nR_DISC, LIFE = 0.08, 15\n\n"
        "PX = pd.read_csv(DATA + 'power_da_prices_native_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
        "PX.index = PX.index.tz_convert(TZ)\nPX['dur'] = PX['mtu_minutes'] / 60.0\n"
        "GN = {}\nfor c in ('ro', 'bg', 'hu'):\n"
        "    g = pd.read_csv(DATA + f'generation_{c}_mw_native_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
        "    g.index = g.index.tz_convert(TZ); GN[c.upper()] = g\n"
        "raw_last = min(PX['RO'].dropna().index.max().tz_localize(None), GN['RO']['solar'].dropna().index.max().tz_localize(None))\n"
        "END = pd.Timestamp(((raw_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())\n"
        "END_X = (END + pd.Timedelta(days=1)).tz_localize(TZ)\nPX = PX[PX.index < END_X]\nY = END.year\n"
        "MTU15 = pd.Timestamp('2025-10-01').tz_localize(TZ)\n"
        "LTM0 = (END + pd.Timedelta(days=1) - pd.DateOffset(years=1)).tz_localize(TZ)\n"
        "print('cut-off:', END.date(), '| last 12 months from', LTM0.date())\n\n" +
        fsrc("hfloor", "on_price_grid", "wmean") + "\n\n\n"
        "GR = {z: on_price_grid(z, z) for z in ('RO', 'BG', 'HU')}\nro = GR['RO']\nLOC_YEAR = PX.index.year\n"
        "CAP = pd.read_csv(DATA + 'installed_capacity_yearly.csv')\n"
        "print(CAP[CAP['type'].str.startswith('Solar')].pivot(index='year', columns='country', values='gw').loc[2019:])\n"
        "twh = {y: (ro['solar'][LOC_YEAR == y] * PX['dur'][LOC_YEAR == y]).sum() / 1e6 for y in range(2019, Y + 1)}\n"
        "print({y: round(v, 2) for y, v in twh.items()}, '(TWh of Romanian solar; last year to the cut-off)')"))

    # §2
    C.append(md(T("## §2 The merit-order effect on the real OPCOM curves\nAdd X MW of supply at 0 EUR/MWh (solar, wind) or X MW of demand at any "
                  "price (batteries charging) and recompute the clearing price. Cross-border flows, blocks and hourly orders stay at their accepted "
                  "values, so this is an upper bound for the coupled market.",
                  "## §2 Efectul ordinii de merit pe curbele reale OPCOM\nAdăugăm X MW de ofertă la 0 EUR/MWh (solar, eolian) sau X MW de cerere la "
                  "orice preț (încărcarea bateriilor) și recalculăm prețul de închidere. Fluxurile transfrontaliere, blocurile și ordinele orare "
                  "rămîn la valorile acceptate, deci rezultatul este o limită superioară pentru piața cuplată.")))
    C.append(code(
        "CURVES = pd.read_csv(DATA + 'opcom_pzu_curves.csv')\nCMETA = json.load(open(DATA + 'opcom_pzu_curves_meta.json'))\n\n" +
        fsrc("curve_fns", "clear") + "\n\n\n"
        "XGRID = np.arange(0, 401, 5)\nfig, axs = plt.subplots(1, 2, figsize=(11, 3.2), sharey=True)\nres = {}\n"
        "for ax, iv in zip(axs, CMETA['intervals']):\n"
        "    S, D_ = curve_fns(iv['interval_label']); P0 = iv['official_clearing_price_eur_mwh']\n"
        "    sup = [clear(S, D_, xs=x) if x else P0 for x in XGRID]; dem = [clear(S, D_, xd=x) if x else P0 for x in XGRID]\n"
        "    res[iv['opcom_interval']] = (sup, dem)\n"
        "    ax.plot(XGRID, sup, label='+X MW supply at 0'); ax.plot(XGRID, dem, '--', label='+X MW demand at any price')\n"
        "    ax.set_title(iv['interval_label']); ax.set_xlabel('X (MW)')\n"
        "    print(iv['interval_label'][:3], 'official', P0, '| +25 MW supply ->', round(sup[5], 2), '| +100 MW demand ->', round(dem[20], 2))\n"
        "axs[0].set_ylabel('EUR/MWh'); axs[0].legend(); plt.show()\n"
        "# batteries: X MW charging at midday (Q45) and discharging in the evening (Q77)\n"
        "for x in (50, 100, 200):\n"
        "    k = int(x / 5)\n"
        "    print(f'{x} MW of batteries: evening - midday spread =', round(res[77][0][k] - res[45][1][k], 2), 'EUR/MWh')"))

    # §3
    C.append(md(T("## §3 Price, solar, wind and residual load: hourly regression\nMonth, hour and weekday fixed effects; HAC standard errors (48 lags).",
                  "## §3 Prețul, solarul, eolianul și consumul rezidual: regresie pe date orare\nEfecte fixe pentru lună, oră și ziua săptămînii; "
                  "erori standard HAC (48 de decalaje).")))
    C.append(code(
        "H = pd.DataFrame({'P': PX['RO'], 'dur': PX['dur'], 'load': ro['load'], 'wind': ro['wind_onshore'], 'solar': ro['solar']})\n"
        "H = H[H.index >= pd.Timestamp('2023-01-01').tz_localize(TZ)]\n"
        "HH = (H[['P', 'load', 'wind', 'solar']].mul(H['dur'], axis=0).groupby(hfloor(H.index)).sum()\n"
        "      .div(H['dur'].groupby(hfloor(H.index)).sum(), axis=0)).dropna()\n"
        "HH[['load', 'wind', 'solar']] /= 1000\nHH['resid'] = HH['load'] - HH['wind'] - HH['solar']\n"
        "fe = pd.get_dummies(pd.DataFrame({'m': HH.index.strftime('%Y-%m'), 'h': HH.index.hour.astype(str), 'w': HH.index.dayofweek.astype(str)}), drop_first=True).astype(float)\n"
        "fe.index = HH.index\n"
        "R1 = sm.OLS(HH['P'], sm.add_constant(pd.concat([HH[['load', 'wind', 'solar']], fe], axis=1))).fit(cov_type='HAC', cov_kwds={'maxlags': 48})\n"
        "print(R1.params[['load', 'wind', 'solar']].round(2), R1.bse[['load', 'wind', 'solar']].round(2), 'R2', round(R1.rsquared, 3))\n"
        "for y in (2023, Y - 1, Y):\n"
        "    s = HH[HH.index.year == y]; b = s.groupby(pd.cut(s['resid'], np.arange(-2, 9.01, 0.5)), observed=True)['P'].agg(['mean', 'count'])\n"
        "    b = b[b['count'] >= 20]; plt.plot([i.mid for i in b.index], b['mean'], 'o-', ms=3, label=str(y))\n"
        "plt.xlabel('residual load (GW)'); plt.ylabel('mean price (EUR/MWh)'); plt.legend(); plt.show()"))

    # §4
    C.append(md(T("## §4 Capture prices, capture rates and cannibalisation",
                  "## §4 Prețul capturat, rata de captare și canibalizarea")))
    C.append(code(
        fsrc("capture") + "\n\n\n"
        "rows = []\nfor z in ('RO', 'BG', 'HU'):\n    for tech in ('solar', 'wind_onshore'):\n        for y in range(2019, Y + 1):\n"
        "            m = pd.Series(LOC_YEAR == y, index=PX.index)\n"
        "            if GR[z][tech][m].notna().sum() < 0.9 * m.sum():\n                continue\n"
        "            cp, base, e = capture(z, tech, m); rows.append((z, tech, y, round(cp, 1), round(base, 1), round(cp / base * 100, 1)))\n"
        "CT = pd.DataFrame(rows, columns=['zone', 'tech', 'year', 'CP', 'base', 'CR %'])\n"
        "print(CT[CT.zone == 'RO'].pivot(index='year', columns='tech', values='CR %'))\n"
        "print(CT[CT.tech == 'solar'].pivot(index='year', columns='zone', values='CR %'))\n\n"
        "# monthly cannibalisation regression (Romania)\nmon = []\n"
        "for per in pd.period_range('2019-01', END.strftime('%Y-%m'), freq='M'):\n"
        "    mk = pd.Series(PX.index.to_period('M') == per, index=PX.index)\n"
        "    cp, base, e = capture('RO', 'solar', mk); ld = (ro['load'][mk] * PX['dur'][mk]).sum()\n"
        "    mon.append((cp / base * 100, e / ld * 100))\nmon = pd.DataFrame(mon, columns=['cr', 'share'])\n"
        "rc = sm.OLS(mon['cr'], sm.add_constant(mon['share'])).fit(cov_type='HAC', cov_kwds={'maxlags': 6})\n"
        "print('slope b =', round(rc.params['share'], 2), 'SE', round(rc.bse['share'], 2))\n\n"
        "# share of solar energy sold in the cheapest 10% of hours\n"
        "for y in (2019, 2023, 2025, Y):\n"
        "    m = (LOC_YEAR == y) & PX['RO'].notna().values & ro['solar'].notna().values\n"
        "    p_, g_, w_ = PX['RO'][m].values, ro['solar'][m].values, PX['dur'][m].values\n"
        "    o = np.argsort(p_, kind='stable'); tsh = np.cumsum(w_[o]) / w_.sum(); esh = np.cumsum((g_ * w_)[o]) / (g_ * w_).sum()\n"
        "    print(y, 'solar energy in cheapest 10%% of hours: %.1f%%' % (esh[np.searchsorted(tsh, 0.10)] * 100))\n"
        "    plt.plot(tsh * 100, esh * 100, label=str(y))\nplt.plot([0, 100], [0, 100], 'k', lw=0.5); plt.legend(); plt.show()"))

    # §5
    C.append(md(T("## §5 Negative prices: hour-equivalents, curtailment value, hidden quarter-hours",
                  "## §5 Prețurile negative: ore echivalente, valoarea opririi, sferturile de oră ascunse")))
    C.append(code(
        "neg = pd.DataFrame({z: {y: PX['dur'][(LOC_YEAR == y) & (PX[z] < 0).values].sum() for y in range(2019, Y + 1)} for z in ['RO', 'BG', 'HU', 'DE_LU']})\n"
        "print(neg.round(2))\n"
        "m = (LOC_YEAR == 2025) & PX['RO'].notna().values & ro['solar'].notna().values\n"
        "p_, e_ = PX['RO'][m], ro['solar'][m] * PX['dur'][m]\n"
        "print('2025: share of solar output at negative prices %.1f%%' % (e_[p_ < 0].sum() / e_.sum() * 100),\n"
        "      '| gain from stopping, EUR per MWh of output: %.2f' % ((p_.clip(lower=0) * e_).sum() / e_.sum() - (p_ * e_).sum() / e_.sum()))\n"
        "q = PX.loc[PX.index >= MTU15, ['RO']].copy(); q['hm'] = q['RO'].groupby(hfloor(q.index)).transform('mean')\n"
        "print('negative quarter-hours:', int((q['RO'] < 0).sum()), '= %.2f h;' % ((q['RO'] < 0).sum() * 0.25),\n"
        "      'inside hours with a non-negative average:', int(((q['RO'] < 0) & (q['hm'] >= 0)).sum()))"))

    # §6
    C.append(md(T("## §6 Intraday shape and daily spreads", "## §6 Profilul zilnic și diferențele zilnice de preț")))
    C.append(code(
        fsrc("day_groups", "tbk") + "\n\n\n"
        "qq = PX.loc[PX.index >= max(LTM0, MTU15), ['RO']].copy(); qq['slot'] = qq.index.hour * 4 + qq.index.minute // 15\n"
        "for s, ms in {'winter': [12, 1, 2], 'spring': [3, 4, 5], 'summer': [6, 7, 8], 'autumn': [9, 10, 11]}.items():\n"
        "    pr = qq[qq.index.month.isin(ms)].groupby('slot')['RO'].mean(); plt.step(np.arange(96) / 4, pr.values, where='post', label=s)\n"
        "    print(s, 'min %.1f at slot %d, max %.1f at slot %d' % (pr.min(), pr.idxmin(), pr.max(), pr.idxmax()))\n"
        "plt.legend(); plt.xlabel('hour (CET)'); plt.show()\n"
        "for z in ['RO', 'BG', 'HU', 'DE_LU']:\n"
        "    dg = day_groups(z, start=pd.Timestamp('2019-01-01').tz_localize(TZ), hourly=True)\n"
        "    sp = pd.Series({d: tbk(p, w, 2) for d, (p, w) in dg.items()})\n"
        "    print(z, sp.groupby(sp.index.year).mean().round(1).to_dict())"))

    # §7
    C.append(md(T("## §7 The battery linear programme: perfect foresight and forecast rules\nOne LP per delivery day (HiGHS). The rules use only "
                  "prices known at 12:00 CET on d−1. Takes about a minute.",
                  "## §7 Programul liniar al bateriei: informație perfectă și reguli de prognoză\nCîte un program liniar pentru fiecare zi de livrare "
                  "(HiGHS). Regulile folosesc numai prețurile cunoscute la 12:00 CET în ziua d−1. Durează aproximativ un minut.")))
    C.append(code(
        fsrc("battery_day", "revenue", "run_battery", "yesterday", "week_ago_mean") + "\n\n\n"
        "dg_all = day_groups('RO', start=pd.Timestamp('2019-01-01').tz_localize(TZ))\n"
        "pf2 = run_battery(dg_all, 2)\nprint('2-hour battery, perfect foresight, thousand EUR per MW and year:',\n"
        "      (pf2.groupby(pf2.index.year).sum() / 1000).round(1).to_dict())\n"
        "ltm = day_groups('RO', start=LTM0); ext = day_groups('RO', start=LTM0 - pd.Timedelta(days=8))\nLT = {}\n"
        "for E in DURS:\n"
        "    pf = run_battery(ltm, E); wk = run_battery(ltm, E, week_ago_mean(ext)); yd = run_battery(ltm, E, yesterday(ext))\n"
        "    cm = pf.index.intersection(wk.index).intersection(yd.index); LT[E] = pf\n"
        "    print(f'{E} h: perfect {pf.sum()/1000:.1f} kEUR/MW; 7-day rule {wk[cm].sum()/pf[cm].sum()*100:.1f}%; yesterday {yd[cm].sum()/pf[cm].sum()*100:.1f}%')"))

    # §8
    C.append(md(T("## §8 15-minute vs hourly prices, the region, and the break-even investment",
                  "## §8 Prețuri pe 15 minute sau orare, regiunea și investiția maximă justificată")))
    C.append(code(
        "ltm_h = day_groups('RO', start=LTM0, hourly=True)\n"
        "for E in DURS:\n    hr = run_battery(ltm_h, E)\n"
        "    print(f'{E} h: hourly {hr.sum()/1000:.1f} -> 15-min {LT[E].sum()/1000:.1f} kEUR/MW ({(LT[E].sum()/hr.reindex(LT[E].index).sum()-1)*100:+.1f}%)')\n"
        "for z in ['BG', 'HU', 'DE_LU']:\n    s = run_battery(day_groups(z, start=LTM0), 2)\n"
        "    print(z, '2-hour battery, last 12 months: %.1f kEUR/MW; daily correlation with RO %.2f' % (s.sum() / 1000, pd.concat([LT[2], s], axis=1).dropna().corr().iloc[0, 1]))\n"
        "af = (1 - (1 + R_DISC) ** -LIFE) / R_DISC\nprint('annuity factor %.2f; break-even EUR/kW (2 h, perfect foresight) %.0f' % (af, LT[2].sum() * 365 / len(LT[2]) * af / 1000))"))

    # §9
    C.append(md(T("## §9 Case study: the month with the most negative hours of the year",
                  "## §9 Studiu de caz: luna cu cele mai multe ore cu preț negativ din an")))
    C.append(code(
        "negm = PX.loc[(PX['RO'] < 0) & (PX.index.year == Y), 'dur']\nnegm = negm.groupby(negm.index.to_period('M')).sum()\n"
        "CM = negm.idxmax(); print('month:', CM, '| negative hours %.2f' % negm.max())\n"
        "mk = pd.Series(PX.index.to_period('M') == CM, index=PX.index)\ncp, base, _ = capture('RO', 'solar', mk)\n"
        "print('solar capture rate %.1f%% (%.1f vs %.1f EUR/MWh)' % (cp / base * 100, cp, base))\n"
        "d2 = pf2[[pd.Period(t, 'M') == CM for t in pf2.index]]\nprint('2-hour battery: %.0f EUR/MW per day in the month' % d2.mean())\n"
        "wk0 = (d2.index[0] - pd.Timedelta(days=d2.index[0].dayofweek))\n"
        "w = PX[(PX.index.tz_localize(None) >= wk0) & (PX.index.tz_localize(None) < wk0 + pd.Timedelta(days=21))]\n"
        "fig, ax = plt.subplots(2, 1, figsize=(11, 4), sharex=True)\nax[0].step(w.index.tz_localize(None), w['RO'], where='post'); ax[0].axhline(0, color='k', lw=0.5)\n"
        "ax[1].plot(w.index.tz_localize(None), ro.loc[w.index, 'solar'] / 1000, label='solar GW'); ax[1].plot(w.index.tz_localize(None), ro.loc[w.index, 'wind_onshore'] / 1000, label='wind GW')\n"
        "ax[1].legend(); plt.show()"))
    return C


def build(lang):
    nb = nbformat.v4.new_notebook()
    nb.cells = cells(lang)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    name = "L6_notebook.ipynb" if lang == "en" else "L6_notebook_ro.ipynb"
    add_colab_cell(nb, lang)
    ExecutePreprocessor(timeout=3600, kernel_name="python3").preprocess(nb, {"metadata": {"path": NBDIR}})
    os.makedirs(NBDIR, exist_ok=True)
    with open(os.path.join(NBDIR, name), "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("executed and wrote", name)


if __name__ == "__main__":
    for lang in (sys.argv[1:] or ["en", "ro"]):
        build(lang)
