"""
make_quantlets_L1.py -- one Quantlet per chart of Lecture 1 (EMQA)
===================================================================
Writes and executes Quantlets/L1/EMQA_L1_<chart>/ for every chart shown in the Lecture 1 deck:
    Metainfo.txt, EMQA_L1_<chart>.ipynb (self-contained, executed), <chart>.png
Each notebook loads only the data it needs (local data/clean or the public repository on GitHub), contains only
the code of its chart (copied from analysis_L1.py, English labels, course chart style inlined) and prints the
numbers shown on the slide, each tagged with its key in L1_numbers.json. After execution this script compares
every printed number with L1_numbers.json and stops if one differs.
Run from the repository root:  python3 lectures/L1/make_quantlets_L1.py [chart ...]
"""

import json
import os
import re
import sys

import nbformat

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_quantlet import Quantlet  # noqa: E402

with open(os.path.join(HERE, "L1_numbers.json")) as f_:
    N = json.load(f_)
PERIOD = {k: v["period_en"] for k, v in N["charts"].items()}
SOURCE = {k: v["source_en"] for k, v in N["charts"].items()}

# ---------------------------------------------------------------------------------------------------------------
# cells shared by the notebooks (inlined in every notebook, so each one runs on its own)
# ---------------------------------------------------------------------------------------------------------------
SETUP = r'''import json
import urllib.request
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
warnings.filterwarnings('ignore')

# course chart style: transparent background, no gridlines, legend at the bottom outside the axes
plt.rcParams.update({
    'figure.facecolor': 'none', 'axes.facecolor': 'none', 'savefig.transparent': True,
    'axes.grid': False, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.edgecolor': '#222222', 'axes.labelcolor': '#222222', 'xtick.color': '#222222', 'ytick.color': '#222222',
    'text.color': '#222222', 'font.size': 11, 'axes.titlesize': 11.5, 'axes.labelsize': 11,
    'legend.fontsize': 10.5, 'legend.frameon': False, 'lines.linewidth': 1.4, 'font.family': 'DejaVu Sans'})
PAL = {'RO': '#2a78d6', 'DE_LU': '#eb6834', 'HU': '#1baf7a', 'BG': '#eda100',
       'c5': '#e87ba4', 'c6': '#008300', 'c7': '#6250d6', 'c8': '#e34948'}   # fixed colour per bidding zone
SERIES = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948']
ZONE_LS = {'RO': '-', 'BG': '--', 'HU': '-.', 'DE_LU': ':'}
ZONES = ['RO', 'BG', 'HU', 'DE_LU']
ZONE_NAME = {'RO': 'Romania (OPCOM PZU)', 'BG': 'Bulgaria (IBEX)', 'HU': 'Hungary (HUPX)', 'DE_LU': 'Germany-Luxembourg'}
MON_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ZONE_SHORT = {'RO': 'RO (OPCOM PZU)', 'BG': 'BG (IBEX)', 'HU': 'HU (HUPX)', 'DE_LU': 'DE-LU (EPEX SPOT)'}


def month_ticks(ax, step=1):
    """Month axis 1..12: every month named, written vertically so it fits."""
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels([MON_EN[m - 1] if (m - 1) % step == 0 else '' for m in range(1, 13)], fontsize=9, rotation=90)


def legend_bottom(fig, ncol=4, y=0.0):
    """One legend centred under the axes, outside the plotting area."""
    handles, labels = [], []
    for ax in fig.axes:
        for h, l_ in zip(*ax.get_legend_handles_labels()):
            if l_ not in labels:
                handles.append(h)
                labels.append(l_)
    if handles:
        fig.legend(handles, labels, loc='lower center', ncol=ncol, bbox_to_anchor=(0.5, y), frameon=False,
                   handlelength=2.0, columnspacing=1.2)


def fl(x, k=4):
    """Round as on the slides."""
    return None if x is None or np.isnan(float(x)) else round(float(x), k)


def d(ts):
    return pd.Timestamp(ts).strftime('%Y-%m-%d')


def show(key, label, value):
    """Print a number of the slide; [key] = its name in lectures/L1/L1_numbers.json."""
    print(f'{label} = {value}   [{key}]')'''

CUTOFF = r'''# data cut-off: last complete calendar month common to the Romanian prices and the generation data
_p = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', usecols=['date_cet', 'RO'], parse_dates=['date_cet']).set_index('date_cet')['RO']
_g = pd.read_csv(DATA + 'generation_ro_mw_daily_cet.csv', usecols=['date_cet', 'hydro_run_of_river'],
                 parse_dates=['date_cet']).set_index('date_cet')['hydro_run_of_river']
_last = min(_p.dropna().index.max(), _g.dropna().index.max())
END = pd.Timestamp(((_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())
END_UTC = (END + pd.Timedelta(days=1)).tz_localize('Europe/Brussels').tz_convert('UTC')   # end of the CET day, in UTC
Y = END.year
print('data cut-off:', END.date())'''

LOAD = {
    "P": "# daily base prices (mean of all market time units of the CET/CEST day), EUR/MWh\n"
         "P = pd.read_csv(DATA + 'power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet').loc[:END]",
    "X": "# native-resolution day-ahead prices (60-min until Sep 2025, 15-min from 1 Oct 2025), CET/CEST clock\n"
         "X = pd.read_csv(DATA + 'power_da_prices_native_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
         "X.index = X.index.tz_convert('Europe/Brussels')\nX = X.loc[:str(END.date())]",
    "H": "# hourly day-ahead prices (15-min prices averaged to the hour from Oct 2025), CET/CEST clock\n"
         "H = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
         "H.index = H.index.tz_convert('Europe/Brussels')\nH = H.loc[:str(END.date())]",
    "G": "# Romanian generation by source, daily mean MW (CET day)\n"
         "G = pd.read_csv(DATA + 'generation_ro_mw_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet').loc[:END]",
    "GH": "# Romanian generation by source and load, hourly mean MW (UTC, interval start)\n"
          "GH = pd.read_csv(DATA + 'generation_ro_mw_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
          "GH = GH.loc[GH.index < END_UTC]",
    "BGH": "# Bulgarian generation (incl. battery discharge and charging), hourly mean MW (UTC)\n"
           "BGH = pd.read_csv(DATA + 'generation_bg_mw_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')\n"
           "BGH = BGH.loc[BGH.index < END_UTC]",
    "CB": "# Romanian cross-border physical flows, daily mean MW (sum > 0 = net import)\n"
          "CB = pd.read_csv(DATA + 'crossborder_ro_mw_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet').loc[:END]",
    "F": "# Brent front-month futures (Yahoo Finance BZ=F), daily close in USD/bbl\n"
         "F = pd.read_csv(DATA + 'fuels_daily.csv', parse_dates=['date']).set_index('date').loc[:END]",
    "TTF": "# TTF natural gas, monthly mean in EUR/MWh (World Bank)\n"
           "TTF = pd.read_csv(DATA + 'ttf_monthly.csv')\nTTF.index = pd.PeriodIndex(TTF['month'], freq='M').to_timestamp()\n"
           "TTF = TTF.drop(columns='month').loc[:END]",
}

BRENT = r'''# Brent: the continuous front-month series switches contract on the first trading day of each month;
# that day's change mixes price and roll, so it is dropped from the return statistics
b = F['brent_usd_bbl'].dropna()
ROLL = b.groupby(b.index.to_period('M')).head(1).index
rb_all = np.log(b).diff().dropna() * 100                         # daily log returns, %
rb = rb_all.drop(rb_all.index.intersection(ROLL))                # roll days removed'''

GRP = r'''# source groups: a group is reported in an hour only if all its parts are reported
GRP = {'Hydro': ['hydro_run_of_river', 'hydro_water_reservoir'], 'Coal': ['brown_coal_lignite', 'hard_coal'],
       'Nuclear': ['nuclear'], 'Gas': ['gas'], 'Wind': ['wind_onshore'], 'Solar': ['solar'], 'Biomass': ['biomass']}
yr = GH.index.year
full_years = [y for y in sorted(set(yr)) if y < Y]
mix, cov = {}, {}
for k, cols in GRP.items():
    s = GH[cols].sum(axis=1, min_count=len(cols))
    mix[k] = s.groupby(yr).sum() / 1e6                           # TWh = sum of hourly mean MW x 1 h / 1e6
    cov[k] = s.notna().groupby(yr).mean()                        # share of hours reported
mix, cov = pd.DataFrame(mix), pd.DataFrame(cov)'''

LFL = r'''def lfl_block(cols, y0, y1):
    """Jan..cut-off month of y1 vs the same months of y0, over the hours reported in BOTH years (TWh)."""
    s = GH[cols].sum(axis=1, min_count=len(cols))
    a = s[(s.index.year == y1) & (s.index.month <= END.month)]
    b_ = s[(s.index.year == y0) & (s.index.month <= END.month)]
    A = pd.Series(a.values, index=a.index.strftime('%m-%d %H'))
    B = pd.Series(b_.values, index=b_.index.strftime('%m-%d %H'))
    A, B = A[~A.index.duplicated()], B[~B.index.duplicated()]
    both = pd.concat([A.rename('a'), B.rename('b')], axis=1).dropna()
    return {'ytd': fl(both['a'].sum() / 1e6, 2), 'prev': fl(both['b'].sum() / 1e6, 2),
            'chg': fl((both['a'].sum() / both['b'].sum() - 1) * 100, 1), 'ytd_own': fl(A.sum() / 1e6, 2)}'''

ORDER = r'''ORDER = ['Hydro', 'Nuclear', 'Coal', 'Gas', 'Wind', 'Solar', 'Biomass']
SCOL = {'Hydro': PAL['RO'], 'Nuclear': PAL['c7'], 'Coal': '#5b4a3a', 'Gas': PAL['DE_LU'], 'Wind': PAL['HU'],
        'Solar': PAL['BG'], 'Biomass': PAL['c6']}'''


def savefig(chart, bottom):
    return (f"fig.tight_layout(rect=(0, {bottom}, 1, 1))\n"
            f"plt.savefig('{chart}.png', dpi=150, bbox_inches='tight', transparent=True)\nplt.show()")


# ---------------------------------------------------------------------------------------------------------------
# the charts of the Lecture 1 deck (build_L1.py), with the code of each one (copied from analysis_L1.py)
# ---------------------------------------------------------------------------------------------------------------
Q = []


