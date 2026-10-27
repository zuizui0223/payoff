# PAYOFF-B: Matched predeparture physical weather result (2026-10-19)

Status: exploratory matched source readout, NOT evidence of learned environmental forecast use or causal movement timing correction.

## Original data and admission

Three original published public CC0 GPS sources: Ciconia ciconia, Anser albifrons, Numenius arquata. The pre-meteorology source detector reproduced the frozen 145, 106 and 59 stationary-to-northward case events. Thirty-eight, forty-one, and thirty-six animal-years had matched previous stationary control opportunities; within-day GPS bracketing <=24 hours was achieved for 32, 32, and 25 respectively. Original CC0 file lengths and MD5 matched the archived source checksums.

Before opening matched weather, exactly 12 pairs for each of the three taxa were chosen using a deterministic SHA256 of source animal/year/candidate date. The control is same-individual, same-site within 30 km, 5–21 calendar days before the case, chosen nearest in time. In the actual chosen subset ALL controls were 5 days before departure cases.

NASA POWER T2M and WS10M original hourly reanalysis for one predecision day and the previous 7 days was retrieved for all 36/36 pairs. Weather positions were rounded to 0.5-degree cells before external request; exact animal ID, position and date are not published. Reconstructed meteorology does NOT establish what cues birds perceived.

## Outcome-blind weather contrasts (descriptive only)

Contrast = (the last predecision day's weather minus the previous 7-day mean) in MOVING case minus the same quantity in a stationary CONTROL from the same animal-year.

| Taxon | Matched pairs | Mean temperature anomaly difference °C | Paired bootstrap 95% interval °C | Mean wind-speed anomaly difference m/s |
|---|---:|---:|---|---:|
| Ciconia ciconia | 12 | -0.9055 | [-2.3142, +0.3153] | +0.1476 |
| Anser albifrons | 12 | -0.4251 | [-2.9649, +1.9769] | -0.2116 |
| Numenius arquata | 12 | -0.1111 | [-2.7543, +2.4948] | -0.4524 |

The raw case-minus-stay one-day temperatures were +0.0124°C, +0.1133°C, and -0.0327°C, respectively. Neither temperature nor wind speed showed a consistent shared case-stay difference. Each temperature-anomaly bootstrap interval includes zero. Intervals measure descriptive sampling variability, not causal certainty or evidence of a true null.

## Identifiability and next ecological gate

Departure and control opportunities are selected retrospectively based on future 2-day movements and nonmovements. The controls occurred exactly 5 calendar days earlier by the design's closest-stay rule, so seasonality, readiness, weather autocorrelation, shared weather-baseline days, stopover resources, spatial confounding, and sensor precision cannot be ruled out. Wind speed without direction cannot indicate tailwind support.

The following remain UNTESTED: environmental forecasting learned by a bird, cue perception, independent feasible recourse, signed active timing correction, destination phenology mismatch, breeding/survival, causal cross-system generality. Original registered V7R/V8 and original 53-season stork non-support results are unchanged.

For a meaningful new ecological test, construct the complete stationary-day at-risk panel (including nondeparting individuals), prespecify weather anomalies versus expected seasonal climate, validate within-day departures and site residency, and use within-animal/flyway/year dependence-aware inference. Do not retune source thresholds or promote a cross-species pooled effect on the present n=12 per system.

Source runs:
- https://github.com/zuizui0223/payoff/actions/runs/39232249141
- https://github.com/zuizui0223/payoff/actions/runs/39233227157
