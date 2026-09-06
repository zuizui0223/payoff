# Continuous-architecture prior-art boundary

The continuous architecture extension uses established ideas from adaptive dynamics, ESS theory, evolutionary branching, specialization, and phenotypic modularity. Those component ideas are not claimed as new.

## Established adaptive-dynamics framework

Geritz, Kisdi, Meszena & Metz (1998), **Evolutionarily singular strategies and the adaptive growth and branching of the evolutionary tree**, Evolutionary Ecology 12:35-57, DOI `10.1023/A:1006554906681`, gives the standard classification of singular strategies by convergence stability, ESS stability, mutual invasibility, and evolutionary branching.

Earlier work by Geritz, Metz, Kisdi & Meszena also developed invasion-fitness and branching arguments in adaptive environments.

PAYOFF therefore does **not** claim to invent:

```text
continuous strategy evolution,
evolutionarily singular strategies,
convergence stability,
disruptive-selection branching,
protected dimorphisms,
or endpoint polymorphism as a general evolutionary phenomenon.
```

## Established specialization / modularity theory

Rueffler, Hermisson & Wagner (2012), **Evolution of functional specialization and division of labor**, PNAS 109:E326-E335, DOI `10.1073/pnas.1110521109`, already develops general theory for functional specialization under performance trade-offs.

Phenotypic integration, modularity, and evolving pleiotropy are mature literatures.

PAYOFF therefore does **not** claim that partial modularity, specialization, or evolution of coupling strength are new concepts.

## PAYOFF-specific continuous bridge

The declared contribution is narrower:

```text
shared conflict load L
        |
        v
network release path R(lambda)
        |
        | monotone, so recovery itself is a valid coordinate
        v
continuous architecture r in [0,L]
        |
        v
cost C(r)=c1*r+kappa*r^2/2
        |
        v
intrinsic payoff b(r)=r-C(r)
        |
        v
symmetric architecture feedback
H(r,q)=-gamma(r-q)^2.
```

Within that registered quadratic model, PAYOFF derives the exact threshold

```text
gamma_branch=-kappa/2
```

from three equivalent receipts:

```text
1. mutant invasion curvature at the singular architecture,
2. variance curvature of the symmetric-game potential,
3. transition from monomorphic partial architecture to protected endpoint polymorphism.
```

The endpoint polymorphism then reduces exactly to the original two-strategy PAYOFF game with

```text
phi_endpoint=b(L)-b(0),
eta_endpoint=gamma L^2.
```

That recovery-coordinate bridge and exact reduction are the appropriate PAYOFF-specific claims.

## Claim ceiling

Preferred:

> We parameterize a continuous architecture path by recovered compromise loss and show that, under a quadratic architecture-cost schedule and symmetric quadratic mismatch feedback, the partial-modularity singular strategy loses evolutionary stability at `gamma=-kappa/2`.

Avoid:

> We discover evolutionary branching of modularity.

Preferred:

> In the declared potential game, sufficiently strong dissimilarity-favoring feedback produces a protected mixture of the fully shared and fully differentiated recovery endpoints.

Avoid:

> Negative frequency dependence universally forces organisms into two architectural extremes.

Preferred:

> The binary PAYOFF game is recovered exactly as the endpoint subgame of the continuous recovery model.

Avoid:

> All continuous architecture games reduce to the PAYOFF two-strategy matrix.
