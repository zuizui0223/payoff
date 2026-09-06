# Network extension — many functions and modular coupling

The two-function model has one residual coupling coefficient `c`. This note generalizes that idea to `n` fitness-relevant functions coupled through an arbitrary connected network.

The extension gives a direct mathematical interpretation of partial modularization: **functional coordinates are nodes; developmental/genetic/structural integration is a weighted coupling graph.**

## Setup

Let

```text
theta = (theta_1,...,theta_n)^T
```

be function-specific optima and

```text
A = diag(a_1,...,a_n),   a_i>0.
```

Let `G` be a connected weighted undirected graph on the functions with graph Laplacian `L_G`, so

```text
L_G is positive semidefinite,
L_G 1 = 0,
null(L_G)=span{1}
```

for a connected graph.

A differentiated architecture has one coordinate per function,

```text
x=(x_1,...,x_n)^T,
```

and loss

```text
D_lambda(x)
= (x-theta)^T A (x-theta)
+ lambda x^T L_G x,
lambda >= 0.
```

The second term penalizes disagreement between coordinates connected by residual integration.

For a weighted graph,

```text
x^T L_G x = sum_{i<j} w_ij (x_i-x_j)^2.
```

Thus `lambda` controls overall integration strength while the graph determines which functions remain coupled.

---

## Theorem N1 — unique network-coupled optimum

For every finite `lambda>=0`, the loss is strictly convex and has unique optimum

```text
x_lambda*
= (A+lambda L_G)^(-1) A theta.
```

The minimized loss is

```text
D_lambda*
= theta^T A theta
  - theta^T A (A+lambda L_G)^(-1) A theta.
```

### Proof

Expanding the objective gives

```text
D_lambda(x)
= x^T(A+lambda L_G)x
  -2 theta^T A x
  +theta^T A theta.
```

Because `A` is positive definite and `lambda L_G` is positive semidefinite,

```text
A+lambda L_G
```

is positive definite. Hence the objective is strictly convex. Setting its gradient to zero gives

```text
(A+lambda L_G)x=A theta,
```

and therefore the stated optimum. Completing the square yields the minimized value.

QED.

---

## Theorem N2 — integration strength monotonically destroys dimensional release

`D_lambda*` is nondecreasing in `lambda`.

If the graph is connected and the function-specific optima are not all equal, then `D_lambda*` is strictly increasing for every finite `lambda`.

Equivalently, recovery relative to the shared architecture is nonincreasing with integration strength.

### Proof by ordered objectives

For `lambda_2>lambda_1`, for every phenotype vector `x`,

```text
D_lambda2(x)
= D_lambda1(x)
+ (lambda_2-lambda_1) x^T L_G x
>= D_lambda1(x).
```

Taking minima over `x` gives

```text
D_lambda2* >= D_lambda1*.
```

For strictness, the envelope theorem gives

```text
d D_lambda*/d lambda
= x_lambda*^T L_G x_lambda*
>=0.
```

For a connected graph this derivative is zero only if `x_lambda*` is constant across all nodes. If `x_lambda*=z1`, the first-order condition becomes

```text
Az1=A theta,
```

because `L_G 1=0`, forcing `theta=z1`. Therefore when the optima are not all equal, `x_lambda*` cannot be constant for finite `lambda`, so

```text
x_lambda*^T L_G x_lambda*>0.
```

Hence the minimized loss is strictly increasing.

QED.

---

## Theorem N3 — endpoints recover full differentiation and the SCH shared world

At zero coupling,

```text
lambda=0
-> x_0*=theta
-> D_0*=0.
```

As coupling becomes arbitrarily strong,

```text
lambda -> infinity
-> x_lambda* -> theta_bar 1
```

where

```text
theta_bar = (sum_i a_i theta_i)/(sum_i a_i).
```

Moreover

```text
D_lambda* -> L_n
```

with

```text
L_n
= sum_i a_i(theta_i-theta_bar)^2
= [1/(sum_i a_i)] sum_{i<j} a_i a_j(theta_i-theta_j)^2.
```

