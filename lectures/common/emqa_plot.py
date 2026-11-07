"""
emqa_plot.py -- shared chart style and data loaders for all EMQA lectures.

Chart rules (course standard):
  * transparent background, no gridlines, no grey reference lines;
  * legend at the bottom, outside the axes (fig.legend, lower center);
  * one y-axis per panel (never twin axes); fixed colour per entity (PAL);
  * the source + data period is NOT drawn in the PDF: it is stored in the numbers JSON
    (``charts`` section) and printed under the figure by the builder.

Data loaders read repo/data/clean/*.csv (produced by data/download_all.py) with paths
relative to this file, so the code works from any working directory.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "data", "clean")

# Categorical palette (validated adjacent-pair order; same hex in emqa_preamble.tex).
PAL = {
    "RO": "#2a78d6", "DE_LU": "#eb6834", "HU": "#1baf7a", "BG": "#eda100",
    "c5": "#e87ba4", "c6": "#008300", "c7": "#6250d6", "c8": "#e34948",
}
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
INK = "#222222"
ZONE_NAME = {"RO": "Romania (OPCOM PZU)", "BG": "Bulgaria (IBEX)", "HU": "Hungary (HUPX)",
             "DE_LU": "Germany-Luxembourg"}
ZONE_LS = {"RO": "-", "BG": "--", "HU": "-.", "DE_LU": ":"}   # secondary encoding besides colour

SRC_EC = "energy-charts.info (Fraunhofer ISE), from exchange/ENTSO-E data"
SRC_YF = "Yahoo Finance (ICE Brent front-month BZ=F)"
SRC_WB = "World Bank Commodity Price Data (Pink Sheet)"


def style():
    plt.rcParams.update({
        "figure.facecolor": "none", "axes.facecolor": "none", "savefig.transparent": True,
        "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK,
        "text.color": INK, "font.size": 11, "axes.titlesize": 11.5, "axes.labelsize": 11,
        "legend.fontsize": 10.5, "legend.frameon": False, "lines.linewidth": 1.4,
        "font.family": "DejaVu Sans", "pdf.fonttype": 42,
    })


def legend_bottom(fig, handles=None, labels=None, ncol=4, y=0.0):
    """Legend centred under the axes, outside the plotting area."""
    if handles is None:
        handles, labels = [], []
        for ax in fig.axes:
            h, l_ = ax.get_legend_handles_labels()
            for hh, ll in zip(h, l_):
                if ll not in labels:
                    handles.append(hh)
                    labels.append(ll)
    if handles:
        fig.legend(handles, labels, loc="lower center", ncol=ncol, bbox_to_anchor=(0.5, y),
                   frameon=False, handlelength=2.0, columnspacing=1.2)


def save(fig, path, bottom=0.17):
    fig.tight_layout(rect=(0, bottom, 1, 1))
    fig.savefig(path, transparent=True, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- loaders
def _p(name):
    return os.path.join(DATA, name)


def prices_daily():
    """Daily base prices (mean of all MTUs of the CET/CEST day), EUR/MWh."""
    return pd.read_csv(_p("power_da_prices_daily_cet.csv"), parse_dates=["date_cet"]).set_index("date_cet")


def prices_native():
    """Native-resolution day-ahead prices (60-min to Sep 2025, 15-min from 1 Oct 2025), CET/CEST index."""
    x = pd.read_csv(_p("power_da_prices_native_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
    x.index = x.index.tz_convert("Europe/Brussels")
    return x


def prices_hourly():
    """Hourly prices (15-min MTUs averaged to the hour after Oct 2025), CET/CEST index."""
    x = pd.read_csv(_p("power_da_prices_hourly_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
    x.index = x.index.tz_convert("Europe/Brussels")
    return x


def generation_ro_daily():
    return pd.read_csv(_p("generation_ro_mw_daily_cet.csv"), parse_dates=["date_cet"]).set_index("date_cet")


def crossborder_ro_daily():
    return pd.read_csv(_p("crossborder_ro_mw_daily_cet.csv"), parse_dates=["date_cet"]).set_index("date_cet")


def fuels_daily():
    return pd.read_csv(_p("fuels_daily.csv"), parse_dates=["date"]).set_index("date")


def ttf_monthly():
    x = pd.read_csv(_p("ttf_monthly.csv"))
    x.index = pd.PeriodIndex(x["month"], freq="M").to_timestamp()
    return x.drop(columns="month")


def generation_ro_hourly():
    """Romanian generation by source, hourly mean MW, UTC index (interval start)."""
    return pd.read_csv(_p("generation_ro_mw_hourly_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")


def generation_bg_hourly():
    """Bulgarian generation (incl. battery discharge/charging from Sep 2026), hourly mean MW, UTC index."""
    return pd.read_csv(_p("generation_bg_mw_hourly_utc.csv"), parse_dates=["timestamp_utc"]).set_index("timestamp_utc")
