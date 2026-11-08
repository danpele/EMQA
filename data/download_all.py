#!/usr/bin/env python3
"""
EMQA real-data layer: download every series used in the course from a public
source, cache the raw responses under data/raw/, and write clean CSVs under
data/clean/.  Also regenerates data/SOURCES.md (coverage actually obtained,
source URL, download date, gaps).

Rules
-----
* Real data only.  No interpolation, no gap filling, no synthetic numbers.
  Missing intervals stay missing; daily aggregates carry a coverage column.
* Idempotent.  Raw files for closed periods are reused; files whose period
  touches the last 10 days are refreshed if older than 20 hours.
  Use  --refresh  to force re-download of everything.
* Secrets (EODHD key) are read from a .env file and never printed.

Time conventions
----------------
* Intraday power data: timestamps in UTC (interval start).
* Daily power aggregates: calendar day in Europe/Brussels (CET/CEST), the
  SDAC market-time convention, for ALL bidding zones (so spreads line up).
* Market data (fuels, carbon, equities): exchange trading date.

Usage:  python data/download_all.py [--refresh]
"""
import gzip
import io
import json
import os
import sys
import time
import zipfile
from datetime import datetime, timedelta, timezone, date

import numpy as np
import pandas as pd
import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "raw")
CLEAN = os.path.join(ROOT, "clean")
MANIFEST = os.path.join(RAW, "_manifest.json")
for d in (RAW, CLEAN):
    os.makedirs(d, exist_ok=True)

REFRESH = "--refresh" in sys.argv
TODAY = date.today()
START_YEAR = 2015
UA = {"User-Agent": "Mozilla/5.0 (EMQA course data script; academic use)"}
LOCAL_TZ = "Europe/Brussels"

