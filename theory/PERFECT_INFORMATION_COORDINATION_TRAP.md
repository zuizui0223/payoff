# PAYOFF-B perfect-information coordination trap

Date: **2026-09-27**  
Status: **exact result for the declared shared-cue interaction game**

## Why this result matters

The information-deadline theorem shows when actors begin using a future cue.

The next question is strategic:

> If useful information is available to everybody, can interaction itself
> prevent the network from using it?

Yes.

The declared shared-cue game produces a stronger result than finite cue
reliability alone:

> **A seasonal interaction network can remain trapped in an obsolete uninformed
> timing equilibrium even when the cue has recovered to perfect accuracy and a
> coordinated informed equilibrium has higher joint payoff.**

The obstacle is not lack of information, lack of response capacity, or a noisy
cue. It is unilateral accessibility.

---

## Setup at perfect cue accuracy

Set

[
q=1.
]

Assume all players share the same prior-optimal constant action.

For player (i), define:

- (R_i): expected state-mismatch loss under that prior action;
- (D_i): cost of waiting for / acquiring the cue;
- (I_i): interaction-mismatch strength;
- (p): probability of the state in which the cue-contingent action differs
  from the prior action.

For a prior-late system,

[
p=\pi
]

and

[
R_i=\pi C_{M,i}.
]

For a prior-early system,

[
p=1-\pi
]

and

[
R_i=(1-\pi)C_{F,i}.
]

All interaction weights are normalized over a player's actual neighbours. If a
single player changes action while all its neighbours retain the old action,
its mismatch fraction is one in the state where the actions diverge.

---

## Proposition 1 — stability of the obsolete uninformed profile

If all players retain the prior-optimal constant action, player (i) has
payoff

[
U_i^{old}=-R_i.
]

If that player alone begins following a perfect cue while all neighbours remain
old, it removes state mismatch but pays the information cost and suffers
interaction mismatch whenever the cue requires the opposite action:

[
U_i^{first}
=
-D_i-pI_i.
]

The unilateral gain from becoming the first informed actor is therefore

[
oxed{
G_i^{first}
=
R_i-D_i-pI_i.
}
]

The old uninformed profile is a Nash equilibrium exactly when

[
oxed{
D_i+pI_i\ge R_i
quad
\forall i.
}
]

It is strict when all inequalities are strict.

Equivalently, the minimum interaction strength needed to block first adoption
is

[
oxed{
I_i^{old}
=
\max\left[
0,
\frac{R_i-D_i}{p}
\right].
}
]

---

## Proposition 2 — stability of the fully informed profile

If all players follow the perfect shared cue, there is no state mismatch and no
interaction mismatch. Player (i) pays only its information cost:

[
U_i^{info}=-D_i.
]

If that player alone reverts to the old constant action while all neighbours
follow the cue, it saves (D_i) but incurs both state mismatch and interaction
mismatch:

[
U_i^{revert}
=
-R_i-pI_i.
]

The fully informed profile is a Nash equilibrium exactly when

[
oxed{
D_i\le R_i+pI_i
quad
\forall i.
}
]

The minimum interaction strength needed to keep the informed state stable is

[
oxed{
I_i^{info}
=
\max\left[
0,
\frac{D_i-R_i}{p}
\right].
}
]

---

## Theorem — perfect-information bistability

Both the old uninformed profile and the fully informed profile are strict Nash
equilibria whenever

[
R_i-pI_i
<
D_i
<
R_i+pI_i
]

for every player, or equivalently,

[
oxed{
|D_i-R_i|<pI_i
quad
\forall i.
}
]

Thus the minimum interaction strength for strict bistability is

[
oxed{
I_i^{bi}
=
\frac{|D_i-R_i|}{p}.
}
]

This is a coordination result under **perfect environmental information**.

---

## Proposition 3 — when the informed equilibrium is jointly better

The old profile has joint payoff

[
U^{old}
=
-\sum_i R_i.
]

The fully informed profile has joint payoff

[
U^{info}
=
-\sum_i D_i.
]

Hence coordinated information use is better exactly when

[
oxed{
\sum_i D_i
<
\sum_i R_i.
}
]

Interaction strength does not enter this joint comparison because coordinated
cue use creates no interaction mismatch.

