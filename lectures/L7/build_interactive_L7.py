"""Build the interactive page of Lecture 7 (Machine learning and foundation models for electricity price forecasting):
interactive/L7.html (EN) and interactive/L7_ro.html (RO).

Inputs (interactive/L7_data.js) are computed here from the saved results of the Lecture 7 Quantlets (Quantlets/L7/*/*_results.npz:
forecasts, probabilities, learning curve of the test year 2025-11-01 to 2026-10-31) and the Romanian day-ahead prices of data/clean
(CET delivery day x 24 hours, the day_matrix rule of the Quantlets). The page logic is in interactive/L7.js.
Run: python3 lectures/L7/build_interactive_L7.py [--no-data]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import interactive_common  # noqa: E402
from interactive_common import slider, select, toggles, radios, play, charts, rnd, csv, ql_dir  # noqa: E402

K = 7

# (anchor, chart file / Quantlet, section key, id prefix)
BLOCKS = [('early-stopping', 'learning_curve', 'dnn', 'lc'),
          ('monthly-mae', 'monthly_ml', 'cmp', 'mm'),
          ('combination', 'combo_weight', 'cmp', 'cw'),
          ('dm-tests', 'dm_matrix', 'cmp', 'dm'),
          ('foundation', 'foundation_hour', 'fm', 'fh'),
          ('spike-decision', 'decision', 'spk', 'sd')]

SECTIONS = {
 'en': dict(dnn='Deep neural networks', fm='Gradient boosting and foundation models', cmp='Model comparison, combination and computational cost',
            spk='Spikes, negative prices and a case study'),
 'ro': dict(dnn='Rețele neuronale adînci', fm='Gradient boosting și modele fundație', cmp='Compararea modelelor, combinarea lor și costul de calcul',
            spk='Salturi de preț, prețuri negative și un studiu de caz'),
}

ABBR_EN = ('Abbreviations: MAE = mean absolute error; DNN = deep neural network; XGBoost = extreme gradient boosting; LEAR = LASSO-estimated '
           'autoregressive model (LASSO = least absolute shrinkage and selection operator); AW-LEAR / AW-ARX = average of LEAR / ARX '
           '(autoregressive model with exogenous inputs) forecasts over several calibration windows; GBM = gradient boosting machine; '
           'MLP = multilayer perceptron; DM = Diebold–Mariano test; ROC = receiver operating characteristic; AUC = area under the ROC curve.')
ABBR_RO = ('Abrevieri: MAE = eroarea absolută medie (mean absolute error); DNN = rețea neuronală adîncă (deep neural network); XGBoost = '
           'extreme gradient boosting; LEAR = model autoregresiv estimat cu LASSO (least absolute shrinkage and selection operator); '
           'AW-LEAR / AW-ARX = media prognozelor LEAR / ARX (model autoregresiv cu variabile exogene) pe mai multe ferestre de calibrare; '
           'GBM = gradient boosting machine; MLP = perceptron multistrat; DM = testul Diebold–Mariano; ROC = receiver operating '
           'characteristic (curba caracteristică de operare); AUC = aria de sub curba ROC.')

L = {
 'en': dict(h1='Lecture 7 · Machine learning and foundation models for electricity price forecasting',
   note='The slide of the lecture is on the left, the same figure on the right, recomputed in your browser from the saved results of '
        'the Quantlets (forecasts of the test year 1 November 2025 – 31 October 2026) and the Romanian day-ahead prices. The ▶ button '
        'moves the main parameter step by step. ' + ABBR_EN,
   src='Prices: OPCOM PZU (Romanian day-ahead market), via energy-charts.info (Fraunhofer ISE), CET delivery day × 24 hours (from 1 October '
       '2025 the hour is the mean of its four quarter-hours). Forecasts and probabilities: saved results of the Quantlets EMQA_L7_* (own '
       'computation: AW-LEAR recalibrated daily, DNN and XGBoost refitted monthly, Chronos zero-shot). Test year 2025-11-01 to 2026-10-31.'),
 'ro': dict(h1='Cursul 7 · Învățare automată și modele fundație pentru prognoza prețului energiei electrice',
   note='În stînga este slide-ul din curs, în dreapta aceeași figură, recalculată în browser din rezultatele salvate ale Quantlet-urilor '
        '(prognozele anului de test 1 noiembrie 2025 – 31 octombrie 2026) și din prețurile românești pentru ziua următoare. Butonul ▶ '
        'modifică parametrul principal pas cu pas. ' + ABBR_RO,
   src='Prețuri: OPCOM PZU (piața românească pentru ziua următoare), prin energy-charts.info (Fraunhofer ISE), ziua de livrare CET × 24 '
       'de ore (din 1 octombrie 2025, ora este media celor patru sferturi de oră). Prognoze și probabilități: rezultatele salvate ale '
       'Quantlet-urilor EMQA_L7_* (calcul propriu: AW-LEAR recalibrat zilnic, DNN și XGBoost reestimate lunar, Chronos fără antrenare, '
       'zero-shot). Anul de test: 2025-11-01 – 2026-10-31.'),
}

LAB = {
 'en': dict(naive='Naive', aw_arx='AW-ARX', aw_lear='AW-LEAR', gbm2='GBM (L2)', mlp2='MLP (L2)', xgb='XGBoost', dnn='DNN', bolt='Chronos-Bolt',
            chr2='Chronos-2', ens4='Ensemble of 4 (L2)', ens_ldx='AW-LEAR + DNN + XGBoost', ens_t4='AW-ARX + AW-LEAR + DNN + XGBoost',
            ens_lc='AW-LEAR + Chronos-2', ens_t5='5 models'),
 'ro': dict(naive='Naiv', aw_arx='AW-ARX', aw_lear='AW-LEAR', gbm2='GBM (C2)', mlp2='MLP (C2)', xgb='XGBoost', dnn='DNN', bolt='Chronos-Bolt',
            chr2='Chronos-2', ens4='Ansamblul de 4 (C2)', ens_ldx='AW-LEAR + DNN + XGBoost', ens_t4='AW-ARX + AW-LEAR + DNN + XGBoost',
            ens_lc='AW-LEAR + Chronos-2', ens_t5='5 modele'),
}
DM_MODELS = ['naive', 'aw_lear', 'ens4', 'xgb', 'dnn', 'bolt', 'chr2', 'ens_ldx', 'ens_t4', 'ens_lc', 'ens_t5']
MM_MODELS = ['naive', 'aw_lear', 'xgb', 'dnn', 'chr2', 'ens_ldx']
PAIRS = [('aw_lear', 'xgb'), ('aw_lear', 'dnn'), ('aw_lear', 'chr2'), ('xgb', 'dnn')]
FH_MODELS = ['naive', 'aw_lear', 'xgb', 'dnn', 'bolt', 'chr2']


def widgets(lang):
    ro = lang == 'ro'
    lab = LAB[lang]
    mo = [('all', 'Tot anul de test' if ro else 'Whole test year'), ('q1', 'Nov–ian' if ro else 'Nov–Jan'), ('q2', 'Feb–apr' if ro else 'Feb–Apr'),
          ('q3', 'Mai–iul' if ro else 'May–Jul'), ('q4', 'Aug–oct' if ro else 'Aug–Oct')]
    return {
     'early-stopping': (slider('lc-p', 'Răbdarea: epoci fără îmbunătățire pînă la oprire' if ro else 'Patience: epochs without improvement before stopping', 1, 30, 1, 25)
                        + play('lc'), charts('lc-chart', cls='one')),
     'monthly-mae': (toggles('mm-m', 'Modele' if ro else 'Models', [(k, lab[k]) for k in MM_MODELS], ['aw_lear', 'xgb', 'dnn', 'ens_ldx'])
                     + select('mm-v', 'Afișare' if ro else 'Show', [('lev', 'MAE lunar (EUR/MWh)' if ro else 'Monthly MAE (EUR/MWh)'),
                                                                   ('rel', 'Diferența față de AW-LEAR (EUR/MWh)' if ro else 'Difference from AW-LEAR (EUR/MWh)')], 'lev'),
                     charts('mm-chart', cls='one')),
     'combination': (select('cw-p', 'Perechea de modele' if ro else 'Pair of models', [(i, f'{lab[a]} + {lab[b]}') for i, (a, b) in enumerate(PAIRS)], 0)
                     + slider('cw-w', 'Ponderea w a celui de-al doilea model' if ro else 'Weight w of the second model', 0, 1, 0.05, 0.5) + play('cw'),
                     charts('cw-curve', 'cw-month')),
     'dm-tests': (select('dm-a', 'Modelul de referință (rîndul)' if ro else 'Benchmark model (row)', [(k, lab[k]) for k in DM_MODELS], 'aw_lear')
                  + select('dm-b', 'Modelul concurent (coloana)' if ro else 'Competing model (column)', [(k, lab[k]) for k in DM_MODELS], 'ens_ldx')
                  + slider('dm-L', 'Laguri Newey–West' if ro else 'Newey–West lags', 0, 14, 1, 7),
                  charts('dm-heat', 'dm-cum')),
     'foundation': (toggles('fh-m', 'Modele' if ro else 'Models', [(k, lab[k]) for k in FH_MODELS], ['naive', 'aw_lear', 'bolt', 'chr2'])
                    + select('fh-s', 'Lunile' if ro else 'Months', mo, 'all'), charts('fh-mae', 'fh-cov')),
     'spike-decision': (select('sd-m', 'Clasificatorul' if ro else 'Classifier', [('xgb', 'XGBoost'), ('logit', 'Regresie logistică' if ro else 'Logistic regression'),
                                                                                  ('persist', 'Persistență (ultimele 7 zile)' if ro else 'Persistence (last 7 days)')], 'xgb')
                        + slider('sd-t', 'Pragul de alertă pentru probabilitate' if ro else 'Alert threshold on the probability', 0.02, 0.98, 0.02, 0.42)
                        + slider('sd-c', 'Costul acțiunii C (EUR/MWh)' if ro else 'Cost of acting C (EUR/MWh)', 5, 70, 5, 30) + play('sd'),
                        charts('sd-roc', 'sd-val')),
    }


QA = {
 'en': {
  'early-stopping': ('The chosen DNN, refitted for October 2026, is trained with early stopping: training stops after 25 epochs without a lower error '
                     'on the last 15% of the days, and the weights of the best epoch are kept. Would training to the end (epoch 76) give a lower '
                     'error on those recent days?',
                     'No. The training error keeps falling, to 23.06 EUR/MWh at epoch 76, but the error on the recent days is lowest at epoch 51 '
                     '(24.50 EUR/MWh) and is 25.07 EUR/MWh at epoch 76: after epoch 51 the network memorises the past. With a short patience the '
                     'search stops too early: with 5 epochs it stops at epoch 30 and keeps epoch 25 (24.91 EUR/MWh).'),
  'monthly-mae': ('Alone, XGBoost and the DNN have a higher annual MAE than AW-LEAR (23.26 and 22.95 against 22.53 EUR/MWh). In how many of the '
                  '12 months does their equal-weight average with AW-LEAR beat AW-LEAR?',
                  'In 10 of 12 months (annual MAE 21.97 EUR/MWh); XGBoost and the DNN alone beat AW-LEAR in only 3 months each. All models err '
                  'most in the same months: October 2026 is the worst month of AW-LEAR (34.9 EUR/MWh). Chronos-2, a foundation model used '
                  'without training on these data, has the lowest annual MAE, 20.82 EUR/MWh.'),
  'combination': ('The errors of AW-LEAR and XGBoost have a correlation of 0.89. Is it worth estimating the weight of the combination instead of '
                  'using equal weights?',
                  'Hardly. The best weight seen afterwards on the test year is w = 0.40 (MAE 22.06 EUR/MWh) against 22.10 EUR/MWh with w = 0.5, '
                  'and the best weight is not known in advance. Because the correlation is below 1, the average errs less than either model '
                  '(23.26 for XGBoost, 22.53 for AW-LEAR). With AW-LEAR + Chronos-2 the weight seen afterwards would be w = 0.75 (20.57 EUR/MWh, against 20.81 with equal weights).'),
  'dm-tests': ('The equal-weight average AW-LEAR + DNN + XGBoost has an MAE 0.56 EUR/MWh lower than AW-LEAR. Is the difference significant '
               'in the one-sided Diebold–Mariano (DM) test at 5%?',
               'Yes: p = 0.001 (DM statistic 3.09 with 7 Newey–West lags). The test uses the 365 daily mean absolute errors; the cumulative '
               'difference on the right grows steadily through the year rather than in a few days. By contrast, adding AW-LEAR to Chronos-2 '
               'changes nothing (p = 0.491). Change the lags: the conclusion for this pair does not depend on them.'),
  'foundation': ('Chronos-2 is a foundation model: it forecasts from the last 2048 hourly prices, without being trained on Romanian data. In how '
                 'many of the 24 hours does it beat AW-LEAR over the test year, and are its 10%–90% bands well calibrated?',
                 'It beats AW-LEAR in all 24 hours (annual MAE 20.82 against 22.53 EUR/MWh). Its 10%–90% band, however, contains 76.5% of the '
                 'prices instead of 80%: it is too narrow and must be recalibrated (Lecture 2) before it is used for risk. Chronos-Bolt, smaller '
                 'and older, is level with AW-LEAR (22.15 EUR/MWh, DM p = 0.220).'),
  'spike-decision': ('A buyer with 1 MW of flexible load can move consumption out of an hour with an alert; acting costs C = 30 EUR/MWh, and a '
                     'missed spike costs on average L̄ = 72.5 EUR/MWh (mean excess over the spike threshold in the validation year). Which '
                     'probability threshold should trigger an alert: 0.5, C/L̄ = 0.414, or the threshold that was best afterwards?',
                     'C/L̄ = 30/72.5 = 0.414, fixed before the test year from the costs. With XGBoost it gives 1806 alerts and 33.0 thousand EUR per MW '
                     'and year; persistence gives 11.8 and perfect foresight 62.4. On this test year the threshold 0.5 happened to do slightly '
                     'better (36.7) and 0.64 best: these are choices made with hindsight. Raise C: the rule asks for a higher probability before acting.'),
 },
 'ro': {
  'early-stopping': ('Rețeaua DNN aleasă, reestimată pentru octombrie 2026, este antrenată cu oprire timpurie (early stopping): antrenarea se '
                     'oprește după 25 de epoci fără o eroare mai mică pe ultimele 15% dintre zile, iar ponderile celei mai bune epoci sînt păstrate. '
                     'Ar da antrenarea pînă la capăt (epoca 76) o eroare mai mică pe aceste zile recente?',
                     'Nu. Eroarea de antrenare continuă să scadă, pînă la 23,06 EUR/MWh în epoca 76, dar eroarea pe zilele recente este minimă în '
                     'epoca 51 (24,50 EUR/MWh) și ajunge la 25,07 EUR/MWh în epoca 76: după epoca 51, rețeaua memorează trecutul. Cu o răbdare '
                     'scurtă, căutarea se oprește prea devreme: cu 5 epoci se oprește în epoca 30 și păstrează epoca 25 (24,91 EUR/MWh).'),
  'monthly-mae': ('Singure, XGBoost și DNN au un MAE anual mai mare decît AW-LEAR (23,26 și 22,95 față de 22,53 EUR/MWh). În cîte dintre cele '
                  '12 luni bate AW-LEAR media lor cu ponderi egale cu AW-LEAR?',
                  'În 10 din 12 luni (MAE anual 21,97 EUR/MWh); singure, XGBoost și DNN bat AW-LEAR doar în cîte 3 luni. Toate modelele greșesc '
                  'cel mai mult în aceleași luni: octombrie 2026 este luna cea mai slabă pentru AW-LEAR (34,9 EUR/MWh). Chronos-2, un model '
                  'fundație folosit fără antrenare pe aceste date, are cel mai mic MAE anual, 20,82 EUR/MWh.'),
  'combination': ('Erorile AW-LEAR și XGBoost au corelația 0,89. Merită estimată ponderea combinației în locul ponderilor egale?',
                  'Aproape deloc. Cea mai bună pondere văzută ulterior pe anul de test este w = 0,40 (MAE 22,06 EUR/MWh), față de 22,10 EUR/MWh '
                  'cu w = 0,5, iar ponderea cea mai bună nu este cunoscută dinainte. Deoarece corelația este sub 1, media greșește mai puțin decît '
                  'fiecare model (23,26 pentru XGBoost, 22,53 pentru AW-LEAR). Pentru AW-LEAR + Chronos-2, ponderea văzută ulterior ar fi '
                  'w = 0,75 (20,57 EUR/MWh, față de 20,81 cu ponderi egale).'),
  'dm-tests': ('Media cu ponderi egale AW-LEAR + DNN + XGBoost are un MAE cu 0,56 EUR/MWh mai mic decît AW-LEAR. Este diferența semnificativă '
               'în testul Diebold–Mariano (DM) unilateral, la 5%?',
               'Da: p = 0,001 (statistica DM 3,09, cu 7 laguri Newey–West). Testul folosește cele 365 de erori absolute medii zilnice; diferența '
               'cumulată din dreapta crește constant de-a lungul anului, nu doar în cîteva zile. În schimb, adăugarea AW-LEAR la Chronos-2 nu '
               'schimbă nimic (p = 0,491). Modificați numărul de laguri: concluzia pentru această pereche nu depinde de el.'),
  'foundation': ('Chronos-2 este un model fundație: prognozează din ultimele 2048 de prețuri orare, fără să fi fost antrenat pe date românești. '
                 'În cîte dintre cele 24 de ore bate AW-LEAR pe anul de test și sînt benzile sale 10%–90% bine calibrate?',
                 'Bate AW-LEAR în toate cele 24 de ore (MAE anual 20,82 față de 22,53 EUR/MWh). Banda sa 10%–90% conține însă 76,5% dintre '
                 'prețuri, nu 80%: este prea îngustă și trebuie recalibrată (Cursul 2) înainte de a fi folosită pentru risc. Chronos-Bolt, '
                 'mai mic și mai vechi, este la egalitate cu AW-LEAR (22,15 EUR/MWh, DM p = 0,220).'),
  'spike-decision': ('Un cumpărător cu 1 MW de consum flexibil poate muta consumul dintr-o oră cu alertă; acțiunea costă C = 30 EUR/MWh, iar un '
                     'salt de preț ratat costă în medie L̄ = 72,5 EUR/MWh (excesul mediu peste pragul de salt în anul de validare). Ce prag de '
                     'probabilitate ar trebui să declanșeze o alertă: 0,5, C/L̄ = 0,414 sau pragul care s-a dovedit cel mai bun ulterior?',
                     'C/L̄ = 30/72,5 = 0,414, fixat dinaintea anului de test, din costuri. Cu XGBoost dă 1806 alerte și 33,0 mii EUR pe MW și '
                     'an; persistența dă 11,8, iar previziunea perfectă 62,4. Pe acest an de test, pragul 0,5 a ieșit puțin mai bine (36,7), iar '
                     '0,64 cel mai bine: acestea sînt alegeri făcute ulterior. Măriți C: regula cere o probabilitate mai mare înainte de a acționa.'),
 },
}

_TEXT_COMMON = """ lab: %s,
 months: %s,
