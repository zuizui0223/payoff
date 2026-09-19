# Monotone phase-error feedback and phenological phase locking

Status: PAYOFF-B empirical/theoretical extension. This result is **not** part of the frozen active PAYOFF-B1 theorem paper. The stability algebra is elementary dynamical-systems/control theory and is not claimed as mathematically novel by itself.

## Setup

Let route position be \(s\), and let the environmental phenology front move locally at positive speed \(c_e\).

Define phenological phase error

\[
E(s)=T_a(s)-T_e(s),
\]

where positive \(E\) means the animal is late relative to the environmental wave and negative \(E\) means it is early.

Let

\[
u(E)=\frac{c_a(E)}{c_e}>0
\]

be animal movement speed relative to environmental-wave speed as a function of current phase error.

Because

\[
\frac{dT_a}{ds}=\frac{1}{c_a},
\qquad
\frac{dT_e}{ds}=\frac{1}{c_e},
\]

phase error obeys the kinematic identity

\[
\frac{dE}{ds}
=
\frac{1}{c_a(E)}-\frac{1}{c_e}
=
\frac{1/u(E)-1}{c_e}.
\tag{1}
\]

## PF1 — monotone feedback gives a stable phase

Assume:

1. \(c_e>0\);
2. \(u(E)>0\) is continuous and strictly increasing;
3. there is a unique \(E_*\) such that \(u(E_*)=1\).

Then \(E_*\) is globally asymptotically stable under Eq. (1).

### Proof

If \(E>E_*\), monotonicity gives \(u(E)>1\), hence

\[
\frac{1}{u(E)}-1<0
\]

and therefore \(dE/ds<0\).

If \(E<E_*\), then \(u(E)<1\), so

\[
\frac{1}{u(E)}-1>0
\]

and \(dE/ds>0\).

At \(E=E_*\), \(u(E_*)=1\) and \(dE/ds=0\).

Thus the vector field points toward \(E_*\) from both sides. \(\square\)

The stable phase does **not** have to be zero. A migrant can preserve a characteristic lead or lag while remaining phase-locked.

## Exponential feedback

The mule-deer reanalysis motivates

\[
u(E)=u_0e^{\kappa E}.
\tag{2}
\]

For \(\kappa>0\), PF1 applies. The crossing \(u=1\) occurs at

\[
E_*=-\frac{\log u_0}{\kappa}.
\tag{3}
\]

Substituting Eq. (2) into Eq. (1),

\[
\frac{dE}{ds}
=
\frac{e^{-\kappa(E-E_*)}-1}{c_e}.
\tag{4}
\]

Near \(E_*\), write

\[
\varepsilon=E-E_*.
\]

Then

\[
\frac{d\varepsilon}{ds}
=
-\frac{\kappa}{c_e}\varepsilon
+O(\varepsilon^2).
\tag{5}
\]

Define the local e-folding correction distance

\[
\ell=\frac{c_e}{\kappa}
\tag{6}
\]

and half-error distance

\[
\ell_{1/2}
=
\ell\log 2
=
\frac{c_e\log 2}{\kappa}.
\tag{7}
\]

These quantify how much migration distance is required to correct a small phase perturbation.

## Common phase-retention coordinate

The discrete STEP controller uses

\[
E_{i+1}=a+\lambda E_i+\epsilon,
\]

where \(\lambda\) is phase retention after one ecologically meaningful correction opportunity.

The continuous controller has the same local coordinate.

From Eq. (5), over a route segment of length \(L\),

\[
\varepsilon(s+L)
=
e^{-L/\ell}\varepsilon(s).
\]

Therefore the equivalent continuous-to-discrete phase-retention coefficient is

\[
\boxed{
\lambda(L)=e^{-L/\ell}
=
\exp\left(-\frac{\kappa L}{c_e}\right)
}
\tag{8}
\]

for a locally linear continuous controller.

Thus:

~~~text
continuous SURF controller:
  kappa, ell
  -> lambda(L) after a declared route length L

discrete STEP controller:
  lambda directly from arrival-to-arrival phase transfer
~~~

This is the common cross-system coordinate used by the empirical registry.

Importantly, the observation interval must be declared. A continuous controller does not have one intrinsic \(\lambda\) independent of route length.

## Mule-deer calibration

Using the official source-data workbook for Ortega et al. (2023), the observational fit is approximately

\[
\log u
=
\log(0.857)
+
0.01830\,E_{\rm start}.
\]

Thus

\[
\kappa\approx0.01830\ {\rm d}^{-1}
\]

and

\[
E_*\approx8.46\ {\rm d}.
\]

With median environmental-wave speed

\[
c_e\approx5.61\ {\rm km\,d}^{-1},
\]

the local correction scale is

\[
\ell\approx307\ {\rm km},
\qquad
\ell_{1/2}\approx213\ {\rm km}.
\]

The empirical start-to-end phase-compression regression independently gives a phase-retention estimate near

\[
\lambda\approx0.107.
\]

That empirical \(\lambda\) is preferred for direct registry comparison; Eq. (8) is the theoretical bridge explaining how a continuous controller generates a route-scale retention coefficient.

## Relationship to PAYOFF-B1

PAYOFF-B1 asks:

> For a fixed movement rate in an exactly anti-phase periodic environment, is there a unique rate maximizing long-run growth?

The phase-control extension asks:

> When movement changes in response to realized phenological phase error, how much of that error persists after the next correction opportunity?

The architecture is therefore:

~~~text
PAYOFF-B1
fixed movement rate
-> unique long-run growth optimum in a canonical periodic model

movement–phenology extension
state-dependent movement / stopover decisions
-> phase-error retention and correction
-> information + feedback uncertainty budget
~~~

The second is motivated by PAYOFF-B's timescale logic but is not a corollary of the fixed-rate theorem.

## Empirical predictions

The framework predicts:

1. stabilizing continuous controllers have \(\kappa>0\);
2. stronger local correction gives shorter \(\ell\);
3. stable discrete correction has \(|\lambda|<1\);
4. different actuator architectures can share similar \(|\lambda|\);
5. environmental predictability changes innovation variance and need not change \(\lambda\);
6. barriers can weaken realized correction by increasing \(|\lambda|\);
7. systems that modify their own resource wave require coupled animal–resource dynamics.

## Claim boundary

Licensed:

- Eq. (1) is a kinematic identity;
- monotone \(u(E)\) with one unit crossing produces a stable phase under the stated model;
- Eq. (8) maps a local linear continuous controller to phase retention over a declared distance;
- \(\kappa\), \(\ell\), and \(\lambda\) describe related but scale-dependent aspects of phase correction.

Not licensed:

- a claim that PF1 or exponential relaxation is new control mathematics;
- a claim that \(E_*\) maximizes lifetime fitness;
- a universal exponential behavioral rule;
- comparison of \(\lambda\) values measured over undeclared or biologically incomparable intervals.
