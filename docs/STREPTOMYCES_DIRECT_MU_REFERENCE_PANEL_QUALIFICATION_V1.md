# Streptomyces direct-mu D-reference panel qualification v1

Status: **prospective / pre-outcome**. This document freezes how pre-existing terminal-deletion references may enter the realization channel. It does not report that any reference panel has been materialized.

## Purpose

The direct-mu state channel is frozen at 72–120 h with `SCO7662/cmlR2` loss as the registered entry state and deeper deletion markers retained as severity information. To identify new entry into that state, pre-existing D material must have an independently estimated realization `d` over the same interval.

The reference panel may not be selected after viewing prodiginine-congener outcomes or after viewing which D isolate happens to grow best.

## Predeclared classes

At least two independently derived qualified references are required in each class:

```text
ENTRY_CLASS
  SCO7662 absent; SCO7350 present; SCO7036/argG present

INTERMEDIATE_CLASS
  SCO7662 absent; SCO7350 absent; SCO7036/argG present

DEEP_CLASS
  SCO7662 absent; SCO7350 absent; SCO7036/argG absent
```

Each reference must retain the registered core marker, be present before the 72 h interval start, be measured in the same medium/context at 72 and 120 h, and have a closed realization band on calibrated core chromosome-equivalent mass.

Unresolved gross secondary rearrangement is disqualifying because the realization measurement would otherwise mix the registered terminal-deletion class with uncharacterized genome-wide changes.

## Conservative aggregation

For each qualified reference `i`, estimate

```text
d_i = core chromosome equivalents at 120 h / core chromosome equivalents at 72 h.
```

The registered D-realization band is the closed envelope from the smallest lower endpoint to the largest upper endpoint across **all** qualified references in all three predeclared classes.

This deliberately retains deletion-class heterogeneity. It is forbidden to discard slow, low-realization, or inconvenient references after viewing their `d` values.

## Current status

```text
qualification rules frozen pre-outcome = TRUE
reference panel materialized           = FALSE
reference panel qualified              = FALSE
d band available                       = FALSE
direct mu outcome available            = FALSE
```

Therefore freezing this gate does not open congener outcomes and does not promote matched-S, architecture mapping, Lane G, eta, or E1.
