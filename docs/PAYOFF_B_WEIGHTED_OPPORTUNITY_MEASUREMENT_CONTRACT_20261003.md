# PAYOFF-B weighted opportunity measurement contract

Date: **2026-10-03**  
Status: **prospective SI / identification guard; V3 main-text scope remains locked**

## Goal

Operationalize

\[
\omega_{\rm eff}
=
\frac{\sum_j o_js_j}{\sum_j s_j}
\]

without silently replacing checkpoint precision contribution \(s_j\) by site
count, habitat area, betweenness, or raw phase retention.

## 1. What \(s_j\) means

\(s_j\) is checkpoint \(j\)'s historical contribution to downstream
**log-precision** on the focal inherited phase-error coordinate.

It is not:
- occupancy;
- stopover duration by itself;
- habitat area;
- site centrality;
- number of visits;
- raw \(|\lambda_j|\).

Under the declared portfolio model, contributions are additive in log variance.

## 2. Strong identification route

Suppose checkpoint \(j\) has independently identified passive phase retention
\(\phi_j\) and observed closed-loop phase retention \(\lambda_j\), measured on
the same transition and phase coordinate.

When active control contracts inherited error in magnitude,

\[
0<|\lambda_j|\le|\phi_j|,
\]

the active correction factor is

\[
r_j
=
\frac{|\lambda_j|}{|\phi_j|}.
\]

The corresponding active log-precision contribution is

\[
\boxed{
f_j
=
-2\log r_j
=
2\log\frac{|\phi_j|}{|\lambda_j|}.
}
\]

Then normalized checkpoint weights are

\[
p_j
=
\frac{f_j}{\sum_k f_k},
\]

and effective opportunity retention is

\[
\boxed{
\omega_{\rm eff}
=
\sum_j o_jp_j.
}
\]

This route estimates realized historical precision contribution directly; it
does not require separately fitting the quadratic \(c_j^2/b_j\) witness.

## 3. Why raw lambda is insufficient

Without \(\phi_j\),

\[
\lambda_j
=
\phi_j\times
\text{active correction factor}.
\]

A small \(|\lambda_j|\) can therefore arise from:
- strong active correction;
- weak passive carry-over;
- both.

Accordingly,

\[
-2\log|\lambda_j|
\]

can summarize total inherited-error contraction but cannot be licensed as
historical **feedback** precision share unless passive retention is separately
handled.

This is the same identification boundary already imposed by the route-wise
phase-control model.

## 4. Overshoot boundary

Negative \(\lambda_j\) can reflect overshoot, anticipation, moving targets, or
coordinate changes.

Magnitude contraction can still be described by \(|\lambda_j|\), but a
negative-retention stage should not be inserted mechanically into a positive
precision-budget interpretation without a stage-specific mechanistic audit.

## 5. Opportunity-retention variable

\(o_j\in[0,1]\) measures the fraction of checkpoint \(j\)'s historically used
correction function that remains after perturbation.

It must be defined independently of the downstream timing outcome.

Examples of relevant ingredients include:
- retained stopover/refuelling function;
- retained ability to wait or accelerate later travel;
- accessible alternative route stages;
- retained information acquisition;
- energetic cost of using substitutes.

Named-site survival is only a proxy when the lost function cannot be replaced.

## 6. Substitution

If a lost checkpoint is replaced by an alternative, the alternative can
preserve effective opportunity.

For the immediate historical-allocation theorem, \(o_j\) represents retained
function relative to the historical contribution.

If organisms actively reallocate control effort to new sites after disruption,
that is **re-optimization/substitution**, not simple opportunity retention, and
requires a separate model or an empirically measured post-change precision
allocation.

## 7. Selection and observation

A valid fragility test also requires the #281 selection guard.

Even with correctly measured \(\omega_{\rm eff}\), population-level final
variance cannot be attributed to within-individual clock fragility when
survival/observation reweights timing phenotypes.

The preferred design therefore combines:
1. independently measured \(\omega_{\rm eff}\);
2. repeated-individual phase tracking;
3. explicit survival/observation accounting.

## 8. Admission rule

A natural portfolio-fragility test can use weighted opportunity only if,
before downstream outcome inspection:

- checkpoint phase coordinates are declared;
- passive-retention reference or another feedback-identification strategy is
  specified;
- \(o_j\) is defined independently of downstream mismatch;
- substitution rules are frozen;
- selection/observation handling is frozen.

Otherwise the system remains an opportunity-loss or migration-network anchor.

## 9. Relation to migration-network centrality

Betweenness, functional connectivity and critical-node metrics can help
identify candidate important sites, but they are not automatically
phase-correction leverage.

A direct empirical study may test whether network centrality predicts
\(f_j\), but it must not set

\[
f_j=\text{centrality}_j
\]

by definition and then claim confirmation.

## 10. Current status

No current PAYOFF-B natural system passes this measurement contract together
with the #281 direct-test triangle.

The natural portfolio-fragility lane therefore remains closed.
