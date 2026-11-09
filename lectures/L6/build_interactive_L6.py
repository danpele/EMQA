"""Build the interactive page of Lecture 6 (Renewables, negative prices and batteries): interactive/L6.html (EN) and
interactive/L6_ro.html (RO).

Inputs (interactive/L6_data.js) are computed here from data/clean with the rules of lectures/L6/analysis_L6.py (capture price on
the native price grid, residual load, hour-equivalents of negative prices, daily battery linear programme); the page logic is in
interactive/L6.js. The battery schedules (about 170 000 daily linear programmes: 4 zones x 3 durations x 5 efficiencies) are solved
in parallel and kept in lectures/L6/cache/interactive_battery.pkl (rebuilt when the prices change).
Run: python3 lectures/L6/build_interactive_L6.py [--no-data]
"""
import hashlib
import os
import pickle
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import interactive_common  # noqa: E402
from interactive_common import slider, select, toggles, play, charts, rnd, DATA  # noqa: E402

K = 6
ZONES = ['RO', 'BG', 'HU', 'DE_LU']
TZ = 'Europe/Brussels'
DURS = (1, 2, 4)
ETAS = (0.75, 0.80, 0.85, 0.90, 0.95)

BLOCKS = [('resid-price', 'resid_price', 'merit', 'rp'),
          ('capture-rates', 'capture_rates', 'capt', 'cr'),
          ('cannibal', 'cannibal', 'capt', 'cn'),
          ('neg-hours', 'neg_hours', 'neg', 'nh'),
          ('battery', 'bat_years', 'bat', 'bt'),
          ('rogb', 'rogb_summer', 'case', 'rg')]

SECTIONS = {
 'en': dict(merit='Renewables and the merit order', capt='Capture prices and cannibalisation', neg='Negative prices',
            bat='The economics of a battery', case='Case study: summer 2026, Romania and Bulgaria'),
 'ro': dict(merit='Sursele regenerabile și ordinea de merit', capt='Prețul capturat și canibalizarea', neg='Prețurile negative',
            bat='Economia unei baterii', case='Studiu de caz: vara lui 2026, România și Bulgaria'),
}

L = {
 'en': dict(h1='Lecture 6 · Renewables, negative prices and batteries',
   note='The slide of the lecture is on the left, the same figure on the right, recomputed in your browser from the course data '
        '(data/clean) when you move a control. The ▶ button moves the main parameter step by step. Under each figure: a readout, '
        'a question for the room and the Quantlet with the code of the chart.',
   src='Day-ahead prices: OPCOM PZU (Piața pentru Ziua Următoare, the Romanian day-ahead market), IBEX (Bulgaria), HUPX (Hungary), EPEX (Germany–Luxembourg); generation, load and '
       'cross-border physical flows (data of ENTSO-E, the European Network of Transmission System Operators for Electricity): energy-charts.info (Fraunhofer ISE). Prices hourly to September 2025 and per '
       '15 minutes from 1 October 2025 (a quarter-hour counts 0.25 h). Battery: 1 MW, at most one full cycle a day, perfect foresight '
       'of the day-ahead prices, optimal schedule of each delivery day by linear programming (rule of the lecture). Data to the '
       'cut-off of the lecture (31 October 2026).'),
 'ro': dict(h1='Cursul 6 · Surse regenerabile, prețuri negative și baterii',
   note='În stînga este slide-ul din curs, în dreapta aceeași figură, recalculată în browser din datele cursului (data/clean) cînd '
        'modificați un control. Butonul ▶ modifică parametrul principal pas cu pas. Sub fiecare figură: o sinteză numerică, o întrebare '
        'pentru sală și Quantlet-ul cu codul figurii.',
   src='Prețuri pentru ziua următoare: OPCOM PZU (Piața pentru Ziua Următoare, România), IBEX (Bulgaria), HUPX (Ungaria), EPEX (Germania–Luxemburg); producția, '
       'consumul și fluxurile fizice transfrontaliere (date ENTSO-E, Rețeaua europeană a operatorilor de transport și sistem pentru energie electrică): energy-charts.info (Fraunhofer ISE). Prețuri orare pînă în '
       'septembrie 2025 și pe 15 minute din 1 octombrie 2025 (un sfert de oră contează 0,25 h). Bateria: 1 MW, cel mult un ciclu complet '
       'pe zi, prețurile pentru ziua următoare cunoscute perfect, programul optim al fiecărei zile de livrare prin programare liniară '
       '(regula din curs). Date pînă la data-limită a cursului (31 octombrie 2026).'),
}