def add(chart, title, what, keywords, datafile, loads, compute, plot, bottom=0.17, intro=""):
    Q.append(dict(chart=chart, title=title, what=what, keywords=keywords, datafile=datafile, loads=loads,
                  compute=compute, plot=plot + "\n" + savefig(chart, bottom), intro=intro))


EC = "energy-charts.info (Fraunhofer ISE), data/clean/"

add("mix_ro_annual", "Romania's electricity generation mix by source",
    "Annual Romanian electricity generation by source (hydro, nuclear, coal, gas, wind, solar, biomass) in TWh for the full "
    "years, with load as a black bar, and the shares of each source in January to the cut-off month of the current and the "
    "previous year over the hours reported in both years. Energy is summed over reported hours; coverage is reported",
    "electricity, generation mix, Romania, hydro, nuclear, coal, solar, energy, TWh, coverage, missing data",
    "Romanian hourly generation by source and load (energy-charts.info, ENTSO-E; data/clean/generation_ro_mw_hourly_utc.csv)",
    ["GH"],
    GRP + "\nload_twh = GH['load'].groupby(yr).sum() / 1e6\n\n" + LFL + "\n\n" + r'''L = {k: lfl_block(c, Y - 1, Y) for k, c in GRP.items()}
tot_a, tot_b = sum(L[k]['ytd'] for k in GRP), sum(L[k]['prev'] for k in GRP)
for k in GRP:
    L[k]['share_ytd'] = fl(L[k]['ytd'] / tot_a * 100, 1)
    L[k]['share_prev'] = fl(L[k]['prev'] / tot_b * 100, 1)

show('mix.min_cov_full', 'lowest coverage of a source in a full year, %', fl(cov.loc[full_years].min().min() * 100, 1))
for y in [full_years[0], full_years[-1]]:
    show(f'mix.{y}.total_twh', f'generation {y}, TWh', fl(mix.loc[y].sum(), 2))
    show(f'mix.{y}.load_twh', f'load {y}, TWh', fl(load_twh.loc[y], 2))
for k in GRP:
    show(f'mix.lfl.{k}.share_prev', f'{k} share, Jan-{MON_EN[END.month - 1]} {Y - 1}, %', L[k]['share_prev'])
    show(f'mix.lfl.{k}.share_ytd', f'{k} share, Jan-{MON_EN[END.month - 1]} {Y}, %', L[k]['share_ytd'])''',
    ORDER + "\n" + r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.5), gridspec_kw={'width_ratios': [1.45, 1]})
bot = np.zeros(len(full_years))
for k in ORDER:
    axs[0].bar(full_years, mix.loc[full_years, k].values, bottom=bot, color=SCOL[k], label=k, width=0.72,
               edgecolor='white', lw=0.8)
    bot += mix.loc[full_years, k].values
axs[0].plot(full_years, load_twh.loc[full_years], 'k_', ms=17, mew=2.2, label='Load (consumption)')
axs[0].set_ylabel('TWh per year')
axs[0].set_xticks(full_years)
axs[0].set_xticklabels([str(y)[2:] for y in full_years])
sh = pd.DataFrame({0: [L[k]['share_prev'] for k in ORDER], 1: [L[k]['share_ytd'] for k in ORDER]}, index=ORDER)
bot = np.zeros(2)
for k in ORDER:
    axs[1].bar([0, 1], sh.loc[k].values, bottom=bot, color=SCOL[k], width=0.55, edgecolor='white', lw=0.8)
    for i in range(2):
        if sh.loc[k].values[i] > 4:
            axs[1].text(i, bot[i] + sh.loc[k].values[i] / 2, f'{sh.loc[k].values[i]:.0f}%', ha='center', va='center',
                        fontsize=9, color='white')
    bot += sh.loc[k].values
axs[1].set_xticks([0, 1])
axs[1].set_xticklabels([str(Y - 1), str(Y)])
axs[1].set_ylabel('% of generation')
axs[1].set_title(f'Jan-{MON_EN[END.month - 1]}, same hours in both years', fontsize=9.5)
legend_bottom(fig, ncol=4)''', bottom=0.22)

add("mix_shares", "Romania: shares of generation by source, 2015, last full year and current year",
    "Shares of Romanian electricity generation by source in 2015, in the last full year and in January to the cut-off "
    "month of the current year (hours reported in both the current and the previous year); prints the change of coal "
    "output, the growth of metered solar and the like-for-like change of nuclear output",
    "electricity, generation mix, Romania, coal, solar, nuclear, shares, like-for-like comparison, missing data",
    "Romanian hourly and daily generation by source (energy-charts.info, ENTSO-E; data/clean/generation_ro_mw_hourly_utc.csv, "
    "generation_ro_mw_daily_cet.csv)",
    ["GH", "G"],
    GRP + "\nshare = mix.div(mix.sum(axis=1), axis=0) * 100\n\n" + LFL + "\n\n" + r'''L = {k: lfl_block(c, Y - 1, Y) for k, c in GRP.items()}
tot_a = sum(L[k]['ytd'] for k in GRP)
for k in GRP:
    L[k]['share_ytd'] = fl(L[k]['ytd'] / tot_a * 100, 1)
gn = G.loc[str(Y), 'nuclear']

show('mix.first', 'first full year', full_years[0])
show('mix.last', 'last full year', full_years[-1])
show('mix.coal_change_pct', 'coal output, change first -> last full year, %',
     fl((mix.loc[full_years[-1], 'Coal'] / mix.loc[full_years[0], 'Coal'] - 1) * 100, 1))
show('mix.solar_x', 'metered solar, last / first full year', fl(mix.loc[full_years[-1], 'Solar'] / mix.loc[full_years[0], 'Solar'], 1))
show('mix.lfl.Nuclear.chg', f'nuclear, Jan-{MON_EN[END.month - 1]} {Y} vs {Y - 1}, %', L['Nuclear']['chg'])
show('nuclear.missing_days', f'days of {Y} without reported nuclear output', int(gn.isna().sum()))''',
    ORDER + "\n" + r'''fig, ax = plt.subplots(figsize=(6.4, 2.3))
yy = np.arange(len(ORDER))
for i, (lab, vals, col) in enumerate([('2015', [share.loc[2015, k] for k in ORDER], '#9aa7b8'),
                                      (str(full_years[-1]), [share.loc[full_years[-1], k] for k in ORDER], PAL['RO']),
                                      (f'{Y} (to {MON_EN[END.month - 1]})', [L[k]['share_ytd'] for k in ORDER], PAL['DE_LU'])]):
    ax.barh(yy + (i - 1) * 0.27, vals, height=0.26, color=col, label=lab)
ax.set_yticks(yy)
ax.set_yticklabels(ORDER)
ax.invert_yaxis()
ax.set_xlabel("% of Romania's generation")
legend_bottom(fig, ncol=3)''', bottom=0.12)

add("prices_daily_4zones", "Daily day-ahead prices in Romania, Bulgaria, Hungary and Germany-Luxembourg",
    "Seven-day mean of the daily base day-ahead electricity price in Romania (OPCOM PZU), Bulgaria (IBEX), Hungary (HUPX) "
    "and Germany-Luxembourg (EPEX SPOT); prints the Romanian daily maximum and its date",
    "electricity prices, day-ahead market, Romania, Bulgaria, Hungary, Germany, market coupling, energy crisis, time series",
    "Daily base day-ahead prices (energy-charts.info, from the exchanges via ENTSO-E; data/clean/power_da_prices_daily_cet.csv)",
    ["P"],
    r'''s = P['RO'].dropna()
show('stats.RO.max', 'Romanian daily maximum, EUR/MWh', fl(s.max(), 2))
show('stats.RO.max_date', 'date of the maximum', d(s.idxmax()))
show('stats.RO.mean', 'Romanian mean of the daily prices, EUR/MWh', fl(s.mean(), 2))''',
    r'''fig, ax = plt.subplots(figsize=(6.4, 2.2))
for z in ['DE_LU', 'HU', 'BG', 'RO']:
    s7 = P[z].dropna().rolling(7, min_periods=7).mean()
    ax.plot(s7.index, s7, color=PAL[z], ls=ZONE_LS[z], lw=1.0, label=ZONE_SHORT[z])
ax.set_ylabel('EUR/MWh\n(7-day mean)')
legend_bottom(fig, ncol=4)''')

add("profile_intraday", "Intraday price profile, Romania and Germany, 2019 vs 2025",
    "Mean day-ahead price by hour of the day (CET/CEST) in Romania and Germany-Luxembourg, calendar years 2019 and 2025: "
    "solar moved the cheapest hour of the day from the night to midday",
    "electricity prices, intraday seasonality, solar, duck curve, Romania, Germany, hourly profile",
    "Hourly day-ahead prices (energy-charts.info, from the exchanges via ENTSO-E; data/clean/power_da_prices_hourly_utc.csv)",
    ["H"],
    r'''hh = H.copy()
hh['hour'] = hh.index.hour
prof = {y: hh.loc[str(y)].groupby('hour')[['RO', 'DE_LU']].mean() for y in [2019, 2025]}
for y in [2019, 2025]:
    pr = prof[y]['RO']
    show(f'season.intraday.RO_{y}.min_h', f'RO {y}: cheapest hour', int(pr.idxmin()))
    show(f'season.intraday.RO_{y}.min', f'RO {y}: lowest hourly mean, EUR/MWh', fl(pr.min(), 1))
    show(f'season.intraday.RO_{y}.max', f'RO {y}: highest hourly mean, EUR/MWh', fl(pr.max(), 1))
    show(f'season.intraday.RO_{y}.ratio_19_13', f'RO {y}: price at 19:00 / price at 13:00', fl(pr.loc[19] / pr.loc[13], 2))''',
    r'''ZL = {'RO': 'RO', 'DE_LU': 'DE-LU'}
fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2))
for ax, z in zip(axs, ['RO', 'DE_LU']):
    for y, ls in [(2019, '--'), (2025, '-')]:
        ax.plot(prof[y].index, prof[y][z], color=PAL[z], ls=ls, marker='o', ms=3.5, label=f'{ZL[z]} {y}')
    ax.set_title(ZONE_NAME[z])
    ax.set_xlabel('Hour of day (CET/CEST)')
    ax.set_xticks(range(0, 24, 3))
