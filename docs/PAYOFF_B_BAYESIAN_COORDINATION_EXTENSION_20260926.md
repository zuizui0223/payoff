# PAYOFF-B Bayesian coordination extension — implementation note

Date: **2026-09-26**  
Status: **exploratory; not promoted into the frozen integrated manuscript**

## What changed

A dependency-free partial-information timing game has been added to PAYOFF-B.
It formalizes the case in which destination residents can condition timing on
realized local spring, while a migrant must commit from a noisy remote cue.

The new object is not another movement-speed rule. It separates:

- perfect-information adaptive capacity;
- information available at commitment;
- private versus joint payoff under partner mismatch.

## Exact new result

For migrant private false-early and missed-early losses C_F and C_M, migrant
interaction mismatch I_M, and resident externality n_R I_R:

    tau_private
    = (C_F + I_M)/(C_F + C_M + 2 I_M)

and

    tau_joint
    = (C_F + I_M + n_R I_R)
      /(C_F + C_M + 2 I_M + 2 n_R I_R).

If C_F > C_M and n_R I_R > 0, then

    tau_joint < tau_private.

Therefore an exact posterior wedge exists in which early timing maximizes joint
payoff but the migrant rationally stays late.

Under the canonical transparent witness

    prior early = 0.55
    false-early cost = 2.0
    missed-early cost = 1.0
    migrant mismatch cost = 0.5
    two resident partners, cost 1.0 each,

the corresponding early-cue accuracy thresholds are approximately

    q_joint   = 0.512658
    q_private = 0.576923.

At q=0.55 the early cue produces posterior early-spring probability about
0.59901: above the joint threshold 0.5625 but below the private threshold
0.625. The joint policy advances; the migrant's private policy does not.

## Interpretation

This creates a three-regime prediction as remote-cue reliability falls:

1. **aligned adaptation** — cue reliability is high enough that both private
   and joint policies advance after an early cue;
2. **information--coordination wedge** — the same cue still justifies advance
   for the interacting system, but not for the migrant privately;
3. **information-limited adaptation** — reliability is so low that even the
   joint-optimal policy does not advance from that cue.

The novel point is therefore not simply that uncertainty creates mismatch.
Partial information interacts with the payoff externality of partner mismatch,
creating a region where the system-level adaptive solution exists and is
inferable from the available cue, yet decentralized selection does not choose
it.

## Relationship to the existing PAYOFF-B result

The existing 2D landscape gate asks whether a known coordinated improvement is
unilaterally accessible. The new Bayesian gate asks an earlier question:
whether the state-contingent improvement is sufficiently knowable at the time
a migrant must commit.

These mechanisms are complementary:

    known but strategically inaccessible
    !=
    not sufficiently knowable at commitment.

The next empirical handoff should therefore estimate pre-departure to
destination predictability rather than immediately adding another taxon to the
phase-retention panel.

## Files

- `src/partial_information_coordination.py`
- `tests/test_partial_information_coordination.py`
- `scripts/payoff_b_partial_information_sweep.py`
- `theory/PARTIAL_INFORMATION_COORDINATION.md`

## Freeze boundary

No existing PAYOFF-B synthetic receipt, Aikens preregistration, broad-bird
result, or integrated PREOUTCOME claim is altered by this exploratory branch.
Promotion should occur only after the new tests pass and the cue-reliability
prediction is stress-tested.
