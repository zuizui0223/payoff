# PAYOFF-B information-rescue coalition theorem

Date: **2026-09-27**  
Status: **exact result for the declared perfect-information shared-cue network**

## Why recovery needs a second theorem

The perfect-information coordination trap establishes that an obsolete
uninformed timing convention can remain a strict equilibrium after environmental
information has fully recovered.

That result answers:

> Why does spontaneous recovery fail?

The rescue theorem asks the complementary question:

> How much coordinated information use must be restored before recovery becomes
> self-sustaining?

The distinction matters because the answer is not generally "all species."

A small temporary informed seed can sometimes move the network across the
coordination barrier and then be released.

---

## Setup

Set cue accuracy to

[
q=1.
]

All actors initially use the same prior-optimal constant timing convention.

For actor (i), define:

- (R_i): prior state-mismatch risk under the old convention;
- (D_i): information / waiting cost;
- (I_i): interaction-mismatch strength;
- (p): probability of the state in which perfect information requires the
  action opposite to the old convention.

Let the interaction network have non-negative edge weights (w_{ij}), and let

[
s_i=sum_{j
e i} w_{ij}
]

be actor (i)'s total interaction weight.

---

## Proposition 1 — simultaneous voluntary coalition

Suppose a coalition (K) simultaneously switches from the old convention to
perfect cue use while all actors outside (K) remain old.

For member (iin K), define its remaining outside interaction fraction

[
b_i(K)
=
rac{sum_{j
otin K}w_{ij}}{s_i}.
]

Its payoff gain relative to the all-old state is

[
oxed{
G_i(K)
=
R_i-D_i-pI_i b_i(K).
}
]

Therefore coalition (K) is weakly self-financing exactly when

[
oxed{
R_i-D_i
ge
pI_i b_i(K)
quad
orall iin K.
}
]

It is strictly self-financing when every inequality is strict.

This makes the ecological meaning clear: coordinated adoption is easier when
coalition members internalize more of each other's interaction weight and leave
less mismatch exposure outside the coalition.

---

## Homogeneous complete network: exact voluntary coalition size

For an unweighted complete graph with (N) identical actors and a coalition of
size (k),

[
b(k)=rac{N-k}{N-1}.
]

Hence

[
oxed{
G(k)
=
R-D
-
pIrac{N-k}{N-1}.
}
]

Weak voluntary adoption requires

[
k
ge
N
-
(N-1)rac{R-D}{pI},
]

with the smallest feasible integer taken.

If (D>R), even the full coalition loses from information use and no voluntary
rescue coalition exists.

---

## Proposition 2 — temporary informed seed

Now suppose a set (S) is temporarily held in the informed state while all
other actors remain free to best respond.

For an uninformed actor (i
otin S), define the fraction of its interaction
weight already pointing to informed neighbours:

[
a_i(S)
=
rac{sum_{jin S}w_{ij}}{s_i}.
]

If (i) remains old, it keeps its state risk (R_i) and mismatches the informed
neighbours.

If it adopts the perfect cue, it pays (D_i), removes state mismatch, repairs
its interactions with (S), and creates mismatch with the still-uninformed
neighbours.

The exact adoption gain is

[
oxed{
H_i(S)
=
R_i-D_i
+
pI_ileft[2a_i(S)-1ight].
}
]

Under PAYOFF-B's path-preserving tie rule, actor (i) adopts spontaneously iff

[
H_i(S)>0.
]

Equivalently, for (I_i>0),

[
oxed{
a_i(S)
>
	heta_i
=
rac12
left[
1-rac{R_i-D_i}{pI_i}
ight].
}
]

Thus recovery from the information trap is a weighted threshold cascade whose
node threshold is not arbitrary: it is derived from seasonal risk, information
cost and interaction cost.

---

## Proposition 3 — rescue cascades are progressive

With non-negative edge weights, enlarging the informed set (S) cannot reduce
(a_i(S)) for any still-uninformed actor.

Therefore (H_i(S)) is non-decreasing as information use spreads.

Once a new actor adopts, it cannot make cue adoption less attractive to any
remaining old actor through the informed-neighbour term.

A seed that makes one outsider cross its strict threshold can therefore
nucleate a self-reinforcing recovery cascade.

This is the mechanism behind **singleton rescue seeds**.

---

## Homogeneous complete network: exact temporary seed threshold

With (N) identical actors in a complete graph and (k) temporarily informed
seeds,

[
a(k)=rac{k}{N-1}.
]

For an unseeded actor,

[
oxed{
H(k)
=
R-D
+
pIrac{2k-N+1}{N-1}.
}
]

Because

[
rac{partial H}{partial k}
=
rac{2pI}{N-1}>0,
]

recovery becomes easier after each additional adoption.

