# EMQA lecture pipeline

Every lecture of *Energy Markets Quantitative Analysis* is built the same way, in English and Romanian, from
one analysis script and one builder. Lecture 1 (`L1/`) is the reference implementation; copy its structure
for L2–L7.

```
data/clean/*.csv                 real downloaded series (data/download_all.py, documented in data/SOURCES.md)
        │
lectures/Lk/analysis_Lk.py       ALL computation  ──►  Lk_numbers.json          (every number shown anywhere)
        │                                         ──►  charts/en/*.pdf, charts/ro/*.pdf
lectures/Lk/build_Lk.py          slide text only (EN+RO), numbers as @{key}
        │                                         ──►  lecturek.tex, lecturek_ro.tex  ──►  lecturek.pdf, lecturek_ro.pdf
lectures/Lk/make_notebook_Lk.py  student notebooks ──►  notebooks/Lk_notebook.ipynb, notebooks/Lk_notebook_ro.ipynb (executed)
```

Run from the repository root:

```bash
python3 lectures/L1/analysis_L1.py        # numbers JSON + both chart sets
python3 lectures/L1/build_L1.py           # both decks; "en" or "ro" builds one
python3 lectures/L1/make_notebook_L1.py   # both notebooks, executed end to end
```

`build_Lk.py` exits with an error unless both decks compile with **0 LaTeX errors and no overfull box
> 1 pt** (never hide them with `\hfuzz`, `\vfuzz` or `\hbadness`). Figures are requested large and
`emqa_build.autofit` recompiles, shrinking only the figures of frames that overflow, until the deck fits — so every
figure ends as large as its frame allows. If a figure ends small, cut text on that frame (one message per frame). It also prints, per language, the
acronym audits and writes `lecturek[_ro]_contact_sheet.png`, which must be checked frame by frame.

## Shared files (`lectures/common/`)

| File | Role |
|---|---|
| `emqa_preamble.tex` | Beamer theme, colours, title page with ASE + Romanian Academy (IPE) affiliations and logos, header/footer, recurring section outline, teaching macros (`\intuition`, `\where`, `\manager`, `\tryit`, `\chartsource`, `\simlabel`). Language labels default to English; `\emqaromanian` switches them. Loaded with `\input{../common/emqa_preamble}`; no bibliography package is used (references are an itemised list, so there is no `\bibsep` problem). |
| `emqa_build.py` | `Numbers` (reads the JSON, renders `@{key|fmt}` placeholders; a missing key is an error), `Deck` (frames, sections, `concept`, `chart`, `figframe` = intuition + one equation + one large figure + ≤3 bullets, quizzes, appendix), `table`, `heat`/`seq` colour cells, `compile_tex` (reports overflows by frame title), `autofit`, `acronym_audit`, `first_use_audit`, `contact_sheet`. |
| `emqa_plot.py` | Chart style (transparent background, no grid, legend at the bottom outside the axes, fixed colour per bidding zone) and data loaders with paths relative to the repository. |
| `logos/` | Logos used on the title page. |

## Rules every lecture follows

1. **Real data only.** No invented numbers, no fictional companies. A simulation is allowed only to teach a
   concept, at most once per lecture, and is labelled `\simlabel` on the slide.
2. **No hand-typed results.** Slide text contains placeholders such as `@{cy.mean.RO|.2f}`, `@{neg.ro_first|date}`,
   `@{tails.vol_max_date|ym}`, `@{spikes.ro_max_ts|dt}`. Hand-typed numbers are limited to definitions (1.96, 1/24,
   15 min, conversion factors, tabulated critical values) and institutional dates (market milestones), each with
   its source on the slide or in the references.
3. **Data conventions.** Cut-off = last complete month (stated on the data slide and in chart captions); missing
   values stay missing, never interpolated or counted as zero, and coverage is reported; energy = sum of mean MW ×
   interval length over reported intervals; daily statistics on the CET/CEST delivery day; daily differences on the
   full calendar (no multi-day jumps); counts of events in hour-equivalents (a 15-min MTU = 0.25 h); quantiles over
   mixed 60/15-min periods are duration-weighted.
4. **Frame types.** *Concept frames* (`Deck.concept`): one-sentence intuition → formula with every symbol defined
   (underbraces naming the blocks) → real-data example → one "On the job" line tied to a decision of the students
   (supplier, trader, hydro/nuclear producer, Transelectrica, industrial consumer, battery developer). *Chart frames*
   (`Deck.chart`): claim title, large figure, source + data period under it, one or two bullets, job line.
   Every frame title is a short claim; the line under it is the precise citation; "Experiment yourself" points to the
   notebook section (§) that reproduces the frame.
5. **Language.** One builder, two decks: every string is `t(english, romanian)`. Romanian: „sînt”, î inside words
   (â only in *român*, *România*), decimal comma (handled by `Numbers`), „de” after counts ending in 20–99 or 00
   (helper `de(key)`), Romanian term with the English one in parentheses at first use.
6. **Acronyms.** Each acronym appears in the Abbreviations frames and is spelled out at first use as
   `full name (ACR)`; `build_Lk.py` fails the audit otherwise (math symbols and citation lines are exempt).
7. **Size.** At most 60 main frames including title and section outlines, at most 5 quiz frames, detailed derivations
   in an appendix after the references. Learning objectives at the start; wrap-up outline, "Research from our group",
   "Further reading and resources" and references at the end. References verified against Crossref/DOI pages.
8. **Charts.** Generated twice (`charts/en`, `charts/ro`) with translated labels; transparent background; legend at the
   bottom outside the plot; no gridlines; one y-axis per panel; colours fixed per entity (`emqa_plot.PAL`). Draw them at
   display size: 6.4 in wide and about 2 in tall, 10–10.5 pt fonts, so text stays legible (≥ 6.5 pt) on the slide; no
   in-chart title that repeats the slide title.
9. **Series pitfalls.** Continuous futures (Brent BZ=F) roll on the first trading day of each month: drop those days from
   return statistics and never report a cross-contract change as a price move. Mean prices are means of signed prices.
   Regressions of trending levels on trending levels are flagged as possibly spurious.

## Starting lecture k

1. Copy `L1/analysis_L1.py`, `L1/build_L1.py`, `L1/make_notebook_L1.py` to `Lk/` and rename.
2. In the analysis script keep section 0 (loading, cut-off) and the `chart()`/`out()` helpers; replace the content.
3. In the builder keep `ABBR`, the front matter and the wrap-up blocks; call `Deck(k, title, V, lang)`.
4. Run the three scripts, fix every overflow and audit message, and check both contact sheets frame by frame.
