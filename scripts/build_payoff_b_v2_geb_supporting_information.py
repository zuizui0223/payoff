#!/usr/bin/env python3
"""Build concise PREOUTCOME Supporting Information for PAYOFF-B V2."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def build_supporting_information() -> str:
    deadline = load_json("payoff_b_information_deadline_theorem_20260927.json")
    trap = load_json("payoff_b_perfect_information_coordination_trap_20260927.json")
    rescue = load_json("payoff_b_information_rescue_coalition_theorem_20260927.json")
    broad = load_json("payoff_b_broad_predictive_connectivity_result_20260926.json")
    wigeon = load_json("payoff_b_wigeon_predictive_connectivity_result_20260926.json")
    longterm = load_json("payoff_b_cv24c_cue_driver_result_20260927.json")

    return f"""# Supporting Information — information deadlines and seasonal coordination

Status: working PREOUTCOME supplement. The registered industrial-development
phase-retention result remains unopened.

## Appendix S1. Exact information-deadline result

For the declared binary seasonal decision, define

- A = (1-pi) C_false-early;
- L = pi C_missed-early;
- R0 = min(A,L).

The cue becomes behaviourally actionable above

q0 = max(A,L)/(A+L).

An actor with delay cost D < R0 waits for the cue only above

q_wait(D) = [max(A,L)+D]/(A+L).

For two actors with D1 < D2 < R0, the exact asynchronous-use interval has width

Delta q = (D2-D1)/(A+L).

Canonical values:

- actionable threshold = {deadline['canonical']['actionable_threshold']};
- lower waiting threshold = {deadline['canonical']['lower_wait_threshold']};
- upper waiting threshold = {deadline['canonical']['higher_wait_threshold']};
- exact window width = {deadline['canonical']['exact_window_width']}.

## Appendix S2. Perfect-information coordination trap

At q=1, the old timing convention and the fully informed convention can both be
strict equilibria.

Canonical joint payoffs:

- old state = {trap['canonical']['old_joint_payoff_q1']};
- informed state = {trap['canonical']['informed_joint_payoff_q1']}.

The informed state has higher joint payoff while unilateral first adoption is
unprofitable for every actor.

## Appendix S3. Recovery coalition and temporary seed

For coalition member i,

G_i(K) = R_i - D_i - p I_i b_i(K).

For an uninformed actor exposed to temporary informed seed S,

H_i(S) = R_i - D_i + p I_i [2 a_i(S)-1].

Canonical minimum singleton rescue seeds:

- complete: any actor;
- chain: {rescue['canonical']['chain_keystone_rescue_adopter']};
- migrant-star: any actor.

These are exact results for the declared shared-cue game and are not management
recommendations.

## Appendix S4. Broad predictive-connectivity robustness

Primary preregistered pooled coefficient:

- beta = {broad['preregistered_primary']['coefficient']:.6f};
- 95% CI = [{broad['preregistered_primary']['ci_low_95']:.6f},
  {broad['preregistered_primary']['ci_high_95']:.6f}];
- p = {broad['preregistered_primary']['p_value_two_sided']:.6f};
- rows = {broad['sample']['analysis_rows']};
- species = {broad['sample']['species']}.

All leave-one-species-out coefficients retained the registered negative
direction, but dependence-aware cluster intervals and the species-level summary
cross zero. The licensed interpretation remains pooled directional support with
dependence-sensitive uncertainty.

## Appendix S5. Wigeon registered null

The registered origin-phase by predictive-connectivity interaction was

- beta = {wigeon['primary_interaction']['estimate']:.6f};
- 95% CI = [{wigeon['primary_interaction']['ci_low_95']:.6f},
  {wigeon['primary_interaction']['ci_high_95']:.6f}];
- p = {wigeon['primary_interaction']['p_value_two_sided']:.6f}.

Status: {wigeon['primary_interaction']['support_status']}.

This result separates pre-commitment predictive information from post-error
phase correction.

## Appendix S6. Long-term cue-driver recovery gate

Frozen status:

{longterm['status']}.

The preregistered decline-to-recovery geometry did not pass. The downstream
history model was therefore not opened. No natural information-recovery
hysteresis is claimed from this lane.

## Appendix S7. Capacity layer

The earlier moving-landscape programme is retained as a distinct capacity
result. Finite temporal adjustment can extend persistence and buffer immediate
route costs, but spatial movement re-enters under stronger sustained forcing.
Synthetic parameter values are mechanism illustrations and are not natural
threshold estimates.

## Appendix S8. Registered industrial-development supplement — pending

The registered fixed-24 h industrial-development phase-retention analysis
remains unopened at this PREOUTCOME stage.

The final Supporting Information must insert its frozen result without changing:

- the main title;
- the structured abstract;
- the T1–T3 information-deadline result;
- the T7–T8 perfect-information / recovery-failure result;
- the broad-bird, flycatcher or wigeon claim boundaries.

Until this registered result is frozen, the package is not final-submission
eligible.

## Source and claim boundary

All exact statements are restricted to their declared finite models. Natural
data support individual edges of the mechanism rather than a directly observed
full degradation–recovery network hysteresis sequence.
"""


if __name__ == "__main__":
    print(build_supporting_information())
