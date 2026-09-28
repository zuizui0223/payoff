# PAYOFF-B cross-system empirical lane: local pollinators versus migratory birds

Date: **2026-09-28**  
Status: **promotion gate passed; frozen as Paper 2 E6 empirical triangulation**  
Role: canonical E6 empirical-generalization lane for Paper 2; the causal claim ceiling remains unchanged.

## Why this lane exists

The current Paper 2 theory is explicitly cross-system: residents and local interactors can often sample local seasonal state, while a long-distance migrant may have to commit before the destination state is observable. The natural-data stack, however, is still bird-heavy. The canonical empirical evidence is broad migratory birds, a pied-flycatcher--resident-tit manipulation, Eurasian wigeon, and negative Hoge Veluwe reversal gates.

That leaves a real ecological-generalization gap: the canonical three-node theory contains a flower, a local pollinator and a migrant, but the natural evidence has not yet compared a local pollination system with migratory phenology.

## Two open-data anchors

### Local plant--pollinator system

Freimuth et al. (2022; DOI 10.1098/rspb.2021.2142; Dryad 10.5061/dryad.v41ns1rxv) provide species-level slopes from the time- and temperature-shift mixed models for Germany, 1980--2020. Source code resolves an important semantic point: the fitted model is `doy ~ temp + lat + long + elev + (temp | species)`, and `run_models.R` adds the overall fixed temperature coefficient to each species random-slope deviation before writing `rnd_eff_temp.csv`. The archived `slope` is therefore the source-used **total species temperature slope**, not a deviation that still needs a group coefficient added.

Published scope:

- 1,764 species total;
- 1,438 plants;
- 20 bee species;
- 22 fly species;
- 206 butterfly/moth species;
- 77 beetle species.

Published group-level temperature sensitivities include:

- plants: **-5.2 +/- 0.2 d / deg C**;
- flies: **-3.9 +/- 0.7 d / deg C**;
- bees: **-2.0 +/- 1.3 d / deg C**;
- butterflies/moths: **-1.9 +/- 0.2 d / deg C**.

For predicted plant--pollinator pairs, the published bee--plant asynchrony trend is especially large:

- **-11.35 +/- 0.39 d / decade**;
- temperature sensitivity of asynchrony: **-5.72 +/- 0.24 d / deg C**.

The sign here does not mean universal deterioration. Plants historically tended to lag the insects, and faster plant advance caused many bee--plant and butterfly--plant pairs to become *more* synchronous over the observed period. That is useful for PAYOFF-B because it shows that local partners can move strongly with the same changing seasonal environment, while the direction of realized mismatch depends on the starting configuration.

### Migratory-bird meta-analysis

Usui et al. (2017; DOI 10.1111/1365-2656.12612; Dryad 10.5061/dryad.mb4nd) provide population-level slope estimates and errors for **413 bird species across five continents**.

Published aggregate results:

- spring migration advanced **2.1 d / decade** on average;
- migration timing advanced **1.2 d / deg C** with warming;
- short-distance migrants advanced more strongly than long-distance migrants both through time and with temperature.

The authors explicitly discuss the information interpretation: conditions encountered by short-distance migrants can be more predictive of breeding-ground conditions than those available to long-distance migrants.


## Source-semantics correction

Dryad describes `rnd_eff_temp.csv` as random effects from the temperature-shift model, but the source export script transforms those values before saving: `rnd_eff$slope <- rnd_eff$slope + mod_coef[2,1]`, and propagates uncertainty as `sqrt(random_SE^2 + fixed_SE^2)`. The archived `slope` can therefore be used directly as the source-defined species total days-per-degree-C response. Taxonomic group membership is needed to reproduce Table 1 group summaries, not to reconstruct an additional fixed effect.

For Usui et al., the published analysis used slope estimates plus sampling error in a Bayesian phylogenetic meta-analysis with phylogeny, species, study, location and species-by-location structure. Any PAYOFF-B rerun that omits the 100-tree phylogenetic layer is explicitly a source-table robustness reconstruction rather than an exact reproduction of the original model.

## What PAYOFF-B can test without cheating

The primary inferential contrast must stay **within the bird meta-analysis**:

> Is the temperature-response slope more negative for short-distance than for long-distance migrants after reproducing the source effect-size contract and dependence structure?

This is not a novelty claim; the source paper already reports the pattern. Its role is to put the PAYOFF-B information-distance axis on a quantitatively reconstructed benchmark.

The pollinator dataset is an independent **local-information benchmark**:

> How heterogeneous are source-model species total temperature responses within each plant/pollinator group, and what do those responses imply for changing interaction synchrony?

The archived slopes are already the source-exported species total slopes. Published group-level means are used as reproduction anchors, while the taxonomic mapping is frozen separately so the five source groups can be reconstructed transparently.

The cross-system comparison is then triangulation:

```text
local plant / pollinator
    strong local climate sensitivity can alter synchrony in either direction

short-distance migrant
    intermediate spatial information problem

long-distance migrant
    weakest access to destination conditions at early commitment
```

That is biologically informative, but it is not licensed as one causal coefficient because taxon, geography, phenophase and source study differ.

## Analysis contract

1. Acquire and checksum the two CC0 Dryad sources.
2. Reconstruct units, sample identifiers, effect-size variance and source export semantics, including verification that Freimuth's archived slope equals fixed temperature effect plus species random deviation.
3. Cross-check the published source-level anchor values and data dimensions before any PAYOFF-B comparison.
4. Refit the Usui short- versus long-distance temperature contrast with repeated species/study/location dependence retained. If the original 100-tree phylogenetic layer is not reproduced, label the result as a dependence-aware robustness reconstruction rather than an exact reproduction.
5. Reproduce Freimuth group-level temperature-response summaries from the archived total species slopes using a frozen, auditable taxonomic-group mapping.
6. Do **not** pool pollinators and birds into one moderator model unless multiple independent source datasets per information-distance class are added.
7. If the bird gradient reproduces and the pollinator benchmark is stable, add it to Paper 2 as an empirical **information-distance triangulation**, not as evidence that pollinators universally outperform migrants.

## What would count as a stronger new meta-analysis

A genuinely new Paper 2 meta-analysis needs multiple independent systems on both sides of the contrast. The clean target is a study-level effect-size table with:

- phenological response in d / deg C or d / decade;
- uncertainty;
- interaction type;
- decision location relative to matched ecological state;
- migration distance / residency;
- local versus remote cue exposure;
- taxon and phenophase;
- study and population identifiers.

Kharouba et al. (2018) provide a useful 54-interaction global synchrony database, and recent plant--pollinator syntheses expand the pollinator side, but these require a separate harmonization pass before they can support an actual moderator meta-analysis.

## Decision for Paper 2

This lane passed its promotion gate and fixes the clearest prior imbalance: **the theory is multi-taxon but the natural evidence was mostly birds**.

The manuscript role is one compact ecological result plus supplementary provenance:

> Local plant--pollinator systems show strong climate-linked shifts in phenology and synchrony, while within migratory birds phenological responsiveness weakens with migration distance. Together with PAYOFF-B's predictive-connectivity result, this is consistent with an information-distance interpretation, without implying a universal taxonomic ranking.

That wording remains below the causal claim ceiling.
