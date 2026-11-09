"""Build the interactive page of Lecture 4 (Risk for energy companies): interactive/L4.html (EN) and interactive/L4_ro.html (RO).

Inputs (interactive/L4_data.js) are computed here from data/clean (day-ahead prices, hourly load) and from the rolling VaR/ES
forecasts of lectures/L4/cache/engine.pkl (written by analysis_L4.py; run it first if the cache is missing). The page logic is
in interactive/L4.js. Run: python3 lectures/L4/build_interactive_L4.py [--no-data]
"""
import os
import pickle
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import interactive_common  # noqa: E402
from interactive_common import slider, select, toggles, play, charts, rnd, csv, cutoff  # noqa: E402

K = 4
METHODS = ['hs', 'normal', 't', 'fhs', 'evt']

# (anchor, chart file / Quantlet, section key, id prefix)
BLOCKS = [('var-es', 'tails', 'risk', 've'),
          ('var-paths', 'var_paths', 'est', 'vp'),
          ('gpd-tail', 'gpd_tail', 'est', 'gp'),
          ('traffic-light', 'traffic', 'bt', 'tl'),
          ('horizon', 'horizon', 'coll', 'hz'),
          ('supplier', 'supplier_month', 'pos', 'sm')]

SECTIONS = {
 'en': dict(risk='Price risk: losses, quantiles, VaR and ES', est='Estimating VaR and ES: four methods',
            bt='Backtesting VaR and ES', coll='From quantiles to margins, guarantees and limits',
            pos='Price risk for suppliers and producers'),
 'ro': dict(risk='Riscul de preț: pierderi, cuantile, VaR și ES', est='Estimarea VaR și ES: patru metode',
            bt='Testarea retrospectivă a VaR și ES', coll='De la cuantile la marje, garanții și limite',
            pos='Riscul de preț pentru furnizori și producători'),
}

L = {
 'en': dict(h1='Lecture 4 · Risk for energy companies',
   note='The slide of the lecture is on the left, the same figure on the right, recomputed in your browser from the course data '
        '(data/clean) when you move a control. The risk factor is the daily change of the Romanian day-ahead base price, '
        'X<sub>t</sub> = P<sub>t</sub> − P<sub>t−1</sub> (EUR/MWh): a rise is a loss for a supplier that buys on the day-ahead market. '
        'VaR (Value at Risk) is a quantile of the loss, ES (Expected Shortfall) the mean loss beyond it. The ▶ button moves the main parameter step by step.',
   src='Day-ahead base prices: OPCOM PZU (Romania), EPEX SPOT (Germany–Luxembourg), via energy-charts.info (Fraunhofer ISE) and '
       'ENTSO-E (European Network of Transmission System Operators for Electricity); hourly load of Romania: ENTSO-E (Transelectrica data). '
       'Rolling one-day-ahead VaR forecasts from 2017-01-01: lectures/L4/analysis_L4.py (each forecast uses only the changes known the day '
       'before). Data to 2026-10-31, the cut-off of the lecture.'),
 'ro': dict(h1='Cursul 4 · Riscul companiilor din energie',
   note='În stînga este slide-ul din curs, în dreapta aceeași figură, recalculată în browser din datele cursului (data/clean) cînd '
        'modificați un control. Factorul de risc este variația zilnică a prețului de bază PZU din România, '
        'X<sub>t</sub> = P<sub>t</sub> − P<sub>t−1</sub> (EUR/MWh): o creștere este o pierdere pentru un furnizor care cumpără pe piața '
        'pentru ziua următoare. VaR (Value at Risk, valoarea la risc) este o cuantilă a pierderii, ES (Expected Shortfall, pierderea '
        'așteptată în coadă) media pierderilor de dincolo de ea. Butonul ▶ modifică parametrul principal pas cu pas.',
   src='Prețurile zilnice de bază: OPCOM PZU (România), EPEX SPOT (Germania–Luxemburg), prin energy-charts.info (Fraunhofer ISE) și '
       'ENTSO-E (Rețeaua europeană a operatorilor de transport și sistem pentru energie electrică); consumul orar al României: ENTSO-E '
       '(date Transelectrica). Prognozele VaR pentru ziua următoare, din 2017-01-01: lectures/L4/analysis_L4.py (fiecare prognoză folosește '
       'doar variațiile cunoscute în ziua anterioară). Date pînă la 2026-10-31, data-limită a cursului.'),
}


