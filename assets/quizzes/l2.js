// ============================================================
// Quiz bank for lecture id 'l2': Forecasting day-ahead electricity prices (EN + RO)
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.EMQA_DATA.quizzes['l2'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 1,
            "en": {
                "title": "Information set at noon",
                "text": "A forecast for delivery day $d$ on the day-ahead market (PZU, Piața pentru Ziua Următoare) must be sent before 12:00 Central European Time (CET) on day $d-1$. Which input may it legally use?",
                "options": [
                    "The realised load of the whole day $d-1$",
                    "All 24 hourly prices of day $d-1$, fixed by the auction held on day $d-2$",
                    "The metered wind and solar output of the whole day $d-1$",
                    "The price of the first hour of day $d$, published shortly after the auction"
                ],
                "correctExplanation": "The prices of $d-1$ were published around 13:00 CET on $d-2$, so they are known at gate closure. Realised load, wind and solar are complete only up to $d-2$, and prices of day $d$ exist only after the auction itself.",
                "incorrectExplanation": "The rule is what is public at 12:00 CET on $d-1$. Day $d-1$ is not yet fully metered and day $d$ is decided by the auction; using either is leakage of future information, which makes a backtest look excellent but cannot be run on a trading desk."
            },
            "ro": {
                "title": "Informația disponibilă la prînz",
                "text": "Prognoza pentru ziua de livrare $d$ pe Piața pentru Ziua Următoare (PZU) trebuie trimisă înainte de ora 12:00 a Europei Centrale (CET) din ziua $d-1$. Ce variabilă de intrare poate folosi în mod corect?",
                "options": [
                    "Consumul realizat în toată ziua $d-1$",
                    "Toate cele 24 de prețuri orare ale zilei $d-1$, stabilite prin licitația din ziua $d-2$",
                    "Producția eoliană și solară măsurată în toată ziua $d-1$",
                    "Prețul primei ore din ziua $d$, publicat la scurt timp după licitație"
                ],
                "correctExplanation": "Prețurile zilei $d-1$ au fost publicate în jurul orei 13:00 CET din ziua $d-2$, deci se cunosc la închiderea licitației. Consumul și producția eoliană și solară realizate sînt complete numai pînă în ziua $d-2$, iar prețurile zilei $d$ apar abia după licitație.",
                "incorrectExplanation": "Regula este ce se cunoaște public la ora 12:00 CET din ziua $d-1$. Ziua $d-1$ nu este încă măsurată complet, iar ziua $d$ se decide prin licitație; folosirea lor înseamnă informație din viitor, iar testarea retrospectivă pare excelentă, dar nu poate fi rulată într-un birou de tranzacționare."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Role of the burn-in",
                "text": "The sample from 1 Jan 2022 to 31 Oct 2026 is split into a first calibration window of 728 days, a burn-in of 182 days and a test year of 365 days. What are the burn-in forecasts used for?",
                "options": [
                    "Only to calibrate the prediction intervals",
                    "To choose the best point-forecast model before the test year",
                    "To estimate the coefficients of the expert models once and for all",
                    "To replace the days of the test year with missing data"
                ],
                "correctExplanation": "The 182 burn-in days produce forecasts whose errors serve only to calibrate the prediction intervals; every error reported in the lecture is measured on the 365-day test year, which is touched once, at the end.",
                "incorrectExplanation": "The models are re-estimated every day on a rolling window ending at $d-1$, so the burn-in is not an estimation sample. Its forecasts supply the past errors that the interval methods need before the test year starts."
            },
            "ro": {
                "title": "Rolul perioadei de rodaj",
                "text": "Eșantionul 1 ianuarie 2022 – 31 octombrie 2026 se împarte într-o primă fereastră de calibrare de 728 de zile, un rodaj de 182 de zile și un an de test de 365 de zile. La ce servesc prognozele din rodaj?",
                "options": [
                    "Numai la calibrarea intervalelor de prognoză",
                    "La alegerea celui mai bun model de prognoză punctuală înaintea anului de test",
                    "La estimarea, o dată pentru totdeauna, a coeficienților modelelor expert",
                    "La înlocuirea zilelor din anul de test care au date lipsă"
                ],
                "correctExplanation": "Cele 182 de zile de rodaj produc prognoze ale căror erori servesc numai la calibrarea intervalelor de prognoză; toate erorile raportate în curs se măsoară pe anul de test de 365 de zile, folosit o singură dată, la final.",
                "incorrectExplanation": "Modelele se reestimează zilnic pe o fereastră glisantă care se încheie în ziua $d-1$, deci rodajul nu este un eșantion de estimare. Prognozele lui furnizează erorile trecute de care au nevoie metodele de interval înainte de începutul anului de test."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Age of the information",
                "text": "The forecast that copies the price of the same hour $k$ days earlier has a mean absolute error (MAE) of 29.37 EUR/MWh for $k=1$, 38.52 for $k=2$ and 34.41 for $k=7$ on the test year. Why does the error fall again at $k=7$?",
                "options": [
                    "Prices of a week earlier are less volatile than recent prices",
                    "A week-old price is averaged over more hours than yesterday's price",
                    "The test year contains more weekend days than working days",
                    "The same weekday a week earlier shares the weekly pattern of consumption"
                ],
                "correctExplanation": "Older information is generally worse, but the weekly cycle is strong: the same weekday one week earlier has the same consumption pattern, so its MAE (34.41) is lower than that of the price of two days earlier (38.52).",
                "incorrectExplanation": "Each forecast copies one hourly price, so no averaging is involved. The dip at $k=7$ reflects the weekly cycle of demand, which is why the naive benchmark uses the price of $d-7$ on some days."
            },
            "ro": {
                "title": "Vechimea informației",
                "text": "Prognoza care copiază prețul aceleiași ore de acum $k$ zile are, în anul de test, eroarea absolută medie (MAE) 29,37 EUR/MWh pentru $k=1$, 38,52 pentru $k=2$ și 34,41 pentru $k=7$. De ce scade din nou eroarea la $k=7$?",
                "options": [
                    "Prețurile de acum o săptămînă sînt mai puțin volatile decît cele recente",
                    "Prețul de acum o săptămînă este mediat pe mai multe ore decît prețul de ieri",
                    "Anul de test conține mai multe zile de weekend decît zile lucrătoare",
                    "Aceeași zi a săptămînii trecute are același tipar săptămînal al consumului"
                ],
                "correctExplanation": "Informația mai veche este în general mai slabă, dar ciclul săptămînal este puternic: aceeași zi a săptămînii trecute are același tipar al consumului, deci MAE (34,41) este mai mică decît pentru prețul de acum două zile (38,52).",
                "incorrectExplanation": "Fiecare prognoză copiază un singur preț orar, deci nu există nicio mediere. Scăderea de la $k=7$ reflectă ciclul săptămînal al cererii, motiv pentru care modelul naiv folosește în unele zile prețul din $d-7$."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Naive forecast for Monday",
                "text": "It is Sunday, 11:30 Central European Time (CET), and you must forecast Monday at 19:00 with the naive benchmark of the lecture. Which price do you use?",
                "options": [
                    "Sunday's price at 19:00, the most recent price of the same hour",
                    "Saturday's price at 19:00, the last working-pattern day",
                    "The previous Monday's price at 19:00, from day $d-7$",
                    "The average of the last seven prices at 19:00"
                ],
                "correctExplanation": "The naive rule uses $P_{d-7,h}$ on Mondays, Saturdays and Sundays and $P_{d-1,h}$ from Tuesday to Friday. On those three days the price of $d-7$ gives a mean absolute error (MAE) of 29.87 EUR/MWh against 33.48 for the price of $d-1$.",
                "incorrectExplanation": "Monday follows a weekend, so yesterday's price has the wrong pattern. The data justify the switch: on Mondays, Saturdays and Sundays the week-old price is more accurate than the most recent one."
            },
            "ro": {
                "title": "Prognoza naivă pentru luni",
                "text": "Este duminică, ora 11:30 a Europei Centrale (CET), și trebuie să prognozați prețul de luni pentru ora 19:00 cu modelul naiv din curs. Ce preț folosiți?",
                "options": [
                    "Prețul de duminică de la ora 19:00, cel mai recent preț al aceleiași ore",
                    "Prețul de sîmbătă de la ora 19:00, ultima zi cu tipar asemănător",
                    "Prețul de luni trecută de la ora 19:00, din ziua $d-7$",
                    "Media ultimelor șapte prețuri de la ora 19:00"
                ],
                "correctExplanation": "Regula naivă folosește $P_{d-7,h}$ lunea, sîmbăta și duminica și $P_{d-1,h}$ de marți pînă vineri. În aceste trei zile, prețul din $d-7$ dă o eroare absolută medie (MAE) de 29,87 EUR/MWh, față de 33,48 pentru prețul din $d-1$.",
                "incorrectExplanation": "Lunea urmează unui weekend, deci prețul de ieri are alt tipar. Datele justifică schimbarea regulii: lunea, sîmbăta și duminica, prețul de acum o săptămînă este mai precis decît cel mai recent."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Naive error versus price",
                "text": "On the test year the naive benchmark has a mean absolute error (MAE) of 27.82 EUR/MWh, and the mean price is 134.46 EUR/MWh. Roughly how large is the typical naive error relative to the price level?",
                "options": [
                    "About 4.8% of the price",
                    "About 34.5% of the price",
                    "About 79% of the price",
                    "About 21% of the price, roughly one fifth"
                ],
                "correctExplanation": "27.82 / 134.46 is about 0.21, so the naive error is about one fifth of the average price, as the lecture states.",
                "incorrectExplanation": "Divide the MAE by the mean price: 27.82 / 134.46 is about 0.21. The 34.5% figure is the symmetric percentage error of the naive rule, a different measure computed hour by hour."
            },
            "ro": {
                "title": "Eroarea naivă față de preț",
                "text": "În anul de test, modelul naiv are eroarea absolută medie (MAE) 27,82 EUR/MWh, iar prețul mediu este 134,46 EUR/MWh. Cît reprezintă, aproximativ, eroarea tipică a modelului naiv din nivelul prețului?",
                "options": [
                    "Circa 4,8% din preț",
                    "Circa 34,5% din preț",
                    "Circa 79% din preț",
                    "Circa 21% din preț, aproximativ o cincime"
                ],
                "correctExplanation": "27,82 / 134,46 este circa 0,21, deci eroarea naivă reprezintă circa o cincime din prețul mediu, așa cum arată cursul.",
                "incorrectExplanation": "Împărțiți MAE la prețul mediu: 27,82 / 134,46 este circa 0,21. Valoarea de 34,5% este eroarea procentuală simetrică a modelului naiv, o altă măsură, calculată oră cu oră."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Computing the rMAE",
                "text": "LEAR averaged across calibration windows (AW-LEAR; LEAR is the autoregression estimated with the least absolute shrinkage and selection operator, LASSO) has a mean absolute error (MAE) of 22.53 EUR/MWh on the test year, and the naive benchmark 27.82 EUR/MWh on the same hours. What is the relative MAE (rMAE)?",
                "options": [
                    "0.190",
                    "0.810",
                    "1.235",
                    "0.795"
                ],
                "correctExplanation": "$\\text{rMAE}=\\text{MAE}_{\\text{model}}/\\text{MAE}_{\\text{naive}}=22.53/27.82\\approx0.810$. A value below 1 means the model beats naive, here by about 19%.",
                "incorrectExplanation": "The rMAE is the ratio of the model MAE to the naive MAE, not one minus it and not its inverse. The value 0.795 belongs to the ensemble of 4, the best model of the lecture."
            },
            "ro": {
                "title": "Calculul rMAE",
                "text": "LEAR mediat pe ferestre de calibrare (AW-LEAR; LEAR este autoregresia estimată cu operatorul de contracție și selecție în normă absolută, LASSO) are în anul de test eroarea absolută medie (MAE) 22,53 EUR/MWh, iar modelul naiv 27,82 EUR/MWh pe aceleași ore. Cît este MAE relativă (rMAE)?",
                "options": [
                    "0,190",
                    "0,810",
                    "1,235",
                    "0,795"
                ],
                "correctExplanation": "$\\text{rMAE}=\\text{MAE}_{\\text{model}}/\\text{MAE}_{\\text{naive}}=22{,}53/27{,}82\\approx0{,}810$. O valoare sub 1 înseamnă că modelul este mai precis decît cel naiv, aici cu circa 19%.",
                "incorrectExplanation": "rMAE este raportul dintre MAE a modelului și MAE a modelului naiv, nu unu minus acest raport și nici inversul lui. Valoarea 0,795 aparține ansamblului de 4 modele, cel mai bun model din curs."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Median or mean forecast",
                "text": "Which forecast minimises the mean absolute error (MAE), and which minimises the root mean squared error (RMSE)?",
                "options": [
                    "The MAE is minimised by the mean forecast, the RMSE by the median forecast",
                    "Both are minimised by the mean forecast",
                    "Both are minimised by the median forecast",
                    "The MAE is minimised by the median forecast, the RMSE by the mean forecast"
                ],
                "correctExplanation": "Absolute errors are minimised by the median, squared errors by the mean. Because the RMSE squares errors, it punishes price spikes more than the MAE does.",
                "incorrectExplanation": "The two measures target different points of the distribution: the median for absolute loss and the mean for squared loss. That is why a model can rank differently on MAE and on RMSE when spikes are present."
            },
            "ro": {
                "title": "Prognoza mediană sau medie",
                "text": "Ce prognoză minimizează eroarea absolută medie (MAE) și ce prognoză minimizează rădăcina erorii pătratice medii (RMSE)?",
                "options": [
                    "MAE este minimă pentru prognoza medie, RMSE pentru prognoza mediană",
                    "Ambele sînt minime pentru prognoza medie",
                    "Ambele sînt minime pentru prognoza mediană",
                    "MAE este minimă pentru prognoza mediană, RMSE pentru prognoza medie"
                ],
                "correctExplanation": "Erorile absolute sînt minimizate de mediană, iar erorile pătratice de medie. Pentru că RMSE ridică erorile la pătrat, ea penalizează salturile de preț mai puternic decît MAE.",
                "incorrectExplanation": "Cele două măsuri țintesc puncte diferite ale distribuției: mediana pentru pierderea absolută și media pentru pierderea pătratică. De aceea, cînd există salturi de preț, ordinea modelelor după MAE poate diferi de cea după RMSE."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "MAPE at prices near zero",
                "text": "The mean absolute percentage error (MAPE) of AW-LEAR (LEAR, the LASSO-estimated autoregression, averaged across calibration windows) is 5,777.7% on the test year. Without the 387 hours with absolute price below 5 EUR/MWh it falls to 32.4%. What should you tell an alarmed board?",
                "options": [
                    "MAPE divides by prices near zero; those few hours produce 99.5% of it, so report the mean absolute error (MAE) and the relative MAE (rMAE) instead",
                    "The model is broken and must be replaced before the next auction",
                    "The 387 hours are data errors and should be deleted from the test year",
                    "MAPE is correct, but must be reported only on weekdays to remove the weekend effect"
                ],
                "correctExplanation": "When the price is close to zero, a small error in EUR/MWh becomes an enormous percentage, and for negative prices the measure loses meaning. The same forecast has MAE 22.53 EUR/MWh and rMAE 0.810.",
                "incorrectExplanation": "The forecast is the same; only the measure changes. Hours with near-zero prices are real (sunny hours with high solar output), so they must stay in the evaluation; the fix is to use MAE and rMAE, never MAPE, for power prices."
            },
            "ro": {
                "title": "MAPE la prețuri apropiate de zero",
                "text": "Eroarea procentuală absolută medie (MAPE) pentru AW-LEAR (LEAR, autoregresia estimată cu LASSO, mediată pe ferestre de calibrare) este 5 777,7% în anul de test. Fără cele 387 de ore în care prețul are valoarea absolută sub 5 EUR/MWh, ea scade la 32,4%. Ce îi spuneți consiliului de administrație alarmat?",
                "options": [
                    "MAPE împarte la prețuri apropiate de zero; aceste puține ore produc 99,5% din valoarea ei, deci raportați eroarea absolută medie (MAE) și MAE relativă (rMAE)",
                    "Modelul este defect și trebuie înlocuit înainte de următoarea licitație",
                    "Cele 387 de ore sînt erori de date și trebuie eliminate din anul de test",
                    "MAPE este corectă, dar trebuie raportată numai pentru zilele lucrătoare, pentru a elimina efectul weekendului"
                ],
                "correctExplanation": "Cînd prețul este aproape de zero, o eroare mică în EUR/MWh devine un procent uriaș, iar pentru prețuri negative măsura nu mai are sens. Aceeași prognoză are MAE 22,53 EUR/MWh și rMAE 0,810.",
                "incorrectExplanation": "Prognoza este aceeași; se schimbă doar măsura. Orele cu prețuri apropiate de zero sînt reale (ore însorite, cu multă producție solară), deci rămîn în evaluare; soluția este MAE și rMAE, niciodată MAPE, pentru prețurile energiei electrice."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Insignificant DM result",
                "text": "ARX averaged across windows (AW-ARX; ARX is the autoregressive model with exogenous variables) against LEAR averaged across windows (AW-LEAR; LEAR is the LASSO-estimated autoregression) gives a Diebold–Mariano (DM) statistic of −0.83 and $p$ = 0.797. Which model goes into production?",
                "options": [
                    "AW-LEAR, because its mean absolute error (MAE) is slightly lower on the test year",
                    "Neither wins significantly: take the simpler one or, better, their average",
                    "AW-ARX, because the negative statistic shows it is significantly better",
                    "Neither: a non-significant test means both models should be discarded"
                ],
                "correctExplanation": "With $p$ = 0.797 the difference is no larger than luck. The lecture recommends the simpler model or their average, which is part of the best ensemble (relative MAE 0.795).",
                "incorrectExplanation": "A small MAE gap on one test year can be luck; that is exactly what the DM test checks. A non-significant result says the models are equivalent, not that both are bad: both beat naive by a wide margin."
            },
            "ro": {
                "title": "Rezultat DM nesemnificativ",
                "text": "ARX mediat pe ferestre (AW-ARX; ARX este modelul autoregresiv cu variabile exogene) față de LEAR mediat pe ferestre (AW-LEAR; LEAR este autoregresia estimată cu LASSO) dă statistica Diebold–Mariano (DM) −0,83 și $p$ = 0,797. Ce model intră în producție?",
                "options": [
                    "AW-LEAR, pentru că eroarea absolută medie (MAE) este puțin mai mică în anul de test",
                    "Niciunul nu este semnificativ mai precis: alegeți modelul mai simplu sau, mai bine, media lor",
                    "AW-ARX, pentru că statistica negativă arată că este semnificativ mai precis",
                    "Niciunul: un test nesemnificativ înseamnă că ambele modele trebuie abandonate"
                ],
                "correctExplanation": "Cu $p$ = 0,797, diferența nu depășește ce poate produce întîmplarea. Cursul recomandă modelul mai simplu sau media lor, care face parte din cel mai bun ansamblu (MAE relativă 0,795).",
                "incorrectExplanation": "O diferență mică de MAE pe un singur an de test se poate datora întîmplării; exact asta verifică testul DM. Un rezultat nesemnificativ arată că modelele sînt echivalente, nu că sînt slabe: ambele sînt mult mai precise decît modelul naiv."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Reading a one-sided p-value",
                "text": "The one-sided Diebold–Mariano (DM) test of AW-LEAR (model A; the LASSO-estimated autoregression, LEAR, averaged across calibration windows) against the ensemble of 4 (model B) gives DM = 2.21 and $p$ = 0.014 on the 365 test days. What does this mean?",
                "options": [
                    "AW-LEAR is significantly more accurate than the ensemble",
                    "The difference is not significant at the 5% level",
                    "The ensemble of 4 is significantly more accurate than AW-LEAR at the 5% level",
                    "The ensemble is more accurate on 98.6% of the test days"
                ],
                "correctExplanation": "The test uses $p=1-\\Phi(\\text{DM})$, and a small $p$ means that model B is more accurate than model A. With $p$ = 0.014, below 0.05, the ensemble is significantly better.",
                "incorrectExplanation": "The p-value is not a share of days. It measures how unlikely a mean daily loss difference this large would be if both models were equally accurate; here that is unlikely, so the ensemble wins."
            },
            "ro": {
                "title": "Interpretarea valorii p unilaterale",
                "text": "Testul Diebold–Mariano (DM) unilateral pentru AW-LEAR (modelul A; autoregresia estimată cu LASSO, LEAR, mediată pe ferestre de calibrare) față de ansamblul de 4 modele (modelul B) dă DM = 2,21 și $p$ = 0,014 pe cele 365 de zile de test. Ce înseamnă acest rezultat?",
                "options": [
                    "AW-LEAR este semnificativ mai precis decît ansamblul",
                    "Diferența nu este semnificativă la pragul de 5%",
                    "Ansamblul de 4 modele este semnificativ mai precis decît AW-LEAR, la pragul de 5%",
                    "Ansamblul este mai precis în 98,6% din zilele de test"
                ],
                "correctExplanation": "Testul folosește $p=1-\\Phi(\\text{DM})$, iar o valoare $p$ mică arată că modelul B este mai precis decît modelul A. Cu $p$ = 0,014, sub 0,05, ansamblul este semnificativ mai precis.",
                "incorrectExplanation": "Valoarea $p$ nu este o proporție de zile. Ea arată cît de puțin probabilă ar fi o diferență medie zilnică atît de mare dacă modelele ar fi la fel de precise; aici este puțin probabilă, deci ansamblul cîștigă."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "One model per hour",
                "text": "The autoregressive model with exogenous variables (ARX) estimated separately for each hour, ARX(728), has a mean absolute error (MAE) of 22.72 EUR/MWh; a single pooled regression with hour-specific intercepts but common slopes reaches 24.54 and is worse in 21 of the 24 hours. Why?",
                "options": [
                    "Different hours react differently to yesterday's price and to the fundamentals, and common slopes force the same reaction",
                    "The pooled model has fewer observations per coefficient than the hourly models",
                    "The pooled model cannot include dummies for Monday, Saturday and Sunday",
                    "The pooled model is estimated on raw prices, while the hourly models use the asinh transformation"
                ],
                "correctExplanation": "The ARX coefficients vary strongly over the day: the weight of yesterday's same hour, for example, is 0.68 at hour 13 and 0.08 at hour 0. Common slopes cannot capture this.",
                "incorrectExplanation": "The pooled model actually has 24 times more observations per coefficient, which is its only advantage. Its weakness is that it forces every hour, from the night to the evening peak, to respond in the same way."
            },
            "ro": {
                "title": "Cîte un model pentru fiecare oră",
                "text": "Modelul autoregresiv cu variabile exogene (ARX) estimat separat pentru fiecare oră, ARX(728), are eroarea absolută medie (MAE) 22,72 EUR/MWh; o singură regresie comună, cu constantă proprie fiecărei ore, dar cu pante comune, ajunge la 24,54 și este mai slabă în 21 din 24 de ore. De ce?",
                "options": [
                    "Orele diferite reacționează diferit la prețul de ieri și la variabilele fundamentale, iar pantele comune impun aceeași reacție",
                    "Modelul comun are mai puține observații pentru fiecare coeficient decît modelele orare",
                    "Modelul comun nu poate include variabile indicator pentru luni, sîmbătă și duminică",
                    "Modelul comun se estimează pe prețuri netransformate, iar modelele orare folosesc transformarea asinh"
                ],
                "correctExplanation": "Coeficienții ARX variază puternic pe parcursul zilei: de exemplu, ponderea prețului aceleiași ore de ieri este 0,68 la ora 13 și 0,08 la ora 0. Pantele comune nu pot surprinde această diferență.",
                "incorrectExplanation": "Modelul comun are de fapt de 24 de ori mai multe observații pentru fiecare coeficient, singurul său avantaj. Slăbiciunea lui este că obligă toate orele, de la noapte pînă la vîrful de seară, să reacționeze la fel."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Night-hour regressors",
                "text": "In the autoregressive model with exogenous variables (ARX), the coefficient of yesterday's same hour is only 0.08 at hour 0. Which regressor carries most weight for the hours just after midnight?",
                "options": [
                    "The load of the same hour on day $d-2$",
                    "The last hour of yesterday, $Y_{d-1,23}$, with a coefficient up to 0.73",
                    "The price of the same hour one week earlier, $Y_{d-7,h}$",
                    "The dummy for Monday"
                ],
                "correctExplanation": "Just after midnight the closest price in time is the one of the previous evening, not the one of the same hour 24 hours earlier, so the coefficient of $Y_{d-1,23}$ reaches up to 0.73 in the night hours.",
                "incorrectExplanation": "Load and wind and solar coefficients stay close to zero in every hour. The night hours lean on the most recent price, the last hour of $d-1$, which is why separate hourly regressions pay off."
            },
            "ro": {
                "title": "Regresorii orelor de noapte",
                "text": "În modelul autoregresiv cu variabile exogene (ARX), coeficientul prețului aceleiași ore de ieri este doar 0,08 la ora 0. Ce regresor are cea mai mare pondere imediat după miezul nopții?",
                "options": [
                    "Consumul din aceeași oră a zilei $d-2$",
                    "Ultima oră a zilei precedente, $Y_{d-1,23}$, cu un coeficient de pînă la 0,73",
                    "Prețul aceleiași ore de acum o săptămînă, $Y_{d-7,h}$",
                    "Variabila indicator pentru luni"
                ],
                "correctExplanation": "Imediat după miezul nopții, prețul cel mai apropiat în timp este cel din seara precedentă, nu cel al aceleiași ore de acum 24 de ore, deci coeficientul lui $Y_{d-1,23}$ ajunge noaptea pînă la 0,73.",
                "incorrectExplanation": "Coeficienții consumului și ai producției eoliene și solare rămîn apropiați de zero la toate orele. Orele de noapte se sprijină pe cel mai recent preț, ultima oră din $d-1$, motiv pentru care regresiile orare separate sînt utile."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Fundamentals lagged two days",
                "text": "For ARX(728) (autoregressive model with exogenous variables, 728-day window) the mean absolute error (MAE) is 22.63 EUR/MWh with prices and calendar only, 22.72 after adding load, wind and solar of $d-2$, and 22.72 after adding also hydro, nuclear, net imports and the carbon price of $d-2$. What should a desk buy first to improve the forecast?",
                "options": [
                    "A deeper neural network fed with the same inputs",
                    "A longer history of the fundamentals observed on $d-2$",
                    "The transmission system operator's (TSO) day-ahead load and renewable forecasts for day $d$",
                    "The realised load of day $d-1$ from a private meter"
                ],
                "correctExplanation": "What happened on $d-2$ is already reflected in the price of $d-1$. The TSO forecasts for day $d$ are published before noon on $d-1$, so they are legal, and this is where most of the possible improvement lies.",
                "incorrectExplanation": "The problem is timing, not model complexity or sample length. The realised load of $d-1$ is not available at 12:00 on $d-1$ and would leak future information."
            },
            "ro": {
                "title": "Variabile fundamentale din d-2",
                "text": "Pentru ARX(728) (modelul autoregresiv cu variabile exogene, fereastră de 728 de zile), eroarea absolută medie (MAE) este 22,63 EUR/MWh numai cu prețuri și calendar, 22,72 după adăugarea consumului și a producției eoliene și solare din $d-2$ și tot 22,72 după adăugarea producției hidro, nucleare, a importului net și a prețului carbonului din $d-2$. Ce ar trebui să cumpere mai întîi un birou de prognoză?",
                "options": [
                    "O rețea neuronală mai profundă, cu aceleași variabile de intrare",
                    "Un istoric mai lung al variabilelor fundamentale observate în ziua $d-2$",
                    "Prognozele operatorului de transport și de sistem (TSO) de consum și de producție regenerabilă pentru ziua $d$",
                    "Consumul realizat în ziua $d-1$, de la un contor privat"
                ],
                "correctExplanation": "Informația din ziua $d-2$ este deja inclusă în prețul zilei $d-1$. Prognozele TSO pentru ziua $d$ apar înainte de prînz în ziua $d-1$, deci pot fi folosite, și tocmai aici se află cea mai mare parte a îmbunătățirii posibile.",
                "incorrectExplanation": "Problema ține de calendar, nu de complexitatea modelului sau de lungimea eșantionului. Consumul realizat în ziua $d-1$ nu se cunoaște la ora 12:00 din ziua $d-1$ și ar introduce informație din viitor."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Asinh and the RMSE",
                "text": "ARX(728) (autoregressive model with exogenous variables) has a mean absolute error (MAE) of 22.86 EUR/MWh on raw prices and 22.72 with the asinh variance-stabilising transformation (VST), but a root mean squared error (RMSE) of 35.85 raw against 36.62 with asinh. What is the best reading?",
                "options": [
                    "The transformation is wrong, because any increase in RMSE shows a worse model",
                    "Raw prices are better in every respect and the transformation should be dropped",
                    "The difference is caused only by the 2 daylight saving time days of the test year",
                    "The transformation gives less weight to spikes when fitting, so it helps typical hours (MAE) and costs a little on spikes (RMSE)"
                ],
                "correctExplanation": "asinh is almost linear near the median and grows only logarithmically far from it, so extreme hours dominate the fit less. Typical hours improve, while the squared-error measure, which punishes spikes, gets slightly worse.",
                "incorrectExplanation": "The two measures answer different questions, so they can move in opposite directions. The 2 daylight saving time days are kept in the evaluation and do not change the ranking."
            },
            "ro": {
                "title": "Transformarea asinh și RMSE",
                "text": "ARX(728) (modelul autoregresiv cu variabile exogene) are eroarea absolută medie (MAE) 22,86 EUR/MWh pe prețuri netransformate și 22,72 cu transformarea de stabilizare a varianței (VST) asinh, dar rădăcina erorii pătratice medii (RMSE) este 35,85 fără transformare și 36,62 cu asinh. Care este interpretarea corectă?",
                "options": [
                    "Transformarea este greșită, pentru că orice creștere a RMSE arată un model mai slab",
                    "Prețurile netransformate sînt mai bune din toate punctele de vedere, iar transformarea trebuie abandonată",
                    "Diferența se datorează numai celor 2 zile cu schimbarea orei din anul de test",
                    "Transformarea dă o pondere mai mică salturilor în estimare, deci ajută orele obișnuite (MAE) și costă puțin la salturi (RMSE)"
                ],
                "correctExplanation": "Funcția asinh este aproape liniară lîngă mediană și crește doar logaritmic departe de ea, deci orele extreme domină mai puțin estimarea. Orele obișnuite se îmbunătățesc, iar măsura pătratică, care penalizează salturile, se înrăutățește puțin.",
                "incorrectExplanation": "Cele două măsuri răspund la întrebări diferite, deci pot evolua în sensuri opuse. Cele 2 zile cu schimbarea orei rămîn în evaluare și nu schimbă clasamentul."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Choosing the LASSO penalty",
                "text": "In the LASSO-estimated autoregression (LEAR; LASSO is the least absolute shrinkage and selection operator), how is the penalty strength $\\lambda_h$ chosen?",
                "options": [
                    "Once, on the test year, to minimise the mean absolute error",
                    "Every day, by the Akaike information criterion (AIC) inside the calibration window",
                    "Fixed at zero, so that all 247 regressors stay in the model",
                    "By random K-fold cross-validation over the whole sample"
                ],
                "correctExplanation": "The penalty is chosen daily by the AIC along the LASSO path inside the window. The lecture insists that it be chosen by an information criterion or on a validation block that ends before the forecast day, never on the test year.",
                "incorrectExplanation": "Tuning on the test year or shuffling days lets the model learn from the future. With $\\lambda=0$ there is no selection at all; the point of LEAR is that the absolute-value penalty sets useless coefficients exactly to zero."
            },
            "ro": {
                "title": "Alegerea penalizării LASSO",
                "text": "În autoregresia estimată cu LASSO (LEAR; LASSO este operatorul de contracție și selecție în normă absolută), cum se alege intensitatea penalizării $\\lambda_h$?",
                "options": [
                    "O singură dată, pe anul de test, pentru a minimiza eroarea absolută medie",
                    "Zilnic, prin criteriul informațional Akaike (AIC), în interiorul ferestrei de calibrare",
                    "Este fixată la zero, astfel încît toți cei 247 de regresori rămîn în model",
                    "Prin validare încrucișată aleatoare (K-fold) pe tot eșantionul"
                ],
                "correctExplanation": "Penalizarea se alege zilnic prin AIC, de-a lungul traiectoriei LASSO, în interiorul ferestrei. Cursul insistă ca ea să fie aleasă printr-un criteriu informațional sau pe un bloc de validare care se încheie înaintea zilei prognozate, niciodată pe anul de test.",
                "incorrectExplanation": "Alegerea pe anul de test sau amestecarea zilelor lasă modelul să învețe din viitor. Cu $\\lambda=0$ nu există nicio selecție; ideea modelului LEAR este că penalizarea în valoare absolută face exact zero coeficienții inutili."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Sparsity of LEAR",
                "text": "The LASSO-estimated autoregression (LEAR) starts from 247 candidates: the 24 prices of $d-1$, $d-2$, $d-3$ and $d-7$ (96), the load and the wind + solar generation of $d-2$, $d-3$ and $d-7$ (144), and 7 weekday dummies. LEAR(728) keeps on average 42 of them. What share is that?",
                "options": [
                    "About 42%",
                    "About 83%",
                    "About 17%",
                    "About 8%"
                ],
                "correctExplanation": "42 / 247 is about 0.17, so LEAR keeps 17% of the candidates on average, between 8 and 121 depending on the hour and the day.",
                "incorrectExplanation": "Divide the number kept by the number of candidates: 42 / 247 is about 17%. The 83% is the share switched off, and 8 is the minimum number of regressors kept in a single fit."
            },
            "ro": {
                "title": "Numărul de regresori păstrați de LEAR",
                "text": "Autoregresia estimată cu LASSO (LEAR) pornește de la 247 de regresori candidați: cele 24 de prețuri din $d-1$, $d-2$, $d-3$ și $d-7$ (96), consumul și producția eoliană și solară din $d-2$, $d-3$ și $d-7$ (144) și 7 indicatori ai zilei săptămînii. LEAR(728) păstrează în medie 42 dintre ei. Ce procent reprezintă?",
                "options": [
                    "Circa 42%",
                    "Circa 83%",
                    "Circa 17%",
                    "Circa 8%"
                ],
                "correctExplanation": "42 / 247 este circa 0,17, deci LEAR păstrează în medie 17% din candidați, între 8 și 121, în funcție de oră și de zi.",
                "incorrectExplanation": "Împărțiți numărul regresorilor păstrați la numărul candidaților: 42 / 247 înseamnă circa 17%. Valoarea de 83% este proporția eliminată, iar 8 este numărul minim de regresori păstrați într-o estimare."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Variables retained by LEAR",
                "text": "Over the 365 daily fits of LEAR(728) (the LASSO-estimated autoregression, 728-day window), which statement matches the selection heat map?",
                "options": [
                    "The load regressors of $d-2$ are kept in most fits, especially in the evening",
                    "The wind + solar regressors are kept more often than yesterday's price of the same hour",
                    "The weekday dummies are almost never kept, because ARX already contains them",
                    "Yesterday's price of the same hour is kept in 79% of the fits and the weekday dummies in 64%, while only 9% of the load regressors survive"
                ],
                "correctExplanation": "The LASSO confirms the ARX (autoregressive model with exogenous variables) experiment: yesterday's same-hour price and the weekday dominate, while only 9% of load and 11% of wind + solar regressors are kept.",
                "incorrectExplanation": "Fundamentals observed two days before delivery carry little information that is not already in the price of $d-1$, so the penalty switches most of them off; real gains need forecasts of the fundamentals for day $d$."
            },
            "ro": {
                "title": "Variabilele păstrate de LEAR",
                "text": "În cele 365 de estimări zilnice ale LEAR(728) (autoregresia estimată cu LASSO, fereastră de 728 de zile), ce afirmație corespunde hărții termice a selecției?",
                "options": [
                    "Regresorii de consum din $d-2$ rămîn în majoritatea estimărilor, mai ales seara",
                    "Regresorii de producție eoliană și solară sînt păstrați mai des decît prețul aceleiași ore de ieri",
                    "Indicatorii zilei săptămînii nu sînt aproape niciodată păstrați, pentru că ARX îi conține deja",
                    "Prețul aceleiași ore de ieri rămîne în 79% din estimări, iar indicatorii zilei săptămînii în 64%, în timp ce din regresorii de consum se păstrează doar 9%"
                ],
                "correctExplanation": "LASSO confirmă experimentul cu ARX (modelul autoregresiv cu variabile exogene): domină prețul aceleiași ore de ieri și ziua săptămînii, iar din regresorii de consum se păstrează doar 9%, din cei de producție eoliană și solară 11%.",
                "incorrectExplanation": "Variabilele fundamentale observate cu două zile înainte de livrare aduc puțină informație care nu se află deja în prețul zilei $d-1$, deci penalizarea le elimină pe cele mai multe; pentru cîștiguri reale sînt necesare prognoze ale lor pentru ziua $d$."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Averaging calibration windows",
                "text": "The autoregressive model with exogenous variables (ARX) has a mean absolute error (MAE) of 24.44 EUR/MWh with a 56-day window and 22.68 with the best single window, 714 days. Averaging across calibration windows (AW-ARX) gives 22.30. What is the managerial lesson?",
                "options": [
                    "Averaging short and long windows beats even the best window chosen with hindsight, without having to know it in advance",
                    "Always use the longest window available, since long windows are the most stable",
                    "Use the 56-day window, because short windows adapt quickest to regime changes",
                    "Re-select every year the window with the lowest test-year MAE"
                ],
                "correctExplanation": "Short windows adapt and long windows are stable; the average gets both. AW-ARX at 22.30 is below every single window, and the best window is not known in advance: on another year a short window might win.",
                "incorrectExplanation": "Choosing the window on the test year is hindsight. The averaged forecast removes the need to choose and still beats each single window, which is why both short and long windows stay in the average."
            },
            "ro": {
                "title": "Medierea ferestrelor de calibrare",
                "text": "Modelul autoregresiv cu variabile exogene (ARX) are eroarea absolută medie (MAE) 24,44 EUR/MWh cu o fereastră de 56 de zile și 22,68 cu cea mai bună fereastră individuală, de 714 zile. Medierea pe ferestre de calibrare (AW-ARX) dă 22,30. Care este concluzia pentru un manager?",
                "options": [
                    "Media ferestrelor scurte și lungi este mai precisă chiar decît cea mai bună fereastră aleasă retrospectiv, fără ca aceasta să trebuiască știută dinainte",
                    "Folosiți întotdeauna cea mai lungă fereastră disponibilă, pentru că ferestrele lungi sînt cele mai stabile",
                    "Folosiți fereastra de 56 de zile, pentru că ferestrele scurte se adaptează cel mai repede la schimbările de regim",
                    "Alegeți în fiecare an fereastra cu cea mai mică MAE pe anul de test"
                ],
                "correctExplanation": "Ferestrele scurte se adaptează, cele lungi sînt stabile; media le are pe amîndouă. AW-ARX, cu 22,30, este sub orice fereastră individuală, iar cea mai bună fereastră nu se cunoaște dinainte: în alt an ar putea cîștiga o fereastră scurtă.",
                "incorrectExplanation": "Alegerea ferestrei pe anul de test înseamnă a folosi informație retrospectivă. Prognoza mediată elimină nevoia de a alege și este totuși mai precisă decît fiecare fereastră, motiv pentru care ferestrele scurte și lungi rămîn în medie."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Gain of the ensemble of 4",
                "text": "On the Romanian test year, the Lasso-Estimated AutoRegressive (LEAR) model averaged across calibration windows (AW-LEAR) has a mean absolute error (MAE) of 22.53 EUR/MWh, and the equal-weight ensemble of 4 models 22.13. The Diebold–Mariano (DM) test of AW-LEAR against the ensemble gives $p$ = 0.014. What do you conclude?",
                "options": [
                    "The ensemble cuts the MAE by about 18%, a large and significant gain",
                    "The ensemble cuts the MAE by about 1.8%, a small but significant gain at the 5% level",
                    "The ensemble cuts the MAE by about 1.8%, but the gain is not significant",
                    "The two models are equivalent, since 0.40 EUR/MWh is within rounding"
                ],
                "correctExplanation": "$(22.53-22.13)/22.53\\approx 1.8\\%$, and $p$ = 0.014 is below 0.05. The gain comes from the weaker members, the gradient boosting machine and the multilayer perceptron, whose errors differ from those of the linear models: a lower average error correlation $\\bar\\rho$ lowers the variance of the averaged error.",
                "incorrectExplanation": "The relative gain is 0.40 out of 22.53, under 2%, not 18%; yet the DM test, which compares the daily error differences with their own noise, rejects equal accuracy, so a small gain can still be significant."
            },
            "ro": {
                "title": "Cîștigul ansamblului de 4 modele",
                "text": "Pe anul de test din România, modelul LEAR (Lasso-Estimated AutoRegressive) mediat pe ferestre de calibrare (AW-LEAR) are o eroare absolută medie (MAE) de 22,53 EUR/MWh, iar ansamblul de 4 modele cu ponderi egale 22,13. Testul Diebold–Mariano (DM) pentru AW-LEAR față de ansamblu dă $p$ = 0,014. Ce concluzie trageți?",
                "options": [
                    "Ansamblul reduce MAE cu circa 18%, un cîștig mare și semnificativ",
                    "Ansamblul reduce MAE cu circa 1,8%, un cîștig mic, dar semnificativ la pragul de 5%",
                    "Ansamblul reduce MAE cu circa 1,8%, dar cîștigul nu este semnificativ",
                    "Cele două modele sînt echivalente, pentru că 0,40 EUR/MWh ține de rotunjire"
                ],
                "correctExplanation": "$(22{,}53-22{,}13)/22{,}53\\approx 1{,}8\\%$, iar $p$ = 0,014 este sub 0,05. Cîștigul vine de la membrii mai slabi, modelul gradient boosting și perceptronul multistrat, ale căror erori diferă de cele ale modelelor liniare: o corelație medie mai mică a erorilor, $\\bar\\rho$, reduce varianța erorii mediate.",
                "incorrectExplanation": "Cîștigul relativ este 0,40 din 22,53, sub 2%, nu 18%; totuși testul DM, care compară diferențele zilnice dintre erori cu propriul lor zgomot, respinge egalitatea preciziei, deci și un cîștig mic poate fi semnificativ."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Contribution of weaker ensemble members",
                "text": "Alone, the gradient boosting machine (GBM) and the multilayer perceptron (MLP) beat AW-LEAR (LEAR, the LASSO-estimated autoregression, averaged across calibration windows) in 0 of the 24 hours. Yet the equal-weight ensemble of 4 that contains them beats AW-LEAR in 15 of the 24 hours. Why?",
                "options": [
                    "The ensemble gives GBM and MLP larger weights in the evening hours",
                    "The ensemble weights are estimated on the test year",
                    "Their errors differ from those of the linear models, so the errors partly cancel in the average",
                    "Averaging removes the bias of each linear model, whatever the other members are"
                ],
                "correctExplanation": "With equal weights, the gain depends on how little the members' errors are correlated. GBM and MLP make different mistakes from the linear expert models, so they improve the average even though they lose alone.",
                "incorrectExplanation": "The weights are equal and need no estimation, which makes them robust. A weaker model with different errors still lowers the error of the average; this is the practical meaning of the ensemble variance formula."
            },
            "ro": {
                "title": "Contribuția membrilor mai slabi ai ansamblului",
                "text": "Luate separat, modelul gradient boosting (GBM) și perceptronul multistrat (MLP) sînt mai precise decît AW-LEAR (LEAR, autoregresia estimată cu LASSO, mediată pe ferestre de calibrare) în 0 din 24 de ore. Totuși, ansamblul de 4 modele cu ponderi egale care le include este mai precis decît AW-LEAR în 15 din 24 de ore. De ce?",
                "options": [
                    "Ansamblul dă ponderi mai mari modelelor GBM și MLP la orele de seară",
                    "Ponderile ansamblului se estimează pe anul de test",
                    "Erorile lor diferă de cele ale modelelor liniare, deci se compensează parțial în medie",
                    "Medierea elimină eroarea sistematică a fiecărui model liniar, oricare ar fi ceilalți membri"
                ],
                "correctExplanation": "Cu ponderi egale, cîștigul depinde de cît de puțin corelate sînt erorile membrilor. GBM și MLP greșesc altfel decît modelele expert liniare, deci îmbunătățesc media, deși luate separat sînt mai slabe.",
                "incorrectExplanation": "Ponderile sînt egale și nu se estimează, ceea ce le face robuste. Un model mai slab, dar cu erori diferite, reduce totuși eroarea mediei; acesta este sensul practic al formulei varianței ansamblului."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Gradient boosting set-up",
                "text": "How is the gradient boosting machine (GBM) of the lecture built and updated?",
                "options": [
                    "One model for all hours with the hour as a feature, 500 small trees with learning rate 0.05, refitted at the start of each test month on all earlier days",
                    "24 separate models, one per hour, re-estimated daily on a 728-day window",
                    "One model per hour whose trees are selected every day by the Akaike information criterion",
                    "One model trained once on the whole sample, including the test year, to use all the data"
                ],
                "correctExplanation": "The GBM adds 500 small trees, each fitted to the residuals of the previous ones and shrunk by $\\nu$ = 0.05; it uses 20 features available at 12:00 on $d-1$ and an expanding window refitted 12 times, once per test month.",
                "incorrectExplanation": "Training on the test year would leak future information. The GBM is a single pooled model refitted monthly; over the year its mean absolute error is 24.05 EUR/MWh, but in the stress week it is the best single model with 34.35."
            },
            "ro": {
                "title": "Construcția modelului gradient boosting",
                "text": "Cum este construit și actualizat modelul gradient boosting (GBM) din curs?",
                "options": [
                    "Un singur model pentru toate orele, cu ora ca variabilă, 500 de arbori mici cu rata de învățare 0,05, reestimat la începutul fiecărei luni de test pe toate zilele anterioare",
                    "24 de modele separate, cîte unul pentru fiecare oră, reestimate zilnic pe o fereastră de 728 de zile",
                    "Cîte un model pentru fiecare oră, cu arborii aleși zilnic prin criteriul informațional Akaike",
                    "Un singur model, estimat o dată pe tot eșantionul, inclusiv pe anul de test, pentru a folosi toate datele"
                ],
                "correctExplanation": "GBM adună 500 de arbori mici, fiecare estimat pe reziduurile celor anteriori și micșorat cu $\\nu$ = 0,05; folosește 20 de variabile cunoscute la 12:00 în ziua $d-1$ și o fereastră extinsă, reestimată de 12 ori, o dată pentru fiecare lună de test.",
                "incorrectExplanation": "Estimarea pe anul de test ar introduce informație din viitor. GBM este un singur model comun, reestimat lunar; pe ansamblul anului are eroarea absolută medie 24,05 EUR/MWh, dar în săptămîna de criză este cel mai bun model individual, cu 34,35."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Training a neural network without look-ahead",
                "text": "Which choice respects time-series discipline when training the multilayer perceptron (MLP) of the lecture?",
                "options": [
                    "Choosing the number of epochs on a random 15% of the training days",
                    "Choosing the number of epochs on the last 15% of the training days, in time order, and fitting the input scaling on the training days only",
                    "Fitting the input scaling on the whole sample, so that the test year is on the same scale",
                    "Keeping the random seed that gives the lowest error on the test year"
                ],
                "correctExplanation": "The lecture picks the epochs on the last 15% of the training days in time order (median 20), averages 4 random seeds, refits monthly and fits the scaling on training days only. The result is a mean absolute error of 25.54 EUR/MWh and a relative error of 0.918 against naive.",
                "incorrectExplanation": "Random validation days, full-sample scaling and seed selection on the test year all let future information into the model. A small untuned network still does not beat the LASSO-estimated autoregression (LEAR), but its backtest is honest."
            },
            "ro": {
                "title": "Antrenarea corectă a unei rețele neuronale",
                "text": "Ce alegere respectă disciplina seriilor de timp la antrenarea perceptronului multistrat (MLP) din curs?",
                "options": [
                    "Alegerea numărului de epoci pe 15% din zilele de antrenare, alese aleator",
                    "Alegerea numărului de epoci pe ultimele 15% din zilele de antrenare, în ordine cronologică, și estimarea standardizării numai pe zilele de antrenare",
                    "Estimarea standardizării pe tot eșantionul, astfel încît anul de test să fie pe aceeași scară",
                    "Păstrarea inițializării aleatoare care dă cea mai mică eroare pe anul de test"
                ],
                "correctExplanation": "Cursul alege numărul de epoci pe ultimele 15% din zilele de antrenare, în ordine cronologică (mediana: 20), face media a 4 inițializări aleatoare, reestimează rețeaua lunar și estimează standardizarea numai pe zilele de antrenare. Rezultatul: eroarea absolută medie 25,54 EUR/MWh și eroarea relativă 0,918 față de modelul naiv.",
                "incorrectExplanation": "Zilele de validare alese aleator, standardizarea pe tot eșantionul și alegerea inițializării pe anul de test introduc toate informație din viitor. O rețea mică, neoptimizată, nu depășește autoregresia estimată cu LASSO (LEAR), dar testarea ei este corectă."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Load versus price forecasting",
                "text": "In case study C2 on Romanian hourly load, the mean absolute percentage error (MAPE) is 4.09% for gradient boosting, 4.85% for a linear regression and 10.17% for the naive forecast. For prices, machine learning alone stays behind linear models. Why the contrast?",
                "options": [
                    "Load data cover a much longer history than price data",
                    "MAPE systematically favours nonlinear models over linear ones",
                    "Load is smooth and never near zero, so MAPE is meaningful and patterns are regular; prices jump and turn negative",
                    "Load forecasts may use the realised load of day $d$"
                ],
                "correctExplanation": "Smooth, strictly positive series give nonlinear models regular patterns to learn. Prices have spikes and negative values; there, a well-built linear model is hard to beat.",
                "incorrectExplanation": "C2 applies the same gate-closure rule as the lecture, with load metered up to $d-2$, so no future data are used. The difference comes from the nature of the two series."
            },
            "ro": {
                "title": "Prognoza consumului și prognoza prețului",
                "text": "În studiul de caz C2 despre consumul orar din România, eroarea procentuală absolută medie (MAPE) este 4,09% pentru gradient boosting, 4,85% pentru o regresie liniară și 10,17% pentru modelul naiv. Pentru prețuri, învățarea automată luată separat rămîne în urma modelelor liniare. De ce această diferență?",
                "options": [
                    "Datele de consum acoperă un istoric mult mai lung decît datele de preț",
                    "MAPE favorizează sistematic modelele neliniare față de cele liniare",
                    "Consumul variază lin și nu se apropie de zero, deci MAPE are sens și tiparele sînt regulate; prețurile au salturi și devin negative",
                    "Prognozele de consum pot folosi consumul realizat în ziua $d$"
                ],
                "correctExplanation": "Seriile netede și strict pozitive oferă modelelor neliniare regularități de învățat. Prețurile au salturi și valori negative; aici, un model liniar bine construit este greu de depășit.",
                "incorrectExplanation": "C2 aplică aceeași regulă ca acest curs, cu consumul măsurat pînă în ziua $d-2$, deci nu folosește date din viitor. Diferența vine din natura celor două serii."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Hour with the largest errors",
                "text": "Looking at the mean absolute error (MAE) by hour on the test year, where are AW-LEAR (LEAR, the LASSO-estimated autoregression, averaged across calibration windows) errors largest?",
                "options": [
                    "At 3 h Central European Time (CET), in the night, when liquidity is lowest",
                    "At 13 h CET, at the solar peak, when prices can turn negative",
                    "At 0 h CET, just after midnight, far from yesterday's same hour",
                    "At 19 h CET, the evening ramp, with an MAE of 34.52 EUR/MWh"
                ],
                "correctExplanation": "At 19 h solar output disappears while demand is still high, so the price ramps steeply and is hard to forecast. Night and early-morning hours are much easier.",
                "incorrectExplanation": "The evening ramp is where the money is lost; the lecture advises putting the best analyst on the evening hours and hedging them."
            },
            "ro": {
                "title": "Ora cu cele mai mari erori",
                "text": "Privind eroarea absolută medie (MAE) pe ore în anul de test, unde sînt cele mai mari erorile AW-LEAR (LEAR, autoregresia estimată cu LASSO, mediată pe ferestre de calibrare)?",
                "options": [
                    "La ora 3, ora Europei Centrale (CET), noaptea, cînd lichiditatea este cea mai mică",
                    "La ora 13 CET, la vîrful producției solare, cînd prețurile pot deveni negative",
                    "La ora 0 CET, imediat după miezul nopții, departe de aceeași oră de ieri",
                    "La ora 19 CET, cînd prețul urcă abrupt seara, cu MAE 34,52 EUR/MWh"
                ],
                "correctExplanation": "La ora 19, producția solară dispare, iar consumul este încă ridicat, deci prețul urcă abrupt și este greu de prognozat. Orele de noapte și cele de dimineață devreme sînt mult mai ușor de prognozat.",
                "incorrectExplanation": "Urcarea de seară este momentul în care se pierd cei mai mulți bani; cursul recomandă alocarea celui mai bun analist orelor de seară și acoperirea riscului acestor ore."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Forecast type for a battery",
                "text": "On the Romanian test year the forecast errors at 12 h and 13 h correlate at 0.96, those at 3 h and 19 h at only 0.13. A battery buys in one hour and sells in another. Which kind of forecast does it need?",
                "options": [
                    "Path forecasts, joint scenarios for all 24 hours, because profit depends on the joint behaviour of the two prices",
                    "A point forecast per hour, because only the expected spread matters",
                    "24 separate quantile forecasts, one per hour",
                    "A forecast of the daily base price"
                ],
                "correctExplanation": "Errors of different hours are not independent, and separate quantiles cannot describe that dependence; paths can. The supplier buying a block needs the point forecast, the risk manager quantiles, the battery paths.",
                "incorrectExplanation": "The battery's result depends on the price difference between two hours, so the dependence between hourly errors matters. Only joint scenarios across the day capture it."
            },
            "ro": {
                "title": "Tipul de prognoză pentru o baterie",
                "text": "Pe datele din România, corelația erorilor de prognoză între orele 12 și 13 este 0,96, iar între orele 3 și 19 doar 0,13. O baterie cumpără energie într-o oră și o vinde în alta. De ce tip de prognoză are nevoie?",
                "options": [
                    "De traiectorii, adică scenarii comune pentru toate cele 24 de ore, pentru că profitul depinde de evoluția comună a celor două prețuri",
                    "De o prognoză punctuală pentru fiecare oră, pentru că contează doar diferența așteptată",
                    "De 24 de prognoze cuantilice separate, cîte una pentru fiecare oră",
                    "De o prognoză a prețului zilnic de bază"
                ],
                "correctExplanation": "Erorile orelor nu sînt independente, iar cuantilele separate nu pot descrie această dependență; traiectoriile pot. Furnizorul care cumpără un bloc de ore folosește prognoza punctuală, managerul de risc cuantilele, iar bateria traiectoriile.",
                "incorrectExplanation": "Rezultatul bateriei depinde de diferența de preț dintre două ore, deci contează dependența dintre erorile orare. Numai scenariile comune pentru întreaga zi o surprind."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "From pinball score to CRPS",
                "text": "On the test year, the pinball score averaged over the 99 quantiles is 8.33 for quantile regression averaging (QRA), 8.47 for conformal prediction (CP) and 8.41 for historical simulation (HS). The continuous ranked probability score (CRPS) is approximately 2 × this score. What is the approximate CRPS of QRA, and how does QRA rank?",
                "options": [
                    "About 4.2, best of the three",
                    "About 16.7, best of the three",
                    "About 16.9, best of the three",
                    "About 16.7, worst of the three"
                ],
                "correctExplanation": "$2\\times 8.33\\approx 16.7$. Both scores are losses, so lower is better, and QRA has the lowest of the three; the differences are small, and all three intervals still cover less than 90%.",
                "incorrectExplanation": "The CRPS is twice the average pinball score, not half of it; 16.9 is the value of CP, and since a lower score means a better forecast, QRA ranks first."
            },
            "ro": {
                "title": "De la scorul pinball la CRPS",
                "text": "Pe anul de test, scorul pinball mediat pe cele 99 de cuantile este 8,33 pentru media regresiilor cuantilice (QRA), 8,47 pentru predicția conformală (CP) și 8,41 pentru simularea istorică (HS). Scorul de probabilitate ordonat continuu (CRPS) este aproximativ 2 × acest scor. Cît este, aproximativ, CRPS pentru QRA și pe ce loc se situează QRA?",
                "options": [
                    "Circa 4,2, cea mai bună dintre cele trei",
                    "Circa 16,7, cea mai bună dintre cele trei",
                    "Circa 16,9, cea mai bună dintre cele trei",
                    "Circa 16,7, cea mai slabă dintre cele trei"
                ],
                "correctExplanation": "$2\\times 8{,}33\\approx 16{,}7$. Ambele scoruri sînt pierderi, deci o valoare mai mică este mai bună, iar QRA are cea mai mică valoare dintre cele trei; diferențele sînt mici, iar toate cele trei intervale acoperă încă sub 90%.",
                "incorrectExplanation": "CRPS este dublul scorului pinball mediu, nu jumătatea lui; 16,9 este valoarea pentru CP, iar cum un scor mai mic înseamnă o prognoză mai bună, QRA se situează pe primul loc."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Coverage of the 90% band",
                "text": "The 90% interval from quantile regression averaging (QRA) covers 85.7% of the test-year prices, conformal prediction (CP) 87.0% and historical simulation (HS) 85.8%. The Kupiec statistic is 162.9 for QRA against a 5% critical value of 3.84. What follows for a risk manager?",
                "options": [
                    "The intervals are too wide, so the open position is overhedged",
                    "QRA is well calibrated, since it has the lowest average pinball score",
                    "The tails are too narrow: the band understates risk and should be widened before it is used for collateral",
                    "The Kupiec test does not reject correct coverage, so the bands can be used as they are"
                ],
                "correctExplanation": "All three methods cover less than 90% and the Kupiec test rejects correct coverage. Too many prices fall below the low quantiles and above the high ones, so the tails must be widened (Lecture 4).",
                "incorrectExplanation": "A lower pinball score (8.33 for QRA) does not guarantee calibration. A statistic of 162.9, far above 3.84, rejects correct coverage; a 90% band holding about 86% of prices understates risk."
            },
            "ro": {
                "title": "Acoperirea intervalului de 90%",
                "text": "Intervalul de 90% obținut prin medierea prin regresie cuantilică (QRA) conține 85,7% din prețurile anului de test, cel obținut prin predicția conformală (CP) 87,0%, iar cel obținut prin simularea istorică (HS) 85,8%. Statistica Kupiec este 162,9 pentru QRA, față de valoarea critică de 3,84 la 5%. Ce rezultă pentru un manager de risc?",
                "options": [
                    "Intervalele sînt prea largi, deci poziția deschisă este acoperită excesiv",
                    "QRA este bine calibrată, pentru că are cel mai mic scor pinball mediu",
                    "Cozile sînt prea înguste: banda subestimează riscul și trebuie lărgită înainte de a fi folosită pentru calculul garanțiilor",
                    "Testul Kupiec nu respinge acoperirea corectă, deci intervalele pot fi folosite ca atare"
                ],
                "correctExplanation": "Toate cele trei metode acoperă mai puțin de 90%, iar testul Kupiec respinge acoperirea corectă. Prea multe prețuri cad sub cuantilele mici și peste cele mari, deci cozile trebuie lărgite (cursul 4).",
                "incorrectExplanation": "Un scor pinball mai mic (8,33 pentru QRA) nu garantează calibrarea. O statistică de 162,9, mult peste 3,84, respinge acoperirea corectă; o bandă de 90% care conține circa 86% din prețuri subestimează riscul."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "A RO–HU spread trade",
                "text": "The daily prices of Romania (RO) and Hungary (HU) are cointegrated, and a shock to their spread halves in 0.8 days. Today Romania is 40 EUR/MWh above Hungary. What do you expect?",
                "options": [
                    "The gap should shrink by about half, to around 20 EUR/MWh, within about a day, unless the border stays congested",
                    "The gap closes completely within 0.8 days",
                    "The gap persists for several months, because the two prices are nonstationary",
                    "The gap widens, because cointegrated spreads follow a random walk"
                ],
                "correctExplanation": "A half-life of 0.8 days means the spread is expected to halve in less than a day. It is a signal for cross-border trading, not a guarantee: when the interconnection is congested, prices can stay apart.",
                "incorrectExplanation": "The half-life is the time to close half of the gap, not all of it. Cointegration means the spread is stationary and keeps returning, which is the opposite of a random walk."
            },
            "ro": {
                "title": "O poziție pe diferența RO–HU",
                "text": "Prețurile zilnice din România (RO) și Ungaria (HU) sînt cointegrate, iar un șoc asupra diferenței dintre ele se înjumătățește în 0,8 zile. Astăzi prețul din România este cu 40 EUR/MWh mai mare decît cel din Ungaria. La ce vă așteptați?",
                "options": [
                    "Diferența ar trebui să se reducă la circa jumătate, în jur de 20 EUR/MWh, în aproximativ o zi, dacă interconexiunea nu rămîne congestionată",
                    "Diferența se închide complet în 0,8 zile",
                    "Diferența persistă cîteva luni, pentru că cele două prețuri sînt nestaționare",
                    "Diferența crește, pentru că diferențele cointegrate urmează un mers aleator"
                ],
                "correctExplanation": "Un timp de înjumătățire de 0,8 zile înseamnă că diferența se reduce la jumătate în mai puțin de o zi. Este un semnal pentru tranzacțiile transfrontaliere, nu o garanție: cînd interconexiunea este congestionată, prețurile pot rămîne diferite.",
                "incorrectExplanation": "Timpul de înjumătățire este timpul în care se închide jumătate din diferență, nu toată. Cointegrarea înseamnă că diferența este staționară și revine mereu, adică opusul unui mers aleator."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Implied gas plant efficiency",
                "text": "On monthly data from 2015-01 to 2026-10, the Romanian power price is cointegrated with the Title Transfer Facility (TTF) gas price, with long-run slope $\\hat\\beta$ = 1.95 (both in EUR/MWh). Ignoring carbon costs, which gas plant efficiency does this slope imply?",
                "options": [
                    "About 195%",
                    "About 95%",
                    "About 51%",
                    "About 35%"
                ],
                "correctExplanation": "One MWh of electricity needs $1/\\eta$ MWh of gas, so a slope of 1.95 implies $\\eta\\approx1/1.95\\approx0.51$: the price behaves as if a gas plant of about 51% efficiency set it.",
                "incorrectExplanation": "Efficiency is the inverse of the slope, not the slope itself or one minus its fractional part. A slope near 2 means about two MWh of gas per MWh of power."
            },
            "ro": {
                "title": "Randamentul implicit al centralei pe gaze",
                "text": "Pe date lunare din perioada 2015-01 – 2026-10, prețul energiei electrice din România este cointegrat cu prețul gazelor la hubul Title Transfer Facility (TTF), cu panta pe termen lung $\\hat\\beta$ = 1,95 (ambele în EUR/MWh). Ignorînd costul carbonului, ce randament al unei centrale pe gaze rezultă din această pantă?",
                "options": [
                    "Circa 195%",
                    "Circa 95%",
                    "Circa 51%",
                    "Circa 35%"
                ],
                "correctExplanation": "Un MWh de energie electrică necesită $1/\\eta$ MWh de gaze, deci o pantă de 1,95 înseamnă $\\eta\\approx1/1{,}95\\approx0{,}51$: prețul se comportă ca și cum ar fi stabilit de o centrală pe gaze cu randament de circa 51%.",
                "incorrectExplanation": "Randamentul este inversul pantei, nu panta însăși și nici unu minus partea ei fracționară. O pantă de aproape 2 înseamnă circa doi MWh de gaze pentru un MWh de energie electrică."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "A dry hydro month",
                "text": "In the monthly error-correction model (ECM), the effect of hydro output above its calendar-month mean is $\\hat\\delta$ = −12.80 EUR/MWh per terawatt-hour (TWh), and the speed of return is $\\hat\\alpha$ = −0.452. A month has 1 TWh less hydro than usual. What should a hydro producer expect?",
                "options": [
                    "Prices about 12.80 EUR/MWh below the level implied by gas",
                    "No effect, because hydro minus its monthly mean is stationary",
                    "A permanent rise of 12.80 EUR/MWh in the long-run price level",
                    "Prices pushed about 12.80 EUR/MWh above the gas-implied level, with the gap closing with a half-life of about 1.2 months"
                ],
                "correctExplanation": "Less hydro means a positive deviation from the gas-implied level; the error-correction term then pulls the price back, with a half-life of 1.2 months. A dry year is a premium over gas, not a new price level.",
                "incorrectExplanation": "The sign of $\\hat\\delta$ is negative, so less hydro raises the price. Stationarity of the hydro deviation means its effect is temporary, not that it is zero; the long-run level is set by gas."
            },
            "ro": {
                "title": "O lună secetoasă",
                "text": "În modelul lunar cu corecția erorii (ECM), efectul producției hidro peste media lunii calendaristice este $\\hat\\delta$ = −12,80 EUR/MWh pentru fiecare terawatt-oră (TWh), iar viteza de revenire este $\\hat\\alpha$ = −0,452. Într-o lună, producția hidro este cu 1 TWh sub cea obișnuită. La ce se poate aștepta un producător hidro?",
                "options": [
                    "La prețuri cu circa 12,80 EUR/MWh sub nivelul dat de gaze",
                    "La niciun efect, pentru că producția hidro minus media lunii este staționară",
                    "La o creștere permanentă cu 12,80 EUR/MWh a nivelului de echilibru al prețului",
                    "La prețuri cu circa 12,80 EUR/MWh peste nivelul dat de gaze, abaterea închizîndu-se cu un timp de înjumătățire de circa 1,2 luni"
                ],
                "correctExplanation": "Mai puțină producție hidro înseamnă o abatere pozitivă de la nivelul dat de gaze; termenul de corecție a erorii readuce apoi prețul spre echilibru, cu un timp de înjumătățire de 1,2 luni. Un an secetos este o primă peste nivelul dat de gaze, nu un nou nivel al prețului.",
                "incorrectExplanation": "Semnul lui $\\hat\\delta$ este negativ, deci mai puțină producție hidro crește prețul. Staționaritatea abaterii hidro înseamnă că efectul ei este temporar, nu că este nul; nivelul de echilibru este dat de gaze."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Accuracy month by month",
                "text": "Case study (a) follows the monthly mean absolute error (MAE) of AW-LEAR (LEAR, the LASSO-estimated autoregression, averaged across calibration windows) over the test year. Which statement is correct?",
                "options": [
                    "AW-LEAR beats naive in all 12 months, but its MAE ranges from 12.84 EUR/MWh in December 2025 to 34.88 EUR/MWh in October 2026",
                    "AW-LEAR beats naive only in the winter months, when prices are high",
                    "The MAE of AW-LEAR is stable around 22.53 EUR/MWh in every month",
                    "October 2026 is the easiest month, because prices were high and regular"
                ],
                "correctExplanation": "The gain over naive is not an artefact of one good period, yet the level of the error varies a lot. A good annual average can hide weak periods, so accuracy should be reported by month.",
                "incorrectExplanation": "22.53 EUR/MWh is the annual MAE, an average of very different months. October 2026, with the stress week, is the hardest month of the test year."
            },
            "ro": {
                "title": "Acuratețea lună de lună",
                "text": "Studiul de caz (a) urmărește eroarea absolută medie (MAE) lunară a AW-LEAR (LEAR, autoregresia estimată cu LASSO, mediată pe ferestre de calibrare) în anul de test. Ce afirmație este corectă?",
                "options": [
                    "AW-LEAR este mai precis decît modelul naiv în toate cele 12 luni, dar MAE variază între 12,84 EUR/MWh în decembrie 2025 și 34,88 EUR/MWh în octombrie 2026",
                    "AW-LEAR este mai precis decît modelul naiv numai în lunile de iarnă, cînd prețurile sînt mari",
                    "MAE pentru AW-LEAR este stabilă, în jur de 22,53 EUR/MWh, în fiecare lună",
                    "Octombrie 2026 este luna cea mai ușoară, pentru că prețurile au fost mari și regulate"
                ],
                "correctExplanation": "Cîștigul față de modelul naiv nu se datorează unei singure perioade favorabile, dar nivelul erorii variază mult. O medie anuală bună poate ascunde perioade slabe, deci acuratețea trebuie raportată lună de lună.",
                "incorrectExplanation": "22,53 EUR/MWh este MAE anuală, o medie a unor luni foarte diferite. Octombrie 2026, cu săptămîna de criză, este luna cea mai dificilă din anul de test."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "The stress week",
                "text": "In the week of 19–25 Oct 2026 the mean price was 258.59 EUR/MWh and the peak 412.35 EUR/MWh. The mean absolute error (MAE) was 40.19 for naive, 36.54 for AW-LEAR (LEAR, the LASSO-estimated autoregression, averaged across windows) and 34.35 for the gradient boosting machine (GBM). What did all models have in common?",
                "options": [
                    "They anticipated the jump in level one day in advance",
                    "They lagged a sudden jump in the price level by about a day, because they rely on yesterday's prices",
                    "They were all worse than the naive benchmark",
                    "Their errors were concentrated in the night hours"
                ],
                "correctExplanation": "The forecasts catch up only once the new level has appeared in the data of $d-1$. The models still beat naive, and GBM, behind AW-LEAR over the year, was the best single model in this week.",
                "incorrectExplanation": "Every model beat naive in this week, but none could foresee the jump: with yesterday's prices as main input, a level shift shows up in the forecast one day late. The practical answer is to hedge the evening hours."
            },
            "ro": {
                "title": "Săptămîna de criză",
                "text": "În săptămîna 19–25 octombrie 2026, prețul mediu a fost 258,59 EUR/MWh, iar maximul 412,35 EUR/MWh. Eroarea absolută medie (MAE) a fost 40,19 pentru modelul naiv, 36,54 pentru AW-LEAR (LEAR, autoregresia estimată cu LASSO, mediată pe ferestre) și 34,35 pentru gradient boosting (GBM). Ce au avut în comun toate modelele?",
                "options": [
                    "Au anticipat saltul de nivel cu o zi înainte",
                    "Au reacționat la saltul brusc al nivelului prețului cu aproximativ o zi întîrziere, pentru că se bazează pe prețurile de ieri",
                    "Au fost toate mai slabe decît modelul naiv",
                    "Erorile lor s-au concentrat în orele de noapte"
                ],
                "correctExplanation": "Prognozele ajung din urmă noul nivel abia după ce acesta apare în datele zilei $d-1$. Modelele rămîn mai precise decît cel naiv, iar GBM, mai slab decît AW-LEAR pe întregul an, a fost cel mai bun model individual în această săptămînă.",
                "incorrectExplanation": "Toate modelele au fost mai precise decît cel naiv în această săptămînă, dar niciunul nu a putut prevedea saltul: cu prețurile de ieri ca principală variabilă, o schimbare de nivel apare în prognoză cu o zi întîrziere. Răspunsul practic este acoperirea riscului orelor de seară."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Quarter-hour shape gain",
                "text": "Since 1 October 2025 the day-ahead market time unit (MTU) is 15 minutes. On the 363 test days without daylight saving time changes, the quarter-hour mean absolute error (MAE) is 26.02 EUR/MWh when the hourly forecast is kept flat and 24.53 EUR/MWh when the intra-hour shape of the 28 previous days is added. By roughly how much does the shape reduce the error?",
                "options": [
                    "About 1.5%",
                    "About 24.5%",
                    "About 5.7%",
                    "About 9.4%"
                ],
                "correctExplanation": "$(26.02-24.53)/26.02=1.49/26.02\\approx5.7\\%$. A simple profile estimated only from past days already recovers part of the structure within the hour.",
                "incorrectExplanation": "The absolute gain is 1.49 EUR/MWh; to express it in percent, divide by the flat-hour MAE of 26.02. A battery bids per quarter-hour, so it should receive the shaped forecast."
            },
            "ro": {
                "title": "Cîștigul profilului intraorar",
                "text": "Din 1 octombrie 2025, intervalul de tranzacționare (MTU) al licitației pe Piața pentru Ziua Următoare (PZU) are 15 minute. Pe cele 363 de zile de test fără schimbarea orei, eroarea absolută medie (MAE) pe sfert de oră este 26,02 EUR/MWh cînd prognoza orară este constantă în interiorul orei și 24,53 EUR/MWh cînd se adaugă profilul intraorar din ultimele 28 de zile. Cu cît reduce profilul eroarea, aproximativ?",
                "options": [
                    "Cu circa 1,5%",
                    "Cu circa 24,5%",
                    "Cu circa 5,7%",
                    "Cu circa 9,4%"
                ],
                "correctExplanation": "$(26{,}02-24{,}53)/26{,}02=1{,}49/26{,}02\\approx5{,}7\\%$. Un profil simplu, estimat numai din zilele trecute, recuperează deja o parte din structura din interiorul orei.",
                "incorrectExplanation": "Cîștigul absolut este 1,49 EUR/MWh; pentru a-l exprima procentual, împărțiți la MAE cu valoare constantă în oră, 26,02. O baterie licitează pe sferturi de oră, deci trebuie să primească prognoza cu profil."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Economic value of a better forecast",
                "text": "A battery of 1 MW (megawatt) and 2 MWh with 90% round-trip efficiency runs one daily cycle chosen from the forecast. Over the 363 days without daylight saving time changes it earns 90,738 EUR per MW with the ensemble forecast, 84,623 EUR with the naive forecast and 99,698 EUR under perfect foresight. How much more does the ensemble earn than naive?",
                "options": [
                    "About 8,960 EUR per MW",
                    "About 16,115 EUR per MW",
                    "About 9,075 EUR per MW",
                    "About 6,115 EUR per MW"
                ],
                "correctExplanation": "90,738 − 84,623 = 6,115 EUR per MW over the year. The ensemble reaches 91.0% of the perfect-foresight profit, against 84.9% for naive.",
                "incorrectExplanation": "8,960 EUR is the gap between perfect foresight and the ensemble, not between the ensemble and naive. Translating relative accuracy into euros like this is what should precede paying for a forecast."
            },
            "ro": {
                "title": "Valoarea economică a unei prognoze mai bune",
                "text": "O baterie de 1 MW (megawatt) și 2 MWh, cu randament de 90%, face un ciclu pe zi, ales după prognoză. În cele 363 de zile fără schimbarea orei, cîștigă 90 738 EUR pe MW cu prognoza ansamblului, 84 623 EUR cu modelul naiv și 99 698 EUR cu informație perfectă. Cu cît cîștigă mai mult ansamblul decît modelul naiv?",
                "options": [
                    "Cu circa 8 960 EUR pe MW",
                    "Cu circa 16 115 EUR pe MW",
                    "Cu circa 9 075 EUR pe MW",
                    "Cu circa 6 115 EUR pe MW"
                ],
                "correctExplanation": "90 738 − 84 623 = 6 115 EUR pe MW într-un an. Ansamblul obține 91,0% din profitul cu informație perfectă, față de 84,9% pentru modelul naiv.",
                "incorrectExplanation": "8 960 EUR este diferența dintre informația perfectă și ansamblu, nu dintre ansamblu și modelul naiv. Un astfel de calcul, care transformă acuratețea relativă în euro, trebuie făcut înainte de a plăti pentru o prognoză."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "An implausibly accurate vendor backtest",
                "text": "A vendor reports a relative mean absolute error (rMAE) of 0.55 for Romanian day-ahead prices and uses the realised load of day $d-1$ as a regressor. The best honest model of the lecture reaches 0.795. What do you do?",
                "options": [
                    "Buy it: an rMAE of 0.55 is far better than any model of the lecture",
                    "Buy it, but only for the evening hours where errors are largest",
                    "Ask for the in-sample fit instead, which is more stable than a rolling backtest",
                    "Do not buy: day $d-1$ is not metered at 12:00 on $d-1$, so the backtest leaks information; ask for a rerun with data up to $d-2$ or published forecasts"
                ],
                "correctExplanation": "Every input must be public before 12:00 Central European Time on $d-1$. A backtest that uses the realised load of $d-1$ looks excellent and cannot be run on a trading desk.",
                "incorrectExplanation": "The impressive number is a symptom of leakage, not of skill. Ask for a rolling backtest that obeys the 12:00 rule, with scalers and penalties fitted in the calibration window only, as the lecture's own leakage self-check does."
            },
            "ro": {
                "title": "O testare retrospectivă neverosimil de bună a unui furnizor",
                "text": "Un furnizor de prognoze raportează pentru prețurile pe Piața pentru Ziua Următoare (PZU) din România o eroare absolută medie relativă (rMAE) de 0,55, dar folosește ca regresor consumul realizat în ziua $d-1$. Cel mai bun model corect din curs ajunge la 0,795. Ce faceți?",
                "options": [
                    "Cumpărați prognoza: o rMAE de 0,55 este mult mai bună decît orice model din curs",
                    "Cumpărați prognoza, dar numai pentru orele de seară, unde erorile sînt cele mai mari",
                    "Cereți în schimb ajustarea pe datele de estimare, mai stabilă decît o testare cu fereastră glisantă",
                    "Nu cumpărați: ziua $d-1$ nu este măsurată la 12:00 în ziua $d-1$, deci testarea folosește informație din viitor; cereți o nouă testare cu date pînă în $d-2$ sau cu prognozele publicate"
                ],
                "correctExplanation": "Orice variabilă de intrare trebuie să fie publică înainte de ora 12:00 a Europei Centrale (CET) din ziua $d-1$. O testare retrospectivă cu consumul realizat în ziua $d-1$ pare excelentă, dar nu poate fi rulată într-un birou de tranzacționare.",
                "incorrectExplanation": "Cifra impresionantă este un simptom al folosirii informației din viitor, nu al calității. Cereți o testare cu fereastră glisantă care respectă regula orei 12:00, cu standardizări și penalizări estimate numai pe fereastra de calibrare, ca în testul de verificare al cursului."
            }
        }
    ]
};
