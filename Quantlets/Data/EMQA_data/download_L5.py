#!/usr/bin/env python3
"""
download_L5.py -- extra real series for Lecture 5 (energy derivatives and hedging), EMQA.
Uses the cached, idempotent fetch() of download_all.py (same raw cache and manifest); does not modify download_all.py.

Series (all public, no login, no key):
  1. OPCOM PCCB-LE-flex: centralised results of the Romanian forward (bilateral contracts) auctions, May 2020 -> today.
     GET https://www.opcom.ro/rapoarte-pccb-le-flex-rez-pccb-le-flex-export?from=DD/MM/YYYY&to=DD/MM/YYYY&limba=ro
     (the 'Export' button of the public page PCCB-LE-flex > Rezultate). Physical delivery in Romania, prices in lei/MWh.
     Clean file: one row per traded auction session (one closing price per session; quantity = initiator side).
  2. ECB reference rate EUR/RON (to convert lei to EUR on the auction date) and euro short-term rate (EUR STR).
  3. NYMEX Dutch TTF natural gas futures, individual contract months still listed on Yahoo Finance (TTF<M><YY>.NYM),
     daily settlement-type closes, EUR/MWh. Expired contracts are not served by Yahoo (left out, not reconstructed).
  4. World Bank Pink Sheet coal prices (Australian, South African), USD/t, monthly (already in the World Bank raw file).
Writes data/clean/opcom_forward_trades.csv, data/clean/ecb_ron_estr_daily.csv, data/clean/ttf_futures_contracts_daily.csv,
data/clean/coal_monthly.csv and appends a 'Lecture 5 additions' section to data/SOURCES.md.
Usage: python3 data/download_L5.py
"""
import io
import json
import os
import re
import sys
from datetime import date, datetime, timezone

import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import download_all as DA  # noqa: E402  (helpers only; its main() is not run)

CLEAN = DA.CLEAN
TODAY = date.today()
MONTH_CODES = "FGHJKMNQUVXZ"
LOG = []


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------- 1. OPCOM forward auctions
def opcom_forward():
    log("[L5-1] OPCOM PCCB-LE-flex results")
    base = "https://www.opcom.ro/rapoarte-pccb-le-flex-rez-pccb-le-flex-export"
    frames = []
    for y in range(2020, TODAY.year + 1):
        e = min(date(y, 12, 31), TODAY)
        params = {"from": f"01/01/{y}", "to": e.strftime("%d/%m/%Y"), "limba": "ro"}
        b = DA.fetch(base, f"opcom_forward/pccb_le_flex_results_{y}.csv", params=params, period_end=e,
                     public_url=f"{base}?from=01/01/{y}&to={params['to']}&limba=ro")
        if not b:
            DA.FAILURES.append((f"OPCOM PCCB-LE-flex {y}", "download failed"))
            continue
        lines = b.decode("utf-8", errors="replace").splitlines()
        i = next((k for k, l_ in enumerate(lines) if l_.startswith("Data licitatie")), None)
        if i is None:
            continue
        df = pd.read_csv(io.StringIO("\n".join(lines[i:])), skipinitialspace=True)
        df.columns = [c.strip() for c in df.columns]
        frames.append(df)
    d = pd.concat([f for f in frames if len(f)], ignore_index=True)
    d = d[d["Ofertele tranzactionate/ netranzactionate"].astype(str).str.strip() == "tranzactionata"].copy()
    d["Data licitatie"] = pd.to_datetime(d["Data licitatie"])
    rows = []
    for code, g in d.groupby("Cod Sesiune Licitatie"):
        assert g["Pret de inchidere [lei/MWh]"].nunique() == 1, code
        ini = g[g["Tip Oferta"].isin(["initiator", "coinitiator"])]
        side = ini["Sens Oferta"].iloc[0] if len(ini) else g["Sens Oferta"].iloc[0]
        seller = ", ".join(sorted(set(g.loc[g["Sens Oferta"] == "vanzare", "Compania"].str.strip())))
        buyer = ", ".join(sorted(set(g.loc[g["Sens Oferta"] == "cumparare", "Compania"].str.strip())))
        q = g.loc[g["Sens Oferta"] == side, "Cantitate totala atribuita [MWh]"].sum()
        mw = g.loc[g["Sens Oferta"] == side, "Cantitate orara atribuita [MWh/h]"].sum()
        r0 = g.iloc[0]
        rows.append({"auction_date": r0["Data licitatie"].date(), "session": code, "profile": str(r0["Profil"]).strip(),
                     "delivery_start": r0["Data de inceput a livrarii"], "delivery_end": r0["Data de sfarsit a livrarii"],
                     "price_ron_mwh": float(r0["Pret de inchidere [lei/MWh]"]), "mw": float(mw), "mwh": float(q),
                     "initiator_side": "sell" if side == "vanzare" else "buy", "seller": seller, "buyer": buyer})
    out = pd.DataFrame(rows).sort_values(["auction_date", "session"])
    return out


