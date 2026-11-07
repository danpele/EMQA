"""
download_L6.py -- extra real data for Lecture 6 (renewables, storage, capture prices, batteries).
Does not modify download_all.py. Run from the repository root:  python3 data/download_L6.py

Writes (data/clean/):
  generation_ro_mw_native_utc.csv   Romania, solar / wind / load / residual load / battery, native 15-min mean MW, UTC
  generation_bg_mw_native_utc.csv   Bulgaria, same columns (+ battery_consumption), native 15-min mean MW, UTC
  generation_hu_mw_native_utc.csv   Hungary, solar / wind / load / residual load, native 15-min mean MW, UTC
  installed_capacity_yearly.csv     installed net capacity by type, GW, end of year, RO / BG / HU
Raw API responses are cached gzip-compressed in data/raw/energy_charts (RO, BG: the files of download_all.py are reused;
HU and installed capacity are new files). A section is appended to data/SOURCES.md (replaced on every run).
Source: energy-charts.info (Fraunhofer ISE) API, which re-publishes ENTSO-E Transparency data (actual generation per
type, actual load) and installed capacity. No interpolation, no gap filling: missing intervals stay missing.
"""

import gzip
import json
import os
import time
from datetime import date, timedelta

import pandas as pd
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw", "energy_charts")
CLEAN = os.path.join(HERE, "clean")
EC = "https://api.energy-charts.info"
FIRST_YEAR = 2019
TODAY = date.today()
KEEP = {"Solar": "solar", "Wind onshore": "wind_onshore", "Load": "load", "Residual load": "residual_load",
        "Battery": "battery", "Battery consumption": "battery_consumption"}
KEEP = {k.lower(): v for k, v in KEEP.items()}          # energy-charts spells "Battery Consumption" for BG
os.makedirs(RAW, exist_ok=True)


def fetch(url, params, path):
    """Download once and cache gzip-compressed; a cached file of a past year is never re-downloaded."""
    if os.path.exists(path):
        return json.loads(gzip.open(path).read())
    for k in range(4):
        r = requests.get(url, params=params, timeout=120)
        if r.status_code == 200:
            with gzip.open(path, "wb") as f:
                f.write(r.content)
            time.sleep(2)
            return r.json()
        time.sleep(10 * (k + 1))
    raise RuntimeError(f"{url} {params}: HTTP {r.status_code}")


def year_json(country, y):
    path = os.path.join(RAW, f"public_power_{country}_{y}.json.gz")
    s = (date(y, 1, 1) - timedelta(days=1)).isoformat()          # same windows as download_all.py
    e = min(date(y + 1, 1, 1), TODAY + timedelta(days=1)).isoformat()
    if country in ("ro", "bg") and os.path.exists(path):
        return json.loads(gzip.open(path).read())
    if y == TODAY.year and os.path.exists(path) and country == "hu":
        os.remove(path)                                  # current year: refresh
    return fetch(f"{EC}/public_power", {"country": country, "start": s, "end": e}, path)


def native(country):
    parts = []
    for y in range(FIRST_YEAR, TODAY.year + 1):
        d = year_json(country, y)
        idx = pd.to_datetime(d["unix_seconds"], unit="s", utc=True)
        cols = {}
        for it in d["production_types"]:
            nm = it["name"] if isinstance(it["name"], str) else it["name"][0].get("en", str(it["name"][0]))
            if nm.lower() in KEEP:
                cols[KEEP[nm.lower()]] = pd.Series(it["data"], index=idx, dtype="float64")
        parts.append(pd.DataFrame(cols))
    df = pd.concat(parts)
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df = df[df.index < pd.Timestamp(TODAY, tz="UTC")].dropna(how="all")
    df.index.name = "timestamp_utc"
    # interval length = the most frequent spacing within the UTC day (a gap does not lengthen the intervals around it)
    step = df.index.to_series().diff().dt.total_seconds().div(60)
    day = df.index.floor("D")
    df["mtu_minutes"] = step.groupby(day).transform(lambda v: v.mode().iloc[0] if v.notna().any() else 60).fillna(60).astype(int)
    return df


