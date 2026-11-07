// Lecture 2 interactive page: forecasting day-ahead prices. Inputs in L2_data.js (lectures/L2/build_interactive_L2.py).
(function () {
'use strict';
const D = window.LK_DATA, T = window.LK_TEXT;
const { C, SERIES, MONTHS, mean, ncdf, nf, pct, $, AX, layout, ttl, plot, out, hline, bindSlider, bindSelect, bindToggles,
  Player, range, safe, cnt } = window.EMQAI;
const P = (id, input, vals, ms) => new Player(id, $(input), vals, ms);
const A = D.A, ND = A.length;
D.small.forEach(([d, h, v]) => { A[d][h] = v; });   // exact values of the hours with |price| < 5 EUR/MWh

// ---------------------------------------------------------------- forecasts: exported models + window averages + ensemble
const F = Object.assign({}, D.F);
const avgOf = keys => A.map((_, d) => A[d].map((__, h) => mean(keys.map(k => F[k][d][h]))));
F.aw_arx = avgOf(['arx56', 'arx84', 'arx112', 'arx714', 'arx721', 'arx728']);
F.aw_lear = avgOf(['lear364', 'lear546', 'lear728']);
F.ens_all = avgOf(['aw_arx', 'aw_lear', 'gbm', 'mlp']);
const COL = { naive: C.grey, snaive: '#b0b7c3', arx728: C.RO, arx728_single: C.c5, aw_arx: C.c7, lear728: C.HU, aw_lear: C.DE_LU,
  gbm: C.BG, mlp: C.c6, ens_all: C.navy };
const lab = k => T.lab[k] || k;
// mean of a loss over a set of (day, hour) cells
function score(k, loss, cells) {
  let s = 0, n = 0;
  cells((d, h) => { const e = A[d][h] - F[k][d][h]; s += loss === 'sq' ? e * e : Math.abs(e); n++; });
  return loss === 'sq' ? Math.sqrt(s / n) : s / n;
}
const allCells = f => { for (let d = 0; d < ND; d++) for (let h = 0; h < 24; h++) f(d, h); };
// date axes: Plotly writes English month names, so the Romanian page uses numeric dates
const DAX = window.EMQAI.LANG === 'ro' ? { type: 'date', tickformat: '%d.%m.%Y' } : { type: 'date' };
const hh = h => String(h).padStart(2, '0');
const month = d => +D.days[d].slice(5, 7);
const SEAS = { all: null, win: [12, 1, 2], spr: [3, 4, 5], sum: [6, 7, 8], aut: [9, 10, 11] };

// ---------------------------------------------------------------- 1. why MAPE fails near zero prices
safe('mape', () => {
  const x = bindSlider('mp-x', v => nf(v, 0), draw), m = bindSelect('mp-m', draw);
  function draw() {
    const k = m(), thr = x();
    let n = 0, ae = 0, ape = 0, sape = 0, nx = 0;
    const px = [], py = [];
    allCells((d, h) => {
      const a = A[d][h], f = F[k][d][h], e = Math.abs(a - f);
      if (Math.abs(a) < thr) { nx++; return; }
      n++; ae += e; if (a !== 0) ape += e / Math.abs(a); sape += 2 * e / (Math.abs(a) + Math.abs(f) || 1);
      if (a !== 0 && ((d * 24 + h) % 3 === 0 || Math.abs(a) < 5)) { px.push(a); py.push(100 * e / Math.abs(a)); }
    });
    const mae = ae / n, mape = 100 * ape / n, smape = 100 * sape / n;
    plot('mp-chart', [{ x: ['MAE (EUR/MWh)', 'sMAPE (%)', 'MAPE (%)'], y: [mae, smape, mape], type: 'bar', marker: { color: [C.RO, C.HU, C.DE_LU] },
      text: [nf(mae, 1), nf(smape, 1), nf(mape, 0)], textposition: 'outside', hoverinfo: 'skip', cliponaxis: false }],
    layout({ title: ttl(T.mpBar), yaxis: AX('', { type: 'log', range: [0, 4.2] }), showlegend: false }));
    plot('mp-ape', [{ x: px, y: py, mode: 'markers', marker: { color: C.RO, size: 3, opacity: 0.35 }, hoverinfo: 'skip' }],
      layout({ title: ttl(T.mpApe), xaxis: AX(T.absp, { range: [-110, 600] }), yaxis: AX(T.ape, { type: 'log', exponentformat: 'power' }), showlegend: false,
        shapes: thr > 0 ? [{ type: 'rect', xref: 'x', yref: 'paper', x0: -thr, x1: thr, y0: 0, y1: 1, fillcolor: 'rgba(138,148,166,0.18)', line: { width: 0 } }] : [] }));
    out('mp-out', [T.mp(lab(k), nf(thr, 0), cntH(n), nf(mae, 2), nf(mape, 1), nf(smape, 1))].concat(nx ? [T.mp2(cntH(nx))] : []));
  }
  draw();
  P('mp-play', 'mp-x', range(0, 30, 1), 300);
});
function cntH(n) { return window.EMQAI.LANG === 'ro' ? cnt(n, 'oră', 'ore') : cnt(n, 'hour', 'hours'); }

// ---------------------------------------------------------------- 2. Diebold-Mariano test
safe('dm-test', () => {
  const a = bindSelect('dm-a', draw), b = bindSelect('dm-b', draw), l = bindSelect('dm-l', draw), L = bindSlider('dm-L', v => v, draw);
  const nwVar = (x, lags) => {
    const n = x.length, m = mean(x), y = x.map(v => v - m);
    let v = y.reduce((s, z) => s + z * z, 0) / n;
    for (let k = 1; k <= lags; k++) { let c = 0; for (let t = k; t < n; t++) c += y[t] * y[t - k]; v += 2 * (1 - k / (lags + 1)) * c / n; }
    return v;
  };
  function draw() {
    const ka = a(), kb = b(), loss = l(), lags = L();
    const lossF = e => (loss === 'sq' ? e * e : Math.abs(e));
    const la = A.map((r, d) => mean(r.map((v, h) => lossF(v - F[ka][d][h])))), lb = A.map((r, d) => mean(r.map((v, h) => lossF(v - F[kb][d][h]))));
    const dt = la.map((v, i) => v - lb[i]);
    let cum = 0; const cs = dt.map(v => (cum += v));
    plot('dm-diff', [{ x: D.days, y: dt, type: 'bar', marker: { color: dt.map(v => (v > 0 ? C.HU : C.DE_LU)) }, hovertemplate: '%{x}: %{y:.1f}<extra></extra>' }],
      layout({ title: ttl(T.dmDiff), xaxis: AX('', DAX), yaxis: AX(T.dt), showlegend: false, bargap: 0 }));
    plot('dm-cum', [{ x: D.days, y: cs, mode: 'lines', line: { color: C.navy, width: 2 }, hovertemplate: '%{x}: %{y:.0f}<extra></extra>' }],
      layout({ title: ttl(T.dmCum), xaxis: AX('', DAX), yaxis: AX(''), showlegend: false, shapes: [hline(0, C.grey, 'dash')] }));
    if (ka === kb) { out('dm-out', [T.dmSame]); return; }
    const s = mean(dt) / Math.sqrt(nwVar(dt, lags) / dt.length), p = 1 - ncdf(s);
    const d2 = loss === 'sq' ? 0 : 2;
    out('dm-out', [T.dm(lab(ka), lab(kb), nf(mean(la), d2 === 0 ? 0 : 2), nf(mean(lb), d2 === 0 ? 0 : 2), nf(s, 2), p < 0.001 ? '< ' + nf(0.001, 3) : '= ' + nf(p, 3), lags), T.dmV(p)]);
  }
  draw();
  P('dm-play', 'dm-L', range(0, 21, 1), 400);
});

// ---------------------------------------------------------------- 3. error by hour of the day
safe('per-hour', () => {
  const ms = bindToggles('ph-m', draw), q = bindSelect('ph-q', draw), e = bindSelect('ph-e', draw);
  function draw() {
    const S = SEAS[q()], loss = e() === 'rmse' ? 'sq' : 'abs';
    const days = [...Array(ND).keys()].filter(d => !S || S.includes(month(d)));
    const byH = k => Array.from({ length: 24 }, (_, h) => score(k, loss, f => days.forEach(d => f(d, h))));
    const H = Array.from({ length: 24 }, (_, i) => i), tr = [], lines = [], cache = {};
    ms().forEach(k => {
      const v = (cache[k] = byH(k));
      tr.push({ x: H, y: v, mode: 'lines+markers', name: lab(k), line: { color: COL[k], width: 2, dash: k === 'arx728_single' ? 'dash' : 'solid' }, marker: { size: 4 } });
      const tot = score(k, loss, f => days.forEach(d => { for (let h = 0; h < 24; h++) f(d, h); }));
      const w = Math.max(...v), bb = Math.min(...v);
      lines.push(T.ph(lab(k), nf(tot, 2), hh(v.indexOf(w)), nf(w, 2), hh(v.indexOf(bb)), nf(bb, 2)));
    });
    const s1 = cache.arx728_single || byH('arx728_single'), s0 = cache.arx728 || byH('arx728');
    lines.push(T.phCmp(s1.filter((v, h) => v > s0[h]).length));
    plot('ph-chart', tr, layout({ title: ttl(T.phTitle(e())), xaxis: AX(T.hour, { dtick: 2 }), yaxis: AX(T.eur, { rangemode: 'tozero' }) }));
    out('ph-out', lines);
  }
  draw();
});

// ---------------------------------------------------------------- 4. calibration windows and their average
safe('windows', () => {
  const fam = bindSelect('wn-f', draw), ws = bindToggles('wn-w', draw);
  const W = { arx: [56, 84, 112, 714, 721, 728], lear: [364, 546, 728] };
  const maeCache = {};
  const mae = k => (maeCache[k] !== undefined ? maeCache[k] : (maeCache[k] = score(k, 'abs', allCells)));
  function draw() {
    const f = fam(), all = W[f], sel = ws().map(Number).filter(w => all.includes(w));
    const x = all.map(String), y = all.map(w => mae(f + w));
    const tr = [{ x, y, type: 'bar', name: T.win, marker: { color: all.map(w => (sel.includes(w) ? C.RO : C.band)) },
      text: y.map(v => nf(v, 2)), textposition: 'outside', cliponaxis: false, hovertemplate: '%{x}: %{y:.2f}<extra></extra>' }];
    const lines = [];
    if (sel.length) {
      const k = 'avg_' + f + sel.join('_');
      if (!F[k]) F[k] = avgOf(sel.map(w => f + w));
      const m = mae(k), ys = sel.map(w => mae(f + w)), bi = ys.indexOf(Math.min(...ys));
      tr.push({ x: [T.avg], y: [m], type: 'bar', name: T.avg, marker: { color: C.navy }, text: [nf(m, 2)], textposition: 'outside', cliponaxis: false,
        hovertemplate: '%{y:.2f}<extra></extra>' });
      lines.push(T.wn(f, sel.join(', '), nf(m, 2), sel[bi], nf(ys[bi], 2)), T.wnGain(ys[bi] - m, nf(Math.abs(ys[bi] - m), 2)));
    } else lines.push(T.wnNone);
    const lo = Math.min(...y) - 1.5, hi = Math.max(...y) + 0.8;
    plot('wn-chart', tr, layout({ title: ttl(T.wnTitle(f)), xaxis: AX(T.win, { type: 'category' }), yaxis: AX(T.eur, { range: [lo, hi] }), showlegend: false }));
    out('wn-out', lines);
  }
  draw();
});

// ---------------------------------------------------------------- 5. MAE by month
safe('monthly', () => {
  const ms = bindToggles('mm-m', draw), r = bindSelect('mm-r', draw);
  const keys = [...new Set(D.days.map(d => d.slice(0, 7)))];
  const mlab = k => MONTHS[+k.slice(5, 7) - 1] + ' ' + k.slice(2, 4);
  const byM = k => keys.map(mk => score(k, 'abs', f => D.days.forEach((d, i) => { if (d.startsWith(mk)) for (let h = 0; h < 24; h++) f(i, h); })));
  const cache = {};
  const get = k => cache[k] || (cache[k] = byM(k));
  function draw() {
    const rel = r() === 'rel', nv = get('naive'), tr = [], lines = [];
    ms().forEach(k => {
      const v = get(k), y = rel ? v.map((x, i) => x / nv[i]) : v;
      tr.push({ x: keys.map(mlab), y, mode: 'lines+markers', name: lab(k), line: { color: COL[k], width: 2 }, marker: { size: 5 } });
      const tot = score(k, 'abs', allCells), w = Math.max(...v), b = Math.min(...v);
      lines.push(T.mm(lab(k), nf(tot, 2), mlab(keys[v.indexOf(w)]), nf(w, 2), mlab(keys[v.indexOf(b)]), nf(b, 2)));
    });
    plot('mm-chart', tr, layout({ title: ttl(T.mmTitle(r())), xaxis: AX(T.month), yaxis: AX(rel ? T.mmRel : T.eur, rel ? {} : { rangemode: 'tozero' }),
      shapes: rel ? [hline(1, C.grey, 'dash')] : [] }));
    out('mm-out', lines);
  }
  draw();
});

// ---------------------------------------------------------------- 6. QRA intervals: coverage and reliability
safe('qra', () => {
  const c = bindSlider('qr-c', v => T.lvl[v] + '%', draw), w = bindSlider('qr-w', v => D.days[v], draw), hs = bindSelect('qr-h', draw);
  const PAIRS = { 50: [25, 75], 80: [10, 90], 90: [5, 95], 98: [1, 99] };
  const Q = t => D.q.v[D.q.taus.indexOf(t)];
  function draw() {
    const lvl = T.lvl[c()], [tl, tu] = PAIRS[lvl], lo = Q(tl), hi = Q(tu), md = Q(50), h = hs();
    let n = 0, inn = 0, wid = 0;
    for (let d = 0; d < ND; d++) for (let k = 0; k < 24; k++) {
      if (h !== 'all' && +h !== k) continue;
      n++; wid += hi[d][k] - lo[d][k]; if (A[d][k] >= lo[d][k] && A[d][k] <= hi[d][k]) inn++;
    }
    const d0 = w(), xs = [], ya = [], yl = [], yh = [], ym = [];
    let wi = 0;
    for (let d = d0; d < Math.min(d0 + 7, ND); d++) for (let k = 0; k < 24; k++) {
      xs.push(`${D.days[d]} ${String(k).padStart(2, '0')}:00`); ya.push(A[d][k]); yl.push(lo[d][k]); yh.push(hi[d][k]); ym.push(md[d][k]);
      if (A[d][k] >= lo[d][k] && A[d][k] <= hi[d][k]) wi++;
    }
    plot('qr-fan', [
      { x: xs, y: yl, mode: 'lines', line: { width: 0 }, hoverinfo: 'skip', showlegend: false },
      { x: xs, y: yh, mode: 'lines', line: { width: 0 }, fill: 'tonexty', fillcolor: 'rgba(42,120,214,0.22)', name: `${lvl}% QRA`, hoverinfo: 'skip' },
      { x: xs, y: ym, mode: 'lines', line: { color: C.RO, width: 1.4 }, name: T.median },
      { x: xs, y: ya, mode: 'lines', line: { color: C.DE_LU, width: 1.6 }, name: T.actual }
    ], layout({ title: ttl(T.qrFan(D.days[d0], D.days[Math.min(d0 + 6, ND - 1)])), xaxis: AX('', DAX), yaxis: AX(T.eur) }));
    // reliability as in the slide: empirical share of prices below the quantile minus its nominal level, in percentage points
    const taus = D.q.tau_all, dev = D.q.rel[h].map((v, i) => 100 * v - taus[i]);
    plot('qr-rel', [
      { x: taus, y: dev, mode: 'lines+markers', line: { color: C.RO, width: 1.5 }, marker: { size: 3 }, name: 'QRA', hovertemplate: 'τ = %{x}%: %{y:.2f}<extra></extra>' },
      { x: [tl, tu], y: [dev[tl - 1], dev[tu - 1]], mode: 'markers', marker: { color: C.DE_LU, size: 10, symbol: 'diamond' }, showlegend: false, hoverinfo: 'skip' }
    ], layout({ title: ttl(T.qrRel), xaxis: AX(T.nominal, { range: [0, 100] }), yaxis: AX(T.empirical), showlegend: false, shapes: [hline(0, C.grey, 'dash')] }));
    out('qr-out', [T.qr(lvl, h === 'all' ? T.all : `${String(h).padStart(2, '0')}:00`, nf(100 * inn / n, 2), nf(wid / n, 1)), T.qrWeek(nf(100 * wi / xs.length, 1))]);
  }
  draw();
  P('qr-play', 'qr-w', range(0, 358, 7), 600);
});
})();
