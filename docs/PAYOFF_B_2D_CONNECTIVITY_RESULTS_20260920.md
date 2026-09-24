# PAYOFF-B two-dimensional connectivity results receipt

Frozen: 2026-09-20

This receipt freezes the first canonical synthetic results from the
two-dimensional moving-landscape extension of PAYOFF-B migration–phenology
tracking.

These are synthetic mechanism results under declared finite landscapes. They
are not calibrated climate thresholds, natural barrier frequencies, or
predictions for a named species.

## 1. Why two dimensions matter

The 2D layer is not a cosmetic extension of the one-dimensional model.

Climate moves along a declared axis, while local movement occurs among four
cardinal neighbors. Habitat quality can make cells unavailable, so vertical
walls with finite gaps and staggered multiple walls create route geometry that
cannot be represented by a one-dimensional projection.

The core causal chain is

    moving climate
    -> spatial route demand
    -> phenological buffering
    -> corridor crossing / detour
    -> interaction matching
    -> evolutionary accessibility
    -> persistence.

Low-density growth remains the evolutionary fitness estimand. Density
regulation affects population dynamics only.

## 2. Space–time substitution under connectivity constraints

### 2.1 Centered versus displaced single corridors

At a 31 x 15 landscape with a wall four cells east of the initial optimum,
strategy-grid resolution 7 x 7, and phenology limits 2 or 4, the sampled
persistence frontier was unchanged by corridor width or by moving the gap six
cells away from the climate axis.

For gap widths 1, 3, and fully open width 15:

    z_max = 2:
        max persisted climate velocity = 0.065
        first failed velocity          = 0.070

    z_max = 4:
        max persisted climate velocity = 0.085
        first failed velocity          = 0.090

The same brackets occurred for centered and offset-6 gaps.

The geometry still changed how much spatial crossing occurred. For example at
the sampled frontier:

    gap width 1, z_max=2:
        centered mean crossing = 0.6945
        offset-6 mean crossing = 0.6654

    gap width 1, z_max=4:
        centered mean crossing = 0.7909
        offset-6 mean crossing = 0.7632.

Thus route geometry changes the spatial realization of tracking without moving
the sampled survival frontier in this declared regime.

### 2.2 Temporal bypass and re-entry of spatial tracking

The strongest qualitative pattern appears when phenological capacity is large.

In the 7 x 7 zigzag-route resolution check, for z_max=4:

    climate velocity 0.04:
        optimal migration = 0
        optimal phenology = 0.333...
        essentially no second-wall crossing

    climate velocity 0.05:
        optimal migration = 0
        optimal phenology = 0.333...
        essentially no second-wall crossing

    climate velocity 0.06:
        optimal migration = 0.166...
        optimal phenology = 0.166...
        mean second-wall crossing = 0.132

    climate velocity 0.07:
        optimal migration = 0.333...
        optimal phenology = 0.166...
        mean second-wall crossing = 0.314.

The interpretation is a three-stage tracking sequence:

    temporal bypass
    -> mixed spatial + temporal tracking
    -> increasingly spatial tracking near the limit.

Phenology can temporarily substitute for movement through a constrained route,
but spatial redistribution re-enters as directional climate forcing becomes
too large.

## 3. Phenology buffers geometric route penalties

A two-wall zigzag route was compared with open and straight routes at climate
velocities 0.04, 0.05, 0.06, and 0.07.

With the 7 x 7 strategy grid, the mean low-density growth penalty of zigzag
relative to open habitat was:

    phenology limit 0:
        -0.04188795

    phenology limit 2:
        -0.03314147

    phenology limit 4:
        -0.00699570.

The magnitude of the route penalty therefore fell by about 83% between
z_max=0 and z_max=4.

In this sampled design, open and zigzag habitats had the same persistence
counts at each phenology limit. The retained claim is therefore **temporal
buffering of route cost**, not a demonstrated persistence rescue caused by
phenology in this particular geometry.

## 4. A temporal-bypass capacity diagnostic

For a lineage constrained to habitat before a wall, the best-case terminal
phenology-only velocity ceiling is

    v_bypass
    =
    [g x_max
     + s z_max
     + sqrt(2 (g0 - C_h) / A)]
    / T,

where x_max is the most climate-advanced accessible cell, C_h is phenology
architecture cost, A is abiotic mismatch strength, and T is the declared
finite horizon.

This is a terminal best-case capacity diagnostic, not a persistence theorem.

For the canonical first-wall geometry:

    z_max=4, h≈1/3

gives a ceiling between 0.05 and 0.06.

That matches the observed qualitative switch:

    v=0.05:
        phenology-only tracking remains optimal,

    v=0.06:
        spatial migration re-enters the optimal strategy.

The diagnostic therefore explains why temporal bypass has a finite operating
range instead of being an unlimited substitute for movement.

## 5. Two-dimensional coevolutionary coordination barriers

### 5.1 Coarse mutation step

The first 2D coevolution design varied:

    interaction strength:
        0, 0.5, 1.0

    geometry:
        open, straight two-wall, zigzag two-wall

    climate velocity:
        0.05, 0.06

    phenology limit:
        2, 4

