"""make_quantlet_data.py -- builds the Quantlet EMQA_data (Quantlets/Data/EMQA_data): how the course data are
downloaded and how to load every series. Run from the repository: python data/make_quantlet_data.py"""
import os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "lectures", "common"))
from emqa_quantlet import Quantlet, QL_ROOT  # noqa: E402

q = Quantlet(k=0, chart="data_coverage",
             title="The data of the course: sources, coverage and loading",
             description="Downloads every series used in the EMQA course from its public source (day-ahead power prices of Romania, Bulgaria, Hungary and Germany-Luxembourg, generation by source and load, cross-border physical flows of Romania, fuels, EU carbon allowances, exchange rates, Romanian energy equities, OPCOM curves and forward trades), and shows the period covered by each file of data/clean.",
             keywords="energy data, day-ahead prices, generation mix, cross-border flows, ENTSO-E, energy-charts, OPCOM, data coverage",
             datafile="All files of data/clean, written by download_all.py, download_L5.py and download_L6.py; sources in data/SOURCES.md")
q.name = "EMQA_data"
q.folder = os.path.join(QL_ROOT, "Data", "EMQA_data")

q.md("## The download scripts\n\n"
     "`download_all.py` downloads every series from its public source, keeps the raw answers in `data/raw/` and writes "
     "the clean files in `data/clean/`; `download_L5.py` and `download_L6.py` add the series of Lectures 5 and 6. "
     "Nothing is interpolated: gaps stay gaps. Intraday power timestamps are in UTC (Coordinated Universal Time, start of "
     "the interval); daily power averages use the Central European calendar day (CET/CEST); market data use exchange "
     "trading dates. The Romanian equities need a free EODHD key in a `.env` file (`EODHD_API_KEY=...`).\n\n"
     "Set `RUN_DOWNLOAD = True` to download everything again (about 15 minutes); by default the notebook reads the files "
     "already published with the course.")
q.code("RUN_DOWNLOAD = False\n"
       "if RUN_DOWNLOAD:\n"
       "    import subprocess, sys\n"
       "    for s in ('download_all.py', 'download_L5.py', 'download_L6.py'):\n"
       "        subprocess.run([sys.executable, s], check=True)   # copies of data/*.py, in this folder")
q.md("## The files of `data/clean` and the period each one covers")
q.code("import pandas as pd\n"
       "FILES = {  # file: (time column, what it holds)\n"
       "    'power_da_prices_hourly_utc.csv': ('timestamp_utc', 'Day-ahead prices RO, BG, HU, DE-LU (EUR/MWh), hourly'),\n"
       "    'power_da_prices_native_utc.csv': ('timestamp_utc', 'Day-ahead prices at native resolution (15 min from Oct 2025)'),\n"
       "    'power_da_prices_daily_cet.csv': ('date_cet', 'Day-ahead prices, daily averages (CET day)'),\n"
       "    'generation_ro_mw_hourly_utc.csv': ('timestamp_utc', 'Romania: generation by source and load (MW), hourly'),\n"
       "    'generation_bg_mw_hourly_utc.csv': ('timestamp_utc', 'Bulgaria: generation by source and load (MW), hourly'),\n"
       "    'generation_hu_mw_native_utc.csv': ('timestamp_utc', 'Hungary: wind, solar and load (MW)'),\n"
       "    'crossborder_ro_mw_hourly_utc.csv': ('timestamp_utc', 'Romania: cross-border physical flows (MW, + = import)'),\n"
       "    'fuels_daily.csv': ('date', 'Brent, WTI, Henry Hub, gasoline, heating oil; EUR/USD'),\n"
       "    'ttf_monthly.csv': ('month', 'TTF natural gas, monthly'),\n"
       "    'eua_daily.csv': ('date', 'EU carbon allowances (EUA), EUR/t'),\n"
       "    'ecb_ron_estr_daily.csv': ('date', 'EUR/RON and euro short-term rate'),\n"
       "    'ro_energy_equities_daily.csv': ('date', 'Hidroelectrica, Nuclearelectrica, OMV Petrom, Romgaz (RON)'),\n"
       "    'opcom_forward_trades.csv': ('auction_date', 'OPCOM forward market trades'),\n"
       "}\n"
       "rows = []\n"
       "for f, (col, what) in FILES.items():\n"
       "    t = pd.read_csv(DATA + f, usecols=[col])[col]\n"
       "    t = pd.to_datetime(t, utc=True, errors='coerce', format='mixed')\n"
       "    rows.append({'file': f, 'content': what, 'first': t.min().date(), 'last': t.max().date(), 'rows': len(t)})\n"
       "COV = pd.DataFrame(rows)\n"
       "pd.set_option('display.max_colwidth', 80)\n"
       "COV")
q.md("## Chart: period covered by each file")
q.code("import matplotlib.pyplot as plt\n"
       "plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False, 'axes.grid': False})\n"
       "fig, ax = plt.subplots(figsize=(9, 4.6))\n"
       "for i, r in COV.iloc[::-1].reset_index(drop=True).iterrows():\n"
       "    ax.barh(i, (pd.Timestamp(r['last']) - pd.Timestamp(r['first'])).days, left=pd.Timestamp(r['first']), height=0.55, color='#1F4E79')\n"
       "ax.set_yticks(range(len(COV))); ax.set_yticklabels(COV['file'].iloc[::-1], fontsize=7)\n"
       "ax.set_xlabel('period covered')\n"
       "fig.patch.set_alpha(0); ax.patch.set_alpha(0)\n"
       "plt.savefig('data_coverage.png', dpi=150, bbox_inches='tight', transparent=True); plt.show()")
q.md("## Loading a series\n\nExample: hourly day-ahead prices of Romania and Bulgaria, in local time.")
q.code("p = pd.read_csv(DATA + 'power_da_prices_hourly_utc.csv', index_col=0, parse_dates=True)\n"
       "p.index = pd.to_datetime(p.index, utc=True).tz_convert('Europe/Bucharest')\n"
       "p[['RO', 'BG']].tail()")
q.write(execute=True)
for s in ("download_all.py", "download_L5.py", "download_L6.py", "SOURCES.md"):
    shutil.copy(os.path.join(HERE, s), os.path.join(q.folder, s))
