# Prediction and reactive correction as substitute control channels

Date: **2026-10-02**  
Status: **prospective theory developed after existing barnacle/wigeon outcomes; those outcomes remain non-confirmatory for this model**

## Motivation

An earlier PAYOFF-B empirical prediction expected routes with stronger
pre-existing environmental predictability to show stronger post-error phase
correction.

That prediction was not supported in the preregistered Eurasian-wigeon test,
and the existing barnacle-goose transition screen also did not support a simple
positive predictability -> correction relation.

A different mechanism is possible:

> good prediction can reduce the error that reaches the feedback stage, making
> strong reactive correction less useful.

This note derives that mechanism exactly.

## 1. Model

Let

    R(q) >= 0

be expected mismatch loss after the actor has used whatever pre-commitment
information is available at cue quality q.

Let

    g in [0,1]

be downstream reactive correction gain.

Then residual mismatch is scaled by

    lambda = 1-g.

Assume quadratic residual mismatch loss and quadratic correction cost:

    L(g;q)
      =
      (1-g)^2 R(q)
      + (c/2) g^2,

with c>0.

The first term says that stronger feedback reduces already-existing mismatch.
The second says that stronger correction is costly.

## 2. Exact optimum

Differentiating,

    dL/dg
      =
      -2R(q)(1-g) + c g.

The unique optimum is

    g*(q)
      =
      2R(q) / [c+2R(q)],

and therefore

    lambda*(q)
      =
      c / [c+2R(q)].

The minimized loss is

    L*(q)
      =
      c R(q) / [c+2R(q)].

## 3. Prediction-correction substitution theorem

For fixed c,

    dg*/dR
      =
      2c/[c+2R]^2
      >
      0,

and

    d lambda*/dR
      =
      -2c/[c+2R]^2
      <
      0.

Therefore:

> systems entering the correction stage with more mismatch optimally use
> stronger reactive correction.

If better pre-commitment information decreases R(q), then:

    q improves
      ->
    pre-correction risk falls
      ->
    optimal correction gain falls
      ->
    phase retention lambda rises.

So **better information and stronger downstream feedback are substitutes** in
this declared model.

They need not be positively correlated.

## 4. Bridge to the canonical Paper-2 information model

In the existing binary model, let

    R0 = min(A,L)

be prior Bayes risk and

    V_A(q)

the canonical value of information.

Then

    R(q)
      =
      R0 - V_A(q).

Below the cue-actionability threshold q0, V_A(q)=0, so correction strength is
unchanged by q.

Above q0,

    R(q)
      =
      R0 - [S q - B],

and therefore

    dR/dq = -S.

Substitution is exact:

    d lambda*/dq
      =
      2 c S / [c+2R(q)]^2
      >
      0.

Thus, once the cue becomes behaviorally actionable, increasing cue reliability
raises optimal phase retention because less reactive correction is needed.

At perfect information,

    R(1)=0,
    g*(1)=0,
    lambda*(1)=1.

Perfect anticipation removes the need for post-error correction in this
minimal model.

## 5. Why this matters for empirical interpretation

A low observed lambda can mean strong post-error correction.

A high observed lambda can mean either:

- weak correction capacity;
- high correction cost;
- little error requiring correction because prediction was already good;
- a different ecological interval or measurement scale.

Therefore

    high predictability
    !=
    strong feedback gain

and

    high lambda
    !=
    poor information use.

This reinforces the two-axis interpretation:

    prediction before error
    and
    correction after error

must be measured separately.

## 5.5 Unified prediction-versus-compensation-information balance

The fixed-c model above captures only one pathway: better information lowers
pre-correction mismatch risk.

The existing PAYOFF-B dual-use theory adds a second pathway: the same cue may
also make downstream compensation cheaper or more targeted.

Let both objects depend on q:

    R = R(q) > 0,
    c = c(q) > 0.

The optimal correction gain remains

    g*
      =
      2R/(c+2R).

