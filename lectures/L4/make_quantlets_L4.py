"""
make_quantlets_L4.py -- one Quantlet per chart of Lecture 4 (EMQA), as in the MFM and SFM courses
================================================================================================
Writes Quantlets/L4/EMQA_L4_<chart>/ for every chart shown in lecture4.pdf (main part and appendix):
    Metainfo.txt, EMQA_L4_<chart>.ipynb (executed), <chart>.png
Each notebook is self-contained (no import of the lecture modules): it loads only the data it needs from the course
repository (local data/clean or the public GitHub copy), recomputes the chart and prints the numbers shown on the slide
under the key they have in L4_numbers.json. After execution this script reads those printed numbers back and checks
them against L4_numbers.json (any mismatch stops the script).

The rolling VaR forecasts are recomputed inside the notebooks: without the Acerbi-Szekely simulations (which only the
ES test needs) the engine of analysis_L4.py takes about 2 s for HS, normal, FHS and EVT and about 40 s for the
Student-t fits, and it reproduces the cached forecasts exactly; so no Quantlet needs a pre-computed file.

Run from the repository root:  python3 lectures/L4/make_quantlets_L4.py [chart ...]
"""
import json
import os
import re
import sys

import nbformat

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_quantlet import Quantlet  # noqa: E402

with open(os.path.join(HERE, "L4_numbers.json")) as fh:
    N = json.load(fh)
END = N["cutoff"]["end"]
PER = {k: v["period_en"].replace("\\%", "%") for k, v in N["charts"].items()}

# ---------------------------------------------------------------- cells shared by several Quantlets
SETUP = r"""import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, NullFormatter

# course chart style: transparent background, no gridlines, legend at the bottom outside the axes
plt.rcParams.update({
    'figure.facecolor': 'none', 'axes.facecolor': 'none', 'savefig.transparent': True,
    'axes.grid': False, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.edgecolor': '#222222', 'axes.labelcolor': '#222222', 'xtick.color': '#222222', 'ytick.color': '#222222',
    'text.color': '#222222', 'font.size': 11, 'axes.labelsize': 11, 'legend.fontsize': 10.5,
    'legend.frameon': False, 'lines.linewidth': 1.4, 'font.family': 'DejaVu Sans'})
PAL = {'RO': '#2a78d6', 'DE_LU': '#eb6834', 'HU': '#1baf7a', 'BG': '#eda100',
       'c5': '#e87ba4', 'c6': '#008300', 'c7': '#6250d6', 'c8': '#e34948'}   # fixed colour per zone / series


def legend_bottom(fig, ncol=4):
    # one legend for the whole figure, centred under the axes
    handles, labels = [], []
    for ax in fig.axes:
        for h, l in zip(*ax.get_legend_handles_labels()):
            if l not in labels:
                handles.append(h)
                labels.append(l)
    fig.legend(handles, labels, loc='lower center', ncol=ncol, bbox_to_anchor=(0.5, 0.0),
               frameon=False, handlelength=2.0, columnspacing=1.2)


def show(key, value):
    # prints a number shown on the slide, under its key in lectures/L4/L4_numbers.json
    print(f'{key:<28} = {value}')


def d(ts):
    return pd.Timestamp(ts).strftime('%Y-%m-%d')"""

PRICES = r"""# daily day-ahead base prices (mean of all market time units of the CET/CEST delivery day), EUR/MWh
PD = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')
START = pd.Timestamp('2015-01-01')
END = pd.Timestamp('@END@')           # cut-off of Lecture 4: last complete month of the download
CAL = pd.date_range(START, END, freq='D')
P = PD[@ZONES@].reindex(CAL)           # full calendar: missing days stay missing
X = P.diff()                           # daily change X_t = P_t - P_{t-1}; a change next to a gap is missing
print('daily prices', d(START), 'to', d(END), '| missing days in Romania:', int(P['RO'].isna().sum()))""".replace("@END@", END)


def prices(zones=("RO",)):
    return PRICES.replace("@ZONES@", repr(list(zones)))


ARCH = r"""# the GARCH filter uses the arch package (not preinstalled on Google Colab)
import importlib.util, subprocess, sys
if importlib.util.find_spec('arch') is None:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'arch'])
from arch import arch_model"""

ENGINE_MD = (r"## Rolling one-day-ahead VaR" "\n\n"
             r"For every day $t$ from 1 January 2017 to the cut-off the forecast uses changes up to $t-1$ only:" "\n\n"
             r"* **HS** (historical simulation): empirical $\alpha$-quantile of the last 365 changes;" "\n"
             r"* **normal**: $\hat\mu+\hat\sigma\,\Phi^{-1}(\alpha)$ on the same 365 changes;" "\n"
             r"* **Student-t**: maximum-likelihood $t$ fit on the same window ($\nu\ge 2.2$);" "\n"
             r"* **FHS** (filtered historical simulation): $\mathrm{VaR}_t=\mu_{d(t)}+\sigma_t\,\hat q_\alpha(z)$, weekday mean $\mu_d$, "
             r"GARCH(1,1) volatility $\sigma_t$ and standardised residuals $z$, refitted every 21 days on 730 days;" "\n"
             r"* **EVT** (conditional extreme value theory): same filter, generalised Pareto tail above the 90% quantile of $z$." "\n\n"
             "This is the forecasting engine of the lecture (`analysis_L4.py`) without the simulations of the expected-shortfall test.")

