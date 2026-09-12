# Streptomyces M5_T0 public PacBio marker corroboration v1

Status: **OBSERVED PUBLIC-SEQUENCE RESULT / CORROBORATION ONLY**.

A one-off audit of the exact M5_T0 PacBio run `SRR16954720` mapped to `NC_003888.3` produced:

```text
SCO3879 / dnaA   100% coverage   124.526x mean depth
SCO7036 / argG     0% coverage     0x
SCO7350             0% coverage     0x
SCO7662 / cmlR2     0% coverage     0x
```

This observed pattern is exactly the registered four-locus pattern expected for `DEEP_CLASS` and provides strong independent sequence corroboration of the source-level M5 deep-deletion candidate.

The result is pinned to workflow run `34667360902`, job `103481885044`, artifact `10289234376`, digest `sha256:c32d1b877abc08ef4c50e347b4ef49b30bde53b0fc4a3029f3d7fa1e81a157f9`.

## Why this is not the primary class qualification

PAYOFF prospectively registered the BGISEQ short-read lane as the primary marker-depth channel and requires its response-blind normalization/threshold calibration before M5 BGI marker ratios are opened. The PacBio result therefore has the role:

```text
DEEP_CLASS independently corroborated by public long reads
```

not:

```text
primary BGI marker gate passed.
```

This separation prevents the already observed target pattern from being used to tune the primary-channel cutoff.

## Remaining blockers

```text
response-blind BGI calibration / primary marker adjudication
gross T0 chromosome-structure audit
current physical stock identity and access
same-context 72 h -> 120 h realization d band
per-reference qualification.
```

Thus qualified matched-D references remain zero and architecture-specific inference remains hard closed.
