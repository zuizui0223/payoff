# PAYOFF-B V8 transfer structural-null result — 2026-10-05

Status: **POSITIVE TRANSFER SLOPE STRUCTURALLY EXPLAINED; NEGATIVE TRANSFER REMAINS NOT SUPPORTED**

This receipt records the audit frozen in
`docs/PAYOFF_B_V8_TRANSFER_STRUCTURAL_NULL_CONTRACT_20261005.md`.

## A1 — baseline-rho adjustment

Equal-species weighted coefficient on V8 delta-rho after adjusting early-window
rho:

- beta = **+0.06308**
- 95% unique-pair bootstrap CI = **-0.02411 to +0.26730**

The point estimate remains positive, although uncertainty is wide.

## A2 — fixed-arrival environmental-geometry null

Holding each species-target cell's bird arrival date fixed at its 2002–2017
mean while allowing target green-up to vary produced:

- fixed-arrival-null beta = **+0.04742**
- 95% CI = **-0.04076 to +0.12269**

Observed primary beta:
- **+0.06244**

Observed minus fixed-arrival null:
- bird increment = **+0.01502**
- 95% CI = **-0.05212 to +0.10273**

Thus no bird-specific increment is detected relative to this
environmental-geometry null.

Frozen audit status:

`STRUCTURAL_EXPLAINED = YES`

`BIRD_INCREMENT_DETECTED = NO`

## A3 — within-window arrival permutation

Permuting annual bird arrival dates within EARLY and LATE windows separately,
while preserving each cell's window-specific arrival distribution and mean,
gave:

- 2,000 permutations;
- null median beta = **+0.04677**;
- null 2.5–97.5% interval = **+0.01312 to +0.08188**;
- observed beta = **+0.06244**;
- fraction null <= observed = **0.8105**;
- fraction null >= observed = **0.1895**.

The observed positive beta is therefore not unusual after year-specific
arrival–green-up alignment is destroyed.

## A4 — baseline/change coupling

Across the 72 eligible unique environmental pairs:

- cor(rho_early, delta_rho) = **-0.7990**
- 95% pair-bootstrap CI = **-0.9008 to -0.6636**.

The V8 change score is strongly coupled to its baseline value, as expected for
bounded noisy correlation changes. This reinforces the decision not to
interpret the raw positive transfer coefficient as a bird response.

## A5 — Fisher-z transfer

Using Fisher-z change rather than raw-r change:

- beta = **+0.08867**
- 95% CI = **+0.01672 to +0.16213**.

Thus the absence of the preregistered negative transfer is not caused by the
raw-r scale. The positive sign itself remains subject to the structural-null
interpretation above.

## Final licensed conclusion from the V8 transfer lane

The defensible result is:

> Source-destination spring predictive connectivity strengthened strongly
> between the two periods, but larger connectivity gains did not translate into
> larger reductions in migratory-bird arrival–green-up mismatch.

The data do **not** support saying:

> increasing predictability worsened bird mismatch.

The apparent positive association is reproduced by fixed-arrival and
within-window-permutation nulls and therefore is not licensed as a biological
bird response.

## Ecological implication

Within this sampled system, broad degradation of environmental predictive
connectivity is not a viable explanation for the persistence of phenological
mismatch. Improving environmental predictability is also not sufficient, by
itself, to guarantee improved realized timing.

This is compatible with a distinction between:
- environmental information quality; and
- the biological ability/opportunity to convert information into timing
  adjustment.

The V8 lane alone does not identify the second component mechanistically.

## Provenance

Structural-null workflow:
- run: 37291407274
- job: 111702414654
- artifact: 11337415962
- artifact SHA256: 54b260d19383aa7fee862ef3023e0a1080f218ef1dd3ed7257a52318019af360
