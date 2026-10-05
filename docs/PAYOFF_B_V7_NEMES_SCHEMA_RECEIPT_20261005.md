# PAYOFF-B V7 Nemes schema-gate receipt — 2026-10-05

Status: **PASS; FOCAL V7 OUTCOME STILL UNOPENED**

Workflow:
- GitHub Actions run: 37251451677
- conclusion: success
- artifact: payoff-b-v7-nemes-schema-gate
- artifact SHA-256: 83f8ec0f7fc6faca30c535e81b3b5541ed99f03d46458a2c462aeffa0b552c96

Public source:
Nemes et al. 2024 Zenodo record 10.5281/zenodo.10094686.

Source-object SHA-256:
- wide RDS: 903b4170cdd887450799d7b59b0af6dd8186e8607e5c666999ac3ff3fa470da0
- long RDS: 8c196b02d51c1c5ead2a455a46cecddbbf99acd925cbcc0b6ed31f85a1ca18f3

## Frozen schema outputs

```text
WIDE_ROWS = 102
WIDE_COLUMNS = 35
LONG_ROWS = 204
LONG_COLUMNS = 14
UNIQUE_INDIVIDUALS = 102
SPECIES = 4
TRACKING_YEARS = 4
SOUTH_SITES = 28
NORTH_SITES = 78
ROUTE_PAIRS = 92
```

All 102 wide records have nonmissing:
- individual ID;
- species;
- year;
- south detection day;
- north detection day;
- south receiver ID and coordinates;
- north receiver ID and coordinates;
- actual First Leaf spring onset at both receivers;
- 30-y average/anomaly First Leaf fields at both receivers;
- First Leaf phenological lag at both receivers;
- route distance;
- actual First Leaf green-wave rate.

NDVI fields are incomplete:
- south actual NDVI: 65/102;
- north actual NDVI: 81/102;
- NDVI green-wave rate: 63/102.

Therefore the predeclared **First Leaf primary route is retained** and NDVI is
not promoted to replace it.

## Admission gate

Predeclared minimum:
- >=50 individuals with paired timing/coordinates;
- >=10 unique route pairs;
- >=3 species.

Observed schema:
- 102 individuals;
- 92 route pairs;
- 4 species.

```text
V7_SCHEMA_GATE = PASS
FIRST_LEAF_PRIMARY = PASS_COMPLETE
NDVI_PRIMARY = NO
FOCAL_RECOVERY_SUMMARY_OPENED = NO
HISTORICAL_PREDICTABILITY_COMPUTED = NO
H1_MODEL_RUN = NO
```

## Consequence

The next permitted step is reconstruction of **pre-outcome historical
phenological predictability** at the frozen receiver pairs.

The predictor must be built without using:
- focal recovery values;
- focal V7 model results;
- focal-year phenology in the historical correlation.

No threshold or outcome definition changes are licensed by this receipt.
