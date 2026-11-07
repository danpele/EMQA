<!--
Versiunea web a Cursului 2 (RO). Construită în web/L2_ro.html de lectures/common/build_web_lecture.py (formatul: docstring-ul scriptului).
Hash-urile slide-urilor: python3 build_web_lecture.py 2 --frames
-->

## @intro

În fiecare zi, înainte de prînz, un furnizor, un producător sau operatorul unei baterii din România trebuie să decidă cîtă energie electrică cumpără sau vinde pentru fiecare oră a zilei următoare. Decizia se ia pe Piața pentru Ziua Următoare (PZU), administrată de operatorul pieței de energie electrică și de gaze naturale din România (OPCOM), iar prețul la care se decontează tranzacția se află abia după licitație. Cursul pornește de la o întrebare practică: cît de bine pot fi prognozate prețurile orare de mîine cu informația disponibilă la ora 12:00 a Europei Centrale (CET) în ziua dinaintea livrării și de unde știm că o prognoză este cu adevărat mai bună decît alta?

Răspunsul se construiește pas cu pas, pe date reale: prețurile orare PZU din România, împreună cu consumul, producția eoliană, solară, hidro și nucleară și fluxurile transfrontaliere, între 1 ianuarie 2022 și 31 octombrie 2026, ultimele 365 de zile fiind păstrate ca an de test. Pornim de la o regulă naivă, pe care orice trader o poate aplica, măsurăm erorile în EUR/MWh și testăm statistic diferențele dintre modele. Construim apoi modele de regresie expert, le restrîngem cu o penalizare care alege automat regresorii, mediem prognozele pe mai multe ferestre de calibrare și pe mai multe modele, facem o introducere în învățarea automată și transformăm prognozele punctuale în intervale. Cursul se încheie cu testele de cointegrare anunțate în cursul 1 și cu patru studii de caz care traduc acuratețea prognozei în bani.

Disciplina contează la fel de mult ca modelele. O testare retrospectivă care folosește informații încă indisponibile la momentul licitației pare excelentă, dar nu poate fi rulată într-un birou de tranzacționare real. Toate cifrele din acest curs provin din prognoze care respectă regula orei 12:00, iar cursul arată cum se verifică acest lucru.

@goals
- **Construiți** o prognoză pentru PZU care folosește numai datele disponibile la ora 12:00 CET în ziua dinaintea livrării.
- **Măsurați** acuratețea prin eroarea absolută medie (MAE), rădăcina erorii pătratice medii (RMSE) și MAE relativă (rMAE) și testați diferențele dintre modele cu testul Diebold–Mariano (DM).
- **Estimați** modele autoregresive cu variabile exogene (ARX), restrîngeți-le cu operatorul de contracție și selecție în normă absolută (LASSO) și obțineți autoregresia estimată cu LASSO (LEAR).
- **Combinați** prognozele, inclusiv modele de învățare automată (ML), și obțineți cuantile ale prețului prin medierea prin regresie cuantilică (QRA).
- **Testați** cointegrarea prețurilor din România și Ungaria și a prețului energiei electrice cu prețul gazelor și producția hidro, anunțată în cursul 1.

# Problema de prognoză și modelele de referință

Înainte de a estima orice model, problema de prognoză trebuie definită exact: ce prețuri prognozăm, în ce moment, cu ce informații și față de ce reper judecăm rezultatul. Secțiunea fixează calendarul licitației PZU, împărțirea datelor în calibrare, rodaj și test, modelul naiv de referință, măsurile erorii și testul statistic folosit pentru compararea modelelor.

## Prognozăm prețul orar PZU din România, numai cu date reale {h=05e1aa4b}

Variabila prognozată este prețul orar PZU al zonei de ofertare România (RO), publicat de OPCOM și descărcat prin energy-charts.info, portalul de date al Institutului Fraunhofer pentru Sisteme de Energie Solară (ISE), care îl preia de la Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E). Variabilele explicative sînt consumul, producția eoliană, solară, hidro și nucleară și fluxurile transfrontaliere, orare și zilnice, de la ENTSO-E (date Transelectrica pentru România); prețul certificatului de emisii (EUA) al Uniunii Europene (UE), aproximat prin titlul SparkChange tranzacționat la bursă și garantat fizic cu certificate EUA (ETC), din Yahoo Finance; prețurile piețelor vecine, Ungaria (HU), de la bursa de energie din Ungaria (HUPX), și zona de ofertare Germania–Luxemburg (DE-LU), de la bursa europeană de energie EPEX SPOT (EPEX); în fine, prețul lunar al gazelor la hubul olandez Title Transfer Facility (TTF), din Pink Sheet al Băncii Mondiale.

Datele se opresc la 31 octombrie 2026 și au fost descărcate la 4 noiembrie 2026. Perioada analizată este 1 ianuarie 2022 – 31 octombrie 2026, cu 1 765 de zile complete. Perioada de test cuprinde ultimele 365 de zile, 1 noiembrie 2025 – 31 octombrie 2026; cele 182 de zile dinaintea ei formează rodajul (*burn-in*), folosit numai pentru calibrarea intervalelor de prognoză. Ora de vară (DST) se tratează ca în tema 1: fiecare zi are 24 de ore, ora lipsă din martie și ora dublată din octombrie se înlocuiesc cu medii. Cele 2 zile cu schimbarea orei din anul de test rămîn în analiză.

## PZU: licitația din ziua d-1 fixează prețurile zilei d {h=5eee2f51}

PZU este licitația zilnică a cuplării unice a piețelor pentru ziua următoare (SDAC), mecanismul care leagă piețele europene pentru ziua următoare; în România o organizează OPCOM. În ziua licitației, $d-1$, cumpărătorii și vînzătorii depun oferte, adică perechi cantitate–preț, pentru fiecare interval de livrare al zilei următoare, $d$. La ora 12:00 CET se închide registrul de oferte. Un algoritm comun, Pan-European Hybrid Electricity Market Integration Algorithm (EUPHEMIA), echilibrează apoi cererea și oferta în toate zonele cuplate, în limita capacităților transfrontaliere, iar rezultatele se publică de regulă în jurul orei 13:00 CET (NEMO Committee, 2025, 2026).

Din ziua de livrare 1 octombrie 2025, licitația stabilește 96 de prețuri pe sfert de oră în loc de 24 de prețuri orare. În datele noastre, prețul orar este media celor patru sferturi de oră, iar această definiție se aplică pe tot anul de test, astfel încît seria orară rămîne comparabilă înainte și după schimbare. Studiul de caz (c) de la finalul cursului revine la sferturile de oră.

Calendarul contează pentru că stabilește ce poate ști prognozistul. Prognoza pentru ziua $d$ trebuie să fie gata înainte de închiderea licitației, la prînz în ziua $d-1$, iar ziua $d$ începe abia după douăsprezece ore și se încheie la 36 de ore după licitație.

## Notația și regula pe care o respectă toate prognozele {h=d9b0d031}

Cursul folosește o notație fixă. Ziua livrării este $d$; $d-1$ este ziua dinainte, în care are loc licitația; $d-2$ este cu două zile înainte. Ora livrării este $h=0,\dots,23$ (CET), $P_{d,h}$ este prețul PZU al orei $h$ din ziua $d$, în EUR/MWh (euro pe megawatt-oră), iar $\hat P_{d,h}$ este prognoza acestui preț.

Regula pe care o respectă toate prognozele din curs este simplă: prognoza pentru ziua $d$ se face înainte de ora 12:00 CET din ziua $d-1$, deci poate folosi numai ce se cunoaște în acel moment. Sînt permise toate cele 24 de prețuri ale zilei $d-1$, stabilite prin licitația din ziua $d-2$. Ar fi permise și prognozele de consum și de producție eoliană și solară pentru ziua $d$, publicate de operatorul de transport și de sistem (TSO) înainte de prînz. Este interzisă orice valoare realizată în ziua $d$, precum și valorile zilei $d-1$ care nu sînt încă măsurate.

Obiectul exercițiului sînt, așadar, cele 24 de prețuri orare PZU din România pentru fiecare zi a anului de test. Eroarea $P_{d,h}-\hat P_{d,h}$ se cunoaște abia după livrarea din ziua $d$, deci evaluarea se face întotdeauna în afara eșantionului de estimare (Lago et al., 2021).

@practice aceeași regulă se aplică oricărui birou de tranzacționare: un model care o încalcă nu poate fi rulat la 12:00.

## Prognoza zilei d folosește doar datele cunoscute la 12:00 CET în ziua d-1 {h=12fe9510}

Slide-ul desenează pe o axă a timpului informația disponibilă. Prețurile zilei $d-1$ au fost publicate în jurul orei 13:00 din ziua $d-2$. Ultima zi măsurată complet este $d-2$, care se încheie la miezul nopții dinaintea zilei licitației. La 12:00 în ziua $d-1$ se trimit ofertele pentru ziua $d$, iar de prognozat sînt cele 24 de prețuri orare (96 pe sfert de oră) ale zilei $d$.

Modelele din acest curs folosesc deci prețurile pînă în ziua $d-1$; consumul, producția și fluxurile realizate pînă în ziua $d-2$; prețul carbonului la închiderea din $d-2$. Ce nu avem în datele noastre gratuite sînt prognozele TSO de consum și de producție regenerabilă pentru ziua $d$, pe care un birou real le-ar folosi. Este un dezavantaj al modelelor noastre, nu o greșeală: aceste prognoze sînt permise, dar nu le avem. Slide-urile următoare arată că tocmai aici se află cea mai mare parte a îmbunătățirii posibile.

@practice o testare retrospectivă cu consumul realizat în ziua $d-1$ pare excelentă, dar la 12:00 acest consum nu se cunoaște.

## Datele se împart cronologic în calibrare, rodaj și test, fără amestecare {h=fb64bc12}

Un model de prognoză a prețurilor trebuie evaluat în aceeași ordine în care ar fi folosit. Fiecare model se reestimează zilnic pe o fereastră care se încheie în ziua $d-1$, produce cele 24 de prognoze pentru ziua $d$, apoi fereastra avansează cu o zi. Nu folosim validare încrucișată aleatoare (K-fold) și nici o împărțire aleatoare pentru validare, deoarece amestecarea zilelor ar lăsa modelul să învețe din viitor, iar testarea retrospectivă ar părea mai bună decît realitatea (Weron, 2014; Lago, Marcjasz, De Schutter & Weron, 2021).

