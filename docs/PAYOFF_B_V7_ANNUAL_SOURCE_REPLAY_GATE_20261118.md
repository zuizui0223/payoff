# PAYOFF-B V7: annual historical GDD-jerk source replay gate

Date: **2026-11-18**. Status: **new candidate-input verification code; no original annual data claimed, V7 biological outcome remains NOT_ESTIMABLE**.

## Purpose

On 2026-11-17 we recovered the original Kölzsch et al. 2015 supporting DOCX (independently supplied by the user). It contains 16 original 1982–2011 S1 regional *mean/SD* values and 23 signed *pairwise correlations*, not the 16×30 numerical regional onset values nor the original 16-region membership crosswalk. The earlier schema-only admission `scripts/payoff_b_v7_original_join_readiness.py` intentionally kept the frozen V7 q×U biological test closed, but by itself could not detect a candidate annual CSV whose headers looked right while its numbers conflicted with published source aggregates.

**New:** `scripts/payoff_b_v7_annual_source_replay.py` adds a numeric, source-only necessary-condition screen. The current readiness gate calls it automatically for any user-provided annual CSV with required columns. It does not fit a goose effect.

## Candidate original yearly onset schema

A candidate supplied independently from the authors or an authoritative data archive must have columns:

```csv
flyway,region_code,year,gdd_jerk_onset_julian,original_source_identifier
```

It must be **exactly 480 distinct rows** (16 named source codes × 30 years, 1982–2011). Every region code must belong to its original flyway and each Julian onset value must be finite and within 1–366. A textual self-reported source identifier is necessary for traceability, **not** evidence of external source authentication.

The original supporting document's SHA256 is `925e1e5921a4f005b55c5ffb60fa2958bcb29be8c56f4252cd00f66effe91e19`, and only the derived, source-verified aggregates are committed.

## Two linked original-statistic checks

1. **16 S1 region summaries:** replay 1982–2011 arithmetic mean Julian onset and sample SD and compare to original printed rounding. Fixed tolerance ±0.5000001 d for the integer mean and ±0.0500001 d for the one-decimal SD.
2. **All 23 original pairwise signed Pearson q values:** use the same aligned thirty years for each original pair and check ±0.0050001 to allow printed two-decimal rounding. Pearson r of raw onset times and of centered anomalies are identical if computed over the same years. No sign correction and no replacement of the published SMA/SMATR `s` values is permitted.

Any missing year, duplicate `region_code,year`, wrong flyway, invalid year or onset, absent source identifier, or incorrect row count **fails before comparison**. If all 16 S1 moments match but the 23 historical correlations disagree, the candidate is **not** an authentic reproduction of the published multivariate environmental structure.

**Important:** Even if a candidate matches all aggregates, it remains only `CANDIDATE_AGGREGATE_REPLAY_CONSISTENT_NOT_AUTHENTICATED`, and `V7_REGISTERED_PRIMARY_GATE=HOLD_NOT_ESTIMABLE`. Matching a finite number of summary moments does not certify underlying daily temperature inputs, original source years, chosen NOAA station data, Icelandic shifted glacier region position, or an author's original analytic code. Source authentication and region geometry must be independent.

## Regression test design (never natural data)

`tests/test_payoff_b_v7_annual_source_replay.py` constructs a **synthetic negative-control** calendar. Each of its 16 regional series is generated to match its original S1 mean and sample SD *exactly* using a common standardized year vector, which forces all 23 pairwise correlations to +1, contradicting the original historical signed-q values.

The regression tests require:

- 480 structurally valid synthetic rows produce **16/16 S1 matches, 0/23 q matches** and mandatory `HOLD`;
- missing or duplicated rows, wrong flyway, non-finite values, missing identifiers and an out-of-range year fail;
- deliberately corrupted marginal S1 moments are detected;
- the pre-existing `original_join_readiness` interface invokes the replay and still **never** unlocks registered q×U or goose timing.

A successful synthetic test therefore demonstrates that *marginal consistency is not enough*; it does **not** claim any new empirical GDD values or a direct proof about geese.

## Use only after original data are sourced

```bash
python -m scripts.payoff_b_v7_annual_source_replay \
  --candidate-annual /path/to/author_original_16region_1982_2011.csv \
  --output outputs/payoff_b_v7_annual_replay.json

python -m scripts.payoff_b_v7_original_join_readiness \
  --annual-region-years /path/to/author_original_16region_1982_2011.csv \
  --output outputs/payoff_b_v7_readiness.json

python -m pytest -q tests/test_payoff_b_v7_annual_source_replay.py \
  tests/test_payoff_b_v7_original_join_readiness.py
```

These examples are commands for future *source-authenticated input*, not a claim that the file exists.

## Original archive recovery check

Source search on 2026-11-18 rechecked the published DOI `10.1111/1365-2656.12281`, its KNAW institutional research page and three separate original Movebank DOI dataset links. The KNAW catalog identifies GPS dataset records, and the article describes how 30-year GDD jerks were computed from European Climate Assessment gridded daily temperatures plus NOAA stations; none of those listings independently supplies the 480 authoritative original regional onset numbers **or** the author-specific 16-region coordinate membership.

Authoritative source request should ask for:

1. Numerical 1982–2011 GDD jerk peak Julian onset for all 16 original generalized regions, including original code and stage/flyway name.
2. Original 16 region representative climate lat/lon and the explicitly shifted Iceland-glacier site, or original stopover-fix↔region membership; source code and original algorithm version are ideal.
3. Original 40 complete spring migrations' individual/year inclusion mapping and original GPS-to-region assignments (to prevent counting the 44 source GPS IDs as 40 complete migrations).
4. Temperature product versions/NOAA station identifiers, missing-year handling, year/date convention, and confirmation of whether printed SMATR slopes for Greenland/Svalbard share the intended S1 data.

Any original data request must preserve license restrictions on individual movement data; do not republish copyrighted DOCX or CC BY-NC GPS tracks into this repository.

## Frozen scientific boundary

Current evidence remains: 23 source historical pairwise q, 13 adjacent links, 11 without two ambiguous code aliases, 52,443 independently verified source GPS fixes, and source-only ordinal prefit diagnostics. None of these numbers licenses a new goose arrival-error regression.

**Original V7 biological fit: NOT_ESTIMABLE / UNOPENED.** Do not replace original year-specific $S_{j,y}$ with the 30-year mean, use a newly retrieved reanalysis as though it were original source, derive geometry-only U from stopover duration, or lower any frozen q×U inclusion threshold.

Source: [published paper](https://doi.org/10.1111/1365-2656.12281) and original-derived provenance in `docs/PAYOFF_B_V7_UPLOADED_SUPPINFO_SOURCE_RESULT_20261117.md`.
