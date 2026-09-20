# Structured prior-art search — movement–phenology phase retention

Status date: 2026-09-20.

Status: **structured web literature screen complete for the GEB submission lane; not an exhaustive bibliometric systematic review.**

## Search question

Does prior literature already combine the following empirical package?

```text
within-migration phenological phase
+ signed/absolute phase retention after one movement opportunity
+ a common cross-taxon retention coordinate lambda
+ separation of environmental innovation from behavioral retention
+ actuator-specific mechanism below that common coordinate
+ perturbation / endogeneity boundary tests
```

## Search families

The screen covered combinations of:

```text
"phase retention" + migration / phenology
"phase transfer" + migration / phenology
"phase error" + migration / green wave
"phase locking" + migration / phenology
feedback / feed-forward + migration timing
control theory + animal migration / phenology
state-space / autoregressive + migration phenology
predictive cues + migration timing
reaction norms + green-up + migration
cue accuracy / cue efficacy + phenological mismatch
phenological navigation
circannual phase / phase response + migration
```

Searches were run across publisher pages, PubMed/PMC, OpenAlex-indexed pages,
Royal Society, Wiley, Springer Nature and related scholarly web results.

## Closest prior-art families

### 1. Autoregressive phenology models are old prior art

Post et al. (2001), *Proceedings of the Royal Society B*,
DOI 10.1098/rspb.2000.1324, developed a general autoregressive model for
life-history timing under climate variation.

Forchhammer et al. (2002), *Journal of Animal Ecology*,
DOI 10.1046/j.1365-2656.2002.00664.x, applied autoregressive timing models to
spring arrival of long- and short-distance migratory birds. Their direct
temporal-dependence coefficient was often below one.

This is an important claim boundary.

Therefore PAYOFF-B must **not** claim that:

```text
using lambda-like retention coefficients in phenological time series is new

or

autoregressive contraction in migration timing is new
```

The distinction is that those studies quantify **year-to-year temporal
dependence in calendar arrival dates**, whereas the current programme estimates
**within-migration retention of animal-minus-environment phase across an
ecologically meaningful correction interval**.

### 2. Chronobiological phase concepts are established

The chronobiology literature has long used:

```text
phase angle
phase response curves
entrainment
circannual phase relationships
Zeitgeber response
```

for seasonal timing in birds and other animals.

Examples include circannual phase-response and avian migration-clock work, and
the broader review literature on phenology, seasonal timing and circannual
rhythms.

Therefore the words `phase`, `phase locking`, `entrainment`, or `phase
response` are **not** themselves novelty claims.

The manuscript should define its usage narrowly:

> ecological phase = animal timing minus environmental timing at a movement
> stage.

### 3. Environmental information / predictive cues are established

Bauer, McNamara & Barta (2020), *Proceedings of the Royal Society B*,
DOI 10.1098/rspb.2020.0622, explicitly model environmental variability,
predictability, information reliability and optimal migration timing.

Kölzsch et al. (2015), *Journal of Animal Ecology*,
DOI 10.1111/1365-2656.12281, empirically link predictability among stopovers to
migration timing.

Bourski (2026), *Journal of Animal Ecology*,
DOI 10.1111/1365-2656.70230, proposes environmental phenology and
"phenological navigation" as an explanation for spring migration timing.

Therefore the information / prediction axis is prior art.

### 4. Cue accuracy and fitness consequences are already separated

Torstenson & Shaw (2025), *Oikos*, DOI 10.1111/oik.10862, explicitly
distinguish cue accuracy from cue efficacy and model the fitness consequences of
phenological change under different cue types and seasonal amplitudes.

Therefore the PAYOFF-B manuscript should not imply that it is the first to
separate timing error from fitness or to distinguish cue types.

Its different contribution is to separate:

```text
environmental innovation entering the next stage
from
retention of already-realized phase error after movement
```

### 5. Behavioral plasticity and compensatory correction are established

Ortega et al. (2023), *Nature Communications*,
DOI 10.1038/s41467-023-37750-z, directly demonstrate en-route behavioral
compensation for phenological mismatch in mule deer.

Laforge et al. (2025), *Ecology Letters*, DOI 10.1111/ele.70101, quantify
individual variation and reaction-norm plasticity in ungulate migration timing.

Chauveau et al. (2025), *Journal of Animal Ecology*,
DOI 10.1111/1365-2656.70031, show longitudinal plastic adjustment of migration
timing to green-up in Alpine ibex.

Therefore:

```text
animals plastically adjust migration to phenology
```

is firmly prior art.

### 6. Broad control-theoretic language is prior art

Berthold's avian migration framework explicitly uses "control and adaptability"
in the broad biological sense.

A 2026 University of Bath doctoral thesis develops formal robust/adaptive
control methods for conservation of migratory species.

Neither is a direct match to the current within-migration phenological
phase-retention coordinate, but together they rule out broad claims that
"control theory has not been applied to migration."

### 7. Alternative strategies and environmental endogeneity are prior art

The green-wave literature already includes continuous surfing, jumping,
overtaking and compensatory movement.

Geremia et al. (2019), *PNAS*, DOI 10.1073/pnas.1913783116, explicitly show
that migrating bison can engineer vegetation phenology.

Thus the strategy labels and endogeneity concept are supporting synthesis, not
stand-alone discoveries.

## Closest conceptual overlap identified

The closest mathematical overlap is Forchhammer et al. (2002):

```text
calendar arrival_t
~ retention * calendar arrival_(t-1)
+ climate
```

The current programme instead estimates:

```text
animal-environment phase_(next movement stage)
~ lambda * animal-environment phase_(current movement stage)
+ route covariates
```

and independently estimates environmental innovation between spatial stages.

That distinction should be explicit in the manuscript because it protects the
candidate novelty from an avoidable AR-model priority problem.

## Search outcome

The structured screen **did not identify** a prior animal-migration study that
uses the full empirical package below as a declared cross-taxon framework:

```text
1. directly reconstructed within-migration animal-environment phase E
2. E_next ~ lambda E_current as a common cross-system response
3. direct estimates across multiple taxa with different movement architectures
4. environmental innovation sigma_xi estimated separately from lambda
5. actuator-specific gains nested below the common lambda coordinate
6. quantitative actuation perturbation plus environmental-endogeneity boundary
```

This is evidence for a **candidate synthesis / measurement contribution**, not
proof of absolute first priority.

## Revised novelty statement licensed for GEB

Recommended wording:

> We introduce a common empirical phase-retention coordinate for comparing how
> phenological deviation is transformed across ecologically meaningful movement
> intervals, and separate this retention from environmental timing innovation.
> Applying the same conceptual coordinate to directly reconstructed migration
> systems reveals that phase contraction is portable across taxa while its
> strength and behavioral implementation are strongly context dependent.

Avoid:

```text
first control theory of migration
first autoregressive model of migration timing
first phase model of migration
first evidence of phenological compensation
first demonstration that information affects migration
universal phase-control law
```

## Novelty gate

For the **GEB Research Article** lane:

```text
structured targeted search:                 PASS
major adjacent prior-art families mapped:   PASS
closest AR/chronobiology overlaps handled:  PASS
exact combined empirical package found:     NO
conservative claim wording available:       PASS
```

For an **Ecology Letters** flagship-first claim:

```text
formal database-level systematic search:
  STILL OPEN

forward/backward citation graph audit:
  STILL OPEN

claim of first / unique general framework:
  NOT LICENSED
```

The current evidence is sufficient to write a conservative GEB novelty claim
without asserting exhaustive priority.