ENGINE = r"""W_HS, W_G, REFIT, U_EVT = 365, 730, 21, 0.90
T0 = pd.Timestamp('2017-01-01')       # first backtest day


def fit_t(w):
    nu, loc, sc = stats.t.fit(w)
    if nu < 2.2:                       # keep a finite variance
        nu = 2.2
        _, loc, sc = stats.t.fit(w, f0=nu)
    return nu, loc, sc


def garch_filter(e):
    # GARCH(1,1), zero mean, Gaussian QMLE on the de-meaned changes
    res = arch_model(e, mean='Zero', vol='GARCH', p=1, q=1, dist='normal', rescale=False).fit(disp='off')
    return (float(res.params['omega']), float(res.params['alpha[1]']), float(res.params['beta[1]']),
            np.asarray(res.conditional_volatility))


def gpd_tail(z, u_q=U_EVT):
    # peaks over threshold: threshold u, GPD shape xi and scale beta (location 0)
    u = np.quantile(z, u_q)
    exc = z[z > u] - u
    xi, _, beta = stats.genpareto.fit(exc, floc=0)
    return u, xi, beta, len(exc), len(z)


def var_evt(tail, a):
    u, xi, beta, n_u, n = tail
    r = (n / n_u) * (1 - a)
    if abs(xi) < 1e-6:
        return u - beta * np.log(r)
    return u + beta / xi * (r ** (-xi) - 1)


def var_engine(xs, end, methods, levels):
    days = pd.date_range(T0, end, freq='D')
    out = {m: {a: np.full(len(days), np.nan) for a in levels} for m in methods}
    state = None
    for k, t in enumerate(days):
        hist = xs[:t - pd.Timedelta(days=1)].dropna()
        w = hist.values[-W_HS:]
        if 't' in methods:
            nu, loc, sc = fit_t(w)
        for a in levels:
            if 'hs' in methods:
                out['hs'][a][k] = np.quantile(w, a)
            if 'normal' in methods:
                out['normal'][a][k] = np.mean(w) + np.std(w, ddof=1) * stats.norm.ppf(a)
            if 't' in methods:
                out['t'][a][k] = loc + sc * stats.t.ppf(a, nu)
        if not {'fhs', 'evt'} & set(methods):
            continue
        if k % REFIT == 0:             # refit the filter on the last 730 changes
            hw = hist[-W_G:]
            mdow = hw.groupby(hw.index.dayofweek).mean()
            e = (hw - mdow.reindex(hw.index.dayofweek).values).values
            om, al, be, sw = garch_filter(e)
            z = e / sw
            state = {'om': om, 'al': al, 'be': be, 'mdow': mdow, 'z': np.sort(z), 'tail': gpd_tail(z),
                     's2': sw[-1] ** 2, 'e': e[-1], 'tlast': hw.index[-1]}
        while state['tlast'] < t - pd.Timedelta(days=1):    # advance sigma to t-1
            nxt = state['tlast'] + pd.Timedelta(days=1)
            state['s2'] = state['om'] + state['al'] * state['e'] ** 2 + state['be'] * state['s2']
            xv = xs.get(nxt, np.nan)
            state['e'] = (xv - state['mdow'][nxt.dayofweek]) if not np.isnan(xv) else np.sqrt(state['s2'])
            state['tlast'] = nxt
        s_t = np.sqrt(state['om'] + state['al'] * state['e'] ** 2 + state['be'] * state['s2'])
        m_t = state['mdow'][t.dayofweek]
        for a in levels:
            if 'fhs' in methods:
                out['fhs'][a][k] = m_t + s_t * np.quantile(state['z'], a)
            if 'evt' in methods:
                out['evt'][a][k] = m_t + s_t * var_evt(state['tail'], a)
    return days, out"""

KUPIEC = r"""def kupiec(hits, p0):
    # likelihood-ratio test of unconditional coverage (Kupiec, 1995)
    n, x = len(hits), int(np.sum(hits))
    ph = x / n
    ll0 = (n - x) * np.log(1 - p0) + x * np.log(p0)
    ll1 = (n - x) * np.log(1 - ph) + (x * np.log(ph) if x > 0 else 0.0) if 0 < ph < 1 else 0.0
    lr = -2 * (ll0 - ll1)
    return lr, float(stats.chi2.sf(lr, 1))"""

QR = r"""from statsmodels.regression.quantile_regression import QuantReg
PR = P['RO']


def qr_forecast(t, taus, w=365):
    # quantile regression of P_t on P_{t-1}, P_{t-7} and weekday dummies, fitted on the w days before t
    idx = pd.date_range(t - pd.Timedelta(days=w), t - pd.Timedelta(days=1), freq='D')
    df = pd.DataFrame({'y': PR.reindex(idx), 'p1': PR.shift(1).reindex(idx), 'p7': PR.shift(7).reindex(idx)})
    for j in range(6):
        df[f'd{j}'] = (idx.dayofweek == j).astype(float)
    df = df.dropna()
    Xm = np.column_stack([np.ones(len(df)), df[['p1', 'p7'] + [f'd{j}' for j in range(6)]].values])
    xt = np.r_[1.0, PR.get(t - pd.Timedelta(days=1), np.nan), PR.get(t - pd.Timedelta(days=7), np.nan),
               [(t.dayofweek == j) * 1.0 for j in range(6)]]
    return {tau: float(xt @ QuantReg(df['y'].values, Xm).fit(q=tau, max_iter=5000).params) for tau in taus}


def conformal(qrf, tau):
    # one-sided conformal widening: add the tau-quantile of the last 365 out-of-sample errors P_s - q_s, s < t
    res = PR.reindex(qrf.index) - qrf
    return qrf + res.shift(1).rolling(365, min_periods=300).quantile(tau)"""

MONTHS = r"""MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def month_axis(ax, step=1):
    # quarterly ticks fall on Jan/Apr/Jul/Oct, so every January (with its year) gets a label
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(1, 13, step)) if step > 1 else mdates.MonthLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: MON[mdates.num2date(v).month - 1] +
                                               (f'\n{mdates.num2date(v).year}' if mdates.num2date(v).month == 1 or p == 0 else '')))"""

COLM = r"""COL = {'hs': PAL['BG'], 'normal': PAL['c5'], 't': PAL['c7'], 'fhs': PAL['RO'], 'evt': PAL['DE_LU']}
LAB = {'hs': 'HS', 'normal': 'Normal', 't': 'Student-t', 'fhs': 'FHS', 'evt': 'EVT'}"""

SRC_EC = "energy-charts.info (Fraunhofer ISE), OPCOM day-ahead prices for Romania via ENTSO-E"
KW_RISK = "value at risk, VaR, expected shortfall, risk management, electricity prices, day-ahead market, Romania, OPCOM"


def save_cell(name):
    # bottom margin = top of the legend minus the tight_layout pad: no empty band between the axis labels and the legend
    return ("fig.canvas.draw()\n"
            "legend_top = max(lg.get_window_extent().y1 for lg in fig.legends) / fig.dpi\n"
            "fig.tight_layout(rect=(0, max(legend_top - 0.08, 0.05) / fig.get_figheight(), 1, 1))\n"
            f"plt.savefig('{name}.png', dpi=150, bbox_inches='tight', transparent=True)\n"
            "plt.show()")