def installed():
    rows = []
    for c in ("ro", "bg", "hu"):
        path = os.path.join(RAW, f"installed_power_{c}.json.gz")
        if os.path.exists(path):
            os.remove(path)                              # small file, always refreshed
        d = fetch(f"{EC}/installed_power", {"country": c, "time_step": "yearly", "installation_decommission": "false"}, path)
        for it in d["production_types"]:
            nm = it["name"] if isinstance(it["name"], str) else it["name"][0].get("en", str(it["name"][0]))
            for yr, v in zip(d["time"], it["data"]):
                rows.append({"country": c.upper(), "year": int(yr), "type": nm, "gw": v})
    return pd.DataFrame(rows)


def freq(df):
    q = df.index[df["mtu_minutes"] == 15]
    if len(q) == 0:
        return "60-min (as served)"
    if (df["mtu_minutes"] == 60).any():
        return f"60-min to {df.index[df['mtu_minutes'] == 60].max():%Y-%m-%d}, 15-min from {q.min():%Y-%m-%d}"
    return "15-min"


def cov(df, col):
    s = df[col].dropna()
    return f"{s.index.min():%Y-%m-%d} - {s.index.max():%Y-%m-%d}" if len(s) else "none"


if __name__ == "__main__":
    out = {}
    for c in ("ro", "bg", "hu"):
        df = native(c)
        fn = f"generation_{c}_mw_native_utc.csv"
        df.to_csv(os.path.join(CLEAN, fn), float_format="%.2f")
        out[c] = (fn, df)
        print(c, len(df), df.index.min(), df.index.max(), list(df.columns))
    cap = installed()
    cap.to_csv(os.path.join(CLEAN, "installed_capacity_yearly.csv"), index=False)
    print("installed capacity rows", len(cap))

    lines = ["", "<!-- BEGIN L6 -->", "## Lecture 6 additions (`data/download_L6.py`)", "",
             "| Series | Frequency | Coverage obtained | Units | Source | Downloaded | Notes / gaps |", "|---|---|---|---|---|---|---|"]
    for c, name in (("ro", "Romania"), ("bg", "Bulgaria"), ("hu", "Hungary")):
        fn, df = out[c]
        cols = [k for k in df.columns if k != "mtu_minutes"]
        lines.append(f"| {name} generation (solar, wind) + load, native resolution (`{fn}`: {', '.join(cols)}) | {freq(df)} | solar {cov(df, 'solar')} | MW (mean over interval) | {EC}/public_power?country={c} | "
                     f"{TODAY} | ENTSO-E actual generation per type and actual load re-published by energy-charts.info; missing intervals "
                     f"left missing; mtu_minutes = interval length. Battery columns only where reported. |")
    lines.append(f"| Installed net capacity by type, RO / BG / HU (`installed_capacity_yearly.csv`) | yearly (end of year) | "
                 f"{cap['year'].min()} - {cap['year'].max()} | GW | {EC}/installed_power?country=ro&time_step=yearly | {TODAY} | "
                 "energy-charts.info from ENTSO-E installed capacity per production type; solar = AC capacity as published. |")
    lines.append("<!-- END L6 -->")
    sp = os.path.join(HERE, "SOURCES.md")
    txt = open(sp, encoding="utf-8").read()
    if "<!-- BEGIN L6 -->" in txt:
        txt = txt[:txt.index("<!-- BEGIN L6 -->")].rstrip("\n") + "\n" + txt[txt.index("<!-- END L6 -->") + len("<!-- END L6 -->"):].lstrip("\n")
    open(sp, "w", encoding="utf-8").write(txt.rstrip("\n") + "\n" + "\n".join(lines) + "\n")
    print("SOURCES.md updated")