axs[0].set_ylabel('EUR/MWh')
legend_bottom(fig, ncol=4)''')

add("profile_annual", "Annual seasonality: load, hydro, solar and the Romanian price by month",
    "Monthly profile of Romanian load, hydro and solar generation (mean GW) and of the Romanian day-ahead price relative to "
    "its annual mean (median over the years): spring is cheap when water and sun meet mild demand",
    "seasonality, monthly profile, electricity prices, hydro, solar, load, Romania",
    "Daily Romanian generation and load and daily day-ahead prices (energy-charts.info; data/clean/generation_ro_mw_daily_cet.csv, "
    "power_da_prices_daily_cet.csv)",
    ["G", "P"],
    r'''fy1 = Y - 1                                                    # last full year
mm = G.loc['2016':str(fy1)].resample('MS').mean()
pm = P['RO'].loc['2016':str(fy1)].resample('MS').mean()
ratio = pm / pm.groupby(pm.index.year).transform('mean')        # monthly price / mean of that year
mprof = pd.DataFrame({'load': mm['load'].groupby(mm.index.month).mean() / 1000,
                      'hydro': (mm['hydro_run_of_river'] + mm['hydro_water_reservoir']).groupby(mm.index.month).mean() / 1000,
                      'solar': mm['solar'].groupby(mm.index.month).mean() / 1000,
                      'price_ratio': ratio.groupby(ratio.index.month).median()})
show('season.annual.price_max_m', 'month with the highest relative price', int(mprof['price_ratio'].idxmax()))
show('season.annual.price_max', 'highest relative price', fl(mprof['price_ratio'].max(), 2))
show('season.annual.price_min_m', 'month with the lowest relative price', int(mprof['price_ratio'].idxmin()))
show('season.annual.price_min', 'lowest relative price', fl(mprof['price_ratio'].min(), 2))
show('season.annual.load_max_m', 'month with the highest load', int(mprof['load'].idxmax()))''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.3))
for c, col, lab in [('load', '#222222', 'Load (consumption)'), ('hydro', PAL['RO'], 'Hydro (run-of-river + reservoir)'),
                    ('solar', PAL['BG'], 'Solar')]:
    axs[0].plot(range(1, 13), mprof[c], color=col, marker='o', ms=4, label=lab)
axs[0].set_ylabel('Mean power, GW')
axs[0].set_title('Load and generation, RO')
axs[1].bar(range(1, 13), mprof['price_ratio'], color=PAL['RO'], width=0.65, label='Price / annual mean (median of years)')
axs[1].axhline(1.0, color='#222222', lw=0.8)
axs[1].set_ylim(0.6, 1.4)
axs[1].set_title('RO day-ahead price by month')
for ax in axs:
    month_ticks(ax)
legend_bottom(fig, ncol=2)''', bottom=0.22)

add("negative_prices", "Negative day-ahead prices per year and by hour of the day",
    "Hours with negative day-ahead prices per year in Romania, Bulgaria, Hungary and Germany-Luxembourg (hour-equivalents: "
    "a 15-minute market time unit counts 0.25 h), and the Romanian negative hours by hour of the day since 2024",
    "negative prices, electricity, day-ahead market, solar, Romania, hour-equivalents, 15-minute MTU",
    "Day-ahead prices at native resolution (energy-charts.info, from the exchanges via ENTSO-E; "
    "data/clean/power_da_prices_native_utc.csv)",
    ["X"],
    r'''hrs = X['mtu_minutes'] / 60.0                                 # duration of each market time unit, hours
neg = {z: ((X[z] < 0) & X[z].notna()).mul(hrs).groupby(X.index.year).sum() for z in ZONES}
ro = X['RO'].dropna()
r24 = X.loc['2024-01-01':, ['RO', 'mtu_minutes']].dropna()
negh = (r24['RO'] < 0) * r24['mtu_minutes'] / 60
hneg = negh.groupby(r24.index.hour).sum()
show('neg.ro_first', 'first negative Romanian price', d(ro[ro < 0].index.min()))
for y in [2024, 2025, Y]:
    show(f'neg.hours.RO.{y}', f'RO negative hours {y}', fl(neg['RO'].loc[y], 2))
show('neg.ro_share_10_16', 'share of RO negative hours 10:00-16:00 (2024 to date), %', fl(hneg.loc[10:15].sum() / hneg.sum() * 100, 1))
show('neg.ro_share_weekend', 'share of RO negative hours on weekends, %',
     fl(negh[r24.index.dayofweek >= 5].sum() / negh.sum() * 100, 1))''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.4), gridspec_kw={'width_ratios': [1.35, 1]})
yrs = list(range(2018, Y + 1))
for i, z in enumerate(ZONES):
    axs[0].bar(np.array(yrs) + (i - 1.5) * 0.2, [neg[z].loc[y] for y in yrs], width=0.2, color=PAL[z], label=ZONE_SHORT[z])
axs[0].set_ylabel('Hours < 0')
axs[0].set_xticks(yrs)
axs[0].set_xticklabels([(str(y) if y % 2 == 0 else '') if y < Y else f'{y}\nYTD' for y in yrs])
axs[1].bar(hneg.index, hneg.values, color=PAL['RO'], width=0.75)
axs[1].set_xlabel('Hour of day (CET/CEST)')
axs[1].set_ylabel('Hours < 0')
axs[1].set_title('RO, by hour of day (2024 to date)')
axs[1].set_xticks(range(0, 24, 6))
legend_bottom(fig, ncol=4)''', bottom=0.12)

add("negative_solar", "Romanian negative-price hours by month, and solar generation by year",
    "Romanian negative-price hours by month and year since 2023 (hour-equivalents) and metered Romanian solar generation "
    "per full year since 2018: negative hours cluster in spring as solar grows",
    "negative prices, solar, seasonality, Romania, electricity, hour-equivalents",
    "Day-ahead prices at native resolution and Romanian hourly generation (energy-charts.info, ENTSO-E; "
    "data/clean/power_da_prices_native_utc.csv, generation_ro_mw_hourly_utc.csv)",
    ["X", "GH"],
    r'''hrs = X['mtu_minutes'] / 60.0
hm = ((X['RO'] < 0) & X['RO'].notna()).mul(hrs).loc['2023-01-01':]
hm = hm.groupby([hm.index.year, hm.index.month]).sum().unstack(0)          # months x years, hours < 0
yr = GH.index.year
full_years = [y for y in sorted(set(yr)) if y < Y]
solar = GH['solar'].groupby(yr).sum() / 1e6                                # TWh over reported hours

''' + LFL + r'''

show('neg.share_apr_may', 'share of negative hours in April-May, %', fl(hm.loc[[4, 5]].sum().sum() / hm.sum().sum() * 100, 1))
show('neg.share_jun_aug', 'share of negative hours in June-August, %', fl(hm.loc[[6, 7, 8]].sum().sum() / hm.sum().sum() * 100, 1))
for y in [2023, 2025]:
    show(f'neg.solar_twh.{y}', f'metered solar {y}, TWh', fl(solar.loc[y], 2))
show('mix.lfl.Solar.ytd_own', f'metered solar Jan-{MON_EN[END.month - 1]} {Y}, TWh', lfl_block(['solar'], Y - 1, Y)['ytd_own'])''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2))
bot = np.zeros(12)
for i, y in enumerate(hm.columns):
    v = hm[y].reindex(range(1, 13)).fillna(0.0).values                    # months after the cut-off have no bar
    axs[0].bar(range(1, 13), v, bottom=bot, color=SERIES[i], width=0.7, edgecolor='white', lw=0.6,
               label=f'{y}' + (' (YTD)' if y == Y else ''))
    bot += v
month_ticks(axs[0])
axs[0].set_ylabel('Hours')
axs[0].set_title('Negative-price hours, RO', fontsize=10.5)
sy = [y for y in full_years if y >= 2018]
axs[1].bar(sy, [solar.loc[y] for y in sy], color=PAL['BG'], width=0.6)
axs[1].set_xticks(sy)
axs[1].set_xticklabels([str(y)[2:] for y in sy])
axs[1].set_title('Solar, RO, TWh (metered)', fontsize=10.5)
legend_bottom(fig, ncol=4)''')

add("day_load", "One day of Romanian consumption: power (MW) and energy (MWh)",
    "Hourly Romanian load on the most recent Wednesday (CET day) with all 24 hours reported: the curve is power in MW, "
    "the shaded area is the energy of the day in MWh",
    "load, power, energy, MW, MWh, Romania, electricity consumption, units",
    "Romanian hourly load (energy-charts.info, ENTSO-E, Transelectrica data; data/clean/generation_ro_mw_hourly_utc.csv)",
    ["GH"],
    r'''ld = GH['load'].tz_convert('Europe/Brussels')
cnt = ld.groupby(ld.index.date).count()
day = max(k for k, v in cnt.items() if v == 24 and pd.Timestamp(k).dayofweek == 2)   # last complete Wednesday
DAYLOAD = ld[ld.index.date == day]
mwh = int(round(DAYLOAD.sum()))                                # 24 x mean MW x 1 h
show('dayload.day', 'day', str(day))
show('dayload.mwh', 'energy of the day, MWh', mwh)
show('dayload.mean_mw', 'mean power, MW', int(round(DAYLOAD.mean())))
show('dayload.min_mw', 'minimum power, MW', int(round(DAYLOAD.min())))
show('dayload.min_h', 'hour of the minimum (CET)', int(DAYLOAD.idxmin().hour))
show('dayload.max_mw', 'maximum power, MW', int(round(DAYLOAD.max())))
show('dayload.max_h', 'hour of the maximum (CET)', int(DAYLOAD.idxmax().hour))''',
    r'''fig, ax = plt.subplots(figsize=(6.4, 2.0))
hh = np.arange(24)
v = np.append(DAYLOAD.values, DAYLOAD.values[-1])
ax.step(np.append(hh, 24), v, where='post', color=PAL['RO'], lw=1.6)
ax.fill_between(np.append(hh, 24), v, step='post', color=PAL['RO'], alpha=0.18)
ax.set_xlim(0, 24)
ax.set_xticks(range(0, 25, 3))
ax.set_ylim(0, DAYLOAD.max() * 1.15)
ax.set_xlabel('hour (CET)')
ax.set_ylabel('MW')
ax.text(12, DAYLOAD.mean() * 0.5, f"area = {mwh:,} MWh = the day's energy", ha='center', fontsize=9.5)''', bottom=0.22)

add("merit_opcom", "The merit order on real OPCOM day-ahead curves",
    "Aggregated supply and demand curves of the Romanian day-ahead market (OPCOM PZU) for one delivery day, midday "
    "(12:00-12:15) and evening (20:00-20:15) quarter-hours, with the official clearing price: the price is set where "
    "the curves cross",
    "merit order, supply curve, demand curve, day-ahead market, OPCOM, clearing price, order book, Romania",
    "OPCOM PZU aggregated curves for one day (data/clean/opcom_pzu_curves.csv and opcom_pzu_curves_meta.json)",
    [],
    r'''CURVES = pd.read_csv(DATA + 'opcom_pzu_curves.csv')