# ---------------------------------------------------------------- the Quantlets
def q_price_changes():
    q = Quantlet(4, "price_changes",
                 "Daily day-ahead base price of Romania (OPCOM) and its daily change X_t = P_t - P_(t-1), the risk factor of "
                 f"Lecture 4; {PER['price_changes']}. Prints the largest daily rise and fall.",
                 "electricity prices, day-ahead market, price changes, risk factor, volatility, Romania, OPCOM, time series",
                 f"power_da_prices_daily_cet.csv: daily day-ahead base prices of Romania, EUR/MWh, {SRC_EC} "
                 f"(cut-off {END})",
                 title="Daily price changes before and after 2021")
    q.code(SETUP).code(prices())
    q.md("## The risk factor\n\nPrices can be negative, so the lecture uses daily changes $X_t=P_t-P_{t-1}$ (EUR/MWh), "
         "not log returns. A buyer of a flat block budgeted at yesterday's price loses $X_t$ per MWh.")
    q.code(r"""x = X['RO'].dropna()
show('dist.RO.max', round(x.max(), 2))
show('dist.RO.max_date', d(x.idxmax()))
show('dist.RO.min', round(x.min(), 2))
show('dist.RO.min_date', d(x.idxmin()))""")
    q.code(r"""fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.2), sharex=True)
axs[0].plot(P.index, P['RO'], color=PAL['RO'], lw=0.6, label='Romania, daily base price $P_t$')
axs[0].set_ylabel('EUR/MWh', fontsize=10)
axs[1].plot(X.index, X['RO'], color=PAL['DE_LU'], lw=0.5, label='daily change $X_t = P_t - P_{t-1}$')
axs[1].set_ylabel('EUR/MWh', fontsize=10)
axs[1].xaxis.set_major_locator(mdates.YearLocator())
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
axs[1].tick_params(axis='x', labelsize=10)
legend_bottom(fig, ncol=2)
""" + save_cell("price_changes"))
    return q


def q_tails():
    q = Quantlet(4, "tails",
                 "Survival function (share of days with a rise larger than z standard deviations) of the standardised daily "
                 "changes of the day-ahead base price in Romania and Germany-Luxembourg against the normal distribution, log "
                 f"scale; {PER['tails']}. Prints excess kurtosis and the count of rises above 3 standard deviations.",
                 "heavy tails, kurtosis, normal distribution, survival function, electricity prices, Romania, Germany, extreme events",
                 "power_da_prices_daily_cet.csv: daily day-ahead base prices of Romania (OPCOM) and Germany-Luxembourg "
                 f"(EPEX SPOT), EUR/MWh, energy-charts.info (Fraunhofer ISE) via ENTSO-E (cut-off {END})",
                 title="Large price rises are far more frequent than the normal curve allows")
    q.code(SETUP).code(prices(("RO", "DE_LU")))
    q.md("## Heavy tails\n\nUnder normality a rise above $\\mu+3\\sigma$ has probability $1-\\Phi(3)\\approx 0.00135$; "
         "the survival curve of the data lies far above the normal curve.")
    q.code(r"""for z in ['RO', 'DE_LU']:
    show(f'dist.{z}.exkurt', round(stats.kurtosis(X[z].dropna()), 2))
x = X['RO'].dropna()
m, s = x.mean(), x.std()
zmax = (x.max() - m) / s
lp = stats.norm.logsf(zmax) / np.log(10)             # log10 P(Z > zmax) under normality
show('dist.RO.n_3sd_up', int((x > m + 3 * s).sum()))
show('dist.RO.exp_3sd', round(len(x) * stats.norm.sf(3), 2))
show('dist.RO.max_z', round(zmax, 1))
show('dist.RO.max_logyears', int(np.floor(-lp - np.log10(365.25))))""")
    q.code(r"""fig, ax = plt.subplots(figsize=(6.4, 2.3))
zz = np.linspace(0, 10, 200)
for z, ls, lab in [('RO', '-', 'Romania'), ('DE_LU', '--', 'Germany-Luxembourg')]:
    s_ = X[z].dropna()
    zs = np.sort(((s_ - s_.mean()) / s_.std()).values)
    surv = 1 - np.arange(1, len(zs) + 1) / (len(zs) + 1)
    sel = zs > 0
    ax.plot(zs[sel], surv[sel], color=PAL[z], ls=ls, lw=1.3, label=lab)
ax.plot(zz, stats.norm.sf(zz), color='#222222', lw=1.0, ls=':', label='normal distribution')
ax.set_yscale('log')
ax.set_ylim(1e-4, 1)
ax.set_xlim(0, 10)
ax.set_xlabel('size of the daily rise, in standard deviations')
ax.set_ylabel('share of days')
ax.set_yticks([1e-4, 1e-2, 1])
ax.set_yticks([1e-3, 1e-1], minor=True)
ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_yticklabels(['0.0001', '0.01', '1'])
legend_bottom(fig, ncol=3)
""" + save_cell("tails"))
    return q


