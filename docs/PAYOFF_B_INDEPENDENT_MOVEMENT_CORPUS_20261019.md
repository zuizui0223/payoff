# PAYOFF-B independent annual-cycle test: public tracking-source census

Date: 2026-10-19. Status: **metadata discovery / no animal outcome opened**.
Source: public DataCite DOI registry, fixed DOI prefix 10.5441 (Movebank Data
Repository); the API is queried exhaustively, not via handpicked species.

## Why this work is biologically necessary

Registered PAYOFF-B V7R and V8 tests did **not** support either a simple
historical-environment-predictability x remaining-route-recourse effect on
phase correction or broadly deteriorating source-to-destination spring
correlation. Additional post-outcome Amaral model shopping cannot turn these
failures into a new confirmation.

The *unresolved* biological question is: **when does a forecastable environment
actually become an actionable cue before migration and reproduction?**

That requires independent animal tracks and time-stamped decision windows,
not a new proxy derived from the same model's response.

## Frozen corpus-discovery protocol (before any raw outcome analysis)

1. Enumerate **all findable DOI records** with DataCite prefix 10.5441,
   respecting pagination and rejecting incomplete responses.
2. Retain every DOI even if its title has no English word for "bird" or
   "migration"; keyword flags are discovery aids, never automatic exclusion.
3. Preserve the DOI, publisher, title, year of **DOI publication**, resource
   type and rights metadata. DOI publication year is NOT movement year.
4. Do **not** download tracks at this stage. A Creative Commons identifier
   in DataCite does not prove event-level download permission or fulfill
   Movebank's licensing, citation and collaboration expectations.
5. Dedupe later on true study and deployment identities, not just names.
   Animals are not guaranteed to have unique identifiers between studies.
6. Publish the full registry and a machine-readable counts receipt regardless
   of whether there are enough candidate studies. No hidden targeted search.

Workflow:
- scripts/build_movebank_doi_registry.py
- tests/test_movebank_doi_registry.py
- .github/workflows/payoff-b-independent-movement-census.yml

## Prospective observational admission gates for a later study

These are future design specifications, **not** claims that DOI metadata pass.

- Obtain permission and license information for every candidate study, and
  archive full source citations, dataset DOIs and study-specific conditions.
- Establish actual bird identity from individual/deployment metadata; validate
  raw timestamps, latitude, longitude, sensor resolution and duplicates.
- Do not extrapolate an individual annual-cycle trajectory from one GPS point
  or mistake same-species observations for repeated individual tracks.
- Compute route/stopover transition geometry only from training animals/years,
  never from the outcome animal's future choices.
- Require independently dated vegetation/temperature cues from a fixed
  data source; use earlier environmental years only for predictive quality.
- Require at least two identifiable decision/checkpoint stages per migration
  with measurable subsequent signed movement or stopover change.
- Require multiple independent study/flyway clusters for confirmatory
  uncertainty, and reject unsupported species-level or event-level pooling.
- Treat reproductive success / survival as unobserved unless the tracking
  dataset actually provides independently measured vital rates.
- Require source cue onset to precede the relevant irreversible decision;
  the greenup midpoint measured *after* an animal has departed is not an
  actionable observation at departure.

The intended primary contrast, if eligible data exist, separates:

A. **Forecast information** learned at an upstream location about a future
destination's season (measured without using target-year future data);

B. **Local feedback information** revealed at the checkpoint before a
subsequent movement/stopover choice;

C. **Remaining feasible recourse** estimated without the focal individual's
subsequent action, e.g. independent movement/time envelopes.

Prediction: signed behavioral correction after a phase error may depend on
local cue value and recourse, even when historical *upstream* forecast
correlation does not explain correction. No sign of a new observational
coefficient is forecast as "supported" before measurement.

## Independence and prior-art guard

Exclude previously opened focal samples (Kölzsch et al. 2015 original goose
transitions; previously modeled Amaral source-target rows) from any putative
independent confirmation. Previously published species may appear in an
independent dataset only if the cohort and individual tracks truly differ.

Use source-study/flyway/year clusters, not repeated events as independent
biological replicates. A single study or a single spring cannot establish
macroevolutionary or global generality.

Before a confirmatory model is registered, conduct a **source eligibility
audit**, report study/taxon/year counts, and document whether cue chronology,
recourse and downstream outcomes are measured at all. Failure is a valid
result; do not lower biological gate thresholds until an effect appears.

## Limitations

This initial work is a **global published-source inventory**, NOT yet a
cross-species biological meta-analysis, database of annual-cycle events,
proof of cue use, or validation of the PAYOFF-B information deadline theorem.

Source documentation:
- DataCite REST DOI listing: https://support.datacite.org/docs/api-get-lists
- Movebank data repository: https://www.movebank.org/cms/movebank-content/data-repository
- Movebank data policy: https://www.movebank.org/cms/movebank-content/data-policy
- NASA MCD12Q2.061 phenology: https://doi.org/10.5067/MODIS/MCD12Q2.061

## Stop/go

This iteration is complete only when the independent DOI registry workflow
runs successfully and reports counts. Do not report a number of biologically
eligible tracks before actual route-level inspection.
