# PAYOFF-B Movebank publication-dependence and public-taxonomy pilot

Date: **2026-10-19**. Scope: 446 Movebank parent DOI packages in the outcome-blind DataCite/DSpace source discovery. This is **not** a bird outcome analysis.

## Evidence from the complete 446-package published metadata census

The complete stage-2 archive (GitHub Actions run 39204043835; artifact 12165445008) includes a parent-package table with a field `linked_publication_dois`. Grouping by **identical published paper DOI** yields:

| Meta-data quantity | All 446 parent packages | 76 T1 cue-and-decision text candidates |
|---|---:|---:|
| Parent DOI packages | 446 | 76 |
| Unique linked publication DOI strings | 341 | 55 |
| Parent packages without a linked publication DOI | 29 | 2 |
| Publication DOI strings appearing in >1 package | 34 | 10 |
| Parent packages belonging to a repeated-publication DOI group | 122 | 32 |

The data above are exact linkage-string counts on the archived source table, not research-cohort counts. One article can contain genuinely independent populations, or multiple papers can reuse the *same* animals, so neither shared nor distinct publication DOI proves cohort-level identity.

Top repeated publication DOI groups in the entire source inventory:
- https://doi.org/10.1126/science.adq3396 — 20 source package DOIs;
- https://doi.org/10.1073/pnas.2316827121 — 13 source package DOIs;
- https://doi.org/10.1111/jav.02515 — 9 source package DOIs.

No ecological direction, sample independence or primary research effect is inferred from these publication-linkage counts.

## Systematic publisher-item pilot (preselected by source-list row position)

Before consulting any GPS events, ten packages at fixed sorted-row indices `0,49,99,149,199,249,299,349,399,445` were requested through original Movebank HTTPS handles. Seven resolved on first public read; three were not resolved within the request timeout and are **not** treated as absence.

For the seven resolvable packages, the original DSpace `/server/api/core/items/{uuid}` item metadata exposed:

| DOI package | Publisher scientific-name string | Publisher animal count | Publisher location count |
|---|---|---:|---:|
| 10.5441/001/1.034jj41h | *Carpodacus erythrinus* | 22 | 1,255 |
| 10.5441/001/1.298 | *Neophron percnopterus* | 65 | 4,828,744 |
| 10.5441/001/1.5jd56s8h | *Chondestes grammacus* | 6 | 869 |
| 10.5441/001/1.67f77j31 | *Cathartes aura* | 18 | 2,605,997 |
| 10.5441/001/1.742 | *Corvus brachyrhynchos* | 12 | 85,308 |
| 10.5441/001/1.c45f2p05 | *Homo sapiens* | 538 | 538 |
| 10.5441/001/1.vv0ft02m | *Pluvialis squatarola* | 14 | 9,230 |

This is a metadata-availability pilot, not a curated biological sample; the *Homo sapiens* record illustrates why the full 446-source catalog **must not be treated as an all-bird dataset**. Publisher counts are not independently validated GPS events, and published location counts must never be summed across packages as independent observations.

## Next inference unit gate

The full public taxonomic source workflow `payoff-b-movebank-taxon-source-census` is required to:
1. Retrieve each official package item and validate the declared DOI;
2. Count successfully observed taxon and sensor fields, explicitly retaining failures;
3. Flag reuse of Movebank study IDs and linked publication DOIs;
4. Separate genuine taxonomic verification from title/abstract keyword hints;
5. Require true individual/deployment and route-stage data before **any** ecological information×actionability effect is fit.

Data-access, animal-use, reproductive-fitness and between-study-independence checks remain separate future gates. This pilot cannot validate the PAYOFF-B game-theoretic or seasonal information mechanism.
