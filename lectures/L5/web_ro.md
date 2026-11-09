<!--
Versiunea web a cursului 5 (RO). Construită în web/L5_ro.html de lectures/common/build_web_lecture.py (formatul: vezi docstring-ul).
Hash-urile slide-urilor: python3 build_web_lecture.py 5 --frames
-->

## @intro

Un furnizor din România care le-a promis clienților un preț fix pentru anul viitor a vîndut energie pe care încă nu o are. Dacă prețul angro crește înainte ca furnizorul să cumpere energia, marja dispare; un producător este expus riscului invers, al scăderii prețului. Cursul arată cum pot fixa aceste firme, de azi, prețul energiei livrate peste cîteva luni, cît din risc elimină efectiv un contract și cît costă această protecție. Răspunsul se sprijină pe instrumente derivate: contracte forward, futures și opțiuni pe energie electrică, gaze și carbon.

În România, întrebarea nu este una teoretică. În 2022, prețul mediu de pe piața pentru ziua următoare a fost 265,3 EUR/MWh, în timp ce banda pentru 2022 fusese cumpărată forward, în medie, la 77,4 EUR/MWh: un furnizor care s-a acoperit la timp a economisit 1,65 milioane EUR pe megawatt (MW), iar un producător care a vîndut forward a renunțat la aceeași sumă. Criza a blocat apoi piața forward și a adus prețuri reglementate; de aceea, o politică de acoperire trebuie să existe înainte de următorul șoc.

Cursul folosește numai date reale: 2 298 de licitații forward ale operatorului pieței de energie electrică și de gaze naturale din România (OPCOM), cu 83,7 terawatt-oră (TWh) tranzacționați, prețuri orare pe piața pentru ziua următoare în România, Ungaria și Germania, prețuri ale gazelor, cărbunelui și carbonului. Pe baza lor construim curba forward, marjele centralelor pe gaze și pe cărbune, raportul de acoperire cu intervalul lui de încredere, prețurile opțiunilor cu formula Black-76 și un studiu de caz pentru un furnizor și un producător în 2022, 2025 și 2026.

@goals
- **Explicați** contractele forward și futures pe energie electrică și gaze, cu livrare fizică sau cu decontare financiară, și interpretați curba prețurilor forward.
- **Calculați** spark spread și dark spread, inclusiv costul certificatului de emisii (EUA) al Uniunii Europene (UE), și evaluați o centrală flexibilă ca serie de opțiuni.
- **Estimați** raportul de acoperire cu varianță minimă și incertitudinea lui și măsurați riscul de bază și riscul de profil.
- **Evaluați** plafoane, praguri minime și collar-uri cu formula Black-76, pe baza unei volatilități estimate pe date reale.
- **Analizați** cît au cîștigat sau au pierdut prin acoperire un furnizor și un producător din România în 2022, 2025 și 2026.

# Motivele acoperirii riscului: expunerile la preț și criza din 2021–2022

Fiecare firmă din sectorul energiei are o poziție de preț, iar criza din 2021–2022 a arătat în România cît de mari pot fi cîștigurile și pierderile celor acoperiți sau neacoperiți. Secțiunea definește expunerile și măsoară lecția crizei pe prețurile reale ale licitațiilor.

## Folosim numai date reale: forward, spot, gaze, carbon {h=478c423f}

Toate cifrele din curs provin din date descărcate. Contractele forward sînt rezultatele pieței centralizate a contractelor bilaterale cu licitație extinsă (PCCB-LE) a OPCOM: 2 298 de licitații, cu 83,7 TWh, între 12 mai 2020 și 28 octombrie 2026. Prețurile spot sînt prețurile orare de pe Piața pentru Ziua Următoare (PZU) pentru România (RO), Ungaria (HU) și zona de ofertare Germania–Luxemburg (DE-LU), publicate de OPCOM, de bursa de energie din Ungaria (HUPX) și de bursa europeană de energie (EPEX SPOT) și preluate prin energy-charts.info, platforma Institutului Fraunhofer pentru Sisteme de Energie Solară (ISE), din datele Rețelei europene a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E).

Prețul gazelor este cel de la Title Transfer Facility (TTF), hubul olandez de gaze naturale: lunar, din Pink Sheet-ul Băncii Mondiale, și zilnic, din contractele futures ale bursei New York Mercantile Exchange (NYMEX), prin Yahoo Finance; tot de la Banca Mondială provine și prețul cărbunelui. Prețul carbonului (EUA) provine din licitațiile bursei European Energy Exchange (EEX) și, ulterior, dintr-un titlu tranzacționat la bursă, garantat cu certificate (*exchange-traded commodity*, ETC); cursul euro (EUR) față de leu (RON) și rata pe termen scurt a euro (€STR) provin de la Banca Centrală Europeană (BCE). Data-limită este 31 octombrie 2026, ultima lună completă.

Două tipuri de date nu sînt disponibile gratuit: contractele futures pe energie de la EEX sau de la bursa maghiară de derivate pe energie (HUDEX) și prețurile opțiunilor. Nu le inventăm; acolo unde avem nevoie de prețul unei opțiuni, îl calculăm cu un model și cu o volatilitate estimată, iar textul precizează acest lucru.

## Fiecare firmă din sectorul energiei are o poziție de preț {h=0cbdb068}

Un furnizor care vinde la prețuri fixe pierde cînd prețul angro crește; un producător pierde cînd prețul scade. Profiturile lor pentru o cantitate de energie sînt