def q_gpd_tail():
    q = Quantlet(4, "gpd_tail",
                 "Upper tail of the GARCH-filtered standardised residuals of the daily price change in Romania: empirical "
                 "exceedance probabilities above the 90% threshold, generalised Pareto fit and normal curve, log scale "
                 f"({PER['gpd_tail']}). Also refits the filter every 21 days from 2017-01-01 and prints the shape and "
                 "scale of the last refit and the share of refits with a positive shape.",
                 "extreme value theory, EVT, generalised Pareto distribution, peaks over threshold, GARCH, tail index, electricity prices, Romania",
                 f"power_da_prices_daily_cet.csv: daily day-ahead base prices of Romania, EUR/MWh, {SRC_EC} (cut-off {END})",
                 title="Above the threshold the Pareto curve follows the data; the normal curve does not")
    q.code(SETUP).code(prices()).code(ARCH)
    q.md("## Filter, then fit the tail\n\n$X_t=\\mu_{d(t)}+\\sigma_t z_t$: weekday mean $\\mu_d$, GARCH(1,1) volatility "
         "$\\sigma_t$, standardised residuals $z_t$. Above the threshold $u$ (90% quantile of $z$) the excesses follow a "
         "generalised Pareto distribution, $P(Z>z)=\\frac{N_u}{n}\\big(1+\\xi\\frac{z-u}{\\beta}\\big)^{-1/\\xi}$.")
    q.code(r"""T0, W_G, REFIT, U_EVT = pd.Timestamp('2017-01-01'), 730, 21, 0.90


def garch_filter(e):
    res = arch_model(e, mean='Zero', vol='GARCH', p=1, q=1, dist='normal', rescale=False).fit(disp='off')
    return np.asarray(res.conditional_volatility)


def gpd_tail(z, u_q=U_EVT):
    u = np.quantile(z, u_q)
    exc = z[z > u] - u
    xi, _, beta = stats.genpareto.fit(exc, floc=0)
    return u, xi, beta, len(exc), len(z)


def standardised(hist):
    # weekday-demeaned changes divided by their GARCH(1,1) volatility
    hw = hist[-W_G:]
    mdow = hw.groupby(hw.index.dayofweek).mean()
    e = (hw - mdow.reindex(hw.index.dayofweek).values).values
    return e / garch_filter(e)""")
    q.code(r"""# the refits of the rolling forecast: every 21 days from 2017-01-01, on the 730 changes before the refit day
refits = []
for t in pd.date_range(T0, END, freq='D')[::REFIT]:
    hist = X['RO'][:t - pd.Timedelta(days=1)].dropna()
    u, xi, beta, n_u, n = gpd_tail(standardised(hist))
    refits.append((d(t), xi, beta))
show('evt.refit_last', refits[-1][0])
show('evt.xi_last', round(refits[-1][1], 3))
show('evt.beta_last', round(refits[-1][2], 3))
show('evt.share_xi_pos', round(100 * np.mean([r[1] > 0 for r in refits]), 0))
print('number of refits:', len(refits))""")
    q.code(r"""# the chart: the filter fitted on the 730 changes before the cut-off
z = np.sort(standardised(X['RO'][:END - pd.Timedelta(days=1)].dropna()))
u, xi, beta, n_u, n = gpd_tail(z)
print(f'chart fit: u = {u:.3f}, xi = {xi:.3f}, beta = {beta:.3f}, {n_u} exceedances of {n}')
fig, ax = plt.subplots(figsize=(6.4, 2.4))
zt = z[z > u]
sv = 1 - np.searchsorted(z, zt, side='left') / len(z)
ax.scatter(zt, sv, s=7, color=PAL['RO'], label='residuals above $u$ (data)', zorder=3)
gx = np.linspace(u, zt.max() * 1.15, 200)
ax.plot(gx, (n_u / n) * stats.genpareto.sf(gx - u, xi, scale=beta), color=PAL['DE_LU'], lw=1.4,
        label='generalised Pareto fit')
ax.plot(gx, stats.norm.sf(gx), color='#222222', ls=':', lw=1.0, label='normal curve')
ax.set_yscale('log')
ax.set_xlim(u - 0.1, gx[-1] + 0.1)
ax.set_ylim(stats.norm.sf(gx[-1]) / 3, 0.3)
yt = [10.0 ** -k for k in range(1, 9, 2) if 10.0 ** -k >= stats.norm.sf(gx[-1]) / 3]
ax.set_yticks(yt)
ax.set_yticklabels([f'{v:.{k}f}' for v, k in zip(yt, range(1, 9, 2))])
ax.minorticks_off()
ax.set_xlabel('standardised residual $z$')
ax.set_ylabel('$P(Z > z)$')
legend_bottom(fig, ncol=3)
""" + save_cell("gpd_tail"))
    return q


def q_var_paths():
    q = Quantlet(4, "var_paths",
                 "Daily price change in Romania with the one-day-ahead 99% VaR of historical simulation (HS), the normal "
                 "model and filtered historical simulation (FHS), and the days the FHS VaR was exceeded, during the "
                 f"2021-2022 energy crisis ({PER['var_paths']}). Prints the number of exceedances of the five methods.",
                 KW_RISK + ", historical simulation, filtered historical simulation, GARCH, EVT, backtesting, energy crisis",
                 f"power_da_prices_daily_cet.csv: daily day-ahead base prices of Romania, EUR/MWh, {SRC_EC} (cut-off {END}); "
                 "the VaR forecasts are recomputed in the notebook",
                 title="In the crisis FHS adapted within days; HS and the normal VaR lagged")
    q.code(SETUP).code(prices()).code(ARCH).md(ENGINE_MD).code(ENGINE)
    q.code(r"""import time
t0 = time.time()
METHODS = ['hs', 'normal', 't', 'fhs', 'evt']
DAYS, OUT = var_engine(X['RO'], END, METHODS, (0.99,))
print(f'{len(DAYS)} daily forecasts in {time.time() - t0:.0f} s')
x = X['RO'].reindex(DAYS).values
HITS = {m: pd.Series(np.where(np.isnan(x), np.nan, (x > OUT[m][0.99]).astype(float)), index=DAYS) for m in METHODS}""")
    q.code(r"""a0, a1 = '2021-07-01', '2023-06-30'
for m in METHODS:
    show(f'vp.{m}', int(HITS[m][a0:a1].sum()))
n = int(HITS['hs'][a0:a1].notna().sum())
show('vp.n', n)
show('vp.exp', round(0.01 * n, 1))""")
    q.code(COLM + "\n" + MONTHS)
    q.code(r"""fig, ax = plt.subplots(figsize=(6.4, 2.6))
xs = X['RO'][a0:a1]
ax.plot(xs.index, xs.values, color='#bbbbbb', lw=0.5, label='daily change $X_t$')
for m in ['hs', 'normal', 'fhs']:
    v = pd.Series(OUT[m][0.99], index=DAYS)[a0:a1]
    ax.plot(v.index, v.values, color=COL[m], lw=0.9, label='99% VaR, ' + LAB[m])
hh = HITS['fhs'][a0:a1]
hd = hh[hh == 1].index
ax.scatter(hd, X['RO'].reindex(hd), s=9, color=PAL['c8'], zorder=4, label='exceedance of FHS VaR')
ax.set_ylabel('EUR/MWh')
ax.set_ylim(-180, 280)
month_axis(ax, 3)
legend_bottom(fig, ncol=3)
""" + save_cell("var_paths"))
    return q


