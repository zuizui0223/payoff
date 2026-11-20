# PAYOFF-B: information reliability × retained corrective opportunity — prospective factorial pilot

**Date: 2026-11-20. Status: prospective experimental PROTOCOL + synthetic planning only; no animals tested.**

This branch operationalizes (without replacing or refitting) the exact actionability theory in theory/ACTIONABILITY_BALANCE_THEOREM.md, the two-clock identification limits in theory/TWO_CLOCK_IDENTIFICATION.md, and the already frozen empirical signature in data/payoff_b_actionability_peak_empirical_contract_20261002.json. Nothing is added to a submitted manuscript as a new theorem or positive result.

## 1. Why a direct experiment is necessary

PAYOFF-B now has published component evidence but **no joint natural q × r test**. Rüppel et al. 2023 had 178 temporally linked departure/route/landing birds, but only 3 sea-crossing landings, below the predeclared support for an independent route × landing/recourse analysis. Lameris et al. 2025 randomized red knots to 6, 12 or 24 h/day food access and already published faster departure, but the accessible derivative lacks the bird-to-aviary crosswalk needed for an independent correctly clustered re-fit. Klinner et al. 2025 already published reduced favourable-tailwind selectivity among longer-route, higher-urgency migrant species. Simple information, departure, stopover and physiological-access headlines are prior art.

A single experiment must independently vary **forecast reliability delivered before choice** and **the availability of useful correction after choice**, on the **same** decision and objective payoff scale. Neither experiment above supplies the interaction.

## 2. Proposed ecological mechanism-proxy assay

**Biological system:** trained bumblebee foragers choosing between two artificial floral-receptivity / nectar reward patches in a contained flight arena. The patch's future receptive/reward state is determined by an independent controller, not inferred from the bee's eventual movement.

This is an **hours-long controlled foraging analogue**, NOT a test that migrating birds perceive destination spring, and NOT field-scale plant–pollinator population synchrony. If conducted, appropriate local ethical, husbandry and welfare review and adequate colony nutrition apply; do not impose harmful food deprivation.

**Randomization unit: entire independent colony.** Randomly assign each colony to one of four q × r treatments:

| Assigned factor | Low | High |
|---|---:|---:|
| Reliability of advance hidden-state cue q | 0.65 | 0.95 |
| Chance of a physically feasible corrective branch r | 0.20 | 0.85 |

Foragers and visits are nested **within** colony, not independent experimental units. Cue medium, visual intensity, initial patch, reward source, observation schedule and base feeder access are kept fixed across arms. An independent external controller generates hidden states, cues and gate-open assignments; its logged cue timestamp must precede the final commitment decision. Colonies do not cross between q treatments to avoid learned-cue carryover. A separate cue-arrives-after-closure sham condition is a *negative control* only, not part of the primary 2×2 comparison.

**No cognitive uptake assumed.** Birds and bees may ignore signals or act on other cues. Actual cue discrimination is separately checked, and a behavioral failure is a possible falsifier, not a reason to change the experiment after seeing its endpoint.

## 3. Exact numerical example anchored to the existing PAYOFF theorem

The scenario is a fixed witness, **not a claim about natural nectar/fitness units**:

- Hidden future state has early probability π=0.40.
- Loss of an incorrectly early action C_F=2; loss of missing an early state C_M=1.
- Total loss scale S=(1−π)C_F+π C_M=1.6; B=max((1−π)C_F,π C_M)=1.2.
- Cue-actionability boundary q0=B/S=0.75.
- On the declared symmetric binary signal branch, V_A(q)=max(0,Sq−B).
- A fixed waiting cost D=0.08 is charged in the same *external* calibrated reward-equivalent units.
- The physical correction gate succeeds with assigned probability r independent of cue truth.

The exact resulting model values are:

| q | r | r × V_A(q) − D | Model-optimal use of cue |
|---:|---:|---:|---|
| 0.65 | 0.20 | −0.080 | no |
| 0.65 | 0.85 | −0.080 | no |
| 0.95 | 0.20 | −0.016 | no |
| 0.95 | 0.85 | +0.192 | yes |

**The correct inference is limited to this reduced mathematical model.** It predicts a potential response in only one arm *if* the organism learns the correct cue state and responds approximately according to the declared losses and opportunity. It does not guarantee a bumblebee will use that policy.

## 4. Exact one primary causal estimand

Let Y be externally scored **net reward-equivalent loss**, including the fixed waiting cost, first aggregated into **one mean per randomized colony**. Smaller Y means better matching. With μ the population-average colony mean under an assigned arm:

