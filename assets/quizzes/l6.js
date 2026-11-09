// ============================================================
// Quiz bank for lecture id 'l6': Renewables, negative prices and batteries (EN + RO)
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.EMQA_DATA.quizzes['l6'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 2,
            "en": {
                "title": "Merit-order effect",
                "text": "Solar and wind plants offer their output on the day-ahead market, Piața pentru Ziua Următoare (PZU), at a price close to zero. Why does adding such zero-cost supply lower the clearing price?",
                "options": [
                    "It raises demand at midday, because cheap energy attracts more consumers into the market",
                    "Renewables have priority by law, so the clearing price is set to zero whenever they produce",
                    "It shifts the supply curve to the right, pushes dearer offers out of the market and moves the crossing with demand down",
                    "It lowers the price of gas, which is the fuel of the marginal plant in most hours"
                ],
                "correctExplanation": "Zero-cost offers move every dearer offer to the right on the supply curve, so the intersection with the (almost vertical) demand curve slides down: the merit-order effect (Sensfuß, Ragwitz & Genoese, 2008).",
                "incorrectExplanation": "The price is still set where supply crosses demand. Renewables do not change fuel prices or demand; they add volume at the bottom of the supply curve, so a dearer plant is no longer needed and the clearing price falls."
            },
            "ro": {
                "title": "Efectul ordinii de merit",
                "text": "Centralele solare și eoliene își oferă producția în piața pentru ziua următoare (PZU) la un preț apropiat de zero. De ce reduce această ofertă cu cost zero prețul de închidere?",
                "options": [
                    "Crește cererea de la amiază, pentru că energia ieftină atrage mai mulți consumatori în piață",
                    "Sursele regenerabile au prioritate prin lege, așa că prețul de închidere este zero ori de cîte ori produc",
                    "Deplasează curba ofertei spre dreapta, împinge în afara pieței ofertele mai scumpe și coboară intersecția cu cererea",
                    "Reduce prețul gazelor, combustibilul centralei marginale în majoritatea orelor"
                ],
                "correctExplanation": "Ofertele cu cost zero mută spre dreapta toate ofertele mai scumpe de pe curba ofertei, iar intersecția cu curba cererii, aproape verticală, coboară: efectul ordinii de merit (Sensfuß, Ragwitz & Genoese, 2008).",
                "incorrectExplanation": "Prețul se formează tot la intersecția ofertei cu cererea. Sursele regenerabile nu schimbă prețul combustibililor sau cererea; ele adaugă volum la baza curbei ofertei, așa că o centrală mai scumpă nu mai este necesară și prețul scade."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Steep local supply curve",
                "text": "On the curves of the Romanian market operator (OPCOM) for 21 Oct 2026, 12:00–12:15, the price was 152.23 EUR/MWh (euro per megawatt-hour) and only 34 MW (megawatts) were offered between 1 EUR/MWh and that price. Using $\\mathrm dp^*/\\mathrm dX=-1/(S'(p^*)-D'(p^*))$, what does this imply?",
                "options": [
                    "The curve was very steep, so a small extra volume at zero price moves the price a lot",
                    "The curve was very flat, so a new park would barely move the price",
                    "The price was set by demand alone, so new supply cannot change it",
                    "Only 34 MW of new solar could ever be accepted in that quarter-hour"
                ],
                "correctExplanation": "Few MW between 1 EUR/MWh and the price means a small slope $S'$ near the price, hence a large $|\\mathrm dp^*/\\mathrm dX|$: the curve was very steep and a small extra volume moves the price a lot.",
                "incorrectExplanation": "The effect of extra supply is the inverse of the slopes of the two curves near the price. Little volume close to the price means a steep curve and a large price change per extra MW, not a small one."
            },
            "ro": {
                "title": "Curba locală abruptă",
                "text": "Pe curbele operatorului pieței din România (OPCOM) din 21 octombrie 2026, pentru 12:00–12:15, prețul a fost 152,23 EUR/MWh (euro pe megawatt-oră) și doar 34 MW (megawați) au fost oferiți între 1 EUR/MWh și acest preț. Folosind $\\mathrm dp^*/\\mathrm dX=-1/(S'(p^*)-D'(p^*))$, ce înseamnă acest lucru?",
                "options": [
                    "Curba era foarte abruptă, deci un volum mic în plus la preț zero schimbă mult prețul",
                    "Curba era foarte plată, deci un parc nou abia ar mișca prețul",
                    "Prețul era fixat numai de cerere, deci oferta nouă nu îl poate schimba",
                    "În acel sfert de oră nu puteau fi acceptați niciodată mai mult de 34 MW solari noi"
                ],
                "correctExplanation": "Puțini MW între 1 EUR/MWh și preț înseamnă o pantă $S'$ mică în jurul prețului, deci un $|\\mathrm dp^*/\\mathrm dX|$ mare: curba era foarte abruptă, iar un volum mic în plus schimbă mult prețul.",
                "incorrectExplanation": "Efectul ofertei suplimentare este inversul pantelor celor două curbe în jurul prețului. Puțin volum aproape de preț înseamnă o curbă abruptă și o schimbare mare de preț pentru fiecare MW în plus, nu una mică."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Megawatts needed in the evening",
                "text": "On the OPCOM (Romanian market operator) curves of 21 Oct 2026, 40 MW (megawatts) more at zero price push the midday price below 50 EUR/MWh (euro per megawatt-hour). How many MW does the same fall require in the evening, and why?",
                "options": [
                    "40 MW, because the merit-order effect does not depend on the time of day",
                    "About 100 MW, because evening demand is roughly twice as high",
                    "1,054 MW, because all net imports must first be displaced",
                    "225 MW, because 1,054 MW of net imports make the evening curve deeper"
                ],
                "correctExplanation": "In the evening the same fall requires 225 MW, because 1,054 MW of net imports make the curve deeper: more volume sits close to the price, so each extra MW moves it less.",
                "incorrectExplanation": "The effect depends on the depth of the curves near the price. The evening book was much deeper, thanks to imports, so 225 MW were needed; 1,054 MW is the size of the net imports, not the volume needed for the fall."
            },
            "ro": {
                "title": "Puterea necesară seara",
                "text": "Pe curbele OPCOM (operatorul pieței din România) din 21 octombrie 2026, 40 MW (megawați) în plus la preț zero duc prețul de la amiază sub 50 EUR/MWh (euro pe megawatt-oră). Cîți MW sînt necesari seara pentru aceeași scădere și de ce?",
                "options": [
                    "40 MW, pentru că efectul ordinii de merit nu depinde de ora din zi",
                    "Circa 100 MW, pentru că cererea de seară este de aproximativ două ori mai mare",
                    "1 054 MW, pentru că trebuie înlocuit întîi tot importul net",
                    "225 MW, pentru că importul net de 1 054 MW adîncește curba de seară"
                ],
                "correctExplanation": "Seara, pentru aceeași scădere sînt necesari 225 MW, deoarece importul net de 1 054 MW adîncește curba: mai mult volum se află aproape de preț, așa că fiecare MW în plus îl mișcă mai puțin.",
                "incorrectExplanation": "Efectul depinde de profunzimea curbelor în jurul prețului. Seara, datorită importului, curba era mult mai adîncă, deci au fost necesari 225 MW; 1 054 MW este importul net, nu volumul necesar pentru scădere."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Order-book effect as an upper bound",
                "text": "On the OPCOM (Romanian market operator) curves of 21 Oct 2026, 25 MW (megawatts) more at zero price lower the midday price from 152.23 to 131.40 EUR/MWh (euro per megawatt-hour). Is this what a new 25 MW solar park does to the Romanian price?",
                "options": [
                    "Yes: the order book is the real market, so the recomputation gives the exact effect",
                    "No: the recomputation holds cross-border flows fixed; in the coupled market part of the extra output is exported, so the true effect is smaller",
                    "No: the true effect is larger, because the regression shows about 43 EUR/MWh per 25 MW",
                    "Yes, but only on days with negative prices, when exports are blocked"
                ],
                "correctExplanation": "The recomputation holds cross-border flows, block orders and hourly orders at their accepted values. In the real coupled market part of any extra midday output is exported, so the Romanian price falls by less; the regression gives about 27 EUR/MWh per GW.",
                "incorrectExplanation": "The order-book exercise is an upper bound: it shows how thin the purely local midday book is. Interconnectors give the midday price its depth, so a real 25 MW park moves the price far less."
            },
            "ro": {
                "title": "Efectul calculat pe ofertele locale ca limită superioară",
                "text": "Pe curbele OPCOM (operatorul pieței din România) din 21 octombrie 2026, 25 MW (megawați) în plus la preț zero coboară prețul de la amiază de la 152,23 la 131,40 EUR/MWh (euro pe megawatt-oră). Acesta este efectul unui parc solar nou de 25 MW asupra prețului din România?",
                "options": [
                    "Da: ofertele sînt piața reală, deci recalcularea dă efectul exact",
                    "Nu: recalcularea păstrează fixe fluxurile transfrontaliere; în piața cuplată o parte din producția suplimentară se exportă, deci efectul real este mai mic",
                    "Nu: efectul real este mai mare, pentru că regresia arată circa 43 EUR/MWh pentru 25 MW",
                    "Da, dar numai în zilele cu prețuri negative, cînd exportul este blocat"
                ],
                "correctExplanation": "Recalcularea păstrează fluxurile transfrontaliere, blocurile și ordinele orare la valorile acceptate. În piața cuplată reală, o parte din producția suplimentară de la amiază se exportă, deci prețul din România scade mai puțin; regresia dă aproximativ 27 EUR/MWh pentru fiecare GW.",
                "incorrectExplanation": "Exercițiul pe oferte este o limită superioară: arată cît de subțire este piața strict locală la amiază. Interconexiunile dau profunzime prețului de la amiază, așa că un parc real de 25 MW mișcă prețul mult mai puțin."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Solar coefficient in the regression",
                "text": "The lecture regresses the hourly Romanian price on load, wind and solar output (in GW, gigawatts), with month, clock-hour and weekday fixed effects, estimated by ordinary least squares (OLS) on 33,600 hours from 2023 to Oct 2026. By how much does each GW of solar lower the price?",
                "options": [
                    "By 15.3 EUR/MWh (euro per megawatt-hour)",
                    "By 40.7 EUR/MWh",
                    "By 26.7 EUR/MWh",
                    "By 43.3 EUR/MWh"
                ],
                "correctExplanation": "Each GW of solar lowers the price by 26.7 EUR/MWh (standard error 2.2), each GW of wind by 15.3, and each GW of load raises it by 40.7; the fit is $R^2$ = 0.65.",
                "incorrectExplanation": "15.3 is the wind coefficient, 40.7 the load coefficient (with a positive sign), and 43.3 EUR/MWh is the effect of the mean midday solar output of 1.62 GW in 2026, not of one GW."
            },
            "ro": {
                "title": "Coeficientul solarului în regresie",
                "text": "Cursul estimează o regresie a prețului orar din România pe consum, producția eoliană și producția solară (în GW, gigawați), cu efecte fixe pentru lună, ora din zi și ziua săptămînii, prin metoda celor mai mici pătrate (OLS, ordinary least squares), pe 33 600 de ore din 2023 pînă în octombrie 2026. Cu cît reduce prețul fiecare GW solar?",
                "options": [
                    "Cu 15,3 EUR/MWh (euro pe megawatt-oră)",
                    "Cu 40,7 EUR/MWh",
                    "Cu 26,7 EUR/MWh",
                    "Cu 43,3 EUR/MWh"
                ],
                "correctExplanation": "Fiecare GW solar reduce prețul cu 26,7 EUR/MWh (eroare standard 2,2), fiecare GW eolian cu 15,3, iar fiecare GW de consum îl crește cu 40,7; $R^2$ = 0,65.",
                "incorrectExplanation": "15,3 este coeficientul eolianului, 40,7 coeficientul consumului (cu semn pozitiv), iar 43,3 EUR/MWh este efectul producției solare medii de la amiază din 2026, de 1,62 GW, nu al unui singur GW."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Midday solar effect by hand",
                "text": "The regression gives −26.7 EUR/MWh (euro per megawatt-hour) per GW (gigawatt) of solar. At midday in 2026 the mean Romanian solar output was 1.62 GW. Roughly how much lower is the midday price associated with this solar output?",
                "options": [
                    "About 43 EUR/MWh",
                    "About 27 EUR/MWh",
                    "About 16 EUR/MWh",
                    "About 66 EUR/MWh"
                ],
                "correctExplanation": "$1.62\\times 26.7\\approx 43.3$ EUR/MWh, the figure reported in the lecture for midday in 2026.",
                "incorrectExplanation": "Multiply the coefficient per GW by the GW actually produced: $1.62\\times 26.7\\approx 43.3$. 27 is the effect of one GW only, and 16 or 66 come from dividing instead of multiplying or from adding the load coefficient."
            },
            "ro": {
                "title": "Efectul solarului la amiază",
                "text": "Regresia dă −26,7 EUR/MWh (euro pe megawatt-oră) pentru fiecare GW (gigawatt) solar. La amiază, în 2026, producția solară medie a României a fost de 1,62 GW. Cu aproximativ cît este mai mic prețul de la amiază asociat acestei producții?",
                "options": [
                    "Cu circa 43 EUR/MWh",
                    "Cu circa 27 EUR/MWh",
                    "Cu circa 16 EUR/MWh",
                    "Cu circa 66 EUR/MWh"
                ],
                "correctExplanation": "$1{,}62\\times 26{,}7\\approx 43{,}3$ EUR/MWh, valoarea raportată în curs pentru amiaza din 2026.",
                "incorrectExplanation": "Coeficientul pe GW se înmulțește cu numărul de GW produși efectiv: $1{,}62\\times 26{,}7\\approx 43{,}3$. 27 este efectul unui singur GW, iar 16 sau 66 provin din împărțire în loc de înmulțire sau din adunarea coeficientului consumului."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Association and causation",
                "text": "In the price regression, $\\alpha_{m(t)}$ is a constant for the month of hour $t$. What does it absorb, and why is the solar coefficient still read as an association rather than a causal effect?",
                "options": [
                    "It absorbs the clock-hour pattern; the coefficient is causal because the hour is fixed",
                    "It absorbs the weather; the coefficient is not causal because solar is measured with error",
                    "It absorbs cross-border flows; the coefficient is causal because flows are controlled",
                    "It absorbs fuel and carbon prices; the regression controls for the calendar, not for everything that moves with sunshine"
                ],
                "correctExplanation": "The month constant absorbs fuel and carbon prices. The regression controls for the calendar (month, clock hour, weekday), but not for everything that moves with sunshine, so the coefficient is an association (Cludius et al., 2014; Würzburg et al., 2013).",
                "incorrectExplanation": "The clock hour has its own constant $\\gamma_{h(t)}$ and flows are not in the model. Fixed effects remove calendar patterns only; other variables that move with sunshine may still be picked up by the solar coefficient."
            },
            "ro": {
                "title": "Asocierea și cauzalitatea",
                "text": "În regresia prețului, $\\alpha_{m(t)}$ este o constantă pentru luna orei $t$. Ce preia ea și de ce coeficientul solarului se citește totuși ca o asociere, nu ca un efect cauzal?",
                "options": [
                    "Preia profilul orei din zi; coeficientul este cauzal pentru că ora este fixată",
                    "Preia vremea; coeficientul nu este cauzal pentru că producția solară este măsurată cu erori",
                    "Preia fluxurile transfrontaliere; coeficientul este cauzal pentru că fluxurile sînt controlate",
                    "Preia prețul gazelor și al carbonului; regresia controlează calendarul, nu tot ce variază odată cu soarele"
                ],
                "correctExplanation": "Constanta lunii preia prețul gazelor și al carbonului. Regresia controlează calendarul (luna, ora, ziua săptămînii), dar nu tot ce variază odată cu soarele, așa că coeficientul este o asociere (Cludius et al., 2014; Würzburg et al., 2013).",
                "incorrectExplanation": "Ora din zi are propria constantă $\\gamma_{h(t)}$, iar fluxurile nu sînt în model. Efectele fixe elimină doar tiparele de calendar; alte variabile care variază odată cu soarele pot fi preluate de coeficientul solarului."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Low residual-load hours",
                "text": "Residual load is load minus wind minus solar, $L_t-W_t-S_t$. What share of all hours had a residual load below 2 GW (gigawatts) in Romania in 2026, against 0.1% in 2023?",
                "options": [
                    "0.6%",
                    "9.0%",
                    "28.3%",
                    "2.3%"
                ],
                "correctExplanation": "Hours with residual load below 2 GW were 0.1% of all hours in 2023 and 9.0% in 2026: the cheap left end of the price curve, once rare, is now common.",
                "incorrectExplanation": "0.6% was the share in 2025; 28.3 EUR/MWh is the price rise per extra GW of residual load, and 2.3% is solar's share of load in 2019."
            },
            "ro": {
                "title": "Ore cu consum rezidual mic",
                "text": "Consumul rezidual este consumul minus producția eoliană și cea solară, $L_t-W_t-S_t$. Ce pondere din totalul orelor a avut în România, în 2026, un consum rezidual sub 2 GW (gigawați), față de 0,1% în 2023?",
                "options": [
                    "0,6%",
                    "9,0%",
                    "28,3%",
                    "2,3%"
                ],
                "correctExplanation": "Orele cu consum rezidual sub 2 GW reprezentau 0,1% din total în 2023 și 9,0% în 2026: partea stîngă, ieftină, a curbei prețului, odinioară rară, a devenit obișnuită.",
                "incorrectExplanation": "0,6% a fost ponderea din 2025; 28,3 EUR/MWh este creșterea prețului pentru fiecare GW de consum rezidual în plus, iar 2,3% este ponderea solarului în consum în 2019."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Definition of capture price",
                "text": "What is the capture price (CP) of a solar park?",
                "options": [
                    "The simple mean of the day-ahead price over all intervals of the year",
                    "The mean price of the daylight hours, from sunrise to sunset",
                    "The mean price weighted by the plant's own output in each interval",
                    "The price fixed in the park's power purchase agreement (PPA)"
                ],
                "correctExplanation": "$\\mathrm{CP}=\\sum_t P_tG_t\\Delta_t/\\sum_t G_t\\Delta_t$: the price of each interval weighted by the energy the plant produces in it. The simple mean is the baseload price $B$.",
                "incorrectExplanation": "A park is paid the price of the intervals in which it produces, in proportion to how much it produces. The simple mean is the baseload price, and an unweighted daylight mean ignores that output peaks at midday."
            },
            "ro": {
                "title": "Definiția prețului capturat",
                "text": "Ce este prețul capturat (CP, capture price) al unui parc solar?",
                "options": [
                    "Media simplă a prețului pentru ziua următoare pe toate intervalele anului",
                    "Prețul mediu al orelor de zi, de la răsărit la apus",
                    "Prețul mediu ponderat cu producția centralei în fiecare interval",
                    "Prețul fixat în contractul pe termen lung al parcului (PPA, power purchase agreement)"
                ],
                "correctExplanation": "$\\mathrm{CP}=\\sum_t P_tG_t\\Delta_t/\\sum_t G_t\\Delta_t$: prețul fiecărui interval ponderat cu energia produsă de centrală în acel interval. Media simplă este prețul de bază $B$.",
                "incorrectExplanation": "Un parc încasează prețul intervalelor în care produce, proporțional cu cît produce. Media simplă este prețul de bază, iar o medie neponderată a orelor de zi ignoră faptul că producția este maximă la amiază."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Capture rate of solar 2026",
                "text": "For Romanian solar in Jan–Oct 2026, the capture price (CP) was 85.0 EUR/MWh (euro per megawatt-hour) and the baseload price $B$ was 137.5 EUR/MWh. What is the capture rate (CR)?",
                "options": [
                    "61.9%",
                    "161.8%",
                    "52.4%",
                    "38.1%"
                ],
                "correctExplanation": "$\\mathrm{CR}=\\mathrm{CP}/B=85.0/137.5\\approx 61.9\\%$.",
                "incorrectExplanation": "The capture rate is CP divided by $B$, not the inverse (161.8%) and not one minus the ratio (38.1%). 52.4 is the profile discount $B-\\mathrm{CP}$ in EUR/MWh, not a rate."
            },
            "ro": {
                "title": "Rata de captare solară 2026",
                "text": "Pentru solarul din România, în ianuarie–octombrie 2026, prețul capturat (CP) a fost 85,0 EUR/MWh (euro pe megawatt-oră), iar prețul de bază $B$ 137,5 EUR/MWh. Care este rata de captare (CR)?",
                "options": [
                    "61,9%",
                    "161,8%",
                    "52,4%",
                    "38,1%"
                ],
                "correctExplanation": "$\\mathrm{CR}=\\mathrm{CP}/B=85{,}0/137{,}5\\approx 61{,}9\\%$.",
                "incorrectExplanation": "Rata de captare este CP împărțit la $B$, nu raportul invers (161,8%) și nici unu minus raportul (38,1%). 52,4 este reducerea datorată profilului, $B-\\mathrm{CP}$, în EUR/MWh, nu o rată."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Capture rate and covariance",
                "text": "The capture rate (CR) can be written as $\\mathrm{CR}=1+\\mathrm{Cov}_\\Delta(P,G)/(\\bar P\\,\\bar G)$. When is the capture rate below one?",
                "options": [
                    "When the plant produces more in winter than in summer",
                    "When the mean price $\\bar P$ is higher than the mean output $\\bar G$",
                    "When price and output are uncorrelated but output is volatile",
                    "When output is high in cheap intervals, that is, when price and output are negatively correlated"
                ],
                "correctExplanation": "With positive $\\bar P$ and $\\bar G$, CR is below one exactly when the covariance is negative: the plant produces most when prices are low. For Romanian solar in 2026 the correlation was −0.43.",
                "incorrectExplanation": "Only the sign of the covariance between price and output matters. Zero correlation gives CR = 1 however volatile output is, and comparing the levels of price and output in different units means nothing."
            },
            "ro": {
                "title": "Rata de captare și covarianța",
                "text": "Rata de captare (CR) se poate scrie $\\mathrm{CR}=1+\\mathrm{Cov}_\\Delta(P,G)/(\\bar P\\,\\bar G)$. Cînd este rata de captare sub unu?",
                "options": [
                    "Cînd centrala produce mai mult iarna decît vara",
                    "Cînd prețul mediu $\\bar P$ este mai mare decît producția medie $\\bar G$",
                    "Cînd prețul și producția sînt necorelate, dar producția este volatilă",
                    "Cînd producția este mare în intervalele ieftine, adică prețul și producția sînt corelate negativ"
                ],
                "correctExplanation": "Cu $\\bar P$ și $\\bar G$ pozitive, CR este sub unu exact atunci cînd covarianța este negativă: centrala produce cel mai mult cînd prețurile sînt mici. Pentru solarul din România, în 2026, corelația a fost −0,43.",
                "incorrectExplanation": "Contează doar semnul covarianței dintre preț și producție. O corelație nulă dă CR = 1 oricît de volatilă ar fi producția, iar compararea nivelurilor prețului și producției, în unități diferite, nu are sens."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Capture rate of wind",
                "text": "In Jan–Oct 2026 Romanian wind had a capture rate (CR) of 103.0%, while solar had 61.9%. Which explanation does the lecture give?",
                "options": [
                    "Wind receives a support payment per MWh (megawatt-hour) that is included in its capture price",
                    "Wind also blows at night and in winter, when prices are high, and Romanian wind output did not grow",
                    "Wind parks switch off at every negative price, while solar parks cannot",
                    "Wind is sold mostly through intraday trading, at higher prices than the day-ahead market"
                ],
                "correctExplanation": "Wind blows also at night and in winter, when prices are high, and Romanian wind output did not grow; its CR moves between 88% and 103% with no trend. Cannibalisation belongs to a technology whose output is concentrated in the same hours and grows fast.",
                "incorrectExplanation": "The capture rate uses only market prices weighted by output, so support payments and switching off do not explain it. The difference is the timing of output: solar is concentrated at midday, wind is not."
            },
            "ro": {
                "title": "Rata de captare a producției eoliene",
                "text": "În ianuarie–octombrie 2026, eolianul din România a avut o rată de captare (CR) de 103,0%, iar solarul de 61,9%. Ce explicație dă cursul?",
                "options": [
                    "Eolianul primește un sprijin pe MWh (megawatt-oră), inclus în prețul său capturat",
                    "Vîntul bate și noaptea, și iarna, cînd prețurile sînt mari, iar producția eoliană a României nu a crescut",
                    "Parcurile eoliene se opresc la fiecare preț negativ, iar cele solare nu pot",
                    "Eolianul se vinde mai ales în piața intrazilnică, la prețuri mai mari decît în piața pentru ziua următoare"
                ],
                "correctExplanation": "Vîntul bate și noaptea, și iarna, cînd prețurile sînt mari, iar producția eoliană a României nu a crescut; rata lui de captare variază între 88% și 103%, fără tendință. Canibalizarea ține de o tehnologie a cărei producție se concentrează în aceleași ore și crește repede.",
                "incorrectExplanation": "Rata de captare folosește doar prețurile pieței, ponderate cu producția, deci nici sprijinul, nici oprirea nu o explică. Diferența vine din momentul producției: solarul este concentrat la amiază, eolianul nu."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Solar capture rate trend",
                "text": "How did the yearly capture rate (CR) of Romanian solar evolve between 2019 and 2025?",
                "options": [
                    "It stayed close to 100% throughout, like wind",
                    "It fell only during the 2022 energy crisis and then recovered",
                    "It fell from 104.5% in 2019 to 59.4% in 2025, with the fall starting in 2023 as solar output grew",
                    "It fell from 92.2% in 2019 to 80.2% in 2025"
                ],
                "correctExplanation": "Solar earned slightly more than the average price in 2019 (104.5%); the fall starts in 2023 together with the growth of solar output and reaches 59.4% in 2025.",
                "incorrectExplanation": "2022 had very high prices for every technology and a solar CR of 99.5%, so it says little about cannibalisation; 92.2% is the 2020 value and 80.2% the 2023 value."
            },
            "ro": {
                "title": "Evoluția ratei de captare solare",
                "text": "Cum a evoluat rata anuală de captare (CR) a solarului din România între 2019 și 2025?",
                "options": [
                    "A rămas aproape de 100% în toată perioada, ca la eolian",
                    "A scăzut doar în criza energetică din 2022, apoi și-a revenit",
                    "A scăzut de la 104,5% în 2019 la 59,4% în 2025, iar scăderea a început în 2023, odată cu creșterea producției solare",
                    "A scăzut de la 92,2% în 2019 la 80,2% în 2025"
                ],
                "correctExplanation": "În 2019, solarul a obținut puțin peste prețul mediu (104,5%); scăderea începe în 2023, odată cu creșterea producției solare, și ajunge la 59,4% în 2025.",
                "incorrectExplanation": "Anul 2022 a avut prețuri foarte mari pentru toate tehnologiile și o rată solară de 99,5%, așa că spune puțin despre canibalizare; 92,2% este valoarea din 2020, iar 80,2% cea din 2023."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Profile discount of all solar",
                "text": "In 2025 Romanian solar plants produced 2.72 terawatt-hours (TWh), and a solar megawatt-hour (MWh) earned 43.9 EUR less than the baseload price (the profile discount $B-\\mathrm{CP}$, baseload price minus capture price). Roughly how much revenue does this discount represent for all Romanian solar output in 2025?",
                "options": [
                    "About 119 million EUR",
                    "About 11.9 million EUR",
                    "About 175 million EUR",
                    "About 1.19 billion EUR"
                ],
                "correctExplanation": "2.72 TWh = 2,720,000 MWh, and $2{,}720{,}000\\times 43.9\\approx 119$ million EUR: the amount solar would have earned in addition at the baseload price.",
                "incorrectExplanation": "One TWh is one million MWh; 175 million EUR is the revenue at the solar capture price of 64.2 EUR/MWh, not the discount, and the other values misplace the factor of ten."
            },
            "ro": {
                "title": "Reducerea de profil pentru tot solarul",
                "text": "În 2025, centralele solare din România au produs 2,72 terawați-oră (TWh), iar un megawatt-oră (MWh) solar a obținut cu 43,9 EUR mai puțin decît prețul de bază (reducerea datorată profilului, $B-\\mathrm{CP}$, prețul de bază minus prețul captat). Ce venit reprezintă, aproximativ, această reducere pentru întreaga producție solară a României în 2025?",
                "options": [
                    "Circa 119 milioane EUR",
                    "Circa 11,9 milioane EUR",
                    "Circa 175 milioane EUR",
                    "Circa 1,19 miliarde EUR"
                ],
                "correctExplanation": "2,72 TWh = 2 720 000 MWh, iar $2\\,720\\,000\\times 43{,}9\\approx 119$ milioane EUR: suma pe care solarul ar fi obținut-o în plus la prețul de bază.",
                "incorrectExplanation": "Un TWh înseamnă un milion de MWh; 175 de milioane EUR este venitul la prețul captat al solarului, 64,2 EUR/MWh, nu reducerea, iar celelalte valori greșesc un factor de zece."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Pricing a solar PPA",
                "text": "A buyer is offered a solar power purchase agreement (PPA) at the 2025 baseload price of 108 EUR/MWh (euro per megawatt-hour). With a 2025 solar capture rate (CR) of 59%, what did the solar profile really earn on the day-ahead market?",
                "options": [
                    "About 108 EUR/MWh, because a PPA fixes the price",
                    "About 64 EUR/MWh, so a buyer paying baseload for the solar profile pays a large premium",
                    "About 44 EUR/MWh, the profile discount",
                    "About 183 EUR/MWh, because solar is scarce at midday"
                ],
                "correctExplanation": "$108\\times 0.59\\approx 64$ EUR/MWh: the solar profile earned about 64 EUR/MWh in 2025. A solar PPA should be priced on the capture price, not on the baseload price.",
                "incorrectExplanation": "The value of the energy delivered is its capture price, baseload times capture rate. 44 EUR/MWh is the discount itself, not the price, and 183 EUR/MWh comes from dividing by the capture rate instead of multiplying."
            },
            "ro": {
                "title": "Prețul unui PPA solar",
                "text": "Unui cumpărător i se oferă un contract pe termen lung pentru energie solară (PPA, power purchase agreement) la prețul de bază din 2025, de 108 EUR/MWh (euro pe megawatt-oră). Cu o rată de captare (CR) solară de 59% în 2025, cît a obținut de fapt profilul solar în piața pentru ziua următoare?",
                "options": [
                    "Circa 108 EUR/MWh, pentru că un PPA fixează prețul",
                    "Circa 64 EUR/MWh, deci cumpărătorul care plătește prețul de bază pentru profilul solar plătește o primă mare",
                    "Circa 44 EUR/MWh, reducerea datorată profilului",
                    "Circa 183 EUR/MWh, pentru că solarul este rar la amiază"
                ],
                "correctExplanation": "$108\\times 0{,}59\\approx 64$ EUR/MWh: profilul solar a obținut circa 64 EUR/MWh în 2025. Prețul unui PPA solar trebuie să pornească de la prețul capturat, nu de la prețul de bază.",
                "incorrectExplanation": "Valoarea energiei livrate este prețul ei capturat, adică prețul de bază înmulțit cu rata de captare. 44 EUR/MWh este reducerea, nu prețul, iar 183 EUR/MWh provine din împărțirea la rata de captare în loc de înmulțire."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Cannibalisation slope",
                "text": "The regression $\\mathrm{CR}_m=a+b\\,s_m+u_m$ on 94 months gives $\\hat b$ = −4.20 for Romania, where $\\mathrm{CR}_m$ is the monthly solar capture rate (CR) in percent and $s_m$ solar output as a percentage of load. If solar's share of monthly load rises from 5% to 8%, by roughly how much does the expected capture rate change?",
                "options": [
                    "It falls by about 4.2 points",
                    "It falls by about 3 points",
                    "It falls by about 12.6 points",
                    "It falls by about 42 points"
                ],
                "correctExplanation": "Three extra percentage points of solar share times −4.20 points each give about −12.6 points of capture rate.",
                "incorrectExplanation": "The slope is per percentage point of solar share: multiply −4.20 by the 3-point rise. 4.2 is the effect of one point only, and 3 ignores the slope."
            },
            "ro": {
                "title": "Panta canibalizării",
                "text": "Regresia $\\mathrm{CR}_m=a+b\\,s_m+u_m$ pe 94 de luni dă $\\hat b$ = −4,20 pentru România, unde $\\mathrm{CR}_m$ este rata de captare (CR) solară lunară, în procente, iar $s_m$ producția solară ca procent din consum. Dacă ponderea solarului în consumul lunii crește de la 5% la 8%, cu aproximativ cît se modifică rata de captare așteptată?",
                "options": [
                    "Scade cu circa 4,2 puncte",
                    "Scade cu circa 3 puncte",
                    "Scade cu circa 12,6 puncte",
                    "Scade cu circa 42 de puncte"
                ],
                "correctExplanation": "Trei puncte procentuale în plus ale ponderii solarului, înmulțite cu −4,20 puncte fiecare, dau circa −12,6 puncte de rată de captare.",
                "incorrectExplanation": "Panta este pe punct procentual de pondere solară: −4,20 se înmulțește cu creșterea de 3 puncte. 4,2 este efectul unui singur punct, iar 3 ignoră panta."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Steepest slope in Romania",
                "text": "The cannibalisation slope of the solar capture rate (CR) on solar's share of load is −4.20 for Romania, −2.14 for Hungary and −1.32 for Bulgaria. Why is the Romanian slope the steepest, according to the lecture?",
                "options": [
                    "Romanian solar parks are older and less efficient than those of the neighbours",
                    "Romania has no interconnectors, so its midday surplus cannot be exported",
                    "Romanian wind output falls in sunny months, which lowers the capture rate",
                    "Romanian prices also fall with the neighbours' solar, which grows together with Romanian solar, so the regression attributes part of the regional effect to the Romanian share"
                ],
                "correctExplanation": "Coupled markets share the midday surplus. Bulgarian and Hungarian solar grew together with Romanian solar, so the Romanian share also proxies regional solar and its slope picks up part of the regional effect (López Prol, Steininger & Zilberman, 2020).",
                "incorrectExplanation": "Romania is coupled with its neighbours and exports at midday. The steep slope reflects an omitted regional driver correlated with the Romanian share; hence forecast regional solar, not only Romanian solar."
            },
            "ro": {
                "title": "Panta cea mai abruptă în România",
                "text": "Panta canibalizării, adică a ratei de captare (CR) solare în funcție de ponderea solarului în consum, este −4,20 pentru România, −2,14 pentru Ungaria și −1,32 pentru Bulgaria. De ce este panta României cea mai abruptă, potrivit cursului?",
                "options": [
                    "Parcurile solare din România sînt mai vechi și mai puțin eficiente decît ale vecinilor",
                    "România nu are interconexiuni, deci surplusul de la amiază nu poate fi exportat",
                    "Producția eoliană a României scade în lunile însorite, ceea ce reduce rata de captare",
                    "Prețul din România scade și cu producția solară a vecinilor, care crește odată cu cea românească, iar regresia atribuie o parte din efectul regional ponderii României"
                ],
                "correctExplanation": "Piețele cuplate își împart surplusul de la amiază. Solarul din Bulgaria și Ungaria a crescut odată cu cel din România, așa că ponderea României ține loc și pentru solarul regional, iar panta preia o parte din efectul regional (López Prol, Steininger & Zilberman, 2020).",
                "incorrectExplanation": "România este cuplată cu vecinii și exportă la amiază. Panta abruptă reflectă un factor regional omis, corelat cu ponderea României; de aceea trebuie prognozat solarul regiunii, nu doar cel al României."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Bulgarian capture rate in 2026",
                "text": "In 2026 the Bulgarian solar capture rate (CR) rose to 77.1%, from 68.6% in 2025, at the same time as the Bulgarian battery fleet grew. Which mechanism does the lecture consider plausible?",
                "options": [
                    "Batteries charging at midday add demand exactly when solar produces and lift the midday price",
                    "Batteries discharging at midday add supply and raise the solar share of load",
                    "Batteries replace solar parks, so less solar is cannibalised",
                    "Batteries raise evening prices, and the capture rate uses evening prices"
                ],
                "correctExplanation": "Charging adds demand at midday, when solar produces, and lifts the midday price. The lecture calls this an association, not a proof, but the mechanism is plausible: solar gains from other people's batteries.",
                "incorrectExplanation": "Batteries charge, not discharge, at midday, and the solar capture price is weighted by solar output, which is mostly at midday; the link is extra midday demand, not evening prices."
            },
            "ro": {
                "title": "Rata de captare din Bulgaria în 2026",
                "text": "În 2026, rata de captare (CR) solară din Bulgaria a urcat la 77,1%, de la 68,6% în 2025, în paralel cu extinderea bateriilor bulgărești. Ce mecanism consideră cursul plauzibil?",
                "options": [
                    "Bateriile care se încarcă la amiază adaugă cerere exact cînd produce solarul și ridică prețul de la prînz",
                    "Bateriile care se descarcă la amiază adaugă ofertă și cresc ponderea solarului în consum",
                    "Bateriile înlocuiesc parcurile solare, deci mai puțin solar este canibalizat",
                    "Bateriile cresc prețul de seară, iar rata de captare folosește prețurile de seară"
                ],
                "correctExplanation": "Încărcarea adaugă cerere la amiază, cînd produce solarul, și ridică prețul de la prînz. Cursul o numește o asociere, nu o dovadă, dar mecanismul este plauzibil: un parc solar cîștigă și din bateriile altora.",
                "incorrectExplanation": "Bateriile se încarcă, nu se descarcă, la amiază, iar prețul capturat solar este ponderat cu producția solară, concentrată la amiază; legătura este cererea suplimentară de la prînz, nu prețul de seară."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Solar in the cheapest hours",
                "text": "Ranking the hours of each year from the cheapest, what share of Romanian solar output was produced in the cheapest 10% of hours in 2025?",
                "options": [
                    "10%, as for any evenly spread output",
                    "32.1%",
                    "7.6%",
                    "9.6%"
                ],
                "correctExplanation": "In 2025 the cheapest 10% of hours carried 32.1% of Romanian solar output, against 7.6% in 2019 and 23.4% in 2026; evenly spread output would put 10% there.",
                "incorrectExplanation": "7.6% is the 2019 value and 9.6% the share of 2025 solar output produced at zero or negative prices. A large and growing part of solar energy is sold precisely when electricity is worth least."
            },
            "ro": {
                "title": "Solarul în orele cele mai ieftine",
                "text": "Ordonînd orele fiecărui an de la cea mai ieftină, ce parte din producția solară a României s-a realizat în 2025 în cele mai ieftine 10% dintre ore?",
                "options": [
                    "10%, ca pentru orice producție distribuită uniform",
                    "32,1%",
                    "7,6%",
                    "9,6%"
                ],
                "correctExplanation": "În 2025, cele mai ieftine 10% dintre ore au conținut 32,1% din producția solară a României, față de 7,6% în 2019 și 23,4% în 2026; o producție distribuită uniform ar pune acolo 10%.",
                "incorrectExplanation": "7,6% este valoarea din 2019, iar 9,6% este partea producției solare din 2025 realizată la prețuri nule sau negative. O parte mare și în creștere a energiei solare se vinde tocmai cînd energia electrică valorează cel mai puțin."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Gain from switching off by hand",
                "text": "In 2025, producing at negative prices cost Romanian solar parks 1.71 million EUR, on a yearly solar output of 2.72 terawatt-hours (TWh); 6.2% of that output was produced at negative prices. The gain from switching off, $g$, is expressed per megawatt-hour (MWh) of yearly output. What is $g$?",
                "options": [
                    "About 6.3 EUR/MWh",
                    "About 10.1 EUR/MWh",
                    "About 0.63 EUR/MWh",
                    "About 0.063 EUR/MWh"
                ],
                "correctExplanation": "$g=1{,}710{,}000/2{,}720{,}000\\approx 0.63$ EUR/MWh, the lecture's figure. Against a profile discount of 43.9 EUR/MWh, switching off at negative prices recovers very little.",
                "incorrectExplanation": "The gain is spread over the whole yearly output, 2,720,000 MWh. Dividing only by the 6.2% produced at negative prices gives about 10.1 EUR/MWh, the average depth of those prices, not $g$; the other values misplace the decimal point."
            },
            "ro": {
                "title": "Cîștigul din oprire, calculat de mînă",
                "text": "În 2025, producția la prețuri negative a costat parcurile solare din România 1,71 milioane EUR, la o producție solară anuală de 2,72 terawați-oră (TWh); 6,2% din această producție s-a realizat la prețuri negative. Cîștigul din oprire, $g$, se exprimă pe megawatt-oră (MWh) de producție anuală. Cît este $g$?",
                "options": [
                    "Circa 6,3 EUR/MWh",
                    "Circa 10,1 EUR/MWh",
                    "Circa 0,63 EUR/MWh",
                    "Circa 0,063 EUR/MWh"
                ],
                "correctExplanation": "$g=1\\,710\\,000/2\\,720\\,000\\approx 0{,}63$ EUR/MWh, valoarea din curs. Față de o reducere datorată profilului de 43,9 EUR/MWh, oprirea la prețuri negative recuperează foarte puțin.",
                "incorrectExplanation": "Cîștigul se raportează la întreaga producție anuală, 2 720 000 MWh. Împărțirea doar la cei 6,2% produși la prețuri negative dă circa 10,1 EUR/MWh, adîncimea medie a acestor prețuri, nu $g$; celelalte valori greșesc poziția virgulei."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Producers that bid below zero",
                "text": "According to the lecture, which two groups of producers bid below zero on the day-ahead market?",
                "options": [
                    "Gas plants at night and coal plants in summer",
                    "Merchant solar parks without support and battery operators",
                    "Plants that import power and plants that export it",
                    "Plants whose output is paid per MWh (megawatt-hour) by a support scheme or contract, and plants such as nuclear and run-of-river hydro that cannot stop cheaply"
                ],
                "correctExplanation": "Negative bids come from plants paid per MWh produced (support schemes, contracts) and from plants that cannot stop cheaply, such as nuclear and run-of-river hydro (Fanone, Gamba & Prokopczuk, 2013).",
                "incorrectExplanation": "A merchant solar park without support has $b_i\\approx 0$ and should stop as soon as the price turns negative. Negative bids need a per-MWh payment or a high cost of stopping."
            },
            "ro": {
                "title": "Producătorii care ofertează sub zero",
                "text": "Potrivit cursului, care sînt cele două categorii de producători care ofertează sub zero în piața pentru ziua următoare?",
                "options": [
                    "Centralele pe gaze noaptea și cele pe cărbune vara",
                    "Parcurile solare fără sprijin și operatorii de baterii",
                    "Centralele care importă energie și cele care o exportă",
                    "Producătorii plătiți pe MWh (megawatt-oră) printr-o schemă de sprijin sau un contract și centralele care nu se pot opri ieftin, cum sînt cele nucleare și hidrocentralele pe firul apei"
                ],
                "correctExplanation": "Ofertele negative vin de la producătorii plătiți pentru fiecare MWh produs (scheme de sprijin, contracte) și de la centralele care nu se pot opri ieftin, cum sînt cele nucleare și hidrocentralele pe firul apei (Fanone, Gamba & Prokopczuk, 2013).",
                "incorrectExplanation": "Un parc solar fără sprijin are $b_i\\approx 0$ și trebuie să se oprească imediat ce prețul devine negativ. O ofertă negativă presupune o plată pe MWh sau un cost mare al opririi."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Counting negative quarter-hours",
                "text": "Since 1 Oct 2025 the day-ahead market uses a 15-minute market time unit (MTU). From that date to 31 Oct 2026, Romania had 687 negative quarter-hours. How many negative hours should be reported?",
                "options": [
                    "171.75 hour-equivalents",
                    "687 hours",
                    "195 hours",
                    "2,748 hours"
                ],
                "correctExplanation": "With $h^-=\\sum_t\\Delta_t\\,\\mathbf 1[P_t\\lt 0]$ and $\\Delta_t$ = 0.25 h, $687\\times 0.25=171.75$ hour-equivalents. A quarter-hour must never be counted as an hour.",
                "incorrectExplanation": "Each quarter-hour counts 0.25 h. 687 counts quarters as hours, 2,748 multiplies instead of dividing by four, and 195 is the count on hourly averages, which hides some negative quarters."
            },
            "ro": {
                "title": "Numărarea sferturilor negative",
                "text": "De la 1 octombrie 2025, piața pentru ziua următoare folosește un interval de tranzacționare (MTU, market time unit) de 15 minute. De atunci pînă la 31 octombrie 2026, România a avut 687 de sferturi de oră cu preț negativ. Cîte ore cu preț negativ trebuie raportate?",
                "options": [
                    "171,75 ore echivalente",
                    "687 de ore",
                    "195 de ore",
                    "2 748 de ore"
                ],
                "correctExplanation": "Cu $h^-=\\sum_t\\Delta_t\\,\\mathbf 1[P_t\\lt 0]$ și $\\Delta_t$ = 0,25 h, $687\\times 0{,}25=171{,}75$ ore echivalente. Un sfert de oră nu se numără niciodată ca o oră.",
                "incorrectExplanation": "Fiecare sfert de oră contează 0,25 h. 687 numără sferturile ca ore, 2 748 înmulțește în loc să împartă la patru, iar 195 este numărul pe medii orare, care ascunde unele sferturi negative."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Negative hours across markets",
                "text": "Which statement about negative day-ahead prices matches the lecture's counts?",
                "options": [
                    "Romania had more negative hours than Germany in 2025, because its order book is thinner",
                    "Romania had 196 negative hours in 2025 against 575 in Germany, and on Jan–Oct the Romanian count fell to 171.75 in 2026 although solar output grew",
                    "Negative hours in Romania rose every year, reaching 575 in 2025",
                    "Romania had no negative hours before 2025"
                ],
                "correctExplanation": "Germany, with far more solar and wind, had 575 negative hours in 2025, Romania 196. On the same months the Romanian count fell to 171.75 in 2026; possible reasons are a higher price level and more batteries charging at midday.",
                "incorrectExplanation": "Romania's first negative hours appeared in 2023 (32 hours), and the count fell in Jan–Oct 2026 compared with Jan–Oct 2025. Germany, not Romania, had 575."
            },
            "ro": {
                "title": "Ore negative în mai multe piețe",
                "text": "Care afirmație despre prețurile negative din piața pentru ziua următoare corespunde cifrelor din curs?",
                "options": [
                    "România a avut mai multe ore negative decît Germania în 2025, pentru că piața ei este mai subțire",
                    "România a avut 196 de ore negative în 2025, față de 575 în Germania, iar pe ianuarie–octombrie numărul din România a scăzut la 171,75 în 2026, deși producția solară a crescut",
                    "Orele negative din România au crescut în fiecare an și au ajuns la 575 în 2025",
                    "România nu a avut ore negative înainte de 2025"
                ],
                "correctExplanation": "Germania, cu mult mai multă putere solară și eoliană, a avut 575 de ore negative în 2025, România 196. Pe aceleași luni, numărul din România a scăzut la 171,75 în 2026; explicațiile posibile sînt un nivel mai ridicat al prețurilor și mai multe baterii care se încarcă la amiază.",
                "incorrectExplanation": "Primele ore negative din România au apărut în 2023 (32 de ore), iar numărul a scăzut în ianuarie–octombrie 2026 față de ianuarie–octombrie 2025. Germania, nu România, a avut 575."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Value of switching off",
                "text": "In 2025, 6.2% of Romanian solar output was produced at negative prices. The gain from switching off in every negative interval was $g$ = 0.63 EUR/MWh (euro per megawatt-hour) of yearly output. What does the lecture conclude?",
                "options": [
                    "Switching off is the main lever: it recovers most of the gap to the baseload price",
                    "Switching off is never worth installing, because negative prices are too rare",
                    "Switching off saves little compared with the profile discount of 43.9 EUR/MWh; the real loss comes from the many midday hours with low positive prices",
                    "Switching off doubles the capture rate of a solar park"
                ],
                "correctExplanation": "0.63 EUR/MWh is tiny next to the 43.9 EUR/MWh profile discount: the large loss comes from low positive midday prices. Remote switch-off is still worth installing because it is cheap, but a park should be valued on its capture price.",
                "incorrectExplanation": "Negative prices attract attention, but a solar park loses far more in the many midday hours with low, still positive prices, which switching off cannot avoid."
            },
            "ro": {
                "title": "Valoarea opririi parcului",
                "text": "În 2025, 6,2% din producția solară a României s-a realizat la prețuri negative. Cîștigul din oprirea în toate intervalele negative a fost $g$ = 0,63 EUR/MWh (euro pe megawatt-oră) din producția anuală. Ce concluzie trage cursul?",
                "options": [
                    "Oprirea este principala pîrghie: recuperează cea mai mare parte din diferența față de prețul de bază",
                    "Oprirea nu merită niciodată instalată, pentru că prețurile negative sînt prea rare",
                    "Oprirea aduce puțin față de reducerea datorată profilului, de 43,9 EUR/MWh; pierderea reală vine din numeroasele ore de la amiază cu prețuri mici, dar pozitive",
                    "Oprirea dublează rata de captare a unui parc solar"
                ],
                "correctExplanation": "0,63 EUR/MWh este foarte puțin față de reducerea datorată profilului, de 43,9 EUR/MWh: pierderea mare vine din prețurile mici, dar pozitive, de la amiază. Oprirea la distanță merită instalată, pentru că este ieftină, dar parcul trebuie evaluat după prețul capturat.",
                "incorrectExplanation": "Prețurile negative atrag atenția, dar un parc solar pierde mult mai mult în numeroasele ore de la amiază cu prețuri mici, încă pozitive, pe care oprirea nu le poate evita."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Hidden negative quarter-hours",
                "text": "Of Romania's 687 negative quarter-hours from 1 Oct 2025 to 31 Oct 2026, 26 (3.8%) fall in hours whose average price is zero or positive. Who can use or must pay these hidden negative prices?",
                "options": [
                    "Nobody: settlement is on hourly averages, so they have no economic effect",
                    "Only the transmission system operator Transelectrica, through balancing",
                    "Only plants with a support scheme, since merchant parks are paid hourly",
                    "A battery or flexible load acting per quarter-hour can use them, and a park metered per quarter-hour pays them"
                ],
                "correctExplanation": "Hourly averages show only 195 negative hours; the 15-minute grid reveals 26 more negative quarter-hours. A battery or flexible load acting per quarter-hour can use them, and a park metered per quarter-hour pays them, so switch-off and battery logic belong on the 15-minute grid.",
                "incorrectExplanation": "Since the Single Day-Ahead Coupling (SDAC) moved to a 15-minute market time unit, each quarter-hour has its own price and is settled at it; averaging over the hour hides prices that someone still pays or earns."
            },
            "ro": {
                "title": "Sferturi negative ascunse",
                "text": "Din cele 687 de sferturi de oră cu preț negativ ale României, între 1 octombrie 2025 și 31 octombrie 2026, 26 (3,8%) se află în ore a căror medie este zero sau pozitivă. Cine poate valorifica sau trebuie să plătească aceste prețuri negative ascunse?",
                "options": [
                    "Nimeni: decontarea se face pe medii orare, deci nu au efect economic",
                    "Doar operatorul de transport Transelectrica, prin echilibrare",
                    "Doar centralele cu schemă de sprijin, pentru că parcurile fără sprijin sînt plătite orar",
                    "O baterie sau un consumator flexibil care acționează pe sfert de oră le poate valorifica, iar un parc măsurat pe sfert de oră le plătește"
                ],
                "correctExplanation": "Mediile orare arată doar 195 de ore negative; detalierea pe 15 minute dezvăluie încă 26 de sferturi negative. O baterie sau un consumator flexibil care acționează pe sfert de oră le poate valorifica, iar un parc măsurat pe sfert de oră le plătește, așa că oprirea și bateriile se programează pe intervale de 15 minute.",
                "incorrectExplanation": "De cînd cuplarea unică a piețelor pentru ziua următoare (SDAC, Single Day-Ahead Coupling) folosește intervale de 15 minute, fiecare sfert de oră are propriul preț și se decontează la el; media orară ascunde prețuri pe care cineva tot le plătește sau le încasează."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Seasonal solar valley",
                "text": "The mean 15-minute price profile of the Romanian day-ahead market over the last 12 months (Nov 2025 – Oct 2026) is computed by season. In which season is the gap between the daily maximum and minimum smallest, and why?",
                "options": [
                    "Winter, about 98 EUR/MWh (euro per megawatt-hour), because solar output is small and the valley almost disappears",
                    "Spring, about 185 EUR/MWh, because demand is lowest",
                    "Summer, about 226 EUR/MWh, because air conditioning flattens the profile",
                    "Autumn, about 148 EUR/MWh, because wind output is highest"
                ],
                "correctExplanation": "The max–min gap is 185 EUR/MWh in spring and 226 in summer but only 98 in winter, when solar output is small and the solar valley almost disappears. In spring the minimum, 23.0 EUR/MWh, falls at 12:45 CET (Central European Time) and the maximum, 208.3, at 19:45.",
                "incorrectExplanation": "The daily gap is driven by the solar valley at midday against the evening peak. Summer has the largest gap, not the smallest; winter, with little solar, has the smallest."
            },
            "ro": {
                "title": "Valea solară pe anotimpuri",
                "text": "Profilul mediu al prețului pe 15 minute din PZU (piața pentru ziua următoare) în ultimele 12 luni (noiembrie 2025 – octombrie 2026) este calculat pe anotimpuri. În ce anotimp este cea mai mică distanța dintre maximul și minimul zilnic și de ce?",
                "options": [
                    "Iarna, circa 98 EUR/MWh (euro pe megawatt-oră), pentru că producția solară este mică și „valea” aproape dispare",
                    "Primăvara, circa 185 EUR/MWh, pentru că cererea este minimă",
                    "Vara, circa 226 EUR/MWh, pentru că aerul condiționat aplatizează profilul",
                    "Toamna, circa 148 EUR/MWh, pentru că producția eoliană este maximă"
                ],
                "correctExplanation": "Distanța maxim–minim este de 185 EUR/MWh primăvara și 226 vara, dar doar 98 iarna, cînd producția solară este mică și „valea” solară aproape dispare. Primăvara, minimul, 23,0 EUR/MWh, apare la 12:45 CET (ora Europei Centrale), iar maximul, 208,3, la 19:45.",
                "incorrectExplanation": "Distanța zilnică vine din „valea” solară de la amiază față de vîrful de seară. Vara are cea mai mare distanță, nu cea mai mică; iarna, cu puțin solar, o are pe cea mai mică."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Battery break-even price",
                "text": "A battery has a round-trip efficiency $\\eta$ = 85%, as in the lecture. It buys energy at 50 EUR per megawatt-hour (EUR/MWh). Above which selling price does the cycle break even, ignoring other costs?",
                "options": [
                    "About 57.5 EUR/MWh",
                    "About 59 EUR/MWh",
                    "About 42.5 EUR/MWh",
                    "50 EUR/MWh"
                ],
                "correctExplanation": "Only 85% of the energy comes back, so the sale price must exceed $50/0.85\\approx 59$ EUR/MWh (Sioshansi et al., 2009).",
                "incorrectExplanation": "Losses act on the energy sold, so the purchase price is divided by $\\eta$. Adding 15% (57.5) understates the threshold, and multiplying by 0.85 (42.5) goes the wrong way."
            },
            "ro": {
                "title": "Prețul de echilibru al bateriei",
                "text": "O baterie are randamentul ciclului complet $\\eta$ = 85%, ca în curs. Cumpără energie la 50 EUR pe megawatt-oră (EUR/MWh). Peste ce preț de vînzare ajunge ciclul la echilibru, ignorînd alte costuri?",
                "options": [
                    "Circa 57,5 EUR/MWh",
                    "Circa 59 EUR/MWh",
                    "Circa 42,5 EUR/MWh",
                    "50 EUR/MWh"
                ],
                "correctExplanation": "Doar 85% din energie se întoarce, deci prețul de vînzare trebuie să depășească $50/0{,}85\\approx 59$ EUR/MWh (Sioshansi et al., 2009).",
                "incorrectExplanation": "Pierderile afectează energia vîndută, deci prețul de cumpărare se împarte la $\\eta$. Adăugarea a 15% (57,5) subestimează pragul, iar înmulțirea cu 0,85 (42,5) merge în sens greșit."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Revenue per MWh of storage",
                "text": "In the last 12 months, with the optimal schedule on 15-minute prices, a 1 megawatt (MW) battery earned 61.0 thousand EUR with 1 hour of storage, 111.2 with 2 hours and 190.9 with 4 hours. What does the 4-hour battery earn per megawatt-hour (MWh) of storage capacity?",
                "options": [
                    "About 61.0 thousand EUR",
                    "About 95.5 thousand EUR",
                    "About 47.7 thousand EUR",
                    "About 190.9 thousand EUR"
                ],
                "correctExplanation": "$190.9/4\\approx 47.7$ thousand EUR per MWh, against $111.2/2=55.6$ for 2 hours and 61.0 for 1 hour: each extra hour trades a smaller spread, while the cells are paid per MWh.",
                "incorrectExplanation": "The 4-hour battery has 4 MWh of storage per MW, so its revenue is divided by 4, not by 2; 190.9 is the revenue per MW, and 61.0 is the 1-hour battery."
            },
            "ro": {
                "title": "Venitul pe MWh de stocare",
                "text": "În ultimele 12 luni, cu programul optim pe prețurile la 15 minute, o baterie de 1 megawatt (MW) a cîștigat 61,0 mii EUR cu o oră de stocare, 111,2 cu 2 ore și 190,9 cu 4 ore. Cît cîștigă bateria de 4 ore pe megawatt-oră (MWh) de capacitate de stocare?",
                "options": [
                    "Circa 61,0 mii EUR",
                    "Circa 95,5 mii EUR",
                    "Circa 47,7 mii EUR",
                    "Circa 190,9 mii EUR"
                ],
                "correctExplanation": "$190{,}9/4\\approx 47{,}7$ mii EUR pe MWh, față de $111{,}2/2=55{,}6$ pentru 2 ore și 61,0 pentru o oră: fiecare oră în plus exploatează un spread mai mic, în timp ce celulele se plătesc pe MWh.",
                "incorrectExplanation": "Bateria de 4 ore are 4 MWh de stocare pe MW, deci venitul se împarte la 4, nu la 2; 190,9 este venitul pe MW, iar 61,0 aparține bateriei de o oră."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Regional daily spreads",
                "text": "In 2026 the mean daily spread between the 2 dearest and the 2 cheapest hours was 174 EUR/MWh (euro per megawatt-hour) in Romania, 150 in Bulgaria, 187 in Hungary and 152 in Germany, about four times the Romanian 2019 level of 45. Why are the spreads of the three neighbouring markets so similar?",
                "options": [
                    "Because the three countries have the same installed solar capacity",
                    "Because the spread is set by a common European regulation",
                    "Because all three have the same fuel mix in the evening",
                    "Because they are coupled: every battery in the region competes for the same spread, and a battery built in Bulgaria lowers it in Romania too"
                ],
                "correctExplanation": "Market coupling links the prices, so the spread is a regional resource shared with every new battery next door; a battery built in Bulgaria lowers the spread in Romania too.",
                "incorrectExplanation": "Installed solar differs widely (at the end of 2025 Bulgaria 7.2 GW, Hungary 9.0 GW, Romania 2.79 GW). The similarity comes from coupling, which shares the midday surplus and the evening scarcity."
            },
            "ro": {
                "title": "Diferențele zilnice regionale",
                "text": "În 2026, diferența zilnică medie dintre cele mai scumpe 2 ore și cele mai ieftine 2 ore a fost 174 EUR/MWh (euro pe megawatt-oră) în România, 150 în Bulgaria, 187 în Ungaria și 152 în Germania, de circa patru ori nivelul din 2019 al României, de 45. De ce sînt atît de apropiate diferențele celor trei piețe vecine?",
                "options": [
                    "Pentru că cele trei țări au aceeași putere solară instalată",
                    "Pentru că diferența este fixată printr-o reglementare europeană comună",
                    "Pentru că toate trei au același mix de combustibili seara",
                    "Pentru că sînt cuplate: toate bateriile din regiune concurează pentru aceeași diferență, iar o baterie construită în Bulgaria o reduce și în România"
                ],
                "correctExplanation": "Cuplarea piețelor leagă prețurile, așa că diferența de preț este o resursă regională, împărțită cu fiecare baterie nouă din țările vecine; o baterie construită în Bulgaria reduce diferența și în România.",
                "incorrectExplanation": "Puterea solară instalată diferă mult (la sfîrșitul anului 2025, Bulgaria 7,2 GW, Ungaria 9,0 GW, România 2,79 GW). Asemănarea vine din cuplare, care împarte surplusul de la amiază și lipsa de seară."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Perfect foresight as upper bound",
                "text": "The battery's daily schedule is found with a linear programme (LP), with 85% round-trip efficiency and at most one cycle a day (reference values of the National Renewable Energy Laboratory, NREL). Why is the perfect-foresight revenue an upper bound?",
                "options": [
                    "Because prices are assumed known in advance; a real battery optimises on a forecast but is paid at the real prices",
                    "Because the LP ignores the round-trip efficiency",
                    "Because perfect foresight allows several cycles a day",
                    "Because it includes balancing revenue on top of day-ahead arbitrage"
                ],
                "correctExplanation": "With perfect foresight the schedule is optimal for the realised prices, so no feasible rule can do better. A forecast rule optimises on predicted prices and is paid at real prices, earning less.",
                "incorrectExplanation": "Efficiency and the one-cycle limit are in both versions, and balancing revenue, capacity fade and fees are excluded in both. The only difference is the information used to set the schedule."
            },
            "ro": {
                "title": "Informația perfectă, limită superioară",
                "text": "Programul zilnic al bateriei se obține cu un program liniar (LP), cu randament de 85% și cel mult un ciclu pe zi (valorile de referință ale Laboratorului Național pentru Energie Regenerabilă, NREL). De ce este venitul cu informație perfectă o limită superioară?",
                "options": [
                    "Pentru că prețurile sînt considerate cunoscute dinainte; o baterie reală se optimizează pe o prognoză, dar este plătită la prețurile reale",
                    "Pentru că programul liniar ignoră randamentul ciclului complet",
                    "Pentru că informația perfectă permite mai multe cicluri pe zi",
                    "Pentru că include veniturile din echilibrare pe lîngă arbitrajul pe ziua următoare"
                ],
                "correctExplanation": "Cu informație perfectă, programul este optim pentru prețurile realizate, așa că nicio regulă aplicabilă nu poate face mai bine. O regulă de prognoză se optimizează pe prețuri prognozate și este plătită la cele reale, deci cîștigă mai puțin.",
                "incorrectExplanation": "Randamentul și limita de un ciclu sînt în ambele variante, iar veniturile din echilibrare, pierderea de capacitate și tarifele sînt excluse în ambele. Singura diferență este informația folosită pentru program."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Doubling storage hours",
                "text": "Moving from a 2-hour to a 4-hour battery doubles the cost of the cells. With perfect foresight in the last 12 months, how did the revenue of the 4-hour battery compare with the 2-hour one?",
                "options": [
                    "Exactly twice as much, since revenue scales with stored energy",
                    "1.72 times as much, because the third and fourth hours trade a smaller spread",
                    "About the same, since the battery is limited to 1 MW (megawatt) of power",
                    "1.72 times less, because longer batteries cycle less"
                ],
                "correctExplanation": "A 4-hour battery earned 190.9 against 111.2 thousand EUR per MW, 1.72 times as much: the cheapest and dearest hours of the day are already used by the first two hours of storage. Size on the revenue of each extra MWh of storage.",
                "incorrectExplanation": "Extra storage does add revenue, but the extra hours buy dearer and sell cheaper than the first ones, so revenue grows less than proportionally."
            },
            "ro": {
                "title": "Dublarea orelor de stocare",
                "text": "Trecerea de la o baterie de 2 ore la una de 4 ore dublează costul celulelor. Cu informație perfectă, în ultimele 12 luni, cum s-a comparat venitul bateriei de 4 ore cu cel al bateriei de 2 ore?",
                "options": [
                    "Exact dublu, pentru că venitul crește proporțional cu energia stocată",
                    "De 1,72 ori mai mare, pentru că orele a treia și a patra valorifică o diferență mai mică",
                    "Aproximativ egal, pentru că bateria este limitată la 1 MW (megawatt) de putere",
                    "De 1,72 ori mai mic, pentru că bateriile mai lungi fac mai puține cicluri"
                ],
                "correctExplanation": "O baterie de 4 ore a cîștigat 190,9 față de 111,2 mii EUR pe MW, adică de 1,72 ori mai mult: cele mai ieftine și cele mai scumpe ore ale zilei sînt deja folosite de primele două ore de stocare. Dimensionați după venitul fiecărui MWh suplimentar de stocare.",
                "incorrectExplanation": "Stocarea suplimentară adaugă venit, dar orele în plus cumpără mai scump și vînd mai ieftin decît primele, așa că venitul crește mai puțin decît proporțional."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Seven-day forecast rule",
                "text": "In the last 12 months a 2-hour battery earned 111.2 thousand EUR per MW (megawatt) with perfect foresight and 93.4 with a rule that schedules on the mean price profile of the last 7 days. What share of perfect foresight does the rule capture, and how does it compare with yesterday's prices?",
                "options": [
                    "About 79%, the same as with yesterday's prices",
                    "About 100%, since the 7-day profile is a perfect forecast",
                    "About 85%, against 79% with yesterday's prices",
                    "About 119%, because the rule avoids timing errors"
                ],
                "correctExplanation": "$93.4/111.2\\approx 0.85$: the 7-day rule earns about 85% of the perfect-foresight revenue for 2 hours, while yesterday's prices earn 79%. Longer batteries forgive timing errors better (89% for 4 hours).",
                "incorrectExplanation": "A rule optimised on a forecast and paid at real prices cannot beat perfect foresight. 79% is the share achieved with yesterday's prices; the 7-day rule does better."
            },
            "ro": {
                "title": "Regula de 7 zile",
                "text": "În ultimele 12 luni, o baterie de 2 ore a cîștigat 111,2 mii EUR pe MW (megawatt) cu informație perfectă și 93,4 cu o regulă care se programează pe profilul mediu al prețurilor din ultimele 7 zile. Ce parte din venitul cu informație perfectă obține regula și cum se compară cu prețurile de ieri?",
                "options": [
                    "Circa 79%, la fel ca prețurile de ieri",
                    "Circa 100%, pentru că profilul pe 7 zile este o prognoză perfectă",
                    "Circa 85%, față de 79% cu prețurile de ieri",
                    "Circa 119%, pentru că regula evită erorile de sincronizare"
                ],
                "correctExplanation": "$93{,}4/111{,}2\\approx 0{,}85$: regula de 7 zile obține circa 85% din venitul cu informație perfectă pentru 2 ore, iar prețurile de ieri 79%. Bateriile mai lungi tolerează mai bine erorile de sincronizare (89% pentru 4 ore).",
                "incorrectExplanation": "O regulă optimizată pe prognoză și plătită la prețurile reale nu poate depăși informația perfectă. 79% este ponderea obținută cu prețurile de ieri; regula de 7 zile face mai bine."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Value of 15-minute prices",
                "text": "On the same days of the last 12 months, moving from hourly to 15-minute prices raised perfect-foresight battery revenue by 14.5% for 1 hour of storage, 10.3% for 2 hours and 7.0% for 4 hours. Which reading is correct?",
                "options": [
                    "15-minute prices can lower revenue, because quarter-hours are more volatile",
                    "Long batteries gain most, because they can use more quarter-hours",
                    "The gains mostly reflect the higher price level of 2026 compared with 2025",
                    "Finer prices can only add revenue, since any hourly schedule can also run on quarter-hours, and short batteries gain most"
                ],
                "correctExplanation": "$R^{15}\\ge R^{60}$ because any hourly schedule is feasible on quarter-hours. Short batteries gain most (+14.5% for 1 hour): they can target the few extreme quarter-hours. Both revenues use the same days, so the gain is granularity alone.",
                "incorrectExplanation": "The comparison is on the same days, so it excludes price-level changes; and since the hourly schedule remains available, extra granularity cannot reduce optimal revenue. The gain shrinks with storage length."
            },
            "ro": {
                "title": "Valoarea prețurilor pe 15 minute",
                "text": "În aceleași zile din ultimele 12 luni, trecerea de la prețuri orare la prețuri pe 15 minute a crescut venitul cu informație perfectă al bateriei cu 14,5% pentru 1 oră de stocare, cu 10,3% pentru 2 ore și cu 7,0% pentru 4 ore. Care interpretare este corectă?",
                "options": [
                    "Prețurile pe 15 minute pot reduce venitul, pentru că sferturile de oră sînt mai volatile",
                    "Bateriile lungi cîștigă cel mai mult, pentru că pot folosi mai multe sferturi de oră",
                    "Cîștigurile reflectă mai ales nivelul mai ridicat al prețurilor din 2026 față de 2025",
                    "Prețurile mai fine pot doar să adauge venit, pentru că orice program orar poate rula și pe sferturi de oră, iar bateriile scurte cîștigă cel mai mult"
                ],
                "correctExplanation": "$R^{15}\\ge R^{60}$, pentru că orice program orar este realizabil și pe sferturi de oră. Bateriile scurte cîștigă cel mai mult (+14,5% pentru 1 oră): pot ținti puținele sferturi extreme. Ambele venituri folosesc aceleași zile, deci cîștigul vine doar din detaliere.",
                "incorrectExplanation": "Comparația se face pe aceleași zile, deci exclude schimbarea nivelului prețurilor; și, cum programul orar rămîne disponibil, detalierea suplimentară nu poate reduce venitul optim. Cîștigul scade cu durata stocării."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Self-cannibalisation of batteries",
                "text": "On the OPCOM (Romanian market operator) curves of 21 Oct 2026, the evening price exceeded the midday price by 91.77 EUR/MWh (euro per megawatt-hour). Adding $X$ MW (megawatts) of batteries as midday demand and evening supply, what happens to the spread on the local order book alone?",
                "options": [
                    "With 50 MW it becomes −13.15 EUR/MWh: 50 MW are enough to close it, an upper bound since flows adjust in the coupled market",
                    "With 50 MW it is almost unchanged, because batteries are small next to the market",
                    "With 50 MW it widens, because charging raises the evening price",
                    "It closes only with 766 MW, the peak output of the Romanian battery fleet"
                ],
                "correctExplanation": "With 50 MW the spread would be −13.15 EUR/MWh and with 100 MW −47.12: charging lifts the midday price and discharging lowers the evening one. Like the merit-order exercise it is an upper bound, because cross-border flows are held fixed. Model the spread after the fleet is built.",
                "incorrectExplanation": "Batteries cannibalise their own spread just as solar cannibalises its price. 766 MW is the maximum Romanian battery output in 2026, not the volume that closes the local spread."
            },
            "ro": {
                "title": "Autocanibalizarea bateriilor",
                "text": "Pe curbele OPCOM (operatorul pieței din România) din 21 octombrie 2026, prețul de seară a depășit prețul de la amiază cu 91,77 EUR/MWh (euro pe megawatt-oră). Dacă se adaugă $X$ MW (megawați) de baterii, drept cerere la amiază și ofertă seara, ce se întîmplă cu diferența numai pe ofertele locale?",
                "options": [
                    "Cu 50 MW devine −13,15 EUR/MWh: 50 MW sînt suficienți ca s-o anuleze, o limită superioară, pentru că în piața cuplată fluxurile se ajustează",
                    "Cu 50 MW rămîne aproape neschimbată, pentru că bateriile sînt mici față de piață",
                    "Cu 50 MW crește, pentru că încărcarea ridică prețul de seară",
                    "Se anulează abia la 766 MW, producția maximă a bateriilor din România"
                ],
                "correctExplanation": "Cu 50 MW diferența ar fi −13,15 EUR/MWh, iar cu 100 MW −47,12: încărcarea ridică prețul de la amiază, iar descărcarea coboară prețul de seară. Ca și calculul ordinii de merit, este o limită superioară, pentru că fluxurile transfrontaliere rămîn fixe. Modelați diferența de după construirea bateriilor.",
                "incorrectExplanation": "Bateriile își canibalizează diferența de preț la fel cum solarul își canibalizează prețul. 766 MW este producția maximă a bateriilor din România în 2026, nu volumul care anulează diferența locală."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Maximum battery investment",
                "text": "The largest investment a yearly revenue $R$ can repay is $I^{\\max}=R\\cdot a(r,n)$, with annuity factor $a(r,n)=(1-(1+r)^{-n})/r$ = 8.56 for $r$ = 8% and $n$ = 15 years. A 2-hour battery earned 111.2 thousand EUR per MW (megawatt) with perfect foresight in the last 12 months. What is $I^{\\max}$ per kW (kilowatt)?",
                "options": [
                    "About 111 EUR/kW",
                    "About 952 EUR/kW",
                    "About 1,668 EUR/kW",
                    "About 13 EUR/kW"
                ],
                "correctExplanation": "$111{,}200\\times 8.56\\approx 952{,}000$ EUR per MW, i.e. about 952 EUR/kW. With the 7-day rule the lecture gets 808 EUR/kW, or 404 EUR per kWh (kilowatt-hour) of storage.",
                "incorrectExplanation": "Multiply the yearly revenue by the annuity factor, then divide by 1,000 to go from MW to kW. 1,668 multiplies by the 15 years without discounting, 111 forgets the annuity factor and 13 divides by it."
            },
            "ro": {
                "title": "Investiția maximă în baterie",
                "text": "Investiția maximă pe care o poate recupera un venit anual $R$ este $I^{\\max}=R\\cdot a(r,n)$, cu factorul de anuitate $a(r,n)=(1-(1+r)^{-n})/r$ = 8,56 pentru $r$ = 8% și $n$ = 15 ani. O baterie de 2 ore a cîștigat 111,2 mii EUR pe MW (megawatt) cu informație perfectă în ultimele 12 luni. Cît este $I^{\\max}$ pe kW (kilowatt)?",
                "options": [
                    "Circa 111 EUR/kW",
                    "Circa 952 EUR/kW",
                    "Circa 1 668 EUR/kW",
                    "Circa 13 EUR/kW"
                ],
                "correctExplanation": "$111\\,200\\times 8{,}56\\approx 952\\,000$ EUR pe MW, adică circa 952 EUR/kW. Cu regula de 7 zile, cursul obține 808 EUR/kW, adică 404 EUR pe kWh (kilowatt-oră) de stocare.",
                "incorrectExplanation": "Venitul anual se înmulțește cu factorul de anuitate, apoi se împarte la 1 000 pentru a trece de la MW la kW. 1 668 înmulțește cu cei 15 ani fără actualizare, 111 omite factorul de anuitate, iar 13 împarte la el."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Solar park and battery in the same week",
                "text": "Case study: in the week of 20–26 Apr 2026, Romania had 24 negative hours and prices ranged from −99.75 to 328.00 EUR/MWh (euro per megawatt-hour). How did the week look for a solar park and for a battery?",
                "options": [
                    "Good for both: high solar output and high price peaks",
                    "Poor for both: negative prices hurt every asset",
                    "Poor for solar, with a capture rate of 42.5%, and among the best for a 2-hour battery, which earned 391 EUR per MW (megawatt) a day against 305 on an average day",
                    "Good for solar, with a capture rate above 100%, and poor for a battery, which could not charge at negative prices"
                ],
                "correctExplanation": "Solar's capture price was 37.0 EUR/MWh against a baseload of 87.0, a capture rate of 42.5%, while a 2-hour battery with perfect foresight earned 391 EUR per MW a day, against 305 on an average day of the last 12 months.",
                "incorrectExplanation": "Deep midday valleys and high evening peaks cut the value of solar output and widen the spread a battery trades: the same sunny week is the worst for a solar park and among the best for a battery."
            },
            "ro": {
                "title": "Parcul solar și bateria în aceeași săptămînă",
                "text": "Studiu de caz: în săptămîna 20–26 aprilie 2026, România a avut 24 de ore cu preț negativ, iar prețurile au variat între −99,75 și 328,00 EUR/MWh (euro pe megawatt-oră). Cum a arătat săptămîna pentru un parc solar și pentru o baterie?",
                "options": [
                    "Bună pentru amîndouă: producție solară mare și vîrfuri mari de preț",
                    "Slabă pentru amîndouă: prețurile negative afectează orice activ",
                    "Slabă pentru solar, cu o rată de captare de 42,5%, și una dintre cele mai bune pentru o baterie de 2 ore, care a cîștigat 391 EUR pe MW (megawatt) pe zi, față de 305 într-o zi medie",
                    "Bună pentru solar, cu o rată de captare peste 100%, și slabă pentru baterie, care nu se putea încărca la prețuri negative"
                ],
                "correctExplanation": "Prețul capturat solar a fost 37,0 EUR/MWh, față de un preț de bază de 87,0, deci o rată de captare de 42,5%, în timp ce o baterie de 2 ore cu informație perfectă a cîștigat 391 EUR pe MW pe zi, față de 305 într-o zi medie din ultimele 12 luni.",
                "incorrectExplanation": "„Văile” adînci de la amiază și vîrfurile mari de seară reduc valoarea producției solare și lărgesc diferența din care cîștigă bateria: aceeași săptămînă însorită este cea mai slabă pentru un parc solar și una dintre cele mai bune pentru o baterie."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Evening imports from Bulgaria",
                "text": "Case study, summer 2026 (1 Jun – 31 Aug): Romania exported at midday but imported 2,064 MW (megawatts) from Bulgaria at 21:00 on all 92 days. At 21:00 the mean price was 243.9 EUR/MWh (euro per megawatt-hour) in Romania and 178.3 in Bulgaria. Why did the Romanian evening price stay higher?",
                "options": [
                    "Because Bulgarian prices are capped by regulation in the evening",
                    "Because Romania exported to Bulgaria in the evening and lost supply",
                    "Because the two markets are not coupled in the evening",
                    "Because the border was fully used, so the two prices separated; the 65.6 EUR/MWh gap is what evening storage and more interconnection are worth"
                ],
                "correctExplanation": "When the interconnector is fully used, coupled prices separate and the importing side stays dearer. The evening gap of 65.6 EUR/MWh measures the value of evening storage and of more interconnection capacity in Romania.",
                "incorrectExplanation": "The markets are coupled at all hours, and in the evening the flow ran from Bulgaria into Romania. Prices converge only while the border has spare capacity; once it is full, they separate."
            },
            "ro": {
                "title": "Importul de seară din Bulgaria",
                "text": "Studiu de caz, vara 2026 (1 iunie – 31 august): România a exportat la prînz, dar a importat din Bulgaria 2 064 MW (megawați) la ora 21, în toate cele 92 de zile. La ora 21, prețul mediu a fost 243,9 EUR/MWh (euro pe megawatt-oră) în România și 178,3 în Bulgaria. De ce a rămas mai mare prețul de seară din România?",
                "options": [
                    "Pentru că prețurile din Bulgaria sînt plafonate prin reglementare seara",
                    "Pentru că România a exportat seara spre Bulgaria și a pierdut ofertă",
                    "Pentru că cele două piețe nu sînt cuplate seara",
                    "Pentru că granița a fost folosită complet, deci prețurile s-au separat; diferența de 65,6 EUR/MWh arată cît valorează stocarea pentru seară și o interconexiune mai mare"
                ],
                "correctExplanation": "Cînd interconexiunea este folosită complet, prețurile piețelor cuplate se separă, iar partea importatoare rămîne mai scumpă. Diferența de seară, de 65,6 EUR/MWh, arată cît valorează în România stocarea pentru seară și o capacitate mai mare de interconexiune.",
                "incorrectExplanation": "Piețele sînt cuplate la toate orele, iar seara fluxul a mers din Bulgaria spre România. Prețurile converg doar cît timp granița are capacitate liberă; cînd este plină, ele se separă."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "April 2026 for each market participant",
                "text": "Case study: April 2026 had 67 negative hours, the most of any month. Which pairing of player and outcome matches the lecture?",
                "options": [
                    "Solar developer: capture rate 49.4%, with 17.9% of output at negative prices; wind developer: capture rate 97.8%",
                    "Solar developer: capture rate 97.8%; wind developer: capture rate 49.4%",
                    "Battery developer: 2-hour revenue below its 12-month average, at 205 EUR per MW (megawatt) a day",
                    "Supplier: negative hours are a cost, so consumption should be moved away from spring middays"
                ],
                "correctExplanation": "In April 2026 solar captured 49.4% (47.2 against 95.6 EUR/MWh, euro per megawatt-hour) with 17.9% of output at negative prices, wind 97.8%, and a 2-hour battery earned 325 EUR per MW a day against 305 on average. Moving consumption to spring middays is paid.",
                "incorrectExplanation": "In Romania wind is not the cannibalised technology; the battery earned above its average (325 against 305), and a flexible supplier or consumer is paid to consume in negative hours."
            },
            "ro": {
                "title": "Aprilie 2026 pentru fiecare participant la piață",
                "text": "Studiu de caz: aprilie 2026 a avut 67 de ore cu preț negativ, cele mai multe dintre toate lunile. Care asociere între participant și rezultat corespunde cursului?",
                "options": [
                    "Dezvoltatorul solar: rată de captare 49,4%, cu 17,9% din producție la prețuri negative; dezvoltatorul eolian: rată de captare 97,8%",
                    "Dezvoltatorul solar: rată de captare 97,8%; dezvoltatorul eolian: rată de captare 49,4%",
                    "Dezvoltatorul de baterii: venitul bateriei de 2 ore sub media celor 12 luni, la 205 EUR pe MW (megawatt) pe zi",
                    "Furnizorul: orele negative sînt un cost, deci consumul trebuie mutat în afara amiezilor de primăvară"
                ],
                "correctExplanation": "În aprilie 2026, rata de captare solară a fost 49,4% (47,2 față de 95,6 EUR/MWh, euro pe megawatt-oră), cu 17,9% din producție la prețuri negative, cea eoliană 97,8%, iar o baterie de 2 ore a cîștigat 325 EUR pe MW pe zi, față de 305 în medie. Mutarea consumului la amiază, primăvara, este plătită.",
                "incorrectExplanation": "În România, eolianul nu este tehnologia canibalizată; bateria a cîștigat peste media ei (325 față de 305), iar un furnizor sau consumator flexibil este plătit să consume în orele negative."
            }
        }
    ]
};
