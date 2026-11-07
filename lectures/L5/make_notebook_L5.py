"""
make_notebook_L5.py -- writes and executes the student notebooks of Lecture 5 (EMQA)
=====================================================================================
    notebooks/L5_notebook.ipynb      (English)
    notebooks/L5_notebook_ro.ipynb   (Romanian)
Same code in both; only the text differs. The computational functions are copied verbatim from analysis_L5.py (extracted
with the ast module), so the notebook runs exactly the code behind the slides. Paths are relative to notebooks/ (data in
../data/clean, written by data/download_all.py and data/download_L5.py). Section numbers match the "Experiment yourself"
pointers on the slides.
Run:  python3 lectures/L5/make_notebook_L5.py
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
SRC = open(os.path.join(HERE, "analysis_L5.py"), encoding="utf-8").read()
TREE = ast.parse(SRC)


def fsrc(*names):
    """Source of top-level functions of analysis_L5.py, in the given order."""
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
        "# Energy Markets Quantitative Analysis — Lecture 5: Energy derivatives and hedging\n"
        "Prof. dr. Daniel Traian Pele — Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting\n\n"
        "This notebook reproduces the numbers and charts of Lecture 5 from the real data in `../data/clean` (see `../data/SOURCES.md`, "
        "section *Lecture 5 additions*). Section numbers (§) match the *Experiment yourself* pointers on the slides.\n\n"
        "**Data.** Romanian forward prices = OPCOM PCCB-LE-flex auction results (one closing price per traded session, lei converted "
        "to EUR with the ECB rate of the auction day). Spot = OPCOM day-ahead (PZU) prices. Gas = TTF (World Bank monthly; NYMEX "
        "single contracts), carbon = EUA, coal = World Bank. Cut-off = last complete month.",
        "# Analiza cantitativă a piețelor de energie — Cursul 5: Derivate pe energie și acoperirea riscului de preț\n"
        "Prof. dr. Daniel Traian Pele — Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică\n\n"
        "Acest notebook Jupyter reproduce cifrele și graficele din cursul 5 pe datele reale din `../data/clean` (vezi `../data/SOURCES.md`, "
        "secțiunea *Lecture 5 additions*). Numerele secțiunilor (§) corespund indicațiilor *Exercițiu practic* de pe diapozitive.\n\n"
        "**Date.** Prețurile forward din România = rezultatele licitațiilor OPCOM PCCB-LE-flex (un preț de închidere pentru fiecare "
        "sesiune încheiată, convertit din lei în EUR cu cursul BCE din ziua licitației). Spot = prețurile PZU ale OPCOM. Gaze = TTF "
        "(Banca Mondială, lunar; contracte NYMEX), carbon = EUA, cărbune = Banca Mondială. Data-limită = ultima lună completă.")))

    # ---------------------------------------------------------------- §1
    C.append(md(T("## §1 Data and the Romanian forward market", "## §1 Datele și piața forward din România")))
    C.append(code(
        "import numpy as np, pandas as pd, matplotlib.pyplot as plt, statsmodels.api as sm, warnings\n"
        "from scipy.stats import norm\nwarnings.filterwarnings('ignore')\n"
        "DATA = '../data/clean/'\nSEED = 20261106\n"
        "ETA_GAS, ETA_COAL = 0.50, 0.38      # efficiencies (assumed)\n"
        "EF_GAS, EF_COAL = 0.202, 0.341      # t CO2 per MWh thermal (IPCC 2006)\n"
        "COAL_MWH_T = 6.978                  # MWh thermal per tonne of 6000 kcal/kg coal\n\n"
        "PD = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "raw_last = PD['RO'].dropna().index.max()\n"
        "END = pd.Timestamp(((raw_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())\n"
        "FW = pd.read_csv(DATA + 'opcom_forward_trades.csv', parse_dates=['auction_date', 'delivery_start', 'delivery_end'])\n"
        "FW = FW[FW['auction_date'] <= END].copy()\n"
        "RATES = pd.read_csv(DATA + 'ecb_ron_estr_daily.csv', parse_dates=['date']).set_index('date')\n"
        "print('cut-off:', END.date(), '| traded forward sessions:', len(FW), '| TWh:', round(FW['mwh'].sum() / 1e6, 2))\n"
        "FW.head()"))
    C.append(code(
        fsrc("kind_of", "vwap", "realised") + "\n\n\n"
        "FW['kind'] = [kind_of(s, e) for s, e in zip(FW['delivery_start'], FW['delivery_end'])]\n"
        "FW['lead_m'] = ((FW['delivery_start'].dt.year - FW['auction_date'].dt.year) * 12 + FW['delivery_start'].dt.month - FW['auction_date'].dt.month)\n"
        "BASE = FW[(FW['profile'] == 'banda LD') & (FW['kind'] != 'other')].copy()\n"
        "vol = FW.pivot_table(index=FW['auction_date'].dt.year, columns='kind', values='mwh', aggfunc='sum').fillna(0) / 1e6\n"
        "print(vol.round(2))\n"
        "vol.plot.bar(stacked=True, figsize=(9, 3)); plt.ylabel('TWh'); plt.show()\n"
        "print((FW.groupby('seller')['mwh'].sum().sort_values(ascending=False).head(5) / FW['mwh'].sum() * 100).round(1))"))

    # ---------------------------------------------------------------- §2
    C.append(md(T("## §2 The 2021–2022 crisis: the 2022 forward against the 2022 spot",
                  "## §2 Criza din 2021–2022: forward-ul pentru 2022 față de spotul din 2022")))
    C.append(code(
        "CY = BASE[BASE['kind'] == 'Y'].copy(); CY['dy'] = CY['delivery_start'].dt.year\n"
        "c22 = CY[CY['dy'] == 2022]\n"
        "S22 = realised(pd.Timestamp('2022-01-01'), pd.Timestamp('2022-12-31')); F22 = vwap(c22)\n"
        "print('VWAP 2022 baseload %.2f EUR/MWh (%d auctions) | realised 2022 spot %.2f | saving per MW-year %.0f EUR' % (F22, len(c22), S22, (S22 - F22) * 8760))\n"
        "for a0, a1 in [('2020-01-01', '2020-12-31'), ('2021-01-01', '2021-06-30'), ('2021-07-01', '2021-12-31')]:\n"
        "    g = c22[(c22['auction_date'] >= a0) & (c22['auction_date'] <= a1)]; print(a0, a1, 'VWAP %.2f, n=%d' % (vwap(g), len(g)))\n"
        "sm_ = PD['RO'].loc['2020':'2022'].resample('MS').mean()\n"
        "fig, ax = plt.subplots(figsize=(9, 3)); ax.plot(sm_.index, sm_.values, label='RO monthly spot')\n"
        "ax.scatter(c22['auction_date'], c22['price_eur_mwh'], s=8, color='C1', label='2022 forward, one auction')\n"
        "ax.hlines([S22, F22], pd.Timestamp('2022-01-01'), pd.Timestamp('2022-12-31'), colors=['k', 'C1'], linestyles='--'); ax.legend(); plt.show()"))

    # ---------------------------------------------------------------- §3
    C.append(md(T("## §3 Futures margin, the forward curve and the ex-post forward premium",
                  "## §3 Marja futures, curba forward și prima forward ex post")))
    C.append(code(
        "TTFC = pd.read_csv(DATA + 'ttf_futures_contracts_daily.csv', parse_dates=['date']).set_index('date').loc[:END]\n"
        "z26 = TTFC['2026-12'].dropna(); dz = z26.diff().dropna()\n"
        "print('TTF Dec-2026: largest daily move %.2f EUR/MWh on %s -> margin call for 10 MW x 744 h = %.0f EUR'\n"
        "      % (dz.abs().max(), dz.abs().idxmax().date(), dz.abs().max() * 7440))\n"
        "CURVE_FROM = (END - pd.DateOffset(months=2) + pd.Timedelta(days=1)).normalize()\n"
        "cur = BASE[(BASE['auction_date'] >= CURVE_FROM) & (BASE['delivery_start'] > END)]\n"
        "print(cur.groupby(['delivery_start', 'delivery_end', 'kind']).apply(vwap).round(2))"))
    C.append(code(
        fsrc("premium_table", "nw_t") + "\n\n\n"
        "PT = premium_table(BASE)\n"
        "M1 = PT[(PT['kind'] == 'M') & (PT['lead_m'] == 1)]\n"
        "MP = M1.groupby('delivery_start').apply(lambda g: pd.Series({'F': vwap(g), 'S': g['S'].iloc[0]}))\n"
        "MP['prem'] = MP['F'] - MP['S']\n"
        "mu, se, tt, pp = nw_t(MP['prem'])\n"
        "print('one-month-ahead monthly band: %d months, mean premium %.2f EUR/MWh, HAC t = %.2f, p = %.3f' % (len(MP), mu, tt, pp))\n"
        "MP['prem'].plot.bar(figsize=(10, 3), color=np.where(MP['prem'] > 0, 'C1', 'C0')); plt.ylabel('F - realised'); plt.show()"))

    # ---------------------------------------------------------------- §4
    C.append(md(T("## §4 Spark, dark and clean spreads; the gas plant as a strip of options",
                  "## §4 Spark spread, dark spread și clean spread; centrala pe gaze ca serie de opțiuni")))
    C.append(code(
        "TTFM = pd.read_csv(DATA + 'ttf_monthly.csv'); TTFM.index = pd.PeriodIndex(TTFM['month'], freq='M').to_timestamp()\n"
        "EUA = pd.read_csv(DATA + 'eua_daily.csv', parse_dates=['date']).set_index('date')\n"
        "COAL = pd.read_csv(DATA + 'coal_monthly.csv'); COAL.index = pd.PeriodIndex(COAL['month'], freq='M').to_timestamp()\n"
        "FUEL = pd.read_csv(DATA + 'fuels_daily.csv', parse_dates=['date']).set_index('date')\n"
        "m_idx = pd.date_range('2015-01-01', END.replace(day=1), freq='MS')\n"
        "PM = PD[['RO', 'HU', 'DE_LU']].resample('MS').mean().reindex(m_idx)\n"
        "full_m = PD[['RO', 'HU', 'DE_LU']].resample('MS').count().reindex(m_idx).eq(pd.Series(m_idx.days_in_month, index=m_idx), axis=0)\n"
        "PM = PM.where(full_m)\n"
        "eua_a = EUA['eua_eex_auction_eur_t'].dropna().resample('MS').mean(); eua_e = EUA['eua_etc_co2l_eur_per_unit'].dropna().resample('MS').mean()\n"
        "EUAM = eua_a.reindex(m_idx).fillna(eua_e.reindex(m_idx).where(m_idx > eua_a.index.max()))\n"
        "GAS = TTFM['ttf_eur_mwh'].reindex(m_idx)\n"
        "COALE = (COAL['coal_southafrica_usd_t'].reindex(m_idx) / FUEL['eurusd_ecb'].resample('MS').mean().reindex(m_idx)) / COAL_MWH_T\n\n\n" +
        fsrc("spreads") + "\n\n\n"
        "SPR = {z: pd.DataFrame(dict(zip(['ss', 'css', 'ds', 'cds'], spreads(PM[z], GAS, COALE, EUAM)))) for z in ['RO', 'DE_LU']}\n"
        "print(pd.DataFrame({'CSS RO': SPR['RO']['css'], 'CSS DE': SPR['DE_LU']['css'], 'CDS RO': SPR['RO']['cds']}).groupby(lambda x: x.year).mean().round(2))\n"
        "pd.DataFrame({'CSS RO': SPR['RO']['css'], 'CSS DE': SPR['DE_LU']['css'], 'CDS RO': SPR['RO']['cds']}).plot(figsize=(10, 3)); plt.axhline(0, color='k', lw=0.6); plt.show()"))
    C.append(code(
        "HP = pd.read_csv(DATA + 'power_da_prices_native_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
        "HP.index = HP.index.tz_convert('Europe/Brussels')\n"
        "H0 = (END - pd.DateOffset(months=12) + pd.Timedelta(days=1)).normalize()\n"
        "HH = HP.loc[str(H0.date()):str(END.date())].copy(); HH['w'] = HH['mtu_minutes'] / 60.0   # hour-equivalents\n"
        "cost = GAS / ETA_GAS + EF_GAS / ETA_GAS * EUAM\n"
        "HH['c'] = cost.reindex(HH.index.tz_localize(None).to_period('M').to_timestamp()).values\n"
        "for z in ['RO', 'DE_LU']:\n"
        "    s = (HH[z] - HH['c']).dropna(); w = HH.loc[s.index, 'w']\n"
        "    print(z, 'in the money %.1f%% of hours | must-run %.0f EUR/MW | flexible %.0f EUR/MW' % (100 * w[s > 0].sum() / w.sum(), (s * w).sum(), (np.maximum(s, 0) * w).sum()))"))

    # ---------------------------------------------------------------- §5
    C.append(md(T("## §5 Minimum-variance hedge ratio, basis risk and shape risk",
                  "## §5 Raportul de acoperire cu varianță minimă, riscul de bază și riscul de profil")))
    C.append(code(
        fsrc("hedge_ratio") + "\n\n\n"
        "dP = PM.diff().dropna()\n"
        "for z in ['HU', 'DE_LU']:\n"
        "    r = hedge_ratio(dP['RO'], dP[z]); h_in = hedge_ratio(dP.loc[:'2020-12-01', 'RO'], dP.loc[:'2020-12-01', z])['h']\n"
        "    oos = dP.loc['2021-01-01':]\n"
        "    vr = 1 - (oos['RO'] - h_in * oos[z]).var() / oos['RO'].var()\n"
        "    print(z, 'h* = %.3f (HAC s.e. %.3f), bootstrap 95%% [%.2f; %.2f], R2 = %.3f | h* 2015-2020 = %.2f, variance cut from 2021: %.1f%%'\n"
        "          % (r['h'], r['se'], r['lo'], r['hi'], r['r2'], h_in, 100 * vr))\n"
        "BAS = pd.DataFrame({'RO-HU': PM['RO'] - PM['HU'], 'RO-DE': PM['RO'] - PM['DE_LU']})\n"
        "print(BAS.describe().round(2)); BAS.plot(figsize=(10, 3)); plt.axhline(0, color='k', lw=0.6); plt.show()"))
    C.append(code(
        "GH = pd.read_csv(DATA + 'generation_ro_mw_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
        "PH = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
        "J = pd.concat([PH['RO'], GH['load'], GH['solar']], axis=1).loc[:str(END.date()) + ' 21:00'].dropna()\n"
        "J = J[J.index >= '2015-01-05']; J['y'] = J.index.tz_convert('Europe/Brussels').year\n\n\n" +
        fsrc("profile_factor") + "\n\n\n"
        "PF = J.groupby('y').apply(profile_factor); PF['f_load'] = PF['load_w'] / PF['base']; PF['f_solar'] = PF['solar_w'] / PF['base']\n"
        "print(PF.round(3)); PF[['f_load', 'f_solar']].plot(marker='o', figsize=(9, 3)); plt.axhline(1, color='k', lw=0.6); plt.show()"))

    # ---------------------------------------------------------------- §6
    C.append(md(T("## §6 Options: Black-76 with real inputs, volatility estimates, the Samuelson effect",
                  "## §6 Opțiuni: Black-76 cu date reale, estimări ale volatilității, efectul Samuelson")))
    C.append(code(
        fsrc("black76", "ann_vol", "cal_vol") + "\n\n\n"
        "CY_ = CY  # calendar-year baseload auctions\n"
        "DL, DT = [], []\n"
        "for y in [END.year - 1, END.year, END.year + 1]:\n"
        "    dl, dt = cal_vol(CY_[CY_['dy'] == y]); DL.append(dl); DT.append(dt)\n"
        "sig_cal = np.sqrt(sum((x ** 2).sum() for x in DL) / sum(x.sum() for x in DT))\n"
        "sig_gas = ann_vol(TTFC['2027-01']).iloc[-60:].std() * np.sqrt(252)\n"
        "z = M1['lr'] / np.sqrt(M1['T']); sig_term = z.std(ddof=1)\n"
        "print('sigma: Romanian yearly forwards %.3f | TTF Jan-2027, 60 days %.3f | monthly spot vs forward %.3f' % (sig_cal, sig_gas, sig_term))\n"
        "F0 = vwap(cur[cur['kind'] == 'Y']); r0 = RATES['estr_pct'].loc[:END].dropna().iloc[-1] / 100\n"
        "T0 = (pd.Timestamp(f'{END.year}-12-15') - END).days / 365.25\n"
        "for lab, sg in [('yearly forwards', sig_cal), ('TTF gas', sig_gas)]:\n"
        "    c = black76(F0, F0, T0, r0, sg, 'call'); p = black76(F0, F0, T0, r0, sg, 'put')\n"
        "    print('%-16s F=%.2f T=%.3f r=%.2f%% -> call %.2f put %.2f delta %.3f vega %.3f | cap 1.1F %.2f, floor 0.9F %.2f'\n"
        "          % (lab, F0, T0, 100 * r0, c[0], p[0], c[1], c[2], black76(F0, 1.1 * F0, T0, r0, sg)[0], black76(F0, 0.9 * F0, T0, r0, sg, 'put')[0]))"))
    C.append(code(
        "W12 = (END - pd.DateOffset(months=12) + pd.Timedelta(days=1)).normalize()\n"
        "for col in TTFC.columns:\n"
        "    r_ = ann_vol(TTFC[col]); print(col, 'last 12 months %.1f%%, 2022 %.1f%%' % (r_.loc[W12:END].std() * np.sqrt(252) * 100, r_.loc['2022'].std() * np.sqrt(252) * 100))\n"
        "pd.DataFrame({c: ann_vol(TTFC[c], 60) for c in ['2026-12', '2027-05']}).plot(figsize=(9, 3)); plt.ylabel('60-day volatility'); plt.show()"))

    # ---------------------------------------------------------------- §7
    C.append(md(T("## §7 Case study: a Romanian supplier in the current year, and a producer",
                  "## §7 Studiu de caz: un furnizor din România în anul curent și un producător")))
    C.append(code(
        "c26 = CY[CY['dy'] == END.year]; F26 = vwap(c26)\n"
        "mm = pd.date_range(f'{END.year}-01-01', END.replace(day=1), freq='MS')\n"
        "S26 = pd.Series([realised(m, m + pd.offsets.MonthEnd(0)) for m in mm], index=mm)\n"
        "hrs = pd.Series([((m + pd.offsets.MonthEnd(0) + pd.Timedelta(days=1)).tz_localize('Europe/Brussels') - m.tz_localize('Europe/Brussels')) / pd.Timedelta(hours=1) for m in mm], index=mm)\n"
        "ref = c26[c26['auction_date'] >= pd.Timestamp(f'{END.year - 1}-10-01')]; Fref = vwap(ref)\n"
        "BUYD = pd.Timestamp(f'{END.year - 1}-12-15'); rb = RATES['estr_pct'].loc[:BUYD].dropna().iloc[-1] / 100\n"
        "prem_m = pd.Series([black76(Fref, Fref, ((m + pd.Timedelta(days=14)) - BUYD).days / 365.25, rb, sig_term)[0] for m in mm], index=mm)\n"
        "ST = pd.DataFrame({'spot': S26, 'fwd': F26, 'half': 0.5 * F26 + 0.5 * S26, 'cap': S26 - np.maximum(S26 - Fref, 0) + prem_m})\n"
        "w = hrs / hrs.sum()\n"
        "print(pd.DataFrame({'mean': (ST.mul(w, axis=0)).sum(), 'sd': ST.std(), 'max': ST.max(), 'EUR per MW': ST.mul(hrs, axis=0).sum()}).round(2))\n"
        "ST.plot(marker='o', figsize=(9, 3)); plt.ylabel('EUR/MWh'); plt.show()\n"
        "c25 = CY[CY['dy'] == END.year - 1]; S25 = realised(pd.Timestamp(f'{END.year - 1}-01-01'), pd.Timestamp(f'{END.year - 1}-12-31'))\n"
        "print('producer, %d: sold forward at VWAP %.2f vs realised %.2f EUR/MWh' % (END.year - 1, vwap(c25), S25))"))
    C.append(md(T("**Try it.** Change the hedge share (e.g. 70%), the cap strike (e.g. 1.1 × Fref) or the volatility, and see how the "
                  "mean cost and its month-to-month standard deviation move.",
                  "**Încercați.** Schimbați ponderea acoperită (de exemplu 70%), prețul de exercitare al plafonului (de exemplu 1,1 × Fref) "
                  "sau volatilitatea și urmăriți cum se modifică costul mediu și abaterea lui standard de la o lună la alta.")))
    return C


def build(lang):
    nb = nbformat.v4.new_notebook()
    nb.cells = cells(lang)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    name = "L5_notebook.ipynb" if lang == "en" else "L5_notebook_ro.ipynb"
    add_colab_cell(nb, lang)
    ExecutePreprocessor(timeout=1800, kernel_name="python3").preprocess(nb, {"metadata": {"path": NBDIR}})
    os.makedirs(NBDIR, exist_ok=True)
    with open(os.path.join(NBDIR, name), "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("executed and wrote", name)


if __name__ == "__main__":
    for lang in (sys.argv[1:] or ["en", "ro"]):
        build(lang)
