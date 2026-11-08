<!--
Versiunea web a cursului 1 (RO). Construită în web/L1_ro.html de lectures/common/build_web_lecture.py (formatul: vezi docstring-ul).
Hash-urile slide-urilor: python3 build_web_lecture.py 1 --frames
-->

## @intro

În fiecare zi, o singură licitație stabilește cît va costa energia electrică în România pentru fiecare sfert de oră din ziua următoare. Un furnizor care cumpără pentru clienții săi, un producător hidro care decide cînd să turbineze apa din lac, o fabrică ce își poate muta o parte din consum și un trader care exportă în Ungaria pornesc toți de la aceeași cifră: prețul de pe Piața pentru Ziua Următoare (PZU), administrată de operatorul pieței de energie electrică și gaze naturale din România (OPCOM). Acest prim curs explică modul în care se formează acest preț, legătura pieței românești cu restul Europei și forma seriei de prețuri după ce a fost descărcată, curățată și măsurată corect.

Cursul folosește numai date reale, descărcate la 4 noiembrie 2026, pînă la 31 octombrie 2026: prețurile pentru ziua următoare din România, Bulgaria, Ungaria și Germania–Luxemburg, producția României pe surse și consumul, fluxurile transfrontaliere, prețul futures al țițeiului Brent și prețul gazelor din Țările de Jos. Pe aceste date documentăm faptele stilizate pe care orice model ulterior trebuie să le reproducă: saltul din 2021–2022, sezonalitatea săptămînală și anuală, minimul de preț de la amiază creat de producția solară, salturile de preț, prețurile negative, cozile groase și gruparea volatilității. Construim apoi instrumentele de bază ale analizei seriilor de timp (staționaritate, autocorelație, teste de rădăcină unitară, descompunere, netezire) și prognoza naivă pe care orice model trebuie să o depășească, iar la final analizăm șase studii de caz pe episoade recente, de la anul secetos 2025 pînă la noile baterii din Bulgaria, în 2026.

@goals
- **Explicați** cum o singură licitație pentru ziua următoare stabilește un preț pentru fiecare oră (acum pentru fiecare sfert de oră) și cum cuplarea piețelor europene leagă România de vecinii săi.
- **Calculați și interpretați** mixul de producție al României din date măsurate, împreună cu gradul lor de acoperire.
- **Recunoașteți** faptele stilizate ale prețurilor energiei electrice pe date reale și alegeți o transformare care funcționează și cînd prețurile sînt nule sau negative.
- **Folosiți** instrumentele de bază ale analizei seriilor de timp și prognoza naivă, reperul pe care orice prognoză trebuie să-l depășească.
- **Analizați** cantitativ șase episoade recente, de la anul secetos 2025 pînă la noile baterii din Bulgaria, în 2026.

# Piețele de energie electrică din România și Europa

Prețul energiei electrice din România se stabilește printr-o singură licitație zilnică, cuplată cu restul Europei, care din octombrie 2025 produce un preț pentru fiecare sfert de oră. Secțiunea prezintă licitația, ordinea de merit, etapele tranzacționării pentru o zi de livrare, instituțiile care stabilesc regulile, cuplarea piețelor și mixul de producție al României.

## Numai date reale: surse și perioadă acoperită {h=1b3bac7b}

Toate cifrele și graficele acestui curs provin din date descărcate. Prețurile provin de la patru burse: OPCOM pentru România, bursa independentă de energie din Bulgaria (IBEX), bursa de energie din Ungaria (HUPX) și European Power Exchange (EPEX SPOT) pentru Germania; ele sînt colectate prin Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E) și republicate de energy-charts.info, portalul de date al Institutului Fraunhofer pentru Sisteme de Energie Solară (ISE).

| Serie | Frecvență | Sursă | Început |
|---|---|---|---|
| Prețurile pentru ziua următoare: România (RO), Bulgaria (BG), Ungaria (HU), Germania–Luxemburg (DE-LU) | 15/60 min | energy-charts.info (Fraunhofer ISE) | 2015-01-01 |
| Producția pe surse și consumul, România și Bulgaria | orară | energy-charts.info, ENTSO-E (producția efectivă) | 2015-01 |
| Fluxurile fizice transfrontaliere ale României | orară | energy-charts.info, ENTSO-E | 2015-01-01 |
| Țiței Brent, contractul futures cel mai apropiat | zilnică | Yahoo Finance (BZ=F) | 2015-01-02 |
| Gaze naturale, hubul Title Transfer Facility (TTF) | lunară | Banca Mondială; cursurile de schimb ale Băncii Centrale Europene (ECB) | 2015-01 |

Datele se opresc la 31 octombrie 2026, ultima lună completă, și au fost descărcate la 4 noiembrie 2026. Ori de cîte ori cursul folosește formularea „2026, de la începutul anului (YTD)”, aceasta înseamnă perioada ianuarie–octombrie 2026. Valorile lipsă rămîn lipsă: nu se interpolează și nu devin zero, iar fiecare total este raportat împreună cu gradul de acoperire, adică ponderea orelor pentru care există date.

## Prețul de închidere a pieței: intersecția cererii cu oferta {h=0cd5093f}

Pe piața pentru ziua următoare, vînzătorii și cumpărătorii depun oferte de preț și cantitate pentru fiecare interval de livrare din ziua următoare. Bursa determină prețul la care cantitatea oferită egalează cantitatea cerută, iar toate tranzacțiile acceptate se decontează la acest preț unic:

