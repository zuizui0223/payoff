# Empirical identification contract: triangular PAYOFF

Status: optional, conditional calibration route. The runnable witness is synthetic,
not a field-data fit. Existing architecture and population results are unchanged.

## Question and minimum measurements

Can matched payoff contrasts identify the two coordinates of the existing
triangular frozen-resident phase diagram, E=kappa*epsilon/alpha and g=-gamma/kappa?

Declare the architecture coordinate r (recovered conflict loss, NOT raw trait
colour), feasible length L, fixed external context, and one common payoff scale.
The coordinate must be reconstructed independently of the calibration responses.
Biological matching is a study-design assumption, not verified by a string label.

Use two different nonzero architectures to measure intrinsic contrasts:

    B(r)=pi(r,delta_r)-pi(0,delta_0)=alpha*r-kappa*r^2/2.

This assumes monomorphic/self interactions have H(r,r)=0 and that other changes
in background ecology do not confound the contrast. Holding focal architecture
at zero, use two distinct positive distances to measure interaction contrasts:

    A(d)=pi(0,delta_d)-pi(0,delta_0)
        =G*d^2*max(0,1-d/epsilon), G=-gamma>0.

Keep density, resource supply, measurement interval and payoff scaling matched.
The two interaction fit points must be inside support and have positive contrasts.
A positive contrast identifies support membership only in this declared exact
model; significance of a noisy estimate is a separate inference problem.

Two response contrasts per stage are an algebraic minimum, not a biological
sample-size recommendation. Replication estimates sampling uncertainty but does
not replace the requirement for distinct architecture/distance values.

## Explicit inverse map and a nonidentification witness

Both transformed responses are lines:

    B(r)/r=alpha-(kappa/2)*r
    A(d)/d^2=G-(G/epsilon)*d.

Thus intercept/slope identify alpha, kappa, G and epsilon=-G/slope in the declared
family. Repeated distances have rank one and are rejected. At a single distance
0.1, (G,epsilon)=(2,0.3) and (4,0.15) give the same interaction contrast: more
replicates of that same design cannot separate intensity from range.

If all payoffs have an unknown common positive multiplier c, fitted alpha,
kappa and G inherit c, but r*=alpha/kappa, epsilon, E and g do not. Therefore a
conditional dimensionless phase position can be identified without absolute
payoff calibration. Different unknown multipliers across the two stages do NOT
cancel; the common-scale requirement is essential.

## Holdout contract and refusal conditions

`calibrate_triangular` fits exactly the two predeclared points in each stage.
Additional coordinates are held out, never refitted. The qualified receipt needs
an intrinsic holdout plus interaction holdouts inside AND outside the inferred
support. Declare holdout coordinates and discrepancy tolerance before measuring
their responses; the software can check coordinate overlap, not actual chronology.

Without this coverage the status is `calibration_only`, with no phase report.
A failed holdout yields `holdout_inconsistent`, also with no phase report.
Nonfinite values, rank failure, incompatible coefficient signs or invalid interior
fit points are rejected. The existing phase theorem is used only for 0<E<1 and
an intrinsic optimum inside [0,L]. Other fitted regimes are explicitly unlicensed
by this particular phase implementation, not asserted biologically impossible.

A successful holdout check is compatibility with the declared family, NOT proof
of the kernel or a confidence interval. The module supplies no noisy-parameter
uncertainty, statistical power calculation, kernel identification across arbitrary
families, or causal identification without the matched-design assumptions.

## What remains unmeasured

The returned barrier concerns a payoff landscape with the resident background
held fixed. It is not a proof of trapping under an evolving resident population,
fixation, stochastic valley crossing, or realized evolutionary accessibility.
Mutation radius is always returned as unidentified. Parent-offspring or other
preselection transition measurements with known detection/censoring would be
needed for that separate process. The largest jump in a finite sample does not
prove a hard mutation-support bound.

## Reproduce

From repository root:

    python -m src.empirical_identification
    python -m pytest -q tests/test_empirical_identification.py

The synthetic exact witness recovers (alpha,kappa,gamma,epsilon)=(0.5,1,-2,0.3),
(r*,E,g)=(0.5,0.6,2). It passes the declared synthetic holdouts and falls inside
the frozen-resident barrier window. The test compares the classification with
`src.triangular_kernel_phase_curve.dimensionless_triangular_window`.

Implementation: `src/empirical_identification.py`.
Related theory: `theory/TRIANGULAR_KERNEL_PHASE_CURVE.md` and
`theory/SMOOTH_KERNEL_ACCESSIBILITY_ROBUSTNESS.md`.
