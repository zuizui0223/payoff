# PAYOFF-B serial two-clock decomposition

Date: **2026-10-03**  
Status: **post-hoc post-freeze theoretical refinement; frozen GEB V2 unchanged**

## 1. Why serial clocks are different from concurrent gates

The explicit two-clock model originally allowed physiological readiness \(G\)
to multiply the downstream feedback controller at every stage.  That is a valid
general architecture when readiness is measured at the same decision stage.

A biologically important special case is simpler:

1. a developmental/physiological clock determines **when the organism enters**
   the focal behavioral mode;
2. once entry has occurred, an information-dependent controller determines
   **how phase error is corrected thereafter**.

For migration this means:

\[
\text{readiness clock}
\rightarrow
\text{migration onset}
\rightarrow
\text{route-wise decision controller}.
\]

The "Mikawa-Anjo clock" belongs to the third term, not to the readiness clock.

This serial architecture is formulated after the mule-deer IFBFat moderation
proxy result was known.  The natural result therefore motivates but does not
confirm the theory.

## 2. Clock 1 sets the entry state

Let physiological state be \(z_i(t)\) and let migration or another focal event
become available when

\[
z_i(t)\ge\Theta_i.
\]

Define entry time

\[
\tau_i
=
\inf\{t:z_i(t)\ge\Theta_i\}.
\]

The ecological phase error when the actor enters the behavioral mode is

\[
e_{i,0}.
\]

For a pair define

\[
m_0
=
\frac{e_{1,0}+e_{2,0}}{2}
\]

and

\[
\Delta_0
=
e_{1,0}-e_{2,0}.
\]

The readiness clock is therefore allowed to create an **initial interaction
mismatch** \(\Delta_0\) before any route-wise feedback occurs.

## 3. Clock 2 propagates and corrects phase after entry

After entry, the reduced controller is

\[
e_{i,k+1}
=
\lambda_i e_{i,k}
\]

in the no-innovation witness.

The post-entry retention can be written

\[
\lambda_i
=
\phi_i(1-O_i g_iK_i),
\]

where \(O_i\) is remaining ecological opportunity, \(K_i\) is phase-information
weight and \(g_i\) is decision gain.

Readiness \(G_i\) is no longer multiplied into this downstream coefficient by
default because the actor has already crossed the readiness gate.

A concurrent physiological gate remains an optional extension when independently
measured at the same decision stage.

## 4. Exact serial two-clock theorem

The initial actor errors are

\[
e_{1,0}=m_0+\frac{\Delta_0}{2},
\qquad
e_{2,0}=m_0-\frac{\Delta_0}{2}.
\]

After \(n\) checkpoints,

\[
e_{1,n}
=
\lambda_1^n
\left(
m_0+\frac{\Delta_0}{2}
\right)
\]

and

\[
e_{2,n}
=
\lambda_2^n
\left(
m_0-\frac{\Delta_0}{2}
\right).
\]

Therefore

\[
\boxed{
\Delta_n
=
(\lambda_1^n-\lambda_2^n)m_0
+
\frac{\lambda_1^n+\lambda_2^n}{2}\Delta_0.
}
\]

This separates later interaction mismatch into two exact components.

### Controller-generated mismatch

\[
\boxed{
C_n
=
(\lambda_1^n-\lambda_2^n)m_0.
}
\]

This term exists even if the readiness clocks produced synchronized entry
\(\Delta_0=0\).

### Timer-propagated mismatch

\[
\boxed{
T_n
=
\frac{\lambda_1^n+\lambda_2^n}{2}\Delta_0.
}
\]

This term carries forward mismatch that already existed at entry.

Thus

\[
\boxed{
\Delta_n=C_n+T_n.
}
\]

## 5. Two limiting cases are diagnostic

### Same decision controller

If

\[
\lambda_1=\lambda_2=\lambda,
\]

then

\[
\boxed{
\Delta_n
=
\lambda^n\Delta_0.
}
\]

