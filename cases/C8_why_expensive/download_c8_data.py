"""
download_c8_data.py -- download and cache the extra market data of Case 8 (run once, from the case folder:
    cd repo/cases/C8_why_expensive && python download_c8_data.py ).

Writes data_c8/ with the raw files, tidy CSVs and download_log.json (URL, HTTP status, date of download).
Sources (all public, no login):
  * Transelectrica, single final imbalance prices ("Preturi finale unice de dezechilibru"), monthly PDF per settlement
    run, page https://www.transelectrica.ro/web/tel/rezultate-decontare-piata-de-echilibrare (Oct 2023 onwards).
    For each delivery month the most recent settlement run is kept (CVMA > corrections > VMA > VM).
  * OPCOM, ROPEX_FM forward-market index (weighted price of all contracts in delivery in month M on the OPCOM
    forward markets PCCB-LE, PCCB-NC, PC-OTC, PCSU, PMC, PCCB-LE-Flex), page https://www.opcom.ro/ropexfm/ro.
  * ECB, monthly average EUR/RON reference rate (for converting lei to EUR).
Attempted, not available without credentials (logged, nothing fabricated):
  * JAO long-term capacity auction results (api.jao.eu requires an API key).
The Eurostat retail prices are downloaded by the notebook itself (data_eurostat/).
"""
import datetime
import hashlib
import html
import json
import os
import re
import urllib.request

import pandas as pd
import pymupdf

OUT = "data_c8"
TODAY = datetime.date.today().isoformat()
UA = {"User-Agent": "Mozilla/5.0 (EMQA teaching case; contact danpele@ase.ro)"}
LOG_P = os.path.join(OUT, "download_log.json")
os.makedirs(os.path.join(OUT, "imbalance_pdf"), exist_ok=True)
LOG = json.load(open(LOG_P)) if os.path.exists(LOG_P) else {}


def get(url, path=None, data=None):
    req = urllib.request.Request(url, headers=UA, data=data)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw, status = r.read(), r.status
    except urllib.error.HTTPError as e:
        raw, status = b"", e.code
    if path and raw:
        open(path, "wb").write(raw)
    return raw, status


def log(key, url, status, note=""):
    LOG[key] = {"url": url, "http_status": status, "downloaded": TODAY, "note": note}
    json.dump(LOG, open(LOG_P, "w"), indent=1, ensure_ascii=False)


# ------------------------------------------------------------------ ECB EUR/RON
u = "https://data-api.ecb.europa.eu/service/data/EXR/M.RON.EUR.SP00.A?format=csvdata&startPeriod=2018-01"
raw, st = get(u, os.path.join(OUT, "ecb_eurron_monthly_raw.csv"))
fx = pd.read_csv(os.path.join(OUT, "ecb_eurron_monthly_raw.csv"))[["TIME_PERIOD", "OBS_VALUE"]]
fx.columns = ["month", "ron_per_eur"]
fx.to_csv(os.path.join(OUT, "ecb_eurron_monthly.csv"), index=False)
log("ecb_eurron_monthly.csv", u, st, "ECB monthly average reference rate, RON per EUR")

# ------------------------------------------------------------------ OPCOM ROPEX_FM
u = "https://www.opcom.ro/ropexfm/ro"
raw, st = get(u, os.path.join(OUT, "opcom_ropexfm_raw.html"))
t = raw.decode("utf-8", "ignore")
body = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", t, flags=re.S))))
rep = re.search(r'name="day"[^>]*value="(\d+)".*?name="month"[^>]*value="(\d+)".*?name="year"[^>]*value="(\d+)"', t, flags=re.S)
report_date = f"{rep.group(3)}-{int(rep.group(2)):02d}-{int(rep.group(1)):02d}" if rep else TODAY
num = lambda s: float(s.replace(".", "").replace(",", "."))
rows = []
for m in re.finditer(r"ROPEX_FM_(\d{4}) ((?:[\d.]+,\d+ ){13})", body + " "):
    vals = [num(v) for v in m.group(2).split()]
    for k, v in enumerate(vals[1:], start=1):
        rows.append({"year": int(m.group(1)), "month": k, "ropex_fm_lei_mwh": v, "annual_lei_mwh": vals[0]})