def widgets(lang):
    ro = lang == 'ro'
    meth = [('hs', 'HS, simulare istorică' if ro else 'HS, historical simulation'), ('normal', 'Normală' if ro else 'Normal'),
            ('t', 'Student-t'), ('fhs', 'FHS, simulare istorică filtrată' if ro else 'FHS, filtered historical simulation'),
            ('evt', 'EVT, teoria valorilor extreme' if ro else 'EVT, extreme value theory')]
    per = [('all', '2015–2026'), ('calm', '2015–2020'), ('crisis', '2021–2022'), ('after', '2023–2026'), ('last', 'Ultimele 365 de zile' if ro else 'Last 365 days')]
    zones = [('RO', 'România' if ro else 'Romania'), ('DE_LU', 'Germania–Luxemburg' if ro else 'Germany–Luxembourg')]
    return {
     'var-es': (select('ve-z', 'Zona' if ro else 'Zone', zones, 'RO') + select('ve-p', 'Perioada' if ro else 'Period', per, 'all')
                + slider('ve-a', 'Nivelul de încredere, α (%)' if ro else 'Confidence level, α (%)', 90, 99.5, 0.5, 99) + play('ve'),
                charts('ve-hist', 've-surv')),
     'var-paths': (select('vp-m', 'Metoda' if ro else 'Method', meth, 'fhs')
                   + select('vp-L', 'Lungimea ferestrei' if ro else 'Window length', [(12, '12 luni' if ro else '12 months'), (24, '24 de luni' if ro else '24 months')], 24)
                   + select('vp-a', 'Nivelul VaR' if ro else 'VaR level', [('0.95', '95%'), ('0.99', '99%')], '0.99')
                   + slider('vp-y', 'Fereastra începe în' if ro else 'Window starts in', 2017, 2025.75, 0.25, 2021.5)
                   + play('vp'), charts('vp-chart', cls='one')),
     'gpd-tail': (slider('gp-u', 'Pragul u: cuantila reziduurilor standardizate (%)' if ro else 'Threshold u: quantile of the standardised residuals (%)', 80, 97, 1, 90)
                  + play('gp'), charts('gp-chart', 'gp-q')),
     'traffic-light': (toggles('tl-m', 'Metodele' if ro else 'Methods', [(m, t.split(',')[0]) for m, t in meth], ['hs', 'normal', 'fhs'])
                       + slider('tl-w', 'Fereastra de testare (zile)' if ro else 'Backtest window (days)', 100, 500, 25, 250)
                       + play('tl'), charts('tl-chart', cls='one')),
     'horizon': (select('hz-z', 'Zona' if ro else 'Zone', zones, 'RO')
                 + slider('hz-a', 'Nivelul cuantilei (%)' if ro else 'Quantile level (%)', 90, 99.5, 0.5, 99)
                 + slider('hz-h', 'Orizontul evidențiat, h (zile)' if ro else 'Highlighted horizon, h (days)', 1, 20, 1, 10) + play('hz'),
                 charts('hz-chart', 'hz-vr')),
     'supplier': (slider('sm-e', 'Limita estimată pe date pînă la sfîrșitul anului' if ro else 'Limit estimated on data to the end of', 2017, 2025, 1, 2020)
                  + slider('sm-a', 'Nivelul limitei (%)' if ro else 'Level of the limit (%)', 90, 99.5, 0.5, 99) + play('sm'),
                  charts('sm-chart', cls='one')),
    }


