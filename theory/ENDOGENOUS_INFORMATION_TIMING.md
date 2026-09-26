# PAYOFF-B endogenous information timing

Date: **2026-09-26**  
Status: **exact minimal extension plus source-backed ecological anchor**

## Question

The partial-information game asks what happens when different species possess
different information about a future seasonal state.

A deeper issue is that information itself may not be available at the same
time as the ecological decision.

A migrant may therefore face:

    act now with poor information
    versus
    wait until a better cue becomes observable.

Waiting is not free. Delaying arrival, settlement, territory acquisition or
pairing can reduce fitness.

So information availability is an **endogenous consequence of decision
timing**, not merely a fixed species trait.

## Exact binary decision

Let the future state be

    theta in {normal, early}

with prior probability pi of the early state.

Before the new cue appears, the decision maker chooses the lower expected loss
between acting early and acting late.

With false-early cost C_F and missed-early cost C_M,

    R_prior
    = min[(1-pi) C_F, pi C_M].

After waiting, a symmetric cue has state-classification accuracy q. The actor
updates on the cue and chooses the lower-loss action separately for each cue
outcome. Let the resulting Bayes risk be R_q.

The private value of waiting for information is

    V_private(q)
    = R_prior - R_q
    >= 0.

If waiting costs D in lost mating, rank, territory or time opportunity, the
individual waits iff

    V_private(q) > D.

Otherwise it rationally commits before the cue becomes available.

## Actionable information has a threshold

More reliable information does not necessarily change decisions smoothly.

For the transparent witness

    pi  = 0.40
    C_F = 2
    C_M = 1,

the private value of information is

| cue accuracy q | V_private |
|---:|---:|
| 0.50 | 0 |
| 0.60 | 0 |
| 0.70 | 0 |
| 0.80 | 0.08 |
| 0.90 | 0.24 |
| 1.00 | 0.40 |

At low reliability, the optimal action is the same after either cue outcome, so
extra signal quality has zero behavioural value. Only after reliability crosses
the action threshold does information become useful.

Thus:

> **available information is not the same thing as actionable information.**

## Information acquisition can itself contain a coordination wedge

Suppose a wrong timing decision also harms interaction partners.

Let E_F and E_M be partner losses from false-early and missed-early decisions.
The system-level costs become

    C_F + E_F
    and
    C_M + E_M.

This gives a joint value of waiting

    V_joint(q).

When partner mismatch matters,

    V_joint(q)

can exceed the focal individual's private information value.

For example, with

    pi = 0.40
    q  = 0.90
    C_F = 2
    C_M = 1
    E_F = E_M = 1,

we obtain

    V_private = 0.24
    V_joint   = 0.54.

For any delay cost

    0.24 <= D < 0.54,

the individual rationally commits early under uncertainty while the interacting
system would benefit if it waited for the cue.

This is an **information-acquisition coordination wedge**.

The coordination problem therefore begins before action selection: selection
can under-invest in information acquisition itself.

## Endogenous information asymmetry between actors

If two actors face the same prospective information but different delay costs,

    D_A > V_private > D_B,

then actor A commits before the cue and actor B waits.

They therefore enter the later ecological game with different information
sets, even though the underlying cue process is identical.

This supplies a simple route to sex-, guild- or life-history-specific
information availability.

It must not be interpreted as proof that any observed sex difference was caused
by these exact costs; it is a mechanism.

## Pied flycatcher–tit experimental anchor

Samplonius & Both (2017, Journal of Animal Ecology,
DOI 10.1111/1365-2656.12640) experimentally advanced and delayed hatching of
resident tits in forest plots across 2014 and 2015.

The result has exactly the temporal asymmetry required for an ecological anchor.

### Earlier male decision

The study reports 159 arriving male pied flycatchers. Male settlement among
available nest boxes did not vary detectably with manipulated tit timing
(Z = 0.854, P = 0.393).

The authors note that almost all males had settled before the manipulated
difference became apparent through tit hatching.

Thus the lack of a treatment response occurred in a decision period when the
relevant manipulated social cue was largely unavailable.

### Later female decision

The study reports 114 arriving females. Females preferentially paired in plots
with earlier tit phenology.

The published pairing GLMM gives

    tit-timing estimate = -0.101
    SE = 0.050
    Z  = -2.030
    P  = 0.042.

A time-dependent Cox analysis gives

    tit-timing estimate = -0.065
    exp(coef) = 0.936
    SE = 0.025
    Z = -2.61
    P < 0.009.

Treatment separation became stronger later in the female settlement period,
coinciding with the stage when early-treatment tits had begun hatching.

Importantly, male and female arrival dates themselves were unrelated to tit
timing treatment. The experimental signal is therefore in settlement/pairing
conditional on when information was available, not in the migration arrival
date itself.

## PAYOFF-B interpretation

The experiment supports a source-backed statement that:

> **the same heterospecific phenological state can be unavailable to an early
> decision maker and behaviourally relevant to a later decision maker.**

This is exactly the information-timing distinction required by the new model.

It does not prove that females deliberately waited to acquire tit information.
Nor does it identify whether the effective cue was direct observation of
hatching, correlated food conditions, competition or predation risk.

The source paper explicitly leaves that mechanism unresolved.

## Connection to the current PAYOFF-B evidence chain

The information programme now has three empirical/theoretical levels:

1. **pre-commitment predictive connectivity**  
   Broad migratory birds show a pooled association between historical
   predictive connectivity and smaller mismatch.

2. **information availability at decision time**  
   The flycatcher experiment shows that heterospecific phenology affected later
   settlement decisions but not the earlier male settlement decision made
   before treatment visibility.

3. **network memory after an information shock**  
   The strict Bayesian game predicts that transient information loss can shift
   an interaction network into a lower-payoff timing regime that persists after
   information recovers, depending on network topology.

Only level 3 remains without a direct natural hysteresis observation.

## Prior-art boundary

The value and costs of information are established topics in ecology and
decision theory. Work on migration timing has already shown that environmental
predictability changes the value of information, and behavioural ecology has
emphasized costs of acquiring social information.

PAYOFF-B therefore does not claim novelty for "information has value" or
"waiting for information can be costly."

The candidate contribution is the integration of:

    decision timing
    -> endogenous information access
    -> private versus joint value of waiting
    -> asymmetric information among interactors
    -> coordination regime and network memory.

## Claim ceiling

Currently licensed:

- exact value-of-waiting and private-versus-joint threshold results in the
  declared binary model;
- an exact information-acquisition coordination wedge;
- a published experimental anchor showing timing-dependent access to a
  manipulated heterospecific phenology signal;
- a mechanistic interpretation of information asymmetry as potentially
  endogenous to timing costs.

Not licensed:

- that male flycatchers consciously choose ignorance;
- that female flycatchers delay arrival in order to observe tit phenology;
- that the original experiment measured C_F, C_M or D;
- that the flycatcher system exhibits the predicted recovery hysteresis.