pr = pd.DataFrame(rows)
vol_part = body[body.find("Cantitate in livrare"):]
vrows = []
for m in re.finditer(r"\b(20\d{2}) ((?:[\d.]+ ){13})", vol_part + " "):
    vals = [num(v) for v in m.group(2).split()]
    for k, v in enumerate(vals[1:], start=1):
        vrows.append({"year": int(m.group(1)), "month": k, "volume_mwh": v})
pr = pr.merge(pd.DataFrame(vrows), on=["year", "month"], how="left")
pr["report_date"] = report_date
pr.to_csv(os.path.join(OUT, "opcom_ropex_fm.csv"), index=False)
log("opcom_ropex_fm.csv", u, st, f"ROPEX_FM monthly index and volume in delivery, lei/MWh, report date {report_date}")
print("ROPEX_FM rows", len(pr), "report date", report_date)

# ------------------------------------------------------------------ Transelectrica imbalance prices
PAGE = "https://www.transelectrica.ro/web/tel/rezultate-decontare-piata-de-echilibrare"
raw, st = get(PAGE, os.path.join(OUT, "transelectrica_settlement_page.html"))
t = raw.decode("utf-8", "ignore")
seg = t[t.find("3.1. Preturi finale unice"):t.find("3.2 Preturi finale pentru deficit")]
LUNI = {"ianuarie": 1, "februarie": 2, "martie": 3, "aprilie": 4, "mai": 5, "iunie": 6, "iulie": 7, "august": 8,
        "septembrie": 9, "octombrie": 10, "noiembrie": 11, "decembrie": 12}
cand = []
for r in re.findall(r"<tr.*?</tr>", seg, flags=re.S):
    cells = [html.unescape(re.sub(r"<[^>]+>|\s+", " ", c)).replace("\xa0", " ").strip() for c in re.findall(r"<td.*?</td>", r, flags=re.S)]
    links = re.findall(r'href="([^"]+)"', r)
    if not links or len(cells) < 3:
        continue
    mm = re.match(r"([A-Za-z ]+?)\s*(\d{4})", cells[0].replace("I unie", "Iunie"))
    dd = re.findall(r"\d+", cells[2])
    if not mm or len(dd) < 3:
        continue
    month = LUNI.get(mm.group(1).strip().lower())
    fin = datetime.date(int(dd[2]), int(dd[1]), int(dd[0]))
    href = links[0] if links[0].startswith("http") else "https://www.transelectrica.ro" + links[0]
    cand.append({"year": int(mm.group(2)), "month": month, "run": cells[1], "finalised": fin, "url": href})
cand = pd.DataFrame(cand)
# keep the most recently finalised settlement run of each delivery month
best = cand.sort_values("finalised").groupby(["year", "month"]).tail(1).sort_values(["year", "month"])
best.to_csv(os.path.join(OUT, "imbalance_files_used.csv"), index=False)
log("transelectrica_settlement_page.html", PAGE, st, f"{len(cand)} price files listed, {len(best)} delivery months")


DATE_RE = r"\d{1,2}[./]\d{1,2}[./]\d{4}"
NUM_RE = r"-?[\d.,]*\d"


