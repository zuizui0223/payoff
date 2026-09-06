# Bounded-error phase identification for triangular PAYOFF

Status: optional extension, synthetic validation only. This does not change the
exact-calibration route or any publication claim. See
[the earlier observation contract](EMPIRICAL_IDENTIFICATION_CONTRACT.md).

## What the inputs mean

Declare a common payoff scale, matched context, fixed architecture coordinate r,
feasible length L, and the quadratic-intrinsic / triangular-interaction family.
Supply two distinct fit coordinates per stage, each as (coordinate, lower, upper).
These are **simultaneous bounds on the response**, not standard errors or an
automatic confidence region. Coordinate error, unmatched ecology, uncertain
kernel family, detection bias and common-scale failure are not represented.

For intrinsic responses B(r)=alpha*r-kappa*r^2/2, each response band is a strip
in (alpha,kappa). For positive interior interaction fit points,
A(d)=G*d^2-lambda*d^3, lambda=G/epsilon. These bands give strips in (G,lambda).
The two calibration strips form a parallelogram, possibly a segment or point.

Additional predeclared validation bands are intersected with these polygons by
exact rational half-plane clipping. The nonlinear support edge does not destroy
convexity: A(d)=max(0,G*d^2-lambda*d^3), so A(d)<=upper is a linear inequality when
upper>=0; a lower inequality is needed only when lower>0. An upper bound below
zero is incompatible with this model. This includes validation coordinates whose
support membership is initially uncertain.

**After assimilation, the validation bands are part of the conditioning data.**
They are not advertised as fresh independent validation of the resulting region.
They must not be used to pick the kernel, error bounds or context after seeing
which choice passes. Chronology and biological matching cannot be verified by
metadata strings. A further external validation would require unused data.

## Exact geometry before a conservative phase enclosure

Empty polygon intersections are `inconsistent_response_bands`, never vacuous
success. Otherwise a rational centroid supplies a feasible parameter witness.
If coefficient signs, positive interior fit support or the registered phase
domain cannot be certified across the set, the result remains unresolved.

Affine coefficient extrema occur at polygon vertices. Positive linear-fractional
ratios r*=alpha/kappa and epsilon=G/lambda also attain extrema at vertices. Thus
these marginal enclosures retain the pairing within each stage rather than
naively dividing separate coefficient intervals. The later enclosure in

    E=epsilon/r*,  g=G/kappa

is an outer rectangle and can lose correlations. A result labelled unresolved
means the enclosure cannot certify a uniform phase, NOT that two feasible phases
have necessarily been demonstrated.

Inside the registered domain 0<E<1 and r*<=L, the ridge/better-outside phase is

    g_on(E)<g<g_hi(E),   g_on(E)=1/E-1.

Both boundary curves decrease with E. For a box [El,Eh] x [gl,gh], sufficient
uniform certificates are therefore:

    barrier:       gl>g_on(El) and gh<g_hi(Eh)
    no ridge:      gh<=g_on(Eh)
    ridge superior or tied: gl>=g_hi(El).

The final case is not the same reason for no barrier as the second case.

## A square-root-free phase test

Define

    D(E,g)=2 E^2 (2g-1)^2 + 2E(18g-1)-27g.

This equals 4E^2/g times the cubic discriminant of

    p(x)-1/2 = -g*x^3/E + (g-1/2)*x^2 + x-1/2.

Once g>g_on(E), the unique positive local maximum lies inside (0,E); the negative
stationary point is a local minimum below zero. Therefore:

    D<0  <=> local ridge is below the outside optimum,
    D=0  <=> equal payoff contact,
    D>0  <=> local ridge exceeds the outside optimum.

For monotonicity of the upper curve, write
x=4E/(3+sqrt(9-8E)) and g_hi=1/2-2/x+3/(2x^2). Since dx/dE>0 and
(d/dx)g_hi=(2x-3)/x^3<0 for 0<x<1, g_hi decreases strictly.

The implementation evaluates the needed signs with Fraction arithmetic; it does
not decide a phase from a rounded square root. Displayed float enclosures round
outward. Decimal strings or Fractions preserve decimal values exactly; a float
preserves its actual binary value, not an idealized decimal. No denominator
limiting is used (Python standard-library `fractions` semantics).

## Qualification and limits

A reported phase requires new intrinsic validation coordinates plus interaction
validation coordinates known to be inside AND outside support throughout the
retained set, as well as a feasible witness. Missing coverage gives
`calibration_only_missing_holdout_coverage`; uncertainty does not become absence.

Common positive payoff rescaling cancels from E and g **only if response-error
bounds are rescaled by the same factor**. Different stage-specific scales do not
cancel. These deterministic bounds have no confidence level unless their joint
statistical coverage is justified separately.

The target is a frozen-resident payoff ridge with a better outside state. It is
not a certificate of trapping when the resident updates, fixation, stochastic
crossing time, or a hard mutation-support bound. Mutation radius stays unidentified.

## Registered synthetic example

For (alpha,kappa,G,epsilon)=(0.5,1,2,0.3), intrinsic fit r=(0.2,0.4), interaction
fit d=(0.05,0.15), and additional intrinsic r=0.6 / interaction d=(0.2,0.4):

- Exact responses recover E=0.6 and g=2.
- Uniform absolute response-error bounds +/-0.0001 give
  E in approximately [0.59419,0.60603] and g in [1.96816,2.03205]; the entire
  outer rectangle is in the declared barrier phase.
- Bounds +/-0.001 yield an unresolved outer rectangle. This is not "no barrier".

These tolerances are in synthetic payoff units, not a natural-system threshold.

## Reproduce

    python -m src.bounded_error_identification
    python -m pytest -q tests/test_bounded_error_identification.py

Files: `src/bounded_error_identification.py` and the corresponding tests. The
standalone cross-repository validation bundle also includes independently seeded
parameter-recovery and direct-extremum checks; finite synthetic tests do not
replace the conditional proofs above.
