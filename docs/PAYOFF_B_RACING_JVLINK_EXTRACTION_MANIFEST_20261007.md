# PAYOFF-B racing JV-Link extraction manifest

Date: **2026-10-07**  
Status: **external-data handoff; no racing outcomes inspected in this repository branch**

## Purpose

The PAYOFF-B racing analysis should not parse opaque JV-Data fixed-width
records inside the statistical layer.

The local JV-Link / JRA-VAN extraction step should first materialize a small,
source-faithful set of normalized tables.  All downstream PAYOFF code consumes
those tables only.

This keeps:

- provider-specific binary/fixed-width parsing outside inference;
- source record identity auditable;
- time provenance explicit;
- the outcome-blind date split reproducible.

## Official source families

### 1. Race metadata: RACE / RA

Use the accumulated race-detail record **RA** to recover at minimum:

- stable race identifier;
- race date;
- scheduled post time;
- meeting / course identifiers as needed for uniqueness.

### 2. Horse result / runner identity: RACE / SE

Use horse-per-race record **SE** to recover at minimum:

- race identifier;
- horse identifier;
- horse number;
- official finish information sufficient to identify one winner;
- fields needed to verify that a runner was a valid starter.

The primary analysis ultimately requires exactly one winner and a stable active
runner set across retained odds snapshots.

### 3. Fixed public forecast: MING / TM

Retrospective primary:

    acquisition API: JVOpen
    dataspec: MING
    record type: TM
    accumulated data category: 7

The category-7 accumulated TM forecast is treated as the stored counterpart of
the final pre-race category-3 forecast.

Required normalized fields:

- race_id;
- horse_id / horse number linkage;
- TM predicted score (0--100 scale);
- raw data category;
- source record/update timestamp if available.

**Fail closed** if the stored record is not category 7 for the retrospective
primary route.

Prospective extension:

    acquisition API: JVRTOpen
    dataspec: 0B17
    record type: TM

Archive realtime category 1, 2 and 3 records at receipt time.  Earlier realtime
forecasts are overwritten by later releases, so category 1 cannot be
retrospectively reconstructed from category 7.

### 4. Time-series win odds: O1 via realtime time-series feed

Use the JRA-VAN time-series win/place/bracket feed:

    acquisition API: JVRTOpen
    dataspec: 0B41
    relevant record: O1

For time-series use, the O1 announcement date/time is part of the snapshot key.

Required normalized fields:

- race_id;
- snapshot timestamp;
- horse_id / horse number linkage;
- decimal win odds.

Only the **win** component is used by the primary PAYOFF test.

The current JV-Data specification guarantees a one-year provision window for
time-series odds.  The retrospective primary sample is therefore restricted to
the officially guaranteed returned window.

## Normalized handoff files

### A. `racing_races.csv`

Required columns:

    race_id,race_date,post_time

Rules:

- one row per race;
- timestamps must have one declared timezone convention;
- post time must be the scheduled/official comparison timestamp used for all
  pre-race offsets.

### B. `racing_results.csv`

Required columns:

    race_id,horse_id,horse_number,winner,valid_starter

Rules:

- one row per race × horse;
- `winner` is 0/1;
- exactly one winner among valid starters in each retained race.

### C. `racing_tm_final.csv`

Required columns:

    race_id,horse_id,horse_number,tm_score,tm_data_category

Primary rules:

- exactly one row per retained race × horse;
- `tm_data_category == 7`;
- `tm_score` finite on the documented score scale;
- runner identifiers must join uniquely to the result table.

### D. `racing_win_odds_snapshots.csv`

Required columns:

    race_id,horse_id,horse_number,snapshot_time,decimal_odds

Primary rules:

- multiple snapshot times per race;
- one row per race × snapshot × active horse;
- odds finite and > 1 after provider missing/scratch codes are resolved;
- no snapshot at or after post time enters the primary analysis.

## Downstream deterministic pipeline

After normalized extraction:

1. intersect races present in RA/SE, TM and time-series odds;
2. use race dates only to create the 70/30 chronological train/test split;
3. select T-30, T-15, T-10, T-5 and LAST from odds snapshots;
4. require the active runner set to be constant across retained slices;
5. calibrate TM scores to probabilities on training races only;
6. freeze those probabilities across all within-race time slices;
7. fit the market/form log-pool weight separately at each time slice on
   training races only;
8. evaluate proper scores and incremental value on untouched test races.

No betting-profit optimization is part of this pipeline.

## Existing PAYOFF implementation

- `src/racing_chronological_split.py`
- `src/racing_time_slices.py`
- `src/racing_public_score_calibration.py`
- `src/racing_information_absorption.py`
- `scripts/calibrate_racing_public_scores.py`
- `scripts/evaluate_racing_information_absorption.py`

## Current external blocker

This repository does not contain the user's local JV-Link subscription,
Windows JV-Link runtime, or extracted JRA-VAN records.

Therefore the remaining empirical blocker is **source materialization**, not
the statistical model:

    JV-Link / Data Lab
        -> four normalized CSV tables above
        -> PAYOFF deterministic pipeline

No substitute web-scraped odds/results should be silently mixed into the
primary route.
