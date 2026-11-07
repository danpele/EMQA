// Readouts of the Lecture 3 interactive page, written by lectures/L3/build_interactive_L3.py.
window.LK_TEXT = {
 unit: { pct: '%', eur: 'EUR/MWh' }, lag: 'Lagul (zile)', acf: 'Autocorelația',
 e: 'Șocurile ε_t', e2: 'Pătratul șocurilor ε_t²', band: 'Banda de 95% în lipsa autocorelației',
 cl: (y0, n, a1, a2, q1, q2) => `Eșantion din ${y0} pînă la data-limită, ${window.EMQAI.cnt(n, 'zi', 'zile')}: ρ₁(ε) = ${a1}, ρ₁(ε²) = ${a2}. Ljung–Box Q(10): ${q1} pentru șocuri, ${q2} pentru pătratul șocurilor (valoarea critică la 5%: 18,3).`,
 z: 'Șocul standardizat z_t', dens: 'Densitatea (scară logaritmică)', hist: 'Șocuri standardizate cu GARCH, România (%)', normal: 'Normală', stud: nu => `Student-t, ν = ${nu}`,
 ft: (k, n, N, en, et) => `|z| > ${k}: ${n} din ${N} șocuri observate; așteptate ${en} sub repartiția normală, ${et} sub Student-t.`,
 sig: u => `Volatilitatea condiționată σ_t (${u})`, roll: 'Abaterea standard mobilă pe 30 de zile', garch: 'GARCH(1,1), filtru calculat în browser',
 gf: (a, b, p, hl, s, om) => `α = ${a}, β = ${b}: persistența ${p}, timpul de înjumătățire ${hl}; σ de lungă durată = ${s} (fixat la estimația sa, ω = ${om}).`,
 gf2: (ll, ll0, mx, md) => `Log-verosimilitatea Student-t ${ll} (la estimații: ${ll0}). Cel mai mare σ_t: ${mx} pe ${md}.`,
 days: x => `${x} zile`, inf: 'infinit (fără revenire la medie)',
 left: '% rămas din șoc', after: 'Zile după șoc',
 you: 'Persistența aleasă',
 hl2: (p, h, d10) => `Persistența ${p}: timpul de înjumătățire ${h} zile; la 10 zile după șoc mai rămîne ${d10} din el.`,
 shock: u => `Șocul ε_(t−1), ${u}`, next: u => `σ_t de a doua zi, ${u}`, fall: 'GJR: prețul a scăzut ieri', rise: 'GJR: prețul a crescut ieri', sym: 'GARCH simetric (γ = 0)',
 ni: (u, s2, dn, up, r) => `Șoc de ±2 abateri standard (±${s2} ${u}): σ de a doua zi ${dn} după o scădere, ${up} după o creștere (raportul ${r}).`,
 ni2: (p) => `Persistența α + γ/2 + β = ${p}; ω și β sînt fixați la estimațiile lor, iar varianța de ieri la nivelul de lungă durată.`,
 price: 'Prețul zilnic de bază (EUR/MWh)', bandL: c => `Banda de ${c}%, stabilită în t−1`, outside: 'În afara benzii',
 fb: (c, n, N, sh, w) => `Banda de ${c}%: ${n} din ${N} zile în afară (${sh}, nominal ${window.EMQAI.nf(100 - c, 0)}%); lățimea medie ±${w} EUR/MWh.`,
 fb2: (a, b) => `În afara benzii înainte de 1 mai 2026: ${a}; de la 1 mai 2026: ${b}.`
};