Thus the network model continuously connects the fully differentiated world to the SCH shared-coordinate world.

### Proof

At `lambda=0`, the objective separates across coordinates and is uniquely minimized by `x_i=theta_i`, giving zero loss.

For `lambda -> infinity`, any sequence of minimizers with nonzero graph disagreement would pay an unbounded coupling penalty, while a constant vector always has finite loss. Hence every limiting minimizer must lie in

```text
null(L_G)=span{1}.
```

Among constant vectors `x=z1`, the remaining objective is

```text
sum_i a_i(z-theta_i)^2,
```

whose unique minimizer is the weighted mean `theta_bar` and whose minimum is `L_n` by Theorem 2 of `THEOREMS.md`.

QED.

---

## Corollary N3.1 — network recovery function

Define recovery from the shared conflict load by

```text
R(lambda)=L_n-D_lambda*.
```

For connected `G` with non-identical optima:

```text
R(0)=L_n,
R(lambda) strictly decreases with lambda,
lim_{lambda->infinity} R(lambda)=0.
```

With architecture cost `K`, define

```text
phi(lambda)=R(lambda)-K.
```

If

```text
0<K<L_n,
```

then there is a unique finite critical integration strength `lambda_crit` satisfying

```text
R(lambda_crit)=K.
```

Below it differentiation pays; above it integration remains favored.

### Proof

The endpoint and monotonicity results follow from Theorems N2-N3. Continuity follows from the inverse formula in Theorem N1 because `A+lambda L_G` remains positive definite for finite nonnegative `lambda`. Therefore `R(lambda)` continuously and strictly decreases from `L_n` to zero. For every `K` strictly between those endpoint values, the intermediate value theorem gives one crossing, and strict monotonicity makes it unique.

QED.

---

## Corollary N3.2 — architecture-cost ceiling

Because

```text
0 <= R(lambda) <= L_n,
```

if

```text
K >= L_n,
```

no degree of decoupling can produce a strictly positive static architecture gain.

This is the many-function form of the two-function ceiling `K>=L`.

---

## Theorem N4 — edge deletion cannot reduce the best pre-cost differentiated fit

Consider two coupling graphs on the same functions with Laplacians `L_1` and `L_2`. Suppose

```text
L_1-L_2
```

is positive semidefinite, meaning architecture 2 weakens/removes coupling without adding new coupling penalties. Then

```text
D_2* <= D_1*.
```

Thus deleting or weakening coupling constraints cannot worsen the optimized pre-cost trait fit. It may still fail to evolve if the architectural cost of that modularization exceeds the recovered loss.

### Proof

For every `x`,

```text
(x-theta)^T A(x-theta)+lambda x^T L_2 x
<=
(x-theta)^T A(x-theta)+lambda x^T L_1 x.
```

Taking minima preserves the inequality.

QED.

---

# Biological interpretation

This gives a hierarchy richer than simply `one trait` versus `two traits`:

```text
fully integrated network
        |
        | weaken selected edges / lower lambda
        v
partial modularization
        |
        | further dimensional release
        v
weakly coupled functional modules
        |
        v
near-independent function-specific coordinates.
```

The relevant evolutionary quantity is not the number of traits by itself. It is

```text
recovered conflict loss from changing the coupling architecture
minus
cost of maintaining/building that architecture.
```

The graph formulation therefore turns BITA's partial decoupling into a many-function modularity model while preserving SCH's conflict load as the fully integrated endpoint.

# PAYOFF game handoff

For any candidate network architecture `A_j`, optimize its phenotype first and obtain payoff `W_j*`. Those optimized architecture values can then be used as strategies in an evolutionary game.

For two architectures, PAYOFF's scalar baseline remains

```text
phi = W_D*-W_S*.
```

For more than two alternative modular architectures, the next extension is a multi-strategy replicator system in which each strategy corresponds to a different coupling graph or coupling strength.
