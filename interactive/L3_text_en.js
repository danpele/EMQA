// Readouts of the Lecture 3 interactive page, written by lectures/L3/build_interactive_L3.py.
window.LK_TEXT = {
 unit: { pct: '%', eur: 'EUR/MWh' }, lag: 'Lag (days)', acf: 'Autocorrelation',
 e: 'Shocks ε_t', e2: 'Squared shocks ε_t²', band: '95% band if no autocorrelation',
 cl: (y0, n, a1, a2, q1, q2) => `Sample ${y0} to the cut-off, ${window.EMQAI.cnt(n, 'day', 'days')}: ρ₁(ε) = ${a1}, ρ₁(ε²) = ${a2}. Ljung–Box Q(10): ${q1} for the shocks, ${q2} for the squared shocks (5% critical value 18.3).`,
 z: 'Standardised shock z_t', dens: 'Density (log scale)', hist: 'GARCH-standardised shocks, Romania (%)', normal: 'Normal', stud: nu => `Student-t, ν = ${nu}`,
 ft: (k, n, N, en, et) => `|z| > ${k}: ${n} of ${N} shocks observed; expected ${en} under the normal, ${et} under the Student-t.`,
 sig: u => `Conditional volatility σ_t (${u})`, roll: '30-day rolling standard deviation', garch: 'GARCH(1,1), filter in the browser',
 gf: (a, b, p, hl, s, om) => `α = ${a}, β = ${b}: persistence ${p}, half-life ${hl}; long-run σ = ${s} (held at its estimate, ω = ${om}).`,
 gf2: (ll, ll0, mx, md) => `Student-t log-likelihood ${ll} (at the estimates: ${ll0}). Highest σ_t: ${mx} on ${md}.`,
 days: x => `${x} days`, inf: 'infinite (no mean reversion)',
 left: '% of the shock left', after: 'Days after the shock',
 you: 'Your persistence',
 hl2: (p, h, d10) => `Persistence ${p}: half-life ${h} days; 10 days after the shock ${d10} of it is left.`,
 shock: u => `Shock ε_(t−1), ${u}`, next: u => `Next-day σ_t, ${u}`, fall: 'GJR: price fell yesterday', rise: 'GJR: price rose yesterday', sym: 'Symmetric GARCH (γ = 0)',
 ni: (u, s2, dn, up, r) => `Shock of ±2 standard deviations (±${s2} ${u}): next-day σ ${dn} after a fall, ${up} after a rise (ratio ${r}).`,
 ni2: (p) => `Persistence α + γ/2 + β = ${p}; ω and β are held at their estimates and yesterday's variance at the long-run level.`,
 price: 'Daily base price (EUR/MWh)', bandL: c => `${c}% band, set on t−1`, outside: 'Outside the band',
 fb: (c, n, N, sh, w) => `${c}% band: ${n} of ${N} days outside (${sh}, nominal ${window.EMQAI.nf(100 - c, 0)}%); mean width ±${w} EUR/MWh.`,
 fb2: (a, b) => `Outside the band before 1 May 2026: ${a}; from 1 May 2026: ${b}.`
};
