# PAYOFF-B post-Bayesian publication reframe

Date: **2026-09-26**  
Status: **candidate reframe; preserves all earlier frozen receipts**

## Decision

Do not discard the temporal-buffering programme. Reorder it.

The integrated ecology paper should no longer open with "timing is only a
finite substitute for movement" as the main surprise. That result becomes the
capacity baseline.

The stronger organizing question is:

> **What prevents an interaction network from taking an adaptive seasonal
> response that physically exists?**

PAYOFF-B now gives three answers:

    cannot do it          -> capacity
    cannot predict it     -> spatial predictive information
    cannot wait to know it -> information timing
    cannot get there      -> coordination / history.

This gives the paper a sharper conceptual architecture than treating movement,
phenology, phase retention and mismatch as parallel observations.

## Proposed title family

Primary working title:

**When information arrives too late: prediction, coordination and ecological
memory in seasonal tracking**

Alternative:

**Predictive connectivity and ecological memory shape seasonal tracking under
environmental change**

Shorter conceptual title:

**When seasonal information fails**

## Figure logic

Figure 1:
three-barrier framework: cannot do / cannot know / cannot get there.

Figure 2:
the information-deadline theorem: exact actionable-cue threshold, actor-specific
wait thresholds, the identity Delta q=(D2-D1)/(A+L), persistent asymmetry under
hard deadlines, and the flycatcher--tit experimental anchor.

Figure 3:
exact partial-information coordination wedge and strict Bayesian timing phase
diagram.

Figure 4:
topology contrast: complete vs chain vs migrant-star; distinguish shock
transmission from historical storage.

Figure 5:
broad-bird predictive-connectivity result, including detrended vs raw
correlation and dependence-aware uncertainty.

Figure 6:
wigeon null interaction, used explicitly to separate predictive information
from phase correction.

Figure 7:
recovery leverage: voluntary coalition size versus temporary rescue seed, with
the chain's central local pollinator as the unique singleton rescue adopter.

Figure 8:
connection back to spatial/temporal capacity: finite temporal buffering and
spatial re-entry as the capacity layer.

The 55-species universal-speed falsification can move to a supplementary or
secondary panel unless it materially improves the narrative.

## Publication boundary

This reframe must not imply that natural network hysteresis has been observed.
The empirical contribution currently establishes a predictive-information
axis with mixed strength across scales:

- pooled broad-bird association: supportive;
- species-independent inference: not established;
- within-wigeon phase-correction modulation: not supported.

The strongest causal/hysteretic result remains theoretical.

That limitation should be stated directly rather than diluted.


## New organizing sentence

The paper should now distinguish three temporal positions of information:

    before commitment:
        predictive connectivity can reduce uncertainty about what lies ahead;

    at / after local arrival:
        additional heterospecific or environmental information can become
        observable, but only if the organism has not already made an
        irreversible or costly decision;

    after mismatch is realized:
        phase correction acts on an error that has already occurred.

These are different ecological functions of information.

The flycatcher--tit experiment provides an external empirical anchor for the
middle position. Earlier male settlement occurred before manipulated tit
hatching became visible and did not respond detectably to treatment, whereas
later female settlement did.

The wigeon null then becomes conceptually useful rather than awkward: stronger
historical predictive connectivity does not necessarily produce stronger
post-error correction.

## Revised one-line message

> **The bottleneck in seasonal adaptation may be not whether useful information
> exists, but whether it arrives before the decision deadline; interactions can
> then convert a temporary information delay into persistent ecological
> history.**


## Counterintuitive hook

The strongest conceptual hook is not simply that migrants lack information.

The new exact result predicts:

    poor cue:
        both partners ignore it -> remain synchronized

    intermediate cue:
        only the lower-delay partner waits and uses it
        -> synchronization breaks

    strong cue:
        both partners wait and use it
        -> synchronization returns.

Thus a monotonic improvement in environmental information can cause a
non-monotonic ecological response.

Working headline:

> **Better information can temporarily worsen phenological coordination when
> interacting species face different decision deadlines.**

This hook should be presented before the longer-term hysteresis result. It gives
the paper an immediate mechanism, while topology-dependent memory explains why
a transient desynchronization can become historically persistent.


## Cue--driver prior-art firewall

Tomotani et al. (2021; DOI 10.3389/fevo.2021.630823) already provide the
closest direct predecessor to the predictive-information argument. In the same
Hoge Veluwe pied-flycatcher system, Ivory Coast and Dutch temperature/NDVI
variables explained male arrival timing, while those variables did not
detectably predict the estimated annual fitness optimum. They explicitly
proposed climate-driven disruption of cue--driver correlations.

Therefore Paper 2 must not sell any of the following as its primary novelty:

- migrants use remote environmental cues;
- cue reliability can decline under climate change;
- wintering-ground conditions may cease to predict breeding-ground optima;
- cue--driver decoupling can generate phenological mismatch.

Those are setup.

The PAYOFF-B novelty begins after the cue is already imperfect:

1. **decision deadlines make information access endogenous;**
2. **partners with different waiting costs cross information-use thresholds at
   different cue qualities;**
3. **therefore improving a shared cue can temporarily increase mismatch;**
4. **interaction topology determines whether that transient mismatch is erased
   or stored as a lower-payoff historical timing regime.**

This sequence is the novelty firewall for the integrated paper.

## Preferred hook after prior-art audit

The strongest opening claim is now:

> **Better information need not improve ecological coordination monotonically.
> When interacting species face different decision deadlines, improving the
> same seasonal cue can first desynchronize them and only later restore
> coordination.**

