# PAYOFF-B: conditional checkpoint information and bounded timing response

Date: 2026-10-08
Status: prospective toy decision model, stacked on the sequential-refresh PR; **no post-hoc V7R rescue**.

## Ecological problem

A checkpoint cue can correlate strongly with destination spring while revealing **no new information** beyond what an animal already knew at departure. Conversely, a weak origin cue can make an identical checkpoint cue genuinely informative. Whether either cue helps fitness also depends on independently specified response capacity.

This branch fixes a construct ambiguity in the prior prospective sequential-refresh model: its reduced proxy A_m = r_m I_m uses the **standalone** predictive quality of checkpoint m rather than the extra information conditional on the animal's earlier cue history. The product r_m I_m is an exploratory coordinate, not a general Bayes-optimal fitness value.

The prospective question becomes:

> Does incremental forecast improvement beyond departure-time cues drive independently measurable downstream adjustments only while timing recourse is physically available?

## 1. Gaussian information renewal

Let standardized seasonal states X_0,...,X_n follow a Gaussian Markov chain:

    X_{j+1} = rho_j X_j + sqrt(1-rho_j^2) epsilon_j,

with independent standard normal innovations and |rho_j| <= 1. An actor has the origin cue Z_0=X_0+nu_0, then a checkpoint cue Z_m=X_m+nu_m. Cue noises are independent Gaussian with variances tau_0^2 and tau_m^2. The target is H=X_n.

Define

    a = product_{j=0}^{m-1} rho_j,
    b = product_{j=m}^{n-1} rho_j,
    v_0 = 1+tau_0^2,
    v_m = 1+tau_m^2.

Origin-only squared predictive correlation:

    R0^2 = (a*b)^2 / v_0.

Checkpoint-only squared predictive correlation:

    Rm,standalone^2 = b^2 / v_m.

**Incremental destination explained variance** conditional on origin information:

    Delta R^2
       = [b*(1-a^2/v_0)]^2 / [v_m - a^2/v_0].          (1)

If the denominator vanishes because the two observations are identical and perfectly measured, Delta R^2=0. With both cues the destination explained variance is R0^2+Delta R^2.

Equation (1) is standard Gaussian conditioning, **not new probability theory**.

### Exact counterexample

Both routes have identical perfect checkpoint-to-target predictability (b=0.9, standalone R^2=0.81).

| Upstream link a | Origin R² | Checkpoint-only R² | Incremental R² |
|---|---:|---:|---:|
| 1.0 — origin already reveals checkpoint | 0.81 | 0.81 | **0.00** |
| 0.0 — origin fails to predict checkpoint | 0.00 | 0.81 | **0.81** |

A high local correlation does not by itself establish learning, renewal, or adaptive value.

## 2. Convert information to an explicit timing-control payoff

Let u be an adjustable standardized arrival/breeding phase. The animal minimizes

    E[(H-u)^2 | available cues] + kappa*u^2,   |u| <= L,

where kappa >= 0 penalizes intervention and L >= 0 is an **exogenously measured physical timing-adjustment limit**. Do not infer L from phase-retention slopes, which can arise under fixed calendar departure.

For mu=E[H | cues], the optimal adjustment is

    u*(mu) = clip(mu/(1+kappa), -L, L).

Let v=Var(mu)=explained variance R², c=1+kappa, s=sqrt(v), and t=cL/s. Let phi and Phi denote standard normal density and CDF. Its **exact ex-ante expected reduction in phase loss** is

    G(v,L,kappa)
      = (v/c)*(2*Phi(t)-1)
        + 2*L*s*phi(t)
        - 2*c*L^2*(1-Phi(t)).                           (2)

For v=0 or L=0 set G=0. Also

    0 <= G <= v/(1+kappa),
    lim_{L->infinity} G = v/(1+kappa).

The value of acquiring checkpoint information *given origin knowledge* under the **same** feasible action set is

    V_new(m,L) = G(R0^2+Delta R^2,L,kappa) - G(R0^2,L,kappa). (3)

This is nonnegative. When L=0 it is zero despite arbitrarily high Delta R^2. At unlimited L, it is Delta R^2/(1+kappa).

This is not generally equal to L times the standalone R², and it is not a simple multiplicative proxy involving an unverified recourse score.

## 3. Early versus late commitment

Let L_0 be the feasible timing change for an early origin-informed decision, L_m the change feasible if commitment is deferred until checkpoint m, and J_m the nonrecoverable cost of waiting, on the same expected-loss scale. Under a **single-decision** timing model, defer iff

    G(R0^2+Delta R^2,L_m,kappa)
       - G(R0^2,L_0,kappa) > J_m.                        (4)

Better later prediction is insufficient if waiting removes earlier options or J_m is too large. A maximum of information quality is not necessarily the optimal commitment point. The model does not prove that an intermediate optimum always exists.

Illustrative cases:

- **Redundancy**: standalone checkpoint R² high, but Delta R²=0.
- **Unusable information**: Delta R²>0, but L_m=0.
- **Actionable information**: Delta R²>0 and L_m>0; wait only if the gain exceeds lost early capacity and direct delay cost.

All values in this document are synthetic or mathematical, not empirical PAYOFF-B confirmations.

## 4. Pre-specified ecological gates

