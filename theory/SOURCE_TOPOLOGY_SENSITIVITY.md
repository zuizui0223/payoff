# Source topology and low-migration dilution

The environment-mosaic invasion operator is

```text
A(m)=diag(r)-mL_G,
```

where `r_j` is the local rare-architecture invasion margin and `L_G` is the undirected patch-graph Laplacian.

Suppose one patch `s` has a unique largest local margin:

```text
r_s > r_j
for every j != s.
```

At zero migration, the principal eigenvalue is simple:

```text
Lambda(0)=r_s
```

with eigenvector `e_s`.

## Theorem — initial migration sensitivity equals minus source degree

By first-order perturbation of a simple symmetric eigenvalue,

```text
Lambda'(0)
= e_s^T (-L_G) e_s
= - (L_G)_ss.
```

Since the diagonal Laplacian entry is the weighted degree of patch `s`,

```text
Lambda'(0)=-d_s.
```

Therefore

```text
Lambda(m)
= r_s - d_s m + O(m^2)
```

as `m -> 0+`.

### Interpretation

Two landscapes can contain an equally strong differentiated-architecture source patch but respond differently to weak migration solely because that source occupies a different network position.

```text
larger source weighted degree
-> more rapid first-order dilution of rare-architecture growth;

smaller source weighted degree
-> slower erosion of source advantage.
```

This is not a statement that isolation is always favorable. The full invasion exponent still depends on all sink strengths and graph structure, and the first-order approximation applies only near zero migration with a unique best source.

## PAYOFF substitution

For rare differentiated architecture,

```text
r_s
= phi_s-eta_s
= s_s L_s-K_s-eta_s.
```

Hence

```text
Lambda_D(m)
= s_sL_s-K_s-eta_s
  - d_s m
  + O(m^2)
```

when patch `s` is the unique best D source.

The same theorem applies to rare shared architecture using

```text
r_s^S=-phi_s-eta_s.
```

## Empirical use

A clean test compares landscapes or experimental movement graphs with the same local source margin but different source degrees. The preregistered prediction is the initial slope

```text
-d_s.
```

The theorem is standard symmetric-eigenvalue perturbation applied to the PAYOFF source-sink operator. The novelty claim remains the architecture-specific substitution of `sL-K-eta`, not eigenvalue perturbation theory itself.
