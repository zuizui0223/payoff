# Spatial and temporal transport of architecture payoff

## Abstract

Architecture payoff measured in one ecological context does not directly determine persistence in heterogeneous space or time. We study how local architecture margins are transported through migration and periodic environmental change. In space, invasion is governed by the principal eigenvalue of a dispersal-growth operator rather than by the mean local payoff alone. In time, additive forcing common to all patches produces no fluctuation premium beyond its mean, whereas source switching creates noncommuting seasonal operators and a positive temporal premium. For a symmetric two-patch anti-phase system, the Floquet exponent admits an exact closed form and the weak-contrast temporal premium has a unique finite migration optimum. The results identify when static architecture ranking survives transport and when space-time structure changes the evolutionary answer.

## 1. Spatial transport

Let `r_i` be patch-specific rare-type margins and `L_G` the graph Laplacian. Under conservative migration `m`, the invasion operator is

```text
A=diag(r)-mL_G.
```

Metapopulation invasion is determined by

```text
Lambda=lambda_max(A).
```

Thus a locally favorable architecture can be rescued or suppressed by connectivity even when the landscape mean gives the opposite static ranking.

## 2. Source-sink transition

For connected conservative migration, increasing `m` transports the principal growth rate away from the best local source toward the landscape-average regime. This produces migration thresholds separating local-source rescue from homogenized failure or success.

## 3. Temporal null case

If temporal forcing is additive and common to every patch,

```text
A(t)=A0+q(t)I,
```

then

```text
Lambda_temporal=lambda_max(A0)+mean(q).
```

Zero-mean common forcing therefore has no additional long-run effect. This provides a clean null against which genuinely spatiotemporal effects can be defined.

## 4. Source switching and Floquet premium

When relative patch quality changes through time, seasonal operators generally do not commute. In the symmetric two-patch anti-phase model,

```text
season A: (r_bar+x,r_bar-x)
season B: (r_bar-x,r_bar+x).
```

The long-run Floquet exponent is

```text
Lambda_F
=r_bar-m
+(1/tau) asinh[
  m/sqrt(m^2+x^2)
  *sinh(tau sqrt(m^2+x^2))
].
```

The temporal premium relative to the static mean is nonnegative in the registered model.

## 5. Finite optimal migration

For nonzero source contrast, the temporal premium has a unique finite migration maximum. In the weak-contrast limit,

```text
m_opt tau -> 1.6061152988...
```

and

```text
P_max ~= 0.13248753945 x^2 tau.
```

Intermediate migration therefore maximizes exploitation of alternating sources: too little migration prevents tracking, while too much migration erases spatial contrast.

## 6. Discussion

The spatial and temporal results sharpen a general transport principle. Local architecture payoff is an input, not an evolutionary conclusion. Space converts local margins into a spectral growth problem, and time converts sequential environments into a Floquet problem. Static ranking survives only in special commuting or homogenized limits.

## Scope after SLK integration

SLK stops at minimal accessibility, invasion, fixation, and weak-mutation occupancy needed for the flagship architecture hierarchy. The present paper owns the deeper spatial and temporal transport theory, including the spectral and Floquet results.
