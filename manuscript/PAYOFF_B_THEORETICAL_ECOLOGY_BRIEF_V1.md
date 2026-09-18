# Exactly one migration optimum under anti-phase environmental switching

**Target:** *Theoretical Ecology* — Brief Communication

## Abstract

Dispersal can increase long-run population growth when habitat quality varies out of phase through time, but the phrase “intermediate dispersal is best” does not specify whether the optimum is unique or how it scales with environmental contrast. We analyze the symmetric two-patch, two-season anti-phase model for which the periodic growth exponent is available in closed form. After nondimensionalization, the temporal growth premium is

\[
F(u,v)=-u+\operatorname{asinh}\!\left[\frac{u}{\sqrt{u^2+v^2}}\sinh\!\sqrt{u^2+v^2}\right],
\]

where \(u=m\tau\) is migration per season and \(v=|x|\tau\) is seasonal patch contrast. We prove that, for every \(v>0\), \(F\) has exactly one stationary point on \(u>0\), and that point is the unique global maximum. Thus optimal migration collapses to one dimensionless curve \(u_*(v)\). The optimum approaches \(1.6061152988\ldots\) under weak contrast and \(1+1/v+O(v^{-2})\) under strong contrast, so \(m_*\tau\to1\). Environmental contrast therefore changes the optimal migration rate only within a bounded seasonal-timescale window in this exact model. The result sharpens existing dispersal-induced-growth theory from existence of beneficial intermediate migration to a unique, dimensionless connectivity prediction.

**Keywords:** dispersal; Floquet growth; metapopulation; periodic environment; source–sink dynamics; temporal heterogeneity

## 1. Introduction

Movement links local population growth to environmental variation. In static two-patch models, dispersal can alter abundance, stability, and persistence, with the direction of the effect depending on patch asymmetry and density dependence (Holt 1985). In stochastic metapopulations, dispersal can also change synchrony and thereby alter stability (Abbott 2011). Periodic environments add a different possibility: when the identity of the favorable patch changes through time, movement can convert temporal asynchrony among patches into positive long-run growth.

This effect is now developed mathematically as **dispersal-induced growth** (DIG). Katriel (2022) characterized DIG in periodic environments using the principal Floquet exponent. Benaïm et al. (2023) studied a two-patch model in which source and sink identities exchange every half period and obtained an explicit growth expression, emphasizing the inflation regime at small migration and long periods. Subsequent work extended the theory to broader migration structures and reducible or asymmetric migration matrices (Benaïm et al. 2025; Liu & Wang 2025).

These results establish that intermediate migration can be beneficial. They do not by themselves give a sharp answer to a simpler quantitative question: **for the exactly anti-phase symmetric model, is the migration rate maximizing the temporal growth premium unique for every nonzero environmental contrast?** If so, does that optimum depend on the absolute growth scale, or only on a dimensionless relation between migration and switching timescales?

We answer those questions exactly. The closed-form growth exponent is not claimed as new; closely related explicit formulas already occur in the anti-phase literature (Benaïm et al. 2023). Our contribution is the global optimization theorem built on that solvable case. We show that the exact temporal premium has one and only one positive maximizer for every nonzero contrast, derive its one-parameter scaling law, and obtain weak- and strong-contrast asymptotes. The biological prediction is unusually compact: in the declared model, optimal migration remains on the order of one movement event per environmental season across the entire contrast range.

## 2. Anti-phase model and temporal premium

Consider two patches connected by symmetric migration rate \(m\ge0\). Each environmental state lasts \(\tau>0\). During the first season the local per-capita growth rates are

\[
(\bar r+x,\;\bar r-x),
\]

and during the second they swap,

\[
(\bar r-x,\;\bar r+x).
\]

Thus the two patches have identical time averages \(\bar r\), but their deviations from that average are exactly anti-phase. The population vector \(n=(n_1,n_2)^\top\) obeys a linear cooperative system with seasonal generators

\[
A_{\pm}=\begin{pmatrix}
\bar r\pm x-m&m\\
m&\bar r\mp x-m
\end{pmatrix}.
\]

Over a full cycle, the growth rate is determined by the dominant Floquet multiplier of \(\exp(A_-\tau)\exp(A_+\tau)\). For this symmetric anti-phase specialization, direct matrix algebra gives

\[
\Lambda_F=\bar r-m+\frac{1}{\tau}\operatorname{asinh}\!\left[
\frac{m}{\sqrt{m^2+x^2}}\sinh\!\left(\tau\sqrt{m^2+x^2}\right)
\right].
\]

Equivalent explicit representations are known for the corresponding switched two-patch problem (Benaïm et al. 2023). We use the formula as a starting point and optimize only the part created by temporal patch switching.

Define the temporal premium over the static time-averaged system,

\[
P=\Lambda_F-\bar r.
\]

