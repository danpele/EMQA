// ============================================================
// Quiz bank for lecture id 'l3': Volatility (EN + RO)
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.EMQA_DATA.quizzes['l3'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 2,
            "en": {
                "title": "Annualising power volatility",
                "text": "After the weekly calendar is removed, the daily shocks of the Romanian day-ahead price (Piața pentru Ziua Următoare, PZU) have a standard deviation of 20.0% per day. Power has an auction every day of the year. Which annualised volatility does the lecture report?",
                "options": [
                    "About 318%, scaling by $\\sqrt{252}$ as for traded assets",
                    "About 69%, scaling by $\\sqrt{12}$ as for monthly data",
                    "About 382%, scaling by $\\sqrt{365}$",
                    "About 7,300%, multiplying by the 365 days of the year"
                ],
                "correctExplanation": "$\\sigma_{\\text{year}}=\\hat\\sigma\\sqrt{A}=20.0\\times\\sqrt{365}\\approx 382$%. Power is auctioned every day, so $A$ = 365; traded assets use 252. The lecture compares these 382% with 42% for Brent.",
                "incorrectExplanation": "Volatility grows with the square root of time, not linearly, and the number of observations per year depends on the market: 365 daily auctions for power, 252 trading days for exchange-traded assets."
            },
            "ro": {
                "title": "Anualizarea volatilității energiei",
                "text": "După eliminarea efectului zilei din săptămînă, șocurile zilnice ale prețului de pe Piața pentru Ziua Următoare (PZU) din România au o abatere standard de 20,0% pe zi. Pentru energia electrică licitația are loc în fiecare zi a anului. Ce volatilitate anualizată raportează cursul?",
                "options": [
                    "Circa 318%, cu scalarea prin $\\sqrt{252}$, ca la activele bursiere",
                    "Circa 69%, cu scalarea prin $\\sqrt{12}$, ca la datele lunare",
                    "Circa 382%, cu scalarea prin $\\sqrt{365}$",
                    "Circa 7 300%, înmulțind cu cele 365 de zile ale anului"
                ],
                "correctExplanation": "$\\sigma_{\\text{an}}=\\hat\\sigma\\sqrt{A}=20{,}0\\times\\sqrt{365}\\approx 382$%. Licitația pentru energie are loc zilnic, deci $A$ = 365; pentru activele bursiere se folosește 252. Cursul compară acești 382% cu 42% pentru Brent.",
                "incorrectExplanation": "Volatilitatea crește cu rădăcina pătrată a timpului, nu liniar, iar numărul de observații pe an depinde de piață: 365 de licitații zilnice pentru energie, 252 de zile de tranzacționare pentru activele bursiere."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Removing the weekly calendar",
                "text": "The mean equation, with seven lags and weekday dummies, explains half of the daily variance of the Romanian price change ($R^2$ = 0.50). Before it, the standard deviation is 28.3% per day. What standard deviation is left for the shock $\\varepsilon_t$?",
                "options": [
                    "About 20.0%, since $28.3\\times\\sqrt{0.5}\\approx 20.0$",
                    "About 14.2%, half of 28.3%",
                    "About 28.3%, because the calendar does not change volatility",
                    "About 24.5%, because only the Monday effect is removed"
                ],
                "correctExplanation": "Halving the variance multiplies the standard deviation by $\\sqrt{0.5}\\approx 0.71$: 28.3% becomes 20.0%, the value in the lecture. All volatility models are then fitted to this shock, never to the raw change.",
                "incorrectExplanation": "$R^2$ is a share of variance, not of standard deviation. Removing half of the variance removes only about 29% of the standard deviation, which takes 28.3% down to 20.0%."
            },
            "ro": {
                "title": "Eliminarea calendarului săptămînal",
                "text": "Ecuația mediei, cu șapte decalaje și variabile pentru zilele săptămînii, explică jumătate din varianța zilnică a variației prețului din România ($R^2$ = 0,50). Înainte de ea, abaterea standard este de 28,3% pe zi. Ce abatere standard rămîne pentru șocul $\\varepsilon_t$?",
                "options": [
                    "Circa 20,0%, deoarece $28{,}3\\times\\sqrt{0{,}5}\\approx 20{,}0$",
                    "Circa 14,2%, jumătate din 28,3%",
                    "Circa 28,3%, deoarece calendarul nu modifică volatilitatea",
                    "Circa 24,5%, deoarece se elimină doar efectul zilei de luni"
                ],
                "correctExplanation": "Înjumătățirea varianței înmulțește abaterea standard cu $\\sqrt{0{,}5}\\approx 0{,}71$: 28,3% devine 20,0%, valoarea din curs. Toate modelele de volatilitate se aplică apoi acestui șoc, niciodată variației brute.",
                "incorrectExplanation": "$R^2$ este o pondere din varianță, nu din abaterea standard. Eliminarea a jumătate din varianță reduce abaterea standard doar cu circa 29%, de la 28,3% la 20,0%."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "A Monday price jump",
                "text": "The price on the day-ahead market (Piața pentru Ziua Următoare, PZU) rises by 35% from Sunday to Monday. What should the risk desk do?",
                "options": [
                    "Widen the limits at once, since a 35% move is a large shock",
                    "Hedge the Monday jump with a contract bought on the previous Friday",
                    "Treat the move as the start of a turbulent regime and review collateral",
                    "Nothing special: Monday is on average about 38% above Sunday, so the shock is almost zero"
                ],
                "correctExplanation": "The weekly calendar is known in advance and is forecast by the mean equation. Only the shock $\\varepsilon_t$, here almost zero, enters the volatility model. A Monday jump is to be forecast, not hedged.",
                "incorrectExplanation": "Demand is lower at weekends, so the price falls on Saturday and Sunday and jumps back on Monday, by about +38% on average. A predictable move is not a risk signal."
            },
            "ro": {
                "title": "Creșterea prețului de luni",
                "text": "Prețul de pe Piața pentru Ziua Următoare (PZU) crește cu 35% de duminică pînă luni. Ce trebuie să facă departamentul de risc?",
                "options": [
                    "Să lărgească imediat limitele, deoarece o variație de 35% este un șoc mare",
                    "Să acopere creșterea de luni cu un contract cumpărat vinerea precedentă",
                    "Să trateze variația ca începutul unui regim agitat și să revizuiască garanțiile",
                    "Nimic special: în medie, prețul de luni este cu circa 38% mai mare decît cel de duminică, deci șocul este aproape zero"
                ],
                "correctExplanation": "Calendarul săptămînal este cunoscut dinainte și este inclus în ecuația mediei. În modelul de volatilitate intră doar șocul $\\varepsilon_t$, aici aproape zero. Creșterea de luni trebuie prognozată, nu acoperită.",
                "incorrectExplanation": "Cererea este mai mică la sfîrșit de săptămînă, astfel că prețul scade sîmbăta și duminica și crește din nou luni, în medie cu circa 38%. O variație previzibilă nu este un semnal de risc."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Sign versus size",
                "text": "The Ljung–Box statistic $Q(10)$ is 13.8 for the shocks $\\varepsilon_t$ ($p$ = 0.18) and 120.0 for the squared shocks $\\varepsilon_t^2$, against a 5% critical value of 18.31. What does this mean for tomorrow's price move?",
                "options": [
                    "Both its direction and its size can be predicted from today's data",
                    "Its direction cannot be predicted, but its size can",
                    "Its direction can be predicted, but its size is purely random",
                    "Neither can be predicted, since the shocks are independent"
                ],
                "correctExplanation": "The shocks show no autocorrelation, but their squares do: this is volatility clustering. The Lagrange multiplier test for autoregressive conditional heteroskedasticity (ARCH-LM) with 10 lags confirms it, with 93.7 and $p\\lt 0.001$.",
                "incorrectExplanation": "Only the squared shocks exceed the critical value. The sign of a shock behaves like a fair coin, while large shocks are followed by large shocks."
            },
            "ro": {
                "title": "Semnul și mărimea șocului",
                "text": "Statistica Ljung–Box $Q(10)$ are valoarea 13,8 pentru șocurile $\\varepsilon_t$ ($p$ = 0,18) și 120,0 pentru pătratele lor $\\varepsilon_t^2$, față de valoarea critică de 18,31 la pragul de 5%. Ce înseamnă aceasta pentru variația de mîine a prețului?",
                "options": [
                    "Atît direcția, cît și mărimea ei pot fi prevăzute pe baza datelor de azi",
                    "Direcția ei nu poate fi prevăzută, dar mărimea ei da",
                    "Direcția ei poate fi prevăzută, dar mărimea este pur aleatoare",
                    "Nici direcția, nici mărimea nu pot fi prevăzute, deoarece șocurile sînt independente"
                ],
                "correctExplanation": "Șocurile nu sînt autocorelate, dar pătratele lor sînt: aceasta este gruparea volatilității. Testul multiplicatorului Lagrange pentru heteroscedasticitate condiționată autoregresivă (ARCH-LM), cu 10 decalaje, o confirmă: 93,7, cu $p\\lt 0{,}001$.",
                "incorrectExplanation": "Doar pătratele șocurilor depășesc valoarea critică. Semnul unui șoc se comportă ca o monedă corectă, în timp ce șocurile mari sînt urmate de șocuri mari."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Fat tails in numbers",
                "text": "The shocks of the Romanian day-ahead price have an excess kurtosis of 20.0 and a skewness of −1.69. How many shocks lie beyond 4 standard deviations, and how many would the normal law predict?",
                "options": [
                    "15 observed against about 15 expected",
                    "15 observed against 0.18 expected",
                    "189 observed against 0.18 expected",
                    "4 observed against about 3 expected"
                ],
                "correctExplanation": "There are 15 such shocks against 0.18 expected under normality. This is why every model of the lecture uses Student-t shocks; the fitted Student-t density has $\\nu$ = 4.3 degrees of freedom.",
                "incorrectExplanation": "189 is the number of raw daily changes above 50% in absolute value, a different statistic. The normal law has zero excess kurtosis and almost never produces 4-standard-deviation days."
            },
            "ro": {
                "title": "Cozile groase în cifre",
                "text": "Șocurile prețului pentru ziua următoare din România au un exces de aplatizare (*kurtosis*) de 20,0 și o asimetrie de −1,69. Cîte șocuri se află dincolo de 4 abateri standard și cîte ar prevedea legea normală?",
                "options": [
                    "15 observate, față de circa 15 așteptate",
                    "15 observate, față de 0,18 așteptate",
                    "189 observate, față de 0,18 așteptate",
                    "4 observate, față de circa 3 așteptate"
                ],
                "correctExplanation": "Există 15 asemenea șocuri, față de 0,18 cîte ar fi de așteptat în ipoteza normalității. De aceea toate modelele din curs folosesc șocuri de tip Student; densitatea Student estimată are $\\nu$ = 4,3 grade de libertate.",
                "incorrectExplanation": "189 este numărul variațiilor zilnice brute care depășesc 50% în valoare absolută, o altă statistică. Legea normală are excesul de aplatizare zero și aproape niciodată nu produce zile de 4 abateri standard."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The crisis in two units",
                "text": "In percent, the standard deviation of the shocks was 18.7% in 2019 and 18.5% in 2022. In euro per megawatt-hour (EUR/MWh) it was 11.2 and 45.8, a ratio of 4.1. What explains the difference?",
                "options": [
                    "Percent volatility is mismeasured in crisis years and should be discarded",
                    "The weekly calendar was much stronger in 2022 than in 2019",
                    "Negative prices in 2022 inflated the changes in EUR/MWh",
                    "The mean price rose from 50 to 265 EUR/MWh, so the same relative move cost about four times more"
                ],
                "correctExplanation": "Both statements are correct and answer different questions: percent volatility gives the relative size of moves, EUR/MWh volatility the money a one-megawatt-hour position gains or loses. During the crisis each move cost about four times more.",
                "incorrectExplanation": "The relative size of moves did not change in the crisis; the price level did. Margin calls are paid in euro, so collateral rose with the price level although percent volatility did not."
            },
            "ro": {
                "title": "Criza în două unități",
                "text": "În procente, abaterea standard a șocurilor a fost de 18,7% în 2019 și de 18,5% în 2022. În euro pe megawatt-oră (EUR/MWh) a fost de 11,2 și de 45,8, un raport de 4,1. Ce explică diferența?",
                "options": [
                    "Volatilitatea procentuală este măsurată greșit în anii de criză și trebuie ignorată",
                    "Efectul zilei din săptămînă a fost mult mai puternic în 2022 decît în 2019",
                    "Prețurile negative din 2022 au umflat variațiile în EUR/MWh",
                    "Prețul mediu a crescut de la 50 la 265 EUR/MWh, deci aceeași variație relativă a costat de circa patru ori mai mult"
                ],
                "correctExplanation": "Ambele afirmații sînt corecte, dar răspund la întrebări diferite: volatilitatea procentuală descrie mărimea relativă a variațiilor, iar cea în EUR/MWh suma pe care o cîștigă sau o pierde o poziție de un megawatt-oră. În criză, fiecare variație a costat de circa patru ori mai mult.",
                "incorrectExplanation": "În criză nu s-a schimbat mărimea relativă a variațiilor, ci nivelul prețului. Apelurile în marjă se plătesc în euro, așa că garanțiile au crescut odată cu nivelul prețului, deși volatilitatea procentuală nu a crescut."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Prices near zero",
                "text": "In the Germany–Luxembourg (DE-LU) bidding zone, one daily move from 0.95 to 92.91 euro per megawatt-hour (EUR/MWh) gave a log change $r_t$ of 458%. What does the lecture conclude?",
                "options": [
                    "Switch to the inverse hyperbolic sine, which solves the near-zero problem",
                    "Drop from the sample all days with a base price below 10 EUR/MWh",
                    "Use percent changes only far from zero, and measure hourly prices only in EUR/MWh",
                    "Treat the 458% move as a genuine risk that the limits must cover"
                ],
                "correctExplanation": "Near zero ordinary moves become huge percentages with no economic meaning. A position is in MWh, so its risk is in EUR/MWh; the lecture uses $r_t$ and $\\Delta P_t$ for the daily base price and only EUR/MWh for hourly prices, which can be negative.",
                "incorrectExplanation": "The inverse hyperbolic sine allows negative prices but explodes near zero just like the logarithm, so it does not solve the problem; dropping days would discard real data."
            },
            "ro": {
                "title": "Prețuri lîngă zero",
                "text": "În zona de ofertare Germania–Luxemburg (DE-LU), o trecere de la 0,95 la 92,91 euro pe megawatt-oră (EUR/MWh) de la o zi la alta a dat o variație logaritmică $r_t$ de 458%. Ce concluzie trage cursul?",
                "options": [
                    "Trecem la sinusul hiperbolic invers, care rezolvă problema prețurilor apropiate de zero",
                    "Eliminăm din eșantion toate zilele cu prețul de bază sub 10 EUR/MWh",
                    "Folosim variațiile procentuale doar departe de zero, iar prețurile orare le măsurăm numai în EUR/MWh",
                    "Tratăm variația de 458% ca pe un risc real, pe care limitele trebuie să-l acopere"
                ],
                "correctExplanation": "Lîngă zero, variații obișnuite devin procente uriașe, fără sens economic. O poziție se măsoară în MWh, deci riscul ei este în EUR/MWh; cursul folosește $r_t$ și $\\Delta P_t$ pentru prețul de bază și numai EUR/MWh pentru prețurile orare, care pot fi negative.",
                "incorrectExplanation": "Sinusul hiperbolic invers permite prețuri negative, dar explodează lîngă zero la fel ca logaritmul, deci nu rezolvă problema; eliminarea zilelor ar arunca date reale."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Power desk versus oil desk",
                "text": "Over 2019–2026 the annualised volatility of the shocks is 382% for Romanian power and 42% for Brent crude oil. A group runs both a power desk and an oil desk. What is the right lesson?",
                "options": [
                    "Use the same percent limit on both desks, adjusted only for position size",
                    "Power is riskier than oil only during the 2021–2022 crisis",
                    "The gap disappears once the weekly calendar is removed",
                    "Never compare their limits in the same percent: power is about 9 times more volatile than oil"
                ],
                "correctExplanation": "382% against 42% is a factor of about 9, and power is several hundred percent a year in every year of the table. Limits expressed in the same percent would be meaningless across the two desks.",
                "incorrectExplanation": "The 382% is already measured after removing the weekly calendar, and the yearly table shows power at several hundred percent in calm years as well as in the crisis."
            },
            "ro": {
                "title": "Energie electrică față de petrol",
                "text": "În 2019–2026, volatilitatea anualizată a șocurilor este de 382% pentru energia electrică din România și de 42% pentru țițeiul Brent. Un grup are un birou de tranzacționare a energiei electrice și unul de petrol. Care este lecția corectă?",
                "options": [
                    "Aceeași limită procentuală pentru ambele birouri, ajustată doar după mărimea poziției",
                    "Energia electrică este mai riscantă decît petrolul doar în criza din 2021–2022",
                    "Diferența dispare după eliminarea efectului zilei din săptămînă",
                    "Limitele lor nu se compară în același procent: energia electrică este de circa 9 ori mai volatilă decît petrolul"
                ],
                "correctExplanation": "382% față de 42% înseamnă un factor de circa 9, iar energia electrică are cîteva sute de procente pe an în fiecare an din tabel. Limite exprimate în același procent nu ar avea sens pentru cele două birouri.",
                "incorrectExplanation": "Cele 382% sînt deja calculate după eliminarea efectului calendarului, iar tabelul anual arată cîteva sute de procente pentru energie atît în anii calmi, cît și în criză."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Reading GARCH parameters",
                "text": "On the Romanian shocks in percent, the generalised autoregressive conditional heteroskedasticity model GARCH(1,1) with Student-t shocks gives $\\hat\\alpha$ = 0.308 and $\\hat\\beta$ = 0.438; on the shocks in euro per megawatt-hour (EUR/MWh) it gives $\\hat\\alpha$ = 0.102 and $\\hat\\beta$ = 0.892. Which reading is correct?",
                "options": [
                    "In percent volatility reacts less and remembers longer than in EUR/MWh",
                    "In percent volatility reacts strongly and forgets quickly; in EUR/MWh it reacts less and remembers long",
                    "Both units give the same dynamics, since they describe the same price",
                    "In EUR/MWh volatility is explosive, since $\\hat\\alpha+\\hat\\beta$ exceeds 1"
                ],
                "correctExplanation": "$\\alpha$ is the reaction to yesterday's shock and $\\beta$ the memory of yesterday's variance. Persistence is 0.746 in percent and 0.994 in EUR/MWh, below 1 in both cases.",
                "incorrectExplanation": "A large $\\alpha$ and a small $\\alpha+\\beta$ mean a strong but short reaction (percent); a small $\\alpha$ with $\\alpha+\\beta$ close to 1 means a weak but long-lasting one (EUR/MWh)."
            },
            "ro": {
                "title": "Interpretarea parametrilor GARCH",
                "text": "Pe șocurile procentuale din România, modelul cu heteroscedasticitate condiționată autoregresivă generalizată GARCH(1,1) cu șocuri Student dă $\\hat\\alpha$ = 0,308 și $\\hat\\beta$ = 0,438; pe șocurile în euro pe megawatt-oră (EUR/MWh) dă $\\hat\\alpha$ = 0,102 și $\\hat\\beta$ = 0,892. Care interpretare este corectă?",
                "options": [
                    "În procente, volatilitatea reacționează mai puțin și își amintește mai mult decît în EUR/MWh",
                    "În procente, volatilitatea reacționează puternic și uită repede; în EUR/MWh reacționează mai puțin, dar își amintește mult timp",
                    "Ambele unități dau aceeași dinamică, deoarece descriu același preț",
                    "În EUR/MWh volatilitatea este explozivă, deoarece $\\hat\\alpha+\\hat\\beta$ depășește 1"
                ],
                "correctExplanation": "$\\alpha$ este reacția la șocul de ieri, iar $\\beta$ memoria varianței de ieri. Persistența este 0,746 în procente și 0,994 în EUR/MWh, sub 1 în ambele cazuri.",
                "incorrectExplanation": "Un $\\alpha$ mare și o sumă $\\alpha+\\beta$ mică înseamnă o reacție puternică, dar scurtă (procente); un $\\alpha$ mic și o sumă $\\alpha+\\beta$ apropiată de 1 înseamnă o reacție slabă, dar de durată (EUR/MWh)."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Long-run volatility",
                "text": "For the generalised autoregressive conditional heteroskedasticity model GARCH(1,1) with Student-t shocks, in percent, $\\hat\\omega$ = 105.677 and $\\hat\\alpha+\\hat\\beta$ = 0.746. What long-run daily volatility $\\bar\\sigma$ does this imply?",
                "options": [
                    "About 20.4% per day",
                    "About 10.3% per day",
                    "About 141.7% per day",
                    "About 416% per day"
                ],
                "correctExplanation": "$\\bar\\sigma^2=\\omega/(1-\\alpha-\\beta)=105.677/0.254\\approx 416$, so $\\bar\\sigma\\approx 20.4$% per day, the value reported in the lecture.",
                "incorrectExplanation": "The long-run variance divides $\\omega$ by one minus the persistence, and the volatility is its square root; 416 is a variance, not a volatility."
            },
            "ro": {
                "title": "Volatilitatea de lungă durată",
                "text": "Pentru modelul cu heteroscedasticitate condiționată autoregresivă generalizată GARCH(1,1) cu șocuri Student, în procente, $\\hat\\omega$ = 105,677 și $\\hat\\alpha+\\hat\\beta$ = 0,746. Ce volatilitate zilnică de lungă durată $\\bar\\sigma$ rezultă?",
                "options": [
                    "Circa 20,4% pe zi",
                    "Circa 10,3% pe zi",
                    "Circa 141,7% pe zi",
                    "Circa 416% pe zi"
                ],
                "correctExplanation": "$\\bar\\sigma^2=\\omega/(1-\\alpha-\\beta)=105{,}677/0{,}254\\approx 416$, deci $\\bar\\sigma\\approx 20{,}4$% pe zi, valoarea raportată în curs.",
                "incorrectExplanation": "Varianța de lungă durată se obține împărțind $\\omega$ la unu minus persistența, iar volatilitatea este rădăcina ei pătrată; 416 este o varianță, nu o volatilitate."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Student-t versus normal",
                "text": "For GARCH(1,1) (generalised autoregressive conditional heteroskedasticity) in percent, normal shocks give persistence 0.927 and a half-life of 9.2 days; Student-t shocks give 0.746 and 2.4 days, with a Bayesian information criterion (BIC) of 24,220.8 against 24,744.5. What is the consequence for a risk desk?",
                "options": [
                    "Prefer the normal model: its higher persistence is more prudent",
                    "The two models are equivalent, since both persistences are below 1",
                    "Use Student-t shocks: the normal model treats every holiday as the start of a lasting turbulent period and keeps limits wide too long",
                    "Prefer the normal model, since a higher BIC means a better fit"
                ],
                "correctExplanation": "A lower BIC is better, and the Student model wins clearly. It accepts that some days are simply extreme, so it does not turn each holiday into a long turbulent period.",
                "incorrectExplanation": "BIC is better when lower. The high persistence of the normal model is an artefact of fat tails, not prudence: it keeps limits wide for 9.2 days instead of 2.4."
            },
            "ro": {
                "title": "Șocuri Student sau normale",
                "text": "Pentru GARCH(1,1) (heteroscedasticitate condiționată autoregresivă generalizată) în procente, șocurile normale dau persistența 0,927 și un timp de înjumătățire de 9,2 zile; șocurile Student dau 0,746 și 2,4 zile, cu un criteriu informațional bayesian (BIC) de 24 220,8 față de 24 744,5. Ce consecință are aceasta pentru departamentul de risc?",
                "options": [
                    "Preferă modelul normal: persistența lui mai mare este mai prudentă",
                    "Cele două modele sînt echivalente, deoarece ambele persistențe sînt sub 1",
                    "Folosește șocuri Student: modelul normal tratează fiecare sărbătoare ca începutul unei perioade agitate de durată și menține limitele largi prea mult timp",
                    "Preferă modelul normal, deoarece un BIC mai mare înseamnă o ajustare mai bună"
                ],
                "correctExplanation": "Un BIC mai mic înseamnă un model mai bun, iar modelul Student cîștigă detașat. El acceptă că unele zile sînt pur și simplu extreme, deci nu transformă fiecare sărbătoare într-o perioadă agitată lungă.",
                "incorrectExplanation": "BIC este mai bun cînd este mai mic. Persistența mare a modelului normal provine din cozile groase, nu din prudență: limitele rămîn largi 9,2 zile în loc de 2,4."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Half-life of Brent shocks",
                "text": "For Brent crude oil, the generalised autoregressive conditional heteroskedasticity model GARCH(1,1) with Student-t shocks gives $\\hat\\alpha+\\hat\\beta$ = 0.973. Using $h_{1/2}=\\ln 0.5/\\ln(\\alpha+\\beta)$, after how long is half of the extra variance created by a shock gone?",
                "options": [
                    "About 2.4 trading days",
                    "About 37 trading days",
                    "About 25.6 trading days, roughly 5 weeks",
                    "About 83 trading days, roughly 17 weeks"
                ],
                "correctExplanation": "$\\ln 0.5/\\ln 0.973=-0.693/-0.0274\\approx 25.6$ trading days, about 5 weeks. This answers Lecture 1: after an oil shock, keep wider limits for weeks, not days.",
                "incorrectExplanation": "$1/(1-0.973)\\approx 37$ is not the half-life; the formula uses logarithms. 2.4 days is the percent half-life of Romanian power and 83 days that of the carbon allowance."
            },
            "ro": {
                "title": "Înjumătățirea șocurilor Brent",
                "text": "Pentru țițeiul Brent, modelul cu heteroscedasticitate condiționată autoregresivă generalizată GARCH(1,1) cu șocuri Student dă $\\hat\\alpha+\\hat\\beta$ = 0,973. Folosind $h_{1/2}=\\ln 0{,}5/\\ln(\\alpha+\\beta)$, după cît timp dispare jumătate din varianța suplimentară creată de un șoc?",
                "options": [
                    "Circa 2,4 zile lucrătoare",
                    "Circa 37 de zile lucrătoare",
                    "Circa 25,6 zile lucrătoare, adică aproximativ 5 săptămîni",
                    "Circa 83 de zile lucrătoare, adică aproximativ 17 săptămîni"
                ],
                "correctExplanation": "$\\ln 0{,}5/\\ln 0{,}973=-0{,}693/-0{,}0274\\approx 25{,}6$ zile lucrătoare, circa 5 săptămîni. Este răspunsul la întrebarea din cursul 1: după un șoc pe piața petrolului, limitele rămîn mai largi săptămîni întregi, nu cîteva zile.",
                "incorrectExplanation": "$1/(1-0{,}973)\\approx 37$ nu este timpul de înjumătățire; formula folosește logaritmi. 2,4 zile este timpul de înjumătățire procentual al energiei electrice din România, iar 83 de zile cel al certificatelor de emisii."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Half-life of OMV Petrom",
                "text": "For OMV Petrom shares, the generalised autoregressive conditional heteroskedasticity model GARCH(1,1) with Student-t shocks gives a persistence $\\hat\\alpha+\\hat\\beta$ = 0.934. What is the half-life of a volatility shock?",
                "options": [
                    "About 10.2 trading days",
                    "About 5.5 trading days",
                    "About 15.2 trading days",
                    "About 0.9 trading days"
                ],
                "correctExplanation": "$h_{1/2}=\\ln 0.5/\\ln 0.934=-0.693/-0.068\\approx 10.2$ trading days: OMV Petrom sits between Romanian power in percent (2.4 days) and Brent (25.6 days).",
                "incorrectExplanation": "The half-life is $\\ln 0.5/\\ln(\\alpha+\\beta)$, not $1/(1-\\alpha-\\beta)$, which gives about 15.2; 5.5 days is the value for Hungarian power in percent."
            },
            "ro": {
                "title": "Înjumătățirea la OMV Petrom",
                "text": "Pentru acțiunile OMV Petrom, modelul cu heteroscedasticitate condiționată autoregresivă generalizată GARCH(1,1) cu șocuri Student dă persistența $\\hat\\alpha+\\hat\\beta$ = 0,934. Care este timpul de înjumătățire al unui șoc de volatilitate?",
                "options": [
                    "Circa 10,2 zile lucrătoare",
                    "Circa 5,5 zile lucrătoare",
                    "Circa 15,2 zile lucrătoare",
                    "Circa 0,9 zile lucrătoare"
                ],
                "correctExplanation": "$h_{1/2}=\\ln 0{,}5/\\ln 0{,}934=-0{,}693/-0{,}068\\approx 10{,}2$ zile lucrătoare: OMV Petrom se află între energia electrică din România în procente (2,4 zile) și Brent (25,6 zile).",
                "incorrectExplanation": "Timpul de înjumătățire este $\\ln 0{,}5/\\ln(\\alpha+\\beta)$, nu $1/(1-\\alpha-\\beta)$, care ar da circa 15,2; 5,5 zile este valoarea pentru energia electrică din Ungaria, în procente."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Sensitivity near one",
                "text": "Persistence rises from 0.973 for Brent to 0.992 for the European Union (EU) emission allowance (EUA). What happens to the half-life of a volatility shock?",
                "options": [
                    "It rises by about 2%, in line with the persistence",
                    "It more than triples, from about 26 to about 83 trading days",
                    "It doubles, from about 26 to about 52 trading days",
                    "It falls, because the EUA sample starts only in October 2021"
                ],
                "correctExplanation": "$\\ln 0.5/\\ln 0.992\\approx 82.8$ trading days against 25.6: the half-life is very sensitive to persistence near 1. For the EUA, wider limits should stay about 17 weeks.",
                "incorrectExplanation": "Near 1, $\\ln(\\alpha+\\beta)$ is almost $-(1-\\alpha-\\beta)$, so the half-life scales with $1/(1-\\alpha-\\beta)$: from 0.027 to 0.008 the gap shrinks more than three times."
            },
            "ro": {
                "title": "Sensibilitatea lîngă 1",
                "text": "Persistența crește de la 0,973 pentru Brent la 0,992 pentru certificatul de emisii al Uniunii Europene (UE), EU Allowance (EUA). Ce se întîmplă cu timpul de înjumătățire al unui șoc de volatilitate?",
                "options": [
                    "Crește cu circa 2%, la fel ca persistența",
                    "Devine de peste trei ori mai mare, de la circa 26 la circa 83 de zile lucrătoare",
                    "Se dublează, de la circa 26 la circa 52 de zile lucrătoare",
                    "Scade, deoarece seria EUA începe abia în octombrie 2021"
                ],
                "correctExplanation": "$\\ln 0{,}5/\\ln 0{,}992\\approx 82{,}8$ zile lucrătoare, față de 25,6: timpul de înjumătățire este foarte sensibil la persistență cînd aceasta se apropie de 1. Pentru EUA, limitele mai largi trebuie menținute circa 17 săptămîni.",
                "incorrectExplanation": "Lîngă 1, $\\ln(\\alpha+\\beta)$ este aproape $-(1-\\alpha-\\beta)$, deci timpul de înjumătățire variază ca $1/(1-\\alpha-\\beta)$: de la 0,027 la 0,008 distanța față de 1 scade de peste trei ori."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Mixing regimes",
                "text": "Over the whole 2019–2026 sample, the half-life of a shock in euro per megawatt-hour (EUR/MWh) from the generalised autoregressive conditional heteroskedasticity model GARCH(1,1)-t is 113.5 days, but re-estimated on 2023 – October 2026 it is only 9.1 days. Why?",
                "options": [
                    "The post-crisis sample is too short to estimate persistence reliably",
                    "Shocks in EUR/MWh truly last about four months in every period",
                    "Solar generation shortened the memory of volatility after 2023",
                    "A model fitted across calm and crisis regimes mistakes the switches for long memory and overstates persistence"
                ],
                "correctExplanation": "In 2019–2020 a shock halves in under a day (0.4), in the crisis persistence reaches 1.000 (infinite half-life), after it 9.1 days. Mixing these regimes overstates persistence (Lamoureux & Lastrapes, 1990), so re-estimate after a regime change.",
                "incorrectExplanation": "The sub-period estimates differ dramatically: the long memory of the full sample comes from the switch between calm and crisis, not from each shock lasting months."
            },
            "ro": {
                "title": "Amestecarea regimurilor",
                "text": "Pe întreaga perioadă 2019–2026, timpul de înjumătățire al unui șoc în euro pe megawatt-oră (EUR/MWh) dat de modelul cu heteroscedasticitate condiționată autoregresivă generalizată GARCH(1,1)-t este de 113,5 zile, dar reestimat pe 2023 – octombrie 2026 este de doar 9,1 zile. De ce?",
                "options": [
                    "Eșantionul de după criză este prea scurt pentru a estima corect persistența",
                    "Șocurile în EUR/MWh durează într-adevăr circa patru luni în orice perioadă",
                    "Producția solară a scurtat memoria volatilității după 2023",
                    "Un model estimat peste regimuri calme și de criză confundă trecerile dintre ele cu o memorie lungă și supraestimează persistența"
                ],
                "correctExplanation": "În 2019–2020 un șoc se înjumătățește în mai puțin de o zi (0,4), în criză persistența ajunge la 1,000 (timp de înjumătățire infinit), iar după criză la 9,1 zile. Amestecarea regimurilor supraestimează persistența (Lamoureux & Lastrapes, 1990), de aceea modelul se reestimează după o schimbare de regim.",
                "incorrectExplanation": "Estimările pe subperioade diferă spectaculos: memoria lungă din eșantionul complet vine din trecerea de la calm la criză, nu din faptul că fiecare șoc ar dura luni întregi."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Inverse leverage effect",
                "text": "On the shocks in euro per megawatt-hour (EUR/MWh), the Glosten–Jagannathan–Runkle (GJR) model gives $\\hat\\gamma$ = −0.127 ($t$ = −6.4) and the exponential generalised autoregressive conditional heteroskedasticity (EGARCH) model gives $\\hat\\gamma$ = 0.104 ($t$ = 7.2). What do they say?",
                "options": [
                    "Falls raise volatility more, the leverage effect known from shares",
                    "Rises and falls have the same effect, since the estimates are not significant",
                    "The two models contradict each other, since their signs differ",
                    "Rises raise volatility more, the inverse leverage effect typical of commodities"
                ],
                "correctExplanation": "In GJR a negative $\\gamma$ means rises raise volatility more; in EGARCH the sign convention is the opposite, so a positive $\\gamma$ says the same. Both are clearly significant (Knittel & Roberts, 2005).",
                "incorrectExplanation": "The two models use opposite sign conventions for $\\gamma$, so different signs here tell the same story; with $|t|$ above 6 the asymmetry is significant."
            },
            "ro": {
                "title": "Efectul de levier invers",
                "text": "Pe șocurile în euro pe megawatt-oră (EUR/MWh), modelul Glosten–Jagannathan–Runkle (GJR) dă $\\hat\\gamma$ = −0,127 ($t$ = −6,4), iar modelul exponențial cu heteroscedasticitate condiționată autoregresivă generalizată (EGARCH) dă $\\hat\\gamma$ = 0,104 ($t$ = 7,2). Ce arată ele?",
                "options": [
                    "Scăderile măresc mai mult volatilitatea, efectul de levier cunoscut de la acțiuni",
                    "Creșterile și scăderile au același efect, deoarece estimațiile nu sînt semnificative",
                    "Cele două modele se contrazic, deoarece semnele diferă",
                    "Creșterile măresc mai mult volatilitatea, efectul de levier invers, tipic pentru mărfuri"
                ],
                "correctExplanation": "În GJR un $\\gamma$ negativ înseamnă că creșterile măresc mai mult volatilitatea; în EGARCH convenția de semn este inversă, deci un $\\gamma$ pozitiv spune același lucru. Ambele sînt clar semnificative (Knittel & Roberts, 2005).",
                "incorrectExplanation": "Cele două modele folosesc convenții de semn opuse pentru $\\gamma$, deci semnele diferite spun aici aceeași poveste; cu $|t|$ peste 6, asimetria este semnificativă."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "A buyer after a 61 EUR move",
                "text": "Yesterday the Romanian price moved by 61 euro per megawatt-hour (EUR/MWh), about two long-run standard deviations. According to the news impact curve of the Glosten–Jagannathan–Runkle (GJR) model, what is tomorrow's $\\sigma$?",
                "options": [
                    "30.6 EUR/MWh after a rise and 37.6 after a fall",
                    "37.6 EUR/MWh after a rise and 30.6 after a fall",
                    "The same value after a rise and after a fall, since the curve is symmetric",
                    "30.3 after a fall and 23.7 after a rise"
                ],
                "correctExplanation": "In EUR/MWh rises raise volatility more: 37.6 against 30.6, the inverse leverage effect. For a buyer the dangerous direction is up, so limits should widen more after a jump than after a fall.",
                "incorrectExplanation": "The GJR curve is asymmetric by design. The values 30.3 and 23.7 are in percent, for a 40% shock, where the order is reversed."
            },
            "ro": {
                "title": "Cumpărătorul după 61 EUR",
                "text": "Ieri prețul din România s-a modificat cu 61 de euro pe megawatt-oră (EUR/MWh), adică circa două abateri standard de lungă durată. Conform curbei de impact a șocurilor (*news impact curve*) din modelul Glosten–Jagannathan–Runkle (GJR), cît este $\\sigma$ de mîine?",
                "options": [
                    "30,6 EUR/MWh după o creștere și 37,6 după o scădere",
                    "37,6 EUR/MWh după o creștere și 30,6 după o scădere",
                    "Aceeași valoare după o creștere și după o scădere, deoarece curba este simetrică",
                    "30,3 după o scădere și 23,7 după o creștere"
                ],
                "correctExplanation": "În EUR/MWh, creșterile măresc mai mult volatilitatea: 37,6 față de 30,6, efectul de levier invers. Pentru un cumpărător direcția periculoasă este în sus, deci limitele se lărgesc mai mult după un salt decît după o scădere.",
                "incorrectExplanation": "Curba GJR este asimetrică prin construcție. Valorile 30,3 și 23,7 sînt în procente, pentru un șoc de 40%, unde ordinea se inversează."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Percent falls and rebounds",
                "text": "In percent, for a shock of 40%, the news impact curve of the Glosten–Jagannathan–Runkle (GJR) model gives $\\sigma$ = 30.3% after a fall and 23.7% after a rise, the opposite order from the euro per megawatt-hour (EUR/MWh) results. How does the lecture reconcile the two?",
                "options": [
                    "The percent results are unreliable and should be ignored",
                    "The percent model uses normal shocks, the EUR/MWh model Student-t shocks",
                    "A rise in EUR/MWh lifts the price level, so moves cost more euro; a fall in percent is often a holiday dip followed by a rebound",
                    "Percent shocks are measured before the weekly calendar is removed"
                ],
                "correctExplanation": "The two results are consistent. At a higher price level the same percent move costs more euro, while large percent falls are often holidays followed by a rebound of similar size.",
                "incorrectExplanation": "Both units use Student-t shocks fitted after removing the calendar; the difference comes from what each unit measures, relative size versus money."
            },
            "ro": {
                "title": "Scăderi procentuale și reveniri",
                "text": "În procente, pentru un șoc de 40%, curba de impact a șocurilor din modelul Glosten–Jagannathan–Runkle (GJR) dă $\\sigma$ = 30,3% după o scădere și 23,7% după o creștere, ordinea inversă față de rezultatele în euro pe megawatt-oră (EUR/MWh). Cum le împacă cursul?",
                "options": [
                    "Rezultatele procentuale nu sînt de încredere și trebuie ignorate",
                    "Modelul procentual folosește șocuri normale, iar cel în EUR/MWh șocuri Student",
                    "O creștere în EUR/MWh ridică nivelul prețului, deci variațiile costă mai mulți euro; o scădere procentuală este adesea o cădere de sărbătoare urmată de o revenire",
                    "Șocurile procentuale sînt măsurate înainte de eliminarea efectului zilei din săptămînă"
                ],
                "correctExplanation": "Cele două rezultate nu se contrazic. La un nivel mai mare al prețului, aceeași variație procentuală costă mai mulți euro, iar scăderile procentuale mari sînt adesea sărbători urmate de o revenire de mărime asemănătoare.",
                "incorrectExplanation": "Ambele unități folosesc șocuri Student, estimate după eliminarea calendarului; diferența vine din ce măsoară fiecare unitate: mărimea relativă sau banii."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Volatility and price level",
                "text": "A regression of the log monthly standard deviation of the shocks in euro per megawatt-hour (EUR/MWh) on the log monthly mean price, over 94 months, gives a slope of 0.75 ($R^2$ = 0.76); for percent shocks the slope is 0.01. If the forward price rises by 10%, what happens to EUR/MWh volatility?",
                "options": [
                    "It rises by about 0.75 EUR/MWh",
                    "It rises by about 7.5%, so limits should be set as a share of the forward price",
                    "It does not change, since percent volatility does not depend on the price",
                    "It rises by about 7.6%, since the $R^2$ is the elasticity"
                ],
                "correctExplanation": "In a log-log regression the slope is an elasticity: volatility in EUR/MWh rises almost in proportion to the price. The reason is the merit order, steeper at high prices. Hence limits as a share of the forward price, not as a fixed amount.",
                "incorrectExplanation": "The slope, not $R^2$, is the elasticity, and it applies to percent changes of both variables. It is percent volatility that does not depend on the price level (slope 0.01)."
            },
            "ro": {
                "title": "Volatilitatea și nivelul prețului",
                "text": "Regresia logaritmului abaterii standard lunare a șocurilor în euro pe megawatt-oră (EUR/MWh) pe logaritmul prețului mediu lunar, pe 94 de luni, dă o pantă de 0,75 ($R^2$ = 0,76); pentru șocurile procentuale panta este 0,01. Dacă prețul contractelor la termen crește cu 10%, ce se întîmplă cu volatilitatea în EUR/MWh?",
                "options": [
                    "Crește cu circa 0,75 EUR/MWh",
                    "Crește cu circa 7,5%, deci limitele se stabilesc ca procent din prețul contractelor la termen",
                    "Nu se modifică, deoarece volatilitatea procentuală nu depinde de preț",
                    "Crește cu circa 7,6%, deoarece $R^2$ este elasticitatea"
                ],
                "correctExplanation": "Într-o regresie log-log panta este o elasticitate: volatilitatea în EUR/MWh crește aproape proporțional cu prețul. Explicația este ordinea de merit, mai abruptă la prețuri mari. De aici limitele ca procent din prețul la termen, nu ca sumă fixă.",
                "incorrectExplanation": "Elasticitatea este panta, nu $R^2$, și se aplică variațiilor procentuale ale ambelor mărimi. Volatilitatea procentuală este cea care nu depinde de nivelul prețului (panta 0,01)."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Fat tails versus asymmetry",
                "text": "Six models, the generalised autoregressive conditional heteroskedasticity (GARCH) model, the Glosten–Jagannathan–Runkle (GJR) model and the exponential GARCH (EGARCH) model, each with normal and Student-t shocks, are compared by the Bayesian information criterion (BIC) in both units. What is the main lesson?",
                "options": [
                    "Asymmetry matters most: GJR with normal shocks beats GARCH with Student-t shocks",
                    "Normal shocks win in euro per megawatt-hour, Student-t shocks in percent",
                    "Every Student-t model beats every normal one; the gain from asymmetry is small by comparison",
                    "BIC and the Akaike information criterion rank the models in opposite order"
                ],
                "correctExplanation": "The best models are GJR-t in percent and EGARCH-t in euro per megawatt-hour, but the gain from asymmetry is small compared with the gain from fat tails; the Akaike information criterion (AIC) gives the same ranking. First get the tails right.",
                "incorrectExplanation": "In percent, GJR with normal shocks has a BIC of 24,690.7, far above 24,220.8 for GARCH with Student-t shocks; fat tails dominate in both units."
            },
            "ro": {
                "title": "Cozile groase și asimetria",
                "text": "Șase modele, modelul cu heteroscedasticitate condiționată autoregresivă generalizată (GARCH), modelul Glosten–Jagannathan–Runkle (GJR) și modelul GARCH exponențial (EGARCH), fiecare cu șocuri normale și Student, sînt comparate cu criteriul informațional bayesian (BIC), în ambele unități. Care este lecția principală?",
                "options": [
                    "Asimetria contează cel mai mult: GJR cu șocuri normale îl depășește pe GARCH cu șocuri Student",
                    "Șocurile normale cîștigă în euro pe megawatt-oră, iar cele Student în procente",
                    "Orice model cu șocuri Student îl depășește pe oricare model cu șocuri normale; cîștigul adus de asimetrie este mic în comparație",
                    "BIC și criteriul informațional Akaike ordonează modelele invers"
                ],
                "correctExplanation": "Cele mai bune modele sînt GJR-t în procente și EGARCH-t în euro pe megawatt-oră, dar cîștigul adus de asimetrie este mic față de cel adus de cozile groase; criteriul informațional Akaike (AIC) dă aceeași ordine. Mai întîi modelați corect cozile.",
                "incorrectExplanation": "În procente, GJR cu șocuri normale are un BIC de 24 690,7, mult peste 24 220,8 pentru GARCH cu șocuri Student; cozile groase domină în ambele unități."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Expected turbulent duration",
                "text": "In the two-regime Markov-switching model on shocks in euro per megawatt-hour (EUR/MWh), the turbulent regime has $\\sigma$ = 41.9 and $p_{22}$ = 0.957. Using the expected duration $1/(1-p_{ii})$, how long does a turbulent spell last on average?",
                "options": [
                    "About 23 days",
                    "About 69 days",
                    "About 1 day",
                    "About 96 days"
                ],
                "correctExplanation": "$1/(1-0.957)=1/0.043\\approx 23$ days. The calm regime, with $\\sigma$ = 12.9 and $p_{11}$ = 0.986, lasts about 69 days; the turbulent one covers 24% of all days.",
                "incorrectExplanation": "The expected duration uses the probability of leaving the regime, $1-p_{ii}$, in the denominator; 69 days is the calm regime."
            },
            "ro": {
                "title": "Durata medie a regimului agitat",
                "text": "În modelul Markov cu două regimuri estimat pe șocurile în euro pe megawatt-oră (EUR/MWh), regimul agitat are $\\sigma$ = 41,9 și $p_{22}$ = 0,957. Folosind durata medie $1/(1-p_{ii})$, cît durează în medie un episod agitat?",
                "options": [
                    "Circa 23 de zile",
                    "Circa 69 de zile",
                    "Circa o zi",
                    "Circa 96 de zile"
                ],
                "correctExplanation": "$1/(1-0{,}957)=1/0{,}043\\approx 23$ de zile. Regimul calm, cu $\\sigma$ = 12,9 și $p_{11}$ = 0,986, durează circa 69 de zile; cel agitat cuprinde 24% din zile.",
                "incorrectExplanation": "La numitorul duratei medii stă probabilitatea de a părăsi regimul, $1-p_{ii}$; 69 de zile este durata regimului calm."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Turbulent days in 2026",
                "text": "The Markov-switching model on shocks in euro per megawatt-hour (EUR/MWh) gives the share of turbulent days: 86% in 2022, 6% in 2025 and 33% in 2026, rising to 48% since July 2026. How does the lecture read 2026?",
                "options": [
                    "A repeat of 2022, since prices rose again",
                    "A quiet year, since percent volatility did not change",
                    "A permanent switch to the turbulent regime from July 2026",
                    "Not a quiet year, but not a 2022 either: short turbulent spells alternate with calm ones"
                ],
                "correctExplanation": "The crisis was one long turbulent block, with the longest spell from 15 June 2022 to 31 January 2023 (231 days). In 2026 the model moves in and out of turbulence for shorter spells; the turbulent probability was 0.47 on 31 October 2026.",
                "incorrectExplanation": "One third of turbulent days is far from quiet, but far below the 86% of 2022, and the spells are short rather than one long regime."
            },
            "ro": {
                "title": "Zilele agitate din 2026",
                "text": "Modelul Markov cu schimbare de regim pe șocurile în euro pe megawatt-oră (EUR/MWh) dă ponderea zilelor agitate: 86% în 2022, 6% în 2025 și 33% în 2026, cu 48% începînd din iulie 2026. Cum interpretează cursul anul 2026?",
                "options": [
                    "O repetare a anului 2022, deoarece prețurile au crescut din nou",
                    "Un an liniștit, deoarece volatilitatea procentuală nu s-a schimbat",
                    "O trecere permanentă în regimul agitat începînd din iulie 2026",
                    "Nu este un an liniștit, dar nici un nou 2022: episoade agitate scurte alternează cu perioade calme"
                ],
                "correctExplanation": "Criza a fost un singur bloc agitat lung, cel mai lung episod durînd de la 15 iunie 2022 pînă la 31 ianuarie 2023 (231 de zile). În 2026 modelul intră și iese din regimul agitat pentru perioade mai scurte; probabilitatea regimului agitat era de 0,47 la 31 octombrie 2026.",
                "incorrectExplanation": "O treime de zile agitate nu înseamnă un an liniștit, dar este mult sub cele 86% din 2022, iar episoadele sînt scurte, nu un singur regim lung."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Real-time regime warning",
                "text": "A supplier wants to use the probability of the turbulent regime from the Markov-switching model, computed with the Hamilton filter, as a real-time early warning. Which probability should it use?",
                "options": [
                    "The smoothed probability, because it uses all the data and is more accurate",
                    "The filtered probability, which uses only the information available up to the previous day",
                    "The unconditional share of turbulent days in the sample, 24%",
                    "The probability $p_{22}$ = 0.957 of staying in the turbulent regime"
                ],
                "correctExplanation": "The smoothed probabilities shown in the chart use all the data, including the future; a real-time warning must use the filtered probabilities, which use only the past.",
                "incorrectExplanation": "On any given day the future is unknown, so a probability built with future data cannot be used for decisions; a constant share or transition probability does not change from day to day."
            },
            "ro": {
                "title": "Avertizarea în timp real",
                "text": "Un furnizor vrea să folosească probabilitatea regimului agitat din modelul Markov cu schimbare de regim, calculată cu filtrul lui Hamilton, ca avertizare timpurie în timp real. Ce probabilitate trebuie să folosească?",
                "options": [
                    "Probabilitatea netezită, deoarece folosește toate datele și este mai precisă",
                    "Probabilitatea filtrată, care folosește doar informația disponibilă pînă în ziua precedentă",
                    "Ponderea necondiționată a zilelor agitate din eșantion, 24%",
                    "Probabilitatea $p_{22}$ = 0,957 de a rămîne în regimul agitat"
                ],
                "correctExplanation": "Probabilitățile netezite din grafic folosesc toate datele, inclusiv pe cele viitoare; o avertizare în timp real trebuie să folosească probabilitățile filtrate, care folosesc doar trecutul.",
                "incorrectExplanation": "În ziua deciziei viitorul nu este cunoscut, deci o probabilitate calculată cu date viitoare nu poate fi folosită; o pondere constantă sau o probabilitate de trecere nu se modifică de la o zi la alta."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Intraday variation and batteries",
                "text": "The realised intraday variation (RV) is the square root of the sum of squared hour-to-hour price changes within a delivery day. Its correlation with the absolute daily shock $|u_t|$ is only 0.46. What follows for a battery developer?",
                "options": [
                    "Intraday variation is a separate risk, and battery revenue scales with it, not with the daily average price",
                    "RV is the realised volatility of finance and can replace daily volatility models",
                    "RV should be measured in percent, like the daily base price",
                    "Daily volatility is a sufficient proxy for intraday risk, since the correlation is positive"
                ],
                "correctExplanation": "A correlation of 0.46 means the daily shock tells little about intraday movement. RV is measured in euro per megawatt-hour because hourly prices can be negative, and it is what a battery or a flexible consumer earns from.",
                "incorrectExplanation": "RV is not the realised volatility of finance: the 24 hours are 24 different products, not one asset, and hourly prices can be negative, so percent changes are unusable."
            },
            "ro": {
                "title": "Variația intrazilnică și bateriile",
                "text": "Variația intrazilnică realizată (RV) este rădăcina pătrată a sumei pătratelor variațiilor de preț de la o oră la alta din aceeași zi de livrare. Corelația ei cu șocul zilnic absolut $|u_t|$ este de doar 0,46. Ce rezultă pentru un investitor în baterii?",
                "options": [
                    "Variația intrazilnică este un risc distinct, iar venitul bateriei depinde de ea, nu de prețul mediu zilnic",
                    "RV este volatilitatea realizată din finanțe și poate înlocui modelele de volatilitate zilnică",
                    "RV trebuie măsurată în procente, ca prețul zilnic de bază",
                    "Volatilitatea zilnică aproximează suficient riscul intrazilnic, deoarece corelația este pozitivă"
                ],
                "correctExplanation": "O corelație de 0,46 arată că șocul zilnic spune puțin despre mișcarea din cursul zilei. RV se măsoară în euro pe megawatt-oră, deoarece prețurile orare pot fi negative, și din ea cîștigă o baterie sau un consumator flexibil.",
                "incorrectExplanation": "RV nu este volatilitatea realizată din finanțe: cele 24 de ore sînt 24 de produse diferite, nu un singur activ, iar prețurile orare pot fi negative, deci variațiile procentuale nu pot fi folosite."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Solar and intraday risk",
                "text": "Mean solar generation in Romania rose from 157 megawatts (MW) in 2019 to 593 MW in January–October 2026, and the median relative intraday variation from 0.64 in 2019 to 1.24 in 2024 (1.01 in 2026). Which mechanism does the lecture give?",
                "options": [
                    "Solar plants raise midday prices, which narrows the daily price range",
                    "Solar output raises the daily base price and therefore percent volatility",
                    "Solar pushes midday prices down, sometimes below zero, while evening prices stay high, widening the gap between hours",
                    "Solar generation strengthens the weekly calendar of demand"
                ],
                "correctExplanation": "Solar plants produce at midday, pushing midday prices down while evening prices, after sunset, stay high. The gap between the cheapest and dearest hours widens, and with it the hour-to-hour variation; the monthly correlation of the two series is 0.46.",
                "incorrectExplanation": "Solar output lowers, not raises, midday prices; the effect is within the day, not on the daily level or on the weekly calendar. Cheaper middays and dearer evenings are the business case of storage."
            },
            "ro": {
                "title": "Producția solară și riscul intrazilnic",
                "text": "Producția solară medie din România a crescut de la 157 de megawați (MW) în 2019 la 593 MW în ianuarie–octombrie 2026, iar mediana variației intrazilnice relative de la 0,64 în 2019 la 1,24 în 2024 (1,01 în 2026). Ce mecanism prezintă cursul?",
                "options": [
                    "Centralele solare ridică prețurile de la prînz, ceea ce îngustează plaja de preț a zilei",
                    "Producția solară ridică prețul zilnic de bază și, prin el, volatilitatea procentuală",
                    "Producția solară împinge în jos prețurile de la prînz, uneori sub zero, în timp ce prețurile de seară rămîn ridicate, iar diferența dintre ore crește",
                    "Producția solară accentuează calendarul săptămînal al cererii"
                ],
                "correctExplanation": "Centralele solare produc la prînz și împing în jos prețurile din mijlocul zilei, în timp ce prețurile de seară, după apusul soarelui, rămîn ridicate. Diferența dintre orele cele mai ieftine și cele mai scumpe crește, iar odată cu ea și variația de la o oră la alta; corelația lunară dintre cele două serii este 0,46.",
                "incorrectExplanation": "Producția solară scade, nu crește, prețurile de la prînz; efectul este în cursul zilei, nu asupra nivelului zilnic sau a calendarului săptămînal. Prețuri mici la prînz și mari seara sînt argumentul economic pentru stocare."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Reading the HAR weights",
                "text": "The heterogeneous autoregressive (HAR) model for the log of realised intraday variation gives weights of 0.40 for yesterday, 0.36 for the last 7 days and 0.22 for the last 30 days, all with $t$-statistics above 6, and $R^2$ = 0.82. Which reading is correct?",
                "options": [
                    "Yesterday matters most, but the last week and month together weigh more than yesterday",
                    "Only yesterday matters; the weekly and monthly terms add nothing",
                    "The last month matters most, since it averages 30 days",
                    "With $R^2$ = 0.82 the model also foresees isolated spikes"
                ],
                "correctExplanation": "0.36 + 0.22 = 0.58 against 0.40 for yesterday: intraday variation has a long memory. In the test year the HAR mean absolute error (MAE) is 35.6 euro per megawatt-hour, against 39.1 for the naive forecast, 9.1% less.",
                "incorrectExplanation": "All three weights are significant, and a forecast built from averages of the past is smooth by construction: it follows slow movements but cannot foresee isolated spikes."
            },
            "ro": {
                "title": "Ponderile modelului HAR",
                "text": "Modelul autoregresiv eterogen (HAR) pentru logaritmul variației intrazilnice realizate dă ponderile 0,40 pentru ziua de ieri, 0,36 pentru ultimele 7 zile și 0,22 pentru ultimele 30 de zile, toate cu statistici $t$ peste 6, iar $R^2$ = 0,82. Care interpretare este corectă?",
                "options": [
                    "Ziua de ieri contează cel mai mult, dar ultima săptămînă și ultima lună au împreună o pondere mai mare decît ea",
                    "Contează doar ziua de ieri; termenii săptămînal și lunar nu adaugă nimic",
                    "Ultima lună contează cel mai mult, deoarece este o medie pe 30 de zile",
                    "Cu $R^2$ = 0,82, modelul anticipează și salturile izolate"
                ],
                "correctExplanation": "0,36 + 0,22 = 0,58, față de 0,40 pentru ziua de ieri: variația intrazilnică are memorie lungă. În anul de test, eroarea absolută medie (MAE) a modelului HAR este de 35,6 euro pe megawatt-oră, față de 39,1 pentru prognoza naivă, adică cu 9,1% mai puțin.",
                "incorrectExplanation": "Toate cele trei ponderi sînt semnificative, iar o prognoză construită din medii ale trecutului este netedă prin construcție: urmărește mișcările lente, dar nu poate anticipa salturile izolate."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "QLIKE penalises underestimation",
                "text": "Suppose the true $\\sigma$ is 20. One forecast says 10, another says 40. What are their losses under the quasi-likelihood loss (QLIKE), $\\varepsilon^2/\\hat\\sigma^2-\\ln(\\varepsilon^2/\\hat\\sigma^2)-1$?",
                "options": [
                    "0.64 for the forecast of 10 and 1.61 for 40: overestimating costs more",
                    "1.61 for the forecast of 10 and 0.64 for 40: underestimating risk costs 2.5 times more",
                    "Equal losses, since both forecasts are off by a factor of 2",
                    "1.61 for both forecasts, since QLIKE is symmetric in logs"
                ],
                "correctExplanation": "For 10 the ratio is $400/100=4$: $4-\\ln 4-1\\approx 1.61$. For 40 it is $400/1600=0.25$: $0.25-\\ln 0.25-1\\approx 0.64$. Underestimating risk costs 2.5 times more, which is what a risk manager wants.",
                "incorrectExplanation": "QLIKE is asymmetric: it penalises a too-low variance forecast more than a too-high one. The mean squared error (MSE) says the opposite, because it squares the large numbers."
            },
            "ro": {
                "title": "QLIKE penalizează subestimarea",
                "text": "Să presupunem că $\\sigma$ adevărat este 20. O prognoză indică 10, alta 40. Care sînt pierderile lor după funcția de pierdere de tip cvasi-verosimilitate (QLIKE), $\\varepsilon^2/\\hat\\sigma^2-\\ln(\\varepsilon^2/\\hat\\sigma^2)-1$?",
                "options": [
                    "0,64 pentru prognoza de 10 și 1,61 pentru 40: supraestimarea costă mai mult",
                    "1,61 pentru prognoza de 10 și 0,64 pentru 40: subestimarea riscului costă de 2,5 ori mai mult",
                    "Pierderi egale, deoarece ambele prognoze greșesc cu un factor de 2",
                    "1,61 pentru ambele prognoze, deoarece QLIKE este simetrică în logaritmi"
                ],
                "correctExplanation": "Pentru 10, raportul este $400/100=4$: $4-\\ln 4-1\\approx 1{,}61$. Pentru 40, este $400/1600=0{,}25$: $0{,}25-\\ln 0{,}25-1\\approx 0{,}64$. Subestimarea riscului costă de 2,5 ori mai mult, ceea ce își dorește un manager de risc.",
                "incorrectExplanation": "QLIKE este asimetrică: penalizează mai mult o prognoză a varianței prea mică decît una prea mare. Eroarea pătratică medie (MSE) spune contrariul, pentru că ridică la pătrat valorile mari."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "A vendor's best MSE",
                "text": "A vendor's volatility model has the lowest mean squared error (MSE) on your test year, thanks to three extreme days. What should you ask for before buying it?",
                "options": [
                    "Nothing more: the lowest MSE proves it is the best model",
                    "A longer in-sample fit with a higher $R^2$",
                    "The quasi-likelihood loss (QLIKE) on the same days and a Diebold–Mariano (DM) test against the generalised autoregressive conditional heteroskedasticity model with Student-t shocks (GARCH-t) and the 30-day history",
                    "The error computed on absolute shocks instead of squared ones"
                ],
                "correctExplanation": "MSE is dominated by a few extreme days, while QLIKE penalises errors in relative terms; the DM test says whether a difference in losses is significant, out of sample. On the course test year the best QLIKE in euro per megawatt-hour (EUR/MWh) belongs to the exponential GARCH with Student-t shocks (EGARCH-t), not significantly better than GARCH-t.",
                "incorrectExplanation": "In-sample fit says nothing about forecasting, and losses built on absolute shocks or errors in logarithms can rank models wrongly with a noisy proxy (Patton, 2011)."
            },
            "ro": {
                "title": "Cea mai mică MSE a furnizorului",
                "text": "Modelul de volatilitate al unui furnizor are cea mai mică eroare pătratică medie (MSE) în anul dumneavoastră de test, datorită a trei zile extreme. Ce îi cereți înainte de a-l cumpăra?",
                "options": [
                    "Nimic în plus: cea mai mică MSE dovedește că este cel mai bun model",
                    "O estimare mai lungă în eșantion, cu un $R^2$ mai mare",
                    "Valoarea funcției de pierdere de tip cvasi-verosimilitate (QLIKE) pe aceleași zile și un test Diebold–Mariano (DM) față de modelul cu heteroscedasticitate condiționată autoregresivă generalizată cu șocuri Student (GARCH-t) și de varianța istorică pe 30 de zile",
                    "Eroarea calculată pe șocurile absolute, în locul pătratelor lor"
                ],
                "correctExplanation": "MSE este dominată de cîteva zile extreme, în timp ce QLIKE penalizează erorile în termeni relativi; testul DM arată dacă diferența dintre pierderi este semnificativă, în afara eșantionului. În anul de test al cursului, cel mai bun QLIKE în euro pe megawatt-oră (EUR/MWh) îl are modelul GARCH exponențial cu șocuri Student (EGARCH-t), fără a fi semnificativ mai bun decît GARCH-t.",
                "incorrectExplanation": "Ajustarea în eșantion nu spune nimic despre prognoză, iar funcțiile construite pe șocuri absolute sau pe erori în logaritmi pot ordona greșit modelele cînd aproximarea este zgomotoasă (Patton, 2011)."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Choosing a default model",
                "text": "Over the 365 test days, the quasi-likelihood loss (QLIKE) in euro per megawatt-hour (EUR/MWh) is 1.428 for the 30-day historical variance and 1.349 for the exponential version of the generalised autoregressive conditional heteroskedasticity model with Student-t shocks (EGARCH-t). In EUR/MWh all GARCH-type models and the exponentially weighted moving average (EWMA) beat the history at the 5% level; in percent none does. The asymmetric models are not significantly better than GARCH-t ($p$ = 0.08). What follows?",
                "options": [
                    "Adopt EGARCH-t, since it is significantly better than GARCH-t",
                    "Use GARCH-t as the default: it beats the history in EUR/MWh, and asymmetric models add little out of sample",
                    "Keep the 30-day history, since gains of a few percent are negligible",
                    "Use EWMA, since it is the only model significant in percent"
                ],
                "correctExplanation": "The best EUR/MWh model, EGARCH-t, is 5.5% below the history, but not significantly better than plain GARCH-t. The gains are modest but systematic, so GARCH-t is the sensible default.",
                "incorrectExplanation": "With $p$ = 0.08 the asymmetric models do not beat GARCH-t at 5%, and in percent no model, EWMA included, beats the history significantly."
            },
            "ro": {
                "title": "Alegerea modelului implicit",
                "text": "Pe cele 365 de zile de test, funcția de pierdere de tip cvasi-verosimilitate (QLIKE) în euro pe megawatt-oră (EUR/MWh) este 1,428 pentru varianța istorică pe 30 de zile și 1,349 pentru varianta exponențială a modelului cu heteroscedasticitate condiționată autoregresivă generalizată, cu șocuri Student (EGARCH-t). În EUR/MWh, toate modelele de tip GARCH, ca și media mobilă cu ponderi exponențiale (EWMA), sînt semnificativ mai precise decît varianța istorică la pragul de 5%; în procente, niciunul. Modelele asimetrice nu sînt semnificativ mai bune decît GARCH-t ($p$ = 0,08). Ce rezultă?",
                "options": [
                    "Adoptăm EGARCH-t, deoarece este semnificativ mai bun decît GARCH-t",
                    "Folosim GARCH-t ca model implicit: este mai precis decît varianța istorică în EUR/MWh, iar modelele asimetrice aduc puțin în afara eșantionului",
                    "Păstrăm varianța istorică pe 30 de zile, deoarece cîștigurile de cîteva procente sînt neglijabile",
                    "Folosim EWMA, deoarece este singurul model semnificativ în procente"
                ],
                "correctExplanation": "Cel mai bun model în EUR/MWh, EGARCH-t, are o pierdere cu 5,5% sub cea a varianței istorice, dar nu este semnificativ mai bun decît GARCH-t simplu. Cîștigurile sînt modeste, dar sistematice, deci GARCH-t este alegerea implicită rezonabilă.",
                "incorrectExplanation": "Cu $p$ = 0,08, modelele asimetrice nu îl depășesc pe GARCH-t la pragul de 5%, iar în procente niciun model, nici EWMA, nu este semnificativ mai precis decît varianța istorică."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Limit changes without news",
                "text": "On 22 January 2026 a shock of +124 euro per megawatt-hour (EUR/MWh) hit. The next day the forecast $\\hat\\sigma$ of the generalised autoregressive conditional heteroskedasticity (GARCH) model jumped from 25 to 47 EUR/MWh, the 30-day historical forecast only to 33; thirty days later the historical forecast fell from 32 to 23 overnight. What does this teach a risk manager?",
                "options": [
                    "A limit that jumps 30 days after a shock, with no news, is the sign of a historical-window model",
                    "GARCH overreacts and should be smoothed with a 30-day window",
                    "The historical model is preferable, because it moves less",
                    "The drop after 30 days reflects new information about the market"
                ],
                "correctExplanation": "In the historical window one day weighs one thirtieth, so the forecast lags; when the shock leaves the window it forgets abruptly. GARCH reacts at once and lets the shock fade gradually, at the rate $\\alpha+\\beta$.",
                "incorrectExplanation": "Nothing happened on the day of the drop: the shock simply left the window. GARCH's quick reaction is why it beats the history out of sample."
            },
            "ro": {
                "title": "Modificarea limitei în absența știrilor",
                "text": "La 22 ianuarie 2026 a avut loc un șoc de +124 euro pe megawatt-oră (EUR/MWh). A doua zi, prognoza $\\hat\\sigma$ a modelului cu heteroscedasticitate condiționată autoregresivă generalizată (GARCH) a crescut de la 25 la 47 EUR/MWh, iar prognoza istorică pe 30 de zile doar la 33; după 30 de zile, prognoza istorică a scăzut într-o singură zi de la 32 la 23. Ce învață din aceasta un manager de risc?",
                "options": [
                    "O limită care se modifică brusc la 30 de zile după un șoc, fără nicio informație nouă, trădează un model cu fereastră istorică",
                    "GARCH reacționează exagerat și trebuie netezit cu o fereastră de 30 de zile",
                    "Modelul istoric este preferabil, deoarece se modifică mai puțin",
                    "Scăderea de după 30 de zile reflectă o informație nouă despre piață"
                ],
                "correctExplanation": "În fereastra istorică o zi are o pondere de o treizecime, deci prognoza întîrzie; cînd șocul iese din fereastră, ea uită brusc. GARCH reacționează imediat și lasă șocul să se stingă treptat, cu rata $\\alpha+\\beta$.",
                "incorrectExplanation": "În ziua scăderii nu s-a întîmplat nimic: șocul a ieșit pur și simplu din fereastră. Reacția rapidă a modelului GARCH este motivul pentru care el cîștigă în afara eșantionului."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The square-root-of-time rule",
                "text": "On 9 April 2026, Brent's one-day forecast from the generalised autoregressive conditional heteroskedasticity (GARCH) model was 93% a year, against a long-run level of 39%. The 20-day 90% band from GARCH was ±38.5%, while $\\sigma\\sqrt{20}$ gave ±43.1%. Why the difference?",
                "options": [
                    "The $\\sigma\\sqrt{h}$ rule is exact for oil, so the GARCH band is too narrow",
                    "The GARCH band uses a different quantile than 1.645",
                    "Brent returns are autocorrelated, so daily variances cannot be added",
                    "Volatility was expected to fall back to its long-run level, so $\\sigma\\sqrt{20}$ was about 12% too wide"
                ],
                "correctExplanation": "GARCH sums the daily forecasts $\\hat\\sigma^2_{T+k}$, which revert to the long-run level; scaling today's high $\\sigma$ ignores the expected calming. On 30 October 2026, with $\\hat\\sigma$ = 32% below the long-run 40%, $\\sigma\\sqrt{20}$ was too narrow instead.",
                "incorrectExplanation": "Oil returns have no autocorrelation, which is exactly why the daily variance forecasts can be summed; both bands use $\\pm1.645$. The rule $\\sigma\\sqrt{h}$ is wrong in both directions."
            },
            "ro": {
                "title": "Regula rădăcinii pătrate",
                "text": "La 9 aprilie 2026, prognoza pentru o zi a modelului cu heteroscedasticitate condiționată autoregresivă generalizată (GARCH) pentru Brent era de 93% pe an, față de un nivel de lungă durată de 39%. Banda de 90% pe 20 de zile dată de GARCH era de ±38,5%, în timp ce $\\sigma\\sqrt{20}$ dădea ±43,1%. De ce diferă?",
                "options": [
                    "Regula $\\sigma\\sqrt{h}$ este exactă pentru petrol, deci banda GARCH este prea îngustă",
                    "Banda GARCH folosește altă cuantilă decît 1,645",
                    "Randamentele Brent sînt autocorelate, deci varianțele zilnice nu se pot aduna",
                    "Se aștepta revenirea volatilității spre nivelul de lungă durată, deci $\\sigma\\sqrt{20}$ dădea o bandă prea largă cu circa 12%"
                ],
                "correctExplanation": "GARCH adună prognozele zilnice $\\hat\\sigma^2_{T+k}$, care revin spre nivelul de lungă durată; scalarea valorii mari $\\sigma$ de azi ignoră calmarea așteptată. La 30 octombrie 2026, cu $\\hat\\sigma$ = 32%, sub nivelul de lungă durată de 40%, $\\sigma\\sqrt{20}$ dădea dimpotrivă o bandă prea îngustă.",
                "incorrectExplanation": "Randamentele petrolului nu sînt autocorelate, tocmai de aceea prognozele zilnice ale varianței se pot aduna; ambele benzi folosesc $\\pm1{,}645$. Regula $\\sigma\\sqrt{h}$ greșește în ambele direcții."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Limits for November 2026",
                "text": "On 31 October 2026 the forecast of the generalised autoregressive conditional heteroskedasticity model with Student-t shocks (GARCH-t) for the Romanian price was $\\hat\\sigma$ = 26.0 euro per megawatt-hour (EUR/MWh), close to its long-run level of 27.6. Using $\\pm1.645\\,\\sigma$, what is the one-day 90% limit for the days of November?",
                "options": [
                    "About ±26 EUR/MWh for each day",
                    "About ±16 EUR/MWh for each day",
                    "About ±43 EUR/MWh, almost the same for each day of November",
                    "About ±43 EUR/MWh on 1 November, widening with $\\sqrt{h}$ to about ±235 by the end of the month"
                ],
                "correctExplanation": "$1.645\\times 26.0\\approx 43$ EUR/MWh. Since the forecast is close to the long-run level, the term structure is almost flat, so the daily limit barely changes over November.",
                "incorrectExplanation": "A daily limit uses the daily forecast for that day, which reverts to the long-run level, not today's $\\sigma$ scaled by $\\sqrt{h}$; and $\\sigma$ alone is about a 68% band, not 90%."
            },
            "ro": {
                "title": "Limitele pentru noiembrie 2026",
                "text": "La 31 octombrie 2026, prognoza modelului cu heteroscedasticitate condiționată autoregresivă generalizată cu șocuri Student (GARCH-t) pentru prețul din România era $\\hat\\sigma$ = 26,0 euro pe megawatt-oră (EUR/MWh), aproape de nivelul de lungă durată, 27,6. Folosind $\\pm1{,}645\\,\\sigma$, cît este limita de 90% pentru o zi în zilele lunii noiembrie?",
                "options": [
                    "Circa ±26 EUR/MWh în fiecare zi",
                    "Circa ±16 EUR/MWh în fiecare zi",
                    "Circa ±43 EUR/MWh, aproape aceeași în fiecare zi din noiembrie",
                    "Circa ±43 EUR/MWh la 1 noiembrie, crescînd cu $\\sqrt{h}$ pînă la circa ±235 la sfîrșitul lunii"
                ],
                "correctExplanation": "$1{,}645\\times 26{,}0\\approx 43$ EUR/MWh. Prognoza fiind aproape de nivelul de lungă durată, structura la termen este aproape plată, deci limita zilnică abia se modifică în noiembrie.",
                "incorrectExplanation": "Limita zilnică folosește prognoza pentru ziua respectivă, care revine spre nivelul de lungă durată, nu $\\sigma$ de azi înmulțit cu $\\sqrt{h}$; iar $\\sigma$ singur dă o bandă de circa 68%, nu de 90%."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Backtesting the one-day band",
                "text": "Over the 365 days of the test year, 38 days fell outside the 90% band of the generalised autoregressive conditional heteroskedasticity model with Student-t shocks (GARCH-t), set on the day before. How should the result be read?",
                "options": [
                    "10.4% outside against 10% expected, spread evenly: 9.4% from November to April and 11.4% from May to October",
                    "10.4% outside against 10% expected, but breaches concentrated in the summer months",
                    "3.8% outside, so the band was too wide",
                    "38% outside, so the band failed during the price rise"
                ],
                "correctExplanation": "$38/365\\approx 10.4$%, close to the 10% target, and the breaches did not cluster despite the price rise; the band widened with the price level, from a mean half-width of 33 to 36 euro per megawatt-hour.",
                "incorrectExplanation": "The breach rate is 38 out of 365 days, not 38% or 3.8%, and the two half-years are close to each other. Formal tests of such bands come in Lecture 4."
            },
            "ro": {
                "title": "Verificarea benzii de o zi",
                "text": "Dintre cele 365 de zile ale anului de test, 38 au căzut în afara benzii de 90% a modelului cu heteroscedasticitate condiționată autoregresivă generalizată cu șocuri Student (GARCH-t), stabilită în ziua precedentă. Cum trebuie citit rezultatul?",
                "options": [
                    "10,4% în afara benzii, față de 10% așteptat, distribuite uniform: 9,4% între noiembrie și aprilie și 11,4% între mai și octombrie",
                    "10,4% în afara benzii, față de 10% așteptat, dar depășirile s-au concentrat în lunile de vară",
                    "3,8% în afara benzii, deci banda a fost prea largă",
                    "38% în afara benzii, deci banda a cedat în timpul creșterii prețului"
                ],
                "correctExplanation": "$38/365\\approx 10{,}4$%, aproape de ținta de 10%, iar depășirile nu s-au grupat, în ciuda creșterii prețului; banda s-a lărgit odată cu nivelul prețului, de la o semilățime medie de 33 la 36 de euro pe megawatt-oră.",
                "incorrectExplanation": "Rata depășirilor este de 38 din 365 de zile, nu 38% sau 3,8%, iar cele două semestre sînt apropiate. Testele formale ale unor asemenea benzi se studiază în cursul 4."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "2026 compared with 2022",
                "text": "In 2026 the mean monthly $\\hat\\sigma$ in percent was 17.4%, as in 2022; in euro per megawatt-hour (EUR/MWh) it doubled from 2019 (10.9 to 21.8) but peaked at 34.7 in January 2026, against 65.1 in September 2022. How should a supplier renewing contracts in November 2026 price risk?",
                "options": [
                    "As in 2022, since percent volatility is identical",
                    "As in 2019, since percent volatility has hardly changed",
                    "With a crisis premium, since the turbulent regime covered most of 2026",
                    "On the higher price level, not on a new volatility regime"
                ],
                "correctExplanation": "The case study's verdict: 2026 is a shock to the price level, with a turbulent regime about half of the time since July, but not (yet) a 2022. The turbulent regime covered 33% of 2026 against 86% in 2022.",
                "incorrectExplanation": "Percent volatility is the same in all three years and says nothing about money at risk; in EUR/MWh 2026 is clearly above 2019 but far below the 2022 peak."
            },
            "ro": {
                "title": "Anul 2026 comparat cu 2022",
                "text": "În 2026, $\\hat\\sigma$ lunar mediu în procente a fost de 17,4%, ca în 2022; în euro pe megawatt-oră (EUR/MWh) s-a dublat față de 2019 (de la 10,9 la 21,8), dar maximul din 2026, 34,7 în ianuarie, rămîne mult sub cel din 2022, 65,1 în septembrie. Cum trebuie să includă riscul în preț un furnizor care reînnoiește contractele în noiembrie 2026?",
                "options": [
                    "Ca în 2022, deoarece volatilitatea procentuală este aceeași",
                    "Ca în 2019, deoarece volatilitatea procentuală abia s-a modificat",
                    "Cu o primă de criză, deoarece regimul agitat a cuprins cea mai mare parte din 2026",
                    "Pe baza nivelului mai ridicat al prețului, nu a unui nou regim de volatilitate"
                ],
                "correctExplanation": "Concluzia studiului de caz: 2026 este un șoc al nivelului prețului, cu un regim agitat în circa jumătate din zile începînd din iulie, dar nu (încă) o criză de tipul celei din 2022. Regimul agitat a cuprins 33% din zilele anului 2026, față de 86% în 2022.",
                "incorrectExplanation": "Volatilitatea procentuală este aceeași în toți cei trei ani și nu spune nimic despre banii expuși riscului; în EUR/MWh, 2026 este clar peste 2019, dar mult sub maximul din 2022."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Hedging energy shares with Brent",
                "text": "Case study C3 applies a dynamic conditional correlation (DCC) model to OMV Petrom, Romgaz and Nuclearelectrica against Brent: the mean correlation is 0.13, and the out-of-sample hedge changes the basket's variance by −1.7% (dynamic) and −6.9% (static), where a negative change means more risk. What is the conclusion?",
                "options": [
                    "A Brent hedge does not reduce the risk of Romanian energy shares, which is mainly regulatory and local",
                    "A static Brent hedge cuts the basket's risk by 6.9%",
                    "The dynamic hedge works well, since the DCC parameters $a$ = 0.021 and $b$ = 0.950 are persistent",
                    "Romanian energy shares move almost one-for-one with oil"
                ],
                "correctExplanation": "With a mean correlation of 0.13, oil explains little of these shares, and both hedges increase the basket's risk out of sample. Their risk is regulatory and local.",
                "incorrectExplanation": "In this replication a negative variance change means more risk, not less; persistent DCC parameters only say the correlation moves slowly, not that it is high."
            },
            "ro": {
                "title": "Acoperirea acțiunilor cu Brent",
                "text": "Studiul de caz C3 aplică un model de corelație condiționată dinamică (DCC) pentru OMV Petrom, Romgaz și Nuclearelectrica față de Brent: corelația medie este 0,13, iar acoperirea în afara eșantionului modifică varianța coșului cu −1,7% (dinamic) și cu −6,9% (static), unde o valoare negativă înseamnă risc mai mare. Care este concluzia?",
                "options": [
                    "Acoperirea cu Brent nu reduce riscul acțiunilor energetice românești, care ține mai ales de reglementare și de piața locală",
                    "Acoperirea statică cu Brent reduce riscul coșului cu 6,9%",
                    "Acoperirea dinamică funcționează bine, deoarece parametrii DCC $a$ = 0,021 și $b$ = 0,950 sînt persistenți",
                    "Acțiunile energetice românești se mișcă aproape unu la unu cu petrolul"
                ],
                "correctExplanation": "Cu o corelație medie de 0,13, petrolul explică puțin din aceste acțiuni, iar ambele acoperiri măresc riscul coșului în afara eșantionului. Riscul lor ține de reglementare și de piața locală.",
                "incorrectExplanation": "În această replicare, o modificare negativă a varianței înseamnă risc mai mare, nu mai mic; parametrii DCC persistenți arată doar că acea corelație se modifică lent, nu că ar fi mare."
            }
        }
    ]
};