# ---------------------------------------------------------------- 2. ECB EUR/RON and EUR STR
def ecb_series(key, rel):
    url = f"https://data-api.ecb.europa.eu/service/data/{key}"
    b = DA.fetch(url, rel, params={"format": "csvdata", "startPeriod": "2015-01-01"}, period_end=TODAY,
                 public_url=url + "?format=csvdata")
    d = pd.read_csv(io.BytesIO(b))
    return pd.Series(d["OBS_VALUE"].values, index=pd.to_datetime(d["TIME_PERIOD"]), dtype="float64")


# ---------------------------------------------------------------- 3. TTF futures contracts (Yahoo)
def yahoo_contract(tk):
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{tk}"
    p1 = int(datetime(2015, 1, 1, tzinfo=timezone.utc).timestamp())
    p2 = int(datetime.now(timezone.utc).timestamp()) + 86400
    b = DA.fetch(url, f"yahoo/contracts/{tk}.json.gz", params={"period1": p1, "period2": p2, "interval": "1d"},
                 period_end=TODAY, public_url=f"{url}?interval=1d", gz=True, pause=0.5, max_tries=2)
    if not b:
        return None
    try:
        r = json.loads(b)["chart"]["result"][0]
        ts = r.get("timestamp") or []
        if len(ts) < 30:
            return None
        tz = r["meta"].get("exchangeTimezoneName", "UTC")
        idx = pd.to_datetime(ts, unit="s", utc=True).tz_convert(tz).tz_localize(None).normalize()
        s = pd.Series(r["indicators"]["quote"][0]["close"], index=idx, dtype="float64")
        return s[~s.index.duplicated(keep="last")].dropna()
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def ttf_contracts():
    log("[L5-3] NYMEX TTF futures contracts (Yahoo Finance)")
    out = {}
    for y in range(TODAY.year, TODAY.year + 4):
        for i, m in enumerate(MONTH_CODES):
            if date(y, i + 1, 1) < date(TODAY.year, TODAY.month, 1):
                continue
            tk = f"TTF{m}{str(y)[2:]}.NYM"
            s = yahoo_contract(tk)
            if s is not None:
                out[f"{y}-{i + 1:02d}"] = s
                log(f"   {tk}: {len(s)} days {s.index[0].date()} - {s.index[-1].date()}")
    df = pd.DataFrame(out).sort_index()
    df.index.name = "date"
    return df


# ---------------------------------------------------------------- 4. coal (World Bank Pink Sheet, cached raw file)
def coal_monthly():
    p = os.path.join(DA.RAW, "worldbank", "CMO-Historical-Data-Monthly.xlsx")
    x = pd.read_excel(p, sheet_name="Monthly Prices", header=None)
    hdr = x.iloc[4].tolist()
    body = x.iloc[6:, [0, hdr.index("Coal, Australian"), hdr.index("Coal, South African **")]].copy()
    body.columns = ["month", "coal_australia_usd_t", "coal_southafrica_usd_t"]
    body = body[body["month"].astype(str).str.match(r"^\d{4}M\d{2}$")]
    body.index = [f"{m[:4]}-{m[5:]}" for m in body["month"]]
    body = body.drop(columns="month").apply(pd.to_numeric, errors="coerce")
    body = body[body.index >= "2015-01"]
    body.index.name = "month"
    return body


