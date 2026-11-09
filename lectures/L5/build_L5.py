r"""
build_L5.py -- Lecture 5 "Energy Derivatives and Hedging" (EMQA), English and Romanian from one source
=====================================================================================================
Writes lectures/L5/lecture5.tex (EN) and lectures/L5/lecture5_ro.tex (RO) from the bilingual slide text in this file
and the numbers in L5_numbers.json (produced by analysis_L5.py), compiles both with pdflatex and checks: 0 LaTeX errors;
no overfull box > 1 pt (nothing masked); every acronym in the Abbreviations frames and spelled out at first use;
contact sheets for the visual check.

Run (from the repository root):
    python3 data/download_L5.py               # once: OPCOM forward results, ECB EUR/RON and EUR STR, TTF contracts, coal
    python3 lectures/L5/analysis_L5.py
    python3 lectures/L5/build_L5.py            # both languages;  add "en" or "ro" for one

Hand-typed numbers are definitions only: efficiencies 50% / 38%, emission factors 0.202 / 0.341 t CO2 per MWh thermal
(IPCC 2006), 6.978 MWh per tonne of coal, 8760 h, 744 h, 10 MW, strikes 0.9 F / 1.1 F, 450 lei/MWh (OUG 153/2022) and
institutional dates (market coupling 17 June 2021 and 8 June 2022).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_build import (Deck, Numbers, acronym_audit, autofit, block, cols, contact_sheet,  # noqa: E402
                        first_use_audit, fmt, hier, items, table)


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
    "ACER": ("European Union Agency for the Cooperation of Energy Regulators",
             "Agenția Uniunii Europene pentru Cooperarea Autorităților de Reglementare din Domeniul Energiei"),
    "BCE": (None, "Banca Centrală Europeană"),
    "ECB": ("European Central Bank", None),
    "CET": ("Central European Time", "ora Europei Centrale"),
    "DE-LU": ("Germany--Luxembourg bidding zone", "zona de ofertare Germania--Luxemburg"),
    "EEX": ("European Energy Exchange", "bursa europeană de energie European Energy Exchange"),
    "ENTSO-E": ("European Network of Transmission System Operators for Electricity",
                "Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică"),
    "EPEX": ("European Power Exchange (EPEX SPOT)", "bursa europeană de energie EPEX SPOT"),
    "CSS": ("clean spark spread", "clean spark spread (marja curată a centralei pe gaze)"),
    "CDS": ("clean dark spread", "clean dark spread (marja curată a centralei pe cărbune)"),
    "SS": ("spark spread", "spark spread (marja brută a centralei pe gaze)"),
    "HE": ("hedge effectiveness", "eficiența acoperirii (hedge effectiveness)"),
    "VM": ("variation margin", "marja de variație"),
    "GARCH": ("generalised autoregressive conditional heteroskedasticity", "heteroscedasticitate condiționată autoregresivă generalizată"),
    "LASSO": ("least absolute shrinkage and selection operator", "operatorul de contracție și selecție în normă absolută"),
    "RON": ("Romanian leu", "leul românesc"), "TJ": ("terajoule", "terajoule"),
    "ETC": ("exchange-traded commodity", "titlu tranzacționat la bursă, garantat cu mărfuri (exchange-traded commodity)"),
    "EU": ("European Union", None),
    "UE": (None, "Uniunea Europeană"),
    "EUA": ("EU emission allowance (1 t CO$_2$)", "certificat de emisii al UE (1 t CO$_2$)"),
    "€STR": ("euro short-term rate", "rata pe termen scurt a euro (euro short-term rate)"),
    "HAC": ("heteroskedasticity- and autocorrelation-consistent", "robust la heteroscedasticitate și autocorelare"),
    "HU": ("Hungary (bidding zone)", "Ungaria (zonă de ofertare)"),
    "HUDEX": ("Hungarian Derivative Energy Exchange", "bursa maghiară de derivate pe energie (Hungarian Derivative Energy Exchange)"),
    "HUPX": ("Hungarian Power Exchange", "bursa de energie din Ungaria"),
    "IPCC": ("Intergovernmental Panel on Climate Change", "Grupul interguvernamental privind schimbările climatice"),
    "ISE": ("Fraunhofer Institute for Solar Energy Systems", "Institutul Fraunhofer pentru Sisteme de Energie Solară"),
    "LD": ("Monday to Sunday (luni--duminică), OPCOM product code", "luni--duminică, codul produsului OPCOM"),
    "MACEE": ("Centralised Electricity Purchase Mechanism (Romania, 2023--2024)",
              "Mecanismul de achiziție centralizată de energie electrică (2023--2024)"),
    "NYMEX": ("New York Mercantile Exchange", "bursa New York Mercantile Exchange"),
    "OLS": ("ordinary least squares", "metoda celor mai mici pătrate"),
    "OPCOM": ("Romanian electricity and gas market operator", "operatorul pieței de energie electrică și de gaze naturale din România"),
    "OUG": ("Government Emergency Ordinance (Romania)", "ordonanță de urgență a Guvernului"),
    "PC-OTC": ("OPCOM continuous market for standardised bilateral contracts",
               "piața centralizată cu negociere dublă continuă a contractelor bilaterale (OPCOM)"),
    "PCCB-LE": ("OPCOM centralised market for bilateral contracts, extended auctions",
                "piața centralizată a contractelor bilaterale, licitație extinsă (OPCOM)"),
    "PPA": ("power purchase agreement", "contract de achiziție de energie pe termen lung (power purchase agreement)"),
    "PZU": ("Piața pentru Ziua Următoare (day-ahead market)", "piața pentru ziua următoare"),
    "RO": ("Romania (bidding zone)", "România (zonă de ofertare)"),
    "TTF": ("Title Transfer Facility (Dutch gas hub)", "Title Transfer Facility (hubul olandez de gaze naturale)"),
    "VaR": ("value at risk", "valoarea expusă la risc (value at risk)"),
    "VWAP": ("volume-weighted average price", "prețul mediu ponderat cu volumul"),
    "EUR": ("euro", "euro"), "MW": ("megawatt", "megawatt"), "MWh": ("megawatt-hour", "megawatt-oră"),
    "TWh": ("terawatt-hour", "terawatt-oră"), "USD": ("United States dollar", "dolarul american"),
}
UNITS = {"EUR", "MW", "MWh", "TWh", "USD", "€STR", "RON", "TJ"}
# tokens inside citations, product names and units only
IGNORE = {"EMQA", "JFE", "JF", "RES", "DSS", "JFQA", "IJF", "ENEECO", "PICBE", "JSES", "SSRN", "CO", "STR", "II", "SPOT", "SA",
          "NB", "RFS", "SDAC"}


def build(lang, H=None):
    V = Numbers(os.path.join(HERE, "L5_numbers.json"), lang)
    N = V.N
    D = Deck(5, "Energy Derivatives and Hedging" if lang == "en" else "Derivate pe energie și acoperirea riscului de preț", V, lang, heights=H)
    t = D.t
    ro = lang == "ro"
    if ro:   # notebook pointer in natural Romanian: "notebook-ul Jupyter, secțiunea 2"
        _tex = D.tex
        D.tex = lambda: _tex().replace("notebook-ul Jupyter \\S", "notebook-ul Jupyter, secțiunea ")
    NB = t("notebook", "notebook-ul Jupyter")
    Y = N["cutoff"]["end"][:4]
    Y1 = str(int(Y) + 1)
    Y0 = str(int(Y) - 1)
    YY1 = Y1[2:]

    def de(key):
        v = int(round(float(V.get(key))))
        return "de " if ro and v >= 20 and (v % 100 >= 20 or v % 100 == 0) else ""

    def f(key, spec=".1f"):
        return fmt(V.get(key), spec, lang)

    OWN = t("(own computation)", "(calcule proprii)")

    # ------------------------------------------------------------------ front matter
    D.parts.append("% END-FRONT-MATTER\n")
    D.frame(t("Learning objectives", "Obiectivele cursului"), it(
        t(("\\textbf{Contracts}", "forwards and futures on power and gas, physical or cash-settled; the forward curve"),
          ("\\textbf{Contractele}", "contracte forward și futures pe energie electrică și gaze, cu livrare fizică sau cu decontare financiară; curba prețurilor forward")),
        t(("\\textbf{Plant margins}", "spark and dark spreads, clean of the price of the European Union (EU) emission allowance (EUA)"),
          ("\\textbf{Marjele centralelor}", "spark spread și dark spread, inclusiv costul certificatului de emisii (EUA) al Uniunii Europene (UE)")),
        t(("\\textbf{Hedging}", "the minimum-variance hedge ratio and its uncertainty; basis risk; shape risk"),
          ("\\textbf{Acoperirea riscului}", "raportul de acoperire cu varianță minimă și incertitudinea lui; riscul de bază; riscul de profil")),
        t(("\\textbf{Options}", "caps, floors and collars; the Black-76 formula with a volatility estimated on real data"),
          ("\\textbf{Opțiuni}", "plafon (cap), prag minim (floor) și combinația lor (collar); formula Black-76, cu o volatilitate estimată pe date reale")),
        t(("\\textbf{Decisions}", "what a Romanian supplier and a producer gained or lost by hedging in 2022, 2025 and " + Y),
          ("\\textbf{Decizii}", "cît au cîștigat sau au pierdut prin acoperire un furnizor și un producător din România în 2022, 2025 și " + Y)),
        sep="3pt"))

    ab = sorted([(k, v) for k, v in ABBR.items() if v[0 if not ro else 1] is not None], key=lambda kv: kv[0].lower().replace("€", ""))

    def abcol(lst):
        return ("{\\scriptsize\\renewcommand{\\arraystretch}{0.96}\\begin{tabular}{@{}>{\\bfseries}l@{\\ \\ }"
                "p{0.74\\linewidth}@{}}" + "\n".join(f"{k} & {v[0] if not ro else v[1]}\\\\" for k, v in lst) + "\\end{tabular}}")

    D.parts.append("% BEGIN-ABBR\n")
    half = (len(ab) + 1) // 2
    for part, lst in enumerate([ab[:half], ab[half:]]):
        hh = (len(lst) + 1) // 2
        D.frame(t("Abbreviations", "Abrevieri") + f" ({part + 1}/2)", "\\vspace{-1mm}\\begin{columns}[T,onlytextwidth]\n" + "".join(
            f"\\begin{{column}}{{0.49\\textwidth}}{abcol(lst[i * hh:(i + 1) * hh])}\\end{{column}}\n" for i in range(2)) +
            "\\end{columns}")
    D.parts.append("% END-ABBR\n")

    D.frame(t("Real data only: Romanian forwards, spot prices, gas, carbon", "Folosim numai date reale: forward, spot, gaze, carbon"), table(
        "@{}p{0.37\\textwidth}p{0.11\\textwidth}p{0.47\\textwidth}@{}",
        [t("Series", "Seria"), t("Frequency", "Frecvența"), t("Source", "Sursa")],
        [[t("Romanian forward contracts: @{data.fw_n|,d} auctions, @{data.fw_twh|.1f} TWh",
            "Contracte forward în România: @{data.fw_n|,d} " + de("data.fw_n") + "licitații, @{data.fw_twh|.1f} TWh"),
          t("per auction", "pe licitație"),
          t("Romanian electricity and gas market operator (OPCOM): centralised market for bilateral contracts, extended auctions (PCCB-LE)",
            "operatorul pieței de energie electrică și de gaze naturale din România (OPCOM): piața centralizată a contractelor bilaterale, licitație extinsă (PCCB-LE)")],
         [t("Day-ahead prices, Piața pentru Ziua Următoare (PZU): Romania (RO), Hungary (HU), Germany--Luxembourg (DE-LU)",
            "Prețuri pe piața pentru ziua următoare (PZU): România (RO), Ungaria (HU), Germania--Luxemburg (DE-LU)"),
          t("hourly", "orară"),
          t("OPCOM, Hungarian Power Exchange (HUPX), European Power Exchange (EPEX SPOT); energy-charts.info (Fraunhofer ISE), from the European Network of "
            "Transmission System Operators for Electricity (ENTSO-E)",
            "OPCOM, bursa de energie din Ungaria (HUPX), bursa europeană de energie (EPEX SPOT); energy-charts.info (Fraunhofer ISE), din datele Rețelei europene a "
            "operatorilor de transport și de sistem (ENTSO-E)")],
         [t("Gas: Title Transfer Facility (TTF); coal", "Gaze: Title Transfer Facility (TTF); cărbune"),
          t("monthly, daily", "lunară, zilnică"),
          t("World Bank Pink Sheet; New York Mercantile Exchange (NYMEX) futures, via Yahoo Finance",
            "Banca Mondială (Pink Sheet); contracte futures New York Mercantile Exchange (NYMEX), prin Yahoo Finance")],
         [t("Carbon (EUA); EUR/RON; euro short-term rate (€STR)", "Carbon (EUA); cursul EUR/RON; rata pe termen scurt a euro (€STR)"),
          t("daily", "zilnică"),
          t("European Energy Exchange (EEX) auctions; exchange-traded commodity (ETC); European Central Bank (ECB)",
            "licitațiile European Energy Exchange (EEX); un titlu garantat cu certificate (ETC); Banca Centrală Europeană (BCE)")]],
        size="scriptsize", stretch="0.95") + "\n\\vspace{0.5mm}\n" + it(
        t("\\textbf{Cut-off} @{cutoff.end|date} (last complete month); forward auctions @{data.fw_first|date} -- @{data.fw_last|date}.",
          "\\textbf{Data-limită}: @{cutoff.end|date} (ultima lună completă); licitații forward: @{data.fw_first|date} -- @{data.fw_last|date}"),
        t("\\textbf{Not free}: EEX or Hungarian Derivative Energy Exchange (HUDEX) power futures, option prices; we do not invent them.",
          "\\textbf{Nu sînt disponibile gratuit}: contractele futures pe energie de la EEX sau de la bursa maghiară de derivate (HUDEX) și prețurile opțiunilor; nu le inventăm"),
        sep="1pt") + D.bottom(None, NB + " \\S1"), "footnotesize")

    # ------------------------------------------------------------------ 1 why hedge
    D.section(t("Reasons for hedging: price exposures and the 2021--2022 crisis", "Motivele acoperirii riscului: expunerile la preț și criza din 2021--2022"))
    D.concept(t("Every firm in the power chain holds a price position", "Fiecare firmă din sectorul energiei are o poziție de preț"),
              t("A supplier with fixed retail prices loses when the wholesale price rises; a producer loses when it falls.",
                "Un furnizor cu prețuri fixe pierde cînd prețul angro crește; un producător pierde cînd prețul scade."),
              "\\[ \\Pi^{\\text{" + t("sup", "furn") + "}}=Q(\\underbrace{R}_{\\text{" + t("retail", "client") + "}}-\\underbrace{S}_{\\text{spot}}),\\quad "
              "\\Pi^{\\text{prod}}=Q(S-\\underbrace{c}_{\\text{cost}}) \\]"
              "\\[ \\Pi^{\\text{" + t("sup", "furn") + "}}_{\\text{" + t("hedged", "acoperit") + "}}=Q(R-S)+Q(S-F)=Q(R-F) \\]" +
              "\\where{" + t("$Q$ = energy, MWh; $S$ = spot price at delivery; $F$ = forward price fixed today, EUR/MWh; a bought forward pays $S-F$ per MWh.",
                             "$Q$ = energia, în MWh; $S$ = prețul spot la livrare; $F$ = prețul forward stabilit azi, în EUR/MWh; un forward cumpărat aduce $S-F$ pe MWh.") + "}",
              it((t("\\textbf{Short power}", "\\textbf{Poziție scurtă}"),
                  t("supplier at fixed prices, industrial consumer", "furnizorul cu prețuri fixe, consumatorul industrial"),
                  t("hedge: buy forward or a cap", "acoperire: cumpără forward sau un plafon")),
                 (t("\\textbf{Long power}", "\\textbf{Poziție lungă}"),
                  t("hydro, nuclear, lignite and solar producers", "producătorii hidro, nucleari, pe lignit și solari"),
                  t("hedge: sell forward or buy a floor", "acoperire: vinde forward sau cumpără un prag minim")),
                 (t("\\textbf{Long the spread}", "\\textbf{Poziție lungă pe marjă}"),
                  t("gas plant: power minus gas and carbon", "centrala pe gaze: energie minus gaze și carbon")), sep="2pt"),
              t("fix the sign of your exposure first: a long firm that buys forward doubles its risk.",
                "stabiliți întîi semnul expunerii: o firmă cu poziție lungă care mai cumpără forward își dublează riscul."),
              cite="(Hull, 2022; Eydeland \\& Wolyniec, 2003)", wl="0.52", wr="0.45")

    D.chart(t("In 2022 the spot cost @{crisis.ratio|.1f} times the forward bought earlier", "În 2022, prețul spot a fost de @{crisis.ratio|.1f} ori mai mare decît prețul forward"), "crisis_cal22", [
        t(("2022 baseload: @{crisis.n} auctions, volume-weighted average price (VWAP) @{crisis.F22|.1f} EUR/MWh; spot @{crisis.S22|.1f}",
           "2020: @{crisis.parts.h20.vwap|.1f}; first half of 2021: @{crisis.parts.h21a.vwap|.1f}; second half: @{crisis.parts.h21b.vwap|.1f}; saving @{crisis.eur_per_mw_m|.2f} million EUR per MW"),
          ("Banda pentru 2022: @{crisis.n} " + de("crisis.n") + "licitații, preț mediu ponderat cu volumul (VWAP) @{crisis.F22|.1f} EUR/MWh; spot @{crisis.S22|.1f}",
           "VWAP: 2020 -- @{crisis.parts.h20.vwap|.1f}; sem.\\ I 2021 -- @{crisis.parts.h21a.vwap|.1f}; sem.\\ II 2021 -- @{crisis.parts.h21b.vwap|.1f}; economie: @{crisis.eur_per_mw_m|.2f} mil.\\ EUR/MW"))],
        height="0.55\\textheight", job=t("when you hedge matters: contracts bought late in 2021 cost twice as much.",
                                         "contează și momentul: contractele cumpărate la sfîrșitul lui 2021 au costat dublu."),
        tryit=NB + " \\S2", cite=t("(own computation; OPCOM)", "(calcule proprii; OPCOM)"))

    D.frame(t("The crisis froze forward trading and brought regulated prices", "Criza a blocat piața forward și a adus prețuri reglementate"), it(
        t(("\\textbf{A transfer, not a gain}", "each MWh sold forward for 2022 went @{crisis.gap|.1f} EUR/MWh below spot: producers lost what hedged suppliers saved"),
          ("\\textbf{Un transfer, nu un cîștig}", "fiecare MWh vîndut forward pentru 2022 a fost cu @{crisis.gap|.1f} EUR/MWh sub spot: producătorii au pierdut exact cît au economisit furnizorii acoperiți")),
        t(("\\textbf{Then forwards overshot}", "calendar 2023 traded up to @{crisis.c23_max|.1f} on @{crisis.c23_argmax|date}; 2023 averaged @{cal.2023.realised|.1f} EUR/MWh"),
          ("\\textbf{Apoi prețurile forward au crescut excesiv}", "banda pentru 2023 s-a tranzacționat la @{crisis.c23_max|.1f} EUR/MWh la @{crisis.c23_argmax|date}; media realizată în 2023: @{cal.2023.realised|.1f}")),
        t(("\\textbf{Romania}", "Government Emergency Ordinance (OUG) 27/2022: capped final prices",
           "OUG 153/2022: Centralised Electricity Purchase Mechanism (MACEE), OPCOM single buyer at 450 lei/MWh for 2023--2024",
           "OPCOM forward volume: @{volume.2021|.1f} TWh in 2021, @{volume.2023|.1f} TWh in 2023"),
          ("\\textbf{În România}", "ordonanța de urgență a Guvernului (OUG) 27/2022: prețuri finale plafonate",
           "OUG 153/2022: Mecanismul de achiziție centralizată de energie electrică (MACEE), cu OPCOM cumpărător unic la 450 lei/MWh, în 2023--2024",
           "volumul forward pe OPCOM: @{volume.2021|.1f} TWh în 2021, doar @{volume.2023|.1f} TWh în 2023")),
        t(("\\textbf{In the EU}", "the EU Agency for the Cooperation of Energy Regulators (ACER) kept the market design and flagged thin forward markets beyond three years"),
          ("\\textbf{În UE}", "Agenția UE pentru Cooperarea Autorităților de Reglementare din Domeniul Energiei (ACER) a păstrat modelul pieței și a semnalat lichiditatea redusă a contractelor forward pe peste trei ani")),
        sep="2pt") + D.bottom(t("write the hedging policy before the crisis; during it, nobody can agree on one.",
                                "scrieți politica de acoperire înainte de criză; în timpul crizei, nimeni nu mai cade de acord asupra ei."), NB + " \\S2"),
        "footnotesize", cite="(OUG 27/2022; OUG 153/2022; ACER, 2022; OPCOM)")

    # ------------------------------------------------------------------ 2 forwards, futures, curve
    D.section(t("Forwards, futures and the forward curve", "Contracte forward, futures și curba forward"))
    D.subsection(t("Contracts", "Contractele"))
    D.concept(t("A power forward delivers constant MW over a whole period", "Un forward pe energie livrează aceeași putere pe toată perioada"),
              t("A baseload forward fixes today the price of every hour of a month, quarter or year.",
                "Un forward în bandă fixează azi prețul tuturor orelor dintr-o lună, un trimestru sau un an."),
              "\\[ \\bar S=\\frac{1}{H}\\sum_{h=1}^{H}S_h,\\qquad \\underbrace{V_T=q\\,H\\,(\\bar S-F)}_{\\text{" + t("value to the buyer", "valoarea pentru cumpărător") + "}} \\]" +
              "\\where{" + t("$H$ = hours of the delivery period (744 in a 31-day month, 8\\,760 in a year); $S_h$ = day-ahead price of hour $h$; $q$ = power, MW; $F$ = forward price.",
                             "$H$ = orele perioadei de livrare (744 într-o lună de 31 de zile, 8\\,760 într-un an); $S_h$ = prețul PZU al orei $h$; $q$ = puterea, în MW; $F$ = prețul forward.") + "}",
              it((t("\\textbf{Profiles}", "\\textbf{Profiluri}"),
                  t("band: all hours, Monday to Sunday (LD), @{data.base_share|.0f}\\% of volume", "bandă: toate orele, luni--duminică (LD), @{data.base_share|.0f}\\% din volum"),
                  t("peak: the peak hours of working days only", "vîrf: numai orele de vîrf ale zilelor lucrătoare")),
                 (t("\\textbf{OPCOM, @{cutoff.end|date}}", "\\textbf{OPCOM, @{cutoff.end|date}}"),
                  t("year " + Y1 + ": @{curve.cal_next.F|.1f} EUR/MWh $\\times$ 8\\,760 MWh per MW", "anul " + Y1 + ": @{curve.cal_next.F|.1f} EUR/MWh, pentru 8\\,760 MWh pe MW"),
                  t("next month: @{curve.m_front.F|.1f} EUR/MWh", "luna următoare: @{curve.m_front.F|.1f} EUR/MWh")), sep="2pt"),
              t("price a customer's contract on the forward of its delivery period, not on today's spot.",
                "faceți oferta către client pe baza prețului forward al perioadei de livrare, nu a prețului spot de azi."),
              tryit=NB + " \\S3", cite="(OPCOM; Benth et al., 2008)", wl="0.53", wr="0.44")

    D.concept(t("Physical delivery and cash settlement", "Livrarea fizică și decontarea financiară"),
              t("A physical forward delivers MWh at $F$; a cash-settled future pays the gap to a reference average.",
                "Forward-ul fizic livrează energia la prețul $F$; contractul futures financiar plătește doar diferența față de o medie."),
              "\\[ \\underbrace{F\\cdot Q}_{\\text{" + t("physical", "fizic") + "}}=\\underbrace{\\bar S Q}_{\\text{spot}}-\\underbrace{(\\bar S^{\\text{ref}}-F)Q}_{\\text{" + t("cash settlement", "decontare") + "}}"
              "\\ \\text{" + t("only if", "numai dacă") + " } \\bar S^{\\text{ref}}=\\bar S \\]" +
              "\\where{" + t("$\\bar S^{\\text{ref}}$ = settlement index of the future (e.g.\\ the German average); otherwise the gap is basis risk (section 4).",
                             "$\\bar S^{\\text{ref}}$ = indicele de decontare (de exemplu, media din Germania); altfel, diferența este riscul de bază (secțiunea 4).") + "}",
              it((t("\\textbf{Physical, Romania}", "\\textbf{Fizic, în România}"),
                  t("OPCOM PCCB-LE auctions and continuous trading of standard contracts (PC-OTC)", "licitațiile OPCOM PCCB-LE și piața centralizată cu negociere continuă (PC-OTC)"),
                  t("no basis risk", "fără risc de bază")),
                 (t("\\textbf{Cash-settled, abroad}", "\\textbf{Financiar, în străinătate}"),
                  t("EEX and HUDEX futures, cleared", "contracte futures EEX și HUDEX, cu casă de compensație"),
                  t("margin calls replace counterparty risk", "în locul riscului de contrapartidă apare nevoia de lichiditate pentru marjă")), sep="2pt"),
              t("physical when you need MWh in Romania; cash-settled when you need liquidity and can carry the basis.",
                "contracte fizice, pentru energie livrată în România; contracte financiare, pentru o piață lichidă, cu riscul de bază asumat."),
              cite="(OPCOM; Hull, 2022)", wl="0.55", wr="0.42")

    D.concept(t("Futures are marked to market daily: the hedge needs cash", "Contractele futures se decontează zilnic, deci cer lichiditate"),
              t("A forward settles once at delivery; a future pays or collects every day's price change.",
                "Forward-ul se decontează o dată, la livrare; deținătorul unui contract futures plătește sau încasează zilnic variația prețului."),
              "\\[ \\underbrace{VM_t=Q(F_t-F_{t-1})}_{\\text{" + t("variation margin", "marja de variație") + "}},\\qquad \\sum_{t=1}^{T}VM_t=Q(F_T-F_0) \\]" +
              "\\where{" + t("$F_t$ = settlement price of day $t$; $Q$ = MWh; initial margin from a value-at-risk (VaR) model (Lecture 4).",
                             "$F_t$ = prețul de decontare din ziua $t$; $Q$ = poziția, în MWh; marja inițială se calculează cu un model de valoare expusă la risc (VaR), vezi cursul 4.") + "}",
              it((t("\\textbf{NYMEX TTF, December " + Y + "}", "\\textbf{NYMEX TTF, decembrie " + Y + "}"),
                  t("@{margin.n|,d} daily prices, @{margin.min|.1f} -- @{margin.max|.1f} EUR/MWh", "@{margin.n|,d} " + de("margin.n") + "prețuri zilnice, între @{margin.min|.1f} și @{margin.max|.1f} EUR/MWh"),
                  t("largest daily move @{margin.max_abs|.2f} EUR/MWh, @{margin.max_date|date}", "cea mai mare variație zilnică: @{margin.max_abs|.2f} EUR/MWh, la @{margin.max_date|date}"),
                  t("10 MW $\\times$ 744 h: margin call @{margin.call_eur|,.0f} EUR in a day", "10 MW $\\times$ 744 h: apel în marjă de @{margin.call_eur|,.0f} EUR într-o zi")), sep="2pt"),
              t("size a credit line for the worst daily move before hedging on an exchange.",
                "dimensionați linia de credit pentru cea mai mare variație zilnică înainte de a vă acoperi la bursă."),
              tryit=NB + " \\S3", cite=t("(own computation; Hull, 2022)", "(calcule proprii; Hull, 2022)"), wl="0.54", wr="0.43")

    D.chart(t("Romanian forward volume collapsed in 2022--2023", "Volumul forward din România s-a prăbușit în 2022--2023"), "fw_volume", [
        t(("Three producers sell @{who.sell_top3_share|.0f}\\% of the volume: lignite @{who.sell_oltenia|.0f}\\%, nuclear @{who.sell_snn|.0f}\\%, hydro @{who.sell_hidro|.0f}\\%",
           "calendar-year products: @{volume.y_share_base|.0f}\\% of baseload volume"),
          ("Trei producători vînd @{who.sell_top3_share|.0f}\\% din volum: Complexul Energetic Oltenia @{who.sell_oltenia|.0f}\\%, Nuclearelectrica @{who.sell_snn|.0f}\\%, Hidroelectrica @{who.sell_hidro|.0f}\\%",
           "produsele pe an calendaristic: @{volume.y_share_base|.0f}\\% din volumul în bandă"))],
        height="0.55\\textheight", job=t("liquidity is thin: spread purchases over many auctions.",
                                         "lichiditatea este redusă: eșalonați cumpărările pe mai multe licitații."),
        tryit=NB + " \\S1", cite=t("(own computation; OPCOM)", "(calcule proprii; OPCOM)"))

    D.subsection(t("The forward curve", "Curba prețurilor forward"))
    D.concept(t("Storable gas follows the cost of carry; power does not", "Forward-ul gazelor reflectă costul de stocare; al energiei, nu"),
              t("Gas can be stored, which ties forward to spot; power cannot, so its forward is an expectation plus a risk premium.",
                "Gazele se pot stoca, deci prețul lor forward este legat de spot prin costul de deținere; energia electrică nu, deci prețul ei forward este prețul spot așteptat plus o primă de risc."),
              "\\[ \\underbrace{F_{t,T}=S_te^{(r+u-y)(T-t)}}_{\\text{" + t("storable", "stocabil") + "}},\\qquad "
              "\\underbrace{F_{t,T}=\\E_t[\\bar S_T]+\\pi_{t,T}}_{\\text{" + t("power", "energie") + "}} \\]" +
              "\\where{" + t("$r$ = interest rate; $u$ = storage cost; $y$ = convenience yield; $\\pi$ = risk premium; contango $F>S$, backwardation $F<S$.",
                             "$r$ = dobînda; $u$ = costul de stocare; $y$ = randamentul de comoditate (convenience yield); $\\pi$ = prima de risc; report (contango): $F>S$; deport (backwardation): $F<S$.") + "}",
              it((t("\\textbf{Gas}, NYMEX TTF, @{ttfcurve.date|date}", "\\textbf{Gaze}, NYMEX TTF, @{ttfcurve.date|date}"),
                  t("Dec " + Y + " @{ttfcurve.2026-12|.1f}, May " + Y1 + " @{ttfcurve.2027-05|.1f} EUR/MWh", "decembrie " + Y + ": @{ttfcurve.2026-12|.1f}; mai " + Y1 + ": @{ttfcurve.2027-05|.1f} EUR/MWh"),
                  t("winter above summer pays for storage", "diferența dintre prețul de iarnă și cel de vară acoperă costul stocării")),
                 (t("\\textbf{Power}, OPCOM", "\\textbf{Energie electrică}, OPCOM"),
                  t("October spot @{curve.spot_lastm|.1f}; Q1 " + Y1 + " @{curve.q_front.F|.1f}; year @{curve.cal_next.F|.1f}", "spot în octombrie: @{curve.spot_lastm|.1f}; trimestrul I " + Y1 + ": @{curve.q_front.F|.1f}; anul " + Y1 + ": @{curve.cal_next.F|.1f}"),
                  t("backwardation: the spike is expected to fade", "deport (backwardation): piața se așteaptă ca prețurile ridicate de acum să scadă")), sep="2pt"),
              t("never put today's spot into next year's budget; use the curve.",
                "nu puneți spotul de azi în bugetul anului viitor; folosiți curba forward."),
              tryit=NB + " \\S3", cite="(Fama \\& French, 1987; Bessembinder \\& Lemmon, 2002)", wl="0.52", wr="0.45")

    D.chart(t("The Romanian forward curve slopes down from a high spot", "Curba forward din România coboară de la un spot ridicat"), "fwd_curve", [
        t("@{curve.n_products} baseload products, VWAP per delivery period: next month @{curve.m_front.F|.1f}, Q1 @{curve.q_front.F|.1f}, year " + Y1 + " @{curve.cal_next.F|.1f} EUR/MWh.",
          "@{curve.n_products} produse în bandă, VWAP pe perioada de livrare: luna următoare @{curve.m_front.F|.1f}, trimestrul I @{curve.q_front.F|.1f}, anul " + Y1 + " @{curve.cal_next.F|.1f} EUR/MWh.")],
        height="0.58\\textheight", job=t("a " + Y1 + " offer starts from @{curve.cal_next.F|.0f} EUR/MWh, not from the October spot.",
                                         "o ofertă pentru " + Y1 + " pornește de la @{curve.cal_next.F|.0f} EUR/MWh, nu de la spotul din octombrie."),
        tryit=NB + " \\S3", cite=t("(own computation; OPCOM)", "(calcule proprii; OPCOM)"))

    D.chart(t("The curve moves: yearly forwards by trade date vs realised", "Curba se mișcă: prețurile anuale, după data tranzacției"), "cal_by_trade", [
        t("2021: VWAP @{cal.2021.vwap|.1f}, realised @{cal.2021.realised|.1f}; 2023: @{cal.2023.vwap|.1f} vs @{cal.2023.realised|.1f}; 2025: @{cal.2025.vwap|.1f} vs @{cal.2025.realised|.1f} EUR/MWh.",
          "2021: VWAP @{cal.2021.vwap|.1f}, realizat @{cal.2021.realised|.1f}; 2023: @{cal.2023.vwap|.1f} față de @{cal.2023.realised|.1f}; 2025: @{cal.2025.vwap|.1f} față de @{cal.2025.realised|.1f} EUR/MWh.")],
        height="0.58\\textheight", job=t("the forward is the price of certainty, not a forecast to rely on in a crisis.",
                                         "prețul forward este prețul certitudinii, nu o prognoză pentru vremuri de criză."),
        tryit=NB + " \\S3", cite=t("(own computation; OPCOM)", "(calcule proprii; OPCOM)"))

    D.concept(t("The ex-post forward premium has no stable sign in Romania", "Prima forward ex post nu are un semn stabil în România"),
              t("If buyers fear spikes more than sellers fear slumps, forwards trade above the expected spot.",
                "Dacă cumpărătorii se tem de salturi mai mult decît vînzătorii de scăderi, forward-ul depășește spotul așteptat."),
              "\\[ \\hat\\pi_i=F_i-\\bar S_i,\\qquad t=\\frac{\\bar\\pi}{\\widehat{\\text{se}}_{\\text{HAC}}(\\bar\\pi)} \\]" +
              "\\where{" + t("$i$ = delivery month; $F_i$ = VWAP of the monthly band bought the month before; $\\bar S_i$ = realised mean; "
                             "standard error heteroskedasticity- and autocorrelation-consistent (HAC), Newey--West, 3 lags.",
                             "$i$ = luna de livrare; $F_i$ = VWAP al benzii lunare cumpărate în luna anterioară; $\\bar S_i$ = media realizată; "
                             "eroare standard robustă la heteroscedasticitate și autocorelare (HAC), Newey--West, 3 decalaje.") + "}",
              it((t("\\textbf{One month ahead}, @{prem.m1.n} months", "\\textbf{Cu o lună înainte}, @{prem.m1.n} " + de("prem.m1.n") + "luni"),
                  t("mean @{prem.m1.mean|+.1f} EUR/MWh, $t$ = @{prem.m1.t|.2f}, $p$ = @{prem.m1.p|.2f}", "media @{prem.m1.mean|+.1f} EUR/MWh, $t$ = @{prem.m1.t|.2f}, $p$ = @{prem.m1.p|.2f}"),
                  t("since 2023: @{prem.m1_post.mean|+.1f}, $t$ = @{prem.m1_post.t|.2f}", "din 2023: @{prem.m1_post.mean|+.1f}, $t$ = @{prem.m1_post.t|.2f}")),
                 (t("\\textbf{All products}, volume-weighted", "\\textbf{Toate produsele}, ponderate cu volumul"),
                  t("delivered to 2021: @{prem.pre.w_mean|+.1f}", "livrate pînă în 2021: @{prem.pre.w_mean|+.1f}"),
                  t("2022: @{prem.crisis.w_mean|+.1f}; from 2023: @{prem.post.w_mean|+.1f} EUR/MWh", "2022: @{prem.crisis.w_mean|+.1f}; din 2023: @{prem.post.w_mean|+.1f} EUR/MWh")), sep="2pt"),
              t("hedging is cheap on average; its real cost is the upside you give up.",
                "acoperirea este, în medie, ieftină; costul ei real este cîștigul la care renunțați."),
              tryit=NB + " \\S3", cite="(Bessembinder \\& Lemmon, 2002; Redl et al., 2009)", wl="0.50", wr="0.47")

    D.chart(t("Month by month, forward minus spot swings both ways", "Lună de lună, diferența forward minus spot are ambele semne"), "premium", [
        t("Median @{prem.m1.median|+.1f} EUR/MWh; the deep negative bars are 2021--2022 surprises, not a stable discount.",
          "Mediana: @{prem.m1.median|+.1f} EUR/MWh; valorile negative mari reflectă creșterile neașteptate de preț din 2021--2022, nu o primă negativă sistematică.")],
        height="0.60\\textheight", job=t("judge a hedge by the risk it removed, not by its ex-post profit.",
                                         "judecați o acoperire după riscul eliminat, nu după profitul de după livrare."),
        tryit=NB + " \\S3", cite=t("(own computation; OPCOM)", "(calcule proprii; OPCOM)"))

    # ------------------------------------------------------------------ 3 spreads
    D.section(t("Spreads: the margins of power plants", "Marjele centralelor electrice"))
    D.concept(t("Clean spark spread: power minus gas minus carbon", "Clean spark spread: energie minus gaze minus carbon"),
              t("A gas plant sells 1 MWh of power, burns $1/\\eta$ MWh of gas and pays for its CO$_2$.",
                "O centrală pe gaze vinde 1 MWh, arde $1/\\eta$ MWh de gaze și plătește certificatele pentru CO$_2$ emis."),
              "\\[ SS=P-\\frac{G}{\\eta_g},\\qquad CSS=P-\\frac{G}{\\eta_g}-\\frac{e_g}{\\eta_g}A \\]" +
              "\\where{" + t("spark spread (SS), clean spark spread (CSS); $P$ = power, EUR/MWh; $G$ = gas, EUR/MWh thermal; $\\eta_g$ = efficiency of the gas plant, 0.50 (assumed); "
                             "$e_g$ = emission factor of gas, 0.202 t CO$_2$/MWh thermal, Intergovernmental Panel on Climate Change (IPCC); $A$ = EUA, EUR/t.",
                             "spark spread (SS), clean spark spread (CSS); $P$ = prețul energiei electrice, EUR/MWh; $G$ = prețul gazelor, EUR/MWh termic; $\\eta_g$ = randamentul centralei pe gaze, 0{,}50 (ipoteză); "
                             "$e_g$ = factorul de emisie al gazelor, 0{,}202 t CO$_2$/MWh termic, Grupul interguvernamental privind schimbările climatice (IPCC); $A$ = prețul EUA, EUR/t.") + "}",
              it((t("\\textbf{Romania, @{spread.lastm.ym|ym}}", "\\textbf{România, @{spread.lastm.ym|ym}}"),
                  t("power @{spread.lastm.p|.1f}; gas cost per MWh of power @{spread.lastm.fuel|.1f} (= @{spread.lastm.gas|.1f}/0.5); carbon @{spread.lastm.co2|.1f}", "prețul energiei @{spread.lastm.p|.1f}; costul gazelor pe MWh electric @{spread.lastm.fuel|.1f} (= @{spread.lastm.gas|.1f}/0,5); costul carbonului @{spread.lastm.co2|.1f} EUR/MWh"),
                  t("SS @{spread.lastm.ss|+.1f}, CSS @{spread.lastm.css|+.1f} EUR/MWh", "SS @{spread.lastm.ss|+.1f}, CSS @{spread.lastm.css|+.1f} EUR/MWh")),
                 (t("\\textbf{Yearly mean CSS}", "\\textbf{CSS, media anuală}"),
                  t("Romania: 2022 @{spread.css_ro.2022|+.1f}, 2025 @{spread.css_ro.2025|+.1f}", "România: 2022 @{spread.css_ro.2022|+.1f}, 2025 @{spread.css_ro.2025|+.1f}"),
                  t("Germany: 2022 @{spread.css_de.2022|+.1f}, 2025 @{spread.css_de.2025|+.1f}", "Germania: 2022 @{spread.css_de.2022|+.1f}, 2025 @{spread.css_de.2025|+.1f}")), sep="2pt"),
              t("a gas producer hedges the spread: sell power, buy gas and EUA forward together.",
                "producătorul pe gaze acoperă marja: vinde energie și cumpără gaze și EUA forward, simultan."),
              tryit=NB + " \\S4", cite="(IPCC, 2006; Deng et al., 2001)", wl="0.55", wr="0.42")

    D.concept(t("Dark spreads and the carbon price that favours gas over coal", "Dark spread și prețul carbonului care favorizează gazele"),
              t("Coal emits more CO$_2$ per MWh, so a high EUA price pushes coal behind gas in the merit order.",
                "Cărbunele emite mai mult CO$_2$ pe MWh, deci un EUA scump împinge cărbunele după gaze în ordinea de merit."),
              "\\[ CDS=P-\\frac{C}{\\eta_c}-\\frac{e_c}{\\eta_c}A,\\qquad A^{*}=\\frac{G/\\eta_g-C/\\eta_c}{e_c/\\eta_c-e_g/\\eta_g} \\]" +
              "\\where{" + t("clean dark spread (CDS); $C$ = coal price, EUR/MWh thermal (USD/t $\\div$ EUR/USD $\\div$ 6.978); $\\eta_c$ = coal plant efficiency, 0.38 (assumed); $e_c$ = emission factor, 0.341 t CO$_2$/MWh thermal; "
                             "$A^{*}$ = EUA price at which CSS = CDS.",
                             "clean dark spread (CDS); $C$ = prețul cărbunelui, EUR/MWh termic (USD/t $\\div$ EUR/USD $\\div$ 6{,}978); $\\eta_c$ = randamentul centralei pe cărbune, 0{,}38 (ipoteză); $e_c$ = factorul de emisie, 0{,}341 t CO$_2$/MWh termic; "
                             "$A^{*}$ = prețul EUA la care CSS = CDS.") + "}",
              it((t("\\textbf{Month: @{spread.lastm.ym|ym}}", "\\textbf{Luna: @{spread.lastm.ym|ym}}"),
                  t("coal @{spread.lastm.coal|.1f} EUR/MWh thermal; CDS Romania @{spread.lastm.cds|+.1f}", "cărbune @{spread.lastm.coal|.1f} EUR/MWh termic; CDS în România @{spread.lastm.cds|+.1f}"),
                  t("$A^{*}$ = @{spread.switch_eua|.1f} EUR/t vs EUA @{spread.lastm.eua|.1f}", "$A^{*}$ = @{spread.switch_eua|.1f} EUR/t, față de EUA @{spread.lastm.eua|.1f}")),
                 (t("\\textbf{Caveats}", "\\textbf{Limite}"),
                  t("lignite has no market price; coal = South African export price", "lignitul nu are preț de piață; folosim cărbunele sud-african de export"),
                  t("EUA = EEX auctions, then the ETC from @{spread.eua_switch|ym}", "EUA = licitațiile EEX, apoi titlul ETC din @{spread.eua_switch|ym}")), sep="2pt"),
              t("a coal producer selling power forward should buy EUA forward with it.",
                "producătorul pe cărbune care vinde energie forward trebuie să cumpere și EUA forward."),
              tryit=NB + " \\S4", cite="(IPCC, 2006; World Bank)", wl="0.56", wr="0.41")

    D.chart(t("Monthly clean spark and clean dark spreads", "Clean spark spread și clean dark spread, lunar"), "spreads", [
        t("CSS negative in @{spread.css_ro_neg_m} of @{spread.n_m} months in Romania, @{spread.css_de_neg_m} in Germany; Romania higher by @{spread.gap_ro_de|.1f} EUR/MWh on average.",
          "CSS negativ în @{spread.css_ro_neg_m} din @{spread.n_m} " + de("spread.n_m") + "luni în România și în @{spread.css_de_neg_m} în Germania; în medie, cu @{spread.gap_ro_de|.1f} EUR/MWh mai mare în România.")],
        height="0.60\\textheight", job=t("a mean spread near zero does not make a plant worthless: it runs only in good hours.",
                                         "o marjă medie apropiată de zero nu face centrala inutilă: ea funcționează doar în orele bune."),
        tryit=NB + " \\S4", cite=t("(own computation; IPCC, 2006)", "(calcule proprii; IPCC, 2006)"))

    D.concept(t("A flexible gas plant is a strip of hourly call options", "O centrală pe gaze flexibilă este o serie de opțiuni call orare"),
              t("The plant runs only when the spread is positive, so it earns the positive part of each hourly spread.",
                "Centrala funcționează doar cînd marja este pozitivă, deci încasează partea pozitivă a fiecărei marje orare."),
              "\\[ \\underbrace{\\sum_h \\max(CSS_h,0)}_{\\text{" + t("flexible", "flexibilă") + "}}\\ \\ge\\ "
              "\\max\\Big(\\underbrace{\\sum_h CSS_h}_{\\text{" + t("must-run", "continuă") + "}},0\\Big) \\]" +
              "\\where{" + t("$CSS_h$ = clean spark spread of hour $h$, 1 MW, gas and EUA at monthly means; no start-up costs, so an upper bound.",
                             "$CSS_h$ = clean spark spread al orei $h$, pentru 1 MW, cu gaze și EUA la media lunii; fără costuri de pornire, deci o limită superioară.") + "}",
              it((t("\\textbf{Romania}, last 12 months", "\\textbf{România}, ultimele 12 luni"),
                  t("positive in @{opt.RO.itm_share|.0f}\\% of hours", "marjă pozitivă în @{opt.RO.itm_share|.0f}\\% din ore"),
                  t("must-run @{opt.RO.base_eur|,.0f}, flexible @{opt.RO.flex_eur|,.0f} EUR per MW", "continuă: @{opt.RO.base_eur|,.0f}; flexibilă: @{opt.RO.flex_eur|,.0f} EUR pe MW")),
                 (t("\\textbf{Germany}", "\\textbf{Germania}"),
                  t("positive in @{opt.DE_LU.itm_share|.0f}\\% of hours", "marjă pozitivă în @{opt.DE_LU.itm_share|.0f}\\% din ore"),
                  t("must-run @{opt.DE_LU.base_eur|,.0f}, flexible @{opt.DE_LU.flex_eur|,.0f} EUR per MW", "continuă: @{opt.DE_LU.base_eur|,.0f}; flexibilă: @{opt.DE_LU.flex_eur|,.0f} EUR pe MW")), sep="2pt"),
              t("value a gas plant or a battery as options, never as a mean spread times 8\\,760 h.",
                "evaluați o centrală pe gaze sau o baterie ca opțiuni, nu ca marjă medie înmulțită cu 8\\,760 h."),
              tryit=NB + " \\S4", cite="(Deng et al., 2001; Eydeland \\& Wolyniec, 2003)", wl="0.52", wr="0.45")

    D.chart(t("Sorted hourly spreads: the value lies in the best hours", "Marjele orare ordonate: valoarea stă în orele cele mai bune"), "spark_hourly", [
        t("The area above zero is the option value; at equal gas and carbon prices Romania has more profitable hours than Germany.",
          "Aria de deasupra lui zero este valoarea opțiunii; la aceleași prețuri ale gazelor și carbonului, România are mai multe ore profitabile decît Germania.")],
        height="0.60\\textheight", job=t("hedge a flexible plant with peak products, not with a band.",
                                         "acoperiți o centrală flexibilă cu produse de vîrf, nu cu bandă."),
        tryit=NB + " \\S4", cite=OWN)

    # ------------------------------------------------------------------ 4 hedge ratio, basis, shape
    hg = N["hedge"]
    D.section(t("Hedge ratio, basis risk and shape risk", "Raportul de acoperire, riscul de bază și riscul de profil"))
    D.concept(t("The minimum-variance hedge ratio is a regression slope", "Raportul de acoperire optim este panta unei regresii"),
              t("Choose the contracts per MWh of exposure that make the hedged cost vary least.",
                "Alegem numărul de contracte pe MWh expus care face costul acoperit cît mai stabil."),
              "\\[ h^{*}=\\arg\\min_h\\Var(\\Delta S-h\\Delta F)=\\rho\\frac{\\sigma_S}{\\sigma_F}=\\frac{\\Cov(\\Delta S,\\Delta F)}{\\Var(\\Delta F)} \\]"
              "\\[ \\Delta S_t=a+h\\,\\Delta F_t+\\varepsilon_t,\\qquad HE=\\rho^2 \\]" +
              "\\where{" + t("$\\Delta S$, $\\Delta F$ = monthly changes of the exposure and of the hedge; $\\rho$ = their correlation; hedge effectiveness (HE) = variance removed; "
                             "$h^{*}$ by ordinary least squares (OLS); derivation in Appendix A.",
                             "$\\Delta S$, $\\Delta F$ = variațiile lunare ale expunerii și ale instrumentului; $\\rho$ = corelația lor; eficiența acoperirii (HE) = varianța eliminată; "
                             "$h^{*}$ prin metoda celor mai mici pătrate (OLS); demonstrația în anexa A.") + "}",
              it((t("\\textbf{Instrument}", "\\textbf{Instrumentul}"),
                  t("a cash-settled future ends at its zone's monthly mean: we use HU and DE-LU means", "un contract futures financiar ajunge la media lunară a zonei sale: folosim mediile HU și DE-LU"),
                  t("@{hedge.HU.n|.0f} months, @{hedge.first|ym} -- @{hedge.last|ym}", "@{hedge.HU.n|.0f} " + de("hedge.HU.n") + "luni, @{hedge.first|ym} -- @{hedge.last|ym}")),
                 (t("\\textbf{Uncertainty}", "\\textbf{Incertitudinea}"),
                  t("HAC standard error, 3 lags", "eroare standard HAC, 3 decalaje"),
                  t("block bootstrap, @{hedge.block}-month blocks, @{hedge.B|,d} draws", "bootstrap pe blocuri de @{hedge.block} luni, @{hedge.B|,d} " + de("hedge.B") + "replicări")), sep="2pt"),
              t("a hedge ratio without a confidence interval is a guess.",
                "un raport de acoperire fără interval de încredere este o simplă presupunere."),
              tryit=NB + " \\S5", cite="(Johnson, 1960; Ederington, 1979)", wl="0.58", wr="0.39")

    def hrow(z, lab):
        h_ = hg[z]
        return [lab, fmt(h_["h"], ".3f", lang), fmt(h_["se"], ".3f", lang), "[" + fmt(h_["lo"], ".2f", lang) + "; " + fmt(h_["hi"], ".2f", lang) + "]",
                fmt(h_["r2"], ".2f", lang), fmt(h_["h_in"], ".2f", lang), fmt(h_["vr_oos_h"], ".1f", lang) + "\\%"]
    D.frame(t("Hungary hedges Romania almost fully; Germany leaves a fifth", "Contractele din Ungaria acoperă aproape tot riscul; cele germane lasă o cincime"),
            D.fig("hedge_scatter", "0.47\\textheight") + "\n\\vspace{0.3mm}\n" +
            "\\begin{center}" + table("@{}lrrrrrr@{}",
                                      [t("Hedge", "Instrument"), "$h^{*}$", t("HAC s.e.", "eroare std.\\ HAC"), t("bootstrap 95\\%", "bootstrap 95\\%"), "$R^2$",
                                       t("$h^{*}$ 2015--20", "$h^{*}$ 2015--20"), t("variance cut from 2021", "varianță eliminată, din 2021")],
                                      [hrow("HU", t("Hungary", "Ungaria")), hrow("DE_LU", t("Germany", "Germania"))], size="scriptsize", stretch="1.05") + "\\end{center}" +
            D.bottom(t("hedge with Hungarian futures before German ones.",
                       "folosiți contractele din Ungaria înaintea celor din Germania."), NB + " \\S5"),
            "footnotesize", cite=t("(own computation; out of sample: $h^{*}$ of 2015--2020 applied from 2021)", "(calcule proprii; $h^{*}$ din 2015--2020, testat din 2021)"))

    D.concept(t("Basis risk: what a foreign hedge leaves behind", "Riscul de bază: ce lasă descoperit un contract din altă zonă"),
              t("Hedged with a German future, a Romanian supplier pays the German forward plus the Romania--Germany gap at delivery.",
                "Acoperit cu un contract futures german, furnizorul din România plătește forward-ul german plus diferența România--Germania de la livrare."),
              "\\[ \\bar S^{\\text{RO}}-h(\\bar S^{X}-F^{X}_0)=hF^{X}_0+\\underbrace{(\\bar S^{\\text{RO}}-h\\bar S^{X})}_{\\text{" + t("basis } b", "baza } b") + "} \\]" +
              "\\where{" + t("$X$ = zone of the future (HU, DE-LU); $F^{X}_0$ = its price today; with $h=1$, $b$ = monthly price gap Romania minus $X$.",
                             "$X$ = zona contractului (HU, DE-LU); $F^{X}_0$ = prețul lui de azi; pentru $h=1$, $b$ = diferența lunară de preț România minus $X$.") + "}",
              it((t("\\textbf{Romania -- Hungary}", "\\textbf{România -- Ungaria}"),
                  t("mean @{basis.HU.mean|+.1f}, st.\\ dev.\\ @{basis.HU.sd|.1f} EUR/MWh", "media @{basis.HU.mean|+.1f}, abaterea standard @{basis.HU.sd|.1f} EUR/MWh"),
                  t("equal prices in @{basis.conv_hu.2021|.0f}\\% of hours in 2021", "prețuri egale în @{basis.conv_hu.2021|.0f}\\% din ore în 2021")),
                 (t("\\textbf{Romania -- Germany}", "\\textbf{România -- Germania}"),
                  t("mean @{basis.DE_LU.mean|+.1f}, st.\\ dev.\\ @{basis.DE_LU.sd|.1f}", "media @{basis.DE_LU.mean|+.1f}, abaterea standard @{basis.DE_LU.sd|.1f}"),
                  t("since 2023 mean @{basis.DE_LU.mean_post|+.1f} EUR/MWh", "din 2023, media @{basis.DE_LU.mean_post|+.1f} EUR/MWh")), sep="2pt"),
              t("a German hedge costs the German forward plus about @{basis.DE_LU.mean_post|.0f} EUR/MWh: price it in.",
                "o acoperire germană costă forward-ul german plus circa @{basis.DE_LU.mean_post|.0f} EUR/MWh: includeți diferența în ofertă."),
              tryit=NB + " \\S5", cite=t("(Hull, 2022; own computation)", "(Hull, 2022; calcule proprii)"), wl="0.55", wr="0.42")

    D.chart(t("The basis became more volatile after 2021, though RO and HU often share a price", "Volatilitatea bazei a crescut după 2021, deși RO și HU au adesea același preț"), "basis", [
        t("Basis to Germany, st.\\ dev.\\ @{basis.DE_LU.sd_pre|.1f} before 2021 and @{basis.DE_LU.sd_post|.1f} after; coupling steps: 17 June 2021 (Interim Coupling), 8 June 2022 (Core flow-based).",
          "Baza față de Germania: abaterea standard @{basis.DE_LU.sd_pre|.1f} înainte de 2021 și @{basis.DE_LU.sd_post|.1f} după; etape ale cuplării: 17 iunie 2021 (Interim Coupling), 8 iunie 2022 (Core, bazată pe fluxuri).")],
        height="0.60\\textheight", job=t("prices converge only without congestion: basis risk is congestion risk.",
                                         "prețurile se egalizează doar fără congestie: riscul de bază este un risc de congestie."),
        tryit=NB + " \\S5", cite=t("(own computation; ENTSO-E, 2021)", "(calcule proprii; ENTSO-E, 2021)"))

    D.concept(t("Shape risk: customers do not consume a flat band", "Riscul de profil: clienții nu consumă în bandă"),
              t("A band covers the same MW every hour; load is higher in dear hours, solar output in cheap ones.",
                "Banda acoperă aceeași putere în fiecare oră; consumul este mai mare în orele scumpe, producția solară în cele ieftine."),
              "\\[ f^{\\text{" + t("load", "cons") + "}}=\\frac{\\sum_h L_hP_h}{\\bar P\\sum_h L_h},\\qquad f^{\\text{solar}}=\\frac{\\sum_h Q_hP_h}{\\bar P\\sum_h Q_h} \\]" +
              "\\where{" + t("$L_h$ = Romanian load, $Q_h$ = solar output in hour $h$; $\\bar P$ = simple mean price of the year; $f>1$: the profile costs more than the band.",
                             "$L_h$ = consumul României, $Q_h$ = producția solară în ora $h$; $\\bar P$ = media simplă a anului; $f>1$: profilul costă mai mult decît banda.") + "}",
              it((t("\\textbf{Supplier}, national load", "\\textbf{Furnizorul}, consumul național"),
                  t("$f^{\\text{load}}$: @{shape.f_load.2019|.3f} (2019), @{shape.f_load.2025|.3f} (2025)", "$f^{\\text{cons}}$: @{shape.f_load.2019|.3f} (2019), @{shape.f_load.2025|.3f} (2025)"),
                  t("+@{shape.load_prem.2025|.1f} EUR/MWh over the band in 2025", "+@{shape.load_prem.2025|.1f} EUR/MWh peste bandă în 2025")),
                 (t("\\textbf{Solar producer}", "\\textbf{Producătorul solar}"),
                  t("$f^{\\text{solar}}$: @{shape.f_solar.2019|.3f} (2019), @{shape.f_solar.2025|.3f} (2025)", "$f^{\\text{solar}}$: @{shape.f_solar.2019|.3f} (2019), @{shape.f_solar.2025|.3f} (2025)"),
                  t("$-$@{shape.solar_disc.2025|.1f} EUR/MWh under the band in 2025", "$-$@{shape.solar_disc.2025|.1f} EUR/MWh sub bandă în 2025")), sep="2pt"),
              t("price a solar power purchase agreement (PPA) at the capture factor, not at the band forward.",
                "evaluați un contract de achiziție pe termen lung (PPA) pentru un parc solar la raportul de captare ($f^{\\text{solar}}$), nu la prețul benzii."),
              tryit=NB + " \\S5", cite=OWN, wl="0.53", wr="0.44")

    D.chart(t("Value of the solar and load profiles relative to baseload", "Valoarea profilului solar și a profilului de consum față de bandă"), "shape", [
        t("Solar capture factor down to @{shape.solar_min|.3f} in @{shape.solar_min_y}; load-weighted price @{shape.load_prem.2025|.1f} EUR/MWh above the band in 2025.",
          "Raportul de captare solar a scăzut la @{shape.solar_min|.3f} în @{shape.solar_min_y}; în 2025, prețul ponderat cu consumul a depășit banda cu @{shape.load_prem.2025|.1f} EUR/MWh.")],
        height="0.60\\textheight", job=t("buy band for the base of the portfolio, peak and hourly products for the shape.",
                                         "cumpărați bandă pentru baza portofoliului și produse de vîrf sau orare pentru profil."),
        tryit=NB + " \\S5", cite=OWN)

    # ------------------------------------------------------------------ 5 options
    D.section(t("Options on energy", "Opțiuni pe energie"))
    D.concept(t("Caps, floors and collars", "Plafon, prag minim și collar"),
              t("A call caps the purchase price and keeps the gain if prices fall; it costs a premium today.",
                "O opțiune call plafonează prețul de cumpărare și păstrează cîștigul dacă prețurile scad; costă o primă plătită azi."),
              "\\[ \\underbrace{(F_T-K)^+}_{\\text{call}},\\quad \\underbrace{(K-F_T)^+}_{\\text{put}},\\quad \\underbrace{\\min(F_T,K_c)+c}_{\\text{" + t("price with a cap", "preț cu plafon") + "}} \\]"
              "\\[ \\text{collar: } \\max\\big(K_p,\\min(F_T,K_c)\\big)+c-p \\]" +
              "\\where{" + t("$F_T$ = forward price at expiry $T$; $K$ = strike; $c$, $p$ = call and put premiums; collar = buy a call at $K_c$, sell a put at $K_p<K_c$.",
                             "$F_T$ = prețul forward la scadența $T$; $K$ = prețul de exercitare; $c$, $p$ = primele call și put; collar = cumpărare call la $K_c$ și vînzare put la $K_p<K_c$.") + "}",
              it((t("\\textbf{Who uses what}", "\\textbf{Cine ce folosește}"),
                  t("supplier: a cap (call)", "furnizorul: plafon (call)"),
                  t("producer: a floor (put)", "producătorul: prag minim (put)"),
                  t("both: a low-cost collar (the supplier buys a call and sells a put; the producer the reverse)", "amîndoi: un collar cu cost redus (furnizorul cumpără call și vinde put; producătorul invers)")),
                 (t("\\textbf{In Romania}", "\\textbf{În România}"),
                  t("no listed power options", "nu există opțiuni pe energie listate"),
                  t("caps sit inside bilateral and PPA contracts", "plafoanele apar în contracte bilaterale și PPA")), sep="2pt"),
              t("buy a cap when a spike would break the firm, not when it would merely hurt.",
                "cumpărați un plafon cînd un salt de preț ar pune firma în pericol, nu doar cînd i-ar reduce profitul."),
              tryit=NB + " \\S6", cite="(Hull, 2022)", wl="0.56", wr="0.41")

    D.concept(t("Black-76 prices an option on a forward from five inputs", "Modelul Black-76 evaluează o opțiune pe forward cu cinci parametri"),
              t("Under the pricing measure a forward has no drift, so the option depends only on $F$, $K$, $T$, $r$ and $\\sigma$.",
                "În evaluarea neutră la risc, forward-ul nu are tendință, deci opțiunea depinde doar de $F$, $K$, $T$, $r$ și $\\sigma$."),
              "\\[ C=e^{-rT}[F\\Phi(d_1)-K\\Phi(d_2)],\\quad P=e^{-rT}[K\\Phi(-d_2)-F\\Phi(-d_1)] \\]"
              "\\[ d_1=\\frac{\\ln(F/K)+\\sigma^2T/2}{\\sigma\\sqrt T},\\qquad d_2=d_1-\\sigma\\sqrt T \\]" +
              "\\where{" + t("$\\Phi$ = standard normal distribution function; $\\sigma$ = annual volatility of $\\ln F$; $T$ in years; $r$ = continuous rate (Appendix B).",
                             "$\\Phi$ = funcția de repartiție normală standard; $\\sigma$ = volatilitatea anuală a lui $\\ln F$; $T$ în ani; $r$ = rata dobînzii fără risc, cu capitalizare continuă (anexa B).") + "}",
              it((t("\\textbf{Inputs}, " + Y1 + " band", "\\textbf{Datele de intrare}, banda pentru " + Y1),
                  t("$F$ = @{bs.F|.2f} EUR/MWh (OPCOM VWAP)", "$F$ = @{bs.F|.2f} EUR/MWh (VWAP OPCOM)"),
                  t("$T$ = @{bs.T_days} days; $r$ = @{bs.r|.2f}\\% (€STR)", "$T$ = @{bs.T_days} de zile; $r$ = @{bs.r|.2f}\\% (€STR)"),
                  t("$\\sigma$ = @{bs.sig_cal|.3f} (next slide)", "$\\sigma$ = @{bs.sig_cal|.3f} (diapozitivul următor)")),
                 (t("\\textbf{Prices}, EUR/MWh", "\\textbf{Prețuri}, EUR/MWh"),
                  t("$K=F$: call = put = @{bs.c.call|.2f}", "$K=F$: call = put = @{bs.c.call|.2f}"),
                  t("cap at 1.1 $F$: @{bs.c.call110|.2f}", "plafon la 1,1 $F$: @{bs.c.call110|.2f}"),
                  t("floor at 0.9 $F$: @{bs.c.put90|.2f}", "prag minim la 0,9 $F$: @{bs.c.put90|.2f}")), sep="1pt"),
              t("ask the bank which volatility it used; the premium grows almost linearly with $\\sigma$.",
                "întrebați banca ce volatilitate a folosit; prima crește aproape proporțional cu $\\sigma$."),
              tryit=NB + " \\S6", cite="(Black, 1976; Hull, 2022)", wl="0.58", wr="0.39")

    D.frame(t("Volatility is the input you must estimate; real estimates disagree", "Volatilitatea trebuie estimată, iar estimările reale diferă"), cols(
        it((t("\\textbf{1. Romanian yearly forwards}", "\\textbf{1. Forward-urile anuale din România}"),
            t("irregular auctions: $\\hat\\sigma^2=\\sum_k(\\Delta\\ln F_k)^2/\\sum_k\\Delta t_k$, gaps $\\le$ 30 days",
              "licitații neregulate: $\\hat\\sigma^2=\\sum_k(\\Delta\\ln F_k)^2/\\sum_k\\Delta t_k$, intervale de cel mult 30 de zile"),
            t("$\\hat\\sigma$ = @{calvol.pooled|.3f} on @{calvol.n} pairs of auction days", "$\\hat\\sigma$ = @{calvol.pooled|.3f}, din @{calvol.n} " + de("calvol.n") + "perechi de zile cu licitații")),
           (t("\\textbf{2. TTF future, January " + Y1 + "}", "\\textbf{2. Contractul TTF pentru ianuarie " + Y1 + "}"),
            t("last 60 trading days: $\\hat\\sigma$ = @{bs.sig_gas|.3f}; call @{bs.g.call|.2f}", "ultimele 60 de zile: $\\hat\\sigma$ = @{bs.sig_gas|.3f}; call @{bs.g.call|.2f}")),
           (t("\\textbf{3. Month average vs forward}", "\\textbf{3. Media lunară față de forward}"),
            t("$\\text{sd}(\\ln(\\bar S/F)/\\sqrt T)$ = @{termvol.all|.3f}, @{termvol.n} auctions", "$\\text{sd}(\\ln(\\bar S/F)/\\sqrt T)$ = @{termvol.all|.3f}, @{termvol.n} " + de("termvol.n") + "licitații")), sep="2pt"),
        it((t("\\textbf{Why they differ}", "\\textbf{De ce diferă}"),
            t("a year averages 8\\,760 hours, far calmer than a month", "un an este media a 8\\,760 de ore, mult mai stabilă decît o lună"),
            t("gas has its own crisis in " + Y, "gazele trec printr-o criză proprie în " + Y),
            t("no free implied volatility for Romania", "nu există volatilitate implicită gratuită pentru România")),
           (t("\\textbf{Better}", "\\textbf{Mai bine}"),
            t("generalised autoregressive conditional heteroskedasticity (GARCH) models of Lecture 3",
              "modelele de heteroscedasticitate condiționată autoregresivă generalizată (GARCH) din cursul 3")), sep="2pt"), "0.55", "0.42") +
        D.bottom(t("match the volatility to the underlying: year, quarter or month.",
                   "alegeți volatilitatea potrivită activului suport: an, trimestru sau lună."), NB + " \\S6"),
        "footnotesize", cite=t("(own computation; OPCOM; Yahoo Finance)", "(calcule proprii; OPCOM; Yahoo Finance)"))

    D.chart(t("Near contracts move more: the Samuelson effect in TTF", "Contractele apropiate de livrare variază mai mult: efectul Samuelson"), "samuelson", [
        t("@{sam.w_from|date} -- @{sam.w_to|date}: December " + Y + " @{sam.2026-12.v12|.0f}\\%, May " + Y1 + " @{sam.2027-05.v12|.0f}\\% a year; in 2022 both near @{sam.2026-12.v22|.0f}\\%.",
          "Volatilitatea anualizată, @{sam.w_from|date} -- @{sam.w_to|date}: contractul pentru decembrie " + Y + " -- @{sam.2026-12.v12|.0f}\\%, cel pentru mai " + Y1 + " -- @{sam.2027-05.v12|.0f}\\%; în 2022, ambele în jur de @{sam.2026-12.v22|.0f}\\%.")],
        height="0.60\\textheight", job=t("an option close to delivery needs a higher volatility.",
                                         "o opțiune apropiată de livrare cere o volatilitate mai mare."),
        tryit=NB + " \\S6", cite=t("(own computation; Samuelson, 1965)", "(calcule proprii; Samuelson, 1965)"))

    D.concept(t("Delta and vega: the option in MWh, and its volatility risk", "Delta și vega: echivalentul în MWh forward și sensibilitatea la volatilitate"),
              t("Delta is the forward quantity that offsets the option; vega is the premium change per volatility point.",
                "Delta este cantitatea de forward care compensează opțiunea; vega este variația primei la un punct de volatilitate."),
              "\\[ \\Delta_C=e^{-rT}\\Phi(d_1),\\quad \\Delta_P=-e^{-rT}\\Phi(-d_1) \\]"
              "\\[ \\mathcal V=e^{-rT}F\\varphi(d_1)\\sqrt T,\\qquad C-P=e^{-rT}(F-K) \\]" +
              "\\where{" + t("$\\varphi$ = standard normal density; $\\mathcal V$ per volatility point (0.01); the last identity is put--call parity.",
                             "$\\varphi$ = densitatea normală standard; $\\mathcal V$ pe un punct de volatilitate (0{,}01); ultima relație este paritatea put--call.") + "}",
              it((t("\\textbf{$K=F$}, $\\sigma$ = @{bs.sig_cal|.3f}", "\\textbf{$K=F$}, $\\sigma$ = @{bs.sig_cal|.3f}"),
                  t("$d_1$ = @{bs.c.d1|.3f}; $\\Delta_C$ = @{bs.c.delta_c|.3f}, $\\Delta_P$ = @{bs.c.delta_p|.3f}", "$d_1$ = @{bs.c.d1|.3f}; $\\Delta_C$ = @{bs.c.delta_c|.3f}, $\\Delta_P$ = @{bs.c.delta_p|.3f}"),
                  t("vega @{bs.c.vega|.3f} EUR/MWh", "vega @{bs.c.vega|.3f} EUR/MWh"),
                  t("$C=P$, as parity requires", "$C=P$, cum cere paritatea")),
                 (t("\\textbf{Cap at 1.1 $F$}", "\\textbf{Plafonul la 1,1 $F$}"),
                  t("delta @{bs.c.delta_c110|.3f}", "delta @{bs.c.delta_c110|.3f}"),
                  t("cap premium for 1 MW over a year: @{bs.mw_year|,.0f} EUR", "costul plafonului pentru 1 MW pe un an: @{bs.mw_year|,.0f} EUR")), sep="2pt"),
              t("the seller of a cap hedges by holding delta MWh forward and rebalancing.",
                "vînzătorul plafonului se acoperă deținînd contracte forward într-o cantitate egală cu delta, pe care o ajustează periodic."),
              tryit=NB + " \\S6", cite="(Black, 1976; Hull, 2022)", wl="0.52", wr="0.45")

    D.chart(t("What each instrument pays for the " + Y1 + " band", "Prețul efectiv al benzii pentru " + Y1 + " cu fiecare instrument"), "collar", [
        t("Forward @{bs.F|.1f}; cap at @{bs.K110|.1f} costs @{bs.c.call110|.2f}; collar @{bs.K90|.1f} -- @{bs.K110|.1f} costs @{bs.c.collar|.2f} EUR/MWh; spikes and monthly averages (Asian options) break Black-76.",
          "Forward @{bs.F|.1f}; plafonul la @{bs.K110|.1f} costă @{bs.c.call110|.2f}; collarul @{bs.K90|.1f} -- @{bs.K110|.1f} costă @{bs.c.collar|.2f} EUR/MWh; salturile și mediile lunare (opțiuni asiatice) încalcă ipotezele Black-76.")],
        height="0.58\\textheight", job=t("a near-zero-cost collar lets a supplier sell a capped retail price.",
                                         "un collar cu cost aproape zero permite furnizorului să ofere un preț plafonat."),
        tryit=NB + " \\S6", cite="(Black, 1976; Weron, 2008)")

    # ------------------------------------------------------------------ 6 case study
    cs = N["case"]
    D.section(t("Case study: a Romanian supplier and a producer", "Studiu de caz: un furnizor și un producător din România"))
    D.frame(t("Case study: a supplier with a 1 MW fixed-price customer in " + Y, "Studiul de caz: un furnizor cu un client de 1 MW la preț fix, " + Y), it(
        t(("\\textbf{The position}", "1 MW flat for all of " + Y + " sold at a fixed price; energy still to be bought",
           "measured on @{case.months} delivered months, to @{case.m_last|ym}"),
          ("\\textbf{Poziția}", "1 MW în bandă, vîndut la preț fix pentru tot anul " + Y + "; energia trebuie cumpărată",
           "evaluare pe cele @{case.months} luni deja livrate, pînă în @{case.m_last|ym}")),
        t(("\\textbf{Four strategies, real prices}", "unhedged: buy each month at the realised spot mean",
           "100\\% forward: OPCOM band " + Y + ", VWAP @{case.F26|.2f} EUR/MWh, @{case.n26} auctions",
           "50\\% forward, 50\\% spot",
           "monthly caps bought 15 Dec " + Y0 + ", $K$ = @{case.Fref|.2f} (VWAP of the last @{case.nref} auctions), Black-76, $\\sigma$ = @{termvol.all|.3f}"),
          ("\\textbf{Patru strategii, prețuri reale}", "fără acoperire: cumpără lunar la media spot realizată",
           "100\\% forward: banda OPCOM pentru " + Y + ", VWAP @{case.F26|.2f} EUR/MWh, @{case.n26} " + de("case.n26") + "licitații",
           "50\\% forward, 50\\% spot",
           "plafoane lunare cumpărate la 15 decembrie " + Y0 + ", $K$ = @{case.Fref|.2f} (VWAP al ultimelor @{case.nref} licitații), Black-76, $\\sigma$ = @{termvol.all|.3f}")),
        t(("\\textbf{What we report}", "mean cost, its month-to-month standard deviation, the worst month, total cost per MW"),
          ("\\textbf{Ce raportăm}", "costul mediu, abaterea standard de la o lună la alta, cea mai scumpă lună, costul total pe MW")),
        sep="3pt") + D.bottom(t("a supplier's risk committee should see exactly this table every month.",
                                "comitetul de risc al unui furnizor ar trebui să vadă lunar exact acest calcul."), NB + " \\S7"),
        "footnotesize", cite=t("(own computation; OPCOM)", "(calcule proprii; OPCOM)"))

    D.chart(t("Case study: in " + Y + " the forward beat the spot in @{case.n_fwd_win} of @{case.months} months", "Studiul de caz: în " + Y + ", forward-ul a fost mai ieftin în @{case.n_fwd_win} din @{case.months} luni"), "case2026", [
        t("Spot peak @{case.spot.max|.1f} EUR/MWh in @{case.spot_max_ym|ym}; the caps paid out in @{case.n_cap_pay} of @{case.months} months.",
          "Prețul spot a atins @{case.spot.max|.1f} EUR/MWh în @{case.spot_max_ym|ym}; plafoanele s-au exercitat în @{case.n_cap_pay} din @{case.months} luni.")],
        height="0.60\\textheight", job=t("a cap costs its premium every month, also when it pays nothing.",
                                         "prima plafonului se plătește în fiecare lună, chiar și atunci cînd opțiunea nu se exercită."),
        tryit=NB + " \\S7", cite=t("(own computation; OPCOM)", "(calcule proprii; OPCOM)"))

    def crow(k, lab):
        c = cs[k]
        return [lab, fmt(c["mean"], ".1f", lang), fmt(c["sd"], ".1f", lang), fmt(c["max"], ".1f", lang), fmt(c["eur_mw"], ",.0f", lang)]
    D.frame(t("Case study: the forward cut cost and risk; the cap cut risk", "Studiul de caz: forward-ul a redus costul și riscul"), cols(
        table("@{}lrrrr@{}", [t("EUR/MWh", "EUR/MWh"), t("mean", "media"), t("st.\\ dev.", "abat.\\ std."), t("worst", "maxim"), t("EUR/MW", "EUR/MW")],
              [crow("spot", t("spot", "spot")), crow("fwd", t("100\\% forward", "100\\% forward")),
               crow("half", t("50\\% forward", "50\\% forward")), crow("cap", t("caps", "plafoane"))], size="footnotesize", stretch="1.25") +
        note(t("Weighted by the hours of each month.", "Ponderat cu numărul de ore al fiecărei luni.")),
        it((t("\\textbf{Reading}", "\\textbf{Interpretare}"),
            t("forward: @{case.save_fwd|,.0f} EUR per MW saved, zero variation", "forward: @{case.save_fwd|,.0f} EUR economisiți pe MW, fără variație"),
            t("caps: premium @{case.prem_mean|.1f} EUR/MWh a month; net @{case.save_cap|,.0f} EUR per MW", "plafoane: prima medie @{case.prem_mean|.1f} EUR/MWh pe lună; economie netă @{case.save_cap|,.0f} EUR pe MW")),
           (t("\\textbf{Not a general verdict}", "\\textbf{Nu este o regulă generală}"),
            t("prices rose after the hedge; in a falling year the forward costs more than spot",
              "prețurile au crescut după acoperire; într-un an cu prețuri în scădere, forward-ul costă mai mult decît spotul")), sep="3pt"),
        "0.50", "0.47") + D.bottom(t("set the hedged share by policy (e.g.\\ 60--80\\% bought in layers), not by a price view.",
                                     "stabiliți ponderea acoperită prin politică (de exemplu 60--80\\%, eșalonat), nu după o opinie despre prețuri."), NB + " \\S7"),
        "footnotesize", cite=OWN)

    D.frame(t("The producer's side, and the summer 2024 spike", "Perspectiva producătorului și saltul de preț din vara lui 2024"), it(
        t(("\\textbf{Producer, 2025}", "@{prod.n25} auctions, VWAP @{prod.F25|.1f} vs realised @{prod.S25|.1f} EUR/MWh",
           "selling forward earned @{prod.loss|.1f} EUR/MWh less than spot (@{prod.loss_mw|,.0f} EUR per MW-year), the price of a fixed revenue",
           "in 2022 the same decision cost @{prod.loss22|.1f} EUR/MWh"),
          ("\\textbf{Producătorul, 2025}", "@{prod.n25} " + de("prod.n25") + "licitații, VWAP @{prod.F25|.1f}, față de media realizată de @{prod.S25|.1f} EUR/MWh",
           "vînzarea forward a adus cu @{prod.loss|.1f} EUR/MWh mai puțin decît spotul (@{prod.loss_mw|,.0f} EUR pe MW și an): prețul unui venit sigur",
           "în 2022, aceeași decizie a costat @{prod.loss22|.1f} EUR/MWh")),
        t(("\\textbf{Summer 2024}", "third quarter bought at @{s24.F_q3|.1f}, delivered at @{s24.S_q3|.1f} EUR/MWh; July alone @{s24.S_jul|.1f}",
           "peak hour @{s24.max_h|.1f} EUR/MWh on @{s24.max_h_ts|dt}, Central European Time (CET)"),
          ("\\textbf{Vara lui 2024}", "contractul pentru trimestrul al treilea s-a tranzacționat la @{s24.F_q3|.1f} EUR/MWh, iar media spot realizată a fost @{s24.S_q3|.1f}; în iulie: @{s24.S_jul|.1f}",
           "ora cea mai scumpă: @{s24.max_h|.1f} EUR/MWh, pe @{s24.max_h_ts|dt} ora Europei Centrale (CET)")),
        t(("\\textbf{The lesson}", "a hedge transfers value between the two sides; it makes cash flows predictable, which lenders pay for"),
          ("\\textbf{Concluzia}", "acoperirea transferă valoare între cele două părți; face fluxurile de numerar previzibile, iar creditorii răsplătesc această previzibilitate prin condiții de finanțare mai bune")),
        sep="3pt") + D.bottom(t("a producer with debt should sell forward even when it expects higher prices.",
                                "un producător îndatorat ar trebui să vîndă forward chiar dacă se așteaptă la prețuri mai mari."), NB + " \\S7"),
        "footnotesize", cite=t("(own computation; OPCOM; Andrei, Pele \\& Cramer, 2026, PICBE)", "(calcule proprii; OPCOM; Andrei, Pele \\& Cramer, 2026, PICBE)"))

    D.frame(t("Elements of a hedging policy", "Elementele unei politici de acoperire a riscului"), cols(
        it((t("\\textbf{Exposure}", "\\textbf{Expunerea}"),
            t("net position per month and profile (band, peak, solar)", "poziția netă pe lună și pe profil (bandă, vîrf, solar)"),
            t("volume risk: demand hardly reacts to price", "riscul de volum: cererea reacționează foarte puțin la preț")),
           (t("\\textbf{Instruments}", "\\textbf{Instrumentele}"),
            t("OPCOM forwards first, then Hungarian, then German futures", "întîi forward OPCOM, apoi futures din Ungaria, apoi din Germania"),
            t("caps for the tail, not for all the volume", "plafoane pentru extreme, nu pentru tot volumul")), sep="3pt"),
        it((t("\\textbf{Execution}", "\\textbf{Execuția}"),
            t("buy in layers over 12--24 months", "cumpărați eșalonat, pe 12--24 de luni"),
            t("keep a liquidity buffer for margin calls", "păstrați o rezervă de lichiditate pentru apelurile în marjă")),
           (t("\\textbf{Control}", "\\textbf{Controlul}"),
            t("limits on open position and VaR (Lecture 4)", "limite pentru poziția deschisă și VaR (cursul 4)"),
            t("report hedged cost and its variance", "raportați costul acoperit și varianța lui")), sep="3pt"), "0.50", "0.47") +
        D.bottom(t("the board approves the policy, traders execute it, risk management measures it.",
                   "consiliul aprobă politica, traderii o execută, departamentul de risc o măsoară."), None),
        "footnotesize", cite=t("(Hull, 2022; Proșcanu, Proșcanu \\& Pele, 2025, JSES; Lecture 4)", "(Hull, 2022; Proșcanu, Proșcanu \\& Pele, 2025, JSES; cursul 4)"))

    # ------------------------------------------------------------------ wrap-up
    D.parts.append("\\section*{" + t("Wrap-up", "Recapitulare") + "}\n")
    D.quiz_frame(t("basis risk", "riscul de bază"),
                 t("A Romanian supplier hedged July 2024 with German baseload futures bought at $F$; July averaged @{basis.DE_LU.max_de|.1f} in Germany and @{basis.DE_LU.max_ro|.1f} EUR/MWh in Romania; what did it pay per MWh?",
                   "Un furnizor din România și-a acoperit luna iulie 2024 cu contracte futures germane în bandă, cumpărate la prețul $F$; media lunii a fost @{basis.DE_LU.max_de|.1f} în Germania și @{basis.DE_LU.max_ro|.1f} EUR/MWh în România; cît a plătit pe MWh?"),
                 t("It bought at @{basis.DE_LU.max_ro|.1f} in Romania and received from the future the difference between @{basis.DE_LU.max_de|.1f} and $F$: net cost $F$ + @{basis.DE_LU.max|.1f} EUR/MWh, the largest monthly basis in our data.",
                   "A cumpărat la @{basis.DE_LU.max_ro|.1f} în România și a primit din contractul futures diferența dintre @{basis.DE_LU.max_de|.1f} și $F$: costul net este $F$ + @{basis.DE_LU.max|.1f} EUR/MWh, cea mai mare bază lunară din datele noastre."))
    D.quiz_frame(t("the hedge ratio", "raportul de acoperire"),
                 t("Our estimate for Hungary is $h^{*}$ = @{hedge.HU.h|.3f} with a bootstrap interval [@{hedge.HU.lo|.2f}; @{hedge.HU.hi|.2f}]; a 20 MW exposure needs how many MW of Hungarian futures?",
                   "Estimarea noastră pentru Ungaria este $h^{*}$ = @{hedge.HU.h|.3f}, cu intervalul bootstrap [@{hedge.HU.lo|.2f}; @{hedge.HU.hi|.2f}]; cîți MW de contracte futures din Ungaria acoperă o expunere de 20 MW?"),
                 t("20 $\\times$ @{hedge.HU.h|.3f} = @{hedge.HU.q20|.1f} MW; since 1 lies inside the interval, a one-for-one hedge of 20 MW is statistically as good.",
                   "20 $\\times$ @{hedge.HU.h|.3f} = @{hedge.HU.q20|.1f} MW; deoarece valoarea 1 se află în interval, o acoperire integrală ($h=1$), de 20 MW, este la fel de bună din punct de vedere statistic."))
    D.quiz_frame(t("spark spread", "clean spark spread"),
                 t("In @{spread.lastm.ym|ym}: power @{spread.lastm.p|.1f}, gas @{spread.lastm.gas|.1f} EUR/MWh, EUA @{spread.lastm.eua|.1f} EUR/t; efficiency 50\\%, 0.202 t CO$_2$ per MWh thermal; did a gas plant earn money on average?",
                   "În @{spread.lastm.ym|ym}: energia @{spread.lastm.p|.1f}, gazele @{spread.lastm.gas|.1f} EUR/MWh, EUA @{spread.lastm.eua|.1f} EUR/t; randament 50\\%, 0,202 t CO$_2$ pe MWh termic; a cîștigat, în medie, o centrală pe gaze?"),
                 t("Fuel @{spread.lastm.gas|.1f}/0.5 = @{spread.lastm.fuel|.1f}; carbon 0.404 $\\times$ @{spread.lastm.eua|.1f} = @{spread.lastm.co2|.1f}; clean spark @{spread.lastm.css|+.1f} EUR/MWh: yes, even before choosing the best hours.",
                   "Combustibilul: @{spread.lastm.gas|.1f}/0,5 = @{spread.lastm.fuel|.1f}; carbonul: 0,404 $\\times$ @{spread.lastm.eua|.1f} = @{spread.lastm.co2|.1f}; clean spark spread @{spread.lastm.css|+.1f} EUR/MWh: da, chiar înainte de a alege orele cele mai bune."))
    D.quiz_frame(t("a cap for a supplier", "un plafon pentru un furnizor"),
                 t("The " + Y1 + " band trades at @{bs.F|.1f}; a cap at @{bs.K110|.1f} costs @{bs.c.call110|.2f} EUR/MWh; what does the supplier pay if the forward ends at 1.3 $F$, and at 0.9 $F$?",
                   "Banda pentru " + Y1 + " se tranzacționează la @{bs.F|.1f}; un plafon la @{bs.K110|.1f} costă @{bs.c.call110|.2f} EUR/MWh; cît plătește furnizorul dacă prețul forward ajunge la 1,3 $F$, respectiv la 0,9 $F$?"),
                 t("At 1.3 $F$: the strike @{bs.K110|.1f} plus the premium; at 0.9 $F$: the market price plus the premium, since the cap is not exercised.",
                   "La 1,3 $F$: prețul de exercitare de @{bs.K110|.1f} plus prima; la 0,9 $F$: prețul pieței plus prima, deoarece plafonul nu se exercită."))

    D.frame(t("Wrap-up", "Recapitulare"), "\\vspace{-2mm}\\begin{multicols}{2}\\scriptsize\\tableofcontents\\end{multicols}\n" + it(
        t("A forward turns an unknown spot into a known price; in 2022 it saved a Romanian supplier @{crisis.eur_per_mw_m|.2f} million EUR per MW, and cost producers the same.",
          "Un contract forward transformă un preț spot necunoscut într-un preț cunoscut; în 2022 i-a adus unui furnizor din România o economie de @{crisis.eur_per_mw_m|.2f} milioane EUR pe MW, iar producătorii care au vîndut forward au pierdut aceeași sumă."),
        t("Hedge Romania with Hungary before Germany, price the shape, and match the volatility to the underlying; next: Lecture 6.",
          "Acoperiți riscul din România cu contracte din Ungaria, înaintea celor din Germania; includeți profilul în preț și alegeți volatilitatea potrivită activului suport; urmează cursul 6."),
        sep="1pt"))

    D.frame(t("Research from our group on Romanian power risk", "Cercetările grupului nostru despre riscul pe piața energiei din România"), it(
        t(("\\textbf{The summer 2024 price spike} (Andrei, Pele \\& Cramer, 2026, PICBE)", "question: which intervention would have lowered Romanian prices most in June--July 2024",
           "method: a random forest on hourly ENTSO-E data, 147 counterfactual scenarios, checked against ridge regression",
           "result: a 10\\% load reduction was the most effective measure; the peak came at night, so solar could not help and storage is the enabling asset"),
          ("\\textbf{Saltul de preț din vara lui 2024} (Andrei, Pele \\& Cramer, 2026, PICBE)", "întrebarea: ce intervenție ar fi redus cel mai mult prețurile din România în iunie--iulie 2024",
           "metoda: o pădure aleatoare (random forest) pe date orare ENTSO-E, 147 de scenarii contrafactuale, verificate cu o regresie ridge",
           "rezultatul: reducerea consumului cu 10\\% este cea mai eficientă măsură; vîrful a avut loc noaptea, deci energia solară nu putea ajuta, iar stocarea devine esențială")),
        t(("\\textbf{Systemic risk in the EU energy sector} (Toma, Dima, Grecu, Pele \\& Lessmann, 2026, SSRN)", "method: the Energy Financial Risk Meter, a least absolute shrinkage and selection operator (LASSO) quantile regression on daily returns of 100 European energy companies",
           "result: the index captures the 2020 pandemic and the 2022 war; a geopolitical-to-energy risk channel switched on"),
          ("\\textbf{Riscul sistemic în sectorul energetic din UE} (Toma, Dima, Grecu, Pele \\& Lessmann, 2026, SSRN)", "metoda: indicatorul Energy Financial Risk Meter, construit prin regresie cuantilică cu operatorul de contracție și selecție în normă absolută (LASSO) pe randamentele zilnice a 100 de companii energetice europene",
           "rezultatul: indicele surprinde pandemia din 2020 și războiul din 2022; se activează un canal de transmitere a riscului geopolitic către sectorul energetic")),
        t(("\\textbf{Demand barely reacts to price} (Proșcanu, Proșcanu \\& Pele, 2025, JSES)", "method: Granger causality and vector autoregressions on Romanian consumption and prices",
           "result: consumption is inelastic and drives price, not the reverse, so volume cannot hedge price risk"),
          ("\\textbf{Cererea reacționează foarte puțin la preț} (Proșcanu, Proșcanu \\& Pele, 2025, JSES)", "metoda: cauzalitate Granger și modele vectoriale autoregresive pe consumul și prețurile din România",
           "rezultatul: consumul este inelastic și influențează prețul, nu invers; de aceea volumul nu poate compensa riscul de preț")),
        sep="3pt") + note(t("Findings as stated in the papers; numbers on the other slides come from our own data.",
                            "Rezultatele de pe acest diapozitiv sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.")),
        "footnotesize", cite=t("(Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting)",
                               "(Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică)"))

    D.frame(t("Want to learn more?", "Lecturi și resurse suplimentare"), cols(it(
        t("\\textbf{J.\\ Hull, Options, Futures, and Other Derivatives}, chapters on hedging, futures and Black's model.",
          "\\textbf{J.\\ Hull, Options, Futures, and Other Derivatives}, capitolele despre acoperirea riscului, contracte futures și modelul Black."),
        t("\\textbf{Benth, Šaltytė Benth \\& Koekebakker (2008)}: forward curves and options in electricity markets.",
          "\\textbf{Benth, Šaltytė Benth \\& Koekebakker (2008)}: curbe forward și opțiuni pe piețele de energie electrică."),
        t("\\textbf{OPCOM reports}: forward auction results, the source of this lecture --- ", "\\textbf{Rapoartele OPCOM}: rezultatele licitațiilor forward, sursa acestui curs --- ") +
        "\\href{https://www.opcom.ro/rapoarte-pccb-le-flex-rez-pccb-le-flex/ro}{opcom.ro}.", sep="4pt"),
        it(t("\\textbf{This course}: code, data, notebooks --- ", "\\textbf{Acest curs}: cod, date, notebook-uri Jupyter --- ") +
           "\\href{https://github.com/danpele/EMQA}{github.com/danpele/EMQA}.",
           t("\\textbf{ACER (2022)}: the final assessment of the EU wholesale electricity market design.",
             "\\textbf{ACER (2022)}: evaluarea finală a modelului pieței angro de energie electrică din UE."),
           t("\\textbf{Experiment yourself}: the notebook reproduces every chart and number of this lecture --- ",
             "\\textbf{Exercițiu practic}: notebook-ul Jupyter reproduce toate graficele și cifrele din acest curs --- ") +
           "\\href{\\emqarepo/\\emqanb}{notebooks/}.", sep="4pt"), "0.52", "0.45"))

    REFS = [
        "ACER (2022). \\textit{ACER's Final Assessment of the EU Wholesale Electricity Market Design}. Ljubljana, April 2022. "
        "\\href{https://www.acer.europa.eu/events-and-engagement/news/press-release-acer-publishes-its-final-assessment-eu-wholesale}{acer.europa.eu}",
        "Andrei, A.-V., Pele, D.-T.\\ \\& Cramer, A.-A.\\ (2026). Evaluating intervention effectiveness during extreme price events: A counterfactual "
        "analysis of Romania's 2024 energy crisis. \\textit{Proceedings of the International Conference on Business Excellence}, 20(1), 84--103. "
        "\\href{https://doi.org/10.2478/picbe-2026-0013}{doi:10.2478/picbe-2026-0013}",
        "Benth, F.\\,E., Šaltytė Benth, J.\\ \\& Koekebakker, S.\\ (2008). \\textit{Stochastic Modeling of Electricity and Related Markets}. "
        "World Scientific. \\href{https://doi.org/10.1142/6811}{doi:10.1142/6811}",
        "Bessembinder, H.\\ \\& Lemmon, M.\\,L.\\ (2002). Equilibrium pricing and optimal hedging in electricity forward markets. "
        "\\textit{Journal of Finance}, 57(3), 1347--1382. \\href{https://doi.org/10.1111/1540-6261.00463}{doi:10.1111/1540-6261.00463}",
        "Black, F.\\ (1976). The pricing of commodity contracts. \\textit{Journal of Financial Economics}, 3(1--2), 167--179. "
        "\\href{https://doi.org/10.1016/0304-405X(76)90024-6}{doi:10.1016/0304-405X(76)90024-6}",
        "Deng, S.-J., Johnson, B.\\ \\& Sogomonian, A.\\ (2001). Exotic electricity options and the valuation of electricity generation and "
        "transmission assets. \\textit{Decision Support Systems}, 30(3), 383--392. \\href{https://doi.org/10.1016/S0167-9236(00)00112-3}{doi:10.1016/S0167-9236(00)00112-3}",
        "Ederington, L.\\,H.\\ (1979). The hedging performance of the new futures markets. \\textit{Journal of Finance}, 34(1), 157--170. "
        "\\href{https://doi.org/10.1111/j.1540-6261.1979.tb02077.x}{doi:10.1111/j.1540-6261.1979.tb02077.x}",
        "ENTSO-E (2021). Successful go-live of Interim Coupling, reaching the SDAC enduring phase. Press release, 18 June 2021. "
        "\\href{https://www.entsoe.eu/news/2021/06/18/successful-go-live-of-interim-coupling-reaching-the-sdac-enduring-phase/}{entsoe.eu}",
        "Eydeland, A.\\ \\& Wolyniec, K.\\ (2003). \\textit{Energy and Power Risk Management: New Developments in Modeling, Pricing, and Hedging}. Wiley. "
        "\\href{https://www.wiley.com/en-us/Energy+and+Power+Risk+Management-p-9780471104001}{wiley.com}",
        "Fama, E.\\,F.\\ \\& French, K.\\,R.\\ (1987). Commodity futures prices: Some evidence on forecast power, premiums, and the theory of storage. "
        "\\textit{Journal of Business}, 60(1), 55--73. \\href{https://doi.org/10.1086/296385}{doi:10.1086/296385}",
        "Hull, J.\\,C.\\ (2022). \\textit{Options, Futures, and Other Derivatives}, 11th ed. Pearson. "
        "\\href{https://www.pearson.com/en-us/subject-catalog/p/options-futures-and-other-derivatives/P200000005938}{pearson.com}",
        "IPCC (2006). \\textit{2006 IPCC Guidelines for National Greenhouse Gas Inventories}, Vol.\\ 2 Energy, ch.\\ 2, Table 2.2 (default emission factors). "
        "\\href{https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf}{ipcc-nggip.iges.or.jp}",
        "Johnson, L.\\,L.\\ (1960). The theory of hedging and speculation in commodity futures. \\textit{Review of Economic Studies}, 27(3), 139--151. "
        "\\href{https://doi.org/10.2307/2296076}{doi:10.2307/2296076}",
        "Kroner, K.\\,F.\\ \\& Sultan, J.\\ (1993). Time-varying distributions and dynamic hedging with foreign currency futures. "
        "\\textit{Journal of Financial and Quantitative Analysis}, 28(4), 535--551. \\href{https://doi.org/10.2307/2331164}{doi:10.2307/2331164}",
        "Longstaff, F.\\,A.\\ \\& Wang, A.\\,W.\\ (2004). Electricity forward prices: A high-frequency empirical analysis. \\textit{Journal of Finance}, "
        "59(4), 1877--1900. \\href{https://doi.org/10.1111/j.1540-6261.2004.00682.x}{doi:10.1111/j.1540-6261.2004.00682.x}",
        "Margrabe, W.\\ (1978). The value of an option to exchange one asset for another. \\textit{Journal of Finance}, 33(1), 177--186. "
        "\\href{https://doi.org/10.1111/j.1540-6261.1978.tb03397.x}{doi:10.1111/j.1540-6261.1978.tb03397.x}",
        "OUG 27/2022 privind măsurile aplicabile clienților finali din piața de energie electrică și gaze naturale (Monitorul Oficial nr.\\ 274, 22 martie 2022); "
        "OUG 153/2022 (MACEE). \\href{https://legislatie.just.ro}{legislatie.just.ro}",
        "Proșcanu, C., Proșcanu, M.\\ \\& Pele, D.\\,T.\\ (2025). The price elasticity of electricity demand in Romania. \\textit{Journal of Social and "
        "Economic Statistics}, 14(2), 131--141. \\href{https://doi.org/10.2478/jses-2025-0009}{doi:10.2478/jses-2025-0009}",
        "Redl, C., Haas, R., Huber, C.\\ \\& Böhm, B.\\ (2009). Price formation in electricity forward markets and the relevance of systematic "
        "forecast errors. \\textit{Energy Economics}, 31(3), 356--364. \\href{https://doi.org/10.1016/j.eneco.2008.12.001}{doi:10.1016/j.eneco.2008.12.001}",
        "Samuelson, P.\\,A.\\ (1965). Proof that properly anticipated prices fluctuate randomly. \\textit{Industrial Management Review}, 6(2), 41--49; "
        "reprinted in \\textit{World Scientific Handbook in Financial Economics} (2015), 25--38. \\href{https://doi.org/10.1142/9789814566926_0002}{doi:10.1142/9789814566926\\_0002}",
        "Schwartz, E.\\,S.\\ (1997). The stochastic behavior of commodity prices: Implications for valuation and hedging. \\textit{Journal of Finance}, "
        "52(3), 923--973. \\href{https://doi.org/10.1111/j.1540-6261.1997.tb02721.x}{doi:10.1111/j.1540-6261.1997.tb02721.x}",
        "Toma, F.-M., Dima, D.\\,M., Grecu, R., Pele, D.\\,T.\\ \\& Lessmann, S.\\ (2026). Energy Financial Risk Meter: Systemic risk in the EU energy "
        "sector. SSRN working paper. \\href{https://doi.org/10.2139/ssrn.6985301}{doi:10.2139/ssrn.6985301}",
        "Weron, R.\\ (2008). Market price of risk implied by Asian-style electricity options and futures. \\textit{Energy Economics}, 30(3), "
        "1098--1115. \\href{https://doi.org/10.1016/j.eneco.2007.05.004}{doi:10.1016/j.eneco.2007.05.004}",
    ]
    nref = len(REFS)
    cut = [(0, 8), (8, 16), (16, nref)]
    for part, (a_, b_) in enumerate(cut):
        D.frame(t("References", "Bibliografie") + f" ({part + 1}/3)", "\\begin{itemize}\\setlength{\\itemsep}{1pt}\\scriptsize\n" +
                "\n".join("\\item " + r for r in REFS[a_:b_]) + "\n\\end{itemize}", "scriptsize")

    # ------------------------------------------------------------------ appendix
    D.mark_main_end()
    D.parts.append("\\section*{" + t("Appendix", "Anexă") + "}\n")
    D.frame(t("Appendix A: the minimum-variance hedge ratio and its estimation", "Anexa A: raportul de acoperire cu varianță minimă și estimarea lui"), cols(
        "\\[ \\frac{\\partial}{\\partial h}\\Var(\\Delta S-h\\Delta F)=-2\\Cov(\\Delta S,\\Delta F)+2h\\Var(\\Delta F)=0 \\]"
        "\\[ \\Rightarrow\\ h^{*}=\\frac{\\Cov(\\Delta S,\\Delta F)}{\\Var(\\Delta F)} \\]\\[ \\Var(\\Delta S-h^{*}\\Delta F)=\\sigma_S^2(1-\\rho^2) \\]" + it(
            t("The second derivative $2\\Var(\\Delta F)>0$, so $h^{*}$ is a minimum.", "A doua derivată, $2\\Var(\\Delta F)>0$, deci $h^{*}$ este un minim."),
            t("$h^{*}$ is the OLS slope of $\\Delta S$ on $\\Delta F$; HAC variance (Newey--West, Bartlett kernel, 3 lags).",
              "$h^{*}$ este panta OLS a regresiei lui $\\Delta S$ pe $\\Delta F$; varianța HAC (Newey--West, nucleu Bartlett, 3 decalaje)."), sep="3pt"),
        it(t(("\\textbf{Moving-block bootstrap}", "draw blocks of @{hedge.block} consecutive months with replacement until $n$ months; recompute $h^{*}$; repeat @{hedge.B|,d} times",
              "95\\% interval = 2.5\\% and 97.5\\% percentiles; blocks keep the autocorrelation of the monthly changes"),
             ("\\textbf{Bootstrap pe blocuri mobile}", "se extrag cu întoarcere blocuri de cîte @{hedge.block} luni consecutive pînă la $n$ luni; se recalculează $h^{*}$; procedura se repetă de @{hedge.B|,d} de ori",
              "intervalul de 95\\% = percentilele de 2,5\\% și 97,5\\%; blocurile păstrează autocorelarea variațiilor lunare")),
           t(("\\textbf{Dynamic hedge ratios}", "$h_t^{*}=\\Cov_{t-1}/\\Var_{t-1}$ from a bivariate GARCH (Lecture 3)"),
             ("\\textbf{Rapoarte de acoperire dinamice}", "$h_t^{*}=\\Cov_{t-1}/\\Var_{t-1}$, dintr-un model GARCH bivariat (cursul 3)")), sep="3pt"), "0.54", "0.43"),
        "small", cite="(Johnson, 1960; Ederington, 1979; Kroner \\& Sultan, 1993)")

    D.frame(t("Appendix B: from a driftless forward to the Black-76 formula", "Anexa B: de la un preț forward fără tendință la formula Black-76"), cols(
        "\\[ \\frac{dF_t}{F_t}=\\sigma\\,dW_t\\ \\Rightarrow\\ \\ln F_T\\sim\\mathcal N\\big(\\ln F_0-\\tfrac12\\sigma^2T,\\ \\sigma^2T\\big) \\]"
        "\\[ C=e^{-rT}\\E\\big[(F_T-K)^+\\big]=e^{-rT}\\big[F_0\\Phi(d_1)-K\\Phi(d_2)\\big] \\]" + it(
            t("A forward costs nothing to enter, so under the pricing measure its drift is zero.",
              "Intrarea într-un contract forward nu costă nimic, deci în evaluarea neutră la risc tendința lui este zero."),
            t("$\\E[F_T\\mathbf 1_{F_T>K}]=F_0\\Phi(d_1)$ and $\\Pr(F_T>K)=\\Phi(d_2)$ (lognormal moments).",
              "$\\E[F_T\\mathbf 1_{F_T>K}]=F_0\\Phi(d_1)$ și $\\Pr(F_T>K)=\\Phi(d_2)$ (momentele repartiției lognormale)."), sep="3pt"),
        it(t(("\\textbf{Spread options}", "an option to exchange gas for power: Margrabe's formula with $\\sigma^2=\\sigma_P^2+\\sigma_G^2-2\\rho\\sigma_P\\sigma_G$",
              "with a strike (clean spark with fixed costs) Kirk's approximation is used in practice"),
             ("\\textbf{Opțiuni pe marjă}", "opțiunea de a schimba gazele în energie: formula Margrabe, cu $\\sigma^2=\\sigma_P^2+\\sigma_G^2-2\\rho\\sigma_P\\sigma_G$",
              "dacă există și un preț de exercitare (de exemplu, costurile variabile ale centralei), în practică se folosește aproximarea Kirk")),
           t(("\\textbf{Mean reversion}", "spot power reverts to its mean; Schwartz (1997) one-factor model gives forward volatilities that fall with maturity"),
             ("\\textbf{Revenirea la medie}", "prețul spot revine la medie; modelul cu un factor al lui Schwartz (1997) dă volatilități forward care scad cu scadența")), sep="3pt"), "0.54", "0.43"),
        "small", cite="(Black, 1976; Margrabe, 1978; Schwartz, 1997)")

    D.frame(t("Appendix C: conventions and conversion factors", "Anexa C: convenții și factori de conversie"), it(
        t(("\\textbf{Forward prices}", "one closing price per OPCOM session; quantity on the initiator side; lei converted with the ECB EUR/RON fixing of the auction day (last fixing on or before)",
           "standard periods only: month, quarter, half-year, calendar year; baseload unless stated"),
          ("\\textbf{Prețurile forward}", "un preț de închidere pentru fiecare sesiune OPCOM; volumul tranzacționat, înregistrat pe partea inițiatorului licitației; conversia din lei cu cursul BCE din ziua licitației (ultimul curs disponibil)",
           "numai perioade standard: lună, trimestru, semestru, an calendaristic; în bandă, dacă nu se precizează altfel")),
        t(("\\textbf{Realised spot}", "mean of the daily day-ahead base prices of the delivery period (CET days); computed only when every day is present"),
          ("\\textbf{Spotul realizat}", "media prețurilor zilnice în bandă de pe PZU din perioada de livrare (zile CET); se calculează numai dacă toate zilele sînt disponibile")),
        t(("\\textbf{Fuels and carbon}", "coal 6\\,000 kcal/kg = 6.978 MWh thermal per tonne; gas 0.202 and hard coal 0.341 t CO$_2$ per MWh thermal (IPCC 2006: 56.1 and 94.6 t/TJ)",
           "EUA = EEX auction monthly mean to @{spread.eua_switch|ym}, then SparkChange ETC (auction/ETC ratio close to 1 in 2021--2025)"),
          ("\\textbf{Combustibili și carbon}", "cărbune de 6\\,000 kcal/kg = 6,978 MWh termic pe tonă; gaze 0,202 și cărbune 0,341 t CO$_2$ pe MWh termic (IPCC 2006: 56,1 și 94,6 t/TJ)",
           "EUA = media lunară a licitațiilor EEX pînă în @{spread.eua_switch|ym}, apoi titlul SparkChange ETC (raportul licitație/ETC este apropiat de 1 în 2021--2025)")),
        t(("\\textbf{Hours}", "hour-equivalents: a 15-minute interval counts 0.25 h (since 1 October 2025)"),
          ("\\textbf{Ore}", "echivalent orar: un interval de 15 minute contează ca 0,25 h (din 1 octombrie 2025)")),
        sep="3pt"), "footnotesize", cite=t("(IPCC, 2006; OPCOM; ECB)", "(IPCC, 2006; OPCOM; BCE)"))
    return D


def main(langs):
    ok = True
    for lang in langs:
        name = "lecture5" if lang == "en" else "lecture5_ro"
        out = os.path.join(HERE, name + ".tex")
        D, tex, res, H = autofit(build, out, lang)
        print(f"[{lang}] frames: main {D.n_main} (incl. title and section outlines), total {D.n_frames}; quiz frames {D.quiz}; "
              f"pages {res['pages']}; errors {res['errors']}; overfull>1pt {len(res['overfull'])}")
        for kind, amt, title in res["where"]:
            print(f"     {kind} {amt:6.1f}pt  {title}")
        small = {k: v for k, v in D.used_h.items() if v < 0.40}
        print(f"[{lang}] figure heights (fraction of text height) below 0.40:", small)
        defined = set(ABBR) - ({"UE", "BCE"} if lang == "en" else {"EU", "ECB"})
        print(f"[{lang}] acronyms missing from Abbreviations:", acronym_audit(tex, defined, IGNORE | ({"EU", "ECB"} if lang == "ro" else set())))
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