with unilateral mutation step 0.2.

At interaction strength 0:

    barriers = 0/4 in every geometry
    persistence rescues = 0/4 in every geometry.

At interaction strength 0.5:

    open:     3/4 barriers, 3/4 rescues
    straight: 3/4 barriers, 3/4 rescues
    zigzag:   3/4 barriers, 3/4 rescues.

At interaction strength 1:

    open:     4/4 barriers, 4/4 rescues
    straight: 4/4 barriers, 4/4 rescues
    zigzag:   4/4 barriers, 4/4 rescues.

Thus the coordination barrier disappears without interaction and appears across
all sampled connectivity geometries when partner matching matters.

### 5.2 Mutation-step resolution

The positive-interaction subset was rerun with unilateral mutation step 0.1.

Across 24 cells:

    barriers:             22/24
    persistence rescues:  21/24.

Breakdown:

    interaction 0.5:
        open     3/4 barriers, 3/4 rescues
        straight 3/4 barriers, 3/4 rescues
        zigzag   4/4 barriers, 3/4 rescues

    interaction 1.0:
        open     4/4 barriers, 4/4 rescues
        straight 4/4 barriers, 4/4 rescues
        zigzag   4/4 barriers, 4/4 rescues.

The barrier therefore does not disappear when the mutation lattice is refined.

The strongest retained ecological hotspot remains

    zigzag geometry
    climate velocity = 0.06
    phenology limit  = 4.

At the fine mutation step, one representative strongest row has

    local endpoint:
        migration 0.3
        phenology 0
        low-density joint growth ≈ -0.824
        extinct

    coordinated matched optimum:
        migration 0.1
        phenology 0.2
        low-density joint growth ≈ +0.259
        persists

    accessibility gap ≈ 1.083.

## 6. Direct local coordination-gate audit

The canonical zigzag cell was audited at one declared mutation step.

Resident matched strategy:

    (migration, phenology) = (0.2, 0).

Coordinated neighbor:

    (0.2, 0.2).

Results:

    resident joint growth:
        -0.840083
        extinct

    coordinated joint growth:
        +0.254889
        persists

    coordinated joint gain:
        +1.094972

    species A unilateral gain:
        -5.945681

    species B unilateral gain:
        -5.945681

    unilateral interaction mismatch:
        3.747280.

Therefore the 2D coordination barrier is local and mechanistic:

> The same phenological step is strongly beneficial when both partners make it
> together, but catastrophically deleterious when either partner moves first.

This direct sign pattern is now part of the standard repository CI.

## 7. Robustness to distribution-level overlap

The baseline 2D interaction term uses spatial centroids and phenological
difference. Because two distributions can share a centroid while occupying
different patches, an optional Bhattacharyya-overlap penalty was added:

    overlap B
    = sum_i sqrt(p_i q_i),

with an additional interaction mismatch proportional to

    1 - B.

The default overlap scale is zero, so canonical results remain unchanged.

The canonical zigzag gate was tested with overlap scales:

    0, 0.5, 1, 2.

For every scale:

    coordination barrier = true
    persistence rescue   = true
    fixed one-step gate  = true.

The unilateral mutant/resident spatial distributions had very low normalized
overlap, approximately 0.07.

As overlap sensitivity increased, the unilateral mutation became still more
deleterious:

    scale 0:
        unilateral gain = -5.946

    scale 0.5:
        -6.065

    scale 1:
        -6.420

    scale 2:
        -7.804.

Thus the barrier is not an artefact of reducing two-dimensional spatial
distributions to their centroids. Explicit local segregation strengthens the
coordination gate in the sampled canonical cell.

## 8. Partner-specific tracking preferences

Species-specific architecture costs were varied through independent cost biases

    phenology cost - migration cost
    in {-0.08, 0, +0.08}

for each partner.

### Moderate forcing: climate velocity 0.04

Without interaction:

    all 9 pairs persisted,

but partner-specific quantitative strategies could differ. For opposed cost
biases, the mean strategy distance was 0.2 and interaction mismatch was larger.

With interaction strength 0.5 or 1:

    strategy distance collapsed to 0,
    interaction mismatch fell to about 0.0044,
    all 9 pairs persisted.

In this regime interaction acts as a **tracking synchronizer**.

### Strong forcing: climate velocity 0.06

Without interaction:

    all 9 pairs converged to matched mixed tracking around
    (migration,phenology)=(0.2,0.2)
    and persisted.

With interaction strength 0.5 or 1:

    all 9 pairs converged to the same spatially biased / migration-only
    local endpoint,
    and all 9 pairs went extinct.

Thus the same interaction-mediated synchronization that aligns tracking under
moderate forcing can become **maladaptive synchronization** under stronger
forcing.

The retained interpretation is not that interaction is inherently beneficial
or harmful. Its effect depends on where the synchronized local attractor lies
relative to the moving-environment persistence envelope.

## 9. Robustness to anisotropic movement

The regular-grid baseline disperses equally along x and y. To test whether the
temporal-buffering result depends on isotropic movement, the x movement weight
was fixed at 1 and the transverse y weight was reduced through

    y/x weight ratio:
        1, 0.5, 0.25, 0.1.

