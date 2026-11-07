r"""
build_L2.py -- Lecture 2 "Forecasting Electricity Prices" (EMQA), English and Romanian from one source
=====================================================================================================
Writes lectures/L2/lecture2.tex (EN) and lectures/L2/lecture2_ro.tex (RO) from the bilingual slide text in this file
and the numbers in L2_numbers.json (produced by analysis_L2.py), compiles both with pdflatex and checks: 0 LaTeX errors;
no overfull box > 1 pt (nothing masked); every acronym in the Abbreviations frames and spelled out at first use;
contact sheets for the visual check.

Run (from anywhere):
    python3 lectures/L2/analysis_L2.py
    python3 lectures/L2/build_L2.py            # both languages;  add "en" or "ro" for one

Rules as in Lecture 1: no computed number typed by hand (results are @{key} placeholders); hand-typed numbers are
definitions (12:00 CET, 1.4826, 0.05, window lengths, 1 MW / 2 MWh, 90% efficiency) and institutional dates.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_build import (Deck, Numbers, acronym_audit, autofit, block, cols, contact_sheet,  # noqa: E402
                        first_use_audit, fmt, heat, hier, items, table)


def it(*xs, sep="1pt"):
    """Bullets: a string is split by hier() (first clause = level 1, the rest = level 2); a tuple
    (head, sub1, sub2, ...) gives an explicit level-1 head with its level-2 bullets."""
    sep = "1pt" if float(sep.replace("pt", "")) > 1 else sep

    def one(x):
        if isinstance(x, tuple):
            return (x[0] + "\n    \\begin{itemize}\\setlength{\\itemsep}{0pt}\n" +
                    "\n".join("      \\item " + (s[0].upper() + s[1:] if s[0].islower() else s) for s in x[1:] if s) + "\n    \\end{itemize}")
        return hier(x)
    return (f"\\begin{{itemize}}\\setlength{{\\itemsep}}{{{sep}}}\n" + "\n".join("  \\item " + one(x) for x in xs if x) +
            "\n\\end{itemize}")


def note(*xs):
    return ("\n\\par\\vspace{0.5mm}{\\scriptsize " + items(*xs, opt="\\setlength{\\itemsep}{0pt}", nest=False) + "}")


# =============================================================================
# Abbreviations (EN, RO) -- used by both audits
# =============================================================================
ABBR = {
    "ADF": ("augmented Dickey--Fuller test", "testul Dickey--Fuller augmentat"),
    "AI": ("artificial intelligence", "inteligență artificială"),
    "AIC": ("Akaike information criterion", "criteriul informațional Akaike"),
    "ARX": ("autoregressive model with exogenous variables", "model autoregresiv cu variabile exogene"),
    "AW": ("averaging across calibration windows", "medierea prognozelor obținute pe mai multe ferestre de calibrare"),
    "AW-ARX": ("ARX averaged across calibration windows", "ARX mediat pe ferestre de calibrare"),
    "AW-LEAR": ("LEAR averaged across calibration windows", "LEAR mediat pe ferestre de calibrare"),
    "CET": ("Central European Time", "ora Europei Centrale"),
    "CP": ("conformal prediction", "predicție conformală"),
    "CRPS": ("continuous ranked probability score", "scorul de probabilitate ordonat continuu (continuous ranked probability score)"),
    "CVaR": ("conditional value at risk", "valoarea la risc condiționată (conditional value at risk)"),
    "DE-LU": ("Germany--Luxembourg bidding zone", "zona de ofertare Germania--Luxemburg"),
    "DM": ("Diebold--Mariano test", "testul Diebold--Mariano"),
    "DNN": ("deep neural network", "rețea neuronală profundă"),
    "DST": ("daylight saving time", "ora de vară"),
    "ECM": ("error-correction model", "model cu corecția erorii"),
    "EUPHEMIA": ("Pan-European Hybrid Electricity Market Integration Algorithm",
                 "algoritmul comun de cuplare a piețelor europene (Pan-European Hybrid Electricity Market Integration Algorithm)"),
    "ENTSO-E": ("European Network of Transmission System Operators for Electricity",
                "Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică"),
    "EPEX": ("EPEX SPOT power exchange", "bursa europeană de energie EPEX SPOT"),
    "ETC": ("exchange-traded commodity", "titlu tranzacționat la bursă, garantat cu mărfuri (exchange-traded commodity)"),
    "EU": ("European Union", None),
    "UE": (None, "Uniunea Europeană"),
    "EUA": ("EU emission allowance (1 t CO$_2$)", "certificat de emisii al UE (1 t CO$_2$)"),
    "GBM": ("gradient boosting machine (boosted trees)", "gradient boosting (ansamblu de arbori de decizie construiți secvențial)"),
    "HS": ("historical simulation", "simulare istorică"),
    "HU": ("Hungary (bidding zone)", "Ungaria (zonă de ofertare)"),
    "HUPX": ("Hungarian Power Exchange", "bursa de energie din Ungaria"),
    "ISE": ("Fraunhofer Institute for Solar Energy Systems", "Institutul Fraunhofer pentru Sisteme de Energie Solară"),
    "LASSO": ("least absolute shrinkage and selection operator", "operatorul de contracție și selecție în normă absolută"),
    "LARS": ("least angle regression", "regresia unghiului minim (least angle regression)"),
    "LEAR": ("LASSO-estimated autoregression", "autoregresie estimată cu LASSO"),
    "LR": ("likelihood ratio", "raportul de verosimilitate"),
    "MAD": ("median absolute deviation", "abaterea absolută mediană"),
    "MAE": ("mean absolute error", "eroarea absolută medie"),
    "MAPE": ("mean absolute percentage error", "eroarea procentuală absolută medie"),
    "ML": ("machine learning", "învățare automată"),
    "MLP": ("multilayer perceptron (feed-forward neural network)", "perceptron multistrat (rețea neuronală directă)"),
    "MTU": ("market time unit", "intervalul de tranzacționare (market time unit)"),
    "OLS": ("ordinary least squares", "metoda celor mai mici pătrate"),
    "OPCOM": ("Romanian electricity and gas market operator", "operatorul pieței de energie electrică și de gaze naturale din România"),
    "PS": ("pinball score", "scorul pinball"),
    "PZU": ("Piața pentru Ziua Următoare (day-ahead market)", "piața pentru ziua următoare"),
    "ReLU": ("rectified linear unit", "unitate liniară rectificată (rectified linear unit)"),
    "RSS": ("residual sum of squares", "suma pătratelor reziduurilor"),
    "QRA": ("quantile regression averaging", "medierea prin regresie cuantilică"),
    "RMSE": ("root mean squared error", "rădăcina erorii pătratice medii"),
    "RO": ("Romania (bidding zone)", "România (zonă de ofertare)"),
    "rMAE": ("relative MAE (model MAE / naive MAE)", "MAE relativă (MAE a modelului / MAE a modelului naiv)"),
    "sMAPE": ("symmetric MAPE", "MAPE simetrică"),
    "SDAC": ("Single Day-Ahead Coupling", "cuplarea unică a piețelor pentru ziua următoare"),
    "TSO": ("transmission system operator", "operator de transport și de sistem"),
    "UC": ("unconditional coverage", "acoperire necondiționată"),
    "TTF": ("Title Transfer Facility (Dutch gas hub)", "Title Transfer Facility (hub olandez de gaze)"),
    "VST": ("variance-stabilising transformation", "transformare de stabilizare a varianței"),
    "EUR": ("euro", "euro"), "MW": ("megawatt", "megawatt"), "MWh": ("megawatt-hour", "megawatt-oră"),
    "TWh": ("terawatt-hour", "terawatt-oră"),
}
UNITS = {"EUR", "MW", "MWh", "TWh"}
# journal codes inside citations only; everything else must be in the Abbreviations list and spelled out
IGNORE = {"AI", "ReP", "EMQA", "IJF", "ENEECO", "APEN", "JASA", "TPWRS", "TSTE", "IEEE", "JBES", "RSER", "JRSS", "PICBE", "RJEF",
          "IIF", "SPOT", "CO", "II", "NEMO", "AIDA", "TabPFN", "UK", "SICI", "AID-JAE"}


def build(lang, H=None):
    V = Numbers(os.path.join(HERE, "L2_numbers.json"), lang)
    N = V.N
    D = Deck(2, "Forecasting Electricity Prices" if lang == "en" else "Prognoza prețurilor energiei electrice", V, lang, heights=H)
    t = D.t
    ro = lang == "ro"
    if ro:   # notebook pointer in natural Romanian: "notebook-ul Jupyter, secțiunea 2"
        _tex = D.tex
        D.tex = lambda: _tex().replace("notebook-ul Jupyter \\S", "notebook-ul Jupyter, secțiunea ")
    NB = t("notebook", "notebook-ul Jupyter")

    def de(key):
        v = int(round(float(V.get(key))))
        return "de " if ro and v >= 20 and (v % 100 >= 20 or v % 100 == 0) else ""

    def pval(key):
        p = float(V.get(key))
        if p < 0.001:
            return "$<$0{,}001" if ro else "$<$0.001"
        return fmt(p, ".3f", lang)

    MN = {"naive": t("naive", "naiv"), "snaive": t("seasonal naive", "naiv sezonier"), "aw_arx": "AW-ARX", "aw_lear": "AW-LEAR",
          "gbm": "GBM", "mlp": "MLP", "ens_all": t("ensemble of 4", "ansamblul de 4 modele"), "ens_lm": t("LEAR+MLP", "LEAR+MLP"),
          "arx728": "ARX(728)", "lear728": "LEAR(728)"}
    TEST = t("test year @{design.test_start|date} -- @{design.test_end|date}", "anul de test @{design.test_start|date} -- @{design.test_end|date}")
    CITE_W = "(Weron, 2014, IJF; Lago, Marcjasz, De Schutter \\& Weron, 2021, APEN)"

    # ------------------------------------------------------------------ front matter
    D.parts.append("% END-FRONT-MATTER\n")
    D.frame(t("Learning objectives", "Obiectivele cursului"), it(
        t("Set up a day-ahead forecast that uses only what is known at 12:00 Central European Time (CET) on the day before delivery.",
          "Construirea unei prognoze pentru piața pentru ziua următoare (PZU); licitația se închide la ora 12:00 a Europei Centrale (CET) "
          "în ziua dinaintea livrării; prognoza poate folosi numai datele disponibile înainte de acest moment"),
        t("Measure accuracy with the mean absolute error (MAE), the root mean squared error (RMSE) and the relative MAE (rMAE), and "
          "test differences with the Diebold--Mariano (DM) test.",
          "Măsurarea acurateței prognozelor; eroarea absolută medie (MAE), rădăcina erorii pătratice medii (RMSE) și MAE relativă (rMAE), "
          "adică eroarea modelului împărțită la eroarea unui model naiv; testul Diebold--Mariano (DM) arată dacă diferența dintre două modele este semnificativă"),
        t("Build expert autoregressive models with exogenous variables (ARX), shrink them with the least absolute shrinkage and "
          "selection operator (LASSO) and obtain the LASSO-estimated autoregression (LEAR).",
          "Estimarea modelelor expert; modelul autoregresiv cu variabile exogene (ARX), cîte o regresie pentru fiecare oră; aceeași regresie, cu "
          "penalizarea operatorului de contracție și selecție în normă absolută (LASSO), devine autoregresia estimată cu LASSO (LEAR)"),
        t("Combine forecasts, preview machine learning (ML) and turn point forecasts into quantiles with quantile regression averaging (QRA).",
          "Combinarea prognozelor și construirea intervalelor de prognoză; media mai multor modele, inclusiv modele de învățare automată (ML); "
          "cuantile ale prețului obținute prin medierea prin regresie cuantilică (QRA)"),
        t("Test cointegration of Romania with Hungary, and of power with gas and hydro, as announced in Lecture 1.",
          "Testarea cointegrării, anunțată în cursul 1; prețurile din România și din Ungaria; prețul energiei electrice, prețul gazelor și producția hidro"),
        sep="4pt"))

    ab = sorted([(k, v) for k, v in ABBR.items() if v[0 if not ro else 1] is not None], key=lambda kv: kv[0].lower())

    def abcol(lst):
        return ("{\\scriptsize\\renewcommand{\\arraystretch}{0.96}\\begin{tabular}{@{}>{\\bfseries}l@{\\ \\ }"
                "p{0.76\\linewidth}@{}}" + "\n".join(f"{k} & {v[0] if not ro else v[1]}\\\\" for k, v in lst) + "\\end{tabular}}")

    D.parts.append("% BEGIN-ABBR\n")
    half = (len(ab) + 1) // 2
    for part, lst in enumerate([ab[:half], ab[half:]]):
        hh = (len(lst) + 1) // 2
        D.frame(t("Abbreviations", "Abrevieri") + f" ({part + 1}/2)", "\\vspace{-1mm}\\begin{columns}[T,onlytextwidth]\n" + "".join(
            f"\\begin{{column}}{{0.49\\textwidth}}{abcol(lst[i * hh:(i + 1) * hh])}\\end{{column}}\n" for i in range(2)) +
            "\\end{columns}")
    D.parts.append("% END-ABBR\n")

    D.frame(t("Real data only: what we forecast and with what", "Prognozăm prețul orar PZU din România, numai cu date reale"), table(
        "@{}p{0.36\\textwidth}p{0.12\\textwidth}p{0.47\\textwidth}@{}",
        [t("Series", "Seria"), t("Frequency", "Frecvența"), t("Source", "Sursa")],
        [[t("Target: day-ahead price of Romania (RO), Piața pentru Ziua Următoare (PZU)",
            "Variabila prognozată: prețul energiei electrice pe piața pentru ziua următoare (PZU) din România (RO)"),
          t("hourly", "orară"),
          t("the Romanian electricity and gas market operator (OPCOM), via energy-charts.info (Fraunhofer ISE) and the European "
            "Network of Transmission System Operators for Electricity (ENTSO-E)",
            "operatorul pieței de energie electrică și de gaze naturale din România (OPCOM), prin energy-charts.info (Fraunhofer ISE) "
            "și Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E)")],
         [t("Load, wind + solar, hydro, nuclear, cross-border flows", "Consumul; producția eoliană, solară, hidro și nucleară; fluxurile transfrontaliere"),
          t("hourly, daily", "orară, zilnică"), t("ENTSO-E (Transelectrica data for Romania), via energy-charts.info",
                                                  "ENTSO-E (date Transelectrica pentru România), prin energy-charts.info")],
         [t("Carbon: European Union (EU) emission allowance (EUA), proxy", "Prețul certificatului de emisii (EUA) al Uniunii Europene (UE), aproximat"), t("daily", "zilnică"),
          t("Yahoo Finance, SparkChange physical EUA exchange-traded commodity (ETC)",
            "Yahoo Finance: SparkChange, titlu tranzacționat la bursă și garantat fizic cu certificate EUA (ETC)")],
         [t("Neighbours: Hungary (HU), Germany--Luxembourg (DE-LU); gas: Title Transfer Facility (TTF)",
            "Piețe vecine: Ungaria (HU), Germania--Luxemburg (DE-LU); gaze naturale: hubul olandez Title Transfer Facility (TTF)"),
          t("daily, monthly", "zilnică, lunară"),
          t("Hungarian Power Exchange (HUPX), European Power Exchange (EPEX SPOT), via energy-charts.info; World Bank Pink Sheet (TTF)",
            "bursa de energie din Ungaria (HUPX) și bursa europeană de energie (EPEX SPOT), prin energy-charts.info; Banca Mondială, Pink Sheet (TTF)")]],
        size="scriptsize", stretch="0.93") + "\n\\vspace{0.5mm}\n" + it(
        t("\\textbf{Cut-off @{cutoff.end|date}}, downloaded @{cutoff.download|date}; panel @{data.start|date} -- @{data.end|date}, "
          "@{data.n_days|,d} complete days.",
          "\\textbf{Perioada analizată}: @{data.start|date} -- @{data.end|date} (@{data.n_days|,d} " + de("data.n_days") + "zile complete); "
          "date descărcate la @{cutoff.download|date}"),
        t("\\textbf{Test} = the last @{design.n_test} days (@{design.test_start|date} -- @{design.test_end|date}); \\textbf{burn-in} = "
          "the @{design.n_burn} days before, used only to calibrate the intervals.",
          "\\textbf{Perioada de test}: ultimele @{design.n_test} " + de("design.n_test") + "zile (@{design.test_start|date} -- "
          "@{design.test_end|date}); \\textbf{Rodajul (burn-in)}: cele @{design.n_burn} " + de("design.n_burn") +
          "zile dinainte, folosite numai pentru calibrarea intervalelor"),
        t("Daylight saving time (DST): 24 columns per day as in Assignment 1; the missing spring hour is the mean of its neighbours, "
          "the doubled autumn hour is averaged; @{design.n_dst_test} DST days in the test year, kept.",
          "\\textbf{Ora de vară (DST)}: 24 de ore pe zi, ca în tema 1; ora lipsă din martie și ora dublată din octombrie se înlocuiesc cu medii; "
          "cele @{design.n_dst_test} zile cu schimbarea orei din anul de test rămîn în analiză"),
        sep="1pt") + D.bottom(None, NB + " \\S1"), "footnotesize")

    # ------------------------------------------------------------------ 1 the forecasting problem
    D.section(t("The forecasting problem and its benchmarks", "Problema de prognoză și modelele de referință"))
    D.subsection(t("The day-ahead market", "Piața pentru ziua următoare"))
    D.frame(t("Day-ahead market: the auction on $d-1$ sets the 96 prices of day $d$",
              "PZU: licitația din ziua $d-1$ fixează cele 96 de prețuri ale zilei $d$"), """
\\begin{center}
\\begin{tikzpicture}[x=1cm,y=1cm]
\\draw[-{Latex},thick,MainBlue] (0,0) -- (14.3,0);
\\foreach \\x in {0.2,4.9,9.6} {\\draw[MainBlue] (\\x,-0.12) -- (\\x,0.12);}
\\node[font=\\scriptsize,anchor=north west] at (0.2,-0.12) {""" + t("day $d-2$", "ziua $d-2$") + """};
\\node[font=\\scriptsize,anchor=north west] at (4.9,-0.12) {""" + t("day $d-1$: trading day", "ziua $d-1$: ziua licitației") + """};
\\node[font=\\scriptsize,anchor=north west] at (9.6,-0.12) {""" + t("day $d$: delivery day", "ziua $d$: ziua livrării") + """};
\\fill[Forest] (7.25,0) circle (3pt);
\\node[font=\\scriptsize,align=center,text width=3.2cm] at (5.5,0.85) {\\textbf{12:00 CET}\\\\ """ +
        t("order books close (gate closure)", "se închide registrul de oferte") + """};
