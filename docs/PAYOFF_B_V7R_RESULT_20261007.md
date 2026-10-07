# PAYOFF-B V7R result — forecast predictability is not the feedback-information coordinate

Date: **2026-10-07**

Status: **PRIMARY NUMERIC NULL; ACTIVE-CORRECTION INTERPRETATION NOT LICENSED**

## 1. Frozen test opened

The source-only gate admitted ten transition types across all three barnacle-goose flyways.

The frozen model was

\[
C_e
=
\alpha_{\rm flyway}
+
\beta_Q Q_e
+
\beta_R R_e
+
\beta_{QR}Q_eR_e
+
\epsilon_e,
\]

with

\[
C_e=1-|\lambda_e|.
\]

The directional prediction was

\[
\beta_{QR}>0.
\]

Nine previously reported transition lambdas reproduced from row-level transition pairs to machine precision:

\[
\max |\Delta\lambda|=5.55\times10^{-16}.
\]

The tenth transition was opened with the same estimator:

- Barents R5→R7
- \(n=7\)
- 3 individuals
- \(\lambda=0.8328581286\).

## 2. Primary result

Observed interaction:

\[
\hat\beta_{QR}=1.3733376462.
\]

Exact within-flyway Q-label permutation:

- 2880/2880 valid permutations
- one-sided \(p_{\rm perm}=0.569940993\)
- permutation median = 1.6330.

The observed positive coefficient is below the permutation median.

Therefore:

\[
\boxed{\text{V7R primary numerical prediction not supported.}}
\]

This is not an “almost significant” pattern.

## 3. Prespecified sensitivities

No prespecified sensitivity rescued the interaction.

| Analysis | \(\beta_{QR}\) | exact permutation \(p\) |
|---|---:|---:|
| Primary Q10–Q90 remaining recourse | 1.373 | 0.570 |
| weighted by transition \(n\) | 0.906 | 0.656 |
| Q20–Q80 remaining recourse | 1.151 | 0.530 |
| local one-step temporal width | 0.024 | 0.465 |
| signed POWER phenology \(r\) | 1.371 | 0.570 |
| POWER \(r^2\) | 1.088 | 0.607 |
| POWER anomaly slope | 1.252 | 0.611 |
| exclude low-individual-support R5→R7 | 1.436 | 0.549 |
| ERA5 \(|r|\) | 1.562 | 0.497 |
| ERA5 signed \(r\) | 1.377 | 0.530 |
| ERA5 \(r^2\) | 0.905 | 0.603 |

Leave-one-transition-out estimates stayed positive, but none produced permutation support.

The closest deletion was Barents R1→R2:

\[
\beta_{QR}=4.895,\qquad p_{\rm perm}=0.121.
\]

Raw \(\lambda\) as a descriptive endpoint gave essentially no interaction:

\[
\beta_{QR}=0.00836,
\qquad
p_{\rm two-sided}=0.991.
\]

The null is therefore not an environmental-product artifact or a single-transition artifact.

## 4. Critical estimand audit

The frozen response is not a clean measure of active correction.

The already existing PAYOFF route-wise identity is

\[
\lambda_t=\phi_t(1-g_t),
\]

where

- \(\phi_t\) = passive phase carry-over / target-state persistence;
- \(g_t\) = active feedback gain.

Therefore

\[
1-|\lambda|
\]

cannot be identified with active correction unless \(\phi\) is independently identified.

This matters here because \(Q\) is itself cross-region environmental predictability. Changing environmental persistence can change \(\lambda\) even without a change in behavioral feedback.

So both statements must be kept simultaneously:

1. **the preregistered numerical Q×R test is null**;
2. **that response cannot cleanly answer whether active correction is Q×R-dependent**.

## 5. Direct behavioral actuator check

The Stage-3 data contain a more direct actuator:

\[
G_e
=
-\operatorname{slope}
(\text{origin stopover duration}
\sim
\text{incoming phase error}).
\]

Positive \(G\) means a late bird shortens its stopover.

The nine existing gain values reproduced to machine precision. The new Barents R5→R7 gain was

\[
G=0.51048248.
\]

### Transition-level test

\[
\beta_{QR}=0.441857,
\qquad
p_{\rm perm}=0.750087.
\]

Weighted by transition \(n\):

\[
\beta_{QR}=0.232196,
\qquad
p_{\rm perm}=0.767789.
\]

Replacing POWER Q with ERA5 Q:

\[
\beta_{QR}=0.774162,
\qquad
p_{\rm perm}=0.593891.
\]

### Row-level actuator test

All 95 individual transition rows were retained with transition-specific intercepts.

The focal term was

\[
\text{incoming phase error}\times Q_{\rm forecast}\times R.
\]

Stronger corrective shortening predicts a negative coefficient.

Observed:

\[
\hat\beta_{EQR}=-0.277659,
\qquad
p_{\rm perm}=0.429712.
\]

Thus the direct stopover actuator also does not support the original \(Q_{\rm forecast}\times R\) prediction.

## 6. The informative counterexamples

The strongest clue is not a marginal p value. It is that strong stopover feedback occurs on transitions with almost no endpoint spring predictability.

### Barents R1→R5

- \(|r_{\rm phenology}|=0.00238\)
- \(R=1.00\)
- \(\lambda=-0.00857\)
- stopover gain \(=0.78696\).

### Svalbard R2→R4

- \(|r_{\rm phenology}|\approx0.00148\)
- \(R\approx0.175\)
- \(\lambda=-0.10632\)
- stopover gain \(=0.588996\).

Therefore high cross-site climatic predictability is not a necessary condition for strong stopover response to incoming phase error in these data.

## 7. The information coordinate was too coarse

The attempted Q combined two different biological information problems.

### Forecast / feedforward information

\[
q_F(t)
=
\text{how well current conditions predict future-region conditions}.
\]

The Kölzsch consecutive-region 30-year spring correlations measure this type of information.

### Feedback / state-estimation information

\[
q_B(t)
=
\text{how accurately the migrant can infer its current phase error locally}.
\]

This is the information required by the route-wise feedback controller.

They are not equivalent:

\[
\boxed{q_F(t)\neq q_B(t)}.
\]

A migrant can have poor long-range forecasting information and still make strong closed-loop corrections after observing local conditions.

This interpretation is consistent with the migration literature: Kölzsch et al. explicitly discuss different cue types at different migration stages, while migration-network theory emphasizes repeated updating at intermediate stopovers.

## 8. Consequence for PAYOFF-B

The competitive-information audit forced separation of different reasons information value can disappear.

V7R now forces a second separation:

\[
\text{information about the future state}
\neq
\text{information about current mismatch}.
\]

A one-dimensional \(q(t)\) is therefore too coarse for the sequential migration controller.

The next theory version should distinguish at least:

\[
q_F(t)=\text{forecast/feedforward information},
\]

\[
q_B(t)=\text{feedback/state-estimation information},
\]

and

\[
r(t)=\text{retained actionability}.
\]

## 9. Stop rule

Do not tune thresholds, add transitions, or add taxa to rescue the failed interaction.

Close:

\[
\boxed{\text{V7R }q_F\times r\text{ route = NOT SUPPORTED}.}
\]

Any \(q_B\) test must begin under a new prospective contract with an independent local cue-reliability coordinate that is not constructed from the focal stopover or phase-correction response.
