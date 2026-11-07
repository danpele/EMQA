"""
emqa_assign.py -- shared helpers for the EMQA assignments (Energy MBA, ASE Bucharest).

What this module does (and only this):
  * personal parameters: ``params(student_id, assignment, role)`` draws YOUR test window and
    settings from a seed computed from your student ID (deterministic, the same every time);
  * data loading: reads the course files in ``repo/data/clean`` and returns tidy tables:
      - ``day_matrix(series)``  -> one row per delivery day (CET), 24 columns h00..h23;
      - ``daily_prices()``      -> daily base prices (CET day) for RO, BG, HU, DE_LU;
      - ``ttf_monthly()``, ``eua_daily()``, ``fuels_daily()``.
It contains NO models and NO solutions.

Information set (gate closure, 12:00 CET on day d-1). A forecast or decision for delivery day d may use
  * all prices up to day d-1 (the d-1 auction cleared on d-2);
  * realised load, wind, solar, hydro and other quantities only up to day d-2 (d-1 is not yet metered);
  * fuel and carbon prices up to the last close before 12:00 on d-1 (in practice the close of d-2).
``leakage_check`` enforces the first two points; ``selection_check`` (Assignment 2) verifies that no choice uses the test window.

Time convention. All prices and volumes are given in CET/CEST (Europe/Brussels) delivery hours,
the time zone of the European day-ahead market coupling (SDAC). Romanian local time (EET/EEST)
is one hour later: CET hour h00 = 01:00-02:00 Romanian time.

Daylight saving time (DST). On the last Sunday of March the CET day has 23 hours, on the last
Sunday of October 25 hours. To keep 24 columns we use the standard convention of the
electricity-price-forecasting literature (e.g. Weron 2014; Lago et al. 2021, epftoolbox):
the missing hour (h02 in March) is the mean of h01 and h03; the doubled hour (h02 in October)
is the mean of its two values. The column ``dst`` flags these days.

15-minute market time unit (MTU). Since delivery day 2025-10-01 the day-ahead market clears
96 quarter-hours per day. ``day_matrix`` uses the hourly file, where each hour after that date is
the arithmetic mean of its four quarter-hours (column ``mtu_minutes`` = 15 in the source file).
Use ``quarter_hours(zone)`` if you need the native 15-minute prices.
"""

import hashlib
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data", "clean"))
TZ = "Europe/Brussels"
HOURS = [f"h{h:02d}" for h in range(24)]

# ----------------------------------------------------------------------------- personalisation
SELECTION_DAYS = 120          # A2: selection (calibration) period, the 120 days just before the test window
ROLES = {
    "B": "Battery-storage operator (merchant BESS on the Romanian day-ahead market)",
    "H": "Hydro producer facing a dry year (reservoir + run-of-river portfolio)",
    "R": "Solar producer (utility-scale PV park, PPA and negative prices)",
    "S": "Supplier / industrial consumer buying on the day-ahead market (PZU)",
}


def normalise_id(student_id):
    """Upper-case, strip spaces; a team is several IDs separated by '+', ',' or ';'."""
    parts = [p.strip().upper().replace(" ", "") for p in str(student_id).replace(",", "+").replace(";", "+").split("+")]
    parts = sorted(p for p in parts if p)
    if not parts:
        raise ValueError("Empty student ID")
    return "+".join(parts)


def seed_of(student_id, assignment):
    key = f"EMQA-2026|A{int(assignment)}|{normalise_id(student_id)}"
    return int(hashlib.sha256(key.encode()).hexdigest(), 16) % (2 ** 32)


def _month_starts(first, last):
    return [d.strftime("%Y-%m-%d") for d in pd.date_range(first, last, freq="MS")]


def _check_days(rng, test_start, k):
    """k distinct days inside the 365-day test window, for hand reconciliation."""
    off = sorted(rng.choice(np.arange(7, 358), size=k, replace=False))
    return [(test_start + pd.Timedelta(days=int(o))).strftime("%Y-%m-%d") for o in off]


