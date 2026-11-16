# PAYOFF-B: source-verified Little Owl biomass-per-visit conversion test
Date: 2026-11-17. Frozen after source-file/row audit but BEFORE the new fit. Exploratory *measurement bridge*, not new evidence of food-fitness or climate-information games. The primary paper Sailas et al. (2026), DOI 10.1002/ece3.72969, already examined habitat, weather and delivered biomass.

## Original source and fail-closed grain
- Original Zenodo record 17521558; Littleowl.dat.JAB.csv sha256 75042cdbd0f4019519b51ea1273ebbf8a736712f43fa7024361d969d752b0928; all_hab_vars.csv sha256 8fcbaee54b4a8af215b7952e6cad2d5fc5fce47917f2e296ef87d4421ef028c3. Both official MD5 checksums verified.
- Source has 952 brood-day rows and 40 nest habitat records. Original country groups are unbalanced and have different observation histories. A reference paper reports 43,007 prey items: prey items are NOT independent brood days.
- Four conflicting (broodID, day) rows occur in German 2012 data for three broods: KW0222012, OF0922012, PO0612012; original age differs for the same brood and calendar day. Exclude **all rows from these three broods** from every model, preserving an exact exclusion receipt. No convenient selection of the first duplicate. If other duplicates persist, NO_GO. This QC decision was frozen prior to any new conversion fit.
- Original prov_rate2 and BM2 adjust for fractional monitored days (prop.day.monitored); their ratio is g estimated delivered per visit, conditional on positive visits and positive biomass. BM2 is source-estimated food mass delivered, not ingested energy or independently weighed prey. For null mass visits, report separate excluded rows rather than invent conversion. Only source brood ages 1–30 admitted.
- Habitat composition: use (Grassland area + Garden area + Hedges area + Orchard area)/151976 from original R script. Check finite numeric area and proportion in [0,1]. Do not treat area as exact available prey biomass.

## Pre-fixed models and validation
One observation = one source-verified brood-day; every brood is given total train weight 1, independent of how many days recorded. No pseudo-independent day-level inferential p-values.

Let v = source prov_rate2, m = source BM2 and q=m/v in g per observed provisioning visit.

- M0: universal training-only brood-balanced mean q; predicted m=v*q0.
- M1: training-only brood-balanced ridge lambda=1 to predict q using source brood age, temp, wind, number_juv.x and original high-quality habitat fraction. Intercept unpenalized, predictors standardized only in training and negative predicted ratios clipped to zero. Predicted m=v*q_pred.
- M2 (oracle *diagnostic* only): M1 plus prey-type shares **observed after delivery** (mammal, bird, insect, earthworms, other). This is NOT a prospective decision-time cue. Do not divide by visit count to create shares unless original prey categories are source verified as same measurement currency; fractions use sum of category counts if >0.

Primary: hold out entire nestID; secondary: hold out entire broodID, plus country as descriptive. Crossvalidation MSE in squared original estimated g delivered per day, equal heldout nest weighting; record pooled equal brood-day MSE as secondary. No country-specific baselines on heldout country.

Admit only with >=700 valid days, >=45 unique broods, >=30 unique nests, >=3 countries and >=10 years. **Exploratory M1 pass** requires MSE(M0)-MSE(M1)>0 in both nest- and brood-heldout designs, >=60% of heldout nests improved, and a non-Germany robustness panel (if >=20 nests, >=2 countries) that has the same positive signs. Otherwise HOLD. M2 cannot rescue a failed M1 because its prey shares are not available before delivery.

Do not posthoc optimize date windows, country partitions, predicted-prey composition or model penalties. A fitted correlation is not the value of forecast information, an interaction game, causal resource-to-fitness conversion or a biological survival effect.

## Missing mechanisms
The source measures delivered prey mass estimate and visits but NOT independent prey field biomass, chick condition/fledging/recruitment, available migration cues or recourse. The direct observation chain is: available prey stock [unobserved] -> visits [observed] -> delivered mass [source estimated] -> consumer fitness [unobserved]. Keep this boundary explicit; do not pool owl coefficients with Scottish blue tit datasets.
