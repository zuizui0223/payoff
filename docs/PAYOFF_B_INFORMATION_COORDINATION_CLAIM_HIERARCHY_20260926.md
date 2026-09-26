# PAYOFF-B information-coordination claim hierarchy

Date: **2026-09-26**  
Status: **candidate reframe after Bayesian + predictive-connectivity programme**

## Proposed ecological headline

> **Useful seasonal information can arrive after the costly decision that
> needs it. Species may therefore rationally commit under uncertainty even when
> an adequate response exists; interaction partners can amplify that information
> timing problem, and network topology can store the resulting timing history
> after information recovers.**

This is stronger and more specific than the previous headline that temporal
buffering is finite.

## Three distinct barriers

PAYOFF-B now separates three mechanisms that previously sat under one broad
"tracking mismatch" label.

### 1. Capacity barrier

Movement and timing can substitute locally, but temporal adjustment has finite
range. Under sustained directional forcing, movement must re-enter.

This is the retained temporal-buffering result.

### 2. Information barrier

A migrant may have adequate physical capacity to advance but must commit before
the future destination state is observed. The relevant ecological quantity is
predictive connectivity between information available before commitment and the
later destination state.

The exact binary game contains an information--coordination wedge in which the
jointly valuable action is not privately selected under the migrant's available
information.

The endogenous-timing extension adds a second wedge: even when a future cue
would improve decisions, a focal actor may rationally commit before the cue if
its opportunity cost of waiting exceeds the private value of information while
remaining below the joint value of waiting.

### 2b. Information-timing barrier

Information quality is not only spatially unequal; it can also be temporally
unavailable.

The new exact waiting model separates

    act now under uncertainty

from

    wait until a more informative cue becomes observable.

If the private value of the future cue is V and delaying the decision costs D,
the focal individual waits only when

    V > D.

Thus an organism can have sufficient physiological capacity and a highly
informative future cue, yet still rationally act before that cue exists because
the opportunity cost of waiting is larger.

When a wrong decision also harms partners, the joint value of waiting can exceed
the focal individual's private value. This creates an information-acquisition
coordination wedge: privately optimal early commitment can coexist with a
system-level benefit of waiting for information.

Unequal delay costs also create a non-monotone information effect. In the
canonical shared-cue comparison, both actors commit at low cue quality, only
the lower-delay actor waits at intermediate cue quality, and both wait at high
cue quality. Expected action mismatch is therefore zero, then positive, then
zero again. On the declared 0.01 grid the desynchronization window is
q=0.82--0.93 and peaks at mismatch probability 0.436 at q=0.82.

So improving information can transiently worsen interactor coordination because
information uptake is asynchronous.

### 3. Coordination-memory barrier

When partners are strategic, a temporary migrant information shock can change
resident timing policies even though the residents' own cue quality did not
change.

The strict phase diagram shows that after information recovery, the displaced
timing regime can remain a strict lower-joint-payoff Bayesian equilibrium.

This memory depends strongly on network topology.

## Strict synthetic result

Across the declared 451-cell grid:

| topology | eligible high-information cells | strict lower-payoff hysteresis |
|---|---:|---:|
| complete | 391 | 118 |
| chain | 364 | 52 |
| migrant-star | 404 | 0 |

The chain and migrant-star have the same number of undirected links. Both can
transmit a temporary information shock, but only the chain retains a broad
strict hysteresis region.

The mechanistic interpretation is therefore:

    transmission of information shock
    !=
    storage of information shock.

Partner topology controls ecological memory.

## Natural-data evidence

### Broad migratory birds: pooled directional support

In the preregistered 37-species / 3,311-row analysis, stronger pre-outcome
predictive connectivity is associated with smaller arrival--green-up mismatch:

    beta = -0.0462
    95% CI = -0.0870 to -0.0054
    p = 0.0265.

The sign remains negative in all leave-one-species-out and leave-one-year-out
fits and in the 10-year trailing-window sensitivity.

Raw undetrended source--destination correlation has essentially no effect.
Thus the signal is associated with interannual predictive connectivity rather
than a shared long-term climate trend.

However, cluster-robust intervals and the species-level summary cross zero.
The licensed claim is therefore a pooled directional macroecological signal,
not species-independent confirmation.

### Flycatcher--tit experiment: timing-dependent information availability

A source-backed experimental anchor now separates early and late decisions in a
resident--migrant interaction.

Samplonius & Both (2017) experimentally advanced or delayed resident tit
hatching phenology across forest plots. Male pied flycatcher settlement was not
detectably related to treatment (Z = 0.854, P = 0.393), and the authors note
that almost all males settled before the manipulated tit-hatching difference
became apparent.

Later-arriving females, by contrast, preferentially settled in earlier-tit
plots. The published pairing GLMM gives a tit-timing effect of -0.101
(SE 0.050, P = 0.042), and the time-dependent Cox analysis gives a treatment
effect of -0.065 (SE 0.025, P < 0.009), with treatment separation increasing
later in the season.

