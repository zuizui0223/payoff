# PAYOFF-B — first read-only published GPS-source admission audit

Date: 2026-10-19. **Source QC only, no biological effect opened.**

Archive: Kölzsch et al. 2016, greater white-fronted goose spring and autumn
migration, DOI https://doi.org/10.5441/001/1.31c2v92f.
Published study DOI: 10.1111/oik.03121. The official Movebank repository
describes 65 tracked geese, six study years, GPS and Argos files, and CC0
public archive metadata. Those numbers are source descriptions, not a newly
verified count of usable longitudinal individual-years.

The full archive landing page is
https://datarepository.movebank.org/handle/10255/move.519

Three original bitstreams (GPS CSV, reference CSV and README) were pinned to
the official public repository metadata, by bitstream UUID, size and MD5
before any source file was opened.

The read-only workflow verifies all three checksum pairs, counts valid
animal-ID/timestamp/location events and reports source coverage and errors
without uploading any individual tracks, animal identifiers or coordinates.
Only public CC0 archive URLs are accessed. Authentication, access-control
bypass and license acceptance automation are not attempted.

**Critical limitation:** This goose dataset may share cohorts with previously
opened PAYOFF goose records; no animal-level independence has yet been
established. Furthermore, event timestamps, animal counts and GPS columns do
NOT show when a bird received a decision-time environmental cue or whether
a reaction rescued fitness. No actionability theorem or coefficient is being
tested in this source QC.

A subsequent confirmatory dataset must have original-cue chronology, signed
incoming phase, independently estimated recourse, behavior, downstream timing
and an independent cohort. No post hoc coefficient is licensed by this audit.

References:
- https://www.movebank.org/cms/movebank-content/data-policy
- https://www.movebank.org/cms/movebank-content/data-repository
- https://doi.org/10.5441/001/1.31c2v92f