def main():
    fw = opcom_forward()
    ron = ecb_series("EXR/D.RON.EUR.SP00.A", "ecb/EXR_D_RON_EUR.csv").rename("eurron_ecb")
    estr = ecb_series("EST/B.EU000A2X2A25.WT", "ecb/EST_B_EU000A2X2A25_WT.csv").rename("estr_pct")
    rates = pd.concat([ron, estr], axis=1).sort_index()
    rates.index.name = "date"
    DA.write_clean(rates, "ecb_ron_estr_daily.csv", "date")
    # lei -> EUR at the last ECB rate on or before the auction date (past only, no interpolation)
    fx = ron.sort_index()
    ad = pd.to_datetime(fw["auction_date"])
    fw["eurron_ecb"] = fx.reindex(fx.index.union(pd.DatetimeIndex(ad.unique()))).ffill().reindex(ad).values
    fw["price_eur_mwh"] = fw["price_ron_mwh"] / fw["eurron_ecb"]
    fw.to_csv(os.path.join(CLEAN, "opcom_forward_trades.csv"), index=False, float_format="%.4f")
    log(f"   -> clean/opcom_forward_trades.csv  {len(fw)} traded sessions "
        f"{fw['auction_date'].min()} - {fw['auction_date'].max()}")
    tc = ttf_contracts()
    DA.write_clean(tc, "ttf_futures_contracts_daily.csv", "date")
    cm = coal_monthly()
    DA.write_clean(cm, "coal_monthly.csv", "month")
    DA.save_manifest()
    write_sources(fw, rates, tc, cm)


def write_sources(fw, rates, tc, cm):
    p = os.path.join(ROOT, "SOURCES.md")
    txt = open(p, encoding="utf-8").read()
    # remove only our own previous section (up to the next level-2 heading of another lecture, or the end)
    txt = re.sub(r"\n## Lecture 5 additions \(download_L5\.py\).*?(?=\n## (?!#)|\n<!-- |\Z)", "", txt, flags=re.S).rstrip() + "\n"
    first = {c: tc[c].first_valid_index() for c in tc}
    rng = "; ".join(f"{c}: {first[c].date()} - {tc[c].last_valid_index().date()}" for c in tc)
    sec = f"""
## Lecture 5 additions (download_L5.py)

Written by `data/download_L5.py` (re-running it replaces only this section). Downloaded {TODAY}.

| Series | Frequency | Coverage obtained | Units | Source | Notes / gaps |
|---|---|---|---|---|---|
| Romanian forward contracts, OPCOM PCCB-LE-flex auction results (`opcom_forward_trades.csv`) | per auction session | {fw['auction_date'].min()} - {fw['auction_date'].max()}, {len(fw)} traded sessions | lei/MWh; EUR/MWh converted | https://www.opcom.ro/rapoarte-pccb-le-flex-rez-pccb-le-flex-export?from=..&to=..&limba=ro (public 'Export' of PCCB-LE-flex > Rezultate) | One row per traded session (single closing price); quantity = initiator side; profile 'banda LD' = baseload (all hours, Mon-Sun), 'varf' = peak profiles. Physical delivery. EUR = lei / ECB EUR/RON of the auction date (last fixing on or before). |
| ECB EUR/RON reference rate; euro short-term rate EUR STR (`ecb_ron_estr_daily.csv`) | daily (TARGET days) | {rates['eurron_ecb'].first_valid_index().date()} - {rates.index.max().date()} | RON per EUR; % p.a. | https://data-api.ecb.europa.eu/service/data/EXR/D.RON.EUR.SP00.A ; .../EST/B.EU000A2X2A25.WT | EUR STR starts 2019-10-01. |
| NYMEX Dutch TTF natural gas futures, individual contract months (`ttf_futures_contracts_daily.csv`, columns = delivery month) | daily (trading days) | {rng} | EUR/MWh | https://finance.yahoo.com/quote/TTFZ26.NYM (pattern TTF<month code><YY>.NYM) | Only contracts still listed on Yahoo are served; expired contracts are not available and are not reconstructed. |
| Coal, Australian and South African export prices (`coal_monthly.csv`) | monthly | {cm.index.min()} - {cm.dropna(how='all').index.max()} | USD/t | World Bank Pink Sheet (CMO-Historical-Data-Monthly.xlsx, cached by download_all.py) | Reference for the dark spread; Romanian lignite has no market price. |

"""
    with open(p, "w", encoding="utf-8") as f:
        f.write(txt + sec)
    log("   -> SOURCES.md: Lecture 5 section written")


if __name__ == "__main__":
    main()
