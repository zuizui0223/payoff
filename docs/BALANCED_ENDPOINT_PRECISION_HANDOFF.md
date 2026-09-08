# PAYOFF reciprocal endpoint-precision balancing handoff — 2026-09-08

When the total deterministic error half-width across the two reciprocal invasion endpoints is fixed, the PAYOFF holdout design now has a sharp allocation rule.

Hold

```text
S = e_u+e_v,
e_h,
L,
m
```

fixed. In the informative regime `2e_h+S<L/2`:

- with one interior holdout, endpoint imbalance does not change the minimax ceiling;
- with two or more interior holdouts, the minimax ceiling is uniquely minimized by

```text
e_u=e_v=S/2;
```

- the arbitrarily-dense error floor is also uniquely minimized by equal endpoint precision.

So the asymmetric placement theorem's shift toward the noisier endpoint is compensatory but cannot fully erase the cost of endpoint precision imbalance.

Use `compare_endpoint_precision_balance(...)` to compare an observed/planned `(e_u,e_v)` pair with the same-total-error balanced counterfactual and report both the finite-design penalty and the dense-floor penalty.

This is a theorem about achieved error bounds. It does not imply equal biological replicate counts unless an independent effort-to-precision model maps replication to those bounds.

See `theory/BALANCED_RECIPROCAL_ENDPOINT_PRECISION.md` and `src/endpoint_precision_allocation.py`.