\\draw[Forest,thick] (7.25,0) -- (6.4,0.45);
\\fill[Crimson] (7.75,0) circle (2.4pt);
\\node[font=\\scriptsize,align=center,text width=2.8cm] at (9.1,0.85) {""" +
        t("about 13:00 CET: prices of day $d$ published", "circa 13:00 CET: se publică prețurile zilei $d$") + """};
\\draw[Crimson] (7.75,0) -- (8.5,0.45);
\\draw[thick,Crimson,{Latex}-{Latex}] (9.6,-0.6) -- (14.2,-0.6) node[midway,below,font=\\scriptsize] {""" +
        t("00:00--24:00: 96 quarter-hour prices", "00:00--24:00: 96 de prețuri pe sfert de oră") + """};
\\end{tikzpicture}
\\end{center}
\\vspace{-2mm}
""" + it(t(("\\textbf{What it is}", "a single daily auction of the Single Day-Ahead Coupling (SDAC), run in Romania by OPCOM",
            "buyers and sellers submit orders (quantity, price) for each period of the next day"),
           ("\\textbf{Ce este}", "licitația zilnică a cuplării unice a piețelor pentru ziua următoare (SDAC); în România o organizează OPCOM",
            "cumpărătorii și vînzătorii depun oferte (cantitate, preț) pentru fiecare interval al zilei următoare")),
         t(("\\textbf{How prices are set}", "at 12:00 CET on day $d-1$ the order books close (gate closure)",
            "a common algorithm, the Pan-European Hybrid Electricity Market Integration Algorithm (EUPHEMIA), matches supply and demand; results normally around 13:00 CET"),
           ("\\textbf{Cum se formează prețul}", "la ora 12:00 CET din ziua $d-1$ se închide registrul de oferte",
            "un algoritm comun, Pan-European Hybrid Electricity Market Integration Algorithm (EUPHEMIA), echilibrează cererea și oferta în limita capacităților transfrontaliere; rezultatele se publică de regulă în jurul orei 13:00 CET")),
         t(("\\textbf{Delivery periods}", "since 1 October 2025: 96 quarter-hour prices per day (before: 24 hourly)",
            "our data: hourly price = mean of the four quarter-hours, used for the whole test year"),
           ("\\textbf{Intervalele de livrare}", "din ziua de livrare 1 octombrie 2025: 96 de prețuri pe sfert de oră (înainte: 24 de prețuri orare)",
            "în datele noastre, prețul orar = media celor patru sferturi de oră; tot anul de test folosește aceste medii")),
         sep="1pt"), "footnotesize", cite="(NEMO Committee, 2025, 2026; OPCOM)")
    D.frame(t("Notation, and the rule every forecast in this lecture obeys",
              "Notația și regula pe care o respectă toate prognozele din acest curs"), it(
        t(("\\textbf{Notation}", "$d$ = delivery day; $d-1$ = the day before, when the auction runs; $d-2$ = two days before",
           "$h=0,\\dots,23$ = hour of delivery (CET); $P_{d,h}$ = day-ahead price of hour $h$ on day $d$, in EUR/MWh; $\\hat P_{d,h}$ = its forecast"),
          ("\\textbf{Notația}", "$d$ = ziua livrării; $d-1$ = ziua dinainte, în care are loc licitația; $d-2$ = cu două zile înainte",
           "$h=0,\\dots,23$ = ora livrării (CET); $P_{d,h}$ = prețul PZU al orei $h$ din ziua $d$, în EUR/MWh; $\\hat P_{d,h}$ = prognoza acestui preț")),
        t(("\\textbf{The rule}", "the forecast for day $d$ is made before 12:00 CET on day $d-1$, so it may use only what is known at that moment",
           "allowed: all 24 prices of day $d-1$ (fixed by the auction on day $d-2$); load, wind and solar forecasts for day $d$ published by the transmission system operator (TSO) before 12:00",
           "not allowed: any realised value of day $d$, or values of day $d-1$ that are not yet metered"),
          ("\\textbf{Regula}", "prognoza pentru ziua $d$ se face înainte de ora 12:00 CET din ziua $d-1$, deci poate folosi numai ce se cunoaște în acel moment",
           "permis: toate cele 24 de prețuri ale zilei $d-1$ (stabilite prin licitația din ziua $d-2$); prognozele de consum și de producție eoliană și solară pentru ziua $d$, publicate de operatorul de transport și de sistem (TSO) înainte de 12:00",
           "interzis: orice valoare realizată în ziua $d$ și valorile zilei $d-1$ care nu sînt încă măsurate")),
        t(("\\textbf{What we forecast and how we score it}", "the 24 hourly prices of the Romanian PZU, for each day of the test year",
           "the error $P_{d,h}-\\hat P_{d,h}$ is known only after day $d$ is delivered"),
          ("\\textbf{Ce prognozăm și cum evaluăm}", "cele 24 de prețuri orare PZU din România, pentru fiecare zi a anului de test",
           "eroarea $P_{d,h}-\\hat P_{d,h}$ se cunoaște abia după livrarea din ziua $d$")),
        sep="4pt") + D.bottom(t("the same rule binds a real trading desk; a model that breaks it cannot be run at 12:00.",
                                "aceeași regulă se aplică oricărui birou de tranzacționare; un model care o încalcă nu poate fi rulat la 12:00.")),
        "footnotesize", cite="(NEMO Committee, 2025; Lago et al., 2021, APEN)")
    D.subsection(t("Information set and horizons", "Informațiile disponibile și orizontul"))
    tl = t
    D.frame(t("At 12:00 CET on $d-1$ you know prices to $d-1$, metered data to $d-2$",
              "Prognoza zilei $d$ folosește doar datele cunoscute la 12:00 CET în ziua $d-1$"), """
\\begin{center}
\\begin{tikzpicture}[x=1cm,y=1cm]
\\draw[-{Latex},thick,MainBlue] (0,0) -- (14.3,0);
\\foreach \\x/\\l in {0.2/{""" + tl("day $d-2$", "ziua $d-2$") + """}, 4.9/{""" + tl("day $d-1$", "ziua $d-1$ (licitația)") + """}, 9.6/{""" +
        tl("day $d$ (delivery)", "ziua $d$ (livrarea)") + """}}
  {\\draw[MainBlue] (\\x,-0.12) -- (\\x,0.12); \\node[font=\\scriptsize,below,anchor=north west] at (\\x,-0.12) {\\l};}
\\fill[Forest] (7.25,0) circle (3pt);
\\node[font=\\scriptsize,align=center,text width=4.0cm] at (7.25,0.95) {\\textbf{""" +
        tl("12:00 CET: gate closure", "12:00 CET: închiderea licitației") + """}\\\\ """ +
        tl("the forecast and the bids for day $d$ are sent", "se trimit ofertele pentru ziua $d$") + """};
\\draw[Forest,thick] (7.25,0) -- (7.25,0.55);
\\fill[Crimson] (4.9,0) circle (2.4pt);
\\node[font=\\scriptsize,align=center,text width=3.2cm] at (3.1,0.95) {""" +
        tl("24:00 of $d-2$: last complete metered day", "sfîrșitul zilei $d-2$: ultima zi măsurată complet") + """};
\\draw[Crimson] (4.9,0) -- (3.9,0.6);
\\fill[MainBlue] (2.55,0) circle (2.4pt);
\\node[font=\\scriptsize,align=center,text width=3.3cm] at (2.0,-0.95) {""" +
        tl("about 13:00 of $d-2$: prices of $d-1$ published", "circa 13:00 în $d-2$: se publică prețurile zilei $d-1$") + """};
\\draw[MainBlue] (2.55,0) -- (2.3,-0.5);
\\draw[thick,Crimson,{Latex}-{Latex}] (9.6,-0.55) -- (14.2,-0.55)
  node[midway,below=3pt,font=\\scriptsize,align=center,text width=4.4cm] {""" + tl("24 hourly (96 quarter-hour) prices to forecast",
                                                                    "de prognozat: 24 de prețuri orare (96 pe sfert de oră)") + """};
