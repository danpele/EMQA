// ============================================================
// EMQA course data (EN + RO). Rendered by assets/site.js.
// Lecture files: { pdf, notebook, code, codeProbe } relative to the repository root.
// A lecture is linked as soon as its PDF exists on the server (or its number is in
// READY in site.js); until then the card reads "In preparation" (status 'prep')
// or "Coming" (status 'coming').
// Strings that start with 'TODO' are facts still to be supplied by the instructor;
// the page shows them as "To be announced" / "Se va anunța".
// ============================================================
(function () {
    const REPO = 'https://github.com/danpele/EMQA';
    const COLAB = 'https://colab.research.google.com/github/danpele/EMQA/blob/main/';
    const files = n => ({
        pdf: `lectures/L${n}/lecture${n}.pdf`,
        pdf_ro: `lectures/L${n}/lecture${n}_ro.pdf`,
        notebook_ro: `notebooks/L${n}_notebook_ro.ipynb`,
        notebook: `notebooks/L${n}_notebook.ipynb`,
        code: `lectures/L${n}`,
        codeProbe: `lectures/L${n}/analysis_L${n}.py`
    });

    window.EMQA_DATA = {
        repo: REPO,
        colab: COLAB,

        // ---------------------------------------------------------------
        // UI strings
        // ---------------------------------------------------------------
        ui: {
            en: {
                pageTitle: 'Energy Markets Quantitative Analysis - Course Website',
                courseTitle: 'Energy Markets Quantitative Analysis',
                // TODO: add the faculty that runs the Energy MBA programme and the academic year
                subtitle: 'Energy MBA (Master of Business Administration) programme | Bucharest University of Economic Studies',
                nav: { home: 'Home', lectures: 'Lectures', cases: 'Case studies', data: 'Data', quizzes: 'Quizzes', resources: 'Resources', contact: 'Contact' },
                overview: 'Course Overview',
                objectives: 'Learning Objectives',
                heroTag: 'Forecasting, volatility, risk and hedging for energy companies, estimated on real Romanian and European market data with Python.',
                heroCta1: 'Explore the lectures',
                heroCta2: 'Data used in the course',
                tbd: 'To be announced',
                chapters: 'Lectures',
                chapter: 'Lecture',
                chapterShort: 'L',
                comingSoon: 'In preparation',
                comingSoonShort: 'in preparation',
                coming: 'Coming',
                chapterSoon: 'The materials of this lecture will be published before the lecture.',
                rows: { course: 'Lecture', code: 'Code' },
                links: { slides: 'Slides (PDF)', notebook: 'Notebook', code: 'Python code', colab: 'Open in Colab' },
                casesShort: 'Case studies',
                further: 'Go deeper: Rafał Weron on electricity price forecasting',
                casesTitle: 'Case Studies',
                casesIntro: 'Real episodes from the course data, used across the lectures.',
                dataTitle: 'Data',
                dataCols: ['Series', 'Frequency', 'Coverage', 'Units', 'Source'],
                dataMissing: 'Not obtained',
                quizzes: 'Self-Assessment Quizzes',
                quizIntro: 'Each attempt draws up to 20 questions at random from the lecture bank and shuffles the answers. An answer is locked once selected.',
                loginPrompt: 'Sign in with your ASE Google account (@ase.ro or @stud.ase.ro) to take the quizzes.',
                loginRequired: 'Sign in above with your ASE Google account to see this quiz.',
                loginWrongDomain: 'Please use your ASE account (@ase.ro or @stud.ase.ro).',
                saving: 'Saving your score...',
                saved: 'Your score has been recorded.',
                saveExpired: 'Your session has expired: sign out, sign in again and recalculate.',
                saveFailed: 'The score could not be saved. Please try again or tell the instructor.',
                loggedAs: 'Logged in as',
                logout: 'Logout',
                quizSoon: 'The quiz for this lecture will be published together with its materials.',
                question: 'Question',
                correct: 'Correct!',
                incorrect: 'Incorrect.',
                correctIs: 'The correct answer is',
                calc: 'Calculate Score',
                reset: 'New attempt',
                score: 'Score',
                unanswered: 'questions unanswered',
                verdicts: ['Keep practising!', 'Keep studying!', 'Good job!', 'Excellent!'],
                detailed: 'Detailed Results',
                colQ: 'Q', colQuestion: 'Question', colCorrect: 'Correct answer', colYours: 'Your answer', colResult: 'Result',
                resources: 'Resources',
                bibliography: 'Bibliography',
                abbreviations: 'Abbreviations',
                contact: 'Contact',
                instructor: 'Lecturer',
                office: 'Office Hours',
                close: 'Close',
                footer: 'Energy Markets Quantitative Analysis | Energy MBA | Bucharest University of Economic Studies'
            },
            ro: {
                pageTitle: 'Analiza cantitativă a piețelor de energie - Site-ul cursului',
                courseTitle: 'Energy Markets Quantitative Analysis',
                // TODO: add the faculty that runs the Energy MBA programme and the academic year
                subtitle: 'Analiza cantitativă a piețelor de energie | Programul Energy MBA (Master of Business Administration) | Academia de Studii Economice din București',
                nav: { home: 'Acasă', lectures: 'Cursuri', cases: 'Studii de caz', data: 'Date', quizzes: 'Quiz-uri', resources: 'Resurse', contact: 'Contact' },
                overview: 'Prezentarea cursului',
                objectives: 'Obiective de învățare',
                heroTag: 'Prognoză, volatilitate, risc și acoperirea riscului pentru companiile din energie, estimate în Python pe date reale de piață din România și din Uniunea Europeană.',
                heroCta1: 'Explorați cursurile',
                heroCta2: 'Datele cursului',
                tbd: 'Se va anunța',
                chapters: 'Cursuri',
                chapter: 'Cursul',
                chapterShort: 'C',
                comingSoon: 'În pregătire',
                comingSoonShort: 'în pregătire',
                coming: 'Urmează',
                chapterSoon: 'Materialele acestui curs vor fi publicate înainte de curs.',
                rows: { course: 'Curs', code: 'Cod' },
                links: { slides: 'Slide-uri (PDF)', notebook: 'Notebook', code: 'Cod Python', colab: 'Deschide în Colab' },
                casesShort: 'Studii de caz',
                further: 'Aprofundare: Rafał Weron despre prognoza prețului energiei electrice',
                casesTitle: 'Studii de caz',
                casesIntro: 'Episoade reale din datele cursului, folosite de-a lungul cursurilor.',
                dataTitle: 'Date',
                dataCols: ['Serie', 'Frecvență', 'Perioadă', 'Unități', 'Sursă'],
                dataMissing: 'Serii care nu au putut fi obținute',
                quizzes: 'Quiz-uri de autoevaluare',
                quizIntro: 'La fiecare încercare se extrag aleator cel mult 20 de întrebări din banca de întrebări a cursului, iar ordinea variantelor de răspuns se schimbă. Un răspuns ales nu mai poate fi modificat.',
                loginPrompt: 'Autentificați-vă cu contul Google ASE (@ase.ro sau @stud.ase.ro) pentru a rezolva quiz-urile.',
                loginRequired: 'Autentificați-vă mai sus cu contul Google ASE pentru a vedea acest quiz.',
                loginWrongDomain: 'Folosiți contul ASE (@ase.ro sau @stud.ase.ro).',
                saving: 'Se salvează scorul...',
                saved: 'Scorul a fost înregistrat.',
                saveExpired: 'Sesiunea a expirat: deconectați-vă, autentificați-vă din nou și recalculați scorul.',
                saveFailed: 'Scorul nu a putut fi salvat. Încercați din nou sau anunțați titularul de curs.',
                loggedAs: 'Autentificat ca',
                logout: 'Deconectare',
                quizSoon: 'Quiz-ul acestui curs va fi publicat odată cu materialele cursului.',
                question: 'Întrebarea',
                correct: 'Corect!',
                incorrect: 'Greșit.',
                correctIs: 'Răspunsul corect este',
                calc: 'Calculează scorul',
                reset: 'Încercare nouă',
                score: 'Scor',
                unanswered: 'întrebări fără răspuns',
                verdicts: ['Mai exersați!', 'Mai studiați!', 'Bine!', 'Excelent!'],
                detailed: 'Rezultate detaliate',
                colQ: 'Nr.', colQuestion: 'Întrebare', colCorrect: 'Răspuns corect', colYours: 'Răspunsul ales', colResult: 'Rezultat',
                resources: 'Resurse',
                bibliography: 'Bibliografie',
                abbreviations: 'Abrevieri',
                contact: 'Contact',
                instructor: 'Titular de curs',
                office: 'Program de consultații',
                close: 'Închide',
                footer: 'Analiza cantitativă a piețelor de energie | Energy MBA | Academia de Studii Economice din București'
            }
        },

        // ---------------------------------------------------------------
        // Overview cards and objectives
        // ---------------------------------------------------------------
        overview: {
            en: [
                { h: 'Course', p: ['Energy Markets Quantitative Analysis (EMQA)', 'Energy MBA (Master of Business Administration) programme, Bucharest University of Economic Studies (ASE)', 'TODO: year of study, semester, academic year 2026/2027'] },
                { h: 'Goal', p: ['Quantitative methods for decisions in energy markets: forecasting prices, measuring volatility and risk, pricing and hedging with derivatives.', 'Every method is applied to real Romanian and European Union (EU) data.'] },
                { h: 'Schedule', p: ['Seven lectures', 'TODO: dates, times and room of the seven lectures'] },
                { h: 'Assessment', p: ['TODO: components and weights of the final grade'] },
                { h: 'Tools', p: ['Python, Jupyter / Google Colab', 'GitHub: slides, notebooks, code and data'] }
            ],
            ro: [
                { h: 'Curs', p: ['Energy Markets Quantitative Analysis (EMQA) - Analiza cantitativă a piețelor de energie', 'Programul Energy MBA (Master of Business Administration), Academia de Studii Economice din București (ASE)', 'TODO: anul de studiu, semestrul, anul universitar 2026/2027'] },
                { h: 'Scop', p: ['Metode cantitative pentru decizii pe piețele de energie: prognoza prețurilor, măsurarea volatilității și a riscului, evaluarea instrumentelor derivate și acoperirea riscului.', 'Fiecare metodă se aplică pe date reale din România și din Uniunea Europeană (UE).'] },
                { h: 'Program', p: ['Șapte cursuri', 'TODO: datele, orele și sala celor șapte cursuri'] },
                { h: 'Evaluare', p: ['TODO: componentele și ponderile notei finale'] },
                { h: 'Instrumente', p: ['Python, Jupyter / Google Colab', 'GitHub: slide-uri, notebook-uri, cod și date'] }
            ]
        },

        objectives: {
            en: [
                'Read the data of energy markets: day-ahead prices, generation mix, cross-border flows, fuel and carbon prices, and the way each is recorded',
                'Forecast day-ahead electricity prices with ARX (autoregressive with exogenous variables) and LEAR (Lasso-Estimated AutoRegressive) models, combinations and probabilistic forecasts, and compare forecasts with RMSE (Root Mean Squared Error), MAE (Mean Absolute Error) and the Diebold–Mariano (DM) test',
                'Model the volatility of oil, gas and power with GARCH (Generalised AutoRegressive Conditional Heteroskedasticity) models estimated by maximum likelihood',
                'Measure the risk of an energy company with Value-at-Risk (VaR), Expected Shortfall (ES) and Cash-Flow-at-Risk (CFaR), and backtest the estimates',
                'Price futures, forwards and options on futures, choose a hedge ratio and value a power purchase agreement (PPA)',
                'Measure how renewables change prices: capture prices, cannibalisation, negative prices and the value of a battery',
                'Build and evaluate machine-learning and foundation-model forecasts of electricity prices, as point forecasts, as probabilistic forecasts and by the profit of a trading decision'
            ],
            ro: [
                'Citirea datelor piețelor de energie: prețuri pentru ziua următoare, mixul de producție, fluxuri transfrontaliere, prețuri ale combustibililor și ale certificatelor de emisii, precum și modul în care este înregistrată fiecare serie',
                'Prognoza prețurilor energiei electrice pentru ziua următoare cu modele ARX (autoregresive cu variabile exogene) și LEAR (Lasso-Estimated AutoRegressive), combinații și prognoze probabilistice, cu compararea prognozelor prin RMSE (rădăcina erorii pătratice medii), MAE (eroarea absolută medie) și testul Diebold–Mariano (DM)',
                'Modelarea volatilității țițeiului, gazului și energiei electrice cu modele GARCH (Generalised AutoRegressive Conditional Heteroskedasticity), estimate prin metoda verosimilității maxime',
                'Măsurarea riscului unei companii din energie cu Value-at-Risk (VaR), Expected Shortfall (ES) și Cash-Flow-at-Risk (CFaR) și testarea retrospectivă (backtesting) a estimărilor',
                'Evaluarea contractelor futures și forward și a opțiunilor pe futures, alegerea raportului de acoperire și evaluarea unui contract de achiziție de energie (PPA, Power Purchase Agreement)',
                'Măsurarea efectului surselor regenerabile asupra prețurilor: prețul capturat, canibalizarea, prețurile negative și valoarea unei baterii',
                'Construirea și evaluarea prognozelor de preț al energiei electrice obținute cu învățare automată și cu modele fundație, ca prognoze punctuale, ca prognoze probabilistice și prin profitul unei decizii de tranzacționare'
            ]
        },

        // ---------------------------------------------------------------
        // Lectures 1-7. `id` is the stable key (quizzes, anchors, tabs).
        // ---------------------------------------------------------------
        lectures: [
            {
                id: 'l1', num: 1, status: 'prep', files: files(1),
                title: { en: 'Energy markets and their data', ro: 'Piețele de energie și datele lor' },
                topics: {
                    en: ['The Romanian generation mix and the day-ahead markets of Romania (OPCOM PZU, Piața pentru Ziua Următoare), Bulgaria, Hungary and Germany–Luxembourg; 15-minute market time units (MTU) since October 2025', 'Daily and yearly price profiles, price spikes and negative prices', 'Stylised facts: heavy tails, volatility clustering, autocorrelation; white noise, autoregressive processes and the random walk; decomposition and smoothing'],
                    ro: ['Mixul de producție al României și piețele pentru ziua următoare din România (OPCOM PZU, Piața pentru Ziua Următoare), Bulgaria, Ungaria și Germania–Luxemburg; intervale de decontare de 15 minute (MTU, market time unit) din octombrie 2025', 'Profilul zilnic și anual al prețurilor, salturi de preț și prețuri negative', 'Fapte stilizate: cozi groase, gruparea volatilității, autocorelație; zgomot alb, procese autoregresive și mersul aleator; descompunere și netezire']
                },
                cases: ['iran', 'hydro', 'coupling', 'negative']
            },
            {
                id: 'l2', num: 2, status: 'prep', files: files(2),
                title: { en: 'Forecasting day-ahead electricity prices', ro: 'Prognoza prețurilor pentru ziua următoare' },
                topics: {
                    en: ['The forecasting problem: what is known at 12:00 CET on day d−1, when the day-ahead auction fixes the 96 prices of day d; naive benchmarks', 'Expert models: ARX (autoregressive with exogenous variables) and LEAR (Lasso-Estimated AutoRegressive)', 'Calibration windows, forecast combinations, evaluation with MAE (Mean Absolute Error), RMSE (Root Mean Squared Error) and the Diebold–Mariano (DM) test', 'Probabilistic forecasts by quantile regression averaging (QRA); cointegration'],
                    ro: ['Problema de prognoză: ce se știe la ora 12:00 CET în ziua d−1, cînd licitația PZU fixează cele 96 de prețuri ale zilei d; modele de referință naive', 'Modele expert: ARX (autoregresiv cu variabile exogene) și LEAR (Lasso-Estimated AutoRegressive)', 'Ferestre de calibrare, combinarea prognozelor, evaluarea prin MAE (eroarea absolută medie), RMSE (rădăcina erorii pătratice medii) și testul Diebold–Mariano (DM)', 'Prognoze probabilistice prin media regresiilor cuantilice (QRA, quantile regression averaging); cointegrare']
                }
            },
            {
                id: 'l3', num: 3, status: 'prep', files: files(3),
                title: { en: 'Volatility', ro: 'Volatilitate' },
                topics: {
                    en: ['Measuring volatility in energy markets; intraday volatility from hourly prices', 'The GARCH (Generalised AutoRegressive Conditional Heteroskedasticity) family, including asymmetric EGARCH and GJR models, estimated by maximum likelihood', 'Volatility regimes and the 2021–2022 energy crisis; forecasting and evaluating volatility'],
                    ro: ['Măsurarea volatilității pe piețele de energie; volatilitatea intrazilnică, din prețurile orare', 'Familia GARCH (Generalised AutoRegressive Conditional Heteroskedasticity), inclusiv modelele asimetrice EGARCH și GJR, estimate prin metoda verosimilității maxime', 'Regimuri de volatilitate și criza energetică din 2021–2022; prognoza și evaluarea volatilității']
                }
            },
            {
                id: 'l4', num: 4, status: 'prep', files: files(4),
                title: { en: 'Risk for energy companies', ro: 'Riscul companiilor din energie' },
                topics: {
                    en: ['Value-at-Risk (VaR) and Expected Shortfall (ES) by four methods: historical simulation, filtered historical simulation, parametric models and extreme value theory (EVT)', 'Backtesting: the Kupiec and Christoffersen tests for VaR, the Acerbi–Székely test for ES', 'From quantiles to margins, guarantees and limits; Cash-Flow-at-Risk (CFaR) for a supplier and a producer'],
                    ro: ['Value-at-Risk (VaR) și Expected Shortfall (ES) prin patru metode: simulare istorică, simulare istorică filtrată, modele parametrice și teoria valorilor extreme (EVT, extreme value theory)', 'Testarea retrospectivă: testele Kupiec și Christoffersen pentru VaR, testul Acerbi–Székely pentru ES', 'De la cuantile la marje, garanții și limite; Cash-Flow-at-Risk (CFaR) pentru un furnizor și un producător']
                }
            },
            {
                id: 'l5', num: 5, status: 'prep', files: files(5),
                title: { en: 'Derivatives and hedging', ro: 'Instrumente derivate și acoperirea riscului' },
                topics: {
                    en: ['Why hedge: exposures and the lesson of the 2021–2022 crisis', 'Forwards, futures and the forward curve; spark and dark spreads, including the cost of EU Allowances (EUA)', 'Hedge ratio, basis risk and shape risk; options on energy futures with the Black-76 model; power purchase agreements (PPA)'],
                    ro: ['De ce acoperim riscul: expuneri și lecția crizei din 2021–2022', 'Contracte forward, futures și curba forward; marjele centralelor (spark spread și dark spread), inclusiv costul certificatelor de emisii (EUA, EU Allowance)', 'Raportul de acoperire, riscul de bază și riscul de profil; opțiuni pe futures pe energie cu modelul Black-76; contracte de achiziție de energie (PPA, Power Purchase Agreement)']
                }
            },
            {
                id: 'l6', num: 6, status: 'prep', files: files(6),
                title: { en: 'Renewables, negative prices and batteries', ro: 'Surse regenerabile, prețuri negative și baterii' },
                topics: {
                    en: ['Renewables and the merit order', 'Capture prices and cannibalisation; negative prices', 'The intraday price shape and the economics of a battery'],
                    ro: ['Sursele regenerabile și ordinea de merit', 'Prețul capturat și canibalizarea; prețurile negative', 'Profilul zilnic al prețurilor și economia unei baterii']
                },
                cases: ['battery', 'negative']
            },
            {
                id: 'l7', num: 7, status: 'prep', files: files(7),
                title: { en: 'Machine learning and foundation models for electricity price forecasting', ro: 'Învățare automată și modele fundație pentru prognoza prețului energiei electrice' },
                topics: {
                    en: ['Electricity price forecasting (EPF) following the work of Rafał Weron: LEAR as the benchmark, deep neural networks (DNN) and gradient boosting', 'The Chronos foundation model for time series, zero-shot; forecast combinations and explanations with SHAP (SHapley Additive exPlanations)', 'Price spikes and negative prices; pitfalls that make a model look better than it is'],
                    ro: ['Prognoza prețului energiei electrice (EPF, electricity price forecasting) după lucrările lui Rafał Weron: LEAR ca reper, rețele neuronale profunde (DNN) și gradient boosting', 'Modelul fundație Chronos pentru serii de timp, fără antrenare; combinarea prognozelor și explicarea lor cu SHAP (SHapley Additive exPlanations)', 'Vîrfuri de preț și prețuri negative; capcanele care fac un model să pară mai bun decît este']
                },
                further: [
                    { url: 'https://www.ai4efin.ase.ro/?p=3464', en: 'Keynote “Machine learning for electricity price forecasting”, AIDA (AI and Digital Assets in Energy and Finance) Conference, ASE Bucharest, 3–5 June 2026', ro: 'Prelegerea „Machine learning for electricity price forecasting”, Conferința AIDA (AI and Digital Assets in Energy and Finance), ASE București, 3–5 iunie 2026' },
                    { url: 'https://p.wz.pwr.edu.pl/~weron.rafal/Conf/IIF24', en: 'International Institute of Forecasters (IIF) Distinguished Lectures on electricity price forecasting: slides and videos', ro: 'Prelegerile IIF (International Institute of Forecasters) Distinguished Lectures despre prognoza prețului energiei electrice: slide-uri și înregistrări' }
                ]
            }
        ],

        // ---------------------------------------------------------------
        // Case studies used across the lectures
        // ---------------------------------------------------------------
        cases: [
            { id: 'iran',
              en: { h: 'Israel–Iran war, June 2025', p: ['Oil and gas prices around the June 2025 war between Israel and Iran: how fast Brent and gas react to a supply threat, and how fast they fall back.'] },
              ro: { h: 'Războiul Israel–Iran, iunie 2025', p: ['Prețurile țițeiului și gazului în jurul războiului dintre Israel și Iran din iunie 2025: cît de repede reacționează Brent și gazul la o amenințare asupra ofertei și cît de repede revin.'] } },
            { id: 'hydro',
              en: { h: 'Romanian hydro: wet 2023, dry 2025', p: ['Hydropower output in a wet year and in a dry year, and what the difference means for Romanian prices, imports and the share price of Hidroelectrica.'] },
              ro: { h: 'Hidrocentralele din România: 2023 umed, 2025 secetos', p: ['Producția hidro într-un an umed și într-un an secetos și efectul diferenței asupra prețurilor din România, a importurilor și a prețului acțiunilor Hidroelectrica.'] } },
            { id: 'nuclear',
              en: { h: 'Cernavodă nuclear plant', p: ['Romania’s baseload nuclear output, followed in the generation data and in the share price of Nuclearelectrica, the operator of the plant.'] },
              ro: { h: 'Centrala nucleară Cernavodă', p: ['Producția nucleară de bază a României, urmărită în datele de producție și în prețul acțiunilor Nuclearelectrica, operatorul centralei.'] } },
            { id: 'battery',
              en: { h: 'Battery storage', p: ['A battery that charges in cheap hours and discharges in expensive ones: the value of a price forecast measured in euros rather than in forecast errors.'] },
              ro: { h: 'Stocarea în baterii', p: ['O baterie care se încarcă în orele ieftine și se descarcă în cele scumpe: valoarea unei prognoze de preț măsurată în euro, nu în erori de prognoză.'] } },
            { id: 'coupling',
              en: { h: 'Price coupling and separation: Romania, Bulgaria, Hungary, summer 2024', p: ['When the three coupled zones clear at the same price and when the interconnectors fill up and prices separate, with the summer of 2024 as the main episode.'] },
              ro: { h: 'Cuplarea și separarea prețurilor: România, Bulgaria, Ungaria, vara 2024', p: ['Cînd cele trei zone cuplate au același preț și cînd interconexiunile se saturează și prețurile se separă, cu vara anului 2024 ca episod principal.'] } },
            { id: 'negative',
              en: { h: 'Negative prices', p: ['Hours, and since October 2025 quarter-hours, with prices below zero: when they occur, how often, and why they break log transforms and naive models.'] },
              ro: { h: 'Prețuri negative', p: ['Ore, iar din octombrie 2025 sferturi de oră, cu prețuri sub zero: cînd apar, cît de des și de ce nu funcționează logaritmarea și modelele naive.'] } },
            { id: 'ytd2026',
              en: { h: '2026 year to date', p: ['The current year as an out-of-sample test: models estimated on earlier years are checked against the 2026 data as they come in.'] },
              ro: { h: 'Anul 2026 pînă în prezent', p: ['Anul curent ca test în afara eșantionului: modelele estimate pe anii anteriori sînt verificate pe datele din 2026, pe măsură ce apar.'] } }
        ],

        // ---------------------------------------------------------------
        // Data: transcribed from data/SOURCES.md (generated by data/download_all.py, 4 Nov 2026)
        // ---------------------------------------------------------------
        data: {
            intro: {
                en: 'All series are downloaded by the script <code>data/download_all.py</code> from the public source listed; nothing is interpolated and gaps are left as gaps. Intraday power timestamps are in UTC (Coordinated Universal Time, start of the interval); daily power averages use the Central European calendar day (CET/CEST) for every zone; market data use exchange trading dates. Full details: <a href="' + REPO + '/blob/main/data/SOURCES.md" target="_blank" rel="noopener">data/SOURCES.md</a>.',
                ro: 'Toate seriile sînt descărcate de scriptul <code>data/download_all.py</code> din sursa publică indicată; nu se interpolează nimic, iar lipsurile rămîn lipsuri. Momentele de timp ale datelor intrazilnice de energie electrică sînt în UTC (Coordinated Universal Time, începutul intervalului); mediile zilnice folosesc ziua calendaristică a Europei Centrale (CET/CEST) pentru toate zonele; datele de piață folosesc zilele de tranzacționare ale bursei. Detalii complete: <a href="' + REPO + '/blob/main/data/SOURCES.md" target="_blank" rel="noopener">data/SOURCES.md</a>.'
            },
            series: [
                { name: { en: 'Day-ahead prices: Romania (OPCOM PZU), Bulgaria (IBEX), Hungary (HUPX), Germany–Luxembourg (EPEX SPOT)', ro: 'Prețuri pentru ziua următoare: România (OPCOM PZU), Bulgaria (IBEX), Ungaria (HUPX), Germania–Luxemburg (EPEX SPOT)' },
                  file: 'power_da_prices_native_utc.csv', freq: { en: 'hourly; 15-min from 2025-10-01', ro: 'orar; 15 min din 2025-10-01' }, coverage: { en: '2015-01-01 – 2026-11-05 (BG from 2016-10-31)', ro: '2015-01-01 – 2026-11-05 (BG din 2016-10-31)' }, units: 'EUR/MWh',
                  source: 'energy-charts.info (Fraunhofer ISE)', href: 'https://api.energy-charts.info/',
                  note: { en: 'Re-publication of exchange data and of ENTSO-E (European Network of Transmission System Operators for Electricity) data; a few missing days left missing; DE-AT-LU zone until 2018-09-30.', ro: 'Republicare a datelor bursiere și a datelor ENTSO-E (European Network of Transmission System Operators for Electricity); cîteva zile lipsă rămîn lipsă; zona DE-AT-LU pînă la 2018-09-30.' } },
                { name: { en: 'Daily base price, same four zones', ro: 'Prețul zilnic de bază, aceleași patru zone' },
                  file: 'power_da_prices_daily_cet.csv', freq: { en: 'daily (CET day)', ro: 'zilnic (ziua CET)' }, coverage: '2015-01-01 – 2026-11-05', units: 'EUR/MWh',
                  source: 'energy-charts.info', href: 'https://api.energy-charts.info/',
                  note: { en: 'Mean of all MTUs of the day, with counts of MTUs and of negative MTUs.', ro: 'Media tuturor intervalelor zilei, cu numărul de intervale și de intervale cu preț negativ.' } },
                { name: { en: 'Romania: net generation by source and load', ro: 'România: producția netă pe surse și consumul' },
                  file: 'generation_ro_mw_daily_cet.csv', freq: { en: 'hourly (UTC) and daily (CET)', ro: 'orar (UTC) și zilnic (CET)' }, coverage: '2015-01-04 – 2026-11-04', units: { en: 'MW (mean)', ro: 'MW (medie)' },
                  source: 'energy-charts.info', href: 'https://api.energy-charts.info/public_power?country=ro',
                  note: { en: 'From ENTSO-E actual generation per type: nuclear, hydro, lignite, coal, gas, wind, solar.', ro: 'Din producția efectivă pe tipuri raportată la ENTSO-E: nuclear, hidro, lignit, cărbune, gaz, eolian, solar.' } },
                { name: { en: 'Bulgaria: nuclear generation and load', ro: 'Bulgaria: producția nucleară și consumul' },
                  file: 'generation_bg_mw_daily_cet.csv', freq: { en: 'hourly (UTC) and daily (CET)', ro: 'orar (UTC) și zilnic (CET)' }, coverage: '2015-01-01 – 2026-11-04', units: { en: 'MW (mean)', ro: 'MW (medie)' },
                  source: 'energy-charts.info', href: 'https://api.energy-charts.info/public_power?country=bg' },
                { name: { en: 'Romania: cross-border physical flows by neighbour', ro: 'România: fluxuri fizice transfrontaliere pe vecini' },
                  file: 'crossborder_ro_mw_daily_cet.csv', freq: { en: 'hourly (UTC) and daily (CET)', ro: 'orar (UTC) și zilnic (CET)' }, coverage: '2015-01-01 – 2026-11-05', units: { en: 'MW (mean)', ro: 'MW (medie)' },
                  source: 'energy-charts.info', href: 'https://api.energy-charts.info/cbet?country=ro',
                  note: { en: 'Positive = net import into Romania; Moldova and Ukraine borders only partly reported.', ro: 'Pozitiv = import net în România; granițele cu Moldova și Ucraina sînt raportate doar parțial.' } },
                { name: { en: 'Brent and WTI (West Texas Intermediate) crude oil, front month', ro: 'Țiței Brent și WTI (West Texas Intermediate), contractul cel mai apropiat' },
                  file: 'fuels_daily.csv', freq: { en: 'daily (trading days)', ro: 'zilnic (zile de tranzacționare)' }, coverage: '2015-01-02 – 2026-11-04', units: 'USD/bbl',
                  source: 'Yahoo Finance (BZ=F, CL=F)', href: 'https://finance.yahoo.com/quote/BZ=F',
                  note: { en: 'Continuous front month, affected by rolls; WTI includes the negative settlement of 2020-04-20.', ro: 'Serie continuă a contractului cel mai apropiat, afectată de rostogoliri; WTI include prețul negativ din 2020-04-20.' } },
                { name: { en: 'Henry Hub natural gas, RBOB (Reformulated Blendstock for Oxygenate Blending) gasoline, heating oil (ULSD, Ultra-Low Sulphur Diesel), front month', ro: 'Gaz natural Henry Hub, benzină RBOB (Reformulated Blendstock for Oxygenate Blending), motorină de încălzire (ULSD, Ultra-Low Sulphur Diesel), contractul cel mai apropiat' },
                  file: 'fuels_daily.csv', freq: { en: 'daily', ro: 'zilnic' }, coverage: '2015-01-02 – 2026-11-04', units: 'USD/MMBtu; USD/gal',
                  source: 'Yahoo Finance (NG=F, RB=F, HO=F)', href: 'https://finance.yahoo.com/quote/NG=F' },
                { name: { en: 'EUR/USD reference rate of the European Central Bank (ECB)', ro: 'Cursul de referință EUR/USD al Băncii Centrale Europene (BCE)' },
                  file: 'fuels_daily.csv', freq: { en: 'daily (TARGET days)', ro: 'zilnic (zile TARGET)' }, coverage: '2015-01-02 – 2026-11-04', units: { en: 'USD per EUR', ro: 'USD pentru 1 EUR' },
                  source: 'ECB Data Portal', href: 'https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A' },
                { name: { en: 'Dutch TTF (Title Transfer Facility) natural gas, monthly average', ro: 'Gaz natural TTF (Title Transfer Facility, Olanda), medie lunară' },
                  file: 'ttf_monthly.csv', freq: { en: 'monthly', ro: 'lunar' }, coverage: '2015-01 – 2026-10', units: 'USD/MMBtu; EUR/MWh',
                  source: 'World Bank, Commodity Markets (“Natural gas, Europe”)', href: 'https://www.worldbank.org/en/research/commodity-markets',
                  note: { en: 'Daily TTF is not freely available; EUR/MWh is a unit conversion, not a market quote.', ro: 'TTF zilnic nu este disponibil gratuit; valoarea în EUR/MWh este o conversie de unități, nu o cotație de piață.' } },
                { name: { en: 'EU Allowance (EUA): EEX (European Energy Exchange) primary auction clearing price', ro: 'Certificate de emisii EUA: prețul de adjudecare la licitațiile primare EEX (European Energy Exchange)' },
                  file: 'eua_daily.csv', freq: { en: 'auction days (3–4 per week)', ro: 'zile de licitație (3–4 pe săptămînă)' }, coverage: '2015-01-08 – 2025-12-15', units: 'EUR/tCO2',
                  source: 'EEX auction reports', href: 'https://www.eex.com/en/markets/environmental-markets/eu-ets-auctions',
                  note: { en: 'The 2026 file is not published as a static download, so the series ends in December 2025.', ro: 'Fișierul pentru 2026 nu este publicat ca descărcare statică, așa că seria se oprește în decembrie 2025.' } },
                { name: { en: 'SparkChange Physical Carbon EUA ETC (exchange-traded commodity), London: CO2, as a proxy for the EUA price', ro: 'SparkChange Physical Carbon EUA ETC (exchange-traded commodity), Londra: CO2, ca aproximare a prețului EUA' },
                  file: 'eua_daily.csv', freq: { en: 'daily', ro: 'zilnic' }, coverage: '2021-10-18 – 2026-11-04', units: { en: 'EUR per unit', ro: 'EUR pe unitate' },
                  source: 'Yahoo Finance (CO2.L)', href: 'https://finance.yahoo.com/quote/CO2.L',
                  note: { en: 'Backed by physical allowances; follows the EUA spot price less fees and covers 2026.', ro: 'Garantat cu certificate fizice; urmează prețul spot EUA minus comisioane și acoperă anul 2026.' } },
                { name: { en: 'Romanian energy shares on the Bucharest Stock Exchange (BVB): Hidroelectrica (H2O), Nuclearelectrica (SNN), OMV Petrom (SNP), Romgaz (SNG)', ro: 'Acțiuni ale companiilor românești de energie la Bursa de Valori București (BVB): Hidroelectrica (H2O), Nuclearelectrica (SNN), OMV Petrom (SNP), Romgaz (SNG)' },
                  file: 'ro_energy_equities_daily.csv', freq: { en: 'daily', ro: 'zilnic' }, coverage: { en: '2015-01-01 – 2026-11-04 (H2O from 2023-07-12)', ro: '2015-01-01 – 2026-11-04 (H2O din 2023-07-12)' }, units: 'RON',
                  source: 'EODHD', href: 'https://eodhd.com/',
                  note: { en: 'Close and dividend/split-adjusted close.', ro: 'Preț de închidere și preț de închidere ajustat pentru dividende și divizări.' } }
            ],
            missing: [
                { name: 'TTF daily (TTF=F)', en: 'Yahoo Finance returned no usable history.', ro: 'Yahoo Finance nu a returnat un istoric utilizabil.' },
                { name: 'ENTSO-E Transparency Platform', en: 'No access token available; energy-charts.info was used instead.', ro: 'Nu a fost disponibil un token de acces; s-a folosit energy-charts.info.' },
                { name: 'AGSI+ gas storage', en: 'Aggregated Gas Storage Inventory: the API (application programming interface) requires a key; not downloaded.', ro: 'Aggregated Gas Storage Inventory: API-ul (interfața de programare) cere o cheie; nu a fost descărcat.' },
                { name: 'EEX German power futures (front calendar year)', en: 'No free public series; not downloaded.', ro: 'Nu există o serie publică gratuită; nu a fost descărcată.' }
            ],
            licence: {
                en: 'Licences: energy-charts.info price data are for private and internal (teaching) use; its generation data are under CC BY 4.0 (Creative Commons Attribution). Yahoo Finance and EODHD data are for personal and educational use.',
                ro: 'Licențe: datele de preț de pe energy-charts.info sînt pentru uz privat și intern (didactic); datele de producție sînt sub licența CC BY 4.0 (Creative Commons Attribution). Datele Yahoo Finance și EODHD sînt pentru uz personal și educațional.'
            }
        },

        // ---------------------------------------------------------------
        // Resources
        // ---------------------------------------------------------------
        resources: [
            { icon: '&#128187;', href: REPO, en: ['GitHub repository', 'Slides, notebooks, code and data scripts'], ro: ['Repository GitHub', 'Slide-uri, notebook-uri, cod și scripturile pentru date'] },
            { icon: '&#9889;', href: 'https://www.energy-charts.info/', en: ['Energy-Charts', 'Fraunhofer ISE: prices, generation and flows for European bidding zones'], ro: ['Energy-Charts', 'Fraunhofer ISE: prețuri, producție și fluxuri pentru zonele de ofertare europene'] },
            { icon: '&#128202;', href: 'https://www.opcom.ro', en: ['OPCOM', 'The Romanian power and gas exchange'], ro: ['OPCOM', 'Bursa română de energie electrică și gaze naturale'] },
            { icon: '&#128190;', img: 'assets/logos/ql_logo.png', href: 'https://quantlet.com', en: ['Quantlet', 'Reproducible code, starting with EMQA_stationarity'], ro: ['Quantlet', 'Cod reproductibil, începînd cu EMQA_stationarity'] },
            { icon: '&#127891;', img: 'assets/logos/qr_logo.png', href: 'https://quantinar.com', en: ['Quantinar', 'P2P (peer-to-peer) platform with advanced courses'], ro: ['Quantinar', 'Platformă P2P (peer-to-peer) cu cursuri avansate'] }
        ],

        bibliography: [
            'Weron, R. (2014). <a href="https://doi.org/10.1016/j.ijforecast.2014.08.008" target="_blank" rel="noopener">Electricity price forecasting: A review of the state-of-the-art with a look into the future</a>. <em>International Journal of Forecasting</em>, 30(4), 1030–1081.',
            'Lago, J., Marcjasz, G., De Schutter, B., &amp; Weron, R. (2021). <a href="https://doi.org/10.1016/j.apenergy.2021.116983" target="_blank" rel="noopener">Forecasting day-ahead electricity prices: A review of state-of-the-art algorithms, best practices and an open-access benchmark</a>. <em>Applied Energy</em>, 293, 116983.',
            'Nowotarski, J., &amp; Weron, R. (2018). <a href="https://doi.org/10.1016/j.rser.2017.05.234" target="_blank" rel="noopener">Recent advances in electricity price forecasting: A review of probabilistic forecasting</a>. <em>Renewable and Sustainable Energy Reviews</em>, 81, 1548–1568.',
            'Weron, R. (2006). <a href="https://doi.org/10.1002/9781118673362" target="_blank" rel="noopener"><em>Modeling and Forecasting Electricity Loads and Prices: A Statistical Approach</em></a>. Wiley.',
            'Hyndman, R. J., &amp; Athanasopoulos, G. (2021). <a href="https://otexts.com/fpp3/" target="_blank" rel="noopener"><em>Forecasting: Principles and Practice</em></a> (3rd ed.). OTexts.',
            'Diebold, F. X., &amp; Mariano, R. S. (1995). <a href="https://doi.org/10.1080/07350015.1995.10524599" target="_blank" rel="noopener">Comparing predictive accuracy</a>. <em>Journal of Business &amp; Economic Statistics</em>, 13(3), 253–263.',
            'Bollerslev, T. (1986). <a href="https://doi.org/10.1016/0304-4076(86)90063-1" target="_blank" rel="noopener">Generalized autoregressive conditional heteroskedasticity</a>. <em>Journal of Econometrics</em>, 31(3), 307–327.',
            'Black, F. (1976). <a href="https://doi.org/10.1016/0304-405X(76)90024-6" target="_blank" rel="noopener">The pricing of commodity contracts</a>. <em>Journal of Financial Economics</em>, 3(1–2), 167–179.',
            'Ansari, A. F., et al. (2024). <a href="https://arxiv.org/abs/2403.07815" target="_blank" rel="noopener">Chronos: Learning the language of time series</a>. <em>Transactions on Machine Learning Research</em>.',
            'Hollmann, N., et al. (2025). <a href="https://doi.org/10.1038/s41586-024-08328-6" target="_blank" rel="noopener">Accurate predictions on small data with a tabular foundation model</a>. <em>Nature</em>, 637, 319–326.'
        ],

        // acronym, English, Romanian (when different)
        abbreviations: [
            ['ARIMA / SARIMA', 'AutoRegressive Integrated Moving Average / Seasonal ARIMA'],
            ['ASE', 'Bucharest University of Economic Studies (Academia de Studii Economice din București)', 'Academia de Studii Economice din București'],
            ['BVB', 'Bucharest Stock Exchange (Bursa de Valori București)', 'Bursa de Valori București'],
            ['CET / CEST', 'Central European (Summer) Time', 'Ora Europei Centrale (de vară)'],
            ['CFaR', 'Cash-Flow-at-Risk'],
            ['DM', 'Diebold–Mariano test', 'testul Diebold–Mariano'],
            ['EPF', 'Electricity Price Forecasting', 'prognoza prețului energiei electrice'],
            ['ES', 'Expected Shortfall'],
            ['EU ETS / EUA', 'EU Emissions Trading System / EU Allowance (one tonne of CO2)', 'Sistemul UE de comercializare a certificatelor de emisii / certificat de emisii (o tonă de CO2)'],
            ['GARCH', 'Generalised AutoRegressive Conditional Heteroskedasticity'],
            ['IBEX / HUPX / EPEX SPOT', 'Independent Bulgarian Energy Exchange / Hungarian Power Exchange / European Power Exchange'],
            ['LEAR', 'Lasso-Estimated AutoRegressive model', 'model autoregresiv estimat cu Lasso'],
            ['MAE / RMSE', 'Mean Absolute Error / Root Mean Squared Error', 'eroarea absolută medie / rădăcina erorii pătratice medii'],
            ['MBA', 'Master of Business Administration'],
            ['MTU', 'Market Time Unit', 'intervalul de decontare al pieței (market time unit)'],
            ['OPCOM PZU', 'Romanian power exchange, Day-Ahead Market (Piața pentru Ziua Următoare)', 'Operatorul pieței de energie, Piața pentru Ziua Următoare'],
            ['PPA', 'Power Purchase Agreement', 'contract de achiziție de energie'],
            ['TTF', 'Title Transfer Facility (Dutch gas hub)', 'Title Transfer Facility (hub-ul olandez de gaze)'],
            ['VaR', 'Value-at-Risk']
        ],

        contact: {
            name: 'Prof. dr. Daniel Traian Pele',
            email: 'danpele@ase.ro',
            en: ['Bucharest University of Economic Studies', 'Department of Statistics and Econometrics', 'Faculty of Cybernetics, Statistics and Economic Informatics', 'Romanian Academy, Institute for Economic Forecasting'],
            ro: ['Academia de Studii Economice din București', 'Departamentul de Statistică și Econometrie', 'Facultatea de Cibernetică, Statistică și Informatică Economică', 'Academia Română, Institutul de Prognoză Economică'],
            office: { en: 'TODO: office hours', ro: 'TODO: program de consultații' }
        },

        footerLogos: [
            ['https://www.ase.ro', 'assets/logos/ase_logo.png', 'ASE'],
            ['https://ipe.ro/new/', 'assets/logos/acad_logo.png', 'Romanian Academy, Institute for Economic Forecasting'],
            ['https://www.theida.net/', 'assets/logos/ida_logo.png', 'IDA'],
            ['https://ai4efin.ase.ro', 'assets/logos/ai4efin_logo.png', 'AI4EFin'],
            ['https://www.digital-finance-msca.com/', 'assets/logos/msca_logo.png', 'MSCA Digital Finance'],
            ['https://quantlet.com', 'assets/logos/ql_logo.png', 'Quantlet'],
            ['https://quantinar.com', 'assets/logos/qr_logo.png', 'Quantinar'],
            ['https://blockchain-research-center.com/', 'assets/logos/brc_logo.png', 'Blockchain Research Center']
        ],

        // Quiz banks register themselves here by lecture id (format: see the QUIZ ENGINE comment in site.js)
        // TODO: no quiz content yet; whether quiz scores count toward the grade is still to be decided
        quizzes: {}
    };
})();
