# PAYOFF deterministic nonlinear-frequency detection handoff — 2026-09-07

The interior-frequency holdout layer now has an ex-ante bounded-error guarantee.
This is distinct from statistical power.

For endpoint centre errors bounded by `e_u,e_v` and an interior centre error
bounded by `e_h`, the true nonlinear residual at frequency `p` must exceed

```text
b(p)=2[e_h+(1-p)e_u+p e_v]
```

in absolute value before closed-band rejection is guaranteed against every
admissible error realization. Equality can still produce band contact.

For an `L`-Lipschitz residual with zero endpoint residuals, an arbitrary registered
design is summarized by an exact worst undetectable amplitude

```text
U=max_p min_j {b_j+L|p-p_j|},
```

including endpoint anchors `(0,0)` and `(1,0)`. Any response with
`||r||_infinity > U` must reject at least one holdout; `U` itself is attainable by
an adversarial residual/error construction.

With common endpoint error `e_E` and common holdout error `e_H`, put

```text
B=2(e_E+e_H).
```

If `B<L/2`, the unique m-point minimax frequencies are

```text
p_i=[iL+(m+1-2i)B]/[(m+1)L]
```

and

```text
U_m=B+(L/2-B)/(m+1).
```

Zero error recovers equal spacing. Positive error pulls points inward. If
`B>=L/2`, noisy holdouts cannot improve the endpoint-only worst-case ceiling
`L/2` for this class.

`required_holdout_count_for_amplitude(...)` inverts this law using the strict
condition `U_m<A`. It returns no finite count when the target amplitude lies at or
below the irreducible error floor. The count refers to distinct interior frequency
settings, not biological replicates and not a probabilistic sample-size/power
calculation.

For the uniform signed-curvature alternative, the midpoint remains optimal. With
bounded errors it is guaranteed to reject only when

```text
kappa > 16[e_h+(e_u+e_v)/2].
```

See `theory/DETERMINISTIC_FREQUENCY_DETECTION_GUARANTEE.md` and
`src/frequency_holdout_detection.py`.
