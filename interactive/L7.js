// Lecture 7 interactive page: machine learning and foundation models. Inputs in L7_data.js (lectures/L7/build_interactive_L7.py).
(function () {
'use strict';
const D = window.LK_DATA, T = window.LK_TEXT;
const { C, mean, nf, pct, $, AX, layout, ttl, plot, out, vline, hline, ncdf, bindSlider, bindSelect, bindToggles, Player, range, safe } = window.EMQAI;
const P = (id, input, vals, ms) => new Player(id, $(input), vals, ms);
const COL = { naive: '#8A94A6', aw_arx: C.c8, aw_lear: C.RO, gbm2: C.c5, mlp2: C.c6, xgb: C.BG, dnn: C.c7, bolt: C.HU, chr2: C.DE_LU,
  ens4: '#555555', ens_ldx: C.navy, ens_t4: C.c8, ens_lc: C.c6, ens_t5: C.c5 };
const MON = D.months.map((m, i) => T.months[i] + (i === 0 || m.endsWith('-01') ? ' ' + m.slice(0, 4) : ''));
const L = k => T.lab[k];
// month index of each test day
const dayMonth = [];
D.mon.forEach((n, i) => { for (let k = 0; k < n; k++) dayMonth.push(i); });
const monthMean = a => D.mon.map((_, i) => mean(a.filter((_, d) => dayMonth[d] === i)));

// ---------------------------------------------------------------- 1. early stopping
safe('early-stopping', () => {
  const tr = D.lc.tr, va = D.lc.va, ep = tr.map((_, i) => i + 1);
  const p = bindSlider('lc-p', v => v, draw);
  function stopAt(pat) {
    let best = 0, e = 0;
    for (e = 0; e < va.length; e++) { if (va[e] < va[best]) best = e; if (e - best >= pat) break; }
    return { s: Math.min(e, va.length - 1), b: best };
  }
  function draw() {
    const { s, b } = stopAt(p());
    plot('lc-chart', [
      { x: ep, y: tr, mode: 'lines', name: T.train, line: { color: C.RO, width: 2 } },
      { x: ep, y: va, mode: 'lines', name: T.valid, line: { color: C.DE_LU, width: 2, dash: 'dash' } },
      { x: [b + 1], y: [va[b]], mode: 'markers', name: T.best, marker: { color: C.navy, size: 11 } }
    ], layout({ title: ttl(T.mae), xaxis: AX(T.epoch), yaxis: AX(T.mae), shapes: [vline(s + 1, C.grey, 'dot')],
      annotations: [{ x: s + 1, y: 1, yref: 'paper', text: T.stop, showarrow: false, xanchor: 'left', font: { size: 11, color: C.navy } }] }));
    out('lc-out', [T.lc(p(), s + 1, b + 1, nf(va[b], 2), nf(tr[s], 2), nf(va[s], 2)), T.lcEnd(nf(tr[tr.length - 1], 2), nf(va[va.length - 1], 2))]);
  }
  draw();
  P('lc-play', 'lc-p', range(1, 30, 1), 350);
});

// ---------------------------------------------------------------- 2. monthly MAE
safe('monthly-mae', () => {
  const ms = bindToggles('mm-m', draw), v = bindSelect('mm-v', draw);
  const MM = {}; Object.keys(D.dl).forEach(k => (MM[k] = monthMean(D.dl[k])));
  function draw() {
    const rel = v() === 'rel', base = MM.aw_lear, tr = [], lines = [];
    ms().forEach(k => {
      const y = rel ? MM[k].map((x, i) => x - base[i]) : MM[k];
      tr.push({ x: MON, y, mode: 'lines+markers', name: L(k), line: { color: COL[k], width: k === 'ens_ldx' ? 2.6 : 1.6 }, marker: { size: 5 },
        hovertemplate: '%{x}: %{y:.2f}<extra>' + L(k) + '</extra>' });
      lines.push(k === 'aw_lear' ? T.fh(L(k), nf(mean(D.dl[k]), 2)) : T.mm(L(k), nf(mean(D.dl[k]), 2), MM[k].filter((x, i) => x < base[i]).length));
    });
    plot('mm-chart', tr, layout({ title: ttl(rel ? T.mmRel : T.mmLev), xaxis: AX('', { type: 'category' }), yaxis: AX(T.eur),
      shapes: rel ? [hline(0, C.grey, 'dash')] : [] }));
    out('mm-out', lines.length ? lines : ['–']);
  }
  draw();
});

// ---------------------------------------------------------------- 3. combination weight
safe('combination', () => {
  const pr = bindSelect('cw-p', draw), w = bindSlider('cw-w', x => nf(x, 2), draw);
  function draw() {
    const c = D.cw[+pr()], i = Math.round(w() * 20), ib = c.mae.indexOf(Math.min(...c.mae));
    plot('cw-curve', [
      { x: c.w, y: c.mae, mode: 'lines', name: `${L(c.a)} + ${L(c.b)}`, line: { color: COL[c.b], width: 2 }, showlegend: false },
      { x: [c.w[i]], y: [c.mae[i]], mode: 'markers', marker: { color: C.navy, size: 11 }, showlegend: false, hovertemplate: 'w = %{x}: %{y:.2f}<extra></extra>' }
    ], layout({ title: ttl(T.cwCurve), xaxis: AX(T.cwW), yaxis: AX(T.eur), shapes: [vline(0.5, C.grey, 'dot')] }));
    const d = c.mon[i].map((x, k) => x - c.mon[0][k]);
    plot('cw-month', [{ x: MON, y: d, type: 'bar', marker: { color: d.map(x => (x < 0 ? C.green : C.red)) }, hovertemplate: '%{x}: %{y:.2f}<extra></extra>' }],
      layout({ title: ttl(T.cwMonth.replace('AW-LEAR', L(c.a))), xaxis: AX('', { type: 'category' }), yaxis: AX(T.eur), showlegend: false }));
    out('cw-out', [T.cw(L(c.a), L(c.b), nf(c.w[i], 2), nf(c.mae[i], 2), nf(c.mae[0], 2), nf(c.mae[20], 2), nf(c.r, 2)),
      T.cwBest(nf(c.w[ib], 2), nf(c.mae[ib], 2), nf(c.mae[10], 2)), T.cwMonthN(d.filter(x => x < 0).length)]);
  }
  draw();
  P('cw-play', 'cw-w', range(0, 1, 0.05), 350);
});

// ---------------------------------------------------------------- 4. Diebold-Mariano tests
safe('dm-tests', () => {
  const a = bindSelect('dm-a', draw), b = bindSelect('dm-b', draw), lg = bindSlider('dm-L', v => v, draw);
  const MODELS = [...$('dm-a').options].map(o => o.value);
  // one-sided DM test, H1: model kb more accurate than ka; loss = daily mean absolute error; Newey-West (Bartlett) variance
  function dm(ka, kb, lags) {
    const d = D.dl[ka].map((x, i) => x - D.dl[kb][i]), n = d.length, m = mean(d), x = d.map(v => v - m);
    let v = x.reduce((s, u) => s + u * u, 0) / n;
    for (let k = 1; k <= lags; k++) { let c = 0; for (let t = k; t < n; t++) c += x[t] * x[t - k]; v += 2 * (1 - k / (lags + 1)) * c / n; }
    const s = m / Math.sqrt(v / n);
    return { s, p: 1 - ncdf(s), d };
  }
  function draw() {
    const lags = lg(), ka = a(), kb = b();
    const z = MODELS.map(r => MODELS.map(c => (r === c ? null : Math.min(dm(r, c, lags).p, 0.1))));
    const txt = MODELS.map(r => MODELS.map(c => (r === c ? '' : nf(dm(r, c, lags).p, 3))));
    const labs = MODELS.map(L);
    plot('dm-heat', [{ z, x: labs, y: labs, type: 'heatmap', zmin: 0, zmax: 0.1, text: txt, hovertemplate: '%{y} → %{x}: p = %{text}<extra></extra>',
      colorscale: [[0, '#0b6e2e'], [0.2, '#7fc97f'], [0.4, '#ffe08a'], [0.6, '#f4a259'], [0.8, '#d7301f'], [1, '#5a0000']], colorbar: { thickness: 10, len: 0.8 } }],
    layout({ title: ttl(T.dmHeat), xaxis: AX('', { tickangle: -40, tickfont: { size: 9 }, dtick: 1 }), yaxis: AX('', { autorange: 'reversed', tickfont: { size: 9 }, dtick: 1 }),
      margin: { l: 150, r: 10, t: 30, b: 120 },
      shapes: ka !== kb ? [{ type: 'rect', xref: 'x', yref: 'y', x0: MODELS.indexOf(kb) - 0.5, x1: MODELS.indexOf(kb) + 0.5, y0: MODELS.indexOf(ka) - 0.5, y1: MODELS.indexOf(ka) + 0.5, line: { color: C.navy, width: 3 } }] : [] }));
    if (ka === kb) { plot('dm-cum', [], layout({ title: ttl(T.dmCum) })); out('dm-out', [T.dmSame]); return; }
    const r = dm(ka, kb, lags);
    let s = 0; const cum = r.d.map(v => (s += v));
    const t0 = new Date(D.t0 + 'T00:00:00Z'), x = cum.map((_, i) => new Date(t0.getTime() + i * 864e5).toISOString().slice(0, 10));
    plot('dm-cum', [{ x, y: cum, mode: 'lines', line: { color: COL[kb], width: 2 }, showlegend: false, hovertemplate: '%{x}: %{y:.1f}<extra></extra>' }],
      layout({ title: ttl(T.dmCum), xaxis: AX('', { type: 'date' }), yaxis: AX(T.eur), shapes: [hline(0, C.grey, 'dash')] }));
    out('dm-out', [T.dm(L(ka), L(kb), nf(mean(D.dl[ka]), 2), nf(mean(D.dl[kb]), 2), nf(r.s, 2), nf(r.p, 4)), r.p < 0.05 ? T.dmYes : T.dmNo]);
  }
  draw();
});

// ---------------------------------------------------------------- 5. foundation models by hour
safe('foundation', () => {
  const ms = bindToggles('fh-m', draw), se = bindSelect('fh-s', draw);
  const SEL = { all: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], q1: [0, 1, 2], q2: [3, 4, 5], q3: [6, 7, 8], q4: [9, 10, 11] };
  const H = Array.from({ length: 24 }, (_, i) => i);
  // day-weighted mean over the chosen months
  const byHour = (k, mm) => { const n = mm.reduce((s, i) => s + D.mon[i], 0); return H.map(h => mm.reduce((s, i) => s + D.fh[k][i][h] * D.mon[i], 0) / n); };
  function draw() {
    const mm = SEL[se()], tr = [], lines = [];
    ms().forEach(k => {
      const y = byHour(k, mm);
      tr.push({ x: H, y, mode: 'lines+markers', name: L(k), line: { color: COL[k], width: k === 'chr2' ? 2.6 : 1.6 }, marker: { size: 4 } });
      lines.push(T.fh(L(k), nf(mean(y), 2)));
    });
    plot('fh-mae', tr, layout({ title: ttl(T.fhMae), xaxis: AX(T.hour, { dtick: 3 }), yaxis: AX(T.eur) }));
    const n = mm.reduce((s, i) => s + D.mon[i], 0);
    const cov = H.map(h => 100 * mm.reduce((s, i) => s + D.fh.cov[i][h], 0) / n);
    plot('fh-cov', [{ x: H, y: cov, type: 'bar', marker: { color: C.DE_LU }, showlegend: false, hovertemplate: '%{x}:00: %{y:.1f}%<extra></extra>' }],
      layout({ title: ttl(T.fhCov), xaxis: AX(T.hour, { dtick: 3 }), yaxis: AX(T.share, { range: [0, 100] }), shapes: [hline(80, C.navy, 'dash')] }));
    const c2 = byHour('chr2', mm), lr = byHour('aw_lear', mm);
    lines.push(T.fhWin(H.filter(h => c2[h] < lr[h]).length), T.fhCovT(nf(mean(cov), 1) + '%'));
    out('fh-out', lines);
  }
  draw();
});

// ---------------------------------------------------------------- 6. spike classifier and cost-loss decision
safe('spike-decision', () => {
  const mdl = bindSelect('sd-m', draw), th = bindSlider('sd-t', v => nf(v, 2), draw), cc = bindSlider('sd-c', v => v, draw);
  const A = D.sd.a, TH = D.sd.th, N = A.length;
  const Y = A.map((v, i) => (v > TH[Math.floor(i / 24)] ? 1 : 0)), NP = Y.reduce((s, y) => s + y, 0), NN = N - NP;
  const EX = A.map((v, i) => v - TH[Math.floor(i / 24)]);           // excess over the spike threshold, EUR/MWh
  const CUTS = range(0.02, 0.98, 0.02);
  const rocs = {};
  function roc(k) {            // full ROC curve and AUC from the sorted scores
    if (rocs[k]) return rocs[k];
    const s = D.sd[k], idx = s.map((_, i) => i).sort((i, j) => s[j] - s[i]);
    const fx = [0], fy = [0]; let tp = 0, fp = 0, auc = 0;
    for (let q = 0; q < N;) {
      let r = q; while (r < N && s[idx[r]] === s[idx[q]]) { Y[idx[r]] ? tp++ : fp++; r++; }
      const x = fp / NN, y = tp / NP; auc += (x - fx[fx.length - 1]) * (y + fy[fy.length - 1]) / 2; fx.push(x); fy.push(y); q = r;
    }
    return (rocs[k] = { fx, fy, auc });
  }
  const at = (k, cut, C0) => {
    const s = D.sd[k]; let n = 0, tp = 0, v = 0;
    for (let i = 0; i < N; i++) if (s[i] > cut) { n++; tp += Y[i]; v += EX[i] - C0; }
    return { n, tp, fp: n - tp, fn: NP - tp, v: v / 1000 };
  };
  function draw() {
    const k = mdl(), cut = th(), C0 = cc(), cl = C0 / D.sd.lbar, r = roc(k), m = at(k, cut, C0), mc = at(k, cl, C0);
    let vp = 0; EX.forEach(e => { if (e - C0 > 0) vp += e - C0; });
    const name = $('sd-m').selectedOptions[0].textContent;
    plot('sd-roc', [
      { x: r.fx, y: r.fy, mode: 'lines', name, line: { color: C.BG, width: 2 }, showlegend: false, hoverinfo: 'skip' },
      { x: [0, 1], y: [0, 1], mode: 'lines', line: { color: C.grey, width: 1, dash: 'dot' }, showlegend: false, hoverinfo: 'skip' },
      { x: [m.fp / NN], y: [m.tp / NP], mode: 'markers', name: T.point, marker: { color: C.navy, size: 11 }, showlegend: false,
        hovertemplate: 'FPR %{x:.3f}, TPR %{y:.3f}<extra></extra>' }
    ], layout({ title: ttl(T.roc), xaxis: AX(T.fpr, { range: [0, 1] }), yaxis: AX(T.tpr, { range: [0, 1] }) }));
    const VC = CUTS.map(c => at(k, c, C0).v);
    plot('sd-val', [{ x: CUTS, y: VC, mode: 'lines', line: { color: C.BG, width: 2 }, showlegend: false, hovertemplate: '%{x:.2f}: %{y:.1f}<extra></extra>' },
      { x: [cut], y: [m.v], mode: 'markers', marker: { color: C.navy, size: 11 }, showlegend: false, hoverinfo: 'skip' }],
    layout({ title: ttl(T.val), xaxis: AX(T.thr, { range: [0, 1] }), yaxis: AX(''), shapes: [vline(cl, C.DE_LU, 'dash')],
      annotations: [{ x: cl, y: 1, yref: 'paper', text: T.cl, showarrow: false, xanchor: 'left', font: { size: 11, color: C.DE_LU } }] }));
    out('sd-out', [T.spikes(NP, nf(Math.min(...TH), 1), nf(Math.max(...TH), 1)),
      T.sd(name, nf(cut, 2), nf(r.auc, 3), m.n, m.tp, m.fp, m.fn),
      T.sd2(nf(m.v, 1), C0, nf(cl, 3), nf(mc.v, 1), nf(vp / 1000, 1))]);
  }
  draw();
  P('sd-play', 'sd-t', CUTS, 300);
});
})();