def q_horizon():
    q = Quantlet(4, "horizon",
                 "Ratio of the empirical 99% quantile of h-day price changes to the 1-day one, h = 1 to 20, for Romania and "
                 f"Germany-Luxembourg, against the square-root-of-time rule sqrt(h); {PER['horizon']}. Prints the 10-day "
                 "ratios, the variance ratio and the autocorrelation of the daily change.",
                 "square-root-of-time rule, VaR horizon, mean reversion, variance ratio, autocorrelation, electricity prices, Romania, Germany",
                 "power_da_prices_daily_cet.csv: daily day-ahead base prices of Romania (OPCOM) and Germany-Luxembourg "
                 f"(EPEX SPOT), EUR/MWh, energy-charts.info (Fraunhofer ISE) via ENTSO-E (cut-off {END})",
                 title="The square-root-of-time rule overstates the 10-day risk")
    q.code(SETUP).code(prices(("RO", "DE_LU")))
    q.md("## Scaling the VaR to h days\n\nIf daily changes were independent, $\\mathrm{VaR}_h=\\sqrt h\\,\\mathrm{VaR}_1$. "
         "Electricity prices revert to their mean, so the empirical ratio $q_{0.99}(P_{t+h}-P_t)/q_{0.99}(P_{t+1}-P_t)$ "
         "grows much more slowly.")
    q.code(r"""HOR, VR = {}, {}
for z in ['RO', 'DE_LU']:
    p = P[z]
    q1 = (p.shift(-1) - p).dropna().quantile(0.99)
    v1 = (p.shift(-1) - p).var()
    HOR[z] = {h: (p.shift(-h) - p).dropna().quantile(0.99) / q1 for h in range(1, 21)}
    VR[z] = {h: (p.shift(-h) - p).var() / (h * v1) for h in range(1, 21)}
show('horizon.ro10', round(HOR['RO'][10], 2))
show('horizon.de10', round(HOR['DE_LU'][10], 2))
show('horizon.sqrt10', round(np.sqrt(10), 2))
show('horizon.vr10_ro', round(VR['RO'][10], 2))
show('horizon.ac1_ro', round(X['RO'].autocorr(1), 3))
show('horizon.ac7_ro', round(X['RO'].autocorr(7), 3))""")
    q.code(r"""fig, ax = plt.subplots(figsize=(6.4, 2.3))
hs = list(range(1, 21))
ax.plot(hs, np.sqrt(hs), color='#222222', ls=':', lw=1.2, label='square-root-of-time rule')
ax.plot(hs, [HOR['RO'][h] for h in hs], color=PAL['RO'], marker='o', ms=3, lw=1.2, label='Romania (data)')
ax.plot(hs, [HOR['DE_LU'][h] for h in hs], color=PAL['DE_LU'], marker='s', ms=3, lw=1.2, ls='--',
        label='Germany-Luxembourg (data)')
ax.set_xticks([1, 5, 10, 15, 20])
ax.set_xlabel('horizon $h$ (days)')
ax.set_ylabel('$h$-day / 1-day\n99% quantile', fontsize=10)
ax.set_ylim(0.8, 4.8)
legend_bottom(fig, ncol=3)
""" + save_cell("horizon"))
    return q


def q_traffic():
    q = Quantlet(4, "traffic",
                 "Basel traffic light for the one-day 99% VaR of the daily price change in Romania: rolling count of "
                 "exceedances in the last 250 days for historical simulation, normal, Student-t, filtered historical "
                 f"simulation and EVT, with the green, yellow and red zones ({PER['traffic']}). Prints the share of days in "
                 "the red zone and the zone probabilities of a correct model.",
                 KW_RISK + ", backtesting, Basel traffic light, exceedances, binomial distribution, BCBS",
                 f"power_da_prices_daily_cet.csv: daily day-ahead base prices of Romania, EUR/MWh, {SRC_EC} (cut-off {END}); "
                 "the VaR forecasts are recomputed in the notebook",
                 title="The Basel traffic light for five VaR models")
    q.code(SETUP).code(prices()).code(ARCH).md(ENGINE_MD).code(ENGINE)
    q.code(r"""import time
t0 = time.time()
METHODS = ['hs', 'normal', 't', 'fhs', 'evt']
DAYS, OUT = var_engine(X['RO'], END, METHODS, (0.99,))
print(f'{len(DAYS)} daily forecasts in {time.time() - t0:.0f} s')
x = X['RO'].reindex(DAYS).values
HITS = {m: pd.Series(np.where(np.isnan(x), np.nan, (x > OUT[m][0.99]).astype(float)), index=DAYS) for m in METHODS}""")
    q.md("## Traffic light\n\nOver 250 days a correct 99% model has $K\\sim\\mathrm{Bin}(250,0.01)$ exceedances: "
         "green for $K\\le4$, yellow for $5\\le K\\le9$, red for $K\\ge10$ (BCBS, 1996).")
    q.code(r"""show('basel.p_green', round(100 * stats.binom.cdf(4, 250, 0.01), 2))
show('basel.p_red', round(100 * stats.binom.sf(9, 250, 0.01), 3))
C250 = {}
for m in METHODS:
    C250[m] = HITS[m].fillna(0).rolling(250).sum()
    c = C250[m].iloc[249:]
    show(f'bt.RO.{m}.a99.share_red', round(100 * (c >= 10).mean(), 1))""")
    q.code(COLM)
    q.code(r"""fig, ax = plt.subplots(figsize=(6.4, 2.3))
for m in METHODS:
    ax.plot(C250[m].index, C250[m].values, color=COL[m], lw=1.0, label=LAB[m])
ax.axhspan(-0.5, 4.5, color=PAL['c6'], alpha=0.10, lw=0)
ax.axhspan(4.5, 9.5, color=PAL['BG'], alpha=0.15, lw=0)
ax.axhspan(9.5, 40, color=PAL['c8'], alpha=0.10, lw=0)
ytop = max(25, max(C250[m].max() for m in METHODS) + 2)
tr = ax.get_yaxis_transform()           # x in axes units, y in data units: zone names in the right margin
for y, lab, c in [(2, 'green', PAL['c6']), (7, 'yellow', '#9a6a00'), ((9.5 + ytop) / 2, 'red', PAL['c8'])]:
    ax.text(1.01, y, lab, transform=tr, fontsize=9.5, color=c, va='center', ha='left', clip_on=False)
ax.set_xlim(DAYS[249] - pd.Timedelta(days=30), DAYS[-1] + pd.Timedelta(days=30))
ax.set_ylim(0, ytop)
ax.set_ylabel('exceedances,\nlast 250 days', fontsize=10)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_bottom(fig, ncol=5)
""" + save_cell("traffic"))
    return q


