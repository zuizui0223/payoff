# Continuous architecture empirical handoff

The continuous PAYOFF model should be tested by estimating its upstream quantities before fitting the population architecture distribution.

## 1. Upstream receipts

For each biological system or environmental context, estimate on one common fitness scale:

```text
L
= shared-coordinate conflict load;

R(lambda)
= conflict loss recovered by a candidate coupling architecture;

r
= observed/constructed recovery coordinate;

C(r)
= architecture maintenance/development cost.
```

For the registered quadratic cost approximation,

```text
C(r)=c1*r+(kappa/2)*r^2.
```

The key empirical quantities are therefore

```text
c1
= local marginal architecture-cost slope near zero recovery;

kappa
= curvature of the cost-recovery relation.
```

The intrinsic prediction is

```text
r0=clip[(1-c1)/kappa,0,L].
```

Do not estimate `r0` from the architecture-frequency data and then call the prediction confirmed.

---

## 2. Frequency-dependent architecture interaction

The registered interaction kernel is

```text
H(r,q)=-gamma(r-q)^2.
```

Estimate `gamma` from pairwise or population-frequency manipulations that change the architectural difference among interactants while keeping intrinsic architecture quality controlled.

Interpretation:

```text
gamma>0  architectural mismatch is costly;
gamma<0  architectural mismatch is beneficial.
```

The critical prediction is

```text
gamma_branch=-kappa/2.
```

This should be predicted from independently estimated `kappa`, not located retrospectively from the observed transition.

---

## 3. Three empirical regimes

### Monomorphic partial architecture

Prediction:

```text
gamma>-kappa/2
```

and an interior intrinsic optimum should produce concentration near

```text
r0=(1-c1)/kappa.
```

### Threshold / broad neutral variance

Prediction:

```text
gamma approx -kappa/2.
```

The model predicts weak selection on architecture variance at fixed mean recovery near `r0`.

### Endpoint polymorphism

Prediction:

```text
gamma<-kappa/2.
```

The declared quadratic model predicts protected occupancy near

```text
r=0
and
r=L,
```

with differentiated-endpoint frequency

```text
p_D*
=
[2(1-c1)-(kappa+2gamma)L]
/[-4gamma L].
```

Intermediate architectures should have lower payoff against this endpoint mixture.

---

## 4. Strong falsification test

Estimate independently:

```text
L,
c1,
kappa,
gamma.
```

Then freeze the predictions

```text
r0,
gamma_branch=-kappa/2,
p_D* when gamma<-kappa/2.
```

Use separate population experiments or comparative systems to test:

```text
observed architecture mean ?= predicted mean,
observed variance regime ?= sign(kappa+2gamma),
observed endpoint frequency ?= predicted p_D*,
intermediate mutant invasion ?= predicted sign.
```

This is preferable to fitting `c1,kappa,gamma` jointly to one final architecture distribution.

---

## 5. Mapping back to measurable coupling

For the two-function quadratic bridge,

```text
R(lambda)
=L*ab/[ab+lambda(a+b)].
```

Therefore an observed partial recovery `r` implies

```text
lambda(r)
=ab(L-r)/[r(a+b)].
```

This makes the continuous architecture prediction measurable either on the recovery scale `r` or on the residual-coupling scale `lambda`.

For many-function graphs, use the numerical monotone inverse of the registered `R(lambda)` curve instead of forcing the two-function closed form.

---

## 6. What would falsify the registered model?

Strong failures include:

```text
selection gradient shifts with gamma even near monomorphic residents;

an interior architecture remains globally ESS when gamma << -kappa/2;

architecture variance rises when kappa+2gamma is strongly positive;

an endpoint mixture at predicted p_D* is invaded by intermediate recovery levels;

R(lambda) is not monotone along the proposed biological architecture path;

or cost and recovery cannot be placed on a common fitness scale.
```

Such failures should motivate a richer cost function, asymmetric interaction kernel, multiple coupling paths, state-dependent architecture costs, or nonquadratic architecture geometry rather than post-hoc reinterpretation of `gamma`.
