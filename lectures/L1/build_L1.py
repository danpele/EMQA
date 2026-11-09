r"""
build_L1.py -- Lecture 1 "Energy Markets and Their Data" (EMQA), English and Romanian from one source
======================================================================================================
Writes lectures/L1/lecture1.tex (EN) and lectures/L1/lecture1_ro.tex (RO) from the bilingual slide text in
this file and the numbers in L1_numbers.json (produced by analysis_L1.py), compiles both twice with pdflatex
and checks: 0 LaTeX errors; no overfull box > 1 pt (nothing masked with \hfuzz/\vfuzz/\hbadness); every acronym
in the Abbreviations frame and spelled out at first use; contact sheets for the visual check.

Run (from anywhere):
    python3 lectures/L1/analysis_L1.py
    python3 lectures/L1/build_L1.py            # both languages;  add "en" or "ro" for one

Rules: no computed number is typed by hand (results are @{key} placeholders); hand-typed numbers are
definitions (1.96, 1/24, 15 min, 3.412142, tabulated critical values) and institutional dates.
Each concept frame: one-sentence intuition -> formula with every symbol defined -> real-data example ->
one line tying it to a decision at work. Weron style: claim titles, citation line, underbraced equations,
per-year colour tables, "Experiment yourself" pointers, outline at each section, wrap-up + further reading.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_build import (Deck, Numbers, acronym_audit, autofit, block, cols, contact_sheet,  # noqa: E402
                        first_use_audit, fmt, heat, hier, items, seq, table)

ZONES = ["RO", "BG", "HU", "DE_LU"]
ZN = {"RO": "RO", "BG": "BG", "HU": "HU", "DE_LU": "DE-LU"}


def it(*xs, sep="1pt"):
    """Bullets: a string is split by hier() (first clause = level 1, the rest = level 2); a tuple
    (head, sub1, sub2, ...) gives an explicit level-1 head with its level-2 bullets."""
    sep = "1pt" if float(sep.replace("pt", "")) > 1 else sep      # nested bullets need the vertical space

    def one(x):
        if isinstance(x, tuple):
            return (x[0] + "\n    \\begin{itemize}\\setlength{\\itemsep}{0pt}\n" +
                    "\n".join("      \\item " + (s[0].upper() + s[1:] if s[0].islower() else s) for s in x[1:] if s) + "\n    \\end{itemize}")
        return hier(x)
    return (f"\\begin{{itemize}}\\setlength{{\\itemsep}}{{{sep}}}\n" + "\n".join("  \\item " + one(x) for x in xs if x) +
            "\n\\end{itemize}")


def note(*xs):
    """A note under a table, as small bullets (course rule: no text outside bullets)."""
    return ("\n\\par\\vspace{0.5mm}{\\scriptsize " +
            items(*xs, opt="\\setlength{\\itemsep}{0pt}", nest=False) + "}")


def strip0(s):
    for z in ("{,}00", ".00"):
        if s.endswith(z):
            return s[:-len(z)]
    return s


# =============================================================================
# Abbreviations (EN, RO) -- used by both audits
# =============================================================================
ABBR = {
    "ACER": ("EU Agency for the Cooperation of Energy Regulators", "Agenția Uniunii Europene pentru Cooperarea Autorităților de Reglementare din Domeniul Energiei"),
    "ACF": ("autocorrelation function", "funcția de autocorelație"),
    "ADF": ("augmented Dickey--Fuller test", "testul Dickey--Fuller augmentat"),
    "AIC": ("Akaike information criterion", "criteriul informațional Akaike"),
    "ANRE": ("Romanian Energy Regulatory Authority", "Autoritatea Națională de Reglementare în Domeniul Energiei"),
    "AR": ("autoregressive model", "model autoregresiv"),
    "ARX": ("autoregressive model with exogenous variables", "model autoregresiv cu variabile exogene"),
    "BG": ("Bulgaria (bidding zone)", "Bulgaria (zonă de ofertare)"),
    "CET": ("Central European Time", "ora Europei Centrale"),
    "CEST": ("Central European Summer Time", "ora de vară a Europei Centrale"),
    "DE-LU": ("Germany--Luxembourg bidding zone", "zona de ofertare Germania--Luxemburg"),
    "DST": ("daylight saving time", "ora de vară"),
    "ECB": ("European Central Bank", "Banca Centrală Europeană"),
    "EET": ("Eastern European Time (Romania)", "ora Europei de Est (România)"),
    "ENTSO-E": ("European Network of Transmission System Operators for Electricity", "Rețeaua europeană a operatorilor de transport și sistem pentru energie electrică"),
    "EPEX": ("EPEX SPOT power exchange", "bursa de energie EPEX SPOT"),
    "EU": ("European Union", None),
    "UE": (None, "Uniunea Europeană"),
    "EUPHEMIA": ("Pan-European Hybrid Electricity Market Integration Algorithm", "algoritmul hibrid paneuropean de integrare a piețelor de energie electrică"),
    "EWMA": ("exponentially weighted moving average", "medie mobilă ponderată exponențial"),
    "HAC": ("heteroskedasticity- and autocorrelation-consistent", "robust la heteroscedasticitate și autocorelație"),
    "HU": ("Hungary (bidding zone)", "Ungaria (zonă de ofertare)"),
    "HUPX": ("Hungarian Power Exchange", "bursa de energie din Ungaria"),
    "IBEX": ("Independent Bulgarian Energy Exchange", "bursa independentă de energie din Bulgaria"),
    "IDA": ("intraday auction", "licitație intrazilnică"),
    "IQR": ("interquartile range", "abatere intercuartilică"),
    "JAO": ("Joint Allocation Office", "Joint Allocation Office (alocarea capacității pe termen lung)"),
    "JB": ("Jarque--Bera test", "testul Jarque--Bera"),
    "KPSS": ("Kwiatkowski--Phillips--Schmidt--Shin test", "testul Kwiatkowski--Phillips--Schmidt--Shin"),
    "CNCAN": ("National Commission for Nuclear Activities Control (Romania)", "Comisia Națională pentru Controlul Activităților Nucleare"),
    "ISE": ("Fraunhofer Institute for Solar Energy Systems", "Institutul Fraunhofer pentru Sisteme de Energie Solară"),
    "PPA": ("power purchase agreement", "contract de achiziție de energie pe termen lung"),
    "MA": ("moving average", "medie mobilă"),
    "MAD": ("median absolute deviation", "abaterea absolută mediană"),
    "MAE": ("mean absolute error", "eroarea absolută medie"),
    "MTU": ("market time unit", "interval de tranzacționare"),
    "NEMO": ("Nominated Electricity Market Operator", "operator desemnat al pieței de energie electrică"),
    "OLS": ("ordinary least squares", "metoda celor mai mici pătrate"),
    "OPCOM": ("Romanian electricity and gas market operator", "operatorul pieței de energie electrică și gaze naturale din România"),
    "OTC": ("over the counter (bilateral)", "tranzacții bilaterale negociate direct"),
    "PACF": ("partial autocorrelation function", "funcția de autocorelație parțială"),
    "PZU": ("Piața pentru Ziua Următoare (day-ahead market)", "piața pentru ziua următoare"),
    "REMIT": ("EU Regulation 1227/2011 on wholesale energy market integrity and transparency",
              "Regulamentul UE 1227/2011 privind integritatea și transparența pieței angro de energie"),
    "RO": ("Romania (bidding zone)", "România (zonă de ofertare)"),
    "RoR": ("run-of-river hydro", "hidrocentrale pe firul apei"),
    "SDAC": ("Single Day-Ahead Coupling", "cuplarea unică a piețelor pentru ziua următoare"),
    "SES": ("simple exponential smoothing", "netezire exponențială simplă"),
    "SIDC": ("Single Intraday Coupling", "cuplarea unică a piețelor intrazilnice"),
    "SMA": ("simple moving average", "medie mobilă simplă"),
    "STL": ("Seasonal--Trend decomposition using Loess", "descompunere sezonieră și de trend prin regresie locală (Loess)"),
    "TSO": ("transmission system operator", "operator de transport și de sistem"),
    "TTF": ("Title Transfer Facility (Dutch gas hub)", "Title Transfer Facility (hub olandez de gaze)"),
    "UTC": ("Coordinated Universal Time", "timpul universal coordonat"),
    "YTD": ("year to date", "de la începutul anului"),
    "EUR": ("euro", "euro"), "RON": ("Romanian leu", "leu românesc"), "USD": ("US dollar", "dolar american"),
    "MW": ("megawatt", "megawatt"), "MWh": ("megawatt-hour", "megawatt-oră"), "GW": ("gigawatt", "gigawatt"),
    "TWh": ("terawatt-hour", "terawatt-oră"), "MMBtu": ("million British thermal units", "milion de unități termice britanice"),
    "bbl": ("barrel (159 litres)", "baril (159 de litri)"),
}
UNITS = {"EUR", "USD", "MW", "MWh", "GW", "TWh", "MMBtu", "bbl", "RON"}
# journal and series codes inside citations only; everything else must be in the Abbreviations list and spelled out
IGNORE = {"PICBE", "LR", "MM", "MT", "US", "EMQA", "IJF", "ENEECO", "APEN", "JASA", "TPWRS", "IEEE", "JOS", "JAE", "BZ", "IIF", "OK", "II", "CO", "SPOT"}


def build(lang, H=None):
    V = Numbers(os.path.join(HERE, "L1_numbers.json"), lang)
    N = V.N
    ROMISS = ", ".join(fmt(x, "date", lang) for x in N["data"]["ro_missing"])
    Y = N["cutoff"]["year"]
    N["Y"], N["YP"] = Y, Y - 1
    GWM = fmt(N["mix"][str(Y - 1)]["load_twh"] * 1000 / (366 if (Y - 1) % 4 == 0 else 365) / 24, ".1f", lang)
    D = Deck(1, "Energy Markets and Their Data" if lang == "en" else "Piețele de energie și datele lor", V, lang, heights=H)
    t = D.t
    f = V.fmt
    ro = lang == "ro"
    MON = ([None, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
            "November", "December"] if not ro else
           [None, "ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie",
            "octombrie", "noiembrie", "decembrie"])
    mlast = MON[N["cutoff"]["month"]]
    jan_last = t(f"Jan--{mlast[:3]}", f"ian.--{mlast[:3]}.")
    NB = t("notebook", "notebook-ul Jupyter")

    def de(key):
        v = int(V.get(key))
        return "de " if ro and v >= 20 and (v % 100 >= 20 or v % 100 == 0) else ""

    def pval(p):
        return r"$<$0{,}001" if (p < 0.001 and ro) else (r"$<$0.001" if p < 0.001 else fmt(p, ".3f", lang))

    # ------------------------------------------------------------------ front matter
    D.parts.append("% END-FRONT-MATTER\n")
    D.frame(t("Learning objectives", "Obiectivele cursului"), it(
        t("Explain how one day-ahead auction sets a price for every hour (now every quarter-hour) and how European "
          "market coupling links Romania with its neighbours.",
          "Să explicați cum stabilește licitația pentru ziua următoare un preț pentru fiecare oră (acum, pentru fiecare "
          "sfert de oră) și cum leagă cuplarea europeană a piețelor România de vecinii săi."),
        t("Compute and read the Romanian generation mix from metered data, with its coverage.",
          "Să calculați și să interpretați mixul de producție al României pe baza datelor măsurate, precizînd gradul lor "
          "de acoperire."),
        t("Recognise the stylized facts of power prices on real data and choose a transformation that works when "
          "prices are zero or negative.",
          "Să recunoașteți, pe date reale, faptele stilizate ale prețurilor energiei electrice și să alegeți o transformare "
          "potrivită atunci cînd prețurile sînt nule sau negative."),
        t("Use the core time-series toolkit and the naive benchmark that every forecast must beat.",
          "Să utilizați instrumentele de bază ale analizei seriilor de timp și prognoza naivă, reperul pe care orice model "
          "trebuie să-l depășească."),
        t("Read six current episodes quantitatively, from the dry year 2025 to Bulgaria's new batteries in @{Y}.",
          "Să analizați cantitativ șase episoade recente, de la seceta din 2025 pînă la noile baterii din Bulgaria, în @{Y}."),
        sep="4pt"))

    ab = sorted([(k, v) for k, v in ABBR.items() if v[0 if not ro else 1] is not None], key=lambda kv: kv[0].lower())
    third = (len(ab) + 2) // 3

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

    D.frame(t("Real data only: what we use and where it ends", "Numai date reale: surse și perioadă acoperită"), note(t("Exchanges: Romanian electricity and gas market operator (OPCOM), Independent Bulgarian Energy Exchange (IBEX), "
               "Hungarian Power Exchange (HUPX), European Power Exchange (EPEX SPOT); European Network of Transmission System "
               "Operators for Electricity (ENTSO-E).",
               "Burse: operatorul pieței de energie electrică și gaze naturale din România (OPCOM), bursa independentă de energie din "
               "Bulgaria (IBEX), bursa de energie din Ungaria (HUPX), European Power Exchange (EPEX SPOT); Rețeaua europeană a "
               "operatorilor de transport și de sistem pentru energie electrică (ENTSO-E).")) + "\\vspace{-1mm}\n" + table(
        "@{}p{0.31\\textwidth}p{0.11\\textwidth}p{0.36\\textwidth}p{0.13\\textwidth}@{}",
        [t("Series", "Serie"), t("Frequency", "Frecvență"), t("Source", "Sursă"), t("From", "Început")],
        [[t("Day-ahead prices: Romania (RO), Bulgaria (BG), Hungary (HU), Germany--Luxembourg (DE-LU)",
            "Prețurile pentru ziua următoare: România (RO), Bulgaria (BG), Ungaria (HU), Germania--Luxemburg (DE-LU)"),
          "15/60 min", t("energy-charts.info (Fraunhofer ISE); prices of the exchanges above",
                         "energy-charts.info (Fraunhofer ISE); prețurile burselor de mai sus"), "@{data.price_first}"],
         [t("Generation by source and consumption, Romania and Bulgaria", "Producția pe surse și consumul, România și Bulgaria"),
          t("hourly", "orară"), t("energy-charts.info, ENTSO-E actual generation", "energy-charts.info, ENTSO-E (producția efectivă)"), "2015-01"],
         [t("Romanian cross-border physical flows", "Fluxurile fizice transfrontaliere ale României"), t("hourly", "orară"),
          "energy-charts.info, ENTSO-E", "@{data.price_first}"],
         [t("Brent crude oil, front-month futures", "Țiței Brent, contractul futures cel mai apropiat"), t("daily", "zilnică"),
          "Yahoo Finance (BZ=F)", "@{data.brent_first}"],
         [t("Title Transfer Facility (TTF) gas, monthly", "Gaze naturale, hubul Title Transfer Facility (TTF)"), t("monthly", "lunară"),
          t("World Bank; European Central Bank (ECB) exchange rates", "Banca Mondială; cursurile de schimb ale Băncii Centrale Europene (ECB)"),
          "2015-01"]], size="scriptsize", stretch="1.0") + "\n\\vspace{0.5mm}\n" + it(
        t("\\textbf{Cut-off: @{cutoff.end|date}} (last complete month), downloaded @{data.download|date}; "
          "``@{Y} year to date (YTD)'' always means " + jan_last + " @{Y}.",
          "\\textbf{Date pînă la @{cutoff.end|date}} (ultima lună completă), descărcate la @{data.download|date}; "
          "„@{Y}, de la începutul anului (YTD)” înseamnă întotdeauna " + jan_last + " @{Y}."),
        t("Missing values stay missing: never interpolated, never counted as zero, and coverage is always reported.",
          "Valorile lipsă nu se interpolează și nu devin zero, iar gradul de acoperire se raportează mereu."),
        sep="2pt") + D.bottom(None, NB + " \\S1"))

    # ------------------------------------------------------------------ 1 markets
    D.section(t("Power markets in Romania and Europe", "Piețele de energie electrică din România și Europa"))
    D.subsection(t("How the day-ahead auction works", "Cum funcționează licitația pentru ziua următoare"))
    D.concept(
        t("The day-ahead auction: a clearing price for each quarter-hour", "Prețul de închidere a pieței: intersecția cererii cu oferta"),
        t("Sellers and buyers send price--quantity bids; the exchange finds the price at which energy offered equals "
          "energy demanded, and every accepted trade is paid that single price.",
          "Vînzătorii și cumpărătorii depun oferte de preț și cantitate; bursa determină prețul la care cantitatea oferită egalează "
          "cantitatea cerută, iar toate tranzacțiile acceptate se decontează la acest preț unic."),
        "\\[ p_t^{*}=\\min\\big\\{p:\\ \\underbrace{S_t(p)}_{" + t("\\text{supply curve}", "\\text{curba ofertei}") +
        "}\\ \\ge\\ \\underbrace{D_t(p)}_{" + t("\\text{demand curve}", "\\text{curba cererii}") + "}\\big\\} \\]" +
        "\\where{" + t("$t$ = delivery quarter-hour (hour before Oct 2025); $S_t(p)$ = energy offered at prices $\\le p$, plants "
                       "sorted by cost (the \\emph{merit order}: renewables and nuclear at the bottom, gas near the top); $D_t(p)$ = energy bought at prices $\\ge p$; "
                       "$p_t^{*}$ = clearing price, in euro per megawatt-hour (EUR/MWh).",
                       "$t$ = sfertul de oră de livrare (ora, pînă în oct. 2025); $S_t(p)$ = oferta la prețuri $\\le p$, cu "
                       "centralele ordonate după cost (\\emph{ordinea de merit}: regenerabile și nuclear la bază, gaze spre vîrf); "
                       "$D_t(p)$ = cererea la prețuri $\\ge p$; "
                       "$p_t^{*}$ = prețul de închidere a pieței, în euro pe megawatt-oră (EUR/MWh).") + "}",
        it(t("\\textbf{On our data}: Romania's day-ahead market, Piața pentru Ziua Următoare (PZU), run by the Romanian market "
             "operator (OPCOM), cleared on average at @{cy.mean.RO|.2f} EUR/MWh in " + jan_last + " @{Y}.",
             "\\textbf{Conform datelor}: prețul mediu pe piața pentru ziua următoare (PZU), administrată de operatorul pieței "
             "(OPCOM), a fost de @{cy.mean.RO|.2f} EUR/MWh în " + jan_last + " @{Y}."),
            t("Reservoir hydro bids its ``water value'' (opportunity cost) and often sets the Romanian price.",
              "Hidrocentralele cu lac de acumulare ofertează la „valoarea apei” (cost de oportunitate) și fixează adesea prețul în România."),
            (t("\\textbf{Two extremes}", "\\textbf{Două extreme}"),
             t("demand on the steep part: \\textbf{spikes}", "cererea ajunge pe porțiunea abruptă: \\textbf{salturi de preț (spikes)}"),
             t("inflexible output and sun above demand: \\textbf{negative prices}",
               "producția inflexibilă și cea solară depășesc cererea: \\textbf{prețuri negative}")), sep="2pt"),
        t("on PZU a supplier pays the price of the most expensive plant needed, not the average cost.",
          "pe PZU, un furnizor plătește prețul fixat de centrala marginală, nu costul mediu al sistemului."),
        wl="0.45", wr="0.52",
        cite="(Weron, 2014, IJF; Maciejowska, Uniejewski \\& Weron, 2023, Oxford Res.\\ Enc.)")
    D.frame(t("The merit order: how the price is formed", "Mecanismul ordinii de merit: cum se formează prețul"), it(
        (t("\\textbf{Supply}: sell offers sorted from cheapest to dearest", "\\textbf{Oferta}: ofertele de vînzare sînt ordonate de la cea mai ieftină la cea mai scumpă"),
         t("each producer offers near its marginal cost, the cost of one more MWh", "fiecare producător ofertează în jurul costului marginal, adică al costului unui MWh în plus"),
         t("usual order: wind, solar and nuclear (marginal cost near zero), run-of-river hydro, lignite, gas",
           "ordinea obișnuită: eolian, solar și nuclear (cost marginal aproape zero), hidro pe firul apei, lignit, gaze"),
         t("reservoir hydro offers at its water value, the price it expects to get later for the same water",
           "hidrocentralele cu lac ofertează la valoarea apei, adică prețul pe care îl așteaptă mai tîrziu pentru aceeași apă")),
        (t("\\textbf{Demand}: buy bids sorted from highest to lowest price", "\\textbf{Cererea}: ofertele de cumpărare sînt ordonate de la prețul cel mai mare la cel mai mic"),
         t("most consumption is bought at any price, so the demand curve is almost vertical",
           "cea mai mare parte a consumului se cumpără la orice preț, de aceea curba cererii este aproape verticală")),
        (t("\\textbf{Price}: set by the last accepted offer, the marginal one", "\\textbf{Prețul}: îl stabilește ultima ofertă acceptată, cea marginală"),
         t("every accepted seller receives it, also those with lower costs", "toți vînzătorii acceptați primesc acest preț, inclusiv cei cu costuri mai mici"),
         t("their difference between price and cost pays for capacity (inframarginal rent)",
           "diferența dintre preț și costul lor le acoperă investiția (renta inframarginală)")),
        (t("\\textbf{Why prices move}", "\\textbf{De ce variază prețul}"),
         t("sun and wind shift the supply to the right: lower price", "soarele și vîntul deplasează oferta spre dreapta: prețul scade"),
         t("evening demand or a missing reactor moves the crossing to the steep, gas-fired part: higher price",
           "cererea de seară sau oprirea unui reactor mută intersecția pe porțiunea abruptă, a centralelor pe gaze: prețul crește")), sep="1pt") +
        D.bottom(t("the price of a quarter-hour is the cost of its most expensive accepted offer, not the average cost of the system.",
                   "prețul unui sfert de oră este dat de cea mai scumpă ofertă acceptată, nu de costul mediu al sistemului.")),
        "footnotesize", cite="(Weron, 2014, IJF; Maciejowska, Uniejewski \\& Weron, 2023, Oxford Res.\\ Enc.)")
    D.figframe(t("The merit order on real OPCOM curves, @{merit.day|date}", "Ordinea de merit pe curbele reale OPCOM, @{merit.day|date}"),
               None, None, "merit_opcom", [
                   (t("Same day, two prices: the supply curve changes with the sun", "Aceeași zi, două prețuri: oferta se schimbă cu soarele"),
                    t("midday: @{merit.mid.q_le0|,.0f} MW offered at zero or negative prices, price @{merit.mid.price|.2f} EUR/MWh",
                      "la amiază: @{merit.mid.q_le0|,.0f} MW oferiți la preț zero sau negativ, preț @{merit.mid.price|.2f} EUR/MWh"),
                    t("evening: no sun, @{merit.eve.net_imp|,.0f} MW of net imports in the supply, price @{merit.eve.price|.2f} EUR/MWh",
                      "seara: fără soare, @{merit.eve.net_imp|,.0f} MW import net în ofertă, preț @{merit.eve.price|.2f} EUR/MWh"))],
               job=t("a buyer who can shift consumption from evening to midday pays the lower clearing price.",
                     "un consumator care își mută consumul de seara la amiază plătește prețul de închidere mai mic."),
               tryit=NB + " \\S1", height="0.62\\textheight",
               cite=t("(OPCOM, PZU aggregated curves)", "(OPCOM, curbele agregate PZU)"))

    tl = t
    D.frame(t("One delivery day, step by step", "Etapele tranzacționării pentru o zi de livrare"), """
