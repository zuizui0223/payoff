# Balanced reciprocal-endpoint precision theorem

Status: deterministic measurement-design result for PAYOFF frequency-response validation. It concerns declared error half-widths, not biological replicate allocation or statistical power.

## Question

Suppose the total reciprocal-endpoint error is fixed:

```text
S = e_u + e_v,
```

and the interior holdout error `e_h`, Lipschitz bound `L`, and number of distinct interior frequencies `m` are also fixed. Is it better to make one reciprocal invasion assay very precise and tolerate a noisier opposite assay, or to balance their achieved error bounds?

Because

```text
B = 2e_h + e_u + e_v = 2e_h + S,
```

fixing the total endpoint error fixes the midpoint nondetection threshold `B`. Endpoint imbalance enters only through

```text
delta = 2|e_v-e_u|.
```

## Dimensionless representation

In the informative regime `B<L/2`, put

```text
b = B/L,
x = delta/L,
q = (1-x)/(1+x).
```

The sharp asymmetric m-point minimax value can be rewritten as

```text
U_m/L = 1/2 - (1/2-b) a_m(q),
```

where

```text
           (1+q)(1-q^m)
a_m(q) = ------------------
          2(1-q^(m+1)).
```

Equivalently, with `S_j(q)=1+q+...+q^j`,

```text
a_m(q) = (1+q) S_{m-1}(q) / [2 S_m(q)].
```

## One holdout is exactly imbalance-invariant

For `m=1`,

```text
a_1(q)=1/2
```

for every `q`. Hence

```text
U_1 = B/2 + L/4
```

is exactly independent of `delta`. This is the same midpoint invariance already seen in the asymmetric placement theorem: with one interior setting, the unique minimax frequency is `p=1/2` and endpoint imbalance cannot change the worst-case ceiling when the total endpoint error is fixed.

## For every m>=2, balance is the unique minimizer

Differentiate `a_m(q)`. After collecting powers,

```text
2 S_m(q)^2 a_m'(q)
  = sum_{k=0}^{m-2} (k+1) [q^k - q^(2m-2-k)].
```

For `0<q<1` and `m>=2`, every bracket is strictly positive because

```text
k < 2m-2-k.
```

Therefore

```text
a_m'(q) > 0.
```

But `q=(L-delta)/(L+delta)` is strictly decreasing in `delta`. Since `B<L/2` gives `1/2-b>0`, it follows that

```text
d U_m / d delta > 0
```

for every `delta>0` and every `m>=2`.

Thus, among all nonnegative `(e_u,e_v)` with the same sum `S`,

```text
e_u = e_v = S/2
```

is the unique minimizer of the finite-design worst undetectable amplitude whenever `m>=2` and the design is informative.

## Dense-design floor

The asymmetric dense-design floor is

```text
U_inf/L = (b+x/2)/(1+x)
        = 1/2 - (1/2-b)/(1+x).
```

For `b<1/2`, this is strictly increasing in `x=delta/L`. Therefore equal endpoint precision also uniquely minimizes the arbitrarily-dense deterministic error floor.

## Noise-dominated regime

If

```text
B >= L/2,
```

all finite designs have the endpoint-only ceiling `L/2`. Endpoint balancing cannot improve that ceiling because interior measurement is already noise-dominated. The unique-minimizer statement therefore applies only to the informative regime.

## Experimental interpretation

The theorem recommends equalizing the **achieved deterministic error half-widths** of the two reciprocal endpoint assays when that is feasible. It does **not** say to split biological replicates 50:50. Equal replicate counts would follow only from a separately justified mapping from effort or replication to the two error half-widths.

Implementation: `src/endpoint_precision_allocation.py`.
Tests: `tests/test_endpoint_precision_allocation.py`.
