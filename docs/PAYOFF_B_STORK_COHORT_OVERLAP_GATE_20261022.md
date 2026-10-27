# PAYOFF-B: do two published white-stork tracking papers share birds?

Protocol locked 2026-10-22 before reading the subject identity values in
the public reference-data CSVs, **not** after seeing any GPS migration
or weather effect in the 2016 autumn source.

Two original published Movebank public CC0 cohorts:
- Rotics et al. 2016 first juvenile-versus-adult white-stork fall
  migration and survival: DOI 10.5441/001/1.hn1bd23k.
  Published original \`reference-data.csv\` 43,098 bytes,
  MD5 b38407ed744cf2bd4806afce929f604a; 122 deployment rows.
- Rotics et al. 2018 adult migration timing and reproduction:
  DOI 10.5441/001/1.v8d24552 (already used in PAYOFF).
  Published original reference CSV 14,115 bytes,
  MD5 1c9f7c976ebb094e8b1b9c37965c5717; 36 deployment rows.

The original data dictionaries specify animal-id, animal-ring-id,
deployment-id, tag-id, life stage, deployment end types and
occasional death comments. Read and compare only exact non-placeholder
identifier intersections for four original fields. A tag may be
redeployed and a distinct Movebank Study ID may refer to a biologically
identical bird; overlapping tags alone do not prove a repeated animal.
Animal ID, ring ID or deployment ID exact intersection is a direct
flag against treating the source as an independent replication.

Only aggregate numbers of reference rows/unique identifiers/collisions
and broad life-stage/deployment-end categories may be exported. Raw
animal IDs, ring values, study-sites, GPS, nest/death details and
identifying combinations are never uploaded.

A lack of exact ID collision does NOT certify independence. Papers
can reuse individuals under new identifier conventions; full published
cohort identity and temporal overlap must be checked, and the 2016
source studies autumn migration and juvenile mortality rather than
the 2018 spring migration stage.

No meteorological cue information, source GPS positions, actual
decision timing, recourse, breeding/survival fitness effect or
cross-species biological law is fitted in this identification audit.