The same open-versus-zigzag comparison was rerun at climate velocities

    0.05, 0.06, 0.07

and phenology limits

    0, 2, 4

with a 7 x 7 strategy grid.

At phenology limit 0, the mean zigzag low-density growth penalty became
progressively larger as transverse movement became harder:

    y/x = 1:
        -0.04501

    y/x = 0.5:
        -0.04864

    y/x = 0.25:
        -0.04961

    y/x = 0.1:
        -0.05249.

Phenological capacity strongly buffered that penalty at every anisotropy level.
At phenology limit 4 the corresponding penalties were

    -0.01073,
    -0.01161,
    -0.01203,
    -0.01285.

Thus increasing the phenology limit from 0 to 4 reduced the magnitude of the
zigzag penalty by approximately

    76.2%, 76.1%, 75.8%, and 75.5%

across the four sampled movement anisotropies. Averaged across anisotropy
levels, the penalty magnitude fell by about 75.9%.

No sampled open-versus-zigzag persistence loss occurred in this design at any
anisotropy level. The retained result is therefore:

> temporal buffering of route-growth costs survives strong directional
> movement anisotropy,

not a demonstrated anisotropy-specific persistence rescue.

The movement kernel retains its original isotropic behavior at the default
weights w_x=w_y=1, and exact mass conservation is regression-tested for
anisotropic weights.

## 10. Retained 2D synthesis

The two-dimensional model supports three nested mechanism claims.

### A. Temporal buffering of connectivity costs

Phenology reduces the growth cost of spatial detours and can temporarily let a
population avoid corridor crossing altogether.

### B. Finite temporal bypass

Temporal buffering has a capacity ceiling. At sufficiently fast environmental
movement, spatial tracking necessarily re-enters and ultimately fails.

### C. Interaction-mediated synchronization and coordination gates

Partner matching can align tracking strategies, but the synchronized local
strategy can be jointly suboptimal. Under strong forcing, unilateral escape can
be selected against even when a coordinated alternative changes extinction
into persistence.

In compact form:

    route geometry
    x temporal buffer
    x partner matching
    ->
    temporal bypass
    -> spatial re-entry
    -> synchronization
    -> possible coordination lock
    -> persistence or extinction.

## 11. Claim ceiling

These results do not establish:

- empirical corridor-width thresholds;
- a universal climate-velocity frontier;
- a universal 83% buffering effect;
- natural prevalence of coordination barriers;
- that interacting species use identical movement or phenological mechanisms;
- that real habitat resistance is binary;
- that real populations follow four-neighbor lattice dispersal;
- that any named system occupies the sampled parameter regimes.

The strongest statements are synthetic mechanism results with explicit
provenance and declared finite landscapes.

## 12. Provenance

Canonical workflow artifacts:

1. Centered 2D high-velocity frontier resolution
   - workflow run: 35476324392
   - artifact: 10594321600
   - sha256: 16e10954c8cca0448cb4b17c13aefd838dd799c7eb840eec0f795b08816b2bd6

2. Offset-6 2D high-velocity frontier resolution
   - workflow run: 35476324392
   - artifact: 10593174785
   - sha256: bb903a0fe7dc7103284695e6c185bd4daae325374ecba03100ccdef9d8c7003e

3. Zigzag strategy-resolution check
   - workflow run: 35476611109
   - artifact: 10593374777
   - sha256: 9c23e0ee6c5724b1f2d7dc37433bad706104ad5c47324fee264304ab6cb001c1

4. 2D coevolution coarse pilot
   - workflow run: 35476662171
   - artifact: 10594646436
   - sha256: 5a8b7a1aa13324f8db0d1ff9ce877045520828901a9f0f90021989acac44b3d1

5. 2D coevolution mutation-step resolution
   - workflow run: 35478423904
   - artifact: 10595351557
   - sha256: bfadc9e26f1208cace85e5f9cb44bc050b1e50ffab154f547d19642ccbde911a

6. Distribution-overlap sensitivity
   - workflow run: 35478538667
   - artifact: 10595076778
   - sha256: 5bd1d575e686d58c30991ee48daa107b8e38d901f6e0ade674af2e08adec7108

7. Strong-forcing partner-asymmetry pilot
   - workflow run: 35478704014
   - artifact: 10595407391
   - sha256: 0867ec0fca88a8ff0fb90bd52723e3066c1acdde369b5fcb287d7954b27e19cf

8. Moderate-forcing partner-asymmetry pilot
   - workflow run: 35478835579
   - artifact: 10594734226
   - sha256: 42674ddb42b8fc0ca30847838db7fbd6e9c8b0dbe65aae7b6f718ca3332141cb

9. Anisotropic-movement sensitivity
   - workflow run: 35479512321
   - artifact: 10595182956
   - sha256: a151aa4b37892f73e7f11ad53b73685bca2bd533d9c2ccf31b480ee1ddd6068e

The direct canonical gate is also exercised in standard CI; one verified run is
workflow 35478420135, job 105991651172.
