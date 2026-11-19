# PAYOFF-B E6 — previously embedded eBird study and forced source-provenance sensitivity

Date: **2026-11-19**. **Post-open source correction; no outcome-driven exclusion, no new effect discovery.**

## Source issue discovered after publication-oriented E6 integration

The canonical published E6 reconstruction uses Usui et al. (2017), *Journal of Animal Ecology* DOI [10.1111/1365-2656.12612](https://doi.org/10.1111/1365-2656.12612), Dryad [10.5061/dryad.mb4nd](https://doi.org/10.5061/dryad.mb4nd); the raw source is distributed under CC0 at [Zenodo record 4970634](https://zenodo.org/records/4970634). The 2026-09-28 existing PAYOFF Actions analysis included **944 temperature effect rows from 28 studies and 279 species**. Its original `+0.421476` d/°C long-minus-short adjusted coefficient was already known, and the source manuscript clearly labels that original association prior art.

A study-by-study provenance screen of the exact 944-row **previously frozen derivative** identified a known noncompliant secondary source:

- `Hurlbert, A.H. & Liang, Z. (2012) Spatiotemporal variation in avian migration phenology: citizen science reveals effects of climate change. PLoS ONE 7:e31662.`
- Original article DOI [10.1371/journal.pone.0031662](https://doi.org/10.1371/journal.pone.0031662) explicitly states that it **downloaded and analyzed eBird checklists** for 2000–2010 in eastern North America. This provenance is explicit in the original paper's Materials and Methods; do not infer it from the study title alone.
- In the previously frozen E6 derivative, the study has **264/944 effects = 27.97%** of all eligible temperature effects: **190 long-distance, 74 short-distance**, representing **18 species**. Removing these rows is required by PAYOFF's **no-eBird source policy**, regardless of coefficient direction or significance.

Original archived source-derived artifact:
- Existing workflow [36383988920](https://github.com/zuizui0223/payoff/actions/runs/36383988920), GitHub artifact ID **10953792024**.
- Exact original artifact ZIP SHA256: `443cab62531d9b633aa6ee67da010fa66b6c230ef87e919d697269e77a7373f0`, verified again on 2026-11-19 against the downloaded unchanged GitHub artifact.
- Inside archive, `bird_temperature_short_long_rows.csv` has original-derived **944** rows, SHA256 `817a2d2d18931944103283c93e4d9bf80568906a21a92369ee168e4f8f203085`. Its source input is already hash pinned to original Usui CSV SHA256 `68816f6cbfccbb9b47b45be0df49f077db914c8e43e567d0ed2cac9bbafde56c`. No raw eBird checklists or eBird files are downloaded for this correction.

## Forced one-study exclusion result — do not choose a winner

Re-use **exactly the original E6 WLS/Study×Species two-way cluster model**, including the same source effect weights and covariates (arrival metric, temperature location, arrival location, data source, continent). Without refitting the full original source to the previous +0.421476 value within numerical tolerance, the correction script must fail closed.

| Parameter | Original E6, source-mixed | Excluding the explicitly eBird-derived study |
|---|---:|---:|
| Effect-size rows | 944 | 680 |
| Studies | 28 | 27 |
| Species | 279 | 279 |
| Long-minus-short coefficient (days/°C) | **+0.421476** | **+0.608389** |
| Two-way clustered SE | 0.146284 | 0.119956 |
| 95% CI (conservative Student-t) | [+0.121326,+0.721627] | **[+0.361817,+0.854961]** |
| p | 0.007672 | **0.00002781** |
| Degrees of freedom | 27 | 26 |

The magnitude becomes larger, not smaller, after excluding this one known eBird study. This is not a *new independent result*: the reduced estimate is the `+0.608389` endpoint already present in the existing E6 28-study leave-one-study-out audit. The scientific value is **correcting data-source compliance and making provenance explicit**.

The original Usui paper's source-level result is *prior art*, not proof that distance affects actual information access or that the thermal data are causal.

## Important remaining restrictions

1. **DO NOT LABEL THE 680-ROW PANEL FULLY EBIRD-FREE.** At this point the remaining **27 original studies have not each been authenticated for absence of eBird-derived input**. The correct label is **`KNOWN_EBIRD_STUDY_EXCLUDED; FULL_SOURCE_AUDIT_PENDING`**.
2. The original 944-row E6 reconstruction remains available only as pre-exclusion provenance; do not silently revise the frozen manuscript or claim the original includes no eBird.
3. Source Hurlbert & Liang (2012) was identified through **positive verification** that its paper used eBird, not selected because it had a convenient coefficient. This is a **forced post-open sensitivity**, not a prospectively preregistered independent test.
4. Other original meta-analyses may contain observational databases whose precise provenance remains unconfirmed. Treat unknown as **unverified**, not as proof of no eBird.
5. Neither the original nor reduced coefficient directly measures an organism's awareness of destination spring, its commitment time, recourse, feedback gain, route-stage urgency or interactor payoff. PAYOFF-B V7 `q×U` remains **NOT_ESTIMABLE**.
6. The separate source-only temperature-location interaction *support gate* in [PR #403](https://github.com/zuizui0223/payoff/pull/403) does not open or fit biological effects. It is not overridden by this sensitivity.

## Reproduction and expected tests

```bash
# Requires the exact prior GitHub Actions artifact ZIP (ID 10953792024)
python -m scripts.payoff_b_e6_known_ebird_exclusion \
  --artifact-zip /path/to/payoff-b-cross-system-information-distance.zip \
  --output outputs/e6_known_ebird_exclusion.json
python -m pytest -q tests/test_payoff_b_e6_known_ebird_exclusion.py
```

No original raw eBird data are fetched; the script accesses the known already-frozen published meta-analysis *derived effect rows* solely to omit them from the admissible sensitivity. Artifact retrieval is not equivalent to original individual-level observations.
