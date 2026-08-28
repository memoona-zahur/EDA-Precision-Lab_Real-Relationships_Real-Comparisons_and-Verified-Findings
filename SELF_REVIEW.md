# SELF_REVIEW — EDA Precision Lab (Week 06 · Day 1)

Requirement-by-requirement check of every today-task item against the actual
delivered artifacts. Verification source: `test_precision_checks.py`
(37 checks passing) plus notebook output inspection.

## Today's tasks

| # | Task | Delivered where | Verified |
|---|---|---|---|
| 1 | Dataset generated from exact spec, unmodified | `generate_data.py` → `data/students.csv` | ✓ (600 rows, all ranges, no dupes/missing; seed=21) |
| 2 | Real relationship chart (study hours) + r + finding | Kata 2 & Capstone §3 | ✓ r = 0.689, slope 2.1 |
| 3 | Null relationship chart (sleep) + r + null finding | Kata 3 & Capstone §4 | ✓ r = −0.022, written up |
| 4 | Comparison chart (by section) + shuffle-test justification | Kata 4 & Capstone §5 | ✓ |
| 5 | Line-chart trap built, false impression named | Kata 5 | ✓ (PNG + text) |
| 6 | Layout collision built, confirmed in PNG, fixed | Kata 6 (+ bbox QA in tests) | ✓ broken overlaps / fixed doesn't |
| 7 | Deliberate color, natural category order | Kata 7 | ✓ arbitrary vs single-hue, A/B/C kept |
| 8 | Self-audit table (steps 2–4 numbers) | Kata 8 | ✓ all claimed = recomputed |
| 9 | Confound named, finding rewritten correlational | Kata 9 & Capstone §7 | ✓ |
| 10 | Pearson & Spearman side by side | Kata 10 & Capstone §6 | ✓ close (0.6895 / 0.7010) |
| 11 | Bootstrap 95% CI, zero-inclusion stated | Kata 11 & Capstone §5 | ✓ [−5.68, −1.80] excludes 0 |
| 12 | Small multiples (3 panels) + interpretation | Kata 12 & Capstone §8 | ✓ consistent (0.68/0.71/0.69) |
| 13 | Full pre-submission checklist run | Kata 13 | ✓ every item addressed |
| — | **Capstone** report end-to-end, clean on Restart & Run All | `week6_day1_capstone_report.ipynb` | ✓ zero error cells |

## Capstone required content (in order)

| Requirement | Present? | Notes |
|---|---|---|
| Diagnosis of the dataset (standard checks) | ✓ | types, missing, dupes, ranges, balance |
| Both relationship charts + Pearson, incl. the null | ✓ | study (0.689) and sleep (−0.022) findings |
| Comparison chart + bootstrap 95% CI + zero-inclusion statement | ✓ | CI [−5.68, −1.80] rules out "no real difference" |
| Spearman-vs-Pearson comparison, stated & interpreted | ✓ | close → linear assumption OK |
| Small-multiples figure + interpretation | ✓ | consistent across sections |
| Correlation-vs-causation caveat naming a real confound | ✓ | motivation / prior prep |
| Visual QA pass (every chart opened as saved file, tight_layout) | ✓ | all figures use `layout="constrained"`; saved PNGs reopened; collision pair bbox-verified |
| Self-audit table covering every stated number | ✓ | all value = recomputed |
| Non-technical summary + honest limitation | ✓ | `technical_summary.md` + Capstone §10 |
| Survives Restart Kernel & Run All | ✓ | both notebooks re-executed clean (EXIT=0, zero error cells) |

## Pre-submission checklist (Lesson 11) applied

1. Chart type justified (shuffle test) — ✓ every relationship & comparison chart
2. Every chart's result, incl. null, in the write-up — ✓ sleep r written up
3. Saved PNG opens clean, no overlaps — ✓ (broken→fixed in Kata 6; bbox-verified)
4. Color & category order deliberate — ✓ single deliberate hue, A/B/C order
5. Every number matches fresh computation — ✓ self-audit tables + 37-check suite
6. Comparison claims backed by a CI — ✓ bootstrap CI
7. No unsupported causal wording — ✓ rewritten as correlational; "causes" removed

## Verification suite

`test_precision_checks.py` — **37/37 passing**:
- dataset shape, ranges, missing/duplicates
- correlation ranges (study 0.55–0.80, sleep near 0)
- Pearson/Spearman closeness
- bootstrap CI excludes zero
- all 15 PNGs valid (magic bytes)
- collision broken/fixed are distinct; broken *overlaps*, fixed *doesn't* (bbox)
- arbitrary vs deliberate color charts distinct
- both notebooks contain zero error cells (Restart & Run All)
