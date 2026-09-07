# Complete-candidate partition equilibrium audit

## Result and scope correction

The earlier `registered_three_function_phase` in `src/hard_partition_game.py`
is exact for the **restricted candidate set** `{S,M01,F}`. It is not the
complete partition game. Three labelled functions admit five, not three,
partitions. When the two omitted partitions are admitted, the registered
`theta=(0,1,3), a=(1,1,1), kappa=1` example has transitions at

```text
h = 1/2, 1, 13/6, where h=-gamma>0.
```

The second omitted two-module architecture invades the old solution for `h>1`.
The complete model has a four-architecture coexistence regime. This corrects
candidate-set scope, not the algebra of the earlier restricted model.

All numbers below are synthetic model results. They are not measured ecological
parameters or empirical demonstrations of historical architecture evolution.

## 1. Why KKT certificates are sufficient here

Let `c_i` be the binary pairwise co-membership feature vector of partition `i`,
`W=diag(w_e)>0`, `b_i` its intrinsic payoff and

```text
Q_ij = (c_i-c_j)^T W (c_i-c_j),
A_ij = b_i+b_j+h Q_ij, h>0,
V(p) = p^T A p, p in the simplex.
```

For any tangent vector `v` with `sum(v_i)=0`, expansion of squared distances gives

```text
v^T A v = -2h ||sum_i v_i c_i||_W^2 <= 0.             (1)
```

The intrinsic terms and separate squared feature norms vanish because `sum v=0`.
Thus `V` is concave on the simplex, although it need not be strictly concave.

The necessary and sufficient global optimum conditions are

```text
(Ap)_i = lambda = p^T A p  for p_i>0,
(Ap)_i <= lambda           for p_i=0.                (2)
```

Necessity follows by transferring mass from present strategies to any candidate.
For sufficiency, expand at a feasible `q`, writing `v=q-p`:

```text
V(q)-V(p) = 2 v^T A p + v^T A v <= 0.
```

The first term is nonpositive by (2), and the second by (1). Therefore every
accepted exact KKT solution is globally uninvadable **within the declared set**.
A small floating-point residual is a numerical check of (2), not an interval
proof of an empirical parameter estimate.

## 2. Co-membership means are unique; architecture frequencies need not be

For two global maximizers `p,q`, the midpoint identity is

```text
V((p+q)/2) - [V(p)+V(q)]/2
    = (h/2) ||sum_i(p_i-q_i)c_i||_W^2.
```

A strictly positive right side contradicts maximality. Hence every global
maximizer has the same co-membership mean `mu*=sum_i p_i c_i`. Also `b^T p` is
identical across maximizers, because

```text
V(p)=2b^T p+2h sum_e w_e mu_e(1-mu_e).
```

However, different distributions of whole architectures may realize that same
mean. Negative feedback alone does **not** identify a unique population mixture.

An explicit counterexample uses all five three-function partitions below, with
all intrinsic payoffs set to zero. In order `(S,M01,M02,M12,F)`, every

```text
p(t) = (t, 1/2-t, 1/2-t, 1/2-t, 2t-1/2),
1/4 <= t <= 1/2,
```

has `mu*=(1/2,1/2,1/2)` and maximal `V=3h/2`. The extremes are a two-strategy
`S/F` mixture and a four-strategy `S/M01/M02/M12` mixture. They cannot be
identified from pairwise co-membership means alone.

### Why singular KKT matrices do not invalidate support enumeration

Fix an optimum `p*`, and let `Z` be all candidates with payoff equal to its
mean. The entire optimal set is exactly

```text
{q >= 0: sum q=1, sum_i q_i c_i=mu*, support(q) subset Z}.  (3)
```

To prove this, use the expansion above. Zero potential difference requires both
zero off-support disadvantage and zero feature-mean displacement; these are
exactly (3). This is a compact polytope. Its extreme points have affinely
independent feature columns, so an extreme optimal mixture has support at most

```text
rank{(1,c_i)} <= 1 + n(n-1)/2.                         (4)
```

An affinely dependent support would allow a nonzero feasible signed direction
preserving total mass and features, contradicting extremality. Conversely, on
an affinely independent support (1) is strictly negative on nonzero tangents,
so the bordered KKT matrix is nonsingular.

Thus enumeration of these smaller supports covers the vertices even when the
full-support KKT system is singular. Coordinatewise minimum and maximum
frequencies over all optimal vertices give the exact ranges over (3). The
implementation reports their floating-point approximations and does not confuse
one sparse representative with the unique biological composition.

## 3. Full five-partition architecture game

Use the hard-sharing partition model: each module shares exactly one coordinate,
module-specific coordinates are optimized, and each extra module costs one.
The fully shared conflict is `L=14/3`.

| Name | Partition | Co-membership `(01,02,12)` | Intrinsic payoff `b` |
|---|---|---|---:|
| S | `{0,1,2}` | `111` | `0` |
| M01 | `{0,1}|{2}` | `100` | `19/6` |
| M02 | `{0,2}|{1}` | `010` | `-5/6` |
| M12 | `{0}|{1,2}` | `001` | `5/3` |
| F | `{0}|{1}|{2}` | `000` | `8/3` |

Payoffs are `b=L-within_partition_loss-(module_count-1)`. All pair weights are
one. These give the distance matrix in that order

```text
Q = [[0,2,2,2,3],
     [2,0,2,2,1],
     [2,2,0,2,1],
     [2,2,2,0,1],
     [3,1,1,1,0]].
```

