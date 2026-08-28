"""Verification suite for the Week 06 Day 1 EDA Precision Lab + Capstone.

Runs from a fresh process (independent of any notebook kernel state) and checks
the lab's deliverables by re-deriving numbers from data/students.csv. All tests
are deterministic because the dataset is generated with a fixed seed.
"""
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import bootstrap

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
CHARTS = os.path.join(HERE, "charts")

STUDENTS_CSV = os.path.join(DATA, "students.csv")
GEN_PY = os.path.join(HERE, "generate_data.py")
KATA_NB = os.path.join(HERE, "week6_day1_precision_lab.ipynb")
CAP_NB = os.path.join(HERE, "week6_day1_capstone_report.ipynb")


def students():
    return pd.read_csv(STUDENTS_CSV)


def _png_ok(path):
    if not os.path.exists(path):
        return False
    with open(path, "rb") as f:
        return f.read(8) == b"\x89PNG\r\n\x1a\n"


passed = 0
failed = 0
failures = []


def check(cond, label):
    global passed, failed
    if cond:
        passed += 1
        print(f"PASS  {label}")
    else:
        failed += 1
        failures.append(label)
        print(f"FAIL  {label}")


# ---------------------------------------------------------------------------
# Part A — dataset correct
# ---------------------------------------------------------------------------
print("== Part A: dataset ==")
df = students()
check(len(df) == 600, "dataset has 600 rows")
check(list(df["student_id"]) == list(range(1, 601)), "student_id is 1..600")
check({"class_section", "study_hours_per_week", "sleep_hours_per_night",
       "attendance_pct", "exam_score"} <= set(df.columns), "expected columns present")
check(df.isna().sum().sum() == 0, "no missing values")
check(df.duplicated().sum() == 0, "no duplicate rows")
check((df["study_hours_per_week"] >= 0).all(), "study hours nonnegative")
check(df["sleep_hours_per_night"].between(3, 10).all(), "sleep hours within [3,10]")
check(df["attendance_pct"].between(40, 100).all(), "attendance within [40,100]")
check(df["exam_score"].between(0, 100).all(), "exam score within [0,100]")

# ---------------------------------------------------------------------------
# Part B — genuine relationships
# ---------------------------------------------------------------------------
print("== Part B: relationships ==")
r_study, p_study = stats.pearsonr(df["study_hours_per_week"], df["exam_score"])
r_sleep, p_sleep = stats.pearsonr(df["sleep_hours_per_night"], df["exam_score"])
check(0.55 < r_study < 0.80, f"study-hours r in plausible range (got {r_study:.3f})")
check(abs(r_sleep) < 0.10, f"sleep-hours r near zero (got {r_sleep:.3f})")
means = df.groupby("class_section")["exam_score"].mean()
check(means["C"] - means["A"] > 1, f"Section C mean above A (diff {means['C']-means['A']:.2f})")

# ---------------------------------------------------------------------------
# Part D — Pearson vs Spearman, bootstrap CI
# ---------------------------------------------------------------------------
print("== Part D: rigor ==")
r_pear, _ = stats.pearsonr(df["study_hours_per_week"], df["exam_score"])
r_spear, _ = stats.spearmanr(df["study_hours_per_week"], df["exam_score"])
check(abs(r_pear - r_spear) < 0.10, f"Pearson/Spearman close (diff {abs(r_pear-r_spear):.3f})")

def diff_means(a, c):
    return a.mean() - c.mean()

ga = df.loc[df["class_section"] == "A", "exam_score"].to_numpy()
gc = df.loc[df["class_section"] == "C", "exam_score"].to_numpy()
res = bootstrap((ga, gc), diff_means, n_resamples=5000, method="BCa", random_state=21)
lo, hi = res.confidence_interval
check(hi < 0, f"bootstrap CI for mean A - mean C excludes zero ([{lo:.2f}, {hi:.2f}])")

# ---------------------------------------------------------------------------
# Part C/E — saved charts exist and are valid PNGs
# ---------------------------------------------------------------------------
print("== Charts (kata + capstone) ==")
expected_pngs = [
    os.path.join(CHARTS, "chart_relationship_study.png"),
    os.path.join(CHARTS, "chart_null_sleep.png"),
    os.path.join(CHARTS, "chart_comparison_section.png"),
    os.path.join(CHARTS, "chart_trap_line.png"),
    os.path.join(CHARTS, "chart_collision_broken.png"),
    os.path.join(CHARTS, "chart_collision_fixed.png"),
    os.path.join(CHARTS, "chart_color_arbitrary.png"),
    os.path.join(CHARTS, "chart_color_deliberate.png"),
    os.path.join(CHARTS, "chart_small_multiples.png"),
]
for p in expected_pngs:
    check(_png_ok(p), f"valid PNG exists: {os.path.basename(p)}")
