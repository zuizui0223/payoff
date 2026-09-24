# PAYOFF-B Aikens pre-environment support-ceiling receipt

Frozen: 2026-09-22

Status: **registered sample-support gate is feasible before environmental filtering**.

This receipt uses only the frozen raw GPS source and the pre-outcome fixed-target
execution contract v2. It does not use MODIS environmental values and does not
open either group-specific lambda.

## 1. Source identity

Frozen raw-GPS artifact:

    artifact:
        10643405042

    archive sha256:
        1f0d706dc6a102261009b7099c748dcce40abb2adedf7b88828395a1d392cfa0

    stage3_industrial_mule_deer_gps.csv sha256:
        03426804557a0244be3ed6eb9f461db578d3ce26fa2b28637f8e98bee9f09466

Source scale:

    GPS observations:
        64,539

    animals:
        137

    animal-years:
        253.

The exact GPS-to-MODIS identity was rebuilt and the frozen manifest hash passed:

    d50e69a20d6e65ec3426a8c938d1dea9d4e2f836c9bf07e02d30c560f5fa8463.

## 2. Fixed-target rule

Execution contract:

    data/aikens2022_phase_reconstruction_execution_contract_v2_20260922.json

Target geometry:

    interval:
        24 h

    matching tolerance:
        +/- 3 h

    anchor:
        earliest raw spring-migration observation in each animal-year

    environment used to select target:
        NO.

For an exact time-distance tie, the frozen pre-outcome rule is:

    minimum absolute target-time deviation
    -> earlier observed timestamp
    -> lexicographically smaller observation_id.

Environmental availability is therefore unable to change which GPS observation
represents a target.

## 3. Registered final support gate

The preregistered contrast requires, in each development group:

    >= 10 animals

and

    >= 100 adjacent fixed-24h phase transitions.

Before environmental phase is attached we can compute a strict **upper bound**
on final support: count adjacent selected target indices as if every selected
target later receives valid phase.

Environmental filtering can only remove these pairs.

## 4. Observed support ceiling

### Large-development group

Animals capable of contributing at least one adjacent target pair:

    48

Maximum possible adjacent fixed-24h pairs:

    1,022

Registered threshold:

    10 animals
    100 pairs

Pre-environment support ceiling:

    PASS.

### Small-development group

Animals capable of contributing at least one adjacent target pair:

    89

Maximum possible adjacent fixed-24h pairs:

    4,434

Registered threshold:

    10 animals
    100 pairs

Pre-environment support ceiling:

    PASS.

## 5. Scientific interpretation

The registered Aikens lambda perturbation is **not doomed by movement-sample
support before environmental reconstruction**.

Both groups exceed the registered final thresholds by wide margins under the
maximum-support ceiling.

This licenses the operational conclusion:

> authenticated environmental extraction is worth executing because the
> preregistered contrast remains support-feasible before environmental
> filtering.

It does **not** license:

> the final contrast is estimable.

The final result can still become

    NOT ESTIMABLE

if enough preselected targets fail environmental reconstruction such that either
group falls below 10 animals or 100 adjacent valid phase pairs.

No threshold may be loosened in response.

## 6. Provenance

One-time workflow:

    payoff-b Aikens pre-environment support ceiling

Run:

    35687039708

Head:

    06e88f100a6d3b0b5ed77dbdd3f32eb5a8589a3a

Conclusion:

    SUCCESS.

Artifact:

    10676913354

Artifact sha256:

    ab88ade2ec53c8f91b1a2099d58ad210ad57ab80d826375938c94bfe8689efa2

The artifact contains the rebuilt exact-manifest receipt, raw phase-key receipt,
fixed-target table and receipt, and this support-ceiling analysis output.

## 7. Claim boundary

Licensed:

- source identity is reproduced;
- fixed targets are selected without environmental information;
- both groups have enough maximum possible animals and pairs to clear the
  registered support thresholds;
- final estimability remains unresolved until environmental phase is attached.

Not licensed:

- any lambda estimate;
- any development-group lambda difference;
- final PASS or FAIL;
- substituting another GPS point when a selected target lacks valid phase;
- widening the interval or tolerance after environmental coverage is observed.
