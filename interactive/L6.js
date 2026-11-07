// Lecture 6 interactive page: renewables, negative prices and batteries. Inputs in L6_data.js (lectures/L6/build_interactive_L6.py).
(function () {
'use strict';
const D = window.LK_DATA, T = window.LK_TEXT;
const { LANG, C, SERIES, ZONE, DASH, MONTHS, mean, nf, pct, $, AX, layout, ttl, plot, out, hline, vline,
  bindSlider, bindSelect, bindToggles, Player, range, safe } = window.EMQAI;
const players = [];
const P = (id, input, vals, ms) => players.push(new Player(id, $(input), vals, ms));
const YEND = +D.end.slice(0, 4);
const YCOL = { 2023: C.grey, 2024: C.HU, 2025: C.c7, 2026: C.RO };
// simple least squares y = a + b x; returns {a, b, se, r2}
function ols(x, y) {
  const n = x.length, mx = mean(x), my = mean(y);
  let sxx = 0, sxy = 0, syy = 0;
  for (let i = 0; i < n; i++) { sxx += (x[i] - mx) ** 2; sxy += (x[i] - mx) * (y[i] - my); syy += (y[i] - my) ** 2; }
  const b = sxy / sxx, a = my - b * mx, sse = syy - b * sxy;
  return { a, b, se: Math.sqrt(sse / (n - 2) / sxx), r2: 1 - sse / syy };
}
const sign = (x, d) => (x >= 0 ? '+' : '') + nf(x, d);

// ---------------------------------------------------------------- 1. price vs residual load
safe('resid-price', () => {
  const ys = bindToggles('rp-y', draw), h = bindSelect('rp-h', draw), bw = bindSlider('rp-b', v => nf(v, 2), draw);
  const keep = { all: () => true, mid: x => x >= 11 && x < 15, eve: x => x >= 18 && x < 22 };
  function draw() {
    const w = bw(), f = keep[h()], tr = [], lines = [];
    ys().forEach(y => {
      const e = D.rp[y], r = [], p = [];
      e.r.forEach((v, i) => { if (f(e.h[i])) { r.push(v); p.push(e.p[i]); } });
      if (r.length < 30) return;
      const bins = {};
      r.forEach((v, i) => { const k = Math.floor(v / w); (bins[k] = bins[k] || []).push(p[i]); });
      const ks = Object.keys(bins).map(Number).filter(k => bins[k].length >= 20).sort((a, b) => a - b);
      tr.push({ x: ks.map(k => (k + 0.5) * w), y: ks.map(k => mean(bins[k])), mode: 'lines+markers', name: y, line: { color: YCOL[y], width: 2 },
        marker: { size: 6 }, hovertemplate: '%{x:.2f} GW: %{y:.1f} EUR/MWh<extra>' + y + '</extra>' });
      const o = ols(r, p), lo = p.filter((_, i) => r[i] < 2), hi = p.filter((_, i) => r[i] > 6);
      lines.push(T.rp(y, r.length, nf(o.b, 1), pct(lo.length / r.length, 1), lo.length ? nf(mean(lo), 1) : '–',
        pct(hi.length / r.length, 1), hi.length ? nf(mean(hi), 1) : '–'));
    });
    plot('rp-chart', tr, layout({ title: ttl(T.rpTitle), xaxis: AX(T.resid), yaxis: AX(T.price), shapes: [hline(0, C.band, 'dot')] }));
    out('rp-out', lines.length ? lines : ['–']);
    if (ys().map(Number).includes(YEND)) $('rp-out').insertAdjacentHTML('beforeend', `<li>${T.partial(YEND)}</li>`);
  }
  draw();
});

// ---------------------------------------------------------------- 2. capture rates by year
safe('capture-rates', () => {
  const t = bindSelect('cr-t', draw), zs = bindToggles('cr-z', draw), m = bindSelect('cr-m', draw);
  function draw() {
    const tech = t(), mode = m(), tr = [], tp = [], lines = [];
    zs().forEach(z => {
      const e = D.cr[z] && D.cr[z][tech]; if (!e) return;
      const yrs = Object.keys(e), v = yrs.map(y => (mode === 'cr' ? 100 * e[y][3] : e[y][1] - e[y][0]));
      tr.push({ x: yrs, y: v, mode: 'lines+markers', name: ZONE[z], line: { color: C[z], dash: DASH[z], width: 2 }, marker: { size: 6 },
        hovertemplate: '%{x}: %{y:.1f}<extra>' + ZONE[z] + '</extra>' });
      tp.push({ x: yrs, y: yrs.map(y => e[y][0]), mode: 'lines+markers', name: ZONE[z] + ', ' + T.capture, line: { color: C[z], width: 2 }, marker: { size: 5 } });
      tp.push({ x: yrs, y: yrs.map(y => e[y][1]), mode: 'lines', name: ZONE[z] + ', ' + T.base, line: { color: C[z], width: 1.2, dash: 'dot' } });
      const y = yrs[yrs.length - 2] || yrs[yrs.length - 1], q = e[y];
      lines.push(T.cr(ZONE[z], T.tech[tech], y, nf(q[0], 1), nf(q[1], 1), pct(q[3], 1), nf(q[2], 2)));
      const ql = e[yrs[yrs.length - 1]];
      lines.push(T.cr(ZONE[z], T.tech[tech], yrs[yrs.length - 1], nf(ql[0], 1), nf(ql[1], 1), pct(ql[3], 1), nf(ql[2], 2)));
    });
    plot('cr-chart', tr, layout({ title: ttl(T.crTitle[mode]), xaxis: AX(T.year, { type: 'category' }), yaxis: AX(''),
      shapes: mode === 'cr' ? [hline(100, C.band, 'dash')] : [hline(0, C.band, 'dash')] }));
    plot('cr-px', tp, layout({ title: ttl(T.crPx), xaxis: AX(T.year, { type: 'category' }), yaxis: AX(T.eur), showlegend: false }));
    lines.push(T.partial(YEND));
    out('cr-out', lines.length > 1 ? lines : ['–']);
  }
  draw();
});

// ---------------------------------------------------------------- 3. cannibalisation: monthly capture rate vs solar share
safe('cannibal', () => {
  const z = bindSelect('cn-z', draw), y0 = bindSlider('cn-y0', v => v, draw), y1 = bindSlider('cn-y1', v => v, draw);
  const mlab = s => `${MONTHS[+s.slice(5, 7) - 1]} ${s.slice(0, 4)}`;
  function draw() {
    const zz = z(), a = Math.min(y0(), y1()), b = Math.max(y0(), y1());
    const rows = D.cn[zz].filter(r => +r[0].slice(0, 4) >= a && +r[0].slice(0, 4) <= b);
    const rest = D.cn[zz].filter(r => !rows.includes(r));
    const tr = [{ x: rest.map(r => r[2]), y: rest.map(r => r[1]), mode: 'markers', name: '', marker: { color: C.band, size: 6 }, showlegend: false,
      text: rest.map(r => mlab(r[0])), hovertemplate: '%{text}: %{x:.1f}%, %{y:.1f}%<extra></extra>' },
    { x: rows.map(r => r[2]), y: rows.map(r => r[1]), mode: 'markers', name: ZONE[zz], marker: { color: C[zz], size: 7 },
      text: rows.map(r => mlab(r[0])), hovertemplate: '%{text}: %{x:.1f}%, %{y:.1f}%<extra></extra>' }];
    const lines = [];
    if (rows.length >= 6) {
      const o = ols(rows.map(r => r[2]), rows.map(r => r[1])), xs = rows.map(r => r[2]), x0 = Math.min(...xs), x1 = Math.max(...xs);
      tr.push({ x: [x0, x1], y: [o.a + o.b * x0, o.a + o.b * x1], mode: 'lines', name: 'OLS', line: { color: C.navy, width: 2, dash: 'dash' } });
      lines.push(T.cn(ZONE[zz], rows.length, sign(o.b, 2).replace(/^\+/, '+ ').replace(/^−/, '− '), nf(o.se, 2), nf(o.a, 1), nf(o.r2, 2)));
      const mn = rows.reduce((p, r) => (r[1] < p[1] ? r : p)), mx = rows.reduce((p, r) => (r[2] > p[2] ? r : p));
      lines.push(T.cnMin(mlab(mn[0]), pct(mn[1] / 100, 1), mlab(mx[0]), pct(mx[2] / 100, 1)));
    } else lines.push('–');
    plot('cn-chart', tr, layout({ xaxis: AX(T.cnX, { rangemode: 'tozero' }), yaxis: AX(T.cnY), shapes: [hline(100, C.band, 'dot')] }));
    out('cn-out', lines);
  }
  draw();
  P('cn-play', 'cn-y0', range(2019, 2025, 1), 900);
});

// ---------------------------------------------------------------- 4. negative prices: month x hour heat map
safe('neg-hours', () => {
  const z = bindSelect('nh-z', draw), y = bindSlider('nh-y', v => v, draw);
  const H = Array.from({ length: 24 }, (_, i) => i);
  function draw() {
    const zz = z(), yy = y(), e = D.nh[zz][yy];
    const tot = e.h.map(r => r.reduce((a, b) => a + b, 0)), n = tot.reduce((a, b) => a + b, 0);
    plot('nh-heat', [{ z: e.h, x: H, y: MONTHS, type: 'heatmap', colorscale: [[0, '#ffffff'], [0.15, '#c6dbef'], [0.5, '#4a90d9'], [1, C.blue]],
      zmin: 0, hovertemplate: '%{y}, %{x}:00: %{z:.2f} h<extra></extra>', colorbar: { thickness: 10, len: 0.8 } }],
    layout({ title: ttl(T.nhTitle(yy)), xaxis: AX(T.hour, { dtick: 3 }), yaxis: AX('', { autorange: 'reversed' }), margin: { l: 44, r: 8, t: 30, b: 40 } }));
    plot('nh-depth', [{ x: MONTHS, y: tot, type: 'bar', name: T.nhHours, marker: { color: C[zz] }, hovertemplate: '%{x}: %{y:.1f} h<extra></extra>' },
      { x: MONTHS, y: e.d, mode: 'lines+markers', name: T.nhMean, yaxis: 'y2', line: { color: C.navy, width: 1.5 }, marker: { size: 6 },
        hovertemplate: '%{x}: %{y:.1f} EUR/MWh<extra></extra>' }],
    layout({ title: ttl(T.nhDepth), xaxis: AX(''), yaxis: AX('h'), yaxis2: AX('EUR/MWh', { overlaying: 'y', side: 'right', showgrid: false }),
      margin: { l: 48, r: 52, t: 30, b: 40 } }));
    const lines = [];
    if (n > 0) {
      const byH = H.map(h => e.h.reduce((a, r) => a + r[h], 0)), mid = byH.slice(10, 16).reduce((a, b) => a + b, 0);
      let sw = 0, sp = 0; e.d.forEach((v, i) => { if (v !== null) { sw += tot[i]; sp += v * tot[i]; } });
      lines.push(T.nh(ZONE[zz], yy, window.EMQAI.cnt(n, LANG === 'ro' ? 'oră' : 'hour', LANG === 'ro' ? 'ore' : 'hours', 2), byH.indexOf(Math.max(...byH)),
        MONTHS[tot.indexOf(Math.max(...tot))], pct(mid / n, 0), nf(sp / sw, 1)));
    } else lines.push(T.nh0(ZONE[zz], yy));
    if (yy === YEND) lines.push(T.partial(yy));
    out('nh-out', lines);
  }
  draw();
  P('nh-play', 'nh-y', range(2022, YEND, 1), 900);
});

// ---------------------------------------------------------------- 5. battery arbitrage revenue
safe('battery', () => {
  const z = bindSelect('bt-z', draw), e = bindSelect('bt-e', draw), eta = bindSlider('bt-eta', v => v + '%', draw), y = bindSlider('bt-y', v => v, draw);
  const AF = (1 - Math.pow(1.08, -15)) / 0.08;
  function draw() {
    const zz = z(), E = e(), k = D.bt.etas.indexOf(eta()), yy = y(), V = D.bt.v[zz], yrs = Object.keys(V);
    const tr = D.bt.durs.map((d, i) => ({ x: yrs, y: yrs.map(yr => V[yr][d][k]), mode: 'lines+markers', name: d + ' h',
      line: { color: SERIES[i], width: String(d) === E ? 3 : 1.5 }, marker: { size: String(d) === E ? 7 : 4 }, hovertemplate: '%{x}: %{y:.1f}<extra>' + d + ' h</extra>' }));
    plot('bt-years', tr, layout({ title: ttl(T.btYears(E, eta() + '%')), xaxis: AX(T.year, { type: 'category' }), yaxis: AX(T.kEUR, { rangemode: 'tozero' }),
      shapes: [{ type: 'rect', xref: 'x', yref: 'paper', x0: yrs.indexOf(String(yy)) - 0.4, x1: yrs.indexOf(String(yy)) + 0.4, y0: 0, y1: 1, fillcolor: 'rgba(197,210,232,0.35)', line: { width: 0 } }] }));
    const ve = V[yy];
    if (!ve) { out('bt-out', ['–']); return; }
    plot('bt-eff', D.bt.durs.map((d, i) => ({ x: D.bt.etas, y: ve[d], mode: 'lines+markers', name: d + ' h', line: { color: SERIES[i], width: String(d) === E ? 3 : 1.5 },
      hovertemplate: '%{x}%: %{y:.1f}<extra>' + d + ' h</extra>' })),
    layout({ title: ttl(T.btEff(yy)), xaxis: AX(T.eff, { dtick: 5 }), yaxis: AX(T.kEUR, { rangemode: 'tozero' }), shapes: [vline(eta(), C.grey, 'dash')] }));
    const r = ve[E][k], n = ve.n;
    const lines = [T.bt(ZONE[zz], yy, E, eta() + '%', nf(r, 1), nf(1000 * r / n, 0), nf(1000 * r / n / E, 0), n),
      T.bt2(nf(ve[4][k] / ve[2][k], 2), nf(AF, 2), nf(r * AF * 365 / n, 0))];
    if (yy === YEND) lines.push(T.partial(yy));
    out('bt-out', lines);
  }
  draw();
  P('bt-play', 'bt-eta', range(75, 95, 5), 700);
});

// ---------------------------------------------------------------- 6. summer 2026: Romania - Bulgaria
safe('rogb', () => {
  const R = D.rg, nd = R.days.length;
  const fmtD = i => R.days[i];
  const d0 = bindSlider('rg-d0', fmtD, draw), d1 = bindSlider('rg-d1', fmtD, draw), bs = bindToggles('rg-b', draw), pm = bindSelect('rg-p', draw);
  const H = Array.from({ length: 24 }, (_, i) => i);
  const BCOL = { sum: C.RO, bulgaria: C.BG, hungary: C.HU, serbia: C.c7 }, BD = { sum: 'solid', bulgaria: 'dash', hungary: 'dashdot', serbia: 'dot' };
  const hm = (M, a, b) => H.map(h => { let s = 0, n = 0; for (let i = a; i <= b; i++) { const v = M[i][h]; if (v !== null) { s += v; n++; } } return n ? s / n : null; });
  function draw() {
    const a = Math.min(d0(), d1()), b = Math.max(d0(), d1());
    const tf = bs().map(k => ({ x: H, y: hm(R[k], a, b), mode: 'lines+markers', name: T.border[k], line: { color: BCOL[k], dash: BD[k], width: 2 }, marker: { size: 4 },
      hovertemplate: '%{x}:00: %{y:.0f} MW<extra>' + T.border[k] + '</extra>' }));
    plot('rg-flow', tf, layout({ title: ttl(T.rgFlow), xaxis: AX(T.hourRO, { dtick: 3 }), yaxis: AX('MW'), shapes: [hline(0, C.navy, 'solid')] }));
    const pro = hm(R.RO, a, b), pbg = hm(R.BG, a, b);
    if (pm() === 'lev') {
      plot('rg-price', [{ x: H, y: pro, mode: 'lines+markers', name: T.ro, line: { color: C.RO, width: 2 }, marker: { size: 4 } },
        { x: H, y: pbg, mode: 'lines+markers', name: T.bg, line: { color: C.BG, width: 2, dash: 'dash' }, marker: { size: 4 } }],
      layout({ title: ttl(T.rgLev), xaxis: AX(T.hourRO, { dtick: 3 }), yaxis: AX(T.eur) }));
    } else {
      const g = H.map(h => (pro[h] !== null && pbg[h] !== null ? pro[h] - pbg[h] : null));
      plot('rg-price', [{ x: H, y: g, type: 'bar', name: T.gap, marker: { color: g.map(v => (v >= 0 ? C.RO : C.BG)) }, hovertemplate: '%{x}:00: %{y:.1f}<extra></extra>' }],
        layout({ title: ttl(T.rgGap), xaxis: AX(T.hourRO, { dtick: 3 }), yaxis: AX(T.eur), showlegend: false }));
    }
    const s = hm(R.sum, a, b), bg = hm(R.bulgaria, a, b);
    const mn = Math.min(...s), mx = Math.max(...s), hb = bg.indexOf(Math.max(...bg));
    let ne = 0;
    for (let i = a; i <= b; i++) { const v = [19, 20, 21, 22].map(h => R.bulgaria[i][h]).filter(x => x !== null); if (v.length && mean(v) > 0) ne++; }
    out('rg-out', [T.rg(R.days[a], R.days[b], b - a + 1, s.indexOf(mn), nf(-mn, 0), s.indexOf(mx), nf(mx, 0)),
      T.rg2(hb, nf(bg[hb], 0), T.rgDays(ne), nf(pro[hb], 1), nf(pbg[hb], 1))]);
  }
  draw();
  P('rg-play', 'rg-d0', range(0, 84, 7), 700);
});
})();
