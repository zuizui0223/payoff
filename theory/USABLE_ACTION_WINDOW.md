# PAYOFF-B usable-action-window theorem

Date: **2026-10-03**  
Status: **prospective post-freeze exact witness; frozen GEB V2 unchanged**

## 1. Opening and closing are different processes

The two-clock architecture requires a distinction between:

\[
G(t)=\text{physiological readiness that opens}
\]

and

\[
O(t)=\text{ecological opportunity that remains before expiry}.
\]

An organism can be:
- informed but not yet ready;
- ready but already too late;
- both ready and within the opportunity window.

The usable gate is

\[
U(t)=G(t)O(t).
\]

## 2. Exact readiness-opportunity window

Take the simple witness

\[
G(t)=1-e^{-\gamma t},
\]

\[
O(t)=e^{-\beta t},
\]

with \(\gamma,\beta>0\).

Then

\[
U(t)
=
(1-e^{-\gamma t})e^{-\beta t}.
\]

It is zero initially because the actor is not ready, and tends to zero at late
times because the opportunity expires.

Its unique maximum is

\[
\boxed{
t_U^*
=
\frac{1}{\gamma}
\log\left(1+\frac{\gamma}{\beta}\right).
}
\]

At that time,

\[
G(t_U^*)
=
\frac{\gamma}{\beta+\gamma},
\]

and

\[
O(t_U^*)
=
\left(
\frac{\beta}{\beta+\gamma}
\right)^{\beta/\gamma}.
\]

Thus the biologically usable action window peaks before readiness is complete.

## 3. Comparative predictions

Faster opportunity expiry \(\beta\) moves the optimum earlier.

Faster readiness \(\gamma\) also moves the usable window earlier.

The key quantity is therefore not "when is the organism ready?" or "when does
the opportunity end?" separately, but their overlap.

## 4. Adding information as another prerequisite

A convenient equal-rate witness for \(n\) opening prerequisites is

\[
F_n(t)
=
(1-e^{-\alpha t})^n e^{-\beta t}.
\]

Its unique maximum is

\[
\boxed{
t_n^*
=
\frac{1}{\alpha}
\log\left(
1+\frac{n\alpha}{\beta}
\right).
}
\]

For \(n=2\), the two opening prerequisites can represent physiological
readiness and normalized information surplus that mature at the same rate.

The common opening level at the optimum is

\[
\frac{n\alpha}{\beta+n\alpha}.
\]

More prerequisites shift the optimum later, while faster expiry pulls it
earlier.

This witness is not a claim that information literally follows the same
exponential trajectory as readiness. It demonstrates the geometry of
overlapping prerequisites.

## 5. Relationship to the earlier actionability theorem

The earlier Paper-2 theorem used a declining actionability coordinate \(r(t)\).

That result is recovered conditionally after readiness is effectively open:

\[
G(t)\approx1,
\qquad
r(t)\approx O(t).
\]

Across the full life cycle, however, usable actionability can be non-monotonic:

\[
r_{\mathrm{usable}}(t)
\propto
G(t)O(t).
\]

This resolves the apparent conflict between:
- developmental readiness increasing with time;
- ecological optionality decreasing with time.

They are different primitive processes.

## 6. Biological examples

### Emergence / flowering

Developmental physiology opens \(G\). A short resource or reproductive window
can close \(O\).

### Migration

Circannual/photoperiodic readiness can open \(G\). Route, stopover, fuel,
breeding and resource deadlines can progressively close particular opportunity
gates \(O_a\).

### Decision checkpoints

The "Mikawa-Anjo clock" operates only where

\[
G>0
\quad\text{and}\quad
O>0.
\]

Information acquired outside this overlap can be accurate but behaviorally
useless.

## 7. New ecological framing

Seasonal adaptation requires overlap among three conditions:

\[
\boxed{
\text{ready}
\times
\text{opportunity remains}
\times
\text{useful information}.
}
\]

A failure in any one channel can produce mismatch without implying a failure
of the other two.

## 8. Novelty boundary

Opening/closing gates and product windows are standard mathematical objects.

PAYOFF-B's contribution is the ecological synthesis: readiness and
actionability are not the same clock, and their overlap determines when
information can actually be converted into seasonal correction.
