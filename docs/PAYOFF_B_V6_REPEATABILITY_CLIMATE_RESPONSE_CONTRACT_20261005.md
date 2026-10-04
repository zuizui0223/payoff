# PAYOFF-B V6 prospective contract — 2026-10-05

Status: **PREOUTCOME; NO FRANKLIN–LIU MATCH OR RESULT OPENED**

## 1. Field question

V6 asks:

> **Does individual-level consistency in migration timing constrain the rate at
> which bird populations shift migration phenology under environmental change?**

This question follows directly from two existing field results.

Franklin et al. (2022) showed that migration timing is often individually
repeatable and explicitly noted that high repeatability may limit the
contribution of within-individual flexibility to population-level phenological
change.

Liu et al. (2026) compiled long-term migration-timing change rates for 549 bird
species and showed that the demographic association of timing advances differs
between pre-breeding and post-breeding migration.

The untested bridge is whether the **individual consistency of timing** predicts
the **long-term rate of population-level timing change**.

## 2. Prior-art boundary

V6 does not claim novelty for:

- individual repeatability of migration timing;
- long-term advances in bird migration timing;
- associations between timing shifts and population trends;
- stage dependence of demographic benefits;
- population-level phenological shifts arising through cohort replacement;
- the general idea that rigid schedules can be vulnerable under climate change.

The candidate contribution is only the direct cross-species test linking
published individual-level timing repeatability to published long-term
population-level phenological change.

A current novelty search found no study that directly tests this link across
species.

## 3. Data sources

### Franklin et al. 2022

Primary source:
- Journal of Animal Ecology 91:1416–1430.
- DOI 10.1111/1365-2656.13697.
- Dryad DOI 10.5061/dryad.n02v6wx09.
- Public GitHub repository:
  `kirstyfranklin/Avian_migration_meta-analysis`.

The released meta-analysis contains:
- 177 repeatability effect sizes;
- 54 papers;
- 47 species;
- event classes including non-breeding departure, breeding arrival,
  breeding departure and non-breeding arrival.

### Liu et al. 2026

Primary source:
- Nature Ecology & Evolution.
- DOI 10.1038/s41559-026-03198-9.
- Figshare DOI 10.6084/m9.figshare.31225291.

The published database contains:
- 4,351 population-level migration-timing estimates;
- 549 avian species;
- timing-change rates separated into pre-breeding and post-breeding migration;
- population-trend information;
- climate-change covariates and life-history traits.

No cross-dataset species match is inspected before this contract is frozen.

## 4. Matching rule

Species are matched by scientific name after taxonomic normalization.

Allowed taxonomic operations:
1. exact binomial match;
2. documented synonym update using a single declared taxonomic backbone;
3. subspecies collapsed to the species used by Liu only when Franklin's source
   record clearly belongs to that species.

No fuzzy name match is allowed without a documented taxonomic mapping.

The taxonomic mapping table must be frozen before any effect relationship is
tested.

## 5. Admission gate

The primary V6 analysis proceeds only if:

- at least **20 species** have usable Franklin repeatability estimates and Liu
  timing-change data in the corresponding seasonal class;
- at least **10 species** contribute pre-breeding data;
- at least **10 species** contribute post-breeding data.

If fewer than 20 species overlap overall:

```text
V6_PRIMARY_ANALYSIS = NOT_ESTIMABLE
```

and no threshold is lowered.

## 6. Primary predictor

Franklin repeatability estimates are not averaged blindly across annual-cycle
events.

Events are mapped prospectively:

### Pre-breeding repeatability
Eligible Franklin event classes:
- departure from non-breeding grounds;
- arrival at breeding grounds.

### Post-breeding repeatability
Eligible Franklin event classes:
- departure from breeding grounds;
- arrival at non-breeding grounds.

When a species has multiple eligible effects within the same seasonal class,
the species-stage repeatability is estimated by a random-effects meta-analytic
mean using the reported sampling uncertainty.

Sex-specific effects:
- combined-sex effects are preferred;
- sex-specific effects are retained only when no combined estimate exists and
  are modeled with sex as an effect-level factor before deriving the
  species-stage estimate.

No repeatability value is selected because it gives a stronger V6 result.

## 7. Primary outcome

The primary outcome is the Liu species-level long-term migration timing change
rate for the corresponding seasonal class.

Sign convention is standardized so that:

[
	ext{negative change rate}
=
	ext{advancement through time}.
]

For interpretability, define advancement rate

[
A=-r_{m timing},
]

so larger (A) means faster advancement.

Population-level records are combined within species and seasonal class using
the Liu study's declared uncertainty / weighting structure where available.
If a species-level estimate is already supplied by Liu, that released estimate
is used without re-fitting the historical time series.

## 8. Primary hypothesis

### H1 — individual-rigidity constraint

If high individual repeatability represents a constraint on within-individual
timing adjustment, species with higher repeatability should show slower
population-level timing advancement:

