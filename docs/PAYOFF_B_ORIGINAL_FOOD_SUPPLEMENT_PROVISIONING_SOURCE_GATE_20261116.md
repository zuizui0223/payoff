# PAYOFF-B biological interaction conversion: feeding vs available caterpillar source gate (2026-11-16)

**Stage: original-data metadata/row-grain admission only. NO new empirical effect fitted.**

## External, independently collected experiment (candidate)

- Seress, Sándor, Evans & Liker (2020), *Journal of Animal Ecology*, "Food availability limits avian reproduction in the city: an experimental study on great tits (Parus major)", DOI:10.1111/1365-2656.13211.
- The original linked Dryad release DOI:10.5061/dryad.qbzkh18dj, "Food availability limits avian reproduction in the city: an experimental study on great tits (Parus major)." Dryad publisher page states that the package contains **provisioning video records, nestling mortality and nestling biometry** with original variable definitions on each Excel workbook's `readme` tab.
- Published paper already demonstrates that experimental supplemental food largely eliminated urban-vs-forest nestling survival and size differences. This is the **prior-art result**. We cannot claim to rediscover food limitation or food supplementation's causal effect from its raw data.

## Precise scientific gap and why a second source is necessary

PAYOFF-B Scotland EIDC site-year observational study (PRs #389–#392) established that available source **mass per standardized branch beating** can predict fledging in a narrow model, but the effect did **not** show hatch-specificity once sampled-season mean food mass was controlled, and early nestling body mass had no robust mass-specific incremental prediction. That source has **no directly observed feeding/provisioning events**, diet selection, realized ingested mass, forecast cues or movements.

An experiment with source-verified video feeding and body condition can potentially separate:
1. Upstream experimental input (supplemented food), treatment allocation, year/habitat/effort;
2. **Actual parental provisioning** (timestamped visit frequency, delivered prey identity, or estimated volume if directly recorded);
3. Nestling development, mortality and reproductive outcomes.

But do not conflate provisions with measured ingested biomass, a population-wide resource supply curve, a cooperation coordination game, or a migrant's inaccessible destination information. Reusing a published experiment is supporting external mechanism calibration, not independent novel confirmation.

## Source-access and strict provenance preflight

- Use anonymous public official Dryad API documented at https://github.com/datadryad/dryad-app/blob/main/documentation/apis/README.md . The canonical dataset API is GET /api/v2/datasets/doi%3A10.5061%2Fdryad.qbzkh18dj, followed by published versions and per-version file metadata. Do not fabricate download URLs, guess private files, authenticate without authorization, or bypass download controls.
- Record official dataset DOI, publication year, source license, version IDs and file IDs, source file sizes, checksum/digest, content SHA256, precise original Excel sheet names, first-row variable names and row counts.
- No claim of matching observational Scotland (different place, species/experiment/site-years); their numerical coefficients are not pooled.
- Only download bounded openly available source workbooks. Strict fail-closed on source digest mismatch, unknown file format, inaccessible/raw data denied, or ambiguous nested identifiers.
- **No original outcome fit until a separate design is explicitly frozen before opening new effect coefficients.** The original Seress et al. 2020 published treatment result is *already known*, so any new analysis is exploratory.

## Data availability decision

At this stage, the original Dryad landing page lists Excel sheets for provisioning videos, mortality and morphology and reports a linked publication; row-level source joins remain **unverified** until the admission script succeeds. Even success cannot prove a mechanism without the original manipulation, visit timing, prey identity, nest and chick identifiers, effort, and planned outcome structure.

## Next admissibility gate

Prefer one study system in which independent source **resource quantity**, realized parental provisioning, and chick condition are all observed. Check nested keys (source observation > feeding session > nest > individual), age alignment and manipulation assignment. Do not infer prey biomass from a video frequency or a food-assistance treatment label. The intermediate interaction pathway is the target. The overarching PAYOFF-B information/recourse hypotheses still need separate source data on cue access, commitment and adjustment.
