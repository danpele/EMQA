"""Build the interactive page of Lecture 2 (Forecasting day-ahead electricity prices): interactive/L2.html (EN) and
interactive/L2_ro.html (RO).

Inputs (interactive/L2_data.js): actual Romanian day-ahead prices of the test year (data/clean, CET delivery day x 24 hours,
same rule as the Quantlets), the point forecasts of the lecture (lectures/L2/cache/forecasts.pkl, tracked in git) and the
QRA quantiles of the test year (Quantlets/L2/EMQA_L2_prob_rel/qra_test.npz). The page logic is in interactive/L2.js.
Run: python3 lectures/L2/build_interactive_L2.py [--no-data]
"""
import os
import pickle
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import interactive_common  # noqa: E402
from interactive_common import slider, select, toggles, play, charts, rnd, csv, cutoff, ql_dir  # noqa: E402

K = 2

# (anchor, chart file / Quantlet, section key, id prefix)
BLOCKS = [('mape', 'mape_fail', 'bench', 'mp'),
          ('dm-test', 'dm_matrix', 'bench', 'dm'),
          ('per-hour', 'per_hour_single', 'expert', 'ph'),
          ('windows', 'windows', 'win', 'wn'),
          ('qra', 'prob_rel', 'prob', 'qr'),
          ('monthly', 'monthly_mae', 'case', 'mm')]

SECTIONS = {
 'en': dict(bench='The forecasting problem and its benchmarks', expert='Expert models: ARX and LEAR',
            win='Windows, combinations and machine learning', prob='Probabilistic forecasts and cointegration',
            case='Case studies on recent Romanian data'),
 'ro': dict(bench='Problema de prognoză și modelele de referință', expert='Modele expert: ARX și LEAR',
            win='Ferestre, combinații și învățare automată', prob='Prognoze probabilistice și cointegrare',
            case='Studii de caz pe date recente din România'),
}

# models exported (point forecasts of the test year); labels in widgets / LK_TEXT
MODELS = ['naive', 'snaive', 'arx56', 'arx84', 'arx112', 'arx714', 'arx721', 'arx728', 'arx728_single',
          'lear364', 'lear546', 'lear728', 'gbm', 'mlp']
TAUS = [1, 5, 10, 25, 50, 75, 90, 95, 99]          # percent; quantiles of QRA exported

L = {
 'en': dict(h1='Lecture 2 · Forecasting day-ahead electricity prices',
   note='The slide of the lecture is on the left, the same figure on the right, recomputed in your browser from the forecasts of the '
        'lecture when you move a control. The ▶ button moves the main parameter step by step. Test year: 1 November 2025 – 31 October '
        '2026 (365 days × 24 hours, Romanian day-ahead market, OPCOM PZU). Under each figure: a readout, a question for the room and the '
        'Quantlet with the code of the chart.',
   src='Prices: OPCOM PZU (Romanian day-ahead market) via energy-charts.info (Fraunhofer ISE); delivery day in Central European Time '
       '(CET/CEST), 24 hourly values per day (the 15-minute prices from 1 October 2025 are averaged to the hour). Forecasts: the models '
       'of Lecture 2, re-estimated every day of the test year with data available at gate closure (Quantlets EMQA_L2_*). '
       'Abbreviations: MAE mean absolute error, RMSE root mean squared error, MAPE mean absolute percentage error, sMAPE symmetric MAPE, '
       'ARX autoregressive model with exogenous inputs, LEAR lasso-estimated autoregressive model, AW average across calibration windows, '
       'GBM gradient boosting machine, MLP multilayer perceptron, DM Diebold–Mariano, QRA quantile regression averaging.'),
 'ro': dict(h1='Cursul 2 · Prognoza prețurilor pentru ziua următoare',
   note='În stînga este slide-ul din curs, în dreapta aceeași figură, recalculată în browser din prognozele cursului cînd modificați un '
        'control. Butonul ▶ modifică parametrul principal pas cu pas. Anul de test: 1 noiembrie 2025 – 31 octombrie 2026 (365 de zile × '
        '24 de ore, piața pentru ziua următoare din România, OPCOM PZU). Sub fiecare figură: o sinteză numerică, o întrebare pentru sală '
        'și Quantlet-ul cu codul figurii.',
   src='Prețuri: OPCOM PZU (piața pentru ziua următoare din România), prin energy-charts.info (Fraunhofer ISE); ziua de livrare în ora '
       'Europei Centrale (CET/CEST), 24 de valori orare pe zi (prețurile pe 15 minute din 1 octombrie 2025 sînt mediate pe oră). '
       'Prognoze: modelele din Cursul 2, reestimate în fiecare zi a anului de test numai cu datele disponibile la închiderea ofertelor '
       '(Quantlets EMQA_L2_*). Abrevieri: MAE eroarea absolută medie, RMSE rădăcina erorii pătratice medii, MAPE eroarea procentuală '
       'absolută medie, sMAPE MAPE simetrică, ARX model autoregresiv cu variabile exogene, LEAR model autoregresiv estimat cu lasso, AW '
       'media pe ferestrele de calibrare, GBM gradient boosting, MLP perceptron multistrat, DM Diebold–Mariano, QRA medierea prin regresie cuantilică.'),
}


