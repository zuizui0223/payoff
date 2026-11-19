# PAYOFF-B — original source-faithful 2023 bird departure→flight→landing linkage

**2026-11-19, source-only validation complete. New biological model NOT fitted.**

## Actual original data (direct from provider)

Rüppel et al. (2023), *Royal Society Open Science* 10:221420, [DOI 10.1098/rsos.221420](https://doi.org/10.1098/rsos.221420). Original [Figshare collection 10.6084/m9.figshare.c.6403996](https://doi.org/10.6084/m9.figshare.c.6403996), **public data/code ZIP file ID 38968813**, filename `rsos221420_si_002.zip`, provider length **100,303 bytes** and recalculated exact ZIP SHA256 **`0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6`**. Publisher license **CC BY 4.0**. The original archive contains `data.Event.RData`, `flights.RData`, `Rcode.Rmd`. Native R successfully read the two original data objects after generic Python RData parsing failed. **No source row, animal ID, GPS coordinate, wind value, or timestamp is published in the PAYOFF result artifacts.**

## Verified source-grain and key chronology

| Source-original quantity | Direct audit result |
|---|---:|
| Daily at-risk bird×date rows in `data.Event` | **1,783**, 33 columns |
| Binary nondeparture risk days | **1,605** |
| Original departure-event rows | **178** |
| Individuals with exactly one terminal departure event | **178**; no duplicates |
| Original first flight records in `flights` | **178**, 70 columns |
| Unique `motusTagID` in each table | **178 / 178** |
| Intersection of IDs (join by `motusTagID` only) | **178**, zero unmatched |
| Flight records duplicated within an ID | **0** |
| Original flight `landing==1` / `landing==0` | **24 / 154** |
| Flight start and end time available and start precedes end | **178 / 178** |
| Start- and end-time wind/cloud covariates complete | **178 / 178** |
| At-risk terminal date equals `flightStart` UTC calendar day | **175 / 178** |
| At-risk terminal date within ±1 UTC calendar day | **178 / 178** |

This is **good source support for constructing individual, time-ordered original departure risk→first-flight→landing rows**. The three ±1-day cases are **not manually edited or declared bad data**: the source could differ in local calendar vs UTC; the matching audit reports both counts and requires original temporal codebook approval before interpreting weather issue times.

The original flight object includes fields `flightStart`, `flightEnd`, `flightCat` and `landing`, start/end observed wind/cloud, and original departure event table includes daily `time_abs`, `status`, `u/v`, `c` and related weather fields. The native source schema and derived count ledger are delivered from GitHub Actions, with no redistribution of raw movement data.

**Caution on route labels:** the simplistic substring search for literal English `onshore` or `offshore` in raw `flightCat` returned zero; this does *not* imply no source route choices. The original author used compact route codes. Preserve the paper's **154 coastal/onshore vs 24 offshore** prior-art counts separately until the original `Rcode.Rmd` recoding is examined; do not guess route codes or recode outcomes. The subsequent source-only script adds only the original code frequency *aggregates*, not raw individual labels.

## What is and is not newly established for PAYOFF

**Confirmed by source audit:** the 2023 Figshare source is *actually* a linked individual observation design (178 at-risk time series and 178 first-flight episodes, 24 observed landings), not just figure-level evidence. It is a stronger original measurement system for ordered choice than a green-up cross-correlation or the previous 2024 Greenland goose source with weather/feeding.

**Already published by Rüppel et al. 2023:** wind/pressure/cloud/rain influence daily departure, routing (sea vs coastal) and interruptions/landing. PAYOFF did not newly discover this. The paper is autumn coastal migration in 2019–2021 for Garden Warbler, Greater Whitethroat, and Sedge Warbler; no spring destination matching or breeding output was collected.

**Still absent or not identified:** actual pre-commitment forecasts of *future* in-flight/destination conditions; bird-specific environmental forecast reliability q, subjective cue use, separate feasible recourse budget `r(t)`, causal waiting cost `D_eff`, post-landing ultimate seasonal mismatch, reproductive fitness, or interacting flower/pollinator phenology. Weather measured at sunset is the local physical environment, **not** a bird's probabilistic knowledge about future weather. Also, landing/nonlanding observation is conditioned on receiver coverage; offshore detection is lower and route-dependent. Event-level regression using these data would be **post-publication observational reanalysis**, subject to selection/detection bias and original 2023 prior-art collision.

A new **forecast-error and recourse** study should first obtain archived **issue-time-appropriate weather forecasts** independent of the observed landing weather and predefine an endpoint beyond the original 2023 published weather/decision slopes. Without that, further re-fitting this same source does **not** directly test PAYOFF-B's information-limited coordination theorem. Do not chase post-hoc significance.

## Code, provenance and quality

- Pre-source original contract: `docs/PAYOFF_B_RUPPEL_SEQUENTIAL_SOURCE_CONTRACT_20261119.md`.
- Source RData amendment: `docs/PAYOFF_B_RUPPEL_RDATA_SOURCE_ESCALATION_20261119.md`.
- Source linkage contract: `docs/PAYOFF_B_RUPPEL_NATIVE_JOIN_PREFIT_20261119.md`.
- Repro scripts: `scripts/payoff_b_ruppel_figshare_source_gate.py`, `scripts/payoff_b_ruppel_rdata_source_gate.py` (pyreadr failure recorded), `scripts/payoff_b_ruppel_original_RData_schema.R`, `scripts/payoff_b_ruppel_native_schema_receipt.py`, `scripts/payoff_b_ruppel_original_decision_join.R`, `scripts/payoff_b_ruppel_join_source_receipt.py`.
- Direct original source GitHub Actions [run 44543643759](https://github.com/zuizui0223/payoff/actions/runs/44543643759) **SUCCESS**, official provider ZIP SHA256 verified, original native R data loaded and all aggregate source keys/time units checked. Artifact ID **14538699556**, aggregate ZIP SHA256 **`bba1e8256451cc730aa9b6c8b2c7045af2d570143a39bd160b01aea7f9f20b25`**. Original version's source names/measurements are retained without changing the input series or test definitions.
- All tests are original schema integrity and fail-closed checks; no new ecological coefficient or prediction interval is inferred. The draft branch remains on [PR #410](https://github.com/zuizui0223/payoff/pull/410); `main`, frozen V2/V7 and prior submitted manuscripts unchanged.
