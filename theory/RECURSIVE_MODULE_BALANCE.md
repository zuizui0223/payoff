# Recursive module balance — every hard module split is a local SCH/BALANCE/BITA problem

The hard-module partition theorem reveals a direct recursive form of the three-world programme.

A candidate split of one existing module into two daughter modules has exactly the same weighted conflict geometry as the original two-function SCH model.

---

## 1. Candidate split as a coarse-grained shared-coordinate problem

Let one current module

```text
C=A union B
```

contain two proposed daughter groups.

Define daughter weights and weighted means

```text
A_A, mu_A,
A_B, mu_B.
```

While `A` and `B` remain one hard module, they are forced to share one module coordinate.

The exact loss recovered by allowing two independent daughter coordinates is

```text
L_node
=
[A_A A_B/(A_A+A_B)](mu_A-mu_B)^2.
```

This is formally identical to SCH's two-function quadratic conflict load, with daughter modules replacing individual functions.

---

## Theorem RMB1 — local split has an exact three-world classification

Suppose making one additional independently adjustable hard module costs

```text
kappa>0.
```

Because the hard split completely releases the daughter-module coordinate conflict,

```text
s_node=1
```

and therefore

```text
R_node=L_node.
```

The local architecture gap is

```text
Phi_node
=R_node-kappa
=L_node-kappa.
```

Hence:

```text
L_node=0
-> no coarse conflict between daughter modules;

0<L_node<kappa
-> recursive BALANCE:
   daughter means conflict,
   but keeping one shared module still pays better;

L_node=kappa
-> local architecture critical surface;

L_node>kappa
-> recursive BITA:
   splitting the module pays.
```

### Proof

`HARD_MODULE_PARTITION.md` proves that `L_node` is exactly the reduction in optimized loss produced by the split. Hard separation creates independent daughter coordinates, so the release fraction for this one coarse degree of freedom is one. Subtracting the added module cost gives the stated classification. QED.

---

## Corollary RMB1.1 — local reserve inside a retained module

For a retained candidate split with

```text
0<L_node<kappa,
```

define

```text
rho_node
=kappa-L_node>0.
```

This is the module-level BALANCE reserve: the amount by which split cost still exceeds recoverable daughter-module conflict.

Thus a retained module need not be conflict-free. It can be retained because its internal split remains inside a BALANCE domain.

---

## 2. Recursive interpretation of a module tree

A hard partition hierarchy can be read as repeated local questions:

```text
current module C
        |
        | propose A|B
        v
coarse SCH conflict L_node
        |
        +--> L_node<kappa
        |    keep C
        |    recursive BALANCE
        |
        +--> L_node>kappa
             split C
             recursive BITA
```

After a split, each daughter can be tested again using its own possible sub-splits.

This gives the three-world programme a recursive architecture interpretation:

```text
SCH
is not only conflict between original functions;
it can also measure conflict between aggregate module optima.

BALANCE
is not only one global middle world;
it can occur inside any retained module.

BITA
is not only one shared-to-differentiated transition;
it can occur repeatedly as modules subdivide.
```

---

## 3. Registered three-function example

For

```text
theta=(0,1,3),
a=(1,1,1),
```

the first coarse split

```text
{0,1}|{2}
```

has

```text
L_node=25/6.
```

Inside retained module `{0,1}`, the next split has

```text
L_node=1/2.
```

Therefore:

```text
kappa>25/6
-> whole system remains one module;

1/2<kappa<25/6
-> outer split pays,
   inner {0}|{1} split remains in recursive BALANCE;

kappa<1/2
-> both split levels pay,
   giving three independent modules.
```

This is exactly the hard-module phase diagram from `HARD_MODULE_PARTITION.md`.

At `kappa=1`, for example:

```text
outer split reserve condition:
25/6-1>0
-> split;

inner retained-module reserve:
1-1/2=1/2>0
-> keep {0,1} together.
```

Thus the final `{0,1}|{2}` architecture contains a real residual conflict inside `{0,1}` but remains optimal because that remaining conflict is not worth another module.

---

## 4. Important global caveat

The local split receipt is exact, but a generic global optimum over many possible partitions need not be obtainable by greedily applying one locally best split at a time.

Alternative partitions can compete, and optimal partitions for different module counts need not be assumed to form one observed historical tree unless that nesting is separately established.

Therefore:

```text
local node classification
= exact for a declared split;

global partition
= solve with the hard-module dynamic programme.
```

Do not infer historical split order from the global partition alone.

---

## 5. Relation to finite-coupling topology

In the hard split,

```text
s_node=1.
```

In a soft finite-coupling split or edgewise release, only part of the relevant conflict may be recovered, so the local architecture gap returns to

```text
Phi_node=s_node L_node-K_node.
```

Thus the recursive hard-module result is the complete-release endpoint of the more general SCH/BALANCE/BITA architecture rule.

---

## 6. Claim boundary

The weighted split identity is standard variance algebra. The contribution here is the cross-repository interpretation:

> every declared hard module split carries its own SCH conflict load, BALANCE reserve, and BITA crossing on the same common fitness scale.

This is a model-based recursive interpretation, not evidence that real module histories necessarily followed a binary split tree.