Differentiating,

    dg*/dq
      =
      2[c R' - R c']
      / (c+2R)^2.

The clearest form is the correction-odds derivative:

    d/dq log[g*/(1-g*)]
      =
      R'/R
      -
      c'/c.

This creates an exact mechanism boundary.

### Prediction-substitution dominant

If

    R'/R < c'/c,

then

    dg*/dq < 0.

Mismatch risk is falling proportionally faster than correction cost. Better
prediction reduces the need for downstream feedback.

### Cue-informed-correction dominant

If

    R'/R > c'/c,

then

    dg*/dq > 0.

Correction cost/effective difficulty is falling proportionally faster than
pre-correction risk. Better information makes downstream correction more
attractive.

### Local balance

If

    R'/R = c'/c,

then

    dg*/dq = 0.

Improved prediction and improved compensation exactly offset locally.

This resolves an apparent tension between two PAYOFF-B mechanisms:

- information can prevent error before commitment;
- information can also help repair error after commitment.

Those two effects have opposite consequences for observed feedback strength.

## 5.6 Empirical consequence

A q-by-correction association does not have one universal expected sign.

A positive association between q and correction can arise when cue-informed
compensation dominates.

A negative association can arise when predictive error prevention dominates.

A null association can arise when the pathways approximately balance, when
neither pathway is strong, or when measurement error is large.

Therefore future tests should estimate, where possible:

1. q -> pre-correction mismatch risk R;
2. q -> correction cost/effectiveness c;
3. R/c -> realized correction gain.

This is stronger than testing one marginal q -> correction slope.

## 6. Existing natural evidence: motivation, not confirmation

### Eurasian wigeon

The preregistered interaction

    incoming phase error x historical predictive connectivity

predicted stronger correction on more predictable route pairs.

Observed:

    beta = +0.0202
    95% CI = [-0.1058, 0.1461]
    p = 0.756
    NOT_SUPPORTED.

This outcome was known before the present substitution model was derived.
It therefore remains a failed preregistered prediction, not confirmation of the
new model.

### Barnacle goose

Existing route-stage data show environmental predictability and phase retention
occupying different combinations. The earlier seven-pair screen did not support
the simple prediction that higher predictability implies stronger correction.

Five stable registry rows happen to show a strong rank ordering in which higher
predictability accompanies larger |lambda| and therefore weaker correction.
Because this pattern was noticed after those outcomes were available and the
rows are non-independent transitions within one taxon, it is an exploratory
motivation only.

No inferential promotion is licensed.

## 7. New prospective prediction

For a future dataset in which pre-correction mismatch risk R(q) and correction
cost c can be measured independently:

1. higher q should lower R(q);
2. conditional on c, lower R should reduce optimal correction gain g;
3. the q -> g relation should disappear below the cue-actionability threshold;
4. correction gain should increase with mismatch risk at fixed q/c;
5. systems with larger correction cost c should retain more error at the same
   pre-correction risk.

A valid test should estimate the q -> R link and the R -> correction link
separately before combining them.

## 8. Relationship to the continuous information-actionability theorem

The two prospective modules answer different questions.

**Continuous information-actionability theorem**

    when should the actor commit while information improves and options vanish?

**Prediction-correction substitution**

    after commitment/error, how much costly correction should the actor deploy?

Together they imply a three-stage seasonal control architecture:

    information acquisition
      ->
    commitment
      ->
    reactive correction.

A system can achieve low final mismatch through different allocations across
these stages.

That is why low observed mismatch alone cannot identify whether a species had:

- good prediction;
- late/early commitment;
- large recourse;
- strong feedback correction;
- or some combination.

## Claim boundary

Allowed:

> In a prospective quadratic-control model, better pre-commitment information
> can optimally reduce the need for downstream reactive correction.

Avoid:

> The existing barnacle-goose data confirm prediction-correction substitution.

Avoid:

> The wigeon registered null supports the new substitution theorem.

Avoid:

> phase-retention lambda is a direct measure of retained actionability r.
