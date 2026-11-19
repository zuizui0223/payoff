# Rüppel 2023 original RData escalation — source-only schema inspection

**Pre-result amendment 2026-11-19**, after original Figshare file list inspected, **before** unpacking RData tables/estimating any source effects.

The original [Figshare collection 6403996](https://doi.org/10.6084/m9.figshare.c.6403996) has two original articles: supplemental analysis ZIP `rsos221420_si_002.zip` (file ID **38968813**, **100,303 bytes**, original publisher MD5 `e8fc27e9eb44aa1e89da09310183b39a`, locally recalculated ZIP SHA256 **`0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6`**), and a separate supplementary PDF (file ID 38968810), which is not analyzed here. Original ZIP contents discovered by the preceding source-only Figshare audit:

- `data.Event.RData` (57,743 uncompressed bytes);
- `flights.RData` (38,300 uncompressed bytes);
- `Rcode.Rmd` (27,765 bytes).

**The earlier '0 plain CSVs' diagnostic did not imply absence of original source data.** It meant the first parser supported only CSV/TSV/JSON, while the original source uses .RData.

## Safe original-data admission (still NO outcome fit)

1. Download only **the exact original ZIP** from its provider-listed anonymous URL (Figshare file 38968813); compare both original size and **recalculated ZIP SHA256** above; fail closed on any mismatch.
2. Inspect two fixed RData member names using `pyreadr` inside CI temporary files. Record *only* source R object names, data-frame row/column counts, original column names and dtypes, cardinalities of ID-like columns and counts of nonmissing candidate time/weather/decision columns. **Do not upload or display raw individual bird IDs, GPS coordinates, times, weather or response values**.
3. Inspect the original R Markdown script locally *only to identify schema object names and authored join operations*. Save just a bounded count of referenced object names and potential join verb tokens in aggregated JSON, not the full copyrighted original source or its individual values.
4. The existence of `flights.RData` and `data.Event.RData` does **not** establish linked choices on one bird. Require an explicit **same-identifier** individual join validated against the author's own code/meaning, with separately timestamped departure-at-risk days, route and subsequent landing events. Prior 30-bird / 10-landing minimum unchanged.
5. Weather at each source sunset/flight hour is **observed historical meteorology**, not an individual probabilistic destination forecast or exogenous independent cue. The already-published Rüppel 2023 weather effects remain prior art. No new biological model, q_wait, D_eff, r(t), downstream fitness or partner matching is permitted without separate frozen contract and source-grain admission.

If pyreadr cannot interpret an original R object, report `ORIGINAL_RDATA_PARSER_UNSUPPORTED` and the exact member; do not invent a tabular record or silently ignore unsupported objects. All outputs aggregate-only, no owner permissions bypass, eBird, TinyFish or changed V2/V7 manuscripts. The source admission must be traced to the original 2023 Figshare file's SHA256 and published CC BY 4.0 license.
