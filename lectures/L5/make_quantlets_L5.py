"""
make_quantlets_L5.py -- one Quantlet per chart of Lecture 5 "Energy derivatives and hedging" (EMQA)
=================================================================================================
Writes Quantlets/L5/EMQA_L5_<chart>/ (Metainfo.txt, executed notebook, <chart>.png) for every chart of the L5 deck,
with the helper lectures/common/emqa_quantlet.py. Each notebook is self-contained: it reads only the data it needs
from DATA (data/clean of a local copy, or the public repository), repeats only the code of analysis_L5.py needed for
its chart, prints the numbers shown on the slide and draws the chart with the English labels.

After execution, every number printed with its JSON key ([key]) is compared with lectures/L5/L5_numbers.json;
the script fails on any mismatch.

Run:  python3 lectures/L5/make_quantlets_L5.py            (all charts)
      python3 lectures/L5/make_quantlets_L5.py premium    (one or more charts)
"""
import json
import os
import re
import sys

import nbformat

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_quantlet import Quantlet  # noqa: E402

N = json.load(open(os.path.join(HERE, "L5_numbers.json"), encoding="utf-8"))
END = N["cutoff"]["end"]

# ---------------------------------------------------------------------------------------------------------------
# cells shared by several notebooks
# ---------------------------------------------------------------------------------------------------------------
STYLE = r'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings('ignore')

# course chart style: transparent background, no gridlines, legend at the bottom outside the axes
plt.rcParams.update({
    'figure.facecolor': 'none', 'axes.facecolor': 'none', 'savefig.transparent': True,
    'axes.grid': False, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.edgecolor': '#222222', 'axes.labelcolor': '#222222', 'xtick.color': '#222222', 'ytick.color': '#222222',
    'text.color': '#222222', 'font.size': 11, 'axes.labelsize': 11, 'legend.fontsize': 10.5,
    'legend.frameon': False, 'lines.linewidth': 1.4, 'font.family': 'DejaVu Sans'})
# fixed colour per entity (course palette)
PAL = {'RO': '#2a78d6', 'DE_LU': '#eb6834', 'HU': '#1baf7a', 'BG': '#eda100',
       'c5': '#e87ba4', 'c6': '#008300', 'c7': '#6250d6', 'c8': '#e34948'}


def legend_bottom(fig, handles=None, labels=None, ncol=4):
    """Legend centred under the axes, outside the plotting area."""
    if handles is None:
        handles, labels = [], []
        for ax in fig.axes:
            for h, l in zip(*ax.get_legend_handles_labels()):
                if l not in labels:
                    handles.append(h)
                    labels.append(l)
    fig.legend(handles, labels, loc='lower center', ncol=ncol, bbox_to_anchor=(0.5, 0.0),
               frameon=False, handlelength=2.0, columnspacing=1.2)


def legend_compact(fig, ncol):
    """Bottom legend with shorter handles and column gaps, for many short entries."""
    legend_bottom(fig, ncol=ncol)
    h, l = fig.legends[-1].legend_handles, [t.get_text() for t in fig.legends[-1].get_texts()]
    fig.legends[-1].remove()
    fig.legend(h, l, loc='lower center', ncol=ncol, bbox_to_anchor=(0.5, 0.0), frameon=False,
               handlelength=1.0, handletextpad=0.4, columnspacing=0.9)


def save_chart(fig, name):
    """Keep under the axes exactly the height of the bottom legend, then save the PNG."""
    fig.canvas.draw()
    bottom = max([lg.get_window_extent().height / fig.bbox.height + 0.035 for lg in fig.legends] or [0.0])
    fig.tight_layout(rect=(0, bottom, 1, 1))
    plt.savefig(name + '.png', dpi=150, bbox_inches='tight', transparent=True)
    plt.show()


