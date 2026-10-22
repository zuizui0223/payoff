# PAYOFF-B strict fix-level stationary source overlap gate

Registered 2026-10-22 **after** observing the preliminary daily-centroid
misclassification patterns. This is a POST-OUTCOME sensitivity gate, NOT
new independent ecological confirmation.

The frozen full original 4-taxon source riskday census contained 7,368
daily-centroid 3-day stationary windows, but source fix-level QC found
substantial within-day excursions beyond the original 30km center in
later northward and other-outcome source days.

Strict sensitivity rule: retain an original riskday only if **ALL original
valid GPS fixes on EACH of the original 3 stationary anchor days** are
within the original 30-km daily-centroid site circle. No GPS thresholds
change, no new source days are selected, and no meteorological outcome is
opened at this stage. This strict rule may exclude actual foraging
excursions, so is a test of spatial-measurement quality rather than a
definition of true migratory rest.

The source-only QA previously found these exact strict subpopulations,
which must reproduce before any weather:
- stork 1,110 of 1,633 (85 northward labels; 716 stays);
- white-fronted goose 1,790 of 2,008 (93 northward; 1,324 stays);
- curlew 1,778 of 1,868 (42 northward; 1,585 stays);
- Egyptian vulture 1,257 of 1,859 (13 northward; 1,029 stays).

Build new NASA source request counts only for **strictly clean,
case/stay-labelled riskdays**. No bird IDs, original source grid cells,
dates, or GPS locations are exported. Before any further exploratory
reanalysis, require at least 10 clean later-northward source days with
an observed clean stay in the same original 0.5-degree grid×year×month,
>=5 such original fine source strata, and at most 500 unique monthly
weather requests. If any species fails this gate, it is
NOT_ESTIMABLE: do not relax boundaries, months or source exclusions.

Any future reanalysis that passes remains **post-outcome** and has a
different selected source population than the original all-daily-centroid
analysis, so apparent changes in a meteorological contrast must be
interpreted as measurement sensitivity, not a new experiment.
Prior V7R, V8, stork-53 and vulture-solar negative results remain unchanged.
