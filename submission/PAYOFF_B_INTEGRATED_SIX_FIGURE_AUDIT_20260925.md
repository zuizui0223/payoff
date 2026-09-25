# PAYOFF-B integrated six-figure audit — 2026-09-25

Status: **PASS — canonical adopted PREOUTCOME six-figure set**

## Canonical render

- workflow: `Integrated PAYOFF-B six figures`
- validated PR head SHA: `cc8674cefecf0a09b85ac25446275b5bdc44dc4b`
- adoption merge commit: `572b3a63de54a6a9abf46739108ed57ee8a876f9`
- workflow run: `36106665345`
- artifact: `payoff-b-integrated-tracking-six-figures`
- artifact ID: `10851039331`
- artifact SHA256: `c6529f1f16b6df25dbff6fa7cf1c37bc11536b0b1792a5f65ddda93378bc62be`

The artifact expands to exactly six SVG figures plus one machine manifest.

## Outcome boundary

```text
aikens_outcome_opened = false
```

Figure 6 therefore contains the preregistered within-taxon Aikens slot as
`UNOPENED`. The figure set contains no inferred, guessed or manually inserted
Aikens lambda result.

## Figure hashes

| Figure | File | SHA256 | Provenance |
|---|---|---|---|
| 1 | `PAYOFF_B_INTEGRATED_FIG1_CONCEPT.svg` | `34fc00c0b117bf8e7d6e1cb39cebde860f92afc01eea70bb127386a7ebcce0b6` | integrated conceptual synthesis; no new quantitative result |
| 2 | `PAYOFF_B_INTEGRATED_FIG2_TEMPORAL_BYPASS.svg` | `166202cb17e74cca857afcb383038a8e082d5337a78a35dd7fab3bbda50375dc` | frozen 2026-09-20 synthetic receipt chain |
| 3 | `PAYOFF_B_INTEGRATED_FIG3_COORDINATION_GATE.svg` | `f34f60a63590b7c7ea101b9c55c680f30786aee6a1a3f1ec7f9c654d819c4591` | frozen 2026-09-20 synthetic receipt chain |
| 4 | `PAYOFF_B_INTEGRATED_FIG4_BROAD_BIRD.svg` | `1f0aa3de78be965d14162cf22d7081a56750a3447ab5516c53f9061828538a6e` | frozen Amaral Stage-1 workflow artifact materialization |
| 5 | `PAYOFF_B_INTEGRATED_FIG5_DIRECT_SYSTEMS.svg` | `b5c0230ee5edb19ee9452d69b2a2c38ce34995dd40245a15d549cdeeb5b66295` | machine direct-system + interval-standardization receipts |
| 6 | `PAYOFF_B_INTEGRATED_FIG6_INFORMATION_ACTUATION.svg` | `e83e38f6f47c62b92f5628612d3411dfb7e7061e1a3dc935ab1cf14425c3001b` | machine innovation / industrial-actuation snapshot + unopened Aikens slot |

## Figure 4 provenance closure

The previously missing broad-bird provenance is closed by:

- original Stage-1 workflow run `35328297725`;
- original artifact ID `10540282539`;
- original artifact SHA256
  `0ec049f6f325c63144d68950831e1afeae14e64d027d59de4d439e87c24b1c34`;
- analysis head `9c8d66aa3c71ee873643c25c5b9bfb0378ea0fbb`;
- materialized machine receipt
  `data/payoff_b_broad_bird_stage1_result_20260925.json`.

The materialized receipt binds hashes for `stage1_summary.csv`,
`stage1_gam_minima.csv`, `stage1_optimum_uncertainty.csv`,
`stage1_species_summary.csv`, `stage1_gam_curves.csv` and
`stage1_species_vertices.csv`.

## Publication implication

The integrated paper no longer has a figure-generation or Figure-4 provenance
blocker before the Aikens result.

Remaining scientific state:

```text
INTEGRATED_MANUSCRIPT = PREOUTCOME
FIGURE_ARCHITECTURE = COMPLETE
BROAD_BIRD_MACHINE_PROVENANCE = COMPLETE
DIRECT_SYSTEM_MACHINE_PROVENANCE = COMPLETE
AIKENS_LAMBDA_OUTCOME = UNOPENED
```

The two-paper publication architecture is adopted. The existing frozen Oikos
and GEB sources remain rollback/provenance sources and are not submitted as
separate overlapping papers while the integrated paper is active.
