# PAYOFF-B: source-verified goose stage calendar and breeding prediction audit

Date: 2026-10-08
Status: **post-publication exploratory**, not a new confirmatory ecological mechanism.
Stacked draft PR #320 on PR #318. Frozen V3, V7R and V8 results and hypotheses remain unchanged.

## Genuine external natural sample

The original Schindler et al. (2024) author-hosted CSV was read from immutable
commit 2171bcd36bf37022c8716e15c0f75412103b0f3f. Normalizing its line
endings reproduces Dryad's version-5 SHA256
9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd.

- **107 complete spring bird-years** from **49 birds** and five annual cohorts
  (2018–2022: 10, 29, 27, 24, 17 bird-years).
- All six annotated stages on each spring individual-year, no duplicate
  individual/year/stage, chronological stage order.
- Stage 3 is start of Iceland spring staging; Stage 5 is start of migration
  flight to Greenland; Stage 6 is start of early breeding. These first_day
  values are stage boundaries, not verified moments of cognitive decisions.
- Source spring rows = 642, not 642 independent breeding trials.
- Individual/year binary outcome categories source count:
  **28 success, 72 failure, 7 deferral** = 107.
  Original article quotes **28 success, 73 failure, 7 deferral** = 108.
  The discrepancy is precisely **one failed case**, but why the original
  published summary and version-5 source differ is not established. Do not
  create a synthetic missing observation or pool the counts without a caveat.

## Step 1: independent stage-calendar structural-null audit

Locked in
docs/PAYOFF_B_GOOSE_STAGING_CALENDAR_SOURCE_CONTRACT_20261008.md
before the stage-response association was inspected.

The new source-only GitHub Actions run **37766775585 succeeded**
(synthetic fixed-calendar negative control and real-source gate).
Calendar year is centred within each source cohort.

| Descriptive quantity | Source estimate |
|---|---:|
| Stage-5 exit day regressed on stage-3 arrival day, within year | **−0.01337** day/day |
| 95% 4,000-draw bootstrap, clustered by bird | **−0.1530 to +0.1199** |
| Staging duration (stage5−stage3) versus arrival, within year | **−1.01337** day/day |
| Within-year departure SD / arrival SD | **0.4405** |
| Within-year shuffled-exit two-sided permutation p (descriptive only) | **0.7928** |

The first two slopes obey an **exact arithmetic identity** on every
complete dataset:

    beta(staging_duration ~ stage3_arrival)
      = beta(stage5_exit ~ stage3_arrival) - 1.

No active feedback mechanism is identifiable from this identity. Under a
fixed-year departure date, the first coefficient is zero and the second
exactly -1 regardless of the information an animal possesses.

The result is calendar-anchoring-compatible: stage-5 exit date barely
depends on stage-3 arrival time. Deleting one complete calendar year at a
time leaves the exit-on-arrival coefficient between **−0.0436 and −0.0010**.
This does not establish pure photoperiod causation, deliberate waiting, lack
of environmental cue perception, or available physical recourse.

This is an external replication of an observational mechanism alias
previously diagnosed in the V7R barnacle goose records, not independent
verification of the PAYOFF-B controller.

## Step 2: exploratory outcome prediction, not reproductive causation

Prior to computing this NEW numeric comparison, the fixed analysis contract
was written to
docs/PAYOFF_B_GOOSE_STAGING_ENERGY_FITNESS_PREDICTION_CONTRACT_20261008.md.

Unit is individual-year success, not stage row. Leave one complete calendar
year out, fit with the remaining four years; evaluate log loss on the excluded
year (5 source-year folds). Fixed lambda=2 ridge Bernoulli, training-only
scaling and fixed features.

- M0: numeric year code, staging start (stage3), early breeding start
  (stage6).
- M1: M0 plus source stage3–4 ACC-fix-weighted feeding fraction and average
  source stage3–4 log_ODBA activity/energy proxy.
- M2: M1 plus realized Iceland staging duration (stage5 first_day−stage3 first_day).

A standalone independent JavaScript calculation of the fixed contrast,
using the original author 642-row source and the specified ridge Newton
algorithm, yielded:

| Model | Five-year heldout average log loss |
|---|---:|
| M0 calendar | **0.597294** |
| M1 calendar + feeding/activity | **0.579074** |
| M2 additionally staging duration | **0.580986** |

Paired gain (M0−M1) = **+0.018219** log-loss points, positive in four of five
heldout years. Paired gain (M1−M2) = **−0.001912**, positive in only three of
five years, with the latest year strongly negative. Brier-score gain from
M1 to M2 is approximately **−0.0000374**.

These numbers are **post-original-study exploratory**. The dedicated
GitHub Actions replication with a bird-cluster validation-only interval was
queued at the time this note was written and must be checked before treating
these as verified permanent numeric outputs. Do not present a novel fitness
effect unless it survives the source and uncertainty audit.

The original Schindler et al. paper already included arrival-day timing,
feeding and activity in a Bernoulli model of breeding success. M1's behavior
is therefore expected and **not a new finding**. The focal extra duration
variable in M2 does not add out-of-year prediction in the observed contrast.
This cannot prove that longer/shorter staging has no biological effect;
the predictor overlaps with dates in M0/M1, the source includes only five
years and 49 repeated individuals, and actionability is not independent.

## Ecological claim boundary

**Supported descriptive finding:** near-fixed year-conditioned Iceland exit
dates make longer staging for early arrivers appear to be compensatory
behavior, even when no active environmental error feedback is identified.

**Exploratory outcome result:** adding realized staging duration to the
declared date/feeding/activity forecast did not improve held-year breeding
success prediction under the fixed ridge comparison.

**Not supported:** active cue-based phase correction, information value at
the irreversible decision, maximum possible speed/stopover recourse,
causal benefits or costs of waiting, independently derived fitness-optimal
phenological target, or cross-species interaction-game equilibria.

## Relation to Paper 2

The ecologically important evidence is a **negative control on mechanistic
interpretation**. A population can show strong apparent schedule
convergence without revealing active information-dependent control, and
timing outcomes can differ from fitness mechanisms. The result may support
a cautious methodology or natural-systems paragraph in The American
Naturalist-bound Paper 2; it is not a standalone new goose-fitness paper.

Sources:
- Original study: https://doi.org/10.1098/rspb.2023.2016
- Author data/code: https://github.com/aschindler23/Schindler_etal_2024_ProcB
- Source calendar workflow: https://github.com/zuizui0223/payoff/actions/runs/37766775585
