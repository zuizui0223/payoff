# PAYOFF-B comparative timing-retention route — 2026-10-03

Status: **PROSPECTIVE CANDIDATE; outcome unopened**

## Ecological question

Why do some migratory schedules carry an early/late departure deviation all
the way to arrival, whereas other migrants reset that deviation en route?

This is the comparative version of the original PAYOFF-B intuition:

> departing late does not necessarily mean arriving late.

The question is not whether timing reset exists. Reset and catch-up are already
documented in individual systems. The question is **what explains
interspecific variation in how much relative timing is retained during a
migration**.

## Prior-art boundary

Already known:
- Hudsonian godwits can dissipate large annual-cycle timing deviations;
- tree swallows show a domino effect that resets during the non-breeding
  period;
- late black-and-white warblers shorten stopovers near the breeding
  destination;
- purple martins retain individual timing order, but consistency weakens over
  longer migration distances;
- a 2022 phylogenetic meta-analysis quantified repeatability of individual
  migration events across 47 species;
- Wang et al. 2024 compiled full annual-cycle tracking dates for 1,531
  individuals plus 177 population records from 186 species and modeled
  determinants of mean migration timing and pooled carry-over paths.

Not found in the literature screen:
- a cross-species estimate of **within-journey departure-to-arrival timing
  retention** on a common relative-timing scale;
- a comparative test of which route/life-history features predict this
  retention.

This is a candidate novelty, not yet a confirmed novelty claim.

## Primary estimand

Use individual-level spring migration records only.

For individual i in species s, population p and year y, define relative spring
departure and arrival timing by centering within the narrowest available
species × population × year group:

\[
d_{ispy}
=
D_{ispy}-\bar D_{spy},
\]

\[
a_{ispy}
=
A_{ispy}-\bar A_{spy}.
\]

Fit a hierarchical transition model

\[
a_{ispy}
=
\lambda_s d_{ispy}
+
b_{py}
+
\epsilon_{ispy}.
\]

Interpretation:
- \(\lambda_s \approx 1\): relative departure timing is carried through to
  arrival;
- \(0<\lambda_s<1\): partial compression / catch-up;
- \(\lambda_s \approx 0\): effective within-migration reset;
- \(\lambda_s<0\): reversal / overshoot;
- \(\lambda_s>1\): amplification of timing differences.

The term "retention" is descriptive. It does not by itself identify active
behavioral correction.

## Data source

Primary candidate:
Wang et al. 2024, *Nature Communications* 15:4111,
DOI 10.1038/s41467-024-48248-7.

The published database contains:
- 1,531 individual full annual-cycle tracks;
- 177 population-level records;
- 186 species;
- individual ID;
- capture site / population information;
- year;
- sex when available;
- breeding and non-breeding coordinates;
- spring departure from the non-breeding site;
- spring arrival at the breeding site;
- autumn departure and arrival.

The public timing/code repository is Figshare
DOI 10.6084/m9.figshare.24613599.

Population-average rows are not admissible to the primary individual-retention
analysis.

## Prespecified admission gate

Before fitting any retention model, the downloaded raw table must satisfy:

1. individual versus population-average rows can be distinguished;
2. species identity is explicit;
3. spring departure and spring arrival are both present in the same row;
4. year is explicit;
5. a population/capture-site/study grouping variable is available or can be
   reconstructed without using timing outcomes;
6. at least 100 individual rows remain after restricting to groups with at
   least 3 individuals in the same species × population × year;
7. at least 10 species have enough within-group variation to contribute to a
   random-slope estimate.

If any of 1–6 fail, the primary analysis stops.
If 7 fails, species-level comparative inference stops and only a pooled
descriptive transition estimate may be reported.

No threshold may be lowered after seeing \(\lambda\) estimates.

## Primary test

The first test is whether departure-to-arrival retention varies among species.

\[
H_0:\sigma_{\lambda,\mathrm{species}}=0
\]

versus a model with species-level random slopes.

This is a heterogeneity question, not a test that all species actively
"correct" timing.

## First mechanistic moderator

Migration distance is the only prespecified primary moderator.

Prediction:

\[
\boxed{
\text{longer migration distance}
\rightarrow
\text{lower timing retention}
}
\]

Rationale:
- longer journeys expose individuals to more variable environmental
  conditions and more opportunities for en-route rescheduling;
- in purple martins, individual timing consistency weakened over longer
  migration distances.

This direction is prospective for the 186-species dataset and must not be
retuned after outcome.

Body mass, sex, flight mode and spring migration duration are sensitivity or
secondary moderators unless separately preregistered before opening the
retention outcome.

## Original PAYOFF-B information prediction

A second, separate gate can be attempted only after the primary retention
estimate is frozen.

For species overlapping the existing preregistered PAYOFF-B predictive-
connectivity dataset, test whether stronger source–destination environmental
predictability is associated with stronger departure-to-arrival retention.

Prediction:

\[
\text{predictive connectivity}\uparrow
\quad\Rightarrow\quad
\lambda\uparrow.
\]

Biological rationale:
if origin information reliably predicts destination spring, the departure
schedule should remain informative throughout migration. When cross-site
predictability is weak, greater en-route resetting is expected.

Admission rule:
- species matching must be taxonomically exact or documented;
- at least 15 independent species are required;
- the predictor must remain the previously defined pre-outcome predictive
  connectivity quantity;
- no alternative cue metric may be substituted after seeing \(\lambda\).

If fewer than 15 species overlap, this lane closes without interpretation.

## Fitness boundary

This comparative route does **not** claim that lower or higher \(\lambda\) is
universally fitter.

- high retention can reflect a reliable endogenous schedule or inflexibility;
- low retention can reflect useful environmental updating or disruption/noise.

Fitness requires a separate vital-rate endpoint.

The direct fitness-rescue screen remains fail-closed. Timing retention is an
ecological strategy coordinate, not a fitness score.

## Why this route may be worth doing

This question sits directly in full-annual-cycle migration ecology:

- individual studies already disagree biologically in whether timing
  deviations persist or reset;
- the repeatability literature shows large variation in timing consistency but
  does not measure propagation from one event to the next;
- the Wang global database makes a comparative transition analysis possible;
- the result would quantify a biologically interpretable property:
  **how much of an individual's relative timing survives the journey**.

This is substantially closer to the original PAYOFF-B question than the V3/V4
abstract control and fitness-rescue framings.

## Stop rule

The route is abandoned if:
- the public Wang data do not support the required within-population-year
  centering;
- species-level slope heterogeneity cannot be identified;
- literature review finds an existing cross-species analysis of the same
  departure-to-arrival retention estimand;
- or the result is indistinguishable from the pooled carry-over coefficient
  already reported by Wang et al. 2024 without an interpretable species-level
  dimension.

Until data admission and the novelty check both pass:

\`\`\`text
PAYOFF_B_COMPARATIVE_RETENTION = PROSPECTIVE
\`\`\`
