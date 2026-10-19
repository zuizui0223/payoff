# PAYOFF-B public independent taxon intake — stork reproduction files

Date: 2026-10-19. Source: Rotics et al. 2018 JAE and Movebank Data
Repository, DOI https://doi.org/10.5441/001/1.v8d24552. License metadata:
CC0. Original study tracks 35 adult white storks over five years, with
movement/acceleration and reproductive context.

The original published package contains a JAE_meta_data.csv file with
individual/year/sex/fledgling count/breeding-attempt and a separate deployment
reference CSV. This workflow downloads and verifies only those small files and
the README using original file MD5 checksums, joins reproduction IDs to
deployment IDs, and reports aggregate completeness and missingness.

The GPS (~273 MB) and acceleration (~1.06 GB) files are explicitly NOT opened,
nor is any individual trajectory or individual identifying record uploaded.
Both are available from the original CC0 source but would require a separate
prespecified analysis and checks on event years, migration stages, environmental
information available *before* decisions, and annual fitness outcomes.

Fledgling counts are directly observed vital-rate-related outcomes, **not**
lifetime fitness, and their availability does not establish any PAYOFF-B
information x recourse coefficient. Previously published direct effects in
Rotics et al. are prior art; a future new independent mechanism must be
hypothesized and locked before consulting relevant movement-response outcomes.

Reference: https://www.movebank.org/cms/movebank-content/data-policy
