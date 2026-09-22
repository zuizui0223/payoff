# Stage 3 — independent movement–phenology validation registry

Status: candidate systems registered; acquisition and harmonization not yet complete.

## Purpose

Stage 1 shows that a universal bird/green-up speed-ratio constant is not supported. The empirical target is now **phase locking**: under what conditions do animals preserve a characteristic lead/lag relative to a moving resource wave?

Stage 3 uses independent individual-tracking systems where resource phenology is either supplied with the dataset or can be reconstructed from published remote-sensing covariates.

The systems below are deliberately chosen to span different outcomes: close surfing, behavioral compensation, route predictability, anthropogenic decoupling, and active modification of the resource wave.

## Priority A — compensatory tracking

### Mule deer: phenological mismatch compensation

Dataset:

```text
Dryad DOI 10.5061/dryad.8kprr4xsj
Migration statistics and animal biometrics for mule deer that migrated
long-distances (2011–2020), Wyoming, USA
```

Published result motivating reuse:

- animals began migration across a very broad range of positions relative to spring green-up;
- late migrants moved faster and reduced stopover time;
- arrival at summer range was much more synchronized than migration onset.

PAYOFF-B use:

```text
Does movement plasticity reduce phase error as migration proceeds?
Is correction rate strongest when realized movement/resource timescales approach matching?
```

This is the highest-priority mechanistic validation because the published system already contains a natural "catch-up" process.

## Priority A — route predictability

### Barnacle geese: three flyways

Movebank Data Repository DOIs:

```text
Barents Sea: 10.5441/001/1.ps244r11
Svalbard:    10.5441/001/1.5k6b1364
Greenland:   10.5441/001/1.5d3f0664
```

The three routes differ in predictability of spring conditions among successive stopovers.

PAYOFF-B use:

```text
Does higher environmental predictability strengthen phase locking?
Do geese preserve route-specific nonzero phase offsets rather than minimizing zero lag?
Does the movement/resource timescale relation differ among flyways?
```

This system directly addresses the moderator that Stage 1 could not resolve from coarse species-level summaries.

## Priority A — avian migration distance contrast

### Eurasian wigeon

Movebank Data Repository DOI:

```text
10.5441/001/1.dv5mm289
```

Published study: migration distance affects how closely Eurasian wigeons follow spring phenology.

PAYOFF-B use:

```text
Does longer migration alter phase-locking error, matching timescale, or correction capacity?
```

This provides an avian individual-level replication independent of the Amaral population-front dataset.

## Priority B — classic green-wave surfing

### Mule deer: greenscape shapes surfing

Dataset:

```text
Dryad DOI 10.5061/dryad.7kc09
```

The published dataset contrasts observed migration against a theoretically perfect surfer and random movement.

PAYOFF-B use:

```text
Can the surfing score be recast as a phase-locking / timescale-matching response?
Do animals classified as better surfers show lower phase drift?
```

## Priority B — anthropogenic mechanism break

### Mule deer: industrial energy development

Dataset:

```text
Dryad DOI 10.5061/dryad.7d7wm37z5
```

The system reports decoupling of migration from the green wave where energy development occurs within corridors.

PAYOFF-B use:

```text
Does anthropogenic corridor modification increase phase drift
without requiring a change in the underlying environmental-wave speed?
```

This is a useful falsification / perturbation system rather than another positive replication.

## Priority B — alternative migration strategy

### Red deer: jump versus surf

Dataset:

```text
Dryad DOI 10.5061/dryad.3hr2c
```

The dataset contains GPS locations from a large Norwegian red-deer study. The published analysis distinguishes migrants that rapidly move between ranges from local phenology tracking.

PAYOFF-B use:

```text
Does the timescale-matching framework separate "jumping" from "surfing" strategies?
```

This is important because a successful migration strategy need not continuously surf a green wave.

## Priority C — endogenous phenology feedback

### Yellowstone bison

Dataset:

```text
Dryad DOI 10.5061/dryad.prr4xgxgz
```

The supplied data include animal/date and local peak-IRG timing. The published work shows that bison can alter vegetation phenology through grazing.

PAYOFF-B use:

```text
Negative control for an exogenous-wave assumption:
does simple movement-to-environment matching fail when movers modify the wave itself?
```

This system is especially valuable as a boundary case: the environment is not an externally imposed temporal driver.

## Harmonized quantities

Where raw trajectories and environmental timing are available, estimate:

```text
individual movement speed / progress along route
local resource-wave timing
local resource-wave speed
directional alignment
species- or individual-specific phase offset
phase residual
phase drift
stopover duration
```

Primary outcome:

```text
change in absolute phase residual along migration
```

rather than raw zero-lag error.

## Comparative predictions

```text
P1  High environmental predictability -> stronger phase locking.
P2  Behavioral speed/stopover plasticity -> faster correction of phase errors.
P3  Ecological barriers / development -> weaker phase locking.
P4  Jump migrants can succeed without continuous u_macro ~ 1.
P5  Endogenous resource modification can break the exogenous-wave prediction.
```

These predictions deliberately allow different migration strategies to produce different outcomes rather than forcing all taxa onto one global optimum.

## Promotion gate

A cross-system empirical paper becomes justified if at least two independent systems show that phase-error correction or phase stability is systematically related to movement/resource timescale matching, while one mechanistically interpretable system demonstrates a predicted failure mode.

Until then, the evidence should be presented as a comparative validation programme rather than a universal empirical law.
