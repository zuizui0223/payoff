# PAYOFF-B weighted correction-opportunity theorem

Date: **2026-10-03**  
Status: **post-freeze exact extension; frozen GEB V2 unchanged**

## 1. Why checkpoint count is not enough

The clock-portfolio theorem used checkpoint number \(n\) as a transparent
measure of downstream correction opportunity.

Natural routes are heterogeneous.  A long, food-rich stopover at a critical
position can contribute more correction capacity than several short or poorly
placed sites.  Conversely, loss of a named site may have little effect if an
alternative provides the same usable correction function.

The relevant quantity is therefore not site count but **correction leverage**.

## 2. Heterogeneous checkpoint model

Let timer effort \(x\) supply upstream log-precision.

For checkpoint \(j\):

- \(c_j\ge0\) is its correction leverage;
- \(y_j\ge0\) is feedback effort allocated there;
- \(b_j>0\) is effort-cost curvature.

The final precision budget is

\[
x+2\sum_j c_jy_j=P.
\]

The cost is

\[
C
=
\frac a2x^2
+
\frac12\sum_j b_jy_j^2.
\]

Define weighted route leverage

\[
\boxed{
L
=
\sum_j\frac{c_j^2}{b_j}.
}
\]

## 3. Exact optimal portfolio

The unique minimum-cost allocation is

\[
\boxed{
x^*
=
\frac{P}{1+4aL}
}
\]

and

\[
\boxed{
y_j^*
=
\frac{2aPc_j}
{b_j(1+4aL)}.
}
\]

The timer share is

\[
\boxed{
s_T
=
\frac{1}{1+4aL},
}
\]

whereas the total feedback share is

\[
\boxed{
s_F
=
\frac{4aL}
{1+4aL}.
}
\]

The checkpoint-specific share is

\[
\boxed{
s_j
=
\frac{
4a\,c_j^2/b_j
}{
1+4aL
}.
}
\]

Thus checkpoint contribution is proportional to

\[
\boxed{
\frac{c_j^2}{b_j}.
}
\]

High-leverage, low-cost checkpoints carry disproportionately large parts of the
historical precision portfolio.

The minimum cost is

\[
\boxed{
C^*
=
\frac{aP^2}
{2(1+4aL)}.
}
\]

## 4. Connection to the existing checkpoint scalings

### Independent per-checkpoint operating capacities

If all \(c_j=1\) and all \(b_j=b\),

\[
L=\frac nb,
\]

so

\[
s_F
=
\frac{4an}
{b+4an}.
\]

This is exactly the previously derived additive per-use cost scaling.

### One shared feedback capacity

If a single feedback investment \(y\) is reused at every checkpoint and total
route leverage is

\[
C_{\rm route}
=
\sum_jc_j,
\]

then

\[
s_F^{\rm shared}
=
\frac{
4aC_{\rm route}^2
}{
b+4aC_{\rm route}^2
}.
\]

For equal \(c_j=1\), \(C_{\rm route}=n\), recovering the canonical \(n^2\)
capacity-cost scaling.

The apparent \(n\) versus \(n^2\) discrepancy is therefore a difference in
whether correction capacity is purchased independently at each stage or shared
across stages.

## 5. Effective opportunity retention

Suppose environmental change leaves only fraction \(o_j\in[0,1]\) of
checkpoint \(j\)'s historically usable correction opportunity.

At the historical independent-capacity optimum, downstream precision
contribution from checkpoint \(j\) is proportional to \(c_j^2/b_j\).

Therefore the effective retained opportunity is

\[
\boxed{
\omega_{\rm eff}
=
\frac{
\sum_j
o_jc_j^2/b_j
}{
\sum_j
c_j^2/b_j
}.
}
\]

This is the quantity that belongs in the immediate fragility equation.

It is **not** generally:

- fraction of sites retained;
- fraction of habitat area retained;
- fraction of route distance retained.

If all checkpoints are equivalent, those simpler fractions can coincide with
\(\omega_{\rm eff}\).  Otherwise they need not.

## 6. Weighted fragility identity

Let historical feedback share be \(s_F\).  Holding the historical allocation
fixed immediately after disruption,

\[
\boxed{
\frac{V_{\rm disrupted}}{V^*}
=
\exp[
(1-\omega_{\rm eff})s_FP
].
}
\]

Thus all previous opportunity-loss results remain exact after replacing the
raw opportunity fraction by the contribution-weighted quantity
\(\omega_{\rm eff}\).

## 7. Checkpoint importance

If one checkpoint \(j\) is completely lost and all others remain intact, its
fraction of historical feedback contribution is

\[
\boxed{
w_j
=
\frac{
c_j^2/b_j
}{
\sum_k c_k^2/b_k
}.
}
\]

Then

\[
1-\omega_{\rm eff}=w_j
\]

and immediate inflation is

\[
\boxed{
F_j
=
\exp[
w_js_FP
].
}
\]

This defines a **correction-opportunity importance weight**.

Removing one high-\(w_j\) checkpoint can therefore be more damaging than
removing several low-\(w_j\) checkpoints.

## 8. Substitution and rerouting

The Filsø pink-footed-goose case illustrates why named-site loss cannot be
mapped directly to \(\omega\).  Birds shifted to alternative staging areas.

In the weighted language, substitution is successful when alternative sites
retain or replace the lost contribution to downstream precision.

Therefore a direct natural test should estimate effective opportunity from
functions such as:

- usable refuelling/stopover time;
- capacity to delay or accelerate subsequent travel;
- route alternatives;
- local resource-wave information;
- energetic cost of correction;

rather than site identity alone.

The theorem does not prescribe one universal field measure of \(c_j\). It
specifies what that measure must represent: **marginal contribution to usable
phase correction**.

## 9. Ecological prediction

Two routes with the same number of stopovers can have very different clock
portfolios if their checkpoint leverage distributions differ.

Likewise two routes that each lose one stopover can experience very different
fragility.

The strongest prediction is therefore:

> **clock-portfolio fragility should track loss of weighted correction leverage,
> not raw loss of sites.**

This sharpens the opportunity-loss theorem and converts the qualitative
substitution warning into an exact route-level quantity.

## 10. Empirical boundary

No current PAYOFF-B natural dataset identifies \(c_j\) from an independent
phase-correction function for every checkpoint and then observes a subsequent
loss event on the same route.

Accordingly:

- Filsø remains a substitution anchor;
- piping plover remains an opportunity-loss behavior anchor;
- industrial mule deer remain an opportunity-loss/control anchor.

The weighted theorem is prospective.

## 11. Novelty boundary

Heterogeneous resource quality, weighted habitat networks and quadratic
allocation models are standard ideas.

PAYOFF-B should claim only the seasonal-timing synthesis:

> **the relevant opportunity variable is the amount of historically used
> correction leverage retained after change; under the declared portfolio
> model its exact weighting is \(c_j^2/b_j\), not site count.**

The exact weights are model-specific and should not be treated as a universal
empirical index without separately identifying checkpoint leverage and costs.
