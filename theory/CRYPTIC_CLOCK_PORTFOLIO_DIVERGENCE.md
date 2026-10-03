# PAYOFF-B cryptic clock-portfolio divergence theorem

Date: **2026-10-03**  
Status: **post-freeze theoretical extension; frozen GEB V2 unchanged**

## 1. Hidden strategies can look identical before environmental change

The clock-portfolio theorem shows that historical final precision can be built
from different combinations of:

- upstream entry-clock precision;
- downstream feedback correction.

Write the historical precision budget as

\[
P=x+f,
\]

where \(x\) is upstream log-precision and \(f\) is downstream feedback
log-precision. Define feedback share

\[
\boxed{
s=\frac{f}{P}.
}
\]

Then

\[
x=(1-s)P.
\]

Two species can therefore reach the same historical target variance \(V^*\)
with different hidden values of \(s\).

Observed final synchrony does not reveal that hidden portfolio.

## 2. Opportunity loss reveals the hidden portfolio

Let \(\omega\in[0,1]\) be the fraction of historically usable downstream
correction opportunity remaining after environmental change.

If the historical allocation is retained in the immediate response,

\[
\boxed{
F
=
\frac{V'}{V^*}
=
\exp[(1-\omega)sP].
}
\]

Thus the post-change variance is

\[
V'=V^*F.
\]

The same historical phenotype can therefore hide different fragilities.

## 3. Cryptic divergence theorem

For two actors,

\[
\log\frac{V_1'}{V_2'}
=
\log\frac{V_1^*}{V_2^*}
+
(1-\omega_1)s_1P_1
-
(1-\omega_2)s_2P_2.
\]

If they were historically equally precise,

\[
V_1^*=V_2^*=V^*,
\]

and experience the same opportunity retention and precision budget,

\[
\omega_1=\omega_2=\omega,
\qquad
P_1=P_2=P,
\]

then

\[
\boxed{
\log\frac{V_1'}{V_2'}
=
(1-\omega)P(s_1-s_2).
}
\]

Therefore:

> **Two species can be phenologically indistinguishable under historical
> conditions yet diverge immediately after environmental change solely because
> their hidden clock portfolios differ.**

The feedback-heavy actor becomes less precise after the same loss of
correction opportunity.

This is a cryptic-strategy effect: historical synchrony does not imply shared
mechanism or shared robustness.

## 4. Fragility threshold

Suppose a species can tolerate at most variance inflation \(T\ge1\).

The threshold opportunity retention at which

\[
F=T
\]

is

\[
\boxed{
\omega_{\rm crit}
=
1-
\frac{\log T}
{sP}.
}
\]

For \(sP>0\), the species exceeds the tolerance when

\[
\omega<\omega_{\rm crit}.
\]

Larger feedback share \(s\) raises \(\omega_{\rm crit}\): less opportunity loss
is needed to cross the same failure threshold.

Timer-only systems \(s=0\) have no threshold for this perturbation because
their precision never depended on downstream opportunity.

## 5. Interaction mismatch variance

Historical synchrony between partners can also be cryptic.

Consider two zero-mean timing errors with equal historical variance \(V^*\) and
correlation \(r<1\).

Historical mismatch variance is

\[
M^*
=
\operatorname{Var}(E_1-E_2)
=
2V^*(1-r).
\]

After opportunity loss, let the partner-specific variance inflation factors be
\(F_1,F_2\), and use a transparent witness in which their correlation
coefficient remains \(r\). Then

\[
M'
=
V^*
[
F_1+F_2
-
2r\sqrt{F_1F_2}
].
\]

Therefore

\[
\boxed{
\frac{M'}{M^*}
=
\frac{F_1+F_2}{2}
+
\frac{r}{2(1-r)}
(\sqrt{F_1}-\sqrt{F_2})^2.
}
\]

The first term is the mean inflation of partner timing variance.

The second is an **asymmetry penalty**.

For positively correlated partners, unequal hidden portfolio fragility
increases interaction mismatch beyond the average variance inflation.

## 6. Why the asymmetry penalty matters

If partners have identical disruption factors,

\[
F_1=F_2=F,
\]

then

\[
M'/M^*=F.
\]

If they inflate differently and \(r>0\),

\[
(\sqrt{F_1}-\sqrt{F_2})^2>0,
\]

so interaction mismatch grows more than would be predicted from the average
loss of precision alone.

Thus climate change can reveal not only hidden individual fragility but hidden
**mechanistic asymmetry between interaction partners**.

This is especially relevant when partners historically tracked the same
seasonal environment closely. Strong historical correlation makes differences
in post-change fragility more consequential.

## 7. Ecological interpretation

Historically synchronized partners can rely on different routes to precision.

One partner may be timer-heavy:

\[
\text{precise entry}
+
\text{little downstream correction}.
\]

The other may be feedback-heavy:

\[
\text{noisy entry}
+
\text{strong downstream correction}.
\]

In an intact environment both can arrive at nearly the same seasonal precision.

If stopovers disappear, resource windows compress or correction opportunities
are otherwise lost, only the feedback-heavy partner loses the mechanism on
which its historical precision depended.

This produces a strong ecological prediction:

> **mismatch can emerge not because climate change affects partners
> differently at the physiological level, but because it exposes hidden
> differences in how they historically achieved the same timing accuracy.**

## 8. Relation to the flexibility-dependence tradeoff

The opportunity-loss theorem showed that more correction opportunities can make
intact precision cheaper while increasing dependence on those opportunities.

The cryptic-divergence theorem adds an interaction consequence.

If two partners historically evolved different feedback shares, environmental
change can expose that hidden portfolio difference even when their historical
phenological distributions were indistinguishable.

Thus flexibility has two faces:

1. it reduces the cost of achieving timing precision;
2. it creates dependence on the ecological architecture that makes correction
   possible.

## 9. Prospective empirical test

The strongest natural design starts with partners or populations that were
historically similarly precise but whose mechanisms differ.

Before opening the disrupted outcome, estimate independently:

1. historical target variance \(V^*\);
2. feedback precision share \(s\);
3. opportunity retention \(\omega\);
4. final timing variance after perturbation.

The prediction is

\[
\log(V'/V^*)
=
(1-\omega)sP.
\]

For interacting partners, additionally estimate historical timing-error
correlation and test whether post-change mismatch follows the predicted
partner-specific inflation factors.

A simple historical synchrony versus current mismatch comparison is
insufficient unless hidden portfolio and opportunity loss are measured
independently.

## 10. Claim boundary

The pairwise mismatch expression assumes equal historical variances, zero mean
errors and a retained correlation coefficient. It is a transparent witness,
not a universal ecological covariance law.

The exact portfolio-divergence identity itself requires only the declared
multiplicative precision architecture.

PAYOFF-B should claim the mechanistic prediction:

> **historical synchrony can conceal different clock portfolios, and
> environmental loss of correction opportunity can reveal those hidden
> strategies as differential precision and interaction mismatch.**

No current PAYOFF-B natural dataset directly estimates all required quantities
for a confirmatory test.