def q_brent_im():
    q = Quantlet(4, "brent_im",
                 "Initial margin of one ICE Brent futures lot (1,000 barrels) computed as a 99% two-day historical-simulation "
                 "VaR with a 12-month lookback, and with an anti-procyclical floor (lookback since 2015), EMIR RTS 153/2013 "
                 f"Art. 24-28; {PER['brent_im']}. Prints the 2026 rise of price and margin and the share of days with "
                 "losses beyond the margin.",
                 "initial margin, collateral, procyclicality, EMIR, CCP, Brent, futures, historical simulation, value at risk",
                 "fuels_daily.csv: daily settlement of the ICE Brent front-month futures (BZ=F), USD/bbl, Yahoo Finance "
                 f"(cut-off {END})",
                 title="Margins are procyclical: the Brent initial margin in 2026")
    q.code(SETUP)
    q.code(r"""# ICE Brent front-month futures (continuous series, rolls on the first trading day of each month), USD/bbl
F = pd.read_csv(DATA + 'fuels_daily.csv', parse_dates=['date']).set_index('date')['brent_usd_bbl'].dropna()
END = pd.Timestamp('@END@')
F = F[:END]
print('Brent', d(F.index[0]), 'to', d(F.index[-1]), len(F), 'trading days')""".replace("@END@", END))
    q.md("## Initial margin as a 2-day 99% VaR\n\n$\\mathrm{IM}_t = 1000\\cdot F_t\\cdot q_{0.99}\\big(|F_s/F_{s-2}-1|\\big)$ "
         "over the last 250 trading days (or since 2015 for the floor). Two-day windows that contain a contract roll are "
         "dropped, so a cross-contract jump is never counted as a price move.")
    q.code(r"""ym = F.index.to_period('M')
roll = pd.Series(np.r_[False, ym[1:] != ym[:-1]], index=F.index)     # first trading day of each month
r2 = F / F.shift(2) - 1
r2[(roll | roll.shift(1, fill_value=False))] = np.nan                  # 2-day windows with a roll dropped
LOT = 1000
absr = r2.abs()
IM1 = LOT * F * absr.rolling(250, min_periods=200).quantile(0.99)      # 12-month lookback
IML = LOT * F * absr.expanding(min_periods=250).quantile(0.99)         # lookback since 2015
IMA = np.maximum(IM1, IML)                                             # with the anti-procyclical floor
im = pd.DataFrame({'im1': IM1, 'ima': IMA, 'F': F})['2016-01-01':]
# coverage: loss over the next two trading days (either side) against the margin
fut2 = (F.shift(-2) - F).abs() * LOT
fut2[(roll.shift(-1, fill_value=False) | roll.shift(-2, fill_value=False))] = np.nan
cov = pd.DataFrame({'l': fut2, 'im1': IM1, 'ima': IMA}).dropna()['2016-01-01':]

s26 = im['2026-01-01':'2026-06-30']
pre26 = im['2026-02-27':].iloc[0]
show('brent.F_pre26', round(F['2026-02-27'], 2))
show('brent.F_max26', round(F['2026-03-01':'2026-06-30'].max(), 2))
show('brent.F_max26_date', d(F['2026-03-01':'2026-06-30'].idxmax()))
show('brent.im1_pre26', round(pre26['im1'], 0))
show('brent.im1_max26', round(s26['im1'].max(), 0))
show('brent.ratio26', round(s26['im1'].max() / pre26['im1'], 2))
show('brent.ratio26_apc', round(s26['ima'].max() / pre26['ima'], 2))
show('brent.exc1', round(100 * (cov['l'] > cov['im1']).mean(), 2))
show('brent.exca', round(100 * (cov['l'] > cov['ima']).mean(), 2))""")
    q.code(r"""fig, ax = plt.subplots(figsize=(6.4, 2.2))
ax.plot(im.index, im['im1'] / 1000, color=PAL['RO'], lw=1.0, label='99% 2-day HS, 12-month lookback')
ax.plot(im.index, im['ima'] / 1000, color=PAL['DE_LU'], lw=1.0, ls='--', label='floor: lookback since 2015 (anti-procyclical)')
ax.set_ylabel('IM, thousand\nUSD per lot', fontsize=10)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_bottom(fig, ncol=2)
""" + save_cell("brent_im"))
    return q