\\end{tikzpicture}
\\end{center}
\\vspace{-1mm}
""" + it(t((t("\\textbf{Allowed} for the forecast of day $d$", "\\textbf{Permis} pentru prognoza zilei $d$"),
          t("prices up to $d-1$; realised load, wind, solar, hydro, nuclear and flows up to $d-2$; carbon at the $d-2$ close",
            "prețurile pînă în $d-1$; consumul, eolianul, solarul, hidro, nuclearul și fluxurile realizate pînă în $d-2$; carbonul la închiderea din $d-2$")),
         ("\\textbf{Ce folosesc modelele noastre}",
          "prețurile pînă în ziua $d-1$; consumul, producția și fluxurile realizate pînă în ziua $d-2$; prețul carbonului la închiderea din $d-2$")),
         t((t("\\textbf{Not in our data}", "\\textbf{Nu avem în date}"),
          t("the day-ahead load and renewable forecasts of the transmission system operator (TSO), which a real desk would use",
            "prognozele operatorului de transport și de sistem (TSO), folosite în practică de un birou de tranzacționare")),
          ("\\textbf{Ce nu avem în date}",
           "prognozele TSO de consum și de producție regenerabilă pentru ziua $d$"))) +
        D.bottom(t("a backtest that uses the realised load of $d-1$ looks excellent and cannot be run at 12:00.",
                   "o testare retrospectivă cu consumul realizat în ziua $d-1$ pare excelentă, dar la 12:00 acest consum nu se cunoaște."), NB + " \\S1"), "footnotesize", cite=t("(Assignment 1; OPCOM; Lago et al., 2021, APEN)",
                                                                           "(tema 1; OPCOM; Lago et al., 2021, APEN)"))

    D.chart(t("Calibration, burn-in, test: time runs one way, data are never shuffled",
              "Datele se împart cronologic în calibrare, rodaj și test, fără amestecare"), "split_timeline", [
        t("Models re-estimated every day on the window ending at $d-1$; no random K-fold, no random validation split.",
          "Calibrare = estimarea modelului, rodaj = prognoze folosite doar pentru intervale, test = măsurarea erorii; reestimare zilnică pe fereastra încheiată în $d-1$, fără K-fold aleator.")],
        height=t("0.52\\textheight", "0.50\\textheight"), job=t("ask any vendor for the rolling backtest, not an in-sample fit.",
                                         "cereți furnizorului o testare retrospectivă (backtest) pe fereastră glisantă, nu ajustarea pe datele de estimare."),
        tryit=NB + " \\S1", cite=CITE_W)

    D.figframe(t("Older information, larger error, except at the weekly lag", "Prețul mai vechi dă erori mai mari, cu excepția celui de acum o săptămînă"),
               None, None, "horizon_naive", [
                   t("Forecast $\\hat P_{d,h}=P_{d-k,h}$; MAE @{horizon.1|.2f} EUR/MWh for $k=1$, @{horizon.2|.2f} for $k=2$, back to @{horizon.7|.2f} for $k=7$ (same weekday).",
                     "Prognoza $\\hat P_{d,h}=P_{d-k,h}$ (prețul aceleiași ore de acum $k$ zile); "
                     "MAE @{horizon.1|.2f} EUR/MWh pentru $k=1$, @{horizon.2|.2f} pentru $k=2$, doar @{horizon.7|.2f} pentru $k=7$ (aceeași zi a săptămînii)")],
               job=t("the day-ahead horizon is 12 to 36 hours; the freshest price you hold at 12:00 is that of $d-1$.",
                     "prognoza de la 12:00 din ziua $d-1$ privește următoarele 12--36 de ore; cel mai recent preț cunoscut este cel al zilei $d-1$."),
               tryit=NB + " \\S2", height="0.62\\textheight", cite=t("(own computation, " + TEST + ")", "(calcule proprii, " + TEST + ")"))

    D.concept(t("Point, probabilistic and path forecasts answer different questions", "Prognozele punctuale, probabilistice și de traiectorie răspund la întrebări diferite"),
              t("A point forecast gives one number per hour, a probabilistic one its distribution, a path forecast joint scenarios for the 24 hours.",
                "Prognoza punctuală dă un preț pentru fiecare oră, cea probabilistică dă distribuția prețului, iar cea de traiectorie dă scenarii pentru toate cele 24 de ore."),
              "\\[ \\underbrace{\\hat P_{d,h}}_{\\text{" + t("point", "punctuală") + "}}\\quad"
              "\\underbrace{\\hat q^{\\tau}_{d,h}:\\ \\Pr(P_{d,h}\\le \\hat q^{\\tau}_{d,h})=\\tau}_{\\text{" + t("quantile", "cuantilă") + "}}"
              "\\quad \\underbrace{\\{\\hat P^{(s)}_{d,0},\\dots,\\hat P^{(s)}_{d,23}\\}_{s=1}^{S}}_{\\text{" + t("paths", "traiectorii") + "}} \\]" +
              "\\where{" + t("$d$ = delivery day; $h$ = hour (CET); $\\tau\\in(0,1)$ = quantile level; $s$ = scenario; $S$ = number of scenarios.",
                             "$d$ = ziua livrării; $h$ = ora (CET); $\\hat q^{\\tau}_{d,h}$ = cuantila de nivel $\\tau\\in(0,1)$; $s$ = scenariul; $S$ = numărul de scenarii.") + "}",
              it((t("\\textbf{On our data}", "\\textbf{Pe datele din România}"),
                  t("errors at 12 h and 13 h correlate at @{path.corr_12_13|.2f}", "corelația erorilor de prognoză între orele 12 și 13: @{path.corr_12_13|.2f}"),
                  t("errors at 3 h and 19 h correlate at only @{path.corr_03_19|.2f}", "între orele 3 și 19: doar @{path.corr_03_19|.2f}")),
                 (t("\\textbf{Who needs what}", "\\textbf{Cine folosește fiecare tip}"),
                  t("supplier buying a block, the point forecast", "furnizorul de energie care cumpără un bloc de ore: prognoza punctuală"),
                  t("risk manager, quantiles (Lecture 4)", "managerul de risc: cuantilele (cursul 4)"),
                  t("battery, paths, since it buys in one hour and sells in another", "operatorul unei baterii: traiectoriile, deoarece cumpără energie într-o oră și o vinde în alta")), sep="2pt"),
              t("decide which of the three your decision needs before you buy a forecast.",
                "înainte de a cumpăra o prognoză, stabiliți de care dintre cele trei tipuri are nevoie decizia dumneavoastră."),
              tryit=NB + " \\S7", cite="(Nowotarski \\& Weron, 2018, RSER)", wl="0.54", wr="0.43")

    # ------------------------------------------------------------------ 2 benchmarks and error measures
    D.subsection(t("Naive benchmarks and error measures", "Modele naive de referință și măsuri ale erorii"))
    D.concept(t("The naive benchmark: yesterday, or last week for Monday and the weekend",
                "Modelul naiv: prețul de ieri sau, lunea și în weekend, prețul de acum 7 zile"),
              t("Every model must beat the rule a trader would use without any model.",
                "Orice model trebuie să fie mai precis decît regula simplă pe care un trader ar aplica-o fără niciun model."),
              "\\[ \\hat P^{\\text{naive}}_{d,h}=\\begin{cases}P_{d-7,h}, & \\text{" + t("Mon, Sat, Sun", "lun., sîm., dum.") +
              "}\\\\ P_{d-1,h}, & \\text{" + t("Tue--Fri", "mar.--vin.") + "}\\end{cases} \\]\\vspace{-2mm}\\[ \\hat P^{(7)}_{d,h}=P_{d-7,h} \\]" +
              "\\where{" + t("$P_{d,h}$ = price of day $d$, hour $h$ (EUR/MWh); $\\hat P^{(7)}$ = seasonal naive (same hour last week).",
                             "$P_{d,h}$ = prețul zilei $d$, ora $h$ (EUR/MWh); $\\hat P^{(7)}$ = modelul naiv sezonier: aceeași oră, cu o săptămînă în urmă.") + "}",
              it((t("\\textbf{Why the switch}, MAE in EUR/MWh", "\\textbf{De ce se schimbă regula} (MAE, EUR/MWh)"),
                  t("Mon, Sat, Sun: $d-7$ @{naive_dow.monsatsun.lag7|.2f} vs $d-1$ @{naive_dow.monsatsun.lag1|.2f}",
                    "luni, sîmbătă, duminică: $d-7$ dă @{naive_dow.monsatsun.lag7|.2f}, $d-1$ dă @{naive_dow.monsatsun.lag1|.2f}"),
                  t("Tue--Fri: $d-1$ @{naive_dow.tuefri.lag1|.2f} vs $d-7$ @{naive_dow.tuefri.lag7|.2f}",
                    "marți--vineri: $d-1$ dă @{naive_dow.tuefri.lag1|.2f}, $d-7$ dă @{naive_dow.tuefri.lag7|.2f}"),
                  ),
                 (t("\\textbf{Test year}", "\\textbf{Anul de test}"),
                  t("naive @{acc.naive.mae|.2f}, seasonal naive @{acc.snaive.mae|.2f} EUR/MWh",
                    "MAE: modelul naiv @{acc.naive.mae|.2f}, naiv sezonier @{acc.snaive.mae|.2f} EUR/MWh"),
                  t("mean price @{test.mean|.2f} EUR/MWh, so the naive error is about one fifth of the price",
                    "prețul mediu este @{test.mean|.2f} EUR/MWh, deci eroarea naivă reprezintă circa o cincime din preț")), sep="2pt"),
              t("ask any forecast vendor for the rMAE against this naive rule on your hours.",
                "cereți oricărui furnizor de prognoze rMAE față de această regulă naivă, calculată pe orele care vă interesează."),
              tryit=NB + " \\S2", cite="(Nogales et al., 2002, IEEE TPWRS; Weron, 2014, IJF)", wl="0.52", wr="0.45")

    D.concept(t("Four error measures, one benchmark-relative score", "Patru măsuri ale erorii și rMAE, care compară modelul cu cel naiv"),
              t("Absolute errors are in EUR/MWh, squared errors punish spikes, rMAE compares with naive.",
                "Erorile absolute sînt în EUR/MWh, cele pătratice penalizează salturile, rMAE compară cu modelul naiv."),
              "\\[ \\text{MAE}=\\tfrac1N\\textstyle\\sum|e_{d,h}|,\\quad \\text{RMSE}=\\sqrt{\\tfrac1N\\textstyle\\sum e_{d,h}^2} \\]"
              "\\[ \\text{sMAPE}=\\tfrac1N\\textstyle\\sum\\frac{2|e_{d,h}|}{|P_{d,h}|+|\\hat P_{d,h}|},\\quad "
              "\\text{rMAE}=\\frac{\\text{MAE}_{\\text{model}}}{\\text{MAE}_{\\text{naive}}} \\]" +
              "\\where{" + t("$e_{d,h}=P_{d,h}-\\hat P_{d,h}$; $N$ = number of (day, hour) pairs; symmetric mean absolute percentage error (sMAPE), bounded by 200\\%; "
                             "a value of rMAE below 1 = better than naive.",
                             "$e_{d,h}=P_{d,h}-\\hat P_{d,h}$ = eroarea; $N$ = numărul perechilor (zi, oră); eroarea procentuală absolută medie simetrică (sMAPE) $\\in[0,200\\%]$; "
                             "valoare rMAE $<1$ = mai precis decît modelul naiv.") + "}",
              it((t("\\textbf{On our data}, " + TEST, "\\textbf{Pe datele din România}, " + TEST),
                  t("naive: MAE @{acc.naive.mae|.2f}, RMSE @{acc.naive.rmse|.2f}, sMAPE @{acc.naive.smape|.1f}\\%",
                    "modelul naiv: MAE @{acc.naive.mae|.2f}, RMSE @{acc.naive.rmse|.2f}, sMAPE @{acc.naive.smape|.1f}\\%"),
                  t("LEAR averaged across calibration windows (AW-LEAR): MAE @{acc.aw_lear.mae|.2f}, RMSE @{acc.aw_lear.rmse|.2f}, rMAE @{acc.aw_lear.rmae|.3f}",
                    "LEAR mediat pe ferestre de calibrare (AW-LEAR, secțiunea 3): MAE @{acc.aw_lear.mae|.2f}, RMSE @{acc.aw_lear.rmse|.2f}, rMAE @{acc.aw_lear.rmae|.3f}"),
                  t("best, " + MN["ens_all"] + ": rMAE @{acc.ens_all.rmae|.3f}, i.e.\\ @{gain.ens_all|.1f}\\% less error than naive",
                    "cel mai bun, " + MN["ens_all"] + ": rMAE @{acc.ens_all.rmae|.3f}, adică o eroare cu @{gain.ens_all|.1f}\\% mai mică decît a modelului naiv")),
                 t("MAE rewards the median forecast, RMSE the mean.", "MAE este minimă pentru prognoza mediană, RMSE pentru cea medie."), sep="2pt"),
              t("report MAE in EUR/MWh to the desk and rMAE to management, on the same hours.",
                "raportați biroului de tranzacționare MAE în EUR/MWh, iar conducerii rMAE, calculate pe aceleași ore."),
              tryit=NB + " \\S2", cite="(Hyndman \\& Koehler, 2006, IJF; Lago et al., 2021, APEN)", wl="0.49", wr="0.48")

    D.figframe(t("Why percentage errors fail near zero and negative prices",
                 "Erorile procentuale nu funcționează la prețuri apropiate de zero sau negative"),
               None, None, "mape_fail", [
                   t("Mean absolute percentage error (MAPE) $=\\tfrac1N\\sum|e_{d,h}|/|P_{d,h}|$; for AW-LEAR @{mape.aw_lear|,.1f}\\%, or @{mape.aw_lear_excl5|.1f}\\% without the @{mape.n_small} hours with $|P|<5$ EUR/MWh.",
                     "Eroarea procentuală absolută medie (MAPE) $=\\tfrac1N\\sum|e_{d,h}|/|P_{d,h}|$; AW-LEAR: @{mape.aw_lear|,.1f}\\%, dar doar @{mape.aw_lear_excl5|.1f}\\% fără cele @{mape.n_small} " + de("mape.n_small") + "ore cu $|P|<5$ EUR/MWh."),
                   t("These few hours produce @{mape.share_from_small|.1f}\\% of the MAPE.", "Aceste puține ore generează @{mape.share_from_small|.1f}\\% din valoarea MAPE.")],
               job=t("never accept a MAPE for power prices; ask for MAE and rMAE.",
                     "nu acceptați MAPE pentru prețurile energiei electrice; cereți MAE și rMAE."),
               tryit=NB + " \\S2", height=t("0.60\\textheight", "0.55\\textheight"), cite="(Hyndman \\& Koehler, 2006, IJF; Weron, 2014, IJF)")

    D.subsection(t("Testing forecast accuracy", "Testarea acurateței prognozelor"))
    D.concept(t("The Diebold--Mariano test: is the gain larger than luck?", "Testul Diebold--Mariano arată dacă un model este cu adevărat mai precis decît altul"),
              t("Compare the daily average error of two models; if the mean difference is large relative to its own noise, one model is really better.",
                "Comparăm, zi de zi, eroarea medie a două modele; dacă diferența medie este mare față de variabilitatea ei, avantajul unui model nu se datorează întîmplării."),
              "\\[ \\Delta_d=\\underbrace{\\tfrac1{24}\\textstyle\\sum_h|e^{A}_{d,h}|}_{\\text{" + t("model A", "modelul A") + "}}-"
              "\\underbrace{\\tfrac1{24}\\textstyle\\sum_h|e^{B}_{d,h}|}_{\\text{" + t("model B", "modelul B") + "}},\\qquad "
              "\\text{DM}=\\frac{\\bar\\Delta}{\\sqrt{\\hat\\sigma^2_{\\Delta}/n}} \\]" +
              "\\where{" + t("$n$ = test days; $\\hat\\sigma^2_{\\Delta}$ = Newey--West variance with 7 lags; $p=1-\\Phi(\\text{DM})$; "
                             "small $p$ = B more accurate than A.",
                             "$\\Delta_d$ = diferența de eroare din ziua $d$; $n$ = numărul zilelor de test; $\\hat\\sigma^2_{\\Delta}$ = varianța Newey--West cu 7 decalaje; "
                             "valoarea $p=1-\\Phi(\\text{DM})$ sub 0{,}05 = B este semnificativ mai precis decît A.") + "}",
              it((t("\\textbf{On our data}, @{dm.n_days} test days", "\\textbf{Pe datele din România}, @{dm.n_days} " + de("dm.n_days") + "zile de test"),
                  t("naive vs AW-LEAR: DM @{dm.naive_lear.stat|.2f}, $p$ " + pval("dm.naive_lear.p"),
                    "modelul naiv față de AW-LEAR: DM @{dm.naive_lear.stat|.2f}, $p$ " + pval("dm.naive_lear.p")),
                  t("ARX averaged across windows (AW-ARX) vs AW-LEAR: DM @{dm.arx_lear.stat|.2f}, $p$ = " + pval("dm.arx_lear.p") + ", no significant difference",
                    "ARX mediat pe ferestre (AW-ARX) față de AW-LEAR: DM @{dm.arx_lear.stat|.2f}, $p$ = " + pval("dm.arx_lear.p") + ", diferență nesemnificativă statistic"),
                  t("AW-LEAR vs " + MN["ens_all"] + ": DM @{dm.lear_ens.stat|.2f}, $p$ = " + pval("dm.lear_ens.p"),
                    "AW-LEAR față de " + MN["ens_all"] + ": DM @{dm.lear_ens.stat|.2f}, $p$ = " + pval("dm.lear_ens.p"))),
                 t("Daily averaging removes the correlation between the 24 hours of a day (multivariate version).",
                   "Media pe zi elimină corelația dintre cele 24 de ore ale aceleiași zile (varianta multivariată a testului)."), sep="2pt"),
              t("switch models only when the gain is significant on your hours.",
                "schimbați modelul numai dacă îmbunătățirea este semnificativă pe orele care vă interesează."),
              tryit=NB + " \\S2", cite="(Diebold \\& Mariano, 1995, JBES; Ziel \\& Weron, 2018, ENEECO)", wl="0.51", wr="0.46")

    D.chart(t("The DM chessboard: which model beats which on the Romanian test year", "Matricea testelor DM: care modele sînt semnificativ mai precise în România"),
            "dm_matrix", [
                t("@{dm.n_sig_vs_naive} of the @{dm.n_others} other models beat the naive benchmark at 5\\%; green cells mark a significant win of the column.",
                  "@{dm.n_sig_vs_naive} dintre celelalte @{dm.n_others} modele sînt semnificativ mai precise decît modelul naiv, la pragul de 5\\%; o celulă verde = modelul din coloană este semnificativ mai precis decît cel din rînd.")],
            height="0.62\\textheight",
            job=t("read a column top to bottom; many green cells mean a model worth paying for.",
                  "citiți fiecare coloană de sus în jos; multe celule verzi indică un model pentru care merită să plătiți."),
            tryit=NB + " \\S2", cite="(Ziel \\& Weron, 2018, ENEECO; Lago et al., 2021, APEN)")

    # ------------------------------------------------------------------ 3 expert ARX
    D.section(t("Expert models: ARX and LEAR", "Modele expert: ARX și LEAR"))
    D.subsection(t("The expert ARX model", "Modelul expert ARX"))
    D.concept(t("The expert ARX model: recent prices, calendar and fundamentals", "Modelul expert ARX: prețuri recente, calendar și variabile fundamentale"),
              t("One linear regression per hour, with the inputs a trader looks at first.",
                "O regresie liniară pentru fiecare oră, cu variabilele urmărite de un trader."),
              "\\[ \\begin{aligned} Y_{d,h}=\\beta_0&+\\underbrace{\\beta_1Y_{d-1,h}+\\beta_2Y_{d-2,h}+\\beta_3Y_{d-7,h}}_{\\text{" + t("autoregression", "autoregresie") + "}}\\\\"
              "&+\\underbrace{\\beta_4Y_{d-1,23}+\\beta_5Y^{\\min}_{d-1}+\\beta_6Y^{\\max}_{d-1}}_{\\text{" + t("yesterday's shape", "forma zilei precedente") + "}}\\\\"
              "&+\\underbrace{\\beta_7\\tilde L_{d,h}+\\beta_8\\tilde R_{d,h}}_{\\text{" + t("fundamentals of } d-2", "fundamentale din } d-2") + "}"
              "+\\underbrace{\\textstyle\\sum_{j}\\delta_jD^{j}_d}_{\\text{" + t("Mon, Sat, Sun", "lun., sîm., dum.") + "}}+\\varepsilon_{d,h} \\end{aligned} \\]" +
              "\\where{" + t("$Y$ = asinh-transformed price; $\\tilde L_{d,h}=L_{d-2,h}$ load, $\\tilde R_{d,h}$ wind + solar of $d-2$, z-scored.",
                             "$Y$ = prețul transformat asinh; $\\tilde L_{d,h}=L_{d-2,h}$ = consumul, $\\tilde R_{d,h}$ = producția eoliană și solară din $d-2$, standardizate.") + "}",
              it((t("\\textbf{Estimation}", "\\textbf{Estimare}"),
                  t("ordinary least squares (OLS), separately for each $h$", "metoda celor mai mici pătrate (OLS), separat pentru fiecare $h$"),
                  t("12 regressors per hour, as in Assignment 1", "12 regresori pentru fiecare oră, ca în tema 1")),
                 (t("\\textbf{On our data}, ARX(728)", "\\textbf{Pe datele din România}, ARX(728)"),
                  t("728-day window, re-estimated daily", "reestimat zilnic pe ultimele 728 de zile"),
                  t("MAE @{acc.arx728.mae|.2f} EUR/MWh, rMAE @{acc.arx728.rmae|.3f}", "MAE @{acc.arx728.mae|.2f} EUR/MWh, rMAE @{acc.arx728.rmae|.3f}")), sep="2pt"),
              t("this is the model to beat before anyone sells you a neural network.",
                "acesta este modelul de depășit înainte să cumpărați o rețea neuronală."),
              tryit=NB + " \\S3", cite="(Ziel \\& Weron, 2018, ENEECO; Weron, 2014, IJF)", wl="0.55", wr="0.42")

    D.chart(t("The ARX coefficients change with the hour of the day", "Coeficienții modelului ARX diferă de la o oră la alta"), "arx_coef", [
        t("$Y_{d-1,h}$ weighs most at hour @{arxcoef.Y1.argmax} (@{arxcoef.Y1.max|.2f}) and least at hour @{arxcoef.Y1.argmin} (@{arxcoef.Y1.min|.2f}); "
          "night hours lean on the last hour of $d-1$ instead (up to @{arxcoef.Y1_23.max|.2f}).",
          "$Y_{d-1,h}$ (aceeași oră, ieri) are coeficientul maxim la ora @{arxcoef.Y1.argmax} (@{arxcoef.Y1.max|.2f}) și minim la ora @{arxcoef.Y1.argmin} "
          "(@{arxcoef.Y1.min|.2f}); noaptea contează mai mult ultima oră a zilei $d-1$ (pînă la @{arxcoef.Y1_23.max|.2f})."),
        t("The load and wind + solar coefficients stay close to zero: at $d-2$ they add little to yesterday's price.",
          "Consumul și producția eoliană și solară au coeficienți apropiați de zero: datele din $d-2$ adaugă puțin.")],
        height=t("0.55\\textheight", "0.50\\textheight"), job=t("one model per hour lets the evening peak learn from different drivers than the night.",
                                         "cîte un model pe oră permite ca vîrful de seară să depindă de alți factori decît noaptea."),
        tryit=NB + " \\S3", cite=t("(own estimation, ARX(728))", "(estimare proprie, ARX(728))"))

    def r3(k, lab):
        return [lab, f"@{{acc.{k}.mae|.2f}}", f"@{{acc.{k}.rmse|.2f}}", f"@{{acc.{k}.rmae|.3f}}"]
    D.frame(t("Fundamentals lagged by two days add almost nothing", "Variabilele fundamentale din ziua $d-2$ aproape că nu îmbunătățesc prognoza"), cols(
        table("@{}p{0.52\\linewidth}rrr@{}", [t("ARX(728), test year", "ARX(728), anul de test"), "MAE", "RMSE", "rMAE"], [
            r3("arx728_noexog", t("prices and calendar only", "numai prețuri și calendar")),
            r3("arx728", t("+ load, wind + solar of $d-2$", "+ consum, producție eoliană și solară din $d-2$")),
            r3("arx728_fund", t("+ hydro, nuclear, net imports, EUA of $d-2$", "+ hidro, nuclear, import net, EUA din $d-2$"))],
            size="footnotesize", stretch="1.25") + note(
            t("Fundamentals missing on a day are carried forward from the past only (nuclear on @{data.fund_ffill.nuclear} days).",
              "Valorile lipsă ale variabilelor fundamentale se înlocuiesc cu ultima valoare observată (pentru nuclear, în @{data.fund_ffill.nuclear} " + de("data.fund_ffill.nuclear") + "zile)."),
            t("EUA = SparkChange ETC close of $d-2$, a proxy of the allowance price.",
              "EUA = prețul de închidere al titlului SparkChange din ziua $d-2$, folosit ca aproximare a prețului certificatului de emisii.")),
        it((t("\\textbf{Why so little}", "\\textbf{De ce atît de puțin}"),
            t("what happened on $d-2$ is already in the price of $d-1$", "informația din ziua $d-2$ este deja inclusă în prețul zilei $d-1$"),
            t("the outages of the Cernavodă nuclear power plant reach the model two days late", "de exemplu, opririle centralei nucleare de la Cernavodă intră în model cu două zile întîrziere")),
           (t("\\textbf{What would help}", "\\textbf{Ce ar ajuta}"),
            t("published day-ahead forecasts of load, wind and solar for day $d$ (ENTSO-E, Transelectrica)",
              "prognozele de consum și de producție eoliană și solară pentru ziua $d$ (ENTSO-E, Transelectrica)"),
            t("they are legal at 12:00 on $d-1$, but not in our free data", "sînt publicate înainte de 12:00 în ziua $d-1$, deci pot fi folosite, dar nu fac parte din datele noastre gratuite")),
           sep="3pt"), "0.50", "0.47") +
        D.bottom(t("buy the TSO's day-ahead load and renewable forecasts before buying a more complex model.",
                   "cumpărați prognozele TSO de consum și de producție regenerabilă pentru ziua următoare înainte de a plăti pentru un model mai complex."), NB + " \\S3"),
        "footnotesize", cite=t("(own estimation; Lago et al., 2021, APEN)", "(estimare proprie; Lago et al., 2021, APEN)"))

    D.chart(t("One model per hour beats one model for all hours", "Cîte un model pentru fiecare oră este mai precis decît un model comun"),
            "per_hour_single", [
                t("MAE @{acc.arx728.mae|.2f} per hour vs @{acc.arx728_single.mae|.2f} EUR/MWh pooled (hour intercepts, common slopes); pooled worse in @{byhour.single_worse_h} of 24 hours.",
                  "MAE: @{acc.arx728.mae|.2f} cu cîte un model pe oră, @{acc.arx728_single.mae|.2f} EUR/MWh cu un model comun (constantă proprie fiecărei ore, pante comune); modelul comun este mai slab în @{byhour.single_worse_h} din 24 de ore.")],
            height="0.50\\textheight", job=t("since 1 Oct 2025 the same choice arises for the 96 quarter-hours.",
                                             "din 1 octombrie 2025 se tranzacționează sferturi de oră, deci aceeași alegere apare pentru cele 96 de intervale ale zilei."),
            tryit=NB + " \\S3", cite="(Ziel \\& Weron, 2018, ENEECO)")

    D.subsection(t("Variance-stabilising transformations", "Transformări de stabilizare a varianței"))
    D.figframe(t("The asinh transformation tames spikes and negative prices",
                 "Transformarea asinh atenuează salturile și acceptă prețuri negative"),
               None, None, "vst", [
                   t("Variance-stabilising transformation (VST) $Y=\\asinh((P-m)/s)$, $m$ = median, $s$ = 1.4826 $\\times$ median absolute deviation (MAD), from the window only.",
                     "Transformarea de stabilizare a varianței (VST): $Y=\\asinh((P-m)/s)$; $m$ = mediana, $s$ = 1{,}4826 $\\times$ abaterea absolută mediană (MAD), ambele din fereastra de calibrare."),
                   t("ARX(728) MAE @{acc.arx728_raw.mae|.2f} raw vs @{acc.arx728.mae|.2f} with asinh; RMSE goes the other way (@{acc.arx728_raw.rmse|.2f} vs @{acc.arx728.rmse|.2f}).",
                     "MAE pentru ARX(728): @{acc.arx728_raw.mae|.2f} pe prețuri netransformate, @{acc.arx728.mae|.2f} cu asinh; pentru RMSE ordinea se inversează (@{acc.arx728_raw.rmse|.2f} față de @{acc.arx728.rmse|.2f}).")],
               job=t("asinh works below zero, where the logarithm cannot be used.",
                     "funcția asinh este definită și pentru valori negative, unde logaritmul nu poate fi folosit."),
               tryit=NB + " \\S3", height="0.56\\textheight", cite="(Uniejewski, Weron \\& Ziel, 2018, IEEE TPWRS)")

    # ------------------------------------------------------------------ 4 LEAR
    D.subsection(t("LASSO-estimated autoregression", "Autoregresia estimată cu LASSO"))
    D.concept(t("LEAR: give the model 247 candidates and let the LASSO switch most of them off",
                "LEAR pornește de la 247 de regresori, iar LASSO îi elimină pe cei mai mulți"),
              t("A penalty on the size of the coefficients sets the useless ones exactly to zero, so the data choose the regressors.",
                "O penalizare a mărimii coeficienților îi face zero pe cei inutili, deci datele aleg regresorii."),
              "\\[ \\hat{\\bm\\beta}_h=\\arg\\min_{\\bm\\beta}\\Big\\{\\underbrace{\\textstyle\\sum_{d\\in\\text{cal}}(Y_{d,h}-\\mathbf x_d^{\\top}\\bm\\beta)^2}_{\\text{" +
              t("fit", "ajustare") + "}}+\\underbrace{\\lambda_h\\textstyle\\sum_j|\\beta_j|}_{\\text{" + t("penalty", "penalizare") + "}}\\Big\\} \\]" +
              "\\where{" + t("$\\mathbf x_d$ = 247 regressors, all 24 prices of $d-1,d-2,d-3,d-7$ (96), load and wind + solar of $d-2,d-3,d-7$ (144), 7 weekday dummies; "
                             "$\\lambda_h$ chosen every day by the Akaike information criterion (AIC) inside the window.",
                             "$\\mathbf x_d$ = 247 de regresori: cele 24 de prețuri din $d-1,d-2,d-3,d-7$ (96), consumul și producția eoliană și solară din $d-2,d-3,d-7$ (144), "
                             "7 indicatori ai zilei; $\\lambda_h$ = intensitatea penalizării, aleasă zilnic prin criteriul informațional Akaike (AIC).") + "}",
              it((t("\\textbf{On our data}, LEAR(728)", "\\textbf{Pe datele din România}, LEAR(728)"),
                  t("on average @{lear.nnz_mean|.0f} of 247 regressors kept (@{lear.nnz_share|.0f}\\%), from @{lear.nnz_min} to @{lear.nnz_max}",
                    "rămîn în medie @{lear.nnz_mean|.0f} din 247 (@{lear.nnz_share|.0f}\\%), între @{lear.nnz_min} și @{lear.nnz_max}"),
                  t("MAE @{acc.lear728.mae|.2f}; averaged over 364, 546, 728 days (AW-LEAR) @{acc.aw_lear.mae|.2f} EUR/MWh",
                    "MAE @{acc.lear728.mae|.2f}; media prognozelor estimate pe 364, 546 și 728 de zile (AW-LEAR): @{acc.aw_lear.mae|.2f} EUR/MWh")),
                 (t("\\textbf{Choosing $\\lambda$ honestly}", "\\textbf{Cum se alege corect $\\lambda$}"),
                  t("by an information criterion, or on a validation block that ends before the forecast day",
                    "printr-un criteriu informațional sau pe un bloc de validare care se încheie înaintea zilei prognozate"),
                  t("never on the test year", "niciodată pe anul de test")), sep="2pt"),
              t("a LASSO model explains itself, since the kept regressors show what drives each hour.",
                "un model LASSO este ușor de interpretat: regresorii păstrați arată ce influențează prețul în fiecare oră."),
              tryit=NB + " \\S4", cite="(Tibshirani, 1996; Uniejewski, Nowotarski \\& Weron, 2016; Lago et al., 2021)",
              wl="0.53", wr="0.44")

    D.chart(t("What LEAR keeps: yesterday's same hour and the weekday, rarely the lagged fundamentals",
              "LEAR păstrează prețul aceleiași ore de ieri și ziua săptămînii"), "lear_sel", [
        t("Kept on average, $P_{d-1,h}$ @{lear.p1_same|.0f}\\%, weekday @{lear.dow|.0f}\\%, load @{lear.load|.0f}\\%, wind + solar @{lear.res|.0f}\\% of the regressors.",
          "Procentul mediu al regresorilor păstrați din fiecare grupă: $P_{d-1,h}$ (aceeași oră, ieri) @{lear.p1_same|.0f}\\%, ziua săptămînii @{lear.dow|.0f}\\%, consum @{lear.load|.0f}\\%, producție eoliană și solară @{lear.res|.0f}\\%.")],
        height="0.58\\textheight", job=t("real gains need forecasts of the fundamentals for day $d$.",
                                         "pentru cîștiguri reale aveți nevoie de prognoze ale variabilelor fundamentale pentru ziua $d$."),
        tryit=NB + " \\S4", cite=t("(own estimation, LEAR(728), " + TEST + ")", "(estimare proprie, LEAR(728), " + TEST + ")"))

    # ------------------------------------------------------------------ 5 windows and combinations
    D.section(t("Windows, combinations and machine learning", "Ferestre, combinații și învățare automată"))
    D.subsection(t("Calibration windows", "Ferestre de calibrare"))
    D.concept(t("Short windows adapt, long windows are stable: average them", "Ferestrele scurte se adaptează, cele lungi sînt stabile: mediați prognozele"),
              t("Instead of guessing the best window length, estimate the model on several windows and average the forecasts.",
                "În loc să ghiciți lungimea optimă a ferestrei de calibrare, estimați modelul pe mai multe ferestre și faceți media prognozelor."),
              "\\[ \\hat P^{\\text{AW}}_{d,h}=\\frac1{|\\mathcal T|}\\sum_{T\\in\\mathcal T}\\underbrace{\\hat P^{(T)}_{d,h}}_{\\text{" +
              t("window of } T \\text{ days", "fereastră de } T \\text{ zile") + "}} \\]" +
              "\\where{" + t("rolling window = last $T$ days, re-estimated daily; ARX: $\\mathcal T=\\{56,84,112,714,721,728\\}$; LEAR: $\\mathcal T=\\{364,546,728\\}$; "
                             "averaging across calibration windows (AW).",
                             "$\\hat P^{(T)}_{d,h}$ = prognoza estimată pe ultimele $T$ zile (fereastră glisantă); ARX: $\\mathcal T=\\{56,84,112,714,721,728\\}$; LEAR: $\\mathcal T=\\{364,546,728\\}$; "
                             "medierea pe ferestre de calibrare (AW).") + "}",
              it((t("\\textbf{On our data}, MAE in EUR/MWh", "\\textbf{Pe datele din România}, MAE în EUR/MWh"),
                  t("ARX(56) @{acc.arx56.mae|.2f}, ARX(112) @{acc.arx112.mae|.2f}, ARX(728) @{acc.arx728.mae|.2f}",
                    "ARX(56) @{acc.arx56.mae|.2f}, ARX(112) @{acc.arx112.mae|.2f}, ARX(728) @{acc.arx728.mae|.2f}"),
                  t("AW-ARX @{acc.aw_arx.mae|.2f}, better than every single window", "AW-ARX @{acc.aw_arx.mae|.2f}, mai precis decît modelul estimat pe oricare fereastră"),
                  t("LEAR(364) @{acc.lear364.mae|.2f}, LEAR(728) @{acc.lear728.mae|.2f}, AW-LEAR @{acc.aw_lear.mae|.2f}",
                    "LEAR(364) @{acc.lear364.mae|.2f}, LEAR(728) @{acc.lear728.mae|.2f}, AW-LEAR @{acc.aw_lear.mae|.2f}")),
                 t("Mixing short (56--112) and long (714--728) windows gives both adaptation and stability.",
                   "Combinarea ferestrelor scurte (56--112 zile) cu cele lungi (714--728 de zile) aduce atît adaptare, cît și stabilitate."), sep="2pt"),
              t("when the market changes regime (2022, 2024), short windows react first; keep them in the average.",
                "cînd piața își schimbă regimul (2022, 2024), ferestrele scurte reacționează primele; păstrați-le în medie."),
              tryit=NB + " \\S5", cite="(Hubicka, Marcjasz \\& Weron, 2019; Marcjasz, Serafin \\& Weron, 2018)", wl="0.52", wr="0.45")

    D.chart(t("Averaging across windows beats the best single window", "Media pe ferestre este mai precisă decît cea mai bună fereastră"), "windows", [
        t("AW-ARX @{acc.aw_arx.mae|.2f} vs the best single window ARX(714) @{acc.arx714.mae|.2f}; dotted line = naive @{acc.naive.mae|.2f} EUR/MWh.",
          "MAE: AW-ARX @{acc.aw_arx.mae|.2f}, față de @{acc.arx714.mae|.2f} pentru cea mai bună fereastră, ARX(714); linia punctată = modelul naiv, @{acc.naive.mae|.2f} EUR/MWh.")],
        height="0.55\\textheight", job=t("you do not need to know the right window in advance; average a short and a long one.",
                                         "nu trebuie să știți dinainte care fereastră este potrivită; faceți media prognozelor obținute pe o fereastră scurtă și pe una lungă."),
        tryit=NB + " \\S5", cite="(Hubicka, Marcjasz \\& Weron, 2019, IEEE TSTE)")

    D.subsection(t("Combining forecasts", "Combinarea prognozelor"))
    D.concept(t("Combining different models: errors that do not coincide cancel out", "Combinarea modelelor: erorile care nu coincid se compensează"),
              t("If two models are wrong on different days, their simple average is wrong less often than either.",
                "Dacă două modele greșesc în zile diferite, media simplă a prognozelor lor greșește mai rar decît fiecare dintre ele."),
              "\\[ \\hat P^{\\text{ens}}_{d,h}=\\frac1K\\sum_{k=1}^{K}\\hat P^{(k)}_{d,h},\\quad "
              "\\Var(\\bar e)=\\frac{\\bar\\sigma^2}{K}\\big(1+(K-1)\\bar\\rho\\big) \\]" +
              "\\where{" + t("$K$ = number of models; $\\bar\\sigma^2$ = average error variance; $\\bar\\rho$ = average correlation of the errors; "
                             "the lower $\\bar\\rho$, the larger the gain; equal weights need no estimation.",
                             "$K$ = numărul de modele; $\\bar\\sigma^2$ = varianța medie a erorilor; $\\bar\\rho$ = corelația medie a erorilor; "
                             "cu cît $\\bar\\rho$ e mai mic, cu atît cîștigul e mai mare; ponderile egale nu se estimează.") + "}",
              it((t("\\textbf{On our data}, " + MN["ens_all"], "\\textbf{Pe datele din România}, " + MN["ens_all"]),
                  t("AW-ARX, AW-LEAR, a gradient boosting machine (GBM) and a multilayer perceptron (MLP), equal weights",
                    "AW-ARX, AW-LEAR, un model gradient boosting (GBM) și un perceptron multistrat (MLP), ponderi egale"),
                  t("MAE @{acc.ens_all.mae|.2f} EUR/MWh, rMAE @{acc.ens_all.rmae|.3f}, the best of all models",
                    "MAE @{acc.ens_all.mae|.2f} EUR/MWh, rMAE @{acc.ens_all.rmae|.3f}, cel mai bun dintre toate modelele"),
                  t("better than AW-LEAR in @{bymonth.n_months_ens_beats_lear} of 12 months and in @{byhour.ens_beats_lear_h} of 24 hours",
                    "mai bun decît AW-LEAR în @{bymonth.n_months_ens_beats_lear} din 12 luni și în @{byhour.ens_beats_lear_h} din 24 de ore"),
                  t("DM test against AW-LEAR: $p$ = " + pval("dm.lear_ens.p"), "testul DM față de AW-LEAR: $p$ = " + pval("dm.lear_ens.p"))),
                 t("The two weaker members (GBM, MLP) still help, because their errors differ.",
                   "Cei doi membri mai slabi (GBM, MLP) ajută totuși, deoarece erorile lor diferă."), sep="2pt"),
              t("ask vendors for forecasts you can average with yours, not for a single best model.",
                "cereți furnizorilor de prognoze serii pe care să le puteți combina cu ale dumneavoastră, nu un singur model „cel mai bun”."),
              tryit=NB + " \\S5", cite="(Bates \\& Granger, 1969; Nowotarski \\& Weron, 2015)", wl="0.48", wr="0.49")

    RES = [("naive", t("Naive", "Naiv")), ("snaive", t("Seasonal naive", "Naiv sezonier")), ("arx56", "ARX(56)"), ("arx728", "ARX(728)"),
           ("aw_arx", "AW-ARX"), ("arx728_single", t("ARX(728), one model", "ARX(728), model comun")),
           ("arx728_raw", t("ARX(728), no VST", "ARX(728), fără VST")), ("lear364", "LEAR(364)"), ("lear728", "LEAR(728)"),
           ("aw_lear", "AW-LEAR"), ("gbm", "GBM"), ("mlp", "MLP"), ("ens_lm", t("Ensemble LEAR+MLP", "Ansamblu LEAR+MLP")),
           ("ens_all", t("Ensemble of 4", "Ansamblu de 4 modele"))]
    vals = {c: [N["acc"][k][c] for k, _ in RES] for c in ["mae", "rmse", "smape", "rmae"]}
    rows = []
    for k, lab in RES:
        rows.append([lab] + [heat(N["acc"][k][c], min(vals[c]), max(vals[c]), True, fmt(N["acc"][k][c], f, lang))
                             for c, f in [("mae", ".2f"), ("rmse", ".2f"), ("smape", ".1f"), ("rmae", ".3f")]])
    D.frame(t("Results on the Romanian test year: the scoreboard", "Clasamentul modelelor pe anul de test în România"),
            "\\begin{center}" + table("@{}lrrrr@{}", [t("Model", "Model"), "MAE", "RMSE", "sMAPE, \\%", "rMAE"], rows,
                                      size="scriptsize", stretch="1.02") + "\\end{center}\\vspace{-2mm}" + note(
                t(TEST[0].upper() + TEST[1:] + ", @{test.n_hours|,d} hours; green = better, red = worse, per column.",
                  TEST[0].upper() + TEST[1:] + ", @{test.n_hours|,d} " + de("test.n_hours") + "ore; verde = mai precis, roșu = mai puțin precis, separat pe fiecare coloană."),
                t("Without the @{design.n_dst_test} DST days the MAE of AW-LEAR is @{acc.aw_lear.mae_nodst|.2f}; the ranking does not change.",
                  "Fără cele @{design.n_dst_test} zile cu schimbarea orei, MAE pentru AW-LEAR este @{acc.aw_lear.mae_nodst|.2f}; clasamentul nu se schimbă.")) +
            D.bottom(None, NB + " \\S5"), "small", cite=CITE_W)

    # ------------------------------------------------------------------ 6 machine learning
    D.subsection(t("Machine learning: a preview of Lecture 7", "Învățarea automată: introducere la cursul 7"))
    D.concept(t("Gradient boosting: many small trees, each correcting the previous ones",
                "Gradient boosting: mulți arbori mici, fiecare corectîndu-i pe cei anteriori"),
              t("Trees capture thresholds and interactions (e.g.\\ low wind and high load in the evening) that a linear model misses.",
                "Arborii surprind praguri și interacțiuni (de exemplu, vînt slab și consum mare seara), pe care un model liniar nu le vede."),
              "\\[ F_m(\\mathbf x)=F_{m-1}(\\mathbf x)+\\nu\\,f_m(\\mathbf x) \\]\\vspace{-2mm}\\[ f_m=\\arg\\min_f\\textstyle\\sum_i\\big(r_i^{(m)}-f(\\mathbf x_i)\\big)^2 \\]" +
              "\\where{" + t("$f_m$ = small regression tree; $r_i^{(m)}=Y_i-F_{m-1}(\\mathbf x_i)$ = current residual; $\\nu=0.05$ = learning rate; 500 trees fixed in advance.",
                             "$f_m$ = un arbore de regresie mic; $r_i^{(m)}=Y_i-F_{m-1}(\\mathbf x_i)$ = reziduul curent; $\\nu=0{,}05$ = rata de învățare; 500 de arbori.") + "}",
              it((t("\\textbf{Our gradient boosting machine (GBM)}", "\\textbf{Modelul nostru de gradient boosting (GBM)}"),
                  t("one model for all hours, with the hour as a feature; 20 features, all available at 12:00 on $d-1$",
                    "un singur model pentru toate orele, ora fiind o variabilă; 20 de variabile, toate cunoscute la 12:00 în ziua $d-1$"),
                  t("refitted at the start of each of the @{ml.n_refits} test months on all days before it (expanding window)",
                    "reestimat la începutul fiecărei luni de test (@{ml.n_refits} reestimări), pe toate zilele anterioare")),
                 (t("\\textbf{Result}", "\\textbf{Rezultat}"),
                  t("MAE @{acc.gbm.mae|.2f}, rMAE @{acc.gbm.rmae|.3f}; behind AW-LEAR over the year", "MAE @{acc.gbm.mae|.2f}, rMAE @{acc.gbm.rmae|.3f}; pe ansamblul anului, mai puțin precis decît AW-LEAR"),
                  t("but the best single model in the stress week (MAE @{weeks.stress_mae.gbm|.2f})", "dar cel mai bun model individual în săptămîna de criză (MAE @{weeks.stress_mae.gbm|.2f})")), sep="2pt"),
              t("trees are worth adding to an ensemble even when they do not win alone.",
                "arborii merită incluși într-un ansamblu, chiar dacă nu sînt cei mai buni luați separat."),
              tryit=NB + " \\S6", cite="(Friedman, 2001, Ann.\\ Stat.; Lago et al., 2021, APEN)", wl="0.50", wr="0.47")

    D.concept(t("Neural networks: 24 prices out of one input vector", "Rețele neuronale: 24 de prețuri dintr-un singur vector de intrare"),
              t("A multi-output network forecasts the whole day at once, like the deep neural network (DNN) of Lago et al.",
                "O rețea cu 24 de ieșiri prognozează toată ziua deodată, ca rețeaua neuronală profundă (DNN) din Lago et al."),
              "\\[ \\hat{\\mathbf Y}_d=W_3\\,\\phi\\big(W_2\\,\\phi(W_1\\mathbf x_d+b_1)+b_2\\big)+b_3\\in\\mathbb R^{24} \\]" +
              "\\where{" + t("$\\mathbf x_d$ = the 247 LEAR regressors + 4 fundamentals of $d-2$; $\\phi$ = rectified linear unit (ReLU); layers of 128 and 64 neurons; "
                             "multilayer perceptron (MLP).",
                             "$\\mathbf x_d$ = cei 247 de regresori LEAR și 4 variabile fundamentale din $d-2$; $\\phi$ = unitatea liniară rectificată (ReLU); straturi ascunse de 128 și 64 de neuroni; "
                             "perceptron multistrat (MLP).") + "}",
              it((t("\\textbf{Time-series discipline}", "\\textbf{Disciplina seriilor de timp}"),
                  t("epochs chosen on the last 15\\% of the training days, in time order (median @{ml.mlp_epochs_med})",
                    "numărul de epoci, ales pe ultimele 15\\% din zile (mediana: @{ml.mlp_epochs_med})"),
                  t("4 seeds averaged; refitted monthly, scaling fitted on training days only",
                    "media a 4 inițializări; reestimare lunară; standardizare pe zilele de antrenare")),
                 (t("\\textbf{Result}", "\\textbf{Rezultat}"),
                  t("MAE @{acc.mlp.mae|.2f}, rMAE @{acc.mlp.rmae|.3f}; a small untuned network does not beat LEAR",
                    "MAE @{acc.mlp.mae|.2f}, rMAE @{acc.mlp.rmae|.3f}; o rețea mică, neoptimizată, nu depășește LEAR"),
                  t("the tuned DNN of Lago et al.\\ (2021) does better (Lecture 7)", "rețeaua DNN optimizată de Lago et al.\\ (2021) obține rezultate mai bune (cursul 7)")), sep="2pt"),
              t("a neural network needs years of data and careful tuning, or you keep LEAR.",
                "o rețea neuronală cere ani de date și o calibrare atentă; altfel, păstrați LEAR."),
              tryit=NB + " \\S6", cite="(Lago, Marcjasz, De Schutter \\& Weron, 2021, APEN)", wl="0.50", wr="0.47")

    D.chart(t("Hour by hour: machine learning helps inside the ensemble, not alone", "Pe ore, învățarea automată ajută în cadrul ansamblului, nu luată separat"), "ml_hour", [
        t("Better than AW-LEAR in @{byhour.gbm_beats_lear_h} hours (GBM), @{byhour.mlp_beats_lear_h} (MLP) and @{byhour.ens_beats_lear_h} of 24 (" + MN["ens_all"] + ").",
          "GBM este mai precis decît AW-LEAR în @{byhour.gbm_beats_lear_h} ore, MLP în @{byhour.mlp_beats_lear_h}, iar " + MN["ens_all"] + " în @{byhour.ens_beats_lear_h} din 24 de ore."),
        t("The hardest hour is @{byhour.lear_worst_h} h CET, the evening ramp (AW-LEAR MAE @{byhour.lear_worst|.2f} EUR/MWh).",
          "Ora cea mai dificilă este @{byhour.lear_worst_h} CET, cînd prețul urcă abrupt seara (MAE AW-LEAR @{byhour.lear_worst|.2f} EUR/MWh).")],
        height="0.50\\textheight", job=t("put your best analyst on the evening hours, where the money is lost.",
                                         "alocați cel mai bun analist orelor de seară, unde se pierd cei mai mulți bani."),
        tryit=NB + " \\S6", cite=t("(own computation, " + TEST + ")", "(calcule proprii, " + TEST + ")"))

    c2 = N["c2"]
    D.frame(t("Our group on Romanian load: machine learning wins when the series is smooth",
              "Studiul de caz C2: pentru consumul din România, învățarea automată dă cele mai mici erori"), it(
        t((t("\\textbf{The study} (Proșcanu, Proșcanu, Pele \\& Costea, 2025)", "\\textbf{Studiul} (Proșcanu, Proșcanu, Pele \\& Costea, 2025)"),
         t("hourly national load of Romania, 2022--2024; classical seasonal models against neural networks",
           "consumul național orar al României, 2022--2024; modele sezoniere clasice comparate cu rețele neuronale")),
          ("\\textbf{Ce a făcut lucrarea} (Proșcanu, Proșcanu, Pele \\& Costea, 2025)",
           "date și metode: consumul național orar al României, 2022--2024; modele sezoniere clasice comparate cu rețele neuronale",
           "rezultat: o rețea neuronală are o eroare net mai mică decît modelul autoregresiv sezonier")),
        (t("\\textbf{Our replication} (studiu de caz C2, same gate-closure rule)", "\\textbf{Replicarea noastră} (studiul de caz C2, cu aceeași regulă: date pînă la 12:00 în ziua $d-1$)"),
         t("@{c2.nDays} test days from @{c2.testStartISO|date}; load metered up to $d-2$",
           "@{c2.nDays} " + de("c2.nDays") + "zile de test, începînd cu @{c2.testStartISO|date}; consumul măsurat pînă în ziua $d-2$"),
         t("MAPE: gradient boosting @{c2.gbmMAPE|.2f}\\%, Chronos-Bolt foundation model @{c2.chronosMAPE|.2f}\\%, MLP @{c2.mlpMAPE|.2f}\\%",
           "MAPE: gradient boosting @{c2.gbmMAPE|.2f}\\%, modelul fundațional Chronos-Bolt @{c2.chronosMAPE|.2f}\\%, MLP @{c2.mlpMAPE|.2f}\\%"),
         t("linear regression @{c2.linMAPE|.2f}\\%, seasonal autoregressive model @{c2.sarimaMAPE|.2f}\\%, naive two days earlier @{c2.naiveMAPE|.2f}\\%",
           "regresie liniară @{c2.linMAPE|.2f}\\%, model autoregresiv sezonier @{c2.sarimaMAPE|.2f}\\%, modelul naiv (consumul de acum două zile) @{c2.naiveMAPE|.2f}\\%")),
        (t("\\textbf{Why the contrast with prices}", "\\textbf{De ce rezultatul diferă de cel pentru prețuri}"),
         t("load is smooth and never near zero, so MAPE is meaningful and nonlinear models have patterns to learn",
           "consumul variază lin și nu se apropie de zero: MAPE are sens, iar modelele neliniare găsesc regularități"),
         t("prices jump and turn negative; there, a well-built linear model is hard to beat", "prețurile au salturi și devin negative: aici, un model liniar bine construit este greu de depășit")),
        sep="3pt") + note(t("C2 figures are computed by the C2 case notebook on our data; the paper's own results are in the case brief.",
                            "Cifrele C2 sînt calculate cu notebook-ul Jupyter al studiului de caz C2, pe datele noastre; rezultatele lucrării sînt prezentate în fișa studiului de caz.")) +
        D.bottom(t("forecast your own load with ML and the price with LEAR plus an ensemble.",
                   "prognozați consumul propriu cu modele ML, iar prețul cu LEAR și un ansamblu de modele.")),
        "footnotesize", cite="(Proșcanu, Proșcanu, Pele \\& Costea, 2025, RJEF; " + t("case study C2", "studiul de caz C2") + ")")

    # ------------------------------------------------------------------ 7 probabilistic
    D.section(t("Probabilistic forecasts and cointegration", "Prognoze probabilistice și cointegrare"))
    D.subsection(t("Quantile regression averaging", "Medierea prin regresie cuantilică"))
    D.concept(t("Quantile regression averaging: from point forecasts to quantiles", "Medierea prin regresie cuantilică: de la prognoze punctuale la cuantile"),
              t("Regress the actual price on several point forecasts, once per quantile level, and the forecasts become a distribution.",
                "Regresăm prețul realizat pe mai multe prognoze punctuale, separat pentru fiecare nivel al cuantilei; rezultatul este o distribuție a prețului."),
              "\\[ \\hat q^{\\tau}_{d,h}=\\beta^{\\tau}_{0,h}+\\beta^{\\tau}_{1,h}\\hat P^{\\text{AW-ARX}}_{d,h}+\\beta^{\\tau}_{2,h}\\hat P^{\\text{AW-LEAR}}_{d,h} \\]"
              "\\[ \\text{PS}_\\tau(q,y)=\\big(\\mathbb 1\\{y<q\\}-\\tau\\big)(q-y) \\]" +
              "\\where{" + t("$\\bm\\beta^{\\tau}_h$ minimises the pinball score (PS) on the last @{prob.w_qra} days of forecasts, re-estimated weekly; $\\tau=0.01,\\dots,0.99$.",
                             "$\\hat q^{\\tau}_{d,h}$ = cuantila de nivel $\\tau$ a prețului; $\\bm\\beta^{\\tau}_h$ minimizează scorul pinball (PS) pe prognozele din ultimele @{prob.w_qra} " + de("prob.w_qra") + "zile, cu reestimare săptămînală; "
                             "$\\tau=0{,}01,\\dots,0{,}99$.") + "}",
              it((t("\\textbf{On our data}, average pinball score", "\\textbf{Pe datele din România}, scorul pinball mediu (mai mic = mai bine)"),
                  t("QRA @{prob.qra.aps|.2f}; conformal prediction (CP) @{prob.cp.aps|.2f}; historical simulation (HS) @{prob.hs.aps|.2f}",
                    "QRA @{prob.qra.aps|.2f}; predicție conformală (CP) @{prob.cp.aps|.2f}; simulare istorică (HS) @{prob.hs.aps|.2f}"),
                  t("CP and HS use the AW-LEAR errors of the last @{prob.w_err} days, as in Assignment 1",
                    "CP și HS folosesc erorile AW-LEAR din ultimele @{prob.w_err} " + de("prob.w_err") + "zile, ca în tema 1")),
                 (t("\\textbf{Coverage of the 90\\% interval}", "\\textbf{Acoperirea intervalului de 90\\%}"),
                  t("QRA @{prob.qra.c90|.1f}\\%, CP @{prob.cp.c90|.1f}\\%, HS @{prob.hs.c90|.1f}\\%; mean QRA width @{prob.qra.w90|.1f} EUR/MWh",
                    "QRA @{prob.qra.c90|.1f}\\%, CP @{prob.cp.c90|.1f}\\%, HS @{prob.hs.c90|.1f}\\%; lățimea medie a intervalului QRA: @{prob.qra.w90|.1f} EUR/MWh"),
                  t("all below 90\\%; the Kupiec test rejects correct coverage", "toate sub 90\\%; testul Kupiec respinge ipoteza unei acoperiri corecte")), sep="2pt"),
              t("a 90\\% band that holds 86\\% of the prices understates the risk of the open position.",
                "o bandă de 90\\% care conține doar 86\\% din prețuri subestimează riscul poziției deschise.").replace("86", fmt(N["prob"]["qra"]["c90"], ".0f", lang)),
              tryit=NB + " \\S7", cite="(Koenker \\& Bassett, 1978; Nowotarski \\& Weron, 2015)", wl="0.52", wr="0.45")

    D.chart(t("A week of QRA intervals in Romania: wide in the evening, narrow at night", "O săptămînă de intervale QRA în România: largi seara, înguste noaptea"),
            "qra_week", [
                t("Week @{weeks.prob|date} -- @{weeks.prob_end|date}; the band widens where the evening price is uncertain and narrows in the calm night hours.",
                  "Săptămîna @{weeks.prob|date} -- @{weeks.prob_end|date}; intervalul este larg seara, cînd prețul este incert, și îngust noaptea."),
                t("The QRA median has MAE @{prob.mae_median_qra|.2f} EUR/MWh, as good as the best point forecast.",
                  "Mediana QRA are MAE @{prob.mae_median_qra|.2f} EUR/MWh, la fel de precisă ca cea mai bună prognoză punctuală.")],
            height="0.52\\textheight", job=t("bid the 50\\% band for volumes you must buy, the tails for what you can shift.",
                                             "ofertați în intervalul de 50\\% volumele pe care trebuie să le cumpărați, iar în cozi pe cele pe care le puteți muta."),
            tryit=NB + " \\S7", cite="(Nowotarski \\& Weron, 2015, Comput.\\ Stat.)")

    D.chart(t("All three methods are too narrow in the tails", "Toate cele trei metode subestimează cozile distribuției prețului"), "prob_rel", [
        t("Coverage error = share of prices below the $\\tau$-quantile minus $\\tau$ (0 = calibrated); above 0 on the left and below 0 on the right = tails too narrow.",
          "Eroarea de acoperire = ponderea prețurilor sub cuantila de nivel $\\tau$ minus $\\tau$ (0 = calibrare perfectă); peste 0 în stînga și sub 0 în dreapta = cozi prea înguste."),
        t("Kupiec statistic for the 90\\% interval: QRA @{prob.qra.kupiec|.1f}, CP @{prob.cp.kupiec|.1f}, HS @{prob.hs.kupiec|.1f} (5\\% critical value 3.84).".replace("3.84", "3{,}84" if ro else "3.84"),
          "Statistica Kupiec pentru intervalul de 90\\%: QRA @{prob.qra.kupiec|.1f}, CP @{prob.cp.kupiec|.1f}, HS @{prob.hs.kupiec|.1f} (valoarea critică la 5\\% este 3{,}84).")],
        height="0.50\\textheight", job=t("widen the tails before using quantiles for collateral (Lecture 4).",
                                         "lărgiți cozile înainte de a folosi cuantilele pentru calculul garanțiilor (cursul 4)."),
        tryit=NB + " \\S7", cite="(Kupiec, 1995, J.\\ Derivatives; Gneiting \\& Raftery, 2007, JASA)")

    # ------------------------------------------------------------------ 8 cointegration
    D.subsection(t("Cointegration: prices that move together", "Cointegrarea: prețuri care evoluează împreună"))
    hu = N["coint"]["HU"]
    D.concept(t("Two trending prices are cointegrated when their spread keeps returning", "Două prețuri sînt cointegrate dacă diferența dintre ele revine spre echilibru"),
              t("Each price may wander, but if a combination is stationary the gap keeps closing and the regression is not spurious.",
                "Fiecare preț poate fi nestaționar, dar, dacă o combinație liniară a lor este staționară, abaterea se închide, iar regresia nu este spurioasă."),
              "\\[ \\underbrace{P^{\\text{RO}}_t=\\alpha+\\beta P^{\\text{HU}}_t+u_t}_{\\text{" + t("step 1, OLS", "pasul 1, OLS") + "}} \\]\\vspace{-2mm}\\[ "
              "\\underbrace{\\Delta\\hat u_t=\\rho\\,\\hat u_{t-1}+\\textstyle\\sum_j\\gamma_j\\Delta\\hat u_{t-j}+\\eta_t}_{\\text{" +
              t("step 2, unit root in } \\hat u", "pasul 2, rădăcină unitară în } \\hat u") + "} \\]" +
              "\\where{" + t("Engle--Granger, $H_0$ no cointegration ($\\rho=0$), MacKinnon critical values; Johansen, trace test on the rank $r$ of a vector error-correction model.",
                             "Engle--Granger: $H_0$ = fără cointegrare ($\\rho=0$), valori critice MacKinnon; Johansen: testul urmei pentru rangul $r$ (numărul relațiilor de cointegrare).") + "}",
              it((t("\\textbf{Romania vs Hungary}, daily, since @{coint.start|date}", "\\textbf{România și Ungaria}, zilnic, din @{coint.start|date}"),
                  t("$\\hat\\beta$ = @{coint.HU.beta|.3f}; Engle--Granger statistic @{coint.HU.eg|.2f} (5\\% critical value @{coint.HU.eg_cv5|.2f}): cointegrated",
                    "$\\hat\\beta$ = @{coint.HU.beta|.3f}; Engle--Granger @{coint.HU.eg|.2f} (critic la 5\\%: @{coint.HU.eg_cv5|.2f}): cointegrate"),
                  t("a shock to the spread halves in @{coint.HU.hl|.1f} days", "un șoc asupra diferenței de preț se înjumătățește în @{coint.HU.hl|.1f} zile")),
                 (t("\\textbf{Johansen trace test}", "\\textbf{Testul urmei Johansen}"),
                  t("$r=0$: @{coint.HU.tr0|.1f} vs @{coint.HU.tr0_cv|.2f}; $r\\le1$: @{coint.HU.tr1|.2f} vs @{coint.HU.tr1_cv|.2f}",
                    "$r=0$: @{coint.HU.tr0|.1f} față de @{coint.HU.tr0_cv|.2f}; $r\\le1$: @{coint.HU.tr1|.2f} față de @{coint.HU.tr1_cv|.2f}"),
                  t("rank 2, the levels are nearly stationary since 2022 (augmented Dickey--Fuller (ADF) $p$ = @{coint.adf_RO|.3f})",
                    "rangul 2: nivelurile sînt aproape staționare din 2022 (testul Dickey--Fuller augmentat (ADF), $p$ = @{coint.adf_RO|.3f})")), sep="2pt"),
              t("a RO--HU spread trade closes within days, not months.", "o poziție pe diferența de preț RO--HU se închide în cîteva zile, nu în luni."),
              tryit=NB + " \\S8", cite="(Engle \\& Granger, 1987; Johansen, 1991; MacKinnon, 1996)", wl="0.50", wr="0.47")

    D.chart(t("Romania and Hungary: coupled markets, a spread that keeps closing", "România și Ungaria: piețe cuplate, cu o diferență de preț care se închide repede"),
            "coint_daily", [
                t("Spread RO $-$ HU: mean @{coint.HU.mean_spread|.2f}, standard deviation @{coint.HU.sd_spread|.2f} EUR/MWh; Romania vs Germany--Luxembourg: @{coint.DE_LU.mean_spread|.2f} and @{coint.DE_LU.sd_spread|.2f}.",
                  "Diferența RO $-$ HU: media @{coint.HU.mean_spread|.2f}, abaterea standard @{coint.HU.sd_spread|.2f} EUR/MWh; pentru România și Germania--Luxemburg: @{coint.DE_LU.mean_spread|.2f} și @{coint.DE_LU.sd_spread|.2f}."),
                t("In the test year RO and HU prices were identical in @{coint.eq_hu_test|.1f}\\% of the hours; the rest reflects congested borders.",
                  "În anul de test, prețurile din RO și HU au fost identice în @{coint.eq_hu_test|.1f}\\% din ore; în restul orelor, interconexiunea a fost congestionată.")],
            height="0.52\\textheight", job=t("use the Hungarian price as a regressor or a check on your Romanian forecast.",
                                             "folosiți prețul din Ungaria ca regresor sau ca verificare a prognozei pentru România."),
            tryit=NB + " \\S8", cite="(Engle \\& Granger, 1987, Econometrica)")

    cm = N["coint_m"]
    D.concept(t("Power, gas and hydro: an error-correction model on monthly data", "Prețul energiei revine spre nivelul dat de gaze: model cu corecția erorii"),
              t("If price and gas are cointegrated, the price is pulled back to its gas-implied level each month, and hydro shifts it in between.",
                "Dacă prețurile energiei și gazelor sînt cointegrate, prețul energiei revine lunar spre nivelul dat de gaze, iar producția hidro îl abate temporar."),
              "\\[ \\Delta P_t=c+\\underbrace{\\alpha\\,(P_{t-1}-a-\\beta\\,\\text{TTF}_{t-1})}_{\\text{" + t("error correction", "corecția erorii") + "}}"
              "+\\gamma\\,\\Delta\\text{TTF}_t+\\delta\\,H_t+\\varepsilon_t \\]" +
              "\\where{" + t("$P_t$ = monthly mean price of Romania; TTF in EUR/MWh; $H_t$ = hydro output minus its calendar-month mean (TWh), stationary; "
                             "$\\alpha<0$ = speed of return.",
                             "$P_t$ = prețul mediu lunar al energiei electrice din România; TTF = prețul gazelor, în EUR/MWh; $H_t$ = producția hidro minus media lunii calendaristice (TWh), staționară; "
                             "$\\alpha<0$ = viteza de revenire spre echilibru.") + "}",
              it((t("\\textbf{On our data}, @{coint_m.start} -- @{coint_m.end}", "\\textbf{Pe datele din România}, @{coint_m.start} -- @{coint_m.end}"),
                  t("Engle--Granger @{coint_m.eg1|.2f} (5\\% critical value @{coint_m.eg1_cv5|.2f}); Johansen rank @{coint_m.jo_rank}",
                    "Engle--Granger @{coint_m.eg1|.2f} (valoarea critică la 5\\%: @{coint_m.eg1_cv5|.2f}); rangul Johansen: @{coint_m.jo_rank}"),
                  t("$\\hat\\beta$ = @{coint_m.beta|.2f}, as if a gas plant of about @{coint_m.eff|.0f}\\% efficiency set the price",
                    "$\\hat\\beta$ = @{coint_m.beta|.2f}, ca și cum prețul ar fi stabilit de o centrală pe gaze cu randament de circa @{coint_m.eff|.0f}\\%")),
                 (t("\\textbf{Error-correction model (ECM)}", "\\textbf{Modelul cu corecția erorii (ECM)}"),
                  t("$\\hat\\alpha$ = @{coint_m.alpha|.3f}, half-life @{coint_m.hl|.1f} months", "$\\hat\\alpha$ = @{coint_m.alpha|.3f}; timpul de înjumătățire: @{coint_m.hl|.1f} luni"),
                  t("$\\hat\\delta$ = @{coint_m.d_hyd|.2f} EUR/MWh per TWh of extra hydro ($t$ = @{coint_m.d_hyd_t|.2f})",
                    "$\\hat\\delta$ = @{coint_m.d_hyd|.2f} EUR/MWh pentru fiecare TWh suplimentar de producție hidro ($t$ = @{coint_m.d_hyd_t|.2f})")), sep="2pt"),
              t("a hydro producer in a dry month can expect prices above the gas-implied level for one or two months.",
                "într-o lună secetoasă, un producător hidro se poate aștepta la prețuri peste nivelul dat de gaze timp de una sau două luni."),
              tryit=NB + " \\S8", cite="(Engle \\& Granger, 1987; Johansen, 1991, Econometrica)", wl="0.53", wr="0.44")
    D.chart(t("Power, gas and hydro: the Lecture 1 regression is not spurious", "Prețul energiei, gazele și hidro: regresia din cursul 1 nu este spurioasă"), "coint_monthly", [
        t("Left, the monthly price follows its gas-implied level; right, months with more hydro than usual sit below it.",
          "În stînga, prețul lunar urmează nivelul de echilibru dat de prețul gazelor; în dreapta, în lunile cu producție hidro peste medie, prețul este sub acest nivel.")],
        height="0.58\\textheight", job=t("read a dry hydro year as a price premium over gas, not as a new price level.",
                                          "interpretați un an hidrologic secetos ca o primă de preț peste nivelul dat de gaze, nu ca un nou nivel al prețului."),
        tryit=NB + " \\S8", cite=t("(Lecture 1, hydro case; own estimation)", "(cursul 1, studiul de caz hidro; estimare proprie)"))

    # ------------------------------------------------------------------ 9 case studies
    D.section(t("Case studies on recent Romanian data", "Studii de caz pe date recente din România"))
    D.subsection(t("(a) A year of forecasts", "(a) Un an de prognoze"))
    D.chart(t("Case study (a): a year of forecasts, month by month", "Studiul de caz (a): acuratețea diferă mult de la o lună la alta"), "monthly_mae", [
        t("AW-LEAR beats naive in @{bymonth.n_months_lear_beats_naive} of 12 months; MAE from @{bymonth.best_mae|.2f} (@{bymonth.best_month|ym}) to @{bymonth.worst_mae|.2f} EUR/MWh (@{bymonth.worst_month|ym}).",
          "AW-LEAR este mai precis decît modelul naiv în @{bymonth.n_months_lear_beats_naive} din 12 luni; MAE variază între @{bymonth.best_mae|.2f} (@{bymonth.best_month|ym}) și @{bymonth.worst_mae|.2f} EUR/MWh (@{bymonth.worst_month|ym}).")],
        height="0.50\\textheight", job=t("report accuracy by month, since a good annual MAE can hide a bad autumn.",
                                         "raportați acuratețea lună de lună: o MAE anuală bună poate ascunde o toamnă slabă."),
        tryit=NB + " \\S9", cite=t("(own computation, " + TEST + ")", "(calcule proprii, " + TEST + ")"))

    D.subsection(t("(b) A stress week", "(b) O săptămînă de criză"))
    D.chart(t("Case study (b): the stress week of @{weeks.stress|date}", "Studiul de caz (b): în săptămîna de criză, modelele întîrzie o zi"), "stress_week", [
        t("Mean @{weeks.stress_mean|.2f}, peak @{weeks.stress_max|.2f} EUR/MWh; MAE naive @{weeks.stress_mae.naive|.2f}, AW-LEAR @{weeks.stress_mae.aw_lear|.2f}, GBM @{weeks.stress_mae.gbm|.2f}, ensemble @{weeks.stress_mae.ens_all|.2f}.",
          "Prețul mediu @{weeks.stress_mean|.2f}, maximul @{weeks.stress_max|.2f} EUR/MWh; MAE: modelul naiv @{weeks.stress_mae.naive|.2f}, AW-LEAR @{weeks.stress_mae.aw_lear|.2f}, GBM @{weeks.stress_mae.gbm|.2f}, ansamblul @{weeks.stress_mae.ens_all|.2f}.")],
        height="0.50\\textheight", job=t("every model lags a jump in level by a day, so hedge the evening hours.",
                                         "toate modelele reacționează la un salt de nivel cu o zi întîrziere; acoperiți riscul orelor de seară."),
        tryit=NB + " \\S9", cite=t("(own computation; OPCOM)", "(calcule proprii; OPCOM)"))

    D.subsection(t("(c) The 15-minute market time unit", "(c) Intervalul de tranzacționare de 15 minute"))
    D.chart(t("Case study (c): forecasting 96 quarter-hours since 1 October 2025", "Studiul de caz (c): sferturile de oră cer un profil în interiorul orei"),
            "mtu15", [
                t("The market time unit (MTU) is 15 minutes; forecast = hourly AW-LEAR + the mean intra-hour shape of the 28 previous days.",
                  "Intervalul de tranzacționare (MTU) are 15 minute; prognoza = AW-LEAR orar + profilul intraorar mediu din ultimele 28 de zile."),
                t("@{mtu15.n_days} test days without DST, quarter-hour MAE @{mtu15.mae_flat|.2f} flat vs @{mtu15.mae_shaped|.2f} EUR/MWh shaped.",
                  "MAE pe sfert de oră în @{mtu15.n_days} " + de("mtu15.n_days") + "zile: @{mtu15.mae_flat|.2f} constant, @{mtu15.mae_shaped|.2f} EUR/MWh cu profil.")],
            height="0.55\\textheight", job=t("a battery bids per quarter-hour; give it the intra-hour shape, not a flat hour.",
                                              "o baterie licitează pe sferturi de oră; folosiți profilul intraorar, nu o valoare constantă."),
            tryit=NB + " \\S9", cite=t("(own computation; OPCOM; SDAC 15-minute go-live, 1 Oct 2025)",
                                        "(calcule proprii; OPCOM; trecerea SDAC la 15 minute, 1 oct. 2025)"))

    bt, fx = N["battery"], N["flex"]
    D.subsection(t("(d) From forecast to money", "(d) Valoarea economică a prognozei"))
    D.chart(t("Case study (d): what a better forecast is worth", "Studiul de caz (d): cît valorează, în bani, o prognoză mai bună"), "battery", [
        t("Battery 1 MW / 2 MWh, one daily cycle, @{battery.n_days} days without DST; @{battery.ens_all.eur|,.0f} EUR per MW with the ensemble (@{battery.ens_all.pct|.1f}\\% of perfect foresight), @{battery.naive.eur|,.0f} with naive.",
          "Baterie de 1 MW / 2 MWh, un ciclu pe zi, @{battery.n_days} " + de("battery.n_days") + "zile fără schimbarea orei; @{battery.ens_all.eur|,.0f} EUR pe MW cu ansamblul (@{battery.ens_all.pct|.1f}\\% din profitul cu informație perfectă), @{battery.naive.eur|,.0f} cu modelul naiv."),
        t("Flexible 4-hour load: @{flex.aw_lear.eur_mwh|.2f} EUR/MWh with AW-LEAR vs @{flex.base_eur_mwh|.2f} for the fixed 8--12 h CET block.",
          "Consum flexibil de 4 ore: @{flex.aw_lear.eur_mwh|.2f} EUR/MWh cu AW-LEAR, față de @{flex.base_eur_mwh|.2f} pentru blocul fix 8--12 CET.")],
        height="0.48\\textheight", job=t("translate rMAE into EUR before paying for a forecast.",
                                         "transformați rMAE în EUR înainte de a plăti pentru o prognoză."),
        tryit=NB + " \\S9", cite=t("(own computation; round-trip efficiency 90\\% assumed)", "(calcule proprii; randament de încărcare--descărcare presupus: 90\\%)"))

    lk = N["leak"]
    D.frame(t("A forecasting desk checklist, and our leakage self-check", "O prognoză se acceptă numai după o listă de verificări; testul nostru arată că nu folosim informație din viitor"), cols(
        it((t("\\textbf{Before you trust a backtest}", "\\textbf{Înainte să aveți încredere într-o testare retrospectivă}"),
            t("every input public before 12:00 CET on $d-1$", "fiecare variabilă de intrare este publicată înainte de ora 12:00 CET din ziua $d-1$"),
            t("scalers, transforms, $\\lambda$ and thresholds fitted in the window only", "standardizările, transformările, $\\lambda$ și pragurile se estimează numai pe fereastra de calibrare"),
            t("chronological validation; the test year touched once", "validarea este cronologică, iar anul de test este folosit o singură dată")),
           (t("\\textbf{Then report}", "\\textbf{Apoi raportați}"),
            t("MAE and rMAE against naive, DM $p$-values, coverage of the intervals", "MAE și rMAE față de modelul naiv, valorile $p$ ale testelor DM, acoperirea intervalelor"),
            t("results by month and by hour, not only one annual number", "rezultate pe luni și pe ore, nu doar o cifră anuală")), sep="3pt"),
        it((t("\\textbf{Our self-check} (analysis script, section 7)", "\\textbf{Autoverificarea noastră} (scriptul de analiză, secțiunea 7)"),
            t("@{leak.n_timestamp_checks|,d} timestamp checks, each input at least @{leak.margin_h|.0f} h before the cut-off",
              "@{leak.n_timestamp_checks|,d} " + de("leak.n_timestamp_checks") + "verificări ale momentului publicării: fiecare variabilă este disponibilă cu cel puțin @{leak.margin_h|.0f} h înainte de ora 12:00"),
            t("@{leak.n_series} forecast series recomputed on @{leak.n_pert_days} days, GBM and MLP on the first day of all @{leak.n_ml_months} refits",
              "@{leak.n_series} " + de("leak.n_series") + "serii de prognoză recalculate în @{leak.n_pert_days} " + de("leak.n_pert_days") + "zile; GBM și MLP, în prima zi a fiecăreia dintre cele @{leak.n_ml_months} reestimări"),
            t("later data deleted or replaced by nonsense; forecasts identical up to rounding",
              "datele ulterioare au fost șterse sau înlocuite cu valori absurde: prognozele au rămas identice, pînă la rotunjire"),
            t("status: passed", "rezultat: verificare trecută")), sep="3pt"), "0.52", "0.45") +
        D.bottom(t("make the leakage check part of every model review, as Assignment 1 does.",
                   "includeți testul de folosire a informației din viitor în orice evaluare a unui model, ca în tema 1."), NB + " \\S10"),
        "footnotesize", cite=t("(Assignment 1; Lago et al., 2021, APEN)", "(tema 1; Lago et al., 2021, APEN)"))

    # ------------------------------------------------------------------ research and practice: AIDA 2026
    WER = "https://github.com/danpele/EMQA/blob/main/resources/aida2026/weron_ml_electricity_price_forecasting.pdf"
    PET = "https://github.com/danpele/EMQA/blob/main/resources/aida2026/petukhina_multivariate_probabilistic_epf.pdf"
    D.subsection(t("Research and practice: AIDA 2026", "Cercetare și practică: conferința AIDA 2026"))
    D.frame(t("AIDA 2026: probabilistic forecasts are judged by the money they make",
              "AIDA 2026: prognozele probabilistice se judecă după banii pe care îi aduc"), cols(
        it((t("\\textbf{R.\\ Weron, keynote} (4 June 2026, \\href{" + WER + "}{slides})",
              "\\textbf{R.\\ Weron}, 4 iunie 2026 (\\href{" + WER + "}{diapozitive})"),
            t("one model per hour (as our ARX, LEAR) or all 24 hours jointly; averaging across windows and LEAR stay the benchmarks to beat",
              "cîte un model pe oră (ca ARX și LEAR) sau un model comun pentru 24 de ore; medierea pe ferestre și LEAR rămîn reperele")),
           (t("\\textbf{What the cited work found}", "\\textbf{Ce au găsit lucrările prezentate}"),
            t("trading on quantiles earned 19--34\\% more than trading on point forecasts (Uniejewski \\& Weron, 2021)",
              "ofertele pe cuantile au adus cu 19--34\\% mai mult profit decît cele pe prognoze punctuale (Uniejewski \\& Weron, 2021)"),
            t("test year 2025: continuous ranked probability score (CRPS) 3.56 for the pretrained transformer TabPFN 3.0 vs 4.71 for LEAR + CP",
              "în 2025, scorul de probabilitate ordonat continuu (CRPS): 3{,}56 pentru transformerul TabPFN (versiunea 3), 4{,}71 pentru LEAR + CP")), sep="3pt"),
        it((t("\\textbf{A.\\ Petukhina}, with G.\\ Mazzon, D.\\ Marazzina (3 June 2026, \\href{" + PET + "}{slides})",
              "\\textbf{A.\\ Petukhina}, cu G.\\ Mazzon, D.\\ Marazzina (3 iunie 2026, \\href{" + PET + "}{diapozitive})"),
            t("Great Britain, outside SDAC, runs two hourly day-ahead auctions (EPEX SPOT, Nord Pool): buy in one, sell in the other",
              "Marea Britanie, în afara SDAC: două licitații orare (EPEX SPOT, Nord Pool); cumpărați într-una, vindeți în cealaltă"),
            t("one joint forecast of both auction prices and the system price (copula model); test Mar -- Sep 2022",
              "prognoză comună a celor două prețuri și a prețului de dezechilibru (copulă); test mar. -- sep. 2022")),
           (t("\\textbf{What it found}", "\\textbf{Ce a găsit}"),
            t("EPEX auction: MAE 47.884 vs 27.926 for LASSO + QRA, but CRPS 16.852 vs 32.605",
              "EPEX: MAE 47{,}884 față de 27{,}926 (LASSO + QRA), dar CRPS 16{,}852 față de 32{,}605"),
            t("trading on mean and conditional value at risk (CVaR): 22\\,001 EUR vs 6\\,283.3 and $-$3\\,005.1 EUR for the LASSO + QRA models",
              "strategia medie -- valoarea la risc condiționată (CVaR): 22\\,001 EUR, față de 6\\,283{,}3 și $-$3\\,005{,}1 EUR (LASSO + QRA)")), sep="3pt"),
        "0.49", "0.48") +
        D.bottom(t("judge a forecast by the decision it feeds: in Great Britain the model with the larger MAE earned more.",
                   "judecați prognoza după decizia pe care o susține: modelul cu MAE mai mare a cîștigat mai mult.")),
        "footnotesize", cite=t("(as printed on the AIDA 2026 slides, Bucharest; papers: \\href{https://doi.org/10.1016/j.eneco.2021.105121}{Uniejewski \\& Weron, 2021, ENEECO}; "
                               "\\href{https://doi.org/10.1016/j.eneco.2024.108008}{Agakishiev et al., 2025, ENEECO})",
                               "(diapozitivele AIDA 2026; lucrări: \\href{https://doi.org/10.1016/j.eneco.2021.105121}{Uniejewski \\& Weron, 2021, ENEECO}; "
                               "\\href{https://doi.org/10.1016/j.eneco.2024.108008}{Agakishiev et al., 2025, ENEECO})"))

    GHE = "https://github.com/danpele/EMQA/blob/main/resources/aida2026/ghelasi_probabilistic_merit_order.pdf"
    D.frame(t("AIDA 2026: a data-driven merit order forecasts the price distribution",
              "AIDA 2026: ordinea de merit, estimată din date, dă distribuția prețului"), cols(
        it((t("\\textbf{P.\\ Ghelasi}, with J.\\ Browell, F.\\ Ziel (3 June 2026, \\href{" + GHE + "}{slides})",
              "\\textbf{P.\\ Ghelasi}, cu J.\\ Browell, F.\\ Ziel (3 iunie 2026, \\href{" + GHE + "}{diapozitive})"),
            t("price = merit order (plants sorted by variable cost) at the load: a fundamental, interpretable model",
              "prețul = ordinea de merit (centrale ordonate după costul variabil) la nivelul consumului; model fundamental, interpretabil"),
            t("efficiencies and CO$_2$ intensities estimated from past prices, within expert bounds",
              "randamentele și intensitățile de CO$_2$, estimate din prețuri trecute, între limite date de experți")),
           (t("\\textbf{Germany, point forecasts}", "\\textbf{Germania, prognoze punctuale}"),
            t("train 1 Oct 2022 -- 1 Oct 2023, test 1 Oct 2023 -- 1 Oct 2024, no recalibration",
              "estimare 1 oct.\\ 2022 -- 1 oct.\\ 2023, test 1 oct.\\ 2023 -- 1 oct.\\ 2024, fără reestimare"),
            t("MAE, EUR/MWh: 11.83 for this model; 13.11 LASSO, 13.96 boosted trees, 16.36 classical merit order, 24.96 naive",
              "MAE, EUR/MWh: 11{,}83 pentru acest model; 13{,}11 LASSO, 13{,}96 gradient boosting, 16{,}36 ordinea de merit clasică, 24{,}96 naiv"),
), sep="2pt"),
        it((t("\\textbf{Probabilistic merit order}", "\\textbf{Ordinea de merit probabilistică}"),
            t("forecast the distribution of each input (load, solar, wind, fuels); plug each sampled scenario into the merit order",
              "distribuția prognozată a fiecărei intrări (consum, solar, vînt, combustibili); fiecare scenariu simulat trece prin ordinea de merit"),
            t("parameters chosen to minimise the CRPS of the resulting prices",
              "parametrii minimizează CRPS a prețurilor rezultate")),
           (t("\\textbf{What it found}", "\\textbf{Ce a găsit}"),
            t("CRPS 13.92 vs 14.04 for a Johnson $S_U$ distribution model and 20.46 for naive",
              "CRPS 13{,}92, față de 14{,}04 pentru un model cu distribuția Johnson $S_U$ și 20{,}46 pentru cel naiv"),
            t("MAE 17.28 vs 18.21 and 25.98; RMSE 25.81 vs 29.19 and 41.47",
              "MAE 17{,}28, față de 18{,}21 și 25{,}98; RMSE 25{,}81, față de 29{,}19 și 41{,}47"),
            t("simulated prices form non-parametric distributions, e.g.\\ a cluster near zero at midday",
              "prețurile simulate au distribuții neparametrice, de ex.\\ o grupare lîngă zero la amiază")), sep="2pt"),
        "0.50", "0.47") +
        D.bottom(t("a fundamental model estimated like a statistical one gives forecasts you can explain plant by plant.",
                   "un model fundamental estimat statistic dă prognoze pe care le puteți explica centrală cu centrală.")),
        "footnotesize", cite=t("(talk by P.\\ Ghelasi at AIDA 2026, Bucharest, 3 June 2026: \\href{" + GHE + "}{slides}; "
                               "paper: \\href{https://doi.org/10.1016/j.eneco.2025.109114}{Ghelasi \\& Ziel, 2026, ENEECO})",
                               "(prezentarea lui P.\\ Ghelasi la AIDA 2026, București, 3 iunie 2026: \\href{" + GHE + "}{diapozitive}; "
                               "lucrare: \\href{https://doi.org/10.1016/j.eneco.2025.109114}{Ghelasi \\& Ziel, 2026, ENEECO})"))

    # ------------------------------------------------------------------ wrap-up
    D.parts.append("\\section*{" + t("Wrap-up", "Recapitulare") + "}\n")
    D.quiz_frame(t("the naive rule on a Monday", "modelul naiv pentru o zi de luni"),
                 t("It is Sunday, 11:30 CET; you must forecast Monday, hour 19:00, with the naive benchmark; which price do you use?",
                   "Este duminică, ora 11:30 CET; trebuie să prognozați cu modelul naiv prețul de luni pentru ora 19:00; ce preț folosiți?"),
                 t("The price of the previous Monday at 19:00 ($d-7$); on our test year this beats Sunday's price on Mon, Sat and Sun "
                   "(MAE @{naive_dow.monsatsun.lag7|.2f} vs @{naive_dow.monsatsun.lag1|.2f} EUR/MWh).",
                   "Prețul de luni trecută, ora 19:00 ($d-7$); în anul de test, pentru zilele de luni, sîmbătă și duminică, această regulă este mai precisă "
                   "decît prețul din ziua precedentă (MAE @{naive_dow.monsatsun.lag7|.2f} față de @{naive_dow.monsatsun.lag1|.2f} EUR/MWh)."))
    D.quiz_frame(t("a suspicious backtest", "o testare retrospectivă suspectă"),
                 t("A vendor reports rMAE 0.55 for Romania and uses the realised load of day $d-1$ as a regressor; do you buy?",
                   "Un furnizor de prognoze raportează rMAE 0{,}55 pentru România, dar folosește ca regresor consumul realizat în ziua $d-1$; cumpărați prognoza?"),
                 t("No: at 12:00 on $d-1$ that day is not yet metered, so the backtest leaks information; ask for a rerun with data up to $d-2$ "
                   "(or published day-ahead forecasts); our honest best is rMAE @{acc.ens_all.rmae|.3f}.",
                   "Nu: la ora 12:00 din ziua $d-1$, consumul acelei zile nu este încă măsurat, deci testarea folosește informație din viitor; cereți o nouă testare "
                   "cu date pînă în ziua $d-2$ (sau cu prognozele publicate de TSO); cel mai bun rezultat corect al nostru este rMAE @{acc.ens_all.rmae|.3f}."))
    D.quiz_frame(t("reading a DM test", "interpretarea testului DM"),
                 t("AW-ARX or AW-LEAR? The DM test gives $p$ = " + pval("dm.arx_lear.p") + "; which model goes into production?",
                   "AW-LEAR sau AW-ARX? Testul DM dă $p$ = " + pval("dm.arx_lear.p") + "; ce model intră în producție?"),
                 t("Neither wins significantly; take the simpler one, or better their average, which is part of the best ensemble "
                   "(rMAE @{acc.ens_all.rmae|.3f}).",
                   "Niciunul nu este semnificativ mai precis; alegeți modelul mai simplu sau, mai bine, media lor, care face parte din cel mai bun "
                   "ansamblu (rMAE @{acc.ens_all.rmae|.3f})."))
    D.quiz_frame(t("an error measure for the board", "o măsură a erorii pentru consiliul de administrație"),
                 t("Your report shows MAPE @{mape.aw_lear|,.0f}\\% for the Romanian price forecast; the board is alarmed; what do you say?",
                   "Raportul dumneavoastră indică MAPE @{mape.aw_lear|,.0f}\\% pentru prognoza prețului din România, iar consiliul este alarmat; ce răspundeți?"),
                 t("MAPE divides by prices near zero ($@{mape.n_small}$ hours below 5 EUR/MWh produce @{mape.share_from_small|.1f}\\% of it); report "
                   "MAE @{acc.aw_lear.mae|.2f} EUR/MWh and rMAE @{acc.aw_lear.rmae|.3f} instead.",
                   "MAPE împarte eroarea la prețuri apropiate de zero (@{mape.n_small} " + de("mape.n_small") + "ore sub 5 EUR/MWh produc "
                   "@{mape.share_from_small|.1f}\\% din valoarea ei); raportați în schimb MAE @{acc.aw_lear.mae|.2f} EUR/MWh și rMAE @{acc.aw_lear.rmae|.3f}."))
    D.quiz_frame(t("cointegration in practice", "cointegrarea în practică"),
                 t("The RO--HU spread is cointegrated with a half-life of @{coint.HU.hl|.1f} days; today Romania is 40 EUR/MWh above Hungary; what do you expect?",
                   "Prețurile din România și Ungaria sînt cointegrate, iar un șoc asupra diferenței se înjumătățește în @{coint.HU.hl|.1f} zile; astăzi prețul din România este cu 40 EUR/MWh mai mare decît cel din Ungaria; la ce vă așteptați?"),
                 t("The gap should shrink by about half within a day, unless the border stays congested; it is a signal for cross-border "
                   "trading, not a guarantee.",
                   "Diferența ar trebui să se reducă la circa jumătate în aproximativ o zi, dacă interconexiunea nu rămîne congestionată; "
                   "este un semnal pentru tranzacțiile transfrontaliere, nu o garanție."))

    D.frame(t("Wrap-up", "Recapitulare"), "\\vspace{-2mm}\\begin{multicols}{2}\\scriptsize\\tableofcontents\\end{multicols}\n" + it(
        t("Honest setup first: information at 12:00 CET on $d-1$, rolling windows, naive benchmark, DM tests.",
          "Mai întîi, un cadru corect: numai informația disponibilă la ora 12:00 CET în ziua $d-1$, ferestre glisante, modelul naiv ca reper și teste DM."),
        t("On the test year the best model, an ensemble of 4, cuts the naive error by @{gain.ens_all|.1f}\\%; next: volatility (Lecture 3).",
          "În anul de test, cel mai bun model, ansamblul de 4 modele, reduce eroarea modelului naiv cu @{gain.ens_all|.1f}\\%; cursul următor: volatilitatea (cursul 3)."),
        sep="1pt"))

    D.frame(t("Research from our group on forecasting Romanian power", "Cercetările grupului nostru despre prognoza consumului și a prețurilor în România"), it(
        t("\\textbf{Benchmarking load forecasts}: classical seasonal models against neural networks on Romania's national consumption; "
          "in the paper a neural network has a clearly lower error than the seasonal autoregressive benchmark (Proșcanu, Proșcanu, Pele \\& Costea, 2025, RJEF) --- case study C2.",
          "\\textbf{Compararea modelelor de prognoză a consumului} (Proșcanu, Proșcanu, Pele \\& Costea, 2025, RJEF); ce a făcut lucrarea: a comparat modele sezoniere clasice "
          "și rețele neuronale pe consumul național orar al României; rezultat: o rețea neuronală are o eroare net mai mică decît modelul autoregresiv sezonier (studiul de caz C2)"),
        t("\\textbf{Four generations of price models}: a comparative evaluation of four generations of forecasting methods for energy "
          "prices, a reference for choosing a model family (Andrei, Velev, Toma, Pele \\& Lessmann, 2024, arXiv 2411.03372).",
          "\\textbf{Patru generații de modele pentru prețul energiei} (Andrei, Velev, Toma, Pele \\& Lessmann, 2024, arXiv 2411.03372); ce a făcut lucrarea: a evaluat comparativ "
          "patru generații de metode de prognoză a prețurilor energiei; utilitate: un reper pentru alegerea familiei de modele"),
        t("\\textbf{Explaining price forecasts across horizons}: which drivers matter at which horizon and in which price regime, for Romanian "
          "hourly prices (Andrei, Pele \\& Cramer, 2026, PICBE).",
          "\\textbf{Explicarea prognozelor de preț pe mai multe orizonturi} (Andrei, Pele \\& Cramer, 2026, PICBE); ce a făcut lucrarea: a explicat prognozele "
          "prețurilor orare din România; rezultat: arată ce factori contează la fiecare orizont de prognoză și în fiecare regim de preț"),
        t("\\textbf{Early warning of price spikes}: an explainable artificial intelligence (AI) system in which the previous price and the residual load drive the "
          "spikes (Andrei, Pele, Cramer, Amza \\& Diaconu, 2026, PICBE) --- preview of Lecture 7.",
          "\\textbf{Avertizarea timpurie a salturilor de preț} (Andrei, Pele, Cramer, Amza \\& Diaconu, 2026, PICBE); ce a făcut lucrarea: a construit un sistem explicabil "
          "de inteligență artificială (AI) pentru piața din România; rezultat: prețul anterior și consumul rezidual sînt principalii factori ai salturilor (tema cursului 7)"),
        sep="3pt") + note(t("Findings as stated in the papers; numbers on the other slides come from our own data.",
                            "Rezultatele de pe acest diapozitiv sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.")),
        "footnotesize", cite=t("(Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting)",
                               "(Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică)"))

    D.frame(t("Want to learn more?", "Lecturi și resurse suplimentare"), cols(it(
        t("\\textbf{R.\\ Weron, IIF Distinguished Lectures on electricity price forecasting} (2025): slides ",
          "\\textbf{R.\\ Weron, IIF Distinguished Lectures despre prognoza prețurilor energiei electrice} (2025): prezentări ") +
        "\\href{https://p.wz.pwr.edu.pl/~weron.rafal/assets/PDF/Weron25_IIF_1.pdf}{" + t("part I", "partea I") + "}, "
        "\\href{https://p.wz.pwr.edu.pl/~weron.rafal/assets/PDF/Weron25_IIF_2.pdf}{" + t("part II", "partea a II-a") + "}, "
        "\\href{https://github.com/lipiecki/energy-analytics-2025}{" + t("notebooks", "notebook-uri Jupyter") + "}.",
        t("\\textbf{epftoolbox}, LEAR and DNN with the open benchmark of Lago et al.\\ (2021): ",
          "\\textbf{epftoolbox}, LEAR și DNN, cu setul de date pentru evaluare publicat de Lago et al.\\ (2021): ") +
        "\\href{https://github.com/jeslago/epftoolbox}{github.com/jeslago/epftoolbox}.",
        "\\textbf{Forecasting -- Principles and Practice}, " + t("3rd ed.", "ed.\\ a 3-a") + ", \\href{https://otexts.com/fpp3/}{otexts.com/fpp3}.", sep="4pt"),
        it(t("\\textbf{This course}: code, data, notebooks --- ", "\\textbf{Acest curs}: cod, date, notebook-uri Jupyter --- ") +
           "\\href{https://github.com/danpele/EMQA}{github.com/danpele/EMQA}.",
           t("\\textbf{Assignment 1} applies ARX, LEAR, DM and the HS/CP intervals to your own test window.",
             "\\textbf{Tema 1} aplică ARX, LEAR, DM și intervalele HS/CP pe propria fereastră de test."),
           t("\\textbf{Experiment yourself}: the notebook reproduces every chart and number of this lecture --- ",
             "\\textbf{Exercițiu practic}: notebook-ul Jupyter reproduce toate graficele și cifrele din acest curs --- ") +
           "\\href{\\emqarepo/\\emqanb}{notebooks/}.", sep="4pt"), "0.52", "0.45"))

    REFS = [
        "Andrei, A.-V., Pele, D.-T.\\ \\& Cramer, A.-A.\\ (2026). Multi-horizon explainability in energy price forecasting: Disentangling "
        "market dynamics and renewable intermittency in Romania's liberalized electricity market. \\textit{Proceedings of the "
        "International Conference on Business Excellence}, 20(1), 104--117. \\href{https://doi.org/10.2478/picbe-2026-0014}{doi:10.2478/picbe-2026-0014}",
        "Andrei, A.-V., Pele, D.-T., Cramer, A.-A., Amza, A.\\ \\& Diaconu, D.\\ (2026). Explainable AI-based early warning system for electricity "
        "price spikes: Evidence from the Romanian market. \\textit{Proceedings of the International Conference on Business Excellence}, 20(1), "
        "4820--4836. \\href{https://doi.org/10.2478/picbe-2026-0352}{doi:10.2478/picbe-2026-0352}",
        "Andrei, A.-V., Velev, G., Toma, F.-M., Pele, D.\\,T.\\ \\& Lessmann, S.\\ (2024). Energy price modelling: A comparative evaluation of "
        "four generations of forecasting methods. arXiv:2411.03372. \\href{https://arxiv.org/abs/2411.03372}{arxiv.org/abs/2411.03372}",
        "Agakishiev, I., Härdle, W.\\,K., Kopa, M., Kozmík, K.\\ \\& Petukhina, A.\\ (2025). Multivariate probabilistic forecasting of electricity prices "
        "with trading applications. \\textit{Energy Economics}, 141, 108008. \\href{https://doi.org/10.1016/j.eneco.2024.108008}{doi:10.1016/j.eneco.2024.108008}",
        "Bates, J.\\,M.\\ \\& Granger, C.\\,W.\\,J.\\ (1969). The combination of forecasts. \\textit{Operational Research Quarterly}, 20(4), 451--468. "
        "\\href{https://doi.org/10.1057/jors.1969.103}{doi:10.1057/jors.1969.103}",
        "Diebold, F.\\,X.\\ \\& Mariano, R.\\,S.\\ (1995). Comparing predictive accuracy. \\textit{Journal of Business \\& Economic Statistics}, "
        "13(3), 253--263. \\href{https://doi.org/10.1080/07350015.1995.10524599}{doi:10.1080/07350015.1995.10524599}",
        "Engle, R.\\,F.\\ \\& Granger, C.\\,W.\\,J.\\ (1987). Co-integration and error correction: Representation, estimation, and testing. "
        "\\textit{Econometrica}, 55(2), 251--276. \\href{https://doi.org/10.2307/1913236}{doi:10.2307/1913236}",
        "Friedman, J.\\,H.\\ (2001). Greedy function approximation: A gradient boosting machine. \\textit{Annals of Statistics}, 29(5), "
        "1189--1232. \\href{https://doi.org/10.1214/aos/1013203451}{doi:10.1214/aos/1013203451}",
        "Ghelasi, P., Browell, J.\\ \\& Ziel, F.\\ (2026). A probabilistic merit order for electricity price forecasting. AIDA Conference, "
        "Bucharest University of Economic Studies, 3 June 2026. "
        "\\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/ghelasi_probabilistic_merit_order.pdf}{github.com/danpele/EMQA/resources/aida2026}",
        "Ghelasi, P.\\ \\& Ziel, F.\\ (2026). A data-driven merit order: Learning a fundamental electricity price model. "
        "\\textit{Energy Economics}, 154, 109114. \\href{https://doi.org/10.1016/j.eneco.2025.109114}{doi:10.1016/j.eneco.2025.109114}",
        "Gneiting, T.\\ \\& Raftery, A.\\,E.\\ (2007). Strictly proper scoring rules, prediction, and estimation. \\textit{Journal of the "
        "American Statistical Association}, 102(477), 359--378. \\href{https://doi.org/10.1198/016214506000001437}{doi:10.1198/016214506000001437}",
        "Hubicka, K., Marcjasz, G.\\ \\& Weron, R.\\ (2019). A note on averaging day-ahead electricity price forecasts across calibration "
        "windows. \\textit{IEEE Transactions on Sustainable Energy}, 10(1), 321--323. \\href{https://doi.org/10.1109/TSTE.2018.2869557}{doi:10.1109/TSTE.2018.2869557}",
        "Hyndman, R.\\,J.\\ \\& Koehler, A.\\,B.\\ (2006). Another look at measures of forecast accuracy. \\textit{International Journal of "
        "Forecasting}, 22(4), 679--688. \\href{https://doi.org/10.1016/j.ijforecast.2006.03.001}{doi:10.1016/j.ijforecast.2006.03.001}",
        "Johansen, S.\\ (1991). Estimation and hypothesis testing of cointegration vectors in Gaussian vector autoregressive models. "
        "\\textit{Econometrica}, 59(6), 1551--1580. \\href{https://doi.org/10.2307/2938278}{doi:10.2307/2938278}",
        "Koenker, R.\\ \\& Bassett, G.\\ (1978). Regression quantiles. \\textit{Econometrica}, 46(1), 33--50. "
        "\\href{https://doi.org/10.2307/1913643}{doi:10.2307/1913643}",
        "Kupiec, P.\\,H.\\ (1995). Techniques for verifying the accuracy of risk measurement models. \\textit{Journal of Derivatives}, 3(2), 73--84. \\href{https://doi.org/10.3905/jod.1995.407942}{doi:10.3905/jod.1995.407942}",
        "Lago, J., Marcjasz, G., De Schutter, B.\\ \\& Weron, R.\\ (2021). Forecasting day-ahead electricity prices: A review of "
        "state-of-the-art algorithms, best practices and an open-access benchmark. \\textit{Applied Energy}, 293, 116983. "
        "\\href{https://doi.org/10.1016/j.apenergy.2021.116983}{doi:10.1016/j.apenergy.2021.116983}",
        "NEMO Committee (2025). 15-Minute MTU in SDAC was implemented. SDAC press release, 1 October 2025. "
        "\\href{https://nemo-committee.eu/assets/files/15-minute-mtu-in-sdac-was-implemented.pdf}{nemo-committee.eu}",
        "NEMO Committee (2026). Single Day-Ahead Coupling (SDAC) and the EUPHEMIA algorithm. "
        "\\href{https://www.nemo-committee.eu/sdac}{nemo-committee.eu/sdac}",
        "MacKinnon, J.\\,G.\\ (1996). Numerical distribution functions for unit root and cointegration tests. "
        "\\textit{Journal of Applied Econometrics}, 11(6), 601--618. "
        "\\href{https://doi.org/10.1002/(SICI)1099-1255(199611)11:6\\%3C601::AID-JAE417\\%3E3.0.CO;2-T}{doi:10.1002/(SICI)1099-1255(199611)11:6\\textless{}601::AID-JAE417\\textgreater{}3.0.CO;2-T}",
        "Marcjasz, G., Serafin, T.\\ \\& Weron, R.\\ (2018). Selection of calibration windows for day-ahead electricity price forecasting. "
        "\\textit{Energies}, 11(9), 2364. \\href{https://doi.org/10.3390/en11092364}{doi:10.3390/en11092364}",
        "Mazzon, G., Petukhina, A.\\ \\& Marazzina, D.\\ (2026). Multivariate probabilistic day-ahead electricity price forecasting and "
        "cross-auction trading in the UK market. AIDA Conference, Bucharest University of Economic Studies, 3 June 2026. "
        "\\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/petukhina_multivariate_probabilistic_epf.pdf}{github.com/danpele/EMQA/resources/aida2026}",
        "Nogales, F.\\,J., Contreras, J., Conejo, A.\\,J.\\ \\& Espínola, R.\\ (2002). Forecasting next-day electricity prices by time "
        "series models. \\textit{IEEE Transactions on Power Systems}, 17(2), 342--348. \\href{https://doi.org/10.1109/TPWRS.2002.1007902}{doi:10.1109/TPWRS.2002.1007902}",
        "Nowotarski, J.\\ \\& Weron, R.\\ (2015). Computing electricity spot price prediction intervals using quantile regression and "
        "forecast averaging. \\textit{Computational Statistics}, 30(3), 791--803. \\href{https://doi.org/10.1007/s00180-014-0523-0}{doi:10.1007/s00180-014-0523-0}",
        "Nowotarski, J.\\ \\& Weron, R.\\ (2018). Recent advances in electricity price forecasting: A review of probabilistic forecasting. "
        "\\textit{Renewable and Sustainable Energy Reviews}, 81, 1548--1568. \\href{https://doi.org/10.1016/j.rser.2017.05.234}{doi:10.1016/j.rser.2017.05.234}",
        "Proșcanu, C.\\,A., Proșcanu, M.\\,E., Pele, D.\\,T.\\ \\& Costea, A.\\ (2025). Watt's next? Benchmarking time series models on "
        "Romania's national electricity consumption. \\textit{Romanian Journal of Economic Forecasting}, 28(3), 146--163. \\href{https://EconPapers.repec.org/RePEc:rjr:romjef:v::y:2025:i:3:p:146-163}{RePEc}.",
        "Tibshirani, R.\\ (1996). Regression shrinkage and selection via the lasso. \\textit{Journal of the Royal Statistical Society B}, "
        "58(1), 267--288. \\href{https://doi.org/10.1111/j.2517-6161.1996.tb02080.x}{doi:10.1111/j.2517-6161.1996.tb02080.x}",
        "Uniejewski, B., Nowotarski, J.\\ \\& Weron, R.\\ (2016). Automated variable selection and shrinkage for day-ahead electricity price "
        "forecasting. \\textit{Energies}, 9(8), 621. \\href{https://doi.org/10.3390/en9080621}{doi:10.3390/en9080621}",
        "Uniejewski, B., Weron, R.\\ \\& Ziel, F.\\ (2018). Variance stabilizing transformations for electricity spot price forecasting. "
        "\\textit{IEEE Transactions on Power Systems}, 33(2), 2219--2229. \\href{https://doi.org/10.1109/TPWRS.2017.2734563}{doi:10.1109/TPWRS.2017.2734563}",
        "Uniejewski, B.\\ \\& Weron, R.\\ (2021). Regularized quantile regression averaging for probabilistic electricity price forecasting. "
        "\\textit{Energy Economics}, 95, 105121. \\href{https://doi.org/10.1016/j.eneco.2021.105121}{doi:10.1016/j.eneco.2021.105121}",
        "Weron, R.\\ (2014). Electricity price forecasting: A review of the state-of-the-art with a look into the future. "
        "\\textit{International Journal of Forecasting}, 30(4), 1030--1081. \\href{https://doi.org/10.1016/j.ijforecast.2014.08.008}{doi:10.1016/j.ijforecast.2014.08.008}",
        "Weron, R.\\ (2026). Machine learning for electricity price forecasting. Keynote, AIDA Conference, Bucharest University of Economic "
        "Studies, 4 June 2026. \\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/weron_ml_electricity_price_forecasting.pdf}{github.com/danpele/EMQA/resources/aida2026}",
        "Ziel, F.\\ \\& Weron, R.\\ (2018). Day-ahead electricity price forecasting with high-dimensional structures: Univariate vs.\\ "
        "multivariate modeling frameworks. \\textit{Energy Economics}, 70, 396--420. \\href{https://doi.org/10.1016/j.eneco.2017.12.016}{doi:10.1016/j.eneco.2017.12.016}",
    ]
    for part, (a_, b_) in enumerate([(0, 9), (9, 18), (18, 27), (27, len(REFS))]):
        D.frame(t("References", "Bibliografie") + f" ({part + 1}/4)", "\\begin{itemize}\\setlength{\\itemsep}{0pt}\\scriptsize\n" +
                "\n".join("\\item " + r for r in REFS[a_:b_]) + "\n\\end{itemize}", "scriptsize")

    # ------------------------------------------------------------------ appendix
    D.mark_main_end()
    D.parts.append("\\section*{" + t("Appendix", "Anexă") + "}\n")
    D.frame(t("Appendix A: LEAR in full", "Anexa A: modelul LEAR în detaliu"), cols(
        "\\[ \\text{AIC}(\\lambda)=n\\ln\\frac{\\text{RSS}(\\lambda)}{n}+2\\,\\mathrm{df}(\\lambda) \\]" + it(
            t("Residual sum of squares (RSS); the degrees of freedom df($\\lambda$) = number of non-zero coefficients; path by least angle regression (LARS), in scikit-learn.",
              "Suma pătratelor reziduurilor (RSS); df($\\lambda$) = gradele de libertate = numărul coeficienților nenuli; traiectoria de regularizare se calculează cu algoritmul least angle regression (LARS), în scikit-learn."),
            t("Price block: $m$, $s$ = median and $1.4826\\cdot$MAD of the prices of rows $d-T-7,\\dots,d-1$, pooled over 24 hours.".replace("1.4826", "1{,}4826" if ro else "1.4826"),
              "Blocul prețurilor: $m$ și $s$ = mediana și $1{,}4826\\cdot$MAD ale prețurilor din zilele $d-T-7,\\dots,d-1$, calculate pe toate cele 24 de ore împreună."),
            t("Load and wind + solar: own asinh transform from rows up to $d-2$; then every column z-scored on the calibration rows.",
              "Consumul și producția eoliană și solară: transformare asinh proprie, cu date pînă în ziua $d-2$; apoi fiecare coloană este standardizată pe zilele de calibrare."),
            sep="3pt"),
        table("@{}lr@{}", [t("Block", "Bloc"), t("Columns", "Coloane")], [
            [t("prices $d-1$, all 24 hours", "prețuri $d-1$, toate cele 24 de ore"), "24"],
            [t("prices $d-2$, $d-3$, $d-7$", "prețuri $d-2$, $d-3$, $d-7$"), "72"],
            [t("load $d-2$, $d-3$, $d-7$", "consum $d-2$, $d-3$, $d-7$"), "72"],
            [t("wind + solar $d-2$, $d-3$, $d-7$", "eolian + solar $d-2$, $d-3$, $d-7$"), "72"],
            [t("day of week", "ziua săptămînii"), "7"], [t("\\textbf{total}", "\\textbf{total}"), "\\textbf{247}"]],
            size="footnotesize", stretch="1.15"), "0.55", "0.42"), "small",
        cite="(Uniejewski, Nowotarski \\& Weron, 2016, Energies; Lago et al., 2021, APEN)")

    q = N["byq"]
    qrows = [[MN[k] if k in MN else k] + [heat(v, min(q[k2][j] for k2 in ["naive", "aw_arx", "aw_lear", "gbm", "mlp", "ens_all"]),
                                                max(q[k2][j] for k2 in ["naive", "aw_arx", "aw_lear", "gbm", "mlp", "ens_all"]), True,
                                                fmt(v, ".2f", lang)) for j, v in enumerate(q[k])]
             for k in ["naive", "aw_arx", "aw_lear", "gbm", "mlp", "ens_all"]]
    D.frame(t("Appendix B: MAE by quarter of the test year", "Anexa B: MAE pe trimestre în anul de test"),
            "\\begin{center}" + table("@{}l" + "r" * len(q["q"]) + "@{}", [t("Model", "Model")] +
                                      [f"{x[:4]} T{x[-1]}" if ro else x.replace("Q", " Q") for x in q["q"]], qrows,
                                      size="footnotesize", stretch="1.15") + "\\end{center}" +
            note(t("Days per quarter: " + ", ".join(str(n) for n in q["ndays"]) + " (the test year starts on @{design.test_start|date}).",
                   "Zile pe trimestru: " + ", ".join(str(n) for n in q["ndays"]) + " (anul de test începe la @{design.test_start|date})."),
                 t("Green = best in that quarter, red = worst.", "Verde = cel mai bun în trimestrul respectiv, roșu = cel mai slab.")),
            "small", cite=CITE_W)

    pr = N["prob"]
    D.frame(t("Appendix C: probabilistic scores and the Kupiec test", "Anexa C: scoruri probabilistice și testul Kupiec"), cols(
        "\\[ \\text{LR}_{\\text{UC}}=-2\\ln\\frac{(1-p_0)^{n-x}p_0^{\\,x}}{(1-\\hat p)^{n-x}\\hat p^{\\,x}}\\sim\\chi^2_1,\\quad \\hat p=\\frac xn \\]" + it(
            t("Likelihood ratio (LR) for unconditional coverage (UC); $x$ = hours outside the 90\\% interval out of $n$ = @{test.n_hours|,d}; $p_0=0.10$.",
              "Raportul de verosimilitate (LR) pentru acoperirea necondiționată (UC); $x$ = orele din afara intervalului de 90\\%, din $n$ = @{test.n_hours|,d}; $p_0=0{,}10$."),
            t("Hours of the same day are not independent, so the test is indicative; a test on the daily miss share with Newey--West variance gives $p$ = " + pval("prob.qra.hac_p") + " for QRA.",
              "Orele aceleiași zile nu sînt independente, deci testul este orientativ; testul pe proporția zilnică a depășirilor, cu varianță Newey--West, dă $p$ = " + pval("prob.qra.hac_p") + " pentru QRA."),
            t("Pinball score averaged over 99 quantiles; the continuous ranked probability score $\\approx 2\\times$ this score.",
              "Scorul pinball mediat pe 99 de cuantile; scorul de probabilitate ordonat continuu $\\approx 2\\times$ acest scor."), sep="3pt"),
        table("@{}lrrrr@{}", [t("Method", "Metoda"), t("Pinball", "Pinball"), t("Cov.\\ 50\\%", "Acop.\\ 50\\%"),
                              t("Cov.\\ 90\\%", "Acop.\\ 90\\%"), "Kupiec"],
              [[k_, fmt(pr[kk]["aps"], ".2f", lang), fmt(pr[kk]["c50"], ".1f", lang), fmt(pr[kk]["c90"], ".1f", lang),
                fmt(pr[kk]["kupiec"], ".1f", lang)] for kk, k_ in [("qra", "QRA"), ("cp", "CP"), ("hs", "HS")]],
              size="footnotesize", stretch="1.2"), "0.50", "0.47"), "footnotesize", cite="(Kupiec, 1995; Gneiting \\& Raftery, 2007, JASA)")

    co, cm = N["coint"], N["coint_m"]
    D.frame(t("Appendix D: unit-root and cointegration tests in full", "Anexa D: testele de rădăcină unitară și de cointegrare, în detaliu"),
            "\\begin{center}" + table("@{}llrr@{}", [t("Series / pair", "Serie / pereche"), t("Test", "Test"), t("Statistic", "Statistica"), t("$p$ / crit.\\ 5\\%", "$p$ / crit.\\ 5\\%")], [
                [t("RO, HU, DE-LU daily levels", "RO, HU, DE-LU, niveluri zilnice"), "ADF $p$", "--", fmt(co["adf_RO"], ".3f", lang) + ", " + fmt(co["adf_HU"], ".3f", lang) + ", " + fmt(co["adf_DE_LU"], ".3f", lang)],
                ["RO--HU", "Engle--Granger", fmt(co["HU"]["eg"], ".2f", lang), fmt(co["HU"]["eg_cv5"], ".2f", lang)],
                ["RO--HU", "Johansen $r=0$ / $r\\le1$", fmt(co["HU"]["tr0"], ".1f", lang) + " / " + fmt(co["HU"]["tr1"], ".2f", lang), fmt(co["HU"]["tr0_cv"], ".2f", lang) + " / " + fmt(co["HU"]["tr1_cv"], ".2f", lang)],
                ["RO--DE-LU", "Engle--Granger", fmt(co["DE_LU"]["eg"], ".2f", lang), fmt(co["DE_LU"]["eg_cv5"], ".2f", lang)],
                [t("RO price, TTF, monthly levels", "preț RO, TTF, niveluri lunare"), "ADF $p$", "--", fmt(cm["adf_price"], ".3f", lang) + ", " + fmt(cm["adf_ttf"], ".3f", lang)],
                [t("hydro minus monthly mean", "hidro minus media lunii"), "ADF $p$", "--", fmt(cm["adf_hyds"], ".3f", lang)],
                [t("price--TTF", "preț--TTF"), "Engle--Granger", fmt(cm["eg1"], ".2f", lang), fmt(cm["eg1_cv5"], ".2f", lang)],
                [t("price--TTF--hydro", "preț--TTF--hidro"), "Engle--Granger", fmt(cm["eg2"], ".2f", lang), fmt(cm["eg2_cv5"], ".2f", lang)],
                [t("price--TTF", "preț--TTF"), "Johansen $r=0$ / $r\\le1$", fmt(cm["tr0"], ".2f", lang) + " / " + fmt(cm["tr1"], ".2f", lang), fmt(cm["tr0_cv"], ".2f", lang) + " / " + fmt(cm["tr1_cv"], ".2f", lang)]],
                size="footnotesize", stretch="1.1") + "\\end{center}" + note(
                t("ADF with AIC lags; Johansen with a constant, 6 lagged differences (daily) or 2 (monthly).",
                  "ADF cu numărul de decalaje ales prin AIC; Johansen cu constantă și 6 diferențe decalate (date zilnice) sau 2 (date lunare)."),
                t("ECM with heteroskedasticity- and autocorrelation-robust standard errors (6 lags), @{coint_m.ecm_n} months, $R^2$ = @{coint_m.ecm_r2|.3f}.",
                  "ECM cu erori standard robuste la heteroscedasticitate și autocorelație (6 decalaje), @{coint_m.ecm_n} " + de("coint_m.ecm_n") + "luni, $R^2$ = @{coint_m.ecm_r2|.3f}.")),
            "small", cite="(Engle \\& Granger, 1987; Johansen, 1991; MacKinnon, 1996)")
    return D


def main(langs):
    ok = True
    for lang in langs:
        name = "lecture2" if lang == "en" else "lecture2_ro"
        out = os.path.join(HERE, name + ".tex")
        D, tex, res, H = autofit(build, out, lang)
        print(f"[{lang}] frames: main {D.n_main} (incl. title and section outlines), total {D.n_frames}; quiz frames {D.quiz}; "
              f"pages {res['pages']}; errors {res['errors']}; overfull>1pt {len(res['overfull'])}")
        for kind, amt, title in res["where"]:
            print(f"     {kind} {amt:6.1f}pt  {title}")
        small = {k: v for k, v in D.used_h.items() if v < 0.40}
        print(f"[{lang}] figure heights (fraction of text height) below 0.40:", small)
        defined = set(ABBR) - ({"UE"} if lang == "en" else {"EU"})
        print(f"[{lang}] acronyms missing from Abbreviations:", acronym_audit(tex, defined, IGNORE))
        bad = first_use_audit(tex, [a for a in defined if a not in UNITS and a != "ISE"])
        print(f"[{lang}] acronyms not spelled out at first use:", [b[0] for b in bad])
        for a, ctx in bad:
            print(f"      {a}: ...{ctx}")
        if res["pages"]:
            contact_sheet(os.path.join(HERE, name + ".pdf"), os.path.join(HERE, name + "_contact_sheet.png"))
        ok &= not res["errors"] and not res["overfull"]
    return ok


if __name__ == "__main__":
    langs = [a for a in sys.argv[1:] if a in ("en", "ro")] or ["en", "ro"]
    sys.exit(0 if main(langs) else 1)
