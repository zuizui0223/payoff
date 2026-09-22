# PAYOFF-B Aikens fixed-target execution amendment v2

Frozen: **2026-09-22**

Status: **pre-environment, pre-lambda execution correction**.

The first execution contract required environmental phase to match every raw GPS
observation. That was stricter than the original preregistration and, more
importantly, put environmental availability before the registered 24 h target
selection.

The original design states that each animal-year receives a fixed target grid,
a GPS observation is matched to each target within the frozen tolerance, and a
phase pair is formed only when both endpoints pass environmental reconstruction.

Version 2 therefore freezes the order as:

~~~text
64,539 raw GPS observations
-> exact frozen MODIS-cell identity
-> 24 h target grid
-> nearest raw GPS within +/-3 h
-> target identity frozen
-> environmental phase attached
-> invalid environmental target remains missing
   (no replacement GPS is selected)
-> adjacent valid target indices form phase pairs
-> >=10 animals and >=100 pairs per development group
-> registered lambda contrast
~~~

The target grid is anchored at the earliest raw spring-migration observation in
each animal-year. Adjacent target windows cannot overlap.

If two raw GPS observations are exactly equidistant from one target, the
pre-outcome deterministic tie-break is:

    smaller absolute time deviation
    -> earlier observed timestamp
    -> lexicographically smaller observation_id.

This rule is independent of environmental availability and source-row order.

This amendment does **not** change the hypothesis, phase coordinate, 24 h segment
scale, +/-3 h tolerance, statistical model, p-value threshold, group definitions,
or sample-support thresholds. It also does not inspect any MODIS environmental
values or lambda estimate.

The key anti-selection rule is:

> Environmental availability may invalidate a preselected target, but it may not
> cause a different GPS observation to be substituted for that target.

Machine contract:

`data/aikens2022_phase_reconstruction_execution_contract_v2_20260922.json`
