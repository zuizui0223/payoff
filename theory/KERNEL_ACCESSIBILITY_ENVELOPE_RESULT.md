# Kernel-family accessibility envelope result

This note freezes the first explicit kernel-robustness result for the bounded
architecture-interaction extension.

The target is not one kernel's critical jump. It is whether a declared local
jump radius receives the **same accessibility classification across a plausible
kernel family**.

Implementation and regression guard:

```text
src/kernel_accessibility_envelope.py
scripts/kernel_accessibility_robustness_sweep.py
tests/test_kernel_accessibility_robustness_sweep.py
```

---

## Registered sweep

Fixed architecture geometry:

```text
alpha=0.5
kappa=1.0
L=1.0
161 grid bins
one-bin declared jump radius = 1/160 = 0.00625.
```

Kernel family:

```text
hard
triangular
cosine
gaussian.
```

Parameter grid:

```text
gamma in {-30,-20,-10,-5,-3,-2,-1,0}
epsilon in {0.05,0.10,0.20,0.30,0.40}.
```

Total:

```text
8 x 5 = 40 cells.
```

Each cell is classified as:

```text
all_accessible
  every declared kernel permits an all-uphill path with one-bin jumps;

all_trapped
  every declared kernel requires a jump larger than one bin;

kernel_sensitive
  the accessibility conclusion changes with kernel shape.
```

---

## Result

The frozen regression result is

```text
all_accessible     18 / 40
kernel_sensitive   21 / 40
all_trapped         1 / 40.
```

The sole robustly trapped cell in this registered grid is

```text
gamma=-30,
epsilon=0.05.
```

The test suite recomputes all 40 cells and requires these exact counts.

---

## Main inference

Within this declared family and grid, the dominant positive result is **not**
that finite interaction range generically creates a local evolvability barrier.
The dominant result is that the barrier classification is often sensitive to
the assumed interaction kernel.

```text
21/40 cells
-> kernel shape changes whether one-bin all-uphill evolution is accessible.
```

So a single hard-cutoff calculation is insufficient evidence for a
kernel-robust architecture barrier.

---

## Non-monotonicity warning

The robustness class is not monotone in either `|gamma|` or `epsilon` over the
registered grid. Very strong or broad feedback can make a locally favoured
architecture region itself globally competitive, removing the particular
all-uphill barrier rather than simply making the barrier larger.

Therefore do not use the shortcut

```text
stronger locality feedback
-> necessarily larger accessibility barrier.
```

The actual payoff profile must be checked.

---

## Why this helps PAYOFF

PAYOFF already separates

```text
global architecture value
from
local accessibility.
```

The present result adds another level:

```text
local accessibility under one assumed interaction kernel
!=
kernel-robust local accessibility.
```

A future empirical handoff can therefore report an interval or class over a
prospectively declared kernel family rather than hiding interaction-shape
uncertainty inside one arbitrary cutoff.

---

## Claim boundary

The `18/21/1` counts describe exactly the declared finite grid. They are not
biological prevalences and should not be generalized to arbitrary parameter
ranges, kernel families, mutation scales or architecture payoff functions.

The scientifically portable object is the procedure:

```text
choose a justified kernel family
-> compute delta_c for every member
-> report all-accessible / all-trapped / kernel-sensitive
-> only call the accessibility conclusion kernel-robust when the class is invariant.
```
