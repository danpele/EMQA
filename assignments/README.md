# EMQA assignments (Energy MBA)

| Assignment | Lectures | Brief (EN / RO) | Starter notebook (EN / RO) |
|---|---|---|---|
| 1. Forecasting the Romanian day-ahead price for a bidding desk | 1-3 | `A1/A1_brief_EN.pdf`, `A1/A1_brief_RO.pdf` | `A1/A1_starter_EN.ipynb`, `A1/A1_starter_RO.ipynb` |
| 2. Risk, contracts and forecast-driven decisions for your role | 4-7 | `A2/A2_brief_EN.pdf`, `A2/A2_brief_RO.pdf` | `A2/A2_starter_EN.ipynb`, `A2/A2_starter_RO.ipynb` |

Personal parameters (test window, hours, settings, reconciliation days) come from your student ID:

```
python make_assignment.py --id <ID> --assignment 1
python make_assignment.py --id <ID> --assignment 2 --role B      # B, H, R or S
```

`emqa_assign.py` loads the course data (`../data/clean`) and provides `params`, `panel`, `day_matrix`,
`quarter_hours`, `daily_prices`, `ttf_monthly`, `eua_daily`, `leakage_check` (gate-closure information set), `selection_check`
(Assignment 2: no choice on the test window), `data_version`, `latest_window`.
It contains no models.

Sources: one LaTeX body per assignment (`A?/A?_brief.tex`, text written as `\T{English}{Romanian}`),
compiled through `A?_brief_EN.tex` / `A?_brief_RO.tex` with `common/assign_preamble.tex`.
The starters are generated in both languages by `_build_starters.py`.
