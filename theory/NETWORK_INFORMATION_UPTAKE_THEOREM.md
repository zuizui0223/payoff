# PAYOFF-B network information-uptake theorem

Date: **2026-09-27**  
Status: **exact result for the declared shared-cue uptake model**

## From individual deadlines to a community boundary

The information-deadline theorem gives each actor an individual reliability
threshold for using a future cue. For actor (i), cue use begins when

[
V(q)>D_i,
]

where (V(q)) is the value of the shared environmental cue and (D_i) is the
opportunity cost of waiting for it.

At any cue quality (q), define the informed set

[
S(q)=\{i:D_i<V(q)\}.
]

As cue quality improves, (S(q)) grows monotonically. Ecological coordination,
however, need not improve monotonically.

## Theorem 1 — asynchronous information use is a network cut

Let the interaction network have nonnegative symmetric edge weights
(w_{ij}). Actors in (S(q)) condition their timing on the shared cue; actors
outside (S(q)) retain the prior-optimal timing convention.

When the cue-contingent action differs from the prior convention, exactly the
edges joining an informed to an uninformed actor are mismatched.

Define the weighted uptake cut

[
C(q)=
\sum_{i\in S(q)}
\sum_{j\notin S(q),,j>i}
w_{ij}.
]

Let total undirected interaction weight be

[
W=
\sum_{i<j}w_{ij}.
]

Then the expected fraction of interaction weight that is temporally mismatched is

[
oxed{
E(q)=M(q)\frac{C(q)}{W},
}
]

where (M(q)) is the probability that an informed actor's cue-contingent
action differs from the old convention.

Thus cue reliability affects mismatch through two distinct terms:

[
\text{cue-induced action difference}
\times
\text{network boundary between users and non-users}.
]

Cue quality alone is not sufficient.

## Theorem 2 — complete networks peak at intermediate uptake

For an unweighted complete network with (N) actors and (k) informed actors,

[
C=k(N-k),
]

and total edges are

[
W=\frac{N(N-1)}{2}.
]

Therefore the asynchronous edge fraction is

[
oxed{
\frac{C}{W}
=
\frac{2k(N-k)}{N(N-1)}.
}
]

It is zero when nobody or everybody uses the cue and is maximized when
information uptake is split as evenly as possible between the two states.

In a large randomly mixed population with informed fraction (f),

[
oxed{
P(\text{asynchronous pair})
=
2f(1-f),
}
]

which reaches its maximum (1/2) at

[
f=1/2.
]

The **network boundary** is therefore largest around half adoption.

The total ecological mismatch (E(q)) need not reach its numerical maximum
exactly at half adoption because (M(q)) can itself vary with cue reliability.
The half-adoption result applies exactly to exposure of interaction edges to
asynchronous information use.

## Theorem 3 — topology and deadline placement jointly determine disruption

Suppose an uninformed actor (i) crosses its information-use threshold while
the current informed set is (S).

The exact change in weighted cut is

[
oxed{
\Delta C_i
=
\sum_{j\notin S,,j\ne i}w_{ij}
-
\sum_{j\in S}w_{ij}.
}
]

The first term is newly exposed interaction weight; the second term is repaired
interaction weight.

Therefore:

- (Delta C_i>0): adoption worsens coordination;
- (Delta C_i=0): adoption moves the information frontier without changing
  total boundary weight;
- (Delta C_i<0): adoption repairs more mismatched interaction weight than it
  creates.

This gives an exact topological interpretation of decision deadlines.

An early adopter with many still-uninformed neighbours can create a large
coordination shock. The same delay-cost distribution placed on different nodes
can therefore generate different mismatch trajectories.

## Simple chain example

Take a five-node chain with four equal interaction edges.

At a cue quality where only one actor has crossed its waiting threshold:

- if the first adopter is a peripheral node, one of four edges crosses the
  information boundary:
  [
  C/W=0.25;
  ]
- if the first adopter is the central node, two of four edges cross the
  boundary:
  [
  C/W=0.50.
  ]

Nothing about the marginal distribution of waiting costs changed. Only the
assignment of deadlines to network position changed.

Thus:

[
oxed{
\text{deadline distribution}
+
\text{network placement}
\rightarrow
\text{coordination disruption}.
}
]

## Complete four-actor witness

With canonical seasonal losses

[
\pi=0.4,quad C_F=2,quad C_M=1
]

and delay costs

[
D=(0.05,0.15,0.25,0.35),
]

information value rises as cue reliability increases.

At low cue reliability only one actor uses the cue. At intermediate reliability
two actors use it, maximizing the complete-graph uptake cut. At perfect
information all four use the cue and the cut returns to zero.

This generalizes the two-actor zero-positive-zero mismatch pattern to a
community adoption frontier.

## Relation to the perfect-information trap

The uptake-cut theorem describes the transient **path into** information use.

The perfect-information coordination theorem describes a second stage: after an
information-using convention has collapsed, interaction can make first
re-adoption unprofitable even after (q=1).

The two results therefore form one sequence:

[
\text{improving / deteriorating cue}
\rightarrow
\text{actors cross individual uptake thresholds}
\rightarrow
\text{an informed--uninformed network cut appears}
\rightarrow
\text{coordination costs feed back on adoption}
\rightarrow
\text{information-use convention can collapse or lock in}.
]

## Comparative predictions

### Deadline variance

Greater dispersion in (D_i) spreads information uptake over a broader cue
range, increasing the opportunity for asynchronous network states.

### Network centrality

For a fixed set of delay costs, assigning lower (D_i) to highly connected or
bridge-like actors can increase the early uptake cut.

### Modularity

If early adopters are clustered within modules, much of their interaction
weight may remain internal to one information state, reducing the cross-state
cut relative to dispersed adoption.

### Perfect information is not the end of the problem

If some actors never find information worth its waiting cost, a nonzero uptake
cut can persist even at (q=1). Even when all actors would individually use a
perfect cue in isolation, strategic first-mover costs can preserve an obsolete
network convention after collapse.

## Claim boundary

This theorem assumes a common binary cue and identical state-dependent action
mapping among informed actors. Real ecological networks can contain
species-specific cues, correlated errors, directed interactions and continuous
timing.

The theorem does not claim that natural communities maximize mismatch at
exactly 50% cue uptake. It states that, under complete/random mixing, the
**interaction boundary between information users and non-users** is maximal at
half uptake.

The ecological novelty candidate is not generic diffusion or threshold adoption.
It is the connection between seasonal decision deadlines, cue reliability,
phenological mismatch and interaction-network cuts.
