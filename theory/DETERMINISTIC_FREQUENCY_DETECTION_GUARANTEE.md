# Deterministic nonlinear-frequency detection under bounded measurement error

Status: exact worst-case design theorem for declared bounded-error and smoothness
contracts. This is **not** statistical power, a replication sample-size calculation,
or evidence that any natural population has a nonlinear frequency response.

## 1. Measurement contract

The endpoint-derived canonical PAYOFF line is

```text
Delta_lin(p) = (1-p)u - p v.
```

Let the true response be

```text
Delta_true(p) = Delta_lin(p) + r(p),
```

where `r(0)=r(1)=0`. Reported measurement centres obey deterministic bounds

```text
|u_hat-u| <= e_u
|v_hat-v| <= e_v
|y_hat(p)-Delta_true(p)| <= e_h(p).
```

The existing no-refit gate constructs the closed endpoint bands
`u_hat +/- e_u`, `v_hat +/- e_v` and the closed interior band
`y_hat +/- e_h`.

At interior frequency `p`, the endpoint-derived prediction band has half-width

```text
q(p)=(1-p)e_u + p e_v.
```

The sum of prediction and observation half-widths is

```text
W(p)=e_h(p)+(1-p)e_u+p e_v.
```

The observed centre difference from the predicted centre equals `r(p)+xi`, with
`|xi|<=W(p)`. Closed bands are disjoint exactly when that centre difference has
magnitude greater than `W(p)`. Therefore rejection is guaranteed for **every**
admissible measurement error iff

```text
|r(p)| > b(p),
b(p)=2 W(p).
```

The factor two is exact. One copy of `W` can adversarially move the centres toward
each other and the other copy is the combined closed-band radius. At equality the
bands can touch, so equality is not a guarantee.

## 2. Exact worst residual that can evade guaranteed detection

Assume a Lipschitz residual class

```text
|r(x)-r(y)| <= L|x-y|,
r(0)=r(1)=0.
```

For registered holdouts `p_i` with nondetection thresholds `b_i`, any response that
is not guaranteed rejected at those holdouts can satisfy

```text
|r(p_i)| <= b_i.
```

Add endpoint anchors `(0,0)` and `(1,0)`. Then every frequency satisfies

```text
|r(p)| <= min_j { b_j + L|p-p_j| }.
```

Hence define

```text
U = max_p min_j { b_j + L|p-p_j| }.
```

Then every residual with

```text
||r||_infinity > U
```

must force at least one holdout rejection, regardless of all admissible bounded
measurement errors.

This bound is exact. The nonnegative lower envelope

```text
r*(p)=min_j { b_j + L|p-p_j| }
```

is itself `L`-Lipschitz, has zero endpoint residuals, obeys every sample bound, and
attains `U`. Worst-direction endpoint errors can be chosen once for all holdouts
and interior errors independently so all closed bands remain non-rejecting. Thus
`U` is the actual deterministic nondetection ceiling, not only an upper bound.

Implementation: `worst_undetectable_lipschitz_amplitude(...)`.

## 3. Uniform-error minimax theorem

Now assume both endpoint margins have common half-width `e_E` and every interior
holdout has common half-width `e_H`. Every interior sample then has the same true-
residual nondetection threshold

```text
B = 2(e_E+e_H).
```

### Noise-dominated regime

Endpoint zeros alone imply

```text
||r||_infinity <= L/2.
```

If

```text
B >= L/2,
```

all noisy holdout cones lie above the endpoint-only envelope. No finite holdout
design improves the deterministic minimax ceiling:

```text
U_m = L/2.
```

All strict designs tie. Holdouts may still detect particular responses; they add
no worst-case guarantee for this declared class.

### Informative regime

If

```text
B < L/2,
```

measurement error changes the optimal placement. Let `m>=1`. To keep the cone
envelope below a candidate ceiling `U>=B`, a boundary gap can be at most

```text
g_boundary <= (2U-B)/L,
```

while an interior gap can be at most

```text
g_interior <= 2(U-B)/L.
```

There are two boundary gaps and `m-1` interior gaps, whose total is one. Therefore

```text
2(2U-B)/L + (m-1)2(U-B)/L >= 1,
```

which gives the sharp lower bound

```text
U_m >= B + (L/2-B)/(m+1).
```

Equality requires every gap constraint to saturate, yielding the unique minimax
frequencies

```text
p_i = [iL + (m+1-2i)B] / [(m+1)L],  i=1,...,m.
```

Thus

```text
U_m* = B + (L/2-B)/(m+1).
```

Consequences:

- `B=0` recovers exact equal spacing `p_i=i/(m+1)` and `U=L/[2(m+1)]`.
- `B>0` pulls the optimal holdouts inward: boundary gaps enlarge and interior gaps
  shrink because exact endpoint residual zeros are more informative than noisy
  interior checks.
- As `m -> infinity`, the deterministic ceiling approaches but never beats the
  irreducible floor `B`.

So simply adding an error constant to the zero-error covering-radius formula is
conservative but not minimax; the exact bounded-error design changes location as
well as the attainable ceiling.

## 4. Exact holdout-count inversion

Suppose the target alternative class is

```text
||r||_infinity >= A.
```

A deterministic guarantee requires the strict inequality

```text
U_m < A,
```

because closed-band contact at `U_m=A` can remain compatible.

If `A>L/2`, the target cannot occur in the declared endpoint-zero `L`-Lipschitz
class. If `A<=B`, or if `B>=L/2`, no finite number of holdouts can guarantee
rejection for every feasible target response.

For the informative nonvacuous regime

```text
B < A <= L/2,
B < L/2,
```

the minimum count is the smallest integer `m>=1` satisfying

```text
B + (L/2-B)/(m+1) < A.
```

Equivalently,

```text
m+1 > (L/2-B)/(A-B).
```

The implementation preserves the strict boundary exactly with rational arithmetic.
This is a **holdout-frequency count**, not the number of biological replicates per
frequency and not statistical power.

## 5. Signed-curvature one-point guarantee with error

For the stronger one-sign curvature class

```text
r'' >= kappa > 0
```

or

```text
r'' <= -kappa < 0,
```

the previous theorem gives the midpoint departure

```text
|r(1/2)| >= kappa/8.
```

At the midpoint the nondetection threshold is

```text
B_mid = 2[e_h + (e_u+e_v)/2].
```

Therefore the midpoint is guaranteed to reject iff

```text
kappa/8 > B_mid,
```

or equivalently

```text
kappa > 8 B_mid
      = 16[e_h + (e_u+e_v)/2].
```

Again equality is excluded because closed bands may touch.

## 6. Claim ceiling

These results convert explicit smoothness and deterministic measurement-error
bounds into falsification guarantees. They do not provide a probability of
detection, confidence level, frequentist/Bayesian power, biological replication
number, or a claim that the assumed `L` or `kappa` is known in a natural system.

The logical sequence remains

```text
reciprocal invasion endpoints
  -> canonical line
  -> predeclared error-aware holdout design
  -> no-refit interior measurements
  -> compatible / rejected.
```

Neither a successful nor a failed frequency-response check substitutes for SCH,
BALANCE, or BITA empirical validation, finite-population fixation evidence,
mutation-support identification, or historical causation.