meta_path = DATA + 'opcom_pzu_curves_meta.json'
CMETA = json.load(urllib.request.urlopen(meta_path)) if meta_path.startswith('http') else json.load(open(meta_path))
day = CURVES['delivery_date'].iloc[0]
M = {}
for iv in CMETA['intervals']:
    k = 'mid' if iv['opcom_interval'] == 45 else 'eve'
    s = CURVES[(CURVES['interval'] == iv['interval_label']) & (CURVES['side'] == 'supply')]
    M[k] = {'label': iv['interval_label'], 'price': iv['official_clearing_price_eur_mwh'], 'q': iv['curve_cleared_quantity_mw'],
            'q_le0': fl(s.loc[s['price_eur_mwh'] <= 0, 'quantity_mw'].max(), 0), 'net_imp': fl(-iv['net_export_mw'], 0)}
show('merit.day', 'delivery day', day)
for k in ['mid', 'eve']:
    show(f'merit.{k}.price', f'{k}: clearing price, EUR/MWh', M[k]['price'])
    show(f'merit.{k}.q_le0', f'{k}: supply offered at a price <= 0, MW', M[k]['q_le0'])
    show(f'merit.{k}.net_imp', f'{k}: net imports in the supply, MW', M[k]['net_imp'])''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.5), sharey=True)
for ax, k in zip(axs, ['mid', 'eve']):
    m = M[k]
    for side, col, lab in [('supply', PAL['RO'], 'supply (sell)'), ('demand', '#222222', 'demand (buy)')]:
        c = CURVES[(CURVES['interval'] == m['label']) & (CURVES['side'] == side)]
        ax.plot(c['quantity_mw'] / 1000, c['price_eur_mwh'].clip(-190, 660), color=col, lw=1.4, label=lab)
    ax.axhline(m['price'], color='#b2182b', ls='--', lw=0.9)
    ax.plot([m['q'] / 1000], [m['price']], 'o', color='#b2182b', ms=5)
    ax.annotate(f"price {m['price']:.2f}", (0.05, m['price']), textcoords='offset points', xytext=(0, 4), fontsize=8.5,
                color='#b2182b')
    ax.set_title({'mid': '12:00-12:15 (midday)', 'eve': '20:00-20:15 (evening)'}[k], fontsize=10)
    ax.set_ylim(-330, 760)
    ax.set_xlim(0, 4)
    # the curves are clipped at -190 and 660 EUR/MWh: the labels sit just outside the clipped lines, clear of the curves
    ax.text(0.05, -215, 'sell at any price (−600)', fontsize=8.5, color=PAL['RO'], va='top')
    ax.text(0.05, 685, 'buy at any price (+4000)', fontsize=8.5, color='#222222', va='bottom')
    ax.set_xlabel('cumulative quantity (GW)')
axs[0].set_ylabel('EUR/MWh')
legend_bottom(fig, ncol=2)''', bottom=0.12)

add("asinh_ro", "Romanian 15-minute prices: level vs asinh transform",
    "Histogram of all Romanian 15-minute day-ahead prices of the current year to the cut-off, in levels and after the "
    "variance-stabilising area hyperbolic sine transform asinh((p - median)/MAD), which handles zero and negative prices "
    "where a logarithm cannot",
    "variance stabilising transformation, asinh, negative prices, skewness, kurtosis, electricity prices, Romania",
    "Day-ahead prices at native resolution (energy-charts.info, OPCOM via ENTSO-E; data/clean/power_da_prices_native_utc.csv)",
    ["X"],
    r'''from scipy import stats
y26 = X.loc[str(Y), 'RO'].dropna()                            # current year to cut-off: all 15-min MTUs
med = float(y26.median())
mad = float(stats.median_abs_deviation(y26, scale='normal'))
z26 = np.arcsinh((y26 - med) / mad)
show('trans.n', 'number of 15-min MTUs', int(len(y26)))
show('trans.n_le0', 'MTUs with price <= 0', int((y26 <= 0).sum()))
show('trans.n_eq0', 'MTUs with price = 0', int((y26 == 0).sum()))
show('trans.median', 'median, EUR/MWh', fl(med, 2))
show('trans.mad', 'MAD (normal-consistent), EUR/MWh', fl(mad, 2))
show('trans.skew_level', 'skewness, level', fl(stats.skew(y26), 2))
show('trans.kurt_level', 'excess kurtosis, level', fl(stats.kurtosis(y26), 2))
show('trans.skew_asinh', 'skewness, asinh', fl(stats.skew(z26), 2))
show('trans.kurt_asinh', 'excess kurtosis, asinh', fl(stats.kurtosis(z26), 2))''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.8))
axs[0].hist(y26.clip(upper=450), bins=np.arange(-150, 455, 5), color=PAL['RO'])
axs[0].set_title(f'RO 15-min prices, Jan-{MON_EN[END.month - 1]} {Y}', fontsize=10.5)
axs[0].axvline(0, color='#222222', lw=0.8)
axs[0].set_xlim(-150, 450)
axs[0].set_xlabel('Level $p_t$, EUR/MWh')
axs[0].set_ylabel('Count')
axs[1].hist(z26, bins=120, color=PAL['HU'])
axs[1].set_xlabel('transformed value')
axs[1].set_title('Variance-stabilised: asinh', fontsize=10.5)''', bottom=0.0)

add("tails_brent", "Fat tails of Brent daily returns: Q-Q plot and density",
    "Normal Q-Q plot and log-scale density of standardised Brent front-month daily log returns (contract-roll days "
    "removed), compared with the normal distribution and a fitted Student-t: far more 4-sigma days than the normal predicts",
    "fat tails, kurtosis, Q-Q plot, Student-t, Brent, crude oil, returns, normality",
    "Brent front-month futures daily close (Yahoo Finance BZ=F; data/clean/fuels_daily.csv)",
    ["F"],
    BRENT + "\n\n" + r'''from scipy import stats
tpar = stats.t.fit(rb)                                          # Student-t: df, location, scale
show('tails.start', 'first return', d(rb.index.min()))
show('tails.end', 'last return', d(rb.index.max()))
show('tails.n', 'number of returns', int(len(rb)))
show('tails.n_roll', 'roll days removed', int(len(rb_all) - len(rb)))
show('tails.exkurt', 'excess kurtosis', fl(stats.kurtosis(rb), 2))
show('tails.t_df', 'fitted Student-t degrees of freedom', fl(tpar[0], 2))
show('tails.n_4sd', 'days beyond 4 standard deviations', int((rb.abs() > 4 * rb.std()).sum()))
show('tails.n_4sd_normal', 'expected under the normal', fl(len(rb) * 2 * stats.norm.sf(4), 2))''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.85))
zz = (rb - rb.mean()) / rb.std()
osm, osr = stats.probplot(zz, dist='norm', fit=False)
axs[0].plot(osm, osr, 'o', ms=2.5, color=PAL['RO'], label='Brent returns (standardised)')
axs[0].plot([-4.5, 4.5], [-4.5, 4.5], color=PAL['c8'], lw=1.2, label='Normal')
axs[0].set_xlabel('Normal quantile')
axs[0].set_ylabel('Empirical')
axs[0].set_title('Q-Q plot')
xs = np.linspace(-8, 8, 400)
sc = np.sqrt(tpar[0] / (tpar[0] - 2))                           # unit-variance Student-t
axs[1].hist(zz, bins=150, density=True, color=PAL['RO'], alpha=0.55)
axs[1].plot(xs, stats.norm.pdf(xs), color=PAL['c8'], lw=1.4)
axs[1].plot(xs, stats.t(tpar[0]).pdf(xs * sc) * sc, color=PAL['c7'], lw=1.4, ls='--', label=f'Student-t, df = {tpar[0]:.1f}')
axs[1].set_xlim(-6, 6)
axs[1].set_yscale('log')
axs[1].set_ylim(1e-4, 1)
axs[1].set_title('Density (log scale)')
axs[1].set_xlabel('standardised return')
legend_bottom(fig, ncol=3)''')

add("volclust_brent", "Volatility clustering in Brent daily returns",
    "Brent front-month daily log returns (contract-roll days removed) and their 21-day rolling volatility in % a year: "
    "calm and turbulent periods cluster; Ljung-Box statistics of returns and squared returns",
    "volatility clustering, Ljung-Box, ARCH effects, Brent, crude oil, returns, rolling volatility",
    "Brent front-month futures daily close (Yahoo Finance BZ=F; data/clean/fuels_daily.csv)",
    ["F"],
    BRENT + "\n\n" + r'''from statsmodels.stats.diagnostic import acorr_ljungbox
vol = rb.rolling(21).std() * np.sqrt(252)                       # annualised, % a year
show('tails.lb_r', 'Ljung-Box Q(10), returns', fl(acorr_ljungbox(rb, lags=[10], return_df=True)['lb_stat'].iloc[0], 1))
show('tails.lb_r2', 'Ljung-Box Q(10), squared returns', fl(acorr_ljungbox(rb ** 2, lags=[10], return_df=True)['lb_stat'].iloc[0], 1))
show('tails.vol_max', 'highest 21-day volatility, % a year', fl(vol.max(), 1))
show('tails.vol_max_date', 'month of the highest volatility', vol.idxmax().strftime('%Y-%m'))
show('tails.vol_median', 'median 21-day volatility, % a year', fl(vol.median(), 1))''',
    r'''fig, axs = plt.subplots(2, 1, figsize=(6.4, 1.75), sharex=True)
axs[0].plot(rb.index, rb, color=PAL['RO'], lw=0.6, label='Brent daily log return, %')
axs[1].plot(vol.index, vol, color=PAL['DE_LU'], lw=1.0, label='21-day volatility, % a year')
axs[0].set_ylabel('%')
axs[1].set_ylabel('% a year')
legend_bottom(fig, ncol=2)''', bottom=0.13)

add("sim_wn_ar_rw", "Simulated white noise, AR(1) and random walk with their sample ACF",
    "Simulation (concept only, labelled as such on the slide): white noise, a stationary AR(1) with phi = 0.9 and a "
    "random walk built from the same 500 standard normal shocks (seed 20261104), with their sample autocorrelation "
    "functions and the white-noise band",
    "simulation, white noise, autoregressive process, AR(1), random walk, autocorrelation, ACF, stationarity",
    "None: simulated series (numpy, seed 20261104)",
    [],
    r'''from statsmodels.tsa.stattools import acf
