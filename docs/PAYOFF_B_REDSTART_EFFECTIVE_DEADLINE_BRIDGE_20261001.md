# PAYOFF-B American redstart effective-deadline bridge

Date: **2026-10-01**  
Status: **published-source mechanistic bridge; not a direct information-deadline test**

## Source

Dossman BC, Rodewald AD, Studds CE, Marra PP (2023).  
*Migratory birds with delayed spring departure migrate faster but pay the costs.*  
**Ecology** 104:e3938. DOI: **10.1002/ecy.3938**.

## Published result used

The published American redstart analysis reports that individuals departing
relatively late by about **10 days** migrated **43% faster** than earlier
departures, while the faster/delayed migration pattern was associated with a
reported **6.3% decrease in annual survival**.

## Licensed PAYOFF-B role

This result is a concrete natural example of why raw elapsed delay is not a
fitness-equivalent information deadline.

It jointly demonstrates:

1. **downstream temporal compensation** — initial departure delay can be partly
   offset by faster migration;
2. **compensation is not free** — reducing downstream timing delay can coexist
   with a fitness cost.

That is qualitatively consistent with

[
D_{eff}
=
J(\delta)+\min_c[K(c)+M(\delta-c)],
]

where compensation can reduce residual timing loss without forcing total
effective cost to zero.

## What it does not identify

The study does **not** estimate:

- natural waiting-for-information cost (J);
- the decomposition (K(c)) and (M(\delta-c)) on the PAYOFF-B fitness scale;
- total natural (D_{eff});
- cue reliability (q);
- actor-specific (q_{wait});
- a pairwise asynchronous information-use window;
- a decision to delay departure specifically in order to acquire information.

Therefore this source is a **mechanistic bridge for compensation-with-cost**,
not a direct empirical test of T2 or T3.

## Manuscript use

One compact sentence in Discussion 4.2 is licensed:

> American redstarts provide a concrete example of the distinction: birds
> departing about 10 days late migrated 43% faster, yet this compensatory
> pattern was associated with a 6.3% survival decrease (Dossman et al. 2023).

The interpretation must remain:

**raw delay can be behaviourally recovered while fitness cost remains.**

It must not be reframed as an estimate of (D_{eff}) or information use.
