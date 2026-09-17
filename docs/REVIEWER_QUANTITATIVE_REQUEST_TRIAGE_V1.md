# PAYOFF-B reviewer quantitative request triage V1

## Purpose

This document classifies likely reviewer requests by whether they improve theorem usability, test implementation, or instead expand the model without strengthening the active short paper. `DO_NOW` means the request is low-risk and directly useful for the registered theorem; `DO_IF_REQUESTED` means it is a scope extension justified only by a specific reviewer concern; `DECLINE` means it adds redundant parameter volume or unsupported real-world calibration.

| Reviewer request | Decision | Quantitative value gained | Trigger / boundary |
|---|---|---|---|
| Add an asymptotic error table comparing the exact optimum `u_*(v)` with the weak- and strong-contrast approximations at a small registered set of `v` values. | `DO_NOW` | Quantifies where the endpoint approximations become practically accurate without changing the theorem. | Report approximation error only; the exact optimum remains the reference and the table is a **model prediction** diagnostic. |
| Retain the exact formula/implementation verification against the general two-season Floquet calculation. | `DO_NOW` | Audits numerical implementation and guards against algebra/code drift. | This verifies implementation consistency; it is not the proof of uniqueness. |
| Add a compact numerical curve for `u_*(v)` if a reviewer asks for interpretability. | `DO_NOW` | Makes the single-valued scaling law visually inspectable across the contrast axis. | The curve must be generated from the exact registered model and cannot be presented as an empirical dispersal distribution. |
| Extend to partial phase-lag or asymmetric migration. | `DO_IF_REQUESTED` | Tests which qualitative features survive once perfect anti-phase symmetry is relaxed. | A phase-lag or asymmetric migration analysis is a new model class. Keep the exact uniqueness theorem scoped to the registered symmetric anti-phase system. |
| Add stochastic switching or a multi-patch network extension. | `DO_IF_REQUESTED` | Could show how the canonical benchmark changes under an explicitly richer process. | This is companion/follow-up theory unless a reviewer specifically requires one minimal comparison. Do not imply uniqueness survives without proof. |
| Add a broad parameter sweep inside the registered model to show robustness. | `DECLINE` | Little inferential gain because the theorem already covers every `v>0`; a dense sweep cannot strengthen an exact universal-in-`v` result. | Use numerical points only for illustration or code verification, not as evidence for theorem validity. |
| Perform field management calibration or convert `m_* tau` into corridor prescriptions without new data. | `DECLINE` | No valid calibration is possible without a defensible mapping from observed movement and environmental switching to `m`, `tau`, and `x`. | **Biological observations analyzed: none**. `FIELD_OPTIMUM_DISTRIBUTION = NOT_ESTIMATED` and `CROSS_SYSTEM_EFFECT_SIZE = NOT_ESTIMATED`. |
| Compare the theorem coefficient to a pooled cross-system effect size. | `DECLINE` | The paper contains no biological sample from which such an effect distribution can be estimated. | The coefficient `0.13248753945` is a theorem-level asymptotic constant, not an ecological meta-effect. |

## Revision rule

Prefer analyses that make an exact result easier to use or audit. Decline requests for dense sweeps when the theorem already closes the parameter domain, and treat any relaxation of symmetry, phase structure, stochasticity, or network size as a new model class unless the reviewer identifies a precise boundary question.

```text
FIELD_OPTIMUM_DISTRIBUTION = NOT_ESTIMATED
CROSS_SYSTEM_EFFECT_SIZE = NOT_ESTIMATED
```

The active paper remains a mathematical benchmark. **Biological observations analyzed: none**, and all optimum/timescale statements remain **model prediction** claims rather than field calibration.
