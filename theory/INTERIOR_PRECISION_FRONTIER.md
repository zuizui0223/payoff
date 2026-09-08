# Exact interior-measurement precision frontier

Status: deterministic PAYOFF measurement-design theorem. It identifies an error-half-width requirement for a fixed number of distinct interior frequency settings. It is not statistical power and does not determine biological replicate counts.

## Setup

Fix:

```text
m       number of distinct interior frequency settings,
A       target nonlinear residual amplitude,
L       Lipschitz bound,
e_u     error half-width for u=Delta(0),
e_v     error half-width for v=-Delta(1).
```

Let the common interior-holdout error half-width `e_h` remain to be designed. Define

```text
S     = e_u+e_v,
delta = 2|e_v-e_u|,
B     = 2e_h+S.
```

For fixed `m,L,delta`, the sharp asymmetric minimax ceiling is affine in `B`:

```text
          L [ B(1-q^m) + (delta/2)(1+q^m) ]
U_m = ------------------------------------------------,
              (L+delta)(1-q^(m+1))

q=(L-delta)/(L+delta).
```

The equal-endpoint case `delta=0` is the exact limit

```text
U_m = B + (L/2-B)/(m+1).
```

Because closed-band contact is compatible, guaranteed detection of every declared alternative with `||r||_infinity >= A` requires

```text
U_m < A,
```

strictly.

## Asymmetric precision frontier

For `delta>0`, solve the inequality for `B`. The excluded critical value is

```text
             A(L+delta)(1-q^(m+1))/L
             - (delta/2)(1+q^m)
B_crit = ------------------------------------ .
                      1-q^m
```

Therefore the sharp interior precision requirement is

```text
e_h < e_h,crit = (B_crit-S)/2.
```

At `e_h=e_h,crit` exactly,

```text
U_m=A,
```

so a worst-case observation can still make the two closed bands touch. The boundary is excluded.

## Symmetric reduction

When `e_u=e_v`, `delta=0` and direct inversion gives

```text
B_crit = [(m+1)A-L/2]/m,

e_h,crit = {[(m+1)A-L/2]/m - (e_u+e_v)}/2.
```

Thus the asymmetric result continuously reduces to the registered common-endpoint-error design.

## Feasibility boundaries

Set `e_h=0`, so `B=S`, and let `U_m^(0)` denote the best finite-count ceiling attainable with perfect interior measurement but the declared endpoint errors unchanged.

If

```text
A <= U_m^(0),
```

then `B_crit<=S`. No nonnegative interior error half-width can guarantee the target with that fixed `m`. Equality is still impossible because the required inequality is strict.

If

```text
S >= L/2,
```

endpoint uncertainty alone is already noise-dominated: even perfect interior measurement cannot push the finite-design ceiling below `L/2`.

If `A>L/2`, the target lies outside the nontrivial endpoint-zero `L`-Lipschitz class rather than defining a meaningful detection requirement.

## Frequency count and precision are dual controls

For any fixed admissible `B`, the sharp minimax ceiling decreases as additional optimally placed frequency settings are added. Consequently, for a fixed target `A<L/2`, the excluded allowable interior-error frontier is nondecreasing with `m`, and strictly increases whenever the target is feasible and the finite design has not reached a limiting equality regime.

This gives two equivalent ex-ante ways to design PAYOFF frequency validation:

```text
fixed precision -> solve minimum m,
fixed m         -> solve maximum admissible e_h.
```

The previous asymmetric holdout-count theorem provides the first direction; this theorem closes the second.

## Dense-setting limit

As `m -> infinity`, `q^m -> 0`. The dense-design condition is

```text
L(B+delta/2)/(L+delta) < A,
```

or

```text
B < A(L+delta)/L - delta/2.
```

Hence even arbitrarily many frequency settings cannot compensate for interior error above

```text
e_h,infinity < [A(L+delta)/L - delta/2 - S]/2.
```

For balanced endpoint precision (`delta=0`) this reduces to

```text
e_h < (A-S)/2.
```

## Interaction with endpoint balancing

Holding `S=e_u+e_v` fixed while increasing endpoint imbalance `delta` raises the minimax nondetection ceiling for every informative `m>=2`. Equivalently, it lowers the admissible interior-error frontier for a fixed target. Thus balancing endpoint precision and tightening interior precision are complementary rather than interchangeable controls.

## Claim boundary

`e_h` is a deterministic error half-width on a common oriented payoff/growth-gap scale. Translating it into observations, individuals, blocks, effort, or monetary cost requires an independent measurement-error model. No probability, confidence level, statistical power, biological sample size, fixation result, mutation support, historical causation, or sister-program validation is inferred.

Implementation: `src/interior_precision_frontier.py`.
Tests: `tests/test_interior_precision_frontier.py`.
