# PAYOFF-B Curlew 2026: published original API verified, data bytes inaccessible without authorization

**Date:** 2026-11-19. **Result:** `PUBLISHED_METADATA_VERIFIED_BINARY_FILE_GET_HTTP_401`, **not** a biological result, and **not** an estimate of theoretical information value or movement recourse.

## What the public original Dryad API actually confirmed

Original Hanzelka et al. 2026 Dryad dataset [DOI 10.5061/dryad.31zcrjf22](https://doi.org/10.5061/dryad.31zcrjf22) is published with original version ID **466868**, publication date **2026-10-01**, license **CC0-1.0**. The official REST v2 metadata was requested and successfully read on GitHub Actions; original archive file IDs were **present in HAL self-link paths** rather than in scalar `id` fields.

| Exact published file | File ID | Provider size | Provider SHA256 (metadata only) |
|---|---:|---:|---|
| `Curlew_COE_habitat.zip` | **4989265** | **590,985,065 bytes** | `e3556851ef646eabad21dc0d482da58028b0327a8aaf459fdb02c3896bd48372` |
| `README.md` | **4989366** | **14,323 bytes** | `feb2e058090abd6863ef91570cd3afe4136d7ec9bb41f040612764648b5b892b` |

The original provider identifies both digest algorithms as **`sha-256`**. These are *published provider digests*, **not independently recalculated from original file bytes**.

Official public anonymous `GET /api/v2/files/{id}/download` to retrieve the README returned **HTTP 401**; the same published archive endpoint when called with `Range: bytes=0-0` also returned **HTTP 401**. The script **did not circumvent authentication, fetch the 591MB ZIP through another private mirror, accept a user's legal agreement, or extract any original bird records**.

The previously known original README content was visible through the publisher's public dataset page, including the semicolon-delimited `data/dt_hab_Curlew.csv` source schema, with original `Bird_ID`, `ID_seas`, `Nest_succ`, `Prebr` and migration/habitat fields. But knowing field names is **not equivalent** to counting actual repeated birds or fitting a model.

Source-only GitHub Actions gate runs:
- [run 44507580040](https://github.com/zuizui0223/payoff/actions/runs/44507580040): initial version metadata parser mismatch;
- [run 44507910563](https://github.com/zuizui0223/payoff/actions/runs/44507910563): HAL version resolved, file metadata parser adjusted;
- [run 44508380017](https://github.com/zuizui0223/payoff/actions/runs/44508380017): original ZIP/README listed but file download returned **HTTP 401**;
- [run 44508754214](https://github.com/zuizui0223/payoff/actions/runs/44508754214): provider `digestType = sha-256` and exact source manifest recorded.

## Stopped biological claims

- Original published study scope: **124 tracked individuals / 233 periods / 2016–2025**. These are **article/README-reported** quantities; the underlying `dt_hab_Curlew.csv` number of rows, unique bird-season rows, repeated individuals, and within-individual nest-success changes remain **UNVERIFIED**.
- Original `Nest_succ` is success of a nesting attempt reconstructed from GPS cluster/residence in the original user-calibrated per-individual workflow, and the paper already uses `Prebr` as a covariate. It does not directly measure juvenile survival, independent body condition, or a PAYOFF information game.
- Original latitude/longitude fields are **redacted for sensitive nesting/wintering locations**. Do not infer high-resolution climate exposure at a secret site.
- Even if the bird-season table were accessible, `Prebr` is an *observed downstream arrival-to-incubation interval*, not independent remaining movement-control capacity or a clean waiting cost `D_eff`; no original predecision future-environment signal and actual information timestamp is identified by the published derived fields.
- A within-bird repeated-year **observational** sensitivity would be considered only after source-grain gates pass; no regression or positive/negative biological effect is fit here.

## Safe source-dependent next action now implemented

`scripts/payoff_b_curlew_local_source_admission.py` accepts either:

1. **Exact provider ZIP:** `Curlew_COE_habitat.zip`, verified against published size **590,985,065 bytes** and provider SHA256 `e355...372` (full digest in source file), then reads only `dt_hab_Curlew.csv` for aggregated eligibility. This is the strongest provenance route.
2. **Small original extracted CSV:** `dt_hab_Curlew.csv`, read directly with original semicolon delimiter. Its own SHA256 is recorded, but it is **explicitly labeled user-supplied/original-origin not independently verified** without a corresponding ZIP digest/author receipt. This is still enough for a *provisional source-grain eligibility screen*, not proof of causal transfer.

Neither method copies raw bird/season IDs or GPS coordinates into public repository files or outputs. The executable original-provenance gate refuses guessed file names, changed original ZIP size/hash, missing source columns, invalid nesting status, negative `Prebr`, habitat proportion outside [0,1], and unknown year mapping. For source-year parsing it only accepts a conservative trailing `_YYYY` or `-YYYY` until the original ID format is documented. All exact replication thresholds are frozen in `docs/PAYOFF_B_CURLEW_SOURCE_GRAIN_FREEZE_20261119.md`.

### Offline use on an authorized copy

```bash
# Better: exact original ZIP with SHA256 verification
python -m scripts.payoff_b_curlew_local_source_admission \
  --local-original-zip /path/to/Curlew_COE_habitat.zip \
  --output outputs/payoff_b_curlew_grain.json

# Or a separately extracted semicolon-delimited CSV (weaker provenance)
python -m scripts.payoff_b_curlew_local_source_admission \
  --local-derived-csv /path/to/dt_hab_Curlew.csv \
  --output outputs/payoff_b_curlew_grain.json
```

No original bytes or source outputs beyond metadata are committed. **Current original source access: BLOCKED_HTTP_401; repeated-bird effect: NOT_ESTIMABLE; PAYOFF-B natural information deadline: NOT_ESTIMABLE**.

### Claim and project status

Maintain the exact anti-phase theory and published E6 reanalysis with explicit prior-art/source-policy boundaries. Do not add the Hanzelka habitat→nest paper result to PAYOFF as an independent information-theory confirmation. This branch stays **Draft** until a permitted original file can be read and its biological sample support verified.
