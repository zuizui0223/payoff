# PAYOFF-B Wytham source admission: 2026-11-14

**Status: PUBLIC SOURCE METADATA AUDIT COMPLETE; DIRECT RESOURCE BIOMASS MODEL NOT ADMITTED.**

New external public records:

- Beck et al. (2022) EIDC, DOI 10.5285/ae6f821a-35a1-4a37-af4d-ca7cb1c83a10. Original catalogue reports nest-building, breeding-pair identity, first-egg date, clutch size, hatching, fledgling number and condition in great/blue/marsh/coal tits for 2020–2021. Publisher catalogue says Open Government Licence. This is a **resident bird** reproductive dataset, not a migrant movement dataset.
- EIDC ringing, DOI 10.5285/af4c9b5a-fba9-4133-b782-2a2cbc927280, for 2020–2021. Potential identity link, not source-verified at row level.
- Wytham long-term half-fall caterpillar phenology is described as the date by which 50% of final-instar winter moth caterpillars have been collected in traps, with interrupted annual coverage since 1961. A half-fall date is **not** measured annual prey biomass magnitude. Original manuscript: https://ora.ox.ac.uk/objects/uuid%3A7b0c37bb-ab3d-4133-9934-c7c3be13f028/files/s2v23vv22p
- New Dryad 2026 Wytham nestling/adult body mass and early-life conditions, DOI 10.5061/dryad.79cnp5jcc, includes mismatch to peak food availability and breeding density according to publisher metadata. **Bird body mass is not food resource biomass.** Original file schema, checksums and overlapping years have not yet been validated.
- López-Idiáquez & Sheldon (2026) EIDC DOI 10.5285/371f7553-42db-4da0-a062-76b5526ecaa7 contains 2023 canopy/understory data, which **do not overlap** the 2020–2021 bird breeding seasons.

These are **metadata-level admissions only**. No file bytes or row-level source joins were opened or fitted in this update. The 2020–2021 breeding outcome and the new Dryad body-mass study are promising independent source leads for a *resident-bird* resource-demand and reproduction bridge, but neither establishes direct daily caterpillar biomass in the inspected metadata.

A prior PAYOFF-B Hoge Veluwe dataset has verified caterpillar peak dates and great-tit recruitment fields, but no certified biomass magnitude in the specific resource table. The negative preregistered Hoge Veluwe cue-reversal gate stays closed.

## Executable source gate

- Registry: `data/payoff_b_wytham_resource_fitness_source_admission_20261114.json`
- Fail-closed audit: `scripts/audit_payoff_b_wytham_source_gate_20261114.py`
- Tests: `tests/test_payoff_b_wytham_source_gate_20261114.py`

No causal claim, cross-guild biomass effect, food biomass × fitness regression, or migration information mechanism is reported. The next required artifact is original source-verified repeated frass dry mass (sampling area/interval and temperature calibration), contemporaneous breeding demand windows, and compatible nest outcomes. If no direct resource biomass is available, the only valid estimand remains **phenological timing mismatch**, not prey biomass supply.
