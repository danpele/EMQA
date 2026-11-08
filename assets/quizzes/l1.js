// ============================================================
// Quiz bank for lecture id 'l1': Energy markets and their data (EN + RO)
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.EMQA_DATA.quizzes['l1'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 2,
            "en": {
                "title": "Uniform clearing price",
                "text": "On the day-ahead market (PZU, Piața pentru Ziua Următoare), a wind farm with a marginal cost close to zero and a gas plant are both accepted in the same quarter-hour, and the gas plant's offer is the last one accepted. What price does the wind farm receive?",
                "options": [
                    "Its own offer price, close to zero, as in a pay-as-bid auction",
                    "The volume-weighted average of all accepted offers",
                    "The single clearing price set by the gas plant's marginal offer",
                    "The average cost of the power system in that quarter-hour"
                ],
                "correctExplanation": "Every accepted trade is paid the single clearing price $p_t^{*}$, set by the last accepted (marginal) offer. The wind farm keeps the gap between this price and its own cost.",
                "incorrectExplanation": "The PZU is a uniform-price auction, not pay-as-bid: the marginal offer sets one price for all accepted sellers and buyers. This is why a supplier pays the cost of the most expensive plant needed, not the average cost of the system."
            },
            "ro": {
                "title": "Prețul unic de închidere",
                "text": "Pe Piața pentru Ziua Următoare (PZU), un parc eolian cu un cost marginal aproape de zero și o centrală pe gaze sînt acceptate în același sfert de oră, iar oferta centralei pe gaze este ultima acceptată. Ce preț primește parcul eolian?",
                "options": [
                    "Prețul din propria ofertă, aproape de zero, ca într-o licitație cu plata la prețul ofertat",
                    "Media ponderată cu volumele a tuturor ofertelor acceptate",
                    "Prețul unic de închidere, stabilit de oferta marginală a centralei pe gaze",
                    "Costul mediu al sistemului energetic în acel sfert de oră"
                ],
                "correctExplanation": "Toate tranzacțiile acceptate se decontează la prețul unic de închidere $p_t^{*}$, stabilit de ultima ofertă acceptată (cea marginală). Parcul eolian păstrează diferența dintre acest preț și propriul cost.",
                "incorrectExplanation": "PZU este o licitație cu preț unic, nu cu plata la prețul ofertat: oferta marginală stabilește un singur preț pentru toți vînzătorii și cumpărătorii acceptați. De aceea un furnizor plătește prețul fixat de centrala marginală, nu costul mediu al sistemului."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Inframarginal rent",
                "text": "A nuclear unit with a marginal cost close to zero is paid the clearing price set by a gas plant on the day-ahead market (PZU, Piața pentru Ziua Următoare). What is the difference between that price and the nuclear unit's marginal cost called, and what is its role?",
                "options": [
                    "The inframarginal rent, which pays for the unit's capacity",
                    "The water value, which rewards keeping fuel for later use",
                    "The congestion rent, which pays for the cross-border lines",
                    "The imbalance charge, collected in real time by the transmission system operator (TSO)"
                ],
                "correctExplanation": "Every accepted seller receives the marginal price, including those with much lower costs; the difference between price and cost, the inframarginal rent, is what pays for their capacity.",
                "incorrectExplanation": "The water value is the opportunity cost of reservoir hydro, the congestion rent arises between zones and imbalance is settled per 15 minutes by Transelectrica; the margin of a low-cost plant inside one auction is the inframarginal rent."
            },
            "ro": {
                "title": "Renta inframarginală",
                "text": "O unitate nucleară cu un cost marginal aproape de zero primește pe Piața pentru Ziua Următoare (PZU) prețul de închidere stabilit de o centrală pe gaze. Cum se numește diferența dintre acest preț și costul marginal al unității nucleare și ce rol are?",
                "options": [
                    "Renta inframarginală, care acoperă investiția în capacitate",
                    "Valoarea apei, care răsplătește păstrarea resursei pentru mai tîrziu",
                    "Renta de congestie, care plătește liniile de interconexiune",
                    "Costul dezechilibrului, încasat în timp real de operatorul de transport și de sistem (TSO)"
                ],
                "correctExplanation": "Toți vînzătorii acceptați primesc prețul marginal, inclusiv cei cu costuri mult mai mici; diferența dintre preț și costul lor, renta inframarginală, este cea care le acoperă investiția în capacitate.",
                "incorrectExplanation": "Valoarea apei este costul de oportunitate al hidrocentralelor cu lac, renta de congestie apare între zone, iar dezechilibrele se decontează la 15 minute de Transelectrica; marja unei centrale ieftine în cadrul aceleiași licitații este renta inframarginală."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Midday versus evening price",
                "text": "On 21 October 2026 the aggregated curves published by OPCOM, the Romanian electricity and gas market operator, cleared at 152.23 euro per megawatt-hour (EUR/MWh) at midday and at 244.00 EUR/MWh in the evening. What best explains the difference?",
                "options": [
                    "Evening buyers bid higher prices, so the demand curve became almost flat",
                    "Random noise in bidding behaviour that averages out over the day",
                    "The evening quarter-hour was cleared under a different price floor",
                    "Without sun, the crossing moved to the steep part of the supply curve, which included 1,054 megawatts (MW) of net imports"
                ],
                "correctExplanation": "At midday 2,333 MW were offered at zero or negative prices (solar, wind, nuclear, run-of-river hydro). In the evening there was no sun, and the curves crossed on the steep part of the supply curve.",
                "incorrectExplanation": "The demand curve is almost vertical and both quarter-hours were cleared by the same auction under the same rules; the gap is not noise but the shape of the supply curve at two different levels of renewable output."
            },
            "ro": {
                "title": "Prețul de la amiază și cel de seară",
                "text": "La 21 octombrie 2026, curbele agregate publicate de operatorul pieței de energie electrică și gaze naturale din România (OPCOM) s-au intersectat la 152,23 euro pe megawatt-oră (EUR/MWh) la amiază și la 244,00 EUR/MWh seara. Ce explică cel mai bine diferența?",
                "options": [
                    "Cumpărătorii de seară au ofertat prețuri mai mari, iar curba cererii a devenit aproape orizontală",
                    "Un zgomot aleator în comportamentul ofertanților, care se compensează în cursul zilei",
                    "Sfertul de oră de seară a fost tranzacționat cu un alt prag minim de preț",
                    "Fără soare, intersecția s-a mutat pe porțiunea abruptă a curbei ofertei, care includea 1 054 megawați (MW) import net"
                ],
                "correctExplanation": "La amiază, 2 333 MW erau oferiți la preț zero sau negativ (solar, eolian, nuclear, hidro pe firul apei). Seara nu mai era soare, iar curbele s-au intersectat pe porțiunea abruptă a curbei ofertei.",
                "incorrectExplanation": "Curba cererii este aproape verticală, iar ambele sferturi de oră au fost tranzacționate în aceeași licitație, după aceleași reguli; diferența nu este zgomot, ci forma curbei ofertei la două niveluri diferite ale producției din surse regenerabile."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Gate closure in Bucharest",
                "text": "Bids for delivery day $d$ on the day-ahead market (PZU, Piața pentru Ziua Următoare) must be sent on day $d-1$ before gate closure at 12:00 Central European Time (CET). What is the deadline on a Bucharest clock, which runs on Eastern European Time (EET)?",
                "options": [
                    "11:00 Bucharest time",
                    "13:00 Bucharest time",
                    "12:00 Bucharest time, since the Single Day-Ahead Coupling (SDAC) uses each zone's local time",
                    "14:00 Bucharest time"
                ],
                "correctExplanation": "EET is one hour ahead of CET, so gate closure at 12:00 CET is 13:00 in Bucharest. After the auction, positions are corrected intraday, and what remains wrong is settled as imbalance per 15 minutes.",
                "incorrectExplanation": "The coupled European auction has one gate closure, defined in CET; Romania runs one hour ahead, so a Romanian trader must bid before 13:00 local time."
            },
            "ro": {
                "title": "Termenul-limită la București",
                "text": "Ofertele pentru ziua de livrare $d$ pe Piața pentru Ziua Următoare (PZU) se transmit în ziua $d-1$, pînă la termenul-limită de la ora 12:00, ora Europei Centrale (CET). Care este termenul-limită după ceasul de la București, care folosește ora Europei de Est (EET)?",
                "options": [
                    "Ora 11:00, ora Bucureștiului",
                    "Ora 13:00, ora Bucureștiului",
                    "Ora 12:00, ora Bucureștiului, deoarece cuplarea unică a piețelor pentru ziua următoare (SDAC) folosește ora locală a fiecărei zone",
                    "Ora 14:00, ora Bucureștiului"
                ],
                "correctExplanation": "EET este cu o oră înaintea CET, deci termenul de la ora 12:00 CET înseamnă ora 13:00 la București. După licitație, pozițiile se ajustează pe piața intrazilnică, iar ce rămîne neacoperit se decontează ca dezechilibru, la 15 minute.",
                "incorrectExplanation": "Licitația europeană cuplată are un singur termen-limită, definit în CET; România este cu o oră înainte, așa că un trader român trebuie să liciteze pînă la ora 13:00, ora locală."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Price floor and censoring",
                "text": "On 1 May 2026 the lowest German quarter-hour price was −499.99 euro per megawatt-hour (EUR/MWh), at the harmonised floor of −500 EUR/MWh then in force. How should an analyst treat such observations?",
                "options": [
                    "As censored values: the true willingness to pay was even lower, so treating them as ordinary data understates the extreme",
                    "As data errors, to be deleted and interpolated from the neighbouring quarter-hours",
                    "As ordinary observations, since the floor is part of the market rules",
                    "As outliers, to be replaced by the median price of the day"
                ],
                "correctExplanation": "A series that touches the floor is censored there. After such prices on 26 April and 1 May, the harmonised minimum was lowered to −600 EUR/MWh for delivery from 29 May 2026.",
                "incorrectExplanation": "The floor cuts off the true equilibrium price; a model that treats it as an ordinary observation understates how extreme the situation was, and real prices are never deleted or interpolated."
            },
            "ro": {
                "title": "Pragul minim și cenzurarea",
                "text": "La 1 mai 2026, cel mai mic preț pe sfert de oră din Germania a fost de −499,99 euro pe megawatt-oră (EUR/MWh), egal cu pragul minim armonizat de −500 EUR/MWh în vigoare atunci. Cum trebuie să trateze analistul asemenea observații?",
                "options": [
                    "Ca valori cenzurate: prețul de echilibru ar fi fost și mai mic, deci tratarea lor ca date obișnuite subestimează situația extremă",
                    "Ca erori de date, care se șterg și se interpolează din sferturile de oră vecine",
                    "Ca observații obișnuite, deoarece pragul face parte din regulile pieței",
                    "Ca valori aberante, care se înlocuiesc cu prețul median al zilei"
                ],
                "correctExplanation": "O serie care atinge pragul este cenzurată. După asemenea prețuri la 26 aprilie și la 1 mai, prețul minim armonizat a coborît la −600 EUR/MWh pentru livrările începînd cu 29 mai 2026.",
                "incorrectExplanation": "Pragul taie prețul real de echilibru; un model care îl tratează ca pe o observație obișnuită subestimează cît de extremă a fost situația, iar prețurile reale nu se șterg și nu se interpolează."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Reading a cross-border gap",
                "text": "Under European market coupling, the Romanian and Hungarian day-ahead prices differ in a given hour. Since 8 June 2022 this border has been part of the Core region's flow-based allocation. What can an analyst conclude from the price gap alone?",
                "options": [
                    "That the Romania–Hungary interconnector itself was full in that hour",
                    "Nothing at all, since coupled zones always have equal prices",
                    "That a network limit was binding, but not which element was binding",
                    "That Romania was exporting power to Hungary in that hour"
                ],
                "correctExplanation": "Cheap zones export to expensive ones until a network limit binds; if no limit binds, prices are equal. Under flow-based allocation the limits sit on critical network elements, so a gap does not say which line was full.",
                "incorrectExplanation": "Coupling equalises prices only while the network is not binding, and power flows towards the higher price; equal prices do not prove an uncongested border, and a gap does not identify the binding line."
            },
            "ro": {
                "title": "Interpretarea unei diferențe de preț",
                "text": "În cuplarea piețelor europene, prețurile pentru ziua următoare din România și Ungaria diferă într-o anumită oră. Din 8 iunie 2022, la această graniță se aplică alocarea bazată pe fluxuri din regiunea Core. Ce poate conchide analistul numai din diferența de preț?",
                "options": [
                    "Că interconexiunea România–Ungaria însăși era plină în acea oră",
                    "Nimic, deoarece zonele cuplate au întotdeauna prețuri egale",
                    "Că o limită a rețelei era atinsă, dar nu și care element de rețea",
                    "Că România exporta energie în Ungaria în acea oră"
                ],
                "correctExplanation": "Zonele cu prețuri mici exportă către cele cu prețuri mari pînă cînd se atinge o limită a rețelei; dacă nicio limită nu este atinsă, prețurile sînt egale. În alocarea bazată pe fluxuri, limitele sînt pe elementele critice ale rețelei, deci diferența nu arată ce linie și-a atins limita.",
                "incorrectExplanation": "Cuplarea egalizează prețurile numai cît timp rețeaua nu este la limită, iar energia circulă spre prețul mai mare; prețurile egale nu dovedesc absența congestiilor, iar o diferență nu identifică linia saturată."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "From 24 to 96 prices",
                "text": "Since which date has the Single Day-Ahead Coupling (SDAC) cleared with a 15-minute market time unit (MTU), giving Romania 96 day-ahead prices on a normal day instead of 24?",
                "options": [
                    "17 June 2021",
                    "8 June 2022",
                    "29 May 2026",
                    "1 October 2025"
                ],
                "correctExplanation": "On 1 October 2025 SDAC moved to a 15-minute MTU. Every count of hours since then must be converted into hour-equivalents before comparing years.",
                "incorrectExplanation": "17 June 2021 is when Romania joined SDAC through the 4M interim coupling, 8 June 2022 when the Romania–Hungary border moved to Core flow-based allocation, and 29 May 2026 when the price floor became −600 EUR/MWh (euro per megawatt-hour)."
            },
            "ro": {
                "title": "De la 24 la 96 de prețuri",
                "text": "De la ce dată cuplarea unică a piețelor pentru ziua următoare (SDAC) folosește un interval de tranzacționare (MTU) de 15 minute, astfel încît România are 96 de prețuri pentru ziua următoare într-o zi obișnuită, în loc de 24?",
                "options": [
                    "17 iunie 2021",
                    "8 iunie 2022",
                    "29 mai 2026",
                    "1 octombrie 2025"
                ],
                "correctExplanation": "La 1 octombrie 2025, SDAC a trecut la un MTU de 15 minute. De atunci, orice număr de ore trebuie convertit în ore echivalente înainte de a compara anii între ei.",
                "incorrectExplanation": "La 17 iunie 2021 România a aderat la SDAC prin cuplarea interimară 4M, la 8 iunie 2022 granița România–Ungaria a trecut la alocarea bazată pe fluxuri din regiunea Core, iar la 29 mai 2026 pragul minim de preț a devenit −600 EUR/MWh (euro pe megawatt-oră)."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Reporting negative hours",
                "text": "In January–October 2026, 687 Romanian quarter-hours on the day-ahead market (PZU, Piața pentru Ziua Următoare) had a negative price. How should this be reported to the board so that it is comparable with earlier, hourly years?",
                "options": [
                    "687 negative hours",
                    "687 quarter-hours (171.75 hours)",
                    "687 quarter-hours (2,748 hours)",
                    "687 quarter-hours (57.25 hours)"
                ],
                "correctExplanation": "Each quarter-hour counts as 15/60 of an hour: $H=687\\times 15/60=171.75$ hour-equivalents. The report should name the unit and give both numbers.",
                "incorrectExplanation": "Counting each quarter-hour as an hour overstates the duration by a factor of 4 and makes 2026 look far worse than earlier years; multiplying by 4 or dividing by 12 confuses the conversion."
            },
            "ro": {
                "title": "Raportarea orelor negative",
                "text": "În ianuarie–octombrie 2026, 687 de sferturi de oră de pe Piața pentru Ziua Următoare (PZU) din România au avut preț negativ. Cum trebuie raportată cifra către conducere, astfel încît să fie comparabilă cu anii anteriori, cu intervale orare?",
                "options": [
                    "687 de ore cu preț negativ",
                    "687 de sferturi de oră (171,75 ore)",
                    "687 de sferturi de oră (2 748 de ore)",
                    "687 de sferturi de oră (57,25 ore)"
                ],
                "correctExplanation": "Fiecare sfert de oră contează 15/60 dintr-o oră: $H=687\\times 15/60=171{,}75$ ore echivalente. Raportul trebuie să precizeze unitatea și să dea ambele cifre.",
                "incorrectExplanation": "Dacă fiecare sfert de oră este numărat ca o oră, durata este supraevaluată de 4 ori, iar 2026 pare mult mai grav decît anii anteriori; înmulțirea cu 4 sau împărțirea la 12 înseamnă o conversie greșită."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Energy in one quarter-hour",
                "text": "In the lecture's example, a 10 megawatt (MW) baseload contract delivers 240 megawatt-hours (MWh) a day. Since October 2025 the market time unit (MTU) of the Romanian day-ahead market (PZU, Piața pentru Ziua Următoare) is 15 minutes, 96 per day. How much energy does this contract deliver in one MTU?",
                "options": [
                    "2.5 MWh",
                    "10 MWh",
                    "2.5 MW",
                    "24 MWh"
                ],
                "correctExplanation": "Energy is power times time: $10\\ \\text{MW}\\times 0.25\\ \\text{h}=2.5$ MWh, and $96\\times 2.5=240$ MWh a day, as in the lecture.",
                "incorrectExplanation": "A MW measures power and a MWh energy; a quarter-hour lasts 0.25 h, so the 10 MW must be multiplied by 0.25, not by 1 hour, and the daily 240 MWh is split into 96 intervals, not 10."
            },
            "ro": {
                "title": "Energia într-un sfert de oră",
                "text": "În exemplul din curs, un contract de 10 megawați (MW) în bandă înseamnă 240 de megawați-oră (MWh) livrați pe zi. Din octombrie 2025, intervalul de tranzacționare (MTU, market time unit) al Pieței pentru Ziua Următoare (PZU) din România este de 15 minute, 96 pe zi. Cîtă energie livrează acest contract într-un MTU?",
                "options": [
                    "2,5 MWh",
                    "10 MWh",
                    "2,5 MW",
                    "24 MWh"
                ],
                "correctExplanation": "Energia este putere înmulțită cu timpul: $10\\ \\text{MW}\\times 0{,}25\\ \\text{h}=2{,}5$ MWh, iar $96\\times 2{,}5=240$ MWh pe zi, ca în curs.",
                "incorrectExplanation": "MW măsoară puterea, iar MWh energia; un sfert de oră durează 0,25 h, deci cei 10 MW se înmulțesc cu 0,25, nu cu o oră întreagă, iar cei 240 MWh pe zi se împart la 96 de intervale, nu la 10."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "What drives grid capacity",
                "text": "On 28 October 2026 Romanian load ranged from 5,253 megawatts (MW) at 3:00 to 7,719 MW at 17:00 Central European Time (CET), and the day's energy was 159,558 megawatt-hours (MWh). Which number drives the capacity and network costs?",
                "options": [
                    "159,558 MWh, the energy consumed that day",
                    "6,648 MW, the mean load of the day",
                    "7,719 MW, the peak power of the day",
                    "5,253 MW, the minimum load that must always be served"
                ],
                "correctExplanation": "The grid must be able to carry the peak power, in MW, even if that level lasts only one hour; capacity and network costs are driven by the peak, not by the average.",
                "incorrectExplanation": "A supplier buys and sells energy in MWh, and 159,558 MWh is simply 24 hours times the mean load of 6,648 MW; but the network is sized for the highest power it must carry."
            },
            "ro": {
                "title": "Ce determină capacitatea rețelei",
                "text": "La 28 octombrie 2026, consumul României a variat între 5 253 de megawați (MW) la ora 3:00 și 7 719 MW la ora 17:00, ora Europei Centrale (CET), iar energia zilei a fost de 159 558 de megawați-oră (MWh). Ce cifră determină costurile de capacitate și de rețea?",
                "options": [
                    "159 558 MWh, energia consumată în acea zi",
                    "6 648 MW, puterea medie a zilei",
                    "7 719 MW, puterea de vîrf a zilei",
                    "5 253 MW, consumul minim care trebuie acoperit permanent"
                ],
                "correctExplanation": "Rețeaua trebuie să poată transporta puterea de vîrf, în MW, chiar dacă acest nivel durează doar o oră; costurile de capacitate și de rețea sînt determinate de vîrf, nu de medie.",
                "incorrectExplanation": "Un furnizor cumpără și vinde energie în MWh, iar 159 558 MWh înseamnă 24 de ore înmulțite cu puterea medie de 6 648 MW; rețeaua este însă dimensionată pentru cea mai mare putere pe care trebuie să o transporte."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Which clock defines a day",
                "text": "Raw timestamps from the European Network of Transmission System Operators for Electricity (ENTSO-E) are in Coordinated Universal Time (UTC). Why must daily price statistics be computed on the delivery day of the Single Day-Ahead Coupling (SDAC) instead?",
                "options": [
                    "Because UTC days have 25 hours on the last Sunday of October",
                    "Because the delivery day runs in Eastern European Time (EET), the Romanian clock",
                    "Because UTC timestamps are rounded to the nearest full hour",
                    "Because the delivery day runs in Central European Time (CET) or, in summer, Central European Summer Time (CEST), and a UTC day would put one or two hours into the wrong day"
                ],
                "correctExplanation": "The SDAC delivery day is defined in CET/CEST. The clock changes then create two irregular days: the last Sunday of March has 23 hours and the last Sunday of October 25, and daily means use the intervals that actually exist.",
                "incorrectExplanation": "UTC has no clock changes and is not rounded; the problem is that it is shifted against the CET/CEST delivery day, so one or two hours would land in the wrong day."
            },
            "ro": {
                "title": "Ce ceas definește ziua",
                "text": "Marcajele temporale din datele brute ale Rețelei europene a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E) sînt în timpul universal coordonat (UTC). De ce statisticile zilnice de preț trebuie calculate pe ziua de livrare din cuplarea unică a piețelor pentru ziua următoare (SDAC)?",
                "options": [
                    "Pentru că zilele UTC au 25 de ore în ultima duminică din octombrie",
                    "Pentru că ziua de livrare este definită în ora Europei de Est (EET), ora României",
                    "Pentru că marcajele UTC sînt rotunjite la ora întreagă cea mai apropiată",
                    "Pentru că ziua de livrare este definită în ora Europei Centrale (CET) sau, vara, în ora de vară a Europei Centrale (CEST), iar o zi UTC ar muta una sau două ore în ziua greșită"
                ],
                "correctExplanation": "Ziua de livrare din SDAC este definită în CET/CEST. Schimbarea orei creează două zile neregulate: ultima duminică din martie are 23 de ore, iar ultima duminică din octombrie 25, iar mediile zilnice se calculează pe intervalele care există efectiv.",
                "incorrectExplanation": "UTC nu are schimbări de oră și nu este rotunjit; problema este decalajul față de ziua de livrare definită în CET/CEST, din cauza căruia una sau două ore ar ajunge în ziua greșită."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Nuclear fall as lower bound",
                "text": "Romanian nuclear output in January–October 2026 was 31.3% lower than in the same months of 2025, compared on the hours reported in both years. Why does the lecture call this a lower bound for the true fall?",
                "options": [
                    "Because rooftop solar is consumed behind the meter and is not metered",
                    "Because September nuclear output was not reported, and those days are simply left out of the comparison",
                    "Because 2025, the base year, already had a long reactor outage",
                    "Because generation is converted from megawatts (MW) to terawatt-hours (TWh) with rounding"
                ],
                "correctExplanation": "Unit 1 of Cernavodă was shut at the end of July and Unit 2 on 13 August, because of the low Danube. The 29 September days without nuclear data are excluded, not filled, so the true fall is at least as large.",
                "incorrectExplanation": "Missing values stay missing and are never counted as zero; since the outage days with no data drop out of both years, the reported 31.3% can only understate the fall."
            },
            "ro": {
                "title": "Scăderea nucleară, limită inferioară",
                "text": "Producția nucleară a României în ianuarie–octombrie 2026 a fost cu 31,3% mai mică decît în aceleași luni din 2025, pe orele raportate în ambii ani. De ce cursul o numește o limită inferioară a scăderii reale?",
                "options": [
                    "Pentru că producția panourilor de pe acoperișuri este consumată direct de proprietari și nu este măsurată",
                    "Pentru că producția nucleară din septembrie nu a fost raportată, iar acele zile sînt pur și simplu excluse din comparație",
                    "Pentru că anul de bază 2025 avusese deja o oprire lungă a unui reactor",
                    "Pentru că producția este convertită din megawați (MW) în terawați-oră (TWh) cu rotunjiri"
                ],
                "correctExplanation": "Unitatea 1 de la Cernavodă a fost oprită la sfîrșitul lui iulie, iar unitatea 2 la 13 august, din cauza nivelului scăzut al Dunării. Cele 29 de zile din septembrie fără date nucleare sînt excluse, nu completate, deci scăderea reală este cel puțin la fel de mare.",
                "incorrectExplanation": "Valorile lipsă rămîn lipsă și nu devin zero; deoarece zilele de oprire fără date dispar din ambii ani, cifra de 31,3% nu poate decît să subestimeze scăderea."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Budgeting on old prices",
                "text": "The mean Romanian day-ahead price was 39.5 euro per megawatt-hour (EUR/MWh) in 2020 and 108.2 EUR/MWh in 2025. By roughly what factor would a 2025 energy budget built on 2020 prices be too low?",
                "options": [
                    "About 1.4",
                    "About 0.4",
                    "About 2.7",
                    "About 6.9"
                ],
                "correctExplanation": "$108.2/39.5\\approx 2.7$. The level shift of 2021–2022 is the first stylized fact: prices fell after 2022 but never returned to the old level.",
                "incorrectExplanation": "The ratio of the two means gives the factor; a model or budget estimated on pre-2021 data describes a market that no longer exists and is off by a factor of two to three."
            },
            "ro": {
                "title": "Bugetul pe prețuri vechi",
                "text": "Prețul mediu pentru ziua următoare din România a fost de 39,5 euro pe megawatt-oră (EUR/MWh) în 2020 și de 108,2 EUR/MWh în 2025. De aproximativ cîte ori ar fi prea mic un buget de energie pentru 2025 construit pe prețurile din 2020?",
                "options": [
                    "De circa 1,4 ori",
                    "De circa 0,4 ori",
                    "De circa 2,7 ori",
                    "De circa 6,9 ori"
                ],
                "correctExplanation": "$108{,}2/39{,}5\\approx 2{,}7$. Saltul de nivel din 2021–2022 este primul fapt stilizat: prețurile au scăzut după 2022, dar nu au mai revenit la vechiul nivel.",
                "incorrectExplanation": "Raportul celor două medii dă factorul; un model sau un buget estimat pe date de dinainte de 2021 descrie o piață care nu mai există și subestimează costurile de două-trei ori."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Volatility scales with level",
                "text": "The standard deviation of daily Romanian price changes was 8.6 euro per megawatt-hour (EUR/MWh) in 2020, at a mean price of 39.5, and 58.9 EUR/MWh in 2022, at a mean of 265.3. What is the right managerial reading?",
                "options": [
                    "Romania became structurally riskier per euro of price in 2022",
                    "Volatility in EUR/MWh moves with the price level, so collateral must scale with the price and the years are not directly comparable",
                    "The 2022 volatility came from spikes, since the spike rule flagged many hours that year",
                    "Volatility fell relative to 2020, since 58.9 is a small share of 265.3"
                ],
                "correctExplanation": "Mean and volatility move together: 8.6/39.5 and 58.9/265.3 are both close to 22%. A market at 200 EUR/MWh moves far more than one at 50, so collateral for day-ahead purchases must scale with the price.",
                "incorrectExplanation": "Relative to the price level, volatility barely changed; and 2022 had only 4 spike hours, because the whole year was high. A volatility in EUR/MWh is not comparable across very different price levels."
            },
            "ro": {
                "title": "Volatilitatea urmează nivelul",
                "text": "Abaterea standard a variațiilor zilnice ale prețului din România a fost de 8,6 euro pe megawatt-oră (EUR/MWh) în 2020, la un preț mediu de 39,5, și de 58,9 EUR/MWh în 2022, la o medie de 265,3. Care este interpretarea corectă pentru un manager?",
                "options": [
                    "România a devenit structural mai riscantă pe fiecare euro de preț în 2022",
                    "Volatilitatea în EUR/MWh crește odată cu nivelul prețului, deci garanțiile trebuie să crească odată cu prețul, iar anii nu sînt direct comparabili",
                    "Volatilitatea din 2022 a provenit din salturile de preț, deoarece regula de identificare a marcat multe ore în acel an",
                    "Volatilitatea a scăzut față de 2020, deoarece 58,9 este o pondere mică din 265,3"
                ],
                "correctExplanation": "Media și volatilitatea evoluează împreună: 8,6/39,5 și 58,9/265,3 sînt ambele în jur de 22%. La 200 EUR/MWh piața fluctuează mult mai mult decît la 50, deci garanțiile pentru PZU (Piața pentru Ziua Următoare) cresc odată cu prețul.",
                "incorrectExplanation": "Raportată la nivelul prețului, volatilitatea aproape nu s-a schimbat; iar 2022 a avut doar 4 ore cu salturi de preț, pentru că întregul an a fost scump. O volatilitate în EUR/MWh nu este comparabilă între niveluri de preț foarte diferite."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The duck curve",
                "text": "In 2025 the cheapest Romanian hour of the day was 13:00, at 58.8 euro per megawatt-hour (EUR/MWh), while the evening peak reached 182.5 EUR/MWh; the evening-to-midday ratio rose from 1.30 in 2019 to 3.11. What drives this change?",
                "options": [
                    "Lower industrial demand at midday since 2019",
                    "Higher gas prices that affect only the evening hours",
                    "The move to a 15-minute market time unit (MTU)",
                    "Solar generation filling the middle of the day and lowering the net demand left for other plants"
                ],
                "correctExplanation": "This is the duck curve: solar pushes the midday price down while the evening, when the sun sets and households consume, stays expensive. In 2019 the cheapest hours were still at night.",
                "incorrectExplanation": "The shift of the cheapest hour from night to 13:00 follows solar output, not demand or market design; the intraday profile changes as solar capacity grows, and this spread is what a battery earns."
            },
            "ro": {
                "title": "Curba în formă de rață",
                "text": "În 2025, ora cu prețul minim din România era 13:00, cu 58,8 euro pe megawatt-oră (EUR/MWh), în timp ce vîrful de seară ajungea la 182,5 EUR/MWh; raportul dintre prețul de seară și cel de la amiază a urcat de la 1,30 în 2019 la 3,11. Ce determină această schimbare?",
                "options": [
                    "Scăderea cererii industriale la amiază după 2019",
                    "Prețurile mai mari ale gazelor, care afectează numai orele de seară",
                    "Trecerea la intervalul de tranzacționare (MTU) de 15 minute",
                    "Producția solară, care acoperă mijlocul zilei și reduce cererea rămasă pentru celelalte centrale"
                ],
                "correctExplanation": "Este „curba în formă de rață”: producția solară coboară prețul de la amiază, în timp ce seara, cînd apune soarele și crește consumul casnic, rămîne scumpă. În 2019, orele cele mai ieftine erau încă noaptea.",
                "incorrectExplanation": "Mutarea orei celei mai ieftine de noaptea la 13:00 urmează producția solară, nu cererea sau designul pieței; profilul intrazilnic se modifică pe măsură ce crește capacitatea solară, iar această diferență este venitul unei baterii."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Tuesday against Sunday",
                "text": "On 199 weeks, from 2 January 2023 to 25 October 2026, a Romanian Tuesday on the day-ahead market (PZU, Piața pentru Ziua Următoare) was on average 12.7 euro per megawatt-hour (EUR/MWh) above the mean of its week, and a Sunday 30.7 EUR/MWh below. What is the average price gap between a Tuesday and the Sunday of the same week?",
                "options": [
                    "About 43.4 EUR/MWh",
                    "About 18.0 EUR/MWh",
                    "About 30.7 EUR/MWh",
                    "About 12.7 EUR/MWh"
                ],
                "correctExplanation": "Both values are distances from the same weekly mean, so the gap is $12.7-(-30.7)=43.4$ EUR/MWh. This is the value of moving flexible consumption from a working day to the weekend.",
                "incorrectExplanation": "The two profile values have opposite signs around the same weekly mean, so they add up in absolute value; 18.0 subtracts them as if both were on the same side, and either value alone ignores the other day."
            },
            "ro": {
                "title": "Marți față de duminică",
                "text": "Pe 199 de săptămîni, între 2 ianuarie 2023 și 25 octombrie 2026, o zi de marți pe Piața pentru Ziua Următoare (PZU) din România a fost în medie cu 12,7 euro pe megawatt-oră (EUR/MWh) peste media săptămînii sale, iar o duminică cu 30,7 EUR/MWh sub ea. Care este diferența medie de preț dintre o zi de marți și duminica aceleiași săptămîni?",
                "options": [
                    "Circa 43,4 EUR/MWh",
                    "Circa 18,0 EUR/MWh",
                    "Circa 30,7 EUR/MWh",
                    "Circa 12,7 EUR/MWh"
                ],
                "correctExplanation": "Ambele valori sînt abateri de la aceeași medie săptămînală, deci diferența este $12{,}7-(-30{,}7)=43{,}4$ EUR/MWh. Aceasta este valoarea mutării consumului flexibil dintr-o zi lucrătoare în weekend.",
                "incorrectExplanation": "Cele două valori ale profilului au semne opuse față de aceeași medie, deci se adună în valoare absolută; 18,0 le scade ca și cum ar fi de aceeași parte a mediei, iar o singură valoare ignoră cealaltă zi."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Spring is cheap",
                "text": "Relative to the annual mean, the Romanian day-ahead price is highest in January (1.26 times the mean) and lowest in April (0.72 times), while hydro output peaks in June with the snow melt. How does a reservoir hydro producer use this pattern?",
                "options": [
                    "It releases as much water as possible in spring, when inflows are highest",
                    "It ignores the pattern, since monthly differences are random shocks",
                    "It saves reservoir water in spring, when power is cheap, to sell it in winter and late summer",
                    "It sells its spring output forward at the January price level"
                ],
                "correctExplanation": "Reservoir hydro bids its water value, the price it expects later for the same water; with spring prices at 0.72 of the mean and January at 1.26, keeping water for expensive months pays.",
                "incorrectExplanation": "The annual profile is a regular seasonal pattern, not a shock, and forward prices for spring reflect the cheap spring months; the reservoir lets the producer move output to the expensive months."
            },
            "ro": {
                "title": "Primăvara, energie ieftină",
                "text": "Raportat la media anuală, prețul pentru ziua următoare din România este maxim în ianuarie (de 1,26 ori media) și minim în aprilie (de 0,72 ori), iar producția hidro atinge maximul în iunie, odată cu topirea zăpezii. Cum folosește acest tipar un producător hidro cu lac de acumulare?",
                "options": [
                    "Turbinează cît mai multă apă primăvara, cînd afluxul este maxim",
                    "Ignoră tiparul, deoarece diferențele lunare sînt șocuri aleatoare",
                    "Economisește apa din lacuri primăvara, cînd energia este ieftină, pentru a o turbina iarna și la sfîrșitul verii",
                    "Își vinde la termen producția de primăvară la nivelul prețului din ianuarie"
                ],
                "correctExplanation": "Hidrocentralele cu lac ofertează la valoarea apei, prețul pe care se așteaptă să-l obțină mai tîrziu pentru aceeași apă; cu primăvara la 0,72 din medie și ianuarie la 1,26, păstrarea apei pentru lunile scumpe este rentabilă.",
                "incorrectExplanation": "Profilul anual este un tipar sezonier regulat, nu un șoc, iar prețurile la termen pentru primăvară reflectă lunile ieftine; lacul îi permite producătorului să mute producția în lunile scumpe."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Few spikes in 2022",
                "text": "An interval of year $y$ is flagged as a spike when $p_t \\gt Q_{3,y}+3\\,(Q_{3,y}-Q_{1,y})$, where $Q_{3,y}-Q_{1,y}$ is the interquartile range (IQR). In 2022, a year of record prices, Romania had only 4 spike hours (threshold 873 euro per megawatt-hour, EUR/MWh), against 276 in 2024 (threshold 274). Why?",
                "options": [
                    "Price caps prevented spikes from forming in 2022",
                    "The threshold moves with each year's distribution, and in 2022 the whole year was high",
                    "The rule measures spikes in percent, and percentage moves were small in 2022",
                    "Prices were hourly in 2022, so spikes were averaged away"
                ],
                "correctExplanation": "The threshold is built from the year's own quartiles, which are robust, so it rose to 873 EUR/MWh in 2022. A spike is a price far above what is normal for that year, and in 2022 high prices were normal.",
                "incorrectExplanation": "The rule is in EUR/MWh and relative to each year's quartiles; record prices that last all year raise the threshold, so few intervals exceed it, while 2024 had a lower threshold and many extreme evenings."
            },
            "ro": {
                "title": "Puține salturi în 2022",
                "text": "Un interval din anul $y$ este marcat ca salt de preț atunci cînd $p_t \\gt Q_{3,y}+3\\,(Q_{3,y}-Q_{1,y})$, unde $Q_{3,y}-Q_{1,y}$ este abaterea intercuartilică (IQR). În 2022, an cu prețuri record, România a avut doar 4 ore cu salturi de preț (prag de 873 euro pe megawatt-oră, EUR/MWh), față de 276 în 2024 (prag de 274). De ce?",
                "options": [
                    "Plafoanele de preț au împiedicat apariția salturilor în 2022",
                    "Pragul urmează distribuția fiecărui an, iar în 2022 întregul an a fost scump",
                    "Regula măsoară salturile în procente, iar variațiile procentuale au fost mici în 2022",
                    "În 2022 prețurile erau orare, deci salturile s-au pierdut prin mediere"
                ],
                "correctExplanation": "Pragul este construit din cuartilele anului respectiv, care sînt robuste, deci a urcat la 873 EUR/MWh în 2022. Un salt de preț înseamnă un preț mult peste nivelul obișnuit al anului, iar în 2022 prețurile mari erau obișnuite.",
                "incorrectExplanation": "Regula este exprimată în EUR/MWh și raportată la cuartilele fiecărui an; prețurile record care durează tot anul ridică pragul, deci puține intervale îl depășesc, în timp ce 2024 a avut un prag mai mic și multe seri extreme."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "When prices turn negative",
                "text": "The first negative Romanian day-ahead price occurred on 21 May 2023. Since 2024, how are negative-price hours distributed over the day and the week?",
                "options": [
                    "Mostly at night, between 00:00 and 06:00, when demand is lowest",
                    "Evenly over the day, with no pattern across the week",
                    "Mostly on weekday evenings, when wind output is highest",
                    "91.1% between 10:00 and 16:00, and 83.9% on weekends"
                ],
                "correctExplanation": "Negative prices fall in the hours when solar output is highest and demand is lowest: around midday and on weekends.",
                "incorrectExplanation": "In Romania the driver is solar, not night-time wind: inflexible output and solar exceed demand at midday, especially on weekends, when factories and offices consume less."
            },
            "ro": {
                "title": "Cînd prețurile devin negative",
                "text": "Primul preț negativ pentru ziua următoare din România a apărut la 21 mai 2023. Din 2024, cum se distribuie orele cu preț negativ în cursul zilei și al săptămînii?",
                "options": [
                    "Mai ales noaptea, între 00:00 și 06:00, cînd cererea este minimă",
                    "Uniform în cursul zilei, fără un tipar săptămînal",
                    "Mai ales în serile zilelor lucrătoare, cînd producția eoliană este maximă",
                    "91,1% între 10:00 și 16:00, iar 83,9% în weekend"
                ],
                "correctExplanation": "Prețurile negative cad în orele în care producția solară este maximă, iar cererea minimă: în jurul amiezii și în weekend.",
                "incorrectExplanation": "În România factorul determinant este solarul, nu vîntul de noapte: producția inflexibilă și cea solară depășesc cererea la amiază, mai ales în weekend, cînd fabricile și birourile consumă mai puțin."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Why asinh, not logs",
                "text": "In January–October 2026, 1,189 of 29,184 Romanian quarter-hours had a price of zero or below, 502 of them exactly 0. Why does the lecture transform prices with $\\operatorname{asinh}$ rather than with logarithms?",
                "options": [
                    "Asinh is defined for zero and negative prices and behaves like a logarithm in both tails",
                    "Asinh removes the weekly and annual seasonality of prices",
                    "Asinh turns prices into percentage changes that are easier to report",
                    "Logarithms would make the distribution symmetric and hide the spikes"
                ],
                "correctExplanation": "With $x_t=(p_t-\\tilde p)/\\widehat{\\mathrm{MAD}}$, where MAD is the median absolute deviation, $\\operatorname{asinh}(x)$ accepts any sign, is almost linear near zero and behaves like $\\ln(2|x|)$ in the tails. The skewness falls from 1.19 to 0.13.",
                "incorrectExplanation": "Logarithms and percentage changes need a positive price, so they fail precisely in the zero and negative hours that matter most for solar and storage; asinh keeps those hours and does not remove seasonality."
            },
            "ro": {
                "title": "De ce asinh, nu logaritm",
                "text": "În ianuarie–octombrie 2026, 1 189 din cele 29 184 de sferturi de oră din România au avut un preț nul sau negativ, dintre care 502 un preț exact 0. De ce cursul transformă prețurile cu $\\operatorname{asinh}$ și nu cu logaritmul?",
                "options": [
                    "Funcția asinh este definită pentru prețuri nule și negative și se comportă ca un logaritm în ambele cozi",
                    "Funcția asinh elimină sezonalitatea săptămînală și anuală a prețurilor",
                    "Funcția asinh transformă prețurile în variații procentuale, mai ușor de raportat",
                    "Logaritmul ar face distribuția simetrică și ar ascunde salturile de preț"
                ],
                "correctExplanation": "Cu $x_t=(p_t-\\tilde p)/\\widehat{\\mathrm{MAD}}$, unde MAD este abaterea absolută mediană, $\\operatorname{asinh}(x)$ acceptă orice semn, este aproape liniară în jurul lui zero și se comportă ca $\\ln(2|x|)$ în cozi. Asimetria scade de la 1,19 la 0,13.",
                "incorrectExplanation": "Logaritmii și variațiile procentuale presupun un preț pozitiv, deci eșuează tocmai în orele cu preț nul sau negativ, cele mai importante pentru producția solară și pentru stocare; asinh păstrează aceste ore și nu elimină sezonalitatea."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Four-sigma oil days",
                "text": "For Brent daily log returns from January 2015 to October 2026, without the 141 contract-roll days, a normal distribution predicts 0.18 moves beyond 4 standard deviations in the sample. How many were observed, and what does it imply?",
                "options": [
                    "About 1, which is consistent with normality",
                    "4, a small excess that a normal fit absorbs",
                    "16, a sign of fat tails; the excess kurtosis is 13.98",
                    "16, which is consistent with the normal curve once roll days are removed"
                ],
                "correctExplanation": "16 observed against 0.18 expected, with an excess kurtosis of 13.98 against 0 for the normal: extreme oil days are far more frequent than a bell curve allows, and a Student-$t$ density fits much better.",
                "incorrectExplanation": "The roll days were already removed; the gap between 16 observed and 0.18 expected is the fat-tail evidence, and a fuel-budget limit built on the normal curve understates how often a crisis day comes."
            },
            "ro": {
                "title": "Zilele de patru sigma",
                "text": "Pentru randamentele logaritmice zilnice ale țițeiului Brent, din ianuarie 2015 pînă în octombrie 2026, fără cele 141 de zile de schimbare a contractului, distribuția normală prevede 0,18 variații de peste 4 abateri standard în eșantion. Cîte au fost observate și ce înseamnă aceasta?",
                "options": [
                    "Circa 1, ceea ce este compatibil cu distribuția normală",
                    "4, un exces mic pe care o distribuție normală îl poate absorbi",
                    "16, semn de cozi groase; excesul de aplatizare este 13,98",
                    "16, ceea ce este compatibil cu distribuția normală după eliminarea zilelor de schimbare a contractului"
                ],
                "correctExplanation": "16 observate, față de 0,18 așteptate, cu un exces de aplatizare de 13,98, față de 0 pentru distribuția normală: zilele extreme pe piața țițeiului sînt mult mai frecvente decît permite clopotul lui Gauss, iar o densitate Student-$t$ se potrivește mult mai bine.",
                "incorrectExplanation": "Zilele de schimbare a contractului fuseseră deja eliminate; diferența dintre 16 observate și 0,18 așteptate este dovada cozilor groase, iar o limită de buget pentru combustibil calculată cu legea normală subestimează frecvența zilelor de criză."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Ljung–Box on oil returns",
                "text": "For Brent with $m=10$ lags, the Ljung–Box statistic is 28.1 for the daily returns $r$ and 506.9 for the squared returns $r^2$, against a 5% critical value of 18.31. What is the main message?",
                "options": [
                    "Returns are predictable in direction, so a trend-following rule pays",
                    "There is little memory in the direction of moves and a lot in their size: volatility clusters",
                    "Neither series is autocorrelated, since both statistics follow a chi-squared law",
                    "Squared returns are non-stationary, so the test is not valid for them"
                ],
                "correctExplanation": "Both statistics exceed 18.31, but 506.9 is far larger than 28.1: big moves are followed by big moves of either sign. This volatility clustering is what the models of Lecture 3 describe.",
                "incorrectExplanation": "The chi-squared law holds only under no autocorrelation, and both statistics reject it; the difference in size says that the direction of moves is hard to predict while their size is persistent."
            },
            "ro": {
                "title": "Ljung–Box pe randamentele țițeiului",
                "text": "Pentru Brent, cu $m=10$ decalaje, statistica Ljung–Box este 28,1 pentru randamentele zilnice $r$ și 506,9 pentru pătratele lor $r^2$, față de o valoare critică de 18,31 la pragul de 5%. Care este mesajul principal?",
                "options": [
                    "Sensul randamentelor este previzibil, deci o regulă care urmează trendul este profitabilă",
                    "Dependența temporală este slabă pentru sensul variațiilor și puternică pentru mărimea lor: volatilitatea este grupată",
                    "Niciuna dintre serii nu are autocorelație, deoarece ambele statistici urmează o distribuție hi-pătrat",
                    "Pătratele randamentelor sînt nestaționare, deci testul nu este valid pentru ele"
                ],
                "correctExplanation": "Ambele statistici depășesc 18,31, dar 506,9 este mult mai mare decît 28,1: variațiile mari sînt urmate de variații mari, de orice semn. Această grupare a volatilității este descrisă de modelele din cursul 3.",
                "incorrectExplanation": "Distribuția hi-pătrat este valabilă numai în absența autocorelației, iar ambele statistici o resping; diferența de mărime arată că sensul variațiilor este greu de anticipat, în timp ce mărimea lor persistă."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Persistent is not noise",
                "text": "An analyst reports that the price on the day-ahead market (PZU, Piața pentru Ziua Următoare) has an autocorrelation of 0.98 at lag 1 and 0.90 at lag 30, and concludes that prices are white noise, so last month tells us nothing. What do you answer?",
                "options": [
                    "Correct: such high autocorrelations mean the series is erratic",
                    "Correct, provided the values lie inside the band $\\pm1.96/\\sqrt T$",
                    "Wrong: values near 1 at lag 30 show monthly seasonality, to be removed with monthly dummies",
                    "Wrong: values near 1 indicate strong persistence; run the augmented Dickey–Fuller (ADF) and Kwiatkowski–Phillips–Schmidt–Shin (KPSS) tests"
                ],
                "correctExplanation": "White noise has autocorrelations near 0. Values near 1 that decay slowly point to a unit root or very slow mean reversion, so the ADF and KPSS tests and the autocorrelation of daily changes should be checked.",
                "incorrectExplanation": "A random walk looks erratic but its level autocorrelation is close to 1, because every value contains all past shocks; 0.98 is far outside any white-noise band, and a slow decay is persistence, not seasonality."
            },
            "ro": {
                "title": "Persistența nu este zgomot",
                "text": "Un analist raportează că prețul de pe Piața pentru Ziua Următoare (PZU) are o autocorelație de 0,98 la decalajul 1 și de 0,90 la decalajul 30 și conchide că prețurile sînt zgomot alb, deci luna trecută nu ne spune nimic. Ce îi răspundeți?",
                "options": [
                    "Are dreptate: autocorelații atît de mari înseamnă că seria este haotică",
                    "Are dreptate, dacă valorile se află în banda $\\pm1{,}96/\\sqrt T$",
                    "Nu are dreptate: valorile apropiate de 1 la decalajul 30 arată o sezonalitate lunară, care se elimină cu variabile lunare",
                    "Nu are dreptate: valorile apropiate de 1 indică o persistență puternică; aplicați testul Dickey–Fuller augmentat (ADF) și testul Kwiatkowski–Phillips–Schmidt–Shin (KPSS)"
                ],
                "correctExplanation": "Zgomotul alb are autocorelații apropiate de 0. Valorile apropiate de 1, care scad lent, indică o rădăcină unitară sau o revenire foarte lentă la medie, deci trebuie aplicate testele ADF și KPSS și examinată autocorelația variațiilor zilnice.",
                "incorrectExplanation": "Mersul aleator pare haotic, dar autocorelația nivelului său este apropiată de 1, deoarece fiecare valoare conține toate șocurile trecute; 0,98 este mult în afara benzii pentru zgomot alb, iar o scădere lentă înseamnă persistență, nu sezonalitate."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Same weekday last week",
                "text": "For Romanian daily base prices from 2023 to October 2026, the autocorrelations are $\\hat\\rho_1=0.789$ and $\\hat\\rho_7=0.672$, and the partial autocorrelation at lag 7 is $\\hat\\alpha_7=0.257$. What does the partial value add?",
                "options": [
                    "The same weekday of the previous week carries information beyond that of the last few days",
                    "Lag 7 becomes irrelevant once lag 1 is in the model",
                    "Prices behave like white noise beyond lag 1",
                    "The weekly effect is stronger than the daily one, since 0.672 exceeds 0.257"
                ],
                "correctExplanation": "The partial autocorrelation function (PACF) measures memory at lag $k$ net of the shorter lags; a value of 0.257 at lag 7 means the same weekday last week matters even after yesterday is known.",
                "incorrectExplanation": "A positive partial value at lag 7 means lag 7 is not made redundant by the shorter lags; comparing an autocorrelation with a partial autocorrelation mixes two different measures."
            },
            "ro": {
                "title": "Aceeași zi, săptămîna trecută",
                "text": "Pentru prețurile zilnice în bandă din România, din 2023 pînă în octombrie 2026, autocorelațiile sînt $\\hat\\rho_1=0{,}789$ și $\\hat\\rho_7=0{,}672$, iar autocorelația parțială la decalajul 7 este $\\hat\\alpha_7=0{,}257$. Ce adaugă valoarea parțială?",
                "options": [
                    "Aceeași zi din săptămîna precedentă aduce informație în plus față de ultimele zile",
                    "Decalajul 7 devine irelevant odată ce decalajul 1 este inclus în model",
                    "După decalajul 1, prețurile se comportă ca un zgomot alb",
                    "Efectul săptămînal este mai puternic decît cel zilnic, deoarece 0,672 depășește 0,257"
                ],
                "correctExplanation": "Funcția de autocorelație parțială (PACF) măsoară memoria la decalajul $k$ după eliminarea efectului decalajelor mai mici; o valoare de 0,257 la decalajul 7 arată că aceeași zi din săptămîna trecută contează chiar și după ce ziua de ieri este cunoscută.",
                "incorrectExplanation": "O valoare parțială pozitivă la decalajul 7 arată că acesta nu devine redundant în prezența decalajelor mai mici; compararea unei autocorelații cu o autocorelație parțială amestecă două măsuri diferite."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Naive forecast for Monday",
                "text": "The naive benchmark forecasts tomorrow's day-ahead price for each hour. Which price does it use to forecast Monday at 10:00?",
                "options": [
                    "Sunday's price at 10:00, the previous day",
                    "The average of Friday, Saturday and Sunday at 10:00",
                    "The price at 10:00 on Monday of the previous week",
                    "Friday's price at 10:00, the last working day"
                ],
                "correctExplanation": "The rule uses $p_{d-1,h}$ for Tuesday to Friday and $p_{d-7,h}$ for Monday, Saturday and Sunday, so that a weekend day is never used to forecast a working day.",
                "incorrectExplanation": "After a weekend, yesterday's price reflects low weekend demand; the naive rule therefore takes the same hour of the same weekday one week earlier for Monday, Saturday and Sunday."
            },
            "ro": {
                "title": "Prognoza naivă pentru luni",
                "text": "Prognoza naivă estimează prețul de mîine pentru ziua următoare, pentru fiecare oră. Ce preț folosește pentru a prognoza ziua de luni, ora 10:00?",
                "options": [
                    "Prețul de duminică, ora 10:00, adică ziua precedentă",
                    "Media prețurilor de vineri, sîmbătă și duminică, ora 10:00",
                    "Prețul de luni din săptămîna precedentă, ora 10:00",
                    "Prețul de vineri, ora 10:00, ultima zi lucrătoare"
                ],
                "correctExplanation": "Regula folosește $p_{d-1,h}$ de marți pînă vineri și $p_{d-7,h}$ luni, sîmbătă și duminică, astfel încît o zi de weekend nu este folosită niciodată pentru a prognoza o zi lucrătoare.",
                "incorrectExplanation": "După un weekend, prețul de ieri reflectă cererea scăzută din weekend; de aceea regula naivă ia, luni, sîmbătă și duminică, aceeași oră din aceeași zi a săptămînii precedente."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Naive rule against yesterday",
                "text": "For Romanian hourly prices in 2025, the naive forecast had a mean absolute error (MAE) of 22.9 euro per megawatt-hour (EUR/MWh), the previous-day lag (day d−1) 24.9 and the same-day-last-week lag (day d−7) 28.2. By how much, in relative terms, does the naive rule reduce the MAE of the previous-day lag?",
                "options": [
                    "About 2.0%",
                    "About 8.0%",
                    "About 8.7%",
                    "About 18.8%"
                ],
                "correctExplanation": "$(24.9-22.9)/24.9=2.0/24.9\\approx 8.0\\%$. Combining the two lags, yesterday on Tuesday–Friday and last week on Monday and the weekend, beats each lag used alone.",
                "incorrectExplanation": "The reduction is measured relative to the error being reduced, the 24.9 of the d−1 lag; dividing by 22.9 gives 8.7%, 18.8% is the comparison with the d−7 lag, and 2.0 is the gap in EUR/MWh, not a percentage."
            },
            "ro": {
                "title": "Regula naivă față de ziua precedentă",
                "text": "Pentru prețurile orare din România în 2025, prognoza naivă a avut o eroare absolută medie (MAE) de 22,9 euro pe megawatt-oră (EUR/MWh), decalajul de o zi (ziua d−1) 24,9, iar decalajul de o săptămînă (ziua d−7) 28,2. Cu cît reduce, relativ, regula naivă MAE a decalajului de o zi?",
                "options": [
                    "Circa 2,0%",
                    "Circa 8,0%",
                    "Circa 8,7%",
                    "Circa 18,8%"
                ],
                "correctExplanation": "$(24{,}9-22{,}9)/24{,}9=2{,}0/24{,}9\\approx 8{,}0\\%$. Combinarea celor două decalaje, ziua precedentă de marți pînă vineri și săptămîna trecută luni și în weekend, este mai bună decît fiecare decalaj folosit singur.",
                "incorrectExplanation": "Reducerea se raportează la eroarea care scade, cei 24,9 ai decalajului d−1; împărțirea la 22,9 dă 8,7%, 18,8% este comparația cu decalajul d−7, iar 2,0 este diferența în EUR/MWh, nu un procent."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Unit-root verdict for Romania",
                "text": "On Romanian daily price levels (2015–2026), the augmented Dickey–Fuller (ADF) test gives $p=0.073$ and the Kwiatkowski–Phillips–Schmidt–Shin (KPSS) statistic is 3.645, with $p$ below 0.01. What is the verdict at the 5% level?",
                "options": [
                    "Stationary: ADF rejects a unit root and KPSS keeps stationarity",
                    "Conflict: both tests reject their null hypotheses",
                    "Inconclusive: neither test rejects its null hypothesis",
                    "Consistent with a unit root: ADF does not reject a unit root and KPSS rejects stationarity"
                ],
                "correctExplanation": "ADF has a unit root as null and keeps it ($p=0.073$); KPSS has stationarity as null and rejects it (3.645 above 0.463). This is consistent with a unit root, not a proof; the daily changes are stationary.",
                "incorrectExplanation": "The two tests have opposite nulls: ADF tests for a unit root, KPSS for stationarity. Here only KPSS rejects; ADF has low power against slow mean reversion, and the 2022 level break pushes it towards a unit root."
            },
            "ro": {
                "title": "Verdictul de rădăcină unitară",
                "text": "Pe nivelurile zilnice ale prețului din România (2015–2026), testul Dickey–Fuller augmentat (ADF) dă $p=0{,}073$, iar statistica Kwiatkowski–Phillips–Schmidt–Shin (KPSS) este 3,645, cu $p$ sub 0,01. Care este verdictul la pragul de 5%?",
                "options": [
                    "Staționară: ADF respinge rădăcina unitară, iar KPSS nu respinge staționaritatea",
                    "Conflict: ambele teste își resping ipoteza nulă",
                    "Neconcludent: niciun test nu își respinge ipoteza nulă",
                    "Compatibil cu o rădăcină unitară: ADF nu respinge rădăcina unitară, iar KPSS respinge staționaritatea"
                ],
                "correctExplanation": "ADF are ca ipoteză nulă rădăcina unitară și nu o respinge ($p=0{,}073$); KPSS are ca ipoteză nulă staționaritatea și o respinge (3,645, peste 0,463). Rezultatul este compatibil cu o rădăcină unitară, dar nu este o dovadă; variațiile zilnice sînt staționare.",
                "incorrectExplanation": "Cele două teste au ipoteze nule opuse: ADF testează rădăcina unitară, KPSS staționaritatea. Aici respinge numai KPSS; ADF are putere redusă în cazul revenirii lente la medie, iar ruptura de nivel din 2022 favorizează nerespingerea rădăcinii unitare."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Classical versus STL",
                "text": "Romanian monthly mean load (2016–2025) is decomposed as $x_t=T_t+S_t+R_t$, both by the classical method and by Seasonal–Trend decomposition using Loess (STL). What does STL show that the classical method cannot?",
                "options": [
                    "That the seasonal amplitude shrank from 1.52 to 1.27 gigawatts (GW) over the decade",
                    "That load is about 0.69 gigawatts (GW) above the trend in January and February",
                    "That the trend is a centred 13-month moving average with half weights at the ends",
                    "That the remainder is white noise by construction"
                ],
                "correctExplanation": "The classical method keeps the seasonal pattern fixed, while STL lets it evolve over time; this is how it shows the amplitude shrinking from 1.52 to 1.27 GW.",
                "incorrectExplanation": "Fixed seasonal indices such as +0.69 GW in winter and the centred moving-average trend are what the classical method itself delivers; neither method guarantees a white-noise remainder."
            },
            "ro": {
                "title": "Metoda clasică și STL",
                "text": "Consumul mediu lunar al României (2016–2025) este descompus ca $x_t=T_t+S_t+R_t$, atît prin metoda clasică, cît și prin descompunerea sezonieră și de trend prin regresie locală (STL). Ce arată STL și nu poate arăta metoda clasică?",
                "options": [
                    "Că amplitudinea sezonieră s-a redus de la 1,52 la 1,27 gigawați (GW) în acest deceniu",
                    "Că în ianuarie și februarie consumul este cu circa 0,69 gigawați (GW) peste trend",
                    "Că trendul este o medie mobilă centrată pe 13 luni, cu ponderi pe jumătate la capete",
                    "Că componenta reziduală este, prin construcție, un zgomot alb"
                ],
                "correctExplanation": "Metoda clasică presupune o componentă sezonieră constantă, în timp ce STL îi permite să varieze în timp; așa se vede reducerea amplitudinii de la 1,52 la 1,27 GW.",
                "incorrectExplanation": "Indicii sezonieri constanți, de exemplu +0,69 GW iarna, și trendul prin medie mobilă centrată sînt chiar rezultatele metodei clasice; niciuna dintre metode nu garantează o componentă reziduală de tip zgomot alb."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Smoothing weight on Brent",
                "text": "On Brent (2024–2026), an exponentially weighted moving average (EWMA) with a 10-day half-life uses $\\alpha=1-2^{-1/10}=0.067$, while simple exponential smoothing (SES), with $\\alpha$ chosen to minimise one-step forecast errors, picks 0.948. How should a manager read this?",
                "options": [
                    "Brent has a long memory, so old prices should receive most of the weight",
                    "The EWMA is the better one-day forecast, because it is smoother",
                    "Almost all weight goes to the last price, as expected for a series close to a random walk; the EWMA is a good contract reference, not a forecast",
                    "A weight of 0.948 means that Brent is strongly mean-reverting"
                ],
                "correctExplanation": "In $\\ell_t=\\alpha x_t+(1-\\alpha)\\ell_{t-1}$, $\\alpha=0.948$ puts almost everything on today's price: for a near random walk the best forecast is close to the last value.",
                "incorrectExplanation": "A large $\\alpha$ means short memory, not long memory or mean reversion; the smooth EWMA is useful as a reference price in contracts but forecasts poorly one day ahead."
            },
            "ro": {
                "title": "Ponderea de netezire pentru Brent",
                "text": "Pe prețul Brent (2024–2026), o medie mobilă ponderată exponențial (EWMA) cu timp de înjumătățire de 10 zile folosește $\\alpha=1-2^{-1/10}=0{,}067$, în timp ce netezirea exponențială simplă (SES), cu $\\alpha$ ales astfel încît să minimizeze erorile de prognoză pentru ziua următoare, alege 0,948. Cum trebuie să interpreteze un manager aceste valori?",
                "options": [
                    "Brent are memorie lungă, deci prețurile vechi trebuie să primească cea mai mare pondere",
                    "EWMA este prognoza mai bună pentru ziua următoare, deoarece este mai netedă",
                    "Aproape toată ponderea revine ultimului preț, cum ne așteptăm pentru o serie apropiată de un mers aleator; EWMA este un bun preț de referință în contracte, nu o prognoză",
                    "O pondere de 0,948 înseamnă că prețul Brent revine puternic la medie"
                ],
                "correctExplanation": "În $\\ell_t=\\alpha x_t+(1-\\alpha)\\ell_{t-1}$, $\\alpha=0{,}948$ pune aproape toată ponderea pe prețul de azi: pentru o serie apropiată de un mers aleator, cea mai bună prognoză este apropiată de ultima valoare.",
                "incorrectExplanation": "Un $\\alpha$ mare înseamnă memorie scurtă, nu memorie lungă sau revenire la medie; EWMA, fiind netedă, este utilă ca preț de referință în contracte, dar este o prognoză slabă pentru ziua următoare."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Hydro: wet versus dry year",
                "text": "Romanian hydro output was 18.34 terawatt-hours (TWh) in wet 2023 and 12.15 TWh in dry 2025, while the 2015–2025 mean was 15.85 TWh. By how much did 2025 fall relative to 2023?",
                "options": [
                    "−23.3%",
                    "−33.8%",
                    "−50.9%",
                    "−6.19%"
                ],
                "correctExplanation": "$(12.15-18.34)/18.34\\approx-33.8\\%$, about a third below the wet year.",
                "incorrectExplanation": "The change must be divided by the 2023 base: −23.3% is the gap of 2025 to the long-run mean, dividing by 2025 gives 50.9%, and 6.19 is the fall in TWh, not in percent."
            },
            "ro": {
                "title": "Hidro: an ploios și an secetos",
                "text": "Producția hidro a României a fost de 18,34 terawați-oră (TWh) în anul ploios 2023 și de 12,15 TWh în anul secetos 2025, iar media 2015–2025 a fost de 15,85 TWh. Cu cît a scăzut producția din 2025 față de 2023?",
                "options": [
                    "−23,3%",
                    "−33,8%",
                    "−50,9%",
                    "−6,19%"
                ],
                "correctExplanation": "$(12{,}15-18{,}34)/18{,}34\\approx-33{,}8\\%$, adică aproximativ o treime sub anul ploios.",
                "incorrectExplanation": "Variația trebuie împărțită la baza din 2023: −23,3% este abaterea anului 2025 față de media multianuală, împărțirea la 2025 dă 50,9%, iar 6,19 este scăderea în TWh, nu în procente."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Hydro–price regression",
                "text": "On monthly data 2015–2025, the model $p_m=\\beta_0+\\beta_1\\,\\mathrm{Hydro}_m+\\beta_2\\,\\mathrm{TTF}_m+u_m$, with the price in euro per megawatt-hour (EUR/MWh), hydro in terawatt-hours (TWh) and TTF the Title Transfer Facility (Dutch) gas price, gives $\\hat\\beta_1=-19.55$ (t = −2.78) and $R^2=0.941$. What is the correct reading?",
                "options": [
                    "Adding 1 TWh of hydro causes the price to fall by 19.55 EUR/MWh",
                    "The high $R^2$ of 0.941 proves that gas and water drive the price",
                    "Hydro has no link with the price, since gas explains almost everything",
                    "One TWh more hydro in a month goes with a price lower by 19.55 EUR/MWh on average, gas held fixed: an association that may be spurious without cointegration"
                ],
                "correctExplanation": "The coefficient is an association, not a measured effect. Price and gas levels trend, so unless they are cointegrated the regression may be spurious; Lecture 2 tests cointegration.",
                "incorrectExplanation": "A regression on trending levels can produce a high $R^2$ without any real relation, so 0.941 is not evidence, and the significant hydro coefficient (t = −2.78) shows the link exists in the data without proving causality."
            },
            "ro": {
                "title": "Regresia hidro–preț",
                "text": "Pe date lunare din 2015–2025, modelul $p_m=\\beta_0+\\beta_1\\,\\mathrm{Hydro}_m+\\beta_2\\,\\mathrm{TTF}_m+u_m$, cu prețul în euro pe megawatt-oră (EUR/MWh), producția hidro în terawați-oră (TWh) și TTF prețul gazelor pe hubul olandez Title Transfer Facility, dă $\\hat\\beta_1=-19{,}55$ (t = −2,78) și $R^2=0{,}941$. Care este interpretarea corectă?",
                "options": [
                    "Un TWh hidro în plus determină o scădere a prețului cu 19,55 EUR/MWh",
                    "Valoarea mare a lui $R^2$, de 0,941, dovedește că gazele și apa determină prețul",
                    "Producția hidro nu are nicio legătură cu prețul, deoarece gazele explică aproape totul",
                    "Un TWh hidro în plus într-o lună este asociat, în medie, cu un preț mai mic cu 19,55 EUR/MWh, la același preț al gazelor: o asociere care poate fi spurioasă fără cointegrare"
                ],
                "correctExplanation": "Coeficientul este o asociere, nu un efect cauzal măsurat. Prețurile energiei și ale gazelor au trend, deci fără cointegrare regresia poate fi spurioasă; cointegrarea se testează în cursul 2.",
                "incorrectExplanation": "O regresie pe niveluri cu trend poate da un $R^2$ mare fără o relație reală, deci 0,941 nu este o dovadă, iar coeficientul semnificativ al producției hidro (t = −2,78) arată că legătura există în date, fără a dovedi cauzalitatea."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Brent and the Israel–Iran war",
                "text": "Brent closed at 69.36 US dollars per barrel (USD/bbl) on 12 June 2025 and at 74.23 on 13 June, the day Israel struck Iran; it peaked at 77.01 on 20 June and closed at 67.14 on 24 June. What was the one-day rise on 13 June?",
                "options": [
                    "7.0%",
                    "4.3%",
                    "12.8%",
                    "11.0%"
                ],
                "correctExplanation": "$74.23/69.36-1\\approx 7.0\\%$, or 4.3 standard deviations of the 2024 daily returns. By 24 June the price was 12.8% below the peak and 3.2% below 12 June: the risk premium was removed as quickly as it came.",
                "incorrectExplanation": "4.3 is the move in standard deviations, 12.8% the fall from the peak to 24 June and 11.0% the rise from 12 June to the peak; the one-day return compares 13 June with 12 June."
            },
            "ro": {
                "title": "Brent și războiul Israel–Iran",
                "text": "Brent s-a închis la 69,36 dolari americani pe baril (USD/bbl) la 12 iunie 2025 și la 74,23 la 13 iunie, ziua în care Israelul a atacat Iranul; maximul a fost de 77,01 la 20 iunie, iar la 24 iunie prețul de închidere a fost de 67,14. Care a fost creșterea într-o zi, la 13 iunie?",
                "options": [
                    "7,0%",
                    "4,3%",
                    "12,8%",
                    "11,0%"
                ],
                "correctExplanation": "$74{,}23/69{,}36-1\\approx 7{,}0\\%$, adică 4,3 abateri standard ale randamentelor zilnice din 2024. La 24 iunie prețul era cu 12,8% sub maxim și cu 3,2% sub nivelul din 12 iunie: prima de risc a fost eliminată la fel de repede cum a apărut.",
                "incorrectExplanation": "4,3 este variația exprimată în abateri standard, 12,8% este scăderea de la maxim pînă la 24 iunie, iar 11,0% este creșterea de la 12 iunie pînă la maxim; randamentul zilei compară 13 iunie cu 12 iunie."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "July 2024 price separation",
                "text": "In July 2024 the share of hours with equal prices, within 0.01 euro per megawatt-hour (EUR/MWh), was 86.8% for Romania–Bulgaria, 6.3% for Romania–Hungary and 3.1% for Romania–Germany; the monthly average was 145.14 EUR/MWh in Romania and 67.70 in Germany–Luxembourg. What do these shares indicate?",
                "options": [
                    "The Romania–Bulgaria border was the main bottleneck",
                    "Romania had left the European day-ahead coupling that month",
                    "The network towards Central Europe was binding most of the time, although prices alone cannot show which element",
                    "German negative prices were exported to Romania at midday"
                ],
                "correctExplanation": "Coupled prices are equal only while the network is not binding. Romania and Bulgaria were almost always equal, while the links towards Central Europe were binding: after sunset the region had to import exactly when the network was full.",
                "incorrectExplanation": "Romania stayed coupled; a high share of equal hours with Bulgaria means that border was rarely binding, and price separation from Hungary and Germany means the constraint lay towards Central Europe."
            },
            "ro": {
                "title": "Separarea prețurilor, iulie 2024",
                "text": "În iulie 2024, ponderea orelor cu prețuri egale, cu o diferență sub 0,01 euro pe megawatt-oră (EUR/MWh), a fost de 86,8% pentru România–Bulgaria, 6,3% pentru România–Ungaria și 3,1% pentru România–Germania; media lunară a fost de 145,14 EUR/MWh în România și de 67,70 în Germania–Luxemburg. Ce arată aceste ponderi?",
                "options": [
                    "Granița România–Bulgaria a fost principalul punct de congestie",
                    "România ieșise din cuplarea europeană pentru ziua următoare în acea lună",
                    "Rețeaua spre Europa Centrală a fost la limită aproape tot timpul, deși elementul saturat nu poate fi identificat numai din prețuri",
                    "Prețurile negative din Germania au fost exportate în România la amiază"
                ],
                "correctExplanation": "Prețurile piețelor cuplate sînt egale numai cît timp rețeaua nu este la limită. România și Bulgaria au avut aproape mereu același preț, în timp ce legăturile spre Europa Centrală erau la limită: după apus, regiunea trebuia să importe exact atunci cînd rețeaua era plină.",
                "incorrectExplanation": "România a rămas cuplată; o pondere mare a orelor cu prețuri egale cu Bulgaria înseamnă că acea graniță a fost rar la limită, iar separarea de Ungaria și Germania arată că restricția se afla spre Europa Centrală."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Negative hours by season",
                "text": "Since 2023, April and May hold 49.6% of all Romanian negative-price hours on the day-ahead market (PZU, Piața pentru Ziua Următoare), and June–August another 34.0%. What share falls in the remaining seven months together?",
                "options": [
                    "83.6%",
                    "34.0%",
                    "50.4%",
                    "16.4%"
                ],
                "correctExplanation": "$100-49.6-34.0=16.4\\%$. Spring combines high solar output, full reservoirs and mild demand; metered solar rose from 1.46 terawatt-hours (TWh) in 2023 to 4.33 TWh in January–October 2026 alone.",
                "incorrectExplanation": "83.6% is the share of April–August together and 50.4% the share outside April–May only; the remaining months are what is left after both groups are removed."
            },
            "ro": {
                "title": "Orele negative pe sezoane",
                "text": "Din 2023, lunile aprilie și mai concentrează 49,6% din orele cu preț negativ de pe Piața pentru Ziua Următoare (PZU) din România, iar lunile iunie–august încă 34,0%. Ce pondere revine celorlalte șapte luni împreună?",
                "options": [
                    "83,6%",
                    "34,0%",
                    "50,4%",
                    "16,4%"
                ],
                "correctExplanation": "$100-49{,}6-34{,}0=16{,}4\\%$. Primăvara combină producția solară ridicată, lacurile pline și cererea moderată; producția solară măsurată a crescut de la 1,46 terawați-oră (TWh) în 2023 la 4,33 TWh numai în ianuarie–octombrie 2026.",
                "incorrectExplanation": "83,6% este ponderea lunilor aprilie–august împreună, iar 50,4% este ponderea tuturor lunilor din afara intervalului aprilie–mai; celelalte luni reprezintă ce rămîne după scăderea ambelor grupe."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Odds of a negative day",
                "text": "A logit model on 1,035 days (January 2024 to October 2026) gives an odds ratio of 0.24 for residual load (load minus solar minus wind, in gigawatts, GW), 4.52 for hydro output and 16.13 for a weekend day. How should the 0.24 be read?",
                "options": [
                    "Each extra GW of residual load lowers the probability of a negative day by 0.24 percentage points",
                    "Each extra GW of residual load multiplies the odds of a negative day by 0.24, that is, cuts them by about three quarters",
                    "Residual load explains 24% of negative days",
                    "The model gives a 24% chance of a negative price for tomorrow's bids"
                ],
                "correctExplanation": "The odds ratio is the exponential of the coefficient ($e^{-1.445}\\approx 0.24$): it multiplies the odds, not the probability. More demand left for other plants makes a negative day much less likely.",
                "incorrectExplanation": "An odds ratio acts on the odds multiplicatively, not on probabilities in percentage points; the fit is measured by the McFadden pseudo-$R^2$ of 0.369, and the model describes realised conditions, it does not forecast for bidding."
            },
            "ro": {
                "title": "Șansele unei zile negative",
                "text": "Un model logit pe 1 035 de zile (ianuarie 2024 – octombrie 2026) dă un raport al șanselor de 0,24 pentru consumul rezidual (consumul minus producția solară și cea eoliană, în gigawați, GW), 4,52 pentru producția hidro și 16,13 pentru o zi de weekend. Cum se interpretează valoarea 0,24?",
                "options": [
                    "Fiecare GW în plus de consum rezidual reduce probabilitatea unei zile cu prețuri negative cu 0,24 puncte procentuale",
                    "Fiecare GW în plus de consum rezidual înmulțește șansele unei zile cu prețuri negative cu 0,24, adică le reduce cu circa trei sferturi",
                    "Consumul rezidual explică 24% din zilele cu prețuri negative",
                    "Modelul dă o probabilitate de 24% pentru un preț negativ în ofertele de mîine"
                ],
                "correctExplanation": "Raportul șanselor este exponențiala coeficientului ($e^{-1{,}445}\\approx 0{,}24$): el înmulțește șansele, nu probabilitatea. Cu cît rămîne mai multă cerere pentru celelalte centrale, cu atît o zi cu prețuri negative este mai puțin probabilă.",
                "incorrectExplanation": "Raportul șanselor acționează multiplicativ asupra șanselor, nu asupra probabilităților în puncte procentuale; calitatea ajustării este dată de pseudo-$R^2$ McFadden, de 0,369, iar modelul descrie condițiile înregistrate, fără a oferi prognoze pentru licitare."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "A European rise in 2026",
                "text": "In January–October 2026 the Romanian day-ahead price rose by 29.8%, from 105.88 to 137.45 euro per megawatt-hour (EUR/MWh), and the German–Luxembourg price by 30.1%, from 87.66 to 114.01. What does the comparison show?",
                "options": [
                    "The rise was European, but the Romanian premium over Germany widened from 18.2 to 23.4 EUR/MWh",
                    "The rise was purely Romanian, driven by the Cernavodă outages",
                    "The Romanian premium over Germany narrowed, because Germany rose more in percent",
                    "Prices rose because Romania had more negative hours than in 2025"
                ],
                "correctExplanation": "Both zones rose by about 30%, so the rise was European; in EUR/MWh the gap grew from 18.2 to 23.4, as nuclear fell by 31.3% and Brent rose.",
                "incorrectExplanation": "A similar percentage rise on a higher Romanian base widens the gap in EUR/MWh; and Romania had fewer negative hours in 2026 (171.75 against 196), not more."
            },
            "ro": {
                "title": "O creștere europeană în 2026",
                "text": "În ianuarie–octombrie 2026, prețul pentru ziua următoare din România a crescut cu 29,8%, de la 105,88 la 137,45 euro pe megawatt-oră (EUR/MWh), iar cel din Germania–Luxemburg cu 30,1%, de la 87,66 la 114,01. Ce arată comparația?",
                "options": [
                    "Creșterea a fost europeană, dar prima prețului românesc față de cel german s-a mărit de la 18,2 la 23,4 EUR/MWh",
                    "Creșterea a fost exclusiv românească, determinată de opririle de la Cernavodă",
                    "Prima prețului românesc față de cel german s-a redus, deoarece Germania a crescut mai mult în procente",
                    "Prețurile au crescut pentru că România a avut mai multe ore cu preț negativ decît în 2025"
                ],
                "correctExplanation": "Ambele zone au crescut cu circa 30%, deci creșterea a fost europeană; în EUR/MWh, diferența a crescut de la 18,2 la 23,4, pe fondul scăderii producției nucleare cu 31,3% și al creșterii prețului Brent.",
                "incorrectExplanation": "O creștere procentuală similară aplicată unei baze românești mai mari mărește diferența în EUR/MWh; iar România a avut mai puține ore cu preț negativ în 2026 (171,75 față de 196), nu mai multe."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Bulgaria's cheaper evenings",
                "text": "In April–September evenings (19:00–22:00 Eastern European Time, EET), the average price was 171.1 euro per megawatt-hour (EUR/MWh) in Romania and 169.7 in Bulgaria in 2025, but 215.5 against 178.0 in 2026; at midday prices stayed close (48.1 against 46.0). What is the most defensible reading?",
                "options": [
                    "Bulgarian batteries are proven to have caused the gap, since it opened only in the evening",
                    "The gap is a data error, since coupled markets always have equal prices",
                    "An evening-only gap is what batteries on one side of the border would produce, but battery data start only on 10 September 2026, so it is an association",
                    "The gap reflects cheaper Bulgarian solar output at midday"
                ],
                "correctExplanation": "The evening gap rose to 37.5 EUR/MWh while midday stayed close, the pattern of batteries charging at midday and discharging in the evening; but the Bulgarian battery series starts after the gap opened in May 2026.",
                "incorrectExplanation": "Coupled prices separate when the network binds, and midday prices stayed close, so solar is not the explanation; without battery data covering the start of the gap, the link cannot be called proof."
            },
            "ro": {
                "title": "Serile mai ieftine din Bulgaria",
                "text": "În orele de seară din aprilie–septembrie (19:00–22:00, ora Europei de Est, EET), prețul mediu a fost de 171,1 euro pe megawatt-oră (EUR/MWh) în România și de 169,7 în Bulgaria în 2025, dar de 215,5 față de 178,0 în 2026; la amiază, prețurile au rămas apropiate (48,1 față de 46,0). Care este interpretarea cea mai solidă?",
                "options": [
                    "Bateriile din Bulgaria au cauzat cu siguranță diferența, deoarece aceasta apare numai seara",
                    "Diferența este o eroare de date, deoarece piețele cuplate au întotdeauna prețuri egale",
                    "O diferență numai seara este ceea ce ar produce bateriile de o singură parte a graniței, dar datele despre baterii încep abia la 10 septembrie 2026, deci este o asociere",
                    "Diferența reflectă producția solară mai ieftină din Bulgaria la amiază"
                ],
                "correctExplanation": "Diferența de seară a urcat la 37,5 EUR/MWh, în timp ce la amiază prețurile au rămas apropiate, adică tiparul unor baterii care se încarcă la amiază și se descarcă seara; seria pentru bateriile din Bulgaria începe însă după apariția diferenței, în mai 2026.",
                "incorrectExplanation": "Prețurile cuplate se separă cînd rețeaua este la limită, iar la amiază prețurile au rămas apropiate, deci solarul nu este explicația; fără date despre baterii la începutul diferenței, legătura nu poate fi numită o dovadă."
            }
        }
    ]
};
