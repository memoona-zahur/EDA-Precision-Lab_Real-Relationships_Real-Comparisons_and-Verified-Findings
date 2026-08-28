# Technical Summary — EDA Precision Report (Week 06 · Day 1)

*Plain-language write-up for a non-technical reader.*

## The dataset
We examined 600 students. For each one we had: reported study hours per week,
reported sleep hours per night, attendance percentage, which class section they
were in (A, B, or C), and their exam score. The dataset was created with a fixed
random seed, so it is fully reproducible and we can check every result against
the known true relationships.

## What we found
1. **More study, higher scores — an association, not proof of cause.**
   The more weekly study hours a student reported, the higher their exam score
   tended to be (Pearson correlation ≈ 0.69, a strong positive relationship).
   On average, each extra weekly study hour was associated with about 2 more
   points on the exam. **Important caveat:** this does *not* prove studying
   causes higher scores. A student who is more motivated might both study more
   and prepare better in ways we didn't measure (attention, prior background,
   sleep discipline). That hidden factor is a "confound" that could explain part
   of the link.

2. **Sleep had no visible relationship.** Hours of sleep per night showed
   essentially zero correlation with exam score (r ≈ −0.02). This looks like a
   "nothing happened" chart, but it is a real, honest result: in this dataset
   sleep carried no signal for scores. We report it rather than hiding it.

3. **Section C scored higher than A and B.** On average Section C was about
   3.8 points higher than Section A. To make sure this wasn't just bad luck in
   the sample, we resampled the data thousands of times (a "bootstrap") and got
   a 95% confidence interval of roughly −5.7 to −1.8 for `mean(A) − mean(C)`.
   Because that interval stays entirely below zero, the difference is very
   unlikely to be random noise — it's a real, repeatable gap. The data doesn't
   tell us *why* (the generator gave Section C a +4 design bonus), only that the
   gap is real.

4. **The study-time relationship was consistent across sections.** Splitting
   students by section didn't change the story — in every section, more study
   was associated with higher scores, with a similar strength (r ≈ 0.68, 0.71,
   0.69 for A, B, C).

## What checks we ran before calling it done
- **Right chart type for the job:** a continuous-variable relationship chart vs.
  a by-category comparison chart, decided by the "shuffle test."
- **Layout QA:** every chart was saved to a file and checked for overlapping
  titles, legends, or labels (we deliberately broke one, saw the collision, and
  fixed it).
- **Self-audit:** every number written in the report was regenerated from the
  code and matched against a table to catch any hand-typed mistakes.
- **Statistical backing:** the comparison claim is backed by a bootstrap
  confidence interval, not just a visual impression.
- **Cautious wording:** findings avoid causal language ("causes", "leads to")
  and are phrased as correlations.

## Honest limitations
This is **observational, cross-sectional** data — a single snapshot, not an
experiment. It **cannot establish cause and effect**, and our two measurements
(study hours, sleep hours) rely on what students reported. Unmeasured factors
such as motivation, prior background, attention, or sleep *quality* could
explain part of the patterns. The "sleep doesn't matter" finding applies to
these 600 students and these particular measurements — it does **not** mean
sleep is unimportant generally, and it should not be over-generalized.