This does not show that females deliberately waited to collect information.
It does support the narrower timing claim required by PAYOFF-B: the same
heterospecific phenological state can be unavailable to an early decision maker
and behaviourally relevant to a later one.

### Wigeon: registered controller prediction not supported

Across 224 consecutive staging transitions, historical route predictive
connectivity varies strongly, but it does not strengthen phase correction:

    origin_phase x connectivity beta = +0.0202
    95% CI = -0.1058 to +0.1461
    p = 0.756.

Therefore predictive information should not be promoted as a universal
post-error feedback controller.

## New empirical distinction

The contrast between the broad analysis and wigeon gives a useful decomposition:

[
\text{predictive information before commitment}
\neq
\text{correction after error appears}.
]

This suggests that predictive connectivity can matter by changing which timing
decision is taken or which timing basin is reached, without necessarily making
subsequent correction stronger.

That separation is biologically closer to the partial-information game than a
claim that high rho simply increases lambda correction.

## What becomes secondary

The following remain valid but should no longer be the main ecological
headline of Paper 2:

- finite temporal buffering;
- latent spatial tracking demand;
- absence of one universal migration-speed/environment-speed optimum;
- one common phase-retention coordinate.

They become layers in the argument:

    finite capacity
    +
    incomplete information
    +
    interaction-dependent accessibility
    ->
    realized tracking architecture and mismatch.

## Candidate paper logic

1. **Local null:** movement and timing can close the same mismatch.
2. **Capacity:** finite timing means successful alignment can hide future
   spatial demand.
3. **Predictive information:** some actors must choose before the destination
   state is known.
4. **Information timing:** useful cues can become available only after an early
   commitment deadline; waiting is favoured only when information value exceeds
   delay cost.
5. **Bayesian coordination:** private and joint incentives can diverge both in
   action choice and in whether to wait for information.
6. **Network game:** a transient information shock can change resident timing
   policies and produce strict recovery hysteresis.
7. **Broad empirical test:** higher pre-outcome predictive connectivity is
   associated with smaller natural phenological mismatch in the registered
   pooled analysis.
8. **Experimental anchor:** the flycatcher--tit manipulation shows that a
   heterospecific phenology treatment is irrelevant to an earlier decision made
   before cue visibility but affects later settlement.
9. **Mechanistic boundary:** wigeon connectivity does not strengthen post-error
   phase correction, showing that prediction, information timing and correction
   are different axes.
10. **Conclusion:** mismatch reflects not only response capacity, but what the
   system could know before a decision deadline and which historically
   accessible timing regime the interaction network occupies.

## Recommended main conclusion

> **Climate adaptation can fail even when an adequate response and useful
> information both exist, because the information may become available only
> after the costly seasonal decision that needs it. Unequal decision deadlines
> create unequal information among interacting species; a transient information
> shock can then redirect the interaction network, and local ecological coupling
> can retain that history after information recovers.**

Empirical qualifier:

> Across migratory birds, pre-outcome predictive connectivity shows the
> predicted pooled association with smaller mismatch, but this effect is
> dependence-sensitive and does not appear as stronger phase correction in the
> wigeon staging system.

## Claim ceiling

PAYOFF-B may currently claim:

- an exact information--coordination wedge in the declared binary game;
- strict topology-dependent information hysteresis in the declared synthetic
  three-player game;
- pooled natural association between predictive connectivity and mismatch under
  the preregistered broad analysis;
- a null registered wigeon prediction for predictive-connectivity modulation of
  phase correction;
- separation of pre-commitment information and post-error correction as
  empirical coordinates;
- an exact private value-of-waiting threshold and information-acquisition
  coordination wedge;
- a source-backed flycatcher--tit experimental anchor for timing-dependent
  information availability;
- a non-monotone information-induced desynchronization result in which
  monotonically improving cue reliability temporarily increases partner
  mismatch because actors cross waiting thresholds at different cue qualities.

PAYOFF-B may not currently claim:

- that natural interaction networks have already been shown to undergo
  predictive-connectivity hysteresis;
- a universal predictive-connectivity coefficient across bird species;
- that climate change has caused the specific rho values in the synthetic game;
- that the 118/391 or 52/364 grid frequencies are natural prevalences;
- that predictive connectivity is a universal phase controller;
- that the old 0.90/0.50 boundary witness is a strict equilibrium.

## Next decisive empirical target

The remaining missing link is a long natural time series containing:

    predictive connectivity decreases
    -> partner timing regime changes
    -> predictive connectivity later recovers
    -> partner timing does or does not recover.

That is the direct empirical test of the hysteresis claim. Until then, the
hysteresis conclusion is mechanistic theory supported by a natural
predictive-information axis, not an observed natural hysteresis event.