ENV_CANDIDATES = [
    os.path.expanduser("~/Documents/2026 MFM/MFM/.env"),
    os.path.join(ROOT, "..", ".env"),
]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def read_secret(name):
    if os.environ.get(name):
        return os.environ[name]
    for f in ENV_CANDIDATES:
        if os.path.exists(f):
            for line in open(f):
                if line.strip().startswith(name + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def load_manifest():
    if os.path.exists(MANIFEST):
        return json.load(open(MANIFEST))
    return {}


MAN = load_manifest()
FAILURES = []  # (series, reason)


def save_manifest():
    with open(MANIFEST, "w") as f:
        json.dump(MAN, f, indent=1, sort_keys=True)


def log(*a):
    print(*a, flush=True)


def fetch(url, rel, params=None, period_end=None, public_url=None, binary=False,
          max_tries=6, pause=0.0, gz=False):
    """Download url -> data/raw/rel (cached). Returns bytes or None.
    `public_url` is what we record (never contains a key)."""
    path = os.path.join(RAW, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fresh_needed = REFRESH
    if os.path.exists(path) and not fresh_needed:
        rec = MAN.get(rel, {})
        recent = period_end is None or (period_end >= TODAY - timedelta(days=10))
        if recent and rec.get("downloaded_utc"):
            age = datetime.now(timezone.utc) - datetime.fromisoformat(rec["downloaded_utc"])
            fresh_needed = age > timedelta(hours=20)
    if os.path.exists(path) and not fresh_needed:
        raw = open(path, "rb").read()
        return gzip.decompress(raw) if gz else raw
    delay = 15
    for attempt in range(max_tries):
        try:
            r = requests.get(url, params=params, headers=UA, timeout=180)
        except requests.RequestException as e:
            log(f"   network error {type(e).__name__}; retry in {delay}s")
            time.sleep(delay); delay *= 2
            continue
        if r.status_code == 429 or r.status_code >= 500:
            log(f"   HTTP {r.status_code}; retry in {delay}s")
            time.sleep(delay); delay = min(delay * 2, 240)
            continue
        if r.status_code != 200:
            log(f"   HTTP {r.status_code} for {public_url or url}")
            return None
        content = r.content
        with open(path, "wb") as f:
            f.write(gzip.compress(content) if gz else content)
        MAN[rel] = {"url": public_url or r.url,
                    "downloaded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        save_manifest()
        if pause:
            time.sleep(pause)
        return content
    return None


def write_clean(df, name, index_label):
    p = os.path.join(CLEAN, name)
    df.to_csv(p, index_label=index_label, float_format="%.4f")
    log(f"   -> clean/{name}  {len(df)} rows")
    return p


def year_ranges(first_year):
    for y in range(first_year, TODAY.year + 1):
        s = date(y, 1, 1) - timedelta(days=1)
        e = min(date(y + 1, 1, 1), TODAY + timedelta(days=1))
        yield y, s, e


# --------------------------------------------------------------------------
# 1. Day-ahead prices (energy-charts.info, Fraunhofer ISE; data from
#    EPEX/ENTSO-E/exchanges).  RO = OPCOM PZU, BG = IBEX, HU = HUPX,
#    DE-LU (from 2018-10-01; DE-AT-LU before).
# --------------------------------------------------------------------------
EC = "https://api.energy-charts.info"
MTU15_START = pd.Timestamp("2025-09-30 22:00", tz="UTC")  # SDAC 15-min MTU go-live (delivery 2025-10-01 CEST)
ZONES = {"RO": ["RO"], "BG": ["BG"], "HU": ["HU"], "DE_LU": ["DE-AT-LU", "DE-LU"]}


def ec_price(bzn, y, s, e):
    rel = f"energy_charts/price_{bzn}_{y}.json.gz"
    b = fetch(f"{EC}/price", rel, params={"bzn": bzn, "start": s.isoformat(), "end": e.isoformat()},
              period_end=e, public_url=f"{EC}/price?bzn={bzn}&start={s}&end={e}", gz=True, pause=2)
    if b is None:
        return None
    try:
        d = json.loads(b)
    except ValueError:
        return None
    if not isinstance(d, dict) or not d.get("unix_seconds"):
        return None
    return pd.Series(d["price"], index=pd.to_datetime(d["unix_seconds"], unit="s", utc=True),
                     dtype="float64")


def build_prices():
    log("[1] Day-ahead prices (energy-charts.info)")
    cols = {}
    for zone, codes in ZONES.items():
        parts, bycode = [], {}
        for code in codes:
            for y, s, e in year_ranges(START_YEAR):
                if code == "DE-AT-LU" and y > 2018:
                    continue
                if code == "DE-LU" and y < 2018:
                    continue
                ser = ec_price(code, y, s, e)
                if ser is None:
                    log(f"   {code} {y}: no data")
                    continue
                parts.append(ser)
                bycode.setdefault(code, []).append(ser)
        if not parts:
            FAILURES.append((f"DA price {zone}", "energy-charts returned no data"))
            continue
        ser = pd.concat(parts)
        ser = ser[~ser.index.duplicated(keep="last")].sort_index()
        if zone == "DE_LU":  # DE-AT-LU only before 2018-10-01 00:00 CEST
            cut = pd.Timestamp("2018-09-30 22:00", tz="UTC")
            old = pd.concat(bycode.get("DE-AT-LU", [ser.iloc[:0]]))
            new = pd.concat(bycode.get("DE-LU", [ser.iloc[:0]]))
            new = new[new.index >= cut]
            ser = pd.concat([old[old.index < cut], new]).sort_index()
            ser = ser[~ser.index.duplicated(keep="last")]
        cols[zone] = ser
    px = pd.DataFrame(cols).sort_index()
    px = px[px.index < pd.Timestamp(TODAY + timedelta(days=2), tz="UTC")]
    px.index.name = "timestamp_utc"
    # native-resolution file (hourly until 2025-09-30, 15-min afterwards)
    px_native = px.copy()
    px_native["mtu_minutes"] = np.where(px.index >= MTU15_START, 15, 60)
    write_clean(px_native, "power_da_prices_native_utc.csv", "timestamp_utc")
    # hourly: hourly products as-is; 15-min products averaged within the hour
    hourly = px.resample("1h").mean()
    hourly = hourly.dropna(how="all", subset=list(cols))
    hourly["mtu_minutes"] = np.where(hourly.index >= MTU15_START, 15, 60)  # 15 => mean of 4 quarter-hours
    write_clean(hourly, "power_da_prices_hourly_utc.csv", "timestamp_utc")
    # daily: CET/CEST calendar day, arithmetic mean of all MTUs (base load)
    loc = px.tz_convert(LOCAL_TZ)
    day = loc.index.tz_localize(None).normalize()
    g = loc.groupby(day)
    daily = g.mean()
    for z in cols:
        daily[f"{z}_n_obs"] = g[z].count()
        daily[f"{z}_n_negative"] = g[z].apply(lambda s: int((s < 0).sum()))
    daily.index.name = "date_cet"
    write_clean(daily, "power_da_prices_daily_cet.csv", "date_cet")
    return px


# --------------------------------------------------------------------------
# 2. Generation by source + load (energy-charts public_power; source ENTSO-E
#    transparency platform for RO/BG), 3. cross-border physical flows (cbet)
# --------------------------------------------------------------------------
def ec_table(endpoint, country, y, s, e):
    rel = f"energy_charts/{endpoint}_{country}_{y}.json.gz"
    b = fetch(f"{EC}/{endpoint}", rel,
              params={"country": country, "start": s.isoformat(), "end": e.isoformat()},
              period_end=e, public_url=f"{EC}/{endpoint}?country={country}&start={s}&end={e}",
              gz=True, pause=2)
    if b is None:
        return None
    d = json.loads(b)
    if not isinstance(d, dict) or not d.get("unix_seconds"):
        return None
    idx = pd.to_datetime(d["unix_seconds"], unit="s", utc=True)
    key = "production_types" if endpoint == "public_power" else "countries"
    out = {}
    for item in d[key]:
        name = item["name"]
        if isinstance(name, list):
            name = name[0].get("en", str(name[0]))
        out[name] = pd.Series(item["data"], index=idx, dtype="float64")
    return pd.DataFrame(out)


def slug(s):
    return (s.lower().replace("fossil ", "").replace(" / ", "_").replace(" ", "_")
            .replace("-", "_"))


def build_table(endpoint, country, fname_prefix, first_year=START_YEAR):
    parts = []
    for y, s, e in year_ranges(first_year):
        t = ec_table(endpoint, country, y, s, e)
        if t is None:
            log(f"   {endpoint} {country} {y}: no data")
            continue
        parts.append(t)
    if not parts:
        FAILURES.append((f"{endpoint} {country}", "energy-charts returned no data"))
        return None
    df = pd.concat(parts)
    df = df[~df.index.duplicated(keep="last")].sort_index()
    df = df[df.index < pd.Timestamp(TODAY + timedelta(days=1), tz="UTC")]
    df.columns = [slug(c) for c in df.columns]
    if endpoint == "cbet":  # energy-charts serves cross-border flows in GW -> convert to MW
        df = df * 1000.0
    df = df.dropna(how="all")
    df.index.name = "timestamp_utc"
    hourly = df.resample("1h").mean().dropna(how="all")
    write_clean(hourly, f"{fname_prefix}_hourly_utc.csv", "timestamp_utc")
    loc = df.tz_convert(LOCAL_TZ)
    day = loc.index.tz_localize(None).normalize()
    g = loc.groupby(day)
    daily = g.mean()
    # coverage: share of intervals with a non-missing load (or first column)
    ref = "load" if "load" in df.columns else df.columns[0]
    daily["coverage_" + ref] = g[ref].count() / g[ref].size()
    daily.index.name = "date_cet"
    write_clean(daily, f"{fname_prefix}_daily_cet.csv", "date_cet")
    return df


def build_generation():
    log("[2] Generation mix + load RO, BG (energy-charts public_power)")
    build_table("public_power", "ro", "generation_ro_mw")
    build_table("public_power", "bg", "generation_bg_mw")
    log("[3] Cross-border physical flows RO (energy-charts cbet)")
    build_table("cbet", "ro", "crossborder_ro_mw")


# --------------------------------------------------------------------------
# 4. Fuels (Yahoo Finance continuous front-month futures), FX (ECB)
# --------------------------------------------------------------------------
YAHOO = {
    "brent_usd_bbl": "BZ=F", "wti_usd_bbl": "CL=F", "henryhub_usd_mmbtu": "NG=F",
    "rbob_usd_gal": "RB=F", "heatingoil_usd_gal": "HO=F",
    "ttf_eur_mwh": "TTF=F", "eua_etc_co2l_eur": "CO2.L",
}


def yahoo_chart(ticker):
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{requests.utils.quote(ticker)}"
    p1 = int(datetime(START_YEAR, 1, 1, tzinfo=timezone.utc).timestamp())
    p2 = int(datetime.now(timezone.utc).timestamp()) + 86400
    rel = f"yahoo/{ticker.replace('=', '_')}.json.gz"
    b = fetch(url, rel, params={"period1": p1, "period2": p2, "interval": "1d",
                                "events": "history", "includeAdjustedClose": "true"},
              period_end=TODAY, public_url=f"{url}?interval=1d&period1={p1}", gz=True, pause=1)
    if b is None:
        return None
    try:
        r = json.loads(b)["chart"]["result"][0]
        ts = r.get("timestamp") or []
        q = r["indicators"]["quote"][0]
        if len(ts) < 30 or "close" not in q:
            return None
        tz = r["meta"].get("exchangeTimezoneName", "UTC")
        idx = pd.to_datetime(ts, unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
        s = pd.Series(q["close"], index=idx, dtype="float64")
        return s[~s.index.duplicated(keep="last")].dropna()
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def ecb_fx():
    url = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A"
    b = fetch(url, "ecb/EXR_D_USD_EUR.csv", params={"format": "csvdata", "startPeriod": f"{START_YEAR}-01-01"},
              period_end=TODAY, public_url=url + "?format=csvdata")
    if b is None:
        FAILURES.append(("EUR/USD ECB", "download failed"))
        return None
    d = pd.read_csv(io.BytesIO(b))
    s = pd.Series(d["OBS_VALUE"].values, index=pd.to_datetime(d["TIME_PERIOD"]), dtype="float64")
    return s.rename("eurusd_ecb")


def build_fuels():
    log("[4] Fuels & carbon (Yahoo Finance, ECB FX)")
    out = {}
    for col, t in YAHOO.items():
        s = yahoo_chart(t)
        if s is None:
            FAILURES.append((f"{col} ({t})", "Yahoo returned no/too-short history"))
            log(f"   {t}: no usable history")
            continue
        out[col] = s
    fx = ecb_fx()
    if fx is not None:
        out["eurusd_ecb"] = fx
    eua_proxy = out.pop("eua_etc_co2l_eur", None)
    ttf = out.pop("ttf_eur_mwh", None)
    df = pd.DataFrame(out).sort_index()
    df.index.name = "date"
    write_clean(df, "fuels_daily.csv", "date")
    return df, eua_proxy, ttf, fx


# --------------------------------------------------------------------------
# TTF monthly (World Bank Pink Sheet, "Natural gas, Europe" = TTF), converted
# --------------------------------------------------------------------------
WB_PAGE = "https://www.worldbank.org/en/research/commodity-markets"
MMBTU_PER_MWH = 3.412142


def build_ttf_monthly(fx, ttf_daily):
    log("[4b] TTF monthly (World Bank CMO Pink Sheet)")
    page = fetch(WB_PAGE, "worldbank/commodity-markets.html", period_end=TODAY)
    import re
    link = None
    if page:
        m = re.findall(rb'https?://[^"]*CMO-Historical-Data-Monthly\.xlsx', page)
        link = m[0].decode() if m else None
    if not link:
        FAILURES.append(("TTF monthly (World Bank)", "link to CMO-Historical-Data-Monthly.xlsx not found"))
        return
    b = fetch(link, "worldbank/CMO-Historical-Data-Monthly.xlsx", period_end=TODAY)
    x = pd.read_excel(io.BytesIO(b), sheet_name="Monthly Prices", header=None)
    hdr = x.iloc[4].tolist()
    col = hdr.index("Natural gas, Europe")
    hh = hdr.index("Natural gas, US")
    brent = hdr.index("Crude oil, Brent")
    body = x.iloc[6:, [0, col, hh, brent]].copy()
    body.columns = ["month", "ttf_usd_mmbtu", "henryhub_usd_mmbtu", "brent_usd_bbl"]
    body = body[body["month"].astype(str).str.match(r"^\d{4}M\d{2}$")]
    body.index = pd.PeriodIndex([f"{m[:4]}-{m[5:]}" for m in body["month"]], freq="M")
    body = body.drop(columns="month").apply(pd.to_numeric, errors="coerce")
    body = body[body.index.year >= START_YEAR]
    if fx is not None:
        fxm = fx.groupby(fx.index.to_period("M")).mean()
        body["eurusd_ecb_monthly_avg"] = fxm.reindex(body.index)
        body["ttf_eur_mwh"] = body["ttf_usd_mmbtu"] * MMBTU_PER_MWH / body["eurusd_ecb_monthly_avg"]
    if ttf_daily is not None:
        body["ttf_yahoo_daily_mean_eur_mwh"] = ttf_daily.groupby(ttf_daily.index.to_period("M")).mean().reindex(body.index)
    body.index = body.index.astype(str)
    body.index.name = "month"
    write_clean(body, "ttf_monthly.csv", "month")


# --------------------------------------------------------------------------
# EUA: EEX primary auction clearing prices (EUR/tCO2)  + daily ETC proxy
# --------------------------------------------------------------------------
EEX_ZIP = ("https://www.eex.com/fileadmin/EEX/Downloads/Markets/Environmentals/"
           "EUA_Emission_Spot_Primary_Market_Auction_Report/Archive_Reports/"
           "emission-spot-primary-market-auction-report-2012-2025-data.zip")


def build_eua(eua_proxy):
    log("[4c] EUA: EEX primary auctions + SparkChange EUA ETC (CO2.L) proxy")
    b = fetch(EEX_ZIP, "eex/emission-spot-primary-market-auction-report-2012-2025-data.zip",
              period_end=date(2025, 12, 31))
    rows = []
    if b is None:
        FAILURES.append(("EUA EEX auctions", "archive zip download failed"))
    else:
        z = zipfile.ZipFile(io.BytesIO(b))
        for n in sorted(z.namelist()):
            if not n.endswith((".xls", ".xlsx")):
                continue
            yr = int(n.split("report-")[-1][:4])
            if yr < START_YEAR:
                continue
            x = pd.read_excel(io.BytesIO(z.read(n)), header=None)
            hrow = next(i for i in range(15) if any(str(v).strip() == "Date" for v in x.iloc[i]))
            hdr = [str(v).strip() for v in x.iloc[hrow]]
            x = x.iloc[hrow + 1:]
            x.columns = hdr
            pc = next(c for c in hdr if c.startswith("Auction Price"))
            vc = next(c for c in hdr if c.startswith("Auction Volume"))
            t = pd.DataFrame({"date": pd.to_datetime(x["Date"], errors="coerce"),
                              "auction": x["Auction Name"].astype(str),
                              "contract": x["Contract"].astype(str),
                              "price": pd.to_numeric(x[pc], errors="coerce"),
                              "volume": pd.to_numeric(x[vc], errors="coerce")})
            t = t.dropna(subset=["date", "price"])
            # EUA only (drop aviation EUAA auctions)
            t = t[~t["auction"].str.contains("EUAA|Aviation", case=False) &
                  ~t["contract"].str.contains("EUAA|AV", case=False)]
            rows.append(t)
    eua = pd.DataFrame()
    if rows:
        a = pd.concat(rows)
        a["pv"] = a["price"] * a["volume"]
        g = a.groupby("date")
        eua = pd.DataFrame({"eua_eex_auction_eur_t": g["pv"].sum() / g["volume"].sum(),
                            "eex_n_auctions": g.size()})
    if eua_proxy is not None:
        eua = eua.join(eua_proxy.rename("eua_etc_co2l_eur_per_unit"), how="outer")
    eua.index.name = "date"
    write_clean(eua, "eua_daily.csv", "date")


# --------------------------------------------------------------------------
# 6. Romanian energy equities (EODHD, Bucharest Stock Exchange), RON
# --------------------------------------------------------------------------
EQUITIES = {"H2O": "H2O.RO", "SNN": "SNN.RO", "SNP": "SNP.RO", "SNG": "SNG.RO"}


def build_equities():
    log("[6] Romanian energy equities (EODHD)")
    key = read_secret("EODHD_API_KEY")
    if not key:
        FAILURES.append(("RO equities", "no EODHD_API_KEY found"))
        return
    frames = {}
    for name, t in EQUITIES.items():
        url = f"https://eodhd.com/api/eod/{t}"
        b = fetch(url, f"eodhd/{t}.json", params={"api_token": key, "fmt": "json",
                                                  "from": f"{START_YEAR}-01-01"},
                  period_end=TODAY, public_url=url + f"?fmt=json&from={START_YEAR}-01-01")
        if b is None:
            FAILURES.append((t, "EODHD download failed"))
            continue
        d = pd.DataFrame(json.loads(b))
        if d.empty:
            FAILURES.append((t, "EODHD empty"))
            continue
        d.index = pd.to_datetime(d["date"])
        frames[f"{name}_close_ron"] = d["close"].astype(float)
        frames[f"{name}_adjclose_ron"] = d["adjusted_close"].astype(float)
        frames[f"{name}_volume"] = d["volume"].astype(float)
    df = pd.DataFrame(frames).sort_index()
    df.index.name = "date"
    write_clean(df, "ro_energy_equities_daily.csv", "date")


# --------------------------------------------------------------------------
# 5 / 7. Sources that need credentials we do not have
# --------------------------------------------------------------------------
def check_keyed_sources():
    log("[5/7] Keyed sources (ENTSO-E, AGSI+), EEX futures")
    if not read_secret("ENTSOE_API_KEY") and not read_secret("ENTSOE_TOKEN"):
        FAILURES.append(("ENTSO-E Transparency", "no security token available; energy-charts used instead"))
    if not read_secret("AGSI_API_KEY") and not read_secret("GIE_API_KEY"):
        FAILURES.append(("AGSI+ gas storage", "API requires free key (x-key); none available - not downloaded"))
    FAILURES.append(("EEX German power futures (Cal front year)", "no free public API/series; not downloaded"))


# --------------------------------------------------------------------------
# SOURCES.md
# --------------------------------------------------------------------------
REGISTRY = [
    # file, column(s), name, freq, units, url, notes
    ("power_da_prices_native_utc.csv", ["RO"], "Day-ahead price Romania (OPCOM PZU)", "hourly; 15-min from 2025-10-01", "EUR/MWh",
     f"{EC}/price?bzn=RO", "energy-charts.info (Fraunhofer ISE) re-publication of exchange/ENTSO-E data. SDAC 15-min MTU from delivery 2025-10-01. Missing CET days (left missing): 2015-09-21, 2015-12-20/21, 2017-12-31, 2018-08-17."),
    ("power_da_prices_native_utc.csv", ["BG"], "Day-ahead price Bulgaria (IBEX)", "hourly; 15-min from 2025-10-01", "EUR/MWh",
     f"{EC}/price?bzn=BG", "IBEX DAM started 2016-01-19 but energy-charts serves BG only from 2016-10-31; 15 further missing days in Nov-Dec 2016 (left missing)."),
    ("power_da_prices_native_utc.csv", ["HU"], "Day-ahead price Hungary (HUPX)", "hourly; 15-min from 2025-10-01", "EUR/MWh",
     f"{EC}/price?bzn=HU", ""),
    ("power_da_prices_native_utc.csv", ["DE_LU"], "Day-ahead price Germany-Luxembourg (EPEX)", "hourly; 15-min from 2025-10-01", "EUR/MWh",
     f"{EC}/price?bzn=DE-LU (DE-AT-LU before 2018-10-01)", "Spliced: DE-AT-LU zone until 2018-09-30, DE-LU from 2018-10-01."),
    ("power_da_prices_daily_cet.csv", ["RO", "BG", "HU", "DE_LU"], "Day-ahead daily base price RO/BG/HU/DE-LU", "daily (CET day)", "EUR/MWh",
     f"{EC}/price", "Arithmetic mean of all MTUs of the CET/CEST calendar day; *_n_obs = MTUs present, *_n_negative = MTUs < 0."),
    ("generation_ro_mw_daily_cet.csv", ["nuclear", "hydro_run_of_river", "hydro_water_reservoir", "brown_coal_lignite", "hard_coal", "gas", "wind_onshore", "solar", "load"],
     "Romania net generation by source + load", "hourly (UTC) & daily (CET), mean MW", "MW (mean)",
     f"{EC}/public_power?country=ro", "energy-charts from ENTSO-E actual generation per type; missing intervals left missing; coverage_load column."),
    ("generation_bg_mw_daily_cet.csv", ["nuclear", "load"], "Bulgaria net generation by source + load", "hourly (UTC) & daily (CET), mean MW", "MW (mean)",
     f"{EC}/public_power?country=bg", "as for RO"),
    ("crossborder_ro_mw_daily_cet.csv", ["sum"], "Romania cross-border physical flows by neighbour", "hourly (UTC) & daily (CET), mean MW", "MW (mean)",
     f"{EC}/cbet?country=ro", "Physical flows per border, served by energy-charts in GW, converted x1000 to MW. Sign: positive = net IMPORT into RO (verified: daily corr 0.98 with load minus generation). Moldova/Ukraine borders only partly reported."),
    ("fuels_daily.csv", ["brent_usd_bbl"], "Brent crude front-month (BZ=F)", "daily (trading days)", "USD/bbl",
     "https://finance.yahoo.com/quote/BZ=F", "Continuous front-month (roll-affected)."),
    ("fuels_daily.csv", ["wti_usd_bbl"], "WTI crude front-month (CL=F)", "daily", "USD/bbl",
     "https://finance.yahoo.com/quote/CL=F", "Includes the real negative settle of 2020-04-20."),
    ("fuels_daily.csv", ["henryhub_usd_mmbtu"], "Henry Hub natural gas front-month (NG=F)", "daily", "USD/MMBtu",
     "https://finance.yahoo.com/quote/NG=F", ""),
    ("fuels_daily.csv", ["rbob_usd_gal"], "RBOB gasoline front-month (RB=F)", "daily", "USD/gal",
     "https://finance.yahoo.com/quote/RB=F", ""),
    ("fuels_daily.csv", ["heatingoil_usd_gal"], "NY Harbor ULSD/heating oil front-month (HO=F)", "daily", "USD/gal",
     "https://finance.yahoo.com/quote/HO=F", ""),
    ("fuels_daily.csv", ["eurusd_ecb"], "EUR/USD ECB reference rate", "daily (TARGET days)", "USD per EUR",
     "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A", "Used for USD->EUR conversions."),
    ("ttf_monthly.csv", ["ttf_usd_mmbtu", "ttf_eur_mwh"], "Dutch TTF natural gas, monthly average (World Bank 'Natural gas, Europe')", "monthly", "USD/MMBtu; EUR/MWh (converted)",
     "https://www.worldbank.org/en/research/commodity-markets (CMO-Historical-Data-Monthly.xlsx)",
     "Daily TTF not available free: Yahoo TTF=F now serves only the latest quote. EUR/MWh = USD/MMBtu x 3.412142 / ECB monthly-average EUR/USD (conversion, not a market quote)."),
    ("eua_daily.csv", ["eua_eex_auction_eur_t"], "EU ETS allowance (EUA) - EEX primary auction clearing price", "auction days (~3-4/week)", "EUR/tCO2",
     EEX_ZIP, "Volume-weighted if >1 auction per day; EUAA (aviation) excluded. 2026 file not published as static download -> ends 2025-12."),
    ("eua_daily.csv", ["eua_etc_co2l_eur_per_unit"], "SparkChange Physical Carbon EUA ETC (LSE: CO2), proxy", "daily", "EUR per ETC unit (~1 EUA less fees)",
     "https://finance.yahoo.com/quote/CO2.L", "Physically-backed ETC; tracks EUA spot less fees. Proxy only, covers 2026."),
    ("ro_energy_equities_daily.csv", ["H2O_close_ron"], "Hidroelectrica (BVB: H2O)", "daily", "RON",
     "https://eodhd.com/api/eod/H2O.RO", "Listed 2023-07-12. close and dividend/split-adjusted close."),
    ("ro_energy_equities_daily.csv", ["SNN_close_ron"], "Nuclearelectrica (BVB: SNN)", "daily", "RON", "https://eodhd.com/api/eod/SNN.RO", ""),
    ("ro_energy_equities_daily.csv", ["SNP_close_ron"], "OMV Petrom (BVB: SNP)", "daily", "RON", "https://eodhd.com/api/eod/SNP.RO", ""),
    ("ro_energy_equities_daily.csv", ["SNG_close_ron"], "Romgaz (BVB: SNG)", "daily", "RON", "https://eodhd.com/api/eod/SNG.RO", "Check split history (adjclose)."),
]


def coverage(file, cols):
    p = os.path.join(CLEAN, file)
    if not os.path.exists(p):
        return "NOT OBTAINED", ""
    df = pd.read_csv(p, index_col=0)
    out = []
    for c in cols:
        if c not in df.columns:
            out.append(f"{c}: missing")
            continue
        s = df[c].dropna()
        if s.empty:
            out.append(f"{c}: empty")
            continue
        out.append(f"{str(s.index[0])[:10]} - {str(s.index[-1])[:10]}")
    uniq = sorted(set(out))
    return ("; ".join(uniq) if len(uniq) > 1 else uniq[0]), len(df)


def last_download(prefix):
    ds = [v["downloaded_utc"][:10] for k, v in MAN.items() if k.startswith(prefix)]
    return max(ds) if ds else ""


PREFIX = {"power": "energy_charts/price", "generation_ro": "energy_charts/public_power_ro",
          "generation_bg": "energy_charts/public_power_bg", "crossborder": "energy_charts/cbet",
          "fuels": "yahoo", "ttf": "worldbank", "eua": "eex", "ro_energy": "eodhd"}


def write_sources():
    lines = ["# EMQA data sources", "",
             "Generated by `download_all.py` - do not edit by hand. All series downloaded by script from the public source given; "
             "no interpolation or gap filling. Intraday power timestamps are UTC (interval start); daily power aggregates use the "
             "CET/CEST (Europe/Brussels) calendar day for every zone; market data use exchange trading dates.", "",
             "| Series | Frequency | Coverage obtained | Units | Source | Downloaded | Notes / gaps |",
             "|---|---|---|---|---|---|---|"]
    for file, cols, name, freq, unit, url, notes in REGISTRY:
        cov, n = coverage(file, cols)
        pre = next((v for k, v in PREFIX.items() if file.startswith(k)), "")
        dl = last_download(pre)
        if file.startswith("fuels") and cols == ["eurusd_ecb"]:
            dl = last_download("ecb")
        lines.append(f"| {name} (`{file}`: {', '.join(cols)}) | {freq} | {cov} | {unit} | {url} | {dl} | {notes} |")
    lines += ["", "Licence note: energy-charts.info price data are for private/internal (teaching) use; "
              "generation data CC BY 4.0. Yahoo/EODHD data are for personal/educational use.", ""]
    open(os.path.join(ROOT, "SOURCES.md"), "w").write("\n".join(lines))
    log("   -> SOURCES.md")


if __name__ == "__main__":
    build_prices()
    build_generation()
    fuels, eua_proxy, ttf, fx = build_fuels()
    build_ttf_monthly(fx, ttf)
    build_eua(eua_proxy)
    build_equities()
    check_keyed_sources()
    write_sources()
    if FAILURES:
        log("Not obtained:")
        for s, r in FAILURES:
            log(f"   - {s}: {r}")