"""

TEXT_JS = {
 'en': r"""window.LK_TEXT = {
 LAB_PLACEHOLDER
 eur: 'EUR/MWh', epoch: 'Epoch', mae: 'MAE (EUR/MWh)', train: 'Training days', valid: 'Last 15% of the days (validation)',
 best: 'Best epoch (weights kept)', stop: 'Stop',
 lc: (p, s, b, vb, ts, vs) => `Patience ${p}: training stops at epoch ${s} and keeps the weights of epoch ${b} (validation MAE ${vb} EUR/MWh). At epoch ${s}: training MAE ${ts}, validation MAE ${vs}.`,
 lcEnd: (t, v) => `Trained to the end (epoch 76): training MAE ${t}, validation MAE ${v} EUR/MWh.`,
 mmLev: 'Monthly MAE (EUR/MWh)', mmRel: 'MAE minus MAE of AW-LEAR (EUR/MWh)',
 mm: (m, a, n) => `${m}: annual MAE ${a} EUR/MWh; beats AW-LEAR in ${n} of 12 months.`,
 cwCurve: 'MAE of the combination (EUR/MWh)', cwW: 'Weight w of the second model', cwMonth: 'Monthly MAE minus AW-LEAR (EUR/MWh)',
 cw: (a, b, w, m, ma, mb, r) => `MAE of (1 − w)·${a} + w·${b} with w = ${w}: ${m} EUR/MWh (${a} alone ${ma}, ${b} alone ${mb}); error correlation ${r}.`,
 cwBest: (w, m, m5) => `Best weight seen afterwards: w = ${w} (MAE ${m}); equal weights: ${m5} EUR/MWh.`,
 cwMonthN: n => `The combination beats the first model in ${n} of 12 months.`,
 dmHeat: 'One-sided DM p-value: column more accurate than row', dmCum: 'Cumulative daily MAE difference, row − column (EUR/MWh)',
 dm: (a, b, ma, mb, s, p) => `${a} (MAE ${ma}) against ${b} (MAE ${mb}): DM statistic ${s}, one-sided p-value ${p}.`,
 dmYes: 'The column model is significantly more accurate at 5%.', dmNo: 'No significant gain at 5%.', dmSame: 'Choose two different models.',
 fhMae: 'MAE by hour (EUR/MWh)', fhCov: 'Chronos-2: share of prices inside the 10%–90% band', hour: 'Hour of the day (CET)', share: 'Share (%)',
 nominal: 'Nominal 80%',
 fh: (n, m) => `${n}: MAE ${m} EUR/MWh.`,
 fhWin: (n) => `Chronos-2 beats AW-LEAR in ${n} of the 24 hours.`, fhCovT: c => `Coverage of the Chronos-2 10%–90% band: ${c} (nominal 80%).`,
 fpr: 'False alarm rate (FPR)', tpr: 'Spikes caught (TPR)', roc: 'ROC curve, spike hours of the test year', point: 'Chosen threshold',
 val: 'Value per MW and year (thousand EUR)', thr: 'Probability threshold', cl: 'C/L̄',
 sd: (m, a, auc, n, tp, fp, fn) => `${m}: AUC ${auc}. Threshold ${a}: ${n} alerts, ${tp} spikes caught, ${fp} false alarms, ${fn} spikes missed.`,
 sd2: (v, c, cl, vcl, vp) => `Value at this threshold: ${v} thousand EUR per MW and year; with C = ${c} EUR/MWh the rule C/L̄ gives ${cl} (value ${vcl}); perfect foresight ${vp}.`,
 spikes: (n, lo, hi) => `${n} spike hours in the test year (price above the 90th percentile of the previous 365 days: ${lo}–${hi} EUR/MWh).`
};
""",
 'ro': r"""window.LK_TEXT = {
 LAB_PLACEHOLDER
 eur: 'EUR/MWh', epoch: 'Epoca', mae: 'MAE (EUR/MWh)', train: 'Zilele de antrenare', valid: 'Ultimele 15% dintre zile (validare)',
 best: 'Cea mai bună epocă (ponderi păstrate)', stop: 'Oprire',
 lc: (p, s, b, vb, ts, vs) => `Răbdarea ${p}: antrenarea se oprește în epoca ${s} și păstrează ponderile epocii ${b} (MAE de validare ${vb} EUR/MWh). În epoca ${s}: MAE de antrenare ${ts}, MAE de validare ${vs}.`,
 lcEnd: (t, v) => `Antrenare pînă la capăt (epoca 76): MAE de antrenare ${t}, MAE de validare ${v} EUR/MWh.`,
 mmLev: 'MAE lunar (EUR/MWh)', mmRel: 'MAE minus MAE-ul AW-LEAR (EUR/MWh)',
 mm: (m, a, n) => `${m}: MAE anual ${a} EUR/MWh; bate AW-LEAR în ${n} din 12 luni.`,
 cwCurve: 'MAE-ul combinației (EUR/MWh)', cwW: 'Ponderea w a celui de-al doilea model', cwMonth: 'MAE lunar minus AW-LEAR (EUR/MWh)',
 cw: (a, b, w, m, ma, mb, r) => `MAE pentru (1 − w)·${a} + w·${b} cu w = ${w}: ${m} EUR/MWh (${a} singur ${ma}, ${b} singur ${mb}); corelația erorilor ${r}.`,
 cwBest: (w, m, m5) => `Cea mai bună pondere văzută ulterior: w = ${w} (MAE ${m}); ponderi egale: ${m5} EUR/MWh.`,
 cwMonthN: n => `Combinația bate primul model în ${n} din 12 luni.`,
 dmHeat: 'Valoarea p DM unilaterală: coloana mai precisă decît rîndul', dmCum: 'Diferența cumulată a MAE zilnic, rînd − coloană (EUR/MWh)',
 dm: (a, b, ma, mb, s, p) => `${a} (MAE ${ma}) față de ${b} (MAE ${mb}): statistica DM ${s}, valoarea p unilaterală ${p}.`,
 dmYes: 'Modelul din coloană este semnificativ mai precis la 5%.', dmNo: 'Niciun cîștig semnificativ la 5%.', dmSame: 'Alegeți două modele diferite.',
 fhMae: 'MAE pe oră (EUR/MWh)', fhCov: 'Chronos-2: ponderea prețurilor din banda 10%–90%', hour: 'Ora zilei (CET)', share: 'Pondere (%)',
 nominal: 'Nominal 80%',
 fh: (n, m) => `${n}: MAE ${m} EUR/MWh.`,
 fhWin: (n) => `Chronos-2 bate AW-LEAR în ${n} din cele 24 de ore.`, fhCovT: c => `Acoperirea benzii 10%–90% a Chronos-2: ${c} (nominal 80%).`,
 fpr: 'Rata alarmelor false (FPR)', tpr: 'Salturi detectate (TPR)', roc: 'Curba ROC, orele cu salt din anul de test', point: 'Pragul ales',
 val: 'Valoarea pe MW și an (mii EUR)', thr: 'Pragul de probabilitate', cl: 'C/L̄',
 sd: (m, a, auc, n, tp, fp, fn) => `${m}: AUC ${auc}. Pragul ${a}: ${window.EMQAI.cnt(n, 'alertă', 'alerte')}, ${window.EMQAI.cnt(tp, 'salt detectat', 'salturi detectate')}, ${window.EMQAI.cnt(fp, 'alarmă falsă', 'alarme false')}, ${window.EMQAI.cnt(fn, 'salt ratat', 'salturi ratate')}.`,
 sd2: (v, c, cl, vcl, vp) => `Valoarea la acest prag: ${v} mii EUR pe MW și an; cu C = ${c} EUR/MWh, regula C/L̄ dă ${cl} (valoarea ${vcl}); previziune perfectă ${vp}.`,
 spikes: (n, lo, hi) => `${window.EMQAI.cnt(n, 'oră', 'ore')} cu salt în anul de test (preț peste percentila 90 a celor 365 de zile anterioare: ${lo}–${hi} EUR/MWh).`
};
""",
}
for _lang in ('en', 'ro'):
    import json as _json
    _mon = ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'] if _lang == 'en' else \
        ['nov', 'dec', 'ian', 'feb', 'mar', 'apr', 'mai', 'iun', 'iul', 'aug', 'sep', 'oct']
    TEXT_JS[_lang] = TEXT_JS[_lang].replace('LAB_PLACEHOLDER', _TEXT_COMMON.strip() % (_json.dumps(LAB[_lang], ensure_ascii=False),
                                                                                         _json.dumps(_mon, ensure_ascii=False)))
del _lang, _mon


# ---------------------------------------------------------------- data (saved Quantlet results + real prices only)
def day_matrix(s):
    """UTC-indexed hourly series -> CET delivery day x 24 hours (rule of the Lecture 7 Quantlets: 25-h day averaged, 23-h day interpolated)."""
    import numpy as np
    import pandas as pd
    TZ = 'Europe/Brussels'
    s = s.copy()
    s.index = pd.to_datetime(s.index, utc=True).tz_convert(TZ)
    df = pd.DataFrame({'v': s.values, 'day': s.index.tz_localize(None).normalize(), 'h': s.index.hour})
    m = df.groupby(['day', 'h'])['v'].mean().unstack('h').reindex(columns=range(24))
    days = m.index
    nh = ((((days + pd.Timedelta(days=1)).tz_localize(TZ)) - days.tz_localize(TZ)) / pd.Timedelta(hours=1)).astype(int)
    for dd in days[np.asarray(nh != 24)]:
        if pd.isna(m.loc[dd, 2]):
            m.loc[dd, 2] = 0.5 * (m.loc[dd, 1] + m.loc[dd, 3])
    return m.dropna(how='any')


def data():
    import numpy as np
    import pandas as pd
    npz = lambda c: np.load(os.path.join(ql_dir(K, c), f'{c}_results.npz'))  # noqa: E731
    HP = csv('power_da_prices_hourly_utc.csv', usecols=['timestamp_utc', 'RO'], index_col=0)
    PM = day_matrix(HP['RO'].dropna())
    dmr = npz('dm_matrix')
    days = pd.to_datetime(dmr['days'])
    A = PM.reindex(days).values.astype(float)
    assert not np.isnan(A).any()
    M = {k: dmr[k].astype(float) for k in dmr.files if k != 'days'}
    M['ens4'] = np.mean([M['aw_arx'], M['aw_lear'], M['gbm2'], M['mlp2']], 0)
    M['ens_ldx'] = (M['aw_lear'] + M['dnn'] + M['xgb']) / 3
    M['ens_t4'] = np.mean([M['aw_arx'], M['aw_lear'], M['dnn'], M['xgb']], 0)
    M['ens_lc'] = 0.5 * (M['aw_lear'] + M['chr2'])
    M['ens_t5'] = np.mean([M['aw_arx'], M['aw_lear'], M['dnn'], M['xgb'], M['chr2']], 0)
    mo = days.to_period('M')
    months = sorted(set(mo))
    out = {'t0': str(days[0].date()), 'n': len(days), 'months': [str(m) for m in months], 'mon': [int((mo == m).sum()) for m in months]}

    # 1. learning curve of the chosen DNN (refit for 2026-10)
    lc = npz('learning_curve')
    out['lc'] = {'tr': rnd(lc['curve_train'], 3), 'va': rnd(lc['curve_val'], 3)}

    # 2.-4. daily mean absolute errors (DM loss) of every model and combination; monthly MAE = mean of the daily values
    keys = sorted(set(DM_MODELS) | set(MM_MODELS) | set(FH_MODELS))
    out['dl'] = {k: rnd(np.mean(np.abs(A - M[k]), 1), 3) for k in keys}

    # 3. combination weight grid for a few pairs: overall and monthly MAE, error correlation
    W = np.round(np.linspace(0, 1, 21), 2)
    out['cw'] = []
    for a, b in PAIRS:
        ea, eb = A - M[a], A - M[b]
        tot, mon = [], []
        for w in W:
            e = np.abs(A - ((1 - w) * M[a] + w * M[b]))
            tot.append(e.mean())
            mon.append([e[mo == m].mean() for m in months])
        out['cw'].append({'a': a, 'b': b, 'w': W.tolist(), 'mae': rnd(tot, 3), 'mon': rnd(mon, 2),
                          'r': round(float(np.corrcoef(ea.ravel(), eb.ravel())[0, 1]), 3)})

    # 5. MAE by hour and month, coverage of the Chronos-2 10%-90% band
    fh = npz('foundation_hour')
    assert np.allclose(fh['chr2'], dmr['chr2'])
    out['fh'] = {k: [rnd(np.abs(A - M[k])[mo == m].mean(0), 2) for m in months] for k in FH_MODELS}
    inb = (A >= fh['chr2_q10']) & (A <= fh['chr2_q90'])
    out['fh']['cov'] = [inb[mo == m].sum(0).tolist() for m in months]

    # 6. spike hours, classifier probabilities and value of the cost-loss rule
    def theta(t):
        ms = t.replace(day=1)
        w = PM.loc[ms - pd.Timedelta(days=365):ms - pd.Timedelta(days=1)].values.ravel()
        return float(np.quantile(w, 0.90))
    TH = np.array([theta(t) for t in days])
    VD = pd.date_range(days[0] - pd.Timedelta(days=365), days[0] - pd.Timedelta(days=1))
    PV = PM.reindex(VD).values
    THV = np.array([theta(t) for t in VD])[:, None]
    lbar = float((PV - THV)[PV > THV].mean())
    dc = npz('decision')
    past = np.stack([PM.reindex(days - pd.Timedelta(days=k)).values for k in range(1, 8)], 0)
    persist = (past > TH[None, :, None]).mean(0)
    out['sd'] = {'a': rnd(A.ravel(), 2), 'th': rnd(TH, 2), 'lbar': round(lbar, 3),
                 'xgb': rnd(dc['spike_xgb'].astype(float).ravel(), 4), 'logit': rnd(dc['spike_logit'].ravel(), 4),
                 'persist': rnd(persist.ravel(), 4)}
    return out


if __name__ == '__main__':
    interactive_common.build(sys.modules[__name__])
