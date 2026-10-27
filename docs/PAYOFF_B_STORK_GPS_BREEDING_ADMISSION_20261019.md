# PAYOFF-B: prospective source admission, white-stork GPS × breeding

2026-10-19. Source: Rotics et al. (2018), published CC0 Movebank DOI
10.5441/001/1.v8d24552 and article DOI 10.1111/1365-2656.12898.

## Focal decision: can movement decisions and reproduction be connected?

Prior source-only QC verified 91 breeding animal-years, 36 deployments,
79 numeric fledgling outcomes (12 unavailable), and a reference-file join.
The prior paper contains its own timing/cost findings: reproducing them
would not demonstrate a new information-actionability mechanism.

Before opening GPS, the following mechanical admission protocol was fixed:

1. Read original published GPS CSV only after strict original file identity
   check: bytes=273153305; MD5=bda2ebd2441316b2e2fd9e9578d7d0b4.
   The source is 273 MB; download is streamed and never committed.
2. Load the independently published reference and breeding files, validate
   unique deployment IDs and unique breeding ID × calendar-year keys.
3. Choose reference join identity using GPS-column source-only matches,
   not fledgling responses: deployment-id, individual-local-identifier
   matched to reference animal-id, or tag-local-identifier to tag-id.
4. Count timestamps and valid WGS84 location rows, exact source-join coverage,
   GPS animal-years linked to breeding records, and repeated individuals.
   Do not label GPS fixes as independent biological samples.
5. Report calendar-month observation coverage for Jan–Feb (at least 5 unique
   dates), Mar–Apr (at least 10), and May–Jun (at least 7). Thresholds
   describe *sampling completeness only*: they do not identify actual
   wintering, migration, stopovers or breeding behavior. Preserve all counts
   even if the three-window subset is sparse.
6. Expose counts for linked numeric fledgling outcomes, but **no fledgling
   association, movement coefficient, seasonal compensation or fitness
   analysis** until route-stage and ecological cue chronology are validated
   separately.
7. Write only aggregate source audit JSON; never upload raw animal identity,
   event positions or the GPS CSV. Strong sample sharing requires review of
   original data terms and appropriate source citation.

## Scientific prior-art and identification boundary

Rotics et al. already related departure, wintering latitude, migration
performance, atmospheric conditions and breeding success. The present source
QC does not establish novelty or causal information use by reusing these
endpoints.

A new independent hypothesis requires a cue *observable before the individual
decision*, actual stage-specific signed responses, an independently
estimable recourse set, and a valid non-identical migration cohort. Only
after an outcome-blind trajectory admission is passed should a separately
registered test estimate a new biological association.

Workflow: .github/workflows/payoff-b-public-stork-gps-breeding-join.yml
Script: scripts/qc_public_movebank_stork_gps_join_2018.py
Test: tests/test_public_movebank_stork_gps_join.py
