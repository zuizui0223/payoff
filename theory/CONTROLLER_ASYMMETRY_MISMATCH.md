# PAYOFF-B prospective controller-asymmetry mismatch theorem

Date: **2026-10-03**  
Status: **prospective post-freeze Paper-2 extension; frozen GEB V2 unchanged**

## 1. Missing bridge

The post-freeze Paper-2 controller explains how one organism estimates and
corrects signed seasonal phase error.  The ecological paper ultimately concerns
**interactions**, so one more bridge is required:

> How does heterogeneity in actor-level information and phase control generate
> mismatch between interacting species exposed to the same seasonal forcing?

The answer is exact in the declared linear mean controller.

## 2. Actor-level effective mean retention

Under the two-clock architecture, actor \(i\) has regression-scale phase
retention

\[
\lambda_i
=
\phi_i(1-G_i g_iK_i),
\]

where

- \(\phi_i\) = passive phase carry-over;
- \(G_i\) = physiological/developmental readiness gate;
- \(K_i\) = effective checkpoint-information weight;
- \(g_i\) = feedback gain.

The previous decision-only controller is the special case \(G_i=1\).

The route-level mean phase state is

\[
e_{i,t+1}
=
\lambda_i e_{i,t}
+
w_{i,t}.
\]

## 3. Common and differential modes

For two interacting actors define

\[
m_t
=
\frac{e_{1,t}+e_{2,t}}{2}
\]

and

\[
\Delta_t
=
e_{1,t}-e_{2,t}.
\]

Let

\[
\bar\lambda
=
\frac{\lambda_1+\lambda_2}{2},
\qquad
\delta\lambda
=
\lambda_1-\lambda_2,
\]

with analogous mean and difference innovations
\(\bar w_t\) and \(\delta w_t\).

Then exactly

\[
\boxed{
m_{t+1}
=
\bar\lambda m_t
+
\frac{\delta\lambda}{4}\Delta_t
+
\bar w_t
}
\]

and

\[
\boxed{
\Delta_{t+1}
=
\delta\lambda\,m_t
+
\bar\lambda\Delta_t
+
\delta w_t.
}
\]

This is the key ecological bridge.

The common seasonal-error mode and the interaction-mismatch mode are coupled
whenever the actors have different controllers.

## 4. Controller-asymmetry mismatch theorem

Suppose the pair is currently synchronized,

\[
\Delta_t=0,
\]

and experiences no actor-specific innovation,

\[
\delta w_t=0.
\]

If both actors nevertheless share a nonzero seasonal error \(m_t\), then

\[
\boxed{
\Delta_{t+1}
=
(\lambda_1-\lambda_2)m_t.
}
\]

Therefore:

> **A shared seasonal error is converted into interaction mismatch whenever
> interacting actors retain or correct that error differently.**

No difference in external climate exposure is required.

No initial interaction mismatch is required.

This is stronger and more mechanistic than saying that species have different
temperature sensitivities.

## 5. Readiness asymmetry alone is sufficient

If passive retention, information and feedback gain are the same but the
physiological/readiness gates differ,

\[
\phi_1=\phi_2=\phi,
\qquad
K_1=K_2=K,
\qquad
g_1=g_2=g,
\]

then

\[
\boxed{
\Delta_{t+1}
=
-\phi gK(G_1-G_2)m_t.
}
\]

Thus a developmental-clock difference can generate mismatch even when the two
actors would make identical information-dependent decisions once both are
ready.

## 6. Information asymmetry alone is sufficient

If passive retention, readiness and control gain are the same but information
weights differ,

\[
\phi_1=\phi_2=\phi,
\qquad
G_1=G_2=G,
\qquad
g_1=g_2=g,
\]

then

\[
\boxed{
\Delta_{t+1}
=
-\phi Gg(K_1-K_2)m_t.
}
\]

Different information about the same seasonal future can therefore generate
mismatch even when the actors have identical physiological readiness and
physical correction gain.

## 7. Control asymmetry alone is sufficient

If passive retention, readiness and information weight are the same,

\[
\phi_1=\phi_2=\phi,
\qquad
G_1=G_2=G,
\qquad
K_1=K_2=K,
\]

then

\[
\boxed{
\Delta_{t+1}
=
-\phi GK(g_1-g_2)m_t.
}
\]

Thus two species can become asynchronous even after receiving equally useful
information at the same readiness state because they differ in how strongly
they translate estimated phase error into correction.

## 8. Persistent mismatch under constant shared forcing

Now let both actors experience the same constant seasonal forcing \(w\):

\[
e_{i,t+1}
=
\lambda_i e_{i,t}+w.
\]

For stable controllers,

\[
|\lambda_i|<1,
\]

the stationary errors are

\[
e_i^*
=
\frac{w}{1-\lambda_i}.
\]

Therefore the stationary interaction mismatch is

\[
\boxed{
\Delta^*
=
w
\frac{\lambda_1-\lambda_2}
{(1-\lambda_1)(1-\lambda_2)}.
}
\]

A constant climate-driven displacement can therefore sustain a persistent
interaction mismatch even though the environmental forcing itself is shared.

The denominator shows an amplification effect: controller differences become
especially consequential as either actor approaches weak restoring control
\(\lambda\to1\).

## 9. Relation to the information-actionability theorem

The actionability theorem predicts that actors can optimally act on the same
improving environmental information at different stages because their remaining
actionability decays at different rates.

The controller-asymmetry theorem describes the next step:

\[
\text{different information-use stage}
\rightarrow
\text{different effective } K,g,\lambda
\rightarrow
\text{shared error converted into } \Delta.
\]

This closes the mechanistic chain from information timing to interaction
mismatch.

## 10. Relation to coordination games

The controller theorem explains how mismatch is **generated**.

The earlier Paper-2 coordination game explains why a mismatched or obsolete
timing configuration may be difficult to **escape** even after information
improves.

The two mechanisms are therefore sequential rather than competing:

1. asymmetric information/control generates differential phase;
2. interaction payoffs can stabilize or retain that differential state.

## 11. Natural interpretation

The existing PAYOFF-B evidence already supplies separate empirical pieces:

- broad migratory birds: predictive connectivity versus realized mismatch;
- mule deer: strong signed phase correction and a whole-route variance funnel;
- resident–migrant systems: different thermal responses widen relative timing;
- wigeon: predictive connectivity is not a universal amplifier of downstream
  correction.

None of these data currently identify \(\lambda_1\) and \(\lambda_2\) for a
single interacting pair together with independent \(K_i,g_i,\phi_i\).

The direct pairwise controller test therefore remains prospective.

## 12. Falsifiable pairwise prediction

For an interacting pair observed before and after a shared seasonal anomaly,
estimate actor-specific incoming phase retention on the same time scale.

The reduced theory predicts

\[
\Delta_{t+1}
-
\bar\lambda\Delta_t
-
\delta w_t
=
\delta\lambda\,m_t.
\]

A strong test would ask whether the observed increase or decrease in pairwise
mismatch is predicted by the **difference in actor-level controller retention**
rather than only by taxon identity or raw temperature sensitivity.

## 13. Novelty boundary

The common/differential-mode algebra is standard linear-systems mathematics.

PAYOFF-B should claim the ecological synthesis:

> seasonal interaction mismatch can be generated by differences in how
> interacting organisms convert information into phase correction, even under
> the same environmental forcing.

The exact natural parameterization of that bridge remains prospective.