The strict temporary-seed threshold is the smallest integer (k) satisfying

[
oxed{
k
>
rac{N-1}{2}
left[
1-rac{R-D}{pI}
ight].
}
]

Once that threshold is crossed, the first unseeded actor benefits from
adopting; subsequent actors face still stronger incentives.

---

## Voluntary coalition and temporary seed are not the same object

A voluntary coalition requires every original coalition member to prefer
simultaneous cue use to the all-old state.

A temporary seed can instead be externally maintained long enough for other
actors to cross their best-response thresholds. Once the network reaches the
strict informed equilibrium, the temporary support can be removed.

Therefore:

[
oxed{
	ext{minimum voluntary coalition}

eq
	ext{minimum temporary rescue seed}.
}
]

This difference is especially important in heterogeneous networks.

---

## Canonical three-species PAYOFF-B result

At perfect information, the canonical system has:

[
R=(0.10,0.10,0.40),
]

[
D=(0.05,0.10,0.30),
]

[
I=(0.50,0.50,0.50),
]

and

[
p=0.40.
]

The all-old state is strict and spontaneous first adoption is unprofitable for
all three species.

### Voluntary simultaneous rescue

Under the complete and chain topologies, the minimum weakly self-financing
coalition contains all three actors.

Under the migrant-star, a two-actor weak coalition can exist when it includes
the migrant and either resident partner.

The canonical full three-actor coalition has gains relative to all-old:

[
(+0.05,;0,;+0.10).
]

It is weakly but not strictly self-financing because the local pollinator is
exactly indifferent.

### Temporary one-species rescue

A much sharper topology result appears when one actor is temporarily maintained
in cue use.

**Complete network**

Any one of the three actors can nucleate full recovery.

**Migrant-star**

Any one of the three actors can also nucleate full recovery.

**Chain**

[
flower
-
local pollinator
-
migrant
]

has a unique singleton rescue seed:

[
oxed{
local pollinator.
}
]

Temporarily restoring cue use in either peripheral species alone does not cause
full recovery.

Temporarily restoring cue use in the central local pollinator does.

After the other species switch, the intervention can be removed and the
fully-informed state persists.

This makes the central pollinator a **singleton rescue seed** in the declared
chain.

---

## Why topology matters for rescue even when it did not matter for trap existence

The symmetric all-old perfect-information trap exists across the tested
connected topologies because a lone spontaneous adopter initially disagrees
with all of its own neighbours.

Rescue is different.

Once one actor is externally held informed, each remaining actor sees a
different fraction of informed neighbours depending on network position.

Thus:

[
oxed{
	ext{trap existence can be topology-insensitive}
}
]

while

[
oxed{
	ext{minimum rescue intervention is topology-sensitive}.
}
]

This resolves an apparent tension between the perfect-information trap theorem
and the earlier topology-dependent memory result.

---

## Ecological prediction

If an interaction network becomes locked in an obsolete seasonal convention,
restoring environmental predictability everywhere may not be enough.

But neither is it necessarily necessary to shift every species directly.

The model predicts that temporary restoration of information use or timing
flexibility in a strategically placed interactor can trigger network-wide
recovery.

In sparse networks, the relevant target is not automatically the most mobile,
most abundant or most climate-sensitive species.

It is the actor whose informed state moves enough neighbours across their
derived adoption thresholds.

This suggests the empirical quantity:

[
oxed{
	ext{rescue leverage}
=
	ext{network-wide recovery caused by a temporary informed seed}.
}
]

---

## Prior-art boundary

Threshold cascades and seed-triggered network cascades are established ideas in
network science, including Watts' threshold-cascade model. Ecological network
research has likewise used keystone interactions, structural controllability
and critical nodes to identify species or interactions with disproportionate
effects on community state and recovery.

PAYOFF-B therefore does not claim generic threshold diffusion, influence
maximization, ecological controllability, or the existence of keystone network
positions as new.

Its candidate ecological contribution is the derivation of the node threshold

[
	heta_i
=
rac12
left[
1-rac{R_i-D_i}{pI_i}
ight]
]

from seasonal mismatch risk, decision deadline / information cost and
interaction strength, and the use of that threshold to connect:

[
environmental information
ightarrow
phenological convention
ightarrow
historical lock-in
ightarrow
minimum ecological rescue.
]

---

## Claim boundary

The rescue theorem is exact for the declared perfect-information shared-cue
network with normalized non-negative interaction weights.

A temporary pinned actor is a mechanism probe, not a literal management
prescription.

Natural singleton rescue seeds have not been empirically identified.

The result does not imply that manipulating one species is safe or desirable in
a real ecosystem.

It provides a testable theoretical prediction about which network positions can
catalyse recovery once environmental information has returned.