def labels(ro):
    return {'naive': 'Naiv' if ro else 'Naive', 'snaive': 'Naiv sezonier' if ro else 'Seasonal naive',
            'arx728': 'ARX(728)', 'arx728_single': 'ARX(728), o singură regresie' if ro else 'ARX(728), single regression',
            'aw_arx': 'AW-ARX', 'lear728': 'LEAR(728)', 'aw_lear': 'AW-LEAR', 'gbm': 'GBM', 'mlp': 'MLP',
            'ens_all': 'Ansamblu 4 modele' if ro else 'Ensemble of 4 models'}


def widgets(lang):
    ro = lang == 'ro'
    Lb = labels(ro)
    mopts = [(k, Lb[k]) for k in ['naive', 'snaive', 'arx728', 'aw_arx', 'lear728', 'aw_lear', 'gbm', 'mlp', 'ens_all']]
    return {
     'mape': (slider('mp-x', 'Se exclud orele cu |preț| sub (EUR/MWh)' if ro else 'Exclude hours with |price| below (EUR/MWh)', 0, 30, 1, 0)
              + select('mp-m', 'Model', mopts, 'aw_lear') + play('mp'), charts('mp-chart', 'mp-ape')),
     'dm-test': (select('dm-a', 'Modelul A (rîndul)' if ro else 'Model A (row)', mopts, 'naive')
                 + select('dm-b', 'Modelul B (coloana)' if ro else 'Model B (column)', mopts, 'aw_lear')
                 + select('dm-l', 'Funcția de pierdere' if ro else 'Loss', [('abs', 'Eroare absolută' if ro else 'Absolute error'),
                                                                          ('sq', 'Eroare pătratică' if ro else 'Squared error')], 'abs')
                 + slider('dm-L', 'Laguri Newey–West' if ro else 'Newey–West lags', 0, 21, 1, 7) + play('dm'),
                 charts('dm-diff', 'dm-cum')),
     'per-hour': (toggles('ph-m', 'Modele' if ro else 'Models', [(k, Lb[k]) for k in ['naive', 'arx728', 'arx728_single', 'aw_lear', 'gbm', 'ens_all']],
                          ['naive', 'arx728', 'arx728_single'])
                  + select('ph-q', 'Perioada' if ro else 'Period', [('all', 'Tot anul de test' if ro else 'Whole test year'),
                                                                    ('win', 'Iarna (dec–feb)' if ro else 'Winter (Dec–Feb)'),
                                                                    ('spr', 'Primăvara (mar–mai)' if ro else 'Spring (Mar–May)'),
                                                                    ('sum', 'Vara (iun–aug)' if ro else 'Summer (Jun–Aug)'),
                                                                    ('aut', 'Toamna (sep–nov)' if ro else 'Autumn (Sep–Nov)')], 'all')
                  + select('ph-e', 'Măsura' if ro else 'Measure', [('mae', 'MAE'), ('rmse', 'RMSE')], 'mae'),
                  charts('ph-chart', cls='one')),
     'windows': (select('wn-f', 'Familia de modele' if ro else 'Model family', [('arx', 'ARX'), ('lear', 'LEAR')], 'arx')
                 + toggles('wn-w', 'Ferestre incluse în medie (zile)' if ro else 'Windows in the average (days)',
                           [(w, str(w)) for w in [56, 84, 112, 364, 546, 714, 721, 728]], [56, 84, 112, 714, 721, 728, 364, 546]),
                 charts('wn-chart', cls='one')),
     'monthly': (toggles('mm-m', 'Modele' if ro else 'Models', [(k, Lb[k]) for k in ['naive', 'aw_arx', 'aw_lear', 'gbm', 'mlp', 'ens_all']],
                         ['naive', 'aw_lear', 'ens_all'])
                 + select('mm-r', 'Scala' if ro else 'Scale', [('abs', 'MAE (EUR/MWh)'), ('rel', 'MAE relativ la naiv (rMAE)' if ro else 'MAE relative to naive (rMAE)')], 'abs'),
                 charts('mm-chart', cls='one')),
     'qra': (slider('qr-c', 'Nivelul nominal al intervalului (%)' if ro else 'Nominal level of the interval (%)', 0, 3, 1, 2)
             + slider('qr-w', 'Săptămîna afișată (începe în ziua)' if ro else 'Week shown (starts on day)', 0, 358, 7, 182)
             + select('qr-h', 'Ora pentru acoperire' if ro else 'Hour for the coverage', [('all', 'Toate orele' if ro else 'All hours')] + [(h, f'{h:02d}:00') for h in range(24)], 'all')
             + play('qr'), charts('qr-fan', 'qr-rel')),
    }


