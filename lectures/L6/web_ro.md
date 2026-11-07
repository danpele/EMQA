<!--
Versiunea web a cursului 6 (RO). Construită în web/L6_ro.html de lectures/common/build_web_lecture.py (formatul: vezi docstring-ul).
Hash-urile slide-urilor: python3 build_web_lecture.py 6 --frames
-->

## @intro

Centralele solare și eoliene își oferă producția la un preț apropiat de zero, pentru că soarele și vîntul nu costă nimic. Fiecare parc nou împinge astfel în afara pieței centralele mai scumpe și reduce prețul în orele în care produce, adică exact în orele în care produc și toate celelalte parcuri de același tip. Cursul de față răspunde la cîteva întrebări legate de acest mecanism: ce se întîmplă cu venitul unui parc solar, de ce prețul din piața pentru ziua următoare (PZU) coboară acum frecvent sub zero la amiază și cît poate cîștiga, de fapt, o baterie care cumpără energie ieftină la prînz și o vinde seara.

Răspunsurile contează pentru toți participanții la piața din România: pentru dezvoltatorii de parcuri solare și eoliene și pentru băncile care îi finanțează, pentru furnizorii și consumatorii industriali care cumpără din PZU, pentru dezvoltatorii de baterii care își dimensionează investiția și pentru Transelectrica, operatorul de transport care gestionează interconexiunile. Puterea solară instalată în România a crescut de 2,4 ori între 2019 și 2025, iar în 2025 un megawatt-oră (MWh) solar a obținut doar 59,4% din prețul mediu al anului.

Toate cifrele provin din date reale, descărcate: prețuri orare și pe 15 minute pentru România și pentru trei piețe vecine sau de referință, producția solară, eoliană și a bateriilor, curbele reale de ofertă și de cerere ale operatorului pieței din România și puterea instalată, din 2019 pînă la 31 octombrie 2026.

@goals
- **Măsurați** cît reduc producția solară și cea eoliană, cu cost marginal aproape zero, prețul din PZU, atît pe ofertele reale, cît și cu o regresie pe date orare.
- **Calculați** prețul capturat și rata de captare pentru solar și eolian și explicați canibalizarea: cu cît se construiește mai mult solar, cu atît scade prețul pe care îl obține.
- **Numărați** corect prețurile negative, în ore echivalente, evaluați oprirea unui parc și interpretați profilul zilnic al prețului pe intervale de 15 minute.
- **Estimați** venitul din arbitraj al bateriilor de 1, 2 și 4 ore cu un program liniar (LP), cu informație perfectă și cu reguli de prognoză, pe prețuri orare și pe 15 minute, în România și la vecini.

# Sursele regenerabile și ordinea de merit

Secțiunea măsoară cu cît reduc producția solară și cea eoliană prețul din PZU, întîi pe curbele reale de ofertă și de cerere dintr-o zi, apoi cu o regresie pe aproape patru ani de date orare. Punctul de plecare este creșterea puterii solare instalate, care face întrebarea urgentă.

## Lucrăm numai cu date reale: prețuri, producție, oferte și putere instalată {h=f99b44c2}

Cursul folosește exclusiv date reale. Prețurile pentru ziua următoare acoperă patru zone de ofertare: România (RO), Bulgaria (BG), Ungaria (HU) și zona Germania–Luxemburg (DE-LU). Ele sînt stabilite de operatorul pieței de energie electrică și de gaze naturale din România (OPCOM), de bursa independentă de energie din Bulgaria (IBEX), de bursa de energie din Ungaria (HUPX) și de bursa europeană de energie EPEX SPOT (EPEX) și sînt preluate prin energy-charts.info, portalul de date al Institutului Fraunhofer pentru Sisteme de Energie Solară (ISE). Prețurile sînt orare, iar de la 1 octombrie 2025 sînt stabilite pentru fiecare sfert de oră.

Producția solară, eoliană și a bateriilor, precum și consumul de energie electrică provin de la Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E), cu Transelectrica drept furnizor de date pentru România; ele sînt disponibile la 15 minute pentru România și Ungaria și orar pentru Bulgaria. Curbele reale de ofertă și de cerere din PZU, pentru două sferturi de oră, provin de la OPCOM, în fișiere Extensible Markup Language (XML), iar puterea instalată este anuală, din ENTSO-E prin energy-charts.info.

Perioada analizată începe în 2019 și se încheie la 31 octombrie 2026, ultima lună completă. Pe această pagină, „2026” înseamnă ianuarie–octombrie 2026, iar „ultimele 12 luni” înseamnă noiembrie 2025 – octombrie 2026. Zilele de livrare se definesc după ora Europei Centrale (CET). Energia este întotdeauna puterea medie, în megawați (MW), înmulțită cu durata, astfel încît un interval de tranzacționare (MTU, *market time unit*) de 15 minute contează 0,25 h.

## Puterea solară instalată în România a crescut de 2,4 ori între 2019 și 2025 {h=2e0f3d08}

Puterea solară instalată în România a urcat de la 1,16 gigawați (GW) la sfîrșitul anului 2019 la 2,79 GW la sfîrșitul anului 2025, adică de 2,4 ori. Producția a urmat aceeași direcție: între ianuarie și octombrie, parcurile solare din România au produs 2,53 terawați-oră (TWh) în 2025 și 4,32 TWh în 2026. Raportată la consum, producția solară a acoperit 2,3% în 2019 și 10,2% în 2026.

Vecinii au crescut și mai repede. La sfîrșitul anului 2025, Bulgaria avea 7,2 GW de putere solară, iar Ungaria 9,0 GW, ambele mult peste România. Cum cele trei piețe sînt cuplate, această putere regională contează pentru prețurile din România la fel de mult ca parcurile românești. Producția măsurată de ENTSO-E poate omite panourile de pe acoperișuri, așa că energia solară reală este ceva mai mare.

@practice un parc solar nou vinde în aceleași ore însorite ca toate parcurile existente, din România și din țările vecine.

@chart solar_growth
Puterea solară instalată la sfîrșitul fiecărui an în România, Bulgaria și Ungaria, 2019–2025, și producția solară a României.

## Oferta cu cost zero deplasează curba ofertei spre dreapta și reduce prețul de închidere {h=b417e380}

În piața pentru ziua următoare, prețul fiecărui sfert de oră se formează la intersecția dintre curba ofertei și curba cererii. Producția solară și cea eoliană se oferă aproape de zero, așa că adăugarea lor mută spre dreapta toate ofertele mai scumpe, iar intersecția cu cererea coboară. Acesta este efectul ordinii de merit (*merit-order effect*) (Sensfuß, Ragwitz & Genoese, 2008). Formal, dacă se oferă în plus $X$ MW la preț zero, noul preț de închidere $p^*(X)$ rezultă din

