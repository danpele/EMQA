<!--
Versiunea web a Cursului 4 (RO). Construită în web/L4_ro.html de lectures/common/build_web_lecture.py (formatul: docstring-ul scriptului).
Hash-urile slide-urilor: python3 build_web_lecture.py 4 --frames
-->

## @intro

O companie energetică ce cumpără sau vinde zilnic energie electrică nu pierde bani pentru că prețurile sînt mari, ci pentru că prețul de mîine diferă de cel pe care și l-a bugetat azi. Un furnizor care cumpără 100 de megawați (MW) în bandă pe piața pentru ziua următoare (PZU) din România pierde 2 400 de euro (EUR) pentru fiecare EUR pe megawatt-oră (EUR/MWh) cu care prețul depășește bugetul. Cursul de față răspunde la trei întrebări: cît de mare poate fi această pierdere într-o zi proastă, cît de des vine o asemenea zi și cum transformă compania răspunsul în limite, rezerve de numerar și garanții bancare.

Cele două răspunsuri consacrate sînt valoarea la risc (VaR, *value-at-risk*), o cuantilă ridicată a pierderii de mîine, și deficitul așteptat (ES, *expected shortfall*), pierderea medie dincolo de această cuantilă. În cursul 1 am anunțat că vom arăta de ce repartiția normală subestimează zilele de criză; aici o facem pe prețuri reale. Estimăm VaR și ES prin patru metode pe prețurile PZU din România, între 1 ianuarie 2015 și 31 octombrie 2026, verificăm fiecare metodă zi de zi pe aproape zece ani (testare retrospectivă, *backtesting*) și urmărim apoi aceleași cuantile în marjele cerute de bursă, în garanția cerută de operatorul pieței și în limitele de poziție exprimate în MW.

Datele sînt reale și descărcate: prețul de bază pentru ziua următoare din România și din zona Germania–Luxemburg, consumul național al României, contractul futures pe țițeiul Brent și prețul gazelor la hubul olandez. Cursul se încheie cu un studiu de caz despre creșterea prețurilor din toamna anului 2026, în care pericolul real a fost lipsa de lichidități, nu VaR zilnică.

@goals
- **Măsurați** riscul de preț al unei poziții pe piața de energie cu VaR și ES, definite prin cuantilele repartiției pierderilor, și explicați de ce repartiția normală subestimează zilele de criză.
- **Estimați** VaR și ES prin patru metode pe prețurile din România: simularea istorică, repartițiile normală și Student-t, simularea istorică filtrată și teoria valorilor extreme.
- **Verificați** un model de risc pe datele care au urmat, cu testele Kupiec și Christoffersen, semaforul Basel și un test pentru ES.
- **Transformați** cuantilele în decizii: limite de poziție, marje la bursă și garanția pentru PZU, pentru un furnizor, un producător și un trader.

# Riscul de preț: pierderi, cuantile, VaR și ES

Riscul unei poziții pe piața de energie se află în variația zilnică a prețului, iar VaR și ES sînt două moduri de a rezuma coada nefavorabilă a acestei variații. Secțiunea definește pierderea și cele două măsuri de risc și arată, pe datele din România, de ce eșuează o limită calculată cu repartiția normală.

## Lucrăm numai cu date reale: prețurile și pozițiile analizate {h=cdfe1810}

Seria principală este prețul de bază de pe PZU din România (RO), administrată de operatorul pieței de energie electrică și de gaze naturale din România (OPCOM); pentru comparație folosim prețul din zona de ofertare Germania–Luxemburg (DE-LU), de la bursa europeană de energie EPEX SPOT (EPEX). Ambele provin de la Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E), prin energy-charts.info, portalul de date al Institutului Fraunhofer pentru Sisteme de Energie Solară (ISE), cu frecvență zilnică și orară. Consumul național al României, de la ENTSO-E (date Transelectrica), dă profilul orar al portofoliului unui furnizor. Alte două serii arată cum se transformă riscul în numerar: contractul futures pe țițeiul Brent cu scadența cea mai apropiată, un contract cu marjă, de pe Yahoo Finance (BZ=F), și prețul lunar al gazelor la hubul olandez Title Transfer Facility (TTF), din Pink Sheet-ul Băncii Mondiale.

Datele acoperă intervalul 1 ianuarie 2015 – 31 octombrie 2026, ultima lună completă, și au fost descărcate la 4 noiembrie 2026. Prețul zilnic este media prețurilor zilei de livrare, după ora Europei Centrale (CET). Cele cinci zile lipsă din seria prețului din România rămîn lipsă, iar variațiile vecine cu ele nu se calculează. Testarea retrospectivă acoperă fiecare zi din intervalul 1 ianuarie 2017 – 31 octombrie 2026, adică 3 587 de zile valide, iar fiecare prognoză folosește numai datele disponibile pînă în ziua precedentă, exact cum ar lucra un birou de risc.

## Riscul stă în variația zilnică a prețului: mică pînă în 2021, mare după {h=a0ad287d}

Variabila care determină pierderea este variația prețului zilnic de bază de la o zi la alta, $X_t=P_t-P_{t-1}$, în EUR/MWh, unde $P_t$ este prețul de bază al zilei $t$. Prețul energiei electrice poate fi negativ, de aceea lucrăm cu variații în euro, nu cu randamente logaritmice, care nu sînt definite pentru un preț negativ.

Graficul arată că mărimea variațiilor nu este stabilă. Pînă în 2021 variațiile zilnice sînt mici; odată cu criza energetică devin foarte mari și rămîn, și după aceea, mai mari decît înainte. Cea mai mare creștere din eșantion este de 260,77 EUR/MWh, la 11 iulie 2022, iar cea mai mare scădere de −166,59 EUR/MWh, la 24 decembrie 2021. Pentru o poziție de 100 MW în bandă, adică 2 400 MWh pe zi, fiecare EUR/MWh de variație modifică rezultatul zilei cu 2 400 EUR.

@practice un furnizor care cumpără zilnic 100 MW în bandă pe PZU și își bugetează costul la prețul de ieri pierde 2 400 EUR pentru fiecare creștere de 1 EUR/MWh.

@chart price_changes
Variația zilnică a prețului de bază de pe PZU din România, în EUR/MWh, 2015–2026.

## Valoarea la risc este o cuantilă a pierderii de mîine {h=593ebad0}

VaR este pierderea depășită doar într-o proporție mică de zile, aleasă dinainte, de exemplu o zi din o sută. Pentru un cumpărător cu o poziție de $Q$ MW în bandă, pierderea zilei $t$ și VaR sînt

