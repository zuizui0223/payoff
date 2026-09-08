# Asymmetric endpoint-precision holdout theorem

Status: exact deterministic measurement-design result for the declared two-architecture PAYOFF frequency-response validation problem. It is not statistical power, a biological replicate count, or evidence that a natural population follows PAYOFF.

## Setup

The endpoint-derived canonical line uses

```text
u = Delta(0)
v = -Delta(1).
```

Let the deterministic centre-error half-widths be

```text
e_u  at p=0,
e_v  at p=1,
e_h  for every interior holdout.
```

For the true nonlinear residual

```text
r(p) = Delta_true(p) - Delta_canonical(p),
r(0)=r(1)=0,
|r(x)-r(y)| <= L |x-y|,
```

the exact closed-band nondetection threshold at an interior frequency is

```text
b(p) = 2[e_h + (1-p)e_u + p e_v].
```

Define two summary quantities

```text
B     = b(1/2) = 2e_h + e_u + e_v,
d     = 2(e_v-e_u),
delta = |d|.
```

`B` is the midpoint error floor. `d` is the signed slope of the nondetection threshold; `delta` is its magnitude.

## 1. Exact noise-dominated boundary

The endpoint anchors alone imply

```text
|r(p)| <= L min(p,1-p),
```

whose maximum is `L/2` at `p=1/2`.

If

```text
B >= L/2,
```

then `b(p)` lies on or above the endpoint triangle everywhere. On `[0,1/2]`, both `b(p)-Lp` endpoints are nonnegative; on `[1/2,1]`, both `b(p)-L(1-p)` endpoints are nonnegative. Therefore no interior cone can lower the endpoint envelope anywhere.

Hence for every finite holdout count

```text
U_m = L/2,
```

and every strict interior placement ties. There is no unique optimal shift.

If `B<L/2`, then automatically

```text
delta < L,
```

because `e_u+e_v < L/2` and `delta=2|e_v-e_u| <= 2(e_u+e_v)`.

This is the informative regime below.

## 2. Minimax problem as exact interval coverage

For a candidate worst undetectable amplitude `U`, a holdout at `x` with threshold `b(x)` constrains the residual below `U` on

```text
[x-(U-b(x))/L, x+(U-b(x))/L].
```

The endpoint anchors cover

```text
[0,U/L] and [1-U/L,1].
```

Thus the minimax design is the smallest `U` for which these intervals cover `[0,1]`. In the informative regime `delta<L`, the left and right boundaries of a holdout interval move monotonically with its centre, so the unique optimum has no gaps and no redundant overlaps: every adjacent boundary touches exactly at the common height `U`.

## 3. Closed form under unequal endpoint errors

Because swapping `e_u` and `e_v` reflects `p -> 1-p`, solve only the orientation in which the `p=1` endpoint is noisier. Then

```text
b(p) = a + delta p,
a = B-delta/2,
q = (L-delta)/(L+delta),   0<q<1.
```

For `m>=1`, equal-height coverage gives

```text
p_1 = (2U-a)/(L+delta),

p_{i+1} = [(L-delta)p_i + 2(U-a)]/(L+delta).
```

The final right-boundary contact condition yields the sharp minimax value

```text
          L [ B(1-q^m) + (delta/2)(1+q^m) ]
U_m = ------------------------------------------------.
              (L+delta)(1-q^(m+1))
```

For `e_v>e_u`, the recurrence above is the unique optimal design. For `e_u>e_v`, reflect it:

```text
p_i(e_u,e_v) = 1 - p_{m+1-i}(e_v,e_u).
```

Therefore the minimax value depends only on `(B,delta)`; the sign of the endpoint-precision asymmetry determines only which way the design is reflected.

## 4. Exact reductions and shift direction

When `delta=0`, the expression has the continuous limit

```text
U_m = B + (L/2-B)/(m+1),
```

with the previously proved symmetric-error placement

```text
p_i = [iL + (m+1-2i)B] / [(m+1)L].
```

For `m=1`, unequal endpoint precision does **not** move the holdout:

```text
p_1 = 1/2,
U_1 = B/2 + L/4.
```

The asymmetry changes neither quantity because the one sample must balance the two endpoint-anchor gaps.

For `m>=2`, direct substitution of the recurrence shows that the design centroid moves toward the noisier endpoint:

```text
e_v > e_u  => mean(p_i) > 1/2,
e_u > e_v  => mean(p_i) < 1/2.
```

The interpretation is compensatory, not preferential: prediction uncertainty is wider toward the noisier endpoint, so minimax design shortens the unsampled geometric distance on that side.

## 5. Infinite-density error floor

As `m -> infinity`, `q^m -> 0`, giving

```text
U_inf = L(B+delta/2)/(L+delta)
      = 2L[e_h + max(e_u,e_v)] / [L+2|e_v-e_u|].
```

This is the sharp deterministic floor for arbitrarily dense interior-frequency measurement under the declared fixed error half-widths. A target nonlinearity at or below this floor cannot be guaranteed detectable merely by adding more distinct frequency settings.

For equal endpoint errors this reduces to the earlier floor

```text
U_inf = 2(e_h+e_endpoint).
```

## 6. Claim boundary

This theorem says how to place distinct interior frequency settings under bounded measurement error. It does not infer:

- a probability distribution for errors,
- statistical power or confidence,
- the number of biological replicates per frequency,
- finite-population fixation,
- mutation support,
- historical causation,
- or SCH/BALANCE/BITA validation.

Implementation: `src/asymmetric_frequency_holdout_detection.py`.
Tests: `tests/test_asymmetric_frequency_holdout_detection.py`.