$$ \Pi^{\text{furn}}=Q(R-S),\qquad \Pi^{\text{prod}}=Q(S-c), \qquad \Pi^{\text{furn}}_{\text{acoperit}}=Q(R-S)+Q(S-F)=Q(R-F), $$ {#eq:profit}

unde $Q$ este energia, în megawatt-oră (MWh), $R$ prețul de vînzare către clientul final, $S$ prețul spot la livrare, $c$ costul producătorului, iar $F$ prețul forward stabilit azi, toate în EUR/MWh. Un forward cumpărat aduce $S-F$ pe MWh; adăugat la poziția furnizorului, el elimină complet prețul $S$, astfel încît profitul acoperit din @eq:profit depinde numai de prețuri cunoscute de azi.

Firmele diferă prin semnul expunerii. Furnizorul cu prețuri fixe și consumatorul industrial au o poziție scurtă: se acoperă cumpărînd forward sau un plafon. Producătorii hidro, nucleari, pe lignit și solari au o poziție lungă: se acoperă vînzînd forward sau cumpărînd un prag minim. O centrală pe gaze are o poziție lungă pe marjă, adică pe diferența dintre prețul energiei și costul gazelor și al carbonului, și trebuie să acopere simultan toate cele trei prețuri (Hull, 2022; Eydeland & Wolyniec, 2003).

@practice stabiliți întîi semnul expunerii: o firmă cu poziție lungă care mai cumpără forward își dublează riscul.

## În 2022, prețul spot a fost de 3,4 ori mai mare decît prețul forward {h=a024f812}

Banda pentru 2022 s-a tranzacționat în 150 de licitații OPCOM. Prețul ei mediu ponderat cu volumul (VWAP) a fost 77,4 EUR/MWh, în timp ce prețul PZU din România a avut în 2022 o medie de 265,3 EUR/MWh, de 3,4 ori mai mult. Un furnizor care își cumpărase forward energia pentru 2022 a economisit 1,65 milioane EUR pentru fiecare MW de consum constant.

Momentul cumpărării a contat aproape la fel de mult ca decizia de a se acoperi. Contractele pentru 2022 s-au tranzacționat, în medie, la 54,4 EUR/MWh în 2020, la 61,5 în semestrul I 2021 și la 136,7 în semestrul II 2021, cînd criza gazelor urcase deja prețurile. Un furnizor care a așteptat pînă la sfîrșitul lui 2021 a plătit aproximativ dublu față de unul care a cumpărat devreme, dar tot mult mai puțin decît spotul.

@practice contează și momentul: contractele cumpărate la sfîrșitul lui 2021 au costat dublu.

@chart crisis_cal22
Media lunară a prețului PZU în România, 2020–2022, fiecare licitație pentru banda 2022 (puncte), prețul forward mediu ponderat și media realizată în 2022 (linii întrerupte).

## Criza a redus tranzacțiile forward și a dus la prețuri reglementate {h=04bb5dbf}

Acoperirea riscului este un transfer, nu un cîștig creat din nimic. Fiecare MWh vîndut forward pentru 2022 a fost cu 187,9 EUR/MWh sub spot: producătorii care au vîndut forward au pierdut exact cît au economisit furnizorii acoperiți. Apoi prețurile forward au crescut excesiv în sens invers: banda pentru 2023 s-a tranzacționat la 509,2 EUR/MWh pe 17 august 2022, iar media realizată în 2023 a fost doar 103,7 EUR/MWh.

România a răspuns prin reglementare. Ordonanța de urgență a Guvernului (OUG) 27/2022 a plafonat prețurile finale, iar OUG 153/2022 a creat Mecanismul de achiziție centralizată de energie electrică (MACEE), în care OPCOM a fost cumpărător unic la 450 lei/MWh, în 2023–2024. Volumul forward pe OPCOM a scăzut de la 27,3 TWh în 2021 la doar 1,6 TWh în 2023. La nivelul UE, Agenția UE pentru Cooperarea Autorităților de Reglementare din Domeniul Energiei (ACER) a păstrat modelul pieței și a semnalat lichiditatea redusă a contractelor forward pe peste trei ani (ACER, 2022).

@practice scrieți politica de acoperire înainte de criză: în timpul crizei, nimeni nu mai cade de acord asupra ei.

## @end

Un contract forward fixează azi prețul unei livrări viitoare și mută bani între cumpărător și vînzător. În 2022, a adus furnizorilor din România exact cît i-a costat pe producători, iar criza care a urmat a secat chiar piața forward.

# Contracte forward, futures și curba forward

Secțiunea descrie contractele la care are acces o firmă din România, forward-urile cu livrare fizică de pe OPCOM și contractele futures cu decontare financiară din străinătate, și interpretează curba forward și prima forward pe prețurile licitațiilor OPCOM. Încheiem cu întrebarea dacă, în medie, cumpărarea forward a energiei este scumpă sau ieftină.

## Un forward pe energie livrează aceeași putere pe toată perioada {h=a618fb0f}

Un forward în bandă fixează azi prețul tuturor orelor dintr-o lună, un trimestru sau un an. La livrare, valoarea lui este

$$ \bar S=\frac{1}{H}\sum_{h=1}^{H}S_h,\qquad V_T=q\,H\,(\bar S-F), $$ {#eq:forward}

unde $H$ este numărul de ore al perioadei de livrare (744 într-o lună de 31 de zile, 8 760 într-un an), $S_h$ prețul PZU al orei $h$, $\bar S$ media acestor prețuri, $q$ puterea, în MW, iar $F$ prețul forward; $V_T$ este valoarea contractului pentru cumpărător la sfîrșitul perioadei.

Contractele diferă prin profil. Banda acoperă toate orele, de luni pînă duminică (LD, codul produsului OPCOM), și reprezintă 94% din volum; contractul de vîrf acoperă numai orele de vîrf ale zilelor lucrătoare. La 31 octombrie 2026, pe OPCOM, anul 2027 avea prețul de 148,1 EUR/MWh, ceea ce pentru 1 MW înseamnă 8 760 MWh la acest preț, iar luna următoare 215,3 EUR/MWh (Benth et al., 2008).

@practice faceți oferta către client pe baza prețului forward al perioadei de livrare, nu a prețului spot de azi.

## Livrarea fizică și decontarea financiară {h=f693a277}

Forward-ul fizic livrează energia la prețul $F$; contractul futures cu decontare financiară plătește doar diferența dintre o medie de referință și $F$, iar firma cumpără energia de pe piața spot. Cele două sînt echivalente numai cu o condiție:

$$ F\cdot Q=\bar S Q-(\bar S^{\text{ref}}-F)Q \quad \text{numai dacă } \bar S^{\text{ref}}=\bar S, $$ {#eq:cash}

unde $\bar S^{\text{ref}}$ este indicele de decontare al contractului futures (de exemplu, media prețurilor din Germania), iar $\bar S$ prețul mediu plătit efectiv de firmă. Cînd diferă, diferența dintre ele este riscul de bază, tema secțiunii a patra.

În România, contractele fizice se tranzacționează în licitațiile OPCOM PCCB-LE și pe piața centralizată cu negociere dublă continuă a contractelor bilaterale (PC-OTC); ele nu au risc de bază. Contractele futures financiare se tranzacționează în străinătate, la EEX și HUDEX, cu casă de compensație: aceasta elimină riscul de contrapartidă, dar cere în schimb plata marjelor (Hull, 2022).

@practice contracte fizice, pentru energie livrată în România; contracte financiare, pentru o piață lichidă, cu riscul de bază asumat.

## Contractele futures se decontează zilnic, deci cer lichiditate {h=f161ee0f}

Forward-ul se decontează o singură dată, la livrare; deținătorul unui contract futures plătește sau încasează zilnic variația prețului. Plata zilnică este marja de variație (VM):

$$ VM_t=Q(F_t-F_{t-1}),\qquad \sum_{t=1}^{T}VM_t=Q(F_T-F_0), $$ {#eq:vm}

unde $F_t$ este prețul de decontare din ziua $t$, iar $Q$ poziția, în MWh. Pe durata contractului, plățile însumate dau același rezultat ca un forward, dar sosesc zi de zi. Pe lîngă ele, bursa cere o marjă inițială, calculată cu un model de valoare expusă la risc (VaR), ca în cursul 4.

Contractul NYMEX TTF pentru decembrie 2026 arată mărimea acestor fluxuri: în 1 487 de prețuri zilnice s-a mișcat între 15,1 și 103,9 EUR/MWh, iar cea mai mare variație zilnică a fost de 11,83 EUR/MWh, la 29 august 2022. Pentru o poziție de 10 MW pe 744 de ore, acea singură zi a însemnat un apel în marjă de 88 015 EUR. O firmă care nu poate plăti un asemenea apel este obligată să închidă acoperirea exact cînd are cea mai mare nevoie de ea.

@practice dimensionați linia de credit pentru cea mai mare variație zilnică înainte de a vă acoperi la bursă.

## Volumul forward din România s-a prăbușit în 2022–2023 {h=32bdf5be}

Piața forward a OPCOM este concentrată pe partea vînzătorilor. Trei producători vînd 83% din volum: Complexul Energetic Oltenia 32%, Nuclearelectrica 30% și Hidroelectrica 21%. Produsele pe an calendaristic reprezintă 80% din volumul în bandă, deci în România acoperirea se face mai ales an cu an.

Volumul a urcat la 27,3 TWh în 2021 și s-a prăbușit în 2022–2023, cînd plafonarea prețurilor și mecanismul cu cumpărător unic MACEE au înlocuit tranzacțiile bilaterale. De atunci, lichiditatea a revenit doar parțial, astfel că o cumpărare mare poate mișca prețul licitației.

@practice lichiditatea este redusă: eșalonați cumpărările pe mai multe licitații.

@chart fw_volume
Energia contractată anual în licitațiile forward OPCOM, în TWh, pe tipuri de produs (an calendaristic, semestru, trimestru, lună, alte perioade); anul 2026 pînă la data-limită.

## Forward-ul gazelor reflectă costul de stocare; al energiei, nu {h=273f2c81}

Gazele se pot stoca, deci prețul lor forward este legat de spot prin costul de deținere; energia electrică nu se poate stoca, deci prețul ei forward este prețul spot așteptat plus o primă de risc (*risk premium*):

$$ F_{t,T}=S_te^{(r+u-y)(T-t)}\ \ \text{(stocabil)},\qquad F_{t,T}=\E_t[\bar S_T]+\pi_{t,T}\ \ \text{(energie)}, $$ {#eq:carry}

unde $F_{t,T}$ este prețul forward la momentul $t$ pentru livrare la $T$, $S_t$ prețul spot, $r$ dobînda, $u$ costul de stocare, $y$ randamentul de comoditate (*convenience yield*), $\E_t[\bar S_T]$ prețul spot mediu așteptat pe perioada de livrare, iar $\pi_{t,T}$ prima de risc. Prima relație se aplică mărfurilor care se pot stoca, a doua energiei electrice. O curbă situată peste spot ($F>S$) indică report (*contango*); una sub spot ($F<S$), deport (*backwardation*) (Fama & French, 1987; Bessembinder & Lemmon, 2002).

La 30 octombrie 2026, contractul NYMEX TTF pe gaze pentru decembrie 2026 se tranzacționa la 103,9 EUR/MWh, iar cel pentru mai 2027 la 78,1: diferența dintre prețul de iarnă și cel de vară acoperă costul stocării. Energia electrică din România era în deport: spotul din octombrie 239,3, trimestrul I 2027 la 176,7, anul 2027 la 148,1 EUR/MWh. Piața se așteaptă ca prețurile ridicate de acum să scadă.

@practice nu puneți spotul de azi în bugetul anului viitor: folosiți curba forward.

## Curba forward din România coboară de la un spot ridicat {h=a3695571}

Curba forward este construită din cele 85 de licitații OPCOM din septembrie și octombrie 2026. Ea conține 7 produse în bandă; VWAP-ul pe perioada de livrare este 215,3 EUR/MWh pentru luna următoare, 176,7 pentru trimestrul I 2027 și 148,1 pentru anul 2027. Fiecare segment orizontal arată prețul la care energia pentru acea perioadă poate fi fixată de azi.

Graficul pune curba alături de spotul lunar realizat în ultimii doi ani, ceea ce face vizibil deportul: piața evaluează lunile următoare aproape de spotul ridicat de acum, iar anul următor mult mai jos.

@practice o ofertă pentru 2027 pornește de la 148 EUR/MWh, nu de la spotul din octombrie.

@chart fwd_curve
Media lunară realizată a prețului PZU în România (linie în trepte) și prețurile forward pentru fiecare perioadă de livrare (segmente orizontale: lună, trimestru, semestru, an); linia verticală punctată marchează data-limită.

## Curba se mișcă: prețurile anuale, după data tranzacției {h=68918147}

Prețul forward este prețul certitudinii, nu o prognoză care nimerește prețul realizat. Graficul arată fiecare licitație a produselor anuale la data tranzacției, iar media realizată a anului ca linie groasă. Pentru 2021, VWAP-ul a fost 51,3 EUR/MWh, iar spotul realizat 111,4; pentru 2023, forward-ul a avut media 172,5 față de 103,7 realizat, pentru că a fost cumpărat în plină criză; pentru 2025, cele două au fost apropiate: 102,1 față de 108,2 EUR/MWh.

Erorile au fost mari și de ambele semne. Acoperirea a fixat costul fiecărui an, dar nivelul la care l-a fixat a depins de momentul cumpărării.

@practice prețul forward este prețul certitudinii, nu o prognoză pentru vremuri de criză.

@chart cal_by_trade
Prețurile contractelor anuale în bandă pe OPCOM, după data licitației (puncte, cîte o culoare pentru fiecare an de livrare), și media spot realizată a fiecărui an de livrare (linii groase).

## Prima forward ex post nu are un semn stabil în România {h=e1068e49}

Dacă cumpărătorii se tem de salturi de preț mai mult decît se tem vînzătorii de scăderi, forward-ul ar trebui să depășească spotul așteptat, iar cumpărătorii ar plăti, în medie, o primă. Prima se poate măsura numai după livrare:

$$ \hat\pi_i=F_i-\bar S_i,\qquad t=\frac{\bar\pi}{\widehat{\text{se}}_{\text{HAC}}(\bar\pi)}, $$ {#eq:premium}

unde $i$ este luna de livrare, $F_i$ VWAP-ul benzii lunare cumpărate în luna anterioară livrării, $\bar S_i$ media spot realizată în luna $i$, $\bar\pi$ media valorilor $\hat\pi_i$, iar $\widehat{\text{se}}_{\text{HAC}}$ eroarea ei standard robustă la heteroscedasticitate și autocorelare (HAC), Newey–West, cu 3 decalaje.

Pentru 30 de luni de livrare cumpărate cu o lună înainte, prima medie este +5,2 EUR/MWh, cu $t$ = 0,42 și $p$ = 0,68: nu există dovezi ale unei prime. Din 2023, media este +24,5, cu $t$ = 1,51, tot nesemnificativă. Pentru toate produsele, ponderate cu volumul, prima a fost −55,8 EUR/MWh pentru livrările pînă în 2021, −166,5 în 2022 și +29,7 din 2023: semnul depinde de perioadă (Bessembinder & Lemmon, 2002; Redl et al., 2009).

@practice acoperirea este, în medie, ieftină; costul ei real este cîștigul la care renunțați.

## Lună de lună, diferența forward minus spot are ambele semne {h=c9fe9529}

Graficul arată prima din @eq:premium pentru fiecare dintre cele 30 de luni de livrare. Mediana ei este −0,2 EUR/MWh, aproape de zero. Valorile negative mari reflectă creșterile neașteptate de preț din 2021–2022, cînd spotul a urcat mult peste ce evaluase forward-ul cu o lună înainte; ele nu sînt o primă negativă sistematică pe care un cumpărător să se poată baza.

Pentru un manager, concluzia este că o acoperire nu trebuie judecată după faptul că a adus sau nu profit după livrare. În unele luni forward-ul a fost peste spot, în altele sub; ceea ce a făcut întotdeauna a fost să elimine incertitudinea costului.

@practice judecați o acoperire după riscul eliminat, nu după profitul de după livrare.

@chart premium
Prețul benzii lunare cumpărate cu o lună înainte minus media spot lunară realizată, în EUR/MWh, pe luni de livrare; barele peste zero arată că cumpărătorul a plătit o primă.

## @end

Contractele forward din România au livrare fizică, sînt vîndute de cîțiva producători mari și sînt mai ales anuale. Curba este prețul certitudinii: se mișcă odată cu piața, iar prima ei față de spotul realizat nu are un semn stabil.

# Marjele centralelor electrice

O centrală pe gaze sau pe cărbune cîștigă diferența dintre prețul energiei și costul combustibilului și al carbonului, deci riscul ei este o marjă, nu un singur preț. Secțiunea calculează clean spark spread și clean dark spread în România și Germania și arată de ce o centrală flexibilă valorează mai mult decît marja ei medie.

## Clean spark spread: energie minus gaze minus carbon {h=27ae7c44}

O centrală pe gaze vinde 1 MWh de energie electrică, arde $1/\eta_g$ MWh de gaze și plătește certificatele pentru CO$_2$ emis. Marjele ei sînt spark spread (SS), marja brută, și clean spark spread (CSS), marja curată:

$$ SS=P-\frac{G}{\eta_g},\qquad CSS=P-\frac{G}{\eta_g}-\frac{e_g}{\eta_g}A, $$ {#eq:css}

unde $P$ este prețul energiei electrice, în EUR/MWh, $G$ prețul gazelor, în EUR pe MWh termic, $\eta_g$ randamentul centralei pe gaze (0,50, ipoteză), $e_g$ factorul de emisie al gazelor, 0,202 t CO$_2$ pe MWh termic, după Grupul interguvernamental privind schimbările climatice (IPCC, 2006), iar $A$ prețul EUA, în EUR pe tonă.

În România, în octombrie 2026, energia a costat 239,3 EUR/MWh, gazele 173,6 pe MWh electric (= 86,8/0,5), iar carbonul 33,3: spark spread a fost +65,7, iar clean spark spread +32,4 EUR/MWh. Media anuală a CSS a fost −32,2 în România în 2022 și +5,8 în 2025; în Germania, −62,2 și −13,1 (Deng et al., 2001).

@practice producătorul pe gaze acoperă marja: vinde energie și cumpără gaze și EUA forward, simultan.

## Dark spread și prețul carbonului care favorizează gazele {h=cdec4b77}

Cărbunele emite mai mult CO$_2$ pe MWh decît gazele, deci un preț ridicat al EUA împinge centralele pe cărbune după cele pe gaze în ordinea de merit. Clean dark spread (CDS), marja curată a centralei pe cărbune, și prețul de echilibru al carbonului sînt

$$ CDS=P-\frac{C}{\eta_c}-\frac{e_c}{\eta_c}A,\qquad A^{*}=\frac{G/\eta_g-C/\eta_c}{e_c/\eta_c-e_g/\eta_g}, $$ {#eq:cds}

unde $C$ este prețul cărbunelui, în EUR pe MWh termic (prețul în USD pe tonă, împărțit la cursul EUR/USD și la 6,978 MWh pe tonă), $\eta_c$ randamentul centralei pe cărbune (0,38, ipoteză), $e_c$ factorul de emisie al cărbunelui, 0,341 t CO$_2$ pe MWh termic, iar $A^{*}$ prețul EUA la care CSS este egal cu CDS; celelalte simboluri sînt cele din @eq:css.

În octombrie 2026, cărbunele a costat 12,8 EUR pe MWh termic, iar clean dark spread în România a fost +131,7 EUR/MWh. Prețul de echilibru $A^{*}$ a fost 283,7 EUR/t, mult peste prețul EUA de 82,4: cu gaze atît de scumpe, cărbunele a rămas mai ieftin. Rezultatul are două limite: lignitul, combustibilul folosit în România, nu are preț de piață, așa că folosim prețul cărbunelui sud-african de export; iar EUA este prețul licitațiilor EEX, înlocuit din ianuarie 2026 de titlul ETC (Banca Mondială).

@practice producătorul pe cărbune care vinde energie forward trebuie să cumpere și EUA forward.

## Clean spark spread și clean dark spread, lunar {h=4fe429cd}

Graficul urmărește marjele lunare din ianuarie 2015 pînă în octombrie 2026. Clean spark spread a fost negativ în 67 din 138 de luni în România și în 121 în Germania; în medie, a fost cu 13,9 EUR/MWh mai mare în România, pentru că, la aceleași prețuri ale gazelor și carbonului, prețul energiei a fost mai ridicat.

O marjă medie apropiată de zero, sau chiar negativă, nu face o centrală pe gaze inutilă. Centrala nu trebuie să funcționeze în fiecare oră: pornește numai cînd marja este pozitivă, iar următoarele două secțiuni măsoară cît valorează această flexibilitate.

@practice o marjă medie apropiată de zero nu face centrala inutilă: ea funcționează doar în orele bune.

@chart spreads
Clean spark spread lunar în România și Germania și clean dark spread în România, în EUR pe MWh de energie electrică, ianuarie 2015 – octombrie 2026.

## O centrală pe gaze flexibilă este o serie de opțiuni call orare {h=ad64cb7c}

Centrala funcționează doar cînd marja este pozitivă, deci încasează partea pozitivă a fiecărei marje orare, adică exact cîștigul unei opțiuni call:

$$ \sum_h \max(CSS_h,0)\ \ge\ \max\Big(\sum_h CSS_h,0\Big), $$ {#eq:strip}

unde $CSS_h$ este clean spark spread al orei $h$, pentru 1 MW, cu gazele și EUA la media lunii. Membrul stîng este marja unei centrale flexibile, cel drept marja unei centrale care funcționează continuu, în fiecare oră. Calculul ignoră costurile de pornire, deci este o limită superioară.

În ultimele 12 luni, marja orară din România a fost pozitivă în 58% din ore; o centrală cu funcționare continuă ar fi cîștigat 38 095 EUR pe MW, iar una flexibilă 235 494. În Germania, marja a fost pozitivă în 41% din ore: funcționare continuă −165 206, flexibilă 112 724 EUR pe MW. Flexibilitatea transformă pierderea în profit (Deng et al., 2001; Eydeland & Wolyniec, 2003).

@practice evaluați o centrală pe gaze sau o baterie ca opțiuni, nu ca marjă medie înmulțită cu 8 760 h.

## Marjele orare ordonate: valoarea stă în orele cele mai bune {h=a651d103}

Dacă ordonăm descrescător marjele orare din ultimele 12 luni, obținem o curbă de durată. Aria de deasupra lui zero este valoarea opțiunii de a funcționa: ea se cîștigă într-o minoritate de ore foarte profitabile. La aceleași prețuri ale gazelor și carbonului, România are mai multe ore profitabile decît Germania.

Pentru acoperire, această formă contează: venitul centralei vine din orele de vîrf, așa că un contract în bandă, care vinde toate orele la fel, nu i se potrivește.

@practice acoperiți o centrală flexibilă cu produse de vîrf, nu cu bandă.

@chart spark_hourly
Clean spark spread orar din ultimele 12 luni, ordonat descrescător, pentru România și Germania, în EUR/MWh.

## @end

O centrală termoelectrică este expusă diferenței dintre prețul energiei, al combustibilului și al carbonului. Marja medie îi subestimează valoarea, pentru că o centrală flexibilă este o serie de opțiuni orare care plătesc doar în orele bune.

# Raportul de acoperire, riscul de bază și riscul de profil

Acoperirea se potrivește rareori exact cu expunerea: contractul se poate deconta în altă țară sau pe o bandă constantă, în timp ce consumul clientului are un profil. Secțiunea estimează cîte contracte trebuie deținute, măsoară riscul lăsat descoperit de contractele futures din Ungaria și Germania și evaluează profilul consumului și al producției solare.

## Raportul de acoperire optim este panta unei regresii {h=5e1b84fb}

Raportul de acoperire este numărul de contracte pe MWh expus care face costul acoperit cît mai stabil:

$$ h^{*}=\arg\min_h\Var(\Delta S-h\Delta F)=\rho\frac{\sigma_S}{\sigma_F}=\frac{\Cov(\Delta S,\Delta F)}{\Var(\Delta F)}, $$ {#eq:hstar}

$$ \Delta S_t=a+h\,\Delta F_t+\varepsilon_t,\qquad HE=\rho^2, $$ {#eq:ols}

unde $\Delta S$ și $\Delta F$ sînt variațiile lunare ale expunerii și ale instrumentului de acoperire, $\sigma_S$ și $\sigma_F$ abaterile lor standard, $\rho$ corelația lor, $a$ termenul liber, iar $\varepsilon_t$ eroarea regresiei din @eq:ols. Eficiența acoperirii (*hedge effectiveness*, HE) este ponderea varianței eliminate. Estimăm $h^{*}$ prin metoda celor mai mici pătrate (OLS); demonstrația se găsește în anexa A (Johnson, 1960; Ederington, 1979).

Ca instrumente folosim mediile lunare ale prețurilor din Ungaria și din DE-LU, pentru că un contract futures financiar ajunge la scadență la media lunară a zonei sale. Eșantionul are 133 de luni, din februarie 2015 pînă în octombrie 2026. Incertitudinea lui $h^{*}$ este măsurată în două feluri: cu o eroare standard HAC, cu 3 decalaje, și cu un bootstrap pe blocuri de 6 luni, cu 2 000 de replicări.

@practice un raport de acoperire fără interval de încredere este o simplă presupunere.

## Acoperirea cu contracte din alte zone: contractele din Ungaria sînt mai eficiente decît cele germane {h=5b3f9b4b}

Prețul din România urmează îndeaproape prețul din Ungaria: $h^{*}$ este 0,966, iar regresia explică 98% din varianța variațiilor lunare din România. Prețul german acoperă mai slab riscul: $h^{*}$ = 0,875, cu $R^2$ = 0,80, deci rămîne descoperită aproximativ o cincime din varianță.

| Instrument | $h^{*}$ | eroare std. HAC | bootstrap 95% | $R^2$ | $h^{*}$ 2015–20 | varianță eliminată, din 2021 |
|---|---|---|---|---|---|---|
| Ungaria | 0,966 | 0,023 | [0,93; 1,03] | 0,98 | 0,92 | 97,9% |
| Germania | 0,875 | 0,049 | [0,73; 1,01] | 0,80 | 0,91 | 81,1% |

Ultimele două coloane testează acoperirea în afara eșantionului: raportul estimat pe 2015–2020 este aplicat începînd din 2021. Chiar și în timpul crizei, acoperirea cu contracte din Ungaria a eliminat 97,9% din varianță, iar cea cu contracte germane 81,1%. Ambele intervale bootstrap conțin valoarea 1, deci o acoperire integrală, MW pentru MW, este acceptabilă statistic în ambele cazuri.

@practice folosiți contractele din Ungaria înaintea celor din Germania.

@chart hedge_scatter
Variațiile lunare ale prețului PZU din România în funcție de cele din Ungaria (stînga) și din Germania (dreapta), în EUR/MWh, cu dreapta raportului de acoperire estimat.

## Riscul de bază al unui contract din altă zonă {h=5867a38f}

Un furnizor din România acoperit cu un contract futures german plătește forward-ul german plus diferența de preț România–Germania de la livrare:

$$ \bar S^{\text{RO}}-h(\bar S^{X}-F^{X}_0)=hF^{X}_0+(\bar S^{\text{RO}}-h\bar S^{X}), $$ {#eq:basis}

unde $X$ este zona contractului (HU sau DE-LU), $\bar S^{\text{RO}}$ și $\bar S^{X}$ mediile lunare realizate ale prețurilor din România și din $X$, $F^{X}_0$ prețul de azi al contractului, iar $h$ raportul de acoperire. Termenul din paranteză este baza $b$; pentru $h=1$, ea este pur și simplu diferența lunară de preț dintre România și $X$, necunoscută în momentul acoperirii.

Față de Ungaria, baza este mică: media ei este −2,1 EUR/MWh, iar abaterea standard 4,5, iar cele două țări au avut prețuri egale în 56% din ore în 2021. Față de Germania, baza este mare: media +13,9, abaterea standard 15,2, iar din 2023 media este +18,7 EUR/MWh (Hull, 2022).

@practice o acoperire germană costă forward-ul german plus circa 19 EUR/MWh: includeți diferența în ofertă.

## Volatilitatea bazei a crescut după 2021, deși RO și HU au adesea același preț {h=b733a86d}

Abaterea standard a bazei lunare față de Germania a fost 7,6 EUR/MWh înainte de 2021 și 18,2 după. Panoul din dreapta numără orele în care România a avut același preț ca Ungaria sau Germania, ceea ce se întîmplă cînd liniile de interconexiune nu sînt congestionate și cuplarea piețelor egalizează prețurile. Etapele cuplării au fost Interim Coupling, la 17 iunie 2021, și cuplarea Core bazată pe fluxuri, la 8 iunie 2022 (ENTSO-E, 2021).

Cînd liniile sînt congestionate, prețurile se separă și baza crește. În practică, riscul de bază este deci riscul de congestie dintre zonele de ofertare.

@practice prețurile se egalizează doar fără congestie: riscul de bază este un risc de congestie.

@chart basis
Stînga: baza lunară, România minus Ungaria și România minus Germania, în EUR/MWh; dreapta: ponderea orelor din fiecare an cu același preț (diferență sub 0,01 EUR/MWh).

## Riscul de profil: clienții nu consumă în bandă {h=0f3beab3}

Un contract în bandă acoperă aceeași putere în fiecare oră, dar consumul este mai mare în orele scumpe, iar producția solară în cele ieftine. Factorii de profil măsoară această diferență:

$$ f^{\text{cons}}=\frac{\sum_h L_hP_h}{\bar P\sum_h L_h},\qquad f^{\text{solar}}=\frac{\sum_h Q_hP_h}{\bar P\sum_h Q_h}, $$ {#eq:shape}

unde $L_h$ este consumul României, iar $Q_h$ producția solară în ora $h$, $P_h$ prețul orei $h$, iar $\bar P$ media simplă a prețurilor din anul respectiv; $f^{\text{cons}}$ este factorul de profil al consumului. Un factor peste 1 înseamnă că profilul costă mai mult decît banda; sub 1, că valorează mai puțin.

Un furnizor care deservește profilul consumului național a avut un factor de 1,039 în 2019 și de 1,066 în 2025, adică, în 2025, +7,1 EUR/MWh peste bandă. Raportul de captare al unui producător solar a fost 1,045 în 2019, dar doar 0,596 în 2025: energia lui s-a vîndut cu 43,7 EUR/MWh sub bandă, pentru că foarte multe centrale solare produc acum în aceleași ore.

@practice evaluați un contract de achiziție pe termen lung (PPA) pentru un parc solar la raportul de captare ($f^{\text{solar}}$), nu la prețul benzii.

## Valoarea profilului solar și a profilului de consum față de bandă {h=de0b1889}

Graficul urmărește an de an cei doi factori din @eq:shape. Raportul de captare solar a scăzut la 0,596 în 2025, pe măsură ce prețurile de la prînz au coborît odată cu creșterea capacității solare; prețul ponderat cu consumul a ajuns, în 2025, cu 7,1 EUR/MWh peste bandă. Forward-ul în bandă acoperă deci prost riscul atît pentru un furnizor, cît și pentru un producător solar: primul rămîne subacoperit în orele scumpe, al doilea supraacoperit în cele ieftine.

@practice cumpărați bandă pentru baza portofoliului și produse de vîrf sau orare pentru profil.

@chart shape
Raportul anual dintre prețul ponderat cu consumul și prețul de bandă și dintre prețul capturat de solar și prețul de bandă, în România, din 2015 pînă la data-limită; linia orizontală marchează raportul 1.

## @end

Contractele din Ungaria acoperă aproape perfect prețurile din România, cele germane lasă descoperită o cincime din varianță și o bază costisitoare. Banda nu surprinde nici profilul consumului și al producției solare, care trebuie evaluat separat.

# Opțiuni pe energie

O opțiune protejează împotriva prețurilor mari (sau mici) și păstrează cîștigul dacă prețul evoluează în sens favorabil, în schimbul unei prime plătite azi. Secțiunea definește plafonul, pragul minim și collar-ul, le evaluează cu formula Black-76 pentru banda din 2027 din România și arată că parametrul esențial, volatilitatea, trebuie estimat și diferă după sursă.

## Plafon, prag minim și collar {h=035b0d24}

O opțiune call plafonează prețul de cumpărare și păstrează cîștigul dacă prețurile scad. Cîștigurile la scadență și prețul efectiv plătit cu un plafon sau cu un collar sînt

$$ (F_T-K)^+,\qquad (K-F_T)^+,\qquad \min(F_T,K_c)+c, $$ {#eq:payoffs}

$$ \text{collar: } \max\big(K_p,\min(F_T,K_c)\big)+c-p, $$ {#eq:collar}

unde $F_T$ este prețul forward la scadența $T$, $K$ prețul de exercitare, $(x)^+=\max(x,0)$, $c$ și $p$ primele opțiunilor call și put, $K_c$ prețul de exercitare al opțiunii call, iar $K_p<K_c$ cel al opțiunii put. Primul termen este cîștigul unei opțiuni call, al doilea al unei opțiuni put; collar-ul combină cumpărarea unei opțiuni call la $K_c$ cu vînzarea unei opțiuni put la $K_p$, astfel încît prima opțiunii put finanțează opțiunea call (Hull, 2022).

Furnizorul cumpără un plafon (*cap*, o opțiune call), producătorul un prag minim (*floor*, o opțiune put), iar amîndoi pot folosi un collar cu cost redus: furnizorul cumpără call și vinde put, producătorul invers. În România nu există opțiuni pe energie listate; plafoanele apar în contracte bilaterale și în PPA.

@practice cumpărați un plafon cînd un salt de preț ar pune firma în pericol, nu doar cînd i-ar reduce profitul.

## Modelul Black-76 evaluează o opțiune pe forward cu cinci parametri {h=31ffbfef}

În evaluarea neutră la risc, forward-ul nu are tendință, deci opțiunea depinde doar de $F$, $K$, $T$, $r$ și $\sigma$ (Black, 1976):

$$ C=e^{-rT}[F\Phi(d_1)-K\Phi(d_2)],\qquad P=e^{-rT}[K\Phi(-d_2)-F\Phi(-d_1)], $$ {#eq:black}

$$ d_1=\frac{\ln(F/K)+\sigma^2T/2}{\sigma\sqrt T},\qquad d_2=d_1-\sigma\sqrt T, $$ {#eq:d1}

unde $C$ și $P$ sînt primele opțiunilor call și put, $F$ prețul forward, $K$ prețul de exercitare, $T$ timpul pînă la scadență, în ani, $r$ rata dobînzii fără risc, cu capitalizare continuă, $\sigma$ volatilitatea anuală a lui $\ln F$, iar $\Phi$ funcția de repartiție normală standard. Demonstrația se găsește în anexa B.

Pentru banda din 2027 din România, datele de intrare sînt $F$ = 148,12 EUR/MWh (VWAP OPCOM), $T$ = 45 de zile, $r$ = 2,44% (€STR) și $\sigma$ = 0,220, estimată în secțiunea următoare. O opțiune la bani, cu $K=F$, costă 4,55 EUR/MWh, atît call, cît și put. Un plafon la 1,1 $F$ costă 0,63, iar un prag minim la 0,9 $F$ costă 0,43 EUR/MWh.

@practice întrebați banca ce volatilitate a folosit: prima crește aproape proporțional cu $\sigma$.

## Estimarea volatilității pentru evaluarea opțiunilor: estimările diferă în funcție de sursa datelor {h=c5b5f1f6}

Trei estimări pe date reale dau rezultate foarte diferite. Prima folosește contractele forward anuale din România. Licitațiile sînt neregulate, așa că varianța se calculează pe unitatea de timp:

$$ \hat\sigma^2=\frac{\sum_k(\Delta\ln F_k)^2}{\sum_k\Delta t_k}, $$ {#eq:volest}

unde $\Delta\ln F_k$ este variația logaritmică a prețului forward între două zile consecutive cu licitații $k$, aflate la cel mult 30 de zile una de alta, iar $\Delta t_k$ timpul dintre ele, în ani. Din 49 de perechi de zile cu licitații rezultă $\hat\sigma$ = 0,220.

A doua folosește contractul futures TTF pentru ianuarie 2027: pe ultimele 60 de zile de tranzacționare, $\hat\sigma$ = 0,499, iar opțiunea call la bani valorează 10,30 EUR/MWh. A treia compară media lunară realizată cu prețul forward cumpărat înainte: abaterea standard a lui $\ln(\bar S/F)/\sqrt T$ este 0,668, pe 153 de licitații.

Diferențele au explicații clare. Un an este media a 8 760 de ore și este mult mai stabil decît o lună; gazele trec printr-o criză proprie în 2026; iar pentru România nu există o volatilitate implicită disponibilă gratuit. O soluție mai bună este prognoza volatilității cu modelele de heteroscedasticitate condiționată autoregresivă generalizată (GARCH) din cursul 3.

@practice alegeți volatilitatea potrivită activului suport: an, trimestru sau lună.

## Contractele apropiate de livrare variază mai mult: efectul Samuelson {h=c519e1d5}

Contractele apropiate de livrare reacționează mai puternic la știri decît cele îndepărtate, pentru că un șoc asupra ofertei de azi afectează complet luna apropiată și doar parțial pe cea îndepărtată (Samuelson, 1965). Graficul compară volatilitatea pe 60 de zile a două contracte TTF. Între 1 noiembrie 2025 și 31 octombrie 2026, contractul pentru decembrie 2026 a avut o volatilitate anualizată de 63%, iar cel pentru mai 2027 de 48%. În 2022, în vîrful crizei, ambele au fost în jur de 66%.

Pentru evaluarea opțiunilor, aceasta înseamnă că o singură valoare a volatilității nu este suficientă: același activ suport are o volatilitate cu atît mai mare cu cît este mai aproape de livrare.

@practice o opțiune apropiată de livrare cere o volatilitate mai mare.

@chart samuelson
Volatilitatea pe o fereastră mobilă de 60 de zile de tranzacționare, în procente pe an, pentru contractele futures NYMEX TTF cu livrare în decembrie 2026 și mai 2027.

## Delta și vega: echivalentul în MWh forward și sensibilitatea la volatilitate {h=011daa6f}

Delta este cantitatea de forward care compensează opțiunea; vega este variația primei la un punct de volatilitate:

$$ \Delta_C=e^{-rT}\Phi(d_1),\qquad \Delta_P=-e^{-rT}\Phi(-d_1), $$ {#eq:delta}

$$ \mathcal V=e^{-rT}F\varphi(d_1)\sqrt T,\qquad C-P=e^{-rT}(F-K), $$ {#eq:vega}

unde $\Delta_C$ și $\Delta_P$ sînt delta opțiunii call și a opțiunii put, $\varphi$ densitatea normală standard, $\mathcal V$ vega, exprimată pe un punct de volatilitate (0,01), iar celelalte simboluri sînt cele din @eq:black și @eq:d1. Ultima relație este paritatea put–call.

Pentru $K=F$ și $\sigma$ = 0,220, $d_1$ = 0,039, $\Delta_C$ = 0,514 și $\Delta_P$ = −0,483; vega este 0,207 EUR/MWh, iar $C=P$, cum cere paritatea atunci cînd $K=F$. Un plafon la 1,1 $F$ are delta 0,116: se comportă ca aproximativ o zecime de MWh forward. Prima lui pentru 1 MW pe un an este 5 519 EUR (Black, 1976; Hull, 2022).

@practice vînzătorul plafonului se acoperă deținînd contracte forward într-o cantitate egală cu delta, pe care o ajustează periodic.

## Prețul efectiv al benzii pentru 2027 cu fiecare instrument {h=49feb87c}

Graficul compară prețul efectiv plătit de un furnizor pentru banda din 2027 cu fiecare strategie, în funcție de prețul forward la scadență. Fără acoperire, plătește prețul pieței. Cu forward-ul, plătește 148,1 EUR/MWh orice s-ar întîmpla. Cu un plafon la 162,9, plătește prețul pieței pînă la prețul de exercitare, plus o primă de 0,63 EUR/MWh. Un collar între 133,3 și 162,9 costă net doar 0,20 EUR/MWh, pentru că opțiunea put vîndută finanțează cea mai mare parte a opțiunii call, dar renunță la cîștigul de sub 133,3.

Prețurile Black-76 sînt un reper, nu prețul pe care l-ar cota o bancă: salturile de preț și opțiunile pe medii lunare (opțiuni asiatice) încalcă ipotezele modelului (Weron, 2008).

@practice un collar cu cost aproape zero permite furnizorului să ofere un preț plafonat.

@chart collar
Prețul efectiv al benzii pentru 2027, în EUR/MWh, în funcție de prețul forward la scadență $F_T$: fără acoperire, forward la prețul $F$, plafon la $K$ = 1,1 $F$ și collar 0,9 $F$ – 1,1 $F$.

## @end

Opțiunile transformă un preț fix într-o asigurare: plafonul protejează furnizorul, pragul minim producătorul, iar collar-ul pe amîndoi, cu un cost redus. Prețul lor depinde mai ales de volatilitate, care trebuie să corespundă contractului acoperit.

# Studiu de caz: un furnizor și un producător din România

Acest studiu de caz aplică instrumentele cursului pe prețurile reale din 2026: un furnizor cu un client de 1 MW la preț fix compară patru strategii de acoperire, iar un producător analizează cît l-a costat sau cît a economisit vînzarea forward în 2022, 2024 și 2025. Secțiunea se încheie cu o politică de acoperire pe care o poate adopta consiliul de administrație.

## Studiul de caz: un furnizor cu un client de 1 MW la preț fix, 2026 {h=6b1ede43}

Furnizorul a vîndut 1 MW în bandă, la preț fix, pentru tot anul 2026, iar energia trebuie încă cumpărată. Rezultatul este evaluat pe cele 10 luni deja livrate, pînă în octombrie 2026, cu prețuri reale, pentru patru strategii:

- **Fără acoperire**: cumpără lunar la media spot realizată.
- **100% forward**: cumpără banda OPCOM pentru 2026, la un VWAP de 111,70 EUR/MWh, din 31 de licitații.
- **50% forward, 50% spot**.
- **Plafoane lunare** cumpărate la 15 decembrie 2025, cu prețul de exercitare $K$ = 120,16 EUR/MWh (VWAP-ul ultimelor 5 licitații), evaluate cu Black-76 și $\sigma$ = 0,668.

Pentru fiecare strategie, studiul de caz raportează costul mediu, abaterea lui standard de la o lună la alta, cea mai scumpă lună și costul total pe MW.

@practice comitetul de risc al unui furnizor ar trebui să vadă lunar exact acest calcul.

## Studiul de caz: în 2026, forward-ul a fost mai ieftin în 6 din 10 luni {h=20ac1702}

Graficul arată costul lunar al fiecărei strategii. Prețurile au crescut în cursul anului, iar spotul a atins maximul de 239,3 EUR/MWh în octombrie 2026; în 6 din cele 10 luni, forward-ul a fost mai ieftin decît spotul. Plafoanele s-au exercitat în 5 din 10 luni, cînd spotul lunar a depășit prețul de exercitare, dar prima lor s-a plătit în fiecare lună.

@practice prima plafonului se plătește în fiecare lună, chiar și atunci cînd opțiunea nu se exercită.

@chart case2026
Costul lunar pentru 1 MW în bandă în 2026, în EUR/MWh, cu patru strategii: fără acoperire (spot), 100% forward, 50% forward și 50% spot, plafoane lunare la prețul de exercitare $K$.

## Studiul de caz: forward-ul a redus costul și riscul, iar plafonul doar riscul {h=c67a5902}

Tabelul rezumă cele patru strategii, ponderate cu numărul de ore al fiecărei luni.

| EUR/MWh | media | abat. std. | maxim | EUR/MW |
|---|---|---|---|---|
| spot | 137,5 | 44,4 | 239,3 | 1 002 956 |
| 100% forward | 111,7 | 0,0 | 111,7 | 814 946 |
| 50% forward | 124,6 | 22,2 | 175,5 | 908 951 |
| plafoane | 133,6 | 13,9 | 148,5 | 975 020 |

Acoperirea integrală cu forward a economisit 188 010 EUR pe MW și a eliminat complet variația de la o lună la alta. Plafoanele au avut o primă medie de 20,4 EUR/MWh pe lună, dar au adus totuși o economie netă de 27 936 EUR pe MW și au redus costul celei mai scumpe luni de la 239,3 la 148,5 EUR/MWh. Acoperirea pe jumătate se situează între cele două.

Rezultatul nu este o regulă generală. În 2026, prețurile au crescut după acoperire; într-un an cu prețuri în scădere, forward-ul costă mai mult decît spotul, iar plafoanele și-ar pierde prima.

@practice stabiliți ponderea acoperită prin politică (de exemplu 60–80%, eșalonat), nu după o opinie despre prețuri.

## Perspectiva producătorului și saltul de preț din vara lui 2024 {h=a8b5e7e9}

Pentru un producător, situația este inversă. În 2025, 101 licitații au vîndut banda la un VWAP de 102,1 EUR/MWh, în timp ce media spot realizată a fost 108,2: vînzarea forward a adus cu 6,0 EUR/MWh mai puțin decît spotul, adică 52 797 EUR pe MW și an. Acesta este prețul unui venit sigur. În 2022, aceeași decizie a costat 187,9 EUR/MWh.

Vara lui 2024 arată riscul opus, pentru cumpărători. Contractul pentru trimestrul al treilea s-a tranzacționat la 90,0 EUR/MWh, iar media spot realizată a fost 127,4; numai în iulie, 145,1. Ora cea mai scumpă a costat 916,7 EUR/MWh, pe 18 iulie 2024, la ora 20:00, ora Europei Centrale (CET) (Andrei, Pele & Cramer, 2026).

Concluzia este că acoperirea transferă valoare între cele două părți ale pieței. Avantajul ei este că fluxurile de numerar devin previzibile, iar creditorii răsplătesc această previzibilitate prin condiții de finanțare mai bune.

@practice un producător îndatorat ar trebui să vîndă forward chiar dacă se așteaptă la prețuri mai mari.

## Elementele unei politici de acoperire a riscului {h=99cc3725}

Cursul poate fi rezumat într-o politică de acoperire cu patru componente:

- **Expunerea**: măsurați poziția netă pe lună și pe profil (bandă, vîrf, solar) și tratați separat riscul de volum, pentru că cererea reacționează foarte puțin la preț (Proșcanu, Proșcanu & Pele, 2025).
- **Instrumentele**: întîi forward-uri OPCOM, apoi contracte futures din Ungaria, apoi din Germania; plafoane pentru valorile extreme, nu pentru tot volumul.
- **Execuția**: cumpărați eșalonat, pe 12–24 de luni, și păstrați o rezervă de lichiditate pentru apelurile în marjă.
- **Controlul**: stabiliți limite pentru poziția deschisă și pentru VaR (cursul 4) și raportați costul acoperit și varianța lui.

@practice consiliul aprobă politica, traderii o execută, departamentul de risc o măsoară.

## @end

În 2026, forward-ul a redus atît costul, cît și riscul unui furnizor din România, iar plafoanele au redus riscul în schimbul unei prime; în 2025, un producător a plătit un preț mic pentru un venit sigur. Pentru că semnul cîștigului se schimbă de la un an la altul, ponderea acoperită trebuie stabilită prin politică.

# Recapitulare

Recapitularea verifică principalele instrumente ale cursului pe cifre reale din România și propune lecturi suplimentare.

## Verifică-te {h=066a0a98}

1. Un furnizor din România și-a acoperit luna iulie 2024 cu contracte futures germane în bandă, cumpărate la prețul $F$. Media lunii a fost 67,7 EUR/MWh în Germania și 145,1 în România. Cît a plătit pe MWh? Răspuns: a cumpărat la 145,1 în România și a primit din contractul futures diferența dintre 67,7 și $F$, deci costul net a fost $F$ + 77,4 EUR/MWh, cea mai mare bază lunară din datele noastre.
2. Estimarea noastră pentru Ungaria este $h^{*}$ = 0,966, cu intervalul bootstrap [0,93; 1,03]. Cîți MW de contracte futures din Ungaria acoperă o expunere de 20 MW? Răspuns: 20 × 0,966 = 19,3 MW; deoarece valoarea 1 se află în interval, o acoperire integrală ($h=1$), de 20 MW, este la fel de bună din punct de vedere statistic.
3. În octombrie 2026, energia a costat 239,3 EUR/MWh, gazele 86,8 EUR/MWh, iar EUA 82,4 EUR/t, cu un randament de 50% și 0,202 t CO$_2$ pe MWh termic. A cîștigat, în medie, o centrală pe gaze? Răspuns: combustibilul costă 86,8/0,5 = 173,6, iar carbonul 0,404 × 82,4 = 33,3, deci clean spark spread este +32,4 EUR/MWh: da, chiar înainte de a alege orele cele mai bune.
4. Banda pentru 2027 se tranzacționează la 148,1 EUR/MWh, iar un plafon la 162,9 costă 0,63 EUR/MWh. Cît plătește furnizorul dacă prețul forward ajunge la 1,3 $F$, respectiv la 0,9 $F$? Răspuns: la 1,3 $F$ plătește prețul de exercitare, 162,9, plus prima; la 0,9 $F$ plătește prețul pieței plus prima, deoarece plafonul nu se exercită.

## Recapitulare {h=f7f48443}

Un contract forward transformă un preț spot necunoscut într-un preț cunoscut. În 2022, i-a adus unui furnizor din România o economie de 1,65 milioane EUR pe MW, iar producătorii care au vîndut forward au pierdut aceeași sumă. Regulile practice ale cursului sînt: acoperiți riscul din România cu contracte din Ungaria, înaintea celor din Germania; includeți profilul consumului și al producției solare în preț; alegeți volatilitatea potrivită activului suport atunci cînd evaluați o opțiune. Urmează cursul 6.

## Cercetările grupului nostru despre riscul pe piața energiei din România {h=63ce4b82}

Trei lucrări recente ale grupului nostru, de la Academia de Studii Economice din București și de la Academia Română, Institutul de Prognoză Economică, studiază riscul pe piața energiei din România:

- **Saltul de preț din vara lui 2024** (Andrei, Pele & Cramer, 2026). Lucrarea analizează ce intervenție ar fi redus cel mai mult prețurile din România în iunie–iulie 2024. Folosește o pădure aleatoare (*random forest*) pe date orare ENTSO-E, cu 147 de scenarii contrafactuale, verificate cu o regresie ridge. Reducerea consumului cu 10% este cea mai eficientă măsură; vîrful a avut loc noaptea, deci energia solară nu putea ajuta, iar stocarea devine esențială.
- **Riscul sistemic în sectorul energetic din UE** (Toma, Dima, Grecu, Pele & Lessmann, 2026). Lucrarea construiește indicatorul Energy Financial Risk Meter, printr-o regresie cuantilică cu operatorul de contracție și selecție în normă absolută (LASSO), pe randamentele zilnice a 100 de companii energetice europene. Indicele surprinde pandemia din 2020 și războiul din 2022 și arată activarea unui canal de transmitere a riscului geopolitic către sectorul energetic.
- **Cererea reacționează foarte puțin la preț** (Proșcanu, Proșcanu & Pele, 2025). Cu ajutorul cauzalității Granger și al modelelor vectoriale autoregresive pe consumul și prețurile din România, lucrarea arată că consumul este inelastic și influențează prețul, nu invers; de aceea, volumul nu poate compensa riscul de preț.

Rezultatele sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.

## Lecturi și resurse suplimentare {h=e0b63cde}

- J. Hull, *Options, Futures, and Other Derivatives*: capitolele despre acoperirea riscului, contractele futures și modelul Black.
- Benth, Šaltytė Benth & Koekebakker (2008): curbe forward și opțiuni pe piețele de energie electrică.
- Rapoartele OPCOM: rezultatele licitațiilor forward, sursa acestui curs — [opcom.ro](https://www.opcom.ro/rapoarte-pccb-le-flex-rez-pccb-le-flex/ro).
- Acest curs: cod, date și notebook-uri Jupyter — [github.com/danpele/EMQA](https://github.com/danpele/EMQA).
- ACER (2022): evaluarea finală a modelului pieței angro de energie electrică din UE.
- Exercițiu practic: notebook-ul Jupyter reproduce toate graficele și cifrele din acest curs, în dosarul notebooks al depozitului cursului.

# Anexă

Anexa prezintă demonstrațiile din spatele raportului de acoperire și al formulei Black-76, precum și convențiile folosite la construirea datelor.

## Anexa A: raportul de acoperire cu varianță minimă și estimarea lui {h=99e9520b}

Anulînd derivata varianței acoperite în raport cu $h$, obținem raportul de acoperire din @eq:hstar:

$$ \frac{\partial}{\partial h}\Var(\Delta S-h\Delta F)=-2\Cov(\Delta S,\Delta F)+2h\Var(\Delta F)=0\ \Rightarrow\ h^{*}=\frac{\Cov(\Delta S,\Delta F)}{\Var(\Delta F)}, $$ {#eq:foc}

$$ \Var(\Delta S-h^{*}\Delta F)=\sigma_S^2(1-\rho^2), $$ {#eq:resvar}

unde simbolurile sînt cele din @eq:hstar. A doua derivată, $2\Var(\Delta F)>0$, deci $h^{*}$ este un minim, iar @eq:resvar arată că ponderea varianței eliminate este $\rho^2$, adică eficiența acoperirii. $h^{*}$ este panta OLS a regresiei lui $\Delta S$ pe $\Delta F$, cu varianță HAC (Newey–West, nucleu Bartlett, 3 decalaje).

Bootstrap-ul pe blocuri mobile extrage cu întoarcere blocuri de cîte 6 luni consecutive pînă la $n$ luni, mărimea eșantionului, recalculează $h^{*}$ și repetă procedura de 2 000 de ori. Intervalul de 95% este dat de percentilele de 2,5% și 97,5%; blocurile păstrează autocorelarea variațiilor lunare. Un raport de acoperire dinamic, $h_t^{*}=\Cov_{t-1}/\Var_{t-1}$, se poate obține dintr-un model GARCH bivariat (cursul 3), cu covarianța și varianța pentru perioada $t$ prognozate pe baza informației disponibile pînă la $t-1$ (Johnson, 1960; Ederington, 1979; Kroner & Sultan, 1993).

## Anexa B: de la un preț forward fără tendință la formula Black-76 {h=3876c854}

Intrarea într-un contract forward nu costă nimic, deci, în evaluarea neutră la risc, tendința lui este zero:

$$ \frac{dF_t}{F_t}=\sigma\,dW_t\ \Rightarrow\ \ln F_T\sim\mathcal N\big(\ln F_0-\tfrac12\sigma^2T,\ \sigma^2T\big), $$ {#eq:gbm}

$$ C=e^{-rT}\E\big[(F_T-K)^+\big]=e^{-rT}\big[F_0\Phi(d_1)-K\Phi(d_2)\big], $$ {#eq:callexp}

unde $W_t$ este o mișcare browniană standard, $F_0$ prețul forward de azi, iar celelalte simboluri sînt cele din @eq:black. Rezultatul decurge din două momente ale repartiției lognormale: $\E[F_T\mathbf 1_{F_T>K}]=F_0\Phi(d_1)$ și $\Pr(F_T>K)=\Phi(d_2)$ (Black, 1976).

Două extensii sînt importante pentru energie. Opțiunea de a schimba gazele în energie electrică se evaluează cu formula Margrabe (Margrabe, 1978), cu volatilitatea $\sigma^2=\sigma_P^2+\sigma_G^2-2\rho\sigma_P\sigma_G$, unde $\sigma_P$ și $\sigma_G$ sînt volatilitățile energiei și ale gazelor, iar $\rho$ corelația lor; dacă există și un preț de exercitare, de exemplu costurile variabile ale centralei, în practică se folosește aproximarea Kirk. În plus, prețul spot al energiei revine la medie: modelul cu un factor al lui Schwartz (1997) dă volatilități forward care scad cu scadența, în acord cu efectul Samuelson.

## Anexa C: convenții și factori de conversie {h=7377ce5c}

- **Prețurile forward**: un preț de închidere pentru fiecare sesiune OPCOM; volumul tranzacționat, înregistrat pe partea inițiatorului licitației; conversia din lei cu cursul EUR/RON al BCE din ziua licitației (ultimul curs disponibil pînă la acea zi). Folosim numai perioade standard: lună, trimestru, semestru și an calendaristic, în bandă, dacă nu se precizează altfel.
- **Spotul realizat**: media prețurilor zilnice în bandă de pe PZU din perioada de livrare, pe zile CET, calculată numai dacă toate zilele sînt disponibile.
- **Combustibili și carbon**: cărbunele de 6 000 kcal/kg echivalează cu 6,978 MWh termic pe tonă; gazele emit 0,202, iar cărbunele 0,341 t CO$_2$ pe MWh termic (IPCC 2006: 56,1 și 94,6 t pe terajoule, TJ). EUA este media lunară a licitațiilor EEX pînă în ianuarie 2026, apoi titlul SparkChange ETC; raportul dintre prețul de licitație și cel al titlului ETC a fost apropiat de 1 în 2021–2025.
- **Ore**: folosim echivalentul orar, astfel că un interval de 15 minute contează ca 0,25 h (din 1 octombrie 2025).
