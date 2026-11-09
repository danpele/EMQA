# EMQA research case studies / Studii de caz din cercetarea grupului

Energy MBA - Energy Markets Quantitative Analysis (EMQA), Prof. Daniel Traian Pele.
Bucharest University of Economic Studies (ASE) and Romanian Academy, Institute for Economic Forecasting (IPE).

There is one case per lecture. Each case is built on a paper by our group and replicated in simplified form on the course data
(`../data/clean/`, see `../data/SOURCES.md`). All numbers in the briefs labelled "our data" are computed by the notebooks.
Each brief documents the data, period and specification of the classroom implementation.

## Mapping: case, lecture, paper, files

| Case | Lecture | Paper (full citation) | Text used |
|---|---|---|---|
| C1 `C1_crisis_2024/` | L1 Markets & data | Andrei, A.-V., Pele, D.-T. & Cramer, A.-A. (2026). Evaluating intervention effectiveness during extreme price events: A counterfactual analysis of Romania's 2024 energy crisis. *Proceedings of the International Conference on Business Excellence*, 20(1), 84-103. [doi:10.2478/picbe-2026-0013](https://doi.org/10.2478/picbe-2026-0013) | Full text (published, open access) |
| C2 `C2_load_forecasting/` | L2 Forecasting | Proșcanu, C. A., Proșcanu, M. E., Pele, D. T. & Costea, A. (2025). Watt's next? Benchmarking time series models on Romania's national electricity consumption. *Romanian Journal of Economic Forecasting*, 28(3), 146-163. [RePEc:rjr:romjef:v::y:2025:i:3:p:146-163](https://EconPapers.repec.org/RePEc:rjr:romjef:v::y:2025:i:3:p:146-163) | Full text (published, open access) |
| C3 `C3_energy_stocks/` | L3 Volatility | Grecu, R. A., Cramer, A. A., Pele, D. T. & Lessmann, S. (2025). The link between energy prices and stock markets in European Union countries. *The North American Journal of Economics and Finance*, 78, 102420. [doi:10.1016/j.najef.2025.102420](https://doi.org/10.1016/j.najef.2025.102420) | Full text of the authors' revised manuscript (section/table numbers); the published version is open access (CC BY) |
| C4 `C4_risk_meter/` | L4 Risk for energy companies | Toma, F.-M., Dima, D.-M., Grecu, R., Pele, D. T. & Lessmann, S. (2026). Energy Financial Risk Meter: Systemic risk in the EU energy sector. SSRN Working Paper 6985301. [doi:10.2139/ssrn.6985301](https://doi.org/10.2139/ssrn.6985301) | Full text (authors' LaTeX source, version of 24 May 2026) |
| C5 `C5_demand_elasticity/` | L5 Derivatives & hedging (incl. PPAs) | Proșcanu, C., Proșcanu, M. & Pele, D. T. (2025). The price elasticity of electricity demand in Romania. *Journal of Social and Economic Statistics*, 14(2), 131-141. [doi:10.2478/jses-2025-0009](https://doi.org/10.2478/jses-2025-0009) | Full text (published, open access) |
| C6 `C6_battery_arbitrage/` | L6 Renewables, storage, flexibility | Andrei, A.-V., Cepoi, C. O., Dumitrescu, B. A., Lessmann, S., Chiriac (Luchian), A.-C., Pele, D. T. & Petukhina, A. (2026). Joint probabilistic forecasting for battery arbitrage in day-ahead power markets. SSRN Working Paper 6872381. [doi:10.2139/ssrn.6872381](https://doi.org/10.2139/ssrn.6872381) | Full text (authors' LaTeX source) |
| C7 `C7_spike_early_warning/` | L7 ML & foundation models | Andrei, A.-V., Pele, D.-T., Cramer, A.-A., Amza, A. & Diaconu, D. (2026). Explainable AI-based early warning system for electricity price spikes: Evidence from the Romanian market. *Proceedings of the International Conference on Business Excellence*, 20(1), 4820-4836. [doi:10.2478/picbe-2026-0352](https://doi.org/10.2478/picbe-2026-0352) | Full text (published, open access) |

Papers cited only as pointers inside the briefs, not replicated:

- **C1.** Andrei et al. (2026), PICBE, [doi:10.2478/picbe-2026-0014](https://doi.org/10.2478/picbe-2026-0014) (multi-horizon explainability) is already on the L1 research slide.
- **C2.** Andrei, Velev, Toma, Pele & Lessmann (2024), *Energy price modelling: A comparative evaluation of four generations of forecasting methods*, [arXiv:2411.03372](https://arxiv.org/abs/2411.03372). Full text was read; it is a candidate for an extra L2/L7 exercise.
- **C5.** Shahar, Lessmann & Pele (2025), *Causality analysis of electricity market liberalization on electricity price using novel machine learning methods*, [arXiv:2507.12331](https://arxiv.org/abs/2507.12331). Full text was read; it is cited in the C5 brief as complementary research on market design.
- **C6.** Basangova, Bolovăneanu, Conda, Pele et al. (2026), *Day-ahead forecasting for redispatch measures using machine learning models*, SSRN 7511080, [doi:10.2139/ssrn.7511080](https://doi.org/10.2139/ssrn.7511080). Full text (draft of 3 July 2026) was read.
- **C7.**
  - Jheng, Tak, Găman, Mazurencu-Marinescu-Pele & Pele (2026), *Can foundation models manage risk? Zero-shot VaR and ES forecasting with conformal calibration in CEE markets*, *Economic Computation and Economic Cybernetics Studies and Research*, 60(2), 267-290, [doi:10.24818/18423264/60.2.26.14](https://doi.org/10.24818/18423264/60.2.26.14). Full text was read; it is a one-line pointer, as requested.
  - The battery paper (C6, [doi:10.2139/ssrn.6872381](https://doi.org/10.2139/ssrn.6872381)) is cited for probabilistic forecasting with random forests.
- **Further reading.** *Finite-Sample Precision Limits for Expected Shortfall Forecast Comparisons* (Mathematics, 2026, [doi:10.3390/math14132316](https://doi.org/10.3390/math14132316)) addresses forecast evaluation in financial risk management; the seven cases focus on energy-market decisions.

## Files in each case folder `Cx_*/`

| File | Content |
|---|---|
| `Cx_case_EN.pdf`, `Cx_case_RO.pdf` | The case brief (question, paper, method, replication with figures and tables, 5 discussion questions, limitations of the classroom replication), followed by a one-page summary of the case. |
| `Cx_brief.tex` | One LaTeX source for both languages (`\T{EN}{RO}`). `Cx_case_EN.tex` and `Cx_case_RO.tex` are the wrappers. |
| `Cx_notebook_EN.ipynb`, `Cx_notebook_RO.ipynb` | The simplified replication, end to end. The code is the same in both; the RO notebook has Romanian text and shows the Romanian charts. Both are executed. |
| `nb_spec.py` | The source of the two notebooks (cells in EN and RO). Edit this file, not the notebooks. |
| `fig/en/*.pdf`, `fig/ro/*.pdf` | All charts, with English and Romanian labels. Transparent background, legend at the bottom. |
| `fig_headline_en.pdf`, `fig_headline_ro.pdf` | One headline chart for the lecture slide. |
| `slide_summary_en.tex`, `slide_summary_ro.tex` | Up to 6 bullet lines for the lecture box "Research from our group". |
| `numbers.json`, `numbers_en.tex`, `numbers_ro.tex`, `tab_*_{en,ro}.tex` | Numbers and tables written by the notebook and read by the brief (decimal comma in RO). |

Shared code is in `common/`:

- `case_utils.py`: chart style, palette, loaders, number and table writers.
- `make_notebooks.py`: builds and executes the two notebooks of a case.
- `build_briefs.py`: compiles the PDFs.
- `case_preamble.tex`: the LaTeX preamble.

## Rebuild

```bash
cd repo/cases
python common/make_notebooks.py C1_crisis_2024     # builds + executes C1_notebook_EN/RO.ipynb, writes figures, numbers and tables
python common/build_briefs.py C1_crisis_2024       # compiles C1_case_EN.pdf and C1_case_RO.pdf (no argument = all cases)
```

Run times on a laptop:

- **C2** about 15 minutes (SARIMA re-filtering, Chronos).
- **C6** about 10 minutes (rolling forests).
- **All other cases** 1-3 minutes each.

C2 uses the `chronos-forecasting` package and downloads the `amazon/chronos-bolt-small` weights once. If either is missing, the cell is skipped and the rest of the notebook still runs. C7 needs `xgboost` and `shap`.

## Data caveats common to all cases

- **Forecasts versus actuals.** Load, solar and wind are *actual* values (energy-charts.info, from ENTSO-E), not the day-ahead forecasts used in several papers. This gives the models perfect foresight on fundamentals.
- **TTF gas.** Only a monthly series is available (World Bank).
- **Romanian equities.** The data cover four energy companies only: SNP, SNG, SNN, and H2O from 2023. There is no BET index.
- **15-minute prices.** Since October 2025 the day-ahead market uses 15-minute products. These prices are averaged to hours.
