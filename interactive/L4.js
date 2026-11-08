// Lecture 4 interactive page: risk for energy companies (VaR, ES, backtests). Inputs in L4_data.js (lectures/L4/build_interactive_L4.py).
(function () {
'use strict';
const D = window.LK_DATA, T = window.LK_TEXT;
const { C, ZONE, mean, sdev, quantile, npdf, ncdf, nqnt, nf, pct, $, AX, layout, ttl, plot, out, vline, hline,
  bindSlider, bindSelect, bindToggles, Player, range, safe } = window.EMQAI;
const P = (id, input, vals, ms) => new Player(id, $(input), vals, ms);
const MCOL = { hs: C.BG, normal: C.c5, t: C.c7, fhs: C.RO, evt: C.DE_LU };

// ---------------------------------------------------------------- lecture helpers
const day0 = new Date(D.t0 + 'T00:00:00Z');
const dateOf = (base, i) => new Date(base.getTime() + i * 864e5).toISOString().slice(0, 10);
const NP = D.P.RO.length, DATES = Array.from({ length: NP }, (_, i) => dateOf(day0, i));
// daily change X_t = P_t - P_{t-1} on the full calendar (null next to a missing day)
const XZ = {};
['RO', 'DE_LU'].forEach(z => { const p = D.P[z]; XZ[z] = p.map((v, i) => (i && v !== null && p[i - 1] !== null ? v - p[i - 1] : null)); });
const lgam = x => { const c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5];
  let y = x, t = x + 5.5; t -= (x + 0.5) * Math.log(t); let s = 1.000000000190015; for (const v of c) s += v / ++y; return -t + Math.log(2.5066282746310005 * s / x); };
// binomial cdf P(K <= k), K ~ Binomial(n, p)
function bcdf(k, n, p) { let s = 0; for (let j = 0; j <= k; j++) s += Math.exp(lgam(n + 1) - lgam(j + 1) - lgam(n - j + 1) + j * Math.log(p) + (n - j) * Math.log(1 - p)); return Math.min(s, 1); }
// Kupiec unconditional coverage test: LR statistic and chi-square(1) p-value
function kupiec(x, n, p0) {
  const ph = x / n, ll0 = (n - x) * Math.log(1 - p0) + x * Math.log(p0);
  const ll1 = ph > 0 && ph < 1 ? (n - x) * Math.log(1 - ph) + x * Math.log(ph) : 0;
  const lr = Math.max(-2 * (ll0 - ll1), 0);
  return { lr, p: 2 * (1 - ncdf(Math.sqrt(lr))) };
}
const pfmt = p => (p < 0.0001 ? '< ' + nf(0.0001, 4) : nf(p, 4));
const apct = a => nf(100 * a, a * 1000 % 10 ? 1 : 0) + '%';

// ---------------------------------------------------------------- 1. VaR and ES of the daily change: empirical vs normal
safe('var-es', () => {
  const z = bindSelect('ve-z', draw), per = bindSelect('ve-p', draw), al = bindSlider('ve-a', v => nf(v, 1) + '%', draw);
  const SPAN = { all: ['2015-01-01', D.end], calm: ['2015-01-01', '2020-12-31'], crisis: ['2021-01-01', '2022-12-31'], after: ['2023-01-01', D.end] };
  function draw() {
    const zz = z(), pp = per(), a = al() / 100;
    const [d0, d1] = pp === 'last' ? [DATES[NP - 365], D.end] : SPAN[pp];
    const x = XZ[zz].filter((v, i) => v !== null && DATES[i] >= d0 && DATES[i] <= d1);
    const m = mean(x), s = sdev(x), za = nqnt(a);
    const ve = quantile(x, a), ee = mean(x.filter(v => v >= ve)), vn = m + s * za, en = m + s * npdf(za) / (1 - a);
    plot('ve-hist', [{ x, type: 'histogram', nbinsx: 120, marker: { color: C[zz] }, name: T.change, hovertemplate: '%{x}: %{y}<extra></extra>' },
      { x: [ve, ve], y: [0, 1], yaxis: 'y2', mode: 'lines', name: T.varE, line: { color: C.navy, width: 2 } },
      { x: [vn, vn], y: [0, 1], yaxis: 'y2', mode: 'lines', name: T.varN, line: { color: C.grey, width: 2, dash: 'dash' } },
      { x: [ee, ee], y: [0, 1], yaxis: 'y2', mode: 'lines', name: T.esE, line: { color: C.red, width: 2, dash: 'dot' } }],
    layout({ title: ttl(T.change), xaxis: AX(T.eur, { range: [-150, 200] }), yaxis: AX(T.count), bargap: 0.02,
      yaxis2: { overlaying: 'y', range: [0, 1], visible: false } }));
    const zs = x.map(v => (v - m) / s), g = range(0, 10, 0.25);
    const se = g.map(q => zs.filter(v => v > q).length / zs.length);
    plot('ve-surv', [{ x: g, y: se.map(v => v || null), mode: 'lines+markers', name: T.emp, line: { color: C[zz], width: 2 }, marker: { size: 4 } },
      { x: g, y: g.map(q => 1 - ncdf(q)), mode: 'lines', name: T.normal, line: { color: C.grey, width: 2, dash: 'dash' } }],
    layout({ title: ttl(T.surv), xaxis: AX(T.z), yaxis: AX('', { type: 'log', exponentformat: 'power', range: [-6, 0] }) }));
    const k = x.filter(v => v > vn).length;
    out('ve-out', [T.ve(ZONE[zz], T.per[pp], x.length, apct(a), nf(ve, 2), nf(vn, 2), nf(ee, 2), nf(en, 2)),
      T.ve2(k, nf((1 - a) * x.length, 1), nf(ve * 2400, 0))]);
  }
  draw();
  P('ve-play', 've-a', range(90, 99.5, 0.5), 400);
});

// ---------------------------------------------------------------- 2. rolling VaR forecasts and their exceedances
safe('var-paths', () => {
  const m = bindSelect('vp-m', draw), a = bindSelect('vp-a', draw), Lm = bindSelect('vp-L', draw);
  const y = bindSlider('vp-y', v => `${Math.floor(v)}-${String(1 + Math.round((v % 1) * 12)).padStart(2, '0')}`, draw);
  const v0 = new Date(D.vp.d0 + 'T00:00:00Z'), VD = Array.from({ length: D.vp.n }, (_, i) => dateOf(v0, i));
  const off = DATES.indexOf(D.vp.d0), X = XZ.RO.slice(off, off + D.vp.n);
  function draw() {
    const mm = m(), aa = a(), V = D.vp.v[mm][aa], yy = y();
    const y0 = Math.floor(yy), mo = Math.round((yy % 1) * 12), d0 = `${y0}-${String(mo + 1).padStart(2, '0')}-01`;
    const e = new Date(Date.UTC(y0, mo + +Lm(), 1) - 864e5).toISOString().slice(0, 10), d1 = e < D.end ? e : D.end;
    const i0 = VD.indexOf(d0), i1 = VD.indexOf(d1) + 1, xs = VD.slice(i0, i1), xv = X.slice(i0, i1), vv = V.slice(i0, i1);
    const hit = xv.map((v, i) => v !== null && vv[i] !== null && v > vv[i]);
    const ex = xs.filter((_, i) => hit[i]), ey = xv.filter((_, i) => hit[i]);
    const lab = T.varLab(T.meth[mm], apct(+aa));
    plot('vp-chart', [{ x: xs, y: xv, mode: 'lines', name: T.actual, line: { color: C.band, width: 1 } },
      { x: xs, y: vv, mode: 'lines', name: lab, line: { color: MCOL[mm], width: 2 } },
      { x: ex, y: ey, mode: 'markers', name: T.exc, marker: { color: C.red, size: 7, symbol: 'x' } }],
    layout({ title: ttl(lab), xaxis: AX('', { type: 'date' }), yaxis: AX(T.eur) }));
    const n = xv.filter((v, i) => v !== null && vv[i] !== null).length, k = hit.filter(Boolean).length, kp = kupiec(k, n, 1 - aa);
    out('vp-out', [T.vp(d0, d1, T.meth[mm], apct(+aa), k, n, nf((1 - aa) * n, 1), pfmt(kp.p)), T.vp2(T.meth[mm], nf(mean(vv.filter(v => v !== null)), 2))]);
  }
  draw();
  P('vp-play', 'vp-y', range(2017, 2025.75, 0.25), 500);
});

// ---------------------------------------------------------------- 3. GPD tail of the GARCH-filtered residuals
safe('gpd-tail', () => {
  const uq = bindSlider('gp-u', v => v + '%', draw);
  const z = D.gp.z, n = z.length, m = mean(z), s = sdev(z);
  const LV = [0.99, 0.995, 0.999];
  function draw() {
    const f = D.gp.fits[uq()], pu = f.n / n;
    const sf = t => pu * (Math.abs(f.xi) < 1e-6 ? Math.exp(-(t - f.u) / f.beta) : Math.pow(Math.max(1 + f.xi * (t - f.u) / f.beta, 1e-12), -1 / f.xi));
    const q = a => f.u + f.beta / f.xi * (Math.pow(n / f.n * (1 - a), -f.xi) - 1);
    const lo = D.gp.fits[80].u, tail = z.map((v, i) => [v, (n - i) / n]).filter(p => p[0] >= lo);
    const g = range(f.u, Math.max(z[n - 1] * 1.3, f.u + 1), 0.05);
    plot('gp-chart', [{ x: tail.map(p => p[0]), y: tail.map(p => p[1]), mode: 'markers', name: T.emp, marker: { color: C.RO, size: 5 } },
      { x: g, y: g.map(sf), mode: 'lines', name: T.gpd, line: { color: C.DE_LU, width: 2.2 } },
      { x: g, y: g.map(t => 1 - ncdf((t - m) / s)), mode: 'lines', name: T.normal, line: { color: C.grey, width: 2, dash: 'dash' } }],
    layout({ title: ttl(T.gpTitle), xaxis: AX(T.resid), yaxis: AX(T.pex, { type: 'log', exponentformat: 'power' }), shapes: [vline(f.u, C.navy, 'dot')] }));
    const labs = LV.map(a => apct(a)), qe = LV.map(a => quantile(z, a)), qg = LV.map(q), qn = LV.map(a => m + s * nqnt(a));
    plot('gp-q', [{ x: labs, y: qe, type: 'bar', name: T.emp, marker: { color: C.RO } }, { x: labs, y: qg, type: 'bar', name: T.gpd, marker: { color: C.DE_LU } },
      { x: labs, y: qn, type: 'bar', name: T.normal, marker: { color: C.grey } }],
    layout({ title: ttl(T.gpQ), xaxis: AX(T.level, { type: 'category' }), yaxis: AX(T.quant), barmode: 'group' }));
    out('gp-out', [T.gp(nf(f.u, 2), uq() + '%', f.n, nf(f.xi, 3), nf(f.beta, 3)), T.gp2(nf(qe[2], 2), nf(qg[2], 2), nf(qn[2], 2)), T.gp3(n, D.gp.d0, D.gp.d1)]);
  }
  draw();
  P('gp-play', 'gp-u', range(80, 97, 1), 500);
});

// ---------------------------------------------------------------- 4. Basel traffic light: rolling count of 99% VaR exceedances
safe('traffic-light', () => {
  const ms = bindToggles('tl-m', draw), w = bindSlider('tl-w', v => v, draw);
  const v0 = new Date(D.vp.d0 + 'T00:00:00Z'), VD = Array.from({ length: D.vp.n }, (_, i) => dateOf(v0, i));
  const off = DATES.indexOf(D.vp.d0), X = XZ.RO.slice(off, off + D.vp.n);
  const HIT = {};
  Object.keys(D.vp.v).forEach(m => { const V = D.vp.v[m]['0.99']; HIT[m] = X.map((v, i) => (v !== null && V[i] !== null && v > V[i] ? 1 : 0)); });
  function draw() {
    const W = w();
    // Basel zones: green while P(K <= k) < 95%, red from the first k with P(K <= k) >= 99.99%
    let g = 0; while (bcdf(g + 1, W, 0.01) < 0.95) g++;
    let r = g + 1; while (bcdf(r, W, 0.01) < 0.9999) r++;
    const tr = [], rows = [];
    let ymax = r + 2;
    ms().forEach(m => {
      const h = HIT[m], c = []; let s = 0;
      for (let i = 0; i < h.length; i++) { s += h[i]; if (i >= W) s -= h[i - W]; c.push(i >= W - 1 ? s : null); }
      const cc = c.slice(W - 1), N = cc.length, mx = Math.max(...cc);
      ymax = Math.max(ymax, mx + 1);
      tr.push({ x: VD, y: c, mode: 'lines', name: T.meth[m], line: { color: MCOL[m], width: 1.8 } });
      rows.push(T.tlRow(T.meth[m], pct(cc.filter(v => v <= g).length / N, 1), pct(cc.filter(v => v > g && v < r).length / N, 1), pct(cc.filter(v => v >= r).length / N, 1), mx));
    });
    const band = (y0, y1, col) => ({ type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0, y1, fillcolor: col, opacity: 0.18, line: { width: 0 }, layer: 'below' });
    plot('tl-chart', tr, layout({ title: ttl(T.tlTitle(W)), xaxis: AX('', { type: 'date' }), yaxis: AX(T.cntL, { range: [0, ymax] }),
      shapes: [band(0, g + 0.5, C.green), band(g + 0.5, r - 0.5, '#E3B400'), band(r - 0.5, ymax, C.red)] }));
    out('tl-out', [T.tl(W, g, r)].concat(rows));
  }
  draw();
  P('tl-play', 'tl-w', range(100, 500, 25), 500);
});

// ---------------------------------------------------------------- 5. horizon: empirical h-day quantiles vs the square-root-of-time rule
safe('horizon', () => {
  const z = bindSelect('hz-z', draw), al = bindSlider('hz-a', v => nf(v, 1) + '%', draw), hh = bindSlider('hz-h', v => v, draw);
  const H = range(1, 20, 1);
  const diffs = (p, h) => { const r = []; for (let i = 0; i + h < p.length; i++) if (p[i] !== null && p[i + h] !== null) r.push(p[i + h] - p[i]); return r; };
  const vr = (x) => { const m = mean(x); return x.reduce((s, v) => s + (v - m) ** 2, 0) / (x.length - 1); };
  function draw() {
    const p = D.P[z()], a = al() / 100, dd = H.map(h => diffs(p, h)), q = dd.map(x => quantile(x, a)), v1 = vr(dd[0]);
    const ratio = q.map(v => v / q[0]), vrat = dd.map((x, i) => vr(x) / (H[i] * v1)), h = hh();
    plot('hz-chart', [{ x: H, y: ratio, mode: 'lines+markers', name: T.emp2, line: { color: C[z()], width: 2 } },
      { x: H, y: H.map(Math.sqrt), mode: 'lines', name: T.sqrt, line: { color: C.grey, width: 2, dash: 'dash' } }],
    layout({ title: ttl(T.hzTitle), xaxis: AX(T.h, { dtick: 2 }), yaxis: AX(''), shapes: [vline(h, C.navy, 'dot')] }));
    plot('hz-vr', [{ x: H, y: vrat, type: 'bar', marker: { color: H.map(k => (k === h ? C[z()] : C.band)) }, showlegend: false }],
      layout({ title: ttl(T.hzVr), xaxis: AX(T.h, { dtick: 2 }), yaxis: AX(''), shapes: [hline(1, C.grey, 'dash')] }));
    const x1 = dd[0], m1 = mean(x1);
    // first-order autocorrelation of the daily change (consecutive calendar days, both observed)
    const X = XZ[z()], pr = []; for (let i = 1; i < X.length; i++) if (X[i] !== null && X[i - 1] !== null) pr.push([X[i - 1], X[i]]);
    const ma = mean(pr.map(v => v[0])), mb = mean(pr.map(v => v[1]));
    const r1 = pr.reduce((s, v) => s + (v[0] - ma) * (v[1] - mb), 0) / Math.sqrt(pr.reduce((s, v) => s + (v[0] - ma) ** 2, 0) * pr.reduce((s, v) => s + (v[1] - mb) ** 2, 0));
    out('hz-out', [T.hz(ZONE[z()], nf(100 * a, 1) + '%', h, nf(ratio[h - 1], 2), nf(Math.sqrt(h), 2), nf(q[0], 2), nf(q[h - 1], 2)),
      T.hz2(h, nf(vrat[h - 1], 2), nf(r1, 3))]);
    void m1;
  }
  draw();
  P('hz-play', 'hz-h', range(1, 20, 1), 400);
});

// ---------------------------------------------------------------- 6. supplier: monthly cost overrun against a normal limit
safe('supplier', () => {
  const ye = bindSlider('sm-e', v => v, draw), al = bindSlider('sm-a', v => nf(v, 1) + '%', draw);
  const M = D.sm.m, O = D.sm.o;
  function draw() {
    const y = ye(), a = al() / 100, cut = `${y}-12`;
    const ins = O.filter((_, i) => M[i] <= cut), m = mean(ins), s = sdev(ins), lim = m + s * nqnt(a);
    const after = M.map((mm, i) => i).filter(i => M[i] > cut), k = after.filter(i => O[i] > lim);
    const col = M.map((mm, i) => (mm <= cut ? C.band : O[i] > lim ? C.red : C.RO));
    plot('sm-chart', [{ x: M, y: O, type: 'bar', marker: { color: col }, name: T.overrun, hovertemplate: '%{x}: %{y:.1f}%<extra></extra>' },
      { x: [M[0], M[M.length - 1]], y: [lim, lim], mode: 'lines', name: T.limit + ' ' + apct(a), line: { color: C.navy, width: 2, dash: 'dash' } }],
    layout({ title: ttl(T.smTitle), xaxis: AX('', { type: 'category', nticks: 12 }), yaxis: AX('%'), bargap: 0.1 }));
    const lines = [T.sm(y, apct(a), nf(m, 2), nf(s, 2), nf(lim, 1))];
    if (after.length) {
      const wi = after.reduce((b, i) => (O[i] > O[b] ? i : b), after[0]);
      lines.push(T.sm2(after.length, k.length, nf((1 - a) * after.length, 1), M[wi], nf(O[wi], 1), nf(D.sm.eur[wi], 2)));
    }
    out('sm-out', lines);
  }
  draw();
  P('sm-play', 'sm-e', range(2017, 2025, 1), 700);
});
})();
