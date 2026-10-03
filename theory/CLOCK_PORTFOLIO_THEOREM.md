# PAYOFF-B clock-portfolio theorem

Date: **2026-10-03**  
Status: **post-freeze theoretical extension; frozen GEB V2 unchanged**

## 1. Why different clock architectures can persist

The serial two-clock result shows

\[
V_n=\lambda^{2n}V_0
\]

when no new process innovation is added.

Thus the same final seasonal precision can be obtained by:

- reducing entry-phase variance \(V_0\) with a more precise
  developmental/physiological clock;
- reducing \(|\lambda|\) with stronger repeated post-entry feedback;
- combining both.

To turn this equivalence into a strategy-allocation result, assign costs to
precision in each clock.

## 2. Log-precision coordinates

Let \(V_{\rm ref}\) be the phase variance without additional entry-clock
investment.

Let timer effort \(x\ge0\) reduce entry variance as

\[
V_0
=
V_{\rm ref}e^{-x}.
\]

Let per-checkpoint feedback effort \(y\ge0\) reduce absolute retention as

\[
|\lambda|
=
e^{-y}.
\]

After \(n\) equivalent correction checkpoints,

\[
\boxed{
V_n
=
V_{\rm ref}
e^{-(x+2ny)}.
}
\]

For a target \(V^*<V_{\rm ref}\), define required log-precision

\[
P
=
\log\frac{V_{\rm ref}}{V^*}.
\]

The target is reached when

\[
x+2ny\ge P.
\]

## 3. Convex cost model

Let

\[
C_T(x)=\frac a2x^2
\]

be the cost of entry-clock precision and

\[
C_F(y)=\frac b2y^2
\]

the cost of post-entry feedback effort.

Here:

- larger \(a\) means precise entry timing is expensive;
- larger \(b\) means strong downstream correction is expensive.

The minimum-cost solution lies on

\[
x+2ny=P.
\]

For \(n>0\), the unique optimum is

\[
\boxed{
x^*
=
\frac{bP}
{b+4n^2a}
}
\]

and

\[
\boxed{
y^*
=
\frac{2naP}
{b+4n^2a}.
}
\]

The minimum total cost is

\[
\boxed{
C^*
=
\frac{abP^2}
{2(b+4n^2a)}.
}
\]

## 4. Precision-budget shares

The fraction of required log-precision supplied by the entry timer is

\[
\boxed{
s_T
=
\frac{x^*}{P}
=
\frac{b}
{b+4n^2a}.
}
\]

The fraction supplied by downstream feedback is

\[
\boxed{
s_F
=
\frac{2ny^*}{P}
=
\frac{4n^2a}
{b+4n^2a}.
}
\]

Thus

\[
s_T+s_F=1.
\]

These shares are independent of target precision \(P\) under the quadratic cost
assumption.

## 5. Checkpoint-number theorem

Holding cost curvatures fixed,

\[
\frac{\partial s_F}{\partial n}>0
\]

for \(n>0\).

Therefore:

> **Life histories with more opportunities for post-entry correction should
> optimally rely more on feedback and less on entry-clock precision.**

At \(n=0\),

\[
s_T=1,
\qquad
s_F=0.
\]

A one-shot event with no post-event correction opportunity must obtain all final
precision upstream.

This gives a formal ecological contrast:

- emergence / one-shot flowering commitment can favor precise upstream timing;
- long migration with many stopovers can tolerate noisier departure timing if
  phase can be corrected repeatedly.

## 6. Relative-cost theorem

If entry-clock precision becomes more costly (\(a\uparrow\)),

\[
s_F\uparrow.
\]

If downstream feedback becomes more costly (\(b\uparrow\)),

\[
s_T\uparrow.
\]

Thus different species can occupy different clock architectures even under the
same final precision target because they face different costs of anticipation
and correction.

## 7. Ecological strategy classes

The theorem turns the qualitative timer × feedback matrix into a cost-based
continuum.

### Timer-heavy strategy

Expected when:
- post-entry decisions are few;
- errors are difficult to reverse;
- feedback actions are expensive;
- entry cues are cheap and reliable.

### Feedback-heavy strategy

Expected when:
- many checkpoints exist;
- actions can be revised repeatedly;
- movement or waiting is cheap relative to upstream precision;
- destination conditions are difficult to predict at entry.

### Mixed strategy

Expected when both forms of precision are useful and costly.

The model therefore predicts **strategic diversity in clock architecture**
rather than one universally optimal phenological clock.

## 8. Why this matters for climate change

Climate change can alter different terms separately.

It can:
- increase the cost of accurate upstream prediction;
- remove stopovers or shorten resource windows, effectively reducing \(n\);
- increase the cost of feedback;
- change the final precision required for successful interaction.

A species adapted to a feedback-heavy strategy may therefore become vulnerable
when route simplification or habitat loss removes correction checkpoints even
if its physiological clock is unchanged.

Conversely, a species with a precise but rigid entry clock can become
vulnerable when cue–driver relationships deteriorate because it has little
downstream recourse.

## 9. Interaction mismatch

Two partners can achieve similar historical final synchrony using different
portfolios.

When climate change changes cue reliability, checkpoint number or correction
costs, those previously equivalent strategies need not remain equivalent.

The serial two-clock mismatch theorem then converts the emerging differences in
entry error and retention into interaction mismatch.

This gives a maintenance mechanism for apparently redundant clock strategies:

> **different clock portfolios can be equally successful under historical
> conditions but diverge when climate change alters the relative costs or
> availability of anticipation and correction.**

## 10. Natural interpretation

Mule deer illustrate the feedback-heavy possibility: migration begins over a
wide range of phase errors, yet downstream speed/stopover adjustment strongly
compresses that variation.

Greater snow goose reproductive timing illustrates downstream stage buffering:
arrival differences are partly absorbed before laying.

Insect emergence and flowering systems provide natural contrasts where the
focal event itself can be much less reversible.

These are motivating anchors, not parameter estimates of \(a\), \(b\) or the
optimal portfolio.

## 11. Novelty boundary

Precision allocation, convex optimization and control-effort trade-offs are
standard mathematical ideas.

PAYOFF-B should claim the ecological synthesis:

> **entry-clock precision and downstream error correction are alternative
> investments in seasonal accuracy, and the number and cost of correction
> opportunities determine which clock architecture is favored.**

The cost functions used here are a transparent witness, not a universal law.
