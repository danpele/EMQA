"""
make_quantlets_L6.py -- one Quantlet per chart of Lecture 6 (EMQA)
==================================================================
    Quantlets/L6/EMQA_L6_<chart>/Metainfo.txt
    Quantlets/L6/EMQA_L6_<chart>/EMQA_L6_<chart>.ipynb     (self-contained, executed)
    Quantlets/L6/EMQA_L6_<chart>/<chart>.png

Every notebook copies only the code of analysis_L6.py that its chart needs (no import of the lecture modules), reads only
the data files it needs from DATA (local data/clean or the public repository), prints the numbers shown on the slide and
draws the English chart in the course style. After execution the printed numbers are compared with L6_numbers.json.
The battery optimisation is light (about 1 ms per daily linear programme), so no Quantlet needs saved results.

Run from the repository root (after analysis_L6.py):
    python3 lectures/L6/make_quantlets_L6.py              # all charts
    python3 lectures/L6/make_quantlets_L6.py spreads      # some charts
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_quantlet import Quantlet  # noqa: E402

N = json.load(open(os.path.join(HERE, "L6_numbers.json")))
END = N["cutoff"]["end"]
LTM_START = N["cutoff"]["ltm_start"]
MON_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def period(chart):
    return N["charts"][chart]["period_en"].replace("\\%", "%")


# =============================================================================
# Code blocks shared by several notebooks (each notebook receives only those it needs)
# =============================================================================
STYLE = r'''import json
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

# course chart style: transparent background, no grid, legend at the bottom outside the axes, fixed colour per zone
PAL = {'RO': '#2a78d6', 'DE_LU': '#eb6834', 'HU': '#1baf7a', 'BG': '#eda100',
       'c5': '#e87ba4', 'c6': '#008300', 'c7': '#6250d6', 'c8': '#e34948'}
ZONE_LS = {'RO': '-', 'BG': '--', 'HU': '-.', 'DE_LU': ':'}
ZN = {'RO': 'Romania', 'BG': 'Bulgaria', 'HU': 'Hungary', 'DE_LU': 'Germany-Lux.'}
INK = '#222222'
plt.rcParams.update({
    'figure.facecolor': 'none', 'axes.facecolor': 'none', 'savefig.transparent': True,
    'axes.grid': False, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.edgecolor': INK, 'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK,
    'text.color': INK, 'font.size': 11, 'axes.titlesize': 11.5, 'axes.labelsize': 11,
    'legend.fontsize': 10.5, 'legend.frameon': False, 'lines.linewidth': 1.4, 'font.family': 'DejaVu Sans'})


def legend_bottom(fig, ncol=4):
    """One legend for the whole figure, centred under the axes, outside the plotting area."""
    handles, labels = [], []
    for ax in fig.axes:
        for h, l in zip(*ax.get_legend_handles_labels()):
            if l not in labels:
                handles.append(h)
                labels.append(l)
    fig.legend(handles, labels, loc='lower center', ncol=ncol, bbox_to_anchor=(0.5, 0.0), frameon=False,
               handlelength=2.0, columnspacing=1.2)


def fl(x, k=4):
    """Rounding used for the numbers of the slides."""
    return None if x is None or np.isnan(float(x)) else round(float(x), k)


def show_numbers(d):
    for k, v in d.items():
        print(f'{k:<34} {v}')'''

PERIOD = r'''TZ = 'Europe/Brussels'                     # delivery days in CET/CEST
END = pd.Timestamp('@END@')               # cut-off of Lecture 6 = last complete month of the data
END_X = (END + pd.Timedelta(days=1)).tz_localize(TZ)
Y = END.year
YEARS = list(range(2019, Y + 1))
MON_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
YTD = f'* {Y} = Jan-{MON_EN[END.month - 1]}'
LTM0 = pd.Timestamp('@LTM@').tz_localize(TZ)    # first day of the last 12 months
MTU15 = pd.Timestamp('2025-10-01').tz_localize(TZ)   # 15-min market time unit from 1 Oct 2025'''.replace("@END@", END).replace("@LTM@", LTM_START)

PRICES = r'''# day-ahead prices, EUR/MWh: hourly to 30 Sep 2025, 15-min from 1 Oct 2025 (SDAC); index in CET/CEST
PX = pd.read_csv(DATA + 'power_da_prices_native_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')
PX.index = PX.index.tz_convert(TZ)
PX['dur'] = PX['mtu_minutes'] / 60.0          # interval length in hours
PX = PX[PX.index < END_X]
LOC_YEAR = PX.index.year
print('prices:', PX.index.min(), 'to', PX.index.max(), '|', (PX['mtu_minutes'] == 15).sum(), '15-min intervals')'''

HFLOOR = r'''def hfloor(idx):
    """Start of the clock hour, computed in UTC (no ambiguity on the autumn DST day)."""
    return idx.tz_convert('UTC').floor('1h').tz_convert(TZ)'''

GEN = r'''def load_gen(c):
    """Generation and load of country c (ro, bg, hu), MW, native resolution, CET/CEST index."""
    g = pd.read_csv(DATA + f'generation_{c}_mw_native_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')
    g.index = g.index.tz_convert(TZ)
    return g


def on_price_grid(g):
    """Generation columns on the price grid: hourly mean for hourly prices; 15-min value for 15-min prices
    (the hourly value is repeated when the source is hourly, as for Bulgaria)."""
    gg = g.drop(columns=['mtu_minutes']).copy()
    out = gg.resample('1h').mean().reindex(hfloor(PX.index)).set_axis(PX.index)
    q15 = PX['mtu_minutes'] == 15
    if (g['mtu_minutes'] == 15).loc[g.index >= MTU15].all():
        out.loc[q15] = gg.resample('15min').mean().reindex(PX.index[q15]).values
    return out


GN = {c.upper(): load_gen(c) for c in @COUNTRIES@}
GR = {z: on_price_grid(GN[z]) for z in GN}
print({z: (str(g.index.min())[:10], str(g.index.max())[:10]) for z, g in GN.items()})'''


def gen(*countries):
    return GEN.replace("@COUNTRIES@", repr(tuple(countries)))


CAPTURE = r'''def capture(zone, tech, mask):
    """Capture price = generation-weighted mean price; baseload = duration-weighted mean price (EUR/MWh)."""
    p, w = PX[zone], GR[zone][tech] * PX['dur']
    m = mask & p.notna() & w.notna()
    base_m = mask & p.notna()
    cp = float((p[m] * w[m]).sum() / w[m].sum())
    base = float((p[base_m] * PX['dur'][base_m]).sum() / PX['dur'][base_m].sum())
    return cp, base, float(w[m].sum())


def capture_years(zones, techs):
    """Capture rate by calendar year (years with at least 90% of the generation intervals reported)."""
    out = {}
    for z in zones:
        for tech in techs:
            for y in YEARS:
                m = pd.Series(LOC_YEAR == y, index=PX.index)
                if GR[z][tech][m].notna().sum() < 0.9 * m.sum():
                    continue
                cp, base, e = capture(z, tech, m)
                out[(z, tech, y)] = {'cp': cp, 'base': base, 'crp': fl(cp / base * 100, 1)}
    return out'''

DAYS = r'''def day_groups(zone, start=None, end=None, hourly=False):
    """Prices per CET delivery day (complete days only: 23/24/25 hours or 92/96/100 quarter-hours)."""
    s = PX[[zone, 'dur']]
    if start is not None:
        s = s[s.index >= start]
    if end is not None:
        s = s[s.index < end]
    if hourly:
        s = s.groupby(hfloor(s.index)).agg({zone: 'mean', 'dur': 'sum'})
    out = {}
    for dd, g in s.groupby(s.index.tz_localize(None).normalize()):
        if g[zone].notna().all() and abs(g['dur'].sum() - round(g['dur'].sum())) < 1e-9 and round(g['dur'].sum()) in (23, 24, 25):
            out[dd] = (g[zone].values.astype(float), g['dur'].values.astype(float))
    return out'''

BATTERY = r'''from scipy import sparse
from scipy.optimize import linprog

ETA, CYCLES, DURS = 0.85, 1.0, (1, 2, 4)   # round-trip efficiency, max cycles per day, hours of storage (NREL 2023 update)


def battery_day(p, dur, E, P=1.0, eta=ETA, cycles=CYCLES):
    """Optimal charge c_t and discharge d_t (MW) of a P-MW / E-MWh battery for one day of prices p_t and interval lengths dur_t (h):
    max sum_t p_t (d_t - c_t) dur_t  s.t.  s_t = s_{t-1} + sqrt(eta) c_t dur_t - d_t dur_t / sqrt(eta),
    0 <= s_t <= E, s_0 = s_T = 0, 0 <= c_t, d_t <= P, sum_t d_t dur_t / sqrt(eta) <= cycles * E.  Linear programme (HiGHS)."""
    n = len(p)
    r = np.sqrt(eta)
    cost = np.concatenate([p * dur, -p * dur, np.zeros(n)])
    Lw = sparse.diags([np.ones(n), -np.ones(n - 1)], [0, -1], format='csr')          # s_t - s_{t-1}
    A_eq = sparse.hstack([-r * sparse.diags(dur), sparse.diags(dur / r), Lw], format='csr')
    A_eq = sparse.vstack([A_eq, sparse.hstack([sparse.csr_matrix((1, 2 * n)), sparse.csr_matrix(([1.0], ([0], [n - 1])), shape=(1, n))])])
    b_eq = np.zeros(n + 1)
    A_ub = sparse.hstack([sparse.csr_matrix((1, n)), sparse.csr_matrix(dur / r), sparse.csr_matrix((1, n))], format='csr')
    bounds = [(0, P)] * (2 * n) + [(0, E)] * n
    res = linprog(cost, A_ub=A_ub, b_ub=[cycles * E], A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    x = res.x
    return x[:n], x[n:2 * n]


def revenue(p, dur, c, d):
    return float(np.sum(p * (d - c) * dur))


def run_battery(dg, E, forecast=None):
    """Daily revenue (EUR per MW) with perfect foresight, or with the schedule optimised on `forecast` (dict day -> prices)."""
    out = {}
    for day, (p, w) in dg.items():
        if forecast is None:
            c, d = battery_day(p, w, E)
        else:
            f = forecast.get(day)
            if f is None or len(f) != len(p):
                continue
            c, d = battery_day(f, w, E)
        out[day] = revenue(p, w, c, d)
    return pd.Series(out)'''


def finish(chart, bottom):
    return (f"fig.tight_layout(rect=(0, {bottom}, 1, 1))\n"
            f"plt.savefig('{chart}.png', dpi=150, bbox_inches='tight', transparent=True)\n"
            "plt.show()")


SRC_EC = "energy-charts.info (Fraunhofer ISE), ENTSO-E Transparency Platform"
PX_WORDS = ("power_da_prices_native_utc.csv: day-ahead prices (EUR/MWh) of Romania (OPCOM), Bulgaria (IBEX), Hungary (HUPX) "
            "and Germany-Luxembourg (EPEX SPOT), hourly to 30 Sep 2025 and 15-min from 1 Oct 2025, from energy-charts.info "
            "(Fraunhofer ISE) / ENTSO-E")
GEN_WORDS = "generation_{c}_mw_native_utc.csv: {name} solar, onshore wind{bat} and load (MW, ENTSO-E via energy-charts.info{res})"


def gw(c, name, bat="", res=""):
    return GEN_WORDS.format(c=c, name=name, bat=bat, res=res)


GW_RO = gw("ro", "Romanian", res=", Transelectrica data; hourly, 15-min from Oct 2025")
GW_BG = gw("bg", "Bulgarian", res=", hourly")
GW_HU = gw("hu", "Hungarian", res=", 15-min")

INTRO_SETUP = "## Setup: chart style and data period"
Q = []


def add(chart, description, keywords, datafile, cells, title=None):
    Q.append(dict(chart=chart, description=description, keywords=keywords, datafile=datafile, cells=cells, title=title))


C = N["cutoff"]
Y, YP = C["year"], C["year"] - 1

# =============================================================================
# 1 solar_growth
# =============================================================================
add("solar_growth",
    f"Installed solar capacity at year end in Romania, Bulgaria and Hungary (2019-{N['cap']['last_year']}, ENTSO-E) and yearly "
    f"Romanian solar output in TWh (2019 to {END}, {Y} = Jan-{MON_EN[C['month'] - 1]}). Prints the growth factor of Romanian "
    "capacity, the like-for-like Jan-cut-off output of the last two years and the solar share of load.",
    "solar, photovoltaic, installed capacity, renewables, generation, Romania, Bulgaria, Hungary, energy, TWh, bar chart",
    "installed_capacity_yearly.csv: installed capacity by country, technology and year (ENTSO-E via energy-charts.info); "
    + PX_WORDS + " (used for the interval lengths); " + GW_RO,
    [("md", "Installed capacity is read at year end; energy = sum over intervals of mean MW x interval length (h)."),
     ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + gen("ro")),
     ("code", r'''CAP = pd.read_csv(DATA + 'installed_capacity_yearly.csv')
cap = CAP[CAP['type'].str.startswith('Solar')]
solar_gw = {z: {int(r.year): fl(r.gw, 2) for r in cap[cap.country == z].itertuples()} for z in ('RO', 'BG', 'HU')}
last_year = int(CAP['year'].max())

ro, dur = GR['RO'], PX['dur']
twh = {y: {c: fl((ro[c][LOC_YEAR == y] * dur[LOC_YEAR == y]).sum() / 1e6, 2) for c in ('solar', 'load')} for y in YEARS}
lfl = {}                                              # like-for-like: January to the cut-off month
for y in (Y - 1, Y):
    m = (LOC_YEAR == y) & (PX.index.month <= END.month)
    lfl[y] = fl((ro['solar'][m] * dur[m]).sum() / 1e6, 2)

show_numbers({'cap.last_year': last_year,
              'cap.solar_ro_x': fl(solar_gw['RO'][last_year] / solar_gw['RO'][2019], 1),
              f'cap.solar.BG.{last_year}': solar_gw['BG'][last_year],
              f'cap.solar.HU.{last_year}': solar_gw['HU'][last_year],
              f'twh_lfl.{Y - 1}.solar': lfl[Y - 1], f'twh_lfl.{Y}.solar': lfl[Y],
              'twh.solar_share_load_2019': fl(twh[2019]['solar'] / twh[2019]['load'] * 100, 1),
              'twh.solar_share_load_ytd': fl(twh[Y]['solar'] / twh[Y]['load'] * 100, 1)})'''),
     ("code", r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.85))
cy = list(range(2019, last_year + 1))
wdt = 0.27
for i, z in enumerate(('RO', 'BG', 'HU')):
    axs[0].bar(np.array(cy) + (i - 1) * wdt, [solar_gw[z][y] for y in cy], width=wdt, color=PAL[z], label=ZN[z])
axs[0].set_ylabel('installed solar\n(GW)', fontsize=9)
axs[0].set_xticks(cy)
axs[0].set_xticklabels([str(y)[2:] for y in cy])
axs[1].bar(range(len(YEARS)), [twh[y]['solar'] for y in YEARS], color=PAL['RO'], width=0.6)
axs[1].set_xticks(range(len(YEARS)))
axs[1].set_xticklabels([str(y)[2:] + ('*' if y == Y else '') for y in YEARS])
axs[1].set_ylabel('RO solar output\n(TWh)', fontsize=9)
axs[1].text(0.02, 0.92, YTD, transform=axs[1].transAxes, fontsize=8.5)
legend_bottom(fig, ncol=3)
''' + finish("solar_growth", 0.2))])

# =============================================================================
# 2 merit_shift
# =============================================================================
add("merit_shift",
    f"Merit-order effect on the real OPCOM day-ahead (PZU) aggregated supply and demand curves of delivery day {N['merit']['day']}, "
    "quarter-hours 12:00-12:15 and 20:00-20:15 Romanian time: clearing price after adding X MW of supply offered at 0 EUR/MWh "
    "(solar) or X MW of demand bid at any price (battery charging), X = 0-400 MW; cross-border flows, blocks and hourly orders "
    "held at their accepted values.",
    "merit order, supply curve, demand curve, day-ahead market, OPCOM, PZU, clearing price, solar, battery, Romania, quarter-hour",
    "opcom_pzu_curves.csv: OPCOM PZU aggregated supply and demand curves (price, MW) of two quarter-hours of "
    f"{N['merit']['day']}; opcom_pzu_curves_meta.json: official clearing prices, cleared quantities and net exports",
    [("md", "The cumulative supply S(p) and demand D(p) are piecewise linear in the published points. The clearing price after a "
            "shift is the lowest p with S(p) + x_s 1[p >= 0] >= D(p) + x_d (bisection)."),
     ("code", r'''import urllib.request


def read_json(path):
    if path.startswith('http'):
        with urllib.request.urlopen(path) as f:
            return json.load(f)
    return json.load(open(path))


CURVES = pd.read_csv(DATA + 'opcom_pzu_curves.csv')
CMETA = read_json(DATA + 'opcom_pzu_curves_meta.json')
print(CURVES['delivery_date'].iloc[0], CURVES.groupby(['interval', 'side']).size())'''),
     ("code", r'''def curve_fns(lab):
    """Cumulative supply S(p) (MW offered at prices <= p) and demand D(p) (MW bid at prices >= p), piecewise linear in
    the published points; ties in price are separated by 1e-7 EUR/MWh so the functions are single-valued."""
    s = CURVES[(CURVES['interval'] == lab) & (CURVES['side'] == 'supply')]
    dm = CURVES[(CURVES['interval'] == lab) & (CURVES['side'] == 'demand')]
    ps = s['price_eur_mwh'].values + np.arange(len(s)) * 1e-7
    pdm = dm['price_eur_mwh'].values[::-1] + np.arange(len(dm)) * 1e-7
    qs, qd = s['quantity_mw'].values, dm['quantity_mw'].values[::-1]
    return (lambda p: np.interp(p, ps, qs)), (lambda p: np.interp(p, pdm, qd))


def clear(S, D, xs=0.0, xd=0.0, p_s=0.0):
    """Clearing price after adding xs MW of supply offered at p_s and xd MW of demand bid at any price: lowest p with
    S(p) + xs*1[p >= p_s] >= D(p) + xd (bisection on the monotone excess supply)."""
    lo, hi = -600.0, 4000.0
    for _ in range(70):
        m_ = 0.5 * (lo + hi)
        if S(m_) + xs * (m_ >= p_s) - D(m_) - xd >= 0:
            hi = m_
        else:
            lo = m_
    return hi


XGRID = np.arange(0, 401, 5)
MERIT, NUM = {}, {}
for iv in CMETA['intervals']:
    k = 'mid' if iv['opcom_interval'] == 45 else 'eve'
    S, D_ = curve_fns(iv['interval_label'])
    P0 = iv['official_clearing_price_eur_mwh']
    sup = np.array([clear(S, D_, xs=x) if x > 0 else P0 for x in XGRID])
    dem = np.array([clear(S, D_, xd=x) if x > 0 else P0 for x in XGRID])
    MERIT[k] = (sup, dem)
    NUM[k] = {'price': P0, 'sup25': fl(sup[XGRID == 25][0], 2), 'net_imp': fl(-iv['net_export_mw'], 0),
              'x_below50': int(XGRID[np.argmax(sup < 50)]) if (sup < 50).any() else None}

show_numbers({'merit.mid.price': NUM['mid']['price'], 'merit.mid.sup.25': NUM['mid']['sup25'],
              'merit.mid.x_below50': NUM['mid']['x_below50'], 'merit.eve.x_below50': NUM['eve']['x_below50'],
              'merit.eve.net_imp': NUM['eve']['net_imp']})'''),
     ("code", r'''fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.9), sharey=True)
for ax, k in zip(axs, ('mid', 'eve')):
    sup, dem = MERIT[k]
    ax.plot(XGRID, sup, color=PAL['RO'], lw=1.6, label='+X MW of supply at 0 EUR/MWh')
    ax.plot(XGRID, dem, color=PAL['DE_LU'], lw=1.6, ls='--', label='+X MW of demand at any price')
    ax.set_title({'mid': '12:00-12:15 Romanian time', 'eve': '20:00-20:15 Romanian time'}[k], fontsize=10)
    ax.set_xlabel('X, MW added')
    ax.set_ylim(-20, 650)
axs[0].set_ylabel('clearing price\n(EUR/MWh)', fontsize=9)
legend_bottom(fig, ncol=2)
''' + finish("merit_shift", 0.27))])

# =============================================================================
# 3 resid_price
# =============================================================================
add("resid_price",
    f"Romanian day-ahead price against residual load (load - wind - solar), hourly, 2023-01-01 to {END}: mean price in bins of "
    "0.5 GW (bins with at least 20 hours) for 2023, the previous year and the current year to the cut-off; prints the OLS slope "
    "of price on residual load with month, hour and weekday fixed effects and HAC (Newey-West, 48 lags) standard errors, and "
    "the share of hours with residual load below 2 GW.",
    "residual load, merit order, day-ahead price, regression, fixed effects, Newey-West, HAC, solar, wind, Romania, OPCOM",
    PX_WORDS + "; " + GW_RO,
    [("md", "Hourly means (15-min prices averaged to the hour); residual load R_t = load_t - wind_t - solar_t (GW). "
            "Regression: P_t = a + b R_t + month, hour and weekday fixed effects + e_t, HAC standard errors (48 lags)."),
     ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + gen("ro")),
     ("code", r'''import statsmodels.api as sm

ro = GR['RO']
H = pd.DataFrame({'P': PX['RO'], 'dur': PX['dur'], 'load': ro['load'], 'wind': ro['wind_onshore'], 'solar': ro['solar']})
H = H[H.index >= pd.Timestamp('2023-01-01').tz_localize(TZ)]
HH = (H[['P', 'load', 'wind', 'solar']].mul(H['dur'], axis=0).groupby(hfloor(H.index)).sum()
      .div(H['dur'].groupby(hfloor(H.index)).sum(), axis=0)).dropna()           # hourly means
HH = HH[HH.index < END_X]
for c in ('load', 'wind', 'solar'):
    HH[c] = HH[c] / 1000.0                                                      # GW
HH['resid'] = HH['load'] - HH['wind'] - HH['solar']
fe = pd.get_dummies(pd.DataFrame({'m': HH.index.strftime('%Y-%m'), 'h': HH.index.hour.astype(str), 'w': HH.index.dayofweek.astype(str)}),
                    drop_first=True).astype(float)
fe.index = HH.index
R2 = sm.OLS(HH['P'], sm.add_constant(pd.concat([HH[['resid']], fe], axis=1))).fit(cov_type='HAC', cov_kwds={'maxlags': 48})

BINS = np.arange(-2.0, 9.01, 0.5)
RBIN, share2 = {}, {}
for y in (2023, Y - 1, Y):
    s_ = HH[HH.index.year == y]
    g_ = s_.groupby(pd.cut(s_['resid'], BINS), observed=True)['P'].agg(['mean', 'count'])
    g_ = g_[g_['count'] >= 20]
    RBIN[y] = (np.array([iv.mid for iv in g_.index]), g_['mean'].values)
    share2[y] = fl((s_['resid'] < 2).mean() * 100, 1)

print(len(HH), 'hours from', HH.index.min(), 'to', HH.index.max())
show_numbers({'reg.resid.b': fl(R2.params['resid'], 2), 'reg.resid.se': fl(R2.bse['resid'], 2),
              'reg.share_resid_below2_2023': share2[2023], f'reg.share_resid_below2_{Y}': share2[Y]})'''),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 1.85))
for y, col, ls in ((2023, '#9a9a9a', ':'), (Y - 1, PAL['HU'], '--'), (Y, PAL['RO'], '-')):
    x_, y_ = RBIN[y]
    ax.plot(x_, y_, color=col, ls=ls, marker='o', ms=3, lw=1.4, label=str(y) if y != Y else f'{Y} (Jan-{MON_EN[END.month - 1]})')
ax.axhline(0, color=INK, lw=0.6)
ax.set_xlabel('residual load = load - wind - solar, GW (hourly)')
ax.set_ylabel('mean price\n(EUR/MWh)', fontsize=9)
legend_bottom(fig, ncol=3)
''' + finish("resid_price", 0.22))])

# =============================================================================
# 4 capture_rates
# =============================================================================
add("capture_rates",
    f"Capture rate of Romanian solar and onshore wind by calendar year, 2019 to {END} ({Y} = Jan-{MON_EN[C['month'] - 1]}): "
    "generation-weighted mean day-ahead price divided by the baseload price, in %; hourly prices to Sep 2025, 15-min from "
    "Oct 2025. Prints the solar capture rates of 2019, the last full year and the current year, the range of the wind capture "
    "rate and the like-for-like change in solar output.",
    "capture price, capture rate, cannibalisation, solar, wind, baseload price, day-ahead, Romania, OPCOM, renewables",
    PX_WORDS + "; " + GW_RO,
    [("md", "Capture price CP = sum_t p_t g_t dt_t / sum_t g_t dt_t; baseload B = sum_t p_t dt_t / sum_t dt_t; "
            "capture rate CR = CP / B (years with at least 90% of the generation intervals reported)."),
     ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + gen("ro")), ("code", CAPTURE),
     ("code", r'''CAPT = capture_years(['RO'], ['solar', 'wind_onshore'])
ro, dur = GR['RO'], PX['dur']
lfl = {}
for y in (Y - 1, Y):
    m = (LOC_YEAR == y) & (PX.index.month <= END.month)
    lfl[y] = fl((ro['solar'][m] * dur[m]).sum() / 1e6, 2)
wind = [CAPT[('RO', 'wind_onshore', y)]['crp'] for y in YEARS if ('RO', 'wind_onshore', y) in CAPT]
show_numbers({'capt.RO.solar.2019.crp': CAPT[('RO', 'solar', 2019)]['crp'],
              f'capt.RO.solar.{Y - 1}.crp': CAPT[('RO', 'solar', Y - 1)]['crp'],
              f'capt.RO.solar.{Y}.crp': CAPT[('RO', 'solar', Y)]['crp'],
              'capt.RO.wind_min': min(wind), 'capt.RO.wind_max': max(wind),
              'twh_lfl.solar_chg': fl((lfl[Y] / lfl[Y - 1] - 1) * 100, 1)})'''),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 1.85))
xs = np.arange(len(YEARS))
sol = [CAPT[('RO', 'solar', y)]['crp'] for y in YEARS]
ax.bar(xs - 0.2, sol, width=0.38, color=PAL['BG'], label='solar')
ax.bar(xs + 0.2, [CAPT[('RO', 'wind_onshore', y)]['crp'] for y in YEARS], width=0.38, color=PAL['HU'], label='wind')
ax.axhline(100, color=INK, lw=0.8, ls='--', label='100% = baseload price')
for i, v in enumerate(sol):
    ax.text(i - 0.2, v + 2, f'{v:.0f}', ha='center', fontsize=8)
ax.set_xticks(xs)
ax.set_xticklabels([str(y) + ('*' if y == Y else '') for y in YEARS])
ax.set_ylim(0, 125)
ax.set_ylabel('capture rate (%)', fontsize=9)
ax.text(0.0, 1.02, YTD, transform=ax.transAxes, fontsize=8, ha='left')
legend_bottom(fig, ncol=3)
''' + finish("capture_rates", 0.2))])

# =============================================================================
# 5 cannibal
# =============================================================================
add("cannibal",
    f"Cannibalisation of solar: monthly solar capture rate (%) against solar output as % of load in the month, Romania, Bulgaria "
    f"and Hungary, {N['cannib']['start'][:7]} to {N['cannib']['end'][:7]} (Hungary from Oct 2019), with the OLS line for "
    "Romania; prints the slopes (HAC standard errors, 6 lags), R-squared and number of months.",
    "cannibalisation, capture rate, solar share, regression, Newey-West, solar, Romania, Bulgaria, Hungary, day-ahead, renewables",
    PX_WORDS + "; " + GW_RO + "; " + GW_BG + "; " + GW_HU,
    [("md", "For each month m: CR_m = capture price / baseload price (%), share_m = solar energy / load energy (%). "
            "OLS CR_m = a + b share_m + e_m with HAC standard errors (6 lags); months with at least 90% of the intervals reported."),
     ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + gen("ro", "bg", "hu")), ("code", CAPTURE),
     ("code", r'''import statsmodels.api as sm

LOC_MONTH = PX.index.to_period('M')
MON = {}
for z in ('RO', 'BG', 'HU'):
    rows = []
    for per in pd.period_range('2019-01', END.strftime('%Y-%m'), freq='M'):
        mk = pd.Series(LOC_MONTH == per, index=PX.index)
        if GR[z]['solar'][mk].notna().sum() < 0.9 * mk.sum() or PX[z][mk].notna().sum() < 0.9 * mk.sum():
            continue
        cp, base, e = capture(z, 'solar', mk)
        ld = (GR[z]['load'][mk] * PX['dur'][mk]).sum()
        rows.append((per.to_timestamp(), cp / base * 100, e / ld * 100, base))
    MON[z] = pd.DataFrame(rows, columns=['month', 'cr', 'share', 'base']).set_index('month')

fit = {z: sm.OLS(MON[z]['cr'], sm.add_constant(MON[z]['share'])).fit(cov_type='HAC', cov_kwds={'maxlags': 6}) for z in MON}
Rc = fit['RO']
show_numbers({'cannib.b': fl(Rc.params['share'], 2), 'cannib.se': fl(Rc.bse['share'], 2), 'cannib.bneg': fl(-Rc.params['share'], 1),
              'cannib.r2': fl(Rc.rsquared, 2), 'cannib.n': len(MON['RO']),
              'cannib.BG.b': fl(fit['BG'].params['share'], 2), 'cannib.HU.b': fl(fit['HU'].params['share'], 2)})'''),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 1.85))
for z, mk in (('HU', 's'), ('BG', '^'), ('RO', 'o')):
    ax.scatter(MON[z]['share'], MON[z]['cr'], s=12 if z == 'RO' else 8, color=PAL[z], marker=mk,
               alpha=0.85 if z == 'RO' else 0.5, lw=0, label=ZN[z])
xx = np.linspace(0, MON['RO']['share'].max() * 1.02, 50)
ax.plot(xx, Rc.params['const'] + Rc.params['share'] * xx, color=PAL['RO'], lw=1.2, label='Romania, fit')
ax.axhline(100, color=INK, lw=0.6, ls='--')
ax.set_xlabel('solar output as % of load in the month')
ax.set_ylabel('solar capture\nrate (%)', fontsize=9)
legend_bottom(fig, ncol=4)
''' + finish("cannibal", 0.26))])

# =============================================================================
# 6 capture_region
# =============================================================================
add("capture_region",
    f"Yearly solar capture rate (%) of Romania, Bulgaria and Hungary, 2019 (Hungary 2020) to {END} ({Y} = "
    f"Jan-{MON_EN[C['month'] - 1]}); Bulgaria publishes hourly solar output only, so after 1 Oct 2025 its hourly value is paired "
    "with each quarter-hour price. Prints the capture rates of the last full year and the current year.",
    "capture rate, cannibalisation, solar, regional market, market coupling, Romania, Bulgaria, Hungary, day-ahead, renewables",
    PX_WORDS + "; " + GW_RO + "; " + GW_BG + "; " + GW_HU,
    [("md", "Capture rate CR = (sum_t p_t g_t dt_t / sum_t g_t dt_t) / (sum_t p_t dt_t / sum_t dt_t), per zone and calendar year "
            "(years with at least 90% of the solar intervals reported)."),
     ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + gen("ro", "bg", "hu")), ("code", CAPTURE),
     ("code", r'''CAPT = capture_years(['RO', 'BG', 'HU'], ['solar'])
show_numbers({f'capt.RO.solar.{Y - 1}.crp': CAPT[('RO', 'solar', Y - 1)]['crp'],
              f'capt.BG.solar.{Y - 1}.crp': CAPT[('BG', 'solar', Y - 1)]['crp'],
              f'capt.HU.solar.{Y - 1}.crp': CAPT[('HU', 'solar', Y - 1)]['crp'],
              f'capt.BG.solar.{Y}.crp': CAPT[('BG', 'solar', Y)]['crp']})'''),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 1.8))
for z in ('RO', 'BG', 'HU'):
    ys = [y for y in YEARS if (z, 'solar', y) in CAPT]
    ax.plot([str(y) + ('*' if y == Y else '') for y in ys], [CAPT[(z, 'solar', y)]['crp'] for y in ys], color=PAL[z],
            ls=ZONE_LS[z], marker='o', ms=4, label=ZN[z])
ax.axhline(100, color=INK, lw=0.6, ls='--')
ax.set_ylabel('solar capture\nrate (%)', fontsize=9)
ax.text(0.99, 0.9, YTD, transform=ax.transAxes, fontsize=8, ha='right')
legend_bottom(fig, ncol=3)
''' + finish("capture_region", 0.2))])

# =============================================================================
# 7 cheap_hours
# =============================================================================
add("cheap_hours",
    f"Share of Romanian solar energy sold in the cheapest hours: intervals of each calendar year ranked by day-ahead price, "
    f"cumulative % of time (duration-weighted) against cumulative % of solar energy, for 2019, 2023, {YP} and {Y} (to {END}). "
    "Prints the share of solar output sold in the cheapest 10% of hours and at prices <= 0.",
    "solar, cheapest hours, Lorenz curve, cannibalisation, negative prices, day-ahead, Romania, OPCOM, energy share",
    PX_WORDS + "; " + GW_RO,
    [("md", "Sort the intervals of a year by price; x = cumulative share of time (interval lengths), y = cumulative share of "
            "solar energy. A curve above the diagonal means solar is concentrated in cheap hours."),
     ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + gen("ro")),
     ("code", r'''ro = GR['RO']
LOR, CHEAP = {}, {}
for y in (2019, 2023, Y - 1, Y):
    m = (LOC_YEAR == y) & PX['RO'].notna().values & ro['solar'].notna().values
    p_, g_, w_ = PX['RO'][m].values, ro['solar'][m].values, PX['dur'][m].values
    o = np.argsort(p_, kind='stable')
    tsh = np.cumsum(w_[o]) / w_.sum()
    esh = np.cumsum((g_ * w_)[o]) / (g_ * w_).sum()
    LOR[y] = (tsh, esh)
    k10 = np.searchsorted(tsh, 0.10)
    CHEAP[y] = {'e_in_cheap10': fl(esh[k10] * 100, 1), 'e_le0': fl((g_ * w_)[p_ <= 0].sum() / (g_ * w_).sum() * 100, 1)}
show_numbers({'cheap.2019.e_in_cheap10': CHEAP[2019]['e_in_cheap10'], f'cheap.{Y - 1}.e_in_cheap10': CHEAP[Y - 1]['e_in_cheap10'],
              f'cheap.{Y - 1}.e_le0': CHEAP[Y - 1]['e_le0'], f'cheap.{Y}.e_in_cheap10': CHEAP[Y]['e_in_cheap10']})'''),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 1.85))
for y, col, ls in ((2019, '#9a9a9a', ':'), (2023, PAL['HU'], '-.'), (Y - 1, PAL['BG'], '--'), (Y, PAL['RO'], '-')):
    tsh, esh = LOR[y]
    ax.plot(tsh * 100, esh * 100, color=col, ls=ls, lw=1.5, label=str(y) + ('*' if y == Y else ''))
ax.plot([0, 100], [0, 100], color=INK, lw=0.6)
ax.axvline(10, color=PAL['c8'], lw=0.8, ls='--')
ax.set_xlabel('hours of the year ranked from the cheapest, cumulative %')
ax.set_ylabel('solar energy\n(cumulative %)', fontsize=9)
legend_bottom(fig, ncol=4)
''' + finish("cheap_hours", 0.23))])

# =============================================================================
# 8 neg_hours
# =============================================================================
add("neg_hours",
    f"Negative day-ahead prices: number of hour-equivalents with a negative price per year in Romania, Bulgaria, Hungary and "
    f"Germany-Luxembourg, 2022 to {END} ({Y} = Jan-{MON_EN[C['month'] - 1]}); a 15-min interval counts 0.25 h. Prints the "
    "counts of the last full year and the like-for-like January-cut-off counts.",
    "negative prices, day-ahead, hour-equivalents, 15-minute MTU, solar, Romania, Bulgaria, Hungary, Germany, market coupling",
    PX_WORDS,
    [("md", "Hour-equivalents with a negative price: H_y = sum over intervals of year y with p_t < 0 of the interval length dt_t (h)."),
     ("code", PERIOD), ("code", PRICES),
     ("code", r'''ZONES = ['RO', 'BG', 'HU', 'DE_LU']
hours = {z: {y: fl(PX['dur'][(LOC_YEAR == y) & (PX[z] < 0).values].sum(), 2) for y in YEARS} for z in ZONES}
lfl = {z: {y: fl(PX['dur'][(LOC_YEAR == y) & (PX.index.month <= END.month) & (PX[z] < 0).values].sum(), 2) for y in (Y - 1, Y)}
       for z in ZONES}
show_numbers({f'neg.hours.RO.{Y - 1}': hours['RO'][Y - 1], f'neg.hours.DE_LU.{Y - 1}': hours['DE_LU'][Y - 1],
              f'neg.lfl.RO.{Y - 1}': lfl['RO'][Y - 1], f'neg.lfl.RO.{Y}': lfl['RO'][Y],
              f'neg.lfl.HU.{Y - 1}': lfl['HU'][Y - 1], f'neg.lfl.HU.{Y}': lfl['HU'][Y]})'''),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 1.85))
yy = [y for y in YEARS if y >= 2022]
for i, z in enumerate(ZONES):
    ax.bar(np.arange(len(yy)) + (i - 1.5) * 0.2, [hours[z][y] for y in yy], width=0.2, color=PAL[z], label=ZN[z])
ax.set_xticks(range(len(yy)))
ax.set_xticklabels([str(y) + ('*' if y == Y else '') for y in yy])
ax.set_ylabel('negative hours\n(hour-equiv.)', fontsize=9)
ax.text(0.01, 0.9, YTD, transform=ax.transAxes, fontsize=8)
legend_bottom(fig, ncol=4)
''' + finish("neg_hours", 0.2))])

# =============================================================================
# 9 shape15
# =============================================================================
add("shape15",
    f"Intraday shape of the Romanian day-ahead price at 15-min resolution: mean price of each of the 96 quarter-hours (CET) by "
    f"season over the last 12 months, {LTM_START} to {END}. Prints the spring minimum and maximum (with their times) and the "
    "daily range of spring, summer and winter.",
    "intraday profile, 15-minute MTU, quarter-hour, duck curve, seasonality, day-ahead, Romania, OPCOM, solar",
    PX_WORDS,
    [("md", "Mean price of quarter-hour slot k = 4 x hour + minute / 15 over the days of each season (meteorological seasons)."),
     ("code", PERIOD), ("code", PRICES),
     ("code", r'''qq = PX.loc[(PX.index >= LTM0) & (PX.index >= MTU15), ['RO']].copy()
qq['slot'] = qq.index.hour * 4 + qq.index.minute // 15
SEAS = {'winter': [12, 1, 2], 'spring': [3, 4, 5], 'summer': [6, 7, 8], 'autumn': [9, 10, 11]}
PROF = {s: qq[qq.index.month.isin(ms)].groupby('slot')['RO'].mean() for s, ms in SEAS.items()}
hm = lambda k: f'{k // 4:02d}:{k % 4 * 15:02d}'
sp = PROF['spring']
show_numbers({'shape.spring.min': fl(sp.min(), 1), 'shape.spring.min_t': hm(sp.idxmin()),
              'shape.spring.max': fl(sp.max(), 1), 'shape.spring.max_t': hm(sp.idxmax()),
              'shape.spring.range': fl(sp.max() - sp.min(), 1), 'shape.summer.range': fl(PROF['summer'].max() - PROF['summer'].min(), 1),
              'shape.winter.range': fl(PROF['winter'].max() - PROF['winter'].min(), 1)})'''),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 1.85))
SL = {'winter': 'winter (Dec-Feb)', 'spring': 'spring (Mar-May)', 'summer': 'summer (Jun-Aug)', 'autumn': 'autumn (Sep-Nov)'}
SC = {'winter': PAL['c7'], 'spring': PAL['HU'], 'summer': PAL['DE_LU'], 'autumn': PAL['BG']}
for s_, pr in PROF.items():
    ax.step(np.arange(96) / 4, pr.values, where='post', color=SC[s_], lw=1.3, label=SL[s_])
ax.axhline(0, color=INK, lw=0.6)
ax.set_xticks(range(0, 25, 3))
ax.set_xlabel('time of day (CET), 96 quarter-hours')
ax.set_ylabel('mean price\n(EUR/MWh)', fontsize=9)
legend_bottom(fig, ncol=4)
''' + finish("shape15", 0.22))])

# =============================================================================
# 10 spreads
# =============================================================================
add("spreads",
    f"Daily price spread: monthly mean of the daily difference between the 2 most expensive and the 2 cheapest hours of the "
    f"day-ahead price (hourly prices, 15-min averaged to the hour) in Romania, Bulgaria, Hungary and Germany-Luxembourg, 2019 "
    f"to {END}; symmetric log scale above 100 EUR/MWh. Prints the mean daily spread of {Y} by zone.",
    "price spread, daily spread, top-bottom spread, battery, arbitrage, volatility, day-ahead, Romania, Bulgaria, Hungary, Germany",
    PX_WORDS,
    [("md", "Spread of day d: mean of the 2 most expensive hours minus mean of the 2 cheapest hours (duration-weighted, complete "
            "delivery days only); monthly means of the daily values."),
     ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + DAYS),
     ("code", r'''def tbk(p, dur, k):
    """Top-k minus bottom-k hours spread of one day (duration-weighted means of the k most expensive / cheapest hours)."""
    o = np.argsort(p)

    def avg(idx):
        acc, tot = 0.0, 0.0
        for i_, wi in zip(idx, dur[idx]):
            take = min(wi, k - tot)
            if take <= 0:
                break
            acc += p[i_] * take
            tot += take
        return acc / tot
    return avg(o[::-1]) - avg(o)


ZONES = ['RO', 'BG', 'HU', 'DE_LU']
SPR = {}
for z in ZONES:
    dg = day_groups(z, start=pd.Timestamp('2019-01-01').tz_localize(TZ), hourly=True)
    SPR[z] = pd.Series({dd: tbk(p, w, 2) for dd, (p, w) in dg.items()})
SPRM = {z: SPR[z].groupby(SPR[z].index.to_period('M')).mean() for z in ZONES}
show_numbers({f'spread.{z}.{Y}': fl(SPR[z][SPR[z].index.year == Y].mean(), 1) for z in ZONES})'''),
     ("code", r'''import matplotlib.dates as mdates

fig, ax = plt.subplots(figsize=(6.4, 1.8))
for z in ZONES:
    s = SPRM[z]
    ax.plot(s.index.to_timestamp(), s.values, color=PAL[z], ls=ZONE_LS[z], lw=1.2, label=ZN[z])
ax.set_ylabel('top-2 minus bottom-2\nhours (EUR/MWh)', fontsize=8.5)
ax.set_yscale('symlog', linthresh=100)
ax.set_yticks([0, 50, 100, 200, 500])
ax.set_yticklabels(['0', '50', '100', '200', '500'])
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.set_xlim(pd.Timestamp('2019-01-01'), END)
legend_bottom(fig, ncol=4)
''' + finish("spreads", 0.2))])

# =============================================================================
# 11 bat_years
# =============================================================================
BAT_MD = ("Battery of 1 MW and E = 1, 2 or 4 MWh, round-trip efficiency 85%, at most one full cycle a day, empty at the start "
          "and end of each delivery day (Cole & Karmakar, 2023, NREL). For each day a linear programme (scipy, HiGHS) maximises "
          "sum_t p_t (d_t - c_t) dt_t. About 1 ms per day, so the whole computation runs in well under a minute.")
add("bat_years",
    f"Revenue of a 1 MW battery arbitraging the Romanian day-ahead market with perfect foresight, by year 2019-{YP} and for the "
    f"last 12 months ({LTM_START} to {END}), for 1, 2 and 4 hours of storage (thousand EUR per MW-year); round trip 85%, at most "
    "one cycle a day, one linear programme per delivery day. Prints the 2h revenue of selected years and of the last 12 months "
    "and the 4h/2h ratio.",
    "battery, energy storage, arbitrage, linear programming, perfect foresight, revenue, day-ahead, Romania, OPCOM, 15-minute MTU",
    PX_WORDS + " (Romanian prices only)",
    [("md", BAT_MD), ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + DAYS), ("code", BATTERY),
     ("code", r'''import time
t0 = time.time()
dg_ro = day_groups('RO', start=pd.Timestamp('2019-01-01').tz_localize(TZ))
PF = {E: run_battery(dg_ro, E) for E in DURS}             # daily revenue, EUR per MW
print(len(dg_ro), 'delivery days,', f'{time.time() - t0:.0f} s')
ltm = {E: fl(PF[E][PF[E].index >= LTM0.tz_localize(None)].sum() / 1000, 1) for E in DURS}
pf_year = {E: {y: fl(PF[E][PF[E].index.year == y].sum() / 1000, 1) for y in YEARS if y < Y} for E in DURS}
show_numbers({'bat.pf.2.2019': pf_year[2][2019], 'bat.pf.2.2022': pf_year[2][2022], f'bat.pf.2.{Y - 1}': pf_year[2][Y - 1],
              'bat.ltm.2.pf': ltm[2], 'bat.x_4v2': fl(ltm[4] / ltm[2], 2)})'''),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 1.8))
yb = list(range(YEARS[0], Y)) + ['LTM']
for i, (E, col) in enumerate(zip(DURS, (PAL['HU'], PAL['RO'], PAL['c7']))):
    vals = [pf_year[E][y] for y in yb[:-1]] + [ltm[E]]
    ax.bar(np.arange(len(yb)) + (i - 1) * 0.27, vals, width=0.27, color=col, label=f'{E} h of storage')
ax.set_xticks(range(len(yb)))
ax.set_xticklabels([str(y) for y in yb[:-1]] + ['last\n12 months'], fontsize=8.5)
ax.set_ylabel('thousand EUR\nper MW-year', fontsize=9)
legend_bottom(fig, ncol=3)
''' + finish("bat_years", 0.2))])

# =============================================================================
# 12 bat_rules
# =============================================================================
add("bat_rules",
    f"Battery revenue in the last 12 months ({LTM_START} to {END}), Romanian day-ahead market, 1 MW with 1, 2 or 4 h of storage, "
    "round trip 85%: perfect foresight on 15-min prices, perfect foresight on hourly averages, and two forecast rules known at "
    "gate closure (mean profile of the last 7 days; yesterday's prices); rules evaluated on the common days and scaled to the "
    "full period. Prints the share of the perfect-foresight revenue earned by each rule.",
    "battery, energy storage, arbitrage, forecast, perfect foresight, linear programming, 15-minute MTU, day-ahead, Romania, OPCOM",
    PX_WORDS + " (Romanian prices only)",
    [("md", BAT_MD + " A rule optimises the schedule on its forecast and is paid the realised prices."),
     ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + DAYS), ("code", BATTERY),
     ("code", r'''def yesterday(dg):
    """Forecast for day d = the prices of day d-1 (known at gate closure on d-1)."""
    return {day: dg[day - pd.Timedelta(days=1)][0] for day in dg if (day - pd.Timedelta(days=1)) in dg}


def week_ago_mean(dg):
    """Forecast for day d = mean profile of days d-1 ... d-7 with the same number of intervals (known at gate closure)."""
    out = {}
    for day in dg:
        past = [dg[day - pd.Timedelta(days=j)][0] for j in range(1, 8) if (day - pd.Timedelta(days=j)) in dg and
                len(dg[day - pd.Timedelta(days=j)][0]) == len(dg[day][0])]
        if len(past) >= 5:
            out[day] = np.mean(past, axis=0)
    return out


native, hourly = day_groups('RO', start=LTM0), day_groups('RO', start=LTM0, hourly=True)
ext = day_groups('RO', start=LTM0 - pd.Timedelta(days=8))       # 8 days before the window for the forecast rules
B, NUM = {}, {}
for E in DURS:
    lt, hr = run_battery(native, E), run_battery(hourly, E)
    yd, wk = run_battery(native, E, yesterday(ext)), run_battery(native, E, week_ago_mean(ext))
    common = lt.index.intersection(yd.index).intersection(wk.index)
    B[E] = {'pf': lt.sum() / 1000, 'hourly': hr.reindex(lt.index).sum() / 1000,
            'wk': wk[common].sum() / 1000 * len(lt) / len(common), 'yday': yd[common].sum() / 1000 * len(lt) / len(common)}
    NUM[f'bat.ltm.{E}.wk_pct'] = fl(wk[common].sum() / lt[common].sum() * 100, 1)
    NUM[f'bat.ltm.{E}.yday_pct'] = fl(yd[common].sum() / lt[common].sum() * 100, 1)
    print(f'{E} h: {len(lt)} days, {len(common)} common days for the rules')
show_numbers(NUM)'''),
     ("code", r'''fig, ax = plt.subplots(figsize=(6.4, 1.85))
lab = ['perfect foresight,\n15-min', 'perfect foresight,\nhourly averages', 'rule: mean of\nlast 7 days', "rule: yesterday's\nprices"]
for i, (E, col) in enumerate(zip(DURS, (PAL['HU'], PAL['RO'], PAL['c7']))):
    b = B[E]
    ax.bar(np.arange(4) + (i - 1) * 0.27, [b['pf'], b['hourly'], b['wk'], b['yday']], width=0.27, color=col, label=f'{E} h')
ax.set_xticks(range(4))
ax.set_xticklabels(lab, fontsize=8.5)
ax.set_ylabel('thousand EUR\nper MW', fontsize=9)
legend_bottom(fig, ncol=3)
''' + finish("bat_rules", 0.2))])

# =============================================================================
# 13 bat_region
# =============================================================================
add("bat_region",
    f"Regional battery arbitrage: mean daily revenue (EUR per MW) of a 2h, 1 MW battery with perfect foresight on the day-ahead "
    f"prices of Romania, Bulgaria and Hungary, monthly, 2024-01 to {END[:7]}, and the monthly mean output of the Romanian and "
    "Bulgarian battery fleets as reported to ENTSO-E. Prints the revenue of the last 12 months by zone (with Germany-Luxembourg) "
    "and the correlation of daily revenues between Romania and its neighbours.",
    "battery, energy storage, arbitrage, regional market, market coupling, correlation, Romania, Bulgaria, Hungary, Germany, ENTSO-E",
    PX_WORDS + "; generation_ro_mw_native_utc.csv and generation_bg_mw_native_utc.csv: battery discharge of the Romanian and "
    "Bulgarian fleets (MW, ENTSO-E via energy-charts.info)",
    [("md", BAT_MD), ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + DAYS), ("code", BATTERY),
     ("code", r'''T24 = pd.Timestamp('2024-01-01').tz_localize(TZ)
D2 = {z: run_battery(day_groups(z, start=T24), 2) for z in ('RO', 'BG', 'HU')}       # daily revenue, EUR per MW
D2['DE_LU'] = run_battery(day_groups('DE_LU', start=LTM0), 2)
LTM = {z: s[s.index >= LTM0.tz_localize(None)] for z, s in D2.items()}
BMM = {z: D2[z].groupby(D2[z].index.to_period('M')).mean() for z in ('RO', 'BG', 'HU')}

FLEET = {}
for c in ('ro', 'bg'):
    g = pd.read_csv(DATA + f'generation_{c}_mw_native_utc.csv', parse_dates=['timestamp_utc'], usecols=['timestamp_utc', 'battery'])
    b = g.set_index('timestamp_utc')['battery']
    b.index = b.index.tz_convert(TZ)
    b = b[(b.index >= T24) & (b.index < END_X)]
    FLEET[c.upper()] = b.groupby(b.index.tz_localize(None).to_period('M')).mean()

show_numbers({**{f'bat.reg.{z}': fl(LTM[z].sum() / 1000, 1) for z in ('RO', 'BG', 'HU', 'DE_LU')},
              'bat.corr_ro_bg': fl(pd.concat([LTM['RO'], LTM['BG']], axis=1).dropna().corr().iloc[0, 1], 2),
              'bat.corr_ro_hu': fl(pd.concat([LTM['RO'], LTM['HU']], axis=1).dropna().corr().iloc[0, 1], 2)})'''),
     ("code", r'''import matplotlib.dates as mdates

fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.9))
for z in ('RO', 'BG', 'HU'):
    s = BMM[z]
    axs[0].plot(s.index.to_timestamp(), s.values, color=PAL[z], ls=ZONE_LS[z], lw=1.3, label=ZN[z])
axs[0].set_ylabel('2h battery, EUR\nper MW per day', fontsize=8.5)
for ax in axs:
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.set_xlim(pd.Timestamp('2024-01-01'), END)
for z in ('RO', 'BG'):
    s = FLEET[z].dropna()
    axs[1].plot(s.index.to_timestamp(), s.values, color=PAL[z], ls=ZONE_LS[z], lw=1.3)
axs[1].set_ylabel('battery output\n(MW, monthly)', fontsize=8.5)
legend_bottom(fig, ncol=3)
''' + finish("bat_region", 0.22))])

# =============================================================================
# 14 case_week
# =============================================================================
add("case_week",
    f"Case study: the Monday-to-Sunday week with the most negative-price hours in the month of {Y} with the most negative hours "
    f"({N['case']['week']} to {N['case']['week_end']}): Romanian 15-min day-ahead price with the optimal schedule of a 2h, 1 MW "
    "battery (charging and discharging intervals), and Romanian solar and wind output (GW). Prints the negative hours, price range, "
    "solar capture price and rate of the week and the battery revenue against the last-12-month average.",
    "case study, negative prices, battery, energy storage, solar, wind, capture rate, 15-minute MTU, day-ahead, Romania, OPCOM",
    PX_WORDS + "; " + GW_RO,
    [("md", BAT_MD + " The week is chosen from the data: the month of the current year with the most negative hour-equivalents, "
                     "then its Monday-to-Sunday week with the most."),
     ("code", PERIOD), ("code", PRICES), ("code", HFLOOR + "\n\n\n" + gen("ro")), ("code", CAPTURE),
     ("code", DAYS), ("code", BATTERY),
     ("code", r'''neg = PX['RO'] < 0
NEGM = PX.loc[neg, 'dur'].groupby(PX.index[neg].to_period('M')).sum()          # negative hour-equivalents by month
CM = NEGM[[p.year == Y for p in NEGM.index]].idxmax()
cm_mask = PX.index.to_period('M') == CM
naive = PX.index.tz_localize(None)
mons = sorted({(t - pd.Timedelta(days=t.dayofweek)).normalize() for t in naive[cm_mask]})


def neg_week(m0):
    msk = (naive >= m0) & (naive < m0 + pd.Timedelta(days=7))
    return PX['dur'][msk & neg.values].sum()


WK0 = max(mons, key=neg_week)
WK1 = WK0 + pd.Timedelta(days=7)
wmask = (naive >= WK0) & (naive < WK1)
cp, base, _ = capture('RO', 'solar', pd.Series(wmask, index=PX.index))

sched, rev = [], []
for k in range(7):
    day = WK0 + pd.Timedelta(days=k)
    msk = (naive >= day) & (naive < day + pd.Timedelta(days=1))
    p, w = PX['RO'][msk].values, PX['dur'][msk].values
    c, d = battery_day(p, w, 2)
    rev.append(revenue(p, w, c, d))
    sched.append(pd.DataFrame({'p': p, 'net': d - c}, index=PX.index[msk]))
WEEK = pd.concat(sched)
ltm2 = run_battery(day_groups('RO', start=LTM0), 2)       # 2h battery, perfect foresight, last 12 months
print('month with the most negative hours:', CM, '| week', WK0.date(), 'to', (WK1 - pd.Timedelta(days=1)).date())
show_numbers({'case.week': str(WK0.date()), 'case.week_neg_h': fl(PX['dur'][wmask & neg.values].sum(), 2),
              'case.week_min': fl(PX['RO'][wmask].min(), 2), 'case.week_max': fl(PX['RO'][wmask].max(), 2),
              'case.week_cp': fl(cp, 1), 'case.week_base': fl(base, 1), 'case.week_cr': fl(cp / base * 100, 1),
              'case.week_bat2_mean_day': fl(np.mean(rev), 0), 'case.bat2_day_ltm': fl(ltm2.mean(), 0)})'''),
     ("code", r'''import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter

fig, axs = plt.subplots(2, 1, figsize=(6.4, 2.5), sharex=True, gridspec_kw={'height_ratios': [1.3, 1]})
tt = WEEK.index.tz_localize(None)
axs[0].step(tt, WEEK['p'], where='post', color=PAL['RO'], lw=0.9, label='RO price, 15-min')
ch, dc = WEEK['net'] < -1e-6, WEEK['net'] > 1e-6
axs[0].fill_between(tt, WEEK['p'].min(), WEEK['p'].max(), where=ch.values, step='post', color=PAL['HU'], alpha=0.25, lw=0,
                    label='2h battery charging')
axs[0].fill_between(tt, WEEK['p'].min(), WEEK['p'].max(), where=dc.values, step='post', color=PAL['DE_LU'], alpha=0.3, lw=0,
                    label='2h battery discharging')
axs[0].axhline(0, color=INK, lw=0.6)
axs[0].set_ylabel('EUR/MWh', fontsize=9.5)
g = GR['RO'].loc[WEEK.index, ['solar', 'wind_onshore']] / 1000
axs[1].plot(tt, g['solar'], color=PAL['BG'], lw=1.1, label='solar, GW')
axs[1].plot(tt, g['wind_onshore'], color=PAL['HU'], lw=1.1, label='wind, GW')
axs[1].set_ylabel('GW', fontsize=9.5)
axs[1].xaxis.set_major_locator(mdates.DayLocator())
dn = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
axs[1].xaxis.set_major_formatter(FuncFormatter(lambda v, p: dn[mdates.num2date(v).weekday()] + ' ' + str(mdates.num2date(v).day)))
legend_bottom(fig, ncol=3)
''' + finish("case_week", 0.2))])


# =============================================================================
# 15 rogb_summer (case study: summer, Romania and Bulgaria)
# =============================================================================
RG_ = N["rogb"]
ROGB_LOAD = "Y = " + str(RG_["year"]) + """
TZL = 'Europe/Bucharest'
CB = pd.read_csv(DATA + 'crossborder_ro_mw_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')
CB.index = pd.to_datetime(CB.index, utc=True).tz_convert(TZL)
PH = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')
PH.index = pd.to_datetime(PH.index, utc=True).tz_convert(TZL)
summer = (CB.index.year == Y) & CB.index.month.isin([6, 7, 8])
RG = CB.loc[summer, ['bulgaria', 'hungary', 'serbia', 'sum']].join(PH[['RO', 'BG']], how='left')
H = RG.groupby(RG.index.hour).mean()
mid_h = RG[RG.index.hour.isin([12, 13, 14])]
eve_h = RG[RG.index.hour.isin([19, 20, 21, 22])]
mid = mid_h.groupby(mid_h.index.normalize())['bulgaria'].mean()
eve = eve_h.groupby(eve_h.index.normalize())['bulgaria'].mean()
hb = int(H['bulgaria'].idxmax())
show_numbers({'rogb.n_days': int(len(RG.index.normalize().unique())),
              'rogb.exp_mw': fl(-H['sum'].min(), 0), 'rogb.imp_mw': fl(H['sum'].max(), 0),
              'rogb.hu_mid_mw': fl(-H.loc[12, 'hungary'], 0), 'rogb.rs_mid_mw': fl(-H.loc[12, 'serbia'], 0),
              'rogb.bg_eve_h': hb, 'rogb.bg_eve_mw': fl(H['bulgaria'].max(), 0),
              'rogb.days_bg_eve_imp': int((eve > 0).sum()), 'rogb.n_days_mid': int((mid < 0).sum()),
              'rogb.p_ro_eve': fl(H.loc[hb, 'RO'], 1), 'rogb.p_bg_eve': fl(H.loc[hb, 'BG'], 1),
              'rogb.p_gap_eve': fl(H.loc[hb, 'RO'] - H.loc[hb, 'BG'], 1)})"""
ROGB_PLOT = """fig, axs = plt.subplots(1, 2, figsize=(6.4, 1.95))
hh = H.index.values
axs[0].axhline(0, color=INK, lw=0.6)
axs[0].plot(hh, H['sum'] / 1000, color=PAL['RO'], lw=1.8, label='Romania: net flow on all borders; RO price')
axs[0].plot(hh, H['bulgaria'] / 1000, color=PAL['BG'], lw=1.6, ls='--', label='Bulgaria: flow on the RO-BG border; BG price')
axs[0].set_ylabel('net import, GW\\n(< 0: export)', fontsize=8.5)
axs[0].set_title('cross-border flows', fontsize=9.5)
axs[1].plot(hh, H['RO'], color=PAL['RO'], lw=1.8)
axs[1].plot(hh, H['BG'], color=PAL['BG'], lw=1.6, ls='--')
axs[1].set_title('day-ahead prices', fontsize=9.5)
axs[1].set_ylabel('day-ahead price\\n(EUR/MWh)', fontsize=8.5)
for ax in axs:
    ax.set_xticks([0, 6, 12, 18, 23])
    ax.set_xlabel('hour of the day (Romanian time)', fontsize=8.5)
