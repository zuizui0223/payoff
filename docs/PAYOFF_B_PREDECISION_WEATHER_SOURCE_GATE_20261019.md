# PAYOFF-B first strictly pre-movement meteorological source audit

Date: 2026-10-19. Status: source-availability only, no hypothesis effect fitting.
The original predecision stationary→northward GPS source screen admitted
145 stork, 106 white-fronted goose and 59 curlew candidate transitions.
Its *same fixed criteria and file checksums* are rerun here and must match
before weather queries. Source stage movements remain observational proxies.

Before observing any meteorological outcome, up to 12 distinct source
animal-years per taxon are selected by a deterministic SHA256 key made
from original taxon, animal ID, year and the candidate date. Animal identity,
date, coordinates and hash are never exposed. Selection is deliberately
limited to a source-feasibility pilot, not a representative biological
sample. Multiple events in one animal-year do not become independent
replicates.

For each selected stationary→northward candidate, the source location is
the three-day stationary centroid. The meteorological reference is only
the full **UTC day before the last stationary day**. Raw WGS84 locations
are rounded to a 0.5-degree public grid *before* submitting queries to
NASA POWER's public hourly point API. Requests specify
\`time-standard=UTC\`, \`T2M\` and \`WS10M\`, one calendar day.
Any unexpected day, timezone, invalid wind or missing response fails the
per-event source availability gate. A day is usable only when at least
18 finite hourly temperature values AND 18 finite wind values are present.
All missing responses are reported, never imputed with future conditions.

Original NASA POWER documentation:
https://power.larc.nasa.gov/docs/services/api/temporal/hourly/

This is **reanalysis**: the physical temperature and surface wind fields
may have existed before the bird's first observed movement, but their
retrospective reconstruction does NOT prove an animal sensed or forecast
them. The stationary-to-northward detector likewise only brackets
movement at day scale. No externally measurable physiological feasible
response, route/stopover adjustment, breeding arrival or fitness endpoint
is estimated by this source audit.

If data coverage is insufficient, report the failure and do not relax
the chronological source gate to rescue PAYOFF-B.
