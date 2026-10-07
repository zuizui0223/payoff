# PAYOFF-B barnacle-goose public-source audit

Date: **2026-10-07**  
Status: **source / feasibility receipt before joint Q–R outcome analysis**

## Source paper

Kölzsch A, Bauer S, de Boer R, Griffin L, Cabot D, Exo K-M,
van der Jeugd HP, Nolet BA. 2015. *Forecasting spring from afar? Timing of
migration and predictability of phenology along different migration routes of
an avian herbivore.* Journal of Animal Ecology 84:272–283.

DOI: 10.1111/1365-2656.12281

Published analytic sample:

- Greenland: N=7;
- Svalbard: N=21;
- Barents Sea: N=12;
- total: N=40;
- one complete spring migration per individual.

Published year distribution:

- Greenland: 4×2008, 1×2009, 2×2010;
- Svalbard: 2×2006, 7×2007, 3×2008, 3×2009, 2×2010, 4×2011;
- Barents Sea: 6×2008, 6×2009.

## Public Movebank archives

All three Movebank Data Repository packages are CC0.

### Greenland

DOI: 10.5441/001/1.5d3f0664

GPS bitstream:

    721751f9-dda5-44a1-9f36-bad42dc191fb

Reference-data bitstream:

    d1ad187e-72d2-4e02-9e95-72c8031063cf

Machine source audit:

- GPS rows: 6,853;
- archive animal IDs: 7;
- event years represented: 2008–2010;
- median within-track interval: 2 h;
- coordinates complete;
- no provider ground-speed column.

Reference-data eligibility:

- explicit not-used deployments: none;
- source-eligible deployments: 7;
- deployment-year counts: 4×2008, 1×2009, 2×2010.

This exactly matches the published Greenland sample.

### Svalbard

DOI: 10.5441/001/1.5k6b1364

GPS bitstream:

    df28a80e-e0c4-49fb-aa87-76ceb2d2b76f

Reference-data bitstream:

    a6e123b0-7588-40da-8f06-73559bb3ff6b

Machine source audit:

- GPS rows: 24,488;
- archive animal IDs: 22;
- event years represented: 2006–2011;
- median within-track interval: 2 h;
- coordinates complete;
- no provider ground-speed column.

Reference-data eligibility:

    70568 -> deployment-id = "70568-not used"

Therefore:

    22 archive IDs - 1 explicit not-used = 21 eligible

Deployment-year counts after that source flag:

- 2×2006;
- 7×2007;
- 3×2008;
- 3×2009;
- 2×2010;
- 4×2011.

This exactly matches the published Svalbard sample.

### Barents Sea

DOI: 10.5441/001/1.ps244r11

GPS bitstream:

    deda6bce-db1e-4f0d-af1f-058dbfcaf83b

Reference-data bitstream:

    90ffc5fa-25f7-40d6-90c6-b8baa2b04df4

Machine source audit:

- GPS rows: 21,102;
- archive animal IDs: 15;
- event years represented in the archive: 2008–2011;
- median within-track interval: 3 h;
- Q25–Q75 within-track interval: 3–15 h;
- coordinates complete;
- provider ground-speed and heading fields present.

Reference-data eligibility:

    78040  -> "78040-not used"
    78042a -> "78042a-not used"
    78042b -> "78042b-not used"

Therefore:

    15 archive IDs - 3 explicit not-used = 12 eligible

Deployment-year counts after the source flags:

- 6×2008;
- 6×2009.

This exactly matches the published Barents Sea sample.

The archive contains later-year fixes from tags that continued transmitting.
Those later spring seasons are **not** part of the source-faithful primary
sample.

## One-spring rule

For each source-eligible deployment:

