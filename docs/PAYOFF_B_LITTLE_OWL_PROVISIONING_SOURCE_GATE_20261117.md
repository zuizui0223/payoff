# PAYOFF-B: independent actual-provisioned biomass evidence gate (Little Owl)

Date 2026-11-17. **Source-only preflight; no new biological effect has been fit.** Source after the Scottish phase-specificity negative control (PR #392) and the blocked Seress provisioning Dryad (PR #393).

## Scientific purpose and nonnovel prior-art boundary

Sailas et al. (2026) *Ecology and Evolution* "Habitat-Dependent Provisioning Patterns Are Modulated by Weather Conditions in a Rapidly Declining Farmland Raptor", DOI **10.1002/ece3.72969**, openly reports 43,007 prey items provisioned to little-owl nestlings across 58 broods in 40 nests from four European countries over 2002–2022. It already reports high-quality habitat buffering weather effects on actual provisioning rate and mass. Data availability in the paper explicitly points to **Zenodo record 17521558**.

This is an independent bird species / data collection from Scottish blue-tit EIDC, **but it is not independent of the existing Little Owl paper**, and cannot be reported as a new discovery of provisioning or habitat buffering. The purpose is a *measurement bridge*: diagnose when visit frequency and **delivered food mass** cease to be equivalent measures of interspecific trophic transfer, and whether dates, habitat/weather, brood size and food quality are jointly measured. The dataset's existence does NOT imply availability of fitness, energy assimilation, bird decisions, remote cues or information-recourse tests.

## Source contract

- Fetch official anonymous Zenodo metadata by GET \`https://zenodo.org/api/records/17521558\`; record API payload SHA256, record DOI/title/version, license, list of original names, sizes, checksums and links. Never reconstruct a Zenodo public file URL from a guess.
- Only open original public file links returned by official record. Enforce explicit sizes, bytes and manifest checksum; reject redirected HTML, unknown auth or excessive files.
- For accessible .csv/.tsv/.xlsx or .zip source files within bounded size, enumerate **exact source columns, units and row counts**; identify if observations are per prey item, per nest-day, country-year, or per brood. Check prey *biomass versus counts*, exact date/time and prey class, sample effort, and unique nest/brood fields.
- No row-level model if site/brood IDs, sampling clock, or actual measured/estimated delivered prey mass columns cannot be identified. Do not invent daily exposure, consumption or inferred nutrient mass.
- Do not pool little-owl 40 nests with Scottish blue tit 44 sites or count them as comparable replication units; the prey measurements and outcomes differ.

## Planned guarded comparison (only after source audit)

If daily records have original delivered biomass and provisioning visit count with same nest-day, first report **biomass per visit** (g/visit, or estimated weight/visit if source uses allometric prey-class estimates) and check variation within brood and across temperature/habitat and prey guild. The null of identical information is delivered mass proportional to visits at a constant per-visit mass, after accounting for sampling duration. Hold out entire nest/brood and year/country where supported, with grouped uncertainty. The published paper's existing habitat/weather interactions are prior art and cannot be repackaged as novelty. A comparison against Scottish blue tit must be **qualitative**, not pooled numerical coefficients.

This is not an information-limited migration game. PAYOFF-B's eventual distinctive claim requires (i) cue available *before* irreversible action, (ii) actual destination state, (iii) partner/resource response, (iv) ability to correct after new information, and (v) measured fitness. Only a subset may be available in this Little Owl panel.

## Stop

If the public file has inadequate source columns, fails checksum, or lacks a comparable observation unit, record a machine-readable NO_GO with no fitted effects. Do not optimize lag, prey-guild weights, sample inclusion or country ordering after examining response data.
