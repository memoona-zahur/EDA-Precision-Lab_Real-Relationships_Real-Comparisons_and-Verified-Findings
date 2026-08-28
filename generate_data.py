"""Generate the students dataset for the Week 06 Day 1 EDA Precision Lab.

The generation code is taken verbatim from the assignment spec so that the
relationships in the data are *known in advance* -- this is what lets us check
our own work throughout the lab.
"""
import os

import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=21)
n = 600

class_section = rng.choice(["A", "B", "C"], size=n, p=[0.34, 0.33, 0.33])
study_hours = rng.normal(10, 3.5, size=n).clip(0, None).round(1)
sleep_hours = rng.normal(7, 1.2, size=n).clip(3, 10).round(1)
attendance_pct = rng.normal(85, 10, size=n).clip(40, 100).round(1)

noise = rng.normal(0, 8, size=n)
section_bonus = pd.Series(class_section).map({"A": 0, "B": 0, "C": 4}).values
exam_score = (50 + 2.6 * study_hours + 0.15 * attendance_pct + section_bonus + noise).clip(0, 100).round(1)

students = pd.DataFrame(
    {
        "student_id": np.arange(1, n + 1),
        "class_section": class_section,
        "study_hours_per_week": study_hours,
        "sleep_hours_per_night": sleep_hours,
        "attendance_pct": attendance_pct,
        "exam_score": exam_score,
    }
)


def main() -> None:
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "students.csv")
    students.to_csv(out_path, index=False)
    print(f"Wrote {len(students)} rows to {out_path}")
    print(students.head())
    print(students.dtypes)


if __name__ == "__main__":
    main()