rng = np.random.default_rng(20261104)
TS = 500
eps = rng.standard_normal(TS)
ar = np.zeros(TS)
for t in range(1, TS):
    ar[t] = 0.9 * ar[t - 1] + eps[t]
SIM = {'wn': eps, 'ar': ar, 'rw': np.cumsum(eps)}
for k, s in SIM.items():
    r = acf(s, nlags=30, fft=True)
    show(f'sim.{k}.acf1', f'{k}: sample ACF at lag 1', fl(r[1], 2))
    show(f'sim.{k}.acf10', f'{k}: sample ACF at lag 10', fl(r[10], 2))
show('sim.ar_theory_acf10', 'AR(1) theoretical ACF at lag 10 = 0.9^10', fl(0.9 ** 10, 2))''',
    r'''fig, axs = plt.subplots(2, 3, figsize=(6.4, 2.2), gridspec_kw={'height_ratios': [1, 1]})
for j, (k, col, ttl) in enumerate([('wn', PAL['RO'], 'White noise'), ('ar', PAL['HU'], 'AR(1), $\\phi=0.9$'),
                                   ('rw', PAL['DE_LU'], 'Random walk')]):
    axs[0, j].plot(SIM[k], color=col, lw=0.8)
    axs[0, j].set_title(ttl, fontsize=10.5)
    axs[0, j].yaxis.set_major_locator(plt.MaxNLocator(2))
    r = acf(SIM[k], nlags=30, fft=True)
    axs[1, j].bar(range(31), r, color=col, width=0.5)
    for sgn in (1, -1):
        axs[1, j].axhline(sgn * 1.96 / np.sqrt(TS), color='#222222', ls='--', lw=0.8)
    axs[1, j].set_ylim(-0.3, 1.05)
    axs[1, j].set_yticks([0, 1])
    axs[1, j].set_xlabel('lag $k$')
axs[1, 0].set_ylabel('sample ACF')''', bottom=0.0)

add("acf_pacf_ro_daily", "ACF and PACF of the Romanian daily day-ahead price",
    "Sample autocorrelation (with Bartlett band) and partial autocorrelation functions of the Romanian daily base "
    "day-ahead price since 2023, lags 1 to 42 days: slow decay and a weekly pattern at lags 7, 14, 21",
    "autocorrelation, partial autocorrelation, ACF, PACF, Bartlett band, weekly seasonality, electricity prices, Romania",
    "Daily base day-ahead prices (energy-charts.info, OPCOM via ENTSO-E; data/clean/power_da_prices_daily_cet.csv)",
    ["P"],
    r'''from statsmodels.tsa.stattools import acf, pacf
sA = P['RO'].loc['2023-01-01':].dropna()
K = 42
rA = acf(sA, nlags=K, fft=True)
pA = pacf(sA, nlags=K, method='ywm')
TA = len(sA)
bart = 1.96 * np.sqrt((1 + 2 * np.concatenate([[0], np.cumsum(rA[1:K] ** 2)])) / TA)   # Bartlett band
show('acf.daily.start', 'first day', d(sA.index.min()))
show('acf.daily.end', 'last day', d(sA.index.max()))
show('acf.daily.T', 'T', TA)
show('acf.daily.r1', 'ACF lag 1', fl(rA[1], 3))
show('acf.daily.r7', 'ACF lag 7', fl(rA[7], 3))
show('acf.daily.p1', 'PACF lag 1', fl(pA[1], 3))
show('acf.daily.p7', 'PACF lag 7', fl(pA[7], 3))''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.7))
axs[0].bar(range(1, K + 1), rA[1:], color=PAL['RO'], width=0.55, label='sample ACF / PACF')
axs[0].plot(range(1, K + 1), bart, color=PAL['c8'], ls='--', lw=1.1, label='Bartlett band')
axs[0].plot(range(1, K + 1), -bart, color=PAL['c8'], ls='--', lw=1.1)
axs[1].bar(range(1, K + 1), pA[1:], color=PAL['RO'], width=0.55)
for ax in axs:
    for sgn in (1, -1):
        ax.axhline(sgn * 1.96 / np.sqrt(TA), color=PAL['c7'], ls=':', lw=1.3,
                   label='white-noise band $\\pm1.96/\\sqrt{T}$' if (sgn == 1 and ax is axs[0]) else None)
    ax.axhline(0, color='#222222', lw=0.6)
    ax.set_xticks([1, 7, 14, 21, 28, 35, 42])
    ax.set_xlabel('lag (days)')
axs[0].set_title('ACF, RO daily price (level)')
axs[1].set_title('PACF, RO daily price (level)')
legend_bottom(fig, ncol=3)''')

add("acf_ro_hourly", "ACF of the Romanian hourly day-ahead price, 2024",
    "Sample autocorrelation function of the Romanian hourly day-ahead price in 2024, lags 1 to 192 hours: peaks at 24 h "
    "(daily cycle) and 168 h (weekly cycle)",
    "autocorrelation, ACF, hourly prices, daily seasonality, weekly seasonality, electricity, Romania",
    "Hourly day-ahead prices (energy-charts.info, OPCOM via ENTSO-E; data/clean/power_da_prices_hourly_utc.csv)",
    ["H"],
    r'''from statsmodels.tsa.stattools import acf
hs = H.loc['2024-01-01':'2024-12-31', 'RO'].dropna()
Kh = 24 * 8
rh = acf(hs, nlags=Kh, fft=True)
show('acf.hourly.T', 'T', int(len(hs)))
show('acf.hourly.r12', 'ACF lag 12 h', fl(rh[12], 3))
show('acf.hourly.r24', 'ACF lag 24 h', fl(rh[24], 3))
show('acf.hourly.r168', 'ACF lag 168 h', fl(rh[168], 3))''',
    r'''fig, ax = plt.subplots(figsize=(6.4, 1.3))
ax.bar(range(1, Kh + 1), rh[1:], color=PAL['RO'], width=0.8, label='sample ACF, RO hourly price 2024')
for sgn in (1, -1):
    ax.axhline(sgn * 1.96 / np.sqrt(len(hs)), color=PAL['c7'], ls=':', lw=1.3,
               label='white-noise band $\\pm1.96/\\sqrt{T}$' if sgn == 1 else None)
ax.set_xticks(range(0, Kh + 1, 24))
ax.set_xlabel('lag (hours)')
legend_bottom(fig, ncol=2)''')

add("naive_bar", "Naive benchmark forecasts of Romanian hourly prices: MAE",
    "Mean absolute error of three naive day-ahead forecasts of the Romanian hourly price (same hour of day d-1, of day d-7, "
    "and the weekday/weekend naive rule: d-7 on Monday, Saturday, Sunday, d-1 otherwise), last two full years and the "
    "current year to the cut-off",
    "naive forecast, benchmark, mean absolute error, MAE, electricity price forecasting, Romania",
    "Hourly day-ahead prices (energy-charts.info, OPCOM via ENTSO-E; data/clean/power_da_prices_hourly_utc.csv)",
    ["H"],
    r'''hz = H['RO'].dropna()
tab = pd.DataFrame({'p': hz.values, 'date': hz.index.tz_localize(None).normalize(), 'hour': hz.index.hour})
tab = tab.groupby(['date', 'hour'])['p'].mean().unstack('hour')        # day x hour
lag1 = tab.shift(1, freq='D').reindex(tab.index)
lag7 = tab.shift(7, freq='D').reindex(tab.index)
naive = lag1.copy()
msk = np.isin(tab.index.dayofweek, [0, 5, 6])                          # Monday, Saturday, Sunday: use d-7
naive[msk] = lag7[msk]
nv = {}
for y in range(2019, Y + 1):
    i = tab.index.year == y
    nv[str(y)] = {'naive': fl((tab[i] - naive[i]).stack().abs().mean(), 2), 'lag1': fl((tab[i] - lag1[i]).stack().abs().mean(), 2),
                  'lag7': fl((tab[i] - lag7[i]).stack().abs().mean(), 2), 'mean': fl(tab[i].stack().mean(), 2)}
for y in [str(v) for v in range(Y - 2, Y + 1)]:
    for k in ['naive', 'lag1', 'lag7', 'mean']:
        show(f'naive.RO.{y}.{k}', f'{y}, ' + ('mean price' if k == 'mean' else f'MAE {k}') + ', EUR/MWh', nv[y][k])
show('naive.RO.n_best', 'years in which the naive rule beats both lags', int(sum(v['naive'] < min(v['lag1'], v['lag7']) for v in nv.values())))
show('naive.RO.n_years', 'years compared', len(nv))''',
    r'''fig, ax = plt.subplots(figsize=(6.4, 1.3))
yrs = [str(y) for y in range(Y - 2, Y + 1)]
for i, (k, lab, col) in enumerate([('naive', 'naive', PAL['RO']), ('lag1', 'd-1', PAL['HU']), ('lag7', 'd-7', PAL['DE_LU'])]):
    ax.bar(np.arange(3) + (i - 1) * 0.26, [nv[y][k] for y in yrs], width=0.25, color=col, label=lab)
ax.set_xticks(range(3))
ax.set_xticklabels([y if y != str(Y) else f'{Y} (YTD)' for y in yrs])
ax.set_ylabel('MAE\n(EUR/MWh)')
legend_bottom(fig, ncol=3)''', bottom=0.12)

add("decomp_load", "Decomposition of Romanian monthly load: classical vs STL",
    "Monthly mean Romanian load (GW) with the classical 2x12 centred moving-average trend and the STL trend (top), and the "
    "classical and STL seasonal components (bottom); prints the classical seasonal indices and the STL seasonal amplitude "
    "in the first and the last full year",
    "time series decomposition, trend, seasonality, STL, moving average, load, electricity demand, Romania",
    "Romanian hourly load (energy-charts.info, ENTSO-E, Transelectrica data; data/clean/generation_ro_mw_hourly_utc.csv)",
    ["GH"],
    r'''from statsmodels.tsa.seasonal import STL, seasonal_decompose
