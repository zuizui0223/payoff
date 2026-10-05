# PAYOFF-B V8 actuator bridge result — 2026-10-05

Status: **NOT ESTIMABLE UNDER THE FROZEN ADMISSION RULE**

The descriptive migration-speed actuator bridge was defined in
`docs/PAYOFF_B_V8_ACTUATOR_BRIDGE_CONTRACT_20261005.md`.

## Frozen admission rule

For each V8 species-target-cell row:
- annual speed = finite positive `vArrMag`;
- outcome scale = `log(vArrMag)`;
- require at least 6 finite speed years in 2002–2009;
- require at least 6 finite speed years in 2010–2017.

The analysis also required at least:
- 20 eligible species-target rows;
- 20 unique spatial source-target pairs;
- 5 species.

These thresholds were not relaxed after outcome access.

## Admission result

Eligible data:
- species-target rows: **5**;
- unique spatial pairs: **4**;
- species: **4**.

Therefore:

`V8_ACTUATOR_BRIDGE = NOT_ESTIMABLE`

No connectivity-change -> migration-speed-change coefficient was computed.

## Consequence

The Amaral source is too sparse in repeated `vArrMag` observations across
both V8 windows to provide a defensible temporal actuator bridge.

This is an availability limitation, not evidence for or against speed-mediated
information use.

The paper should not use the V8 lane to claim:
- that migration speed changed with predictive connectivity;
- that speed failed to respond;
- that downstream recourse is absent.

Those mechanism claims remain anchored in independent individual-level systems
such as the mule-deer and published compensation examples.

## Provenance

Workflow:
- run: 37296006485
- job: 111717256613
- artifact: 11339430514
- artifact SHA256: 999342c14cbf8449d5efc559b9d80a973d7d1075308c703ada2f48b1b40ecdf3