def show(label, value, key=None, fmt='.2f'):
    """Print one number of the slide; [key] = its name in lectures/L5/L5_numbers.json."""
    s = value if isinstance(value, str) else format(value, fmt)
    print(f'{label:<58s} {s:>12s}' + (f'   [{key}]' if key else ''))'''

LOAD_PD = r'''# daily day-ahead base prices (mean of all market time units of the CET/CEST day), EUR/MWh
PD = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')
# cut-off = last complete month of the Romanian series
_last = PD['RO'].dropna().index.max()
END = pd.Timestamp(((_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())
d = lambda ts: pd.Timestamp(ts).strftime('%Y-%m-%d')
print('cut-off (last complete month):', d(END))'''

LOAD_FW = r'''# OPCOM PCCB-LE-flex auction results: one row per traded session, price converted to EUR with the ECB EUR/RON fixing
FW = pd.read_csv(DATA + 'opcom_forward_trades.csv', parse_dates=['auction_date', 'delivery_start', 'delivery_end'])
FW = FW[FW['auction_date'] <= END].copy()


def kind_of(s, e):
    """Standard delivery period of a product: M (month), Q (quarter), H (half-year), Y (calendar year), else 'other'."""
    if s.day != 1 or (e + pd.Timedelta(days=1)).day != 1:
        return 'other'
    n = (e.year - s.year) * 12 + e.month - s.month + 1
    if n == 1:
        return 'M'
    if n == 3 and s.month in (1, 4, 7, 10):
        return 'Q'
    if n == 6 and s.month in (1, 7):
        return 'H'
    if n == 12 and s.month == 1:
        return 'Y'
    return 'other'


FW['kind'] = [kind_of(s, e) for s, e in zip(FW['delivery_start'], FW['delivery_end'])]
FW['lead_m'] = ((FW['delivery_start'].dt.year - FW['auction_date'].dt.year) * 12 +
                FW['delivery_start'].dt.month - FW['auction_date'].dt.month)
# baseload ('banda LD') products with a standard delivery period
BASE = FW[(FW['profile'] == 'banda LD') & (FW['kind'] != 'other')].copy()


def vwap(df):
    """Volume-weighted average price, EUR/MWh."""
    return float(np.average(df['price_eur_mwh'], weights=df['mwh'])) if len(df) else np.nan


def realised(s, e, col='RO'):
    """Mean day-ahead base price over [s, e] (CET days); NaN unless every day is present."""
    x = PD.loc[s:e, col]
    full = len(x) == (e - s).days + 1 and x.notna().all()
    return float(x.mean()) if full else np.nan


print(len(FW), 'traded auctions from', d(FW['auction_date'].min()), 'to', d(FW['auction_date'].max()),
      '|', len(BASE), 'baseload auctions with a standard delivery period')'''

CY_CELL = r'''# calendar-year baseload products
CY = BASE[BASE['kind'] == 'Y'].copy()
CY['dy'] = CY['delivery_start'].dt.year'''

PREMIUM_TABLE = r'''def premium_table(base):
    """Ex-post forward premium of every baseload product fully delivered by the cut-off: F - realised mean spot."""
    b = base[base['delivery_end'] <= END].copy()
    b['S'] = [realised(s, e) for s, e in zip(b['delivery_start'], b['delivery_end'])]
    b = b.dropna(subset=['S'])
    b['prem'] = b['price_eur_mwh'] - b['S']
    b['lr'] = np.log(b['S'] / b['price_eur_mwh'])
    b['T'] = ((b['delivery_start'] + (b['delivery_end'] - b['delivery_start']) / 2) - b['auction_date']).dt.days / 365.25
    return b


PT = premium_table(BASE)
# monthly products traded in the month before delivery
M1 = PT[(PT['kind'] == 'M') & (PT['lead_m'] == 1)]'''

MONTHLY_PM = r'''# monthly mean day-ahead prices, kept only for months with every day present
m_idx = pd.date_range('2015-01-01', END.replace(day=1), freq='MS')
PM = PD[['RO', 'HU', 'DE_LU']].resample('MS').mean().reindex(m_idx)
NDM = PD[['RO', 'HU', 'DE_LU']].resample('MS').count().reindex(m_idx)
PM = PM.where(NDM.eq(pd.Series(m_idx.days_in_month, index=m_idx), axis=0))'''

FUEL_COST = r'''# technical assumptions (stated on the slides)
ETA_GAS, ETA_COAL = 0.50, 0.38        # efficiency of a combined-cycle gas plant and of a hard-coal plant
EF_GAS, EF_COAL = 0.202, 0.341        # t CO2 per MWh thermal (IPCC 2006: 56.1 and 94.6 t CO2/TJ)
COAL_MWH_T = 6.978                    # MWh thermal per tonne of 6000 kcal/kg coal (6000*4.1868/3600)

# gas: TTF monthly (World Bank), EUR/MWh
TTFM = pd.read_csv(DATA + 'ttf_monthly.csv')
TTFM.index = pd.PeriodIndex(TTFM['month'], freq='M').to_timestamp()
GAS = TTFM['ttf_eur_mwh'].reindex(m_idx)
# carbon: EEX primary-auction EUA price (monthly mean); SparkChange ETC proxy after the last EEX month
EUA = pd.read_csv(DATA + 'eua_daily.csv', parse_dates=['date']).set_index('date')
eua_a = EUA['eua_eex_auction_eur_t'].dropna().resample('MS').mean()
eua_e = EUA['eua_etc_co2l_eur_per_unit'].dropna().resample('MS').mean()
EUAM = eua_a.reindex(m_idx).fillna(eua_e.reindex(m_idx).where(m_idx > eua_a.index.max()))
print('EUA: EEX auctions to', eua_a.index.max().strftime('%Y-%m'), '; ETC proxy afterwards')'''


def hedge_code():
    return r'''import statsmodels.api as sm
SEED = 20261106


def hedge_ratio(dS, dF, B=2000, block=6, seed=SEED):
    """h* = Cov(dS, dF)/Var(dF) by OLS; HAC (Newey-West, 3 lags) standard error; moving-block bootstrap 95% interval."""
    X = sm.add_constant(dF.values)
    r = sm.OLS(dS.values, X).fit(cov_type='HAC', cov_kwds={'maxlags': 3})
    rng = np.random.default_rng(seed)
    n = len(dS)
    hs = []
    for _ in range(B):
        idx = np.concatenate([np.arange(s, s + block) for s in rng.integers(0, n - block + 1, size=n // block + 1)])[:n]
        a, b = dS.values[idx], dF.values[idx]
        hs.append(np.cov(a, b)[0, 1] / np.var(b, ddof=1))
    lo, hi = np.percentile(hs, [2.5, 97.5])
    return {'h': float(r.params[1]), 'se': float(r.bse[1]), 'lo': float(lo), 'hi': float(hi), 'r2': float(r.rsquared),
            'rho': float(np.corrcoef(dS, dF)[0, 1]), 'n': int(n)}


dP = PM.diff().dropna()          # monthly changes of the monthly mean prices
HR = {}
for z in ['HU', 'DE_LU']:
    HR[z] = hedge_ratio(dP['RO'], dP[z])
    ins, oos = dP.loc[:'2020-12-01'], dP.loc['2021-01-01':]
    h_in = hedge_ratio(ins['RO'], ins[z])          # estimated on 2015-2020, applied from 2021
    v0 = oos['RO'].var()
    HR[z]['h_in'] = h_in['h']
    HR[z]['vr_oos_h'] = 100 * (1 - (oos['RO'] - h_in['h'] * oos[z]).var() / v0)
    HR[z]['vr_oos_1'] = 100 * (1 - (oos['RO'] - oos[z]).var() / v0)

print('monthly changes', dP.index.min().strftime('%Y-%m'), 'to', dP.index.max().strftime('%Y-%m'), '; n =', len(dP))
for z, nm in [('HU', 'Hungary'), ('DE_LU', 'Germany')]:
    show(f'{nm}: h*', HR[z]['h'], f'hedge.{z}.h', '.3f')
    show(f'{nm}: HAC standard error', HR[z]['se'], f'hedge.{z}.se', '.3f')
    show(f'{nm}: bootstrap 95% lower bound', HR[z]['lo'], f'hedge.{z}.lo', '.2f')
    show(f'{nm}: bootstrap 95% upper bound', HR[z]['hi'], f'hedge.{z}.hi', '.2f')
    show(f'{nm}: R2 (hedge effectiveness)', HR[z]['r2'], f'hedge.{z}.r2', '.2f')
    show(f'{nm}: h* estimated on 2015-2020', HR[z]['h_in'], f'hedge.{z}.h_in', '.2f')
    show(f'{nm}: variance removed from 2021 with that h*, %', HR[z]['vr_oos_h'], f'hedge.{z}.vr_oos_h', '.1f')
    show(f'{nm}: variance removed from 2021 with h = 1, %', HR[z]['vr_oos_1'], f'hedge.{z}.vr_oos_1', '.1f')'''


BLACK76 = r'''from scipy.stats import norm


def black76(F, K, T, r, sigma, kind='call'):
    """Black (1976) price of a European option on a forward F; returns price, delta, vega (per 1 vol point), d1, d2."""
    d1 = (np.log(F / K) + 0.5 * sigma ** 2 * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    disc = np.exp(-r * T)
    if kind == 'call':
        p, delta = disc * (F * norm.cdf(d1) - K * norm.cdf(d2)), disc * norm.cdf(d1)
    else:
        p, delta = disc * (K * norm.cdf(-d2) - F * norm.cdf(-d1)), -disc * norm.cdf(-d1)
    vega = disc * F * norm.pdf(d1) * np.sqrt(T) / 100
    return float(p), float(delta), float(vega), float(d1), float(d2)


# euro short-term rate (ECB)
RATES = pd.read_csv(DATA + 'ecb_ron_estr_daily.csv', parse_dates=['date']).set_index('date')'''


def save_cell(chart, bottom=None):
    return f"save_chart(fig, '{chart}')"


C = N["charts"]
DFW = ("OPCOM PCCB-LE-flex forward auction results (data/clean/opcom_forward_trades.csv, prices in EUR via the ECB EUR/RON "
       "fixing) and OPCOM day-ahead (PZU) daily base prices via energy-charts.info (data/clean/power_da_prices_daily_cet.csv)")
DPD = "day-ahead daily base prices of OPCOM, HUPX and EPEX SPOT via energy-charts.info (data/clean/power_da_prices_daily_cet.csv)"
DFUEL = ("World Bank TTF gas monthly (data/clean/ttf_monthly.csv); EEX primary-auction EUA prices and the SparkChange "
         "CO2 ETC proxy (data/clean/eua_daily.csv)")


def period(ch):
    return C[ch]["period_en"].replace("\\,", ",")


# ---------------------------------------------------------------------------------------------------------------
# the Quantlets
# ---------------------------------------------------------------------------------------------------------------
def q_fw_volume():
    q = Quantlet(5, "fw_volume",
                 "Yearly volume (TWh) of electricity contracted on the Romanian OPCOM PCCB-LE-flex forward auctions, stacked by "
                 "delivery product (month, quarter, half-year, calendar year, other periods); " + period("fw_volume") +
                 ". Also prints the shares of the three state producers in the volume sold and the share of calendar-year products.",
                 "forward contracts, OPCOM, PCCB-LE-flex, liquidity, traded volume, Romania, electricity, energy derivatives",
                 DFW, title="Romanian forward volume by product and year")
    q.md("Volume of the Romanian forward market (OPCOM PCCB-LE-flex auctions) by year of the auction and delivery product.")
    q.code(STYLE).code(LOAD_PD).code(LOAD_FW)
    q.code(r'''FW['year'] = FW['auction_date'].dt.year
vol = FW.pivot_table(index='year', columns='kind', values='mwh', aggfunc='sum').fillna(0) / 1e6   # TWh
for y in vol.index:
    show(f'TWh contracted in {y}' + (' (to the cut-off)' if y == END.year else ''), vol.loc[y].sum(), f'volume.{y}')
tot = FW['mwh'].sum()
sel = FW.groupby('seller')['mwh'].sum()
PROD3 = {'SOCIETATEA COMPLEXUL ENERGETIC OLTENIA S.A.': ('lignite (CE Oltenia)', 'who.sell_oltenia'),
         'SOCIETATEA NATIONALA NUCLEARELECTRICA S.A.': ('nuclear (Nuclearelectrica)', 'who.sell_snn'),
         'S.C. HIDROELECTRICA S.A.': ('hydro (Hidroelectrica)', 'who.sell_hidro')}
show('three state producers, % of the volume sold', 100 * sel.loc[list(PROD3)].sum() / tot, 'who.sell_top3_share', '.1f')
for s, (lab, key) in PROD3.items():
    show('  ' + lab + ', %', 100 * sel.loc[s] / tot, key, '.1f')
show('calendar-year products, % of baseload volume',
     100 * BASE.loc[BASE['kind'] == 'Y', 'mwh'].sum() / BASE['mwh'].sum(), 'volume.y_share_base', '.1f')''')
    q.code(r'''KCOL = {'M': PAL['RO'], 'Q': PAL['HU'], 'H': PAL['BG'], 'Y': PAL['DE_LU'], 'other': '#9a9a9a'}
KL = {'M': 'month', 'Q': 'quarter', 'H': 'half-year', 'Y': 'calendar year', 'other': 'other periods'}
fig, ax = plt.subplots(figsize=(6.4, 2.0))
bot = np.zeros(len(vol))
for k in ['Y', 'H', 'Q', 'M', 'other']:
    if k in vol:
        ax.bar(vol.index, vol[k].values, bottom=bot, color=KCOL[k], width=0.7, label=KL[k])
        bot += vol[k].values
ax.set_ylabel('TWh')
ax.set_xticks(vol.index)
ax.set_xticklabels([str(y) + ('*' if y == END.year else '') for y in vol.index])   # * = to the cut-off
legend_compact(fig, ncol=5)
''' + save_cell("fw_volume", 0.2))
    return q


def q_crisis_cal22():
    q = Quantlet(5, "crisis_cal22",
                 "Prices of the OPCOM forward auctions for calendar-2022 baseload by auction date, against the monthly mean "
                 "Romanian day-ahead price 2020-2022, the realised 2022 average and the volume-weighted forward price; "
                 + period("crisis_cal22") + ". A supplier who bought 2022 forward paid a fraction of the 2022 spot price.",
                 "forward hedge, energy crisis 2022, OPCOM, day-ahead price, Romania, VWAP, hedging",
                 DFW, title="Calendar-2022 forward trades versus the 2022 spot price")
    q.md("Forward prices of calendar-2022 baseload contracts on OPCOM, by auction date, against the realised day-ahead price.")
    q.code(STYLE).code(LOAD_PD).code(LOAD_FW).code(CY_CELL)
    q.code(r'''c22 = CY[CY['dy'] == 2022]
S22 = realised(pd.Timestamp('2022-01-01'), pd.Timestamp('2022-12-31'))   # realised 2022 average spot
F22 = vwap(c22)                                                           # volume-weighted forward price
show('auctions for 2022 baseload', len(c22), 'crisis.n', 'd')
show('VWAP of the 2022 forward, EUR/MWh', F22, 'crisis.F22', '.1f')
show('realised 2022 spot average, EUR/MWh', S22, 'crisis.S22', '.1f')
show('gap spot - forward, EUR/MWh', S22 - F22, 'crisis.gap', '.2f')
show('ratio spot / forward', S22 / F22, 'crisis.ratio', '.2f')
show('saving per MW of baseload, million EUR', (S22 - F22) * 8760 / 1e6, 'crisis.eur_per_mw_m', '.3f')
for lab, a0, a1, key in [('bought in 2020', '2020-01-01', '2020-12-31', 'h20'),
                         ('bought in the first half of 2021', '2021-01-01', '2021-06-30', 'h21a'),
                         ('bought in the second half of 2021', '2021-07-01', '2021-12-31', 'h21b')]:
    g = c22[(c22['auction_date'] >= a0) & (c22['auction_date'] <= a1)]
    show(f'VWAP {lab}, EUR/MWh', vwap(g), f'crisis.parts.{key}.vwap', '.1f')''')
    q.code(r'''SPOT_M = PD['RO'].loc[:END].resample('MS').mean()
fig, ax = plt.subplots(figsize=(6.4, 2.1))
sm_ = SPOT_M.loc['2020-01-01':'2022-12-01']
ax.plot(sm_.index + pd.Timedelta(days=14), sm_.values, color=PAL['RO'], lw=1.4, label='Romania, monthly mean day-ahead')
ax.scatter(c22['auction_date'], c22['price_eur_mwh'], s=9, color=PAL['DE_LU'], zorder=3,
           label='forward for Cal-2022 baseload, one auction')
ax.hlines(S22, pd.Timestamp('2022-01-01'), pd.Timestamp('2022-12-31'), color='#222222', lw=1.2, ls='--', label='realised 2022 average')
ax.hlines(F22, pd.Timestamp('2022-01-01'), pd.Timestamp('2022-12-31'), color=PAL['DE_LU'], lw=1.2, ls='--',
          label='volume-weighted forward')
ax.set_ylabel('EUR/MWh')
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_bottom(fig, ncol=2)
''' + save_cell("crisis_cal22", 0.28))
    return q


def q_cal_by_trade():
    q = Quantlet(5, "cal_by_trade",
                 "Prices of the calendar-year baseload forward contracts on OPCOM (Cal-2021 to Cal-2027) by auction date, with the "
                 "realised mean day-ahead price of each delivered year as a thick line; " + period("cal_by_trade") +
                 ". Shows how the forward curve moves with the trade date.",
                 "forward curve, calendar-year baseload, OPCOM, trade date, realised spot, Romania, electricity",
                 DFW, title="Calendar-year forwards by trade date versus realised spot")
    q.md("Each calendar-year baseload product on OPCOM, by auction date, and the realised mean spot of that year.")
    q.code(STYLE).code(LOAD_PD).code(LOAD_FW).code(CY_CELL)
    q.code(r'''calt = {}
for y, g in CY.groupby('dy'):
    if len(g) < 5:          # products with fewer than five auctions are not shown
        continue
    calt[y] = {'n': len(g), 'vwap': vwap(g), 'realised': realised(pd.Timestamp(f'{y}-01-01'), pd.Timestamp(f'{y}-12-31'))}
    show(f'Cal-{y}: auctions', len(g), f'cal.{y}.n', 'd')
    show(f'Cal-{y}: VWAP, EUR/MWh', calt[y]['vwap'], f'cal.{y}.vwap', '.1f')
    if not np.isnan(calt[y]['realised']):
        show(f'Cal-{y}: realised mean spot, EUR/MWh', calt[y]['realised'], f'cal.{y}.realised', '.1f')''')
    q.code(r'''fig, ax = plt.subplots(figsize=(6.4, 2.05))
cols_ = [PAL['RO'], PAL['HU'], PAL['DE_LU'], PAL['c7'], PAL['BG'], PAL['c5'], PAL['c6']]
for i, y in enumerate([y for y in sorted(calt) if y <= END.year + 1]):
    g = CY[CY['dy'] == y]
    ax.scatter(g['auction_date'], g['price_eur_mwh'], s=7, color=cols_[i % len(cols_)], label=f'Cal-{y}')
    if not np.isnan(calt[y]['realised']) and y <= END.year - 1:
        ax.hlines(calt[y]['realised'], pd.Timestamp(f'{y}-01-01'), pd.Timestamp(f'{y}-12-31'), color=cols_[i % len(cols_)], lw=2.0)
ax.set_ylabel('EUR/MWh')
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_compact(fig, ncol=4)
for h_ in fig.legends[-1].legend_handles:          # legend markers readable
    if hasattr(h_, 'set_sizes'):
        h_.set_sizes([30])
''' + save_cell("cal_by_trade", 0.2))
    return q


CURVE = r'''# forward curve: baseload products traded in the last three months for delivery after the cut-off, VWAP per product
CURVE_FROM = (END - pd.DateOffset(months=2) + pd.Timedelta(days=1)).normalize()
cur = BASE[(BASE['auction_date'] >= CURVE_FROM) & (BASE['delivery_start'] > END)]
curve = (cur.groupby(['delivery_start', 'delivery_end', 'kind'])
         .apply(lambda g: pd.Series({'F': vwap(g), 'n': len(g), 'twh': g['mwh'].sum() / 1e6})).reset_index())'''


def q_fwd_curve():
    q = Quantlet(5, "fwd_curve",
                 "Romanian baseload forward curve at the cut-off: volume-weighted OPCOM forward price of each product "
                 "(month, quarter, half-year, calendar year) over its delivery period, against the realised monthly mean "
                 "day-ahead price of the last 24 months; " + period("fwd_curve") + ".",
                 "forward curve, term structure, backwardation, OPCOM, baseload, Romania, electricity",
                 DFW, title="The Romanian baseload forward curve")
    q.md("The forward curve today: products traded in the last three months for delivery after the cut-off.")
    q.code(STYLE).code(LOAD_PD).code(LOAD_FW)
    q.code(CURVE + r'''
print(curve.round(2).to_string())
show('products on the curve', len(curve), 'curve.n_products', 'd')
show('auctions on the curve', len(cur), 'curve.n_sessions', 'd')
cal = curve[curve['kind'] == 'Y'].sort_values('delivery_start')
show(f"next calendar year ({cal['delivery_start'].iloc[0].year}), EUR/MWh", cal['F'].iloc[0], 'curve.cal_next.F', '.1f')
mth = curve[curve['kind'] == 'M'].sort_values('delivery_start')
if len(mth):
    show(f"front month ({mth['delivery_start'].iloc[0]:%Y-%m}), EUR/MWh", mth['F'].iloc[0], 'curve.m_front.F', '.1f')
qq = curve[curve['kind'] == 'Q'].sort_values('delivery_start')
if len(qq):
    show(f"front quarter (from {d(qq['delivery_start'].iloc[0])}), EUR/MWh", qq['F'].iloc[0], 'curve.q_front.F', '.1f')
show('mean spot of the last three months, EUR/MWh', PD.loc[END - pd.DateOffset(months=3) + pd.Timedelta(days=1):END, 'RO'].mean(),
     'curve.spot_last3', '.1f')
show('mean spot of the last month, EUR/MWh', PD.loc[END.replace(day=1):END, 'RO'].mean(), 'curve.spot_lastm', '.1f')''')
    q.code(r'''from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
KCOL = {'M': PAL['RO'], 'Q': PAL['HU'], 'H': PAL['BG'], 'Y': PAL['DE_LU']}
KL = {'M': 'month', 'Q': 'quarter', 'H': 'half-year', 'Y': 'calendar year'}
SPOT_M = PD['RO'].loc[:END].resample('MS').mean()
fig, ax = plt.subplots(figsize=(6.4, 2.2))
sp = SPOT_M.loc[END - pd.DateOffset(months=23):]
ax.step(sp.index, sp.values, where='post', color=PAL['RO'], lw=1.3)
for r in curve.sort_values('kind').itertuples():
    ax.hlines(r.F, r.delivery_start, r.delivery_end + pd.Timedelta(days=1), color=KCOL[r.kind], lw=2.4)
ks = [k for k in ['M', 'Q', 'H', 'Y'] if (curve['kind'] == k).any()]
hnd = [Line2D([], [], color=PAL['RO'], lw=1.3)] + [Line2D([], [], color=KCOL[k], lw=2.4) for k in ks]
lab = ['realised monthly mean (PZU)'] + ['forward, ' + KL[k] for k in ks]
ax.axvline(END + pd.Timedelta(days=1), color='#222222', lw=0.8, ls=':')     # cut-off
ax.set_ylabel('EUR/MWh')
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: MON[mdates.num2date(v).month - 1] + f'\n{mdates.num2date(v).year}'))
legend_bottom(fig, handles=hnd, labels=lab, ncol=2)
''' + save_cell("fwd_curve", 0.26))
    return q


def q_premium():
    q = Quantlet(5, "premium",
                 "Ex-post forward premium of Romanian monthly baseload contracts traded on OPCOM in the month before delivery: "
                 "volume-weighted forward price minus the realised mean day-ahead price of the delivery month; "
                 + period("premium") + ". Prints the mean with a Newey-West (HAC) t-test, the median and the share of positive months.",
                 "forward premium, risk premium, Newey-West, HAC, OPCOM, monthly baseload, Romania, electricity",
                 DFW, title="Ex-post forward premium of one-month-ahead products")
    q.md("Forward minus realised spot for monthly baseload products bought one month ahead.")
    q.code(STYLE).code(LOAD_PD).code(LOAD_FW).code(PREMIUM_TABLE)
    q.code(r'''import statsmodels.api as sm


def nw_t(x, lags=3):
    """Mean of x with a Newey-West (HAC, 3 lags) standard error: mean, se, t, p."""
    x = np.asarray(x, float)
    r = sm.OLS(x, np.ones(len(x))).fit(cov_type='HAC', cov_kwds={'maxlags': lags})
    return float(r.params[0]), float(r.bse[0]), float(r.tvalues[0]), float(r.pvalues[0])


MP = M1.groupby('delivery_start').apply(lambda g: pd.Series({'F': vwap(g), 'S': g['S'].iloc[0], 'n': len(g)}))
MP['prem'] = MP['F'] - MP['S']
mu, se, tt, pp = nw_t(MP['prem'])
show('delivery months', len(MP), 'prem.m1.n', 'd')
show('first delivery month', MP.index.min().strftime('%Y-%m'), 'prem.m1.first')
show('last delivery month', MP.index.max().strftime('%Y-%m'), 'prem.m1.last')
show('mean premium F - S, EUR/MWh', mu, 'prem.m1.mean', '.2f')
show('HAC standard error', se, 'prem.m1.se', '.2f')
show('t statistic', tt, 'prem.m1.t', '.2f')
show('p-value', pp, 'prem.m1.p', '.3f')
show('median premium, EUR/MWh', MP['prem'].median(), 'prem.m1.median', '.1f')
show('share of months with F > S, %', 100 * (MP['prem'] > 0).mean(), 'prem.m1.pos_share', '.1f')
gm = MP[MP.index >= '2023-01-01']
a, _, c, p = nw_t(gm['prem'])
show('from 2023: mean premium, EUR/MWh', a, 'prem.m1_post.mean', '.2f')
show('from 2023: t statistic', c, 'prem.m1_post.t', '.2f')''')
    q.code(r'''from matplotlib.patches import Patch
fig, ax = plt.subplots(figsize=(6.4, 2.0))
ax.bar(MP.index, MP['prem'], width=25, color=[PAL['DE_LU'] if v > 0 else PAL['RO'] for v in MP['prem']])
ax.axhline(0, color='#222222', lw=0.6)
hnd = [Patch(color=PAL['DE_LU'], label='F above realised spot (premium paid)'),
       Patch(color=PAL['RO'], label='F below realised spot')]
ax.set_ylabel('F minus realised,\nEUR/MWh', fontsize=10)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_bottom(fig, handles=hnd, labels=[h.get_label() for h in hnd], ncol=2)
''' + save_cell("premium", 0.2))
    return q


def q_spreads():
    q = Quantlet(5, "spreads",
                 "Monthly clean spark spread (Romania and Germany) and clean dark spread (Romania): monthly mean day-ahead price "
                 "minus fuel cost (TTF gas at 50% efficiency, South African coal at 38%) and carbon cost (EUA); "
                 + period("spreads") + ".",
                 "clean spark spread, clean dark spread, gas-fired generation, coal, EUA, carbon price, TTF, Romania, Germany",
                 DPD + "; " + DFUEL + "; World Bank South African coal (data/clean/coal_monthly.csv) converted with the ECB "
                 "EUR/USD rate (data/clean/fuels_daily.csv)", title="Monthly clean spark and clean dark spreads")
    q.md("Clean spark and clean dark spreads, monthly, from real power, gas, coal and carbon prices.")
    q.code(STYLE).code(LOAD_PD).code(MONTHLY_PM).code(FUEL_COST)
    q.code(r'''# coal: World Bank South African export coal, USD/t -> EUR per MWh thermal
COAL = pd.read_csv(DATA + 'coal_monthly.csv')
COAL.index = pd.PeriodIndex(COAL['month'], freq='M').to_timestamp()
FUEL = pd.read_csv(DATA + 'fuels_daily.csv', parse_dates=['date']).set_index('date')
fxm = FUEL['eurusd_ecb'].resample('MS').mean().reindex(m_idx)
COALE = (COAL['coal_southafrica_usd_t'].reindex(m_idx) / fxm) / COAL_MWH_T


def spreads(p, gas, coal, eua):
    """Spark, clean spark, dark and clean dark spreads in EUR per MWh of electricity."""
    ss = p - gas / ETA_GAS
    css = ss - EF_GAS / ETA_GAS * eua
    ds = p - coal / ETA_COAL
    cds = ds - EF_COAL / ETA_COAL * eua
    return pd.DataFrame({'ss': ss, 'css': css, 'ds': ds, 'cds': cds})


SPR = {z: spreads(PM[z], GAS, COALE, EUAM) for z in ['RO', 'DE_LU']}
show('months with a clean spark spread', SPR['RO']['css'].notna().sum(), 'spread.n_m', 'd')
show('months with a negative clean spark spread, Romania', (SPR['RO']['css'] < 0).sum(), 'spread.css_ro_neg_m', 'd')
show('months with a negative clean spark spread, Germany', (SPR['DE_LU']['css'] < 0).sum(), 'spread.css_de_neg_m', 'd')
show('mean gap of the clean spark spread, Romania - Germany', (SPR['RO']['css'] - SPR['DE_LU']['css']).mean(), 'spread.gap_ro_de', '.2f')
show('highest clean spark spread, Romania, EUR/MWh', SPR['RO']['css'].max(), 'spread.css_ro_max', '.2f')
show('  month', SPR['RO']['css'].idxmax().strftime('%Y-%m'), 'spread.css_ro_max_ym')
show('lowest clean spark spread, Romania, EUR/MWh', SPR['RO']['css'].min(), 'spread.css_ro_min', '.2f')
show('  month', SPR['RO']['css'].idxmin().strftime('%Y-%m'), 'spread.css_ro_min_ym')
show('months where gas beats coal (CSS > CDS), Romania', (SPR['RO']['css'] > SPR['RO']['cds']).sum(), 'spread.gas_cheaper_m', 'd')
yrs = SPR['RO'].groupby(SPR['RO'].index.year).mean()
for y in yrs.index:
    show(f'{y}: mean clean spark / clean dark spread, Romania', f"{yrs.loc[y, 'css']:.2f} / {yrs.loc[y, 'cds']:.2f}")''')
    q.code(r'''fig, ax = plt.subplots(figsize=(6.4, 2.2))
ax.plot(SPR['RO'].index, SPR['RO']['css'], color=PAL['RO'], lw=1.3, label='clean spark, Romania')
ax.plot(SPR['DE_LU'].index, SPR['DE_LU']['css'], color=PAL['DE_LU'], lw=1.1, ls=':', label='clean spark, Germany')
ax.plot(SPR['RO'].index, SPR['RO']['cds'], color=PAL['c7'], lw=1.1, ls='--', label='clean dark, Romania')
ax.axhline(0, color='#222222', lw=0.6)
ax.set_ylabel('EUR per MWh\nof electricity', fontsize=10)
ax.xaxis.set_major_locator(mdates.YearLocator(2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_compact(fig, ncol=3)
''' + save_cell("spreads", 0.2))
    return q


def q_spark_hourly():
    q = Quantlet(5, "spark_hourly",
                 "Sorted hourly clean spark spreads of a gas plant (50% efficiency) in Romania and Germany over the last 12 "
                 "complete months, " + period("spark_hourly") + " (60-min and 15-min market time units weighted by duration): "
                 "the area above zero is the value of running only in profitable hours (a strip of hourly call options).",
                 "spark spread option, real option, gas-fired plant, flexibility, duration curve, day-ahead, Romania, Germany",
                 "day-ahead prices at native resolution (data/clean/power_da_prices_native_utc.csv, energy-charts.info); "
                 + DFUEL, title="Sorted hourly clean spark spreads")
    q.md("A 1 MW gas plant as a strip of hourly options: the clean spark spread of every market time unit, sorted.")
    q.code(STYLE).code(LOAD_PD)
    q.code(r'''m_idx = pd.date_range('2015-01-01', END.replace(day=1), freq='MS')''')
    q.code(FUEL_COST)
    q.code(r'''# day-ahead prices at native resolution (60 min, 15 min from 1 Oct 2025), CET/CEST
HP = pd.read_csv(DATA + 'power_da_prices_native_utc.csv', parse_dates=['timestamp_utc'],
                 usecols=['timestamp_utc', 'mtu_minutes', 'RO', 'DE_LU']).set_index('timestamp_utc')
HP.index = HP.index.tz_convert('Europe/Brussels')
H0 = (END - pd.DateOffset(months=12) + pd.Timedelta(days=1)).normalize()      # last 12 complete months
HH = HP.loc[str(H0.date()):str(END.date())].copy()
HH['w'] = HH['mtu_minutes'] / 60.0                  # hour-equivalent of each market time unit
mkey = HH.index.tz_localize(None).to_period('M').to_timestamp()
cost = GAS / ETA_GAS + EF_GAS / ETA_GAS * EUAM      # fuel + carbon cost per MWh of electricity, monthly
HH['c'] = cost.reindex(mkey).values
print('window:', d(H0), 'to', d(END))
for z, nm in [('RO', 'Romania'), ('DE_LU', 'Germany')]:
    s = HH[z] - HH['c']
    ok = s.notna()
    w, s = HH.loc[ok, 'w'], s[ok]
    show(f'{nm}: hours', w.sum(), f'opt.{z}.hours', '.1f')
    show(f'{nm}: share of hours with a positive spread, %', 100 * w[s > 0].sum() / w.sum(), f'opt.{z}.itm_share', '.1f')
    show(f'{nm}: must-run margin, EUR per MW', (s * w).sum(), f'opt.{z}.base_eur', ',.0f')
    show(f'{nm}: flexible margin (only positive hours), EUR per MW', (np.maximum(s, 0) * w).sum(), f'opt.{z}.flex_eur', ',.0f')''')
    q.code(r'''fig, ax = plt.subplots(figsize=(6.4, 2.3))
for z, col, ls, nm in [('RO', PAL['RO'], '-', 'Romania'), ('DE_LU', PAL['DE_LU'], ':', 'Germany')]:
    s = (HH[z] - HH['c']).dropna()
    w = HH.loc[s.index, 'w']
    o = np.argsort(-s.values)
    ax.plot(np.cumsum(w.values[o]), s.values[o], color=col, ls=ls, lw=1.4, label=nm)
ax.axhline(0, color='#222222', lw=0.6)
ax.set_ylim(-250, 400)
ax.set_xlabel('hours of the last 12 months, sorted from the highest spread')
ax.set_ylabel('clean spark,\nEUR/MWh', fontsize=10)
legend_bottom(fig, ncol=2)
''' + save_cell("spark_hourly", 0.24))
    return q


def q_hedge_scatter():
    q = Quantlet(5, "hedge_scatter",
                 "Minimum-variance hedge ratio of the Romanian monthly day-ahead price with Hungarian and German prices: "
                 "scatter of monthly changes with the OLS line, h* and R2; " + period("hedge_scatter") + ". Prints h* with "
                 "HAC standard errors, moving-block bootstrap 95% intervals and the out-of-sample variance reduction from 2021 "
                 "with h* estimated on 2015-2020.",
                 "hedge ratio, minimum variance, OLS, HAC, block bootstrap, hedge effectiveness, cross hedge, Romania, Hungary, Germany",
                 DPD, title="Minimum-variance hedge ratio, Romania versus Hungary and Germany")
    q.md("Monthly changes of the Romanian price regressed on those of Hungary and Germany: the slope is the hedge ratio h*.")
    q.code(STYLE).code(LOAD_PD).code(MONTHLY_PM).code(hedge_code())
    q.code(r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.95), sharey=True)
for ax, z, col, nm in [(axs[0], 'HU', PAL['HU'], 'Hungary'), (axs[1], 'DE_LU', PAL['DE_LU'], 'Germany')]:
    ax.scatter(dP[z], dP['RO'], s=8, color=col, alpha=0.8)
    xx = np.linspace(dP[z].min(), dP[z].max(), 10)
    ax.plot(xx, HR[z]['h'] * xx, color='#222222', lw=1.0)
    ax.set_xlabel(f'Δ {nm}, EUR/MWh', fontsize=10)
    ax.text(0.03, 0.92, f"h* = {HR[z]['h']:.2f},  R² = {HR[z]['r2']:.2f}", transform=ax.transAxes, fontsize=10)
axs[0].set_ylabel('Δ Romania,\nEUR/MWh', fontsize=10)  # Δ = monthly change
''' + save_cell("hedge_scatter", 0.02))
    return q


def q_basis():
    q = Quantlet(5, "basis",
                 "Basis risk of a foreign hedge: monthly price gap Romania minus Hungary and Romania minus Germany (left) and "
                 "the duration-weighted share of hours in which the Romanian price equals the Hungarian or German one within "
                 "0.01 EUR/MWh, by year (right); " + period("basis").replace("right: |difference| < 0.01 EUR/MWh", "hourly and monthly data") + ".",
                 "basis risk, market coupling, price convergence, cross-border, Romania, Hungary, Germany, day-ahead",
                 DPD + "; day-ahead prices at native resolution (data/clean/power_da_prices_native_utc.csv)",
                 title="Basis Romania-Hungary and Romania-Germany")
    q.md("The basis left by a Hungarian or German hedge, and how often the prices are equal.")
    q.code(STYLE).code(LOAD_PD).code(MONTHLY_PM)
    q.code(r'''BAS = pd.DataFrame({'HU': PM['RO'] - PM['HU'], 'DE_LU': PM['RO'] - PM['DE_LU']})     # monthly basis
for z, nm in [('HU', 'Romania - Hungary'), ('DE_LU', 'Romania - Germany')]:
    b = BAS[z].dropna()
    show(f'{nm}: mean basis, EUR/MWh', b.mean(), f'basis.{z}.mean', '.2f')
    show(f'{nm}: std. dev. 2015-2020, EUR/MWh', b[:'2020-12-01'].std(), f'basis.{z}.sd_pre', '.2f')
    show(f'{nm}: std. dev. from 2021, EUR/MWh', b['2021-01-01':].std(), f'basis.{z}.sd_post', '.2f')
    show(f'{nm}: mean from 2023, EUR/MWh', b['2023-01-01':].mean(), f'basis.{z}.mean_post', '.2f')
    show(f'{nm}: largest monthly basis, EUR/MWh ({b.idxmax():%Y-%m})', b.max(), f'basis.{z}.max', '.2f')

# share of hours with the same price (|difference| < 0.01 EUR/MWh), weighted by duration (60/15-min units)
NP = pd.read_csv(DATA + 'power_da_prices_native_utc.csv', parse_dates=['timestamp_utc'],
                 usecols=['timestamp_utc', 'mtu_minutes', 'RO', 'HU', 'DE_LU']).set_index('timestamp_utc')
NP.index = NP.index.tz_convert('Europe/Brussels')
NP = NP.loc[:str(END.date())].copy()
NP['w'] = NP['mtu_minutes'] / 60
NP = NP[NP['RO'].notna() & NP['HU'].notna()]
wy = NP['w'].groupby(NP.index.year).sum()
conv = (NP['w'] * ((NP['RO'] - NP['HU']).abs() < 0.01)).groupby(NP.index.year).sum() / wy * 100
convd = (NP['w'] * ((NP['RO'] - NP['DE_LU']).abs() < 0.01)).groupby(NP.index.year).sum() / wy * 100
for y in conv.index:
    show(f'{y}: % of hours RO = HU', conv[y], f'basis.conv_hu.{y}', '.1f')
for y in convd.index:
    show(f'{y}: % of hours RO = DE', convd[y], f'basis.conv_de.{y}', '.1f')''')
    q.code(r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.05), gridspec_kw={'width_ratios': [1.6, 1]})
axs[0].plot(BAS.index, BAS['HU'], color=PAL['HU'], lw=1.2, label='Romania minus Hungary')
axs[0].plot(BAS.index, BAS['DE_LU'], color=PAL['DE_LU'], lw=1.0, ls=':', label='Romania minus Germany')
axs[0].axhline(0, color='#222222', lw=0.6)
axs[0].set_ylabel('monthly basis,\nEUR/MWh', fontsize=10)
axs[0].xaxis.set_major_locator(mdates.YearLocator(3))
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
yy = [int(y) for y in conv.index]
axs[1].bar([y - 0.2 for y in yy], conv.values, width=0.4, color=PAL['HU'])
axs[1].bar([y + 0.2 for y in yy], convd.values, width=0.4, color=PAL['DE_LU'])
axs[1].set_ylabel('% of hours with\nthe same price', fontsize=10)
axs[1].set_xticks([2015, 2020, 2025])
legend_bottom(fig, ncol=2)
''' + save_cell("basis", 0.22))
    return q


def q_shape():
    q = Quantlet(5, "shape",
                 "Shape risk in Romania: yearly load-weighted day-ahead price and solar capture price relative to the baseload "
                 "(time-average) price; " + period("shape") + ".",
                 "shape risk, profile factor, capture price, solar cannibalisation, load-weighted price, baseload, Romania",
                 "hourly day-ahead prices (data/clean/power_da_prices_hourly_utc.csv) and Romanian hourly load and solar output "
                 "(data/clean/generation_ro_mw_hourly_utc.csv), energy-charts.info / ENTSO-E",
                 title="Load and solar profile factors, Romania")
    q.md("Profile factors: what one MWh of load or of solar output is worth relative to one MWh of the band.")
    q.code(STYLE).code(LOAD_PD)
    q.code(r'''PH = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', parse_dates=['timestamp_utc'],
                 usecols=['timestamp_utc', 'RO']).set_index('timestamp_utc')
GH = pd.read_csv(DATA + 'generation_ro_mw_hourly_utc.csv', parse_dates=['timestamp_utc'],
                 usecols=['timestamp_utc', 'load', 'solar']).set_index('timestamp_utc')
J = pd.concat([PH['RO'], GH['load'], GH['solar']], axis=1).loc[:str(END.date()) + ' 21:00'].dropna()
J = J[J.index >= '2015-01-05']
J['y'] = J.index.tz_convert('Europe/Brussels').year


def profile_factor(g):
    base = g['RO'].mean()
    return pd.Series({'base': base, 'load_w': (g['RO'] * g['load']).sum() / g['load'].sum(),
                      'solar_w': (g['RO'] * g['solar']).sum() / g['solar'].sum() if g['solar'].sum() > 0 else np.nan})


PF = J.groupby('y').apply(profile_factor)
PF['f_load'] = PF['load_w'] / PF['base']
PF['f_solar'] = PF['solar_w'] / PF['base']
show('hours used', len(J), 'shape.n_hours', ',d')
for y in PF.index:
    show(f'{y}: load factor', PF.loc[y, 'f_load'], f'shape.f_load.{y}', '.3f')
    show(f'{y}: solar factor', PF.loc[y, 'f_solar'], f'shape.f_solar.{y}', '.3f')
show('lowest solar factor', PF['f_solar'].min(), 'shape.solar_min', '.3f')
show('  year', str(PF['f_solar'].idxmin()), 'shape.solar_min_y')
show('2025: load-weighted minus baseload price, EUR/MWh', PF.loc[2025, 'load_w'] - PF.loc[2025, 'base'], 'shape.load_prem.2025', '.2f')''')
    q.code(r'''fig, ax = plt.subplots(figsize=(6.4, 2.0))
ax.plot(PF.index, PF['f_load'], marker='o', ms=3.5, color=PAL['RO'], lw=1.3, label='load-weighted / baseload price')
ax.plot(PF.index, PF['f_solar'], marker='s', ms=3.5, color=PAL['BG'], lw=1.3, label='solar capture / baseload price')
ax.axhline(1, color='#222222', lw=0.6)
ax.set_xticks(PF.index)
ax.set_xticklabels([str(y) + ('*' if y == END.year else '') for y in PF.index], fontsize=9.5)    # * = to the cut-off
ax.set_ylabel('ratio')
legend_bottom(fig, ncol=2)
''' + save_cell("shape", 0.2))
    return q


def q_samuelson():
    q = Quantlet(5, "samuelson",
                 "Samuelson effect in Dutch TTF gas futures: rolling 60-trading-day annualised volatility of the NYMEX TTF "
                 "contracts for December 2026 and May 2027 (single contracts, no rolls); " + period("samuelson") +
                 ". The contract nearer to delivery is more volatile.",
                 "Samuelson effect, futures volatility, time to maturity, TTF, natural gas, rolling volatility",
                 "NYMEX TTF futures, individual contract months, daily closes from Yahoo Finance "
                 "(data/clean/ttf_futures_contracts_daily.csv)", title="The Samuelson effect in TTF futures")
    q.md("Volatility of two TTF contracts with different delivery months, measured over the same calendar days.")
    q.code(STYLE).code(LOAD_PD)
    q.code(r'''TTFC = pd.read_csv(DATA + 'ttf_futures_contracts_daily.csv', parse_dates=['date']).set_index('date').loc[:END]


def ann_vol(s, window=None):
    """Daily log returns between consecutive trading days (gaps <= 4 calendar days); with window: rolling annualised vol."""
    s = s.dropna()
    r = np.log(s).diff().dropna()
    gap = s.index.to_series().diff().dt.days.reindex(r.index)
    r = r[gap <= 4]
    return r if window is None else r.rolling(window).std() * np.sqrt(252)


W12 = (END - pd.DateOffset(months=12) + pd.Timedelta(days=1)).normalize()
show('window of the last 12 months: from', d(W12), 'sam.w_from')
show('                               to', d(END), 'sam.w_to')
for c in TTFC.columns:
    r = ann_vol(TTFC[c])
    show(f'TTF {c}: volatility last 12 months, % per year', r.loc[W12:END].std() * np.sqrt(252) * 100, f'sam.{c}.v12', '.1f')
    show(f'TTF {c}: volatility in 2022, % per year', r.loc['2022'].std() * np.sqrt(252) * 100, f'sam.{c}.v22', '.1f')
ROLLV = pd.DataFrame({c: ann_vol(TTFC[c], 60) for c in ['2026-12', '2027-05']})''')
    q.code(r'''MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
fig, ax = plt.subplots(figsize=(6.4, 2.0))
for c, cc, ls in [('2026-12', PAL['RO'], '-'), ('2027-05', PAL['DE_LU'], ':')]:
    v = ROLLV[c].dropna() * 100
    ax.plot(v.index, v.values, color=cc, ls=ls, lw=1.3, label='TTF contract for ' + MON[int(c[5:]) - 1] + ' ' + c[:4])
ax.set_ylabel('volatility,\n% per year', fontsize=10)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_bottom(fig, ncol=2)
''' + save_cell("samuelson", 0.2))
    return q


def q_collar():
    y1 = int(END[:4]) + 1
    q = Quantlet(5, "collar",
                 f"Effective price paid for the Romanian Cal-{y1} baseload band as a function of the forward price at "
                 "expiry: unhedged, forward, cap (call bought at K = 1.1 F) and collar 0.9 F - 1.1 F, with Black-76 premia "
                 "from real inputs (F = OPCOM VWAP, volatility of the calendar forwards, euro short-term rate); "
                 + period("collar") + ".",
                 "Black-76, option pricing, cap, collar, call option, put option, hedging, forward, OPCOM, Romania",
                 DFW + "; ECB euro short-term rate (data/clean/ecb_ron_estr_daily.csv)",
                 title=f"Effective price of the Cal-{y1} band with forward, cap and collar")
    q.md("What each instrument pays for next year's band: inputs of the Black-76 model taken from real data.")
    q.code(STYLE).code(LOAD_PD).code(LOAD_FW).code(CY_CELL).code(CURVE).code(BLACK76)
    q.code(r'''def cal_vol(g, max_gap=30):
    """Volatility of a calendar forward from irregular auction days: daily VWAP, sigma^2 = sum (d ln F)^2 / sum dt,
    using only pairs of auction days at most max_gap calendar days apart."""
    dv = g.groupby('auction_date').apply(vwap)
    dl = np.log(dv).diff().dropna()
    dt = dv.index.to_series().diff().dt.days.dropna() / 365.25
    m = dt <= max_gap / 365.25
    return dl[m], dt[m]


DL, DT = [], []
for y in [END.year - 1, END.year, END.year + 1]:
    dl, dt = cal_vol(CY[CY['dy'] == y])
    DL.append(dl)
    DT.append(dt)
sig = float(np.sqrt(sum((x ** 2).sum() for x in DL) / sum(x.sum() for x in DT)))   # pooled volatility

cal = curve[curve['kind'] == 'Y'].sort_values('delivery_start')
F0 = round(float(cal['F'].iloc[0]), 2)                     # next calendar year on the curve (VWAP)
R = RATES['estr_pct'].loc[:END].dropna()
r0 = R.iloc[-1] / 100
EXPIRY = pd.Timestamp(f'{END.year}-12-15')
T0 = (EXPIRY - END).days / 365.25
c110, _, _, _, _ = black76(F0, 1.1 * F0, T0, r0, sig, 'call')
p90, _, _, _, _ = black76(F0, 0.9 * F0, T0, r0, sig, 'put')
c_atm, _, _, _, _ = black76(F0, F0, T0, r0, sig, 'call')
show(f"F = Cal-{cal['delivery_start'].iloc[0].year} baseload VWAP, EUR/MWh", F0, 'bs.F', '.2f')
show('volatility of the calendar forwards (pooled), per year', sig, 'bs.sig_cal', '.4f')
show(f'euro short-term rate on {d(R.index[-1])}, %', r0 * 100, 'bs.r', '.3f')
show(f'time to expiry ({d(EXPIRY)}), years', T0, 'bs.T', '.4f')
show('at-the-money call, EUR/MWh', c_atm, 'bs.c.call', '.2f')
show('cap strike K = 1.1 F, EUR/MWh', 1.1 * F0, 'bs.K110', '.2f')
show('floor strike 0.9 F, EUR/MWh', 0.9 * F0, 'bs.K90', '.2f')
show('call at 1.1 F, EUR/MWh', c110, 'bs.c.call110', '.2f')
show('put at 0.9 F, EUR/MWh', p90, 'bs.c.put90', '.2f')
show('collar = call 1.1 F - put 0.9 F, EUR/MWh', c110 - p90, 'bs.c.collar', '.2f')
show('cap premium per MW of baseload for a year, EUR', round(c110, 2) * 8760, 'bs.mw_year', ',.0f')   # premium as quoted (2 decimals) x 8760 h''')
    q.code(r'''fig, ax = plt.subplots(figsize=(6.4, 2.05))
FT = np.linspace(0.75 * F0, 1.3 * F0, 200)                      # forward price at expiry
cT, pT = round(c110, 2) * np.exp(r0 * T0), round(p90, 2) * np.exp(r0 * T0)    # premia carried to expiry
ax.plot(FT, FT, color='#9a9a9a', lw=1.2, label='unhedged')
ax.plot(FT, np.full_like(FT, F0), color=PAL['HU'], lw=1.4, label='forward at F')
ax.plot(FT, np.minimum(FT, 1.1 * F0) + cT, color=PAL['DE_LU'], lw=1.4, ls='--', label='cap at 1.1 F')
ax.plot(FT, np.clip(FT, 0.9 * F0, 1.1 * F0) + cT - pT, color=PAL['c7'], lw=1.4, ls='-.', label='collar 0.9 F to 1.1 F')
ax.set_xlabel('forward price at expiry $F_T$, EUR/MWh')
ax.set_ylabel('effective price,\nEUR/MWh', fontsize=10)
legend_compact(fig, ncol=4)
''' + save_cell("collar", 0.3))
    return q


def q_case2026():
    y = int(END[:4])
    q = Quantlet(5, "case2026",
                 f"Case study {y}: monthly cost of 1 MW of baseload for a Romanian supplier, {y}-01 to {END[:7]}, with four "
                 f"strategies: unhedged (realised day-ahead monthly mean), 100% forward Cal-{y} (OPCOM VWAP), 50% "
                 "forward + 50% spot, and monthly caps at K bought in December of the previous year (Black-76 premium with the "
                 "terminal volatility of one-month-ahead forwards and the euro short-term rate).",
                 "case study, hedging strategy, forward, cap, Black-76, supplier, cost of energy, OPCOM, Romania",
                 DFW + "; ECB euro short-term rate (data/clean/ecb_ron_estr_daily.csv)",
                 title=f"Case study {y}: cost of four hedging strategies")
    q.md(f"A supplier buys 1 MW of baseload for {y}: spot, forward, half and half, or monthly caps.")
    q.code(STYLE).code(LOAD_PD).code(LOAD_FW).code(CY_CELL).code(PREMIUM_TABLE).code(BLACK76)
    q.code(r'''# terminal volatility of ln(S/F) per sqrt(year), monthly products bought one month ahead
sig_term = round(float((M1['lr'] / np.sqrt(M1['T'])).std(ddof=1)), 4)
show('terminal volatility of one-month-ahead forwards, per year', sig_term, 'termvol.all', '.4f')

c26 = CY[CY['dy'] == END.year]
F26 = vwap(c26)
mm = pd.date_range(f'{END.year}-01-01', END.replace(day=1), freq='MS')
S26 = pd.Series([realised(m, m + pd.offsets.MonthEnd(0)) for m in mm], index=mm)
hrs = pd.Series([((m + pd.offsets.MonthEnd(0) + pd.Timedelta(days=1)).tz_localize('Europe/Brussels') -
                  m.tz_localize('Europe/Brussels')) / pd.Timedelta(hours=1) for m in mm], index=mm)     # hours of each month
# cap strip bought on 15 December of the previous year: K = VWAP of the last auction quarter of that year
ref = c26[c26['auction_date'] >= pd.Timestamp(f'{END.year - 1}-10-01')]
if len(ref) == 0:
    ref = c26[c26['auction_date'] >= pd.Timestamp(f'{END.year - 1}-07-01')]
Fref = vwap(ref)
BUYD = pd.Timestamp(f'{END.year - 1}-12-15')
rb = RATES['estr_pct'].loc[:BUYD].dropna().iloc[-1] / 100
prem_m = pd.Series([black76(Fref, Fref, ((m + pd.Timedelta(days=14)) - BUYD).days / 365.25, rb, sig_term)[0] for m in mm], index=mm)
STRAT = pd.DataFrame({'spot': S26, 'fwd': F26, 'half': 0.5 * F26 + 0.5 * S26,
                      'cap': S26 - np.maximum(S26 - Fref, 0) + prem_m})
w = hrs / hrs.sum()
show(f'Cal-{END.year} VWAP, EUR/MWh', F26, 'case.F26', '.2f')
show('cap strike K (VWAP of the last quarter of auctions), EUR/MWh', Fref, 'case.Fref', '.2f')
show('mean cap premium, EUR/MWh', prem_m.mean(), 'case.prem_mean', '.2f')
show('months', len(mm), 'case.months', 'd')
show('months where the forward beat the spot', int((S26 > F26).sum()), 'case.n_fwd_win', 'd')
show('months where the cap paid out', int((S26 > Fref).sum()), 'case.n_cap_pay', 'd')
show('highest monthly spot, EUR/MWh', S26.max(), 'case.spot.max', '.2f')
show('  month', S26.idxmax().strftime('%Y-%m'), 'case.spot_max_ym')
for k, lab in [('spot', 'unhedged'), ('fwd', '100% forward'), ('half', '50/50'), ('cap', 'monthly caps')]:
    show(f'{lab}: hour-weighted mean cost, EUR/MWh', (STRAT[k] * w).sum(), f'case.{k}.mean', '.2f')
    show(f'{lab}: cost per MW, EUR', (STRAT[k] * hrs).sum(), f'case.{k}.eur_mw', ',.0f')
eur = {k: round((STRAT[k] * hrs).sum()) for k in STRAT}      # costs per MW, rounded to the euro as on the slide
show('saving of the forward vs spot, EUR per MW', eur['spot'] - eur['fwd'], 'case.save_fwd', ',.0f')
show('saving of the caps vs spot, EUR per MW', eur['spot'] - eur['cap'], 'case.save_cap', ',.0f')''')
    q.code(r'''MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
fig, ax = plt.subplots(figsize=(6.4, 2.1))
xm = STRAT.index + pd.Timedelta(days=14)
ax.plot(xm, STRAT['spot'], marker='o', ms=3.5, color='#9a9a9a', lw=1.3, label='unhedged (spot)')
ax.plot(xm, STRAT['fwd'], color=PAL['HU'], lw=1.6, label=f'100% forward Cal-{END.year}')
ax.plot(xm, STRAT['half'], color=PAL['RO'], lw=1.2, ls=':', label='50% forward + 50% spot')
ax.plot(xm, STRAT['cap'], color=PAL['DE_LU'], lw=1.3, ls='--', marker='s', ms=3, label='monthly caps at K')
ax.set_ylabel('cost, EUR/MWh')
ax.set_xticks(xm)
ax.set_xticklabels([MON[m.month - 1] for m in STRAT.index])
legend_bottom(fig, ncol=2)
''' + save_cell("case2026", 0.2))
    return q


QUANTLETS = [q_fw_volume, q_crisis_cal22, q_cal_by_trade, q_fwd_curve, q_premium, q_spreads, q_spark_hourly,
             q_hedge_scatter, q_basis, q_shape, q_samuelson, q_collar, q_case2026]


# ---------------------------------------------------------------------------------------------------------------
# check: every number printed with [key] equals the value in L5_numbers.json
# ---------------------------------------------------------------------------------------------------------------
LINE = re.compile(r"^(.*?)\s+(\S+)\s+\[([^\]]+)\]\s*$")


def lookup(key):
    x = N
    for p in key.split("."):
        x = x[p]
    return x


def check(q):
    nb = nbformat.read(os.path.join(q.folder, q.name + ".ipynb"), as_version=4)
    bad, n = [], 0
    for c in nb.cells:
        for o in c.get("outputs", []):
            if o.get("output_type") == "error":
                bad.append(f"error: {o.get('ename')}: {o.get('evalue')}")
            for ln in (o.get("text", "") if o.get("output_type") == "stream" else "").splitlines():
                m = LINE.match(ln)
                if not m:
                    continue
                s, key = m.group(2), m.group(3)
                n += 1
                try:
                    ref = lookup(key)
                except (KeyError, TypeError):
                    bad.append(f"{key}: not in L5_numbers.json")
                    continue
                if isinstance(ref, str):
                    if s != ref:
                        bad.append(f"{key}: notebook {s} vs JSON {ref}")
                    continue
                v = float(s.replace(",", ""))
                dec = len(s.split(".")[1]) if "." in s else 0
                if abs(v - float(ref)) > 0.5 * 10 ** -dec + 1e-6:      # equal up to the printed precision
                    bad.append(f"{key}: notebook {s} vs JSON {ref}")
    return n, bad


def main(names):
    report = []
    for f in QUANTLETS:
        q = f()
        if names and q.chart not in names:
            continue
        q.write(execute=True)
        n, bad = check(q)
        report.append((q.name, n, bad))
        print(f"  {n} numbers checked against L5_numbers.json" + ("" if not bad else ": MISMATCH " + "; ".join(bad)))
    nbad = sum(len(b) for _, _, b in report)
    print(f"\n{len(report)} Quantlets written; {sum(n for _, n, _ in report)} numbers checked; {nbad} mismatches")
    if nbad:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