fy1 = Y - 1                                                     # last full year
lm = GH['load'].resample('MS').mean()
lm.index = lm.index.tz_localize(None)
lm = (lm.loc['2016-01-01':f'{fy1}-12-01'] / 1000).asfreq('MS')    # GW
w = np.r_[1 / 24, np.repeat(1 / 12, 11), 1 / 24]                # 2x12 centred moving average
cma = lm.rolling(13, center=True).apply(lambda v: float(np.dot(v, w)), raw=True)
raw_idx = (lm - cma).groupby(lm.index.month).mean()
sidx = raw_idx - raw_idx.mean()                                 # classical seasonal indices, sum to zero
sd_ = seasonal_decompose(lm, model='additive', period=12)
stl = STL(lm, period=12, seasonal=13, robust=True).fit()
y0s, y1s = str(lm.index[0].year), str(fy1)
show('decomp.start', 'first month', lm.index[0].strftime('%Y-%m'))
show('decomp.end', 'last month', lm.index[-1].strftime('%Y-%m'))
for m in ['Jan', 'Feb', 'May']:
    show(f'decomp.sidx.{m}', f'classical seasonal index {m}, GW', fl(sidx.loc[MON_EN.index(m) + 1], 3))
show('decomp.stl_amp_first', f'STL seasonal amplitude {y0s}, GW', fl(stl.seasonal.loc[y0s].max() - stl.seasonal.loc[y0s].min(), 2))
show('decomp.stl_amp_last', f'STL seasonal amplitude {y1s}, GW', fl(stl.seasonal.loc[y1s].max() - stl.seasonal.loc[y1s].min(), 2))''',
    r'''# side by side, one colour per method: classical = blue solid, STL = orange dashed
fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.75))
axs[0].plot(lm.index, lm, color='#222222', lw=1.0, label='RO load, GW')
axs[0].plot(cma.index, cma, color=PAL['RO'], lw=1.8, label='Classical method')
axs[0].plot(stl.trend.index, stl.trend, color=PAL['DE_LU'], lw=1.4, ls='--', label='STL')
axs[1].plot(sd_.seasonal.index, sd_.seasonal, color=PAL['RO'], lw=1.4, label='Classical method')
axs[1].plot(stl.seasonal.index, stl.seasonal, color=PAL['DE_LU'], lw=1.2, ls='--', label='STL')
axs[0].set_title('Load and trend, GW', fontsize=10.5)
axs[1].set_title('Seasonal component, GW', fontsize=10.5)
for ax in axs:
    ax.xaxis.set_major_locator(mdates.YearLocator(3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_bottom(fig, ncol=3)''', bottom=0.13)

add("smooth_brent", "Smoothing Brent: simple moving average vs EWMA",
    "Brent front-month daily close since 2024 with a 20-day simple moving average and an exponentially weighted moving "
    "average with a half-life of 10 trading days; prints the EWMA weight and the weight estimated by simple exponential smoothing",
    "smoothing, moving average, exponentially weighted moving average, EWMA, exponential smoothing, half-life, Brent, crude oil",
    "Brent front-month futures daily close (Yahoo Finance BZ=F; data/clean/fuels_daily.csv)",
    ["F"],
    r'''from statsmodels.tsa.holtwinters import SimpleExpSmoothing
b = F['brent_usd_bbl'].dropna()
bs = b.loc['2024-01-01':]
HL = 10                                                         # half-life, trading days
alpha_hl = 1 - 2 ** (-1 / HL)
ses = SimpleExpSmoothing(bs.values, initialization_method='estimated').fit()
show('smooth.start', 'first day', d(bs.index.min()))
show('smooth.end', 'last day', d(bs.index.max()))
show('smooth.alpha_hl', 'EWMA weight for a 10-day half-life', fl(alpha_hl, 4))
show('smooth.alpha_ses', 'weight estimated by simple exponential smoothing', fl(ses.params['smoothing_level'], 4))''',
    r'''fig, ax = plt.subplots(figsize=(6.4, 1.9))
ax.plot(bs.index, bs, color='#222222', lw=0.9, label='Brent (BZ=F)')
ax.plot(bs.index, bs.rolling(20).mean(), color=PAL['RO'], lw=1.6, label='20-day moving average')
ax.plot(bs.index, bs.ewm(alpha=alpha_hl, adjust=False).mean(), color=PAL['DE_LU'], lw=1.6, ls='--',
        label=f'EWMA, half-life {HL} days')
ax.set_ylabel('USD/bbl')
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
legend_bottom(fig, ncol=3)''', bottom=0.14)

add("hydro_case", "Case study: Romanian hydro output, wet 2023 vs dry 2025, and hydro vs the day-ahead price",
    "Monthly Romanian hydro generation (TWh) in the wet year 2023, the dry year 2025 and the 2015-2025 monthly mean, and a "
    "scatter of monthly hydro output against the monthly mean Romanian day-ahead price; prints the annual totals, net "
    "imports and the hydro coefficient of a regression of the price on hydro and TTF gas (HAC standard errors)",
    "hydro, drought, case study, Romania, electricity prices, regression, HAC, TTF gas, net imports",
    "Romanian hourly generation, daily cross-border flows, daily day-ahead prices (energy-charts.info, ENTSO-E) and monthly "
    "TTF gas prices (World Bank); data/clean/generation_ro_mw_hourly_utc.csv, crossborder_ro_mw_daily_cet.csv, "
    "power_da_prices_daily_cet.csv, ttf_monthly.csv",
    ["GH", "CB", "P", "TTF"],
    r'''import statsmodels.api as sm
hyd = GH[['hydro_run_of_river', 'hydro_water_reservoir']].sum(axis=1, min_count=2)
hy_a = hyd.groupby(GH.index.year).sum() / 1e6                                   # TWh per year, reported hours
hydro_m = hyd.resample('MS').sum(min_count=600) / 1e6                          # TWh per month (>= 600 reported hours)
hydro_m.index = hydro_m.index.tz_localize(None)
hydro_m = hydro_m.loc[:str(Y - 1)].dropna()
imp_twh = (CB['sum'] * 24 / 1e6).groupby(CB.index.year).sum()                   # net imports, TWh
dfm = pd.concat([hydro_m.rename('hydro'), P['RO'].resample('MS').mean().rename('price'),
                 TTF['ttf_eur_mwh'].rename('ttf')], axis=1).dropna()
ols = sm.OLS(dfm['price'], sm.add_constant(dfm[['hydro', 'ttf']])).fit(cov_type='HAC', cov_kwds={'maxlags': 6})
show('hydro.y2023', 'hydro 2023, TWh', fl(hy_a.loc[2023], 2))
show('hydro.y2025', 'hydro 2025, TWh', fl(hy_a.loc[2025], 2))
show('hydro.chg_pct', 'change 2025 vs 2023, %', fl((hy_a.loc[2025] / hy_a.loc[2023] - 1) * 100, 1))
show('hydro.mean_1525', 'mean 2015-2025, TWh', fl(hy_a.loc[2015:2025].mean(), 2))
show('hydro.vs_mean_pct', '2025 vs the 2015-2025 mean, %', fl((hy_a.loc[2025] / hy_a.loc[2015:2025].mean() - 1) * 100, 1))
show('hydro.netimp2023', 'net imports 2023, TWh', fl(imp_twh.loc[2023], 2))
show('hydro.netimp2025', 'net imports 2025, TWh', fl(imp_twh.loc[2025], 2))
show('hydro.reg.n', 'regression: months', int(ols.nobs))
show('hydro.reg.r2', 'regression: R squared', fl(ols.rsquared, 3))
show('hydro.reg.hydro.b', 'regression: EUR/MWh per extra TWh of hydro', fl(ols.params['hydro'], 2))
show('hydro.reg.hydro.t', 'regression: t statistic (HAC)', fl(ols.tvalues['hydro'], 2))''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2), gridspec_kw={'width_ratios': [1.5, 1]})
hy_avg = hydro_m.loc['2015':'2025'].groupby(hydro_m.loc['2015':'2025'].index.month).mean()
axs[0].plot(range(1, 13), hydro_m.loc['2023'].values, color=PAL['RO'], marker='o', ms=4, label='2023 (wet)')
axs[0].plot(range(1, 13), hydro_m.loc['2025'].values, color=PAL['DE_LU'], marker='s', ms=4, ls='--', label='2025 (dry)')
axs[0].plot(range(1, 13), hy_avg.values, color='#222222', lw=1.0, ls=':', label='Hydro mean 2015-2025')
month_ticks(axs[0])
axs[0].set_ylabel('TWh per month')
axs[0].set_title('Hydro generation, RO')
axs[1].scatter(dfm['hydro'], dfm['price'], s=14, color=PAL['RO'], label='one month')
axs[1].set_xlabel('Hydro, TWh per month')
axs[1].set_ylabel('EUR/MWh')
axs[1].set_title('Hydro vs RO price, monthly')
legend_bottom(fig, ncol=4)''', bottom=0.13)

add("iran_brent", "Case study: Brent around the June 2025 Israel-Iran war",
    "Brent front-month daily close from 2 June to 4 July 2025, with the Israeli strikes on Iran (13 June), the peak close "
    "and the ceasefire (24 June); prints the one-day jump, its size in 2024 standard deviations and the reversal",
    "event study, geopolitical risk, Brent, crude oil, Iran, Israel, price shock, case study",
    "Brent front-month futures daily close (Yahoo Finance BZ=F; data/clean/fuels_daily.csv)",
    ["F"],
    BRENT + "\n\n" + r'''p12, p13, p24 = (b.loc[x] for x in ['2025-06-12', '2025-06-13', '2025-06-24'])
win = b.loc['2025-06-13':'2025-06-23']
sd24 = rb.loc['2024'].std()                                     # daily return volatility in 2024, %
show('iran.p12', 'close 12 Jun 2025, USD/bbl', fl(p12, 2))
show('iran.p13', 'close 13 Jun 2025, USD/bbl', fl(p13, 2))
show('iran.chg13', 'change on 13 Jun, %', fl((p13 / p12 - 1) * 100, 1))
show('iran.z13', 'log change on 13 Jun / 2024 daily sd', fl(np.log(p13 / p12) * 100 / sd24, 1))
show('iran.peak', 'peak close 13-23 Jun, USD/bbl', fl(win.max(), 2))
show('iran.peak_date', 'date of the peak', d(win.idxmax()))
show('iran.p24', 'close 24 Jun 2025, USD/bbl', fl(p24, 2))
show('iran.chg24_peak', 'change peak -> 24 Jun, %', fl((p24 / win.max() - 1) * 100, 1))
show('iran.chg24_12', 'change 12 Jun -> 24 Jun, %', fl((p24 / p12 - 1) * 100, 1))''',
    r'''bw = b.loc['2025-06-02':'2025-07-04']
