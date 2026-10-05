# PAYOFF-B V7 USA-NPN source-gate receipt — 2026-10-05

Status: **PASS; HISTORICAL PREDICTABILITY STILL UNOPENED**

Workflow:
- GitHub Actions run: 37251917013
- conclusion: success
- artifact: payoff-b-v7-usapn-source-gate
- artifact SHA-256:
  1ac5bd4532859f6cd6037aaf998e1ca96953254448e30f4a467670697d9fd431

Source:
USA National Phenology Network historical annual First Leaf Spring Index
(PRISM), WCS layer `si-x:average_leaf_prism`.

## Spatial coverage result

```text
TOTAL_INDIVIDUAL_ROUTES = 102
SOUTH_RECEIVERS_INSIDE_PRISM = 102
NORTH_RECEIVERS_INSIDE_PRISM = 87
INDIVIDUAL_ROUTES_BOTH_INSIDE = 87
TOTAL_ROUTE_PAIRS = 92
ROUTE_PAIRS_BOTH_INSIDE = 77
SPECIES_BOTH_INSIDE = 4
```

Frozen source gate:
- >=50 individual paired routes: PASS (87);
- >=10 unique paired routes: PASS (77);
- >=3 species: PASS (4).

Therefore the predeclared PRISM source remains the **primary V7 historical
predictability source**.

The pre-result BEST fallback is not activated. BEST remains only a
predeclared spatial/source sensitivity if later executed; it may not replace
PRISM because of a favorable focal result.

## WCS availability result

The source-gate workflow successfully retrieved the 2015 annual First Leaf
GeoTIFF via WCS 2.0.1.

```text
FILE_TYPE = TIFF image data
WIDTH = 1405
HEIGHT = 621
BYTES = 3146180
SHA256 = 19ff8306166491764cb6c4aa744f276053ee07b2d5e5b5cb94d1b0d66a14db9f
```

No raster pixel value was reported or summarized by the gate.

## State after gate

```text
V7_USAPN_SOURCE_GATE = PASS
V7_PRIMARY_SOURCE = PRISM_FIRST_LEAF
PRIMARY_ANALYSIS_ROUTES_MAX = 87
PRIMARY_ROUTE_PAIRS_MAX = 77
SPECIES = 4
HISTORICAL_PIXEL_VALUES_OPENED = NO
PREDICTABILITY_VALUES_OPENED = NO
RECOVERY_OUTCOME_OPENED = NO
H1_MODEL_RUN = NO
```

The next allowed step is outcome-blind extraction of historical First Leaf
values and route predictability for the 87 spatially eligible individual
routes.
