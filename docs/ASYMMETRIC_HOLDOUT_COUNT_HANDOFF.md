# PAYOFF asymmetric holdout-count handoff — 2026-09-08

The unequal-endpoint-precision design now has an exact inverse: given a target nonlinear residual amplitude `A`, return the minimum number of **distinct interior frequency settings** needed for a worst-case deterministic detection guarantee.

Use `required_asymmetric_holdout_count_for_amplitude(...)` with `A`, `L`, `e_u`, `e_v`, and `e_h`.

In the informative asymmetric regime define

```text
B = 2e_h+e_u+e_v,
delta = 2|e_v-e_u|,
q = (L-delta)/(L+delta),
U_inf = L(B+delta/2)/(L+delta).
```

For `U_inf < A <= L/2`, the exact count is the smallest integer satisfying

```text
q^m < T(A),

T(A) = [A(L+delta)-L(B+delta/2)]
       /[A(L-delta)+L(delta/2-B)].
```

The inequality is strict. If `T(A)=q^k` exactly, `k` settings are not enough; the answer is `k+1` because closed bands may touch at equality.

No finite count exists at or below `U_inf`. If `B>=L/2`, interior settings cannot improve the endpoint-only ceiling at all. Swapping endpoint precisions leaves the required count unchanged and only reflects the optimal locations.

This is a count of frequency settings, not biological replicates and not statistical power.

See `theory/ASYMMETRIC_HOLDOUT_COUNT_INVERSION.md` and `src/asymmetric_holdout_count.py`.
