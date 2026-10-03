# PAYOFF-B clock-portfolio fragility under opportunity loss

Date: **2026-10-03**  
Status: **post-freeze exact corollary of the quadratic clock-portfolio witness; frozen GEB V2 unchanged**

## 1. Question

The clock-portfolio theorem asks how a seasonal system should allocate precision
between:

1. an upstream entry timer; and
2. repeated downstream feedback.

A new vulnerability question follows immediately:

> What happens if a system historically optimized for many downstream correction
> opportunities suddenly loses some of them?

This is ecologically relevant to stopover loss, corridor obstruction, compressed
resource windows, lost staging habitats, or any change that reduces the fraction
of historically usable correction opportunities.

## 2. Historical optimum

The historical portfolio uses

\[
V_0=V_{\rm ref}e^{-x}
\]

and

\[
|\lambda|=e^{-y}
\]

with \(n\) equivalent correction checkpoints.

Final inherited-error variance is

\[
V_n
=
V_{\rm ref}e^{-(x+2ny)}.
\]

For target variance \(V^*\), define

\[
P=\log\frac{V_{\rm ref}}{V^*}.
\]

Under the quadratic cost witness

\[
C=\frac a2x^2+\frac b2y^2,
\]

the optimum satisfies

\[
x^*+2ny^*=P
\]

with feedback precision share

\[
\boxed{
s_{\rm feedback}
=
\frac{2ny^*}{P}
=
\frac{4n^2a}{b+4n^2a}.
}
\]

## 3. Sudden opportunity loss

Let \(\omega\in[0,1]\) be the fraction of historically usable downstream
correction opportunity that remains after environmental change.

The organism retains the historical allocation \((x^*,y^*)\) in the immediate
response, but only \(\omega n\) equivalent correction opportunity remains.

Then

\[
V_{\rm disrupted}
=
V_{\rm ref}
e^{-[x^*+2\omega ny^*]}.
\]

Relative to the historical target,

\[
\boxed{
\frac{V_{\rm disrupted}}{V^*}
=
\exp\left[2n(1-\omega)y^*\right].
}
\]

Using the historical feedback share,

\[
\boxed{
\frac{V_{\rm disrupted}}{V^*}
=
\exp\left[(1-\omega)s_{\rm feedback}P\right].
}
\]

Equivalently,

\[
\boxed{
\log\frac{V_{\rm disrupted}}{V^*}
=
(1-\omega)s_{\rm feedback}P.
}
\]

## 4. Ecological interpretation

The historical fraction of precision supplied by downstream feedback is also a
fragility coordinate under sudden loss of downstream opportunity.

For the same target precision \(P\) and the same fractional opportunity loss:

- timer-heavy systems have smaller \(s_{\rm feedback}\) and smaller error
  inflation;
- feedback-heavy systems have larger \(s_{\rm feedback}\) and larger error
  inflation;
- one-shot systems with \(n=0\) have \(s_{\rm feedback}=0\), so loss of
  downstream correction opportunity is irrelevant because they never depended
  on it.

Thus:

> **The benefit of having many correction opportunities creates a dependence on
> those opportunities.**

A strategy that is optimal in an intact route can become disproportionately
vulnerable when corridor structure is degraded.

## 5. More checkpoints can increase fragility after sudden loss

Under the quadratic witness,

\[
s_{\rm feedback}
=
\frac{4n^2a}{b+4n^2a}
\]

increases with \(n\).

Therefore, holding the target precision and cost curvatures fixed, historical
systems with more correction checkpoints evolve a more feedback-heavy
portfolio and suffer greater immediate error inflation from the same fractional
loss of opportunity.

This does **not** mean more checkpoints are harmful in intact environments.
They lower the cost of achieving precision.  The vulnerability appears only
when the historically available architecture is suddenly removed.

## 6. Flexibility-dependence tradeoff

The same checkpoint number \(n\) that increases feedback reliance also reduces
the minimum cost of hitting the target precision in the intact environment.

At the quadratic optimum,

\[
\boxed{
C^*(n)
=
\frac{abP^2}
{2(b+4an^2)}.
}
\]

For \(n>0\),

\[
\frac{dC^*}{dn}<0.
\]

Meanwhile, for any fixed opportunity-loss fraction
\(\omega<1\),

\[
\log F(n)
=
(1-\omega)P
\frac{4an^2}{b+4an^2},
\]

and

\[
\frac{d\log F}{dn}>0.
\]

Therefore:

