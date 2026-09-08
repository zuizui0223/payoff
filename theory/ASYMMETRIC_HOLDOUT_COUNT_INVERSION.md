# Exact holdout-count inversion under asymmetric endpoint precision

Status: deterministic measurement-design theorem for the PAYOFF interior-frequency validation problem. This is not statistical power and the count below is not a biological replication count.

## Starting point

For an `L`-Lipschitz nonlinear residual with zero endpoint residuals, unequal endpoint error half-widths are summarized by

```text
B     = 2e_h + e_u + e_v,
delta = 2|e_v-e_u|.
```

In the informative regime `B<L/2`, the asymmetric minimax theorem gives `delta<L`,

```text
q = (L-delta)/(L+delta),  0<q<1,
```

and

```text
          L [ B(1-q^m) + (delta/2)(1+q^m) ]
U_m = ------------------------------------------------.
              (L+delta)(1-q^(m+1))
```

The deterministic dense-design floor is

```text
U_inf = L(B+delta/2)/(L+delta).
```

A target class means all admissible alternatives with

```text
||r||_infinity >= A.
```

Because the validation bands are closed, guaranteed rejection requires the strict condition

```text
U_m < A.
```

Equality is not sufficient.

## Exact inversion theorem

Write `t=q^m`. Rearranging `U_m<A` gives

```text
q^m < T(A),
```

with

```text
       A(L+delta) - L(B+delta/2)
T(A)= --------------------------------- .
       A(L-delta) + L(delta/2-B)
```

For

```text
U_inf < A <= L/2,
```

we have

```text
0 < T(A) <= 1.
```

Therefore the exact minimum number of distinct interior frequency settings is

```text
m_min = min {m>=1 : q^m < T(A)}.
```

Equivalently, as a real-number identity,

```text
m_min = floor[ log(T(A))/log(q) ] + 1.
```

The `+1` is essential at an exact equality boundary. If `T(A)=q^k`, then `m=k` only gives `U_k=A`, so closed prediction/observation bands may still touch and the guaranteed count is `k+1`.

The implementation deliberately avoids floating logarithms. It brackets and binary-searches the integer using exact rational comparisons of `q^m` with `T(A)`, preserving the strict boundary exactly.

## Limiting regimes

If

```text
A <= U_inf,
```

no finite count can guarantee detection: adding arbitrarily many distinct frequency settings cannot beat the asymmetric deterministic error floor.

If

```text
B >= L/2,
```

interior measurements cannot improve the endpoint-only minimax ceiling `L/2`, regardless of count.

If

```text
A > L/2,
```

the requested target amplitude is outside the declared endpoint-zero `L`-Lipschitz class, whose maximum possible sup-amplitude is `L/2`.

When `e_u=e_v`, `delta=0` and the theorem reduces exactly to the previously registered uniform-error count inversion.

## Reflection invariance

The count depends on endpoint precisions only through

```text
B = 2e_h+e_u+e_v,
delta = 2|e_v-e_u|.
```

Thus exchanging `e_u` and `e_v` leaves `q`, `T(A)`, `U_m` and `m_min` unchanged. Only the optimal frequency locations are reflected through `p=1/2`.

## Claim boundary

`m_min` counts **distinct interior frequency settings**. It does not determine observations, individuals, experimental blocks or biological replicates per setting. No probability model, confidence level, power, fixation result, mutation support, historical causation or sister-program validation is inferred.

Implementation: `src/asymmetric_holdout_count.py`.
Tests: `tests/test_asymmetric_holdout_count.py`.
