<!--
Versiunea web a Cursului 3 (RO). Construită în web/L3_ro.html de lectures/common/build_web_lecture.py (formatul: docstring-ul scriptului).
Hash-urile slide-urilor: python3 build_web_lecture.py 3 --frames
-->

## @intro

Prețul energiei electrice se stabilește din nou în fiecare zi, pentru fiecare oră, pe piața pentru ziua următoare. Un furnizor, un producător sau un consumator mare care cumpără ori vinde pe această piață nu este interesat numai de prețul așteptat: îl interesează cît de departe de așteptarea de azi poate ajunge prețul de mîine. Această distanță este volatilitatea prețului și de ea depind mărimea limitelor de tranzacționare, garanțiile plătite bursei, marja pe care un furnizor o adaugă la un contract cu preț fix și valoarea unei baterii. Cursul măsoară volatilitatea pe date reale de pe Piața pentru Ziua Următoare (PZU) din România, administrată de operatorul pieței de energie electrică și de gaze naturale din România (OPCOM), între 1 ianuarie 2019 și 31 octombrie 2026, și o compară cu volatilitatea țițeiului, a certificatelor de emisii, a gazelor naturale și a acțiunilor energetice românești.

Energia electrică nu se comportă ca un activ financiar. Ea nu poate fi stocată, astfel că energia livrată în ziua $t$ și cea livrată în ziua $t-1$ sînt produse diferite, iar prețul se poate apropia de zero sau poate deveni chiar negativ. Variațiile zilnice sînt foarte mari: abaterea lor standard este de 28,3% pe zi, iar prețul energiei electrice este de circa 9 ori mai volatil decît cel al petrolului. În plus, volatilitatea apare grupată: un șoc mare astăzi anunță șocuri mari și în zilele următoare. Aceste două fapte, împreună cu un calendar săptămînal foarte pronunțat, determină toate instrumentele folosite în curs.

Mai întîi stabilim cum se măsoară volatilitatea, în procente sau în euro pe megawatt-oră, după eliminarea efectului zilei din săptămînă. Apoi o modelăm cu modele cu heteroscedasticitate condiționată autoregresivă generalizată (GARCH), separăm regimurile calme de cele agitate, măsurăm riscul din cursul zilei pe baza prețurilor orare și comparăm prognozele de volatilitate în afara eșantionului. Cursul se încheie cu un studiu de caz despre anul 2026 și cu răspunsul promis în cursul 1: cît timp trebuie menținute limite de risc mai largi după un șoc.

@goals
- **Măsurați** corect volatilitatea, ca variații procentuale sau în EUR/MWh ale prețului pentru ziua următoare, după eliminarea efectului zilei din săptămînă, și decideți ce faceți cînd prețurile se apropie de zero sau devin negative.
- **Modelați** volatilitatea cu modele GARCH cu șocuri de tip Student și interpretați persistența, timpul de înjumătățire al unui șoc și asimetria dintre creșterile și scăderile de preț.
- **Recunoașteți** regimurile calme și agitate, criza energetică din 2021–2022 și anul 2026, precum și riscul din cursul zilei creat de producția solară.
- **Prognozați și evaluați** volatilitatea pentru ziua următoare și pentru următoarele săptămîni, comparînd prognozele cu o funcție de pierdere robustă și cu un test de semnificație.
- **Stabiliți** cît timp trebuie menținute limite de risc mai largi după un șoc, întrebarea lăsată deschisă în cursul 1.

# Măsurarea volatilității

Înainte de orice model, două alegeri stabilesc ce înseamnă „volatilitate” pentru energia electrică: unitatea în care măsurăm variația prețului, procente sau euro pe megawatt-oră, și ceea ce eliminăm din variație pentru că este cunoscut dinainte, adică efectul zilei din săptămînă. Secțiunea face ambele alegeri pe datele din România și descrie faptele stilizate pe care modelele din secțiunile următoare trebuie să le reproducă: gruparea volatilității, cozile groase și o volatilitate în bani care crește odată cu nivelul prețului.

## Sursele datelor: energie electrică, combustibili, carbon și acțiuni energetice {h=122bad76}

Cursul folosește numai date reale, descărcate din surse publice. Seria principală este prețul pe PZU din România (RO); pentru comparație folosim Ungaria (HU) și zona de ofertare Germania–Luxemburg (DE-LU). Prețurile provin de la OPCOM, de la bursa de energie din Ungaria (HUPX) și de la EPEX SPOT și sînt preluate de la Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E), prin energy-charts.info, portalul de date al Institutului Fraunhofer pentru Sisteme de Energie Solară (ISE). Datele de energie electrică sînt zilnice și orare și acoperă perioada 1 ianuarie 2019 – 31 octombrie 2026, ultima lună completă: 2 861 de zile de livrare, după ora Europei Centrale (CET), fără zile lipsă.

Pentru comparația cu alte active energetice adăugăm producția solară zilnică din România (ENTSO-E, date Transelectrica); contractul futures cel mai apropiat pe țițeiul Brent, în dolari americani (USD) pe baril, de pe Yahoo Finance; certificatul de emisii al Uniunii Europene (UE), *EU Allowance* (EUA), aproximat printr-un titlu tranzacționat la bursă, garantat cu certificate (*exchange-traded commodity*, ETC); prețul lunar al gazelor naturale pe hubul olandez Title Transfer Facility (TTF), din Pink Sheet al Băncii Mondiale, deoarece nu există o serie zilnică gratuită; și două acțiuni listate la Bursa de Valori București (BVB), OMV Petrom (SNP) și Hidroelectrica (H2O), ajustate cu dividendele, de la furnizorul de date eodhd.com (EODHD).

Două operații de curățare contează. Pentru Brent eliminăm prima zi de tranzacționare a fiecărei luni, în total 95 de zile, deoarece schimbarea contractului celui mai apropiat nu este o mișcare de preț. Seria EUA începe la 19 octombrie 2021.

## Definiția volatilității {h=41c1dbcf}

Volatilitatea arată cît de departe de prețul de azi ajunge, de obicei, prețul de mîine. Pentru energia electrică, prețul zilnic $P_t$ este prețul de bază al zilei $t$, adică media prețurilor orare ale zilei, în euro (EUR) pe megawatt-oră (MWh). Variația prețului se poate măsura în procente sau în euro:

