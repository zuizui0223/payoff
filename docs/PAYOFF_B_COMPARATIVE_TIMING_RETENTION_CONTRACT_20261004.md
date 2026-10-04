# PAYOFF-B comparative timing-retention contract — 2026-10-04

Status: **PROSPECTIVE; NO WANG-2024 INDIVIDUAL-LEVEL RESULT OPENED**

## 1. Field question

The comparative question is:

> **Why do some migratory bird species carry departure-timing differences
> through to arrival, whereas others compress those differences en route?**

This is narrower than generic "phenological flexibility" and narrower than
PAYOFF-B V4's rejected general fitness-rescue question.

## 2. Prior-art boundary

Schmaljohann (2019, Movement Ecology 7:25) already established that:
- within species, later migration start generally predicts later arrival;
- in spring, the pooled within-species effect was about 0.4 arrival days per
  1-day shift in migration start;
- species-specific slopes varied substantially;
- almost all reported species-specific slopes were positive and below 1.

Therefore PAYOFF-B must not claim novelty for:
- departure-to-arrival carry-over;
- less-than-one average retention;
- existence of species-specific variation in retention.

Wang et al. (2024, Nature Communications 15:4111) compiled 1708 full annual
tracking records from 186 species, including 1531 individual records and 177
population-level records. The paper modeled departure date as a predictor of
arrival date in a global SEM and reported strong carry-over, but did not make
species-specific departure-to-arrival retention or its ecological predictors
the focal estimand.

## 3. Primary estimand

For spring migration, define for individual/record i in species j:

[
A_{ij}
=
alpha_j
+
eta_j(D_{ij}-ar D_j)
+
gamma(M_{ij}-ar M_j)
+
eta_{source}
+
eta_{year}
+
epsilon_{ij},
]

where:
- (D) is departure date from the last non-breeding site;
- (A) is arrival date at the breeding site;
- (M) is spring migration distance;
- (eta_j) is the **species-specific timing-retention coefficient**.

Interpretation:
- (eta_j=1): a 1-day departure difference is retained as a 1-day arrival difference;
- (0<eta_j<1): departure differences are compressed en route;
- (eta_j=0): complete erasure of departure-order differences;
- (eta_j<0): rank reversal / over-correction;
- (eta_j>1): amplification.

This is a descriptive within-species estimand, not a direct behavioral-control
parameter.

Autumn is a declared secondary replication with breeding departure and
non-breeding arrival.

## 4. Data-admission rules

Primary analysis uses only records explicitly reported at the **individual**
level.

Population-level averages are excluded from the primary within-species
retention analysis because they cannot identify between-individual timing
transmission.

A species enters the primary species-specific retention display only when:
- at least 5 individual spring records have both departure and arrival dates;
- at least 2 unique departure dates are represented;
- the departure-date SD is at least 2 days.

The hierarchical model may retain species with >=3 valid individual records for
partial pooling, but no species-level biological interpretation is allowed for
species below the display threshold.

If fewer than 20 species pass the display threshold, the comparative predictor
analysis is **NOT ESTIMABLE** and no threshold is relaxed after outcome access.

## 5. Primary comparative hypotheses

The goal is to explain among-species variation in (eta_j), not merely to
show that it exists.

### H1 — migration-distance / opportunity hypothesis

Longer spring migrations provide more route stages at which speed, stopover or
route duration can change. If opportunity for en-route adjustment dominates,
longer migration distance predicts **lower retention**:

[
rac{partial eta}{partial log distance}<0.
]

### H2 — schedule-constraint alternative

Long-distance migrants may rely more strongly on endogenous schedules and
remote cues, limiting facultative correction. If schedule constraint dominates,
longer migration distance predicts **higher retention**:

[
rac{partial eta}{partial log distance}>0.
]

H1 and H2 are competing predictions. The sign is not to be chosen after seeing
the data.

### Secondary predictors

Declared secondary moderators:
- log lean body mass;
- breeding latitude;
- non-breeding latitude;
- spring migration duration;
- flight mode if available in the released Wang data.

These are secondary because prior work already tested body mass and migration
distance against timing/speed, but not specifically as moderators of the
species-specific departure-to-arrival retention coefficient.

## 6. Comparative model

Preferred implementation is a one-stage hierarchical model in which the
within-species departure slope varies by species and that random slope is
modeled as a function of species traits.

Conceptually:

[
eta_j
=
eta_0
+
b_1log distance_j
+
b_2log mass_j
+
b_3 latitude_j
+
u_{phylogeny,j}
+
u_j.
]

Source paper / population is included where recoverable to avoid treating
heterogeneous study protocols as independent biological variation.

A two-stage analysis of extracted species slopes is sensitivity only; the
one-stage partial-pooling model is primary.

## 7. Mandatory sensitivities

1. Remove population-average rows entirely — primary already does this.
2. Species threshold n>=8 instead of n>=5.
3. Exclude records digitized from figures if source flag permits.
4. Add sex where reported.
5. Study/source random effect.
6. Repeat Passeriformes-only analysis to compare with Schmaljohann's songbird
   scope.
7. Run autumn as a directional replication, not as a pooled second outcome.
8. Refit after excluding species represented by only one source study if this
   leaves >=20 species.

## 8. Claim ceiling

A supported association may license:

> Species differ in how strongly departure timing is transmitted to arrival,
> and part of that variation is associated with [declared trait].

It does **not** license:
- direct estimates of behavioral correction gain;
- claims that a low slope proves active compensation;
- fitness rescue;
- climate-change adaptation;
- causal effects of migration distance or body mass.

A low (eta) can arise from active correction, environmental forcing,
selection/attrition, measurement error, or route heterogeneity.

## 9. Novelty gate

The comparative route remains open only if all are true:

1. >=20 species pass the predeclared primary display threshold;
2. the released data preserve individual-level departure and arrival pairings;
3. no prior study identified in the novelty search has already tested
   ecological predictors of species-specific departure-to-arrival retention at
   a comparable multi-order scale;
4. at least one primary/secondary moderator can be defined independently of the
   same departure/arrival dates used to estimate retention.

If any fail:

```text
COMPARATIVE_RETENTION_ROUTE = CLOSE
```

## 10. Current access state

The Wang et al. article confirms that the released dataset contains:
- species/subspecies;
- individual identification;
- breeding/non-breeding coordinates;
- non-breeding departure date;
- breeding arrival date;
- breeding departure date;
- non-breeding arrival date;
- capture site;
- tracking year;
- sex when reported.

The article and repository state that all migration-timing data and code are
available at Figshare DOI 10.6084/m9.figshare.24613599.

The current tool session has not yet materialized the Figshare XLSX/CSV bytes,
so no individual-level retention result has been opened.

```text
WANG_DATA_SCHEMA = SOURCE_CONFIRMED
WANG_RAW_BYTES = ACCESS_PENDING
OUTCOME_OPENED = NO
```
