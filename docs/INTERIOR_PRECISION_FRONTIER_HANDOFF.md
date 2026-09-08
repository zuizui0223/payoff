# PAYOFF interior precision frontier handoff — 2026-09-08

The deterministic frequency-validation design can now be inverted in both directions.

Previously:

```text
fixed error bounds + target amplitude A -> minimum distinct frequency count m.
```

Now, with `m` fixed:

```text
fixed endpoint errors + target amplitude A -> strict maximum interior error half-width e_h.
```

Use `required_interior_precision_for_amplitude(...)` with `m`, `A`, `L`, `e_u`, and `e_v`.

For unequal endpoint precision, put

```text
S=e_u+e_v,
delta=2|e_v-e_u|,
q=(L-delta)/(L+delta).
```

The sharp excluded midpoint-threshold boundary is

```text
B_crit = [A(L+delta)(1-q^(m+1))/L - (delta/2)(1+q^m)]/(1-q^m),
```

and the common interior measurement must satisfy

```text
e_h < (B_crit-S)/2.
```

The inequality is strict: equality gives `U_m=A`, where closed bands may still touch.

If even `e_h=0` leaves `U_m>=A`, no nonnegative interior error bound can guarantee the target with the declared finite count. If endpoint error alone is noise-dominated, improving the interior assay cannot repair the design.

This is an error-half-width requirement on the common oriented PAYOFF scale. It is not a biological replicate count or a statistical power calculation.

See `theory/INTERIOR_PRECISION_FRONTIER.md` and `src/interior_precision_frontier.py`.
