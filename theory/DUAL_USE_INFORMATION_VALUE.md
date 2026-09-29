# PAYOFF-B dual-use information theorem

Date: **2026-09-29**  
Status: **exact additive binary extension; prospective natural test**

## Problem

The fixed-deadline theorem assumes that the focal later cue changes the
seasonal action but does not itself alter the cost of waiting.

That assumption can fail. The same later information may also reveal how to
compensate for having waited: whether to migrate faster, skip a stopover,
change route, shorten a pre-breeding interval or choose another recovery
strategy.

Then the effective waiting cost is cue-dependent. It is no longer valid to
insert one fixed \(D_{\mathrm{eff}}\) into the original closed form without
qualification.

## Additive dual-use decision

Let the actor face two downstream decisions after waiting.

### Seasonal action

Before the cue, the minimum expected seasonal mismatch loss is

\[
R_{A0}.
\]

After observing a cue of reliability \(q\), the expected Bayes risk is

\[
R_A(q),
\]

so the seasonal-action information value is

\[
V_A(q)=R_{A0}-R_A(q).
\]

### Compensation decision

Conditional on having waited, suppose an uninformed compensation choice would
have prior expected loss

\[
R_{C0}.
\]

The same cue can reduce that compensation loss to

\[
R_C(q),
\]

giving compensation information value

\[
V_C(q)=R_{C0}-R_C(q)\ge0.
\]

Let \(J\) be the direct nonrecoverable cost of waiting.

Immediate commitment has expected loss \(R_{A0}\). Waiting has expected loss

\[
R_A(q)+J+R_C(q).
\]

Therefore

\[
\boxed{
\text{wait}
\iff
V_A(q)>J+R_C(q)
}
\]

or equivalently

\[
\boxed{
\text{wait}
\iff
V_A(q)+V_C(q)>J+R_{C0}.
}
\]

This is the **dual-use information theorem**.

The same cue has two values, but they enter asymmetrically: seasonal
information creates the reason to wait, while compensation information reduces
the cost created by waiting.

## Corollary 1 — compensation information cannot justify waiting by itself

Because

\[
V_C(q)\le R_{C0},
\]

if the cue has no seasonal-action value,

\[
V_A(q)=0,
\]

then

\[
V_A(q)+V_C(q)
\le
R_{C0}
\le
J+R_{C0}.
\]

Hence compensation information alone cannot make waiting strictly optimal.

The actor cannot rationally create a delay solely to learn how to repair that
self-created delay.

A dual-use cue can make waiting easier, but only when the cue also has positive
value for the focal seasonal action.

## Corollary 2 — direct waiting cost remains irreducible

At perfect information,

\[
V_A(1)=R_{A0},
\qquad
V_C(1)=R_{C0}.
\]

Thus a perfect dual-use cue is worth waiting for iff

\[
R_{A0}>J.
\]

The uninformed compensation burden \(R_{C0}\) cancels. Perfect compensation
information can remove avoidable compensation loss, but it cannot remove the
direct cost of waiting.

Therefore no amount of compensation information can rescue waiting when

\[
J\ge R_{A0}.
\]

## Corollary 3 — compensation information can rescue an otherwise impossible wait

Action information alone, evaluated against the uninformed compensation
burden, can never justify waiting when

\[
J+R_{C0}\ge R_{A0}.
\]

Yet a perfect dual-use cue permits waiting whenever

\[
J<R_{A0}.
\]

Therefore the exact direct-cost rescue interval is

\[
\boxed{
J\in
\left[
\max(0,R_{A0}-R_{C0}),
R_{A0}
\right).
}
\]

Inside this interval, action information alone never pays for waiting, but the
same cue becomes worth waiting for because it also identifies a better
compensation response.

This is not circular. Seasonal-action value remains necessary; compensation
information only removes an otherwise prohibitive component of the waiting
burden.

## Symmetric binary closed form

