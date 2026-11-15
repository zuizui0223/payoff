# PAYOFF-B JMA full event-definition audit and taxonomy correction

**2026-11-15 | PR #352 | original-data run https://github.com/zuizui0223/payoff/actions/runs/43659881923 | 78 tests passed**

## Critical original-data correction

The previous provisional string-matching taxon classifier was **wrong**:
- `いちょう発芽/黄葉/落葉` was misclassified as an insect because `いちょう` contains `ちょう`. These 3 files are plants.
- `ひぐらし初鳴` and `つくつくほうし初鳴` were misclassified as plant/unclassified. They are cicada insect events.
- `とかげ初見` was misclassified as plant/unclassified; it is a reptile event.

The source label taxonomy is now prefix-based with explicit audited names. Correct original 65 event files: **41 plant, 14 insect, 6 bird, 3 amphibian, 1 reptile**. The previous 41 plant/unclassified + 15 insect count was an accidental coincidence and **must not be reused**. All previous cross-taxon correlations and intervals involving plant/insect groups were contaminated by this classification error; replace with corrected runs, not pooled averages of old estimates.

## Original phenological stage inventory

- 28 flowering event files
- 3 full bloom
- 5 bud/leafout
- 2 color change
- 3 leaf fall
- 14 first call
- 10 first sighting

This totals 65. These are explicit stage terms in original labels, not proof of biological equivalence or effort-standardized event definitions.

## Corrected real-data station-balanced cross-taxon correlations

Each exact source-event pair at a station requires >=10 overlapping years. Mean correlation across event pairs within each station, then equal weight to stations.

| Groups | Station count | Corrected station-balanced mean r |
|---|---:|---:|
| Amphibian–insect | 73 | +0.156520 |
| Amphibian–plant | 75 | +0.134725 |
| Insect–plant | 101 | +0.113695 |
| Amphibian–bird | 74 | +0.112540 |
| Bird–insect | 100 | +0.096751 |
| Bird–plant | 101 | +0.088798 |

These remain weak positive *descriptive* observed-event associations. Do not reuse pre-correction bootstrap intervals or rm-code strata as corrected values. Corrected bootstrap and rm-code strata are computed in the current CI receipt but should be read and cited from the current run before reporting numerical intervals.

## Source and identification limits

- 160,367 original calendar-valid event cells, 65 source files, 102 phenology station IDs; 141,562 events have unique date-valid original station metadata.
- JMA original `rm` quality code semantics remain unverified. Observation processes and termination dates differ; source labels are not species-level functional traits.
- There is **no fitted measured temperature, rainfall, snow, sunshine, humidity, wind, NDVI or resource biomass coefficient**. No causal coupling, trophic mismatch, migration payoff or fitness is identified.
- Next priority: source-certify original `rm` documentation and collect actual JMA weather time series for matched station-years. Keep NDVI and independently measured biomass as separate evidence layers.