legend_bottom(fig, ncol=2)
fig.subplots_adjust(wspace=0.45)
"""
add("rogb_summer",
    f"Case study, summer {RG_['year']} ({RG_['start']} to {RG_['end']}): mean cross-border physical flow of Romania by hour of the day "
    "(all borders, and the border with Bulgaria; + = net import into Romania) and mean day-ahead prices of Romania and Bulgaria by "
    "hour. Romania exports at midday, mostly to Hungary and Serbia, and imports from Bulgaria every evening, when its price is above "
    "the Bulgarian one.",
    "cross-border flows, interconnection, market coupling, Romania, Bulgaria, day-ahead price, price spread, solar, evening peak",
    "crossborder_ro_mw_hourly_utc.csv: physical flows of Romania per border (MW, + = import), hourly, energy-charts.info / ENTSO-E; "
    "power_da_prices_hourly_utc.csv: hourly day-ahead prices of Romania (OPCOM) and Bulgaria (IBEX), EUR/MWh",
    [("md", "Hours are Romanian local time. Midday window: 12:00-15:00; evening window: 19:00-23:00. Moldova and Ukraine borders "
            "are only partly reported, so 'all borders' is mostly Bulgaria, Hungary and Serbia."),
     ("code", ROGB_LOAD),
     ("code", ROGB_PLOT + finish("rogb_summer", 0.27))],
    title=f"Summer {RG_['year']}: Romania exports at midday and buys from Bulgaria in the evening")


# =============================================================================
# Build, execute, check the printed numbers against L6_numbers.json
# =============================================================================
def lookup(key):
    v = N
    for part in key.split("."):
        v = v[part]
    return v


def check(q):
    """Compare every 'key value' line printed by the notebook with L6_numbers.json."""
    import nbformat
    nb = nbformat.read(os.path.join(q.folder, q.name + ".ipynb"), as_version=4)
    bad, n = [], 0
    for cell in nb.cells:
        for o in cell.get("outputs", []):
            for line in o.get("text", "").splitlines():
                parts = line.split()
                if len(parts) != 2 or "." not in parts[0] or parts[0][0].isdigit():
                    continue
                try:
                    ref = lookup(parts[0])
                except (KeyError, TypeError):
                    continue
                n += 1
                try:
                    ok = abs(float(parts[1]) - float(ref)) <= 1e-6 + 1e-9 * abs(float(ref))
                except ValueError:
                    ok = parts[1] == str(ref)
                if not ok:
                    bad.append(f"{parts[0]}: notebook {parts[1]} vs JSON {ref}")
    return n, bad


if __name__ == "__main__":
    only = sys.argv[1:]
    report = []
    for s in Q:
        if only and s["chart"] not in only:
            continue
        q = Quantlet(6, s["chart"], s["description"], s["keywords"], s["datafile"], title=s["title"])
        q.md(INTRO_SETUP).code(STYLE)
        for kind, text in s["cells"]:
            (q.md if kind == "md" else q.code)(text)
        t0 = time.time()
        q.write(execute=True)
        n, bad = check(q)
        report.append((q.name, time.time() - t0, n, bad))
        print(f"  {time.time() - t0:.0f} s, {n} numbers checked" + ("" if not bad else "  MISMATCH: " + "; ".join(bad)))
    print("\nQuantlet                       time(s)  numbers  mismatches")
    for name, t, n, bad in report:
        print(f"{name:<30} {t:7.0f}  {n:7d}  {len(bad)}")
    if any(r[3] for r in report):
        sys.exit("number mismatches: see above")