fig, ax = plt.subplots(figsize=(6.4, 2.0))
ax.plot(bw.index, bw, color=PAL['RO'], marker='o', ms=4, label='Brent close, USD/bbl')
# labels sit in free corners of the axes (axes fraction), with a thin leader line to their point
for dt, txt, xy_txt, ha in [('2025-06-13', '13 Jun: Israel strikes Iran', (0.02, 0.90), 'left'),
                            (str(win.idxmax().date()), 'peak close', (0.68, 0.93), 'left'),
                            ('2025-06-24', '24 Jun: ceasefire in effect', (0.99, 0.10), 'right')]:
    ax.annotate(txt, (pd.Timestamp(dt), b.loc[dt]), xytext=xy_txt, textcoords='axes fraction', ha=ha, va='center',
                fontsize=9.5, arrowprops=dict(arrowstyle='-', lw=0.6, color='#555555'))
ax.set_ylim(bw.min() - 5.5, bw.max() + 3)
ax.set_ylabel('USD/bbl')
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%-d %b'))
legend_bottom(fig, ncol=1)''', bottom=0.13)

add("separation_2024", "Case study: market separation in summer 2024",
    "Daily base day-ahead prices in Romania, Bulgaria, Hungary and Germany-Luxembourg from June to September 2024, and "
    "hourly prices on 16 July 2024: in July 2024 Romania paid about twice the German price",
    "market coupling, price separation, congestion, cross-border, electricity prices, Romania, Germany, case study",
    "Daily and hourly day-ahead prices (energy-charts.info, from the exchanges via ENTSO-E; "
    "data/clean/power_da_prices_daily_cet.csv, power_da_prices_hourly_utc.csv)",
    ["P", "H"],
    r'''jul = P.loc['2024-07', ZONES].mean()
g16 = P.loc['2024-07-16', ZONES]
hd16 = H.loc['2024-07-16', ZONES]                               # hourly, 16 July 2024
for z in ZONES:
    show(f'sep.jul.{z}', f'July 2024 mean, {z}, EUR/MWh', fl(jul[z], 2))
show('sep.d16_gap', '16 Jul daily base, RO - DE-LU, EUR/MWh', fl(g16['RO'] - g16['DE_LU'], 2))
show('sep.d16_ro_max', '16 Jul, highest RO hour, EUR/MWh', fl(hd16['RO'].max(), 2))
show('sep.d16_ro_max_h', '16 Jul, hour of the RO maximum (CEST)', int(hd16['RO'].idxmax().hour))
show('sep.d16_de_min', '16 Jul, lowest DE-LU hour, EUR/MWh', fl(hd16['DE_LU'].min(), 2))
show('sep.d16_de_min_h', '16 Jul, hour of the DE-LU minimum (CEST)', int(hd16['DE_LU'].idxmin().hour))''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.2), gridspec_kw={'width_ratios': [1.6, 1]})
ss = P.loc['2024-06-01':'2024-09-30', ZONES]
for z in ['DE_LU', 'HU', 'BG', 'RO']:
    axs[0].plot(ss.index, ss[z], color=PAL[z], ls=ZONE_LS[z], lw=1.2, label=ZONE_SHORT[z])
    axs[1].plot(hd16.index.hour, hd16[z], color=PAL[z], ls=ZONE_LS[z], lw=1.4)
axs[0].set_ylabel('EUR/MWh')
axs[0].xaxis.set_major_locator(mdates.MonthLocator())
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
axs[0].set_title('Summer 2024, daily base')
axs[1].axhline(0, color='#222222', lw=0.6)
axs[1].set_xlabel('Hour (CEST)')
axs[1].set_ylabel('EUR/MWh')
axs[1].set_xticks(range(0, 24, 4))
axs[1].set_title('16 July 2024, hourly')
legend_bottom(fig, ncol=4)''', bottom=0.13)

add("cy_prices", "Case study: day-ahead prices and Brent in the current year",
    "Daily base day-ahead prices in Romania, Bulgaria, Hungary and Germany-Luxembourg and the Brent front-month close from "
    "1 January of the current year to the cut-off; prints the year-to-date mean against the same months of the previous "
    "year and the Brent moves of March",
    "electricity prices, Brent, crude oil, current year, year-to-date, Romania, case study",
    "Daily day-ahead prices (energy-charts.info, from the exchanges via ENTSO-E) and Brent front-month close (Yahoo Finance "
    "BZ=F); data/clean/power_da_prices_daily_cet.csv, fuels_daily.csv",
    ["P", "F"],
    r'''pY = P.loc[str(Y), ZONES]
pPrev = P.loc[f'{Y - 1}-01-01':f'{Y - 1}-{END:%m-%d}', ZONES]   # same months of the previous year
b = F['brent_usd_bbl'].dropna()
bY = b.loc[str(Y)]
bm = bY.resample('MS').mean()
mar = b.loc[f'{Y}-03']
show('cutoff.end', 'cut-off', d(END))
show('cy.mean.RO', f'RO mean Jan-{MON_EN[END.month - 1]} {Y}, EUR/MWh', fl(pY['RO'].mean(), 2))
show('cy.mean_prev.RO', f'RO mean Jan-{MON_EN[END.month - 1]} {Y - 1}, EUR/MWh', fl(pPrev['RO'].mean(), 2))
show('cy.chg.RO', 'change, %', fl((pY['RO'].mean() / pPrev['RO'].mean() - 1) * 100, 1))
show('cy.lm.RO', f'RO mean {MON_EN[END.month - 1]} {Y}, EUR/MWh', fl(pY['RO'].resample('MS').mean().iloc[-1], 1))
show('cy.lm_prev.RO', f'RO mean {MON_EN[END.month - 1]} {Y - 1}, EUR/MWh', fl(P.loc[f'{Y - 1}-{END:%m}', 'RO'].mean(), 1))
show('cy.brent.jan_avg', 'Brent January mean, USD/bbl', fl(bm.iloc[0], 2))
show('cy.brent.last_avg', 'Brent last-month mean, USD/bbl', fl(bm.iloc[-1], 2))
show('cy.brent.mar_pct', 'Brent in March (same contract), %', fl((mar.iloc[-1] / mar.iloc[0] - 1) * 100, 1))
show('cy.brent.roll_apr', 'Brent, first April day vs end of March (contract roll), %', fl((b.loc[f'{Y}-04'].iloc[0] / mar.iloc[-1] - 1) * 100, 1))''',
    r'''fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.3), sharex=True, gridspec_kw={'height_ratios': [1.4, 1]})
for z in ['DE_LU', 'HU', 'BG', 'RO']:
    axs[0].plot(pY.index, pY[z], color=PAL[z], ls=ZONE_LS[z], lw=1.0, label=z.replace('_', '-'))
axs[0].set_ylabel('EUR/MWh', fontsize=9.5)
axs[1].plot(bY.index, bY, color=PAL['c7'], lw=1.3, label='Brent')
axs[1].set_ylabel('USD/bbl', fontsize=9.5)
axs[1].xaxis.set_major_locator(mdates.MonthLocator())
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
fig.align_ylabels(axs)
legend_bottom(fig, ncol=5)''', bottom=0.12)

add("cy_generation", "Case study: Romanian hydro, nuclear and solar output, current vs previous year",
    "Monthly mean Romanian hydro, nuclear and solar generation (GW, reported hours) in the previous year and in the "
    "current year to the cut-off: the Cernavoda nuclear plant offline twice and hydro below the previous year; months "
    "without reported data stay empty",
    "generation, nuclear outage, hydro, solar, Romania, current year, missing data, case study",
    "Romanian hourly and daily generation by source (energy-charts.info, ENTSO-E; data/clean/generation_ro_mw_hourly_utc.csv, "
    "generation_ro_mw_daily_cet.csv)",
    ["GH", "G"],
    LFL + "\n\n" + r'''hm_ = (G['hydro_run_of_river'] + G['hydro_water_reservoir']).resample('MS').mean()    # daily data, monthly mean MW
cmp_ = {m: (hm_.loc[f'{Y}-{m:02d}'].iloc[0], hm_.loc[f'{Y - 1}-{m:02d}'].iloc[0]) for m in range(1, END.month + 1)}
gm = G.loc[f'{Y}-05', 'nuclear']
show('mix.lfl.Nuclear.chg', f'nuclear, Jan-{MON_EN[END.month - 1]} {Y} vs {Y - 1} (hours reported in both), %',
     lfl_block(['nuclear'], Y - 1, Y)['chg'])
show('mix.lfl.Solar.chg', f'solar, Jan-{MON_EN[END.month - 1]} {Y} vs {Y - 1}, %', lfl_block(['solar'], Y - 1, Y)['chg'])
show('nuclear.may_zero_days', f'days in May {Y} with zero nuclear output', int((gm < 1).sum()))
show('nuclear.hydro_aug_oct_chg', f'hydro Aug-{MON_EN[END.month - 1]} {Y} vs {Y - 1}, %',
     fl((sum(cmp_[m][0] for m in range(8, END.month + 1)) / sum(cmp_[m][1] for m in range(8, END.month + 1)) - 1) * 100, 1))''',
    r'''fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.1))


def month_mean(s):
    """Monthly mean in GW; a month with fewer than half of its hours reported stays empty."""
    g = s.groupby(s.index.month)
    return (g.mean() / 1000).where(g.count() >= 0.5 * g.size())


