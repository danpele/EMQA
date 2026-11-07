// Readouts of the Lecture 1 interactive page, written by lectures/L1/build_interactive_L1.py.
window.LK_TEXT = {
 eur: 'EUR/MWh', mw: 'MW', hour: 'Hour of the day (CET)', lag: 'Lag (hours)', acf: 'Autocorrelation', year: 'Year',
 supply: 'Supply (sell offers)', demand: 'Demand (buy bids)', supply0: 'Supply, published', demand0: 'Demand, published',
 qty: 'Cumulative quantity (MW)', price: 'Price (EUR/MWh)', clearing: 'Clearing point', official: 'Official price',
 mo: (p, q, p0, q0, dp) => `Clearing price ${p} EUR/MWh at ${q} MW (published curves: ${p0} EUR/MWh at ${q0} MW); change of the mid-point ${dp} EUR/MWh.`,
 range: (a, b) => `any price from ${a} to ${b}`,
 mo2: (s, d, a, b) => `Shift of the supply curve ${s} MW, of the demand curve ${d} MW. Official clearing prices on 21 October 2026: ${a} EUR/MWh at midday, ${b} EUR/MWh in the evening.`,
 dpTitle: w => w === 1 ? 'Daily base price' : `Daily base price, ${w}-day moving average`,
 dp: (z, m, s, mx, md, n) => `${z}: mean ${m}, standard deviation ${s}, maximum ${mx} EUR/MWh on ${md} (${window.EMQAI.cnt(n, 'day', 'days')}).`,
 ipTitle: 'Mean price by hour (EUR/MWh)', ipNorm: 'Hour / daily mean',
 ip: (z, y, s, lo, hlo, hi, hhi, r) => `${z}, ${y}, ${s}: cheapest hour ${hlo}:00 (${lo} EUR/MWh), most expensive ${hhi}:00 (${hi} EUR/MWh); ratio 19:00 / 13:00 = ${r}.`,
 season: { all: 'whole year', win: 'winter', spr: 'spring', sum: 'summer', aut: 'autumn' },
 ngYear: t => `Hours with a price below ${t} EUR/MWh, by year`, ngHour: (t, y) => `Hours below ${t} EUR/MWh in ${y}, by hour of the day`,
 hours: 'Hours',
 ng: (z, t, y, n, sh, peak) => `${z}, price below ${t} EUR/MWh: ${window.EMQAI.cnt(n, 'hour', 'hours')} in ${y}; ${sh} of them between 10:00 and 16:00; most frequent hour ${peak}:00.`,
 ng0: (z, t, y) => `${z}: no hour with a price below ${t} EUR/MWh in ${y}.`,
 partial: y => `${y} runs to the cut-off of the lecture (partial year).`,
 asRaw: 'Hourly price (EUR/MWh)', asTr: 'asinh((p − median) / (c · MAD))', count: 'Hours',
 as: (y, n, m, mad, sk0, k0, sk1, k1) => `Romania ${y}, ${window.EMQAI.cnt(n, 'hour', 'hours')}: median ${m}, MAD ${mad} EUR/MWh. Skewness ${sk0} → ${sk1}; excess kurtosis ${k0} → ${k1}.`,
 acTitle: (z, y) => `Autocorrelation function (ACF) of hourly prices, ${z}, ${y}`,
 ac: (r1, r24, r168, b) => `ρ(1) = ${r1}, ρ(24) = ${r24}, ρ(168) = ${r168}; 95% band for white noise ±${b}.`
};