$$ p_t^{*}=\min\big\{p:\ S_t(p)\ \ge\ D_t(p)\big\} $$ {#eq:clearing}

unde $t$ este sfertul de oră de livrare (ora de livrare, pînă în octombrie 2025), $S_t(p)$ este curba ofertei, adică energia oferită la prețuri de cel mult $p$, cu centralele ordonate după cost (*ordinea de merit*: regenerabilele și nuclearul la bază, gazele spre vîrf), $D_t(p)$ este curba cererii, adică energia cumpărată la prețuri de cel puțin $p$, iar $p_t^{*}$ este prețul de închidere a pieței, în euro pe megawatt-oră (EUR/MWh).

Conform datelor noastre, prețul mediu pe PZU a fost de 137,45 EUR/MWh în ianuarie–octombrie 2026. În România, hidrocentralele cu lac de acumulare ofertează la „valoarea apei”, adică la costul de oportunitate al folosirii apei acum și nu mai tîrziu, și fixează adesea prețul. Același mecanism explică cele două extreme ale prețurilor: cînd cererea ajunge pe porțiunea abruptă a curbei ofertei, apar salturi de preț (*spikes*); cînd producția inflexibilă și cea solară depășesc cererea, prețul devine negativ (Weron, 2014; Maciejowska, Uniejewski & Weron, 2023).

@practice pe PZU, un furnizor plătește prețul fixat de centrala marginală, nu costul mediu al sistemului.

## Mecanismul ordinii de merit: cum se formează prețul {h=eed11756}

Oferta din licitație este o listă de oferte de vînzare ordonate de la cea mai ieftină la cea mai scumpă. Fiecare producător ofertează în jurul costului său marginal, adică al costului unui MWh în plus. Ordinea obișnuită este: eolian, solar și nuclear, cu un cost marginal aproape de zero, apoi hidro pe firul apei, lignit și, la final, gaze. Hidrocentralele cu lac fac excepție: ele ofertează la valoarea apei, prețul pe care se așteaptă să-l obțină mai tîrziu pentru aceeași apă. Cererea este lista ofertelor de cumpărare, ordonate de la prețul cel mai mare la cel mai mic; deoarece cea mai mare parte a consumului se cumpără la orice preț, curba cererii este aproape verticală.

Prețul îl stabilește ultima ofertă acceptată, cea marginală, și toți vînzătorii acceptați îl primesc, inclusiv cei cu costuri mult mai mici. Diferența dintre preț și costul lor, renta inframarginală, este cea care le acoperă investiția în capacitate. Tot de aici se vede de ce variază prețul: soarele și vîntul deplasează curba ofertei spre dreapta și reduc prețul, în timp ce cererea de seară sau oprirea unui reactor nuclear mută intersecția pe porțiunea abruptă, a centralelor pe gaze, și îl cresc.

@practice prețul unui sfert de oră este dat de cea mai scumpă ofertă acceptată, nu de costul mediu al sistemului.

## Ordinea de merit pe curbele reale OPCOM, 21 octombrie 2026 {h=95afa9d4}

Graficul prezintă curbele agregate ale cererii și ofertei publicate de OPCOM pentru PZU, în două sferturi de oră din aceeași zi, 21 octombrie 2026. Cantitățile includ ofertele bloc, ofertele orare și fluxurile transfrontaliere nete, deci sînt chiar curbele pe care licitația le-a intersectat.

La amiază, 2 333 MW erau oferiți la preț zero sau negativ, în cea mai mare parte producție solară, eoliană, nucleară și hidro pe firul apei, care funcționează oricum, iar piața s-a închis la 152,23 EUR/MWh. Seara nu mai era soare, oferta conținea 1 054 MW import net, iar intersecția s-a mutat pe porțiunea abruptă a curbei: prețul a fost de 244,00 EUR/MWh. Diferența dintre cele două prețuri din aceeași zi nu este zgomot, ci reflectă forma curbei ofertei la două niveluri diferite ale producției din surse regenerabile.

@practice un consumator care își mută consumul de seara la amiază plătește prețul de închidere mai mic.

@chart merit_opcom
Curbele agregate ale cererii și ofertei pe PZU (prețul în EUR/MWh în funcție de cantitatea cumulată, în GW) pentru un sfert de oră de la amiază și unul de seară din 21 octombrie 2026, cu punctul de închidere marcat pe fiecare.

## Etapele tranzacționării pentru o zi de livrare {h=ca78da83}

Licitația pentru ziua următoare este doar una dintre cele patru etape prin care trece o zi de livrare. Mai întîi, cu săptămîni sau ani înainte, energia se cumpără și se vinde la termen, pe piețele centralizate ale OPCOM sau prin contracte bilaterale negociate direct (OTC). Apoi, în ziua $d-1$, ofertele se transmit pe PZU pînă la termenul-limită de la ora 12:00, ora Europei Centrale (CET), adică 13:00 la București; rezultatele apar la începutul după-amiezii. În a treia etapă, în zilele $d-1$ și $d$, pozițiile se ajustează prin licitații intrazilnice (IDA) și prin tranzacționare continuă pînă aproape de livrare. În sfîrșit, în ziua $d$, în timp real, Transelectrica, operatorul de transport și de sistem (TSO), echilibrează sistemul, iar abaterile de la programul notificat se decontează ca dezechilibre, la 15 minute.

Două detalii practice contează în lucrul cu datele. România folosește ora Europei de Est (EET), cu o oră înaintea CET, iar în cuplarea unică a piețelor pentru ziua următoare (SDAC) prețurile se exprimă în EUR, deși OPCOM le publică și în lei (RON). Contează și ordinea etapelor: fiecare o corectează pe cea anterioară, astfel că ce nu s-a contractat la termen se cumpără pe PZU, iar ce rămîne neacoperit după piața intrazilnică se decontează ca dezechilibru (Maciejowska, Uniejewski & Weron, 2023).

@practice traderul își acoperă riscul la termen, licitează pe PZU pînă la ora 13:00 (ora Bucureștiului), corectează erorile pe piața intrazilnică și decontează dezechilibrul rămas.

## Cine stabilește regulile: operatori, reglementatori, limite de preț, transparență {h=8354df6f}

Trei instituții din România dau forma pieței. OPCOM este operatorul desemnat al pieței de energie electrică (NEMO) și administrează PZU și piața intrazilnică. Transelectrica, în calitate de TSO, conduce sistemul în timp real și decontează dezechilibrele. Autoritatea Națională de Reglementare în Domeniul Energiei (ANRE) stabilește regulile la nivel național și licențiază participanții la piață.

Transparența este reglementată de Regulamentul Uniunii Europene (UE) privind integritatea și transparența pieței angro de energie (REMIT): informațiile privilegiate, de exemplu oprirea neplanificată a unei centrale mari, trebuie publicate fără întîrziere, iar asemenea mesaje influențează prețul PZU. Agenția UE pentru Cooperarea Autorităților de Reglementare din Domeniul Energiei (ACER) supraveghează piața pentru a depista abuzurile. Prețurile au și limite: prețul minim armonizat în SDAC era de $-500$ EUR/MWh și a devenit $-600$ EUR/MWh pentru livrările începînd cu 29 mai 2026. O serie care atinge pragul este cenzurată, deoarece prețul de echilibru ar fi fost și mai mic; un model care tratează pragul ca pe o observație obișnuită subestimează cît de extremă a fost situația.

@practice citiți mesajele REMIT înainte de a licita: o oprire neplanificată anunțată la timp schimbă prețul PZU.

## Cuplarea piețelor: exporturi spre zonele cu prețuri mari, pînă la limita rețelei {h=6a874611}

Europa organizează o singură licitație comună pentru ziua următoare. Conceptual, algoritmul alege cantitățile cumpărate și vîndute în fiecare zonă de ofertare astfel încît să maximizeze bunăstarea totală, adică valoarea pentru cumpărători minus costul vînzătorilor, în limitele rețelei:

$$ \max\sum_{z}\Big[\int_0^{d_z} D_z^{-1}-\int_0^{s_z} S_z^{-1}\Big]\quad \text{cu restricția }\ \text{fluxuri}\in\mathcal F $$ {#eq:coupling}

unde $z$ este zona de ofertare, $d_z$ și $s_z$ sînt energia cumpărată, respectiv vîndută în $z$, $D_z^{-1}$ și $S_z^{-1}$ sînt inversele curbelor cererii și ofertei (valoarea pentru cumpărători și costul vînzătorilor pentru fiecare MWh), iar $\mathcal F$ este mulțimea schimburilor fezabile între zone. Zonele cu prețuri mici exportă către cele cu prețuri mari pînă cînd se atinge o limită a rețelei. Dacă nicio limită nu este atinsă, prețurile sînt egale, $p_z=p_{z'}$; altfel, ele se separă.

Imaginea unei singure capacități pe fiecare graniță este o simplificare. Din 8 iunie 2022, la granița România–Ungaria se aplică alocarea *bazată pe fluxuri* din regiunea Core, cu limite pe elementele critice ale rețelei, în timp ce la granița România–Bulgaria se păstrează alocarea capacității pe graniță. De aici rezultă două precauții: prețurile egale nu dovedesc absența congestiilor pe interconexiune, iar o diferență de preț nu arată ce linie și-a atins limita. În plus, schimburile programate diferă de fluxurile fizice, iar drepturile de transport pe termen lung se alocă separat, prin Joint Allocation Office (JAO).

@practice pe RO–HU, un trader cîștigă din diferența de preț doar cînd interconexiunea este saturată.

## Zece ani de cuplare: de la patru țări la o licitație europeană {h=3254189f}

Piața românească s-a integrat treptat în cea europeană. În 2014, România s-a cuplat cu Cehia, Slovacia și Ungaria în 4M Market Coupling. La 19 noiembrie 2019 a aderat la cuplarea unică a piețelor intrazilnice (SIDC), iar la 17 iunie 2021 la SDAC, prin cuplarea interimară 4M. Granița Bulgaria–România a fost cuplată în SDAC la 27 octombrie 2021, iar la 8 iunie 2022 granița România–Ungaria a trecut la alocarea bazată pe fluxuri din regiunea Core. În martie 2025, granițele României au intrat în licitațiile intrazilnice, iar la 1 octombrie 2025 SDAC a trecut la intervalul de tranzacționare de 15 minute.

Toate prețurile se calculează cu algoritmul hibrid paneuropean de integrare a piețelor de energie electrică (EUPHEMIA). Pentru analist, concluzia este simplă: fiecare dintre aceste etape a schimbat datele, prin vecini noi, produse noi sau o rezoluție mai fină. Înainte de a compara două perioade, verificați care dintre aceste date se află între ele.

## Din 1 octombrie 2025, o zi are 96 de prețuri, nu 24 {h=f1734e1f}

Intervalul de tranzacționare (MTU) s-a redus de la o oră la 15 minute, așa că orice număr de intervale trebuie acum convertit în ore echivalente. Prețul mediu zilnic și numărul de ore cu preț negativ se calculează astfel:

$$ \bar p_d=\frac{1}{M_d}\sum_{m=1}^{M_d}p_{d,m},\qquad H_y=\sum_{t\in y}\mathbb 1\{p_t<0\}\cdot\frac{\Delta_t}{60} $$ {#eq:mtu}

unde $p_{d,m}$ este prețul intervalului $m$ din ziua $d$, $M_d$ este numărul de intervale din acea zi (96 din octombrie 2025, 24 înainte, cu unul în plus sau în minus în cele două zile în care se trece la ora de vară (DST) sau se revine de la ea), $\bar p_d$ este *prețul mediu zilnic al energiei în bandă*, $\mathbb 1\{p_t<0\}$ este 1 dacă prețul intervalului $t$ este negativ și 0 altfel, $\Delta_t\in\{60,15\}$ este durata intervalului în minute, iar $H_y$ este numărul de ore echivalente cu preț negativ din anul $y$.

Datele noastre conțin 94 222 de intervale orare pînă în septembrie 2025 și 38 020 de sferturi de oră de atunci. În ianuarie–octombrie 2026, România a avut 687 de sferturi de oră cu preț negativ, adică 171,75 ore. Dacă fiecare sfert de oră ar fi numărat ca o oră, durata ar fi supraevaluată de 4 ori, iar anul 2026 ar părea mult mai grav decît anii anteriori.

@practice întrebați mereu „ore sau sferturi de oră?” înainte de a compara anii între ei.

## Producția României: hidro, nuclear, gaze, cărbune și tot mai mult solar {h=d9aaba9b}

România produce energie electrică dintr-un mix diversificat. În grafic, producția hidro însumează centralele pe firul apei (RoR) și pe cele cu lac de acumulare, iar cărbunele însumează lignitul și huila. Bara neagră reprezintă consumul: cînd se află deasupra coloanei de producție, țara a fost importator net în anul respectiv. Energia este însumată pe orele raportate de TSO, cu o acoperire de cel puțin 98,1% în anii compleți, iar datele solare măsurate pot exclude o parte din producția panourilor de pe acoperișuri, consumată direct de proprietari.

Panoul din stînga arată cum s-a redus și și-a schimbat structura producția într-un deceniu; panoul din dreapta compară ianuarie–octombrie 2025 cu ianuarie–octombrie 2026, pe orele raportate în ambii ani, pentru ca o lună lipsă să nu pară o scădere a producției.

@chart mix_ro_annual
Producția anuală a României pe surse (TWh, cumulat) în anii compleți 2015–2025, cu consumul marcat printr-o bară neagră (stînga), și ponderile surselor în ianuarie–octombrie 2025 și 2026 (dreapta).

## România: cărbunele scade, solarul crește, iar nuclearul se reduce în 2026 {h=488e0773}

Comparația ponderilor fiecărei surse în 2015, 2025 și ianuarie–octombrie 2026 arată trei evoluții. Producția pe cărbune a scăzut cu 63,9% între 2015 și 2025, în timp ce producția solară măsurată a crescut de 2,2 ori în aceeași perioadă. În 2026, producția nucleară din ianuarie–octombrie a fost cu 31,3% mai mică decît în aceleași luni din 2025, pe orele raportate în ambii ani. Scăderea reală este cel puțin la fel de mare, deoarece cele 29 de zile din septembrie pentru care producția nucleară nu a fost raportată sînt pur și simplu excluse din comparație. Tabelul complet se află în Anexa D.

Aceste schimbări contează pentru prețuri, pentru că modifică centrala marginală. Mai puțin cărbune și mai puțin nuclear în bandă înseamnă că gazele, importurile sau hidrocentralele cu lac fixează mai des prețul; mai mult solar coboară prețurile de la amiază și mărește diferența față de seară.

@practice producătorii hidro și consumatorii industriali urmăresc ce centrală devine marginală cînd lipsește apa sau un reactor.

@chart mix_shares
Ponderea fiecărei surse în producția României (%) în 2015, 2025 și ianuarie–octombrie 2026, sub formă de bare orizontale.

## Structura cursului: șapte prelegeri și o hartă a modelelor {h=1bb3187f}

Acest curs deschide o serie de șapte: (1) piețele de energie și datele lor; (2) prognoza, cu modele clasice și cu modele autoregresive cu variabile exogene (ARX); (3) volatilitatea; (4) riscul în companiile de energie, inclusiv riscul preț–volum, fluxul de numerar la risc, dezechilibrele și riscul de bază; (5) derivatele și acoperirea riscului, inclusiv contractele de achiziție de energie pe termen lung (PPA); (6) regenerabilele, stocarea și flexibilitatea, cu canibalizarea, prețurile negative și bateriile; (7) învățarea automată și modelele fundaționale pentru prognoză.

Modelele din literatură se împart în trei familii (Weron, 2014): modelele fundamentale, construite pe curba ofertei și pe costul combustibilului și al CO$_2$; modelele de formă redusă (revenire la medie, salturi) și cele statistice; învățarea automată și modelele hibride. Aceleași date pot fi privite în două moduri (Ziel & Weron, 2018): univariat, ca o singură serie lungă de prețuri, sau multivariat, ca 24 (acum 96) de serii zilnice, cîte una pentru fiecare interval de livrare. Indiferent de familie, orice model trebuie să depășească prognoza naivă prezentată în secțiunea 3.

@practice întrebați furnizorul de prognoze din ce familie face parte modelul și cu cît depășește prognoza naivă.

## @end

O singură licitație zilnică, cuplată la nivel european, stabilește prețul din România ca fiind costul ofertei marginale, acum pentru 96 de sferturi de oră. Mixul de producție din spatele ei se schimbă rapid: mai puțin cărbune, mai mult solar și, în 2026, mult mai puțin nuclear.

# Date din energie și fapte stilizate

Înainte de orice model, datele trebuie măsurate în unitățile potrivite, pe fusul orar corect și fără valori inventate. Secțiunea fixează aceste convenții și documentează apoi, pe seriile din România și din Europa, faptele stilizate ale prețurilor energiei: salturile de nivel, sezonalitatea la trei frecvențe, salturile de preț, prețurile negative, cozile groase și gruparea volatilității.

## Putere și energie: MW nu înseamnă MWh {h=811b05c6}

Un megawatt (MW) măsoară puterea, adică ritmul producției sau al consumului; un megawatt-oră (MWh) măsoară cantitatea de energie, de exemplu 1 MW timp de o oră. Energia dintr-o perioadă și gradul de acoperire al datelor se calculează astfel:

$$ E=\frac{1}{10^6}\sum_{t\ \text{raportat}}P_t\,\Delta_t\ \ [\text{TWh}],\qquad \text{acoperire}=\frac{\text{ore raportate}}{\text{ore din perioadă}} $$ {#eq:energy}

unde $P_t$ este puterea medie în intervalul $t$, în MW, $\Delta_t$ este durata intervalului, în ore, astfel încît $P_t\Delta_t$ este exprimat în MWh, iar $E$ este energia, în terawați-oră (TWh), cu $1\ \text{TWh}=10^6\ \text{MWh}$. Suma se face numai pe intervalele raportate: orele lipsă nu se completează, iar fiecare total are alături gradul de acoperire.

Conform datelor noastre, România a consumat 53,56 TWh în 2025, adică o putere medie de 6,1 gigawați (GW). În tot cursul folosim două prețuri de referință: prețul în bandă (*base*), media prețurilor din întreaga zi de livrare, și prețul de vîrf (*peak*), media dintre orele 08:00 și 20:00, de luni pînă vineri. Gazele și țițeiul se cotează în dolari americani (USD) pe milion de unități termice britanice (MMBtu), respectiv pe baril (bbl); conversia lor în EUR/MWh se află în Anexa G.

@practice un contract de 10 MW în bandă înseamnă 240 MWh livrați pe zi.

## O zi de consum în România: puterea în MW, energia în MWh {h=454f640d}

Graficul face distincția concretă pentru o zi reală, 28 octombrie 2026. Curba reprezintă puterea: cît consumă țara în fiecare oră, în MW. Minimul a fost de 5 253 MW la ora 3:00, iar maximul de 7 719 MW la ora 17:00 (CET). Aria colorată de sub curbă este energia: 159 558 MWh în acea zi, adică 24 de ore înmulțite cu o putere medie de 6 648 MW.

Cele două mărimi răspund la întrebări de afaceri diferite. Un furnizor cumpără energie, în MWh, pentru fiecare interval și este plătit de clienți pentru energie. Rețeaua, în schimb, trebuie să poată transporta puterea de vîrf, în MW, chiar dacă acest nivel durează doar o oră; costurile de capacitate și de rețea sînt determinate de vîrf, nu de medie.

@practice un furnizor cumpără energie (MWh) pentru fiecare interval, iar rețeaua trebuie să acopere puterea de vîrf (MW).

@chart day_load
Consumul orar al României (MW) la 28 octombrie 2026, zi CET, cu aria de sub curbă, adică energia zilei în MWh, colorată.

## Pregătirea datelor (1): ziua de livrare, schimbarea orei și a zonei {h=1552d80b}

Marcajele temporale din datele brute ENTSO-E sînt în timpul universal coordonat (UTC). Statisticile zilnice trebuie însă să folosească ziua de livrare din SDAC, care este definită în ora Europei Centrale (CET) sau, vara, în ora de vară a Europei Centrale (CEST); o zi UTC ar muta una sau două ore în ziua greșită. Schimbarea orei creează în fiecare an două zile neregulate: ultima duminică din martie are 23 de ore, iar ultima duminică din octombrie are 25, iar mediile zilnice se calculează pe intervalele care există efectiv.

Și zonele de ofertare se schimbă. Germania, Austria și Luxemburg au format o singură zonă pînă la 30 septembrie 2018; seria noastră pentru Germania este îmbinată la acea dată. Fiecare grafic și fiecare cifră a cursului pot fi reproduse în notebook-ul Jupyter al cursului (notebooks/L1_notebook.ipynb), iar un singur grafic, marcat ca atare, folosește date simulate, pentru a ilustra zgomotul alb și mersul aleator (Lago, Marcjasz, De Schutter & Weron, 2021).

## Pregătirea datelor (2): zile lipsă și rupturi de serie {h=d59c11a5}

Sursa, energy-charts.info, care republică prețurile raportate de OPCOM și de IBEX la ENTSO-E, nu are preț pentru unele zile și nu indică motivul. Pentru România lipsesc 5 zile: 21 septembrie 2015, 20 și 21 decembrie 2015, 31 decembrie 2017 și 17 august 2018. Seria pentru Bulgaria începe abia la 31 octombrie 2016, deși bursa IBEX organizează piața pentru ziua următoare din 19 ianuarie 2016, și mai lipsesc 15 zile pînă la 31 decembrie 2016. Aceste zile nu se completează, iar variația zilnică nu se calculează peste un gol.

Și seriile futures au rupturi. Seria Brent pentru contractul cel mai apropiat prezintă un salt la trecerea de la un contract la următorul; aceste salturi nu sînt mișcări ale pieței, iar zilele respective sînt excluse din statisticile randamentelor.

@practice la un furnizor, cele mai multe erori de prognoză apar la prelucrarea datelor (fus orar greșit, goluri completate), nu în model.

## Prețurile au explodat în 2021–2022 și nu au mai revenit la vechiul nivel {h=d5e0efbd}

Graficul prezintă prețurile zilnice pentru ziua următoare în cele patru zone, din 2015 pînă în octombrie 2026. Pînă în 2020, prețurile au rămas într-un interval îngust; în 2021–2022, criza gazelor din Europa le-a dus la niveluri fără precedent, iar maximul zilnic din România a ajuns la 738,28 EUR/MWh, la 30 august 2022. Prețurile au scăzut apoi, dar nu pînă la vechiul nivel.

România, Bulgaria și Ungaria evoluează împreună, deoarece piețele lor sînt cuplate, în timp ce Germania este mai ieftină din 2023. Saltul de nivel din 2021–2022 este primul fapt stilizat: orice model estimat pe date de dinainte de 2021, ca și orice buget construit pe ele, descrie o piață care nu mai există.

@practice un consumator industrial care își face bugetul cu prețurile de dinainte de 2021 le subestimează de două-trei ori.

@chart prices_daily_4zones
Prețurile zilnice în bandă (EUR/MWh) în România, Bulgaria, Ungaria și Germania–Luxemburg, 1 ianuarie 2015 – 31 octombrie 2026 (Bulgaria din 31 octombrie 2016).

## Volatilitatea crește odată cu nivelul prețului {h=105c18e3}

Tabelul prezintă, pentru fiecare zonă și an, prețul mediu și volatilitatea, măsurată ca abatere standard a variațiilor zilnice ale prețului, ambele în EUR/MWh.

| EUR/MWh | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 YTD |
|---|---|---|---|---|---|---|---|---|---|
| Media RO | 46,4 | 50,4 | 39,5 | 111,4 | 265,3 | 103,7 | 103,5 | 108,2 | 137,4 |
| Media DE-LU | 44,5 | 37,7 | 30,5 | 96,8 | 235,5 | 95,2 | 78,5 | 89,3 | 114,0 |
| Volatilitate RO | 10,9 | 11,5 | 8,6 | 25,2 | 58,9 | 26,3 | 32,4 | 24,4 | 31,6 |
| Volatilitate DE-LU | 11,5 | 11,9 | 11,5 | 34,4 | 65,3 | 30,3 | 31,4 | 28,3 | 36,0 |

Cele două mărimi evoluează împreună: în 2022, cînd media din România a fost de 265,3 EUR/MWh, abaterea standard a variațiilor zilnice a fost de 58,9, față de 8,6 în 2020, cînd media era de 39,5. Bulgaria și Ungaria urmează același tipar. O volatilitate măsurată în EUR/MWh nu este, așadar, comparabilă între ani cu niveluri de preț foarte diferite. În 2026 (YTD), media din România a fost de 137,45 EUR/MWh, față de 105,88 EUR/MWh în ianuarie–octombrie 2025, o creștere de 29,8%.

@practice garanțiile pentru PZU cresc odată cu prețul: la 200 EUR/MWh piața fluctuează mult mai mult decît la 50.

## Producția solară a mutat minimul zilnic al prețului la amiază {h=a0e03712}

Graficul compară prețul mediu al fiecărei ore din zi în 2019 și în 2025, pentru fiecare zonă. În 2019, orele cele mai ieftine erau noaptea, ca într-un sistem energetic clasic, cînd cererea este minimă. În 2025, ora cu prețul minim se mutase la 13:00, cu 58,8 EUR/MWh în România, în timp ce vîrful de seară ajungea la 182,5 EUR/MWh. Raportul dintre prețul de seară și cel de la amiază a urcat de la 1,30 la 3,11.

Aceasta este „curba în formă de rață” (*duck curve*): producția solară acoperă mijlocul zilei, reduce cererea rămasă pentru celelalte centrale și coboară prețul, în timp ce seara, cînd apune soarele și crește consumul casnic, rămîne scumpă. Profilul intrazilnic nu mai este o trăsătură fixă a pieței; el se modifică pe măsură ce crește capacitatea solară.

@practice venitul unei baterii provine din această diferență dintre amiază și seară, valorificată o dată sau de două ori pe zi.

@chart profile_intraday
Prețul mediu pentru ziua următoare (EUR/MWh) pe ore ale zilei (CET), în anii 2019 și 2025, cîte un panou pentru fiecare zonă.

## La sfîrșit de săptămînă, energia este mai ieftină {h=e1e20267}

În weekend, fabricile și birourile consumă mai puțin, sînt necesare mai puține centrale și prețul scade. Profilul săptămînal se măsoară astfel:

$$ \hat s_j=\frac1W\sum_{w=1}^{W}\Big(p_{w,j}-\frac17\sum_{i=1}^{7}p_{w,i}\Big) $$ {#eq:weekday}

unde $j$ este ziua săptămînii, $W$ este numărul de săptămîni complete, $p_{w,j}$ este prețul zilnic din ziua $j$ a săptămînii $w$, suma interioară împărțită la 7 este prețul mediu al săptămînii $w$, iar $\hat s_j$ este abaterea medie a zilei $j$ față de media săptămînii din care face parte, în EUR/MWh. Scăderea mediei fiecărei săptămîni elimină salturile de nivel, precum cel din 2022, care altfel ar domina mediile.

Pe 199 de săptămîni, între 2 ianuarie 2023 și 25 octombrie 2026:

| | Lu | Ma | Mi | Jo | Vi | Sî | Du |
|---|---|---|---|---|---|---|---|
| RO | 9,1 | 12,7 | 12,6 | 10,4 | 3,4 | −17,5 | −30,7 |
| DE-LU | 7,0 | 11,0 | 11,6 | 7,9 | 3,3 | −15,8 | −25,1 |

În România, o duminică este în medie cu 30,7 EUR/MWh mai ieftină decît media săptămînii sale, iar o sîmbătă cu 17,5; zilele lucrătoare se situează peste medie, cu valorile cele mai mari marțea și miercurea.

@practice un consumator industrial își poate muta consumul flexibil (mentenanță, pompare, încărcare) duminica, reducîndu-și astfel costurile cu energia.

## Primăvara, energia este ieftină: multă apă, mult soare, cerere moderată {h=30e28a5a}

De-a lungul anului, prețul din România urmează echilibrul dintre cerere și sursele ieftine. Raportat la media anuală, prețul este maxim în ianuarie (de 1,26 ori media) și minim în aprilie (de 0,72 ori). Consumul este maxim în ianuarie–februarie și minim în mai, iar producția hidro atinge maximul în iunie, odată cu topirea zăpezii. Primăvara, apa abundentă și producția solară în creștere întîlnesc o cerere moderată, iar prețurile scad.

Profilul anual este a treia frecvență sezonieră a seriei, după cea zilnică și cea săptămînală; modelele care îl ignoră atribuie „șocurilor” ceea ce este de fapt un tipar regulat.

@practice un producător hidro economisește apa din lacuri primăvara, cînd energia este ieftină, pentru a o turbina iarna și la sfîrșitul verii.

@chart profile_annual
Medii lunare 2016–2025: consumul, producția hidro și cea solară a României pe luni (GW, stînga) și prețul PZU din fiecare lună raportat la media anuală, mediana pe ani (dreapta).

## Salturile de preț: puține ore, prețuri extreme {h=28b10f20}

Un salt de preț (*spike*) apare într-un interval în care prețul depășește cu mult nivelul obișnuit al anului respectiv. O regulă robustă marchează intervalul $t$ din anul $y$ ca salt de preț atunci cînd

$$ p_t>Q_{3,y}+3\,(Q_{3,y}-Q_{1,y}) $$ {#eq:spike}

unde $Q_{1,y}$ și $Q_{3,y}$ sînt percentilele 25 și 75 ale tuturor prețurilor din anul $y$, ponderate cu durata intervalului (un interval de 15 minute are un sfert din ponderea unui interval orar), iar $Q_{3,y}-Q_{1,y}$ este abaterea intercuartilică (IQR). Percentilele sînt robuste, deci salturile înseși abia mișcă pragul (Janczura, Trück, Weron & Wolff, 2013).

| Anul | Prag RO | Ore RO | Ore DE-LU |
|---|---|---|---|
| 2020 | 109 | 54,00 | 30,00 |
| 2021 | 394 | 69,00 | 280,00 |
| 2022 | 873 | 4,00 | 4,00 |
| 2023 | 292 | 38,00 | 13,00 |
| 2024 | 274 | 276,00 | 72,00 |
| 2025 | 285 | 120,00 | 88,75 |
| 2026 | 427 | 39,25 | 32,25 |

Deoarece pragul urmează distribuția fiecărui an, 2022 are foarte puține salturi de preț în ciuda prețurilor record: întregul an a fost scump. În România, anul 2024 iese în evidență, cu 276 de ore cu salturi de preț, față de 72 în Germania. Cel mai mare preț din România în datele noastre este de 1021,61 EUR/MWh, la 3 septembrie 2024, ora 19:00 CEST.

@practice un furnizor cu contracte la preț fix își poate pierde cea mai mare parte a marjei anuale în cîteva zeci de ore cu salturi de preț, motiv pentru care își acoperă riscul.

## Prețurile negative au apărut în România în 2023 și au devenit frecvente {h=3d3da655}

Primul preț negativ pe PZU a apărut la 21 mai 2023. De atunci, prețurile negative au devenit o trăsătură obișnuită a pieței și urmează un tipar clar: din 2024, 91,1% din orele cu preț negativ cad între 10:00 și 16:00, iar 83,9% în weekend. Sînt orele în care producția solară este maximă, iar cererea minimă.

Barele din grafic sînt exprimate în ore echivalente, astfel încît un sfert de oră cu preț negativ contează 0,25 ore, iar anii cu prețuri orare pot fi comparați cu cei cu prețuri pe sfert de oră.

@practice un parc solar fără stocare își vinde o mare parte din producție în cele mai ieftine ore ale anului (cursul 6).

@chart negative_prices
Numărul anual de ore cu preț negativ pentru ziua următoare (ore echivalente) în cele patru zone, din 2018 pînă în octombrie 2026 (stînga), și orele cu preț negativ din România pe ore ale zilei, din 2024 (dreapta).

## Prețurile negative, numărate corect: ore echivalente {h=3e6510f9}

Tabelul numără orele cu preț negativ pentru ziua următoare în fiecare zonă, în ore echivalente; ultima coloană dă numărul sferturilor de oră cu preț negativ din 2026, de 4 ori mai mare decît numărul orelor echivalente.

| Zona | 2022 | 2023 | 2024 | 2025 | 2026 YTD | ian.–oct. 2025 | 2026: intervale de 15 min |
|---|---|---|---|---|---|---|---|
| RO | 0 | 32 | 85 | 196 | 171,75 | 196 | 687 |
| BG | 0 | 11 | 55 | 170 | 152,25 | 170 | 609 |
| HU | 0 | 74 | 262 | 281 | 223,50 | 281 | 894 |
| DE-LU | 69 | 301 | 457 | 574,75 | 465 | 574,75 | 1 860 |

România nu a avut prețuri negative înainte de 2023, în timp ce Germania le-a avut în fiecare an, din cauza centralelor inflexibile combinate cu producția eoliană. România, Bulgaria și Ungaria evoluează împreună, dar din 2023 Ungaria are mai multe ore cu preț negativ. În ianuarie–octombrie 2026, România a avut 171,75 ore cu preț negativ, față de 196,00 ore în aceleași luni din 2025: creșterea numărului de prețuri negative nu este automată, iar studiul de caz (d) analizează factorii care o determină.

@practice în rapoartele către conducere scrieți „687 de sferturi de oră (171,75 h)”, nu un număr fără unitate.

## Prețul poate fi nul sau negativ: folosiți diferențe sau asinh {h=7618fe91}

Variațiile procentuale și logaritmii presupun un preț pozitiv, deci eșuează tocmai în orele cele mai importante pentru producția solară și pentru stocare. O transformare definită pentru orice semn păstrează orele cu preț nul sau negativ (Uniejewski, Weron & Ziel, 2018):

$$ y_t=\asinh(x_t)=\ln\big(x_t+\sqrt{x_t^2+1}\big),\qquad x_t=\frac{p_t-\tilde p}{\widehat{\mathrm{MAD}}} $$ {#eq:asinh}

unde $p_t$ este prețul, $\tilde p$ este mediana sa, $\widehat{\mathrm{MAD}}$ este abaterea absolută mediană (MAD) înmulțită cu 1,4826, astfel încît să estimeze abaterea standard în cazul distribuției normale, $x_t$ este prețul standardizat, iar $y_t$ este prețul transformat. Pentru valori mari ale lui $|x|$, $\asinh(x)\approx\operatorname{sign}(x)\ln(2|x|)$: transformarea se comportă ca un logaritm în ambele cozi și este aproape liniară în jurul lui zero.

În ianuarie–octombrie 2026, 1 189 din cele 29 184 de sferturi de oră din România au avut un preț nul sau negativ, dintre care 502 un preț exact 0. După transformare, asimetria scade de la 1,19 la 0,13, iar excesul de aplatizare (*kurtosis*) de la 6,73 la −0,55: distribuția devine aproape simetrică, cu cozi subțiri. Pentru raportare însă, variațiile PZU se exprimă cel mai simplu ca diferențe în EUR/MWh.

@chart asinh_ro
Histograma tuturor prețurilor pe sfert de oră din România, ianuarie–octombrie 2026, în nivel (EUR/MWh, stînga) și după transformarea asinh (dreapta).

## Cozi groase: variațiile extreme ale țițeiului sînt mult mai frecvente {h=ded78b77}

„Cozile groase” înseamnă că zilele cu creșteri sau scăderi foarte mari apar mult mai des decît ar permite clopotul lui Gauss. Dovada provine din randamentele logaritmice zilnice ale țițeiului Brent, între 5 ianuarie 2015 și 30 octombrie 2026, fără cele 141 de zile de schimbare a contractului. Conform distribuției normale, variațiile de peste 4 abateri standard ar trebui să apară de 0,18 ori într-un asemenea eșantion; observăm 16. Excesul de aplatizare este 13,98, față de 0 pentru distribuția normală; formulele și testul de normalitate Jarque–Bera (JB) se află în Anexa F (Jarque & Bera, 1980).

Graficul cuantil–cuantil arată același lucru vizual: cuantilele observate se îndepărtează de dreapta distribuției normale în ambele cozi, iar o densitate Student-$t$ se potrivește histogramei mult mai bine decît cea normală.

@practice o limită de buget pentru combustibil calculată pe baza legii normale subestimează frecvența zilelor de criză (cursul 4).

@chart tails_brent
Randamentele logaritmice zilnice ale țițeiului Brent, 5 ianuarie 2015 – 30 octombrie 2026: graficul cuantil–cuantil față de distribuția normală (stînga) și histograma randamentelor standardizate, cu densitățile normală și Student-t (dreapta).

## Perioadele calme și cele agitate apar grupat {h=09fe719b}

O variație mare astăzi face mai probabilă o altă variație mare mîine, chiar dacă sensul ei nu poate fi anticipat. Statistica Ljung–Box testează dacă primele $m$ autocorelații ale unei serii sînt simultan nule:

$$ Q(m)=T(T+2)\sum_{k=1}^{m}\frac{\hat\rho_k^2}{T-k}\ \sim\ \chi^2_m $$ {#eq:ljungbox}

unde $T$ este numărul de observații, $\hat\rho_k$ este autocorelația de selecție la decalajul $k$, iar $\chi^2_m$ este distribuția hi-pătrat cu $m$ grade de libertate, pe care o urmează statistica atunci cînd nu există autocorelație (Ljung & Box, 1978).

Pentru Brent, cu $m=10$, statistica este 28,1 pentru randamentele $r$, dar 506,9 pentru pătratele lor $r^2$, față de o valoare critică de 18,31 la pragul de 5%. Ambele resping ipoteza nulă, dar diferența de mărime este mesajul: dependența temporală este slabă pentru sensul variațiilor și puternică pentru mărimea lor. Această grupare a volatilității este descrisă de modelele din cursul 3.

@practice după un șoc, departamentul de risc menține limite mai largi săptămîni întregi, nu doar cîteva zile (cursul 3).

@chart volclust_brent
Randamentele logaritmice zilnice ale țițeiului Brent, în % (sus), și volatilitatea lor pe 21 de zile, în % pe an (jos), 5 ianuarie 2015 – 30 octombrie 2026.

## @end

Prețurile energiei își schimbă nivelul, urmează cicluri zilnice, săptămînale și anuale, au salturi, devin negative, au cozi groase și volatilitate grupată. Unitățile de măsură, fusurile orare și golurile din date trebuie tratate înainte ca aceste fapte să poată fi măsurate.

# Instrumente de analiză a seriilor de timp

Secțiunea introduce instrumentele folosite în tot cursul pentru a descrie o serie de prețuri: staționaritatea, autocorelația și autocorelația parțială, prognoza naivă, testele de rădăcină unitară, descompunerea și netezirea exponențială. Fiecare instrument este aplicat pe datele din România, din Germania sau pe țițeiul Brent.

## Staționaritate: regulile jocului nu se schimbă în timp {h=799527c5}

O serie este (slab) staționară dacă media, dispersia și memoria ei rămîn aceleași în orice perioadă:

$$ \E X_t=\mu,\quad \Var X_t=\gamma_0,\quad \Cov(X_t,X_{t-k})=\gamma_k\quad \text{pentru orice } t $$ {#eq:stationary}

unde $X_t$ este valoarea seriei la momentul $t$, $\mu$ este media sa constantă, $\gamma_0$ este dispersia constantă, iar $\gamma_k$ este autocovarianța la decalajul $k$, care depinde numai de decalajul $k$, nu și de momentul $t$.

Graficul prezintă trei serii simulate, singurul grafic cu date simulate din curs: un zgomot alb; un model autoregresiv (AR) de ordinul 1, AR(1), cu $\phi=0{,}9$, care revine mereu la medie; și un mers aleator, ale cărui șocuri sînt permanente. O greșeală frecventă este să credem că mersul aleator are autocorelație mică pentru că pare haotic. Este exact invers: autocorelația nivelului său este apropiată de 1, aici 0,96 la decalajul 10, deoarece fiecare valoare conține toate șocurile trecute.

@practice un preț mediu istoric poate servi drept prognoză numai dacă seria este staționară; testați acest lucru înainte de a construi bugetul.

@chart sim_wn_ar_rw
Serii simulate (T = 500, șocuri normale standard): zgomot alb, AR(1) cu phi = 0,9 și mers aleator, cu funcțiile lor de autocorelație de selecție dedesubt.

## Autocorelația: cît din trecut se regăsește în prețul de azi {h=20415e29}

Autocorelația de ordinul $k$ este corelația dintre serie și aceeași serie decalată cu $k$ perioade:

$$ \hat\rho_k=\frac{\sum_{t=k+1}^{T}(x_t-\bar x)(x_{t-k}-\bar x)}{\sum_{t=1}^{T}(x_t-\bar x)^2} $$ {#eq:acf}

unde $x_t$ este observația de la momentul $t$, $\bar x$ este media de selecție, iar $T$ este volumul eșantionului. Pentru un zgomot alb, autocorelațiile de selecție se află în banda $\pm1{,}96/\sqrt T$ cu probabilitatea de 95%. Banda Bartlett la decalajul $k$, $\pm1{,}96\sqrt{(1+2\sum_{j<k}\hat\rho_j^2)/T}$, este mai largă și este valabilă dacă autocorelația teoretică este nulă după decalajul $k-1$. Funcția de autocorelație parțială (PACF) măsoară memoria la decalajul $k$, după eliminarea efectului decalajelor mai mici.

Patru reguli de interpretare acoperă majoritatea situațiilor. O scădere lentă de la valori apropiate de 1 indică persistență sau o rădăcină unitară, care trebuie testată. O scădere geometrică, cu o PACF care se anulează după $p$ decalaje, indică un model AR($p$). Vîrfurile la decalajele 7 și 14, pentru date zilnice, sau 24 și 168, pentru date orare, arată sezonalitate. Dacă toate valorile se află în bandă, nu există memorie liniară, dar trebuie verificate și pătratele $x_t^2$, deoarece volatilitatea poate fi totuși grupată (Hyndman & Athanasopoulos, 2021).

@practice prognoza unui furnizor pentru ziua de mîine pornește de la „aceeași zi din săptămîna trecută”: autocorelația la decalajul 7 este 0,672 în România, din 2023.

## Prețul ține minte ziua de ieri, săptămîna trecută și aceeași oră {h=3538be57}

Cele două grafice aplică regulile de interpretare prețurilor din România. Pentru prețurile zilnice în bandă dintre 1 ianuarie 2023 și 31 octombrie 2026, autocorelația la decalajul 1 este $\hat\rho_1=0{,}789$, iar la decalajul 7, $\hat\rho_7=0{,}672$; autocorelația parțială la decalajul 7 este $\hat\alpha_7=0{,}257$, deci aceeași zi din săptămîna precedentă aduce informație în plus față de ultimele zile. Funcția de autocorelație scade lent, cu vîrfuri la multiplii lui 7.

Pentru prețurile orare din 2024, autocorelația la decalajul 24 (aceeași oră de ieri) este $\hat\rho_{24}=0{,}776$, iar la decalajul 168 (aceeași oră de săptămîna trecută), $\hat\rho_{168}=0{,}681$. Prețul ține minte, așadar, ziua de ieri, săptămîna trecută și aceeași oră a zilei: aceste decalaje sînt variabilele explicative firești ale modelelor de prognoză din cursul 2 (Ziel & Weron, 2018).

@chart acf_pacf_ro_daily
Autocorelația (stînga) și autocorelația parțială (dreapta) a prețurilor zilnice în bandă din România, 1 ianuarie 2023 – 31 octombrie 2026 (T = 1400), cu banda Bartlett.

@chart acf_ro_hourly
Autocorelația prețurilor orare din România în 2024 (T = 8784), pînă la decalajul de 168 de ore, cu banda pentru zgomot alb.

## Prognoza naivă: reperul pe care orice model trebuie să-l depășească {h=222ca816}

Cea mai simplă prognoză rezonabilă spune că prețul de mîine pentru fiecare oră este prețul de azi pentru aceeași oră; luni, sîmbătă și duminică se folosește prețul aceleiași ore din ziua corespunzătoare a săptămînii precedente:

$$ \hat p_{d,h}=\begin{cases} p_{d-1,h} & d=\text{Ma–Vi}\\ p_{d-7,h} & d=\text{Lu, Sî, Du}\end{cases},\qquad \mathrm{MAE}=\frac{1}{n}\sum_{d,h}|p_{d,h}-\hat p_{d,h}| $$ {#eq:naive}

unde $p_{d,h}$ este prețul orei $h$ din ziua $d$, $\hat p_{d,h}$ este prognoza sa, $n$ este numărul de prognoze, iar eroarea absolută medie (MAE) este media erorilor absolute de prognoză, în EUR/MWh (Nogales et al., 2002).

Pentru România, în 2025, prognoza naivă a avut o MAE de 22,9 EUR/MWh, la un preț mediu de 108,2. Regula zi lucrătoare/weekend are erori mai mici decît ambele decalaje simple, ziua precedentă și aceeași zi din săptămîna trecută, în 7 din 8 ani; toți anii și Germania se află în Anexa E. Un model care nu depășește acest reper nu aduce nimic nou, oricît de sofisticat ar fi (Weron, 2014; Lago et al., 2021).

@practice înainte de a plăti un serviciu de prognoză, cereți eroarea lui absolută medie comparativ cu acest reper.

@chart naive_bar
MAE (EUR/MWh) a prognozei naive și a celor două decalaje simple (ziua d−1 și ziua d−7) pentru prețurile orare din România în 2024, 2025 și 2026 (YTD).

## Persistența șocurilor: două teste cu ipoteze opuse {h=b6d4046a}

Un test pornește de la ipoteza „șocurile sînt permanente” și caută o revenire la medie; celălalt pornește de la „seria este stabilă” și caută o derivă lentă. Testul Dickey–Fuller augmentat (ADF) estimează

$$ \Delta x_t=\alpha+\gamma\,x_{t-1}+\sum_{j}\delta_j\Delta x_{t-j}+u_t $$ {#eq:adf}

unde $\Delta x_t=x_t-x_{t-1}$ este variația seriei, $\alpha$ este o constantă, $\gamma$ măsoară atracția spre medie, $\delta_j$ sînt coeficienții variațiilor decalate suplimentare, care preiau dinamica pe termen scurt, iar $u_t$ este eroarea. Ipoteza nulă este $H_0:\gamma=0$, adică rădăcină unitară; statistica $\hat\gamma/\mathrm{se}$ se compară cu valorile critice Dickey–Fuller, de circa $-2{,}86$ la 5%, iar numărul de decalaje $p$ se alege după criteriul informațional Akaike (AIC) (Dickey & Fuller, 1979). Testul Kwiatkowski–Phillips–Schmidt–Shin (KPSS) are ipoteza nulă opusă, staționaritatea, și o respinge la valori mari, peste 0,463 la 5% (Kwiatkowski et al., 1992). Formulele complete se află în Anexa A.

| $H_0$: | KPSS nerespinsă | KPSS respinsă |
|---|---|---|
| ADF respinsă | staționară | conflict |
| ADF nerespinsă | neconcludent | rădăcină unitară* |

*Compatibil cu o rădăcină unitară, dar nu este o dovadă: testul ADF are putere redusă în cazul revenirii lente la medie, iar rupturile de nivel, precum cea din 2022, favorizează nerespingerea rădăcinii unitare.

@practice dacă șocurile pot fi permanente, un furnizor nu își poate baza bugetul pe „revenirea la normal”.

## Un verdict pe serie: nivelurile persistă, variațiile sînt staționare {h=1eff8512}

Aplicînd ambele teste, numai cu constantă, cu decalajele ADF alese după AIC și la pragul de 5%, obținem un verdict pentru fiecare serie:

| Seria | Perioada | T | ADF | p | KPSS | p | Verdict |
|---|---|---|---|---|---|---|---|
| Preț RO, nivel | 2015–2026 | 4 317 | −2,71 | 0,073 | 3,645 | <0,01 | rădăcină unitară* |
| Preț RO, variație zilnică | 2015–2026 | 4 312 | −14,81 | <0,001 | 0,045 | >0,10 | staționară |
| Preț DE-LU, nivel | 2015–2026 | 4 322 | −3,54 | 0,007 | 3,441 | <0,01 | conflict |
| Brent, logaritmul prețului | 2015–2026 | 2 976 | −2,19 | 0,212 | 3,820 | <0,01 | rădăcină unitară* |
| Brent, randament logaritmic | 2015–2026 | 2 975 | −10,79 | <0,001 | 0,049 | >0,10 | staționară |
| Hidro RO, desezonalizat | 2015–2025 | 132 | −4,19 | <0,001 | 0,354 | 0,097 | staționară |

Nivelurile prețului din România și ale țițeiului Brent sînt compatibile cu o rădăcină unitară (ipoteză nerespinsă, ceea ce nu este o dovadă), în timp ce variațiile lor sînt staționare. Pentru Germania, ambele teste își resping ipoteza nulă, un conflict care reflectă revenirea la medie combinată cu saltul de nivel din 2021–2022. Producția hidro este testată după scăderea mediilor lunare, fiind o serie sezonieră, și este staționară. Dacă prețul din România este analizat numai din 2023, verdictul nu se schimbă: ADF $p=0{,}361$, KPSS 1,039.

@practice modelați *variațiile* prețului (sau prețul transformat) și includeți explicit sezonalitatea.

## Descompunerea: trend, sezonalitate și componenta reziduală {h=8e6a472b}

O serie sezonieră poate fi scrisă ca suma a trei componente:

$$ x_t=T_t+S_t+R_t $$ {#eq:decomp}

unde $T_t$ este trendul, $S_t$ este componenta sezonieră, iar $R_t$ este componenta reziduală. Metoda clasică estimează trendul printr-o medie mobilă (MA) centrată și presupune o componentă sezonieră constantă; descompunerea sezonieră și de trend prin regresie locală (STL) îi permite să varieze în timp (Cleveland et al., 1990).

Graficul aplică ambele metode consumului mediu lunar al României, între ianuarie 2016 și decembrie 2025. Față de trend, consumul este mai mare cu 0,69 GW în ianuarie și februarie și mai mic cu 0,65 GW în mai. STL arată că amplitudinea sezonieră s-a redus de la 1,52 la 1,27 GW în acest deceniu. Ponderile mediei mobile și un exemplu de calcul se află în Anexa B, iar algoritmul STL în Anexa C.

@practice Transelectrica și furnizorii planifică lunar capacitățile cu ajutorul indicilor sezonieri; STL arată cînd se schimbă chiar profilul sezonier.

@chart decomp_load
Consumul mediu lunar al României, ianuarie 2016 – decembrie 2025 (GW): seria observată, cu trendul clasic și trendul STL (sus), și componentele sezoniere clasică și STL (jos).

## Netezirea exponențială: datele recente cîntăresc mai mult {h=88f1ebe7}

Nivelul netezit este o medie a tuturor valorilor trecute, cu ponderi care scad geometric:

$$ \ell_t=\alpha x_t+(1-\alpha)\ell_{t-1},\qquad \alpha=1-2^{-1/h} $$ {#eq:ewma}

unde $\ell_t$ este nivelul netezit la momentul $t$, $x_t$ este observația nouă (informația nouă), $(1-\alpha)\ell_{t-1}$ este memoria trecutului, $\alpha$ este ponderea de netezire, iar $h$ este timpul de înjumătățire, în zile, adică numărul de zile după care ponderea unei observații se reduce la jumătate.

Pe prețul Brent din ianuarie 2024 pînă în octombrie 2026, o medie mobilă ponderată exponențial (EWMA) cu timp de înjumătățire de 10 zile folosește $\alpha=0{,}067$. Dacă $\alpha$ este ales astfel încît să minimizeze erorile de prognoză pentru ziua următoare, netezirea exponențială simplă (SES) alege 0,948: aproape toată ponderea revine ultimului preț, exact cum ne așteptăm pentru o serie apropiată de un mers aleator (Hyndman & Athanasopoulos, 2021).

@practice EWMA este un bun preț de referință în contracte, dar o prognoză slabă.

@chart smooth_brent
Prețul de închidere al țițeiului Brent (USD/bbl), 2 ianuarie 2024 – 30 octombrie 2026, cu media mobilă simplă pe 20 de zile de tranzacționare și o EWMA cu timp de înjumătățire de 10 zile.

## @end

Nivelurile prețurilor se comportă ca serii cu rădăcină unitară, iar variațiile lor sînt staționare; prețul ține minte ziua de ieri, săptămîna trecută și aceeași oră. Prognoza naivă construită pe aceste decalaje este reperul pe care orice model trebuie să-l depășească.

# Studii de caz pe date recente

Șase episoade din perioada 2023–2026 arată faptele stilizate în acțiune: un an ploios și unul secetos, un șoc petrolier, o separare regională a prețurilor, prețurile negative și producția solară, creșterea prețurilor din 2026 și apariția bateriilor în Bulgaria. Fiecare studiu de caz este analizat cu instrumentele din secțiunile anterioare și numai pe date reale.

## Studiul de caz (a): producția hidro în 2025, cu o treime sub 2023 {h=6a8ef687}

Producția hidro a României depinde de ploi și de zăpadă. În 2023, un an ploios, centralele pe firul apei și cele cu lac au produs 18,34 TWh, maximul din 2015 încoace; în 2025, un an secetos, au produs 12,15 TWh, minimul perioadei, adică o scădere de 33,8%. Față de media 2015–2025, de 15,85 TWh, producția din 2025 a fost cu 23,3% sub normal.

În același interval, România a trecut de la export net, cu un import net de −3,06 TWh, la import net, de +3,76 TWh. Evoluția este compatibilă cu lipsa apei, dar nu o dovedește: între cei doi ani s-au modificat și producția nucleară, cererea și prețurile din țările vecine, iar graficul singur nu poate separa aceste efecte.

@practice producția unei companii hidro și factura unui importator net depind de precipitații la fel de mult ca de piață.

@chart hydro_case
Producția hidro lunară a României (TWh) în 2023 și 2025, cu media lunară 2015–2025 (stînga), și prețul mediu lunar în funcție de producția hidro lunară (dreapta).

## Studiul de caz (a): mai multă apă, prețuri mai mici {h=ee5a5635}

Pentru a lega apa de preț la același preț al gazelor, estimăm pe date lunare din 2015–2025 modelul

$$ p_m=\beta_0+\beta_1\,\mathrm{Hydro}_m+\beta_2\,\mathrm{TTF}_m+u_m $$ {#eq:hydroreg}

unde $p_m$ este prețul mediu PZU în luna $m$ (EUR/MWh), $\mathrm{Hydro}_m$ este producția hidro (TWh), $\mathrm{TTF}_m$ este prețul gazelor pe hubul olandez (EUR/MWh), $\beta_0,\beta_1,\beta_2$ sînt coeficienții, iar $u_m$ este eroarea. Modelul este estimat prin metoda celor mai mici pătrate (OLS), cu erori standard robuste la heteroscedasticitate și autocorelație (HAC), cu 6 decalaje.

| 2015–2025 | estimație | e.s. | t |
|---|---|---|---|
| Constantă | 44,80 | 10,21 | 4,39 |
| Hidro | −19,55 | 7,02 | −2,78 |
| TTF | 1,89 | 0,06 | 34,16 |

Un TWh hidro în plus într-o lună este asociat, în medie, cu un preț mai mic cu 19,55 EUR/MWh, la același preț al gazelor. Este o asociere, nu un efect cauzal măsurat. Prețurile energiei și ale gazelor au trend (secțiunea 3), deci fără cointegrare regresia poate fi spurioasă: un $R^2$ de 0,941 nu este o dovadă, iar cointegrarea se testează în cursul 2.

@practice producătorii hidro și traderii urmăresc nivelul lacurilor ca indicator anticipativ al prețului PZU.

## Studiul de caz (b): Brent, +7% într-o zi, apoi sub nivelul inițial {h=fdf19f2e}

În iunie 2025, prețul țițeiului Brent a reacționat puternic la războiul dintre Israel și Iran. La 12 iunie 2025, Brent s-a închis la 69,36 USD/bbl; la 13 iunie, ziua în care Israelul a atacat Iranul, s-a închis la 74,23, o creștere de 7,0% într-o singură zi, adică 4,3 abateri standard ale randamentelor zilnice din 2024. Maximul a fost atins la 20 iunie 2025, la 77,01. La 24 iunie, cu armistițiul în vigoare, prețul de închidere a fost de 67,14, cu 12,8% sub maxim și cu 3,2% sub nivelul din 12 iunie.

Episodul arată cum un șoc geopolitic este întîi inclus în preț ca primă de risc și apoi eliminat la fel de repede cînd întreruperea temută a aprovizionării nu se produce. El ilustrează și cozile groase din secțiunea anterioară: o zi de 4,3 abateri standard este rară într-o distribuție normală, dar nu și pe piața țițeiului.

@practice un cumpărător de combustibil și-a acoperit riscul la maximul din 20 iunie; patru zile mai tîrziu, piața era mult sub prețul fixat.

@chart iran_brent
Prețul de închidere zilnic al țițeiului Brent (USD/bbl) în zilele de tranzacționare dintre 2 iunie și 4 iulie 2025.

## Studiul de caz (c): în iulie 2024, România a plătit dublul prețului din Germania {h=a1f71249}

În vara lui 2024, piețele cuplate din sud-estul Europei s-au separat de Europa Centrală. În iulie 2024, prețul mediu pentru ziua următoare a fost de 145,14 EUR/MWh în România, 136,47 în Bulgaria și 135,54 în Ungaria, dar numai 67,70 în Germania–Luxemburg.

Panoul din dreapta detaliază ziua de 16 iulie 2024, cînd diferența zilnică dintre România și Germania a ajuns la 162,87 EUR/MWh. Vîrful orar din România a fost de 801,62 EUR/MWh la ora 20:00, în timp ce prețul din Germania era de −11,48 EUR/MWh la ora 14:00: în aceeași zi, Germania avea prea multă energie solară la amiază, iar sud-estul Europei prea puțină energie seara.

@practice pentru cumpărătorii din sud-estul Europei, serile verilor caniculare și secetoase reprezintă principalul risc de preț.

@chart separation_2024
Prețurile zilnice în bandă în cele patru zone, 1 iunie – 30 septembrie 2024 (stînga), și prețurile orare din 16 iulie 2024 (dreapta).

## Studiul de caz (c): seri caniculare și o rețea congestionată {h=c3f3d99e}

Ponderea orelor din iulie 2024 în care prețurile au fost egale, cu o diferență sub 0,01 EUR/MWh, arată unde rețeaua era la limită: 86,8% pentru România–Bulgaria, dar numai 6,3% pentru România–Ungaria și 3,1% pentru România–Germania. Rețeaua spre Europa Centrală era la limita capacității, deși elementul de rețea saturat nu poate fi identificat numai din prețuri. După apus, producția solară dispare, iar aerul condiționat menține cererea ridicată, așa că regiunea trebuie să importe exact atunci cînd rețeaua este plină.

Și apa a fost puțină. Producția hidro a României în iulie–august a fost de 1,94 TWh în 2024, față de 2,67 TWh în 2023, iar importul net mediu a fost de 737 MW, față de 66 MW. Vîrful verii a venit la 3 septembrie 2024, cu un preț zilnic în România de 246,89 EUR/MWh (Germania: 158,39) și un preț orar de 1021,61 EUR/MWh la ora 19:00 CEST, cel mai mare preț orar din România în datele noastre.

Concluziile pentru modelare sînt trei. Prețurile piețelor cuplate sînt egale numai cît timp rețeaua nu este la limită. Prețul din România trebuie modelat cu factori regionali: hidro, solar și consumul din sud-estul Europei. Diferența față de Germania trebuie tratată ca o variabilă separată, al cărei comportament depinde de regim.

## Studiul de caz (d): prețurile negative apar mai ales primăvara {h=ef0bee02}

Din 2023, lunile aprilie și mai concentrează 49,6% din orele cu preț negativ din România, iar lunile iunie–august încă 34,0%. Primăvara combină producția solară ridicată, lacurile pline și cererea moderată, adică exact situația în care oferta inflexibilă depășește consumul la amiază.

Panoul din dreapta arată factorul din spatele tendinței: producția solară măsurată a crescut de la 1,46 TWh în 2023 la 2,72 TWh în 2025 și a ajuns la 4,33 TWh numai în ianuarie–octombrie 2026.

@practice cele mai ieftine ore sînt cele de la amiază, în weekendurile de primăvară: atunci se încarcă bateriile, iar industria își poate programa consumul flexibil.

@chart negative_solar
Orele cu preț negativ din România pe luni calendaristice, ianuarie 2023 – octombrie 2026 (stînga), și producția solară anuală măsurată a României, în TWh, 2018–2025 (dreapta).

## Studiul de caz (d): factorii asociați zilelor cu prețuri negative {h=965acf49}

Pentru a descrie condițiile din zilele cu cel puțin un sfert de oră cu preț negativ, estimăm un model logit. Modelul descrie condițiile efectiv înregistrate, fără a oferi prognoze pentru licitare, deoarece variabilele explicative sînt cunoscute abia după eveniment.

$$ \Pr(\text{zi cu preț negativ})=\Lambda\big(\beta_0+\beta_1R_d+\beta_2\mathrm{Hyd}_d+\beta_3\mathrm{Wkd}_d+\gamma_{y}\big) $$ {#eq:logit}

unde $\Lambda(u)=1/(1+e^{-u})$ este funcția logistică, $R_d$ este consumul rezidual din ziua $d$, adică consumul minus producția solară și cea eoliană, în medii zilnice și GW, deci cererea rămasă pentru celelalte centrale, $\mathrm{Hyd}_d$ este producția hidro (GW), $\mathrm{Wkd}_d$ este 1 în zilele de weekend, iar $\gamma_y$ sînt efectele anuale. Eșantionul acoperă perioada 1 ianuarie 2024 – 31 octombrie 2026, cu $n=1\,035$ zile, dintre care 108 cu prețuri negative. Tabelul complet se află în Anexa F.

Interpretarea este simplă: fiecare GW în plus de consum rezidual înmulțește șansele unei zile cu prețuri negative cu 0,24; fiecare GW în plus de producție hidro le înmulțește cu 4,52; iar o zi de weekend le înmulțește cu 16,13. Pseudo-$R^2$ McFadden este 0,369.

@practice regenerabilele sînt limitate cel mai probabil în weekendurile de primăvară, cu lacuri pline.

## Studiul de caz (e): prețuri în creștere, saltul prețului țițeiului în martie {h=a6bc21f0}

În ianuarie–octombrie 2026, prețul mediu din România a fost de 137,45 EUR/MWh, cu 29,8% peste aceleași luni din 2025. Creșterea s-a accelerat spre sfîrșitul perioadei: în octombrie, media a fost de 239,3 EUR/MWh, față de 121,9 cu un an înainte.

Țițeiul a evoluat în același sens. Media lunară a prețului Brent a urcat de la 64,77 la 108,34 USD/bbl. În martie, prețul contractului cu scadența în mai a crescut cu 52,2%, evoluție pe care presa a pus-o pe seama conflictului cu Iranul și a situației din strîmtoarea Ormuz. Scăderea de 14,5% din 1 aprilie nu este o mișcare a pieței, ci provine doar din trecerea la contractul următor, o confirmare a regulilor de pregătire a datelor din secțiunea 2.

@practice bugetele stabilite în ianuarie s-au dovedit mult prea mici: țițeiul și oferta internă au evoluat în aceeași direcție.

@chart cy_prices
Prețurile zilnice în bandă în cele patru zone (EUR/MWh, sus) și prețul de închidere Brent (USD/bbl, jos), 1 ianuarie – 31 octombrie 2026.

## Studiul de caz (e): Cernavodă oprită de două ori, hidro sub 2025 {h=64d1ca94}

În același timp, oferta internă a scăzut. Producția nucleară a României a fost de 0 MW în 19 zile din mai, conform datelor, și din nou începînd din august: unitatea 1 a centralei de la Cernavodă a fost oprită la sfîrșitul lui iulie, iar unitatea 2 la 13 august, din cauza nivelului scăzut al Dunării, din care provine apa de răcire. Datele pentru septembrie nu sînt raportate. În ianuarie–octombrie, producția nucleară a scăzut cu 31,3% pe orele raportate în ambii ani, o limită inferioară a scăderii reale.

Producția hidro a fost cu 14,7% mai mică decît în 2025 în august–octombrie, în timp ce producția solară a fost cu 71,2% mai mare de la începutul anului. Opririle sînt documentate de comunicatele Nuclearelectrica, de World Nuclear News și de Comisia Națională pentru Controlul Activităților Nucleare (CNCAN).

@practice o singură centrală poate influența prețul la nivel național; citiți mesajele REMIT la fel de atent ca prognoza meteo.

@chart cy_generation
Producția medie lunară a României din surse nucleare, hidro și solare (GW) în 2025 și în 2026 pînă în octombrie, pe orele raportate.

## Studiul de caz (e): prețuri cu circa 30% mai mari, ofertă mai mică {h=79ab4423}

Tabelul pune alături factorii din 2026, pentru ianuarie–octombrie din fiecare an.

| ian.–oct. | 2025 | 2026 | var. % |
|---|---|---|---|
| Preț RO, EUR/MWh | 105,88 | 137,45 | +29,8 |
| Preț DE-LU, EUR/MWh | 87,66 | 114,01 | +30,1 |
| RO − DE-LU, EUR/MWh | 18,2 | 23,4 | |
| Ore cu preț negativ, RO | 196 | 171,75 | |
| Hidro RO, TWh | 9,61 | 10,44 | +8,6 |
| Nuclear RO, TWh* | 7,42 | 5,10 | −31,3 |
| Solar RO, TWh | 2,53 | 4,33 | +71,2 |
| Import net RO, TWh | 3,67 | 2,51 | |

*Numai orele raportate în ambii ani (limită inferioară).

Prețurile au crescut cu circa 30% atît în România, cît și în Germania, deci creșterea a fost europeană, dar prima prețului românesc față de cel german s-a mărit de la 18,2 la 23,4 EUR/MWh. Pe întreaga perioadă, producția hidro a fost cu 8,6% peste 2025, deși a coborît sub nivelul din 2025 la sfîrșitul verii; producția nucleară a fost mult mai mică, iar cea solară mult mai mare. Un consumator care își acoperise riscul pentru achizițiile din 2026 la începutul anului a fost protejat de cea mai mare parte a acestei creșteri.

@practice prețul a crescut cu circa 30%, cu nuclearul, hidro și țițeiul în aceeași direcție, iar acoperirea riscului s-a dovedit rentabilă.

## Studiul de caz (e): valorile extreme din 2026, România și Brent {h=aef55ec6}

Mediile ascund valorile extreme la care trebuie să reziste limitele de risc. În România, prețul de bază zilnic a variat între un minim de 29,63 EUR/MWh, la 15 februarie 2026, și un maxim de 323,76 EUR/MWh, la 29 octombrie 2026. La nivel de sfert de oră, intervalul a fost mult mai larg: de la −99,75 EUR/MWh, la 26 aprilie 2026, ora 13:00, pînă la 1015,65 EUR/MWh, la 30 iunie 2026, ora 18:45 (CET/CEST).

Graficul marchează aceste extreme pe prețul zilnic din România, împreună cu cel mai mare preț de închidere al țițeiului Brent din acest an.

@chart cy_extremes
Prețul de bază zilnic din România (EUR/MWh, stînga) și prețul de închidere Brent (USD/bbl, dreapta), 1 ianuarie – 31 octombrie 2026, cu valorile extreme ale anului marcate.

## Studiul de caz (e): valorile extreme din 2026, Germania și Brent {h=40c463ad}

Piața germană a atins pragul minim de preț. Cel mai mic preț pe sfert de oră a fost de −499,99 EUR/MWh, la 1 mai 2026, ora 13:15, egal cu pragul de −500 EUR/MWh în vigoare atunci. După asemenea prețuri la 26 aprilie și la 1 mai, prețul minim armonizat a coborît la −600 EUR/MWh pentru livrările începînd cu 29 mai 2026, conform notei SDAC publicate de OPCOM la 7 mai 2026. O serie care atinge pragul este cenzurată, așa cum am arătat în secțiunea 1.

Pentru țițeiul Brent, cel mai mare preț de închidere din 2026 a fost de 118,35 USD/bbl, la 31 martie 2026, iar cea mai mare variație zilnică, fără schimbările de contract, a fost de −13,29%, la 8 aprilie 2026.

@practice stabiliți limitele de risc pe baza valorilor extreme, nu a mediilor.

## Studiul de caz (f): din primăvara lui 2026, Bulgaria are prețuri mai mici seara {h=936af8b6}

Piețele din România și Bulgaria sînt cuplate și au de obicei aproape același preț. În orele de seară, între 19:00 și 22:00, ora locală (EET), din aprilie pînă în septembrie, prețul mediu a fost de 171,1 EUR/MWh în România și de 169,7 în Bulgaria în 2025, dar de 215,5 față de 178,0 EUR/MWh în 2026. La amiază, între 11:00 și 15:00, prețurile au rămas apropiate în 2026 (48,1 față de 46,0).

O diferență care apare numai seara este exact ceea ce ne-am aștepta să producă bateriile care se încarcă la amiază și se descarcă seara de o singură parte a graniței. Seria pentru bateriile din Bulgaria este însă raportată abia din 10 septembrie 2026, după apariția diferenței, în mai 2026, deci legătura este o asociere, nu o dovadă.

@practice un dezvoltator român de proiecte de stocare concurează pentru aceeași diferență regională amiază–seară (cursul 6).

@chart bg_battery
Diferența lunară dintre prețurile din România și Bulgaria în orele 19:00–22:00 EET (EUR/MWh, sus) și descărcarea și încărcarea bateriilor din Bulgaria (MW, jos), ianuarie 2023 – octombrie 2026, ora locală.

## @end

Studiile de caz arată aceleași fapte în acțiune: apa, opririle centralei nucleare, țițeiul, limitele rețelei și producția solară influențează prețurile din România, adesea în aceeași direcție. Fiecare constatare este o asociere, cu excepția cazurilor în care un design de cercetare adecvat permite mai mult.

# Recapitulare

Recapitularea verifică două competențe ale cursului, numărarea prețurilor negative și citirea unei autocorelații, sintetizează mesajele principale, prezintă cercetările grupului nostru pe aceeași temă și indică resurse suplimentare.

## Verifică-te {h=dea1bc7b}

1. Într-o lună de după 1 octombrie 2025, 48 de prețuri pe sfert de oră din România au fost negative, iar un membru al consiliului de administrație vă întreabă cîte ore cu preț negativ au fost. Ce îi răspundeți?
   Răspuns: $48\times15/60=12$ ore echivalente. Dacă spuneți „48 de ore”, supraevaluați durata de 4 ori față de anii anteriori, cu intervale orare. Formularea corectă este „48 de sferturi de oră (12 ore)”.
2. Un analist din echipa dumneavoastră afirmă: „autocorelația prețului PZU este 0,98 la decalajul 1 și 0,90 la decalajul 30, deci prețurile sînt zgomot alb, iar luna trecută nu ne spune nimic”. Are dreptate?
   Răspuns: Nu. Zgomotul alb are autocorelații apropiate de 0; valorile apropiate de 1 indică o persistență puternică, adică o rădăcină unitară sau o revenire foarte lentă la medie. Aplicați testele ADF și KPSS și examinați autocorelația variațiilor zilnice.

## Recapitulare {h=ec7fb96a}

Două mesaje sintetizează cursul. Prețul din România provine dintr-o singură licitație pe zi, cuplată la nivel european, cu 96 de sferturi de oră din octombrie 2025; orice număr de ore trebuie, așadar, exprimat în ore echivalente. Iar reperul pe care orice model trebuie să-l depășească este prognoza naivă, care pentru România, în 2025, a avut o MAE de 22,92 EUR/MWh. Cursul următor este dedicat prognozei (cursul 2).

## Cercetările grupului nostru despre piața din România {h=f74dff34}

Mai multe lucrări ale grupului nostru studiază aceeași piață. Andrei, Pele & Cramer (2026) realizează o analiză contrafactuală a crizei prețurilor din România din iunie–iulie 2024 (studiul de caz c), pe date orare ENTSO-E; ei arată că reducerea cererii cu 10% este cea mai robustă dintre intervențiile prioritare și că vîrful de preț s-a produs în ore aproape fără producție solară. Într-o a doua lucrare, Andrei, Pele & Cramer (2026) explică prognozele de preț: ce factori contează la fiecare orizont, de la 0–6 ore pînă la două săptămîni, și în fiecare regim de preț, pentru prețurile orare din România din perioada 2018–2024, temă reluată în cursul 7.

Proșcanu, Proșcanu, Pele & Costea (2025) compară modele sezoniere clasice cu rețele neuronale pentru prognoza consumului național al României, temă reluată în cursul 2. Proșcanu, Proșcanu & Pele (2025) arată că consumul din România este inelastic la preț și că cauzalitatea în sens Granger merge de la consum la preț, nu invers, ceea ce explică de ce curba cererii este abruptă. Shahar, Lessmann & Pele (2025) aplică metode cauzale de învățare automată liberalizării piețelor din Statele Unite și găsesc o scădere a prețului de circa 7% pe termen scurt. Rezultatele sînt preluate din rezumatele lucrărilor; toate celelalte cifre din curs provin din datele noastre.

## Vreți să aflați mai mult? {h=a5ef6cf5}

- R. Weron, IIF Distinguished Lectures despre prognoza prețurilor energiei electrice (2025): prezentări [partea I](https://p.wz.pwr.edu.pl/~weron.rafal/assets/PDF/Weron25_IIF_1.pdf), [partea a II-a](https://p.wz.pwr.edu.pl/~weron.rafal/assets/PDF/Weron25_IIF_2.pdf), [notebook-uri Jupyter](https://github.com/lipiecki/energy-analytics-2025), [înregistrări video](https://www.youtube.com/playlist?list=PLUxduCQo6_X2UTvdP9OE8DwfuBClKFNur).
- **epftoolbox**, setul de evaluare cu acces liber realizat de Lago et al. (2021): [github.com/jeslago/epftoolbox](https://github.com/jeslago/epftoolbox).
- **Forecasting: Principles and Practice**, ediția a 3-a: [otexts.com/fpp3](https://otexts.com/fpp3/).
- **Acest curs**: cod, date și notebook-uri Jupyter, la [github.com/danpele/EMQA](https://github.com/danpele/EMQA).
- **Date și reguli**: [energy-charts.info](https://www.energy-charts.info), [platforma de transparență ENTSO-E](https://transparency.entsoe.eu), [opcom.ro](https://www.opcom.ro), [transelectrica.ro](https://www.transelectrica.ro), [jao.eu](https://www.jao.eu).
- **Încercați singuri**: notebook-ul Jupyter reproduce fiecare grafic și fiecare cifră din acest curs, [L1_notebook_ro.ipynb](https://github.com/danpele/EMQA/blob/main/notebooks/L1_notebook_ro.ipynb).

# Anexă

Anexa prezintă formulele complete ale testelor de rădăcină unitară, un exemplu de calcul pentru descompunerea clasică, algoritmul STL, mixul de producție și prognoza naivă în cifre, statisticile pentru cozile groase împreună cu tabelul complet al modelului logit și conversia prețurilor combustibililor în EUR/MWh.

## Anexa A: testele ADF și KPSS în detaliu {h=c0363199}

Regresia ADF în forma sa generală (Said & Dickey, 1984) este

$$ \Delta x_t=\alpha+\beta t+\gamma x_{t-1}+\sum_{j=1}^{p}\delta_j\Delta x_{t-j}+u_t $$ {#eq:adffull}

unde $\beta t$ este un trend determinist, iar celelalte simboluri au semnificația din @eq:adf. Ipotezele sînt $H_0:\gamma=0$ față de $H_1:\gamma<0$; statistica $\tau=\hat\gamma/\mathrm{se}(\hat\gamma)$ urmează distribuția Dickey–Fuller, nu distribuția Student, iar valorile $p$ se calculează după MacKinnon (1996). Numărul de decalaje se alege prin minimizarea AIC, pornind de la $p_{\max}=12(T/100)^{1/4}$. Termenii determiniști trebuie să corespundă ipotezei alternative: o constantă pentru staționaritatea în nivel, un trend pentru staționaritatea în jurul trendului.

Statistica KPSS (Kwiatkowski et al., 1992) este

$$ \mathrm{KPSS}=\frac{1}{T^2\hat\sigma^2_{\mathrm{LR}}}\sum_{t=1}^T S_t^2,\qquad S_t=\sum_{s\le t}e_s $$ {#eq:kpss}

$$ \hat\sigma^2_{\mathrm{LR}}=\hat\gamma_0+2\sum_{k=1}^{\ell}\Big(1-\frac{k}{\ell+1}\Big)\hat\gamma_k $$ {#eq:lrvar}

unde $e_s$ sînt reziduurile regresiei pe o constantă (și pe trend), $S_t$ sînt sumele lor parțiale, $\hat\sigma^2_{\mathrm{LR}}$ este dispersia pe termen lung, estimată cu nucleul Bartlett, $\hat\gamma_k$ este autocovarianța reziduurilor la decalajul $k$, iar $\ell$ este lățimea de bandă, aleasă prin regula Hobijn et al. din statsmodels. Valoarea critică la 5% pentru varianta în nivel este 0,463.

## Anexa B: descompunerea clasică, exemplu de calcul {h=f0873907}

Pentru date lunare, trendul clasic este o medie mobilă centrată pe 13 luni, cu ponderi înjumătățite la capete:

$$ \hat T_t=\frac{1}{24}x_{t-6}+\frac{1}{12}\sum_{j=-5}^{5}x_{t+j}+\frac{1}{24}x_{t+6} $$ {#eq:matrend}

unde $x_t$ este consumul mediu lunar, iar $\hat T_t$ este trendul estimat. Pentru consumul României (GW), ianuarie 2016 – decembrie 2025, prima valoare a trendului, pentru iulie 2016, este $\hat T=\frac{1}{24}(7{,}424+7{,}870)+\frac{1}{12}\cdot 72{,}503=6{,}679$ GW, cu ianuarie 2016 și ianuarie 2017 cu pondere înjumătățită și lunile februarie–decembrie 2016 însumate. Valoarea observată a fost de 6,389 GW, deci abaterea față de trend este −0,290.

Indicele sezonier al lunii $j$ este $\hat S_j=\bar d_j-\frac1{12}\sum_i\bar d_i$, unde $\bar d_j$ este abaterea medie față de trend în luna $j$; suma mediilor brute a fost 0,0005, deci corecția este foarte mică. Rezultatele au fost verificate cu statsmodels.

| Luna | Indice | Luna | Indice |
|---|---|---|---|
| ian. | 0,686 | iul. | −0,143 |
| feb. | 0,694 | aug. | −0,302 |
| mar. | 0,237 | sep. | −0,444 |
| apr. | −0,381 | oct. | −0,194 |
| mai | −0,650 | noi. | 0,374 |
| iun. | −0,442 | dec. | 0,565 |

## Anexa C: algoritmul STL {h=ebc580ce}

STL alternează două bucle (Cleveland, Cleveland, McRae & Terpenning, 1990). Bucla interioară, repetată de mai multe ori, (1) elimină trendul, $x_t-\hat T_t$; (2) netezește fiecare subserie lunară (toate lunile ianuarie, toate lunile februarie și așa mai departe) prin loess cu fereastra $n_s$; (3) elimină componenta de frecvență joasă a rezultatului, obținînd componenta sezonieră $\hat S_t$; și (4) netezește $x_t-\hat S_t$ prin loess cu fereastra $n_t$, obținînd trendul $\hat T_t$.

Bucla exterioară calculează ponderi de robustețe $\rho_t=B\big(|\hat R_t|/(6\,\mathrm{median}|\hat R|)\big)$, cu $B(u)=(1-u^2)^2$ pentru $|u|<1$ și 0 altfel, unde $\hat R_t$ este componenta reziduală; astfel, valorile extreme cîntăresc mai puțin în bucla interioară următoare. Aici folosim perioada 12, $n_s=13$ și varianta robustă. Intensitatea sezonalității, $1-\Var(R)/\Var(S+R)$, este 0,848. STL este numai aditiv: în cazul sezonalității multiplicative, se aplică seriei transformate prin $\ln x_t$ sau, pentru prețuri, prin asinh.

## Anexa D: mixul de producție în cifre {h=3ae6f974}

| Pondere, % | 2015 | 2020 | 2023 | 2024 | 2025 | ian.–oct. 2025 | ian.–oct. 2026 |
|---|---|---|---|---|---|---|---|
| Hidro | 26,2 | 27,8 | 32,4 | 27,9 | 25,6 | 25,7 | 27,6 |
| Nuclear | 17,9 | 20,7 | 19,8 | 21,1 | 21,3 | 19,8 | 13,5 |
| Cărbune | 28,3 | 17,4 | 14,4 | 13,6 | 13,8 | 14,4 | 12,1 |
| Gaze | 14,6 | 18,4 | 16,9 | 20,1 | 20,2 | 19,8 | 20,5 |
| Eolian | 10,3 | 12,4 | 13,2 | 12,4 | 12,4 | 12,6 | 13,9 |
| Solar | 1,9 | 2,4 | 2,6 | 4,1 | 5,7 | 6,8 | 11,4 |
| Biomasă | 0,8 | 0,9 | 0,7 | 0,9 | 0,9 | 0,9 | 1,0 |
| **Total TWh** | 64,2 | 55,4 | 56,6 | 51,2 | 47,4 | 37,4 | 37,9 |
| Consum TWh | 57,0 | 58,1 | 53,4 | 54,3 | 53,6 | 43,9 | 42,3 |
| Import net TWh | −6,9 | 1,9 | −3,1 | 3,0 | 3,8 | 3,7 | 2,5 |

Ultimele două coloane folosesc numai orele raportate în ambii ani. Un import net pozitiv înseamnă energie intrată în România. Între 2015 și 2025, producția totală a scăzut de la 64,2 la 47,4 TWh, în timp ce consumul s-a modificat puțin, iar țara a trecut de la exportator net la importator net.

## Anexa E: prognoza naivă, toți anii {h=1a8805bc}

| MAE | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|
| RO naivă | 9,7 | 7,4 | 19,9 | 59,7 | 26,0 | 27,7 | 22,9 | 29,4 |
| RO d−1 | 10,7 | 8,1 | 22,2 | 58,5 | 27,3 | 29,7 | 24,9 | 31,1 |
| RO d−7 | 11,2 | 8,6 | 25,1 | 75,4 | 31,0 | 33,9 | 28,2 | 36,6 |
| DE-LU naivă | 9,8 | 9,3 | 24,3 | 66,2 | 28,6 | 27,3 | 27,5 | 36,1 |
| DE-LU d−1 | 9,5 | 10,0 | 25,3 | 58,2 | 27,2 | 27,8 | 26,0 | 32,8 |
| DE-LU d−7 | 10,3 | 10,3 | 31,5 | 87,1 | 33,6 | 32,8 | 32,8 | 42,2 |

MAE este exprimată în EUR/MWh, pe prețuri orare; din octombrie 2025, prețul orar este media celor patru prețuri pe 15 minute. În România, regula naivă este cea mai bună dintre cele trei variante în fiecare an, cu excepția lui 2022, cînd decalajul simplu de o zi a fost puțin mai bun. În Germania, decalajul de o zi cîștigă mai des, ceea ce arată că și reperul trebuie verificat pentru fiecare piață în parte (Nogales et al., 2002; Weron, 2014).

## Anexa F: cozile groase și modelul logit, în detaliu {h=8a510e0f}

Asimetria, aplatizarea și statistica Jarque–Bera sînt

$$ \hat S=\frac{\frac1T\sum_t(r_t-\bar r)^3}{\hat\sigma^3},\qquad \hat K=\frac{\frac1T\sum_t(r_t-\bar r)^4}{\hat\sigma^4} $$ {#eq:skewkurt}

$$ \mathrm{JB}=\frac T6\Big(\hat S^2+\frac{(\hat K-3)^2}{4}\Big)\sim\chi^2_2 $$ {#eq:jb}

unde $r_t$ este randamentul din ziua $t$, $\bar r$ este randamentul mediu, $\hat\sigma$ este abaterea standard, $T$ este numărul de randamente, $\hat S$ este asimetria, $\hat K$ este aplatizarea ($\hat K-3$ fiind excesul de aplatizare), iar $\chi^2_2$ este distribuția hi-pătrat cu două grade de libertate, pe care o urmează JB în ipoteza normalității. Pentru randamentele logaritmice zilnice ale țițeiului Brent, fără zilele de schimbare a contractului, asimetria este −0,94, excesul de aplatizare 13,98, iar JB 23 500, față de o valoare critică de 5,99 la 5%. Distribuția Student-$t$ ajustată are 3,21 grade de libertate, deci cozi foarte groase.

Modelul logit complet pentru o zi cu cel puțin un sfert de oră cu preț negativ în România, cu 2024 ca an de bază (@eq:logit):

| | estimație | raportul șanselor | z |
|---|---|---|---|
| Constantă | −0,023 | 0,98 | −0,02 |
| Consum rezidual, GW | −1,445 | 0,24 | −7,67 |
| Hidro, GW | 1,508 | 4,52 | 4,37 |
| Weekend | 2,780 | 16,13 | 9,24 |
| Anul 2025 | 1,337 | 3,81 | 3,98 |
| Anul 2026 | 0,534 | 1,71 | 1,54 |

Raportul șanselor este exponențiala coeficientului. La același consum rezidual, aceeași producție hidro și același tip de zi, o zi din 2025 a avut șanse mai mari de preț negativ decît o zi din 2024, în timp ce efectul anului 2026 nu este semnificativ.

## Anexa G: conversia prețurilor gazelor și țițeiului în EUR/MWh {h=bdbd21ff}

Un preț al gazelor exprimat în USD pe MMBtu se convertește în EUR/MWh astfel:

$$ P^{\text{EUR/MWh}}=P^{\text{USD/MMBtu}}\times 3{,}412142\,/\,e_m $$ {#eq:convert}

unde $1\ \text{MMBtu}=0{,}293071$ MWh, deci $1/0{,}293071=3{,}412142$ MMBtu pe MWh, iar $e_m$ este cursul mediu lunar USD pe EUR publicat de ECB. Țițeiul Brent se cotează în USD/bbl, un baril avînd 159 de litri.

Prețul TTF publicat de Banca Mondială este o medie lunară în USD/MMBtu, convertită cu cursul ECB; nu este o cotație tranzacționată în EUR. Combustibilii și energia electrică trebuie comparați numai în aceeași unitate și în aceeași monedă: un preț al gazelor în USD/MMBtu și unul al energiei în EUR/MWh diferă printr-un factor de circa 3,4, înainte de aplicarea cursului de schimb.
