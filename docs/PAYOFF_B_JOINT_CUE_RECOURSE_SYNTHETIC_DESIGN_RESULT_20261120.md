# PAYOFF-B — synthetic factorial q×r assay planning result

**Date 2026-11-20. STATUS: SYNTHETIC DESIGN ONLY; ZERO BUMBLEBEES/PLANTS/BIRDS WERE ASSAYED.**
This is a Monte Carlo power/identifiability **design calculation**, not evidence for a natural cue×recourse mechanism or for full annual-cycle migration.

## Inputs, theorem and registered assay contract

The pre-simulation design and falsifiers are in docs/PAYOFF_B_JOINT_CUE_RECOURSE_PROSPECTIVE_ASSAY_20261120.md and the machine-readable contract data/payoff_b_joint_cue_recourse_experiment_contract_20261120.json.

The fixed binary witness is π=.4, false-early loss 2, missed-early loss 1, q∈{.65,.95}, independently assigned successful correction opportunity r∈{.20,.85}, fixed waiting cost D=.08. Thus q0=.75, high cue value .32, and the exact r-adjusted net values are:

| Treatment arm | Exact r×V(q)−D in the declared reduced model | Idealized information-use decision |
|---|---:|---|
| low cue / low opportunity | −.080 | no |
| low cue / high opportunity | −.080 | no |
| high cue / low opportunity | −.016 | no |
| **high cue / high opportunity** | **+.192** | only arm where using the cue is model-optimal |

A **positive treatment interaction on objective net loss** is thus possible in the declared model, **not guaranteed behavior by real organisms**. Calibration of reward penalties, cue distinguishability and physical gate opening is a separate admission requirement before real trials.

## Full 15-scenario Monte Carlo dry run

Exactly 300 simulation replicates, seed **20261120**, 48 independent episode draws **nested within each randomized colony**, colony-level baseline measurement variation SD=.08, within-colony compliance variation SD=.10. Compliance scenarios: **0% (true nonuse null), 50%, 75%**. The outcome is the planned colony-mean loss difference-in-differences, positive when high cue accuracy helps more when correction is available.

Values below are the **fraction of synthetic replications with a positive interaction whose approximate-normal lower 95% bound exceeds zero**. They are not experimentally measured power:

| Truly independent colonies / randomized treatment arm | Null: no cue use | Hypothetical 50% policy adherence | Hypothetical 75% policy adherence |
|---|---:|---:|---:|
| **8** | .030 | .267 | .483 |
| **12** | .037 | .337 | .590 |
| **16** | .043 | .380 | .763 |
| **24** | .023 | .590 | **.890** |
| **32** | .023 | .700 | **.980** |

Estimated synthetic mean interactions across simulated cluster means approximate the expected policy-dependent contrasts:

- true zero-cue-use control: near **0** (rounded from −.0032 to +.0018 across n);
- 50% policy adherence: simulated means **+.091 to +.098** reward-equivalent units, exact simple-model expectation **+.096**;
- 75% policy adherence: simulated means **+.137 to +.146**, theoretical expectation **+.144**;
- perfect Bayes-optimal policy without behavioral nonadherence has theoretical interaction **+.192**.

A policy-adherence scenario of 75% reaches the approximate 80% design-detection target **first at 24 independent colonies per arm** (96 colonies total). Under a less optimistic 50% adherence assumption, **none of the fixed 8–32 colonies-per-arm candidates reaches 80%** (32 per arm only 70%). **Do not call 96 real colonies feasible or sufficient** without an independent learning pilot, variance estimates, husbandry/resource assessment and independent ethical approvals. The experiment is currently a hypothesis test design, not scheduled or performed.

## Null-control code fault and repair

The first synthetic run inadvertently sampled colony compliance as a **Gaussian centered at 0 and truncated below at 0**, which made the supposedly zero-use null contain a small number of positive-compliance colonies. The signed synthetic contrast was biased positive (~.008 even under the intended null). This was a **model implementation defect**, not evidence of ecology or a case of a real subject responding.

The simulation was corrected to make **compliance exactly zero whenever the no-uptake null is selected**, with an additional regression test requiring identical source-state outcomes across all four assigned q/r arms under that sharp null and an approximate false-detection calibration test. The corrected null mean is close to zero and the original buggy null run is **superseded**. Frozen q/r settings, candidate sample sizes and main outcome definition were not retuned.

### Important uncertainty limitation

This code's **normal-approximation** cluster-level confidence interval is a planning heuristic; even in the corrected null the two-sided rejection fraction was **.073 at 12 and 16 colonies per arm**, above nominal .05 in these Monte Carlo runs. This warns against using small-cluster asymptotic normal tests for the actual experiment. The eventual primary inferential protocol must specify **colony-level randomization inference or a small-sample valid cluster procedure**, independent batches, blocked assignment and effective trial attrition before outcomes. A calibration p-value or simulated power from this script is **not** a substitute for that step.

## Exact artifact provenance / execution status

- Source branch [Draft PR #412](https://github.com/zuizui0223/payoff/pull/412), based on main.
- Source-only script scripts/payoff_b_joint_cue_recourse_design_sim.py and **9 source/falsifier tests** in tests/test_payoff_b_joint_cue_recourse_design_sim.py.
- GitHub Actions existing-test branch-only simulation [run 44681774335](https://github.com/zuizui0223/payoff/actions/runs/44681774335), dedicated synthetic job **SUCCESS**, suite **test SUCCESS**.
- Original aggregate-only result artifact **14605250518**, downloaded and independently inspected.
- Artifact ZIP SHA256 **9e5838cba4f18ce5ce3ff32159216a6e3e6ca99c1b16c2840d82649d3671c0b5**.
- Extracted original synthetic JSON SHA256 **10f58c30b20881e81e0b0f180b97f2d3afa006612955d3d6627b0bcbe4d65398**.
- Simplified machine-readable result receipt data/payoff_b_joint_cue_recourse_synthetic_design_result_20261120.json lists all 15 rounded estimates, false rejection frequencies, source hashes, and nonbiological status.
- Additional standalone original-source simulation Actions is configured; a conditional branch-only job was added temporarily to the existing test workflow to ensure numeric execution is verified while that newly introduced workflow is not being scheduled. This additional test job does **not** alter submitted theories or manuscripts; review/removal before any eventual merge is recommended.

**Scientific interpretation:** This demonstrates that the **prospective joint mechanism can be tested operationally**, under a fixed, explicit PAYOFF binary model and independent-colony assignment. It does **not** demonstrate a new biological cue response. The original theorem remains exact within its model; natural forecast-time×opportunity effects, phenological synchrony, reproductive fitness and partner hysteresis remain **UNTESTED**.

## Next external hinge

The experiment is not executable from GitHub alone. Real biological execution requires independent q-learning/cue-delivery and gate/payoff calibrations, ethical permissions, colony availability and a facility. One pilot should first estimate real learning/compliance and colony variance before selecting a confirmatory colony count; **do not use any future outcome-aware threshold modification**. Real winter→spring migration remains a separate, more difficult measurement problem.
