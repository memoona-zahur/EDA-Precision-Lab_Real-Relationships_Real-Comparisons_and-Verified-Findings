# EDA Precision Lab — Real Relationships, Real Comparisons, and Verified Findings

Week 06 · Day 1. A precision-focused lab closing the gaps from Friday's
assessment (relationship vs. comparison charts, correlations computed *not*
eyeballed, layout QA on saved files, self-audited numbers). Includes the full
submission-quality Capstone report.

## Repository contents

| File | Purpose |
|---|---|
| `week6_day1_precision_lab.ipynb` | **Kata notebook** — Parts A–E, tasks 1–13 (the practice exercises, including intentional anti-patterns to build and fix). |
| `week6_day1_capstone_report.ipynb` | **Capstone** — a single, standalone, submission-quality EDA Precision Report. |
| `generate_data.py` | Dataset generator (exact assignment spec, `seed=21`). |
| `data/students.csv` | 600 × 6 students dataset produced by the generator. |
| `charts/` | All 15 saved PNG figures from both notebooks. |
| `test_precision_checks.py` | 37-check automated verification suite (dataset, statistics, PNG validity, layout-collision QA, notebook cleanliness). |
| `technical_summary.md` | Plain-language write-up for a non-technical reader. |
| `SELF_REVIEW.md` | Requirement-by-requirement verification of the whole lab. |
| `requirements.txt` | Pinned Python dependencies. |

## How to run

```bash
pip3 install -r requirements.txt
python3 generate_data.py            # (re)create data/students.csv
python3 test_precision_checks.py    # run the 37-check verification suite
jupyter notebook                    # open the two notebooks
```

Both notebooks survive **Restart Kernel & Run All** with zero error cells.

## Verified findings (recomputed from `students.csv`)

| # | Finding | Statistic | Status |
|---|---|---|---|
| 1 | Weekly study hours associated with higher exam scores | Pearson r = 0.689 (p = 8.1e-86), slope ≈ 2.1 pts/hr | Verified ✓ |
| 2 | Nightly sleep hours show no relationship with scores | Pearson r = −0.022 (p = 0.596) — genuine null | Verified ✓ |
| 3 | Section C outscores A (comparison chart) | mean C − mean A = 3.8 pts | Verified ✓ |
| 4 | A-vs-C gap is real, not noise (bootstrap) | 95% CI for mean A − C = [−5.68, −1.80], **excludes 0** | Verified ✓ |
| 5 | Study-hours relationship is essentially linear | Pearson 0.6895 vs Spearman 0.7010; \|diff\| = 0.012 | Verified ✓ |
| 6 | Study-hours relationship consistent across sections | r ≈ 0.68 / 0.71 / 0.69 (A/B/C) | Verified ✓ |

*All findings are produced by `f-string`s from live variables, never hand-typed,
and re-verified in each notebook's self-audit table and in
`test_precision_checks.py`.*

## Reading the notebooks as a report

Both notebooks are written as **narrative reports, not just code**. Every chart
section follows the same pattern (mirroring the reference `eda-precision-lab`
repo):

> **Question:** the specific question the chart answers
>
> ...the chart (built, saved, reopened)...
>
> **What this tells us:** the narrative finding in prose

You can read only the `##` section headers and the **"What this tells us"**
paragraphs to get the full findings without ever looking at a chart or the code.
Every number in those findings is produced by the code cell above it (never
hand-typed) and is re-verified in each notebook's self-audit table (Section 9 in
the Capstone, Step 8 in the kata notebook).

## Why two notebooks?

- **Kata notebook** — the deliberate practice: build the line-chart trap, break
  the chart layout and fix it, draw arbitrary colors and then a deliberate one,
  self-audit the numbers. It intentionally contains anti-patterns so you can see
  and fix them.
- **Capstone** — the standalone report. The assignment asks for "a single,
  complete, submission-quality notebook that stands on its own — assume a reader
  sees only this notebook, not today's kata cells," so it excludes the
  intentionally-broken examples and presents only the clean, final analysis.