QA = {
 'en': {
  'var-es': ('A normal curve fitted to the Romanian daily price changes of 2015–2026 puts the 99% quantile at 60.18 EUR/MWh. The empirical '
             '99% quantile is 88.21 EUR/MWh. Why the gap?',
             'The daily changes have fat tails: excess kurtosis 11.97, and 52 rises above three standard deviations against 5.82 expected '
             'under the normal law. The normal VaR therefore understates the extreme quantiles, and the gap widens as α grows. ES (the mean '
             'loss beyond VaR) reacts even more, because it averages the extreme days the normal curve misses. Choose the period 2021–2022 '
             'to see both measures on the crisis years, or the last 365 days for the current risk.'),
  'var-paths': ('In July 2021–June 2023, a correct 99% VaR model should be exceeded on about 7 of the 730 days. How many exceedances do '
                'the normal model and filtered historical simulation (FHS) have?',
                'The normal model is exceeded on 45 days, historical simulation (HS) on 28, FHS on 19 and EVT on 17 (expected 7.3). All '
                'methods were too low in the crisis, but FHS, which scales the residuals by a GARCH (generalised autoregressive conditional '
                'heteroskedasticity) volatility, reacts within days to a volatility jump, while HS and the normal model, with a 365-day '
                'window, adapt only slowly. The Kupiec test in the readout compares the exceedance rate of the window with 1 − α.'),
  'gpd-tail': ('The generalised Pareto distribution (GPD) is fitted to the residuals above the threshold u. Does the estimated tail shape ξ '
               'depend on the choice of u?',
               'Yes, and this is the main practical difficulty of extreme value theory (EVT): a low threshold gives many exceedances but '
               'mixes in the body of the distribution; a high threshold uses only a few dozen points and the estimate becomes noisy. Move u '
               'from 80% to 97% and watch ξ and the implied 99.9% quantile. In the lecture, the shape at the 90% threshold varies between '
               '−0.38 and 0.33 across the 171 refits since 2017, positive in 53% of them.'),
  'traffic-light': ('Over 250 days, a correct 99% VaR model is in the green zone (at most 4 exceedances) 89.2% of the time. In which share '
                    'of the days is the normal model in the red zone (10 or more)?',
                    'In 29.5% of the days since the backtest window filled (from September 2017), against 6.2% for FHS and 2.8% for EVT; a '
                    'correct model would be red only 0.025% of the time. The zones are binomial quantiles: green while the cumulative '
                    'probability of the count under a Binomial(n, 1%) law is below 95%, red from 99.99%. Change the window to see the thresholds scale with n.'),
  'horizon': ('The square-root-of-time rule scales a 1-day VaR to 10 days by √10 = 3.16. What ratio do the Romanian prices show at the 99% level?',
              'Only 1.72 (Germany–Luxembourg: 1.75). Daily price changes are negatively autocorrelated (ρ(1) = −0.076): a price spike is '
              'followed by a fall, so changes over several days partly cancel. The variance ratio at 10 days is 0.33, far below 1. The √h '
              'rule assumes independent changes and would overstate the 10-day VaR of a flat day-ahead position.'),
  'supplier': ('A supplier budgets each month at the load-weighted price of the previous month. A normal 99% limit estimated on 2015–2020 '
               'puts the monthly cost overrun at 50.5%. How many months exceed it in 2021–2026?',
               'Three months out of 70, against 0.7 expected; the worst is November 2024, +86.6% (about 5.96 million EUR for 100 MW shaped '
               'like the national load). The limit estimated on calm years is too tight for the crisis and after. Move the end of the '
               'estimation sample: a limit that includes 2021–2022 is wider, and the count of later exceedances falls.'),
 },
 'ro': {
  'var-es': ('O curbă normală ajustată la variațiile zilnice ale prețului din România în 2015–2026 plasează cuantila de 99% la 60,18 EUR/MWh. '
             'Cuantila empirică de 99% este 88,21 EUR/MWh. De unde vine diferența?',
             'Variațiile zilnice au cozi groase: excesul de kurtosis este 11,97, iar creșterile de peste trei abateri standard sînt 52, față '
             'de 5,82 așteptate în legea normală. VaR normal subestimează deci cuantilele extreme, iar diferența crește odată cu α. ES '
             '(media pierderilor de dincolo de VaR) reacționează și mai puternic, pentru că mediază zilele extreme pe care curba normală nu le '
             'vede. Alegeți perioada 2021–2022 pentru anii de criză sau ultimele 365 de zile pentru riscul actual.'),
  'var-paths': ('În iulie 2021–iunie 2023, un model VaR de 99% corect ar trebui depășit în circa 7 din cele 730 de zile. Cîte depășiri au '
                'modelul normal și simularea istorică filtrată (FHS)?',
                'Modelul normal este depășit în 45 de zile, simularea istorică (HS) în 28, FHS în 19, iar EVT în 17 (așteptat: 7,3). Toate '
                'metodele au fost prea jos în criză, dar FHS, care scalează reziduurile cu o volatilitate GARCH (model autoregresiv '
                'generalizat cu heteroscedasticitate condiționată), reacționează în cîteva zile la un salt al volatilității, în timp ce HS '
                'și modelul normal, cu o fereastră de 365 de zile, se adaptează lent. Testul Kupiec din sinteză compară rata depășirilor din fereastră cu 1 − α.'),
  'gpd-tail': ('Distribuția Pareto generalizată (GPD) se ajustează reziduurilor de peste pragul u. Depinde forma estimată a cozii, ξ, de alegerea lui u?',
               'Da, și aceasta este principala dificultate practică a teoriei valorilor extreme (EVT): un prag jos dă multe depășiri, dar '
               'amestecă și corpul distribuției; un prag înalt folosește doar cîteva zeci de puncte, iar estimația devine instabilă. Mutați '
               'u de la 80% la 97% și urmăriți ξ și cuantila de 99,9% implicată. În curs, forma estimată la pragul de 90% variază între '
               '−0,38 și 0,33 în cele 171 de reestimări din 2017, fiind pozitivă în 53% dintre ele.'),
  'traffic-light': ('Pe 250 de zile, un model VaR de 99% corect este în zona verde (cel mult 4 depășiri) în 89,2% din timp. În ce proporție '
                    'din zile este modelul normal în zona roșie (10 sau mai multe)?',
                    'În 29,5% din zile de cînd fereastra de testare s-a umplut (din septembrie 2017), față de 6,2% pentru FHS și 2,8% '
                    'pentru EVT; un model corect ar fi în zona roșie doar 0,025% din timp. Zonele sînt cuantile binomiale: verde cît timp '
                    'probabilitatea cumulată a numărului de depășiri într-o lege Binomial(n, 1%) este sub 95%, roșu de la 99,99%. '
                    'Schimbați fereastra pentru a vedea cum se scalează pragurile cu n.'),
  'horizon': ('Regula rădăcinii pătrate a timpului scalează un VaR pe o zi la 10 zile cu √10 = 3,16. Ce raport arată prețurile din România la nivelul de 99%?',
              'Doar 1,72 (Germania–Luxemburg: 1,75). Variațiile zilnice ale prețului sînt autocorelate negativ (ρ(1) = −0,076): un salt de '
              'preț este urmat de o scădere, deci variațiile pe mai multe zile se compensează parțial. Raportul varianțelor la 10 zile este '
              '0,33, mult sub 1. Regula √h presupune variații independente și ar supraestima VaR pe 10 zile al unei poziții de bandă pe PZU.'),
  'supplier': ('Un furnizor își bugetează fiecare lună la prețul ponderat cu consumul din luna anterioară. O limită normală de 99% estimată '
               'pe 2015–2020 plasează depășirea lunară a costului la 50,5%. Cîte luni o depășesc în 2021–2026?',
               'Trei luni din 70, față de 0,7 așteptate; cea mai rea este noiembrie 2024, +86,6% (circa 5,96 milioane EUR pentru 100 MW cu '
               'profilul consumului național). Limita estimată pe anii calmi este prea strînsă pentru criză și pentru perioada de după. '
               'Mutați sfîrșitul eșantionului de estimare: o limită care include 2021–2022 este mai largă, iar numărul depășirilor ulterioare scade.'),
 },
}

