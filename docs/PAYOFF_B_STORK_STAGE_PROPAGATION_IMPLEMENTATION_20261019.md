# 2026-10-19 implementation handoff: frozen stork 53-season stage pilot

The pre-outcome analytical lock already exists at
\`docs/PAYOFF_B_STORK_STAGE_PROPAGATION_PILOT_LOCK_20261019.md\`.
This implementation does **not** modify that lock. It rebuilds only the
original Jan-Feb baseline / March-April 20%-to-80% crossings from the
original published CC0 stork GPS checksum, and requires the original exact
53 animal-years / 27 animals / 15 repeated animals.

The primary year-FE slope is calculated with exact group-demeaning, equal
animal-year contribution. Cluster bootstrap (2,500 draws; seed 20261019)
resamples *whole individual histories*, not event rows. Failed bootstrap
repetitions must be reported, not silently presented as more independent
animal records. 1,000 year-stratified permutations and leave-one-animal-out
checks are descriptive controls.

Calendar-leap normalization and raw-DOY variation must both be shown.
Within-animal demeaning uses only animals observed in >1 admitted years.

No raw bird identifiers, locations or per-individual outcomes are exported.
Fledgling counts are neither ingested as a response nor regressed on the
timing slope. A beta <1 with an upper 95%-bootstrap confidence limit <1
licenses only **observational temporal compression between relative northing
checkpoints**. It is not evidence of feedback control, cue information,
reproductive benefit, or generality across bird clades.

Do not pool this January-April pilot's 53 seasons with the separate
February-May within-range 91-season source screen.
