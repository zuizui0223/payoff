# PAYOFF public-raw / generic-game / architecture-mapping lane contract v1

Status: canonical empirical anti-conflation contract.

The empirical programme is split into three non-substitutable lanes.

```text
Lane R  public raw archive reconstruction
Lane G  generic frequency-game validation
Lane A  architecture mapping

                    G PASS
                      \
                       >--- alignment gate ---> architecture-specific E1 claim
                      /
                    A PASS

R is provenance/auditability infrastructure.  It may support G, but it never
supplies architecture semantics and never promotes a claim by itself.
```

## 1. Lane R — public raw archive reconstruction

Question:

> Can the public evidence object be reconstructed faithfully enough that another analyst can recover the declared tables, variables and transformations?

Allowed outputs:

```text
archive identity / DOI / repository commit
file manifest
byte acquisition state
checksums
schema / sheet / table reconstruction
identifier and treatment dictionaries
transformation recipes
reproduction of the source analysis
```

Forbidden outputs:

```text
this is a stable coexistence game
this strategy is shared/integrated
this strategy is differentiated/released
eta is positive/negative
PAYOFF E1 is supported
```

### R levels

```text
R0  archive metadata / file identity located
R1  bytes acquired and checksum pinned
R2  manifest and data schema reconstructed
R3  transformations / analysis-ready table reconstructed
R4  published analysis or registered target analysis reproduced
```

`R4` does not imply Lane G or Lane A.

## 2. Lane G — generic game validation

Question:

> Treating the alternatives only as neutral strategy labels, does relative performance depend on composition in the way claimed by the generic game layer?

The alternatives must remain architecture-neutral in this lane, for example

```text
strategy_1 / strategy_2
strain_A / strain_B
generalist / specialist only as source biological names
```

but **not**

```text
shared architecture / differentiated architecture
```

unless that semantic mapping has already been independently certified in Lane A.
Even then, the Lane G receipt itself remains neutral.

Allowed outputs include:

```text
frequency support
common outcome scale
oriented rare-invasion signs
set-valued phase identification
observed-range frequency response
affine no-refit compatibility / rejection
context dependence
time-horizon validity
```

A successful Lane G result licenses a **generic game-layer claim only**.

## 3. Lane A — architecture mapping

Question:

> Independently of the observed frequency-game result, do the two empirical alternatives instantiate PAYOFF's integrated/shared versus differentiated/released architecture contrast?

The minimum mapping evidence is

```text
A1 integrated/shared candidate explicitly defined
A2 differentiated/released candidate explicitly defined
A3 same net biological task/outcome
A4 stable/heritable strategic unit
A5 functional/unit consistency between the two alternatives
A6 mapping justified independently of the frequency-game outcome
```

Forbidden reasoning:

```text
rare-type advantage exists
therefore the rare type is differentiated

coexistence occurs
therefore this must be a shared-vs-differentiated PAYOFF game

specialists outperform WT
therefore the specialist consortium is automatically one D architecture
```

Lane A may be strong even when no frequency experiment exists.

## 4. E1 promotion is an intersection, not a relabeling

Architecture-specific frequency feedback is licensed only when

```text
G is certified
AND A is certified
AND same system
AND same empirical comparison
AND same strategic unit
AND explicit pair alignment is independently declared.
```

Symbolically,

```text
E1 = G ∩ A ∩ ALIGNMENT.
```

Raw reconstruction is tracked orthogonally:

```text
R -> provenance strength / reproducibility
```

If Lane G says its evidence source is the raw archive, then the relevant Lane R
receipt must match the same `system_id` and `dataset_id` and must have a certified
reconstruction.  Published-text Lane G evidence can remain valid even while R is
incomplete; it is simply weaker for numerical reanalysis and auditability.

## 5. Current examples

### Pseudomonas stutzeri

```text
R: public ERIC archive identified; full raw reconstruction not yet certified
G: PASS at the published-sign level
   pH 6.5 reciprocal invasion recovered
   pH 7.5 partial phase recovered
A: FAIL / not established
   complete-pathway generalist vs nitrite-only specialist is not a validated
   PAYOFF integrated-vs-differentiated architecture pair
E1: NO
```

### Streptomyces coelicolor

```text
R: not the current bottleneck
G: frequency assays exist for specialist cells vs WT cells
A: strong architecture-level evidence exists for terminal differentiation
ALIGNMENT: FAIL
   G varies CELL identity while A concerns COLONY ARCHITECTURE
E1: NO
```

### evolved E. coli cross-feeding consortium

```text
R: numerical reconstruction remains a separate task
G: direct consortium-vs-ancestor competition exists, but only one total S:D ratio
A: actual generalist-to-differentiated ecological transition is strong, but D is
   a multigenotype consortium and unit consistency remains open
E1: NO
```

### Beck et al. synthetic E. coli

```text
R: public GitHub workbook identified; binary workbook not yet reconstructed here
G: numeric generic comparison pending R
A: static generalist-vs-pathway-partitioned consortium mapping can be assessed
   independently of the eventual numeric result
E1: NO
```

## 6. Separate work queues

### Raw reconstruction queue

```text
R1  Pseudomonas stutzeri ERIC archive
    target: recover short-window trajectory tables and reproduce reciprocal tests

R2  Beck et al. synthetic E. coli GitHub workbook
    target: reconstruct WT-vs-consortium environment-dependent payoff tables

R3  Arabidopsis halleri Dryad workbook
    target: reconstruct mesocosm composition x reproduction tables
```

### Architecture mapping queue

```text
A1  Streptomyces coelicolor
    target: define colony-level S and D architecture units and identify whether a
    matched generalist-only heritable comparator actually exists

A2  evolved E. coli cross-feeding lineage
    target: adjudicate whether a stable multigenotype consortium can count as the
    strategic D unit without silently changing the unit of selection

A3  plant SCH/BITA systems
    target: search for a directly comparable integrated versus released pair on
    one common reproductive-fitness scale
```

A candidate can be high priority in one queue and low priority in the other.
That is intentional.

## 7. Machine guard

Canonical implementation:

```text
src/evidence_lane_separation.py
```

The code explicitly prevents

```text
R success -> G promotion
R success -> A promotion
G success -> A promotion
A success -> G promotion
```

and licenses architecture-specific promotion only through the explicit alignment
gate.

## 8. Current programme status

```text
RAW_RECONSTRUCTION_LANE_SEPARATED
GENERIC_GAME_VALIDATION_LANE_SEPARATED
ARCHITECTURE_MAPPING_LANE_SEPARATED
ARCHITECTURE_SPECIFIC_PROMOTION_REQUIRES_G_AND_A_AND_ALIGNMENT
GENERIC_GAME_VALIDATION_CANNOT_PROMOTE_ARCHITECTURE_SEMANTICS
RAW_ARCHIVE_RECONSTRUCTION_CANNOT_PROMOTE_GAME_OR_ARCHITECTURE_CLAIMS
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
```