With dimensionless variables

\[
u=m\tau,\qquad v=|x|\tau,
\]

we obtain

\[
F(u,v)=\tau P=-u+\operatorname{asinh}\!\left[
\frac{u}{d}\sinh d
\right],\qquad d=\sqrt{u^2+v^2}.
\tag{1}
\]

The average growth \(\bar r\) drops out of the optimization completely. For \(v>0\), \(F(0,v)=0\), \(F(u,v)>0\) for finite positive \(u\), and \(F(u,v)\to0\) as \(u\to\infty\). Hence at least one finite positive maximum exists. The issue is uniqueness.

## 3. A unique global migration optimum

### Theorem 1

For every fixed \(v>0\), the function \(F(u,v)\) in Eq. (1) has exactly one stationary point on \(u>0\). That point is the unique global maximum.

### Proof

Let

\[
d=\sqrt{u^2+v^2},\qquad s=\sinh d,\qquad c=\cosh d.
\]

Differentiating Eq. (1) gives

\[
F_u=-1+\frac{v^2s/d^3+u^2c/d^2}
{\sqrt{1+u^2s^2/d^2}}.
\tag{2}
\]

Both terms inside the comparison are positive. Squaring the positive numerator and denominator in the second term and simplifying shows that the sign of \(F_u\) is the sign of

\[
R(d)-\frac{u^2}{d^2},
\tag{3}
\]

where

\[
R(d)=\frac{\sinh^2d-d^2}{(d\cosh d-\sinh d)^2}.
\tag{4}
\]

Because \(d^2=u^2+v^2\), the second term in Eq. (3) is

\[
\frac{u^2}{d^2}=1-\frac{v^2}{d^2},
\]

which is strictly increasing in \(d\) for fixed \(v>0\), from zero at \(u=0\) toward one as \(u\to\infty\).

It remains to show that \(R(d)\) is strictly decreasing. Differentiation yields

\[
R'(d)=-\frac{2H(d)}{(d\cosh d-\sinh d)^3},
\]

with

\[
H(d)=\cosh d\,(d^2+\sinh^2d)-\sinh d\,(d^3+2d).
\]

For \(d>0\), the denominator is positive because \(d\cosh d-\sinh d\) vanishes at the origin and has derivative \(d\sinh d>0\). Expanding \(H\) as an even power series gives

\[
H(d)=\sum_{n=3}^{\infty}A_n\frac{d^{2n}}{(2n)!},
\]

where

\[
A_n=\frac{9^n}{4}-8n^3+16n^2-10n-\frac14.
\]

Since \(A_2=0\) and

\[
A_{n+1}-9A_n=8n(n-1)(8n-11)>0\qquad(n\ge2),
\]

