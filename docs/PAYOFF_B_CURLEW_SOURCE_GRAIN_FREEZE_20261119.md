# PAYOFF-B — Eurasian Curlew original-source data-grain and repeat-ID admission

Date: **2026-11-19**. Status: **SOURCE-GATE FROZEN BEFORE NEW OUTCOME INSPECTION**, not a newly preregistered independent experiment. Scientific role: determine whether the candidate source genuinely supports an individual longitudinal *movement-to-nest* analysis, while refusing to misrepresent habitat or phenological covariates as measured information use.

## Original 2026 source

- Hanzelka et al. (2026), *Sex-dependent carry-over effects of non-breeding habitat use on breeding performance in the Eurasian Curlew*, DOI **10.1002/jav.03665**; original Dryad dataset DOI **10.5061/dryad.31zcrjf22**, first published 2026-10-01. Original public README [Dryad](https://datadryad.org/dataset/doi%3A10.5061/dryad.31zcrjf22).
- Study scope reported by authors: **124 GPS-tracked individual Curlews / 233 migration-nonbreeding-breeding periods / 2016–2025**. These are **author-reported scopes**, **not verified dimensions of the specific analysis CSV**.
- Dryad includes a publicly listed `README.md` (~14.32KB) and `Curlew_COE_habitat.zip` (~590.99MB). The original archive is not present in PAYOFF GitHub and **no file checksum or original CSV row count has been verified yet**.
- Original README describes `data/dt_hab_Curlew.csv` inside the ZIP; it is **semicolon-delimited** (the source specifically warns that Excel may not preserve formats). Expected fields: `ID_seas` (bird+breeding-year composite), `Bird_ID`, `Sex`, `Br_gr`, `Non_gr`, `Dist`, `Prebr`, `Nest_succ` and habitat-use fraction columns `st_*`, `non_*`, `br_*`.
- `Prebr` is **days from arrival in breeding area until onset of incubation**; `Nest_succ` is source-defined **successful incubation/nesting** (0/1), **not fledging or first-year recruitment**.
- Breeding / wintering lat/lon `X_br`, `Y_br`, `X_non`, `Y_non` are **redacted for sensitive wildlife locations**; they must not be guessed or reconstructed from hidden GPS sources. Original `Nest_succ_user.R` uses GPS clustering and per-individual adjustments to estimate successful nesting. It is **not an independent human-confirmed nest success measurement for every bird-year**.
- The published paper already modeled `Prebr` and `Br_gr` as covariates, and fitted sex-specific nonbreeding/stopover/breeding habitat use associations to nest success. **Do not promote those published associations as a new PAYOFF result.**

## Two distinct gates

**G1 — Original source retrieval and record grain (opened here; no phenotype model):**
1. Query the documented **public Dryad v2 GET API**, record resolved dataset identifier, published version, license, file IDs and provider-reported file sizes and checksums if available; do not invent them.
2. Attempt **public** small `README.md` retrieval and confirm checksum if declared.
3. For the 590.99MB ZIP, prefer **HTTP byte ranges** to inspect the archive central directory and extract only the semicolon-delimited `dt_hab_Curlew.csv`. If remote Range is not supported, download is 401/403, redirects are inaccessible, or the exact archive/CSV identity is uncertain, return `SOURCE_ACCESS_BLOCKED`; do not bypass authorization, do not stage an unbounded 591MB download, and do not claim the CSV was inspected.
4. If the CSV is accessible, validate raw SHA256 of the **extracted CSV** and source ZIP file digest if obtainable (range access alone cannot hash a whole ZIP). Never state ZIP SHA256 was verified when only ranged reads occurred.
5. Report **aggregates only** (no individual IDs, raw GPS coordinates or nest locations): total CSV rows, unique `ID_seas`, unique `Bird_ID`, distinct bird×season entries, repeated birds with >=2 seasons, birds whose *observed success status varies* across seasons, bird-years with nonmissing `Prebr`, within-bird `Prebr` change, breeding region/sex balance and fraction of records with missing data.
6. Check `Nest_succ` values are only 0/1 after source NA parsing, `Prebr` is valid, `Dist` is nonnegative and habitat use fractions are in [0,1] when finite. `NA` for a habitat class denotes *absence of that category*, not automatically a missing bird or zero habitat use. Preserve exact original semantics and don't silently fill NA with 0 for statistical fitting.

**G2 — Identification and proposed follow-up (do not open a new phenotype fit here):**
- An exploratory *within-bird-year* prebreeding interval association to nest success is admissible only if **>=30 genuinely repeated individual IDs**, **>=20 birds with both 0 and 1 observed nest outcomes**, **>=20 repeated individuals with nonzero within-individual Prebr change**, and **>=3 original breeding seasons** with dates independently extractable from original `ID_seas`. A composite `ID_seas` whose year cannot be parsed under a documented source rule fails. These are practical minimum support checks, **not an ex-post power or statistical significance guarantee**.
- If passed, the only candidate observation-level estimand is **within-individual `Prebr`–nest success association**, controlling year and source breeding group, using individual cluster-aware inference. It would be **exploratory, already close to an original Prebr-adjusted covariate**, not a new mechanism result and not a tested information-theory payoff.
- **The more important direct PAYOFF-B mechanism gate automatically FAILS for this published derived table**, even if G2 passes, because neither pre-decision environmental cue exposure nor historical origin→destination predictability at the decision time nor independently measured remaining adjustment capacity is present. `Prebr` is an **observed downstream interval** and cannot stand in for fitness waiting cost `D_eff` or feasible recourse `r(t)`; nesting success is not a complete fitness measure.
- Do **not** use a GPS-derived nest decision inferred from the same trajectory as an independent confirmation of a causal tracking mechanism without measurement-error sensitivity. Separate observational prediction from causal mediation.

## Numerical support ceiling

Author-reported 233 periods and 124 individuals do not prove >=30 repeated individuals or >=20 with changing success. They also do not certify the number of distinct breeding *years* retained in the actual source CSV. So the record-grain gate must decide `PASS_DATA_GRAIN` versus `NOT_IDENTIFIABLE` based on source bytes, without filling missing years or using model-sign-driven thresholds.

If the source ZIP is inaccessible, the deliverable is a reproducible `ACCESS_BLOCKED` receipt with provider status and exact reason, *not a simulated ecological coefficient*. The source remains a candidate, not counted as new independent macro evidence. Do not access eBird or TinyFish, or change the frozen V2/V7 papers.

## Reproduction (public source metadata only / restricted downloads held)

```bash
python -m scripts.payoff_b_curlew_dryad_source_gate \
  --output outputs/payoff_b_curlew_source_gate_20261119.json
python -m pytest -q tests/test_payoff_b_curlew_dryad_source_gate.py
```

Executable source code must limit requests, write no sensitive individual data or files, and keep the original ZIP's authentication and byte-range status explicit. This document precedes any new effect fitting.
