# PAYOFF-B barnacle-goose route variance-geometry result

Date: **2026-10-03**  
Status: **post-freeze descriptive audit; frozen GEB V2 and frozen lambda gates unchanged**

## Source

The analysis uses exactly the three highlighted fixed-transition datasets
already frozen for the barnacle-goose phase-retention programme:

- Svalbard R2→R4: 16 transitions, 15 individuals;
- Greenland R2→R3: 6 transitions, 6 individuals;
- Barents R1→R2: 12 transitions, 8 individuals.

The source artifact files and SHA256 values were frozen before opening the new
variance summaries in
\`data/payoff_b_barnacle_variance_geometry_contract_20261003.json\`.

No pooled goose effect is fitted.

## Descriptive identity

For each route, the existing model is

\[
E_{next}=a+\lambda E_{current}+\varepsilon.
\]

OLS with an intercept gives the exact sample-variance identity

\[
\boxed{
\rho_V
=
\frac{\operatorname{Var}(E_{next})}
{\operatorname{Var}(E_{current})}
=
\lambda^2+\omega,
}
\]

where

\[
\omega=
\frac{\operatorname{Var}(\varepsilon)}
{\operatorname{Var}(E_{current})}.
\]

\(\omega\) is a normalized residual-variance coordinate. It is not identified
as environmental process innovation.

## Results

| Flyway / route | n | \(\lambda\) | variance ratio \(\rho_V\) | \(\lambda^2\) | residual ratio \(\omega\) | linearly inherited fraction of destination variance |
|---|---:|---:|---:|---:|---:|---:|
| Svalbard R2→R4 | 16 | −0.1063 | **2.019** | 0.0113 | **2.008** | 0.006 |
| Greenland R2→R3 | 6 | +0.1307 | **0.0649** | 0.0171 | 0.0478 | 0.264 |
| Barents R1→R2 | 12 | +0.4941 | **0.578** | 0.2441 | 0.3341 | 0.422 |

### Svalbard

Incoming phase variance was 82.29 d² and destination variance was 166.17 d²:

\[
\rho_V=2.019.
\]

The individual-cluster bootstrap interval is wide,

\[
95\%\ CI=0.311\text{--}9.292,
\]

reflecting only 16 transitions. The key descriptive point is not significance:
the point estimate combines a near-zero / sign-reversing phase-retention slope

\[
\lambda=-0.106
\]

with **variance expansion**, not convergence.

Only about 0.6% of destination variance is represented by the fitted
\(\lambda^2\) component at the point estimate; the normalized residual
coordinate is 2.008.

### Greenland

Incoming variance was 155.94 d² and destination variance was 10.11 d²:

\[
\rho_V=0.0649,
\]

with cluster-bootstrap

\[
95\%\ CI=0.0065\text{--}0.5095.
\]

This route shows strong variance contraction together with low positive phase
retention (\(\lambda=0.131\)).

### Barents

Incoming variance was 771.17 d² and destination variance was 445.90 d²:

\[
\rho_V=0.578,
\]

with cluster-bootstrap

\[
95\%\ CI=0.294\text{--}1.409.
\]

The point estimate indicates moderate contraction, but uncertainty includes no
contraction. The phase-retention slope is much larger than in the other two
highlighted routes (\(\lambda=0.494\)).

## Main ecological result

All three highlighted barnacle-goose routes have

\[
|\lambda|<1,
\]

but they do **not** have a common variance geometry.

In particular:

> **loss of phase memory does not imply population synchronization.**

Svalbard is the boundary case. Incoming phase has little linear memory at the
next route stage and reverses sign on average, yet destination phase dispersion
is larger than origin dispersion. The old phase error has been overwritten, but
the population has not become more synchronized.

Greenland instead combines low memory with strong convergence. Barents retains
more incoming phase and shows intermediate dispersion.

Thus \(\lambda\) alone cannot rank “tracking quality,” “phase control,” or
“synchronization.”

## Relation to mule deer

The post-freeze Ortega reanalysis gives

\[
\rho_V=0.249,\qquad \lambda=0.107.
\]

Its normalized OLS residual coordinate is therefore

\[
\omega
=
0.249-0.107^2
\approx0.237,
\]

and only about 4.6% of destination phase variance is represented by the linear
incoming-phase component at the point estimate.

Mule deer and Svalbard geese can therefore both have low \(|\lambda|\), while
one shows a strong whole-route funnel and the other shows route-stage variance
expansion. This reinforces that memory loss and synchronization are separate
ecological dimensions.

The systems are not numerically pooled because their interval definitions,
phase reconstructions and biological contexts differ.

## Claim boundary

Licensed:

- mean phase retention and population phase dispersion are empirically
  separable coordinates;
- the same low-\(|\lambda|\) regime can coexist with either variance contraction
  or variance expansion;
- route-stage residual variation can dominate destination phase dispersion.

Not licensed:

- \(\omega\) is environmental process innovation \(Q\);
- Svalbard variance expansion proves poor information or failed control;
- Greenland contraction proves individualized Bayesian feedback;
- the three flyways are independent species-level replicates;
- post-freeze variance geometry changes any frozen barnacle-goose lambda result;
- any direct estimate of \(K\), \(g\), \(\phi\), \(r\), or \(D_{eff}\).
