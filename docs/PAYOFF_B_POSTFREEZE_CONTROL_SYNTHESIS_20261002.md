# PAYOFF-B post-freeze control synthesis — 2026-10-02

Status: **Paper-2 development note; frozen GEB V2 is unchanged**

## New ecological spine

The post-freeze theory now supports one coherent control story:

1. **Schroedinger's spring** — the destination seasonal state is partly latent.
2. **Checkpoint inference** — movement exposes the animal to new local cues.
3. **Signed recourse** — early and late phase error call for opposite
   speed/stopover corrections.
4. **Route-wise feedback** — residual phase error is propagated and corrected
   again at the next checkpoint.
5. **Actionability loss** — information can improve while the remaining
   correction set shrinks.
6. **Coordination** — interacting species can use the same improving
   information at different stages and can become strategically locked into
   different timing conventions.

The compact metaphor is:

> **a Shinkansen running toward Schroedinger's spring**

but the formal model is a sequential Bayesian phase controller, not a railway
analogy.

## What changed relative to frozen Paper 2

The frozen manuscript has an exact information threshold and an effective
deadline cost.  PR 255 added stagewise information and signed recourse.  PR 257
added the continuous information-actionability balance.

The remaining missing piece was explicit phase-state propagation across route
checkpoints.  The prospective route-wise controller now supplies

    e_(t+1) = phi_t (e_t-u_t) + w_t

with checkpoint belief updating and bounded signed correction.

Under perfect estimation and proportional feedback,

    lambda_t = phi_t (1-g_t).

This creates a direct conceptual bridge to the existing empirical
phase-retention coordinate while preserving the current prohibition against
treating lambda as actionability r.

## Strongest new biological question

The most specific next empirical question is no longer merely:

> Do migrants track spring?

It is:

> **At which route checkpoints do animals re-estimate whether they are early or
> late relative to the resource wave, and which actuators do they use to reduce
> that error before the next checkpoint?**

That question separates information acquisition from control and turns
phenological tracking into a testable ecological feedback problem.

## Submission rule

Do not overwrite the frozen V2 manuscript or package.

Any manuscript integration should be a clearly labelled post-freeze Paper-2
revision and should state that the stagewise/actionability/control synthesis was
formalized after the registered empirical gates and does not alter their
outcomes.
