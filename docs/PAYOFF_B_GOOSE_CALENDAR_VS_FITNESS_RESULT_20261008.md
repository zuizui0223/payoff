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

## Audit correction: stage6 is a later-stage predictor (2026-10-08)

The original M0/M1/M2 comparison above included the day that early breeding
starts (stage6). That variable occurs **after the stage5 Iceland exit**.
Therefore the original models can only be read as *retrospective
post-arrival prediction of breeding outcome*, not as a model of information
available when choosing to leave the Iceland staging area. They are preserved
here without reclassification or numerical retuning.

The dedicated GitHub workflow initially FAILED because its synthetic toy
contained 125 bird-years while the function asserted exactly 107 output
rows. The source-only stage-calendar test passed, but the *fitness forecast
did not execute* in that failed workflow. The source-code test was repaired
to compare output coverage with the input row count, and a time-of-availability
guard was added. The repair is explicit, not a null or a successful biological
replication.

A separate earlier-available information set was fixed in
docs/PAYOFF_B_GOOSE_AS_OF_STAGE5_TIME_GATE_20261008.md
*before seeing the new as-of-stage5 numerical result*:

- A0: known year code + Iceland staging start (stage3).
- A1: A0 + stage3–4 feeding-fix fraction and stage3–4 mean log_ODBA,
  both stage summaries ending before stage5 departure (these are proxies
  available to an analyst, not measured beliefs of the bird).
- A2: A1 + stage5 departure minus stage3 arrival (realized staging duration).
- **No stage6 arrival/breeding-start variable** appears in any A model.

An independent JavaScript re-implementation of the locked training-only
standardization and five-year blocked ridge logistic model yielded:

| Source-available-at-stage5 model | Mean held-year log loss | Mean held-year Brier |
|---|---:|---:|
| A0 calendar at staging exit | **0.584465** | 0.196943 |
| A1 plus stage3–4 feeding/activity | **0.567970** | 0.189536 |
| A2 plus actual staging duration | **0.571462** | 0.189837 |

Matched A0→A1 log-loss improvement is **+0.016495**. A1→A2 is
**−0.003492**, meaning the extra duration variable makes held-year
predictions marginally worse, on average. The five source-year A1→A2 gains
were **+0.010238, +0.004158, +0.005238, +0.003749,
and −0.048707**. This result is thus not directionally uniform
across years: deterioration in the final held-out year outweighs
small apparent gains in the first four.

**Verified against the repaired GitHub workflow**:
- GitHub Actions run **37770592060**, job **113288924463**: all synthetic
  identity checks, source validation, retrospective and as-of-stage5
  cross-validation, and artifact upload **PASS**.
- Artifact **11548035498** (SHA256
  5be659e601dd0cb03b7c369700a870dfa433af01a4f8d636daf46b5b62f9c466)
  contains all three JSON outputs.
- Source Python logistic analysis independently reproduces the exact
  separate JavaScript results in the table above.
- A0→A1 mean held-year log-loss improvement +0.016495; 4,000 bird-cluster
  validation-only 95% interval **[−0.018465, +0.051306]**.
- A1→A2 mean improvement **−0.003492**, 4,000 bird-cluster validation-only
  95% interval **[−0.016315, +0.009070]**, which crosses zero.
- These intervals resample precomputed held-year prediction errors by bird
  but **do not refit the model** in each bootstrap draw and do not account
  for only five independent calendar-year regimes. They are descriptive
  uncertainty bounds, not causal selection tests or formal equivalence
  intervals.

The corrected stage5-safe comparison was therefore **completed and
independently checked**, with no strong support for additional staging-duration
predictive information in this prespecified covariate contrast.

A1→A2 comparison is also a **calendar-geometry test**, not a unique
independent staging effect: when stage3 start is known, adding its difference
from stage5 exit is algebraically equivalent to adding stage5 exit.
Therefore any predictive gain or loss cannot decide whether a goose waited,
was physically constrained, or followed a socially or photoperiodically
anchored departure day.

Even a time-safe positive outcome would not establish an energetic or
demographic *causal* cost of timing correction, or an actual perception of
future Greenland spring. The authors already included breeding arrival,
feeding and ODBA predictors in their published model. These are
post-publication exploratory descriptive comparisons, not a new species-
general ecological mechanism.

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


## Post-result audit: common calendar and individual-specific departures can coexist