TEXT_JS = {
 'en': r"""window.LK_TEXT = {
 eur: 'EUR/MWh', count: 'Days', change: 'Daily change X (EUR/MWh)', z: 'z (standard deviations)', surv: 'Share of days with X > z·σ (log scale)',
 emp: 'Empirical', normal: 'Normal', varE: 'VaR, empirical', varN: 'VaR, normal', esE: 'ES, empirical',
 per: { all: '2015–2026', calm: '2015–2020', crisis: '2021–2022', after: '2023–2026', last: 'last 365 days' },
 ve: (z, p, n, a, ve, vn, ee, en) => `${z}, ${p} (${window.EMQAI.cnt(n, 'day', 'days')}): ${a} VaR ${ve} EUR/MWh empirical, ${vn} normal; ES ${ee} empirical, ${en} normal.`,
 ve2: (k, e, eur) => `Days above the normal VaR: ${k} (expected ${e}). For 100 MW flat (2,400 MWh a day), the empirical VaR is ${eur} EUR a day.`,
 meth: { hs: 'HS', normal: 'Normal', t: 'Student-t', fhs: 'FHS', evt: 'EVT' },
 actual: 'Daily change X', exc: 'Exceedances', varLab: (m, a) => `${m} VaR ${a}`,
 vp: (d0, d1, m, a, k, n, e, p) => `${d0} to ${d1}: ${m} ${a} VaR exceeded on ${k} of ${n} days (expected ${e}); Kupiec test p = ${p}.`,
 vp2: (m, v) => `Mean ${m} VaR in the window: ${v} EUR/MWh.`,
 gpTitle: 'Upper tail of the standardised residuals', gpQ: 'Quantiles implied by each model', resid: 'Standardised residual z', pex: 'P(Z > z) (log scale)',
 gpd: 'GPD fit', level: 'Level', quant: 'Quantile of z',
 gp: (u, uq, n, xi, b) => `Threshold u = ${u} (${uq} quantile), ${window.EMQAI.cnt(n, 'exceedance', 'exceedances')}; GPD shape ξ = ${xi}, scale β = ${b}.`,
 gp2: (e, g, nn) => `99.9% quantile of z: ${e} empirical, ${g} GPD, ${nn} normal.`,
 gp3: (n, d0, d1) => `GARCH-filtered residuals of the last ${n} days, ${d0} to ${d1}.`,
 tlTitle: w => `Exceedances of the 99% VaR in the last ${w} days`, cntL: 'Exceedances',
 green: 'green', yellow: 'yellow', red: 'red',
 tl: (w, g, r) => `Window ${w} days: green up to ${g} exceedances, red from ${r} (cumulative Binomial(${w}, 1%) probability below 95% and from 99.99%).`,
 tlRow: (m, sg, sy, sr, mx) => `${m}: green ${sg}, yellow ${sy}, red ${sr} of the days; maximum ${mx} exceedances.`,
 hzTitle: 'q(h) / q(1): empirical vs √h', hzVr: 'Variance ratio Var(h-day) / (h · Var(1-day))', h: 'Horizon h (days)',
 sqrt: '√h rule', emp2: 'Empirical ratio',
 hz: (z, a, h, r, s, q1, qh) => `${z}, ${a} quantile: ${h}-day ratio ${r} against √h = ${s}; 1-day quantile ${q1}, ${h}-day ${qh} EUR/MWh.`,
 hz2: (h, vr, r1) => `Variance ratio at ${h} days: ${vr}; first-order autocorrelation of the daily change ${r1}.`,
 smTitle: 'Monthly cost overrun of the supplier (%)', overrun: 'Overrun vs last month', limit: 'Normal limit', est: 'Estimation sample',
 sm: (y, a, m, s, l) => `Sample 2015-03 to ${y}-12: mean ${m}%, standard deviation ${s}%; normal ${a} limit ${l}%.`,
 sm2: (n, k, e, w, wp, we) => `After the sample: ${k} of ${n} months above the limit (expected ${e}); worst month ${w}, +${wp}% (${we} million EUR for 100 MW).`
};
""",
 'ro': r"""window.LK_TEXT = {
 eur: 'EUR/MWh', count: 'Zile', change: 'Variația zilnică X (EUR/MWh)', z: 'z (abateri standard)', surv: 'Proporția zilelor cu X > z·σ (scală log)',
 emp: 'Empirică', normal: 'Normală', varE: 'VaR, empiric', varN: 'VaR, normal', esE: 'ES, empiric',
 per: { all: '2015–2026', calm: '2015–2020', crisis: '2021–2022', after: '2023–2026', last: 'ultimele 365 de zile' },
 ve: (z, p, n, a, ve, vn, ee, en) => `${z}, ${p} (${window.EMQAI.cnt(n, 'zi', 'zile')}): VaR ${a} ${ve} EUR/MWh empiric, ${vn} normal; ES ${ee} empiric, ${en} normal.`,
 ve2: (k, e, eur) => `Zile peste VaR normal: ${k} (așteptat ${e}). Pentru 100 MW în bandă (2.400 MWh pe zi), VaR empiric este ${eur} EUR pe zi.`,
 meth: { hs: 'HS', normal: 'Normal', t: 'Student-t', fhs: 'FHS', evt: 'EVT' },
 actual: 'Variația zilnică X', exc: 'Depășiri', varLab: (m, a) => `VaR ${m} ${a}`,
 vp: (d0, d1, m, a, k, n, e, p) => `${d0} – ${d1}: VaR ${m} ${a} depășit în ${k} din ${window.EMQAI.cnt(n, 'zi', 'zile')} (așteptat ${e}); testul Kupiec p = ${p}.`,
 vp2: (m, v) => `VaR ${m} mediu în fereastră: ${v} EUR/MWh.`,
 gpTitle: 'Coada superioară a reziduurilor standardizate', gpQ: 'Cuantilele implicate de fiecare model', resid: 'Reziduul standardizat z', pex: 'P(Z > z) (scală log)',
 gpd: 'Ajustarea GPD', level: 'Nivelul', quant: 'Cuantila lui z',
 gp: (u, uq, n, xi, b) => `Pragul u = ${u} (cuantila de ${uq}), ${window.EMQAI.cnt(n, 'depășire', 'depășiri')}; forma GPD ξ = ${xi}, scala β = ${b}.`,
 gp2: (e, g, nn) => `Cuantila de 99,9% a lui z: ${e} empiric, ${g} GPD, ${nn} normal.`,
 gp3: (n, d0, d1) => `Reziduurile filtrate GARCH din ultimele ${window.EMQAI.cnt(n, 'zi', 'zile')}, ${d0} – ${d1}.`,
 tlTitle: w => `Depășiri ale VaR de 99% în ultimele ${window.EMQAI.cnt(w, 'zi', 'zile')}`, cntL: 'Depășiri',
 green: 'verde', yellow: 'galben', red: 'roșu',
 tl: (w, g, r) => `Fereastra de ${window.EMQAI.cnt(w, 'zi', 'zile')}: verde pînă la ${g} depășiri, roșu de la ${r} (probabilitatea cumulată Binomial(${w}, 1%) sub 95%, respectiv de la 99,99%).`,
 tlRow: (m, sg, sy, sr, mx) => `${m}: verde ${sg}, galben ${sy}, roșu ${sr} din zile; maximum ${window.EMQAI.cnt(mx, 'depășire', 'depășiri')}.`,
 hzTitle: 'q(h) / q(1): empiric față de √h', hzVr: 'Raportul varianțelor Var(h zile) / (h · Var(1 zi))', h: 'Orizontul h (zile)',
 sqrt: 'Regula √h', emp2: 'Raportul empiric',
 hz: (z, a, h, r, s, q1, qh) => `${z}, cuantila de ${a}: raportul la ${h} zile ${r}, față de √h = ${s}; cuantila pe o zi ${q1}, pe ${h} zile ${qh} EUR/MWh.`,
 hz2: (h, vr, r1) => `Raportul varianțelor la ${h} zile: ${vr}; autocorelația de ordinul 1 a variației zilnice ${r1}.`,
 smTitle: 'Depășirea lunară a costului furnizorului (%)', overrun: 'Depășirea față de luna anterioară', limit: 'Limita normală', est: 'Eșantionul de estimare',
 sm: (y, a, m, s, l) => `Eșantionul 2015-03 – ${y}-12: media ${m}%, abaterea standard ${s}%; limita normală de ${a} ${l}%.`,
 sm2: (n, k, e, w, wp, we) => `După eșantion: ${k} din ${window.EMQAI.cnt(n, 'lună', 'luni')} peste limită (așteptat ${e}); cea mai rea lună ${w}, +${wp}% (${we} milioane EUR pentru 100 MW).`
};
""",
}


