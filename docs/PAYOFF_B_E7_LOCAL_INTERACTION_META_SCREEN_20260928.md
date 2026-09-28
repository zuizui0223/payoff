# PAYOFF-B E7 source screen — from E6 triangulation to a genuine multi-study local-interaction meta-analysis

Date: **2026-09-28**  
Status: **prospective source screen only; not canonical Paper 2 evidence**

## Why this is the next gate

E6 solved the largest immediate ecological weakness in Paper 2. The migratory-bird side now has a real effect-size meta-regression: 944 temperature-response rows from 28 studies and 279 species, with weaker temperature responsiveness in long-distance than short-distance migrants. The local side is also real, but it is still dominated by one exceptionally large German plant–pollinator dataset.

The next defensible escalation is **not** to pool “bird” and “pollinator” as if taxonomy were an experimental treatment. It is to build a multi-study local plant–pollinator estimate first.

The target question is:

> **Across independent local plant–pollinator systems, how strongly and how consistently does warming change partner phenology and relative timing?**

If this can be estimated with a common unit and dependence-aware uncertainty, Paper 2 can compare two independent empirical axes:

```text
within migratory birds:
    short-distance -> long-distance
    weaker temperature responsiveness with information distance

within local interactions:
    plant <-> pollinator
    magnitude and heterogeneity of temperature-driven response asymmetry
```

That is much stronger than a raw taxon comparison.

## Effect-size contract

Three estimands are kept separate.

### Tier A — direct synchrony response to temperature

`beta_sync_C`: days of relative timing per °C.

This is the cleanest local-information effect because it directly measures whether warming changes the temporal relation between interacting partners.

### Tier B — partner-response disparity

`delta_beta_partner_C = beta_pollinator - beta_plant`, in days per °C.

Both partner slopes must be estimated against a matched environmental exposure in the same system. A positive or negative value is interpreted relative to the sign convention of the phenology variable; the magnitude captures differential temperature sensitivity.

### Tier C — synchrony trend through time

`beta_sync_time`: days per decade.

Tier C is ecologically useful but is **not pooled** with Tier A or B. Time trends conflate warming with other long-term changes.

## Public-data source screen

The current source map contains multiple independent systems with public data:

- Freimuth et al. 2022 — Germany, 1,763 species; already reconstructed in E6.
- Bartomeus et al. 2013 — 46 years of apple flowering and native bee records; Dryad `10.5061/dryad.9g7d8`.
- Kehrberger & Holzschuh 2019 — one spring plant and two *Osmia* species across 11 temperature-gradient grasslands; Dryad `10.5061/dryad.5tq5dn6`.
- Kudo & Cooper 2019 — *Corydalis*–bumblebee mismatch over 19 years plus snow-removal experiment; Dryad `10.5061/dryad.q4fm37m`.
- Weaver & Mallinger 2022 — specialist bee *Habropoda laboriosa* plus *Vaccinium* hosts over a 117-year collection record; Dryad `10.5061/dryad.zcrjdfndn`.
- Stemkovski et al. — 67 bee species across 18 Rocky Mountain sites; Dryad `10.5061/dryad.t76hdr7zc`.
- Hall et al. 2026 — direct plant–pollinator synchrony, temperature and precipitation data along a dryland elevational gradient; Dryad `10.5061/dryad.j0zpc86s2`.

Kharouba et al. 2018 remains a useful external synthesis benchmark: 88 species in 54 pairwise interactions showed large recent shifts in the **magnitude** of synchrony but no consistent direction. It is not entered as 54 effect rows until the row-level source table and uncertainty can be pinned.

## Promotion rule

E7 is promoted only if at least **three independent local systems** produce the same Tier A or Tier B estimand with uncertainty and source-level reproduction.

The pooled model must retain study/system dependence, report weight concentration and leave-one-study-out sensitivity, and keep Tier C separate.

Until that happens, the current E6 wording remains the claim ceiling:

> local plant–pollinator systems provide an independent benchmark; the cross-system comparison is triangulation, not a causal taxonomic ranking.

## Why this is useful even if E7 fails

A failure to harmonize the systems is itself informative for paper architecture: it means the E6 result is already at the correct empirical ceiling, and Paper 2 should not bloat itself with a pseudo-meta-analysis.

The gate is therefore fail-closed: **common estimand first, pooled result second.**