Graficul arată cum se folosește eșantionul. Prima prognoză se face cu o fereastră de calibrare de 728 de zile; următoarele 182 de zile formează rodajul, ale cărui prognoze servesc numai la calibrarea intervalelor; ultimele 365 de zile formează anul de test, pe care se măsoară toate erorile din acest curs. Calibrare înseamnă estimarea modelului, rodaj înseamnă prognoze folosite doar pentru intervale, iar test înseamnă măsurarea erorii. Anul de test este folosit o singură dată, la final.

@practice cereți furnizorului de prognoze o testare retrospectivă (*backtest*) cu fereastră glisantă, nu ajustarea pe datele de estimare.

@chart split_timeline
Prețul zilnic de bază din România, 1 ianuarie 2022 – 31 octombrie 2026, în EUR/MWh, cu prima fereastră de calibrare de 728 de zile, rodajul de 182 de zile și perioada de test de 365 de zile marcate prin fundal colorat.

## Prețul mai vechi dă erori mai mari, cu excepția celui de acum o săptămînă {h=7f4714a5}

Cea mai simplă prognoză copiază prețul aceleiași ore de acum $k$ zile, $\hat P_{d,h}=P_{d-k,h}$. Graficul arată MAE a acestei prognoze în anul de test, în funcție de vechimea $k$ a informației. Cu prețul de ieri, $k=1$, MAE este 29,37 EUR/MWh. Cu prețul de acum două zile urcă la 38,52, pentru că informația este mai veche. La $k=7$, însă, eroarea coboară la 34,41, deoarece aceeași zi a săptămînii trecute are același tipar săptămînal al consumului.

Rezultă două concluzii. Informația cea mai recentă este cea mai valoroasă, deci orice model corect se va sprijini puternic pe prețurile zilei $d-1$. Iar ciclul săptămînal este suficient de puternic încît, în unele zile, un preț vechi de o săptămînă să fie mai bun decît unul mai recent; de aici pornește modelul naiv definit două slide-uri mai departe.

@practice prognoza de la 12:00 din ziua $d-1$ privește următoarele 12–36 de ore, iar cel mai recent preț cunoscut este cel al zilei $d-1$.

@chart horizon_naive
MAE a prognozei care copiază prețul aceleiași ore de acum $k$ zile, pentru $k$ de la una la 14 zile, în anul de test; barele pentru $k$ = 7 și 14 (aceeași zi a săptămînii) sînt evidențiate.

## Prognozele punctuale, probabilistice și de traiectorie răspund la întrebări diferite {h=38cd1ad6}

O prognoză poate avea trei forme. Prognoza punctuală dă un preț pentru fiecare oră; cea probabilistică dă distribuția prețului, de exemplu printr-un set de cuantile; cea de traiectorie dă scenarii comune pentru toate cele 24 de ore:

