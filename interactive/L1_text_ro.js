// Readouts of the Lecture 1 interactive page, written by lectures/L1/build_interactive_L1.py.
window.LK_TEXT = {
 eur: 'EUR/MWh', mw: 'MW', hour: 'Ora zilei (CET)', lag: 'Lag (ore)', acf: 'Autocorelație', year: 'Anul',
 supply: 'Oferta (vînzare)', demand: 'Cererea (cumpărare)', supply0: 'Oferta, publicată', demand0: 'Cererea, publicată',
 qty: 'Cantitatea cumulată (MW)', price: 'Prețul (EUR/MWh)', clearing: 'Punctul de închidere', official: 'Prețul oficial',
 mo: (p, q, p0, q0, dp) => `Prețul de închidere ${p} EUR/MWh la ${q} MW (curbele publicate: ${p0} EUR/MWh la ${q0} MW); variația punctului de mijloc ${dp} EUR/MWh.`,
 range: (a, b) => `orice preț între ${a} și ${b}`,
 mo2: (s, d, a, b) => `Deplasarea curbei ofertei ${s} MW, a curbei cererii ${d} MW. Prețurile oficiale de închidere pe 21 octombrie 2026: ${a} EUR/MWh la amiază, ${b} EUR/MWh seara.`,
 dpTitle: w => w === 1 ? 'Prețul zilnic de bază' : `Prețul zilnic de bază, media mobilă pe ${w % 100 >= 1 && w % 100 <= 19 ? w : w + ' de'} zile`,
 dp: (z, m, s, mx, md, n) => `${z}: media ${m}, abaterea standard ${s}, maximul ${mx} EUR/MWh pe ${md} (${window.EMQAI.cnt(n, 'zi', 'zile')}).`,
 ipTitle: 'Prețul mediu pe oră (EUR/MWh)', ipNorm: 'Ora / media zilei',
 ip: (z, y, s, lo, hlo, hi, hhi, r) => `${z}, ${y}, ${s}: ora cea mai ieftină ${hlo}:00 (${lo} EUR/MWh), cea mai scumpă ${hhi}:00 (${hi} EUR/MWh); raportul 19:00 / 13:00 = ${r}.`,
 season: { all: 'tot anul', win: 'iarna', spr: 'primăvara', sum: 'vara', aut: 'toamna' },
 ngYear: t => `Ore cu prețul sub ${t} EUR/MWh, pe ani`, ngHour: (t, y) => `Ore sub ${t} EUR/MWh în ${y}, pe ora zilei`,
 hours: 'Ore',
 ng: (z, t, y, n, sh, peak) => `${z}, preț sub ${t} EUR/MWh: ${window.EMQAI.cnt(n, 'oră', 'ore')} în ${y}; ${sh} dintre ele între 10:00 și 16:00; ora cea mai frecventă ${peak}:00.`,
 ng0: (z, t, y) => `${z}: nicio oră cu prețul sub ${t} EUR/MWh în ${y}.`,
 partial: y => `${y} se oprește la data-limită a cursului (an incomplet).`,
 asRaw: 'Prețul orar (EUR/MWh)', asTr: 'asinh((p − mediana) / (c · MAD))', count: 'Ore',
 as: (y, n, m, mad, sk0, k0, sk1, k1) => `România ${y}, ${window.EMQAI.cnt(n, 'oră', 'ore')}: mediana ${m}, MAD ${mad} EUR/MWh. Asimetria ${sk0} → ${sk1}; excesul de kurtosis ${k0} → ${k1}.`,
 acTitle: (z, y) => `Funcția de autocorelație (ACF) a prețurilor orare, ${z}, ${y}`,
 ac: (r1, r24, r168, b) => `ρ(1) = ${r1}, ρ(24) = ${r24}, ρ(168) = ${r168}; banda de 95% pentru zgomot alb ±${b}.`
};
