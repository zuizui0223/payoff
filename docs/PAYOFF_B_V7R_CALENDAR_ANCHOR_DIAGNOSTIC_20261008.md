# PAYOFF-B V7R post-outcome calendar-anchoring diagnostic

Date: **2026-10-08**  
Status: **POST-OUTCOME EXPLORATORY; NOT A NEW CONFIRMATION**

This note **does not** modify the frozen V7R source precheck, primary
\(\beta_{QR}\) result, or preregistered sensitivity endpoints.

## 1. Motivation and preserved primary result

The V7R source-registered meta-analysis tested whether historical
cross-stopover spring-onset predictability \(Q\) and a route-duration-envelope
proxy for remaining temporal recourse \(R\) jointly predicted phase retention.

Frozen primary:

- 10 transition types in three flyways;
- \(\beta_{QR}=+1.373337646\);
- exact within-flyway permutation \(p=0.569941\);
- **not supported**.

The independently archived sensitivity receipt also remains null across the
prespecified definitions.

A post-outcome observation motivated this diagnostic: the Barents R1→R5
transition has near-zero cross-site spring predictability but near-zero phase
retention. This does **not** by itself prove successful active correction.

## 2. Exact accounting decomposition

For each tracked transition, let:

- \(A_0\): arrival date at the origin local stop;
- \(D_s\): duration at that local stop;
- \(D_t\): transit time to destination;
- \(A_1=A_0+D_s+D_t\): arrival date at destination;
- \(S_0,S_1\): region-year environmental-onset coordinates used in Stage-3;
- \(E_0=A_0-S_0\), \(E_1=A_1-S_1\): phase coordinates.

The row-wise identity is:

\[
E_1=E_0+D_s+D_t+S_0-S_1.
\]

Regress every component on \(E_0\) within the same transition, with an
intercept. By linearity,

\[
\boxed{\lambda
=1+\beta_{\mathrm{stay}}+\beta_{\mathrm{transit}}
+\beta_{\mathrm{spring}}}.
\]

This is **an arithmetic / covariance identity**, not an identified structural
partition of causal active feedback versus passive forcing.

Across all 10 registered transition types, the decomposition reproduces the
Stage-3 phase transfer within floating-point precision.

## 3. Barents R1→R5: striking but observational

The data contain 10 transitions from six tagged individuals across 2008–2010.

Historical cross-stopover spring-onset predictability:

\[
Q=|\rho_{\rm spring}|=0.0023829.
\]

Phase-retention decomposition:

| component | observed slope |
|---|---:|
| baseline carry-over | +1.000000 |
| local stopover duration | −0.786957 |
| transit duration | +0.019389 |
| origin minus destination spring | −0.241003 |
| **net phase-retention \(\lambda\)** | **−0.008571** |

A bookkeeping operation that sets the covariance contribution of local stay to
zero would change the resulting slope to \(+0.778387\). **Do not interpret
this as an intervention counterfactual.**

Cluster resampling of the six individuals (4,000 draws) for the stopover slope:

- point estimate −0.786957;
- percentile 95% interval approximately −0.956 to −0.568;
- 99.8% of resamples have a negative slope.

This supports a **descriptive timing association**, not its causal origin.

## 4. Calendar departure synchronization

Because \(D_s=T_{\rm departure}-A_0\),

\[
\beta(D_s\sim A_0)
=
\beta(T_{\rm departure}\sim A_0)-1.
\]

In Barents R1→R5:

- departure date on last-local-stop arrival date slope = **+0.0353**;
- within-year departure-on-arrival slope = **+0.0319**;
- within-year departure/arrival spread ratio = **0.138**;
- bootstrap 95% interval of departure-on-arrival slope ≈ −0.150 to +0.147.

Within-year ranges:

| year | transition rows | last local stop arrival range | departure range |
|---|---:|---:|---:|
| 2009 | 6 | 69.67 days | 10 days |
| 2010 | 3 | 39.96 days | 5 days |

Estimated local spring-onset date at origin R1 (POWER reconstruction):

| year | reconstructed spring onset, DOY | mean departure, DOY |
|---|---:|---:|
| 2008 (n=1) | 77.70 | 139.67 |
| 2009 (n=6) | 92.90 | 136.50 |
| 2010 (n=3) | 108.56 | 139.00 |

Descriptively, the local spring reconstruction shifts by about **30.9 days**
while the departures stay in a much narrower annual calendar window.
Three years are **not enough** to infer a reliable environmental-cue effect.

## 5. Important origin-definition audit

Barents R1 is centred near \(53.47^\circ\) N, \(6.76^\circ\) E — a
Netherlands wintering / initial-staging region.

All ten focal transitions originate at a **second or later observed local
stopover within R1**:

- stop index 2: 4 transitions;
- index 3: 4;
- index 4: 1;
- index 5: 1.

None of the ten focal origin-arrival timestamps is the first observed
stopover arrival within the wintering region.

Consequently, the extreme spread of the "origin arrival" dates partly measures
**how the last local stop was selected**, not how far apart the animals first
arrived at a migration-stage region. This can induce apparently strong
stay-versus-arrival compensation even without cue-responsive correction.

Kölzsch et al. (2015) also warned that initial stopover arrival times may be
uncertain because tagging occurred after animals arrived, and discussed
partially fixed migration schedules / photoperiod-based cues as an explanation
when predictive connectivity is poor.

Primary paper: https://doi.org/10.1111/1365-2656.12281

## 6. Ecological interpretation and stop rule

**Observed:** Some individuals reached the last wintering-region local stop
at very different dates but departed the larger region in a much narrower
calendar window. The phase slope near zero has contributions from both
stay-time covariance and environmental-coordinate covariance.

**Compatible hypotheses:**

1. fixed/photoperiod-linked departure schedule;
2. energetic readiness and synchronization before an ecological barrier;
3. active stagewise timing feedback;
4. source-data construction / within-region last-stop selection effects.

The current data and decomposition **cannot distinguish these mechanisms
causally**.

It is especially important that a near-zero cross-site climate correlation
\(Q_{\mathrm{forecast}}\) does not imply there were no locally accessible cues
\(Q_{\mathrm{feedback}}\).

This observation is **not** a successful rescue of the registered
\(Q_{\mathrm{forecast}}\times R\) interaction.

The useful next research distinction is:

- a fixed calendar/photoperiod schedule;
- local environmentally responsive feedback;
- energetic constraints before a barrier.

A confirmation route needs a separately specified dataset with direct,
time-stamped cue and physiological/behavioral measurements or an exogenous
perturbation. Do not select another V7R transition after seeing these results
and call it independent verification.

## 7. Provenance

Unchanged Stage-3 workflow archives:

- multiflyway SHA256
  \`8e720be44e0ef2e3e497786c9241c6625b4b14c46506fbb30ea027dcdf36749f\`
- Svalbard SHA256
  \`29558f9b8b43a7375b3922118a77b74464558f4869a7722472570a32745f2856\`

This is separate from the existing V7R post-outcome sensitivity/reproducibility
audit. The original V7R receipt and its noted numerical drift are preserved.
