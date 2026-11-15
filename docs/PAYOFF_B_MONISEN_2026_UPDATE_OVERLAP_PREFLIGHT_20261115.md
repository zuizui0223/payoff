# PAYOFF-B Monitoring Sites 1000: 2026 original-data access and overlap preflight

**2026-11-15. No raw Monitoring Sites 1000 observation file has yet been downloaded or joined.**

## Newly confirmed official update and sampling

- 2026-11-12 official Monitoring Sites 1000 alpine data files updated: https://www.biodic.go.jp/moni1000/alpine.html
- Official 2025 alpine report lists Daisetsuzan, Northern Alps (Tateyama, Chogatake–Jonendake), Hakusan, Southern Alps (Kitadake), Fuji; program started in 2009 at Hakusan/Kitadake, expanded in 2010. Report https://www.biodic.go.jp/moni1000/findings/reports/pdf/2025_alpine_zone.pdf
- Annual physical temperature and flowering monitoring; visual flowering recorded every few days to one week within 10 × 20 m fixed plots, with *flowering stage and flowering amount*: https://www.biodic.go.jp/moni1000/findings/data/index_flowering-visual.html
- Camera flowering photo observations every 1–2 hours, but original photos are not downloadable from normal data-file pages; data sheets may be available: https://www.biodic.go.jp/moni1000/findings/data/index_flowering-photographs.html
- Bumblebee transect 2–3 km, once every 1–3 years, so it cannot support unqualified annual pollinator activity inference.
- Official data access requires reviewing terms and completing download questionnaire (which requests purpose and selected dataset channels): https://www.biodic.go.jp/moni1000/question/question.html . This user-directed form has **not** been submitted by the assistant; do not bypass or fabricate acceptance.

## Preflight script implemented

`python scripts/payoff_b_monisen_overlap_preflight.py --mapping mapping.json --output overlap.json`

Mapping format (illustrative **not actual Monitoring Sites 1000 column names**):

```json
{
  "flowering": {"path": "downloaded_flowering.csv", "site_column": "VERIFIED_SITE_COLUMN", "year_column": "VERIFIED_YEAR_COLUMN", "source_id": "OFFICIAL_FILE_AND_VERSION"},
  "temperature": {"path": "downloaded_temperature.csv", "site_column": "VERIFIED_SITE_COLUMN", "year_column": "VERIFIED_YEAR_COLUMN", "source_id": "OFFICIAL_FILE_AND_VERSION"}
}
```

The script requires explicit site/year columns, source identifiers, UTF-8 CSV and actual observations. It records source SHA256, row counts, invalid site/year rows, unique site-years, strict site/year intersection and number of sites with at least three shared years. It does not treat matching site ID strings as proof of a valid cross-protocol station crosswalk, and it does not infer phenological or climate effects. The script intentionally does **not** silently parse XLS/XLSX or Shift-JIS; those require independently documented original-file parsing and provenance-preserving conversion first.

## Decision gate

- If same-plot/year temperature and flowering original data are sufficiently overlapping, begin H1: temperature-anomaly × flowering-stage/amount annual panel, controlling survey effort and plot/species identity.
- If overlap fails, do not substitute a distant JMA weather station without spatial and temporal metadata.
- Only if bumblebee original sampled years and transects can be matched to flowering records should pollinator-plant H4 be tested, and then only at sampled-year grain.
- Do not infer actual resource biomass or pollinator abundance from flowering amount alone; those are separate variables.

**Next external dependency:** user completes official data download terms/questionnaire and provides the resulting original files or a connected, authorized source route. Then the preflight script can compute actual overlap immediately.