for ax, (ttl, cols) in zip(axs, [('Hydro', ['hydro_run_of_river', 'hydro_water_reservoir']), ('Nuclear', ['nuclear']),
                                 ('Solar', ['solar'])]):
    a = GH.loc[str(Y - 1), cols].sum(axis=1, min_count=len(cols))
    c = GH.loc[str(Y), cols].sum(axis=1, min_count=len(cols))
    ma, mc = month_mean(a), month_mean(c)
    for m in mc.index[mc.isna()]:
        if m <= END.month:
            ax.axvspan(m - 0.5, m + 0.5, color='#d9d9d9', alpha=0.7, lw=0)
            ax.text(m, 1.02, 'no data', transform=ax.get_xaxis_transform(), ha='center', va='bottom', fontsize=9, color='#555555')
    ax.plot(ma.index, ma.values, color='#222222', ls='--', marker='o', ms=3, lw=1.2, label=str(Y - 1))
    ax.plot(mc.index, mc.values, color=PAL['RO'], marker='s', ms=3.5, lw=1.6, label=f'{Y} (to {MON_EN[END.month - 1]})')
    ax.set_title(ttl, fontsize=11, pad=14)
    ax.set_xlim(0.5, 12.5)
    month_ticks(ax)
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_locator(plt.MaxNLocator(4))
axs[0].set_ylabel('Mean power, GW')
legend_bottom(fig, ncol=2)''', bottom=0.13)

add("cy_extremes", "Case study: extremes of the current year, Romanian price and Brent",
    "Romanian daily base day-ahead price and Brent front-month close from 1 January of the current year to the cut-off, "
    "with the highest and lowest days marked; prints the daily and 15-minute extremes with their dates",
    "extremes, price spikes, negative prices, electricity, Brent, Romania, current year, case study",
    "Daily and native-resolution day-ahead prices (energy-charts.info, OPCOM via ENTSO-E) and Brent front-month close "
    "(Yahoo Finance BZ=F); data/clean/power_da_prices_daily_cet.csv, power_da_prices_native_utc.csv, fuels_daily.csv",
    ["P", "X", "F"],
    r'''ro_ = P.loc[str(Y), 'RO'].dropna()
xY = X.loc[str(Y)]
b_ = F['brent_usd_bbl'].dropna().loc[str(Y)]
show('cy.ro_max_day', 'highest RO daily base, EUR/MWh', fl(ro_.max(), 2))
show('cy.ro_max_day_date', 'date', d(ro_.idxmax()))
show('cy.ro_min_day', 'lowest RO daily base, EUR/MWh', fl(ro_.min(), 2))
show('cy.ro_min_day_date', 'date', d(ro_.idxmin()))
show('cy.ro_max_mtu', 'highest RO 15-min price, EUR/MWh', fl(xY['RO'].max(), 2))
show('cy.ro_max_mtu_ts', 'time (CET/CEST)', xY['RO'].idxmax().strftime('%Y-%m-%d %H:%M'))
show('cy.ro_min_mtu', 'lowest RO 15-min price, EUR/MWh', fl(xY['RO'].min(), 2))
show('cy.ro_min_mtu_ts', 'time (CET/CEST)', xY['RO'].idxmin().strftime('%Y-%m-%d %H:%M'))
show('cy.brent.max', 'highest Brent close, USD/bbl', fl(b_.max(), 2))
show('cy.brent.max_date', 'date', d(b_.idxmax()))''',
    r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.3))
axs[0].plot(ro_.index, ro_.values, color=PAL['RO'], lw=0.9)
for dt, col in [(ro_.idxmax(), '#b2182b'), (ro_.idxmin(), '#2166ac')]:
    axs[0].plot([dt], [ro_[dt]], 'o', color=col, ms=5)
    axs[0].annotate(f'{ro_[dt]:.0f}', (dt, ro_[dt]), textcoords='offset points', xytext=(6, -3 if col == '#2166ac' else -10),
                    fontsize=8.5, color=col)
axs[0].set_title('RO daily base price (EUR/MWh)', fontsize=10)
axs[1].plot(b_.index, b_.values, color='#222222', lw=0.9)
axs[1].plot([b_.idxmax()], [b_.max()], 'o', color='#b2182b', ms=5)
axs[1].annotate(f'{b_.max():.1f}', (b_.idxmax(), b_.max()), textcoords='offset points', xytext=(-38, -4), fontsize=8.5, color='#b2182b')
axs[1].set_title('Brent close (USD/bbl)', fontsize=10)
for ax in axs:
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', labelsize=8)''', bottom=0.14)

add("bg_battery", "Case study: Romania-Bulgaria evening price gap and Bulgarian batteries",
    "Monthly Romania minus Bulgaria day-ahead price spread in the evening hours 19:00-22:00 local time (EET) since 2023, "
    "and the monthly mean Bulgarian battery discharge and charging (MW) since the battery series starts; an association, "
    "not proof",
    "battery storage, price spread, evening peak, Romania, Bulgaria, day-ahead market, case study",
    "Day-ahead prices at native resolution and Bulgarian hourly generation incl. batteries (energy-charts.info, ENTSO-E); "
    "data/clean/power_da_prices_native_utc.csv, generation_bg_mw_hourly_utc.csv",
    ["X", "BGH"],
    r'''XL = X.copy()
XL.index = XL.index.tz_convert('Europe/Bucharest')              # local time, same in Romania and Bulgaria
wloc = XL['mtu_minutes'] / 60                                   # duration weights (60- and 15-min MTUs)


def wmean(z, mask):
    v, ww = XL.loc[mask, z], wloc[mask]
    ok = v.notna()
    return float((v[ok] * ww[ok]).sum() / ww[ok].sum())


ev, mid = {}, {}
for y in [2023, 2024, 2025, Y]:
    base = (XL.index.year == y) & (XL.index.month >= 4) & (XL.index.month <= 9)  # April-September
    ev[y] = {z: fl(wmean(z, base & (XL.index.hour >= 19) & (XL.index.hour <= 21)), 1) for z in ['RO', 'BG']}
    mid[y] = {z: fl(wmean(z, base & (XL.index.hour >= 11) & (XL.index.hour <= 14)), 1) for z in ['RO', 'BG']}
evm = XL[(XL.index.hour >= 19) & (XL.index.hour <= 21)].loc['2023-01-01':]
evw = evm['mtu_minutes'] / 60
mk = evm.index.tz_localize(None).to_period('M')
ev_sp = ((evm['RO'] - evm['BG']) * evw).groupby(mk).sum() / evw.groupby(mk).sum()   # monthly RO - BG evening spread
bat = BGH[['battery', 'battery_consumption']].copy()
bat.index = bat.index.tz_convert('Europe/Bucharest')
bat_first = bat.dropna(how='all').index.min()
bb = bat.loc[bat_first:]
batm = bb.groupby(bb.index.tz_localize(None).to_period('M')).mean()
for y in [2025, Y]:
    for z in ['RO', 'BG']:
        show(f'bat.evening.{y}.{z}', f'{z}, Apr-Sep {y}, 19:00-22:00 EET, EUR/MWh', ev[y][z])
for z in ['RO', 'BG']:
    show(f'bat.midday.{Y}.{z}', f'{z}, Apr-Sep {Y}, 11:00-15:00 EET, EUR/MWh', mid[Y][z])
show('bat.bg_first', 'first reported BG battery hour', bat_first.strftime('%Y-%m-%d'))
show('bat.gap_open', f'first month of {Y} with an evening spread > 15 EUR/MWh',
     next((k.strftime('%Y-%m') for k, v in ev_sp.items() if k.year == Y and v > 15), 'none'))''',
    r'''fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.0), sharex=True, gridspec_kw={'height_ratios': [1.4, 1]})
xi = ev_sp.index.to_timestamp()
axs[0].bar(xi, ev_sp.values, width=20, color=[PAL['RO'] if v >= 0 else PAL['c8'] for v in ev_sp.values],
           label='RO − BG, 19-22 h EET')
axs[0].axhline(0, color='#222222', lw=0.6)
axs[0].set_ylabel('EUR/MWh')
bi = batm.index.to_timestamp()
axs[1].bar(bi - pd.Timedelta(days=5), batm['battery'].values, width=9, color=PAL['HU'], label='BG battery discharge')
axs[1].bar(bi + pd.Timedelta(days=5), -batm['battery_consumption'].values, width=9, color=PAL['BG'], label='BG battery charging')
axs[1].set_ylabel('MW')
axs[1].set_xlim(pd.Timestamp('2022-12-15'), END + pd.Timedelta(days=20))
axs[1].xaxis.set_major_locator(mdates.YearLocator())
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
legend_bottom(fig, ncol=3)''', bottom=0.14)


# ---------------------------------------------------------------------------------------------------------------
def build(spec):
    c = spec["chart"]
    q = Quantlet(k=1, chart=c, title=spec["title"],
                 description=f"{spec['what']}. Data: {PERIOD[c]}. Source: {SOURCE[c]}.",
                 keywords=spec["keywords"], datafile=spec["datafile"])
    q.md(f"{spec['what']}.\n\n**Data:** {PERIOD[c]}. **Source:** {SOURCE[c]}.\n\n"
         "The numbers printed below are those on the slide; the tag `[key]` is their name in `lectures/L1/L1_numbers.json`.")
    q.code(SETUP)
    if spec["loads"]:
        q.md("## Data\nReal series from the course repository (see `data/SOURCES.md`), cut at the last complete month; "
             "missing values stay missing.")
        q.code(CUTOFF + "\n\n" + "\n".join(LOAD[k] for k in spec["loads"]))
    q.md("## Computation")
    q.code(spec["compute"])
    q.md("## Chart")
    q.code(spec["plot"])
    q.write(execute=True)
    return q


LINE = re.compile(r"^(.*) = (.*?)   \[([\w.\-]+)\]$")


def check(q):
    """Compare every number printed by the executed notebook with L1_numbers.json."""
    nb = nbformat.read(os.path.join(q.folder, q.name + ".ipynb"), as_version=4)
    out = "".join(o.get("text", "") for cell in nb.cells if cell.cell_type == "code" for o in cell.get("outputs", [])
                  if o.get("output_type") == "stream")
    bad, n = [], 0
    for line in out.splitlines():
        m = LINE.match(line)
        if not m:
            continue
        val, key = m.group(2), m.group(3)
        ref = N
        for part in key.split("."):
            ref = ref.get(part) if isinstance(ref, dict) else None
        n += 1
        if ref is None:
            bad.append(f"{key}: not in L1_numbers.json (notebook {val})")
            continue
        try:
            ok = abs(float(val) - float(ref)) < 1e-9
        except (TypeError, ValueError):
            ok = str(val) == str(ref)
        if not ok:
            bad.append(f"{key}: notebook {val} vs L1_numbers.json {ref}")
    return n, bad


if __name__ == "__main__":
    shown = set(N["charts"]) - {"spikes_ro_2024"}           # spikes_ro_2024 is computed but not shown in the deck
    names = [s["chart"] for s in Q]
    assert set(names) == shown, (set(names) ^ shown)
    only = set(sys.argv[1:])
    problems = []
    for spec in Q:
        if only and spec["chart"] not in only:
            continue
        q = build(spec)
        n, bad = check(q)
        print(f"   {n} numbers checked against L1_numbers.json" + ("" if not bad else ": MISMATCH"))
        problems += [f"{q.name}: {b}" for b in bad]
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("all Quantlets written; every printed number equals L1_numbers.json")
