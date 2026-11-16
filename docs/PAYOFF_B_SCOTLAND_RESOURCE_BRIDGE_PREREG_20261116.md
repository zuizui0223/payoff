# PAYOFF-B: Scotland resource-curve source admission (2026-11-16)

Status: **outcome-blind schema/data acquisition gate** for a new independent data panel. Existing PR #388 selection/breeding outcomes were already opened and failed the 2/3 population consistency gate. No positive claim from this new dataset until exact provenance, joint identifiers and independent validation are checked.

## Public primary sources and prior-art boundaries

1. **EIDC 2022, Phillimore et al.** "Tritrophic phenology and associated data from 44 sites in Scotland, 2014–2021", DOI 10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3. The official catalogue documents 44 sites, two-day tree phenology, roughly four-day branch-beating caterpillar/spider/beetle counts, blue tit first egg/hatching date and breeding success. Dataset use is under the Open Government Licence. File-level schema, downloadable access and exact site-year join **not yet verified**.
2. **Zenodo 2024, Macphie et al.**, DOI 10.5281/zenodo.14170139, supporting Oikos 2025 "Tree taxon effects on the phenology of caterpillar abundance and biomass" (10.1111/oik.10972). The prior article already models host-tree-dependent seasonal caterpillar abundance and biomass. Candidate for repeat-sampled measured mass, but file names, years and overlap unverified until audit.
3. **Zenodo 2026, Macphie/Bialy et al.**, DOI 10.5281/zenodo.23335990, companion of Ecology and Evolution 2026 "The spring phenology of arboreal beetles and spiders and their potential as alternative prey for birds mistimed with peak caterpillar abundance" (10.1002/ece3.74489). Prior art already describes alternative-prey phenology, so their seasonality alone is *not a novel discovery*. Candidate for an independent alternative-guild seasonal-abundance proxy, pending source-level join.
4. **Macphie et al. 2026 preprint**, DOI 10.32942/X27Q35, "Timing isn't everything: impacts of maximum abundance and duration of a seasonal resource on consumer fitness". Uses 44 sites, 11 years and already identifies resource-height and width associations with the optimum of blue-tit hatch dates, breeding success and selection. Data/code reportedly "will be made available upon publication". This overlaps materially with any naive caterpillar seasonality–breeding success test.

## What to verify before analysis

- Download **only authorized public** files, without credentials or bypasses. Record SHA256 of downloaded byte streams, official record IDs, artifact names, file byte sizes, metadata checksums, years, site/nest/resource IDs, sampling effort, and original source units.
- Check EIDC direct data-packaging endpoint for whether it is accessible anonymously; catalogue metadata OGL **does not imply** direct anonymous download. If login or explicit acceptance is required, record as blocked.
- Repeated food record must have actual observation date and **site/year identifier**; required count/biomass field and sampling effort calibrated. Number per standardized branch beating is **not** automatically g per m² or consumed prey biomass.
- Bird record must have individual hatch date, actual reproductive outcome and matching site/year; counts per site-year, years and nests included in crosswalk must be audited.
- Source data may overlap the same parent sample used in already published papers. No "independent replication" just because it is a different publication; independence is about individuals/site-years and scientific contrast.

## If actual joint data pass

**Focal estimand:** independent site-year-sampled time-resolved prey availability during an *observed hatch-based* nestling window, and the incremental out-of-year/out-of-site predictive effect on fledging outcome compared with a seasonality-only baseline. Do not infer real consumption or diet-switching.

Use a **pre-fixed** demand window (hatch day to hatch+13 days, equal daily weights; a biologically reasonable proxy, explicitly **not** directly measured energetic demand); require measured prey sampling covering this interval, no interpolation outside convex observed support, and a minimum source-specific coverage fraction, to be frozen after schema inspection but before outcome coefficients.

Predictions to distinguish:
- P1: Caterpillar **peak** may fail even where within-nestling-window prey exposure is predictive. This is a stronger real bridge from resource amount to biotic contact than PR #388's peak values.
- P2: Conditional on caterpillar-window exposure and source climate/site, independent beetle/spider abundance *could* partially buffer poor caterpillar-window timing, but the data record only potential availability, not ingestion.
- P3: When enough replicated event-stage decisions exist, assess timing of hatch relative to resource; **never** misrepresent local nests as migratory forecast-information or en-route recourse tests.

Hold-out entire **site-year** (not nests) and **sites** for generalization; compare a common set of rows across models, null intercept, source-relevant temperature/site baseline, prey peak-only, window exposure, alternative prey-window exposure, and interaction. Unit aggregation/nesting, uncertainty and prior-art similarity must be reported. No post-hoc optimization of demand window, prey guild weights or correlation lag.

## Stop conditions

If exact source acquisition, source schema, matching identifiers, effort correction, or food units fail, stop at a machine-readable **NO_GO**. Do not simulate missing biomass, infer real prey mass from abundance, or claim a fitted fitness effect.