# PAYOFF-B V8 matched between-within result — 2026-10-05

Status: **BETWEEN ASSOCIATION NOT SUPPORTED; WITHIN TRANSFER NOT SUPPORTED; DISSOCIATION NOT SUPPORTED**

This receipt records the result defined in
`docs/PAYOFF_B_V8_MATCHED_BETWEEN_WITHIN_CONTRACT_20261005.md`.

## Frozen matched sample

- 150 species-target-cell rows;
- 72 unique spatial source-target pairs;
- 22 species;
- two observations per species-target row: EARLY and LATE.

## Primary decomposition

Species-equal-weighted model:

`mismatch ~ period_late + z_between + z_within`

where:
- `z_between` = persistent route-level predictive connectivity;
- `z_within` = within-route deviation from that route mean.

Results:

- beta_between = **+0.01218**
- 95% pair-bootstrap CI = **-0.11108 to +0.08939**

- beta_within = **+0.05178**
- 95% pair-bootstrap CI = **-0.01170 to +0.11308**

- within-minus-between contrast = **+0.03960**
- 95% CI = **-0.04993 to +0.17550**

Frozen decisions:

`BETWEEN_INFORMATION_ASSOCIATION = NOT_SUPPORTED`

`WITHIN_INFORMATION_TRANSFER = NOT_SUPPORTED`

`BETWEEN_WITHIN_DISSOCIATION = NOT_SUPPORTED`

## Period-specific descriptive checks

EARLY:
- beta = **+0.03353**
- 95% CI = **-0.07947 to +0.14986**

LATE:
- beta = **+0.01122**
- 95% CI = **-0.13782 to +0.04680**

Neither period shows the negative route-level association predicted by the
matched-panel hypothesis.

## Consequence

The earlier 2026-09-26 pooled broad-bird association between higher
pre-outcome predictive connectivity and smaller mismatch does not reproduce as
a supported between-route effect in this stricter 150-row / 72-pair matched
panel.

Therefore the V8 lane should not be used to claim a clean
`high information -> low mismatch` cross-sectional relationship plus failed
within-route transfer.

The robust V8 statements remain:
1. source-destination spring connectivity increased strongly;
2. overall mismatch did not clearly improve;
3. larger connectivity gains did not predict larger mismatch reductions;
4. the apparent positive transfer slope is structurally explained.

## Provenance

Workflow:
- run: 37292709984
- job: 111706648237
- artifact: 11337572951
- artifact SHA256: 1c834c6f6f7922772c7c069fda380ceb8a82c0a4a3443b5990f66937d5011f3c