def widgets(lang):
    ro = lang == 'ro'
    Z = dict(RO='România', BG='Bulgaria', HU='Ungaria', DE_LU='Germania–Luxemburg') if ro else \
        dict(RO='Romania', BG='Bulgaria', HU='Hungary', DE_LU='Germany–Luxembourg')
    z3 = [(z, Z[z]) for z in ('RO', 'BG', 'HU')]
    hrs = [('all', 'Toate orele' if ro else 'All hours'), ('mid', 'Amiaza, 11:00–15:00' if ro else 'Midday, 11:00–15:00'),
           ('eve', 'Seara, 18:00–22:00' if ro else 'Evening, 18:00–22:00')]
    return {
     'resid-price': (toggles('rp-y', 'Anii' if ro else 'Years', [(y, str(y)) for y in (2023, 2024, 2025, 2026)], [2023, 2026])
                     + select('rp-h', 'Orele zilei' if ro else 'Hours of the day', hrs, 'all')
                     + slider('rp-b', 'Lățimea intervalelor de consum rezidual (GW)' if ro else 'Width of the residual-load bins (GW)', 0.25, 2, 0.25, 0.5),
                     charts('rp-chart', cls='one')),
     'capture-rates': (select('cr-t', 'Tehnologia' if ro else 'Technology', [('solar', 'Solar'), ('wind', 'Eolian' if ro else 'Wind')], 'solar')
                       + toggles('cr-z', 'Zone' if ro else 'Zones', z3, ['RO', 'BG', 'HU'])
                       + select('cr-m', 'Afișează' if ro else 'Show', [('cr', 'Rata de captură (%)' if ro else 'Capture rate (%)'),
                                                                      ('disc', 'Discountul față de prețul de bază (EUR/MWh)' if ro else 'Discount to the base price (EUR/MWh)')], 'cr'),
                       charts('cr-chart', 'cr-px')),
     'cannibal': (select('cn-z', 'Zona' if ro else 'Zone', z3, 'RO')
                  + slider('cn-y0', 'Lunile de la' if ro else 'Months from', 2019, 2026, 1, 2019)
                  + slider('cn-y1', 'pînă la (inclusiv anul)' if ro else 'to (year included)', 2019, 2026, 1, 2026) + play('cn'),
                  charts('cn-chart', cls='one')),
     'neg-hours': (select('nh-z', 'Zona' if ro else 'Zone', [(z, Z[z]) for z in ZONES], 'RO')
                   + slider('nh-y', 'Anul' if ro else 'Year', 2022, 2026, 1, 2026) + play('nh'),
                   charts('nh-heat', 'nh-depth')),
     'battery': (select('bt-z', 'Zona' if ro else 'Zone', [(z, Z[z]) for z in ZONES], 'RO')
                 + select('bt-e', 'Durata bateriei (ore la puterea maximă)' if ro else 'Battery duration (hours at full power)',
                          [(e, f'{e} h ({e} MWh / 1 MW)') for e in DURS], 2)
                 + slider('bt-eta', 'Randamentul pe ciclu complet, încărcare și descărcare (%)' if ro else 'Round-trip efficiency (%)', 75, 95, 5, 85)
                 + slider('bt-y', 'Anul' if ro else 'Year', 2019, 2026, 1, 2025) + play('bt'),
                 charts('bt-years', 'bt-eff')),
     'rogb': (slider('rg-d0', 'Prima zi a perioadei' if ro else 'First day of the period', 0, 91, 1, 0)
              + slider('rg-d1', 'Ultima zi a perioadei' if ro else 'Last day of the period', 0, 91, 1, 91)
              + toggles('rg-b', 'Granițele' if ro else 'Borders', [('sum', 'Toate' if ro else 'All'), ('bulgaria', 'Bulgaria'),
                                                                    ('hungary', 'Ungaria' if ro else 'Hungary'), ('serbia', 'Serbia')], ['sum', 'bulgaria'])
              + select('rg-p', 'Panoul din dreapta' if ro else 'Right panel', [('lev', 'Prețurile RO și BG' if ro else 'RO and BG prices'),
                                                                               ('gap', 'Diferența de preț RO − BG' if ro else 'Price gap RO − BG')], 'lev')
              + play('rg'), charts('rg-flow', 'rg-price')),
    }


