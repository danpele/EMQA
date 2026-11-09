// ============================================================
// Quiz bank for lecture id 'l7': Machine learning and foundation models for electricity price forecasting (EN + RO)
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.EMQA_DATA.quizzes['l7'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 0,
            "en": {
                "title": "Role of the validation year",
                "text": "In the experiment of the lecture on the Romanian day-ahead market (PZU, Piața pentru Ziua Următoare), what is the validation year 1 Nov 2024 – 31 Oct 2025 used for?",
                "options": [
                    "Only to choose the settings (hyperparameters) of each model, which are frozen before the test year is opened",
                    "To rank the final models and compute the Diebold–Mariano (DM) tests reported in the scoreboard",
                    "To estimate the weights of the combinations, while the settings are chosen on the test year",
                    "To run the leakage check, by replacing all future data with 10,000 EUR/MWh"
                ],
                "correctExplanation": "Settings are chosen by random search on the validation year only: the setting with the lowest mean absolute error (MAE) is frozen, and the test year 1 Nov 2025 – 31 Oct 2026 is opened once, after every choice is made.",
                "incorrectExplanation": "The test year is never used to choose anything, and the final comparison, including the DM tests against the benchmark, is made on the test year. The validation year exists precisely so that tuning never touches the data on which the models are judged."
            },
            "ro": {
                "title": "Rolul anului de validare",
                "text": "În experimentul din curs pe piața pentru ziua următoare (PZU), la ce folosește anul de validare 1 noiembrie 2024 – 31 octombrie 2025?",
                "options": [
                    "Numai la alegerea setărilor (hiperparametrilor) fiecărui model, care sînt fixate înainte de deschiderea anului de test",
                    "La clasarea finală a modelelor și la calculul testelor Diebold–Mariano (DM) din clasament",
                    "La estimarea ponderilor combinațiilor, în timp ce setările se aleg pe anul de test",
                    "La testul de scurgere a informației, prin înlocuirea tuturor datelor viitoare cu 10 000 EUR/MWh"
                ],
                "correctExplanation": "Setările se aleg prin căutare aleatoare numai pe anul de validare: setarea cu cea mai mică eroare absolută medie (MAE) este fixată, iar anul de test, 1 noiembrie 2025 – 31 octombrie 2026, se deschide o singură dată, după ce toate alegerile au fost făcute.",
                "incorrectExplanation": "Anul de test nu se folosește pentru nicio alegere, iar comparația finală, inclusiv testele DM față de reper, se face pe anul de test. Anul de validare există tocmai pentru ca reglarea modelelor să nu atingă niciodată datele pe care acestea sînt judecate."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Shuffled cross-validation gain",
                "text": "The honest walk-forward mean absolute error (MAE) of eXtreme Gradient Boosting (XGBoost) on the test year is 23.26 EUR/MWh; with shuffled 5-fold cross-validation it is 22.01. By how much does shuffling flatter the model, relative to the honest MAE?",
                "options": [
                    "About 1.25%, the difference between the two errors",
                    "About 5.4%",
                    "About 5.7%",
                    "About 3.1%"
                ],
                "correctExplanation": "$(23.26-22.01)/23.26 = 1.25/23.26 \\approx 5.4\\%$. The gain exists on paper only: shuffling the days puts future days in the training sample.",
                "incorrectExplanation": "The relative gain divides the difference by the honest MAE, not by the flattered one (that gives 5.7%), and 1.25 is in EUR/MWh, not in percent. The 3.1% belongs to the other invalid evaluation, with same-day load and wind and solar as inputs."
            },
            "ro": {
                "title": "Cîștigul validării cu amestecare",
                "text": "Eroarea absolută medie (MAE) corectă, cronologică, a modelului eXtreme Gradient Boosting (XGBoost) în anul de test este 23,26 EUR/MWh; cu validarea încrucișată cu 5 subeșantioane amestecate devine 22,01. Cu cît avantajează amestecarea modelul, în raport cu MAE corectă?",
                "options": [
                    "Cu circa 1,25%, diferența dintre cele două erori",
                    "Cu circa 5,4%",
                    "Cu circa 5,7%",
                    "Cu circa 3,1%"
                ],
                "correctExplanation": "$(23{,}26-22{,}01)/23{,}26 = 1{,}25/23{,}26 \\approx 5{,}4\\%$. Cîștigul există doar pe hîrtie: amestecarea zilelor aduce zile din viitor în eșantionul de antrenare.",
                "incorrectExplanation": "Cîștigul relativ împarte diferența la MAE corectă, nu la cea avantajată (care dă 5,7%), iar 1,25 este în EUR/MWh, nu în procente. Valoarea de 3,1% aparține celeilalte evaluări invalide, cu consumul și producția eoliană și solară din aceeași zi ca intrări."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Parameters per day of history",
                "text": "The tuned deep neural network (DNN) has 141,336 parameters for 1,727 training days at the last refit, while the Lasso-estimated autoregressive (LEAR) model has at most 247 coefficients per hour. What follows for the evaluation?",
                "options": [
                    "A low training error proves that the network will forecast well, since it is more flexible than LEAR",
                    "The network must use fewer inputs than LEAR, otherwise it cannot be estimated at all",
                    "The network should be judged on its training error, corrected for the number of parameters",
                    "The training error says nothing about the future: only days the model has not seen can judge it"
                ],
                "correctExplanation": "With so many parameters the network can bend towards the noise of the training years. The penalty on complexity and the stopping rules limit this, but the final judgement always comes from days kept aside.",
                "incorrectExplanation": "Flexibility buys thresholds and interactions and pays for them with variance. A network with many more parameters than days can still be estimated, with penalties and early stopping, but its fit to the past is no evidence; ask on which days its error was measured."
            },
            "ro": {
                "title": "Parametri pe zi de istoric",
                "text": "Rețeaua neuronală profundă (DNN) calibrată are 141 336 de parametri pentru 1 727 de zile de antrenare la ultima reestimare, în timp ce modelul autoregresiv estimat cu Lasso (LEAR) are cel mult 247 de coeficienți pentru fiecare oră. Ce rezultă pentru evaluare?",
                "options": [
                    "O eroare mică pe datele de antrenare dovedește că rețeaua va prognoza bine, fiindcă este mai flexibilă decît LEAR",
                    "Rețeaua trebuie să folosească mai puține variabile decît LEAR, altfel nu poate fi estimată deloc",
                    "Rețeaua trebuie judecată după eroarea pe datele de antrenare, corectată cu numărul de parametri",
                    "Eroarea pe datele de antrenare nu spune nimic despre viitor: modelul poate fi judecat numai pe zile nevăzute"
                ],
                "correctExplanation": "Cu atîția parametri, rețeaua se poate apleca spre zgomotul anilor de antrenare. Penalizarea complexității și regulile de oprire limitează acest lucru, dar verdictul final vine întotdeauna din zilele păstrate deoparte.",
                "incorrectExplanation": "Flexibilitatea aduce praguri și interacțiuni, dar se plătește prin varianță. O rețea cu mult mai mulți parametri decît zile poate fi estimată, cu penalizări și oprire timpurie, însă potrivirea pe trecut nu este o dovadă; întrebați pe ce zile a fost măsurată eroarea."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Advantages of random search",
                "text": "Hyperparameters are chosen by trying 24 random settings plus the Lecture 2 setting for each model. Why random draws rather than a full grid (Bergstra and Bengio, 2012)?",
                "options": [
                    "Random draws guarantee that the global optimum of the validation error is found",
                    "A full grid would require the test year to evaluate the settings",
                    "Only a few settings really matter, and random draws cover each of them better for the same budget",
                    "Random search removes the need for a separate validation sample"
                ],
                "correctExplanation": "For the same number of trials, a grid repeats the same few values of each important setting, while random draws try many different values of each. The whole search took 7.3 minutes on one core of the central processing unit (CPU).",
                "incorrectExplanation": "Random search gives no guarantee of a global optimum, and it still needs a validation sample: a search without one is not a search but a leak. Its advantage is efficiency when only a few settings matter."
            },
            "ro": {
                "title": "Avantajele căutării aleatoare",
                "text": "Hiperparametrii se aleg încercînd 24 de setări aleatoare plus setarea din cursul 2, pentru fiecare model. De ce extrageri aleatoare și nu o grilă completă (Bergstra și Bengio, 2012)?",
                "options": [
                    "Extragerile aleatoare garantează găsirea optimului global al erorii de validare",
                    "O grilă completă ar presupune folosirea anului de test pentru evaluarea setărilor",
                    "Doar cîteva setări contează cu adevărat, iar extragerile aleatoare le acoperă mai bine, cu același număr de încercări",
                    "Căutarea aleatoare face inutil un eșantion de validare separat"
                ],
                "correctExplanation": "Cu același număr de încercări, o grilă repetă aceleași cîteva valori ale fiecărei setări importante, în timp ce extragerile aleatoare încearcă multe valori diferite. Întreaga căutare a durat 7,3 minute pe un nucleu al unității centrale de procesare (CPU).",
                "incorrectExplanation": "Căutarea aleatoare nu garantează un optim global și are nevoie în continuare de un eșantion de validare: o căutare fără el nu este o căutare, ci o scurgere de informație. Avantajul ei este eficiența atunci cînd doar cîteva setări contează."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Gain from tuning the DNN",
                "text": "On the validation year, the best setting of the deep neural network (DNN) has a mean absolute error (MAE) of 22.59 EUR/MWh, while the Lecture 2 setting has 24.24. By how much does tuning reduce the validation MAE, relative to the Lecture 2 setting?",
                "options": [
                    "About 6.8%",
                    "About 7.3%",
                    "About 1.65%",
                    "About 14%"
                ],
                "correctExplanation": "$(24.24-22.59)/24.24 = 1.65/24.24 \\approx 6.8\\%$. The Lecture 2 setting ranked only 14 of the 25 settings tried.",
                "incorrectExplanation": "Divide by the starting point, the Lecture 2 setting: dividing by 22.59 gives 7.3%. The figure 1.65 is in EUR/MWh, and 14 is the rank of the Lecture 2 setting among the 25 tried, not a percentage."
            },
            "ro": {
                "title": "Cîștigul din calibrarea DNN",
                "text": "În anul de validare, cea mai bună setare a rețelei neuronale profunde (DNN) are o eroare absolută medie (MAE) de 22,59 EUR/MWh, iar setarea din cursul 2 are 24,24. Cu cît reduce calibrarea MAE de validare, în raport cu setarea din cursul 2?",
                "options": [
                    "Cu circa 6,8%",
                    "Cu circa 7,3%",
                    "Cu circa 1,65%",
                    "Cu circa 14%"
                ],
                "correctExplanation": "$(24{,}24-22{,}59)/24{,}24 = 1{,}65/24{,}24 \\approx 6{,}8\\%$. Setarea din cursul 2 era doar pe locul 14 din cele 25 de setări încercate.",
                "incorrectExplanation": "Se împarte la punctul de plecare, setarea din cursul 2: împărțirea la 22,59 dă 7,3%. Valoarea 1,65 este în EUR/MWh, iar 14 este locul setării din cursul 2 între cele 25 încercate, nu un procent."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Reading the learning curve",
                "text": "In the refit for Oct 2026 of the deep neural network (DNN), the error on the last 15% of training days reaches its minimum at epoch 51 (24.50 EUR/MWh) and training stops at epoch 76, while the training error keeps falling. How is this used?",
                "options": [
                    "The network is kept at epoch 76, since its training error is lowest there",
                    "The last 15% of days are added to the test year to measure the final error",
                    "Epoch 51 is kept, and the network is refitted on all training days for that many epochs",
                    "Training restarts with more neurons, because the error on recent days rises"
                ],
                "correctExplanation": "After epoch 51 the network fits the past better and recent days worse: it starts to memorise. Early stopping uses only past days, and the network is then refitted on all days for the best number of epochs (median 56 over 12 refits $\\times$ 4 seeds).",
                "incorrectExplanation": "A falling training error is not a sign of a better forecast; the gap between the two curves is variance made visible. The stopping rule never touches the test year, and the cure for memorising is to stop earlier, not to add neurons."
            },
            "ro": {
                "title": "Citirea curbei de învățare",
                "text": "În reestimarea din octombrie 2026 a rețelei neuronale profunde (DNN), eroarea pe ultimele 15% din zilele de antrenare atinge minimul la epoca 51 (24,50 EUR/MWh), iar antrenarea se oprește la epoca 76, în timp ce eroarea pe datele de antrenare continuă să scadă. Cum se folosește această informație?",
                "options": [
                    "Rețeaua este păstrată la epoca 76, fiindcă acolo eroarea pe datele de antrenare este minimă",
                    "Ultimele 15% din zile sînt adăugate anului de test pentru măsurarea erorii finale",
                    "Se păstrează epoca 51, iar rețeaua se reestimează pe toate zilele de antrenare, cu același număr de epoci",
                    "Antrenarea se reia cu mai mulți neuroni, pentru că eroarea pe zilele recente crește"
                ],
                "correctExplanation": "După epoca 51, rețeaua reproduce tot mai bine trecutul și tot mai slab zilele recente: începe să memoreze. Oprirea timpurie folosește numai zile din trecut, apoi rețeaua se reestimează pe toate zilele, cu numărul cel mai bun de epoci (mediana 56, pe 12 reestimări $\\times$ 4 inițializări).",
                "incorrectExplanation": "O eroare de antrenare în scădere nu înseamnă o prognoză mai bună; distanța dintre cele două curbe este varianța, făcută vizibilă. Regula de oprire nu atinge anul de test, iar remediul pentru memorare este oprirea mai devreme, nu mai mulți neuroni."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "How boosting builds a forecast",
                "text": "The tuned eXtreme Gradient Boosting (XGBoost) model has 1,500 trees of depth 8 and a learning rate $\\eta = 0.02$. Which description of gradient boosting is right?",
                "options": [
                    "Each tree is fitted independently on a bootstrap sample, and the trees are averaged with equal weights",
                    "Each new tree is fitted to what is still wrong and added with a small weight, $F_m = F_{m-1} + \\eta f_m$",
                    "Only the best of the 1,500 trees is kept, chosen by its error on the validation year",
                    "One tree is fitted per hour of the day, so the 1,500 trees form 24 separate models"
                ],
                "correctExplanation": "Boosting corrects the remaining errors step by step; the small weight $\\eta = 0.02$ means that many trees are needed, each contributing a little. Each tree is fitted on a fraction 0.8 of the rows.",
                "incorrectExplanation": "Independent trees on bootstrap samples, averaged, describe a random forest, not boosting. Boosting keeps all the trees and adds them in sequence, each one correcting the errors left by the sum of the previous ones."
            },
            "ro": {
                "title": "Cum construiește boosting prognoza",
                "text": "Modelul eXtreme Gradient Boosting (XGBoost) calibrat are 1 500 de arbori de adîncime 8 și rata de învățare $\\eta = 0{,}02$. Care descriere a metodei gradient boosting este corectă?",
                "options": [
                    "Fiecare arbore este estimat independent, pe un eșantion bootstrap, iar arborii sînt mediați cu ponderi egale",
                    "Fiecare arbore nou este potrivit pe ceea ce este încă greșit și adăugat cu o pondere mică, $F_m = F_{m-1} + \\eta f_m$",
                    "Se păstrează doar cel mai bun dintre cei 1 500 de arbori, ales după eroarea din anul de validare",
                    "Se estimează cîte un arbore pentru fiecare oră a zilei, deci cei 1 500 de arbori formează 24 de modele separate"
                ],
                "correctExplanation": "Gradient boosting corectează pas cu pas erorile rămase; ponderea mică $\\eta = 0{,}02$ face necesari mulți arbori, fiecare contribuind puțin. Fiecare arbore este estimat pe o fracțiune 0,8 din rînduri.",
                "incorrectExplanation": "Arborii independenți, estimați pe eșantioane bootstrap și mediați, descriu o pădure aleatoare, nu gradient boosting. Gradient boosting păstrează toți arborii și îi adaugă secvențial, fiecare corectînd erorile lăsate de suma celor dinainte."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Ceiling of a sum of leaves",
                "text": "In the October 2026 refit of eXtreme Gradient Boosting (XGBoost), the first tree asks whether the price of day $d-1$, same hour, is below 119.5 EUR/MWh; that tree has 233 leaves, and the model adds up 1,500 such trees, each leaf holding a value $w_j^{*}=-G_j/(H_j+\\lambda)$ learnt on the training days. What follows for extreme prices?",
                "options": [
                    "Extremes are handled best, because 1,500 trees can add up to any value",
                    "The learning rate removes any upper limit once enough trees are added",
                    "Thresholds such as 119.5 EUR/MWh are re-estimated every hour, so new extremes are learnt at once",
                    "A price far above anything seen in training cannot be forecast, because the forecast is a sum of leaf values learnt from the past"
                ],
                "correctExplanation": "Trees cannot go above the prices stored in their leaves, so extremes are capped; this is a structural limit of trees, unlike linear models, which can extrapolate.",
                "incorrectExplanation": "Every leaf value is computed from training observations, so adding more trees or shrinking each step with the learning rate does not create values beyond what the past contained; the model is refitted monthly, not hourly."
            },
            "ro": {
                "title": "Plafonul unei sume de frunze",
                "text": "În reestimarea pentru octombrie 2026 a modelului eXtreme Gradient Boosting (XGBoost), primul arbore întreabă dacă prețul din ziua $d-1$, aceeași oră, este sub 119,5 EUR/MWh; acest arbore are 233 de frunze, iar modelul adună 1 500 de asemenea arbori, fiecare frunză conținînd o valoare $w_j^{*}=-G_j/(H_j+\\lambda)$ învățată pe zilele de antrenare. Ce rezultă pentru prețurile extreme?",
                "options": [
                    "Extremele sînt tratate cel mai bine, pentru că 1 500 de arbori pot însuma orice valoare",
                    "Rata de învățare elimină orice limită superioară, dacă se adaugă destui arbori",
                    "Pragurile precum 119,5 EUR/MWh sînt reestimate în fiecare oră, deci extremele noi sînt învățate imediat",
                    "Un preț mult peste tot ce s-a văzut la antrenare nu poate fi prognozat, pentru că prognoza este o sumă de valori ale frunzelor învățate din trecut"
                ],
                "correctExplanation": "Arborii nu pot depăși prețurile memorate în frunze, deci valorile extreme sînt plafonate; aceasta este o limită structurală a arborilor, spre deosebire de modelele liniare, care pot extrapola.",
                "incorrectExplanation": "Fiecare valoare a unei frunze se calculează din observațiile de antrenare, deci adăugarea de arbori sau micșorarea fiecărui pas prin rata de învățare nu creează valori dincolo de ce a conținut trecutul; modelul este reestimat lunar, nu în fiecare oră."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Tuned trees against benchmarks",
                "text": "On the test year, tuned eXtreme Gradient Boosting (XGBoost) has a mean absolute error (MAE) of 23.26 EUR/MWh, against 24.05 for the untuned gradient boosting machine (GBM) of Lecture 2 (Diebold–Mariano (DM) test, $p \\lt 0.001$) and 22.53 for AW-LEAR, the Lasso-estimated autoregressive (LEAR) model averaged across calibration windows (DM, $p = 0.016$). What is the correct reading?",
                "options": [
                    "Tuning made no real difference, since the gain over the GBM is below one euro per MWh",
                    "XGBoost beats AW-LEAR, because its p-value against the GBM is below 0.001",
                    "Tuning gives a significant gain over the GBM, but AW-LEAR remains significantly more accurate",
                    "The three models are equivalent, since their MAEs differ by less than 2 EUR/MWh"
                ],
                "correctExplanation": "Both one-sided tests reject: XGBoost is more accurate than the GBM, and AW-LEAR is more accurate than XGBoost. Tuning matters more than the software: the same kind of trees gained almost one euro per MWh from good settings.",
                "incorrectExplanation": "Significance is judged by the DM test, not by the size of the gap in EUR/MWh, and each p-value refers to one specific pair of models. A win over the GBM says nothing about AW-LEAR."
            },
            "ro": {
                "title": "Arbori calibrați față de repere",
                "text": "În anul de test, modelul eXtreme Gradient Boosting (XGBoost) calibrat are eroarea absolută medie (MAE) 23,26 EUR/MWh, față de 24,05 pentru modelul gradient boosting (GBM) necalibrat din cursul 2 (testul Diebold–Mariano (DM), $p \\lt 0{,}001$) și 22,53 pentru AW-LEAR, modelul autoregresiv estimat cu Lasso (LEAR) mediat pe mai multe ferestre de calibrare (DM, $p = 0{,}016$). Care este interpretarea corectă?",
                "options": [
                    "Calibrarea nu a schimbat nimic important, fiindcă cîștigul față de GBM este sub un euro pe MWh",
                    "XGBoost este mai precis decît AW-LEAR, pentru că valoarea p față de GBM este sub 0,001",
                    "Calibrarea aduce un cîștig semnificativ față de GBM, dar AW-LEAR rămîne semnificativ mai precis",
                    "Cele trei modele sînt echivalente, fiindcă valorile MAE diferă cu mai puțin de 2 EUR/MWh"
                ],
                "correctExplanation": "Ambele teste unilaterale resping ipoteza nulă: XGBoost este mai precis decît GBM, iar AW-LEAR este mai precis decît XGBoost. Calibrarea contează mai mult decît programul: același tip de arbori a cîștigat aproape un euro pe MWh prin setări bune.",
                "incorrectExplanation": "Semnificația se judecă prin testul DM, nu după mărimea diferenței în EUR/MWh, iar fiecare valoare p se referă la o anumită pereche de modele. Un cîștig față de GBM nu spune nimic despre AW-LEAR."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Inputs used by Chronos",
                "text": "How is the Chronos-2 foundation model used for the 24 day-ahead prices in this lecture (zero-shot)?",
                "options": [
                    "It receives the last 2048 hourly prices (85 days) and, without any training on Romanian data, returns quantiles; the median is the point forecast",
                    "It is retrained every month on Romanian prices, load, wind and solar, like the deep neural network (DNN)",
                    "It receives the same 251 inputs as the deep neural network (DNN) and is fine-tuned on the validation year",
                    "It receives the prices of day $d$ up to 12:00 and extrapolates the rest of the day"
                ],
                "correctExplanation": "Chronos models were pretrained by Amazon on large collections of time series and are used as they are. On the test year Chronos-2 had prices only, no fundamentals, and was never trained on our data.",
                "incorrectExplanation": "Zero-shot means no training or fine-tuning on the target data. The context ends with day $d-1$, and the code checks that it is built only from days before day $d$."
            },
            "ro": {
                "title": "Datele de intrare ale modelului Chronos",
                "text": "Cum este folosit modelul fundațional Chronos-2 pentru cele 24 de prețuri ale zilei următoare în acest curs (zero-shot)?",
                "options": [
                    "Primește ultimele 2048 de prețuri orare (85 de zile) și, fără nicio antrenare pe datele din România, dă cuantile; mediana este prognoza punctuală",
                    "Este reantrenat lunar pe prețurile, consumul și producția eoliană și solară din România, ca rețeaua neuronală profundă (DNN)",
                    "Primește aceleași 251 de intrări ca rețeaua neuronală profundă (DNN) și este ajustat pe anul de validare",
                    "Primește prețurile zilei $d$ pînă la ora 12:00 și extrapolează restul zilei"
                ],
                "correctExplanation": "Modelele Chronos au fost preantrenate de Amazon pe colecții mari de serii de timp și sînt folosite ca atare. În anul de test, Chronos-2 a avut numai prețuri, fără variabile fundamentale, și nu a fost antrenat niciodată pe datele noastre.",
                "incorrectExplanation": "Zero-shot înseamnă fără antrenare sau ajustare pe datele-țintă. Contextul se încheie cu ziua $d-1$, iar codul verifică faptul că este construit numai din zilele dinaintea zilei $d$."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Chronos-2 against AW-LEAR",
                "text": "On the test year, Chronos-2 has a mean absolute error (MAE) of 20.82 EUR/MWh and AW-LEAR, the Lasso-estimated autoregressive (LEAR) model averaged across calibration windows, has 22.53. What is the gain of Chronos-2, in percent of the MAE of AW-LEAR?",
                "options": [
                    "About 1.71%",
                    "About 8.2%",
                    "About 6.3%",
                    "About 7.6%"
                ],
                "correctExplanation": "$(22.53-20.82)/22.53 = 1.71/22.53 \\approx 7.6\\%$, as in the scoreboard; the one-sided Diebold–Mariano (DM) test gives $p \\lt 0.001$, and Chronos-2 is ahead in all 24 hours.",
                "incorrectExplanation": "The gain is measured relative to the benchmark: dividing by 20.82 gives 8.2%. The figure 1.71 is the difference in EUR/MWh, and 6.3% is the gain of the ensemble of 5 models that includes Chronos-2."
            },
            "ro": {
                "title": "Chronos-2 față de AW-LEAR",
                "text": "În anul de test, Chronos-2 are eroarea absolută medie (MAE) 20,82 EUR/MWh, iar AW-LEAR, modelul autoregresiv estimat cu Lasso (LEAR) mediat pe mai multe ferestre de calibrare, are 22,53. Cît este cîștigul modelului Chronos-2, în procente din MAE a modelului AW-LEAR?",
                "options": [
                    "Circa 1,71%",
                    "Circa 8,2%",
                    "Circa 6,3%",
                    "Circa 7,6%"
                ],
                "correctExplanation": "$(22{,}53-20{,}82)/22{,}53 = 1{,}71/22{,}53 \\approx 7{,}6\\%$, ca în clasament; testul Diebold–Mariano (DM) unilateral dă $p \\lt 0{,}001$, iar Chronos-2 este mai precis în toate cele 24 de ore.",
                "incorrectExplanation": "Cîștigul se măsoară în raport cu reperul: împărțirea la 20,82 dă 8,2%. Valoarea 1,71 este diferența în EUR/MWh, iar 6,3% este cîștigul ansamblului de 5 modele care include Chronos-2."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Coverage of the Chronos band",
                "text": "The 10%–90% forecast band of Chronos-2 holds 76.5% of the test-year prices. What should a risk manager conclude?",
                "options": [
                    "The band is too wide, so the model is too cautious about its own uncertainty",
                    "The band is too narrow: the model is overconfident, and the band should be recalibrated before sizing risk",
                    "The band is correct, since 76.5% lies between 10% and 90%",
                    "The median forecast is biased, so it should not be used"
                ],
                "correctExplanation": "A 10%–90% band should hold 80% of the prices; holding only 76.5% means that too many prices fall outside it. Use the median as the point forecast and recalibrate the bands (Lecture 2) before sizing risk with them.",
                "incorrectExplanation": "Coverage is compared with the nominal 80%, the probability between the 10% and 90% quantiles, not with the quantile levels themselves. Too little coverage means a band that is too narrow; it says nothing against the median, which was the most accurate single point forecast."
            },
            "ro": {
                "title": "Acoperirea intervalului Chronos",
                "text": "Intervalul de prognoză 10%–90% al modelului Chronos-2 conține 76,5% din prețurile anului de test. Ce ar trebui să concluzioneze un manager de risc?",
                "options": [
                    "Intervalul este prea larg, deci modelul este prea prudent față de propria incertitudine",
                    "Intervalul este prea îngust: modelul își subestimează incertitudinea, iar intervalul trebuie recalibrat înainte de a dimensiona riscul",
                    "Intervalul este corect, fiindcă 76,5% se află între 10% și 90%",
                    "Prognoza mediană este deplasată, deci nu trebuie folosită"
                ],
                "correctExplanation": "Un interval 10%–90% ar trebui să conțină 80% din prețuri; dacă acoperă doar 76,5%, prea multe prețuri cad în afara lui. Folosiți mediana ca prognoză punctuală și recalibrați intervalele (cursul 2) înainte de a dimensiona riscul cu ele.",
                "incorrectExplanation": "Acoperirea se compară cu nivelul nominal de 80%, probabilitatea dintre cuantilele de 10% și 90%, nu cu nivelurile cuantilelor. O acoperire prea mică înseamnă un interval prea îngust; nu spune nimic împotriva medianei, care a fost cea mai precisă prognoză punctuală individuală."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Zero-shot rankings across years",
                "text": "In the zero-shot comparison shown in Rafał Weron's AIDA 2026 keynote, the root mean squared error (RMSE) in 2022 was 45.71 for the Lasso-estimated autoregressive (LEAR) model with conformal prediction, 41.07 for Chronos 2 and 34.39 for TabPFN v3.0 ts; in 2025 it was 20.38, 20.58 and 17.66. Which lesson fits these numbers?",
                "options": [
                    "Zero-shot models always beat LEAR, whatever the year",
                    "LEAR should be abandoned, since it was the worst model in both years",
                    "Rankings move between years: Chronos 2 beat LEAR in 2022 but not in 2025, so one year is not enough to rank models",
                    "The 2025 errors are lower, so the models must have been retrained on the test data"
                ],
                "correctExplanation": "In 2025 LEAR (20.38) was slightly ahead of Chronos 2 (20.58), the reverse of 2022. Keep LEAR as the benchmark and test zero-shot models next to it, over several years.",
                "incorrectExplanation": "Rankings, like error levels, change from year to year. LEAR was not the worst model in 2025, and the pretrained models were used without retraining on the test data; a single year is not enough to rank them."
            },
            "ro": {
                "title": "Clasamente zero-shot pe ani",
                "text": "În comparația modelelor zero-shot din conferința invitată a lui Rafał Weron la AIDA 2026, rădăcina erorii pătratice medii (RMSE) a fost în 2022 de 45,71 pentru modelul autoregresiv estimat cu Lasso (LEAR) cu predicție conformală, 41,07 pentru Chronos 2 și 34,39 pentru TabPFN v3.0 ts; în 2025 a fost 20,38, 20,58 și, respectiv, 17,66. Ce lecție se potrivește acestor cifre?",
                "options": [
                    "Modelele zero-shot sînt întotdeauna mai precise decît LEAR, indiferent de an",
                    "LEAR trebuie abandonat, fiindcă a fost cel mai slab model în ambii ani",
                    "Clasamentele se schimbă de la un an la altul: Chronos 2 a întrecut LEAR în 2022, dar nu și în 2025, deci un singur an nu ajunge pentru a ordona modelele",
                    "Erorile din 2025 sînt mai mici, deci modelele trebuie să fi fost reantrenate pe datele de test"
                ],
                "correctExplanation": "În 2025, LEAR (20,38) a fost puțin înaintea modelului Chronos 2 (20,58), invers decît în 2022. Păstrați LEAR ca reper și testați modelele zero-shot alături de el, pe mai mulți ani.",
                "incorrectExplanation": "Clasamentele, ca și nivelul erorilor, se schimbă de la un an la altul. LEAR nu a fost cel mai slab model în 2025, iar modelele preantrenate au fost folosite fără reantrenare pe datele de test; un singur an nu ajunge pentru a le ordona."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Relative MAE of the DNN",
                "text": "The relative mean absolute error (rMAE) divides the MAE of a model by that of the naive model. On the test year the naive model has MAE 27.82 EUR/MWh and the tuned deep neural network (DNN) 22.95. What is the rMAE of the DNN?",
                "options": [
                    "0.825",
                    "0.810",
                    "1.212",
                    "0.175"
                ],
                "correctExplanation": "$22.95/27.82 \\approx 0.825$: the DNN errs about 17.5% less than the naive model.",
                "incorrectExplanation": "The rMAE puts the model in the numerator and the naive model in the denominator; the inverse gives 1.212, and 0.175 is one minus the rMAE, the gain over the naive model. 0.810 is the rMAE of the Lasso-estimated autoregressive (LEAR) model averaged across calibration windows (AW-LEAR)."
            },
            "ro": {
                "title": "MAE relativă a rețelei DNN",
                "text": "MAE relativă (rMAE) împarte eroarea absolută medie (MAE) a unui model la cea a modelului naiv. În anul de test, modelul naiv are MAE 27,82 EUR/MWh, iar rețeaua neuronală profundă (DNN) calibrată 22,95. Cît este rMAE a rețelei DNN?",
                "options": [
                    "0,825",
                    "0,810",
                    "1,212",
                    "0,175"
                ],
                "correctExplanation": "$22{,}95/27{,}82 \\approx 0{,}825$: rețeaua DNN greșește cu circa 17,5% mai puțin decît modelul naiv.",
                "incorrectExplanation": "rMAE pune modelul la numărător și modelul naiv la numitor; inversul dă 1,212, iar 0,175 este 1 minus rMAE, adică cîștigul față de modelul naiv. Valoarea 0,810 este rMAE a modelului autoregresiv estimat cu Lasso (LEAR) mediat pe mai multe ferestre de calibrare (AW-LEAR)."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Combination compared with the benchmark",
                "text": "One-sided Diebold–Mariano (DM) tests against AW-LEAR, the Lasso-estimated autoregressive (LEAR) model averaged across calibration windows, give $p = 0.944$ for the tuned deep neural network (DNN), $p = 0.984$ for tuned eXtreme Gradient Boosting (XGBoost) and $p = 0.001$ for the average AW-LEAR + DNN + XGBoost. What is the correct reading?",
                "options": [
                    "The machine learning models are useless, since neither beats AW-LEAR alone",
                    "The combination wins only because it contains three models, so any three models would win",
                    "A p-value of 0.944 shows that the DNN is significantly better than AW-LEAR",
                    "Neither model beats AW-LEAR alone, but averaged with it they do, and the gain is significant"
                ],
                "correctExplanation": "The combination has a mean absolute error (MAE) of 21.97 EUR/MWh against 22.53 (+2.5%). Its errors are not perfectly correlated with those of AW-LEAR, so averaging lowers the error even though each machine learning model alone is slightly worse.",
                "incorrectExplanation": "In a one-sided test that the model is more accurate than AW-LEAR, a large p-value means no evidence of a gain. Adding models helps only when their errors differ: adding AW-LEAR to Chronos-2 changed nothing ($p = 0.491$)."
            },
            "ro": {
                "title": "Combinația comparată cu reperul",
                "text": "Testele Diebold–Mariano (DM) unilaterale față de AW-LEAR, modelul autoregresiv estimat cu Lasso (LEAR) mediat pe mai multe ferestre de calibrare, dau $p = 0{,}944$ pentru rețeaua neuronală profundă (DNN) calibrată, $p = 0{,}984$ pentru eXtreme Gradient Boosting (XGBoost) calibrat și $p = 0{,}001$ pentru media AW-LEAR + DNN + XGBoost. Care este interpretarea corectă?",
                "options": [
                    "Modelele de învățare automată sînt inutile, fiindcă niciunul nu întrece singur AW-LEAR",
                    "Combinația cîștigă doar pentru că are trei modele, deci orice trei modele ar cîștiga",
                    "O valoare p de 0,944 arată că rețeaua DNN este semnificativ mai bună decît AW-LEAR",
                    "Niciun model nu întrece singur AW-LEAR, dar în medie cu acesta îl întrec, iar cîștigul este semnificativ"
                ],
                "correctExplanation": "Combinația are eroarea absolută medie (MAE) 21,97 EUR/MWh, față de 22,53 (+2,5%). Erorile ei nu sînt perfect corelate cu cele ale modelului AW-LEAR, așa că media reduce eroarea, deși fiecare model de învățare automată, luat separat, este puțin mai slab.",
                "incorrectExplanation": "Într-un test unilateral că modelul este mai precis decît AW-LEAR, o valoare p mare înseamnă că nu există dovezi ale unui cîștig. Adăugarea de modele ajută numai cînd erorile lor diferă: adăugarea AW-LEAR la Chronos-2 nu a schimbat nimic ($p = 0{,}491$)."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Variance of an averaged error",
                "text": "For two forecast errors with the same standard deviation $\\sigma$ and correlation $\\rho$, the variance of their average is $\\tfrac14(\\sigma^2+\\sigma^2+2\\rho\\sigma^2)$. With $\\rho = 0.89$, the correlation of the errors of eXtreme Gradient Boosting (XGBoost) with those of the statistical benchmark, what share of the single-model variance remains?",
                "options": [
                    "0.89",
                    "0.945",
                    "1.000",
                    "0.445"
                ],
                "correctExplanation": "$\\tfrac14(2+2\\cdot 0.89)\\sigma^2 = \\tfrac{1+0.89}{2}\\sigma^2 = 0.945\\,\\sigma^2$. The gain is modest but real, because $\\rho \\lt 1$ (Bates and Granger, 1969).",
                "incorrectExplanation": "The formula gives $(1+\\rho)/2$, not $\\rho$ or $\\rho/2$. Only with perfectly correlated errors, $\\rho = 1$, would the average bring no gain at all."
            },
            "ro": {
                "title": "Varianța erorii mediate",
                "text": "Pentru două erori de prognoză cu aceeași abatere standard $\\sigma$ și corelația $\\rho$, varianța mediei lor este $\\tfrac14(\\sigma^2+\\sigma^2+2\\rho\\sigma^2)$. Cu $\\rho = 0{,}89$, corelația erorilor modelului eXtreme Gradient Boosting (XGBoost) cu cele ale modelului statistic de referință, ce parte din varianța unui singur model rămîne?",
                "options": [
                    "0,89",
                    "0,945",
                    "1,000",
                    "0,445"
                ],
                "correctExplanation": "$\\tfrac14(2+2\\cdot 0{,}89)\\sigma^2 = \\tfrac{1+0{,}89}{2}\\sigma^2 = 0{,}945\\,\\sigma^2$. Cîștigul este modest, dar real, pentru că $\\rho \\lt 1$ (Bates și Granger, 1969).",
                "incorrectExplanation": "Formula dă $(1+\\rho)/2$, nu $\\rho$ sau $\\rho/2$. Numai cu erori perfect corelate, $\\rho = 1$, media nu ar aduce niciun cîștig."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Chronos-2 alone or combined",
                "text": "Chronos-2 has a mean absolute error (MAE) of 20.82 EUR/MWh and the average AW-LEAR + Chronos-2 has 20.81, where AW-LEAR is the Lasso-estimated autoregressive (LEAR) model averaged across calibration windows; the Diebold–Mariano (DM) test between them gives $p = 0.491$. Which do you deploy, according to the lecture?",
                "options": [
                    "Chronos-2 alone, since adding AW-LEAR brings no gain and costs 87.6 minutes of computing",
                    "AW-LEAR alone, since it is the benchmark and the gains are not significant",
                    "The combination: same accuracy, but if the pretrained model degrades or becomes unavailable, LEAR still carries half of the forecast",
                    "The combination, because the DM test shows that it is significantly more accurate than Chronos-2"
                ],
                "correctExplanation": "The two have the same accuracy ($p = 0.491$): on the hard days the two models make similar errors. The case for the combination is robustness, not accuracy.",
                "incorrectExplanation": "$p = 0.491$ means no evidence of a difference in either direction, so the combination is not significantly better. AW-LEAR alone is 7.6% worse than Chronos-2, which beats it with $p \\lt 0.001$."
            },
            "ro": {
                "title": "Chronos-2 singur sau în combinație",
                "text": "Chronos-2 are eroarea absolută medie (MAE) 20,82 EUR/MWh, iar media AW-LEAR + Chronos-2 are 20,81, unde AW-LEAR este modelul autoregresiv estimat cu Lasso (LEAR) mediat pe mai multe ferestre de calibrare; testul Diebold–Mariano (DM) dintre ele dă $p = 0{,}491$. Pe care îl puneți în producție, potrivit cursului?",
                "options": [
                    "Chronos-2 singur, fiindcă adăugarea AW-LEAR nu aduce niciun cîștig și costă 87,6 minute de calcul",
                    "AW-LEAR singur, fiindcă este reperul, iar cîștigurile nu sînt semnificative",
                    "Combinația: aceeași acuratețe, dar dacă modelul preantrenat se degradează sau devine indisponibil, LEAR asigură în continuare jumătate din prognoză",
                    "Combinația, pentru că testul DM arată că este semnificativ mai precisă decît Chronos-2"
                ],
                "correctExplanation": "Cele două au aceeași acuratețe ($p = 0{,}491$): în zilele dificile, cele două modele greșesc asemănător. Argumentul pentru combinație este robustețea, nu acuratețea.",
                "incorrectExplanation": "$p = 0{,}491$ înseamnă că nu există dovezi ale unei diferențe în niciun sens, deci combinația nu este semnificativ mai bună. AW-LEAR singur este cu 7,6% mai slab decît Chronos-2, care îl întrece cu $p \\lt 0{,}001$."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Month-by-month comparison",
                "text": "Over the 12 months of the test year, how often do tuned eXtreme Gradient Boosting (XGBoost) and the deep neural network (DNN) beat AW-LEAR, the Lasso-estimated autoregressive (LEAR) model averaged across calibration windows, in monthly mean absolute error (MAE)?",
                "options": [
                    "Each alone in only 3 months; averaged with AW-LEAR, in 10 months",
                    "Each alone in 10 months; averaged with AW-LEAR, in all 12 months",
                    "Each alone in 6 months, and the combination in 6 as well",
                    "Never alone; the combination in 3 months, January, June and October"
                ],
                "correctExplanation": "An annual average can hide months in which a model is much worse. All models err more in the same months, January, June and October, so the combination helps in ordinary months but cannot remove the large errors of the difficult ones.",
                "incorrectExplanation": "Alone, the machine learning models are slightly worse than AW-LEAR over the year and win in only 3 months each. January, June and October are the months in which every model errs more, not the months won by the combination."
            },
            "ro": {
                "title": "Comparația lună de lună",
                "text": "În cele 12 luni ale anului de test, de cîte ori întrec eXtreme Gradient Boosting (XGBoost) calibrat și rețeaua neuronală profundă (DNN) modelul AW-LEAR, adică modelul autoregresiv estimat cu Lasso (LEAR) mediat pe mai multe ferestre de calibrare, după eroarea absolută medie (MAE) lunară?",
                "options": [
                    "Fiecare, singur, doar în 3 luni; în medie cu AW-LEAR, în 10 luni",
                    "Fiecare, singur, în 10 luni; în medie cu AW-LEAR, în toate cele 12 luni",
                    "Fiecare, singur, în 6 luni, iar combinația tot în 6",
                    "Niciodată singure; combinația în 3 luni: ianuarie, iunie și octombrie"
                ],
                "correctExplanation": "O medie anuală poate ascunde luni în care un model este mult mai slab. Toate modelele greșesc mai mult în aceleași luni, ianuarie, iunie și octombrie, așa că combinația ajută în lunile obișnuite, dar nu poate elimina erorile mari din lunile grele.",
                "incorrectExplanation": "Luate separat, modelele de învățare automată sînt puțin mai slabe decît AW-LEAR pe tot anul și cîștigă doar în cîte 3 luni. Ianuarie, iunie și octombrie sînt lunile în care toate modelele greșesc mai mult, nu lunile cîștigate de combinație."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Computational cost of AW-LEAR",
                "text": "Over the test year, on one processor core, AW-LEAR (the Lasso-estimated autoregressive (LEAR) model averaged across calibration windows) takes 87.6 minutes, against 2.6 for eXtreme Gradient Boosting (XGBoost), 2.7 for the deep neural network (DNN) and 0.3 for Chronos-2. Why is the statistical benchmark the expensive model?",
                "options": [
                    "It is fitted once per test hour, 8,760 times in total",
                    "It has many more parameters than the DNN",
                    "Its Lasso penalty is tuned again on 25 random settings every day",
                    "It is refitted for 365 days $\\times$ 3 windows $\\times$ 24 hours, while the machine learning models are refitted monthly"
                ],
                "correctExplanation": "Daily refits across three calibration windows and 24 separate hourly models add up. Chronos-2 is the cheapest because it is never trained; hidden costs, such as the 7.3-minute search and the people who run the pipeline every day, come on top.",
                "incorrectExplanation": "LEAR has at most 247 coefficients per hour, against 141,336 parameters in the DNN: its cost comes from how often it is refitted, not from its size. Compare models on error per euro of total cost of ownership, not on error alone."
            },
            "ro": {
                "title": "Costul de calcul al AW-LEAR",
                "text": "Pe tot anul de test, pe un singur nucleu, AW-LEAR (modelul autoregresiv estimat cu Lasso (LEAR) mediat pe mai multe ferestre de calibrare) are nevoie de 87,6 minute, față de 2,6 pentru eXtreme Gradient Boosting (XGBoost), 2,7 pentru rețeaua neuronală profundă (DNN) și 0,3 pentru Chronos-2. De ce este modelul statistic de referință cel scump?",
                "options": [
                    "Este estimat o dată pentru fiecare oră de test, de 8 760 de ori în total",
                    "Are mult mai mulți parametri decît rețeaua DNN",
                    "Penalizarea Lasso este recalibrată zilnic pe 25 de setări aleatoare",
                    "Este reestimat pentru 365 de zile $\\times$ 3 ferestre $\\times$ 24 de ore, în timp ce modelele de învățare automată sînt reestimate lunar"
                ],
                "correctExplanation": "Reestimările zilnice, pe trei ferestre de calibrare și pentru 24 de modele orare separate, se adună. Chronos-2 este cel mai ieftin, fiindcă nu este antrenat niciodată; la acestea se adaugă costurile ascunse, precum căutarea de 7,3 minute și oamenii care întrețin zilnic fluxul de date.",
                "incorrectExplanation": "LEAR are cel mult 247 de coeficienți pentru fiecare oră, față de 141 336 de parametri ai rețelei DNN: costul vine din frecvența reestimării, nu din mărimea modelului. Comparați modelele după eroare raportată la costul total de utilizare, nu doar după eroare."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Adding up SHAP contributions",
                "text": "For 30 Jun 2026, 20:00 Central European Time (CET), the eXtreme Gradient Boosting (XGBoost) forecast rises from 125 EUR/MWh, the model average, to 499. The SHapley Additive exPlanations (SHAP) contribution of the price of $d-1$ at the same hour is 213, and that of the price of $d-7$ is 64. How much do all the other inputs add together?",
                "options": [
                    "About 374 EUR/MWh",
                    "About 97 EUR/MWh",
                    "About 161 EUR/MWh",
                    "About 277 EUR/MWh"
                ],
                "correctExplanation": "SHAP values add up exactly to the forecast: $499 = 125 + 213 + 64 + \\text{rest}$, so the rest is $499-125-213-64 = 97$ EUR/MWh.",
                "incorrectExplanation": "Start from the model average, not from zero, and subtract both contributions shown: 374 is the whole gap $499-125$, 161 leaves out the price of $d-7$, and 277 is the sum of the two contributions."
            },
            "ro": {
                "title": "Însumarea contribuțiilor SHAP",
                "text": "Pentru 30 iunie 2026, ora 20:00 a Europei Centrale (CET), prognoza modelului eXtreme Gradient Boosting (XGBoost) urcă de la 125 EUR/MWh, prognoza medie a modelului, la 499. Contribuția SHAP (explicațiile aditive bazate pe valorile Shapley, SHapley Additive exPlanations) a prețului din $d-1$, aceeași oră, este 213, iar cea a prețului din $d-7$ este 64. Cît adaugă, împreună, toate celelalte variabile?",
                "options": [
                    "Circa 374 EUR/MWh",
                    "Circa 97 EUR/MWh",
                    "Circa 161 EUR/MWh",
                    "Circa 277 EUR/MWh"
                ],
                "correctExplanation": "Valorile SHAP se adună exact la prognoză: $499 = 125 + 213 + 64 + \\text{rest}$, deci restul este $499-125-213-64 = 97$ EUR/MWh.",
                "incorrectExplanation": "Se pornește de la prognoza medie, nu de la zero, și se scad ambele contribuții: 374 este întreaga diferență $499-125$, 161 omite prețul din $d-7$, iar 277 este suma celor două contribuții."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "A small SHAP share for load",
                "text": "Load has only 8.5% of the mean absolute SHapley Additive exPlanations (SHAP) value of eXtreme Gradient Boosting (XGBoost), against 32.9% for the price of $d-1$ at the same hour. Can we conclude that load does not affect the price?",
                "options": [
                    "Yes: SHAP measures the causal effect of each input on the market price",
                    "Yes, but only in the evening hours, when spikes occur",
                    "No: SHAP explains the model, not the market; load enters only with its $d-2$ value, already reflected in yesterday's price",
                    "No, because SHAP values do not add up to the forecast for tree models"
                ],
                "correctExplanation": "At gate closure load is known only up to $d-2$, so it is old news. Better inputs, such as the load and wind forecasts of the transmission system operator (TSO), would carry more information.",
                "incorrectExplanation": "SHAP values do add up exactly to the forecast (the largest gap over 8,760 test hours was 0.000009), but they describe how the model uses its inputs, not causal effects in the market."
            },
            "ro": {
                "title": "Pondere SHAP mică pentru consum",
                "text": "Consumul are doar 8,5% din media valorii absolute SHAP (explicațiile aditive bazate pe valorile Shapley, SHapley Additive exPlanations) a modelului eXtreme Gradient Boosting (XGBoost), față de 32,9% pentru prețul din $d-1$, aceeași oră. Putem concluziona că consumul nu influențează prețul?",
                "options": [
                    "Da: SHAP măsoară efectul cauzal al fiecărei variabile asupra prețului pieței",
                    "Da, dar numai în orele de seară, cînd apar vîrfurile",
                    "Nu: SHAP explică modelul, nu piața; consumul intră doar cu valoarea din $d-2$, deja reflectată în prețul de ieri",
                    "Nu, pentru că valorile SHAP nu se adună la prognoză în cazul arborilor"
                ],
                "correctExplanation": "La închiderea licitației, consumul este cunoscut doar pînă în $d-2$, deci este o informație veche. Intrări mai bune, cum ar fi prognozele de consum și de producție eoliană ale operatorului de transport și de sistem (TSO), ar aduce mai multă informație.",
                "incorrectExplanation": "Valorile SHAP se adună exact la prognoză (cea mai mare diferență pe cele 8 760 de ore de test a fost 0,000009), dar descriu modul în care modelul își folosește intrările, nu efecte cauzale în piață."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Threshold effect of wind and solar",
                "text": "The SHapley Additive exPlanations (SHAP) contribution of wind and solar generation of $d-2$ to the eXtreme Gradient Boosting (XGBoost) forecast has a correlation of −0.64 with its level. What does the chart show about the shape of the effect?",
                "options": [
                    "The effect appears above about 2 gigawatts (GW), mostly at midday, and is close to zero below: a threshold that trees learn and a linear model cannot express",
                    "The effect is a straight line: every additional gigawatt (GW) lowers the price by the same amount",
                    "The effect is positive at midday and negative at night",
                    "The effect is close to zero in every hour, since wind and solar have only 2.5% of the SHAP total"
                ],
                "correctExplanation": "The more wind and solar, the more negative the contribution, but only once generation is large. A solar developer can read here the price discount that its own output helps to create.",
                "incorrectExplanation": "A correlation of −0.64 does not imply a straight line; the relation bends at about 2 GW. A small global share is an average over all hours and hides large effects in the sunny and windy ones."
            },
            "ro": {
                "title": "Efectul de prag al regenerabilelor",
                "text": "Contribuția SHAP (explicațiile aditive bazate pe valorile Shapley, SHapley Additive exPlanations) a producției eoliene și solare din $d-2$ la prognoza modelului eXtreme Gradient Boosting (XGBoost) are corelația −0,64 cu nivelul acestei producții. Ce arată graficul despre forma efectului?",
                "options": [
                    "Efectul apare peste aproximativ 2 gigawați (GW), mai ales la prînz, și este aproape nul sub acest nivel: un prag pe care arborii îl învață, iar un model liniar nu îl poate exprima",
                    "Efectul este o linie dreaptă: fiecare gigawatt (GW) în plus scade prețul cu aceeași sumă",
                    "Efectul este pozitiv la prînz și negativ noaptea",
                    "Efectul este aproape nul în toate orele, fiindcă producția eoliană și solară are doar 2,5% din totalul SHAP"
                ],
                "correctExplanation": "Cu cît producția eoliană și solară este mai mare, cu atît contribuția este mai negativă, dar numai după ce producția devine mare. Un dezvoltator de parcuri solare poate citi aici reducerea de preț la care contribuie chiar producția sa.",
                "incorrectExplanation": "O corelație de −0,64 nu înseamnă o linie dreaptă; relația se frînge în jurul a 2 GW. O pondere globală mică este o medie pe toate orele și ascunde efecte mari în orele cu mult soare și vînt."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Permutation importance of the DNN",
                "text": "For the deep neural network (DNN), shuffling the prices of $d-1$ across test days raises the mean absolute error (MAE) by 22.82 EUR/MWh, the day of week by 3.66, load by 2.12, and wind and solar by −0.08. How should the −0.08 be read?",
                "options": [
                    "Wind and solar harm the DNN, so removing them would gain 0.08 EUR/MWh with certainty",
                    "Wind and solar are the most important inputs, since their importance is negative",
                    "The shuffling was done incorrectly, since an importance cannot be negative",
                    "Shuffling wind and solar changes the error not at all: the network does not rely on them"
                ],
                "correctExplanation": "Permutation importance is $I_b = \\text{MAE}_{b\\ \\text{shuffled}} - \\text{MAE}$, averaged over 5 permutations; a value near zero, of either sign, means that the block carries no information the network uses. The network depends on yesterday's prices even more than the trees.",
                "incorrectExplanation": "A small negative value is noise around zero, which random shuffling can produce; it is neither evidence that the input harms the model nor a sign of an error. The practical message: monitor the price feed of $d-1$ first."
            },
            "ro": {
                "title": "Importanța prin permutare (DNN)",
                "text": "Pentru rețeaua neuronală profundă (DNN), amestecarea prețurilor din $d-1$ între zilele de test crește eroarea absolută medie (MAE) cu 22,82 EUR/MWh, a zilei săptămînii cu 3,66, a consumului cu 2,12, iar a producției eoliene și solare cu −0,08. Cum trebuie citită valoarea −0,08?",
                "options": [
                    "Producția eoliană și solară dăunează rețelei DNN, deci eliminarea ei ar aduce sigur un cîștig de 0,08 EUR/MWh",
                    "Producția eoliană și solară este cea mai importantă variabilă, fiindcă importanța ei este negativă",
                    "Amestecarea a fost făcută greșit, fiindcă o importanță nu poate fi negativă",
                    "Amestecarea producției eoliene și solare nu modifică deloc eroarea: rețeaua nu se bazează pe ea"
                ],
                "correctExplanation": "Importanța prin permutare este $I_b = \\text{MAE}_{b\\ \\text{amestecat}} - \\text{MAE}$, medie pe 5 permutări; o valoare apropiată de zero, de orice semn, arată că blocul nu aduce informație folosită de rețea. Rețeaua depinde de prețurile de ieri chiar mai mult decît arborii.",
                "incorrectExplanation": "O valoare negativă mică este zgomot în jurul lui zero, pe care amestecarea aleatoare îl poate produce; nu dovedește că variabila dăunează modelului și nici nu semnalează o greșeală. Mesajul practic: monitorizați întîi fluxul prețurilor din $d-1$."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Spikes and negative prices by hour",
                "text": "A spike is an hour with a price above the 90th percentile of the hourly prices of the 12 months before the delivery month. Which statement matches the test year on the Romanian day-ahead market (PZU, Piața pentru Ziua Următoare)?",
                "options": [
                    "Exactly 10% of hours are spikes, by construction, spread evenly over the day",
                    "22.1% of hours are spikes, most frequent at 19:00, while prices at or below zero occur in 255 hours, mostly around 13:00",
                    "Spikes cluster around 13:00, when solar generation peaks, and negative prices in the evening",
                    "Spikes occur in 57.0% of all hours, and prices at or below zero on 255 days"
                ],
                "correctExplanation": "The threshold moved from 166.8 to 202.4 EUR/MWh, yet 22.1% of test hours were spikes, far more than one in ten; at 19:00, 57.0% of days had a spike. Prices at or below zero occurred in 255 hours on 53 days, near the solar peak.",
                "incorrectExplanation": "One in ten is what the definition would give only in a stable market; the threshold comes from the previous 12 months, so the share can differ widely. 57.0% is the share of days with a spike at 19:00, and 255 counts hours, not days."
            },
            "ro": {
                "title": "Vîrfuri și prețuri negative pe ore",
                "text": "Un vîrf de preț este o oră cu preț peste percentila 90 a prețurilor orare din cele 12 luni dinaintea lunii de livrare. Care afirmație descrie anul de test pe piața pentru ziua următoare (PZU)?",
                "options": [
                    "Exact 10% din ore sînt vîrfuri, prin construcție, distribuite uniform în cursul zilei",
                    "22,1% din ore sînt vîrfuri, cele mai multe la ora 19, iar prețurile mai mici sau egale cu zero apar în 255 de ore, mai ales în jurul orei 13",
                    "Vîrfurile se grupează în jurul orei 13, cînd producția solară este maximă, iar prețurile negative seara",
                    "Vîrfurile apar în 57,0% din toate orele, iar prețurile mai mici sau egale cu zero în 255 de zile"
                ],
                "correctExplanation": "Pragul s-a mișcat între 166,8 și 202,4 EUR/MWh, totuși 22,1% din orele de test au fost vîrfuri, mult peste una din zece; la ora 19, 57,0% din zile au avut un vîrf. Prețurile mai mici sau egale cu zero au apărut în 255 de ore, în 53 de zile, în jurul maximului producției solare.",
                "incorrectExplanation": "Una din zece este ponderea pe care ar da-o definiția numai pe o piață stabilă; pragul provine din cele 12 luni anterioare, deci ponderea poate fi mult diferită. 57,0% este ponderea zilelor cu vîrf la ora 19, iar 255 numără ore, nu zile."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Brier skill of XGBoost",
                "text": "On the test year, the Brier score of eXtreme Gradient Boosting (XGBoost) for spike probabilities is 0.072, against 0.172 for a constant equal to the share of spikes (spikes occur in 22.1% of test hours). By how much does XGBoost reduce the Brier score of the constant forecast?",
                "options": [
                    "About 42%",
                    "About 10%",
                    "About 58%",
                    "About 2.4%"
                ],
                "correctExplanation": "$1-0.072/0.172\\approx 0.58$, a reduction of about 58%. The constant's score is close to $p(1-p)=0.221\\times 0.779\\approx 0.172$, the Brier score of always forecasting the base rate.",
                "incorrectExplanation": "42% is the ratio of the two scores, not the reduction; 0.100 is the absolute gap, not 10% of anything, and 2.4 is how many times larger the constant's score is, not a percentage."
            },
            "ro": {
                "title": "Cîștigul Brier al XGBoost",
                "text": "Pe anul de test, scorul Brier al modelului eXtreme Gradient Boosting (XGBoost) pentru probabilitățile de vîrf este 0,072, față de 0,172 pentru o constantă egală cu ponderea vîrfurilor (vîrfurile apar în 22,1% din orele de test). Cu cît reduce XGBoost scorul Brier al prognozei constante?",
                "options": [
                    "Circa 42%",
                    "Circa 10%",
                    "Circa 58%",
                    "Circa 2,4%"
                ],
                "correctExplanation": "$1-0{,}072/0{,}172\\approx 0{,}58$, o reducere de circa 58%. Scorul constantei este apropiat de $p(1-p)=0{,}221\\times 0{,}779\\approx 0{,}172$, scorul Brier al prognozei egale mereu cu frecvența de bază.",
                "incorrectExplanation": "42% este raportul celor două scoruri, nu reducerea; 0,100 este diferența absolută, nu 10% din ceva, iar 2,4 arată de cîte ori este mai mare scorul constantei, nu un procent."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "A price forecast as spike alarm",
                "text": "On the test year, the price forecast of AW-LEAR (the Lasso-estimated autoregressive (LEAR) model averaged across calibration windows), compared with the spike threshold, has an area under the curve (AUC) of 0.959 and an F1 (harmonic mean of precision and recall) of 0.788, against 0.953 and 0.749 for a dedicated eXtreme Gradient Boosting (XGBoost) classifier. What is the practical message?",
                "options": [
                    "Buy a spike-alert service only if it beats the spike signal already hidden in your own price forecast",
                    "Dedicated classifiers are always needed, since a price forecast cannot detect spikes",
                    "AW-LEAR is also the best tool for negative prices, with an F1 of 0.788",
                    "The XGBoost classifier is useless, since its AUC is below 0.959"
                ],
                "correctExplanation": "A good price forecast already detects spikes: AW-LEAR has the highest AUC and F1 for spikes. For prices at or below zero all models do worse, and the F1 of AW-LEAR there is 0.558.",
                "incorrectExplanation": "The F1 of 0.788 refers to spikes, not to negative prices. The classifier is far from useless (Brier score 0.072, honest probabilities); the point is that a dedicated service must add something beyond your price forecast."
            },
            "ro": {
                "title": "Prognoza de preț ca alarmă",
                "text": "În anul de test, prognoza de preț a modelului AW-LEAR (modelul autoregresiv estimat cu Lasso (LEAR) mediat pe mai multe ferestre de calibrare), comparată cu pragul de vîrf, are aria de sub curbă (AUC) 0,959 și F1 (media armonică a preciziei și a sensibilității) 0,788, față de 0,953 și 0,749 pentru un clasificator dedicat eXtreme Gradient Boosting (XGBoost). Care este mesajul practic?",
                "options": [
                    "Cumpărați un serviciu de alertă pentru vîrfuri doar dacă depășește semnalul ascuns deja în prognoza dumneavoastră de preț",
                    "Clasificatorii dedicați sînt întotdeauna necesari, fiindcă o prognoză de preț nu poate detecta vîrfurile",
                    "AW-LEAR este cel mai bun instrument și pentru prețurile negative, cu F1 de 0,788",
                    "Clasificatorul XGBoost este inutil, fiindcă AUC lui este sub 0,959"
                ],
                "correctExplanation": "O prognoză bună de preț detectează deja vîrfurile: AW-LEAR are cea mai mare AUC și cel mai mare F1 la vîrfuri. La prețurile mai mici sau egale cu zero toate modelele se descurcă mai slab, iar F1 al modelului AW-LEAR este acolo 0,558.",
                "incorrectExplanation": "F1 de 0,788 se referă la vîrfuri, nu la prețurile negative. Clasificatorul nu este deloc inutil (scor Brier 0,072, probabilități corecte); ideea este că un serviciu dedicat trebuie să aducă ceva în plus față de prognoza dumneavoastră de preț."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Alert threshold when costs double",
                "text": "Under the cost–loss rule, one acts when the spike probability exceeds $C/\\bar L$. With $C = 30$ EUR/MWh and $\\bar L = 72.5$ EUR/MWh the threshold is 0.414. If moving 1 MWh costs 60 EUR instead of 30, what is the new threshold?",
                "options": [
                    "0.414",
                    "0.207",
                    "0.586",
                    "0.828"
                ],
                "correctExplanation": "$60/72.5 \\approx 0.828$: the threshold doubles, so you act only on the more certain spikes.",
                "incorrectExplanation": "The threshold is proportional to the cost of acting: a higher cost raises it, it does not halve it (0.207) or leave it unchanged (0.414). 0.586 is one minus the old threshold."
            },
            "ro": {
                "title": "Pragul de alertă la cost dublu",
                "text": "Potrivit regulii cost–pierdere, se reacționează cînd probabilitatea vîrfului depășește $C/\\bar L$. Cu $C = 30$ EUR/MWh și $\\bar L = 72{,}5$ EUR/MWh, pragul este 0,414. Dacă mutarea a 1 MWh costă 60 EUR în loc de 30, care este noul prag?",
                "options": [
                    "0,414",
                    "0,207",
                    "0,586",
                    "0,828"
                ],
                "correctExplanation": "$60/72{,}5 \\approx 0{,}828$: pragul se dublează, deci reacționați numai la vîrfurile mai sigure.",
                "incorrectExplanation": "Pragul este proporțional cu costul reacției: un cost mai mare îl ridică, nu îl înjumătățește (0,207) și nici nu îl lasă neschimbat (0,414). Valoarea 0,586 este 1 minus vechiul prag."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Value of acting on alerts",
                "text": "Per MW of flexible load and per year, acting on spike alerts at the threshold $C/\\bar L$ earns 33.0 thousand EUR, persistence 11.8 and perfect foresight 62.4. What share of the perfect-foresight value does the rule capture?",
                "options": [
                    "About 19%",
                    "About 53%",
                    "About 47%",
                    "About 64%"
                ],
                "correctExplanation": "$33.0/62.4 \\approx 0.53$, about 53%, almost three times the value of persistence. The best threshold seen afterwards (0.64) would have earned more, but it is hindsight and could not have been chosen in advance.",
                "incorrectExplanation": "19% is the share captured by persistence ($11.8/62.4$), 47% is what the rule leaves on the table, and 0.64 is the best threshold in hindsight, not a share of value."
            },
            "ro": {
                "title": "Valoarea reacției la alerte",
                "text": "Pe MW de consum flexibil și pe an, reacția la alertele de vîrf la pragul $C/\\bar L$ aduce 33,0 mii EUR, persistența 11,8, iar informația perfectă 62,4. Ce parte din valoarea informației perfecte obține regula?",
                "options": [
                    "Circa 19%",
                    "Circa 53%",
                    "Circa 47%",
                    "Circa 64%"
                ],
                "correctExplanation": "$33{,}0/62{,}4 \\approx 0{,}53$, adică circa 53%, aproape de trei ori valoarea persistenței. Cel mai bun prag văzut ulterior (0,64) ar fi adus mai mult, dar este înțelepciune retrospectivă și nu putea fi ales dinainte.",
                "incorrectExplanation": "19% este partea obținută de persistență ($11{,}8/62{,}4$), 47% este ce lasă regula neobținut, iar 0,64 este cel mai bun prag văzut ulterior, nu o parte din valoare."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Alerts in the case-study week",
                "text": "In the case-study week 27 Jun – 3 Jul 2026 there were 47 spike hours; the cost–loss rule raised 45 alerts, of which 39 were correct. What is the precision of the alerts, the share of alerts that were spikes?",
                "options": [
                    "About 83.0%",
                    "About 95.7%",
                    "About 86.7%",
                    "About 13.3%"
                ],
                "correctExplanation": "$39/45 \\approx 86.7\\%$. The alert worked, but the size of the spike was missed: on 30 Jun 2026 at 20:00 the price reached 954.59 EUR/MWh, and no model came close.",
                "incorrectExplanation": "Precision divides correct alerts by alerts; dividing by the 47 spikes gives the recall (83.0%). 45/47 compares counts of different things, and 13.3% is the share of false alarms."
            },
            "ro": {
                "title": "Alertele din săptămîna studiată",
                "text": "În săptămîna studiului de caz, 27 iunie – 3 iulie 2026, au fost 47 de ore cu vîrfuri; regula cost–pierdere a emis 45 de alerte, dintre care 39 au fost corecte. Cît este precizia alertelor, adică ponderea alertelor urmate de vîrfuri?",
                "options": [
                    "Circa 83,0%",
                    "Circa 95,7%",
                    "Circa 86,7%",
                    "Circa 13,3%"
                ],
                "correctExplanation": "$39/45 \\approx 86{,}7\\%$. Alerta a funcționat, dar amploarea vîrfului a fost ratată: la 30 iunie 2026, ora 20:00, prețul a atins 954,59 EUR/MWh, iar niciun model nu s-a apropiat de acest nivel.",
                "incorrectExplanation": "Precizia împarte alertele corecte la numărul de alerte; împărțirea la cele 47 de vîrfuri dă sensibilitatea (83,0%). 45/47 compară numere care măsoară lucruri diferite, iar 13,3% este ponderea alarmelor false."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Choosing on the test year",
                "text": "The honest deep neural network (DNN), chosen on validation with one seed, has a mean absolute error (MAE) of 23.34 EUR/MWh on the test year. The best of its 25 settings, picked directly on the test year, has 22.52, just below AW-LEAR at 22.53 (the Lasso-estimated autoregressive (LEAR) model averaged across calibration windows). What does this show?",
                "options": [
                    "An apparent victory over the benchmark, created only by choosing on the data used for evaluation",
                    "That the validation year chose the wrong setting, so validation is useless",
                    "That the DNN is as accurate as AW-LEAR and can replace it",
                    "That one seed is enough, since the two MAEs differ by less than one euro"
                ],
                "correctExplanation": "This is data snooping (White, 2000). Validation works, with Spearman correlations between validation and test MAE of 0.86 for the DNN and 0.94 for eXtreme Gradient Boosting (XGBoost), but it is not perfect, and the gap is exactly what snooping exploits.",
                "incorrectExplanation": "Rank correlations of 0.86 and 0.94 show that validation ranks settings well. The 22.52 cannot be reproduced in production, because nobody can pick a setting on data that do not yet exist; ask how many models were tried before the one presented."
            },
            "ro": {
                "title": "Alegerea pe anul de test",
                "text": "Rețeaua neuronală profundă (DNN) aleasă corect, la validare, cu o singură inițializare, are eroarea absolută medie (MAE) 23,34 EUR/MWh în anul de test. Cea mai bună dintre cele 25 de setări ale ei, aleasă direct pe anul de test, are 22,52, chiar sub AW-LEAR, cu 22,53 (modelul autoregresiv estimat cu Lasso (LEAR) mediat pe mai multe ferestre de calibrare). Ce arată acest rezultat?",
                "options": [
                    "O victorie aparentă asupra reperului, creată doar prin alegerea pe datele folosite pentru evaluare",
                    "Că anul de validare a ales setarea greșită, deci validarea este inutilă",
                    "Că rețeaua DNN este la fel de precisă ca AW-LEAR și îl poate înlocui",
                    "Că o singură inițializare este suficientă, fiindcă cele două valori MAE diferă cu mai puțin de un euro"
                ],
                "correctExplanation": "Este alegerea pe datele de test (White, 2000). Validarea funcționează, cu o corelație Spearman între MAE de validare și MAE de test de 0,86 pentru rețeaua DNN și 0,94 pentru eXtreme Gradient Boosting (XGBoost), dar nu este perfectă, iar tocmai această diferență este exploatată.",
                "incorrectExplanation": "Corelațiile de rang de 0,86 și 0,94 arată că validarea ordonează bine setările. Valoarea 22,52 nu poate fi reprodusă în producție, fiindcă nimeni nu poate alege o setare pe date care încă nu există; întrebați cîte modele au fost încercate înaintea celui prezentat."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Spurious gains among many models",
                "text": "With $m$ independent tests at the 5% level, the probability of at least one false win is $1-0.95^m$. What is it for $m = 10$ models?",
                "options": [
                    "0.050",
                    "0.599",
                    "0.500",
                    "0.401"
                ],
                "correctExplanation": "$1-0.95^{10} \\approx 1-0.599 = 0.401$; for $m = 100$ it is 0.994. This is why White's Reality Check (RC) and the superior predictive ability (SPA) test compare all models with the benchmark at once.",
                "incorrectExplanation": "0.050 is the level of a single test, and 0.599 is the probability of no false win at all. The risk grows quickly with the number of models tried, which is why one should ask how many were tried before the one presented."
            },
            "ro": {
                "title": "Cîștiguri aparente între multe modele",
                "text": "Cu $m$ teste independente la pragul de 5%, probabilitatea a cel puțin unei victorii false este $1-0{,}95^m$. Cît este ea pentru $m = 10$ modele?",
                "options": [
                    "0,050",
                    "0,599",
                    "0,500",
                    "0,401"
                ],
                "correctExplanation": "$1-0{,}95^{10} \\approx 1-0{,}599 = 0{,}401$; pentru $m = 100$ este 0,994. De aceea testul Reality Check (RC) al lui White și testul abilității predictive superioare (SPA) compară simultan toate modelele cu reperul.",
                "incorrectExplanation": "0,050 este pragul unui singur test, iar 0,599 este probabilitatea de a nu avea nicio victorie falsă. Riscul crește repede cu numărul de modele încercate; de aceea trebuie întrebat cîte modele au fost încercate înaintea celui prezentat."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Model frozen for a year",
                "text": "Fitted once before the test year, eXtreme Gradient Boosting (XGBoost) has a mean absolute error (MAE) of 24.25 EUR/MWh, 4.2% worse than with monthly refits; a 365-day rolling window gives 25.59. What is the right reading?",
                "options": [
                    "The loss is constant over the year, so a yearly refit is enough",
                    "The loss grows with time, from +0.15 EUR/MWh in the first 3 months to +3.70 in the last 3, and a short window lacks enough past spikes to learn from",
                    "The shorter the training window the better, since markets change",
                    "Monthly refits are too expensive, since each one takes several hours"
                ],
                "correctExplanation": "Markets change, so a frozen model degrades. Yet the trees need many past spikes, and one year does not contain enough of them, so a short window does worse than the whole history. A monthly refit of XGBoost takes about 13 seconds.",
                "incorrectExplanation": "The gap of the frozen model widens over the year, and a monthly refit is cheap. Put the monthly refit in the operating calendar, with an owner, like any other control."
            },
            "ro": {
                "title": "Model neactualizat un an",
                "text": "Estimat o singură dată, înaintea anului de test, modelul eXtreme Gradient Boosting (XGBoost) are eroarea absolută medie (MAE) 24,25 EUR/MWh, cu 4,2% mai slab decît cu reestimare lunară; o fereastră glisantă de 365 de zile dă 25,59. Care este interpretarea corectă?",
                "options": [
                    "Pierderea este constantă în cursul anului, deci o reestimare anuală este suficientă",
                    "Pierderea crește în timp, de la +0,15 EUR/MWh în primele 3 luni la +3,70 în ultimele 3, iar o fereastră scurtă nu conține destule vîrfuri din trecut pentru învățare",
                    "Cu cît fereastra de antrenare este mai scurtă, cu atît mai bine, fiindcă piețele se schimbă",
                    "Reestimările lunare sînt prea scumpe, fiindcă fiecare durează cîteva ore"
                ],
                "correctExplanation": "Piețele se schimbă, așa că un model neactualizat se degradează. Totuși, arborii au nevoie de multe vîrfuri din trecut, iar un singur an nu conține destule, deci o fereastră scurtă este mai slabă decît întregul istoric. O reestimare lunară a modelului XGBoost durează circa 13 secunde.",
                "incorrectExplanation": "Diferența modelului neactualizat crește în cursul anului, iar reestimarea lunară este ieftină. Includeți reestimarea lunară în calendarul operațional, cu un responsabil, ca pe orice alt control."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Same-day inputs and information leakage",
                "text": "If the load and the wind and solar generation (renewable energy sources, RES) of day $d$ are used as inputs, the mean absolute error (MAE) of eXtreme Gradient Boosting (XGBoost) falls from 23.26 to 22.55 EUR/MWh. How should this 3.1% gain be read?",
                "options": [
                    "As a genuine gain, since load and RES are fundamentals of the market",
                    "As proof that SHapley Additive exPlanations (SHAP) underestimated the role of load and RES",
                    "As look-ahead: these values are not known at 12:00 on $d-1$, and the gain is only an upper bound on what perfect forecasts of them could add",
                    "As a sign that the model should be refitted daily instead of monthly"
                ],
                "correctExplanation": "Every input must be time-stamped at gate closure. The leaked model looks better on paper, but in production the values of day $d$ do not exist at auction time; forecasts of them could recover at most this gain.",
                "incorrectExplanation": "The issue is not the relevance of load and RES but their timing. Ask every vendor for a walk-forward test with each input time-stamped at gate closure."
            },
            "ro": {
                "title": "Intrările din aceeași zi și informația din viitor",
                "text": "Dacă se folosesc drept intrări consumul și producția eoliană și solară (surse regenerabile de energie, RES) din ziua $d$, eroarea absolută medie (MAE) a modelului eXtreme Gradient Boosting (XGBoost) scade de la 23,26 la 22,55 EUR/MWh. Cum trebuie citit acest cîștig de 3,1%?",
                "options": [
                    "Ca un cîștig real, fiindcă consumul și RES sînt variabile fundamentale ale pieței",
                    "Ca o dovadă că explicațiile aditive bazate pe valorile Shapley (SHAP) au subestimat rolul consumului și al RES",
                    "Ca informație din viitor: aceste valori nu sînt cunoscute la ora 12:00 în ziua $d-1$, iar cîștigul este doar o limită superioară a ceea ce ar putea aduce prognoze perfecte ale lor",
                    "Ca un semn că modelul ar trebui reestimat zilnic, nu lunar"
                ],
                "correctExplanation": "Fiecare intrare trebuie datată la momentul închiderii licitației. Modelul cu scurgere de informație pare mai bun pe hîrtie, dar în producție valorile zilei $d$ nu există la momentul licitației; prognozele lor ar putea recupera cel mult acest cîștig.",
                "incorrectExplanation": "Problema nu este relevanța consumului și a RES, ci momentul în care sînt cunoscute. Cereți oricărui furnizor o testare cronologică, cu fiecare intrare datată la momentul închiderii licitației."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Test for information leakage",
                "text": "For the first day of each test month, all data after 12:00 on $d-1$ are replaced by 10,000 EUR/MWh and the models are refitted. Which result shows that the pipeline is clean?",
                "options": [
                    "The forecasts are unchanged: identical for the trees and the spike classifier, and within 0.001 EUR/MWh for the deep neural network (DNN)",
                    "The forecasts rise sharply, which shows that the models react to new information",
                    "The mean absolute error (MAE) on these days rises by less than 4.2%",
                    "The forecasts fall back to those of the naive model"
                ],
                "correctExplanation": "If no information from after gate closure enters the pipeline, impossible future values cannot change any forecast. The tiny DNN difference is a rounding effect of parallel arithmetic; for Chronos, the code checks that the context uses only days before day $d$.",
                "incorrectExplanation": "Any change in the forecasts would mean that future data leak into the inputs or the fit. The check belongs in every model review, for statistical and machine learning models alike."
            },
            "ro": {
                "title": "Testul privind informația din viitor",
                "text": "Pentru prima zi din fiecare lună de test, toate datele de după ora 12:00 din ziua $d-1$ sînt înlocuite cu 10 000 EUR/MWh, iar modelele sînt reestimate. Ce rezultat arată că fluxul de date este curat?",
                "options": [
                    "Prognozele nu se schimbă: sînt identice pentru arbori și pentru clasificatorul de vîrfuri, iar pentru rețeaua neuronală profundă (DNN) diferă cu mai puțin de 0,001 EUR/MWh",
                    "Prognozele cresc puternic, ceea ce arată că modelele reacționează la informația nouă",
                    "Eroarea absolută medie (MAE) din aceste zile crește cu mai puțin de 4,2%",
                    "Prognozele revin la cele ale modelului naiv"
                ],
                "correctExplanation": "Dacă nicio informație de după închiderea licitației nu intră în flux, valorile viitoare imposibile nu pot schimba nicio prognoză. Diferența minusculă a rețelei DNN vine din rotunjirile calculelor paralele; pentru Chronos, codul verifică faptul că contextul folosește numai zilele dinaintea zilei $d$.",
                "incorrectExplanation": "Orice schimbare a prognozelor ar arăta că date din viitor ajung în intrări sau în estimare. Verificarea trebuie inclusă în evaluarea oricărui model, statistic sau de învățare automată."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Four generations on 27 markets",
                "text": "In the comparison of four generations of forecasting models on electricity prices of 27 European Union (EU) countries (Andrei, Velev, Toma, Pele and Lessmann, 2024), presented at AIDA 2026, what were the ranks for Romania?",
                "options": [
                    "The autoregressive integrated moving average (ARIMA) model ranked first, ahead of all deep learning models",
                    "Chronos ranked first and PatchTST last",
                    "All the pretrained models of the fourth generation ranked in the top two",
                    "PatchTST ranked 1, TimesFM 2, Chronos 8 and the autoregressive integrated moving average (ARIMA) model 9"
                ],
                "correctExplanation": "PatchTST ranked first or second in all 27 countries. Transformers (PatchTST) and foundation models (TimesFM) lead, but the gains are model-specific, not uniform across the fourth generation.",
                "incorrectExplanation": "The pretrained models did not all lead: in Romania TimesFM ranked 2 but Chronos 8. The models were compared with walk-forward validation and ranked by a score that averages the symmetric mean absolute percentage error (SMAPE) and the root mean squared error (RMSE)."
            },
            "ro": {
                "title": "Patru generații pe 27 de piețe",
                "text": "În comparația a patru generații de modele de prognoză pe prețurile energiei electrice din 27 de țări ale Uniunii Europene (UE) (Andrei, Velev, Toma, Pele și Lessmann, 2024), prezentată la AIDA 2026, care au fost locurile pentru România?",
                "options": [
                    "Modelul autoregresiv integrat cu medie mobilă (ARIMA) a fost pe primul loc, înaintea tuturor modelelor de învățare profundă",
                    "Chronos a fost pe primul loc, iar PatchTST pe ultimul",
                    "Toate modelele preantrenate din generația a patra au fost pe primele două locuri",
                    "PatchTST pe locul 1, TimesFM pe 2, Chronos pe 8 și modelul autoregresiv integrat cu medie mobilă (ARIMA) pe 9"
                ],
                "correctExplanation": "PatchTST este pe primul sau al doilea loc în toate cele 27 de țări. Transformerele (PatchTST) și modelele fundaționale (TimesFM) conduc, dar cîștigurile depind de model și nu sînt uniforme în generația a patra.",
                "incorrectExplanation": "Nu toate modelele preantrenate au condus: în România, TimesFM a fost pe locul 2, dar Chronos pe 8. Modelele au fost comparate prin validare walk-forward și clasate după un scor care mediază eroarea procentuală absolută medie simetrică (SMAPE) și rădăcina erorii pătratice medii (RMSE)."
            }
        }
    ]
};