$$ L_t = Q\cdot 24\cdot X_t, \qquad \text{VaR}_{\alpha,t}=\min\{\ell:\ \Pr(L_t\le \ell\mid\mathcal F_{t-1})\ge\alpha\} $$ {#eq:var}

unde $L_t$ este pierderea în EUR, $Q$ poziția în MW (pentru 100 MW în bandă, $Q\cdot 24$ = 2 400 MWh pe zi), $X_t$ variația prețului în EUR/MWh, $\alpha$ nivelul de încredere, 0,95 sau 0,99, iar $\mathcal F_{t-1}$ informația disponibilă pînă în ziua $t-1$, adică prețurile cunoscute la ora 12:00 CET, la închiderea licitației. VaR este deci cuantila de ordin $\alpha$ a pierderii, condiționată de ceea ce se știe în momentul ofertării.

Pe ultimele 365 de zile din România, cuantila de 99% a lui $X_t$ este 86,63 EUR/MWh, ceea ce înseamnă, pentru 100 MW, o VaR$_{0,99}$ de 207 922 EUR; cuantila de 95% este 50,39 EUR/MWh. VaR nu spune însă cît de mare este pierderea în cele mai proaste 1% dintre zile. Ea este un prag, nu o medie, iar pentru mărimea zilelor proaste avem nevoie de ES.

@practice biroul de tranzacționare raportează zilnic VaR de 99%, dimineața, înainte de licitația de la ora 12:00 CET.

## Deficitul așteptat este pierderea medie dincolo de VaR {h=257df0a7}

ES răspunde la întrebarea: cînd vine o zi proastă, cît de mare este, în medie, pierderea? Este media pierderii de dincolo de VaR sau, echivalent, media tuturor valorilor VaR cu nivel de încredere peste $\alpha$:

$$ \text{ES}_{\alpha,t}=\E\big[L_t\mid L_t\ge \text{VaR}_{\alpha,t}\big]=\frac{1}{1-\alpha}\int_{\alpha}^{1}\text{VaR}_{u,t}\,du $$ {#eq:es}

unde $u$ parcurge nivelurile de încredere de peste $\alpha$. ES este o măsură coerentă a riscului (Artzner et al., 1999); în particular, este subaditivă:

$$ \text{ES}(L_1+L_2)\le\text{ES}(L_1)+\text{ES}(L_2) $$ {#eq:subadd}

unde $L_1$ și $L_2$ sînt pierderile a două poziții, deci diversificarea nu adaugă niciodată risc. VaR poate încălca această proprietate (Acerbi și Tasche, 2002). De aceea, revizuirea fundamentală a portofoliului de tranzacționare (FRTB, *Fundamental Review of the Trading Book*), adică regulile Basel pentru riscul de piață, folosește ES de 97,5% în locul VaR de 99% (BCBS, 2019).

Pe ultimele 365 de zile, VaR$_{0,975}$ este 61,96 EUR/MWh, iar ES$_{0,975}$ este 86,91 EUR/MWh, media celor mai proaste 10 zile. Pentru cîte 100 MW în România și în Germania–Luxemburg, VaR de 99% este 86,63 și 91,76 EUR/MWh, considerate separat, dar 150,77 împreună: cu o corelație de 0,55 între variațiile celor două prețuri, riscul total este mai mic decît suma riscurilor.

@practice dimensionați rezerva de numerar cu ES, nu cu VaR.

## Creșterile mari de preț sînt mult mai frecvente decît prevede repartiția normală {h=89429e75}

Dacă variațiile prețului ar urma o repartiție normală, zilele extreme ar fi extrem de rare. Nu sînt. Excesul de aplatizare (*kurtosis*) al lui $X_t$ este 12,0 în România și 12,1 în Germania–Luxemburg, față de 0 pentru repartiția normală: repartiția are un centru îngust și cozi lungi.

Numărul creșterilor mari face ideea concretă. Creșteri de peste 3 abateri standard au apărut în 52 de zile, în timp ce repartiția normală ar prevedea 5,8 pe același eșantion. Cea mai mare creștere are 10,1 abateri standard: în ipoteza normalității, o asemenea zi ar apărea o dată la peste $10^{20}$ ani. Graficul compară repartiția observată a variațiilor cu repartiția normală care are aceeași medie și aceeași abatere standard, pentru ambele zone de ofertare.

@practice o limită calculată cu repartiția normală subestimează frecvența zilelor de criză (cursul 1).

@chart tails
Repartiția variațiilor zilnice ale prețului în România și în Germania–Luxemburg, 2015–2026, comparată cu repartiția normală cu aceeași medie și aceeași abatere standard.

## O limită calculată în 2020 cu repartiția normală a fost depășită în 2021–2022 de 19 ori mai des decît se prevedea {h=4b927335}

O limită fixă presupune că riscul de mîine seamănă cu cel din trecut; într-o criză, această ipoteză nu se verifică. Să luăm limita pe care un manager de risc ar fi stabilit-o la sfîrșitul anului 2020 cu ajutorul repartiției normale:

$$ \ell_{0{,}99}=\hat\mu+z_{0{,}99}\,\hat\sigma, \qquad z_{0{,}99}=2{,}326 $$ {#eq:normlim}

unde $\hat\mu$ și $\hat\sigma$ sînt media și abaterea standard a lui $X_t$ în 2015–2020, iar $z_{0,99}$ este cuantila de 99% a repartiției normale standard. O limită corectă este depășită în 1% din zile.

Estimată pe 2 182 de zile din 2015–2020, $\hat\sigma$ este 10,21, iar limita este 23,77 EUR/MWh. Chiar în 2015–2020 limita a fost depășită de 45 de ori, față de 21,8 depășiri așteptate, din cauza cozilor groase. Ulterior, eșecul a devenit spectaculos: 139 de depășiri în 2021–2022, față de 7,3 așteptate, și 226 în 2023–2026, față de 14,0 așteptate, adică de 16 ori mai multe. Limita nu s-a modificat cînd s-a modificat volatilitatea, așa că a continuat să măsoare o piață care nu mai exista.

@practice o limită trebuie să urmeze volatilitatea; secțiunea următoare prezintă patru moduri de a o actualiza.

# Estimarea VaR și ES: patru metode

Există multe moduri de a estima o cuantilă a pierderii de mîine, iar în aceeași zi și pe aceleași date ele dau răspunsuri diferite. Secțiunea prezintă simularea istorică, repartițiile normală și Student-t, simularea istorică filtrată și teoria valorilor extreme, apoi le compară în octombrie 2026 și pe parcursul crizei din 2021–2022.

## Simularea istorică: ultimul an de date este repartiția zilei de mîine {h=6808e619}

Simularea istorică (HS, *historical simulation*) nu presupune nicio repartiție: ordonează ultimele 365 de variații zilnice și citește direct cuantila; a patra cea mai mare variație este VaR de 99%. Formal,

$$ \widehat{\text{VaR}}^{\text{HS}}_{\alpha,t}=\hat q_{\alpha}\big(X_{t-W},\dots,X_{t-1}\big), \qquad \widehat{\text{ES}}^{\text{HS}}_{\alpha,t}=\text{media valorilor }\{X_s\ge\widehat{\text{VaR}}^{\text{HS}}_{\alpha,t}\} $$ {#eq:hs}

unde $W$ = 365 de zile este fereastra, $\hat q_\alpha$ cuantila empirică a variațiilor din fereastră, iar $X_s$ variațiile din fereastră egale cu VaR sau mai mari decît ea.

În octombrie 2026, HS dă o VaR$_{0,99}$ de 86,63 și un ES$_{0,975}$ de 87,59 EUR/MWh. Pe perioada de testare 2017–2026 a fost depășită în 2,04% din zile, nu în 1%. Punctul ei slab este viteza: un regim nou are nevoie de luni de zile pentru a umple fereastra, iar o zi de criză contează cu pondere întreagă timp de 365 de zile, apoi dispare brusc, astfel că VaR scade la o dată fixă care nu are nicio legătură cu piața.

@practice HS este metoda implicită în multe companii energetice și reacționează cu întîrziere.

## Repartițiile normală și Student-t: doi sau trei parametri {h=6ee5603a}

Abordarea parametrică ajustează o curbă pe variațiile din ultimul an și citește cuantila ei. Repartiția normală are doi parametri; repartiția Student-t adaugă un al treilea, numărul gradelor de libertate, care îi îngroașă cozile:

$$ \text{VaR}^{N}_{\alpha}=\mu+\sigma z_\alpha, \qquad \text{ES}^{N}_{\alpha}=\mu+\sigma\frac{\varphi(z_\alpha)}{1-\alpha} $$ {#eq:normal}

$$ \text{VaR}^{t}_{\alpha}=m+s\,t_{\nu,\alpha}, \qquad \text{ES}^{t}_{\alpha}=m+s\,\frac{g_\nu(t_{\nu,\alpha})}{1-\alpha}\cdot\frac{\nu+t_{\nu,\alpha}^2}{\nu-1} $$ {#eq:student}

unde $\mu$ și $\sigma$ sînt media și abaterea standard, $z_\alpha$ și $\varphi$ cuantila și densitatea repartiției normale standard, $m$, $s$ și $\nu$ locația, scala și gradele de libertate ale repartiției Student-t, estimate prin metoda verosimilității maxime (MLE), iar $t_{\nu,\alpha}$ și $g_\nu$ cuantila și densitatea repartiției Student-t. Formulele pentru ES sînt deduse în Anexa A.

În octombrie 2026, repartiția normală dă VaR$_{0,99}$ = 69,64 și ES$_{0,975}$ = 69,98 EUR/MWh; repartiția Student-t dă 76,66 și 80,05. La testarea retrospectivă, VaR normală de 99% a fost depășită în 3,21% din zile, iar VaR Student-t în 1,98%, față de ținta de 1%. Curba t corectează o parte din coadă, dar nu și centrul: la 95% este prea îngustă, cu 8,75% din zile peste ea.

@practice VaR normală este cel mai ușor de explicat și cel mai periculos de folosit fără verificare.

## Simularea istorică filtrată: volatilitatea de azi, forma repartiției din trecut {h=c299e9be}

Simularea istorică filtrată (FHS, *filtered historical simulation*) combină cele două idei anterioare. Împarte variațiile trecute la volatilitatea lor, obținînd șocuri standardizate, apoi înmulțește aceste șocuri cu volatilitatea de azi; forma cozii vine astfel din istorie, iar scala din prezent (Barone-Adesi, Giannopoulos și Vosper, 1999):

$$ e_t=X_t-\mu_{d(t)}, \quad \sigma_t^2=\omega+a\,e_{t-1}^2+b\,\sigma_{t-1}^2, \quad z_t=e_t/\sigma_t $$ {#eq:fhs-garch}

$$ \text{VaR}^{\text{FHS}}_{\alpha,t}=\mu_{d(t)}+\sigma_t\,\hat q_\alpha(z) $$ {#eq:fhs-var}

unde $\mu_{d(t)}$ este variația medie a zilei din săptămînă (prețul scade la sfîrșit de săptămînă), $e_t$ variația din care s-a scăzut această medie, $\sigma_t$ volatilitatea din modelul autoregresiv generalizat cu heteroscedasticitate condiționată (GARCH) din cursul 3 (Bollerslev, 1986), cu parametrii $\omega$, $a$ și $b$, reestimat la fiecare 21 de zile pe 730 de zile, $z_t$ șocul standardizat, iar $\hat q_\alpha(z)$ cuantila empirică a șocurilor. ES se obține înmulțind $\sigma_t$ cu media șocurilor $z$ de peste $\hat q_\alpha(z)$.

Pe datele din România, volatilitatea GARCH(1,1) variază între 4,06 EUR/MWh (29 martie 2021) și 100,86 EUR/MWh (12 iulie 2022). În octombrie 2026, VaR$_{0,99}$ obținută prin FHS este 67,50 EUR/MWh. La testarea retrospectivă, VaR de 99% a fost depășită în 1,51% din zile, iar VaR de 95% în 5,58%, cu valoarea $p$ a testului Kupiec de 0,120: este prima metodă de pînă acum care trece testul la 95%.

@practice FHS ridică limita la cîteva zile după un salt al volatilității; HS are nevoie de luni.

## Teoria valorilor extreme: modelăm numai coada, cu o curbă Pareto generalizată {h=5e559fc5}

Teoria valorilor extreme (EVT, *extreme value theory*) modelează numai coada. Peste un prag ridicat, excesele aproape oricărei repartiții urmează aceeași curbă cu doi parametri, repartiția Pareto generalizată (GPD) (Pickands, 1975):

$$ \Pr(Z-u\le y\mid Z>u)\approx 1-\Big(1+\frac{\xi y}{\beta}\Big)^{-1/\xi} $$ {#eq:gpd}

$$ \text{VaR}_\alpha=u+\frac{\beta}{\xi}\Big[\Big(\frac{n}{N_u}(1-\alpha)\Big)^{-\xi}-1\Big], \quad \text{ES}_\alpha=\frac{\text{VaR}_\alpha+\beta-\xi u}{1-\xi} $$ {#eq:evt}

unde $Z$ este șocul standardizat, $y$ excesul peste prag, $u$ pragul, ales prin metoda depășirilor unui prag (POT, *peaks over threshold*) drept cuantila de 90% a lui $z$, $N_u$ numărul reziduurilor, din cele $n$, care îl depășesc, $\xi$ parametrul de formă (grosimea cozii), iar $\beta$ scala repartiției GPD, ambii estimați prin MLE. Rezultatul se înmulțește apoi cu $\sigma_t$, ca la FHS (McNeil și Frey, 2000); deducerea formulelor se află în Anexa B.

Pe variațiile brute, cu pragul la cuantila de 95%, $\hat\xi$ = 0,164: o coadă groasă, în care momentele de ordin peste 6,1 nu există. După filtrul GARCH, $\hat\xi$ median este 0,011: filtrul preia cea mai mare parte a cozii. La testarea retrospectivă, VaR EVT de 99% a fost depășită în 1,37% din zile, cel mai bun rezultat dintre cele cinci metode.

@practice folosiți EVT pentru ziua care apare o dată la zece ani și nu se află în nicio fereastră.

## Peste prag, curba Pareto urmează datele, iar curba normală nu {h=e8032d32}

Graficul arată coada variațiilor filtrate GARCH din cele 730 de zile dinainte de 31 octombrie 2026, împreună cu curba Pareto ajustată și cu curba normală. La ultima reestimare, din 11 octombrie 2026, $\hat\xi$ = 0,182 și $\hat\beta$ = 0,569. Peste prag, curba Pareto urmează punctele observate, în timp ce curba normală scade mult prea repede.

Parametrul de formă nu este stabil: $\hat\xi$ a fost pozitiv în 53% din reestimări, deci coada reziduurilor standardizate este uneori groasă, alteori nu (Balkema și de Haan, 1974; McNeil și Frey, 2000). Acesta este un motiv în plus pentru a reestima modelul periodic, în loc să fixăm o dată pentru totdeauna forma cozii.

@practice o zi de 4 abateri standard este rară, dar posibilă; curba normală o consideră practic imposibilă.

@chart gpd_tail
Coada variațiilor filtrate GARCH ale prețului din România în cele 730 de zile dinainte de 31 octombrie 2026, cu curba Pareto generalizată ajustată și cu curba normală.

## Aceeași zi, aceleași date, cinci răspunsuri: alegerea metodei este o decizie de risc {h=56935146}

Tabelul prezintă media celor 31 de prognoze făcute pentru zilele din octombrie 2026. Primele trei coloane sînt în EUR/MWh, ultimele două în mii EUR pentru 100 MW în bandă, adică 2 400 MWh pe zi.

| Metoda | VaR 0,95 | VaR 0,99 | ES 0,975 | VaR 0,99, mii EUR | ES 0,975, mii EUR |
|---|---|---|---|---|---|
| HS | 50,38 | 86,63 | 87,59 | 208 | 210 |
| Normală | 49,33 | 69,64 | 69,98 | 167 | 168 |
| Student-t | 45,77 | 76,66 | 80,05 | 184 | 192 |
| FHS | 36,22 | 67,50 | 67,44 | 162 | 162 |
| EVT | 35,66 | 64,33 | 68,54 | 154 | 164 |

Aceeași poziție, în aceeași zi, are o VaR de 99% între 154 și 208 mii EUR, în funcție de metodă. Diferența nu este zgomot. HS și Student-t conțin încă în fereastră zilele volatile din ultimul an, în timp ce FHS și EVT folosesc volatilitatea actuală, care în octombrie 2026 era sub media anului. Alegerea metodei este, așadar, ea însăși o decizie de risc.

@practice raportați două metode alăturate și explicați diferența dintre ele.

## În criză, FHS s-a adaptat repede, iar HS și VaR normală au întîrziat {h=41f7228a}

Diferența dintre metode contează cel mai mult într-o criză. Între 1 iulie 2021 și 30 iunie 2023, adică în 730 de zile, o VaR corectă de 99% ar fi trebuit depășită de 7,3 ori. Numărul depășirilor a fost 28 pentru HS, 45 pentru repartiția normală, 29 pentru Student-t, 19 pentru FHS și 17 pentru EVT. Nicio metodă nu a fost corectă, dar metodele filtrate, care urmează volatilitatea GARCH, s-au adaptat în cîteva zile, în timp ce HS și VaR normală au așteptat ca ferestrele lor să se umple cu zile de criză.

@practice într-o criză, un model care reacționează în cîteva zile protejează lichiditățile.

@chart var_paths
Variațiile zilnice ale prețului din România și prognozele VaR de 99% ale celor cinci metode, 1 iulie 2021 – 30 iunie 2023, cu depășirile marcate.

## Regula rădăcinii pătrate a timpului supraestimează riscul pe 10 zile {h=ac2b2d7e}

Autoritățile de reglementare și multe companii trec de la VaR pe o zi la VaR pe zece zile înmulțind-o cu $\sqrt{10}$ = 3,16. Regula presupune că variațiile zilnice sînt independente, ca într-un mers aleator. Prețurile energiei electrice nu se comportă așa: ele revin spre un nivel stabilit de costul combustibililor și de calendarul săptămînal.

Măsurată direct, cuantila de 99% pe 10 zile este de 1,72 ori cuantila pe o zi în România și de 1,75 ori în Germania–Luxemburg, nu de 3,16 ori. Raportul varianțelor la 10 zile este 0,33, în timp ce valoarea 1 ar corespunde unui mers aleator. Autocorelația lui $X_t$ este −0,076 la decalajul 1, o ușoară revenire, și 0,474 la decalajul 7, tiparul săptămînal (Weron, 2014). Graficul compară cuantila empirică pentru fiecare orizont cu scalarea prin rădăcina pătrată a timpului.

@practice pentru un orizont de 10 zile, măsurați direct variațiile pe 10 zile; înmulțirea cu √10 blochează capital inutil.

@chart horizon
Cuantila empirică de 99% a variațiilor prețului pe orizonturi de pînă la 10 zile, în România și în Germania–Luxemburg, comparată cu scalarea cuantilei pe o zi prin rădăcina pătrată a timpului.

# Testarea retrospectivă: și-a respectat modelul promisiunea?

O VaR este o promisiune privind frecvența cu care pierderile o vor depăși, iar promisiunea poate fi verificată ulterior. Secțiunea numără depășirile cu testul Kupiec, le verifică momentul apariției cu testul Christoffersen și cu semaforul Basel și testează ES cu statistica Acerbi–Székely, pe 3 587 de zile.

## Testul Kupiec: sînt atîtea depășiri cîte au fost promise? {h=898f3ddd}

O VaR de 99% promite că va fi depășită în 1% din zile. Testul Kupiec (1995) numără depășirile și verifică dacă proporția lor diferă de această promisiune:

$$ I_t=\mathbf 1\{L_t>\text{VaR}_{\alpha,t}\}, \qquad x=\textstyle\sum_{t=1}^{n}I_t, \qquad \hat p=x/n $$ {#eq:hit}

$$ \text{LR}_{uc}=-2\ln\frac{(1-p)^{n-x}\,p^{x}}{(1-\hat p)^{n-x}\,\hat p^{\,x}}\ \sim\ \chi^2_1 $$ {#eq:kupiec}

unde $I_t$ este indicatorul depășirii (1 dacă pierderea depășește VaR, 0 altfel), $n$ numărul zilelor, $x$ numărul depășirilor, $\hat p$ proporția lor observată, iar $p=1-\alpha$ proporția promisă. $\text{LR}_{uc}$ este testul raportului de verosimilitate (LR) pentru acoperirea necondiționată; în ipoteza nulă urmează o repartiție $\chi^2$ cu un grad de libertate, iar modelul este respins la pragul de 5% dacă $\text{LR}_{uc}$ depășește 3,84.

Pentru VaR de 99% pe 3 587 de zile se așteaptă 35,9 depășiri. VaR normală a avut 115, cu $\text{LR}_{uc}$ = 111,5; FHS a avut 54, cu $\text{LR}_{uc}$ = 8,0; EVT a avut 49, cu $p$ = 0,037. Puterea testului depinde de eșantion: pe un singur an, la 99%, ne așteptăm la doar 2–3 depășiri, iar testul respinge foarte greu; zece ani de date zilnice îl fac precis.

@practice cereți numărul depășirilor înainte de a avea încredere în VaR raportată de cineva.

## Testul Christoffersen: apar depășirile grupate? {h=b74858b1}

Un model bun nu este surprins de două ori la rînd: o depășire azi nu trebuie să facă mai probabilă o depășire mîine. Christoffersen (1998) verifică acest lucru comparînd două probabilități condiționate:

$$ \pi_{01}=\Pr(I_t=1\mid I_{t-1}=0), \qquad \pi_{11}=\Pr(I_t=1\mid I_{t-1}=1) $$ {#eq:markov}

$$ \text{LR}_{ind}=-2\ln\frac{(1-\hat\pi)^{n_{00}+n_{10}}\hat\pi^{\,n_{01}+n_{11}}}{(1-\hat\pi_{01})^{n_{00}}\hat\pi_{01}^{\,n_{01}}(1-\hat\pi_{11})^{n_{10}}\hat\pi_{11}^{\,n_{11}}}\sim\chi^2_1 $$ {#eq:christoffersen}

unde $\pi_{01}$ este probabilitatea unei depășiri după o zi fără depășire, $\pi_{11}$ probabilitatea unei depășiri după o zi cu depășire, $n_{ij}$ numărul zilelor cu $I_{t-1}=i$ și $I_t=j$, $\hat\pi$ proporția totală a depășirilor, iar $\hat\pi_{01}$ și $\hat\pi_{11}$ proporțiile condiționate estimate. Ipoteza nulă este $H_0$: $\pi_{01}=\pi_{11}$. Testul comun pentru acoperire și independență este $\text{LR}_{cc}$ = $\text{LR}_{uc}$ + $\text{LR}_{ind}$, cu repartiția $\chi^2_2$.

Pentru VaR de 99%, valorile $p$ ale testului de independență sînt 0,682 pentru HS, 0,868 pentru VaR normală și 0,199 pentru FHS. Nicio metodă nu pică testul: depășirile cad rareori în zile consecutive. Ele se grupează însă pe luni. VaR normală a fost depășită în 7,26% din zile în 2021–2022 și în 2,33% în 2017–2020. Un test de ordinul întîi, care privește numai ziua precedentă, nu observă acest lucru; semaforul Basel, care privește o fereastră de 250 de zile, îl observă.

@practice urmăriți momentul în care apar depășirile, nu doar numărul lor.

## În zece ani, doar metodele filtrate trec testul la 95%; la 99%, toate metodele au prea multe depășiri {h=d46990f5}

Tabelul reunește testarea retrospectivă a celor cinci metode pentru România, 1 ianuarie 2017 – 31 octombrie 2026. Proporțiile așteptate sînt 5% și 1% din 3 587 de zile, adică 35,9 depășiri la 99%. „Zilele roșii” sînt proporția zilelor în care ultimele 250 de zile conțin cel puțin 10 depășiri (blocul următor); același tabel pentru Germania–Luxemburg se află în Anexa D.

| România | 95%: proporția | Kupiec p | 99%: număr | proporția, % | Kupiec p | Christoffersen p | zile roșii, % |
|---|---|---|---|---|---|---|---|
| HS | 6,16 | 0,002 | 73 | 2,04 | <0,001 | 0,682 | 16,7 |
| Normală | 7,36 | <0,001 | 115 | 3,21 | <0,001 | 0,868 | 29,5 |
| Student-t | 8,75 | <0,001 | 71 | 1,98 | <0,001 | 0,630 | 18,3 |
| FHS | 5,58 | 0,120 | 54 | 1,51 | 0,005 | 0,199 | 6,2 |
| EVT | 5,55 | 0,139 | 49 | 1,37 | 0,037 | 0,244 | 2,8 |

La 95%, numai FHS și EVT trec testul Kupiec, cu valori $p$ de 0,120 și 0,139. La 99% toate metodele sînt respinse, dar abaterile diferă mult: VaR normală este depășită în 3,21% din zile și stă 29,5% din zile în zona roșie, în timp ce EVT este depășită în 1,37% din zile și se află în zona roșie în 2,8% din zile. Niciun model nu surprinde complet coada de 99% a prețurilor energiei.

@practice acceptați un model la 95%, dar păstrați capital suplimentar pentru coada de 99%, pe care niciun model nu o surprinde complet.

## Semaforul Basel: VaR normală a stat 30% din zile în zona roșie {h=4e9da893}

Comitetul de la Basel pentru Supraveghere Bancară (BCBS, 1996) judecă o VaR de 99% după numărul depășirilor din ultimele 250 de zile: zona verde pentru 0–4, galbenă pentru 5–9 și roșie pentru 10 sau mai multe. Un model corect se află în zona verde cu probabilitatea 89,2% și în zona roșie cu probabilitatea 0,025%, deci zona roșie este un semnal puternic că modelul greșește.

Graficul urmărește zi de zi zona fiecărei metode pe toată perioada de testare. VaR normală a stat aproape o treime din zile în zona roșie; HS a fost în zona roșie în 16,7% din zile, FHS în 6,2%, iar EVT în 2,8%. Perioadele roșii se concentrează în anii de criză: este tocmai gruparea pe luni pe care testul Christoffersen nu a detectat-o.

@practice zona galbenă cere recalibrarea modelului, iar cea roșie oprirea lui pentru limite.

@chart traffic
Zona din semaforul Basel pentru VaR de 99% a fiecărei metode (numărul depășirilor din ultimele 250 de zile), România, testare retrospectivă 2017–2026.

## În 2021–2022 toate metodele au eșuat; din 2023, metodele filtrate au revenit aproape de 1% {h=ccbd11fe}

Împărțirea perioadei de testare în trei subperioade arată de unde provin eșecurile. Tabelul dă proporția zilelor în care pierderea a depășit VaR de 99%, în procente, pentru România și Germania–Luxemburg.

| VaR 99%, % din zile | RO 17–20 | RO 21–22 | RO 23–26 | DE-LU 17–20 | DE-LU 21–22 | DE-LU 23–26 |
|---|---|---|---|---|---|---|
| HS | 1,58 | 4,93 | 1,00 | 1,16 | 3,84 | 1,07 |
| Normală | 2,33 | 7,26 | 2,00 | 2,40 | 5,89 | 2,07 |
| Student-t | 1,30 | 4,66 | 1,29 | 1,37 | 3,97 | 1,29 |
| FHS | 1,37 | 2,88 | 0,93 | 1,44 | 2,47 | 1,36 |
| EVT | 1,24 | 2,47 | 0,93 | 1,51 | 2,19 | 1,07 |

În criză, chiar și FHS a fost depășită în 2,88% din zile în România: șocul gazelor a mutat întreaga repartiție, nu doar scala ei. După criză imaginea se schimbă: din 2023, FHS și EVT sînt la 0,93%, HS la 1,00%, și doar VaR normală rămîne departe de țintă, la 2,00%. Un model care arată bine în anii liniștiți spune puțin despre comportamentul lui într-o criză.

@practice testați orice model pe 2021–2022 înainte de a vă baza pe el într-o criză.

## Testarea ES: sînt pierderile de dincolo de VaR atît de mari cît s-a prognozat? {h=55d2acca}

ES nu poate fi verificat prin numărare, pentru că se referă la mărimea pierderilor de dincolo de VaR. Acerbi și Székely (2014) împart fiecare pierdere din zilele cu depășiri la prognoza ES; dacă ES este corect, media acestor rapoarte este 1:

$$ Z_2=\frac{1}{T(1-\alpha)}\sum_{t=1}^{T}\frac{L_t\,I_t}{\text{ES}_{\alpha,t}}-1, \qquad \E_{H_0}[Z_2]=0 $$ {#eq:z2}

unde $T$ este numărul zilelor, $\alpha$ = 0,975, $I_t$ depășirea VaR$_{0,975}$, $L_t$ pierderea, iar $\text{ES}_{\alpha,t}$ prognoza ES. Un $Z_2$ pozitiv înseamnă că ES a fost prea mic. Valoarea $p$ se obține din 2 000 de traiectorii simulate din fiecare model (Anexa C).

| Z2 | total | p | 2021–22 | p | 2023–26 | p |
|---|---|---|---|---|---|---|
| HS | 0,628 | <0,001 | 2,694 | <0,001 | −0,026 | 0,761 |
| Normală | 1,425 | <0,001 | 4,170 | <0,001 | 0,697 | <0,001 |
| Student-t | 0,908 | <0,001 | 2,910 | <0,001 | 0,329 | 0,052 |
| FHS | 0,335 | 0,004 | 1,164 | <0,001 | −0,083 | 0,759 |
| EVT | 0,279 | 0,009 | 1,183 | <0,001 | −0,114 | 0,722 |

În criză, toate prognozele ES au fost prea mici, cele normale cu diferența cea mai mare. Din 2023, FHS, EVT și HS trec testul. Deoarece un ES de 97,5% se sprijină pe doar circa 9 zile extreme pe an, comparația modelelor are nevoie de mai mulți ani de date (Pele și Mazurencu-Marinescu-Pele, 2026).

@practice evaluați ES pe mai mulți ani, niciodată pe un trimestru (circa 9 zile extreme pe an).

## AIDA 2026: o deplasare conformală arată cît greșește VaR și o corectează {h=5aae05ca}

La conferința AIDA (Academia de Studii Economice din București, 4 iunie 2026), D. T. Pele a prezentat o lucrare comună cu V. Bolovăneanu, A. T. Ginavar, S. Lessmann și W. K. Härdle despre recalibrarea prognozelor VaR ([diapozitive](https://github.com/danpele/EMQA/blob/main/resources/aida2026/pele_conformal_tail_risk.pdf); lucrarea a fost trimisă spre publicare). Metoda are nevoie de un singur număr. În fiecare zi, scorul $s_t=\hat q_t-r_t$ compară cuantila prognozată cu randamentul realizat și este pozitiv în ziua unei depășiri; $\hat q_V$ este cuantila de 99% a scorurilor trecute, iar VaR corectată este VaR plus $\hat q_V$. Deplasarea este fie fixă, estimată pe un eșantion de calibrare (un audit), fie glisantă, pe ultimele 250 de zile (pentru utilizarea zilnică). Lucrarea o aplică VaR de 1% a 10 modele, modele fundaționale, modele de tip GARCH și HS, pe 24 de active, inclusiv petrol și gaze, în total 240 de perechi, și evaluează rezultatul cu testele Kupiec și Christoffersen și cu semaforul Basel din această secțiune.

Ca diagnostic, $\hat q_V$ variază între −0,007, pentru un model prea prudent, și +0,102, pentru un model fără informație utilă despre coadă, și explică 53,4% ($R^2$ parțial) din cîștigul la scorul cuantilic. Ca instrument de corecție, perechile din zona verde cresc de la 63/240 (26,2%) inițial la 203/240 (84,6%) cu deplasarea fixă și la 234/240 (97,5%) cu deplasarea glisantă. Rata depășirilor este refăcută, dar gruparea lor nu, astfel încît testul Christoffersen își păstrează rolul. Legătura cu acest curs este directă: testul Kupiec arată dacă VaR eșuează, $\hat q_V$ arată cu cît, iar lărgirea $\hat c_t$ a garanției pentru PZU, din secțiunea următoare, este aceeași deplasare cu un singur parametru.

@practice după un test eșuat, lărgiți VaR cu deplasarea conformală și testați în continuare gruparea depășirilor.

# De la cuantile la marje, garanții și limite

Cuantilele din secțiunile anterioare devin numerar și limite în trei locuri: marjele cerute de bursă, garanția de pe PZU și limitele de poziție ale biroului de tranzacționare. Secțiunea arată cum se calculează fiecare și de ce o companie bine acoperită la risc poate rămîne totuși fără lichidități.

## Marjele la bursă sînt VaR plătită în numerar, în fiecare zi {h=d2fdf779}

Casa de compensare reține un depozit care acoperă pierderea de 99% pe două zile și decontează zilnic, în numerar, cîștigurile și pierderile:

$$ \text{IM}_t=K F_t\,\hat q_{0{,}99}\big(|r^{(2)}|\big), \qquad \text{VM}_t=n K(F_t-F_{t-1}) $$ {#eq:margin}

unde $\text{IM}_t$ este marja inițială (IM) și $\text{VM}_t$ marja de variație (VM), ambele cerute de contrapartea centrală (CCP), $F_t$ prețul futures, $K$ = 1 000 de barili pentru un lot Brent, $r^{(2)}$ randamentul pe două zile, $\hat q_{0,99}$ cuantila lui empirică de 99%, în valoare absolută, iar $n$ numărul loturilor vîndute (pozitiv) sau cumpărate (negativ).

Regulile provin din Regulamentul privind infrastructura pieței europene (EMIR) și din standardele tehnice de reglementare (RTS) asociate, Regulamentul delegat 153/2013. Pentru contractele futures, marja trebuie să acopere 99% din pierderi pe o perioadă de lichidare de 2 zile, pe cel puțin 12 luni de date (art. 24–26). Articolul 28 adaugă instrumentele anticiclice (APC, *anti-procyclicality*): o rezervă de 25%, o pondere de 25% pentru observațiile din perioade de criză sau un prag calculat pe 10 ani. Pe contractul Brent al bursei Intercontinental Exchange (ICE), o poziție de 100 de loturi vîndute a avut cea mai mare marjă de variație într-o zi, de 0,88 milioane de dolari americani (USD), la 16 septembrie 2019.

@practice producătorul acoperit cîștigă mai tîrziu din vînzarea fizică, dar plătește marja azi.

## În 2022, companii energetice bine acoperite la risc au rămas fără lichidități pentru marje {h=f377a636}

Banca Centrală Europeană (BCE) a descris ce s-a întîmplat în noiembrie 2022. Contractele futures pe gaze TTF au atins 227 EUR/MWh la 7 martie 2022, de circa 12 ori nivelul de la începutul anului 2021. La jumătatea anului 2022 se depunea o marjă inițială de aproximativ două ori mai mare decît la sfîrșitul anului 2021. Companiile afectate au fost mai ales utilitățile și producătorii care vînduseră la termen: firme care se acopereau la risc, nu speculatori. Poziția lor fizică se apreciase, dar cîștigul urma să vină abia la livrare, în timp ce marja trebuia plătită imediat, în numerar.

Uniunea Europeană (UE) a răspuns prin Regulamentul delegat (UE) 2022/2311, care a acceptat garanțiile publice drept garanții pînă la 29 noiembrie 2023. În România, același mecanism funcționează pe piața pentru ziua următoare: OPCOM validează o ofertă de cumpărare la preț pozitiv numai în limita garanției participantului, de regulă o scrisoare de garanție bancară (OPCOM, 2025).

@practice riscul care poate scufunda o companie acoperită la risc este cel de lichiditate, nu prețul în sine.

## Marjele sînt prociclice: în 2026, marja Brent a crescut de 2,7 ori în două luni {h=b75f433b}

O marjă calculată din randamentele ultimelor 12 luni crește exact atunci cînd piața devine volatilă, adică atunci cînd numerarul este cel mai greu de găsit. Graficul recalculează marja inițială pe lot din contractul futures Brent cu scadența cea mai apropiată. La începutul anului 2026, prețul Brent a urcat de la 72,48 USD (27 februarie 2026) la 118,35 USD (31 martie 2026). Cu 12 luni de date, IM a crescut de la 5 970 la 16 313 USD pe lot, adică de 2,73 ori; cu un prag calculat pe datele din 2015 încoace, a crescut doar de 2,07 ori.

Pragul și protejează mai bine: pierderile mai mari decît IM au apărut în 1,80% din zile cu 12 luni de date și în 0,66% cu prag, față de ținta de 1%. Instrumentele anticiclice din EMIR nu țin, așadar, doar de stabilitatea casei de compensare; ele fac din marjă și o cuantilă de 99% mai bună.

@practice planificați lichiditățile pentru marja cerută într-o criză, nu pentru marja de astăzi.

@chart brent_im
Prețul contractului Brent cu scadența cea mai apropiată și marja inițială pe lot calculată cu 12 luni de date și cu prag din 2015, zile de tranzacționare 2016–2026.

## Garanția pentru PZU se calculează din cuantila prognozată a prețului de mîine {h=0a932b97}

Ca să fie sigur că va cumpăra, furnizorul ofertează pînă la un preț ridicat, iar garanția trebuie să acopere acest preț înmulțit cu volumul. Garanția se sprijină deci pe o cuantilă ridicată a prețului de mîine, prognozată prin regresie cuantilică (QR) (Koenker și Bassett, 1978) și lărgită cu o corecție conformală (Romano et al., 2019):

$$ G_t\ \ge\ Q\cdot 24\cdot \hat q_{\tau,t}, \qquad \hat q_{\tau,t}=\beta_0+\beta_1P_{t-1}+\beta_2P_{t-7}+\textstyle\sum_j\delta_jD_{j,t} $$ {#eq:guarantee}

$$ \tilde q_{\tau,t}=\hat q_{\tau,t}+\hat c_t, \qquad \hat c_t=\hat q_\tau\big(P_s-\hat q_{\tau,s},\ s=t-365,\dots,t-1\big) $$ {#eq:conformal}

unde $G_t$ este garanția în EUR, $Q$ poziția în MW, $\hat q_{\tau,t}$ prognoza QR a cuantilei de ordin $\tau$ a prețului, estimată pe ultimele 365 de zile, ca la medierea prin regresie cuantilică (QRA) din cursul 2, $\beta_0$, $\beta_1$, $\beta_2$ și $\delta_j$ coeficienții ei, $P_{t-1}$ și $P_{t-7}$ prețurile de acum o zi și de acum o săptămînă, $D_{j,t}$ variabilele pentru ziua săptămînii, $\tilde q_{\tau,t}$ cuantila lărgită, iar $\hat c_t$ corecția conformală, adică cuantila de ordin $\tau$ a erorilor de prognoză din trecut.

Cu $\tau$ = 0,99, în 2017–2026, prețul a rămas sub prognoză în 96,90% din zile cu QR simplă, în 98,47% cu QR lărgită și în 98,49% cu FHS. Pentru 100 MW în bandă, garanția costă în medie 0,371 milioane EUR pe zi, iar lărgirea adaugă 7,5%. Suma depinde mult de regim: 0,172 milioane EUR pe zi în 2017–2020 și 0,649 în 2021–2022.

@practice dimensionați linia bancară din spatele garanției pe cuantila din criză, înainte de criză.

## Lărgirea cozilor apropie cuantila de 99% de acoperirea promisă {h=e37ef8af}

Graficul compară, pe toată perioada de testare, proporția zilelor în care prețul a rămas sub fiecare prognoză de 99%. Valorile $p$ ale testului Kupiec la 99% sînt sub 0,001 pentru QR simplă, 0,003 pentru QR lărgită și 0,005 pentru FHS: corecția conformală apropie acoperirea de promisiune, fără să o atingă complet. La 95%, QR lărgită trece testul, cu $p$ = 0,053, așa cum sugera cursul 2 pentru cozi (Nowotarski și Weron, 2018).

@practice o prognoză folosită pentru garanții trebuie să fie calibrată în coadă, nu doar precisă în medie.

@chart coverage
Acoperirea prognozei cuantilei de 99% a prețului PZU din România pentru QR simplă, QR lărgită și FHS, testare retrospectivă 2017–2026.

## Limita de poziție în MW trebuie să scadă atunci cînd VaR crește {h=9af5f0b8}

Conducerea stabilește un buget zilnic de risc, în EUR, iar biroul de tranzacționare îl împarte la VaR de azi pentru 1 MW:

$$ Q^{\max}_t=\frac{B}{24\cdot\text{VaR}^{\text{FHS}}_{0{,}99,t}} $$ {#eq:limit}

unde $B$ este bugetul zilnic de VaR, aici 250 000 EUR (o ipoteză de lucru), $\text{VaR}^{\text{FHS}}_{0,99,t}$ VaR de 99% obținută prin FHS, în EUR/MWh, iar $Q^{\max}_t$ poziția deschisă maximă în bandă, în MW.

Cu VaR FHS de 99% pe datele din România, VaR mediană din 2019 a fost 20,27 EUR/MWh, ceea ce permite 514 MW. La 12 iulie 2022, VaR a fost 245,80, iar limita doar 42 MW. La 31 octombrie 2026, VaR a fost 53,15, iar limita 196 MW. O limită fixă în MW lasă suma expusă la risc să crească odată cu volatilitatea; un buget fix în EUR o menține constantă și obligă poziția să se micșoreze atunci cînd piața devine periculoasă.

@practice stabiliți limitele în EUR de VaR și transformați-le zilnic în MW.

# Furnizorul și producătorul: un singur preț, două cozi

Furnizorul și producătorul se confruntă cu același preț, dar cu cozi opuse, iar factura lunară a furnizorului depinde și de profilul consumului. Secțiunea măsoară fluxul de numerar lunar la risc al furnizorului, compară cele două cozi și rezumă studiul de caz C4 despre riscul sistemic și riscurile specifice sectorului energetic.

## Costul lunar la risc al unui furnizor: limita normală a eșuat din nou {h=34d9efd9}

Furnizorul stabilește prețul lunii viitoare după costul lunii curente; riscul este un salt al prețului ponderat cu consumul. Depășirea costului și cuantila ei sînt

$$ \bar P^{L}_m=\frac{\sum_h P_hL_h}{\sum_h L_h}, \qquad o_m=\frac{\bar P^{L}_m}{\bar P^{L}_{m-1}}-1, \qquad \text{CFaR}_{0{,}95}=\hat q_{0{,}95}(o_m) $$ {#eq:cfar}

unde $P_h$ este prețul orar, $L_h$ consumul național în ora $h$ (profilul portofoliului), $\bar P^{L}_m$ prețul ponderat cu consumul în luna $m$, $o_m$ depășirea costului de la o lună la alta, iar fluxul de numerar la risc (CFaR, *cash-flow-at-risk*) este cuantila acestei depășiri. Sumele în EUR se referă la un portofoliu de 100 MW în medie.

Pe 140 de luni, din martie 2015 pînă în octombrie 2026, limita normală de 99% estimată pe 2015–2020 este o depășire de +50,5%. Ea a fost depășită de 3 ori din 2021, față de 0,7 depășiri așteptate. Cea mai proastă lună a fost noiembrie 2024, cu +86,6%, adică 5,96 milioane EUR. Empiric, pe toate lunile, CFaR$_{0,95}$ este +39,9%, adică 2,84 milioane EUR, iar ES$_{0,95}$ este +60,2%, adică 6,49 milioane EUR.

@practice includeți în oferta cu preț fix o primă calculată din ES sau acoperiți-o la termen (cursul 5).

## Din 2021, limita lunară normală de 99% a fost depășită de 3 ori (0,7 așteptate) {h=f29d67da}

Graficul arată depășirea lunară a costului ponderat cu consumul din martie 2015 încoace, împreună cu limita normală de 99% calculată în 2020. Barele roșii sînt lunile care depășesc limita. Cea mai mare depășire a apărut în noiembrie 2024, după vara anului 2024, și nu în timpul crizei din 2022: riscul lunar al furnizorului depinde de saltul de la o lună la alta, nu de nivelul prețului.

@practice reestimați limita lunară în fiecare trimestru și testați-o în condițiile lunilor din 2022.

@chart supplier_month
Depășirea lunară a costului energiei ponderat cu consumul în România, martie 2015 – octombrie 2026, cu limita normală de 99% calculată în 2020; lunile peste limită sînt marcate cu roșu.

## Același preț, două cozi: coada furnizorului este mai groasă decît a producătorului {h=6b9516b4}

Furnizorul pierde cînd prețul crește, producătorul cînd prețul scade:

$$ L^{\text{cumpărător}}_t=+Q\,24\,X_t, \qquad L^{\text{vînzător}}_t=-Q\,24\,X_t $$ {#eq:twotails}

unde $L^{\text{cumpărător}}_t$ este pierderea cumpărătorului (furnizorul), $L^{\text{vînzător}}_t$ pierderea producătorului care vinde pe piața spot, $Q$ poziția în MW, iar $X_t$ variația prețului. Există o singură repartiție a lui $X_t$, dar două cozi: cea superioară, a furnizorului, și cea inferioară, a producătorului. Pentru că prețurile sar mai mult în sus decît în jos, asimetria lui $X_t$ este 1,02.

Pe datele zilnice din 1 ianuarie 2015 – 31 octombrie 2026, cuantila de 99% a variației (riscul furnizorului) este +88,21 EUR/MWh, iar cuantila de 1% (riscul producătorului) este −70,74 EUR/MWh. ES$_{0,975}$ este 91,29 pentru furnizor, față de 74,92 pentru producător. Asimetria se păstrează și pe prețul de bază lunar: cuantila de 95% a variației este +42,4%, iar cuantila de 5% este −32,3%.

@practice riscul de preț al producătorului este mai mic, dar un an secetos adaugă riscul de volum (diapozitivul următor).

## Studiul de caz C4: un indicator de risc sistemic și două riscuri specifice companiilor energetice {h=b4986170}

Studiul de caz C4 pornește de la o lucrare a grupului nostru (Toma, Dima, Grecu, Pele și Lessmann, 2026). Lucrarea folosește 100 de companii energetice europene din perioada 2016–2026 și estimează regresii cuantilice de 5% cu operatorul de contracție și selecție în normă absolută (LASSO); penalizarea medie pe companii este indicatorul de risc financiar al sectorului energetic (EFRM, *Energy Financial Risk Meter*). EFRM surprinde șocurile din 2020 și 2022, iar împreună cu indicatorul compozit de stres sistemic al BCE (CISS) prognozează lunile volatile cu o arie de sub curbă (AUC) de 0,731.

Replicarea noastră pe trei companii din România, OMV Petrom, Romgaz și Nuclearelectrica, dă o AUC de 0,38, față de 0,61 pentru volatilitatea trecută: un indicator sistemic are nevoie de multe companii, ca în lucrare. Studiul de caz adaugă două riscuri specifice companiilor energetice. Prima preț–volum a profilului casnic, adică costul suplimentar al cumpărării unor cantități mai mari în orele scumpe, a fost de 5,2% din prețul de bază în 2025. Un parc hidro care a vîndut la termen producția mediană ar fi trebuit să răscumpere în anul secetos 2022 volumul lipsă, cu un cost de 394 de milioane EUR.

@practice includeți indicatorul sistemic, prima preț–volum și costul anului secetos în același tablou de bord.

## AIDA 2026: riscul sistemic din energia UE a crescut brusc din iulie 2021 {h=73044e9c}

La conferința AIDA (3 iunie 2026), F.-M. Toma a prezentat lucrarea din studiul de caz C4 ([diapozitive](https://github.com/danpele/EMQA/blob/main/resources/aida2026/toma_energy_financial_risk_meter.pdf); lucrarea: [doi:10.2139/ssrn.6985301](https://doi.org/10.2139/ssrn.6985301)). Lucrarea folosește 100 de companii energetice europene, din aprilie 2016 pînă în martie 2026. Pentru fiecare firmă, cuantila de 5% a randamentului este regresată prin LASSO pe randamentele celorlalte 99 de firme, pe contractele futures pe petrol și gaze și pe indici bursieri; EFRM este penalizarea LASSO medie, astfel încît o valoare mai mare înseamnă că sînt necesare mai multe legături pentru a explica coada, adică o expunere sistemică mai mare.

EFRM lunar are două rupturi: februarie 2020, la începutul pandemiei, și iulie 2021, în timpul creșterii prețului gazelor, cu șapte luni înaintea invaziei Ucrainei. Riscul geopolitic a influențat EFRM abia după invazie, cu +1,52 puncte procentuale într-un model cu parametri variabili. De atunci, efectul EFRM asupra acțiunilor din Stoxx 600 s-a atenuat cu circa 60%, iar cel asupra swapurilor pe riscul de credit pe 5 ani a rămas pozitiv. În afara eșantionului, EFRM împreună cu CISS prognozează lunile volatile cu o AUC de 0,731, față de 0,708 doar pentru EFRM și 0,673 doar pentru CISS.

@practice VaR proprie a unei firme nu vede contagiunea; urmăriți alături de ea un indicator sectorial.

## AIDA 2026: riscul extrem al firmelor poluante anticipă prima de carbon {h=9423a50f}

La conferința AIDA (5 iunie 2026), prof. Wolfgang Karl Härdle a prezentat o lucrare comună cu R. Wang și L. Zhang ([diapozitive](https://github.com/danpele/EMQA/blob/main/resources/aida2026/wang_carbon_risk_dynamics.pdf); lucrarea: [doi:10.2139/ssrn.5757742](https://doi.org/10.2139/ssrn.5757742)). Punctul de plecare este puzzle-ul primei de carbon. Ipoteza compensării riscului spune că firmele cu emisii mari ar trebui să cîștige mai mult, deoarece investitorii cer un randament mai mare pentru riscul lor de tranziție; preferința pentru activele verzi spune că firmele cu emisii reduse ar trebui să cîștige mai mult. Lucrarea folosește acțiuni din China, din iulie 2014 pînă în februarie 2025: cele mai mari 50 de firme poluante și cele mai mari 50 de firme cu emisii reduse, alese din primele și ultimele 30% după emisiile de CO$_2$ raportate la venituri. Pentru fiecare firmă, cuantila de 5% a randamentului este regresată prin LASSO pe celelalte firme și pe factori macroeconomici, inclusiv volatilitatea prețului carbonului, pe o fereastră de 63 de zile, exact ca pentru EFRM din secțiunea anterioară. Indicatorul dinamic al riscului de carbon (CARDI) este raportul dintre indicatorul de risc financiar (FRM), adică penalizarea LASSO medie $\lambda$, al firmelor poluante și cel al firmelor cu emisii reduse.

Regimurile de risc ridicat ale CARDI coincid cu evenimente neașteptate sau incipiente ale politicii climatice. Ambele ipoteze ale puzzle-ului sînt valabile, în funcție de CARDI: o creștere a CARDI anticipă o primă mai mare a firmelor cu emisii reduse, ajustată pentru factorii de risc, în luna următoare, cu un coeficient de 0,022 pentru cuantila de 5%, pe 118 luni, în timp ce rapoartele construite din conectivitate, din co-mișcarea extremă sau din VaR condiționată nu o anticipează. O strategie cu poziție long pe firmele cu emisii reduse și short pe cele poluante, deschisă doar cînd CARDI crește, a obținut un randament cumulat de 115,84% în 2015–2024, cu un raport Sharpe de 0,72, față de 89,03% și 0,49 pentru aceeași poziție menținută permanent. Pentru o companie energetică, raportul arată ce parte a sectorului poartă riscul extrem.

@practice într-o firmă de petrol și gaze, urmăriți CARDI: cînd crește, investitorii preferă firmele cu emisii reduse.

# Studiu de caz: creșterea prețurilor din toamna anului 2026

În 2026, prețul din România s-a dublat între iunie și octombrie fără nicio zi cu variație violentă. Studiul de caz arată că modelele VaR au trecut testele, în timp ce nevoia de lichidități a unui furnizor s-a dublat, și se încheie cu o listă de verificare pentru biroul de risc.

## Studiu de caz: în 2026 prețul s-a dublat treptat, fără salturi {h=d7a38358}

Media lunară a prețului PZU a fost 122,99 EUR/MWh în iunie 2026 și 239,32 în octombrie, cu un maxim de 323,76 EUR/MWh la 29 octombrie 2026. Creșterea s-a produs treptat, prin multe variații zilnice moderate, nu prin cîteva salturi. În cele 153 de zile ale perioadei, o VaR corectă de 99% ar fi trebuit depășită de 1,5 ori; FHS a fost depășită de 2 ori, HS o dată, iar VaR normală de 3 ori. Judecînd după VaR zilnică, nu s-a întîmplat nimic alarmant.

@practice o creștere lentă trece testele VaR, dar consumă lichidități: urmăriți și nivelul prețului.

@chart case2026
Prețul de bază PZU din România și prognozele VaR de 99%, 1 iunie – 31 octombrie 2026, cu depășirile marcate.

## Studiu de caz: în 2026 pericolul a fost lipsa de lichidități, nu VaR zilnică {h=27678bb2}

Riscul de piață aproape nu s-a modificat. VaR FHS de 99% a fost 61,64 EUR/MWh în iunie și 67,50 în octombrie, iar testul ES din 2023 încoace nu respinge FHS ($Z_2$ = −0,083). Nevoia de lichidități s-a dublat însă. Garanția pentru 100 MW pe PZU, calculată din cuantila de 99% lărgită, a crescut de la 0,416 la 0,776 milioane EUR pe zi. Prețul ar fi depășit limita garanției în 3 zile, iar fără lărgire în 6.

Factura lunară a furnizorului pentru 100 MW a crescut cu +25,1% în august (2,38 milioane EUR), cu +16,2% în septembrie (1,86 milioane) și cu +34,0% în octombrie (4,68 milioane). Fiecare lună a rămas sub limita de 99% de +50,5%, dar cele trei depășiri au venit la rînd, iar costul lor se cumulează. Factorii au fost externi: prețul gazelor TTF a crescut de la 44,94 la 86,81 EUR/MWh între iunie și octombrie, Brent a ajuns la 108,34 USD în octombrie, iar prețul din Germania–Luxemburg la 169,48 EUR/MWh.

@practice un raport de risc are nevoie, alături de VaR, de o secțiune de lichiditate: garanții, marje și depășirea cumulată a costului lunar.

## Lista de verificare a biroului de risc pentru prețurile energiei {h=734519db}

Cursul poate fi rezumat în patru pași pentru un birou de risc.

- **Măsurarea.** Definiți poziția și semnul pierderii, de cumpărător sau de vînzător. Folosiți numai datele cunoscute la închiderea licitației. Raportați VaR și ES obținute prin două metode, dintre care una filtrată (FHS sau EVT).
- **Verificarea.** Aplicați testele Kupiec și Christoffersen și semaforul Basel pe mai mulți ani, inclusiv 2021–2022. Folosiți testul $Z_2$ pentru ES și nu ierarhizați modelele pe baza cîtorva zile extreme.
- **Decizia.** Stabiliți limite în EUR de VaR, transformate zilnic în MW. Calculați garanțiile și liniile de credit din cuantile ridicate, bine calibrate. Păstrați o rezervă de lichidități pentru marja cerută într-o criză.
- **Raportarea.** În EUR și în MW, lunar, cu lichiditatea alături de riscul de piață.

@practice tema 2 (sarcina 5) aplică această listă fluxului de numerar al rolului dumneavoastră.

# Recapitulare

Recapitularea verifică ideile principale prin cinci întrebări scurte, rezumă cursul și trimite la cercetările grupului nostru și la lecturi suplimentare.

## Verifică-te {h=2a7eb881}

1. VaR de 99% pe o zi, pentru 100 MW, este de 162 de mii EUR. Ce promite această cifră și ce nu spune? Răspuns: în aproximativ o zi din 100, pierderea ar trebui să o depășească. Cifra nu spune nimic despre mărimea pierderii în acele zile, pe care o măsoară ES (162 de mii EUR la 97,5%).
2. În ultimele 250 de zile, VaR de 99% a fost depășită de 7 ori. În ce zonă a semaforului se află modelul și ce arată testul Kupiec? Răspuns: în zona galbenă (5–9). Testul Kupiec dă $\text{LR}_{uc}$ = 5,50 și $p$ = 0,019, deci ipoteza este respinsă la pragul de 5%. Recalibrați modelul, de exemplu trecînd de la HS la FHS, și continuați monitorizarea.
3. Directorul financiar calculează VaR pe 10 zile ca $\sqrt{10}$ înmulțit cu VaR pe o zi. Este o abordare prudentă sau risipitoare pentru energie? Răspuns: risipitoare. Prețurile energiei revin spre medie, iar cuantila empirică de 99% pe 10 zile este doar de 1,72 ori cea pe o zi în România, nu de 3,16 ori.
4. Ați vîndut 100 de loturi Brent pentru a vă acoperi producția, iar astăzi prețul crește cu 5 USD pe baril. Ce se întîmplă diseară? Răspuns: plătiți o marjă de variație de 100 × 1 000 × 5 = 500 000 USD în numerar. Țițeiul pe care îl veți vinde mai tîrziu valorează mai mult, dar banii pleacă astăzi.
5. Prognoza dumneavoastră pentru cuantila de 99% a prețului de mîine a fost depășită în 111 zile din 3 585. Ce faceți? Răspuns: lărgiți coada cu o corecție conformală calculată din erorile recente. Acoperirea crește de la 96,90% la 98,47%, cu o garanție mai mare cu doar 7,5%.

## Recapitulare {h=d8e7a67e}

VaR este o cuantilă a pierderii de mîine, iar ES media pierderilor de dincolo de ea. Pe prețurile energiei, repartiția normală eșuează, metodele filtrate, FHS și EVT, se apropie cel mai mult de țintă, iar niciuna nu a fost corectă în 2021–2022. Aceleași cuantile stabilesc limitele de poziție, marjele la bursă și garanția pentru PZU. Studiul de caz din 2026 arată că lichiditatea, nu VaR, este prima afectată de o creștere a prețului. Cursul următor tratează acoperirea riscului cu instrumente derivate (cursul 5).

## Cercetările grupului nostru despre riscul pe piețele de energie {h=29baf521}

Trei lucrări recente ale grupului nostru, de la Academia de Studii Economice din București și de la Academia Română, Institutul de Prognoză Economică, tratează temele acestui curs. Rezultatele de mai jos sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.

- **Indicatorul de risc financiar al sectorului energetic** (Toma, Dima, Grecu, Pele și Lessmann, 2026). Lucrarea construiește un indicator de risc sistemic pentru sectorul energetic din UE, din regresii cuantilice LASSO pe 100 de companii; indicatorul surprinde șocurile din 2020 și 2022 (studiul de caz C4).
- **Modele fundaționale pentru VaR și ES** (Jheng, Tak, Găman, Mazurencu-Marinescu-Pele și Pele, 2026). Lucrarea folosește zece serii de randamente zilnice din cinci piețe din Europa Centrală și de Est (CEE), inclusiv România, cu evaluare în afara eșantionului în 2018–2025. Aplică trei modele preantrenate pentru serii de timp, fără reantrenare, comparate cu metode clasice, și le evaluează cu testele Kupiec, Christoffersen și Acerbi–Székely și cu semaforul Basel. Cel mai bun model neajustat are 90% din ferestre în zona verde, proporție care urcă la 96,7% după o calibrare conformală glisantă, cel mai bun rezultat dintre toate modelele.
- **Cît de precisă este o comparație a prognozelor ES?** (Pele și Mazurencu-Marinescu-Pele, 2026). Lucrarea transformă limita de precizie $(n\alpha)^{-1/2}$ a ES în patru diagnostice practice, inclusiv o regulă pentru mărimea eșantionului. Pe active financiare globale, aproximativ una din cinci comparații între prognoze ES nu este concludentă la nivelurile de risc cerute de reglementare.

## Lecturi și resurse suplimentare {h=d43472bf}

- **McNeil, Frey și Embrechts**, *Quantitative Risk Management*, ediția a 2-a: VaR, ES, EVT și testare retrospectivă.
- **Christoffersen**, *Elements of Financial Risk Management*, ediția a 2-a: FHS și testare retrospectivă, cu exerciții.
- **BCE**, Financial stability risks from energy derivatives markets (2022): [ecb.europa.eu](https://www.ecb.europa.eu/pub/financial-stability/fsr/special/html/ecb.fsrart202211_01~173476301a.en.html).
- **Acest curs**: cod, date și notebook-uri Jupyter pe [github.com/danpele/EMQA](https://github.com/danpele/EMQA); notebook-ul reproduce toate graficele și cifrele din acest curs.
- **Tema 2**, sarcina 5: VaR și ES ale fluxului de numerar al rolului dumneavoastră, cu testare retrospectivă.
- **OPCOM**, procedura privind garanțiile pentru PZU: [opcom.ro](https://www.opcom.ro).

# Anexă

Anexa prezintă deducerea formulelor ES pentru repartițiile normală, Student-t și Pareto generalizată, cele trei teste retrospective în detaliu și tabelul de testare pentru Germania–Luxemburg.

## Anexa A: ES pentru repartițiile normală și Student-t {h=c52f433e}

Pentru repartiția normală, ES este media pierderii de peste cuantilă:

$$ \text{ES}^{N}_\alpha=\frac{1}{1-\alpha}\int_{z_\alpha}^{\infty}(\mu+\sigma z)\varphi(z)\,dz=\mu+\sigma\frac{\varphi(z_\alpha)}{1-\alpha} $$ {#eq:app-normal}

unde $z$ este variabila normală standard, $\varphi$ densitatea ei, $z_\alpha$ cuantila de ordin $\alpha$, iar $\mu$ și $\sigma$ media și abaterea standard. Pasul folosește egalitatea $\int_{c}^{\infty}z\varphi(z)\,dz=\varphi(c)$, deoarece derivata lui $\varphi$ este $-z\varphi$. La $\alpha$ = 0,975, ES$^N$ = $\mu$ + 2,338$\sigma$, aproape egal cu VaR$^N_{0,99}$ = $\mu$ + 2,326$\sigma$: de aceea FRTB a putut înlocui o măsură cu cealaltă.

Pentru repartiția Student-t,

$$ \text{ES}^{t}_\alpha=m+s\,\frac{g_\nu(t_{\nu,\alpha})}{1-\alpha}\cdot\frac{\nu+t_{\nu,\alpha}^{2}}{\nu-1}, \quad \nu>1 $$ {#eq:app-t}

unde $m$, $s$ și $\nu$ sînt locația, scala și gradele de libertate, iar $t_{\nu,\alpha}$ și $g_\nu$ cuantila și densitatea repartiției Student-t standard. Formula rezultă din $\int_c^\infty x\,g_\nu(x)\,dx=g_\nu(c)\,(\nu+c^2)/(\nu-1)$. Pentru $\nu\le 1$ media, deci și ES, nu există. Estimăm zilnic $(m,s,\nu)$ prin MLE și menținem $\nu$ cel puțin la 2,2, pentru ca varianța să existe (McNeil, Frey și Embrechts, 2015).

## Anexa B: VaR și ES din coada Pareto generalizată {h=a4034457}

Conform teoremei Pickands–Balkema–de Haan, pentru un prag $u$ ridicat, excesele peste $u$ urmează aproximativ o repartiție GPD, pentru aproape orice repartiție. Probabilitatea din coadă peste $u$ este atunci

$$ \Pr(Z>z)\approx\frac{N_u}{n}\Big(1+\xi\frac{z-u}{\beta}\Big)^{-1/\xi}, \quad z>u $$ {#eq:app-tail}

unde $N_u/n$ este proporția celor $n$ observații care depășesc $u$, $\xi$ parametrul de formă, iar $\beta$ scala. Punînd $\Pr(Z>\text{VaR}_\alpha)=1-\alpha$ și rezolvînd, obținem

$$ \text{VaR}_\alpha=u+\frac{\beta}{\xi}\Big[\Big(\frac{n(1-\alpha)}{N_u}\Big)^{-\xi}-1\Big] $$ {#eq:app-var}

Pentru GPD, excesul mediu peste un nivel $v$ situat deasupra lui $u$ este liniar în $v$, cu condiția $\xi<1$:

$$ \E[Z-v\mid Z>v]=\frac{\beta+\xi(v-u)}{1-\xi} \quad\Rightarrow\quad \text{ES}_\alpha=\frac{\text{VaR}_\alpha+\beta-\xi u}{1-\xi} $$ {#eq:app-es}

Semnul lui $\xi$ clasifică coada: $\xi>0$ înseamnă coadă groasă, $\xi=0$ coadă exponențială, iar $\xi<0$ coadă mărginită. EVT condiționată aplică aceste formule șocurilor standardizate $z_t=e_t/\sigma_t$ și apoi calculează VaR$_t=\mu_{d(t)}+\sigma_t\,$VaR$^z_\alpha$, unde VaR$^z_\alpha$ este cuantila GPD a șocurilor (McNeil și Frey, 2000).

## Anexa C: cele trei teste retrospective, în detaliu {h=f8689862}

**Kupiec și Christoffersen.** În ipoteza $H_0$, fiecare $I_t$ este o variabilă Bernoulli($p$) independentă, iar $\text{LR}_{uc}$ compară proporția promisă $p$ cu proporția observată $\hat p$. $\text{LR}_{ind}$ compară un lanț Markov de ordinul întîi cu ipoteza de independență. Statistica comună $\text{LR}_{cc}$ = $\text{LR}_{uc}$ + $\text{LR}_{ind}$ urmează repartiția $\chi^2_2$, cu valoarea critică la 5% de 5,99.

**Semaforul Basel.** Pentru un model corect, numărul depășirilor în 250 de zile este $x\sim$ Binomial(250; 0,01). Atunci $\Pr(x\le4)$ = 89,22%, $\Pr(5\le x\le9)$ = 10,76% și $\Pr(x\ge10)$ = 0,025% (BCBS, 1996).

**Testul Acerbi–Székely.** Atunci cînd VaR și ES sînt corecte, $\E[L_tI_t]=(1-\alpha)\text{ES}_t$, deci $\E[Z_2]=0$. $Z_2$ combină o eroare de VaR, adică un număr greșit de $I_t$, cu o eroare de ES, adică o mărime greșită a pierderilor din coadă; ES nu este elicitabil (Gneiting, 2011), de aceea se testează împreună cu VaR. Valoarea $p$ se obține din 2 000 de traiectorii simulate, fiecare zi fiind extrasă din repartiția prognozată de modelul respectiv: fereastra pentru HS, $\mu+\sigma z^*$ pentru FHS, unde $z^*$ este un șoc reeșantionat, și GPD peste $u$ pentru EVT (Acerbi și Székely, 2014).

## Anexa D: aceeași testare retrospectivă pentru Germania–Luxemburg {h=d3625046}

Testarea retrospectivă pentru zona Germania–Luxemburg acoperă intervalul 1 ianuarie 2017 – 31 octombrie 2026, adică 3 591 de zile, cu aceleași metode și ferestre ca pentru România.

| DE-LU | 95%: proporția | Kupiec p | 99%: număr | proporția | Kupiec p | Chr. p | roșu, % | Z2 | p |
|---|---|---|---|---|---|---|---|---|---|
| HS | 6,38 | <0,001 | 60 | 1,67 | <0,001 | 0,998 | 9,2 | 0,529 | <0,001 |
| Normală | 6,66 | <0,001 | 107 | 2,98 | <0,001 | 0,332 | 16,3 | 1,250 | <0,001 |
| Student-t | 8,33 | <0,001 | 67 | 1,87 | <0,001 | 0,174 | 9,0 | 0,617 | 0,001 |
| FHS | 5,82 | 0,028 | 58 | 1,62 | <0,001 | 0,948 | 2,7 | 0,305 | 0,009 |
| EVT | 5,93 | 0,013 | 53 | 1,48 | 0,007 | 0,811 | 0,7 | 0,283 | 0,007 |

Clasamentul este același ca în România: repartiția normală are cele mai slabe rezultate, iar metodele filtrate cele mai bune.