QA = {
 'en': {
  'resid-price': ('Residual load is load minus wind and solar output. In 2026, how often is the hourly residual load of Romania below 2 GW, '
                  'and what is the mean price in those hours?',
                  'In about 9% of the hours of 2026 (to the cut-off), against 0.1% in 2023; the mean price in those hours is about 51 EUR/MWh, against '
                  'about 192 EUR/MWh when residual load is above 6 GW. Across 2023–2026, a regression with month, hour and weekday fixed effects gives '
                  '+28.32 EUR/MWh per GW of residual load (t = 32.1). The cloud of points is wide: residual load explains a large part of the price, '
                  'but neighbouring markets, hydro and fuel prices move it too.'),
  'capture-rates': ('The capture rate is the output-weighted mean price of a technology divided by the time-weighted (base) price. Why did the '
                    'solar capture rate of Romania fall from 104.5% in 2019 to 59.4% in 2025?',
                    'Because solar output is concentrated in the same midday hours, and as capacity grew those hours became the cheapest of the day '
                    '(the merit-order effect of the plants themselves). In 2025 solar earned 64.2 EUR/MWh against a base price of 108.2 EUR/MWh, a '
                    'discount of 43.9 EUR/MWh. Wind, spread more evenly over the day and night, keeps a much higher capture rate: switch the technology.'),
  'cannibal': ('Over the months from 2019 to October 2026, by how much does the Romanian solar capture rate fall for each extra percentage point of '
               'solar in the load?',
               'About 4.2 percentage points (slope −4.2, R² = 0.53 on 94 months; standard error 1.03 in the lecture, robust to autocorrelation). The same slope is −1.32 in '
               'Bulgaria and −2.14 in Hungary. Move the start of the window: the slope estimated on recent months only is driven by the record '
               'solar shares of 2025–2026 (up to 17.8% of the load in August 2026, lowest capture rate 44.3% in March 2026).'),
  'neg-hours': ('In Romania, in which months and hours are the negative prices of 2026 concentrated, and how deep are they?',
                'In the middle of the day (roughly 10:00–16:00) of the spring months, when solar output is high, demand moderate and hydro plants '
                'run. The heat map counts hour-equivalents (a 15-minute interval counts 0.25 h); the right panel shows the duration-weighted mean '
                'of the negative prices by month. Choose 2022: Romania had no negative price before May 2023.'),
  'battery': ('A 1-MW battery with 2 hours of storage and 85% round-trip efficiency earned about 98.7 thousand EUR in Romania in 2025 with perfect '
              'foresight. Does a 4-hour battery earn twice as much?',
              'No: 165.2 thousand EUR, i.e. 1.67 times as much. The extra hours of storage buy energy in less cheap hours and sell it in less '
              'expensive ones, so each MWh of capacity earns less (and the real schedule is decided on forecasts, not on known prices: with the '
              'mean profile of the previous week the lecture keeps about 85% of the perfect-foresight revenue). Move the efficiency: from 75% to 95%, the revenue of the 2-hour battery in Romania rises '
              'by 39–46% in 2019–2022 but only by 21–22% in 2024–2026, when the deep midday troughs (down to negative prices) make the '
              'buying price small compared with the selling price, so the losses cost less.'),
  'rogb': ('In summer 2026 (1 June–31 August), Romania exported at midday and imported in the evening. From which neighbour did the evening imports '
           'come, and why?',
           'From Bulgaria, on all 92 days: at 21:00 Romanian time, the mean flow on the Romania–Bulgaria border was 2,064 MW towards Romania. '
           'At that hour the mean Romanian price was 243.9 EUR/MWh and the Bulgarian one 178.3 EUR/MWh (gap 65.6 EUR/MWh): the interconnector '
           'was congested, otherwise market coupling would have equalised the two prices. At midday both prices were about 50 EUR/MWh and '
           'Romania exported, mostly to Hungary (857 MW) and Serbia (367 MW).'),
 },
 'ro': {
  'resid-price': ('Consumul rezidual este consumul minus producția eoliană și solară. În 2026, cît de des este consumul rezidual orar al României '
                  'sub 2 GW și care este prețul mediu în acele ore?',
                  'În aproximativ 9% dintre orele din 2026 (pînă la data-limită), față de 0,1% în 2023; prețul mediu în aceste ore este de circa 51 EUR/MWh, față de '
                  'circa 192 EUR/MWh cînd consumul rezidual depășește 6 GW. Pe 2023–2026, o regresie cu efecte fixe de lună, oră și zi a săptămînii '
                  'dă +28,32 EUR/MWh pentru fiecare GW de consum rezidual (t = 32,1). Norul de puncte este larg: consumul rezidual explică o parte '
                  'mare a prețului, dar și piețele vecine, hidrocentralele și prețurile combustibililor îl mișcă.'),
  'capture-rates': ('Rata de captură este prețul mediu ponderat cu producția unei tehnologii, împărțit la prețul mediu ponderat cu timpul (prețul '
                    'de bază). De ce a scăzut rata de captură a solarului din România de la 104,5% în 2019 la 59,4% în 2025?',
                    'Pentru că producția solară este concentrată în aceleași ore de la amiază, iar pe măsură ce capacitatea a crescut, acele ore au '
                    'devenit cele mai ieftine ale zilei (efectul de ordine de merit al centralelor înseși). În 2025, solarul a obținut 64,2 EUR/MWh, '
                    'față de un preț de bază de 108,2 EUR/MWh, un discount de 43,9 EUR/MWh. Eolianul, distribuit mai uniform între zi și noapte, '
                    'păstrează o rată de captură mult mai mare: schimbați tehnologia.'),
  'cannibal': ('Pe lunile din 2019 pînă în octombrie 2026, cu cît scade rata de captură a solarului din România pentru fiecare punct procentual '
               'în plus al solarului în consum?',
               'Cu aproximativ 4,2 puncte procentuale (panta −4,2, R² = 0,53 pe 94 de luni; eroarea standard 1,03 în curs, robustă la autocorelare). Aceeași pantă este '
               '−1,32 în Bulgaria și −2,14 în Ungaria. Mutați începutul ferestrei: panta estimată numai pe lunile recente este determinată de '
               'ponderile record ale solarului din 2025–2026 (pînă la 17,8% din consum în august 2026, cea mai mică rată de captură 44,3% în martie 2026).'),
  'neg-hours': ('În România, în ce luni și ore sînt concentrate prețurile negative din 2026 și cît de adînci sînt?',
                'La mijlocul zilei (aproximativ 10:00–16:00) în lunile de primăvară, cînd producția solară este mare, consumul moderat și '
                'hidrocentralele funcționează. Harta numără ore echivalente (un interval de 15 minute contează 0,25 h); panoul din dreapta arată '
                'media ponderată cu durata a prețurilor negative, pe luni. Alegeți 2022: România nu a avut preț negativ înainte de mai 2023.'),
  'battery': ('O baterie de 1 MW cu 2 ore de stocare și randament pe ciclu complet de 85% a cîștigat în România, în 2025, aproximativ 98,7 mii EUR, '
              'cu prețurile cunoscute perfect. Cîștigă o baterie de 4 ore de două ori mai mult?',
              'Nu: 165,2 mii EUR, adică de 1,67 ori mai mult. Orele suplimentare de stocare cumpără energie în ore mai puțin ieftine și o vînd '
              'în ore mai puțin scumpe, deci fiecare MWh de capacitate cîștigă mai puțin (iar programul real se decide pe prognoze, nu pe prețuri '
              'cunoscute: cu profilul mediu al săptămînii anterioare, cursul păstrează circa 85% din venitul cu prețuri cunoscute). Mutați randamentul: de la 75% la 95%, venitul bateriei de 2 ore din România crește '
              'cu 39–46% în 2019–2022, dar doar cu 21–22% în 2024–2026, cînd golurile adînci de la amiază (pînă la prețuri negative) fac '
              'prețul de cumpărare mic față de cel de vînzare, deci pierderile costă mai puțin.'),
  'rogb': ('În vara lui 2026 (1 iunie–31 august), România a exportat la amiază și a importat seara. De la care vecin au venit importurile de seară și de ce?',
           'Din Bulgaria, în toate cele 92 de zile: la ora 21:00 a României, fluxul mediu pe granița România–Bulgaria a fost de 2.064 MW spre '
           'România. La acea oră, prețul mediu din România a fost 243,9 EUR/MWh, iar cel din Bulgaria 178,3 EUR/MWh (diferența 65,6 EUR/MWh): '
           'interconexiunea era congestionată, altfel cuplarea piețelor ar fi egalizat cele două prețuri. La amiază, ambele prețuri au fost de '
           'circa 50 EUR/MWh, iar România a exportat, mai ales spre Ungaria (857 MW) și Serbia (367 MW).'),
 },
}

