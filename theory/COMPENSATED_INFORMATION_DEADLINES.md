# PAYOFF-B compensated information deadlines

Date: **2026-09-29**  
Status: **exact reduction plus linear closed form**

## Motivation

The information-deadline theorem uses an opportunity cost (D) for waiting
until a later cue becomes available. For a migrant, however, a one-day delay at
a staging site need not cause a one-day delay at the breeding site. An animal
may shorten later stopovers or travel faster.

The quantity entering the theorem should therefore be the **fitness-equivalent
cost remaining after optimal downstream compensation**, not raw elapsed time.

This distinction is empirically important in greater snow goose. Bêty, Giroux
& Gauthier (2004) radio-tracked females between the southern Quebec staging
area and Bylot Island in 1997–1999. Across all females, later departure was
associated with shorter migration duration (Spearman (r=-0.35)); departure
date and arrival date were weakly related ((r=0.14)), whereas migration
duration and arrival were strongly related ((r=0.81)). These observations
show that raw departure delay and downstream arrival delay are not
interchangeable quantities. They do not by themselves estimate PAYOFF-B (D).

## Proposition — compensated deadline reduction

Let waiting for information create a raw temporal delay (deltage0).
After waiting, the actor can compensate by (c) time units, with

[
0le cle min(C,delta),
]

where (C) is compensatory capacity.

Let (K(c)) be the cost of compensation and (M(delta-c)) the fitness loss
from the residual timing delay. Define

[
oxed{
D_{mathrm{eff}}(delta,C)
=
min_{0le clemin(C,delta)}
left[
K(c)+M(delta-c)
ight].
}
]

If compensation and residual timing losses are additive to the cue-conditioned
Bayes risk, the original information-deadline theorem applies unchanged after

[
Dlongrightarrow D_{mathrm{eff}}.
]

Thus, when (D_{mathrm{eff}}<R_0),

[
oxed{
q_{mathrm{wait}}
=
rac{
max(A,L)+D_{mathrm{eff}}
}{
A+L
}.
}
]

This is the bridge between PAYOFF-B's previously separate **capacity** and
**information** layers: response capacity changes whether waiting for
information is costly enough to be worthwhile.

## Immediate consequences

Because zero compensation is always feasible,

[
D_{mathrm{eff}}le M(delta).
]

Increasing the feasible compensation set cannot increase
(D_{mathrm{eff}}). Therefore greater downstream compensatory capacity weakly
lowers the information-use threshold, all else equal.

For two actors,

[
Delta q
=
rac{
|D_{mathrm{eff},2}-D_{mathrm{eff},1}|
}{
A+L
}
]

whenever both thresholds are finite.

Consequently, actors can use the same cue asynchronously even when their raw
waiting time is identical. Heterogeneity in downstream compensation alone can
create different information-use thresholds.

The reverse warning is equally important: raw delay rankings need not equal
effective deadline-cost rankings. An actor that waits longer can still face a
smaller (D_{mathrm{eff}}) if it can cheaply recover more of the lost time.

## Linear closed form

Let

[
K(c)=kappa c,
qquad
M(r)=mu r.
]

Then

[
D_{mathrm{eff}}
=
min_c
left[
kappa c+mu(delta-c)
ight].
]

If (kappagemu), compensation costs at least as much as leaving the delay
unrecovered, so

[
c^*=0,
qquad
D_{mathrm{eff}}=mudelta.
]

If (kappa<mu),

[
c^*=min(C,delta),
]

and

[
oxed{
D_{mathrm{eff}}
=
kappamin(C,delta)
+
mumax(delta-C,0).
}
]

The information threshold therefore has a capacity kink. With
(S=A+L),

[
rac{partial q_{mathrm{wait}}}{partialdelta}
=
egin{cases}
kappa/S, & delta<C,\
mu/S, & delta>C,
end{cases}
qquad
(kappa<mu).
]

Before capacity is exhausted, raw delay raises the cue threshold only at the
marginal compensation cost. After capacity is exhausted, the threshold rises
at the full marginal timing-loss rate.

## Canonical numerical witness

Use the original PAYOFF-B loss scale

[
pi=0.4,quad C_F=2,quad C_M=1,
quad A+L=1.6,
quad max(A,L)=1.2.
]

For raw delay (delta=0.30), no compensatory capacity gives

[
D_{mathrm{eff}}=0.30,
qquad
q_{mathrm{wait}}=0.9375.
]

Now let (C=0.20), (kappa=0.20), and (mu=1). Optimal compensation is
(c^*=0.20), leaving residual delay 0.10:

[
D_{mathrm{eff}}
=
0.20(0.20)+1(0.10)
=
0.14,
]

so

[
q_{mathrm{wait}}=0.8375.
]

The same raw information delay therefore produces substantially different
information-use thresholds depending on downstream compensatory capacity.

Two actors with the same raw (delta=0.30), but capacities 0 and 0.20 under
these costs, have an exact asynchronous-window width

[
Delta q
=
rac{0.30-0.14}{1.60}
=
0.10.
]

## Ecological interpretation

This result changes the empirical target for (D).

A direct test should not estimate waiting cost from migration distance, days
spent waiting, or departure date alone. It should estimate the **incremental
expected fitness loss of waiting after optimal feasible downstream
compensation**.

In migration systems this means separately estimating:

1. the raw delay created by waiting for information;
2. how much delay can be recovered through speed, stopover compression,
   route changes or later phenological adjustment;
3. the energetic or survival cost of that compensation;
4. the fitness loss from residual arrival or breeding delay.

Greater snow goose is especially useful because historical tracking shows
substantial variation in migration duration and weak individual-level coupling
between departure and arrival timing, while independent Bylot data quantify a
strong timing-fitness surface. These pieces motivate the decomposition but do
not yet identify its terms on the same individuals.

## Relationship to hidden deadline states

If the residual timing-loss surface or compensation cost depends on a future
state (H), define the state-specific optimized cost

[
D_{mathrm{eff}}(H)
=
min_c
[
K(c,H)+M(delta-c,H)
].
]

When compensation can adapt after (H) becomes known but the wait/commit
decision occurs earlier, the information-deadline theorem uses

[
E[D_{mathrm{eff}}(H)midmathcal I].
]

If the compensatory action itself must be chosen before (H) is known, the
relevant cost is instead

[
min_c
E[
K(c,H)+M(delta-c,H)
midmathcal I
].
]

Because

[
E[min_c L(c,H)midmathcal I]
le
min_c E[L(c,H)midmathcal I],
]

later information that allows compensation to be state-contingent can itself
reduce the effective deadline cost.

This creates a second information value: information can help not only choose
the seasonal action, but also choose **how to compensate for having waited**.

## Claim boundary

The reduction is exact under the declared additive model. The greater-snow-goose
tracking evidence is only an ecological anchor for compensation and cannot be
used to assign numerical (C,kappa,mu) without an independently specified
fitness model.

In the downstream coordination game, the player-specific (D_i) should likewise be read as this effective cost whenever compensation is available; the strategic inequalities are otherwise unchanged.

The natural direct-test target becomes

[
oxed{
D_i^{mathrm{eff}}
ightarrow
q_{wait,i}
ightarrow
	ext{asynchronous cue use}.
}
]

Raw waiting duration alone is not the theorem's empirical predictor.
