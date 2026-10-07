# PAYOFF-B competitive-information extension

Date: **2026-10-07**  
Status: **prospective reduced-form extension; frozen PAYOFF-B manuscripts unchanged**

## 1. Purpose

The current PAYOFF-B actionability model writes usable later information as

\[
N(t)=r(t)V_A(q(t))-C(t),
\]

where:

- \(q(t)\) is cue quality;
- \(r(t)\) is retained actionability / recourse;
- \(C(t)\) is direct waiting cost;
- above the canonical actionability boundary \(q_0=B/S\),

\[
V_A(q)=Sq-B.
\]

A competitive prediction system exposes a distinct reason that information can
lose value even when the focal actor remains physically able to act:

> other actors may learn the same information, so the focal actor loses its
> **relative** informational advantage.

This extension is a mechanism-separation device. It is not claimed to be a new
theorem of market microstructure.

## 2. Reduced form

Let

\[
e(t)\in[0,1]
\]

be a declared **retained differential-information weight**. In a competitive
prediction system, it can represent the fraction of focal information value
that remains unabsorbed by other actors or a market.

Define

\[
\boxed{
N(t)=r(t)e(t)[Sq(t)-B]-C(t)
}
\]

whenever \(q(t)>q_0\).

The previous PAYOFF-B actionability model is recovered exactly by \(e(t)=1\).

A pure competitive-information limit is obtained by \(r(t)=1\).

The product

\[
u(t)=r(t)e(t)
\]

will be called **retained usable-information weight**.

## 3. Balance condition

For differentiable paths,

\[
\frac{dN}{dt}
=
reSq'
+r'e[Sq-B]
+re'[Sq-B]
-C'.
\]

Any interior stationary point satisfies

\[
reSq'
=
-r'e[Sq-B]
-re'[Sq-B]
+C'.
\]

With zero marginal waiting cost and positive \(r,e,V_A\),