$$ r_t = 100\ln\frac{P_t}{P_{t-1}}, \qquad \Delta P_t = P_t - P_{t-1}, $$ {#eq:returns}

unde $r_t$ este variația procentuală (o variație logaritmică, înmulțită cu 100), iar $\Delta P_t$ variația în EUR/MWh. Volatilitatea unui eșantion de $T$ zile este abaterea standard a variațiilor; ea se anualizează cu rădăcina pătrată a numărului de observații dintr-un an:

$$ \hat\sigma = \sqrt{\frac{1}{T-1}\sum_{t=1}^{T}(r_t-\bar r)^2}, \qquad \sigma_{\text{an}} = \hat\sigma\sqrt{A}, $$ {#eq:sigma}

unde $\bar r$ este variația medie din cele $T$ zile, $\hat\sigma$ volatilitatea zilnică, $\sigma_{\text{an}}$ volatilitatea anualizată, iar $A$ numărul de observații pe an: 365 pentru energie, unde licitația are loc în fiecare zi, și 252 pentru activele tranzacționate la bursă.

Pe datele din România pentru 2019–2026, abaterea standard a lui $r_t$ este de 28,3% pe zi, iar cea a lui $\Delta P_t$ de 30,9 EUR/MWh. Anualizată, după eliminarea efectului calendarului, volatilitatea este de 382%, față de 42% pentru Brent și 38% pentru EUA. Comparația trebuie citită cu grijă: variația prețului energiei nu este randamentul unui activ, deoarece energia nu se poate stoca, iar zilele $t$ și $t-1$ corespund unor produse diferite. Nimeni nu poate cumpăra energia de azi ca s-o vîndă mîine.

@practice Un furnizor care cumpără zilnic energie de pe PZU este expus exact acestei surprize zilnice.

## Variațiile zilnice alternează perioade calme și perioade agitate {h=c7b89fbb}

Graficul arată prețul de bază din România și variația lui procentuală zilnică pe întreaga perioadă. Se remarcă două trăsături. Mai întîi, mărimea variațiilor nu este constantă: lunile liniștite, în care prețul se mișcă cu cîteva procente pe zi, alternează cu perioade agitate, în care variațiile de 50% sau mai mari se succed. Apoi, perioadele agitate nu coincid numai cu criza energetică, cînd nivelul prețului a fost cel mai ridicat; unele dintre cele mai mari variații procentuale apar după criză, în 2023 și 2024.

Zilele extreme sînt sărbători și întreruperi ale calendarului obișnuit. Cea mai mare creștere, de +194%, a avut loc la 2 ianuarie 2023, imediat după sărbătoarea de Anul Nou; cea mai mare scădere, de −227%, la 25 decembrie 2023, ziua de Crăciun, cînd cererea s-a prăbușit. În total, 189 dintre cele 2 860 de variații zilnice depășesc 50% în valoare absolută. Asemenea valori ar fi de neconceput pentru o acțiune sau pentru un curs de schimb și arată de ce energia electrică are nevoie de instrumente de risc proprii.

@practice O lună calmă spune puțin despre luna următoare: riscul apare grupat.

@chart returns_ro
Sus: prețul zilnic de bază din România, în EUR/MWh; jos: variația logaritmică zilnică $r_t$, în procente; banda colorată marchează criza energetică, septembrie 2021 – decembrie 2022.

## Variațiile procentuale la prețuri apropiate de zero sau negative {h=16154762}

Logaritmul din @eq:returns cere prețuri pozitive, iar lîngă zero variații obișnuite devin procente uriașe. În literatura despre prețul energiei electrice se folosește adesea o alternativă, sinusul hiperbolic invers:

$$ \asinh(x)=\ln\bigl(x+\sqrt{x^2+1}\bigr), \qquad \Delta\asinh P_t\approx\Delta\ln P_t \ \text{ dacă } P_t\gg 1, $$ {#eq:asinh}

unde $\asinh$ este sinusul hiperbolic invers, definit pentru prețuri de orice semn, iar $\Delta$ variația de la ziua $t-1$ la ziua $t$. Departe de zero, cele două transformări coincid practic: de la 100 la 120 EUR/MWh, ambele dau 18,2%. Lîngă zero însă ambele explodează, deci transformarea nu rezolvă problema variațiilor procentuale; ea permite doar prețuri negative (Uniejewski, Weron & Ziel, 2018).

Pe datele noastre, prețul de bază din România a fost mereu pozitiv, cu un minim de 3,97 EUR/MWh, dar au existat 485 de ore cu prețuri negative, în 117 zile. În zona DE-LU, prețul de bază a fost zero sau negativ în 20 de zile, iar o trecere de la 0,95 la 92,91 EUR/MWh a dat $r_t$ = 458%, o valoare fără niciun sens economic. De aceea, în acest curs folosim pentru prețul de bază $r_t$, în procente, și $\Delta P_t$, în EUR/MWh, iar pentru prețurile orare numai EUR/MWh.

@practice O poziție se măsoară în MWh, deci riscul ei este în EUR/MWh. Procentele au sens doar departe de zero.

## Jumătate din variația zilnică vine din calendarul săptămînal {h=a75f1690}

O parte importantă a variației zilnice nu este deloc o surpriză. Cererea este mai mică la sfîrșit de săptămînă, astfel că prețul scade sîmbăta și duminica și crește din nou luni. Înainte de a măsura volatilitatea, eliminăm această parte previzibilă cu o ecuație a mediei:

$$ r_t=c+\sum_{k=1}^{7}\phi_k r_{t-k}+\sum_{j=2}^{7}\delta_j D_{j,t}+\varepsilon_t, $$ {#eq:mean}

unde $c$ este o constantă, $\phi_k$ ponderea variației de acum $k$ zile, $D_{j,t}$ o variabilă egală cu 1 dacă ziua $t$ este ziua $j$ a săptămînii (și 0 în rest), $\delta_j$ efectul acestei zile, iar $\varepsilon_t$ șocul, adică partea din variație care nu putea fi anticipată. Aceeași ecuație se estimează pentru $\Delta P_t$, iar șocul ei în EUR/MWh se notează $u_t$.

Panoul din stînga al graficului arată variația medie pentru fiecare zi a săptămînii: circa +38% lunea și circa −18%, respectiv −19% sîmbăta și duminica. Ecuația explică jumătate din varianța zilnică ($R^2$ = 0,50), iar abaterea standard scade de la 28,3% la 20,0%. Toate modelele de volatilitate de mai jos se aplică șocurilor $\varepsilon_t$ și, în EUR/MWh, șocurilor $u_t$, niciodată variației brute.

@practice Creșterea prețului de luni nu este un semnal de risc: ea trebuie prognozată, nu acoperită.

@chart dow_effect
Stînga: variația procentuală zilnică medie a prețului de bază din România, pe zile ale săptămînii; dreapta: abaterea standard a variației brute și a șocului rămas după ecuația mediei.

## Gruparea volatilității: autocorelația șocurilor și a pătratelor lor {h=bd5501cd}

După eliminarea calendarului, șocurile $\varepsilon_t$ se comportă ca o monedă corectă în privința semnului, dar nu și a mărimii. Graficul arată autocorelația șocurilor (stînga) și a pătratelor lor (dreapta), pentru decalaje de pînă la o lună. Primele sînt aproape toate în interiorul benzii așteptate în lipsa autocorelației; celelalte sînt pozitive și ies clar din bandă la multe decalaje. Două teste confirmă imaginea. Statistica Ljung–Box,

$$ Q(10)=T(T+2)\sum_{k=1}^{10}\frac{\hat\rho_k^2}{T-k}, $$ {#eq:ljungbox}

unde $\hat\rho_k$ este autocorelația de selecție de ordin $k$, iar $T$ numărul de zile, are valoarea 13,8 pentru $\varepsilon_t$ ($p$ = 0,18, fără autocorelație) și 120,0 pentru $\varepsilon_t^2$, mult peste valoarea critică de 18,31 la pragul de 5%. Testul multiplicatorului Lagrange pentru heteroscedasticitate condiționată autoregresivă (ARCH-LM), cu 10 decalaje, dă 93,7, cu $p<0{,}001$ (Engle, 1982).

Aceasta este gruparea volatilității, faptul stilizat central al cursului: direcția variației de mîine nu poate fi prevăzută pe baza datelor de azi, dar mărimea ei da.

@practice Un șoc mare astăzi anunță șocuri mari și în zilele următoare: acesta este subiectul cursului.

@chart acf_clust
Autocorelația șocurilor $\varepsilon_t$ (stînga) și a pătratelor lor $\varepsilon_t^2$ (dreapta), pentru decalaje de la 1 la 30 de zile, cu banda de 95% așteptată în lipsa autocorelației.

## Zilele extreme sînt mult mai frecvente decît prevede legea normală {h=7a759502}

Al doilea fapt stilizat este cel al cozilor groase. Șocurile $\varepsilon_t$ au un exces de aplatizare (*kurtosis*) de 20,0, în timp ce legea normală are zero, și o asimetrie de −1,69: cele mai mari variații sînt scăderi, în zilele de sărbătoare și în zilele cu vînt puternic, cînd cererea este mică sau producția eoliană mare. Există 15 șocuri dincolo de 4 abateri standard, față de 0,18 cîte ar fi de așteptat în ipoteza normalității.

Graficul arată, pe scară logaritmică, densitatea șocurilor standardizate cu un model GARCH, densitatea normală și o densitate Student cu $\nu$ = 4,3 grade de libertate. Curba normală coboară mult prea repede în cozi; curba Student urmărește datele mult mai bine. De aceea toate modelele din secțiunea următoare folosesc șocuri de tip Student (Bollerslev, 1987).

@practice O limită calculată cu distribuția normală este depășită mult mai des decît s-a planificat (cursul 4).

@chart tails
Densitatea șocurilor standardizate cu GARCH, $z_t$, ale prețului din România (bare, scară logaritmică), împreună cu densitatea normală (linie întreruptă) și densitatea Student cu $\nu$ = 4,3.

## Volatilitatea din 2022: similară în procente, de 4 ori mai mare în EUR/MWh {h=563fd144}

Alegerea unității de măsură nu este un detaliu tehnic. Graficul arată, an cu an, abaterea standard a șocurilor în procente și în EUR/MWh. În procente, anul 2022, anul crizei energetice, nu a fost mai volatil decît 2019: 18,5% față de 18,7%, un raport de 0,99. În EUR/MWh, aceiași ani dau 11,2 față de 45,8, un raport de 4,1, deoarece prețul mediu a crescut de la 50 la 265 EUR/MWh.

Ambele afirmații sînt corecte, dar răspund la întrebări diferite. Volatilitatea procentuală descrie mărimea relativă a variațiilor, iar volatilitatea în EUR/MWh descrie suma pe care o cîștigă sau o pierde o poziție de un megawatt-oră. În timpul crizei, mărimea relativă a variațiilor nu s-a schimbat, dar fiecare variație a costat de circa patru ori mai mult.

@practice Apelurile în marjă se plătesc în euro: garanțiile au crescut odată cu nivelul prețului, deși volatilitatea procentuală nu a crescut.

@chart vol_units
Abaterea standard a șocurilor zilnice ale prețului din România, pe ani, 2019–2026: în procente, $\varepsilon_t$ (stînga), și în EUR/MWh, $u_t$ (dreapta).

## Energia electrică este de circa 9 ori mai volatilă decît petrolul {h=60fec772}

Tabelul compară volatilitatea anualizată a șocurilor zilnice ale fiecărei serii, an cu an (în procente):

| Volatilitatea anualizată, % | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| Energie electrică, România | 358 | 349 | 287 | 354 | 543 | 444 | 310 | 346 |
| Energie electrică, Ungaria | 247 | 329 | 289 | 335 | 566 | 547 | 358 | 339 |
| EUA | – | – | – | 53 | 32 | 37 | 24 | 28 |
| Brent | 30 | 71 | 32 | 46 | 31 | 25 | 29 | 56 |
| Gaze TTF (lunar) | 42 | 82 | 58 | 100 | 78 | 38 | 28 | 63 |
| OMV Petrom (SNP) | 24 | 35 | 22 | 22 | 18 | 17 | 20 | 21 |
| Hidroelectrica (H2O) | – | – | – | – | 13 | 14 | 14 | 30 |

Pentru energia electrică, abaterea standard zilnică se înmulțește cu $\sqrt{365}$, iar pentru activele bursiere cu $\sqrt{252}$; pentru TTF avem doar medii lunare, scalate cu $\sqrt{12}$, ceea ce subestimează riscul. Liniuța arată că seria nu era încă disponibilă. Volatilitatea energiei electrice din România și din Ungaria este de cîteva sute de procente pe an, în fiecare an; pe întreaga perioadă, 382%, față de 42% pentru Brent, adică de circa 9 ori mai mare. Brent are vîrfuri în 2020 și în 2026, carbonul în 2022. Cele două acțiuni românești sînt mult mai liniștite decît mărfurile pe care le vînd companiile lor, deși volatilitatea Hidroelectrica s-a dublat în 2026.

@practice Nu comparați limitele unui birou de tranzacționare a energiei electrice cu cele ale unui birou de petrol, exprimate în același procent.

## @end

Volatilitatea este abaterea standard a șocului zilnic de preț, după eliminarea efectului calendarului, măsurată în procente sau în EUR/MWh. Pentru energia electrică din România ea este cu un ordin de mărime mai mare decît pentru petrol sau carbon, apare grupată, are cozi groase, iar în bani urmează nivelul prețului.

# Modelele din familia GARCH

Gruparea volatilității înseamnă că varianța de mîine poate fi prognozată din datele de azi. Secțiunea prezintă modelul GARCH, îl estimează prin metoda verosimilității maxime cu șocuri de tip Student, măsoară cît durează un șoc de volatilitate și adaugă două extensii asimetrice, în care creșterile și scăderile de preț au efecte diferite.

## GARCH actualizează varianța de mîine pe baza șocului de azi {h=4f37154c}

Un șoc mare ieri mărește varianța de azi; efectul se stinge apoi treptat, de la o zi la alta. Modelul GARCH(1,1) (Engle, 1982; Bollerslev, 1986) descrie acest mecanism printr-o relație de recurență:

$$ \sigma_t^2=\omega+\alpha\,\varepsilon_{t-1}^2+\beta\,\sigma_{t-1}^2, \qquad \varepsilon_t=\sigma_t z_t, $$ {#eq:garch}

unde $\sigma_t^2$ este varianța condiționată a zilei $t$, cunoscută în seara zilei $t-1$; $\omega>0$ este o constantă; $\alpha\ge0$ măsoară reacția la șocul de ieri, $\varepsilon_{t-1}$; $\beta\ge0$ este memoria varianței de ieri; iar $z_t$ este șocul standardizat, cu media 0 și varianța 1. Suma $\alpha+\beta$ se numește persistență; cînd este mai mică decît 1, varianța revine spre nivelul de lungă durată

$$ \bar\sigma^2=\frac{\omega}{1-\alpha-\beta}. $$ {#eq:longrun}

Pentru $\beta=0$, modelul devine modelul inițial cu heteroscedasticitate condiționată autoregresivă (ARCH) al lui Engle (1982).

Pe șocurile procentuale din România, estimațiile sînt $\hat\alpha$ = 0,308 și $\hat\beta$ = 0,438, deci $\hat\alpha+\hat\beta$ = 0,746, iar volatilitatea de lungă durată este $\bar\sigma$ = 20,4% pe zi. Pe șocurile în EUR/MWh, estimațiile sînt $\hat\alpha$ = 0,102 și $\hat\beta$ = 0,892, deci $\hat\alpha+\hat\beta$ = 0,994 și $\bar\sigma$ = 27,6 EUR/MWh pe zi. Cele două unități dau dinamici foarte diferite: în procente, volatilitatea reacționează puternic și uită repede; în EUR/MWh reacționează mai puțin, dar își amintește mult timp.

@practice În fiecare seară, GARCH dă departamentului de risc valoarea $\sigma$ pentru ziua următoare, pe baza datelor pe care le are deja.

## Parametrii se estimează prin verosimilitate maximă, cu șocuri Student {h=da43bbd6}

Alegem parametrii care fac cel mai probabile șocurile observate. Cu șocuri de tip Student, logaritmul funcției de verosimilitate este

$$ \ell(\omega,\alpha,\beta,\nu)=\sum_{t=1}^{T}\Bigl[\ln f_\nu\Bigl(\frac{\varepsilon_t}{\sigma_t}\Bigr)-\ln\sigma_t\Bigr], $$ {#eq:loglik}

unde $f_\nu$ este densitatea Student rescalată la varianța 1, cu $\nu>2$ grade de libertate, iar $\sigma_t$ urmează @eq:garch. Un $\nu$ mic înseamnă cozi groase; pentru $\nu\to\infty$ densitatea devine normală. Modelele se compară cu criteriul informațional bayesian (BIC), $\text{BIC}=k\ln T-2\hat\ell$, unde $k$ este numărul de parametri, iar $\hat\ell$ valoarea maximă a log-verosimilității; un BIC mai mic înseamnă un model mai bun. Formula completă se găsește în anexa A.

| GARCH(1,1), șocuri în % | normală | Student |
|---|---|---|
| log-verosimilitatea | −12 360,3 | −12 094,5 |
| BIC | 24 744,5 | 24 220,8 |
| $\hat\alpha+\hat\beta$ | 0,927 | 0,746 |
| înjumătățire, zile | 9,2 | 2,4 |
| $\hat\nu$ | – | 4,27 |

Modelul Student cîștigă detașat, cu un BIC mult mai mic. Diferența nu este doar statistică. Modelul normal tratează fiecare sărbătoare ca începutul unei perioade agitate de durată, așa că estimează o persistență mare (0,927) și un timp de înjumătățire al șocului de 9,2 zile. Modelul Student acceptă că unele zile sînt pur și simplu extreme; persistența lui este 0,746, iar timpul de înjumătățire 2,4 zile.

@practice Folosiți șocuri de tip Student: cu șocuri normale, limitele rămîn largi prea mult timp.

## GARCH: salturi scurte în procente, creștere persistentă în EUR/MWh {h=14721c04}

Graficul arată volatilitatea condiționată zilnică $\hat\sigma_t$ a celor două modele GARCH(1,1)-t pe întreaga perioadă. În procente, volatilitatea este formată din salturi scurte, peste un nivel de bază destul de stabil; cel mai mare salt, 156% pe zi, a avut loc la 26 decembrie 2023, imediat după scăderea de Crăciun, și a dispărut în cîteva zile. În EUR/MWh imaginea este a unui platou lung: volatilitatea a crescut pe parcursul anului 2021, a atins maximul de 85,7 EUR/MWh la 4 septembrie 2022, în plină criză, și a scăzut lent în 2023. Minimul, 8,8 EUR/MWh, a fost înregistrat la 6 iulie 2019, iar la sfîrșitul perioadei valoarea era 27,4.

Cele două curbe spun povești diferite pentru că măsoară lucruri diferite. Curba procentuală răspunde la întrebarea „cît de mare este variația de mîine raportată la preț?”, iar cea în EUR/MWh la întrebarea „cîți euro pe megawatt-oră poate costa variația de mîine?”.

@practice Garanțiile unui furnizor urmează curba în EUR/MWh, nu pe cea procentuală.

@chart cond_vol
Volatilitatea condiționată zilnică GARCH(1,1)-t a prețului din România: pe variațiile procentuale (sus) și pe variațiile în EUR/MWh (jos), cu perioada crizei energetice marcată.

## Timpul de înjumătățire arată în cîte zile dispare jumătate din șoc {h=b1e2663b}

Varianța suplimentară creată de un șoc se reduce în fiecare zi cu factorul $\alpha+\beta$. Aplicînd media condiționată în @eq:garch obținem

$$ \E_t\bigl[\sigma^2_{t+h}\bigr]-\bar\sigma^2=(\alpha+\beta)^{h-1}\bigl(\sigma^2_{t+1}-\bar\sigma^2\bigr), $$ {#eq:decay}

unde $\E_t$ este media condiționată de datele pînă în ziua $t$, iar $h$ numărul de zile înainte. Timpul de înjumătățire $h_{1/2}$ este numărul de zile după care a dispărut jumătate din varianța suplimentară:

$$ h_{1/2}=\frac{\ln 0{,}5}{\ln(\alpha+\beta)}. $$ {#eq:halflife}

Deducerea formulei se găsește în anexa B. Tabelul dă persistența și timpul de înjumătățire pentru fiecare serie, toate din modelul GARCH(1,1)-t:

| GARCH(1,1)-t | $\hat\alpha+\hat\beta$ | $h_{1/2}$ | unitatea |
|---|---|---|---|
| România, % | 0,746 | 2,4 | zile |
| România, EUR/MWh | 0,994 | 113,5 | zile |
| Ungaria, % | 0,881 | 5,5 | zile |
| Brent | 0,973 | 25,6 | zile lucrătoare |
| EUA | 0,992 | 82,8 | zile lucrătoare |
| OMV Petrom | 0,934 | 10,2 | zile lucrătoare |

Eșantioanele încep în 2019 pentru energia electrică, Brent și OMV Petrom și la 19 octombrie 2021 pentru EUA. Timpul de înjumătățire este foarte sensibil la persistență cînd aceasta se apropie de 1: trecerea de la 0,973 la 0,992 îl face de peste trei ori mai mare.

@practice După un șoc pe piața petrolului, mențineți limite mai largi circa 5 săptămîni; după un șoc procentual al prețului energiei electrice, doar cîteva zile.

## Timpul de înjumătățire al șocurilor de volatilitate, pe piețe {h=bd846704}

În cursul 1 ne-am întrebat cît timp trebuie să mențină departamentul de risc limite mai largi după un șoc. Graficul răspunde, reprezentînd $100(\hat\alpha+\hat\beta)^h$, procentul din varianța suplimentară care mai rămîne la $h$ zile după un șoc, pentru fiecare serie; timpii de înjumătățire apar în paranteze, în legendă.

Pentru Brent, timpul de înjumătățire este de 26 de zile lucrătoare, circa 5 săptămîni; pentru EUA, de 83 de zile lucrătoare, circa 17 săptămîni. Acțiunile OMV Petrom se află între ele, la circa 10 zile lucrătoare. Pentru energia electrică din România, răspunsul depinde de unitatea de măsură: un șoc procentual se înjumătățește în 2,4 zile, dar un șoc în EUR/MWh are nevoie de 114 zile, deoarece volatilitatea în bani urmează nivelul prețului, iar acesta se modifică lent. O parte din această memorie lungă vine din amestecarea anilor calmi cu anii de criză într-un singur eșantion, după cum arată secțiunea următoare.

@practice După un șoc, departamentul de risc menține limite mai largi săptămîni întregi, nu doar cîteva zile, cum anunța cursul 1.

@chart halflife
Procentul din varianța suplimentară rămas la $h$ zile după un șoc, $100(\hat\alpha+\hat\beta)^h$, pentru energia electrică din România în procente și în EUR/MWh, Brent, EUA și OMV Petrom (SNP); timpii de înjumătățire în paranteze; linia punctată marchează 50%.

## GARCH asimetric: creșterile și scăderile nu au același efect {h=503e1d92}

În @eq:garch, o creștere și o scădere de aceeași mărime au același efect asupra varianței de mîine. Două extensii renunță la această ipoteză. Modelul Glosten–Jagannathan–Runkle (GJR) adaugă un termen pentru șocurile negative:

$$ \sigma_t^2=\omega+(\alpha+\gamma I_{t-1})\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2, $$ {#eq:gjr}

unde $I_{t-1}=1$ dacă $\varepsilon_{t-1}<0$ și 0 în rest. Dacă $\gamma>0$, scăderile cresc mai mult volatilitatea, așa-numitul efect de levier al acțiunilor; dacă $\gamma<0$, creșterile o fac. Modelul GARCH exponențial (EGARCH) al lui Nelson (1991) lucrează cu logaritmul varianței:

$$ \ln\sigma_t^2=\omega+\alpha\bigl(|z_{t-1}|-\sqrt{2/\pi}\bigr)+\gamma z_{t-1}+\beta\ln\sigma_{t-1}^2, $$ {#eq:egarch}

unde $z_{t-1}$ este șocul standardizat de ieri, iar $\sqrt{2/\pi}$ media lui $|z|$ în cazul normal. Aici convenția de semn este inversă: $\gamma<0$ înseamnă că scăderile cresc mai mult volatilitatea.

Pe șocurile procentuale din România, GJR dă $\hat\gamma$ = 0,225 ($t$ = 2,9), iar EGARCH $\hat\gamma$ = −0,083 ($t$ = −3,9): scăderile cresc mai mult volatilitatea, un efect de revenire după o scădere. În EUR/MWh semnul se inversează: GJR dă $\hat\gamma$ = −0,127 ($t$ = −6,4), iar EGARCH $\hat\gamma$ = 0,104 ($t$ = 7,2), deci creșterile măresc mai mult volatilitatea. Este efectul de levier invers, tipic pentru mărfuri (Knittel & Roberts, 2005).

@practice Pentru un cumpărător, direcția periculoasă este în sus: după un salt de preț, lărgiți limitele mai mult decît după o scădere.

## În EUR/MWh, creșterile de preț măresc mai mult volatilitatea {h=7d82978e}

Curba de impact a șocurilor (*news impact curve*; Engle & Ng, 1993) arată valoarea $\sigma$ din ziua următoare, dată de modelul GJR, în funcție de șocul de azi, toate celelalte mărimi fiind fixate la nivelul lor de lungă durată. Graficul o desenează separat pentru scăderi și pentru creșteri, în procente și în EUR/MWh.

Pentru un șoc de 61 EUR/MWh, adică de circa două abateri standard de lungă durată, $\sigma$ din ziua următoare este de 37,6 EUR/MWh după o creștere și de 30,6 după o scădere. În procente ordinea se inversează: pentru un șoc de 40%, $\sigma$ este de 30,3% după o scădere și de 23,7% după o creștere. Cele două rezultate nu se contrazic. O creștere în EUR/MWh ridică nivelul prețului, iar la un nivel mai mare aceeași variație procentuală costă mai mulți euro; o scădere procentuală este adesea o cădere de sărbătoare, urmată de o revenire de mărime asemănătoare.

@practice Un consumator industrial care cumpără la prețul spot trebuie să reacționeze mai repede la creșteri decît la scăderi.

@chart nic
Curbele de impact ale șocurilor pentru modelul GJR(1,1)-t: $\sigma_t$ din ziua următoare în funcție de șocul de ieri, în procente (stînga) și în EUR/MWh (dreapta), separat după o scădere și după o creștere.

## Volatilitatea în EUR/MWh crește odată cu nivelul prețului {h=8da9e58a}

De ce urmează volatilitatea în bani nivelul prețului? La prețuri mari, curba ofertei, adică ordinea de merit a centralelor, este mai abruptă, așa că același șoc al cererii mută mai mult prețul. Graficul reprezintă, pentru fiecare lună, abaterea standard a șocurilor în EUR/MWh în funcție de prețul mediu, ambele pe scară logaritmică, cu culori diferite pentru fiecare an.

Regresia lui $\ln\hat\sigma_m(u)$ pe $\ln\bar P_m$, unde $\hat\sigma_m(u)$ este abaterea standard a șocurilor $u_t$ din luna $m$, iar $\bar P_m$ prețul mediu al lunii, estimată pe 94 de luni, dă o pantă de 0,75, cu $R^2$ = 0,76. Cum ambele variabile sînt logaritmate, panta este o elasticitate: volatilitatea în EUR/MWh crește aproape proporțional cu prețul. Aceeași regresie pentru șocurile procentuale are panta 0,01 și $R^2$ = 0,00. Volatilitatea procentuală nu depinde de nivelul prețului; cea în EUR/MWh aproape că se scalează cu el.

@practice Stabiliți limitele în EUR/MWh ca procent din prețul contractelor la termen, nu ca sumă fixă.

@chart vol_level
Abaterea standard lunară a șocurilor în EUR/MWh în funcție de prețul mediu lunar, ambele pe scară logaritmică, colorate după an, cu dreapta de regresie log-log.

## Importanța relativă a cozilor groase și a asimetriei {h=aa8933aa}

Tabelul pune alături cele șase modele: trei ecuații ale varianței (GARCH, GJR, EGARCH), fiecare cu șocuri normale și cu șocuri Student, în ambele unități de măsură. Pentru fiecare dă persistența, BIC și valoarea $p$ a testului Ljung–Box pentru pătratele șocurilor standardizate, $z_t^2$.

| Modelul | $\alpha+\beta$ (%) | BIC (%) | $p$, $z^2$ (%) | $\alpha+\beta$ (EUR) | BIC (EUR) | $p$, $z^2$ (EUR) |
|---|---|---|---|---|---|---|
| GARCH, normal | 0,927 | 24 744,5 | 0,328 | 0,998 | 24 573,2 | 0,000 |
| GARCH, Student | 0,746 | 24 220,8 | 0,367 | 0,994 | 24 450,7 | 0,000 |
| GJR, normal | 0,651 | 24 690,7 | 0,151 | 0,998 | 24 525,1 | 0,000 |
| GJR, Student | 0,727 | 24 214,1 | 0,243 | 0,996 | 24 411,7 | 0,000 |
| EGARCH, normal | 0,903 | 24 691,4 | 0,529 | 0,995 | 24 518,0 | 0,000 |
| EGARCH, Student | 0,831 | 24 219,2 | 0,532 | 0,995 | 24 403,9 | 0,000 |

Orice model cu șocuri Student îl depășește pe oricare model cu șocuri normale. Cel mai bun după BIC este GJR-t în procente și EGARCH-t în EUR/MWh, dar cîștigul adus de asimetrie este mic în comparație cu cel adus de cozile groase; criteriul informațional Akaike (AIC) dă aceeași ordine (anexa C). Coloana de diagnostic arată o diferență între unități: în procente, în $z_t^2$ nu mai rămîne grupare, în timp ce în EUR/MWh rămîne ($p<0{,}001$). O singură ecuație nu poate urmări în același timp mișcarea lentă a nivelului prețului și șocurile zilnice.

@practice Mai întîi modelați corect cozile distribuției, apoi asimetria.

## @end

Modelul GARCH prognozează varianța de mîine pe baza șocului de azi și a varianței de ieri. Cu șocuri Student, un șoc procentual al prețului energiei din România se înjumătățește în circa două zile, un șoc al petrolului în circa 5 săptămîni, iar în EUR/MWh creșterile măresc volatilitatea mai mult decît scăderile.

# Regimuri de volatilitate și criza energetică

În modelul GARCH volatilitatea se modifică treptat; criza energetică a semănat mai degrabă cu trecerea într-o altă stare. Secțiunea estimează un model Markov cu două regimuri, datează perioadele agitate din 2019–2026 și arată cum depinde persistența GARCH de perioadă și de unitatea de măsură.

## Modelul Markov cu schimbare de regim separă regimul calm de cel agitat {h=e78e804d}

Modelul presupune două stări neobservate, una calmă și una agitată, fiecare cu volatilitatea ei, și o probabilitate fixă de trecere de la una la alta:

$$ u_t=\mu_{s_t}+\sigma_{s_t}\eta_t, \qquad \Pr(s_t=j\mid s_{t-1}=i)=p_{ij}, $$ {#eq:ms}

unde $u_t$ este șocul în EUR/MWh, $s_t$ regimul din ziua $t$ (calm sau agitat), $\mu_{s_t}$ și $\sigma_{s_t}$ media și abaterea standard din acel regim, $\eta_t$ o variabilă normală standard, iar $p_{ij}$ probabilitatea de trecere din regimul $i$ în regimul $j$. Parametrii se estimează prin verosimilitate maximă, cu filtrul lui Hamilton (1989) (anexa D). Durata medie a unei șederi în regimul $i$ este

$$ \text{durata medie a regimului } i=\frac{1}{1-p_{ii}}. $$ {#eq:duration}

Pentru fiecare zi, modelul dă probabilitatea regimului agitat. Pe șocurile în EUR/MWh din România, regimul calm are $\sigma$ = 12,9 și $p_{11}$ = 0,986, deci durează în medie circa 69 de zile; regimul agitat are $\sigma$ = 41,9 și $p_{22}$ = 0,957, circa 23 de zile, și cuprinde 24% din zile. Estimat pe șocurile procentuale, regimul agitat durează doar 3,5 zile: în procente el surprinde salturi izolate, nu perioade lungi.

@practice O probabilitate a regimului agitat peste 0,5 cere revizuirea acoperirii riscului și a garanțiilor.

## Regimurile de volatilitate în timpul crizei și în 2026 {h=ca5733e2}

Graficul pune prețul de bază zilnic deasupra probabilității netezite a regimului agitat. Criza energetică apare ca un singur bloc lung: cel mai lung episod agitat a durat de la 15 iunie 2022 pînă la 31 ianuarie 2023, adică 231 de zile. Înainte de criză, regimul calm a dominat aproape complet, iar după ea modelul intră și iese din regimul agitat pentru perioade mai scurte.

Ponderea zilelor agitate pe ani rezumă această istorie: 86% în 2022, 6% în 2025 și 33% în 2026, cu 48% începînd din iulie 2026. Anul 2026 nu este așadar un an liniștit, dar nici o repetare a anului 2022: episoadele agitate sînt scurte și alternează cu perioade calme.

@practice Transelectrica și furnizorii pot folosi probabilitatea regimului agitat ca avertizare timpurie pentru costurile de echilibrare.

@chart ms_regime
Sus: prețul zilnic de bază din România, în EUR/MWh; jos: probabilitatea netezită a regimului agitat, din modelul Markov cu două regimuri pe șocurile în EUR/MWh.

## Persistența depinde de perioadă și de unitatea de măsură {h=4200abf2}

Dacă volatilitatea trece de la un regim la altul, un model GARCH estimat pe toate regimurile confundă aceste treceri cu o memorie lungă (Lamoureux & Lastrapes, 1990). Tabelul reestimează modelul GARCH(1,1)-t pe trei subperioade:

| GARCH(1,1)-t pe | $\hat\alpha+\hat\beta$ (%) | $h_{1/2}$ (%) | $\hat\alpha+\hat\beta$ (EUR) | $h_{1/2}$ (EUR) | $\bar\sigma$, EUR/MWh |
|---|---|---|---|---|---|
| 2019–2020 (calm) | 0,568 | 1,2 | 0,208 | 0,4 | 10,5 |
| 2021–2022 (criză) | 0,882 | 5,5 | 1,000 | $\infty$ | – |
| 2023 – octombrie 2026 | 0,727 | 2,2 | 0,927 | 9,1 | 20,9 |
| întreaga perioadă | 0,746 | 2,4 | 0,994 | 113,5 | 27,6 |

În EUR/MWh diferențele sînt spectaculoase. În 2019–2020 un șoc se înjumătățește în mai puțin de o zi. În criză, $\hat\alpha+\hat\beta$ ajunge la 1, deci timpul de înjumătățire este infinit și nu există un nivel de lungă durată, deoarece volatilitatea a crescut lună de lună odată cu prețul. După criză, timpul de înjumătățire este de 9,1 zile. Valoarea de 113,5 zile pentru întreaga perioadă amestecă aceste regimuri, iar amestecarea regimurilor supraestimează persistența. În procente, persistența rămîne mult sub 1 în fiecare perioadă: criza a mutat nivelul prețului, nu volatilitatea procentuală.

@practice Reestimați modelul după o schimbare de regim: un model estimat pe perioada crizei menține limitele largi prea mult timp.

## @end

Criza din 2021–2022 a fost, în EUR/MWh, un singur regim agitat lung, în timp ce anul 2026 alternează între regimuri. Un model GARCH estimat peste mai multe regimuri supraestimează persistența, de aceea trebuie reestimat după o schimbare de regim.

# Volatilitatea intrazilnică, din prețurile orare

Prețul de bază zilnic ascunde ce se întîmplă în cursul zilei. Secțiunea măsoară variația prețurilor orare în fiecare zi de livrare, arată cum a crescut-o producția solară și o prognozează cu un model simplu cu memorie lungă.

## Variația intrazilnică măsoară cît se mișcă prețul în cursul zilei {h=9dd2fab9}

Adunăm pătratele variațiilor de la o oră la alta din aceeași zi de livrare și extragem rădăcina pătrată: din această variație cîștigă o baterie sau un consumator flexibil. O numim variația intrazilnică realizată (RV):

$$ \text{RV}_d=\sqrt{\sum_{h=1}^{H_d-1}\bigl(P_{d,h}-P_{d,h-1}\bigr)^2}, \qquad \text{RV relativă}_d=\frac{\text{RV}_d}{\bar P_d}, $$ {#eq:rv}

unde $P_{d,h}$ este prețul orei $h$ din ziua $d$ (începînd cu 1 octombrie 2025, cînd piața a trecut la sferturi de oră, media celor patru sferturi de oră), $H_d$ numărul de ore din zi, 24, respectiv 23 sau 25 în cele 8 + 8 zile cu schimbarea orei, iar $\bar P_d$ prețul zilnic de bază. RV se măsoară în EUR/MWh, deoarece prețurile orare pot fi negative.

Media anuală a RV a fost de 36 EUR/MWh în 2019, 186 în 2022 și 135 în 2026. Raportată la preț, mediana a fost de 0,64 în 2019 și de 1,24 în 2024. Este un risc diferit de cel zilnic: corelația dintre $\text{RV}_d$ și șocul zilnic absolut $|u_t|$ este de doar 0,46. Nu este nici volatilitatea realizată din finanțe (Andersen & Bollerslev, 1998), care însumează randamentele intrazilnice ale unui singur activ; aici cele 24 de ore sînt 24 de produse diferite.

@practice Venitul unui investitor în baterii depinde de variația intrazilnică, nu de prețul mediu zilnic.

## Producția solară a mărit variația prețului în cursul zilei {h=8090209b}

Graficul compară mediana lunară a variației intrazilnice relative cu producția solară medie din România. Variația relativă a fost de 0,64 în 2019, a atins maximul de 1,24 în 2024 și a fost de 1,01 în 2026. În aceeași perioadă, producția solară medie a crescut de la 157 MW în 2019 la 593 MW în ianuarie–octombrie 2026, iar corelația lunară dintre cele două serii este 0,46.

Mecanismul este simplu. Centralele solare produc la prînz, ceea ce împinge în jos prețurile din mijlocul zilei, uneori sub zero, în timp ce prețurile de seară, după apusul soarelui, rămîn ridicate. Diferența dintre orele cele mai ieftine și cele mai scumpe crește, iar odată cu ea și variația de la o oră la alta.

@practice Mai multă producție solară înseamnă prețuri mici la prînz și mari seara: argumentul economic pentru stocare.

@chart rv_solar
Sus: mediana lunară a variației intrazilnice raportate la prețul zilei; jos: producția solară medie lunară din România, în megawați (MW).

## Variația intrazilnică are memorie lungă: zi, săptămînă, lună {h=031be1c9}

Trei medii pe orizonturi diferite dau o regresie simplă cu memorie lungă, modelul autoregresiv eterogen (HAR) al lui Corsi (2009):

$$ \ln\text{RV}_d=b_0+b_D\ln\text{RV}_{d-1}+\frac{b_W}{7}\sum_{j=1}^{7}\ln\text{RV}_{d-j}+\frac{b_M}{30}\sum_{j=1}^{30}\ln\text{RV}_{d-j}+e_d, $$ {#eq:har}

unde $b_0$ este o constantă, $b_D$, $b_W$ și $b_M$ sînt ponderile zilei de ieri, ale ultimelor 7 zile și ale ultimelor 30 de zile, iar $e_d$ este eroarea. Modelul se estimează prin metoda celor mai mici pătrate (OLS). Deoarece este estimat în logaritmi, prognoza în EUR/MWh este $\exp(\widehat{\ln\text{RV}}_d+s^2/2)$, unde $s^2$ este varianța erorilor; termenul $s^2/2$ corectează deplasarea care apare cînd aplicăm exponențiala unei medii.

Estimate pe datele de dinaintea anului de test, ponderile sînt $\hat b_D$ = 0,40, $\hat b_W$ = 0,36 și $\hat b_M$ = 0,22, toate cu statistici $t$ peste 6, iar $R^2$ = 0,82. Ziua de ieri contează cel mai mult, dar ultima săptămînă și ultima lună au împreună o pondere mai mare decît ea. În anul de test, eroarea absolută medie (MAE) a modelului HAR este de 35,6 EUR/MWh, față de 39,1 pentru prognoza naivă, care presupune că mîine va fi ca ieri, adică cu 9,1% mai puțin.

@practice O baterie își programează mentenanța în zilele cu variație prognozată mică.

## Prognozele HAR urmăresc variația, dar nu și salturile izolate {h=6f419835}

Graficul arată, pentru anul de test 1 noiembrie 2025 – 31 octombrie 2026, variația intrazilnică realizată în fiecare zi și prognoza HAR făcută în ziua precedentă. Modelul se reestimează zilnic pe datele disponibile în ziua $d-1$, deci prognoza nu folosește nicio informație din viitor. Eroarea absolută medie este de 35,6 EUR/MWh.

Prognoza urmărește bine mișcările lente ale variației intrazilnice, creșterea sezonieră din primăvară și vară și săptămînile mai liniștite de iarnă, dar nu poate anticipa salturile izolate. O prognoză construită din medii ale trecutului este netedă prin construcție.

@practice Folosiți prognoza pentru planificare și păstrați rezerve pentru salturile pe care nu le poate anticipa.

@chart har_fc
Variația intrazilnică realizată $\text{RV}_d$, în EUR/MWh, în anul de test (gri) și prognoza HAR făcută în ziua $d-1$ (linia colorată).

## @end

Variația intrazilnică a prețurilor orare este un risc distinct de volatilitatea zilnică, determinat în mare măsură de producția solară. Ea are memorie lungă, iar o regresie HAR o prognozează mai bine decît valoarea de ieri, deși nu îi poate anticipa salturile izolate.

# Prognoza și evaluarea volatilității

Un model de volatilitate este util numai dacă prognozează bine în zile pe care nu le-a văzut. Secțiunea explică cum se evaluează prognoza unei mărimi care nu se observă niciodată direct, compară cinci modele pe un an de test cu un test de semnificație și arată cum se comportă prognozele de volatilitate pe mai multe săptămîni.

## Prognoza volatilității se evaluează față de o aproximare zgomotoasă {h=6d4f9456}

Volatilitatea adevărată nu se observă niciodată. Comparăm prognoza cu o aproximare zgomotoasă, pătratul șocului, folosind o funcție de pierdere care ordonează totuși corect modelele. Două funcții sînt frecvent folosite, funcția de pierdere de tip cvasi-verosimilitate (QLIKE) și eroarea pătratică medie (MSE):

$$ \text{QLIKE}_t=\frac{\varepsilon_t^2}{\hat\sigma_t^2}-\ln\frac{\varepsilon_t^2}{\hat\sigma_t^2}-1, \qquad \text{MSE}_t=\bigl(\varepsilon_t^2-\hat\sigma_t^2\bigr)^2, $$ {#eq:qlike}

unde $\varepsilon_t$ este șocul zilei $t$, în afara eșantionului, iar $\hat\sigma_t^2$ prognoza varianței făcută în ziua $t-1$. Ambele funcții ordonează corect modelele în medie, chiar și cu o aproximare zgomotoasă (Patton, 2011), dar MSE este dominată de cîteva zile extreme, în timp ce QLIKE penalizează erorile în termeni relativi. Două modele se compară cu testul Diebold–Mariano (DM), aplicat diferențelor zilnice dintre pierderile lor.

Un exemplu arată diferența. Să presupunem că $\sigma$ adevărat este 20. O prognoză de 10 are QLIKE = 1,61; o prognoză de 40 are QLIKE = 0,64. Subestimarea riscului costă de 2,5 ori mai mult decît supraestimarea, ceea ce își dorește un manager de risc; MSE spune contrariul, pentru că ridică la pătrat valorile mari.

Cadrul de evaluare: anul de test este 1 noiembrie 2025 – 31 octombrie 2026, iar cele cinci modele se reestimează zilnic pe datele pînă în ziua $t-1$ (Hansen & Lunde, 2005).

@practice Cereți furnizorului modelului de risc valoarea QLIKE pe zilele dumneavoastră, în afara eșantionului.

## Prognozele de tip GARCH comparate cu volatilitatea istorică pe 30 de zile {h=ae26c3fc}

Tabelul compară prognozele varianței pentru ziua următoare date de cinci modele pe cele 365 de zile ale anului de test: varianța istorică pe 30 de zile, o medie mobilă cu ponderi exponențiale (EWMA), ca în RiskMetrics (1996), și cele trei modele GARCH cu șocuri Student.

| Varianța pentru ziua următoare | QLIKE, % | $p$ față de 30 de zile | QLIKE, EUR | $p$ față de 30 de zile |
|---|---|---|---|---|
| varianța istorică pe 30 de zile | 1,523 | – | 1,428 | – |
| EWMA | 1,499 | 0,082 | 1,398 | 0,026 |
| GARCH(1,1)-t | 1,459 | 0,170 | 1,378 | 0,040 |
| GJR(1,1)-t | 1,445 | 0,145 | 1,357 | 0,032 |
| EGARCH(1,1)-t | 1,452 | 0,120 | 1,349 | 0,027 |

Un QLIKE mai mic înseamnă un model mai bun. Valorile $p$ provin dintr-un test DM unilateral față de varianța istorică pe 30 de zile, cu eroarea standard Newey–West calculată cu 7 decalaje (Diebold & Mariano, 1995). Cel mai bun model este GJR-t în procente, cu o pierdere cu 5,1% sub cea a varianței istorice, și EGARCH-t în EUR/MWh, cu 5,5% sub ea.

La pragul de 5%, în EUR/MWh toate modelele de tip GARCH, ca și EWMA, sînt semnificativ mai precise decît varianța istorică; în procente, niciunul. Modelele asimetrice nu sînt semnificativ mai bune decît modelul GARCH-t simplu ($p$ = 0,08). Cîștigurile sînt modeste, de cîteva procente din pierdere, dar sînt sistematice.

@practice Folosiți GARCH-t ca model implicit: modelele asimetrice aduc puțin în afara eșantionului.

## Volatilitatea GARCH și cea istorică pe 30 de zile în jurul celui mai mare șoc {h=499cbf5d}

Graficul arată de ce cîștigă GARCH. El reprezintă, pentru anul de test, șocul absolut din fiecare zi, în EUR/MWh, împreună cu prognoza GARCH-t și cu prognoza istorică pe 30 de zile, ambele făcute în ziua precedentă. Cel mai mare șoc din anul de test a fost de +124 EUR/MWh, la 22 ianuarie 2026. A doua zi, $\hat\sigma$ GARCH a crescut de la 25 la 47 EUR/MWh, în timp ce prognoza istorică a urcat doar la 33, deoarece o singură zi are o pondere de o treizecime în fereastra ei.

Varianța istorică și uită brusc. După 30 de zile, șocul iese din fereastră, iar prognoza istorică scade într-o singură zi de la 32 la 23 EUR/MWh, fără nicio informație nouă în acea zi. GARCH, în schimb, lasă șocul să se stingă treptat, cu rata $\alpha+\beta$.

@practice O limită care se modifică brusc la 30 de zile după un șoc, fără nicio informație nouă, trădează un model cu fereastră istorică.

@chart fc_test
Șocul zilnic absolut $|u_t|$, în EUR/MWh, în anul de test (bare gri), împreună cu prognoza GARCH-t $\hat\sigma_t$ făcută în $t-1$ și cu prognoza istorică pe 30 de zile (linie întreruptă).

## Pe mai multe săptămîni, volatilitatea revine spre nivelul normal {h=33d5af5b}

O volatilitate mare se așteaptă să scadă, iar una mică să crească; de aceea regula obișnuită $\sigma\sqrt{h}$ greșește riscul pe $h$ zile. Prognoza GARCH pentru $h$ zile înainte este

$$ \hat\sigma^2_{T+h\mid T}=\bar\sigma^2+(\alpha+\beta)^{h-1}\bigl(\hat\sigma^2_{T+1}-\bar\sigma^2\bigr), $$ {#eq:multistep}

unde $T$ este ziua prognozei, $\hat\sigma^2_{T+1}$ prognoza varianței pentru ziua următoare, iar $\bar\sigma^2$ varianța de lungă durată din @eq:longrun. Pentru randamente fără autocorelație, cum sînt cele ale petrolului sau carbonului, dar nu și ale energiei electrice, varianța sumei pe $h$ zile este suma prognozelor zilnice:

$$ \Var_T\Bigl(\sum_{k=1}^{h}r_{T+k}\Bigr)=\sum_{k=1}^{h}\hat\sigma^2_{T+k\mid T}\ \ne\ h\,\hat\sigma^2_{T+1}, $$ {#eq:aggvar}

unde $\Var_T$ este varianța condiționată de datele pînă în ziua $T$, iar $r_{T+k}$ randamentul din ziua $T+k$. Banda de 90% este $\pm1{,}645$ înmulțit cu rădăcina pătrată a acestei varianțe.

Brent în 2026 ilustrează ambele direcții. La 9 aprilie 2026, după șocul petrolier din primăvară, $\hat\sigma_{T+1}$ era de 93% pe an, față de un nivel de lungă durată de 39%. Banda pe 20 de zile dată de GARCH era de ±38,5%, în timp ce $\sigma\sqrt{20}$ dădea ±43,1%, adică o bandă prea largă cu 12%, pentru că ignora calmarea așteptată. La 30 octombrie 2026, cu piața din nou calmă, $\hat\sigma_{T+1}$ era de 32%, sub nivelul de lungă durată de 40%, iar acum $\sigma\sqrt{20}$ dădea o bandă prea îngustă.

@practice Un consumator industrial care își face bugetul de combustibil pentru luna următoare adună prognozele GARCH, nu scalează $\sigma$ de azi.

## @end

Prognozele de volatilitate se compară cu QLIKE și cu testul DM, pe zile pe care modelul nu le-a văzut. Modelele de tip GARCH sînt mai precise decît varianța istorică pe 30 de zile, semnificativ în EUR/MWh, iar pe mai multe săptămîni prognoza revine spre nivelul de lungă durată, astfel că regula $\sigma\sqrt{h}$ greșește în ambele direcții.

# Studiu de caz: prețul energiei electrice din România în 2026

Studiul de caz aplică instrumentele cursului la întrebarea pe care și-a pus-o fiecare companie energetică din România în toamna lui 2026: este creșterea prețurilor o nouă criză, ca în 2022? Analizăm prețurile și volatilitatea din 2026, testăm banda GARCH de o zi pe anul de test, stabilim limitele pentru noiembrie 2026 și replicăm un studiu despre acțiunile energetice și petrol.

## Studiu de caz: nivelul prețurilor și volatilitatea în 2026, comparativ cu 2022 {h=bbb122f1}

Prețurile au crescut puternic în 2026. Media lunară a prețului de bază din România a urcat de la 150 EUR/MWh în ianuarie la 239 în octombrie. Brentul a crescut de la 69 USD pe baril în februarie la 100 în martie și la 108 în octombrie, iar gazele TTF de la 32 la 87 EUR/MWh între februarie și octombrie.

Volatilitatea spune o poveste mai nuanțată. În procente, aproape nimic nu s-a schimbat: $\hat\sigma$ lunar mediu a fost de 17,4% în 2026, 17,4% în 2022 și 16,6% în 2019. În EUR/MWh, volatilitatea s-a dublat față de 2019, de la 10,9 la 21,8, dar luna cu valoarea maximă din 2026, 34,7 în ianuarie, rămîne mult sub maximul din 2022, 65,1 în septembrie 2022. Regimul agitat a cuprins 33% din zilele anului 2026, față de 86% în 2022, iar probabilitatea lui era de 0,47 la 31 octombrie 2026. Pentru Brent, volatilitatea GARCH a ajuns la 100% pe an la 9 aprilie 2026, față de o medie de 30% în 2025.

Concluzia: 2026 este un șoc al nivelului prețului, cu un regim agitat în circa jumătate din zile începînd din iulie, dar nu (încă) o criză de tipul celei din 2022.

@practice Un furnizor care reînnoiește contractele în noiembrie 2026 trebuie să includă în preț riscul asociat nivelului mai ridicat, nu unui nou regim de volatilitate.

## Studiu de caz: banda GARCH-t de o zi a fost corectă în anul de test {h=a2f03264}

Un departament de risc transformă prognoza volatilității într-o bandă: prețul prognozat plus sau minus cuantila distribuției Student înmulțită cu $\hat\sigma_t$, totul stabilit în ziua $t-1$. Pentru o bandă de 90%, cam o zi din zece ar trebui să cadă în afara ei. Graficul arată banda și prețul efectiv în anul de test.

Banda a funcționat. Dintre cele 365 de zile, 38 au căzut în afara benzii, adică 10,4%, față de 10% așteptat. Depășirile s-au distribuit uniform în cursul anului: 9,4% între noiembrie și aprilie și 11,4% între mai și octombrie, în ciuda creșterii prețului. Banda s-a lărgit odată cu nivelul prețului: semilățimea ei medie a fost de 33 EUR/MWh în prima jumătate a anului de test și de 36 în septembrie–octombrie.

@practice Un furnizor își poate fixa limita zilnică de achiziție pe baza acestei benzi; testele formale ale unor asemenea benzi se studiază în cursul 4.

@chart case_band
Prețul zilnic de bază din România în anul de test, banda GARCH-t de 90% stabilită în $t-1$ (zona colorată) și zilele aflate în afara benzii (puncte).

## Studiu de caz: limitele pentru noiembrie 2026 și șocul din aprilie {h=ab8dacad}

Graficul transformă prognoza pe mai mulți pași din @eq:multistep în limite. În stînga se află prognoza GARCH-t a valorii zilnice $\sigma$ pentru prețul din România în zilele lunii noiembrie 2026, făcută cu datele pînă la 31 octombrie 2026, împreună cu nivelul ei de lungă durată. La 31 octombrie, prognoza era $\hat\sigma$ = 26,0 EUR/MWh, aproape de nivelul de lungă durată, 27,6, deci structura la termen a prognozei este aproape plată. Limita de 90% pentru o zi este de circa ±43 EUR/MWh în fiecare zi din noiembrie.

În dreapta se află banda de 90% pentru Brent pe un orizont de $h$ zile de tranzacționare, calculată la 9 aprilie 2026, în vîrful șocului petrolier: banda GARCH, care adună prognozele zilnice ca în @eq:aggvar, crește mai lent decît $\sigma\sqrt{h}$ calculat cu volatilitatea de azi, deoarece se aștepta revenirea volatilității spre nivelul ei de lungă durată.

@practice Stabiliți limitele după structura la termen a prognozei, nu după volatilitatea de azi.

@chart term_structure
Stînga: prognoza GARCH-t a valorii zilnice $\sigma$ pentru prețul din România, în funcție de numărul de zile înainte, cu nivelul de lungă durată (linie întreruptă); dreapta: banda de 90% pentru Brent pe $h$ zile de tranzacționare, la 9 aprilie 2026, GARCH-t față de $\sigma$ de azi $\times\sqrt{h}$.

## Studiul de caz C3: legătura slabă dintre acțiunile energetice românești și petrol {h=f1f1426c}

Studiul de caz C3 pornește de la o lucrare a grupului nostru, Grecu, Cramer, Pele & Lessmann (2025). Lucrarea folosește indicii bursieri ai celor 27 de state ale Uniunii Europene și contractele futures pe Brent și TTF din perioada 2010–2023. Ea estimează volatilitatea fiecărei serii cu un model GARCH, apoi o corelație condiționată dinamică (DCC) între fiecare indice și prețurile energiei pentru fiecare zi și, în final, un model Markov pentru regimurile acestei corelații. Rezultatele arată că corelația cu petrolul este în general între 0 și 0,4, că Europa Centrală și de Est (ECE) este regiunea cel mai slab corelată și că regimurile corelației persistă cu probabilități de peste 98%.

Replicarea noastră aplică aceeași metodă pentru trei acțiuni energetice românești, OMV Petrom, Romgaz (SNG) și Nuclearelectrica (SNN), față de Brent, pe 2 860 de zile. Parametrii DCC sînt $a$ = 0,021 și $b$ = 0,950: corelația reacționează lent și este foarte persistentă. Corelația medie este 0,13, cu un maxim de 0,54 în 2020 și un minim de −0,32 în 2022, aceeași cronologie ca în lucrare. Acoperirea riscului coșului cu Brent, în afara eșantionului, modifică varianța acestuia cu −1,7% în varianta dinamică și cu −6,9% în cea statică; aici o valoare negativă înseamnă risc mai mare, deci acoperirea nu ajută. Cifrele C3 sînt calculate cu notebook-ul Jupyter al studiului de caz C3, pe datele noastre; rezultatele lucrării sînt prezentate în fișa studiului de caz.

@practice Riscul acțiunilor energetice românești ține de reglementare și de piața locală: acoperirea cu Brent nu îl reduce.

## @end

În 2026, prețul energiei electrice din România a urcat la un nivel mai ridicat fără să intre într-un regim de volatilitate de tipul celui din 2022. Banda GARCH-t de o zi a funcționat corect în anul de test, limitele pentru noiembrie urmează structura la termen a prognozei, iar acțiunile energetice românești nu pot fi acoperite cu petrol.

# Recapitulare

Recapitularea verifică ideile principale prin cinci întrebări scurte, rezumă cursul și trimite la cercetările grupului nostru și la lecturi suplimentare.

## Întrebări de autoevaluare {h=eeb091f5}

1. Pentru Brent, GARCH(1,1)-t dă $\hat\alpha+\hat\beta$ = 0,973. După un șoc, în cît timp dispare jumătate din varianța suplimentară? Răspuns: din @eq:halflife, $h_{1/2}=\ln 0{,}5/\ln 0{,}973$ = 25,6 zile lucrătoare, circa 5 săptămîni: limitele rămîn mai largi săptămîni întregi, nu cîteva zile.
2. În 2022, volatilitatea procentuală a prețului din România a fost aceeași ca în 2019. S-a schimbat riscul unei poziții deschise de 10 MW a unui furnizor? Răspuns: da. Poziția cîștigă sau pierde în euro, iar volatilitatea șocurilor în EUR/MWh a crescut de 4,1 ori, odată cu nivelul prețului.
3. Prețul PZU crește cu 35% de duminică pînă luni. Trebuie departamentul de risc să lărgească limitele? Răspuns: nu. În medie, prețul de luni este cu 38% mai mare decît cel de duminică; calendarul este inclus în ecuația mediei @eq:mean, iar în modelul GARCH intră doar șocul $\varepsilon_t$, aici aproape zero.
4. Modelul de volatilitate al unui furnizor are cea mai mică eroare pătratică medie în anul de test, datorită a trei zile extreme. Ce îi cereți? Răspuns: valoarea QLIKE pe aceleași zile și un test DM față de GARCH-t și de varianța istorică pe 30 de zile. În anul nostru de test, cel mai bun QLIKE în EUR/MWh îl are EGARCH-t, fără a fi semnificativ mai bun decît GARCH-t.
5. Ieri prețul s-a modificat cu 61 EUR/MWh. Pentru un cumpărător, ziua de mîine este mai riscantă după o creștere sau după o scădere? Răspuns: după o creștere. Modelul GJR în EUR/MWh dă $\sigma$ = 37,6 după o creștere și 30,6 după o scădere, efectul de levier invers.

## Recapitulare {h=5e1f86d9}

Mai întîi măsurăm: eliminăm efectul zilei din săptămînă înainte de a măsura volatilitatea și alegem cu grijă unitatea de măsură. În procente, criza energetică nu a fost mai volatilă decît anul 2019; în EUR/MWh, volatilitatea a fost de 4,1 ori mai mare, iar aceasta este volatilitatea pe care o urmează garanțiile și apelurile în marjă.

Apoi modelăm și prognozăm: modelul GARCH cu șocuri Student este modelul implicit. Șocurile petrolului se înjumătățesc în circa 5 săptămîni, șocurile procentuale ale prețului energiei din România în cîteva zile; modelele asimetrice aduc puțin în afara eșantionului; un model cu regimuri datează criza, iar modelul HAR prognozează variația intrazilnică. Cursul următor transformă volatilitatea în măsuri de risc pentru companiile energetice (cursul 4).

## Cercetările grupului nostru despre volatilitate și risc {h=60765cad}

Mai multe lucrări ale grupului nostru, de la Academia de Studii Economice din București și de la Academia Română, Institutul de Prognoză Economică, folosesc instrumentele acestui curs. Rezultatele de mai jos sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.

- **Prețurile energiei și bursele din UE** (Grecu, Cramer, Pele & Lessmann, 2025). Lucrarea estimează volatilitatea GARCH, corelații DCC zilnice și regimuri Markov pentru 27 de indici bursieri naționali, față de petrol și gaze, în perioada 2010–2023. Rezultatele arată că piețele europene urmează mai mult petrolul decît gazele, cu regimuri persistente ale corelației; lucrarea stă la baza studiului de caz C3.
- **Entropia și riscul de piață** (Pele, Lazar & Dufour, 2017). Lucrarea măsoară entropia randamentelor intrazilnice euro–yen și o leagă de valoarea expusă la risc (VaR) și de pierderea medie în coada distribuției (*expected shortfall*, ES) intrazilnice. Rezultatele arată o relație negativă între entropie și VaR, respectiv ES intrazilnic; entropia intrazilnică servește apoi la prognoza VaR zilnic.
- **Entropia datelor de înaltă frecvență și riscul zilnic** (Pele & Mazurencu-Marinescu-Pele, 2019). Lucrarea folosește entropia randamentelor intrazilnice ale Bitcoin pentru prognoza VaR zilnic și o compară cu modelele GARCH clasice. Prognoza VaR bazată pe entropie dă cele mai bune rezultate la testare, ceea ce arată că datele intrazilnice conțin informație despre riscul zilnic.
- **Energy Financial Risk Meter** (Toma, Dima, Grecu, Pele & Lessmann, 2026). Lucrarea construiește un indicator al riscului sistemic pentru sectorul energetic din UE, tema cursului 4.

## AIDA 2026: crizele geopolitice fac negativă legătura burselor din UE cu energia {h=bed1f3de}

La conferința AIDA a Academiei de Studii Economice din București, pe 3 iunie 2026, Alexandru-Adrian Cramer a prezentat lucrarea lui Grecu, Cramer, Pele și Lessmann despre prețurile energiei și bursele europene, articolul pe care se sprijină studiul de caz C3, cu datele extinse pînă în 2026. Lucrarea folosește indicele bursier principal al fiecărei țări din Uniunea Europeană, grupat și în indici regionali și după nivelul producției industriale, precum și contractele futures generice pe petrolul Brent și pe gazele TTF olandeze, din 2010 pînă în 2026. Mai întîi modelează volatilitatea fiecărei serii cu GARCH, apoi estimează o corelație condiționată dinamică (DCC) zilnică între fiecare indice și petrol sau gaze, modelul din studiul de caz C3; un model Markov cu schimbare de regim separă perioadele de corelație ridicată și scăzută, iar un model vectorial autoregresiv structural, pe date lunare, urmărește răspunsul indicilor la un șoc al petrolului sau al gazelor.

Corelația indicilor bursieri cu petrolul este în general pozitivă, în cele mai multe cazuri între 0 și 0,4, iar corelația cu gazele este, în general, mai mică decît cea cu petrolul. Petrolul este cel mai puternic corelat cu indicii din sudul și vestul Europei, gazele cu cei din nordul și vestul Europei, iar țările cele mai industrializate urmează mai îndeaproape petrolul. Crizele geopolitice fac corelația negativă: după anexarea Crimeii, în 2014 (gaze, mai ales în nordul și vestul Europei), după invazia Ucrainei de către Rusia, în 2022 (pentru gaze, cel mai puternic în Europa Centrală și de Est), și în timpul tensiunilor din Orientul Mijlociu din 2026. După un șoc al petrolului sau al gazelor, indicii țărilor celor mai industrializate sînt mai afectați în primele luni, iar efectul se estompează pe termen mediu. Rezultatele sînt cele raportate de autori: [diapozitivele prezentării](https://github.com/danpele/EMQA/blob/main/resources/aida2026/cramer_energy_stock_markets.pdf); articolul: [doi:10.1016/j.najef.2025.102420](https://doi.org/10.1016/j.najef.2025.102420).

@practice Cine acoperă acțiuni din UE cu futures pe petrol sau gaze trebuie să se aștepte ca, într-o criză geopolitică, corelația să își schimbe semnul.

## AIDA 2026: șocurile tokenurilor energetice se transmit mai ales pe termen scurt {h=432e5954}

La aceeași conferință AIDA, pe 4 iunie 2026, Souhir Ben Amor și Matúš Horváth au prezentat lucrarea lor despre transmiterea tranzitorie și persistentă a șocurilor între tokenurile energetice și alte piețe. Tokenurile energetice sînt active digitale pe un blockchain care reprezintă energie regenerabilă, de exemplu un token pentru un kilowatt-oră. Lucrarea studiază tokenuri energetice (Power Ledger, SunContract, Energy Web), criptomonede, acțiuni și fonduri de energie curată, mărfuri (petrol, gaze, cupru, aur, certificate de emisii ale Uniunii Europene), fonduri de investiții sustenabile și obligațiuni verzi, din 7 decembrie 2020 pînă la 31 ianuarie 2026. Un model vectorial autoregresiv cu parametri variabili în timp măsoară cît din varianța prognozei fiecărui activ provine din șocurile celorlalte (interconectarea) și o împarte într-o componentă pe termen scurt, tranzitorie, și una pe termen lung, persistentă.

Transmiterea șocurilor variază puternic în timp și are loc mai ales pe termen scurt: banda pe termen scurt reprezintă circa 60% din interconectarea totală, iar cea pe termen lung circa 5%. Crizele din eșantion, turbulențele criptomonedelor din 2021 și criza energetică din 2022, amplifică șocurile pe termen scurt, în timp ce structura pe termen lung rămîne stabilă. Power Ledger și SunContract sînt cei mai importanți transmițători de șocuri pe termen scurt; Energy Web devine relevant mai ales în episoadele de criză. Valoarea pentru diversificare depinde de token: în portofoliul de varianță minimă, raportul Sharpe este 0,127 fără tokenuri și 0,143 cu SunContract, singurul token cu un cîștig constant pozitiv al raportului Sharpe; Power Ledger este neutru, iar Energy Web, receptor net persistent de șocuri, reduce raportul Sharpe pe termen lung. Rezultatele sînt cele raportate de autori: [diapozitivele prezentării](https://github.com/danpele/EMQA/blob/main/resources/aida2026/benamor_energy_tokens_spillovers.pdf).

@practice Șocurile dintre tokenurile energetice și celelalte piețe se transmit în cîteva zile; valoarea pentru diversificare se judecă pentru fiecare token în parte.

## Lecturi și resurse suplimentare {h=7bd33022}

- **R. F. Engle, GARCH 101** (2001): cea mai clară introducere scurtă, scrisă de laureatul Nobel care a propus modelul ARCH, [doi:10.1257/jep.15.4.157](https://doi.org/10.1257/jep.15.4.157).
- **R. Weron, Modeling and Forecasting Electricity Loads and Prices** (Wiley, 2006): faptele stilizate și volatilitatea prețurilor energiei electrice, [doi:10.1002/9781118673362](https://doi.org/10.1002/9781118673362).
- **Pachetul Python arch** (K. Sheppard), folosit pentru toate modelele din acest curs: [arch.readthedocs.io](https://arch.readthedocs.io).
- **Acest curs**: cod, date și notebook-uri Jupyter la [github.com/danpele/EMQA](https://github.com/danpele/EMQA).
- **Studiul de caz C3**: modelul DCC și acoperirea cu Brent pentru acțiunile energetice românești, pas cu pas.
- **Exercițiu practic**: notebook-ul Jupyter al cursului reproduce toate graficele și cifrele: [L3_notebook_ro.ipynb](https://github.com/danpele/EMQA/blob/main/notebooks/L3_notebook_ro.ipynb).

# Anexă

Anexa prezintă detaliile tehnice din spatele textului principal: funcția de verosimilitate Student a modelului GARCH, deducerea prognozei pe mai mulți pași și a timpului de înjumătățire, tabelul complet al celor șase modele, filtrul Hamilton și motivul pentru care folosim QLIKE.

## Anexa A: funcția de verosimilitate Student a modelului GARCH {h=f6f5ca86}

Scris complet, logaritmul funcției de verosimilitate pentru un model GARCH cu șocuri Student este

$$ \ell(\theta)=\sum_{t=1}^{T}\Bigl[\ln\Gamma\bigl(\tfrac{\nu+1}{2}\bigr)-\ln\Gamma\bigl(\tfrac{\nu}{2}\bigr)-\tfrac12\ln\bigl(\pi(\nu-2)\bigr)-\tfrac12\ln\sigma_t^2-\tfrac{\nu+1}{2}\ln\Bigl(1+\frac{\varepsilon_t^2}{(\nu-2)\sigma_t^2}\Bigr)\Bigr], $$ {#eq:tlik}

unde $\theta=(\omega,\alpha,\beta,\nu)$ reunește parametrii, $\Gamma$ este funcția gamma, $\sigma_t^2$ urmează @eq:garch, iar $\varepsilon_t$ este șocul. Factorul $\nu-2$ dă variabilei Student varianța 1, astfel încît $\sigma_t^2$ să rămînă varianța condiționată. Funcția se maximizează numeric, cu restricțiile $\omega>0$, $\alpha,\beta\ge0$, $\alpha+\beta<1$ și $\nu>2$, cu erori standard robuste, folosind pachetul Python arch. În cazul normal,

$$ \ell=-\tfrac12\sum_{t}\bigl[\ln(2\pi)+\ln\sigma_t^2+\varepsilon_t^2/\sigma_t^2\bigr], $$ {#eq:normlik}

care este limita expresiei @eq:tlik pentru $\nu\to\infty$.

| GARCH(1,1)-t | % | EUR/MWh |
|---|---|---|
| $\omega$ | 105,677 (35,482) | 4,635 (1,773) |
| $\alpha$ | 0,308 (0,081) | 0,102 (0,020) |
| $\beta$ | 0,438 (0,150) | 0,892 (0,021) |
| $\nu$ | 4,266 (0,370) | 6,149 (0,655) |

Fiecare celulă conține estimația și, în paranteză, eroarea ei standard.

## Anexa B: prognoza pe mai mulți pași și timpul de înjumătățire {h=051b5825}

Deducerea relației @eq:decay are trei pași.

1. Scriem $\varepsilon_t^2=\sigma_t^2+v_t$, unde $v_t$ este o surpriză cu $\E_{t-1}[v_t]=0$. Înlocuind în @eq:garch, obținem $\sigma^2_{t+1}=\omega+(\alpha+\beta)\sigma_t^2+\alpha v_t$.
2. Aplicăm media condiționată în $T$: $\E_T[\sigma^2_{T+h}]=\omega+(\alpha+\beta)\E_T[\sigma^2_{T+h-1}]$, pentru $h\ge2$. Scăzînd identitatea de lungă durată $\bar\sigma^2=\omega+(\alpha+\beta)\bar\sigma^2$, vedem că abaterea față de $\bar\sigma^2$ se înmulțește în fiecare zi cu $\alpha+\beta$.
3. Rezultă $\E_T[\sigma^2_{T+h}]-\bar\sigma^2=(\alpha+\beta)^{h-1}(\sigma^2_{T+1}-\bar\sigma^2)$. Rămîne jumătate din abatere cînd $(\alpha+\beta)^{h}=1/2$, deci $h_{1/2}=\ln(1/2)/\ln(\alpha+\beta)$, adică @eq:halflife.

Pentru modelele asimetrice, persistența se definește altfel. În modelul GJR cu $z_t$ simetric, termenul $\gamma I_{t-1}$ este activ în jumătate din zile, deoarece $\Pr(\varepsilon<0)=1/2$, deci persistența este $\alpha+\gamma/2+\beta$. În modelul EGARCH, $\ln\sigma_t^2$ urmează un proces autoregresiv cu coeficientul $\beta$, deci persistența este $\beta$.

## Anexa C: cele șase modele, în ambele unități de măsură {h=460b8e7e}

Tabelul dă log-verosimilitatea $\hat\ell$ (log-L), criteriul informațional Akaike $\text{AIC}=2k-2\hat\ell$ și criteriul informațional bayesian $\text{BIC}=k\ln T-2\hat\ell$, unde $k$ este numărul de parametri, pentru cele șase modele, în ambele unități de măsură. Toate sînt estimate pe 2 853 de zile, între 1 ianuarie 2019 și 31 octombrie 2026.

| Modelul | log-L, % | AIC, % | BIC, % | log-L, EUR | AIC, EUR | BIC, EUR |
|---|---|---|---|---|---|---|
| GARCH, normal | −12 360,3 | 24 726,6 | 24 744,5 | −12 274,7 | 24 555,4 | 24 573,2 |
| GARCH, Student | −12 094,5 | 24 197,0 | 24 220,8 | −12 209,4 | 24 426,8 | 24 450,7 |
| GJR, normal | −12 329,4 | 24 666,8 | 24 690,7 | −12 246,6 | 24 501,3 | 24 525,1 |
| GJR, Student | −12 087,2 | 24 184,3 | 24 214,1 | −12 185,9 | 24 381,9 | 24 411,7 |
| EGARCH, normal | −12 329,8 | 24 667,6 | 24 691,4 | −12 243,1 | 24 494,2 | 24 518,0 |
| EGARCH, Student | −12 089,7 | 24 189,4 | 24 219,2 | −12 182,1 | 24 374,1 | 24 403,9 |

AIC și BIC dau aceeași ordine: GJR-t este cel mai bun în procente, iar EGARCH-t în EUR/MWh. Pentru GJR-t, asimetria $\hat\gamma$ și numărul de grade de libertate $\hat\nu$ sînt 0,225 și 4,41 în procente, respectiv −0,127 și 6,50 în EUR/MWh.

## Anexa D: filtrul Hamilton și robustețea funcției QLIKE {h=3da84f13}

Filtrul Hamilton calculează recursiv probabilitățile regimurilor din @eq:ms. La pasul de predicție,

$$ \Pr(s_t=j\mid\mathcal F_{t-1})=\sum_i p_{ij}\Pr(s_{t-1}=i\mid\mathcal F_{t-1}), $$ {#eq:hamilton}

unde $\mathcal F_{t-1}$ este informația disponibilă pînă în ziua $t-1$, iar $p_{ij}$ sînt probabilitățile de tranziție. La pasul de actualizare, fiecare probabilitate prognozată se înmulțește cu densitatea normală a lui $u_t$ în regimul $j$, iar rezultatele se normalizează astfel încît suma lor să fie 1; suma logaritmilor constantelor de normalizare este log-verosimilitatea. Probabilitățile netezite din grafic folosesc toate datele, iar cele filtrate doar trecutul; o avertizare în timp real trebuie să folosească probabilitățile filtrate.

De ce QLIKE? Dacă $\E_{t-1}[\varepsilon_t^2]=\sigma_t^2$, valoarea așteptată a QLIKE este minimă numai pentru $\hat\sigma_t^2=\sigma_t^2$, oricît de zgomotos ar fi $\varepsilon_t^2$ ca aproximare. Același lucru este valabil pentru MSE, în timp ce alte funcții, ca $|\varepsilon_t|-\hat\sigma_t$ sau erorile în logaritmi, pot ordona greșit modelele (Patton, 2011). Statistica DM este media diferențelor zilnice de pierdere împărțită la eroarea ei standard Newey–West, calculată cu 7 decalaje; ea are asimptotic o distribuție normală.
