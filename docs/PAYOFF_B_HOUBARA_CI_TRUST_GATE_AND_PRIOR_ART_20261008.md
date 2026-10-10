# PAYOFF-B houbara: source-CI trust gate and prior-art boundary

Date 2026-10-08
Status: historical raw-source checks passed; later source timeout false-green diagnosed; fail-closed code repairs committed.

## Verified original source receipts

GitHub Actions run 37773797850 successfully downloaded and verified original Zenodo record 4917565:
- MigrationData.xlsx: 13,365,399 bytes; MD5 183edf4bc6b3ba9946e4145589ff1c2d.
- PNAS_code.R: 23,948 bytes; MD5 73050bfb758fd8d7a290913d80315ce7.
- OOXML metadata: five original sheets.

GitHub Actions run 37777751409 independently parsed original real event rows:
spring 132 records / 44 individuals, autumn 152 records / 48 individuals,
one autumn negative trip duration, full source codebook from Explanations.
The original paper's spring Figure 2 states 133 / 45; reason for the
archive-versus-publication one-record and one-bird discrepancy remains UNKNOWN.

## Discovered erroneous green CI

In later run 37784494209, the real-data gate generated
ACCESS_OR_CHECKSUM_HOLD (TimeoutError on all three Zenodo XLSX endpoints,
with R code also unavailable) but process exited 0 and CI was labeled
SUCCESS. Synthetic parser check succeeded but source bytes were NOT
verified in that run. Therefore, a green CI job cannot be equated
automatically with a passing real-source gate.

Applied fail-closed repairs:
- scripts/payoff_b_houbara_zenodo_metadata_gate.py now exits nonzero
  after writing its receipt unless the original XLSX passed declared
  schema/MD5 and the original R code also passed MD5.
- scripts/payoff_b_houbara_event_time_recourse_gate.py now exits nonzero
  after writing its receipt unless actual event data and the original
  author's field semantics were both verified in that execution.
- Two houbara workflows now use upload-artifact with if: always(),
  preserving failure JSON when source retrieval fails.

A former legitimate source admission remains evidence even if a newer
download becomes temporarily unavailable. A failed download is never a
biological null result, a success, or a new cue-use estimate. The added
author-semantics code must pass on actual source bytes before claiming
it independently verified (earlier data/field meaning are source-backed).

## Source semantics and biological claim ceiling

Author XLSX Explanations defines departure.date as last origin fix before
the flight; arrival.date as first destination fix; departure.temperature.C
as an 8-day prior MODIS mean; arrival.temperature.C as an 8-day mean
AFTER arrival. The latter is post-outcome relative to an origin-departure
decision, not evidence of available future information.

No intermediate route decision, feasible recourse, reproductive/survival
fitness, or heterospecific interaction is contained in the released
spring event sheet. Burnside 2021 had already identified repeatable
temperature-cue departure effects. Repeating that paper is not a new
PAYOFF-B mechanism.

## Decisive prior-art overlap

Gurarie et al. (2019), Ecosphere doi:10.1002/ecs2.2971, already
documented arrival–departure decoupling and compensating migration
durations among 1,048 female caribou across seven herds. Carneiro et al.
(2020), Frontiers Ecology and Evolution doi:10.3389/fevo.2020.00145,
already tested direct versus stopover routing and weather in 57
whimbrel migrations, with 9 direct, 48 stopover and only three
birds observed switching route strategy; repeated-individual model
did not robustly establish the original departure-date association.
Those original effects are PRIOR ART, not discoveries of PAYOFF.

A novel direct PAYOFF-B mechanism still requires independently dated
new on-route cue, feasible response set, actual behavior after cue,
and for fitness assertions independent energetic and reproductive
outcomes from the SAME biological subjects. No examined source
has passed all of these gates.