$$ \underbrace{\hat P_{d,h}}_{\text{punctuală}}\qquad\underbrace{\hat q^{\tau}_{d,h}:\ \Pr(P_{d,h}\le \hat q^{\tau}_{d,h})=\tau}_{\text{cuantilă}}\qquad \underbrace{\{\hat P^{(s)}_{d,0},\dots,\hat P^{(s)}_{d,23}\}_{s=1}^{S}}_{\text{traiectorii}} $$ {#eq:types}

unde $d$ este ziua livrării, $h$ ora (CET), $\hat q^{\tau}_{d,h}$ cuantila de nivel $\tau\in(0,1)$, $s$ indicele scenariului, iar $S$ numărul de scenarii.

Diferența contează pentru că erorile orelor nu sînt independente. Pe datele din România, corelația erorilor de prognoză între orele 12 și 13 este 0,96, iar între orele 3 și 19 doar 0,13. Un set de 24 de cuantile separate nu poate descrie această dependență; traiectoriile pot. Fiecare utilizator are nevoie de altceva (Nowotarski & Weron, 2018): furnizorul care cumpără un bloc de ore folosește prognoza punctuală, managerul de risc folosește cuantilele (cursul 4), iar operatorul unei baterii are nevoie de traiectorii, deoarece cumpără energie într-o oră și o vinde în alta, deci contează evoluția comună a celor două prețuri.

@practice înainte de a cumpăra o prognoză, stabiliți de care dintre cele trei tipuri are nevoie decizia dumneavoastră.

## Modelul naiv: prețul de ieri sau, lunea și în weekend, prețul de acum 7 zile {h=ff93a3a8}

Orice model trebuie să fie mai precis decît regula simplă pe care un trader ar aplica-o fără niciun model. Modelul naiv standard din literatură (Nogales et al., 2002; Weron, 2014) ia prețul de ieri în zilele lucrătoare de la mijlocul săptămînii și prețul de acum o săptămînă în zilele al căror tipar diferă de cel al zilei precedente:

$$ \hat P^{\text{naive}}_{d,h}=\begin{cases}P_{d-7,h}, & \text{lun., sîm., dum.}\\ P_{d-1,h}, & \text{mar.–vin.}\end{cases} $$ {#eq:naive}

$$ \hat P^{(7)}_{d,h}=P_{d-7,h} $$ {#eq:snaive}

unde $P_{d,h}$ este prețul zilei $d$, ora $h$ (EUR/MWh), iar $\hat P^{(7)}$ din @eq:snaive este modelul naiv sezonier: aceeași oră, cu o săptămînă în urmă.

Datele justifică schimbarea regulii. Lunea, sîmbăta și duminica, prețul din $d-7$ dă o MAE de 29,87 EUR/MWh, iar prețul din $d-1$ dă 33,48, pentru că lunea urmează unui weekend, iar weekendul urmează unei zile lucrătoare. De marți pînă vineri ordinea se inversează: 26,27 pentru $d-1$ și 37,83 pentru $d-7$. Pe întregul an de test, modelul naiv are MAE 27,82 EUR/MWh, iar cel naiv sezonier 34,41. La un preț mediu de 134,46 EUR/MWh, eroarea naivă reprezintă circa o cincime din preț.

@practice cereți oricărui furnizor de prognoze rMAE față de această regulă naivă, calculată pe orele care vă interesează.

## Patru măsuri ale erorii și rMAE, care compară modelul cu cel naiv {h=4be13c74}

Erorile de prognoză pot fi rezumate în mai multe feluri, iar fiecare măsură răspunde la o întrebare puțin diferită (Hyndman & Koehler, 2006). Cu $e_{d,h}=P_{d,h}-\hat P_{d,h}$:

$$ \text{MAE}=\tfrac1N\textstyle\sum|e_{d,h}|,\qquad \text{RMSE}=\sqrt{\tfrac1N\textstyle\sum e_{d,h}^2} $$ {#eq:mae}

$$ \text{sMAPE}=\tfrac1N\textstyle\sum\frac{2|e_{d,h}|}{|P_{d,h}|+|\hat P_{d,h}|},\qquad \text{rMAE}=\frac{\text{MAE}_{\text{model}}}{\text{MAE}_{\text{naive}}} $$ {#eq:smape}

unde $N$ este numărul perechilor (zi, oră), iar sumele se fac pe toate aceste perechi. Eroarea procentuală absolută medie simetrică (sMAPE) ia valori între 0 și 200%. rMAE împarte MAE a modelului la MAE a modelului naiv @eq:naive, calculate pe aceleași ore; o valoare sub 1 înseamnă că modelul este mai precis decît cel naiv.

MAE se exprimă în EUR/MWh și se explică ușor; RMSE ridică erorile la pătrat și penalizează deci mai puternic salturile de preț. MAE este minimă pentru prognoza mediană, RMSE pentru cea medie. În anul de test, modelul naiv are MAE 27,82, RMSE 44,54 și sMAPE 34,5%. LEAR mediat pe ferestre de calibrare (AW-LEAR), prezentat mai departe, obține MAE 22,53, RMSE 36,35 și rMAE 0,810. Cel mai bun model din curs, ansamblul de 4 modele, are rMAE 0,795, adică o eroare cu 20,5% mai mică decît a modelului naiv.

@practice raportați biroului de tranzacționare MAE în EUR/MWh, iar conducerii rMAE, calculate pe aceleași ore.

## Erorile procentuale nu funcționează la prețuri apropiate de zero sau negative {h=50559ac1}

Eroarea procentuală absolută medie (MAPE) este populară în rapoartele de afaceri, dar nu funcționează pentru prețurile energiei electrice:

$$ \text{MAPE}=\tfrac1N\textstyle\sum|e_{d,h}|/|P_{d,h}| $$ {#eq:mape}

cu $e_{d,h}$, $P_{d,h}$ și $N$ definite ca în @eq:mae. Problema este numitorul. Cînd prețul este aproape de zero, cum se întîmplă în orele însorite cu multă producție solară, chiar și o eroare mică în EUR/MWh devine un procent uriaș, iar cînd prețul este negativ măsura nu mai are niciun sens.

În anul de test, MAPE pentru AW-LEAR este 5 777,7%. Fără cele 387 de ore în care prețul are valoarea absolută sub 5 EUR/MWh, ea scade la 32,4%. Aceste puține ore generează 99,5% din valoarea MAPE. Graficul arată, pentru fiecare oră a anului de test, eroarea procentuală absolută în funcție de prețul realizat: erorile explodează în banda îngustă din jurul lui zero, iar în rest rămîn moderate. Aceeași prognoză poate părea, deci, rezonabilă sau catastrofală numai în funcție de măsura aleasă (Hyndman & Koehler, 2006; Weron, 2014).

@practice nu acceptați MAPE pentru prețurile energiei electrice; cereți MAE și rMAE.

@chart mape_fail
Eroarea procentuală absolută a prognozei AW-LEAR în funcție de prețul realizat, pentru fiecare dintre cele 8 760 de ore ale anului de test, cu banda $|P|<5$ EUR/MWh evidențiată și linia erorii de 100% marcată.

## Testul Diebold–Mariano arată dacă un model este cu adevărat mai precis decît altul {h=9f22d35e}

O MAE mai mică pe un singur an de test se poate datora întîmplării. Testul Diebold–Mariano (Diebold & Mariano, 1995) verifică dacă diferența medie dintre erorile a două modele este mare față de propria ei variabilitate. Urmînd Ziel & Weron (2018), cele 24 de erori orare se mediază mai întîi în cadrul fiecărei zile, ceea ce elimină corelația puternică dintre orele aceleiași zile (varianta multivariată a testului):

$$ \Delta_d=\underbrace{\tfrac1{24}\textstyle\sum_h|e^{A}_{d,h}|}_{\text{modelul A}}-\underbrace{\tfrac1{24}\textstyle\sum_h|e^{B}_{d,h}|}_{\text{modelul B}},\qquad \text{DM}=\frac{\bar\Delta}{\sqrt{\hat\sigma^2_{\Delta}/n}} $$ {#eq:dm}

unde $e^{A}_{d,h}$ și $e^{B}_{d,h}$ sînt erorile modelelor A și B, $\Delta_d$ diferența dintre erorile lor absolute medii din ziua $d$, $\bar\Delta$ media acestei diferențe pe cele $n$ zile de test, $\hat\sigma^2_{\Delta}$ varianța ei Newey–West cu 7 decalaje, iar valoarea $p$ unilaterală este $p=1-\Phi(\text{DM})$, cu $\Phi$ funcția de repartiție normală standard. O valoare $p$ sub 0,05 înseamnă că B este semnificativ mai precis decît A.

Pe cele 365 de zile de test, modelul naiv față de AW-LEAR dă DM = 7,32, cu $p<0{,}001$: LEAR este clar mai precis. ARX mediat pe ferestre (AW-ARX) față de AW-LEAR dă DM = −0,83 și $p$ = 0,797, deci diferența nu este semnificativă statistic. AW-LEAR față de ansamblul de 4 modele dă DM = 2,21 și $p$ = 0,014: ansamblul este semnificativ mai precis.

@practice schimbați modelul numai dacă îmbunătățirea este semnificativă pe orele care vă interesează.

## Matricea testelor DM: care modele sînt semnificativ mai precise în România {h=da2dce64}

Aplicînd testul DM din @eq:dm fiecărei perechi de modele, obținem o matrice de valori $p$. Fiecare celulă răspunde la întrebarea „este modelul din coloană mai precis decît cel din rînd?”, iar o celulă verde înseamnă că modelul din coloană este semnificativ mai precis. Diagonala rămîne goală.

În anul de test din România, 8 dintre celelalte 9 modele sînt semnificativ mai precise decît modelul naiv, la pragul de 5%; excepția este modelul naiv sezonier, care este mai slab. Coloanele cu multe celule verzi aparțin modelelor care le depășesc pe cele mai multe dintre celelalte. Matricea permite o comparație rapidă a modelelor, fără a supraevalua diferențe mici de MAE care nu sînt semnificative statistic (Ziel & Weron, 2018; Lago et al., 2021).

@practice citiți fiecare coloană de sus în jos: multe celule verzi indică un model pentru care merită să plătiți.

@chart dm_matrix
Valorile $p$ unilaterale ale testului DM pentru fiecare pereche de modele, pe cele 365 de zile de test, plafonate la 0,10; celulele verzi arată că modelul din coloană este semnificativ mai precis decît cel din rînd.

## @end

O prognoză pentru PZU trebuie să folosească numai informația cunoscută la ora 12:00 CET în ziua $d-1$, să fie evaluată pe un an de test cu fereastră glisantă și comparată cu modelul naiv, în EUR/MWh și prin rMAE, iar testul DM separă cîștigurile reale de întîmplare.

# Modele expert: ARX și LEAR

Modelele expert sînt regresii liniare ale căror variabile sînt cele urmărite mai întîi de un trader: prețurile recente, calendarul și variabilele fundamentale ale cererii și ofertei. Secțiunea construiește modelul ARX, arată cum variază coeficienții de la o oră la alta, transformă prețurile pentru a atenua salturile și lasă apoi LASSO să aleagă automat regresorii în modelul LEAR.

## Modelul expert ARX: prețuri recente, calendar și variabile fundamentale {h=9324a1b3}

Modelul ARX este cîte o regresie liniară pentru fiecare oră, cu variabilele urmărite de un trader (Ziel & Weron, 2018; Weron, 2014):

$$ Y_{d,h}=\beta_0+\underbrace{\beta_1Y_{d-1,h}+\beta_2Y_{d-2,h}+\beta_3Y_{d-7,h}}_{\text{autoregresie}}+\underbrace{\beta_4Y_{d-1,23}+\beta_5Y^{\min}_{d-1}+\beta_6Y^{\max}_{d-1}}_{\text{forma zilei precedente}}+\underbrace{\beta_7\tilde L_{d,h}+\beta_8\tilde R_{d,h}}_{\text{fundamentale din } d-2}+\underbrace{\textstyle\sum_{j}\delta_jD^{j}_d}_{\text{lun., sîm., dum.}}+\varepsilon_{d,h} $$ {#eq:arx}

unde $Y_{d,h}$ este prețul orei $h$ din ziua $d$, transformat asinh (transformarea este definită mai jos); $Y_{d-1,h}$, $Y_{d-2,h}$ și $Y_{d-7,h}$ sînt prețurile aceleiași ore cu una, două și șapte zile în urmă; $Y_{d-1,23}$ este ultima oră a zilei precedente, iar $Y^{\min}_{d-1}$ și $Y^{\max}_{d-1}$ minimul și maximul acelei zile; $\tilde L_{d,h}=L_{d-2,h}$ este consumul, iar $\tilde R_{d,h}$ producția eoliană și solară din aceeași oră a zilei $d-2$, ambele standardizate; $D^{j}_d$ sînt variabile indicator pentru luni, sîmbătă și duminică, cu coeficienții $\delta_j$; $\beta_0,\dots,\beta_8$ sînt coeficienți, iar $\varepsilon_{d,h}$ este eroarea.

Modelul se estimează prin metoda celor mai mici pătrate (OLS), separat pentru fiecare dintre cele 24 de ore, cu 12 regresori pentru fiecare oră, ca în tema 1. Pe datele din România, varianta ARX(728), estimată pe ultimele 728 de zile și reestimată zilnic, are MAE 22,72 EUR/MWh și rMAE 0,817, adică este deja cu aproape o cincime mai precisă decît modelul naiv.

@practice acesta este modelul de depășit înainte să cumpărați o rețea neuronală.

## Coeficienții modelului ARX diferă de la o oră la alta {h=217e83e4}

Pentru că fiecare oră are propria regresie, coeficienții din @eq:arx pot diferi pe parcursul zilei. Graficul arată media fiecărui coeficient pe cele 365 de estimări zilnice din anul de test, oră cu oră. Ponderea prețului aceleiași ore de ieri, $Y_{d-1,h}$, este maximă la ora 13 (0,68) și minimă la ora 0 (0,08). Noaptea contează mai mult ultima oră a zilei $d-1$, al cărei coeficient ajunge pînă la 0,73: imediat după miezul nopții, prețul cel mai apropiat în timp este cel din seara precedentă, nu cel al aceleiași ore de acum 24 de ore.

Coeficienții consumului și ai producției eoliene și solare rămîn apropiați de zero la toate orele. Observate în ziua $d-2$, aceste variabile fundamentale adaugă puțin la ce conține deja prețul de ieri. Profilul orar al coeficienților este motivul pentru care se folosește cîte un model pentru fiecare oră, nu o singură ecuație.

@practice cîte un model pe oră permite ca vîrful de seară să depindă de alți factori decît noaptea.

@chart arx_coef
Coeficienții medii ai modelului ARX(728), pe ore (CET), pe cele 365 de estimări zilnice din anul de test, pentru prețurile din $d-1$, $d-2$ și $d-7$, consum și producția eoliană și solară.

## Variabilele fundamentale din ziua d-2 aproape că nu îmbunătățesc prognoza {h=46d1e3f9}

Tabelul compară trei variante ale modelului ARX(728) în anul de test. Numai cu prețuri și calendar, MAE este 22,63 EUR/MWh. Adăugînd consumul și producția eoliană și solară din $d-2$, MAE devine 22,72, iar adăugînd și producția hidro, cea nucleară, importul net și EUA din $d-2$, MAE rămîne 22,72. Variabilele fundamentale nu îmbunătățesc prognoza.

| ARX(728), anul de test | MAE | RMSE | rMAE |
|---|---|---|---|
| numai prețuri și calendar | 22,63 | 36,49 | 0,813 |
| + consum, producție eoliană și solară din d-2 | 22,72 | 36,62 | 0,817 |
| + hidro, nuclear, import net, EUA din d-2 | 22,72 | 36,50 | 0,817 |

Valorile lipsă ale variabilelor fundamentale se înlocuiesc cu ultima valoare observată (pentru nuclear, în 29 de zile). EUA este prețul de închidere al titlului SparkChange din ziua $d-2$, folosit ca aproximare a prețului certificatului de emisii.

Explicația ține de calendar. Informația din ziua $d-2$ este deja inclusă în prețul zilei $d-1$, pe care modelul îl folosește oricum; de exemplu, opririle centralei nucleare de la Cernavodă intră în model cu două zile întîrziere. Ar ajuta prognozele publicate de consum și de producție eoliană și solară chiar pentru ziua $d$ (ENTSO-E, Transelectrica). Ele apar înainte de 12:00 în ziua $d-1$, deci pot fi folosite, dar nu fac parte din datele noastre gratuite (Lago et al., 2021).

@practice cumpărați prognozele TSO de consum și de producție regenerabilă pentru ziua următoare înainte de a plăti pentru un model mai complex.

## Cîte un model pentru fiecare oră este mai precis decît un model comun {h=224d9f21}

O alternativă la cele 24 de regresii orare este o singură regresie comună pentru toate orele, cu constantă proprie fiecărei ore, dar cu pante comune. Modelul comun este mai simplu și folosește de 24 de ori mai multe observații pentru fiecare coeficient, dar obligă toate orele să reacționeze la fel la prețul de ieri și la variabilele fundamentale.

În anul de test, ARX(728) cu cîte un model pe oră are MAE 22,72 EUR/MWh, iar varianta cu model comun ajunge la 24,54. Graficul arată MAE pe ore pentru ambele variante și pentru modelul naiv: modelul comun este mai slab în 21 din 24 de ore. Cîștigul obținut cu modele orare separate se potrivește cu profilurile diferite ale coeficienților de pe slide-ul anterior (Ziel & Weron, 2018).

@practice din 1 octombrie 2025 se tranzacționează sferturi de oră, deci aceeași alegere apare pentru cele 96 de intervale ale zilei.

@chart per_hour_single
MAE pe ore (CET) în anul de test pentru modelul naiv, ARX(728) cu un singur model pentru toate orele și ARX(728) cu cîte un model pe oră.

## Transformarea asinh atenuează salturile și acceptă prețuri negative {h=03928cf3}

Prețurile energiei electrice au salturi și pot fi negative, astfel încît o regresie pe prețuri netransformate este dominată de cîteva ore extreme. O transformare de stabilizare a varianței (VST) comprimă valorile extreme înainte de estimare (Uniejewski, Weron & Ziel, 2018). Cursul folosește inversa sinusului hiperbolic:

$$ Y=\asinh\!\left(\frac{P-m}{s}\right) $$ {#eq:vst}

unde $P$ este prețul, $m$ mediana sa, iar $s$ = 1,4826 × abaterea absolută mediană (MAD), ambele calculate numai pe fereastra de calibrare, astfel încît în transformare nu intră informații din viitor. Prognozele se fac pe scara lui $Y$ și se readuc la prețuri cu sinusul hiperbolic.

Panoul din stînga al graficului arată transformarea: în apropierea medianei este aproape liniară, departe de ea crește doar logaritmic și, spre deosebire de logaritm, este definită și pentru prețuri negative. Panoul din dreapta compară MAE lunară a modelului ARX(728) cu și fără transformare. Pe tot anul de test, MAE este 22,86 pe prețuri netransformate și 22,72 cu asinh. Pentru RMSE ordinea se inversează (35,85 față de 36,62), pentru că transformarea dă o pondere mai mică salturilor în estimare.

@practice funcția asinh este definită și pentru valori negative, unde logaritmul nu poate fi folosit.

@chart vst
Stînga: transformarea asinh și o simplă standardizare, în funcție de preț, cu mediana și scala din ultima fereastră; dreapta: MAE lunară a modelului ARX(728) pe prețuri netransformate și pe prețuri transformate asinh, în anul de test.

## LEAR pornește de la 247 de regresori, iar LASSO îi elimină pe cei mai mulți {h=f43bbd84}

În loc ca regresorii să fie aleși pe baza judecății expertului, modelul LEAR pornește de la mulți candidați și lasă o penalizare să-i aleagă (Tibshirani, 1996; Uniejewski, Nowotarski & Weron, 2016; Lago et al., 2021). Pentru fiecare oră $h$:

$$ \hat{\boldsymbol\beta}_h=\arg\min_{\boldsymbol\beta}\Big\{\underbrace{\textstyle\sum_{d\in\text{cal}}(Y_{d,h}-\mathbf x_d^{\top}\boldsymbol\beta)^2}_{\text{ajustare}}+\underbrace{\lambda_h\textstyle\sum_j|\beta_j|}_{\text{penalizare}}\Big\} $$ {#eq:lasso}

unde suma se face pe zilele ferestrei de calibrare, $Y_{d,h}$ este prețul transformat, $\mathbf x_d$ vectorul celor 247 de regresori (cele 24 de prețuri din $d-1$, $d-2$, $d-3$ și $d-7$, adică 96; consumul și producția eoliană și solară din $d-2$, $d-3$ și $d-7$, adică 144; 7 indicatori ai zilei săptămînii), $\boldsymbol\beta$ vectorul coeficienților $\beta_j$, iar $\lambda_h\ge0$ intensitatea penalizării, aleasă zilnic prin criteriul informațional Akaike (AIC) în interiorul ferestrei. Penalizarea în valoare absolută face exact zero coeficienții inutili, deci datele aleg regresorii.

Pe datele din România, LEAR(728) păstrează în medie 42 din cei 247 de regresori (17%), între 8 și 121, în funcție de oră și de zi. MAE este 22,62 EUR/MWh; media prognozelor estimate pe ferestre de 364, 546 și 728 de zile (AW-LEAR) dă 22,53. Penalizarea trebuie aleasă corect: printr-un criteriu informațional sau pe un bloc de validare care se încheie înaintea zilei prognozate, niciodată pe anul de test.

@practice un model LASSO este ușor de interpretat: regresorii păstrați arată ce influențează prețul în fiecare oră.

## LEAR păstrează prețul aceleiași ore de ieri și ziua săptămînii {h=b12325f3}

Deoarece LASSO face exact zero o parte din coeficienți, putem număra cît de des rămîne în model fiecare grupă de regresori. Harta termică arată, pentru fiecare oră a zilei și fiecare grupă de regresori candidați, procentul păstrat de LEAR(728) în cele 365 de estimări zilnice din anul de test.

În medie, prețul aceleiași ore de ieri, $P_{d-1,h}$, rămîne în 79% din estimări, iar indicatorii zilei săptămînii în 64%. În schimb, din regresorii de consum se păstrează doar 9%, iar din cei de producție eoliană și solară 11%. LASSO confirmă rezultatul experimentului cu ARX: variabilele fundamentale observate cu două zile înainte de livrare aduc puțină informație care nu se află deja în prețul zilei $d-1$.

@practice pentru cîștiguri reale aveți nevoie de prognoze ale variabilelor fundamentale pentru ziua $d$.

@chart lear_sel
Procentul regresorilor păstrați de LEAR(728), pe grupe de regresori (rînduri) și pe ore ale zilei (coloane), în cele 365 de estimări zilnice din anul de test.

## @end

Modelul expert ARX, cu cîte o regresie pentru fiecare oră, reduce deja eroarea modelului naiv cu aproape o cincime; transformarea asinh tratează salturile și prețurile negative; LASSO păstrează un set mic de regresori, mai ales prețurile recente și ziua săptămînii, în timp ce variabilele fundamentale din $d-2$ aproape că nu contează.

# Ferestre, combinații și învățare automată

Niciun model și nicio fereastră de calibrare nu sînt cele mai bune în orice moment. Secțiunea mediază prognozele pe mai multe ferestre de calibrare și pe mai multe modele, prezintă clasamentul modelelor pe anul de test din România și face o introducere la două modele de învățare automată, gradient boosting și o rețea neuronală, dezvoltate în cursul 7.

## Ferestrele scurte se adaptează, cele lungi sînt stabile: mediați prognozele {h=c16d1f7c}

Lungimea ferestrei de calibrare este o alegere dificilă. O fereastră scurtă se adaptează repede cînd piața se schimbă; una lungă dă estimări mai stabile. În loc să ghiciți lungimea optimă, puteți estima modelul pe mai multe ferestre și face media prognozelor (Hubicka, Marcjasz & Weron, 2019; Marcjasz, Serafin & Weron, 2018):

$$ \hat P^{\text{AW}}_{d,h}=\frac1{|\mathcal T|}\sum_{T\in\mathcal T}\hat P^{(T)}_{d,h} $$ {#eq:aw}

unde $\hat P^{(T)}_{d,h}$ este prognoza modelului estimat pe ultimele $T$ zile (fereastră glisantă, reestimată zilnic), $\mathcal T$ este mulțimea lungimilor de fereastră, iar $|\mathcal T|$ numărul lor. Pentru ARX, $\mathcal T=\{56,84,112,714,721,728\}$; pentru LEAR, $\mathcal T=\{364,546,728\}$. Aceasta este medierea pe ferestre de calibrare (AW).

Pe datele din România, MAE a modelului ARX este 24,44 EUR/MWh cu o fereastră de 56 de zile, 23,41 cu 112 zile și 22,72 cu 728 de zile. Media, AW-ARX, ajunge la 22,30, mai precisă decît modelul estimat pe oricare fereastră. Pentru LEAR, valorile sînt 22,96 pentru LEAR(364), 22,62 pentru LEAR(728) și 22,53 pentru AW-LEAR. Combinarea ferestrelor scurte (56–112 zile) cu cele lungi (714–728 de zile) aduce atît adaptare, cît și stabilitate.

@practice cînd piața își schimbă regimul (2022, 2024), ferestrele scurte reacționează primele; păstrați-le în medie.

## Media pe ferestre este mai precisă decît cea mai bună fereastră {h=15321caf}

Graficul arată MAE pentru fiecare fereastră de calibrare, pentru ARX și LEAR, cu prognoza mediată ca ultimă bară în fiecare panou și modelul naiv, 27,82 EUR/MWh, ca linie punctată. Pentru ARX, prognoza mediată AW-ARX are MAE 22,30 EUR/MWh, sub cea mai bună fereastră individuală, ARX(714), cu 22,68.

Rezultatul este util tocmai pentru că fereastra cea mai bună nu se cunoaște dinainte: în alt an ar putea cîștiga o fereastră scurtă. Medierea elimină nevoia de a alege și dă totuși un rezultat cel puțin la fel de bun ca alegerea cea mai bună făcută retrospectiv (Hubicka, Marcjasz & Weron, 2019).

@practice nu trebuie să știți dinainte care fereastră este potrivită: faceți media prognozelor obținute pe o fereastră scurtă și pe una lungă.

@chart windows
MAE în anul de test pentru ARX (stînga) și LEAR (dreapta), în funcție de fereastra de calibrare $T$ în zile, cu prognoza mediată pe ferestre (AW) și modelul naiv ca linie punctată.

## Combinarea modelelor: erorile care nu coincid se compensează {h=c3241f8b}

Dacă două modele greșesc în zile diferite, media simplă a prognozelor lor greșește mai rar decît fiecare dintre ele. Cu $K$ modele și ponderi egale (Bates & Granger, 1969; Nowotarski & Weron, 2015):

$$ \hat P^{\text{ens}}_{d,h}=\frac1K\sum_{k=1}^{K}\hat P^{(k)}_{d,h},\qquad \Var(\bar e)=\frac{\bar\sigma^2}{K}\big(1+(K-1)\bar\rho\big) $$ {#eq:ens}

unde $\hat P^{(k)}_{d,h}$ este prognoza modelului $k$, $K$ numărul de modele, $\bar e$ eroarea prognozei mediate, $\bar\sigma^2$ varianța medie a erorilor modelelor, iar $\bar\rho$ corelația medie a erorilor lor. Cu cît $\bar\rho$ este mai mic, cu atît cîștigul este mai mare; dacă erorile ar fi perfect corelate, medierea nu ar aduce nimic. Ponderile egale nu se estimează, ceea ce le face robuste.

Pe datele din România, ansamblul de 4 modele mediază AW-ARX, AW-LEAR, un model gradient boosting (GBM) și un perceptron multistrat (MLP), cu ponderi egale. Are MAE 22,13 EUR/MWh și rMAE 0,795, cel mai bun dintre toate modelele. Este mai precis decît AW-LEAR în 8 din 12 luni și în 15 din 24 de ore, iar testul DM față de AW-LEAR dă $p$ = 0,014. Cei doi membri mai slabi, GBM și MLP, ajută totuși, deoarece erorile lor diferă de cele ale modelelor liniare.

@practice cereți furnizorilor de prognoze serii pe care să le puteți combina cu ale dumneavoastră, nu un singur model „cel mai bun”.

## Clasamentul modelelor pe anul de test în România {h=51d466a1}

Tabelul reunește acuratețea tuturor modelelor în anul de test, 1 noiembrie 2025 – 31 octombrie 2026, 8 760 de ore. Pe slide, celulele sînt colorate separat pe fiecare coloană: verde pentru mai precis, roșu pentru mai puțin precis.

| Model | MAE | RMSE | sMAPE, % | rMAE |
|---|---|---|---|---|
| Naiv | 27,82 | 44,54 | 34,5 | 1,000 |
| Naiv sezonier | 34,41 | 55,48 | 39,4 | 1,237 |
| ARX(56) | 24,44 | 40,09 | 30,0 | 0,879 |
| ARX(728) | 22,72 | 36,62 | 27,8 | 0,817 |
| AW-ARX | 22,30 | 36,34 | 27,6 | 0,802 |
| ARX(728), model comun | 24,54 | 37,97 | 29,5 | 0,882 |
| ARX(728), fără VST | 22,86 | 35,85 | 28,4 | 0,822 |
| LEAR(364) | 22,96 | 36,80 | 28,1 | 0,825 |
| LEAR(728) | 22,62 | 36,36 | 27,7 | 0,813 |
| AW-LEAR | 22,53 | 36,35 | 27,7 | 0,810 |
| GBM | 24,05 | 37,73 | 28,7 | 0,864 |
| MLP | 25,54 | 40,05 | 29,8 | 0,918 |
| Ansamblu LEAR+MLP | 23,12 | 36,95 | 28,1 | 0,831 |
| Ansamblu de 4 modele | 22,13 | 35,76 | 27,4 | 0,795 |

Se văd trei regularități. Toate modelele de regresie sînt mult mai precise decît modelul naiv, în timp ce modelul naiv sezonier este mai slab decît cel naiv. Medierea, pe ferestre sau pe modele, ajută întotdeauna: AW-ARX depășește orice ARX individual, iar ansamblul de 4 modele are cele mai bune valori în toate coloanele. Modelele de învățare automată, luate separat, rămîn în urma celor liniare. Fără cele 2 zile cu schimbarea orei, MAE pentru AW-LEAR este 22,48, iar clasamentul nu se schimbă (Weron, 2014; Lago, Marcjasz, De Schutter & Weron, 2021).

## Gradient boosting: mulți arbori mici, fiecare corectîndu-i pe cei anteriori {h=7bd21c65}

Arborii de regresie surprind praguri și interacțiuni, de exemplu vînt slab și consum mare seara, pe care un model liniar nu le vede. Gradient boosting construiește prognoza ca sumă a multor arbori mici, fiecare estimat pe erorile rămase de la cei anteriori (Friedman, 2001):

$$ F_m(\mathbf x)=F_{m-1}(\mathbf x)+\nu\,f_m(\mathbf x) $$ {#eq:gbm}

$$ f_m=\arg\min_f\textstyle\sum_i\big(r_i^{(m)}-f(\mathbf x_i)\big)^2 $$ {#eq:gbmfit}

unde $F_m(\mathbf x)$ este prognoza după $m$ arbori pentru vectorul de intrare $\mathbf x$, $f_m$ un arbore de regresie mic, $r_i^{(m)}=Y_i-F_{m-1}(\mathbf x_i)$ reziduul curent al observației $i$, iar $\nu$ = 0,05 rata de învățare, care micșorează contribuția fiecărui arbore nou; numărul de arbori, 500, este fixat dinainte.

Modelul nostru GBM este unul singur pentru toate orele, ora fiind una dintre variabile, și folosește 20 de variabile, toate cunoscute la 12:00 în ziua $d-1$. Este reestimat la începutul fiecărei luni de test (12 reestimări), pe toate zilele anterioare (fereastră extinsă). Pe ansamblul anului are MAE 24,05 EUR/MWh și rMAE 0,864, mai puțin precis decît AW-LEAR. Totuși, în săptămîna de criză din studiul de caz (b) este cel mai bun model individual, cu MAE 34,35 (Lago et al., 2021).

@practice arborii merită incluși într-un ansamblu, chiar dacă nu sînt cei mai buni luați separat.

## Rețele neuronale: 24 de prețuri dintr-un singur vector de intrare {h=58c13518}

O rețea neuronală cu 24 de ieșiri prognozează toată ziua deodată, ca rețeaua neuronală profundă (DNN) din Lago et al. (2021). Cursul folosește un perceptron multistrat (MLP) mic:

$$ \hat{\mathbf Y}_d=W_3\,\phi\big(W_2\,\phi(W_1\mathbf x_d+b_1)+b_2\big)+b_3\in\mathbb R^{24} $$ {#eq:mlp}

unde $\hat{\mathbf Y}_d$ este vectorul celor 24 de prognoze ale prețului transformat din ziua $d$, $\mathbf x_d$ vectorul de intrare (cei 247 de regresori LEAR și 4 variabile fundamentale din $d-2$), $W_1$, $W_2$, $W_3$ matricele de ponderi, $b_1$, $b_2$, $b_3$ vectorii de termeni liberi ai straturilor, iar $\phi$ unitatea liniară rectificată (ReLU), $\phi(z)=\max(0,z)$. Cele două straturi ascunse au 128 și 64 de neuroni.

Disciplina seriilor de timp se aplică și aici. Numărul de epoci de antrenare se alege pe ultimele 15% din zilele de antrenare, în ordine cronologică (mediana: 20); se face media a 4 inițializări aleatoare; rețeaua se reestimează lunar, iar standardizarea variabilelor se estimează numai pe zilele de antrenare. Rezultatul este MAE 25,54 EUR/MWh și rMAE 0,918: o rețea mică, neoptimizată, nu depășește LEAR. Rețeaua DNN optimizată de Lago et al. (2021) obține rezultate mai bune, după cum arată cursul 7.

@practice o rețea neuronală cere ani de date și o calibrare atentă; altfel, păstrați LEAR.

## Pe ore, învățarea automată ajută în cadrul ansamblului, nu luată separat {h=1b733abe}

Graficul arată MAE pe ore pentru AW-LEAR, GBM, MLP și ansamblul de 4 modele. Luate separat, modelele de învățare automată sînt mai precise decît AW-LEAR în 0 ore (GBM) și în 0 ore (MLP). Ansamblul de 4 modele, care le include, este mai precis decît AW-LEAR în 15 din 24 de ore. Acesta este sensul practic al relației @eq:ens: un model mai slab, dar cu erori diferite, îmbunătățește totuși media.

Profilul pe ore arată și unde se concentrează erorile. Ora cea mai dificilă este 19 CET, cînd prețul urcă abrupt seara, după ce producția solară dispare, iar consumul este încă ridicat; la această oră AW-LEAR are MAE 34,52 EUR/MWh. Orele de noapte și cele de dimineață devreme sînt mult mai ușor de prognozat.

@practice alocați cel mai bun analist orelor de seară, unde se pierd cei mai mulți bani.

@chart ml_hour
MAE pe ore (CET) în anul de test pentru AW-LEAR, GBM, MLP și ansamblul de 4 modele; modelele ML sînt reestimate lunar.

## Studiul de caz C2: pentru consumul din România, învățarea automată dă cele mai mici erori {h=9099287f}

Învățarea automată nu rămîne întotdeauna în urma modelelor liniare. Un studiu al grupului nostru (Proșcanu, Proșcanu, Pele & Costea, 2025) a comparat modele sezoniere clasice cu rețele neuronale pe consumul național orar al României din perioada 2022–2024; în lucrare, o rețea neuronală are o eroare net mai mică decît modelul autoregresiv sezonier. Studiul de caz C2 al cursului reia comparația cu aceeași regulă ca în acest curs, adică date pînă la 12:00 în ziua $d-1$: 217 zile de test, începînd cu 27 mai 2024, cu consumul măsurat pînă în ziua $d-2$.

În replicarea noastră, MAPE este 4,09% pentru gradient boosting, 4,16% pentru modelul fundațional Chronos-Bolt și 4,58% pentru MLP, față de 4,85% pentru o regresie liniară, 8,03% pentru un model autoregresiv sezonier și 10,17% pentru modelul naiv care copiază consumul de acum două zile. Cifrele C2 sînt calculate cu notebook-ul Jupyter al studiului de caz C2, pe datele noastre; rezultatele lucrării sînt prezentate în fișa studiului de caz.

Diferența față de prețuri are o explicație clară. Consumul variază lin și nu se apropie de zero, astfel încît MAPE are sens, iar modelele neliniare găsesc regularități de învățat. Prețurile au salturi și devin negative; aici, un model liniar bine construit este greu de depășit.

@practice prognozați consumul propriu cu modele ML, iar prețul cu LEAR și un ansamblu de modele.

## @end

Medierea pe ferestre de calibrare și pe modele dă cele mai bune prognoze din anul de test: ansamblul de 4 modele ajunge la rMAE 0,795. Modelele de învățare automată ajută în cadrul ansamblului, chiar dacă, luate separat, sînt mai puțin precise.

# Prognoze probabilistice și cointegrare

O prognoză punctuală nu ajunge pentru gestiunea riscului, iar prețurile piețelor vecine sau ale combustibililor sînt legate pe termen lung. Secțiunea transformă prognozele punctuale în cuantile prin QRA și verifică dacă sînt bine calibrate, apoi testează cointegrarea dintre România și Ungaria și dintre prețul energiei, prețul gazelor și producția hidro.

## Medierea prin regresie cuantilică: de la prognoze punctuale la cuantile {h=dd8d72ef}

QRA regresează prețul realizat pe mai multe prognoze punctuale, separat pentru fiecare nivel al cuantilei, iar rezultatul este o distribuție a prețului (Koenker & Bassett, 1978; Nowotarski & Weron, 2015):

$$ \hat q^{\tau}_{d,h}=\beta^{\tau}_{0,h}+\beta^{\tau}_{1,h}\hat P^{\text{AW-ARX}}_{d,h}+\beta^{\tau}_{2,h}\hat P^{\text{AW-LEAR}}_{d,h} $$ {#eq:qra}

$$ \text{PS}_\tau(q,y)=\big(\mathbf{1}\{y<q\}-\tau\big)(q-y) $$ {#eq:pinball}

unde $\hat q^{\tau}_{d,h}$ este cuantila de nivel $\tau$ a prețului orei $h$ din ziua $d$, $\hat P^{\text{AW-ARX}}_{d,h}$ și $\hat P^{\text{AW-LEAR}}_{d,h}$ sînt cele două prognoze punctuale, iar coeficienții $\boldsymbol\beta^{\tau}_h=(\beta^{\tau}_{0,h},\beta^{\tau}_{1,h},\beta^{\tau}_{2,h})$ minimizează scorul pinball (PS) din @eq:pinball pe prognozele din ultimele 182 de zile, cu reestimare săptămînală. În @eq:pinball, $q$ este o cuantilă prognozată, $y$ prețul realizat, iar $\mathbf{1}\{y<q\}$ ia valoarea 1 cînd prețul este sub cuantilă și 0 în caz contrar. Nivelurile sînt $\tau$ = 0,01, …, 0,99.

Două metode mai simple servesc drept comparație: predicția conformală (CP) și simularea istorică (HS), care folosesc amîndouă erorile AW-LEAR din ultimele 112 zile, ca în tema 1. Scorul pinball mediu (mai mic = mai bine) este 8,33 pentru QRA, 8,47 pentru CP și 8,41 pentru HS. Intervalul de 90% conține însă doar 85,7% din prețuri pentru QRA, 87,0% pentru CP și 85,8% pentru HS; lățimea medie a intervalului QRA este 93,0 EUR/MWh. Toate sînt sub 90%, iar testul Kupiec respinge ipoteza unei acoperiri corecte.

@practice o bandă de 90% care conține doar 86% din prețuri subestimează riscul poziției deschise.

## O săptămînă de intervale QRA în România: largi seara, înguste noaptea {h=920981fd}

Graficul arată prognozele QRA pentru săptămîna 12 octombrie 2026 – 18 octombrie 2026, oră cu oră: intervalele de 90% și de 50%, mediana QRA și prețul realizat. Intervalul se lărgește seara, cînd prețul este incert, și se îngustează noaptea, cînd prețul este stabil. Așa trebuie să se comporte o prognoză probabilistică bună: lățimea intervalului urmează incertitudinea fiecărei ore, în loc să fie aceeași la toate orele.

Mediana distribuției QRA este ea însăși o prognoză punctuală. Pe anul de test are MAE 22,14 EUR/MWh, la fel de precisă ca cea mai bună prognoză punctuală. Trecerea de la prognoze punctuale la cuantile nu costă, așadar, nimic în acuratețea punctuală și adaugă o măsură a riscului (Nowotarski & Weron, 2015).

@practice pentru volumele pe care trebuie să le cumpărați, ofertați în intervalul de 50%; pentru cele pe care le puteți muta în altă oră, folosiți cozile.

@chart qra_week
Prețul orar realizat, mediana QRA și intervalele QRA de 50% și de 90% pentru săptămîna 12–18 octombrie 2026, în EUR/MWh.

## Toate cele trei metode subestimează cozile distribuției prețului {h=1c2fdbbd}

O prognoză probabilistică este bine calibrată cînd exact $\tau$% din prețuri se află sub cuantila de nivel $\tau$, pentru orice nivel $\tau$. Graficul arată, pentru cele 99 de niveluri ale cuantilei, ponderea prețurilor aflate sub cuantila prognozată minus $\tau$, în puncte procentuale; o prognoză calibrată perfect se află pe linia 0. Toate cele trei metode sînt peste linie în stînga și sub linie în dreapta: prea multe prețuri cad sub cuantilele mici și peste cele mari, deci cozile sînt prea înguste.

Testul Kupiec pentru intervalul de 90% confirmă formal acest lucru (Kupiec, 1995; Gneiting & Raftery, 2007). Statistica sa este 162,9 pentru QRA, 83,3 pentru CP și 154,1 pentru HS, mult peste valoarea critică de 3,84 la pragul de 5%. Testul este definit în Anexa C.

@practice lărgiți cozile înainte de a folosi cuantilele pentru calculul garanțiilor (cursul 4).

@chart prob_rel
Ponderea prețurilor aflate sub fiecare cuantilă prognozată minus nivelul cuantilei $\tau$, în puncte procentuale, pentru QRA, CP și HS, pe cele 99 de niveluri ale cuantilei din anul de test.

## Două prețuri sînt cointegrate dacă diferența dintre ele revine spre echilibru {h=5d884617}

Fiecare dintre două prețuri poate fi nestaționar, dar, dacă o combinație liniară a lor este staționară, abaterea dintre ele se închide, iar regresia dintre ele nu este spurioasă. Procedura Engle–Granger testează acest lucru în doi pași (Engle & Granger, 1987):

$$ P^{\text{RO}}_t=\alpha+\beta P^{\text{HU}}_t+u_t $$ {#eq:eg1}

$$ \Delta\hat u_t=\rho\,\hat u_{t-1}+\textstyle\sum_j\gamma_j\Delta\hat u_{t-j}+\eta_t $$ {#eq:eg2}

unde $P^{\text{RO}}_t$ și $P^{\text{HU}}_t$ sînt prețurile zilnice din România și din Ungaria, $\alpha$ și $\beta$ se estimează prin OLS la pasul 1 @eq:eg1, $\hat u_t$ este reziduul (diferența de preț), iar pasul 2 @eq:eg2 testează existența unei rădăcini unitare în $\hat u_t$, cu $\Delta$ diferența de ordinul întîi, $\gamma_j$ coeficienții diferențelor decalate și $\eta_t$ eroarea. Ipoteza nulă este absența cointegrării ($\rho=0$), cu valori critice MacKinnon (1996). Testul urmei Johansen (Johansen, 1991) testează în schimb rangul $r$, adică numărul relațiilor de cointegrare, într-un model vectorial cu corecția erorii.

Pentru România și Ungaria, cu date zilnice din 1 ianuarie 2022, $\hat\beta$ = 0,963, iar statistica Engle–Granger este −10,58, față de valoarea critică de −3,34 la 5%: prețurile sînt cointegrate. Un șoc asupra diferenței de preț se înjumătățește în 0,8 zile. Testul urmei Johansen dă 139,7 față de 15,49 pentru $r=0$ și 6,21 față de 3,84 pentru $r\le1$, deci rangul 2: chiar nivelurile sînt aproape staționare din 2022 (testul Dickey–Fuller augmentat (ADF), $p$ = 0,064).

@practice o poziție pe diferența de preț RO–HU se închide în cîteva zile, nu în luni.

## România și Ungaria: piețe cuplate, cu o diferență de preț care se închide repede {h=7a01d77c}

Panoul de sus al graficului arată prețurile zilnice de bază din România (OPCOM PZU) și din Ungaria (HUPX) din 2022, iar panoul de jos diferența dintre ele. La această scară, cele două serii aproape că nu se pot distinge. Diferența RO − HU are media −2,07 EUR/MWh și abaterea standard 15,08. Prin comparație, diferența dintre România și Germania–Luxemburg are media 21,06 și abaterea standard 37,79: piața mai îndepărtată este mai slab legată de cea românească.

În anul de test, prețurile din RO și HU au fost identice în 10,1% din ore. În restul orelor, interconexiunea dintre cele două zone a fost congestionată, iar prețurile au putut diferi, dar diferența a continuat să se închidă (Engle & Granger, 1987).

@practice folosiți prețul din Ungaria ca regresor sau ca verificare a prognozei pentru România.

@chart coint_daily
Prețurile zilnice de bază din România și din Ungaria, 1 ianuarie 2022 – 31 octombrie 2026 (sus), și diferența RO − HU (jos), în EUR/MWh.

## Prețul energiei revine spre nivelul dat de gaze: model cu corecția erorii {h=ad6ce5fa}

În cursul 1, prețul lunar al energiei electrice din România a fost regresat pe prețul gazelor și pe producția hidro. Dacă prețul energiei și cel al gazelor sînt cointegrate, regresia nu este spurioasă, iar prețul energiei revine lunar spre nivelul dat de gaze, în timp ce producția hidro îl abate temporar. Modelul cu corecția erorii (ECM) descrie direct acest mecanism:

$$ \Delta P_t=c+\underbrace{\alpha\,(P_{t-1}-a-\beta\,\text{TTF}_{t-1})}_{\text{corecția erorii}}+\gamma\,\Delta\text{TTF}_t+\delta\,H_t+\varepsilon_t $$ {#eq:ecm}

unde $P_t$ este prețul mediu lunar al energiei electrice din România, $\text{TTF}_t$ prețul gazelor în EUR/MWh, $a+\beta\,\text{TTF}_{t-1}$ nivelul de echilibru pe termen lung (dat de gaze), $H_t$ producția hidro minus media lunii calendaristice, în TWh (terawatt-oră), o serie staționară, $c$ o constantă, $\gamma$ efectul imediat al unei variații a prețului gazelor, $\delta$ efectul producției hidro suplimentare, iar $\varepsilon_t$ eroarea. Coeficientul $\alpha<0$ este viteza de revenire spre echilibru.

Pe datele din perioada 2015-01 – 2026-10, statistica Engle–Granger este −5,64, față de valoarea critică de −3,38 la 5%, iar rangul Johansen este 1: prețul energiei și cel al gazelor sînt cointegrate. Estimația $\hat\beta$ = 1,95 arată că prețul se comportă ca și cum ar fi stabilit de o centrală pe gaze cu randament de circa 51%. În ECM, $\hat\alpha$ = −0,452, ceea ce dă un timp de înjumătățire de 1,2 luni, iar $\hat\delta$ = −12,80 EUR/MWh pentru fiecare TWh suplimentar de producție hidro, cu $t$ = −3,10 (Engle & Granger, 1987; Johansen, 1991).

@practice într-o lună secetoasă, un producător hidro se poate aștepta la prețuri peste nivelul dat de gaze timp de una sau două luni.

## Prețul energiei, gazele și hidro: regresia din cursul 1 nu este spurioasă {h=6a3671f9}

Panoul din stînga al graficului arată prețul lunar din România împreună cu nivelul său de echilibru dat de prețul gazelor TTF, din regresia de cointegrare; prețul urmează acest nivel, cu abateri care se închid în cîteva luni. Panoul din dreapta arată, pentru fiecare lună, abaterea prețului de la echilibru în funcție de producția hidro raportată la media lunii respective. Panta este negativă: în lunile cu producție hidro peste medie, prețul este sub nivelul dat de gaze, iar în lunile cu producție hidro sub medie, peste acest nivel.

Cele două panouri arată împreună că regresia din cursul 1 surprinde o relație reală pe termen lung, nu o coincidență între două serii cu trend, și că producția hidro explică o mare parte din abaterile temporare.

@practice interpretați un an hidrologic secetos ca o primă de preț peste nivelul dat de gaze, nu ca un nou nivel al prețului.

@chart coint_monthly
Stînga: prețul lunar din România și nivelul de echilibru dat de prețul gazelor TTF, 2015-01 – 2026-10, în EUR/MWh; dreapta: abaterea de la echilibru în funcție de producția hidro minus media lunii, în TWh, cîte un punct pentru fiecare lună.

## @end

QRA transformă prognozele punctuale în intervale a căror lățime urmează incertitudinea fiecărei ore, dar toate metodele au cozi prea înguste. Prețurile din România și Ungaria sînt cointegrate, iar diferența dintre ele se înjumătățește în mai puțin de o zi; prețul lunar al energiei este cointegrat cu prețul gazelor, iar producția hidro explică abaterile.

# Studii de caz pe date recente din România

Patru studii de caz aplică modelele din curs pe date recente din România și traduc acuratețea în întrebările unui manager: cît de stabilă este acuratețea de-a lungul anului, ce se întîmplă într-o săptămînă de criză, cum se prognozează noile prețuri pe sfert de oră și cît valorează, în euro, o prognoză mai bună. Secțiunea se încheie cu o listă de verificări pentru orice birou de prognoză.

## Studiul de caz (a): acuratețea diferă mult de la o lună la alta {h=72a86c52}

Graficul urmărește MAE lunară a modelului naiv, a AW-ARX, a AW-LEAR și a ansamblului de 4 modele în anul de test. AW-LEAR este mai precis decît modelul naiv în 12 din 12 luni, deci cîștigul nu se datorează unei singure perioade favorabile. Nivelul erorii variază însă mult: MAE pentru AW-LEAR este între 12,84 EUR/MWh în decembrie 2025 și 34,88 EUR/MWh în octombrie 2026.

Imaginea lunară arată și că o medie anuală bună poate ascunde perioade slabe: octombrie 2026 este luna cea mai dificilă din anul de test. Defalcarea pe trimestre din Anexa B spune aceeași poveste.

@practice raportați acuratețea lună de lună: o MAE anuală bună poate ascunde o toamnă slabă.

@chart monthly_mae
MAE lunară a modelului naiv, a AW-ARX, a AW-LEAR și a ansamblului de 4 modele în anul de test, în EUR/MWh.

## Studiul de caz (b): în săptămîna de criză (19 octombrie 2026) modelele întîrzie o zi {h=cd6defa6}

Săptămîna 19–25 octombrie 2026 a fost o perioadă de criză pe piața din România. Prețul mediu a fost 258,59 EUR/MWh, iar maximul 412,35 EUR/MWh. Graficul arată prețul orar realizat, împreună cu prognozele modelului naiv, ale AW-LEAR și ale ansamblului.

În această săptămînă, MAE este 40,19 pentru modelul naiv, 36,54 pentru AW-LEAR, 34,35 pentru GBM și 34,95 pentru ansamblu. Modelele rămîn mai precise decît cel naiv, dar toate reacționează la un salt brusc al nivelului prețului cu aproximativ o zi întîrziere: prognozele se bazează pe prețurile de ieri, deci ajung din urmă noul nivel abia după ce acesta apare în date. GBM, mai puțin precis decît AW-LEAR pe întregul an, este cel mai bun model individual în această săptămînă.

@practice toate modelele reacționează la un salt de nivel cu o zi întîrziere; acoperiți riscul orelor de seară.

@chart stress_week
Prețul orar realizat și prognozele modelului naiv, ale AW-LEAR și ale ansamblului pentru săptămîna 19–25 octombrie 2026, în EUR/MWh.

## Studiul de caz (c): sferturile de oră cer un profil în interiorul orei {h=e41d636f}

Din 1 octombrie 2025, intervalul de tranzacționare (MTU) al licitației PZU are 15 minute, deci fiecare oră are patru prețuri. Modelele orare din acest curs prognozează media celor patru. O cale simplă de a obține prognoze pe sfert de oră este să adăugăm la prognoza orară AW-LEAR profilul intraorar mediu din ultimele 28 de zile, adică abaterea obișnuită a fiecărui sfert de oră de la media orei sale.

Graficul arată o singură zi, 1 iulie 2026: prețul realizat pe 15 minute, prognoza orară AW-LEAR, constantă în interiorul orei, și prognoza cu profil. Pe cele 363 de zile de test fără schimbarea orei, MAE pe sfert de oră este 26,02 EUR/MWh cu valoare constantă în oră și 24,53 EUR/MWh cu profil. Un profil simplu, estimat numai din zilele trecute, recuperează deja o parte din structura din interiorul orei.

@practice o baterie licitează pe sferturi de oră; folosiți profilul intraorar, nu o valoare constantă.

@chart mtu15
Prețurile realizate pe 15 minute din 1 iulie 2026, prognoza orară AW-LEAR constantă în interiorul orei și prognoza cu profilul intraorar din ultimele 28 de zile, în EUR/MWh.

## Studiul de caz (d): cît valorează, în bani, o prognoză mai bună {h=b014276a}

O rMAE mai bună contează numai dacă schimbă deciziile. Studiul de caz traduce acuratețea prognozei în bani pentru doi utilizatori. Primul este o baterie de 1 MW (megawatt) și 2 MWh, cu randament de 90%, care face un ciclu pe zi: se încarcă în orele cele mai ieftine și se descarcă în cele mai scumpe, alese după prognoză. În cele 363 de zile fără schimbarea orei, bateria cîștigă 90 738 EUR pe MW cu prognoza ansamblului, adică 91,0% din profitul cu informație perfectă, față de 84 623 EUR cu modelul naiv.

Al doilea este un furnizor cu un proces flexibil de 4 ore, care poate fi plasat oriunde în zi. Plasarea lui în orele pe care AW-LEAR le prognozează ca fiind cele mai ieftine costă 67,87 EUR/MWh, față de 100,59 EUR/MWh pentru un bloc fix 8–12 CET. Graficul arată ambele rezultate pentru informația perfectă, ansamblu, AW-LEAR, GBM, AW-ARX și modelul naiv.

@practice transformați rMAE în EUR înainte de a plăti pentru o prognoză.

@chart battery
Stînga: profitul bateriei în anul de test, în mii EUR pe MW, pentru fiecare prognoză și pentru informația perfectă; dreapta: prețul mediu plătit de cumpărătorul flexibil, în EUR/MWh, cu blocul fix 8–12 pentru comparație.

## O prognoză se acceptă numai după o listă de verificări; testul nostru arată că nu folosim informație din viitor {h=632bc1ff}

Înainte de a avea încredere într-o testare retrospectivă, un birou de prognoză trebuie să verifice trei lucruri: fiecare variabilă de intrare a fost publicată înainte de ora 12:00 CET din ziua $d-1$; standardizările, transformările, penalizarea $\lambda$ și eventualele praguri s-au estimat numai pe fereastra de calibrare; validarea a fost cronologică, iar anul de test a fost folosit o singură dată. Raportul trebuie să conțină apoi MAE și rMAE față de modelul naiv, valorile $p$ ale testelor DM și acoperirea intervalelor, pe luni și pe ore, nu doar o cifră anuală.

Analiza din spatele acestui curs se verifică singură (scriptul de analiză, secțiunea 7). Ea face 9 364 de verificări ale momentului publicării, care confirmă că fiecare variabilă este disponibilă cu cel puțin 12 h înainte de ora 12:00. Recalculează 17 serii de prognoză în 14 zile, iar GBM și MLP în prima zi a fiecăreia dintre cele 12 reestimări, după ce datele ulterioare au fost șterse sau înlocuite cu valori absurde; prognozele rămîn identice, pînă la rotunjire. Rezultat: verificare trecută (Lago et al., 2021).

@practice includeți testul de folosire a informației din viitor în orice evaluare a unui model, ca în tema 1.

## @end

Acuratețea variază mult de la o lună la alta, iar toate modelele reacționează cu o zi întîrziere la un salt brusc al prețului, dar prognozele mai bune aduc bani: cu ansamblul, bateria obține 91,0% din profitul cu informație perfectă. Lista de verificări și testul de folosire a informației din viitor fac rezultatele credibile.

# Recapitulare

Recapitularea verifică ideile principale prin cinci întrebări scurte, rezumă cursul și prezintă cercetările grupului nostru și lecturile suplimentare.

## Verifică-te {h=f723684f}

1. Este duminică, ora 11:30 CET, și trebuie să prognozați cu modelul naiv prețul de luni pentru ora 19:00. Ce preț folosiți? Răspuns: prețul de luni trecută, ora 19:00 ($d-7$). În anul de test, pentru zilele de luni, sîmbătă și duminică, această regulă este mai precisă decît prețul din ziua precedentă (MAE 29,87 față de 33,48 EUR/MWh).
2. Un furnizor de prognoze raportează rMAE 0,55 pentru România, dar folosește ca regresor consumul realizat în ziua $d-1$. Cumpărați prognoza? Răspuns: nu. La ora 12:00 din ziua $d-1$, consumul acelei zile nu este încă măsurat, deci testarea folosește informație din viitor. Cereți o nouă testare cu date pînă în ziua $d-2$ (sau cu prognozele publicate de TSO); cel mai bun rezultat corect al nostru este rMAE 0,795.
3. AW-LEAR sau AW-ARX? Testul DM dă $p$ = 0,797. Ce model intră în producție? Răspuns: niciunul nu este semnificativ mai precis. Alegeți modelul mai simplu sau, mai bine, media lor, care face parte din cel mai bun ansamblu (rMAE 0,795).
4. Raportul dumneavoastră indică MAPE 5 778% pentru prognoza prețului din România, iar consiliul de administrație este alarmat. Ce răspundeți? Răspuns: MAPE împarte eroarea la prețuri apropiate de zero; 387 de ore sub 5 EUR/MWh produc 99,5% din valoarea ei. Raportați în schimb MAE 22,53 EUR/MWh și rMAE 0,810.
5. Prețurile din România și Ungaria sînt cointegrate, iar un șoc asupra diferenței se înjumătățește în 0,8 zile. Astăzi prețul din România este cu 40 EUR/MWh mai mare decît cel din Ungaria. La ce vă așteptați? Răspuns: diferența ar trebui să se reducă la circa jumătate în aproximativ o zi, dacă interconexiunea nu rămîne congestionată. Este un semnal pentru tranzacțiile transfrontaliere, nu o garanție.

## Recapitulare {h=5928e570}

Cursul a pornit de la un cadru corect: numai informația disponibilă la ora 12:00 CET în ziua $d-1$, ferestre glisante, modelul naiv ca reper și teste DM pentru compararea modelelor. Pe această bază, modelele expert ARX și varianta lor cu LASSO, LEAR, reduc eroarea modelului naiv cu aproape o cincime, iar medierea pe ferestre și pe modele adaugă un cîștig suplimentar, semnificativ statistic. În anul de test, cel mai bun model, ansamblul de 4 modele, reduce eroarea modelului naiv cu 20,5%.

QRA transformă aceste prognoze punctuale în intervale, utile, dar cu cozi prea înguste. Cointegrarea leagă prețul din România de cel din Ungaria și, pe termen lung, de prețul gazelor. Cursul următor trece de la nivelul prețurilor la volatilitatea lor (cursul 3).

## Cercetările grupului nostru despre prognoza consumului și a prețurilor în România {h=affe5b83}

Mai multe lucrări ale grupului nostru de la Academia de Studii Economice din București și de la Academia Română, Institutul de Prognoză Economică, tratează întrebările din acest curs. Rezultatele de mai jos sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.

- **Compararea modelelor de prognoză a consumului.** Proșcanu, Proșcanu, Pele & Costea (2025) compară modele sezoniere clasice și rețele neuronale pe consumul național orar al României; o rețea neuronală are o eroare net mai mică decît modelul autoregresiv sezonier. Comparația stă la baza studiului de caz C2.
- **Patru generații de modele pentru prețul energiei.** Andrei, Velev, Toma, Pele & Lessmann (2024) evaluează comparativ patru generații de metode de prognoză a prețurilor energiei, un reper pentru alegerea familiei de modele.
- **Explicarea prognozelor de preț pe mai multe orizonturi.** Andrei, Pele & Cramer (2026) explică prognozele prețurilor orare din România și arată ce factori contează la fiecare orizont de prognoză și în fiecare regim de preț.
- **Avertizarea timpurie a salturilor de preț.** Andrei, Pele, Cramer, Amza & Diaconu (2026) construiesc un sistem explicabil de inteligență artificială (AI) pentru piața din România, în care prețul anterior și consumul rezidual sînt principalii factori ai salturilor, temă dezvoltată în cursul 7.

## Lecturi și resurse suplimentare {h=8d7aa196}

- R. Weron, IIF Distinguished Lectures despre prognoza prețurilor energiei electrice (2025): prezentări [partea I](https://p.wz.pwr.edu.pl/~weron.rafal/assets/PDF/Weron25_IIF_1.pdf), [partea a II-a](https://p.wz.pwr.edu.pl/~weron.rafal/assets/PDF/Weron25_IIF_2.pdf) și [notebook-uri Jupyter](https://github.com/lipiecki/energy-analytics-2025).
- epftoolbox, cu LEAR și DNN și setul de date pentru evaluare publicat de Lago et al. (2021): [github.com/jeslago/epftoolbox](https://github.com/jeslago/epftoolbox).
- Forecasting: Principles and Practice, ediția a 3-a: [otexts.com/fpp3](https://otexts.com/fpp3/).
- Acest curs, cu cod, date și notebook-uri Jupyter: [github.com/danpele/EMQA](https://github.com/danpele/EMQA). Notebook-ul cursului reproduce toate graficele și cifrele.
- Tema 1 aplică ARX, LEAR, testul DM și intervalele HS și CP pe propria fereastră de test.

# Anexă

Anexa prezintă detaliile tehnice din spatele slide-urilor principale: specificarea completă a modelului LEAR, acuratețea pe trimestre, scorurile probabilistice și testul Kupiec, precum și toate testele de rădăcină unitară și de cointegrare.

## Anexa A: modelul LEAR în detaliu {h=b3d3b509}

Penalizarea $\lambda$ din @eq:lasso se alege zilnic prin AIC, calculat de-a lungul traiectoriei de regularizare LASSO:

$$ \text{AIC}(\lambda)=n\ln\frac{\text{RSS}(\lambda)}{n}+2\,\mathrm{df}(\lambda) $$ {#eq:aic}

unde $n$ este numărul zilelor de calibrare, $\text{RSS}(\lambda)$ suma pătratelor reziduurilor (RSS) pentru penalizarea $\lambda$, iar $\mathrm{df}(\lambda)$ gradele de libertate, egale cu numărul coeficienților nenuli. Traiectoria de regularizare se calculează cu algoritmul regresiei unghiului minim (*least angle regression*, LARS), în scikit-learn.

Blocul prețurilor se transformă cu @eq:vst, unde $m$ și $s$ sînt mediana și 1,4826 · MAD ale prețurilor din zilele $d-T-7,\dots,d-1$, calculate pe toate cele 24 de ore împreună. Consumul și producția eoliană și solară au o transformare asinh proprie, cu date pînă în ziua $d-2$, apoi fiecare coloană este standardizată pe zilele de calibrare. Cele 247 de coloane se compun astfel:

| Bloc | Coloane |
|---|---|
| prețuri d-1, toate cele 24 de ore | 24 |
| prețuri d-2, d-3, d-7 | 72 |
| consum d-2, d-3, d-7 | 72 |
| eolian + solar d-2, d-3, d-7 | 72 |
| ziua săptămînii | 7 |
| **total** | **247** |

## Anexa B: MAE pe trimestre în anul de test {h=d8f429db}

Tabelul dă MAE, în EUR/MWh, a principalelor modele, pe trimestre. Anul de test începe la 1 noiembrie 2025, deci trimestrele au 61, 90, 91, 92 și 31 de zile. Pe slide, verdele marchează cel mai bun model din fiecare trimestru, iar roșul pe cel mai slab.

| Model | 2025 T4 | 2026 T1 | 2026 T2 | 2026 T3 | 2026 T4 |
|---|---|---|---|---|---|
| naiv | 19,80 | 30,19 | 27,55 | 28,32 | 36,05 |
| AW-ARX | 15,24 | 23,62 | 22,97 | 22,09 | 31,05 |
| AW-LEAR | 14,86 | 22,99 | 22,64 | 22,91 | 34,88 |
| GBM | 16,25 | 24,71 | 22,98 | 24,97 | 37,88 |
| MLP | 17,27 | 25,49 | 24,89 | 26,30 | 41,58 |
| ansamblu de 4 modele | 14,82 | 23,02 | 22,09 | 22,50 | 32,91 |

Ansamblul este cel mai bun sau aproape de cel mai bun în fiecare trimestru, în timp ce ordinea modelelor individuale se schimbă; în ultima lună, octombrie 2026, AW-ARX este mai precis decît AW-LEAR.

## Anexa C: scoruri probabilistice și testul Kupiec {h=38ad4d47}

Testul Kupiec (Kupiec, 1995) este un test al raportului de verosimilitate (LR) pentru acoperirea necondiționată (UC):

$$ \text{LR}_{\text{UC}}=-2\ln\frac{(1-p_0)^{n-x}p_0^{\,x}}{(1-\hat p)^{n-x}\hat p^{\,x}}\sim\chi^2_1,\qquad \hat p=\frac xn $$ {#eq:kupiec}

unde $x$ este numărul orelor din afara intervalului de 90%, $n$ = 8 760 numărul orelor, $p_0$ = 0,10 proporția nominală din afara intervalului, iar $\hat p$ proporția observată; dacă acoperirea este corectă, statistica urmează o distribuție $\chi^2$ cu un grad de libertate. Orele aceleiași zile nu sînt independente, deci testul este orientativ; testul pe proporția zilnică a depășirilor, cu varianță Newey–West, dă $p<0{,}001$ pentru QRA.

Scorul pinball este mediat pe cele 99 de cuantile; scorul de probabilitate ordonat continuu este aproximativ 2 × acest scor (Gneiting & Raftery, 2007).

| Metoda | Pinball | Acop. 50% | Acop. 90% | Kupiec |
|---|---|---|---|---|
| QRA | 8,33 | 47,3 | 85,7 | 162,9 |
| CP | 8,47 | 46,5 | 87,0 | 83,3 |
| HS | 8,41 | 45,8 | 85,8 | 154,1 |

## Anexa D: testele de rădăcină unitară și de cointegrare, în detaliu {h=99488be4}

Tabelul cuprinde toate testele de rădăcină unitară și de cointegrare din curs. Testele ADF folosesc un număr de decalaje ales prin AIC; testele Johansen includ o constantă și 6 diferențe decalate pentru datele zilnice sau 2 pentru datele lunare. ECM din @eq:ecm este estimat cu erori standard robuste la heteroscedasticitate și autocorelație (6 decalaje), pe 141 de luni, cu $R^2$ = 0,778.

| Serie / pereche | Test | Statistica | p / crit. 5% |
|---|---|---|---|
| RO, HU, DE-LU, niveluri zilnice | ADF p | – | 0,064, 0,052, 0,015 |
| RO–HU | Engle–Granger | −10,58 | −3,34 |
| RO–HU | Johansen r=0 / r≤1 | 139,7 / 6,21 | 15,49 / 3,84 |
| RO–DE-LU | Engle–Granger | −5,79 | −3,34 |
| preț RO, TTF, niveluri lunare | ADF p | – | 0,295, 0,249 |
| hidro minus media lunii | ADF p | – | 0,002 |
| preț–TTF | Engle–Granger | −5,64 | −3,38 |
| preț–TTF–hidro | Engle–Granger | −5,95 | −3,80 |
| preț–TTF | Johansen r=0 / r≤1 | 21,32 / 3,74 | 15,49 / 3,84 |

Nivelurile lunare ale prețului și ale TTF au rădăcină unitară (valori $p$ ADF de 0,295 și 0,249), în timp ce producția hidro minus media lunii este staționară (0,002); testele Engle–Granger resping absența cointegrării pentru fiecare pereche, ceea ce susține ECM din @eq:ecm.