\[
\tau =
[\mu_{\mathrm{low}\ q,\mathrm{high}\ r}
 - \mu_{\mathrm{high}\ q,\mathrm{high}\ r}]
-
[\mu_{\mathrm{low}\ q,\mathrm{low}\ r}
 - \mu_{\mathrm{high}\ q,\mathrm{low}\ r}].
\]

The **intention-to-treat (ITT) interaction** is positive when increasing cue reliability has a larger reward benefit in high-opportunity colonies. Always report four arm estimates, both marginal treatment effects and the interaction regardless of sign.

**Do not** replace assigned treatment with realized gate use (a post-randomization mediator), nor replace the calibrated loss scale with an endpoint that happened to show significance. Real-world statistical analysis must use **independent-colony** randomization inference or appropriate colony-aware uncertainty, not trial-level pseudo-replication.

## 5. Independent admission / calibration BEFORE main payoff

1. **Cue generation/calibration:** external hidden states, cue correctness and delivery times logged independently of animal actions, with at least 200 held-out cue validation probes per assigned q arm. Delivered accuracy must be within ±0.04 of planned value. In a no-cost probe, trained subjects must demonstrate meaningful cue discrimination before treatment-effect interpretation.
2. **Opportunity calibration:** separate fully informed oracle trials must validate that the correction gate physically opens in target proportions ±0.05, and must estimate the high-vs-low *actual available reward value* on the same scale. Chance of a gate opening is only a **proposed operational proxy** for theoretical r; if reward-value ratio does not match, **do not equate** physical gate frequency to r in an ecological claim.
3. **Loss scale & delay:** false-early/missed-early reward penalties and waiting penalty must be physically measured before outcome exposure. D=0.08 is a toy parameter unless reward-equivalent biological costs can be demonstrated. Any discrepancy requires a new public design version **before collecting focal biology**.
4. **Blindness / leakage:** future rewarding patch is not visible, audible or smelled before the assigned cue, and the cue does not itself move the barrier or change physiological readiness. Log when physical reversal became impossible. Failed independence means SOURCE_DESIGN_NOT_IDENTIFIABLE.
5. **Colony unit:** minimum eight actually independent colonies in each arm and 20 valid main episodes per colony. Colonies/foragers, not trials, determine replication; independent batches and balanced assignment are required. True sample size is determined from an independent behavioral pilot and animal-welfare constraints, not declared sufficient by synthetic power alone.

## 6. What would contradict PAYOFF's proposed biological connection?

- A calibrated q/r manipulation produces no positive ITT interaction or an unresolved colony-aware effect despite adequate independent replication.
- Subjects appear to use an informative cue **after the physical opportunity is closed** at the same magnitude as before closure: the claimed remaining-action gate is missing or a different action remains.
- Behavioral switches respond but patch matching / actual pollen delivery / externally scored payoff do not improve. Information acquisition cannot be equated with fitness benefit.
- A q-only or r-only model predicts independent colonies/batches as well as the prespecified joint model.
- Opportunity/cue calibrations fail, or trained subjects never learn the cue: **MECHANISM_NOT_ESTIMABLE**, NOT a universal biological null.

The assay can demonstrate complementarity in an immediate **behavioral/reward task**, not full annual-cycle migration, reproductive fitness or natural two-species hysteresis. A later seasonal partner synchrony study would need its own real original endpoints and preregistered source/data gates.

## 7. What the synthetic simulator does and does NOT establish

The standard-library script scripts/payoff_b_joint_cue_recourse_design_sim.py:
- verifies exact q0 and all four closed-form net values above;
- simulates **independent colonies** in four randomized cells, with 48 trials per colony, colony-level measurement heterogeneity SD 0.08, within-colony policy compliance heterogeneity SD 0.10;
- fixes 300 Monte Carlo replications, seed 20261120, candidate **8/12/16/24/32 colonies per cell** and hypothetical behavioral compliance 0 / 0.50 / 0.75;
- computes colony-mean factorial ITT contrast, approximate normal intervals and synthetic rejection/directional-detection frequencies;
- labels every result **SYNTHETIC_DESIGN_CALIBRATION_ONLY_NO_NATURAL_DATA**. The no-cue-use scenario is a check of false positive calibration, not a biological null experiment.

The simple approximate interval is only a design diagnostic: small-n animal inference needs proper preregistered colony randomization and controls for training, batch and contamination. No actual biology has been acquired or inferred from simulated values.

**Publication status:** support for exact mathematical trade-off remains theorem-level. Existing natural ingredient evidence remains published prior art. The q×actionability ecological interaction, information-use window, partner coordination and natural hysteresis are still **UNTESTED**. Do not merge into a frozen manuscript or promote this branch's simulated effect as new biological confirmation.
