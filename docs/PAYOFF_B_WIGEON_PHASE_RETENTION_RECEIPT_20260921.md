# PAYOFF-B Eurasian wigeon phase-retention receipt

Frozen: 2026-09-21

Status: **prospective third-taxon phase-retention result promoted from source-backed PAYOFF-B macro analysis**.

## 1. Source provenance

Primary PAYOFF source branch:

    PR #144
    empirical/movement-phenology-macro-20260918
    head SHA:
        df79ddba9bcf7d8c8f77829fa7e9b8f670b36ff6

Preregistration:

    docs/MOVEMENT_PHENOLOGY_WIGEON_CONTROLLER_PREREGISTRATION.md
    blob SHA:
        e3b6b5d223a5707667883991f88197448729111c

Direct result receipt:

    docs/MOVEMENT_PHENOLOGY_WIGEON_DIRECT_RECEIPT.md
    blob SHA:
        d1a4014ce36a589cd32386890bb0cc5ee39fa478

Direct-controller registry:

    data/MOVEMENT_PHENOLOGY_DIRECT_CONTROLLER_REGISTRY.csv
    blob SHA:
        dea4917baa362e0805015151ae34c7de4456b1ae

Independent project-daily crosscheck:

    zuizui0223.github.io/research-daily/2026-09-21.md
    commit:
        41b9ed85e72a2d4abf74bb89b8db34834b531d44

Primary biological source:

    van Toor et al. (2021)
    Movement Ecology 9:61
    DOI 10.1186/s40462-021-00296-0

Tracking source:

    Movebank Data Repository
    DOI 10.5441/001/1.dv5mm289

Environmental reconstruction:

    NASA POWER daily T2M
    published 5 °C thermal-growing-season rule

## 2. Preregistered gates

The direct controller preregistration was frozen before the promoted wigeon
estimate was available.

### Reconstruction gates

Required:

    movement reconstruction close to the published spring-migration sample;
    independent environmental-phase reconstruction;
    >=30 consecutive staging transitions;
    >=10 individuals.

Observed:

    reconstructed tracks:
        33

    reconstructed individuals:
        29

    published tracks / individuals:
        35 / 31

    reconstructed median endpoint distance:
        1911 km

    published median endpoint distance:
        1899 km

    staging events with reconstructed TGS:
        256 / 256

    reconstructed median arrival phase:
        20.93 d after TGS onset

    published median arrival phase:
        22.5 d after TGS onset

Result:

    movement reconstruction gate:
        PASS

    environmental TGS gate:
        PASS

    transition-support gate:
        PASS

## 3. Primary prospective lambda test

For consecutive staging events the registered model was

    E_(i+1)
    = a + lambda E_i
      + route covariates
      + error.

The primary no-correction null was

    H0: lambda = 1.

Preregistered primary prediction:

    lambda < 1.

Data:

    consecutive staging transitions:
        224

    individuals:
        28

Equivalent change-model coefficient:

    beta_E = -0.14006

    cluster SE = 0.04509

    cluster p = 0.00442

Since

    lambda = 1 + beta_E,

the direct phase-retention estimate is

    lambda = 0.85994

    SE = 0.04509.

Direct test against no correction:

    H0: lambda = 1

    p = 0.00190.

Therefore:

    PRIMARY PHASE-RETENTION GATE:
        PASS.

The corresponding descriptive coordinates are

    R_phi = |lambda| = 0.860

and

    C_phi = 1-|lambda| = 0.140.

Thus the fitted observational transition removes about 14% of incoming phase
deviation per reconstructed staging-to-staging transition.

This is weaker correction than the strongest mule-deer and barnacle-goose
examples, but it is significantly different from complete retention.

## 4. Stronger preregistered / exploratory forecast

The preregistration also froze the stronger cross-system forecast

    |lambda| < 0.75.

Observed:

    |lambda| = 0.860.

Therefore:

    STRONG-CONTRACTION FORECAST:
        FAIL.

This failure is retained.

PAYOFF-B must not rewrite the wigeon result as confirmation of a universal
strong-correction coefficient.

## 5. System-specific actuator tests

### Stopover — formal prospective actuator gate

Registered directional prediction:

    S'(E) < 0.