Cue--driver disruption is the ecological motivation for changing cue quality;
it is not the contribution itself.

The longer-term second result is:

> **A temporary information-induced desynchronization can become ecological
> memory when the interaction network contains a strict alternative timing
> equilibrium.**


## Long-term natural reversal lane: closed negative

The preregistered 1980--2010 Hoge Veluwe cue--driver lane did **not** pass the
information decline--recovery gate. The connectivity series is visibly
nonstationary and the best two-line description changes around 2001, but the
pre-break fitted slope is positive rather than negative.

Accordingly:

- no natural hysteresis model was opened;
- the cue window was not retuned;
- the breakpoint was not redefined from the known selection trajectory;
- the result is retained as `NO_CUE_DRIVER_REVERSAL`.

This strengthens the publication logic. Cue--driver disruption remains
well-motivated prior art, not a new result that PAYOFF-B needs to rescue.

The main empirical/theoretical chain should therefore be presented as:

    broad birds:
        predictive information relates to realized mismatch, pooled but
        dependence-sensitive

    flycatcher manipulation:
        cue usefulness depends on whether it is visible before the decision

    long-term flycatcher lane:
        no preregistered natural decline--recovery information cycle

    wigeon:
        predictive connectivity does not act as a stronger post-error controller

    exact theory:
        unequal decision deadlines make cue uptake asynchronous

    network theory:
        topology can store a transient desynchronization as ecological memory.

The natural network-hysteresis prediction remains deliberately prospective.


## Exact theorem upgrade

The information-induced mismatch is no longer only a numerical phase-diagram
result. The deadline theorem gives the exact uptake thresholds, and the
shared-cue network adds a second exact result: **perfect environmental
information can coexist with a strict obsolete uninformed equilibrium.**

For the declared binary seasonal decision, define the prior expected costs of
committing early and late as

    A=(1-pi) C_F
    L=pi C_M.

An actor with waiting cost D begins using a future cue only above

    q_wait(D)
    = [max(A,L)+D]/(A+L),

provided D < min(A,L).

Thus two interacting actors with unequal deadlines have an exact
desynchronization width

    Delta q
    = |D2-D1|/(A+L)

when both eventually wait.

This makes the primary comparative prediction unusually simple:

> **The ecological range over which better information worsens coordination is
> proportional to heterogeneity in the opportunity cost of waiting.**

There is also a stronger regime. If one actor has

    D >= min(A,L),

even perfect information is not valuable enough to justify delaying its
decision. Cue reliability can reach q=1 without restoring shared information
use.

This should become the analytic centerpiece of Figure 2. The earlier numerical
q=0.82--0.93 window is retained as one transparent witness of the theorem, not
as the result itself.


## Perfect-information trap as the second analytic centerpiece

At q=1, define R_i as player i's expected loss under the old prior-optimal
timing, D_i as its information/waiting cost, I_i as interaction strength, and p
as the probability that perfect information would make it switch action.

The old timing convention is stable when

    D_i + p I_i >= R_i.

The fully informed convention is stable when

    D_i <= R_i + p I_i.

Both are strict when

    |D_i-R_i| < p I_i.

Yet coordinated information use has higher joint payoff whenever

    sum D_i < sum R_i.

The canonical witness satisfies all of these conditions. At q=1:

    obsolete late|late|late joint payoff = -0.60
    informed follow|follow|follow payoff = -0.45.

No species benefits from becoming the first cue user.

When q is degraded from 1, the informed convention collapses at q=0.79 on the
0.01 grid. When q is subsequently restored to 1, the old convention remains.

This gives the paper a stronger causal sequence:

    decision deadlines
    -> asynchronous information uptake
    -> coordination barrier to first adoption
    -> collapse of an information-using convention
    -> historical lock-in despite perfect information recovery.

The key distinction from generic cue--driver mismatch is therefore not merely
that information becomes unreliable. It is that **restoring information can be
insufficient because interaction has made information use a coordination
state.**

### Updated preferred opening

> **Environmental information can recover before ecological coordination does.
> When interacting species face different decision deadlines, information use
> becomes a strategic convention: better information can first desynchronize
> partners, and after an information-using convention collapses, even perfect
> information may not restore it.**

This combines the information-deadline theorem and network game in one
mechanism and should replace the weaker framing that the system simply "cannot
know" the future.


## Recovery is a separate network property

The integrated model now distinguishes three questions that should not be
collapsed:

    Can the informed convention persist?
    Can the obsolete convention persist?
    What is the smallest perturbation that moves the system between them?

For a temporary informed seed S, an old actor i adopts when

    R_i-D_i+pI_i[2a_i(S)-1] > 0,

where a_i(S) is the fraction of its interaction weight already attached to
informed neighbours.

This turns ecological recovery into a threshold-cascade problem with thresholds
derived from biological timing costs.

The canonical result is especially clean:

- complete network: any singleton seed rescues the system;
- migrant-star: any singleton seed rescues the system;
- chain: only the central local pollinator is a singleton rescue seed.

Thus the strongest applied-looking statement should remain theoretical:

> **The species that determines whether a seasonal convention can be rescued
> need not be the species that caused the mismatch or the species with the worst
> information; it can be the interactor whose network position gives the
> greatest recovery leverage.**

Generic seed-triggered cascades are established network science. PAYOFF-B's
claim is the ecological derivation of those thresholds from seasonal risk,
decision deadlines and partner mismatch.
