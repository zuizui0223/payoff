# PAYOFF-B: Rotics 2016 and 2018 stork cohorts cannot yet be deemed independent

2026-10-22. Read-only **source identity provenance** audit before opening
the autumn 2016 GPS/behavior or survival outcome.

Movebank CC0 sources: 2016 autumn juveniles/adults,
DOI `10.5441/001/1.hn1bd23k`, reference 122 rows; and 2018
previously PAYOFF-opened adult migration/reproduction source,
DOI `10.5441/001/1.v8d24552`, reference 36 rows. Both reference
original MD5 checksums were validated. Only de-identified aggregate
intersection counts were published, no bird ID, ring number,
tag identifier, nest or GPS position.

| Original public identity comparison | Result |
|---|---:|
| Exact shared `animal-id` strings | 0 |
| Exact shared `animal-ring-id` strings | 0 |
| Exact shared `deployment-id` strings | 0 |
| Exact shared `tag-id` strings | **35** |
| Of common tag IDs, both deployment on/off dates comparable | 2 |
| These with overlapping registered deployment intervals | **2** |
| Common tag IDs without comparable on/off dates | **33** |

The two apparently simultaneous registrations under the same tag string
could arise from identifier namespaces, copied metadata or track-device
policy, rather than one physical logger being attached to two birds at
once. These alternatives have not been reconciled. The 2016 source
has 66 juvenile and 56 adult reference rows; 'dead' deployment ends
are present but do not alone define verified survival duration or causes.

**Decision:** Do not treat 2016 and 2018 as independent experimental
or validation cohorts. A zero exact animal/ring/deployment-ID collision
is insufficient to prove distinct subjects, especially with unresolved
device ID namespace. Keep 2016 GPS outcomes sealed against
confirmatory PAYOFF-B reanalysis until original documentation or
authorized animal-level provenance is checked.

This is a provenance/methodology outcome only, not a biological
find of juvenile survival or PAYOFF-B information value.

Source audit: https://github.com/zuizui0223/payoff/actions/runs/39782552112
Machine receipt: `data/payoff_b_stork_shared_tag_timeline_result_20261022.json`.