Downstream feedback cannot create new between-actor mismatch from shared error;
it only propagates or erases the mismatch inherited from the readiness clocks.

For

\[
|\lambda|<1,
\]

the initial readiness-generated mismatch decays.

### Same entry phase

If

\[
\Delta_0=0,
\]

then

\[
\boxed{
\Delta_n
=
(\lambda_1^n-\lambda_2^n)m_0.
}
\]

The physiological clocks can be perfectly synchronized and interaction mismatch
still emerges because the decision controllers differ.

## 6. Timer precision and downstream feedback are partially substitutable

For one actor with no new process innovation,

\[
e_n=\lambda^n e_0.
\]

Therefore entry-phase variance satisfies

\[
\boxed{
V_n
=
\lambda^{2n}V_0.
}
\]

For a target final variance \(V^*\),

\[
\boxed{
V_0
=
\frac{V^*}{\lambda^{2n}}.
}
\]

A stronger downstream controller (smaller \(|\lambda|\)) can therefore tolerate
a less precise entry timer while achieving the same final tracking precision.

This gives an exact serial-clock version of prediction–correction substitution:

> **precision before entry and correction after entry are partly substitutable
> routes to the same final seasonal alignment.**

The result does not imply that the two mechanisms have equal fitness costs.
Timer plasticity, energetic costs of correction and process innovation can
break the simple equivalence.

It does imply that observing only final arrival or event synchrony can hide
very different biological strategies.

## 7. Biological meaning

The two clocks have different jobs:

\[
\boxed{
\text{readiness clock}
\Rightarrow
\text{where the trajectory starts}
}
\]

and

\[
\boxed{
\text{decision clock}
\Rightarrow
\text{what happens to that error afterward}.
}
\]

This is stronger than calling both mechanisms "phenological sensitivity."

A bee emergence clock, plant flowering threshold or migratory readiness
programme can primarily determine entry timing.

A route-wise migrant controller can subsequently accelerate, wait, change
stopover duration or otherwise alter the retained phase error.

## 8. Mule-deer interpretation

The current mule-deer results are consistent with this serial decomposition:

- March IFBFat is associated with migration-start timing in the conservative
  readiness subset;
- signed start phase predicts post-departure speed and stopover;
- IFBFat main effects on downstream actuators are weak in the channel audit;
- the prespecified DFP × IFBFat moderation proxy does not support stronger
  feedback at higher IFBFat.

These observations are **not** a confirmatory test of the serial theorem,
because the serial architecture was articulated after the moderation result was
known.

Their licensed role is narrower: they show why an entry-clock interpretation
is plausible and why readiness need not be assumed to multiply every
post-entry feedback decision.

## 9. Relation to H1 and H2

Under the evidence grades:

- **H1 serial hybrid**: readiness/timer evidence and downstream decision-control
  evidence coexist in the same system;
- **H2 concurrent gating**: readiness measured at the decision stage directly
  modifies the signed phase-to-action response.

Mule deer currently support an H1 candidate.

The IFBFat moderation proxy does not support H2, but it cannot rule out a
different stage-specific readiness variable.

## 10. Direct empirical prediction

A clean serial test needs:

1. pre-entry physiological readiness;
2. entry phase \(e_0\);
3. repeated post-entry phase and actions;
4. actor-specific downstream retention \(\lambda\).

The theory predicts that later mismatch can be partitioned into:

\[
\text{entry-clock contribution}
+
\text{controller contribution}.
\]

For interacting species this suggests estimating both the phase difference at
entry and the downstream retention of each partner rather than treating one
phenological slope as the whole mechanism.

## 11. Novelty boundary

Hybrid systems, switching dynamics and feedback control are established
mathematical ideas.

The PAYOFF-B contribution is the ecological decomposition:

> **physiological clocks set the initial seasonal state, whereas decision
> controllers determine whether that initial error is erased, retained or
> converted into new interaction mismatch.**

The exact natural decomposition remains prospective.
