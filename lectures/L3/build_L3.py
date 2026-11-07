r"""
build_L3.py -- Lecture 3 "Volatility of Energy Prices" (EMQA), English and Romanian from one source
==================================================================================================
Writes lectures/L3/lecture3.tex (EN) and lectures/L3/lecture3_ro.tex (RO) from the bilingual slide text in this file
and the numbers in L3_numbers.json (produced by analysis_L3.py), compiles both with pdflatex and checks: 0 LaTeX errors;
no overfull box > 1 pt (nothing masked); every acronym in the Abbreviations frames and spelled out at first use;
contact sheets for the visual check.

Run (from anywhere):
    python3 lectures/L3/analysis_L3.py
    python3 lectures/L3/build_L3.py            # both languages;  add "en" or "ro" for one

Rules as in Lectures 1-2: no computed number typed by hand (results are @{key} placeholders); hand-typed numbers are
definitions (365 and 252 days, lambda = 0.94, 90% and 95% levels, 1.645, 18.31, sqrt(2/pi), window lengths) and
institutional dates (1 October 2025: 15-minute day-ahead products).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_build import (Numbers, acronym_audit, autofit, cols, contact_sheet,  # noqa: E402
                        first_use_audit, fmt, heat, hier, items, table, Deck)


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
    "AIC": ("Akaike information criterion", "criteriul informațional Akaike"),
    "ARCH": ("autoregressive conditional heteroskedasticity", "heteroscedasticitate condiționată autoregresivă"),
    "ARCH-LM": ("Lagrange multiplier test for ARCH effects", "testul multiplicatorului Lagrange pentru efecte ARCH"),
    "BIC": ("Bayesian (Schwarz) information criterion", "criteriul informațional bayesian (Schwarz)"),
    "BVB": ("Bucharest Stock Exchange", "Bursa de Valori București"),
    "CEE": ("Central and Eastern Europe", None),
    "ECE": (None, "Europa Centrală și de Est"),
    "CET": ("Central European Time", "ora Europei Centrale"),
    "DCC": ("dynamic conditional correlation", "corelație condiționată dinamică"),
    "DE-LU": ("Germany--Luxembourg bidding zone", "zona de ofertare Germania--Luxemburg"),
    "DM": ("Diebold--Mariano test", "testul Diebold--Mariano"),
    "EGARCH": ("exponential GARCH (Nelson)", "GARCH exponențial (Nelson)"),
    "ENTSO-E": ("European Network of Transmission System Operators for Electricity",
                "Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică"),
    "EODHD": ("market data vendor eodhd.com", "furnizorul de date de piață eodhd.com"),
    "ES": ("expected shortfall", "pierderea medie în coada distribuției (expected shortfall)"),
    "ETC": ("exchange-traded commodity", "titlu tranzacționat la bursă, garantat cu mărfuri (exchange-traded commodity)"),
    "EU": ("European Union", None),
    "UE": (None, "Uniunea Europeană"),
    "EUA": ("EU emission allowance (1 t CO$_2$)", "certificat de emisii al UE (1 t CO$_2$)"),
    "EWMA": ("exponentially weighted moving average", "medie mobilă cu ponderi exponențiale"),
    "GARCH": ("generalised autoregressive conditional heteroskedasticity", "heteroscedasticitate condiționată autoregresivă generalizată"),
    "GJR": ("Glosten--Jagannathan--Runkle asymmetric GARCH", "modelul GARCH asimetric Glosten--Jagannathan--Runkle"),
    "H2O": ("Hidroelectrica (BVB ticker)", "Hidroelectrica (simbolul bursier BVB)"),
    "HAR": ("heterogeneous autoregressive model (Corsi)", "modelul autoregresiv eterogen (Corsi)"),
    "HU": ("Hungary (bidding zone)", "Ungaria (zonă de ofertare)"),
    "HUPX": ("Hungarian Power Exchange", "bursa de energie din Ungaria"),
    "ISE": ("Fraunhofer Institute for Solar Energy Systems", "Institutul Fraunhofer pentru Sisteme de Energie Solară"),
    "MAE": ("mean absolute error", "eroarea absolută medie"),
    "MSE": ("mean squared error", "eroarea pătratică medie"),
    "OLS": ("ordinary least squares", "metoda celor mai mici pătrate"),
    "OPCOM": ("Romanian electricity and gas market operator", "operatorul pieței de energie electrică și de gaze naturale din România"),
    "PZU": ("Piața pentru Ziua Următoare (day-ahead market)", "piața pentru ziua următoare"),
    "QLIKE": ("quasi-likelihood loss function", "funcția de pierdere de tip cvasi-verosimilitate"),
    "RO": ("Romania (bidding zone)", "România (zonă de ofertare)"),
    "RV": ("realised intraday variation of the price", "variația intrazilnică realizată a prețului"),
    "SNG": ("Romgaz (BVB ticker)", "Romgaz (simbolul bursier BVB)"),
    "SNN": ("Nuclearelectrica (BVB ticker)", "Nuclearelectrica (simbolul bursier BVB)"),
    "SNP": ("OMV Petrom (BVB ticker)", "OMV Petrom (simbolul bursier BVB)"),
    "TTF": ("Title Transfer Facility (Dutch gas hub)", "Title Transfer Facility (hub olandez de gaze)"),
    "VaR": ("value at risk", "valoarea expusă la risc (value at risk)"),
    "EUR": ("euro", "euro"), "MW": ("megawatt", "megawatt"), "MWh": ("megawatt-hour", "megawatt-oră"),
    "USD": ("United States dollar", "dolar american"), "RON": ("Romanian leu", "leu românesc"),
}
UNITS = {"EUR", "MW", "MWh", "USD", "RON"}
# journal codes and proper names inside citations or tickers only; everything else must be in the Abbreviations list
IGNORE = {"EMQA", "IJF", "ENEECO", "JBES", "JOE", "JFEC", "JFIN", "IER", "OBES", "JAE", "JEP", "NAJEF", "SSRN", "IIF", "SPOT", "CO",
          "II", "OMV", "BZ", "IEEE", "TPWRS", "RESTAT", "EPEX"}


def build(lang, H=None):
    V = Numbers(os.path.join(HERE, "L3_numbers.json"), lang)
    N = V.N
    D = Deck(3, "Volatility of Energy Prices" if lang == "en" else "Volatilitatea prețurilor energiei", V, lang, heights=H)
    t = D.t
    ro = lang == "ro"
    if ro:   # notebook pointer in natural Romanian: "notebook-ul Jupyter, secțiunea 2"
        _tex = D.tex
        D.tex = lambda: _tex().replace("notebook-ul Jupyter \\S", "notebook-ul Jupyter, secțiunea ")
    NB = t("notebook", "notebook-ul Jupyter")

    def de(key):
        v = int(round(float(V.get(key))))
        return "de " if ro and v >= 20 and (v % 100 >= 20 or v % 100 == 0) else ""

    def f(key, spec=".2f"):
        return fmt(V.get(key), spec, lang)

    def pv(key):
        p = V.get(key)
        if p is None:
            return "--"
        if p < 0.001:
            return "$<$0{,}001" if ro else "$<$0.001"
        return fmt(p, ".3f", lang)

    def hl(key):
        v = V.get(key)
        return "$\\infty$" if v is None else fmt(v, ".1f", lang)

    TEST = t("test year @{design.test_start|date} -- @{design.test_end|date}", "anul de test @{design.test_start|date} -- @{design.test_end|date}")
    OWN = t("own estimation", "estimare proprie")
    PANEL = "@{data.y0}--@{data.y1}"

    # ------------------------------------------------------------------ front matter
    D.parts.append("% END-FRONT-MATTER\n")
    D.frame(t("Learning objectives", "Obiectivele cursului"), it(
        (t("\\textbf{Measure volatility correctly}", "\\textbf{Măsurarea corectă a volatilității}"),
         t("percent or EUR/MWh changes of the day-ahead price; the weekly calendar removed first",
           "variații procentuale sau în EUR/MWh ale prețului pentru ziua următoare; mai întîi se elimină efectul zilei din săptămînă"),
         t("what to do when prices approach zero or turn negative", "ce facem cînd prețurile se apropie de zero sau devin negative")),
        (t("\\textbf{Model it}", "\\textbf{Modelarea volatilității}"),
         t("models with generalised autoregressive conditional heteroskedasticity (GARCH), with Student-t shocks",
           "modele cu heteroscedasticitate condiționată autoregresivă generalizată (GARCH), cu șocuri de tip Student"),
         t("persistence, half-life of a shock, asymmetry between price rises and falls",
           "persistența, timpul de înjumătățire al unui șoc, asimetria dintre creșterile și scăderile de preț")),
        (t("\\textbf{Recognise regimes and intraday risk}", "\\textbf{Regimuri de volatilitate și riscul din cursul zilei}"),
         t("calm and turbulent regimes, the 2021--2022 energy crisis, the year 2026", "regimuri calme și agitate; criza energetică din 2021--2022; anul 2026"),
         t("intraday variation of hourly prices and the role of solar generation", "variația prețurilor orare în cursul zilei și rolul producției solare")),
        (t("\\textbf{Forecast and evaluate}", "\\textbf{Prognoza și evaluarea}"),
         t("one day and several weeks ahead; comparison of forecasts with a robust loss function and a significance test",
           "pentru ziua următoare și pentru următoarele săptămîni; compararea prognozelor cu o funcție de pierdere robustă și cu un test de semnificație"),
         t("the answer promised in Lecture 1: how long a risk desk should keep wider limits after a shock",
           "răspunsul promis în cursul 1: cît timp trebuie menținute limite de risc mai largi după un șoc")),
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

    D.frame(t("Real data: Romanian power, fuels, carbon and energy shares", "Folosim numai date reale: energie, combustibili, carbon, acțiuni"), table(
        "@{}p{0.40\\textwidth}p{0.11\\textwidth}p{0.44\\textwidth}@{}",
        [t("Series", "Seria"), t("Frequency", "Frecvența"), t("Source", "Sursa")],
        [[t("Day-ahead price of Romania (RO), Piața pentru Ziua Următoare (PZU); Hungary (HU) and Germany--Luxembourg (DE-LU) for comparison",
            "Prețul pe piața pentru ziua următoare (PZU) din România (RO); pentru comparație, Ungaria (HU) și Germania--Luxemburg (DE-LU)"),
          t("daily, hourly", "zilnică, orară"),
          t("Romanian market operator (OPCOM), Hungarian Power Exchange (HUPX), EPEX SPOT; via energy-charts.info "
            "(Fraunhofer ISE) and the European Network of Transmission System Operators for Electricity (ENTSO-E)",
            "operatorul pieței de energie din România (OPCOM), bursa din Ungaria (HUPX), EPEX SPOT; prin energy-charts.info (Fraunhofer ISE) și "
            "Rețeaua europeană a operatorilor de transport și de sistem (ENTSO-E)")],
         [t("Solar generation in Romania", "Producția solară din România"), t("daily", "zilnică"),
          t("ENTSO-E (Transelectrica data), via energy-charts.info", "ENTSO-E (date Transelectrica), prin energy-charts.info")],
         [t("Brent crude oil, nearest futures contract, in dollars (USD) per barrel", "Țițeiul Brent, contractul futures cel mai apropiat, în dolari americani (USD) pe baril"),
          t("daily", "zilnică"), "Yahoo Finance (BZ=F)"],
         [t("European Union (EU) emission allowance (EUA), via an exchange-traded commodity (ETC) backed by allowances",
            "Certificatul de emisii al Uniunii Europene (UE), EU Allowance (EUA), aproximat printr-un titlu bursier garantat cu certificate (ETC)"),
          t("daily", "zilnică"), "Yahoo Finance (SparkChange, CO2.L)"],
         [t("Gas: Title Transfer Facility (TTF), monthly average", "Gaze naturale: hubul olandez Title Transfer Facility (TTF), media lunară"),
          t("monthly", "lunară"), t("World Bank, Pink Sheet (no free daily series)", "Banca Mondială, Pink Sheet (fără serie zilnică gratuită)")],
         [t("Shares on the Bucharest Stock Exchange (BVB): OMV Petrom (SNP), Hidroelectrica (H2O)",
            "Acțiuni listate la Bursa de Valori București (BVB): OMV Petrom (SNP), Hidroelectrica (H2O)"),
          t("daily", "zilnică"), t("data vendor eodhd.com (EODHD), dividend-adjusted", "furnizorul eodhd.com (EODHD), ajustate cu dividendele")]],
        size="scriptsize", stretch="0.88") + "\n\\vspace{0.5mm}\n" + it(
        (t("\\textbf{Period}", "\\textbf{Perioada}"),
         t("power: @{data.start|date} -- @{data.end|date} (last complete month), @{data.n_days|,d} delivery days in Central European Time (CET), none missing; downloaded @{cutoff.download|date}",
           "energie electrică: @{data.start|date} -- @{data.end|date} (ultima lună completă), @{data.n_days|,d} " + de("data.n_days") + "zile de livrare, după ora Europei Centrale (CET), fără zile lipsă"),
         t("Brent: the @{mkt.brent_n_roll} first trading days of a month are dropped (contract change, not a price move); EUA from @{mkt.eua_start|date}",
           "Brent: fără prima zi de tranzacționare a fiecărei luni (@{mkt.brent_n_roll} " + de("mkt.brent_n_roll") + "zile, schimbarea contractului); EUA din @{mkt.eua_start|date}")),
        sep="1pt") + D.bottom(None, NB + " \\S1"), "footnotesize")

    # ------------------------------------------------------------------ 1 measuring volatility
    D.section(t("Measuring volatility", "Măsurarea volatilității"))
    D.subsection(t("Percent or EUR/MWh", "În procente sau în EUR/MWh"))
    D.concept(t("Volatility is the typical size of tomorrow's price surprise", "Volatilitatea măsoară mărimea obișnuită a surprizei de preț"),
              t("Volatility tells how far from today's price tomorrow's price usually lands.",
                "Volatilitatea arată cît de departe de prețul de azi ajunge, de obicei, prețul de mîine."),
              "\\[ \\underbrace{r_t=100\\ln\\frac{P_t}{P_{t-1}}}_{\\text{" + t("change in \\%", "variația în \\%") + "}}\\qquad "
              "\\underbrace{\\Delta P_t=P_t-P_{t-1}}_{\\text{" + t("change in EUR/MWh", "variația în EUR/MWh") + "}} \\]"
              "\\[ \\hat\\sigma=\\sqrt{\\tfrac{1}{T-1}\\textstyle\\sum_{t=1}^{T}(r_t-\\bar r)^2},\\qquad \\sigma_{\\text{" + t("year", "an") + "}}=\\hat\\sigma\\sqrt{A} \\]" +
              "\\where{" + t("$P_t$ = daily base price, mean of the day's hourly prices, EUR/MWh; $T$ = number of days; "
                             "$A$ = 365 for power (an auction every day), 252 for traded assets.",
                             "$P_t$ = prețul zilnic de bază (media prețurilor orare ale zilei), EUR/MWh; $T$ = numărul de zile; "
                             "$A$ = 365 pentru energie (licitație zilnică), 252 pentru activele bursiere.") + "}",
              it((t("\\textbf{On our data}, " + PANEL, "\\textbf{Pe datele din România}, " + PANEL),
                  t("$\\hat\\sigma$ of $r_t$ = @{ret.sd|.1f}\\% per day; of $\\Delta P_t$ = @{ret.sd_eur|.1f} EUR/MWh",
                    "$\\hat\\sigma$ pentru $r_t$: @{ret.sd|.1f}\\% pe zi; pentru $\\Delta P_t$: @{ret.sd_eur|.1f} EUR/MWh"),
                  t("annualised, calendar removed: @{voly.RO_full_ann|.0f}\\%; Brent @{voly.BRENT_full_ann|.0f}\\%, EUA @{voly.EUA_full_ann|.0f}\\%",
                    "anualizată, fără efectul calendarului: @{voly.RO_full_ann|.0f}\\%; Brent @{voly.BRENT_full_ann|.0f}\\%, EUA @{voly.EUA_full_ann|.0f}\\%")),
                 (t("\\textbf{Not an asset return}", "\\textbf{Nu este randamentul unui activ}"),
                  t("electricity cannot be stored: days $t$ and $t-1$ are different products",
                    "energia nu se poate stoca: zilele $t$ și $t-1$ sînt produse diferite")),
                 sep="2pt"),
              t("a supplier that buys on the PZU every day is exposed exactly to this daily surprise.",
                "un furnizor care cumpără zilnic energie de pe PZU este expus exact acestei surprize zilnice."),
              tryit=NB + " \\S1", cite="(Weron, 2006; Weron, 2014, IJF)", wl="0.53", wr="0.44")

    D.chart(t("Daily price changes alternate calm and turbulent stretches", "Variațiile zilnice alternează perioade calme și perioade agitate"),
            "returns_ro", [
                t(("Extreme days", "largest rise @{ret.max|+.0f}\\% on @{ret.max_date|date}, largest fall @{ret.min|.0f}\\% on @{ret.min_date|date} (Christmas)",
                   "@{ret.n_abs50} days with $|r_t|>50\\%$ out of @{ret.n|,d}"),
                  ("Zilele extreme", "cea mai mare creștere: @{ret.max|+.0f}\\%, la @{ret.max_date|date}; cea mai mare scădere: @{ret.min|.0f}\\%, la @{ret.min_date|date} (Crăciunul)",
                   "@{ret.n_abs50} " + de("ret.n_abs50") + "zile cu $|r_t|>50\\%$, din @{ret.n|,d}"))],
            height="0.62\\textheight",
            job=t("a calm month says little about next month: risk comes in clusters.", "o lună calmă spune puțin despre luna următoare: riscul apare grupat."),
            tryit=NB + " \\S1", cite=t("(OPCOM day-ahead prices)", "(prețurile PZU publicate de OPCOM)"))

    D.concept(t("Near zero the percent change explodes; below zero it does not exist", "Lîngă zero, variația procentuală explodează; sub zero, nu există"),
              t("The logarithm needs positive prices; near zero, ordinary moves become huge percentages.",
                "Logaritmul cere prețuri pozitive; lîngă zero, variații obișnuite devin procente uriașe."),
              "\\[ \\operatorname{asinh}(x)=\\ln\\bigl(x+\\sqrt{x^2+1}\\bigr) \\]\\vspace{-2mm}\\[ \\Delta\\operatorname{asinh}P_t\\approx\\Delta\\ln P_t\\ \\ \\text{" +
              t("if", "dacă") + "}\\ P_t\\gg 1 \\]" +
              "\\where{" + t("$\\operatorname{asinh}$ = inverse hyperbolic sine, defined for any sign; from 100 to 120 EUR/MWh both formulas give @{nonpos.log_100_120|.1f}\\%; "
                             "near zero both explode.",
                             "$\\operatorname{asinh}$ = sinusul hiperbolic invers, definit pentru orice semn; de la 100 la 120 EUR/MWh ambele formule dau @{nonpos.log_100_120|.1f}\\%; "
                             "lîngă zero ambele explodează.") + "}",
              it((t("\\textbf{On our data}, " + PANEL, "\\textbf{Pe datele noastre}, " + PANEL),
                  t("Romania: base price always positive (minimum @{nonpos.ro_min|.2f} EUR/MWh)",
                    "România: prețul de bază a fost mereu pozitiv (minimum @{nonpos.ro_min|.2f} EUR/MWh)"),
                  t("but @{nonpos.neg_heq_RO|,.0f} hours with negative prices, on @{nonpos.neg_days_RO} days",
                    "dar @{nonpos.neg_heq_RO|,.0f} de ore cu prețuri negative, în @{nonpos.neg_days_RO} " + de("nonpos.neg_days_RO") + "zile"),
                  t("DE-LU: @{nonpos.daily.DE_LU} days with base price $\\le 0$; from @{nonpos.de_maxabs_p0|.2f} to @{nonpos.de_maxabs_p1|.2f} EUR/MWh: $r_t$ = @{nonpos.de_maxabs_pct|.0f}\\%",
                    "DE-LU: @{nonpos.daily.DE_LU} de zile cu prețul de bază $\\le 0$; de la @{nonpos.de_maxabs_p0|.2f} la @{nonpos.de_maxabs_p1|.2f} EUR/MWh: $r_t$ = @{nonpos.de_maxabs_pct|.0f}\\%")),
                 (t("\\textbf{Our choice}", "\\textbf{Alegerea din acest curs}"),
                  t("base price: $r_t$ (\\%) and $\\Delta P_t$ (EUR/MWh); hourly prices: EUR/MWh",
                    "prețul de bază: $r_t$ (\\%) și $\\Delta P_t$ (EUR/MWh); prețurile orare: EUR/MWh")), sep="2pt"),
              t("a position is in MWh, so its risk is in EUR/MWh; use percent only far from zero.",
                "o poziție se măsoară în MWh, deci riscul ei este în EUR/MWh; procentele au sens doar departe de zero."),
              tryit=NB + " \\S1", cite="(Uniejewski, Weron \\& Ziel, 2018, IEEE TPWRS)", wl="0.52", wr="0.45")

    D.figframe(t("Half of the daily change is the weekly calendar, known in advance",
                 "Jumătate din variația zilnică vine din calendarul săptămînal"),
               None,
               "\\[ r_t=c+\\textstyle\\sum_{k=1}^{7}\\phi_k r_{t-k}+\\sum_{j=2}^{7}\\delta_j D_{j,t}+\\varepsilon_t \\]",
               "dow_effect", [
                   t(("Mean equation: $\\phi_k$ = weight of the change $k$ days ago, $D_{j,t}=1$ if day $t$ is weekday $j$; $R^2$ = @{mean.r2_pct|.2f}",
                      "standard deviation @{mean.sd_raw|.1f}\\% before, @{mean.sd_res|.1f}\\% after; models below use $\\varepsilon_t$ and, in EUR/MWh, $u_t$"),
                     ("Ecuația mediei: $\\phi_k$ = ponderea variației de acum $k$ zile; $D_{j,t}=1$ în ziua $j$ a săptămînii; $R^2$ = @{mean.r2_pct|.2f}",
                      "abaterea standard scade de la @{mean.sd_raw|.1f}\\% la @{mean.sd_res|.1f}\\%; modelele folosesc $\\varepsilon_t$ și, în EUR/MWh, $u_t$"))],
               job=t("a Monday price jump is not a risk signal: forecast it, do not hedge it.",
                     "creșterea prețului de luni nu este un semnal de risc: ea trebuie prognozată, nu acoperită."),
               tryit=NB + " \\S1", height="0.45\\textheight", cite=t("(" + OWN + "; Weron, 2014, IJF)", "(" + OWN + "; Weron, 2014, IJF)"))

    D.subsection(t("Stylised facts", "Faptele stilizate"))
    D.figframe(t("The sign of a shock is unpredictable, its size is not", "Sensul unui șoc nu poate fi anticipat, mărimea lui da"),
               None, None,
               "acf_clust", [
                   t(("Ljung--Box $Q(10)=T(T+2)\\sum_{k\\le10}\\hat\\rho_k^2/(T-k)$, $\\hat\\rho_k$ = autocorrelation at lag $k$: @{facts.lb_e|.1f} for $\\varepsilon_t$ ($p$ = @{facts.lb_e_p|.2f}), @{facts.lb_e2|.1f} for $\\varepsilon_t^2$ (critical value 18.31)",
                      "Lagrange multiplier test for autoregressive conditional heteroskedasticity (ARCH-LM), 10 lags: @{facts.lm|.1f}, $p<0.001$"),
                     ("Testul Ljung--Box $Q(10)=T(T+2)\\sum_{k\\le10}\\hat\\rho_k^2/(T-k)$, $\\hat\\rho_k$ = autocorelația de ordin $k$: @{facts.lb_e|.1f} pentru $\\varepsilon_t$ ($p$ = @{facts.lb_e_p|.2f}), @{facts.lb_e2|.1f} pentru $\\varepsilon_t^2$ (valoarea critică: 18{,}31)",
                      "testul multiplicatorului Lagrange pentru heteroscedasticitate condiționată autoregresivă (ARCH-LM), 10 decalaje: @{facts.lm|.1f}, $p<0{,}001$"))],
               job=t("a large shock today announces large shocks in the next days: the subject of this lecture.",
                     "un șoc mare astăzi anunță șocuri mari și în zilele următoare: acesta este subiectul cursului."),
               tryit=NB + " \\S2", height="0.45\\textheight", cite="(Ljung \\& Box, 1978; Engle, 1982, Econometrica)")

    D.figframe(t("Extreme days are far more frequent than the normal law allows", "Zilele extreme sînt mult mai frecvente decît prevede legea normală"),
               None, None, "tails", [
                   t(("Shocks $\\varepsilon_t$: excess kurtosis @{facts.kurt|.1f}, skewness @{facts.skew|.2f} (large falls: holidays, windy days)",
                      "@{facts.n_4sd} shocks beyond 4 standard deviations, against @{facts.n_4sd_norm|.2f} expected under normality; Student-t with $\\nu$ = @{garch.pct.garch_t.nu|.1f} degrees of freedom"),
                     ("Șocurile $\\varepsilon_t$: excesul de aplatizare (kurtosis) @{facts.kurt|.1f}, asimetria @{facts.skew|.2f} (scăderi mari: sărbători, zile cu vînt puternic)",
                      "@{facts.n_4sd} șocuri dincolo de 4 abateri standard, față de @{facts.n_4sd_norm|.2f} așteptate în ipoteza normalității; distribuția Student, cu $\\nu$ = @{garch.pct.garch_t.nu|.1f} grade de libertate"))],
               job=t("a limit built on the normal curve is breached far more often than planned (Lecture 4).",
                     "o limită calculată cu distribuția normală este depășită mult mai des decît s-a planificat (cursul 4)."),
               tryit=NB + " \\S2", height="0.50\\textheight", cite=t("(" + OWN + "; Bollerslev, 1987, RESTAT)", "(" + OWN + "; Bollerslev, 1987, RESTAT)"))

    D.figframe(t("The crisis: same volatility in percent, @{voly.ratio_eur_22_19|.0f} times higher in EUR/MWh",
                 "Criza: aceeași volatilitate în procente, de @{voly.ratio_eur_22_19|.0f} ori mai mare în EUR/MWh"),
               None, None, "vol_units", [
                   t(("Standard deviation of the shocks, 2019 vs 2022",
                      "in percent: @{voly.RO_pct_d.2019|.1f}\\% vs @{voly.RO_pct_d.2022|.1f}\\% (ratio @{voly.ratio_pct_22_19|.2f})",
                      "in EUR/MWh: @{voly.RO_eur.2019|.1f} vs @{voly.RO_eur.2022|.1f} (ratio @{voly.ratio_eur_22_19|.1f}); mean price @{voly.RO_lvl.2019|.0f} vs @{voly.RO_lvl.2022|.0f} EUR/MWh"),
                     ("Abaterea standard a șocurilor, 2019 față de 2022",
                      "în procente: @{voly.RO_pct_d.2019|.1f}\\% față de @{voly.RO_pct_d.2022|.1f}\\% (raport @{voly.ratio_pct_22_19|.2f})",
                      "în EUR/MWh: @{voly.RO_eur.2019|.1f} față de @{voly.RO_eur.2022|.1f} (raport @{voly.ratio_eur_22_19|.1f}); prețul mediu: @{voly.RO_lvl.2019|.0f}, respectiv @{voly.RO_lvl.2022|.0f} EUR/MWh"))],
               job=t("margin calls are paid in EUR: collateral rose with the price level although percent volatility did not.",
                     "apelurile în marjă se plătesc în euro: garanțiile au crescut odată cu nivelul prețului, deși volatilitatea procentuală nu a crescut."),
               tryit=NB + " \\S2", height="0.50\\textheight", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    VY = N["voly"]
    yrs = [str(y) for y in range(2019, 2027)]
    allv = [VY[k][y] for k in ["RO", "HU", "EUA", "BRENT", "TTF", "SNP", "H2O"] for y in yrs if VY[k][y] is not None]
    rows = []
    for k, lab in [("RO", t("Power, Romania", "Energie electrică, România")), ("HU", t("Power, Hungary", "Energie electrică, Ungaria")),
                   ("EUA", "EUA"), ("BRENT", "Brent"), ("TTF", t("TTF gas (monthly)", "Gaze TTF (lunar)")),
                   ("SNP", "OMV Petrom (SNP)"), ("H2O", "Hidroelectrica (H2O)")]:
        rows.append([lab] + [heat(VY[k][y], min(allv), 400, True, fmt(VY[k][y], ".0f", lang)) if VY[k][y] is not None else "--" for y in yrs])
    D.frame(t("Power prices are about @{voly.ratio_ro_brent|.0f} times more volatile than oil",
              "Energia electrică este de circa @{voly.ratio_ro_brent|.0f} ori mai volatilă decît petrolul"),
            "\\begin{center}" + table("@{}l" + "r" * len(yrs) + "@{}", [t("Annualised volatility, \\%", "Volatilitatea anualizată, \\%")] + yrs, rows,
                                      size="footnotesize", stretch="1.05") + "\\end{center}\\vspace{-1mm}" + it(
                (t("\\textbf{How to read it}", "\\textbf{Cum se citește tabelul}"),
                 t("daily shocks: standard deviation $\\times\\sqrt{365}$ for power, $\\times\\sqrt{252}$ for traded assets; TTF: monthly averages $\\times\\sqrt{12}$ (understates risk)",
                   "abaterea standard a șocurilor zilnice $\\times\\sqrt{365}$ pentru energie, $\\times\\sqrt{252}$ pentru activele bursiere; TTF: medii lunare $\\times\\sqrt{12}$ (subestimează riscul)"),
                 t("Brent peaks in 2020 and 2026, carbon in 2022; -- = series not yet available",
                   "Brent are vîrfuri în 2020 și 2026, carbonul în 2022; -- = seria nu era încă disponibilă")), sep="1pt") +
            D.bottom(t("never compare the limits of a power desk with those of an oil desk in the same percent.",
                       "nu comparați limitele unui birou de tranzacționare a energiei electrice cu cele ale unui birou de petrol, exprimate în același procent."), NB + " \\S2"),
            "footnotesize", cite=t("(" + OWN + "; World Bank Pink Sheet)", "(" + OWN + "; Banca Mondială, Pink Sheet)"))

    # ------------------------------------------------------------------ 2 GARCH family
    D.section(t("The GARCH family", "Modelele din familia GARCH"))
    D.subsection(t("GARCH(1,1) and its estimation", "Modelul GARCH(1,1) și estimarea lui"))
    g, ge = "garch.pct.garch_t", "garch.eur.garch_t"
    D.concept(t("GARCH updates tomorrow's variance from today's shock",
                "GARCH actualizează varianța de mîine pe baza șocului de azi"),
              t("A big shock yesterday raises today's variance; the effect then fades day by day.",
                "Un șoc mare ieri mărește varianța de azi; efectul se stinge apoi treptat, de la o zi la alta."),
              "\\[ \\sigma_t^2=\\underbrace{\\omega}_{\\text{" + t("constant", "constanta") + "}}+"
              "\\underbrace{\\alpha\\,\\varepsilon_{t-1}^2}_{\\text{" + t("reaction to the shock", "reacția la șoc") + "}}+"
              "\\underbrace{\\beta\\,\\sigma_{t-1}^2}_{\\text{" + t("memory", "memoria") + "}} \\]\\vspace{-1mm}"
              "\\[ \\varepsilon_t=\\sigma_t z_t,\\qquad \\bar\\sigma^2=\\frac{\\omega}{1-\\alpha-\\beta} \\]" +
              "\\where{" + t("$\\sigma_t^2$ = conditional variance, known on the evening of $t-1$; $z_t$ = standardised shock (mean 0, variance 1); "
                             "$\\omega>0$, $\\alpha,\\beta\\ge0$, persistence $\\alpha+\\beta<1$, long-run variance $\\bar\\sigma^2$; $\\beta=0$: ARCH model (Engle, 1982).",
                             "$\\sigma_t^2$ = varianța condiționată, cunoscută în seara zilei $t-1$; $z_t$ = șocul standardizat (media 0, varianța 1); "
                             "$\\omega>0$, $\\alpha,\\beta\\ge0$, persistența $\\alpha+\\beta<1$, varianța de lungă durată $\\bar\\sigma^2$; $\\beta=0$: modelul ARCH (Engle, 1982).") + "}",
              it((t("\\textbf{Romania, shocks in \\%}", "\\textbf{România, șocuri în \\%}"),
                  "$\\hat\\alpha$ = @{" + g + ".alpha|.3f}, $\\hat\\beta$ = @{" + g + ".beta|.3f}, $\\hat\\alpha+\\hat\\beta$ = @{" + g + ".pers|.3f}",
                  t("long-run $\\bar\\sigma$ = @{" + g + ".usd|.1f}\\% per day", "$\\bar\\sigma$ de lungă durată: @{" + g + ".usd|.1f}\\% pe zi")),
                 (t("\\textbf{Romania, shocks in EUR/MWh}", "\\textbf{România, șocuri în EUR/MWh}"),
                  "$\\hat\\alpha$ = @{" + ge + ".alpha|.3f}, $\\hat\\beta$ = @{" + ge + ".beta|.3f}, $\\hat\\alpha+\\hat\\beta$ = @{" + ge + ".pers|.3f}",
                  t("long-run $\\bar\\sigma$ = @{" + ge + ".usd|.1f} EUR/MWh per day", "$\\bar\\sigma$ de lungă durată: @{" + ge + ".usd|.1f} EUR/MWh pe zi")),
                 sep="2pt"),
              t("every evening GARCH gives the risk desk tomorrow's $\\sigma$, from data it already has.",
                "în fiecare seară, GARCH dă departamentului de risc valoarea $\\sigma$ pentru ziua următoare."),
              tryit=NB + " \\S3", cite="(Engle, 1982, Econometrica; Bollerslev, 1986, JOE)", wl="0.58", wr="0.39")

    gn = "garch.pct.garch_n"
    D.concept(t("Parameters are estimated by maximum likelihood with Student-t shocks", "Parametrii se estimează prin verosimilitate maximă, cu șocuri Student"),
              t("Choose the parameters that make the observed shocks most probable; Student-t leaves room for extreme days.",
                "Alegem parametrii care fac cel mai probabile șocurile observate; legea Student lasă loc zilelor extreme."),
              "\\[ \\ell(\\omega,\\alpha,\\beta,\\nu)=\\sum_{t=1}^{T}\\Bigl[\\ln f_\\nu\\Bigl(\\frac{\\varepsilon_t}{\\sigma_t}\\Bigr)-\\ln\\sigma_t\\Bigr] \\]" +
              "\\where{" + t("$f_\\nu$ = Student-t density with variance 1 and $\\nu>2$ degrees of freedom; small $\\nu$ = fat tails, $\\nu\\to\\infty$ = normal; "
                             "Bayesian information criterion (BIC) $=k\\ln T-2\\hat\\ell$, $k$ = number of parameters (lower = better); Appendix A.",
                             "$f_\\nu$ = densitatea Student cu varianța 1 și $\\nu>2$ grade de libertate; $\\nu$ mic = cozi groase, $\\nu\\to\\infty$ = distribuția normală; "
                             "criteriul informațional bayesian (BIC) $=k\\ln T-2\\hat\\ell$, $k$ = numărul de parametri (mai mic = mai bun); anexa A.") + "}",
              table("@{}lrr@{}", [t("GARCH(1,1), shocks in \\%", "GARCH(1,1), șocuri în \\%"), t("normal", "normală"), "Student"], [
                  [t("log-likelihood", "log-verosimilitatea"), f(gn + ".ll", ",.1f"), f(g + ".ll", ",.1f")],
                  ["BIC", f(gn + ".bic", ",.1f"), f(g + ".bic", ",.1f")],
                  ["$\\hat\\alpha+\\hat\\beta$", f(gn + ".pers", ".3f"), f(g + ".pers", ".3f")],
                  [t("half-life, days", "înjumătățire, zile"), f(gn + ".hl", ".1f"), f(g + ".hl", ".1f")],
                  ["$\\hat\\nu$", "--", f(g + ".nu", ".2f")]], size="footnotesize", stretch="1.15") + it(
                  t(("\\textbf{Reading}", "Student wins (lower BIC); the normal model reads every holiday as lasting volatility"),
                    ("\\textbf{Interpretare}", "modelul Student cîștigă (BIC mai mic); cel normal tratează fiecare sărbătoare ca volatilitate durabilă"))),
              t("use Student-t shocks; with normal shocks the limits stay wide for too long.",
                "folosiți șocuri de tip Student; cu șocuri normale, limitele rămîn largi prea mult timp."),
              tryit=NB + " \\S3", cite="(Bollerslev, 1987, RESTAT)", wl="0.50", wr="0.47")

    D.chart(t("GARCH volatility: short spikes in percent, a long hump in EUR/MWh", "GARCH: salturi scurte în procente, valori mari durabile în EUR/MWh"),
            "cond_vol", [
                t(("Peaks", "in percent: @{garch.cv.pct_max|.0f}\\% per day on @{garch.cv.pct_max_date|date}, gone within days",
                   "in EUR/MWh: @{garch.cv.eur_max|.1f} on @{garch.cv.eur_max_date|date}, against a minimum of @{garch.cv.eur_min|.1f} on @{garch.cv.eur_min_date|date}; @{garch.cv.eur_last|.1f} at the cut-off"),
                  ("Valorile maxime", "în procente: @{garch.cv.pct_max|.0f}\\% pe zi, la @{garch.cv.pct_max_date|date}, dispărute în cîteva zile",
                   "în EUR/MWh: @{garch.cv.eur_max|.1f}, la @{garch.cv.eur_max_date|date}, față de un minim de @{garch.cv.eur_min|.1f}, la @{garch.cv.eur_min_date|date}; @{garch.cv.eur_last|.1f} la sfîrșitul perioadei"))],
            height="0.60\\textheight",
            job=t("a supplier's collateral follows the EUR/MWh line, not the percent line.",
                  "garanțiile unui furnizor urmează curba în EUR/MWh, nu pe cea procentuală."),
            tryit=NB + " \\S3", cite=t("(" + OWN + ", GARCH(1,1)-t)", "(" + OWN + ", GARCH(1,1)-t)"))

    D.subsection(t("Persistence and half-life", "Persistența și timpul de înjumătățire"))
    X = N["xm"]

    def xrow(k, lab, unit):
        return [lab, fmt(X[k]["pers"], ".3f", lang), hl(f"xm.{k}.hl"), unit]
    D.concept(t("The half-life counts the days until half of a volatility shock is gone", "Timpul de înjumătățire arată în cîte zile dispare jumătate din șoc"),
              t("The extra variance created by a shock shrinks every day by the factor $\\alpha+\\beta$.",
                "Varianța suplimentară creată de un șoc se reduce în fiecare zi cu factorul $\\alpha+\\beta$."),
              "\\[ \\E_t\\bigl[\\sigma^2_{t+h}\\bigr]-\\bar\\sigma^2=(\\alpha+\\beta)^{h-1}\\bigl(\\sigma^2_{t+1}-\\bar\\sigma^2\\bigr) \\]\\vspace{-1mm}"
              "\\[ h_{1/2}=\\frac{\\ln 0.5}{\\ln(\\alpha+\\beta)} \\]".replace("0.5", "0{,}5" if ro else "0.5") +
              "\\where{" + t("$\\E_t$ = expectation given the data up to day $t$; $h$ = days ahead; $h_{1/2}$ = half-life; derivation in Appendix B.",
                             "$\\E_t$ = media condiționată de datele pînă în ziua $t$; $h$ = numărul de zile; $h_{1/2}$ = timpul de înjumătățire; deducerea formulei: anexa B.") + "}",
              table("@{}lrrl@{}", [t("GARCH(1,1)-t", "GARCH(1,1)-t"), "$\\hat\\alpha+\\hat\\beta$", "$h_{1/2}$", t("unit", "unitatea")], [
                  xrow("RO_pct", t("Romania, \\%", "România, \\%"), t("days", "zile")),
                  xrow("RO_eur", t("Romania, EUR/MWh", "România, EUR/MWh"), t("days", "zile")),
                  xrow("HU_pct", t("Hungary, \\%", "Ungaria, \\%"), t("days", "zile")),
                  xrow("BRENT", "Brent", t("trading days", "zile lucrătoare")),
                  xrow("EUA", "EUA", t("trading days", "zile lucrătoare")),
                  xrow("SNP", "OMV Petrom", t("trading days", "zile lucrătoare"))], size="footnotesize", stretch="1.12") + note(
                  t("Samples: power and Brent from 2019, EUA from @{mkt.eua_start|date}, OMV Petrom from 2019.",
                    "Eșantioane: energie electrică și Brent din 2019, EUA din @{mkt.eua_start|date}, OMV Petrom din 2019.")),
              t("after an oil shock keep wider limits for about @{xm.BRENT.hl_weeks|.0f} weeks; after a percent shock in power, for days.",
                "după un șoc pe piața petrolului, mențineți limite mai largi circa @{xm.BRENT.hl_weeks|.0f} săptămîni; după un șoc procentual al prețului energiei electrice, doar cîteva zile."),
              tryit=NB + " \\S3", cite="(Engle, 2001, JEP)", wl="0.49", wr="0.48")

    D.figframe(t("Answer to Lecture 1: oil and carbon shocks fade in weeks, not days",
                 "Petrolul și carbonul: șocurile de volatilitate durează săptămîni"),
               None, None, "halflife", [
                   t(("Curves: $100(\\hat\\alpha+\\hat\\beta)^h$ = percent of the extra variance left after $h$ days; half-lives in brackets", "Brent @{xm.BRENT.hl|.0f} trading days, about @{xm.BRENT.hl_weeks|.0f} weeks; EUA @{xm.EUA.hl|.0f}, about @{xm.EUA.hl_weeks|.0f} weeks",
                      "Romania: @{xm.RO_pct.hl|.1f} days in percent, but @{xm.RO_eur.hl|.0f} days in EUR/MWh, because volatility in money follows the price level"),
                     ("Curbele: $100(\\hat\\alpha+\\hat\\beta)^h$ = procentul din varianța suplimentară rămas după $h$ zile; timpii de înjumătățire, în paranteze", "Brent: @{xm.BRENT.hl|.0f} " + de("xm.BRENT.hl") + "zile lucrătoare, circa @{xm.BRENT.hl_weeks|.0f} săptămîni; EUA: @{xm.EUA.hl|.0f}, circa @{xm.EUA.hl_weeks|.0f} săptămîni",
                      "România: @{xm.RO_pct.hl|.1f} zile în procente, dar @{xm.RO_eur.hl|.0f} de zile în EUR/MWh, unde volatilitatea urmează nivelul prețului"))],
               job=t("after a shock, a risk desk keeps wider limits for weeks, not days, as announced in Lecture 1.",
                     "după un șoc, departamentul de risc menține limite mai largi săptămîni întregi, nu doar cîteva zile, cum anunța cursul 1."),
               tryit=NB + " \\S3", height="0.50\\textheight", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    D.subsection(t("Asymmetry", "Asimetria"))
    gj, eg, gju, egu = "garch.pct.gjr_t", "garch.pct.egarch_t", "garch.eur.gjr_t", "garch.eur.egarch_t"
    D.concept(t("Asymmetric GARCH: rises and falls do not move volatility equally", "GARCH asimetric: creșterile și scăderile nu au același efect"),
              t("Two extensions let a rise and a fall of the same size have different effects on tomorrow's variance.",
                "Două extensii permit ca o creștere și o scădere de aceeași mărime să aibă efecte diferite asupra varianței de mîine."),
              "\\[ \\text{GJR:}\\ \\ \\sigma_t^2=\\omega+(\\alpha+\\gamma I_{t-1})\\varepsilon_{t-1}^2+\\beta\\sigma_{t-1}^2 \\]"
              "\\[ \\text{EGARCH:}\\ \\ \\ln\\sigma_t^2=\\omega+\\alpha\\bigl(|z_{t-1}|-\\sqrt{2/\\pi}\\bigr)+\\gamma z_{t-1}+\\beta\\ln\\sigma_{t-1}^2 \\]" +
              "\\where{" + t("$I_{t-1}=1$ if $\\varepsilon_{t-1}<0$, else 0; Glosten--Jagannathan--Runkle (GJR): $\\gamma>0$ = falls raise volatility more (leverage effect of shares), $\\gamma<0$ = rises do; "
                             "exponential GARCH (EGARCH): opposite sign convention for $\\gamma$.",
                             "$I_{t-1}=1$ dacă $\\varepsilon_{t-1}<0$, altfel 0; modelul Glosten--Jagannathan--Runkle (GJR): $\\gamma>0$ = scăderile cresc mai mult volatilitatea (efectul de levier al acțiunilor), $\\gamma<0$ = creșterile; "
                             "GARCH exponențial (EGARCH): convenția de semn pentru $\\gamma$ este inversă.") + "}",
              it((t("\\textbf{Romania, shocks in \\%}", "\\textbf{România, șocuri în \\%}"),
                  "GJR: $\\hat\\gamma$ = @{" + gj + ".gamma|.3f} ($t$ = @{" + gj + ".gamma_t|.1f}); EGARCH: $\\hat\\gamma$ = @{" + eg + ".gamma|.3f} ($t$ = @{" + eg + ".gamma_t|.1f})",
                  t("falls raise volatility more (rebound after a drop)", "scăderile cresc mai mult volatilitatea (revenire după scădere)")),
                 (t("\\textbf{Romania, shocks in EUR/MWh}", "\\textbf{România, șocuri în EUR/MWh}"),
                  "GJR: $\\hat\\gamma$ = @{" + gju + ".gamma|.3f} ($t$ = @{" + gju + ".gamma_t|.1f}); EGARCH: $\\hat\\gamma$ = @{" + egu + ".gamma|.3f} ($t$ = @{" + egu + ".gamma_t|.1f})",
                  t("rises raise volatility more: inverse leverage effect", "creșterile cresc mai mult volatilitatea: efectul de levier invers")), sep="2pt"),
              t("for a buyer the dangerous direction is up: after a price jump, widen the limits more than after a fall.",
                "pentru un cumpărător, direcția periculoasă este în sus: după un salt de preț, lărgiți limitele mai mult decît după o scădere."),
              tryit=NB + " \\S4", cite="(Glosten et al., 1993, JFIN; Nelson, 1991; Knittel \\& Roberts, 2005, ENEECO)", wl="0.52", wr="0.45")

    D.figframe(t("In EUR/MWh, rises raise volatility more: the inverse leverage effect",
                 "În EUR/MWh, creșterile de preț măresc mai mult volatilitatea"),
               None, None, "nic", [
                   t(("News impact curve: next-day $\\sigma$ as a function of today's shock (GJR); for a shock of @{garch.eur.nic_2sd|.0f} EUR/MWh",
                      "next-day $\\sigma$ = @{garch.eur.nic_up2|.1f} EUR/MWh after a rise, @{garch.eur.nic_dn2|.1f} after a fall",
                      "in percent (shock of @{garch.pct.nic_2sd|.0f}\\%) the order is reversed: @{garch.pct.nic_dn2|.1f}\\% after a fall, @{garch.pct.nic_up2|.1f}\\% after a rise"),
                     ("Curba de impact a șocurilor: $\\sigma$ de mîine în funcție de șocul de azi (GJR); pentru un șoc de @{garch.eur.nic_2sd|.0f} EUR/MWh",
                      "$\\sigma$ în ziua următoare: @{garch.eur.nic_up2|.1f} EUR/MWh după o creștere, @{garch.eur.nic_dn2|.1f} după o scădere",
                      "în procente (șoc de @{garch.pct.nic_2sd|.0f}\\%), ordinea se inversează: @{garch.pct.nic_dn2|.1f}\\% după o scădere, @{garch.pct.nic_up2|.1f}\\% după o creștere"))],
               job=t("an industrial consumer on spot prices should react faster to rises than to falls.",
                     "un consumator industrial care cumpără la prețul spot trebuie să reacționeze mai repede la creșteri decît la scăderi."),
               tryit=NB + " \\S4", height="0.50\\textheight", cite="(Engle \\& Ng, 1993, JFIN; " + t(OWN + ", GJR(1,1)-t)", OWN + ", GJR(1,1)-t)"))

    D.figframe(t("Volatility in EUR/MWh grows with the price level",
                 "Volatilitatea în EUR/MWh crește odată cu nivelul prețului"),
               None, None, "vol_level", [
                   t(("Why: at high prices the supply curve (merit order) is steeper, so the same demand shock moves the price more",
                      "regression of $\\ln\\hat\\sigma_m(u)$ on $\\ln\\bar P_m$, @{level.n} months: slope @{level.slope|.2f}, $R^2$ = @{level.r2|.2f}; in percent: slope @{level.slope_pct|.2f}, $R^2$ = @{level.r2_pct|.2f}"),
                     ("Explicația: la prețuri mari, curba ofertei (ordinea de merit) este mai abruptă, deci același șoc al cererii mută mai mult prețul",
                      "regresia lui $\\ln\\hat\\sigma_m(u)$ pe $\\ln\\bar P_m$, @{level.n} " + de("level.n") + "luni: panta @{level.slope|.2f}, $R^2$ = @{level.r2|.2f}; în procente: panta @{level.slope_pct|.2f}, $R^2$ = @{level.r2_pct|.2f}"))],
               job=t("set EUR/MWh limits as a share of the forward price, not as a fixed amount.",
                     "stabiliți limitele în EUR/MWh ca procent din prețul contractelor la termen, nu ca sumă fixă."),
               tryit=NB + " \\S4", height="0.48\\textheight", cite="(Knittel \\& Roberts, 2005, ENEECO; " + t(OWN + ")", OWN + ")"))

    GG = N["garch"]
    MODS = [("garch_n", t("GARCH, normal", "GARCH, normal")), ("garch_t", "GARCH, Student"), ("gjr_n", t("GJR, normal", "GJR, normal")),
            ("gjr_t", "GJR, Student"), ("egarch_n", t("EGARCH, normal", "EGARCH, normal")), ("egarch_t", "EGARCH, Student")]
    trow = []
    for k, lab in MODS:
        r_ = [lab]
        for u in ["pct", "eur"]:
            bics = [GG[u][kk]["bic"] for kk, _ in MODS]
            r_ += [fmt(GG[u][k]["pers"], ".3f", lang), heat(GG[u][k]["bic"], min(bics), max(bics), True, fmt(GG[u][k]["bic"], ",.1f", lang)),
                   fmt(GG[u][k]["lbz2_p"], ".3f", lang)]
        trow.append(r_)
    best = {"garch_n": "GARCH", "garch_t": "GARCH-t", "gjr_n": "GJR", "gjr_t": "GJR-t", "egarch_n": "EGARCH", "egarch_t": "EGARCH-t"}
    D.frame(t("Fat tails matter more than asymmetry", "Cozile groase contează mai mult decît asimetria"),
            "\\begin{center}" + table("@{}l" + "rrr" * 2 + "@{}", [t("Model", "Modelul"), "$\\alpha+\\beta$ (\\%)", "BIC (\\%)", t("$p$, $z^2$ (\\%)", "$p$, $z^2$ (\\%)"),
                                                                    "$\\alpha+\\beta$ (EUR)", "BIC (EUR)", t("$p$, $z^2$ (EUR)", "$p$, $z^2$ (EUR)")],
                                      trow, size="footnotesize", stretch="1.05") + "\\end{center}\\vspace{-1mm}" + it(
                (t("\\textbf{Ranking by BIC} (green = best)", "\\textbf{Clasamentul după BIC} (verde = cel mai bun)"),
                 t("every Student-t model beats every normal one; best: " + best[GG["pct"]["best_bic"]] + " in \\%, " + best[GG["eur"]["best_bic"]] + " in EUR/MWh; "
                   "Akaike information criterion (AIC) in Appendix C",
                   "orice model cu distribuția Student îl depășește pe oricare cu distribuția normală; cel mai bun: " + best[GG["pct"]["best_bic"]] + " în \\%, " + best[GG["eur"]["best_bic"]] + " în EUR/MWh; "
                   "criteriul informațional Akaike (AIC): anexa C")),
                (t("\\textbf{Diagnostic}: Ljung--Box $p$ for $z_t^2$, the squared standardised shocks", "\\textbf{Diagnostic}: valoarea $p$ Ljung--Box pentru $z_t^2$, pătratul șocurilor standardizate"),
                 t("in \\% no clustering is left; in EUR/MWh some is ($p<0.001$): one equation cannot follow both the price level and the daily shocks",
                   "în \\% nu mai rămîne grupare; în EUR/MWh rămîne ($p<0{,}001$): o singură ecuație nu poate urmări și nivelul prețului, și șocurile zilnice")), sep="1pt") +
            D.bottom(t("first get the tails right, then worry about asymmetry.", "mai întîi modelați corect cozile distribuției, apoi asimetria."), NB + " \\S4"),
            "footnotesize", cite="(Bollerslev, 1987; Glosten, Jagannathan \\& Runkle, 1993; Nelson, 1991)")

    # ------------------------------------------------------------------ 3 regimes
    D.section(t("Regimes and the energy crisis", "Regimuri de volatilitate și criza energetică"))
    M = "ms.eur"
    D.concept(t("A Markov-switching model separates calm and turbulent regimes", "Modelul Markov cu schimbare de regim separă calmul de agitație"),
              t("Two hidden states, each with its own volatility; for every day the model gives the probability of the turbulent one.",
                "Două stări neobservate, fiecare cu volatilitatea ei; pentru fiecare zi, modelul dă probabilitatea stării agitate."),
              "\\[ u_t=\\mu_{s_t}+\\sigma_{s_t}\\eta_t,\\qquad \\Pr(s_t=j\\mid s_{t-1}=i)=p_{ij} \\]\\vspace{-1mm}"
              "\\[ \\text{" + t("expected duration of regime", "durata medie a regimului") + " } i=\\frac{1}{1-p_{ii}} \\]" +
              "\\where{" + t("$u_t$ = shock in EUR/MWh; $s_t$ = regime (calm or turbulent); $\\eta_t$ = standard normal; $p_{ij}$ = transition probabilities, by maximum likelihood (Appendix D).",
                             "$u_t$ = șocul în EUR/MWh; $s_t$ = regimul (calm sau agitat); $\\eta_t$ = variabilă normală standard; $p_{ij}$ = probabilitățile de tranziție, estimate prin verosimilitate maximă (anexa D).") + "}",
              it((t("\\textbf{Romania, shocks in EUR/MWh}", "\\textbf{România, șocuri în EUR/MWh}"),
                  t("calm: $\\sigma$ = @{" + M + ".sd_lo|.1f}, $p_{11}$ = @{" + M + ".p_ll|.3f}, about @{" + M + ".dur_lo|.0f} days",
                    "calm: $\\sigma$ = @{" + M + ".sd_lo|.1f}, $p_{11}$ = @{" + M + ".p_ll|.3f}, circa @{" + M + ".dur_lo|.0f} de zile"),
                  t("turbulent: $\\sigma$ = @{" + M + ".sd_hi|.1f}, $p_{22}$ = @{" + M + ".p_hh|.3f}, about @{" + M + ".dur_hi|.0f} days; @{" + M + ".share_hi|.0f}\\% of all days",
                    "agitat: $\\sigma$ = @{" + M + ".sd_hi|.1f}, $p_{22}$ = @{" + M + ".p_hh|.3f}, circa @{" + M + ".dur_hi|.0f} de zile; @{" + M + ".share_hi|.0f}\\% din zile")),
                 (t("\\textbf{In percent}", "\\textbf{În procente}"),
                  t("turbulent state: only @{ms.pct.dur_hi|.1f} days, isolated spikes", "starea agitată: doar @{ms.pct.dur_hi|.1f} zile, salturi izolate")), sep="2pt"),
              t("a turbulent-regime probability above 0.5 triggers a review of hedges and collateral.",
                "o probabilitate a regimului agitat peste 0{,}5 cere revizuirea acoperirii riscului și a garanțiilor."),
              tryit=NB + " \\S5", cite="(Hamilton, 1989, Econometrica)", wl="0.52", wr="0.45")

    D.chart(t("The crisis was one long turbulent regime; 2026 moves in and out",
              "Criza a fost un regim agitat lung; 2026 alternează între regimuri"),
            "ms_regime", [
                t(("Turbulent days", "longest spell: @{" + M + ".longest_start|date} -- @{" + M + ".longest_end|date}, @{" + M + ".longest_days} days",
                   "share by year: 2022 @{" + M + ".by_year.2022|.0f}\\%, 2025 @{" + M + ".by_year.2025|.0f}\\%, 2026 @{" + M + ".by_year.2026|.0f}\\% (@{" + M + ".share_2026_q3q4|.0f}\\% since July)"),
                  ("Zilele din regimul agitat", "cel mai lung episod: @{" + M + ".longest_start|date} -- @{" + M + ".longest_end|date}, @{" + M + ".longest_days} " + de(M + ".longest_days") + "zile",
                   "ponderea pe ani: 2022 @{" + M + ".by_year.2022|.0f}\\%, 2025 @{" + M + ".by_year.2025|.0f}\\%, 2026 @{" + M + ".by_year.2026|.0f}\\% (@{" + M + ".share_2026_q3q4|.0f}\\% din iulie)"))],
            height="0.60\\textheight",
            job=t("Transelectrica and suppliers can use the regime probability as an early warning for balancing costs.",
                  "Transelectrica și furnizorii pot folosi probabilitatea regimului agitat ca avertizare timpurie pentru costurile de echilibrare."),
            tryit=NB + " \\S5", cite=t("(" + OWN + "; Hamilton, 1989)", "(" + OWN + "; Hamilton, 1989)"))

    S = N["sub"]
    labp = [t("2019--2020 (calm)", "2019--2020 (calm)"), t("2021--2022 (crisis)", "2021--2022 (criză)"),
            t("2023 -- @{data.end|ym}", "2023 -- @{data.end|ym}"), t("whole sample", "întreaga perioadă")]
    srows = []
    for i, lab in enumerate(labp):
        a_, b_ = S["pct"][i], S["eur"][i]
        srows.append([lab, fmt(a_["pers"], ".3f", lang), hl(f"sub.pct.{i}.hl"), fmt(b_["pers"], ".3f", lang), hl(f"sub.eur.{i}.hl"),
                      fmt(b_["usd"], ".1f", lang) if b_["usd"] is not None else "--"])
    D.frame(t("Persistence depends on the period and on the unit", "Persistența depinde de perioadă și de unitatea de măsură"),
            "\\begin{center}" + table("@{}lrrrrr@{}", [t("GARCH(1,1)-t on", "GARCH(1,1)-t pe"), "$\\hat\\alpha+\\hat\\beta$ (\\%)", "$h_{1/2}$ (\\%)",
                                                        "$\\hat\\alpha+\\hat\\beta$ (EUR)", "$h_{1/2}$ (EUR)", "$\\bar\\sigma$, EUR/MWh"], srows,
                                      size="footnotesize", stretch="1.1") + "\\end{center}\\vspace{-1mm}" + it(
                (t("\\textbf{In EUR/MWh}", "\\textbf{În EUR/MWh}"),
                 t("in 2019--2020 a shock halves in under a day; in the crisis $\\hat\\alpha+\\hat\\beta$ reaches 1, because volatility rose with the price month after month",
                   "în 2019--2020 un șoc se înjumătățește în mai puțin de o zi; în criză, $\\hat\\alpha+\\hat\\beta$ ajunge la 1, deoarece volatilitatea a crescut lună de lună odată cu prețul"),
                 t("the whole-sample value mixes regimes, and mixing regimes overstates persistence",
                   "valoarea pentru întreaga perioadă amestecă regimurile, ceea ce supraestimează persistența")),
                (t("\\textbf{In percent}", "\\textbf{În procente}"),
                 t("persistence stays well below 1 in every period: the crisis moved the level, not percent volatility",
                   "persistența rămîne mult sub 1 în fiecare perioadă: criza a mutat nivelul prețului, nu volatilitatea procentuală")), sep="1pt") +
            D.bottom(t("re-estimate after a regime change; a model fitted on the crisis keeps limits wide for too long.",
                       "reestimați modelul după o schimbare de regim; un model estimat pe perioada crizei menține limitele largi prea mult timp."), NB + " \\S5"),
            "footnotesize", cite="(Lamoureux \\& Lastrapes, 1990, JBES; " + t(OWN + ")", OWN + ")"))

    # ------------------------------------------------------------------ 4 intraday
    D.section(t("Intraday volatility from hourly prices", "Volatilitatea intrazilnică, din prețurile orare"))
    D.concept(t("Intraday variation measures how much the price moves within a day",
                "Variația intrazilnică măsoară cît se mișcă prețul în cursul zilei"),
              t("Sum the squared hour-to-hour changes of one delivery day; this is the variation a battery or a flexible consumer earns from.",
                "Adunăm pătratele variațiilor de la o oră la alta din aceeași zi de livrare; din această variație cîștigă o baterie sau un consumator flexibil."),
              "\\[ \\text{RV}_d=\\sqrt{\\textstyle\\sum_{h=1}^{H_d-1}\\bigl(P_{d,h}-P_{d,h-1}\\bigr)^2},\\qquad \\text{" + t("relative", "relativă") + "}=\\frac{\\text{RV}_d}{\\bar P_d} \\]" +
              "\\where{" + t("$P_{d,h}$ = price of hour $h$ of day $d$ (from 1 October 2025, mean of the four quarter-hours); $H_d$ = 24 hours (23 or 25 on the "
                             "@{rv.n_23} + @{rv.n_25} clock-change days); $\\bar P_d$ = daily base price; in EUR/MWh, because hourly prices can be negative.",
                             "$P_{d,h}$ = prețul orei $h$ din ziua $d$ (din 1 octombrie 2025, media celor patru sferturi de oră); $H_d$ = 24 de ore (23 sau 25 în cele "
                             "@{rv.n_23} + @{rv.n_25} zile cu schimbarea orei); $\\bar P_d$ = prețul zilnic de bază; în EUR/MWh, deoarece prețurile orare pot fi negative.") + "}",
              it((t("\\textbf{Realised intraday variation (RV)}, yearly mean", "\\textbf{Variația intrazilnică realizată (RV)}, media anuală"),
                  t("2019: @{rv.by_year.2019|.0f}; 2022: @{rv.by_year.2022|.0f}; 2026: @{rv.by_year.2026|.0f} EUR/MWh",
                    "2019: @{rv.by_year.2019|.0f}; 2022: @{rv.by_year.2022|.0f}; 2026: @{rv.by_year.2026|.0f} EUR/MWh"),
                  t("relative to the price (median): @{rv.rel_by_year.2019|.2f} in 2019, @{rv.rel_by_year.2024|.2f} in 2024",
                    "raportată la preț (mediana): @{rv.rel_by_year.2019|.2f} în 2019, @{rv.rel_by_year.2024|.2f} în 2024")),
                 (t("\\textbf{A different risk}", "\\textbf{Un risc diferit}"),
                  t("correlation between RV$_d$ and $|u_t|$: only @{rv.corr_daily_abs|.2f}", "corelația dintre RV$_d$ și $|u_t|$: doar @{rv.corr_daily_abs|.2f}"),
                  t("not the realised volatility of finance: the 24 hours are 24 different products",
                    "nu este volatilitatea realizată din finanțe: cele 24 de ore sînt 24 de produse diferite")), sep="2pt"),
              t("a battery developer's revenue scales with intraday variation, not with the daily average price.",
                "venitul unui investitor în baterii depinde de variația intrazilnică, nu de prețul mediu zilnic."),
              tryit=NB + " \\S6", cite="(Andersen \\& Bollerslev, 1998, IER; Weron, 2014, IJF)", wl="0.52", wr="0.45")

    D.chart(t("Solar generation has made the price move more within the day", "Producția solară a mărit variația prețului în cursul zilei"),
            "rv_solar", [
                t(("Relative intraday variation (median)", "@{rv.rel_by_year.2019|.2f} in 2019, peak @{rv.rel_by_year.2024|.2f} in @{rv.rel_peak_year}, @{rv.rel_by_year.2026|.2f} in 2026",
                   "mean solar output: @{rv.sol_2019|.0f} MW in 2019, @{rv.sol_last|.0f} MW in Jan -- @{data.end|ym}; monthly correlation @{rv.corr_rel_solar_m|.2f}"),
                  ("Variația intrazilnică relativă (mediana)", "@{rv.rel_by_year.2019|.2f} în 2019, maximum @{rv.rel_by_year.2024|.2f} în @{rv.rel_peak_year}, @{rv.rel_by_year.2026|.2f} în 2026",
                   "producția solară medie: @{rv.sol_2019|.0f} MW în 2019, @{rv.sol_last|.0f} MW în ianuarie -- @{data.end|ym}; corelația lunară: @{rv.corr_rel_solar_m|.2f}"))],
            height="0.60\\textheight",
            job=t("more solar means cheaper middays and dearer evenings: the business case of storage.",
                  "mai multă producție solară înseamnă prețuri mici la prînz și mari seara: argumentul economic pentru stocare."),
            tryit=NB + " \\S6", cite=t("(" + OWN + "; ENTSO-E solar generation)", "(" + OWN + "; producția solară ENTSO-E)"))

    D.concept(t("Intraday variation has a long memory: day, week and month",
                "Variația intrazilnică are memorie lungă: zi, săptămînă, lună"),
              t("Three averages over different horizons give a simple long-memory regression.",
                "Trei medii pe orizonturi diferite dau o regresie cu memorie lungă."),
              "\\[ \\begin{aligned}\\ln\\text{RV}_d=b_0&+b_D\\ln\\text{RV}_{d-1}+\\tfrac{b_W}{7}\\textstyle\\sum_{j=1}^{7}\\ln\\text{RV}_{d-j}\\\\ "
              "&+\\tfrac{b_M}{30}\\textstyle\\sum_{j=1}^{30}\\ln\\text{RV}_{d-j}+e_d\\end{aligned} \\]" +
              "\\where{" + t("heterogeneous autoregressive (HAR) model, by ordinary least squares (OLS); $b_D$, $b_W$, $b_M$ = weights of yesterday, the last 7 and 30 days; "
                             "forecast $=\\exp(\\widehat{\\ln\\text{RV}}_d+s^2/2)$, $s^2$ = residual variance.",
                             "modelul autoregresiv eterogen (HAR), estimat prin metoda celor mai mici pătrate (OLS); $b_D$, $b_W$, $b_M$ = ponderile zilei de ieri, ale ultimelor 7 și 30 de zile; "
                             "prognoza $=\\exp(\\widehat{\\ln\\text{RV}}_d+s^2/2)$, $s^2$ = varianța erorilor.") + "}",
              it((t("\\textbf{Estimates}, before the test year", "\\textbf{Estimări}, înaintea anului de test"),
                  t("$\\hat b_D$ = @{har.bd|.2f}, $\\hat b_W$ = @{har.bw|.2f}, $\\hat b_M$ = @{har.bm|.2f} (all $t>$ @{har.bm_t|.0f}), $R^2$ = @{har.r2|.2f}",
                    "$\\hat b_D$ = @{har.bd|.2f}, $\\hat b_W$ = @{har.bw|.2f}, $\\hat b_M$ = @{har.bm|.2f} (toate cu $t>$ @{har.bm_t|.0f}), $R^2$ = @{har.r2|.2f}")),
                 (t("\\textbf{Test year}", "\\textbf{Anul de test}"),
                  t("mean absolute error (MAE): HAR @{har.mae_har|.1f}, yesterday's value @{har.mae_naive|.1f} EUR/MWh (@{har.gain|.1f}\\% less)",
                    "eroarea absolută medie (MAE): HAR @{har.mae_har|.1f}, valoarea de ieri @{har.mae_naive|.1f} EUR/MWh (cu @{har.gain|.1f}\\% mai puțin)")), sep="2pt"),
              t("a battery operator schedules maintenance on days with low forecast variation.",
                "o baterie își programează mentenanța în zilele cu variație prognozată mică."),
              tryit=NB + " \\S6", cite="(Corsi, 2009, JFEC)", wl="0.56", wr="0.41")

    D.chart(t("HAR forecasts follow intraday variation, not its isolated spikes", "Prognozele HAR urmăresc variația, dar nu și salturile izolate"),
            "har_fc", [
                t(("Test year, forecast made on $d-1$", "HAR re-estimated every day on the data available on $d-1$; MAE @{har.mae_har|.1f} EUR/MWh"),
                  ("Anul de test, prognoză făcută în ziua $d-1$", "HAR reestimat zilnic pe datele disponibile în ziua $d-1$; MAE @{har.mae_har|.1f} EUR/MWh"))],
            height="0.60\\textheight",
            job=t("use the forecast for planning; keep reserves for the spikes it cannot see.",
                  "folosiți prognoza pentru planificare și păstrați rezerve pentru salturile pe care nu le poate anticipa."),
            tryit=NB + " \\S6", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    # ------------------------------------------------------------------ 5 forecasting
    D.section(t("Forecasting and evaluating volatility", "Prognoza și evaluarea volatilității"))
    D.concept(t("A volatility forecast is judged against a noisy proxy",
                "Prognoza volatilității se evaluează față de o aproximare zgomotoasă"),
              t("We compare the forecast with a noisy proxy, the squared shock, using a loss that still ranks models correctly.",
                "Comparăm prognoza cu o aproximare zgomotoasă, pătratul șocului, folosind o funcție de pierdere care ordonează totuși corect modelele."),
              "\\[ \\text{QLIKE}_t=\\frac{\\varepsilon_t^2}{\\hat\\sigma_t^2}-\\ln\\frac{\\varepsilon_t^2}{\\hat\\sigma_t^2}-1,\\qquad "
              "\\text{MSE}_t=\\bigl(\\varepsilon_t^2-\\hat\\sigma_t^2\\bigr)^2 \\]" +
              "\\where{" + t("quasi-likelihood loss (QLIKE), mean squared error (MSE); $\\varepsilon_t$ = out-of-sample shock of day $t$; $\\hat\\sigma_t^2$ = forecast made on $t-1$; "
                             "MSE is dominated by a few extreme days; Diebold--Mariano (DM) test on the daily loss differences.",
                             "funcția de pierdere de tip cvasi-verosimilitate (QLIKE), eroarea pătratică medie (MSE); $\\varepsilon_t$ = șocul zilei $t$, în afara eșantionului; "
                             "$\\hat\\sigma_t^2$ = prognoza făcută în $t-1$; MSE este dominată de cîteva zile extreme; testul Diebold--Mariano (DM) compară pierderile zilnice.") + "}",
              it((t("\\textbf{Example}: true $\\sigma$ = 20", "\\textbf{Exemplu}: $\\sigma$ adevărat = 20"),
                  t("forecast 10: QLIKE = @{qex.under|.2f}; forecast 40: QLIKE = @{qex.over|.2f}", "prognoza 10: QLIKE = @{qex.under|.2f}; prognoza 40: QLIKE = @{qex.over|.2f}"),
                  t("underestimating costs @{qex.ratio|.1f} times more; MSE says the opposite", "subestimarea costă de @{qex.ratio|.1f} ori mai mult; MSE spune contrariul")),
                 (t("\\textbf{Design}, " + TEST, "\\textbf{Cadrul de evaluare}, " + TEST),
                  t("five models re-estimated daily on data up to $t-1$", "cinci modele, reestimate zilnic pe datele pînă în $t-1$")), sep="2pt"),
              t("ask your risk vendor for QLIKE on your own days, out of sample.",
                "cereți furnizorului modelului de risc valoarea QLIKE pe zilele dumneavoastră, în afara eșantionului."),
              tryit=NB + " \\S7", cite="(Patton, 2011, JOE; Hansen \\& Lunde, 2005, JAE)", wl="0.52", wr="0.45")

    FC = N["fc"]
    ML = [("hist30", t("30-day historical variance", "varianța istorică pe 30 de zile")),
          ("ewma", t("exponentially weighted moving average (EWMA), $\\lambda$ = 0.94", "medie mobilă cu ponderi exponențiale (EWMA), $\\lambda$ = 0{,}94")),
          ("garch", "GARCH(1,1)-t"), ("gjr", "GJR(1,1)-t"), ("egarch", "EGARCH(1,1)-t")]
    ML[1] = ("ewma", t("exponentially weighted average (EWMA)", "medie cu ponderi exponențiale (EWMA)"))
    frows = []
    for k, lab in ML:
        r_ = [lab]
        for u in ["pct", "eur"]:
            qs = [FC[u][kk]["qlike"] for kk, _ in ML]
            r_ += [heat(FC[u][k]["qlike"], min(qs), max(qs), True, fmt(FC[u][k]["qlike"], ".3f", lang)), pv(f"fc.{u}.{k}.p_beats_hist") if k != "hist30" else "--"]
        frows.append(r_)
    bestn = {"hist30": "hist30", "ewma": "EWMA", "garch": "GARCH-t", "gjr": "GJR-t", "egarch": "EGARCH-t"}
    D.frame(t("GARCH-type forecasts beat the 30-day history, significantly in EUR",
              "Modelele GARCH sînt mai precise decît varianța istorică"),
            "\\begin{center}" + table("@{}lrrrr@{}", [t("One-day-ahead variance", "Varianța pentru ziua următoare"),
                                                       t("QLIKE, \\%", "QLIKE, \\%"), t("$p$ vs 30-day", "$p$ față de 30 de zile"),
                                                       t("QLIKE, EUR", "QLIKE, EUR"), t("$p$ vs 30-day", "$p$ față de 30 de zile")], frows,
                                      size="footnotesize", stretch="1.05") + "\\end{center}\\vspace{-1mm}" + it(
                (t("\\textbf{Reading}", "\\textbf{Interpretare}"),
                 t("lower QLIKE = better (green); $p$ = one-sided DM test (Newey--West, 7 lags), @{fc.n} days",
                   "QLIKE mai mic = model mai bun (verde); $p$ = testul DM unilateral (Newey--West, 7 decalaje), @{fc.n} " + de("fc.n") + "zile"),
                 t("best: " + bestn[FC["pct"]["best"]] + " in \\% (@{fc.pct.gain_best_vs_hist|.1f}\\% below the 30-day loss), " + bestn[FC["eur"]["best"]] +
                   " in EUR/MWh (@{fc.eur.gain_best_vs_hist|.1f}\\%)",
                   "cel mai bun: " + bestn[FC["pct"]["best"]] + " în \\% (pierdere cu @{fc.pct.gain_best_vs_hist|.1f}\\% sub varianța pe 30 de zile), " + bestn[FC["eur"]["best"]] +
                   " în EUR/MWh (@{fc.eur.gain_best_vs_hist|.1f}\\%)")),
                (t("\\textbf{Significance at 5\\%}", "\\textbf{Semnificația, la pragul de 5\\%}"),
                 t("EUR/MWh: all GARCH-type models beat the history; percent: none does; asymmetry adds nothing significant ($p$ = @{fc.eur.p_best_vs_garch|.2f})",
                   "în EUR/MWh, toate modelele GARCH sînt mai precise decît varianța istorică; în procente, niciunul; asimetria nu aduce un cîștig semnificativ ($p$ = @{fc.eur.p_best_vs_garch|.2f})")), sep="1pt") +
            D.bottom(t("use GARCH-t as the default; asymmetric models add little out of sample.",
                       "folosiți GARCH-t ca model implicit; modelele asimetrice aduc puțin în afara eșantionului."), NB + " \\S7"),
            "footnotesize", cite="(Diebold \\& Mariano, 1995, JBES; Patton, 2011, JOE; RiskMetrics, 1996)")

    GH = "ghost"
    D.chart(t("GARCH reacts at once; the 30-day history lags, then forgets abruptly",
              "GARCH reacționează imediat; varianța istorică întîrzie și uită brusc"),
            "fc_test", [
                t(("Largest shock of the test year: @{" + GH + ".shock|+.0f} EUR/MWh on @{" + GH + ".date|date}",
                   "next day: GARCH $\\hat\\sigma$ from @{" + GH + ".garch_before|.0f} to @{" + GH + ".garch_after|.0f}, history only @{" + GH + ".hist_after|.0f} EUR/MWh",
                   "30 days later the shock leaves the window: the history drops from @{" + GH + ".hist_30|.0f} to @{" + GH + ".hist_31|.0f} overnight"),
                  ("Cel mai mare șoc din anul de test: @{" + GH + ".shock|+.0f} EUR/MWh, la @{" + GH + ".date|date}",
                   "a doua zi, $\\hat\\sigma$ GARCH crește de la @{" + GH + ".garch_before|.0f} la @{" + GH + ".garch_after|.0f}, iar varianța istorică dă doar @{" + GH + ".hist_after|.0f} EUR/MWh",
                   "după 30 de zile, șocul iese din fereastră: estimarea istorică scade într-o singură zi de la @{" + GH + ".hist_30|.0f} la @{" + GH + ".hist_31|.0f}"))],
            height="0.58\\textheight",
            job=t("a limit that jumps 30 days after a shock, with no news, is a warning sign of a historical-window model.",
                  "o limită care se modifică brusc la 30 de zile după un șoc, fără nicio informație nouă, trădează un model cu fereastră istorică."),
            tryit=NB + " \\S7", cite=t("(" + OWN + ", " + TEST + ")", "(" + OWN + ")"))   # RO: test year already in the source line; keeps the footer on one line

    BP, BE = "ts.brent.peak", "ts.brent.end"
    D.concept(t("Weeks ahead, volatility returns to its long-run level",
                "Pe mai multe săptămîni, volatilitatea revine spre nivelul normal"),
              t("High volatility is expected to fall and low volatility to rise, so $\\sigma\\sqrt{h}$ misstates the risk over $h$ days.",
                "O volatilitate mare se așteaptă să scadă, iar una mică să crească; de aceea, regula $\\sigma\\sqrt{h}$ greșește riscul pe $h$ zile."),
              "\\[ \\hat\\sigma^2_{T+h\\mid T}=\\bar\\sigma^2+(\\alpha+\\beta)^{h-1}\\bigl(\\hat\\sigma^2_{T+1}-\\bar\\sigma^2\\bigr) \\]\\vspace{-1mm}"
              "\\[ \\Var_T\\Bigl(\\textstyle\\sum_{k=1}^{h}r_{T+k}\\Bigr)=\\sum_{k=1}^{h}\\hat\\sigma^2_{T+k\\mid T}\\ \\ne\\ h\\,\\hat\\sigma^2_{T+1} \\]" +
              "\\where{" + t("$T$ = forecast day; second formula: returns without autocorrelation (oil, carbon), not power; 90\\% band = $\\pm1.645\\sqrt{\\cdot}$.",
                             "$T$ = ziua prognozei; a doua formulă: randamente fără autocorelație (petrol, carbon), nu energie electrică; banda de 90\\% = $\\pm1{,}645\\sqrt{\\cdot}$.") + "}",
              it((t("\\textbf{Brent on @{" + BP + ".date|date}}, after the 2026 oil shock", "\\textbf{Brent la @{" + BP + ".date|date}}, după șocul petrolier din 2026"),
                  t("$\\hat\\sigma_{T+1}$ = @{" + BP + ".s1_ann|.0f}\\% a year, long-run @{" + BP + ".lr_ann|.0f}\\%", "$\\hat\\sigma_{T+1}$ = @{" + BP + ".s1_ann|.0f}\\% pe an, pe termen lung @{" + BP + ".lr_ann|.0f}\\%"),
                  t("20-day band: GARCH $\\pm$@{" + BP + ".band20|.1f}\\%, $\\sigma\\sqrt{20}$ $\\pm$@{" + BP + ".band20_sqrt|.1f}\\% (@{" + BP + ".over|.0f}\\% too wide)",
                    "banda pe 20 de zile: GARCH $\\pm$@{" + BP + ".band20|.1f}\\%, $\\sigma\\sqrt{20}$: $\\pm$@{" + BP + ".band20_sqrt|.1f}\\% (prea largă cu @{" + BP + ".over|.0f}\\%)")),
                 (t("\\textbf{Brent on @{" + BE + ".date|date}}, calm again", "\\textbf{Brent la @{" + BE + ".date|date}}, din nou calm"),
                  t("$\\hat\\sigma_{T+1}$ = @{" + BE + ".s1_ann|.0f}\\% $<$ @{" + BE + ".lr_ann|.0f}\\%: now $\\sigma\\sqrt{20}$ is too narrow",
                    "$\\hat\\sigma_{T+1}$ = @{" + BE + ".s1_ann|.0f}\\% $<$ @{" + BE + ".lr_ann|.0f}\\%: acum $\\sigma\\sqrt{20}$ dă o bandă prea îngustă")), sep="2pt"),
              t("an industrial buyer budgeting next month's fuel should add the GARCH forecasts, not scale today's $\\sigma$.",
                "un consumator industrial care își face bugetul de combustibil adună prognozele GARCH, nu scalează $\\sigma$ de azi."),
              tryit=NB + " \\S7", cite="(Engle, 2001, JEP; " + t(OWN + ")", OWN + ")"), wl="0.52", wr="0.45")

    # ------------------------------------------------------------------ 6 case study
    D.section(t("Case study: Romanian power in 2026", "Studiu de caz: prețul energiei electrice din România în 2026"))
    C = "case"
    D.frame(t("Case study: 2026 is a level shock, not (yet) a new 2022", "Studiu de caz: 2026 este un șoc de nivel, nu (încă) o criză ca în 2022"), it(
        (t("\\textbf{What happened to prices}", "\\textbf{Ce s-a întîmplat cu prețurile}"),
         t("Romanian base price: @{" + C + ".p_jan|.0f} EUR/MWh in January, @{" + C + ".p_oct|.0f} in October 2026 (monthly means)",
           "prețul de bază din România: @{" + C + ".p_jan|.0f} EUR/MWh în ianuarie, @{" + C + ".p_oct|.0f} în octombrie 2026 (medii lunare)"),
         t("Brent: @{" + C + ".brent_feb|.0f} USD/bbl in February, @{" + C + ".brent_mar|.0f} in March, @{" + C + ".brent_oct|.0f} in October; TTF gas: @{" + C + ".ttf_feb|.0f} $\\to$ @{" + C + ".ttf_oct|.0f} EUR/MWh (February $\\to$ October)",
           "Brent: @{" + C + ".brent_feb|.0f} USD/baril în februarie, @{" + C + ".brent_mar|.0f} în martie, @{" + C + ".brent_oct|.0f} în octombrie; gaze TTF: @{" + C + ".ttf_feb|.0f} $\\to$ @{" + C + ".ttf_oct|.0f} EUR/MWh (februarie $\\to$ octombrie)")),
        (t("\\textbf{What happened to volatility}", "\\textbf{Ce s-a întîmplat cu volatilitatea}"),
         t("in percent, nothing: mean monthly $\\hat\\sigma$ @{" + C + ".r_26_mean|.1f}\\% in 2026, @{" + C + ".r_22_mean|.1f}\\% in 2022, @{" + C + ".r_19_mean|.1f}\\% in 2019",
           "în procente, aproape nimic: $\\hat\\sigma$ lunar mediu de @{" + C + ".r_26_mean|.1f}\\% în 2026, @{" + C + ".r_22_mean|.1f}\\% în 2022, @{" + C + ".r_19_mean|.1f}\\% în 2019"),
         t("in EUR/MWh it doubled from 2019 (@{" + C + ".e_19_mean|.1f} $\\to$ @{" + C + ".e_26_mean|.1f}), but its peak month, @{" + C + ".peak_sd|.1f} (@{" + C + ".peak_sd_month|ym}), stays far below 2022 (@{" + C + ".sd_22_max|.1f}, @{" + C + ".sd_22_max_month|ym})",
           "în EUR/MWh s-a dublat față de 2019 (@{" + C + ".e_19_mean|.1f} $\\to$ @{" + C + ".e_26_mean|.1f}), dar luna cu valoarea maximă, @{" + C + ".peak_sd|.1f} (@{" + C + ".peak_sd_month|ym}), rămîne mult sub 2022 (@{" + C + ".sd_22_max|.1f}, @{" + C + ".sd_22_max_month|ym})"),
         t("turbulent regime: @{ms.eur.by_year.2026|.0f}\\% of the days of 2026 (2022: @{ms.eur.by_year.2022|.0f}\\%); probability @{ms.eur.last_prob|.2f} on @{data.end|date}",
           "regimul agitat: @{ms.eur.by_year.2026|.0f}\\% din zilele anului 2026 (2022: @{ms.eur.by_year.2022|.0f}\\%); probabilitatea la @{data.end|date}: @{ms.eur.last_prob|.2f}"),
         t("Brent: GARCH volatility up to @{" + C + ".brent_cv_2026max|.0f}\\% annualised (@{" + C + ".brent_cv_2026max_date|date}), against @{" + C + ".brent_cv_2025|.0f}\\% on average in 2025",
           "Brent: volatilitatea GARCH a ajuns la @{" + C + ".brent_cv_2026max|.0f}\\% pe an (@{" + C + ".brent_cv_2026max_date|date}), față de o medie de @{" + C + ".brent_cv_2025|.0f}\\% în 2025")),
        (t("\\textbf{Verdict}", "\\textbf{Concluzia}"),
         t("a shock to the price level, with a turbulent regime about half of the time since July; not (yet) a 2022",
           "un șoc al nivelului prețului, cu regim agitat în circa jumătate din zile începînd cu luna iulie; nu (încă) o criză de tipul celei din 2022")), sep="3pt") +
        D.bottom(t("a supplier renewing contracts in November 2026 should price risk on the higher level, not on a new volatility regime.",
                   "un furnizor care reînnoiește contractele în noiembrie 2026 trebuie să includă în preț riscul asociat nivelului mai ridicat, nu unui nou regim de volatilitate."), NB + " \\S8"),
        "footnotesize", cite=t("(" + OWN + "; World Bank Pink Sheet; Yahoo Finance)", "(" + OWN + "; Banca Mondială, Pink Sheet; Yahoo Finance)"))

    D.chart(t("Case study: the one-day GARCH-t band held over the test year",
              "Studiu de caz: banda GARCH-t de o zi a fost corectă în anul de test"),
            "case_band", [
                t(("Band = forecast price $\\pm$ Student quantile $\\times\\hat\\sigma_t$, set on $t-1$",
                   "@{fc.eur.band_out} of @{fc.n} days outside (@{fc.eur.band_out_pct|.1f}\\%, 10\\% expected): @{case.band_out_first|.1f}\\% from November to April, @{case.band_out_last|.1f}\\% from May to October",
                   "mean half-width @{case.band_w_first|.0f} EUR/MWh in the first half, @{case.band_w_last|.0f} in September--October"),
                  ("Banda = prețul prognozat $\\pm$ cuantila Student $\\times\\hat\\sigma_t$, stabilită în ziua $t-1$",
                   "@{fc.eur.band_out} din @{fc.n} " + de("fc.n") + "zile în afara benzii (@{fc.eur.band_out_pct|.1f}\\%, față de 10\\% așteptat): @{case.band_out_first|.1f}\\% între noiembrie și aprilie, @{case.band_out_last|.1f}\\% între mai și octombrie",
                   "semilățimea medie: @{case.band_w_first|.0f} EUR/MWh în prima jumătate, @{case.band_w_last|.0f} în septembrie--octombrie"))],
            height="0.55\\textheight",
            job=t("a supplier can set its daily purchase limit from this band; the formal tests of such bands come in Lecture 4.",
                  "un furnizor își poate fixa limita zilnică de achiziție pe baza acestei benzi; testele formale ale acestor benzi se studiază în cursul 4."),
            tryit=NB + " \\S8", cite=t("(" + OWN + ", " + TEST + ")", "(" + OWN + ")"))   # RO: test year already in the source line; keeps the footer on one line

    D.chart(t("Case study: November 2026 limits and the April oil shock",
              "Studiu de caz: limitele pentru noiembrie 2026 și șocul din aprilie"),
            "term_structure", [
                t(("Romania, @{data.end|date}: $\\hat\\sigma$ = @{ts.eur.s1|.1f} EUR/MWh, close to the long-run @{ts.eur.lr|.1f}",
                   "one-day 90\\% limit about $\\pm$@{ts.eur.lim1|.0f} EUR/MWh for each day of November; Brent: the band grows slower than $\\sigma\\sqrt{h}$"),
                  ("România, @{data.end|date}: $\\hat\\sigma$ = @{ts.eur.s1|.1f} EUR/MWh, aproape de nivelul de lungă durată, @{ts.eur.lr|.1f}",
                   "limita de 90\\% pentru o zi: circa $\\pm$@{ts.eur.lim1|.0f} EUR/MWh în fiecare zi din noiembrie; Brent: banda crește mai lent decît $\\sigma\\sqrt{h}$"))],
            height="0.50\\textheight",
            job=t("set limits from the forecast term structure, not from today's volatility.",
                  "stabiliți limitele după structura la termen a prognozei, nu după volatilitatea de azi."),
            tryit=NB + " \\S8", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    c3 = "c3"
    D.frame(t("Case study C3: Romanian energy shares are weakly tied to oil",
              "Studiul de caz C3: acțiunile energetice, slab corelate cu petrolul"), it(
        (t("\\textbf{What the paper did} (Grecu, Cramer, Pele \\& Lessmann, 2025)", "\\textbf{Ce a făcut lucrarea} (Grecu, Cramer, Pele \\& Lessmann, 2025)"),
         t("data: stock indices of the 27 European Union countries, Brent and TTF futures, 2010--2023",
           "date: indicii bursieri ai celor 27 de state ale Uniunii Europene, contractele futures pe Brent și TTF, 2010--2023"),
         t("method: GARCH volatility for each series, then a dynamic conditional correlation (DCC) for each day; a Markov model for regimes of that correlation",
           "metodă: volatilitatea fiecărei serii cu un model GARCH, apoi o corelație condiționată dinamică (DCC) pentru fiecare zi; un model Markov pentru regimurile acestei corelații"),
         t("result: the correlation with oil is mostly between 0 and 0.4; Central and Eastern Europe (CEE) is the least correlated region; regimes persist above 98\\%",
           "rezultat: corelația cu petrolul este în general între 0 și 0{,}4; Europa Centrală și de Est (ECE) este regiunea cel mai slab corelată; regimurile persistă cu probabilitate de peste 98\\%")),
        (t("\\textbf{Our replication} (OMV Petrom, Romgaz (SNG), Nuclearelectrica (SNN) vs Brent, @{c3.nObs|,d} days)",
           "\\textbf{Replicarea noastră} (OMV Petrom, Romgaz (SNG), Nuclearelectrica (SNN) față de Brent, @{c3.nObs|,d} de zile)"),
         t("DCC parameters $a$ = @{c3.dccA|.3f}, $b$ = @{c3.dccB|.3f}: a slow, very persistent correlation",
           "parametrii DCC: $a$ = @{c3.dccA|.3f}, $b$ = @{c3.dccB|.3f}; corelația reacționează lent și este foarte persistentă"),
         t("mean correlation @{c3.rhoMean|.2f}; maximum @{c3.rhoMax|.2f} in @{c3.rhoMaxYear}, minimum @{c3.rhoMin|.2f} in @{c3.rhoMinYear}: the calendar of the paper",
           "corelația medie: @{c3.rhoMean|.2f}; maximum @{c3.rhoMax|.2f} în @{c3.rhoMaxYear}, minimum @{c3.rhoMin|.2f} în @{c3.rhoMinYear}, aceeași cronologie ca în lucrare"),
         t("hedging the basket with Brent, out of sample: variance change @{c3.effDyn|+.1f}\\% (dynamic), @{c3.effStatic|+.1f}\\% (static); negative = more risk",
           "acoperirea riscului coșului cu Brent, în afara eșantionului: variația varianței @{c3.effDyn|+.1f}\\% (dinamic), @{c3.effStatic|+.1f}\\% (static); valoare negativă = risc mai mare")),
        sep="3pt") + note(t("C3 numbers are computed by the C3 case notebook on our data; the paper's own results are in the case brief.",
                            "Cifrele C3 sînt calculate cu notebook-ul Jupyter al studiului de caz C3, pe datele noastre; rezultatele lucrării sînt prezentate în fișa studiului de caz.")) +
        D.bottom(t("the risk of Romanian energy shares is regulatory and local; a Brent hedge does not reduce it.",
                   "riscul acțiunilor energetice românești ține de reglementare și de piața locală; acoperirea cu Brent nu îl reduce.")),
        "footnotesize", cite="(Grecu, Cramer, Pele \\& Lessmann, 2025, NAJEF; " + t("case study C3", "studiul de caz C3") + ")")

    # ------------------------------------------------------------------ wrap-up
    D.parts.append("\\section*{" + t("Wrap-up", "Recapitulare") + "}\n")
    D.quiz_frame(t("half-life of an oil shock", "timpul de înjumătățire al unui șoc petrolier"),
                 t("For Brent, GARCH(1,1)-t gives $\\hat\\alpha+\\hat\\beta$ = @{xm.BRENT.pers|.3f}; after a shock, how long until half of the extra variance is gone?",
                   "Pentru Brent, GARCH(1,1)-t dă $\\hat\\alpha+\\hat\\beta$ = @{xm.BRENT.pers|.3f}; după un șoc, în cît timp dispare jumătate din varianța suplimentară?"),
                 t("$h_{1/2}=\\ln 0.5/\\ln$ @{xm.BRENT.pers|.3f} = @{xm.BRENT.hl|.1f} trading days, about @{xm.BRENT.hl_weeks|.0f} weeks: limits stay wider for weeks, not days.",
                   "$h_{1/2}=\\ln 0{,}5/\\ln$ @{xm.BRENT.pers|.3f} = @{xm.BRENT.hl|.1f} zile lucrătoare, circa @{xm.BRENT.hl_weeks|.0f} săptămîni: limitele rămîn mai largi săptămîni întregi, nu cîteva zile."))
    D.quiz_frame(t("percent or euro", "procente sau euro"),
                 t("In 2022 the percent volatility of the Romanian price was the same as in 2019; did the risk of a supplier's open position of 10 MW change?",
                   "În 2022, volatilitatea procentuală a prețului din România a fost aceeași ca în 2019; s-a schimbat riscul unei poziții deschise de 10 MW a unui furnizor?"),
                 t("Yes: the position loses or gains in EUR, and the EUR/MWh volatility of the shocks rose @{voly.ratio_eur_22_19|.1f} times, with the price level.",
                   "Da: poziția cîștigă sau pierde în euro, iar volatilitatea șocurilor în EUR/MWh a crescut de @{voly.ratio_eur_22_19|.1f} ori, odată cu nivelul prețului."))
    D.quiz_frame(t("a Monday jump", "creșterea de luni"),
                 t("The PZU price rises by 35\\% from Sunday to Monday; should the risk desk widen the limits?",
                   "Prețul PZU crește cu 35\\% de duminică pînă luni; trebuie departamentul de risc să lărgească limitele?"),
                 t("No: on average Monday is @{mean.dow_pct.Mon|+.0f}\\% above Sunday; the calendar is forecast by the mean equation, and only the shock $\\varepsilon_t$ (here almost zero) enters GARCH.",
                   "Nu: în medie, prețul de luni este cu @{mean.dow_pct.Mon|.0f}\\% mai mare decît cel de duminică; calendarul este inclus în ecuația mediei, iar în modelul GARCH intră doar șocul $\\varepsilon_t$, aici aproape zero."))
    D.quiz_frame(t("choosing a volatility model", "alegerea modelului de volatilitate"),
                 t("A vendor's volatility model has the lowest mean squared error on your test year, thanks to three extreme days; what do you ask for?",
                   "Modelul de volatilitate al unui furnizor are cea mai mică eroare pătratică medie în anul de test, datorită a trei zile extreme; ce îi cereți?"),
                 t("QLIKE on the same days and a DM test against GARCH-t and the 30-day history; on our test year the best QLIKE in EUR/MWh is " +
                   bestn[FC["eur"]["best"]] + ", not significantly better than GARCH-t.",
                   "Valoarea QLIKE pe aceleași zile și un test DM față de GARCH-t și de varianța istorică pe 30 de zile; în anul nostru de test, cel mai bun QLIKE în EUR/MWh îl are " +
                   bestn[FC["eur"]["best"]] + ", fără a fi semnificativ mai bun decît GARCH-t."))
    D.quiz_frame(t("after a rise or after a fall", "după o creștere sau după o scădere"),
                 t("Yesterday the price moved by @{garch.eur.nic_2sd|.0f} EUR/MWh; for a buyer, is tomorrow riskier if it was a rise or a fall?",
                   "Ieri prețul s-a modificat cu @{garch.eur.nic_2sd|.0f} EUR/MWh; pentru un cumpărător, ziua de mîine este mai riscantă după o creștere sau după o scădere?"),
                 t("After a rise: the GJR model in EUR/MWh gives $\\sigma$ = @{garch.eur.nic_up2|.1f} after a rise, @{garch.eur.nic_dn2|.1f} after a fall (inverse leverage effect).",
                   "După o creștere: modelul GJR în EUR/MWh dă $\\sigma$ = @{garch.eur.nic_up2|.1f} după o creștere și @{garch.eur.nic_dn2|.1f} după o scădere (efectul de levier invers)."))

    D.frame(t("Wrap-up", "Recapitulare"), "\\vspace{-2mm}\\begin{multicols}{2}\\scriptsize\\tableofcontents[hideallsubsections]\\end{multicols}\n" + it(
        (t("\\textbf{Measure}", "\\textbf{Măsurare}"),
         t("remove the weekly calendar first; in percent the crisis was not more volatile, in EUR/MWh it was @{voly.ratio_eur_22_19|.1f} times more",
           "mai întîi se elimină calendarul săptămînal; în procente criza nu a fost mai volatilă, în EUR/MWh volatilitatea a fost de @{voly.ratio_eur_22_19|.1f} ori mai mare")),
        (t("\\textbf{Model and forecast}", "\\textbf{Modelare și prognoză}"),
         t("GARCH-t is the default; oil shocks halve in about @{xm.BRENT.hl_weeks|.0f} weeks; next: risk measures for energy companies (Lecture 4)",
           "GARCH-t este modelul implicit; șocurile petrolului se înjumătățesc în circa @{xm.BRENT.hl_weeks|.0f} săptămîni; cursul următor: măsurarea riscului în companiile energetice (cursul 4)")),
        sep="1pt"))

    D.frame(t("Research from our group on volatility and risk", "Cercetările grupului nostru despre volatilitate și risc"), it(
        (t("\\textbf{Energy prices and EU stock markets} (Grecu, Cramer, Pele \\& Lessmann, 2025, NAJEF)", "\\textbf{Prețurile energiei și bursele din UE} (Grecu, Cramer, Pele \\& Lessmann, 2025, NAJEF)"),
         t("what it did: GARCH volatility, daily DCC correlations and Markov regimes for 27 national indices against oil and gas, 2010--2023",
           "ce a făcut lucrarea: volatilitate GARCH, corelații DCC zilnice și regimuri Markov pentru 27 de indici naționali, față de petrol și gaze, 2010--2023"),
         t("result: European markets follow oil more than gas, with persistent regimes (case study C3)",
           "rezultat: piețele europene urmează mai mult petrolul decît gazele, cu regimuri persistente (studiul de caz C3)")),
        (t("\\textbf{Entropy and market risk} (Pele, Lazar \\& Dufour, 2017, Entropy)", "\\textbf{Entropia și riscul de piață} (Pele, Lazar \\& Dufour, 2017, Entropy)"),
         t("what it did: measured the entropy of intraday euro--yen returns and related it to intraday value at risk (VaR) and expected shortfall (ES)",
           "ce a făcut lucrarea: a măsurat entropia randamentelor intrazilnice euro--yen și a legat-o de valoarea expusă la risc (VaR) și de pierderea medie în coada distribuției (ES)"),
         t("result: a negative relation between entropy and intraday VaR and ES; intraday entropy is then used to forecast the daily VaR",
           "rezultat: o relație negativă între entropie și VaR, respectiv ES intrazilnic; entropia intrazilnică servește apoi la prognoza VaR zilnic")),
        (t("\\textbf{High-frequency entropy for daily risk} (Pele \\& Mazurencu-Marinescu-Pele, 2019, Entropy)", "\\textbf{Entropia datelor de înaltă frecvență și riscul zilnic} (Pele \\& Mazurencu-Marinescu-Pele, 2019, Entropy)"),
         t("what it did: used the entropy of intraday Bitcoin returns to forecast the daily VaR, against classical GARCH models",
           "ce a făcut lucrarea: a folosit entropia randamentelor intrazilnice ale Bitcoin pentru prognoza VaR zilnic, comparativ cu modelele GARCH clasice"),
         t("result: the entropy-based VaR forecast performs best in the backtests: intraday data carry information on daily risk",
           "rezultat: prognoza VaR bazată pe entropie dă cele mai bune rezultate la testare; datele intrazilnice conțin informație despre riscul zilnic")),
        (t("\\textbf{Energy Financial Risk Meter} (Toma, Dima, Grecu, Pele \\& Lessmann, 2026, SSRN)", "\\textbf{Energy Financial Risk Meter} (Toma, Dima, Grecu, Pele \\& Lessmann, 2026, SSRN)"),
         t("what it did: a systemic-risk indicator for the EU energy sector; preview of Lecture 4", "ce a făcut lucrarea: un indicator al riscului sistemic pentru sectorul energetic din UE; tema cursului 4")),
        sep="1pt") + note(t("Findings as stated in the papers; numbers on the other slides come from our own data.",
                            "Rezultatele de pe acest diapozitiv sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.")),
        "footnotesize", cite=t("(Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting)",
                               "(Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică)"))

    D.frame(t("Want to learn more?", "Lecturi și resurse suplimentare"), cols(it(
        t("\\textbf{R.\\,F.\\ Engle, GARCH 101} (2001): the clearest short introduction, by the Nobel laureate who invented ARCH --- ",
          "\\textbf{R.\\,F.\\ Engle, GARCH 101} (2001): cea mai clară introducere scurtă, scrisă de laureatul Nobel care a propus modelul ARCH --- ") +
        "\\href{https://doi.org/10.1257/jep.15.4.157}{doi:10.1257/jep.15.4.157}.",
        t("\\textbf{R.\\ Weron, Modeling and Forecasting Electricity Loads and Prices} (Wiley, 2006): stylised facts and volatility of power prices.",
          "\\textbf{R.\\ Weron, Modeling and Forecasting Electricity Loads and Prices} (Wiley, 2006): faptele stilizate și volatilitatea prețurilor energiei electrice."),
        t("\\textbf{The \\texttt{arch} Python package} (K.\\ Sheppard), used for every model of this lecture: ",
          "\\textbf{Pachetul Python \\texttt{arch}} (K.\\ Sheppard), folosit pentru toate modelele din acest curs: ") +
        "\\href{https://arch.readthedocs.io}{arch.readthedocs.io}.", sep="4pt"),
        it(t("\\textbf{This course}: code, data, notebooks --- ", "\\textbf{Acest curs}: cod, date, notebook-uri Jupyter --- ") +
           "\\href{https://github.com/danpele/EMQA}{github.com/danpele/EMQA}.",
           t("\\textbf{Case study C3}: the DCC model and the Brent hedge for Romanian energy shares, step by step.",
             "\\textbf{Studiul de caz C3}: modelul DCC și acoperirea cu Brent pentru acțiunile energetice românești, pas cu pas."),
           t("\\textbf{Experiment yourself}: the notebook reproduces every chart and number of this lecture --- ",
             "\\textbf{Exercițiu practic}: notebook-ul Jupyter reproduce toate graficele și cifrele din acest curs --- ") +
           "\\href{\\emqarepo/\\emqanb}{notebooks/}.", sep="4pt"), "0.52", "0.45"))

    REFS = [
        "Andersen, T.\\,G.\\ \\& Bollerslev, T.\\ (1998). Answering the skeptics: Yes, standard volatility models do provide accurate forecasts. "
        "\\textit{International Economic Review}, 39(4), 885--905. \\href{https://doi.org/10.2307/2527343}{doi:10.2307/2527343}",
        "Bollerslev, T.\\ (1986). Generalized autoregressive conditional heteroskedasticity. \\textit{Journal of Econometrics}, 31(3), 307--327. "
        "\\href{https://doi.org/10.1016/0304-4076(86)90063-1}{doi:10.1016/0304-4076(86)90063-1}",
        "Bollerslev, T.\\ (1987). A conditionally heteroskedastic time series model for speculative prices and rates of return. "
        "\\textit{Review of Economics and Statistics}, 69(3), 542--547. \\href{https://doi.org/10.2307/1925546}{doi:10.2307/1925546}",
        "Corsi, F.\\ (2009). A simple approximate long-memory model of realized volatility. \\textit{Journal of Financial Econometrics}, 7(2), 174--196. "
        "\\href{https://doi.org/10.1093/jjfinec/nbp001}{doi:10.1093/jjfinec/nbp001}",
        "Diebold, F.\\,X.\\ \\& Mariano, R.\\,S.\\ (1995). Comparing predictive accuracy. \\textit{Journal of Business \\& Economic Statistics}, 13(3), 253--263. "
        "\\href{https://doi.org/10.1080/07350015.1995.10524599}{doi:10.1080/07350015.1995.10524599}",
        "Engle, R.\\,F.\\ (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. "
        "\\textit{Econometrica}, 50(4), 987--1007. \\href{https://doi.org/10.2307/1912773}{doi:10.2307/1912773}",
        "Engle, R.\\,F.\\ (2001). GARCH 101: The use of ARCH/GARCH models in applied econometrics. \\textit{Journal of Economic Perspectives}, 15(4), 157--168. "
        "\\href{https://doi.org/10.1257/jep.15.4.157}{doi:10.1257/jep.15.4.157}",
        "Engle, R.\\,F.\\ \\& Ng, V.\\,K.\\ (1993). Measuring and testing the impact of news on volatility. \\textit{Journal of Finance}, 48(5), 1749--1778. "
        "\\href{https://doi.org/10.1111/j.1540-6261.1993.tb05127.x}{doi:10.1111/j.1540-6261.1993.tb05127.x}",
        "Glosten, L.\\,R., Jagannathan, R.\\ \\& Runkle, D.\\,E.\\ (1993). On the relation between the expected value and the volatility of the nominal excess "
        "return on stocks. \\textit{Journal of Finance}, 48(5), 1779--1801. \\href{https://doi.org/10.1111/j.1540-6261.1993.tb05128.x}{doi:10.1111/j.1540-6261.1993.tb05128.x}",
        "Grecu, R.\\,A., Cramer, A.\\,A., Pele, D.\\,T.\\ \\& Lessmann, S.\\ (2025). The link between energy prices and stock markets in European Union countries. "
        "\\textit{North American Journal of Economics and Finance}, 78, 102420. \\href{https://doi.org/10.1016/j.najef.2025.102420}{doi:10.1016/j.najef.2025.102420}",
        "Hamilton, J.\\,D.\\ (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. \\textit{Econometrica}, 57(2), 357--384. "
        "\\href{https://doi.org/10.2307/1912559}{doi:10.2307/1912559}",
        "Hansen, P.\\,R.\\ \\& Lunde, A.\\ (2005). A forecast comparison of volatility models: Does anything beat a GARCH(1,1)? \\textit{Journal of Applied Econometrics}, "
        "20(7), 873--889. \\href{https://doi.org/10.1002/jae.800}{doi:10.1002/jae.800}",
        "Knittel, C.\\,R.\\ \\& Roberts, M.\\,R.\\ (2005). An empirical examination of restructured electricity prices. \\textit{Energy Economics}, 27(5), 791--817. "
        "\\href{https://doi.org/10.1016/j.eneco.2004.11.005}{doi:10.1016/j.eneco.2004.11.005}",
        "Lamoureux, C.\\,G.\\ \\& Lastrapes, W.\\,D.\\ (1990). Persistence in variance, structural change, and the GARCH model. \\textit{Journal of Business \\& Economic "
        "Statistics}, 8(2), 225--234. \\href{https://doi.org/10.1080/07350015.1990.10509794}{doi:10.1080/07350015.1990.10509794}",
        "Ljung, G.\\,M.\\ \\& Box, G.\\,E.\\,P.\\ (1978). On a measure of lack of fit in time series models. \\textit{Biometrika}, 65(2), 297--303. "
        "\\href{https://doi.org/10.1093/biomet/65.2.297}{doi:10.1093/biomet/65.2.297}",
        "Nelson, D.\\,B.\\ (1991). Conditional heteroskedasticity in asset returns: A new approach. \\textit{Econometrica}, 59(2), 347--370. "
        "\\href{https://doi.org/10.2307/2938260}{doi:10.2307/2938260}",
        "Patton, A.\\,J.\\ (2011). Volatility forecast comparison using imperfect volatility proxies. \\textit{Journal of Econometrics}, 160(1), 246--256. "
        "\\href{https://doi.org/10.1016/j.jeconom.2010.03.034}{doi:10.1016/j.jeconom.2010.03.034}",
        "Pele, D.\\,T., Lazar, E.\\ \\& Dufour, A.\\ (2017). Information entropy and measures of market risk. \\textit{Entropy}, 19(5), 226. "
        "\\href{https://doi.org/10.3390/e19050226}{doi:10.3390/e19050226}",
        "Pele, D.\\,T.\\ \\& Mazurencu-Marinescu-Pele, M.\\ (2019). Using high-frequency entropy to forecast Bitcoin's daily value at risk. \\textit{Entropy}, 21(2), 102. "
        "\\href{https://doi.org/10.3390/e21020102}{doi:10.3390/e21020102}",
        "RiskMetrics (1996). \\textit{RiskMetrics --- Technical Document}, 4th ed. J.\\,P.\\ Morgan / Reuters, New York.",
        "Toma, F.-M., Dima, D.-M., Grecu, R., Pele, D.\\,T.\\ \\& Lessmann, S.\\ (2026). Energy Financial Risk Meter: Systemic risk in the EU energy sector. "
        "SSRN Working Paper 6985301. \\href{https://doi.org/10.2139/ssrn.6985301}{doi:10.2139/ssrn.6985301}",
        "Uniejewski, B., Weron, R.\\ \\& Ziel, F.\\ (2018). Variance stabilizing transformations for electricity spot price forecasting. \\textit{IEEE Transactions on "
        "Power Systems}, 33(2), 2219--2229. \\href{https://doi.org/10.1109/TPWRS.2017.2734563}{doi:10.1109/TPWRS.2017.2734563}",
        "Weron, R.\\ (2006). \\textit{Modeling and Forecasting Electricity Loads and Prices: A Statistical Approach}. Wiley, Chichester. "
        "\\href{https://doi.org/10.1002/9781118673362}{doi:10.1002/9781118673362}",
        "Weron, R.\\ (2014). Electricity price forecasting: A review of the state-of-the-art with a look into the future. \\textit{International Journal of Forecasting}, "
        "30(4), 1030--1081. \\href{https://doi.org/10.1016/j.ijforecast.2014.08.008}{doi:10.1016/j.ijforecast.2014.08.008}",
    ]
    for part, (a_, b_) in enumerate([(0, 8), (8, 16), (16, len(REFS))]):
        D.frame(t("References", "Bibliografie") + f" ({part + 1}/3)", "\\begin{itemize}\\setlength{\\itemsep}{1pt}\\scriptsize\n" +
                "\n".join("\\item " + r for r in REFS[a_:b_]) + "\n\\end{itemize}", "scriptsize")

    # ------------------------------------------------------------------ appendix
    D.mark_main_end()
    D.parts.append("\\section*{" + t("Appendix", "Anexă") + "}\n")
    D.frame(t("Appendix A: the Student-t likelihood of GARCH", "Anexa A: funcția de verosimilitate Student a modelului GARCH"), cols(
        "\\[ \\begin{aligned}\\ell(\\theta)=\\sum_{t=1}^{T}\\Bigl[&\\ln\\Gamma\\bigl(\\tfrac{\\nu+1}{2}\\bigr)-\\ln\\Gamma\\bigl(\\tfrac{\\nu}{2}\\bigr)-\\tfrac12\\ln\\bigl(\\pi(\\nu-2)\\bigr)\\\\ "
        "&-\\tfrac12\\ln\\sigma_t^2-\\tfrac{\\nu+1}{2}\\ln\\Bigl(1+\\frac{\\varepsilon_t^2}{(\\nu-2)\\sigma_t^2}\\Bigr)\\Bigr]\\end{aligned} \\]" + it(
            t("$\\theta=(\\omega,\\alpha,\\beta,\\nu)$; $\\Gamma$ = gamma function; the factor $\\nu-2$ gives the Student variable variance 1.",
              "$\\theta=(\\omega,\\alpha,\\beta,\\nu)$; $\\Gamma$ = funcția gamma; factorul $\\nu-2$ dă variabilei Student varianța 1."),
            t("Numerical maximisation under $\\omega>0$, $\\alpha,\\beta\\ge0$, $\\alpha+\\beta<1$, $\\nu>2$; robust standard errors; package \\texttt{arch}.",
              "Maximizare numerică cu $\\omega>0$, $\\alpha,\\beta\\ge0$, $\\alpha+\\beta<1$, $\\nu>2$; erori standard robuste; pachetul \\texttt{arch}."),
            t("Normal case: $\\ell=-\\tfrac12\\sum_t\\bigl[\\ln(2\\pi)+\\ln\\sigma_t^2+\\varepsilon_t^2/\\sigma_t^2\\bigr]$, the limit $\\nu\\to\\infty$.",
              "Cazul normal: $\\ell=-\\tfrac12\\sum_t\\bigl[\\ln(2\\pi)+\\ln\\sigma_t^2+\\varepsilon_t^2/\\sigma_t^2\\bigr]$, limita pentru $\\nu\\to\\infty$."), sep="3pt"),
        table("@{}lrr@{}", [t("GARCH(1,1)-t", "GARCH(1,1)-t"), t("\\%", "\\%"), "EUR/MWh"],
              [[p_, f"{fmt(V.get(f'garch.pct.garch_t.{k}'), '.3f', lang)} ({fmt(V.get(f'garch.pct.garch_t.{k}_se'), '.3f', lang)})",
                f"{fmt(V.get(f'garch.eur.garch_t.{k}'), '.3f', lang)} ({fmt(V.get(f'garch.eur.garch_t.{k}_se'), '.3f', lang)})"]
               for p_, k in [("$\\omega$", "omega"), ("$\\alpha$", "alpha"), ("$\\beta$", "beta"), ("$\\nu$", "nu")]],
              size="scriptsize", stretch="1.2") + note(t("Estimate (standard error).", "Estimația (eroarea standard).")), "0.56", "0.41"), "footnotesize",
        cite="(Bollerslev, 1987, RESTAT)")

    D.frame(t("Appendix B: multi-step forecast and half-life", "Anexa B: prognoza pe mai mulți pași și timpul de înjumătățire"), it(
        t(("\\textbf{Step 1}", "write $\\varepsilon_{t}^2=\\sigma_{t}^2+v_t$ with $\\E_{t-1}[v_t]=0$; then $\\sigma^2_{t+1}=\\omega+(\\alpha+\\beta)\\sigma_t^2+\\alpha v_t$"),
          ("\\textbf{Pasul 1}", "scriem $\\varepsilon_{t}^2=\\sigma_{t}^2+v_t$, cu $\\E_{t-1}[v_t]=0$; atunci $\\sigma^2_{t+1}=\\omega+(\\alpha+\\beta)\\sigma_t^2+\\alpha v_t$")),
        t(("\\textbf{Step 2}", "take expectations at $T$: $\\E_T[\\sigma^2_{T+h}]=\\omega+(\\alpha+\\beta)\\E_T[\\sigma^2_{T+h-1}]$ for $h\\ge2$",
           "subtract $\\bar\\sigma^2=\\omega+(\\alpha+\\beta)\\bar\\sigma^2$: the deviation from $\\bar\\sigma^2$ is multiplied by $\\alpha+\\beta$ every day"),
          ("\\textbf{Pasul 2}", "aplicăm media condiționată în $T$: $\\E_T[\\sigma^2_{T+h}]=\\omega+(\\alpha+\\beta)\\E_T[\\sigma^2_{T+h-1}]$, pentru $h\\ge2$",
           "scădem $\\bar\\sigma^2=\\omega+(\\alpha+\\beta)\\bar\\sigma^2$: abaterea față de $\\bar\\sigma^2$ se înmulțește în fiecare zi cu $\\alpha+\\beta$")),
        t(("\\textbf{Step 3}", "hence $\\E_T[\\sigma^2_{T+h}]-\\bar\\sigma^2=(\\alpha+\\beta)^{h-1}(\\sigma^2_{T+1}-\\bar\\sigma^2)$",
           "half of the deviation is left when $(\\alpha+\\beta)^{h}=1/2$, so $h_{1/2}=\\ln(1/2)/\\ln(\\alpha+\\beta)$"),
          ("\\textbf{Pasul 3}", "rezultă $\\E_T[\\sigma^2_{T+h}]-\\bar\\sigma^2=(\\alpha+\\beta)^{h-1}(\\sigma^2_{T+1}-\\bar\\sigma^2)$",
           "rămîne jumătate din abatere cînd $(\\alpha+\\beta)^{h}=1/2$, deci $h_{1/2}=\\ln(1/2)/\\ln(\\alpha+\\beta)$")),
        t(("\\textbf{GJR and EGARCH}", "GJR with a symmetric $z_t$: persistence $\\alpha+\\gamma/2+\\beta$, because $\\Pr(\\varepsilon<0)=1/2$",
           "EGARCH: $\\ln\\sigma_t^2$ follows an autoregression with coefficient $\\beta$; the persistence is $\\beta$"),
          ("\\textbf{GJR și EGARCH}", "GJR cu $z_t$ simetric: persistența este $\\alpha+\\gamma/2+\\beta$, deoarece $\\Pr(\\varepsilon<0)=1/2$",
           "EGARCH: $\\ln\\sigma_t^2$ urmează un proces autoregresiv cu coeficientul $\\beta$; persistența este $\\beta$")), sep="4pt"), "small",
        cite="(Engle, 2001, JEP; Bollerslev, 1986, JOE)")

    def crow(u, k, lab):
        s_ = GG[u][k]
        return [lab, fmt(s_["ll"], ",.1f", lang), fmt(s_["aic"], ",.1f", lang), fmt(s_["bic"], ",.1f", lang),
                fmt(s_.get("gamma"), ".3f", lang) if s_.get("gamma") is not None else "--", fmt(s_.get("nu"), ".2f", lang) if s_.get("nu") is not None else "--"]
    crows = [[lab] + [fmt(GG[u][k][c], ",.1f", lang) for u in ["pct", "eur"] for c in ["ll", "aic", "bic"]] for k, lab in MODS]
    D.frame(t("Appendix C: all six models, both units", "Anexa C: cele șase modele, în ambele unități de măsură"),
            "\\begin{center}" + table("@{}lrrrrrr@{}", [t("Model", "Modelul"), t("log-L, \\%", "log-L, \\%"), "AIC, \\%", "BIC, \\%",
                                                          "log-L, EUR", "AIC, EUR", "BIC, EUR"], crows, size="footnotesize", stretch="1.15") + "\\end{center}" + note(
        t("log-L = log-likelihood $\\hat\\ell$; AIC $=2k-2\\hat\\ell$, BIC $=k\\ln T-2\\hat\\ell$, $k$ = number of parameters; @{garch.pct.garch_t.n|,d} days, @{data.start|date} -- @{data.end|date}.",
          "log-L = log-verosimilitatea $\\hat\\ell$; AIC $=2k-2\\hat\\ell$, BIC $=k\\ln T-2\\hat\\ell$, $k$ = numărul de parametri; @{garch.pct.garch_t.n|,d} de zile, @{data.start|date} -- @{data.end|date}."),
        t("Asymmetry $\\hat\\gamma$ and $\\hat\\nu$: GJR-t @{garch.pct.gjr_t.gamma|.3f}, @{garch.pct.gjr_t.nu|.2f} (\\%); @{garch.eur.gjr_t.gamma|.3f}, @{garch.eur.gjr_t.nu|.2f} (EUR/MWh).",
          "Asimetria $\\hat\\gamma$ și $\\hat\\nu$: GJR-t @{garch.pct.gjr_t.gamma|.3f}, @{garch.pct.gjr_t.nu|.2f} (\\%); @{garch.eur.gjr_t.gamma|.3f}, @{garch.eur.gjr_t.nu|.2f} (EUR/MWh).")), "small",
        cite="(Glosten, Jagannathan \\& Runkle, 1993; Nelson, 1991)")

    D.frame(t("Appendix D: the Hamilton filter and the robustness of QLIKE", "Anexa D: filtrul Hamilton și robustețea funcției QLIKE"), it(
        t(("\\textbf{Hamilton filter} (Markov switching)", "predict: $\\Pr(s_t=j\\mid\\mathcal F_{t-1})=\\sum_i p_{ij}\\Pr(s_{t-1}=i\\mid\\mathcal F_{t-1})$",
           "update: multiply by the normal density of $u_t$ in regime $j$ and normalise; the log of the normaliser summed over $t$ is the log-likelihood",
           "smoothed probabilities (the chart) use all the data, filtered ones only the past; a real-time warning must use the filtered ones"),
          ("\\textbf{Filtrul Hamilton} (modelul Markov)", "predicția: $\\Pr(s_t=j\\mid\\mathcal F_{t-1})=\\sum_i p_{ij}\\Pr(s_{t-1}=i\\mid\\mathcal F_{t-1})$",
           "actualizarea: se înmulțește cu densitatea normală a lui $u_t$ în regimul $j$ și se normalizează; suma logaritmilor constantelor de normalizare este log-verosimilitatea",
           "probabilitățile netezite (din grafic) folosesc toate datele, cele filtrate doar trecutul; o avertizare în timp real trebuie să folosească probabilitățile filtrate")),
        t(("\\textbf{Why QLIKE}", "with $\\E_{t-1}[\\varepsilon_t^2]=\\sigma_t^2$, the expected QLIKE is minimised only at $\\hat\\sigma_t^2=\\sigma_t^2$, whatever the noise of $\\varepsilon_t^2$",
           "the same holds for MSE; losses such as $|\\varepsilon_t|-\\hat\\sigma_t$ or $\\ln$-errors can rank models wrongly (Patton, 2011)",
           "DM statistic: mean daily loss difference over its Newey--West standard error (7 lags), asymptotically normal"),
          ("\\textbf{De ce QLIKE}", "dacă $\\E_{t-1}[\\varepsilon_t^2]=\\sigma_t^2$, valoarea așteptată a QLIKE este minimă numai pentru $\\hat\\sigma_t^2=\\sigma_t^2$, oricît de zgomotos ar fi $\\varepsilon_t^2$",
           "același lucru este valabil pentru MSE; alte funcții, ca $|\\varepsilon_t|-\\hat\\sigma_t$ sau erorile logaritmice, pot ordona greșit modelele (Patton, 2011)",
           "statistica DM: media diferențelor zilnice de pierdere împărțită la eroarea ei standard Newey--West (7 decalaje); asimptotic normală")), sep="4pt"), "small",
        cite="(Hamilton, 1989; Patton, 2011, JOE; Diebold \\& Mariano, 1995)")
    return D


def main(langs):
    ok = True
    for lang in langs:
        name = "lecture3" if lang == "en" else "lecture3_ro"
        out = os.path.join(HERE, name + ".tex")
        D, tex, res, H = autofit(build, out, lang)
        print(f"[{lang}] frames: main {D.n_main} (incl. title and section outlines), total {D.n_frames}; quiz frames {D.quiz}; "
              f"pages {res['pages']}; errors {res['errors']}; overfull>1pt {len(res['overfull'])}")
        for kind, amt, title in res["where"]:
            print(f"     {kind} {amt:6.1f}pt  {title}")
        small = {k: v for k, v in D.used_h.items() if v < 0.40}
        print(f"[{lang}] figure heights (fraction of text height) below 0.40:", small)
        defined = set(ABBR) - ({"UE", "ECE"} if lang == "en" else {"EU", "CEE"})
        # the RO deck keeps English titles in the reference list (e.g. "the EU energy sector")
        print(f"[{lang}] acronyms missing from Abbreviations:", acronym_audit(tex, defined, IGNORE | ({"EU"} if lang == "ro" else set())))
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