**Gate 1 — environmental prediction.** For a named checkpoint and destination, compare an origin-cue-only forecast with a nested forecast that additionally includes a checkpoint cue available **before** the downstream behavioral decision. Estimate improvement in proper held-out forecast score using an untouched, year-blocked holdout. Standalone pairwise climate correlation does not meet this gate. Allow for repeated individuals, flyways, spatial pairs and years.

**Gate 2 — response capacity.** Estimate an *independent* individual-scale feasible timing-change set from movement, energy/fuel, wind, route, stopover or pre-breeding constraints. A population-duration envelope does not identify any individual's actionability.

**Gate 3 — behavior.** Pre-register the sign and endpoint of the interaction between checkpoint forecast innovation and independently measured remaining recourse. Include fixed departure calendar, photoperiod, origin cues and local seasonal conditions as competitors. Do not interpret negative stopover-duration covariance slopes as feedback gain: a fixed departure calendar can generate them mechanically.

**Gate 4 — fitness (when available).** Compare actual reproductive or survival outcomes with predicted timing consequences; better timing fit by itself is not fitness evidence.

**Fail closed:** If the checkpoint cue does not improve held-out prediction, no information-refresh claim. If prediction improves but behavior does not change under independent recourse evidence, no active-control claim. If phase correction is observed without fitness, no demographic benefit claim.

## 5. Relation to prior art

- Kölzsch et al. (2015), Journal of Animal Ecology, established spring-onset predictability along goose flyways and timing associations: https://doi.org/10.1111/1365-2656.12281
- Individually repeatable temperature cues for migration departure were shown for Asian houbara in PNAS (2021): https://pmc.ncbi.nlm.nih.gov/articles/PMC8285904/
- Informational mismatch of resident versus migrant species was previously discussed: https://doi.org/10.3389/fevo.2016.00031
- Brlík et al. (2026, Nature Ecology & Evolution, accepted), reported extensive annual-cycle timing links and partial duration compensation: https://keele-repository.worktribe.com/output/1806510/temporal-links-in-avian-migration-schedules-across-the-annual-cycle

Bayesian filtering, partial-correlation increments and bounded quadratic optimal control are prior art; this branch claims **no standalone mathematical novelty**. Its ecological purpose is to avoid treating all route predictability as *new* information or all observable phase correction as *available biological recourse*.

## 6. Validation and scope

- src/conditional_checkpoint_value.py computes exact conditional R², bounded-control Bayes gain, and commitment comparison.
- tests/test_conditional_checkpoint_value.py includes redundancy, weak-link refresh, noisy cue, zero recourse, delay-cost, effort-cost, and 50,000-sample seeded Monte Carlo checks.
- The registered V7R Q×R interaction (10 transitions; permutation p about 0.570) remains unsupported and unchanged.
- This branch is **stacked on** analysis/payoff-b-sequential-information-refresh-20261007, not a modification to any frozen manuscript, pre-registration or outcome receipt.


## 7. Sharper behavioral fingerprint: respond to surprise, not raw warmth

Define the origin-conditioned **checkpoint innovation**:

    eta_m = Z_m - (a/v_0)*Z_0.

The posterior mean destination forecast update is

    E[H|Z_0,Z_m] - E[H|Z_0] = K_m * eta_m,
    K_m = b*(1-a^2/v_0) / (v_m-a^2/v_0).

The variance identity is

    Delta R^2 = K_m^2 * Var(eta_m).

When the remaining action set is nonbinding and reversible, the change in the
optimal timing plan is proportional to K_m*eta_m/(1+kappa), **not** to raw
checkpoint warming alone.

**Same-cue, opposite-action witness.** With links (0.8, 0.9), the same
positive checkpoint anomaly Z_m=+1 gives *negative* innovation eta=-0.6 when
origin anomaly Z_0=+2, but *positive* innovation eta=+1 when Z_0=0.
With equal nonsaturating recourse, optimal conditional timing plans shift in
opposite directions. This is a synthetic testable prediction, not a report
of migratory behavior.

Prospective behavioral test: pre-specify the observed cue, its destination
forecast coefficient and **which downstream decision remains reversible**.
Regress the next action change on the residual checkpoint innovation, while
including photoperiod, wind, direct local food/weather effects, and a fixed
departure-calendar negative control. A conditional association is not by
itself causal evidence of cognitive updating.

## 8. V8 falsification context and calibration caveat

The separate preregistered PAYOFF-B V8 environmental analysis (PR #306)
showed **stronger**, not degraded, signed detrended spring-onset connectivity:
166 unique spatial pairs, 28 species, mean change in rho +0.3690 (95%
pair-bootstrap CI +0.2984 to +0.4365). But the registered environmental
connectivity gain -> bird mismatch improvement transfer was **not supported**
(beta +0.06244; 95% pair-bootstrap CI -0.01411 to +0.13635).

This is a motivation to distinguish prediction, observation, forecast
calibration and actionability, **not support for any new mechanism**.
Increasing within-window correlation need not imply better prospective
out-of-sample forecast *calibration*, especially if mean cue-target offsets
have changed. An animal may also fail to observe an available predictor.
The new design therefore must check held-out temporal transfer and
calibration, as well as checkpoint-specific incremental prediction and
independently estimated individual feasible action.

No V8 outcome is reopened or remodeled here.
