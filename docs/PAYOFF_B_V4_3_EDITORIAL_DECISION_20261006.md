# PAYOFF-B V4.3 editorial decision — 2026-10-06

Status: **CURRENT AMERICAN NATURALIST DEVELOPMENT ROUTE**

## Decision

Target the integrated theory-plus-natural-evidence paper first as an American Naturalist Major Article.

Canonical development manuscript:
`manuscript/PAYOFF_B_INFORMATION_VALUE_ACTIONABILITY_V4_3_AMNAT.md`

Canonical front matter:
`submission/AMNAT_V4_3_FRONTMATTER_20261005.md`

## Central ecological question

How should seasonal tracking be understood when the value of environmental information and the opportunity for downstream correction are separate quantities?

## Central answer

Seasonal timing is produced by at least two distinct control layers:

1. **forecast value** — how much decision-relevant uncertainty current information removes;
2. **correction opportunity** — how much timing error can still be changed after commitment.

Standardized environmental correlation is not itself forecast value, and forecast value is not itself realized biological adjustment.

## Bird result

Registered primary result:
- detrended source-destination rho increased from 0.284 to 0.653;
- mean delta-rho +0.369;
- 26/28 species positive;
- dependence-robust.

Posthoc scale diagnostic:
- target anomaly SD 2.41 -> 4.66 d;
- source-informed LOO RMSE 4.11 -> 4.17 d;
- target-history-only LOO RMSE 3.18 -> 5.86 d;
- G_CV = MSE(no source) - MSE(source) changed from -16.09 to +15.99 d^2;
- delta G_CV +32.08 d^2;
- all source/target/spatial dependence intervals positive;
- 25/28 species show positive delta G_CV;
- exact-complete 58-pair delta G_CV +28.30 d^2;
- global omission of each calendar year leaves 16/16 positive means and 16/16 CIs above zero.

Licensed ecological interpretation:
> As spring phenology became more variable, contemporaneous cross-site environmental information gained substantial out-of-sample predictive value relative to a target-history baseline.

Not licensed:
- birds perceived or used the reconstructed source information;
- source information caused stable mismatch;
- downstream correction caused stable mismatch;
- climate change caused the two-window contrast;
- the posthoc information-value result was preregistered.

## Mule-deer role

Mule deer remain an independent mechanism anchor showing that downstream signed phase correction is biologically real:
- start-to-end phase variance contracts strongly;
- late individuals move faster and stop less;
- early individuals show the opposite adjustment.

This does not identify the bird mechanism and does not jointly estimate G(t) and r(t).

## Theory

Use the general decision-scale form:

    G(t) = L0(t) - L1(t)
    N(t) = r(t) G(t) - C(t)

The prior binary-cue model G(t)=S q(t)-B and its closed-form t* are retained as a special case.

For Gaussian timing prediction under squared loss:

    baseline risk = sigma_Y^2
    residual risk = sigma_Y^2 (1-rho^2)
    information value = sigma_Y^2 rho^2.

These are standard decision/prediction results, not claimed as new mathematics.

## Novelty boundary

Do not claim novelty for:
- value of information;
- cue-optimum variance decomposition;
- current versus climatological synchrony;
- feedforward versus feedback control;
- sequential cue acquisition;
- increasing spatial synchrony under warming.

The contribution that survives is the empirical and mechanistic synthesis:
> standardized coupling, absolute environmental variability, decision-scale forecast value, and biological correction opportunity can move differently through the same seasonal system.

## Main figures

1. Information value versus residual uncertainty versus actionability.
2. Bird environmental result: rho, target variability, cross-validated G_CV, and day-scale mismatch.
3. Mule-deer phase funnel and signed actuator responses.

## Journal position

American Naturalist remains the first target.

Ecology Letters / PNAS / Nature Ecology & Evolution would require a direct natural test measuring G(t), r(t), and behavior along the same seasonal trajectory.

## Superseded route

`docs/PAYOFF_B_V4_2_EDITORIAL_DECISION_20261005.md` is retained as provenance but is superseded because its headline equated increasing rho with improved environmental predictability.