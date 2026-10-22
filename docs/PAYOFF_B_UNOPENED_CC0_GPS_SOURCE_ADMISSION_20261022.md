# PAYOFF-B unopened bird-GPS source queue

2026-10-22. Frozen **before any new bird GPS outcomes were read**.
This is a public metadata admission ledger from the already frozen complete
446-parent Movebank Data Repository census, not a representative biological
sample or ecological information-use analysis.

Inputs are immutable GitHub Actions run artifacts:
- GBIF-exact-class 446-parent ledger from run 39212703373
- DataCite original full parent package metadata from run 39204043835
- Movebank DSpace publisher item taxonomy, permissions and Study IDs
  from run 39211112610.

The applicant population is every publisher record meeting ALL of:
1. Exactly one publisher bird species name, exact GBIF Aves-only class.
2. Explicitly published CC0/public-domain rights metadata.
3. A *GPS-named child file* in the original public package, not just
   a broad abstract or sensor-type guess.
4. >=10 publisher-reported animals and >=10,000 publisher-reported fixes.
   These are discovery criteria, NOT verified event-level measurements.
5. Recorded Movebank Study ID and original associated publication DOI;
   both must differ from all previously used/opened PAYOFF source datasets.
6. No previously used Movebank dataset parent DOI.

Every rejected package and **all exclusion reasons** remain in a complete
machine-readable 446-parent CSV. The initial review queue is at most 8
records with distinct publisher taxon strings, study IDs and publication
DOIs, ordered by recorded source animal count, location count then DOI.
No timing, phenological phase, movement direction, cue, reproduction or
fitness outcome influences this selection.

*Stage 1 does not establish data permission, individual independence or
actual GPS validity*. The next stage must use only publicly CC0 file objects
with official original MD5/size, inspect source field names and actual
individual-year/season coverage, and verify no repeated cohorts by original
deployment/animal IDs and cited paper records before any effect estimates.

A dataset may contain labels or release dates different from true animal
migration seasons. At least one prospective local cue, within-individual
decision opportunity and independently measured downstream timing or
fitness outcome are needed for a real PAYOFF-B ecological test. The
previously unsupported V7R/V8 and stork-53 tests are unchanged.
