# PAYOFF-B: Burnside houbara source decision — admit past cue proxy, hold post-commitment recourse

Date: 2026-10-08.
Status: **SOURCE VALIDATED, CLAIM GATE CLOSED FOR MIDROUTE CONTROL AND FITNESS.**
Evidence gate read from original author Zenodo v1, 10.5281/zenodo.4917565,
published PNAS 10.1073/pnas.2026378118. The source is NOT a new independent
confirmation of Burnside et al.'s original result.

## Verified original bytes and real sample

GitHub workflow 37773797850 independently retrieved both official Zenodo
files, matching original MD5. Separate workflow 37777751409 inspected the
real study records, author Explanations and original 442-line R reproduction
script, successfully.

- Spring source: **132 departure/arrival records, 44 birds**, years
  2012–2020, no missingness among bird ID, departure and arrival dates,
  departure-temperature and arrival-temperature, and no arrival-before-
  departure rows.
- Autumn source: **152 event records, 48 birds**, years 2011–2019; one
  source record has arrival timestamp approximately **8.167 days BEFORE**
  departure; this anomalous record must not be silently altered or used as
  genuine negative trip length.
- The *published Figure 2 caption* reports 133 spring departures from
  45 birds. The original public v1 workbook has 132/44, so two counts are
  each one less than publication. The reason is unverified; source version,
  different inclusion or a published figure discrepancy are possibilities,
  NOT demonstrated resolutions.
- Spring and autumn data contain one record per bird-year in the archived
  workbook (not complete daily GPS trajectories). Its 1,000-shuffle null
  spring sheet is a randomized event-level comparison, not a raw day-by-day
  risk set of decisions not to depart.

## A critical temporal distinction in the ORIGINAL author's own definitions

The original XLSX Explanations tab defines:
- departure.date = **last fix** on the departure site before starting
  migration. It is not the exact instant the animal evaluated a forecast.
- arrival.date = **first fix** on the arrival site after completing migration.
- departure.temperature.C = MODIS-derived 8-day mean **BEFORE the recorded
  departure date**. It may be a potentially locally available environmental
  proxy, but the MODIS number itself is NOT a measured subjective cue.
- arrival.temperature.C = MODIS-derived 8-day mean **AFTER arrival.date**.
  This is later than both departure and arrival and therefore cannot be
  entered into a retrospective model pretending to represent information
  available *at departure*.
- annual.ref.temperature.breeding = reference breeding-site temperature
  at the **population mean departure date**, not independently observed
  information at a particular bird's origin at its departure. Because
  individual departure dates differ, the field need not even have occurred
  yet for an early-departing bird.
- daylength = daylight hours on departure date; wind.velocity.NS = wind
  during the evening of departure, both aligned to the realized event.
- departure.date.shuffled and temperature.rand are original authors'
  within-individual shuffled-date null values, not observed animal
  counterfactual actions or feasible route choices.

A new fail-closed version of
scripts/payoff_b_houbara_event_time_recourse_gate.py reads these definitions
from the original workbook on each source audit and explicitly tags which
fields are temporally INVALID as predeparture features. It does not
substitute inferred arrival resources for an observed fitness optimum.

## PAYOFF-B causal identification decision

| Proposed claim | From this source? | Reason |
|---|---|---|
| Departure-site temperature is individually repeatable around departures | **ORIGINAL STUDY YES** | Burnside et al. 2021 already established this in tracked Asian houbara |
| Source time can be paired with later arrival and local temperature | **YES** | Source event panel and raw columns verified |
| A bird knew the future breeding-site spring at departure | **NO** | Breeding-site reference and postarrival thermal summary are not actual internal beliefs |
| A bird updated new information during migration | **NO** | No intermediate observed information checkpoint in workbook |
| A bird chose to accelerate or change stopover when new information became available | **NO** | No intermediate action trajectory, independently feasible recourse or standardized maximum alternative |
| Early or late choice caused extra breeding/survival success | **NO** | No individual survival, reproduction or energy-cost endpoint in workbook |
| A migrant–resident interaction can be empirically solved as a coordination game | **NO** | No paired consumer-resource or heterospecific partner timing/fitness response |

**Source verdict: PREDEPARTURE-CUE REPLICATION / INFORMATION-AVAILABILITY
EXAMPLE; DO NOT PROMOTE TO NEW PAYOFF-B CHECKPOINT RECOURSE/FITNESS CLAIM.**

A novel evidence path would require independently timed route-level new
information and action corrections on the same tracked individuals, and
subsequent fitness measured against an independently defined ecological
optimum. If no such source exists, retain the Paper-2 manuscript as a
theoretical framework tested by negative and non-identifying natural
examples; do not invent or reconstruct observed behavioral decisions.

## Accountability and replicability

- Source code and prior-art record: docs/PAYOFF_B_HOUBARA_PREDECISION_CUE_SOURCE_GATE_20261008.md
- Registered event-level source check:
  docs/PAYOFF_B_HOUBARA_EVENT_TIME_AND_RECOURSE_SOURCE_CONTRACT_20261008.md
- Source-only origin workbook MD5/XLSX metadata audit:
  https://github.com/zuizui0223/payoff/actions/runs/37773797850
- Real original row and chronology audit:
  https://github.com/zuizui0223/payoff/actions/runs/37777751409
- New strengthened author-Explanations semantics test:
  scripts/payoff_b_houbara_event_time_recourse_gate.py
- Unresolved mismatch should be treated as **source provenance uncertainty**,
  not a null or falsification of the authors' published result.

Frozen PAYOFF-B V7R and V8 empirical results remain unchanged.