$$ S(p)+X\cdot\mathbf 1[p\ge 0]=D(p)\ \Rightarrow\ p^*(X) $$ {#eq:merit}

iar sensibilitatea lui față de $X$ este

$$ \frac{\mathrm dp^*}{\mathrm dX}=-\frac{1}{S'(p^*)-D'(p^*)} $$ {#eq:slope}

unde $S(p)$ este cantitatea, în MW, oferită la prețuri cel mult egale cu $p$, $D(p)$ cantitatea cerută la prețuri de cel puțin $p$, $X$ puterea suplimentară oferită la 0 EUR/MWh (euro, EUR, pe megawatt-oră), $\mathbf 1[p\ge 0]$ este egal cu unu cînd prețul este nenegativ și cu zero în rest, iar $S'$ și $D'$ sînt pantele celor două curbe, în MW pentru 1 EUR/MWh.

Relația @eq:slope arată că efectul depinde de forma curbelor în jurul prețului. Dacă sînt plate, multe oferte se află aproape de preț, iar un parc nou abia îl mișcă; dacă sînt abrupte, un volum mic în plus schimbă mult prețul. Pe curbele OPCOM din 21 octombrie 2026, pentru intervalul 12:00–12:15, prețul a fost 152,23 EUR/MWh și doar 34 MW au fost oferiți între 1 EUR/MWh și acest preț: curba era foarte abruptă.

@practice cu cît curba locală este mai abruptă, cu atît un parc nou își modifică mai mult propriul preț.

## Pe ofertele din România, 40 MW în plus la preț zero coboară prețul de la amiază sub 50 EUR/MWh {h=fd0609c0}

Graficul aplică relația @eq:merit pe curbele reale din 21 octombrie 2026. La amiază, numai 25 MW în plus la preț zero coboară prețul de la 152,23 la 131,40 EUR/MWh, iar 40 MW îl duc sub 50 EUR/MWh. Seara, pentru aceeași scădere sînt necesari 225 MW, deoarece importul net de 1 054 MW adîncește curba.

Aceste cifre trebuie citite ca o limită superioară. Recalcularea păstrează fluxurile transfrontaliere, blocurile și ordinele orare la valorile acceptate (Anexa C). În piața cuplată reală, o parte din producția suplimentară de la amiază se exportă, deci prețul din România scade mai puțin. Exercițiul arată cît de subțire este, la amiază, piața strict locală și de ce contează interconexiunile.

@practice pentru Transelectrica: interconexiunile, nu centralele locale, dau profunzime prețului de la amiază.

@chart merit_shift
Prețul de închidere recalculat pe curbele PZU din 21 octombrie 2026, în funcție de MW adăugați ca ofertă la 0 EUR/MWh sau ca cerere la orice preț, la amiază (12:00–12:15) și seara.

## În piața cuplată, 1 GW solar în plus reduce prețul din România cu aproximativ 27 EUR/MWh {h=85774493}

Pentru a măsura efectul în piața cuplată reală, cursul estimează o regresie pe date orare. În aceeași lună, la aceeași oră și în aceeași zi a săptămînii, orele cu mai mult soare și vînt sînt mai ieftine; regresia măsoară cu cît:

$$ P_t=\underbrace{\alpha_{m(t)}+\gamma_{h(t)}+\delta_{w(t)}}_{\text{efecte fixe}}+\beta_L L_t+\beta_W W_t+\beta_S S_t+\varepsilon_t $$ {#eq:regression}

unde $P_t$ este prețul orar, în EUR/MWh, $L_t$, $W_t$ și $S_t$ sînt consumul, producția eoliană și producția solară, în GW, $\alpha_{m(t)}$ este o constantă pentru luna orei $t$ (preia prețul gazelor și al carbonului), $\gamma_{h(t)}$ o constantă pentru ora din zi, $\delta_{w(t)}$ o constantă pentru ziua săptămînii, iar $\varepsilon_t$ eroarea. Modelul se estimează prin metoda celor mai mici pătrate (OLS, *ordinary least squares*).

Pe 33 600 de ore, din 2023 pînă în octombrie 2026, $R^2$ = 0,65. Fiecare GW solar reduce prețul cu 26,7 EUR/MWh, fiecare GW eolian cu 15,3, iar fiecare GW de consum îl crește cu 40,7. Eroarea standard (SE) a coeficientului solar este 2,2, robustă la heteroscedasticitate și autocorelare (HAC). La amiază, în 2026, producția solară medie a fost de 1,62 GW, ceea ce corespunde unui preț mai mic cu 43,3 EUR/MWh. Este o asociere, nu un efect cauzal: regresia controlează calendarul, nu tot ce variază odată cu soarele (Cludius et al., 2014; Würzburg et al., 2013).

@practice un furnizor care cumpără blocuri de amiază le plătește mai puțin în zilele însorite, cu aproximativ această sumă.

## Prețul crește cu consumul rezidual; orele sub 2 GW au ajuns la 9,0% în 2026 {h=5e1b9955}

Consumul rezidual este consumul minus producția eoliană și cea solară, $L_t-W_t-S_t$, adică cererea rămasă pentru celelalte centrale și pentru import. El rezumă într-un singur număr ce lasă sursele regenerabile restului sistemului. Cu aceleași efecte fixe ca în @eq:regression, un GW de consum rezidual în plus crește prețul cu 28,3 EUR/MWh (SE 0,9).

Graficul grupează orele după consumul rezidual, în intervale de 0,5 GW, și arată prețul mediu din fiecare interval. Curba urcă abrupt: orele cu consum rezidual mic sînt ieftine, cele cu consum rezidual mare sînt scumpe. S-a schimbat însă frecvența cu care se ajunge în partea stîngă a curbei. Orele cu consum rezidual sub 2 GW reprezentau 0,1% din total în 2023 și 9,0% în 2026.

@practice un producător hidro păstrează apa pentru orele cu consum rezidual mare, cînd fiecare GW valorează cel mai mult.

@chart resid_price
Prețul orar mediu în funcție de consumul rezidual (intervale de 0,5 GW, cu cel puțin 20 de ore), din 2023 pînă în octombrie 2026, pe ani.

## @end

Sursele regenerabile cu cost zero deplasează curba ofertei și reduc prețul: în piața cuplată, cu circa 27 EUR/MWh pentru fiecare GW solar, iar pe ofertele strict locale mult mai mult. Orele cu consum rezidual foarte mic, odinioară rare, au devenit obișnuite.

# Prețul capturat și canibalizarea

Un parc solar nu încasează prețul mediu al anului, ci prețul orelor în care produce. Secțiunea definește prețul capturat și rata de captare, le urmărește an de an în România și arată că, pe măsură ce ponderea sa crește, solarul își reduce propriul preț: canibalizarea.

## Prețul capturat este prețul mediu ponderat cu producția centralei {h=186a8c5f}

Prețul capturat (CP, *capture price*) este prețul mediu ponderat cu producția centralei; prețul de bază $B$ este media simplă pe toate intervalele; raportul lor este rata de captare (CR, *capture rate*), numită și factor de valoare:

$$ \mathrm{CP}=\frac{\sum_t P_t G_t\Delta_t}{\sum_t G_t\Delta_t},\qquad B=\frac{\sum_t P_t\Delta_t}{\sum_t\Delta_t} $$ {#eq:capture}

$$ \mathrm{CR}=\frac{\mathrm{CP}}{B}=1+\frac{\mathrm{Cov}_\Delta(P,G)}{\bar P\,\bar G} $$ {#eq:cr}

unde $P_t$ este prețul intervalului $t$, $G_t$ producția centralei (sau a tehnologiei), în MW, $\Delta_t$ durata intervalului (1 h sau, din octombrie 2025, 0,25 h), $\bar P$ și $\bar G$ mediile prețului și producției ponderate cu durata, iar $\mathrm{Cov}_\Delta$ covarianța lor ponderată cu durata (demonstrația este în Anexa A).

A doua formă din @eq:cr explică tot ce urmează. Rata de captare este sub unu exact atunci cînd producția este mare în intervalele ieftine, adică atunci cînd prețul și producția sînt corelate negativ. Pentru solarul din România, în ianuarie–octombrie 2026, CP a fost 85,0 EUR/MWh, iar $B$ = 137,5 EUR/MWh, deci CR = 61,9%; corelația dintre preț și producție a fost −0,43. Eolianul din România a avut, în aceeași perioadă, CR = 103,0%: vîntul bate și noaptea, și iarna, cînd prețurile sînt mari (Hirth, 2013; Hirth, Ueckerdt & Edenhofer, 2016).

@practice prețul unui contract pe termen lung pentru energie solară (PPA, *power purchase agreement*) pornește de la prețul capturat, nu de la prețul de bază.

## Rata de captare a solarului în România a scăzut de la 104% în 2019 la 59% în 2025 {h=bd6cff79}

Graficul urmărește ratele de captare ale solarului și eolianului din România începînd cu 2019. În 2019, solarul a obținut chiar puțin peste prețul mediu: era o tehnologie mică, a cărei producție de la amiază întîlnea o cerere ridicată. Scăderea începe în 2023, odată cu creșterea producției solare, și ajunge la 59% în 2025. În 2026 rata este 61,9%, deși producția a crescut cu 71% față de aceleași luni din 2025.

Eolianul se comportă altfel: rata lui de captare variază între 88% și 103%, fără tendință, pentru că producția eoliană a României nu a crescut. Canibalizarea nu este deci o trăsătură a surselor regenerabile în general, ci a unei tehnologii a cărei producție se concentrează în aceleași ore și crește repede.

@practice o bancă ce finanțează un proiect solar trebuie să înmulțească prețul de bază cu rata de captare.

@chart capture_rates
Ratele anuale de captare ale solarului și eolianului din România, din 2019 pînă în octombrie 2026.

## În 2025, un MWh solar din România a obținut cu 43,9 EUR mai puțin decît prețul de bază {h=61411f4c}

Tabelul conține cifrele din spatele graficului: prețul de bază $B$, prețurile capturate CP ale solarului și eolianului (ambele în EUR/MWh), ratele de captare și producția anuală. Coloana $B-\mathrm{CP}$ este reducerea datorată profilului solar: cu cît mai puțin decît prețul mediu obține un MWh solar.

| Anul | $B$ | CP solar | CR solar, % | $B-\mathrm{CP}$ | CP eolian | CR eolian, % | TWh solar | TWh eolian |
|---|---|---|---|---|---|---|---|---|
| 2019 | 50,4 | 52,7 | 104,5 | −2,3 | 47,2 | 93,6 | 1,37 | 6,68 |
| 2020 | 39,5 | 36,4 | 92,2 | +3,1 | 36,6 | 92,6 | 1,34 | 6,89 |
| 2021 | 111,4 | 100,6 | 90,3 | +10,8 | 111,0 | 99,6 | 1,29 | 6,44 |
| 2022 | 265,3 | 264,0 | 99,5 | +1,3 | 234,4 | 88,4 | 1,37 | 6,92 |
| 2023 | 103,7 | 83,2 | 80,2 | +20,6 | 101,0 | 97,4 | 1,46 | 7,45 |
| 2024 | 103,5 | 68,0 | 65,7 | +35,5 | 93,4 | 90,2 | 2,09 | 6,34 |
| 2025 | 108,2 | 64,2 | 59,4 | +43,9 | 106,7 | 98,7 | 2,72 | 5,88 |
| 2026* | 137,5 | 85,0 | 61,9 | +52,4 | 141,6 | 103,0 | 4,32 | 5,27 |

Asteriscul marchează 2026 = ianuarie–octombrie 2026. Anul 2022, al crizei energetice, a avut prețuri foarte mari pentru toate tehnologiile, așa că ratele lui de captare spun puțin despre canibalizare. Începînd din 2022, reducerea suportată de solar crește în fiecare an: 20,6 EUR/MWh în 2023, 35,5 în 2024, 43,9 în 2025 și 52,4 în primele zece luni din 2026.

@practice diferența $B-\mathrm{CP}$ este un cost suportat de dezvoltatorul solar și a crescut în fiecare an din 2022.

## Cînd ponderea solarului în consumul lunii crește cu un punct procentual, rata de captare solară scade cu circa 4,2 puncte {h=75c91f5b}

Canibalizarea se poate măsura direct, punînd în legătură rata de captare solară a fiecărei luni cu ponderea producției solare în consumul acelei luni:

$$ \mathrm{CR}_m=a+b\,s_m+u_m $$ {#eq:cannibal}

unde $\mathrm{CR}_m$ este rata de captare solară din luna $m$, în procente, $s_m$ producția solară din luna $m$, ca procent din consum, $a$ și $b$ sînt termenul liber și panta, iar $u_m$ eroarea.

Pentru România, pe 94 de luni, panta estimată este $\hat b$ = −4,20 (SE 1,03), cu $R^2$ = 0,53: fiecare punct procentual în plus al solarului în consumul lunii reduce rata de captare cu circa 4,2 puncte. Aceeași regresie dă −2,14 pentru Ungaria și −1,32 pentru Bulgaria. Panta României este cea mai abruptă și pentru că prețul din România scade și cu producția solară a vecinilor, care crește odată cu cea românească; regresia atribuie o parte din efectul regional ponderii României (López Prol, Steininger & Zilberman, 2020).

@practice pentru a prognoza venitul unui parc, prognozați producția solară a regiunii, nu doar pe cea a României.

@chart cannibal
Rata lunară de captare solară în funcție de ponderea producției solare în consum, în România, Bulgaria și Ungaria, cu dreapta de regresie pentru România.

## Regiunea se canibalizează împreună: ratele de captare din România, Bulgaria și Ungaria au scăzut simultan {h=a3bd24c1}

Graficul compară ratele anuale de captare solară din cele trei piețe cuplate. Ele au scăzut împreună: în 2025, rata a fost 59,4% în România, 68,6% în Bulgaria și 57,5% în Ungaria. Piețele cuplate își împart surplusul de la amiază, așa că un parc dintr-o țară resimte și parcurile construite în celelalte.

În 2026, rata din Bulgaria a urcat la 77,1%, în paralel cu extinderea bateriilor bulgărești. Este o asociere, nu o dovadă, dar mecanismul este plauzibil: bateriile care se încarcă la amiază adaugă cerere exact cînd produce solarul și ridică prețul de la prînz.

@practice bateriile care se încarcă la amiază cresc prețul obținut de solar; un parc solar cîștigă și din bateriile altora.

@chart capture_region
Ratele anuale de captare solară în România, Bulgaria și Ungaria, din 2019 (Ungaria din 2020) pînă în octombrie 2026.

## În 2025, 32,1% din producția solară a României s-a vîndut în cele mai ieftine 10% dintre ore {h=7d17c525}

Canibalizarea se vede și altfel: se ordonează orele fiecărui an de la cea mai ieftină la cea mai scumpă și se calculează ce parte din energia solară a anului s-a produs pînă la fiecare rang. Graficul desenează această curbă pentru fiecare an. Dacă producția solară ar fi distribuită uniform în timpul anului, cele mai ieftine 10% dintre ore ar conține 10% din ea.

În 2019, cele mai ieftine 10% dintre ore conțineau doar 7,6% din producția solară a României. În 2025 conțineau 32,1%, iar în 2026, 23,4%. În 2025, 9,6% din producția solară s-a realizat la prețuri nule sau negative. O parte mare și în creștere a energiei solare se vinde tocmai atunci cînd energia electrică valorează cel mai puțin.

@practice cum am anunțat în cursul 1: un parc solar fără stocare își vinde o mare parte din producție în cele mai ieftine ore ale anului.

@chart cheap_hours
Ponderea cumulată a producției solare anuale a României în funcție de rangul orei, cu orele ordonate de la cea mai ieftină, cîte o curbă pentru fiecare an.

## @end

Rata de captare a solarului din România a scăzut de la 104,5% în 2019 la 59,4% în 2025, în timp ce eolianul a rămas aproape de 100%. Scăderea este regională și legată de creșterea producției solare: cu cît există mai mult solar, cu atît prețul obținut de el este mai mic.

# Prețurile negative

Din 2023, prețul din PZU coboară uneori sub zero. Secțiunea explică de ce un producător ar oferta plătind ca să producă, arată cum se numără corect prețurile negative, evaluează oprirea unui parc și arată ce dezvăluie piața pe 15 minute, ascuns de mediile orare.

## Un producător ofertează sub zero cînd oprirea îl costă mai mult decît plata pentru a produce {h=898be1f6}

O centrală ofertează la costul unui MWh suplimentar, minus ce primește sau economisește doar dacă funcționează:

$$ b_i=c_i-s_i-k_i $$ {#eq:bid}

unde $b_i$ este oferta centralei $i$, în EUR/MWh, $c_i$ costul ei marginal, $s_i$ sprijinul plătit pentru fiecare MWh produs, iar $k_i$ costul opririi și al repornirii, exprimat pe MWh. Cînd $s_i+k_i$ depășește $c_i$, oferta devine negativă. Sub zero ofertează două categorii de producători: cei a căror producție este plătită pe MWh printr-o schemă de sprijin sau printr-un contract și centralele care nu se pot opri ieftin, cum sînt cele nucleare și hidrocentralele pe firul apei (Fanone, Gamba & Prokopczuk, 2013).

Prețurile negative se numără în ore echivalente:

$$ h^{-}=\sum_t \Delta_t\,\mathbf 1[P_t<0] $$ {#eq:neghours}

unde $\Delta_t$ este durata intervalului $t$, în ore, iar $\mathbf 1[P_t<0]$ este egal cu unu cînd prețul intervalului este negativ. În 2025, România a avut 196 de ore cu preț negativ, cu un preț negativ mediu de −10,5 EUR/MWh; cel mai mic preț din 2026 a fost −99,75 EUR/MWh.

@practice un parc solar fără sprijin are $b_i\approx 0$, deci trebuie să se oprească imediat ce prețul devine negativ.

## România a avut 196 de ore cu preț negativ în 2025, Germania 575 {h=5460a741}

Graficul numără, cu relația @eq:neghours, orele cu preț negativ din fiecare an în România, Bulgaria, Ungaria și Germania. Germania, cu mult mai multă putere solară și eoliană, are mult mai multe: 575 de ore în 2025. România a avut 196.

Comparînd aceleași luni, ianuarie–octombrie, numărul a scăzut în 2026: în România de la 196 la 171,75 ore, în Ungaria de la 281 la 223,5 ore. Scăderea s-a produs deși producția solară a crescut. Explicațiile posibile sînt un nivel general mai ridicat al prețurilor și mai multe baterii care se încarcă la amiază, adăugînd cerere tocmai în orele care altădată deveneau negative. Regula de numărare este cea din cursul 1: un interval de 15 minute contează 0,25 h.

@practice un furnizor cu clienți industriali flexibili poate fi plătit pentru a consuma în aceste ore.

@chart neg_hours
Orele cu preț negativ din fiecare an în România, Bulgaria, Ungaria și Germania–Luxemburg, din 2022 pînă în octombrie 2026, în ore echivalente.

## Oprirea la prețuri negative aduce puțin; pierderea reală vine din prețul mic, dar pozitiv, de la amiază {h=95ad43c9}

Un parc fără sprijin pe MWh cîștigă $|P_t|$ pentru fiecare MWh pe care nu îl produce la preț negativ. Cîștigul obținut prin oprire în toate intervalele negative, raportat la un MWh din producția anuală, este

$$ g=\frac{\sum_t \max(0,-P_t)\,G_t\Delta_t}{\sum_t G_t\Delta_t} $$ {#eq:gain}

unde $G_t$ este producția solară, în MW, $\Delta_t$ durata intervalului, iar $\max(0,-P_t)$ suma plătită pe MWh cînd prețul este negativ. Comparația relevantă este cu reducerea datorată profilului, $B-\mathrm{CP}$, din secțiunea anterioară.

În 2025, 6,2% din producția solară a României s-a realizat la prețuri negative, cu un cost de 1,71 milioane EUR pentru parcuri. Totuși, cîștigul din oprire a fost doar $g$ = 0,63 EUR/MWh, față de o reducere datorată profilului de 43,9 EUR/MWh. În 2026, 4,0% din producție s-a realizat la prețuri negative, iar $g$ = 0,35 EUR/MWh. Prețurile negative atrag atenția, dar pierderea mare a unui parc solar vine din numeroasele ore de la amiază cu prețuri mici, dar pozitive.

@practice instalați oprirea la distanță, pentru că este ieftină, dar evaluați parcul după prețul capturat.

## Sferturile de oră arată 26 prețuri negative ascunse în ore cu medie nenegativă {h=ac676c0b}

De la 1 octombrie 2025, cuplarea unică a piețelor pentru ziua următoare (SDAC, *Single Day-Ahead Coupling*) folosește un MTU de 15 minute (NEMO Committee, 2025). De atunci și pînă la 31 octombrie 2026, România a avut 687 de sferturi de oră cu preț negativ, adică 171,75 ore echivalente. Dintre acestea, 26 (3,8%) se află în ore a căror medie este zero sau pozitivă.

Diferența contează, pentru că mediile orare arată doar 195 de ore negative. O baterie sau un consumator flexibil care acționează pe sfert de oră poate valorifica sferturile negative ascunse; un parc măsurat pe sfert de oră le plătește. Regula de numărare este @eq:neghours, cu $\Delta_t$ = 0,25 h: un sfert de oră nu se numără niciodată ca o oră.

@practice programați oprirea centralelor și bateriile pe intervale de 15 minute, ca piața.

## @end

Producătorii ofertează sub zero cînd sprijinul sau costul repornirii fac oprirea scumpă. România are mai puține ore negative decît Germania, iar numărul lor a scăzut în 2026; oprirea aduce puțin în comparație cu pierderea din prețurile mici, dar pozitive, de la amiază.

# Profilul zilnic și diferențele de preț

Prețurile mici de la amiază și cele mari de seară formează un profil zilnic al prețului. Secțiunea citește acest profil pe prețurile la 15 minute, definește diferența zilnică de preț din care cîștigă o baterie și o compară între România și vecinii ei.

## Primăvara, sferturile de oră de la amiază au costat în medie 23,0 EUR/MWh, iar cele de seară 208,3 {h=0e6af8bb}

Graficul arată prețul mediu al fiecărui sfert de oră din zi în ultimele 12 luni, separat pe anotimpuri. Primăvara, profilul formează o „vale” solară adîncă: minimul, 23,0 EUR/MWh, apare la 12:45 CET, iar maximul, 208,3 EUR/MWh, la 19:45 CET, după apus, cînd cererea este încă mare.

Distanța dintre maxim și minim măsoară oportunitatea zilnică pentru stocare. Ea este de 185 EUR/MWh primăvara și 226 vara, dar doar 98 EUR/MWh iarna, cînd producția solară este mică și „valea” aproape dispare.

@practice o baterie se încarcă în „vale” și se descarcă seara; diferența este marja ei brută.

@chart shape15
Profilul mediu al prețului pe 15 minute în PZU, pe anotimpuri, în ultimele 12 luni (noiembrie 2025 – octombrie 2026), ora CET.

## O baterie cîștigă diferența dintre orele scumpe și cele ieftine, mai puțin pierderile {h=adebd477}

Bateria cumpără un MWh cînd este ieftin și vinde, cînd este scump, ce rămîne după încărcare și descărcare. O primă măsură a cazului de afaceri este diferența zilnică dintre cele mai scumpe $k$ ore și cele mai ieftine $k$ ore, împreună cu marja brută aproximativă a unui ciclu:

$$ S^{(k)}_d=\bar P^{\,\mathrm{top}\,k}_d-\bar P^{\,\mathrm{bot}\,k}_d $$ {#eq:spread}

$$ \pi_d\approx k\,\big(\eta\,\bar P^{\,\mathrm{top}\,k}_d-\bar P^{\,\mathrm{bot}\,k}_d\big) $$ {#eq:margin}

unde $\bar P^{\,\mathrm{top}\,k}_d$ și $\bar P^{\,\mathrm{bot}\,k}_d$ sînt prețurile medii ale celor mai scumpe, respectiv ale celor mai ieftine $k$ ore din ziua $d$, $k$ este numărul de ore de stocare, $\eta$ randamentul ciclului complet (85%), iar $\pi_d$ marja brută a unui ciclu pentru o baterie de 1 MW, în EUR.

Pentru România și $k=2$, diferența zilnică medie a fost de 45 EUR/MWh în 2019, 151 în 2025 și 174 în 2026. Pierderile impun un prag: dacă bateria cumpără la 50 EUR/MWh, trebuie să vîndă peste $50/0{,}85\approx59$ EUR/MWh ca să nu piardă, pentru că doar 85% din energie se întoarce (Sioshansi et al., 2009).

@practice un dezvoltator de baterii citește cazul de afaceri din diferența zilnică de preț, înaintea oricărui model.

## Diferența zilnică de preț este de circa patru ori mai mare decît în 2019 și asemănătoare în România, Bulgaria și Ungaria {h=823281da}

Graficul urmărește media lunară a diferenței zilnice pe 2 ore, @eq:spread, în cele patru piețe, începînd cu 2019. Diferența a crescut odată cu criza energetică din 2022, nu a mai revenit la nivelul vechi și este acum de circa patru ori mai mare decît în 2019. În 2026, diferența medie dintre cele mai scumpe 2 ore și cele mai ieftine 2 ore a fost 174 EUR/MWh în România, 150 în Bulgaria, 187 în Ungaria și 152 în Germania.

Cele trei piețe vecine au diferențe foarte apropiate pentru că sînt cuplate: toate bateriile din regiune concurează pentru aceeași diferență, iar o baterie construită în Bulgaria o reduce și în România.

@practice tratați diferența de preț ca pe o resursă regională, împărțită cu fiecare baterie nouă din țările vecine.

@chart spreads
Media lunară a diferenței zilnice dintre cele mai scumpe 2 ore și cele mai ieftine 2 ore, în România, Bulgaria, Ungaria și Germania–Luxemburg, din 2019 pînă în octombrie 2026 (scară logaritmică peste 100).

## @end

„Valea” solară creează o diferență zilnică mare, maximă primăvara și vara. Diferența pe 2 ore este de circa patru ori mai mare decît în 2019 și este împărțită de întreaga regiune cuplată.

# Economia unei baterii

Diferența zilnică este doar o primă măsură. Secțiunea calculează venitul unei baterii cu programul zilnic optim, compară informația perfectă cu reguli simple de prognoză și prețurile orare cu cele pe 15 minute, arată cum își erodează bateriile propria diferență de preț și transformă venitul într-o investiție maximă.

## Programul zilnic optim al unei baterii este soluția unui program liniar mic {h=a6867c7f}

Bateria alege cînd să se încarce și cînd să se descarce pentru a-și maximiza venitul, în limitele ei fizice. Pentru fiecare zi, ea rezolvă

$$ \max_{c,\,x}\ \sum_t P_t\,(x_t-c_t)\,\Delta_t $$ {#eq:lpobj}

$$ e_t=e_{t-1}+\big(\sqrt\eta\,c_t-x_t/\sqrt\eta\big)\Delta_t $$ {#eq:lpstate}

$$ 0\le e_t\le E,\quad e_0=e_T=0,\quad 0\le c_t,x_t\le 1,\quad \sum_t x_t\Delta_t\le\sqrt\eta E $$ {#eq:lplimits}

unde $c_t$ și $x_t$ sînt puterea de încărcare, respectiv de descărcare, în MW, $P_t$ prețul, $\Delta_t$ durata intervalului, $e_t$ energia stocată, în MWh, $E$ capacitatea de stocare (1, 2 sau 4 MWh pentru o baterie de 1 MW), $\eta$ = 0,85 randamentul ciclului complet, împărțit egal între încărcare și descărcare, iar $T$ numărul de intervale din zi. Ultima restricție permite cel mult un ciclu pe zi (forma matriceală este în Anexa B).

Ipotezele, randament de 85% și un ciclu pe zi, sînt valorile de referință ale Laboratorului Național pentru Energie Regenerabilă (NREL) din Statele Unite (Cole & Karmakar, 2023). Nu includem pierderea de capacitate, tarifele și veniturile din echilibrare. Programul se rezolvă în două ipoteze despre informație: cu informație perfectă, cînd prețurile sînt cunoscute dinainte, ceea ce dă o limită superioară, și cu o regulă de prognoză, cînd programul se optimizează pe prognoză, dar plata se face la prețurile reale.

@practice acest program, cu prețurile și limitele dumneavoastră, stă la baza oricărui instrument de programare a bateriilor.

## Cu informație perfectă, o baterie de 2 ore a cîștigat 111,2 mii EUR pe MW în ultimele 12 luni {h=6f66b47a}

Graficul arată venitul anual al bateriilor de 1 MW cu 1, 2 și 4 ore de stocare, calculat cu @eq:lpobj și informație perfectă. Pentru 2 ore, venitul a fost de 26,3 mii EUR pe MW și an în 2019, 125,0 în 2022 și 98,7 în 2025; în ultimele 12 luni a ajuns la 111,2 mii EUR.

Bateriile mai lungi cîștigă mai mult, dar nu proporțional. O baterie de 4 ore cîștigă de 1,72 ori cît una de 2 ore, nu dublu, pentru că orele a treia și a patra valorifică o diferență mai mică: cele mai ieftine și cele mai scumpe ore ale zilei sînt deja folosite de primele două.

@practice dimensionați bateria după venitul adus de fiecare MWh suplimentar de stocare, nu după venitul total.

@chart bat_years
Venitul anual din arbitraj al bateriilor de 1, 2 și 4 ore, cu informație perfectă, în mii EUR pe MW, 2019–2025 și ultimele 12 luni.

## O regulă simplă de prognoză obține 85% din venitul cu informație perfectă al unei baterii de 2 ore {h=2aa99b7f}

O baterie reală nu cunoaște prețurile de mîine. Cursul testează două reguli care folosesc doar informația disponibilă la 12:00 CET în ziua dinaintea livrării, $d-1$, cînd se depun ofertele. Prima folosește profilul mediu al prețurilor din ultimele 7 zile, a doua prețurile de ieri. Programul se optimizează pe prognoză, iar plata se face la prețurile reale.

Regula de 7 zile obține 82%, 85% și 89% din venitul cu informație perfectă pentru bateriile de 1, 2 și 4 ore. Prețurile de ieri obțin 75%, 79% și 84%. Bateriile mai lungi tolerează mai bine erorile de sincronizare: dacă ora cea mai ieftină este ratată cu o oră, o baterie de 4 ore se încarcă tot în ore ieftine. Comparația se face pe 361 de zile comune și este scalată la întreaga perioadă.

@practice bugetați pe baza unei reguli aplicabile; o prognoză mai bună (cursul 2) reduce o parte din diferență.

@chart bat_rules
Venitul, în mii EUR pe MW, al bateriilor de 1, 2 și 4 ore în ultimele 12 luni: informație perfectă pe prețuri la 15 minute și pe medii orare, regula de 7 zile și prețurile de ieri.

## Prețurile pe 15 minute au crescut cu 14,5% venitul unei baterii de 1 oră, în aceleași zile {h=57edd823}

Orice program orar poate fi executat și pe sferturi de oră, deci prețurile mai fine pot doar să adauge venit:

$$ R^{15}=\max_{c,x}\sum_t P^{15}_t(x_t-c_t)\tfrac14\ \ge\ R^{60} $$ {#eq:granularity}

unde $R^{15}$ este venitul optim pe cele 96 de prețuri pe sfert de oră $P^{15}_t$ dintr-o zi, $R^{60}$ venitul optim cînd fiecare oră este plătită la media celor patru sferturi ale ei, iar $c_t$, $x_t$ puterea de încărcare și de descărcare. Ambele se calculează pe aceleași zile, deci diferența este doar valoarea detalierii.

În ultimele 12 luni, în mii EUR pe MW, bateria de 1 oră a cîștigat 53,2 pe prețuri orare și 61,0 pe prețuri la 15 minute (+14,5%), cea de 2 ore 100,8 și 111,2 (+10,3%), iar cea de 4 ore 178,4 și 190,9 (+7,0%). O comparație cu anul anterior, orar, ar include și schimbarea nivelului prețurilor; de aceea ambele venituri folosesc aceleași zile.

@practice bateriile de durată scurtă cîștigă cel mai mult din prețurile pe 15 minute.

## Bateriile își canibalizează diferența de preț: pe ofertele locale, 50 MW ar fi anulat-o la 21 octombrie 2026 {h=b46f90db}

Bateriile sînt supuse aceleiași canibalizări ca solarul. Încărcarea adaugă cerere la amiază, iar descărcarea adaugă ofertă seara; ambele apropie cele două prețuri. Pe curbele OPCOM, efectul se poate calcula astfel:

$$ \Delta P(X)=p^{*}_{\text{seară}}(+X\text{ ofertă})-p^{*}_{\text{amiază}}(+X\text{ cerere}) $$ {#eq:batspread}

unde $X$ este puterea bateriilor, în MW, iar $p^*$ prețul de închidere recalculat pe curbele OPCOM pentru 12:00–12:15 și 20:00–20:15 (ora României), cu $X$ adăugat drept cerere la amiază și drept ofertă seara; fluxurile transfrontaliere rămîn fixe (Anexa C).

La 21 octombrie 2026, prețul realizat de seară a depășit prețul de la amiază cu 91,77 EUR/MWh. Cu 50 MW de baterii, diferența ar fi fost −13,15 EUR/MWh, iar cu 100 MW, −47,12: numai pe ofertele locale, 50 MW sînt suficienți ca să anuleze diferența. Ca și calculul ordinii de merit, rezultatul este o limită superioară, pentru că în piața cuplată fluxurile se ajustează. Bateriile funcționează deja: în România au livrat pînă la 766 MW în 2026, iar în Bulgaria, cu date raportate din 9 septembrie 2026, pînă la 2 795 MW.

@practice modelați diferența de preț de după construirea bateriilor, nu pe cea observată înainte.

## O baterie din România concurează pentru aceeași diferență regională de preț ca bateriile din Bulgaria și Ungaria {h=4a7f9491}

Graficul urmărește venitul lunar cu informație perfectă al unei baterii de 2 ore în România, Bulgaria și Ungaria, începînd cu 2024. În ultimele 12 luni, în mii EUR pe MW, acesta a fost 117,6 în Ungaria, 111,2 în România, 96,4 în Bulgaria și 90,6 în Germania. Panoul din dreapta arată producția bateriilor raportată la ENTSO-E în România și Bulgaria.

Veniturile zilnice evoluează împreună: corelația lor cu România este 0,80 pentru Bulgaria și 0,87 pentru Ungaria. O zi bună pentru o baterie din România este o zi bună și pentru bateriile vecinilor, iar fiecare dintre ele ia o parte din aceeași diferență de preț de seară.

@practice cum am anunțat în cursul 1: un dezvoltator român de baterii concurează pentru aceeași diferență regională de preț de seară.

@chart bat_region
Stînga: venitul unei baterii de 2 ore cu informație perfectă, în EUR pe MW pe zi, lunar, în România, Bulgaria și Ungaria; dreapta: producția lunară a bateriilor raportată la ENTSO-E în România și Bulgaria; ianuarie 2024 – octombrie 2026.

## La 8% pe 15 ani, venitul bateriei de 2 ore justifică o investiție de cel mult 808 EUR pe kW {h=affb5e55}

Investiția maximă pe care o poate recupera un venit anual este venitul înmulțit cu factorul de anuitate:

$$ I^{\max}=R\cdot a(r,n) $$ {#eq:imax}

$$ a(r,n)=\sum_{j=1}^{n}(1+r)^{-j}=\frac{1-(1+r)^{-n}}{r} $$ {#eq:annuity}

unde $R$ este venitul anual pe MW, în EUR, $r$ rata de actualizare (8%, o ipoteză), $n$ durata de viață (15 ani, după NREL), iar $a(r,n)$ factorul de anuitate, aici 8,56 (Anexa D). Împărțind $I^{\max}$ la 1 000 se obțin EUR pe kilowatt (kW).

Pentru o baterie de 2 ore, în ultimele 12 luni, informația perfectă justifică cel mult 952 EUR/kW, iar regula de 7 zile 808 EUR/kW, adică 404 EUR pe kilowatt-oră (kWh) de stocare. Cîteva elemente nu sînt incluse: costurile de operare, tarifele de rețea și pierderea de capacitate ar reduce $I^{\max}$; veniturile din echilibrare l-ar crește; bateriile noi reduc diferența de preț (Schmidt et al., 2019).

@practice comparați 404 EUR/kWh cu oferta pentru instalația la cheie, înaintea oricărei alte analize.

## @end

O baterie de 2 ore a cîștigat 111,2 mii EUR pe MW în ultimele 12 luni cu informație perfectă și circa 85% din această sumă cu o regulă simplă. Prețurile pe 15 minute adaugă venit, bateriile noi erodează diferența de preț, iar la 8% pe 15 ani venitul justifică cel mult 808 EUR pe kW.

# Studii de caz: aprilie 2026; vara 2026

Două studii de caz aplică instrumentele cursului pe episoade reale: aprilie 2026, luna cu cele mai multe ore cu preț negativ, și vara lui 2026, cînd România a exportat la amiază și a importat seara din Bulgaria.

## Studiu de caz: în săptămîna din 20 aprilie 2026, România a avut 24 de ore cu preț negativ, iar rata de captare solară a fost 42% {h=26c065dd}

Graficul arată prețurile pe 15 minute și producția solară și eoliană a României în săptămîna 20–26 aprilie 2026, împreună cu intervalele în care o baterie de 2 ore cu informație perfectă se încarcă și se descarcă. Săptămîna a avut 24 de ore cu preț negativ. Prețurile au variat între −99,75 EUR/MWh, la 26 aprilie, ora 13:00, și 328,00 EUR/MWh, iar producția solară a atins 2 243 MW.

Pentru solar, săptămîna a fost slabă: prețul capturat a fost 37,0 EUR/MWh, față de un preț de bază de 87,0, deci o rată de captare de 42,5%. Pentru o baterie, aceeași săptămînă a fost una dintre cele mai bune: o baterie de 2 ore cu informație perfectă a cîștigat 391 EUR pe MW pe zi, față de 305 într-o zi medie din ultimele 12 luni.

@practice aceeași săptămînă însorită este cea mai slabă pentru un parc solar și una dintre cele mai bune pentru o baterie.

@chart case_week
Prețul PZU pe 15 minute, cu intervalele de încărcare și de descărcare ale unei baterii de 2 ore (sus), și producția solară și eoliană, în GW (jos), 20–26 aprilie 2026, ora CET.

## Studiu de caz: ce a însemnat luna aprilie 2026 pentru fiecare participant la piață {h=7c2d6136}

Aprilie 2026 a avut 67 de ore cu preț negativ, cele mai multe dintre toate lunile. Aceeași lună a însemnat lucruri diferite pentru participanții la piață:

- **Dezvoltatorul solar**: rata de captare a fost 49,4% (47,2 față de 95,6 EUR/MWh), cu 17,9% din producție la prețuri negative. Decizia este între stocare în același amplasament și un PPA care stabilește prețul profilului solar.
- **Dezvoltatorul eolian**: rata de captare a fost 97,8%. În România, eolianul nu este tehnologia canibalizată.
- **Dezvoltatorul de baterii**: o baterie de 2 ore a cîștigat 325 EUR pe MW pe zi, față de 305 în medie în ultimele 12 luni.
- **Furnizorul și consumatorul industrial**: 67 de ore cu preț negativ. Mutarea consumului la amiază, primăvara, este plătită.
- **Transelectrica**: după apus, creșterea cererii nete și interconexiunile fixează prețul.

## Vara 2026: România a exportat la prînz și a cumpărat seara din Bulgaria {h=6cd091dc}

Graficul arată fluxurile transfrontaliere medii pe ore ale României și prețurile din România și Bulgaria între 1 iunie și 31 august 2026; fluxurile pozitive înseamnă import în România. La prînz, România exportă: 960 MW net la ora 12, pe toate granițele, mai ales spre Ungaria (857 MW) și Serbia (367 MW). Spre Bulgaria a exportat între 12:00 și 15:00 doar în 43 din cele 92 de zile.

Seara direcția se inversează: România importă din Bulgaria 2 064 MW la ora 21, în toate cele 92 de zile. La ora 21, prețul mediu a fost 243,9 EUR/MWh în România și 178,3 în Bulgaria. Cînd granița este folosită complet, cele două prețuri se separă, iar prețul de seară din România rămîne mai mare. Granițele cu Moldova și Ucraina sînt raportate doar parțial.

@practice diferența de seară, de 65,6 EUR/MWh, arată cît valorează în România stocarea pentru seară și o capacitate mai mare de interconexiune.

@chart rogb_summer
Fluxul mediu pe ore din zi, fluxul net al României pe toate granițele și fluxul pe granița România–Bulgaria (+ = import în România), și prețurile PZU din România și Bulgaria, 1 iunie – 31 august 2026.

## @end

Într-o săptămînă însorită de primăvară, aceleași prețuri care coboară rata de captare a solarului la 42,5% ridică marja zilnică a unei baterii mult peste media ei. Vara, granița cu Bulgaria, folosită complet seara, menține prețul din România peste cel bulgăresc.

# Recapitulare

Recapitularea verifică ideile principale prin patru întrebări, rezumă cursul, prezintă cercetările grupului nostru pe aceeași temă și indică resurse pentru studiu suplimentar.

## Verifică-te {h=860194f9}

1. Vi se oferă un PPA solar la prețul de bază din 2025, de 108 EUR/MWh. Cît obține de fapt profilul solar? Răspuns: aproximativ 64 EUR/MWh în 2025, pentru că rata de captare a fost 59%. Cumpărătorul care plătește prețul de bază pentru profilul solar plătește o primă mare.
2. De la 1 octombrie 2025, România a avut 687 de sferturi de oră cu preț negativ. Cîte ore cu preț negativ raportați? Răspuns: 171,75 ore echivalente, pentru că fiecare sfert de oră contează 0,25 h, nu 687 de ore.
3. Dublarea stocării de la 2 la 4 ore dublează costul celulelor. Se dublează și venitul? Răspuns: nu. În ultimele 12 luni, o baterie de 4 ore a cîștigat de 1,72 ori cît una de 2 ore, deoarece orele suplimentare valorifică o diferență de preț mai mică.
4. Pe curbele OPCOM din 21 octombrie 2026, 25 MW în plus la preț zero coboară prețul de la amiază la 131,4 EUR/MWh. Acesta este efectul unui parc nou de 25 MW? Răspuns: nu. Curbele păstrează fixe fluxurile transfrontaliere, iar în piața cuplată o parte din producția suplimentară se exportă, deci efectul real este mai mic. Regresia dă o scădere de aproximativ 27 EUR/MWh pentru fiecare GW.

## Recapitulare {h=d35f405b}

Producția solară reduce prețul pe care îl primește: rata de captare a solarului din România a scăzut de la 104% în 2019 la 59% în 2025, în timp ce eolianul a rămas aproape de 100%. Bateriile trăiesc din aceeași diferență regională de preț pe care o creează solarul: o baterie de 2 ore a cîștigat 111 mii EUR pe MW în ultimele 12 luni cu informație perfectă și circa 85% din această sumă cu o regulă simplă de prognoză. Urmează cursul 7.

## Cercetările grupului nostru despre sursele regenerabile și prețurile din România {h=735992df}

Mai multe lucrări ale grupului nostru studiază piața din România cu aceiași factori ca acest curs. Rezultatele de mai jos sînt cele raportate în lucrări; celelalte cifre de pe această pagină provin din calculele noastre.

- **Explicarea scăderilor și salturilor de preț** (Andrei & Pele, 2025): lucrarea identifică prețurile orare neobișnuite din România cu algoritmul *isolation forest* și le explică prin valori Shapley. Producția eoliană și cea solară explică scăderile de preț, iar erorile de prognoză a consumului și producția convențională explică salturile.
- **Factorii prețului pe orizonturi și regimuri** (Andrei, Pele & Cramer, 2026): lucrarea prognozează prețurile orare din România în perioada 2018–2024 cu ansambluri de arbori și măsoară ce factori contează la fiecare orizont și în regimurile de preț scăzut, normal și ridicat. Ea identifică factorii regenerabili din spatele regimului de preț scăzut studiat în acest curs.
- **Avertizarea timpurie a salturilor de preț** (Andrei, Pele, Cramer, Amza & Diaconu, 2026): lucrarea construiește un sistem explicabil de inteligență artificială (AI) pentru avertizarea timpurie a salturilor de preț din România. Prognoza consumului rezidual este principalul factor, aceeași variabilă ca în regresia noastră.
- **Elasticitatea cererii de energie electrică** (Proșcanu, Proșcanu & Pele, 2025): lucrarea testează cauzalitatea Granger între consumul și prețul energiei electrice din România. Consumul nu reacționează la preț, de unde curba cererii aproape verticală din ordinea de merit.

## Lecturi și resurse suplimentare {h=117d0184}

- **Hirth (2013)**: lucrarea de referință despre rata de captare a energiei eoliene și solare, [articolul](https://doi.org/10.1016/j.eneco.2013.02.004).
- **Cole & Karmakar (2023)**: costurile, randamentul și durata de viață a bateriilor, folosite în acest curs, [raportul](https://doi.org/10.2172/1984976).
- **energy-charts.info**: prețuri, producție și putere instalată, actualizate, pentru România și vecinii ei, [energy-charts.info](https://energy-charts.info).
- **Acest curs**: cod, date și notebook-uri Jupyter, [github.com/danpele/EMQA](https://github.com/danpele/EMQA).
- **Curbele agregate OPCOM**: descărcați altă zi și repetați calculul ordinii de merit, [opcom.ro](https://www.opcom.ro/rapoarte-pzu-curbe-agregate/ro).
- **Exercițiu practic**: notebook-ul Jupyter reproduce toate graficele și cifrele din acest curs.

# Anexă

Anexa conține demonstrațiile și detaliile de calcul pentru rata de captare, programul bateriei, recalcularea prețului de închidere și factorul de anuitate.

## Anexa A: rata de captare este unu plus o covarianță scalată {h=679f9bab}

Se definesc ponderile după durată, mediile ponderate și covarianța ponderată:

$$ w_t=\frac{\Delta_t}{\sum_s\Delta_s},\quad \bar P=\sum_t w_tP_t=B,\quad \bar G=\sum_t w_tG_t,\quad \mathrm{Cov}_\Delta(P,G)=\sum_t w_t(P_t-\bar P)(G_t-\bar G) $$

unde $w_t$ este ponderea intervalului $t$, proporțională cu durata lui $\Delta_t$, iar $P_t$ și $G_t$ sînt prețul și producția. Împărțind numărătorul și numitorul lui CP din @eq:capture la $\sum_s\Delta_s$, se obține $\mathrm{CP}=\sum_t w_tP_tG_t/\bar G$. Din definiția covarianței, $\sum_t w_tP_tG_t=\mathrm{Cov}_\Delta(P,G)+\bar P\bar G$. Prin urmare

$$ \mathrm{CR}=\frac{\mathrm{CP}}{\bar P}=1+\frac{\mathrm{Cov}_\Delta(P,G)}{\bar P\,\bar G} $$

Pentru producția solară din România, în ianuarie–octombrie 2026, $\bar P$ = 137,4, $\bar G$ = 593 MW, iar covarianța este −31 069, deci CR = 0,619. CR este sub unu exact atunci cînd producția este mare în intervalele ieftine și nu este definită dacă $\bar P\le 0$ (Hirth, 2013).

## Anexa B: programul bateriei în formă matriceală {h=cb6c94b4}

Variabilele se grupează într-un singur vector $z=(c_1,\dots,c_T,\,x_1,\dots,x_T,\,e_1,\dots,e_T)$, cu $3T$ variabile, unde $T$ este 92, 96 sau 100 de sferturi de oră, în funcție de schimbarea orei (24 de ore înainte de octombrie 2025). Funcția obiectiv minimizează venitul cu semn schimbat:

$$ \min_z\ \sum_t P_t\Delta_t c_t-\sum_t P_t\Delta_t x_t $$

cu restricțiile de egalitate

$$ e_t-e_{t-1}-\sqrt\eta\,\Delta_tc_t+\Delta_tx_t/\sqrt\eta=0,\quad t=1,\dots,T,\quad e_0=0,\quad e_T=0 $$

și cu inegalitatea și limitele $\sum_t\Delta_tx_t/\sqrt\eta\le E$, $0\le c_t,x_t\le1$ și $0\le e_t\le E$, cu simbolurile din @eq:lpobj – @eq:lplimits. Programul se rezolvă cu algoritmul HiGHS din scipy.

Pentru regulile de prognoză, programul se rezolvă pe prognoza $\hat P_t$ (media ultimelor 7 zile sau prețurile zilei $d-1$), iar venitul se calculează apoi ca $\sum_tP_t(x_t-c_t)\Delta_t$, cu prețurile reale $P_t$. Zilele cu alt număr de intervale decît prognoza (schimbarea orei) sînt eliminate: rămîn 361 din 365 de zile (Sioshansi et al., 2009).

## Anexa C: recalcularea prețului de închidere pe curbele OPCOM {h=643ba0ef}

OPCOM publică, pentru fiecare sfert de oră, punctele agregate ale curbelor de ofertă și de cerere (preț, MW cumulați), în format XML. Blocurile, ordinele orare și fluxurile transfrontaliere nete se adaugă la limitele de preț, −600 și +4 000 EUR/MWh, ca în graficul OPCOM.

$S(p)$ și $D(p)$ se obțin prin interpolare liniară între punctele publicate. Noul preț este cel mai mic $p$ pentru care $S(p)+X\mathbf 1[p\ge0]-D(p)\ge0$, găsit prin bisecție pe $[-600,4000]$. Pentru încărcarea bateriilor, se adaugă la $D$ o cerere de $X$ MW la orice preț.

Ca verificare, pentru $X=0$ curbele se intersectează pe un segment orizontal: la amiază de la 152,16 EUR/MWh în sus, seara de la 206,49. Prețurile oficiale, 152,23 și 244,00, se află pe aceste segmente, iar pentru $X=0$ folosim prețul oficial, nu curba.

## Anexa D: factorul de anuitate {h=c7e97ca9}

Valoarea actualizată a unui venit anual constant $R$, pe $n$ ani, la rata $r$, este o sumă geometrică:

$$ V=\sum_{j=1}^{n}R(1+r)^{-j}=R\,q\,\frac{1-q^{n}}{1-q},\qquad q=(1+r)^{-1} $$

Deoarece $q/(1-q)=1/r$, expresia devine

$$ V=R\,\frac{1-(1+r)^{-n}}{r}=R\,a(r,n) $$

adică relația @eq:annuity. Proiectul se recuperează dacă investiția $I\le V$; pentru $r$ = 8% și $n$ = 15, $a$ = 8,56. Pe kWh de stocare, $I^{\max}/E$ cu regula de 7 zile este 428, 404 și 365 EUR/kWh pentru bateriile de 1, 2 și 4 ore (Cole & Karmakar, 2023).
