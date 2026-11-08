<!--
Versiunea web a Cursului 7 (RO). Construită în web/L7_ro.html de lectures/common/build_web_lecture.py (formatul: docstring-ul scriptului).
Hash-urile slide-urilor: python3 build_web_lecture.py 7 --frames
-->

## @intro

Învățarea automată (ML, *machine learning*) promite prognoze mai precise ale prețului energiei electrice, iar mulți furnizori de modele o vînd tocmai cu această promisiune. Cursul pune o întrebare lucidă: pe piața pentru ziua următoare (PZU) din România, administrată de operatorul pieței de energie electrică și de gaze naturale (OPCOM), o rețea neuronală profundă (DNN) calibrată, un ansamblu de arbori de decizie construiți secvențial (*gradient boosting*) și un model fundațional preantrenat prognozează oare mai bine cele 24 de prețuri orare de mîine decît modelele statistice de referință din cursul 2? Iar dacă da, cu cît, cu ce cost și cum putem explica de ce?

Răspunsul contează pentru orice companie care tranzacționează pe PZU. Un furnizor cumpără cu o zi înainte orele de care are nevoie, un producător hotărăște cînd să vîndă, iar proprietarul unei baterii alege cînd să o încarce și cînd să o descarce. Fiecare plătește erorile de prognoză în euro pe megawatt-oră (EUR/MWh). Un model care pare mai bun decît este, pentru că a fost evaluat pe zilele greșite sau cu informații care nu existau la momentul licitației, costă de două ori: o dată la cumpărare și încă o dată cînd cedează în producție.

Cursul folosește aceleași date reale și același an de test ca în cursul 2: prețurile orare de pe PZU, împreună cu consumul, producția eoliană și solară și alte variabile fundamentale, descărcate de pe energy-charts.info (Fraunhofer ISE) și Yahoo Finance, pînă la 31 octombrie 2026. Se adaugă un singur ingredient, de care învățarea automată are nevoie: un an de validare separat, pe care se aleg setările modelelor înainte de a deschide anul de test.

@goals
- **Organizați corect** un experiment de învățare automată: eșantioane de antrenare, de validare și de test care se succed în timp, cu prognoze care folosesc numai informația cunoscută la ora 12:00 a Europei Centrale (CET) în ziua dinaintea livrării.
- **Construiți și calibrați** o rețea neuronală profundă și un model gradient boosting pentru cele 24 de prețuri orare ale zilei următoare și încercați un model fundațional preantrenat.
- **Comparați** aceste modele cu modelele de referință din cursul 2, pe același an de test, cu eroarea absolută medie (MAE), rădăcina erorii pătratice medii (RMSE), MAE relativă (rMAE) și testul Diebold–Mariano (DM), și combinați învățarea automată cu modelele statistice.
- **Explicați** prognozele, anticipați vîrfurile de preț și prețurile negative și recunoașteți capcanele care fac un model să pară mai bun decît este.

# Învățarea automată, evaluată corect

Modelele flexibile pot învăța tipare pe care un model liniar nu le vede, dar pot învăța și zgomotul trecutului; secțiunea stabilește regulile care păstrează evaluarea corectă. Datele sînt împărțite în eșantioane de antrenare, de validare și de test, în ordine cronologică, iar setările se aleg prin căutare aleatoare numai pe anul de validare.

## Aceleași date și același an de test ca în cursul 2, plus un an de validare {h=cb3e7af7}

Variabila prognozată este prețul orar de pe PZU pentru zona de ofertare România (RO). Variabilele explicative sînt cele din cursul 2: prețurile pînă în ziua $d-1$; consumul, producția eoliană și solară, hidro, nucleară și importul net pînă în ziua $d-2$, de la Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E); și prețul certificatelor de emisii (EUA) ale Uniunii Europene (UE), printr-un titlu tranzacționat la bursă, garantat cu mărfuri (ETC). Datele acoperă perioada pînă la 31 octombrie 2026 și au fost descărcate la 4 noiembrie 2026 de pe energy-charts.info, portalul de date al Institutului Fraunhofer pentru Sisteme de Energie Solară (ISE), și de pe Yahoo Finance.

Timpul este împărțit în trei. Antrenarea începe la 8 ianuarie 2022 și crește cu o lună la fiecare reestimare. Anul de validare, 1 noiembrie 2024 – 31 octombrie 2025, este folosit numai pentru alegerea setărilor modelelor. Anul de test, 1 noiembrie 2025 – 31 octombrie 2026, are 8 760 de ore, iar modelele sînt reestimate lunar.

Modelele de referință sînt prognozele din cursul 2, preluate din fișierele acestuia: modelul naiv; modelul autoregresiv cu variabile exogene (ARX); operatorul de contracție și selecție în normă absolută (LASSO); autoregresia estimată cu LASSO (LEAR); ARX și LEAR mediate pe mai multe ferestre de calibrare (AW-ARX și AW-LEAR); ansamblul de 4 modele. Fiindcă anul de test este același, fiecare eroare din acest curs se poate compara direct cu cele din cursul 2.

## Învățarea automată cîștigă flexibilitate, dar plătește prin varianță {h=99f85e49}

Un model flexibil poate învăța praguri și interacțiuni pe care LEAR nu le vede, dar poate învăța și zgomotul din anii de antrenare. Toate modelele din acest curs, statistice sau nu, se estimează după același principiu: se minimizează potrivirea pe zilele de antrenare plus o penalizare a complexității,

