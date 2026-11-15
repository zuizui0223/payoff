# PAYOFF-B: original Monitoring Sites 1000 source discovery and first empirical join gate

2026-11-15. **Official source catalog verified, raw data not acquired or joined.**

## Official sources verified

- Ministry of the Environment Monitoring Sites 1000 data catalog: https://www.biodic.go.jp/moni1000/findings/data/
- Alpine monitoring: air/soil temperature, visual and camera flowering phenology, butterflies, bumblebees, vegetation.
- Forest/grassland: tree census, litter/seed fall, ground beetles and terrestrial birds. The forest/grassland terrestrial bird data page was updated 2026-06-15.
- Satoyama: bird census, butterflies and mammals. Satoyama bird methodology explicitly records species and counts along ~1 km routes, six visits each breeding and winter season: https://www.biodic.go.jp/moni1000/findings/data/index_file_bird.html
- Manuals: https://www.biodic.go.jp/moni1000/manual/
- Data usage/download includes a questionnaire/terms flow: https://www.biodic.go.jp/moni1000/question/question.html
- Tree census source instructions: https://www.biodic.go.jp/moni1000/data_file/TreeDataPackage.pdf ; original file revisions and provenance matter.

## Ranked first analysis

**First candidate: alpine within-site annual temperature–flowering–bumblebee/butterfly co-fluctuation.** Multiple original data types exist in one ecosystem monitoring program. Verify original site IDs, actual year overlap, flowering definition and repeated pollinator survey effort before any site-year join. Do not equate observation dates with activity-density curves or plant-pollinator interaction edges.

**Second candidate: forest bird counts versus independent resource dynamics.** Litter/seed fall measures resource flux but does not automatically measure bird diet, insect biomass or seasonal food availability. Tree census is not a direct g/m² biomass series. No H2 food-mismatch admission without independent relevant resource guild and bird demand timing.

**Third candidate: satoyama bird and butterfly population-year responses.** Counts have repeated seasonal visits but require effort/detection modeling; they do not directly identify migration arrival or departure.

## Connection to previous PAYOFF-B results

- PR #353–364 original JMA event dates establish exploratory annual timing co-fluctuation and strong plant-reference/site-selection sensitivity.
- PR #365 provides original Tokyo daily weather for 2019–2021 but lacks a certified station crosswalk and QA codes.
- PR #366 implements the source-gated monitoring/weather/biomass/demand bundle and rejects proxy substitutions.
- Existing PAYOFF-B two-clock theory predicts that common climate responses need not preserve usable overlap when physiological readiness, information and opportunity windows differ.
- The verified Hoge Veluwe great-tit/caterpillar archive offers a distinct *resource timing/fitness* validation track; it must not be treated as Japanese Monitoring Sites 1000 biomass or migratory arrival evidence.

## Hard stop

No Monitoring Sites 1000 raw ZIP/Excel original data has been acquired in this PR, so **site-year overlap, actual biomass coverage, ecological effects and cross-dataset regression are unknown**. The next work is to pass the official data access/terms workflow, obtain the raw source and digest, inspect real column schemas, audit site/year overlap, and only then fit H1. H2/H3 require further independent resource/demand/route measurements.