QA = {
 'en': {
  'mape': ('The test year has 8,760 hours. The MAPE of AW-LEAR is above 5,700%, its MAE 22.53 EUR/MWh. Is the model really that bad?',
           'No. The percentage error divides by the actual price, and 387 hours have |price| below 5 EUR/MWh (60 are exactly zero, 195 are '
           'negative). These hours produce 99.5% of the MAPE; excluding them, the MAPE of AW-LEAR falls to 32.4%. Move the slider: the MAE and '
           'the sMAPE hardly change, the MAPE collapses. With prices near zero, MAE, RMSE and the relative MAE (rMAE, MAE divided by the MAE of '
           'the naive forecast) are the measures to report.'),
  'dm-test': ('AW-LEAR has an MAE of 22.53 EUR/MWh, the naive forecast 27.82. Is the difference significant, and is AW-LEAR significantly '
              'better than AW-ARX (22.30)?',
              'The first yes, the second no. The DM test works on the daily loss differential d_t (mean over the 24 hours of |e_A| − |e_B|) '
              'with a Newey–West variance (7 lags): naive vs AW-LEAR gives DM = 7.32, one-sided p < 0.001; AW-ARX vs AW-LEAR gives DM = −0.83, '
              'p = 0.80, so AW-LEAR is not more accurate than AW-ARX. Change the loss to squared errors or the number of lags: the sign of the '
              'conclusion for naive vs AW-LEAR does not change; for close models it can.'),
  'per-hour': ('ARX(728) estimates one regression per hour (24 models); the single-regression version uses common slopes and only hour-specific '
               'intercepts. In how many hours is the single regression worse?',
               'In 21 of the 24 hours. Its MAE over the year is 24.54 EUR/MWh, against 22.72 for ARX(728) with one regression per hour: each hour '
               'has its own dynamics (night hours follow the previous day closely, the solar hours depend more on renewables). The errors of '
               'all models peak in the evening: AW-LEAR has its worst hour at 19:00 (34.52 EUR/MWh) and its best at 01:00 (9.47).'),
  'windows': ('ARX with a 56-day window has an MAE of 24.44 EUR/MWh, with 728 days 22.72. Does the average of the forecasts across the six '
              'ARX windows beat the best single window?',
              'Yes. AW-ARX, the average across the windows 56, 84, 112, 714, 721 and 728 days, has an MAE of 22.30 EUR/MWh, below every single '
              'window (best: 714 days, 22.68). Short windows adapt quickly to new price levels, long ones estimate the coefficients precisely; '
              'their errors are not perfectly correlated, so averaging reduces the error. Untick windows to see which combinations still help. '
              'For LEAR, the average of 364, 546 and 728 days (22.53) also beats each window (best: 728 days, 22.62).'),
  'monthly': ('Is AW-LEAR better than the naive forecast in every month of the test year, and is the ensemble of four models always better than AW-LEAR?',
              'AW-LEAR beats the naive forecast in all 12 months; the ensemble (mean of AW-ARX, AW-LEAR, GBM and MLP) beats AW-LEAR in 8 of the '
              '12 months. The error level moves a lot between months: AW-LEAR has 12.84 EUR/MWh in December 2025 and 34.88 in October 2026. '
              'Switch to the relative MAE: the ranking of the models is more stable than the level of their errors.'),
  'qra': ('The 90% QRA interval (built from the AW-ARX and AW-LEAR forecasts) should contain the price in 90% of the hours. How often does it in the test year?',
          'In 85.67% of the hours, below 90%: the interval is too narrow, and the Kupiec test (a likelihood-ratio test of the share of hours outside the interval) rejects correct coverage (p < 0.001). The 50% '
          'interval covers 47.3%. The reliability chart shows, for each quantile level τ, the share of prices below the quantile minus τ, in percentage '
          'points (pp): above zero in the lower tail and below zero in the upper tail, so extreme prices are more frequent than the '
          'model expects. Choose an hour: the evening hours have the widest intervals.'),
 },
 'ro': {
  'mape': ('Anul de test are 8.760 de ore. MAPE pentru AW-LEAR depășește 5.700%, iar MAE este 22,53 EUR/MWh. Este modelul chiar atît de slab?',
           'Nu. Eroarea procentuală împarte la prețul efectiv, iar 387 de ore au |preț| sub 5 EUR/MWh (60 sînt exact zero, 195 negative). '
           'Aceste ore produc 99,5% din MAPE; fără ele, MAPE pentru AW-LEAR scade la 32,4%. Mutați cursorul: MAE și sMAPE aproape nu se '
           'schimbă, MAPE se prăbușește. Cu prețuri apropiate de zero, raportăm MAE, RMSE și MAE relativ (rMAE, MAE împărțit la MAE al '
           'prognozei naive).'),
  'dm-test': ('AW-LEAR are MAE 22,53 EUR/MWh, prognoza naivă 27,82. Este diferența semnificativă și este AW-LEAR semnificativ mai bun decît AW-ARX (22,30)?',
              'Prima da, a doua nu. Testul DM folosește diferența zilnică a pierderilor d_t (media pe cele 24 de ore a |e_A| − |e_B|), cu '
              'varianța Newey–West (7 laguri): naiv față de AW-LEAR dă DM = 7,32, p unilateral < 0,001; AW-ARX față de AW-LEAR dă DM = −0,83, '
              'p = 0,80, deci AW-LEAR nu este mai precis decît AW-ARX. Schimbați pierderea în eroare pătratică sau numărul de laguri: '
              'concluzia pentru naiv față de AW-LEAR rămîne; pentru modele apropiate se poate schimba.'),
  'per-hour': ('ARX(728) estimează o regresie pentru fiecare oră (24 de modele); varianta cu o singură regresie are pante comune și doar '
               'termeni liberi diferiți pe ore. În cîte ore este varianta cu o singură regresie mai slabă?',
               'În 21 din cele 24 de ore. MAE pe an este 24,54 EUR/MWh, față de 22,72 pentru ARX(728) cu cîte o regresie pe oră: fiecare oră '
               'are propria dinamică (orele de noapte urmează îndeaproape ziua anterioară, orele solare depind mai mult de regenerabile). '
               'Erorile tuturor modelelor sînt maxime seara: AW-LEAR are cea mai slabă oră la 19:00 (34,52 EUR/MWh) și cea mai bună la 01:00 (9,47).'),
  'windows': ('ARX cu fereastra de 56 de zile are MAE 24,44 EUR/MWh, cu 728 de zile 22,72. Este media prognozelor pe cele șase ferestre ARX '
              'mai bună decît cea mai bună fereastră?',
              'Da. AW-ARX, media pe ferestrele de 56, 84, 112, 714, 721 și 728 de zile, are MAE 22,30 EUR/MWh, sub fiecare fereastră '
              'luată separat (cea mai bună: 714 zile, 22,68). Ferestrele scurte se adaptează repede la noile niveluri ale prețului, cele lungi '
              'estimează precis coeficienții; erorile lor nu sînt perfect corelate, deci media reduce eroarea. Debifați ferestre pentru a vedea '
              'ce combinații mai ajută. Pentru LEAR, media pe 364, 546 și 728 de zile (22,53) este și ea sub fiecare fereastră (cea mai bună: 728 de zile, 22,62).'),
  'monthly': ('Este AW-LEAR mai bun decît prognoza naivă în fiecare lună a anului de test și este ansamblul de patru modele mereu mai bun decît AW-LEAR?',
              'AW-LEAR bate prognoza naivă în toate cele 12 luni; ansamblul (media AW-ARX, AW-LEAR, GBM și MLP) bate AW-LEAR în 8 din cele '
              '12 luni. Nivelul erorii variază mult între luni: AW-LEAR are 12,84 EUR/MWh în decembrie 2025 și 34,88 în octombrie 2026. '
              'Treceți la MAE relativ: ordinea modelelor este mai stabilă decît nivelul erorilor.'),
  'qra': ('Intervalul QRA de 90% (construit din prognozele AW-ARX și AW-LEAR) ar trebui să conțină prețul în 90% din ore. Cît de des o face în anul de test?',
          'În 85,67% din ore, sub 90%: intervalul este prea îngust, iar testul Kupiec (un test al raportului de verosimilitate pentru ponderea orelor din afara intervalului) respinge acoperirea corectă (p < 0,001). Intervalul de 50% '
          'acoperă 47,3%. Graficul de fiabilitate arată, pentru fiecare nivel τ, ponderea prețurilor sub cuantilă minus τ, în puncte procentuale '
          '(pp): peste zero în coada inferioară și sub zero în coada superioară, deci prețurile extreme sînt mai frecvente decît se așteaptă '
          'modelul. Alegeți o oră: orele de seară au intervalele cele mai largi.'),
 },
}

