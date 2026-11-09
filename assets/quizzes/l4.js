// ============================================================
// Quiz bank for lecture id 'l4': Risk for energy companies (EN + RO)
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.EMQA_DATA.quizzes['l4'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 1,
            "en": {
                "title": "Loss per EUR/MWh",
                "text": "A supplier buys 100 megawatts (MW) flat every day on the Romanian day-ahead market, Piața pentru Ziua Următoare (PZU), and budgets at yesterday's price. How much does it lose for each EUR per megawatt-hour (EUR/MWh) of price rise?",
                "options": ["100 EUR", "2,400 EUR", "240 EUR", "24,000 EUR"],
                "correctExplanation": "100 MW over the 24 hours of the delivery day is 2,400 MWh, so each EUR/MWh of rise costs 2,400 EUR: $L_t=Q\\cdot 24\\cdot X_t$.",
                "incorrectExplanation": "Multiply the position in MW by the 24 hours of the day: 100 × 24 = 2,400 MWh, hence 2,400 EUR for every EUR/MWh. Forgetting the hours, or adding a zero, is the usual slip."
            },
            "ro": {
                "title": "Pierderea pe EUR/MWh",
                "text": "Un furnizor cumpără zilnic 100 de megawați (MW) în bandă pe piața pentru ziua următoare (PZU) din România și își bugetează costul la prețul de ieri. Cît pierde pentru fiecare EUR pe megawatt-oră (EUR/MWh) cu care crește prețul?",
                "options": ["100 EUR", "2 400 EUR", "240 EUR", "24 000 EUR"],
                "correctExplanation": "100 MW pe cele 24 de ore ale zilei de livrare înseamnă 2 400 MWh, deci fiecare EUR/MWh de creștere costă 2 400 EUR: $L_t=Q\\cdot 24\\cdot X_t$.",
                "incorrectExplanation": "Poziția în MW se înmulțește cu cele 24 de ore ale zilei: 100 × 24 = 2 400 MWh, deci 2 400 EUR pentru fiecare EUR/MWh. Greșeala obișnuită este omiterea orelor sau un zero în plus."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Price changes versus log returns",
                "text": "Why does the lecture measure the risk of a power position on daily price changes $X_t=P_t-P_{t-1}$, in EUR per megawatt-hour (EUR/MWh), rather than on log returns?",
                "options": ["Log returns are too volatile for power prices to be useful", "Regulators require changes in euro for all power positions", "Price changes are normally distributed, while log returns are not", "Power prices can be negative, and log returns are not defined for a negative price"],
                "correctExplanation": "A log return needs a positive price; power prices can fall below zero, so the lecture works with changes in euro, which also translate directly into the loss $L_t=Q\\cdot 24\\cdot X_t$.",
                "incorrectExplanation": "The reason is technical, not regulatory: the logarithm of a negative price does not exist. Price changes are far from normal too (excess kurtosis of 12.0), so normality is not the argument."
            },
            "ro": {
                "title": "Variații de preț și randamente logaritmice",
                "text": "De ce măsoară cursul riscul unei poziții pe piața energiei electrice pe variațiile zilnice ale prețului, $X_t=P_t-P_{t-1}$, în EUR pe megawatt-oră (EUR/MWh), și nu pe randamente logaritmice?",
                "options": ["Randamentele logaritmice sînt prea volatile pentru a fi utile la prețurile energiei", "Autoritățile de reglementare cer variații în euro pentru toate pozițiile pe energie", "Variațiile prețului urmează o repartiție normală, iar randamentele logaritmice nu", "Prețul energiei electrice poate fi negativ, iar randamentul logaritmic nu este definit pentru un preț negativ"],
                "correctExplanation": "Un randament logaritmic cere un preț pozitiv; prețul energiei poate coborî sub zero, de aceea cursul lucrează cu variații în euro, care se transformă direct în pierderea $L_t=Q\\cdot 24\\cdot X_t$.",
                "incorrectExplanation": "Motivul este tehnic, nu de reglementare: logaritmul unui preț negativ nu există. Nici variațiile nu sînt normale (excesul de aplatizare este 12,0), deci normalitatea nu este argumentul."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Interpreting VaR",
                "text": "Your 99% one-day value-at-risk (VaR) for 100 megawatts (MW) flat is 162 thousand EUR. What does this number promise?",
                "options": ["On about 1 day in 100 the loss should exceed 162 thousand EUR; it says nothing about how large the loss is on those days", "The average loss on the worst 1% of days is 162 thousand EUR", "The company loses exactly 162 thousand EUR on 1 day in 100, and never more", "On 99 days in 100 the loss equals 162 thousand EUR"],
                "correctExplanation": "VaR is a quantile of tomorrow's loss: a threshold, not an average. The size of the loss beyond it is measured by expected shortfall (ES), the mean loss beyond VaR.",
                "incorrectExplanation": "Confusing VaR with an average loss is the classic mistake: the average loss on the bad days is expected shortfall (ES). VaR only says how often the threshold should be crossed."
            },
            "ro": {
                "title": "Interpretarea VaR",
                "text": "Valoarea la risc (VaR) de 99% pe o zi, pentru 100 de megawați (MW) în bandă, este de 162 de mii EUR. Ce promite această cifră?",
                "options": ["În aproximativ o zi din 100, pierderea ar trebui să depășească 162 de mii EUR; cifra nu spune nimic despre mărimea pierderii în acele zile", "Pierderea medie în cele mai proaste 1% dintre zile este de 162 de mii EUR", "Compania pierde exact 162 de mii EUR într-o zi din 100 și niciodată mai mult", "În 99 de zile din 100, pierderea este egală cu 162 de mii EUR"],
                "correctExplanation": "VaR este o cuantilă a pierderii de mîine: un prag, nu o medie. Mărimea pierderii de dincolo de prag o măsoară deficitul așteptat (ES), pierderea medie dincolo de VaR.",
                "incorrectExplanation": "Greșeala clasică este confundarea VaR cu o pierdere medie: pierderea medie din zilele proaste este deficitul așteptat (ES). VaR spune doar cît de des ar trebui depășit pragul."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "From quantile to euros",
                "text": "On the last 365 days, the 99% quantile of the daily change of the Romanian day-ahead price is 86.63 EUR per megawatt-hour (EUR/MWh). What is, approximately, the 99% value-at-risk (VaR) of a 100 megawatt (MW) flat position?",
                "options": ["About 8,663 EUR", "About 20,792 EUR", "About 207,922 EUR", "About 2,079,216 EUR"],
                "correctExplanation": "100 MW flat is 2,400 MWh per day, and 86.63 × 2,400 ≈ 207,900 EUR; the lecture reports a VaR$_{0.99}$ of 207,922 EUR, computed from the unrounded quantile.",
                "incorrectExplanation": "The VaR in EUR is the quantile in EUR/MWh times the daily volume, $Q\\cdot 24$ = 2,400 MWh. Multiplying only by 100 MW, or by 240, misses the hours of the day."
            },
            "ro": {
                "title": "De la cuantilă la euro",
                "text": "Pe ultimele 365 de zile, cuantila de 99% a variației zilnice a prețului de pe piața pentru ziua următoare (PZU) din România este 86,63 EUR pe megawatt-oră (EUR/MWh). Cît este, aproximativ, valoarea la risc (VaR) de 99% pentru o poziție de 100 de megawați (MW) în bandă?",
                "options": ["Circa 8 663 EUR", "Circa 20 792 EUR", "Circa 207 922 EUR", "Circa 2 079 216 EUR"],
                "correctExplanation": "100 MW în bandă înseamnă 2 400 MWh pe zi, iar 86,63 × 2 400 ≈ 207 900 EUR; cursul raportează o VaR$_{0,99}$ de 207 922 EUR, calculată din cuantila nerotunjită.",
                "incorrectExplanation": "VaR în EUR este cuantila în EUR/MWh înmulțită cu volumul zilnic, $Q\\cdot 24$ = 2 400 MWh. Înmulțirea doar cu 100 MW sau cu 240 omite orele zilei."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Why FRTB prefers ES",
                "text": "Why does the Fundamental Review of the Trading Book (FRTB), the Basel market-risk rules, use expected shortfall (ES) at 97.5% instead of value-at-risk (VaR) at 99%?",
                "options": ["ES is easier to backtest by counting exceedances than VaR", "ES at 97.5% is always smaller, so banks need less capital", "ES does not depend on the shape of the loss distribution", "ES measures the average loss beyond VaR and is subadditive, so diversification never adds risk"],
                "correctExplanation": "ES is a coherent risk measure (Artzner et al., 1999): $\\text{ES}(L_1+L_2)\\le\\text{ES}(L_1)+\\text{ES}(L_2)$, while VaR may break this property. It also looks at the size of the bad days, not only at their frequency.",
                "incorrectExplanation": "ES is actually harder to backtest, since it cannot be checked by counting. For a normal curve ES$_{0.975}$ = $\\mu$ + 2.338$\\sigma$, almost equal to VaR$_{0.99}$ = $\\mu$ + 2.326$\\sigma$, so the switch is about coherence, not about lower capital."
            },
            "ro": {
                "title": "De ce preferă FRTB ES",
                "text": "De ce folosește revizuirea fundamentală a portofoliului de tranzacționare (FRTB), adică regulile Basel pentru riscul de piață, deficitul așteptat (ES) de 97,5% în locul valorii la risc (VaR) de 99%?",
                "options": ["ES se testează retrospectiv mai ușor decît VaR, prin numărarea depășirilor", "ES de 97,5% este întotdeauna mai mic, deci băncile au nevoie de mai puțin capital", "ES nu depinde de forma repartiției pierderilor", "ES măsoară pierderea medie de dincolo de VaR și este subaditiv, deci diversificarea nu adaugă niciodată risc"],
                "correctExplanation": "ES este o măsură coerentă a riscului (Artzner et al., 1999): $\\text{ES}(L_1+L_2)\\le\\text{ES}(L_1)+\\text{ES}(L_2)$, în timp ce VaR poate încălca această proprietate. În plus, ES ține seama de mărimea zilelor proaste, nu doar de frecvența lor.",
                "incorrectExplanation": "ES este, de fapt, mai greu de testat, pentru că nu poate fi verificat prin numărare. Pentru repartiția normală, ES$_{0,975}$ = $\\mu$ + 2,338$\\sigma$, aproape egal cu VaR$_{0,99}$ = $\\mu$ + 2,326$\\sigma$, deci schimbarea ține de coerență, nu de un capital mai mic."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Joint VaR of two zones",
                "text": "For 100 megawatts (MW) in Romania and 100 MW in Germany–Luxembourg (DE-LU), the 99% value-at-risk (VaR) is 86.63 and 91.76 EUR per megawatt-hour (EUR/MWh) separately. The correlation between the two price changes is 0.55. What joint 99% VaR does the lecture report?",
                "options": ["178.39 EUR/MWh, the sum of the two", "150.77 EUR/MWh, less than the sum", "91.76 EUR/MWh, the larger of the two", "196.20 EUR/MWh, more than the sum because of the correlation"],
                "correctExplanation": "Together the two positions have a 99% VaR of 150.77 EUR/MWh, below the sum of 178.39: with a correlation of 0.55, part of the risk diversifies away.",
                "incorrectExplanation": "Adding VaRs assumes the two prices always move together (perfect correlation). With a correlation of 0.55 the joint risk is smaller than the sum, but larger than either position alone."
            },
            "ro": {
                "title": "VaR comună pentru două zone",
                "text": "Pentru cîte 100 de megawați (MW) în România și în Germania–Luxemburg (DE-LU), valoarea la risc (VaR) de 99% este 86,63 și 91,76 EUR pe megawatt-oră (EUR/MWh), considerate separat. Corelația dintre variațiile celor două prețuri este 0,55. Ce VaR de 99% pentru cele două poziții împreună raportează cursul?",
                "options": ["178,39 EUR/MWh, suma celor două", "150,77 EUR/MWh, mai puțin decît suma", "91,76 EUR/MWh, cea mai mare dintre cele două", "196,20 EUR/MWh, mai mult decît suma, din cauza corelației"],
                "correctExplanation": "Împreună, cele două poziții au o VaR de 99% de 150,77 EUR/MWh, sub suma de 178,39: cu o corelație de 0,55, o parte din risc se diversifică.",
                "incorrectExplanation": "Adunarea valorilor VaR presupune că cele două prețuri se mișcă mereu împreună (corelație perfectă). Cu o corelație de 0,55, riscul total este mai mic decît suma, dar mai mare decît riscul fiecărei poziții."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Counting 3-sigma rises",
                "text": "On Romanian day-ahead prices, 2015–2026, on how many days did the price rise by more than 3 standard deviations, and how many such days would a normal curve expect over the same sample?",
                "options": ["52 days observed, against 5.8 expected", "5.8 days observed, against 52 expected", "About 6 days observed, as the normal curve predicts", "52 days observed, against 26 expected"],
                "correctExplanation": "Rises above 3 standard deviations occurred on 52 days, about nine times the 5.8 expected. The excess kurtosis is 12.0, against 0 for a normal curve, and the largest rise was 10.1 standard deviations.",
                "incorrectExplanation": "Power prices have a narrow centre and long tails: extreme days are far more frequent than the normal curve allows. A limit built on the normal curve therefore understates how often a crisis day comes."
            },
            "ro": {
                "title": "Creșteri de peste 3 sigma",
                "text": "Pe prețurile de pe piața pentru ziua următoare (PZU) din România, 2015–2026, în cîte zile a crescut prețul cu mai mult de 3 abateri standard și cîte asemenea zile ar prevedea repartiția normală pe același eșantion?",
                "options": ["52 de zile observate, față de 5,8 așteptate", "5,8 zile observate, față de 52 așteptate", "Circa 6 zile observate, cît prevede repartiția normală", "52 de zile observate, față de 26 așteptate"],
                "correctExplanation": "Creșteri de peste 3 abateri standard au apărut în 52 de zile, de circa nouă ori mai des decît cele 5,8 așteptate. Excesul de aplatizare este 12,0, față de 0 pentru repartiția normală, iar cea mai mare creștere a avut 10,1 abateri standard.",
                "incorrectExplanation": "Prețurile energiei au un centru îngust și cozi lungi: zilele extreme sînt mult mai frecvente decît admite repartiția normală. O limită calculată cu repartiția normală subestimează deci frecvența zilelor de criză."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "A static limit in crisis",
                "text": "A 99% limit of 23.77 EUR per megawatt-hour (EUR/MWh), set from the normal curve at the end of 2020, was breached 139 times in 2021–2022, against 7.3 expected. Roughly how many times more often than planned is that?",
                "options": ["About 2 times", "About 7 times", "About 14 times", "About 19 times"],
                "correctExplanation": "139 / 7.3 ≈ 19. The limit did not move when volatility moved, so it measured a market that no longer existed; in 2023–2026 it was still breached 226 times against 14.0 expected.",
                "incorrectExplanation": "Divide the observed breaches by the expected ones: 139 / 7.3 ≈ 19. The lesson is that a limit must move with volatility, which is what the filtered methods do."
            },
            "ro": {
                "title": "O limită fixă în criză",
                "text": "O limită de 99% de 23,77 EUR pe megawatt-oră (EUR/MWh), calculată la sfîrșitul anului 2020 cu repartiția normală, a fost depășită de 139 de ori în 2021–2022, față de 7,3 depășiri așteptate. De aproximativ cîte ori mai des decît se prevedea?",
                "options": ["De circa 2 ori", "De circa 7 ori", "De circa 14 ori", "De circa 19 ori"],
                "correctExplanation": "139 / 7,3 ≈ 19. Limita nu s-a modificat cînd s-a modificat volatilitatea, așa că a continuat să măsoare o piață care nu mai exista; în 2023–2026 a fost depășită tot de 226 de ori, față de 14,0 așteptate.",
                "incorrectExplanation": "Se împart depășirile observate la cele așteptate: 139 / 7,3 ≈ 19. Concluzia este că o limită trebuie să urmeze volatilitatea, ceea ce fac metodele filtrate."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Reading the HS quantile",
                "text": "Historical simulation (HS) with a window of 365 days reads the 99% value-at-risk (VaR) directly from the sorted daily changes. Which change is it?",
                "options": ["The 4th largest change", "The 37th largest change", "The 18th largest change", "The single largest change"],
                "correctExplanation": "1% of 365 days is 3.65 days, so the 99% VaR is the 4th largest change of the window. HS assumes no distribution: the past year is taken as the distribution of tomorrow.",
                "incorrectExplanation": "The tail share is $1-\\alpha$ = 1%, and 1% of 365 is about 3.65, hence the 4th largest change. Using 10% or 5% of the window would give a 90% or 95% quantile instead."
            },
            "ro": {
                "title": "Cuantila în simularea istorică",
                "text": "Simularea istorică (HS) cu o fereastră de 365 de zile citește valoarea la risc (VaR) de 99% direct din variațiile zilnice ordonate. Care variație este aceasta?",
                "options": ["A patra cea mai mare variație", "A 37-a cea mai mare variație", "A 18-a cea mai mare variație", "Cea mai mare variație din fereastră"],
                "correctExplanation": "1% din 365 de zile înseamnă 3,65 zile, deci VaR de 99% este a patra cea mai mare variație din fereastră. HS nu presupune nicio repartiție: ultimul an de date este considerat repartiția zilei de mîine.",
                "incorrectExplanation": "Proporția din coadă este $1-\\alpha$ = 1%, iar 1% din 365 înseamnă circa 3,65, de unde a patra cea mai mare variație. Cu 10% sau 5% din fereastră s-ar obține cuantila de 90% sau de 95%."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The weakness of HS",
                "text": "Historical simulation (HS) is the default in many energy companies. In the 2017–2026 backtest its 99% value-at-risk (VaR) was exceeded on 2.04% of days. What is its main weakness?",
                "options": ["It assumes that price changes follow a normal curve", "It cannot be computed when prices are negative", "It is slow: a new regime needs months to fill the window, and a crisis day drops out on a fixed date, so VaR jumps down for no market reason", "It overreacts to yesterday's change, because it weights recent days more heavily"],
                "correctExplanation": "In HS every day of the window counts with full weight for 365 days and then disappears at once. The model therefore lags the market when a crisis begins and drops its VaR on a date that has nothing to do with the market.",
                "incorrectExplanation": "HS uses no distribution and works on price changes, which are defined for negative prices; it weights all days equally. Its problem is speed, which is exactly what filtered historical simulation fixes."
            },
            "ro": {
                "title": "Punctul slab al HS",
                "text": "Simularea istorică (HS) este metoda implicită în multe companii energetice. La testarea retrospectivă 2017–2026, valoarea la risc (VaR) de 99% obținută prin HS a fost depășită în 2,04% din zile. Care este principalul ei punct slab?",
                "options": ["Presupune că variațiile prețului urmează repartiția normală", "Nu poate fi calculată cînd prețurile sînt negative", "Este lentă: un regim nou are nevoie de luni pentru a umple fereastra, iar o zi de criză iese din fereastră la o dată fixă, astfel că VaR scade fără vreun motiv de piață", "Reacționează excesiv la variația de ieri, pentru că dă o pondere mai mare zilelor recente"],
                "correctExplanation": "În HS, fiecare zi din fereastră contează cu pondere întreagă timp de 365 de zile, apoi dispare brusc. Modelul reacționează deci cu întîrziere la începutul unei crize și își reduce VaR la o dată care nu are nicio legătură cu piața.",
                "incorrectExplanation": "HS nu folosește nicio repartiție și lucrează pe variații, definite și pentru prețuri negative; toate zilele au aceeași pondere. Problema ei este viteza, pe care o corectează tocmai simularea istorică filtrată."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Student-t at two levels",
                "text": "In the 2017–2026 backtest, the Student-t 99% value-at-risk (VaR) was exceeded on 1.98% of days and the Student-t 95% VaR on 8.75%. What does this say about the Student-t curve?",
                "options": ["It is well calibrated at both confidence levels", "Its fatter tails fix part of the 99% tail, but the curve is too narrow in the centre", "Its tails are too fat, so it is too prudent at 99%", "It fails only because it has fewer parameters than the normal curve"],
                "correctExplanation": "The third parameter, the degrees of freedom, fattens the tails: the 99% exceedance rate falls from 3.21% for the normal curve to 1.98%. At 95%, however, 8.75% of days lie above the VaR instead of 5%.",
                "incorrectExplanation": "Both rates are above their targets (1% and 5%), so the curve is not too prudent anywhere. The Student-t has three parameters, one more than the normal; its problem is the centre, not the number of parameters."
            },
            "ro": {
                "title": "Student-t la două niveluri",
                "text": "La testarea retrospectivă 2017–2026, valoarea la risc (VaR) de 99% obținută cu repartiția Student-t a fost depășită în 1,98% din zile, iar VaR Student-t de 95% în 8,75%. Ce arată aceste cifre despre repartiția Student-t?",
                "options": ["Este bine calibrată la ambele niveluri de încredere", "Cozile mai groase corectează o parte din coada de 99%, dar curba este prea îngustă în centru", "Cozile sînt prea groase, deci este prea prudentă la 99%", "Eșuează doar pentru că are mai puțini parametri decît repartiția normală"],
                "correctExplanation": "Al treilea parametru, numărul gradelor de libertate, îngroașă cozile: proporția depășirilor la 99% scade de la 3,21% pentru repartiția normală la 1,98%. La 95%, însă, 8,75% din zile se află peste VaR, în loc de 5%.",
                "incorrectExplanation": "Ambele proporții sînt peste ținte (1% și 5%), deci curba nu este prea prudentă nicăieri. Repartiția Student-t are trei parametri, cu unul mai mult decît cea normală; problema ei este centrul, nu numărul parametrilor."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "How FHS works",
                "text": "How does filtered historical simulation (FHS) build tomorrow's value-at-risk (VaR)?",
                "options": ["It sorts the last 365 raw price changes and reads their empirical quantile", "It fits a normal curve to the last year of changes and reads its quantile", "It fits a generalised Pareto curve to the largest losses only", "It divides past changes by their generalised autoregressive conditional heteroskedasticity (GARCH) volatility and rescales the standardised shocks by today's volatility"],
                "correctExplanation": "FHS takes the shape of the tail from history and the scale from the present: $\\text{VaR}^{\\text{FHS}}_{\\alpha,t}=\\mu_{d(t)}+\\sigma_t\\,\\hat q_\\alpha(z)$. In the backtest its 99% VaR was exceeded on 1.51% of days, and its 95% VaR passed the Kupiec test ($p$ = 0.120).",
                "incorrectExplanation": "Sorting raw changes is plain historical simulation, fitting a curve is the parametric approach, and the Pareto tail is extreme value theory. FHS combines a GARCH volatility with the empirical quantile of standardised shocks."
            },
            "ro": {
                "title": "Cum funcționează FHS",
                "text": "Cum construiește simularea istorică filtrată (FHS) valoarea la risc (VaR) pentru ziua de mîine?",
                "options": ["Ordonează ultimele 365 de variații brute ale prețului și citește cuantila lor empirică", "Ajustează o repartiție normală pe variațiile din ultimul an și citește cuantila ei", "Ajustează o curbă Pareto generalizată numai pe cele mai mari pierderi", "Împarte variațiile trecute la volatilitatea lor din modelul autoregresiv generalizat cu heteroscedasticitate condiționată (GARCH) și înmulțește șocurile standardizate cu volatilitatea de azi"],
                "correctExplanation": "FHS ia forma cozii din istorie și scala din prezent: $\\text{VaR}^{\\text{FHS}}_{\\alpha,t}=\\mu_{d(t)}+\\sigma_t\\,\\hat q_\\alpha(z)$. La testarea retrospectivă, VaR de 99% a fost depășită în 1,51% din zile, iar VaR de 95% a trecut testul Kupiec ($p$ = 0,120).",
                "incorrectExplanation": "Ordonarea variațiilor brute este simularea istorică simplă, ajustarea unei curbe este abordarea parametrică, iar coada Pareto ține de teoria valorilor extreme. FHS combină volatilitatea GARCH cu cuantila empirică a șocurilor standardizate."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "FHS below HS in October",
                "text": "In October 2026 the 99% value-at-risk (VaR) was 86.63 EUR per megawatt-hour (EUR/MWh) with historical simulation (HS) but 67.50 with filtered historical simulation (FHS). What explains the gap?",
                "options": ["HS still carried the volatile days of the past year in its window, while FHS used today's volatility, which was below the yearly average", "FHS ignores the largest days of its window", "HS uses a longer window of 730 days", "FHS assumes normally distributed shocks, which have thinner tails"],
                "correctExplanation": "HS gives every day of the last 365 the same weight; FHS rescales the shocks by today's generalised autoregressive conditional heteroskedasticity (GARCH) volatility, which in October 2026 was below the average of the past year. The gap is not noise but a different view of current risk.",
                "incorrectExplanation": "FHS uses the empirical quantile of its standardised shocks, not a normal curve, and keeps the large days in that quantile. The HS window is 365 days; it is the GARCH model of FHS that is refitted on 730 days."
            },
            "ro": {
                "title": "FHS sub HS în octombrie",
                "text": "În octombrie 2026, valoarea la risc (VaR) de 99% a fost 86,63 EUR pe megawatt-oră (EUR/MWh) prin simularea istorică (HS), dar 67,50 prin simularea istorică filtrată (FHS). Ce explică diferența?",
                "options": ["HS conținea încă în fereastră zilele volatile din ultimul an, în timp ce FHS folosea volatilitatea actuală, care era sub media anului", "FHS ignoră cele mai mari zile din fereastra sa", "HS folosește o fereastră mai lungă, de 730 de zile", "FHS presupune șocuri cu repartiție normală, care au cozi mai subțiri"],
                "correctExplanation": "HS dă aceeași pondere fiecărei zile din ultimele 365; FHS înmulțește șocurile cu volatilitatea de azi din modelul autoregresiv generalizat cu heteroscedasticitate condiționată (GARCH), care în octombrie 2026 era sub media ultimului an. Diferența nu este zgomot, ci o altă imagine a riscului curent.",
                "incorrectExplanation": "FHS folosește cuantila empirică a șocurilor standardizate, nu repartiția normală, și păstrează zilele mari în această cuantilă. Fereastra HS are 365 de zile; modelul GARCH din FHS este cel reestimat pe 730 de zile."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "The shape of the tail",
                "text": "Extreme value theory (EVT) fits a generalised Pareto distribution (GPD) to the tail. On raw Romanian price changes the shape parameter is $\\hat\\xi$ = 0.164; after the generalised autoregressive conditional heteroskedasticity (GARCH) filter, the median $\\hat\\xi$ is 0.011. How should a risk manager read this?",
                "options": ["The raw tail is light, and filtering makes it heavier", "Both estimates point to a bounded tail with a maximum loss", "The raw tail is heavy, with no moments above order 6.1, and the volatility filter absorbs most of it", "The shape parameter is stable, so it can be fixed once and for all"],
                "correctExplanation": "A positive $\\xi$ means a heavy tail, and moments above order $1/\\xi$ ≈ 6.1 do not exist. After dividing by the GARCH volatility, $\\hat\\xi$ is close to zero: most of the tail came from changing volatility.",
                "incorrectExplanation": "Bounded tails need $\\xi\\lt 0$, which is not the case here. Nor is $\\hat\\xi$ stable: it was positive in only 53% of the refits, which is why the model is refitted regularly."
            },
            "ro": {
                "title": "Forma cozii",
                "text": "Teoria valorilor extreme (EVT) ajustează pe coadă o repartiție Pareto generalizată (GPD). Pe variațiile brute ale prețului din România, parametrul de formă este $\\hat\\xi$ = 0,164; după filtrul modelului autoregresiv generalizat cu heteroscedasticitate condiționată (GARCH), $\\hat\\xi$ median este 0,011. Cum trebuie interpretate aceste valori?",
                "options": ["Coada brută este subțire, iar filtrul o îngroașă", "Ambele estimații indică o coadă mărginită, cu o pierdere maximă", "Coada brută este groasă, fără momente de ordin peste 6,1, iar filtrul volatilității preia cea mai mare parte a ei", "Parametrul de formă este stabil, deci poate fi fixat o dată pentru totdeauna"],
                "correctExplanation": "Un $\\xi$ pozitiv înseamnă o coadă groasă, iar momentele de ordin peste $1/\\xi$ ≈ 6,1 nu există. După împărțirea la volatilitatea GARCH, $\\hat\\xi$ este aproape de zero: cea mai mare parte a cozii provenea din volatilitatea variabilă.",
                "incorrectExplanation": "O coadă mărginită cere $\\xi\\lt 0$, ceea ce nu este cazul aici. Nici $\\hat\\xi$ nu este stabil: a fost pozitiv în doar 53% din reestimări, de aceea modelul se reestimează periodic."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Five VaR methods on the same day",
                "text": "For 100 megawatts (MW) flat, the table of the lecture gives the mean of the 31 forecasts made for October 2026 by five methods. Between which values does the 99% value-at-risk (VaR) lie?",
                "options": ["Between 162 and 167 thousand EUR, practically the same for all methods", "Between 64 and 87 thousand EUR", "Between 208 and 254 thousand EUR", "Between 154 and 208 thousand EUR, a gap that is a risk decision in itself"],
                "correctExplanation": "Extreme value theory gives 154 and historical simulation 208 thousand EUR for the same position on the same days. The gap is not noise: methods that use today's volatility differ from those that carry the past year in their window.",
                "incorrectExplanation": "64.33 to 86.63 are the VaRs in EUR per megawatt-hour, not in thousand EUR; multiplied by 2,400 MWh per day they give 154 to 208 thousand EUR. Choosing a method is therefore a risk decision, and the lecture advises reporting two methods side by side."
            },
            "ro": {
                "title": "Cinci metode VaR pentru aceeași zi",
                "text": "Pentru 100 de megawați (MW) în bandă, tabelul din curs dă media celor 31 de prognoze făcute de cinci metode pentru zilele din octombrie 2026. Între ce valori se află valoarea la risc (VaR) de 99%?",
                "options": ["Între 162 și 167 de mii EUR, practic aceeași pentru toate metodele", "Între 64 și 87 de mii EUR", "Între 208 și 254 de mii EUR", "Între 154 și 208 mii EUR, o diferență care este ea însăși o decizie de risc"],
                "correctExplanation": "Teoria valorilor extreme dă 154, iar simularea istorică 208 mii EUR pentru aceeași poziție, în aceleași zile. Diferența nu este zgomot: metodele care folosesc volatilitatea actuală diferă de cele care păstrează în fereastră ultimul an.",
                "incorrectExplanation": "Valorile de la 64,33 la 86,63 sînt VaR în EUR pe megawatt-oră, nu în mii EUR; înmulțite cu 2 400 MWh pe zi, ele dau între 154 și 208 mii EUR. Alegerea metodei este deci o decizie de risc, iar cursul recomandă raportarea a două metode alăturate."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Closest in the crisis",
                "text": "Between 1 Jul 2021 and 30 Jun 2023 (730 days), a correct 99% value-at-risk (VaR) should have been exceeded 7.3 times on Romanian prices. Which method came closest?",
                "options": ["Historical simulation (HS), with 28 exceedances", "The normal curve, with 45 exceedances", "Extreme value theory (EVT), with 17 exceedances", "The Student-t curve, with 29 exceedances"],
                "correctExplanation": "EVT had 17 exceedances and filtered historical simulation (FHS) 19. No method was right, but the filtered ones, which follow the generalised autoregressive conditional heteroskedasticity (GARCH) volatility, adapted within days.",
                "incorrectExplanation": "HS and the normal VaR waited for their windows to fill with crisis days, so they collected 28 and 45 exceedances. In a crisis, a model that reacts within days protects the cash."
            },
            "ro": {
                "title": "Cel mai aproape în criză",
                "text": "Între 1 iulie 2021 și 30 iunie 2023 (730 de zile), o valoare la risc (VaR) corectă de 99% ar fi trebuit depășită de 7,3 ori pe prețurile din România. Care metodă s-a apropiat cel mai mult?",
                "options": ["Simularea istorică (HS), cu 28 de depășiri", "Repartiția normală, cu 45 de depășiri", "Teoria valorilor extreme (EVT), cu 17 depășiri", "Repartiția Student-t, cu 29 de depășiri"],
                "correctExplanation": "EVT a avut 17 depășiri, iar simularea istorică filtrată (FHS) 19. Nicio metodă nu a fost corectă, dar metodele filtrate, care urmează volatilitatea din modelul autoregresiv generalizat cu heteroscedasticitate condiționată (GARCH), s-au adaptat în cîteva zile.",
                "incorrectExplanation": "HS și VaR normală au așteptat ca ferestrele lor să se umple cu zile de criză, așa că au acumulat 28 și 45 de depășiri. Într-o criză, un model care reacționează în cîteva zile protejează lichiditățile."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Scaling VaR to ten days",
                "text": "Your 1-day 99% value-at-risk (VaR) on a Romanian power position is 100 thousand EUR. Using the empirical ratio measured in the lecture for Romania, what is a realistic 10-day 99% VaR, and what would the square-root-of-time rule give?",
                "options": ["About 316 thousand EUR empirically, against 172 with the rule", "About 172 thousand EUR empirically, against 316 with the rule", "About 100 thousand EUR in both cases, since prices revert", "About 1,000 thousand EUR empirically, against 316 with the rule"],
                "correctExplanation": "The empirical 10-day 99% quantile is 1.72 times the 1-day one in Romania, while the rule multiplies by $\\sqrt{10}$ = 3.16. Power prices revert: the variance ratio at 10 days is 0.33, where 1 would mean a random walk.",
                "incorrectExplanation": "The square-root rule assumes independent daily changes. Power prices revert to a level set by fuel costs and the weekly calendar (autocorrelation −0.076 at lag 1, 0.474 at lag 7), so multiplying by 3.16 overstates the risk and wastes capital."
            },
            "ro": {
                "title": "VaR pe zece zile",
                "text": "Valoarea la risc (VaR) de 99% pe o zi pentru o poziție pe energie din România este de 100 de mii EUR. Folosind raportul empiric măsurat în curs pentru România, cît este o VaR realistă de 99% pe 10 zile și cît ar da regula rădăcinii pătrate a timpului?",
                "options": ["Circa 316 mii EUR empiric, față de 172 cu regula", "Circa 172 de mii EUR empiric, față de 316 cu regula", "Circa 100 de mii EUR în ambele cazuri, pentru că prețurile revin spre medie", "Circa 1 000 de mii EUR empiric, față de 316 cu regula"],
                "correctExplanation": "Cuantila empirică de 99% pe 10 zile este de 1,72 ori cea pe o zi în România, în timp ce regula înmulțește cu $\\sqrt{10}$ = 3,16. Prețurile energiei revin spre medie: raportul varianțelor la 10 zile este 0,33, iar valoarea 1 ar corespunde unui mers aleator.",
                "incorrectExplanation": "Regula rădăcinii pătrate presupune variații zilnice independente. Prețurile energiei revin spre un nivel stabilit de costul combustibililor și de calendarul săptămînal (autocorelație −0,076 la decalajul 1 și 0,474 la decalajul 7), deci înmulțirea cu 3,16 supraestimează riscul și blochează capital inutil."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Expected exceedances",
                "text": "The backtest covers 3,587 valid days from 1 Jan 2017 to 31 Oct 2026. How many exceedances of a correct 99% value-at-risk (VaR) should we expect?",
                "options": ["About 3.6", "About 17.9", "About 35.9", "About 179.4"],
                "correctExplanation": "A 99% VaR promises exceedances on 1% of days: 0.01 × 3,587 ≈ 35.9. Ten years of daily data make the Kupiec test sharp, while one year at 99% gives only 2–3 expected exceedances.",
                "incorrectExplanation": "Multiply the number of days by the promised share $p=1-\\alpha$ = 0.01. The value 179.4 is the expectation for a 95% VaR (5% of days)."
            },
            "ro": {
                "title": "Depășiri așteptate",
                "text": "Testarea retrospectivă acoperă 3 587 de zile valide, din 1 ianuarie 2017 pînă la 31 octombrie 2026. La cîte depășiri ale unei valori la risc (VaR) corecte de 99% ne așteptăm?",
                "options": ["Circa 3,6", "Circa 17,9", "Circa 35,9", "Circa 179,4"],
                "correctExplanation": "O VaR de 99% promite depășiri în 1% din zile: 0,01 × 3 587 ≈ 35,9. Zece ani de date zilnice fac testul Kupiec precis, în timp ce un singur an, la 99%, dă doar 2–3 depășiri așteptate.",
                "incorrectExplanation": "Numărul zilelor se înmulțește cu proporția promisă, $p=1-\\alpha$ = 0,01. Valoarea 179,4 este numărul așteptat pentru o VaR de 95% (5% din zile)."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Kupiec test result for FHS",
                "text": "Filtered historical simulation (FHS) had 54 exceedances of its 99% value-at-risk (VaR) over 3,587 days, against 35.9 expected, with a Kupiec likelihood ratio (LR) statistic $\\text{LR}_{uc}$ = 8.0. At the 5% level the critical value is 3.84. What is the verdict?",
                "options": ["Not rejected: 54 is close enough to 35.9", "Rejected: too many exceedances, even though FHS is among the best methods", "Rejected: too few exceedances, so the model is too prudent", "The test cannot be applied when there are more than 50 exceedances"],
                "correctExplanation": "8.0 exceeds 3.84, so FHS is rejected at 99%. In fact every method is rejected at 99% over ten years; the normal VaR, with 115 exceedances, has $\\text{LR}_{uc}$ = 111.5.",
                "incorrectExplanation": "With 3,587 days the test is sharp: 54 against 35.9 is a significant excess, not a small deviation, and it is an excess, not a shortfall. The $\\text{LR}_{uc}$ statistic follows a $\\chi^2_1$ distribution under the null whatever the count."
            },
            "ro": {
                "title": "Rezultatul testului Kupiec pentru FHS",
                "text": "Simularea istorică filtrată (FHS) a avut 54 de depășiri ale valorii la risc (VaR) de 99% în 3 587 de zile, față de 35,9 așteptate, iar statistica testului Kupiec, bazat pe raportul de verosimilitate (LR), este $\\text{LR}_{uc}$ = 8,0. La pragul de 5%, valoarea critică este 3,84. Care este verdictul?",
                "options": ["Nu se respinge: 54 este suficient de aproape de 35,9", "Se respinge: prea multe depășiri, deși FHS se numără printre cele mai bune metode", "Se respinge: prea puține depășiri, deci modelul este prea prudent", "Testul nu poate fi aplicat cînd sînt peste 50 de depășiri"],
                "correctExplanation": "8,0 depășește 3,84, deci FHS este respinsă la 99%. De fapt, pe zece ani toate metodele sînt respinse la 99%; VaR normală, cu 115 depășiri, are $\\text{LR}_{uc}$ = 111,5.",
                "incorrectExplanation": "Pe 3 587 de zile testul este precis: 54 față de 35,9 este un exces semnificativ, nu o abatere mică, și este un exces, nu un deficit. Statistica $\\text{LR}_{uc}$ urmează în ipoteza nulă o repartiție $\\chi^2_1$, oricare ar fi numărul depășirilor."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Limits of the Christoffersen test",
                "text": "For the 99% value-at-risk (VaR), the Christoffersen independence $p$-values are 0.682 for historical simulation (HS), 0.868 for the normal VaR and 0.199 for filtered historical simulation (FHS). What is the right reading?",
                "options": ["Exceedances are independent, so all three models are correct", "The test proves that exceedances never cluster in time", "The normal VaR is the best model, because its $p$-value is the highest", "Exceedances rarely fall on consecutive days, but they cluster in months, which a first-order test misses and the traffic light sees"],
                "correctExplanation": "The test compares $\\pi_{01}$ and $\\pi_{11}$, so it only looks at yesterday. The normal VaR was exceeded on 7.26% of days in 2021–2022 and on 2.33% in 2017–2020: clustering by months, which the 250-day traffic light detects.",
                "incorrectExplanation": "Passing the independence test says nothing about the number of exceedances (all three fail Kupiec at 99%), and a high $p$-value is not a ranking of models. A first-order test cannot see clustering over months."
            },
            "ro": {
                "title": "Limitele testului Christoffersen",
                "text": "Pentru valoarea la risc (VaR) de 99%, valorile $p$ ale testului de independență Christoffersen sînt 0,682 pentru simularea istorică (HS), 0,868 pentru VaR normală și 0,199 pentru simularea istorică filtrată (FHS). Care este interpretarea corectă?",
                "options": ["Depășirile sînt independente, deci toate cele trei modele sînt corecte", "Testul dovedește că depășirile nu se grupează niciodată în timp", "VaR normală este cel mai bun model, pentru că are cea mai mare valoare $p$", "Depășirile cad rareori în zile consecutive, dar se grupează pe luni, ceea ce un test de ordinul întîi nu observă, iar semaforul Basel observă"],
                "correctExplanation": "Testul compară $\\pi_{01}$ cu $\\pi_{11}$, deci privește numai ziua precedentă. VaR normală a fost depășită în 7,26% din zile în 2021–2022 și în 2,33% în 2017–2020: o grupare pe luni, pe care semaforul Basel, cu fereastra de 250 de zile, o detectează.",
                "incorrectExplanation": "Trecerea testului de independență nu spune nimic despre numărul depășirilor (toate trei pică testul Kupiec la 99%), iar o valoare $p$ mare nu ierarhizează modelele. Un test de ordinul întîi nu poate vedea gruparea pe luni."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Seven exceedances in 250 days",
                "text": "Over the last 250 days your 99% value-at-risk (VaR) was exceeded 7 times. In which zone of the traffic light of the Basel Committee on Banking Supervision (BCBS) is the model, and what does the Kupiec test say?",
                "options": ["Green zone; the Kupiec test does not reject", "Red zone; stop using the model at once", "Yellow zone; the Kupiec test gives $\\text{LR}_{uc}$ = 5.50 and $p$ = 0.019, so the model is rejected at 5%", "Yellow zone; the Kupiec test does not reject at 5%"],
                "correctExplanation": "The zones are green for 0–4, yellow for 5–9 and red for 10 or more exceedances. With 2.5 expected, 7 gives $\\text{LR}_{uc}$ = 5.50 and $p$ = 0.019: recalibrate, for example by moving from historical simulation to filtered historical simulation, and keep watching.",
                "incorrectExplanation": "Seven exceedances fall in the yellow band (5–9), not green or red. Yellow means recalibrate; red, which a correct model reaches with probability 0.025%, means stop using the model for limits."
            },
            "ro": {
                "title": "Șapte depășiri în 250 de zile",
                "text": "În ultimele 250 de zile, valoarea la risc (VaR) de 99% a fost depășită de 7 ori. În ce zonă a semaforului Comitetului de la Basel pentru Supraveghere Bancară (BCBS) se află modelul și ce arată testul Kupiec?",
                "options": ["În zona verde; testul Kupiec nu respinge modelul", "În zona roșie; modelul trebuie oprit imediat", "În zona galbenă; testul Kupiec dă $\\text{LR}_{uc}$ = 5,50 și $p$ = 0,019, deci modelul este respins la pragul de 5%", "În zona galbenă; testul Kupiec nu respinge modelul la pragul de 5%"],
                "correctExplanation": "Zonele sînt: verde pentru 0–4, galbenă pentru 5–9 și roșie pentru 10 sau mai multe depășiri. Cu 2,5 depășiri așteptate, 7 dau $\\text{LR}_{uc}$ = 5,50 și $p$ = 0,019: recalibrați modelul, de exemplu trecînd de la simularea istorică la simularea istorică filtrată, și continuați monitorizarea.",
                "incorrectExplanation": "Șapte depășiri cad în banda galbenă (5–9), nu în cea verde sau roșie. Zona galbenă cere recalibrarea; zona roșie, în care un model corect ajunge cu probabilitatea 0,025%, cere oprirea modelului pentru limite."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Days in the red zone",
                "text": "Over the 2017–2026 backtest on Romania, what share of days did the normal 99% value-at-risk (VaR) spend in the red zone of the Basel traffic light, compared with extreme value theory (EVT)?",
                "options": ["29.5% for the normal VaR, against 2.8% for EVT", "2.8% for the normal VaR, against 29.5% for EVT", "About 1% for both, as promised", "16.7% for the normal VaR, against 6.2% for EVT"],
                "correctExplanation": "The normal VaR spent almost a third of the days in the red zone, EVT only 2.8%. A correct model is red with probability 0.025%, so these red periods, concentrated in the crisis years, are strong evidence against the normal VaR.",
                "incorrectExplanation": "16.7% and 6.2% are the shares of historical simulation and filtered historical simulation. The ranking is clear: the normal VaR is the worst and the filtered methods are the best."
            },
            "ro": {
                "title": "Zile în zona roșie",
                "text": "Pe perioada de testare 2017–2026 pentru România, ce proporție din zile a petrecut în zona roșie a semaforului Basel valoarea la risc (VaR) normală de 99%, în comparație cu teoria valorilor extreme (EVT)?",
                "options": ["29,5% pentru VaR normală, față de 2,8% pentru EVT", "2,8% pentru VaR normală, față de 29,5% pentru EVT", "Circa 1% pentru amîndouă, cum s-a promis", "16,7% pentru VaR normală, față de 6,2% pentru EVT"],
                "correctExplanation": "VaR normală a stat aproape o treime din zile în zona roșie, EVT doar 2,8%. Un model corect ajunge în zona roșie cu probabilitatea 0,025%, deci aceste perioade roșii, concentrate în anii de criză, sînt un semnal puternic împotriva VaR normale.",
                "incorrectExplanation": "16,7% și 6,2% sînt proporțiile pentru simularea istorică și simularea istorică filtrată. Ierarhia este clară: VaR normală este cea mai slabă, iar metodele filtrate sînt cele mai bune."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Passing at 95%",
                "text": "In the ten-year backtest on Romania, which methods pass the Kupiec test for the 95% value-at-risk (VaR)?",
                "options": ["All five methods", "Only historical simulation (HS) and the normal curve", "Only the Student-t curve", "Only filtered historical simulation (FHS) and extreme value theory (EVT), with $p$-values of 0.120 and 0.139"],
                "correctExplanation": "FHS is exceeded on 5.58% of days and EVT on 5.55%, close to the 5% target. HS (6.16%), the normal curve (7.36%) and the Student-t (8.75%) are rejected.",
                "incorrectExplanation": "Only the filtered methods, which follow today's volatility, pass at 95%. At 99% every method is rejected, which is why the lecture advises holding extra capital for the 99% tail."
            },
            "ro": {
                "title": "Trecerea testului la 95%",
                "text": "La testarea retrospectivă pe zece ani pentru România, ce metode trec testul Kupiec pentru valoarea la risc (VaR) de 95%?",
                "options": ["Toate cele cinci metode", "Doar simularea istorică (HS) și repartiția normală", "Doar repartiția Student-t", "Doar simularea istorică filtrată (FHS) și teoria valorilor extreme (EVT), cu valori $p$ de 0,120 și 0,139"],
                "correctExplanation": "FHS este depășită în 5,58% din zile, iar EVT în 5,55%, aproape de ținta de 5%. HS (6,16%), repartiția normală (7,36%) și Student-t (8,75%) sînt respinse.",
                "incorrectExplanation": "Doar metodele filtrate, care urmează volatilitatea actuală, trec testul la 95%. La 99% toate metodele sînt respinse, de aceea cursul recomandă capital suplimentar pentru coada de 99%."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Backtests in 2021–2022",
                "text": "In 2021–2022 even the 99% value-at-risk (VaR) from filtered historical simulation (FHS) was exceeded on 2.88% of days in Romania, while since 2023 FHS and extreme value theory (EVT) are at 0.93%. What is the lesson?",
                "options": ["The gas shock moved the whole distribution, not only its scale; a model that looks good in calm years tells little about a crisis", "FHS is broken and should be replaced by the normal curve", "The failure in 2021–2022 was caused by missing data", "Since 2023 a 99% VaR is no longer needed"],
                "correctExplanation": "A volatility filter rescales the distribution but cannot anticipate a shift of its whole shape. Hence the advice: test every model on 2021–2022 before trusting it in a crisis.",
                "incorrectExplanation": "In the crisis every method failed, and the normal VaR worst of all (7.26%); since 2023 it still stays far off, at 2.00%. Only five days of the Romanian price are missing, so data gaps cannot explain the failure."
            },
            "ro": {
                "title": "Testele retrospective din 2021–2022",
                "text": "În 2021–2022, chiar și valoarea la risc (VaR) de 99% obținută prin simularea istorică filtrată (FHS) a fost depășită în 2,88% din zile în România, în timp ce din 2023 FHS și teoria valorilor extreme (EVT) sînt la 0,93%. Care este lecția?",
                "options": ["Șocul gazelor a mutat întreaga repartiție, nu doar scala ei; un model care arată bine în anii liniștiți spune puțin despre o criză", "FHS nu funcționează și trebuie înlocuită cu repartiția normală", "Eșecul din 2021–2022 s-a datorat datelor lipsă", "Din 2023, o VaR de 99% nu mai este necesară"],
                "correctExplanation": "Un filtru de volatilitate rescalează repartiția, dar nu poate anticipa o deplasare a întregii ei forme. De aici recomandarea: testați orice model pe 2021–2022 înainte de a vă baza pe el într-o criză.",
                "incorrectExplanation": "În criză toate metodele au eșuat, iar VaR normală cel mai mult (7,26%); din 2023 rămîne tot departe de țintă, la 2,00%. Din seria prețului din România lipsesc doar cinci zile, deci datele lipsă nu pot explica eșecul."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Reading the Z2 statistic",
                "text": "The Acerbi–Székely statistic $Z_2$ tests expected shortfall (ES) at 97.5%. In 2021–2022 the normal ES had $Z_2$ = 4.170, with a $p$-value below 0.001. What does a positive $Z_2$ mean?",
                "options": ["ES was too large, so the model was too prudent", "ES was too small: the losses beyond value-at-risk (VaR) were larger than forecast", "The exceedances were clustered in time", "The number of exceedances was exactly as promised"],
                "correctExplanation": "$Z_2$ averages the ratios of the exceedance losses to their ES forecasts, minus 1; if ES is right it is 0. In the crisis every ES was too small, the normal one by the widest margin; since 2023 filtered historical simulation, extreme value theory and historical simulation pass.",
                "incorrectExplanation": "ES cannot be checked by counting, because it is a statement about the size of the losses beyond VaR. A positive $Z_2$ signals underestimated tail losses, not over-prudence or clustering."
            },
            "ro": {
                "title": "Interpretarea statisticii Z2",
                "text": "Statistica Acerbi–Székely $Z_2$ testează deficitul așteptat (ES) de 97,5%. În 2021–2022, ES normal a avut $Z_2$ = 4,170, cu o valoare $p$ sub 0,001. Ce înseamnă un $Z_2$ pozitiv?",
                "options": ["ES a fost prea mare, deci modelul a fost prea prudent", "ES a fost prea mic: pierderile de dincolo de valoarea la risc (VaR) au fost mai mari decît s-a prognozat", "Depășirile au fost grupate în timp", "Numărul depășirilor a fost exact cel promis"],
                "correctExplanation": "$Z_2$ face media rapoartelor dintre pierderile din zilele cu depășiri și prognozele ES, minus 1; dacă ES este corect, valoarea este 0. În criză toate prognozele ES au fost prea mici, cele normale cu diferența cea mai mare; din 2023, simularea istorică filtrată, teoria valorilor extreme și simularea istorică trec testul.",
                "incorrectExplanation": "ES nu poate fi verificat prin numărare, pentru că se referă la mărimea pierderilor de dincolo de VaR. Un $Z_2$ pozitiv semnalează pierderi extreme subestimate, nu prudență excesivă sau grupare."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Tail days behind ES",
                "text": "The lecture advises judging a 97.5% expected shortfall (ES) on several years, never on one quarter. About how many tail days per year does such an ES rest on, with daily data?",
                "options": ["About 9", "About 36", "About 1", "About 25"],
                "correctExplanation": "2.5% of about 365 days is roughly 9 tail days a year, so a quarter holds only 2 or 3. That is why the comparison of ES models needs several years of data (Pele and Mazurencu-Marinescu-Pele, 2026).",
                "incorrectExplanation": "The tail share at 97.5% is $1-\\alpha$ = 2.5%, and 2.5% of a year of daily data is about 9 days. With so few observations, ranking models on a few tail days is unreliable."
            },
            "ro": {
                "title": "Zilele din coada ES",
                "text": "Cursul recomandă evaluarea deficitului așteptat (ES) de 97,5% pe mai mulți ani, niciodată pe un trimestru. Pe aproximativ cîte zile extreme pe an se sprijină un asemenea ES, cu date zilnice?",
                "options": ["Circa 9", "Circa 36", "Circa 1", "Circa 25"],
                "correctExplanation": "2,5% din circa 365 de zile înseamnă aproximativ 9 zile extreme pe an, deci un trimestru conține doar 2 sau 3. De aceea comparația modelelor ES are nevoie de mai mulți ani de date (Pele și Mazurencu-Marinescu-Pele, 2026).",
                "incorrectExplanation": "Proporția din coadă la 97,5% este $1-\\alpha$ = 2,5%, iar 2,5% dintr-un an de date zilnice înseamnă circa 9 zile. Cu atît de puține observații, ierarhizarea modelelor pe cîteva zile extreme nu este de încredere."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Conformal correction of VaR",
                "text": "In the work presented at AIDA 2026, each value-at-risk (VaR) forecast is widened by $\\hat q_V$, the 99% quantile of past scores, across 240 model–asset pairs. What happened to the number of pairs in the green zone of the Basel traffic light?",
                "options": ["It fell from 203/240 to 63/240", "It stayed at about one pair in four", "It rose to 240/240, and the clustering of exceedances also disappeared", "It rose from 63/240 raw to 203/240 with the fixed shift and to 234/240 with the rolling shift"],
                "correctExplanation": "The green-zone pairs rose from 26.2% raw to 84.6% with the fixed shift and 97.5% with the rolling 250-day shift. The exceedance rate is restored, but not their clustering, so the Christoffersen test keeps its role.",
                "incorrectExplanation": "One shift parameter restores the exceedance rate for most pairs, but it does not change the timing of exceedances. The same one-parameter widening is used for the day-ahead guarantee later in the lecture."
            },
            "ro": {
                "title": "Deplasarea conformală",
                "text": "În lucrarea prezentată la AIDA 2026, fiecare prognoză a valorii la risc (VaR) este lărgită cu $\\hat q_V$, cuantila de 99% a scorurilor trecute, pe 240 de perechi model–activ. Ce s-a întîmplat cu numărul perechilor din zona verde a semaforului Basel?",
                "options": ["A scăzut de la 203/240 la 63/240", "A rămas la circa o pereche din patru", "A crescut la 240/240, iar gruparea depășirilor a dispărut și ea", "A crescut de la 63/240 inițial la 203/240 cu deplasarea fixă și la 234/240 cu deplasarea glisantă"],
                "correctExplanation": "Perechile din zona verde au crescut de la 26,2% inițial la 84,6% cu deplasarea fixă și la 97,5% cu deplasarea glisantă pe 250 de zile. Rata depășirilor este refăcută, dar gruparea lor nu, astfel încît testul Christoffersen își păstrează rolul.",
                "incorrectExplanation": "Un singur parametru de deplasare reface rata depășirilor pentru majoritatea perechilor, dar nu schimbă momentul apariției lor. Aceeași lărgire cu un singur parametru este folosită mai departe în curs pentru garanția cerută pe piața pentru ziua următoare."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Computing the variation margin",
                "text": "You sold 100 lots of Brent futures (1,000 barrels each) to hedge your production, and today the price rises by 5 United States dollars (USD) per barrel. What happens tonight with the variation margin (VM)?",
                "options": ["You receive 500,000 USD in cash", "You pay 5,000 USD in cash", "You pay 500,000 USD in cash, although the physical oil you sell later is worth more", "Nothing is paid until the contract expires"],
                "correctExplanation": "$\\text{VM}_t=nK(F_t-F_{t-1})$ = 100 × 1,000 × 5 = 500,000 USD, paid in cash the same evening. The hedge works in value, but the cash leaves today while the gain on the physical sale arrives later.",
                "incorrectExplanation": "A short futures position loses when the price rises, and the clearing house settles gains and losses every evening. Forgetting the 1,000 barrels per lot gives the 5,000 USD slip."
            },
            "ro": {
                "title": "Calculul marjei de variație",
                "text": "Ați vîndut 100 de loturi futures Brent (cîte 1 000 de barili) pentru a vă acoperi producția, iar astăzi prețul crește cu 5 dolari americani (USD) pe baril. Ce se întîmplă diseară cu marja de variație (VM)?",
                "options": ["Primiți 500 000 USD în numerar", "Plătiți 5 000 USD în numerar", "Plătiți 500 000 USD în numerar, deși țițeiul pe care îl veți vinde mai tîrziu valorează mai mult", "Nu se plătește nimic pînă la scadența contractului"],
                "correctExplanation": "$\\text{VM}_t=nK(F_t-F_{t-1})$ = 100 × 1 000 × 5 = 500 000 USD, plătiți în numerar în aceeași seară. Acoperirea funcționează ca valoare, dar banii pleacă azi, iar cîștigul din vînzarea fizică vine mai tîrziu.",
                "incorrectExplanation": "O poziție futures vîndută pierde cînd prețul crește, iar casa de compensare decontează zilnic cîștigurile și pierderile. Omiterea celor 1 000 de barili dintr-un lot duce la cifra de 5 000 USD."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Procyclical margins",
                "text": "When Brent rose from 72.48 to 118.35 United States dollars (USD) in early 2026, the initial margin (IM) per lot computed on 12 months of history went from 5,970 to 16,313 USD (×2.73). With a floor computed on data since 2015 it rose only ×2.07. What else did the floor achieve?",
                "options": ["It raised the margin only in calm periods", "Losses beyond the IM occurred on 0.66% of days, against 1.80% with 12 months of history and a target of 1%", "It removed the need for variation margin", "It made the margin rise exactly as much as the 12-month version"],
                "correctExplanation": "The floor is one of the anti-procyclicality tools of the European Market Infrastructure Regulation (EMIR). It dampens the jump in a crisis and also makes the margin a better 99% quantile: 0.66% of days beyond the IM, against 1.80% with 12 months.",
                "incorrectExplanation": "A margin computed from the last 12 months rises exactly when the market becomes volatile, when cash is scarcest. The floor smooths this, and the lecture's numbers show it also protects better."
            },
            "ro": {
                "title": "Marje prociclice",
                "text": "Cînd prețul Brent a urcat de la 72,48 la 118,35 dolari americani (USD) la începutul anului 2026, marja inițială (IM) pe lot calculată cu 12 luni de date a crescut de la 5 970 la 16 313 USD (de 2,73 ori). Cu un prag calculat pe datele din 2015 încoace, a crescut doar de 2,07 ori. Ce a mai obținut pragul?",
                "options": ["A ridicat marja doar în perioadele liniștite", "Pierderile mai mari decît IM au apărut în 0,66% din zile, față de 1,80% cu 12 luni de date și de ținta de 1%", "A eliminat nevoia marjei de variație", "A făcut marja să crească exact cît versiunea pe 12 luni"],
                "correctExplanation": "Pragul este unul dintre instrumentele anticiclice din Regulamentul privind infrastructura pieței europene (EMIR). El atenuează saltul din criză și face din marjă și o cuantilă de 99% mai bună: 0,66% din zile peste IM, față de 1,80% cu 12 luni.",
                "incorrectExplanation": "O marjă calculată din ultimele 12 luni crește exact cînd piața devine volatilă, adică atunci cînd numerarul este cel mai greu de găsit. Pragul netezește acest efect, iar cifrele din curs arată că și protejează mai bine."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Liquidity needs of hedged firms",
                "text": "According to the European Central Bank (ECB), which firms were hurt most by margin calls in 2022, when Title Transfer Facility (TTF) gas futures reached 227 EUR per megawatt-hour (EUR/MWh) on 7 March 2022?",
                "options": ["Utilities and producers that had sold forward: hedgers whose physical gain would arrive only at delivery", "Speculators with large unhedged long positions", "Households on fixed-price supply contracts", "Banks that had lent to energy traders"],
                "correctExplanation": "The physical position of the hedgers gained value, but the gain would arrive only at delivery, while the margin had to be paid in cash immediately. By mid-2022 about twice as much initial margin was posted as in late 2021.",
                "incorrectExplanation": "A short forward hedge loses on the futures leg when prices rise, so the margin calls hit those who had sold forward. The risk that sinks a hedged company is liquidity, not the price itself."
            },
            "ro": {
                "title": "Nevoia de lichiditate a firmelor acoperite",
                "text": "Potrivit Băncii Centrale Europene (BCE), ce firme au fost cel mai grav afectate de apelurile în marjă din 2022, cînd contractele futures pe gaze la hubul olandez Title Transfer Facility (TTF) au atins 227 EUR pe megawatt-oră (EUR/MWh), la 7 martie 2022?",
                "options": ["Utilitățile și producătorii care vînduseră la termen: firme acoperite la risc, al căror cîștig fizic urma să vină abia la livrare", "Speculatorii cu poziții long mari, neacoperite", "Gospodăriile cu contracte de furnizare la preț fix", "Băncile care creditaseră traderii de energie"],
                "correctExplanation": "Poziția fizică a firmelor acoperite se apreciase, dar cîștigul urma să vină abia la livrare, în timp ce marja trebuia plătită imediat, în numerar. La jumătatea anului 2022 se depunea o marjă inițială de aproximativ două ori mai mare decît la sfîrșitul anului 2021.",
                "incorrectExplanation": "O acoperire prin vînzare la termen pierde pe contractul futures cînd prețul crește, deci apelurile în marjă i-au lovit pe cei care vînduseră la termen. Riscul care poate scufunda o companie acoperită este cel de lichiditate, nu prețul în sine."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Widening the guarantee",
                "text": "Your 99% quantile forecast of tomorrow's Romanian day-ahead price, from quantile regression (QR), was exceeded on 111 days out of 3,585 (coverage 96.90%). What does the lecture recommend, and at what cost for the guarantee?",
                "options": ["Switch to a normal curve, which brings coverage to 99% at no extra cost", "Keep the forecast: 96.90% is close enough to 99%", "Double the guarantee to be on the safe side", "Widen the tail with a conformal correction from recent errors: coverage rises to 98.47% for 7.5% more guarantee"],
                "correctExplanation": "The conformal correction $\\hat c_t$ is the 99% quantile of the past forecast errors, added to the QR forecast. Coverage rises from 96.90% to 98.47%, close to the promise, while the guarantee for 100 megawatts (MW) flat costs 0.371 million EUR per day on average.",
                "incorrectExplanation": "A forecast used for collateral must be calibrated in the tail, not only accurate on average. A one-parameter widening gets close to the promise without doubling the bank line."
            },
            "ro": {
                "title": "Lărgirea garanției",
                "text": "Prognoza dumneavoastră pentru cuantila de 99% a prețului de mîine pe piața pentru ziua următoare (PZU), obținută prin regresie cuantilică (QR), a fost depășită în 111 zile din 3 585 (acoperire de 96,90%). Ce recomandă cursul și cu ce cost pentru garanție?",
                "options": ["Trecerea la repartiția normală, care aduce acoperirea la 99% fără cost suplimentar", "Păstrarea prognozei: 96,90% este suficient de aproape de 99%", "Dublarea garanției, pentru siguranță", "Lărgirea cozii cu o corecție conformală calculată din erorile recente: acoperirea crește la 98,47%, cu o garanție mai mare cu 7,5%"],
                "correctExplanation": "Corecția conformală $\\hat c_t$ este cuantila de 99% a erorilor de prognoză din trecut, adăugată la prognoza QR. Acoperirea crește de la 96,90% la 98,47%, aproape de promisiune, iar garanția pentru 100 de megawați (MW) în bandă costă în medie 0,371 milioane EUR pe zi.",
                "incorrectExplanation": "O prognoză folosită pentru garanții trebuie să fie calibrată în coadă, nu doar precisă în medie. O lărgire cu un singur parametru se apropie de promisiune fără a dubla linia bancară."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Position limit in MW",
                "text": "The board sets a daily value-at-risk (VaR) budget of 250,000 EUR, which the desk converts into a maximum flat position in megawatts (MW): $Q^{\\max}=B/(24\\cdot\\text{VaR})$. On 12 Jul 2022 the 99% VaR from filtered historical simulation (FHS) was 245.80 EUR per megawatt-hour (EUR/MWh). What was the limit?",
                "options": ["42 MW", "514 MW", "196 MW", "1,017 MW"],
                "correctExplanation": "250,000 / (24 × 245.80) ≈ 42 MW. With the median VaR of 2019 (20.27 EUR/MWh) the same budget allows 514 MW, and on 31 Oct 2026 (VaR 53.15) 196 MW.",
                "incorrectExplanation": "514 MW and 196 MW are the limits for 2019 and 31 Oct 2026. A fixed EUR budget forces the position to shrink when the market becomes dangerous, while a fixed MW limit lets the money at risk grow with volatility."
            },
            "ro": {
                "title": "Limita de poziție în MW",
                "text": "Conducerea stabilește un buget zilnic de valoare la risc (VaR) de 250 000 EUR, pe care biroul de tranzacționare îl transformă într-o poziție maximă în bandă, în megawați (MW): $Q^{\\max}=B/(24\\cdot\\text{VaR})$. La 12 iulie 2022, VaR de 99% obținută prin simularea istorică filtrată (FHS) a fost 245,80 EUR pe megawatt-oră (EUR/MWh). Care a fost limita?",
                "options": ["42 MW", "514 MW", "196 MW", "1 017 MW"],
                "correctExplanation": "250 000 / (24 × 245,80) ≈ 42 MW. Cu VaR mediană din 2019 (20,27 EUR/MWh), același buget permite 514 MW, iar la 31 octombrie 2026 (VaR 53,15) 196 MW.",
                "incorrectExplanation": "514 MW și 196 MW sînt limitele pentru 2019 și pentru 31 octombrie 2026. Un buget fix în EUR obligă poziția să se micșoreze cînd piața devine periculoasă, în timp ce o limită fixă în MW lasă suma expusă la risc să crească odată cu volatilitatea."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Supplier's monthly overrun",
                "text": "For a supplier with 100 megawatts (MW) on average, the normal 99% limit on the monthly overrun of the load-weighted cost, estimated on 2015–2020, is +50.5%. What happened from 2021 onwards?",
                "options": ["It was never exceeded, as the normal curve promises", "It was exceeded 3 times against 0.7 expected, and the worst month was Nov 2024, with +86.6%", "It was exceeded in every month of 2022", "It was exceeded once, in the peak month of the 2022 crisis"],
                "correctExplanation": "The normal limit failed again: 3 breaches against 0.7 expected. The worst month, Nov 2024 (+86.6%, 5.96 million EUR), came after the summer of 2024, not in the 2022 crisis: monthly risk depends on the jump from one month to the next, not on the price level.",
                "incorrectExplanation": "Empirically the 95% cash-flow-at-risk (CFaR) is +39.9% (2.84 million EUR) and the 95% expected shortfall (ES) +60.2% (6.49 million EUR). A fixed retail offer should carry an ES-based premium or be hedged forward."
            },
            "ro": {
                "title": "Depășirea lunară a furnizorului",
                "text": "Pentru un furnizor cu 100 de megawați (MW) în medie, limita normală de 99% pentru depășirea lunară a costului ponderat cu consumul, estimată pe 2015–2020, este +50,5%. Ce s-a întîmplat începînd din 2021?",
                "options": ["Nu a fost depășită niciodată, cum promite repartiția normală", "A fost depășită de 3 ori, față de 0,7 așteptate, iar cea mai proastă lună a fost noiembrie 2024, cu +86,6%", "A fost depășită în fiecare lună din 2022", "A fost depășită o singură dată, în luna de vîrf a crizei din 2022"],
                "correctExplanation": "Limita normală a eșuat din nou: 3 depășiri, față de 0,7 așteptate. Cea mai proastă lună, noiembrie 2024 (+86,6%, 5,96 milioane EUR), a venit după vara anului 2024, nu în criza din 2022: riscul lunar depinde de saltul de la o lună la alta, nu de nivelul prețului.",
                "incorrectExplanation": "Empiric, fluxul de numerar la risc (CFaR) de 95% este +39,9% (2,84 milioane EUR), iar deficitul așteptat (ES) de 95% este +60,2% (6,49 milioane EUR). O ofertă cu preț fix ar trebui să includă o primă calculată din ES sau să fie acoperită la termen."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Supplier versus producer",
                "text": "On daily Romanian data from 1 Jan 2015 to 31 Oct 2026, the 99% quantile of the price change is +88.21 EUR per megawatt-hour (EUR/MWh) and the 1% quantile is −70.74 EUR/MWh. Who faces the heavier price tail?",
                "options": ["The supplier, who buys and loses when prices rise: prices jump up more than down, and the skewness is 1.02", "The producer, who sells and loses when prices fall, because falls are more frequent", "Both equally, since they face the same price", "Neither: only the level of the price matters, not its changes"],
                "correctExplanation": "There is one distribution of $X_t$ but two tails. The expected shortfall (ES) at 97.5% is 91.29 for the supplier against 74.92 for the producer; on monthly base prices the 95% quantile of the change is +42.4% and the 5% quantile −32.3%.",
                "incorrectExplanation": "Same price does not mean same risk: the buyer's loss is $+Q\\,24\\,X_t$ and the seller's $-Q\\,24\\,X_t$, and the upper tail is longer. The producer's price risk is smaller, although a dry year adds volume risk."
            },
            "ro": {
                "title": "Furnizor față de producător",
                "text": "Pe datele zilnice din România, 1 ianuarie 2015 – 31 octombrie 2026, cuantila de 99% a variației prețului este +88,21 EUR pe megawatt-oră (EUR/MWh), iar cuantila de 1% este −70,74 EUR/MWh. Cine are coada de preț mai groasă?",
                "options": ["Furnizorul, care cumpără și pierde cînd prețul crește: prețurile sar mai mult în sus decît în jos, iar asimetria este 1,02", "Producătorul, care vinde și pierde cînd prețul scade, pentru că scăderile sînt mai frecvente", "Amîndoi la fel, pentru că se confruntă cu același preț", "Niciunul: contează doar nivelul prețului, nu variațiile lui"],
                "correctExplanation": "Există o singură repartiție a lui $X_t$, dar două cozi. Deficitul așteptat (ES) de 97,5% este 91,29 pentru furnizor, față de 74,92 pentru producător; pe prețul de bază lunar, cuantila de 95% a variației este +42,4%, iar cuantila de 5% −32,3%.",
                "incorrectExplanation": "Același preț nu înseamnă același risc: pierderea cumpărătorului este $+Q\\,24\\,X_t$, a vînzătorului $-Q\\,24\\,X_t$, iar coada superioară este mai lungă. Riscul de preț al producătorului este mai mic, deși un an secetos adaugă riscul de volum."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Number of firms in a systemic risk measure",
                "text": "The Energy Financial Risk Meter (EFRM), built on 100 European energy firms, together with the Composite Indicator of Systemic Stress (CISS) predicts volatile months with an area under the curve (AUC) of 0.731. The case study C4 replication on OMV Petrom, Romgaz and Nuclearelectrica gave an AUC of 0.38, against 0.61 for past volatility. What is the lesson?",
                "options": ["Systemic risk meters do not work for energy firms", "A systemic meter needs many firms, as in the paper; three firms are too few", "Past volatility is always the better systemic indicator", "Romanian energy firms carry no systemic risk"],
                "correctExplanation": "The EFRM is the mean LASSO penalty (least absolute shrinkage and selection operator) across many firms; its strength comes from the breadth of the cross-section. On 100 firms it captures the shocks of 2020 and 2022 and has a break in July 2021.",
                "incorrectExplanation": "The weak result on three firms reflects the small cross-section, not a failure of the method. A firm's own value-at-risk cannot see contagion, so the lecture advises reading a sector meter next to it."
            },
            "ro": {
                "title": "Numărul de firme într-o măsură a riscului sistemic",
                "text": "Indicatorul de risc financiar al sectorului energetic (EFRM), construit pe 100 de companii energetice europene, împreună cu indicatorul compozit de stres sistemic (CISS) al Băncii Centrale Europene (BCE), prognozează lunile volatile cu o arie de sub curbă (AUC) de 0,731. Replicarea din studiul de caz C4 pe OMV Petrom, Romgaz și Nuclearelectrica a dat o AUC de 0,38, față de 0,61 pentru volatilitatea trecută. Care este lecția?",
                "options": ["Indicatorii de risc sistemic nu funcționează pentru companiile energetice", "Un indicator sistemic are nevoie de multe companii, ca în lucrare; trei companii sînt prea puține", "Volatilitatea trecută este întotdeauna un indicator sistemic mai bun", "Companiile energetice din România nu au risc sistemic"],
                "correctExplanation": "EFRM este penalizarea medie a operatorului de contracție și selecție în normă absolută (LASSO) pe multe companii; puterea lui vine din numărul mare de firme. Pe 100 de companii surprinde șocurile din 2020 și 2022 și are o ruptură în iulie 2021.",
                "incorrectExplanation": "Rezultatul slab pe trei companii reflectă eșantionul mic, nu un eșec al metodei. Valoarea la risc (VaR) proprie a unei firme nu vede contagiunea, de aceea cursul recomandă urmărirea alături de ea a unui indicator sectorial."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Autumn 2026: liquidity risk",
                "text": "Between June and October 2026 the monthly mean of the Romanian day-ahead price rose from 122.99 to 239.32 EUR per megawatt-hour (EUR/MWh), while the 99% value-at-risk (VaR) from filtered historical simulation (FHS) moved only from 61.64 to 67.50. What was the real danger for a supplier of 100 megawatts (MW)?",
                "options": ["Market risk: the VaR was exceeded far too often", "Too few exceedances, so the model was far too prudent", "Cash: the day-ahead guarantee rose from 0.416 to 0.776 million EUR per day, and three monthly cost overruns came in a row", "Currency risk, because Brent is priced in dollars"],
                "correctExplanation": "Over the 153 days a correct 99% VaR should have been exceeded 1.5 times, and FHS was exceeded 2 times: by the daily VaR nothing alarming happened. Cash needs doubled, and the bill rose by +25.1%, +16.2% and +34.0% in August, September and October.",
                "incorrectExplanation": "A slow rise through many moderate daily changes passes the VaR tests and still drains cash. A risk report needs a liquidity line next to VaR: guarantees, margins and the cumulative monthly overrun."
            },
            "ro": {
                "title": "Toamna 2026: riscul de lichiditate",
                "text": "Între iunie și octombrie 2026, media lunară a prețului de pe piața pentru ziua următoare (PZU) din România a crescut de la 122,99 la 239,32 EUR pe megawatt-oră (EUR/MWh), în timp ce valoarea la risc (VaR) de 99% obținută prin simularea istorică filtrată (FHS) s-a modificat doar de la 61,64 la 67,50. Care a fost pericolul real pentru un furnizor de 100 de megawați (MW)?",
                "options": ["Riscul de piață: VaR a fost depășită mult prea des", "Prea puține depășiri, deci un model mult prea prudent", "Lichiditățile: garanția pentru PZU a crescut de la 0,416 la 0,776 milioane EUR pe zi, iar trei depășiri lunare ale costului au venit la rînd", "Riscul valutar, pentru că Brent se cotează în dolari"],
                "correctExplanation": "În cele 153 de zile, o VaR corectă de 99% ar fi trebuit depășită de 1,5 ori, iar FHS a fost depășită de 2 ori: judecînd după VaR zilnică, nu s-a întîmplat nimic alarmant. Nevoia de lichidități s-a dublat, iar factura a crescut cu +25,1%, +16,2% și +34,0% în august, septembrie și octombrie.",
                "incorrectExplanation": "O creștere lentă, prin multe variații zilnice moderate, trece testele VaR, dar consumă lichidități. Un raport de risc are nevoie, alături de VaR, de o secțiune de lichiditate: garanții, marje și depășirea cumulată a costului lunar."
            }
        }
    ]
};
