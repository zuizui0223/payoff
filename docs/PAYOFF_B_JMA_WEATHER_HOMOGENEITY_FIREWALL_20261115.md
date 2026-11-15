# PAYOFF-B JMA weather: homogeneity-number firewall

**2026-11-15 | code and tests, NOT a fitted weather effect**

Official JMA historical CSV instructions (https://www.data.jma.go.jp/risk/obsdl/top/help1.html) explicitly state that the downloaded numeric dataset includes **均質番号 (homogeneity numbers)** and that values with different homogeneity numbers require caution when compared. Original CSV settings also allow quality flags and indicators for nonhomogeneous observation periods (https://www.data.jma.go.jp/risk/obsdl/index.php).

This is distinct from the JMA biological-phenology `rm` codes, which are NOT weather homogeneity numbers. The previous weather importer retained quality flags but discarded homogeneity numbers. That would permit a spurious phenology–weather association from station moves, instrument or observation changes.

Changes:
- `src/japan_phenology_jma_daily_import.py`: optional source-mapped per-variable `homogeneity_columns`, retained with each date/variable, never inferred from a value.
- `src/japan_phenology_jma_homogeneity.py`: requires a single station and date-valid history, audits measured days by original homogeneity regime, rejects missing regime codes and blocks unstratified time-series modeling across multiple regimes.
- Tests verify one regime admission, multiple-regime rejection, missing regime fail-closed, and CSV preservation of original regime numbers.

**Not yet completed:** original daily JMA CSV acquisition and source-specific column mapping for each station; original quality code meaning certification; measured weather–phenology fit; NDVI or measured resource biomass. Do not treat synthetic regression fixtures as measured weather data.

Next real-data priority: obtain one modest original JMA daily CSV covering the same official station and phenology dates, verify header/quality/homogeneity mappings, then scale by station/variable and date after confirming allowed source acquisition and station identity.