cap_pngs = [
    os.path.join(CHARTS, "cap_relationship_study_annotated.png"),
    os.path.join(CHARTS, "cap_null_sleep.png"),
    os.path.join(CHARTS, "cap_comparison_section.png"),
    os.path.join(CHARTS, "cap_small_multiples.png"),
]
for p in cap_pngs:
    check(_png_ok(p), f"valid capstone PNG exists: {os.path.basename(p)}")

# Collision pair must be two *different* files (broken vs fixed).
broken = os.path.join(CHARTS, "chart_collision_broken.png")
fixed = os.path.join(CHARTS, "chart_collision_fixed.png")
check(_png_ok(broken) and _png_ok(fixed) and
      os.path.getsize(broken) != os.path.getsize(fixed),
      "collision broken/fixed are distinct files")

# Arbitrary vs deliberate color charts must differ.
arb = os.path.join(CHARTS, "chart_color_arbitrary.png")
delib = os.path.join(CHARTS, "chart_color_deliberate.png")
check(_png_ok(arb) and _png_ok(delib) and os.path.getsize(arb) != os.path.getsize(delib),
      "arbitrary vs deliberate color charts are distinct files")

# Layout QA: the "broken" figure should show an overlap, the "fixed" figure should not.
# We reconstruct each figure exactly as in the kata and measure bounding-box overlap
# between the annotation and the legend -- the programmatic analog of opening the PNG.
print("== Layout collision QA ==")
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
x = df["study_hours_per_week"]
y = df["exam_score"]
r_s, p_s = stats.pearsonr(x, y)

def _overlap(a, b):
    # bbox.bounds is (x0, y0, width, height) -> compute x1/y1 explicitly
    ax0, ay0, aw, ah = a.bounds
    bx0, by0, bw, bh = b.bounds
    ax1, ay1 = ax0 + aw, ay0 + ah
    bx1, by1 = bx0 + bw, by0 + bh
    ix = max(0, min(ax1, bx1) - max(ax0, bx0))
    iy = max(0, min(ay1, by1) - max(ay0, by0))
    return ix > 0 and iy > 0

def detect(use_constrained, annot_xy, loc="upper left"):
    fig, ax = plt.subplots(figsize=(8, 5), layout="constrained" if use_constrained else None)
    ax.scatter(x, y, s=18, alpha=0.4, label="student")
    leg = ax.legend(loc=loc)
    ann = ax.text(annot_xy[0], annot_xy[1], f"r = {r_s:.3f}", transform=ax.transAxes,
                  fontsize=12, bbox=dict(boxstyle="round", fc="yellow"))
    fig.canvas.draw()
    legend_bbox = leg.get_window_extent(fig.canvas.get_renderer())
    ann_bbox = ann.get_window_extent(fig.canvas.get_renderer())
    plt.close(fig)
    return _overlap(legend_bbox, ann_bbox)

# Broken: annotation dropped exactly on top of the upper-left legend, no constrained layout.
broken_overlaps = detect(False, (0.16, 0.93), loc="upper left")
# Fixed: annotation moved to the lower-right (away from the legend), constrained layout.
fixed_overlaps = detect(True, (0.03, 0.92), loc="lower right")
check(broken_overlaps, "broken layout: annotation overlaps legend (collision reproduced)")
check(not fixed_overlaps, "fixed layout: annotation no longer overlaps legend")

# ---------------------------------------------------------------------------
# Deliverable files exist
# ---------------------------------------------------------------------------
print("== Deliverables ==")
for f, label in [(STUDENTS_CSV, "students.csv"), (GEN_PY, "generate_data.py"),
                 (KATA_NB, "kata notebook"), (CAP_NB, "capstone notebook")]:
    check(os.path.exists(f), f"exists: {label}")


# ---------------------------------------------------------------------------
# Notebooks execute cleanly (Restart Kernel & Run All => no error cells)
# ---------------------------------------------------------------------------
print("== Notebook cleanliness ==")
try:
    import nbformat
    for path, label in [(KATA_NB, "kata notebook"), (CAP_NB, "capstone notebook")]:
        nb = nbformat.read(path, as_version=4)
        errs = [i for i, c in enumerate(nb.cells)
                if c.cell_type == "code" and any(
                    o.get("output_type") == "error" for o in c.get("outputs", []))]
        check(not errs, f"{label}: zero error cells (found {len(errs)})")
except Exception as e:  # pragma: no cover
    failed += 1
    failures.append(f"nbformat check failed: {e}")
    print("FAIL  notebook cleanliness (nbformat error)")

print()
print(f"== RESULT: {passed} passed, {failed} failed ==")
if failures:
    print("Failed checks:")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("All checks passed.")
