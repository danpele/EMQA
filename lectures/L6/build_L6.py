r"""
build_L6.py -- Lecture 6 "Renewables and storage" (EMQA), English and Romanian from one source
=============================================================================================
Writes lectures/L6/lecture6.tex (EN) and lectures/L6/lecture6_ro.tex (RO) from the bilingual slide text in this file and
the numbers in L6_numbers.json (produced by analysis_L6.py), compiles both with pdflatex and checks: 0 LaTeX errors; no
overfull box > 1 pt (nothing masked); every acronym in the Abbreviations frames and spelled out at first use; contact sheets.

Run (from the repository root):
    python3 data/download_L6.py           # once: 15-min generation (RO, BG, HU) and installed capacity
    python3 lectures/L6/analysis_L6.py
    python3 lectures/L6/build_L6.py       # both languages;  add "en" or "ro" for one

Hand-typed numbers are definitions and assumptions only: 1 MW, 1/2/4 h of storage, 85% round-trip efficiency, one cycle a
day, 15-year life (Cole & Karmakar, 2023, NREL), 8% discount rate (assumption), 15 min = 0.25 h, institutional dates.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_build import (Deck, Numbers, acronym_audit, autofit, block, cols, contact_sheet,  # noqa: E402
                        first_use_audit, fmt, heat, hier, items, seq, table)


def it(*xs, sep="1pt"):
    """Bullets: a string is split by hier() (first clause = level 1, the rest = level 2); a tuple
    (head, sub1, sub2, ...) gives an explicit level-1 head with its level-2 bullets."""
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
    "AI": ("artificial intelligence", "inteligență artificială"),
    "BG": ("Bulgaria (bidding zone)", "Bulgaria (zonă de ofertare)"),
    "CET": ("Central European Time", "ora Europei Centrale"),
    "CP": ("capture price", "prețul capturat"),
    "CR": ("capture rate (value factor)", "rata de captare"),
    "DE-LU": ("Germany--Luxembourg bidding zone", "zona de ofertare Germania--Luxemburg"),
    "ENTSO-E": ("European Network of Transmission System Operators for Electricity",
                "Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică"),
    "EPEX": ("EPEX SPOT power exchange", "bursa europeană de energie EPEX SPOT"),
    "HAC": ("heteroskedasticity- and autocorrelation-consistent (standard errors)",
            "(erori standard) robuste la heteroscedasticitate și autocorelare"),
    "HU": ("Hungary (bidding zone)", "Ungaria (zonă de ofertare)"),
    "HUPX": ("Hungarian Power Exchange", "bursa de energie din Ungaria"),
    "IBEX": ("Independent Bulgarian Energy Exchange", "bursa independentă de energie din Bulgaria"),
    "ISE": ("Fraunhofer Institute for Solar Energy Systems", "Institutul Fraunhofer pentru Sisteme de Energie Solară"),
    "LP": ("linear programme", "program liniar (problemă de programare liniară)"),
    "MTU": ("market time unit", "intervalul de tranzacționare (market time unit)"),
    "NREL": ("National Renewable Energy Laboratory (United States)", "Laboratorul Național pentru Energie Regenerabilă (Statele Unite)"),
    "OLS": ("ordinary least squares", "metoda celor mai mici pătrate"),
    "OPCOM": ("Romanian electricity and gas market operator", "operatorul pieței de energie electrică și de gaze naturale din România"),
    "PPA": ("power purchase agreement", "contract bilateral de vînzare a energiei pe termen lung (power purchase agreement)"),
    "PZU": ("Piața pentru Ziua Următoare (day-ahead market)", "piața pentru ziua următoare"),
    "RO": ("Romania (bidding zone)", "România (zonă de ofertare)"),
    "SDAC": ("Single Day-Ahead Coupling", "cuplarea unică a piețelor pentru ziua următoare"),
    "SE": ("standard error", "eroarea standard"),
    "XML": ("Extensible Markup Language (data file format)", "format de fișier de date Extensible Markup Language"),
    "EUR": ("euro", "euro"), "MW": ("megawatt", "megawatt"), "MWh": ("megawatt-hour", "megawatt-oră"),
    "GW": ("gigawatt = 1\\,000 MW", "gigawatt = 1\\,000 MW"), "TWh": ("terawatt-hour", "terawatt-oră"),
    "kW": ("kilowatt", "kilowatt"), "kWh": ("kilowatt-hour", "kilowatt-oră"),
}
UNITS = {"EUR", "MW", "MWh", "TWh", "GW", "kW", "kWh"}
# journal codes inside citations only; everything else must be in the Abbreviations list and spelled out
IGNORE = {"AI", "ReP", "EMQA", "IJF", "ENEECO", "ENPOL", "APEN", "JSES", "PICBE", "SPOT", "CO", "II", "NEMO", "TP", "IV", "III", "PJM", "SHAP", "HiGHS", "SOURCES",
          "AIDA", "SSRN", "CEE"}   # conference, repository and a word of a talk title, in citations and references only


def build(lang, H=None):
    V = Numbers(os.path.join(HERE, "L6_numbers.json"), lang)
    N = V.N
    D = Deck(6, "Renewables and Storage: Cannibalisation, Negative Prices and Batteries" if lang == "en" else
             "Surse regenerabile și stocare: canibalizare, prețuri negative și baterii", V, lang, heights=H)
    t = D.t
    ro = lang == "ro"
    if ro:   # notebook pointer in natural Romanian: "notebook-ul Jupyter, secțiunea 2"
        _tex = D.tex
        D.tex = lambda: _tex().replace("notebook-ul Jupyter \\S", "notebook-ul Jupyter, secțiunea ")
    NB = t("notebook", "notebook-ul Jupyter")

    def de(key):
        v = int(round(abs(float(V.get(key)))))
        return "de " if ro and v >= 20 and (v % 100 >= 20 or v % 100 == 0) else ""

    Y = N["Y"]
    YTD = t("Jan--Oct @{Y}", "ian.--oct. @{Y}") if N["cutoff"]["month"] == 10 else t("@{data.ytd_label_en}", "@{data.ytd_label_ro}")
    LTM = t("last 12 months (@{cutoff.ltm_start|ym} -- @{cutoff.ltm_end|ym})", "ultimele 12 luni (@{cutoff.ltm_start|ym} -- @{cutoff.ltm_end|ym})")
    OWN = t("own computation", "calcule proprii")

    # ------------------------------------------------------------------ front matter
    D.parts.append("% END-FRONT-MATTER\n")
    D.frame(t("Learning objectives", "Obiectivele cursului"), it(
        (t("\\textbf{Merit order}", "\\textbf{Ordinea de merit}"),
         t("measure how much zero-cost solar and wind lower the price of the Romanian day-ahead market (PZU)",
           "măsurarea efectului producției solare și eoliene, cu cost marginal aproape zero, asupra prețului din piața pentru ziua următoare (PZU)"),
         t("on the real order book and with a regression on hourly data", "pe ofertele reale și cu o regresie pe date orare")),
        (t("\\textbf{Capture price and capture rate}", "\\textbf{Prețul capturat și rata de captare}"),
         t("the price a solar or wind MWh actually earns, compared with the average price",
           "prețul efectiv obținut de un MWh solar sau eolian, comparat cu prețul mediu"),
         t("cannibalisation: the more solar, the lower its own price", "canibalizarea: cu cît există mai mult solar, cu atît prețul obținut de el scade")),
        (t("\\textbf{Negative prices and the daily price shape}", "\\textbf{Prețurile negative și profilul zilnic al prețului}"),
         t("count negative prices in hour-equivalents; value switching a park off", "numărarea prețurilor negative în ore echivalente; valoarea opririi unui parc"),
         t("read the 15-minute daily profile", "interpretarea profilului zilnic pe intervale de 15 minute")),
        (t("\\textbf{Batteries}", "\\textbf{Bateriile}"),
         t("arbitrage revenue of 1-, 2- and 4-hour batteries from a linear programme (LP)",
           "venitul din arbitraj al bateriilor de 1, 2 și 4 ore, calculat cu un program liniar (LP)"),
         t("perfect foresight vs forecast rules, hourly vs 15-minute prices, Romania vs neighbours",
           "informație perfectă sau reguli de prognoză; prețuri orare sau pe 15 minute; România sau vecinii")),
        sep="3pt"))

    ab = sorted([(k, v) for k, v in ABBR.items() if v[0 if not ro else 1] is not None], key=lambda kv: kv[0].lower())

    def abcol(lst):
        return ("{\\scriptsize\\renewcommand{\\arraystretch}{1.0}\\begin{tabular}{@{}>{\\bfseries}l@{\\ \\ }"
                "p{0.76\\linewidth}@{}}" + "\n".join(f"{k} & {v[0] if not ro else v[1]}\\\\" for k, v in lst) + "\\end{tabular}}")

    D.parts.append("% BEGIN-ABBR\n")
    hh = (len(ab) + 1) // 2
    D.frame(t("Abbreviations", "Abrevieri"), "\\vspace{-1mm}\\begin{columns}[T,onlytextwidth]\n" + "".join(
        f"\\begin{{column}}{{0.49\\textwidth}}{abcol(ab[i * hh:(i + 1) * hh])}\\end{{column}}\n" for i in range(2)) + "\\end{columns}")
    D.parts.append("% END-ABBR\n")

    D.frame(t("Real data only: prices, generation, order books, installed capacity",
              "Lucrăm numai cu date reale: prețuri, producție, oferte și putere instalată"), table(
        "@{}p{0.30\\textwidth}p{0.15\\textwidth}p{0.50\\textwidth}@{}",
        [t("Series", "Seria"), t("Frequency", "Frecvența"), t("Source", "Sursa")],
        [[t("Day-ahead prices: Romania (RO), Bulgaria (BG), Hungary (HU), Germany--Luxembourg (DE-LU)",
            "Prețuri pentru ziua următoare: România (RO), Bulgaria (BG), Ungaria (HU), Germania--Luxemburg (DE-LU)"),
          t("hourly; 15-min from 1 Oct 2025", "orară; 15 minute din 1 oct.\\ 2025"),
          t("Romanian market operator (OPCOM), Independent Bulgarian Energy Exchange (IBEX), Hungarian Power Exchange (HUPX), "
            "European Power Exchange (EPEX SPOT); via energy-charts.info (Fraunhofer ISE)",
            "operatorul pieței din România (OPCOM), bursa independentă de energie din Bulgaria (IBEX), bursa de energie din Ungaria (HUPX), "
            "bursa europeană de energie (EPEX SPOT); prin energy-charts.info (Fraunhofer ISE)")],
         [t("Solar, wind, battery output, load", "Producția solară, eoliană, a bateriilor; consumul"),
          t("RO, HU 15-min; BG hourly", "RO, HU 15 minute; BG orară"),
          t("European Network of Transmission System Operators for Electricity (ENTSO-E); Transelectrica data for RO",
            "Rețeaua europeană a operatorilor de transport și de sistem (ENTSO-E); date Transelectrica pentru RO")],
         [t("PZU supply and demand curves", "Curbele de ofertă și de cerere PZU"), t("2 quarter-hours", "2 sferturi de oră"),
          t("OPCOM, Extensible Markup Language (XML) files", "OPCOM, fișiere Extensible Markup Language (XML)")],
         [t("Installed capacity", "Puterea instalată"), t("yearly", "anuală"), "ENTSO-E " + t("via energy-charts.info", "prin energy-charts.info")]],
        size="scriptsize", stretch="0.95") + "\n\\vspace{1mm}\n" + it(
        t(("\\textbf{Period}: 2019 -- @{cutoff.end|date}, the last complete month", "@{Y} = " + YTD + "; ``last 12 months'' = @{cutoff.ltm_start|ym} -- @{cutoff.ltm_end|ym}",
           "delivery days in Central European Time (CET)"),
          ("\\textbf{Perioada}: 2019 -- @{cutoff.end|date}, ultima lună completă", "@{Y} înseamnă " + YTD + "; „ultimele 12 luni” = @{cutoff.ltm_start|ym} -- @{cutoff.ltm_end|ym}",
           "zilele de livrare se definesc după ora Europei Centrale (CET)")),
        t(("\\textbf{Conventions}", "energy = mean MW $\\times$ duration; a 15-minute market time unit (MTU) counts 0.25 h"),
          ("\\textbf{Convenții}", "energia = puterea medie (MW) $\\times$ durata; un interval de tranzacționare (MTU) de 15 minute contează 0{,}25 h")),
        sep="1pt") + D.bottom(None, NB + " \\S1"), "footnotesize", cite="(data/SOURCES.md; data/download\\_L6.py)")

    # ------------------------------------------------------------------ 1 merit order
    D.section(t("Renewables and the merit order", "Sursele regenerabile și ordinea de merit"))
    D.subsection(t("The solar boom", "Creșterea producției solare"))
    D.chart(t("Installed solar in Romania grew @{cap.solar_ro_x|.1f} times from 2019 to @{cap.last_year}",
              "Puterea solară instalată în România a crescut de @{cap.solar_ro_x|.1f} ori între 2019 și @{cap.last_year}"), "solar_growth", [
        t(("\\textbf{Romanian solar output, Jan--Oct}: @{twh_lfl.2025.solar|.2f} TWh in @{YP}, @{twh_lfl.2026.solar|.2f} TWh in @{Y}",
           "@{twh.solar_share_load_2019|.1f}\\% of load in 2019, @{twh.solar_share_load_ytd|.1f}\\% in @{Y}; neighbours: Bulgaria @{cap.solar.BG.2025|.1f} GW, Hungary @{cap.solar.HU.2025|.1f} GW"),
          ("\\textbf{Producția solară a României, ianuarie--octombrie}: @{twh_lfl.2025.solar|.2f} TWh în @{YP} și @{twh_lfl.2026.solar|.2f} TWh în @{Y}",
           "@{twh.solar_share_load_2019|.1f}\\% din consum în 2019, @{twh.solar_share_load_ytd|.1f}\\% în @{Y}; vecinii: Bulgaria @{cap.solar.BG.2025|.1f} GW, Ungaria @{cap.solar.HU.2025|.1f} GW"))],
        height="0.62\\textheight", size="footnotesize",
        job=t("a new solar park sells in the same sunny hours as every park already built, here and next door.",
              "un parc solar nou vinde în aceleași ore însorite ca toate parcurile existente, din România și din țările vecine."),
        tryit=NB + " \\S1", cite=t("(ENTSO-E; metered output may omit rooftop panels)", "(ENTSO-E; producția măsurată poate omite panourile de pe acoperișuri)"))

    D.subsection(t("The merit-order effect", "Efectul ordinii de merit"))
    D.concept(t("Zero-cost supply shifts the supply curve right and lowers the clearing price",
                "Oferta cu cost zero deplasează curba ofertei spre dreapta și reduce prețul de închidere"),
              t("Solar and wind bid near zero, so dearer offers move right and the crossing with demand slides down.",
                "Solarul și eolianul ofertează aproape de zero; ofertele mai scumpe se mută spre dreapta, iar intersecția cu cererea coboară."),
              "\\[ S(p)+X\\cdot\\mathbf 1[p\\ge 0]=D(p)\\ \\Rightarrow\\ p^*(X) \\]\\vspace{-2mm}"
              "\\[ \\frac{\\mathrm dp^*}{\\mathrm dX}=-\\frac{1}{S'(p^*)-D'(p^*)} \\]" +
              "\\where{" + t("$S(p)$ = MW offered at prices $\\le p$; $D(p)$ = MW bid at prices $\\ge p$; $X$ = extra MW offered at 0 EUR/MWh; "
                             "$S'$, $D'$ = slopes of the curves (MW per EUR/MWh).",
                             "$S(p)$ = MW oferiți la prețuri $\\le p$; $D(p)$ = MW ceruți la prețuri $\\ge p$; $X$ = MW în plus, oferiți la 0 EUR/MWh; "
                             "$S'$, $D'$ = pantele curbelor (MW pentru 1 EUR/MWh).") + "}",
              it((t("\\textbf{Reading the formula}", "\\textbf{Cum se citește formula}"),
                  t("flat curves around the price: small effect", "curbe plate în jurul prețului: efect mic"),
                  t("steep curves: large effect", "curbe abrupte: efect mare")),
                 (t("\\textbf{OPCOM, @{merit.day|date}, 12:00--12:15}", "\\textbf{OPCOM, @{merit.day|date}, 12:00--12:15}"),
                  t("price @{merit.mid.price|.2f} EUR/MWh", "prețul: @{merit.mid.price|.2f} EUR/MWh"),
                  t("only @{merit.mid.depth_1_to_p|,.0f} MW offered between 1 EUR/MWh and that price", "doar @{merit.mid.depth_1_to_p|,.0f} MW oferiți între 1 EUR/MWh și acest preț")), sep="2pt"),
              t("the steeper the local curve, the more a new park moves its own price.",
                "cu cît curba locală este mai abruptă, cu atît un parc nou își modifică mai mult propriul preț."),
              tryit=NB + " \\S2", cite="(Sensfuß, Ragwitz \\& Genoese, 2008, ENPOL)", wl="0.50", wr="0.47")

    D.figframe(t("On the Romanian order book alone, @{merit.mid.x_below50} MW more at zero price pushes midday below 50 EUR/MWh",
                 "Ofertele din România: +@{merit.mid.x_below50} MW la preț zero coboară amiaza sub 50 EUR/MWh"),
               None, None, "merit_shift", [
                   t(("\\textbf{Midday}: +25 MW at zero price, @{merit.mid.price|.2f} $\\to$ @{merit.mid.sup.25|.2f} EUR/MWh",
                      "evening: @{merit.eve.net_imp|,.0f} MW of net imports deepen the curve; @{merit.eve.x_below50} MW are needed for the same fall",
                      "flows held fixed, so this is an upper bound for the coupled market"),
                     ("\\textbf{La amiază}: +25 MW la preț zero, @{merit.mid.price|.2f} $\\to$ @{merit.mid.sup.25|.2f} EUR/MWh",
                      "seara: importul net de @{merit.eve.net_imp|,.0f} MW adîncește curba; pentru aceeași scădere sînt necesari @{merit.eve.x_below50} MW",
                      "fluxurile rămîn fixe, deci rezultatul este o limită superioară pentru piața cuplată"))],
               job=t("for Transelectrica: interconnectors, not local plants, give the midday price its depth.",
                     "pentru Transelectrica: interconexiunile, nu centralele locale, dau profunzime prețului de la amiază."),
               tryit=NB + " \\S2", height="0.60\\textheight", size="footnotesize",
               cite=t("(OPCOM aggregated curves; " + OWN + ")", "(curbele agregate OPCOM; " + OWN + ")"))

    D.concept(t("In the coupled market, 1 GW more solar lowers the Romanian price by about @{reg.solar_babs|.0f} EUR/MWh",
                "În piața cuplată, 1 GW solar în plus reduce prețul din România cu aproximativ @{reg.solar_babs|.0f} EUR/MWh"),
              t("Within the same month and clock hour, sunnier and windier hours are cheaper; the regression measures by how much.",
                "La aceeași oră și în aceeași lună, orele cu mai mult soare și vînt sînt mai ieftine."),
              "\\[ P_t=\\underbrace{\\alpha_{m(t)}+\\gamma_{h(t)}+\\delta_{w(t)}}_{\\text{" + t("fixed effects", "efecte fixe") +
              "}}+\\beta_L L_t+\\beta_W W_t+\\beta_S S_t+\\varepsilon_t \\]" +
              "\\where{" + t("$P_t$ = hourly price (EUR/MWh), $L_t$, $W_t$, $S_t$ = load, wind, solar (GW); $\\alpha$, $\\gamma$, $\\delta$ = constants per month (fuel, carbon), "
                             "clock hour and weekday, estimated by ordinary least squares (OLS).",
                             "$P_t$ = prețul orar (EUR/MWh), $L_t$, $W_t$, $S_t$ = consumul, producția eoliană și cea solară (GW); $\\alpha$, $\\gamma$, $\\delta$ = constante "
                             "pentru lună (gaze, carbon), oră și ziua săptămînii, estimate prin metoda celor mai mici pătrate (OLS).") + "}",
              it((t("\\textbf{Estimates}, @{reg.n|,d} hours, 2023 -- @{reg.end|ym}, $R^2$ = @{reg.r2|.2f}", "\\textbf{Estimări}, @{reg.n|,d} " + de("reg.n") + "ore, 2023 -- @{reg.end|ym}, $R^2$ = @{reg.r2|.2f}"),
                  t("EUR/MWh per GW: solar @{reg.solar.b|.1f}, wind @{reg.wind.b|.1f}, load @{reg.load.b|+.1f}", "EUR/MWh pentru 1 GW: solar @{reg.solar.b|.1f}, eolian @{reg.wind.b|.1f}, consum @{reg.load.b|+.1f}"),
                  t("standard error (SE) of solar @{reg.solar.se|.1f}, heteroskedasticity- and autocorrelation-consistent (HAC)",
                    "eroarea standard (SE) pentru solar: @{reg.solar.se|.1f}, robustă la heteroscedasticitate și autocorelare (HAC)")),
                 (t("\\textbf{At midday in @{Y}}", "\\textbf{La amiază, în @{Y}}"),
                  t("@{reg.solar_mean_day_gw|.2f} GW of solar: @{reg.solar_effect_midday|.1f} EUR/MWh, an association, not a causal effect", "@{reg.solar_mean_day_gw|.2f} GW solar în medie: @{reg.solar_effect_midday|.1f} EUR/MWh; o asociere, nu un efect cauzal")), sep="2pt"),
              t("a supplier buying midday blocks should expect them cheaper on sunny days, by about this amount.",
                "un furnizor care cumpără blocuri de amiază le plătește mai puțin în zilele însorite, cu aproximativ această sumă."),
              tryit=NB + " \\S3", cite="(Cludius et al., 2014, ENEECO; Würzburg et al., 2013, ENEECO)", wl="0.49", wr="0.48")

    D.chart(t("Price rises with residual load; hours below 2 GW of residual load reached @{reg.share_resid_below2_2026|.1f}\\% in @{Y}",
              "Prețul crește cu consumul rezidual; orele sub 2 GW au ajuns la @{reg.share_resid_below2_2026|.1f}\\% în @{Y}"), "resid_price", [
        t(("\\textbf{Residual load} = load $-$ wind $-$ solar, the demand left for other plants and imports",
           "+1 GW raises the price by @{reg.resid.b|.1f} EUR/MWh (SE @{reg.resid.se|.1f}), same fixed effects",
           "hours below 2 GW: @{reg.share_resid_below2_2023|.1f}\\% in 2023, @{reg.share_resid_below2_2026|.1f}\\% in @{Y}"),
          ("\\textbf{Consumul rezidual} = consum $-$ eolian $-$ solar, adică cererea rămasă pentru celelalte centrale și pentru import",
           "+1 GW crește prețul cu @{reg.resid.b|.1f} EUR/MWh (SE @{reg.resid.se|.1f}), cu aceleași efecte fixe",
           "orele sub 2 GW: @{reg.share_resid_below2_2023|.1f}\\% în 2023, @{reg.share_resid_below2_2026|.1f}\\% în @{Y}"))],
        height="0.60\\textheight", size="footnotesize",
        job=t("a hydro producer saves water for high residual load, where each GW is worth most.",
              "un producător hidro păstrează apa pentru orele cu consum rezidual mare, cînd fiecare GW valorează cel mai mult."),
        tryit=NB + " \\S3", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    D.subsection(t("Renewables and the grid: redispatch", "Sursele regenerabile și rețeaua: redispecerizarea"))
    D.frame(t("Research from our group: machine learning forecasts German redispatch one day ahead",
              "Cercetarea grupului nostru: învățarea automată prognozează redispecerizarea din Germania cu o zi înainte"), it(
        t(("\\textbf{Why redispatch}: wind in the north, demand in the industrial south of Germany",
           "after the day-ahead market, transmission system operators order plants up or down to keep lines within limits"),
          ("\\textbf{De ce redispecerizare}: vîntul este în nordul Germaniei, consumul în sudul industrializat",
           "după piața pentru ziua următoare, operatorii de transport și de sistem cer centralelor să crească sau să reducă producția")),
        t(("\\textbf{What the work did}: forecast the hourly redispatch volume (MW), up and down, of the four German operators",
           "24 h ahead, with what is known on the afternoon of $d-1$: wind, solar, load, price spreads, scheduled exchanges",
           "data Oct 2021 -- Feb 2026; 11 monthly test windows, Mar 2025 -- Feb 2026"),
          ("\\textbf{Ce a făcut lucrarea}: a prognozat volumul orar al redispecerizării (MW), în sus și în jos, la cei patru operatori germani",
           "cu 24 h înainte, cu ce se știe în după-amiaza zilei $d-1$: vînt, solar, consum, diferențe de preț, schimburi programate",
           "date oct.\\ 2021 -- feb.\\ 2026; 11 ferestre lunare de test, mar.\\ 2025 -- feb.\\ 2026")),
        t(("\\textbf{What it found}: deep neural networks are most often among the best models",
           "the best of them is in the model confidence set (mean absolute error) for 6 of the 8 series",
           "covariates help only when aligned in time: significantly better forecasts in 40--60\\% of the dense series"),
          ("\\textbf{Ce a găsit}: rețelele neuronale adînci sînt cel mai des printre cele mai bune modele",
           "cea mai bună dintre ele intră în mulțimea de încredere a modelelor (eroarea absolută medie) pentru 6 din cele 8 serii",
           "variabilele explicative ajută doar aliniate în timp: prognoze semnificativ mai bune în 40--60\\% dintre seriile dense")),
        sep="2pt") + D.bottom(t("for Transelectrica: forecast where wind and solar will meet the limits of the grid, a day ahead.",
                                "pentru Transelectrica: prognozați cu o zi înainte unde vor atinge eolianul și solarul limitele rețelei.")),
        "footnotesize", cite=t("(Basangova, Bolovăneanu, Conda, Erlwein-Sayer, Melzer, Pele, Petukhina \\& Phan, 2026, talk at AIDA 2026 (AI and Digital Assets in Energy and Finance), Bucharest, 3 June 2026: "
                               "\\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/bolovaneanu_redispatch_forecasting.pdf}{slides})",
                               "(Basangova, Bolovăneanu, Conda, Erlwein-Sayer, Melzer, Pele, Petukhina \\& Phan, 2026, prezentare la AIDA 2026 (AI and Digital Assets in Energy and Finance), București, 3 iunie 2026: "
                               "\\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/bolovaneanu_redispatch_forecasting.pdf}{diapozitive})"))

    # ------------------------------------------------------------------ 2 capture prices
    D.section(t("Capture prices and cannibalisation", "Prețul capturat și canibalizarea"))
    D.subsection(t("Definitions", "Definiții"))
    D.concept(t("The capture price is the average price weighted by the plant's own output",
                "Prețul capturat este prețul mediu ponderat cu producția centralei"),
              t("A solar park is paid the price of the intervals in which it produces, not the average of all intervals.",
                "Un parc solar încasează prețul intervalelor în care produce, nu media tuturor intervalelor."),
              "\\[ \\mathrm{CP}=\\frac{\\sum_t P_t G_t\\Delta_t}{\\sum_t G_t\\Delta_t},\\qquad B=\\frac{\\sum_t P_t\\Delta_t}{\\sum_t\\Delta_t} \\]"
              "\\[ \\mathrm{CR}=\\frac{\\mathrm{CP}}{B}=1+\\frac{\\mathrm{Cov}_\\Delta(P,G)}{\\bar P\\,\\bar G} \\]" +
              "\\where{" + t("capture price (CP), baseload price $B$, capture rate (CR); $P_t$ = price, $G_t$ = output (MW), $\\Delta_t$ = 1 h or 0.25 h, "
                             "$\\mathrm{Cov}_\\Delta$ = duration-weighted covariance (Appendix A).",
                             "prețul capturat (CP), prețul de bază $B$, rata de captare (CR); $P_t$ = prețul, $G_t$ = producția (MW), $\\Delta_t$ = 1 h sau 0{,}25 h, "
                             "$\\mathrm{Cov}_\\Delta$ = covarianța ponderată cu durata (Anexa A).") + "}",
              it((t("\\textbf{Romanian solar, " + YTD + "}", "\\textbf{Solarul din România, " + YTD + "}"),
                  t("CP @{capt.RO.solar.2026.cp|.1f}, $B$ @{capt.RO.solar.2026.base|.1f} EUR/MWh; CR @{capt.RO.solar.2026.crp|.1f}\\%",
                    "CP @{capt.RO.solar.2026.cp|.1f}, $B$ @{capt.RO.solar.2026.base|.1f} EUR/MWh; CR @{capt.RO.solar.2026.crp|.1f}\\%"),
                  t("correlation of price and output @{capt.cov.corr|.2f}: this pulls CR below 1", "corelația dintre preț și producție: @{capt.cov.corr|.2f}; de aceea CR este sub 1")),
                 (t("\\textbf{Romanian wind, same period}", "\\textbf{Eolianul din România, aceeași perioadă}"),
                  t("CR @{capt.RO.wind.2026.crp|.1f}\\%: wind also blows at night and in winter", "CR @{capt.RO.wind.2026.crp|.1f}\\%; vîntul bate și noaptea, și iarna")), sep="2pt"),
              t("price a solar power purchase agreement (PPA) on the capture price, not on the baseload price.",
                "prețul unui contract pe termen lung pentru energie solară (PPA) pornește de la prețul capturat, nu de la prețul de bază."),
              tryit=NB + " \\S4", cite="(Hirth, 2013, ENEECO; Hirth, Ueckerdt \\& Edenhofer, 2016, Energy J.)", wl="0.50", wr="0.47")

    D.subsection(t("Romania, year by year", "România, an de an"))
    D.chart(t("Solar's capture rate in Romania fell from @{capt.RO.solar.2019.crp|.0f}\\% in 2019 to @{capt.RO.solar.2025.crp|.0f}\\% in 2025",
              "Rata de captare a solarului în România a scăzut de la @{capt.RO.solar.2019.crp|.0f}\\% în 2019 la @{capt.RO.solar.2025.crp|.0f}\\% în 2025"), "capture_rates", [
        t(("\\textbf{Solar}: the fall starts in 2023, with the growth of output", "@{Y}: @{capt.RO.solar.2026.crp|.1f}\\%, while output rose @{twh_lfl.solar_chg|.0f}\\% on the same months of @{YP}",
           "wind: between @{capt.RO.wind_min|.0f}\\% and @{capt.RO.wind_max|.0f}\\%, no trend, because wind output did not grow"),
          ("\\textbf{Solarul}: scăderea începe în 2023, odată cu creșterea producției", "@{Y}: @{capt.RO.solar.2026.crp|.1f}\\%, deși producția a crescut cu @{twh_lfl.solar_chg|.0f}\\% față de aceleași luni din @{YP}",
           "eolianul: între @{capt.RO.wind_min|.0f}\\% și @{capt.RO.wind_max|.0f}\\%, fără tendință, deoarece producția eoliană nu a crescut"))],
        height="0.60\\textheight", size="footnotesize",
        job=t("a bank lending to a solar project should multiply the baseload price by the capture rate.",
              "o bancă ce finanțează un proiect solar trebuie să înmulțească prețul de bază cu rata de captare."),
        tryit=NB + " \\S4", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    cr = N["capt"]["RO"]
    rows = []
    for y in [str(v) for v in range(2019, Y + 1)]:
        s_, w_ = cr["solar"][y], cr["wind"][y]
        rows.append([(y if int(y) < Y else y + "*"), fmt(s_["base"], ".1f", lang), fmt(s_["cp"], ".1f", lang),
                     heat(s_["crp"], 55, 105, False, fmt(s_["crp"], ".1f", lang)), fmt(s_["disc"], "+.1f", lang),
                     fmt(w_["cp"], ".1f", lang), heat(w_["crp"], 55, 105, False, fmt(w_["crp"], ".1f", lang)),
                     fmt(s_["twh"], ".2f", lang), fmt(w_["twh"], ".2f", lang)])
    D.frame(t("In 2025 a Romanian solar MWh earned @{capt.RO.solar.2025.disc|.1f} EUR less than the baseload price",
              "În 2025, un MWh solar din România a obținut cu @{capt.RO.solar.2025.disc|.1f} EUR mai puțin decît prețul de bază"),
            "\\begin{center}" + table("@{}lrrrrrrrr@{}", [t("Year", "Anul"), "$B$", t("Solar CP", "CP solar"),
                                                           t("Solar CR, \\%", "CR solar, \\%"), "$B-\\mathrm{CP}$",
                                                           t("Wind CP", "CP eolian"), t("Wind CR, \\%", "CR eolian, \\%"),
                                                           t("Solar TWh", "TWh solar"), t("Wind TWh", "TWh eolian")], rows,
                                      size="footnotesize", stretch="1.05") + "\\end{center}\\vspace{-2mm}" + it(
                t(("\\textbf{Reading the table}: $B$, CP in EUR/MWh; green = CR close to 100\\%, red = far below", "* @{Y} = " + YTD + "; 2022 = energy crisis, all prices high"),
                  ("\\textbf{Cum se citește tabelul}: $B$ și CP în EUR/MWh; verde = CR aproape de 100\\%, roșu = mult sub", "* @{Y} = " + YTD + "; 2022 = criza energetică, toate prețurile au fost mari")),
                sep="1pt") +
            D.bottom(t("the gap $B-\\mathrm{CP}$ is a cost borne by the solar developer; it grew every year since 2022.",
                       "diferența $B-\\mathrm{CP}$ este un cost suportat de dezvoltatorul solar; a crescut în fiecare an din 2022."), NB + " \\S4"),
            "footnotesize", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    D.subsection(t("Cannibalisation", "Canibalizarea"))
    D.figframe(t("When solar's share of monthly load rises by one point, the solar capture rate falls by about @{cannib.bneg|.1f} points",
                 "Cînd ponderea solarului în consumul lunii crește cu un punct procentual, rata de captare solară scade cu circa @{cannib.bneg|.1f} puncte"),
               None, None, "cannibal", [
                   t(("\\textbf{Regression} $\\mathrm{CR}_m=a+b\\,s_m+u_m$, $s_m$ = solar output as \\% of load in month $m$",
                      "Romania: $\\hat b$ = @{cannib.b|.2f} (SE @{cannib.se|.2f}), $R^2$ = @{cannib.r2|.2f}, @{cannib.n} months",
                      "Hungary @{cannib.HU.b|.2f}, Bulgaria @{cannib.BG.b|.2f}: Romanian prices also fall with the neighbours' solar"),
                     ("\\textbf{Regresia} $\\mathrm{CR}_m=a+b\\,s_m+u_m$, unde $s_m$ = producția solară, în \\% din consumul lunii $m$",
                      "România: $\\hat b$ = @{cannib.b|.2f} (SE @{cannib.se|.2f}), $R^2$ = @{cannib.r2|.2f}, @{cannib.n} " + de("cannib.n") + "luni",
                      "Ungaria @{cannib.HU.b|.2f}, Bulgaria @{cannib.BG.b|.2f}; prețul din România scade și cu producția solară a vecinilor"))],
               job=t("forecast regional solar, not only Romanian solar, to forecast a park's revenue.",
                     "pentru venitul unui parc, prognozați producția solară regională, nu doar pe cea a României."),
               tryit=NB + " \\S4", height="0.56\\textheight", size="footnotesize",
               cite="(López Prol, Steininger \\& Zilberman, 2020, ENEECO)")

    D.chart(t("Regional cannibalisation: Romanian, Bulgarian and Hungarian capture rates fell in step",
              "Rata de captare solară a scăzut simultan în România, Bulgaria și Ungaria"), "capture_region", [
        t(("\\textbf{2025}: Romania @{capt.RO.solar.2025.crp|.1f}\\%, Bulgaria @{capt.BG.solar.2025.crp|.1f}\\%, Hungary @{capt.HU.solar.2025.crp|.1f}\\%",
           "@{Y}: Bulgaria rises to @{capt.BG.solar.2026.crp|.1f}\\% as its battery fleet grows, an association, not a proof"),
          ("\\textbf{2025}: România @{capt.RO.solar.2025.crp|.1f}\\%, Bulgaria @{capt.BG.solar.2025.crp|.1f}\\%, Ungaria @{capt.HU.solar.2025.crp|.1f}\\%",
           "@{Y}: Bulgaria urcă la @{capt.BG.solar.2026.crp|.1f}\\%, odată cu extinderea bateriilor; este o asociere, nu o dovadă"))],
        height="0.62\\textheight", size="footnotesize",
        job=t("batteries charging at midday raise the price solar sells at: solar gains from other people's batteries.",
              "un parc solar cîștigă și din bateriile altora, care se încarcă la amiază și îi cresc prețul."),
        tryit=NB + " \\S4", cite=t("(" + OWN + "; Bulgarian output is hourly)", "(" + OWN + "; producția din Bulgaria este orară)"))

    D.chart(t("In 2025, @{cheap.2025.e_in_cheap10|.1f}\\% of Romanian solar output was sold in the cheapest 10\\% of hours",
              "În 2025, @{cheap.2025.e_in_cheap10|.1f}\\% din energia solară s-a vîndut în cele mai ieftine 10\\% dintre ore"), "cheap_hours", [
        t(("\\textbf{Reading}: hours ranked from the cheapest; the curve = share of the year's solar energy produced up to that rank",
           "2019: @{cheap.2019.e_in_cheap10|.1f}\\%; 2025: @{cheap.2025.e_in_cheap10|.1f}\\%; @{Y}: @{cheap.2026.e_in_cheap10|.1f}\\%; at zero or negative prices: @{cheap.2025.e_le0|.1f}\\% of 2025 output"),
          ("\\textbf{Citire}: orele sînt ordonate de la cea mai ieftină; curba = partea din energia solară a anului produsă pînă la acel rang",
           "2019: @{cheap.2019.e_in_cheap10|.1f}\\%; 2025: @{cheap.2025.e_in_cheap10|.1f}\\%; @{Y}: @{cheap.2026.e_in_cheap10|.1f}\\%; la prețuri nule sau negative: @{cheap.2025.e_le0|.1f}\\% din producția anului 2025"))],
        height="0.60\\textheight", size="footnotesize",
        job=t("as announced in Lecture 1: a solar park without storage sells much of its output in the cheapest hours of the year.",
              "cum am anunțat în cursul 1: un parc solar fără stocare vinde mult în cele mai ieftine ore ale anului."),
        tryit=NB + " \\S4", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    # ------------------------------------------------------------------ 3 negative prices
    D.section(t("Negative prices", "Prețurile negative"))
    D.concept(t("A producer bids below zero when stopping costs more than paying to produce",
                "Un producător ofertează sub zero cînd oprirea îl costă mai mult decît plata pentru a produce"),
              t("The bid is the cost of one more MWh minus what the plant earns or saves only by running.",
                "Oferta este costul unui MWh în plus, minus ce primește sau economisește centrala doar dacă funcționează."),
              "\\[ b_i=c_i-s_i-k_i,\\qquad h^{-}=\\textstyle\\sum_t \\Delta_t\\,\\mathbf 1[P_t<0] \\]" +
              "\\where{" + t("$b_i$ = offer of plant $i$ (EUR/MWh), $c_i$ = marginal cost; $s_i$ = support paid per MWh produced, $k_i$ = restart cost per MWh of a stop; "
                             "$h^-$ = negative hours in hour-equivalents.",
                             "$b_i$ = oferta centralei $i$ (EUR/MWh), $c_i$ = costul marginal; $s_i$ = sprijinul plătit pe MWh produs, $k_i$ = costul repornirii, pe MWh al unei opriri; "
                             "$h^-$ = orele cu preț negativ, în ore echivalente.") + "}",
              it((t("\\textbf{Who bids below zero}", "\\textbf{Cine ofertează sub zero}"),
                  t("output paid per MWh by a support scheme or contract", "producția plătită pe MWh printr-o schemă de sprijin sau un contract"),
                  t("nuclear and run-of-river hydro, which cannot stop cheaply", "centralele nucleare și hidro pe firul apei, care nu se pot opri ieftin")),
                 (t("\\textbf{Romania, 2025}", "\\textbf{România, 2025}"),
                  t("@{neg.hours.RO.2025|.0f} negative hours; mean negative price @{neg.depth.RO.2025|.1f} EUR/MWh", "@{neg.hours.RO.2025|.0f} " + de("neg.hours.RO.2025") + "ore negative; prețul negativ mediu: @{neg.depth.RO.2025|.1f} EUR/MWh"),
                  t("lowest @{Y} price: @{neg.ro_min|.2f} EUR/MWh", "cel mai mic preț din @{Y}: @{neg.ro_min|.2f} EUR/MWh")), sep="2pt"),
              t("a merchant solar park has $b_i\\approx 0$: it should stop as soon as the price turns negative.",
                "un parc solar fără sprijin are $b_i\\approx 0$, deci trebuie să se oprească imediat ce prețul devine negativ."),
              tryit=NB + " \\S5", cite="(Fanone, Gamba \\& Prokopczuk, 2013, ENEECO)", wl="0.44", wr="0.53")

    D.chart(t("Romania had @{neg.hours.RO.2025|.0f} negative hours in 2025, Germany @{neg.hours.DE_LU.2025|.0f}",
              "România a avut @{neg.hours.RO.2025|.0f} " + de("neg.hours.RO.2025") + "ore cu preț negativ în 2025, Germania @{neg.hours.DE_LU.2025|.0f}"), "neg_hours", [
        t(("\\textbf{Jan--Oct, @{YP} vs @{Y}}: Romania @{neg.lfl.RO.2025|.0f} $\\to$ @{neg.lfl.RO.2026|.2f} h, Hungary @{neg.lfl.HU.2025|.0f} $\\to$ @{neg.lfl.HU.2026|.1f} h",
           "fewer despite more solar; possible reasons: a higher price level, more batteries charging at midday"),
          ("\\textbf{Ianuarie--octombrie, @{YP} față de @{Y}}: România @{neg.lfl.RO.2025|.0f} $\\to$ @{neg.lfl.RO.2026|.2f} h, Ungaria @{neg.lfl.HU.2025|.0f} $\\to$ @{neg.lfl.HU.2026|.1f} h",
           "mai puține, deși solarul a crescut; explicații posibile: prețuri mai mari în general, mai multe baterii care se încarcă la amiază"))],
        height="0.62\\textheight", size="footnotesize",
        job=t("a supplier with flexible industrial clients can be paid to consume in these hours.",
              "un furnizor cu clienți industriali flexibili poate fi plătit pentru a consuma în aceste ore."),
        tryit=NB + " \\S5", cite=t("(" + OWN + "; counting rule of Lecture 1)", "(" + OWN + "; regula de numărare din cursul 1)"))

    D.concept(t("Revenue losses: low positive midday prices cost more than negative prices",
                "Pierderile de venit: prețurile mici, dar pozitive, de la amiază costă mai mult decît prețurile negative"),
              t("A merchant park gains $|P_t|$ for each MWh it does not produce at a negative price; such MWh are few.",
                "Un parc fără sprijin cîștigă $|P_t|$ pentru fiecare MWh neprodus la preț negativ; acești MWh sînt puțini."),
              "\\[ g=\\frac{\\sum_t \\max(0,-P_t)\\,G_t\\Delta_t}{\\sum_t G_t\\Delta_t}\\quad\\text{" + t("vs", "față de") + "}\\quad B-\\mathrm{CP} \\]" +
              "\\where{" + t("$G_t$ = solar output (MW); $g$ = gain per MWh of yearly output if the park stops in every negative interval; $B-\\mathrm{CP}$ = profile discount.",
                             "$G_t$ = producția solară (MW); $g$ = cîștigul pe MWh de producție anuală, dacă parcul se oprește în toate intervalele negative; "
                             "$B-\\mathrm{CP}$ = reducerea datorată profilului.") + "}",
              it((t("\\textbf{Romanian solar, 2025}", "\\textbf{Solarul din România, 2025}"),
                  t("@{curt.2025.e_neg_pct|.1f}\\% of output at negative prices, costing @{curt.2025.cost_neg_meur|.2f} million EUR", "@{curt.2025.e_neg_pct|.1f}\\% din producție la prețuri negative, cu un cost de @{curt.2025.cost_neg_meur|.2f} milioane EUR"),
                  t("$g$ = @{curt.2025.gain_mwh_all|.2f} against $B-\\mathrm{CP}$ = @{capt.RO.solar.2025.disc|.1f} EUR/MWh", "$g$ = @{curt.2025.gain_mwh_all|.2f}, față de $B-\\mathrm{CP}$ = @{capt.RO.solar.2025.disc|.1f} EUR/MWh")),
                 (t("\\textbf{@{Y}}", "\\textbf{@{Y}}"),
                  t("@{curt.2026.e_neg_pct|.1f}\\% of output; $g$ = @{curt.2026.gain_mwh_all|.2f} EUR/MWh", "@{curt.2026.e_neg_pct|.1f}\\% din producție; $g$ = @{curt.2026.gain_mwh_all|.2f} EUR/MWh")), sep="2pt"),
              t("install remote switch-off because it is cheap, but value a park on its capture price.",
                "instalați oprirea la distanță, pentru că este ieftină, dar evaluați parcul după prețul capturat."),
              tryit=NB + " \\S5", cite=t("(" + OWN + ")", "(" + OWN + ")"), wl="0.50", wr="0.47")

    D.frame(t("Quarter-hours reveal @{neg.q15.n_hidden} negative prices hidden inside hours with a non-negative average",
              "Sferturile de oră arată @{neg.q15.n_hidden} prețuri negative ascunse în ore cu medie nenegativă"), it(
        t(("\\textbf{Since the 15-minute MTU of the Single Day-Ahead Coupling (SDAC)}, 1 Oct 2025",
           "@{neg.q15.n_negq} negative quarter-hours in Romania = @{neg.q15.h_negq|.2f} hour-equivalents",
           "@{neg.q15.n_hidden} of them (@{neg.q15.hidden_pct|.1f}\\%) fall in hours whose average is zero or positive"),
          ("\\textbf{De la 1 octombrie 2025}, cînd cuplarea unică a piețelor pentru ziua următoare (SDAC) a trecut la MTU de 15 minute",
           "@{neg.q15.n_negq} " + de("neg.q15.n_negq") + "sferturi de oră negative în România = @{neg.q15.h_negq|.2f} ore echivalente",
           "@{neg.q15.n_hidden} " + de("neg.q15.n_hidden") + "dintre ele (@{neg.q15.hidden_pct|.1f}\\%) sînt în ore cu media zero sau pozitivă")),
        t(("\\textbf{Why it matters}", "hourly averages show only @{neg.q15.n_neg_hours_avg} negative hours",
           "a battery or flexible load acting per quarter-hour can use them; a park metered per quarter-hour pays them"),
          ("\\textbf{De ce contează}", "mediile orare arată doar @{neg.q15.n_neg_hours_avg} " + de("neg.q15.n_neg_hours_avg") + "ore negative",
           "o baterie sau un consumator flexibil care acționează pe sfert de oră le poate valorifica; un parc măsurat pe sfert de oră le plătește")),
        t(("\\textbf{Counting rule}", "$h^-=\\sum_t\\Delta_t\\mathbf 1[P_t<0]$, $\\Delta_t$ = 0.25 h: never count a quarter-hour as an hour"),
          ("\\textbf{Regula de numărare}", "$h^-=\\sum_t\\Delta_t\\mathbf 1[P_t<0]$, $\\Delta_t$ = 0{,}25 h; un sfert de oră nu se numără niciodată ca o oră")),
        sep="4pt") + D.bottom(t("set switch-off and battery logic on the 15-minute grid, as the market now is.",
                                "programați oprirea centralelor și bateriile pe intervale de 15 minute, ca piața."), NB + " \\S5"),
        "footnotesize", cite="(NEMO Committee, 2025; " + OWN + ")")

    # ------------------------------------------------------------------ 4 intraday shape and spreads
    D.section(t("Intraday shape and price spreads", "Profilul zilnic și diferențele de preț"))
    D.chart(t("Spring quarter-hours: @{shape.spring.min|.1f} EUR/MWh at midday, @{shape.spring.max|.1f} in the evening",
              "Primăvara, prețul mediu: @{shape.spring.min|.1f} EUR/MWh la amiază, @{shape.spring.max|.1f} seara"), "shape15", [
        t(("\\textbf{The solar valley}: spring minimum at @{shape.spring.min_t}, maximum at @{shape.spring.max_t} CET",
           "maximum minus minimum: spring @{shape.spring.range|.0f}, summer @{shape.summer.range|.0f}, winter only @{shape.winter.range|.0f} EUR/MWh"),
          ("\\textbf{„Valea” solară}: primăvara, minimul este la @{shape.spring.min_t}, iar maximul la @{shape.spring.max_t} CET",
           "maximul minus minimul: primăvara @{shape.spring.range|.0f}, vara @{shape.summer.range|.0f}, iarna doar @{shape.winter.range|.0f} EUR/MWh"))],
        height="0.62\\textheight", size="footnotesize",
        job=t("a battery charges in the valley and discharges on the evening ramp: the gap is its gross margin.",
              "o baterie se încarcă în „vale” și se descarcă seara: diferența este marja ei brută."),
        tryit=NB + " \\S6", cite=t("(" + OWN + ", " + LTM + ")", "(" + OWN + ", " + LTM + ")"))

    D.concept(t("A battery earns the spread between dear and cheap hours, minus its losses",
                "O baterie cîștigă diferența dintre orele scumpe și cele ieftine, mai puțin pierderile"),
              t("Buy a MWh when it is cheap; sell what survives the round trip when it is dear.",
                "Bateria cumpără un MWh cînd este ieftin și vinde, cînd este scump, ce rămîne după încărcare și descărcare."),
              "\\[ S^{(k)}_d=\\bar P^{\\,\\mathrm{top}\\,k}_d-\\bar P^{\\,\\mathrm{bot}\\,k}_d \\]"
              "\\[ \\pi_d\\approx k\\,\\big(\\eta\\,\\bar P^{\\,\\mathrm{top}\\,k}_d-\\bar P^{\\,\\mathrm{bot}\\,k}_d\\big) \\]" +
              "\\where{" + t("$\\bar P^{\\,\\mathrm{top}\\,k}_d$, $\\bar P^{\\,\\mathrm{bot}\\,k}_d$ = mean price of the $k$ dearest and cheapest hours of day $d$, $k$ = hours of storage; "
                             "$\\eta$ = round-trip efficiency (85\\%), $\\pi_d$ = gross margin of one cycle, 1 MW (EUR).",
                             "$\\bar P^{\\,\\mathrm{top}\\,k}_d$, $\\bar P^{\\,\\mathrm{bot}\\,k}_d$ = prețul mediu al celor mai scumpe, respectiv al celor mai ieftine $k$ ore din ziua $d$; "
                             "$k$ = orele de stocare; $\\eta$ = randamentul ciclului complet (85\\%), $\\pi_d$ = marja brută a unui ciclu, 1 MW (EUR).") + "}",
              it((t("\\textbf{Romania, $k=2$, mean daily spread}", "\\textbf{România, $k=2$, diferența zilnică medie}"),
                  t("@{spread.RO.2019|.0f} EUR/MWh in 2019, @{spread.RO.2025|.0f} in 2025, @{spread.RO.2026|.0f} in @{Y}",
                    "@{spread.RO.2019|.0f} EUR/MWh în 2019, @{spread.RO.2025|.0f} în 2025, @{spread.RO.2026|.0f} în @{Y}")),
                 (t("\\textbf{Losses set a threshold}", "\\textbf{Pierderile impun un prag}"),
                  t("buying at 50 EUR/MWh, it must sell above $50/0.85\\approx59$ EUR/MWh", "dacă bateria cumpără la 50 EUR/MWh, trebuie să vîndă peste $50/0{,}85\\approx59$ EUR/MWh")), sep="2pt"),
              t("a battery developer reads the business case from the daily spread, before any model.",
                "un dezvoltator de baterii citește cazul de afaceri din diferența zilnică de preț, înaintea oricărui model."),
              tryit=NB + " \\S6", cite="(Sioshansi et al., 2009, ENEECO)", wl="0.50", wr="0.47")

    D.chart(t("The daily spread is about four times its 2019 level and similar in Romania, Bulgaria and Hungary",
              "Diferența zilnică de preț este de circa patru ori mai mare decît în 2019 și asemănătoare în România, Bulgaria și Ungaria"), "spreads", [
        t(("\\textbf{Dearest 2 minus cheapest 2 hours, @{Y}}: Romania @{spread.RO.2026|.0f}, Bulgaria @{spread.BG.2026|.0f}, Hungary @{spread.HU.2026|.0f}, Germany @{spread.DE_LU.2026|.0f} EUR/MWh",
           "coupled markets: every battery in the region competes for the same spread"),
          ("\\textbf{Cele mai scumpe 2 ore minus cele mai ieftine 2 ore, @{Y}}: România @{spread.RO.2026|.0f}, Bulgaria @{spread.BG.2026|.0f}, Ungaria @{spread.HU.2026|.0f}, Germania @{spread.DE_LU.2026|.0f} EUR/MWh",
           "piețele sînt cuplate, deci toate bateriile din regiune concurează pentru aceeași diferență"))],
        height="0.62\\textheight", size="footnotesize",
        job=t("treat the spread as a regional resource, shared with every new battery next door.",
              "tratați diferența de preț ca pe o resursă regională, împărțită cu fiecare baterie nouă din țările vecine."),
        tryit=NB + " \\S6", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    # ------------------------------------------------------------------ 5 batteries
    D.section(t("The economics of a battery", "Economia unei baterii"))
    D.subsection(t("The optimal schedule", "Programul optim"))
    D.concept(t("The best daily schedule of a battery solves a small linear programme",
                "Programul zilnic optim al unei baterii este soluția unui program liniar mic"),
              t("Choose when to charge and discharge to maximise revenue, within the battery's physical limits.",
                "Se aleg orele de încărcare și de descărcare care maximizează venitul, în limitele fizice ale bateriei."),
              "\\[ \\max_{c,\\,x}\\ \\textstyle\\sum_t P_t\\,(x_t-c_t)\\,\\Delta_t \\]\\vspace{-3mm}"
              "\\[ e_t=e_{t-1}+\\big(\\sqrt\\eta\\,c_t-x_t/\\sqrt\\eta\\big)\\Delta_t \\]\\vspace{-3mm}"
              "\\[ 0\\le e_t\\le E,\\ e_0=e_T=0,\\ 0\\le c_t,x_t\\le 1,\\ \\textstyle\\sum_t x_t\\Delta_t\\le\\sqrt\\eta E \\]" +
              "\\where{" + t("$c_t$, $x_t$ = charging, discharging power (MW); $e_t$ = stored energy (MWh); $E$ = 1, 2 or 4 MWh; $\\eta$ = 0.85; "
                             "last constraint: at most one cycle a day (Appendix B).",
                             "$c_t$, $x_t$ = puterea de încărcare, respectiv de descărcare (MW); $e_t$ = energia stocată (MWh); $E$ = 1, 2 sau 4 MWh; $\\eta$ = 0{,}85; "
                             "ultima restricție: cel mult un ciclu pe zi (Anexa B).") + "}",
              it((t("\\textbf{Assumptions}", "\\textbf{Ipoteze}"),
                  t("85\\% round trip, one cycle a day: National Renewable Energy Laboratory (NREL) reference", "randament 85\\%, un ciclu pe zi: valorile de referință ale Laboratorului Național pentru Energie Regenerabilă (NREL)"),
                  t("no capacity fade, fees or balancing revenue", "nu includem pierderea de capacitate, tarifele și veniturile din echilibrare")),
                 (t("\\textbf{Two information sets}", "\\textbf{Două ipoteze despre informație}"),
                  t("perfect foresight: prices known, an upper bound", "informație perfectă: prețurile sînt cunoscute; o limită superioară"),
                  t("forecast rule: optimise on a forecast, get paid real prices", "regulă de prognoză: optimizare pe prognoză, plată la prețurile reale")), sep="2pt"),
              t("this programme, with your own prices and limits, is the core of every battery dispatch tool.",
                "acest program, cu prețurile și limitele dumneavoastră, stă la baza oricărui instrument de programare a bateriilor."),
              tryit=NB + " \\S7", cite="(Cole \\& Karmakar, 2023, NREL)", wl="0.53", wr="0.44")

    D.chart(t("With perfect foresight, a 2-hour battery earned @{bat.ltm.2.pf|.1f} thousand EUR per MW in the last 12 months",
              "Cu informație perfectă, o baterie de 2 ore a cîștigat @{bat.ltm.2.pf|.1f} mii EUR pe MW în ultimele 12 luni"), "bat_years", [
        t(("\\textbf{2 hours, thousand EUR per MW-year}: @{bat.pf.2.2019|.1f} (2019), @{bat.pf.2.2022|.1f} (2022), @{bat.pf.2.2025|.1f} (2025)",
           "4 hours earn @{bat.x_4v2|.2f} times what 2 hours earn: the third and fourth hours trade a smaller spread"),
          ("\\textbf{2 ore, mii EUR pe MW și an}: @{bat.pf.2.2019|.1f} (2019), @{bat.pf.2.2022|.1f} (2022), @{bat.pf.2.2025|.1f} (2025)",
           "4 ore cîștigă de @{bat.x_4v2|.2f} ori cît 2 ore; orele a treia și a patra valorifică o diferență mai mică"))],
        height="0.62\\textheight", size="footnotesize",
        job=t("size the battery on the revenue of each extra MWh of storage, not on total revenue.",
              "dimensionați bateria după venitul adus de fiecare MWh suplimentar de stocare, nu după venitul total."),
        tryit=NB + " \\S7", cite=t("(" + OWN + "; day-ahead prices only)", "(" + OWN + "; doar prețurile pentru ziua următoare)"))

    D.chart(t("A simple 7-day rule earns @{bat.ltm.2.wk_pct|.0f}\\% of the 2-hour perfect-foresight revenue",
              "O regulă simplă obține @{bat.ltm.2.wk_pct|.0f}\\% din venitul cu informație perfectă (2 ore)"), "bat_rules", [
        t(("\\textbf{Rules known at 12:00 CET on $d-1$}: mean profile of the last 7 days, @{bat.ltm.1.wk_pct|.0f}\\%, @{bat.ltm.2.wk_pct|.0f}\\%, @{bat.ltm.4.wk_pct|.0f}\\% (1, 2, 4 h)",
           "yesterday's prices: @{bat.ltm.1.yday_pct|.0f}\\%, @{bat.ltm.2.yday_pct|.0f}\\%, @{bat.ltm.4.yday_pct|.0f}\\%; longer batteries forgive timing errors"),
          ("\\textbf{Reguli cunoscute la 12:00 CET în ziua $d-1$}: profilul mediu al ultimelor 7 zile, @{bat.ltm.1.wk_pct|.0f}\\%, @{bat.ltm.2.wk_pct|.0f}\\%, @{bat.ltm.4.wk_pct|.0f}\\% (1, 2, 4 ore)",
           "prețurile de ieri: @{bat.ltm.1.yday_pct|.0f}\\%, @{bat.ltm.2.yday_pct|.0f}\\%, @{bat.ltm.4.yday_pct|.0f}\\%; bateriile mai lungi tolerează erorile de sincronizare"))],
        height="0.62\\textheight", size="footnotesize",
        job=t("budget on a rule you can actually run: a better forecast (Lecture 2) closes part of the gap.",
              "bugetați pe baza unei reguli aplicabile: o prognoză mai bună (cursul 2) reduce o parte din diferență."),
        tryit=NB + " \\S7", cite=t("(" + OWN + ", " + LTM + ")", "(" + OWN + ", " + LTM + ")"))

    D.subsection(t("Probabilistic forecasts for trading", "Prognoze probabilistice pentru tranzacționare"))
    D.frame(t("Forecasting the whole price distribution helps a battery bid",
              "Prognoza întregii distribuții a prețului ajută o baterie să liciteze"), it(
        t(("\\textbf{What the work did}: forecast the joint next-day distribution of 96 hourly prices (24 h $\\times$ Romania, Bulgaria, Hungary, Czechia)",
           "distributional random forest, 37 predictors, Jan 2018 -- Sep 2024; 70 rolling windows: 365 days to train, the next 30 to test",
           "the median picks the charge hour and the later discharge hour; quantiles set the buy and sell limit prices"),
          ("\\textbf{Ce a făcut lucrarea}: a prognozat distribuția comună a celor 96 de prețuri orare de a doua zi (24 h $\\times$ România, Bulgaria, Ungaria, Cehia)",
           "pădure aleatoare distribuțională, 37 de predictori, ian.\\ 2018 -- sep.\\ 2024; 70 de ferestre mobile: 365 de zile de estimare, 30 de test",
           "mediana alege ora de încărcare și ora ulterioară de descărcare; cuantilele fixează prețurile-limită de cumpărare și de vînzare")),
        t(("\\textbf{What it found}: forecast errors peak at 17:00--18:00, usually the discharge hours",
           "Romania, cumulative profit of a 1 MW / 1 MWh battery: 143.0 thousand EUR with the quantile rule, 133.2 with fixed hours, 188.2 with perfect foresight",
           "the quantile rule beats the fixed-hour rule in all four markets; trading across markets adds value (150.3 thousand EUR)"),
          ("\\textbf{Ce a găsit}: erorile de prognoză sînt maxime la 17:00--18:00, de obicei orele de descărcare",
           "România, profitul cumulat al unei baterii de 1 MW / 1 MWh: 143,0 mii EUR cu regula cuantilelor, 133,2 cu ore fixe, 188,2 cu informație perfectă",
           "regula cuantilelor depășește regula cu ore fixe în toate cele patru piețe; tranzacționarea între piețe adaugă valoare (150,3 mii EUR)")),
        t("\\textbf{Investment}: with 500\\,000 EUR upfront, 90\\% efficiency, 15 years and 7\\%, day-ahead arbitrage alone does not cover it",
          "\\textbf{Investiția}: la 500\\,000 EUR, randament 90\\%, 15 ani și 7\\%, arbitrajul pe piața pentru ziua următoare nu o acoperă singur"),
        sep="2pt") + D.bottom(t("bid from forecast quantiles, not from a single price forecast: the hours that pay are in the tails.",
                                "licitați pe baza cuantilelor prognozei, nu a unei singure valori: orele profitabile sînt în cozile distribuției.")),
        "footnotesize", cite=t("(Andrei, Cepoi, Dumitrescu, Lessmann, Luchian, Pele \\& Petukhina, 2026, \\href{https://doi.org/10.2139/ssrn.6872381}{doi:10.2139/ssrn.6872381}; talk by C.\\,O.\\ Cepoi at AIDA 2026, Bucharest, 3 June 2026: "
                               "\\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/cepoi_battery_arbitrage.pdf}{slides})",
                               "(Andrei, Cepoi, Dumitrescu, Lessmann, Luchian, Pele \\& Petukhina, 2026, \\href{https://doi.org/10.2139/ssrn.6872381}{doi:10.2139/ssrn.6872381}; prezentarea lui C.\\,O.\\ Cepoi la AIDA 2026, București, 3 iunie 2026: "
                               "\\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/cepoi_battery_arbitrage.pdf}{diapozitive})"))

    D.subsection(t("15 minutes, self-cannibalisation, the region", "15 minute, autocanibalizare, regiunea"))
    D.concept(t("15-minute prices raised a 1-hour battery's revenue by @{bat.ltm.1.gain15|.1f}\\% on the same days",
                "Prețurile pe 15 minute au crescut cu @{bat.ltm.1.gain15|.1f}\\% venitul unei baterii de 1 oră, în aceleași zile"),
              t("Any hourly schedule can be run on quarter-hours, so finer prices can only add revenue.",
                "Orice program orar poate fi executat pe sferturi de oră, deci prețurile mai fine pot doar să adauge venit."),
              "\\[ R^{15}=\\max_{c,x}\\textstyle\\sum_t P^{15}_t(x_t-c_t)\\tfrac14\\ \\ge\\ R^{60} \\]" +
              "\\where{" + t("$R^{15}$ = optimal revenue on the 96 quarter-hour prices $P^{15}_t$; $R^{60}$ = optimal revenue when each hour is paid the mean of its quarters; "
                             "same days, so the difference is the value of granularity alone.",
                             "$R^{15}$ = venitul optim pe cele 96 de prețuri $P^{15}_t$; $R^{60}$ = venitul optim cînd fiecare oră este plătită la media sferturilor ei; "
                             "aceleași zile, deci diferența este doar valoarea detalierii.") + "}",
              it((t("\\textbf{Last 12 months, thousand EUR per MW}", "\\textbf{Ultimele 12 luni, mii EUR pe MW}"),
                  t("1 h: @{bat.ltm.1.hourly|.1f} $\\to$ @{bat.ltm.1.pf|.1f} (@{bat.ltm.1.gain15|+.1f}\\%)", "1 oră: @{bat.ltm.1.hourly|.1f} $\\to$ @{bat.ltm.1.pf|.1f} (@{bat.ltm.1.gain15|+.1f}\\%)"),
                  t("2 h: @{bat.ltm.2.hourly|.1f} $\\to$ @{bat.ltm.2.pf|.1f} (@{bat.ltm.2.gain15|+.1f}\\%)", "2 ore: @{bat.ltm.2.hourly|.1f} $\\to$ @{bat.ltm.2.pf|.1f} (@{bat.ltm.2.gain15|+.1f}\\%)"),
                  t("4 h: @{bat.ltm.4.hourly|.1f} $\\to$ @{bat.ltm.4.pf|.1f} (@{bat.ltm.4.gain15|+.1f}\\%)", "4 ore: @{bat.ltm.4.hourly|.1f} $\\to$ @{bat.ltm.4.pf|.1f} (@{bat.ltm.4.gain15|+.1f}\\%)")),
                 t("A comparison with the hourly year before would mix in price-level changes.", "O comparație cu anul anterior, orar, ar include și schimbarea nivelului prețurilor."), sep="2pt"),
              t("short batteries gain most from 15-minute prices.", "bateriile de durată scurtă cîștigă cel mai mult din prețurile pe 15 minute."),
              tryit=NB + " \\S8", cite="(NEMO Committee, 2025; " + OWN + ")", wl="0.50", wr="0.47")

    D.concept(t("Batteries cannibalise their own spread: on the local order book, 50 MW would have closed it on @{merit.day|date}",
                "Bateriile își canibalizează diferența de preț: pe ofertele locale, 50 MW ar fi anulat-o la @{merit.day|date}"),
              t("Charging adds demand at midday and discharging adds supply in the evening: both pull the two prices together.",
                "Încărcarea adaugă cerere la amiază, iar descărcarea adaugă ofertă seara; ambele apropie cele două prețuri."),
              "\\[ \\Delta P(X)=p^{*}_{\\text{" + t("eve", "seara") + "}}(+X\\text{ " + t("supply", "ofertă") + "})-p^{*}_{\\text{" + t("mid", "amiază") + "}}(+X\\text{ " + t("demand", "cerere") + "}) \\]" +
              "\\where{" + t("$X$ = MW of batteries; $p^*$ = clearing price recomputed on the OPCOM curves of 12:00--12:15 and 20:00--20:15 (Romanian time); flows fixed (Appendix C).",
                             "$X$ = puterea bateriilor (MW); $p^*$ = prețul recalculat pe curbele OPCOM pentru 12:00--12:15 și 20:00--20:15 (ora României); fluxuri fixe (Anexa C).") + "}",
              it((t("\\textbf{Evening minus midday price}", "\\textbf{Prețul de seară minus cel de la amiază}"),
                  t("actual @{merit.spread0|.2f} EUR/MWh", "realizat: @{merit.spread0|.2f} EUR/MWh"),
                  t("50 MW: @{merit.spread_bat50|.2f}; 100 MW: @{merit.spread_bat100|.2f}", "50 MW: @{merit.spread_bat50|.2f}; 100 MW: @{merit.spread_bat100|.2f}")),
                 (t("\\textbf{Fleets already running}", "\\textbf{Baterii deja în funcțiune}"),
                  t("Romania: battery output up to @{bat.fleet_RO_max|,.0f} MW in @{Y}", "România: bateriile au livrat pînă la @{bat.fleet_RO_max|,.0f} MW în @{Y}"),
                  t("Bulgaria, reported since @{bat.fleet_BG_first|date}: up to @{bat.fleet_BG_max|,.0f} MW", "Bulgaria (date raportate din @{bat.fleet_BG_first|date}): pînă la @{bat.fleet_BG_max|,.0f} MW")), sep="2pt"),
              t("model the spread after the fleet is built, not the spread seen before it.",
                "modelați diferența de preț de după construirea bateriilor, nu pe cea observată înainte."),
              tryit=NB + " \\S2", cite=t("(OPCOM aggregated curves; " + OWN + ")", "(curbele agregate OPCOM; " + OWN + ")"), wl="0.50", wr="0.47")

    D.chart(t("A Romanian battery competes for the same regional spread as the Bulgarian and Hungarian ones",
              "O baterie din România concurează pentru aceeași diferență regională de preț ca bateriile din Bulgaria și Ungaria"), "bat_region", [
        t(("\\textbf{2 hours, last 12 months, thousand EUR per MW}: Hungary @{bat.reg.HU|.1f}, Romania @{bat.reg.RO|.1f}, Bulgaria @{bat.reg.BG|.1f}, Germany @{bat.reg.DE_LU|.1f}",
           "daily revenue correlation with Romania: Bulgaria @{bat.corr_ro_bg|.2f}, Hungary @{bat.corr_ro_hu|.2f}"),
          ("\\textbf{2 ore, ultimele 12 luni, mii EUR pe MW}: Ungaria @{bat.reg.HU|.1f}, România @{bat.reg.RO|.1f}, Bulgaria @{bat.reg.BG|.1f}, Germania @{bat.reg.DE_LU|.1f}",
           "corelația veniturilor zilnice cu România: Bulgaria @{bat.corr_ro_bg|.2f}, Ungaria @{bat.corr_ro_hu|.2f}"))],
        height="0.60\\textheight", size="footnotesize",
        job=t("as announced in Lecture 1: a Romanian battery developer competes for the same regional evening spread.",
              "cum am anunțat în cursul 1: un dezvoltator român de baterii concurează pentru aceeași diferență regională de preț de seară."),
        tryit=NB + " \\S8", cite=t("(" + OWN + "; battery output as reported to ENTSO-E)", "(" + OWN + "; producția bateriilor raportată la ENTSO-E)"))

    D.concept(t("At 8\\% over 15 years, the 2-hour revenue supports at most @{bat.ltm.2.capex_wk_kw|,.0f} EUR per kW",
                "La 8\\% pe 15 ani, venitul bateriei de 2 ore justifică o investiție de cel mult @{bat.ltm.2.capex_wk_kw|,.0f} EUR pe kW"),
              t("The largest investment a yearly revenue can repay is that revenue times the annuity factor.",
                "Investiția maximă pe care o poate recupera un venit anual este venitul înmulțit cu factorul de anuitate."),
              "\\[ I^{\\max}=R\\cdot a(r,n) \\]\\[ a(r,n)=\\sum_{j=1}^{n}(1+r)^{-j}=\\frac{1-(1+r)^{-n}}{r} \\]" +
              "\\where{" + t("$R$ = yearly revenue per MW (EUR), $r$ = 8\\% (assumption), $n$ = 15 years (NREL), so $a$ = @{bat.af|.2f}; "
                             "$I^{\\max}/1\\,000$ = EUR per kilowatt (kW), Appendix D.",
                             "$R$ = venitul anual pe MW (EUR), $r$ = 8\\% (ipoteză), $n$ = 15 ani (NREL), deci $a$ = @{bat.af|.2f}; "
                             "$I^{\\max}/1\\,000$ = EUR pe kilowatt (kW), Anexa D.") + "}",
              it((t("\\textbf{2 hours, last 12 months}", "\\textbf{2 ore, ultimele 12 luni}"),
                  t("perfect foresight: @{bat.ltm.2.capex_pf_kw|,.0f} EUR/kW", "informație perfectă: @{bat.ltm.2.capex_pf_kw|,.0f} EUR/kW"),
                  t("7-day rule: @{bat.ltm.2.capex_wk_kw|,.0f} EUR/kW = @{bat.ltm.2.capex_wk_kwh|,.0f} EUR per kilowatt-hour (kWh)",
                    "regula de 7 zile: @{bat.ltm.2.capex_wk_kw|,.0f} EUR/kW = @{bat.ltm.2.capex_wk_kwh|,.0f} EUR pe kilowatt-oră (kWh)")),
                 (t("\\textbf{Not included}", "\\textbf{Ce nu am inclus}"),
                  t("operating costs, grid tariffs, fade: lower $I^{\\max}$", "costurile de operare, tarifele, pierderea capacității: reduc $I^{\\max}$"),
                  t("balancing revenue raises it; new fleets shrink the spread", "veniturile din echilibrare îl cresc; bateriile noi reduc diferența")), sep="2pt"),
              t("compare @{bat.ltm.2.capex_wk_kwh|,.0f} EUR/kWh with the turnkey quote before anything else.",
                "comparați @{bat.ltm.2.capex_wk_kwh|,.0f} EUR/kWh cu oferta pentru instalația la cheie, înaintea oricărei alte analize."),
              tryit=NB + " \\S8", cite="(Cole \\& Karmakar, 2023, NREL; Schmidt et al., 2019, Joule)", wl="0.47", wr="0.50")

    # ------------------------------------------------------------------ 6 case study
    D.section(t("Case studies: @{case.month|ym}; summer @{rogb.year}", "Studii de caz: @{case.month|ym}; vara @{rogb.year}"))
    D.subsection(t("@{case.month|ym}: the most negative hours", "@{case.month|ym}: cele mai multe ore cu preț negativ"))
    D.chart(t("Case study: in the week of @{case.week|date}, Romania had @{case.week_neg_h|.0f} negative hours and solar captured @{case.week_cr|.0f}\\%",
              "Studiu de caz: în săptămîna din @{case.week|date}, România a avut @{case.week_neg_h|.0f} " + de("case.week_neg_h") +
              "ore cu preț negativ, iar rata de captare solară a fost @{case.week_cr|.0f}\\%"), "case_week", [
        t(("\\textbf{Prices from @{case.week_min|.2f} to @{case.week_max|.2f} EUR/MWh}; solar CP @{case.week_cp|.1f} vs $B$ @{case.week_base|.1f}",
           "2-hour battery: @{case.week_bat2_mean_day|.0f} EUR per MW a day, against @{case.bat2_day_ltm|.0f} on an average day of the last 12 months"),
          ("\\textbf{Prețuri între @{case.week_min|.2f} și @{case.week_max|.2f} EUR/MWh}; CP solar @{case.week_cp|.1f}, față de $B$ @{case.week_base|.1f}",
           "bateria de 2 ore: @{case.week_bat2_mean_day|.0f} EUR pe MW pe zi, față de @{case.bat2_day_ltm|.0f} într-o zi medie din ultimele 12 luni"))],
        height="0.62\\textheight", size="footnotesize",
        job=t("the same sunny week is the worst for a solar park and among the best for a battery.",
              "aceeași săptămînă însorită este cea mai slabă pentru un parc solar și una dintre cele mai bune pentru o baterie."),
        tryit=NB + " \\S9", cite=t("(" + OWN + "; schedule with perfect foresight)", "(" + OWN + "; program cu informație perfectă)"))

    D.frame(t("Case study: what @{case.month|ym} meant for each player in the Romanian market",
              "Studiu de caz: ce a însemnat luna @{case.month|ym} pentru fiecare participant la piață"), it(
        t(("\\textbf{Solar developer}: capture rate @{case.cr_solar|.1f}\\% (@{case.cp_solar|.1f} vs @{case.base|.1f} EUR/MWh)",
           "@{case.e_neg_pct|.1f}\\% of output at negative prices; decision: storage on site, or a PPA that prices the solar profile"),
          ("\\textbf{Dezvoltatorul solar}: rata de captare @{case.cr_solar|.1f}\\% (@{case.cp_solar|.1f} față de @{case.base|.1f} EUR/MWh)",
           "@{case.e_neg_pct|.1f}\\% din producție la prețuri negative; decizie: stocare în același amplasament sau un PPA care stabilește prețul profilului solar")),
        t(("\\textbf{Wind developer}: capture rate @{case.cr_wind|.1f}\\%", "in Romania, wind is not the cannibalised technology"),
          ("\\textbf{Dezvoltatorul eolian}: rata de captare @{case.cr_wind|.1f}\\%", "în România, eolianul nu este tehnologia canibalizată")),
        t(("\\textbf{Battery developer}: 2 hours, @{case.bat2_day|.0f} EUR per MW a day", "against @{case.bat2_day_ltm|.0f} on average over the last 12 months"),
          ("\\textbf{Dezvoltatorul de baterii}: 2 ore, @{case.bat2_day|.0f} EUR pe MW pe zi", "față de @{case.bat2_day_ltm|.0f} în medie în ultimele 12 luni")),
        t(("\\textbf{Supplier and industrial consumer}: @{case.neg_h|.0f} negative hours", "moving consumption to spring middays is paid"),
          ("\\textbf{Furnizorul și consumatorul industrial}: @{case.neg_h|.0f} " + de("case.neg_h") + "ore cu preț negativ", "mutarea consumului la amiază, primăvara, este plătită")),
        t(("\\textbf{Transelectrica}", "after sunset the evening ramp and the interconnectors set the price"),
          ("\\textbf{Transelectrica}", "după apus, creșterea cererii nete și interconexiunile fixează prețul")),
        sep="3pt") + D.bottom(None, NB + " \\S9"), "footnotesize", cite=t("(" + OWN + ")", "(" + OWN + ")"))

    # ------------------------------------------------------------------ 6b case study: summer, Romania and Bulgaria
    D.subsection(t("Summer @{rogb.year}: Romania and Bulgaria", "Vara @{rogb.year}: România și Bulgaria"))
    D.chart(t("Summer @{rogb.year}: midday exports, evening imports from Bulgaria",
              "Vara @{rogb.year}: export la prînz, import seara din Bulgaria"), "rogb_summer", [
        t(("\\textbf{Midday: Romania exports}, @{rogb.exp_mw|,.0f} MW net at 12:00 on all borders",
           "mostly to Hungary (@{rogb.hu_mid_mw|,.0f} MW) and Serbia (@{rogb.rs_mid_mw|,.0f} MW); to Bulgaria on only @{rogb.n_days_mid} of @{rogb.n_days} days (12:00--15:00)"),
          ("\\textbf{La prînz România exportă}: @{rogb.exp_mw|,.0f} MW net la ora 12, pe toate granițele",
           "mai ales spre Ungaria (@{rogb.hu_mid_mw|,.0f} MW) și Serbia (@{rogb.rs_mid_mw|,.0f} MW); spre Bulgaria doar în @{rogb.n_days_mid} din @{rogb.n_days} de zile (12:00--15:00)")),
        t(("\\textbf{Evening: Romania imports from Bulgaria}, @{rogb.bg_eve_mw|,.0f} MW at 21:00, on all @{rogb.n_days} days",
           "price at 21:00: Romania @{rogb.p_ro_eve|.1f}, Bulgaria @{rogb.p_bg_eve|.1f} EUR/MWh; the full border separates the two prices"),
          ("\\textbf{Seara România importă din Bulgaria}: @{rogb.bg_eve_mw|,.0f} MW la ora 21, în toate cele @{rogb.n_days} de zile",
           "prețul la ora 21: România @{rogb.p_ro_eve|.1f}, Bulgaria @{rogb.p_bg_eve|.1f} EUR/MWh; granița plină separă cele două prețuri"))],
        height="0.50\\textheight", size="footnotesize",
        job=t("the evening gap of @{rogb.p_gap_eve|.1f} EUR/MWh is the value of evening storage and interconnection.",
              "diferența de seară, de @{rogb.p_gap_eve|.1f} EUR/MWh, este valoarea stocării de seară și a interconexiunii."),
        cite=t("(" + OWN + "; + = import into Romania)", "(" + OWN + "; + = import în România)"))

    # ------------------------------------------------------------------ wrap-up
    D.parts.append("\\section*{" + t("Wrap-up", "Recapitulare") + "}\n")
    D.quiz_frame(t("capture rate", "rata de captare"),
                 t("A solar PPA is offered at the @{YP} baseload forward of @{capt.RO.solar.2025.base|.0f} EUR/MWh; what does the solar profile really earn?",
                   "Vi se oferă un PPA solar la prețul de bază din @{YP}, de @{capt.RO.solar.2025.base|.0f} EUR/MWh; cît obține de fapt profilul solar?"),
                 t("About @{capt.RO.solar.2025.cp|.0f} EUR/MWh in 2025 (capture rate @{capt.RO.solar.2025.crp|.0f}\\%); the buyer at the baseload price pays a large premium for the profile.",
                   "Aproximativ @{capt.RO.solar.2025.cp|.0f} EUR/MWh în 2025 (rata de captare @{capt.RO.solar.2025.crp|.0f}\\%); cumpărătorul care plătește prețul de bază plătește o primă mare pentru profil."))
    D.quiz_frame(t("counting negative prices", "numărarea prețurilor negative"),
                 t("Since 1 October 2025, Romania has had @{neg.q15.n_negq} negative quarter-hours; how many negative hours do you report?",
                   "De la 1 octombrie 2025, România a avut @{neg.q15.n_negq} " + de("neg.q15.n_negq") + "sferturi de oră cu preț negativ; cîte ore cu preț negativ raportați?"),
                 t("@{neg.q15.h_negq|.2f} hour-equivalents ($\\times$0.25 h), not @{neg.q15.n_negq} hours.",
                   "@{neg.q15.h_negq|.2f} ore echivalente (fiecare sfert de oră contează 0{,}25 h), nu @{neg.q15.n_negq} " + de("neg.q15.n_negq") + "ore."))
    D.quiz_frame(t("battery duration", "durata bateriei"),
                 t("Doubling storage from 2 h to 4 h doubles the cost of the cells; does it double revenue?",
                   "Dublarea stocării de la 2 la 4 ore dublează costul celulelor; se dublează și venitul?"),
                 t("No: in the last 12 months a 4-hour battery earned @{bat.x_4v2|.2f} times what a 2-hour one earned, because the extra hours trade a smaller spread.",
                   "Nu; în ultimele 12 luni, o baterie de 4 ore a cîștigat de @{bat.x_4v2|.2f} ori cît una de 2 ore, deoarece orele suplimentare valorifică o diferență de preț mai mică."))
    D.quiz_frame(t("the merit-order effect", "efectul ordinii de merit"),
                 t("On the OPCOM curves of @{merit.day|date}, 25 MW more at zero price lowers the midday price to @{merit.mid.sup.25|.1f} EUR/MWh; is this what a new 25 MW park does?",
                   "Pe curbele OPCOM din @{merit.day|date}, 25 MW în plus la preț zero coboară prețul de la amiază la @{merit.mid.sup.25|.1f} EUR/MWh; acesta este efectul unui parc nou de 25 MW?"),
                 t("No: the curves hold cross-border flows fixed; in the coupled market part of the extra output is exported, so the true effect is smaller (the regression gives a fall of about @{reg.solar_babs|.0f} EUR/MWh per GW).",
                   "Nu; curbele păstrează fixe fluxurile transfrontaliere, iar în piața cuplată o parte din producție se exportă, deci efectul real este mai mic (regresia dă o scădere de aproximativ @{reg.solar_babs|.0f} EUR/MWh pentru fiecare GW)."))

    D.frame(t("Wrap-up", "Recapitulare"), "\\vspace{-2mm}\\begin{multicols}{2}\\scriptsize\\tableofcontents\\end{multicols}\n" + it(
        t("Solar lowers the price it is paid: Romanian capture rate @{capt.RO.solar.2019.crp|.0f}\\% (2019) $\\to$ @{capt.RO.solar.2025.crp|.0f}\\% (2025); wind near 100\\%.",
          "Producția solară reduce prețul pe care îl primește; rata de captare în România: @{capt.RO.solar.2019.crp|.0f}\\% (2019) $\\to$ @{capt.RO.solar.2025.crp|.0f}\\% (2025); eolianul rămîne aproape de 100\\%."),
        t("Batteries live on the same regional spread: @{bat.ltm.2.pf|.0f} thousand EUR per MW for 2 h with perfect foresight, about @{bat.ltm.2.wk_pct|.0f}\\% of it with a simple rule; next: Lecture 7.",
          "Bateriile trăiesc din aceeași diferență regională de preț; @{bat.ltm.2.pf|.0f} mii EUR pe MW pentru 2 ore, cu informație perfectă, și circa @{bat.ltm.2.wk_pct|.0f}\\% din această sumă cu o regulă simplă; urmează cursul 7."),
        sep="1pt"))

    D.frame(t("Research from our group on renewables and Romanian prices", "Cercetările grupului nostru despre sursele regenerabile și prețurile din România"), it(
        t(("\\textbf{Explaining price drops and spikes} (Andrei \\& Pele, 2025, Preprints)", "what the paper did: detected unusual hourly Romanian prices with an isolation forest and explained them with Shapley values",
           "result: wind and solar output drive the price drops; load forecast errors and conventional generation drive the spikes"),
          ("\\textbf{Explicarea scăderilor și salturilor de preț} (Andrei \\& Pele, 2025, Preprints)", "ce a făcut lucrarea: a identificat prețurile orare neobișnuite din România cu algoritmul isolation forest și le-a explicat cu valori Shapley",
           "rezultat: producția eoliană și cea solară explică scăderile de preț; erorile de prognoză a consumului și producția convențională explică salturile")),
        t(("\\textbf{Price drivers by horizon and regime} (Andrei, Pele \\& Cramer, 2026, PICBE)", "what the paper did: forecast Romanian hourly prices 2018--2024 with tree ensembles and measured which drivers matter at each horizon and in low-, normal- and high-price regimes",
           "use here: the renewable drivers behind the low-price regime of this lecture"),
          ("\\textbf{Factorii prețului pe orizonturi și regimuri} (Andrei, Pele \\& Cramer, 2026, PICBE)", "ce a făcut lucrarea: a prognozat prețurile orare din România în perioada 2018--2024 cu ansambluri de arbori și a măsurat ce factori contează la fiecare orizont și în regimurile de preț scăzut, normal și ridicat",
           "legătura cu acest curs: factorii regenerabili din spatele regimului de preț scăzut")),
        t(("\\textbf{Early warning of spikes} (Andrei, Pele, Cramer, Amza \\& Diaconu, 2026, PICBE)", "what the paper did: built an explainable artificial intelligence (AI) early-warning system for Romanian price spikes",
           "result: the residual-load forecast is the main driver, the variable of our regression"),
          ("\\textbf{Avertizarea timpurie a salturilor de preț} (Andrei, Pele, Cramer, Amza \\& Diaconu, 2026, PICBE)", "ce a făcut lucrarea: a construit un sistem explicabil de inteligență artificială (AI) pentru avertizarea timpurie a salturilor de preț din România",
           "rezultat: prognoza consumului rezidual este principalul factor, aceeași variabilă ca în regresia noastră")),
        t(("\\textbf{Price elasticity of demand} (Proșcanu, Proșcanu \\& Pele, 2025, JSES)", "what the paper did: tested Granger causality between Romanian consumption and price",
           "result: consumption does not react to price, hence the almost vertical demand curve of the merit order"),
          ("\\textbf{Elasticitatea cererii de energie electrică} (Proșcanu, Proșcanu \\& Pele, 2025, JSES)", "ce a făcut lucrarea: a testat cauzalitatea Granger între consumul și prețul energiei electrice din România",
           "rezultat: consumul nu reacționează la preț, de aici curba cererii aproape verticală din ordinea de merit")),
        sep="2pt") + note(t("Findings as stated in the papers; numbers on the other slides come from our own data.",
                            "Rezultatele de pe acest diapozitiv sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.")),
        "footnotesize", cite=t("(Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting)",
                               "(Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică)"))

    D.frame(t("Further reading and resources", "Lecturi și resurse suplimentare"), cols(it(
        t("\\textbf{Hirth (2013)}: the reference paper on the value factor of wind and solar: ",
          "\\textbf{Hirth (2013)}: lucrarea de referință despre rata de captare a energiei eoliene și solare: ") + "\\href{https://doi.org/10.1016/j.eneco.2013.02.004}{doi:10.1016/j.eneco.2013.02.004}.",
        t("\\textbf{Cole \\& Karmakar (2023)}: battery costs, efficiency and lifetime used in this lecture: ",
          "\\textbf{Cole \\& Karmakar (2023)}: costurile, randamentul și durata de viață a bateriilor, folosite în acest curs: ") +
        "\\href{https://doi.org/10.2172/1984976}{doi:10.2172/1984976}.",
        t("\\textbf{energy-charts.info}: live prices, generation and installed capacity for Romania and its neighbours: ",
          "\\textbf{energy-charts.info}: prețuri, producție și putere instalată, actualizate, pentru România și vecinii ei: ") +
        "\\href{https://energy-charts.info}{energy-charts.info}.", sep="4pt"),
        it(t("\\textbf{This course}: code, data, notebooks --- ", "\\textbf{Acest curs}: cod, date, notebook-uri Jupyter --- ") +
           "\\href{https://github.com/danpele/EMQA}{github.com/danpele/EMQA}.",
           t("\\textbf{OPCOM aggregated curves}: download another day and repeat the merit-order computation: ",
             "\\textbf{Curbele agregate OPCOM}: descărcați altă zi și repetați calculul ordinii de merit: ") +
           "\\href{https://www.opcom.ro/rapoarte-pzu-curbe-agregate/ro}{opcom.ro}.",
           t("\\textbf{Experiment yourself}: the notebook reproduces every chart and number of this lecture.",
             "\\textbf{Exercițiu practic}: notebook-ul Jupyter reproduce toate graficele și cifrele din acest curs."), sep="4pt"), "0.52", "0.45"))

    REFS = [
        "Andrei, A.-V.\\ \\& Pele, D.\\,T.\\ (2025). Explainable AI for electricity price anomaly detection: A SHAP-driven approach in Romania's "
        "energy market. \\textit{Preprints}. \\href{https://doi.org/10.20944/preprints202508.0410.v1}{doi:10.20944/preprints202508.0410.v1}",
        "Andrei, A.-V., Cepoi, C., Dumitrescu, B.-A., Lessmann, S., Luchian, A., Pele, D.-T.\\ \\& Petukhina, A.\\ (2026). Joint probabilistic "
        "forecasting for battery arbitrage in day-ahead power markets. SSRN Working Paper 6872381. \\href{https://doi.org/10.2139/ssrn.6872381}{doi:10.2139/ssrn.6872381}",
        "Andrei, A.-V., Pele, D.-T.\\ \\& Cramer, A.-A.\\ (2026). Multi-horizon explainability in energy price forecasting: Disentangling "
        "market dynamics and renewable intermittency in Romania's liberalized electricity market. \\textit{Proceedings of the "
        "International Conference on Business Excellence}, 20(1), 104--117. \\href{https://doi.org/10.2478/picbe-2026-0014}{doi:10.2478/picbe-2026-0014}",
        "Andrei, A.-V., Pele, D.-T., Cramer, A.-A., Amza, A.\\ \\& Diaconu, D.\\ (2026). Explainable AI-based early warning system for electricity "
        "price spikes: Evidence from the Romanian market. \\textit{Proceedings of the International Conference on Business Excellence}, 20(1), "
        "4820--4836. \\href{https://doi.org/10.2478/picbe-2026-0352}{doi:10.2478/picbe-2026-0352}",
        "Basangova, M., Bolovăneanu, V., Conda, A., Erlwein-Sayer, C., Melzer, A., Pele, D.\\,T., Petukhina, A.\\ \\& Phan, M.\\ (2026). Day-ahead "
        "forecasting for redispatch measures using machine learning models. Talk at the AIDA Conference, Bucharest University of Economic Studies, "
        "3 June 2026. \\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/bolovaneanu_redispatch_forecasting.pdf}{github.com/danpele/EMQA}",
        "Bradbury, K., Pratson, L.\\ \\& Patiño-Echeverri, D.\\ (2014). Economic viability of energy storage systems based on price arbitrage "
        "potential in real-time U.S.\\ electricity markets. \\textit{Applied Energy}, 114, 512--519. \\href{https://doi.org/10.1016/j.apenergy.2013.10.010}{doi:10.1016/j.apenergy.2013.10.010}",
        "Cludius, J., Hermann, H., Matthes, F.\\,C.\\ \\& Graichen, V.\\ (2014). The merit order effect of wind and photovoltaic electricity "
        "generation in Germany 2008--2016: Estimation and distributional implications. \\textit{Energy Economics}, 44, 302--313. "
        "\\href{https://doi.org/10.1016/j.eneco.2014.04.020}{doi:10.1016/j.eneco.2014.04.020}",
        "Cepoi, C.\\,O.\\ (2026). Uncertainty meets opportunity: Joint probabilistic forecasting for battery arbitrage in CEE day-ahead power "
        "markets. Talk at the AIDA Conference, Bucharest University of Economic Studies, 3 June 2026. "
        "\\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/cepoi_battery_arbitrage.pdf}{github.com/danpele/EMQA}",
        "Cole, W.\\ \\& Karmakar, A.\\ (2023). Cost projections for utility-scale battery storage: 2023 update. NREL/TP-6A40-85332, National "
        "Renewable Energy Laboratory. \\href{https://doi.org/10.2172/1984976}{doi:10.2172/1984976}",
        "Fanone, E., Gamba, A.\\ \\& Prokopczuk, M.\\ (2013). The case of negative day-ahead electricity prices. \\textit{Energy Economics}, 35, "
        "22--34. \\href{https://doi.org/10.1016/j.eneco.2011.12.006}{doi:10.1016/j.eneco.2011.12.006}",
        "Hirth, L.\\ (2013). The market value of variable renewables: The effect of solar wind power variability on their relative price. "
        "\\textit{Energy Economics}, 38, 218--236. \\href{https://doi.org/10.1016/j.eneco.2013.02.004}{doi:10.1016/j.eneco.2013.02.004}",
        "Hirth, L., Ueckerdt, F.\\ \\& Edenhofer, O.\\ (2016). Why wind is not coal: On the economics of electricity generation. "
        "\\textit{The Energy Journal}, 37(3), 1--28. \\href{https://doi.org/10.5547/01956574.37.3.lhir}{doi:10.5547/01956574.37.3.lhir}",
        "López Prol, J., Steininger, K.\\,W.\\ \\& Zilberman, D.\\ (2020). The cannibalization effect of wind and solar in the California "
        "wholesale electricity market. \\textit{Energy Economics}, 85, 104552. \\href{https://doi.org/10.1016/j.eneco.2019.104552}{doi:10.1016/j.eneco.2019.104552}",
        "NEMO Committee (2025). 15-Minute MTU in SDAC was implemented. Single Day-Ahead Coupling (SDAC) press release, 1 October 2025. "
        "\\href{https://nemo-committee.eu/assets/files/15-minute-mtu-in-sdac-was-implemented.pdf}{nemo-committee.eu}",
        "Proșcanu, C., Proșcanu, M.\\ \\& Pele, D.\\,T.\\ (2025). The price elasticity of electricity demand in Romania. \\textit{Journal of "
        "Social and Economic Statistics}, 14(2), 131--141. \\href{https://doi.org/10.2478/jses-2025-0009}{doi:10.2478/jses-2025-0009}",
        "Schmidt, O., Melchior, S., Hawkes, A.\\ \\& Staffell, I.\\ (2019). Projecting the future levelized cost of electricity storage "
        "technologies. \\textit{Joule}, 3(1), 81--100. \\href{https://doi.org/10.1016/j.joule.2018.12.008}{doi:10.1016/j.joule.2018.12.008}",
        "Sensfuß, F., Ragwitz, M.\\ \\& Genoese, M.\\ (2008). The merit-order effect: A detailed analysis of the price effect of renewable "
        "electricity generation on spot market prices in Germany. \\textit{Energy Policy}, 36(8), 3086--3094. \\href{https://doi.org/10.1016/j.enpol.2008.03.035}{doi:10.1016/j.enpol.2008.03.035}",
        "Sioshansi, R., Denholm, P., Jenkin, T.\\ \\& Weiss, J.\\ (2009). Estimating the value of electricity storage in PJM: Arbitrage and "
        "some welfare effects. \\textit{Energy Economics}, 31(2), 269--277. \\href{https://doi.org/10.1016/j.eneco.2008.10.005}{doi:10.1016/j.eneco.2008.10.005}",
        "Weron, R.\\ (2014). Electricity price forecasting: A review of the state-of-the-art with a look into the future. "
        "\\textit{International Journal of Forecasting}, 30(4), 1030--1081. \\href{https://doi.org/10.1016/j.ijforecast.2014.08.008}{doi:10.1016/j.ijforecast.2014.08.008}",
        "Würzburg, K., Labandeira, X.\\ \\& Linares, P.\\ (2013). Renewable generation and electricity prices: Taking stock and new evidence "
        "for Germany and Austria. \\textit{Energy Economics}, 40, S159--S171. \\href{https://doi.org/10.1016/j.eneco.2013.09.011}{doi:10.1016/j.eneco.2013.09.011}",
    ]
    for part, (a_, b_) in enumerate([(0, 7), (7, 14), (14, len(REFS))]):
        D.frame(t("References", "Bibliografie") + f" ({part + 1}/3)", "\\begin{itemize}\\setlength{\\itemsep}{1pt}\\scriptsize\n" +
                "\n".join("\\item " + r for r in REFS[a_:b_]) + "\n\\end{itemize}", "scriptsize")

    # ------------------------------------------------------------------ appendix
    D.mark_main_end()
    D.parts.append("\\section*{" + t("Appendix", "Anexă") + "}\n")
    D.frame(t("Appendix A: the capture rate is one plus a scaled covariance", "Anexa A: rata de captare este unu plus o covarianță scalată"), it(
        t(("\\textbf{Notation}", "weights $w_t=\\Delta_t/\\sum_s\\Delta_s$; $\\bar P=\\sum_t w_tP_t=B$; $\\bar G=\\sum_t w_tG_t$; $\\mathrm{Cov}_\\Delta(P,G)=\\sum_t w_t(P_t-\\bar P)(G_t-\\bar G)$"),
          ("\\textbf{Notație}", "ponderile $w_t=\\Delta_t/\\sum_s\\Delta_s$; $\\bar P=\\sum_t w_tP_t=B$; $\\bar G=\\sum_t w_tG_t$; $\\mathrm{Cov}_\\Delta(P,G)=\\sum_t w_t(P_t-\\bar P)(G_t-\\bar G)$")),
        t(("\\textbf{Step 1}", "divide numerator and denominator of CP by $\\sum_s\\Delta_s$: $\\mathrm{CP}=\\sum_t w_tP_tG_t\\,/\\,\\bar G$"),
          ("\\textbf{Pasul 1}", "se împart numărătorul și numitorul lui CP la $\\sum_s\\Delta_s$: $\\mathrm{CP}=\\sum_t w_tP_tG_t\\,/\\,\\bar G$")),
        t(("\\textbf{Step 2}", "$\\sum_t w_tP_tG_t=\\mathrm{Cov}_\\Delta(P,G)+\\bar P\\bar G$ (definition of the covariance)"),
          ("\\textbf{Pasul 2}", "$\\sum_t w_tP_tG_t=\\mathrm{Cov}_\\Delta(P,G)+\\bar P\\bar G$ (definiția covarianței)")),
        t(("\\textbf{Step 3}", "$\\mathrm{CR}=\\mathrm{CP}/\\bar P=1+\\mathrm{Cov}_\\Delta(P,G)/(\\bar P\\bar G)$",
           "Romanian solar, " + YTD + ": $\\bar P$ = @{capt.cov.mp|.1f}, $\\bar G$ = @{capt.cov.mg|,.0f} MW, covariance @{capt.cov.cov|,.0f}, so CR = @{capt.cov.cr|.3f}"),
          ("\\textbf{Pasul 3}", "$\\mathrm{CR}=\\mathrm{CP}/\\bar P=1+\\mathrm{Cov}_\\Delta(P,G)/(\\bar P\\bar G)$",
           "producția solară din România, " + YTD + ": $\\bar P$ = @{capt.cov.mp|.1f}, $\\bar G$ = @{capt.cov.mg|,.0f} MW, covarianța @{capt.cov.cov|,.0f}, deci CR = @{capt.cov.cr|.3f}")),
        t(("\\textbf{Reading}", "CR $<1$ exactly when output is high in cheap intervals; CR is undefined if $\\bar P\\le 0$"),
          ("\\textbf{Interpretare}", "CR $<1$ exact atunci cînd producția este mare în intervalele ieftine; CR nu este definită dacă $\\bar P\\le 0$")),
        sep="3pt"), "footnotesize", cite="(Hirth, 2013, ENEECO)")

    D.frame(t("Appendix B: the battery programme in matrix form", "Anexa B: programul bateriei în formă matriceală"), it(
        t(("\\textbf{Variables}", "$z=(c_1..c_T,\\,x_1..x_T,\\,e_1..e_T)$, $3T$ variables, $T$ = 92, 96 or 100 quarter-hours (24 hours before October 2025)"),
          ("\\textbf{Variabile}", "$z=(c_1..c_T,\\,x_1..x_T,\\,e_1..e_T)$, $3T$ variabile; $T$ = 92, 96 sau 100 de sferturi de oră (24 de ore înainte de octombrie 2025)")),
        t(("\\textbf{Objective}", "minimise $\\sum_t P_t\\Delta_t c_t-\\sum_t P_t\\Delta_t x_t$ (the negative of revenue)"),
          ("\\textbf{Funcția obiectiv}", "se minimizează $\\sum_t P_t\\Delta_t c_t-\\sum_t P_t\\Delta_t x_t$ (venitul cu semn schimbat)")),
        t(("\\textbf{Equalities}", "$e_t-e_{t-1}-\\sqrt\\eta\\Delta_tc_t+\\Delta_tx_t/\\sqrt\\eta=0$ for $t=1..T$, with $e_0=0$; and $e_T=0$"),
          ("\\textbf{Egalități}", "$e_t-e_{t-1}-\\sqrt\\eta\\Delta_tc_t+\\Delta_tx_t/\\sqrt\\eta=0$ pentru $t=1..T$, cu $e_0=0$; în plus, $e_T=0$")),
        t(("\\textbf{Inequality and bounds}", "$\\sum_t\\Delta_tx_t/\\sqrt\\eta\\le E$; $0\\le c_t,x_t\\le1$; $0\\le e_t\\le E$; solved with the HiGHS solver (scipy)"),
          ("\\textbf{Inegalitate și limite}", "$\\sum_t\\Delta_tx_t/\\sqrt\\eta\\le E$; $0\\le c_t,x_t\\le1$; $0\\le e_t\\le E$; rezolvare cu algoritmul HiGHS (scipy)")),
        t(("\\textbf{Forecast rules}", "the programme is solved on $\\hat P_t$ (mean of the last 7 days, or day $d-1$), then revenue is $\\sum_tP_t(x_t-c_t)\\Delta_t$ with the real $P_t$",
           "days whose length differs from the forecast's (clock changes) are dropped: @{bat.ltm.2.n_common} of @{bat.ltm.2.n_days} days kept"),
          ("\\textbf{Regulile de prognoză}", "programul se rezolvă pe $\\hat P_t$ (media ultimelor 7 zile sau prețurile zilei $d-1$), apoi venitul este $\\sum_tP_t(x_t-c_t)\\Delta_t$, cu prețurile reale $P_t$",
           "zilele cu alt număr de intervale decît prognoza (schimbarea orei) sînt eliminate: rămîn @{bat.ltm.2.n_common} din @{bat.ltm.2.n_days} zile")),
        sep="3pt"), "footnotesize", cite="(Sioshansi et al., 2009, ENEECO)")

    D.frame(t("Appendix C: recomputing the clearing price on the OPCOM curves", "Anexa C: recalcularea prețului de închidere pe curbele OPCOM"), it(
        t(("\\textbf{Curves}", "OPCOM publishes, per quarter-hour, the aggregated supply and demand points (price, cumulative MW) in XML",
           "blocks, hourly orders and net cross-border flows are added at the price limits ($-$600 and $+$4\\,000 EUR/MWh), as in OPCOM's own chart"),
          ("\\textbf{Curbele}", "OPCOM publică, pentru fiecare sfert de oră, punctele agregate ale ofertei și cererii (preț, MW cumulați), în format XML",
           "blocurile, ordinele orare și fluxurile transfrontaliere nete se adaugă la limitele de preț ($-$600 și $+$4\\,000 EUR/MWh), ca în graficul OPCOM")),
        t(("\\textbf{Algorithm}", "$S(p)$, $D(p)$ = linear interpolation between published points; new price = lowest $p$ with $S(p)+X\\mathbf 1[p\\ge0]-D(p)\\ge0$, by bisection on $[-600,4000]$",
           "for battery charging, $X$ MW of demand at any price are added to $D$"),
          ("\\textbf{Algoritmul}", "$S(p)$, $D(p)$ = interpolare liniară între punctele publicate; noul preț = cel mai mic $p$ pentru care $S(p)+X\\mathbf 1[p\\ge0]-D(p)\\ge0$, găsit prin bisecție pe $[-600,4000]$",
           "pentru încărcarea bateriilor, se adaugă la $D$ cererea de $X$ MW la orice preț")),
        t(("\\textbf{Check}", "with $X=0$ the curves cross on a flat segment: midday prices from @{merit.mid.p_curve_low|.2f} upwards, evening from @{merit.eve.p_curve_low|.2f}; the official prices @{merit.mid.price|.2f} and @{merit.eve.price|.2f} lie on these segments",
           "the official price, not the curve, is used at $X=0$"),
          ("\\textbf{Verificare}", "pentru $X=0$, curbele se intersectează pe un segment orizontal: la amiază de la @{merit.mid.p_curve_low|.2f} în sus, seara de la @{merit.eve.p_curve_low|.2f}; prețurile oficiale @{merit.mid.price|.2f} și @{merit.eve.price|.2f} se află pe aceste segmente",
           "pentru $X=0$ folosim prețul oficial")),
        sep="3pt"), "footnotesize", cite="(OPCOM; data/clean/opcom\\_pzu\\_curves\\_meta.json)")

    D.frame(t("Appendix D: the annuity factor", "Anexa D: factorul de anuitate"), it(
        t(("\\textbf{Present value of a constant revenue}", "$V=\\sum_{j=1}^{n}R(1+r)^{-j}=R\\,q\\,\\frac{1-q^{n}}{1-q}$ with $q=(1+r)^{-1}$"),
          ("\\textbf{Valoarea actualizată a unui venit constant}", "$V=\\sum_{j=1}^{n}R(1+r)^{-j}=R\\,q\\,\\frac{1-q^{n}}{1-q}$, cu $q=(1+r)^{-1}$")),
        t(("\\textbf{Simplify}", "$q/(1-q)=1/r$, hence $V=R\\,\\frac{1-(1+r)^{-n}}{r}=R\\,a(r,n)$"),
          ("\\textbf{Simplificare}", "$q/(1-q)=1/r$, deci $V=R\\,\\frac{1-(1+r)^{-n}}{r}=R\\,a(r,n)$")),
        t(("\\textbf{Break-even}", "the project pays back if investment $I\\le V$; with $r$ = 8\\%, $n$ = 15: $a$ = @{bat.af|.2f}"),
          ("\\textbf{Pragul de rentabilitate}", "proiectul se recuperează dacă investiția $I\\le V$; pentru $r$ = 8\\% și $n$ = 15: $a$ = @{bat.af|.2f}")),
        t(("\\textbf{Per kWh of storage}", "$I^{\\max}/E$: for 1, 2, 4 h with the 7-day rule, @{bat.ltm.1.capex_wk_kwh|,.0f}, @{bat.ltm.2.capex_wk_kwh|,.0f}, @{bat.ltm.4.capex_wk_kwh|,.0f} EUR/kWh"),
          ("\\textbf{Pe kWh de stocare}", "$I^{\\max}/E$: pentru 1, 2 și 4 ore, cu regula de 7 zile, @{bat.ltm.1.capex_wk_kwh|,.0f}, @{bat.ltm.2.capex_wk_kwh|,.0f} și @{bat.ltm.4.capex_wk_kwh|,.0f} EUR/kWh")),
        sep="3pt"), "footnotesize", cite="(Cole \\& Karmakar, 2023, NREL)")
    return D


def main(langs):
    ok = True
    for lang in langs:
        name = "lecture6" if lang == "en" else "lecture6_ro"
        out = os.path.join(HERE, name + ".tex")
        D, tex, res, H = autofit(build, out, lang)
        print(f"[{lang}] frames: main {D.n_main} (incl. title and section outlines), total {D.n_frames}; quiz frames {D.quiz}; "
              f"pages {res['pages']}; errors {res['errors']}; overfull>1pt {len(res['overfull'])}")
        for kind, amt, title in res["where"]:
            print(f"     {kind} {amt:6.1f}pt  {title}")
        small = {k: v for k, v in D.used_h.items() if v < 0.40}
        print(f"[{lang}] figure heights (fraction of text height) below 0.40:", small)
        defined = set(ABBR)
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
