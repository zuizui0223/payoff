# PAYOFF-B Aikens environmental-product preregistration amendment

Frozen: **2026-09-22**

Status: **pre-outcome product amendment; Aikens lambda outcome remains unopened**.

## Why this amendment is necessary

The 2026-09-21 registration treated `MOD09Q1.006` as the preferred
study-faithful primary environmental source and `MOD09Q1.061` as a sensitivity
lane.

That routing is no longer operational. NASA LP DAAC announced that distribution
of MODIS Version 6 land products would cease and that V6 products would no
longer be available through Earthdata Search, the LP DAAC Data Pool, AppEEARS,
or USGS EarthExplorer. Version 6.0 was decommissioned on 2023-07-31. NASA directs
users to Version 6.1, which remains available through AppEEARS.

Official source:

- NASA Earthdata / LP DAAC, *MODIS Version 6 Land Data Product Distribution to
  End in July*:
  https://www.earthdata.nasa.gov/data/alerts-outages/modis-version-6-land-data-product-distribution-end-july-2023

This is an external source-availability change, not an outcome-driven retuning.

## Effective rule

From this freeze forward, the primary environmental reconstruction for the
Aikens within-mule-deer lambda perturbation is:

```text
MOD09Q1.061
+
MOD10A2.061
```

with the already frozen exact V061 request geometry.

The historical labels

```text
v061_sensitivity_only
study_faithful_v006_primary_if_materialized
```

are superseded **only as product-role labels**. They are not instructions to
rebuild the request manifest.

## Frozen request identity

The existing exact request stays unchanged:

```text
GPS observations:          64,539
unique MODIS 250 m cells:  10,899
unique cell-years:         19,500
year-scoped tasks:         24
manifest SHA256:
d50e69a20d6e65ec3426a8c938d1dea9d4e2f836c9bf07e02d30c560f5fa8463
```

Changing product role therefore adds no new spatial, temporal, taxonomic, or
outcome-dependent selection freedom.

## Confirmatory contract remains unchanged

The amendment does **not** change:

```text
independent test:
    aikens2022_lambda_perturbation_v1

phase coordinate:
    signed_days_relative_to_local_peak_IRG

segment scale:
    fixed_24h_spring_migration_interval

prediction:
    lambda_large-development
    >
    lambda_small-development

primary model:
    E_next
    ~ E_current
    + E_current:large_development
    + C(animal_year)

cluster uncertainty:
    animal_id

primary gate:
    delta_lambda_large > 0
    and p_difference <= 0.05

sample support:
    >= 10 animals per group
    >= 100 fixed-24h transitions per group
```

The same IRG reconstruction and quality rules must be applied to both
development populations.

## Interpretation boundary

This amendment licenses a **current-product reconstruction** of the registered
phase coordinate. It does not license the claim that V061 reproduces the exact
V006 pixel values or the exact published Aikens green-wave reconstruction.

Consequently:

- a passing lambda contrast supports the preregistered within-taxon forcing
  prediction under the frozen V061 reconstruction;
- a failing contrast remains a failure of that prediction;
- product-version replacement cannot be invoked post hoc to rescue the sign or
  p-value;
- any later V006 archive recovery may be reported only as a sensitivity or
  replication analysis after the V061 primary result is frozen.

## Machine contract

`data/aikens2022_environment_product_amendment_20260922.json`

The repository test suite checks that this amendment still points to the exact
frozen V061 manifest and does not alter the registered lambda contract.