TEXT_JS = {
 'en': r"""window.LK_TEXT = {
 eur: 'EUR/MWh', gw: 'GW', hour: 'Hour of the day (CET)', hourRO: 'Hour of the day (Romanian time)', year: 'Year', month: 'Month',
 resid: 'Residual load = load − wind − solar (GW)', price: 'Day-ahead price (EUR/MWh)',
 rpTitle: 'Mean price by bin of residual load (bins with at least 20 hours)',
 rp: (y, n, b, lo, plo, hi, phi) => `${y}: ${window.EMQAI.cnt(n, 'hour', 'hours')}; slope of a straight line through the hours ${b} EUR/MWh per GW; residual load below 2 GW in ${lo} of the hours (mean price ${plo}), above 6 GW in ${hi} (mean price ${phi}).`,
 crTitle: { cr: 'Capture rate = capture price / base price (%)', disc: 'Base price − capture price (EUR/MWh)' },
 crPx: 'Capture price and base price (EUR/MWh)', base: 'base price', capture: 'capture price',
 tech: { solar: 'solar', wind: 'wind' },
 cr: (z, t, y, cp, base, cr, twh) => `${z}, ${t}, ${y}: capture price ${cp}, base price ${base} EUR/MWh, capture rate ${cr}; output ${twh} TWh.`,
 partial: y => `${y} runs to the cut-off of the lecture (partial year).`,
 cnX: 'Solar output / load in the month (%)', cnY: 'Solar capture rate in the month (%)',
 cn: (z, n, b, se, a, r2) => `${z}, ${window.EMQAI.cnt(n, 'month', 'months')}: capture rate = ${a} ${b} × solar share (OLS, ordinary least squares: classical standard error of the slope ${se}, R² = ${r2}).`,
 cnMin: (m, v, ms, s) => `Lowest capture rate ${v} in ${m}; highest solar share ${s} in ${ms}.`,
 nhTitle: y => `Hours with a negative price in ${y} (hour-equivalents)`, nhDepth: 'Mean negative price (EUR/MWh) and negative hours, by month',
 nhHours: 'negative hours', nhMean: 'mean negative price',
 nh: (z, y, n, peak, pm, mid, mn) => `${z}, ${y}: ${n} with a negative price; most in ${pm}, ${mid} of them between 10:00 and 16:00; mean negative price ${mn} EUR/MWh.`,
 nh0: (z, y) => `${z}: no negative price in ${y}.`,
 btYears: (e, eta) => `Annual revenue of a 1-MW battery, η = ${eta} (thousand EUR)`, btEff: y => `Revenue vs round-trip efficiency, ${y} (thousand EUR)`,
 eff: 'Round-trip efficiency (%)', kEUR: 'Thousand EUR per MW',
 bt: (z, y, e, eta, r, pd, pm, n) => `${z}, ${y}, ${e} h, η = ${eta}: ${r} thousand EUR per MW (${pd} EUR per day, ${pm} EUR per MWh of storage capacity and day), ${window.EMQAI.cnt(n, 'day', 'days')}.`,
 bt2: (x, af, cap) => `4 h earns ${x} times as much as 2 h. Capital cost that this revenue repays over 15 years at 8%: ${cap} EUR per kW (annuity factor ${af}).`,
 rgFlow: 'Mean net import of Romania (MW; < 0: export)', rgLev: 'Mean day-ahead price (EUR/MWh)', rgGap: 'Mean price gap Romania − Bulgaria (EUR/MWh)',
 border: { sum: 'all borders', bulgaria: 'Bulgaria', hungary: 'Hungary', serbia: 'Serbia' },
 rg: (d0, d1, n, exh, ex, imh, im) => `${d0} to ${d1} (${window.EMQAI.cnt(n, 'day', 'days')}): largest mean export on all borders ${ex} MW at ${exh}:00, largest mean import ${im} MW at ${imh}:00.`,
 rg2: (h, bg, nd, pro, pbg) => `Border with Bulgaria: largest mean import ${bg} MW at ${h}:00, evening import (19:00–23:00) on ${nd}; at ${h}:00 the prices are ${pro} (RO) and ${pbg} EUR/MWh (BG).`,
 rgDays: n => window.EMQAI.cnt(n, 'day', 'days'),
 ro: 'Romania', bg: 'Bulgaria', gap: 'RO − BG'
};
""",
 'ro': r"""window.LK_TEXT = {
 eur: 'EUR/MWh', gw: 'GW', hour: 'Ora zilei (CET)', hourRO: 'Ora zilei (ora României)', year: 'Anul', month: 'Luna',
 resid: 'Consumul rezidual = consum − eolian − solar (GW)', price: 'Prețul pentru ziua următoare (EUR/MWh)',
 rpTitle: 'Prețul mediu pe intervale de consum rezidual (intervale cu cel puțin 20 de ore)',
 rp: (y, n, b, lo, plo, hi, phi) => `${y}: ${window.EMQAI.cnt(n, 'oră', 'ore')}; panta dreptei prin ore ${b} EUR/MWh pe GW; consum rezidual sub 2 GW în ${lo} din ore (preț mediu ${plo}), peste 6 GW în ${hi} (preț mediu ${phi}).`,
 crTitle: { cr: 'Rata de captură = prețul de captură / prețul de bază (%)', disc: 'Prețul de bază − prețul de captură (EUR/MWh)' },
 crPx: 'Prețul de captură și prețul de bază (EUR/MWh)', base: 'prețul de bază', capture: 'prețul de captură',
 tech: { solar: 'solar', wind: 'eolian' },
 cr: (z, t, y, cp, base, cr, twh) => `${z}, ${t}, ${y}: prețul de captură ${cp}, prețul de bază ${base} EUR/MWh, rata de captură ${cr}; producția ${twh} TWh.`,
 partial: y => `${y} se oprește la data-limită a cursului (an incomplet).`,
 cnX: 'Producția solară / consumul lunii (%)', cnY: 'Rata de captură a solarului în lună (%)',
 cn: (z, n, b, se, a, r2) => `${z}, ${window.EMQAI.cnt(n, 'lună', 'luni')}: rata de captură = ${a} ${b} × ponderea solarului (MCO, metoda celor mai mici pătrate: eroarea standard clasică a pantei ${se}, R² = ${r2}).`,
 cnMin: (m, v, ms, s) => `Cea mai mică rată de captură ${v} în ${m}; cea mai mare pondere a solarului ${s} în ${ms}.`,
 nhTitle: y => `Ore cu preț negativ în ${y} (ore echivalente)`, nhDepth: 'Prețul negativ mediu (EUR/MWh) și orele negative, pe luni',
 nhHours: 'ore negative', nhMean: 'prețul negativ mediu',
 nh: (z, y, n, peak, pm, mid, mn) => `${z}, ${y}: ${n} cu preț negativ; cele mai multe în ${pm}, ${mid} dintre ele între 10:00 și 16:00; prețul negativ mediu ${mn} EUR/MWh.`,
 nh0: (z, y) => `${z}: niciun preț negativ în ${y}.`,
 btYears: (e, eta) => `Venitul anual al unei baterii de 1 MW, η = ${eta} (mii EUR)`, btEff: y => `Venitul în funcție de randament, ${y} (mii EUR)`,
 eff: 'Randamentul pe ciclu complet (%)', kEUR: 'Mii EUR pe MW',
 bt: (z, y, e, eta, r, pd, pm, n) => `${z}, ${y}, ${e} h, η = ${eta}: ${r} mii EUR pe MW (${pd} EUR pe zi, ${pm} EUR pe MWh de capacitate de stocare și zi), ${window.EMQAI.cnt(n, 'zi', 'zile')}.`,
 bt2: (x, af, cap) => `Bateria de 4 h cîștigă de ${x} ori mai mult decît cea de 2 h. Costul de capital pe care acest venit îl recuperează în 15 ani la 8%: ${cap} EUR pe kW (factorul de anuitate ${af}).`,
 rgFlow: 'Importul net mediu al României (MW; < 0: export)', rgLev: 'Prețul mediu pentru ziua următoare (EUR/MWh)', rgGap: 'Diferența medie de preț România − Bulgaria (EUR/MWh)',
 border: { sum: 'toate granițele', bulgaria: 'Bulgaria', hungary: 'Ungaria', serbia: 'Serbia' },
 rg: (d0, d1, n, exh, ex, imh, im) => `${d0} – ${d1} (${window.EMQAI.cnt(n, 'zi', 'zile')}): cel mai mare export mediu pe toate granițele ${ex} MW la ${exh}:00, cel mai mare import mediu ${im} MW la ${imh}:00.`,
 rg2: (h, bg, nd, pro, pbg) => `Granița cu Bulgaria: cel mai mare import mediu ${bg} MW la ${h}:00, import seara (19:00–23:00) în ${nd}; la ${h}:00 prețurile sînt ${pro} (RO) și ${pbg} EUR/MWh (BG).`,
 rgDays: n => window.EMQAI.cnt(n, 'zi', 'zile'),
 ro: 'România', bg: 'Bulgaria', gap: 'RO − BG'
};
""",
}


