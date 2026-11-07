// Lecture 1 interactive page: energy markets and their data. Inputs in L1_data.js (lectures/L1/build_interactive_L1.py).
(function () {
'use strict';
const D = window.LK_DATA, T = window.LK_TEXT;
const { LANG, C, ZONE, DASH, mean, sdev, median, quantile, nf, pct, $, AX, layout, ttl, plot, out, vline, hline,
  bindSlider, bindSelect, bindToggles, Player, range, safe } = window.EMQAI;
const players = [];
const P = (id, input, vals, ms) => players.push(new Player(id, $(input), vals, ms));

// ---------------------------------------------------------------- 1. merit order on the real OPCOM curves
safe('merit-order', () => {
  // quantity offered (supply) or bid (demand) at price p: points are (price, cumulative quantity) in quantity order
  function qAt(ps, qs, p, sup) {
    let q = 0;
    for (let i = 1; i < ps.length; i++) {
      const p0 = ps[i - 1], p1 = ps[i], q0 = qs[i - 1], q1 = qs[i];
      const inSeg = sup ? p >= Math.min(p0, p1) : p <= Math.max(p0, p1);
      if (!inSeg) break;
      if (p1 === p0) { q = q1; continue; }
      const f = (p - p0) / (p1 - p0);
      q = f >= 0 && f <= 1 ? q0 + f * (q1 - q0) : q1;
    }
    return q;
  }
  // clearing: lowest price with supply >= demand (lo) and highest price with supply <= demand (hi); lo < hi when the curves
  // cross on a vertical segment, and then every price in [lo, hi] clears the same quantity
  function clear(c, dS, dD) {
    const g = p => qAt(c.sp, c.sq, p, true) + dS - (qAt(c.dp, c.dq, p, false) + dD);
    const bis = (ok, a, b) => { for (let k = 0; k < 60; k++) { const m = (a + b) / 2; ok(m) ? (b = m) : (a = m); } return b; };
    const lo = g(-600) >= 0 ? -600 : g(4000) < 0 ? 4000 : bis(p => g(p) >= 0, -600, 4000);
    const hi = g(4000) <= 0 ? 4000 : g(-600) > 0 ? -600 : bis(p => g(p) > 1e-6, -600, 4000);
    const p = hi - lo > 0.05 ? (lo + hi) / 2 : lo;
    return { p, lo, hi: Math.max(lo, hi), q: Math.min(qAt(c.sp, c.sq, p, true) + dS, qAt(c.dp, c.dq, p, false) + dD) };
  }
  const iv = bindSelect('mo-i', draw), s = bindSlider('mo-s', v => nf(v, 0), draw), d = bindSlider('mo-d', v => nf(v, 0), draw);
  // zero-price extra supply: inserted where the supply curve crosses 0 EUR/MWh (shifts all offers at or above 0 to the right)
  function shifted(c, dS) {
    const sp = [], sq = [];
    let done = false;
    for (let i = 0; i < c.sp.length; i++) {
      if (!done && c.sp[i] >= 0) { const q0 = i ? qAt(c.sp, c.sq, 0, true) : 0; sp.push(0, 0); sq.push(q0, q0 + dS); done = true; }
      sp.push(c.sp[i]); sq.push(c.sq[i] + (done ? dS : 0));
    }
    return { sp, sq };
  }
  function draw() {
    const c = D.mo[+iv()], dS = s(), dD = d();
    const base = clear(c, 0, 0);
    const sh = dS ? shifted(c, Math.max(dS, -qAt(c.sp, c.sq, 1e9, true))) : { sp: c.sp, sq: c.sq };
    const cc = Object.assign({}, c, sh);
    const r = clear(cc, 0, dD);
    const clip = p => Math.max(-200, Math.min(1000, p));
    const tr = [
      { x: c.sq.map(q => q / 1000), y: c.sp.map(clip), mode: 'lines', name: T.supply0, line: { color: C.RO, width: 1, dash: 'dot' }, hoverinfo: 'skip', visible: dS ? true : false },
      { x: c.dq.map(q => q / 1000), y: c.dp.map(clip), mode: 'lines', name: T.demand0, line: { color: C.DE_LU, width: 1, dash: 'dot' }, hoverinfo: 'skip', visible: dD ? true : false },
      { x: sh.sq.map(q => q / 1000), y: sh.sp.map(clip), mode: 'lines', name: T.supply, line: { color: C.RO, width: 2.2 } },
      { x: c.dq.map(q => (q + dD) / 1000), y: c.dp.map(clip), mode: 'lines', name: T.demand, line: { color: C.DE_LU, width: 2.2 } },
      { x: [r.q / 1000, r.q / 1000], y: [r.lo, r.hi], mode: 'lines+markers', name: T.clearing, line: { color: C.navy, width: 4 }, marker: { color: C.navy, size: 10 } }
    ];
    plot('mo-chart', tr, layout({ title: ttl($('mo-i').selectedOptions[0].textContent), xaxis: AX(T.qty.replace('MW', 'GW'), { rangemode: 'tozero' }),
      yaxis: AX(T.price, { range: [-200, 1000] }), shapes: [hline(c.p_off, C.grey, 'dash')], margin: { l: 60, r: 12, t: 34, b: 44 } }));
    const pr = r => (r.hi - r.lo > 0.05 ? T.range(nf(r.lo, 2), nf(r.hi, 2)) : nf(r.p, 2));
    out('mo-out', [T.mo(pr(r), nf(r.q, 0), pr(base), nf(base.q, 0), (r.p - base.p >= 0 ? '+' : '') + nf(r.p - base.p, 2)),
      T.mo2((dS >= 0 ? '+' : '') + nf(dS, 0), (dD >= 0 ? '+' : '') + nf(dD, 0), nf(D.mo[0].p_off, 2), nf(D.mo[1].p_off, 2))]);
  }
  draw();
  P('mo-play', 'mo-s', range(0, 1000, 25), 300);
});

// ---------------------------------------------------------------- 2. daily prices of the four zones
safe('daily-prices', () => {
  const t0 = new Date(D.dp.t0 + 'T00:00:00Z'), days = Array.from({ length: D.dp.n }, (_, i) => new Date(t0.getTime() + i * 864e5).toISOString().slice(0, 10));
  const zs = bindToggles('dp-z', draw), w = bindSlider('dp-w', v => v, draw), y0 = bindSlider('dp-y', v => v, draw);
  function ma(a, k) {
    const r = new Array(a.length).fill(null); let s = 0, n = 0; const q = [];
    for (let i = 0; i < a.length; i++) {
      q.push(a[i]); if (a[i] !== null) { s += a[i]; n++; }
      if (q.length > k) { const o = q.shift(); if (o !== null) { s -= o; n--; } }
      r[i] = q.length === k && n >= Math.ceil(0.8 * k) ? s / n : null;
    }
    return r;
  }
  function draw() {
    const k = w(), start = `${y0()}-01-01`, i0 = days.findIndex(x => x >= start), tr = [], lines = [];
    zs().forEach(z => {
      const v = ma(D.dp[z], k).slice(i0), x = days.slice(i0);
      tr.push({ x, y: v, mode: 'lines', name: ZONE[z], line: { color: C[z], width: 1.4, dash: DASH[z] }, connectgaps: false,
        hovertemplate: '%{x}: %{y:.1f} EUR/MWh<extra>' + ZONE[z] + '</extra>' });
      const raw = D.dp[z].slice(i0), ok = raw.map((v2, i) => [v2, x[i]]).filter(a => a[0] !== null);
      if (ok.length) {
        const vals = ok.map(a => a[0]), im = vals.indexOf(Math.max(...vals));
        lines.push(T.dp(ZONE[z], nf(mean(vals), 1), nf(sdev(vals), 1), nf(vals[im], 1), ok[im][1], ok.length));
      }
    });
    plot('dp-chart', tr, layout({ title: ttl(T.dpTitle(k)), xaxis: AX('', { type: 'date' }), yaxis: AX(T.eur, { rangemode: 'tozero' }) }));
    out('dp-out', lines.length ? lines : ['–']);
  }
  draw();
  P('dp-play', 'dp-y', range(2015, 2026, 1), 700);
});

// ---------------------------------------------------------------- 3. intraday profile by zone, year and season
safe('intraday-profile', () => {
  const z = bindSelect('ip-z', draw), s = bindSelect('ip-s', draw), y = bindSlider('ip-y', v => v, draw);
  const H = Array.from({ length: 24 }, (_, i) => i);
  function draw() {
    const zz = z(), ss = s(), yy = y(), tr = [], tn = [];
    const yrs = Object.keys(D.ip[zz]).map(Number);
    // reference year (first available) in grey, chosen year in colour
    const ref = Math.min(...yrs);
    [[ref, C.grey, 'dot'], [yy, C[zz], 'solid']].forEach(([yr, col, dash]) => {
      const p = D.ip[zz][yr]; if (!p) return;
      const v = p[ss], m = mean(v.filter(a => a !== null));
      tr.push({ x: H, y: v, mode: 'lines+markers', name: String(yr), line: { color: col, width: 2, dash }, marker: { size: 4 } });
      tn.push({ x: H, y: v.map(a => a / m), mode: 'lines+markers', name: String(yr), line: { color: col, width: 2, dash }, marker: { size: 4 }, showlegend: false });
    });
    plot('ip-chart', tr, layout({ title: ttl(T.ipTitle), xaxis: AX(T.hour, { dtick: 3 }), yaxis: AX(T.eur) }));
    plot('ip-norm', tn, layout({ title: ttl(T.ipNorm), xaxis: AX(T.hour, { dtick: 3 }), yaxis: AX(''), shapes: [hline(1, C.band, 'dash')] }));
    const p = D.ip[zz][yy];
    if (!p) { out('ip-out', ['–']); return; }
    const v = p[ss], lo = Math.min(...v), hi = Math.max(...v);
    const lines = [T.ip(ZONE[zz], yy, T.season[ss], nf(lo, 1), v.indexOf(lo), nf(hi, 1), v.indexOf(hi), nf(v[19] / v[13], 2))];
    if (yy === +D.end.slice(0, 4)) lines.push(T.partial(yy));
    out('ip-out', lines);
  }
  draw();
  P('ip-play', 'ip-y', range(2016, 2026, 1), 800);
});

// ---------------------------------------------------------------- 4. negative and cheap hours
safe('negative-prices', () => {
  const z = bindSelect('ng-z', draw), t = bindSlider('ng-t', v => nf(v, 0), draw), y = bindSlider('ng-y', v => v, draw);
  function draw() {
    const zz = z(), k = D.ng.thr.indexOf(t()), yy = y(), V = D.ng.v[zz], yrs = Object.keys(V).map(Number);
    const tot = yrs.map(yr => V[yr][k].reduce((a, b) => a + b, 0));
    plot('ng-year', [{ x: yrs, y: tot, type: 'bar', marker: { color: yrs.map(yr => (yr === yy ? C[zz] : C.band)) }, name: ZONE[zz],
      hovertemplate: '%{x}: %{y:.0f}<extra></extra>' }],
    layout({ title: ttl(T.ngYear(nf(t(), 0))), xaxis: AX(T.year, { dtick: 1 }), yaxis: AX(T.hours), showlegend: false }));
    const hv = V[yy] ? V[yy][k] : new Array(24).fill(0);
    plot('ng-hour', [{ x: Array.from({ length: 24 }, (_, i) => i), y: hv, type: 'bar', marker: { color: C[zz] }, hovertemplate: '%{x}:00: %{y:.1f}<extra></extra>' }],
      layout({ title: ttl(T.ngHour(nf(t(), 0), yy)), xaxis: AX(T.hour, { dtick: 3 }), yaxis: AX(T.hours), showlegend: false }));
    const n = hv.reduce((a, b) => a + b, 0);
    const lines = [];
    if (n > 0) {
      const mid = hv.slice(10, 16).reduce((a, b) => a + b, 0);
      lines.push(T.ng(ZONE[zz], nf(t(), 0), yy, n, pct(mid / n, 0), hv.indexOf(Math.max(...hv))));
    } else lines.push(T.ng0(ZONE[zz], nf(t(), 0), yy));
    if (yy === +D.end.slice(0, 4)) lines.push(T.partial(yy));
    out('ng-out', lines);
  }
  draw();
  P('ng-play', 'ng-t', range(-50, 20, 5), 600);
});

// ---------------------------------------------------------------- 5. asinh variance-stabilising transform
safe('asinh', () => {
  const c = bindSlider('as-c', v => nf(v, 1), draw), y = bindSelect('as-y', draw);
  const mom = a => { const m = mean(a), s = sdev(a), n = a.length; let s3 = 0, s4 = 0; a.forEach(x => { const z = (x - m) / s; s3 += z ** 3; s4 += z ** 4; }); return [s3 / n, s4 / n - 3]; };
  function draw() {
    const x = D.as[y()], md = median(x), mad = 1.4826 * median(x.map(v => Math.abs(v - md))), cc = c();
    const tx = x.map(v => Math.asinh((v - md) / (cc * mad)));
    plot('as-raw', [{ x, type: 'histogram', nbinsx: 80, marker: { color: C.RO }, hovertemplate: '%{x}: %{y}<extra></extra>' }],
      layout({ title: ttl(T.asRaw), xaxis: AX(T.eur), yaxis: AX(T.count), showlegend: false, bargap: 0.02 }));
    plot('as-tr', [{ x: tx, type: 'histogram', nbinsx: 80, marker: { color: C.c7 }, hovertemplate: '%{x:.2f}: %{y}<extra></extra>' }],
      layout({ title: ttl(T.asTr), xaxis: AX(''), yaxis: AX(T.count), showlegend: false, bargap: 0.02 }));
    const [s0, k0] = mom(x), [s1, k1] = mom(tx);
    out('as-out', [T.as(y(), x.length, nf(md, 1), nf(mad, 1), nf(s0, 2), nf(k0, 2), nf(s1, 2), nf(k1, 2))]);
  }
  draw();
  P('as-play', 'as-c', range(0.1, 5, 0.1), 250);
});

// ---------------------------------------------------------------- 6. ACF of hourly prices
safe('acf-hourly', () => {
  const z = bindSelect('ac-z', draw), f = bindSelect('ac-f', draw), y = bindSlider('ac-y', v => v, draw), L = bindSlider('ac-L', v => v, draw);
  function draw() {
    const zz = z(), e = D.ac[zz][y()];
    if (!e) { plot('ac-chart', [], layout({})); out('ac-out', ['–']); return; }
    const a = e[f()].slice(0, L()), lags = a.map((_, i) => i + 1), b = 1.96 / Math.sqrt(e.n);
    const col = lags.map(l => (l % 168 === 0 ? C.DE_LU : l % 24 === 0 ? C.c7 : C[zz]));
    plot('ac-chart', [{ x: lags, y: a, type: 'bar', marker: { color: col }, hovertemplate: 'lag %{x}: %{y:.3f}<extra></extra>' }],
      layout({ title: ttl(T.acTitle(ZONE[zz], y())), xaxis: AX(T.lag, { dtick: 24 }), yaxis: AX(T.acf, { range: [Math.min(-0.2, Math.min(...a) - 0.05), 1] }), showlegend: false,
        bargap: 0.1, shapes: [hline(b, C.grey, 'dash'), hline(-b, C.grey, 'dash')] }));
    const full = e[f()];
    out('ac-out', [T.ac(nf(full[0], 3), nf(full[23], 3), nf(full[167], 3), nf(b, 3))]);
  }
  draw();
  P('ac-play', 'ac-y', range(2016, 2026, 1), 800);
});
})();