The initial annual-calendar structural null showed nearly invariant staging exit
conditional on arrival, but a common annual departure average does **not**
require all individuals to have zero persistent offsets from that average.
We therefore examined the 30 repeat-tracked individuals (97 non-independent
same-bird interannual observation pairs among 49 source birds), without opening
their energy or breeding outcomes.

The **preliminary source-only exploratory correlations**, after subtracting
each year's group mean, were

    stage 2 first flight start       r = +0.5062
    stage 3 Iceland staging start    r = +0.3814
    stage 4 later staging start     r = +0.2908
    stage 5 Iceland flight exit     r = +0.6874
    stage 6 early breeding start    r = +0.3160.

These Pearson correlations reuse some birds across multiple pairs and are
*not 97 independent samples*. The stage-5 estimate looked unusually high,
but all stages had been inspected before formal resampling. It was therefore
labelled **POST-EXPOSURE EXPLORATORY**, not a preregistered stage-5 result.

An independent JS implementation of 10,000 year-restricted shuffles of each
bird's full five-stage standardized seasonal vector, retaining the original
bird-year observation pattern and equally averaging within-bird pair products
over the 30 repeated birds, yielded the following post-result diagnostics:

| Stage | Equal-bird average standard-score cross-year product | Year-specific bird-label permutation, positive-tail p |
|---|---:|---:|
| 2 | +0.3354 | 0.00470 |
| 3 | +0.2604 | 0.02490 |
| 4 | +0.2724 | 0.02090 |
| 5 | **+0.5387** | **0.00010** |
| 6 | +0.2662 | 0.02440 |

An independently implemented Python/GitHub Actions run **37771712261**
confirmed the exact individual-equal cross-year-product values in the table.
With 10,000 independently seeded Python within-year identity permutations,
the stage-5 within-stage positive-tail p was **0.00010** and the
**max-over-five-stage post-selection p was 0.00030**. The direct
**stage5-minus-stage3** comparison was **p=0.06499**, so an especially
high stage-5 relative to stage-3 effect was not established.
The stage-5 product statistic was **0.5387**, with a 10,000-resample
equal-bird bootstrap 95% descriptive interval **[0.2289,0.9121]**.
All are post-selection exploratory and do **not** demonstrate a
fitness benefit, internal chronotype, clock gene, cue use, or adaptive
behavioral compensation.

**Reproduction:** GitHub Actions run **37771712261** / job
**113292639943** completed successfully; the synthetic identity test,
source-verified full permutation, bootstrap and artifact upload all passed.
Machine-readable record: artifact **11547973222**, ZIP SHA256
3c3ca227e2eb6dfa756c90afc7e6e370d44fc496ac8fbc9c4f0398356c08fd5d.
Separate independently computed JavaScript estimates matched Python's
descriptive products exactly, while seeded Monte Carlo p-values differ
slightly as expected between RNG implementations. Exact Python receipt:
data/payoff_b_goose_individual_exit_repeatability_ci_receipt_20261008.json.

**A more realistic open-loop comparator** for the data is therefore

    departure_{i,y} = annual departure calendar_y
                       + stable bird-specific offset_i
                       + unmeasured noise_{i,y}.

This model can produce calendar-like departure concentration,
near-zero departure-on-arrival slope, apparent -1 stay-duration slope,
and persistent individual departure rank, *without requiring*
feedback from a newly observed destination spring phase.
The bird offset could reflect social family membership, consistent habitat
or route, individual state or other stable unmeasured factors.
It does not prove physiological calendar rigidity.

**Prior-art restriction:** individual migration-timing repeatability is already
established in Franklin et al. (2022, J Anim Ecol,
doi:10.1111/1365-2656.13697; 177 repeatability effects from 47 avian species).
Individually consistent departure-temperature cues had already been directly
shown in satellite-tracked Asian houbara (2021,
https://pmc.ncbi.nlm.nih.gov/articles/PMC8285904/).
Therefore this result is a source-specific **mechanism-aliasing negative
control**, not novel natural evidence that individual schedules or
information-informed timing first exist in geese.

Original experimental/causal driver remains unidentified because local
temperature, route coordinates, full social-group membership and predecision
cues are not in the released summarized source used in this audit.

Source-only code:
scripts/payoff_b_goose_individual_exit_repeatability.py

Post-exposure exploratory contract:
docs/PAYOFF_B_GOOSE_INDIVIDUAL_EXIT_REPEATABILITY_POSTRESULT_CONTRACT_20261008.md

Independent computation ledger:
data/payoff_b_goose_individual_exit_repeatability_js_crosscheck_20261008.json
