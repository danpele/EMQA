r"""
build_L4.py -- Lecture 4 "Risk Management for Energy Prices" (EMQA), English and Romanian from one source
=========================================================================================================
Writes lectures/L4/lecture4.tex (EN) and lectures/L4/lecture4_ro.tex (RO) from the bilingual slide text in this file
and the numbers in L4_numbers.json (produced by analysis_L4.py), compiles both with pdflatex and checks: 0 LaTeX errors;
no overfull box > 1 pt (nothing masked); every acronym in the Abbreviations frames and spelled out at first use;
contact sheets for the visual check.

Run (from anywhere):
    python3 lectures/L4/analysis_L4.py
    python3 lectures/L4/build_L4.py            # both languages;  add "en" or "ro" for one

No computed number is typed by hand (results are @{key} placeholders). Hand-typed numbers are definitions (confidence
levels, 24 h, 100 MW, 2,400 MWh, 2.326, 250 days, window lengths, the 250,000 EUR budget assumption, 1 lot = 1,000 bbl),
tabulated thresholds (Basel zones, chi-square 3.84) and institutional facts with their source (EMIR RTS 153/2013,
ECB Financial Stability Review Nov 2022, Delegated Regulation 2022/2311, OPCOM guarantee procedure) or paper results.
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
    "APC": ("anti-procyclicality tools of a CCP", "instrumentele anticiclice ale unei CCP (anti-procyclicality)"),
    "AUC": ("area under the curve (0.5 = no skill, 1 = perfect)", "aria de sub curbă (0,5 = fără putere de discriminare, 1 = perfect)"),
    "BCBS": ("Basel Committee on Banking Supervision", "Comitetul de la Basel pentru Supraveghere Bancară"),
    "BCE": (None, "Banca Centrală Europeană"),
    "CARDI": ("carbon risk dynamic indicator", "indicatorul dinamic al riscului de carbon"),
    "CCP": ("central counterparty (clearing house)", "contraparte centrală (casă de compensare)"),
    "CEE": ("Central and Eastern Europe", "Europa Centrală și de Est"),
    "CET": ("Central European Time", "ora Europei Centrale"),
    "CFaR": ("cash-flow-at-risk", "fluxul de numerar la risc (cash-flow-at-risk)"),
    "CISS": ("Composite Indicator of Systemic Stress (ECB)", "indicatorul compozit de stres sistemic (BCE)"),
    "DE-LU": ("Germany--Luxembourg bidding zone", "zona de ofertare Germania--Luxemburg"),
    "ECB": ("European Central Bank", None),
    "EFRM": ("Energy Financial Risk Meter", "indicatorul de risc financiar al sectorului energetic (Energy Financial Risk Meter)"),
    "EMIR": ("European Market Infrastructure Regulation (EU) No 648/2012", "Regulamentul (UE) nr. 648/2012 privind infrastructura pieței europene (EMIR)"),
    "ENTSO-E": ("European Network of Transmission System Operators for Electricity",
                "Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică"),
    "EPEX": ("EPEX SPOT power exchange", "bursa europeană de energie EPEX SPOT"),
    "ES": ("expected shortfall", "deficitul așteptat (expected shortfall)"),
    "EU": ("European Union", None),
    "UE": (None, "Uniunea Europeană"),
    "EVT": ("extreme value theory", "teoria valorilor extreme"),
    "FHS": ("filtered historical simulation", "simularea istorică filtrată"),
    "FRTB": ("Fundamental Review of the Trading Book (Basel market-risk rules)", "revizuirea fundamentală a portofoliului de tranzacționare (regulile Basel pentru riscul de piață)"),
    "FRM": ("Financial Risk Meter", "indicatorul de risc financiar (Financial Risk Meter)"),
    "GARCH": ("generalised autoregressive conditional heteroskedasticity", "model autoregresiv generalizat cu heteroscedasticitate condiționată"),
    "GPD": ("generalised Pareto distribution", "repartiția Pareto generalizată"),
    "HS": ("historical simulation", "simularea istorică"),
    "ICE": ("Intercontinental Exchange (ICE Futures Europe)", "bursa Intercontinental Exchange (ICE Futures Europe)"),
    "IM": ("initial margin", "marja inițială"),
    "ISE": ("Fraunhofer Institute for Solar Energy Systems", "Institutul Fraunhofer pentru Sisteme de Energie Solară"),
    "LASSO": ("least absolute shrinkage and selection operator", "operatorul de contracție și selecție în normă absolută"),
    "LR": ("likelihood ratio", "raportul de verosimilitate"),
    "MLE": ("maximum likelihood estimation", "estimarea prin metoda verosimilității maxime"),
    "OPCOM": ("Romanian electricity and gas market operator", "operatorul pieței de energie electrică și de gaze naturale din România"),
    "POT": ("peaks over threshold", "depășirile unui prag (peaks over threshold)"),
    "PZU": ("Piața pentru Ziua Următoare (day-ahead market)", "piața pentru ziua următoare"),
    "QR": ("quantile regression", "regresia cuantilică"),
    "QRA": ("quantile regression averaging (Lecture 2)", "medierea prin regresie cuantilică (cursul 2)"),
    "RO": ("Romania (bidding zone)", "România (zonă de ofertare)"),
    "RTS": ("regulatory technical standards", "standarde tehnice de reglementare"),
    "TTF": ("Title Transfer Facility (Dutch gas hub)", "Title Transfer Facility (hub olandez de gaze)"),
    "VaR": ("value-at-risk", "valoarea la risc (value-at-risk)"),
    "VM": ("variation margin", "marja de variație"),
    "EUR": ("euro", "euro"), "MW": ("megawatt", "megawatt"), "MWh": ("megawatt-hour", "megawatt-oră"),
    "USD": ("United States dollar", "dolarul american"),
}
UNITS = {"EUR", "MW", "MWh", "USD"}
# journal codes and tickers inside citations only; everything else must be in the Abbreviations list and spelled out
IGNORE = {"AI", "ReP", "OMV", "RSER", "EMQA", "IJF", "JBF", "JEF", "JASA", "IER", "SSRN", "ECECSR", "BZ", "SPOT", "CO", "II", "III", "IEEE", "AOS", "EJ", "ASE", "IPE", "AIDA"}


def build(lang, H=None):
    V = Numbers(os.path.join(HERE, "L4_numbers.json"), lang)
    N = V.N
    D = Deck(4, "Risk Management for Energy Prices" if lang == "en" else "Managementul riscului de preț pe piețele de energie", V, lang, heights=H)
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

    def dec(x):
        """Hand-typed definitional decimal with the right separator."""
        return x.replace(".", "{,}") if ro else x

    BT = N["bt"]
    AIDA = "https://github.com/danpele/EMQA/blob/main/resources/aida2026/"
    TALK_TOMA, TALK_PELE = AIDA + "toma_energy_financial_risk_meter.pdf", AIDA + "pele_conformal_tail_risk.pdf"
    TALK_WANG, DOI_WANG = AIDA + "wang_carbon_risk_dynamics.pdf", "https://doi.org/10.2139/ssrn.5757742"
    MN = {"hs": "HS", "normal": t("Normal", "Normală"), "t": "Student-$t$", "fhs": "FHS", "evt": "EVT"}
    METHODS = ["hs", "normal", "t", "fhs", "evt"]
    BTP = t("backtest @{data.t0|date} -- @{data.end|date}", "testare retrospectivă @{data.t0|date} -- @{data.end|date}")

    # ------------------------------------------------------------------ front matter
    D.parts.append("% END-FRONT-MATTER\n")
    D.frame(t("Learning objectives", "Obiectivele cursului"), it(
        t(("Measure the price risk of an energy position", "value-at-risk (VaR) and expected shortfall (ES) as quantiles of the loss distribution",
           "why the normal curve understates crisis days (promised in Lecture 1)"),
          ("Măsurarea riscului de preț al unei poziții pe piața de energie", "valoarea la risc (VaR) și deficitul așteptat (ES), definite cu ajutorul cuantilelor repartiției pierderilor",
           "de ce repartiția normală subestimează zilele de criză (anunțat în cursul 1)")),
        t(("Estimate VaR and ES in four ways on Romanian prices", "historical simulation (HS), normal and Student-$t$, filtered historical simulation (FHS), extreme value theory (EVT)"),
          ("Estimarea VaR și ES prin patru metode, pe prețurile din România", "simularea istorică (HS), repartițiile normală și Student-$t$, simularea istorică filtrată (FHS), teoria valorilor extreme (EVT)")),
        t(("Check a risk model after the fact (backtesting)", "Kupiec and Christoffersen tests, the Basel traffic light, a test for ES"),
          ("Verificarea unui model de risc pe datele care au urmat (testare retrospectivă)", "testele Kupiec și Christoffersen, semaforul Basel și un test pentru ES")),
        t(("Turn quantiles into decisions", "position limits, exchange margins and the day-ahead guarantee, for a supplier, a producer and a trader"),
          ("Transformarea cuantilelor în decizii", "limite de poziție, marje la bursă și garanția pentru piața pentru ziua următoare, pentru un furnizor, un producător și un trader")),
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

    D.frame(t("Real data only: the prices and positions we measure", "Lucrăm numai cu date reale: prețurile și pozițiile analizate"), table(
        "@{}p{0.40\\textwidth}p{0.11\\textwidth}p{0.44\\textwidth}@{}",
        [t("Series", "Seria"), t("Frequency", "Frecvența"), t("Source", "Sursa")],
        [[t("Day-ahead base price of Romania (RO), Piața pentru Ziua Următoare (PZU), and of the Germany--Luxembourg zone (DE-LU)",
            "Prețul de bază pe piața pentru ziua următoare (PZU) din România (RO) și din zona Germania--Luxemburg (DE-LU)"),
          t("daily, hourly", "zilnică, orară"),
          t("the Romanian market operator (OPCOM) and the European Power Exchange (EPEX SPOT), via energy-charts.info (Fraunhofer ISE) and the European "
            "Network of Transmission System Operators for Electricity (ENTSO-E)",
            "operatorul pieței de energie electrică și de gaze naturale din România (OPCOM) și bursa europeană de energie (EPEX SPOT), prin energy-charts.info "
            "(Fraunhofer ISE) și Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică (ENTSO-E)")],
         [t("Romanian load (shape of a supplier's portfolio)", "Consumul național al României (profilul portofoliului unui furnizor)"), t("hourly", "orară"),
          t("ENTSO-E (Transelectrica data), via energy-charts.info", "ENTSO-E (date Transelectrica), prin energy-charts.info")],
         [t("Brent crude oil futures, front month (a margined contract)", "Contractul futures pe țițeiul Brent cu scadența cea mai apropiată (un contract cu marjă)"),
          t("daily", "zilnică"), t("Yahoo Finance (BZ=F)", "Yahoo Finance (BZ=F)")],
         [t("Dutch gas hub price, Title Transfer Facility (TTF)", "Prețul gazelor la hubul olandez Title Transfer Facility (TTF)"), t("monthly", "lunară"),
          t("World Bank, Pink Sheet", "Banca Mondială, Pink Sheet")]],
        size="scriptsize", stretch="0.95") + "\n\\vspace{0.5mm}\n" + it(
        t(("\\textbf{Period}", "@{data.start|date} -- @{data.end|date} (last complete month); downloaded @{cutoff.download|date}; daily price = mean of the delivery day in Central European Time (CET)",
           "@{data.n_missing_ro} missing days of the Romanian price stay missing; changes next to them are not computed"),
          ("\\textbf{Perioada}", "@{data.start|date} -- @{data.end|date} (ultima lună completă); date descărcate la @{cutoff.download|date}; prețul zilnic = media prețurilor zilei de livrare, după ora Europei Centrale (CET)",
           "cele @{data.n_missing_ro} zile lipsă din seria prețului din România rămîn lipsă; variațiile vecine cu ele nu se calculează")),
        t(("\\textbf{Backtest}", "every day from @{data.t0|date} to @{data.end|date} (@{data.n_test_valid_ro|,d} valid days), each forecast made with data up to the previous day"),
          ("\\textbf{Testarea retrospectivă}", "fiecare zi din intervalul @{data.t0|date} -- @{data.end|date} (@{data.n_test_valid_ro|,d} " + de("data.n_test_valid_ro") +
           "zile valide); fiecare prognoză folosește numai datele pînă în ziua precedentă")),
        sep="1pt") + D.bottom(None, NB + " \\S1"), "footnotesize")

    # ------------------------------------------------------------------ 1 price risk, VaR and ES
    D.section(t("Price risk: losses, quantiles, VaR and ES", "Riscul de preț: pierderi, cuantile, VaR și ES"))
    D.chart(t("Daily price changes before and after 2021",
              "Variațiile zilnice ale prețului înainte și după 2021"), "price_changes", [
        t(("$X_t=P_t-P_{t-1}$ = change of the daily base price, EUR/MWh", "prices can be negative, so we use changes, not log returns",
           "largest rise @{dist.RO.max|.2f} (@{dist.RO.max_date|date}), largest fall @{dist.RO.min|.2f} EUR/MWh (@{dist.RO.min_date|date})"),
          ("$X_t=P_t-P_{t-1}$ = variația zilnică a prețului de bază, EUR/MWh", "prețul poate fi negativ: folosim variații, nu randamente logaritmice",
           "creșterea maximă: @{dist.RO.max|.2f} (@{dist.RO.max_date|date}); scăderea maximă: @{dist.RO.min|.2f} EUR/MWh (@{dist.RO.min_date|date})"))],
        height="0.56\\textheight",
        job=t("a supplier that buys 100 MW flat on the PZU and budgets at yesterday's price loses 2,400 EUR for every EUR/MWh of rise.",
              "un furnizor care cumpără 100 MW în bandă pe PZU, la bugetul de ieri, pierde 2.400 EUR la fiecare creștere de 1 EUR/MWh."),
        tryit=NB + " \\S1", cite=t("(OPCOM; EPEX SPOT; own computation)", "(OPCOM; EPEX SPOT; calcule proprii)"))

    D.concept(t("Value-at-risk is a quantile of tomorrow's loss", "Valoarea la risc este o cuantilă a pierderii de mîine"),
              t("VaR is the loss that is exceeded only on a small, chosen share of days, e.g.\\ one day in a hundred.",
                "VaR este pierderea depășită doar într-o proporție mică de zile, aleasă dinainte, de exemplu o zi din o sută."),
              "\\[ \\underbrace{L_{t}=Q\\cdot 24\\cdot X_{t}}_{\\text{" + t("loss, EUR", "pierderea, EUR") + "}},\\qquad "
              "\\underbrace{\\text{VaR}_{\\alpha,t}=\\min\\{\\ell:\\ \\Pr(L_t\\le \\ell\\mid\\mathcal F_{t-1})\\ge\\alpha\\}}_{\\text{" +
              t("the } \\alpha\\text{-quantile of the loss", "cuantila de ordin } \\alpha \\text{ a pierderii") + "}} \\]" +
              "\\where{" + t("$Q$ = position in MW (100 MW flat: $Q\\cdot 24$ = 2,400 MWh per day); $X_t$ = price change, EUR/MWh; "
                             "$\\alpha$ = confidence level, 0.95 or 0.99; $\\mathcal F_{t-1}$ = information up to day $t-1$ (prices known at 12:00 CET, gate closure).",
                             "$Q$ = poziția, în MW (100 MW în bandă: $Q\\cdot 24$ = 2.400 MWh pe zi); $X_t$ = variația prețului, EUR/MWh; "
                             "$\\alpha$ = nivelul de încredere, 0{,}95 sau 0{,}99; $\\mathcal F_{t-1}$ = informația disponibilă pînă în ziua $t-1$ (prețurile cunoscute la ora 12:00 CET, la închiderea licitației).") + "}",
              it((t("\\textbf{On our data}, last 365 days", "\\textbf{Pe datele din România}, ultimele 365 de zile"),
                  t("99\\% quantile of $X_t$: @{lastyear.var99|.2f} EUR/MWh, i.e.\\ VaR$_{0.99}$ = @{lastyear.var99_eur|,.0f} EUR for 100 MW",
                    "cuantila de 99\\% a lui $X_t$: @{lastyear.var99|.2f} EUR/MWh; pentru 100 MW, VaR$_{0{,}99}$ = @{lastyear.var99_eur|,.0f} EUR"),
                  t("95\\% quantile: @{lastyear.var95|.2f} EUR/MWh", "cuantila de 95\\%: @{lastyear.var95|.2f} EUR/MWh")),
                 (t("\\textbf{What VaR does not say}", "\\textbf{Ce nu spune VaR}"),
                  t("how large the loss is on the worst 1\\% of days", "cît de mare este pierderea în cele mai proaste 1\\% dintre zile"),
                  t("for that we need the ES, next slide", "pentru aceasta avem nevoie de ES (diapozitivul următor)")), sep="2pt"),
              t("the desk reports the 99\\% VaR every morning, before bidding at 12:00 CET.",
                "biroul de tranzacționare raportează zilnic VaR de 99\\%, dimineața, înainte de licitația de la ora 12:00 CET."),
              tryit=NB + " \\S2", cite="(Jorion, 2007; McNeil, Frey \\& Embrechts, 2015)", wl="0.55", wr="0.42")

    D.concept(t("Expected shortfall: the average loss beyond VaR", "Deficitul așteptat este pierderea medie dincolo de VaR"),
              t("When a bad day comes, how large is the loss on average?",
                "Cînd vine o zi proastă, cît de mare este, în medie, pierderea?"),
              "\\[ \\text{ES}_{\\alpha,t}=\\E\\big[L_t\\mid L_t\\ge \\text{VaR}_{\\alpha,t}\\big]=\\frac{1}{1-\\alpha}\\int_{\\alpha}^{1}\\text{VaR}_{u,t}\\,du \\]"
              "\\[ \\underbrace{\\text{ES}(L_1+L_2)\\le\\text{ES}(L_1)+\\text{ES}(L_2)}_{\\text{" + t("subadditivity: diversification never adds risk", "subaditivitate: diversificarea nu adaugă risc") + "}} \\]" +
              "\\where{" + t("ES is coherent, VaR may break subadditivity; "
                             "the Fundamental Review of the Trading Book (FRTB) uses ES at 97.5\\% instead of VaR at 99\\%.",
                             "ES este o măsură coerentă a riscului, VaR poate încălca subaditivitatea; "
                             "revizuirea fundamentală a portofoliului de tranzacționare (FRTB) folosește ES de 97{,}5\\% în locul VaR de 99\\%.") + "}",
              it((t("\\textbf{On our data}, last 365 days, EUR/MWh", "\\textbf{Pe datele din România}, ultimele 365 de zile, EUR/MWh"),
                  t("VaR$_{0.975}$ @{lastyear.var975|.2f}, ES$_{0.975}$ @{lastyear.es975|.2f} (mean of the @{lastyear.n_ge_var975} worst days)",
                    "VaR$_{0{,}975}$ = @{lastyear.var975|.2f}; ES$_{0{,}975}$ = @{lastyear.es975|.2f} (media celor mai proaste @{lastyear.n_ge_var975} zile)")),
                 (t("\\textbf{Romania + Germany--Luxembourg}, 100 MW in each", "\\textbf{România + Germania--Luxemburg}, cîte 100 MW în fiecare zonă"),
                  t("99\\% VaR: @{subadd.var_ro|.2f} + @{subadd.var_de|.2f} separately, @{subadd.var_sum|.2f} together", "VaR de 99\\%: @{subadd.var_ro|.2f} + @{subadd.var_de|.2f} separat, @{subadd.var_sum|.2f} împreună"),
                  t("correlation @{subadd.corr|.2f}: the joint risk is smaller", "corelația @{subadd.corr|.2f}: riscul total este mai mic")), sep="2pt"),
              t("size the cash buffer with ES, not with VaR.",
                "dimensionați rezerva de numerar cu ES, nu cu VaR."),
              tryit=NB + " \\S2", cite="(Artzner et al., 1999, Math.\\ Finance; Acerbi \\& Tasche, 2002, JBF; BCBS, 2019)", wl="0.53", wr="0.44")

    D.chart(t("Large price rises are far more frequent than the normal curve allows",
              "Creșterile mari de preț sînt mult mai frecvente decît prevede repartiția normală"), "tails", [
        t(("Excess kurtosis @{dist.RO.exkurt|.1f} in Romania, @{dist.DE_LU.exkurt|.1f} in Germany--Luxembourg (0 for a normal curve)",
           "rises above 3 standard deviations: @{dist.RO.n_3sd_up} days observed vs @{dist.RO.exp_3sd|.1f} expected under normality",
           "the largest rise is @{dist.RO.max_z|.1f} standard deviations: under normality, once in more than $10^{@{dist.RO.max_logyears}}$ years"),
          ("Excesul de aplatizare (kurtosis): @{dist.RO.exkurt|.1f} în România și @{dist.DE_LU.exkurt|.1f} în Germania--Luxemburg (0 pentru repartiția normală)",
           "creșteri de peste 3 abateri standard: @{dist.RO.n_3sd_up} zile observate, față de @{dist.RO.exp_3sd|.1f} așteptate în ipoteza normalității",
           "cea mai mare creștere are @{dist.RO.max_z|.1f} abateri standard: în ipoteza normalității, ar apărea o dată la peste $10^{@{dist.RO.max_logyears}}$ de ani"))],
        height="0.52\\textheight",
        job=t("a limit built on the normal curve understates how often a crisis day comes (Lecture 1).",
              "o limită calculată cu repartiția normală subestimează frecvența zilelor de criză (cursul 1)."),
        tryit=NB + " \\S2", cite=t("(own computation, @{data.start|date} -- @{data.end|date})", "(calcule proprii, @{data.start|date} -- @{data.end|date})"))

    D.concept(t("A normal-curve limit set in 2020 was breached @{normlim.ratio_crisis|.0f} times more often than planned in 2021--2022",
                "O limită calculată în 2020 cu repartiția normală a fost depășită în 2021--2022 de @{normlim.ratio_crisis|.0f} ori mai des decît se prevedea"),
              t("A static limit assumes that tomorrow's risk looks like the past; in a crisis it does not.",
                "O limită fixă presupune că riscul de mîine seamănă cu cel din trecut; într-o criză, această ipoteză nu se verifică."),
              "\\[ \\underbrace{\\ell_{0.99}=\\hat\\mu+z_{0.99}\\,\\hat\\sigma}_{\\text{" + t("normal 99\\% limit", "limita normală de 99\\%") + "}},\\qquad z_{0.99}=" + dec("2.326") + " \\]" +
              "\\where{" + t("$\\hat\\mu$, $\\hat\\sigma$ = mean and standard deviation of $X_t$ in 2015--2020; $z_{0.99}$ = 99\\% quantile of the standard normal distribution; "
                             "a correct limit is exceeded on 1\\% of days.",
                             "$\\hat\\mu$, $\\hat\\sigma$ = media și abaterea standard a lui $X_t$ în 2015--2020; $z_{0{,}99}$ = cuantila de 99\\% a repartiției normale standard; "
                             "o limită corectă este depășită în 1\\% din zile.").replace("z_{0.99}", "z_{0{,}99}" if ro else "z_{0.99}") + "}",
              it((t("\\textbf{The limit}, from @{normlim.n_pre|,d} days of 2015--2020", "\\textbf{Limita}, estimată pe @{normlim.n_pre|,d} " + de("normlim.n_pre") + "zile din 2015--2020"),
                  t("$\\hat\\sigma$ = @{normlim.s|.2f}, limit = @{normlim.lim99|.2f} EUR/MWh", "$\\hat\\sigma$ = @{normlim.s|.2f}; limita = @{normlim.lim99|.2f} EUR/MWh"),
                  t("already in 2015--2020: @{normlim.n_pre_exc} breaches vs @{normlim.exp_pre|.1f} expected", "chiar în 2015--2020: @{normlim.n_pre_exc} depășiri, față de @{normlim.exp_pre|.1f} așteptate")),
                 (t("\\textbf{Breaches afterwards}", "\\textbf{Depășiri ulterioare}"),
                  t("2021--2022: @{normlim.exc_crisis} vs @{normlim.exp_crisis|.1f} expected", "2021--2022: @{normlim.exc_crisis}, față de @{normlim.exp_crisis|.1f} așteptate"),
                  t("2023--2026: @{normlim.exc_after} vs @{normlim.exp_after|.1f} expected (@{normlim.ratio_after|.0f} times more)",
                    "2023--2026: @{normlim.exc_after}, față de @{normlim.exp_after|.1f} așteptate (de @{normlim.ratio_after|.0f} ori mai multe)")), sep="2pt"),
              t("a limit must move with volatility; the next section shows four ways to make it move.",
                "o limită trebuie să urmeze volatilitatea; secțiunea următoare prezintă patru moduri de a o actualiza."),
              tryit=NB + " \\S2", cite=t("(own computation; Lecture 1)", "(calcule proprii; cursul 1)"), wl="0.50", wr="0.47")

    # ------------------------------------------------------------------ 2 estimation
    D.section(t("Estimating VaR and ES: four methods", "Estimarea VaR și ES: patru metode"))
    D.subsection(t("Historical simulation and parametric models", "Simularea istorică și modelele parametrice"))
    D.concept(t("Historical simulation with a one-year window", "Simularea istorică pe o fereastră de un an"),
              t("Sort the last 365 daily changes; the 4th largest is the 99\\% VaR.",
                "Ordonăm ultimele 365 de variații zilnice; a patra cea mai mare este VaR de 99\\%."),
              "\\[ \\widehat{\\text{VaR}}^{\\text{HS}}_{\\alpha,t}=\\hat q_{\\alpha}\\big(X_{t-W},\\dots,X_{t-1}\\big) \\]"
              "\\[ \\widehat{\\text{ES}}^{\\text{HS}}_{\\alpha,t}=\\text{" + t("mean of", "media valorilor") + " }\\{X_s\\ge\\widehat{\\text{VaR}}^{\\text{HS}}_{\\alpha,t}\\} \\]" +
              "\\where{" + t("$W$ = 365 days (the window); $\\hat q_\\alpha$ = empirical quantile; no distribution is assumed.",
                             "$W$ = 365 de zile (fereastra); $\\hat q_\\alpha$ = cuantila empirică; nu se presupune nicio repartiție.") + "}",
              it((t("\\textbf{On our data}, October 2026", "\\textbf{Pe datele din România}, octombrie 2026"),
                  t("VaR$_{0.99}$ @{last.hs.var99|.2f}, ES$_{0.975}$ @{last.hs.es975|.2f} EUR/MWh", "VaR$_{0{,}99}$ = @{last.hs.var99|.2f}; ES$_{0{,}975}$ = @{last.hs.es975|.2f} EUR/MWh"),
                  t("2017--2026: exceeded on @{bt.RO.hs.a99.rate|.2f}\\% of days, not 1\\%",
                    "2017--2026: depășită în @{bt.RO.hs.a99.rate|.2f}\\% din zile, nu în 1\\%")),
                 (t("\\textbf{Weakness}", "\\textbf{Punctul slab}"),
                  t("a new regime needs months to fill the window", "un regim nou are nevoie de luni de zile pentru a umple fereastra"),
                  t("a crisis day counts for 365 days, then drops out at once", "o zi de criză contează 365 de zile, apoi dispare brusc")), sep="2pt"),
              t("HS is the default in many energy companies, and it lags the market.",
                "HS este metoda implicită în multe companii energetice și reacționează cu întîrziere."),
              tryit=NB + " \\S3", cite="(Jorion, 2007; Christoffersen, 2012)", wl="0.50", wr="0.47")

    D.concept(t("Normal and Student-$t$: two parameters or three", "Repartițiile normală și Student-$t$: doi sau trei parametri"),
              t("Fit a curve to the last year of changes and read its quantile; the Student-$t$ curve has fatter tails.",
                "Ajustăm o curbă pe variațiile din ultimul an și citim cuantila ei; curba Student-$t$ are cozi mai groase."),
              "\\[ \\text{VaR}^{N}_{\\alpha}=\\mu+\\sigma z_\\alpha,\\qquad \\text{ES}^{N}_{\\alpha}=\\mu+\\sigma\\frac{\\varphi(z_\\alpha)}{1-\\alpha} \\]"
              "\\[ \\text{VaR}^{t}_{\\alpha}=m+s\\,t_{\\nu,\\alpha},\\qquad \\text{ES}^{t}_{\\alpha}=m+s\\,\\frac{g_\\nu(t_{\\nu,\\alpha})}{1-\\alpha}\\cdot\\frac{\\nu+t_{\\nu,\\alpha}^2}{\\nu-1} \\]" +
              "\\where{" + t("$\\mu,\\sigma$ = mean, standard deviation; $z_\\alpha$, $\\varphi$ = normal quantile, density; "
                             "$m,s,\\nu$ = location, scale, degrees of freedom, by maximum likelihood estimation (MLE); $t_{\\nu,\\alpha}$, $g_\\nu$ = Student-$t$ quantile, density (Appendix A).",
                             "$\\mu,\\sigma$ = media, abaterea standard; $z_\\alpha$, $\\varphi$ = cuantila și densitatea normală standard; "
                             "$m,s,\\nu$ = locația, scala, gradele de libertate, estimate prin metoda verosimilității maxime (MLE); $t_{\\nu,\\alpha}$, $g_\\nu$ = cuantila și densitatea Student-$t$ (Anexa A).") + "}",
              it((t("\\textbf{On our data}, October 2026, EUR/MWh", "\\textbf{Pe datele din România}, octombrie 2026, EUR/MWh"),
                  t("normal: VaR$_{0.99}$ @{last.normal.var99|.2f}, ES$_{0.975}$ @{last.normal.es975|.2f}", "normală: VaR$_{0{,}99}$ = @{last.normal.var99|.2f}; ES$_{0{,}975}$ = @{last.normal.es975|.2f}"),
                  t("Student-$t$: VaR$_{0.99}$ @{last.t.var99|.2f}, ES$_{0.975}$ @{last.t.es975|.2f}", "Student-$t$: VaR$_{0{,}99}$ = @{last.t.var99|.2f}; ES$_{0{,}975}$ = @{last.t.es975|.2f}")),
                 (t("\\textbf{Backtest}, days above the 99\\% VaR", "\\textbf{Testarea retrospectivă}, zile peste VaR de 99\\%"),
                  t("normal @{bt.RO.normal.a99.rate|.2f}\\%, Student-$t$ @{bt.RO.t.a99.rate|.2f}\\% (target 1\\%)", "normală: @{bt.RO.normal.a99.rate|.2f}\\%; Student-$t$: @{bt.RO.t.a99.rate|.2f}\\% (ținta: 1\\%)"),
                  t("at 95\\% the $t$ curve is too narrow: @{bt.RO.t.a95.rate|.2f}\\%", "la 95\\%, curba $t$ este prea îngustă: @{bt.RO.t.a95.rate|.2f}\\%")), sep="2pt"),
              t("the normal VaR is the easiest to explain and the most dangerous to trust.",
                "VaR normală este cel mai ușor de explicat și cel mai periculos de folosit fără verificare."),
              tryit=NB + " \\S3", cite="(McNeil, Frey \\& Embrechts, 2015)", wl="0.55", wr="0.42")

    D.subsection(t("Filtered historical simulation and extreme values", "Simularea istorică filtrată și valorile extreme"))
    D.concept(t("Filtered historical simulation: past shocks rescaled to current volatility", "Simularea istorică filtrată: șocurile trecute, rescalate la volatilitatea curentă"),
              t("Divide past changes by their volatility, then rescale the shocks by today's volatility.",
                "Împărțim variațiile trecute la volatilitatea lor, apoi înmulțim șocurile cu volatilitatea de azi."),
              "\\[ e_t=X_t-\\mu_{d(t)},\\quad \\sigma_t^2=\\omega+a\\,e_{t-1}^2+b\\,\\sigma_{t-1}^2,\\quad z_t=e_t/\\sigma_t \\]"
              "\\[ \\text{VaR}^{\\text{FHS}}_{\\alpha,t}=\\mu_{d(t)}+\\sigma_t\\,\\hat q_\\alpha(z) \\]" +
              "\\where{" + t("$\\mu_{d(t)}$ = mean change of that weekday (prices fall at weekends); "
                             "$\\sigma_t$ = generalised autoregressive conditional heteroskedasticity (GARCH) volatility, Lecture 3, refitted every 21 days on 730 days; "
                             "ES: $\\sigma_t$ times the mean of $z$ above $\\hat q_\\alpha(z)$.",
                             "$\\mu_{d(t)}$ = variația medie a zilei din săptămînă (prețul scade la sfîrșit de săptămînă); "
                             "$\\sigma_t$ = volatilitatea din modelul autoregresiv generalizat cu heteroscedasticitate condiționată (GARCH), cursul 3, reestimat la 21 de zile pe 730 de zile; "
                             "ES: $\\sigma_t$ înmulțit cu media valorilor $z$ peste $\\hat q_\\alpha(z)$.") + "}",
              it((t("\\textbf{On our data}, GARCH(1,1)", "\\textbf{Pe datele din România}, GARCH(1,1)"),
                  t("$\\sigma_t$ from @{garch.sig_min|.2f} (@{garch.sig_min_date|date}) to @{garch.sig_max|.2f} EUR/MWh (@{garch.sig_max_date|date})",
                    "$\\sigma_t$ între @{garch.sig_min|.2f} (@{garch.sig_min_date|date}) și @{garch.sig_max|.2f} EUR/MWh (@{garch.sig_max_date|date})"),
                  t("October 2026: VaR$_{0.99}$ @{last.fhs.var99|.2f} EUR/MWh", "octombrie 2026: VaR$_{0{,}99}$ = @{last.fhs.var99|.2f} EUR/MWh")),
                 (t("\\textbf{Backtest}", "\\textbf{Testarea retrospectivă}"),
                  t("99\\%: @{bt.RO.fhs.a99.rate|.2f}\\% of days", "99\\%: @{bt.RO.fhs.a99.rate|.2f}\\% din zile"),
                  t("95\\%: @{bt.RO.fhs.a95.rate|.2f}\\%, Kupiec $p$ = " + pval("bt.RO.fhs.a95.p_uc"), "95\\%: @{bt.RO.fhs.a95.rate|.2f}\\%; Kupiec: $p$ = " + pval("bt.RO.fhs.a95.p_uc"))), sep="2pt"),
              t("FHS raises the limit within days of a volatility jump; HS needs months.",
                "FHS ridică limita la cîteva zile după un salt al volatilității; HS are nevoie de luni."),
              tryit=NB + " \\S3", cite="(Barone-Adesi, Giannopoulos \\& Vosper, 1999; Bollerslev, 1986)", wl="0.53", wr="0.44")

    D.concept(t("Extreme value theory: model only the tail, with a generalised Pareto curve",
                "Teoria valorilor extreme: modelăm numai coada, cu o curbă Pareto generalizată"),
              t("Above a high threshold, the excesses of almost any distribution follow the same two-parameter curve.",
                "Peste un prag ridicat, excesele aproape oricărei repartiții urmează aceeași curbă cu doi parametri."),
              "\\[ \\Pr(Z-u\\le y\\mid Z>u)\\approx 1-\\Big(1+\\frac{\\xi y}{\\beta}\\Big)^{-1/\\xi} \\]"
              "\\[ \\text{VaR}_\\alpha=u+\\frac{\\beta}{\\xi}\\Big[\\Big(\\frac{n}{N_u}(1-\\alpha)\\Big)^{-\\xi}-1\\Big],\\quad \\text{ES}_\\alpha=\\frac{\\text{VaR}_\\alpha+\\beta-\\xi u}{1-\\xi} \\]" +
              "\\where{" + t("peaks over threshold (POT): $u$ = 90\\% quantile of $z$, exceeded by $N_u$ of $n$ residuals; "
                             "generalised Pareto distribution (GPD): shape $\\xi$ (tail heaviness), scale $\\beta$, by MLE; then multiplied by $\\sigma_t$ as in FHS (Appendix B).",
                             "metoda depășirilor unui prag (POT): $u$ = cuantila de 90\\% a lui $z$, depășită de $N_u$ din cele $n$ reziduuri; "
                             "repartiția Pareto generalizată (GPD): forma $\\xi$ (grosimea cozii), scala $\\beta$, estimate prin MLE; apoi înmulțim cu $\\sigma_t$, ca la FHS (Anexa B).") + "}",
              it((t("\\textbf{Raw changes}, threshold = 95\\% quantile", "\\textbf{Variațiile brute}, pragul = cuantila de 95\\%"),
                  t("$\\hat\\xi$ = @{evt.xi_raw|.3f}: a heavy tail", "$\\hat\\xi$ = @{evt.xi_raw|.3f}: o coadă groasă"),
                  t("moments above order @{evt.tail_index|.1f} do not exist", "momentele de ordin peste @{evt.tail_index|.1f} nu există")),
                 (t("\\textbf{After the GARCH filter}", "\\textbf{După filtrul GARCH}"),
                  t("median $\\hat\\xi$ = @{evt.xi_med|.3f}: the filter absorbs most of the tail", "$\\hat\\xi$ median = @{evt.xi_med|.3f}: filtrul preia cea mai mare parte a cozii"),
                  t("99\\% backtest: @{bt.RO.evt.a99.rate|.2f}\\% of days, the best of five", "testarea VaR de 99\\%: @{bt.RO.evt.a99.rate|.2f}\\% din zile, cel mai bun rezultat")), sep="2pt"),
              t("use EVT for the one-in-ten-years day that no window contains.",
                "folosiți EVT pentru ziua care apare o dată la zece ani și nu se află în nicio fereastră."),
              tryit=NB + " \\S3", cite="(Pickands, 1975; McNeil \\& Frey, 2000; Chan \\& Gray, 2006, IJF)", wl="0.55", wr="0.42")

    D.chart(t("Above the threshold the Pareto curve fits the data; the normal curve does not",
              "Peste prag, curba Pareto urmează datele, iar curba normală nu"), "gpd_tail", [
        t(("Last refit (@{evt.refit_last|date}): $\\hat\\xi$ = @{evt.xi_last|.3f}, $\\hat\\beta$ = @{evt.beta_last|.3f}",
           "$\\hat\\xi>0$ in @{evt.share_xi_pos|.0f}\\% of the refits: the standardised tail is sometimes heavy, sometimes not"),
          ("Ultima reestimare (@{evt.refit_last|date}): $\\hat\\xi$ = @{evt.xi_last|.3f}, $\\hat\\beta$ = @{evt.beta_last|.3f}",
           "$\\hat\\xi>0$ în @{evt.share_xi_pos|.0f}\\% din reestimări: coada reziduurilor standardizate este uneori groasă, alteori nu"))],
        height="0.54\\textheight",
        job=t("a 4-sigma day is rare but not impossible; the normal curve calls it impossible.",
              "o zi de 4 abateri standard este rară, dar posibilă; curba normală o consideră practic imposibilă."),
        tryit=NB + " \\S3", cite="(Balkema \\& de Haan, 1974; McNeil \\& Frey, 2000)")

    D.subsection(t("Comparing the methods", "Compararea metodelor"))
    lr = []
    for m in METHODS:
        L_ = N["last"][m]
        lr.append([MN[m], fmt(L_["var95"], ".2f", lang), fmt(L_["var99"], ".2f", lang), fmt(L_["es975"], ".2f", lang),
                   fmt(L_["var99_eur"], ",.0f", lang), fmt(L_["es975_eur"], ",.0f", lang)])
    D.frame(t("VaR and ES on the same day by five methods",
              "VaR și ES pentru aceeași zi, estimate prin cinci metode"),
            "\\begin{center}" + table("@{}lrrrrr@{}", [t("Method", "Metoda"), "VaR$_{" + dec("0.95") + "}$", "VaR$_{" + dec("0.99") + "}$", "ES$_{" + dec("0.975") + "}$",
                                                      t("VaR$_{0.99}$, kEUR", "VaR$_{0{,}99}$, mii EUR"), t("ES$_{0.975}$, kEUR", "ES$_{0{,}975}$, mii EUR")], lr,
                                      size="footnotesize", stretch="1.2") + "\\end{center}\\vspace{-1mm}" + note(
                t("Mean of the @{last.n} forecasts made for October 2026; first three columns in EUR/MWh; last two for 100 MW flat (2,400 MWh per day).",
                  "Media celor @{last.n} prognoze pentru zilele din octombrie 2026; primele trei coloane în EUR/MWh; ultimele două pentru 100 MW în bandă (2.400 MWh pe zi).")) +
            it((t("\\textbf{Reading the table}", "\\textbf{Cum citim tabelul}"),
                t("HS and Student-$t$ still carry the volatile days of the past year", "HS și Student-$t$ conțin încă zilele volatile din ultimul an"),
                t("FHS and EVT use today's volatility, below the yearly average in October 2026", "FHS și EVT folosesc volatilitatea actuală, sub media anului în octombrie 2026"))) +
            D.bottom(t("report two methods side by side and explain the gap.",
                       "raportați două metode alăturate și explicați diferența dintre ele."), NB + " \\S3"),
            "footnotesize", cite=t("(own estimates)", "(estimări proprii)"))

    D.chart(t("In the crisis FHS adapted within days; HS and the normal VaR lagged",
              "În criză, FHS s-a adaptat repede, iar HS și VaR normală au întîrziat"), "var_paths", [
        t(("Exceedances of the 99\\% VaR, 1 Jul 2021 -- 30 Jun 2023 (@{vp.n} days, @{vp.exp|.1f} expected)",
           "HS @{vp.hs}, normal @{vp.normal}, Student-$t$ @{vp.t}, FHS @{vp.fhs}, EVT @{vp.evt}"),
          ("Depășiri ale VaR de 99\\%, 1 iulie 2021 -- 30 iunie 2023 (@{vp.n} " + de("vp.n") + "zile, @{vp.exp|.1f} depășiri așteptate)",
           "HS: @{vp.hs}; normală: @{vp.normal}; Student-$t$: @{vp.t}; FHS: @{vp.fhs}; EVT: @{vp.evt}"))],
        height="0.56\\textheight",
        job=t("in a crisis, a model that reacts within days protects the cash.",
              "într-o criză, un model care reacționează în cîteva zile protejează lichiditățile."),
        tryit=NB + " \\S3", cite=t("(own estimates)", "(estimări proprii)"))

    D.chart(t("The square-root-of-time rule overstates the 10-day risk",
              "Regula rădăcinii pătrate a timpului supraestimează riscul pe 10 zile"), "horizon", [
        t(("10-day 99\\% quantile = @{horizon.ro10|.2f} $\\times$ the 1-day one (RO; @{horizon.de10|.2f} in DE-LU), not $\\sqrt{10}$ = @{horizon.sqrt10|.2f}",
           "variance ratio at 10 days @{horizon.vr10_ro|.2f} (1 = random walk); autocorrelation of $X_t$: @{horizon.ac1_ro|.3f} at lag 1, @{horizon.ac7_ro|.3f} at lag 7"),
          ("Cuantila de 99\\% pe 10 zile = @{horizon.ro10|.2f} $\\times$ cea pe o zi (RO; @{horizon.de10|.2f} în DE-LU), nu $\\sqrt{10}$ = @{horizon.sqrt10|.2f}",
           "raportul varianțelor la 10 zile: @{horizon.vr10_ro|.2f} (1 = mers aleator); autocorelația lui $X_t$: @{horizon.ac1_ro|.3f} (decalaj 1), @{horizon.ac7_ro|.3f} (decalaj 7)"))],
        height="0.52\\textheight",
        job=t("for a 10-day horizon, measure 10-day changes directly; multiplying by $\\sqrt{10}$ wastes capital.",
              "măsurați direct variațiile pe 10 zile; înmulțirea cu $\\sqrt{10}$ blochează capital inutil."),
        tryit=NB + " \\S3", cite=t("(own computation; Weron, 2014, IJF)", "(calcule proprii; Weron, 2014, IJF)"))

    # ------------------------------------------------------------------ 3 backtesting
    D.section(t("Backtesting VaR and ES", "Testarea retrospectivă a VaR și ES"))
    D.concept(t("Kupiec test: are there as many exceedances as promised?", "Testul Kupiec: sînt atîtea depășiri cîte au fost promise?"),
              t("A 99\\% VaR promises to be exceeded on 1\\% of days; count the exceedances and test whether the share differs from 1\\%.",
                "O VaR de 99\\% promite că va fi depășită în 1\\% din zile; numărăm depășirile și testăm dacă proporția lor diferă de 1\\%."),
              "\\[ I_t=\\mathbf 1\\{L_t>\\text{VaR}_{\\alpha,t}\\},\\qquad x=\\textstyle\\sum_{t=1}^{n}I_t,\\qquad \\hat p=x/n \\]"
              "\\[ \\text{LR}_{uc}=-2\\ln\\frac{(1-p)^{n-x}\\,p^{x}}{(1-\\hat p)^{n-x}\\,\\hat p^{\\,x}}\\ \\sim\\ \\chi^2_1 \\]" +
              "\\where{" + t("$I_t$ = exceedance indicator; $p=1-\\alpha$ = promised share; likelihood ratio (LR) test of unconditional coverage; reject at 5\\% if LR$_{uc}>$ 3.84.",
                             "$I_t$ = indicatorul depășirii; $p=1-\\alpha$ = proporția promisă; testul raportului de verosimilitate (LR) pentru acoperirea necondiționată; respingem la pragul de 5\\% dacă LR$_{uc}>$ 3{,}84.") + "}",
              it((t("\\textbf{On our data}, 99\\% VaR, @{bt.RO.fhs.a99.n|,d} days", "\\textbf{Pe datele din România}, VaR de 99\\%, @{bt.RO.fhs.a99.n|,d} " + de("bt.RO.fhs.a99.n") + "zile"),
                  t("expected @{bt.RO.fhs.a99.exp|.1f} exceedances", "depășiri așteptate: @{bt.RO.fhs.a99.exp|.1f}"),
                  t("normal @{bt.RO.normal.a99.x}, LR$_{uc}$ @{bt.RO.normal.a99.lr_uc|.1f}; FHS @{bt.RO.fhs.a99.x}, LR$_{uc}$ @{bt.RO.fhs.a99.lr_uc|.1f}",
                    "normală: @{bt.RO.normal.a99.x}, LR$_{uc}$ = @{bt.RO.normal.a99.lr_uc|.1f}; FHS: @{bt.RO.fhs.a99.x}, LR$_{uc}$ = @{bt.RO.fhs.a99.lr_uc|.1f}"),
                  t("EVT @{bt.RO.evt.a99.x}, $p$ = " + pval("bt.RO.evt.a99.p_uc"), "EVT: @{bt.RO.evt.a99.x}, $p$ = " + pval("bt.RO.evt.a99.p_uc"))),
                 (t("\\textbf{Power of the test}", "\\textbf{Puterea testului}"),
                  t("with one year at 99\\% we expect only 2--3 exceedances; the test can hardly reject", "pe un singur an, la 99\\%, ne așteptăm la doar 2--3 depășiri; testul respinge foarte greu"),
                  t("ten years of daily data make it sharp", "zece ani de date zilnice îl fac precis")), sep="2pt"),
              t("ask for the exceedance count before you trust anyone's VaR.",
                "cereți numărul depășirilor înainte de a avea încredere în VaR raportată de cineva."),
              tryit=NB + " \\S4", cite="(Kupiec, 1995, J.\\ Derivatives)", wl="0.52", wr="0.45")

    D.concept(t("Christoffersen test: do exceedances come in clusters?", "Testul Christoffersen: apar depășirile grupate?"),
              t("A good model is not surprised twice in a row: an exceedance today should not make one tomorrow more likely.",
                "Un model bun nu este surprins de două ori la rînd: o depășire azi nu trebuie să facă mai probabilă o depășire mîine."),
              "\\[ \\pi_{01}=\\Pr(I_t=1\\mid I_{t-1}=0),\\qquad \\pi_{11}=\\Pr(I_t=1\\mid I_{t-1}=1) \\]"
              "\\[ \\text{LR}_{ind}=-2\\ln\\frac{(1-\\hat\\pi)^{n_{00}+n_{10}}\\hat\\pi^{\\,n_{01}+n_{11}}}{(1-\\hat\\pi_{01})^{n_{00}}\\hat\\pi_{01}^{\\,n_{01}}(1-\\hat\\pi_{11})^{n_{10}}\\hat\\pi_{11}^{\\,n_{11}}}\\sim\\chi^2_1 \\]" +
              "\\where{" + t("$n_{ij}$ = days with $I_{t-1}=i$, $I_t=j$; $\\hat\\pi$ = overall share; $H_0$: $\\pi_{01}=\\pi_{11}$; joint test LR$_{cc}$ = LR$_{uc}$ + LR$_{ind}\\sim\\chi^2_2$.",
                             "$n_{ij}$ = numărul zilelor cu $I_{t-1}=i$ și $I_t=j$; $\\hat\\pi$ = proporția totală; $H_0$: $\\pi_{01}=\\pi_{11}$; testul comun LR$_{cc}$ = LR$_{uc}$ + LR$_{ind}\\sim\\chi^2_2$.") + "}",
              it((t("\\textbf{On our data}, 99\\% VaR, independence $p$-values", "\\textbf{Pe datele din România}, VaR de 99\\%, valorile $p$ ale testului de independență"),
                  t("HS " + pval("bt.RO.hs.a99.p_ind") + ", normal " + pval("bt.RO.normal.a99.p_ind") + ", FHS " + pval("bt.RO.fhs.a99.p_ind"),
                    "HS: " + pval("bt.RO.hs.a99.p_ind") + "; normală: " + pval("bt.RO.normal.a99.p_ind") + "; FHS: " + pval("bt.RO.fhs.a99.p_ind")),
                  t("no method fails it: exceedances rarely fall on consecutive days", "nicio metodă nu îl pică: depășirile cad rareori în zile consecutive")),
                 (t("\\textbf{But they cluster in months}", "\\textbf{Dar se grupează pe luni}"),
                  t("normal: @{bt.RO.normal.a99.rate_crisis|.2f}\\% of days in 2021--2022, @{bt.RO.normal.a99.rate_calm|.2f}\\% in 2017--2020",
                    "normală: @{bt.RO.normal.a99.rate_crisis|.2f}\\% din zile în 2021--2022, @{bt.RO.normal.a99.rate_calm|.2f}\\% în 2017--2020"),
                  t("a first-order test misses it; the traffic light sees it", "un test de ordinul întîi nu observă acest lucru; semaforul Basel îl observă")), sep="2pt"),
              t("look at the timing of exceedances, not only at their number.",
                "urmăriți momentul în care apar depășirile, nu doar numărul lor."),
              tryit=NB + " \\S4", cite="(Christoffersen, 1998, IER)", wl="0.55", wr="0.42")

    def btrow(z, m):
        r95, r99 = BT[z][m]["a95"], BT[z][m]["a99"]
        return [MN[m],
                heat(abs(r95["rate"] - 5), 0, 4, True, fmt(r95["rate"], ".2f", lang)), pval(f"bt.{z}.{m}.a95.p_uc"),
                f"{r99['x']}", heat(abs(r99["rate"] - 1), 0, 2.2, True, fmt(r99["rate"], ".2f", lang)), pval(f"bt.{z}.{m}.a99.p_uc"),
                pval(f"bt.{z}.{m}.a99.p_ind"), heat(r99["share_red"], 0, 30, True, fmt(r99["share_red"], ".1f", lang))]
    D.frame(t("Over ten years only the filtered methods pass at 95\\%; at 99\\% every method has too many exceedances",
              "În zece ani, doar metodele filtrate trec testul la 95\\%; la 99\\%, toate metodele au prea multe depășiri"),
            "\\begin{center}" + table("@{}lrrrrrrr@{}", [t("Romania", "România"), t("95\\%: share", "95\\%: proporția"), "Kupiec $p$",
                                                         t("99\\%: count", "99\\%: număr"), t("share, \\%", "proporția, \\%"), "Kupiec $p$",
                                                         "Christoffersen $p$", t("red days, \\%", "zile roșii, \\%")],
                                      [btrow("RO", m) for m in METHODS], size="footnotesize", stretch="1.2") + "\\end{center}\\vspace{-1mm}" + note(
                t(BTP[0].upper() + BTP[1:] + "; expected: 5\\% and 1\\% of @{bt.RO.fhs.a99.n|,d} days (@{bt.RO.fhs.a99.exp|.1f} at 99\\%); green = close to the target, red = far.",
                  BTP[0].upper() + BTP[1:] + "; așteptat: 5\\% și 1\\% din @{bt.RO.fhs.a99.n|,d} " + de("bt.RO.fhs.a99.n") + "zile (@{bt.RO.fhs.a99.exp|.1f} la 99\\%); verde = aproape de țintă, roșu = departe."),
                t("Red days = share of days whose last 250 days held 10 or more exceedances (next slide); Germany--Luxembourg: Appendix D.",
                  "Zile roșii = proporția zilelor în care ultimele 250 de zile conțin cel puțin 10 depășiri (diapozitivul următor); Germania--Luxemburg: Anexa D.")) +
            D.bottom(t("accept a model at 95\\%, but hold extra capital for the 99\\% tail that none of them captures fully.",
                       "acceptați un model la 95\\%, dar păstrați capital suplimentar pentru coada de 99\\%, pe care niciun model nu o surprinde complet."), NB + " \\S4"),
            "footnotesize", cite="(Kupiec, 1995; Christoffersen, 1998; " + t("own estimates)", "estimări proprii)"))

    D.chart(t("The Basel traffic light: the normal VaR spent @{bt.RO.normal.a99.share_red|.0f}\\% of days in the red zone",
              "Semaforul Basel: VaR normală a stat @{bt.RO.normal.a99.share_red|.0f}\\% din zile în zona roșie"), "traffic", [
        t(("Count of 99\\% exceedances in the last 250 days: green 0--4, yellow 5--9, red 10 or more by the Basel Committee on Banking Supervision (BCBS)",
           "a correct model is green with probability @{basel.p_green|.1f}\\%, red with @{basel.p_red|.3f}\\%",
           "red days: HS @{bt.RO.hs.a99.share_red|.1f}\\%, FHS @{bt.RO.fhs.a99.share_red|.1f}\\%, EVT @{bt.RO.evt.a99.share_red|.1f}\\%"),
          ("Numărul depășirilor VaR de 99\\% în ultimele 250 de zile: verde 0--4, galben 5--9, roșu 10 sau mai multe după Comitetul de la Basel pentru Supraveghere Bancară (BCBS)",
           "un model corect este în zona verde cu probabilitatea @{basel.p_green|.1f}\\% și în zona roșie cu @{basel.p_red|.3f}\\%",
           "zile în zona roșie: HS @{bt.RO.hs.a99.share_red|.1f}\\%, FHS @{bt.RO.fhs.a99.share_red|.1f}\\%, EVT @{bt.RO.evt.a99.share_red|.1f}\\%"))],
        height="0.50\\textheight",
        job=t("yellow means recalibrate, red means stop using the model for limits.",
              "zona galbenă cere recalibrarea modelului, iar cea roșie oprirea lui pentru limite."),
        tryit=NB + " \\S4", cite="(BCBS, 1996)")

    def prow(m):
        return [MN[m]] + [heat(abs(BT[z][m]["a99"][f"rate_{p}"] - 1), 0, 4, True, fmt(BT[z][m]["a99"][f"rate_{p}"], ".2f", lang))
                          for z in ["RO", "DE_LU"] for p in ["calm", "crisis", "after"]]
    D.frame(t("In 2021--2022 every method failed; since 2023 the filtered ones are back near 1\\%",
              "În 2021--2022 toate metodele au eșuat; din 2023, metodele filtrate au revenit aproape de 1\\%"),
            "\\begin{center}" + table("@{}lrrrrrr@{}", [t("99\\% VaR, \\% of days", "VaR 99\\%, \\% din zile"),
                                                       "RO 17--20", "RO 21--22", "RO 23--26", "DE-LU 17--20", "DE-LU 21--22", "DE-LU 23--26"],
                                      [prow(m) for m in METHODS], size="footnotesize", stretch="1.2") + "\\end{center}\\vspace{-1mm}" +
            it((t("\\textbf{The crisis}", "\\textbf{Criza}"),
                t("even FHS was exceeded on @{bt.RO.fhs.a99.rate_crisis|.2f}\\% of days in Romania: the gas shock moved the whole distribution",
                  "chiar și FHS a fost depășită în @{bt.RO.fhs.a99.rate_crisis|.2f}\\% din zile în România: șocul gazelor a mutat întreaga repartiție")),
               (t("\\textbf{After the crisis}", "\\textbf{După criză}"),
                t("FHS @{bt.RO.fhs.a99.rate_after|.2f}\\%, EVT @{bt.RO.evt.a99.rate_after|.2f}\\%, HS @{bt.RO.hs.a99.rate_after|.2f}\\%, normal @{bt.RO.normal.a99.rate_after|.2f}\\%",
                  "FHS: @{bt.RO.fhs.a99.rate_after|.2f}\\%; EVT: @{bt.RO.evt.a99.rate_after|.2f}\\%; HS: @{bt.RO.hs.a99.rate_after|.2f}\\%; normală: @{bt.RO.normal.a99.rate_after|.2f}\\%")), sep="2pt") +
            D.bottom(t("test every model on 2021--2022 before you trust it in a crisis.",
                       "testați orice model pe 2021--2022 înainte de a vă baza pe el într-o criză."), NB + " \\S4"),
            "footnotesize", cite=t("(own estimates)", "(estimări proprii)"))

    zrows = [[MN[m], fmt(BT["RO"][m]["z2"]["all"]["z2"], ".3f", lang), pval(f"bt.RO.{m}.z2.all.p"),
              fmt(BT["RO"][m]["z2"]["crisis"]["z2"], ".3f", lang), pval(f"bt.RO.{m}.z2.crisis.p"),
              fmt(BT["RO"][m]["z2"]["after"]["z2"], ".3f", lang), pval(f"bt.RO.{m}.z2.after.p")] for m in METHODS]
    D.concept(t("Backtesting ES: are the losses beyond VaR as large as forecast?", "Testarea ES: sînt pierderile de dincolo de VaR atît de mari cît s-a prognozat?"),
              t("Divide each exceedance loss by its ES forecast; if ES is right, the ratios average 1.",
                "Împărțim fiecare pierdere din zilele cu depășiri la prognoza ES; dacă ES este corect, media este 1."),
              "\\[ Z_2=\\frac{1}{T(1-\\alpha)}\\sum_{t=1}^{T}\\frac{L_t\\,I_t}{\\text{ES}_{\\alpha,t}}-1,\\qquad \\E_{H_0}[Z_2]=0 \\]" +
              "\\where{" + t("$\\alpha$ = 0.975; $I_t$ = exceedance of VaR$_{0.975}$; $Z_2>0$ = ES too small; "
                             "$p$-value from 2,000 paths simulated from each model (Appendix C).",
                             "$\\alpha$ = 0{,}975; $I_t$ = depășirea VaR$_{0{,}975}$; $Z_2>0$ = ES prea mic; "
                             "valoarea $p$: 2.000 de traiectorii simulate din fiecare model (Anexa C).") + "}",
              table("@{}lrrrrrr@{}", ["$Z_2$", t("all", "total"), "$p$", "2021--22", "$p$", "2023--26", "$p$"], zrows, size="scriptsize", stretch="1.1") + "\\par\\vspace{1mm}" +
              it(t("\\textbf{Reading}: every ES was too small in the crisis; since 2023, FHS, EVT and HS pass.",
                   "\\textbf{Interpretare}: în criză, toate prognozele ES au fost prea mici; din 2023, FHS, EVT și HS trec testul.")),
              t("judge ES on several years, never on one quarter (about 9 tail days a year).",
                "evaluați ES pe mai mulți ani, niciodată pe un trimestru (circa 9 zile extreme pe an)."),
              tryit=NB + " \\S4", cite="(Acerbi \\& Székely, 2014; Pele \\& Mazurencu-Marinescu-Pele, 2026)", wl="0.45", wr="0.52")

    # ------------------------------------------------------------------ AIDA 2026: conformal diagnosis of VaR forecasts
    D.frame(t("AIDA 2026: one conformal shift measures how far a VaR misses, and repairs it",
              "AIDA 2026: o deplasare conformală arată cît greșește VaR și o corectează"), it(
        (t("\\textbf{What the work did} (D.\\,T.\\ Pele, AIDA (AI and Digital Assets in Energy and Finance) conference, 4 June 2026)", "\\textbf{Ce a făcut lucrarea} (D.\\,T.\\ Pele, conferința AIDA (AI and Digital Assets in Energy and Finance), 4 iunie 2026)"),
         t("score $s_t=\\hat q_t-r_t$ ($>0$ on an exceedance day); $\\hat q_V$ = 99\\% quantile of past scores; corrected VaR = VaR + $\\hat q_V$, fixed (audit) or rolling over 250 days",
           "scorul $s_t=\\hat q_t-r_t$ ($>0$ în ziua unei depășiri); $\\hat q_V$ = cuantila de 99\\% a scorurilor trecute; VaR corectată = VaR + $\\hat q_V$, fixă (audit) sau glisantă pe 250 de zile"),
         t("1\\% VaR of 10 models (foundation models, GARCH-type, HS) on 24 assets, incl.\\ oil and gas: 240 pairs; Kupiec, Christoffersen, traffic light",
           "VaR de 1\\% a 10 modele (fundaționale, de tip GARCH, HS) pe 24 de active, inclusiv petrol și gaze: 240 de perechi; Kupiec, Christoffersen, semaforul Basel")),
        (t("\\textbf{What it found}", "\\textbf{Ce a găsit}"),
         t("$\\hat q_V$ from $-$0.007 (too prudent) to +0.102 (no tail signal); it explains 53.4\\% (partial $R^2$) of the gain in quantile score",
           "$\\hat q_V$ între $-$0{,}007 (prea prudent) și +0{,}102 (fără informație despre coadă); explică 53{,}4\\% ($R^2$ parțial) din cîștigul la scorul cuantilic"),
         t("green-zone pairs: 63/240 (26.2\\%) raw, 203/240 (84.6\\%) fixed, 234/240 (97.5\\%) rolling",
           "perechi în zona verde: 63/240 (26{,}2\\%) inițial, 203/240 (84{,}6\\%) fix, 234/240 (97{,}5\\%) glisant"),
         t("the exceedance rate is restored, their clustering is not", "rata depășirilor este refăcută, gruparea lor nu")),
        (t("\\textbf{Link to this lecture}", "\\textbf{Legătura cu acest curs}"),
         t("Kupiec says whether VaR fails, $\\hat q_V$ by how much; our guarantee widening $\\hat c_t$ (Section 4) is the same shift",
           "testul Kupiec arată dacă VaR eșuează, $\\hat q_V$ cu cît; lărgirea garanției $\\hat c_t$ (secțiunea 4) este aceeași deplasare")),
        sep="1pt") + note(t("Findings as stated by the authors; talk: \\href{" + TALK_PELE + "}{slides}; paper submitted.",
                            "Rezultatele sînt cele raportate de autori; prezentarea: \\href{" + TALK_PELE + "}{diapozitive}; lucrare trimisă spre publicare.")) +
        D.bottom(t("after a failed backtest, widen VaR by the conformal shift and keep testing for clusters.",
                   "după un test eșuat, lărgiți VaR cu deplasarea conformală și testați în continuare gruparea depășirilor.")),
        "footnotesize", cite=t("(Pele, Bolovăneanu, Ginavar, Lessmann \\& Härdle, AIDA, ASE, 4 June 2026)", "(Pele, Bolovăneanu, Ginavar, Lessmann \\& Härdle, AIDA, ASE, 4 iunie 2026)"))

    # ------------------------------------------------------------------ 4 collateral and limits
    D.section(t("From quantiles to margins, guarantees and limits", "De la cuantile la marje, garanții și limite"))
    D.subsection(t("Exchange margins", "Marjele la bursă"))
    D.concept(t("Exchange margins: initial margin as a VaR, variation margin paid daily", "Marjele la bursă: marja inițială ca VaR, marja de variație plătită zilnic"),
              t("The clearing house holds a deposit that covers a 99\\% two-day loss and settles gains and losses in cash every evening.",
                "Casa de compensare reține un depozit pentru pierderea de 99\\% pe două zile și decontează zilnic diferențele."),
              "\\[ \\underbrace{\\text{IM}_t=K F_t\\,\\hat q_{" + dec("0.99") + "}\\big(|r^{(2)}|\\big)}_{\\text{" + t("initial margin", "marja inițială") + "}},\\quad "
              "\\underbrace{\\text{VM}_t=n K(F_t-F_{t-1})}_{\\text{" + t("variation margin", "marja de variație") + "}} \\]" +
              "\\where{" + t("initial margin (IM), variation margin (VM), set by the central counterparty (CCP); $F_t$ = futures price; $K$ = 1,000 barrels per Brent lot; "
                             "$r^{(2)}$ = two-day return; $n$ = lots sold (+) or bought ($-$).",
                             "marja inițială (IM) și de variație (VM), cerute de contrapartea centrală (CCP); $F_t$ = prețul futures, $K$ = 1.000 de barili (un lot Brent); "
                             "$r^{(2)}$ = randamentul pe două zile; $n$ = loturi vîndute (+) sau cumpărate ($-$).") + "}",
              it((t("\\textbf{European Market Infrastructure Regulation (EMIR)}, regulatory technical standards (RTS) 153/2013",
                    "\\textbf{Regulamentul privind infrastructura pieței europene (EMIR)}, standardele tehnice de reglementare (RTS) 153/2013"),
                  t("futures: 99\\%, 2-day liquidation, at least 12 months of data (Art.~24--26)", "futures: 99\\%, lichidare în 2 zile, minimum 12 luni de date (art.~24--26)"),
                  t("anti-procyclicality (APC), Art.~28: a 25\\% buffer, or 25\\% weight on stress, or a 10-year floor",
                    "instrumente anticiclice (APC), art.~28: o rezervă de 25\\%, o pondere de 25\\% pentru zilele de criză sau un prag pe 10 ani")),
                 t("\\textbf{Intercontinental Exchange (ICE) Brent}, 100 lots sold: largest one-day VM @{brent.vm_max|.2f} million USD (@{brent.vm_max_date|date})",
                   "\\textbf{Brent, Intercontinental Exchange (ICE)}, 100 de loturi vîndute: VM maximă într-o zi @{brent.vm_max|.2f} mil.\\ USD (@{brent.vm_max_date|date})"), sep="2pt"),
              t("a hedged producer gains on the physical sale later, but pays the margin today.",
                "producătorul acoperit cîștigă mai tîrziu din vînzarea fizică, dar plătește marja azi."),
              tryit=NB + " \\S5", cite=t("(EU Delegated Regulation 153/2013; ICE Futures Europe)", "(Regulamentul delegat (UE) 153/2013; ICE Futures Europe)"), wl="0.45", wr="0.52")

    D.frame(t("In 2022, well-hedged energy companies ran short of cash for margins", "În 2022, companii energetice bine acoperite la risc au rămas fără lichidități pentru marje"), it(
        t(("\\textbf{What happened}, according to the European Central Bank (ECB), November 2022",
           "TTF gas futures reached 227 EUR/MWh on 7 March 2022, about 12 times the level of early 2021",
           "by mid-2022 about twice as much initial margin was posted as in late 2021",
           "the firms hurt were mostly utilities and producers that had sold forward: hedgers, not speculators"),
          ("\\textbf{Ce s-a întîmplat}, după Banca Centrală Europeană (BCE), noiembrie 2022",
           "contractele futures pe gaze TTF au atins 227 EUR/MWh la 7 martie 2022, de circa 12 ori nivelul de la începutul anului 2021",
           "la jumătatea anului 2022 se depunea o marjă inițială de aproximativ două ori mai mare decît la sfîrșitul anului 2021",
           "companiile afectate au fost mai ales utilitățile și producătorii care vînduseră la termen: firme care se acopereau la risc, nu speculatori")),
        t(("\\textbf{How the European Union (EU) responded}", "Delegated Regulation (EU) 2022/2311: public guarantees accepted as collateral until 29 November 2023"),
          ("\\textbf{Cum a răspuns Uniunea Europeană (UE)}", "Regulamentul delegat (UE) 2022/2311: garanțiile publice acceptate drept garanții pînă la 29 noiembrie 2023")),
        t(("\\textbf{In Romania}, on the day-ahead market", "OPCOM accepts a buy order at a positive price only up to the participant's guarantee (a bank letter)"),
          ("\\textbf{În România}, pe piața pentru ziua următoare", "OPCOM validează o ofertă de cumpărare la preț pozitiv numai în limita garanției participantului (o scrisoare de garanție bancară)")),
        sep="3pt") + D.bottom(t("the risk that sinks a hedged company is liquidity, not the price itself.",
                                "riscul care poate scufunda o companie acoperită la risc este cel de lichiditate, nu prețul în sine.")),
        "footnotesize", cite=t("(ECB, 2022; Delegated Regulation (EU) 2022/2311; OPCOM, 2025)", "(BCE, 2022; Regulamentul delegat (UE) 2022/2311; OPCOM, 2025)"))

    D.chart(t("Margins are procyclical: in 2026 the Brent margin rose @{brent.ratio26|.1f}-fold in two months",
              "Marjele sînt prociclice: în 2026, marja Brent a crescut de @{brent.ratio26|.1f} ori în două luni"), "brent_im", [
        t(("Brent rose from @{brent.F_pre26|.2f} USD (27 Feb 2026) to @{brent.F_max26|.2f} USD (@{brent.F_max26_date|date})",
           "IM with 12 months of history: @{brent.im1_pre26|,.0f} $\\to$ @{brent.im1_max26|,.0f} USD per lot; with the floor since 2015: $\\times$@{brent.ratio26_apc|.2f} instead of $\\times$@{brent.ratio26|.2f}",
           "losses beyond IM: @{brent.exc1|.2f}\\% of days with 12 months, @{brent.exca|.2f}\\% with the floor (target 1\\%)"),
          ("Prețul Brent a urcat de la @{brent.F_pre26|.2f} USD (27 februarie 2026) la @{brent.F_max26|.2f} USD (@{brent.F_max26_date|date})",
           "IM cu 12 luni de date: @{brent.im1_pre26|,.0f} $\\to$ @{brent.im1_max26|,.0f} USD pe lot; cu pragul calculat din 2015: $\\times$@{brent.ratio26_apc|.2f} în loc de $\\times$@{brent.ratio26|.2f}",
           "pierderi mai mari decît IM: @{brent.exc1|.2f}\\% din zile cu 12 luni de date, @{brent.exca|.2f}\\% cu prag (ținta: 1\\%)"))],
        height="0.48\\textheight",
        job=t("plan your cash for the margin a crisis would demand, not for today's margin.",
              "planificați lichiditățile pentru marja cerută într-o criză, nu pentru marja de astăzi."),
        tryit=NB + " \\S5", cite=t("(own computation; EMIR RTS, Art.~28; ICE Brent)", "(calcule proprii; RTS EMIR, art.~28; Brent ICE)"))

    D.subsection(t("Guarantees and limits", "Garanții și limite"))
    g = "guar.a99"
    D.concept(t("The day-ahead guarantee is set from a quantile forecast of tomorrow's price", "Garanția pentru PZU se calculează din cuantila prognozată a prețului de mîine"),
              t("To be sure its order clears, a supplier bids up to a high price, and the guarantee must cover price times volume.",
                "Ca să fie sigur că va cumpăra, furnizorul ofertează pînă la un preț ridicat; garanția acoperă acest preț înmulțit cu volumul."),
              "\\[ G_t\\ \\ge\\ Q\\cdot 24\\cdot \\hat q_{\\tau,t},\\qquad \\hat q_{\\tau,t}=\\beta_0+\\beta_1P_{t-1}+\\beta_2P_{t-7}+\\textstyle\\sum_j\\delta_jD_{j,t} \\]"
              "\\[ \\tilde q_{\\tau,t}=\\hat q_{\\tau,t}+\\hat c_t,\\qquad \\hat c_t=\\hat q_\\tau\\big(P_s-\\hat q_{\\tau,s},\\ s=t-365,\\dots,t-1\\big) \\]" +
              "\\where{" + t("$G_t$ = guarantee, EUR; $\\hat q_{\\tau,t}$ = quantile regression (QR) on the last 365 days, as in quantile regression averaging (QRA), Lecture 2; "
                             "$D_{j,t}$ = weekday dummies; $\\hat c_t$ = conformal correction from past errors.",
                             "$G_t$ = garanția, EUR; $\\hat q_{\\tau,t}$ = regresia cuantilică (QR) pe ultimele 365 de zile, ca la medierea prin regresie cuantilică (QRA), cursul 2; "
                             "$D_{j,t}$ = variabile pentru ziua săptămînii; $\\hat c_t$ = corecția conformală, din erorile trecute.") + "}",
              it((t("\\textbf{On our data}, $\\tau$ = 0.99, 2017--2026", "\\textbf{Pe datele din România}, $\\tau$ = 0{,}99, 2017--2026"),
                  t("days with the price below the forecast: QR @{" + g + ".qr.cov|.2f}\\%, widened @{" + g + ".cqr.cov|.2f}\\%, FHS @{" + g + ".fhs.cov|.2f}\\%",
                    "zile cu prețul sub prognoză: QR @{" + g + ".qr.cov|.2f}\\%; QR lărgită @{" + g + ".cqr.cov|.2f}\\%; FHS @{" + g + ".fhs.cov|.2f}\\%"),
                  ),
                 (t("\\textbf{Cost}, 100 MW flat", "\\textbf{Costul}, 100 MW în bandă"),
                  t("@{" + g + ".cqr.g_mean|.3f} million EUR per day on average, +@{" + g + ".extra_cost_pct|.1f}\\% for the widening", "în medie @{" + g + ".cqr.g_mean|.3f} milioane EUR pe zi; lărgirea costă +@{" + g + ".extra_cost_pct|.1f}\\%"),
                  t("2017--2020: @{" + g + ".cqr.g_calm|.3f}; 2021--2022: @{" + g + ".cqr.g_crisis|.3f} million EUR per day", "2017--2020: @{" + g + ".cqr.g_calm|.3f}; 2021--2022: @{" + g + ".cqr.g_crisis|.3f} milioane EUR pe zi")), sep="2pt"),
              t("size the bank line behind the guarantee on the crisis quantile, before the crisis.",
                "dimensionați linia bancară din spatele garanției pe cuantila din criză, înainte de criză."),
              tryit=NB + " \\S6", cite="(OPCOM, 2025; Koenker \\& Bassett, 1978; Romano et al., 2019)", wl="0.55", wr="0.42")

    D.chart(t("Widening the tails brings the 99\\% quantile close to its promise", "Lărgirea cozilor apropie cuantila de 99\\% de acoperirea promisă"), "coverage", [
        t(("Kupiec $p$ at 99\\%: QR " + pval(g + ".qr.kupiec_p") + ", widened " + pval(g + ".cqr.kupiec_p") + ", FHS " + pval(g + ".fhs.kupiec_p"),
           "at 95\\% the widened QR passes ($p$ = " + pval("guar.a95.cqr.kupiec_p") + "), as Lecture 2 suggested for the tails"),
          ("Testul Kupiec la 99\\%: QR " + pval(g + ".qr.kupiec_p") + "; QR lărgită " + pval(g + ".cqr.kupiec_p") + "; FHS " + pval(g + ".fhs.kupiec_p"),
           "la 95\\%, QR lărgită trece testul ($p$ = " + pval("guar.a95.cqr.kupiec_p") + "), așa cum sugera cursul 2 pentru cozi"))],
        height="0.50\\textheight",
        job=t("a forecast used for collateral must be calibrated in the tail, not only accurate on average.",
              "o prognoză folosită pentru garanții trebuie să fie calibrată în coadă, nu doar precisă în medie."),
        tryit=NB + " \\S6", cite="(Nowotarski \\& Weron, 2018, RSER; Romano et al., 2019)")

    D.concept(t("A position limit in MW should shrink when VaR grows", "Limita de poziție în MW trebuie să scadă atunci cînd VaR crește"),
              t("The board sets a daily risk budget in EUR; the desk divides it by today's VaR per MW.",
                "Conducerea stabilește un buget zilnic de risc, în EUR; biroul de tranzacționare îl împarte la VaR de azi pentru 1 MW."),
              "\\[ Q^{\\max}_t=\\frac{B}{24\\cdot\\text{VaR}^{\\text{FHS}}_{0.99,t}} \\]".replace("0.99", "0{,}99" if ro else "0.99") +
              "\\where{" + t("$B$ = daily VaR budget, here 250,000 EUR (an assumption for the example); VaR in EUR/MWh; $Q^{\\max}_t$ in MW of open flat position.",
                             "$B$ = bugetul zilnic de VaR, aici 250.000 EUR (o ipoteză de lucru); VaR în EUR/MWh; $Q^{\\max}_t$ = poziția deschisă maximă în bandă, în MW.") + "}",
              it((t("\\textbf{On our data}, FHS 99\\% VaR", "\\textbf{Pe datele din România}, VaR FHS de 99\\%"),
                  t("2019 (median): VaR @{limit.v_2019|.2f} EUR/MWh, limit @{limit.q_2019|,.0f} MW", "2019 (mediana): VaR = @{limit.v_2019|.2f} EUR/MWh; limita = @{limit.q_2019|,.0f} MW"),
                  t("@{limit.q_min_date|date}: VaR @{limit.v_max|.2f}, limit @{limit.q_min|,.0f} MW", "@{limit.q_min_date|date}: VaR = @{limit.v_max|.2f}; limita = @{limit.q_min|,.0f} MW"),
                  t("@{data.end|date}: VaR @{limit.v_last|.2f}, limit @{limit.q_last|,.0f} MW", "@{data.end|date}: VaR = @{limit.v_last|.2f}; limita = @{limit.q_last|,.0f} MW")),
                 (t("\\textbf{Why it matters}", "\\textbf{De ce contează}"),
                  t("a fixed MW limit lets the money at risk grow with volatility", "o limită fixă în MW lasă suma expusă la risc să crească odată cu volatilitatea"),
                  t("a fixed EUR budget keeps it constant", "un buget fix în EUR o menține constantă")), sep="2pt"),
              t("set limits in EUR of VaR and convert them to MW every day.", "stabiliți limitele în EUR de VaR și transformați-le zilnic în MW."),
              tryit=NB + " \\S6", cite=t("(own estimates)", "(estimări proprii)"), wl="0.46", wr="0.51")

    # ------------------------------------------------------------------ 5 positions
    D.section(t("Price risk for suppliers and producers", "Riscul de preț pentru furnizori și producători"))
    S = "supplier"
    D.concept(t("A supplier's monthly cost-at-risk: the normal limit failed again", "Costul lunar la risc al unui furnizor: limita normală a eșuat din nou"),
              t("A supplier prices next month at this month's cost; the risk is a jump of the load-weighted price.",
                "Furnizorul stabilește prețul lunii viitoare după costul lunii curente; riscul este un salt al prețului ponderat cu consumul."),
              "\\[ \\bar P^{L}_m=\\frac{\\sum_h P_hL_h}{\\sum_h L_h},\\qquad o_m=\\frac{\\bar P^{L}_m}{\\bar P^{L}_{m-1}}-1 \\]\\vspace{-2mm}\\[ \\text{CFaR}_{0.95}=\\hat q_{0.95}(o_m) \\]".replace("0.95", "0{,}95" if ro else "0.95") +
              "\\where{" + t("$P_h$ = hourly price; $L_h$ = Romanian load (portfolio shape); $o_m$ = cost overrun; "
                             "cash-flow-at-risk (CFaR) = its quantile; in EUR for 100 MW on average.",
                             "$P_h$ = prețul orar; $L_h$ = consumul național (profilul portofoliului); $o_m$ = depășirea costului; "
                             "fluxul de numerar la risc (CFaR) = cuantila ei; în EUR, pentru 100 MW în medie.") + "}",
              it((t("\\textbf{On our data}, @{supplier.n} months, @{supplier.start|ym} -- @{supplier.end|ym}", "\\textbf{Pe datele din România}, @{supplier.n} " + de("supplier.n") + "luni, @{supplier.start|ym} -- @{supplier.end|ym}"),
                  t("normal 99\\% limit (2015--2020): +@{supplier.lim99|.1f}\\%, exceeded @{supplier.exc99_post} times since 2021 (@{supplier.exp99_post|.1f} expected)",
                    "limita normală de 99\\% (2015--2020): +@{supplier.lim99|.1f}\\%, depășită de @{supplier.exc99_post} ori din 2021 (@{supplier.exp99_post|.1f} așteptate)"),
                  t("worst month @{supplier.worst|ym}: +@{supplier.worst_pct|.1f}\\%, @{supplier.worst_eur|.2f} million EUR", "cea mai proastă lună, @{supplier.worst|ym}: +@{supplier.worst_pct|.1f}\\%, adică @{supplier.worst_eur|.2f} milioane EUR")),
                 (t("\\textbf{Empirical, all months}", "\\textbf{Empiric, toate lunile}"),
                  t("CFaR$_{0.95}$ = +@{supplier.q95_all|.1f}\\%, i.e.\\ @{supplier.q95_eur|.2f} million EUR", "CFaR$_{0{,}95}$ = +@{supplier.q95_all|.1f}\\%, adică @{supplier.q95_eur|.2f} milioane EUR"),
                  t("ES$_{0.95}$ = +@{supplier.es95_all|.1f}\\%, i.e.\\ @{supplier.es95_eur|.2f} million EUR", "ES$_{0{,}95}$ = +@{supplier.es95_all|.1f}\\%, adică @{supplier.es95_eur|.2f} milioane EUR")), sep="2pt"),
              t("price a fixed retail offer with an ES-based premium, or hedge it forward (Lecture 5).",
                "includeți în oferta cu preț fix o primă calculată din ES sau acoperiți-o la termen (cursul 5)."),
              tryit=NB + " \\S7", cite=t("(own computation; Assignment 2)", "(calcule proprii; tema 2)"), wl="0.52", wr="0.45")

    D.chart(t("Since 2021 the normal 99\\% monthly limit was exceeded @{supplier.exc99_post} times (@{supplier.exp99_post|.1f} expected)",
              "Din 2021, limita lunară normală de 99\\% a fost depășită de @{supplier.exc99_post} ori (@{supplier.exp99_post|.1f} așteptate)"), "supplier_month", [
        t("Red bars exceed the limit computed in 2020; the largest overrun came in @{supplier.worst|ym}, after the summer of 2024.",
          "Barele roșii depășesc limita calculată în 2020; cea mai mare depășire a apărut în @{supplier.worst|ym}, după vara anului 2024.")],
        height="0.52\\textheight",
        job=t("re-estimate the monthly limit every quarter and stress it with the 2022 months.",
              "reestimați limita lunară în fiecare trimestru și testați-o în condițiile lunilor din 2022."),
        tryit=NB + " \\S7", cite=t("(own computation)", "(calcule proprii)"))

    D.concept(t("Loss tails: the supplier's tail is heavier than the producer's", "Cozile pierderilor: coada furnizorului este mai groasă decît a producătorului"),
              t("A supplier loses when the price rises, a producer when it falls; prices jump up more than down.",
                "Furnizorul pierde cînd prețul crește, producătorul cînd scade; prețurile sar mai mult în sus decît în jos."),
              "\\[ L^{\\text{" + t("buyer", "cumpărător") + "}}_t=+Q\\,24\\,X_t,\\qquad L^{\\text{" + t("seller", "vînzător") + "}}_t=-Q\\,24\\,X_t \\]" +
              "\\where{" + t("one distribution of $X_t$, two tails: upper (supplier), lower (producer selling spot); skewness of $X_t$: @{producer.skew|.2f}.",
                             "o singură repartiție a lui $X_t$, două cozi: superioară (furnizorul) și inferioară (producătorul care vinde pe piața spot); asimetria lui $X_t$: @{producer.skew|.2f}.") + "}",
              it((t("\\textbf{Daily}, EUR/MWh, @{data.start|date} -- @{data.end|date}", "\\textbf{Zilnic}, EUR/MWh, @{data.start|date} -- @{data.end|date}"),
                  t("99\\% quantile (supplier): +@{producer.d_q99|.2f}; 1\\% quantile (producer): @{producer.d_q01|.2f}", "cuantila de 99\\% (furnizorul): +@{producer.d_q99|.2f}; cuantila de 1\\% (producătorul): @{producer.d_q01|.2f}"),
                  t("ES$_{0.975}$: @{producer.d_es_hi|.2f} (supplier) vs @{producer.d_es_lo|.2f} (producer)", "ES$_{0{,}975}$: @{producer.d_es_hi|.2f} (furnizorul) față de @{producer.d_es_lo|.2f} (producătorul)")),
                 (t("\\textbf{Monthly base price}", "\\textbf{Prețul de bază lunar}"),
                  t("95\\% quantile of the change +@{producer.m_q95|.1f}\\%, 5\\% quantile @{producer.m_q05|.1f}\\%", "cuantila de 95\\% a variației: +@{producer.m_q95|.1f}\\%; cuantila de 5\\%: @{producer.m_q05|.1f}\\%"),
                  ), sep="2pt"),
              t("the producer's price risk is smaller, but a dry year adds volume risk (next slide).",
                "riscul de preț al producătorului este mai mic, dar un an secetos adaugă riscul de volum (diapozitivul următor)."),
              tryit=NB + " \\S7", cite=t("(own computation)", "(calcule proprii)"), wl="0.47", wr="0.50")

    D.frame(t("Case study C4: a systemic risk meter and two risks specific to energy companies",
              "Studiul de caz C4: un indicator de risc sistemic și două riscuri specifice companiilor energetice"), it(
        t(("\\textbf{The paper} (Toma, Dima, Grecu, Pele \\& Lessmann, 2026)",
           "data and method: 100 European energy companies, 2016--2026; 5\\% quantile regressions with the least absolute shrinkage and selection operator (LASSO); the mean penalty is the Energy Financial Risk Meter (EFRM)",
           "result: the EFRM captures 2020 and 2022; with the ECB's Composite Indicator of Systemic Stress (CISS) it predicts volatile months with area under the curve (AUC) 0.731"),
          ("\\textbf{Ce a făcut lucrarea} (Toma, Dima, Grecu, Pele \\& Lessmann, 2026)",
           "date și metodă: 100 de companii energetice europene, 2016--2026; regresii cuantilice de 5\\% cu operatorul de contracție și selecție în normă absolută (LASSO); penalizarea medie este indicatorul de risc financiar al sectorului energetic (EFRM)",
           "rezultat: EFRM surprinde șocurile din 2020 și 2022; împreună cu indicatorul compozit de stres sistemic al BCE (CISS), prognozează lunile volatile cu aria de sub curbă (AUC) 0,731")),
        t(("\\textbf{Our replication} on three Romanian companies (OMV Petrom, Romgaz, Nuclearelectrica)",
           "AUC @{c4.aucERM|.2f}, against @{c4.aucVol|.2f} for past volatility: a systemic meter needs many firms, as in the paper"),
          ("\\textbf{Replicarea noastră} pe trei companii din România (OMV Petrom, Romgaz, Nuclearelectrica)",
           "AUC @{c4.aucERM|.2f}, față de @{c4.aucVol|.2f} pentru volatilitatea trecută: un indicator sistemic are nevoie de multe companii, ca în lucrare")),
        t(("\\textbf{Energy-specific risks}", "price--volume premium of the household profile: @{c4.premPctLast|.1f}\\% of the base price in 2025",
           "dry-year buy-back of a hydro fleet that sold its median output forward: @{c4.maxBuy|,.0f} million EUR (@{c4.maxBuyYear})"),
          ("\\textbf{Riscuri specifice energiei}", "prima preț--volum a profilului casnic: @{c4.premPctLast|.1f}\\% din prețul de bază în 2025",
           "recumpărarea în anul secetos pentru un parc hidro care a vîndut la termen producția mediană: @{c4.maxBuy|,.0f} " + de("c4.maxBuy") + "milioane EUR (@{c4.maxBuyYear})")),
        sep="2pt") + D.bottom(t("put the systemic meter, the price--volume premium and the dry-year cost on one dashboard.",
                   "includeți indicatorul sistemic, prima preț--volum și costul anului secetos în același tablou de bord.")),
        "footnotesize", cite="(Toma, Dima, Grecu, Pele \\& Lessmann, 2026, SSRN; " + t("case study C4", "studiul de caz C4") + ")")

    D.frame(t("AIDA 2026: systemic tail risk in EU energy broke upward in July 2021",
              "AIDA 2026: riscul sistemic din energia UE a crescut brusc din iulie 2021"), it(
        (t("\\textbf{What the work did} (F.-M.\\ Toma, AIDA conference, 3 June 2026; paper of case study C4)",
           "\\textbf{Ce a făcut lucrarea} (F.-M.\\ Toma, conferința AIDA, 3 iunie 2026; lucrarea din studiul de caz C4)"),
         t("100 European energy firms, April 2016 -- March 2026: each firm's 5\\% return quantile regressed by LASSO on the other 99 firms, oil, gas and stock indices",
           "100 de companii energetice europene, aprilie 2016 -- martie 2026: cuantila de 5\\% a randamentului fiecărei firme, regresată prin LASSO pe celelalte 99 de firme, petrol, gaze și indici bursieri"),
         t("EFRM = mean LASSO penalty: more links needed to explain the tail = more systemic exposure",
           "EFRM = penalizarea LASSO medie: mai multe legături necesare pentru a explica coada = expunere sistemică mai mare")),
        (t("\\textbf{What it found}", "\\textbf{Ce a găsit}"),
         t("EFRM breaks: February 2020 (pandemic) and July 2021 (gas run-up), seven months before the invasion",
           "rupturi ale EFRM: februarie 2020 (pandemia) și iulie 2021 (creșterea gazelor), cu șapte luni înaintea invaziei"),
         t("geopolitical risk moved the EFRM only after the invasion: +1.52 percentage points (time-varying model)",
           "riscul geopolitic a influențat EFRM abia după invazie: +1{,}52 puncte procentuale (model cu parametri variabili)"),
         t("effect on Stoxx 600 stocks about 60\\% weaker since, on 5-year credit default swaps still positive",
           "efectul asupra acțiunilor din Stoxx 600 s-a atenuat cu circa 60\\%, cel asupra swapurilor pe riscul de credit pe 5 ani a rămas pozitiv"),
         t("volatile months: AUC 0.731 for EFRM + CISS, 0.708 EFRM alone, 0.673 CISS alone",
           "lunile volatile: AUC 0{,}731 pentru EFRM + CISS, 0{,}708 doar EFRM, 0{,}673 doar CISS")),
        sep="1pt") + note(t("Findings as stated by the authors; talk: \\href{" + TALK_TOMA + "}{slides}; paper: \\href{https://doi.org/10.2139/ssrn.6985301}{doi:10.2139/ssrn.6985301}.",
                            "Rezultatele sînt cele raportate de autori; prezentarea: \\href{" + TALK_TOMA + "}{diapozitive}; lucrarea: \\href{https://doi.org/10.2139/ssrn.6985301}{doi:10.2139/ssrn.6985301}.")) +
        D.bottom(t("a firm's own VaR cannot see contagion; read a sector meter next to it.",
                   "VaR proprie a unei firme nu vede contagiunea; urmăriți alături de ea un indicator sectorial.")),
        "footnotesize", cite=t("(Toma, AIDA, ASE, 3 June 2026; Toma, Dima, Grecu, Pele \\& Lessmann, 2026, SSRN)", "(Toma, AIDA, ASE, 3 iunie 2026; Toma, Dima, Grecu, Pele \\& Lessmann, 2026, SSRN)"))

    # ------------------------------------------------------------------ AIDA 2026: carbon risk dynamics (same LASSO meter, high- vs low-carbon firms)
    D.frame(t("AIDA 2026: the tail risk of carbon-heavy firms predicts the low-carbon premium",
              "AIDA 2026: riscul extrem al firmelor poluante anticipă prima de carbon"), it(
        (t("\\textbf{What the work did} (Prof.\\ Wolfgang Karl Härdle, AIDA, 5 June 2026; with R.\\ Wang and L.\\ Zhang)",
           "\\textbf{Ce a făcut lucrarea} (prof.\\ Wolfgang Karl Härdle, AIDA, 5 iunie 2026; cu R.\\ Wang și L.\\ Zhang)"),
         t("carbon premium puzzle: do high-carbon firms earn more (risk compensation) or low-carbon firms (green preference)?",
           "puzzle-ul primei de carbon: cîștigă mai mult firmele poluante (risc) sau cele cu emisii reduse (preferințe verzi)?"),
         t("China, July 2014 -- February 2025: 50 high-carbon and 50 low-carbon firms; LASSO regressions as for the EFRM, 63 days, 5\\% quantile",
           "China, iul.\\ 2014 -- feb.\\ 2025: cîte 50 de firme poluante și cu emisii reduse; LASSO ca la EFRM, 63 de zile, cuantila de 5\\%"),
         t("carbon risk dynamic indicator (CARDI) = Financial Risk Meter (FRM, mean penalty $\\lambda$), high-carbon / low-carbon firms",
           "indicatorul dinamic al riscului de carbon (CARDI) = indicatorul de risc financiar (FRM, $\\lambda$ mediu), firme poluante / cu emisii reduse")),
        (t("\\textbf{What it found}", "\\textbf{Ce a găsit}"),
         t("high-risk regimes of CARDI coincide with unexpected or early-stage climate-policy events",
           "regimurile de risc ridicat ale CARDI coincid cu evenimente neașteptate sau incipiente ale politicii climatice"),
         t("a rising CARDI predicts a higher factor-adjusted low-carbon premium next month (0.022, 118 months); the conditional VaR ratio does not",
           "creșterea CARDI anticipă o primă ajustată mai mare a firmelor cu emisii reduse luna următoare (0{,}022, 118 luni); raportul VaR condiționate nu"),
         t("long low-carbon, short high-carbon only when CARDI rises (2015--2024): 115.84\\%, Sharpe 0.72 (always on: 89.03\\%, 0.49)",
           "long pe firmele cu emisii reduse, short pe cele poluante doar cînd CARDI crește (2015--2024): 115{,}84\\%, Sharpe 0{,}72 (permanent: 89{,}03\\%, 0{,}49)")),
        t("\\textbf{Link to this lecture}: the EFRM of the previous frame, split by carbon intensity",
          "\\textbf{Legătura cu acest curs}: EFRM din cadrul anterior, separat după intensitatea emisiilor"),
        sep="1pt") + note(t("Findings as stated by the authors; talk: \\href{" + TALK_WANG + "}{slides}; paper: \\href{" + DOI_WANG + "}{doi:10.2139/ssrn.5757742}.",
                            "Rezultatele sînt cele raportate de autori; prezentarea: \\href{" + TALK_WANG + "}{diapozitive}; lucrarea: \\href{" + DOI_WANG + "}{doi:10.2139/ssrn.5757742}.")) +
        D.bottom(t("in an oil and gas firm, watch CARDI: when it rises, investors favour low-carbon peers.",
                   "într-o firmă de petrol și gaze, urmăriți CARDI: cînd crește, investitorii preferă firmele cu emisii reduse.")),
        "footnotesize", cite=t("(Wang, Härdle \\& Zhang, AIDA, ASE, 5 June 2026; 2025, SSRN)", "(Wang, Härdle \\& Zhang, AIDA, ASE, 5 iunie 2026; 2025, SSRN)"))

    # ------------------------------------------------------------------ 6 case study autumn 2026
    D.section(t("Case study: the price rise of autumn 2026", "Studiu de caz: creșterea prețurilor din toamna anului 2026"))
    D.chart(t("Case study: in 2026 the price doubled gradually, without jumps",
              "Studiu de caz: în 2026 prețul s-a dublat treptat, fără salturi"), "case2026", [
        t(("Monthly mean @{case.p_jun|.2f} EUR/MWh in June, @{case.p_oct|.2f} in October; peak @{case.p_max|.2f} (@{case.p_max_date|date})",
           "99\\% VaR exceedances in @{case.n} days (@{case.exp99|.1f} expected): FHS @{case.fhs.x99}, HS @{case.hs.x99}, normal @{case.normal.x99}"),
          ("Media lunară: @{case.p_jun|.2f} EUR/MWh în iunie, @{case.p_oct|.2f} în octombrie; maximul: @{case.p_max|.2f} EUR/MWh (@{case.p_max_date|date})",
           "depășiri ale VaR de 99\\% în @{case.n} " + de("case.n") + "zile (@{case.exp99|.1f} așteptate): FHS @{case.fhs.x99}, HS @{case.hs.x99}, normală @{case.normal.x99}"))],
        height="0.52\\textheight",
        job=t("a slow rise passes the VaR tests and still drains cash: watch the price level too.",
              "o creștere lentă trece testele VaR, dar consumă lichidități: urmăriți și nivelul prețului."),
        tryit=NB + " \\S8", cite=t("(own estimates; OPCOM)", "(estimări proprii; OPCOM)"))

    D.frame(t("Case study: market risk and liquidity needs in 2026", "Studiu de caz: riscul de piață și nevoia de lichidități în 2026"), cols(
        it((t("\\textbf{Market risk barely moved}", "\\textbf{Riscul de piață aproape nu s-a modificat}"),
            t("FHS 99\\% VaR: @{case.fhs_jun|.2f} EUR/MWh in June, @{case.fhs_oct|.2f} in October", "VaR FHS de 99\\%: @{case.fhs_jun|.2f} EUR/MWh în iunie, @{case.fhs_oct|.2f} în octombrie"),
            t("ES test since 2023, FHS: $Z_2$ = @{case.z2_after_fhs|.3f}, not rejected", "testul ES din 2023, FHS: $Z_2$ = @{case.z2_after_fhs|.3f}, ipoteza nu este respinsă")),
           (t("\\textbf{Cash needs doubled}", "\\textbf{Nevoia de lichidități s-a dublat}"),
            t("day-ahead guarantee for 100 MW (widened 99\\% quantile): @{case.g_jun|.3f} $\\to$ @{case.g_oct|.3f} million EUR per day",
              "garanția pentru 100 MW pe piața pentru ziua următoare (cuantila de 99\\% lărgită): @{case.g_jun|.3f} $\\to$ @{case.g_oct|.3f} milioane EUR pe zi"),
            t("orders above the guarantee limit: @{case.g_miss} days (@{case.qr_miss} without widening)", "zile cu prețul peste limita garanției: @{case.g_miss} (@{case.qr_miss} fără lărgire)")), sep="3pt"),
        it((t("\\textbf{The supplier's monthly bill}, 100 MW", "\\textbf{Factura lunară a furnizorului}, 100 MW"),
            t("August +@{case.o_08|.1f}\\% (@{case.eur_08|.2f} million EUR), September +@{case.o_09|.1f}\\% (@{case.eur_09|.2f}), October +@{case.o_10|.1f}\\% (@{case.eur_10|.2f})",
              "august: +@{case.o_08|.1f}\\% (@{case.eur_08|.2f} milioane EUR); septembrie: +@{case.o_09|.1f}\\% (@{case.eur_09|.2f}); octombrie: +@{case.o_10|.1f}\\% (@{case.eur_10|.2f})"),
            t("each month below the 99\\% limit of +@{case.lim99|.1f}\\%, but three in a row", "fiecare lună sub limita de 99\\% de +@{case.lim99|.1f}\\%, dar trei luni la rînd")),
           (t("\\textbf{Drivers}", "\\textbf{Factorii}"),
            t("TTF gas @{case.ttf_jun|.2f} $\\to$ @{case.ttf_oct|.2f} EUR/MWh (June $\\to$ October)", "gazele TTF: @{case.ttf_jun|.2f} $\\to$ @{case.ttf_oct|.2f} EUR/MWh (iunie $\\to$ octombrie)"),
            t("Brent @{case.brent_oct|.2f} USD in October; Germany--Luxembourg @{case.de_oct|.2f} EUR/MWh", "Brent: @{case.brent_oct|.2f} USD în octombrie; Germania--Luxemburg: @{case.de_oct|.2f} EUR/MWh")), sep="3pt"),
        "0.50", "0.47") + D.bottom(t("a risk report needs a liquidity line next to VaR: guarantees, margins and the cumulative monthly overrun.",
                                     "un raport de risc are nevoie, alături de VaR, de o secțiune de lichiditate: garanții, marje și depășirea cumulată a costului lunar."), NB + " \\S8"),
        "footnotesize", cite=t("(own estimates; OPCOM; World Bank; Yahoo Finance)", "(estimări proprii; OPCOM; Banca Mondială; Yahoo Finance)"))

    D.frame(t("A risk desk checklist for energy prices", "Lista de verificare a biroului de risc pentru prețurile energiei"), cols(
        it((t("\\textbf{Measure}", "\\textbf{Măsurarea}"),
            t("define the position and the sign of the loss (buyer or seller)", "definiți poziția și semnul pierderii (cumpărător sau vînzător)"),
            t("use only data known at gate closure", "folosiți numai datele cunoscute la închiderea licitației"),
            t("report VaR and ES from two methods, one of them filtered (FHS or EVT)", "raportați VaR și ES obținute prin două metode, dintre care una filtrată (FHS sau EVT)")),
           (t("\\textbf{Check}", "\\textbf{Verificarea}"),
            t("Kupiec, Christoffersen and the traffic light on several years, including 2021--2022", "testele Kupiec și Christoffersen și semaforul Basel pe mai mulți ani, inclusiv 2021--2022"),
            t("$Z_2$ for ES; never rank models on a few tail days", "testul $Z_2$ pentru ES; nu ierarhizați modelele pe baza cîtorva zile extreme")), sep="3pt"),
        it((t("\\textbf{Decide}", "\\textbf{Decizia}"),
            t("limits in EUR of VaR, converted daily to MW", "limite exprimate în EUR de VaR, transformate zilnic în MW"),
            t("guarantees and credit lines from calibrated high quantiles", "garanții și linii de credit calculate din cuantile ridicate, bine calibrate"),
            t("a cash buffer for the margin a crisis would demand", "o rezervă de lichidități pentru marja cerută într-o criză")),
           (t("\\textbf{Report}", "\\textbf{Raportarea}"),
            t("in EUR and in MW, by month, with the liquidity next to the market risk", "în EUR și în MW, lunar, cu lichiditatea alături de riscul de piață")), sep="3pt"), "0.49", "0.48") +
        D.bottom(t("Assignment 2 (Task 5) applies this checklist to the cash flow of your own role.",
                   "tema 2 (sarcina 5) aplică această listă fluxului de numerar al rolului dumneavoastră.")),
        "footnotesize", cite=t("(BCBS, 2019; EMIR RTS 153/2013; Assignment 2)", "(BCBS, 2019; RTS EMIR 153/2013; tema 2)"))

    # ------------------------------------------------------------------ wrap-up
    D.parts.append("\\section*{" + t("Wrap-up", "Recapitulare") + "}\n")
    D.quiz_frame(t("reading a VaR", "interpretarea VaR"),
                 t("Your 99\\% one-day VaR for 100 MW is @{last.fhs.var99_eur|,.0f} thousand EUR; what does it promise, and what does it not say?",
                   "VaR de 99\\% pe o zi, pentru 100 MW, este de @{last.fhs.var99_eur|,.0f} " + de("last.fhs.var99_eur") + "mii EUR; ce promite această cifră și ce nu spune?"),
                 t("On about 1 day in 100 the loss should exceed it; it says nothing about how large the loss is on those days, which is what ES "
                   "(@{last.fhs.es975_eur|,.0f} thousand EUR at 97.5\\%) measures.",
                   "În aproximativ o zi din 100, pierderea ar trebui să o depășească; nu spune nimic despre mărimea pierderii în acele zile, pe care o măsoară ES "
                   "(@{last.fhs.es975_eur|,.0f} " + de("last.fhs.es975_eur") + "mii EUR la 97{,}5\\%)."))
    D.quiz_frame(t("seven exceedances", "șapte depășiri"),
                 t("Over the last 250 days your 99\\% VaR was exceeded 7 times; what zone is it in, and what does Kupiec say?",
                   "În ultimele 250 de zile, VaR de 99\\% a fost depășită de 7 ori; în ce zonă a semaforului se află modelul și ce arată testul Kupiec?"),
                 t("Yellow (5--9); LR$_{uc}$ = @{quiz.k7_lr|.2f}, $p$ = @{quiz.k7_p|.3f}: rejected at 5\\%; recalibrate (e.g.\\ move from HS to FHS) and keep watching.",
                   "Zona galbenă (5--9); LR$_{uc}$ = @{quiz.k7_lr|.2f}, $p$ = @{quiz.k7_p|.3f}: ipoteza este respinsă la pragul de 5\\%; recalibrați modelul (de exemplu, treceți de la HS la FHS) și continuați monitorizarea."))
    D.quiz_frame(t("ten days", "zece zile"),
                 t("Your chief financial officer computes the 10-day VaR as $\\sqrt{10}$ times the 1-day VaR; is that prudent or wasteful for power?",
                   "Directorul financiar calculează VaR pe 10 zile ca $\\sqrt{10}$ înmulțit cu VaR pe o zi; este o abordare prudentă sau risipitoare pentru energie?"),
                 t("Wasteful: power prices revert, and the empirical 10-day 99\\% quantile is only @{horizon.ro10|.2f} times the 1-day one in Romania, not @{horizon.sqrt10|.2f}.",
                   "Risipitoare: prețurile energiei revin spre medie, iar cuantila empirică de 99\\% pe 10 zile este doar de @{horizon.ro10|.2f} ori cea pe o zi în România, nu de @{horizon.sqrt10|.2f} ori."))
    D.quiz_frame(t("a margin call", "un apel în marjă"),
                 t("You sold 100 lots of Brent to hedge your production; today the price rises by 5 USD per barrel; what happens tonight?",
                   "Ați vîndut 100 de loturi Brent pentru a vă acoperi producția; astăzi prețul crește cu 5 USD pe baril; ce se întîmplă diseară?"),
                 t("You pay a variation margin of 100 $\\times$ 1,000 $\\times$ 5 = 500,000 USD in cash; the physical oil you sell later is worth more, but the cash leaves today.",
                   "Plătiți o marjă de variație de 100 $\\times$ 1.000 $\\times$ 5 = 500.000 USD în numerar; țițeiul pe care îl veți vinde mai tîrziu valorează mai mult, dar banii pleacă astăzi."))
    D.quiz_frame(t("a guarantee that is too small", "o garanție prea mică"),
                 t("Your 99\\% quantile forecast of tomorrow's price was exceeded on @{guar.a99.qr.miss} days out of @{guar.a99.n|,d}; what do you do?",
                   "Prognoza dumneavoastră pentru cuantila de 99\\% a prețului de mîine a fost depășită în @{guar.a99.qr.miss} " + de("guar.a99.qr.miss") + "zile din @{guar.a99.n|,d}; ce faceți?"),
                 t("Widen the tail with a conformal correction from recent errors: coverage rises from @{guar.a99.qr.cov|.2f}\\% to @{guar.a99.cqr.cov|.2f}\\% for @{guar.a99.extra_cost_pct|.1f}\\% more guarantee.",
                   "Lărgiți coada cu o corecție conformală calculată din erorile recente: acoperirea crește de la @{guar.a99.qr.cov|.2f}\\% la @{guar.a99.cqr.cov|.2f}\\%, cu o garanție mai mare cu doar @{guar.a99.extra_cost_pct|.1f}\\%."))

    D.frame(t("Wrap-up", "Recapitulare"), "\\vspace{-2mm}\\begin{multicols}{2}\\scriptsize\\tableofcontents\\end{multicols}\n" + it(
        t("VaR is a quantile, ES the mean beyond it; on power prices the normal curve fails, filtered methods (FHS, EVT) come closest, and none was right in 2021--2022.",
          "VaR este o cuantilă, iar ES media pierderilor de dincolo de ea; pe prețurile energiei, repartiția normală eșuează, metodele filtrate (FHS, EVT) se apropie cel mai mult de țintă și niciuna nu a fost corectă în 2021--2022."),
        t("The same quantiles set limits, margins and guarantees; the 2026 case shows that liquidity, not VaR, is the first casualty. Next: hedging with derivatives (Lecture 5).",
          "Aceleași cuantile stabilesc limite, marje și garanții; studiul de caz din 2026 arată că lichiditatea, nu VaR, este prima afectată; cursul următor: acoperirea riscului cu instrumente derivate (cursul 5)."),
        sep="1pt"))

    D.frame(t("Research from our group on energy risk", "Cercetările grupului nostru despre riscul pe piețele de energie"), it(
        t(("\\textbf{Energy Financial Risk Meter} (Toma, Dima, Grecu, Pele \\& Lessmann, 2026, SSRN)",
           "a systemic-risk indicator for the EU energy sector from LASSO quantile regressions on 100 companies; it captures the 2020 and 2022 shocks (case study C4)"),
          ("\\textbf{Indicatorul de risc financiar al sectorului energetic} (Toma, Dima, Grecu, Pele \\& Lessmann, 2026, SSRN)",
           "ce a făcut lucrarea: a construit un indicator de risc sistemic pentru sectorul energetic din UE, din regresii cuantilice LASSO pe 100 de companii; rezultat: indicatorul surprinde șocurile din 2020 și 2022 (studiul de caz C4)")),
        t(("\\textbf{Foundation models for VaR and ES} (Jheng, Tak, Găman, Mazurencu-Marinescu-Pele \\& Pele, 2026)",
           "data: ten daily return series from five Central and Eastern European (CEE) markets, including Romania, out of sample 2018--2025",
           "method: three pre-trained time-series models, used without fine-tuning, against classical benchmarks; Kupiec, Christoffersen, Acerbi--Székely tests and the Basel traffic light",
           "result: green-zone rate 90\\% for the best raw model, 96.7\\% after a rolling conformal calibration, the highest of all"),
          ("\\textbf{Modele fundaționale pentru VaR și ES} (Jheng, Tak, Găman, Mazurencu-Marinescu-Pele \\& Pele, 2026)",
           "date: zece serii de randamente zilnice din cinci piețe din Europa Centrală și de Est (CEE), inclusiv România, cu evaluare în afara eșantionului în 2018--2025",
           "metodă: trei modele preantrenate pentru serii de timp, folosite fără reantrenare, comparate cu metode clasice; testele Kupiec, Christoffersen, Acerbi--Székely și semaforul Basel",
           "rezultat: 90\\% din ferestre în zona verde pentru cel mai bun model neajustat și 96{,}7\\% după o calibrare conformală glisantă, cel mai bun rezultat dintre toate")),
        t(("\\textbf{How precise is an ES comparison?} (Pele \\& Mazurencu-Marinescu-Pele, 2026, Mathematics)",
           "turns the $(n\\alpha)^{-1/2}$ precision limit of ES into four practical diagnostics, including a sample-size rule",
           "result: on global financial assets about one in five pairwise ES comparisons cannot be trusted at regulatory tail levels"),
          ("\\textbf{Cît de precisă este o comparație a prognozelor ES?} (Pele \\& Mazurencu-Marinescu-Pele, 2026, Mathematics)",
           "ce a făcut lucrarea: a transformat limita de precizie $(n\\alpha)^{-1/2}$ a ES în patru diagnostice practice, inclusiv o regulă pentru mărimea eșantionului",
           "rezultat: pe active financiare globale, aproximativ una din cinci comparații între prognoze ES nu este concludentă la nivelurile de risc cerute de reglementare")),
        sep="3pt") + note(t("Findings as stated in the papers; numbers on the other slides come from our own data.",
                            "Rezultatele de pe acest diapozitiv sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.")),
        "footnotesize", cite=t("(Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting)",
                               "(Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică)"))

    D.frame(t("Want to learn more?", "Lecturi și resurse suplimentare"), cols(it(
        t("\\textbf{McNeil, Frey \\& Embrechts}, \\textit{Quantitative Risk Management}, 2nd ed.: VaR, ES, EVT, backtesting.",
          "\\textbf{McNeil, Frey \\& Embrechts}, \\textit{Quantitative Risk Management}, ed.\\ a 2-a: VaR, ES, EVT, testare retrospectivă."),
        t("\\textbf{Christoffersen}, \\textit{Elements of Financial Risk Management}, 2nd ed.: FHS and backtests, with exercises.",
          "\\textbf{Christoffersen}, \\textit{Elements of Financial Risk Management}, ed.\\ a 2-a: FHS și testare retrospectivă, cu exerciții."),
        t("\\textbf{ECB}, Financial stability risks from energy derivatives markets (2022): ", "\\textbf{BCE}, Financial stability risks from energy derivatives markets (2022): ") +
        "\\href{https://www.ecb.europa.eu/pub/financial-stability/fsr/special/html/ecb.fsrart202211_01~173476301a.en.html}{ecb.europa.eu}.", sep="4pt"),
        it(t("\\textbf{This course}: code, data, notebooks --- ", "\\textbf{Acest curs}: cod, date, notebook-uri Jupyter --- ") +
           "\\href{https://github.com/danpele/EMQA}{github.com/danpele/EMQA}.",
           t("\\textbf{Assignment 2}, Task 5: VaR and ES of your role's cash flow, with backtests.",
             "\\textbf{Tema 2}, sarcina 5: VaR și ES ale fluxului de numerar al rolului dumneavoastră, cu testare retrospectivă."),
           t("\\textbf{OPCOM}, day-ahead guarantee procedure: ", "\\textbf{OPCOM}, procedura privind garanțiile pentru PZU: ") +
           "\\href{https://www.opcom.ro}{opcom.ro}.",
           t("\\textbf{Experiment yourself}: the notebook reproduces every chart and number of this lecture --- ",
             "\\textbf{Exercițiu practic}: notebook-ul Jupyter reproduce toate graficele și cifrele din acest curs --- ") +
           "\\href{\\emqarepo/\\emqanb}{notebooks/}.", sep="4pt"), "0.52", "0.45"))

    REFS = [
        "Acerbi, C.\\ \\& Székely, B.\\ (2014). Backtesting expected shortfall. \\textit{Risk}, 27(11), 76--81. "
        "\\href{https://www.risk.net/risk-magazine/technical-paper/2381658/back-testing-expected-shortfall}{risk.net}",
        "Acerbi, C.\\ \\& Tasche, D.\\ (2002). On the coherence of expected shortfall. \\textit{Journal of Banking \\& Finance}, 26(7), 1487--1503. "
        "\\href{https://doi.org/10.1016/S0378-4266(02)00283-2}{doi:10.1016/S0378-4266(02)00283-2}",
        "Artzner, P., Delbaen, F., Eber, J.-M.\\ \\& Heath, D.\\ (1999). Coherent measures of risk. \\textit{Mathematical Finance}, 9(3), 203--228. "
        "\\href{https://doi.org/10.1111/1467-9965.00068}{doi:10.1111/1467-9965.00068}",
        "Balkema, A.\\,A.\\ \\& de Haan, L.\\ (1974). Residual life time at great age. \\textit{Annals of Probability}, 2(5), 792--804. "
        "\\href{https://doi.org/10.1214/aop/1176996548}{doi:10.1214/aop/1176996548}",
        "Barone-Adesi, G., Giannopoulos, K.\\ \\& Vosper, L.\\ (1999). VaR without correlations for portfolios of derivative securities. "
        "\\textit{Journal of Futures Markets}, 19(5), 583--602. "
        "\\href{https://doi.org/10.1002/(SICI)1096-9934(199908)19:5\\%3C583::AID-FUT5\\%3E3.0.CO;2-S}{doi.org (Wiley)}",
        "BCBS (1996). Supervisory framework for the use of ``backtesting'' in conjunction with the internal models approach to market risk "
        "capital requirements. Basel Committee on Banking Supervision, January 1996. \\href{https://www.bis.org/publ/bcbs22.htm}{bis.org/publ/bcbs22.htm}",
        "BCBS (2019). Minimum capital requirements for market risk. Basel Committee on Banking Supervision, January 2019. "
        "\\href{https://www.bis.org/bcbs/publ/d457.htm}{bis.org/bcbs/publ/d457.htm}",
        "Bollerslev, T.\\ (1986). Generalized autoregressive conditional heteroskedasticity. \\textit{Journal of Econometrics}, 31(3), 307--327. "
        "\\href{https://doi.org/10.1016/0304-4076(86)90063-1}{doi:10.1016/0304-4076(86)90063-1}",
        "Chan, K.\\,F.\\ \\& Gray, P.\\ (2006). Using extreme value theory to measure value-at-risk for daily electricity spot prices. "
        "\\textit{International Journal of Forecasting}, 22(2), 283--300. \\href{https://doi.org/10.1016/j.ijforecast.2005.10.002}{doi:10.1016/j.ijforecast.2005.10.002}",
        "Christoffersen, P.\\,F.\\ (1998). Evaluating interval forecasts. \\textit{International Economic Review}, 39(4), 841--862. "
        "\\href{https://doi.org/10.2307/2527341}{doi:10.2307/2527341}",
        "Christoffersen, P.\\,F.\\ (2012). \\textit{Elements of Financial Risk Management}, 2nd ed. Academic Press. "
        "\\href{https://shop.elsevier.com/books/elements-of-financial-risk-management/christoffersen/978-0-12-374448-7}{elsevier.com}",
        "Commission Delegated Regulation (EU) No 153/2013 of 19 December 2012 on requirements for central counterparties (RTS under EMIR), "
        "\\textit{Official Journal of the EU}, L 52, 23.2.2013, Art.~24--28. \\href{https://eur-lex.europa.eu/eli/reg_del/2013/153/oj}{eur-lex.europa.eu/eli/reg\\_del/2013/153/oj}",
        "Commission Delegated Regulation (EU) 2022/2311 of 21 October 2022 as regards temporary emergency measures on collateral requirements. "
        "\\textit{Official Journal of the EU}, L 307, 28.11.2022. \\href{https://eur-lex.europa.eu/eli/reg_del/2022/2311/oj}{eur-lex.europa.eu/eli/reg\\_del/2022/2311/oj}",
        "ECB --- Furtuna, O., Grassi, A., Ianiro, A., Kallage, K., Koci, R., Lenoci, F., Sowiński, A.\\ \\& Vacirca, F.\\ (2022). Financial stability "
        "risks from energy derivatives markets. \\textit{Financial Stability Review}, European Central Bank, November 2022. "
        "\\href{https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202211_01~173476301a.en.html}{ecb.europa.eu}",
        "Gneiting, T.\\ (2011). Making and evaluating point forecasts. \\textit{Journal of the American Statistical Association}, 106(494), 746--762. "
        "\\href{https://doi.org/10.1198/jasa.2011.r10138}{doi:10.1198/jasa.2011.r10138}",
        "Jheng, S.-L., Tak, R., Găman, Ș., Mazurencu-Marinescu-Pele, M.\\ \\& Pele, D.\\,T.\\ (2026). Can foundation models manage risk? Zero-shot VaR "
        "and ES forecasting with conformal calibration in CEE markets. \\textit{Economic Computation and Economic Cybernetics Studies and Research}, "
        "60(2), 267--290. \\href{https://doi.org/10.24818/18423264/60.2.26.14}{doi:10.24818/18423264/60.2.26.14}",
        "Jorion, P.\\ (2007). \\textit{Value at Risk: The New Benchmark for Managing Financial Risk}, 3rd ed. McGraw-Hill. "
        "\\href{https://www.mheducation.com.au/ebook-value-at-risk-the-new-benchmark-for-managing-financial-risk-3e-9781307199963-aus}{mheducation.com.au}",
        "Koenker, R.\\ \\& Bassett, G.\\ (1978). Regression quantiles. \\textit{Econometrica}, 46(1), 33--50. "
        "\\href{https://doi.org/10.2307/1913643}{doi:10.2307/1913643}",
        "Kupiec, P.\\,H.\\ (1995). Techniques for verifying the accuracy of risk measurement models. \\textit{Journal of Derivatives}, 3(2), 73--84. "
        "\\href{https://doi.org/10.3905/jod.1995.407942}{doi:10.3905/jod.1995.407942}",
        "McNeil, A.\\,J.\\ \\& Frey, R.\\ (2000). Estimation of tail-related risk measures for heteroscedastic financial time series: An extreme value "
        "approach. \\textit{Journal of Empirical Finance}, 7(3--4), 271--300. \\href{https://doi.org/10.1016/S0927-5398(00)00012-8}{doi:10.1016/S0927-5398(00)00012-8}",
        "McNeil, A.\\,J., Frey, R.\\ \\& Embrechts, P.\\ (2015). \\textit{Quantitative Risk Management: Concepts, Techniques and Tools}, revised ed. Princeton University Press. "
        "\\href{https://press.princeton.edu/books/hardcover/9780691166278/quantitative-risk-management}{press.princeton.edu}",
        "Nowotarski, J.\\ \\& Weron, R.\\ (2018). Recent advances in electricity price forecasting: A review of probabilistic forecasting. "
        "\\textit{Renewable and Sustainable Energy Reviews}, 81, 1548--1568. \\href{https://doi.org/10.1016/j.rser.2017.05.234}{doi:10.1016/j.rser.2017.05.234}",
        "OPCOM (2025). Procedura privind constituirea, verificarea și utilizarea garanțiilor financiare pentru participarea la Piața pentru Ziua "
        "Următoare, rev.\\ 10, May 2025. \\href{https://www.opcom.ro}{opcom.ro}",
        "Pele, D.\\,T.\\ \\& Mazurencu-Marinescu-Pele, M.\\ (2026). Finite-sample precision limits for expected shortfall forecast comparisons. "
        "\\textit{Mathematics}, 14(13), 2316. \\href{https://doi.org/10.3390/math14132316}{doi:10.3390/math14132316}",
        "Pele, D.\\,T., Bolovăneanu, V., Ginavar, A.\\,T., Lessmann, S.\\ \\& Härdle, W.\\,K.\\ (2026). Recalibrating tail risk forecasts under temporal "
        "dependence: conformal audit of foundation models for VaR forecasting. AIDA Conference, Bucharest University of Economic Studies, 4 June 2026. "
        "\\href{" + TALK_PELE + "}{github.com/danpele/EMQA/resources/aida2026}",
        "Pickands, J.\\ (1975). Statistical inference using extreme order statistics. \\textit{Annals of Statistics}, 3(1), 119--131. "
        "\\href{https://doi.org/10.1214/aos/1176343003}{doi:10.1214/aos/1176343003}",
        "Romano, Y., Patterson, E.\\ \\& Candès, E.\\ (2019). Conformalized quantile regression. \\textit{Advances in Neural Information Processing "
        "Systems}, 32, 3543--3553. \\href{https://proceedings.neurips.cc/paper/2019/hash/5103c3584b063c431bd1268e9b5e76fb-Abstract.html}{proceedings.neurips.cc}",
        "Toma, F.-M., Dima, D.-M., Grecu, R., Pele, D.\\,T.\\ \\& Lessmann, S.\\ (2026). Energy Financial Risk Meter: Systemic risk in the EU energy "
        "sector. SSRN Working Paper 6985301. \\href{https://doi.org/10.2139/ssrn.6985301}{doi:10.2139/ssrn.6985301}",
        "Toma, F.-M.\\ (2026). Energy Financial Risk Meter: systemic risk in the EU energy sector (with D.-M.\\ Dima, R.\\ Grecu, D.\\,T.\\ Pele and S.\\ Lessmann). "
        "AIDA Conference, Bucharest University of Economic Studies, 3 June 2026. \\href{" + TALK_TOMA + "}{github.com/danpele/EMQA/resources/aida2026}",
        "Wang, R., Härdle, W.\\,K.\\ \\& Zhang, L.\\ (2025). Measuring carbon risk dynamics. SSRN Working Paper 5757742. "
        "\\href{" + DOI_WANG + "}{doi:10.2139/ssrn.5757742}",
        "Wang, R., Härdle, W.\\,K.\\ \\& Zhang, L.\\ (2026). Measuring carbon risk dynamics. "
        "AIDA Conference, Bucharest University of Economic Studies, 5 June 2026. \\href{" + TALK_WANG + "}{github.com/danpele/EMQA/resources/aida2026}",
        "Weron, R.\\ (2014). Electricity price forecasting: A review of the state-of-the-art with a look into the future. "
        "\\textit{International Journal of Forecasting}, 30(4), 1030--1081. \\href{https://doi.org/10.1016/j.ijforecast.2014.08.008}{doi:10.1016/j.ijforecast.2014.08.008}",
    ]
    for part, (a_, b_) in enumerate([(0, 9), (9, 17), (17, 25), (25, len(REFS))]):
        D.frame(t("References", "Bibliografie") + f" ({part + 1}/4)", "\\begin{itemize}\\setlength{\\itemsep}{1pt}\\scriptsize\n" +
                "\n".join("\\item " + r for r in REFS[a_:b_]) + "\n\\end{itemize}", "scriptsize")

    # ------------------------------------------------------------------ appendix
    D.mark_main_end()
    D.parts.append("\\section*{" + t("Appendix", "Anexă") + "}\n")
    D.frame(t("Appendix A: ES of the normal and Student-$t$ distributions", "Anexa A: ES pentru repartițiile normală și Student-$t$"), cols(
        "\\[ \\text{ES}^{N}_\\alpha=\\frac{1}{1-\\alpha}\\int_{z_\\alpha}^{\\infty}(\\mu+\\sigma z)\\varphi(z)\\,dz=\\mu+\\sigma\\frac{\\varphi(z_\\alpha)}{1-\\alpha} \\]" + it(
            t("Because $\\int_{c}^{\\infty}z\\varphi(z)\\,dz=\\varphi(c)$ (the derivative of $\\varphi$ is $-z\\varphi$).",
              "Deoarece $\\int_{c}^{\\infty}z\\varphi(z)\\,dz=\\varphi(c)$ (derivata lui $\\varphi$ este $-z\\varphi$)."),
            t("At $\\alpha$ = 0.975, ES$^N$ = $\\mu$ + 2.338$\\sigma$, almost VaR$^N_{0.99}$ = $\\mu$ + 2.326$\\sigma$: this is why FRTB swapped one for the other.",
              "La $\\alpha$ = 0{,}975, ES$^N$ = $\\mu$ + 2{,}338$\\sigma$, aproape egal cu VaR$^N_{0{,}99}$ = $\\mu$ + 2{,}326$\\sigma$: de aceea FRTB a înlocuit o măsură cu cealaltă."), sep="3pt"),
        "\\[ \\text{ES}^{t}_\\alpha=m+s\\,\\frac{g_\\nu(t_{\\nu,\\alpha})}{1-\\alpha}\\cdot\\frac{\\nu+t_{\\nu,\\alpha}^{2}}{\\nu-1},\\quad \\nu>1 \\]" + it(
            t("From $\\int_c^\\infty x\\,g_\\nu(x)\\,dx=g_\\nu(c)\\,(\\nu+c^2)/(\\nu-1)$; for $\\nu\\le 1$ the mean, hence ES, does not exist.",
              "Din $\\int_c^\\infty x\\,g_\\nu(x)\\,dx=g_\\nu(c)\\,(\\nu+c^2)/(\\nu-1)$; pentru $\\nu\\le 1$ media, deci și ES, nu există."),
            t("We fit $(m,s,\\nu)$ by MLE every day; $\\nu$ is kept at least 2.2 so that the variance exists.",
              "Estimăm zilnic $(m,s,\\nu)$ prin MLE; $\\nu$ este menținut cel puțin la 2{,}2, pentru ca varianța să existe."), sep="3pt"), "0.49", "0.48"),
        "small", cite="(McNeil, Frey \\& Embrechts, 2015, ch.~2)")

    D.frame(t("Appendix B: VaR and ES from the generalised Pareto tail", "Anexa B: VaR și ES din coada Pareto generalizată"), cols(
        "\\[ \\Pr(Z>z)\\approx\\frac{N_u}{n}\\Big(1+\\xi\\frac{z-u}{\\beta}\\Big)^{-1/\\xi},\\quad z>u \\]"
        "\\[ \\Pr(Z>\\text{VaR}_\\alpha)=1-\\alpha\\ \\Rightarrow \\]\\vspace{-2mm}\\[ \\text{VaR}_\\alpha=u+\\frac{\\beta}{\\xi}\\Big[\\Big(\\frac{n(1-\\alpha)}{N_u}\\Big)^{-\\xi}-1\\Big] \\]" + it(
            t("Pickands--Balkema--de Haan: for a high $u$, excesses over $u$ are approximately GPD for almost all distributions.",
              "Teorema Pickands--Balkema--de Haan: pentru un prag $u$ ridicat, excesele peste $u$ urmează aproximativ o repartiție GPD, pentru aproape orice repartiție."), sep="3pt"),
        "\\[ \\E[Z-v\\mid Z>v]=\\frac{\\beta+\\xi(v-u)}{1-\\xi} \\]\\vspace{-2mm}\\[ \\Rightarrow\\ \\text{ES}_\\alpha=\\frac{\\text{VaR}_\\alpha+\\beta-\\xi u}{1-\\xi} \\]" + it(
            t("The mean excess is linear in $v$ for the GPD (needs $\\xi<1$); $\\xi>0$ = heavy tail, $\\xi=0$ = exponential, $\\xi<0$ = bounded tail.",
              "Excesul mediu este liniar în $v$ pentru GPD (cu condiția $\\xi<1$); $\\xi>0$ = coadă groasă, $\\xi=0$ = coadă exponențială, $\\xi<0$ = coadă mărginită."),
            t("Conditional EVT: apply this to $z_t=e_t/\\sigma_t$, then VaR$_t=\\mu_{d(t)}+\\sigma_t\\,$VaR$^z_\\alpha$.",
              "EVT condiționată: aplicăm formula lui $z_t=e_t/\\sigma_t$, apoi VaR$_t=\\mu_{d(t)}+\\sigma_t\\,$VaR$^z_\\alpha$."), sep="3pt"), "0.50", "0.47"),
        "small", cite="(Pickands, 1975; Balkema \\& de Haan, 1974; McNeil \\& Frey, 2000)")

    D.frame(t("Appendix C: the three backtests in full", "Anexa C: cele trei teste retrospective, în detaliu"), cols(
        it(t(("\\textbf{Kupiec and Christoffersen}", "under $H_0$ each $I_t$ is Bernoulli($p$), independent; LR$_{uc}$ compares $p$ with $\\hat p$",
              "LR$_{ind}$ compares a first-order Markov chain with independence; LR$_{cc}$ = LR$_{uc}$ + LR$_{ind}\\sim\\chi^2_2$, 5\\% critical value 5.99"),
             ("\\textbf{Kupiec și Christoffersen}", "în ipoteza $H_0$, fiecare $I_t$ este o variabilă Bernoulli($p$), independentă; LR$_{uc}$ compară $p$ cu $\\hat p$",
              "LR$_{ind}$ compară un lanț Markov de ordinul întîi cu ipoteza de independență; LR$_{cc}$ = LR$_{uc}$ + LR$_{ind}\\sim\\chi^2_2$, valoarea critică la 5\\%: 5{,}99")),
           t(("\\textbf{Basel traffic light}", "$x\\sim$ Binomial(250, 0.01) for a correct model",
              "$\\Pr(x\\le4)$ = @{basel.p_green|.2f}\\%, $\\Pr(5\\le x\\le9)$ = @{basel.p_yellow|.2f}\\%, $\\Pr(x\\ge10)$ = @{basel.p_red|.3f}\\%"),
             ("\\textbf{Semaforul Basel}", "$x\\sim$ Binomial(250; 0{,}01) pentru un model corect",
              "$\\Pr(x\\le4)$ = @{basel.p_green|.2f}\\%, $\\Pr(5\\le x\\le9)$ = @{basel.p_yellow|.2f}\\%, $\\Pr(x\\ge10)$ = @{basel.p_red|.3f}\\%")), sep="3pt"),
        it(t(("\\textbf{Acerbi--Székely $Z_2$}", "since $\\E[L_tI_t]=(1-\\alpha)\\text{ES}_t$ when VaR and ES are correct, $\\E[Z_2]=0$",
              "$Z_2$ mixes a VaR error (wrong count of $I_t$) and an ES error (wrong size); ES alone is not elicitable, so it is tested together with VaR",
              "our $p$-value: 2,000 simulated paths, each day drawn from that model's predictive distribution (HS: the window; FHS: $\\mu+\\sigma z^*$; EVT: GPD above $u$)"),
             ("\\textbf{Testul Acerbi--Székely $Z_2$}", "deoarece $\\E[L_tI_t]=(1-\\alpha)\\text{ES}_t$ atunci cînd VaR și ES sînt corecte, $\\E[Z_2]=0$",
              "$Z_2$ combină o eroare de VaR (numărul greșit de $I_t$) cu o eroare de ES (mărimea greșită); ES nu este elicitabil, de aceea se testează împreună cu VaR",
              "valoarea $p$: 2.000 de traiectorii simulate, fiecare zi fiind extrasă din repartiția prognozată de modelul respectiv (HS: fereastra; FHS: $\\mu+\\sigma z^*$; EVT: GPD peste $u$)")), sep="3pt"), "0.49", "0.48"),
        "footnotesize", cite="(Kupiec, 1995; Christoffersen, 1998; BCBS, 1996; Acerbi \\& Székely, 2014)")

    def drow(m):
        r95, r99 = BT["DE_LU"][m]["a95"], BT["DE_LU"][m]["a99"]
        return [MN[m], fmt(r95["rate"], ".2f", lang), pval(f"bt.DE_LU.{m}.a95.p_uc"), f"{r99['x']}", fmt(r99["rate"], ".2f", lang),
                pval(f"bt.DE_LU.{m}.a99.p_uc"), pval(f"bt.DE_LU.{m}.a99.p_ind"), fmt(r99["share_red"], ".1f", lang),
                fmt(BT["DE_LU"][m]["z2"]["all"]["z2"], ".3f", lang), pval(f"bt.DE_LU.{m}.z2.all.p")]
    D.frame(t("Appendix D: the same backtest for Germany--Luxembourg", "Anexa D: aceeași testare retrospectivă pentru Germania--Luxemburg"),
            "\\begin{center}" + table("@{}lrrrrrrrrr@{}", [t("DE-LU", "DE-LU"), t("95\\%: share", "95\\%: proporția"), "Kupiec $p$",
                                                          t("99\\%: count", "99\\%: număr"), t("share", "proporția"), "Kupiec $p$", "Chr.\\ $p$",
                                                          t("red, \\%", "roșu, \\%"), "$Z_2$", "$p$"],
                                      [drow(m) for m in METHODS], size="footnotesize", stretch="1.2") + "\\end{center}" +
            note(t(BTP[0].upper() + BTP[1:] + ", @{bt.DE_LU.fhs.a99.n|,d} days; same methods and windows as for Romania.",
                   BTP[0].upper() + BTP[1:] + ", @{bt.DE_LU.fhs.a99.n|,d} " + de("bt.DE_LU.fhs.a99.n") + "zile; aceleași metode și ferestre ca pentru România."),
                 t("The ranking is the same as in Romania: normal worst, filtered methods best.",
                   "Clasamentul este același ca în România: repartiția normală are cele mai slabe rezultate, metodele filtrate cele mai bune.")),
            "small", cite=t("(own estimates; EPEX SPOT)", "(estimări proprii; EPEX SPOT)"))
    return D


def main(langs):
    ok = True
    for lang in langs:
        name = "lecture4" if lang == "en" else "lecture4_ro"
        out = os.path.join(HERE, name + ".tex")
        D, tex, res, H = autofit(build, out, lang)
        print(f"[{lang}] frames: main {D.n_main} (incl. title and section outlines), total {D.n_frames}; quiz frames {D.quiz}; "
              f"pages {res['pages']}; errors {res['errors']}; overfull>1pt {len(res['overfull'])}")
        for kind, amt, title in res["where"]:
            print(f"     {kind} {amt:6.1f}pt  {title}")
        small = {k: v for k, v in D.used_h.items() if v < 0.40}
        print(f"[{lang}] figure heights (fraction of text height) below 0.40:", small)
        defined = set(ABBR) - ({"UE", "BCE"} if lang == "en" else {"EU", "ECB"})
        ign = IGNORE | ({"ECB", "EU"} if lang == "ro" else set())     # English titles in the reference list only
        print(f"[{lang}] acronyms missing from Abbreviations:", acronym_audit(tex, defined, ign))
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
