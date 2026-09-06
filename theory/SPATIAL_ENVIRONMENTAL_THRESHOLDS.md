# Spatial environmental thresholds under a common patch response

Let each patch have its own reference architecture gap

```text
phi_j0=s_jL_j-K_j
```

at environmental reference `e0`, while all patches respond to one environmental variable with the same slope `alpha`:

```text
phi_j(e)
= phi_j0 + alpha(e-e0),
alpha != 0.
```

Keep `eta_j` and the symmetric migration graph fixed.

This common-slope assumption is restrictive but powerful: environmental forcing adds the same scalar to every local static architecture gap, so the spatial invasion operator changes by a scalar multiple of the identity.

---

## Theorem 1 — exact environmental shift of the spatial invasion spectrum

At `e0`, define rare-D and rare-S local margins

```text
r_j,D0=phi_j0-eta_j,
r_j,S0=-phi_j0-eta_j.
```

The reference spatial operators are

```text
A_D0(m)=diag(r_D0)-mL_G,
A_S0(m)=diag(r_S0)-mL_G.
```

At environment `e`,

```text
A_D(e,m)
= A_D0(m)+alpha(e-e0)I,

A_S(e,m)
= A_S0(m)-alpha(e-e0)I.
```

Therefore their principal invasion exponents satisfy exactly

```text
Lambda_D(e,m)
= Lambda_D0(m)+alpha(e-e0),

Lambda_S(e,m)
= Lambda_S0(m)-alpha(e-e0).
```

### Proof

Adding `cI` to a matrix adds `c` to every eigenvalue without changing eigenvectors. Here the environmental shift is `+alpha(e-e0)I` for rare D and its negative for rare S. QED.

---

## Corollary 1.1 — exact spatial critical environments

The rare-D neutral environment is

```text
e_D(m)
= e0 - Lambda_D0(m)/alpha.
```

The rare-S neutral environment is

```text
e_S(m)
= e0 + Lambda_S0(m)/alpha.
```

For `alpha>0`,

```text
D invades when e>e_D(m),
S invades when e<e_S(m).
```

Thus the signed environmental interval between reciprocal spatial invasion boundaries is

```text
W_e,spatial(m)
= e_S(m)-e_D(m)
= [Lambda_D0(m)+Lambda_S0(m)]/alpha.
```

Interpretation for `alpha>0`:

```text
W_e,spatial>0
-> reciprocal-invasion environmental interval;

W_e,spatial<0
-> mutual-non-invasion / coordination environmental interval;

W_e,spatial=0
-> one common spatial transition.
```

The sign language reverses appropriately if `alpha<0`; the formulas themselves remain valid.

---

## Theorem 2 — migration compresses the signed reciprocal environmental window

For a connected undirected graph, the environment-mosaic theorem gives

```text
Lambda_D0(m)
```

and

```text
Lambda_S0(m)
```

as nonincreasing functions of migration rate `m`. Therefore, for `alpha>0`,

```text
W_e,spatial(m)
= [Lambda_D0(m)+Lambda_S0(m)]/alpha
```

is nonincreasing in migration.

If at least one reciprocal local-margin landscape is heterogeneous, the decline is strict over finite migration intervals where its principal exponent changes strictly.

### Interpretation

Migration does more than dilute one source patch. It systematically compresses the environmental separation between the two reciprocal landscape invasion thresholds under a common environmental response.

Depending on the strong-migration endpoint, increased migration can:

```text
shrink a reciprocal-invasion window,
collapse it to one transition,
or push it into a mutual-non-invasion coordination window.
```

---

## Corollary 2.1 — strong-migration limit

As `m->infinity`,

```text
Lambda_D0(m)
-> mean(phi_j0-eta_j)
= phi_bar0-eta_bar,

Lambda_S0(m)
-> mean(-phi_j0-eta_j)
= -phi_bar0-eta_bar.
```

Hence

```text
e_D(infinity)
= e0-(phi_bar0-eta_bar)/alpha,

e_S(infinity)
= e0+(-phi_bar0-eta_bar)/alpha.
```

The signed reciprocal width tends to

```text
W_e,spatial(infinity)
= -2 eta_bar/alpha.
```

Thus strong conservative mixing erases the contribution of patch-to-patch `phi` heterogeneity to reciprocal threshold separation; only the landscape-average frequency feedback remains in this limit.

