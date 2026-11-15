# PAYOFF-B common-support independent flowering-reference falsification

**2026-11-15 | PR #363 | original-data CI https://github.com/zuizui0223/payoff/actions/runs/43675590427 | 100 tests passed**

The previous 200 random disjoint source-file partitions allowed the set of contributing stations to vary with each partition. Here each 20-year block selects four original flowering source files maximizing 20-year *shared* station coverage with bird/insect first-sighting series (selection uses only coverage, never observed effect sizes), freezes all station IDs and evaluates all six oriented balanced 2-vs-2 plant reference assignments.

| Window | Selected plant files | Fixed stations | Six r values summarized | Median r | r min–max | Positive |
|---|---|---:|---:|---:|---|
| 1961–1980 | 001,003,004,006 | 18 | 6 | +0.290349 | −0.022523 to +0.431420 | 5/6 |
| 1981–2000 | 001,004,007,011 | 28 | 6 | +0.053467 | −0.134230 to +0.202408 | 5/6 |
| 2001–2020 | 001,004,008,009 | 17 | 6 | **−0.227943** | **−0.378868 to −0.117654** | **0/6** |

**Interpretation:** The sign of the inferred interannual bird–plant vs insect–plant lag co-fluctuation is not stable to restricting the sample to an identical station network and a small, jointly observed flowering source-file set. In 2001–2020, all six disjoint reference assignments are negative in the strict common-support panel, while the broad varying-station 200-split median was +0.356747. This contrast **does not isolate station composition as the cause**, because the plant source-file universe also changes (26 files versus a selected four). The six oriented assignments are not six independent replicates and their range is not a confidence interval.

The fixed common-support sample is smaller (17 sites in the most recent period), coverage-optimized and potentially geographically unrepresentative. The underlying JMA biological `rm` codes and observer effort remain uncertified. Neither food biomass nor measured climate was fitted. Do not claim trophic mismatch, ecological coordination, adaptation or a climate mechanism from this analysis.

**Next diagnostic:** distinguish plant source-file selection effects from station-composition effects using a factorial common-support analysis: for each fixed set of plant files, calculate matched-site and variable-site estimates with the same files, and for each fixed site set compare alternative plant source subsets. Report coverage loss and selection sensitivity; then join source-verified annual weather anomalies.