1. read the deployment year from \`deploy-on-date\`;
2. retain only the spring trajectory from that deployment year for the primary
   Kölzsch reanalysis;
3. do not add later tag years as extra pseudo-independent migrations.

Implementation:

    src/goose_archive_eligibility.py

## Corrected stopover reconstruction

The first reconstruction used a 30-km anchor-radius interpretation. That was
rejected after checking the cited source method.

van Wijk et al. (2012) instead describe:

- clusters of **successive positions** whose pairwise displacement is <=30 km;
- minimum residence 48 h;
- one >30-km detour can remain part of the stopover if the bird returns to the
  preceding cluster within 8 h;
- a second detour ends the stopover.

The related De Boer et al. analysis of these barnacle-goose data reports a 6-h
detour-return variant. The prospective primary reconstruction uses the original
8-h van-Wijk window and keeps 6 h as sensitivity.

Implementation:

    src/goose_stopover_detection.py

Machine audit with the corrected 8-h detector and the frozen one-spring sample:

| Flyway | Machine mean detected stops | Published Kölzsch mean |
|---|---:|---:|
| Greenland | 5.43 | 5.3 ± 0.2 SE |
| Svalbard | 4.19 | 4.2 ± 0.3 SE |
| Barents Sea | 6.75 | 5.7 ± 0.5 SE |

Greenland and Svalbard reproduce the aggregate architecture closely. Barents is
somewhat over-segmented and therefore requires region-level mapping or a
sensitivity analysis before component-specific claims.

No flyway-specific thresholds are permitted.

## Breeding endpoint audit

A naive literal automation of the Kölzsch rule

    last stopover before end June with a 7--26 d residence

does **not** safely recover breeding arrival from the archived tracks.

With the corrected detector, long Arctic clusters frequently continue for much
longer than 26 d:

- Greenland: 0/7 final pre-July clusters satisfy the literal 7--26 d range;
- Svalbard: 4/21;
- Barents Sea: 1/12.

Selecting the last *qualifying* 7--26 d cluster would therefore mislabel an
earlier Icelandic/Norwegian/continental staging site as the breeding endpoint
for many birds.

The code now fails closed instead of falling back to an earlier site:

    src/goose_route_timing.py
    select_breeding_endpoint()

### Independent curated endpoint source

Shariati's thesis provides Appendix Tables A1 and A2 with:

- bird ID;
- tracking year;
- last staging site;
- departure date from the last staging site;
- breeding site;
- breeding-site arrival date.

These tables cover:

- Russian/Barents Sea tracks: 12 individuals across 2008--2010;
- Svalbard tracks: 17 individuals across 2006--2010.

For the one-spring PAYOFF sample, the first deployment-year rows give an
independent curated endpoint for:

- all 12 Barents individuals;
- 17 of the 21 Svalbard individuals.

The four 2011 Svalbard individuals and all seven Greenland individuals are not
covered by those Appendix tables.

Primary remaining-duration recourse should therefore begin with the curated
29-individual Svalbard+Barents subset rather than infer breeding arrival from
our own stopover segmentation.

Implementation accepts an external curated arrival without redefining it:

    remaining_schedule_to_curated_arrival()

No full Appendix table has been copied into this repository; it remains an
external source that must be materialized with provenance if this route is
executed.

## Environmental Q source

The paper's Supporting Information states that it contains:

- Table S1: mean and SD of GDD-jerk spring-onset dates by stopover region;
- Tables S2–S7: yearly spring-onset anomalies for consecutive-region pairs;
- 30-year climate window: 1982–2011.

The Wiley DOCX endpoint is currently bot-blocked to the automated fetch route,
but the article HTML exposes the supplement description and many published
link-level correlation/slope results.

Primary Q remains held until either:

1. Tables S2–S7 are materialized directly; or
2. the 1982–2011 spring-onset series is reconstructed source-faithfully from
   the declared climate inputs.

Do not substitute approximate values digitized from arrow widths in Figure 1.

## Feasibility conclusion

Source gate: **PASS**

The public system is sufficient in principle for a joint identification test
because:

- the exact analytic individual/year sample can be recovered from archive
  metadata without response-based exclusions;
- GPS resolution is adequate to reconstruct stopover and transit timing;
- fixed stopover rules approximately reproduce published flyway-level stop
  counts;
- the paper provides a separate 30-year environmental predictability source.

Remaining primary blockers:

1. materialize the spring-anomaly tables;
2. map fixed reconstructed stops to the published regional climate links;
3. declare the breeding-arrival endpoint used for remaining-duration recourse.

No joint Q×R outcome has yet been opened.