[
rac{partial A}{partial R}<0,
]

where (R) is migration-timing repeatability.

Equivalent wording:

> species with more individually stereotyped migration timing advance their
> population timing less rapidly.

This is the declared directional hypothesis.

## 9. Competing biological alternative

### H0/B — composition-mediated change

High repeatability need not prevent population-level phenological change.

Populations can shift through:
- differential survival of individuals with different timings;
- recruitment of cohorts with different timing;
- changing frequencies of stable individual phenotypes.

Under this route, species-level repeatability may be unrelated to long-term
timing shift.

A null or weak H1 result is therefore biologically interpretable and is not a
failed measurement.

## 10. Stage interaction

The primary model includes seasonal class and the interaction:

[
A
=
alpha
+
eta_R R
+
eta_S S
+
eta_{RS}R	imes S
+
arepsilon,
]

where (S) distinguishes pre-breeding from post-breeding migration.

This tests whether rigidity constrains timing change differently across the two
annual-cycle migration stages.

The interaction is primary because Liu et al. show stage-dependent demographic
consequences and Franklin et al. show event-specific repeatability.

## 11. Secondary demographic test

Only after H1 is evaluated, a secondary analysis asks whether repeatability
modifies the population benefit associated with timing advancement.

Conceptually:

[
	ext{population trend}
sim
A
+
R
+
A	imes R
+
	ext{season}
+
	ext{covariates}.
]

This is secondary because the expected matched species count is much smaller
than the Liu database and may not support a stable interaction.

No demographic model is run unless at least:
- 20 matched species overall; and
- 8 species per seasonal class with population-trend data.

Failure of this gate leaves the demographic extension unrun.

## 12. Covariates

Primary covariates are restricted to variables already motivated in the source
papers and available independently of the focal repeatability/timing outcomes:

- log body mass;
- migration distance, if available on a comparable species scale;
- ecological group (landbird/waterbird/seabird);
- absolute breeding latitude;
- tracking method / repeatability estimation method as Franklin-source
  measurement covariates.

No new ecological moderator is added after seeing the focal result.

## 13. Phylogeny

The primary comparative analysis accounts for phylogenetic non-independence if
the matched sample is >=20 species and a compatible tree can be constructed.

Baseline:
- phylogenetic generalized least squares or a phylogenetic random effect.

Sensitivity:
- non-phylogenetic weighted model.

A disagreement between phylogenetic and non-phylogenetic estimates is reported,
not resolved by selecting the preferred sign.

## 14. Weighting and uncertainty

Franklin repeatability estimates carry sampling uncertainty.

Liu timing-change estimates also carry uncertainty where available.

Preferred analysis propagates both sources of uncertainty through a
measurement-error / hierarchical model.

A simple species-point-estimate regression is sensitivity only.

## 15. Mandatory sensitivities

1. pre-breeding only;
2. post-breeding only;
3. combined-sex Franklin effects only;
4. exclude repeatability values based on conventional ringing;
5. exclude species with only one repeatability effect;
6. landbirds only;
7. leave-one-species-out;
8. leave-one-source-paper-out;
9. exact taxonomic matches only;
10. remove the highest-precision repeatability quartile to check dominance.

## 16. Claim ceiling

A supported H1 licenses:

> Across the matched species, higher individual repeatability of migration
> timing is associated with slower long-term population-level timing
> advancement.

It does not license:
- repeatability as a direct physiological rigidity parameter;
- proof that low repeatability causes climate adaptation;
- proof that high repeatability causes population decline;
- claims about species absent from the matched sample.

A null H1 licenses:

> Individual timing consistency does not, by itself, explain why species differ
> in long-term migration-timing shifts; population change can occur despite
> highly repeatable individual schedules.

Both outcomes answer a field question raised explicitly by Franklin et al.

## 17. Novelty gate

V6 remains open only if all are true:

1. >=20 matched species pass the admission gate;
2. a current literature search identifies no previous cross-species test
   directly linking individual migration-timing repeatability to long-term
   timing-change rate;
3. the Liu dataset provides species identities and stage-specific timing-change
   information at sufficient resolution;
4. the Franklin effects can be mapped to pre/post-breeding classes without
   outcome-dependent recoding.

If any fail:

```text
V6_PUBLICATION_ROUTE = CLOSE
```

## 18. Outcome access rule

Before the taxonomic match and admission count are frozen:

- do not calculate a repeatability–shift correlation;
- do not inspect the sign of the matched association;
- do not fit population-trend models.

The first allowed opened quantity is the **match count and composition only**.

```text
V6_FRANKLIN_DATA = PUBLIC_CONFIRMED
V6_LIU_DATA = PUBLIC_CONFIRMED
V6_SPECIES_MATCH = UNOPENED
V6_H1 = UNOPENED
V6_DEMOGRAPHIC_EXTENSION = UNOPENED
```
