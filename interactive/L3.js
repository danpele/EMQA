// Lecture 3 interactive page: volatility. Inputs in L3_data.js (lectures/L3/build_interactive_L3.py).
(function () {
'use strict';
const D = window.LK_DATA, T = window.LK_TEXT;
const { C, mean, sdev, npdf, ncdf, nqnt, nf, pct, cnt, $, AX, layout, ttl, plot, out, hline, bindSlider, bindSelect, Player, range, safe } = window.EMQAI;
const P = (id, input, vals, ms) => new Player(id, $(input), vals, ms);
const CU = { pct: C.RO, eur: C.c7 };

// ---------------------------------------------------------------- lecture helpers
const days = (t0, n) => { const a = new Date(t0 + 'T00:00:00Z'); return Array.from({ length: n }, (_, i) => new Date(a.getTime() + i * 864e5).toISOString().slice(0, 10)); };
function acf(x, L) {
  const m = mean(x), d = x.map(v => v - m), v0 = d.reduce((s, v) => s + v * v, 0), r = [];
  for (let k = 1; k <= L; k++) { let s = 0; for (let t = k; t < d.length; t++) s += d[t] * d[t - k]; r.push(s / v0); }
  return r;
}
const ljung = (r, n, m) => n * (n + 2) * r.slice(0, m).reduce((s, v, k) => s + v * v / (n - k - 1), 0);
// log-gamma (Lanczos) and the Student-t distribution (regularised incomplete beta, Numerical Recipes)
function lgam(x) { const c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5]; let y = x, t = x + 5.5; t -= (x + 0.5) * Math.log(t); let s = 1.000000000190015; for (const v of c) s += v / ++y; return -t + Math.log(2.5066282746310005 * s / x); }
function betacf(a, b, x) {
  let qab = a + b, qap = a + 1, qam = a - 1, c = 1, d = 1 - qab * x / qap; if (Math.abs(d) < 1e-30) d = 1e-30; d = 1 / d; let h = d;
  for (let m = 1; m <= 200; m++) {
    const m2 = 2 * m; let aa = m * (b - m) * x / ((qam + m2) * (a + m2));
    d = 1 + aa * d; if (Math.abs(d) < 1e-30) d = 1e-30; c = 1 + aa / c; if (Math.abs(c) < 1e-30) c = 1e-30; d = 1 / d; h *= d * c;
    aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
    d = 1 + aa * d; if (Math.abs(d) < 1e-30) d = 1e-30; c = 1 + aa / c; if (Math.abs(c) < 1e-30) c = 1e-30; d = 1 / d; const del = d * c; h *= del;
    if (Math.abs(del - 1) < 3e-12) break;
  }
  return h;
}
function ibeta(a, b, x) {
  if (x <= 0) return 0; if (x >= 1) return 1;
  const bt = Math.exp(lgam(a + b) - lgam(a) - lgam(b) + a * Math.log(x) + b * Math.log(1 - x));
  return x < (a + 1) / (a + b + 2) ? bt * betacf(a, b, x) / a : 1 - bt * betacf(b, a, 1 - x) / b;
}
const tcdf = (t, nu) => { const p = 0.5 * ibeta(nu / 2, 0.5, nu / (nu + t * t)); return t > 0 ? 1 - p : p; };
function tq(p, nu) { let lo = -50, hi = 50; for (let k = 0; k < 80; k++) { const m = (lo + hi) / 2; tcdf(m, nu) < p ? (lo = m) : (hi = m); } return (lo + hi) / 2; }
const tpdfStd = (z, nu) => { const s = Math.sqrt((nu - 2) / nu); return Math.exp(lgam((nu + 1) / 2) - lgam(nu / 2) - 0.5 * Math.log(nu * Math.PI) - (nu + 1) / 2 * Math.log(1 + (z / s) ** 2 / nu)) / s; };
// GARCH(1,1) variance filter with the backcast of the Python arch package (EWMA, lambda 0.94, of the first 75 squared shocks)
function garch(e, om, a, b) {
  const n = Math.min(75, e.length); let w = 0, bc = 0;
  for (let i = 0; i < n; i++) { const wi = Math.pow(0.94, i); w += wi; bc += wi * e[i] * e[i]; }
  bc /= w;
  const h = new Array(e.length); h[0] = om + (a + b) * bc;
  for (let t = 1; t < e.length; t++) h[t] = om + a * e[t - 1] * e[t - 1] + b * h[t - 1];
  return h;
}
const halfLife = p => (p > 0 && p < 1 ? Math.log(0.5) / Math.log(p) : Infinity);
const setVal = (id, v) => { const el = $(id); el.value = v; el.dispatchEvent(new Event('input')); };

// ---------------------------------------------------------------- 1. clustering: ACF of shocks and squared shocks
safe('clustering', () => {
  const u = bindSelect('cl-u', draw), L = bindSlider('cl-L', v => v, draw), y = bindSlider('cl-y', v => v, draw);
  function draw() {
    const S = D[u()], dd = days(S.t0, S.e.length), i0 = dd.findIndex(x => x >= `${y()}-01-01`), e = S.e.slice(i0), e2 = e.map(v => v * v);
    const ra = acf(e, 60), rb = acf(e2, 60), n = e.length, b = 1.96 / Math.sqrt(n), lags = Array.from({ length: L() }, (_, i) => i + 1);
    const lay = t => layout({ title: ttl(t), xaxis: AX(T.lag), yaxis: AX(T.acf, { range: [-0.15, 0.6] }), showlegend: false, bargap: 0.3,
      shapes: [{ type: 'rect', xref: 'paper', yref: 'y', x0: 0, x1: 1, y0: -b, y1: b, fillcolor: 'rgba(154,154,154,0.25)', line: { width: 0 } }] });
    plot('cl-e', [{ x: lags, y: ra.slice(0, L()), type: 'bar', marker: { color: CU[u()] }, hovertemplate: '%{x}: %{y:.3f}<extra></extra>' }], lay(T.e + ' (' + T.unit[u()] + ')'));
    plot('cl-e2', [{ x: lags, y: rb.slice(0, L()), type: 'bar', marker: { color: CU[u()] }, hovertemplate: '%{x}: %{y:.3f}<extra></extra>' }], lay(T.e2));
    out('cl-out', [T.cl(y(), n, nf(ra[0], 3), nf(rb[0], 3), nf(ljung(ra, n, 10), 1), nf(ljung(rb, n, 10), 1))]);
  }
  draw();
  P('cl-play', 'cl-y', range(2019, 2025, 1), 900);
});

// ---------------------------------------------------------------- 2. fat tails of the standardised shocks
safe('fat-tails', () => {
  const nu = bindSlider('ft-nu', v => nf(v, 1), draw), k = bindSlider('ft-k', v => nf(v, 1), draw);
  const z = D.z, N = z.length, w = 0.25, edges = range(-8, 8, w), cnts = new Array(edges.length - 1).fill(0);
  z.forEach(v => { const c = Math.min(Math.max(v, -7.999), 7.999); cnts[Math.floor((c + 8) / w)]++; });
  const mids = cnts.map((_, i) => edges[i] + w / 2), dens = cnts.map(c => (c ? c / (N * w) : null));
  const xs = range(-8, 8, 0.05);
  function draw() {
    const v = nu(), kk = k();
    const tr = [{ x: mids, y: dens, type: 'bar', name: T.hist, marker: { color: C.RO, opacity: 0.55 }, hovertemplate: '%{x:.2f}: %{y:.4f}<extra></extra>' },
      { x: xs, y: xs.map(npdf), mode: 'lines', name: T.normal, line: { color: C.ink, dash: 'dash', width: 1.4 } },
      { x: xs, y: xs.map(x => tpdfStd(x, v)), mode: 'lines', name: T.stud(nf(v, 1)), line: { color: C.DE_LU, width: 2 } }];
    plot('ft-chart', tr, layout({ title: ttl(T.dens), xaxis: AX(T.z), yaxis: AX('', { type: 'log', range: [-4, 0] }), bargap: 0,
      shapes: [{ type: 'line', x0: kk, x1: kk, yref: 'paper', y0: 0, y1: 1, line: { color: C.grey, dash: 'dot', width: 1.2 } },
               { type: 'line', x0: -kk, x1: -kk, yref: 'paper', y0: 0, y1: 1, line: { color: C.grey, dash: 'dot', width: 1.2 } }] }));
    const n = z.filter(x => Math.abs(x) > kk).length, s = Math.sqrt((v - 2) / v);
    out('ft-out', [T.ft(nf(kk, 1), n, N, nf(N * 2 * (1 - ncdf(kk)), 2), nf(N * 2 * (1 - tcdf(kk / s, v)), 1))]);
  }
  $('ft-nu').value = D.z_nu; $('ft-nu').dispatchEvent(new Event('input'));
  P('ft-play', 'ft-nu', range(2.5, 30, 0.5), 200);
});

// ---------------------------------------------------------------- 3. GARCH(1,1) filter in the browser
safe('garch-filter', () => {
  const u = bindSelect('gf-u', () => { const g = D[u()].garch; $('gf-a').value = g.alpha; $('gf-b').value = g.beta; $('gf-b').dispatchEvent(new Event('input')); $('gf-a').dispatchEvent(new Event('input')); });
  const a = bindSlider('gf-a', v => nf(v, 3), draw), b = bindSlider('gf-b', v => nf(v, 3), draw);
  function draw() {
    const S = D[u()], g = S.garch, aa = a(), bb = Math.min(b(), 0.999 - aa), p = aa + bb, om = g.uvar * (1 - p);
    const e = S.e, h = garch(e, om, aa, bb), sig = h.map(Math.sqrt), dd = days(S.t0, e.length);
    const roll = e.map((_, t) => (t < 29 ? null : Math.sqrt(e.slice(t - 29, t + 1).reduce((s, v) => s + v * v, 0) / 30)));
    let ll = 0; const nu = g.nu;
    for (let t = 0; t < e.length; t++) ll += S.tconst - 0.5 * Math.log(h[t]) - (nu + 1) / 2 * Math.log(1 + e[t] * e[t] / (h[t] * (nu - 2)));
    plot('gf-chart', [{ x: dd, y: roll, mode: 'lines', name: T.roll, line: { color: C.grey, width: 1 } },
      { x: dd, y: sig, mode: 'lines', name: T.garch, line: { color: CU[u()], width: 1.3 } }],
    layout({ title: ttl(T.sig(T.unit[u()])), xaxis: AX('', { type: 'date' }), yaxis: AX(T.unit[u()], { rangemode: 'tozero' }) }));
    const im = sig.indexOf(Math.max(...sig)), hl = halfLife(p);
    out('gf-out', [T.gf(nf(aa, 3), nf(bb, 3), nf(p, 3), Number.isFinite(hl) ? T.days(nf(hl, 1)) : T.inf, nf(Math.sqrt(g.uvar), 2), nf(om, 3)),
      T.gf2(nf(ll, 1), nf(g.ll, 1), nf(sig[im], 1), dd[im])]);
  }
  { const g = D.pct.garch; $('gf-a').value = g.alpha; $('gf-b').value = g.beta; $('gf-a').dispatchEvent(new Event('input')); $('gf-b').dispatchEvent(new Event('input')); }
  P('gf-play', 'gf-b', range(0, 0.68, 0.02), 250);
});

// ---------------------------------------------------------------- 4. half-life of a volatility shock
safe('half-life', () => {
  const p = bindSlider('hl-p', v => nf(v, 3), draw), H = bindSlider('hl-h', v => v, draw);
  const NM = { RO_pct: ['Romania, %', 'România, %'], RO_eur: ['Romania, EUR/MWh', 'România, EUR/MWh'], BRENT: ['Brent', 'Brent'], EUA: ['EUA', 'EUA'], SNP: ['OMV Petrom (SNP)', 'OMV Petrom (SNP)'] };
  const COL = { RO_pct: C.RO, RO_eur: C.c7, BRENT: C.DE_LU, EUA: C.HU, SNP: C.BG };
  const ro = window.EMQAI.LANG === 'ro' ? 1 : 0;
  function draw() {
    const hh = range(0, H(), 1), tr = Object.entries(D.xm).map(([k, x]) => ({ x: hh, y: hh.map(h => 100 * Math.pow(x.pers, h)), mode: 'lines',
      name: `${NM[k][ro]} (${nf(x.hl, 1)})`, line: { color: COL[k], width: 1.3 } }));
    tr.push({ x: hh, y: hh.map(h => 100 * Math.pow(p(), h)), mode: 'lines', name: T.you, line: { color: C.navy, width: 3, dash: 'dash' } });
    plot('hl-chart', tr, layout({ xaxis: AX(T.after), yaxis: AX(T.left, { range: [0, 100] }), shapes: [hline(50, C.ink, 'dot')] }));
    const hl = halfLife(p());
    out('hl-out', [T.hl2(nf(p(), 3), nf(hl, 1), pct(Math.pow(p(), 10), 1))]);
  }
  draw();
  P('hl-play', 'hl-p', [0.5, 0.6, 0.7, 0.746, 0.8, 0.85, 0.9, 0.934, 0.95, 0.973, 0.98, 0.992, 0.994, 0.999], 600);
});

// ---------------------------------------------------------------- 5. news impact curve (GJR-GARCH-t)
safe('news-impact', () => {
  const u = bindSelect('ni-u', () => { const g = D[u()].gjr; $('ni-a').value = g.alpha; $('ni-g').value = g.gamma; $('ni-g').dispatchEvent(new Event('input')); $('ni-a').dispatchEvent(new Event('input')); });
  const gm = bindSlider('ni-g', v => nf(v, 3), draw), a = bindSlider('ni-a', v => nf(v, 3), draw);
  function draw() {
    const g = D[u()].gjr, aa = a(), gg = Math.max(gm(), -aa), ph = aa + gg / 2 + g.beta;
    const pp = Math.min(ph, 0.999), s2 = g.omega / (1 - pp), sd = Math.sqrt(s2);
    const xs = range(-4, 4, 0.04).map(k => k * sd);
    const f = (x, gam) => Math.sqrt(g.omega + g.beta * s2 + (aa + gam * (x < 0)) * x * x);
    const neg = xs.filter(x => x < 0), pos = xs.filter(x => x >= 0);
    plot('ni-chart', [{ x: neg, y: neg.map(x => f(x, gg)), mode: 'lines', name: T.fall, line: { color: C.c8, width: 2.2 } },
      { x: pos, y: pos.map(x => f(x, gg)), mode: 'lines', name: T.rise, line: { color: C.HU, width: 2.2 } },
      { x: xs, y: xs.map(x => Math.sqrt(g.omega + g.beta * s2 + (aa + gg / 2) * x * x)), mode: 'lines', name: T.sym, line: { color: C.grey, width: 1.2, dash: 'dot' } }],
    layout({ xaxis: AX(T.shock(T.unit[u()])), yaxis: AX(T.next(T.unit[u()]), { rangemode: 'tozero' }) }));
    const dn = f(-2 * sd, gg), up = f(2 * sd, gg);
    out('ni-out', [T.ni(T.unit[u()], nf(2 * sd, 1), nf(dn, 2), nf(up, 2), nf(dn / up, 2)), T.ni2(nf(ph, 3))]);
  }
  { const g = D.pct.gjr; $('ni-a').value = g.alpha; $('ni-g').value = g.gamma; $('ni-a').dispatchEvent(new Event('input')); $('ni-g').dispatchEvent(new Event('input')); }
  P('ni-play', 'ni-g', range(-0.3, 0.6, 0.05), 400);
});

// ---------------------------------------------------------------- 6. one-day band on the test year
safe('forecast-band', () => {
  const m = bindSelect('fb-m', draw), c = bindSlider('fb-c', v => v, draw);
  const F = D.fb, n = F.date.length;
  function draw() {
    const cc = c(), q = (1 + cc / 100) / 2, lo = [], hi = [], xo = [], yo = [];
    let k = 0, w = 0, k1 = 0, n1 = 0, k2 = 0, n2 = 0;
    for (let i = 0; i < n; i++) {
      const v = F[m()][i], nu = F.nu[i];
      const z = m() === 'garch' ? tq(q, nu) * Math.sqrt((nu - 2) / nu) : nqnt(q), hw = z * Math.sqrt(v), mid = F.p1[i] + F.yhat[i];
      lo.push(mid - hw); hi.push(mid + hw); w += hw;
      const o = Math.abs(F.e[i]) > hw;
      if (o) { k++; xo.push(F.date[i]); yo.push(F.p[i]); }
      if (F.date[i] < '2026-05-01') { n1++; k1 += o; } else { n2++; k2 += o; }
    }
    plot('fb-chart', [{ x: F.date, y: hi, mode: 'lines', line: { width: 0 }, showlegend: false, hoverinfo: 'skip' },
      { x: F.date, y: lo, mode: 'lines', fill: 'tonexty', fillcolor: 'rgba(98,80,214,0.22)', line: { width: 0 }, name: T.bandL(cc), hoverinfo: 'skip' },
      { x: F.date, y: F.p, mode: 'lines', name: T.price, line: { color: C.RO, width: 1.2 } },
      { x: xo, y: yo, mode: 'markers', name: T.outside, marker: { color: C.c8, size: 6 } }],
    layout({ xaxis: AX('', { type: 'date' }), yaxis: AX(T.price) }));
    out('fb-out', [T.fb(cc, k, n, pct(k / n, 1), nf(w / n, 1)), T.fb2(pct(k1 / n1, 1), pct(k2 / n2, 1))]);
  }
  draw();
  P('fb-play', 'fb-c', range(50, 99, 1), 150);
});
})();
