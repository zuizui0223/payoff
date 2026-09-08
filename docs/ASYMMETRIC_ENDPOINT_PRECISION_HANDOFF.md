# PAYOFF asymmetric endpoint-precision handoff — 2026-09-08

The bounded-error interior-frequency design now allows the two reciprocal endpoint assays to have different deterministic precision.

Use `design_asymmetric_endpoint_lipschitz_detection(...)` with:

- `L`: declared Lipschitz bound for the nonlinear residual,
- `e_u`: error half-width for `u=Delta(0)` (rare D in S),
- `e_v`: error half-width for `v=-Delta(1)` (rare S in D),
- `e_h`: common interior-holdout error half-width,
- `m`: number of distinct interior frequency settings.

The design is controlled by

```text
B_mid = 2e_h + e_u + e_v,
delta = 2|e_v-e_u|.
```

If `B_mid >= L/2`, no finite interior design improves the endpoint-only worst-case ceiling `L/2`.

If `B_mid < L/2`, the minimax design is unique. Its worst undetectable amplitude depends only on `(B_mid,delta)`. Swapping the two endpoint precisions leaves that amplitude unchanged and reflects every recommended frequency through `p=1/2`.

A single holdout remains exactly `p=1/2` even under asymmetric endpoint precision. With two or more holdouts, the design centroid moves toward the noisier endpoint. This is compensation for the wider prediction band on that side.

The arbitrarily-dense deterministic floor is

```text
U_inf = 2L[e_h+max(e_u,e_v)] / [L+2|e_v-e_u|].
```

This remains measurement-design theory only. It is not statistical power, a biological replication count, or an empirical ecological result.

See `theory/ASYMMETRIC_ENDPOINT_PRECISION_HOLDOUT_THEOREM.md` and `src/asymmetric_frequency_holdout_detection.py`.