# ---------------------------------------------------------------- data (real course data only; rules of analysis_L6.py)
def _load():
    import pandas as pd
    PX = pd.read_csv(os.path.join(DATA, 'power_da_prices_native_utc.csv'), parse_dates=['timestamp_utc']).set_index('timestamp_utc')
    PX.index = PX.index.tz_convert(TZ)
    PX['dur'] = PX['mtu_minutes'] / 60.0
    GN = {}
    for c in ('ro', 'bg', 'hu'):
        g = pd.read_csv(os.path.join(DATA, f'generation_{c}_mw_native_utc.csv'), parse_dates=['timestamp_utc']).set_index('timestamp_utc')
        g.index = g.index.tz_convert(TZ)
        GN[c.upper()] = g
    last = min(PX['RO'].dropna().index.max().tz_localize(None), GN['RO']['solar'].dropna().index.max().tz_localize(None))
    END = pd.Timestamp(((last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())
    PX = PX[PX.index < (END + pd.Timedelta(days=1)).tz_localize(TZ)]
    return PX, GN, END


def hfloor(idx):
    return idx.tz_convert('UTC').floor('1h').tz_convert(TZ)


def on_price_grid(PX, GN, gen):
    import pandas as pd
    MTU15 = pd.Timestamp('2025-10-01').tz_localize(TZ)
    g = GN[gen].drop(columns=['mtu_minutes']).copy()
    out = g.resample('1h').mean().reindex(hfloor(PX.index)).set_axis(PX.index)
    q15 = PX['mtu_minutes'] == 15
    if (GN[gen]['mtu_minutes'] == 15).loc[GN[gen].index >= MTU15].all():
        out.loc[q15] = g.resample('15min').mean().reindex(PX.index[q15]).values
    return out


def day_groups(PX, zone, start):
    s = PX[[zone, 'dur']]
    s = s[s.index >= start]
    out = {}
    for dd, g in s.groupby(s.index.tz_localize(None).normalize()):
        tot = g['dur'].sum()
        if g[zone].notna().all() and abs(tot - round(tot)) < 1e-9 and round(tot) in (23, 24, 25):
            out[dd] = (g[zone].values.astype(float), g['dur'].values.astype(float))
    return out


def battery_day(p, dur, E, P=1.0, eta=0.85, cycles=1.0):
    """Same linear programme as analysis_L6.battery_day; returns the revenue of the day (EUR per MW)."""
    import numpy as np
    from scipy import sparse
    from scipy.optimize import linprog
    n = len(p)
    r = np.sqrt(eta)
    cost = np.concatenate([p * dur, -p * dur, np.zeros(n)])
    Lw = sparse.diags([np.ones(n), -np.ones(n - 1)], [0, -1], format='csr')
    A_eq = sparse.hstack([-r * sparse.diags(dur), sparse.diags(dur / r), Lw], format='csr')
    A_eq = sparse.vstack([A_eq, sparse.hstack([sparse.csr_matrix((1, 2 * n)), sparse.csr_matrix(([1.0], ([0], [n - 1])), shape=(1, n))])])
    A_ub = sparse.hstack([sparse.csr_matrix((1, n)), sparse.csr_matrix(dur / r), sparse.csr_matrix((1, n))], format='csr')
    res = linprog(cost, A_ub=A_ub, b_ub=[cycles * E], A_eq=A_eq, b_eq=np.zeros(n + 1),
                  bounds=[(0, P)] * (2 * n) + [(0, E)] * n, method='highs')
    x = res.x
    return float(np.sum(p * (x[n:2 * n] - x[:n]) * dur))


def _bat_job(args):
    days, E, eta = args
    return [battery_day(p, w, E, eta=eta) for p, w in days]


def data():
    import numpy as np
    import pandas as pd
    import statsmodels.api as sm
    PX, GN, END = _load()
    Y = END.year
    out = {'end': str(END.date())}
    GR = {z: on_price_grid(PX, GN, z) for z in ('RO', 'BG', 'HU')}
    YR, MO = PX.index.year, PX.index.to_period('M')

    # 1. residual load and price, hourly 2023 to the cut-off (Romania)
    ro = GR['RO']
    H = pd.DataFrame({'P': PX['RO'], 'dur': PX['dur'], 'load': ro['load'], 'wind': ro['wind_onshore'], 'solar': ro['solar']})
    H = H[H.index >= pd.Timestamp('2023-01-01').tz_localize(TZ)]
    HH = (H[['P', 'load', 'wind', 'solar']].mul(H['dur'], axis=0).groupby(hfloor(H.index)).sum()
          .div(H['dur'].groupby(hfloor(H.index)).sum(), axis=0)).dropna()
    HH['resid'] = (HH['load'] - HH['wind'] - HH['solar']) / 1000
    out['rp'] = {str(y): {'r': rnd(HH['resid'][HH.index.year == y].values, 2), 'p': rnd(HH['P'][HH.index.year == y].values, 1),
                          'h': HH.index[HH.index.year == y].hour.tolist()} for y in (2023, 2024, 2025, 2026)}

    # 2. capture prices by zone, technology and year (duration weights, generation on the price grid)
    def capture(zone, tech, mask):
        p, w = PX[zone], GR[zone][tech] * PX['dur']
        m = mask & p.notna() & w.notna()
        bm = mask & p.notna()
        return (float((p[m] * w[m]).sum() / w[m].sum()), float((p[bm] * PX['dur'][bm]).sum() / PX['dur'][bm].sum()), float(w[m].sum()))
    cr = {}
    for z in ('RO', 'BG', 'HU'):
        for tech, key in (('solar', 'solar'), ('wind_onshore', 'wind')):
            for y in range(2019, Y + 1):
                m = pd.Series(YR == y, index=PX.index)
                if GR[z][tech][m].notna().sum() < 0.9 * m.sum():
                    continue
                cp, base, e = capture(z, tech, m)
                cr.setdefault(z, {}).setdefault(key, {})[str(y)] = [round(cp, 1), round(base, 1), round(e / 1e6, 2), round(cp / base, 4)]
    out['cr'] = cr

    # 3. monthly capture rate vs solar share of load
    mon = {}
    for z in ('RO', 'BG', 'HU'):
        rows = []
        for per in pd.period_range('2019-01', END.strftime('%Y-%m'), freq='M'):
            mk = pd.Series(MO == per, index=PX.index)
            if GR[z]['solar'][mk].notna().sum() < 0.9 * mk.sum() or PX[z][mk].notna().sum() < 0.9 * mk.sum():
                continue
            cp, base, e = capture(z, 'solar', mk)
            ld = (GR[z]['load'][mk] * PX['dur'][mk]).sum()
            rows.append([str(per), round(cp / base * 100, 2), round(e / ld * 100, 2)])
        mon[z] = rows
        if z == 'RO':
            a = np.array([[r[1], r[2]] for r in rows])
            b = sm.OLS(a[:, 0], sm.add_constant(a[:, 1])).fit().params[1]
            print(f'  check cannibalisation slope RO: {b:.2f} (lecture -4.2)')
    out['cn'] = mon

    # 4. negative prices: hour-equivalents by month x hour of the day, mean negative price by month
    nh = {}
    for z in ZONES:
        nh[z] = {}
        for y in range(2022, Y + 1):
            m = (YR == y) & PX[z].notna().values & (PX[z] < 0).values
            s = PX[m]
            heat = np.zeros((12, 24))
            np.add.at(heat, (s.index.month - 1, s.index.hour), s['dur'].values)
            dep = [None] * 12
            for mm in range(12):
                k = s.index.month == mm + 1
                if k.any():
                    dep[mm] = round(float((s[z][k] * s['dur'][k]).sum() / s['dur'][k].sum()), 1)
            nh[z][str(y)] = {'h': rnd(heat, 2), 'd': dep}
    out['nh'] = nh

    # 5. battery: perfect-foresight revenue per day for durations x efficiencies, aggregated by year
    T0 = pd.Timestamp('2019-01-01').tz_localize(TZ)
    dg = {z: day_groups(PX, z, T0) for z in ZONES}
    key = hashlib.md5(pd.util.hash_pandas_object(PX[ZONES].fillna(-9999)).values.tobytes() + b'L6-int-bat-v1').hexdigest()
    cache = os.path.join(HERE, 'cache', 'interactive_battery.pkl')
    BAT = pickle.load(open(cache, 'rb')) if os.path.exists(cache) else {}
    if BAT.get('key') != key:
        from multiprocessing import Pool
        print('  battery: daily linear programmes (a few minutes) ...')
        jobs, idx = [], []
        for z in ZONES:
            days = list(dg[z].keys())
            vals = list(dg[z].values())
            for E in DURS:
                for eta in ETAS:
                    for i in range(0, len(vals), 200):
                        jobs.append((vals[i:i + 200], E, eta))
                        idx.append((z, E, eta, days[i:i + 200]))
        with Pool(max(1, (os.cpu_count() or 2) - 2)) as pool:
            res = pool.map(_bat_job, jobs)
        BAT = {'key': key}
        for (z, E, eta, days), r in zip(idx, res):
            BAT.setdefault((z, E, eta), {}).update(dict(zip(days, r)))
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        pickle.dump(BAT, open(cache, 'wb'))
    bt = {}
    for z in ZONES:
        bt[z] = {}
        for y in range(2019, Y + 1):
            ent = {}
            for E in DURS:
                v = []
                for eta in ETAS:
                    s = pd.Series(BAT[(z, E, eta)])
                    s = s[s.index.year == y]
                    v.append(round(float(s.sum()) / 1000, 2))
                ent[str(E)] = v
            n = sum(1 for d_ in dg[z] if d_.year == y)
            if n:
                ent['n'] = n
                bt[z][str(y)] = ent
    out['bt'] = {'etas': [int(round(e * 100)) for e in ETAS], 'durs': list(DURS), 'v': bt}
    print('  check battery RO 2025 2h eta .85:', bt['RO']['2025']['2'][2], '(lecture 98.7)')

    # 6. summer 2026: Romania's cross-border flows and RO / BG prices by day x hour (Romanian time)
    TZL = 'Europe/Bucharest'
    CB = pd.read_csv(os.path.join(DATA, 'crossborder_ro_mw_hourly_utc.csv'), parse_dates=['timestamp_utc']).set_index('timestamp_utc')
    CB.index = pd.to_datetime(CB.index, utc=True).tz_convert(TZL)
    PH = pd.read_csv(os.path.join(DATA, 'power_da_prices_hourly_utc.csv'), parse_dates=['timestamp_utc']).set_index('timestamp_utc')
    PH.index = pd.to_datetime(PH.index, utc=True).tz_convert(TZL)
    summer = (CB.index.year == 2026) & CB.index.month.isin([6, 7, 8])
    RG = CB.loc[summer, ['bulgaria', 'hungary', 'serbia', 'sum']].join(PH[['RO', 'BG']], how='left')
    days = sorted(set(RG.index.tz_localize(None).normalize()))
    rg = {'days': [str(d_.date()) for d_ in days]}
    for c in ['bulgaria', 'hungary', 'serbia', 'sum', 'RO', 'BG']:
        M = np.full((len(days), 24), np.nan)
        di = {d_: i for i, d_ in enumerate(days)}
        for t, v in RG[c].items():
            M[di[t.tz_localize(None).normalize()], t.hour] = v
        rg[c] = rnd(M, 1)
    out['rg'] = rg
    return out


if __name__ == '__main__':
    interactive_common.build(sys.modules[__name__])
