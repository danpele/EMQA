"""
make_quantlets_L3.py -- one Quantlet per chart of Lecture 3 "Volatility of energy prices" (EMQA)
=================================================================================================
Writes Quantlets/L3/EMQA_L3_<chart>/ (Metainfo.txt, executed notebook, <chart>.png) for every chart shown in lecture3.pdf,
with the helper lectures/common/emqa_quantlet.py. Each notebook is self-contained (no import of the lecture modules),
reads the course data (local data/clean or the public repository), prints the numbers shown on the slide and draws the
chart with the English labels.

Heavy step: the rolling one-day-ahead GARCH-t forecasts of the test year (365 re-estimations) are computed here once and
saved, small, inside the two Quantlets that need them (fc_test, case_band); their notebooks load the file and keep the
full recomputation under RUN_ALL = False.

After execution, every printed number tagged [key] is compared with lectures/L3/L3_numbers.json; a mismatch is reported.
Run from the repository root:  python3 lectures/L3/make_quantlets_L3.py  [chart ...]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_quantlet import QL_ROOT, Quantlet  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
with open(os.path.join(HERE, "L3_numbers.json")) as fh:
    N = json.load(fh)
PERIOD = f"{N['data']['start']} to {N['data']['end']}"
TEST = f"{N['design']['test_start']} to {N['design']['test_end']}"
ROLL_FILE = "garch_t_rolling_eur.csv"

# ======================================================================================================================
# Code shared by the notebooks (copied into each notebook that needs it)
# ======================================================================================================================
SETUP = r'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# course chart style: transparent background, no gridlines, legend at the bottom outside the axes
plt.rcParams.update({
    'figure.facecolor': 'none', 'axes.facecolor': 'none', 'savefig.transparent': True,
    'axes.grid': False, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.edgecolor': '#222222', 'axes.labelcolor': '#222222', 'xtick.color': '#222222', 'ytick.color': '#222222',
    'text.color': '#222222', 'font.size': 11, 'axes.titlesize': 11.5, 'axes.labelsize': 11,
    'legend.fontsize': 10.5, 'legend.frameon': False, 'lines.linewidth': 1.4})
PAL = {'RO': '#2a78d6', 'DE_LU': '#eb6834', 'HU': '#1baf7a', 'BG': '#eda100',
       'c5': '#e87ba4', 'c6': '#008300', 'c7': '#6250d6', 'c8': '#e34948'}
C_PCT, C_EUR = PAL['RO'], PAL['c7']          # percent changes, EUR/MWh changes


def legend_bottom(fig, handles=None, labels=None, ncol=4, y=0.0):
    # legend centred under the axes, outside the plotting area
    if handles is None:
        handles, labels = [], []
        for ax in fig.axes:
            for h, l in zip(*ax.get_legend_handles_labels()):
                if l not in labels:
                    handles.append(h)
                    labels.append(l)
    fig.legend(handles, labels, loc='lower center', ncol=ncol, bbox_to_anchor=(0.5, y), frameon=False,
               handlelength=2.0, columnspacing=1.2)


def slide(label, key, x, k=None):
    # prints a number shown on the slide; [key] = its name in lectures/L3/L3_numbers.json
    if k is not None:
        x = round(float(x), k)
    print(f'{label:<58s} {x}   [{key}]')'''

ARCH = r'''try:
    import arch
except ImportError:          # Google Colab: install the arch package once
    import subprocess, sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'arch'])
from arch import arch_model


def fit(e, vol='GARCH', o=0, dist='t'):
    # zero-mean GARCH(1,1) (o=0) or GJR-GARCH(1,1,1) (o=1), Student-t shocks by default
    return arch_model(np.asarray(e, float), mean='Zero', vol=vol, p=1, o=o, q=1, dist=dist,
                      rescale=False).fit(disp='off', show_warning=False)'''

PRICES = r'''# Romanian daily base price (mean of all MTUs of the CET/CEST delivery day), EUR/MWh
PD = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', usecols=['date_cet', 'RO'], parse_dates=['date_cet']).set_index('date_cet')
# cut-off = last complete month; panel from 2019-01-01, on the full calendar
_last = PD['RO'].dropna().index.max()
END = pd.Timestamp(((_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())
START = pd.Timestamp('2019-01-01')
CAL = pd.date_range(START, END, freq='D')
P = PD['RO'].reindex(CAL)
print('Romania, daily base price:', START.date(), 'to', END.date(), '|', len(CAL), 'days, missing:', int(P.isna().sum()))'''

CHANGES = r'''# daily changes on the full calendar: percent (log) and EUR/MWh
r = 100 * np.log(P.where(P > 0)).diff()      # r_t = 100 ln(P_t / P_{t-1}); missing if a price is <= 0
u = P.diff()                                  # Delta P_t = P_t - P_{t-1}, EUR/MWh'''

MEAN = r'''import statsmodels.api as sm


def mean_design(y, lags=7):
    # constant + AR(1..7) + six day-of-week dummies (Monday = base)
    X = pd.DataFrame({f'L{k}': y.shift(k) for k in range(1, lags + 1)}, index=y.index)
    for j in range(1, 7):
        X[f'D{j}'] = (y.index.dayofweek == j).astype(float)
    X.insert(0, 'const', 1.0)
    return X


def mean_fit(y, lags=7):
    # OLS mean equation; returns (residuals = shocks, fitted model)
    X = mean_design(y, lags)
    df = pd.concat([y.rename('y'), X], axis=1).dropna()
    m = sm.OLS(df['y'], df.drop(columns='y')).fit()
    return m.resid, m


E_PCT, M_PCT = mean_fit(r)       # shocks epsilon_t, percent
E_EUR, M_EUR = mean_fit(u)       # shocks u_t, EUR/MWh
print('shocks:', E_PCT.index[0].date(), 'to', E_PCT.index[-1].date(), '|', len(E_PCT), 'days')'''

MEAN_PCT = MEAN.replace("E_EUR, M_EUR = mean_fit(u)       # shocks u_t, EUR/MWh\n", "")

BRENT = r'''def mkt_returns(px, drop_roll=False, vol=None):
    # 100 x log returns on trading days; drop_roll removes the first trading day of each month (futures roll);
    # vol: keep only days with a positive traded volume
    px = px.dropna()
    if vol is not None:
        px = px[vol.reindex(px.index).fillna(0) > 0]
    r_ = 100 * np.log(px).diff().dropna()
    if drop_roll:
        first = r_.index.to_series().groupby(r_.index.to_period('M')).transform('min') == r_.index
        r_ = r_[~first]
    return r_


FU = pd.read_csv(DATA + 'fuels_daily.csv', usecols=['date', 'brent_usd_bbl'], parse_dates=['date']).set_index('date')
BRENT = mkt_returns(FU['brent_usd_bbl'].loc[str(START - pd.Timedelta(days=10)):str(END)], drop_roll=True).loc[START:END]
print('Brent BZ=F returns:', BRENT.index[0].date(), 'to', BRENT.index[-1].date(), '|', len(BRENT), 'trading days (roll days dropped)')'''

HOURLY = r'''# hourly prices of Romania (15-min MTUs averaged to the hour from 1 Oct 2025), CET/CEST clock
HP = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', usecols=['timestamp_utc', 'RO'], parse_dates=['timestamp_utc']).set_index('timestamp_utc')['RO']
HP.index = HP.index.tz_convert('Europe/Brussels')
HP = HP.dropna().loc[str(START.date()):str(END.date())]
# intraday variation RV_d = sqrt(sum_h (P_{d,h} - P_{d,h-1})^2), within the delivery day
_h = pd.DataFrame({'p': HP.values, 'day': HP.index.tz_localize(None).normalize()})
_h['dp'] = _h.groupby('day')['p'].diff()
_gh = _h.groupby('day')
RV = pd.DataFrame({'rv': np.sqrt(_gh['dp'].apply(lambda x: (x ** 2).sum(min_count=1))), 'lvl': _gh['p'].mean()}).reindex(CAL)
print('days with RV:', int(RV['rv'].notna().sum()), 'of', len(CAL))'''

YFMT = r'''import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def yfmt(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))


def mfmt(ax, step=1):
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=step))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: MON[mdates.num2date(v).month - 1] +
                                               (f'\n{mdates.num2date(v).year}' if mdates.num2date(v).month == 1 else '')))'''

CRISIS = "CRISIS = (pd.Timestamp('2021-09-01'), pd.Timestamp('2022-12-31'))   # energy crisis, shaded"

# one-day-ahead forecasts of the test year (identical to lectures/L3/analysis_L3.py, section 8, for the models charted)
ONE_DAY = r'''def one_day(y, t):
    # forecasts for day t from data up to t-1: mean equation re-estimated by OLS, then GARCH(1,1)-t on its residuals
    X = mean_design(y)
    df = pd.concat([y.rename('y'), X], axis=1)
    tr = df.loc[:t - pd.Timedelta(days=1)].dropna()
    Xt, yt = tr.drop(columns='y').values, tr['y'].values
    b = np.linalg.lstsq(Xt, yt, rcond=None)[0]
    e_tr = yt - Xt @ b
    yhat = float(df.loc[t].drop('y').values @ b)
    res = fit(e_tr)
    return {'y': float(df.loc[t, 'y']), 'yhat': yhat, 'e': float(df.loc[t, 'y']) - yhat,
            'hist30': float(np.mean(e_tr[-30:] ** 2)),                                  # 30-day historical variance
            'garch': float(res.forecast(horizon=1, reindex=False).variance.values[-1, 0]),  # GARCH-t variance forecast
            'nu': float(res.params['nu'])}'''


def roll_cell(chart):
    return (r'''RUN_ALL = False    # True: recompute the 365 rolling GARCH-t forecasts (well under a minute on Colab); False: load them
TDAYS = pd.date_range(END - pd.Timedelta(days=364), END, freq='D')      # test year
if RUN_ALL:
''' + "\n".join("    " + ln if ln else "" for ln in (MEAN.split("\n") + [""] + ARCH.split("\n") + [""] + ONE_DAY.split("\n"))) + r'''

    R = pd.DataFrame([one_day(u.loc[START:END], t) for t in TDAYS], index=TDAYS)
else:
    # saved by lectures/L3/make_quantlets_L3.py with the code above
    R = pd.read_csv(REPO + 'Quantlets/L3/EMQA_L3_''' + chart + "/" + ROLL_FILE + r'''', index_col=0, parse_dates=True)
    assert R.index.equals(TDAYS), 'saved forecasts do not match the test year of the data'
print('test year:', TDAYS[0].date(), 'to', TDAYS[-1].date(), '|', len(R), 'one-day-ahead forecasts')''')


# ======================================================================================================================
# Charts
# ======================================================================================================================
DATA_PRICE = ("power_da_prices_daily_cet.csv: daily base day-ahead price of Romania (OPCOM, via energy-charts.info / ENTSO-E), "
              "EUR/MWh, mean of all market time units of the CET/CEST delivery day")
KW_BASE = "energy markets, electricity prices, Romania, day-ahead market, OPCOM, volatility"
Q = {}


def add(chart, description, keywords, datafile, cells):
    Q[chart] = (description, keywords, datafile, cells)


# 1 ------------------------------------------------------------------------------------------------------------------
add("returns_ro",
    f"Romanian daily base day-ahead price and its daily log change r_t = 100 ln(P_t/P_t-1), {PERIOD} (CET delivery days), "
    "with the energy crisis (Sep 2021 to Dec 2022) shaded: calm and turbulent stretches alternate (volatility clustering).",
    KW_BASE + ", log returns, volatility clustering, time series plot, energy crisis",
    DATA_PRICE,
    [("md", "## Daily price and daily change\n\nThe daily change in percent is $r_t = 100\\ln(P_t/P_{t-1})$, on the full calendar "
            "(every day has an auction). Large changes come in clusters."),
     ("code", PRICES), ("code", CHANGES),
     ("md", "### Numbers on the slide"),
     ("code", r'''rr = r.dropna()
slide('daily changes', 'ret.n', int(len(rr)))
slide('largest rise, %', 'ret.max', rr.max(), 1)
slide('  on', 'ret.max_date', str(rr.idxmax().date()))
slide('largest fall, %', 'ret.min', rr.min(), 1)
slide('  on', 'ret.min_date', str(rr.idxmin().date()))
slide('days with |r_t| > 50%', 'ret.n_abs50', int((rr.abs() > 50).sum()))'''),
     ("md", "### Chart"),
     ("code", YFMT + "\nfrom matplotlib.patches import Patch\n" + CRISIS + r'''

from matplotlib.ticker import MaxNLocator
fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.1), sharex=True, gridspec_kw={'height_ratios': [1, 1.2]})
axs[0].plot(P.index, P.values, color=PAL['RO'], lw=0.6)
axs[0].set_ylabel('EUR/MWh', fontsize=9.5)
axs[1].plot(rr.index, rr.values, color=C_PCT, lw=0.35)
axs[1].set_ylabel('change, %', fontsize=9.5)
for ax in axs:
    ax.axvspan(*CRISIS, color=PAL['c8'], alpha=0.08, lw=0)
yfmt(axs[1])
legend_bottom(fig, handles=[plt.Line2D([], [], color=PAL['RO'], lw=1.2), plt.Line2D([], [], color=C_PCT, lw=0.6),
                            Patch(color=PAL['c8'], alpha=0.15)],
              labels=['daily base price', 'change $r_t$ (log, %)', 'crisis: Sep 2021–Dec 2022'], ncol=3)
for ax in axs:
    ax.yaxis.set_major_locator(MaxNLocator(3))
fig.tight_layout(rect=(0, 0.12, 1, 1))
plt.savefig('returns_ro.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 2 ------------------------------------------------------------------------------------------------------------------
add("dow_effect",
    f"Weekly calendar in the Romanian daily price change, {PERIOD}: mean log change by weekday (left) and the standard deviation "
    "of the daily change before and after the mean equation (constant + AR(1..7) + day-of-week dummies, OLS), which removes about half of the variance.",
    KW_BASE + ", day-of-week effect, seasonality, autoregression, OLS, mean equation",
    DATA_PRICE,
    [("md", "## The weekly calendar\n\nMean equation, estimated by ordinary least squares (OLS):\n\n"
            "$$r_t=c+\\sum_{k=1}^{7}\\phi_k r_{t-k}+\\sum_{j=2}^{7}\\delta_j D_{j,t}+\\varepsilon_t$$\n\n"
            "$D_{j,t}=1$ if day $t$ is weekday $j$. The residuals $\\varepsilon_t$ are the shocks modelled in the rest of the lecture."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN_PCT),
     ("md", "### Numbers on the slide"),
     ("code", r'''rr = r.dropna()
DOW = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
dow = rr.groupby(rr.index.dayofweek).mean()
for k, v in dow.items():
    slide(f'mean change on {DOW[k]}, %', f'mean.dow_pct.{DOW[k]}', v, 2)
sd_raw, sd_res = rr.loc[E_PCT.index].std(), E_PCT.std()
slide('R^2 of the mean equation', 'mean.r2_pct', M_PCT.rsquared, 3)
slide('std. dev. of the raw change, %', 'mean.sd_raw', sd_raw, 2)
slide('std. dev. after the mean equation, %', 'mean.sd_res', sd_res, 2)'''),
     ("md", "### Chart"),
     ("code", r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0), gridspec_kw={'width_ratios': [1.5, 1]})
axs[0].bar(range(7), dow.values, color=[PAL['c8'] if v < 0 else PAL['RO'] for v in dow.values], width=0.65)
axs[0].axhline(0, color='#222222', lw=0.6)
axs[0].set_xticks(range(7))
axs[0].set_xticklabels(DOW, fontsize=9)
axs[0].set_ylabel('mean change, %', fontsize=9)
axs[1].bar([0, 1], [round(sd_raw, 2), round(sd_res, 2)], color=['#9a9a9a', C_PCT], width=0.55)
axs[1].set_xticks([0, 1])
axs[1].set_xticklabels(['raw change', 'after the mean\nequation'], fontsize=9)
axs[1].set_ylabel('std. dev., %', fontsize=9)
fig.tight_layout(rect=(0, 0.02, 1, 1))
plt.savefig('dow_effect.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 3 ------------------------------------------------------------------------------------------------------------------
add("vol_units",
    f"Standard deviation of the daily shocks of the Romanian base price by year, {PERIOD}, in percent (left) and in EUR/MWh (right): "
    "in 2022 the percent volatility equals that of 2019, while the EUR/MWh volatility is about four times higher, because it follows the price level.",
    KW_BASE + ", standard deviation, volatility units, energy crisis, price level",
    DATA_PRICE,
    [("md", "## Volatility in two units\n\nShocks = residuals of the mean equation (constant + AR(1..7) + day-of-week dummies) "
            "for the percent change $r_t$ ($\\varepsilon_t$) and for the change in EUR/MWh $\\Delta P_t$ ($u_t$). Yearly standard deviations."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN),
     ("md", "### Numbers on the slide"),
     ("code", r'''YEARS = list(range(START.year, END.year + 1))
sd_pct = {y: round(E_PCT[E_PCT.index.year == y].std(), 1) for y in YEARS}
sd_eur = {y: round(E_EUR[E_EUR.index.year == y].std(), 1) for y in YEARS}
lvl = {y: round(P[P.index.year == y].mean(), 1) for y in YEARS}
print(pd.DataFrame({'sd %': sd_pct, 'sd EUR/MWh': sd_eur, 'mean price': lvl}))
for y in [2019, 2022]:
    slide(f'std. dev. of the % shocks, {y}', f'voly.RO_pct_d.{y}', sd_pct[y])
    slide(f'std. dev. of the EUR/MWh shocks, {y}', f'voly.RO_eur.{y}', sd_eur[y])
    slide(f'mean price {y}, EUR/MWh', f'voly.RO_lvl.{y}', lvl[y])
slide('ratio 2022 / 2019, percent', 'voly.ratio_pct_22_19', sd_pct[2022] / sd_pct[2019], 2)
slide('ratio 2022 / 2019, EUR/MWh', 'voly.ratio_eur_22_19', sd_eur[2022] / sd_eur[2019], 1)'''),
     ("md", "### Chart"),
     ("code", r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1))
x = np.arange(len(YEARS))
axs[0].bar(x, [sd_pct[y] for y in YEARS], color=C_PCT, width=0.65)
axs[0].set_ylabel('%', fontsize=9.5)
axs[1].bar(x, [sd_eur[y] for y in YEARS], color=C_EUR, width=0.65)
axs[1].set_ylabel('EUR/MWh', fontsize=9.5)
for ax in axs:
    ax.set_xticks(x)
    ax.set_xticklabels([f"'{str(y)[2:]}" for y in YEARS], fontsize=9)
axs[0].set_title(r'std. dev. of the % shocks $\varepsilon_t$', fontsize=9.5)
axs[1].set_title(r'std. dev. of the EUR/MWh shocks $u_t$', fontsize=9.5)
fig.tight_layout(rect=(0, 0.02, 1, 1))
plt.savefig('vol_units.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 4 ------------------------------------------------------------------------------------------------------------------
add("acf_clust",
    f"Autocorrelation function (lags 1-30) of the daily shocks of the Romanian base price and of their squares, {PERIOD}: "
    "the shocks are almost uncorrelated, their squares are not (volatility clustering); Ljung-Box and ARCH-LM tests.",
    KW_BASE + ", autocorrelation, ACF, Ljung-Box test, ARCH-LM test, volatility clustering, stylised facts",
    DATA_PRICE,
    [("md", "## The sign is unpredictable, the size is not\n\nLjung–Box statistic $Q(10)=T(T+2)\\sum_{k\\le10}\\hat\\rho_k^2/(T-k)$ "
            "on the shocks $\\varepsilon_t$ and on $\\varepsilon_t^2$; Engle's ARCH-LM test with 10 lags."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN_PCT),
     ("md", "### Numbers on the slide"),
     ("code", r'''from statsmodels.tsa.stattools import acf
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
lb_e, lb_e2 = acorr_ljungbox(E_PCT, [10]), acorr_ljungbox(E_PCT ** 2, [10])
lm = het_arch(E_PCT, nlags=10)
slide('Ljung-Box Q(10), shocks', 'facts.lb_e', lb_e['lb_stat'].iloc[0], 1)
slide('  p-value', 'facts.lb_e_p', lb_e['lb_pvalue'].iloc[0], 3)
slide('Ljung-Box Q(10), squared shocks', 'facts.lb_e2', lb_e2['lb_stat'].iloc[0], 1)
slide('ARCH-LM, 10 lags', 'facts.lm', lm[0], 1)
print('ARCH-LM p-value:', lm[1])'''),
     ("md", "### Chart"),
     ("code", r'''from matplotlib.patches import Patch
fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.0), sharey=True)
K = 30
ci = 1.96 / np.sqrt(len(E_PCT))
for ax, s_, ttl in [(axs[0], E_PCT, r'shocks $\varepsilon_t$'), (axs[1], E_PCT ** 2, r'squared shocks $\varepsilon_t^2$')]:
    ax.bar(range(1, K + 1), acf(s_, nlags=K)[1:], color=C_PCT, width=0.6)
    ax.axhspan(-ci, ci, color='#9a9a9a', alpha=0.25, lw=0)
    ax.axhline(0, color='#222222', lw=0.5)
    ax.set_title(ttl, fontsize=10)
    ax.set_xlabel('lag (days)', fontsize=9)
axs[0].set_ylabel('autocorrelation', fontsize=9)
legend_bottom(fig, handles=[Patch(color='#9a9a9a', alpha=0.4)], labels=['95% band if no autocorrelation'], ncol=1)
fig.tight_layout(rect=(0, 0.12, 1, 1))
plt.savefig('acf_clust.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 5 ------------------------------------------------------------------------------------------------------------------
add("tails",
    f"Density (log scale) of the GARCH(1,1)-t standardised daily shocks of the Romanian base price, {PERIOD}, against the normal "
    "and the fitted Student-t density: extreme days are far more frequent than the normal law allows (fat tails).",
    KW_BASE + ", fat tails, kurtosis, Student-t distribution, GARCH, standardised residuals",
    DATA_PRICE,
    [("md", "## Fat tails\n\nGARCH(1,1) with Student-$t$ shocks on the percent shocks $\\varepsilon_t$: "
            "$\\varepsilon_t=\\sigma_t z_t$, $\\sigma_t^2=\\omega+\\alpha\\varepsilon_{t-1}^2+\\beta\\sigma_{t-1}^2$. "
            "The histogram shows the standardised shocks $z_t=\\varepsilon_t/\\hat\\sigma_t$."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN_PCT), ("code", ARCH),
     ("md", "### Numbers on the slide"),
     ("code", r'''from scipy import stats
res = fit(E_PCT)
nu = round(float(res.params['nu']), 4)
z = (E_PCT - E_PCT.mean()) / E_PCT.std()
slide('excess kurtosis of the shocks', 'facts.kurt', E_PCT.kurt(), 2)
slide('skewness of the shocks', 'facts.skew', E_PCT.skew(), 2)
slide('shocks beyond 4 standard deviations', 'facts.n_4sd', int((z.abs() > 4).sum()))
slide('  expected under normality', 'facts.n_4sd_norm', len(z) * 2 * stats.norm.sf(4), 2)
slide('Student-t degrees of freedom nu', 'garch.pct.garch_t.nu', nu)'''),
     ("md", "### Chart"),
     ("code", r'''zz = res.std_resid
fig, ax = plt.subplots(figsize=(6.4, 2.0))
bins = np.linspace(-8, 8, 65)
hcount, edges = np.histogram(np.clip(zz, -8, 8), bins=bins, density=True)
ax.bar(0.5 * (edges[1:] + edges[:-1]), hcount, width=edges[1] - edges[0], color=C_PCT, alpha=0.55, lw=0,
       label='standardised shocks, Romania')
xs = np.linspace(-8, 8, 400)
ax.plot(xs, stats.norm.pdf(xs), color='#222222', lw=1.0, ls='--', label='normal')
sc = np.sqrt((nu - 2) / nu)          # unit-variance Student-t
ax.plot(xs, stats.t.pdf(xs / sc, nu) / sc, color=PAL['DE_LU'], lw=1.2, label=f'Student-t, $\\nu$ = {nu:.1f}')
ax.set_yscale('log')
ax.set_ylim(1e-4, 1)
ax.set_xlabel('standardised shock $z_t$', fontsize=9)
ax.set_ylabel('density (log)', fontsize=9)
legend_bottom(fig, ncol=3)
fig.tight_layout(rect=(0, 0.17, 1, 1))
plt.savefig('tails.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 6 ------------------------------------------------------------------------------------------------------------------
add("cond_vol",
    f"GARCH(1,1)-t conditional volatility of the daily shocks of the Romanian base price, {PERIOD}, in percent and in EUR/MWh: "
    "short spikes in percent, a long hump in EUR/MWh during the energy crisis.",
    KW_BASE + ", GARCH, conditional volatility, Student-t, energy crisis",
    DATA_PRICE,
    [("md", "## GARCH conditional volatility in two units\n\n$\\sigma_t^2=\\omega+\\alpha\\varepsilon_{t-1}^2+\\beta\\sigma_{t-1}^2$, "
            "Student-$t$ shocks, estimated by maximum likelihood on the percent shocks $\\varepsilon_t$ and on the EUR/MWh shocks $u_t$."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN), ("code", ARCH),
     ("md", "### Numbers on the slide"),
     ("code", r'''CV = {'pct': pd.Series(fit(E_PCT).conditional_volatility, index=E_PCT.index),
      'eur': pd.Series(fit(E_EUR).conditional_volatility, index=E_EUR.index)}
slide('peak sigma, % per day', 'garch.cv.pct_max', CV['pct'].max(), 1)
slide('  on', 'garch.cv.pct_max_date', str(CV['pct'].idxmax().date()))
slide('peak sigma, EUR/MWh', 'garch.cv.eur_max', CV['eur'].max(), 1)
slide('  on', 'garch.cv.eur_max_date', str(CV['eur'].idxmax().date()))
slide('minimum sigma, EUR/MWh', 'garch.cv.eur_min', CV['eur'].min(), 1)
slide('  on', 'garch.cv.eur_min_date', str(CV['eur'].idxmin().date()))
slide('sigma at the cut-off, EUR/MWh', 'garch.cv.eur_last', CV['eur'].iloc[-1], 1)'''),
     ("md", "### Chart"),
     ("code", YFMT + "\nfrom matplotlib.patches import Patch\n" + CRISIS + r'''

from matplotlib.ticker import MaxNLocator
fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.1), sharex=True)
axs[0].plot(CV['pct'].index, CV['pct'].values, color=C_PCT, lw=0.6)
axs[0].set_ylabel('%', fontsize=9.5)
axs[1].plot(CV['eur'].index, CV['eur'].values, color=C_EUR, lw=0.6)
axs[1].set_ylabel('EUR/MWh', fontsize=9.5)
for ax in axs:
    ax.axvspan(*CRISIS, color=PAL['c8'], alpha=0.08, lw=0)
yfmt(axs[1])
legend_bottom(fig, handles=[plt.Line2D([], [], color=C_PCT), plt.Line2D([], [], color=C_EUR), Patch(color=PAL['c8'], alpha=0.15)],
              labels=[r'GARCH-t $\hat\sigma_t$, %', r'GARCH-t $\hat\sigma_t$, EUR/MWh', 'energy crisis'], ncol=3)
for ax in axs:
    ax.yaxis.set_major_locator(MaxNLocator(3))
fig.tight_layout(rect=(0, 0.12, 1, 1))
plt.savefig('cond_vol.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 7 ------------------------------------------------------------------------------------------------------------------
add("halflife",
    "Decay of a volatility shock, 100(alpha+beta)^h, implied by GARCH(1,1)-t models for the Romanian base price (percent and EUR/MWh shocks, "
    f"{PERIOD}), Brent crude oil (ICE Brent front month, from 2019), EU carbon allowances (SparkChange EUA ETC, from {N['mkt']['eua_start']}) "
    "and OMV Petrom shares (BVB: SNP, from 2019), all to the cut-off; half-lives in brackets: oil and carbon shocks fade in weeks, not days.",
    KW_BASE + ", GARCH, persistence, half-life, Brent, EU ETS, carbon, OMV Petrom, mean reversion",
    DATA_PRICE + "; fuels_daily.csv: Brent BZ=F close, USD/bbl (Yahoo Finance); eua_daily.csv: SparkChange physical EUA ETC (CO2L), EUR "
    "(Yahoo Finance); ro_energy_equities_daily.csv: OMV Petrom (SNP) dividend-adjusted close and volume, RON (EODHD)",
    [("md", "## Half-life of a volatility shock\n\n$\\mathrm{E}_t[\\sigma^2_{t+h}]-\\bar\\sigma^2=(\\alpha+\\beta)^{h-1}(\\sigma^2_{t+1}-\\bar\\sigma^2)$, "
            "so half of the shock is gone after $h_{1/2}=\\ln 0.5/\\ln(\\alpha+\\beta)$ days. GARCH(1,1)-t on each series, over its own sample. "
            "Markets: log returns on trading days; Brent without the monthly roll days; OMV Petrom without zero-volume days."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN), ("code", ARCH), ("code", BRENT),
     ("code", r'''EUA = pd.read_csv(DATA + 'eua_daily.csv', usecols=['date', 'eua_etc_co2l_eur_per_unit'], parse_dates=['date']).set_index('date')['eua_etc_co2l_eur_per_unit']
EUAR = mkt_returns(EUA.loc[:str(END)])
EQ = pd.read_csv(DATA + 'ro_energy_equities_daily.csv', usecols=['date', 'SNP_adjclose_ron', 'SNP_volume'], parse_dates=['date']).set_index('date')
SNP = mkt_returns(EQ['SNP_adjclose_ron'].loc[str(START - pd.Timedelta(days=10)):str(END)], vol=EQ['SNP_volume']).loc[START:END]
print('EUA:', EUAR.index[0].date(), 'to', EUAR.index[-1].date(), '| SNP:', SNP.index[0].date(), 'to', SNP.index[-1].date())'''),
     ("md", "### Numbers on the slide"),
     ("code", r'''XM = {'RO_pct': E_PCT, 'RO_eur': E_EUR, 'BRENT': BRENT - BRENT.mean(), 'EUA': EUAR - EUAR.mean(), 'SNP': SNP - SNP.mean()}
PERS, HL = {}, {}
for k, e in XM.items():
    p = fit(e.dropna()).params
    PERS[k] = round(float(p['alpha[1]'] + p['beta[1]']), 4)
    HL[k] = round(float(np.log(0.5) / np.log(p['alpha[1]'] + p['beta[1]'])), 1)     # half-life, days
    slide(f'{k}: alpha + beta', f'xm.{k}.pers', PERS[k])
    slide(f'{k}: half-life, days', f'xm.{k}.hl', HL[k])
slide('Brent half-life, weeks (5 trading days)', 'xm.BRENT.hl_weeks', HL['BRENT'] / 5, 1)
slide('EUA half-life, weeks (5 trading days)', 'xm.EUA.hl_weeks', HL['EUA'] / 5, 1)'''),
     ("md", "### Chart"),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 2.1))
hh = np.arange(0, 121)
for k, lab, c in [('RO_pct', 'Romania, %', C_PCT), ('RO_eur', 'Romania, EUR/MWh', C_EUR), ('BRENT', 'Brent', PAL['c8']),
                  ('EUA', 'EUA', PAL['c6']), ('SNP', 'OMV Petrom', '#8c6d31')]:
    ax.plot(hh, 100 * PERS[k] ** hh, color=c, lw=1.3, label=f'{lab} ({HL[k]})')
ax.axhline(50, color='#222222', lw=0.6, ls=':')
ax.set_xlabel('days after the shock (trading days for markets, calendar days for power)', fontsize=9)
ax.set_ylabel('% left', fontsize=9)
ax.set_xlim(0, 120)
legend_bottom(fig, ncol=3)
fig.tight_layout(rect=(0, 0.26, 1, 1))
plt.savefig('halflife.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 8 ------------------------------------------------------------------------------------------------------------------
add("nic",
    f"News impact curves of GJR-GARCH(1,1,1)-t models for the daily shocks of the Romanian base price, {PERIOD}: next-day volatility "
    "as a function of today's shock, in percent and in EUR/MWh; in EUR/MWh rises raise volatility more (inverse leverage effect), in percent falls do.",
    KW_BASE + ", GJR-GARCH, asymmetry, leverage effect, inverse leverage effect, news impact curve",
    DATA_PRICE,
    [("md", "## News impact curve (GJR)\n\n$\\sigma_t^2=\\omega+(\\alpha+\\gamma I_{t-1})\\varepsilon_{t-1}^2+\\beta\\sigma_{t-1}^2$, "
            "$I_{t-1}=1$ if $\\varepsilon_{t-1}<0$. The curve sets $\\sigma_{t-1}^2$ at its long-run level "
            "$\\bar\\sigma^2=\\omega/(1-\\alpha-\\gamma/2-\\beta)$ and plots $\\sigma_t$ against the shock."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN), ("code", ARCH),
     ("md", "### Numbers on the slide"),
     ("code", r'''NIC = {}
for un, e in [('pct', E_PCT), ('eur', E_EUR)]:
    p = fit(e, o=1).params
    s2 = p['omega'] / (1 - (p['alpha[1]'] + 0.5 * p['gamma[1]'] + p['beta[1]']))
    sd = np.sqrt(s2)
    x = np.linspace(-4 * sd, 4 * sd, 201)
    NIC[un] = (x, np.sqrt(p['omega'] + p['beta[1]'] * s2 + (p['alpha[1]'] + p['gamma[1]'] * (x < 0)) * x ** 2))
    slide(f'{un}: shock of 2 long-run std. dev.', f'garch.{un}.nic_2sd', 2 * sd, 1)
    slide(f'{un}: next-day sigma after a rise', f'garch.{un}.nic_up2', np.sqrt(p['omega'] + p['beta[1]'] * s2 + p['alpha[1]'] * (2 * sd) ** 2), 2)
    slide(f'{un}: next-day sigma after a fall', f'garch.{un}.nic_dn2',
          np.sqrt(p['omega'] + p['beta[1]'] * s2 + (p['alpha[1]'] + p['gamma[1]']) * (2 * sd) ** 2), 2)'''),
     ("md", "### Chart"),
     ("code", r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1))
for ax, un, xl in [(axs[0], 'pct', r'shock $\varepsilon_{t-1}$, %'), (axs[1], 'eur', r'shock $u_{t-1}$, EUR/MWh')]:
    x_, s_ = NIC[un]
    ax.plot(x_[x_ < 0], s_[x_ < 0], color=PAL['c8'], lw=1.5)
    ax.plot(x_[x_ >= 0], s_[x_ >= 0], color=PAL['HU'], lw=1.5)
    ax.set_xlabel(xl, fontsize=9)
axs[0].set_ylabel(r'next-day $\sigma_t$', fontsize=9)
axs[0].set_title('percent', fontsize=9.5)
axs[1].set_title('EUR/MWh', fontsize=9.5)
legend_bottom(fig, handles=[plt.Line2D([], [], color=PAL['c8'], lw=1.5), plt.Line2D([], [], color=PAL['HU'], lw=1.5)],
              labels=['price fell yesterday', 'price rose yesterday'], ncol=2)
fig.tight_layout(rect=(0, 0.15, 1, 1))
plt.savefig('nic.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 9 ------------------------------------------------------------------------------------------------------------------
add("vol_level",
    f"Monthly standard deviation of the daily EUR/MWh shocks of the Romanian base price against the monthly mean price, {PERIOD}, "
    "log-log scales, coloured by year, with the log-log regression line: volatility in EUR/MWh grows with the price level.",
    KW_BASE + ", volatility and price level, log-log regression, merit order, scatter plot",
    DATA_PRICE,
    [("md", "## Volatility grows with the price level\n\nFor each month $m$: $\\hat\\sigma_m(u)$ = standard deviation of the daily EUR/MWh shocks, "
            "$\\bar P_m$ = mean price. OLS regression $\\ln\\hat\\sigma_m(u)=a+b\\ln\\bar P_m+e_m$ (and the same with the percent shocks)."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN),
     ("md", "### Numbers on the slide"),
     ("code", r'''m = pd.DataFrame({'sd': E_EUR.groupby(E_EUR.index.to_period('M')).std(), 'lvl': P.groupby(P.index.to_period('M')).mean()}).dropna()
ll = sm.OLS(np.log(m['sd']), sm.add_constant(np.log(m['lvl']))).fit()
mp = pd.DataFrame({'sd': E_PCT.groupby(E_PCT.index.to_period('M')).std(), 'lvl': m['lvl']}).dropna()
lp = sm.OLS(np.log(mp['sd']), sm.add_constant(np.log(mp['lvl']))).fit()
slide('months', 'level.n', len(m))
slide('slope, EUR/MWh volatility on price level', 'level.slope', ll.params.iloc[1], 2)
slide('  R^2', 'level.r2', ll.rsquared, 2)
slide('slope, percent volatility on price level', 'level.slope_pct', lp.params.iloc[1], 2)
slide('  R^2', 'level.r2_pct', lp.rsquared, 2)'''),
     ("md", "### Chart"),
     ("code", r'''SERIES = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948']
fig, ax = plt.subplots(figsize=(6.4, 2.3))
yrs = m.index.year
for y in range(START.year, END.year + 1):
    ax.scatter(m['lvl'][yrs == y], m['sd'][yrs == y], s=14, color=SERIES[(y - START.year) % 8], label=str(y), lw=0)
xx = np.linspace(m['lvl'].min(), m['lvl'].max(), 50)
ax.plot(xx, np.exp(ll.params.iloc[0]) * xx ** ll.params.iloc[1], color='#222222', lw=0.9, ls='--', label='log-log fit')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xticks([30, 50, 100, 200, 400])
ax.set_xticklabels(['30', '50', '100', '200', '400'])
ax.set_yticks([5, 10, 20, 50, 100])
ax.set_yticklabels(['5', '10', '20', '50', '100'])
ax.minorticks_off()
ax.set_xlabel('monthly mean price, EUR/MWh (log scale)', fontsize=9)
ax.set_ylabel('monthly $\\hat\\sigma(u)$,\nEUR/MWh', fontsize=9)
fig.legend(*ax.get_legend_handles_labels(), loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.0), frameon=False,
           fontsize=9.5, handlelength=1.0, columnspacing=0.8, handletextpad=0.2, markerscale=1.3)
fig.tight_layout(rect=(0, 0.12, 1, 1))
plt.savefig('vol_level.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 10 -----------------------------------------------------------------------------------------------------------------
add("ms_regime",
    f"Romanian daily base price and the smoothed probability of the turbulent regime of a two-regime Markov-switching model "
    f"(switching mean and variance) on the daily EUR/MWh shocks, {PERIOD}: the energy crisis was one long turbulent regime, 2026 moves in and out.",
    KW_BASE + ", Markov switching, regime switching, Hamilton filter, smoothed probabilities, energy crisis",
    DATA_PRICE,
    [("md", "## Two volatility regimes\n\n$u_t=\\mu_{s_t}+\\sigma_{s_t}\\eta_t$, $s_t\\in\\{\\text{calm},\\text{turbulent}\\}$ a two-state Markov chain "
            "(Hamilton, 1989), estimated by maximum likelihood with 20 random starting values (seed fixed). "
            "The chart shows the smoothed probability $\\Pr(s_t=\\text{turbulent}\\mid u_1,\\dots,u_T)$."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN),
     ("md", "### Numbers on the slide"),
     ("code", r'''from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression
np.random.seed(20261106)
ms = MarkovRegression(E_EUR.values, k_regimes=2, trend='c', switching_variance=True).fit(search_reps=20, disp=False)
s2 = ms.params[-2:]
hi = int(np.argmax(s2))                                  # turbulent = regime with the larger variance
PT = ms.regime_transition[:, :, 0]                        # PT[i, j] = Pr(s_t = i | s_{t-1} = j)
ph = pd.Series(ms.smoothed_marginal_probabilities[:, hi], index=E_EUR.index)
slide('std. dev. of shocks, turbulent regime', 'ms.eur.sd_hi', np.sqrt(s2[hi]), 1)
slide('std. dev. of shocks, calm regime', 'ms.eur.sd_lo', np.sqrt(s2[1 - hi]), 1)
slide('expected duration of the turbulent regime, days', 'ms.eur.dur_hi', 1 / (1 - PT[hi, hi]), 1)
on = (ph > 0.5).astype(int)
g = (on.diff() != 0).cumsum()
spells = on.groupby(g).agg(['first', 'size'])
idx = on[g == spells[spells['first'] == 1]['size'].idxmax()].index
slide('longest turbulent spell, start', 'ms.eur.longest_start', str(idx[0].date()))
slide('longest turbulent spell, end', 'ms.eur.longest_end', str(idx[-1].date()))
slide('longest turbulent spell, days', 'ms.eur.longest_days', int(len(idx)))
for y in [2022, 2025, 2026]:
    slide(f'share of turbulent days in {y}, %', f'ms.eur.by_year.{y}', 100 * (ph[ph.index.year == y] > 0.5).mean(), 0)
slide('share of turbulent days since 1 July 2026, %', 'ms.eur.share_2026_q3q4', 100 * (ph.loc['2026-07-01':] > 0.5).mean(), 0)
slide('probability at the cut-off', 'ms.eur.last_prob', ph.iloc[-1], 2)'''),
     ("md", "### Chart"),
     ("code", YFMT + r'''
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.1), sharex=True, gridspec_kw={'height_ratios': [1, 1]})
axs[0].plot(P.index, P.values, color=PAL['RO'], lw=0.6)
axs[0].set_ylabel('EUR/MWh', fontsize=9.5)
axs[1].fill_between(ph.index, 0, ph.values, color=C_EUR, alpha=0.6, lw=0)
axs[1].set_ylabel('prob.', fontsize=9.5)
axs[1].set_ylim(0, 1)
axs[1].set_yticks([0, 0.5, 1])
axs[0].yaxis.set_major_locator(MaxNLocator(3))
yfmt(axs[1])
legend_bottom(fig, handles=[plt.Line2D([], [], color=PAL['RO']), Patch(color=C_EUR, alpha=0.6)],
              labels=['daily base price', 'probability of the turbulent regime (smoothed)'], ncol=2)
fig.tight_layout(rect=(0, 0.12, 1, 1))
plt.savefig('ms_regime.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 11 -----------------------------------------------------------------------------------------------------------------
DATA_HOURLY = ("power_da_prices_hourly_utc.csv: hourly day-ahead price of Romania (OPCOM, via energy-charts.info / ENTSO-E; 15-min market "
               "time units averaged to the hour from 1 Oct 2025), EUR/MWh")
add("rv_solar",
    f"Relative intraday variation of the Romanian day-ahead price (realised variation of hourly prices divided by the daily price, monthly median) "
    f"and mean Romanian solar generation (monthly mean, MW), {PERIOD}: solar generation has made the price move more within the day.",
    KW_BASE + ", intraday variation, realised volatility, hourly prices, solar generation, renewables",
    DATA_PRICE + "; " + DATA_HOURLY + "; generation_ro_mw_daily_cet.csv: Romanian solar generation, daily mean MW (ENTSO-E, Transelectrica data, via energy-charts.info)",
    [("md", "## Intraday variation and solar generation\n\n$RV_d=\\sqrt{\\sum_h (P_{d,h}-P_{d,h-1})^2}$ over the hours of delivery day $d$; "
            "relative variation $RV_d/|\\bar P_d|$, with $\\bar P_d$ the mean hourly price of the day."),
     ("code", PRICES), ("code", HOURLY),
     ("code", r'''GEN = pd.read_csv(DATA + 'generation_ro_mw_daily_cet.csv', usecols=['date_cet', 'solar'], parse_dates=['date_cet']).set_index('date_cet')
SOL = GEN['solar'].reindex(CAL)
RV['rel'] = RV['rv'] / RV['lvl'].abs()'''),
     ("md", "### Numbers on the slide"),
     ("code", r'''YEARS = list(range(START.year, END.year + 1))
rel = {y: round(RV['rel'][RV.index.year == y].median(), 2) for y in YEARS}
for y in YEARS:
    slide(f'median relative intraday variation, {y}', f'rv.rel_by_year.{y}', rel[y])
slide('year of the peak', 'rv.rel_peak_year', max(YEARS, key=lambda y: rel[y]))
slide('mean solar output 2019, MW', 'rv.sol_2019', SOL[SOL.index.year == 2019].mean(), 0)
slide(f'mean solar output {END.year} (to the cut-off), MW', 'rv.sol_last', SOL[SOL.index.year == END.year].mean(), 0)
mm = pd.DataFrame({'rel': RV['rel'].resample('MS').median(), 'sol': SOL.resample('MS').mean()}).dropna()
slide('monthly correlation', 'rv.corr_rel_solar_m', np.corrcoef(mm['rel'], mm['sol'])[0, 1], 2)'''),
     ("md", "### Chart"),
     ("code", YFMT + r'''
from matplotlib.ticker import MaxNLocator
fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.1), sharex=True)
rm = RV['rel'].resample('MS').median()
axs[0].plot(rm.index, rm.values, color=PAL['RO'], lw=1.2)
axs[0].set_ylabel('RV / price', fontsize=9.5)
sm_ = SOL.resample('MS').mean()
axs[1].plot(sm_.index, sm_.values, color=PAL['BG'], lw=1.2)
axs[1].set_ylabel('solar, MW', fontsize=9.5)
yfmt(axs[1])
legend_bottom(fig, handles=[plt.Line2D([], [], color=PAL['RO'], lw=1.2), plt.Line2D([], [], color=PAL['BG'], lw=1.2)],
              labels=['RV / daily price (monthly median)', 'solar output (monthly mean)'], ncol=2)
for ax in axs:
    ax.yaxis.set_major_locator(MaxNLocator(3))
fig.tight_layout(rect=(0, 0.12, 1, 1))
plt.savefig('rv_solar.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 12 -----------------------------------------------------------------------------------------------------------------
add("har_fc",
    f"Realised intraday variation of the Romanian day-ahead price and its one-day-ahead HAR forecast over the test year {TEST}, "
    "the HAR model being re-estimated every day on the data available the day before: the forecasts follow the variation, not its isolated spikes.",
    KW_BASE + ", HAR model, realised volatility, intraday variation, forecasting, out-of-sample, mean absolute error",
    DATA_PRICE + "; " + DATA_HOURLY,
    [("md", "## HAR forecasts of intraday variation\n\n$\\ln RV_d=b_0+b_D\\ln RV_{d-1}+\\frac{b_W}{7}\\sum_{j=1}^{7}\\ln RV_{d-j}+"
            "\\frac{b_M}{30}\\sum_{j=1}^{30}\\ln RV_{d-j}+e_d$ (Corsi, 2009), by OLS. Forecast $=\\exp(\\widehat{\\ln RV}_d+s^2/2)$, "
            "$s^2$ = residual variance. Test year = the last 365 days to the cut-off; the model is re-estimated every day on an expanding window."),
     ("code", PRICES), ("code", HOURLY),
     ("code", r'''import statsmodels.api as sm
lr = np.log(RV['rv'])
HD = pd.DataFrame({'y': lr, 'd': lr.shift(1), 'w': lr.shift(1).rolling(7).mean(), 'm': lr.shift(1).rolling(30).mean()}).dropna()
TEST0 = END - pd.Timedelta(days=364)
TDAYS = pd.date_range(TEST0, END, freq='D')
tr = HD.loc[:TEST0 - pd.Timedelta(days=1)]
HAR = sm.OLS(tr['y'], sm.add_constant(tr[['d', 'w', 'm']])).fit(cov_type='HAC', cov_kwds={'maxlags': 7})
pred = []
for t in TDAYS:                                       # expanding window, data up to d-1
    tr = HD.loc[:t - pd.Timedelta(days=1)]
    Xt = sm.add_constant(tr[['d', 'w', 'm']]).values
    b = np.linalg.lstsq(Xt, tr['y'].values, rcond=None)[0]
    s2 = np.var(tr['y'].values - Xt @ b)
    pred.append(np.exp(np.r_[1.0, HD.loc[t, ['d', 'w', 'm']].values] @ b + 0.5 * s2))
HARF = pd.Series(pred, index=TDAYS)
act = RV['rv'].loc[TDAYS]
naive = RV['rv'].shift(1).loc[TDAYS]'''),
     ("md", "### Numbers on the slide"),
     ("code", r'''for k, nm in [('d', 'bd'), ('w', 'bw'), ('m', 'bm')]:
    slide(f'HAR coefficient b_{k.upper()} (before the test year)', f'har.{nm}', HAR.params[k], 3)
    slide(f'  HAC t-statistic', f'har.{nm}_t', HAR.tvalues[k], 1)
slide('R^2', 'har.r2', HAR.rsquared, 2)
mae_h, mae_n = (HARF - act).abs().mean(), (naive - act).abs().mean()
slide('test year MAE, HAR, EUR/MWh', 'har.mae_har', mae_h, 1)
slide("test year MAE, yesterday's value, EUR/MWh", 'har.mae_naive', mae_n, 1)
slide('error reduction, %', 'har.gain', 100 * (1 - mae_h / mae_n), 1)'''),
     ("md", "### Chart"),
     ("code", YFMT + r'''
fig, ax = plt.subplots(figsize=(6.4, 2.0))
ax.plot(act.index, act.values, color='#9a9a9a', lw=0.7, label='realised intraday variation $RV_d$')
ax.plot(HARF.index, HARF.values, color=PAL['RO'], lw=1.1, label='HAR forecast made on $d-1$')
ax.set_ylabel('EUR/MWh', fontsize=9.5)
mfmt(ax, 2)
legend_bottom(fig, ncol=2)
fig.tight_layout(rect=(0, 0.2, 1, 1))
plt.savefig('har_fc.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 13 -----------------------------------------------------------------------------------------------------------------
ROLL_MD = ("## Rolling one-day-ahead GARCH-t forecasts\n\nFor every day $t$ of the test year (the last 365 days to the cut-off) the mean equation "
           "(constant + AR(1..7) + day-of-week dummies) and a GARCH(1,1)-t on its residuals are re-estimated on all EUR/MWh changes up to $t-1$; "
           "the 30-day historical variance is the mean of the last 30 squared residuals. The 365 re-estimations are kept out of the default run, "
           f"so the results are loaded from `{ROLL_FILE}` (saved in this Quantlet by `lectures/L3/make_quantlets_L3.py` with exactly this code); "
           "set `RUN_ALL = True` to recompute them.")
DATA_ROLL = f"; {ROLL_FILE} (in this Quantlet): the 365 rolling one-day-ahead GARCH(1,1)-t and 30-day historical variance forecasts, computed from these prices"
add("fc_test",
    f"Absolute daily EUR/MWh shocks of the Romanian base price over the test year {TEST} with the one-day-ahead GARCH(1,1)-t volatility forecast "
    "and the 30-day historical volatility, both re-estimated every day with the data up to the day before: GARCH reacts at once, "
    "the 30-day history lags and then forgets the shock abruptly 30 days later.",
    KW_BASE + ", GARCH, volatility forecasting, historical volatility, out-of-sample, rolling window",
    DATA_PRICE + DATA_ROLL,
    [("code", PRICES), ("code", CHANGES), ("md", ROLL_MD), ("code", roll_cell("fc_test")),
     ("md", "### Numbers on the slide\n\nThe largest absolute shock of the test year and the two forecasts around it."),
     ("code", r'''ts = R['e'].abs().idxmax()
k = R.index.get_loc(ts)
slide('largest shock of the test year, EUR/MWh', 'ghost.shock', R['e'].loc[ts], 1)
slide('  on', 'ghost.date', str(ts.date()))
slide('GARCH sigma on that day (made the day before)', 'ghost.garch_before', np.sqrt(R['garch'].iloc[k]), 1)
slide('GARCH sigma the next day', 'ghost.garch_after', np.sqrt(R['garch'].iloc[k + 1]), 1)
slide('30-day historical sigma the next day', 'ghost.hist_after', np.sqrt(R['hist30'].iloc[k + 1]), 1)
slide('30-day historical sigma 30 days later', 'ghost.hist_30', np.sqrt(R['hist30'].iloc[k + 30]), 1)
slide('30-day historical sigma 31 days later', 'ghost.hist_31', np.sqrt(R['hist30'].iloc[k + 31]), 1)'''),
     ("md", "### Chart"),
     ("code", YFMT + r'''
fig, ax = plt.subplots(figsize=(6.4, 2.0))
ax.bar(R.index, R['e'].abs(), color='#b5b5b5', width=1.0, label='realised $|u_t|$')
ax.plot(R.index, np.sqrt(R['garch']), color=C_EUR, lw=1.2, label=r'GARCH-t $\hat\sigma_t$, forecast on $t-1$')
ax.plot(R.index, np.sqrt(R['hist30']), color=PAL['BG'], lw=1.0, ls='--', label='30-day historical')
ax.set_ylabel('EUR/MWh', fontsize=9.5)
mfmt(ax, 2)
legend_bottom(fig, ncol=3)
fig.tight_layout(rect=(0, 0.2, 1, 1))
plt.savefig('fc_test.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 14 -----------------------------------------------------------------------------------------------------------------
add("case_band",
    f"Romanian daily base price over the test year {TEST} with the one-day 90% band set the day before: forecast price "
    "(previous price + forecast change of the mean equation) plus or minus the Student-t quantile times the GARCH(1,1)-t volatility forecast; "
    "days outside the band are marked.",
    KW_BASE + ", GARCH, prediction interval, risk limits, Student-t, backtesting, case study",
    DATA_PRICE + DATA_ROLL,
    [("code", PRICES), ("code", CHANGES), ("md", ROLL_MD), ("code", roll_cell("case_band")),
     ("md", "### The 90% band and the numbers on the slide\n\nBand $=\\hat P_t\\pm q_{0.95}(\\nu)\\sqrt{(\\nu-2)/\\nu}\\,\\hat\\sigma_t$, "
            "with $\\hat P_t=P_{t-1}+\\widehat{\\Delta P}_t$ and $q_{0.95}(\\nu)$ the Student-$t$ quantile (unit-variance scaling)."),
     ("code", r'''from scipy import stats
q = stats.t.ppf(0.95, R['nu']) * np.sqrt((R['nu'] - 2) / R['nu'])
w = q * np.sqrt(R['garch'])                       # half-width, EUR/MWh
out = R['e'].abs() > w
y1 = END.year
slide('days in the test year', 'fc.n', len(R))
slide('days outside the band', 'fc.eur.band_out', int(out.sum()))
slide('  share, % (10% expected)', 'fc.eur.band_out_pct', 100 * out.mean(), 1)
slide('share outside, November to April, %', 'case.band_out_first', 100 * out.loc[:f'{y1}-04-30'].mean(), 1)
slide('share outside, May to October, %', 'case.band_out_last', 100 * out.loc[f'{y1}-05-01':].mean(), 1)
slide('mean half-width, November to April, EUR/MWh', 'case.band_w_first', w.loc[:f'{y1}-04-30'].mean(), 0)
slide('mean half-width, September to October, EUR/MWh', 'case.band_w_last', w.loc[f'{y1}-09-01':].mean(), 0)'''),
     ("md", "### Chart"),
     ("code", YFMT + r'''
pm = P.shift(1).loc[TDAYS] + R['yhat']
fig, ax = plt.subplots(figsize=(6.4, 2.1))
ax.fill_between(TDAYS, pm - w, pm + w, color=C_EUR, alpha=0.25, lw=0, label='90% GARCH-t band (set on $t-1$)')
ax.plot(TDAYS, P.loc[TDAYS], color=PAL['RO'], lw=0.8, label='base price')
oo = out[out]
ax.scatter(oo.index, P.loc[oo.index], s=9, color=PAL['c8'], zorder=3, label='outside the band')
ax.set_ylabel('EUR/MWh', fontsize=9.5)
mfmt(ax, 2)
legend_bottom(fig, ncol=3)
fig.tight_layout(rect=(0, 0.13, 1, 1))
plt.savefig('case_band.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])

# 15 -----------------------------------------------------------------------------------------------------------------
add("term_structure",
    f"Term structure of GARCH(1,1)-t volatility forecasts: daily volatility forecast of the Romanian base price (EUR/MWh shocks) for the "
    f"60 days after the cut-off {N['data']['end']}, against its long-run level (left); 90% band of the Brent return over h trading days on "
    f"{N['ts']['brent']['peak']['date']}, the day of the highest 2026 Brent volatility, from the GARCH forecasts, from today's sigma times sqrt(h) and "
    "from the long-run level (right). Estimation samples from 2019.",
    KW_BASE + ", GARCH, volatility forecast, term structure, mean reversion, square-root-of-time rule, Brent, risk limits, case study",
    DATA_PRICE + "; fuels_daily.csv: Brent BZ=F close, USD/bbl (Yahoo Finance)",
    [("md", "## Term structure of the volatility forecast\n\n$\\hat\\sigma^2_{T+h\\mid T}=\\bar\\sigma^2+(\\alpha+\\beta)^{h-1}(\\hat\\sigma^2_{T+1}-\\bar\\sigma^2)$, "
            "$\\bar\\sigma^2=\\omega/(1-\\alpha-\\beta)$. For returns without autocorrelation (oil), the variance over $h$ days is "
            "$\\sum_{k=1}^{h}\\hat\\sigma^2_{T+k\\mid T}$, not $h\\hat\\sigma^2_{T+1}$; 90% band $=\\pm1.645\\sqrt{\\cdot}$."),
     ("code", PRICES), ("code", CHANGES), ("code", MEAN), ("code", ARCH), ("code", BRENT),
     ("md", "### Numbers on the slide"),
     ("code", r'''from scipy import stats
z95 = stats.norm.ppf(0.95)
res = fit(E_EUR)
f = res.forecast(horizon=60, reindex=False).variance.values[-1]
p = res.params
lr = p['omega'] / (1 - p['alpha[1]'] - p['beta[1]'])
slide('Romania: sigma forecast for the next day, EUR/MWh', 'ts.eur.s1', np.sqrt(f[0]), 1)
slide('Romania: long-run sigma, EUR/MWh', 'ts.eur.lr', np.sqrt(lr), 1)
slide('Romania: one-day 90% limit, +/- EUR/MWh', 'ts.eur.lim1', z95 * np.sqrt(f[0]), 0)

# Brent: day of the highest 2026 conditional volatility (full-sample model), then forecasts with data up to that day only
cvb = pd.Series(fit(BRENT - BRENT.mean()).conditional_volatility, index=BRENT.index) * np.sqrt(252)
BPEAK = cvb.loc[str(END.year)].idxmax()
TSB = {}
for tag, t_end in [('peak', BPEAK), ('end', BRENT.index[-1])]:
    xb = BRENT.loc[:t_end]
    gb = fit(xb - xb.mean())
    fb = gb.forecast(horizon=60, reindex=False).variance.values[-1]
    lrb = gb.params['omega'] / (1 - gb.params['alpha[1]'] - gb.params['beta[1]'])
    TSB[tag] = (fb, lrb)
    slide(f'Brent ({tag}): forecast day', f'ts.brent.{tag}.date', str(t_end.date()))
    slide(f'  sigma next day, % a year', f'ts.brent.{tag}.s1_ann', np.sqrt(fb[0] * 252), 0)
    slide(f'  long-run sigma, % a year', f'ts.brent.{tag}.lr_ann', np.sqrt(lrb * 252), 0)
    slide(f'  20-day 90% band, GARCH, +/- %', f'ts.brent.{tag}.band20', z95 * np.sqrt(fb[:20].sum()), 1)
    slide(f'  20-day 90% band, sigma x sqrt(20), +/- %', f'ts.brent.{tag}.band20_sqrt', z95 * np.sqrt(20 * fb[0]), 1)
    slide(f'  sigma x sqrt(20) too wide by, %', f'ts.brent.{tag}.over', 100 * (np.sqrt(20 * fb[0]) / np.sqrt(fb[:20].sum()) - 1), 0)'''),
     ("md", "### Chart"),
     ("code", r'''MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.1))
h = np.arange(1, 61)
axs[0].plot(h, np.sqrt(f), color=C_EUR, lw=1.4, label='GARCH-t forecast, Romania')
axs[0].axhline(np.sqrt(lr), color='#222222', lw=0.8, ls='--', label='long-run level')
axs[0].set_xlabel('days ahead $h$', fontsize=9)
axs[0].set_ylabel('EUR/MWh', fontsize=9)
axs[0].set_ylim(0, 1.25 * np.sqrt(lr))
axs[0].set_title(r'Romania: daily $\sigma$ forecast', fontsize=9.5)
hb = np.arange(1, 41)
fb, lrb = TSB['peak']
axs[1].plot(hb, z95 * np.sqrt(np.cumsum(fb[:40])), color=PAL['c8'], lw=1.4, label='GARCH-t band, Brent')
axs[1].plot(hb, z95 * np.sqrt(hb * fb[0]), color=PAL['BG'], lw=1.1, ls='-.', label=r"today's $\sigma\times\sqrt{h}$")
axs[1].plot(hb, z95 * np.sqrt(hb * lrb), color='#222222', lw=0.8, ls='--')
axs[1].set_xlabel('horizon $h$ (trading days)', fontsize=9)
axs[1].set_ylabel(r'$\pm$%', fontsize=9)
axs[1].set_title(f'Brent, {MON[BPEAK.month - 1]} {BPEAK.day}: 90% band over $h$ days', fontsize=9.5)
legend_bottom(fig, ncol=2)
fig.tight_layout(rect=(0, 0.27, 1, 1))
plt.savefig('term_structure.png', dpi=150, bbox_inches='tight', transparent=True)
plt.show()''')])


# ======================================================================================================================
# Saved rolling forecasts (computed here with the same code as the RUN_ALL branch of the notebooks)
# ======================================================================================================================
def save_rolling(folders):
    from joblib import Parallel, delayed
    ns = {"DATA": os.path.join(REPO, "data", "clean") + os.sep}
    exec("\n\n".join([SETUP, PRICES, CHANGES, MEAN, ARCH, ONE_DAY]), ns)
    pd, u, START, END = ns["pd"], ns["u"], ns["START"], ns["END"]
    tdays = pd.date_range(END - pd.Timedelta(days=364), END, freq="D")
    y = u.loc[START:END]
    rows = Parallel(n_jobs=-1)(delayed(ns["one_day"])(y, t) for t in tdays)
    R = pd.DataFrame(rows, index=tdays)
    R.index.name = "date"
    for fo in folders:
        os.makedirs(fo, exist_ok=True)
        R.to_csv(os.path.join(fo, ROLL_FILE))
    print("rolling GARCH-t forecasts saved:", len(R), "days,", ", ".join(os.path.basename(f) for f in folders))


# ======================================================================================================================
# Check of the printed numbers against L3_numbers.json
# ======================================================================================================================
LINE = re.compile(r"^(.*\S)\s+(\S+)\s+\[([A-Za-z0-9_.]+)\]\s*$")


def lookup(key):
    x = N
    for p in key.split("."):
        x = x[p]
    return x


def check(q):
    import nbformat
    nb = nbformat.read(os.path.join(q.folder, q.name + ".ipynb"), as_version=4)
    bad, n = [], 0
    for c in nb.cells:
        for o in c.get("outputs", []):
            if o.get("output_type") != "stream":
                continue
            for ln in o["text"].splitlines():
                m = LINE.match(ln)
                if not m:
                    continue
                n += 1
                val, key = m.group(2), m.group(3)
                ref = lookup(key)
                if isinstance(ref, str):
                    ok = val == ref
                else:
                    try:
                        ok = abs(float(val) - float(ref)) < 1e-9
                    except ValueError:
                        ok = False
                if not ok:
                    bad.append(f"{key}: notebook {val}, json {ref}")
    return n, bad


def main(only=None):
    charts = only or list(Q)
    need = [os.path.join(QL_ROOT, "L3", f"EMQA_L3_{c}") for c in ("fc_test", "case_band") if c in charts]
    if need:
        save_rolling(need)
    report = {}
    for c in charts:
        desc, kw, df, cells = Q[c]
        q = Quantlet(3, c, desc, kw, df, title=desc.split(":")[0] if len(desc.split(":")[0]) < 160 else None)
        q.code(SETUP)
        for kind, txt in cells:
            (q.md if kind == "md" else q.code)(txt)
        q.write(execute=True)
        report[c] = check(q)
    print("\nNumbers printed by the notebooks vs L3_numbers.json")
    nbad = 0
    for c, (n, bad) in report.items():
        print(f"  {c:<16s} {n:3d} numbers checked, {len(bad)} mismatch(es)")
        for b in bad:
            print("      MISMATCH", b)
        nbad += len(bad)
    print(f"{len(report)} Quantlets written; {nbad} mismatch(es)")
    return nbad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:] or None) else 0)