def parse_pdf(path):
    """Words with coordinates -> (date, interval, price). The files come in two layouts (days as columns or,
    in rotated pages, days along the other axis) and two decimal conventions; both are detected per file."""
    doc = pymupdf.open(path)
    out = []
    for page in doc:
        W = page.get_text("words")
        cen = lambda w: (0.5 * (w[0] + w[2]), 0.5 * (w[1] + w[3]))
        D = [(cen(w), w[4]) for w in W if re.fullmatch(DATE_RE, w[4])]
        # header dates: the largest group sharing (almost) the same coordinate on one axis
        best_axis, best = None, []
        for ax in (0, 1):
            vals = pd.Series([round(c[1 - ax]) for c, _ in D])
            if vals.empty:
                continue
            mode = vals.mode().iloc[0]
            grp = [(c, d) for c, d in D if abs(c[1 - ax] - mode) <= 3]
            if len(grp) > len(best):
                best_axis, best = ax, grp
        if len(best) < 20:
            continue
        ax = best_axis                        # dates spread along axis ax; intervals along axis 1-ax
        hdr = [w for w in W if w[4].startswith("Interval")]
        hc = cen(hdr[0])[ax] if hdr else min(c[ax] for c, _ in best) - 20
        I = []
        for w in W:
            c = cen(w)
            m = re.fullmatch(r"(?:INT)?(\d{1,3})", w[4])
            if m and abs(c[ax] - hc) < 15 and 1 <= int(m.group(1)) <= 100 and abs(c[1 - ax] - best[0][0][1 - ax]) > 3:
                I.append((c[1 - ax], int(m.group(1))))
        if len(I) < 90:
            continue
        cols = sorted((c[ax], d) for c, d in best)
        colw = (cols[-1][0] - cols[0][0]) / (len(cols) - 1)
        rows = sorted(I)
        rowh = abs(rows[-1][0] - rows[0][0]) / (len(rows) - 1)
        toks = [w[4] for w in W]
        comma_dec = sum(bool(re.fullmatch(r"-?\d+,\d{2}", t_)) for t_ in toks) > sum(bool(re.fullmatch(r"-?[\d,]*\.\d{2}", t_)) for t_ in toks)
        cells = {}
        for w in W:
            if not re.fullmatch(NUM_RE, w[4]) or re.fullmatch(DATE_RE, w[4]):
                continue
            c = cen(w)
            col = min(cols, key=lambda d: abs(d[0] - c[ax])); row = min(rows, key=lambda r: abs(r[0] - c[1 - ax]))
            if abs(col[0] - c[ax]) > 0.45 * colw or abs(row[0] - c[1 - ax]) > 0.45 * rowh:
                continue
            if abs(c[ax] - hc) < 15:          # an interval label, not a price
                continue
            cells.setdefault((col[1], row[1]), []).append((c[1 - ax] if ax == 1 else c[0], w[4]))
        for (d, i), parts in cells.items():
            s = "".join(p_ for _, p_ in sorted(parts))
            s = s.replace(".", "").replace(",", ".") if comma_dec else s.replace(",", "")
            try:
                out.append({"date": pd.to_datetime(d.replace("/", "."), dayfirst=True).date().isoformat(), "interval": i, "price_lei_mwh": float(s)})
            except ValueError:
                pass
    return out


def parse_xlsx(path):
    x = pd.read_excel(path, header=None, engine="openpyxl")
    h = x.index[x[0].astype(str).str.startswith("Interval")][0]
    dates = x.loc[h, 1:]
    out = []
    for r in range(h + 1, len(x)):
        i = x.loc[r, 0]
        if pd.isna(i):
            continue
        for c, d in dates.items():
            v = x.loc[r, c]
            if pd.notna(v) and pd.notna(d):
                out.append({"date": pd.Timestamp(d).date().isoformat(), "interval": int(i), "price_lei_mwh": float(v)})
    return out


allrows = []
for _, b in best.iterrows():
    # cache key = delivery month + hash of the file URL, so a newer settlement revision is never confused with an old file
    uid = hashlib.sha1(b.url.encode()).hexdigest()[:10]
    fn = os.path.join(OUT, "imbalance_pdf", f"imbalance_{b.year}_{b.month:02d}_{uid}.pdf")
    if not os.path.exists(fn):
        raw, st = get(b.url, fn)
        log(os.path.basename(fn), b.url, st, f"run {b.run}, finalised {b.finalised}")
    rows = parse_xlsx(fn) if open(fn, "rb").read(2) == b"PK" else parse_pdf(fn)   # one month is served as .xlsx
    ndays = pd.Period(f"{b.year}-{b.month:02d}").days_in_month
    print(f"{b.year}-{b.month:02d} {b.run:14s} cells {len(rows):5d} / {ndays * 96}")
    for r in rows:
        r["run"] = b.run
    allrows += rows
imb = pd.DataFrame(allrows).sort_values(["date", "interval"])
imb.to_csv(os.path.join(OUT, "imbalance_prices_15min.csv"), index=False)
print("imbalance prices:", len(imb), imb.date.min(), imb.date.max())

# ------------------------------------------------------------------ attempted, not available
u = "https://api.jao.eu/OWSMP/getauctions?corridor=RO-HU&fromdate=2025-01-01"
raw, st = get(u)
log("jao_auctions_RO-HU", u, st, "JAO auction API requires an API key (AUTH_API_KEY header); not downloaded")
u = "https://api.jao.eu/OWSMP/getauctions?corridor=RO-BG&fromdate=2025-01-01"
raw, st = get(u)
log("jao_auctions_RO-BG", u, st, "JAO auction API requires an API key (AUTH_API_KEY header); not downloaded")
print(json.dumps({k: v["http_status"] for k, v in LOG.items() if not k.startswith("imbalance_")}, indent=1))
