# Streptomyces direct-mu marker/window handoff v1

Current frozen state-channel design:

```text
entry marker:       SCO7662 / cmlR2 (~178 kb from right end)
severity marker 1:  SCO7350 (~503 kb)
severity marker 2:  SCO7036 / argG (~841 kb)
core reference:     SCO3879 / dnaA in central oriC region
primary interval:   72 h -> 120 h
```

The primary registered `D` entry is loss of SCO7662 relative to a genotype- and time-matched calibrated core reference. SCO7350 and argG are retained as deeper severity states and are not counted as additional entry events.

Terminal/core copy ratios must be calibrated against intact material matched by genotype, time, and condition because oriC-to-terminal dosage can vary with replication state independently of deletion.

The 72->120 h interval is frozen pre-outcome as the first adjacent interval in the registered 2025 colony time series and ends at the five-day time point used for the canonical external-task assay.

This advances only the **state channel**. The independent realization channel

```text
r = d/g
```

remains unfrozen and must be measured over the same interval/context without reverse-engineering it from the final state fraction.

Therefore:

```text
STATE_CHANNEL_FROZEN = TRUE
DIRECT_MU_FULLY_READY = FALSE
OUTCOME_OPENING_ALLOWED = FALSE
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
ETA_IDENTIFIED = FALSE
E1 = FALSE
```
