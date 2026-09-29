# PAYOFF-B greater snow goose information-deadline bridge

Date: **2026-09-29**  
Status: **published-input bridge; not a direct theorem test**

## Why this system matters

Greater snow goose now provides the closest located conjunction of two
ingredients needed by PAYOFF-B in one ecological lineage:

1. an experimental spring-migration perturbation whose duration changes later
   reproductive performance;
2. an independent reconstruction of how informative temperatures at successive
   stopovers are about later Arctic conditions.

A public Movebank study (`Greater snow goose migration`, study 1442516400)
adds individual GPS movement for 2019-2023, but this branch does not open a new
movement outcome.

## 1. The perturbation-duration result is strong but is not pure D

Legagneux et al. (2012; doi:10.1098/rspb.2011.1351) held 2,037 female greater
snow geese for 0-4 days during spring staging. Duration, not food treatment, was
associated with reproductive success, and the effect differed strongly among
years.

Published logistic coefficients for DAYS give the following descriptive
probabilities at the model reference mass:

| year | breeding context | beta_days | p(success), 0 d | p(success), 4 d | relative drop |
|---|---|---:|---:|---:|---:|
| 2007 | average | -0.37 | 0.142 | 0.036 | 74.4% |
| 2008 | highly favourable | -0.03 | 0.255 | 0.233 | 8.7% |
| 2009 | unfavourable | -0.38 | 0.203 | 0.053 | 74.0% |

The later Grandmont et al. (2023; doi:10.1111/1365-2435.14256) analysis
supports breeding suppression as the main downstream response and reports that
arrival date, laying date, clutch size and nesting success among birds reaching
the breeding grounds were not detectably shifted by captivity duration.

**Claim boundary:** captivity duration combines time lost with capture,
handling and captivity stress. It therefore supplies a
**D-like perturbation-cost anchor**, not an identified PAYOFF-B opportunity cost
D. The calculations above must not be inserted into q_wait as if D had been
measured.

## 2. The same system has a quantified information gradient

Resendiz-Infante & Gauthier (2024;
doi:10.3389/fbirs.2024.1307628) reconstructed temperature relationships along
the St. Lawrence -> Nunavik -> Baffin -> Bylot route over 1979-2018.

For genuinely later Bylot conditions, published correlations were:

| information location | later Bylot period | rho | Gaussian q bridge |
|---|---|---:|---:|
| St. Lawrence, 1 Apr-15 May | 30 May-15 Jun | 0.03 | 0.510 |
| St. Lawrence, 1-15 May | 30 May-15 Jun | 0.25 | 0.580 |
| Nunavik, 10-31 May | 30 May-15 Jun | 0.11 | 0.535 |
| Baffin, 20 May-5 Jun | 30 May-15 Jun | 0.35 | 0.614 |

The q values use the already declared PAYOFF-B secondary mapping

[
q=0.5+\arcsin(\rho)/\pi.
]

They are **model-conditional translations**, not measured sensory accuracy.

The empirical point does not depend on that translation: information about the
later breeding-site temperature is weak from southern stopovers and improves
only near the destination.

## 3. New theoretical consequence: the information deadline can itself be environmental

The goose perturbation experiment shows that the fitness consequence of the
same pre-breeding perturbation can be strongly context dependent. It motivates,
but does not prove, replacing a fixed waiting cost D by a context-specific cost

[
D(z).
]

If context z is known at the decision time, the exact threshold becomes

[
q_{wait}(z)
=
\frac{\max(A,L)+D(z)}{A+L},
]

provided (D(z)<R_0). Therefore

[
q_{wait}(z_2)-q_{wait}(z_1)
=
\frac{D(z_2)-D(z_1)}{A+L}.
]

This gives a new ecological prediction:

> **The same organism can have different information-use thresholds in
> different ecological contexts because the opportunity cost of delaying the
> decision changes.**

A harsher, more time-limited context can move the threshold upward even if cue
quality itself is unchanged.

## 4. Why this sharpens the original "unknown future" problem

For greater snow goose, southern temperature is a weak predictor of future
Bylot conditions, while the consequence of a spring perturbation was largest in
an unfavourable breeding year.

That combination suggests a stronger prospective mechanism:

[
\text{remote actor does not know the future state}
]

and may also not know

[
\text{how costly waiting will turn out to be in that future state}.
]

PAYOFF-B should treat this as a **state-dependent deadline hypothesis**, not as
an empirical conclusion from the goose studies.

## 5. The next direct test

The public Movebank study contains 75 GPS-tracked greater snow geese from
2019-2023. A legitimate next analysis would be registered before opening the
movement response and would ask whether local departure behaviour becomes more
temperature-contingent as independently reconstructed predictive information
increases along the route.

That analysis would still be a behavioural-uptake proxy unless a clean,
independent D can be identified. The current captivity experiment is not
sufficient for that promotion.

Thus the evidence ladder is now:

[
\text{exact deadline theorem}
>
\text{same-system perturbation-cost + information-quality bridge}
>
\text{prospective GPS cue-uptake test}
>
\text{future direct D-to-q threshold test}.
]