For each module \(m\in\{A,C\}\), define

\[
A_m=(1-\pi_m)C_{F,m},
\qquad
L_m=\pi_m C_{M,m},
\]

\[
S_m=A_m+L_m,
\qquad
B_m=\max(A_m,L_m),
\qquad
R_{m0}=\min(A_m,L_m).
\]

Under a symmetric binary cue of accuracy \(q\),

\[
V_m(q)
=
\max[0,S_m q-B_m].
\]

The dual-use threshold is the first solution of

\[
\max[0,S_Aq-B_A]
+
\max[0,S_Cq-B_C]
=
J+R_{C0}.
\]

This function is continuous and piecewise linear, with kinks at

\[
q_{0,A}=B_A/S_A,
\qquad
q_{0,C}=B_C/S_C.
\]

The implementation solves each admissible active-set segment exactly; no grid
search is used.

## Canonical rescue witness

Use the original action module

\[
\pi_A=0.4,\quad C_{F,A}=2,\quad C_{M,A}=1.
\]

Then

\[
R_{A0}=0.4,
\qquad
q_{0,A}=0.75.
\]

For the compensation module use

\[
\pi_C=0.5,\quad C_{F,C}=C_{M,C}=1,
\]

so

\[
R_{C0}=0.5,
\qquad
q_{0,C}=0.5.
\]

Let direct waiting cost be

\[
J=0.10.
\]

If the cue informed only the seasonal action, waiting would carry burden

\[
J+R_{C0}=0.60>R_{A0}=0.40,
\]

so even perfect action information would not justify waiting.

With dual-use information, for \(q>0.75\),

\[
V_A(q)=1.6q-1.2,
\qquad
V_C(q)=q-0.5.
\]

The threshold solves

\[
(1.6q-1.2)+(q-0.5)=0.60,
\]

giving

\[
\boxed{
q_{\mathrm{wait}}^{dual}
=
\frac{2.3}{2.6}
\approx0.8846.
}
\]

The same cue therefore converts a system in which waiting is impossible under
action-only accounting into one with a finite information-use threshold.

## Relationship to effective deadline cost

The theorem can also be written

\[
V_A(q)>D_{\mathrm{eff}}(q),
\]

where

\[
D_{\mathrm{eff}}(q)
=
J+R_C(q).
\]

This is the key distinction from the fixed-\(D_{\mathrm{eff}}\) theorem:
when the focal cue also informs compensation, the effective deadline cost
declines with cue quality.

The original closed form

\[
q_{\mathrm{wait}}
=
\frac{\max(A,L)+D_{\mathrm{eff}}}{A+L}
\]

remains exact only when \(D_{\mathrm{eff}}\) is fixed with respect to the focal
cue, or when a cue-independent effective cost has already been identified.

Otherwise \(q_{\mathrm{wait}}\) is an implicit or piecewise solution of

\[
V_A(q)=D_{\mathrm{eff}}(q).
\]

## Ecological predictions

The extension yields four direct predictions.

1. **Compensation-information bonus.** Systems in which a late cue also predicts
   the best recovery action should begin using that cue at lower reliability
   than otherwise identical systems in which compensation remains uninformed.
2. **No pure self-rescue.** Compensation information cannot induce waiting
   below the seasonal-action actionability boundary.
3. **Irreducible direct cost.** High direct waiting cost \(J\) prevents waiting
   even under perfect dual-use information.
4. **Cue-dependent deadline cost.** Empirical models must not treat
   \(D_{\mathrm{eff}}\) as exogenous to \(q\) if the focal cue also informs
   downstream compensation.

## Greater snow goose relevance

Greater snow goose motivates, but does not test, this extension.

The route system contains multiple possible compensation decisions after
departure, and later Arctic information may potentially affect the value of
those responses. Existing studies do not identify whether the same focal cue
used for seasonal timing also changes the downstream compensation policy.

