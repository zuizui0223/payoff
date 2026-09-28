# PAYOFF-B cross-system information-distance result

Date: **2026-09-28**  
Status: **promotion gate passed; candidate E6 for Paper 2**  
Branch: `analysis/payoff-b-cross-system-information-20260928`  
Frozen workflow run: **36383988920**  
Frozen head: `5c6122fdb83ffed058749eaa6f27266f7635276a`

## Question

Does phenological responsiveness weaken when a seasonal decision must be made
using information farther removed from the ecological state that ultimately
needs to be matched?

This is tested in two deliberately separated lanes:

1. a within-source migratory-bird meta-regression, where migration distance is
   an explicit moderator;
2. a local plant--pollinator benchmark, used to show the magnitude and
   heterogeneity of phenological temperature responses when partners occur in
   the same seasonal environment.

The two sources are **not pooled into a taxon contrast**.

## Frozen source identity

### Migratory birds

Usui, Butchart & Phillimore (2017), *Journal of Animal Ecology*  
DOI: 10.1111/1365-2656.12612  
Dryad DOI: 10.5061/dryad.mb4nd

Frozen CSV SHA-256:

```
68816f6cbfccbb9b47b45be0df49f077db914c8e43e567d0ed2cac9bbafde56c
```

The source contains 2,976 slope rows. The registered PAYOFF-B temperature
contrast retains 944 short/long-distance rows from 28 studies and 279 species:

- short-distance: 352 rows, 181 species;
- long-distance: 592 rows, 128 species.

### Local plant--pollinator benchmark

Freimuth et al. (2022), *Proceedings of the Royal Society B*  
DOI: 10.1098/rspb.2021.2142  
Dryad DOI: 10.5061/dryad.v41ns1rxv

Frozen `rnd_eff_temp.csv` SHA-256:

```
946f56b8aa5f43bb15f5bbbd8c5174be23c12691332651e09bce2cb20edf7efd
```

The source contains 1,763 species-level temperature slopes.

## Result 1 — migration distance survives a dependence-aware reconstruction

The distance-only inverse-variance fit gives:

| group | temperature slope (d / °C) | 95% CI |
|---|---:|---:|
| short-distance migrants | -1.025 | -1.312 to -0.739 |
| long-distance migrants | -0.630 | -0.869 to -0.390 |

Thus the raw long-minus-short contrast is **+0.395 d / °C**, with
95% CI **+0.110 to +0.681** and **p = 0.0090**.

The registered primary model uses inverse-variance weighting and two-way
cluster-robust uncertainty by **Study x Species**, while adjusting for arrival
metric, temperature location, arrival location, data source and continent.

The adjusted long-minus-short contrast is **+0.421 d / °C**, with 95% CI
**+0.135 to +0.708** and **p = 0.0040**.

Because negative slopes mean earlier migration in warmer years, the positive
long-minus-short coefficient means that **long-distance migrants advance less
strongly with warming than short-distance migrants**.

The sign and interval are stable to the declared sensitivity analyses:

- 99th-percentile cap on inverse-variance weights:
  **+0.417**, 95% CI **+0.118 to +0.715**, p = 0.0080;
- unweighted adjusted fit:
  **+0.538**, 95% CI **+0.190 to +0.887**, p = 0.0037.

A leave-one-study-out audit refits the adjusted model 28 times. Every
held-out-study coefficient is positive, every 95% CI retains a positive lower
bound, the coefficient range is **+0.378 to +0.608 d / °C**, the smallest CI
lower bound is **+0.066**, and the largest p-value is **0.0195**.

Inference uses Student-t critical values with 27 degrees of freedom, based on
the smaller marginal cluster count. PAYOFF-B clusters Study and Species but
does not refit the source paper's phylogenetic random effect. The underlying
migration-distance pattern is already reported by Usui et al. under their
phylogenetic meta-analysis.

This is a reconstruction of an effect already reported by Usui et al.; it is
not a PAYOFF-B novelty claim. Its value here is that the information-distance
gradient remains visible under the PAYOFF-B dependence-aware contract.

## Result 2 — the local plant--pollinator benchmark reproduces exactly

Species names in the Freimuth slope file were independently classified to the
five published groups. Live GBIF matching resolved all but three historical
strings. Three exact, source-scoped overrides were then applied and retained
in the audit table:

- `Ammophila arenaria` -> Plants;
- `Salix alba` -> Plants;
- `Tethea or` -> Butterflies/Moths.

After those declared overrides, **all five published group counts and rounded
means reproduce**:

| group | n | reconstructed mean (d / °C) | reconstructed SE |
|---|---:|---:|---:|
| Plants | 1,438 | -5.152 | 0.153 |
| Bees | 20 | -2.024 | 1.298 |
| Flies | 22 | -3.879 | 0.707 |
| Butterflies/Moths | 206 | -1.848 | 0.231 |
| Beetles | 77 | -1.706 | 0.518 |

The benchmark therefore establishes a second empirical fact relevant to the
theory: organisms sharing a local seasonal environment can all be responsive
to temperature while still differing substantially in response magnitude.
Local cue access is not equivalent to perfect ecological synchrony.

## Cross-system ecological interpretation

The licensed synthesis is:

```text
same local seasonal environment
    plant--pollinator partners show strong but unequal temperature responses

short-distance migration
    stronger temperature responsiveness

long-distance migration
    weaker temperature responsiveness
```

Together with the existing PAYOFF-B broad-bird result that stronger
pre-outcome source--destination predictive connectivity is associated with
smaller arrival--green-up mismatch, this creates a coherent empirical
**information-distance** axis.

The biological interpretation is not that one taxon is intrinsically better at
climate tracking. It is that the usefulness of environmental information can
depend on **where and when the decision is made relative to the future state
that matters**.

## Claim boundary

PAYOFF-B may now say:

> **Within migratory birds, phenological temperature responsiveness weakens
> with migration distance. Independently, local plant--pollinator partners show
> strong but unequal temperature responsiveness. Together with the
> predictive-connectivity analysis, these patterns are consistent with the
> hypothesis that spatial and temporal access to information constrains
> seasonal tracking.**

PAYOFF-B may **not** say:

- pollinators universally track climate better than birds;
- the bird--pollinator difference is a causal taxonomic effect;
- the Usui migration-distance pattern is newly discovered;
- these two source datasets alone are a new cross-taxon meta-analysis;
- this result demonstrates natural information hysteresis.

## Paper 2 role

This result should enter Paper 2 as **E6 — cross-system information-distance
triangulation**.

It strengthens the ecological side of the paper without changing the central
claim ceiling:

- predictive information before commitment matters in natural birds;
- decision-time information availability matters experimentally;
- post-error correction is a separate axis and is not universally strengthened
  by connectivity;
- migration distance carries an independent phenological-response gradient;
- local plant--pollinator systems provide a non-migratory benchmark;
- full natural degradation--recovery hysteresis remains unobserved.

The next escalation is a genuinely multi-study cross-system moderator
meta-analysis. That requires multiple independent plant--pollinator and
migration datasets on a harmonized effect-size contract and remains a separate
gate.