\[
\boxed{
\frac{Sq'}{Sq-B}
=
-\frac{r'}{r}
-\frac{e'}{e}
}
\]

so the relative gain in focal information value balances the sum of:

1. relative actionability loss;
2. relative loss of differential information value.

## 4. General product-identification result

The observable reduced form depends on \(r(t)\) and \(e(t)\) only through

\[
u(t)=r(t)e(t).
\]

Therefore

\[
\boxed{
N(t)=u(t)V_A(q(t))-C(t).
}
\]

If \(q(t)\), \(C(t)\), and net usable value \(N(t)\) were known exactly, then
above the actionability boundary one could at most recover

\[
u(t)
=
\frac{N(t)+C(t)}{V_A(q(t))}.
\]

One cannot recover \(r(t)\) and \(e(t)\) separately without additional
information.

More generally, any two admissible pairs

\[
(r_1(t),e_1(t))
\quad\text{and}\quad
(r_2(t),e_2(t))
\]

that satisfy

\[
r_1(t)e_1(t)=r_2(t)e_2(t)
\]

for every \(t\) generate exactly the same \(N(t)\) under the same \(q(t)\) and
\(C(t)\).

This is **complete mechanism aliasing in the declared multiplicative reduced
form**.

It is simple algebra, not a claimed generic identification theorem. Its
importance for PAYOFF-B is interpretive:

> a hump-shaped information-value trajectory does not by itself identify
> biological irreversibility.

Independent measurement of biological actionability is required if the
ecological claim is specifically about recourse loss.

## 5. Exponential special case

Let information improve from the canonical actionability boundary:

\[
q(t)
=
q_0+\Delta_q[1-\exp(-\alpha t)],
\]

with \(\alpha>0\).

Let

\[
r(t)=\exp(-\beta t),
\qquad
e(t)=\exp(-\gamma t),
\]

with \(\beta,\gamma\ge0\) and \(\beta+\gamma>0\).

With zero direct waiting cost,

\[
N(t)
=
S\Delta_q
\exp[-(\beta+\gamma)t]
[1-\exp(-\alpha t)].
\]

The unique interior maximum is

\[
\boxed{
t^*
=
\frac{\log\left(1+\alpha/(\beta+\gamma)\right)}{\alpha}.
}
\]

### Corollary 1 — hazards add

Only

\[
\beta+\gamma
\]

enters the optimum.

Thus the exponential version of the general product-identification problem is:

\[
\boxed{
\text{peak timing identifies total usable-value decay, not its mechanism.}
}
\]

### Corollary 2 — ecological limit

If \(\gamma=0\),

\[
t^*
=
\frac{\log(1+\alpha/\beta)}{\alpha},
\]

which recovers the existing PAYOFF-B actionability result.

### Corollary 3 — competitive-information limit

If \(\beta=0\) and \(\gamma>0\), an interior optimum still exists:

\[
t^*
=
\frac{\log(1+\alpha/\gamma)}{\alpha}.
\]

Useful information can therefore peak before predictive accuracy peaks even
when the actor loses no physical ability to act.

## 6. Horse racing as a boundary case

Pari-mutuel racing is useful because, until the wagering cutoff, the focal
action set can remain approximately available while collective forecasts
change rapidly.

The clean object is **not**:

> buy early to lock the displayed odds.

In a pari-mutuel pool, an early displayed price is not generally the final
settlement price.

The useful object is instead:

> how much incremental predictive value does a fixed forecast retain over the
> contemporaneous collective forecast?

For race \(r\), horse \(i\), and pre-race time \(t\), let

\[
f_{ir}
\]

be a fixed public/form forecast and

\[
m_{irt}
\]

the normalized contemporaneous market-implied probability.

A deliberately simple forecast-combination device is

\[
h_{irt}(w_t)
\propto
f_{ir}^{\,w_t}
m_{irt}^{\,1-w_t}.
\]

Choose \(w_t\) on training races only by minimizing multinomial log loss.

Interpretation:

- \(w_t=0\): the market encompasses the fixed forecast under this combination;
- \(w_t>0\): the fixed forecast retains incremental predictive content;
- a decline in \(w_t\) is descriptive evidence that the fixed forecast is
  becoming less complementary to the market.

Crucially,

\[
w_t\neq e(t)
\]

as a structural identity. \(w_t\) is only an empirical proxy / forecast
encompassing weight.

## 7. Retrospective JRA test

The current retrospective design uses:

- JRA-VAN accumulated TM category 7 as the fixed final pre-race forecast;
- time-series win odds;
- T-30, T-15, T-10, T-5, and LAST;
- a 10-minute maximum staleness rule;
- an outcome-blind chronological 70/30 date split;
- training-only calibration of the TM score;
- training-only fitting of \(w_t\);
- held-out log loss and paired race-level bootstrap contrasts.

The primary held-out endpoints are:

\[
\Delta_{\rm form}(t)
=
L_{\rm market}(t)-L_{\rm hybrid}(t),
\]

plus the training-estimated \(w_t\) trajectory and the market's own log loss.

The strongest descriptive PAYOFF pattern would be:

\[
L_{\rm market}(t)\downarrow
\]

while

\[
\Delta_{\rm form}(t)\downarrow.
\]

That would mean the collective forecast improves while the fixed forecast's
incremental value disappears.

## 8. Prior-art boundary

The racing mechanisms and forecast-combination architecture are established
prior art.

In particular:

- Benter-style systems already combine a fundamental model with public
  implied probabilities;
- Figlewski and subsequent betting-market research examine whether focal
  forecasts contain information beyond market odds;
- Johnson, Jones & Tang analyze information in price paths;
- Green et al. (2019) directly show that useful horse-racing forecasting
  information can diffuse through a market and lose economic value over time;
- Hanyu et al. (2026) analyze last-minute information dynamics in Japanese
  pari-mutuel racing.

Therefore PAYOFF-B does **not** claim novelty for:

- information aggregation in betting markets;
- forecast combination with odds;
- time-varying market efficiency;
- information-value decay through market diffusion;
- predictive content of odds paths;
- late informed wagering.

The racing route is retained only as a known-mechanism contrast for the PAYOFF
identification problem.

## 9. What racing changes in PAYOFF-B

Before this comparison, a hump in usable information could be narrated too
quickly as:

\[
q(t)\uparrow,\quad r(t)\downarrow.
\]

The competitive boundary case shows that the same qualitative trajectory can
instead occur under

\[
q(t)\uparrow,\quad r(t)\approx1,\quad e(t)\downarrow.
\]

Therefore the safe general statement is:

> **Information is useful only while it remains usable; loss of usability can
> arise from different mechanisms that must be measured separately.**

For the ecological paper, the empirical burden becomes stronger:

1. estimate cue/predictive quality \(q(t)\);
2. independently measure biological recourse/actionability \(r(t)\);
3. do not infer \(r(t)\) merely from the observed timing of information use.

## 10. Claim boundary

Safe:

> In the declared multiplicative reduced form, only the product of retained
> actionability and retained differential-information value enters net usable
> information. Their separate mechanisms are not identified by the value
> trajectory alone.

Safe:

> In the exponential special case, only the sum of the two decay rates enters
> the closed-form optimum.

Safe:

> Horse racing supplies an established competitive-information boundary case
> in which information value can decay through market absorption without a
> matching loss of physical actionability.

Not licensed:

> This is a new theorem of optimal stopping or market microstructure.

Not licensed:

> The horse-racing forecast combination is novel.

Not licensed:

> A fitted \(w_t\) is numerically equal to the structural \(e(t)\).

Not licensed:

> Better probabilistic prediction guarantees positive betting returns.

Not licensed:

> An ecological information-value hump proves loss of biological recourse.
