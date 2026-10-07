# PAYOFF-B barnacle-goose joint q–r identification

Date: **2026-10-07**  
Status: **prospective public-data reanalysis design; no new goose outcome opened to choose the primary direction**

## 1. Question

Can environmental predictability and remaining behavioral recourse be measured
**independently at the same migration stages**?

This is the empirical identification problem exposed by the PAYOFF-B
competitive-information boundary case.

The target is not another generic migration-timing correlation.

The target is to separate:

\[
Q_j
=
\text{predictive quality of information available at route stage }j
\]

from

\[
R_j
=
\text{remaining capacity to alter downstream timing after stage }j.
\]

Only after those are estimated independently do we examine

\[
A_j=Q_jR_j
\]

as a descriptive actionable-predictability coordinate.

\(A_j\) is **not** assumed numerically equal to the canonical binary PAYOFF
information value.

## 2. Natural system

Kölzsch et al. (2015), *Journal of Animal Ecology* 84:272–283,
DOI 10.1111/1365-2656.12281.

Three barnacle-goose flyways:

- Greenland;
- Svalbard;
- Barents Sea.

The paper combines many individual stopover sites into **16 general stopover
regions** and quantifies climatic predictability between consecutive regions
from 30 years of spring-onset data (1982–2011).

Original stopover definition:

- bird remains within a 30-km radius;
- for longer than 48 h;
- maximally one outlier location is allowed.

Original breeding-site definition:

- last stopover before end of June;
- residence 7–26 days.

Initial stopovers were excluded from arrival-time analyses when tagging was too
late to determine true arrival.

## 3. Public tracking archives

Movebank Data Repository, CC0:

### Greenland

DOI: 10.5441/001/1.5d3f0664

Repository GPS file:

    Migration timing in barnacle geese (Greenland) (...).csv

Machine audit performed 2026-10-07:

- 6,853 location rows;
- 7 archived individual IDs;
- years 2008–2010;
- coordinates complete;
- median within-track interval ≈ 2 h;
- no provider ground-speed column.

### Svalbard

DOI: 10.5441/001/1.5k6b1364

Machine audit:

- 24,488 location rows;
- 22 archived individual IDs;
- years 2006–2011;
- coordinates complete;
- median within-track interval ≈ 2 h;
- no provider ground-speed column.

### Barents Sea

DOI: 10.5441/001/1.ps244r11

Machine audit:

- 21,102 location rows;
- 15 archived individual IDs;
- years 2008–2011;
- coordinates complete;
- median within-track interval ≈ 3 h;
- provider ground-speed and heading columns are present.

### Critical eligibility mismatch

The published analysis states:

- Greenland N=7;
- Svalbard N=21;
- Barents Sea N=12.

The raw archive currently exposes:

- Greenland 7 IDs;
- Svalbard 22 IDs;
- Barents Sea 15 IDs.

Therefore the public archive is **not mechanically identical to the final
analytic sample**.

Primary inference must not proceed until the original inclusion/exclusion logic
is reproduced from reference/deployment metadata, track coverage, or explicit
paper criteria.

Archive presence alone is not an eligibility rule.

## 4. Environmental predictability Q

The Supporting Information contains:

- Table S1: mean and SD of GDD-jerk peak dates (spring onset) by stopover
  region;
- Tables S2–S7: annual spring-onset anomalies for pairs of consecutive
  stopover regions by flyway.

The paper's link quantities are:

- Pearson correlation between consecutive-region spring anomalies;
- regression slope / proportionality index.

We retain those for source-faithful reproduction.

For the PAYOFF reanalysis, we add a forecasting metric calculated from exactly
the same anomaly pairs:

\[
Q_j^{\rm LOO}
=
1-
\frac{\mathrm{MSE}_{\rm linear,LOO}}
     {\mathrm{MSE}_{\rm climatology,LOO}}.
\]

The model for each held-out year predicts next-region spring anomaly from the
current-region anomaly using all other years.

Raw \(Q^{\rm LOO}\) may be negative.

For the descriptive product \(A_j\) only:

\[
Q_j=\min[1,\max(0,Q_j^{\rm LOO})].
\]

Do not silently substitute \(|r|\), \(r^2\), or the published correlation for
this forecast-skill coordinate.

Implementation:

    src/goose_joint_identification.py
    climate_link_predictability()

## 5. Behavioral recourse R

### 5.1 Identification rule

Do **not** infer recourse from:

- final-arrival correlation;
- phase-retention lambda;
- mismatch residuals;
- the observed attenuation of timing error.

Those are timing responses and would recreate the mechanism-aliasing problem.

### 5.2 Primary empirical R: remaining-schedule envelope

For each retained stopover region \(j\), and each eligible track that visits it,
measure

\[
T^{remain}_{ij}
=
\text{elapsed time from departure at region }j
\text{ to arrival at the declared breeding stage}.
\]

