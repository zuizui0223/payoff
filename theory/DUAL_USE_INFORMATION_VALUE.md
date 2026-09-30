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

## Pairwise dual-use desynchronization

Dual-use information creates a second source of actor-specific thresholds.

Consider two actors with the **same** seasonal-action problem and the same
direct waiting cost (J<R_{A0}). Let their only difference be the magnitude
of a balanced downstream compensation problem, (G_i), with prior
compensation risk (G_i/2). The same cue accuracy (q) informs both the
seasonal action and compensation.

For actor (i),

[
oxed{
q_i
=
rac{B_A+J+G_i}{S_A+G_i}.
}
]

Therefore, for (G_2>G_1),

[
oxed{
q_2-q_1
=
rac{
(G_2-G_1)(R_{A0}-J)
}{
(S_A+G_1)(S_A+G_2)
}.
}
]

This is a finite asynchronous information-use window generated with **no
difference in raw waiting time and no difference in direct waiting cost**.
Heterogeneity in the downstream problem that must be solved after waiting is
sufficient.

The comparative static is intentionally counterintuitive:

[
rac{partial q_i}{partial G_i}
=
rac{R_{A0}-J}{(S_A+G_i)^2}
>0.
]

A larger compensation problem creates more potential compensation information
value, but at any imperfect shared cue it also leaves more residual
compensation loss. Thus actors with larger (G) require a more reliable cue
before waiting becomes worthwhile.

This does not contradict the compensation-information bonus. For a **fixed**
(G), making compensation informed weakly lowers the threshold relative to
leaving that same compensation problem uninformed. Across actors with different
(G), however, the actor facing the larger compensation burden has the higher
dual-use threshold.

This yields a new empirical distinction:

- **information-use breadth** — how many downstream decisions the cue informs;
- **downstream problem severity** — how costly those decisions are when only
  imperfectly informed.

They should not be collapsed into one axis.

### General pairwise headroom

Allow the two actors to differ in both direct waiting cost (J_i) and
compensation severity (G_i). Whenever (J_i<R_{A0}),

[
oxed{
q_i
=
1-H_i,
qquad
H_i
=
rac{R_{A0}-J_i}{S_A+G_i}.
}
]

The dimensionless quantity (H_i) is the actor's **information-waiting
headroom**: residual direct fitness room before waiting becomes impossible,
scaled by the total action-plus-compensation information problem.

When both actors have finite thresholds,

[
oxed{
Delta q
=
|H_1-H_2|.
}
]

This unifies the two sources of threshold heterogeneity. Larger (J_i)
shrinks headroom through the numerator; larger (G_i) shrinks it through the
denominator.

A useful consequence is an **iso-threshold contour**:

[
rac{R_{A0}-J_1}{S_A+G_1}
=
rac{R_{A0}-J_2}{S_A+G_2}.
]

Different direct waiting costs and different compensation problems can exactly
offset, producing identical information-use thresholds. Conversely, one actor
can have lower direct waiting cost yet a higher threshold if it faces a
sufficiently larger downstream compensation problem.

If (J_ige R_{A0}), actor (i) never waits even at perfect dual-use
information. A pair with one finite threshold and one such actor therefore has
persistent asymmetric uptake through (q=1).

## Multi-module dual-use theorem

The compensation decision need not be singular. Waiting may create several
conditional downstream decisions: travel speed, stopover duration, route
choice, post-arrival buffering, reproductive allocation, or others.

Let the focal seasonal action have prior risk \(R_{A0}\) and information value
\(V_A(q)\). Let conditional module \(j\) have prior loss \(R_{j0}\) if
uninformed and cue-conditioned information value \(V_j(q)\). Let \(J\) be the
direct nonrecoverable cost of waiting.

Then

\[
\boxed{
\text{wait}
\iff
V_A(q)+\sum_j V_j(q)
>
J+\sum_j R_{j0}.
}
\]

### Universal perfect-information condition

At perfect information,

\[
V_A(1)=R_{A0},
\qquad
V_j(1)=R_{j0}.
\]

All conditional-module terms cancel. Therefore

\[
\boxed{
\exists q\le1\text{ with waiting optimal}
\iff
R_{A0}>J.
}
\]

This result is independent of:

- how many conditional recovery decisions exist;
- how severe their uninformed losses are; or
- how those conditional losses are partitioned among modules.

Conditional information can determine **when** waiting becomes worthwhile, but
not whether perfect information can overcome the direct cost of waiting.

### Conditional-complexity penalty

A cue-informed conditional decision can lower the cost of a **given**
downstream problem relative to leaving that problem uninformed. But the
existence of the waiting-contingent problem itself cannot make waiting more
attractive than a world in which that problem does not exist.

The multi-module condition can be rearranged as

\[
V_A(q)
>
J+\sum_j R_j(q).
\]