\[
\boxed{
n\uparrow
\quad\Rightarrow\quad
\text{intact precision becomes cheaper}
\quad\text{but}\quad
\text{opportunity-loss fragility increases}.
}
\]

This is a **flexibility-dependence tradeoff**.

Repeated correction opportunities are beneficial when the route architecture is
intact.  Because the historical optimum then shifts precision investment toward
feedback, the same architecture becomes more dependent on retaining those
opportunities.

The result explains how high behavioral flexibility can coexist with high
environmental sensitivity: flexibility is robust to timing error but vulnerable
to removal of the conditions that make correction possible.

## 7. Climate-change and land-use interpretation

The opportunity-loss parameter \(\omega\) can represent different mechanisms:

- loss of stopover sites;
- narrowing of resource windows;
- barriers that make route correction costly or delayed;
- development that causes animals to pause or bypass useful habitat;
- phenological acceleration that removes time for later correction.

The theorem is intentionally agnostic about which physical mechanism reduces
\(\omega\).

## 8. Industrial mule deer as an anchor, not a validation

Aikens et al. (2022) provide a relevant natural boundary case.  Industrial
energy development in a mule-deer migration corridor altered migration
behaviour and reduced route-scale green-wave surfing by 38.65% over the study
period.  PAYOFF-B's registered reanalysis independently found lower relative
near-boundary movement-control permeability in the large-development
population.

Those results show that landscape modification can attenuate movement control
while migration remains physically possible.

They do **not** estimate:

\[
n,\quad
\omega,\quad
s_{\rm feedback},
\]

or the clock-portfolio fragility factor.

The industrial system is therefore an **opportunity-loss anchor**, not a test
of the theorem.

## 9. Strong prospective test

A direct test should use the same taxon or population under different
opportunity regimes.

Before opening outcome data, measure or freeze:

1. entry-phase variance \(V_0\);
2. number or weighted amount of usable correction opportunities;
3. downstream phase retention or final phase variance;
4. a perturbation that changes opportunity without redefining entry timing.

The strongest prediction is not merely that disrupted routes have larger
mismatch. It is:

\[
\boxed{
\text{error inflation}
\propto
\text{historical feedback reliance}
\times
\text{opportunity loss}.
}
\]

Systems historically relying more on downstream correction should be more
sensitive to the same proportional loss of correction opportunity.

## 10. Evolutionary rescue

If the new opportunity regime persists, selection can in principle reallocate
investment toward the entry timer.

The immediate fragility theorem therefore describes **ecological mismatch
before portfolio re-optimization**.

This generates a temporal prediction:

1. rapid environmental change -> mismatch spike in feedback-heavy systems;
2. persistent new regime -> possible evolutionary/developmental shift toward
   greater upstream precision;
3. if upstream precision is physiologically constrained, chronic mismatch can
   remain.

## 11. Boundary

The exponential precision functions and quadratic costs are a transparent
mathematical witness, not a universal cost law.

The exact licensed result is conditional on that declared portfolio model.

The ecological synthesis is:

> **Clock architecture creates hidden dependence: organisms that historically
> achieved timing accuracy through repeated downstream correction are
> especially vulnerable when environmental change removes those correction
> opportunities.**


## Robustness to per-checkpoint operating costs

The canonical quadratic witness treats \(y\) as an investment in feedback
capacity, with cost \(by^2/2\) that does not itself multiply by the number of
checkpoints.

A stricter operating-cost alternative is

\[
C
=
\frac a2x^2
+
n\frac b2y^2.
\]

The same precision constraint holds,

\[
x+2ny=P.
\]

The optimum precision shares become

\[
\boxed{
s_{\mathrm{timer}}
=
\frac{b}{b+4an},
\qquad
s_{\mathrm{feedback}}
=
\frac{4an}{b+4an}.
}
\]

The feedback-majority threshold is now

\[
\boxed{
n_c=\frac{b}{4a},
}
\]

and the minimum intact cost is

\[
\boxed{
C^*_{\rm use}
=
\frac{abP^2}{2(b+4an)}.
}
\]

Thus cumulative per-checkpoint operating cost weakens the rate at which the
portfolio shifts toward feedback—from an \(n^2\) effect to an \(n\) effect—but
does not change the qualitative results:

1. more correction checkpoints lower the minimum intact precision cost;
2. more checkpoints increase the optimal feedback share;
3. loss of a fixed fraction of usable opportunity harms more
   feedback-dependent portfolios.

The flexibility-dependence tradeoff is therefore not an artifact of assuming
that feedback capacity has zero per-use cost.