The source-backed actuator registration is frozen in

    data/wigeon_stopover_actuator_registration_20260921.json

with the preregistered inferential support rule

    p <= 0.05.

Observed:

    stopover slope
        = -0.000140 day / phase-day

    cluster SE
        = 0.003902

    p
        = 0.972.

Thus the point estimate has the preregistered negative direction but the
inferential support requirement fails.

Machine interpretation:

    direction_passed:
        TRUE

    support_passed:
        FALSE

    formal actuator gate:
        FAIL.

Therefore:

    STOPOVER ACTUATOR:
        NOT SUPPORTED.

This distinction is important: PAYOFF-B does not count a nearly-zero coefficient
as actuator support merely because its sign happens to match the prediction.

The secondary registered stopover-gain band

    0.3 < g_S < 0.8

also fails.

### Travel speed

Observed:

    log travel-speed gain / phase-day
        = +0.00109

    cluster SE
        = 0.000824

    p
        = 0.197.

Therefore:

    TRAVEL-SPEED ACTUATOR:
        NOT SUPPORTED.

### Migration-distance moderation

Observed direct-controller moderation:

    beta = -0.0253
    SE = 0.0278
    p = 0.371.

Independent route-progress × endpoint-distance reconstruction:

    p = 0.670.

Therefore:

    DIRECT DISTANCE MODERATION:
        NOT SUPPORTED.

## 6. Gate interpretation

The source-backed wigeon result is now the canonical empirical example of

    lambda PASS
    actuator FAIL.

It supports

    shared phase-retention geometry

without supporting

    one shared speed / stopover actuator architecture.

This is exactly why PAYOFF-B now uses two independent gates.

The result should be read as

> wigeons retain significantly less than the full incoming phase deviation
> across consecutive staging transitions, but the measured stopover and
> between-staging speed variables do not explain that contraction.

It should not be read as

> wigeons use the same actuator as mule deer or barnacle geese.

## 7. Cross-system consequence

The macro branch already contains direct phase-retention estimates for:

    mule deer:
        lambda ~= 0.107

    barnacle goose:
        Svalbard  lambda = -0.106
        Greenland lambda = 0.131
        Barents   lambda = 0.494

    Eurasian wigeon:
        lambda = 0.85994.

The source branch deliberately does not estimate one universal lambda from
these values.

The licensed cross-system statement is instead:

> phase retention can be represented on a common response coordinate across
> distinct migratory systems, while retention strength and actuator
> architecture differ sharply.

Wigeon is the prospectively registered third-taxon test that both supports the
primary no-correction rejection and falsifies the stronger |lambda|<0.75
forecast.

## 8. Relationship to the current prospective-gate architecture

This receipt resolves the former PAYOFF-B status

    TRACKING_WIGEON_RETENTION_ACTUATOR_PATTERN_REPORTED_NUMERIC_RECEIPT_PENDING

to

    TRACKING_WIGEON_PROSPECTIVE_PHASE_RETENTION_RECEIPT_FROZEN.

It does **not** imply that every cross-system synthesis can pool the numerical
lambda values directly. The current synthesis layer still requires an explicit
common phase-coordinate ID and segment-scale contract.

The wigeon source analysis uses consecutive staging-to-staging transitions.
Any confirmatory pooled lambda analysis must therefore declare how other
systems map onto the same correction-opportunity scale before numerical
pooling.

## 9. Claim ceiling

Licensed:

- direct movement and environmental reconstruction gates pass;
- the preregistered primary lambda<1 prediction passes;
- lambda=0.85994 with SE=0.04509;
- no-correction lambda=1 is rejected at p=0.00190;
- the stronger |lambda|<0.75 forecast fails;
- the stopover actuator is not supported;
- the travel-speed actuator is not supported;
- distance moderation is not supported in the direct controller;
- lambda PASS / actuator FAIL is an observed prospective outcome.

Not licensed:

- universal lambda;
- universal correction fraction;
- universal stopover gain;
- a causal identification of the hidden wigeon actuator;
- treating the absence of measured speed/stopover effects as absence of all
  behavioral control;
- pooling lambda values across incompatible segment definitions without a
  predeclared scale map.
