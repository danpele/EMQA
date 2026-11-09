"""Build the interactive page of Lecture 5 (Derivatives and hedging): interactive/L5.html (EN) and interactive/L5_ro.html (RO).

Inputs (interactive/L5_data.js) are computed here from data/clean (OPCOM forward trades, day-ahead prices, TTF, EUA, coal,
EUR/USD, €STR) with the same rules as lectures/L5/analysis_L5.py; the page logic is in interactive/L5.js.
Run: python3 lectures/L5/build_interactive_L5.py [--no-data]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import interactive_common  # noqa: E402
from interactive_common import slider, select, toggles, play, charts, rnd, csv  # noqa: E402

K = 5

# (anchor, chart file / Quantlet, section key, id prefix)
BLOCKS = [('forward-curve', 'fwd_curve', 'fwd', 'fc'),
          ('spreads', 'spreads', 'spr', 'sp'),
          ('hedge-ratio', 'hedge_scatter', 'hedge', 'hr'),
          ('basis', 'basis', 'hedge', 'bs'),
          ('samuelson', 'samuelson', 'opt', 'sm'),
          ('black76-collar', 'collar', 'opt', 'bk')]

SECTIONS = {
 'en': dict(fwd='Forwards, futures and the forward curve', spr='Spreads: the margins of power plants',
            hedge='Hedge ratio, basis risk and shape risk', opt='Options on energy'),
 'ro': dict(fwd='Contracte forward, futures și curba forward', spr='Marjele centralelor electrice',
            hedge='Raportul de acoperire, riscul de bază și riscul de profil', opt='Opțiuni pe energie'),
}

L = {
 'en': dict(h1='Lecture 5 · Derivatives and hedging',
   note='The slide of the lecture is on the left, the same figure on the right, recomputed in your browser from the course data '
        '(data/clean) when you move a control. The ▶ button moves the main parameter step by step. Under each figure: a readout, '
        'a question for the room and the Quantlet with the code of the chart.',
   src='Forward trades: OPCOM (Romanian power exchange), PCCB-LE-flex and related forward markets, baseload ("banda") products, prices '
       'converted to EUR/MWh at the ECB (European Central Bank) EUR/RON rate. Day-ahead prices: OPCOM PZU, HUPX, EPEX via '
       'energy-charts.info. TTF (Title Transfer Facility) gas: World Bank monthly series and single futures contracts; EUA (EU Allowance) '
       'carbon prices: EEX auctions; coal: World Bank (South Africa, Richards Bay); €STR (euro short-term rate): ECB. Monthly averages '
       'only for complete months. Data to the cut-off of the lecture (31 October 2026).'),
 'ro': dict(h1='Cursul 5 · Instrumente derivate și acoperirea riscului',
   note='În stînga este slide-ul din curs, în dreapta aceeași figură, recalculată în browser din datele cursului (data/clean) cînd '
        'modificați un control. Butonul ▶ modifică parametrul principal pas cu pas. Sub fiecare figură: o sinteză numerică, o întrebare '
        'pentru sală și Quantlet-ul cu codul figurii.',
   src='Tranzacții forward: OPCOM (bursa de energie din România), PCCB-LE-flex și piețele forward asociate, produse de bandă, prețuri '
       'convertite în EUR/MWh la cursul EUR/RON al BCE (Banca Centrală Europeană). Prețuri pentru ziua următoare: OPCOM PZU, HUPX, EPEX, '
       'prin energy-charts.info. Gaze TTF (Title Transfer Facility): seria lunară a Băncii Mondiale și contracte futures individuale; '
       'certificate de emisii EUA (EU Allowance): licitațiile EEX; cărbune: Banca Mondială (Africa de Sud, Richards Bay); €STR (rata '
       'euro pe termen scurt): BCE. Mediile lunare doar pentru lunile complete. Date pînă la data-limită a cursului (31 octombrie 2026).'),
}


def widgets(lang):
    ro = lang == 'ro'
    return {
     'forward-curve': (slider('fc-t', 'Curba la sfîrșitul lunii' if ro else 'Curve at the end of', 0, 1, 1, 1)
                       + slider('fc-w', 'Fereastra licitațiilor (luni)' if ro else 'Window of auctions (months)', 1, 6, 1, 2) + play('fc'),
                       charts('fc-chart', cls='one')),
     'spreads': (select('sp-z', 'Zona' if ro else 'Zone', [('RO', 'România' if ro else 'Romania'),
                                                           ('DE_LU', 'Germania–Luxemburg' if ro else 'Germany–Luxembourg')], 'RO')
                 + slider('sp-g', 'Randamentul centralei pe gaz, η' if ro else 'Efficiency of the gas plant, η', 0.35, 0.62, 0.01, 0.5)
                 + slider('sp-c', 'Randamentul centralei pe cărbune, η' if ro else 'Efficiency of the coal plant, η', 0.30, 0.46, 0.01, 0.38)
                 + play('sp'), charts('sp-chart', cls='one')),
     'hedge-ratio': (select('hr-z', 'Instrumentul de acoperire' if ro else 'Hedging instrument',
                            [('HU', 'Prețul din Ungaria' if ro else 'Hungarian price'),
                             ('DE_LU', 'Prețul din Germania–Luxemburg' if ro else 'German–Luxembourg price')], 'HU')
                     + slider('hr-a', 'Primul an al eșantionului' if ro else 'First year of the sample', 2015, 2024, 1, 2015)
                     + slider('hr-b', 'Ultimul an al eșantionului' if ro else 'Last year of the sample', 2016, 2026, 1, 2026) + play('hr'),
                     charts('hr-sc', 'hr-roll')),
     'basis': (select('bs-z', 'Zona de referință' if ro else 'Reference zone',
                      [('HU', 'Ungaria' if ro else 'Hungary'), ('DE_LU', 'Germania–Luxemburg' if ro else 'Germany–Luxembourg')], 'HU')
               + slider('bs-s', 'Anul de separare (înainte / după)' if ro else 'Split year (before / after)', 2017, 2025, 1, 2021) + play('bs'),
               charts('bs-chart', 'bs-conv')),
     'samuelson': (toggles('sm-c', 'Contracte TTF' if ro else 'TTF contracts',
                           [(c, lab) for c, lab in (('2026-12', 'dec 2026' if ro else 'Dec 2026'), ('2027-01', 'ian 2027' if ro else 'Jan 2027'),
                                                    ('2027-02', 'feb 2027' if ro else 'Feb 2027'), ('2027-05', 'mai 2027' if ro else 'May 2027'))],
                           ['2026-12', '2027-05'])
                   + slider('sm-w', 'Fereastra volatilității (zile de tranzacționare)' if ro else 'Volatility window (trading days)', 20, 250, 10, 60)
                   + play('sm'), charts('sm-chart', cls='one')),
     'black76-collar': (slider('bk-F', 'Prețul forward F (EUR/MWh)' if ro else 'Forward price F (EUR/MWh)', 80, 250, 0.01, 148.12)
                        + slider('bk-s', 'Volatilitatea σ (% pe an)' if ro else 'Volatility σ (% a year)', 5, 100, 0.01, 22.02)
                        + slider('bk-T', 'Zile pînă la scadență' if ro else 'Days to expiry', 1, 365, 1, 45)
                        + slider('bk-r', 'Rata dobînzii r (% pe an)' if ro else 'Interest rate r (% a year)', 0, 6, 0.01, 2.44)
                        + slider('bk-c', 'Plafon: strike-ul call-ului (% din F)' if ro else 'Cap: call strike (% of F)', 100, 130, 1, 110)
                        + slider('bk-p', 'Prag: strike-ul put-ului (% din F)' if ro else 'Floor: put strike (% of F)', 70, 100, 1, 90)
                        + play('bk'), charts('bk-pay', 'bk-prem')),
    }


QA = {
 'en': {
  'forward-curve': ('At the end of October 2026, the October day-ahead average in Romania was 239.32 EUR/MWh, while the calendar 2027 baseload '
                    'traded at 148.12 EUR/MWh. Does the downward slope of the curve mean that the market expects spot prices to fall by about 90 EUR/MWh?',
                    'Not exactly. A forward price is the expected spot price plus a risk premium, and part of the gap is seasonal: November and December '
                    '2026 traded at 215.33 and 214.27 EUR/MWh, the first quarter of 2027 at 176.69 and the whole year at 148.12, which also averages '
                    'the cheap solar summer. Move the slider back: in 2022 the curve sloped down from a crisis spot, and the Cal-2023 product (calendar '
                    'year 2023) traded at up to 509.18 EUR/MWh, while 2023 delivered 103.74 EUR/MWh on the day-ahead market.'),
  'spreads': ('With the course assumptions (gas plant efficiency 50%, coal 38%), the Romanian clean spark spread was negative in 67 of 138 months. '
              'What happens to this count if the gas plant is a modern combined cycle with an efficiency of 58%?',
              'The count falls, because a higher efficiency lowers both the fuel cost and the carbon cost per MWh of electricity: '
              'clean spark spread = p − gas/η − (0.202/η)·EUA. At 0.58 the count falls from 67 to 29 months. '
              'The clean dark spread of coal does not change with the gas slider: the switch between gas and coal depends on the relative cost, '
              'not on the price of power alone.'),
  'hedge-ratio': ('Monthly changes of the Romanian price are hedged with the Hungarian price. Over 2015–2026 the minimum-variance hedge ratio '
                  'is h* = 0.966. Is the hedge ratio with the German price lower, and why?',
                  'Yes: h* = 0.875 with R² = 0.80, against R² = 0.98 for Hungary. The hedge ratio is h* = ρ·σ_RO/σ_F; Romania and Hungary are coupled '
                  'and often share the same price, while Germany is farther away in the grid and its price moves partly for other reasons (wind, '
                  'solar, its own interconnections). The variance left after the hedge is 1 − R²: about 2% with Hungary and about a fifth with Germany.'),
  'basis': ('The basis is the difference between the Romanian price and the price of the hedging instrument. Did the RO–HU basis become more '
            'or less volatile after 2021?',
            'More volatile: the standard deviation of the monthly RO–HU basis rises from 2.82 EUR/MWh before 2021 to 5.77 EUR/MWh from 2021, '
            'and that of RO–DE from 7.61 to 18.23 EUR/MWh. At the same time Romania and Hungary still share exactly the same price in many hours '
            '(the right panel): a basis that is usually zero but occasionally large is the typical risk left by a cross-border hedge.'),
  'samuelson': ('Over the last 12 months, the TTF contract for December 2026 had an annualised volatility of 63.0%, the May 2027 contract 47.7%. '
                'Why does the nearer contract move more?',
                'This is the Samuelson effect: shocks to supply and demand (storage, weather, cargoes of LNG, liquefied natural gas) mostly affect the price for delivery '
                'soon, and are expected to fade before a distant delivery month. As expiry approaches, the futures price behaves more and more like '
                'the spot price, and its volatility rises. In 2022 the difference was small (66.1% against 66.8%): in a crisis even distant '
                'months moved as much as the front.'),
  'black76-collar': ('With F = 148.12 EUR/MWh, σ = 22.0%, 45 days to expiry and r = 2.44%, the at-the-money call costs 4.55 EUR/MWh. '
                     'How much does a cap at 1.1·F cost, and how much does a collar 0.9·F – 1.1·F cost?',
                     'The cap (a call with strike 162.93) costs 0.63 EUR/MWh, about 5,500 EUR for 1 MW over a year; selling a put with strike '
                     '133.31 (0.43 EUR/MWh) brings the collar to 0.20 EUR/MWh. The buyer gives up the gains below the floor in exchange for a '
                     'cheaper cap. Raise σ to 50% (close to the volatility of near TTF contracts): the at-the-money call rises to 10.33 and the collar to 0.88 EUR/MWh, and the call and the put at K = F '
                     'stay equal, as put–call parity requires (C − P = e<sup>−rT</sup>(F − K)).'),
 },
 'ro': {
  'forward-curve': ('La sfîrșitul lui octombrie 2026, media PZU (piața pentru ziua următoare) din România în octombrie era 239,32 EUR/MWh, iar '
                    'banda pentru anul calendaristic 2027 se tranzacționa la 148,12 EUR/MWh. Înseamnă panta descendentă a curbei că piața se '
                    'așteaptă ca prețul spot să scadă cu aproximativ 90 EUR/MWh?',
                    'Nu întocmai. Prețul forward este prețul spot așteptat plus o primă de risc, iar o parte din diferență este sezonieră: '
                    'noiembrie și decembrie 2026 s-au tranzacționat la 215,33 și 214,27 EUR/MWh, primul trimestru din 2027 la 176,69, iar anul '
                    'întreg la 148,12, care include și vara ieftină, cu producție solară mare. Mutați cursorul înapoi: în 2022, curba cobora de la '
                    'un spot de criză, iar produsul Cal-2023 (anul calendaristic 2023) s-a tranzacționat pînă la 509,18 EUR/MWh, în timp ce în 2023 '
                    'media PZU a fost 103,74 EUR/MWh.'),
  'spreads': ('Cu ipotezele din curs (randamentul centralei pe gaz 50%, al celei pe cărbune 38%), spread-ul clean spark din România a fost '
              'negativ în 67 din 138 de luni. Ce se întîmplă cu acest număr dacă centrala pe gaz este un ciclu combinat modern, cu randamentul 58%?',
              'Numărul scade, deoarece un randament mai mare reduce atît costul combustibilului, cît și costul emisiilor pe MWh de energie '
              'electrică: clean spark spread = p − gaz/η − (0,202/η)·EUA. La 0,58, numărul scade de la 67 la 29 de luni. Spread-ul '
              'clean dark al cărbunelui nu se schimbă cu acest cursor: alegerea între gaz și cărbune depinde de costul relativ, nu doar de prețul energiei.'),
  'hedge-ratio': ('Variațiile lunare ale prețului din România sînt acoperite cu prețul din Ungaria. Pe 2015–2026, raportul de acoperire de '
                  'varianță minimă este h* = 0,966. Este mai mic raportul cu prețul din Germania și de ce?',
                  'Da: h* = 0,875, cu R² = 0,80, față de R² = 0,98 pentru Ungaria. Raportul de acoperire este h* = ρ·σ_RO/σ_F; România și Ungaria '
                  'sînt cuplate și au adesea același preț, în timp ce Germania este mai departe în rețea, iar prețul ei se mișcă parțial din alte '
                  'cauze (vînt, solar, propriile interconexiuni). Varianța rămasă după acoperire este 1 − R²: circa 2% cu Ungaria și circa o '
                  'cincime cu Germania.'),
  'basis': ('Baza este diferența dintre prețul din România și prețul instrumentului de acoperire. A devenit baza RO–HU mai volatilă sau mai '
            'puțin volatilă după 2021?',
            'Mai volatilă: abaterea standard a bazei lunare RO–HU crește de la 2,82 EUR/MWh înainte de 2021 la 5,77 EUR/MWh din 2021, iar a '
            'bazei RO–DE de la 7,61 la 18,23 EUR/MWh. În același timp, România și Ungaria au încă exact același preț în multe ore (panoul din '
            'dreapta): o bază de obicei nulă, dar ocazional mare, este riscul tipic lăsat de o acoperire printr-o altă zonă.'),
  'samuelson': ('În ultimele 12 luni, contractul TTF pentru decembrie 2026 a avut volatilitatea anualizată 63,0%, iar contractul pentru mai '
                '2027 47,7%. De ce se mișcă mai mult contractul mai apropiat?',
                'Acesta este efectul Samuelson: șocurile de cerere și ofertă (stocuri, vreme, transporturi de GNL, adică gaz natural lichefiat) '
                'afectează mai ales prețul pentru livrarea apropiată și se așteaptă să dispară înainte de o lună de livrare îndepărtată. Pe măsură '
                'ce scadența se apropie, prețul futures se comportă tot mai mult ca prețul spot, iar volatilitatea lui crește. În 2022, diferența '
                'a fost mică (66,1% față de 66,8%): într-o criză, chiar și lunile îndepărtate s-au mișcat cît contractul apropiat.'),
  'black76-collar': ('Cu F = 148,12 EUR/MWh, σ = 22,0%, 45 de zile pînă la scadență și r = 2,44%, call-ul la bani (K = F) costă 4,55 EUR/MWh. '
                     'Cît costă un plafon (cap) la 1,1·F și cît costă un collar 0,9·F – 1,1·F?',
                     'Plafonul (un call cu strike 162,93) costă 0,63 EUR/MWh, adică circa 5.500 EUR pentru 1 MW pe un an; vînzarea unui put cu '
                     'strike 133,31 (0,43 EUR/MWh) aduce costul collar-ului la 0,20 EUR/MWh. Cumpărătorul renunță la cîștigurile de sub prag în '
                     'schimbul unui plafon mai ieftin. Ridicați σ la 50% (aproape de volatilitatea contractelor TTF apropiate): call-ul la bani crește la 10,33, iar collar-ul la 0,88 EUR/MWh, iar '
                     'call-ul și put-ul la K = F rămîn egale, cum cere paritatea put–call (C − P = e<sup>−rT</sup>(F − K)).'),
 },
}

TEXT_JS = {
 'en': r"""window.LK_TEXT = {
 eur: 'EUR/MWh', delivery: 'Delivery period', kind: { M: 'month', Q: 'quarter', H: 'half-year', Y: 'calendar year' },
 kindPl: { M: 'Monthly products', Q: 'Quarterly products', H: 'Half-year products', Y: 'Calendar-year products' },
 spot: 'Realised day-ahead price, Romania (monthly mean)', asof: 'Curve date',
 fcTitle: (d, w) => `Baseload forward curve at ${d} (volume-weighted average price, VWAP, of the auctions in the last ${w === 1 ? 'month' : w + ' months'})`,
 fc: (n, np, s) => `${window.EMQAI.cnt(n, 'auction', 'auctions')}, ${window.EMQAI.cnt(np, 'product', 'products')}; mean day-ahead price in the last month: ${s} EUR/MWh.`,
 fcItem: (k, a, b, f, r) => `${k} ${a}${b ? '–' + b : ''}: ${f} EUR/MWh` + (r ? `, realised ${r}` : ''),
 fc0: 'No baseload product with delivery after this date was auctioned in the window.',
 spTitle: z => `Monthly spreads, ${z} (EUR per MWh of electricity)`,
 css: 'Clean spark spread (gas)', cds: 'Clean dark spread (coal)',
 sp: (n, nm, nd, last, ym, c, d) => `Clean spark spread negative in ${nm} of ${window.EMQAI.cnt(n, 'month', 'months')}; clean dark spread negative in ${nd}. ${ym}: clean spark ${c}, clean dark ${d} EUR/MWh.`,
 sp2: (g, c, e) => `Cost of 1 MWh of electricity in the last month: gas ${g} EUR (fuel + CO₂), coal ${c} EUR; EUA ${e} EUR/t.`,
 dRO: 'Monthly change, Romania (EUR/MWh)', dF: z => `Monthly change, ${z} (EUR/MWh)`, fit: 'h* line', roll: 'Rolling 36-month h*',
 hr: (z, a, b, n, h, r2, rho) => `${z}, ${a}–${b} (${window.EMQAI.cnt(n, 'monthly change', 'monthly changes')}): h* = ${h}, R² = ${r2}, correlation ${rho}.`,
 hr2: (v0, vh, v1) => `Standard deviation of the monthly change of the Romanian price: ${v0} EUR/MWh unhedged, ${vh} hedged with h*, ${v1} hedged one for one.`,
 hrRoll: 'h* on the previous 36 months',
 bsTitle: z => `Monthly basis, Romania − ${z} (EUR/MWh)`, convTitle: z => `Share of hours with the same price, Romania = ${z}`,
 bs: (z, m, s, s0, s1, y) => `Basis Romania − ${z}: mean ${m}, standard deviation ${s} EUR/MWh; before ${y}: ${s0}, from ${y}: ${s1}.`,
 bs2: (mx, mxd, mn, mnd) => `Largest basis ${mx} EUR/MWh (${mxd}), smallest ${mn} EUR/MWh (${mnd}).`,
 smTitle: w => `Annualised volatility of daily log returns, ${w}-day window (%)`,
 sm: (c, v, v22) => `${c}: last 12 months ${v}%, 2022 ${v22}%.`,
 vol: '% a year', month: { '2026-12': 'December 2026', '2027-01': 'January 2027', '2027-02': 'February 2027', '2027-05': 'May 2027' },
 payTitle: 'Effective purchase price at expiry (EUR/MWh)', premTitle: 'Black-76 premium by strike (EUR/MWh)',
 FT: 'Forward price at expiry, F_T (EUR/MWh)', strike: 'Strike K (EUR/MWh)',
 unhedged: 'Unhedged', fwd: 'Forward at F', cap: 'Cap (call bought)', collar: 'Collar', call: 'Call', put: 'Put',
 bk: (c, p, dc, dp, v) => `At the money (K = F): call ${c}, put ${p} EUR/MWh; delta ${dc} / ${dp}; vega ${v} EUR/MWh per volatility point.`,
 bk2: (kc, c, kp, p, col, y) => `Cap K = ${kc}: ${c} EUR/MWh (${y} EUR for 1 MW over a year); floor K = ${kp}: put ${p}; collar costs ${col} EUR/MWh.`
};
""",
 'ro': r"""window.LK_TEXT = {
 eur: 'EUR/MWh', delivery: 'Perioada de livrare', kind: { M: 'luna', Q: 'trimestrul', H: 'semestrul', Y: 'anul' },
 kindPl: { M: 'Produse lunare', Q: 'Produse trimestriale', H: 'Produse semestriale', Y: 'Produse anuale' },
 spot: 'Prețul PZU realizat, România (media lunară)', asof: 'Data curbei',
 fcTitle: (d, w) => `Curba forward de bandă la ${d} (prețul mediu ponderat cu volumul, VWAP, al licitațiilor din ${w === 1 ? 'ultima lună' : 'ultimele ' + w + ' luni'})`,
 fc: (n, np, s) => `${window.EMQAI.cnt(n, 'licitație', 'licitații')}, ${window.EMQAI.cnt(np, 'produs', 'produse')}; prețul PZU mediu în ultima lună: ${s} EUR/MWh.`,
 fcItem: (k, a, b, f, r) => `${k} ${a}${b ? '–' + b : ''}: ${f} EUR/MWh` + (r ? `, realizat ${r}` : ''),
 fc0: 'În fereastra aleasă nu s-a licitat niciun produs de bandă cu livrare după această dată.',
 spTitle: z => `Spread-uri lunare, ${z} (EUR pe MWh de energie electrică)`,
 css: 'Clean spark spread (gaz)', cds: 'Clean dark spread (cărbune)',
 sp: (n, nm, nd, last, ym, c, d) => `Clean spark spread negativ în ${nm} din ${window.EMQAI.cnt(n, 'lună', 'luni')}; clean dark spread negativ în ${nd}. ${ym}: clean spark ${c}, clean dark ${d} EUR/MWh.`,
 sp2: (g, c, e) => `Costul unui MWh de energie electrică în ultima lună: gaz ${g} EUR (combustibil + CO₂), cărbune ${c} EUR; EUA ${e} EUR/t.`,
 dRO: 'Variația lunară, România (EUR/MWh)', dF: z => `Variația lunară, ${z} (EUR/MWh)`, fit: 'Dreapta h*', roll: 'h* pe 36 de luni',
 hr: (z, a, b, n, h, r2, rho) => `${z}, ${a}–${b} (${window.EMQAI.cnt(n, 'variație lunară', 'variații lunare')}): h* = ${h}, R² = ${r2}, corelația ${rho}.`,
 hr2: (v0, vh, v1) => `Abaterea standard a variației lunare a prețului din România: ${v0} EUR/MWh fără acoperire, ${vh} cu acoperire h*, ${v1} cu acoperire unu la unu.`,
 hrRoll: 'h* pe ultimele 36 de luni',
 bsTitle: z => `Baza lunară, România − ${z} (EUR/MWh)`, convTitle: z => `Ponderea orelor cu același preț, România = ${z}`,
 bs: (z, m, s, s0, s1, y) => `Baza România − ${z}: media ${m}, abaterea standard ${s} EUR/MWh; înainte de ${y}: ${s0}, din ${y}: ${s1}.`,
 bs2: (mx, mxd, mn, mnd) => `Baza maximă ${mx} EUR/MWh (${mxd}), minimă ${mn} EUR/MWh (${mnd}).`,
 smTitle: w => `Volatilitatea anualizată a randamentelor zilnice logaritmice, fereastră de ${w % 100 >= 1 && w % 100 <= 19 ? w : w + ' de'} zile (%)`,
 sm: (c, v, v22) => `${c}: ultimele 12 luni ${v}%, 2022 ${v22}%.`,
 vol: '% pe an', month: { '2026-12': 'decembrie 2026', '2027-01': 'ianuarie 2027', '2027-02': 'februarie 2027', '2027-05': 'mai 2027' },
 payTitle: 'Prețul efectiv de cumpărare la scadență (EUR/MWh)', premTitle: 'Prima Black-76 în funcție de strike (EUR/MWh)',
 FT: 'Prețul forward la scadență, F_T (EUR/MWh)', strike: 'Strike-ul K (EUR/MWh)',
 unhedged: 'Fără acoperire', fwd: 'Forward la F', cap: 'Plafon (call cumpărat)', collar: 'Collar', call: 'Call', put: 'Put',
 bk: (c, p, dc, dp, v) => `La bani (K = F): call ${c}, put ${p} EUR/MWh; delta ${dc} / ${dp}; vega ${v} EUR/MWh pe punct de volatilitate.`,
 bk2: (kc, c, kp, p, col, y) => `Plafon K = ${kc}: ${c} EUR/MWh (${y} EUR pentru 1 MW pe un an); prag K = ${kp}: put ${p}; collar-ul costă ${col} EUR/MWh.`
};
""",
}


# ---------------------------------------------------------------- data (real course data only, rules of analysis_L5.py)
def data():
    import numpy as np
    import pandas as pd
    PD = csv('power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')
    raw = PD['RO'].dropna().index.max()
    END = pd.Timestamp(((raw + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())
    PD = PD.loc[:END]
    out = {'end': str(END.date())}

    # forward trades: baseload products with a standard delivery period
    FW = csv('opcom_forward_trades.csv', parse_dates=['auction_date', 'delivery_start', 'delivery_end'])
    FW = FW[(FW['auction_date'] <= END) & (FW['profile'] == 'banda LD')].copy()

    def kind_of(s, e):
        if s.day != 1 or (e + pd.Timedelta(days=1)).day != 1:
            return 'other'
        n = (e.year - s.year) * 12 + e.month - s.month + 1
        return {1: 'M', 3: 'Q' if s.month in (1, 4, 7, 10) else 'other', 6: 'H' if s.month in (1, 7) else 'other',
                12: 'Y' if s.month == 1 else 'other'}.get(n, 'other')

    FW['kind'] = [kind_of(s, e) for s, e in zip(FW['delivery_start'], FW['delivery_end'])]
    FW = FW[FW['kind'] != 'other'].sort_values('auction_date')
    out['fw'] = {'d': FW['auction_date'].dt.strftime('%Y-%m-%d').tolist(), 's': FW['delivery_start'].dt.strftime('%Y-%m').tolist(),
                 'e': FW['delivery_end'].dt.strftime('%Y-%m').tolist(), 'k': FW['kind'].tolist(),
                 'p': rnd(FW['price_eur_mwh'].values, 2), 'q': rnd(FW['mwh'].values, 0)}

    # monthly day-ahead means, complete months only
    m_idx = pd.date_range('2015-01-01', END.replace(day=1), freq='MS')
    PM = PD[['RO', 'HU', 'DE_LU']].resample('MS').mean().reindex(m_idx)
    NDM = PD[['RO', 'HU', 'DE_LU']].resample('MS').count().reindex(m_idx)
    PM = PM.where(NDM.eq(pd.Series(m_idx.days_in_month, index=m_idx), axis=0))
    out['m'] = {'t': [t.strftime('%Y-%m') for t in m_idx], **{z: rnd(PM[z].values, 2) for z in ['RO', 'HU', 'DE_LU']}}

    # fuels and carbon (monthly), as analysis_L5.py
    TTF = csv('ttf_monthly.csv')
    TTF.index = pd.PeriodIndex(TTF['month'], freq='M').to_timestamp()
    EUA = csv('eua_daily.csv', parse_dates=['date']).set_index('date')
    COAL = csv('coal_monthly.csv')
    COAL.index = pd.PeriodIndex(COAL['month'], freq='M').to_timestamp()
    FUEL = csv('fuels_daily.csv', parse_dates=['date']).set_index('date')
    eua_a = EUA['eua_eex_auction_eur_t'].dropna().resample('MS').mean()
    eua_e = EUA['eua_etc_co2l_eur_per_unit'].dropna().resample('MS').mean()
    EUAM = eua_a.reindex(m_idx).fillna(eua_e.reindex(m_idx).where(m_idx > eua_a.index.max()))
    fxm = FUEL['eurusd_ecb'].resample('MS').mean().reindex(m_idx)
    out['m']['gas'] = rnd(TTF['ttf_eur_mwh'].reindex(m_idx).values, 2)
    out['m']['coal'] = rnd(((COAL['coal_southafrica_usd_t'].reindex(m_idx) / fxm) / 6.978).values, 3)
    out['m']['eua'] = rnd(EUAM.values, 2)

    # hours with the same price in Romania and the reference zone (|difference| < 0.01 EUR/MWh), duration-weighted, by year
    HP = csv('power_da_prices_native_utc.csv', parse_dates=['timestamp_utc']).set_index('timestamp_utc')
    HP.index = HP.index.tz_convert('Europe/Brussels')
    HP = HP.loc[:str(END.date())]
    w = HP['mtu_minutes'] / 60
    conv = {}
    for z in ['HU', 'DE_LU']:
        ok = HP['RO'].notna() & HP[z].notna()
        same = (w * ((HP['RO'] - HP[z]).abs() < 0.01))[ok]
        c = same.groupby(HP.index[ok].year).sum() / w[ok].groupby(HP.index[ok].year).sum() * 100
        conv[z] = {str(y): rnd(v, 1) for y, v in c.items()}
    out['conv'] = conv

    # TTF single futures contracts (daily settlement prices)
    TC = csv('ttf_futures_contracts_daily.csv', parse_dates=['date']).set_index('date').loc[:END]
    out['ttf'] = {'t': TC.index.strftime('%Y-%m-%d').tolist(), **{c: rnd(TC[c].values, 3) for c in TC.columns}}

    # Black-76 defaults: Cal-2027 VWAP of the last two months, latest €STR, expiry 15 December
    R = csv('ecb_ron_estr_daily.csv', parse_dates=['date']).set_index('date')['estr_pct'].loc[:END].dropna()
    cur = FW[(FW['auction_date'] >= (END - pd.DateOffset(months=2) + pd.Timedelta(days=1)).normalize())
             & (FW['delivery_start'] > END) & (FW['kind'] == 'Y')]
    cal = cur[cur['delivery_start'].dt.year == END.year + 1]
    out['bk'] = {'F': rnd(float(np.average(cal['price_eur_mwh'], weights=cal['mwh'])), 2), 'r': rnd(float(R.iloc[-1]), 3),
                 'T': int((pd.Timestamp(f'{END.year}-12-15') - END).days), 'sig': 22.02}
    return out


if __name__ == '__main__':
    interactive_common.build(sys.modules[__name__])