$$ \hat\theta=\arg\min_{\theta}\ \underbrace{\frac1n\sum_{i=1}^{n}\ell\big(Y_i,f_\theta(\mathbf x_i)\big)}_{\text{potrivirea pe zilele de antrenare}}+\underbrace{\lambda\,\Omega(\theta)}_{\text{penalizare}} $$ {#eq:erm}

unde $f_\theta$ este modelul, cu parametrii $\theta$, $\mathbf x_i$ sînt variabilele cunoscute la închiderea licitației, $Y_i$ este prețul, $\ell$ funcția de pierdere (aici eroarea absolută), $n$ numărul de observații de antrenare, $\Omega$ complexitatea modelului, iar $\lambda$ ponderea ei.

Modelele diferă prin gradul de flexibilitate. LEAR are cel mult 247 de coeficienți pentru fiecare oră. Rețeaua noastră DNN are 141 336 de parametri, pentru 1 727 de zile de antrenare la ultima reestimare. Cu atîția parametri, eroarea pe datele de antrenare nu spune nimic despre viitor: modelul poate fi judecat numai pe date pe care nu le-a văzut. Penalizarea din @eq:erm și regulile de oprire din secțiunea următoare limitează cît de mult se poate apleca rețeaua spre zgomot, dar verdictul final vine întotdeauna din zilele păstrate deoparte.

@practice întrebați furnizorul de prognoze cîți parametri are modelul pentru fiecare zi de istoric și pe ce zile a fost măsurată eroarea.

## Trei eșantioane în ordine cronologică: antrenare, validare, test {h=b82cb03b}

Graficul arată cum este împărțit istoricul. În anul de validare se compară 25 de setări pentru fiecare model, reestimate la fiecare 3 luni; setarea cu cea mai mică MAE este fixată înainte de începutul anului de test. În anul de test, modelele sînt reestimate la începutul fiecărei luni, pe toate zilele anterioare.

Anul de test nu se folosește pentru nicio alegere. Este același an ca în cursul 2, deci erorile se pot compara direct. Ordinea contează: amestecarea zilelor între eșantioane, așa cum face validarea încrucișată obișnuită, ar permite modelului să învețe din zile care vin după cele pe care le prognozează (Bergmeir și Benítez, 2012). Ultima secțiune a cursului măsoară cît de mult avantajează o asemenea greșeală un model.

@practice tratați anul de test ca pe un plic sigilat: se deschide o singură dată, după ce toate alegerile au fost făcute.

@chart split_ml
Prețul de bază zilnic din România, 2022–2026, cu perioadele de antrenare, validare și test marcate.

## Hiperparametrii se aleg prin căutare aleatoare pe anul de validare {h=6aa27a5e}

Setări precum numărul de neuroni sau de arbori nu sînt estimate de model; încercăm mai multe și o păstrăm pe cea care prognozează cel mai bine zilele nevăzute. Formal,

$$ \gamma^{*}=\arg\min_{\gamma\in\{\gamma_0,\dots,\gamma_{24}\}}\ \frac{1}{24\,|\mathcal V|}\sum_{d\in\mathcal V}\sum_{h=0}^{23}\big|P_{d,h}-\hat P_{d,h}(\gamma)\big| $$ {#eq:search}

unde $\gamma$ este o setare (vectorul hiperparametrilor), $\gamma_0$ setarea din cursul 2, celelalte fiind extrase aleator, $\mathcal V$ mulțimea zilelor anului de validare, $|\mathcal V|$ numărul lor, $P_{d,h}$ prețul din ziua $d$ și ora $h$, iar $\hat P_{d,h}(\gamma)$ prognoza lui cu setarea $\gamma$.

De ce aleator și nu pe o grilă completă? Doar cîteva setări contează cu adevărat, iar extragerile aleatoare le acoperă mai bine, cu același număr de încercări (Bergstra și Bengio, 2012). Bugetul nostru este de 24 de setări aleatoare plus setarea din cursul 2, pentru fiecare dintre cele două modele, iar întreaga căutare durează 7,3 minute pe un nucleu al unității centrale de procesare (CPU). Spațiile de căutare și valorile alese sînt prezentate în anexa D.

@practice o căutare modestă, dar documentată, este suficientă. O căutare fără un eșantion de validare separat nu este o căutare, ci o scurgere de informație.

## @end

Învățarea automată se judecă numai pe date nevăzute. Setările se aleg pe un an de validare, iar anul de test se deschide o singură dată, după ce toate alegerile au fost făcute.

# Rețele neuronale profunde

O rețea neuronală este un lanț de regresii, fiecare urmată de o transformare neliniară, antrenat prin pași mici împotriva erorii. Secțiunea construiește rețeaua folosită în curs, arată cum este antrenată și oprită la timp și măsoară ce aduce calibrarea.

## O rețea neuronală înlănțuie regresii, fiecare urmată de o funcție neliniară {h=d1cbe4ee}

Fiecare neuron transformă neliniar o combinație liniară a intrărilor; stratul de ieșire dă deodată cele 24 de prețuri ale zilei $d$. Cu un singur strat ascuns,

$$ \mathbf z=\phi\big(W_1\mathbf x_d+\mathbf b_1\big),\qquad \hat{\mathbf Y}_d=W_2\,\mathbf z+\mathbf b_2\in\mathbb R^{24} $$ {#eq:dnn}

$$ \phi(u)=\max(0,u)\quad\text{sau}\quad \phi(u)=\ln(1+e^{u}) $$ {#eq:act}

unde $\mathbf x_d$ sînt intrările zilei $d$ (prețuri, consum, producție eoliană și solară, variabile fundamentale, ziua săptămînii), $W_1$ și $W_2$ ponderile, $\mathbf b_1$ și $\mathbf b_2$ termenii liberi, $\mathbf z$ ieșirile neuronilor ascunși, $\phi$ funcția de activare, adică unitatea liniară rectificată (ReLU, *rectified linear unit*) sau varianta ei netedă, softplus (@eq:act), iar $\hat{\mathbf Y}_d$ prețurile transformate cu asinh, ca în cursul 2.

Rețeaua aleasă pe anul de validare are 251 de intrări, un strat ascuns de 512 neuroni cu funcția softplus și 24 de ieșiri: în total 141 336 de parametri. Rețelele cu două straturi au fost mai slabe la validare. Rețeaua este vizibil mai bună decît perceptronul multistrat (MLP) din cursul 2: în anul de test are MAE 22,95 EUR/MWh, față de 25,54 pentru MLP.

@practice o rețea neuronală este o regresie cu mult mai mulți coeficienți: are nevoie de aceeași disciplină a datelor, nu de mai puțină.

## Antrenarea: pași mici împotriva erorii, opriți la timp {h=47322134}

Ponderile se modifică puțin, în direcția care reduce eroarea pe un grup aleator de zile. Funcția de pierdere pe un grup și pasul de actualizare sînt

$$ \mathcal L(\theta)=\frac{1}{24\,|B|}\sum_{d\in B}\sum_{h=0}^{23}\big|Y_{d,h}-\hat Y_{d,h}(\theta)\big| $$ {#eq:loss}

$$ \theta\leftarrow\theta-\eta\,\widehat{\nabla\mathcal L} $$ {#eq:sgd}

unde $B$ este un grup de 64 de zile (*mini-batch*), $Y_{d,h}$ și $\hat Y_{d,h}(\theta)$ prețul transformat și prognoza lui, $\eta$ rata de învățare ($3\cdot10^{-4}$), iar $\widehat{\nabla\mathcal L}$ gradientul, rescalat prin metoda Adam (Kingma și Ba, 2015; detalii în anexa A). O epocă înseamnă o parcurgere a tuturor zilelor de antrenare.

Pentru a decide cînd ne oprim (*early stopping*), rețeaua este antrenată pe primele 85% din zilele de antrenare, iar eroarea ei este urmărită pe ultimele 15%. Se păstrează epoca cea mai bună, apoi rețeaua se reestimează pe toate zilele, cu același număr de epoci. Pe datele noastre, epocile păstrate au mediana 56 și variază între 23 și 92, pe 12 reestimări $\times$ 4 inițializări. O a doua protecție împotriva memorării este *dropout*: în timpul antrenării, fiecare neuron este dezactivat aleator, cu probabilitatea 0,1 (Srivastava et al., 2014).

@practice regula de oprire folosește numai zile din trecut: face parte din model și se verifică la fel ca restul.

## Oprirea timpurie: ne oprim cînd eroarea pe zilele recente nu mai scade {h=a8a5848b}

Graficul arată curba de învățare pentru reestimarea din octombrie 2026. Eroarea pe zilele de antrenare continuă să scadă, dar eroarea pe ultimele 15% din zile atinge minimul la epoca 51, la 24,50 EUR/MWh, iar antrenarea se oprește la epoca 76.

După acest punct, rețeaua reproduce tot mai bine trecutul și tot mai slab zilele recente: începe să memoreze. Distanța dintre cele două curbe este varianța din @eq:erm, făcută vizibilă. Oprirea timpurie păstrează rețeaua în punctul în care a învățat tiparele regulate ale pieței, dar nu și accidentele anilor de antrenare.

@practice dacă un furnizor nu vă poate arăta această curbă, rețeaua a fost probabil antrenată pînă a reprodus trecutul.

@chart learning_curve
Eroarea pe zilele de antrenare și eroarea pe ultimele 15% din zile, pe epoci, pentru rețeaua DNN aleasă, reestimarea din octombrie 2026, inițializarea 1; epoca cea mai bună este marcată.

## Căutarea aleatoare reduce eroarea de validare a ambelor modele {h=04c9e07a}

Graficul ordonează cele 25 de setări încercate pentru fiecare model după MAE din anul de validare. Pentru rețeaua DNN, cea mai bună setare are 22,59 EUR/MWh, în timp ce setarea din cursul 2 are 24,24 și se află pe locul 14 din 25. Pentru eXtreme Gradient Boosting (XGBoost), cea mai bună setare are 22,76, față de 23,83 pentru setarea din cursul 2, tot pe locul 14.

Toate cele 25 de setări ale ambelor modele sînt mai precise decît modelul naiv în anul de validare (26,90 EUR/MWh), deci modelele sînt utile chiar și prost calibrate; dar abia calibrarea le aduce aproape de modelele statistice de referință.

@practice prevedeți un an de validare pentru calibrare înainte de a avea încredere într-o prognoză de învățare automată.

@chart search
MAE de validare a celor 25 de setări pentru rețeaua DNN și pentru XGBoost, ordonate, cu setarea din cursul 2 și modelul naiv marcate.

## @end

Calibrată pe anul de validare, rețeaua este clar mai bună decît perceptronul multistrat din cursul 2. Oprirea timpurie și dropout o împiedică să memoreze trecutul.

# Gradient boosting și modele fundaționale

Arborii pun întrebări cu răspuns da/nu despre variabile și surprind de la sine pragurile și interacțiunile; gradient boosting adună mulți arbori mici, fiecare corectînd erorile celor dinainte. Secțiunea se încheie cu modelele fundaționale, rețele preantrenate care prognozează prețurile din România fără să fi fost antrenate pe ele.

## Un arbore de regresie împarte intrările în căsuțe, cu cîte un preț fiecare {h=c224a304}

Un arbore pune întrebări cu răspuns da/nu; fiecare frunză finală conține o valoare, deci pragurile și interacțiunile apar de la sine. Un arbore cu $J$ frunze prognozează

$$ f(\mathbf x)=\textstyle\sum_{j=1}^{J}w_j\,\mathbb 1\{\mathbf x\in R_j\} $$ {#eq:tree}

$$ \text{Gain}=\frac{G_L^2}{H_L+\lambda}+\frac{G_R^2}{H_R+\lambda}-\frac{(G_L+G_R)^2}{H_L+H_R+\lambda}-\gamma $$ {#eq:gain}

unde $R_j$ este frunza $j$ (o căsuță în spațiul variabilelor), $w_j$ valoarea ei, $\mathbb 1\{\cdot\}$ funcția indicator, $G$ și $H$ sumele derivatelor de ordinul 1 și 2 ale pierderii pentru observațiile care merg la stînga ($L$) sau la dreapta ($R$) unei împărțiri candidate, iar $\lambda$ și $\gamma$ penalizări pentru valorile frunzelor și pentru numărul lor. Arborele crește păstrînd, la fiecare pas, împărțirea cu cel mai mare cîștig (@eq:gain); anexa B arată de unde provine formula.

Pe datele noastre, în reestimarea pentru octombrie 2026, primul arbore întreabă: prețul din $d-1$, aceeași oră, este sub 119,5 EUR/MWh? Acest arbore are 233 de frunze, iar modelul adună 1 500 de asemenea arbori.

@practice un arbore gîndește ca un trader: dacă ieri prețul a trecut de un prag, diseară urmează o primă.

## Gradient boosting: fiecare arbore nou corectează erorile rămase {h=2dbe793e}

Gradient boosting potrivește un arbore mic pe ceea ce este încă greșit, îl adaugă cu o pondere mică și repetă procedeul, aici de peste o mie de ori (Friedman, 2001; Chen și Guestrin, 2016):

$$ F_m(\mathbf x)=F_{m-1}(\mathbf x)+\eta\,f_m(\mathbf x),\qquad w_j^{*}=-\frac{G_j}{H_j+\lambda} $$ {#eq:boost}

$$ \min\ \textstyle\sum_{i}\ell\big(Y_i,F_M(\mathbf x_i)\big)+\sum_{m}\big(\gamma J_m+\tfrac{\lambda}{2}\sum_j w_{mj}^2\big) $$ {#eq:boostobj}

unde $F_m$ este prognoza după $m$ arbori, $F_M$ prognoza finală după toți cei $M$ arbori, $f_m$ arborele $m$, cu $J_m$ frunze și valorile frunzelor $w_{mj}$, $\eta$ rata de învățare, $w_j^{*}$ valoarea optimă a frunzei $j$ (anexa B), $G_j$ și $H_j$ sumele derivatelor de ordinul 1 și 2 ale pierderii în acea frunză, iar $\ell$ eroarea absolută.

Setarea aleasă pe anul de validare are 1 500 de arbori de adîncime 8, $\eta$ = 0,02, fiecare arbore fiind estimat pe o fracțiune 0,8 din rînduri. În anul de test, XGBoost calibrat are MAE 23,26 EUR/MWh, față de 24,05 pentru modelul gradient boosting (GBM) necalibrat din cursul 2, un cîștig semnificativ (DM: $p<0{,}001$). AW-LEAR, cu 22,53, rămîne mai precis (DM: $p$ = 0,016).

@practice calibrarea contează mai mult decît programul: același tip de arbori a cîștigat aproape un euro pe MWh prin setări bune.

## Modelele fundaționale prognozează prețurile fără nicio antrenare {h=1f7398d1}

Modelele Chronos au fost antrenate de Amazon pe colecții mari de serii de timp (Ansari et al., 2024; Ansari et al., 2025). Noi le dăm doar prețurile recente și le cerem următoarele 24 de ore, fără nicio antrenare pe datele din România (*zero-shot*):

$$ \big(\hat q^{\tau}_{d,h}\big)_{h=0,\dots,23}^{\tau=0{,}1;\,0{,}5;\,0{,}9}=g\big(P_{t-2047},\dots,P_{t}\big) $$ {#eq:chronos}

unde $P_{t-2047},\dots,P_t$ sînt ultimele 2048 de prețuri orare, pînă la sfîrșitul zilei $d-1$ (85 de zile), $g$ este rețeaua preantrenată, folosită ca atare, iar $\hat q^{\tau}_{d,h}$ cuantila de nivel $\tau$ prognozată pentru ora $h$ a zilei $d$. Prognoza punctuală este mediana $\hat q^{0{,}5}$.

În anul de test, numai cu prețuri și fără variabile fundamentale, Chronos-2 are MAE 20,82 EUR/MWh, Chronos-Bolt 22,15, iar AW-LEAR 22,53. Chronos-2 este mai precis decît AW-LEAR (DM: $p<0{,}001$), și asta în toate cele 24 de ore. Rezultatul este robust: în anul de validare, Chronos-2 avea 21,05, față de 22,59 pentru cea mai bună rețea DNN calibrată, iar modelul a fost publicat în octombrie 2025, înaintea anului de test, deci nu putea să fi văzut aceste prețuri.

@practice testați un model fundațional înainte de a construi propria rețea: costă puțin, iar aici a fost cel mai precis model individual.

## Chronos-2 este mai precis decît AW-LEAR în fiecare oră a zilei {h=f83dd7ef}

Graficul compară, oră cu oră, MAE a celor două modele Chronos cu cea a modelului AW-LEAR, în anul de test. Chronos-2 se află sub AW-LEAR în fiecare oră. Chronos-Bolt, mai mic și mai vechi, este la egalitate cu AW-LEAR (DM: $p$ = 0,220).

Cuantilele din @eq:chronos dau și un interval de prognoză. Intervalul 10%–90% al modelului Chronos-2 ar trebui să conțină 80% din prețuri, dar conține 76,5%: este prea îngust, deci modelul își subestimează propria incertitudine.

@practice folosiți mediana și recalibrați intervalele (cursul 2) înainte de a dimensiona riscul cu ele.

@chart foundation_hour
MAE pe ore ale zilei în anul de test, pentru Chronos-2, Chronos-Bolt și AW-LEAR.

## AIDA 2026: DNN întrece LEAR, modelele preantrenate concurează {h=6a82de0f}

La conferința AIDA 2026 (Academia de Studii Economice din București, iunie 2026), conferința invitată a lui Rafał Weron ([diapozitive](https://github.com/danpele/EMQA/blob/main/resources/aida2026/weron_ml_electricity_price_forecasting.pdf)) a urmărit evoluția modelelor pentru prețul energiei electrice, de la modelele ARX și medierea pe ferestre de calibrare la LEAR și apoi la rețelele neuronale profunde și interpretabile. Rezultatele și cifrele de mai jos sînt cele de pe diapozitivele conferinței.

- **Rețelele profunde față de LEAR.** În evaluarea deschisă care însoțește codurile LEAR și DNN din biblioteca epftoolbox, rețeaua DNN a avut rMAE mai mică decît LEAR pe toate cele cinci piețe prezentate ([Lago et al., 2021](https://doi.org/10.1016/j.apenergy.2021.116983)).
- **Rețele interpretabile.** NBEATSx descompune prognoza în blocuri de trend, sezonalitate și variabile exogene, astfel încît o rețea profundă poate fi citită ca o descompunere ([Olivares et al., 2023](https://doi.org/10.1016/j.ijforecast.2022.03.001)).
- **Modele zero-shot.** Modelele preantrenate, folosite fără reantrenare, au fost comparate cu LEAR și cu rețele DNN distribuționale pentru cele 24 de prețuri orare ale zilei următoare, cu o fereastră de antrenare glisantă de 4 ani și un test între 2021 și 2025. În 2022, RMSE a fost 45,71 pentru LEAR cu predicție conformală, 41,07 pentru Chronos 2 și 34,39 pentru TabPFN v3.0 ts; în 2025 a fost 20,38, 20,58 și, respectiv, 17,66. O versiune TabPFN a avut cea mai mică RMSE în fiecare an, dar clasamentele se schimbă: TabPFN v2.0 a avut RMSE 68,85 în 2022 și 17,52 în 2025.

Anul nostru de test arată același lucru: Chronos-2, folosit fără reantrenare, este cel mai precis model individual (MAE 20,82 EUR/MWh, față de 22,53 pentru AW-LEAR). Rezultatele conferinței adaugă avertismentul că un singur an nu ajunge pentru a ordona modelele.

@practice păstrați LEAR ca reper și testați modelele zero-shot alături de el, pe mai mulți ani.

## AIDA 2026: patru generații de modele pe 27 de serii europene de prețuri {h=0e9b9f9a}

La aceeași conferință, Alexandru-Victor Andrei ([diapozitive](https://github.com/danpele/EMQA/blob/main/resources/aida2026/andrei_ai4efin_benchmarking.pdf)) a prezentat o comparație a patru generații de metode de prognoză a seriilor de timp pe prețurile energiei electrice ([Andrei, Velev, Toma, Pele și Lessmann, 2024](https://arxiv.org/abs/2411.03372)). Cifrele de mai jos sînt cele de pe diapozitive.

- **Patru generații.** Au fost comparate unsprezece modele: modele econometrice, precum modelul autoregresiv integrat cu medie mobilă (ARIMA); modele de învățare profundă (DLinear, NLinear, TSMixer); transformere (Autoformer, Basisformer, Informer, PatchTST, Quatformer); și modele preantrenate adaptate din modelele mari de limbaj (LLM), Chronos și TimesFM, folosite fără reantrenare.
- **Date și validare walk-forward.** Prețurile angro ale energiei electrice pentru 27 de țări ale Uniunii Europene (UE) provin de pe platforma Ember (sursa inițială: ENTSO-E). Fiecare model citește 96 de pași de timp și îi prognozează pe următorii 96; fiecare fereastră de antrenare are 2000 de ore (83 de zile), fiecare fereastră de test 500 de ore (20 de zile), iar ferestrele avansează în timp. Modelele sînt clasate după scorul (100·SMAPE + RMSE)/2, unde SMAPE este eroarea procentuală absolută medie simetrică.
- **Rezultate.** PatchTST este pe primul sau al doilea loc în toate cele 27 de țări. Pentru România, locurile sînt: PatchTST 1, TimesFM 2, Chronos 8 și ARIMA 9; pentru Germania: PatchTST 1, TimesFM 5 și Chronos 10. Transformerele (PatchTST) și modelele fundaționale (TimesFM) conduc, dar cîștigurile depind de model și nu sînt uniforme în generația a patra.

În acest curs, mai noul Chronos-2 (2025), folosit fără reantrenare pe prețurile românești pentru ziua următoare, este cel mai precis model individual (MAE 20,82 EUR/MWh).

@practice comparați generațiile de modele prin validare walk-forward, pe mai multe piețe, înainte de a alege.

## @end

Arborii construiți secvențial și calibrați sînt mai buni decît modelul GBM din cursul 2, dar rămîn în urma modelului AW-LEAR. Chronos-2, preantrenat și fără nicio antrenare pe datele noastre, este mai precis decît AW-LEAR în fiecare oră.

# Comparație corectă, combinare și cost

Toate modelele sînt comparate acum pe același an de test, cu aceleași măsuri ale erorii și cu teste DM față de AW-LEAR. Secțiunea arată că combinațiile dintre învățarea automată și modelele statistice sînt semnificativ mai bune, explică de ce funcționează media și pune acuratețea în balanță cu costul de calcul.

## Clasamentul: Chronos-2 este cel mai bun model individual {h=7951ab4e}

Tabelul reunește toate modelele, în anul de test. RMSE penalizează erorile mari mai mult decît MAE; rMAE împarte MAE la cea a modelului naiv; coloana „față de AW-LEAR” dă cîștigul procentual față de AW-LEAR; iar „DM, p” este valoarea p a unui test unilateral că modelul este mai precis decît AW-LEAR, calculat pe eroarea absolută medie zilnică, cu varianță Newey–West, ca în cursul 2 (Diebold și Mariano, 1995).

| Model | MAE | RMSE | rMAE | față de AW-LEAR, % | DM, p |
|---|---|---|---|---|---|
| Naiv | 27,82 | 44,54 | 1,000 | −23,5 | – |
| AW-ARX | 22,30 | 36,34 | 0,802 | +1,0 | 0,203 |
| AW-LEAR | 22,53 | 36,35 | 0,810 | +0,0 | – |
| Ansamblul de 4 (cursul 2) | 22,13 | 35,76 | 0,795 | +1,8 | 0,014 |
| GBM (cursul 2) | 24,05 | 37,73 | 0,864 | −6,7 | 1,000 |
| MLP (cursul 2) | 25,54 | 40,05 | 0,918 | −13,3 | 1,000 |
| XGBoost, calibrat | 23,26 | 36,94 | 0,836 | −3,2 | 0,984 |
| DNN, calibrată | 22,95 | 36,42 | 0,825 | −1,8 | 0,944 |
| Chronos-Bolt, fără antrenare | 22,15 | 35,65 | 0,796 | +1,7 | 0,220 |
| Chronos-2, fără antrenare | 20,82 | 34,32 | 0,748 | +7,6 | <0,001 |
| AW-LEAR + DNN + XGBoost | 21,97 | 35,42 | 0,790 | +2,5 | 0,001 |
| AW-ARX + AW-LEAR + DNN + XGBoost | 21,69 | 35,25 | 0,779 | +3,8 | <0,001 |
| AW-LEAR + Chronos-2 | 20,81 | 34,11 | 0,748 | +7,6 | – |
| Ansamblul de 5 (cu Chronos-2) | 21,12 | 34,50 | 0,759 | +6,3 | <0,001 |

Se desprind trei concluzii. Calibrate, rețeaua DNN și XGBoost sînt mai bune decît versiunile lor din cursul 2, dar, luate separat, rămîn puțin în urma modelului AW-LEAR. Chronos-2, fără antrenare, este cel mai bun model individual, cu 7,6% sub AW-LEAR. Iar orice combinație care amestecă învățarea automată cu modelele statistice este semnificativ mai precisă decît AW-LEAR.

## Testele DM: combinațiile cu ML depășesc semnificativ AW-LEAR {h=fd3fa090}

Graficul este o matrice de teste DM unilaterale pe cele 365 de zile ale anului de test: fiecare celulă dă valoarea p a testului că modelul de pe rînd este mai precis decît modelul de pe coloană. Valorile p mici marchează cîștiguri greu de pus pe seama întîmplării.

Combinația AW-LEAR + DNN + XGBoost este mai precisă decît AW-LEAR ($p$ = 0,001), deși niciunul dintre modelele de învățare automată nu reușește acest lucru singur. Cu AW-ARX adăugat, MAE scade la 21,69, sub ansamblul din cursul 2 ($p<0{,}001$). În schimb, adăugarea AW-LEAR la Chronos-2 nu schimbă nimic ($p$ = 0,491): în zilele dificile, cele două modele greșesc asemănător, așa că media lor nu aduce un cîștig de acuratețe.

@chart dm_matrix
Matricea valorilor p ale testelor DM unilaterale între toate modelele, în anul de test (modelul de pe rînd mai precis decît cel de pe coloană).

## Media funcționează pentru că erorile nu sînt identice {h=e7a47eac}

De ce media a două modele le depășește pe amîndouă? Pentru două erori de prognoză $e_1$ și $e_2$, cu abaterile standard $\sigma_1$, $\sigma_2$ și corelația $\rho$,

$$ \Var\Big(\tfrac{e_1+e_2}{2}\Big)=\tfrac14\big(\sigma_1^2+\sigma_2^2+2\rho\sigma_1\sigma_2\big) $$ {#eq:combo}

astfel încît, atîta timp cît $\rho<1$, media greșește mai puțin decît ar greși, în medie, cele două modele luate separat (Bates și Granger, 1969). Pe datele noastre, corelația erorilor cu AW-LEAR este 0,94 pentru rețeaua DNN și 0,89 pentru XGBoost: mare, dar sub 1, și asta este suficient.

Graficul arată MAE a combinației în funcție de ponderea dată modelului de învățare automată. Ponderile egale sînt aproape la fel de bune ca ponderea optimă văzută ulterior (0,40). Această pondere optimă este doar o ilustrare, fiindcă este citită din anul de test; în practică nu putea fi cunoscută dinainte.

@practice faceți media cu ponderi egale înainte de a estima ponderi „inteligente”.

@chart combo_weight
MAE în anul de test a combinației dintre AW-LEAR și un model de învățare automată, în funcție de ponderea acestuia din urmă; ponderile egale și ponderea optimă văzută ulterior sînt marcate.

## Lunar, combinația este mai precisă decît AW-LEAR în 10 din 12 luni {h=b5d91b2f}

O medie anuală poate ascunde luni în care un model este mult mai slab. Graficul arată MAE a fiecărui model în fiecare lună a anului de test. Luate separat, XGBoost și rețeaua DNN depășesc AW-LEAR fiecare doar în 3 luni; în medie cu acesta, în 10 luni.

Toate modelele greșesc mai mult în aceleași luni, ianuarie, iunie și octombrie: zilele dificile sînt dificile pentru toate. De aceea combinația ajută în lunile obișnuite, dar nu poate elimina erorile mari din lunile grele.

@practice raportați comitetului de risc acuratețea lună de lună, nu doar media anuală.

@chart monthly_ml
MAE lunară în anul de test pentru AW-LEAR, rețeaua DNN, XGBoost și combinația lor.

## Costul de calcul: LEAR zilnic este cel mai scump, ML costă minute {h=31fd863a}

Acuratețea este doar jumătate din alegerea unui model; cealaltă jumătate este costul. Pe tot anul de test, pe un singur nucleu, AW-LEAR are nevoie de 87,6 minute, pentru că este reestimat pentru 365 de zile $\times$ 3 ferestre $\times$ 24 de ore. XGBoost are nevoie de 2,6 minute, rețeaua DNN de 2,7, iar Chronos-2 de numai 0,3, fiindcă nu este antrenat niciodată.

Acești timpi nu includ costurile ascunse: căutarea setărilor (7,3 minute), preantrenarea modelelor Chronos (făcută de alții) și, mai ales, oamenii care întrețin zilnic fluxul de date. Comparația răstoarnă o idee răspîndită: pe această problemă, modelul statistic de referință, reestimat în fiecare zi, este cel scump, iar învățarea automată reestimată lunar costă cîteva minute.

@practice comparați modelele după eroare raportată la costul total de utilizare, nu doar după eroare.

@chart cost_gain
Timpul de calcul în anul de test (un nucleu al unui laptop cu 18 nuclee) față de cîștigul de MAE în raport cu AW-LEAR, pe modele.

## @end

Combinațiile dintre învățarea automată și modelele statistice sînt semnificativ mai precise decît AW-LEAR, pentru că erorile lor nu sînt perfect corelate. Chronos-2 este cel mai precis model individual, iar modelele de învățare automată costă doar minute de calcul.

# Explicarea prognozelor

O prognoză care nu poate fi explicată este greu de acceptat și imposibil de auditat. Secțiunea descompune fiecare prognoză a arborilor în contribuțiile variabilelor, cu valorile Shapley, și măsoară de ce depinde rețeaua neuronală prin importanța calculată prin permutare.

## Valorile Shapley descompun fiecare prognoză în contribuțiile variabilelor {h=4dc56058}

Contribuția unei variabile este efectul ei mediu atunci cînd este adăugată în model, calculat pe toate ordinile posibile de adăugare a variabilelor (Shapley, 1953; Lundberg et al., 2020):

$$ \phi_j=\sum_{S\not\ni j}\tfrac{|S|!\,(p-|S|-1)!}{p!}\big[v(S\cup\{j\})-v(S)\big] $$ {#eq:shapley}

$$ \hat f(\mathbf x)=\phi_0+\textstyle\sum_{j}\phi_j $$ {#eq:additive}

unde $\phi_j$ este valoarea variabilei $j$ după metoda explicațiilor aditive bazate pe valorile Shapley (SHAP, *SHapley Additive exPlanations*), $S$ o submulțime a celorlalte variabile, $|S|$ numărul ei de elemente, $v(S)$ prognoza așteptată cînd se cunosc doar variabilele din $S$, $\phi_0$ prognoza medie, $\hat f(\mathbf x)$ prognoza pentru intrările $\mathbf x$, iar $p$ = 20 numărul de variabile.

Valorile Shapley sînt singura împărțire echitabilă în sensul teoriei jocurilor, iar @eq:additive arată că se adună exact la prognoză. Pe datele noastre, pentru XGBoost, pe cele 8 760 de ore de test, cea mai mare diferență dintre $\hat f$ și $\phi_0+\sum\phi_j$ este 0,000009. Prețurile din zilele anterioare au 69,3% din contribuția totală.

@practice cereți explicația fiecărei alerte, nu doar un clasament global.

## Ce determină prognoza arborilor: prețul de ieri, la aceeași oră {h=5c700531}

Graficul ordonează variabilele modelului XGBoost după media valorii absolute SHAP, $|\phi|$, în anul de test. Pe primele locuri se află prețul din $d-1$, aceeași oră, cu 32,9% din media $|\phi|$, prețul din $d-7$, aceeași oră, cu 15,6%, și ziua săptămînii, cu 9,3%.

Consumul are 8,5%, iar producția eoliană și solară 2,5%. Aceste ponderi mici nu înseamnă că variabilele fundamentale nu contează pentru piață: ele sînt cunoscute doar pînă în $d-2$, deci la închiderea licitației sînt informații vechi, reflectate deja în prețurile de ieri. Intrări mai bune, cum ar fi prognozele consumului și ale producției eoliene pentru ziua de mîine, ar aduce mai multă informație.

@practice cumpărați întîi intrări mai bune: prognozele operatorului de transport și de sistem (TSO).

@chart shap_global
Media valorii absolute SHAP a fiecărei variabile a modelului XGBoost, ca pondere din total, în anul de test, 8 760 de ore.

## Producția eoliană și solară scade prețul doar în orele în care este mare {h=921bf65f}

Fiecare punct din grafic este o oră din anul de test: pe axa orizontală, producția eoliană și solară din $d-2$ la acea oră; pe axa verticală, contribuția ei SHAP la prognoză. Cu cît producția eoliană și solară este mai mare, cu atît contribuția este mai negativă (corelație −0,64).

Relația nu este o linie dreaptă. Efectul apare peste aproximativ 2 gigawați (GW), mai ales la prînz, și este aproape nul sub acest nivel: un prag pe care un model liniar nu îl poate exprima, dar pe care arborii îl învață singuri.

@practice un dezvoltator de parcuri solare poate citi aici reducerea de preț la care contribuie chiar producția sa.

@chart shap_res
Contribuția SHAP a producției eoliene și solare în funcție de nivelul ei din $d-2$, cîte un punct pentru fiecare oră de test.

## Rețeaua neuronală se bazează și mai mult pe prețurile de ieri {h=f9c69bbd}

Valorile Shapley se calculează ușor pentru arbori, dar greu pentru o rețea. O măsură mai simplă se aplică oricărui model: importanța prin permutare (Breiman, 2001),

$$ I_b=\text{MAE}_{b\ \text{amestecat}}-\text{MAE} $$

unde $I_b$ este importanța blocului de variabile $b$, $\text{MAE}_{b\ \text{amestecat}}$ eroarea atunci cînd valorile blocului $b$ sînt amestecate între zilele de test, iar $\text{MAE}$ eroarea fără amestecare; rezultatul este o medie pe 5 permutări.

Pentru rețeaua DNN, amestecarea prețurilor din $d-1$ crește MAE cu 22,82 EUR/MWh, a zilei săptămînii cu 3,66, a consumului cu 2,12, în timp ce producția eoliană și solară o modifică cu −0,08, adică deloc. Rețeaua depinde de prețurile de ieri chiar mai mult decît arborii.

@practice monitorizați întîi fluxul prețurilor din $d-1$: fără el, rețeaua cedează.

@chart perm_dnn
Importanța prin permutare a blocurilor de variabile ale rețelei DNN în anul de test, creșterea MAE în EUR/MWh, 5 permutări.

## Finanțele energiei folosesc învățarea automată, dar rar o explică {h=929f4242}

La aceeași conferință, Roxana Clodnitchi ([diapozitive](https://github.com/danpele/EMQA/blob/main/resources/aida2026/clodnitchi_ai_energy_finance_review.pdf)) a prezentat o analiză sistematică a literaturii despre inteligența artificială (AI) în finanțele energiei ([Anagnoste et al., 2025](https://doi.org/10.1016/j.esr.2025.101833)). Au fost examinate circa 700 de articole din Web of Science, iar 232 de articole evaluate colegial, din perioada 2020–2025, au fost reținute și grupate pe șase piloni ai finanțelor energiei. Cifrele de mai jos sînt cele de pe diapozitive.

- **Unde se folosește AI.** Ponderea lucrărilor care folosesc AI sau învățare automată este 100% pentru mecanismele de preț și pentru derivatele pe energie, 97,5% pentru piețele energetice și financiare, 93,0% pentru gestiunea riscului, 60,4% pentru finanțele verzi și 0% pentru finanțele corporative ale firmelor de energie, care se bazează pe econometria datelor panel.
- **Ce metode.** Domină rețelele neuronale: le folosesc 88,2% din lucrările despre derivate și 72,1% din cele despre gestiunea riscului.
- **Ce lipsește.** AI explicabilă apare în 19,6% din lucrările despre derivate și în 0–5% din lucrările celorlalți piloni; analiza propune ca pas următor AI explicabilă și învățarea automată cauzală, pentru autoritățile de reglementare și pentru evaluarea politicilor.

Valorile SHAP și importanța prin permutare din această secțiune sînt tocmai tipul de explicație pe care analiza îl găsește rar.

@practice cereți explicația odată cu prognoza: autoritățile și consiliile de administrație o vor cere.

## @end

Ambele modele de învățare automată se bazează în primul rînd pe prețul de ieri, la aceeași oră. Producția eoliană și solară contează doar peste un prag, pe care un model liniar nu îl poate surprinde.

# Vîrfuri de preț, prețuri negative și un studiu de caz

Pentru mulți utilizatori, orele extreme contează mai mult decît eroarea medie: o baterie sau un consumator flexibil își cîștigă banii în orele cu vîrfuri și cu prețuri negative. Secțiunea definește aceste evenimente, construiește clasificatori care le dau probabilitatea, transformă probabilitățile în decizii cu o regulă cost–pierdere și analizează, într-un studiu de caz, cel mai mare preț din anul de test.

## Vîrfurile de preț apar seara, prețurile negative la prînz {h=a40f1d4e}

Un vîrf de preț este o oră cu preț peste $\theta$, percentila 90 a prețurilor orare din cele 12 luni dinaintea lunii de livrare. Pragul urmărește piața, așa că se mișcă de-a lungul anului de test, între 166,8 și 202,4 EUR/MWh. Cu această definiție, 22,1% din orele de test sînt vîrfuri, mult peste una din zece cît ar da definiția pe o piață stabilă; cele mai multe apar la ora 19, cînd 57,0% din zile au un vîrf.

Prețurile mai mici sau egale cu zero sînt evenimentul opus: 255 de ore, în 53 de zile din anul de test, mai ales în jurul orei 13, cînd producția solară este maximă. Graficul arată ponderea zilelor cu fiecare eveniment, pe ore ale zilei.

@practice o baterie se încarcă la prînz și se descarcă la orele 19–20: cele două evenimente sînt chiar modelul ei de afaceri.

@chart events_hour
Ponderea zilelor din anul de test cu vîrf de preț și cu preț mai mic sau egal cu zero, pe ore ale zilei.

## Clasificarea vîrfurilor: o prognoză bună de preț le detectează deja {h=f2d878e5}

Un clasificator dă probabilitatea ca o oră să fie un vîrf; judecăm cît de bine ordonează orele și cît de corecte sînt probabilitățile lui:

$$ \hat\pi_{d,h}=\Pr\big(P_{d,h}>\theta_d\mid\mathbf x_{d,h}\big) $$ {#eq:spikeprob}

$$ \text{Brier}=\frac{1}{n}\sum_{d,h}\big(\hat\pi_{d,h}-S_{d,h}\big)^2 $$ {#eq:brier}

unde $\hat\pi_{d,h}$ este probabilitatea prognozată a unui vîrf în ora $h$ a zilei $d$, $\theta_d$ pragul de vîrf, $\mathbf x_{d,h}$ variabilele explicative, $S_{d,h}$ este 1 dacă ora este un vîrf și 0 altfel, iar $n$ numărul de ore (Brier, 1950). După ce probabilitățile sînt transformate în alerte, precizia este ponderea alertelor urmate de vîrfuri, sensibilitatea este ponderea vîrfurilor semnalate, iar F1 media lor armonică. Aria de sub curbă (AUC) este probabilitatea ca o oră cu vîrf să primească un scor mai mare decît o oră obișnuită (Fawcett, 2006).

Pe datele noastre, clasificatorii XGBoost și logistic sînt reestimați lunar. Vîrfurile apar în 22,1% din orele de test, dar numai în 14,3% din ultimul eșantion de antrenare. Scorul Brier al modelului XGBoost este 0,072, față de 0,172 pentru o constantă egală cu ponderea vîrfurilor. Se adaugă două repere: persistența, adică ponderea vîrfurilor la aceeași oră în ultimele 7 zile, și chiar prognoza de preț AW-LEAR, comparată cu $\theta$.

@practice judecați o alertă după probabilitățile ei, nu doar după cîte vîrfuri semnalează.

## Alertele din anul de test: AW-LEAR egalează un clasificator dedicat {h=8513b220}

Tabelul prezintă scorurile din anul de test: coloanele 2–6 pentru vîrfuri (1 938 de ore), coloanele 7–8 pentru prețurile mai mici sau egale cu zero (255 de ore). O alertă se emite cînd probabilitatea depășește 0,5; pentru AW-LEAR, cînd prognoza prețului depășește $\theta$ (sau este mai mică sau egală cu zero).

| Model | AUC, vîrfuri | Precizie | Sensibilitate | F1 | Brier | AUC, preț ≤ 0 | F1, preț ≤ 0 |
|---|---|---|---|---|---|---|---|
| XGBoost | 0,953 | 0,826 | 0,685 | 0,749 | 0,072 | 0,980 | 0,571 |
| Regresie logistică | 0,953 | 0,847 | 0,641 | 0,730 | 0,072 | 0,980 | 0,581 |
| Persistență, 7 zile | 0,918 | 0,761 | 0,681 | 0,719 | 0,083 | 0,847 | 0,205 |
| Prognoza AW-LEAR > θ | 0,959 | 0,851 | 0,733 | 0,788 | – | 0,983 | 0,558 |

Surpriza este pe ultimul rînd: prognoza de preț AW-LEAR, comparată cu pragul, detectează vîrfurile cel puțin la fel de bine ca clasificatorii dedicați, cu cea mai mare AUC (0,959) și cel mai mare F1 (0,788). La prețurile negative, toate modelele se descurcă mai slab; XGBoost semnalează doar o fracțiune 0,467 din evenimente la pragul 0,5, pentru că aceste ore sînt rare și depind de vremea de mîine.

@practice cumpărați un serviciu de alertă pentru vîrfuri doar dacă depășește semnalul ascuns deja în prognoza dumneavoastră de preț.

## Persistența detectează vîrfurile, dar nu și prețurile negative {h=8c8f2ab0}

Graficul prezintă curbele caracteristice de operare a receptorului (ROC, *receiver operating characteristic*): pentru fiecare prag de alertă, ponderea evenimentelor semnalate față de ponderea alarmelor false. La vîrfuri, AUC variază între 0,918 pentru persistență și 0,959 pentru AW-LEAR. Chiar și persistența se descurcă bine, deoarece vîrful de seară se repetă de la o zi la alta.

La prețurile negative imaginea se schimbă: persistența are AUC 0,847, față de 0,980 pentru XGBoost. Prețurile negative depind de soarele și vîntul de mîine, nu de ziua de ieri, așa că o regulă care privește doar trecutul ratează multe dintre ele.

@chart roc
Curbele ROC ale clasificatorilor și ale reperelor în anul de test, pentru vîrfuri (stînga) și pentru prețuri mai mici sau egale cu zero (dreapta), 8 760 de ore.

## Regula cost–pierdere: reacționați cînd probabilitatea depășește C/L {h=275221dc}

O probabilitate devine utilă numai cînd este transformată într-o decizie. Să luăm 1 MW de consum flexibil, care poate fi mutat dintr-o oră cu alertă. Reacția costă $C$; un vîrf ratat costă în medie $\bar L$. Regula clasică cost–pierdere (Murphy, 1977) spune să reacționăm atunci cînd

$$ \hat\pi_{d,h}>\frac{C}{\bar L}=\frac{30}{72{,}5}=0{,}414 $$ {#eq:costloss}

unde $C$ = 30 EUR/MWh este costul presupus al reacției, iar $\bar L$ = 72,5 EUR/MWh este depășirea medie a pragului $\theta$ în anul de validare. Mutarea a 1 MWh dintr-o oră cu alertă aduce $P_{d,h}-\theta_d-C$.

Graficul arată valoarea regulii în anul de test, în funcție de prag. Pe MW și an, regula la pragul C/L aduce 33,0 mii EUR, persistența 11,8, iar informația perfectă 62,4. Cel mai bun prag văzut ulterior (0,64) ar fi adus mai mult, dar este înțelepciune retrospectivă și nu putea fi ales dinainte.

@practice stabiliți pragul din propriile costuri; cel mai bun prag văzut ulterior este înțelepciune retrospectivă.

@chart decision
Valoarea pe MW și an a reacției la alertele de vîrf, în funcție de pragul de probabilitate, cu pragul C/L, persistența și informația perfectă marcate; 1 MW de consum flexibil, C = 30 EUR/MWh.

## Studiu de caz, 30 iunie 2026: vîrf anticipat, amploare subestimată {h=32d50d6f}

Studiul de caz privește săptămîna 27 iunie 2026 – 3 iulie 2026. La 30 iunie 2026, ora 20:00 CET, prețul a atins 954,59 EUR/MWh, cel mai mare preț din anul de test. Toate modelele se așteptau la un preț ridicat: AW-LEAR a prognozat 520, XGBoost 499, rețeaua DNN 614, iar Chronos-2 607 EUR/MWh, în timp ce probabilitatea vîrfului era 0,992. Niciun model nu s-a apropiat însă de nivelul efectiv.

În întreaga săptămînă au fost 47 de ore cu vîrfuri; regula la pragul C/L a emis 45 de alerte, iar 39 dintre ele au fost corecte. Alerta a funcționat; amploarea vîrfului a fost ratată de toate modelele.

@practice probabilitatea arată dacă reacționați, prognoza punctuală arată cît.

@chart case_week
Prețurile orare și prognozele AW-LEAR, XGBoost, DNN și Chronos-2, 27 iunie – 3 iulie 2026, cu orele cu alertă marcate.

## Studiu de caz: arborii au urmat seara extremă din ziua precedentă {h=3561480f}

Graficul descompune prognoza modelului XGBoost pentru 30 iunie 2026, ora 20:00 CET, în contribuții SHAP exprimate în EUR/MWh (anexa C explică trecerea de la scara asinh). Prognoza urcă de la 125 EUR/MWh, prognoza medie a modelului, la 499. Prețul din $d-1$, aceeași oră, adaugă 213, iar prețul din $d-7$ adaugă 64: arborii au urmat seara extremă din ziua precedentă.

Descompunerea arată și o limită a arborilor: ei nu pot depăși prețurile memorate în frunze, deci valorile extreme sînt plafonate. Un preț mult peste tot ce s-a văzut în antrenare nu poate fi prognozat de o sumă de valori ale frunzelor învățate din trecut.

@practice prezentați consiliului de administrație această descompunere pentru fiecare alertă importantă.

@chart shap_local
Contribuțiile SHAP în EUR/MWh la prognoza XGBoost pentru 30 iunie 2026, ora 20:00 CET, de la prognoza medie a modelului la prognoza finală.

## Avertizarea timpurie a vîrfurilor: lucrarea grupului și replicarea ei {h=32f10f0a}

Andrei, Pele, Cramer, Amza și Diaconu (2026) au construit un sistem de avertizare timpurie a vîrfurilor pentru PZU din România. Au folosit 5 000 de ore din 2024, cu date despre consum, surse regenerabile și combustibili, au definit vîrful drept un preț peste percentila 90 și au combinat păduri aleatoare și XGBoost, explicate cu SHAP, într-un scor de avertizare construit din pragurile mai multor indicatori. Rezultatul lor: prețul anterior și prognoza consumului rezidual sînt principalii factori ai vîrfurilor.

Replicarea noastră, studiul de caz C7, folosește numai informația de la închiderea licitației. În perioada de test iulie 2025 – octombrie 2026, vîrfurile apar în 22,1% din ore (10,0% în antrenare). XGBoost atinge o AUC de 0,946, iar principalii săi factori sînt prețul de ieri și cel de acum o săptămînă, la aceeași oră, ca pe diapozitivele anterioare. Rezultatele lucrării sînt cele raportate de autori; cifrele replicării sînt calculate cu notebook-ul Jupyter al studiului de caz C7, pe datele noastre.

@practice prognoza consumului rezidual este variabila de care un model de vîrfuri are cea mai mare nevoie și care lipsește din datele noastre publice.

## @end

Vîrfurile de preț apar seara, iar prețurile negative la prînz. O prognoză bună de preț detectează deja vîrfurile, regula cost–pierdere transformă probabilitățile în bani, iar niciun model nu a anticipat amploarea celui mai mare vîrf.

# Capcane care fac un model să pară mai bun

Cele mai multe promisiuni de cîștiguri mari din învățarea automată provin din greșeli de evaluare, nu din modele mai bune. Secțiunea reproduce pe datele noastre trei asemenea greșeli, informația din viitor, alegerea pe anul de test și modelele neactualizate, măsoară cît de mult avantajează fiecare rezultatul și se încheie cu un test de scurgere a informației.

## Informația din viitor: două evaluări invalide avantajează XGBoost {h=ad0b50db}

Graficul compară MAE corectă a modelului XGBoost, 23,26 EUR/MWh, cu două evaluări invalide. Prima este validarea încrucișată cu 5 subeșantioane amestecate: zilele sînt amestecate înainte de împărțire, așa că zile din viitor ajung în eșantionul de antrenare. MAE scade la 22,01, cu 5,4% mai bine, dar doar pe hîrtie.

A doua folosește drept intrări consumul și producția eoliană și solară din ziua $d$, notate în grafic surse regenerabile de energie (RES). Aceste valori nu sînt cunoscute la ora 12:00 în ziua $d-1$. MAE devine 22,55, un cîștig aparent de 3,1%; aceasta este totodată limita superioară a ceea ce ar putea aduce prognoze perfecte ale acestor variabile.

@practice cereți oricărui furnizor o testare cronologică, cu fiecare intrare datată la momentul închiderii licitației.

@chart pit_leak
MAE a modelului XGBoost în anul de test, la evaluarea cronologică corectă, la validarea încrucișată cu 5 subeșantioane amestecate și cu consumul și RES din aceeași zi ca intrări.

## Alegerea pe anul de test simulează o victorie asupra LEAR {h=e0c49865}

Rețeaua DNN aleasă corect, la validare, cu o singură inițializare, are MAE 23,34 EUR/MWh în anul de test. Dacă alegem în schimb cea mai bună dintre cele 25 de setări direct pe anul de test, obținem 22,52, chiar sub AW-LEAR (22,53): o victorie aparentă asupra modelului statistic de referință, creată doar prin alegerea pe datele folosite pentru evaluare (White, 2000).

Graficul pune față în față MAE a fiecărei setări în anul de validare și MAE ei în anul de test. Clasamentele sînt apropiate, cu o corelație Spearman de 0,86 pentru rețeaua DNN și 0,94 pentru XGBoost: validarea funcționează, dar nu este perfectă, iar tocmai această diferență este exploatată de alegerea pe anul de test.

@practice întrebați cîte modele au fost încercate înaintea celui prezentat: cu cît sînt mai multe încercări, cu atît cel mai bun pare mai bun decît este.

@chart snooping
MAE din anul de validare față de MAE din anul de test pentru cele 25 de setări ale fiecărui model, cîte o inițializare pe configurație, cu AW-LEAR marcat.

## Cel mai bun dintre multe modele trebuie testat față de reper {h=89e8fe68}

Alegerea celui mai bun dintre multe modele pe aceleași date este o problemă de testare multiplă. Cu $m$ teste independente la pragul de 5%, probabilitatea a cel puțin unei victorii false este $1-0{,}95^m$: 0,401 pentru $m=10$ și 0,994 pentru $m=100$. Conferința invitată a lui Chung-Ming Kuan la AIDA 2026 ([diapozitive](https://github.com/danpele/EMQA/blob/main/resources/aida2026/kuan_multiple_inequality_testing.pdf)) a prezentat testele care controlează acest risc; conținutul de mai jos urmează diapozitivele conferinței.

Testul Reality Check (RC) al lui White compară simultan toate modelele cu reperul,

$$ \mathrm{RC}_n=\max_{k=1,\dots,m}\sqrt{n}\,\bar d_k,\qquad \bar d_k=\frac1n\sum_{t=1}^{n}d_{k,t} $$

unde $d_{k,t}$ este pierderea reperului minus pierderea modelului $k$ în ziua $t$, iar ipoteza nulă $E(d_{k,t})\le 0$ pentru orice $k$ spune că niciun model nu întrece reperul. Valoarea critică se obține prin bootstrap pe întregul vector $(d_{1,t},\dots,d_{m,t})$, care păstrează corelația dintre modele ([White, 2000](https://doi.org/10.1111/1468-0262.00152)).

- Testul Reality Check este conservator: modelele slabe adăugate în set îi reduc puterea ([Hansen, 2005](https://doi.org/10.1198/073500105000000063)).
- Testul abilității predictive superioare (SPA) al lui Hansen (2005) recentrează modelele slabe și este mai puternic.
- Variantele pas cu pas, Step-RC ([Romano & Wolf, 2005](https://doi.org/10.1111/j.1468-0262.2005.00615.x)) și Step-SPA ([Hsu, Hsu & Kuan, 2010](https://doi.org/10.1016/j.jempfin.2010.01.001)), identifică modelele care întrec reperul, controlînd rata erorii la nivelul familiei de ipoteze (FWER).

Pe datele noastre, cea mai bună dintre cele 25 de setări DNN pe anul de test trece chiar sub AW-LEAR: exact selecția pe care o corectează testele Reality Check și SPA.

@practice cînd vi se arată cel mai bun dintre multe modele, cereți valoarea p a testului RC sau SPA.

## Reestimarea: un model neactualizat un an pierde 4,2% {h=094d9807}

Piețele se schimbă, așa că un model trebuie reestimat. Graficul compară modelul XGBoost reestimat lunar cu o versiune estimată o singură dată, înaintea anului de test, și cu o versiune estimată pe o fereastră glisantă scurtă. Modelul neactualizat are MAE 24,25, cu 4,2% mai slab. Pierderea crește în timp: +0,15 EUR/MWh în primele 3 luni și +3,70 în ultimele 3.

O fereastră glisantă scurtă, de 365 de zile, este chiar mai slabă (MAE 25,59) decît întregul istoric: arborii au nevoie de multe vîrfuri din trecut pentru a învăța, iar un singur an nu conține destule.

@practice includeți reestimarea lunară în calendarul operațional, cu un responsabil, ca pe orice alt control.

@chart pit_retrain
MAE a modelului XGBoost în anul de test, cu reestimare lunară pe tot istoricul, estimat o singură dată și cu fereastră glisantă de 365 de zile, plus diferența lunară a modelului neactualizat.

## Testul de scurgere a informației: ștergerea viitorului nu schimbă nimic {h=9c11cb69}

Un test simplu arată dacă un flux de prelucrare a datelor folosește, fără să vrea, informație din viitor. Pentru prima zi din fiecare dintre cele 12 luni de test, toate datele de după ora 12:00 din ziua $d-1$ sînt șterse, apoi înlocuite cu 10 000 EUR/MWh. XGBoost, rețeaua DNN și clasificatorul de vîrfuri sînt reestimate și trebuie să dea aceleași prognoze.

Așa se întîmplă. Arborii și clasificatorul dau prognoze identice, iar rețeaua DNN diferă cu mai puțin de 0,001 EUR/MWh, din cauza rotunjirilor calculelor paralele. Pentru Chronos, codul verifică faptul că contextul este construit numai din zilele dinaintea zilei $d$.

Testul încheie o listă de verificare valabilă înainte de a avea încredere în orice model:

- fiecare intrare datată la momentul închiderii licitației;
- setări alese pe un an de validare;
- un singur an de test, deschis o singură dată, cu teste DM față de LEAR;
- reestimări lunare și un test de perturbare ca acesta.

@practice includeți această verificare în evaluarea oricărui model, statistic sau de învățare automată.

## @end

Validarea încrucișată cu amestecare, intrările din aceeași zi și alegerea pe anul de test fac toate un model să pară mai bun decît este. Un model neactualizat se degradează, iar un test cu valori viitoare imposibile arată că fluxul de date este curat.

# Recapitulare

Cursul se încheie cu cinci întrebări cu care se poate confrunta un manager, o sinteză a rezultatelor, cercetările grupului nostru și resurse pentru studiu suplimentar.

## Verifică-te {h=7fff39a1}

1. Un start-up prezintă o rețea neuronală cu rMAE 0,70 pentru România, testată prin validare încrucișată cu 5 subeșantioane amestecate. Ce cereți? Răspuns: o testare cronologică pe un an neatins, cu intrări cunoscute la ora 12:00 în ziua $d-1$. Pe datele noastre, doar amestecarea a făcut XGBoost să pară cu 5,4% mai bun.
2. Chronos-2 are cea mai mică MAE dintre modelele individuale, iar combinația AW-LEAR + Chronos-2 are aceeași MAE. Pe care o puneți în producție? Răspuns: combinația. Are aceeași acuratețe (DM: $p$ = 0,491), dar dacă modelul preantrenat se degradează sau devine indisponibil, LEAR asigură în continuare jumătate din prognoză.
3. Consumul are o pondere SHAP mică (8,5%). Putem concluziona că acesta nu influențează prețul? Răspuns: nu. SHAP explică modelul, nu piața; consumul intră doar cu valoarea din ziua $d-2$, deja reflectată în prețul de ieri.
4. Mutarea a 1 MWh vă costă 60 EUR în loc de 30. Cum se schimbă pragul de alertă? Răspuns: se dublează. C/L crește de la 0,414 la aproximativ dublul acestei valori, deci reacționați numai la vîrfurile mai sigure.
5. Echipa de date propune ca modelul să fie antrenat o dată pe an, pentru a economisi efort. Ce arată anul de test? Răspuns: un model neactualizat un an a fost cu 4,2% mai puțin precis, iar diferența a crescut în ultimele luni, în timp ce o reestimare lunară a modelului XGBoost durează circa 13 secunde.

## Recapitulare {h=18e2817b}

Calibrate, rețeaua DNN și XGBoost sînt mai precise decît în cursul 2, dar nu depășesc singure AW-LEAR; în medie cu acesta, îl depășesc, iar cîștigul este semnificativ. Chronos-2, fără nicio antrenare, este cel mai precis model individual, cu MAE 20,82, cu 7,6% sub AW-LEAR.

Cealaltă lecție privește disciplina. Orice model, statistic sau de învățare automată, trebuie explicat, validat pe date pe care nu le-a văzut și reestimat periodic. Capcanele din ultima secțiune arată că o greșeală de evaluare poate produce ușor un cîștig mai mare decît cîștigul real al celui mai bun model.

## Cercetările grupului nostru: învățarea automată pe piața din România {h=e16df61a}

- **Avertizarea timpurie a vîrfurilor de preț** (Andrei, Pele, Cramer, Amza și Diaconu, 2026, PICBE): a construit un sistem explicabil de inteligență artificială (AI) pentru PZU din România și arată că prețul anterior și consumul rezidual sînt principalii factori ai vîrfurilor; lucrarea este replicată în studiul de caz C7.
- **Explicarea prognozelor de preț pe mai multe orizonturi** (Andrei, Pele și Cramer, 2026, PICBE): a explicat prognozele de învățare automată pentru prețurile orare din România și arată ce factori contează la fiecare orizont și în fiecare regim de preț.
- **Patru generații de modele pentru prețul energiei** (Andrei, Velev, Toma, Pele și Lessmann, 2024, [arXiv](https://arxiv.org/abs/2411.03372)): a comparat patru generații de metode de prognoză a prețurilor energiei, de la modelele statistice la învățarea profundă, oferind un reper pentru alegerea familiei de modele.
- **Modele fundaționale pentru riscul extrem** (Jheng, Tak, Găman, Mazurencu-Marinescu-Pele și Pele, 2026, ECECSR): a folosit modele fundaționale preantrenate, fără reantrenare și cu calibrare conformală, pentru prognoza pierderilor extreme pe piețele din Europa Centrală și de Est.

Rezultatele de mai sus sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.

## Lecturi și resurse suplimentare {h=d87b127d}

- **epftoolbox**: rețeaua DNN și modelul LEAR din Lago et al. (2021), cu date deschise pentru evaluare, [github.com/jeslago/epftoolbox](https://github.com/jeslago/epftoolbox).
- **XGBoost** și **shap**, documentație: [xgboost.readthedocs.io](https://xgboost.readthedocs.io), [shap.readthedocs.io](https://shap.readthedocs.io).
- **Chronos**, modele fundaționale: [github.com/amazon-science/chronos-forecasting](https://github.com/amazon-science/chronos-forecasting).
- **Interpretable Machine Learning** (C. Molnar), gratuit online: [christophm.github.io](https://christophm.github.io/interpretable-ml-book/).
- **Acest curs**: cod, date și notebook-uri Jupyter, [github.com/danpele/EMQA](https://github.com/danpele/EMQA).
- **Studiul de caz C7** replică pe datele cursului lucrarea despre avertizarea timpurie a vîrfurilor.
- **Exercițiu practic**: notebook-ul Jupyter al cursului reproduce toate graficele și cifrele, în dosarul de notebook-uri din depozitul cursului.

# Anexă

Anexa prezintă derivările din spatele antrenării rețelei și a arborilor, conversia valorilor SHAP în euro și spațiile de căutare ale hiperparametrilor.

## Anexa A: propagarea înapoi a erorii și pasul Adam {h=047655e0}

Gradientul funcției de pierdere în raport cu ponderile rețelei din @eq:dnn se obține cu regula de derivare a funcțiilor compuse, de la ieșire spre intrări:

$$ \frac{\partial\mathcal L}{\partial W_2}=\boldsymbol\delta\,\mathbf z^{\top},\quad \boldsymbol\delta=\frac{\partial\mathcal L}{\partial\hat{\mathbf Y}} $$ {#eq:bp2}

$$ \frac{\partial\mathcal L}{\partial W_1}=\big[(W_2^{\top}\boldsymbol\delta)\odot\phi'(\mathbf u)\big]\mathbf x^{\top} $$ {#eq:bp1}

unde $\boldsymbol\delta$ este derivata pierderii în raport cu ieșirile, $\mathbf u=W_1\mathbf x+\mathbf b_1$ intrarea funcției de activare, $\odot$ produsul element cu element, iar $\phi'$ derivata funcției de activare. Pentru eroarea absolută, $\partial|y-\hat y|/\partial\hat y=-\operatorname{sign}(y-\hat y)$; pentru softplus, $\phi'(u)=1/(1+e^{-u})$.

Metoda Adam (Kingma și Ba, 2015) rescalează acest gradient, astfel încît fiecare pondere are propriul pas:

$$ m_k=\beta_1m_{k-1}+(1-\beta_1)g_k $$ {#eq:adam-m}

$$ v_k=\beta_2v_{k-1}+(1-\beta_2)g_k^2 $$ {#eq:adam-v}

$$ \theta_k=\theta_{k-1}-\eta\,\frac{m_k/(1-\beta_1^k)}{\sqrt{v_k/(1-\beta_2^k)}+\varepsilon} $$ {#eq:adam}

unde $g_k$ este gradientul pe grupul de zile $k$, $m_k$ și $v_k$ mediile mobile ale gradientului și ale pătratului său, $\eta$ rata de învățare, iar $\beta_1=0{,}9$, $\beta_2=0{,}999$, $\varepsilon=10^{-8}$ sînt valorile implicite. Penalizarea ponderilor adaugă $\lambda\theta$ la $g_k$, o penalizare pătratică, aici cu $\lambda$ = $10^{-5}$.

## Anexa B: de ce valoarea optimă a unei frunze este −G/(H+λ) {h=50ba5188}

XGBoost aproximează funcția de pierdere în jurul prognozei curente $F_{m-1}$ printr-o dezvoltare Taylor de ordinul doi:

$$ \ell\big(Y_i,F_{m-1}+f\big)\approx\ell_i+g_i f(\mathbf x_i)+\tfrac12h_i f(\mathbf x_i)^2 $$ {#eq:taylor}

$$ \sum_{j}\Big[G_jw_j+\tfrac12(H_j+\lambda)w_j^2\Big]+\gamma J,\quad G_j=\textstyle\sum_{i\in R_j}g_i $$ {#eq:leafobj}

$$ w_j^{*}=-\frac{G_j}{H_j+\lambda},\qquad \text{scor}=-\tfrac12\sum_j\frac{G_j^2}{H_j+\lambda}+\gamma J $$ {#eq:leafopt}

unde $\ell_i$ este pierderea curentă a observației $i$, $g_i$ și $h_i$ derivatele de ordinul întîi și al doilea ale pierderii, $G_j$ și $H_j$ sumele lui $g_i$ și $h_i$ din frunza $j$, $J$ numărul de frunze, iar $\lambda$, $\gamma$ penalizările din @eq:boostobj.

În fiecare frunză, obiectivul @eq:leafobj este o parabolă în $w_j$; anulînd derivata, se obține $w_j^*$. Cîștigul unei împărțiri din @eq:gain este scorul dinainte minus scorul de după împărțire. Pentru eroarea absolută, $h_i=0$, iar XGBoost calculează atunci valorile frunzelor printr-o căutare unidimensională.

## Anexa C: valori SHAP exprimate în EUR/MWh {h=6ed90f88}

Arborii prognozează prețul transformat cu asinh, iar valorile SHAP se adună pe această scară. Pentru a raporta contribuțiile în euro, prognoza și prognoza medie sînt transformate înapoi,

$$ \hat P=m+s\,\sinh\Big(\phi_0+\textstyle\sum_j\phi_j\Big),\qquad P_0=m+s\,\sinh\phi_0 $$ {#eq:shap-back}

$$ \phi_j^{\text{EUR}}=\phi_j\,\frac{\hat P-P_0}{\sum_k\phi_k}\ \Rightarrow\ \sum_j\phi_j^{\text{EUR}}=\hat P-P_0 $$ {#eq:shap-eur}

unde $m$ și $s$ sînt mediana și abaterea absolută mediană (MAD), scalată, a prețurilor de antrenare, $\hat P$ prognoza în EUR/MWh, $P_0$ prognoza medie în EUR/MWh, iar $\phi_j^{\text{EUR}}$ contribuția variabilei $j$ în euro. Diferența în euro $\hat P-P_0$ se împarte proporțional cu $\phi_j$. Semnele și ordinea nu se schimbă, iar contribuțiile se adună exact la prognoza în EUR/MWh.

## Anexa D: spațiile de căutare și setările alese {h=9ad4ebef}

Pentru fiecare model au fost evaluate 24 de extrageri aleatoare (cu valoare inițială fixată) și setarea din cursul 2; setarea aleasă este cea cu MAE minimă în anul de validare.

| Setare DNN | Valori încercate | Aleasă |
|---|---|---|
| neuroni, stratul 1 | 64, 128, 256, 512 | 512 |
| neuroni, stratul 2 | 0, 32, 64, 128, 256 | niciunul |
| funcția de activare | ReLU, softplus | softplus |
| dropout | 0,0; 0,1; 0,2; 0,3 | 0,1 |
| rata de învățare | $3\cdot10^{-4}$; $10^{-3}$; $3\cdot10^{-3}$ | $3\cdot10^{-4}$ |
| penalizare L1, intrări | 0; $10^{-3}$; $10^{-2}$; $10^{-1}$ | 0 |
| grup (zile) | 32, 64, 128 | 64 |
| consum/RES/variabile fundamentale | da sau nu | da/da/da |

| Setare XGBoost | Valori încercate | Aleasă |
|---|---|---|
| arbori | 300, 600, 1000, 1500 | 1500 |
| rata de învățare $\eta$ | 0,02; 0,05; 0,10 | 0,02 |
| adîncimea | 3, 4, 5, 6, 8 | 8 |
| ponderea min. în frunză | 1, 5, 20, 50 | 5 |
| rînduri pe arbore | 0,6; 0,8; 1,0 | 0,8 |
| $\lambda$ | 0,1; 1,0; 10,0 | 0,1 |
| funcția de pierdere | pătrat, abs., Huber | absolută |