TEXT_JS = {
 'en': r"""window.LK_TEXT = {
 eur: 'EUR/MWh', hour: 'Hour of the day (CET)', month: 'Month', day: 'Day of the test year',
 lab: { naive: 'Naive', snaive: 'Seasonal naive', arx728: 'ARX(728)', arx728_single: 'ARX(728), single regression', aw_arx: 'AW-ARX',
        lear728: 'LEAR(728)', aw_lear: 'AW-LEAR', gbm: 'GBM', mlp: 'MLP', ens_all: 'Ensemble of 4 models' },
 mpBar: 'Error measures', mpApe: 'Absolute percentage error (APE) by actual price, log scale', ape: 'APE (%)', absp: 'Actual price (EUR/MWh)',
 mp: (m, x, n, mae, mape, smape) => `${m}, hours with |price| ≥ ${x} EUR/MWh: ${n}. MAE ${mae} EUR/MWh, MAPE ${mape}%, sMAPE ${smape}%.`,
 mp2: n => `${n} excluded.`,
 dmDiff: 'Daily loss differential d_t (A − B)', dmCum: 'Cumulative sum of d_t', dt: 'd_t',
 dm: (a, b, mA, mB, s, p, L) => `${a}: mean loss ${mA}; ${b}: ${mB}. DM = ${s} (Newey–West, ${L} lags), one-sided p ${p} for H₁: B is more accurate than A.`,
 dmSame: 'Choose two different models.',
 dmV: (p) => p < 0.05 ? 'At 5%, B is significantly more accurate than A.' : 'At 5%, there is no significant evidence that B is more accurate than A.',
 phTitle: e => `${e === 'mae' ? 'MAE' : 'RMSE'} by hour of the day (EUR/MWh)`,
 ph: (m, v, hw, w, hb, b) => `${m}: ${v} over the period; worst hour ${hw}:00 (${w}), best ${hb}:00 (${b}).`,
 phCmp: n => `ARX(728) with a single regression is worse than ARX(728) with one regression per hour in ${n} of the 24 hours.`,
 wnTitle: f => `MAE of ${f.toUpperCase()} by calibration window and of their average (EUR/MWh)`, win: 'Calibration window (days)', avg: 'Average',
 wn: (f, list, m, best, bm) => `AW-${f.toUpperCase()} over ${list} days: MAE ${m} EUR/MWh; best single window ${best} days (${bm}).`,
 wnNone: 'Tick at least one window of this family.',
 wnGain: (g, s) => g > 0 ? `The average is ${s} EUR/MWh below the best window it contains.` : `The average is ${s} EUR/MWh above the best window it contains.`,
 mmTitle: r => r === 'abs' ? 'MAE by month (EUR/MWh)' : 'MAE relative to the naive forecast, by month', mmRel: 'rMAE',
 mm: (m, v, wm, w, bm, b) => `${m}: year ${v}; worst month ${wm} (${w}), best ${bm} (${b}).`,
 qrFan: (d0, d1) => `QRA intervals and actual price, ${d0} – ${d1}`, qrRel: 'Reliability: share of prices below the quantile minus τ (pp)',
 nominal: 'Nominal level of the quantile τ (%)', empirical: 'Empirical share − τ (pp)', actual: 'Actual price', median: 'Median', diag: 'Perfect calibration',
 lvl: [50, 80, 90, 98],
 qr: (c, h, cov, w) => `${c}% interval, ${h}: coverage ${cov}%, mean width ${w} EUR/MWh.`,
 qrWeek: (cov) => `In the week shown, the interval contains ${cov}% of the 168 prices.`,
 all: 'all hours'
};
""",
 'ro': r"""window.LK_TEXT = {
 eur: 'EUR/MWh', hour: 'Ora zilei (CET)', month: 'Luna', day: 'Ziua anului de test',
 lab: { naive: 'Naiv', snaive: 'Naiv sezonier', arx728: 'ARX(728)', arx728_single: 'ARX(728), o singură regresie', aw_arx: 'AW-ARX',
        lear728: 'LEAR(728)', aw_lear: 'AW-LEAR', gbm: 'GBM', mlp: 'MLP', ens_all: 'Ansamblu 4 modele' },
 mpBar: 'Măsuri ale erorii', mpApe: 'Eroarea procentuală absolută (APE) după prețul efectiv, scală logaritmică', ape: 'APE (%)', absp: 'Prețul efectiv (EUR/MWh)',
 mp: (m, x, n, mae, mape, smape) => `${m}, ore cu |preț| ≥ ${x} EUR/MWh: ${n}. MAE ${mae} EUR/MWh, MAPE ${mape}%, sMAPE ${smape}%.`,
 mp2: n => `${n} excluse.`,
 dmDiff: 'Diferența zilnică a pierderilor d_t (A − B)', dmCum: 'Suma cumulată a d_t', dt: 'd_t',
 dm: (a, b, mA, mB, s, p, L) => `${a}: pierderea medie ${mA}; ${b}: ${mB}. DM = ${s} (Newey–West, ${L} laguri), p unilateral ${p} pentru H₁: B este mai precis decît A.`,
 dmSame: 'Alegeți două modele diferite.',
 dmV: (p) => p < 0.05 ? 'La 5%, B este semnificativ mai precis decît A.' : 'La 5%, nu avem dovezi semnificative că B este mai precis decît A.',
 phTitle: e => `${e === 'mae' ? 'MAE' : 'RMSE'} pe ora zilei (EUR/MWh)`,
 ph: (m, v, hw, w, hb, b) => `${m}: ${v} pe perioadă; cea mai slabă oră ${hw}:00 (${w}), cea mai bună ${hb}:00 (${b}).`,
 phCmp: n => `ARX(728) cu o singură regresie este mai slab decît ARX(728) cu cîte o regresie pe oră în ${n} din cele 24 de ore.`,
 wnTitle: f => `MAE pentru ${f.toUpperCase()} pe ferestre de calibrare și pentru media lor (EUR/MWh)`, win: 'Fereastra de calibrare (zile)', avg: 'Media',
 wn: (f, list, m, best, bm) => `AW-${f.toUpperCase()} pe ${list} zile: MAE ${m} EUR/MWh; cea mai bună fereastră ${best} zile (${bm}).`,
 wnNone: 'Bifați cel puțin o fereastră din această familie.',
 wnGain: (g, s) => g > 0 ? `Media este cu ${s} EUR/MWh sub cea mai bună fereastră inclusă.` : `Media este cu ${s} EUR/MWh peste cea mai bună fereastră inclusă.`,
 mmTitle: r => r === 'abs' ? 'MAE pe luni (EUR/MWh)' : 'MAE relativ la prognoza naivă, pe luni', mmRel: 'rMAE',
 mm: (m, v, wm, w, bm, b) => `${m}: anul ${v}; cea mai slabă lună ${wm} (${w}), cea mai bună ${bm} (${b}).`,
 qrFan: (d0, d1) => `Intervale QRA și prețul efectiv, ${d0} – ${d1}`, qrRel: 'Fiabilitate: ponderea prețurilor sub cuantilă minus τ (pp)',
 nominal: 'Nivelul nominal al cuantilei τ (%)', empirical: 'Ponderea empirică − τ (pp)', actual: 'Prețul efectiv', median: 'Mediana', diag: 'Calibrare perfectă',
 lvl: [50, 80, 90, 98],
 qr: (c, h, cov, w) => `Intervalul de ${c}%, ${h}: acoperire ${cov}%, lățime medie ${w} EUR/MWh.`,
 qrWeek: (cov) => `În săptămîna afișată, intervalul conține ${cov}% din cele 168 de prețuri.`,
 all: 'toate orele'
};
""",
}


