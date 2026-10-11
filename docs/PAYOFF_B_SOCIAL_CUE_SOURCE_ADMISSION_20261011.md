# PAYOFF-B: social-cue source admission and novelty gate

Date: 2026-10-11  
Status: **PRE-OUTCOME SOURCE AUDIT — no new empirical endpoints opened**  
Base: `analysis/payoff-b-value-of-information-corridor-20261010`; frozen V3/V7R/V8 and Paper-2 V4 manuscript untouched.

## Corrected prior-art frontier

The generically phrased experiment “show flycatchers use heterospecific cues independent of real competitor presence” is **already prior art**, not a prospective novelty point.

- Samplonius & Both (2017), *J Animal Ecology*, DOI https://doi.org/10.1111/1365-2656.12640, randomly advanced/delayed resident tit hatch dates at the plot level in 2014–2015, observing the settlement/pairing response of migrant pied flycatchers. Late-arriving females differed in treatment response; males did not show the same settlement response. The intervention simultaneously changed resident state and its informative appearance. Dryad: https://doi.org/10.5061/dryad.bs427.
- Morinay, Forsman & Doligez (2020), *Animal Behaviour* 161:103–113, DOI https://doi.org/10.1016/j.anbehav.2020.01.002, used experimental playback of great tit song features with presentation decoupled from actual great tit pairs. Old collared flycatcher females differed in response by experimentally measured aggressiveness. Hence **pure social-cue playback influencing settlement and individual-quality moderation were already tested**; species differs (collared rather than pied flycatcher), and no direct cue timing × density × fitness identification is established by that headline.
- Samplonius & Both (2019), *Current Biology* DOI https://doi.org/10.1016/j.cub.2018.11.063, analysed fatal competition in the pied flycatcher–resident tit interaction. Raw replication dataset is declared at https://doi.org/10.34894/85y1hy (Groningen repository, eight files). Do not assume animal/year/site keys link to the 2017 Dryad experiment.
- Beck et al. (2024), *Animal Behaviour* 209:95–120, DOI https://doi.org/10.1016/j.anbehav.2023.12.010, experimentally shifted great tit density/social networks and **did not** detect a parallel patch-discovery change. Hence neither density → information uptake nor information → behavior may be assumed monotonic/universal.

These are source-derived reported results, not a new PAYOFF-B meta-analysis or individual-level join.

## Empirical admission target (2017 Dryad source only)

Dataset DOI: https://doi.org/10.5061/dryad.bs427. The public repository identifies exactly seven files:
- `arrival_early_late.R` — published analysis code;
- `arrival.csv` — flycatcher arrival data;
- `arrorder.csv` — sex-specific arrival order;
- `population.csv` — general breeding biology;
- `replicates.csv` — nesting box and subplot mapping;
- `swaps14.csv` — 2014 manipulation records;
- `swaps15.csv` — 2015 manipulation records.

Dryad API file IDs and sizes are fixed in `data/payoff_b_social_cue_source_manifest_20261011.json`. A third-party indexed metadata manifest independently confirms these IDs/sizes: https://github.com/Lakens/cooper-bes-validation-manuscript/blob/main/code/data/manifests/10_1111_1365_2656_12640.manifest.json.

**Run the source gate BEFORE assessing new treatment outcomes.** Attempt public, documented Dryad file URLs only; record ID, actual bytes, SHA256, header fields, number of rows and retrieval status. No correlation, model coefficient, subgroup difference, density threshold, reproductive success or sex effect is calculated in this stage. Raw values stay in the CI runner's temporary directory; only audit receipts become artifacts. A transport/format failure is `SOURCE_ACCESS_BLOCKED`, not a new negative biological result.

## Distinct prerequisites for a new question

Before any direct ecological test, require, in the **same identifiable observational unit or randomized unit**:

1. independent actual competitor state/density (H,d);
2. experimentally varied cue *availability* or reliability, with documented signal perception and a timestamp *before* the relevant choice (S,T);
3. known reversibility of the immediate selection/settlement decision;
4. contemporaneous competition cost and reproductive success or mortality (W);
5. cluster-level (subplot/year) assignment structure and enough independent units;
6. explicit direct-competition, photoperiod/calendar, arrival-order and local-forcing rival accounts.

**Source question only:** Does the 2017 archive actually contain all necessary columns and joining keys to consider a new conditional test, or only the outcomes of the original manipulation? An archive header does not establish that cues were independently randomized or sensed by migrants.

## Prospectively admissible / inadmissible tests

- Admissible **as published-result reproduction**: plot-level manipulation by female arrival stage, with author methods and R script; retain published reported estimates as prior art.
- **Not admissible as a newly causal information-value result**: deriving cue-belief accuracy from the outcome itself; treating manipulated real tit hatch as an independently randomized *informational* cue; inferring future reproductive fitness solely from settling/pairing probability.
- **Not admissible as a combined mortality test**: blending 2017 treatment outcomes with 2019 deaths using study-level means as if same individuals were followed. Require verified ID/year/geography and compatible observation process first.
- **Not admissible as novel**: a playback effect on settlement, by itself, since Morinay et al. 2020 already decoupled playback and actual tit pairs.
- **Potential new prediction, awaiting proper data**: with a predecision signal independently calibrated to future resources and an independently observed competitor density, information-induced settlement *and its actual fitness benefit* change with the time remaining to revise settlement decisions, not merely with arrival order.

## Stop / go

If source audit succeeds but independent S/H/T and W cannot be identified: `SOURCE_PASS_MECHANISM_NOT_IDENTIFIED`, use in Paper 2 as a **prior-art confrontation**, not as a new empirical estimate. If the source cannot be retrieved, `SOURCE_ACCESS_BLOCKED`. Rejected alternatives are not reasons to re-open the frozen V7R/V8 outcomes or to claim a new top-journal result.

## References

- Samplonius & Both 2017: https://doi.org/10.1111/1365-2656.12640 ; https://doi.org/10.5061/dryad.bs427.
- Morinay, Forsman & Doligez 2020: https://doi.org/10.1016/j.anbehav.2020.01.002.
- Samplonius & Both 2019: https://doi.org/10.1016/j.cub.2018.11.063 ; https://doi.org/10.34894/85y1hy.
- Beck et al. 2024: https://doi.org/10.1016/j.anbehav.2023.12.010.
