# PAYOFF-B: conditional forecast-innovation test of en-route change — design HOLD

Date: 2026-10-08.
Status: **conditional next-test design, not a preregistration and no source data fit**.
Rüppel et al. 2023 had already published weather-linked departure,
offshore/coastal routing and interrupted flights. Their Figshare 6403996
source gate must establish the grain/chronology and sample **before** this
test is allowed; do not equate supplementary figure tables with raw
flight-by-flight weather, decisions and no-event risk sets.

## The distinction existing published work does not by itself settle

Let I0 contain what is known when a bird departs: individual, calendar
day, origin weather, predicted weather en route and feasible options.
Let W1 be *information arriving after the departure commitment but
before the route/landing action*. A crude landing~W1 coefficient can
arise with a pre-planned weather-responsive rule, correlated origin
weather, fixed social patterns, or a true revision to new information.

The only incremental *information* question is:

    Does new, later-available weather W1 improve OUT-OF-YEAR/INDIVIDUAL
    forecast of a subsequent landing/routing decision, conditional on
    I0 and a forecast for W1 available at I0?

This is not automatically cognition, planning or fitness optimization.
It distinguishes statistical information arriving later from a
strictly origin-information-only description, under measurement,
comparability and detection assumptions.

## Competing risk-set models (conditional on the source passing)

Unit = bird x decision-eligible flight segment x time interval.
Require flight in progress at the start of that interval and an actual
opportunity to land or continue, with receiver detection/censoring
accounted for. Failure to assemble non-landing risk intervals or
pre-choice weather means SOURCE/HYPOTHESIS HOLD rather than a regression
with only landing events.

- B0 open-loop calendar/ID: season clock, bird identity or prior
  migration propensity, route/weather information known BEFORE
  departing, and previous flight state.
- B1 departure forecast: B0 + prospectively reconstructable
  origin-time forecast E[W1|I0] for the exact later place/time,
  fitted ONLY from earlier environmental data (no realised flight
  decisions or postevent weather used to train it).
- B2 route-updated information: B1 + forecast innovation
  W1-E[W1|I0], timestamped BEFORE the landing/route decision,
  with detection quality and spatial-time dependences.
- B3 behavior+payoff: only if actual remaining physically feasible
  alternatives, independent energetic cost and demographic endpoints
  are measured in the same subject; otherwise MUST NOT be run.

Main exploratory comparison B1 vs B2: paired heldout log-loss/Brier
gain with bird and weather-episode dependency and year-held-out folds.
B0 vs B1 is a different predeparture forecast question. Comparing a
model with observed future W1 to a baseline without forecast access is
not sufficient because W1 may be postdecision or a direct weather
hazard correlated with the environment at departure.

## Identifiability warning: weather contingency is not re-planning

A fixed conditional rule decided before departure,

    if headwind encountered later exceeds a threshold, land;

and a process of dynamically revising a prior intended non-stop
flight after new headwind information can generate the **same**
observed wind–landing response. An immediate physical constraint
(e.g. insufficient remaining flight range under headwind) can do so
as well. This is a basic observational equivalence in sequential
decision theory, NOT a novel theorem.

Merely adding contemporaneous W1 after origin W0 to a flight-level
landing regression can show that **later weather has incremental
predictive information**. It does not show a new *policy* was learned
or that animals made accurate subjective predictions. To establish
policy revision, one would additionally need at least one of:
- a separately recorded plan or probability forecast before departure
  and a different updated plan before landing;
- experimental access to equivalent observed weather under different
  predeparture information sets with independent feasible actions;
- repeated policy choices under matched weather, varying verified
  forecast histories while accounting for birds' habits and route
  social structure.

The Rüppel original source has one observed flight per tracked bird
(178/178), **no archived departure-issued forecast of its later flight
weather**, and no flight-in-progress land/continue risk intervals.
The authors already included northward wind change during flight in
their landing model. Thus current case is a **source-gated
observational benchmark**, not a new learned-controller test.

## Required diagnostic negative controls

1. **Temporal gate**: all covariates for B2 are measured strictly before
   the decision, not after a completed landing or via destination
   conditions recorded days later. Time-stamp source latency included.
2. **False early cue**: weather reports measured AFTER landing cannot be
   valid predictors at that decision. If such postevent data improve
   a retrospective model, this is a leakage detector, NOT evidence of
   foresight.
3. **Forecast innovation null**: if current weather equals a perfect
   departure forecast with zero forecast error, B2 cannot have
   *incremental information* over B1 (excluding model and sampling noise).
4. **Calendar + individual offset**: a model with fixed bird/year
   schedules can produce arrival/stay correlations and must be assessed,
   using complete episode/clustering support.
5. **Censored receiver tracks**: lost detections cannot be silently
   interpreted as flight continuation or landing; estimate/weight
   detection when supported by the telemetry design.
6. **Spatial-weather pseudo replication**: weather on the same evening
   shared by many birds gives fewer effective independent conditions
   than bird x hour rows imply.
7. **Original Rüppel 2023 prior art**: if B2 is no more than their
   original landing versus headwind/overcast analysis, the novelty
   claim FAILS even when p is small.

## What would and would NOT advance PAYOFF-B

- Positive B1 to B2 out-of-year skill, with a correct time gate, shows
  the functional **incremental value of a later environmental variable**
  for predicting a later observed action; it does not identify cognitive
  surprise, causal flexibility or benefits of landing.
- B2 no better than B1 does NOT prove no cue use if the archive has
  limited weather variation, receiver coverage, route heterogeneity
  or small conditional risk support.
- An alternative action's **feasibility** is not observed merely because
  another bird took it under different wind. Estimating potential
  landing opportunities requires independent behavioral/biomechanical
  constraints and terrain/route accessibility.
- Without same-individual demographic or partner-phenology outcomes,
  *optimal timing* and interspecific coordination benefits remain
  UNIDENTIFIED regardless of any positive B2 predictive gain.

## Source and existing evidence

- Rüppel et al. 2023, Royal Society Open Science 10:221420,
  https://doi.org/10.1098/rsos.221420
- Public supplement collection:
  https://doi.org/10.6084/m9.figshare.c.6403996
- Conditional source-only Figshare audit:
  scripts/payoff_b_ruppel_figshare_source_gate.py
- Existing goose/calendar and houbara/origin-cue gates are negative
  examples of what NOT to call direct feedback or decision-time
  information.

**Admission outcome remains unresolved until the actual Figshare source
audit has returned. Do not report any B0–B2 coefficients until then.**
