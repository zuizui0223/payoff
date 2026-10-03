# PAYOFF-B Wang distance-dependent timing compensation — preanalysis contract

Date: **2026-10-03**  
Status: **PREOUTCOME FINAL; numerical Wang migration-timing values not yet inspected in PAYOFF-B**

## Why this route exists

The broad V4 fitness-rescue question was closed by prior art. Annual-cycle
studies already show that timing deviations can dissipate, persist, or carry
survival and reproductive costs.

A first macro-comparative idea was to estimate how much departure-date
variation survives to arrival across species. That idea was also narrowed by a
prior-art audit before Wang timing outcomes were inspected.

Schmaljohann (2019) already estimated species-specific start-to-arrival slopes
for 17 spring and 21 autumn songbird species, demonstrated substantial
between-species variation, and showed that most species-specific effects were
positive but below one.

The remaining ecological question is therefore:

> **Does migration distance determine how much of a departure-time deviation
> survives to arrival?**

This is a field-motivated question. Ralston et al. (2025) explicitly proposed
that individual migration distance may affect the ability to compensate delayed
spring departure en route. Comparative stopover studies also show that
long-distance migrants face stronger time constraints and make different
departure decisions.

Two mechanisms make opposite predictions:

- **recourse-opportunity:** a longer route supplies more stages at which a late
  migrant can increase migration speed, shorten stopovers or otherwise catch
  up;
- **time-constraint:** a longer route imposes a tighter schedule, so a late
  start may be harder to absorb.

## Prior-art boundary

PAYOFF-B must not claim novelty for:

- departure date affecting arrival date;
- carry-over of migration timing;
- species-specific departure-to-arrival slopes;
- among-species heterogeneity in those slopes;
- longer-distance migrants moving faster on average.

Relevant boundaries:

- **Schmaljohann 2019:** species-specific start-to-arrival slopes in 17 spring
  and 21 autumn migrant species; substantial slope heterogeneity already shown.
- **Wang et al. 2024:** pooled global carry-over from departure to arrival in
  1,708 full annual-cycle tracking records from 186 species.
- **Franklin et al. 2022:** comparative within-stage timing repeatability across
  47 species; related but a different estimand.
- **Ralston et al. 2025:** migration distance explicitly proposed as a possible
  determinant of compensation after delayed spring departure.

Candidate novelty, if any, is restricted to explaining variation in
departure-to-arrival timing retention with migration distance.

## Retention coordinate

For individual \(i\) of species \(s\), study/paper \(j\), and tracking year
\(y\), define within-stratum anomalies

\[
d'_i = d_i - \bar d_{s,j,y},
\qquad
a'_i = a_i - \bar a_{s,j,y}.
\]

For descriptive visualization, a species-specific retention slope is

\[
a'_i = \beta_s d'_i + \epsilon_i.
\]

Interpretation:

- \(\beta_s=1\): departure deviations persist fully to arrival;
- \(0<\beta_s<1\): partial temporal compression;
- \(\beta_s=0\): complete reset by arrival;
- \(\beta_s<0\): over-correction / reversal.

The existence and heterogeneity of \(\beta_s\) are prior art. These slopes are
not estimates of cognitive information use, physiological control gain,
actionability or fitness.

## Data gate

Use only individual-level Wang records. Population-level means are excluded.

The spring route opens only if:

1. at least **20 species** have at least **8 informative paired individual
   records** after the declared centering;
2. each retained species has nonzero within-stratum departure variation;
3. at least 20 eligible species have nonmissing spring migration distance;
4. there is sufficient between-species migration-distance variation to estimate
   the focal interaction.

A centering stratum is species × study/paper × tracking year and must contain at
least two individual records.

If any gate fails, this macro-comparative lane closes without relaxing the
threshold after outcome inspection.

## Final primary model

The final preoutcome analysis is a one-stage multilevel test using eligible
individual-level spring records.

Response:

\[
a'_i.
\]

Focal timing predictor:

\[
d'_i.
\]

Migration distance is decomposed into:

- a **between-species component**: standardized species-mean log spring
  migration distance;
- a **within-species component**: standardized individual log spring migration
  distance minus the species mean, when sufficiently variable.

The **primary coefficient** is the cross-level interaction

\[
d'_i \times \overline{\log D}_s.
\]

This directly asks whether the same departure-time deviation is retained
differently in shorter- and longer-distance migrant species.

Model structure:

- fixed departure anomaly;
- fixed between-species log migration distance;
- departure anomaly × between-species log migration distance **[PRIMARY]**;
- within-species distance and its interaction with departure anomaly when
  identifiable **[SECONDARY]**;
- species random intercept;
- species random slope for departure anomaly;
- study/paper random intercept where identifiable.

## Competing predictions

No directional sign is selected in advance.

**Recourse-opportunity prediction**

\[
\text{distance} \uparrow
\Rightarrow
\text{retention} \downarrow.
\]

Longer routes may give migrants more opportunities to change stopover duration,
migration speed or route and therefore erase departure-time deviations.

**Time-constraint prediction**

\[
\text{distance} \uparrow
\Rightarrow
\text{retention} \uparrow.
\]

Longer routes may impose stronger time constraints and make a departure delay
harder to absorb.

The primary test is therefore two-sided.

## Secondary analyses

Secondary results cannot rescue a null primary distance interaction.

Allowed secondary analyses are:

- within-species migration-distance × departure-anomaly interaction;
- spring–autumn contrast in retention among species eligible in both seasons;
- log body mass as an additional moderator;
- species-specific shrunken \(\beta_s\) values for descriptive visualization.

No post-result taxonomic subgroup search is allowed.

## Novelty decision rule

The comparative route is supported only if:

- all data gates pass; and
- the declared uncertainty interval for the primary
  departure-anomaly × between-species migration-distance interaction excludes
  zero.

If the primary interaction is unresolved, close the comparative PAYOFF-B route.

A larger dataset, significant pooled carry-over, or significant heterogeneity
in species-specific slopes is **not sufficient novelty**, because those results
are already established.

## Outcome firewall

Before this contract was finalized, PAYOFF-B inspected only published summaries,
source metadata and the literature boundary.

No numerical Wang departure or arrival timing outcomes were inspected.

Schema probing is limited to file metadata, table/sheet names, column names and
row counts. Numerical timing values may be opened only after the data gate and
analysis script are fixed.

## Revision provenance

The first version of this contract treated species-specific retention
heterogeneity as candidate novelty.

It was narrowed before outcome inspection after discovering Schmaljohann
(2019), which had already estimated species-specific start-to-arrival slopes.

It was then reformulated as the direct distance × departure-anomaly interaction
after identifying Ralston et al. (2025), which explicitly highlighted migration
distance as a candidate determinant of compensation following delayed spring
departure.

Both revisions were literature-driven and occurred before Wang migration-timing
outcomes were inspected.