# ---------------------------------------------------------------- data (real course data only)
def day_matrix(s):
    """UTC-indexed hourly series -> CET delivery day x 24 hours (rule of the L2 Quantlets and analysis_L2.py)."""
    import numpy as np
    import pandas as pd
    TZ = 'Europe/Brussels'
    s = s.copy()
    s.index = pd.to_datetime(s.index, utc=True).tz_convert(TZ)
    df = pd.DataFrame({'v': s.values, 'day': s.index.tz_localize(None).normalize(), 'h': s.index.hour})
    m = df.groupby(['day', 'h'])['v'].mean().unstack('h').reindex(columns=range(24))
    days = m.index
    nh = ((((days + pd.Timedelta(days=1)).tz_localize(TZ)) - days.tz_localize(TZ)) / pd.Timedelta(hours=1)).astype(int)
    dst = np.asarray(nh != 24)
    for dd in days[dst]:
        if pd.isna(m.loc[dd, 2]):
            m.loc[dd, 2] = 0.5 * (m.loc[dd, 1] + m.loc[dd, 3])
    return m.dropna(how='any')


def data():
    import numpy as np
    import pandas as pd
    END = cutoff()
    TDAYS = pd.date_range(END - pd.Timedelta(days=364), END, freq='D')
    HP = csv('power_da_prices_hourly_utc.csv', index_col=0, usecols=['timestamp_utc', 'RO'])
    A = day_matrix(HP['RO'].dropna()).reindex(TDAYS).values.astype(float)
    assert not np.isnan(A).any()
    FC = pickle.load(open(os.path.join(HERE, 'cache', 'forecasts.pkl'), 'rb'))
    pt = FC['point']
    M = {}
    for k in MODELS:
        v = FC[k] if k in ('gbm', 'mlp') else pt[k][-365:]
        M[k] = np.asarray(v, float)
        assert M[k].shape == (365, 24), k
    # check against the lecture numbers (MAE of the test year)
    for k, ref in (('naive', 27.82), ('arx728', 22.72), ('lear728', 22.62), ('gbm', 24.05), ('mlp', 25.54)):
        assert abs(np.abs(A - M[k]).mean() - ref) < 0.006, (k, np.abs(A - M[k]).mean())
    Q = np.sort(np.load(os.path.join(ql_dir(2, 'prob_rel'), 'qra_test.npz'))['q'].astype(float), axis=2)
    taus = np.arange(1, 100)
    rel = {'all': rnd([(A <= Q[:, :, j]).mean() for j in range(99)], 4)}
    for h in range(24):
        rel[h] = rnd([(A[:, h] <= Q[:, h, j]).mean() for j in range(99)], 4)
    # actual prices to 0.01 EUR/MWh; the hours with |price| < 5 EUR/MWh exactly (they drive the MAPE: denominators near zero)
    small = [[int(d), int(h), float(A[d, h])] for d, h in zip(*np.where(np.abs(A) < 5))]
    return {'end': str(END.date()), 'days': [str(d.date()) for d in TDAYS], 'A': rnd(A, 2), 'small': small,
            'F': {k: rnd(v, 1) for k, v in M.items()},
            'q': {'taus': TAUS, 'v': [rnd(Q[:, :, t - 1], 2) for t in TAUS], 'rel': rel, 'tau_all': taus.tolist()}}


if __name__ == '__main__':
    interactive_common.build(sys.modules[__name__])