def q_coverage():
    q = Quantlet(4, "coverage",
                 "Coverage of the 99% quantile forecast of the next day's base price in Romania, used to size the OPCOM "
                 "day-ahead guarantee: share of days with the price below the forecast in 2017-2020, 2021-2022 and "
                 "2023-2026 for quantile regression, quantile regression with conformal widening and FHS (previous price plus "
                 f"99% VaR); {PER['coverage']}. Prints the coverage and the Kupiec test p-values.",
                 "quantile regression, conformal prediction, collateral, guarantee, coverage, Kupiec test, filtered historical simulation, electricity prices, Romania",
                 f"power_da_prices_daily_cet.csv: daily day-ahead base prices of Romania, EUR/MWh, {SRC_EC} (cut-off {END}); "
                 "the quantile regressions and the FHS forecasts are recomputed in the notebook",
                 title="Widening the tails brings the 99% quantile close to its promise")
    q.code(SETUP).code(prices()).code(ARCH).md(ENGINE_MD).code(ENGINE)
    q.md("## Quantile forecasts of tomorrow's price\n\n$\\hat q_{\\tau,t}=\\beta_0+\\beta_1P_{t-1}+\\beta_2P_{t-7}+\\sum_j"
         "\\delta_jD_{j,t}$ fitted on the last 365 days (one regression per day, from 2016), widened by the "
         "$\\tau$-quantile of the last 365 out-of-sample errors (one-sided conformal correction).")
    q.code(QR)
    q.code(r"""import time
t0 = time.time()
TAUS = (0.95, 0.99)
QD = pd.date_range('2016-01-01', END, freq='D')
rr = [qr_forecast(t, TAUS) for t in QD]
QRF = pd.DataFrame({tau: [r[tau] for r in rr] for tau in TAUS}, index=QD)
print(f'{len(QD)} days x 2 quantile regressions in {time.time() - t0:.0f} s')
t0 = time.time()
DAYS, OUT = var_engine(X['RO'], END, ['fhs'], TAUS)
print(f'FHS forecasts in {time.time() - t0:.0f} s')""")
    q.code(KUPIEC)
    q.code(r"""PERIODS = [('calm', '2017-01-01', '2020-12-31'), ('crisis', '2021-01-01', '2022-12-31'), ('after', '2023-01-01', d(END))]
GUAR = {}
for tau in TAUS:
    a = 'a95' if tau == 0.95 else 'a99'
    fhs_q = PR.shift(1).reindex(DAYS) + pd.Series(OUT['fhs'][tau], index=DAYS)
    df = pd.DataFrame({'p': PR.reindex(DAYS), 'qr': QRF[tau].reindex(DAYS), 'cqr': conformal(QRF[tau], tau).reindex(DAYS),
                       'fhs': fhs_q}).dropna()
    GUAR[a] = {}
    for k in ['qr', 'cqr', 'fhs']:
        g = {'cov': 100 * (df['p'] <= df[k]).mean(), 'kupiec_p': kupiec((df['p'] > df[k]).astype(int).values, 1 - tau)[1]}
        for lab, b0, b1 in PERIODS:
            g['cov_' + lab] = 100 * (df[b0:b1]['p'] <= df[b0:b1][k]).mean()
        GUAR[a][k] = g
for k in ['qr', 'cqr', 'fhs']:
    for lab in ['calm', 'crisis', 'after']:
        show(f'guar.a99.{k}.cov_{lab}', round(GUAR['a99'][k]['cov_' + lab], 2))
for k in ['qr', 'cqr', 'fhs']:
    show(f'guar.a99.{k}.kupiec_p', round(GUAR['a99'][k]['kupiec_p'], 4))
show('guar.a95.cqr.kupiec_p', round(GUAR['a95']['cqr']['kupiec_p'], 4))""")
    q.code(r"""fig, ax = plt.subplots(figsize=(6.4, 2.3))
ww = 0.26
for j, (k, lab, c) in enumerate([('qr', 'quantile regression', PAL['BG']), ('cqr', '+ conformal widening', PAL['RO']),
                                  ('fhs', 'FHS', PAL['DE_LU'])]):
    ax.bar(np.arange(3) + (j - 1) * ww, [GUAR['a99'][k]['cov_' + p[0]] for p in PERIODS], width=ww, color=c, label=lab)
ax.axhline(99, color='#222222', lw=0.9, ls=':', label='target 99%')
ax.set_xticks(range(3))
ax.set_xticklabels(['2017-2020', '2021-2022', '2023-' + str(END.year)])
ax.set_ylim(90, 100.5)
ax.set_ylabel('coverage, % of days', fontsize=10)
legend_bottom(fig, ncol=4)
""" + save_cell("coverage"))
    return q


def q_supplier_month():
    q = Quantlet(4, "supplier_month",
                 "Monthly change of the load-weighted day-ahead price in Romania (the cost overrun of a supplier that "
                 "budgets each month at last month's price) against the normal 99% limit estimated on 2015-2020 data; "
                 f"months above the limit in red; {PER['supplier_month']}. Prints the exceedances since 2021 and the worst month.",
                 "supplier risk, procurement cost, load-weighted price, risk limit, normal distribution, electricity prices, Romania, Transelectrica",
                 "power_da_prices_hourly_utc.csv: hourly day-ahead prices of Romania (OPCOM), EUR/MWh, and "
                 "generation_ro_mw_hourly_utc.csv: hourly national load of Romania (Transelectrica via ENTSO-E), MW, "
                 f"both from energy-charts.info (Fraunhofer ISE) (cut-off {END})",
                 title="Since 2021 the normal 99% monthly limit was exceeded more often than expected")
    q.code(SETUP)
    q.code(r"""END = pd.Timestamp('@END@')     # cut-off of Lecture 4
# hourly day-ahead prices of Romania (15-min prices averaged to the hour from October 2025) and hourly national load
HP = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', usecols=['timestamp_utc', 'RO'], parse_dates=['timestamp_utc']).set_index('timestamp_utc')['RO']
GL = pd.read_csv(DATA + 'generation_ro_mw_hourly_utc.csv', usecols=['timestamp_utc', 'load'], parse_dates=['timestamp_utc']).set_index('timestamp_utc')['load']
HP.index = pd.to_datetime(HP.index, utc=True)
GL.index = pd.to_datetime(GL.index, utc=True)
hl = pd.DataFrame({'p': HP, 'l': GL}).dropna()
hl['m'] = hl.index.tz_convert('Europe/Brussels').tz_localize(None).to_period('M')
print(len(hl), 'hours with both price and load')""".replace("@END@", END))
    q.md("## A supplier's monthly cost overrun\n\nLoad-weighted price $\\bar P^{L}_m=\\sum_h P_hL_h/\\sum_h L_h$; cost overrun "
         "$o_m=\\bar P^{L}_m/\\bar P^{L}_{m-1}-1$. The limit is $\\hat\\mu+\\Phi^{-1}(0.99)\\,\\hat\\sigma$ from the months "
         "up to December 2020.")
    q.code(r"""mon = hl.groupby('m').apply(lambda g: pd.Series({'lwp': (g.p * g.l).sum() / g.l.sum(), 'hours': len(g)}))
mon = mon[(mon.index >= pd.Period('2015-02', 'M')) & (mon.index <= pd.Period(END, 'M'))]
mon['o'] = mon['lwp'] / mon['lwp'].shift(1) - 1
mon = mon.dropna()
o_pre = mon['o'][mon.index <= pd.Period('2020-12', 'M')]
lim_o = o_pre.mean() + stats.norm.ppf(0.99) * o_pre.std()
post = mon[mon.index >= pd.Period('2021-01', 'M')]
print('months', mon.index[0], 'to', mon.index[-1])
show('supplier.lim99', round(100 * lim_o, 1))
show('supplier.exc99_post', int((post['o'] > lim_o).sum()))
show('supplier.exp99_post', round(0.01 * len(post), 2))
show('supplier.worst', str(mon['o'].idxmax()))
show('supplier.worst_pct', round(100 * mon['o'].max(), 1))""")
    q.code(r"""fig, ax = plt.subplots(figsize=(6.4, 2.2))
xm = mon.index.to_timestamp()
above = (mon['o'] > lim_o).values
ax.bar(xm[~above], 100 * mon['o'][~above], width=22, color=PAL['RO'], label='cost overrun: monthly change of the load-weighted price')
ax.bar(xm[above], 100 * mon['o'][above], width=22, color=PAL['c8'], label='above the limit')
ax.axhline(100 * lim_o, color='#222222', lw=0.9, ls='--', label='normal 99% limit, 2015-2020 data')
ax.set_ylabel('%')
ax.tick_params(axis='x', labelsize=10)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_bottom(fig, ncol=2)
""" + save_cell("supplier_month"))
    return q


