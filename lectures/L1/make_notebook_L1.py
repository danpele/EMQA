"""
make_notebook_L1.py -- writes and executes the student notebooks of Lecture 1 (EMQA)
=====================================================================================
    notebooks/L1_notebook.ipynb      (English)
    notebooks/L1_notebook_ro.ipynb   (Romanian)
Same code in both (the analysis of analysis_L1.py, simplified for students); only the text differs.
Paths are relative to the notebooks/ folder (data in ../data/clean), so the notebooks run from a clone
of the repository. Section numbers match the "Experiment yourself" pointers on the slides.
Run:  python3 lectures/L1/make_notebook_L1.py
"""

import os
import sys

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
from colab_cell import add_colab_cell  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NBDIR = os.path.abspath(os.path.join(HERE, "..", "..", "notebooks"))


def cells(lang):
    def T(en, ro):
        return en if lang == "en" else ro

    md, code = nbformat.v4.new_markdown_cell, nbformat.v4.new_code_cell
    C = []
    C.append(md(T(
        "# Energy Markets Quantitative Analysis — Lecture 1: Energy markets and their data\n"
        "Prof. dr. Daniel Traian Pele — Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting\n\n"
        "This notebook reproduces the numbers and charts of Lecture 1 from the real data in `../data/clean` "
        "(see `../data/SOURCES.md`). Section numbers (§) match the *Experiment yourself* pointers on the slides.\n\n"
        "**Rules used everywhere:** data are cut at the last complete month; missing values stay missing (never "
        "interpolated, never counted as zero); counts of negative prices are in hour-equivalents (a 15-minute "
        "interval counts 0.25 h).",
        "# Analiza cantitativă a piețelor de energie — Cursul 1: Piețele de energie și datele lor\n"
        "Prof. dr. Daniel Traian Pele — Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică\n\n"
        "Acest notebook Jupyter reproduce numerele și graficele din Cursul 1 pe datele reale din `../data/clean` "
        "(vezi `../data/SOURCES.md`). Numerele secțiunilor (§) corespund indicațiilor *Încercați singuri* de pe slide-uri.\n\n"
        "**Reguli folosite peste tot:** datele se opresc la ultima lună completă; valorile lipsă rămîn lipsă (nu le "
        "interpolăm și nu le socotim zero); prețurile negative se numără în echivalent-ore (un interval de 15 minute "
        "contează 0,25 h).")))
    C.append(md(T("## §1 Data, clocks and the cut-off", "## §1 Date, ceasuri și data-limită")))
    C.append(code(
        "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\nimport statsmodels.api as sm\n"
        "from scipy import stats\nfrom statsmodels.tsa.stattools import acf, pacf, adfuller, kpss\n"
        "from statsmodels.tsa.seasonal import STL, seasonal_decompose\nfrom statsmodels.tsa.holtwinters import SimpleExpSmoothing\n"
        "from statsmodels.stats.diagnostic import acorr_ljungbox\nimport warnings\nwarnings.filterwarnings('ignore')\n\n"
        "DATA = '../data/clean/'\n"
        "P = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "X = pd.read_csv(DATA + 'power_da_prices_native_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
        "X.index = X.index.tz_convert('Europe/Brussels')          # CET/CEST delivery-day clock\n"
        "H = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
        "H.index = H.index.tz_convert('Europe/Brussels')\n"
        "GH = pd.read_csv(DATA + 'generation_ro_mw_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
        "G = pd.read_csv(DATA + 'generation_ro_mw_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "BGH = pd.read_csv(DATA + 'generation_bg_mw_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
        "CB = pd.read_csv(DATA + 'crossborder_ro_mw_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')\n"
        "F = pd.read_csv(DATA + 'fuels_daily.csv', parse_dates=['date']).set_index('date')\n"
        "TTF = pd.read_csv(DATA + 'ttf_monthly.csv'); TTF.index = pd.PeriodIndex(TTF['month'], freq='M').to_timestamp()\n\n"
        "# cut-off: last complete month common to prices and generation\n"
        "raw_last = min(P['RO'].dropna().index.max(), G['hydro_run_of_river'].dropna().index.max())\n"
        "END = (raw_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)\n"
        "Y = END.year\n"
        "end_utc = (END + pd.Timedelta(days=1)).tz_localize('Europe/Brussels').tz_convert('UTC')\n"
        "P, G, CB, F = P.loc[:END], G.loc[:END], CB.loc[:END], F.loc[:END]\n"
        "X, H = X.loc[:str(END.date())], H.loc[:str(END.date())]\n"
        "GH, BGH = GH[GH.index < end_utc], BGH[BGH.index < end_utc]\n"
        "PF = P.asfreq('D')   # full calendar: a change across a gap stays missing\n"
        "print('cut-off:', END.date(), '| 60-min MTUs:', (X['mtu_minutes'] == 60).sum(), '| 15-min MTUs:', (X['mtu_minutes'] == 15).sum())"))
    C.append(code(
        "# missing days in the daily price series (left missing, never filled)\n"
        "for z in ['RO', 'BG']:\n"
        "    s = PF[z].loc[PF[z].first_valid_index():]\n"
        "    print(z, 'first day', s.index.min().date(), '| missing days:', int(s.isna().sum()), [d.date() for d in s[s.isna()].index][:6])"))
    C.append(code(
        "# merit order on the real OPCOM aggregated curves (one day, two quarter-hours)\n"
        "import json\n"
        "CU = pd.read_csv(DATA + 'opcom_pzu_curves.csv'); META = json.load(open(DATA + 'opcom_pzu_curves_meta.json'))\n"
        "fig, axs = plt.subplots(1, 2, figsize=(10, 3.5), sharey=True)\n"
        "for ax, iv in zip(axs, META['intervals']):\n"
        "    for side, col in [('supply', 'tab:blue'), ('demand', 'black')]:\n"
        "        c = CU[(CU['interval'] == iv['interval_label']) & (CU['side'] == side)]\n"
        "        ax.plot(c['quantity_mw'] / 1000, c['price_eur_mwh'].clip(-190, 660), color=col, label=side)\n"
        "    ax.axhline(iv['official_clearing_price_eur_mwh'], color='red', ls='--')\n"
        "    s = CU[(CU['interval'] == iv['interval_label']) & (CU['side'] == 'supply')]\n"
        "    print(iv['interval_label'], '| price', iv['official_clearing_price_eur_mwh'], '| MW offered at <= 0:',\n"
        "          s.loc[s['price_eur_mwh'] <= 0, 'quantity_mw'].max(), '| net import MW:', -iv['net_export_mw'])\n"
        "    ax.set_title(iv['interval_label'][:15]); ax.set_xlabel('GW')\n"
        "axs[0].set_ylabel('EUR/MWh'); axs[0].legend(); plt.show()"))
    C.append(code(
        "# one day of Romanian load: power (MW) and energy (MWh = area under the curve)\n"
        "ld = GH['load'].tz_convert('Europe/Brussels')\n"
        "cnt = ld.groupby(ld.index.date).count()\n"
        "day = max(k for k, v in cnt.items() if v == 24 and pd.Timestamp(k).dayofweek == 2)\n"
        "one = ld[ld.index.date == day]\n"
        "print(day, '| energy MWh:', round(one.sum()), '| mean MW:', round(one.mean()), '| min/max MW:', round(one.min()), round(one.max()))\n"
        "plt.figure(figsize=(9, 3)); plt.step(range(24), one.values, where='post'); plt.fill_between(range(24), one.values, step='post', alpha=0.2)\n"
        "plt.ylabel('MW'); plt.xlabel('hour (CET)'); plt.ylim(0); plt.show()"))
    C.append(md(T("## §2 Romanian generation mix (energy from reported hours, with coverage)",
                  "## §2 Mixul de producție al României (energie din orele raportate, cu acoperire)")))
    C.append(code(
        "GRP = {'Hydro': ['hydro_run_of_river', 'hydro_water_reservoir'], 'Coal': ['brown_coal_lignite', 'hard_coal'],\n"
        "       'Nuclear': ['nuclear'], 'Gas': ['gas'], 'Wind': ['wind_onshore'], 'Solar': ['solar'], 'Biomass': ['biomass']}\n"
        "yr = GH.index.year\n"
        "mix = pd.DataFrame({k: GH[c].sum(axis=1, min_count=len(c)).groupby(yr).sum() / 1e6 for k, c in GRP.items()})   # TWh\n"
        "cov = pd.DataFrame({k: GH[c].sum(axis=1, min_count=len(c)).notna().groupby(yr).mean() for k, c in GRP.items()})\n"
        "full = [y for y in mix.index if y < Y]\n"
        "share = mix.div(mix.sum(axis=1), axis=0) * 100\n"
        "print(share.loc[full].round(1))\n"
        "print('minimum coverage in full years: %.1f%%' % (cov.loc[full].min().min() * 100))\n"
        "mix.loc[full].plot(kind='bar', stacked=True, figsize=(9, 4), ylabel='TWh'); plt.show()"))
    C.append(code(
        "# like-for-like: Jan..cut-off month of this year vs last year, hours reported in BOTH years\n"
        "def lfl(cols):\n"
        "    s = GH[cols].sum(axis=1, min_count=len(cols))\n"
        "    a = s[(s.index.year == Y) & (s.index.month <= END.month)]\n"
        "    b = s[(s.index.year == Y - 1) & (s.index.month <= END.month)]\n"
        "    A = pd.Series(a.values, index=a.index.strftime('%m-%d %H')); A = A[~A.index.duplicated()]\n"
        "    B = pd.Series(b.values, index=b.index.strftime('%m-%d %H')); B = B[~B.index.duplicated()]\n"
        "    j = pd.concat([A.rename('now'), B.rename('before')], axis=1)\n"
        "    both = j.dropna()\n"
        "    return pd.Series({'TWh now': both['now'].sum() / 1e6, 'TWh before': both['before'].sum() / 1e6,\n"
        "                      'change %': (both['now'].sum() / both['before'].sum() - 1) * 100, 'coverage %': len(both) / len(j) * 100})\n"
        "print(pd.DataFrame({k: lfl(c) for k, c in GRP.items()}).T.round(2))"))
    C.append(md(T("## §3 Price levels and seasonality", "## §3 Nivelul prețurilor și sezonalitatea")))
    C.append(code(
        "Z = ['RO', 'BG', 'HU', 'DE_LU']\n"
        "P[Z].rolling(7).mean().plot(figsize=(9, 4), ylabel='EUR/MWh'); plt.show()\n"
        "byyear = pd.DataFrame({z: P[z].groupby(P.index.year).mean() for z in Z}).round(1)\n"
        "vol = pd.DataFrame({z: PF[z].diff().groupby(PF.index.year).std() for z in Z}).round(1)\n"
        "print('mean by year\\n', byyear.loc[2018:], '\\nsd of daily changes\\n', vol.loc[2018:])"))
    C.append(code(
        "hh = H.copy(); hh['hour'] = hh.index.hour\n"
        "prof = pd.DataFrame({f'RO {y}': hh.loc[str(y)].groupby('hour')['RO'].mean() for y in [2019, 2025]})\n"
        "prof.plot(marker='o', figsize=(8, 3.5), ylabel='EUR/MWh'); plt.show()\n"
        "# weekly pattern: distance of each weekday from the mean of its own ISO week\n"
        "wk = P.loc['2023-01-01':, ['RO', 'DE_LU']].dropna()\n"
        "iso = wk.index.isocalendar(); key = iso['year'].astype(str) + '-' + iso['week'].astype(str)\n"
        "full_w = (key.map(key.value_counts()) == 7).values\n"
        "wk, key = wk[full_w], key[full_w]\n"
        "print((wk - wk.groupby(key.values).transform('mean')).groupby(wk.index.dayofweek).mean().round(1))"))
    C.append(md(T("## §4 Spikes and negative prices (hour-equivalents)", "## §4 Vîrfuri și prețuri negative (echivalent-ore)")))
    C.append(code(
        "hrs = X['mtu_minutes'] / 60\n"
        "neg_h = pd.DataFrame({z: ((X[z] < 0) & X[z].notna()).mul(hrs).groupby(X.index.year).sum() for z in Z})\n"
        "neg_n = pd.DataFrame({z: ((X[z] < 0) & X[z].notna()).groupby(X.index.year).sum() for z in Z})\n"
        "print('hour-equivalents\\n', neg_h.loc[2022:], '\\nnumber of negative MTUs\\n', neg_n.loc[2022:])\n\n"
        "def wquantile(x, w, q):\n"
        "    o = np.argsort(x); x, w = np.asarray(x)[o], np.asarray(w)[o]\n"
        "    return float(np.interp(q, (np.cumsum(w) - 0.5 * w) / w.sum(), x))\n\n"
        "s = X[['RO', 'mtu_minutes']].dropna()\n"
        "for y, g in s.groupby(s.index.year):\n"
        "    w = g['mtu_minutes'].values / 60\n"
        "    q1, q3 = wquantile(g['RO'].values, w, 0.25), wquantile(g['RO'].values, w, 0.75)\n"
        "    thr = q3 + 3 * (q3 - q1)\n"
        "    print(y, 'threshold %.0f EUR/MWh, spike hours %.2f' % (thr, ((g['RO'] > thr) * w).sum()))"))
    C.append(md(T("## §5 Transformations, fat tails, volatility clustering", "## §5 Transformări, cozi groase, volatilitate în grupuri")))
    C.append(code(
        "y = X.loc[str(Y), 'RO'].dropna()   # all 15-min prices of the current year\n"
        "med, mad = y.median(), stats.median_abs_deviation(y, scale='normal')\n"
        "z = np.arcsinh((y - med) / mad)\n"
        "print('share <= 0: %.2f%%' % ((y <= 0).mean() * 100), '| skew %.2f -> %.2f' % (stats.skew(y), stats.skew(z)),\n"
        "      '| excess kurtosis %.2f -> %.2f' % (stats.kurtosis(y), stats.kurtosis(z)))\n"
        "b = F['brent_usd_bbl'].dropna()\n"
        "# the continuous front-month switches contract on the first trading day of each month: drop those days\n"
        "ROLL = b.groupby(b.index.to_period('M')).head(1).index\n"
        "r = np.log(b).diff().dropna() * 100; r = r.drop(r.index.intersection(ROLL))\n"
        "print('Brent: excess kurtosis %.2f, JB %.0f' % (stats.kurtosis(r), stats.jarque_bera(r).statistic))\n"
        "print('Ljung-Box(10): returns %.1f, squared returns %.1f' % (acorr_ljungbox(r, lags=[10])['lb_stat'].iloc[0],\n"
        "                                                          acorr_ljungbox(r ** 2, lags=[10])['lb_stat'].iloc[0]))\n"
        "(r.rolling(21).std() * np.sqrt(252)).plot(figsize=(9, 3), ylabel='% p.a.'); plt.show()"))
    C.append(md(T("## §6 Stationarity, autocorrelation and the naive benchmark\n"
                  "The only simulated series of the lecture (white noise, AR(1), random walk) is generated here, to teach the concept.",
                  "## §6 Staționaritate, autocorelație și reperul naiv\n"
                  "Singurele serii simulate din curs (zgomot alb, AR(1), mers aleator) sînt generate aici, doar pentru a ilustra conceptul.")))
    C.append(code(
        "rng = np.random.default_rng(20261104); e = rng.standard_normal(500)\n"
        "ar = np.zeros(500)\n"
        "for t in range(1, 500):\n"
        "    ar[t] = 0.9 * ar[t - 1] + e[t]\n"
        "for name, s in [('white noise', e), ('AR(1)', ar), ('random walk', np.cumsum(e))]:\n"
        "    print(name, 'ACF lag 1 = %.2f, lag 10 = %.2f' % tuple(acf(s, nlags=10, fft=True)[[1, 10]]))\n"
        "sA = P['RO'].loc['2023-01-01':].dropna()\n"
        "print('RO daily price: ACF(1) %.3f, ACF(7) %.3f, PACF(7) %.3f' % (acf(sA, nlags=7, fft=True)[1], acf(sA, nlags=7, fft=True)[7],\n"
        "                                                            pacf(sA, nlags=7, method='ywm')[7]))"))
    C.append(code(
        "def naive_mae(z):\n"
        "    hz = H[z].dropna()\n"
        "    tab = pd.DataFrame({'p': hz.values, 'date': hz.index.tz_localize(None).normalize(), 'hour': hz.index.hour})\n"
        "    tab = tab.groupby(['date', 'hour'])['p'].mean().unstack('hour')\n"
        "    lag1 = tab.shift(1, freq='D').reindex(tab.index); lag7 = tab.shift(7, freq='D').reindex(tab.index)\n"
        "    naive = lag1.copy(); m = np.isin(tab.index.dayofweek, [0, 5, 6]); naive[m] = lag7[m]\n"
        "    out = {}\n"
        "    for k, f in [('naive', naive), ('d-1', lag1), ('d-7', lag7)]:\n"
        "        e = (tab - f).abs().stack()\n"
        "        out[k] = e.groupby(e.index.get_level_values(0).year).mean()\n"
        "    p = tab.stack(); out['mean price'] = p.groupby(p.index.get_level_values(0).year).mean()\n"
        "    return pd.DataFrame(out).loc[2019:].round(2)\n"
        "m = naive_mae('RO'); print(m)\n"
        "print('naive best in', int((m['naive'] < m[['d-1', 'd-7']].min(axis=1)).sum()), 'of', len(m), 'years')"))
    C.append(md(T("## §7 Unit-root (ADF) and stationarity (KPSS) tests", "## §7 Testele de rădăcină unitară (ADF) și de staționaritate (KPSS)")))
    C.append(code(
        "hydro_m = GH[['hydro_run_of_river', 'hydro_water_reservoir']].sum(axis=1, min_count=2).resample('MS').sum(min_count=600) / 1e6\n"
        "hydro_m.index = hydro_m.index.tz_localize(None); hydro_m = hydro_m.loc[:str(Y - 1)].dropna()\n"
        "series = {'RO level': P['RO'].dropna(), 'RO daily change': PF['RO'].diff().dropna(), 'DE-LU level': P['DE_LU'].dropna(),\n"
        "          'Brent log price': np.log(b), 'Brent log return': np.log(b).diff().dropna(),\n"
        "          'RO hydro, deseasonalised': hydro_m - hydro_m.groupby(hydro_m.index.month).transform('mean')}\n"
        "rows = {}\n"
        "for k, x in series.items():\n"
        "    a, kp = adfuller(x, regression='c', autolag='AIC'), kpss(x, regression='c', nlags='auto')\n"
        "    rows[k] = {'ADF': round(a[0], 2), 'ADF p': round(a[1], 4), 'KPSS': round(kp[0], 3), 'KPSS p': kp[1]}\n"
        "print(pd.DataFrame(rows).T)"))
    C.append(md(T("## §8 Decomposition: classical (2×12 moving average) and STL", "## §8 Descompunere: clasică (medie mobilă 2×12) și STL")))
    C.append(code(
        "lm = GH['load'].resample('MS').mean(); lm.index = lm.index.tz_localize(None)\n"
        "lm = (lm.loc['2016-01-01':f'{Y - 1}-12-01'] / 1000).asfreq('MS')\n"
        "w = np.r_[1 / 24, np.repeat(1 / 12, 11), 1 / 24]\n"
        "cma = lm.rolling(13, center=True).apply(lambda v: float(np.dot(v, w)), raw=True)\n"
        "d = (lm - cma).groupby(lm.index.month).mean(); print('seasonal indices (GW)\\n', (d - d.mean()).round(3))\n"
        "stl = STL(lm, period=12, seasonal=13, robust=True).fit(); stl.plot(); plt.show()"))
    C.append(md(T("## §9 Exponential smoothing", "## §9 Netezirea exponențială")))
    C.append(code(
        "bs = b.loc['2024-01-01':]\n"
        "alpha = 1 - 2 ** (-1 / 10)\n"
        "ses = SimpleExpSmoothing(bs.values, initialization_method='estimated').fit()\n"
        "print('alpha for a 10-day half-life %.3f; optimal SES alpha %.3f' % (alpha, ses.params['smoothing_level']))\n"
        "pd.DataFrame({'Brent': bs, 'SMA 20': bs.rolling(20).mean(), 'EWMA': bs.ewm(alpha=alpha, adjust=False).mean()}).plot(figsize=(9, 3.5)); plt.show()"))
    C.append(md(T("## §10 Case studies\n### §10a Wet 2023, dry 2025", "## §10 Studii de caz\n### §10a 2023 ploios, 2025 secetos")))
    C.append(code(
        "print('hydro TWh: 2023 %.2f, 2025 %.2f, change %.1f%%' % (mix.loc[2023, 'Hydro'], mix.loc[2025, 'Hydro'],\n"
        "      (mix.loc[2025, 'Hydro'] / mix.loc[2023, 'Hydro'] - 1) * 100))\n"
        "dfm = pd.concat([hydro_m.rename('hydro'), P['RO'].resample('MS').mean().rename('price'),\n"
        "                 TTF['ttf_eur_mwh'].rename('ttf')], axis=1).dropna()\n"
        "ols = sm.OLS(dfm['price'], sm.add_constant(dfm[['hydro', 'ttf']])).fit(cov_type='HAC', cov_kwds={'maxlags': 6})\n"
        "print(ols.summary().tables[1])"))
    C.append(md(T("### §10b The June 2025 oil shock", "### §10b Șocul petrolier din iunie 2025")))
    C.append(code(
        "w = b.loc['2025-06-10':'2025-06-26']; print(w)\n"
        "print('12->13 Jun: %+.1f%%; peak -> 24 Jun: %+.1f%%' % ((b['2025-06-13'] / b['2025-06-12'] - 1) * 100,\n"
        "      (b['2025-06-24'] / b.loc['2025-06-13':'2025-06-23'].max() - 1) * 100))"))
    C.append(md(T("### §10c Regional price separation, summer 2024", "### §10c Separarea regională a prețurilor, vara 2024")))
    C.append(code(
        "print(P.loc['2024-07', Z].mean().round(2))\n"
        "hj = H.loc['2024-07-01':'2024-07-31', Z].dropna()\n"
        "print('share of July hours with equal prices: RO-BG %.1f%%, RO-HU %.1f%%, RO-DE %.1f%%' % tuple(\n"
        "      (np.abs(hj['RO'] - hj[z]) < 0.01).mean() * 100 for z in ['BG', 'HU', 'DE_LU']))\n"
        "H.loc['2024-07-16', Z].plot(figsize=(8, 3.5), ylabel='EUR/MWh'); plt.show()"))
    C.append(md(T("### §10d Negative prices and solar: a descriptive logit (realised data, not a bidding model)",
                  "### §10d Prețuri negative și solar: un logit descriptiv (date realizate, nu un model de licitare)")))
    C.append(code(
        "nd = ((X['RO'] < 0) & X['RO'].notna()).groupby(X.index.normalize().tz_localize(None)).max().astype(float)\n"
        "jj = pd.concat([nd.rename('neg'), (G['solar'] / 1000).rename('solar'), (G['wind_onshore'] / 1000).rename('wind'),\n"
        "                ((G['hydro_run_of_river'] + G['hydro_water_reservoir']) / 1000).rename('hydro'),\n"
        "                (G['load'] / 1000).rename('load')], axis=1).loc['2024-01-01':].dropna()\n"
        "jj['residual_load'] = jj['load'] - jj['solar'] - jj['wind']   # demand left after wind and solar (GW)\n"
        "jj['weekend'] = (jj.index.dayofweek >= 5).astype(float)\n"
        "for yy in sorted(set(jj.index.year))[1:]:\n"
        "    jj[f'y{yy}'] = (jj.index.year == yy).astype(float)\n"
        "X_ = sm.add_constant(jj[['residual_load', 'hydro', 'weekend'] + [c for c in jj.columns if c.startswith('y')]])\n"
        "fit = sm.Logit(jj['neg'], X_).fit(disp=0)\n"
        "print(fit.summary().tables[1]); print('odds ratios:', np.exp(fit.params).round(2).to_dict())"))
    C.append(md(T("### §10e The current year so far", "### §10e Anul curent pînă acum")))
    C.append(code(
        "cur = P.loc[str(Y), Z].mean(); prev = P.loc[f'{Y - 1}-01-01':f'{Y - 1}-{END:%m-%d}', Z].mean()\n"
        "print(pd.DataFrame({'Jan..cut-off ' + str(Y - 1): prev, 'Jan..cut-off ' + str(Y): cur, 'change %': (cur / prev - 1) * 100}).round(1))\n"
        "print(pd.DataFrame({k: lfl(GRP[k]) for k in ['Nuclear', 'Hydro', 'Solar']}).T.round(2))\n"
        "print('nuclear days not reported this year:', G.loc[str(Y), 'nuclear'].isna().sum(),\n"
        "      '| days at 0 MW in May:', (G.loc[f'{Y}-05', 'nuclear'] < 1).sum())\n"
        "hyd = (G['hydro_run_of_river'] + G['hydro_water_reservoir']).resample('MS').mean()\n"
        "print(pd.DataFrame({str(Y - 1): hyd.loc[str(Y - 1)].values[:END.month], str(Y): hyd.loc[str(Y)].values}, index=range(1, END.month + 1)).round(0))\n"
        "mar = b.loc[f'{Y}-03']\n"
        "print('Brent, May contract within March: %.2f -> %.2f (%+.1f%%); 1 April roll: %+.1f%%' % (mar.iloc[0], mar.iloc[-1],\n"
        "      (mar.iloc[-1] / mar.iloc[0] - 1) * 100, (b.loc[f'{Y}-04'].iloc[0] / mar.iloc[-1] - 1) * 100))"))
    C.append(code(
        "# extremes of the current year: RO daily base price and Brent close\n"
        "ro = P.loc[str(Y), 'RO'].dropna(); bb = b.loc[str(Y)].dropna()\n"
        "print('RO max %.2f on %s, min %.2f on %s; Brent max %.2f on %s' % (ro.max(), ro.idxmax().date(), ro.min(), ro.idxmin().date(),\n"
        "      bb.max(), bb.idxmax().date()))\n"
        "fig, axs = plt.subplots(1, 2, figsize=(10, 3))\n"
        "axs[0].plot(ro); axs[0].plot([ro.idxmax(), ro.idxmin()], [ro.max(), ro.min()], 'ro'); axs[0].set_title('RO, EUR/MWh')\n"
        "axs[1].plot(bb, color='k'); axs[1].plot([bb.idxmax()], [bb.max()], 'ro'); axs[1].set_title('Brent, USD/bbl'); plt.show()"))
    C.append(md(T("### §10f Romania, Bulgaria and batteries\nLocal time (EET, Bucharest = Sofia); evening = intervals 19:00--22:00, April--September.",
                  "### §10f România, Bulgaria și bateriile\nOra locală (EET, București = Sofia); seara = intervalele 19:00--22:00, aprilie--septembrie.")))
    C.append(code(
        "XL = X.copy(); XL.index = XL.index.tz_convert('Europe/Bucharest'); wl = XL['mtu_minutes'] / 60\n"
        "def wmean(z, m):\n"
        "    v, ww = XL.loc[m, z], wl[m]; ok = v.notna(); return float((v[ok] * ww[ok]).sum() / ww[ok].sum())\n"
        "for yy in [2024, 2025, Y]:\n"
        "    base = (XL.index.year == yy) & (XL.index.month >= 4) & (XL.index.month <= 9)\n"
        "    ev = base & (XL.index.hour >= 19) & (XL.index.hour <= 21)\n"
        "    print(yy, 'evening RO %.1f vs BG %.1f EUR/MWh' % (wmean('RO', ev), wmean('BG', ev)))\n"
        "    mid = base & (XL.index.hour >= 11) & (XL.index.hour <= 14)\n"
        "    print(yy, '   midday RO %.1f vs BG %.1f EUR/MWh' % (wmean('RO', mid), wmean('BG', mid)))\n"
        "bat = BGH[['battery', 'battery_consumption']].dropna(how='all')\n"
        "bat.index = bat.index.tz_convert('Europe/Bucharest')\n"
        "print('Bulgarian battery data start (local date):', bat.index.min().date())\n"
        "print(bat.groupby(bat.index.tz_localize(None).to_period('M')).mean().round(0))"))
    return C


def build(lang):
    nb = nbformat.v4.new_notebook()
    nb.cells = cells(lang)
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    name = "L1_notebook.ipynb" if lang == "en" else "L1_notebook_ro.ipynb"
    add_colab_cell(nb, lang)
    ExecutePreprocessor(timeout=900, kernel_name="python3").preprocess(nb, {"metadata": {"path": NBDIR}})
    os.makedirs(NBDIR, exist_ok=True)
    with open(os.path.join(NBDIR, name), "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print("executed and wrote", name)


if __name__ == "__main__":
    for lang in (sys.argv[1:] or ["en", "ro"]):
        build(lang)