Because every posterior conditional risk satisfies

\[
R_j(q)\ge0,
\]

the waiting margin with conditional problems is never larger than

\[
V_A(q)-J,
\]

the margin in an otherwise identical no-problem world.

Therefore

\[
\boxed{
q_{\mathrm{wait}}^{\mathrm{with\ conditional\ problems}}
\ge
q_{\mathrm{wait}}^{\mathrm{no\ conditional\ problems}}
}
\]

whenever both thresholds exist.

This resolves an apparent paradox:

- **information bonus:** for a fixed downstream problem, informing its solution
  lowers the threshold relative to leaving it uninformed;
- **conditional-complexity penalty:** adding a new problem that exists only
  because the actor waited cannot lower the threshold relative to a world
  without that problem.

Thus "the cue has more uses" is not by itself evidence that organisms should
wait for it at lower reliability.

### Multi-module rescue interval

If the conditional decisions remained uninformed, action information alone
would never pay for waiting when

\[
J+\sum_j R_{j0}\ge R_{A0}.
\]

Yet fully informed conditional decisions allow waiting whenever \(J<R_{A0}\).
Hence the exact rescue interval generalizes to

\[
\boxed{
J\in
\left[
\max\left(0,R_{A0}-\sum_j R_{j0}\right),
R_{A0}
\right).
}
\]

### Exact binary threshold

For symmetric binary modules, every information-value function has the form

\[
V_m(q)=\max[0,S_mq-B_m].
\]

The exact threshold is therefore the first root of

\[
\sum_m \max[0,S_mq-B_m]
=
J+\sum_j R_{j0},
\]

where the sum on the left includes the focal seasonal-action module and all
conditional modules.

Because the active set changes only at finitely many actionability thresholds,
the implementation solves this root exactly by scanning those breakpoints. No
numerical grid search is required.

### High-q headroom

When all modules are active at the threshold,

\[
q_{\mathrm{wait}}
=
1-
\frac{
R_{A0}-J
}{
S_A+\sum_j S_j
}.
\]

Thus

\[
\boxed{
H
=
\frac{
R_{A0}-J
}{
S_A+\sum_j S_j
}
}
\]

is the multi-module information-waiting headroom in the all-active regime.

Adding conditional decision complexity increases the total information slope in
the denominator. This can push the reliability threshold closer to one even
though the same cue is useful for more downstream choices.

This distinction prevents a misleading intuition: **more uses of information
do not necessarily imply earlier information use** when those uses correspond
to additional problems created by waiting.


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
sources of uncertainty (Samson et al. 1989), and stopping problems in which an
actor chooses between irreversible action and waiting for more accurate
information (Bhattacharjya & Deleris 2014; Lehrer & Wang 2024). Importantly, Samson et al. show that
information values across multiple uncertainties are generally **non-additive**.
The additive decomposition used here is therefore not a generic property of
value of information: it follows from the explicitly declared additive
declared additive separability of the seasonal-action and compensation loss modules. Ecology
likewise has an established value-of-information literature in evolutionary
fitness and adaptive management (Donaldson-Matasci et al. 2010; Williams et al.
2011; Canessa et al. 2015).

Nor is the migration biology new in isolation. Stopover sites have explicitly
been proposed as information sources that can improve arrival timing (Winkler
et al. 2014); route predictability can change optimal migration progression
(Bauer et al. 2020); and migrants can compensate en route for phenological
error by changing speed and stopover use (Ortega et al. 2023).

PAYOFF-B therefore does **not** claim novelty for:

- information having value for more than one downstream choice;
- sequential value of information;
- threshold policies for waiting versus irreversible action under uncertainty;
- stopover information;
- behavioral compensation during migration; or
- generic value-of-information additivity; the present sum is licensed only
  by the declared additive separability of the loss structure.

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
logic under a special separable ecology, rather than a new general theory of
information value. The novelty claim should therefore be attached to the
**information-deadline geometry and its ecological interpretation**, not to
value-of-information theory itself.

References for this boundary:

- Miller AC (1975) The Value of Sequential Information. *Management Science*
  22:1–11. DOI: 10.1287/mnsc.22.1.1.
- Samson D, Wirth A, Rickard J (1989) The value of information from multiple
  sources of uncertainty in decision analysis. *European Journal of
  Operational Research* 39:254–260. DOI: 10.1016/0377-2217(89)90163-X.
- Bhattacharjya D, Deleris LA (2014) The Value of Information in Some
  Variations of the Stopping Problem. *Decision Analysis* 11:189–203.
  DOI: 10.1287/deca.2014.0298.
- Lehrer E, Wang T (2024) The value of information in stopping problems.
  *Economic Theory* 78:619–648. DOI: 10.1007/s00199-023-01543-8.
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