# ---------------------------------------------------------------- data (real course data only)
def data():
    import numpy as np
    import pandas as pd
    from arch import arch_model
    from scipy import stats
    END = cutoff()
    out = {'end': str(END.date())}
    PD = csv('power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')
    CAL = pd.date_range('2015-01-01', END, freq='D')
    P = PD[['RO', 'DE_LU']].reindex(CAL)
    X = P.diff()
    out['t0'] = str(CAL[0].date())
    out['P'] = {z: rnd(P[z].values, 2) for z in ['RO', 'DE_LU']}

    # rolling one-day-ahead VaR forecasts (analysis_L4.py engine), Romania, 95% and 99%
    cache = os.path.join(HERE, 'cache', 'engine.pkl')
    if not os.path.exists(cache):
        raise SystemExit('lectures/L4/cache/engine.pkl is missing: run python3 lectures/L4/analysis_L4.py first')
    E = pickle.load(open(cache, 'rb'))['eng']['RO']
    days = E['days']
    out['vp'] = {'d0': str(days[0].date()), 'n': len(days),
                 'v': {m: {str(a): rnd(E['out'][m][a]['var'], 2) for a in (0.95, 0.99)} for m in METHODS}}

    # GARCH-filtered standardised residuals of the last 730 days (as the gpd_tail chart) and GPD fits by threshold
    hist = X['RO'][:END].dropna()[-730:]
    mdow = hist.groupby(hist.index.dayofweek).mean()
    e = (hist - mdow.reindex(hist.index.dayofweek).values).values
    res = arch_model(e, mean='Zero', vol='GARCH', p=1, q=1, dist='normal', rescale=False).fit(disp='off')
    z = e / np.asarray(res.conditional_volatility)
    fits = {}
    for uq in range(80, 98):
        u = np.quantile(z, uq / 100)
        exc = z[z > u] - u
        xi, _, beta = stats.genpareto.fit(exc, floc=0)
        fits[uq] = {'u': round(float(u), 4), 'xi': round(float(xi), 4), 'beta': round(float(beta), 4), 'n': int(len(exc))}
    out['gp'] = {'z': rnd(np.sort(z), 4), 'fits': fits, 'd0': str(hist.index[0].date()), 'd1': str(hist.index[-1].date())}

    # supplier: monthly change of the load-weighted price (hourly prices x Romanian load), as analysis_L4.py section 7
    H = csv('power_da_prices_hourly_utc.csv', usecols=['timestamp_utc', 'RO'], parse_dates=['timestamp_utc']).set_index('timestamp_utc')['RO']
    G = csv('generation_ro_mw_hourly_utc.csv', usecols=['timestamp_utc', 'load'], parse_dates=['timestamp_utc']).set_index('timestamp_utc')['load']
    hl = pd.DataFrame({'p': H, 'l': G}).dropna()
    hl['m'] = hl.index.tz_convert('Europe/Brussels').tz_localize(None).to_period('M')
    hl['pl'] = hl['p'] * hl['l']
    g = hl.groupby('m')
    mon = pd.DataFrame({'lwp': g['pl'].sum() / g['l'].sum(), 'hours': g.size()})
    mon = mon[(mon.index >= pd.Period('2015-02', 'M')) & (mon.index <= pd.Period(END, 'M'))]
    mon['o'] = mon['lwp'] / mon['lwp'].shift(1) - 1
    mon['eur'] = 100 * mon['hours'] * (mon['lwp'] - mon['lwp'].shift(1))
    mon = mon.dropna()
    out['sm'] = {'m': [str(p) for p in mon.index], 'o': rnd(100 * mon['o'].values, 2), 'eur': rnd(mon['eur'].values / 1e6, 3)}
    return out


if __name__ == '__main__':
    interactive_common.build(sys.modules[__name__])
