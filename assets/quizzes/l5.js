// ============================================================
// Quiz bank for lecture id 'l5': Derivatives and hedging (EN + RO)
// correct = index (0-3) of the right option in the original order.
// incorrectExplanation must not name a letter: the engine prepends
// "The correct answer is X) ..." after shuffling the options.
// ============================================================
window.EMQA_DATA.quizzes['l5'] = {
    "draw": 20,
    "questions": [
        {
            "correct": 1,
            "en": {
                "title": "Hedging a hydro producer",
                "text": "A Romanian hydro producer sells its output on the day-ahead market and fears a fall in prices. Which hedge matches the sign of its exposure?",
                "options": [
                    "Buy power forward or buy a cap, as a fixed-price supplier does",
                    "Sell power forward or buy a floor (a put option)",
                    "Buy power forward and sell a floor to finance it",
                    "No hedge is needed, because a hydro plant has no fuel cost"
                ],
                "correctExplanation": "A producer is long power: its profit $Q(S-c)$ falls when the spot price $S$ falls. Selling forward or buying a floor offsets this exposure; buying forward would add to the long position.",
                "incorrectExplanation": "Fix the sign of the exposure first: producers are long power and hedge by selling, suppliers are short and hedge by buying. A long firm that buys forward doubles its risk, and the absence of a fuel cost does not remove the price risk on revenue."
            },
            "ro": {
                "title": "Acoperirea unui producător hidro",
                "text": "Un producător hidro din România își vinde energia pe piața pentru ziua următoare și se teme de o scădere a prețului. Ce acoperire corespunde semnului expunerii sale?",
                "options": [
                    "Cumpără forward sau un plafon, ca un furnizor cu prețuri fixe",
                    "Vinde forward sau cumpără un prag minim (o opțiune put)",
                    "Cumpără forward și vinde un prag minim ca să îl finanțeze",
                    "Nu are nevoie de acoperire, pentru că o centrală hidro nu are cost cu combustibilul"
                ],
                "correctExplanation": "Producătorul are o poziție lungă: profitul $Q(S-c)$ scade cînd prețul spot $S$ scade. Vînzarea forward sau cumpărarea unui prag minim compensează această expunere; cumpărarea forward ar mări poziția lungă.",
                "incorrectExplanation": "Stabiliți întîi semnul expunerii: producătorii au poziție lungă și se acoperă vînzînd, furnizorii au poziție scurtă și se acoperă cumpărînd. O firmă cu poziție lungă care mai cumpără forward își dublează riscul, iar lipsa costului cu combustibilul nu elimină riscul de preț asupra veniturilor."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Hedged supplier profit",
                "text": "A supplier sells $Q$ megawatt-hours (MWh) at a fixed retail price $R$ and buys a forward for the same quantity at price $F$. With $S$ the spot price at delivery, what is its hedged profit?",
                "options": [
                    "$Q(R-S)$",
                    "$Q(S-F)$",
                    "$Q(R+F-2S)$",
                    "$Q(R-F)$"
                ],
                "correctExplanation": "The bought forward pays $Q(S-F)$; adding it to the unhedged profit $Q(R-S)$ cancels $S$ and leaves $Q(R-F)$, which depends only on prices known today.",
                "incorrectExplanation": "The forward is bought, so it pays $S-F$ per MWh, not $F-S$. Added to $Q(R-S)$, the spot price disappears: the hedged margin is the retail price minus the forward price."
            },
            "ro": {
                "title": "Profitul furnizorului acoperit",
                "text": "Un furnizor vinde $Q$ megawatt-oră (MWh) la un preț fix $R$ către clientul final și cumpără forward aceeași cantitate la prețul $F$. Dacă $S$ este prețul spot la livrare, care este profitul acoperit?",
                "options": [
                    "$Q(R-S)$",
                    "$Q(S-F)$",
                    "$Q(R+F-2S)$",
                    "$Q(R-F)$"
                ],
                "correctExplanation": "Forward-ul cumpărat aduce $Q(S-F)$; adăugat la profitul neacoperit $Q(R-S)$, el elimină $S$ și lasă $Q(R-F)$, care depinde numai de prețuri cunoscute de azi.",
                "incorrectExplanation": "Forward-ul este cumpărat, deci aduce $S-F$ pe MWh, nu $F-S$. Însumat cu $Q(R-S)$, prețul spot dispare: marja acoperită este prețul de vînzare minus prețul forward."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The 2022 saving per MW",
                "text": "The 2022 baseload forward was bought on the platform of the Romanian electricity and gas market operator (OPCOM) at a volume-weighted average price (VWAP) of 77.4 EUR per megawatt-hour (EUR/MWh); the 2022 day-ahead price averaged 265.3 EUR/MWh. Roughly how much did a supplier save per megawatt (MW) of constant consumption over the 8,760 hours of the year?",
                "options": [
                    "About 1.65 million EUR",
                    "About 0.68 million EUR",
                    "About 2.32 million EUR",
                    "About 188 thousand EUR"
                ],
                "correctExplanation": "The gap is 265.3 − 77.4 = 187.9 EUR/MWh; times 8,760 MWh for 1 MW over a year it gives about 1.65 million EUR, the figure in the lecture.",
                "incorrectExplanation": "Multiply the price gap, not a single price, by the energy: 77.4 × 8,760 is the cost of the hedge and 265.3 × 8,760 the unhedged cost; 188 thousand EUR ignores that 1 MW over a year is 8,760 MWh, not 1,000."
            },
            "ro": {
                "title": "Economia din 2022 pe MW",
                "text": "Banda pentru 2022 a fost cumpărată pe platforma operatorului pieței de energie electrică și de gaze naturale din România (OPCOM) la un preț mediu ponderat cu volumul (VWAP) de 77,4 EUR pe megawatt-oră (EUR/MWh); prețul mediu de pe piața pentru ziua următoare în 2022 a fost 265,3 EUR/MWh. Cît a economisit, aproximativ, un furnizor pentru fiecare megawatt (MW) de consum constant, în cele 8 760 de ore ale anului?",
                "options": [
                    "Circa 1,65 milioane EUR",
                    "Circa 0,68 milioane EUR",
                    "Circa 2,32 milioane EUR",
                    "Circa 188 de mii EUR"
                ],
                "correctExplanation": "Diferența este 265,3 − 77,4 = 187,9 EUR/MWh; înmulțită cu 8 760 MWh pentru 1 MW pe un an, ea dă circa 1,65 milioane EUR, cifra din curs.",
                "incorrectExplanation": "Se înmulțește diferența de preț, nu un singur preț, cu energia: 77,4 × 8 760 este costul acoperirii, iar 265,3 × 8 760 costul fără acoperire; 188 de mii EUR ignoră faptul că 1 MW pe un an înseamnă 8 760 MWh, nu 1 000."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Timing of the hedge",
                "text": "On the platform of the Romanian electricity and gas market operator (OPCOM), contracts for 2022 baseload traded on average at 54.4 EUR per megawatt-hour (EUR/MWh) in 2020, 61.5 in the first half of 2021 and 136.7 in the second half of 2021, while the 2022 spot averaged 265.3. What does this show?",
                "options": [
                    "Hedging late in 2021 was useless, since the forward had caught up with the spot",
                    "The forward price in 2020 was an accurate forecast of the 2022 spot",
                    "Buying late cost about twice as much as buying early, yet still far less than the spot",
                    "The timing of the purchase hardly matters once the decision to hedge is taken"
                ],
                "correctExplanation": "136.7 is roughly twice 54.4–61.5, so a supplier that waited paid about double; but 136.7 was still far below the 265.3 realised in 2022. The timing of the purchase mattered almost as much as the decision to hedge.",
                "incorrectExplanation": "Late buyers still saved over 125 EUR/MWh relative to the spot, so the hedge was not useless, and the 2020 price missed the 2022 spot by a wide margin. The lesson is that when you hedge matters, which is why a policy spreads purchases over time."
            },
            "ro": {
                "title": "Momentul acoperirii",
                "text": "Pe platforma operatorului pieței de energie electrică și de gaze naturale din România (OPCOM), contractele pentru banda 2022 s-au tranzacționat, în medie, la 54,4 EUR pe megawatt-oră (EUR/MWh) în 2020, la 61,5 în semestrul I 2021 și la 136,7 în semestrul II 2021, în timp ce spotul din 2022 a avut media 265,3. Ce arată aceste cifre?",
                "options": [
                    "Acoperirea de la sfîrșitul lui 2021 a fost inutilă, pentru că forward-ul ajunsese la nivelul spotului",
                    "Prețul forward din 2020 a fost o prognoză exactă a spotului din 2022",
                    "Cumpărarea tîrzie a costat aproximativ dublu față de cea timpurie, dar tot mult mai puțin decît spotul",
                    "Momentul cumpărării aproape că nu contează, odată luată decizia de acoperire"
                ],
                "correctExplanation": "136,7 este aproximativ dublul valorilor 54,4–61,5, deci un furnizor care a așteptat a plătit cam dublu; totuși, 136,7 a rămas mult sub media de 265,3 realizată în 2022. Momentul cumpărării a contat aproape la fel de mult ca decizia de a se acoperi.",
                "incorrectExplanation": "Cumpărătorii tîrzii au economisit totuși peste 125 EUR/MWh față de spot, deci acoperirea nu a fost inutilă, iar prețul din 2020 a ratat cu mult spotul din 2022. Lecția este că momentul acoperirii contează; de aceea, politica eșalonează cumpărările în timp."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "A hedge is a transfer",
                "text": "Each megawatt-hour (MWh) sold forward for 2022 went 187.9 EUR/MWh below the spot price. How should a board interpret this number?",
                "options": [
                    "As value created by the forward market for both sides",
                    "As a transfer: producers that sold forward lost exactly what hedged suppliers saved",
                    "As proof that producers should never sell forward",
                    "As a risk premium that sellers systematically earn"
                ],
                "correctExplanation": "A hedge moves money between buyer and seller; it does not create value from nothing. The 187.9 EUR/MWh gained by hedged suppliers in 2022 is exactly what producers that sold forward gave up.",
                "incorrectExplanation": "The forward is a zero-sum contract between the two sides. One crisis year does not prove that selling forward is wrong (in 2025 producers gave up only 6.0 EUR/MWh for a fixed revenue), and the 2022 gap was a loss for sellers, not a premium earned by them."
            },
            "ro": {
                "title": "Acoperirea ca transfer",
                "text": "Fiecare megawatt-oră (MWh) vîndut forward pentru 2022 a fost cu 187,9 EUR/MWh sub prețul spot. Cum ar trebui să interpreteze consiliul de administrație această cifră?",
                "options": [
                    "Ca valoare creată de piața forward pentru ambele părți",
                    "Ca un transfer: producătorii care au vîndut forward au pierdut exact cît au economisit furnizorii acoperiți",
                    "Ca dovadă că producătorii nu ar trebui să vîndă niciodată forward",
                    "Ca o primă de risc pe care vînzătorii o încasează sistematic"
                ],
                "correctExplanation": "Acoperirea mută bani între cumpărător și vînzător; nu creează un cîștig din nimic. Cei 187,9 EUR/MWh cîștigați în 2022 de furnizorii acoperiți sînt exact suma la care au renunțat producătorii care au vîndut forward.",
                "incorrectExplanation": "Contractul forward este un joc cu sumă nulă între cele două părți. Un singur an de criză nu arată că vînzarea forward este greșită (în 2025, producătorii au renunțat doar la 6,0 EUR/MWh pentru un venit sigur), iar diferența din 2022 a fost o pierdere pentru vînzători, nu o primă încasată de ei."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Collapse of forward volume",
                "text": "After Government Emergency Ordinance (OUG) 153/2022 created the Centralised Electricity Purchase Mechanism (MACEE), with the Romanian electricity and gas market operator (OPCOM) as single buyer at 450 lei per megawatt-hour (lei/MWh), what happened to forward volume on OPCOM?",
                "options": [
                    "It rose from 1.6 terawatt-hours (TWh) in 2021 to 27.3 TWh in 2023",
                    "It stayed close to 15 terawatt-hours (TWh) a year throughout 2021–2023",
                    "It fell from 83.7 terawatt-hours (TWh) in 2021 to 7.4 TWh in 2023",
                    "It fell from 27.3 terawatt-hours (TWh) in 2021 to 1.6 TWh in 2023"
                ],
                "correctExplanation": "Forward volume peaked at 27.3 TWh in 2021 and collapsed to 1.6 TWh in 2023, when price caps and the MACEE single-buyer mechanism replaced bilateral trading; liquidity has since returned only in part.",
                "incorrectExplanation": "83.7 TWh is the total of all 2,298 auctions from 2020 to 2026, not one year's volume. The crisis froze forward trading: regulation replaced the market that firms would have used to hedge, which is why a hedging policy must exist before the next shock."
            },
            "ro": {
                "title": "Prăbușirea volumului forward",
                "text": "După ce Ordonanța de urgență a Guvernului (OUG) 153/2022 a creat Mecanismul de achiziție centralizată de energie electrică (MACEE), în care operatorul pieței de energie electrică și de gaze naturale din România (OPCOM) a fost cumpărător unic la 450 lei pe megawatt-oră (lei/MWh), ce s-a întîmplat cu volumul forward pe OPCOM?",
                "options": [
                    "A crescut de la 1,6 terawatt-oră (TWh) în 2021 la 27,3 TWh în 2023",
                    "A rămas în jur de 15 terawatt-oră (TWh) pe an în 2021–2023",
                    "A scăzut de la 83,7 terawatt-oră (TWh) în 2021 la 7,4 TWh în 2023",
                    "A scăzut de la 27,3 terawatt-oră (TWh) în 2021 la 1,6 TWh în 2023"
                ],
                "correctExplanation": "Volumul forward a atins maximul de 27,3 TWh în 2021 și s-a prăbușit la 1,6 TWh în 2023, cînd plafonarea prețurilor și mecanismul cu cumpărător unic MACEE au înlocuit tranzacțiile bilaterale; de atunci, lichiditatea a revenit doar parțial.",
                "incorrectExplanation": "83,7 TWh este totalul celor 2 298 de licitații din 2020–2026, nu volumul unui singur an. Criza a blocat piața forward: reglementarea a înlocuit piața pe care firmele ar fi folosit-o pentru acoperire; de aceea, politica de acoperire trebuie să existe înainte de următorul șoc."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Locking in the 2027 band",
                "text": "On 31 Oct 2026 the Romanian electricity and gas market operator (OPCOM) priced the 2027 baseload year at 148.1 EUR per megawatt-hour (EUR/MWh) and the next month at 215.3, while the October spot averaged 239.3. What annual energy cost does a supplier lock in today for 1 megawatt (MW) of flat consumption in 2027?",
                "options": [
                    "About 1.30 million EUR",
                    "About 1.89 million EUR",
                    "About 2.10 million EUR",
                    "About 110 thousand EUR"
                ],
                "correctExplanation": "A yearly band of 1 MW delivers 8,760 MWh; at 148.1 EUR/MWh that is about 1.30 million EUR. An offer for 2027 must start from the forward of the delivery period.",
                "incorrectExplanation": "Use the forward of the delivery period, not the next month (215.3) or today's spot (239.3), and multiply by the 8,760 hours of a year, not by the 744 hours of a 31-day month."
            },
            "ro": {
                "title": "Fixarea benzii pentru 2027",
                "text": "La 31 octombrie 2026, pe platforma operatorului pieței de energie electrică și de gaze naturale din România (OPCOM), anul 2027 avea prețul de 148,1 EUR pe megawatt-oră (EUR/MWh), iar luna următoare 215,3, în timp ce spotul din octombrie a avut media 239,3. Ce cost anual al energiei fixează azi un furnizor pentru 1 megawatt (MW) de consum constant în 2027?",
                "options": [
                    "Circa 1,30 milioane EUR",
                    "Circa 1,89 milioane EUR",
                    "Circa 2,10 milioane EUR",
                    "Circa 110 mii EUR"
                ],
                "correctExplanation": "O bandă anuală de 1 MW livrează 8 760 MWh; la 148,1 EUR/MWh, costul este de circa 1,30 milioane EUR. Oferta pentru 2027 trebuie să pornească de la prețul forward al perioadei de livrare.",
                "incorrectExplanation": "Se folosește prețul forward al perioadei de livrare, nu al lunii următoare (215,3) sau spotul de azi (239,3), și se înmulțește cu cele 8 760 de ore ale anului, nu cu cele 744 de ore ale unei luni de 31 de zile."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Physical or cash-settled",
                "text": "A Romanian supplier can hedge with a physical forward on the platform of the Romanian electricity and gas market operator (OPCOM) or with a cash-settled future on the German price. When do the two give the same hedged cost?",
                "options": [
                    "Always, because both fix the price $F$ today",
                    "Only if the future is cleared, so that counterparty risk disappears",
                    "Only if the future's settlement average equals the average price the firm actually pays",
                    "Only if the variation margin is paid at delivery rather than daily"
                ],
                "correctExplanation": "The cash-settled future pays $(\\bar S^{\\text{ref}}-F)Q$ while the firm buys at $\\bar S$; the cost equals $FQ$ only if $\\bar S^{\\text{ref}}=\\bar S$. Any gap between the two averages is basis risk.",
                "incorrectExplanation": "Clearing removes counterparty risk and daily margins change only the timing of cash flows, but neither makes the German average equal the Romanian one. A physical forward on OPCOM carries no basis risk; a foreign future does."
            },
            "ro": {
                "title": "Livrare fizică sau financiară",
                "text": "Un furnizor din România se poate acoperi cu un forward cu livrare fizică pe platforma operatorului pieței de energie electrică și de gaze naturale din România (OPCOM) sau cu un contract futures cu decontare financiară pe prețul din Germania. Cînd dau cele două același cost acoperit?",
                "options": [
                    "Întotdeauna, pentru că ambele fixează de azi prețul $F$",
                    "Numai dacă contractul futures trece printr-o casă de compensație, care elimină riscul de contrapartidă",
                    "Numai dacă media de decontare a contractului futures este egală cu prețul mediu plătit efectiv de firmă",
                    "Numai dacă marja de variație se plătește la livrare, nu zilnic"
                ],
                "correctExplanation": "Contractul futures financiar plătește $(\\bar S^{\\text{ref}}-F)Q$, iar firma cumpără la $\\bar S$; costul este $FQ$ numai dacă $\\bar S^{\\text{ref}}=\\bar S$. Orice diferență între cele două medii este risc de bază.",
                "incorrectExplanation": "Casa de compensație elimină riscul de contrapartidă, iar marjele zilnice schimbă doar momentul plăților, dar niciuna nu face media din Germania egală cu cea din România. Forward-ul fizic de pe OPCOM nu are risc de bază; contractul din străinătate are."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Size of a margin call",
                "text": "The New York Mercantile Exchange (NYMEX) gas future on the Title Transfer Facility (TTF) for December 2026 had its largest daily move, 11.83 EUR per megawatt-hour (EUR/MWh), on 29 Aug 2022. What variation margin (VM) did that day mean for a position of 10 megawatts (MW) over 744 hours?",
                "options": [
                    "About 11,830 EUR",
                    "About 88,015 EUR",
                    "About 880,152 EUR",
                    "About 8,802 EUR"
                ],
                "correctExplanation": "The position is 10 × 744 = 7,440 MWh, and $VM_t=Q(F_t-F_{t-1})$ = 7,440 × 11.83 ≈ 88,015 EUR, paid in a single day.",
                "incorrectExplanation": "The margin is the price change times the whole position in MWh, not per MW or per hour. A firm that cannot pay such a call is forced to close the hedge when it needs it most, so the credit line must be sized for the worst daily move."
            },
            "ro": {
                "title": "Mărimea apelului în marjă",
                "text": "Contractul futures pe gaze al bursei New York Mercantile Exchange (NYMEX) pentru Title Transfer Facility (TTF), hubul olandez de gaze naturale, cu livrare în decembrie 2026, a avut cea mai mare variație zilnică, de 11,83 EUR pe megawatt-oră (EUR/MWh), la 29 august 2022. Ce marjă de variație (VM) a însemnat acea zi pentru o poziție de 10 megawați (MW) pe 744 de ore?",
                "options": [
                    "Circa 11 830 EUR",
                    "Circa 88 015 EUR",
                    "Circa 880 152 EUR",
                    "Circa 8 802 EUR"
                ],
                "correctExplanation": "Poziția este 10 × 744 = 7 440 MWh, iar $VM_t=Q(F_t-F_{t-1})$ = 7 440 × 11,83 ≈ 88 015 EUR, plătiți într-o singură zi.",
                "incorrectExplanation": "Marja este variația prețului înmulțită cu întreaga poziție în MWh, nu pe MW sau pe oră. O firmă care nu poate plăti un asemenea apel este obligată să închidă acoperirea exact cînd are cea mai mare nevoie de ea, deci linia de credit se dimensionează pentru cea mai mare variație zilnică."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Gas versus power forwards",
                "text": "Why is the forward price of gas at the Dutch Title Transfer Facility (TTF) tied to its spot price by the cost of carry, while the Romanian power forward is not?",
                "options": [
                    "Because gas is traded on an exchange and Romanian power only in auctions",
                    "Because power forwards include the price of emission allowances and gas forwards do not",
                    "Because the power market has no interest rate, so $r=0$ in the formula",
                    "Because gas can be stored and power cannot, so the power forward is the expected spot plus a risk premium"
                ],
                "correctExplanation": "Storage allows arbitrage between spot and forward, so $F_{t,T}=S_te^{(r+u-y)(T-t)}$. Power cannot be stored, so $F_{t,T}=E_t[\\bar S_T]+\\pi_{t,T}$: the expected average spot over the delivery period plus a risk premium.",
                "incorrectExplanation": "The difference comes from storability, not from the trading venue or from carbon costs. That is also why the TTF curve shows a winter premium over summer (103.9 EUR/MWh for December 2026 against 78.1 for May 2027): it pays for storage."
            },
            "ro": {
                "title": "Forward pe gaze și pe energie",
                "text": "De ce prețul forward al gazelor la Title Transfer Facility (TTF), hubul olandez de gaze naturale, este legat de spot prin costul de deținere, iar prețul forward al energiei electrice din România nu?",
                "options": [
                    "Pentru că gazele se tranzacționează la bursă, iar energia din România doar în licitații",
                    "Pentru că prețul forward al energiei include certificatele de emisii, iar cel al gazelor nu",
                    "Pentru că pe piața energiei nu există dobîndă, deci $r=0$ în formulă",
                    "Pentru că gazele se pot stoca, iar energia electrică nu, deci forward-ul ei este spotul așteptat plus o primă de risc"
                ],
                "correctExplanation": "Stocarea permite arbitrajul între spot și forward, deci $F_{t,T}=S_te^{(r+u-y)(T-t)}$. Energia electrică nu se poate stoca, așa că $F_{t,T}=E_t[\\bar S_T]+\\pi_{t,T}$: spotul mediu așteptat pe perioada de livrare plus o primă de risc.",
                "incorrectExplanation": "Diferența vine din posibilitatea stocării, nu din locul de tranzacționare sau din costul carbonului. Tot de aceea curba TTF arată o diferență între iarnă și vară (103,9 EUR/MWh pentru decembrie 2026, față de 78,1 pentru mai 2027): ea acoperă costul stocării."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Reading the Romanian curve",
                "text": "In October 2026 the Romanian spot averaged 239.3 EUR per megawatt-hour (EUR/MWh), the first quarter of 2027 traded at 176.7 and the year 2027 at 148.1. How is this curve described, and what follows for a 2027 budget?",
                "options": [
                    "Backwardation ($F \\lt S$); the budget should start from 148.1, not from the October spot",
                    "Contango ($F \\gt S$); the budget should start from the October spot of 239.3",
                    "Backwardation ($F \\lt S$); the budget should start from the October spot, since the curve is only a forecast",
                    "Contango ($F \\gt S$); the budget should use the first-quarter price of 176.7 for the whole year"
                ],
                "correctExplanation": "A curve below the spot is in backwardation: the market expects the price spike to fade. The 2027 band at 148.1 EUR/MWh is the price at which next year's energy can be locked in today, so it is the right starting point.",
                "incorrectExplanation": "Contango means a forward above the spot, which is not the case here. Today's spot should never enter next year's budget: the forward of the delivery period is the price actually available, and a quarterly price covers only three months."
            },
            "ro": {
                "title": "Interpretarea curbei forward",
                "text": "În octombrie 2026, spotul din România a avut media 239,3 EUR pe megawatt-oră (EUR/MWh), trimestrul I 2027 se tranzacționa la 176,7, iar anul 2027 la 148,1. Cum se numește această formă a curbei și ce rezultă pentru bugetul pe 2027?",
                "options": [
                    "Deport ($F \\lt S$); bugetul pornește de la 148,1, nu de la spotul din octombrie",
                    "Report ($F \\gt S$); bugetul pornește de la spotul din octombrie, de 239,3",
                    "Deport ($F \\lt S$); bugetul pornește de la spotul din octombrie, pentru că curba este doar o prognoză",
                    "Report ($F \\gt S$); bugetul folosește prețul trimestrului I, de 176,7, pentru tot anul"
                ],
                "correctExplanation": "O curbă situată sub spot indică deport (backwardation): piața se așteaptă ca prețurile ridicate de acum să scadă. Banda pentru 2027, la 148,1 EUR/MWh, este prețul la care energia anului viitor poate fi fixată de azi, deci este punctul de plecare corect.",
                "incorrectExplanation": "Reportul (contango) înseamnă un forward peste spot, ceea ce nu este cazul aici. Spotul de azi nu trebuie pus în bugetul anului viitor: prețul forward al perioadei de livrare este prețul disponibil efectiv, iar prețul unui trimestru acoperă doar trei luni."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Forward is not a forecast",
                "text": "The 2023 baseload forward on the platform of the Romanian electricity and gas market operator (OPCOM) was bought at a volume-weighted average price (VWAP) of 172.5 EUR per megawatt-hour (EUR/MWh), while the 2023 spot averaged 103.7; for 2021 the figures were 51.3 and 111.4. What is the right reading?",
                "options": [
                    "The forward is a biased forecast that always exceeds the realised price",
                    "Buyers of the 2023 band made an error that a better price forecast would have avoided",
                    "The forward is the price of certainty; its error can be large and of either sign",
                    "The forward is an unbiased forecast, so the two errors cancel and can be ignored"
                ],
                "correctExplanation": "In 2021 the forward was far below the realised spot, in 2023 far above, because it was bought at the height of the crisis. A hedge fixes the cost of each year, but the level at which it is fixed depends on the moment of purchase.",
                "incorrectExplanation": "Errors of both signs rule out a bias in one fixed direction, and the 2023 buyers did exactly what a hedge does: they removed uncertainty at the price then available. The forward should not be relied on as a forecast in a crisis."
            },
            "ro": {
                "title": "Forward-ul nu este o prognoză",
                "text": "Banda pentru 2023 a fost cumpărată pe platforma operatorului pieței de energie electrică și de gaze naturale din România (OPCOM) la un preț mediu ponderat cu volumul (VWAP) de 172,5 EUR pe megawatt-oră (EUR/MWh), iar spotul din 2023 a avut media 103,7; pentru 2021, cifrele au fost 51,3 și 111,4. Care este interpretarea corectă?",
                "options": [
                    "Forward-ul este o prognoză deplasată, care depășește întotdeauna prețul realizat",
                    "Cumpărătorii benzii pentru 2023 au făcut o greșeală pe care o prognoză mai bună ar fi evitat-o",
                    "Forward-ul este prețul certitudinii; eroarea lui poate fi mare și de ambele semne",
                    "Forward-ul este o prognoză nedeplasată, deci cele două erori se compensează și pot fi ignorate"
                ],
                "correctExplanation": "În 2021, forward-ul a fost mult sub spotul realizat, iar în 2023 mult peste, pentru că a fost cumpărat în plină criză. Acoperirea fixează costul fiecărui an, dar nivelul la care îl fixează depinde de momentul cumpărării.",
                "incorrectExplanation": "Erorile de ambele semne exclud o deplasare într-o singură direcție, iar cumpărătorii din 2023 au făcut exact ce face o acoperire: au eliminat incertitudinea la prețul disponibil atunci. Forward-ul nu trebuie folosit ca prognoză în vremuri de criză."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Testing the forward premium",
                "text": "Over 30 delivery months bought one month ahead, the mean ex-post premium (forward minus realised spot) is +5.2 EUR per megawatt-hour (EUR/MWh), with $t$ = 0.42 based on a heteroskedasticity- and autocorrelation-consistent (HAC) standard error, and $p$ = 0.68. What should a manager conclude?",
                "options": [
                    "Buyers pay a significant premium, so hedging is expensive on average",
                    "Sellers accept a significant discount, so producers should avoid forwards",
                    "There is no evidence of a premium: hedging is cheap on average, and its real cost is the upside given up",
                    "The premium is significant at the 5% level, because its mean is positive"
                ],
                "correctExplanation": "With $t$ = 0.42 the mean is far from significant, and the median is −0.2 EUR/MWh. Hedging costs little on average; what it really gives up is the gain when prices move favourably.",
                "incorrectExplanation": "A positive mean is not evidence when its standard error is large: $p$ = 0.68 means such a mean arises easily when the true premium is zero. Even since 2023, at +24.5 with $t$ = 1.51, the premium is not significant."
            },
            "ro": {
                "title": "Testul primei forward",
                "text": "Pentru 30 de luni de livrare cumpărate cu o lună înainte, prima medie ex post (forward minus spotul realizat) este +5,2 EUR pe megawatt-oră (EUR/MWh), cu $t$ = 0,42, calculat cu eroarea standard robustă la heteroscedasticitate și autocorelare (HAC), și $p$ = 0,68. Ce ar trebui să concluzioneze un manager?",
                "options": [
                    "Cumpărătorii plătesc o primă semnificativă, deci acoperirea este scumpă în medie",
                    "Vînzătorii acceptă o reducere semnificativă, deci producătorii ar trebui să evite forward-urile",
                    "Nu există dovezi ale unei prime: acoperirea este, în medie, ieftină, iar costul ei real este cîștigul la care se renunță",
                    "Prima este semnificativă la pragul de 5%, pentru că media ei este pozitivă"
                ],
                "correctExplanation": "Cu $t$ = 0,42, media este departe de a fi semnificativă, iar mediana este −0,2 EUR/MWh. Acoperirea costă puțin în medie; la ce renunță cu adevărat este cîștigul cînd prețurile evoluează favorabil.",
                "incorrectExplanation": "O medie pozitivă nu este o dovadă cînd eroarea ei standard este mare: $p$ = 0,68 arată că o asemenea medie apare ușor și cînd prima reală este zero. Nici din 2023, cu +24,5 și $t$ = 1,51, prima nu este semnificativă."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Premium by sub-period",
                "text": "Across all products of the Romanian electricity and gas market operator (OPCOM), weighted by volume, the ex-post forward premium was −55.8 EUR per megawatt-hour (EUR/MWh) for deliveries up to 2021, −166.5 for 2022 and +29.7 from 2023. Which statement do these figures support?",
                "options": [
                    "Forwards are a systematically cheap way to buy energy in Romania",
                    "The sign of the premium depends on the period, so it cannot guide the hedge",
                    "Forwards became systematically expensive after 2023, so suppliers should stop hedging",
                    "The negative values show that sellers were compensated for bearing risk"
                ],
                "correctExplanation": "The volume-weighted premium was negative before and during the crisis, when the spot surprised upward, and positive from 2023: there is no stable sign. A hedge should be judged by the risk it removed, not by its ex-post profit.",
                "incorrectExplanation": "Negative values mean that buyers paid less than the realised spot, so sellers lost rather than being compensated. One sub-period of positive premia is no reason to stop hedging; the hedged share should be set by policy, not by a view on the premium."
            },
            "ro": {
                "title": "Prima pe subperioade",
                "text": "Pentru toate produsele operatorului pieței de energie electrică și de gaze naturale din România (OPCOM), ponderate cu volumul, prima forward ex post a fost −55,8 EUR pe megawatt-oră (EUR/MWh) pentru livrările pînă în 2021, −166,5 în 2022 și +29,7 din 2023. Ce afirmație susțin aceste cifre?",
                "options": [
                    "Forward-ul este o cale sistematic ieftină de a cumpăra energie în România",
                    "Semnul primei depinde de perioadă, deci nu poate ghida acoperirea",
                    "Forward-ul a devenit sistematic scump după 2023, deci furnizorii ar trebui să renunțe la acoperire",
                    "Valorile negative arată că vînzătorii au fost recompensați pentru riscul asumat"
                ],
                "correctExplanation": "Prima ponderată cu volumul a fost negativă înainte de criză și în timpul ei, cînd spotul a crescut neașteptat, și pozitivă din 2023: nu există un semn stabil. O acoperire se judecă după riscul eliminat, nu după profitul de după livrare.",
                "incorrectExplanation": "Valorile negative înseamnă că cumpărătorii au plătit mai puțin decît spotul realizat, deci vînzătorii au pierdut, nu au fost recompensați. O singură subperioadă cu prime pozitive nu justifică renunțarea la acoperire; ponderea acoperită se stabilește prin politică, nu după o opinie despre primă."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Computing the clean spark spread",
                "text": "In October 2026 Romanian power cost 239.3 EUR per megawatt-hour (EUR/MWh), gas 86.8 EUR per MWh thermal and the European Union (EU) emission allowance (EUA) 82.4 EUR/t. With an efficiency $\\eta_g$ = 0.50 and 0.202 t CO$_2$ per MWh thermal, what was the clean spark spread (CSS)?",
                "options": [
                    "+32.4 EUR/MWh",
                    "+65.7 EUR/MWh",
                    "+49.1 EUR/MWh",
                    "+152.5 EUR/MWh"
                ],
                "correctExplanation": "Fuel costs 86.8/0.5 = 173.6 and carbon (0.202/0.5) × 82.4 = 0.404 × 82.4 = 33.3 per MWh of power, so $CSS$ = 239.3 − 173.6 − 33.3 = +32.4 EUR/MWh.",
                "incorrectExplanation": "+65.7 is the spark spread without carbon; +49.1 forgets to divide the emission factor by the efficiency; +152.5 forgets that a plant with 50% efficiency burns 2 MWh of gas per MWh of power. All costs must be expressed per MWh of electricity."
            },
            "ro": {
                "title": "Calculul clean spark spread",
                "text": "În octombrie 2026, energia electrică din România a costat 239,3 EUR pe megawatt-oră (EUR/MWh), gazele 86,8 EUR pe MWh termic, iar certificatul de emisii (EUA) al Uniunii Europene (UE) 82,4 EUR/t. Cu randamentul $\\eta_g$ = 0,50 și 0,202 t CO$_2$ pe MWh termic, cît a fost clean spark spread (CSS), marja curată a centralei pe gaze?",
                "options": [
                    "+32,4 EUR/MWh",
                    "+65,7 EUR/MWh",
                    "+49,1 EUR/MWh",
                    "+152,5 EUR/MWh"
                ],
                "correctExplanation": "Combustibilul costă 86,8/0,5 = 173,6, iar carbonul (0,202/0,5) × 82,4 = 0,404 × 82,4 = 33,3 pe MWh electric, deci $CSS$ = 239,3 − 173,6 − 33,3 = +32,4 EUR/MWh.",
                "incorrectExplanation": "+65,7 este spark spread, fără carbon; +49,1 omite împărțirea factorului de emisie la randament; +152,5 ignoră faptul că o centrală cu randament de 50% arde 2 MWh de gaze pentru fiecare MWh electric. Toate costurile trebuie exprimate pe MWh de energie electrică."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Coal-to-gas switching price",
                "text": "In October 2026 the switching price $A^{*}$, the price of the European Union (EU) emission allowance (EUA) at which the clean spark spread equals the clean dark spread, was 283.7 EUR/t, while the EUA cost 82.4 EUR/t. What does this imply?",
                "options": [
                    "Gas plants were ahead of coal plants in the merit order",
                    "The EUA price was too high for coal plants to run profitably",
                    "A small rise in the EUA price would have made gas cheaper than coal",
                    "With gas this expensive, coal remained the cheaper fuel even after paying for carbon"
                ],
                "correctExplanation": "Coal falls behind gas only when the EUA price exceeds $A^{*}$. At 82.4 EUR/t, far below 283.7, coal stayed cheaper; the clean dark spread in Romania was +131.7 EUR per megawatt-hour (EUR/MWh).",
                "incorrectExplanation": "Because coal emits more CO$_2$ per MWh, a high EUA price favours gas, but here the gap to the switching price was over 200 EUR/t. Note the caveat: Romanian lignite has no market price, so coal is proxied by the South African export price."
            },
            "ro": {
                "title": "Prețul de echilibru al carbonului",
                "text": "În octombrie 2026, prețul de echilibru $A^{*}$, adică prețul certificatului de emisii (EUA) al Uniunii Europene (UE) la care clean spark spread este egal cu clean dark spread, a fost 283,7 EUR/t, iar EUA costa 82,4 EUR/t. Ce rezultă de aici?",
                "options": [
                    "Centralele pe gaze erau înaintea celor pe cărbune în ordinea de merit",
                    "Prețul EUA era prea mare pentru ca centralele pe cărbune să fie profitabile",
                    "O creștere mică a prețului EUA ar fi făcut gazele mai ieftine decît cărbunele",
                    "Cu gaze atît de scumpe, cărbunele a rămas combustibilul mai ieftin, chiar și după plata carbonului"
                ],
                "correctExplanation": "Cărbunele trece după gaze doar cînd prețul EUA depășește $A^{*}$. La 82,4 EUR/t, mult sub 283,7, cărbunele a rămas mai ieftin; clean dark spread în România a fost +131,7 EUR pe megawatt-oră (EUR/MWh).",
                "incorrectExplanation": "Cărbunele emite mai mult CO$_2$ pe MWh, deci un preț ridicat al EUA favorizează gazele, dar aici distanța pînă la prețul de echilibru depășea 200 EUR/t. Rezultatul are o limită: lignitul din România nu are preț de piață, așa că se folosește prețul cărbunelui sud-african de export."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Value of flexibility",
                "text": "Over the 12 months to October 2026, a must-run gas plant in Romania would have earned 38,095 EUR per megawatt (MW) and a flexible one 235,494; in Germany the figures were −165,206 and 112,724. What explains the gap?",
                "options": [
                    "Flexible plants buy gas at lower prices than must-run plants",
                    "The flexible figure includes start-up costs, which the must-run figure omits",
                    "Romania has lower gas and carbon prices than Germany",
                    "A flexible plant earns only the positive hourly spreads, like a strip of call options"
                ],
                "correctExplanation": "Running only when the hourly clean spark spread $CSS_h$ is positive earns $\\sum_h \\max(CSS_h,0)$, which is at least $\\max(\\sum_h CSS_h,0)$. In Germany flexibility turns a loss into a profit.",
                "incorrectExplanation": "Both plants face the same monthly gas and carbon prices, and the calculation ignores start-up costs, so the flexible value is an upper bound. Romania earns more because its power prices are higher, not because its fuel is cheaper. Value a gas plant or a battery as options, never as a mean spread times 8,760 h."
            },
            "ro": {
                "title": "Valoarea flexibilității",
                "text": "În cele 12 luni pînă în octombrie 2026, o centrală pe gaze cu funcționare continuă ar fi cîștigat în România 38 095 EUR pe megawatt (MW), iar una flexibilă 235 494; în Germania, cifrele au fost −165 206 și 112 724. Ce explică diferența?",
                "options": [
                    "Centralele flexibile cumpără gazele mai ieftin decît cele cu funcționare continuă",
                    "Cifra pentru centrala flexibilă include costurile de pornire, omise la funcționarea continuă",
                    "România are prețuri ale gazelor și carbonului mai mici decît Germania",
                    "O centrală flexibilă încasează doar marjele orare pozitive, ca o serie de opțiuni call"
                ],
                "correctExplanation": "Funcționînd doar cînd clean spark spread orar $CSS_h$ este pozitiv, centrala încasează $\\sum_h \\max(CSS_h,0)$, cel puțin cît $\\max(\\sum_h CSS_h,0)$. În Germania, flexibilitatea transformă pierderea în profit.",
                "incorrectExplanation": "Ambele centrale au aceleași prețuri lunare ale gazelor și carbonului, iar calculul ignoră costurile de pornire, deci valoarea centralei flexibile este o limită superioară. România cîștigă mai mult pentru că prețul energiei este mai ridicat, nu pentru că are combustibil mai ieftin. Evaluați o centrală pe gaze sau o baterie ca opțiuni, nu ca marjă medie înmulțită cu 8 760 h."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Hedging a flexible plant",
                "text": "Sorted hourly clean spark spreads show that a flexible gas plant earns most of its margin in a minority of very profitable hours. Which forward product best hedges its power sales?",
                "options": [
                    "Peak products, which cover the hours in which the plant actually runs",
                    "A baseload band, because it sells all hours equally",
                    "A calendar-year band, because it holds most of the volume of the Romanian electricity and gas market operator (OPCOM)",
                    "No power forward at all, since a plant that behaves like an option needs no hedge"
                ],
                "correctExplanation": "The plant's income comes from the peak hours, so a band contract, which sells every hour, does not match its output profile. Peak products sell the hours in which the plant actually produces.",
                "incorrectExplanation": "Selling a band would commit the plant to deliver in cheap hours when it would rather stay off. The liquidity of calendar products does not fix this mismatch, and the plant still carries price risk in the hours in which it runs."
            },
            "ro": {
                "title": "Acoperirea centralei flexibile",
                "text": "Clean spark spread orar, ordonat descrescător, arată că o centrală pe gaze flexibilă își cîștigă cea mai mare parte a marjei într-o minoritate de ore foarte profitabile. Ce produs forward acoperă cel mai bine vînzările ei de energie?",
                "options": [
                    "Produsele de vîrf, care acoperă orele în care centrala funcționează efectiv",
                    "Banda, pentru că vinde toate orele la fel",
                    "Banda pe an calendaristic, pentru că reprezintă cea mai mare parte a volumului operatorului pieței de energie electrică și de gaze naturale din România (OPCOM)",
                    "Niciun forward, pentru că o centrală care se comportă ca o opțiune nu are nevoie de acoperire"
                ],
                "correctExplanation": "Venitul centralei vine din orele de vîrf, așa că un contract în bandă, care vinde toate orele, nu corespunde profilului ei de producție. Produsele de vîrf vînd exact orele în care centrala produce.",
                "incorrectExplanation": "Vînzarea unei benzi ar obliga centrala să livreze și în orele ieftine, cînd ar prefera să stea oprită. Lichiditatea produselor anuale nu rezolvă această nepotrivire, iar centrala rămîne expusă la preț în orele în care funcționează."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Minimum-variance hedge ratio",
                "text": "The minimum-variance hedge ratio $h^{*}$ minimises $\\mathrm{Var}(\\Delta S-h\\Delta F)$. Which expression gives it, and how is it estimated in the lecture?",
                "options": [
                    "$h^{*}=\\sigma_S/\\sigma_F$, the ratio of the standard deviations, computed directly",
                    "$h^{*}=\\rho$, the correlation between the changes of the exposure and of the hedge",
                    "$h^{*}=\\rho\\,\\sigma_S/\\sigma_F$, the slope of an ordinary least squares (OLS) regression of $\\Delta S$ on $\\Delta F$",
                    "$h^{*}=\\rho^2$, the share of variance removed by the hedge"
                ],
                "correctExplanation": "Setting the derivative to zero gives $h^{*}=\\mathrm{Cov}(\\Delta S,\\Delta F)/\\mathrm{Var}(\\Delta F)=\\rho\\,\\sigma_S/\\sigma_F$, which is the ordinary least squares slope. The share of variance removed, $\\rho^2$, is the hedge effectiveness, a different quantity.",
                "incorrectExplanation": "The ratio of volatilities ignores how closely the two prices move together, and the correlation alone ignores their relative size. $\\rho^2$ measures how good the hedge is, not how many contracts to hold."
            },
            "ro": {
                "title": "Raportul de acoperire optim",
                "text": "Raportul de acoperire cu varianță minimă $h^{*}$ minimizează $\\mathrm{Var}(\\Delta S-h\\Delta F)$. Ce expresie îl dă și cum este estimat în curs?",
                "options": [
                    "$h^{*}=\\sigma_S/\\sigma_F$, raportul abaterilor standard, calculat direct",
                    "$h^{*}=\\rho$, corelația dintre variațiile expunerii și ale instrumentului de acoperire",
                    "$h^{*}=\\rho\\,\\sigma_S/\\sigma_F$, panta regresiei lui $\\Delta S$ pe $\\Delta F$, estimată prin metoda celor mai mici pătrate (OLS)",
                    "$h^{*}=\\rho^2$, ponderea varianței eliminate prin acoperire"
                ],
                "correctExplanation": "Anulînd derivata, obținem $h^{*}=\\mathrm{Cov}(\\Delta S,\\Delta F)/\\mathrm{Var}(\\Delta F)=\\rho\\,\\sigma_S/\\sigma_F$, adică panta estimată prin metoda celor mai mici pătrate. Ponderea varianței eliminate, $\\rho^2$, este eficiența acoperirii, o mărime diferită.",
                "incorrectExplanation": "Raportul volatilităților ignoră cît de strîns se mișcă împreună cele două prețuri, iar corelația singură ignoră mărimea lor relativă. $\\rho^2$ arată cît de bună este acoperirea, nu cîte contracte trebuie deținute."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Sizing a Hungarian hedge",
                "text": "The hedge ratio of Romanian on Hungarian (HU) monthly price changes is estimated at $h^{*}$ = 0.966, with a bootstrap 95% interval of [0.93; 1.03]. How many megawatts (MW) of Hungarian futures should hedge a 20 MW exposure?",
                "options": [
                    "About 20.7 MW, because 20/0.966 corrects for the lower Hungarian price",
                    "About 19.3 MW, though a one-for-one hedge of 20 MW is statistically as good",
                    "Exactly 19.3 MW; a 20 MW hedge would be rejected by the interval",
                    "About 18.6 MW, applying the lower bound of the interval for safety"
                ],
                "correctExplanation": "20 × 0.966 = 19.3 MW. Because 1 lies inside [0.93; 1.03], a hedge of 20 MW is statistically acceptable too.",
                "incorrectExplanation": "The hedge ratio multiplies the exposure; it does not divide it. A point estimate without its interval is a guess: here the interval contains 1, so the precise 19.3 is not statistically better than 20."
            },
            "ro": {
                "title": "Acoperirea cu contracte din Ungaria",
                "text": "Raportul de acoperire al variațiilor lunare ale prețului din România în funcție de cele din Ungaria (HU) este estimat la $h^{*}$ = 0,966, cu intervalul bootstrap de 95% [0,93; 1,03]. Cîți megawați (MW) de contracte futures din Ungaria acoperă o expunere de 20 MW?",
                "options": [
                    "Circa 20,7 MW, pentru că 20/0,966 corectează prețul mai mic din Ungaria",
                    "Circa 19,3 MW, deși o acoperire integrală, de 20 MW, este la fel de bună din punct de vedere statistic",
                    "Exact 19,3 MW; o acoperire de 20 MW ar fi respinsă de interval",
                    "Circa 18,6 MW, aplicînd din prudență limita inferioară a intervalului"
                ],
                "correctExplanation": "20 × 0,966 = 19,3 MW. Deoarece valoarea 1 se află în intervalul [0,93; 1,03], și o acoperire de 20 MW este acceptabilă statistic.",
                "incorrectExplanation": "Raportul de acoperire înmulțește expunerea, nu o împarte. O estimare punctuală fără interval de încredere este o simplă presupunere: aici intervalul conține valoarea 1, deci cifra de 19,3 nu este statistic mai bună decît 20."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Basis in July 2024",
                "text": "A Romanian supplier hedged July 2024 with baseload futures on the Germany–Luxembourg zone (DE-LU), bought at $F$. July averaged 67.7 EUR per megawatt-hour (EUR/MWh) in Germany and 145.1 in Romania. What was its net cost per MWh?",
                "options": [
                    "$F$ + 77.4 EUR/MWh",
                    "$F$ EUR/MWh, since the future fixed the price",
                    "$F$ − 77.4 EUR/MWh",
                    "145.1 EUR/MWh, as if it were unhedged"
                ],
                "correctExplanation": "It paid 145.1 in Romania and received $67.7-F$ from the future, so its net cost was $145.1-(67.7-F)=F+77.4$ EUR/MWh: the largest monthly basis in the data.",
                "incorrectExplanation": "A cash-settled German future pays the German average minus $F$, not the Romanian one, so the Romania–Germany gap at delivery stays with the firm. The hedge removed the German price risk but left the basis, which here added 77.4 EUR/MWh."
            },
            "ro": {
                "title": "Baza din iulie 2024",
                "text": "Un furnizor din România și-a acoperit luna iulie 2024 cu contracte futures în bandă pe zona Germania–Luxemburg (DE-LU), cumpărate la prețul $F$. Media lunii a fost 67,7 EUR pe megawatt-oră (EUR/MWh) în Germania și 145,1 în România. Cît a plătit net pe MWh?",
                "options": [
                    "$F$ + 77,4 EUR/MWh",
                    "$F$ EUR/MWh, pentru că contractul futures a fixat prețul",
                    "$F$ − 77,4 EUR/MWh",
                    "145,1 EUR/MWh, ca și cum nu s-ar fi acoperit"
                ],
                "correctExplanation": "A plătit 145,1 în România și a primit $67{,}7-F$ din contractul futures, deci costul net a fost $145{,}1-(67{,}7-F)=F+77{,}4$ EUR/MWh: cea mai mare bază lunară din datele cursului.",
                "incorrectExplanation": "Contractul futures german cu decontare financiară plătește media din Germania minus $F$, nu media din România, deci diferența România–Germania de la livrare rămîne la firmă. Acoperirea a eliminat riscul prețului german, dar a lăsat baza, care aici a adăugat 77,4 EUR/MWh."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Pricing the German basis",
                "text": "The monthly basis of Romania against Hungary (HU) has a mean of −2.1 EUR per megawatt-hour (EUR/MWh) and a standard deviation of 4.5; against Germany–Luxembourg (DE-LU) the mean is +13.9, the standard deviation 15.2, and since 2023 the mean is +18.7. How should a supplier quoting a fixed price use these figures?",
                "options": [
                    "Ignore the basis, since its mean is small relative to the price level",
                    "Prefer German futures, because their positive basis lowers the hedged cost",
                    "Treat both hedges as equivalent, since both bases average close to zero",
                    "Price a German hedge at the German forward plus about 19 EUR/MWh, and prefer Hungarian contracts"
                ],
                "correctExplanation": "With $h=1$ the hedged cost is the foreign forward $F^{X}_0$ plus the basis. Against Germany the basis has averaged +18.7 since 2023 and is volatile, so it must be priced in; against Hungary it is small and stable.",
                "incorrectExplanation": "A positive basis means that Romanian prices exceed German ones, so it raises, not lowers, the cost of a German hedge. A mean of +13.9 with a standard deviation of 15.2 is neither small nor close to zero."
            },
            "ro": {
                "title": "Baza față de Germania",
                "text": "Baza lunară a României față de Ungaria (HU) are media −2,1 EUR pe megawatt-oră (EUR/MWh) și abaterea standard 4,5; față de zona Germania–Luxemburg (DE-LU), media este +13,9, abaterea standard 15,2, iar din 2023 media este +18,7. Cum ar trebui să folosească aceste cifre un furnizor care ofertează un preț fix?",
                "options": [
                    "Să ignore baza, pentru că media ei este mică în raport cu nivelul prețului",
                    "Să prefere contractele germane, pentru că baza lor pozitivă reduce costul acoperit",
                    "Să trateze cele două acoperiri ca echivalente, pentru că ambele baze au media apropiată de zero",
                    "Să evalueze o acoperire germană la forward-ul german plus circa 19 EUR/MWh și să prefere contractele din Ungaria"
                ],
                "correctExplanation": "Pentru $h=1$, costul acoperit este forward-ul din străinătate $F^{X}_0$ plus baza. Față de Germania, baza a avut media +18,7 din 2023 și este volatilă, deci trebuie inclusă în ofertă; față de Ungaria este mică și stabilă.",
                "incorrectExplanation": "O bază pozitivă înseamnă că prețul din România îl depășește pe cel german, deci crește, nu reduce, costul unei acoperiri germane. O medie de +13,9 cu abaterea standard 15,2 nu este nici mică, nici apropiată de zero."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Basis and congestion",
                "text": "The standard deviation of the monthly Romania–Germany basis rose from 7.6 EUR per megawatt-hour (EUR/MWh) before 2021 to 18.2 after, although market coupling (Interim Coupling in June 2021, Core flow-based coupling in June 2022) made equal prices more frequent. What is basis risk, in practice?",
                "options": [
                    "The risk that a foreign clearing house defaults on the future",
                    "The risk that the euro–leu exchange rate moves before delivery",
                    "The risk of congestion between bidding zones, which separates their prices",
                    "The risk that the forward premium changes sign from one period to the next"
                ],
                "correctExplanation": "Prices converge only when cross-border lines are not congested and market coupling equalises them; when the lines are congested, prices separate and the basis opens.",
                "incorrectExplanation": "Clearing removes counterparty risk, and power prices are compared in EUR in both zones. The time-varying forward premium is a separate issue: basis risk concerns the gap between two zones' prices at delivery."
            },
            "ro": {
                "title": "Baza și congestia",
                "text": "Abaterea standard a bazei lunare România–Germania a crescut de la 7,6 EUR pe megawatt-oră (EUR/MWh) înainte de 2021 la 18,2 după, deși cuplarea piețelor (Interim Coupling în iunie 2021, cuplarea Core bazată pe fluxuri în iunie 2022) a făcut mai frecvente prețurile egale. Ce este, în practică, riscul de bază?",
                "options": [
                    "Riscul ca o casă de compensație din străinătate să intre în incapacitate de plată",
                    "Riscul ca, pînă la livrare, cursul dintre euro și leu să se modifice",
                    "Riscul de congestie dintre zonele de ofertare, care separă prețurile acestora",
                    "Riscul ca prima forward să își schimbe semnul de la o perioadă la alta"
                ],
                "correctExplanation": "Prețurile se egalizează doar cînd liniile de interconexiune nu sînt congestionate și cuplarea piețelor le aduce la același nivel; cînd liniile sînt congestionate, prețurile se separă și baza crește.",
                "incorrectExplanation": "Casa de compensație elimină riscul de contrapartidă, iar prețurile energiei sînt comparate în EUR în ambele zone. Variația în timp a primei forward este o altă problemă: riscul de bază privește diferența dintre prețurile a două zone la livrare."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Solar capture factor",
                "text": "In 2025 the solar capture factor $f^{\\text{solar}}$ in Romania was 0.596, against 1.045 in 2019. What does this mean for a solar producer?",
                "options": [
                    "Its output sold 59.6 EUR per megawatt-hour (EUR/MWh) below the band price",
                    "Its output sold at about 60% of the band price, 43.7 EUR per megawatt-hour (EUR/MWh) below the band",
                    "Its output sold 4.5% above the band price, as in 2019",
                    "Its output sold at the band price, since the factor only measures volume"
                ],
                "correctExplanation": "The factor is the output-weighted price divided by the simple mean price; 0.596 means each MWh of solar output earned about 60% of the band, 43.7 EUR/MWh less, because so many solar plants now produce in the same hours.",
                "incorrectExplanation": "The factor is a ratio, not a price gap, and it weights prices by output, so it measures value, not volume. Above 1 the profile is worth more than the band (as in 2019); below 1 it is worth less."
            },
            "ro": {
                "title": "Raportul de captare solar",
                "text": "În 2025, raportul de captare al producției solare din România, $f^{\\text{solar}}$, a fost 0,596, față de 1,045 în 2019. Ce înseamnă acest lucru pentru un producător solar?",
                "options": [
                    "Energia lui s-a vîndut cu 59,6 EUR pe megawatt-oră (EUR/MWh) sub prețul benzii",
                    "Energia lui s-a vîndut la circa 60% din prețul benzii, cu 43,7 EUR pe megawatt-oră (EUR/MWh) sub bandă",
                    "Energia lui s-a vîndut cu 4,5% peste prețul benzii, ca în 2019",
                    "Energia lui s-a vîndut la prețul benzii, pentru că factorul măsoară doar volumul"
                ],
                "correctExplanation": "Factorul este prețul ponderat cu producția solară împărțit la media simplă a prețurilor; 0,596 înseamnă că fiecare MWh solar a obținut circa 60% din prețul benzii, cu 43,7 EUR/MWh mai puțin, pentru că foarte multe centrale solare produc acum în aceleași ore.",
                "incorrectExplanation": "Factorul este un raport, nu o diferență de preț, și ponderează prețurile cu producția, deci măsoară valoarea, nu volumul. Peste 1, profilul valorează mai mult decît banda (ca în 2019); sub 1, valorează mai puțin."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Pricing a solar PPA",
                "text": "A supplier serving the national load profile paid a shape factor of 1.066 in 2025 (+7.1 EUR per megawatt-hour, EUR/MWh, over the band), while the solar capture factor was 0.596. A buyer is negotiating a solar power purchase agreement (PPA). On what should the price be based?",
                "options": [
                    "On the band forward adjusted by the solar capture factor, not on the band forward alone",
                    "On the band forward, since the PPA delivers energy over the same year",
                    "On the load-weighted price, since the buyer serves a load profile",
                    "On the peak forward, since solar plants produce during the day"
                ],
                "correctExplanation": "Solar output is concentrated in cheap midday hours, so it is worth much less than the band, and a PPA priced at the band forward would overpay. The band is a poor hedge for both sides: the supplier is under-hedged in expensive hours, the solar producer over-hedged in cheap ones.",
                "incorrectExplanation": "A band contract assumes the same MW in every hour, which neither consumption nor solar output follows. The lecture's rule is to price a solar PPA at the capture factor, which measures what solar output actually earned."
            },
            "ro": {
                "title": "Evaluarea unui PPA solar",
                "text": "Un furnizor care deservește profilul consumului național a avut în 2025 un factor de profil de 1,066 (+7,1 EUR pe megawatt-oră, EUR/MWh, peste bandă), iar raportul de captare solar a fost 0,596. Un cumpărător negociază un contract de achiziție pe termen lung (PPA) pentru un parc solar. Pe ce ar trebui să se bazeze prețul?",
                "options": [
                    "Pe prețul benzii ajustat cu raportul de captare solar, nu pe prețul benzii ca atare",
                    "Pe prețul benzii, pentru că PPA livrează energie în același an",
                    "Pe prețul ponderat cu consumul, pentru că cumpărătorul deservește un profil de consum",
                    "Pe prețul forward de vîrf, pentru că centralele solare produc ziua"
                ],
                "correctExplanation": "Producția solară este concentrată în orele ieftine de la prînz, deci valorează mult mai puțin decît banda, iar un PPA evaluat la prețul benzii ar fi plătit prea scump. Banda acoperă prost ambele părți: furnizorul rămîne subacoperit în orele scumpe, producătorul solar supraacoperit în cele ieftine.",
                "incorrectExplanation": "Un contract în bandă presupune aceeași putere în fiecare oră, ceea ce nu urmează nici consumul, nici producția solară. Regula din curs este evaluarea unui PPA solar la raportul de captare, care măsoară cît a obținut efectiv producția solară."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Building a collar",
                "text": "A Romanian supplier wants protection against high prices at a low cost. Which combination forms the supplier's collar described in the lecture?",
                "options": [
                    "Sell a call at $K_c$ and buy a put at $K_p$",
                    "Buy a call and a put at the same strike $K=F$",
                    "Buy a put at $K_p$ and sell a forward",
                    "Buy a call at $K_c$ and sell a put at $K_p \\lt K_c$"
                ],
                "correctExplanation": "The supplier buys a call (the cap) and finances it by selling a put, giving up the gain below $K_p$; its effective price is $\\max(K_p,\\min(F_T,K_c))+c-p$. A producer does the reverse.",
                "incorrectExplanation": "Selling a call and buying a put is the producer's collar; buying a call and a put at the same strike is a costly bet on volatility, not a cheap hedge. The point of the collar is that the put premium pays for most of the call."
            },
            "ro": {
                "title": "Construcția unui collar",
                "text": "Un furnizor din România vrea protecție împotriva prețurilor mari, cu un cost redus. Ce combinație formează collar-ul furnizorului descris în curs?",
                "options": [
                    "Vinde o opțiune call la $K_c$ și cumpără o opțiune put la $K_p$",
                    "Cumpără o opțiune call și una put la același preț de exercitare $K=F$",
                    "Cumpără o opțiune put la $K_p$ și vinde forward",
                    "Cumpără o opțiune call la $K_c$ și vinde o opțiune put la $K_p \\lt K_c$"
                ],
                "correctExplanation": "Furnizorul cumpără o opțiune call (plafonul) și o finanțează vînzînd o opțiune put, renunțînd la cîștigul de sub $K_p$; prețul lui efectiv este $\\max(K_p,\\min(F_T,K_c))+c-p$. Producătorul face invers.",
                "incorrectExplanation": "Vînzarea unei opțiuni call și cumpărarea unei opțiuni put formează collar-ul producătorului; cumpărarea ambelor opțiuni la același preț de exercitare este un pariu costisitor pe volatilitate, nu o acoperire ieftină. Rostul collar-ului este că prima opțiunii put plătește cea mai mare parte a opțiunii call."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Yearly cost of a cap",
                "text": "Under the Black-76 model, a cap at 1.1$F$ on the 2027 Romanian band, with strike 162.9 EUR per megawatt-hour (EUR/MWh), costs 0.63 EUR/MWh. What is its premium for 1 megawatt (MW) over the 8,760 hours of 2027?",
                "options": [
                    "About 630 EUR",
                    "About 3,767 EUR",
                    "About 5,519 EUR",
                    "About 39,858 EUR"
                ],
                "correctExplanation": "1 MW over 8,760 hours is 8,760 MWh, so the premium is $0.63\\times 8{,}760\\approx 5{,}519$ EUR, the figure of the lecture.",
                "incorrectExplanation": "The premium is quoted per MWh and must be multiplied by the energy of the year; 3,767 EUR is the floor at 0.9$F$ (0.43 EUR/MWh), 39,858 EUR the at-the-money option (4.55 EUR/MWh), and 630 EUR ignores the number of hours."
            },
            "ro": {
                "title": "Costul anual al unui plafon",
                "text": "Cu modelul Black-76, un plafon la 1,1$F$ pe banda din 2027 din România, cu prețul de exercitare 162,9 EUR pe megawatt-oră (EUR/MWh), costă 0,63 EUR/MWh. Cît este prima lui pentru 1 megawatt (MW) pe cele 8 760 de ore ale anului 2027?",
                "options": [
                    "Circa 630 EUR",
                    "Circa 3 767 EUR",
                    "Circa 5 519 EUR",
                    "Circa 39 858 EUR"
                ],
                "correctExplanation": "1 MW pe 8 760 de ore înseamnă 8 760 MWh, deci prima este $0{,}63\\times 8\\,760\\approx 5\\,519$ EUR, valoarea din curs.",
                "incorrectExplanation": "Prima este cotată pe MWh și trebuie înmulțită cu energia anului; 3 767 EUR corespunde floor-ului la 0,9$F$ (0,43 EUR/MWh), 39 858 EUR opțiunii la bani (4,55 EUR/MWh), iar 630 EUR ignoră numărul de ore."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "At-the-money parity",
                "text": "With the Black-76 model, $F$ = 148.12 EUR per megawatt-hour (EUR/MWh), $T$ = 45 days, $r$ = 2.44% (the euro short-term rate, €STR) and $\\sigma$ = 0.220, an at-the-money call ($K=F$) costs 4.55 EUR/MWh. What does the put with the same strike cost?",
                "options": [
                    "About 0.43 EUR/MWh",
                    "4.55 EUR/MWh, by put–call parity",
                    "About 9.10 EUR/MWh",
                    "About 0.63 EUR/MWh"
                ],
                "correctExplanation": "Put–call parity gives $C-P=e^{-rT}(F-K)$, which is zero when $K=F$, so the put also costs 4.55 EUR/MWh.",
                "incorrectExplanation": "0.43 is the floor at 0.9$F$ and 0.63 the cap at 1.1$F$: out-of-the-money options are cheaper. At the money a call and a put on a forward have equal value; doubling the call premium confuses the put with a call-plus-put combination."
            },
            "ro": {
                "title": "Paritatea put–call la bani",
                "text": "Cu modelul Black-76, $F$ = 148,12 EUR pe megawatt-oră (EUR/MWh), $T$ = 45 de zile, $r$ = 2,44% (rata pe termen scurt a euro, €STR) și $\\sigma$ = 0,220, o opțiune call la bani ($K=F$) costă 4,55 EUR/MWh. Cît costă opțiunea put cu același preț de exercitare?",
                "options": [
                    "Circa 0,43 EUR/MWh",
                    "4,55 EUR/MWh, din paritatea put–call",
                    "Circa 9,10 EUR/MWh",
                    "Circa 0,63 EUR/MWh"
                ],
                "correctExplanation": "Paritatea put–call dă $C-P=e^{-rT}(F-K)$, care este zero cînd $K=F$, deci și opțiunea put costă 4,55 EUR/MWh.",
                "incorrectExplanation": "0,43 este prețul pragului minim la 0,9$F$, iar 0,63 al plafonului la 1,1$F$: opțiunile în afara banilor sînt mai ieftine. La bani, opțiunile call și put pe un forward au aceeași valoare; dublarea primei confundă opțiunea put cu o combinație call plus put."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "Which volatility to use",
                "text": "Three volatility estimates from real data give 0.220 (Romanian yearly forwards, 49 pairs of auction days), 0.499 (the January 2027 gas future on the Dutch Title Transfer Facility, TTF) and 0.668 (the realised monthly average against the forward bought before it). Why do they differ so much?",
                "options": [
                    "A year averages 8,760 hours and is far calmer than a month, and gas had its own crisis in 2026",
                    "Two of the three estimates contain errors, and only one of them is correct",
                    "Volatility is the same for all contracts; the difference is pure sampling noise",
                    "The 0.220 estimate ignores the time between auctions, which inflates the others"
                ],
                "correctExplanation": "Each estimate refers to a different underlying: a yearly band, a gas month and a power month. The volatility must match the contract being hedged: year, quarter or month.",
                "incorrectExplanation": "The estimates are not mistakes; the yearly one divides the squared log changes by the time between auctions, precisely because auctions are irregular. With no free implied volatility for Romania, the choice is a modelling decision, and generalised autoregressive conditional heteroskedasticity (GARCH) models (Lecture 3) can forecast it."
            },
            "ro": {
                "title": "Ce volatilitate folosim",
                "text": "Trei estimări ale volatilității pe date reale dau 0,220 (contractele forward anuale din România, 49 de perechi de zile cu licitații), 0,499 (contractul futures pe gaze pentru ianuarie 2027 la Title Transfer Facility, TTF, hubul olandez) și 0,668 (media lunară realizată față de prețul forward cumpărat înainte). De ce diferă atît de mult?",
                "options": [
                    "Un an este media a 8 760 de ore și este mult mai stabil decît o lună, iar gazele trec printr-o criză proprie în 2026",
                    "Două dintre cele trei estimări sînt greșite și doar una dintre ele este corectă",
                    "Volatilitatea este aceeași pentru toate contractele; diferența este doar zgomot de eșantionare",
                    "Estimarea de 0,220 ignoră timpul dintre licitații, ceea ce le umflă pe celelalte"
                ],
                "correctExplanation": "Fiecare estimare se referă la alt activ suport: o bandă anuală, o lună de gaze și o lună de energie electrică. Volatilitatea trebuie să corespundă contractului acoperit: an, trimestru sau lună.",
                "incorrectExplanation": "Estimările nu sînt greșite; cea anuală împarte pătratele variațiilor logaritmice la timpul dintre licitații, tocmai pentru că licitațiile sînt neregulate. Pentru România nu există o volatilitate implicită disponibilă gratuit, deci alegerea este o decizie de modelare, iar modelele de heteroscedasticitate condiționată autoregresivă generalizată (GARCH) din cursul 3 o pot prognoza."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The Samuelson effect",
                "text": "From 1 Nov 2025 to 31 Oct 2026 the December 2026 gas future on the Dutch Title Transfer Facility (TTF) had an annualised volatility of 63%, and the May 2027 contract 48%. What follows for option pricing?",
                "options": [
                    "Use the average of the two, about 55%, for any TTF option",
                    "Distant contracts are riskier, so long-dated options need a higher volatility",
                    "The gap is temporary: in 2022 both were near 66%, so a single number is enough",
                    "An option on a contract close to delivery needs a higher volatility"
                ],
                "correctExplanation": "Near contracts react more to news, because a shock to today's supply affects the near month fully and the distant month only partly (Samuelson, 1965). The same underlying has a higher volatility the closer it is to delivery.",
                "incorrectExplanation": "The ranking is the reverse of the intuition that distant means riskier. That both contracts were near 66% at the peak of the 2022 crisis does not justify one number in normal times; averaging hides exactly the term structure that matters."
            },
            "ro": {
                "title": "Efectul Samuelson",
                "text": "Între 1 noiembrie 2025 și 31 octombrie 2026, contractul futures pe gaze pentru decembrie 2026 la Title Transfer Facility (TTF), hubul olandez, a avut o volatilitate anualizată de 63%, iar cel pentru mai 2027 de 48%. Ce rezultă pentru evaluarea opțiunilor?",
                "options": [
                    "Se folosește media celor două, circa 55%, pentru orice opțiune TTF",
                    "Contractele îndepărtate sînt mai riscante, deci opțiunile cu scadență lungă cer o volatilitate mai mare",
                    "Diferența este temporară: în 2022 ambele erau în jur de 66%, deci o singură valoare este suficientă",
                    "O opțiune pe un contract apropiat de livrare cere o volatilitate mai mare"
                ],
                "correctExplanation": "Contractele apropiate de livrare reacționează mai puternic la știri, pentru că un șoc asupra ofertei de azi afectează complet luna apropiată și doar parțial pe cea îndepărtată (Samuelson, 1965). Același activ suport are o volatilitate cu atît mai mare cu cît este mai aproape de livrare.",
                "incorrectExplanation": "Ordinea este inversă intuiției că un contract îndepărtat ar fi mai riscant. Faptul că ambele contracte erau în jur de 66% în vîrful crizei din 2022 nu justifică o singură valoare în perioade normale; media ascunde exact structura la termen care contează."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Delta of a cap",
                "text": "Under the Black-76 model, a cap at 1.1$F$ on the 2027 Romanian band has a delta of 0.116, while the at-the-money call has a delta of 0.514. How does the bank that sold the cap hedge it?",
                "options": [
                    "It buys 1 megawatt-hour (MWh) forward per MWh of cap and holds it to expiry",
                    "It buys 0.514 megawatt-hours (MWh) forward per MWh of cap, the at-the-money delta",
                    "It holds about 0.116 megawatt-hours (MWh) forward per MWh of cap and rebalances as the price moves",
                    "It sells 0.116 megawatt-hours (MWh) forward per MWh of cap, since it is short the call"
                ],
                "correctExplanation": "Delta, $e^{-rT}\\Phi(d_1)$, is the forward quantity that offsets the option: the cap behaves like about a tenth of a MWh forward. The seller is short the call, so it buys delta and adjusts it as $F$ moves.",
                "incorrectExplanation": "A full forward over-hedges an out-of-the-money cap, and the at-the-money delta does not apply to a strike 10% above $F$. A short call loses when prices rise, so the offset is a bought, not a sold, forward."
            },
            "ro": {
                "title": "Delta unui plafon",
                "text": "În modelul Black-76, un plafon la 1,1$F$ pe banda pentru 2027 din România are delta 0,116, iar opțiunea call la bani are delta 0,514. Cum se acoperă banca ce a vîndut plafonul?",
                "options": [
                    "Cumpără forward 1 megawatt-oră (MWh) pentru fiecare MWh de plafon și îl păstrează pînă la scadență",
                    "Cumpără forward 0,514 megawatt-oră (MWh) pentru fiecare MWh de plafon, delta opțiunii la bani",
                    "Deține forward circa 0,116 megawatt-oră (MWh) pentru fiecare MWh de plafon și ajustează poziția cînd prețul se mișcă",
                    "Vinde forward 0,116 megawatt-oră (MWh) pentru fiecare MWh de plafon, pentru că are o poziție scurtă pe call"
                ],
                "correctExplanation": "Delta, $e^{-rT}\\Phi(d_1)$, este cantitatea de forward care compensează opțiunea: plafonul se comportă ca aproximativ o zecime de MWh forward. Vînzătorul are o poziție scurtă pe call, deci cumpără delta și o ajustează periodic, pe măsură ce $F$ se mișcă.",
                "incorrectExplanation": "Un forward integral supraacoperă un plafon în afara banilor, iar delta opțiunii la bani nu se aplică unui preț de exercitare cu 10% peste $F$. Poziția scurtă pe call pierde cînd prețul crește, deci compensarea se face cumpărînd, nu vînzînd forward."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "Net cost of the collar",
                "text": "For the 2027 Romanian band, $F$ = 148.1 EUR per megawatt-hour (EUR/MWh). A cap (a call) at 1.1$F$ = 162.9 costs 0.63 EUR/MWh and a floor (a put) at 0.9$F$ = 133.3 costs 0.43 EUR/MWh. A supplier builds a collar: it buys the cap and sells the floor. What is its net premium?",
                "options": [
                    "About 1.06 EUR/MWh",
                    "About 0.20 EUR/MWh",
                    "About 0.63 EUR/MWh",
                    "About −0.20 EUR/MWh: the supplier is paid"
                ],
                "correctExplanation": "The supplier pays 0.63 and receives 0.43, so the collar costs $0.63-0.43=0.20$ EUR/MWh net, as in the lecture. In exchange it gives up the gain from prices below 133.3.",
                "incorrectExplanation": "The sold put is a receipt, not a cost, so the two premiums are subtracted, not added; and since the cap is dearer than the floor, the supplier still pays a small net amount."
            },
            "ro": {
                "title": "Costul net al collar-ului",
                "text": "Pentru banda din 2027 din România, $F$ = 148,1 EUR pe megawatt-oră (EUR/MWh). Un plafon (o opțiune call) la 1,1$F$ = 162,9 costă 0,63 EUR/MWh, iar un floor (o opțiune put) la 0,9$F$ = 133,3 costă 0,43 EUR/MWh. Un furnizor construiește un collar: cumpără plafonul și vinde floor-ul. Cît este prima netă?",
                "options": [
                    "Circa 1,06 EUR/MWh",
                    "Circa 0,20 EUR/MWh",
                    "Circa 0,63 EUR/MWh",
                    "Circa −0,20 EUR/MWh: furnizorul încasează"
                ],
                "correctExplanation": "Furnizorul plătește 0,63 și încasează 0,43, deci collar-ul costă net $0{,}63-0{,}43=0{,}20$ EUR/MWh, ca în curs. În schimb, renunță la cîștigul de sub 133,3.",
                "incorrectExplanation": "Opțiunea put vîndută este o încasare, nu un cost, deci cele două prime se scad, nu se adună; și cum plafonul este mai scump decît floor-ul, furnizorul plătește totuși o sumă netă mică."
            }
        },
        {
            "correct": 2,
            "en": {
                "title": "Case study: forward hedge",
                "text": "In the case study a supplier sold 1 megawatt (MW) flat for 2026. Over the 10 months delivered to October 2026, buying at the spot cost 1,002,956 EUR per MW, while the 100% forward hedge, at a volume-weighted average price (VWAP) of 111.70 EUR per megawatt-hour (EUR/MWh), cost 814,946 EUR. What did the forward achieve?",
                "options": [
                    "It saved 188,010 EUR per MW but left the monthly cost as volatile as the spot",
                    "It cost 188,010 EUR per MW more than the spot, the usual price of certainty",
                    "It saved 188,010 EUR per MW and removed all month-to-month variation",
                    "It saved 94,005 EUR per MW, half of the gap, because only half the volume was hedged"
                ],
                "correctExplanation": "1,002,956 − 814,946 = 188,010 EUR per MW, and the monthly cost was fixed at 111.7 (standard deviation 0.0 against 44.4 for the spot). In 2026 prices rose after the hedge was placed, so the forward cut both cost and risk.",
                "incorrectExplanation": "The forward fixes the price in every month, so its cost does not vary. The saving is not a general rule: in a year of falling prices the forward costs more than the spot, which is why the hedged share is set by policy."
            },
            "ro": {
                "title": "Studiul de caz: acoperirea forward",
                "text": "În studiul de caz, un furnizor a vîndut 1 megawatt (MW) în bandă pentru 2026. În cele 10 luni livrate pînă în octombrie 2026, cumpărarea pe spot a costat 1 002 956 EUR pe MW, iar acoperirea integrală cu forward, la un preț mediu ponderat cu volumul (VWAP) de 111,70 EUR pe megawatt-oră (EUR/MWh), a costat 814 946 EUR. Ce a obținut forward-ul?",
                "options": [
                    "A economisit 188 010 EUR pe MW, dar costul lunar a rămas la fel de volatil ca spotul",
                    "A costat cu 188 010 EUR pe MW mai mult decît spotul, prețul obișnuit al certitudinii",
                    "A economisit 188 010 EUR pe MW și a eliminat complet variația de la o lună la alta",
                    "A economisit 94 005 EUR pe MW, jumătate din diferență, pentru că doar jumătate din volum a fost acoperit"
                ],
                "correctExplanation": "1 002 956 − 814 946 = 188 010 EUR pe MW, iar costul lunar a fost fixat la 111,7 (abaterea standard 0,0, față de 44,4 pentru spot). În 2026, prețurile au crescut după acoperire, deci forward-ul a redus atît costul, cît și riscul.",
                "incorrectExplanation": "Forward-ul fixează prețul în fiecare lună, deci costul lui nu variază. Economia nu este o regulă generală: într-un an cu prețuri în scădere, forward-ul costă mai mult decît spotul; de aceea, ponderea acoperită se stabilește prin politică."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "Case study: monthly caps",
                "text": "In the same 2026 case study, monthly caps bought on 15 Dec 2025 with a strike of 120.16 EUR per megawatt-hour (EUR/MWh) cost an average premium of 20.4 EUR/MWh a month and paid out in 5 of the 10 months. What was their effect?",
                "options": [
                    "They lost money, since the premium was paid even in months when the cap paid nothing",
                    "They gave the same result as the forward, because both fix the purchase price",
                    "They cut the worst month to the strike of 120.16, since the cap fully offsets prices above it",
                    "They saved 27,936 EUR per megawatt (MW) net and cut the worst month from 239.3 to 148.5 EUR/MWh"
                ],
                "correctExplanation": "Although the premium was paid every month, the caps saved 27,936 EUR per MW net and cut the worst month from 239.3 to 148.5 EUR/MWh, with a monthly standard deviation of 13.9 against 44.4 for the spot.",
                "incorrectExplanation": "The cap limits the price at the strike, but its premium comes on top, so the worst month cost 148.5, above the strike. Caps cut risk at a premium but, unlike the forward, keep the market price when it is below the strike, so the two strategies differ."
            },
            "ro": {
                "title": "Studiul de caz: plafoanele lunare",
                "text": "În același studiu de caz pentru 2026, plafoanele lunare cumpărate la 15 decembrie 2025, cu prețul de exercitare de 120,16 EUR pe megawatt-oră (EUR/MWh), au avut o primă medie de 20,4 EUR/MWh pe lună și s-au exercitat în 5 din cele 10 luni. Ce efect au avut?",
                "options": [
                    "Au adus pierderi, pentru că prima s-a plătit și în lunile în care plafonul nu s-a exercitat",
                    "Au dat același rezultat ca forward-ul, pentru că ambele fixează prețul de cumpărare",
                    "Au redus cea mai scumpă lună la prețul de exercitare de 120,16, pentru că plafonul compensează integral prețurile mai mari",
                    "Au adus o economie netă de 27 936 EUR pe megawatt (MW) și au redus cea mai scumpă lună de la 239,3 la 148,5 EUR/MWh"
                ],
                "correctExplanation": "Deși prima s-a plătit în fiecare lună, plafoanele au adus o economie netă de 27 936 EUR pe MW și au redus cea mai scumpă lună de la 239,3 la 148,5 EUR/MWh, cu o abatere standard lunară de 13,9, față de 44,4 pentru spot.",
                "incorrectExplanation": "Plafonul limitează prețul la nivelul prețului de exercitare, dar prima se adaugă, deci cea mai scumpă lună a costat 148,5, peste prețul de exercitare. Plafoanele reduc riscul în schimbul unei prime, dar, spre deosebire de forward, păstrează prețul pieței cînd acesta este sub prețul de exercitare, deci cele două strategii diferă."
            }
        },
        {
            "correct": 0,
            "en": {
                "title": "The producer sells forward",
                "text": "In 2025, 101 auctions of the Romanian electricity and gas market operator (OPCOM) sold the band at a volume-weighted average price (VWAP) of 102.1 EUR per megawatt-hour (EUR/MWh), while the spot averaged 108.2. What did selling forward cost a producer, and why might it still sell forward?",
                "options": [
                    "About 52,797 EUR per megawatt (MW) a year; lenders value predictable cash flows",
                    "About 187.9 EUR/MWh, as in 2022; it should stop selling forward",
                    "Nothing, since a forward is always priced at the expected spot",
                    "About 894,000 EUR per megawatt (MW), the full value of its output"
                ],
                "correctExplanation": "Selling at 102.1 instead of 108.2 brought 6.0 EUR/MWh less, or 52,797 EUR per MW-year: the price of a fixed revenue. A producer with debt should sell forward even when it expects higher prices, because lenders pay for predictability.",
                "incorrectExplanation": "187.9 EUR/MWh was the cost in 2022, and 894,000 EUR is the whole revenue of 1 MW at 102.1, not the gap. Ex post the forward can end above or below the spot; a hedge is judged by the risk it removed."
            },
            "ro": {
                "title": "Producătorul vinde forward",
                "text": "În 2025, 101 licitații ale operatorului pieței de energie electrică și de gaze naturale din România (OPCOM) au vîndut banda la un preț mediu ponderat cu volumul (VWAP) de 102,1 EUR pe megawatt-oră (EUR/MWh), iar media spot a fost 108,2. Cît l-a costat pe un producător vînzarea forward și de ce ar putea totuși să vîndă forward?",
                "options": [
                    "Circa 52 797 EUR pe megawatt (MW) și an; creditorii răsplătesc fluxurile de numerar previzibile",
                    "Circa 187,9 EUR/MWh, ca în 2022; ar trebui să renunțe la vînzarea forward",
                    "Nimic, pentru că un forward are întotdeauna prețul spot așteptat",
                    "Circa 894 000 EUR pe megawatt (MW), valoarea întregii producții"
                ],
                "correctExplanation": "Vînzarea la 102,1 în loc de 108,2 a adus cu 6,0 EUR/MWh mai puțin, adică 52 797 EUR pe MW și an: prețul unui venit sigur. Un producător îndatorat ar trebui să vîndă forward chiar dacă se așteaptă la prețuri mai mari, pentru că creditorii răsplătesc previzibilitatea.",
                "incorrectExplanation": "187,9 EUR/MWh a fost costul din 2022, iar 894 000 EUR este întregul venit al unui MW la 102,1, nu diferența. Ex post, forward-ul poate fi peste sau sub spot; o acoperire se judecă după riscul eliminat."
            }
        },
        {
            "correct": 1,
            "en": {
                "title": "A hedging policy",
                "text": "Which set of rules matches the hedging policy proposed at the end of the lecture?",
                "options": [
                    "Hedge all volume when traders expect prices to rise and none otherwise, adjusting the share each month to the price outlook",
                    "Use forwards of the Romanian electricity and gas market operator (OPCOM) first, then Hungarian, then German futures; buy in layers over 12–24 months; keep a liquidity buffer for margin calls",
                    "Use German futures first for their liquidity, buy the whole year in a single auction, and cover the entire volume with caps",
                    "Let traders choose instruments and the hedged share freely, and report only the realised profit or loss of the hedge"
                ],
                "correctExplanation": "The policy sets the hedged share by rule (e.g. 60–80% bought in layers), ranks instruments by basis risk, buys caps for the tail only, keeps cash for margins, and limits the open position and value-at-risk (VaR). The board approves it, traders execute it, risk management measures it.",
                "incorrectExplanation": "A hedged share chosen by a price view turns hedging into speculation. German futures carry a large basis, a single auction can move a thin market, and caps on all volume are expensive; reports should show the hedged cost and its variance, not only ex-post profit."
            },
            "ro": {
                "title": "Politica de acoperire",
                "text": "Ce set de reguli corespunde politicii de acoperire propuse la finalul cursului?",
                "options": [
                    "Acoperirea întregului volum cînd traderii se așteaptă la creșteri de preț și a niciunei cantități în rest, cu ponderea ajustată lunar după perspectiva prețurilor",
                    "Întîi forward-uri ale operatorului pieței de energie electrică și de gaze naturale din România (OPCOM), apoi contracte futures din Ungaria, apoi din Germania; cumpărare eșalonată pe 12–24 de luni; rezervă de lichiditate pentru apelurile în marjă",
                    "Întîi contracte futures germane, pentru lichiditatea lor, cumpărarea întregului an într-o singură licitație și acoperirea întregului volum cu plafoane",
                    "Traderii aleg liber instrumentele și ponderea acoperită, iar raportarea arată doar profitul sau pierderea realizată din acoperire"
                ],
                "correctExplanation": "Politica stabilește ponderea acoperită printr-o regulă (de exemplu 60–80%, eșalonat), ordonează instrumentele după riscul de bază, folosește plafoane doar pentru valorile extreme, păstrează lichiditate pentru marje și limitează poziția deschisă și valoarea expusă la risc (VaR). Consiliul aprobă politica, traderii o execută, departamentul de risc o măsoară.",
                "incorrectExplanation": "O pondere acoperită aleasă după o opinie despre prețuri transformă acoperirea în speculație. Contractele germane au o bază mare, o singură licitație poate mișca o piață cu lichiditate redusă, iar plafoanele pe tot volumul sînt scumpe; raportarea trebuie să arate costul acoperit și varianța lui, nu doar profitul ex post."
            }
        },
        {
            "correct": 3,
            "en": {
                "title": "The summer 2024 spike",
                "text": "In summer 2024 the Romanian third-quarter baseload contract was bought at 90.0 EUR per megawatt-hour (EUR/MWh) and delivered at 127.4; July alone averaged 145.1, and the most expensive hour cost 916.7 EUR/MWh on 18 Jul 2024 at 20:00 Central European Time (CET). What does this episode illustrate?",
                "options": [
                    "The risk that producers bear when prices fall after they sell forward",
                    "That forward prices systematically overstate the realised spot",
                    "That hourly spikes do not matter for a buyer of a monthly band",
                    "The upside price risk of unhedged buyers, the mirror image of the producers' risk"
                ],
                "correctExplanation": "Buyers that had fixed the third quarter at 90.0 paid far less than the 127.4 realised, while unhedged buyers bore the spike. A hedge transfers value between the two sides of the market.",
                "incorrectExplanation": "Here the spot ended above the forward, so the loss fell on unhedged buyers, not on producers, and one episode shows no systematic bias in either direction. Hourly spikes feed into the monthly average that unhedged buyers pay."
            },
            "ro": {
                "title": "Saltul de preț din vara lui 2024",
                "text": "În vara lui 2024, contractul în bandă pentru trimestrul al treilea s-a tranzacționat în România la 90,0 EUR pe megawatt-oră (EUR/MWh), iar media spot realizată a fost 127,4; numai în iulie, 145,1, iar ora cea mai scumpă a costat 916,7 EUR/MWh, pe 18 iulie 2024, la ora 20:00, ora Europei Centrale (CET). Ce ilustrează acest episod?",
                "options": [
                    "Riscul pe care îl suportă producătorii cînd prețul scade după ce au vîndut forward",
                    "Faptul că prețurile forward supraestimează sistematic spotul realizat",
                    "Faptul că salturile orare de preț nu contează pentru cumpărătorul unei benzi lunare",
                    "Riscul de creștere a prețului pentru cumpărătorii neacoperiți, imaginea în oglindă a riscului producătorilor"
                ],
                "correctExplanation": "Cumpărătorii care fixaseră trimestrul al treilea la 90,0 au plătit mult mai puțin decît media realizată de 127,4, în timp ce cumpărătorii neacoperiți au suportat saltul. Acoperirea transferă valoare între cele două părți ale pieței.",
                "incorrectExplanation": "Aici spotul a depășit forward-ul, deci pierderea a revenit cumpărătorilor neacoperiți, nu producătorilor, iar un singur episod nu arată o deplasare sistematică în vreo direcție. Salturile orare intră în media lunară pe care o plătesc cumpărătorii neacoperiți."
            }
        }
    ]
};