Interaction therefore changes **accessibility**, not the value of the
coordinated informed state.

---

## Perfect-information coordination trap

PAYOFF-B defines the strong trap as the conjunction:

1. the obsolete uninformed profile is a Nash equilibrium;
2. the fully informed profile has higher joint payoff.

A stronger bistable trap additionally requires the fully informed profile to be
a strict Nash equilibrium.

Therefore:

[
oxed{
\text{perfect information}
+
\text{better coordinated informed solution}
\not\Rightarrow
\text{evolutionary / strategic accessibility}.
}
]

---

## Canonical three-player witness

The shared-cue witness uses

[
\pi=0.4
]

and information costs

[
D=(0.05,0.10,0.30)
]

for flower, local pollinator, and migrant.

Their prior-late risks are

[
R=(0.10,0.10,0.40).
]

With interaction strength

[
I_i=0.50
]

for all three and

[
p=0.4,
]

the first-mover interaction penalty is

[
pI_i=0.20.
]

The unilateral information gains from the obsolete all-late state are

[
G^{first}
=
(-0.15,-0.20,-0.10).
]

So nobody wants to be first.

Yet

[
\sum R_i=0.60
]

while

[
\sum D_i=0.45,
]

so moving together to perfect cue use improves joint payoff by

[
oxed{0.15}.
]

At (q=1):

[
U^{old}=-0.60,
]

[
U^{info}=-0.45.
]

Both profiles are strict equilibria.

The minimum interaction strengths required for strict bistability are:

- flower: (0.125);
- local pollinator: (0);
- migrant: (0.25).

The declared value (I=0.50) lies strictly inside the bistable region.

---

## Information degradation creates historical lock-in

Start the canonical system in the fully informed profile at (q=1).

Reduce shared cue reliability in steps of 0.01.

The all-informed state persists through the exact stability boundary at

[
q=0.80
]

because the implementation retains the current policy at an exact tie.

At

[
q=0.79,
]

the migrant abandons cue use and the interaction network collapses to

[
late|late|late.
]

Now restore cue quality stepwise to

[
q=1.
]

The network remains

[
late|late|late.
]

At full recovery, the informed profile again has higher joint payoff, but the
old profile is itself strict and no player benefits from moving first.

Thus the same model gives

[
oxed{
information\ degradation
\rightarrow
collapse\ of\ information\ use
\rightarrow
perfect\ information\ recovery
\not\rightarrow
behavioural\ recovery.
}
]

This is a direct bridge from decision deadlines to ecological history.

---

## Relation to topology

For the canonical symmetric all-old versus all-informed comparison, complete,
chain, and migrant-star networks all give the same trap when every player has at
least one interaction partner and mismatch is normalized by connected
neighbours.

This is not a contradiction with the earlier topology result.

The two results answer different questions:

- **perfect-information acquisition trap:** whether coordinated cue use is
  strategically accessible at all;
- **topology-dependent ecological memory:** how heterogeneous timing states are
  stored once different players occupy different policies and cue qualities.

Topology is therefore most important for the structure of heterogeneous
historical states, whereas the symmetric acquisition trap can exist in any
connected interaction network.

---

## Ecological interpretation

The strong result is not "animals fail to perceive perfect information."

The model says:

1. obtaining / waiting for the information has a cost;
2. using it first creates a temporal mismatch with partners still following the
   old regime;
3. coordinated information use removes that interaction penalty;
4. therefore a high-payoff informed state can exist without being reachable by
   unilateral change.

A temporary period of poor environmental predictability can consequently
destroy an information-using convention. Restoring environmental predictability
alone may not rebuild it.

---

## Claim boundary

This theorem is exact for the declared shared binary cue game.

It does not imply that natural flowers, pollinators, or migratory birds literally
observe one common binary signal.

The canonical payoffs are mechanism probes, not fitted biological quantities.

Coordination traps under perfect information are established objects in game
theory. PAYOFF-B's ecological contribution is the connection between:

[
decision\ deadlines
\rightarrow
information\ acquisition
\rightarrow
seasonal\ interaction\ mismatch
\rightarrow
historical\ ecological\ state.
]

The natural network-hysteresis prediction remains prospective.