### Exact equilibrium on the complete candidate set

With omitted coordinates interpreted as zero:

| Range of `h` | Positive-frequency strategies | Frequencies |
|---|---|---|
| `0<h<1/2` | `M01` | `1` |
| `1/2<h<1` | `M01,F` | `p_M01=1/2+1/(4h); p_F=1/2-1/(4h)` |
| `1<h<13/6` | `M01,M12,F` | `p_M01=1/2+1/(4h); p_M12=1/2-1/(2h); p_F=1/(4h)` |
| `h>13/6` | `S,M01,M12,F` | `p_S=1/2-13/(12h); p_M01=4/(3h); p_M12=7/(12h); p_F=1/2-5/(6h)` |

At each boundary the neighbouring formulas agree and the entering frequency is
zero. For `h=0` the unique intrinsic winner is `M01`.

### Proof, including every excluded strategy

Subtract the resident mean payoff. Present strategies have zero margin by direct
substitution. The absent-strategy margins are:

```text
M01-only regime:
    S:   2h-19/6
    M02: 2h-4
    M12: 2h-3/2
    F:   h-1/2

M01/F regime:
    S:   2h-19/6
    M02: h-7/2
    M12: h-1

M01/M12/F regime:
    S:   h-13/6
    M02: h-7/2

S/M01/M12/F regime:
    M02: -4/3.
```

All are nonpositive in their stated ranges. The positive support probabilities
sum to one. Thus (2) proves global optimality for every `h`.

Moreover, `M02` is strictly excluded in every regime. The remaining four feature
vectors `(111,100,001,000)` are affinely independent. Equation (1) is strictly
negative on that face, proving a **unique full-game equilibrium** in this fixture,
including at the three entry boundaries.

### Specific correction to the previous three-strategy extrapolation

Against the old `M01/F` equilibrium, omitted `M12` has margin

```text
h-1.
```

Against the old `S/M01/F` equilibrium it has constant margin

```text
7/12 > 0.
```

So the restricted solution is a full-game equilibrium only for `h<=1`. The old
entry boundary `19/12` for `S` is not preserved: with `M12` admitted, `S` enters
at `13/6` instead. At `h=2`, the full equilibrium is

```text
(S,M01,M02,M12,F) = (0,5/8,0,1/4,1/8),
```

whereas the restricted model assigns `S` the positive frequency `5/48`.

At strong feedback the full model still converges to the same endpoint limit,
`(S,F)->(1/2,1/2)`, with both two-module types vanishing like `1/h`. This limiting
agreement does not rescue the incorrect finite-feedback candidate restriction.

## 4. Population dynamics and accessibility boundary

For symmetric `A`, replicator dynamics increase `V`:

```text
dV/dt=2 sum_i p_i[(Ap)_i-p^T A p]^2 >= 0.
```

For the unique full-game equilibrium `p*` above, the relative entropy
`D(p*||p)=sum_{i:p*_i>0} p*_i log(p*_i/p_i)` has derivative

```text
dD/dt = (p-p*)^T A p
      = (p-p*)^T A p* -2h ||sum_i(p_i-p*_i)c_i||_W^2 <= 0.
```

Equality implies another global maximizer by (3), hence `p=p*` in this fixture.
This gives convergence from strictly positive initial candidate frequencies.
Mutation-free replicator dynamics do not introduce an architecture absent at
initialization. Therefore a restricted simulation can remain on a face whose
apparent equilibrium is invasible in the full strategy set.

## 5. Reproduction and numerical audit

```bash
python -m pytest -q tests/test_concave_partition_equilibrium.py
python scripts/audit_partition_equilibrium.py --output-dir outputs/full_partition_audit
```

Outputs are `five_partition_equilibria.csv` and `summary.json`. The runner checks
the closed forms independently of the KKT solve and tests old restricted mixtures
against every full-set invader. The JSON is labelled
`SYNTHETIC_MODEL_AUDIT_NOT_EMPIRICAL`.

The solver keeps the existing public entry point
`stable_negative_feedback_mixture`, removes a common payoff offset, normalizes
payoff scale before solving, and reports KKT residuals, all detected optimal
vertices, frequency ranges, and feature-mean agreement. Its default limit is 12
candidate strategies. All 5 partitions for 3 functions are included; larger
Bell-number sets require explicit limits and remain combinatorially expensive.
Input validation rejects nonfinite parameters, malformed/duplicate partitions,
and nonnegative gamma. Numerical certificates are conditional on tolerances.

## 6. Prior art and claim ceiling

Concave optimization, KKT sufficiency, feature-rank support bounds and stable
population games are established mathematics. Relevant primary sources are:

- Boyd & Vandenberghe (2004), *Convex Optimization*, Chapters 4-5:
  https://web.stanford.edu/~boyd/cvxbook/
- Hofbauer & Sandholm (2009), *Stable Games and their Dynamics*, Journal of
  Economic Theory 144:1665-1693, doi:10.1016/j.jet.2009.01.007. Author manuscript:
  https://users.ssc.wisc.edu/~whs/research/sg.pdf

The contribution here is the complete-candidate audit of the declared
architecture game, its exact four-phase formulas, and the distinction between
unique co-membership means and identifiable whole-architecture composition.
No first-theory claim or empirical promotion is made. Hard partition release
fraction `s_P=R(P)/L` remains a loss-recovery ratio; it is not the geometric
trait-separation fraction used in the two-coordinate residual-coupling model.
