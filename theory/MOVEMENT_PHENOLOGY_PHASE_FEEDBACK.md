# Monotone phase-error feedback generates phenological phase locking

Status: PAYOFF-B empirical/theoretical extension. This result is **not** part of the frozen active theorem paper and is not yet claimed as literature-novel.

## Setup

Let route position be (s), and let the environmental phenology front move locally at positive speed (c_e).

Define phenological phase error

[
E(s)=T_a(s)-T_e(s),
]

where positive (E) means the animal is late relative to the environmental wave and negative (E) means it is early.

Let

[
u(E)=rac{c_a(E)}{c_e}>0
]

be the animal/environment speed ratio as a function of current phase error.

Because

[
rac{dT_a}{ds}=rac{1}{c_a},qquad
rac{dT_e}{ds}=rac{1}{c_e},
]

phase error obeys

[
rac{dE}{ds}
=
rac{1}{c_a(E)}-rac{1}{c_e}
=
rac{1/u(E)-1}{c_e}.
	ag{1}
]

This is a kinematic identity.

## Theorem PF1 — monotone feedback phase locking

Assume:

1. (c_e>0);
2. (u(E)>0) is continuous and strictly increasing;
3. there exists a unique (E_*) such that (u(E_*)=1).

Then (E_*) is a globally asymptotically stable equilibrium of Eq. (1).

### Proof

If (E>E_*), strict monotonicity gives (u(E)>1). Hence

[
1/u(E)-1<0,
]

so (dE/ds<0): phase error moves downward toward (E_*).

If (E<E_*), then (u(E)<1), so

[
1/u(E)-1>0,
]

and (dE/ds>0): phase error moves upward toward (E_*).

At (E=E_*), (u=1), so (dE/ds=0).

Thus the vector field points toward (E_*) everywhere, making the equilibrium globally asymptotically stable. (square)

The stable phase does not have to be zero. The animal can preserve a characteristic lead or lag while still being perfectly phase-locked.

## Exponential feedback

The mule-deer source-data reanalysis motivates the empirical form

[
u(E)=u_0 e^{kappa E}.
	ag{2}
]

For (kappa>0), Eq. (2) is strictly increasing, so PF1 applies. The equilibrium is

[
E_*=-rac{log u_0}{kappa}.
	ag{3}
]

Therefore a fitted (u_0<1) does not imply chronic failure to track. It means the controller crosses (u=1) at a positive phase offset.

Substituting Eq. (2) into Eq. (1),

[
rac{dE}{ds}
=
rac{e^{-kappa(E-E_*)}-1}{c_e}.
	ag{4}
]

Near (E_*), let (arepsilon=E-E_*). Then

[
rac{darepsilon}{ds}
=
-rac{kappa}{c_e}arepsilon
+O(arepsilon^2).
]

The local e-folding correction distance is

[
ell=rac{c_e}{kappa},
	ag{5}
]

and the phase-error half-distance is

[
ell_{1/2}=rac{c_elog 2}{kappa}.
	ag{6}
]

This gives a second empirical quantity beyond the equilibrium phase: how much migration distance is required to correct phase error.

## Mule-deer calibration from published source data

Using the official source-data workbook for Ortega et al. (2023), the current observational fit gives approximately

[
log u
=
log(0.857)
+
0.01830,E_{m start},
]

with a strongly positive (kappa).

The implied crossover is

[
E_*approx 8.46 {m d},
]

meaning the fitted relative speed crosses (u=1) when animals are about eight days behind the remotely sensed green-wave peak.

Using the median annual fitted green-wave speed of approximately (5.61) km d(^{-1}), the local linearization gives

[
ellapprox 307 {m km},
qquad
ell_{1/2}approx 213 {m km}.
]

These are observational controller-scale summaries, not evolutionary constants.

## Relationship to the original PAYOFF-B theorem

The original PAYOFF-B paper asks:

> For a fixed movement rate in a periodic anti-phase environment, is there a unique rate maximizing long-run growth?

PF1 asks a different question:

> If movement rate itself changes in response to phenological phase error, when does the coupled animal–environment system restore a stable phase relationship?

Thus:

~~~text
PAYOFF-B1:
fixed movement rate
-> unique growth optimum under exact anti-phase switching

phase-feedback extension:
state-dependent movement rate
-> stable phase locking under monotone error feedback
~~~

The two results are complementary but should not be conflated.

## Empirical predictions

PF1 yields direct comparative predictions:

1. species or populations with (kappa>0) should correct phase error along migration;
2. larger (kappa) should produce shorter correction distances;
3. barriers that reduce the realized slope (du/dE) should weaken phase locking;
4. strongly predictable routes can maintain stable nonzero (E_*);
5. systems where animals modify the resource wave violate the exogenous-(c_e) interpretation and require coupled dynamics.

## Claim boundary

PF1 is a kinematic stability result under an assumed monotone feedback law. It does not prove that the feedback evolved by natural selection, that (E_*) maximizes fitness, or that the exponential response is universal.

Before publication as a theorem contribution, its novelty must be checked against migration-control, optimal-foraging, green-wave surfing, and pursuit/tracking theory.