def q_case2026():
    q = Quantlet(4, "case2026",
                 "Case study, autumn 2026: daily base price in Romania with the previous price plus the one-day 99% VaR of "
                 "historical simulation and filtered historical simulation, the conformal 99% guarantee limit and the "
                 f"days with an FHS exceedance; {PER['case2026']}. Prints the monthly mean prices, the peak and the number "
                 "of 99% VaR exceedances.",
                 KW_RISK + ", case study, price rise, filtered historical simulation, quantile regression, guarantee",
                 f"power_da_prices_daily_cet.csv: daily day-ahead base prices of Romania, EUR/MWh, {SRC_EC} (cut-off {END}); "
                 "the VaR and quantile forecasts are recomputed in the notebook",
                 title="Case study: in 2026 the price doubled gradually, without jumps")
    q.code(SETUP).code(prices()).code(ARCH).md(ENGINE_MD).code(ENGINE).code(QR)
    q.code(r"""import time
t0 = time.time()
METHODS = ['hs', 'normal', 'fhs']
DAYS, OUT = var_engine(X['RO'], END, METHODS, (0.99,))
x = X['RO'].reindex(DAYS).values
HITS = {m: pd.Series(np.where(np.isnan(x), np.nan, (x > OUT[m][0.99]).astype(float)), index=DAYS) for m in METHODS}
# quantile regressions from January 2025: the conformal correction of June-October 2026 uses the 365 days before
QD = pd.date_range('2025-01-01', END, freq='D')
QRF = pd.Series([qr_forecast(t, (0.99,))[0.99] for t in QD], index=QD)
CQR = conformal(QRF, 0.99)
print(f'forecasts in {time.time() - t0:.0f} s')""")
    q.code(r"""C0 = pd.Timestamp('2026-06-01')
show('case.p_jun', round(PR['2026-06'].mean(), 2))
show('case.p_oct', round(PR['2026-10'].mean(), 2))
show('case.p_max', round(PR[C0:END].max(), 2))
show('case.p_max_date', d(PR[C0:END].idxmax()))
n = int(X['RO'][C0:END].notna().sum())
show('case.n', n)
show('case.exp99', round(0.01 * n, 2))
for m in METHODS:
    show(f'case.{m}.x99', int(HITS[m][C0:END].dropna().sum()))""")
    q.code(COLM + "\n" + MONTHS)
    q.code(r"""fig, ax = plt.subplots(figsize=(6.4, 2.3))
cc = pd.date_range(C0, END, freq='D')
ax.plot(cc, PR.reindex(cc), color='#222222', lw=1.2, label='base price $P_t$')
for m, ls in [('hs', '--'), ('fhs', '-')]:
    band = PR.shift(1).reindex(cc) + pd.Series(OUT[m][0.99], index=DAYS).reindex(cc)
    ax.plot(cc, band, color=COL[m], lw=1.0, ls=ls, label='P(t-1) + 99% VaR, ' + LAB[m])
ax.plot(cc, CQR.reindex(cc), color=PAL['HU'], lw=0.9, ls='-.', label='guarantee limit (conformal 99%)')
hd = HITS['fhs'].reindex(cc)
hd = hd[hd == 1].index
ax.scatter(hd, PR.reindex(hd), s=14, color=PAL['c8'], zorder=4, label='FHS exceedance')
ax.set_ylabel('EUR/MWh')
month_axis(ax)
legend_bottom(fig, ncol=3)
""" + save_cell("case2026"))
    return q


BUILDERS = {"price_changes": q_price_changes, "tails": q_tails, "gpd_tail": q_gpd_tail, "var_paths": q_var_paths,
            "horizon": q_horizon, "traffic": q_traffic, "brent_im": q_brent_im, "coverage": q_coverage,
            "supplier_month": q_supplier_month, "case2026": q_case2026}


# ---------------------------------------------------------------- check: printed numbers = L4_numbers.json
def lookup(key):
    v = N
    for p in key.split("."):
        v = v[p]
    return v


def check(q):
    nb = nbformat.read(os.path.join(q.folder, q.name + ".ipynb"), as_version=4)
    bad, n = [], 0
    for c in nb.cells:
        for o in c.get("outputs", []):
            for line in o.get("text", "").splitlines():
                m = re.match(r"^(\S+)\s+= (.*)$", line)
                if not m:
                    continue
                key, val = m.group(1), m.group(2).strip()
                ref = lookup(key)
                n += 1
                if isinstance(ref, str):
                    ok = val == ref
                else:
                    ok = abs(float(val) - float(ref)) < 1e-6
                if not ok:
                    bad.append(f"{key}: notebook {val}, L4_numbers.json {ref}")
    return n, bad


if __name__ == "__main__":
    names = sys.argv[1:] or list(BUILDERS)
    problems = {}
    for name in names:
        q = BUILDERS[name]()
        q.write(execute=True)
        n, bad = check(q)
        print(f"  {n} numbers checked against L4_numbers.json" + ("" if not bad else ": MISMATCH " + "; ".join(bad)))
        if bad:
            problems[name] = bad
    if problems:
        sys.exit("number mismatches: " + json.dumps(problems, indent=1))
    print("all", len(names), "Quantlets written, executed and checked")