\\begin{center}
\\begin{tikzpicture}[x=1cm,y=1cm,
  box/.style={draw=MainBlue,fill=BlockGray,rounded corners=2pt,align=center,text width=3.05cm,minimum height=1.3cm,font=\\scriptsize}]
\\draw[-{Latex},thick,MainBlue] (0,0) -- (14.5,0);
\\node[box] at (1.7,1.05) {""" + tl("\\textbf{1. Forward contracts}\\\\ OPCOM centralised markets, over-the-counter (OTC) deals; weeks to years ahead",
                                   "\\textbf{1. Contracte la termen}\\\\ piețele centralizate OPCOM și contracte bilaterale negociate direct (OTC), cu săptămîni sau ani înainte") + """};
\\node[box] at (5.3,1.05) {""" + tl("\\textbf{2. PZU bid}\\\\ gate closure 12:00 Central European Time (CET) on $d-1$ = 13:00 in Bucharest; results published early afternoon",
                                   "\\textbf{2. Oferta pe PZU}\\\\ termen-limită: 12:00, ora Europei Centrale (CET), în ziua $d-1$ (13:00 la București); rezultatele apar la începutul după-amiezii") + """};
\\node[box] at (8.9,1.05) {""" + tl("\\textbf{3. Intraday correction}\\\\ intraday auctions (IDA) and continuous trading until shortly before delivery",
                                   "\\textbf{3. Ajustări intrazilnice}\\\\ licitații intrazilnice (IDA) și tranzacționare continuă pînă aproape de livrare") + """};
\\node[box] at (12.5,1.05) {""" + tl("\\textbf{4. Imbalance}\\\\ Transelectrica, the transmission system operator (TSO), balances the grid; deviations settled per 15 min",
                                    "\\textbf{4. Echilibrare}\\\\ Transelectrica, operatorul de transport și de sistem (TSO), echilibrează sistemul; dezechilibrele se decontează la 15 min") + """};
\\foreach \\x/\\l in {1.7/{""" + tl("weeks--years", "săptămîni--ani") + """}, 5.3/{""" + tl("day $d-1$", "ziua $d-1$") + """}, 8.9/{""" +
        tl("$d-1$ and $d$", "$d-1$ și $d$") + """}, 12.5/{""" + tl("day $d$, real time", "ziua $d$, în timp real") + """}}
  \\node[font=\\scriptsize,below] at (\\x,-0.05) {\\l};
