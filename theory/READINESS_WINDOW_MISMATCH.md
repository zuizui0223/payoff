# PAYOFF-B asynchronous-readiness window theorem

Date: **2026-10-03**  
Status: **prospective post-freeze exact special case; frozen GEB V2 unchanged**

## 1. Question

The two-clock architecture separates a developmental/physiological readiness
clock from an information-dependent decision controller.

Can differences in the readiness clock alone create a temporary interaction
mismatch if the two actors otherwise have the same controller? Yes.

## 2. Step-gate model

Let two actors begin with the same seasonal error

\[
e_1(0)=e_2(0)=e_0.
\]

Actor \(i\)'s readiness gate opens at \(\tau_i\):

\[
G_i(t)=\mathbf 1[t\ge\tau_i].
\]

Once ready, both actors correct at the same rate \(c\):

\[
\frac{de_i}{dt}=-cG_i(t)e_i(t).
\]

Therefore

\[
e_i(t)=
\begin{cases}
e_0,&t<\tau_i,\\
e_0e^{-c(t-\tau_i)},&t\ge\tau_i.
\end{cases}
\]

## 3. Readiness window

Assume \(\tau_1\le\tau_2\). The interval

\[
\boxed{\tau_1\le t<\tau_2}
\]

is a **readiness window**: actor 1 can already correct while actor 2 cannot.

During the window,

\[
\Delta(t)
=
e_0[e^{-c(t-\tau_1)}-1].
\]

Mismatch grows in magnitude until actor 2 becomes ready.

## 4. Exact maximum mismatch

At \(t=\tau_2\),

\[
\boxed{
|\Delta_{\max}|
=
|e_0|\,[1-e^{-c\Delta\tau}],
}
\]

where

\[
\Delta\tau=\tau_2-\tau_1.
\]

After \(\tau_2\), both actors correct at the same rate and mismatch magnitude
decays. This is therefore the global maximum caused by readiness asynchrony.

## 5. Consequences

If \(\Delta\tau=0\), no mismatch is created.

If \(c=0\), no mismatch is created even if readiness differs.

Thus readiness asynchrony matters only because a functioning controller begins
acting at different times.

As \(\Delta\tau\to\infty\),

\[
|\Delta_{\max}|\to|e_0|.
\]

The effect is positive but saturating:

\[
\frac{\partial|\Delta_{\max}|}{\partial\Delta\tau}
=
|e_0|c\,e^{-c\Delta\tau}.
\]

Small differences in readiness time are most consequential when post-readiness
correction is fast.

## 6. Biological interpretation

A developmental clock controls **when correction becomes possible**.

A decision controller controls **how rapidly error is corrected once it is
possible**.

Two species can therefore have identical information and identical decision
rules yet desynchronize because one becomes ready earlier.

This provides a continuous-time counterpart to PAYOFF-B's earlier asynchronous
information-use window.

## 7. Four clock-information states

Readiness \(G(t)\) and information quality are distinct. Along a seasonal route
an actor can be:

1. not ready and poorly informed;
2. not ready but well informed;
3. ready but poorly informed;
4. ready and well informed.

Only the fourth supports high-quality signed correction.

The ordering of information recovery and physiological readiness is therefore
itself an ecological trait.

## 8. Empirical prediction

A direct test requires readiness time and post-readiness correction to be
measured separately.

The theory predicts that pairwise mismatch should peak near the later
readiness time and scale as

\[
|e_0|\,[1-e^{-c|\tau_2-\tau_1|}].
\]

This is not identifiable from final phenology alone.

## 9. Novelty boundary

Threshold timing and exponential relaxation are standard dynamical systems.

PAYOFF-B's ecological synthesis is:

> **different readiness times can create a finite mismatch window even when
> interacting actors share the same environmental information and the same
> post-readiness controller.**

Direct natural validation remains prospective.
