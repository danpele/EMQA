// Lecture 5 interactive page: derivatives and hedging. Inputs in L5_data.js (lectures/L5/build_interactive_L5.py).
(function () {
'use strict';
const D = window.LK_DATA, T = window.LK_TEXT;
const { LANG, C, ZONE, mean, sdev, ncdf, npdf, nf, $, AX, layout, ttl, plot, out, vline, hline,
  bindSlider, bindSelect, bindToggles, Player, range, safe } = window.EMQAI;
const players = [];
const P = (id, input, vals, ms) => players.push(new Player(id, $(input), vals, ms));
const KC = { M: C.RO, Q: C.HU, H: C.BG, Y: C.DE_LU };
const ymAdd = (ym, k) => { let y = +ym.slice(0, 4), m = +ym.slice(5, 7) - 1 + k; y += Math.floor(m / 12); m = ((m % 12) + 12) % 12; return `${y}-${String(m + 1).padStart(2, '0')}`; };
const monthEnd = ym => { const y = +ym.slice(0, 4), m = +ym.slice(5, 7); return new Date(Date.UTC(y, m, 0)).toISOString().slice(0, 10); };
const mIdx = {}; D.m.t.forEach((t, i) => (mIdx[t] = i));
const ymLabel = ym => (LANG === 'ro' ? window.EMQAI.MONTHS[+ym.slice(5, 7) - 1] + ' ' + ym.slice(0, 4) : window.EMQAI.MONTHS[+ym.slice(5, 7) - 1] + ' ' + ym.slice(0, 4));

// ---------------------------------------------------------------- 1. forward curve at a chosen month end
safe('forward-curve', () => {
  const F = D.fw, first = F.d[0].slice(0, 7), last = D.end.slice(0, 7), ends = [];
  for (let ym = first; ym <= last; ym = ymAdd(ym, 1)) ends.push(ym);
  const el = $('fc-t'); el.max = ends.length - 1; el.value = ends.length - 1; el.defaultValue = String(ends.length - 1);
  const t = bindSlider('fc-t', v => monthEnd(ends[v]), draw), w = bindSlider('fc-w', v => v, draw);
  function realised(s, e) {                    // mean of complete monthly means (RO) over [s, e], if all months are available
    const v = []; for (let ym = s; ym <= e; ym = ymAdd(ym, 1)) { const i = mIdx[ym]; if (i === undefined || D.m.RO[i] === null) return null; v.push(D.m.RO[i]); }
    return v.length ? mean(v) : null;
  }
  function draw() {
    const E = ends[t()], dE = monthEnd(E), d0 = monthEnd(ymAdd(E, -w()));
    const g = {};
    let n = 0;
    for (let i = 0; i < F.d.length; i++) {
      if (F.d[i] <= d0 || F.d[i] > dE || F.s[i] <= E) continue;
      const key = F.s[i] + '|' + F.e[i] + '|' + F.k[i];
      (g[key] = g[key] || { s: F.s[i], e: F.e[i], k: F.k[i], pq: 0, q: 0, n: 0 });
      g[key].pq += F.p[i] * F.q[i]; g[key].q += F.q[i]; g[key].n++; n++;
    }
    const prods = Object.values(g).sort((a, b) => (a.s + a.k).localeCompare(b.s + b.k));
    const tr = [], seen = {};
    prods.forEach(p => {
      const f = p.pq / p.q;
      tr.push({ x: [p.s + '-01', monthEnd(p.e)], y: [f, f], mode: 'lines', line: { color: KC[p.k], width: p.k === 'Y' ? 5 : 3.5 },
        name: T.kindPl[p.k], legendgroup: p.k, showlegend: !seen[p.k], hovertemplate: `${p.s}–${p.e}: %{y:.2f} EUR/MWh<extra>${T.kindPl[p.k]}</extra>` });
      seen[p.k] = true;
    });
    const x0 = ymAdd(E, -12), x1 = prods.length ? prods.reduce((a, p) => (p.e > a ? p.e : a), E) : ymAdd(E, 12);
    const sx = [], sy = [];
    for (let ym = x0; ym <= x1 && mIdx[ym] !== undefined; ym = ymAdd(ym, 1)) { sx.push(ym + '-15'); sy.push(D.m.RO[mIdx[ym]]); }
    tr.unshift({ x: sx, y: sy, mode: 'lines+markers', name: T.spot, line: { color: C.grey, width: 1.3 }, marker: { size: 4 }, hovertemplate: '%{x|%Y-%m}: %{y:.1f}<extra></extra>' });
    plot('fc-chart', tr, layout({ title: ttl(T.fcTitle(dE, w())), xaxis: AX('', { type: 'date', range: [x0 + '-01', monthEnd(x1)] }),
      yaxis: AX(T.eur, { rangemode: 'tozero' }), shapes: [vline(dE, C.navy, 'dash')] }));
    if (!prods.length) { out('fc-out', [T.fc0]); return; }
    const lm = D.m.RO[mIdx[E]];
    const items = prods.filter(p => p.k !== 'M' || prods.filter(q => q.k === 'M').indexOf(p) < 3).slice(0, 7).map(p => {
      const r = p.e <= D.end.slice(0, 7) ? realised(p.s, p.e) : null;
      return T.fcItem(T.kind[p.k], p.s, p.e !== p.s ? p.e : '', nf(p.pq / p.q, 2), r !== null ? nf(r, 2) : '');
    });
    out('fc-out', [T.fc(n, prods.length, lm !== null && lm !== undefined ? nf(lm, 2) : '–'), items.join('; ') + '.']);
  }
  draw();
  P('fc-play', 'fc-t', range(0, ends.length - 1, 1), 350);
});

// ---------------------------------------------------------------- 2. clean spark and clean dark spreads
safe('spreads', () => {
  const z = bindSelect('sp-z', draw), g = bindSlider('sp-g', v => nf(v, 2), draw), c = bindSlider('sp-c', v => nf(v, 2), draw);
  const EFG = 0.202, EFC = 0.341;
  function draw() {
    const zz = z(), eg = g(), ec = c(), M = D.m;
    const css = M.t.map((_, i) => (M[zz][i] === null || M.gas[i] === null || M.eua[i] === null ? null : M[zz][i] - M.gas[i] / eg - EFG / eg * M.eua[i]));
    const cds = M.t.map((_, i) => (M[zz][i] === null || M.coal[i] === null || M.eua[i] === null ? null : M[zz][i] - M.coal[i] / ec - EFC / ec * M.eua[i]));
    const x = M.t.map(t => t + '-15');
    plot('sp-chart', [
      { x, y: css, mode: 'lines', name: T.css, line: { color: C.RO, width: 1.6 }, hovertemplate: '%{x|%Y-%m}: %{y:.1f}<extra></extra>' },
      { x, y: cds, mode: 'lines', name: T.cds, line: { color: C.c8, width: 1.4, dash: 'dash' }, hovertemplate: '%{x|%Y-%m}: %{y:.1f}<extra></extra>' }],
    layout({ title: ttl(T.spTitle(ZONE[zz])), xaxis: AX('', { type: 'date' }), yaxis: AX(T.eur), shapes: [hline(0, C.navy, 'dot')] }));
    const ok = css.map((v, i) => v !== null && cds[i] !== null);
    const n = ok.filter(Boolean).length, nm = css.filter((v, i) => ok[i] && v < 0).length, nd = cds.filter((v, i) => ok[i] && v < 0).length;
    const li = ok.lastIndexOf(true);
    out('sp-out', [T.sp(n, nm, nd, li, M.t[li], nf(css[li], 2), nf(cds[li], 2)),
      T.sp2(nf(M.gas[li] / eg + EFG / eg * M.eua[li], 2), nf(M.coal[li] / ec + EFC / ec * M.eua[li], 2), nf(M.eua[li], 2))]);
  }
  draw();
  P('sp-play', 'sp-g', range(0.35, 0.62, 0.01), 250);
});

// ---------------------------------------------------------------- 3. minimum-variance hedge ratio
const cov = (a, b) => { const ma = mean(a), mb = mean(b); let s = 0; for (let i = 0; i < a.length; i++) s += (a[i] - ma) * (b[i] - mb); return s / (a.length - 1); };
function changes(zz) {   // monthly changes where both months are complete: [ym, dRO, dZ]
  const M = D.m, r = [];
  for (let i = 1; i < M.t.length; i++) {
    if ([M.RO[i], M.RO[i - 1], M[zz][i], M[zz][i - 1]].some(v => v === null)) continue;
    r.push([M.t[i], M.RO[i] - M.RO[i - 1], M[zz][i] - M[zz][i - 1]]);
  }
  return r;
}
safe('hedge-ratio', () => {
  const z = bindSelect('hr-z', draw), a = bindSlider('hr-a', v => v, draw), b = bindSlider('hr-b', v => v, draw);
  function draw() {
    const zz = z(), lo = Math.min(a(), b()), hi = Math.max(a(), b());
    const all = changes(zz), sel = all.filter(r => +r[0].slice(0, 4) >= lo && +r[0].slice(0, 4) <= hi);
    const x = sel.map(r => r[2]), y = sel.map(r => r[1]);
    const h = cov(x, y) / cov(x, x), rho = cov(x, y) / Math.sqrt(cov(x, x) * cov(y, y));
    const xs = [Math.min(...x), Math.max(...x)];
    plot('hr-sc', [
      { x, y, mode: 'markers', name: ZONE[zz], marker: { color: C[zz], size: 6, opacity: 0.7 }, text: sel.map(r => r[0]), hovertemplate: '%{text}: %{x:.1f}, %{y:.1f}<extra></extra>' },
      { x: xs, y: xs.map(v => mean(y) + h * (v - mean(x))), mode: 'lines', name: T.fit, line: { color: C.navy, width: 2 } }],
    layout({ title: ttl(`h* = ${nf(h, 3)}`), xaxis: AX(T.dF(ZONE[zz])), yaxis: AX(T.dRO), showlegend: false }));
    // rolling 36-month hedge ratio over the whole sample
    const rx = [], ry = [];
    for (let i = 35; i < all.length; i++) { const w = all.slice(i - 35, i + 1), u = w.map(r => r[2]), v = w.map(r => r[1]); rx.push(all[i][0] + '-15'); ry.push(cov(u, v) / cov(u, u)); }
    plot('hr-roll', [{ x: rx, y: ry, mode: 'lines', name: T.roll, line: { color: C[zz], width: 1.6 } }],
      layout({ title: ttl(T.hrRoll), xaxis: AX('', { type: 'date' }), yaxis: AX('h*'), showlegend: false,
        shapes: [hline(1, C.grey, 'dot'), { type: 'rect', xref: 'x', yref: 'paper', x0: `${lo}-01-01`, x1: `${hi}-12-31`, y0: 0, y1: 1, fillcolor: C.band, opacity: 0.35, line: { width: 0 } }] }));
    const sd = v => sdev(v);
    out('hr-out', [T.hr(ZONE[zz], lo, hi, sel.length, nf(h, 3), nf(rho * rho, 3), nf(rho, 3)),
      T.hr2(nf(sd(y), 2), nf(sd(y.map((v, i) => v - h * x[i])), 2), nf(sd(y.map((v, i) => v - x[i])), 2))]);
  }
  draw();
  P('hr-play', 'hr-a', range(2015, 2024, 1), 700);
});

// ---------------------------------------------------------------- 4. basis risk
safe('basis', () => {
  const z = bindSelect('bs-z', draw), s = bindSlider('bs-s', v => v, draw);
  function draw() {
    const zz = z(), y0 = s(), M = D.m;
    const t = [], b = [];
    M.t.forEach((ym, i) => { if (M.RO[i] !== null && M[zz][i] !== null) { t.push(ym); b.push(M.RO[i] - M[zz][i]); } });
    const pre = b.filter((_, i) => +t[i].slice(0, 4) < y0), post = b.filter((_, i) => +t[i].slice(0, 4) >= y0);
    plot('bs-chart', [{ x: t.map(v => v + '-15'), y: b, type: 'bar', marker: { color: t.map(v => (+v.slice(0, 4) < y0 ? C.band : C[zz])) },
      hovertemplate: '%{x|%Y-%m}: %{y:.2f}<extra></extra>' }],
    layout({ title: ttl(T.bsTitle(ZONE[zz])), xaxis: AX('', { type: 'date' }), yaxis: AX(T.eur), showlegend: false, bargap: 0.1,
      shapes: [vline(`${y0}-01-01`, C.navy, 'dash')] }));
    const cy = Object.keys(D.conv[zz]);
    plot('bs-conv', [{ x: cy, y: cy.map(y => D.conv[zz][y]), type: 'bar', marker: { color: C[zz] }, hovertemplate: '%{x}: %{y:.1f}%<extra></extra>' }],
      layout({ title: ttl(T.convTitle(ZONE[zz])), xaxis: AX('', { dtick: 2 }), yaxis: AX('%', { rangemode: 'tozero' }), showlegend: false }));
    const imx = b.indexOf(Math.max(...b)), imn = b.indexOf(Math.min(...b));
    out('bs-out', [T.bs(ZONE[zz], nf(mean(b), 2), nf(sdev(b), 2), nf(sdev(pre), 2), nf(sdev(post), 2), y0),
      T.bs2(nf(b[imx], 2), t[imx], nf(b[imn], 2), t[imn])]);
  }
  draw();
  P('bs-play', 'bs-s', range(2017, 2025, 1), 700);
});

// ---------------------------------------------------------------- 5. Samuelson effect in TTF futures
safe('samuelson', () => {
  const cs = bindToggles('sm-c', draw), w = bindSlider('sm-w', v => v, draw);
  const COL = { '2026-12': C.RO, '2027-01': C.HU, '2027-02': C.BG, '2027-05': C.DE_LU };
  const DASHC = { '2026-12': 'solid', '2027-01': 'dashdot', '2027-02': 'dash', '2027-05': 'dot' };
  const day = s => Date.parse(s + 'T00:00:00Z') / 864e5;
  // daily log returns between consecutive quotes at most 4 calendar days apart
  const R = {};
  Object.keys(COL).forEach(c => {
    const p = D.ttf[c], r = [];
    let prev = -1;
    for (let i = 0; i < p.length; i++) {
      if (p[i] === null) continue;
      if (prev >= 0 && day(D.ttf.t[i]) - day(D.ttf.t[prev]) <= 4) r.push([D.ttf.t[i], Math.log(p[i] / p[prev])]);
      prev = i;
    }
    R[c] = r;
  });
  const end = D.end;
  const from12 = `${+end.slice(0, 4) - 1}-${end.slice(5, 7) === '12' ? '01' : String(+end.slice(5, 7) + 1).padStart(2, '0')}-01`;
  function draw() {
    const k = w(), tr = [], lines = [];
    cs().forEach(c => {
      const r = R[c], x = [], y = [];
      for (let i = k - 1; i < r.length; i++) { x.push(r[i][0]); y.push(100 * Math.sqrt(252) * sdev(r.slice(i - k + 1, i + 1).map(a => a[1]))); }
      tr.push({ x, y, mode: 'lines', name: 'TTF ' + T.month[c], line: { color: COL[c], width: 1.4, dash: DASHC[c] }, hovertemplate: '%{x}: %{y:.1f}%<extra></extra>' });
      const v12 = r.filter(a => a[0] >= from12 && a[0] <= end).map(a => a[1]), v22 = r.filter(a => a[0].startsWith('2022')).map(a => a[1]);
      lines.push(T.sm('TTF ' + T.month[c], nf(100 * Math.sqrt(252) * sdev(v12), 1), v22.length > 2 ? nf(100 * Math.sqrt(252) * sdev(v22), 1) : '–'));
    });
    plot('sm-chart', tr, layout({ title: ttl(T.smTitle(k)), xaxis: AX('', { type: 'date' }), yaxis: AX(T.vol, { rangemode: 'tozero' }) }));
    out('sm-out', lines.length ? lines : ['–']);
  }
  draw();
  P('sm-play', 'sm-w', range(20, 250, 10), 400);
});

// ---------------------------------------------------------------- 6. Black-76, cap and collar
safe('black76-collar', () => {
  const setv = (id, v) => { const e = $(id); e.value = v; e.defaultValue = String(v); };
  setv('bk-F', D.bk.F); setv('bk-r', D.bk.r); setv('bk-T', D.bk.T); setv('bk-s', D.bk.sig);
  const F = bindSlider('bk-F', v => nf(v, 2), draw), s = bindSlider('bk-s', v => nf(v, 2), draw), Td = bindSlider('bk-T', v => v, draw),
    r = bindSlider('bk-r', v => nf(v, 2), draw), kc = bindSlider('bk-c', v => v + '%', draw), kp = bindSlider('bk-p', v => v + '%', draw);
  function b76(f, k, t, rr, sg) {
    const d1 = (Math.log(f / k) + 0.5 * sg * sg * t) / (sg * Math.sqrt(t)), d2 = d1 - sg * Math.sqrt(t), df = Math.exp(-rr * t);
    return { c: df * (f * ncdf(d1) - k * ncdf(d2)), p: df * (k * ncdf(-d2) - f * ncdf(-d1)), dc: df * ncdf(d1), dp: -df * ncdf(-d1), vega: df * f * npdf(d1) * Math.sqrt(t) / 100 };
  }
  function draw() {
    const f = F(), sg = s() / 100, t = Td() / 365.25, rr = r() / 100, Kc = f * kc() / 100, Kp = f * kp() / 100;
    const atm = b76(f, f, t, rr, sg), cap = b76(f, Kc, t, rr, sg), flo = b76(f, Kp, t, rr, sg), g = Math.exp(rr * t);
    const FT = range(0.75 * f, 1.3 * f, f / 200);
    plot('bk-pay', [
      { x: FT, y: FT, mode: 'lines', name: T.unhedged, line: { color: C.grey, width: 1.3 } },
      { x: FT, y: FT.map(() => f), mode: 'lines', name: T.fwd, line: { color: C.HU, width: 1.6 } },
      { x: FT, y: FT.map(v => Math.min(v, Kc) + cap.c * g), mode: 'lines', name: T.cap, line: { color: C.DE_LU, width: 1.6, dash: 'dash' } },
      { x: FT, y: FT.map(v => Math.min(Math.max(v, Kp), Kc) + (cap.c - flo.p) * g), mode: 'lines', name: T.collar, line: { color: C.c7, width: 1.6, dash: 'dashdot' } }],
    layout({ title: ttl(T.payTitle), xaxis: AX(T.FT), yaxis: AX(T.eur), hovermode: 'x unified' }));
    const K = range(0.7 * f, 1.3 * f, f / 150);
    const pr = K.map(k => b76(f, k, t, rr, sg));
    plot('bk-prem', [
      { x: K, y: pr.map(o => o.c), mode: 'lines', name: T.call, line: { color: C.DE_LU, width: 1.8 } },
      { x: K, y: pr.map(o => o.p), mode: 'lines', name: T.put, line: { color: C.RO, width: 1.8 } },
      { x: [Kc, Kp], y: [cap.c, flo.p], mode: 'markers', marker: { color: C.navy, size: 9 }, showlegend: false, hovertemplate: 'K = %{x:.2f}: %{y:.2f}<extra></extra>' }],
    layout({ title: ttl(T.premTitle), xaxis: AX(T.strike), yaxis: AX(T.eur, { rangemode: 'tozero' }), shapes: [vline(f, C.grey, 'dot')] }));
    out('bk-out', [T.bk(nf(atm.c, 2), nf(atm.p, 2), nf(atm.dc, 3), nf(atm.dp, 3), nf(atm.vega, 3)),
      T.bk2(nf(Kc, 2), nf(cap.c, 2), nf(Kp, 2), nf(flo.p, 2), nf(cap.c - flo.p, 2), nf(cap.c * 8760, 0))]);
  }
  draw();
  P('bk-play', 'bk-s', range(5, 100, 1), 150);
});
})();
