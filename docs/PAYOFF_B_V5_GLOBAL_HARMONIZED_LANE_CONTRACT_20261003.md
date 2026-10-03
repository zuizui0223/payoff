# PAYOFF-B V5 global harmonized lane contract — 2026-10-03

Status: **PREOUTCOME; no V5 propagation coefficient opened**

## 1. Rationale

The literature-effect synthesis remains valuable, but source studies differ in
tracking technology, event definition, model specification and reporting.

Wang et al. (2024) provide a complementary harmonized dataset compiled from 306
tracking studies, containing four major annual-cycle timing events for 1531
individual records plus 177 population-level records across 186 species.

V5 therefore has two prespecified lanes:

- **Lane G — global harmonized reanalysis:** one common raw-data schema, individual
  records only;
- **Lane L — literature transition synthesis:** independent eligible published
  systems using the frozen `beta_AB` effect definition.

Lane G is the primary comparative lane. Lane L is an external replication /
generality lane. Neither lane may be changed after its focal outcomes are
opened.

## 2. Source

Wang X et al. 2024. *Nature Communications* 15:4111.
DOI: 10.1038/s41467-024-48248-7.

Public repository:
- Figshare DOI: 10.6084/m9.figshare.24613599.v1
- timing file: `migration_data_final.csv`
- README: `README_final.txt`

The source publication reports:
- 1531 individual tracking records;
- 177 population-level records;
- 186 species;
- four timing events:
  1. departure from non-breeding site;
  2. arrival at breeding site;
  3. departure from breeding site;
  4. arrival at non-breeding site.

## 3. Record inclusion

Lane G includes **individual-level records only**.

Population means/proxies are excluded from all primary V5 inference.

The exact field that distinguishes individual from population records will be
resolved from the public file schema before any timing coefficient is
calculated and recorded in an extraction receipt.

Records must have:
- a resolvable individual identifier;
- a source paper/study identifier;
- species identity;
- tracking year when available;
- the event dates required for the focal transition.

No missing timing value is imputed.

## 4. Four annual-cycle transitions

The four declared transitions are:

1. **SPRING_ACTIVE**
   - A: departure from non-breeding site
   - B: arrival at breeding site

2. **BREEDING_STATIONARY**
   - A: arrival at breeding site
   - B: departure from breeding site

3. **AUTUMN_ACTIVE**
   - A: departure from breeding site
   - B: arrival at non-breeding site

4. **NONBREEDING_STATIONARY**
   - A: arrival at non-breeding site
   - B: subsequent departure from non-breeding site represented in the same
     full-annual-cycle record.

The source paper itself defines these four corresponding periods as spring
migration, breeding, autumn migration and non-breeding.

## 5. Timing deviations

The target estimand is within-source relative timing, not differences among
species or regions in mean calendar date.

For each event, dates are centered within the most specific source cohort that
can be constructed without using outcome values:

`paper/study × species × capture site/population × tracking year`

If a required grouping field is absent, the next coarser prespecified level is:

`paper/study × species × tracking year`, then
`paper/study × species`.

Groups with fewer than three individual records are excluded from the baseline
Lane G fit because they do not provide a minimally stable within-source timing
contrast. Sensitivities require at least 5 and at least 10 records per group.

Centering uses the within-group mean. Translation does not alter the raw slope;
the purpose is to remove between-source/year calendar offsets and keep the
estimand tied to relative schedule position.

## 6. Primary Lane G model

The four transitions are stacked in long form.

For transition (j),

[
d_{B}=a_j+eta_j d_A+epsilon.
]

A hierarchical model estimates transition-specific slopes while accounting for
shared study/species/cohort sources.

Required grouping terms:
- paper/study;
- species;
- source cohort;
- individual when repeated individual-year records are present.

The declared contrast is

[
C_G =
rac{eta_{m BREEDING}+eta_{m NONBREEDING}}{2}
-
rac{eta_{m SPRING}+eta_{m AUTUMN}}{2}.
]

H1 predicts

[
C_G < 0.
]

The ecological wording remains descriptive:

> within the harmonized tracking corpus, relative timing is propagated less
> strongly across stationary than active-migration transitions.

No observational coefficient is called a causal fraction of delay absorbed.

## 7. Paired-source sensitivity

A high-value sensitivity restricts inference to source cohorts that contribute
at least one ACTIVE and one STATIONARY transition from the same individual
panel.

This within-source comparison reduces confounding by:
- species;
- tracking method;
- source-study design;
- calendar period;
- many persistent individual-schedule differences.

It is prespecified and cannot replace the baseline only because its result is
more favorable.

## 8. H2 in Lane G

Available-time H2 is **not** tested with each individual's own (B-A) interval
as a predictor of that individual's propagation.

For each stationary source cohort, the moderator is an effect-level mean period
duration.

Priority:
1. source-level reported mean duration if present in the harmonized data/source;
2. cohort mean duration derived from A/B dates.

Derived duration is labeled `SAME_SAMPLE_DERIVED` and analyzed as sensitivity,
not as independent primary evidence for H2.

The H2 claim is not promoted if only same-sample-derived duration is available.

## 9. Measurement and digitization sensitivity

Wang et al. report that some source dates were digitized from published figures.
If a source-level digitization flag can be reconstructed before inspecting V5
slopes, V5 will run a sensitivity excluding those records.

If no reliable digitization flag is present in the public source metadata, the
limitation is reported rather than inferred post hoc.

The baseline does not apply post-outcome data-quality exclusions.

## 10. Relation to Wang et al. published analysis

Wang et al. already showed, using Bayesian phylogenetic SEM, that timing at
earlier phases can predict later migration timing, especially
departure-to-arrival carry-over during spring and autumn migration.

V5 does **not** claim discovery of global carry-over effects.

The new question is narrower:

> when all four annual-cycle transitions are put on the same unstandardized
> day/day scale, are stationary transitions systematically weaker propagation
> links than active migration transitions?

This is a reanalysis question, not a claim that the source dataset was created
for V5.

## 11. Cross-lane adjudication

The strongest V5 conclusion requires convergence:

- Lane G supports the declared stationary-vs-active contrast; and
- Lane L independently supports the same directional contrast using eligible
  Tier A/B literature effects.

Decision states:

```text
G_PASS + L_PASS        -> CONVERGENT_COMPARATIVE_SUPPORT
G_PASS + L_FAIL/NULL   -> GLOBAL_DATASET_SUPPORT_ONLY
G_FAIL/NULL + L_PASS   -> LITERATURE_SYNTHESIS_SUPPORT_ONLY
G_FAIL/NULL + L_FAIL   -> NO_SUPPORT
L_INSUFFICIENT         -> GLOBAL_RESULT_WITH_EXTERNAL_VALIDATION_UNRESOLVED
G_INSUFFICIENT         -> LITERATURE_RESULT_ONLY_IF_LANE_L_GATE_PASSES
```

No lane is dropped because it disagrees with the other.

## 12. Outcome lock

Before the first Lane G (eta) is calculated:
- exact source columns and record-type rule must be written to a schema receipt;
- the count-only eligibility summary may be computed;
- timing coefficients, class contrasts and effect-size plots remain unopened.

The next permissible step is therefore **schema and count audit only**.
