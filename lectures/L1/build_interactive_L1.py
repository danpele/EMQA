"""Build the interactive page of Lecture 1 (Energy markets and their data): interactive/L1.html (EN) and interactive/L1_ro.html (RO).

Inputs (interactive/L1_data.js) are computed here from data/clean (OPCOM PZU curves, day-ahead prices); the page logic is in
interactive/L1.js. Run: python3 lectures/L1/build_interactive_L1.py [--no-data]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import interactive_common  # noqa: E402
from interactive_common import slider, select, toggles, play, charts, rnd, csv, cutoff, DATA  # noqa: E402

K = 1
ZONES = ['RO', 'BG', 'HU', 'DE_LU']

# (anchor, chart file / Quantlet, section key, id prefix)
BLOCKS = [('merit-order', 'merit_opcom', 'mkt', 'mo'),
          ('daily-prices', 'prices_daily_4zones', 'facts', 'dp'),
          ('intraday-profile', 'profile_intraday', 'facts', 'ip'),
          ('negative-prices', 'negative_prices', 'facts', 'ng'),
          ('asinh', 'asinh_ro', 'facts', 'as'),
          ('acf-hourly', 'acf_ro_hourly', 'tool', 'ac')]

SECTIONS = {
 'en': dict(mkt='Power markets in Romania and Europe', facts='Energy data and stylized facts', tool='Time-series methods'),
 'ro': dict(mkt='Piețele de energie electrică din România și Europa', facts='Datele din energie și faptele stilizate',
            tool='Instrumente pentru serii de timp'),
}

L = {
 'en': dict(h1='Lecture 1 · Energy markets and their data',
   note='The slide of the lecture is on the left, the same figure on the right, recomputed in your browser from the course data '
        '(data/clean) when you move a control. The ▶ button moves the main parameter step by step. Under each figure: a readout, '
        'a question for the room and the Quantlet with the code of the chart.',
   src='Day-ahead prices: OPCOM PZU (Romania), IBEX (Bulgaria), HUPX (Hungary), EPEX (Germany–Luxembourg), via energy-charts.info '
       '(Fraunhofer ISE). Aggregated supply and demand curves: OPCOM, PZU, delivery day 21 October 2026. Hour of the day in Central European Time (CET/CEST); '
       'from 1 October 2025 the 15-minute prices are averaged to the hour (profiles, ACF) or counted as quarter-hours (negative hours). '
       'Data to the cut-off of the lecture.'),
 'ro': dict(h1='Cursul 1 · Piețele de energie și datele lor',
   note='În stînga este slide-ul din curs, în dreapta aceeași figură, recalculată în browser din datele cursului (data/clean) cînd '
        'modificați un control. Butonul ▶ modifică parametrul principal pas cu pas. Sub fiecare figură: o sinteză numerică, o întrebare '
        'pentru sală și Quantlet-ul cu codul figurii.',
   src='Prețuri pentru ziua următoare: OPCOM PZU (România), IBEX (Bulgaria), HUPX (Ungaria), EPEX (Germania–Luxemburg), prin '
       'energy-charts.info (Fraunhofer ISE). Curbele agregate de cerere și ofertă: OPCOM, PZU, ziua de livrare 21 octombrie 2026. Ora '
       'zilei în ora Europei Centrale (CET/CEST); din 1 octombrie 2025, prețurile pe 15 minute sînt mediate pe oră (profiluri, ACF) sau numărate ca sferturi '
       'de oră (orele negative). Date pînă la data-limită a cursului.'),
}


def widgets(lang):
    ro = lang == 'ro'
    Z = dict(RO='România', BG='Bulgaria', HU='Ungaria', DE_LU='Germania–Luxemburg') if ro else \
        dict(RO='Romania', BG='Bulgaria', HU='Hungary', DE_LU='Germany–Luxembourg')
    zopts = [(z, Z[z]) for z in ZONES]
    seas = [('all', 'Tot anul' if ro else 'Whole year'), ('win', 'Iarna (dec–feb)' if ro else 'Winter (Dec–Feb)'),
            ('spr', 'Primăvara (mar–mai)' if ro else 'Spring (Mar–May)'), ('sum', 'Vara (iun–aug)' if ro else 'Summer (Jun–Aug)'),
            ('aut', 'Toamna (sep–nov)' if ro else 'Autumn (Sep–Nov)')]
    return {
     'merit-order': (select('mo-i', 'Intervalul de 15 minute' if ro else '15-minute interval',
                            [(0, 'Q45, 12:00–12:15 ora României (amiază)' if ro else 'Q45, 12:00–12:15 Romanian time (midday)'),
                             (1, 'Q77, 20:00–20:15 ora României (seară)' if ro else 'Q77, 20:00–20:15 Romanian time (evening)')], 0)
                     + slider('mo-s', 'Ofertă suplimentară la preț zero, de exemplu solar (MW)' if ro else 'Extra supply offered at zero price, e.g. solar (MW)', 0, 1000, 25, 0)
                     + slider('mo-d', 'Cerere suplimentară, inelastică (MW)' if ro else 'Extra demand, price-inelastic (MW)', -1000, 1000, 50, 0)
                     + play('mo'), charts('mo-chart', cls='one')),
     'daily-prices': (toggles('dp-z', 'Zone' if ro else 'Zones', zopts, ['RO', 'DE_LU'])
                      + slider('dp-w', 'Media mobilă (zile)' if ro else 'Moving average (days)', 1, 90, 1, 30)
                      + slider('dp-y', 'Începutul perioadei' if ro else 'Start of the period', 2015, 2026, 1, 2019) + play('dp'),
                      charts('dp-chart', cls='one')),
     'intraday-profile': (select('ip-z', 'Zona' if ro else 'Zone', zopts, 'RO') + select('ip-s', 'Sezonul' if ro else 'Season', seas, 'all')
                          + slider('ip-y', 'Anul' if ro else 'Year', 2016, 2026, 1, 2025) + play('ip'),
                          charts('ip-chart', 'ip-norm')),
     'negative-prices': (select('ng-z', 'Zona' if ro else 'Zone', zopts, 'RO')
                         + slider('ng-t', 'Prag: preț sub (EUR/MWh)' if ro else 'Threshold: price below (EUR/MWh)', -50, 20, 5, 0)
                         + slider('ng-y', 'Anul pentru profilul orar' if ro else 'Year of the hourly profile', 2019, 2026, 1, 2025) + play('ng'),
                         charts('ng-year', 'ng-hour')),
     'asinh': (slider('as-c', 'Scala transformării, c (multipli ai abaterii absolute mediane, MAD)' if ro else 'Scale of the transform, c (multiples of the median absolute deviation, MAD)', 0.1, 5, 0.1, 1)
               + select('as-y', 'Anul (prețuri orare, România)' if ro else 'Year (hourly prices, Romania)', [(y, str(y)) for y in range(2019, 2027)], 2025)
               + play('as'), charts('as-raw', 'as-tr')),
     'acf-hourly': (select('ac-z', 'Zona' if ro else 'Zone', zopts, 'RO')
                    + select('ac-f', 'Seria' if ro else 'Series', [('lev', 'Prețul orar' if ro else 'Hourly price'),
                                                                   ('d24', 'Diferența față de aceeași oră de ieri' if ro else 'Change from the same hour yesterday')], 'lev')
                    + slider('ac-y', 'Anul' if ro else 'Year', 2016, 2026, 1, 2025) + slider('ac-L', 'Laguri afișate (ore)' if ro else 'Lags shown (hours)', 48, 336, 24, 168)
                    + play('ac'), charts('ac-chart', cls='one')),
    }


QA = {
 'en': {
  'merit-order': ('At midday on 21 October 2026, the PZU (day-ahead market) cleared at 152.23 EUR/MWh, with about 2.8 GW on the published curves. '
                  'How much extra supply offered at zero price brings the midday price close to zero: about 50 MW, 500 MW or 2,000 MW?',
                  'About 50 MW. Near the crossing the demand curve is almost vertical: buyers bid for about 2,816 MW at 152 EUR/MWh and only about '
                  '11 MW more at 0 EUR/MWh. With 25 MW more supply the published curves clear at 131.40 EUR/MWh, with 50 MW at 0.68 EUR/MWh. In the '
                  'evening interval the curves cross on a vertical segment (any price from 206.49 to 247.00 EUR/MWh clears 3,423 MW; the official '
                  'price is 244.00 EUR/MWh), and 300 MW at zero price take the price to 0. Price-inelastic demand is the reason why a sunny hour can turn the price negative.'),
  'daily-prices': ('Over 2015–2020 the four zones traded at similar daily prices. What happens to the gap between Romania and Germany–Luxembourg after 2022?',
                   'Set the start to 2022 and keep Romania and Germany–Luxembourg on: the 30-day averages separate for long stretches, with Romania '
                   'above Germany in every summer from 2022 to 2026 (June–August means). Market coupling equalises prices only when the interconnectors are not congested; '
                   'the readout gives the mean and the standard deviation of each zone over the chosen period.'),
  'intraday-profile': ('In Romania, is the cheapest hour of the day in 2025 the same as in 2016?',
                       'No. In 2016, as in 2019, the cheapest hour is 03:00, as in a market driven by demand; in 2025 it is 13:00 (58.8 EUR/MWh), '
                       'because of the growth of solar capacity. The most expensive hour stays 19:00, but the ratio 19:00 / 13:00 rises from 1.30 in '
                       '2019 to 3.11 in 2025. Choose summer to see the "duck curve" at its deepest; the right panel divides each hour by the daily '
                       'mean, so years with different price levels can be compared.'),
  'negative-prices': ('Romania had its first negative day-ahead price on 21 May 2023. In which hours of the day do the negative prices of 2025 occur?',
                      'Around midday, when solar output is at its maximum: in 2025, 95% of the negative hours fall between 10:00 and 16:00, most often '
                      'at 13:00. Since 2024, 84% of them fall on weekends, and since 2023 about half of them in April and May (lecture numbers). Raise '
                      'the threshold to 0 EUR/MWh and above: the number of very cheap hours grows faster than that of strictly negative ones.'),
  'asinh': ('Hourly prices have a long right tail and, since 2023, negative values. Why not simply take logarithms?',
            'The logarithm is not defined for zero or negative prices. The area hyperbolic sine, asinh((p − median)/(c·MAD)), where MAD is the '
            'median absolute deviation, behaves like a logarithm in the tails and is almost linear near the median, and it accepts any sign. '
            'For Romania in 2025, c = 1 brings the skewness from 0.90 to 0.09 and the excess kurtosis from 4.24 to −0.24; a smaller c compresses '
            'the tails further (negative excess kurtosis), a larger c leaves the series closer to the raw prices.'),
  'acf-hourly': ('The autocorrelation of hourly prices peaks again at lags 24 and 168. What does this mean for a forecasting model?',
                 'The price of hour h depends on the same hour of the previous day and of the same day of the previous week: daily and weekly '
                 'seasonality (Romania, 2025: ρ(24) = 0.777, ρ(168) = 0.724). A next-day model therefore uses lags 24 (d−1), 48 (d−2) and 168 (d−7), '
                 'as the ARX model (autoregressive with exogenous inputs) of Lecture 2. The change from the same hour of yesterday turns ρ(24) negative (−0.263, the usual sign after a '
                 'seasonal difference) and keeps a weekly peak (ρ(168) = 0.296).'),
 },
 'ro': {
  'merit-order': ('La amiază, pe 21 octombrie 2026, PZU (piața pentru ziua următoare) s-a închis la 152,23 EUR/MWh, cu aproximativ 2,8 GW pe '
                  'curbele publicate. Cîtă ofertă suplimentară la preț zero aduce prețul de la amiază aproape de zero: circa 50 MW, 500 MW sau 2.000 MW?',
                  'Circa 50 MW. Lîngă punctul de intersecție, curba cererii este aproape verticală: cumpărătorii cer aproximativ 2.816 MW la '
                  '152 EUR/MWh și doar cu circa 11 MW mai mult la 0 EUR/MWh. Cu 25 MW de ofertă în plus, curbele publicate se intersectează la '
                  '131,40 EUR/MWh, iar cu 50 MW la 0,68 EUR/MWh. În intervalul de seară, curbele se intersectează pe un segment vertical (orice preț '
                  'între 206,49 și 247,00 EUR/MWh închide 3.423 MW; prețul oficial este 244,00 EUR/MWh), iar 300 MW la preț zero duc prețul la 0. '
                  'Cererea inelastică la preț explică de ce o oră însorită poate face prețul negativ.'),
  'daily-prices': ('În 2015–2020, cele patru zone aveau prețuri zilnice apropiate. Ce se întîmplă după 2022 cu diferența dintre România și Germania–Luxemburg?',
                   'Alegeți începutul în 2022 și păstrați România și Germania–Luxemburg: mediile pe 30 de zile se separă pe perioade lungi, cu '
                   'România peste Germania în fiecare vară din 2022 pînă în 2026 (mediile iunie–august). Cuplarea piețelor egalizează prețurile numai cînd interconexiunile nu sînt '
                   'congestionate; sinteza dă media și abaterea standard a fiecărei zone pe perioada aleasă.'),
  'intraday-profile': ('În România, este ora cea mai ieftină a zilei în 2025 aceeași ca în 2016?',
                       'Nu. În 2016, ca și în 2019, ora cea mai ieftină este 03:00, ca într-o piață determinată de consum; în 2025 este 13:00 '
                       '(58,8 EUR/MWh), din cauza creșterii capacității solare. Ora cea mai scumpă rămîne 19:00, dar raportul 19:00 / 13:00 crește de '
                       'la 1,30 în 2019 la 3,11 în 2025. Alegeți vara pentru a vedea „curba rață” (duck curve) cea mai adîncă; panoul din dreapta '
                       'împarte fiecare oră la media zilei, deci compară ani cu niveluri diferite ale prețului.'),
  'negative-prices': ('România a avut primul preț negativ pentru ziua următoare pe 21 mai 2023. În ce ore ale zilei apar prețurile negative din 2025?',
                      'În jurul amiezii, cînd producția solară este maximă: în 2025, 95% dintre orele cu preț negativ sînt între 10:00 și 16:00, cel '
                      'mai des la 13:00. Din 2024, 84% dintre ele cad în weekend, iar din 2023 aproximativ jumătate în aprilie și mai (cifrele din '
                      'curs). Ridicați pragul la 0 EUR/MWh și peste: numărul orelor foarte ieftine crește mai repede decît cel al orelor strict negative.'),
  'asinh': ('Prețurile orare au o coadă dreaptă lungă și, din 2023, valori negative. De ce nu luăm pur și simplu logaritmul?',
            'Logaritmul nu este definit pentru prețuri zero sau negative. Sinusul hiperbolic invers, asinh((p − mediana)/(c·MAD)), unde MAD '
            'este abaterea absolută mediană, se comportă ca un logaritm în cozi și aproape liniar lîngă mediană, și acceptă orice semn. Pentru '
            'România în 2025, c = 1 reduce asimetria de la 0,90 la 0,09 și excesul de kurtosis de la 4,24 la −0,24; un c mai mic comprimă și '
            'mai mult cozile (exces de kurtosis negativ), un c mai mare lasă seria mai aproape de prețurile brute.'),
  'acf-hourly': ('Autocorelația prețurilor orare are din nou vîrfuri la lagurile 24 și 168. Ce înseamnă aceasta pentru un model de prognoză?',
                 'Prețul orei h depinde de aceeași oră din ziua anterioară și din aceeași zi a săptămînii trecute: sezonalitate zilnică și '
                 'săptămînală (România, 2025: ρ(24) = 0,777, ρ(168) = 0,724). Un model pentru ziua următoare folosește deci lagurile 24 (d−1), '
                 '48 (d−2) și 168 (d−7), ca modelul ARX (autoregresiv cu variabile exogene) din Cursul 2. Diferența față de aceeași oră de ieri face ρ(24) negativ (−0,263, semnul '
                 'obișnuit după o diferență sezonieră) și păstrează un vîrf săptămînal (ρ(168) = 0,296).'),
 },
}

TEXT_JS = {
 'en': r"""window.LK_TEXT = {
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
""",
 'ro': r"""window.LK_TEXT = {
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
""",
}


# ---------------------------------------------------------------- data (real course data only)
def data():
    import numpy as np
    import pandas as pd
    END = cutoff()
    out = {'end': str(END.date()), 'zones': ZONES}

    # 1. OPCOM aggregated curves, two 15-minute intervals of 21 October 2026
    cur = csv('opcom_pzu_curves.csv')
    meta = json.load(open(os.path.join(DATA, 'opcom_pzu_curves_meta.json'), encoding='utf-8'))
    out['mo'] = []
    for iv in meta['intervals']:
        lab = iv['interval_label']
        s = cur[(cur['interval'] == lab) & (cur['side'] == 'supply')][['price_eur_mwh', 'quantity_mw']].values
        d = cur[(cur['interval'] == lab) & (cur['side'] == 'demand')][['price_eur_mwh', 'quantity_mw']].values
        p_off = iv['official_clearing_price_eur_mwh']
        out['mo'].append({'label': lab, 'p_off': p_off,
                          'q_cross': iv['curve_cleared_quantity_mw'],
                          'sp': rnd(s[:, 0], 2), 'sq': rnd(s[:, 1], 1), 'dp': rnd(d[:, 0], 2), 'dq': rnd(d[:, 1], 1)})

    # 2. daily base prices (CET days)
    P = csv('power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet').loc[:END]
    P = P.asfreq('D')
    out['dp'] = {'t0': str(P.index[0].date()), 'n': len(P), **{z: rnd(P[z].values, 1) for z in ZONES}}

    # 3.-6. hourly (CET/CEST) and native prices
    H = csv('power_da_prices_hourly_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')
    H.index = H.index.tz_convert('Europe/Brussels')
    H = H.loc[:str(END.date())]
    X = csv('power_da_prices_native_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')
    X.index = X.index.tz_convert('Europe/Brussels')
    X = X.loc[:str(END.date())]
    years = list(range(2015, END.year + 1))
    SEAS = {'all': list(range(1, 13)), 'win': [12, 1, 2], 'spr': [3, 4, 5], 'sum': [6, 7, 8], 'aut': [9, 10, 11]}
    prof = {}
    for z in ZONES:
        s = H[z].dropna()
        prof[z] = {}
        for y in years:
            sy = s[s.index.year == y]
            if len(sy) < 24 * 60:
                continue
            prof[z][y] = {k: rnd(sy[sy.index.month.isin(m)].groupby(sy[sy.index.month.isin(m)].index.hour).mean().reindex(range(24)).values, 2)
                          for k, m in SEAS.items()}
    out['ip'] = prof

    # negative / cheap hours: hour-equivalents (quarter-hours count 0.25) below each threshold, by zone, year and hour of the day
    thr = list(range(-50, 21, 5))
    hrs = X['mtu_minutes'] / 60.0
    ng = {}
    for z in ZONES:
        v = X[z]
        ok = v.notna()
        ng[z] = {}
        for y in years:
            m = ok & (X.index.year == y)
            if m.sum() < 24 * 60:
                continue
            vy, wy, hy = v[m].values, hrs[m].values, X.index[m].hour.values
            ng[z][y] = [rnd(np.bincount(hy, weights=wy * (vy < t), minlength=24), 2) for t in thr]
    out['ng'] = {'thr': thr, 'v': ng}

    # asinh: hourly Romanian prices of each year 2019 to the cut-off
    out['as'] = {}
    for y in range(2019, END.year + 1):
        s = H['RO'][H.index.year == y].dropna()
        out['as'][y] = rnd(s.values, 1)

    # ACF of hourly prices, lags 1..336, by zone, year, level / 24-hour difference
    def acf(x, L=336):
        x = x[~np.isnan(x)]
        x = x - x.mean()
        n, v = len(x), x @ x
        return [float(x[k:] @ x[:-k] / v) for k in range(1, L + 1)], n

    ac = {}
    for z in ZONES:
        ac[z] = {}
        for y in years:
            s = H[z][H.index.year == y]
            s = s[~s.index.duplicated()]
            if s.notna().sum() < 24 * 60:
                continue
            x = s.values.astype(float)
            a1, n1 = acf(x)
            d24 = x[24:] - x[:-24]
            a2, _ = acf(d24)
            ac[z][y] = {'lev': rnd(a1, 3), 'd24': rnd(a2, 3), 'n': n1}
    out['ac'] = ac
    return out


if __name__ == '__main__':
    interactive_common.build(sys.modules[__name__])
