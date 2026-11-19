# PAYOFF-B E6 — original primary-observation-source audit, 11/27 studies

Date: **2026-11-19**  
Status: **PARTIAL ORIGIN AUDIT ONLY**. `583/680` effect rows can be linked to eleven original articles with **named primary observational sources other than eBird**. This does **not** certify that every secondary input, species grouping, effect estimate, or table is fully eBird-free. Unreviewed sources are not assigned an origin by exclusion.

## Source base, frozen counts

The original Usui 2017 E6 derived table of 944 effect-size rows / 28 original studies / 279 species is pinned to the original 2026-09-28 GitHub Actions archive. Hurlbert & Liang 2012 explicitly used eBird checklists and supplies **264 effects**. See [forced source-policy correction](PAYOFF_B_E6_KNOWN_EBIRD_SOURCE_SENSITIVITY_20261119.md). After this whole study is excluded, **680 effects / 27 studies** remain.

Original source-paper and institutional repositories were checked for the observation data **used in the cited original study**. The following eleven studies each explicitly identify a distinct first-party observation source:

| Source original study | E6 effect rows | Published primary observation system (not eBird as named source) | Source |
|---|---:|---|---|
| Gordo & Doi 2012 | 130 | Japan Meteorological Agency (JMA) standardized phenology stations, 1953–2005 | [Climate Research 54:95](https://doi.org/10.3354/cr01099) |
| Murphy-Klassen et al. 2005 | 96 | Delta Marsh (Manitoba) 63-year local first-sighting series | [The Auk 122:1130](https://doi.org/10.1093/auk/122.4.1130) |
| DeLeon et al. 2011 | 93 | Buffalo Ornithological Society's 1967–2008 database | [The Condor 113:915](https://doi.org/10.1525/cond.2011.100223) |
| Marra et al. 2005 | 63 | Mist-net captures from three North American bird-banding stations | [Oecologia 142:307](https://pubmed.ncbi.nlm.nih.gov/15480801/) |
| Sokolov 2006 | 49 | Long-term passerine monitoring on the Curonian (Courland) Spit | [Original English edition](https://doi.org/10.1134/S0013873806010052) |
| Barrett 2011 | 42 | Troms regional ornithologists' first-arrival reports; supporting original observations archived in UiT Dataverse | [UiT source dataset](https://doi.org/10.18710/4MCRQL) |
| Kolářová & Adamík 2015 | 40 | 1828–1847 historical Bohemian Patriotic-Economic Society phenology network | [Climate Research 63:91](https://doi.org/10.3354/cr01290) |
| Hüppop & Hüppop 2003 | 24 | Helgoland standardized bird trapping/ringing station | [Royal Society B 270:233](https://pmc.ncbi.nlm.nih.gov/articles/PMC1691241/) |
| Jenkins & Sparks 2010 | 22 | David Jenkins' local Aboyne field records, Scotland | [NERC original monitoring report](https://nora.nerc.ac.uk/id/eprint/3392/) |
| Ellwood et al. **2010** | 22 | Historical Thoreau, Brewster, Griscom and Corey arrival observations through 2007 | [The Condor 112:754](https://doi.org/10.1525/cond.2010.100006) |
| Jones et al. 2012 | 2 | **Project FeederWatch**, a separately named citizen-science program | [Cornell FeederWatch source](https://feederwatch.org/explore/scientific-articles/the-early-bird-gets-earlier-a-phenological-shift-in-migration-timing-of-the-american-robin-turdus-migratorius-in-the-state-of-wisconsin/) |
| **Total** | **583** | **11** distinct original studies with identified alternative original observation data sources | |

Important classification nuance: the Ellwood 2010 study's input years end in **2007** and are explicitly historical naturalists' records; a **different 2025 follow-up** later combined those historical series with modern eBird data. This later follow-up does not retroactively establish that the 2010 study used eBird. Conversely, a named alternative primary data stream does not eliminate the need to examine each original study's full methods and any reused auxiliary input before certifying its derived E6 effect rows as fully eBird-independent.

For the 11 identified studies combined: **583 effects = 85.74%** of the 680 rows after excluding the confirmed eBird study. Remaining **97 effects (14.26%) from 16 source studies** still lack a paper-specific original-observation-source classification in this ledger. They remain **UNVERIFIED**, not silently labeled eBird-free or eBird-derived.

## What the executable inventory validates

`scripts/payoff_b_e6_source_origin_inventory.py` uses **only** the original checksum-verified GitHub archived E6 source-derived 944-row table. It matches each source study by an immutable bibliographic marker; validates expected count and exact one-study identity; excludes the known 264-row eBird study; guards against duplicate classifications; and requires a 583/97 split of the remaining 680 rows. It also reports distance-class counts for audit without fitting any new temperature-response coefficient, so effect signs or p-values **cannot influence source classification**. The companion tests and source-only GitHub Actions workflow ensure the same partition is reproduced in CI from the frozen artifact.

## Biological limits

- E6's **+0.608389 d/°C** adjusted migrant long-minus-short response in [PR #404](https://github.com/zuizui0223/payoff/pull/404) remains a **forced published source exclusion of one known eBird-based study**, not a newly discovered effect or independent test.
- The 583 effect rows are **not** promoted as a newly fit "eBird-free subset" merely because their published original observational source is identifiable. Further original full-method and secondary-stream checking is necessary, and the 16 unknown studies remain unverified.
- The dataset still lacks independent within-study crossing of temperature measurement site × migration-distance class, as shown in [PR #403](https://github.com/zuizui0223/payoff/pull/403). It cannot identify migration decision-time cue access, recourse value, or causal biological information distance.
- Do not change frozen Paper 2 or V7, claim biological hysteresis, import fresh eBird observations, or merge draft PRs as part of this audit.

## Reproduction

```bash
python -m scripts.payoff_b_e6_source_origin_inventory \
  --artifact-zip /path/to/frozen_20260928_e6_workflow_artifact.zip \
  --output outputs/e6_source_origin_inventory.json
python -m pytest -q tests/test_payoff_b_e6_source_origin_inventory.py
```
