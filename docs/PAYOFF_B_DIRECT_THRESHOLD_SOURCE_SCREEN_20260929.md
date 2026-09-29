# PAYOFF-B source screen for a direct natural deadline-threshold test

Date: **2026-09-29**  
Status: **screen complete; no located source currently satisfies the full direct-test contract**

## Qualification target

A direct natural test of the pairwise information-deadline mechanism requires all of the following in the same system:

| quantity | required role |
|---|---|
| pre-commitment cue reliability q | environmental information quality |
| delay/opportunity cost D_i | independent cost of postponing commitment |
| C_F, C_M, pi or equivalent state-loss scale | converts D_i to predicted q_i |
| observed cue use | distinguishes commit-now from wait/use-cue |
| repeated q support | must cross below, within and above the predicted asynchronous window |

## Candidate 1 — Barnacle goose predictability system

Kölzsch et al. (2015), *Journal of Animal Ecology*  
DOI: 10.1111/1365-2656.12281

Public tracking sources include Movebank datasets from the original study.

What it supplies:

- 40 tracked barnacle geese across Greenland, Svalbard and Barents Sea routes;
- 16 combined stopover regions;
- environmental predictability between consecutive stopovers;
- observed arrival timing;
- published evidence that arrival at stopovers was more closely tied to local spring onset where predictability was higher.

Qualification:

- q-like information quality: **YES**
- behaviour linked to q: **YES, continuous timing response**
- independent D: **NO**
- binary wait/use-cue decision: **NO**
- exact q1 < q <= q2 window: **NO**

Classification: **NEAR_DIRECT_INFORMATION_USE_LANE**

This is substantially closer to the theorem than the current wigeon post-error-correction lane because the response concerns timing relative to environmental predictability rather than correction after phase error.

## Candidate 2 — Barnacle goose breeding / fitness extension

Boom et al. (2023), *Journal of Animal Ecology*  
DOI: 10.1111/1365-2656.14020  
Dryad: 10.5061/dryad.m63xsj47x

The public dataset contains 96 adult female barnacle geese, some repeated over years, spanning 2008–2020. It provides nest/potential-nest locations, breeding status, nesting success, arrival date and local GDD-based spring onset, plus raw tracking data for records not already hosted on Movebank. The source also incorporates 11 tracks from the Kölzsch et al. lineage.

What it adds:

- breeding propensity;
- nesting success;
- arrival date relative to spring onset;
- broad life-history tactics from long-distance migrants to residents;
- raw tracking support for many tracks.

Important boundary:

Breeding propensity or nesting success is a fitness consequence, not automatically the opportunity cost D of waiting one decision interval. Estimating D from these outcomes would require a prespecified causal/decision model for how a marginal delay changes expected fitness. It cannot be read off from Breeding or Nesting_success.

Qualification:

- q-like information quality: **potentially reconstructable**
- fitness consequence: **YES**
- independent D: **NOT YET**
- cue-use threshold: **NOT YET**
- exact asynchronous window: **NO**

Classification: **BEST_CURRENT_DEVELOPMENT_CANDIDATE_NOT_DIRECT**

## Candidate 3 — American redstart delay-cost anchor

Dossman et al. (2023), *Ecology*  
DOI: 10.1002/ecy.3938

The study reports that birds departing 10 days later migrated about 43% faster and had about a 6.3% reduction in apparent annual survival. The paper also cites prior evidence that an approximately 10-day arrival difference was associated with a substantial reduction in fledging success.

What it supplies:

- a concrete ecological cost associated with migratory delay;
- an empirically grounded time-pressure / deadline axis.

What it lacks for the theorem:

- a controlled or reconstructed cue-reliability sweep q;
- an observed switch in use of a later cue;
- a shared-cue interacting pair.

Classification: **DELAY_COST_ANCHOR_ONLY**

## Decision

No screened source currently licenses the sentence:

> measured D2-D1 predicts measured q2-q1, and the interval q1 < q <= q2 contains observed asynchronous cue use.

The most promising development path is the barnacle-goose lineage because predictability, migration timing, arrival, breeding state and reproductive outcomes exist in closely connected public datasets.

However, PAYOFF-B should **not** promote that system to a direct theorem test unless D can be estimated independently of the cue-use outcome.

## Next analysis gate for the barnacle-goose lineage

Before opening any new response model:

1. reconstruct consecutive-stopover predictive connectivity from historical spring-onset series;
2. define the decision event at each stopover without using the focal response;
3. determine whether an independent fitness model can identify a marginal delay cost D for that decision;
4. verify that q spans enough range to bracket an actor-specific threshold;
5. only then register a cue-use threshold analysis.

If step 3 fails, retain barnacle goose as a strong information-use bridge, not a direct D -> q test.

## Claim ceiling after this screen

The correct current statement is:

> The deadline-to-threshold-to-asynchrony mapping is exact and implementation-verified in the declared model. Existing natural systems support information quality, timing dependence, response asymmetry and fitness costs of delay separately, but no located dataset yet identifies the full pairwise deadline-threshold mechanism in one natural system.
