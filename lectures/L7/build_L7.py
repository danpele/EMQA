r"""
build_L7.py -- Lecture 7 "Machine learning for energy markets" (EMQA), English and Romanian from one source
==========================================================================================================
Writes lectures/L7/lecture7.tex (EN) and lectures/L7/lecture7_ro.tex (RO) from the bilingual slide text in this file
and the numbers in L7_numbers.json (produced by analysis_L7.py), compiles both with pdflatex and checks: 0 LaTeX errors;
no overfull box > 1 pt (nothing masked); every acronym in the Abbreviations frames and spelled out at first use;
contact sheets for the visual check.

Run (from the repository root):
    python3 lectures/L7/analysis_L7.py
    python3 lectures/L7/build_L7.py            # both languages;  add "en" or "ro" for one

Rules as in Lectures 1-2: no computed number typed by hand (results are @{key} placeholders); hand-typed numbers are
definitions (12:00 CET, 85%/15% split, 2048 hours of context, 24 random configurations, C = 30 EUR/MWh assumed, 0.5) and
institutional dates.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "common"))
from emqa_build import (Deck, Numbers, acronym_audit, autofit, cols, contact_sheet,  # noqa: E402
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
    "AI": ("artificial intelligence", "inteligență artificială"),
    "ARIMA": ("autoregressive integrated moving average", "model autoregresiv integrat cu medie mobilă"),
    "ARX": ("autoregressive model with exogenous variables", "model autoregresiv cu variabile exogene"),
    "AUC": ("area under the ROC curve", "aria de sub curba ROC"),
    "AW": ("averaging across calibration windows", "medierea prognozelor obținute pe mai multe ferestre de calibrare"),
    "AW-ARX": ("ARX averaged across calibration windows", "ARX mediat pe ferestre de calibrare"),
    "AW-LEAR": ("LEAR averaged across calibration windows", "LEAR mediat pe ferestre de calibrare"),
    "CET": ("Central European Time", "ora Europei Centrale"),
    "CPU": ("central processing unit (processor core)", "unitatea centrală de procesare (nucleu de procesor)"),
    "DM": ("Diebold--Mariano test", "testul Diebold--Mariano"),
    "DNN": ("deep neural network", "rețea neuronală profundă"),
    "DST": ("daylight saving time", "ora de vară"),
    "ENTSO-E": ("European Network of Transmission System Operators for Electricity",
                "Rețeaua europeană a operatorilor de transport și de sistem pentru energie electrică"),
    "ETC": ("exchange-traded commodity", "titlu tranzacționat la bursă, garantat cu mărfuri (exchange-traded commodity)"),
    "EU": ("European Union", None),
    "UE": (None, "Uniunea Europeană"),
    "EUA": ("EU emission allowance (1 t CO$_2$)", "certificat de emisii al UE (1 t CO$_2$)"),
    "GBM": ("gradient boosting machine (boosted trees)", "gradient boosting (ansamblu de arbori de decizie construiți secvențial)"),
    "ISE": ("Fraunhofer Institute for Solar Energy Systems", "Institutul Fraunhofer pentru Sisteme de Energie Solară"),
    "LASSO": ("least absolute shrinkage and selection operator", "operatorul de contracție și selecție în normă absolută"),
    "LLM": ("large language model", "model mare de limbaj"),
    "LEAR": ("LASSO-estimated autoregression", "autoregresie estimată cu LASSO"),
    "MAD": ("median absolute deviation", "abaterea absolută mediană"),
    "MAE": ("mean absolute error", "eroarea absolută medie"),
    "ML": ("machine learning", "învățare automată"),
    "MLP": ("multilayer perceptron (feed-forward neural network)", "perceptron multistrat (rețea neuronală directă)"),
    "OPCOM": ("Romanian electricity and gas market operator", "operatorul pieței de energie electrică și de gaze naturale din România"),
    "PZU": ("Piața pentru Ziua Următoare (day-ahead market)", "piața pentru ziua următoare"),
    "RC": ("Reality Check (data-snooping test of White, 2000)", "testul Reality Check (testul de selecție abuzivă al lui White, 2000)"),
    "RES": ("renewable energy sources (here: wind + solar)", "surse regenerabile de energie (aici: eolian + solar)"),
    "ReLU": ("rectified linear unit", "unitate liniară rectificată (rectified linear unit)"),
    "RMSE": ("root mean squared error", "rădăcina erorii pătratice medii"),
    "RO": ("Romania (bidding zone)", "România (zonă de ofertare)"),
    "ROC": ("receiver operating characteristic", "caracteristica de operare a receptorului (receiver operating characteristic)"),
    "rMAE": ("relative MAE (model MAE / naive MAE)", "MAE relativă (MAE a modelului / MAE a modelului naiv)"),
    "SMAPE": ("symmetric mean absolute percentage error", "eroarea procentuală absolută medie simetrică"),
    "SPA": ("superior predictive ability (test of Hansen, 2005)", "abilitate predictivă superioară (testul lui Hansen, 2005)"),
    "FWER": ("familywise error rate", "rata erorii la nivelul familiei de ipoteze"),
    "SHAP": ("SHapley Additive exPlanations", "explicații aditive bazate pe valorile Shapley (SHapley Additive exPlanations)"),
    "TSO": ("transmission system operator", "operator de transport și de sistem"),
    "XGBoost": ("eXtreme Gradient Boosting (library)", "eXtreme Gradient Boosting (bibliotecă de programe)"),
    "EUR": ("euro", "euro"), "MW": ("megawatt", "megawatt"), "MWh": ("megawatt-hour", "megawatt-oră"),
    "GW": ("gigawatt", "gigawatt"),
}
UNITS = {"EUR", "MW", "MWh", "GW"}
# journal codes inside citations only; everything else must be in the Abbreviations list and spelled out
IGNORE = {"AI", "PatchTST", "TimesFM", "TS", "ReP", "AIDA", "TabPFN", "NBEATSx", "NBEAT", "JEF", "ESR", "EMQA", "IJF", "ENEECO", "APEN", "JASA", "TPWRS", "IEEE", "JBES", "PICBE", "RJEF", "IIF", "SPOT", "CO", "II",
          "XG", "JMLR", "ICLR", "KDD", "ACM", "SIGKDD", "TMLR", "NMI", "ECECSR", "MWR", "PRL", "CSDA", "ESL", "NIPS", "AM",
          "ECO", "ES", "VaR", "CEE", "SSRN", "IPE", "ASE", "TVOCCA", "VOFEIT"}


def build(lang, H=None):
    V = Numbers(os.path.join(HERE, "L7_numbers.json"), lang)
    N = V.N
    D = Deck(7, "Machine Learning for Energy Markets" if lang == "en" else "Învățarea automată pe piețele de energie", V, lang, heights=H)
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

    def pv(key):             # "$p$ = 0.016" or "$p<0.001$"
        p = float(V.get(key))
        if p < 0.001:
            return "$p<0{,}001$" if ro else "$p<0.001$"
        return "$p$ = " + fmt(p, ".3f", lang)

    def n(x, spec):          # a hand-typed definition number with the right decimal mark
        return fmt(x, spec, lang)

    def sci(x):              # 0.0003 -> $3\cdot10^{-4}$
        if x == 0:
            return "0"
        m_, e_ = f"{x:.0e}".split("e")
        return "$" + ("" if m_ == "1" else m_ + "\\cdot") + "10^{" + str(int(e_)) + "}$"

    TEST = t("test year @{design.test_start|date} -- @{design.test_end|date}", "anul de test @{design.test_start|date} -- @{design.test_end|date}")
    OWN = t("(own computation, " + TEST + ")", "(calcule proprii, " + TEST + ")")
    CITE_L = "(Lago, Marcjasz, De Schutter \\& Weron, 2021, APEN)"
    a = N["acc"]

    # ------------------------------------------------------------------ front matter
    D.parts.append("% END-FRONT-MATTER\n")
    D.frame(t("Learning objectives", "Obiectivele cursului"), it(
        t("Set up an honest machine learning (ML) experiment: training, validation and test samples in time order, and only the "
          "information known at 12:00 Central European Time (CET) on the day before delivery.",
          "Organizarea corectă a unui experiment de învățare automată (ML); eșantioanele de antrenare, de validare și de test se succed "
          "în timp; prognoza folosește numai informația cunoscută la ora 12:00 a Europei Centrale (CET) în ziua dinaintea livrării"),
        t("Build and tune a deep neural network (DNN) and gradient-boosted trees for the 24 day-ahead prices of Romania; try a "
          "pretrained foundation model.",
          "Construirea și calibrarea a două modele pentru cele 24 de prețuri orare ale zilei următoare; o rețea neuronală profundă (DNN); "
          "un ansamblu de arbori de decizie construiți secvențial (gradient boosting); în plus, un model fundațional preantrenat"),
        t("Compare them with the benchmarks of Lecture 2 on the same test year, with the mean absolute error (MAE), the root mean squared error (RMSE), "
          "the relative MAE (rMAE) and the Diebold--Mariano (DM) test; combine machine learning with the statistical models.",
          "Compararea cu modelele de referință din cursul 2, pe același an de test; eroarea absolută medie (MAE), rădăcina erorii pătratice medii (RMSE), "
          "MAE relativă (rMAE) și testul Diebold--Mariano (DM); combinarea modelelor de învățare automată cu modelele statistice"),
        t("Explain the forecasts, predict price spikes and negative prices, and recognise the pitfalls that make a model look better than it is.",
          "Explicarea prognozelor, anticiparea vîrfurilor de preț și a prețurilor negative; capcanele care fac un model să pară mai bun decît este"),
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

    D.frame(t("Same data, same test year as Lecture 2, plus a validation year", "Aceleași date și același an de test ca în cursul 2, plus un an de validare"), table(
        "@{}p{0.24\\textwidth}p{0.70\\textwidth}@{}",
        [t("Element", "Element"), t("Choice in this lecture", "Alegerea din acest curs")],
        [[t("Target", "Variabila prognozată"),
          t("hourly day-ahead price of Romania (RO), Piața pentru Ziua Următoare (PZU), run by the Romanian electricity and gas market operator (OPCOM)",
            "prețul orar de pe piața pentru ziua următoare (PZU) din România (RO), administrată de operatorul pieței de energie electrică și de gaze naturale (OPCOM)")],
         [t("Inputs (as in Lecture 2)", "Variabile explicative (ca în cursul 2)"),
          t("prices up to $d-1$; load, wind + solar, hydro, nuclear, net imports up to $d-2$, from the European Network of Transmission System Operators "
            "for Electricity (ENTSO-E); carbon: European Union (EU) emission allowance (EUA), via an exchange-traded commodity (ETC)",
            "prețurile pînă în ziua $d-1$; consumul, producția eoliană și solară, hidro, nucleară și importul net pînă în ziua $d-2$, de la Rețeaua europeană a operatorilor de transport "
            "și de sistem pentru energie electrică (ENTSO-E); prețul certificatelor de emisii (EUA) ale Uniunii Europene (UE), printr-un titlu tranzacționat la bursă (ETC)")],
         [t("Training", "Antrenare"), t("from @{design.train_start|date}; grows by one month at each refit", "de la @{design.train_start|date}; crește cu o lună la fiecare reestimare")],
         [t("Validation year", "Anul de validare"), t("@{design.val_start|date} -- @{design.val_end|date}: used only to choose the settings of the models",
                                                       "@{design.val_start|date} -- @{design.val_end|date}: folosit numai pentru alegerea setărilor modelelor")],
         [t("Test year", "Anul de test"), t("@{design.test_start|date} -- @{design.test_end|date}, @{test.n_hours|,d} hours, models refitted monthly",
                                             "@{design.test_start|date} -- @{design.test_end|date}, @{test.n_hours|,d} " + de("test.n_hours") + "ore, modele reestimate lunar")]],
        size="scriptsize", stretch="1.0") + "\n\\vspace{1mm}\n" + it(
        t("\\textbf{Data up to @{cutoff.end|date}}, downloaded @{cutoff.download|date} from energy-charts.info (Fraunhofer ISE) and Yahoo Finance.",
          "\\textbf{Date pînă la @{cutoff.end|date}}; descărcate la @{cutoff.download|date} de pe energy-charts.info (Fraunhofer ISE) și Yahoo Finance"),
        (t("\\textbf{Benchmarks}: the forecasts of Lecture 2, read from its files", "\\textbf{Modelele de referință}: prognozele din cursul 2, preluate din fișierele acestuia"),
         t("naive model; autoregressive model with exogenous variables (ARX); least absolute shrinkage and selection operator (LASSO)",
           "modelul naiv; modelul autoregresiv cu variabile exogene (ARX); operatorul de contracție și selecție în normă absolută (LASSO)"),
         t("LASSO-estimated autoregression (LEAR); ARX averaged across calibration windows (AW-ARX), LEAR likewise (AW-LEAR); ensemble of 4 models",
           "autoregresia estimată cu LASSO (LEAR); ARX mediat pe mai multe ferestre de calibrare (AW-ARX), LEAR la fel (AW-LEAR); ansamblul de 4 modele")),
        sep="1pt") + D.bottom(None, NB + " \\S1"), "footnotesize")

    # ------------------------------------------------------------------ 1 principles
    D.section(t("Machine learning, evaluated honestly", "Învățarea automată, evaluată corect"))
    D.concept(t("Machine learning buys flexibility and pays for it with variance", "Învățarea automată cîștigă flexibilitate, dar plătește prin varianță"),
              t("A flexible model can learn thresholds and interactions that LEAR misses, but it can also learn the noise of the training years.",
                "Un model flexibil poate învăța praguri și interacțiuni pe care LEAR nu le vede, dar poate învăța și zgomotul din anii de antrenare."),
              "\\[ \\hat\\theta=\\arg\\min_{\\theta}\\ \\underbrace{\\frac1n\\sum_{i=1}^{n}\\ell\\big(Y_i,f_\\theta(\\mathbf x_i)\\big)}_{\\text{" +
              t("fit to the training days", "potrivirea pe zilele de antrenare") + "}}+\\underbrace{\\lambda\\,\\Omega(\\theta)}_{\\text{" +
              t("penalty", "penalizare") + "}} \\]" +
              "\\where{" + t("$f_\\theta$ = the model with parameters $\\theta$; $\\mathbf x_i$ = inputs known at gate closure; $Y_i$ = price; "
                             "$\\ell$ = loss, here the absolute error; $\\Omega$ = complexity, $\\lambda$ = its weight.",
                             "$f_\\theta$ = modelul, cu parametrii $\\theta$; $\\mathbf x_i$ = variabilele cunoscute la închiderea licitației; $Y_i$ = prețul; "
                             "$\\ell$ = funcția de pierdere, aici eroarea absolută; $\\Omega$ = complexitatea modelului, iar $\\lambda$ = ponderea ei.") + "}",
              it((t("\\textbf{How flexible are our models?}", "\\textbf{Cît de flexibile sînt modelele noastre?}"),
                  t("LEAR: at most 247 coefficients per hour", "LEAR: cel mult 247 de coeficienți pentru fiecare oră"),
                  t("our DNN: @{search.dnn.n_params|,d} parameters, for @{design.n_train_days_last|,d} training days at the last refit",
                    "rețeaua DNN: @{search.dnn.n_params|,d} " + de("search.dnn.n_params") + "parametri, pentru @{design.n_train_days_last|,d} " + de("design.n_train_days_last") + "zile de antrenare la ultima reestimare")),
                 (t("\\textbf{Consequence}", "\\textbf{Consecința}"),
                  t("the training error says nothing about the future; only data the model has not seen can judge it",
                    "eroarea pe datele de antrenare nu spune nimic despre viitor; modelul poate fi judecat numai pe date pe care nu le-a văzut")), sep="3pt"),
              t("ask a vendor how many parameters the model has per day of history, and on which days its error was measured.",
                "întrebați furnizorul de prognoze cîți parametri are modelul pentru fiecare zi de istoric și pe ce zile a fost măsurată eroarea."),
              tryit=NB + " \\S1", cite="(Hastie, Tibshirani \\& Friedman, 2009; Lago et al., 2021, APEN)", wl="0.52", wr="0.45")

    D.chart(t("Three samples in time order: training, validation, test",
              "Trei eșantioane în ordine cronologică: antrenare, validare, test"), "split_ml", [
        (t("\\textbf{Validation year}: @{search.n_cfg} settings per model compared, refitted every 3 months",
           "\\textbf{Anul de validare}: se compară @{search.n_cfg} " + de("search.n_cfg") + "setări pentru fiecare model, reestimate la fiecare 3 luni"),
         t("the setting with the lowest MAE is frozen before the test year starts",
           "setarea cu cea mai mică MAE este fixată înainte de începutul anului de test")),
        (t("\\textbf{Test year}: models refitted at the start of each month on all earlier days",
           "\\textbf{Anul de test}: modelele sînt reestimate la începutul fiecărei luni, pe toate zilele anterioare"),
         t("never used to choose anything; the same year as in Lecture 2, so the errors are directly comparable",
           "nu se folosește pentru nicio alegere; este același an ca în cursul 2, deci erorile se pot compara direct"))],
        height="0.58\\textheight", job=t("treat the test year like a sealed envelope, opened once, after every choice is made.",
                                         "tratați anul de test ca pe un plic sigilat, deschis o singură dată, după toate alegerile."),
        tryit=NB + " \\S1", cite="(Bergmeir \\& Benítez, 2012, Inf.\\ Sci.; Lago et al., 2021, APEN)")

    D.concept(t("Hyperparameters are chosen by random search on the validation year", "Hiperparametrii se aleg prin căutare aleatoare pe anul de validare"),
              t("Settings such as the number of neurons or of trees are not estimated by the model; we try several and keep the one that forecasts best on unseen days.",
                "Setări precum numărul de neuroni sau de arbori nu sînt estimate de model; încercăm mai multe și o păstrăm pe cea care prognozează cel mai bine zilele nevăzute."),
              "\\[ \\gamma^{*}=\\arg\\min_{\\gamma\\in\\{\\gamma_0,\\dots,\\gamma_{24}\\}}\\ \\frac{1}{24\\,|\\mathcal V|}\\sum_{d\\in\\mathcal V}\\sum_{h=0}^{23}"
              "\\big|P_{d,h}-\\hat P_{d,h}(\\gamma)\\big| \\]" +
              "\\where{" + t("$\\gamma$ = one setting (vector of hyperparameters); $\\gamma_0$ = the setting of Lecture 2, the others drawn at random; "
                             "$\\mathcal V$ = days of the validation year; $\\hat P_{d,h}(\\gamma)$ = forecast with setting $\\gamma$.",
                             "$\\gamma$ = o setare (vectorul hiperparametrilor); $\\gamma_0$ = setarea din cursul 2, celelalte extrase aleator; "
                             "$\\mathcal V$ = zilele anului de validare; $\\hat P_{d,h}(\\gamma)$ = prognoza cu setarea $\\gamma$.") + "}",
              it((t("\\textbf{Why random, not a full grid}", "\\textbf{De ce aleator și nu pe o grilă completă}"),
                  t("only a few settings matter; random draws cover each of them better with the same budget",
                    "doar cîteva setări contează cu adevărat; extragerile aleatoare le acoperă mai bine, cu același număr de încercări")),
                 (t("\\textbf{Our budget}", "\\textbf{Bugetul nostru}"),
                  t("@{search.n_random} random settings + the Lecture 2 setting, for each of the two models",
                    "@{search.n_random} de setări aleatoare și setarea din cursul 2, pentru fiecare dintre cele două modele"),
                  t("@{cost.search|.1f} minutes on one core of the central processing unit (CPU)",
                    "@{cost.search|.1f} minute pe un nucleu al unității centrale de procesare (CPU)")), sep="3pt"),
              t("a modest, documented search is enough; a search without a separate validation sample is not a search but a leak.",
                "o căutare modestă, dar documentată, este suficientă; o căutare fără un eșantion de validare separat nu este o căutare, ci o scurgere de informație."),
              tryit=NB + " \\S2", cite="(Bergstra \\& Bengio, 2012, JMLR)", wl="0.55", wr="0.42")

    # ------------------------------------------------------------------ 2 neural networks
    D.section(t("Deep neural networks", "Rețele neuronale profunde"))
    D.concept(t("A neural network stacks regressions, each followed by a bend", "O rețea neuronală înlănțuie regresii, fiecare urmată de o funcție neliniară"),
              t("Each neuron bends a linear combination of the inputs; the output layer gives the 24 prices of day $d$ at once.",
                "Fiecare neuron transformă neliniar o combinație liniară a intrărilor; stratul de ieșire dă deodată cele 24 de prețuri ale zilei $d$."),
              "\\[ \\mathbf z=\\phi\\big(W_1\\mathbf x_d+\\mathbf b_1\\big),\\qquad \\hat{\\mathbf Y}_d=W_2\\,\\mathbf z+\\mathbf b_2\\in\\mathbb R^{24} \\]"
              "\\[ \\phi(u)=\\max(0,u)\\quad\\text{" + t("or", "sau") + "}\\quad \\phi(u)=\\ln(1+e^{u}) \\]" +
              "\\where{" + t("$\\mathbf x_d$ = inputs of day $d$ (prices, load, wind + solar, fundamentals, weekday); $W_1,W_2$ = weights, $\\mathbf b_1,\\mathbf b_2$ = intercepts; "
                             "$\\phi$ = rectified linear unit (ReLU) or its smooth version (softplus); $\\hat{\\mathbf Y}_d$ = asinh-scaled prices, as in Lecture 2.",
                             "$\\mathbf x_d$ = intrările zilei $d$ (prețuri, consum, eolian și solar, variabile fundamentale, ziua săptămînii); $W_1,W_2$ = ponderi, "
                             "$\\mathbf b_1,\\mathbf b_2$ = termeni liberi; $\\phi$ = unitatea liniară rectificată (ReLU) sau varianta netedă (softplus); "
                             "$\\hat{\\mathbf Y}_d$ = prețurile transformate cu asinh (cursul 2).") + "}",
              it((t("\\textbf{Our network} (chosen on the validation year)", "\\textbf{Rețeaua noastră} (aleasă pe anul de validare)"),
                  t("@{search.dnn.n_inputs} inputs, one hidden layer of @{search.dnn.cfg.n1} neurons, softplus, 24 outputs",
                    "@{search.dnn.n_inputs} de intrări, un strat ascuns de @{search.dnn.cfg.n1} de neuroni, funcția softplus, 24 de ieșiri"),
                  t("@{search.dnn.n_params|,d} parameters; two-layer networks did worse on validation",
                    "@{search.dnn.n_params|,d} " + de("search.dnn.n_params") + "parametri; rețelele cu două straturi au fost mai slabe la validare")),
                 (t("\\textbf{Better than in Lecture 2}", "\\textbf{Mai bună decît în cursul 2}"),
                  t("the multilayer perceptron (MLP) of Lecture 2 had MAE @{l2.mlp|.2f}; ours has @{acc.dnn.mae|.2f} EUR/MWh",
                    "perceptronul multistrat (MLP): MAE @{l2.mlp|.2f}; rețeaua de acum: @{acc.dnn.mae|.2f} EUR/MWh")), sep="2pt"),
              t("a network is a regression with many more coefficients: it needs the same data discipline, not less.",
                "o rețea neuronală este o regresie cu mult mai mulți coeficienți: are nevoie de aceeași disciplină a datelor, nu de mai puțină."),
              tryit=NB + " \\S2", cite=CITE_L, wl="0.56", wr="0.41")

    D.concept(t("Training: small steps against the error, stopped in time", "Antrenarea: pași mici împotriva erorii, opriți la timp"),
              t("The weights move a little in the direction that lowers the error on a random batch of days; we stop when the error on later days stops falling.",
                "Ponderile se modifică puțin, în direcția care reduce eroarea pe un grup aleator de zile; ne oprim cînd eroarea pe zilele mai recente nu mai scade."),
              "\\[ \\mathcal L(\\theta)=\\frac{1}{24\\,|B|}\\sum_{d\\in B}\\sum_{h=0}^{23}\\big|Y_{d,h}-\\hat Y_{d,h}(\\theta)\\big| \\]"
              "\\[ \\theta\\leftarrow\\theta-\\eta\\,\\widehat{\\nabla\\mathcal L} \\]" +
              "\\where{" + t("$B$ = a mini-batch of @{search.dnn.cfg.batch} days; $\\eta$ = learning rate (" + sci(N['search']['dnn']['cfg']['lr']) + "); $\\widehat{\\nabla\\mathcal L}$ = gradient rescaled by the Adam method; "
                             "one epoch = one pass over all training days.",
                             "$B$ = un grup de @{search.dnn.cfg.batch} " + de("search.dnn.cfg.batch") + "zile (mini-batch); $\\eta$ = rata de învățare (" + sci(N['search']['dnn']['cfg']['lr']) + "); "
                             "$\\widehat{\\nabla\\mathcal L}$ = gradientul, rescalat prin metoda Adam; o epocă = o parcurgere a tuturor zilelor de antrenare.") + "}",
              it((t("\\textbf{Early stopping}", "\\textbf{Oprirea timpurie (early stopping)}"),
                  t("train on the first 85\\% of the training days, watch the error on the last 15\\%", "antrenare pe primele 85\\% din zile, urmărirea erorii pe ultimele 15\\%"),
                  t("keep the best epoch, then refit on all days for that many epochs", "se păstrează epoca cea mai bună, apoi rețeaua se reestimează pe toate zilele, cu același număr de epoci")),
                 (t("\\textbf{On our data}", "\\textbf{Pe datele noastre}"),
                  t("epochs kept: median @{search.dnn.epochs_med}, from @{search.dnn.epochs_min} to @{search.dnn.epochs_max} (12 refits $\\times$ 4 seeds)",
                    "epocile păstrate: mediana @{search.dnn.epochs_med}, între @{search.dnn.epochs_min} și @{search.dnn.epochs_max} (12 reestimări $\\times$ 4 inițializări)"),
                  t("dropout: during training each neuron is switched off at random with probability @{search.dnn.cfg.drop|.1f}",
                    "dropout: în timpul antrenării, fiecare neuron este dezactivat aleator, cu probabilitatea @{search.dnn.cfg.drop|.1f}")), sep="3pt"),
              t("the stopping rule uses only past days: it is part of the model, so it is checked like the rest.",
                "regula de oprire folosește numai zile din trecut: face parte din model și se verifică la fel ca restul."),
              tryit=NB + " \\S2", cite="(Kingma \\& Ba, 2015, ICLR; Srivastava et al., 2014, JMLR)", wl="0.52", wr="0.45")

    D.chart(t("Early stopping: stop when the error on recent days stops falling", "Oprirea timpurie: ne oprim cînd eroarea pe zilele recente nu mai scade"),
            "learning_curve", [
                (t("Refit for @{curve.month|ym}: the error on the last 15\\% of days is lowest at epoch @{curve.best_ep}",
                   "Reestimarea pentru @{curve.month|ym}: eroarea pe ultimele 15\\% din zile este minimă la epoca @{curve.best_ep}"),
                 t("@{curve.v_best|.2f} EUR/MWh; training stops at epoch @{curve.n_ep}",
                   "@{curve.v_best|.2f} EUR/MWh; antrenarea se oprește la epoca @{curve.n_ep}")),
                t("After that point the network fits the past better and the recent days worse: it starts to memorise.",
                  "După acest punct, rețeaua reproduce mai bine trecutul, dar mai slab zilele recente: începe să memoreze")],
            height="0.58\\textheight", job=t("ask the vendor for this curve: without it, the network may simply have memorised the past.",
                                             "cereți furnizorului această curbă: fără ea, rețeaua poate să fi memorat trecutul."),
            tryit=NB + " \\S2", cite=t("(own computation; chosen DNN, seed 1)", "(calcule proprii; rețeaua DNN aleasă, inițializarea 1)"))

    D.chart(t("Random search cuts the validation error of both models", "Căutarea aleatoare reduce eroarea de validare a ambelor modele"),
            "search", [
                (t("\\textbf{DNN}: best setting @{search.dnn.val_best|.2f} EUR/MWh; Lecture 2 setting @{search.dnn.val_l2|.2f}, rank @{search.dnn.rank_l2} of @{search.n_cfg}",
                   "\\textbf{DNN}: cea mai bună setare are MAE @{search.dnn.val_best|.2f} EUR/MWh; setarea din cursul 2, @{search.dnn.val_l2|.2f}, locul @{search.dnn.rank_l2} din @{search.n_cfg}"),
                 t("\\textbf{eXtreme Gradient Boosting (XGBoost)}: @{search.xgb.val_best|.2f} against @{search.xgb.val_l2|.2f} (rank @{search.xgb.rank_l2})",
                   "\\textbf{eXtreme Gradient Boosting (XGBoost)}: @{search.xgb.val_best|.2f} față de @{search.xgb.val_l2|.2f} (locul @{search.xgb.rank_l2})")),
                t("All @{search.n_cfg} settings of both models beat the naive model on the validation year (@{search.naive_val|.2f} EUR/MWh).",
                  "Toate cele @{search.n_cfg} " + de("search.n_cfg") + "setări, la ambele modele, sînt mai precise decît modelul naiv (@{search.naive_val|.2f} EUR/MWh)")],
            height="0.58\\textheight", job=t("budget one validation year for tuning any machine-learning model.",
                                             "prevedeți un an de validare pentru calibrarea oricărui model de învățare automată."),
            tryit=NB + " \\S2", cite=t("(own computation; validation year @{design.val_start|date} -- @{design.val_end|date})",
                                       "(calcule proprii; anul de validare @{design.val_start|date} -- @{design.val_end|date})"))

    # ------------------------------------------------------------------ 3 trees and foundation models
    D.section(t("Gradient boosting and foundation models", "Gradient boosting și modele fundaționale"))
    D.concept(t("A regression tree cuts the inputs into boxes and predicts one price per box", "Un arbore de regresie împarte intrările în căsuțe, cu cîte un preț fiecare"),
              t("A tree asks yes/no questions; each final leaf holds one value, so thresholds and interactions come for free.",
                "Un arbore pune întrebări cu răspuns da/nu; fiecare frunză finală conține o valoare, deci pragurile și interacțiunile apar de la sine."),
              "\\[ f(\\mathbf x)=\\textstyle\\sum_{j=1}^{J}w_j\\,\\mathbb 1\\{\\mathbf x\\in R_j\\} \\]\\vspace{-1mm}"
              "\\[ \\text{Gain}=\\frac{G_L^2}{H_L+\\lambda}+\\frac{G_R^2}{H_R+\\lambda}-\\frac{(G_L+G_R)^2}{H_L+H_R+\\lambda}-\\gamma \\]" +
              "\\where{" + t("$R_j$ = leaf $j$, $w_j$ = its value; $G$, $H$ = sums of the 1st and 2nd derivatives of the loss, left ($L$) and right ($R$); "
                             "$\\lambda$, $\\gamma$ = penalties; the split with the largest gain is kept.",
                             "$R_j$ = frunza $j$, $w_j$ = valoarea ei; $G$, $H$ = sumele derivatelor de ordinul 1 și 2 ale pierderii, la stînga ($L$) și la dreapta ($R$); "
                             "$\\lambda$, $\\gamma$ = penalizări; se alege împărțirea cu cel mai mare cîștig.") + "}",
              it((t("\\textbf{On our data} (refit for @{tree.month|ym})", "\\textbf{Pe datele noastre} (reestimarea pentru @{tree.month|ym})"),
                  t("first question of the first tree: price of $d-1$, same hour, below @{tree.split|.1f} EUR/MWh?",
                    "primul arbore întreabă: prețul din $d-1$, aceeași oră, este sub @{tree.split|.1f} EUR/MWh?"),
                  t("@{tree.n_leaves_t0} leaves; the model adds up @{tree.n_trees|,d} such trees",
                    "@{tree.n_leaves_t0} " + de("tree.n_leaves_t0") + "frunze; modelul adună @{tree.n_trees|,d} " + de("tree.n_trees") + "arbori")), sep="2pt"),
              t("a tree speaks the language of a trading desk: above a level yesterday, a premium tonight.",
                "un arbore gîndește ca un trader: dacă ieri prețul a trecut de un prag, diseară urmează o primă."),
              tryit=NB + " \\S3", cite="(Chen \\& Guestrin, 2016, KDD; Hastie et al., 2009)", wl="0.60", wr="0.37")

    D.concept(t("Gradient boosting: each new tree corrects the remaining errors", "Gradient boosting: fiecare arbore nou corectează erorile rămase"),
              t("Fit a small tree to what is still wrong, add it with a small weight, repeat a thousand times.",
                "Potrivim un arbore mic pe ceea ce este încă greșit, îl adăugăm cu o pondere mică și repetăm de o mie de ori."),
              "\\[ F_m(\\mathbf x)=F_{m-1}(\\mathbf x)+\\eta\\,f_m(\\mathbf x),\\qquad w_j^{*}=-\\frac{G_j}{H_j+\\lambda} \\]"
              "\\[ \\min\\ \\textstyle\\sum_{i}\\ell\\big(Y_i,F_M(\\mathbf x_i)\\big)+\\sum_{m}\\big(\\gamma J_m+\\tfrac{\\lambda}{2}\\sum_j w_{mj}^2\\big) \\]" +
              "\\where{" + t("$F_m$ = forecast after $m$ trees; $f_m$ = tree $m$, with $J_m$ leaves; $\\eta$ = learning rate; $w_j^{*}$ = optimal value of leaf $j$ (Appendix B); $\\ell$ = absolute error.",
                             "$F_m$ = prognoza după $m$ arbori; $f_m$ = arborele $m$, cu $J_m$ frunze; $\\eta$ = rata de învățare; $w_j^{*}$ = valoarea optimă a frunzei $j$ (anexa B); $\\ell$ = eroarea absolută.") + "}",
              it((t("\\textbf{Chosen on the validation year}", "\\textbf{Setarea aleasă pe anul de validare}"),
                  t("@{search.xgb.cfg.n_est|,d} trees of depth @{search.xgb.cfg.depth}, $\\eta$ = @{search.xgb.cfg.eta|.2f}, each tree on a fraction @{search.xgb.cfg.sub|.1f} of the rows",
                    "@{search.xgb.cfg.n_est|,d} " + de("search.xgb.cfg.n_est") + "arbori de adîncime @{search.xgb.cfg.depth}, $\\eta$ = @{search.xgb.cfg.eta|.2f}, fiecare pe o fracțiune @{search.xgb.cfg.sub|.1f} din rînduri")),
                 (t("\\textbf{Test year}", "\\textbf{Anul de test}"),
                  t("MAE @{acc.xgb.mae|.2f} EUR/MWh; untuned gradient boosting machine (GBM) of Lecture 2: @{l2.gbm|.2f} (DM " + pv("dm.gbm2__xgb.p") + ")",
                    "MAE @{acc.xgb.mae|.2f} EUR/MWh; modelul gradient boosting (GBM) necalibrat din cursul 2: @{l2.gbm|.2f} (DM: " + pv("dm.gbm2__xgb.p") + ")"),
                  t("AW-LEAR (@{acc.aw_lear.mae|.2f}) is still more accurate (DM " + pv("dm.xgb__aw_lear.p") + ")",
                    "AW-LEAR (@{acc.aw_lear.mae|.2f}) rămîne mai precis (DM: " + pv("dm.xgb__aw_lear.p") + ")")), sep="2pt"),
              t("tuning matters more than the software: the same kind of trees gained almost one euro per MWh from good settings.",
                "calibrarea contează mai mult decît programul: același tip de arbori a cîștigat aproape un euro pe MWh prin setări bune."),
              tryit=NB + " \\S3", cite="(Friedman, 2001, Ann.\\ Stat.; Chen \\& Guestrin, 2016, KDD)", wl="0.57", wr="0.40")

    D.concept(t("Foundation models forecast Romanian prices with no training at all", "Modelele fundaționale prognozează prețurile fără nicio antrenare"),
              t("Chronos models were trained by Amazon on large collections of time series; we give them only the recent prices and ask for the next 24 hours (zero-shot).",
                "Modelele Chronos au fost antrenate de Amazon pe colecții mari de serii de timp; noi le dăm doar prețurile recente și le cerem următoarele 24 de ore (fără reantrenare, zero-shot)."),
              "\\[ \\big(\\hat q^{\\tau}_{d,h}\\big)_{h=0,\\dots,23}^{\\tau=0.1,\\,0.5,\\,0.9}=g\\big(P_{t-2047},\\dots,P_{t}\\big) \\]".replace("0.1,\\,0.5,\\,0.9", "0{,}1;\\,0{,}5;\\,0{,}9" if ro else "0.1,\\,0.5,\\,0.9") +
              "\\where{" + t("$P_{t-2047},\\dots,P_t$ = the last 2048 hourly prices, up to the end of $d-1$ (@{found.ctx_days} days); $g$ = the pretrained network, used as it is; "
                             "$\\hat q^{\\tau}$ = forecast quantiles; the point forecast is the median $\\hat q^{0.5}$.",
                             "$P_{t-2047},\\dots,P_t$ = ultimele 2048 de prețuri orare, pînă la sfîrșitul zilei $d-1$ (@{found.ctx_days} de zile); $g$ = rețeaua preantrenată, folosită ca atare; "
                             "$\\hat q^{\\tau}$ = cuantilele prognozate; prognoza punctuală este mediana $\\hat q^{0{,}5}$.") + "}",
              it((t("\\textbf{Test year}, prices only, no fundamentals", "\\textbf{Anul de test}, numai cu prețuri, fără variabile fundamentale"),
                  t("Chronos-2: MAE @{acc.chr2.mae|.2f}; Chronos-Bolt: @{acc.bolt.mae|.2f}; AW-LEAR: @{acc.aw_lear.mae|.2f} EUR/MWh",
                    "Chronos-2: MAE @{acc.chr2.mae|.2f}; Chronos-Bolt: @{acc.bolt.mae|.2f}; AW-LEAR: @{acc.aw_lear.mae|.2f} EUR/MWh"),
                  t("Chronos-2 more accurate than AW-LEAR: DM " + pv("dm.aw_lear__chr2.p") + "; in all @{found.chr2_beats_lear_h} hours",
                    "Chronos-2 este mai precis decît AW-LEAR: DM, " + pv("dm.aw_lear__chr2.p") + "; în toate cele @{found.chr2_beats_lear_h} de ore")),
                 (t("\\textbf{Robustness}", "\\textbf{Robustețe}"),
                  t("validation year: Chronos-2 @{found.val_chr2|.2f}, best tuned DNN @{search.dnn.val_best|.2f}",
                    "în anul de validare: Chronos-2 @{found.val_chr2|.2f}, cea mai bună rețea DNN calibrată @{search.dnn.val_best|.2f}"),
                  t("published in Oct 2025, before the test year", "publicat în octombrie 2025, înaintea anului de test")), sep="2pt"),
              t("test a foundation model before building your own network: it is cheap, and here it was the most accurate single model.",
                "testați un model fundațional înainte de a construi propria rețea: costă puțin, iar aici a fost cel mai precis model individual."),
              tryit=NB + " \\S4", cite="(Ansari et al., 2024, TMLR; Ansari et al., 2025, arXiv)", wl="0.52", wr="0.45")

    D.chart(t("Chronos-2 beats AW-LEAR in every hour of the day",
              "Chronos-2 este mai precis decît AW-LEAR în fiecare oră a zilei"), "foundation_hour", [
        t("Chronos-Bolt, smaller and older, is level with AW-LEAR (DM " + pv("dm.aw_lear__bolt.p") + ").",
          "Chronos-Bolt, mai mic și mai vechi, este la egalitate cu AW-LEAR (DM: " + pv("dm.aw_lear__bolt.p") + ")"),
        t("The 10\\%--90\\% band of Chronos-2 holds @{found.cov80|.1f}\\% of the prices, not 80\\%: too narrow.",
          "Intervalul 10\\%--90\\% al modelului Chronos-2 conține @{found.cov80|.1f}\\% din prețuri, nu 80\\%: este prea îngust")],
        height="0.58\\textheight", job=t("use the median; recalibrate the bands (Lecture 2) before sizing risk with them.",
                                         "folosiți mediana; recalibrați intervalele (cursul 2) înainte de a dimensiona riscul cu ele."),
        tryit=NB + " \\S4", cite=OWN)


    # ------------------------------------------------------------------ AIDA 2026: what the field found (Weron keynote)
    WER = "https://github.com/danpele/EMQA/blob/main/resources/aida2026/weron_ml_electricity_price_forecasting.pdf"
    KUA = "https://github.com/danpele/EMQA/blob/main/resources/aida2026/kuan_multiple_inequality_testing.pdf"
    CLO = "https://github.com/danpele/EMQA/blob/main/resources/aida2026/clodnitchi_ai_energy_finance_review.pdf"
    # (no subsection: the section outline of this lecture has no room for an extra line)
    D.frame(t("AIDA 2026 keynote: deep networks beat LEAR, zero-shot models compete",
              "AIDA 2026: DNN întrece LEAR, modelele preantrenate concurează"), cols(
        it((t("\\textbf{R.\\ Weron, keynote} (4 June 2026, \\href{" + WER + "}{slides})",
              "\\textbf{R.\\ Weron, conferință invitată} (4 iunie 2026, \\href{" + WER + "}{diapozitive})"),
            t("model evolution: ARX, averaging across windows, LEAR, deep and interpretable networks",
              "evoluția modelelor: ARX, medierea pe ferestre, LEAR, rețele profunde și interpretabile"),
            t("pretrained zero-shot models against LEAR and distributional DNN models, test 2021--2025",
              "modele preantrenate, fără reantrenare (zero-shot), față de LEAR și de rețele DNN distribuționale, test 2021--2025")),
           (t("\\textbf{Deep and interpretable networks}", "\\textbf{Rețele profunde și interpretabile}"),
            t("open epftoolbox benchmark: the DNN had a lower rMAE than LEAR in all five markets (Lago et al., 2021)",
              "evaluarea deschisă epftoolbox: rețeaua DNN are rMAE mai mică decît LEAR pe toate cele cinci piețe (Lago et al., 2021)"),
            t("NBEATSx: trend, seasonality and exogenous blocks make the network readable (Olivares et al., 2023)",
              "NBEATSx: blocurile de trend, sezonalitate și variabile exogene fac rețeaua interpretabilă (Olivares et al., 2023)")), sep="3pt"),
        it((t("\\textbf{Zero-shot results} (RMSE, as printed)", "\\textbf{Rezultate zero-shot} (RMSE, conform diapozitivelor)"),
            t("2022: LEAR + conformal prediction " + n(45.71, ".2f") + ", Chronos 2 " + n(41.07, ".2f") + ", TabPFN 3.0 ts " + n(34.39, ".2f"),
              "2022: LEAR + predicție conformală " + n(45.71, ".2f") + ", Chronos 2 " + n(41.07, ".2f") + ", TabPFN 3.0 ts " + n(34.39, ".2f")),
            t("2025: " + n(20.38, ".2f") + ", " + n(20.58, ".2f") + ", " + n(17.66, ".2f") + "; a TabPFN version was the best in every year",
              "2025: " + n(20.38, ".2f") + ", " + n(20.58, ".2f") + " și " + n(17.66, ".2f") + "; o versiune TabPFN a fost cea mai bună în fiecare an")),
           (t("\\textbf{Link with our test year}", "\\textbf{Legătura cu anul nostru de test}"),
            t("Chronos-2, zero-shot, is our most accurate single model (MAE @{acc.chr2.mae|.2f} vs @{acc.aw_lear.mae|.2f} for AW-LEAR)",
              "Chronos-2, fără reantrenare, este cel mai precis model individual (MAE @{acc.chr2.mae|.2f}, față de @{acc.aw_lear.mae|.2f} la AW-LEAR)"),
            t("rankings move: TabPFN 2.0 had RMSE " + n(68.85, ".2f") + " in 2022, " + n(17.52, ".2f") + " in 2025",
              "clasamentele se schimbă: TabPFN 2.0 a avut RMSE " + n(68.85, ".2f") + " în 2022 și " + n(17.52, ".2f") + " în 2025")), sep="3pt"),
        "0.50", "0.47") +
        D.bottom(t("keep LEAR as the benchmark and test zero-shot models next to it, over several years.",
                   "păstrați LEAR ca reper și testați modelele zero-shot alături de el, pe mai mulți ani.")),
        "footnotesize", cite=t("(AIDA 2026 slides, Bucharest; papers: ", "(diapozitivele AIDA 2026, București; lucrări: ") +
        "\\href{https://doi.org/10.1016/j.apenergy.2021.116983}{Lago et al., 2021, APEN}; "
        "\\href{https://doi.org/10.1016/j.ijforecast.2022.03.001}{Olivares et al., 2023, IJF})")

    # ------------------------------------------------------------------ AIDA 2026: four generations of forecasting methods (Andrei et al.)
    AND = "https://github.com/danpele/EMQA/blob/main/resources/aida2026/andrei_ai4efin_benchmarking.pdf"
    D.frame(t("AIDA 2026: four generations of models on 27 European price series",
              "AIDA 2026: patru generații de modele pe 27 de serii europene de prețuri"), cols(
        it((t("\\textbf{A.-V.\\ Andrei et al., talk} (3 June 2026, \\href{" + AND + "}{slides})",
              "\\textbf{A.-V.\\ Andrei et al., prezentare} (3 iunie 2026, \\href{" + AND + "}{diapozitive})"),
            t("11 models, four generations: econometric, e.g.\\ autoregressive integrated moving average (ARIMA); deep learning; transformers; "
              "pretrained large language models (LLM): Chronos, TimesFM",
              "11 modele, patru generații: econometrie, de ex.\\ modelul autoregresiv integrat cu medie mobilă (ARIMA); învățare profundă; "
              "transformere; modele mari de limbaj (LLM) preantrenate: Chronos, TimesFM"),
            ),
           (t("\\textbf{Data and walk-forward validation}", "\\textbf{Date și validare walk-forward}"),
            t("wholesale prices of 27 European Union (EU) countries, Ember (from ENTSO-E)",
              "prețuri angro din 27 de țări ale Uniunii Europene (UE), Ember (ENTSO-E)"),
            t("96 steps in, 96 out; training 2000 hours (83 days), test 500 hours (20 days)",
              "96 de pași la intrare și 96 la ieșire; antrenare 2000 de ore (83 de zile), test 500 de ore (20 de zile)"),
            t("symmetric mean absolute percentage error (SMAPE); score (100 $\\times$ SMAPE + RMSE)/2",
              "eroarea procentuală absolută medie simetrică (SMAPE); scor (100 $\\times$ SMAPE + RMSE)/2")), sep="3pt"),
        it((t("\\textbf{Results} (rank among the 11 models)", "\\textbf{Rezultate} (locul între cele 11 modele)"),
            t("PatchTST (a transformer) is first or second in all 27 countries",
              "PatchTST (un transformer) este pe primul sau al doilea loc în toate cele 27 de țări"),
            t("Romania: PatchTST 1, TimesFM 2, Chronos 8, ARIMA 9",
              "România: PatchTST 1, TimesFM 2, Chronos 8, ARIMA 9"),
            t("Germany: PatchTST 1, TimesFM 5, Chronos 10",
              "Germania: PatchTST 1, TimesFM 5, Chronos 10"),
            t("gains are model-specific, not uniform across the 4th generation",
              "cîștigurile depind de model, nu sînt uniforme în generația a patra")),
           (t("\\textbf{Link with this lecture}", "\\textbf{Legătura cu acest curs}"),
            t("on Romanian prices, Chronos-2 (2025) is our best single model (MAE @{acc.chr2.mae|.2f})",
              "pe prețurile din România, Chronos-2 (2025) este cel mai bun model individual (MAE @{acc.chr2.mae|.2f})")), sep="3pt"),
        "0.52", "0.45") +
        D.bottom(t("compare model generations with walk-forward validation on several markets before choosing one.",
                   "comparați generațiile de modele prin validare walk-forward, pe mai multe piețe, înainte de a alege.")),
        "footnotesize", cite=t("(AIDA 2026 slides, Bucharest; paper: ", "(diapozitivele AIDA 2026, București; lucrare: ") +
        "\\href{https://arxiv.org/abs/2411.03372}{Andrei et al., 2024, arXiv})")

    # ------------------------------------------------------------------ 4 comparison, combination, cost
    D.section(t("Honest comparison, combination and cost", "Comparație corectă, combinare și cost"))
    RES = [("naive", t("Naive", "Naiv")), ("aw_arx", "AW-ARX"), ("aw_lear", "AW-LEAR"), ("ens4", t("Ensemble of 4 (Lecture 2)", "Ansamblul de 4 (cursul 2)")),
           ("gbm2", t("GBM (Lecture 2)", "GBM (cursul 2)")), ("mlp2", t("MLP (Lecture 2)", "MLP (cursul 2)")),
           ("xgb", t("XGBoost, tuned", "XGBoost, calibrat")), ("dnn", t("DNN, tuned", "DNN, calibrată")),
           ("bolt", t("Chronos-Bolt, zero-shot", "Chronos-Bolt, fără antrenare")), ("chr2", t("Chronos-2, zero-shot", "Chronos-2, fără antrenare")),
           ("ens_ldx", "AW-LEAR + DNN + XGBoost"), ("ens_t4", "AW-ARX + AW-LEAR + DNN + XGBoost"),
           ("ens_lc", "AW-LEAR + Chronos-2"), ("ens_t5", t("Ensemble of 5 (with Chronos-2)", "Ansamblul de 5 (cu Chronos-2)"))]
    vals = {c: [a[k][c] for k, _ in RES] for c in ["mae", "rmse", "rmae", "vs_lear"]}
    rows = []
    for k, lab in RES:
        dmk = f"aw_lear__{k}"
        dmp = pval(f"dm.{dmk}.p") if dmk in N["dm"] else "--"
        rows.append([lab] + [heat(a[k][c], min(vals[c]), max(vals[c]), c != "vs_lear", fmt(a[k][c], f, lang))
                             for c, f in [("mae", ".2f"), ("rmse", ".2f"), ("rmae", ".3f"), ("vs_lear", "+.1f")]] + [dmp])
    D.frame(t("Scoreboard: Chronos-2 is the best single model",
              "Clasamentul: Chronos-2 este cel mai bun model individual"),
            "\\begin{center}" + table("@{}lrrrrr@{}", [t("Model", "Model"), "MAE", "RMSE", "rMAE", t("vs AW-LEAR, \\%", "față de AW-LEAR, \\%"),
                                                     t("DM $p$", "DM, $p$")], rows, size="scriptsize", stretch="0.96") + "\\end{center}\\vspace{-2mm}" + note(
                t("Root mean squared error (RMSE); relative MAE (rMAE) = MAE / MAE of the naive model; green = better, per column.",
                  "Rădăcina erorii pătratice medii (RMSE); MAE relativă (rMAE) = MAE / MAE a modelului naiv; verde = mai precis, pe fiecare coloană."),
                t("DM $p$: one-sided test that the model is more accurate than AW-LEAR (daily mean absolute error, Newey--West variance, as in Lecture 2).",
                  "DM, $p$: test unilateral că modelul este mai precis decît AW-LEAR (eroarea absolută medie zilnică, varianță Newey--West, ca în cursul 2).")) +
            D.bottom(None, NB + " \\S5"), "small", cite=OWN)

    D.chart(t("DM tests: combinations with ML beat AW-LEAR significantly",
              "Testele DM: combinațiile cu ML depășesc semnificativ AW-LEAR"), "dm_matrix", [
        t("AW-LEAR + DNN + XGBoost beats AW-LEAR (" + pv("dm.aw_lear__ens_ldx.p") + "); adding AW-ARX gives MAE @{acc.ens_t4.mae|.2f}, better than the Lecture 2 ensemble (" + pv("dm.ens4__ens_t4.p") + ").",
          "AW-LEAR + DNN + XGBoost este mai precis decît AW-LEAR (" + pv("dm.aw_lear__ens_ldx.p") + "); cu AW-ARX adăugat, MAE scade la @{acc.ens_t4.mae|.2f}, sub ansamblul din cursul 2 (" + pv("dm.ens4__ens_t4.p") + ")"),
        t("Adding AW-LEAR to Chronos-2 changes nothing (" + pv("dm.chr2__ens_lc.p") + "): on the hard days the two models make similar errors.",
          "Adăugarea AW-LEAR la Chronos-2 nu schimbă nimic (" + pv("dm.chr2__ens_lc.p") + "): în zilele dificile, cele două modele greșesc asemănător")],
        height="0.58\\textheight", tryit=NB + " \\S5", cite=t("(own computation; one-sided DM tests)", "(calcule proprii; teste DM unilaterale)"))

    D.chart(t("Averaging works because the errors are not identical", "Media funcționează pentru că erorile nu sînt identice"), "combo_weight", [
        t("$\\Var\\big(\\tfrac{e_1+e_2}{2}\\big)=\\tfrac14(\\sigma_1^2+\\sigma_2^2+2\\rho\\sigma_1\\sigma_2)$: with correlation $\\rho<1$, the average errs less ($e$ = error, $\\sigma$ = its standard deviation).",
          "$\\Var\\big(\\tfrac{e_1+e_2}{2}\\big)=\\tfrac14(\\sigma_1^2+\\sigma_2^2+2\\rho\\sigma_1\\sigma_2)$: dacă $\\rho<1$, media greșește mai puțin ($e$ = eroarea, $\\sigma$ = abaterea ei standard, $\\rho$ = corelația)"),
        t("Error correlation with AW-LEAR: @{combo.corr.dnn|.2f} (DNN), @{combo.corr.xgb|.2f} (XGBoost); equal weights do almost as well as the best weight seen afterwards (@{combo.w_best_xgb|.2f}).",
          "Corelația erorilor cu AW-LEAR: @{combo.corr.dnn|.2f} (DNN), @{combo.corr.xgb|.2f} (XGBoost); ponderile egale sînt aproape la fel de bune ca ponderea optimă văzută ulterior (@{combo.w_best_xgb|.2f})")],
        height="0.58\\textheight", job=t("average with equal weights before estimating clever weights.", "faceți media cu ponderi egale înainte de a estima ponderi „inteligente”."),
        tryit=NB + " \\S5", cite="(Bates \\& Granger, 1969; " + t("own computation", "calcule proprii") + ")")

    D.chart(t("Month by month, the combination beats AW-LEAR in @{bymonth.n_ldx_beats_lear} of 12 months",
              "Lunar, combinația este mai precisă decît AW-LEAR în @{bymonth.n_ldx_beats_lear} din 12 luni"), "monthly_ml", [
        (t("Alone, XGBoost and the DNN each beat AW-LEAR in only @{bymonth.n_xgb_beats_lear} months; averaged with it, in @{bymonth.n_ldx_beats_lear}.",
           "Luate separat, XGBoost și DNN depășesc AW-LEAR fiecare doar în @{bymonth.n_xgb_beats_lear} luni; în medie cu acesta, în @{bymonth.n_ldx_beats_lear} luni")
         if N["bymonth"]["n_xgb_beats_lear"] == N["bymonth"]["n_dnn_beats_lear"] else
         t("Alone, XGBoost and the DNN beat AW-LEAR in only @{bymonth.n_xgb_beats_lear} and @{bymonth.n_dnn_beats_lear} months; averaged with it, in @{bymonth.n_ldx_beats_lear}.",
           "Luate separat, XGBoost depășește AW-LEAR în @{bymonth.n_xgb_beats_lear} luni, iar DNN în @{bymonth.n_dnn_beats_lear}; în medie cu acesta, combinația îl depășește în @{bymonth.n_ldx_beats_lear} luni")),
        t("All models err more in the same months (January, June, October): the hard days are hard for everyone.",
          "Toate modelele greșesc mai mult în aceleași luni (ianuarie, iunie, octombrie): zilele dificile sînt dificile pentru toate")],
        height="0.58\\textheight", job=t("report accuracy month by month to the risk committee, not only the annual average.",
                                         "raportați comitetului de risc acuratețea lună de lună, nu doar media anuală."),
        tryit=NB + " \\S5", cite=OWN)

    D.chart(t("Compute cost: daily LEAR is the expensive model, ML costs minutes",
              "Costul de calcul: LEAR zilnic este cel mai scump, ML costă minute"), "cost_gain", [
        (t("Test year, one core: AW-LEAR @{cost.aw_lear|.1f} min (365 days $\\times$ 3 windows $\\times$ 24 h)",
           "Anul de test, pe un nucleu: AW-LEAR @{cost.aw_lear|.1f} min (365 de zile $\\times$ 3 ferestre $\\times$ 24 de ore)"),
         t("XGBoost @{cost.xgb|.1f} min, DNN @{cost.dnn|.1f} min, Chronos-2 @{cost.chr2|.1f} min",
           "XGBoost @{cost.xgb|.1f} min, DNN @{cost.dnn|.1f} min, Chronos-2 @{cost.chr2|.1f} min")),
        t("Hidden costs: the search (@{cost.search|.1f} min), the pretraining of Chronos, the people who run the pipeline.",
          "Costuri ascunse: căutarea setărilor (@{cost.search|.1f} min), preantrenarea Chronos, oamenii care operează fluxul")],
        height="0.58\\textheight", job=t("compare models on error per euro of total cost of ownership, not on error alone.",
                                         "comparați modelele după eroare raportată la costul total de utilizare, nu doar după eroare."),
        tryit=NB + " \\S5", cite=t("(own computation; times measured on one core of an 18-core laptop)", "(calcule proprii; timpi măsurați pe un nucleu al unui laptop cu 18 nuclee)"))

    # ------------------------------------------------------------------ 5 explainability
    D.section(t("Explaining the forecasts", "Explicarea prognozelor"))
    D.concept(t("Shapley values split each forecast into the contributions of its inputs", "Valorile Shapley descompun fiecare prognoză în contribuțiile variabilelor"),
              t("The contribution of an input is its average effect when it is added to the model, over all orders in which the inputs could be added.",
                "Contribuția unei variabile este efectul ei mediu atunci cînd este adăugată în model, calculat pe toate ordinile posibile de adăugare a variabilelor."),
              "\\[ \\phi_j=\\sum_{S\\not\\ni j}\\tfrac{|S|!\\,(p-|S|-1)!}{p!}\\big[v(S\\cup\\{j\\})-v(S)\\big] \\]\\vspace{-2mm}\\[ \\hat f(\\mathbf x)=\\phi_0+\\textstyle\\sum_{j}\\phi_j \\]" +
              "\\where{" + t("$\\phi_j$ = SHapley Additive exPlanations (SHAP) value of input $j$; $S$ = a subset of the other inputs; $v(S)$ = expected forecast when only $S$ is known; "
                             "$\\phi_0$ = average forecast; $p$ = 20 inputs.",
                             "$\\phi_j$ = valoarea variabilei $j$ după metoda explicațiilor aditive bazate pe valorile Shapley (SHAP); $S$ = o submulțime a celorlalte variabile; "
                             "$v(S)$ = prognoza așteptată cînd se cunoaște doar $S$; $\\phi_0$ = prognoza medie; $p$ = 20 de variabile.") + "}",
              it((t("\\textbf{Why Shapley values}", "\\textbf{De ce valorile Shapley}"),
                  t("the only fair split in the game-theory sense; they add up exactly to the forecast",
                    "singura împărțire echitabilă în sensul teoriei jocurilor; se adună exact la prognoză")),
                 (t("\\textbf{On our data}", "\\textbf{Pe datele noastre}"),
                  t("XGBoost, @{test.n_hours|,d} test hours; largest gap between $\\hat f$ and $\\phi_0+\\sum\\phi_j$: @{shap.check|.6f}",
                    "XGBoost, @{test.n_hours|,d} " + de("test.n_hours") + "ore de test; cea mai mare diferență dintre $\\hat f$ și $\\phi_0+\\sum\\phi_j$: @{shap.check|.6f}"),
                  t("past prices carry @{shap.groups.price|.1f}\\% of the total contribution",
                    "prețurile din zilele anterioare au @{shap.groups.price|.1f}\\% din contribuția totală")), sep="3pt"),
              t("ask for the explanation of each alarm, not only for a global ranking.",
                "cereți explicația fiecărei alerte, nu doar un clasament global."),
              tryit=NB + " \\S6", cite="(Shapley, 1953; Lundberg et al., 2020, Nat.\\ Mach.\\ Intell.)", wl="0.53", wr="0.44")

    D.chart(t("What drives the trees: yesterday's price at the same hour", "Ce determină prognoza arborilor: prețul de ieri, la aceeași oră"), "shap_global", [
        t("Top inputs: price $d-1$ same hour @{shap.top_share.0|.1f}\\%, price $d-7$ same hour @{shap.top_share.1|.1f}\\%, day of week @{shap.top_share.2|.1f}\\% of the mean $|\\phi|$.",
          "Ponderi în media $|\\phi|$: prețul din $d-1$, aceeași oră (@{shap.top_share.0|.1f}\\%), din $d-7$ (@{shap.top_share.1|.1f}\\%), ziua săptămînii (@{shap.top_share.2|.1f}\\%)"),
        t("Load @{shap.groups.load|.1f}\\%, wind + solar @{shap.groups.res|.1f}\\%: known only up to $d-2$, they are old news at gate closure.",
          "Consum @{shap.groups.load|.1f}\\%, eolian și solar @{shap.groups.res|.1f}\\%: cunoscute doar pînă în $d-2$, deci informații vechi")],
        height="0.58\\textheight", job=t("buy better inputs first: the load and wind forecasts of the transmission system operator (TSO).",
                                         "cumpărați întîi intrări mai bune: prognozele operatorului de transport și de sistem (TSO)."),
        tryit=NB + " \\S6", cite=OWN)

    D.chart(t("Wind and solar lower the price only in the hours when they are large", "Producția eoliană și solară scade prețul doar în orele în care este mare"), "shap_res", [
        (t("Each point is one test hour", "Fiecare punct este o oră din anul de test"),
         t("the more wind + solar on $d-2$ at that hour, the more negative its contribution (correlation @{shap.res_corr|.2f})",
           "mai multă producție eoliană și solară în $d-2$ înseamnă o contribuție mai negativă (corelație @{shap.res_corr|.2f})")),
        t("The effect appears above about 2 gigawatts (GW): a threshold that a linear model cannot express.",
          "Efectul apare peste circa 2 gigawați (GW): un prag pe care un model liniar nu îl poate exprima")],
        height="0.58\\textheight", job=t("a solar developer can read here the price discount that its own output helps to create.",
                                         "un dezvoltator solar vede aici reducerea de preț la care contribuie propria producție."),
        tryit=NB + " \\S6", cite=OWN)

    D.chart(t("The neural network relies even more on yesterday's prices", "Rețeaua neuronală se bazează și mai mult pe prețurile de ieri"), "perm_dnn", [
        (t("Permutation importance $I_b$ = rise in MAE when block $b$ is shuffled across test days",
           "Importanța prin permutare $I_b$ = creșterea MAE cînd blocul $b$ este amestecat între zilele de test"),
         t("5 permutations, valid for any model", "5 permutări, metodă valabilă pentru orice model")),
        (t("Prices of $d-1$: +@{perm.price_d1|.2f} EUR/MWh", "Prețurile din $d-1$: +@{perm.price_d1|.2f} EUR/MWh"),
         t("day of week +@{perm.day_of_week|.2f}, load +@{perm.load|.2f}, wind + solar @{perm.wind_solar|+.2f}",
           "ziua săptămînii +@{perm.day_of_week|.2f}, consumul +@{perm.load|.2f}, producția eoliană și solară @{perm.wind_solar|+.2f}"))],
        height="0.58\\textheight", job=t("monitor the price feed of $d-1$ first: the network fails without it.",
                                         "monitorizați întîi fluxul prețurilor din $d-1$: fără el, rețeaua cedează."),
        tryit=NB + " \\S6", cite="(Breiman, 2001, Mach.\\ Learn.; " + t("own computation", "calcule proprii") + ")")


    # (no subsection: the section outline of this lecture has no room for an extra line)
    D.frame(t("Energy finance uses machine learning widely but rarely explains it",
              "Finanțele energiei folosesc învățarea automată, dar rar o explică"), cols(
        it((t("\\textbf{R.\\ Clodnitchi, talk} (3 June 2026, \\href{" + CLO + "}{slides})",
              "\\textbf{R.\\ Clodnitchi, prezentare} (3 iunie 2026, \\href{" + CLO + "}{diapozitive})"),
            t("systematic review of artificial intelligence (AI) in energy finance (Anagnoste et al., 2025, \\textit{Energy Strategy Reviews})",
              "analiză sistematică a literaturii despre inteligența artificială (AI) în finanțele energiei (Anagnoste et al., 2025, \\textit{Energy Strategy Reviews})"),
            t("about 700 Web of Science articles screened, 232 peer-reviewed kept (2020--2025), on six pillars of energy finance",
              "circa 700 de articole din Web of Science, 232 reținute (evaluate colegial, 2020--2025), pe șase piloni ai finanțelor energiei")),
           (t("\\textbf{Where AI is used} (share of papers using AI/ML)", "\\textbf{Unde se folosește AI} (ponderea lucrărilor cu AI/ML)"),
            t("pricing mechanisms 100\\%, energy derivatives 100\\%, energy and financial markets " + n(97.5, ".1f") + "\\%, risk management " + n(93.0, ".1f") + "\\%",
              "mecanisme de preț 100\\%, derivate pe energie 100\\%, piețe energetice și financiare " + n(97.5, ".1f") + "\\%, gestiunea riscului " + n(93.0, ".1f") + "\\%"),
            t("green finance " + n(60.4, ".1f") + "\\%; corporate finance of energy firms 0\\% (panel econometrics only)",
              "finanțe verzi " + n(60.4, ".1f") + "\\%; finanțele corporative ale firmelor de energie 0\\% (numai econometrie pe date panel)")), sep="3pt"),
        it((t("\\textbf{What is missing}", "\\textbf{Ce lipsește}"),
            t("explainable AI: " + n(19.6, ".1f") + "\\% of the derivatives papers, 0--5\\% in the other pillars",
              "AI explicabilă: " + n(19.6, ".1f") + "\\% din lucrările despre derivate, 0--5\\% în ceilalți piloni"),
            t("neural networks dominate: " + n(88.2, ".1f") + "\\% of the derivatives papers, " + n(72.1, ".1f") + "\\% in risk management",
              "domină rețelele neuronale: " + n(88.2, ".1f") + "\\% din lucrările despre derivate, " + n(72.1, ".1f") + "\\% în gestiunea riscului"),
            t("proposed next step: explainable AI and causal machine learning for regulators and policy evaluation",
              "direcția propusă: AI explicabilă și învățare automată cauzală, pentru autoritățile de reglementare și evaluarea politicilor")),
           (t("\\textbf{Link with this lecture}", "\\textbf{Legătura cu acest curs}"),
            t("the SHAP and permutation charts of this section are the kind of explanation the review finds rare",
              "graficele SHAP și de permutare din această secțiune sînt tipul de explicație pe care analiza îl găsește rar")), sep="3pt"),
        "0.52", "0.45") +
        D.bottom(t("ask for the explanation together with the forecast: regulators and boards will ask for it.",
                   "cereți explicația odată cu prognoza: autoritățile și consiliile de administrație o vor cere.")),
        "footnotesize", cite=t("(AIDA 2026 slides, Bucharest; paper: ", "(diapozitivele AIDA 2026, București; lucrare: ") +
        "\\href{https://doi.org/10.1016/j.esr.2025.101833}{Anagnoste et al., 2025, ESR})")

    # ------------------------------------------------------------------ 6 spikes, negative prices, case study
    D.section(t("Spikes, negative prices and a case study", "Vîrfuri de preț, prețuri negative și un studiu de caz"))
    D.chart(t("Spikes come in the evening, negative prices at midday", "Vîrfurile de preț apar seara, prețurile negative la prînz"), "events_hour", [
        (t("\\textbf{Spike}: price above $\\theta$, the 90th percentile of the hourly prices of the 12 months before the delivery month",
           "\\textbf{Vîrf de preț}: preț peste $\\theta$, percentila 90 a prețurilor orare din cele 12 luni dinaintea lunii de livrare"),
         t("$\\theta$ from @{spike.theta_min|.1f} to @{spike.theta_max|.1f} EUR/MWh; @{spike.share_test|.1f}\\% of test hours are spikes, most at @{spike.peak_h}:00 (@{spike.peak_h_share|.1f}\\% of days)",
           "$\\theta$ între @{spike.theta_min|.1f} și @{spike.theta_max|.1f} EUR/MWh; @{spike.share_test|.1f}\\% din orele de test sînt vîrfuri, cele mai multe la ora @{spike.peak_h} (@{spike.peak_h_share|.1f}\\% din zile)")),
        t("\\textbf{Price $\\leq$ 0}: @{neg.n_test} hours on @{neg.n_days} days of the test year, mostly around @{neg.peak_h}:00.",
          "\\textbf{Preț $\\leq$ 0}: @{neg.n_test} " + de("neg.n_test") + "ore, în @{neg.n_days} " + de("neg.n_days") + "zile din anul de test, mai ales în jurul orei @{neg.peak_h}")],
        height="0.58\\textheight", job=t("a battery charges at midday and discharges at 19:00--20:00: the two events are its business model.",
                                         "o baterie se încarcă la prînz și se descarcă la orele 19--20: cele două evenimente sînt chiar modelul ei de afaceri."),
        tryit=NB + " \\S7", cite=OWN)

    sm = N["spike"]
    ng = N["neg"]
    crow = []
    for k, lab in [("xgb", "XGBoost"), ("logit", t("Logistic regression", "Regresie logistică")), ("persist", t("Persistence, 7 days", "Persistență, 7 zile")),
                   ("lear", t("AW-LEAR forecast $>\\theta$", "Prognoza AW-LEAR $>\\theta$"))]:
        crow.append([lab] + [fmt(sm[k][c], ".3f", lang) for c in ["auc", "prec", "rec", "f1"]] +
                    [fmt(sm[k]["brier"], ".3f", lang) if "brier" in sm[k] else "--", fmt(ng[k]["auc"], ".3f", lang), fmt(ng[k]["f1"], ".3f", lang)])
    D.concept(t("Spike classifiers: a good price forecast already detects spikes", "Clasificarea vîrfurilor: o prognoză bună de preț le detectează deja"),
              t("A classifier gives the probability that an hour is a spike; we judge how well it ranks the hours and how honest its probabilities are.",
                "Un clasificator dă probabilitatea ca o oră să fie un vîrf; judecăm cît de bine ordonează orele și cît de corecte sînt probabilitățile lui."),
              "\\[ \\hat\\pi_{d,h}=\\Pr\\big(P_{d,h}>\\theta_d\\mid\\mathbf x_{d,h}\\big) \\]\\vspace{-2mm}"
              "\\[ \\text{Brier}=\\frac{1}{n}\\sum_{d,h}\\big(\\hat\\pi_{d,h}-S_{d,h}\\big)^2 \\]" +
              "\\where{" + t("$S_{d,h}$ = 1 if the hour is a spike, 0 otherwise; precision = share of alerts that were spikes; recall = share of spikes that got an alert; "
                             "F1 = their harmonic mean; area under the curve (AUC) = probability that a spike hour gets a higher score than a normal hour.",
                             "$S_{d,h}$ = 1 dacă ora este un vîrf, 0 altfel; precizia = ponderea alertelor urmate de vîrfuri; sensibilitatea = ponderea vîrfurilor semnalate; "
                             "F1 = media lor armonică; aria de sub curbă (AUC) = probabilitatea ca o oră cu vîrf să primească un scor mai mare decît o oră obișnuită.") + "}",
              it((t("\\textbf{On our data}: XGBoost and logistic classifiers, refitted monthly", "\\textbf{Pe datele noastre}: clasificatori XGBoost și logistic, reestimați lunar"),
                  t("spikes in @{spike.share_test|.1f}\\% of test hours, @{spike.share_train_last|.1f}\\% in the last training sample",
                    "vîrfuri în @{spike.share_test|.1f}\\% din orele de test și în @{spike.share_train_last|.1f}\\% din ultimul eșantion de antrenare"),
                  t("Brier score: XGBoost @{spike.xgb.brier|.3f}; constant share of spikes @{spike.brier_clim|.3f}",
                    "scorul Brier: XGBoost @{spike.xgb.brier|.3f}; ponderea constantă a vîrfurilor @{spike.brier_clim|.3f}")),
                 (t("\\textbf{Benchmarks}", "\\textbf{Repere}"),
                  t("persistence: share of spikes at the same hour in the last 7 days", "persistența: ponderea vîrfurilor la aceeași oră în ultimele 7 zile"),
                  t("the AW-LEAR price forecast itself, compared with $\\theta$", "chiar prognoza de preț AW-LEAR, comparată cu $\\theta$")), sep="3pt"),
              t("judge an alert by its probabilities, not only by how many spikes it catches.",
                "judecați o alertă după probabilitățile ei, nu doar după cîte vîrfuri semnalează."),
              tryit=NB + " \\S7", cite="(Brier, 1950; Fawcett, 2006)", wl="0.56", wr="0.41")

    D.frame(t("Alerts on the test year: AW-LEAR matches a dedicated classifier",
              "Alertele din anul de test: AW-LEAR egalează un clasificator dedicat"),
            "\\begin{center}" + table("@{}lrrrrrrr@{}", [t("Model", "Model"), "AUC", t("Precision", "Precizie"), t("Recall", "Sensibilitate"), "F1", "Brier",
                                                         "AUC", "F1"], crow, size="footnotesize", stretch="1.25") + "\\end{center}" + note(
                t("Columns 2--6: spikes (@{spike.n_test|,d} hours); columns 7--8: prices $\\leq$ 0 (@{neg.n_test} hours). Alert when probability $>$ 0.5; AW-LEAR: alert when its price forecast exceeds $\\theta$ (or is $\\leq$ 0).",
                  "Coloanele 2--6: vîrfuri (@{spike.n_test|,d} " + de("spike.n_test") + "ore); coloanele 7--8: prețuri $\\leq$ 0 (@{neg.n_test} " + de("neg.n_test") + "ore). Alertă cînd probabilitatea $>$ 0{,}5; AW-LEAR: alertă cînd prognoza prețului depășește $\\theta$ (sau este $\\leq$ 0)."),
                t("For negative prices, XGBoost catches only @{neg.xgb.rec|.3f} of the events at threshold 0.5: these hours are rare and depend on tomorrow's weather.",
                  "La prețurile negative, XGBoost semnalează doar o fracțiune @{neg.xgb.rec|.3f} din evenimente la pragul 0{,}5: aceste ore sînt rare și depind de vremea de mîine.")) +
            D.bottom(t("buy a spike-alert service only if it beats the spike signal already hidden in your price forecast.",
                       "cumpărați un serviciu de alertă pentru vîrfuri doar dacă depășește semnalul ascuns deja în prognoza dumneavoastră de preț."), NB + " \\S7"),
            "small", cite=OWN)

    D.chart(t("Persistence detects spikes, but not negative prices", "Persistența detectează vîrfurile, dar nu și prețurile negative"), "roc", [
        t("Receiver operating characteristic (ROC) curves; spikes: AUC from @{spike.persist.auc|.3f} (persistence) to @{spike.lear.auc|.3f} (AW-LEAR), since the evening spike repeats day after day.",
          "Curbele caracteristice de operare (ROC); vîrfuri: AUC între @{spike.persist.auc|.3f} (persistență) și @{spike.lear.auc|.3f} (AW-LEAR), deoarece vîrful de seară se repetă de la o zi la alta"),
        t("Negative prices: persistence @{neg.persist.auc|.3f} against @{neg.xgb.auc|.3f} for XGBoost; they depend on tomorrow's sun and wind, not on yesterday.",
          "Prețuri negative: persistența are AUC @{neg.persist.auc|.3f}, față de @{neg.xgb.auc|.3f} pentru XGBoost; ele depind de soarele și vîntul de mîine, nu de ziua de ieri")],
        height="0.58\\textheight", tryit=NB + " \\S7", cite=OWN)

    D.chart(t("Cost--loss rule: act when the spike probability exceeds C/L", "Regula cost--pierdere: reacționați cînd probabilitatea depășește C/L"), "decision", [
        (t("\\textbf{Rule}: act if $\\hat\\pi_{d,h}>C/\\bar L$ = 30/@{decision.Lbar|.1f} = @{decision.cut|.3f}",
           "\\textbf{Regula}: reacție dacă $\\hat\\pi_{d,h}>C/\\bar L$ = 30/@{decision.Lbar|.1f} = @{decision.cut|.3f}"),
         t("C = cost of acting = 30 EUR/MWh (assumed): moving 1 MWh out of an alerted hour earns $P_{d,h}-\\theta_d-C$",
           "C = costul reacției = 30 EUR/MWh (ipoteză): mutarea a 1 MWh dintr-o oră cu alertă aduce $P_{d,h}-\\theta_d-C$"),
         t("$\\bar L$ = cost of a missed spike = mean excess over $\\theta$ in the validation year",
           "$\\bar L$ = costul unui vîrf ratat = depășirea medie a pragului în anul de validare")),
        t("Value per MW and year: @{decision.v_cut|.1f} thousand EUR at C/L, @{decision.v_persist|.1f} with persistence, @{decision.v_perfect|.1f} with perfect foresight.",
          "Valoarea pe MW și an: @{decision.v_cut|.1f} mii EUR la pragul C/L, @{decision.v_persist|.1f} cu persistența, @{decision.v_perfect|.1f} cu informație perfectă")],
        height="0.58\\textheight", job=t("set the threshold from your costs, not from hindsight (best threshold ex post: @{decision.best_cut|.2f}).",
                                         "stabiliți pragul din propriile costuri, nu retrospectiv (cel mai bun prag ulterior: @{decision.best_cut|.2f})."),
        tryit=NB + " \\S7", cite="(Murphy, 1977, MWR; " + t("own computation", "calcule proprii") + ")")

    D.chart(t("Case study, @{case.day|date}: every model saw the spike, none its size",
              "Studiu de caz, @{case.day|date}: vîrf anticipat, amploare subestimată"), "case_week", [
        (t("\\textbf{Hour @{case.hour}:00 CET}: @{case.price|.2f} EUR/MWh, the highest price of the test year",
           "\\textbf{Ora @{case.hour}:00 CET}: @{case.price|.2f} EUR/MWh, cel mai mare preț din anul de test"),
         t("forecasts: AW-LEAR @{case.aw_lear|.0f}, XGBoost @{case.xgb|.0f}, DNN @{case.dnn|.0f}, Chronos-2 @{case.chr2|.0f}; spike probability @{case.p_xgb|.3f}",
           "prognoze: AW-LEAR @{case.aw_lear|.0f}, XGBoost @{case.xgb|.0f}, DNN @{case.dnn|.0f}, Chronos-2 @{case.chr2|.0f}; probabilitatea vîrfului @{case.p_xgb|.3f}")),
        t("In that week: @{case.w_spike_h} spike hours, @{case.w_alerts} alerts at C/L, @{case.w_hits} of them correct.",
          "În acea săptămînă: @{case.w_spike_h} " + de("case.w_spike_h") + "ore cu vîrf, @{case.w_alerts} " + de("case.w_alerts") + "alerte la pragul C/L, dintre care @{case.w_hits} corecte")],
        height="0.58\\textheight", job=t("the probability says whether to act, the point forecast how much.",
                                         "probabilitatea arată dacă reacționați, prognoza punctuală arată cît."),
        tryit=NB + " \\S8", cite=t("(own computation; Romanian day-ahead prices)", "(calcule proprii; prețurile PZU din România)"))

    D.chart(t("Case study: the trees followed the extreme evening of the day before",
              "Studiu de caz: arborii au urmat seara extremă din ziua precedentă"), "shap_local", [
        t("From @{case.base_eur|.0f} (model average) to @{case.xgb_eur|.0f} EUR/MWh: price of $d-1$, same hour, @{case.top_eur.0|+.0f}; price of $d-7$ @{case.top_eur.1|+.0f}.",
          "De la @{case.base_eur|.0f} (prognoza medie) la @{case.xgb_eur|.0f} EUR/MWh: prețul din $d-1$, aceeași oră, @{case.top_eur.0|+.0f}; prețul din $d-7$ @{case.top_eur.1|+.0f}"),
        t("Trees cannot go above the prices stored in their leaves: extremes are capped.",
          "Arborii nu pot depăși prețurile memorate în frunze: valorile extreme sînt plafonate")],
        height="0.58\\textheight", job=t("show the board this breakdown for every large alert.",
                                         "prezentați consiliului de administrație această descompunere pentru fiecare alertă importantă."),
        tryit=NB + " \\S8", cite=t("(own computation; SHAP values in EUR/MWh, Appendix C)", "(calcule proprii; valori SHAP în EUR/MWh, anexa C)"))

    D.frame(t("Our group on spike early warning: the paper and our replication",
              "Avertizarea timpurie a vîrfurilor: lucrarea grupului și replicarea ei"), it(
        (t("\\textbf{What the paper did} (Andrei, Pele, Cramer, Amza \\& Diaconu, 2026)", "\\textbf{Ce a făcut lucrarea} (Andrei, Pele, Cramer, Amza \\& Diaconu, 2026)"),
         t("data: 5,000 hours of the Romanian day-ahead market in 2024, with load, renewable and fuel data; spike = price above the 90th percentile",
           "date: 5.000 de ore de pe PZU din România, în 2024, cu date despre consum, surse regenerabile și combustibili; vîrf = preț peste percentila 90"),
         t("method: random forests and XGBoost explained with SHAP; an early-warning score built from the thresholds of several indicators",
           "metodă: păduri aleatoare și XGBoost, explicate cu SHAP; un scor de avertizare construit din pragurile mai multor indicatori"),
         t("result: the previous price and the residual load forecast are the main drivers of spikes",
           "rezultat: prețul anterior și prognoza consumului rezidual sînt principalii factori ai vîrfurilor")),
        (t("\\textbf{Our replication} (case study C7, gate-closure information only)", "\\textbf{Replicarea noastră} (studiul de caz C7, numai cu informația de la închiderea licitației)"),
         t("test period Jul 2025 -- Oct 2026; spikes in @{c7.spikeTest|.1f}\\% of hours (training: @{c7.spikeTrain|.1f}\\%)",
           "perioada de test: iulie 2025 -- octombrie 2026; vîrfuri în @{c7.spikeTest|.1f}\\% din ore (în antrenare: @{c7.spikeTrain|.1f}\\%)"),
         t("XGBoost AUC @{c7.xAUC|.3f}; top drivers: yesterday's and last week's price at the same hour, as on the previous slides",
           "XGBoost: AUC @{c7.xAUC|.3f}; principalii factori: prețul de ieri și cel de acum o săptămînă, la aceeași oră, ca pe diapozitivele anterioare")),
        sep="3pt") + note(t("Paper results as stated in the paper; replication numbers computed by the C7 case notebook on our data.",
                            "Rezultatele lucrării sînt cele raportate de autori; cifrele replicării sînt calculate cu notebook-ul Jupyter al studiului de caz C7, pe datele noastre.")) +
        D.bottom(t("a residual-load forecast is the input that a spike model needs most and that our public data lack.",
                   "prognoza consumului rezidual este variabila de care un model de vîrfuri are cea mai mare nevoie și care lipsește din datele noastre publice.")),
        "footnotesize", cite="(Andrei, Pele, Cramer, Amza \\& Diaconu, 2026, PICBE; " + t("case study C7", "studiul de caz C7") + ")")

    # ------------------------------------------------------------------ 7 pitfalls
    D.section(t("Pitfalls that flatter a model", "Capcane care fac un model să pară mai bun"))
    D.chart(t("Look-ahead: two invalid evaluations flatter XGBoost", "Informația din viitor: două evaluări invalide avantajează XGBoost"), "pit_leak", [
        (t("\\textbf{Shuffled 5-fold cross-validation}: future days end up in the training sample",
           "\\textbf{Validare încrucișată cu 5 subeșantioane amestecate}: zile din viitor intră în antrenare"),
         t("MAE @{pit.shuffled|.2f} instead of @{pit.honest|.2f}: @{pit.shuf_gain|.1f}\\% better, on paper only", "MAE @{pit.shuffled|.2f} în loc de @{pit.honest|.2f}: cu @{pit.shuf_gain|.1f}\\% mai bine, doar pe hîrtie")),
        (t("\\textbf{Load and renewable energy sources (RES) of day $d$ as inputs}: unknown at 12:00 on $d-1$",
           "\\textbf{Consum și surse regenerabile de energie (RES) din ziua $d$}: necunoscute la 12:00 în $d-1$"),
         t("MAE @{pit.leak|.2f}, an apparent gain of @{pit.leak_gain|.1f}\\%: the most that perfect forecasts of these inputs could add",
           "MAE @{pit.leak|.2f}, un cîștig aparent de @{pit.leak_gain|.1f}\\%: cel mult cît ar aduce prognoze perfecte ale acestor variabile"))],
        height="0.58\\textheight", job=t("ask every vendor for a walk-forward test with each input time-stamped at gate closure.",
                                         "cereți oricărui furnizor o testare cronologică, cu intrările datate la închiderea licitației."),
        tryit=NB + " \\S9", cite="(Bergmeir \\& Benítez, 2012, Inf.\\ Sci.; " + t("own computation", "calcule proprii") + ")")

    D.chart(t("Data snooping: choosing on the test year fakes a win over LEAR", "Alegerea pe anul de test simulează o victorie asupra LEAR"), "snooping", [
        t("Honest DNN (chosen on validation, 1 seed): MAE @{search.dnn.test_chosen|.2f}; best of @{search.n_cfg} settings on the test year: @{search.dnn.test_best|.2f}, just below AW-LEAR (@{acc.aw_lear.mae|.2f}).",
          "Rețeaua DNN aleasă corect (la validare, o inițializare): MAE @{search.dnn.test_chosen|.2f}; cea mai bună dintre cele @{search.n_cfg} " + de("search.n_cfg") + "setări pe anul de test: @{search.dnn.test_best|.2f}, chiar sub AW-LEAR (@{acc.aw_lear.mae|.2f})"),
        t("Validation works, but not perfectly: Spearman rank correlation @{search.dnn.spearman|.2f} (DNN), @{search.xgb.spearman|.2f} (XGBoost).",
          "Validarea funcționează, dar imperfect: corelația Spearman a rangurilor, @{search.dnn.spearman|.2f} (DNN), @{search.xgb.spearman|.2f} (XGBoost)")],
        height="0.58\\textheight", job=t("ask how many models were tried: the more trials, the more the best one flatters.",
                                         "întrebați cîte modele au fost încercate: cu cît mai multe, cu atît cel mai bun pare mai bun."),
        tryit=NB + " \\S9", cite="(White, 2000, Econometrica; " + t("own computation", "calcule proprii") + ")")

    # (no subsection: the section outline of this lecture has no room for an extra line)
    D.frame(t("The best of many models must be tested against the benchmark",
              "Cel mai bun dintre multe modele trebuie testat față de reper"), cols(
        "\\vspace{-2mm}\\[ \\mathrm{RC}_n=\\max_{k=1,\\dots,m}\\sqrt{n}\\,\\bar d_k,\\qquad \\bar d_k=\\frac1n\\sum_{t=1}^{n}d_{k,t} \\]" +
        "\\where{" + t("$d_{k,t}$ = benchmark loss minus loss of model $k$ on day $t$; $H_0$: $E(d_{k,t})\\le 0$ for all $k$; "
                       "critical value: joint bootstrap of $(d_{1,t},\\dots,d_{m,t})$, which keeps the correlation between models.",
                       "$d_{k,t}$ = pierderea reperului minus cea a modelului $k$ în ziua $t$; $H_0$: $E(d_{k,t})\\le 0$ pentru orice $k$; "
                       "valoarea critică: bootstrap comun pe $(d_{1,t},\\dots,d_{m,t})$, cu corelația dintre modele păstrată.") + "}" +
        it(t("\\textbf{Why}: for $m$ independent 5\\% tests, P(at least one false win) = $1-" + n(0.95, ".2f") + "^m$: " + n(0.401, ".3f") + " ($m$ = 10), " + n(0.994, ".3f") + " ($m$ = 100).",
             "\\textbf{De ce}: pentru $m$ teste independente la 5\\%, P(cel puțin o victorie falsă) = $1-" + n(0.95, ".2f") + "^m$: " + n(0.401, ".3f") + " ($m$ = 10), " + n(0.994, ".3f") + " ($m$ = 100)"), sep="2pt"),
        it((t("\\textbf{C.-M.\\ Kuan, 4 June 2026} (\\href{" + KUA + "}{slides})",
              "\\textbf{C.-M.\\ Kuan, 4 iunie 2026} (\\href{" + KUA + "}{diapozitive})"),
            t("Reality Check (RC), White (2000): conservative, poor models added to the set reduce its power (Hansen, 2005)",
              "testul Reality Check (RC), White (2000): conservator, modelele slabe adăugate îi reduc puterea (Hansen, 2005)"),
            t("superior predictive ability (SPA) test, Hansen (2005): recentres the poor models, more powerful",
              "testul abilității predictive superioare (SPA), Hansen (2005): recentrează modelele slabe, mai puternic"),
            t("Step-RC (Romano \\& Wolf, 2005), Step-SPA (Hsu, Hsu \\& Kuan, 2010): name the winners, familywise error rate (FWER) under control",
              "Step-RC (Romano \\& Wolf, 2005), Step-SPA (Hsu, Hsu \\& Kuan, 2010): identifică modelele mai bune, controlînd rata erorii la nivelul familiei de ipoteze (FWER)")),
           (t("\\textbf{On our data}", "\\textbf{Pe datele noastre}"),
            t("the best of @{search.n_cfg} DNN settings on the test year is just below AW-LEAR: the selection RC and SPA correct for",
              "cea mai bună dintre cele @{search.n_cfg} " + de("search.n_cfg") + "setări DNN pe anul de test trece sub AW-LEAR: cazul corectat de RC și SPA")), sep="3pt"),
        "0.44", "0.53") +
        D.bottom(t("when shown the best of many models, ask for an RC or SPA p-value against your benchmark.",
                   "cînd vi se arată cel mai bun dintre multe modele, cereți valoarea p a testului RC sau SPA.")),
        "footnotesize", cite=t("(AIDA 2026 slides; papers: ", "(diapozitivele AIDA 2026; lucrări: ") +
        "\\href{https://doi.org/10.1111/1468-0262.00152}{White, 2000}; \\href{https://doi.org/10.1198/073500105000000063}{Hansen, 2005}; "
        "\\href{https://doi.org/10.1111/j.1468-0262.2005.00615.x}{Romano \\& Wolf, 2005}; \\href{https://doi.org/10.1016/j.jempfin.2010.01.001}{Hsu et al., 2010})")

    D.chart(t("Retraining: a model frozen for a year loses @{pit.once_loss|.1f}\\%",
              "Reestimarea: un model neactualizat un an pierde @{pit.once_loss|.1f}\\%"), "pit_retrain", [
        t("Fitted once, before the test year: MAE @{pit.once|.2f}; the loss grows with time (+@{pit.once_first_q|.2f} EUR/MWh in the first 3 months, +@{pit.once_last_q|.2f} in the last 3).",
          "Estimat o singură dată, înaintea anului de test: MAE @{pit.once|.2f}; pierderea crește în timp (+@{pit.once_first_q|.2f} EUR/MWh în primele 3 luni, +@{pit.once_last_q|.2f} în ultimele 3)"),
        t("A short rolling window (365 days, MAE @{pit.roll365|.2f}) is worse than the whole history: the trees need many past spikes to learn from.",
          "O fereastră glisantă scurtă (365 de zile, MAE @{pit.roll365|.2f}) este mai slabă decît întregul istoric: arborii au nevoie de multe vîrfuri din trecut pentru a învăța")],
        height="0.58\\textheight", job=t("put the monthly refit in the operating calendar, with an owner, like any other control.",
                                         "includeți reestimarea lunară în calendarul operațional, cu un responsabil, ca pe orice alt control."),
        tryit=NB + " \\S9", cite=OWN)

    D.frame(t("Leakage self-check: deleting the future changes no forecast",
              "Testul de scurgere a informației: ștergerea viitorului nu schimbă nimic"), cols(it(
        (t("\\textbf{The test}", "\\textbf{Testul}"),
         t("for the first day of each of the @{leak.n_months} test months, all data after 12:00 on $d-1$ are deleted, then replaced by 10\\,000 EUR/MWh",
           "pentru prima zi din fiecare dintre cele @{leak.n_months} luni de test, toate datele de după ora 12:00 din ziua $d-1$ sînt șterse, apoi înlocuite cu 10\\,000 EUR/MWh"),
         t("XGBoost, the DNN and the spike classifier are refitted and must give the same forecasts",
           "XGBoost, rețeaua DNN și clasificatorul de vîrfuri sînt reestimate și trebuie să dea aceleași prognoze")),
        (t("\\textbf{Result}", "\\textbf{Rezultatul}"),
         t("trees and classifier: identical; DNN: differences below 0.001 EUR/MWh (rounding in parallel arithmetic)",
           "arborii și clasificatorul: prognoze identice; DNN: diferențe sub 0{,}001 EUR/MWh (rotunjiri ale calculelor paralele)"),
         t("Chronos: the context is built only from days before day $d$, checked in the code", "Chronos: contextul este construit numai din zilele dinaintea zilei $d$, verificat în cod")),
        sep="3pt"), it(
        (t("\\textbf{Checklist before trusting a model}", "\\textbf{Lista de verificare înainte de a avea încredere într-un model}"),
         t("every input time-stamped at gate closure", "fiecare intrare datată la momentul închiderii licitației"),
         t("settings chosen on a validation year", "setări alese pe un an de validare"),
         t("one test year, opened once, with DM tests against LEAR", "un singur an de test, deschis o singură dată, cu teste DM față de LEAR"),
         t("monthly refits and a perturbation test like this one", "reestimări lunare și un test de perturbare ca acesta")), sep="3pt"), "0.52", "0.45") +
        D.bottom(t("make this check part of every model review, for statistical and machine-learning models alike.",
                   "includeți această verificare în evaluarea oricărui model, statistic sau de învățare automată."), NB + " \\S10"),
        "footnotesize", cite=t("(Lecture 2; Lago et al., 2021, APEN)", "(cursul 2; Lago et al., 2021, APEN)"))

    # ------------------------------------------------------------------ wrap-up
    D.parts.append("\\section*{" + t("Wrap-up", "Recapitulare") + "}\n")
    D.quiz_frame(t("a perfect backtest", "o testare retrospectivă perfectă"),
                 t("A start-up shows a neural network with rMAE 0.70 on Romania, tested with shuffled 5-fold cross-validation; what do you ask for?",
                   "Un start-up prezintă o rețea neuronală cu rMAE 0{,}70 pentru România, testată prin validare încrucișată cu 5 subeșantioane amestecate; ce cereți?"),
                 t("A walk-forward test on one untouched year, with inputs known at 12:00 on $d-1$: on our data, shuffling alone made XGBoost look @{pit.shuf_gain|.1f}\\% better.",
                   "O testare cronologică pe un an neatins, cu intrări cunoscute la ora 12:00 în ziua $d-1$: pe datele noastre, doar amestecarea a făcut XGBoost să pară cu @{pit.shuf_gain|.1f}\\% mai bun."))
    D.quiz_frame(t("which model to deploy", "ce model puneți în producție"),
                 t("Chronos-2 has the lowest MAE of the single models; AW-LEAR + Chronos-2 has the same MAE; which do you deploy?",
                   "Chronos-2 are cea mai mică MAE dintre modelele individuale; combinația AW-LEAR + Chronos-2 are aceeași MAE; pe care o puneți în producție?"),
                 t("The combination: same accuracy (DM " + pv("dm.chr2__ens_lc.p") + "), but if the pretrained model degrades or becomes unavailable, LEAR still carries half of the forecast.",
                   "Combinația: aceeași acuratețe (DM, " + pv("dm.chr2__ens_lc.p") + "), dar dacă modelul preantrenat se degradează sau devine indisponibil, LEAR asigură în continuare jumătate din prognoză."))
    D.quiz_frame(t("reading SHAP", "interpretarea valorilor SHAP"),
                 t("Load has a small SHAP share (@{shap.groups.load|.1f}\\%); can we conclude that load does not affect the price?",
                   "Consumul are o pondere SHAP mică (@{shap.groups.load|.1f}\\%); putem concluziona că acesta nu influențează prețul?"),
                 t("No: SHAP explains the model, not the market; load enters only with its $d-2$ value, already reflected in yesterday's price.",
                   "Nu: SHAP explică modelul, nu piața; consumul intră doar cu valoarea din ziua $d-2$, deja reflectată în prețul de ieri."))
    D.quiz_frame(t("an alert threshold", "pragul de alertă"),
                 t("Moving 1 MWh costs you 60 EUR instead of 30; how does the alert threshold change?",
                   "Mutarea a 1 MWh vă costă 60 EUR în loc de 30; cum se schimbă pragul de alertă?"),
                 t("It doubles: C/L rises from @{decision.cut|.3f} to about twice that value, so you act only on the more certain spikes.",
                   "Se dublează: C/L crește de la @{decision.cut|.3f} la aproximativ dublul acestei valori, deci reacționați numai la vîrfurile mai sigure."))
    D.quiz_frame(t("retraining", "reestimarea"),
                 t("Your data team proposes to train the model once a year to save effort; what does the test year say?",
                   "Echipa de date propune ca modelul să fie antrenat o dată pe an, pentru a economisi efort; ce arată anul de test?"),
                 t("A model frozen for the year was @{pit.once_loss|.1f}\\% less accurate, and the gap widened in the last months; a monthly refit of XGBoost takes about @{cost.xgb_refit_s|.0f} seconds.",
                   "Un model neactualizat un an a fost cu @{pit.once_loss|.1f}\\% mai puțin precis, iar diferența a crescut în ultimele luni; o reestimare lunară a XGBoost durează circa @{cost.xgb_refit_s|.0f} de secunde."))

    D.frame(t("Wrap-up", "Recapitulare"), "\\vspace{-2mm}\\begin{multicols}{2}\\scriptsize\\tableofcontents\\end{multicols}\n" + it(
        t("Tuned, the DNN and XGBoost improve on Lecture 2 but do not beat AW-LEAR alone; averaged with it, they do.",
          "Calibrate, rețeaua DNN și XGBoost sînt mai precise decît în cursul 2, dar nu depășesc singure AW-LEAR; în medie cu acesta, îl depășesc"),
        t("Chronos-2, with no training, is the most accurate single model (MAE @{acc.chr2.mae|.2f}, @{acc.chr2.vs_lear|.1f}\\% below AW-LEAR); every model must be explained, validated and refitted.",
          "Chronos-2, fără antrenare, este cel mai precis model individual (MAE @{acc.chr2.mae|.2f}, cu @{acc.chr2.vs_lear|.1f}\\% sub AW-LEAR); orice model trebuie explicat, validat și reestimat"),
        sep="1pt"))

    D.frame(t("Research from our group on machine learning for Romanian power prices", "Cercetările grupului nostru: învățarea automată pe piața din România"), it(
        t("\\textbf{Early warning of price spikes} (Andrei, Pele, Cramer, Amza \\& Diaconu, 2026, PICBE): built an explainable artificial intelligence (AI) system for the Romanian day-ahead market; "
          "the previous price and the residual load drive the spikes --- case study C7.",
          "\\textbf{Avertizarea timpurie a vîrfurilor de preț} (Andrei, Pele, Cramer, Amza \\& Diaconu, 2026, PICBE); ce a făcut lucrarea: a construit un sistem explicabil de inteligență "
          "artificială (AI) pentru PZU din România; rezultat: prețul anterior și consumul rezidual sînt principalii factori ai vîrfurilor (studiul de caz C7)"),
        t("\\textbf{Explaining price forecasts across horizons} (Andrei, Pele \\& Cramer, 2026, PICBE): explained machine-learning forecasts of Romanian hourly prices "
          "and showed which drivers matter at each horizon and in each price regime.",
          "\\textbf{Explicarea prognozelor de preț pe mai multe orizonturi} (Andrei, Pele \\& Cramer, 2026, PICBE); ce a făcut lucrarea: a explicat prognozele de învățare automată "
          "pentru prețurile orare din România; rezultat: arată ce factori contează la fiecare orizont și în fiecare regim de preț"),
        t("\\textbf{Four generations of price models} (Andrei, Velev, Toma, Pele \\& Lessmann, 2024, arXiv 2411.03372): compared four generations of forecasting methods "
          "for energy prices, from statistical models to deep learning, as a guide for choosing a model family.",
          "\\textbf{Patru generații de modele pentru prețul energiei} (Andrei, Velev, Toma, Pele \\& Lessmann, 2024, arXiv 2411.03372); ce a făcut lucrarea: a comparat patru generații "
          "de metode de prognoză a prețurilor energiei, de la modelele statistice la învățarea profundă; utilitate: un reper pentru alegerea familiei de modele"),
        t("\\textbf{Foundation models for tail risk} (Jheng, Tak, Găman, Mazurencu-Marinescu-Pele \\& Pele, 2026, ECECSR): used pretrained foundation models, without retraining "
          "and with conformal calibration, to forecast extreme losses in Central and Eastern European markets.",
          "\\textbf{Modele fundaționale pentru riscul extrem} (Jheng, Tak, Găman, Mazurencu-Marinescu-Pele \\& Pele, 2026, ECECSR); ce a făcut lucrarea: a folosit modele fundaționale "
          "preantrenate, fără reantrenare și cu calibrare conformală, pentru prognoza pierderilor extreme pe piețele din Europa Centrală și de Est"),
        sep="3pt") + note(t("Findings as stated in the papers; numbers on the other slides come from our own data.",
                            "Rezultatele de pe acest diapozitiv sînt cele raportate în lucrări; celelalte cifre din curs provin din calculele noastre.")),
        "footnotesize", cite=t("(Bucharest University of Economic Studies; Romanian Academy, Institute for Economic Forecasting)",
                               "(Academia de Studii Economice din București; Academia Română, Institutul de Prognoză Economică)"))

    D.frame(t("Want to learn more?", "Lecturi și resurse suplimentare"), cols(it(
        t("\\textbf{epftoolbox}: the DNN and LEAR of Lago et al.\\ (2021) with open benchmark data --- ",
          "\\textbf{epftoolbox}: rețeaua DNN și modelul LEAR din Lago et al.\\ (2021), cu date deschise pentru evaluare --- ") +
        "\\href{https://github.com/jeslago/epftoolbox}{github.com/jeslago/epftoolbox}.",
        t("\\textbf{XGBoost} and \\textbf{shap} documentation: ", "\\textbf{XGBoost} și \\textbf{shap}, documentație: ") +
        "\\href{https://xgboost.readthedocs.io}{xgboost.readthedocs.io}, \\href{https://shap.readthedocs.io}{shap.readthedocs.io}.",
        t("\\textbf{Chronos} foundation models: ", "\\textbf{Chronos}, modele fundaționale: ") + "\\href{https://github.com/amazon-science/chronos-forecasting}{github.com/amazon-science/chronos-forecasting}.",
        t("\\textbf{Interpretable Machine Learning} (C.\\ Molnar), free online: ", "\\textbf{Interpretable Machine Learning} (C.\\ Molnar), gratuit online: ") +
        "\\href{https://christophm.github.io/interpretable-ml-book/}{christophm.github.io}.", sep="4pt"),
        it(t("\\textbf{This course}: code, data, notebooks --- ", "\\textbf{Acest curs}: cod, date, notebook-uri Jupyter --- ") +
           "\\href{https://github.com/danpele/EMQA}{github.com/danpele/EMQA}.",
           t("\\textbf{Case study C7} replicates the spike early-warning paper on our data.",
             "\\textbf{Studiul de caz C7} replică pe datele cursului lucrarea despre avertizarea timpurie a vîrfurilor."),
           t("\\textbf{Experiment yourself}: the notebook reproduces every chart and number of this lecture --- ",
             "\\textbf{Exercițiu practic}: notebook-ul Jupyter reproduce toate graficele și cifrele din acest curs --- ") +
           "\\href{\\emqarepo/\\emqanb}{notebooks/}.", sep="4pt"), "0.52", "0.45"))

    REFS = [
        "Anagnoste, S., Andrei, A.-V., Bolovăneanu, V., Cepoi, C.-O., Clodnitchi, R., Cramer, A.-A., Grecu, R.-A., Lessmann, S., Pele, D.\\,T., "
        "Petukhina, A.\\ \\& Strat, V.\\,A.\\ (2025). The role of AI in (re)shaping energy finance: A systematic literature review. "
        "\\textit{Energy Strategy Reviews}, 61, 101833. \\href{https://doi.org/10.1016/j.esr.2025.101833}{doi:10.1016/j.esr.2025.101833}",
        "Andrei, A.-V., Pele, D.-T.\\ \\& Cramer, A.-A.\\ (2026). Multi-horizon explainability in energy price forecasting: Disentangling "
        "market dynamics and renewable intermittency in Romania's liberalized electricity market. \\textit{Proceedings of the "
        "International Conference on Business Excellence}, 20(1), 104--117. \\href{https://doi.org/10.2478/picbe-2026-0014}{doi:10.2478/picbe-2026-0014}",
        "Andrei, A.-V., Pele, D.-T., Cramer, A.-A., Amza, A.\\ \\& Diaconu, D.\\ (2026). Explainable AI-based early warning system for electricity "
        "price spikes: Evidence from the Romanian market. \\textit{Proceedings of the International Conference on Business Excellence}, 20(1), "
        "4820--4836. \\href{https://doi.org/10.2478/picbe-2026-0352}{doi:10.2478/picbe-2026-0352}",
        "Andrei, A.-V., Velev, G., Toma, F.-M., Pele, D.\\,T.\\ \\& Lessmann, S.\\ (2024). Energy price modelling: A comparative evaluation of "
        "four generations of forecasting methods. \\href{https://arxiv.org/abs/2411.03372}{arXiv:2411.03372}",
        "Andrei, A.-V., Velev, G., Toma, F.-M., Pele, D.\\,T.\\ \\& Lessmann, S.\\ (2026). Energy price modelling: A comparative evaluation of "
        "four generations of forecasting methods. Talk, AIDA Conference, Bucharest University of Economic Studies, 3 June 2026. "
        "\\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/andrei_ai4efin_benchmarking.pdf}{github.com/danpele/EMQA/resources/aida2026}",
        "Ansari, A.\\,F., Stella, L., Turkmen, C.\\ et al.\\ (2024). Chronos: Learning the language of time series. \\textit{Transactions on Machine "
        "Learning Research}. \\href{https://arxiv.org/abs/2403.07815}{arXiv:2403.07815}",
        "Ansari, A.\\,F., Shchur, O., Küken, J.\\ et al.\\ (2025). Chronos-2: From univariate to universal forecasting. \\href{https://arxiv.org/abs/2510.15821}{arXiv:2510.15821}",
        "Bates, J.\\,M.\\ \\& Granger, C.\\,W.\\,J.\\ (1969). The combination of forecasts. \\textit{Journal of the Operational Research Society}, 20(4), 451--468. "
        "\\href{https://doi.org/10.1057/jors.1969.103}{doi:10.1057/jors.1969.103}",
        "Bergmeir, C.\\ \\& Benítez, J.\\,M.\\ (2012). On the use of cross-validation for time series predictor evaluation. \\textit{Information Sciences}, 191, 192--213. "
        "\\href{https://doi.org/10.1016/j.ins.2011.12.028}{doi:10.1016/j.ins.2011.12.028}",
        "Bergstra, J.\\ \\& Bengio, Y.\\ (2012). Random search for hyper-parameter optimization. \\textit{Journal of Machine Learning Research}, 13, 281--305. "
        "\\href{https://jmlr.org/papers/v13/bergstra12a.html}{jmlr.org/papers/v13/bergstra12a.html}",
        "Breiman, L.\\ (2001). Random forests. \\textit{Machine Learning}, 45(1), 5--32. \\href{https://doi.org/10.1023/A:1010933404324}{doi:10.1023/A:1010933404324}",
        "Brier, G.\\,W.\\ (1950). Verification of forecasts expressed in terms of probability. \\textit{Monthly Weather Review}, 78(1), 1--3. "
        "\\href{https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2}{doi:10.1175/1520-0493(1950)078\\allowbreak<0001:VOFEIT>2.0.CO;2}",
        "Chen, T.\\ \\& Guestrin, C.\\ (2016). XGBoost: A scalable tree boosting system. \\textit{Proceedings of the 22nd ACM SIGKDD Conference}, 785--794. "
        "\\href{https://doi.org/10.1145/2939672.2939785}{doi:10.1145/2939672.2939785}",
        "Clodnitchi, R.\\ (2026). The role of AI in (re)shaping energy finance: A systematic literature review. Talk, AIDA Conference, Bucharest "
        "University of Economic Studies, 3 June 2026. \\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/clodnitchi_ai_energy_finance_review.pdf}{github.com/danpele/EMQA/resources/aida2026}",
        "Diebold, F.\\,X.\\ \\& Mariano, R.\\,S.\\ (1995). Comparing predictive accuracy. \\textit{Journal of Business \\& Economic Statistics}, "
        "13(3), 253--263. \\href{https://doi.org/10.1080/07350015.1995.10524599}{doi:10.1080/07350015.1995.10524599}",
        "Fawcett, T.\\ (2006). An introduction to ROC analysis. \\textit{Pattern Recognition Letters}, 27(8), 861--874. "
        "\\href{https://doi.org/10.1016/j.patrec.2005.10.010}{doi:10.1016/j.patrec.2005.10.010}",
        "Friedman, J.\\,H.\\ (2001). Greedy function approximation: A gradient boosting machine. \\textit{Annals of Statistics}, 29(5), "
        "1189--1232. \\href{https://doi.org/10.1214/aos/1013203451}{doi:10.1214/aos/1013203451}",
        "Hansen, P.\\,R.\\ (2005). A test for superior predictive ability. \\textit{Journal of Business \\& Economic Statistics}, 23(4), 365--380. "
        "\\href{https://doi.org/10.1198/073500105000000063}{doi:10.1198/073500105000000063}",
        "Hastie, T., Tibshirani, R.\\ \\& Friedman, J.\\ (2009). \\textit{The Elements of Statistical Learning}, 2nd ed. Springer. "
        "\\href{https://doi.org/10.1007/978-0-387-84858-7}{doi:10.1007/978-0-387-84858-7}",
        "Hsu, P.-H., Hsu, Y.-C.\\ \\& Kuan, C.-M.\\ (2010). Testing the predictive ability of technical analysis using a new stepwise test without data "
        "snooping bias. \\textit{Journal of Empirical Finance}, 17(3), 471--484. \\href{https://doi.org/10.1016/j.jempfin.2010.01.001}{doi:10.1016/j.jempfin.2010.01.001}",
        "Jheng, S., Tak, R., Găman, Ș., Mazurencu-Marinescu-Pele, M.\\ \\& Pele, D.\\,T.\\ (2026). Can foundation models manage risk? Zero-shot VaR and ES "
        "forecasting with conformal calibration in CEE markets. \\textit{Economic Computation and Economic Cybernetics Studies and Research}, 60(2), 267--290. "
        "\\href{https://doi.org/10.24818/18423264/60.2.26.14}{doi:10.24818/18423264/60.2.26.14}",
        "Kingma, D.\\,P.\\ \\& Ba, J.\\ (2015). Adam: A method for stochastic optimization. \\textit{International Conference on Learning Representations}. "
        "\\href{https://arxiv.org/abs/1412.6980}{arXiv:1412.6980}",
        "Kuan, C.-M.\\ (2026). Large-scale multiple inequality testing without data snooping bias. Keynote, AIDA Conference, Bucharest University of "
        "Economic Studies, 4 June 2026. \\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/kuan_multiple_inequality_testing.pdf}{github.com/danpele/EMQA/resources/aida2026}",
        "Lago, J., De Ridder, F.\\ \\& De Schutter, B.\\ (2018). Forecasting spot electricity prices: Deep learning approaches and empirical comparison of "
        "traditional algorithms. \\textit{Applied Energy}, 221, 386--405. \\href{https://doi.org/10.1016/j.apenergy.2018.02.069}{doi:10.1016/j.apenergy.2018.02.069}",
        "Lago, J., Marcjasz, G., De Schutter, B.\\ \\& Weron, R.\\ (2021). Forecasting day-ahead electricity prices: A review of "
        "state-of-the-art algorithms, best practices and an open-access benchmark. \\textit{Applied Energy}, 293, 116983. "
        "\\href{https://doi.org/10.1016/j.apenergy.2021.116983}{doi:10.1016/j.apenergy.2021.116983}",
        "Lundberg, S.\\,M., Erion, G., Chen, H.\\ et al.\\ (2020). From local explanations to global understanding with explainable AI for trees. "
        "\\textit{Nature Machine Intelligence}, 2(1), 56--67. \\href{https://doi.org/10.1038/s42256-019-0138-9}{doi:10.1038/s42256-019-0138-9}",
        "Marcjasz, G., Narajewski, M., Weron, R.\\ \\& Ziel, F.\\ (2023). Distributional neural networks for electricity price forecasting. "
        "\\textit{Energy Economics}, 125, 106843. \\href{https://doi.org/10.1016/j.eneco.2023.106843}{doi:10.1016/j.eneco.2023.106843}",
        "Murphy, A.\\,H.\\ (1977). The value of climatological, categorical and probabilistic forecasts in the cost-loss ratio situation. "
        "\\textit{Monthly Weather Review}, 105(7), 803--816. \\href{https://doi.org/10.1175/1520-0493(1977)105<0803:TVOCCA>2.0.CO;2}{doi:10.1175/1520-0493(1977)105\\allowbreak<0803:TVOCCA>2.0.CO;2}",
        "Olivares, K.\\,G., Challu, C., Marcjasz, G., Weron, R.\\ \\& Dubrawski, A.\\ (2023). Neural basis expansion analysis with exogenous variables: "
        "Forecasting electricity prices with NBEATSx. \\textit{International Journal of Forecasting}, 39(2), 884--900. "
        "\\href{https://doi.org/10.1016/j.ijforecast.2022.03.001}{doi:10.1016/j.ijforecast.2022.03.001}",
        "Romano, J.\\,P.\\ \\& Wolf, M.\\ (2005). Stepwise multiple testing as formalized data snooping. \\textit{Econometrica}, 73(4), 1237--1282. "
        "\\href{https://doi.org/10.1111/j.1468-0262.2005.00615.x}{doi:10.1111/j.1468-0262.2005.00615.x}",
        "Shapley, L.\\,S.\\ (1953). A value for n-person games. In \\textit{Contributions to the Theory of Games II}, 307--317. Princeton University Press. "
        "\\href{https://doi.org/10.1515/9781400881970-018}{doi:10.1515/9781400881970-018}",
        "Srivastava, N., Hinton, G., Krizhevsky, A., Sutskever, I.\\ \\& Salakhutdinov, R.\\ (2014). Dropout: A simple way to prevent neural networks "
        "from overfitting. \\textit{Journal of Machine Learning Research}, 15, 1929--1958. \\href{https://jmlr.org/papers/v15/srivastava14a.html}{jmlr.org/papers/v15/srivastava14a.html}",
        "Weron, R.\\ (2014). Electricity price forecasting: A review of the state-of-the-art with a look into the future. "
        "\\textit{International Journal of Forecasting}, 30(4), 1030--1081. \\href{https://doi.org/10.1016/j.ijforecast.2014.08.008}{doi:10.1016/j.ijforecast.2014.08.008}",
        "Weron, R.\\ (2026). Machine learning for electricity price forecasting. Keynote, AIDA Conference, Bucharest University of Economic "
        "Studies, 4 June 2026. \\href{https://github.com/danpele/EMQA/blob/main/resources/aida2026/weron_ml_electricity_price_forecasting.pdf}{github.com/danpele/EMQA/resources/aida2026}",
        "White, H.\\ (2000). A reality check for data snooping. \\textit{Econometrica}, 68(5), 1097--1126. "
        "\\href{https://doi.org/10.1111/1468-0262.00152}{doi:10.1111/1468-0262.00152}",
    ]
    for part, (a_, b_) in enumerate([(0, 9), (9, 18), (18, 27), (27, len(REFS))]):
        D.frame(t("References", "Bibliografie") + f" ({part + 1}/4)", "\\begin{itemize}\\setlength{\\itemsep}{1pt}\\scriptsize\n" +
                "\n".join("\\item " + r for r in REFS[a_:b_]) + "\n\\end{itemize}", "scriptsize")

    # ------------------------------------------------------------------ appendix
    D.mark_main_end()
    D.parts.append("\\section*{" + t("Appendix", "Anexă") + "}\n")
    D.frame(t("Appendix A: back-propagation and the Adam update", "Anexa A: propagarea înapoi a erorii și pasul Adam"), cols(
        "\\[ \\frac{\\partial\\mathcal L}{\\partial W_2}=\\boldsymbol\\delta\\,\\mathbf z^{\\top},\\quad \\boldsymbol\\delta=\\frac{\\partial\\mathcal L}{\\partial\\hat{\\mathbf Y}} \\]"
        "\\[ \\frac{\\partial\\mathcal L}{\\partial W_1}=\\big[(W_2^{\\top}\\boldsymbol\\delta)\\odot\\phi'(\\mathbf u)\\big]\\mathbf x^{\\top} \\]" + it(
            t("Chain rule, from the output back to the inputs; for the absolute error $\\partial|y-\\hat y|/\\partial\\hat y=-\\operatorname{sign}(y-\\hat y)$.",
              "Regula de derivare a funcțiilor compuse, de la ieșire spre intrări; pentru eroarea absolută, $\\partial|y-\\hat y|/\\partial\\hat y=-\\operatorname{sign}(y-\\hat y)$."),
            t("$\\mathbf u=W_1\\mathbf x+\\mathbf b_1$; $\\odot$ = element-wise product; for softplus, $\\phi'(u)=1/(1+e^{-u})$.", "$\\mathbf u=W_1\\mathbf x+\\mathbf b_1$; $\\odot$ = produs element cu element; pentru softplus, $\\phi'(u)=1/(1+e^{-u})$."), sep="3pt"),
        "\\[ m_k=\\beta_1m_{k-1}+(1-\\beta_1)g_k \\]\\[ v_k=\\beta_2v_{k-1}+(1-\\beta_2)g_k^2 \\]"
        "\\[ \\theta_k=\\theta_{k-1}-\\eta\\,\\frac{m_k/(1-\\beta_1^k)}{\\sqrt{v_k/(1-\\beta_2^k)}+\\varepsilon} \\]" + it(
            t("$g_k$ = gradient on mini-batch $k$; $\\beta_1=0.9$, $\\beta_2=0.999$, $\\varepsilon=10^{-8}$ (defaults); each weight gets its own step size.",
              "$g_k$ = gradientul pe grupul de zile $k$; $\\beta_1=0{,}9$, $\\beta_2=0{,}999$, $\\varepsilon=10^{-8}$ (valori implicite); fiecare pondere are propriul pas."),
            t("Weight decay adds $\\lambda\\theta$ to $g_k$ (a quadratic penalty, here $\\lambda$ = " + sci(N['search']['dnn']['cfg']['wd']) + ").",
              "Penalizarea ponderilor adaugă $\\lambda\\theta$ la $g_k$ (o penalizare pătratică, aici $\\lambda$ = " + sci(N['search']['dnn']['cfg']['wd']) + ")."), sep="3pt"), "0.50", "0.47"), "small",
        cite="(Kingma \\& Ba, 2015, ICLR; Hastie et al., 2009)")

    D.frame(t("Appendix B: why the optimal leaf value is $-G/(H+\\lambda)$", "Anexa B: de ce valoarea optimă a unei frunze este $-G/(H+\\lambda)$"), cols(
        "\\[ \\ell\\big(Y_i,F_{m-1}+f\\big)\\approx\\ell_i+g_i f(\\mathbf x_i)+\\tfrac12h_i f(\\mathbf x_i)^2 \\]"
        "\\[ \\sum_{j}\\Big[G_jw_j+\\tfrac12(H_j+\\lambda)w_j^2\\Big]+\\gamma J,\\quad G_j=\\textstyle\\sum_{i\\in R_j}g_i \\]"
        "\\[ w_j^{*}=-\\frac{G_j}{H_j+\\lambda},\\qquad \\text{" + t("score", "scor") + "}=-\\tfrac12\\sum_j\\frac{G_j^2}{H_j+\\lambda}+\\gamma J \\]",
        it(t("Second-order Taylor expansion of the loss around the current forecast; $g_i$, $h_i$ = first and second derivatives; $H_j$ = sum of $h_i$ in leaf $j$.",
             "Dezvoltare Taylor de ordinul doi a funcției de pierdere în jurul prognozei curente; $g_i$, $h_i$ = derivatele de ordinul întîi și al doilea; $H_j$ = suma $h_i$ din frunza $j$."),
           t("Within a leaf the objective is a parabola in $w_j$: setting its derivative to zero gives $w_j^*$.",
             "În fiecare frunză, obiectivul este o parabolă în $w_j$: anulînd derivata, se obține $w_j^*$."),
           t("The split gain of the regression-tree slide is the score before the split minus the score after it.",
             "Cîștigul unei împărțiri, de pe diapozitivul despre arborele de regresie, este scorul dinainte minus scorul de după împărțire."),
           t("For the absolute error $h_i=0$; XGBoost then sets the leaf values by a line search.",
             "Pentru eroarea absolută, $h_i=0$; XGBoost calculează atunci valorile frunzelor printr-o căutare unidimensională."), sep="3pt"), "0.52", "0.45"), "small",
        cite="(Chen \\& Guestrin, 2016, KDD)")

    D.frame(t("Appendix C: SHAP values in EUR/MWh", "Anexa C: valori SHAP exprimate în EUR/MWh"), cols(
        "\\[ \\hat P=m+s\\,\\sinh\\Big(\\phi_0+\\textstyle\\sum_j\\phi_j\\Big),\\qquad P_0=m+s\\,\\sinh\\phi_0 \\]"
        "\\[ \\phi_j^{\\text{EUR}}=\\phi_j\\,\\frac{\\hat P-P_0}{\\sum_k\\phi_k}\\ \\Rightarrow\\ \\sum_j\\phi_j^{\\text{EUR}}=\\hat P-P_0 \\]",
        it(t("The trees forecast the asinh-scaled price; $m$, $s$ = median and scaled median absolute deviation (MAD) of the training prices.",
             "Arborii prognozează prețul transformat cu asinh; $m$, $s$ = mediana și abaterea absolută mediană (MAD), scalată, a prețurilor de antrenare."),
           t("SHAP values add up on that scale; to report euros, the euro gap $\\hat P-P_0$ is shared in proportion to $\\phi_j$.",
             "Valorile SHAP se adună pe această scară; pentru a raporta în euro, diferența $\\hat P-P_0$ se împarte proporțional cu $\\phi_j$."),
           t("Signs and ranking are unchanged; the contributions add up exactly to the forecast in EUR/MWh.",
             "Semnele și ordinea nu se schimbă; contribuțiile se adună exact la prognoza în EUR/MWh."), sep="3pt"), "0.50", "0.47"), "small",
        cite="(Lundberg et al., 2020, Nat.\\ Mach.\\ Intell.)")

    sd, sx = N["search"]["dnn"]["cfg"], N["search"]["xgb"]["cfg"]
    yes, no = t("yes", "da"), t("no", "nu")
    D.frame(t("Appendix D: search spaces and the chosen settings", "Anexa D: spațiile de căutare și setările alese"), cols(
        table("@{}llr@{}", [t("DNN setting", "Setare DNN"), t("Values tried", "Valori încercate"), t("Chosen", "Aleasă")], [
            [t("neurons, layer 1", "neuroni, stratul 1"), "64, 128, 256, 512", str(sd["n1"])],
            [t("neurons, layer 2", "neuroni, stratul 2"), "0, 32, 64, 128, 256", t("none", "niciunul") if sd["n2"] == 0 else str(sd["n2"])],
            [t("activation", "funcția de activare"), "ReLU, softplus", sd["act"].replace("relu", "ReLU")],
            ["dropout", "; ".join(n(x, ".1f") for x in (0.0, 0.1, 0.2, 0.3)), n(sd["drop"], ".1f")],
            [t("learning rate", "rata de învățare"), "; ".join(sci(x) for x in (3e-4, 1e-3, 3e-3)), sci(sd["lr"])],
            [t("L1 penalty, inputs", "penalizare L1, intrări"), "; ".join(sci(x) for x in (0, 1e-3, 1e-2, 1e-1)), sci(sd["l1"])],
            [t("batch (days)", "grup (zile)"), "32, 64, 128", str(sd["batch"])],
            [t("load/RES/fund.", "consum/RES/fund."), t("yes or no", "da sau nu"),
             "/".join(yes if sd[k] else no for k in ["load", "res", "fund"])]], size="scriptsize", stretch="1.05"),
        table("@{}llr@{}", [t("XGBoost setting", "Setare XGBoost"), t("Values tried", "Valori încercate"), t("Chosen", "Aleasă")], [
            [t("trees", "arbori"), "300, 600, 1000, 1500", str(sx["n_est"])],
            [t("learning rate $\\eta$", "rata de învățare $\\eta$"), "; ".join(n(x, ".2f") for x in (0.02, 0.05, 0.1)), n(sx["eta"], ".2f")],
            [t("depth", "adîncimea"), "3, 4, 5, 6, 8", str(sx["depth"])],
            [t("min.\\ leaf weight", "ponderea min.\\ în frunză"), "1, 5, 20, 50", str(sx["mcw"])],
            [t("rows per tree", "rînduri pe arbore"), "; ".join(n(x, ".1f") for x in (0.6, 0.8, 1.0)), n(sx["sub"], ".1f")],
            ["$\\lambda$", "; ".join(n(x, ".1f") for x in (0.1, 1.0, 10.0)), n(sx["lam"], ".1f")],
            [t("loss", "funcția de pierdere"), t("square, abs., Huber", "pătrat, abs., Huber"), t("absolute", "absolută")]],
            size="scriptsize", stretch="1.05"), "0.49", "0.49") +
        note(t("24 random draws per model (fixed seed) + the Lecture 2 setting; chosen = lowest MAE on the validation year.",
               "24 de extrageri aleatoare pe model (cu valoare inițială fixată) și setarea din cursul 2; aleasă = MAE minimă în anul de validare.")),
        "small", cite="(Bergstra \\& Bengio, 2012, JMLR)")
    return D


def main(langs):
    ok = True
    for lang in langs:
        name = "lecture7" if lang == "en" else "lecture7_ro"
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
