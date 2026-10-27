# PAYOFF-B 2026-10-19: empirical stage timing audit and scientific verdict

## 1. Preregistered stork 53-season result — **NOT SUPPORTED**

The original pre-outcome registration
`docs/PAYOFF_B_STORK_STAGE_PROPAGATION_PILOT_LOCK_20261019.md`
was executed without changing the Jan-Apr winter-referenced source filter:
53 animal-years / 27 animals / five years. The year-fixed-effect estimate
for the original 20% → 80% northward passage-time relationship was
**β = 0.82436**, with 2,500 animal-cluster bootstrap samples giving
95% interval **[0.55059, 1.15306]**. The registered compression
support rule requires β<1 AND upper CI <1; it fails.

Within-animal repeated-source estimate β = 0.48279 was an explicitly
secondary descriptive metric, not a positive confirmatory primary claim.
The leave-one-animal-out range was [0.75036, 0.92900]; all 2,500
bootstrap samples were estimable. Calendar leap correction did not change
the year-FE slope. Full receipt:
https://github.com/zuizui0223/payoff/actions/runs/39222907002

## 2. Different within-Feb-May source geometry: exploratory five-system panel

The separate source-geometry filter was registered after identifying
which archived bird GPS streams had available temporal coverage.
It is NOT an alternative primary stork analysis and cannot replace
the negative predeclared 53-season result.

| Source taxon | Instrument | Admitted animal-years | Year-FE β(T80~T20) | Animal-bootstrap 95% CI |
|---|---|---:|---:|---:|
| Ciconia ciconia | GPS | 91 | +0.84240 | +0.73137 to +0.92623 |
| Scolopax minor | Argos | 37 | +0.34723 | −0.06218 to +0.78165 |
| Anser albifrons | GPS | 23 | +0.03541 | −0.01960 to +0.08156 |
| Numenius arquata | GPS | 7 | **NOT_ESTIMABLE** | — |
| Anas acuta / A. platyrhynchos | GPS | 0 | **NOT_ESTIMABLE** | — |

The 23 white-fronted-goose source pairs are each from different animal
IDs: there is no within-animal replication, and their underlying cohort
may overlap previously opened PAYOFF goose evidence. Woodcock Argos
location accuracy and sample timing cannot be equated to stork/goose GPS.
The exploratory stork 91-season β differs in source definition from the
registered original 53-season one. Species means are therefore NOT
pooled into a universal effect and the between-system contrast is NOT
tested as a causal ecological interaction.

Source run:
https://github.com/zuizui0223/payoff/actions/runs/39224044652

## 3. Independent source-window null — no active adaptation required

A fully synthetic model with independent entry timing X and independent
duration W, Y=X+W, has OLS β(Y~X)=0.999984 with no observation censoring
and β=0.657013 when restricted to Y≤day 120. It contains **zero**
behavioral feedback by construction, showing that observation-window
selection alone can create apparent temporal "compensation". Its synthetic
parameters are not fitted or tuned to the real bird data.

Source run:
https://github.com/zuizui0223/payoff/actions/runs/39223641740

## 4. Ecological result, boundary and next real observation

**Directly observed:** same-form year-adjusted associations between two
retrospectively defined latitude progression checkpoints differ across
archive systems, and the originally registered stork compression claim is
not supported.

**Not established:** actual breeding arrival, stage-resolved signed
active correction, reliability and availability of environmental cues
BEFORE route decisions, physiological feasible recourse, individual
fitness benefit, between-species generality, or independence of all
historical tracking cohorts.

Do not interpret the very small goose β as strong active reset and do
not prefer the exploratory stork β simply because its confidence interval
falls below one. The window-censoring null and sensor-specific uncertainty
must accompany all prose discussing those patterns.

**Next independent biological gate:** derive real departure and checkpoint
time intervals at validated stops; add dated, external local wind/
temperature/vegetation cues known before a decision; estimate the feasible
response set without using the focal bird's observed choice; compare
downstream signed action and phase. Do not modify existing V7R/V8 or the
53-season stork primary outcome.
