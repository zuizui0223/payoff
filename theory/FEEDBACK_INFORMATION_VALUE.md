# PAYOFF-B feedback-information extension

Date: **2026-10-08**  
Status: **POST-V7R PROSPECTIVE THEORY; no q_B outcome opened**

## 1. Why a second information coordinate is required

V7R rejected the simple route

\[
q_F\times r
\rightarrow
\text{stronger reactive correction},
\]

where \(q_F\) was historical cross-site spring predictability.

The direct stopover actuator was also strong on some transitions with
approximately zero \(q_F\).

This motivates, but does not confirm, a distinction between:

\[
q_F
=
\text{forecast/feedforward information about a future site},
\]

and

\[
q_B
=
\text{feedback/state-estimation information about current mismatch}.
\]

The present note derives the second channel prospectively.

## 2. Current phase state and local cue

Let current signed phase error be

\[
e\sim N(0,P).
\]

A local environmental observation is

\[
z=e+\nu,
\qquad
\nu\sim N(0,R_B).
\]

Here \(R_B\) is feedback-cue noise. Smaller \(R_B\) means more informative
local state estimation.

The posterior mean and variance are

\[
\hat e
=
\frac{P}{P+R_B}z,
\]

\[
P^+
=
\frac{PR_B}{P+R_B}.
\]

Across repeated realizations,

\[
\operatorname{Var}(\hat e)
=
\frac{P^2}{P+R_B}.
\]

Thus better local information increases the variance of the *inferred*
correctable state while decreasing posterior uncertainty.

## 3. Costly reactive correction

Let action \(u\) incur cost

\[
\kappa u^2
\]

and residual mismatch incur

\[
\mu(e-u)^2,
\]

with \(\kappa,\mu>0\).

Conditional on the cue, the unbounded optimum is

\[
u^*
=
g\hat e,
\]

where

\[
g
=
\frac{\mu}{\kappa+\mu}.
\]

Cue reliability does not change the certainty-equivalent gain \(g\); it changes
how accurately the state driving that gain is estimated.

## 4. Exact value of feedback information

Without the cue, the zero-mean prior implies optimal action \(u=0\), with
expected loss

\[
L_0=\mu P.
\]

With the cue and optimal correction,

\[
E[L_B]
=
\mu P^+
+
\frac{\kappa\mu}{\kappa+\mu}
\operatorname{Var}(\hat e).
\]

Therefore the exact value of the local feedback cue is

\[
\boxed{
V_B(P,R_B)
=
\frac{\mu^2P^2}
{(\kappa+\mu)(P+R_B)}
}.
\]

Consequences:

\[
\frac{\partial V_B}{\partial R_B}<0,
\]

so noisier local state information is less valuable, and

\[
\frac{\partial V_B}{\partial P}>0,
\]

so feedback information becomes more valuable when more mismatch risk reaches
the correction stage.

## 5. Exact forecast-feedback substitution

Suppose better feedforward information \(q_F\) lowers pre-correction mismatch
variance:

\[
P=P(q_F),
\qquad
P'(q_F)<0.
\]

Then

\[
\frac{dV_B}{dq_F}
=
\frac{\partial V_B}{\partial P}P'(q_F)
<0.
\]

Thus, in this declared model:

\[
\boxed{
\text{better forecast information can reduce the value of local feedback information}.
}
\]

This is the uncertainty-aware counterpart of the existing
prediction-correction substitution theorem.

It does not imply that \(q_F\) and \(q_B\) themselves are negatively
correlated. They are distinct properties.

## 6. Finite actionability

Let feasible correction be bounded:

\[
|u|\le a.
\]

Then the implemented action is

\[
u_a^*
=
\operatorname{clip}(g\hat e,-a,a).
\]

As \(a\to0\), even perfect local state information cannot generate a large
behavioral response.

Therefore the behavioral expression of \(q_B\) depends on remaining
actionability.

This motivates an empirical interaction between independent local
state-information quality and independent recourse.

## 7. Environmental proxy for q_B

The empirical proxy is not derived from goose behavior.

Let local vegetation observation at region \(j\) be

\[
Y_{jyt}=f_j(\tau_{jyt})+\varepsilon_{jyt},
\]

where

\[
\tau_{jyt}
=
\text{DOY}_{t}-S_{jy}
\]

is phase relative to independently reconstructed local spring onset.

Near \(\tau=0\), approximate

\[
Y_{jyt}
=
a_{jy}+b_j\tau_{jyt}+\varepsilon_{jyt}.
\]

Then local phase-resolution variance is approximately

\[
\sigma_{\tau,j}^2
=
\frac{\sigma_j^2}{b_j^2},
\]

and local Fisher-style phase information is

\[
\boxed{
J_{B,j}
=
\frac{b_j^2}{\sigma_j^2}.
}
\]

Higher \(J_B\) means the same vegetation observation carries more information
about current local seasonal phase.

The primary empirical coordinate will use

\[
Q_{B,j}
=
z\{\log(J_{B,j})\}
\]

across the frozen origin-region panel.

The z transform is affine after taking log information; it changes scale, not
the ordering of the predeclared local information coordinate.

## 8. Claim boundary

This note licenses the prospective prediction:

> A more observable local seasonal state should allow incoming phase error to
> produce a stronger signed correction when downstream actionability remains.

It does not license:

- that geese directly perceive satellite NDVI;
- that \(J_B\) equals internal sensory precision;
- that V7R null confirms forecast-feedback substitution;
- that local vegetation is the only feedback cue;
- that the unbounded LQ solution applies literally to migration.
