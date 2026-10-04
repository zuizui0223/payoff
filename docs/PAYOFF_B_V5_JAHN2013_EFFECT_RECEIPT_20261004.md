# PAYOFF-B V5 Jahn 2013 effect receipt — 2026-10-04

Status: **ADMISSIBLE EFFECT EXTRACTION; H1/H2 NOT RUN**

## Source

Jahn AE et al. 2013. *The Auk* 130:247–257.  
DOI: 10.1525/auk.2013.13010.

The published Table 1 reports individual fall departure / winter-arrival dates
and spring winter-departure / breeding-arrival dates for Eastern Kingbirds,
Western Kingbirds and Scissor-tailed Flycatchers.

## Frozen estimand

For each species/cohort with adequate complete pairs:

\[
A_i = a + \beta_{AB}D_i + \varepsilon_i,
\]

with both dates converted to day of year on the same calendar scale.

No correlation coefficient was converted to a slope. The slope was fit directly
from the published individual dates.

## Validation against the source publication

For Western Kingbirds, six individuals have complete spring
departure/arrival pairs:

```text
C  24-Apr -> 05-May
D  24-Apr -> 05-May
E  14-Apr -> 26-Apr
F  23-Apr -> 09-May
G  20-Apr -> 28-Apr
N  10-Apr -> 18-Apr
```

Their Pearson correlation is 0.9384, reproducing the paper's reported
spring departure–arrival correlation of approximately r=0.94.

This provides a source-faithfulness check before using the raw slope.

## Opened effects

### Western Kingbird — spring active migration

```text
n = 6
beta_AB = 1.22565 d/d
SE = 0.22564
95% CI = [0.59916, 1.85214]
```

Interpretation under the V5 coordinate:
the point estimate does not indicate compression; one day of later departure
was associated with about 1.23 d of later breeding-ground arrival in this small
cohort. The interval is wide and includes one-for-one propagation.

### Western Kingbird — autumn active migration

Eleven individuals have complete breeding-departure / first-winter-arrival
pairs.

```text
n = 11
beta_AB = 0.82013 d/d
SE = 0.19645
95% CI = [0.37574, 1.26452]
```

### Scissor-tailed Flycatcher — autumn active migration

All five published birds have complete autumn departure/arrival pairs.

```text
n = 5
beta_AB = 1.23775 d/d
SE = 0.45487
95% CI = [-0.20983, 2.68534]
```

The uncertainty is retained without thresholding by significance.

## Fail-closed exclusions

### Scissor-tailed Flycatcher spring

Only two individuals have both spring departure and breeding-arrival dates.
No primary slope is admitted.

```text
STFL_SPRING = INSUFFICIENT_COMPLETE_PAIRS
```

### Eastern Kingbird

Table 1 contains:
- Nebraska and Oklahoma breeding origins;
- one Nebraska individual tracked in two years.

The paper's reported spring correlation uses a source-specific handling of
these records that is not fully specified by the table alone. Mixing the
Oklahoma bird with Nebraska birds or choosing/averaging one repeated year
post hoc would create an avoidable analysis choice.

Therefore no Eastern Kingbird beta_AB is opened from this table in V5
without a predeclared repeated-individual/population rule.

```text
EAKI = HOLD_RECORD_STRUCTURE_AMBIGUITY
```

## Corpus consequence

The cumulative V5 effect file is now:

`data/payoff_b_buffer_limits_effects_v0_2_20261004.csv`

Current numerical corpus:

```text
PRIMARY_EFFECTS_OPENED = 9
UNIQUE_STUDY_IDS_WITH_EFFECTS = 4
BIOLOGICAL_DATASET_COHORTS = 5
ACTIVE_MIGRATION_EFFECTS = 6
STATIONARY_EFFECTS = 3
H1_MODEL_RUN = NO
H2_MODEL_RUN = NO
```

The two Tyrannus species are treated as separate biological species/cohorts
within the same study, while study-level dependence must be retained in any
future meta-regression.

The frozen H1/H2 stability thresholds remain unchanged.