A direct natural test must therefore distinguish:

- **cue-independent compensation**, where fixed \(D_{\mathrm{eff}}\) is valid;
- **cue-informed compensation**, where the dual-use threshold is required.

No current greater-snow-goose result is promoted to a dual-use information
test.

## Relation to prior information theory and migration ecology

The generic **value of information** is not new. Decision analysis has long
treated information as valuable when it changes downstream decisions, including
sequential information acquisition (Miller 1975), information about multiple
sources of uncertainty (Samson et al. 1989), and information used across
multiple decision problems. Ecology likewise has an established value-of-
information literature in evolutionary fitness and adaptive management
(Donaldson-Matasci et al. 2010; Williams et al. 2011; Canessa et al. 2015).

Nor is the migration biology new in isolation. Stopover sites have explicitly
been proposed as information sources that can improve arrival timing (Winkler
et al. 2014); route predictability can change optimal migration progression
(Bauer et al. 2020); and migrants can compensate en route for phenological
error by changing speed and stopover use (Ortega et al. 2023).

PAYOFF-B therefore does **not** claim novelty for:

- information having value for more than one downstream choice;
- sequential value of information;
- stopover information;
- behavioral compensation during migration; or
- generic additivity of expected losses under risk neutrality.

The candidate contribution is narrower: embed a downstream compensation
decision **inside the cost of waiting for the focal seasonal cue**, then solve
the resulting information deadline exactly. In that construction:

1. compensation uncertainty is incurred only conditional on waiting;
2. the focal cue can lower its own effective deadline cost as cue quality rises;
3. compensation information alone cannot rationally justify creating the delay
   it would help repair;
4. direct waiting cost remains irreducible even under perfect dual-use
   information;
5. an exact interval exists where action information alone yields never-wait
   but dual-use information yields a finite reliability threshold.

These are deadline-specific consequences of ordinary value-of-information
logic, rather than a new general theory of information value.

References for this boundary:

- Miller AC (1975) The Value of Sequential Information. *Management Science*
  22:1–11. DOI: 10.1287/mnsc.22.1.1.
- Samson D, Wirth A, Rickard J (1989) The value of information from multiple
  sources of uncertainty in decision analysis. *European Journal of
  Operational Research* 39:254–260. DOI: 10.1016/0377-2217(89)90163-X.
- Donaldson-Matasci MC, Bergstrom CT, Lachmann M (2010) The fitness value of
  information. *Oikos* 119:219–230. DOI:
  10.1111/j.1600-0706.2009.17781.x.
- Williams BK, Eaton MJ, Breininger DR (2011) Adaptive resource management and
  the value of information. *Ecological Modelling* 222:3429–3436. DOI:
  10.1016/j.ecolmodel.2011.07.003.
- Canessa S et al. (2015) When do we need more data? A primer on calculating
  the value of information for applied ecologists. *Methods in Ecology and
  Evolution* 6:1219–1228. DOI: 10.1111/2041-210X.12423.
- Winkler DW et al. (2014) Cues, strategies, and outcomes: how migrating
  vertebrates track environmental change. *Movement Ecology* 2:10.
  DOI: 10.1186/2051-3933-2-10.
- Bauer S, McNamara JM, Barta Z (2020) Environmental variability, reliability
  of information and the timing of migration. *Proceedings of the Royal
  Society B* 287:20200622. DOI: 10.1098/rspb.2020.0622.
- Ortega AC et al. (2023) Migrating mule deer compensate en route for
  phenological mismatches. *Nature Communications* 14:2008.
  DOI: 10.1038/s41467-023-37750-z.

## Claim boundary

The theorem is exact for two additive symmetric binary decision modules sharing
a cue-accuracy coordinate. It is not an empirical reinterpretation of the
existing bird datasets.

The broader finite-state statement follows from ordinary value-of-information
logic under additive separability, but the closed form above is licensed only
for the declared binary model.