all \(A_n>0\) for \(n\ge3\). Therefore \(H(d)>0\) and \(R'(d)<0\) for every \(d>0\).

At \(u=0\), the increasing side of the stationary condition is zero while \(R(v)>0\). As \(u\to\infty\), the increasing side tends to one while \(R(d)\to0\). A strictly increasing function and a strictly decreasing function can cross only once, and here they must cross. By Eq. (3), \(F_u\) is positive before this crossing and negative after it. The stationary point is therefore the unique global maximum. \(\square\)

The theorem replaces a generic “intermediate migration” statement by a single-valued prediction. Let \(u_*(v)\) denote the unique maximizer. Dimensional optimal migration is

\[
m_*=\frac{u_*(|x|\tau)}{\tau}.
\tag{5}
\]

All optima therefore collapse onto one curve in the dimensionless contrast \(v=|x|\tau\) (Fig. 2).

## 4. The optimum stays on the seasonal timescale

The scaling curve has simple endpoints.

### Weak environmental contrast

For fixed \(u>0\) and \(v\to0\), Eq. (1) expands as

\[
F(u,v)=v^2H_0(u)+O(v^4),
\]

where

\[
H_0(u)=\frac{u-\tanh u}{2u^2}.
\]

Its unique positive maximizer solves

\[
u\tanh^2u-2u+2\tanh u=0,
\]

which gives

\[
u_*(v)\longrightarrow u_0=1.60611529880277\ldots
\qquad(v\to0).
\tag{6}
\]

At this point

\[
H_0(u_0)=0.132487539446827\ldots,
\]

so the maximal dimensional premium is

\[
P_{\max}=0.13248753945\,x^2\tau+O(x^4\tau^3).
\tag{7}
\]

Thus weak anti-phase heterogeneity produces a quadratic rescue budget but selects a finite migration timescale independent of the absolute contrast magnitude to leading order.

### Strong environmental contrast

For \(d\to\infty\), Eq. (4) gives

\[
R(d)=\frac{1}{(d-1)^2}\left[1+O(d^2e^{-2d})\right].
\]

Substitution into the stationary condition yields

\[
u_*(v)=1+\frac1v+O(v^{-2}),
\qquad v\to\infty,
\tag{8}
\]

and therefore

\[
m_*\tau\to1.
\tag{9}
\]

The corresponding maximum satisfies

\[
\max_uF(u,v)=v-\log v-1+O(v^{-1}).
\tag{10}
\]

A fixed nine-point numerical audit, not used to prove uniqueness, quantifies how quickly these endpoint formulas approach the exact solution. At \(v=0.1\), the weak-contrast approximation to \(u_*\) has 0.0226% relative error and the weak approximation to the maximum premium has 0.0144% error. At \(v=10\), the strong approximation \(1+1/v\) has 0.933% error in \(u_*\) and \(v-\log v-1\) has 0.736% error in the maximum premium; by \(v=100\), these errors fall to 0.00995% and 0.00530%, respectively. No validity threshold is inferred from these checkpoints; they report approximation error for the exact model rather than defining new parameter regimes.

Equations (6)–(9) give a bounded timescale prediction across the full contrast axis: the optimal dimensionless migration moves from about 1.606 under weak contrast toward 1 under strong contrast. Contrast changes the precise optimum, but not its order of magnitude.

## 5. Biological interpretation and limits

The solvable anti-phase case isolates a mechanism that is easy to obscure in broader periodic models. Migration is harmful at both extremes for the temporal premium: at zero migration individuals cannot exploit the patch that is currently favorable, while very rapid migration homogenizes the patches and removes the benefit of their temporal opposition. Between these extremes, movement converts the reversal of patch quality into increased long-run growth. Theorem 1 shows that, in this symmetric case, this balance is not multimodal or parameter-fragile: there is exactly one best migration rate.

The scaling variable \(u=m\tau\) gives the ecological interpretation. Optimal movement is controlled primarily by the environmental switching clock. If seasons last \(\tau\), the preferred migration rate is approximately between \(1/\tau\) and \(1.606/\tau\) across the contrast range of the exact model. This is a stronger prediction than “some intermediate migration can help,” because it gives a narrow dimensionless target that can be compared across systems with different absolute growth rates and season durations.

This result sits inside, rather than replaces, modern DIG theory. Periodic dispersal-induced persistence has been established for much broader patch systems and migration matrices (Katriel 2022; Benaïm et al. 2023, 2025; Liu & Wang 2025). The price of the exact uniqueness result is symmetry: two patches, equal season duration, exact anti-phase switching, constant symmetric migration, and linear rare-population dynamics. Asymmetric migration, unequal season lengths, partial phase shifts, more patches, stochastic switching, and density dependence can change the shape of the growth response and are outside the theorem.

Those limitations define useful tests of robustness rather than hidden assumptions. The exact solution provides a benchmark: departures from a single optimum or from the seasonal-timescale band must be generated by model ingredients absent from the symmetric anti-phase core. In that sense, the theorem supplies a null geometry for more complicated temporally varying metapopulations.

## 6. Conclusion

For the symmetric two-patch anti-phase periodic environment, the temporal growth premium has exactly one positive migration optimum for every nonzero environmental contrast. The optimum is governed by a single dimensionless function \(u_*(v)\), approaching \(1.6061152988\ldots\) under weak contrast and 1 under strong contrast. The result does not claim that periodic environments generically have unique dispersal optima. It shows that one canonical and widely studied source-switching geometry does, and turns that geometry into a quantitative seasonal-timescale prediction.

## References

Abbott KC (2011) A dispersal-induced paradox: synchrony and stability in stochastic metapopulations. *Ecology Letters* 14:1158–1169. https://doi.org/10.1111/j.1461-0248.2011.01670.x

Benaïm M, Lobry C, Sari T, Strickler É (2023) Untangling the role of temporal and spatial variations in persistence of populations. *Theoretical Population Biology* 154:1–26. https://doi.org/10.1016/j.tpb.2023.07.003

Benaïm M, Lobry C, Sari T, Strickler É (2025) Dispersal-induced growth or decay in a time-periodic environment: the case of reducible migration matrices. *Journal of Mathematical Biology* 91:26. https://doi.org/10.1007/s00285-025-02258-1

Holt RD (1985) Population dynamics in two-patch environments: some anomalous consequences of an optimal habitat distribution. *Theoretical Population Biology* 28:181–208. https://doi.org/10.1016/0040-5809(85)90027-9

Katriel G (2022) Dispersal-induced growth in a time-periodic environment. *Journal of Mathematical Biology* 85:24. https://doi.org/10.1007/s00285-022-01791-7

Liu S, Wang H (2025) Dispersal-induced growth in time-periodic two-patch environments with asymmetric migration. *Journal of Mathematical Biology* 92:20. https://doi.org/10.1007/s00285-025-02325-7