---

## Theorem 3 — environmental heterogeneity alone creates a low-migration reciprocal-invasion window

Set

```text
eta_j=0
```

for every patch and take `alpha>0`.

At zero migration,

```text
Lambda_D0(0)=max_j phi_j0,
Lambda_S0(0)=max_j(-phi_j0)=-min_j phi_j0.
```

Therefore

```text
W_e,spatial(0)
= [max phi_j0-min phi_j0]/alpha.
```

This is exactly the range of patch static architecture gaps divided by the common environmental slope.

If the patch gaps are heterogeneous,

```text
W_e,spatial(0)>0
```

even though there is no frequency dependence at all.

As migration becomes strong,

```text
W_e,spatial(infinity)=0.
```

### Biological interpretation

Different patches cross their local shared-versus-differentiated architecture boundary at different environmental values. With weak movement, one part of the landscape can support rare D while another supports rare S, producing reciprocal spatial invasibility across a finite environmental interval.

This phenomenon must not be misidentified as negative frequency dependence: it arises from environmental mosaic structure alone.

---

## Corollary 3.1 — exact zero-migration local threshold range

For `eta_j=0`, each patch has local static environmental crossing

```text
e_j*
= e0-phi_j0/alpha.
```

The zero-migration reciprocal-invasion interval is exactly the span of these local architecture crossings:

```text
[min_j e_j*, max_j e_j*].
```

Its width is

```text
(max phi_j0-min phi_j0)/|alpha|.
```

Strong migration collapses the landscape onto the mean-gap crossing

```text
e_infinity*
= e0-phi_bar0/alpha.
```

---

## 4. Two-patch closed form

For two unit-coupled patches with reference rare-D margins

```text
r_1,D0,
r_2,D0,
```

the reference exponent is

```text
Lambda_D0(m)
= 1/2[r_1,D0+r_2,D0-2m
      +sqrt((r_1,D0-r_2,D0)^2+4m^2)].
```

Hence

```text
e_D(m)
= e0-Lambda_D0(m)/alpha.
```

An analogous expression holds for rare S after replacing the local margins by `r_j,S0`.

For a D source-sink pair with negative mean reference margin, `e_D(m)` rises monotonically with migration when `alpha>0`: stronger mixing requires a more D-favorable environment before differentiated architecture can invade.

---

## 5. Connection to the nonspatial environmental width

If all patches are identical,

```text
phi_j0=phi0,
eta_j=eta,
```

then migration and graph structure disappear from the principal exponents:

```text
Lambda_D0=phi0-eta,
Lambda_S0=-phi0-eta.
```

Thus

```text
W_e,spatial
= -2eta/alpha.
```

Its absolute value is the previous well-mixed environmental width

```text
2|eta|/|alpha|,
```

with the sign distinguishing reciprocal invasion (`eta<0`) from mutual non-invasion (`eta>0`).

So the spatial environmental theory strictly contains the earlier one-population environmental result as the homogeneous-patch special case.

---

## 6. Empirical prediction

A strong experiment can estimate or preregister:

```text
phi_j0=s_jL_j-K_j,
eta_j,
movement graph,
migration m,
common environmental slope alpha.
```

Then no spatial frequency data are needed to fit the transition location. PAYOFF predicts

```text
e_D(m)=e0-Lambda_D0(m)/alpha
```

and

```text
e_S(m)=e0+Lambda_S0(m)/alpha.
```

The test is whether rare architecture introductions switch sign at those independently predicted environmental values.

A particularly clean design varies migration while holding the patch environment response fixed. For `alpha>0`, the registered prediction is

```text
e_D(m) nondecreasing with m,
e_S(m) nonincreasing with m,
W_e,spatial(m) nonincreasing with m.
```

---

## 7. Claim boundary

The spectral shift identity itself is elementary linear algebra, and spatial environmental thresholds based on principal eigenvalues belong to established persistence theory.

PAYOFF's contribution is the cross-scale substitution

```text
phi_j0=s_jL_j-K_j
```

and the separation of reciprocal architecture invasion thresholds under environmental mosaic structure.

The common-slope assumption should be stated explicitly. If patches have different slopes `alpha_j`, the environmental forcing is no longer a scalar multiple of the identity and the exact threshold formulas above do not hold; the full parameter-dependent principal eigenvalue must then be evaluated.