def params(student_id, assignment, role=None):
    """Personal parameters of one student (or team) for assignment 1 or 2."""
    rng = np.random.default_rng(seed_of(student_id, assignment))
    sid = normalise_id(student_id)
    if int(assignment) == 1:
        test_start = pd.Timestamp(str(rng.choice(_month_starts("2024-09-01", "2025-11-01"))))
        blocks = {
            "Night (h00-h05 CET)": list(range(0, 6)),
            "Morning ramp (h06-h09 CET)": list(range(6, 10)),
            "Solar hours (h10-h15 CET)": list(range(10, 16)),
            "Evening peak (h17-h20 CET)": list(range(17, 21)),
        }
        block = rng.choice(list(blocks))
        return {
            "student_id": sid,
            "assignment": 1,
            "zone": "RO",
            "test_start": test_start.strftime("%Y-%m-%d"),
            "test_end": (test_start + pd.Timedelta(days=364)).strftime("%Y-%m-%d"),
            "burn_in_days": 112,
            "focus_block_name": str(block),
            "focus_hours": blocks[str(block)],
            "arx_windows": [56, 84, 112, 714, 721, 728],
            "lear_window": int(rng.choice([364, 546, 728])),
            "error_window": int(rng.choice([56, 84, 112])),
            "garch_years": int(rng.choice([3, 4, 5])),
            "check_days": _check_days(rng, test_start, 2),
            "check_hour": int(rng.choice(blocks[str(block)])),
        }
    if int(assignment) == 2:
        if role is None or str(role).upper() not in ROLES:
            raise ValueError(f"Assignment 2 needs role in {list(ROLES)}: {ROLES}")
        role = str(role).upper()
        start = pd.Timestamp(str(rng.choice(_month_starts("2025-01-01", "2025-11-01"))))
        sel_start = start - pd.Timedelta(days=SELECTION_DAYS)
        p = {
            "student_id": sid,
            "assignment": 2,
            "role": role,
            "role_name": ROLES[role],
            "zone": "RO",
            # three chronological periods: (1) estimation = everything before selection_start (rolling calibration windows);
            # (2) selection = the SELECTION_DAYS days before test_start: choose the rule, alpha, w*, K, toll ... here only;
            # (3) test = test_start .. test_end: choices frozen, report results here only
            "selection_start": sel_start.strftime("%Y-%m-%d"),
            "selection_end": (start - pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
            "selection_days": SELECTION_DAYS,
            "test_start": start.strftime("%Y-%m-%d"),
            "test_end": (start + pd.Timedelta(days=364)).strftime("%Y-%m-%d"),
            "burn_in_days": 112,                 # forecast days before selection_start (their errors feed HS/CP intervals)
            "lear_window": int(rng.choice([364, 546, 728])),
            "error_window": int(rng.choice([56, 84, 112])),
            "var_window": 250,
            "alphas": [0.95, 0.99],
            "risk_knob": [0.5, 0.6, 0.7, 0.8, 0.9],
            "check_days": _check_days(rng, start, 3),
        }
        if role == "B":
            p.update(power_mw=1.0, energy_mwh=float(rng.choice([1.0, 2.0])),
                     efficiency_rt=float(rng.choice([0.85, 0.88, 0.90])),
                     degradation_eur_mwh=float(rng.choice([5.0, 10.0])), cycles_per_day=1)
        elif role == "H":
            p.update(fleet_share=float(rng.choice([0.10, 0.20, 0.25])),
                     flex_share=float(rng.choice([0.5, 0.6, 0.7])),
                     pmax_factor=float(rng.choice([1.8, 2.0, 2.2])))
        elif role == "R":
            p.update(pv_mwp=float(rng.choice([50.0, 100.0, 150.0])),
                     ppa_hedge=float(rng.choice([0.5, 0.7])),
                     curtail_threshold_eur=float(rng.choice([0.0, -5.0])))
        elif role == "S":
            p.update(avg_load_mw=float(rng.choice([10.0, 20.0, 50.0])),
                     flex_share=float(rng.choice([0.10, 0.15, 0.20])),
                     max_load_factor=float(rng.choice([1.3, 1.5])))
        return p
    raise ValueError("assignment must be 1 or 2")


# ----------------------------------------------------------------------------- data loading
def _read(name, **kw):
    return pd.read_csv(os.path.join(DATA, name), **kw)


def _to_day_matrix(s):
    """UTC-indexed hourly series -> DataFrame (CET delivery day x h00..h23) + 'dst' flag."""
    s = s.copy()
    s.index = pd.to_datetime(s.index, utc=True).tz_convert(TZ)
    df = pd.DataFrame({"v": s.values, "day": s.index.tz_localize(None).normalize(), "h": s.index.hour})
    df = df.groupby(["day", "h"])["v"].mean()  # 25-hour day: doubled hour averaged
    m = df.unstack("h").reindex(columns=range(24))
    days = m.index
    start = days.tz_localize(TZ)
    end = (days + pd.Timedelta(days=1)).tz_localize(TZ)
    expected = ((end - start) / pd.Timedelta(hours=1)).astype(int)  # 23, 24 or 25
    dst = np.asarray(expected != 24)
    # 23-hour day: missing h02 = mean(h01, h03) (only on DST days)
    for d in days[dst]:
        if pd.isna(m.loc[d, 2]):
            m.loc[d, 2] = 0.5 * (m.loc[d, 1] + m.loc[d, 3])
    # incomplete days (e.g. the last, partly published day) are dropped
    m = m.dropna(how="any")
    dst = pd.Series(dst, index=days).reindex(m.index).values
    m.columns = HOURS
    m["dst"] = dst
    m.index.name = "date"
    return m


def day_matrix(series="RO"):
    """
    One row per CET delivery day, 24 hourly columns.
    series: 'RO','BG','HU','DE_LU'  -> day-ahead price, EUR/MWh
            any column of generation_ro_mw_hourly_utc.csv, e.g. 'load','solar','wind_onshore',
            'hydro_water_reservoir','hydro_run_of_river','nuclear','gas' -> mean MW in the hour
            'res' -> wind_onshore + solar (MW)
    """
    if series in ("RO", "BG", "HU", "DE_LU"):
        p = _read("power_da_prices_hourly_utc.csv", index_col=0)
        return _to_day_matrix(p[series].dropna())
    g = _read("generation_ro_mw_hourly_utc.csv", index_col=0)
    if series == "res":
        s = g["wind_onshore"] + g["solar"]
    else:
        s = g[series]
    return _to_day_matrix(s.dropna())


def quarter_hours(zone="RO"):
    """Native-MTU prices (hourly before 2025-10-01, 15-minute after), index in CET."""
    p = _read("power_da_prices_native_utc.csv", index_col=0)
    s = p[[zone, "mtu_minutes"]].dropna()
    s.index = pd.to_datetime(s.index, utc=True).tz_convert(TZ)
    return s


def daily_prices():
    """Daily base prices (CET day). Days after the last complete hourly day are dropped
    (the last published day can be partial)."""
    d = _read("power_da_prices_daily_cet.csv", index_col=0, parse_dates=True)
    d.index.name = "date"
    return d.loc[: day_matrix("RO").index.max()]


def ttf_monthly():
    t = _read("ttf_monthly.csv")
    t["month"] = pd.PeriodIndex(t["month"], freq="M")
    return t.set_index("month")


def eua_daily():
    e = _read("eua_daily.csv", index_col=0, parse_dates=True)
    e.index.name = "date"
    return e


def fuels_daily():
    f = _read("fuels_daily.csv", index_col=0, parse_dates=True)
    f.index.name = "date"
    return f


def panel(zone="RO", start="2022-01-01"):
    """Prices P, load L and wind+solar R (each: CET day x h00..h23) on one gap-free calendar.
    From 2022 the three matrices have no missing days (checked)."""
    P = day_matrix(zone)[HOURS]
    L = day_matrix("load")[HOURS]
    R = day_matrix("res")[HOURS]
    idx = P.index.intersection(L.index).intersection(R.index)
    idx = idx[idx >= pd.Timestamp(start)]
    full = pd.date_range(idx.min(), idx.max(), freq="D")
    if len(full) != len(idx):
        raise ValueError("calendar gaps in the panel; choose a later start")
    return P.loc[full], L.loc[full], R.loc[full]


def leakage_check(forecast_fn, P, L, R, day):
    """Rule R4 (no look-ahead). forecast_fn(P, L, R, day) must return 24 prices for `day`.

    Information set at gate closure (12:00 CET on day d-1):
      * prices P: every day up to d-1 is known (the d-1 auction cleared on d-2);
      * realised load L and wind+solar R: only up to day d-2 (day d-1 is not yet metered).
    We call forecast_fn twice: with the full data, and with P from day d onwards and L, R from day d-1
    onwards set to NaN. If the two forecasts differ, your function used information not available at gate closure.
    Fit every transformation and model INSIDE forecast_fn, so that the check also covers them."""
    day = pd.Timestamp(day)
    f_full = np.asarray(forecast_fn(P, L, R, day), dtype=float)
    Pc, Lc, Rc = P.copy(), L.copy(), R.copy()
    Pc.loc[Pc.index >= day] = np.nan
    for M in (Lc, Rc):
        M.loc[M.index >= day - pd.Timedelta(days=1)] = np.nan
    f_cut = np.asarray(forecast_fn(Pc, Lc, Rc, day), dtype=float)
    ok = bool(np.all(np.isfinite(f_cut)) and np.allclose(f_full, f_cut, equal_nan=False))
    print("leakage check", day.date(), "PASSED" if ok else
          "FAILED: the forecast uses prices of day d or later, or load/RES of day d-1 or later")
    return ok


def selection_check(select_fn, P, L, R, p):
    """Rule R4b (A2: no selection on the test window). select_fn(P, L, R) must return your frozen choices
    (rule name, alpha, w*, K, toll, ...) as a dict. We call it twice: with the full data and with every value
    from p["test_start"] onwards set to NaN. If the choices differ, your selection used test-period data.
    A diagnostic, not a proof: it only sees the data passed through the arguments, so compute every choice
    inside select_fn from P, L, R (no global copies of test-period data) and return ALL frozen choices."""
    t0 = pd.Timestamp(p["test_start"])
    a = select_fn(P, L, R)
    Pc, Lc, Rc = P.copy(), L.copy(), R.copy()
    for M in (Pc, Lc, Rc):
        M.loc[M.index >= t0] = np.nan
    b = select_fn(Pc, Lc, Rc)

    def same(x, y):
        if isinstance(x, dict) and isinstance(y, dict):
            return x.keys() == y.keys() and all(same(x[k], y[k]) for k in x)
        if isinstance(x, (int, float, np.floating, np.integer)) and isinstance(y, (int, float, np.floating, np.integer)):
            return bool(np.isfinite(y) and np.isclose(x, y))
        return x == y
    ok = same(a, b)
    print("selection check", p["selection_start"], "-", p["selection_end"], "PASSED" if ok else
          "FAILED: a choice depends on data of the test window")
    return ok


def last_complete_day():
    """Last CET day with complete RO prices AND complete RO load/generation."""
    return min(day_matrix("RO").index.max(), day_matrix("load").index.max())


def latest_window(p, n_days=28):
    """MODE = 'latest': replace the personal test window by the last n_days complete days.
    The instructor re-runs every notebook in this mode on data downloaded AFTER the deadline
    (an unseen hold-out). Your code must therefore never hard-code dates."""
    q = dict(p)
    end = last_complete_day()
    q["test_end"] = end.strftime("%Y-%m-%d")
    q["test_start"] = (end - pd.Timedelta(days=n_days - 1)).strftime("%Y-%m-%d")
    if "selection_days" in q:                       # A2: the selection period moves with the test window
        ts = pd.Timestamp(q["test_start"])
        q["selection_start"] = (ts - pd.Timedelta(days=q["selection_days"])).strftime("%Y-%m-%d")
        q["selection_end"] = (ts - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    k = len(p.get("check_days", [1, 1]))
    days = pd.date_range(q["test_start"], q["test_end"], periods=k + 2)[1:-1]
    q["check_days"] = [d.normalize().strftime("%Y-%m-%d") for d in days]
    q["mode"] = "latest"
    return q


def data_version():
    """Record of the data you used: file name, last modified, SHA-256 (first 12 hex), rows.
    Print it at the top of your notebook (reproducibility rule R3)."""
    rows = []
    for f in sorted(os.listdir(DATA)):
        if not f.endswith(".csv"):
            continue
        path = os.path.join(DATA, f)
        with open(path, "rb") as fh:
            h = hashlib.sha256(fh.read()).hexdigest()[:12]
        rows.append({"file": f, "modified": pd.Timestamp(os.path.getmtime(path), unit="s").strftime("%Y-%m-%d %H:%M"),
                     "sha256_12": h})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(params("DEMO-0001", 1))
    print(params("DEMO-0001", 2, "B"))
    m = day_matrix("RO")
    print(m.tail(3).round(1))
