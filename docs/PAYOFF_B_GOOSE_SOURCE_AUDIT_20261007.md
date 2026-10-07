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

## Fixed stopover reconstruction

Published stopover criterion:

- within 30-km radius;
- >48 h;
- at most one outlier position.

A frozen observed-anchor reconstruction was implemented before the joint Q–R
analysis.

To prevent artificial subdivision of one 30-km site caused by choosing
different observed anchors, temporally adjacent candidates are merged when
their centers are <=60 km apart. The 60-km limit is exactly twice the published
site radius and was set before cross-flyway comparison.

No flyway-specific thresholds were used.

Fixed-rule machine result:

| Flyway | Machine mean stops | Published mean stops |
|---|---:|---:|
| Greenland | 5.00 | 5.3 ± 0.2 SE |
| Svalbard | 3.90 | 4.2 ± 0.3 SE |
| Barents Sea | 6.08 | 5.7 ± 0.5 SE |

The reconstruction is not identical to unpublished/manual site decisions, but
it reproduces the reported aggregate architecture without route-specific
retuning.

Implementation:

    src/goose_stopover_detection.py

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
