# Large-contrast numerical stability v1

The exact anti-phase temporal formulas are mathematically finite well beyond the range where direct evaluation of `sinh(d)` and `cosh(d)` is representable in binary64 arithmetic.

This repository therefore evaluates the large-`d` derivative and exact-optimum crossing using algebraically equivalent bounded ratios built from `tanh(d)` and `sech(d)^2 = 1 - tanh(d)^2`.

For the exact optimum crossing,

```text
R(d) = [sinh(d)^2 - d^2] / [d cosh(d) - sinh(d)]^2
```

is evaluated for large `d` as

```text
R(d) = [tanh(d)^2 - d^2 sech(d)^2] / [d - tanh(d)]^2.
```

The derivative is likewise divided through by `cosh(d)` before evaluation. These transformations do not change the mathematical estimand; they only prevent overflow in intermediate quantities.

Regression coverage includes `v = 300, 400, 1000`, where the previous direct-hyperbolic implementation overflowed even though the exact optimum remains finite and approaches `u*=1` from above.
