# PAYOFF-B V7 prospective contract — predictability × urgency in migration decisions

Date: **2026-10-05**

Status: **PREOUTCOME; no new focal tracking result opened**

## 1. Biological question

> **When should a migrant trust local environmental information?**

Long-distance migrants move through a chain of sites. Environmental information
available at one site can help predict conditions at the next, but the value of
waiting for good information may change as the breeding deadline approaches.

The specific V7 question is:

> **Does the influence of predictive environmental information on migration
> timing depend on route-stage urgency / remaining opportunity?**

This is the direct ecological form of the user's original intuition:
future conditions may become easier to infer while the time available to wait
or adjust becomes smaller.

## 2. Primary field

- migration ecology / movement ecology;
- environmental cue use and migration decisions;
- full-annual-cycle timing;
- global-change phenology.

This is not framed as a new control-theory paper.

## 3. Prior-art boundary

### Bauer, Gienapp & Madsen 2008

Pink-footed geese:
- departure decisions respond to day length and accumulated temperature;
- the relevance of these cues changes en route;
- local accumulated temperature at stopovers informs northward progression.

Therefore V7 cannot claim novelty for:
- stage-dependent cue use;
- en-route environmental updating;
- local temperature affecting departure decisions.

### Kölzsch et al. 2015

Barnacle geese:
- climatic/phenological predictability between consecutive stopovers was
  quantified independently from a 30-year spring-phenology series;
- higher predictability was associated with arrival timing closer to local
  spring onset;
- timing also changed systematically along the route / toward breeding.

Therefore V7 cannot claim novelty for:
- predictive connectivity along migration routes;
- predictability affecting migration timing;
- route position affecting timing.

### Theurich et al. 2026

Dark-bellied Brent geese:
- wind selectivity strongly affected departure probability;
- wind selectivity declined over the seasonal departure window;
- baseline departure tendency rose as migration urgency increased.

Therefore V7 cannot claim novelty for:
- time-varying cue selectivity;
- urgency weakening willingness to wait for favorable conditions.

## 4. Candidate contribution

The only candidate biological contribution is the **joint test**:

> predictive environmental information should influence realized migration
> timing differently depending on route-stage urgency / remaining opportunity.

A new estimator alone is not novelty.

## 5. Primary natural system

Kölzsch et al. 2015 barnacle-goose tracking data.

Public Movebank datasets:
- Greenland: DOI 10.5441/001/1.5d3f0664
- Svalbard: DOI 10.5441/001/1.5k6b1364
- Barents Sea: DOI 10.5441/001/1.ps244r11

The published study contains:
- 40 complete spring migrations;
- 16 generalized stopover regions across three flyways;
- independent 30-year spring-onset predictability between consecutive regions;
- route position / distance to breeding grounds;
- individual arrival timing relative to local spring onset.

## 6. Primary estimand

For visit i to stopover region j in flyway f, define:

[
E_{ij}
=
A_{ij} - S_{jy},
]

where:
- (A_{ij}) = individual arrival date;
- (S_{jy}) = onset of spring at the region in that year.

The primary response is absolute timing error:

[
Y_{ij}=|E_{ij}|.
]

Predictive information for the preceding transition is:

[
q_j = mathrm{corr}(S_{j-1,y},S_{j,y}),
]

or the published proportionality/predictability index when that is the
prespecified source quantity for the same transition.

Route-stage urgency is represented only by a **geometry-only proxy** fixed
before outcome fitting:

[
U_j
=
1 - rac{d_{j,mathrm{breed}}}
{d_{mathrm{winter},mathrm{breed}}},
]

where (U=0) near the start of migration and (U=1) near the breeding
destination.

This is not declared to be theoretical actionability (r).

## 7. Primary model

The primary model is:

[
Y_{ij}
=
alpha
+
eta_q q_j
+
eta_U U_j
+
eta_{qU} q_jU_j
+
b_f
+
b_{mathrm{year}}
+
b_{mathrm{individual}}
+
epsilon_{ij}.
]

The focal quantity is (eta_{qU}).

### Directional prediction

If increasing urgency reduces the behavioral value of otherwise predictive
information, then the benefit of predictability should weaken toward the
terminal route stages:

[
oxed{eta_{qU}>0}
]

under the absolute-error parameterization, because a negative main effect of
predictability on error becomes less negative at higher urgency.

Equivalent verbal prediction:

> high predictive connectivity improves timing most before the final
> high-urgency stages.

## 8. Competing prediction

If proximity to breeding makes environmental information more important rather
than less actionable, then:

[
eta_{qU}<0.
]

A null interaction means current data do not support stage-dependent use of
predictive information beyond additive route-position and predictability
effects.

All three outcomes are interpretable.

## 9. Stronger intermediate-peak test

The stronger actionability-balance prediction is **not** the primary test.

It is opened only if:
- at least four ordered route stages are represented within at least two
  flyways;
- cue predictability varies within route;
- timing error can be estimated at those stages without using the same data to
  define q.

Then a prespecified smooth or quadratic stage interaction may test whether the
predictability benefit peaks before the terminal stage.

No "hump" is claimed from three binned stages or visual inspection.

## 10. Required independence

Predictability must come from the historical spring-onset series and must not be
estimated from goose timing.

Urgency must come from route geometry / remaining distance and must not be
defined from stopover duration, migration speed, timing error, or departure
behavior.

The response is the observed goose timing relative to local spring.

## 11. Mandatory sensitivities

1. use phenology correlation coefficient r as q;
2. use proportionality index s as the alternative predictability measure;
3. analyze each flyway separately;
4. breeding attempts only;
5. exclude terminal breeding-site observations;
6. include ecological-barrier indicator;
7. use signed timing error instead of absolute error;
8. leave-one-stopover-region-out;
9. cluster uncertainty by stopover transition rather than treating visits as
   fully independent;
10. replace continuous U by ordered route-stage rank as a sensitivity only.

## 12. Admission gate

Do not fit the focal interaction unless:
- at least 10 distinct stopover transitions have independent q values;
- at least 3 route positions are represented;
- at least 30 individual stopover visits contribute to the response;
- at least two flyways contribute;
- q and U are not correlated at |r| >= 0.90 across transitions.

If the gate fails:

```text
V7_PRIMARY_TEST = NOT_ESTIMABLE
```

and no threshold is relaxed.

## 13. Claim ceiling

A supported focal interaction licenses only:

> The relationship between environmental predictability and realized migration
> timing varies with route position / urgency in this goose system.

It does not license:
- direct measurement of information value;
- direct measurement of actionability;
- proof that birds consciously estimate future spring;
- universal migration-deadline theory;
- causal fitness rescue.

## 14. Novelty gate

V7 remains open only if a current literature search finds no prior study that
directly tests an interaction between independently estimated environmental
predictability and independently defined route-stage urgency / remaining
opportunity on migratory timing or departure behavior.

If such a study is found:

```text
V7_PUBLICATION_ROUTE = CLOSE_PRIOR_ART
```

## 15. Outcome-access rule

Before this contract is committed:

- do not download/re-fit the Kölzsch individual tracking data;
- do not calculate q × U;
- do not inspect the interaction sign;
- do not bin stages by observed timing response.

Published aggregate results already known from Kölzsch et al. 2015 remain
prior-art context and are not treated as V7 outcome access.

```text
V7_CONTRACT = FROZEN_PREOUTCOME
V7_TRACKING_ROWS = UNOPENED_FOR_NEW_ANALYSIS
V7_FOCAL_INTERACTION = UNOPENED
```