\\end{tikzpicture}
\\end{center}
\\vspace{1mm}
""" + it(
        t("\\textbf{Clocks and money}: Romania runs on Eastern European Time (EET), one hour ahead of CET; the Single Day-Ahead "
          "Coupling (SDAC) clears in EUR, and OPCOM also publishes prices in Romanian lei (RON).",
          "\\textbf{Ora și moneda}: România folosește ora Europei de Est (EET), cu o oră înaintea CET; în cuplarea unică a "
          "piețelor pentru ziua următoare (SDAC), prețurile se exprimă în EUR, iar OPCOM le publică și în lei (RON)."),
        t("\\textbf{Why the order matters}: each step corrects the previous one; what is not covered forward is bought on PZU, "
          "and what is still wrong after intraday trading is settled as imbalance.",
          "\\textbf{De ce contează ordinea}: fiecare etapă o corectează pe cea anterioară; ce nu s-a contractat la termen se "
          "cumpără pe PZU, iar ce rămîne neacoperit după piața intrazilnică se decontează ca dezechilibru."),
        sep="2pt") + D.bottom(t("a trader hedges forward, bids on PZU before 13:00 Bucharest time, fixes forecast "
                                "errors intraday and pays what is left as imbalance.",
                                "traderul își acoperă riscul la termen, licitează pe PZU pînă la ora 13:00 "
                                "(ora Bucureștiului), corectează erorile pe piața intrazilnică și decontează dezechilibrul rămas.")),
        "footnotesize", cite="(Maciejowska, Uniejewski \\& Weron, 2023, Oxford Res.\\ Enc.; OPCOM; Transelectrica)")

    D.frame(t("Who sets the rules: operators, regulators, price limits, disclosure",
              "Cine stabilește regulile: operatori, reglementatori, limite de preț, transparență"), it(
        (t("\\textbf{Who is who}", "\\textbf{Cine ce face}"),
         t("OPCOM: the Nominated Electricity Market Operator (NEMO); it runs PZU and the intraday market",
           "OPCOM: operatorul desemnat al pieței de energie electrică (NEMO); administrează PZU și piața intrazilnică"),
         t("Transelectrica (TSO): runs the grid in real time and settles imbalances",
           "Transelectrica (TSO): conduce sistemul în timp real și decontează dezechilibrele"),
         t("the Romanian Energy Regulatory Authority (ANRE): sets the national rules and licenses market participants",
           "Autoritatea Națională de Reglementare în Domeniul Energiei (ANRE): stabilește regulile și licențiază participanții")),
        (t("\\textbf{Disclosure}", "\\textbf{Transparență}"),
         t("the European Union (EU) Regulation on wholesale energy market integrity and transparency (REMIT): inside information "
           "must be published promptly",
           "Regulamentul Uniunii Europene (UE) privind integritatea și transparența pieței angro de energie (REMIT): "
           "informațiile privilegiate se publică fără întîrziere"),
         t("for example, unplanned outages of large plants; such messages move PZU prices",
           "de exemplu, opririle neplanificate ale centralelor mari; asemenea informații influențează prețul PZU"),
         t("the EU Agency for the Cooperation of Energy Regulators (ACER) monitors the market for abuse",
           "Agenția UE pentru Cooperarea Autorităților de Reglementare din Domeniul Energiei (ACER) supraveghează piața pentru a depista abuzurile")),
        (t("\\textbf{Price limits}", "\\textbf{Limite de preț}"),
         t("SDAC harmonised minimum: $-500$ EUR/MWh; $-600$ for delivery from 29 May 2026 (OPCOM)",
           "prețul minim armonizat în SDAC: $-500$ EUR/MWh; $-600$ pentru livrările începînd cu 29 mai 2026 (OPCOM)"),
         t("a series that touches the floor is censored there: the true willingness to pay was even lower",
           "o serie care atinge pragul este cenzurată: prețul de echilibru ar fi fost și mai mic")),
        sep="2pt") + D.bottom(t("read REMIT messages before bidding; an unplanned outage announced in time changes the PZU price.",
                                "citiți mesajele REMIT înainte de a licita; o oprire neplanificată anunțată la timp schimbă prețul PZU.")),
        "footnotesize", cite=t("(OPCOM; ANRE; ACER; Regulation (EU) 1227/2011)", "(OPCOM; ANRE; ACER; Regulamentul (UE) 1227/2011)"))

    D.subsection(t("Market coupling and the 15-minute market time unit", "Cuplarea piețelor și intervalul de 15 minute"))
    D.concept(
        t("Coupling lets power flow to the higher price until the network limit binds",
          "Cuplarea piețelor: exporturi spre zonele cu prețuri mari, pînă la limita rețelei"),
        t("Europe runs one joint day-ahead auction; cheap zones export to expensive ones until a network limit binds, "
          "and only then do prices differ.",
          "Europa organizează o singură licitație comună pentru ziua următoare; zonele cu prețuri mici exportă către cele cu "
          "prețuri mari pînă la atingerea unei limite de rețea și abia atunci prețurile se separă."),
        "\\[ \\max\\sum_{z}\\Big[\\underbrace{\\textstyle\\int_0^{d_z}\\!D_z^{-1}}_{" + t("\\text{buyers' value}", "\\text{valoare}") +
        "}-\\underbrace{\\textstyle\\int_0^{s_z}\\!S_z^{-1}}_{" + t("\\text{sellers' cost}", "\\text{cost}") +
        "}\\Big]\\ " + t("\\text{s.t. }", "\\text{a.î. }") + "\\underbrace{\\mathbf{flows}\\in\\mathcal F}_{" + t("\\text{network limits}", "\\text{limitele rețelei}") + "} \\]" +
        "\\where{" + t("$z$ = bidding zone; $d_z, s_z$ = energy bought and sold in $z$; $\\mathcal F$ = feasible exchanges; "
                       "if no limit binds, $p_z=p_{z'}$, otherwise prices separate.",
                       "$z$ = zona de ofertare; $d_z, s_z$ = energia cumpărată, respectiv vîndută în $z$; $\\mathcal F$ = "
                       "schimburile fezabile; dacă nicio limită nu este atinsă, $p_z=p_{z'}$, altfel prețurile se separă.") + "}",
        it(t("\\emph{Simplified picture}: one capacity per border; since 8 Jun 2022 Romania--Hungary is in the Core region's "
             "\\emph{flow-based} allocation (limits on critical network elements); Romania--Bulgaria keeps a per-border limit.",
             "\\emph{Imagine simplificată}: o capacitate pe fiecare graniță; din 8 iunie 2022, la granița România--Ungaria se aplică "
             "alocarea \\emph{bazată pe fluxuri} din regiunea Core; la granița "
             "România--Bulgaria se păstrează alocarea capacității pe graniță."),
           t("Equal prices do not prove an uncongested border; a gap does not say which line is full.",
             "Prețurile egale nu dovedesc absența congestiilor pe interconexiune; o diferență de preț nu arată ce linie și-a atins limita."),
           t("Scheduled exchanges differ from physical flows; long-term rights are sold by the Joint Allocation Office (JAO).",
             "Schimburile programate diferă de fluxurile fizice; drepturile pe termen lung se alocă prin Joint Allocation Office (JAO)."),
           sep="2pt"),
        t("a trader on RO--HU flows earns the price spread only when cross-border capacity binds.",
          "pe RO--HU, un trader cîștigă din diferența de preț doar cînd interconexiunea este saturată."),
        cite=t("(Weron, 2014, IJF; JAO; Core flow-based market coupling)", "(Weron, 2014, IJF; JAO; cuplarea bazată pe fluxuri Core)"),
        wl="0.45", wr="0.52")

    MS = [("2014", t("Romania coupled with Czechia, Slovakia, Hungary (4M Market Coupling)", "România se cuplează cu Cehia, Slovacia și Ungaria (4M Market Coupling)")),
          ("19 Nov 2019" if not ro else "19 nov. 2019", t("joins Single Intraday Coupling (SIDC)", "aderarea la cuplarea unică a piețelor intrazilnice (SIDC)")),
          ("17 Jun 2021" if not ro else "17 iun. 2021", t("joins Single Day-Ahead Coupling via the 4M interim coupling", "aderarea la SDAC, prin cuplarea interimară 4M")),
          ("27 Oct 2021" if not ro else "27 oct. 2021", t("Bulgaria--Romania border coupled in SDAC", "cuplarea graniței Bulgaria--România în SDAC")),
          ("8 Jun 2022" if not ro else "8 iun. 2022", t("Core flow-based allocation (Romania--Hungary)", "alocarea bazată pe fluxuri în regiunea Core (România--Ungaria)")),
          ("Mar 2025" if not ro else "mar. 2025", t("Romanian borders in intraday auctions (IDA)", "granițele României intră în licitațiile intrazilnice")),
          ("1 Oct 2025" if not ro else "1 oct. 2025", t("15-minute market time unit in SDAC", "intervalul de 15 minute în SDAC"))]
    xs = [1.1 + i * 2.0 for i in range(len(MS))]
    tik = "\\begin{center}\\begin{tikzpicture}[x=1cm,y=1cm]\n\\draw[-{Latex},thick,MainBlue] (0,0) -- (14.1,0);\n"
    for i, (x, (dte, txt)) in enumerate(zip(xs, MS)):
        yv = 1.15 if i % 2 == 0 else -1.15
        tik += (f"\\fill[MainBlue] ({x:.2f},0) circle (2.2pt);\\draw[MainBlue] ({x:.2f},0) -- ({x:.2f},{yv * 0.55:.2f});\n"
                f"\\node[align=center,text width=2.25cm,font=\\scriptsize] at ({x:.2f},{yv:.2f}) {{\\textbf{{{dte}}}\\\\ {txt}}};\n")
    tik += "\\end{tikzpicture}\\end{center}"
    D.frame(t("Ten years of coupling: from four countries to one European auction", "Zece ani de cuplare: de la patru țări la o licitație europeană"),
            "\\vspace{0.5mm}" + tik + "\n\\vspace{0.5mm}\n" + it(
                t("Prices are computed by the Pan-European Hybrid Electricity Market Integration Algorithm (EUPHEMIA).",
                  "Prețurile se calculează cu algoritmul hibrid paneuropean de integrare a piețelor de energie electrică (EUPHEMIA)."),
                t("Each step changed the data: new neighbours, new products, a finer resolution; check the date before comparing periods.",
                  "Fiecare etapă a schimbat datele: vecini noi, produse noi, o rezoluție mai fină; verificați data înainte de a compara perioade.")),
            "small", cite=t("(OPCOM press releases 2019--2025; IBEX/OPCOM, 27 Oct 2021; JAO)", "(comunicate OPCOM 2019--2025; IBEX/OPCOM, 27 oct. 2021; JAO)"))

    D.concept(
        t("Since 1 October 2025 a trading day has 96 prices, not 24", "Din 1 octombrie 2025, o zi are 96 de prețuri, nu 24"),
        t("The market time unit (MTU) shrank from one hour to 15 minutes, so every count of hours must be converted.",
          "Intervalul de tranzacționare (MTU) s-a redus de la o oră la 15 minute, așa că numărul intervalelor trebuie convertit "
          "în ore echivalente."),
        "\\[ \\bar p_d=\\frac{1}{M_d}\\sum_{m=1}^{M_d}p_{d,m},\\qquad H_y=\\sum_{t\\in y}\\underbrace{\\mathbb 1\\{p_t<0\\}}_{" +
        t("\\text{1 if negative}", "\\text{1 dacă } p_t<0") + "}\\cdot\\underbrace{\\Delta_t/60}_{" +
        t("\\text{length in hours}", "\\text{durata în ore}") + "} \\]" +
        "\\where{" + t("$p_{d,m}$ = price of MTU $m$ on day $d$; $M_d$ = MTUs that day: 96 since Oct 2025, 24 before ($\\pm$1 "
                       "hour on the daylight saving time (DST) days); $\\bar p_d$ = \\emph{daily base price}; "
                       "$\\Delta_t\\in\\{60,15\\}$ = MTU length in minutes; $H_y$ = hour-equivalents in year $y$.",
                       "$p_{d,m}$ = prețul intervalului $m$ din ziua $d$; $M_d$ = numărul de intervale din zi: 96 din oct. "
                       "2025, 24 înainte ($\\pm$1 oră la schimbarea orei de vară (DST)); "
                       "$\\bar p_d$ = \\emph{prețul mediu zilnic al energiei în bandă}; $\\Delta_t\\in\\{60,15\\}$ = durata intervalului, în minute; "
                       "$H_y$ = numărul de ore echivalente din anul $y$.") + "}",
        it((t("\\textbf{On our data}", "\\textbf{Conform datelor}"),
            t("@{data.n_mtu_60|,d} hourly MTUs until Sep 2025, @{data.n_mtu_15|,d} quarter-hours since",
              "@{data.n_mtu_60|,d} " + de("data.n_mtu_60") + "intervale orare pînă în sep. 2025 și @{data.n_mtu_15|,d} " +
              de("data.n_mtu_15") + "sferturi de oră de atunci"),
            t(jan_last + " @{Y}: @{neg.n_mtu.RO.@{Y}|,d} negative quarter-hours in Romania = @{neg.hours.RO.@{Y}|.2f} h",
              jan_last + " @{Y}: @{neg.n_mtu.RO.@{Y}|,d} " + de(f"neg.n_mtu.RO.{Y}") + "sferturi de oră cu preț negativ în "
              "România, adică @{neg.hours.RO.@{Y}|.2f} h"),
            t("counting them as hours would overstate the duration by a factor of 4", "numărate ca ore, durata ar fi supraevaluată de 4 ori"))),
        t("always ask ``hours or quarter-hours?'' before comparing years.",
          "întrebați mereu „ore sau sferturi de oră?” înainte de a compara anii între ei."),
        tryit=NB + " \\S1", cite=t("(OPCOM, 1 Oct 2025)", "(OPCOM, 1 oct. 2025)"))
    D.subsection(t("What Romania generates", "Ce produce România"))
    D.chart(t("Romania's power: hydro, nuclear, gas and coal --- with solar rising fast",
              "Producția României: hidro, nuclear, gaze, cărbune și tot mai mult solar"), "mix_ro_annual", [
        t("Hydro = run-of-river (RoR) + reservoir, coal = lignite + hard coal; black bar = consumption, above the stack it means "
          "net imports; energy summed over reported hours (coverage $\\ge$ @{mix.min_cov_full|.1f}\\% in full years); "
          "metered solar may miss rooftop output.",
          "Hidro = centrale pe firul apei (RoR) + centrale cu lac de acumulare, cărbune = lignit + huilă; bara neagră reprezintă consumul, "
          "iar deasupra coloanei de producție indică import net; energia este însumată pe orele raportate (acoperire $\\ge$ "
          "@{mix.min_cov_full|.1f}\\% în anii compleți); datele solare măsurate pot exclude producția panourilor de pe acoperișuri.")],
        height="0.60\\textheight", tryit=NB + " \\S2", cite=t("(energy-charts.info; data source: ENTSO-E)", "(energy-charts.info; sursa datelor: ENTSO-E)"))

    srcs = ["Hydro", "Nuclear", "Coal", "Gas", "Wind", "Solar", "Biomass"]
    SN = {"Hydro": t("Hydro", "Hidro"), "Nuclear": "Nuclear", "Coal": t("Coal", "Cărbune"), "Gas": t("Gas", "Gaze"),
          "Wind": t("Wind", "Eolian"), "Solar": "Solar", "Biomass": t("Biomass", "Biomasă")}
    ycols = ["2015", "2020", "2023", "2024", "2025"]
    rows = []
    for k in srcs:
        vals = [N["mix"][y][k]["share"] for y in ycols] + [N["mix"]["lfl"][k]["share_prev"], N["mix"]["lfl"][k]["share_ytd"]]
        rows.append([SN[k]] + [seq(v, max(vals), shown=fmt(v, ".1f", lang), max_pct=45) for v in vals])
    rows.append([t("\\textbf{Total TWh}", "\\textbf{Total TWh}")] + [f(f"mix.{y}.total_twh", ".1f") for y in ycols] +
                [f("mix.lfl_tot.prev", ".1f"), f("mix.lfl_tot.ytd", ".1f")])
    rows.append([t("Load TWh", "Consum TWh")] + [f(f"mix.{y}.load_twh", ".1f") for y in ycols] +
                [f("mix.lfl.load.prev", ".1f"), f("mix.lfl.load.ytd", ".1f")])
    rows.append([t("Net imp. TWh", "Import net TWh")] + [f(f"mix.{y}.netimp_twh", ".1f") for y in ycols] +
                [f("mix.lfl_imp.prev", ".1f"), f("mix.lfl_imp.ytd", ".1f")])
    MIXTAB = (table("@{}l" + "r" * 7 + "@{}", [t("Share, \\%", "Pondere, \\%")] + ycols +
              [t("Jan--Oct ", "ian.--oct. ") + "@{YP}", t("Jan--Oct ", "ian.--oct. ") + "@{Y}"], rows, size="footnotesize", stretch="1.1") +
              note(t("Last two columns: hours reported in both years.", "Ultimele două coloane: numai orele raportate în ambii ani."),
                   t("Net imports $>0$: into Romania.", "Import net $>0$: energie intrată în România.")))
    D.figframe(t("Romania: coal shrinks, solar grows, nuclear drops in @{Y}", "România: cărbunele scade, solarul crește, iar nuclearul se reduce în @{Y}"), None, None,
               "mix_shares", [
                   t("Coal output: @{mix.coal_change_pct|.1f}\\% from @{mix.first} to @{mix.last}; metered solar @{mix.solar_x|.1f}$\\times$ over the same years.",
                     "Producția pe cărbune: @{mix.coal_change_pct|.1f}\\% între @{mix.first} și @{mix.last}; în aceeași perioadă, solarul măsurat a crescut de @{mix.solar_x|.1f} ori."),
                   t("Nuclear, " + jan_last + " @{Y} vs @{YP}: @{mix.lfl.Nuclear.chg|+.1f}\\% on hours reported in both years; "
                     "a lower bound: the @{nuclear.missing_days} unreported September days are left out.",
                     "Nuclear, " + jan_last + " @{Y} față de @{YP}: @{mix.lfl.Nuclear.chg|+.1f}\\% pe orele raportate în ambii ani; "
                     "limită inferioară: cele @{nuclear.missing_days} " + de("nuclear.missing_days") + "zile neraportate din septembrie sînt excluse.")],
               job=t("when water or a reactor is missing, another plant sets the price.",
                     "cînd lipsește apa sau un reactor, prețul este stabilit de o altă centrală."),
               tryit=NB + " \\S2", height="0.60\\textheight",
               cite=t("(Romania; energy-charts.info; data source: ENTSO-E)", "(România; energy-charts.info; sursa datelor: ENTSO-E)"))
    D.frame(t("Course structure and models covered", "Structura cursului și modelele studiate"), cols(
        block(t("Course roadmap", "Planul cursului"), "\\begin{enumerate}\\setlength{\\itemsep}{0pt}\\footnotesize\n" + "\n".join(
            "\\item " + x for x in [
                t("\\textbf{Energy markets and their data} (today)", "\\textbf{Piețele de energie și datele lor} (astăzi)"),
                t("Forecasting: classical and expert autoregressive models with exogenous variables (ARX)", "Prognoza: modele clasice și modele autoregresive cu variabile exogene (ARX)"),
                t("Volatility", "Volatilitatea"),
                t("Risk in energy companies: price--volume, cash flow at risk, imbalance, basis",
                  "Riscul în companiile de energie: preț--volum, flux de numerar la risc, dezechilibre, risc de bază"),
                t("Derivatives and hedging, including power purchase agreements", "Derivate și acoperirea riscului, inclusiv contractele de achiziție de energie (PPA)"),
                t("Renewables, storage, flexibility: cannibalisation, negative prices, batteries",
                  "Regenerabile, stocare, flexibilitate: canibalizare, prețuri negative, baterii"),
                t("Machine learning and foundation models for forecasting", "Învățare automată și modele fundaționale pentru prognoză")]) +
            "\n\\end{enumerate}"),
        it((t("\\textbf{Model families}", "\\textbf{Familii de modele}"),
            t("fundamental: supply stack, fuel and carbon cost", "fundamentale: curba ofertei, costul combustibilului și al CO$_2$"),
            t("reduced-form (mean reversion, jumps) and statistical", "de formă redusă (revenire la medie, salturi) și statistice"),
            t("machine learning and hybrids", "învățare automată și modele hibride")),
           (t("\\textbf{Two views of the same data}", "\\textbf{Două perspective asupra acelorași date}"),
            t("univariate: one long series of prices", "univariată: o singură serie lungă de prețuri"),
            t("multivariate: 24 (now 96) daily series, one per period", "multivariată: 24 (acum 96) de serii zilnice, cîte una pe interval")),
           t("Every model must beat the \\textbf{naive benchmark} of Section 3.", "Orice model trebuie să depășească \\textbf{prognoza naivă} din secțiunea 3."),
           sep="2pt"), "0.56", "0.41") +
        D.bottom(t("ask any forecast vendor which family the model belongs to and by how much it beats the naive benchmark.",
                   "întrebați furnizorul de prognoze din ce familie face parte modelul și cu cît depășește prognoza naivă.")),
        "footnotesize", cite="(Weron, 2014, IJF; Ziel \\& Weron, 2018, ENEECO)")

    # ------------------------------------------------------------------ 2 data and stylized facts
    D.section(t("Energy data and stylized facts", "Date din energie și fapte stilizate"))
    D.subsection(t("Units, clocks and clean data", "Unități de măsură, fusuri orare și date curate"))
    D.concept(
        t("Power (MW) and energy (MWh)", "Puterea (MW) și energia (MWh)"),
        t("A megawatt (MW) is how fast energy flows; a megawatt-hour (MWh) is how much flowed, e.g.\\ 1 MW for one hour.",
          "Un megawatt (MW) măsoară puterea, adică ritmul producției sau al consumului; un megawatt-oră (MWh) măsoară "
          "cantitatea de energie, de exemplu 1 MW timp de o oră."),
        "\\[ E=\\frac{1}{10^6}\\sum_{t\\ \\text{" + t("reported", "raportat") + "}}\\underbrace{P_t\\,\\Delta_t}_{\\text{MWh}}\\ [\\text{TWh}] \\]"
        "\\[ \\text{" + t("coverage", "acoperire") + "}=\\frac{\\text{" + t("reported hours", "ore raportate") + "}}{\\text{" +
        t("hours in the period", "ore din perioadă") + "}} \\]" +
        "\\where{" + t("$P_t$ = mean power in interval $t$ (MW); $\\Delta_t$ = its length (h); $E$ = energy in terawatt-hours (TWh), "
                       "$1\\ \\text{TWh}=10^6\\ \\text{MWh}$.",
                       "$P_t$ = puterea medie în intervalul $t$ (MW); $\\Delta_t$ = durata intervalului (h); $E$ = energia, în "
                       "terawați-oră (TWh), $1\\ \\text{TWh}=10^6\\ \\text{MWh}$.") + "}",
        it(t("\\textbf{On our data}: Romania consumed @{mix.@{YP}.load_twh|.2f} TWh in @{YP}, a mean load of " + GWM + " gigawatts (GW).",
             "\\textbf{Conform datelor}: România a consumat @{mix.@{YP}.load_twh|.2f} TWh în @{YP}, adică o putere medie de "
             + GWM + " gigawați (GW)."),
           t("Missing hours are not filled, and every total comes with its coverage.",
             "Orele lipsă nu se completează, iar fiecare total are alături gradul de acoperire."),
           (t("\\textbf{Reference prices}", "\\textbf{Prețuri de referință}"),
            t("base: mean of the delivery day", "în bandă (base): media prețurilor zilei de livrare"),
            t("peak: mean of 08:00--20:00, Monday to Friday", "de vîrf (peak): prețul mediu 08:00--20:00, luni--vineri")),
           t("Gas and oil are quoted in US dollars (USD) per million British thermal units (MMBtu) and per barrel (bbl); "
             "conversion to EUR/MWh: Appendix G.",
             "Gazele și țițeiul se cotează în dolari americani (USD) pe milion de unități termice britanice (MMBtu), respectiv pe "
             "baril (bbl); conversia în EUR/MWh: Anexa G."), sep="0pt"),
        t("a 10 MW baseload contract delivers 240 MWh a day.",
          "un contract de 10 MW în bandă înseamnă 240 MWh livrați pe zi."),
        wl="0.45", wr="0.52", tryit=NB + " \\S1", cite=t("(energy-charts.info; World Bank Commodity Price Data)", "(energy-charts.info; Banca Mondială)"))
    D.figframe(t("One day of Romanian consumption: power in MW, energy in MWh", "O zi de consum în România: puterea în MW, energia în MWh"),
               None, None, "day_load", [
                   (t("\\textbf{The curve} shows power: how much the country draws at each hour (MW)",
                      "\\textbf{Curba} arată puterea: cît consumă țara în fiecare oră (MW)"),
                    t("minimum @{dayload.min_mw|,d} MW at @{dayload.min_h}:00, maximum @{dayload.max_mw|,d} MW at @{dayload.max_h}:00 (CET)",
                      "minimum @{dayload.min_mw|,d} MW la ora @{dayload.min_h}:00, maximum @{dayload.max_mw|,d} MW la ora @{dayload.max_h}:00 (CET)")),
                   (t("\\textbf{The shaded area} is energy: @{dayload.mwh|,d} MWh on @{dayload.day|date}",
                      "\\textbf{Aria colorată} este energia: @{dayload.mwh|,d} MWh pe @{dayload.day|date}"),
                    t("24 hours $\\times$ a mean of @{dayload.mean_mw|,d} MW",
                      "24 de ore $\\times$ o putere medie de @{dayload.mean_mw|,d} MW"))],
               job=t("a supplier buys energy (MWh), while the grid must cover the peak power (MW).",
                     "un furnizor cumpără energie (MWh), iar rețeaua trebuie să acopere puterea de vîrf (MW)."),
               tryit=NB + " \\S1", height="0.50\\textheight",
               cite=t("(Romania; energy-charts.info; data source: ENTSO-E)", "(România; energy-charts.info; sursa datelor: ENTSO-E)"))

    D.frame(t("Clean data (1): delivery day, clock changes, zone changes", "Pregătirea datelor (1): ziua de livrare, schimbarea orei și a zonei"), it(
        t("\\textbf{Clocks}: raw time stamps are in Coordinated Universal Time (UTC); daily statistics use the SDAC delivery day, in "
          "Central European Time (CET) or, in summer, Central European Summer Time (CEST); a UTC day would put one or two hours "
          "into the wrong day.",
          "\\textbf{Fusuri orare}: marcajele temporale din datele brute sînt în timpul universal coordonat (UTC); statisticile zilnice folosesc ziua de "
          "livrare din SDAC, în ora Europei Centrale (CET) sau, vara, în ora de vară a Europei Centrale (CEST); o zi UTC ar muta "
          "una sau două ore în ziua greșită."),
        t("\\textbf{Clock changes}: the last Sunday of March has 23 hours, the last Sunday of October 25; daily means use the "
          "intervals that exist.",
          "\\textbf{Schimbarea orei}: ultima duminică din martie are 23 de ore, ultima duminică din octombrie are 25; mediile "
          "zilnice folosesc intervalele care există efectiv."),
        t("\\textbf{Zone change}: Germany--Austria--Luxembourg was one zone until 30 Sep 2018; our series is spliced there.",
          "\\textbf{Schimbarea zonei}: Germania--Austria--Luxemburg a fost o singură zonă de ofertare pînă la 30 sep. 2018; "
          "seria noastră le îmbină la acea dată."),
        t("Every chart and number is reproduced in the student notebook (notebooks/L1\\_notebook.ipynb); one simulated figure, "
          "clearly labelled, illustrates white noise and the random walk.",
          "Fiecare grafic și fiecare cifră pot fi reproduse în notebook-ul Jupyter al cursului; un singur grafic, marcat ca "
          "atare, folosește date simulate (zgomot alb, mers aleator)."),
        sep="3pt") + D.bottom(None, NB + " \\S1"), "footnotesize", cite="(Lago, Marcjasz, De Schutter \\& Weron, 2021, APEN)")
    D.frame(t("Clean data (2): missing days and series breaks", "Pregătirea datelor (2): zile lipsă și rupturi de serie"), it(
        t("\\textbf{Missing days}: the source (energy-charts.info, which republishes the prices of OPCOM and of the Independent Bulgarian Energy Exchange (IBEX) reported to ENTSO-E) "
          "has no price for some days, and gives no reason; Romania: @{data.ro_missing_n} days (" + ROMISS + "); "
          "Bulgaria: the series starts @{data.bg_first|date}, although IBEX has run its day-ahead market since 19 Jan 2016, "
          "and @{data.bg_missing_n} more days are missing up to @{data.bg_missing_last|date}; we do not fill these days, "
          "and no daily change is computed across a gap.",
          "\\textbf{Zile lipsă}: sursa (energy-charts.info, care republică prețurile OPCOM și ale bursei independente de energie din Bulgaria (IBEX) raportate la ENTSO-E) "
          "nu are preț pentru unele zile și nu indică motivul; România: @{data.ro_missing_n} zile (" + ROMISS + "); "
          "Bulgaria: seria începe la @{data.bg_first|date}, deși bursa IBEX organizează piața pentru ziua următoare din 19 ianuarie 2016, "
          "și mai lipsesc @{data.bg_missing_n} zile pînă la @{data.bg_missing_last|date}; aceste zile nu se completează, "
          "iar variația zilnică nu se calculează peste un gol."),
        t("\\textbf{Futures rolls}: the Brent front-month series jumps when the contract rolls; those days are dropped from return statistics.",
          "\\textbf{Schimbarea contractului futures}: seria Brent poate prezenta un salt la trecerea la contractul următor; aceste zile sînt excluse "
          "din statisticile randamentelor."),
        sep="3pt") + D.bottom(t("most forecasting errors at a supplier start in data handling (wrong clock, filled gaps), "
                                "not in the model.",
                                "la un furnizor, cele mai multe erori de prognoză apar la prelucrarea datelor (fus orar greșit, "
                                "goluri completate), nu în model."), NB + " \\S1"), "footnotesize", cite="(Lago, Marcjasz, De Schutter \\& Weron, 2021, APEN)")

    D.subsection(t("Price level and seasonality", "Nivelul prețurilor și sezonalitatea"))
    D.chart(t("Prices jumped in 2021--2022 and never returned to the old level", "Prețurile au explodat în 2021--2022 și nu au mai revenit la vechiul nivel"),
            "prices_daily_4zones", [
                t("Romanian daily maximum @{stats.RO.max|.2f} EUR/MWh on @{stats.RO.max_date|date}; RO, BG and HU move "
                  "together (coupled), while Germany has been cheaper since 2023.",
                  "Maximul zilnic din România: @{stats.RO.max|.2f} EUR/MWh, la @{stats.RO.max_date|date}; RO, BG și HU evoluează "
                  "împreună (piețe cuplate), iar Germania este mai ieftină din 2023.")], height="0.60\\textheight",
            job=t("an industrial consumer budgeting with pre-2021 prices is off by a factor of two to three.",
                  "un consumator industrial care își face bugetul cu prețurile de dinainte de 2021 le subestimează de două-trei ori."),
            tryit=NB + " \\S3", cite=t("(energy-charts.info; prices: OPCOM, IBEX, HUPX, EPEX SPOT)", "(energy-charts.info; prețuri: OPCOM, IBEX, HUPX, EPEX SPOT)"))

    yrs = [str(y) for y in range(2018, Y + 1)]
    rows = []
    for z in ZONES:
        v = [N["byyear"][z][y]["mean"] for y in yrs]
        rows.append([ZN[z]] + [heat(x, min(v), max(v), shown=fmt(x, ".1f", lang)) for x in v])
    rows.append(["\\multicolumn{" + str(len(yrs) + 1) + "}{@{}l}{\\textit{" + t("Volatility: standard deviation of daily price changes",
                                                                                  "Volatilitate: abaterea standard a variațiilor zilnice ale prețului") + "}}"])
    for z in ZONES:
        v = [N["byyear"][z][y]["sd_d"] for y in yrs]
        rows.append([ZN[z]] + [heat(x, min(v), max(v), shown=fmt(x, ".1f", lang)) for x in v])
    D.frame(t("Volatility moves with the price level", "Volatilitatea crește odată cu nivelul prețului"), table(
        "@{}l" + "r" * len(yrs) + "@{}", [t("Mean, EUR/MWh", "Media, EUR/MWh")] + yrs[:-1] + ["@{Y} YTD"], rows,
        size="footnotesize", stretch="1.05") +
        note(t("Colour within each row: green = lowest, red = highest (@{Y} YTD = " + jan_last + ").",
               "Culoarea, pe fiecare rînd: verde = valoarea minimă, roșu = valoarea maximă (@{Y} YTD = " + jan_last + " @{Y}).")) +
        "\n\\vspace{1mm}\n" + it(t("@{Y} YTD: Romania @{cy.mean.RO|.2f} vs @{cy.mean_prev.RO|.2f} EUR/MWh in " + jan_last + " @{YP} "
                                 "(@{cy.chg.RO|+.1f}\\%).",
                                 "@{Y} YTD: România @{cy.mean.RO|.2f} EUR/MWh, față de @{cy.mean_prev.RO|.2f} EUR/MWh în " + jan_last +
                                 " @{YP} (@{cy.chg.RO|+.1f}\\%).")) +
        D.bottom(t("collateral for PZU purchases must scale with the price, since a 200 EUR/MWh market moves far more than a 50 one.",
                   "garanțiile pentru PZU cresc odată cu prețul: la 200 EUR/MWh piața fluctuează mult mai mult decît la 50.")),
        cite=t("(energy-charts.info; own computation)", "(energy-charts.info; calcule proprii)"))

    D.chart(t("Solar moved the cheapest hour of the day to midday", "Producția solară a mutat minimul zilnic al prețului la amiază"), "profile_intraday", [
        t("From 2019 to 2025 the cheapest hour moved from night to midday; 2025: cheapest at @{season.intraday.RO_2025.min_h}:00 "
          "(@{season.intraday.RO_2025.min|.1f} EUR/MWh in Romania), evening peak @{season.intraday.RO_2025.max|.1f}; evening/midday "
          "ratio @{season.intraday.RO_2019.ratio_19_13|.2f} $\\to$ @{season.intraday.RO_2025.ratio_19_13|.2f}, the ``duck curve''.",
          "Între 2019 și 2025, ora cu prețul minim s-a deplasat din timpul nopții către amiază; 2025: minimul la ora @{season.intraday.RO_2025.min_h}:00 "
          "(@{season.intraday.RO_2025.min|.1f} EUR/MWh în România), vîrful de seară la @{season.intraday.RO_2025.max|.1f}; raportul "
          "seară/amiază a urcat de la @{season.intraday.RO_2019.ratio_19_13|.2f} la @{season.intraday.RO_2025.ratio_19_13|.2f}: "
          "„curba în formă de rață” (duck curve).")], height="0.60\\textheight",
        job=t("a battery developer's revenue is this midday-to-evening spread, captured once or twice a day.",
              "venitul unei baterii provine din această diferență dintre amiază și seară, valorificată o dată sau de două ori pe zi."),
        tryit=NB + " \\S3", cite=t("(energy-charts.info; hourly day-ahead prices)", "(energy-charts.info; prețuri orare PZU)"))

    wk = N["season"]["weekly"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    dlab = days if not ro else ["Lu", "Ma", "Mi", "Jo", "Vi", "Sî", "Du"]
    D.concept(
        t("Weekends are cheaper", "La sfîrșit de săptămînă, energia este mai ieftină"),
        t("Factories and offices consume less on weekends, so fewer plants are needed and the price drops.",
          "În weekend, fabricile și birourile consumă mai puțin, sînt necesare mai puține centrale și prețul scade."),
        "\\[ \\hat s_j=\\frac1W\\sum_{w=1}^{W}\\Big(\\underbrace{p_{w,j}}_{" + t("\\text{day }j\\text{ of week }w", "\\text{ziua }j\\text{ din săptămîna }w") +
        "}-\\underbrace{\\tfrac17\\textstyle\\sum_{i=1}^{7}p_{w,i}}_{" + t("\\text{mean of week }w", "\\text{media săptămînii }w") + "}\\Big) \\]" +
        "\\where{" + t("$j$ = weekday; $W$ = number of complete weeks; $\\hat s_j$ = average distance of weekday $j$ from its own "
                       "week's mean (EUR/MWh); subtracting each week's mean removes level shifts such as 2022.",
                       "$j$ = ziua săptămînii; $W$ = numărul de săptămîni complete; $\\hat s_j$ = abaterea medie a zilei $j$ față de "
                       "media săptămînii din care face parte (EUR/MWh); scăderea mediei săptămînale elimină salturile de nivel, ca în 2022.") + "}",
        it(t("\\textbf{On our data}: @{season.weekly.n_weeks} weeks, @{season.weekly.start|date} -- @{season.weekly.end|date}.",
             "\\textbf{Conform datelor}: @{season.weekly.n_weeks} " + de("season.weekly.n_weeks") + "săptămîni, "
             "@{season.weekly.start|date} -- @{season.weekly.end|date}.")) + "\\vspace{0.5mm}" +
        table("@{}l" + "r" * 7 + "@{}", [""] + dlab,
              [[z_] + [heat(wk[zk][dd], min(wk[zk].values()), max(wk[zk].values()), shown=fmt(wk[zk][dd], ".1f", lang)) for dd in days]
               for z_, zk in [("RO", "RO"), ("DE-LU", "DE_LU")]], size="scriptsize") + "\\par\\vspace{1mm}" +
        it(t("Sunday in Romania: $\\hat s_{\\text{Sun}}=$ @{season.weekly.RO.Sun|.1f} EUR/MWh relative to its week's mean.",
             "Duminica, în România: $\\hat s_{\\text{Du}}=$ @{season.weekly.RO.Sun|.1f} EUR/MWh față de media săptămînii.")),
        t("an industrial consumer can move flexible load (maintenance, pumping, charging) to Sunday and save that difference.",
          "un consumator industrial își poate muta consumul flexibil (mentenanță, pompare, încărcare) duminica, reducîndu-și astfel "
          "costurile cu energia."),
        tryit=NB + " \\S3", wl="0.50", wr="0.47")

    sa = N["season"]["annual"]
    D.chart(t("Seasonal profile of prices, consumption and hydro output", "Profilul sezonier al prețurilor, al consumului și al producției hidro"), "profile_annual", [
        t(f"Price relative to the annual mean: highest in {MON[sa['price_max_m']]} (@{{season.annual.price_max|.2f}}), "
          f"lowest in {MON[sa['price_min_m']]} (@{{season.annual.price_min|.2f}}); consumption is highest in January--February and "
          f"lowest in {MON[sa['load_min_m']]}; hydro peaks in {MON[sa['hydro_max_m']]} (snow melt).",
          f"Prețul raportat la media anuală: maxim în {MON[sa['price_max_m']]} (@{{season.annual.price_max|.2f}}), minim în "
          f"{MON[sa['price_min_m']]} (@{{season.annual.price_min|.2f}}); consumul este maxim în ianuarie--februarie și minim în "
          f"{MON[sa['load_min_m']]}; producția hidro atinge maximul în {MON[sa['hydro_max_m']]} (topirea zăpezii).")],
        height="0.60\\textheight",
        job=t("a hydro producer saves reservoir water in spring, when power is cheap, to sell it in winter and late summer.",
              "un producător hidro economisește apa din lacuri primăvara, cînd energia este ieftină, pentru a o turbina iarna și la sfîrșitul verii."),
        tryit=NB + " \\S3", cite=t("(energy-charts.info; monthly means 2016--@{YP})", "(energy-charts.info; medii lunare 2016--@{YP})"))

    D.subsection(t("Spikes and negative prices", "Salturi de preț și prețuri negative"))
    sp = N["spikes"]["tukey"]
    D.concept(
        t("Price spikes: definition and number of hours per year", "Salturile de preț: definiție și numărul de ore pe an"),
        t("A spike is an interval whose price is far above what is normal for that year.",
          "Un salt de preț (spike) apare într-un interval în care prețul depășește cu mult nivelul obișnuit al anului respectiv."),
        "\\[ p_t>\\underbrace{Q_{3,y}}_{" + t("\\text{75th percentile}", "\\text{percentila 75}") + "}+3\\cdot\\underbrace{(Q_{3,y}-Q_{1,y})}_{" +
        t("\\text{interquartile range (IQR)}", "\\text{abaterea intercuartilică (IQR)}") + "} \\]" +
        "\\where{" + t("$Q_{1,y},Q_{3,y}$ = 25th and 75th percentiles of all prices of year $y$, weighted by interval length "
                       "(15-min intervals count a quarter); percentiles are robust, so spikes barely move the threshold.",
                       "$Q_{1,y},Q_{3,y}$ = percentilele 25 și 75 ale prețurilor din anul $y$, ponderate cu durata "
                       "intervalului (un interval de 15 min are un sfert din ponderea unui interval orar); percentilele sînt robuste, deci salturile abia mișcă pragul.") + "}",
        table("@{}lrrr@{}", [t("Year", "Anul"), t("RO thr.", "Prag RO"), "RO h", "DE-LU h"],
              [[y, f(f"spikes.tukey.RO.{y}.thr", ".0f"),
                seq(sp["RO"][y]["hours"], 280, shown=f(f"spikes.tukey.RO.{y}.hours", ".2f")),
                seq(sp["DE_LU"][y]["hours"], 280, shown=f(f"spikes.tukey.DE_LU.{y}.hours", ".2f"))]
               for y in [str(x) for x in range(2020, Y + 1)]], size="scriptsize", stretch="1.0") + "\\par\\vspace{1mm}" +
        it(t("Highest Romanian price in our data: @{spikes.ro_max|.2f} EUR/MWh on @{spikes.ro_max_ts|dt} CEST.",
             "Cel mai mare preț din România în datele noastre: @{spikes.ro_max|.2f} EUR/MWh, la @{spikes.ro_max_ts|dt} CEST.")),
        t("a supplier with fixed-price retail contracts loses most of the year's margin in a few dozen spike hours, which is why it hedges.",
          "un furnizor cu contracte la preț fix își poate pierde cea mai mare parte a marjei anuale în cîteva zeci de ore cu salturi de "
          "preț, motiv pentru care își acoperă riscul."),
        tryit=NB + " \\S4", cite="(Janczura, Trück, Weron \\& Wolff, 2013, ENEECO)", wl="0.55", wr="0.42")

    D.chart(t("Negative prices reached Romania in 2023 and are now routine", "Prețurile negative au apărut în România în 2023 și au devenit frecvente"),
            "negative_prices", [
                t("First negative Romanian price: @{neg.ro_first|date}; since 2024, @{neg.ro_share_10_16|.1f}\\% of negative hours "
                  "fall between 10:00 and 16:00 and @{neg.ro_share_weekend|.1f}\\% on weekends; bars in hour-equivalents.",
                  "Primul preț negativ în România: @{neg.ro_first|date}; din 2024, @{neg.ro_share_10_16|.1f}\\% din orele cu preț negativ "
                  "cad între 10:00 și 16:00, iar @{neg.ro_share_weekend|.1f}\\% în weekend; barele sînt în ore echivalente.")],
            height="0.60\\textheight",
            job=t("a solar park without storage sells much of its output in the cheapest hours of the year (Lecture 6).",
                  "un parc solar fără stocare își vinde o mare parte din producție în cele mai ieftine ore ale anului (cursul 6)."),
            tryit=NB + " \\S4", cite=t("(energy-charts.info; own count, a 15-min MTU = 0.25 h)", "(energy-charts.info; numărare proprie, 15 min = 0,25 h)"))

    ny = [str(y) for y in range(2022, Y + 1)]
    hmax = max(N["neg"]["hours"][z][y] for z in ZONES for y in ny)
    rows = [[ZN[z]] + [seq(N["neg"]["hours"][z][y], hmax, shown=strip0(fmt(N["neg"]["hours"][z][y], ".2f", lang))) for y in ny] +
            [strip0(f(f"neg.lfl_prev.{z}", ".2f")), f(f"neg.n_mtu.{z}.{Y}", ",d")] for z in ZONES]
    D.frame(t("Counting negative prices correctly: hour-equivalents", "Prețurile negative, numărate corect: ore echivalente"), table(
        "@{}l" + "r" * (len(ny) + 2) + "@{}", [t("Zone", "Zona")] + ny[:-1] + ["@{Y} YTD", jan_last + " @{YP}", t("@{Y}: 15-min MTUs", "@{Y}: intervale 15 min")],
        rows, size="footnotesize", stretch="1.1") +
        note(t("Hours with a negative day-ahead price; darker = more hours; last column: negative quarter-hours "
               "(= 4 $\\times$ hour-equivalents).",
               "Ore cu preț PZU negativ; nuanța mai închisă = mai multe ore; ultima coloană: sferturi de oră cu preț negativ "
               "(= 4 $\\times$ orele echivalente).")) + "\n\\vspace{1.5mm}\n" + it(
            t("Romania had none before 2023; Germany had them every year (inflexible plants plus wind).",
              "România nu a avut niciunul înainte de 2023; Germania a avut în fiecare an (centrale inflexibile și vînt)."),
            t("RO, BG and HU move together (coupled), but Hungary has had more negative hours since 2023.",
              "RO, BG și HU evoluează împreună (cuplare), dar din 2023 Ungaria are mai multe ore cu preț negativ."),
            t(jan_last + " @{Y}: Romania @{neg.hours.RO.@{Y}|.2f} h vs @{neg.lfl_prev.RO|.2f} h a year earlier; growth is not automatic (Case study d).",
              jan_last + " @{Y}: România @{neg.hours.RO.@{Y}|.2f} h, față de @{neg.lfl_prev.RO|.2f} h cu un an înainte; creșterea nu este automată (studiul de caz d)."),
            sep="0pt") +
        D.bottom(t("in reports to the board, write ``@{neg.n_mtu.RO.@{Y}|,d} quarter-hours (@{neg.hours.RO.@{Y}|.2f} h)''; never a bare number.",
                   "în rapoartele către conducere scrieți „@{neg.n_mtu.RO.@{Y}|,d} " + de(f"neg.n_mtu.RO.{Y}") + "sferturi de oră (@{neg.hours.RO.@{Y}|.2f} h)”, nu un număr fără unitate."),
                 NB + " \\S4"), cite=t("(energy-charts.info; own computation)", "(energy-charts.info; calcule proprii)"))

    D.subsection(t("Distribution and volatility", "Distribuția prețurilor și volatilitatea"))
    D.figframe(
        t("Prices can be zero or negative: use differences or asinh", "Prețul poate fi nul sau negativ: folosiți diferențe sau asinh"),
        t("Percentage changes need a positive price, but asinh is defined for any sign.",
          "Variațiile procentuale presupun un preț pozitiv, dar asinh este definită pentru orice semn."),
        "\\[ y_t=\\operatorname{asinh}(x_t)=\\ln\\big(x_t+\\sqrt{x_t^2+1}\\big),\\quad x_t=\\frac{p_t-\\tilde p}{\\widehat{\\mathrm{MAD}}},"
        "\\quad \\operatorname{asinh}(x)\\approx\\operatorname{sign}(x)\\ln(2|x|)\\ \\text{" + t("for large", "pentru") + " } |x| \\]",
        "asinh_ro", [
            t("$\\tilde p$ = median, $\\widehat{\\mathrm{MAD}}$ = median absolute deviation (MAD) $\\times1.4826$.",
              "$\\tilde p$ = mediana, $\\widehat{\\mathrm{MAD}}$ = abaterea absolută mediană (MAD) $\\times1{,}4826$."),
            t(jan_last + " @{Y}: @{trans.n_le0|,d} of @{trans.n|,d} quarter-hours $\\le 0$ (@{trans.n_eq0|,d} exactly 0); skewness "
              "@{trans.skew_level|.2f} $\\to$ @{trans.skew_asinh|.2f}, excess kurtosis @{trans.kurt_level|.2f} $\\to$ @{trans.kurt_asinh|.2f}.",
              jan_last + " @{Y}: @{trans.n_le0|,d} din @{trans.n|,d} " + de("trans.n") + "sferturi de oră cu preț $\\le 0$ (@{trans.n_eq0|,d} "
              "exact 0); asimetria @{trans.skew_level|.2f} $\\to$ @{trans.skew_asinh|.2f}, excesul de aplatizare (kurtosis) "
              "@{trans.kurt_level|.2f} $\\to$ @{trans.kurt_asinh|.2f}.")],
        tryit=NB + " \\S5", cite="(Uniejewski, Weron \\& Ziel, 2018, IEEE TPWRS)", height="0.60\\textheight")

    D.figframe(
        t("Extreme oil moves are far more frequent than a normal curve allows", "Cozi groase: variațiile extreme ale țițeiului sînt mult mai frecvente"),
        t("``Fat tails'': very large up or down days come far more often than a bell curve allows.",
          "„Cozi groase”: zilele cu variații foarte mari apar mult mai des decît permite clopotul lui Gauss."),
        None, "tails_brent", [
            t("Brent daily log returns without the @{tails.n_roll} contract-roll days; moves beyond 4 "
              "standard deviations: @{tails.n_4sd} observed vs @{tails.n_4sd_normal|.2f} expected under normality, excess kurtosis "
              "@{tails.exkurt|.2f} (Jarque--Bera (JB) test: Appendix F).",
              "Randamente logaritmice zilnice Brent, fără cele @{tails.n_roll} " +
              de("tails.n_roll") + "zile de schimbare a contractului; peste 4 abateri standard: @{tails.n_4sd} observate, "
              "@{tails.n_4sd_normal|.2f} așteptate sub normalitate, exces de aplatizare (kurtosis) @{tails.exkurt|.2f} (testul "
              "Jarque--Bera (JB): Anexa F).")],
        job=t("a fuel budget built on the normal curve understates crisis days (Lecture 4).",
              "un buget de combustibil bazat pe legea normală subestimează zilele de criză (cursul 4)."),
        tryit=NB + " \\S5", cite="(Jarque \\& Bera, 1980, Econ.\\ Letters; Yahoo Finance BZ=F)", height="0.60\\textheight")

    D.figframe(
        t("Calm and turbulent periods come in clusters", "Perioadele calme și cele agitate apar grupat"),
        t("A big move today makes another big move more likely, whatever its direction.",
          "O variație mare azi face probabilă o altă variație mare, indiferent de sens."),
        "\\[ Q(m)=T(T+2)\\sum_{k=1}^{m}\\frac{\\hat\\rho_k^2}{T-k}\\ \\sim\\ \\chi^2_m\\quad\\text{(Ljung--Box)} \\]",
        "volclust_brent", [
            t("Brent: $Q_{10}(r)=$ @{tails.lb_r|.1f} but $Q_{10}(r^2)=$ @{tails.lb_r2|.1f} (5\\% critical value 18.31); little memory in "
              "the direction of moves, a lot in their size.",
              "Brent: $Q_{10}(r)=$ @{tails.lb_r|.1f}, dar $Q_{10}(r^2)=$ @{tails.lb_r2|.1f} (valoarea critică la 5\\%: 18{,}31); "
              "memorie slabă pentru sensul variațiilor, puternică pentru mărimea lor.")],
        job=t("after a shock, a risk desk keeps wider limits for weeks, not days (Lecture 3).",
              "după un șoc, limitele de risc rămîn mai largi săptămîni, nu zile (cursul 3)."),
        tryit=NB + " \\S5", cite="(Ljung \\& Box, 1978, Biometrika)", height="0.60\\textheight")
    D.section(t("Time-series toolkit", "Instrumente de analiză a seriilor de timp"))
    D.subsection(t("Stationarity and autocorrelation", "Staționaritate și autocorelație"))
    D.figframe(
        t("Weak stationarity: constant mean, variance and autocovariances", "Staționaritatea slabă: medie, varianță și autocovarianțe constante"),
        t("Weakly stationary: mean, spread and lag-$k$ memory are the same in every period.",
          "Slab staționară: media, dispersia și memoria la fiecare decalaj $k$ sînt aceleași în orice perioadă."),
        "\\[ \\E X_t=\\mu,\\quad \\Var X_t=\\gamma_0,\\quad \\Cov(X_t,X_{t-k})=\\gamma_k\\quad " +
        t("\\text{for every } t", "\\text{pentru orice } t") + " \\]",
        "sim_wn_ar_rw", [
            (t("White noise, a first-order autoregressive (AR) model AR(1) with $\\phi=0.9$, a random walk",
               "Zgomot alb, un model autoregresiv (AR) de ordinul 1, AR(1), cu $\\phi=0{,}9$, un mers aleator"),
             t("AR(1) reverts to its mean; random-walk shocks are permanent: autocorrelation @{sim.rw.acf10|.2f} at lag 10",
               "AR(1) revine la medie; șocurile mersului aleator sînt permanente: autocorelația @{sim.rw.acf10|.2f} la decalajul 10"))],
        job=t("a historical average price is a forecast only if the series is stationary.",
              "un preț mediu istoric este o prognoză numai dacă seria este staționară."),
        tryit=NB + " \\S6", cite="(Hyndman \\& Athanasopoulos, 2021, OTexts)", height="0.60\\textheight")
    D.parts[-1] = D.parts[-1].replace("\\chartsource{", "\\chartsource{\\simlabel\\ ")

    D.concept(
        t("Autocorrelation measures how much today's price remembers the past", "Autocorelația: cît din trecut se regăsește în prețul de azi"),
        t("The autocorrelation at lag $k$ is the correlation between the series and itself shifted by $k$ periods.",
          "Autocorelația de ordinul $k$ este corelația dintre serie și aceeași serie decalată cu $k$ perioade."),
        "\\[ \\hat\\rho_k=\\frac{\\sum_{t=k+1}^{T}(x_t-\\bar x)(x_{t-k}-\\bar x)}{\\sum_{t=1}^{T}(x_t-\\bar x)^2} \\]" +
        it(t("White-noise band: $\\pm1.96/\\sqrt T$.", "Banda de încredere pentru zgomot alb: $\\pm1{,}96/\\sqrt T$."),
           t("Bartlett band at lag $k$: $\\pm1.96\\sqrt{(1+2\\sum_{j<k}\\hat\\rho_j^2)/T}$, valid if the true autocorrelation is zero beyond lag $k-1$.",
             "Banda Bartlett la decalajul $k$: $\\pm1{,}96\\sqrt{(1+2\\sum_{j<k}\\hat\\rho_j^2)/T}$, valabilă dacă autocorelația teoretică este nulă după decalajul $k-1$."),
           t("Partial autocorrelation function (PACF): memory at lag $k$ net of shorter lags.",
             "Funcția de autocorelație parțială (PACF): memoria la decalajul $k$, după eliminarea efectului decalajelor mai mici."), sep="2pt"),
        it((t("\\textbf{Four reading rules}", "\\textbf{Patru reguli de interpretare}"),
            t("slow decay from near 1: persistence or a unit root; test it", "scădere lentă de la valori apropiate de 1: persistență sau rădăcină unitară; testați"),
            t("geometric decay, PACF cut after $p$ lags: an AR($p$) model", "scădere geometrică, PACF se anulează după $p$ decalaje: un model AR($p$)"),
            t("peaks at lags 7, 14 (days) or 24, 168 (hours): seasonality", "vîrfuri la decalajele 7, 14 (zile) sau 24, 168 (ore): sezonalitate"),
            t("all inside the band: no linear memory (check $x_t^2$ too)", "toate valorile în bandă: nicio memorie liniară (verificați și $x_t^2$)"))),
        t("a supplier's forecast for tomorrow starts from ``same weekday last week'': $\\hat\\rho_7=$ @{acf.daily.r7|.3f} in Romania since 2023.",
          "prognoza unui furnizor pentru ziua de mîine pornește de la „aceeași zi din săptămîna trecută”: $\\hat\\rho_7=$ @{acf.daily.r7|.3f} în România, din 2023."),
        tryit=NB + " \\S6", cite="(Hyndman \\& Athanasopoulos, 2021; Ljung \\& Box, 1978)", wl="0.52", wr="0.45")
    def acf_src(f1, f2):
        """Two charts from the same source: one source line under the second chart, both periods in it."""
        import re as _re
        f1 = _re.sub(r"\\chartsource\{[^{}]*\}", "", f1)
        m1, m2 = V.get("charts.acf_pacf_ro_daily"), V.get("charts.acf_ro_hourly")
        per = t("top: ", "sus: ") + m1["period_" + lang] + t("; bottom: ", "; jos: ") + m2["period_" + lang]
        return f1 + "\n" + _re.sub(r"\\chartsource\{[^{}]*\}", lambda _m: "\\chartsource{" + t("Source", "Sursa") + ": " +
                                     m2["source_" + lang] + ". " + t("Data", "Date") + ": " + per + ".}", f2)
    D.frame(t("Autocorrelation of prices at daily and weekly lags", "Autocorelația prețurilor la decalaje de o zi și de o săptămînă"),
            acf_src(D.fig("acf_pacf_ro_daily", "0.42\\textheight"), D.fig("acf_ro_hourly", "0.30\\textheight")) + "\n" + it(
        t("Daily, @{acf.daily.start|date} -- @{acf.daily.end|date}: $\\hat\\rho_1=$ @{acf.daily.r1|.3f}, $\\hat\\rho_7=$ @{acf.daily.r7|.3f}, "
          "PACF $\\hat\\alpha_7=$ @{acf.daily.p7|.3f}; hourly, 2024: $\\hat\\rho_{24}=$ @{acf.hourly.r24|.3f}, $\\hat\\rho_{168}=$ @{acf.hourly.r168|.3f}.",
          "Date zilnice, @{acf.daily.start|date} -- @{acf.daily.end|date}: $\\hat\\rho_1=$ @{acf.daily.r1|.3f}, $\\hat\\rho_7=$ @{acf.daily.r7|.3f}, "
          "PACF $\\hat\\alpha_7=$ @{acf.daily.p7|.3f}; date orare, 2024: $\\hat\\rho_{24}=$ @{acf.hourly.r24|.3f}, $\\hat\\rho_{168}=$ @{acf.hourly.r168|.3f}.")) +
            D.bottom(None, NB + " \\S6"), "small", cite="(Ziel \\& Weron, 2018, ENEECO)")
    nvy = N["naive"]["years"]
    rows = []
    for z in ["RO", "DE_LU"]:
        for lab, key in [(t("naive", "naiv"), "naive"), ("$d-1$", "lag1"), ("$d-7$", "lag7")]:
            r = [f"{ZN[z]} {lab}"]
            for y in nvy:
                trio = [N["naive"][z][y][k] for k in ["naive", "lag1", "lag7"]]
                r.append(heat(N["naive"][z][y][key], min(trio), max(trio), shown=fmt(N["naive"][z][y][key], ".1f", lang)))
            rows.append(r)
    NAIVETAB = table("@{}l" + "r" * len(nvy) + "@{}", ["MAE"] + nvy, rows, size="footnotesize", stretch="1.1")
    D.figframe(
        t("The benchmark to beat: the naive forecast", "Prognoza naivă: reperul pe care orice model trebuie să-l depășească"),
        t("Tomorrow, each hour costs what it cost today (after weekends: the same day last week).",
          "Mîine, fiecare oră costă cît a costat azi (după weekend: ca săptămîna trecută)."),
        "\\[ \\hat p_{d,h}=\\begin{cases} p_{d-1,h} & " + t("d=\\text{Tue--Fri}", "d=\\text{Ma--Vi}") + "\\\\ p_{d-7,h} & " +
        t("d=\\text{Mon, Sat, Sun}", "d=\\text{Lu, Sî, Du}") + "\\end{cases},\\qquad \\mathrm{MAE}=\\frac{1}{n}\\sum_{d,h}|p_{d,h}-\\hat p_{d,h}| \\]",
        "naive_bar", [
            t("Mean absolute error (MAE), EUR/MWh: Romania @{YP}, @{naive.RO.@{YP}.naive|.1f} at a mean price of @{naive.RO.@{YP}.mean|.1f}; "
              "the weekday/weekend rule beats both pure lags in @{naive.RO.n_best} of @{naive.RO.n_years} years (Appendix E).",
              "Eroarea absolută medie (MAE), România, @{YP}: @{naive.RO.@{YP}.naive|.1f} EUR/MWh, la un preț mediu de "
              "@{naive.RO.@{YP}.mean|.1f}; regula zi lucrătoare/weekend bate ambele decalaje simple în @{naive.RO.n_best} "
              "din @{naive.RO.n_years} ani (Anexa E).")],
        job=t("before paying for a forecasting service, ask for its MAE next to this benchmark.",
              "înainte de a plăti un serviciu de prognoză, cereți-i MAE alături de acest reper."),
        tryit=NB + " \\S6", cite="(Nogales et al., 2002, IEEE TPWRS; Weron, 2014, IJF; Lago et al., 2021, APEN)", height="0.60\\textheight")
    D.subsection(t("Unit-root tests, decomposition, smoothing", "Teste de rădăcină unitară, descompunere și netezire"))
    D.concept(
        t("Shock persistence: two tests with opposite null hypotheses", "Persistența șocurilor: două teste cu ipoteze opuse"),
        t("One test starts from ``shocks are permanent'' and looks for a pull back to a mean; the other starts from ``the series is "
          "stable'' and looks for a slow drift.",
          "Un test pornește de la ipoteza „șocurile sînt permanente” și caută o revenire la medie; celălalt pornește de la „seria "
          "este stabilă” și caută o derivă lentă."),
        "\\[ \\Delta x_t=\\alpha+\\underbrace{\\gamma\\,x_{t-1}}_{" + t("\\text{pull to the mean}", "\\text{revenirea la medie}") +
        "}+\\underbrace{\\textstyle\\sum_{j}\\delta_j\\Delta x_{t-j}}_{" + t("\\text{extra lags}", "\\text{decalaje}") + "}+u_t \\]" +
        "\\where{" + t("augmented Dickey--Fuller (ADF): $H_0:\\gamma=0$ (unit root), $\\hat\\gamma/\\mathrm{se}$ against "
                       "Dickey--Fuller critical values (about $-2.86$ at 5\\%), lags $p$ chosen by the Akaike information criterion (AIC); "
                       "Kwiatkowski--Phillips--Schmidt--Shin (KPSS): $H_0$ = stationary, large values reject (0.463 at 5\\%); "
                       "full formulas: Appendix A.",
                       "testul Dickey--Fuller augmentat (ADF): $H_0:\\gamma=0$ (rădăcină unitară), $\\hat\\gamma/\\mathrm{se}$ comparat "
                       "cu valorile critice Dickey--Fuller (circa $-2{,}86$ la 5\\%), decalajele $p$ alese după criteriul informațional "
                       "Akaike (AIC); testul Kwiatkowski--Phillips--Schmidt--Shin (KPSS): $H_0$ = serie staționară, respinsă la valori mari "
                       "(0{,}463 la 5\\%); formulele complete: Anexa A.") + "}",
        table("@{}lll@{}", [t("", "$H_0$:"), t("KPSS: keep", "KPSS nerespinsă"), t("KPSS: reject", "KPSS respinsă")],
              [[t("ADF: reject", "ADF respinsă"), "\\cellcolor{Forest!25}" + t("stationary", "staționar"), "\\cellcolor{Bitter!30}conflict"],
               [t("ADF: keep", "ADF nerespinsă"), t("inconclusive", "neconcludent"),
                "\\cellcolor{Crimson!25}" + t("unit root$^{*}$", "răd.\\ unitară$^{*}$")]], size="scriptsize") +
        "\\par\\vspace{1mm}" + it(t("$^{*}$Consistent with a unit root, not a proof: ADF has low power against slow mean reversion, "
                                    "and level breaks (2022) push it towards ``unit root''.",
                                    "$^{*}$Compatibil cu o rădăcină unitară, dar nu este o dovadă: testul ADF are putere redusă în "
                                    "cazul revenirii lente la medie, iar rupturile de nivel (2022) favorizează nerespingerea rădăcinii unitare."), sep="1pt"),
        t("if a supplier's price can carry permanent shocks, ``prices will come back to normal'' is not a safe budget assumption.",
          "dacă șocurile pot fi permanente, un furnizor nu își poate baza bugetul pe „revenirea la normal”."),
        tryit=NB + " \\S7", cite="(Dickey \\& Fuller, 1979, JASA; Kwiatkowski et al., 1992, J.\\ Econometrics)", wl="0.55", wr="0.42")

    LBL = {"ro_lvl": t("RO price, level", "Preț RO, nivel"), "ro_d": t("RO price, daily change", "Preț RO, variație zilnică"),
           "de_lvl": t("DE-LU price, level", "Preț DE-LU, nivel"), "br_lvl": t("Brent, log price", "Brent, logaritmul prețului"),
           "br_r": t("Brent, log return", "Brent, randament logaritmic"),
           "hy_ds": t("RO hydro, deseasonalised", "Hidro RO, desezonalizat")}
    DEC = {"stationary": ("Forest!25", t("stationary", "staționar")), "unit_root": ("Crimson!25", t("unit root$^{*}$", "rădăcină unitară$^{*}$")),
           "conflict": ("Bitter!30", "conflict"), "inconclusive": ("BlockGray", t("inconclusive", "neconcludent"))}
    rows = []
    for k in N["unit"]["order"]:
        u = N["unit"][k]
        kp = ("$<$0{,}01" if ro else "$<$0.01") if u["kpss_p_trunc"] == "lt" else (("$>$0{,}10" if ro else "$>$0.10") if u["kpss_p_trunc"] == "gt" else fmt(u["kpss_p"], ".3f", lang))
        c_, l_ = DEC[u["decision"]]
        rows.append([LBL[k], f"{u['first'][:4]}--{u['last'][:4]}", fmt(u["T"], ",d", lang), fmt(u["adf"], ".2f", lang), pval(u["adf_p"]),
                     fmt(u["kpss"], ".3f", lang), kp, f"\\cellcolor{{{c_}}}{l_}"])
    D.frame(t("ADF and KPSS results by series: levels and changes", "Rezultatele testelor ADF și KPSS pe serii: niveluri și variații"), table(
        "@{}llrrrrrl@{}", [t("Series", "Seria"), t("Sample", "Perioada"), "$T$", "ADF", "$p$", "KPSS", "$p$", t("Verdict", "Verdict")], rows,
        size="footnotesize", stretch="1.0") + note(t("$^{*}$Consistent with a unit root (not rejected); not a proof.",
        "$^{*}$Compatibil cu o rădăcină unitară (ipoteză nerespinsă); nu este o dovadă.")) + "\n\\vspace{1mm}\n" + it(
        t("Romanian and Brent \\textbf{levels} are consistent with a unit root, while their \\textbf{changes} are stationary.",
          "\\textbf{Nivelurile} RO și Brent sînt compatibile cu o rădăcină unitară, \\textbf{variațiile} sînt staționare."),
        t("Germany: both tests reject (conflict): mean reversion plus the 2021--2022 level shift.",
          "Germania: ambele teste își resping ipoteza nulă (conflict): revenire la medie și saltul de nivel din 2021--2022."),
        t("Hydro is tested without its monthly means (a seasonal series); Romanian price since 2023 only: "
          "ADF $p=$ @{unit.ro_2023.adf_p|.3f}, KPSS @{unit.ro_2023.kpss|.3f}.",
          "Seria hidro este testată după scăderea mediilor lunare (serie sezonieră); prețul din România numai din 2023: "
          "ADF $p=$ @{unit.ro_2023.adf_p|.3f}, KPSS @{unit.ro_2023.kpss|.3f}."), sep="1pt") +
        D.bottom(t("model price \\emph{changes} (or transformed prices) and put seasonality in explicitly.",
                   "modelați \\emph{variațiile} prețului (sau prețul transformat) și includeți explicit sezonalitatea."), NB + " \\S7"),
        cite=t("(own computation; constant only; ADF lags by AIC; 5\\% level)", "(calcule proprii; numai constantă; decalaje ADF după AIC; prag de 5\\%)"))

    D.figframe(
        t("Decomposition splits a series into trend, season and the rest", "Descompunerea: trend, sezonalitate și componenta reziduală"),
        t("Seasonal--Trend decomposition using Loess (STL) lets the season evolve.",
          "Descompunerea sezonieră și de trend prin regresie locală (STL) lasă sezonul să evolueze."),
        "\\[ x_t=T_t+S_t+R_t\\qquad(" + t("\\text{trend + season + remainder}", "\\text{trend + sezon + rest}") + ") \\]",
        "decomp_load", [
            t("Romanian load vs trend: Jan @{decomp.sidx.Jan|+.2f}, Feb @{decomp.sidx.Feb|+.2f}, May @{decomp.sidx.May|.2f} GW; STL "
              "amplitude @{decomp.stl_amp_first|.2f} $\\to$ @{decomp.stl_amp_last|.2f} GW, moving-average (MA) weights: Appendix B.",
              "Consumul României față de trend: ian. @{decomp.sidx.Jan|+.2f}, feb. @{decomp.sidx.Feb|+.2f}, mai @{decomp.sidx.May|.2f} GW; "
              "amplitudinea STL: @{decomp.stl_amp_first|.2f} $\\to$ @{decomp.stl_amp_last|.2f} GW, ponderile mediei mobile (MA): Anexa B.")],
        job=t("Transelectrica and suppliers plan monthly capacity with seasonal indices.",
              "Transelectrica și furnizorii planifică lunar capacitățile cu indici sezonieri."),
        tryit=NB + " \\S8", cite="(Cleveland et al., 1990, JOS; Hyndman \\& Athanasopoulos, 2021)", height="0.60\\textheight")

    D.figframe(
        t("Exponential smoothing: recent data count more", "Netezirea exponențială: datele recente cîntăresc mai mult"),
        t("The smoothed level averages all past values, with weights shrinking geometrically.",
          "Nivelul netezit: medie ponderată a valorilor trecute, cu ponderi care scad geometric."),
        "\\[ \\ell_t=\\underbrace{\\alpha x_t}_{" + t("\\text{news}", "\\text{informația nouă}") + "}+\\underbrace{(1-\\alpha)\\ell_{t-1}}_{" +
        t("\\text{memory}", "\\text{memoria}") + "},\\qquad \\alpha=1-2^{-1/h} \\]",
        "smooth_brent", [
            t("$h$ = half-life (days), so the exponentially weighted moving average (EWMA) has $\\alpha=$ @{smooth.alpha_hl|.3f}; "
              "best simple exponential smoothing (SES) weight: @{smooth.alpha_ses|.3f}, almost the last price.",
              "$h$ = timpul de înjumătățire (zile), deci media mobilă ponderată exponențial (EWMA) are $\\alpha=$ @{smooth.alpha_hl|.3f}; "
              "ponderea optimă a netezirii exponențiale simple (SES): @{smooth.alpha_ses|.3f}, practic ultimul preț.")],
        job=t("an EWMA is a good contract reference price, but a weak forecast.",
              "EWMA este un bun preț de referință în contracte, dar o prognoză slabă."),
        tryit=NB + " \\S9", cite="(Hyndman \\& Athanasopoulos, 2021, OTexts, ch.\\ 8)", height="0.62\\textheight")
    D.section(t("Case studies on current data", "Studii de caz pe date recente"))
    D.subsection(t("(a) Hydro output in 2023 and 2025", "(a) Producția hidro în 2023 și 2025"))
    D.chart(t("Case study (a): 2025 hydro output was a third below wet 2023", "Studiul de caz (a): producția hidro în 2025, cu o treime sub 2023"), "hydro_case", [
        t("Hydro: @{hydro.y2023|.2f} TWh in 2023 (highest since 2015) vs @{hydro.y2025|.2f} TWh in 2025 (lowest), \\textbf{@{hydro.chg_pct|.1f}\\%}; "
          "2025 vs the 2015--2025 mean of @{hydro.mean_1525|.2f} TWh: @{hydro.vs_mean_pct|.1f}\\%.",
          "Hidro: @{hydro.y2023|.2f} TWh în 2023 (maximul din 2015) și @{hydro.y2025|.2f} TWh în 2025 (minimul), \\textbf{@{hydro.chg_pct|.1f}\\%}; "
          "2025 față de media 2015--2025 (@{hydro.mean_1525|.2f} TWh): @{hydro.vs_mean_pct|.1f}\\%."),
        t("Romania went from net exporter (@{hydro.netimp2023|.2f} TWh) to net importer (@{hydro.netimp2025|+.2f} TWh); "
          "consistent with less water, but nuclear, demand and prices abroad also moved.",
          "România a trecut de la export net (@{hydro.netimp2023|.2f} TWh) la import net (@{hydro.netimp2025|+.2f} TWh); "
          "compatibil cu lipsa apei, dar s-au schimbat și nuclearul, cererea și prețurile vecinilor.")], height="0.60\\textheight",
        job=t("a hydro producer's output and a net importer's bill depend on rain.",
              "producția unei companii hidro și factura unui importator net depind de ploaie."),
        tryit=NB + " \\S10a", cite=t("(energy-charts.info; data source: ENTSO-E)", "(energy-charts.info; sursa datelor: ENTSO-E)"))
    D.concept(
        t("Case study (a): wetter months go with lower Romanian prices", "Studiul de caz (a): mai multă apă, prețuri mai mici"),
        t("Holding the gas price fixed, months with more hydro output have had lower Romanian prices --- an association, not a measured effect.",
          "Cu gazele la preț fix, lunile cu mai multă apă au avut prețuri mai mici: o asociere, nu un efect cauzal."),
        "\\[ p_m=\\beta_0+\\underbrace{\\beta_1\\,\\mathrm{Hydro}_m}_{" + t("\\text{water}", "\\text{apa}") + "}+\\underbrace{\\beta_2\\,\\mathrm{TTF}_m}_{" +
        t("\\text{gas cost}", "\\text{costul gazelor}") + "}+u_m \\]" +
        "\\where{" + t("$p_m$ = mean RO day-ahead price, month $m$ (EUR/MWh); $\\mathrm{Hydro}_m$ = hydro output (TWh); "
                       "$\\mathrm{TTF}_m$ = Dutch gas price (EUR/MWh); estimated by ordinary least squares (OLS) with heteroskedasticity- and "
                       "autocorrelation-consistent (HAC) standard errors, 6 lags.",
                       "$p_m$ = prețul mediu PZU în luna $m$ (EUR/MWh); $\\mathrm{Hydro}_m$ = producția hidro (TWh); $\\mathrm{TTF}_m$ = "
                       "prețul gazelor pe hubul olandez (EUR/MWh); estimare prin metoda celor mai mici pătrate (OLS), cu erori standard "
                       "robuste la heteroscedasticitate și autocorelație (HAC), 6 decalaje.") + "}",
        table("@{}lrrr@{}", [N["hydro"]["reg"]["start"][:4] + "--" + N["hydro"]["reg"]["end"][:4], "$\\hat\\beta$", t("s.e.", "e.s."), "$t$"],
              [[lab, f(f"hydro.reg.{k}.b", ".2f"), f(f"hydro.reg.{k}.se", ".2f"), f(f"hydro.reg.{k}.t", ".2f")]
               for lab, k in [(t("Constant", "Constantă"), "const"), ("Hydro", "hydro"), ("TTF", "ttf")]], size="footnotesize") +
        "\\par\\vspace{1mm}" + it(
            t("One TWh more hydro in a month: @{hydro.reg.hydro.b|.2f} EUR/MWh on average, gas held fixed.",
              "Un TWh hidro în plus într-o lună: în medie, @{hydro.reg.hydro.b|.2f} EUR/MWh, la același preț al gazelor."),
            t("Caveat: price and gas levels trend (Section 3): spurious regression unless cointegrated; "
              "$R^2=$ @{hydro.reg.r2|.3f} is not evidence; Lecture 2 tests cointegration.",
              "Atenție: prețurile energiei și ale gazelor au trend (secțiunea 3), deci fără cointegrare regresia poate fi spurioasă; "
              "$R^2=$ @{hydro.reg.r2|.3f} nu este o dovadă; cointegrarea se testează în cursul 2."), sep="2pt"),
        t("hydro producers and traders watch reservoir levels as a leading indicator of the PZU price.",
          "producătorii hidro și traderii urmăresc nivelul lacurilor ca indicator anticipativ al prețului PZU."),
        tryit=NB + " \\S10a", cite=t("(own estimation; Newey--West standard errors)", "(estimare proprie; erori standard Newey--West)"), wl="0.50", wr="0.47")
    D.subsection(t("(b) The June 2025 oil shock", "(b) Șocul petrolier din iunie 2025"))
    D.chart(t("Case study (b): Brent +7\\% in a day, then back below the pre-war price", "Studiul de caz (b): Brent, +7\\% într-o zi, apoi sub nivelul inițial"),
            "iran_brent", [
        t("Close 12 Jun 2025 @{iran.p12|.2f} $\\to$ 13 Jun (Israel strikes Iran) @{iran.p13|.2f}: \\textbf{@{iran.chg13|+.1f}\\%} "
          "(@{iran.z13|.1f} standard deviations of 2024 daily returns); peak @{iran.peak|.2f} on @{iran.peak_date|date}; 24 Jun (ceasefire in effect) "
          "@{iran.p24|.2f}, i.e.\\ \\textbf{@{iran.chg24_peak|.1f}\\%} from the peak and @{iran.chg24_12|+.1f}\\% vs 12 Jun.",
          "Prețul de închidere: 12 iunie 2025 @{iran.p12|.2f} $\\to$ 13 iunie (Israelul atacă Iranul) @{iran.p13|.2f}, adică "
          "\\textbf{@{iran.chg13|+.1f}\\%} (@{iran.z13|.1f} abateri standard ale randamentelor zilnice din 2024); maximul: @{iran.peak|.2f}, "
          "la @{iran.peak_date|date}; 24 iunie, cu armistițiul în vigoare: @{iran.p24|.2f}, adică \\textbf{@{iran.chg24_peak|.1f}\\%} față de "
          "maxim și @{iran.chg24_12|+.1f}\\% față de 12 iunie.")],
            height="0.60\\textheight",
            job=t("a fuel buyer hedged at the 20 June peak; four days later the market was far below that price.",
                  "un cumpărător de combustibil și-a acoperit riscul la maximul din 20 iunie; patru zile mai tîrziu, piața era mult sub prețul fixat."),
            tryit=NB + " \\S10b", cite="(Yahoo Finance, ICE Brent BZ=F)" if False else "(Yahoo Finance, Brent BZ=F)")

    D.subsection(t("(c) Regional price separation, summer 2024", "(c) Separarea regională a prețurilor în vara lui 2024"))
    D.chart(t("Case study (c): in July 2024 Romania paid twice the German price", "Studiul de caz (c): în iulie 2024, România a plătit dublul prețului din Germania"), "separation_2024", [
        t("July 2024 averages: RO @{sep.jul.RO|.2f}, BG @{sep.jul.BG|.2f}, HU @{sep.jul.HU|.2f}, DE-LU @{sep.jul.DE_LU|.2f} EUR/MWh; "
          "16 Jul: RO--DE-LU gap @{sep.d16_gap|.2f}; RO hourly peak @{sep.d16_ro_max|.2f} at @{sep.d16_ro_max_h}:00 while DE-LU was "
          "@{sep.d16_de_min|.2f} at @{sep.d16_de_min_h}:00.",
          "Mediile din iulie 2024: RO @{sep.jul.RO|.2f}, BG @{sep.jul.BG|.2f}, HU @{sep.jul.HU|.2f}, DE-LU @{sep.jul.DE_LU|.2f} EUR/MWh; "
          "16 iulie: diferența RO--DE-LU, @{sep.d16_gap|.2f}; vîrful orar din România, @{sep.d16_ro_max|.2f} la ora @{sep.d16_ro_max_h}:00, "
          "în timp ce DE-LU avea @{sep.d16_de_min|.2f} la ora @{sep.d16_de_min_h}:00.")], height="0.60\\textheight",
        job=t("for South-East European buyers, the evening hours of hot, dry summers are the main price risk.",
              "pentru cumpărătorii din sud-estul Europei, serile verilor caniculare și secetoase reprezintă principalul risc de preț."),
        tryit=NB + " \\S10c", cite=t("(energy-charts.info; daily and hourly day-ahead prices)", "(energy-charts.info; prețuri PZU zilnice și orare)"))

    D.frame(t("Case study (c): evening, heat and a congested network", "Studiul de caz (c): seri caniculare și o rețea congestionată"), cols(it(
        t("Equal prices (within 0.01 EUR/MWh) in July hours: RO--BG @{sep.eq_ro_bg|.1f}\\%, RO--HU @{sep.eq_ro_hu|.1f}\\%, RO--DE-LU @{sep.eq_ro_de|.1f}\\%; "
          "the network towards Central Europe was binding; which element was binding cannot be read from prices alone.",
          "Prețuri egale (diferență sub 0{,}01 EUR/MWh) în orele din iulie: RO--BG @{sep.eq_ro_bg|.1f}\\%, RO--HU @{sep.eq_ro_hu|.1f}\\%, "
          "RO--DE-LU @{sep.eq_ro_de|.1f}\\%; rețeaua spre Europa Centrală era la limita capacității; elementul de rețea saturat nu "
          "poate fi identificat numai din prețuri."),
        t("After sunset solar disappears while air conditioning keeps demand high; the region must import exactly then.",
          "După apus, producția solară dispare, iar aerul condiționat menține cererea ridicată; regiunea trebuie să importe exact atunci."),
        t("Romanian hydro in July--August: @{sep.hydro_ja_2024|.2f} TWh in 2024 vs @{sep.hydro_ja_2023|.2f} in 2023; net imports "
          "averaged @{sep.imp_ja_2024|,.0f} MW vs @{sep.imp_ja_2023|,.0f} MW.",
          "Producția hidro în iulie--august: @{sep.hydro_ja_2024|.2f} TWh în 2024, față de @{sep.hydro_ja_2023|.2f} TWh în 2023; "
          "importul net mediu: @{sep.imp_ja_2024|,.0f} MW, față de @{sep.imp_ja_2023|,.0f} MW."),
        t("Summer peak: RO daily @{sep.peak|.2f} EUR/MWh on @{sep.peak_date|date} (DE-LU @{sep.de_on_peak|.2f}); hourly "
          "@{sep.peak_hour_v|.2f} at @{sep.peak_hour}:00 CEST, the highest Romanian hourly price in our data.",
          "Vîrful verii: prețul zilnic din România, @{sep.peak|.2f} EUR/MWh, la @{sep.peak_date|date} (DE-LU @{sep.de_on_peak|.2f}); prețul "
          "orar, @{sep.peak_hour_v|.2f} la ora @{sep.peak_hour}:00 CEST, cel mai mare preț orar din România în datele noastre."), sep="2pt"),
        block(t("Lesson for modelling", "Concluzii pentru modelare"), it(
              t("Coupled prices are equal only while the network is not binding.",
                "Prețurile piețelor cuplate sînt egale numai cît timp rețeaua nu este la limită."),
              t("Model Romania with regional drivers: hydro, solar, load in South-East Europe.",
                "Modelați prețul din România cu factori regionali: hidro, solar, consumul din sud-estul Europei."),
              t("Treat the spread to Germany as its own, regime-dependent variable.",
                "Tratați diferența față de Germania ca variabilă separată, dependentă de regim."), sep="2pt")),
        "0.60", "0.37") + D.bottom(None, NB + " \\S10c"),
        cite=t("(energy-charts.info; ENTSO-E physical flows)", "(energy-charts.info; fluxuri fizice ENTSO-E)"))

    D.subsection(t("(d) Negative prices and solar", "(d) Prețurile negative și energia solară"))
    D.chart(t("Case study (d): negative hours cluster in spring, as solar grows year after year",
              "Studiul de caz (d): prețurile negative apar mai ales primăvara"), "negative_solar", [
        t("April--May hold @{neg.share_apr_may|.1f}\\% of Romanian negative hours since 2023 (June--August @{neg.share_jun_aug|.1f}\\%); "
          "metered solar: @{neg.solar_twh.2023|.2f} TWh (2023) $\\to$ @{neg.solar_twh.2025|.2f} TWh (2025), "
          "@{mix.lfl.Solar.ytd_own|.2f} TWh in " + jan_last + " @{Y}.",
          "Din 2023, lunile aprilie și mai concentrează @{neg.share_apr_may|.1f}\\% din orele cu preț negativ din România (iunie--august: "
          "@{neg.share_jun_aug|.1f}\\%); producția solară măsurată: @{neg.solar_twh.2023|.2f} TWh (2023) $\\to$ @{neg.solar_twh.2025|.2f} TWh "
          "(2025), @{mix.lfl.Solar.ytd_own|.2f} TWh în " + jan_last + " @{Y}.")], height="0.60\\textheight",
        job=t("the cheapest hours are spring weekend middays; a battery charges and flexible industry consumes then.",
              "cele mai ieftine ore sînt cele de la amiază, în weekendurile de primăvară; atunci se încarcă bateriile, iar industria își poate programa consumul flexibil."),
        tryit=NB + " \\S10d", cite=t("(energy-charts.info; data source: ENTSO-E)", "(energy-charts.info; sursa datelor: ENTSO-E)"))

    lg = N["logit"]["coef"]
    LOGTAB = table("@{}lrrr@{}", ["", "$\\hat\\beta$", t("odds ratio", "raportul șanselor"), "$z$"],
                   [[lab, fmt(lg[k]["b"], ".3f", lang), fmt(lg[k]["or"], ".2f", lang), fmt(lg[k]["z"], ".2f", lang)]
                    for lab, k in [(t("Constant", "Constantă"), "const"), (t("Residual load, GW", "Consum rezidual, GW"), "resid"),
                                   (t("Hydro, GW", "Hidro, GW"), "hydro"), ("Weekend", "wkend")] +
                    [(t("Year ", "Anul ") + k[1:], k) for k in lg if k.startswith("y")]], size="footnotesize", stretch="1.1")
    D.concept(
        t("Case study (d): what accompanies negative-price days",
          "Studiul de caz (d): factorii asociați zilelor cu prețuri negative"),
        t("We describe the realised conditions on days with at least one negative quarter-hour; this describes, it does not forecast for bidding.",
          "Descriem condițiile efectiv înregistrate în zilele cu cel puțin un sfert de oră cu preț negativ; modelul descrie condițiile observate, fără a oferi prognoze pentru licitare."),
        "\\[ \\Pr(\\text{" + t("negative day", "zi negativă") + "})=\\Lambda\\big(\\beta_0+\\underbrace{\\beta_1R_d}_{" + t("\\text{residual load}", "\\text{consum rezidual}") +
        "}+\\beta_2\\mathrm{Hyd}_d+\\underbrace{\\beta_3\\mathrm{Wkd}_d+\\gamma_{y}}_{\\text{calendar}}\\big) \\]" +
        "\\where{" + t("$\\Lambda(u)=1/(1+e^{-u})$ (logit); residual load $R_d$ = load $-$ solar $-$ wind (daily means, GW), the demand left for "
                       "other plants; $\\gamma_y$ = year effects; sample @{logit.start|date} -- @{logit.end|date}, $n=$ @{logit.n|,d} days, "
                       "@{logit.n_neg} negative; full table: Appendix F.",
                       "$\\Lambda(u)=1/(1+e^{-u})$ (logit); consumul rezidual $R_d$ = consum $-$ solar $-$ eolian (medii zilnice, GW), adică "
                       "cererea rămasă pentru celelalte centrale; $\\gamma_y$ = efectele anuale; eșantionul: @{logit.start|date} -- "
                       "@{logit.end|date}, $n=$ @{logit.n|,d} " + de("logit.n") + "zile, dintre care @{logit.n_neg} cu prețuri negative; tabelul complet: Anexa F.") + "}",
        it((t("\\textbf{In plain words}", "\\textbf{Interpretare}"),
            t("each extra GW of residual load multiplies the odds of a negative day by @{logit.coef.resid.or|.2f}",
              "fiecare GW în plus de consum rezidual înmulțește șansele unei zile cu prețuri negative cu @{logit.coef.resid.or|.2f}"),
            t("each extra GW of hydro multiplies the odds by @{logit.coef.hydro.or|.2f}",
              "fiecare GW în plus de producție hidro înmulțește șansele cu @{logit.coef.hydro.or|.2f}"),
            t("a weekend day multiplies the odds by @{logit.coef.wkend.or|.2f}", "o zi de weekend înmulțește șansele cu @{logit.coef.wkend.or|.2f}"),
            t("McFadden pseudo-$R^2=$ @{logit.pr2|.3f}", "pseudo-$R^2$ McFadden $=$ @{logit.pr2|.3f}"))),
        t("curtailment of renewables is most likely on spring weekends with full reservoirs.",
          "regenerabilele sînt limitate cel mai probabil în weekendurile de primăvară, cu lacuri pline."),
        tryit=NB + " \\S10d", cite=t("(own estimation, logit; energy-charts.info)", "(estimare proprie, logit; energy-charts.info)"),
        wl="0.61" if ro else "0.57", wr="0.36" if ro else "0.40")
    D.subsection(t("(e) @{Y} so far", "(e) Anul @{Y} pînă acum"))
    D.chart(t("Case study (e): @{Y} prices climbed; oil jumped in March", "Studiul de caz (e): prețuri în creștere, saltul prețului țițeiului în martie"), "cy_prices", [
        t(jan_last + " @{Y}: Romania @{cy.mean.RO|.2f} EUR/MWh (@{cy.chg.RO|+.1f}\\%); " + mlast + " @{cy.lm.RO|.1f} vs @{cy.lm_prev.RO|.1f} a year earlier.",
          jan_last + " @{Y}: România @{cy.mean.RO|.2f} EUR/MWh (@{cy.chg.RO|+.1f}\\%); în " + mlast + ", @{cy.lm.RO|.1f}, față de "
          "@{cy.lm_prev.RO|.1f} cu un an înainte."),
        t("Brent monthly average @{cy.brent.jan_avg|.2f} $\\to$ @{cy.brent.last_avg|.2f} USD/bbl; within March the May contract rose "
          "@{cy.brent.mar_pct|+.1f}\\% (press: Iran conflict, Strait of Hormuz); the @{cy.brent.roll_apr|.1f}\\% on 1 April is a contract roll.",
          "Media lunară Brent: @{cy.brent.jan_avg|.2f} $\\to$ @{cy.brent.last_avg|.2f} USD/bbl; în martie, contractul pentru mai "
          "a crescut cu @{cy.brent.mar_pct|+.1f}\\% (presa: Iran, strîmtoarea Ormuz); "
          "@{cy.brent.roll_apr|.1f}\\% la 1 aprilie: doar trecerea la contractul următor.")], height="0.62\\textheight",
        job=t("budgets set in January were far too low.",
              "bugetele stabilite în ianuarie s-au dovedit mult prea mici."),
        tryit=NB + " \\S10e", cite=t("(energy-charts.info; Yahoo Finance BZ=F; cut-off @{cutoff.end|date})", "(energy-charts.info; Yahoo Finance BZ=F; date pînă la @{cutoff.end|date})"))

    D.chart(t("Case study (e): Cernavodă nuclear plant offline twice, hydro below 2025", "Studiul de caz (e): Cernavodă oprită de două ori, hidro sub 2025"), "cy_generation", [
        t("Nuclear 0 MW on @{nuclear.may_zero_days} days in May and from August (low Danube); " + jan_last +
          " @{mix.lfl.Nuclear.chg|+.1f}\\% on hours reported in both years (lower bound).",
          "Nuclear 0 MW în @{nuclear.may_zero_days} " + de("nuclear.may_zero_days") + "zile din mai și din august (Dunărea scăzută); " + jan_last +
          ": @{mix.lfl.Nuclear.chg|+.1f}\\% pe orele raportate în ambii ani (limită inferioară)."),
        t("Hydro @{nuclear.hydro_aug_oct_chg|+.1f}\\% in Aug--Oct, solar @{mix.lfl.Solar.chg|+.1f}\\% year to date.",
          "Hidro @{nuclear.hydro_aug_oct_chg|+.1f}\\% în aug.--oct., solar @{mix.lfl.Solar.chg|+.1f}\\% de la începutul anului.")], height="0.62\\textheight",
        job=t("one plant can move the national price: read REMIT messages like the weather forecast.",
              "o singură centrală poate muta prețul național: citiți mesajele REMIT ca pe prognoza meteo."),
        tryit=NB + " \\S10e", cite=t("(Nuclearelectrica, 29 Jul @{Y}; World Nuclear News, 30 Jul @{Y}; CNCAN, 9 Sep @{Y})",
                                     "(Nuclearelectrica, 29 iul. @{Y}; World Nuclear News, 30 iul. @{Y}; CNCAN, 9 sep. @{Y})"))

    def chg_cell(key, good_low=True):
        v = V.get(key)
        return heat(v, -40, 40, good_low=good_low, shown=fmt(v, "+.1f", lang))

    rows = [[t("RO price, EUR/MWh", "Preț RO, EUR/MWh"), f("cy.mean_prev.RO", ".2f"), f("cy.mean.RO", ".2f"), chg_cell("cy.chg.RO")],
            [t("DE-LU price, EUR/MWh", "Preț DE-LU, EUR/MWh"), f("cy.mean_prev.DE_LU", ".2f"), f("cy.mean.DE_LU", ".2f"), chg_cell("cy.chg.DE_LU")],
            [t("RO $-$ DE-LU, EUR/MWh", "RO $-$ DE-LU, EUR/MWh"), f("cy.spread_prev", ".1f"), f("cy.spread_ytd", ".1f"), ""],
            [t("RO negative hours", "Ore cu preț negativ, RO"), strip0(f("neg.lfl_prev.RO", ".2f")), strip0(f(f"neg.hours.RO.{Y}", ".2f")), ""],
            [t("RO hydro, TWh", "Hidro RO, TWh"), f("mix.lfl.Hydro.prev", ".2f"), f("mix.lfl.Hydro.ytd", ".2f"), chg_cell("mix.lfl.Hydro.chg", False)],
            [t("RO nuclear, TWh$^{*}$", "Nuclear RO, TWh$^{*}$"), f("mix.lfl.Nuclear.prev", ".2f"), f("mix.lfl.Nuclear.ytd", ".2f"), chg_cell("mix.lfl.Nuclear.chg", False)],
            [t("RO solar, TWh", "Solar RO, TWh"), f("mix.lfl.Solar.prev", ".2f"), f("mix.lfl.Solar.ytd", ".2f"), chg_cell("mix.lfl.Solar.chg", False)],
            [t("RO net imports, TWh", "Import net RO, TWh"), f("mix.lfl_imp.prev", ".2f"), f("mix.lfl_imp.ytd", ".2f"), ""]]
    D.frame(t("Case study (e): @{Y} drivers --- price up about 30\\%, supply down", "Studiul de caz (e): prețuri cu circa 30\\% mai mari, ofertă mai mică"),
            "\\begin{center}" + table("@{}lrrr@{}", [jan_last, "@{YP}", "@{Y}", t("\\% chg", "var. \\%")], rows, size="small", stretch="1.08") + "\\end{center}" +
            "\n\\vspace{-3mm}" + note(t("Green = favourable for a consumer, red = unfavourable; cut-off @{cutoff.end|date}.",
                                        "Verde = favorabil pentru consumator, roșu = nefavorabil; date pînă la @{cutoff.end|date}."),
                                      t("$^{*}$Hours reported in both years (lower bound).", "$^{*}$Numai orele raportate în ambii ani (limită inferioară).")) +
            D.bottom(t("price up by about 30\\%, with nuclear, hydro and oil all pointing the same way, and a hedge paid for itself.",
                       "prețul a crescut cu circa 30\\%, cu nuclearul, hidro și țițeiul în aceeași direcție, iar acoperirea riscului s-a dovedit rentabilă."),
                     NB + " \\S10e"), "small", cite=t("(own computation; energy-charts.info)", "(calcule proprii; energy-charts.info)"))

    D.figframe(t("Case study (e): @{Y} extremes in Romania and on Brent", "Studiul de caz (e): valorile extreme din @{Y}, România și Brent"),
               None, None, "cy_extremes", [
        (t("\\textbf{Romania}", "\\textbf{România}"),
         t("daily base price: high @{cy.ro_max_day|.2f} EUR/MWh on @{cy.ro_max_day_date|date}, low @{cy.ro_min_day|.2f} on @{cy.ro_min_day_date|date}",
           "prețul de bază zilnic: maximul, @{cy.ro_max_day|.2f} EUR/MWh, la @{cy.ro_max_day_date|date}; minimul, @{cy.ro_min_day|.2f}, la @{cy.ro_min_day_date|date}"),
         t("quarter-hour: high @{cy.ro_max_mtu|.2f} on @{cy.ro_max_mtu_ts|dt}, low @{cy.ro_min_mtu|.2f} on @{cy.ro_min_mtu_ts|dt} (CET/CEST)",
           "sfertul de oră: maximul, @{cy.ro_max_mtu|.2f}, la @{cy.ro_max_mtu_ts|dt}; minimul, @{cy.ro_min_mtu|.2f}, la @{cy.ro_min_mtu_ts|dt} (CET/CEST)"))],
               tryit=NB + " \\S10e", height="0.55\\textheight",
               cite=t("(own computation; energy-charts.info; Yahoo Finance)", "(calcule proprii; energy-charts.info; Yahoo Finance)"))
    D.frame(t("Case study (e): @{Y} extremes in Germany and on Brent", "Studiul de caz (e): valorile extreme din @{Y}, Germania și Brent"), it(
        (t("\\textbf{Germany}", "\\textbf{Germania}"),
         t("lowest quarter-hour @{cy.de_min_mtu|.2f} on @{cy.de_min_mtu_ts|dt}, at the $-500$ floor then in force",
           "minimul pe sfert de oră: @{cy.de_min_mtu|.2f}, la @{cy.de_min_mtu_ts|dt}, egal cu pragul de atunci"),
         t("after such prices on 26 April and 1 May, the floor became $-600$ for delivery from 29 May 2026",
           "după 26 aprilie și 1 mai, pragul a coborît la $-600$, din 29 mai 2026")),
        (t("\\textbf{Brent}", "\\textbf{Țițeiul Brent}"),
         t("highest close @{cy.brent.max|.2f} USD/bbl on @{cy.brent.max_date|date}",
           "cel mai mare preț de închidere: @{cy.brent.max|.2f} USD/bbl, la @{cy.brent.max_date|date}"),
         t("largest daily change excluding contract rolls: @{cy.brent.max_move|+.2f}\\% on @{cy.brent.max_move_date|date}",
           "cea mai mare variație zilnică (fără schimbările de contract): @{cy.brent.max_move|+.2f}\\%, la @{cy.brent.max_move_date|date}")), sep="2pt") +
        D.bottom(t("set risk limits on the extremes, not on the averages.", "stabiliți limitele de risc pe baza valorilor extreme, nu a mediilor."), NB + " \\S10e"),
        "small", cite=t("(own computation; OPCOM SDAC note, 7 May 2026)", "(calcule proprii; nota SDAC a OPCOM, 7 mai 2026)"))

    D.subsection(t("(f) Romania, Bulgaria and batteries", "(f) România, Bulgaria și bateriile"))
    bt = N["bat"]
    D.chart(t("Case study (f): since spring @{Y}, Bulgaria's evenings are cheaper",
              "Studiul de caz (f): din primăvara lui @{Y}, Bulgaria are prețuri mai mici seara"), "bg_battery", [
        t("Evenings 19:00--22:00 local time (EET), Apr--Sep, RO vs BG; @{bat.evening.2025.RO|.1f} vs @{bat.evening.2025.BG|.1f} EUR/MWh (2025), "
          "@{bat.evening.@{Y}.RO|.1f} vs @{bat.evening.@{Y}.BG|.1f} (@{Y}); middays 11:00--15:00 close in @{Y} (@{bat.midday.@{Y}.RO|.1f} vs "
          "@{bat.midday.@{Y}.BG|.1f}).",
          "Seara, 19:00--22:00 ora locală (EET), apr.--sep., RO față de BG; @{bat.evening.2025.RO|.1f} față de @{bat.evening.2025.BG|.1f} EUR/MWh (2025), "
          "@{bat.evening.@{Y}.RO|.1f} față de @{bat.evening.@{Y}.BG|.1f} (@{Y}); la amiază (11:00--15:00), prețuri apropiate în @{Y} "
          "(@{bat.midday.@{Y}.RO|.1f} față de @{bat.midday.@{Y}.BG|.1f})."),
        t("Battery data start only @{bat.bg_first|date}, after the gap opened (@{bat.gap_open|ym}); an association, not proof.",
          "Datele despre baterii încep abia la @{bat.bg_first|date}, după apariția diferenței (@{bat.gap_open|ym}); este o asociere, nu o dovadă.")],
        height="0.60\\textheight",
        job=t("a Romanian battery developer competes for the same evening spread (Lecture 6).",
              "un dezvoltator român de stocare concurează pentru aceeași diferență de preț de seară (cursul 6)."),
        tryit=NB + " \\S10f", cite=t("(energy-charts.info; data source: ENTSO-E; own computation, local time EET)",
                                     "(energy-charts.info; sursa datelor: ENTSO-E; calcule proprii, ora locală EET)"))

    # ------------------------------------------------------------------ wrap-up
    D.parts.append("\\section*{" + t("Wrap-up", "Recapitulare") + "}\n")
    D.quiz_frame(t("counting negative prices", "numărarea prețurilor negative"),
                 t("In a month after 1 October 2025, 48 of Romania's quarter-hour prices were negative; a board member asks how many "
                   "negative hours there were; what do you answer?",
                   "Într-o lună de după 1 octombrie 2025, 48 de prețuri pe sfert de oră din România au fost negative; un membru al "
                   "consiliului de administrație vă întreabă cîte ore cu preț negativ au fost; ce îi răspundeți?"),
                 t("$48\\times15/60=12$ hour-equivalents; saying 48 ``hours'' overstates by a factor of 4 against earlier, hourly years; "
                   "best answer: ``48 quarter-hours (12 hours)''.",
                   "$48\\times15/60=12$ ore echivalente; dacă spuneți „48 de ore”, supraevaluați durata de 4 ori față de anii anteriori, cu "
                   "intervale orare; formularea corectă: „48 de sferturi de oră (12 ore)”."))
    D.quiz_frame(t("reading an autocorrelation", "citirea unei autocorelații"),
                 t("Your analyst says: ``the PZU price autocorrelation is 0.98 at lag 1 and 0.90 at lag 30, so prices are white noise and "
                   "last month tells us nothing''; is this right?",
                   "Un analist din echipa dumneavoastră afirmă: „autocorelația prețului PZU este 0{,}98 la decalajul 1 și 0{,}90 la decalajul 30, "
                   "deci prețurile sînt zgomot alb, iar luna trecută nu ne spune nimic”; are dreptate?"),
                 t("No: white noise has autocorrelations near 0; values near 1 mean strong persistence, i.e.\\ a unit root or a very slow "
                   "mean reversion; run ADF and KPSS and look at the autocorrelation of daily changes.",
                   "Nu: zgomotul alb are autocorelații apropiate de 0; valorile apropiate de 1 indică o persistență puternică, adică o "
                   "rădăcină unitară sau o revenire foarte lentă la medie; aplicați testele ADF și KPSS și examinați autocorelația variațiilor zilnice."))

    D.frame(t("Wrap-up", "Recapitulare"), "\\vspace{-2mm}\\begin{multicols}{2}\\scriptsize\\tableofcontents\\end{multicols}\n" + it(
        t("One auction per day, coupled across Europe, with 96 quarter-hours since Oct 2025; count in hour-equivalents.",
          "O singură licitație pe zi, cuplată la nivel european, cu 96 de sferturi de oră din oct. 2025; numărați în ore echivalente."),
        t("Benchmark to beat: the naive forecast (Romania @{YP}: MAE @{naive.RO.@{YP}.naive|.2f} EUR/MWh); next: forecasting (Lecture 2).",
          "Reperul de depășit: prognoza naivă (România, @{YP}: MAE @{naive.RO.@{YP}.naive|.2f} EUR/MWh); urmează prognoza (cursul 2)."),
        sep="1pt"))

    D.frame(t("Research from our group on the Romanian market", "Cercetările grupului nostru despre piața din România"), it(
        t("\\textbf{The summer-2024 crisis} (Case c): a counterfactual analysis of Romania's June--July 2024 price crisis on ENTSO-E hourly "
          "data; a 10\\% demand reduction is the robust first-tier intervention, and the peak fell in hours with almost no solar "
          "(Andrei, Pele \\& Cramer, 2026, PICBE).",
          "\\textbf{Criza din vara lui 2024} (studiul de caz c): analiză contrafactuală a crizei prețurilor din România din iunie--iulie 2024, "
          "pe date orare ENTSO-E; reducerea cererii cu 10\\% este cea mai robustă dintre intervențiile prioritare, iar vîrful de preț s-a produs "
          "în ore aproape fără producție solară (Andrei, Pele \\& Cramer, 2026, PICBE)."),
        t("\\textbf{Explaining price forecasts}: which drivers matter at which horizon (0--6 h up to two weeks) and in which price "
          "regime, for Romanian hourly prices 2018--2024 (Andrei, Pele \\& Cramer, 2026, PICBE) --- preview of Lecture 7.",
          "\\textbf{Explicarea prognozelor de preț}: ce factori contează la fiecare orizont (de la 0--6 ore pînă la două săptămîni) "
          "și în fiecare regim de preț, pentru prețurile orare românești 2018--2024 (Andrei, Pele \\& Cramer, 2026, PICBE) --- "
          "tema cursului 7."),
        t("\\textbf{Forecasting national consumption}: classical seasonal models against neural networks on Romanian load "
          "(Proșcanu, Proșcanu, Pele \\& Costea, 2025, Romanian J.\\ Economic Forecasting) --- preview of Lecture 2.",
          "\\textbf{Prognoza consumului național}: modele sezoniere clasice comparate cu rețele neuronale, pe consumul României "
          "(Proșcanu, Proșcanu, Pele \\& Costea, 2025, Romanian J.\\ Economic Forecasting) --- tema cursului 2."),
        t("\\textbf{Demand barely reacts to price}: Romanian consumption is price-inelastic; Granger causality runs from consumption to price, "
          "not back (Proșcanu, Proșcanu \\& Pele, 2025, J.\\ Social and Economic Statistics) --- why the demand curve is steep.",
          "\\textbf{Cererea abia reacționează la preț}: consumul din România este inelastic la preț; cauzalitatea în sens Granger merge de la consum "
          "la preț, nu invers (Proșcanu, Proșcanu \\& Pele, 2025, J.\\ Social and Economic Statistics) --- de aceea curba cererii "
          "este abruptă."),
        t("\\textbf{Does liberalisation lower prices?} Causal machine learning on US market liberalisation finds a short-term "
          "price decrease of about 7\\% (Shahar, Lessmann \\& Pele, 2025, arXiv 2507.12331).",
          "\\textbf{Scade liberalizarea prețurile?} Metodele cauzale de învățare automată aplicate liberalizării piețelor din Statele Unite "
          "indică o scădere a prețului de circa 7\\% pe termen scurt (Shahar, Lessmann \\& Pele, 2025, arXiv 2507.12331)."),
        sep="3pt") + note(t("Findings as stated in the papers' abstracts; numbers on the other slides come from our own data.",
                            "Rezultatele sînt preluate din rezumatele lucrărilor; cifrele de pe celelalte diapozitive provin din datele noastre.")),
        "footnotesize", cite=t("(Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting)", "(Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică)"))

    D.frame(t("Want to learn more?", "Vreți să aflați mai mult?"), cols(it(
        t("\\textbf{R.\\ Weron, IIF Distinguished Lectures on electricity price forecasting} (2025): slides ",
          "\\textbf{R.\\ Weron, IIF Distinguished Lectures despre prognoza prețurilor energiei electrice} (2025): prezentări ") +
        "\\href{https://p.wz.pwr.edu.pl/~weron.rafal/assets/PDF/Weron25_IIF_1.pdf}{" + t("part I", "partea I") + "}, "
        "\\href{https://p.wz.pwr.edu.pl/~weron.rafal/assets/PDF/Weron25_IIF_2.pdf}{" + t("part II", "partea a II-a") + "}, "
        "\\href{https://github.com/lipiecki/energy-analytics-2025}{" + t("notebooks", "notebook-uri Jupyter") + "}, "
        "\\href{https://www.youtube.com/playlist?list=PLUxduCQo6_X2UTvdP9OE8DwfuBClKFNur}{" + t("videos", "înregistrări video") + "}.",
        t("\\textbf{epftoolbox}, the open benchmark of Lago et al.\\ (2021): ", "\\textbf{epftoolbox}, setul de evaluare cu acces liber realizat de Lago et al.\\ (2021): ") +
        "\\href{https://github.com/jeslago/epftoolbox}{github.com/jeslago/epftoolbox}.",
        "\\textbf{Forecasting: Principles and Practice}, " + t("3rd ed.", "ed.\\ a 3-a") + ": \\href{https://otexts.com/fpp3/}{otexts.com/fpp3}.", sep="4pt"),
        it(t("\\textbf{This course}: code, data, notebooks --- ", "\\textbf{Acest curs}: cod, date, notebook-uri Jupyter --- ") +
           "\\href{https://github.com/danpele/EMQA}{github.com/danpele/EMQA}.",
           t("\\textbf{Data and rules}: ", "\\textbf{Date și reguli}: ") + "\\href{https://www.energy-charts.info}{energy-charts.info}, "
           "\\href{https://transparency.entsoe.eu}{" + t("ENTSO-E Transparency Platform", "platforma de transparență ENTSO-E") + "}, "
           "\\href{https://www.opcom.ro}{opcom.ro}, \\href{https://www.transelectrica.ro}{transelectrica.ro}, \\href{https://www.jao.eu}{jao.eu}.",
           t("\\textbf{Experiment yourself}: the notebook reproduces every chart and number of this lecture --- ",
             "\\textbf{Încercați singuri}: notebook-ul Jupyter reproduce fiecare grafic și fiecare cifră din acest curs --- ") +
           "\\href{\\emqarepo/\\emqanb}{notebooks/}.", sep="4pt"), "0.52", "0.45"))

    REFS = [
        "Andrei, A.-V., Pele, D.-T.\\ \\& Cramer, A.-A.\\ (2026). Evaluating intervention effectiveness during extreme price events: A "
        "counterfactual analysis of Romania's 2024 energy crisis. \\textit{Proceedings of the International Conference on Business "
        "Excellence}, 20(1), 84--103. \\href{https://doi.org/10.2478/picbe-2026-0013}{doi:10.2478/picbe-2026-0013}",
        "Andrei, A.-V., Pele, D.-T.\\ \\& Cramer, A.-A.\\ (2026). Multi-horizon explainability in energy price forecasting: Disentangling "
        "market dynamics and renewable intermittency in Romania's liberalized electricity market. \\textit{Proceedings of the "
        "International Conference on Business Excellence}, 20(1), 104--117. \\href{https://doi.org/10.2478/picbe-2026-0014}{doi:10.2478/picbe-2026-0014}",
        "Cleveland, R.\\,B., Cleveland, W.\\,S., McRae, J.\\,E.\\ \\& Terpenning, I.\\ (1990). STL: A seasonal-trend decomposition "
        "procedure based on loess. \\textit{Journal of Official Statistics}, 6(1), 3--73. "
        "\\href{https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/stl-a-seasonal-trend-decomposition-procedure-based-on-loess.pdf}{scb.se}",
        "Dickey, D.\\,A.\\ \\& Fuller, W.\\,A.\\ (1979). Distribution of the estimators for autoregressive time series with a unit root. "
        "\\textit{Journal of the American Statistical Association}, 74(366), 427--431. \\href{https://doi.org/10.1080/01621459.1979.10482531}{doi:10.1080/01621459.1979.10482531}",
        "Hyndman, R.\\,J.\\ \\& Athanasopoulos, G.\\ (2021). \\textit{Forecasting: Principles and Practice}, 3rd ed. OTexts. \\href{https://otexts.com/fpp3/}{otexts.com/fpp3}",
        "Janczura, J., Trück, S., Weron, R.\\ \\& Wolff, R.\\,C.\\ (2013). Identifying spikes and seasonal components in electricity spot "
        "price data: A guide to robust modeling. \\textit{Energy Economics}, 38, 96--110. \\href{https://doi.org/10.1016/j.eneco.2013.03.013}{doi:10.1016/j.eneco.2013.03.013}",
        "Jarque, C.\\,M.\\ \\& Bera, A.\\,K.\\ (1980). Efficient tests for normality, homoscedasticity and serial independence of "
        "regression residuals. \\textit{Economics Letters}, 6(3), 255--259. \\href{https://doi.org/10.1016/0165-1765(80)90024-5}{doi:10.1016/0165-1765(80)90024-5}",
        "Kwiatkowski, D., Phillips, P.\\,C.\\,B., Schmidt, P.\\ \\& Shin, Y.\\ (1992). Testing the null hypothesis of stationarity against "
        "the alternative of a unit root. \\textit{Journal of Econometrics}, 54(1--3), 159--178. \\href{https://doi.org/10.1016/0304-4076(92)90104-Y}{doi:10.1016/0304-4076(92)90104-Y}",
        "Lago, J., Marcjasz, G., De Schutter, B.\\ \\& Weron, R.\\ (2021). Forecasting day-ahead electricity prices: A review of "
        "state-of-the-art algorithms, best practices and an open-access benchmark. \\textit{Applied Energy}, 293, 116983. "
        "\\href{https://doi.org/10.1016/j.apenergy.2021.116983}{doi:10.1016/j.apenergy.2021.116983}",
        "Ljung, G.\\,M.\\ \\& Box, G.\\,E.\\,P.\\ (1978). On a measure of lack of fit in time series models. \\textit{Biometrika}, 65(2), "
        "297--303. \\href{https://doi.org/10.1093/biomet/65.2.297}{doi:10.1093/biomet/65.2.297}",
        "Maciejowska, K., Uniejewski, B.\\ \\& Weron, R.\\ (2023). Forecasting electricity prices. \\textit{Oxford Research Encyclopedia "
        "of Economics and Finance}. \\href{https://doi.org/10.1093/acrefore/9780190625979.013.667}{doi:10.1093/acrefore/9780190625979.013.667}",
        "MacKinnon, J.\\,G.\\ (1996). Numerical distribution functions for unit root and cointegration tests. "
        "\\textit{Journal of Applied Econometrics}, 11(6), 601--618. "
        "\\href{https://doi.org/10.1002/(SICI)1099-1255(199611)11:6\\%3C601::AID-JAE417\\%3E3.0.CO;2-T}{doi.org (Wiley)}",
        "Nogales, F.\\,J., Contreras, J., Conejo, A.\\,J.\\ \\& Espínola, R.\\ (2002). Forecasting next-day electricity prices by time "
        "series models. \\textit{IEEE Transactions on Power Systems}, 17(2), 342--348. \\href{https://doi.org/10.1109/TPWRS.2002.1007902}{doi:10.1109/TPWRS.2002.1007902}",
        "Proșcanu, C.\\,A., Proșcanu, M.\\,E., Pele, D.\\,T.\\ \\& Costea, A.\\ (2025). Watt's next? Benchmarking time series models on "
        "Romania's national electricity consumption. \\textit{Romanian Journal of Economic Forecasting}, issue 3, 146--163. "
        "\\href{https://ipe.ro/ftp/RePEc/rjef3_2025/rjef3_2025p146-163.pdf}{ipe.ro}",
        "Proșcanu, C., Proșcanu, M.\\ \\& Pele, D.\\,T.\\ (2025). The price elasticity of electricity demand in Romania. \\textit{Journal "
        "of Social and Economic Statistics}, 14(2), 131--141. \\href{https://doi.org/10.2478/jses-2025-0009}{doi:10.2478/jses-2025-0009}",
        "Said, S.\\,E.\\ \\& Dickey, D.\\,A.\\ (1984). Testing for unit roots in autoregressive-moving average models of unknown order. "
        "\\textit{Biometrika}, 71(3), 599--607. \\href{https://doi.org/10.1093/biomet/71.3.599}{doi:10.1093/biomet/71.3.599}",
        "Shahar, O., Lessmann, S.\\ \\& Pele, D.\\,T.\\ (2025). Causality analysis of electricity market liberalization on electricity "
        "price using novel machine learning methods. \\href{https://arxiv.org/abs/2507.12331}{arXiv:2507.12331}",
        "Uniejewski, B., Weron, R.\\ \\& Ziel, F.\\ (2018). Variance stabilizing transformations for electricity spot price forecasting. "
        "\\textit{IEEE Transactions on Power Systems}, 33(2), 2219--2229. \\href{https://doi.org/10.1109/TPWRS.2017.2734563}{doi:10.1109/TPWRS.2017.2734563}",
        "Weron, R.\\ (2014). Electricity price forecasting: A review of the state-of-the-art with a look into the future. "
        "\\textit{International Journal of Forecasting}, 30(4), 1030--1081. \\href{https://doi.org/10.1016/j.ijforecast.2014.08.008}{doi:10.1016/j.ijforecast.2014.08.008}",
        "Ziel, F.\\ \\& Weron, R.\\ (2018). Day-ahead electricity price forecasting with high-dimensional structures: Univariate vs.\\ "
        "multivariate modeling frameworks. \\textit{Energy Economics}, 70, 396--420. \\href{https://doi.org/10.1016/j.eneco.2017.12.016}{doi:10.1016/j.eneco.2017.12.016}",
        t("Market and event sources: OPCOM press releases " + "\\href{https://opcom.ro/uploads/doc/Comunicate/Lansare\\%20PI\\%20OPCOM\\%20in\\%20SIDC_19.11.2019_EN.pdf}{19 Nov 2019} (\\href{https://gme.mercatoelettrico.org/Portals/0/Documents/it-IT/20191128_Press_release_for_2nd_wave_successful_go-livev1.0.pdf}{SIDC joint release}), \\href{https://opcom.ro/uploads/doc/Comunicate/211027\\%20PR\\%20successful\\%20go-live\\%20BG-RO\\%20border_EN.pdf}{27 Oct 2021} (\\href{https://www.ote-cr.cz/en/about-ote/ote-news/inclusion-of-the-bulgarian-romanian-border-to-the-single-day-ahead-coupling-sdac}{SDAC release}), \\href{https://www.opcom.ro/uploads/doc/Comunicate/SIDC\\%2015\\%20Min\\%20MTU\\%20Go-Live\\%205th\\%20Wave_EN.pdf}{19 Mar 2025} (\\href{https://hupx.hu/2025/03/20/new-milestone-single-intraday-market-coupling}{HUPX}), \\href{https://www.nemo-committee.eu/assets/files/15-minute-mtu-in-sdac-was-implemented.pdf}{1 Oct 2025 (SDAC)}; " +
          "\\href{https://www.nemo-committee.eu/assets/files/harmonised-minimum-clearing-price-for-sdac-to-be-set-to-600-eur-per-mwh-starting-from-the-28th-may-2026-(trading-date).pdf}{SDAC note} (7 May 2026, minimum price $-600$ from delivery 29 May 2026); Nuclearelectrica current reports "
          "\\href{https://bvb.ro/infocont/infocont26/SNN_20260727190124_RC-SNN-raport-curent-debit-dunare---bvb.pdf}{27 Jul 2026} and \\href{https://bvb.ro/infocont/infocont26/SNN_20260729175811_RC-SNN-raport-curent-oprire-u-2---bvb.pdf}{29 Jul 2026}; \\href{https://www.world-nuclear-news.org/articles/danubes-record-low-leads-to-hungary-romania-nuclear-shutdowns}{World Nuclear News} (30 Jul 2026); "
          "statement of the National Commission for Nuclear Activities Control (CNCAN) on Cernavodă, \\href{https://www.cncan.ro/comunicate/cncan-monitorizeaza-situatia-de-la-cne-cernavoda-in-contextul-conditiilor-hidrologice-de-pe-dunare}{9 Sep 2026}; "
          "press report on the Strait of Hormuz (\\href{https://www.semafor.com/article/03/12/2026/oil-prices-rise-above-100-again-over-strait-of-hormuz-attacks}{Semafor, 12 Mar 2026}).",
          "Surse pentru piață și evenimente: comunicatele OPCOM " + "\\href{https://opcom.ro/uploads/doc/Comunicate/Lansare\\%20PI\\%20OPCOM\\%20in\\%20SIDC_19.11.2019_EN.pdf}{19 nov. 2019} (\\href{https://gme.mercatoelettrico.org/Portals/0/Documents/it-IT/20191128_Press_release_for_2nd_wave_successful_go-livev1.0.pdf}{comunicat comun SIDC}), \\href{https://opcom.ro/uploads/doc/Comunicate/211027\\%20PR\\%20successful\\%20go-live\\%20BG-RO\\%20border_EN.pdf}{27 oct. 2021} (\\href{https://www.ote-cr.cz/en/about-ote/ote-news/inclusion-of-the-bulgarian-romanian-border-to-the-single-day-ahead-coupling-sdac}{comunicat SDAC}), \\href{https://www.opcom.ro/uploads/doc/Comunicate/SIDC\\%2015\\%20Min\\%20MTU\\%20Go-Live\\%205th\\%20Wave_EN.pdf}{19 mar. 2025} (\\href{https://hupx.hu/2025/03/20/new-milestone-single-intraday-market-coupling}{HUPX}), \\href{https://www.nemo-committee.eu/assets/files/15-minute-mtu-in-sdac-was-implemented.pdf}{1 oct. 2025 (SDAC)}; " +
          "\\href{https://www.nemo-committee.eu/assets/files/harmonised-minimum-clearing-price-for-sdac-to-be-set-to-600-eur-per-mwh-starting-from-the-28th-may-2026-(trading-date).pdf}{nota SDAC} (7 mai 2026, preț minim $-600$ pentru livrări din 29 mai 2026); rapoartele curente Nuclearelectrica "
          "\\href{https://bvb.ro/infocont/infocont26/SNN_20260727190124_RC-SNN-raport-curent-debit-dunare---bvb.pdf}{27 iul. 2026} și \\href{https://bvb.ro/infocont/infocont26/SNN_20260729175811_RC-SNN-raport-curent-oprire-u-2---bvb.pdf}{29 iul. 2026}; \\href{https://www.world-nuclear-news.org/articles/danubes-record-low-leads-to-hungary-romania-nuclear-shutdowns}{World Nuclear News} (30 iul. 2026); "
          "comunicatul Comisiei Naționale pentru Controlul Activităților Nucleare (CNCAN) despre Cernavodă, \\href{https://www.cncan.ro/comunicate/cncan-monitorizeaza-situatia-de-la-cne-cernavoda-in-contextul-conditiilor-hidrologice-de-pe-dunare}{9 sep. 2026}; "
          "presa despre strîmtoarea Ormuz (\\href{https://www.semafor.com/article/03/12/2026/oil-prices-rise-above-100-again-over-strait-of-hormuz-attacks}{Semafor, 12 mar. 2026})."),
    ]
    D.frame(t("References (1/2)", "Bibliografie (1/2)"), "\\begin{itemize}\\setlength{\\itemsep}{0pt}\\scriptsize\n" +
            "\n".join("\\item " + r for r in REFS[:11]) + "\n\\end{itemize}", "scriptsize")
    D.frame(t("References (2/2)", "Bibliografie (2/2)"), "\\begin{itemize}\\setlength{\\itemsep}{0pt}\\scriptsize\n" +
            "\n".join("\\item " + r for r in REFS[11:]) + "\n\\end{itemize}", "scriptsize")

    # ------------------------------------------------------------------ appendix (not counted in the main deck)
    D.mark_main_end()
    D.parts.append("\\section*{" + t("Appendix", "Anexă") + "}\n")
    D.frame(t("Appendix A: ADF and KPSS in full", "Anexa A: testele ADF și KPSS în detaliu"), cols(
        block("ADF (Said \\& Dickey, 1984)",
              "\\[ \\Delta x_t=\\alpha+\\beta t+\\gamma x_{t-1}+\\sum_{j=1}^{p}\\delta_j\\Delta x_{t-j}+u_t \\]" + it(
              t("$H_0:\\gamma=0$ vs $H_1:\\gamma<0$; $\\tau=\\hat\\gamma/\\mathrm{se}(\\hat\\gamma)$ follows the Dickey--Fuller distribution; "
                "$p$-values from MacKinnon (1996).",
                "$H_0:\\gamma=0$ față de $H_1:\\gamma<0$; $\\tau=\\hat\\gamma/\\mathrm{se}(\\hat\\gamma)$ urmează distribuția Dickey--Fuller; "
                "valorile $p$ se calculează după MacKinnon (1996)."),
              t("Lag order: minimise AIC starting from $p_{\\max}=12(T/100)^{1/4}$.",
                "Numărul de decalaje: minimizarea AIC, pornind de la $p_{\\max}=12(T/100)^{1/4}$."),
              t("Deterministic terms must match the alternative; constant: level-stationary; trend: trend-stationary.",
                "Termenii determiniști trebuie să corespundă ipotezei alternative; constantă: staționaritate în nivel; trend: "
                "staționaritate în jurul trendului."), sep="1pt")),
        block("KPSS (Kwiatkowski et al., 1992)",
              "\\[ \\mathrm{KPSS}=\\frac{1}{T^2\\hat\\sigma^2_{\\mathrm{LR}}}\\sum_{t=1}^T S_t^2,\\quad S_t=\\sum_{s\\le t}e_s \\]"
              "\\[ \\hat\\sigma^2_{\\mathrm{LR}}=\\hat\\gamma_0+2\\sum_{k=1}^{\\ell}\\Big(1-\\frac{k}{\\ell+1}\\Big)\\hat\\gamma_k \\]" + it(
              t("$e_s$ = residuals from a regression on a constant (and trend).",
                "$e_s$ = reziduurile regresiei pe o constantă (și pe trend)."),
              t("Bartlett kernel with bandwidth $\\ell$ (Hobijn et al.\\ rule in statsmodels); critical value 0.463 (5\\%, level).",
                "Nucleu Bartlett cu lățimea de bandă $\\ell$ (regula Hobijn et al.\\ din statsmodels); valoarea critică 0{,}463 (5\\%, nivel)."),
              sep="1pt")), "0.49", "0.49"), "small")
    D.frame(t("Appendix B: classical decomposition, worked example", "Anexa B: descompunerea clasică, exemplu de calcul"), cols(
        "\\[ \\hat T_t=\\tfrac{1}{24}x_{t-6}+\\tfrac{1}{12}\\textstyle\\sum_{j=-5}^{5}x_{t+j}+\\tfrac{1}{24}x_{t+6} \\]" + it(
            t("First trend value, @{decomp.ex.date|ym}: $\\hat T=\\frac{1}{24}(@{decomp.ex.y_first|.3f}+@{decomp.ex.y_last|.3f})+"
              "\\frac{1}{12}\\cdot @{decomp.ex.sum_mid|.3f}=$ @{decomp.ex.cma|.3f} GW (Jan 2016 and Jan 2017 at half weight; "
              "Feb--Dec 2016 summed).",
              "Prima valoare a trendului, @{decomp.ex.date|ym}: $\\hat T=\\frac{1}{24}(@{decomp.ex.y_first|.3f}+@{decomp.ex.y_last|.3f})+"
              "\\frac{1}{12}\\cdot @{decomp.ex.sum_mid|.3f}=$ @{decomp.ex.cma|.3f} GW (ian. 2016 și ian. 2017 cu pondere înjumătățită; "
              "feb.--dec. 2016 însumate)."),
            t("Observed @{decomp.ex.y|.3f} GW $\\Rightarrow$ deviation @{decomp.ex.detr|.3f}.", "Valoarea observată, @{decomp.ex.y|.3f} GW $\\Rightarrow$ abaterea @{decomp.ex.detr|.3f}."),
            t("Seasonal index: $\\hat S_j=\\bar d_j-\\frac1{12}\\sum_i\\bar d_i$ (raw means summed to @{decomp.raw_mean|.4f}).",
              "Indicele sezonier: $\\hat S_j=\\bar d_j-\\frac1{12}\\sum_i\\bar d_i$ (suma mediilor brute: @{decomp.raw_mean|.4f})."), sep="3pt"),
        table("@{}lr@{\\hspace{6mm}}lr@{}", [t("Month", "Luna"), "$\\hat S_j$", t("Month", "Luna"), "$\\hat S_j$"],
              [[MON[i + 1][:3], f(f"decomp.sidx.{m1}", ".3f"), MON[i + 7][:3], f(f"decomp.sidx.{m2}", ".3f")]
               for i, (m1, m2) in enumerate(zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]))],
              size="footnotesize", stretch="1.2") +
        note(t("Romanian load (GW), @{decomp.start|ym} -- @{decomp.end|ym}; checked against statsmodels.",
               "Consumul României (GW), @{decomp.start|ym} -- @{decomp.end|ym}; rezultate verificate cu statsmodels.")), "0.56", "0.40"), "small")
    D.frame(t("Appendix C: the STL algorithm", "Anexa C: algoritmul STL"), it(
        t("\\textbf{Inner loop} (repeated): (1) detrend, $x_t-\\hat T_t$; (2) smooth each month's sub-series (all Januaries, all Februaries, "
          "\\dots) by loess with span $n_s$; (3) remove its low-frequency part $\\Rightarrow\\hat S_t$; (4) smooth $x_t-\\hat S_t$ by loess "
          "with span $n_t$ $\\Rightarrow\\hat T_t$.",
          "\\textbf{Bucla interioară} (repetată): (1) eliminarea trendului, $x_t-\\hat T_t$; (2) netezirea fiecărei subserii lunare "
          "(toate lunile ianuarie, toate lunile februarie, \\dots) prin loess cu fereastra $n_s$; (3) eliminarea componentei de "
          "frecvență joasă $\\Rightarrow\\hat S_t$; (4) netezirea lui $x_t-\\hat S_t$ prin loess cu fereastra $n_t$ $\\Rightarrow\\hat T_t$."),
        t("\\textbf{Outer loop}: robustness weights $\\rho_t=B\\big(|\\hat R_t|/(6\\,\\mathrm{median}|\\hat R|)\\big)$, $B(u)=(1-u^2)^2$ for "
          "$|u|<1$, else 0, so outliers count less in the next inner loop.",
          "\\textbf{Bucla exterioară}: ponderi de robustețe $\\rho_t=B\\big(|\\hat R_t|/(6\\,\\mathrm{median}|\\hat R|)\\big)$, "
          "$B(u)=(1-u^2)^2$ pentru $|u|<1$, altfel 0, astfel că valorile extreme cîntăresc mai puțin în bucla următoare."),
        t("Here: period 12, $n_s=13$, robust; strength of seasonality $1-\\Var(R)/\\Var(S+R)=$ @{decomp.fs|.3f}.",
          "Aici: perioada 12, $n_s=13$, varianta robustă; intensitatea sezonalității: $1-\\Var(R)/\\Var(S+R)=$ @{decomp.fs|.3f}."),
        t("Additive only: for multiplicative seasonality apply STL to $\\ln x_t$ (or asinh for prices).",
          "Numai pentru modelul aditiv: în cazul sezonalității multiplicative, aplicați STL seriei transformate prin $\\ln x_t$ (sau prin asinh, pentru prețuri)."), sep="5pt"),
        "small", cite="(Cleveland, Cleveland, McRae \\& Terpenning, 1990, JOS)")
    D.frame(t("Appendix D: generation mix in numbers", "Anexa D: mixul de producție în cifre"), "\\begin{center}" + MIXTAB + "\\end{center}",
            "small", cite=t("(energy-charts.info; data source: ENTSO-E)", "(energy-charts.info; sursa datelor: ENTSO-E)"))
    D.frame(t("Appendix E: naive benchmark, all years", "Anexa E: prognoza naivă, toți anii"), "\\begin{center}" + NAIVETAB + "\\end{center}" +
            note(t("MAE in EUR/MWh on hourly prices (from Oct 2025: hourly mean of the 15-min prices).",
                    "MAE în EUR/MWh, pe prețuri orare (din oct. 2025: media orară a prețurilor pe 15 minute)."),
                  t("Green = best of the three in that year and zone.", "Verde = cea mai bună dintre cele trei variante, în anul și zona respective.")), "small",
            cite="(Nogales et al., 2002, IEEE TPWRS; Weron, 2014, IJF)")
    D.frame(t("Appendix F: fat tails and the negative-day logit in full", "Anexa F: cozile groase și modelul logit, în detaliu"), cols(
        "\\[ \\hat S=\\frac{\\frac1T\\sum_t(r_t-\\bar r)^3}{\\hat\\sigma^3},\\quad \\hat K=\\frac{\\frac1T\\sum_t(r_t-\\bar r)^4}{\\hat\\sigma^4} \\]"
        "\\[ \\mathrm{JB}=\\frac T6\\Big(\\hat S^2+\\frac{(\\hat K-3)^2}{4}\\Big)\\sim\\chi^2_2 \\]" + it(
            t("Brent daily log returns (roll days removed): skewness @{tails.skew|.2f}, excess kurtosis @{tails.exkurt|.2f}, "
              "JB @{tails.jb|,.0f} (5\\% critical value 5.99); Student-$t$ fit: @{tails.t_df|.2f} degrees of freedom.",
              "Randamentele logaritmice zilnice ale țițeiului Brent (fără zilele de schimbare a contractului): asimetria @{tails.skew|.2f}, "
              "excesul de aplatizare @{tails.exkurt|.2f}, JB @{tails.jb|,.0f} (valoarea critică: 5{,}99); distribuția Student-$t$ ajustată "
              "are @{tails.t_df|.2f} grade de libertate.")),
        LOGTAB + note(t("Logit for a day with at least one negative RO quarter-hour; base year @{logit.base_year}.",
                        "Modelul logit pentru o zi cu cel puțin un sfert de oră cu preț negativ în RO; anul de bază: @{logit.base_year}.")),
        "0.43", "0.54"), "small", cite=t("(Jarque \\& Bera, 1980; own estimation)", "(Jarque \\& Bera, 1980; estimare proprie)"))
    D.frame(t("Appendix G: converting gas and oil prices to EUR/MWh", "Anexa G: conversia prețurilor gazelor și țițeiului în EUR/MWh"), cols(
        "\\[ P^{\\text{EUR/MWh}}=P^{\\text{USD/MMBtu}}\\times " + t("3.412142", "3{,}412142") + "\\,/\\,e_m \\]" +
        "\\where{" + t("$1\\ \\text{MMBtu}=0.293071$ MWh, so $1/0.293071=3.412142$ MMBtu per MWh; $e_m$ = monthly USD per EUR rate "
                       "of the ECB; Brent: 1 bbl = 159 litres, quoted in USD/bbl",
                       "$1\\ \\text{MMBtu}=0{,}293071$ MWh, deci $1/0{,}293071=3{,}412142$ MMBtu pe MWh; $e_m$ = cursul mediu lunar "
                       "USD pe EUR publicat de ECB; Brent: 1 bbl = 159 de litri, cotat în USD/bbl") + "}",
        it(t("World Bank TTF is a monthly average in USD/MMBtu converted with the ECB rate; it is not a traded EUR quote.",
             "Prețul TTF publicat de Banca Mondială este o medie lunară în USD/MMBtu, convertită cu cursul ECB; nu este o cotație "
             "tranzacționată în EUR."),
           t("Compare fuels and power only in the same unit and currency; a gas price in USD/MMBtu and a power price in EUR/MWh "
             "differ by a factor of about 3.4 before any exchange rate.",
             "Comparați combustibilii și energia electrică numai în aceeași unitate și monedă; un preț al gazelor în USD/MMBtu și unul "
             "al energiei în EUR/MWh diferă printr-un factor de circa 3{,}4, înainte de aplicarea cursului de schimb."), sep="3pt"),
        "0.50", "0.47"), "small", cite=t("(World Bank Commodity Price Data; ECB reference rates)", "(Banca Mondială; cursurile de referință ECB)"))
    return D


def main(langs):
    ok = True
    for lang in langs:
        name = "lecture1" if lang == "en" else "lecture1_ro"
        out = os.path.join(HERE, name + ".tex")
        D, tex, res, H = autofit(build, out, lang)
        print(f"[{lang}] frames: main {D.n_main} (incl. title and section outlines), total {D.n_frames}; quiz frames {D.quiz}; "
              f"pages {res['pages']}; errors {res['errors']}; overfull>1pt {len(res['overfull'])}")
        for kind, amt, title in res["where"]:
            print(f"     {kind} {amt:6.1f}pt  {title}")
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
