# PAYOFF-B V8 signed arrival-greenup mismatch result — 2026-10-06

Status: **POSTHOC SIGNED-TIMING DIAGNOSTIC; FROZEN V8 ENDPOINTS UNCHANGED**

## Why this audit was needed

The frozen bird endpoint used:

    log1p(abs(arrival - greenup)).

A later posthoc sensitivity used absolute mismatch in days.

Both discard direction. A smaller absolute gap can arise because birds
actively track a changing seasonal target, or because the environmental target
moves toward an otherwise stable bird schedule.

This diagnostic restores the sign:

    signed lag = arrival - target green-up.

Positive values mean birds arrive after mid-green-up; negative values mean
birds arrive before mid-green-up.

## Sample

The reconstructed transfer sample matches the frozen transfer lane:

- **150 species-target rows**;
- **72 unique environmental pairs**;
- **22 species**.

## Signed relative arrival shifted

Unweighted species-target rows:

- early signed lag = **-7.81 d**;
- late signed lag = **-5.69 d**;
- late-minus-early change = **+2.12 d**;
- 95% unique-pair bootstrap CI = **+1.41 to +2.77 d**.

Equal-species weighting:

- early signed lag = **-8.53 d**;
- late signed lag = **-6.40 d**;
- change = **+2.14 d**;
- 95% pair-bootstrap CI = **+1.32 to +2.92 d**.

Direction:
- **20/22 species** have positive signed-lag change;
- **57/72 pairs** have positive signed-lag change.

Birds therefore became about two days **less early relative to mid-green-up**.

This should not automatically be called improvement, because zero lag is not
established as the fitness optimum and first arrival can naturally precede
mid-green-up.

## Bird arrival itself changed little

Mean estimated arrival date:

- early = **123.17**;
- late = **122.98**;
- shift = **-0.19 d**;
- 95% pair-bootstrap CI = **-0.95 to +0.52 d**.

Equal-species arrival shift:
- **-0.19 d**;
- 95% CI = **-1.02 to +0.65 d**.

Thus the bird arrival front did not show a resolved period shift.

## Target green-up advanced strongly

Mean target mid-green-up:

- early = **130.98**;
- late = **128.67**;
- shift = **-2.31 d**;
- 95% pair-bootstrap CI = **-2.58 to -2.08 d**.

Equal-species green-up shift:
- **-2.32 d**;
- 95% CI = **-2.57 to -2.09 d**.

Therefore the +2.12 d signed-lag change is generated primarily by an advancing
environmental target, not by a corresponding shift in bird arrival.

## Why absolute mismatch looked stable or slightly smaller

Absolute arrival-green-up mismatch:

Unweighted:
- **8.42 d -> 8.07 d**;
- change **-0.35 d**;
- 95% CI **-0.90 to +0.20 d**.

Equal species:
- **9.04 d -> 8.42 d**;
- change **-0.63 d**;
- 95% CI **-1.14 to -0.04 d**.

Because birds were, on average, several days earlier than mid-green-up in both
periods, an earlier green-up date moved the environmental target toward the
largely unchanged arrival schedule. The modest decline in absolute mismatch
therefore does **not** demonstrate active tracking.

This agrees with the structural-null warning from the information-value
transfer analysis: target green-up geometry can generate apparent changes in
mismatch even without temporal adjustment by birds.

## Ecological interpretation

The combined bird evidence now has a sharper form.

Between 2002–2009 and 2010–2017:

1. destination green-up became more variable;
2. nonlocal environmental forecast value increased strongly;
3. the nonlocal signal became temporally earlier relative to bird arrival;
4. target green-up advanced by about 2.3 d;
5. estimated bird arrival changed by only about 0.2 d;
6. birds consequently became about 2.1 d less early relative to mid-green-up;
7. route-level gains in forecast value did not predict bird-specific mismatch
   improvement beyond structural nulls.

Thus the bird system does not show population-level arrival timing becoming more
responsive simply because a reconstructed environmental signal became more
valuable and temporally available.

A concise licensed interpretation is:

> **Environmental forecast opportunity increased, while the estimated bird
> arrival schedule remained comparatively rigid.**

This is consistent with Amaral et al. (2025), who reported that migration speed
responds to green-up but does not fully compensate for phenological change.

## Consequence for the manuscript

Retire as a central biological interpretation:

> bird mismatch did not deteriorate / tracking was maintained.

That statement is mathematically true on the absolute-gap scale but
mechanistically misleading.

Prefer:

> Target green-up advanced by about 2.3 d while estimated arrival changed little,
> shifting signed relative arrival by about 2.1 d. The apparent stability of
> absolute mismatch therefore does not constitute evidence that birds converted
> the increased environmental forecast value into arrival adjustment.

This strengthens the separation between:
- environmental information availability/value; and
- biological uptake, decision, and correction.

## Claim boundary

Licensed:
- signed relative arrival shifted by about +2.1 d;
- target green-up advanced strongly;
- bird arrival itself did not show a resolved period shift;
- absolute mismatch stability is not evidence of active adjustment.

Not licensed:
- later relative arrival reduced fitness;
- zero arrival-greenup lag is optimal;
- birds failed to perceive the source cue;
- actuator limitation caused the weak arrival shift;
- actionability r(t) declined.

## Provenance

Workflow:
- run: 37392945997
- artifact: 11381568325
- artifact SHA256:
  9cdc5be806f2cd25654f366ac323c0986a601670a978ce28ef9f8b4d64099cd2

Script:
analysis/movement_phenology/payoff_b_v8_signed_mismatch_diagnostic.R