Use elapsed duration, not the absolute calendar date of breeding arrival.

Across tracks:

\[
T_j^{fast}=P_{10}(T_j^{remain}),
\]

\[
T_j^{typ}=P_{50}(T_j^{remain}),
\]

\[
T_j^{slow}=P_{90}(T_j^{remain}).
\]

Advance recourse:

\[
C_j^{adv}=T_j^{typ}-T_j^{fast}.
\]

Delay recourse:

\[
C_j^{delay}=T_j^{slow}-T_j^{typ}.
\]

Normalize each direction by its value at the first retained stage.

This definition automatically includes realized combinations of:

- migration-speed changes;
- shorter or longer stopovers;
- skipped stopovers;
- alternative downstream route schedules.

Unlike a component-sum construction, empirical \(R_j\) is **not forced to be
monotone**. A downstream bottleneck or route alternative can create local
increases in observed timing flexibility.

Implementation:

    src/goose_joint_identification.py
    remaining_duration_recourse()

### 5.3 Secondary mechanistic decomposition

After reproducing stopovers, decompose the route into:

- transit / flight components;
- stopover components.

For component k:

\[
C_k^{adv}
=
P_{50}(T_k)-P_{10}(T_k),
\]

\[
C_k^{delay}
=
P_{90}(T_k)-P_{50}(T_k).
\]

Summing remaining component capacities gives a mechanistic secondary estimate
of where timing flexibility resides.

This component-sum version is useful for attributing recourse to flight versus
stopover control, but it is secondary because skipped-route architectures make
strict component alignment less natural.

Implementation:

    observed_recourse_envelope()

### 5.4 Movement speed

For Barents Sea the archive contains a ground-speed field, but the cross-flyway
primary analysis must use one common definition.

Therefore compute displacement speed from timestamp + coordinates for **all
three flyways**.

Provider ground speed in Barents Sea is a validation variable, not the primary
cross-flyway definition.

## 6. Alignment of Q and R

For a climate-predictability link

    current stopover region j -> next region j+1,

pair \(Q_j\) with the recourse still available **after departure from region
j**.

The stage is therefore the decision state at the current region, not arrival at
the next one.

The descriptive coordinate is

\[
A_j=Q_jR_j.
\]

Primary direction for late correction uses \(R_j^{adv}\).

Early-correction analysis uses \(R_j^{delay}\) separately.

## 7. Primary questions

### Q1 — Is maximum predictive skill also maximum actionable predictability?

Compare:

\[
\arg\max_j Q_j
\]

with

\[
\arg\max_j A_j.
\]

The PAYOFF hypothesis is that they need not coincide.

### Q2 — Does actionable predictability peak before the end of the route?

Because information can improve while recourse disappears, an intermediate
maximum is possible.

This is a prospective test, not a guaranteed prediction for every flyway.

### Q3 — Do ecological barriers affect Q without equivalently affecting R?

The original paper reports weaker spring-onset correlations across major
oceanic/inland barriers.

The joint framework predicts that barrier-driven information loss and
actuator-derived recourse are separable axes.

### Q4 — Does independent R explain timing correction beyond Q alone?

Only after Q and R are frozen, test whether downstream actuator use or timing
correction is better explained by:

    Q only

versus

    Q + R

versus

    Q × R.

This downstream test is secondary because actuator use also contributes to the
construction of R and must be defined without circular reuse of the same
response.

A clean version should use component envelopes from training tracks and evaluate
timing response on held-out tracks.

## 8. Split strategy

Sample size is small, especially for Greenland.

Do not create arbitrary 70/30 individual splits that leave too few trajectories.

Primary robustness should instead use:

1. leave-one-individual-out reconstruction of duration envelopes;
2. leave-one-year-out climate predictive skill;
3. flyway-level replication as three independent ecological architectures.

Any held-out actuator-response test must freeze its component envelope using
only non-held-out trajectories.

## 9. Failure conditions

Hold the direct q–r empirical claim if any of the following occurs:

- published analytic sample cannot be reproduced;
- stopover detection cannot approximately reproduce reported stage counts;
- too few repeated component durations exist to estimate P10/P50/P90;
- spring-anomaly supplement cannot be mapped unambiguously to stopover regions;
- route components cannot be aligned consistently with the climate links.

In that case retain only the theoretical identification warning.

## 10. Claim boundary

Safe:

> The public goose system contains both long-term cross-site spring
> predictability data and high-resolution movement tracks from which downstream
> actuator timing can be reconstructed.

Safe:

> PAYOFF-B can estimate predictive information and remaining recourse from
> separate observables in this system.

Not yet licensed:

> Barnacle geese maximize Q × R.

Not yet licensed:

> The route has an intermediate actionable-information optimum.

Not yet licensed:

> Observed component-duration envelopes equal physiological maximum recourse.

Not yet licensed:

> Differences among flyways causally arise from ecological barriers without
> further controls.
