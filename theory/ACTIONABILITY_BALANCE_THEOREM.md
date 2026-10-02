# PAYOFF-B prospective actionability-balance theorem

Date: **2026-10-02**  
Status: **prospective exact extension; frozen GEB Paper 2 unchanged**

## 1. Why this extension exists

The frozen Paper-2 theorem asks whether a later cue is worth waiting for.

The stagewise extension adds a second process:

- information quality can improve through time;
- the set of actions still available can shrink through time.

The result is a direct mathematical version of the ecological intuition:

> later information can be more accurate yet less useful because the actor has
> fewer remaining ways to respond.

Generic sequential value-of-information, Bayesian stopping and irreversible
decision theory are established prior art. This note does not claim novelty for
those ideas. It records exact consequences of the declared PAYOFF-B reduced
model.

## 2. Canonical Paper-2 information value

Let

    A = (1-pi) C_F,
    L = pi C_M,
    S = A+L,
    B = max(A,L),
    R0 = min(A,L).

Above the cue-actionability boundary

    q0 = B/S,

the canonical information value is

    V_A(q)=S q-B.

The merged stagewise extension introduces retained actionability

    r(t) in [0,1],

so the usable information value is

    V(t)=r(t)[S q(t)-B].

Let C(t) be cumulative waiting cost. The net value of waiting until time t is

    N(t)=r(t)[S q(t)-B]-C(t).

## 3. Actionability-balance condition

For differentiable q(t), r(t) and C(t), any interior stationary point with
q(t)>q0 and r(t)>0 satisfies

    dN/dt
      = r(t) S q'(t)
        + r'(t)[S q(t)-B]
        - C'(t)
      = 0.

Therefore,

    r S q'
      = -r' [S q-B] + C'.

Interpretation:

- left side = marginal gain from improving information;
- first right-side term = marginal loss because recourse is disappearing;
- second right-side term = marginal direct cost of waiting.

With zero marginal waiting cost,

    S q' / [S q-B]
      =
    -r'/r.

So the **relative rate of information-value gain** must equal the
**relative rate of optionality loss**.

This is the actionability-balance condition.

## 4. Exponential learning / exponential irreversibility theorem

Take a cue trajectory that begins exactly at the Paper-2 actionability boundary:

    q(t)
      =
    q0 + Delta_q [1-exp(-alpha t)],

with

    alpha>0,
    0<Delta_q<=1-q0.

Let retained actionability decay as

    r(t)=exp(-beta t),

with beta>0.

Then, with no additional waiting cost,

    N(t)
      =
    S Delta_q
    exp(-beta t)
    [1-exp(-alpha t)].

At t=0,

    N(0)=0.

As t -> infinity,

    N(t)->0.

Differentiating gives

    N'(t)
      =
    S Delta_q exp(-beta t)
    [(alpha+beta)exp(-alpha t)-beta].

Hence there is one and only one interior maximum at

    exp(-alpha t*)=beta/(alpha+beta),

or

    t*
      =
    log(1+alpha/beta)/alpha.

### Consequence 1 — perfect information is generally too late

If q(t) approaches its maximum only asymptotically while r(t)->0, the maximal
behavioral value occurs before cue quality is maximal.

For the symmetric witness

    q0=0.5,
    Delta_q=0.5,
    alpha=beta=1,

the optimum is

    t*=log 2,

and

    q(t*)=0.75,

even though

    q(infinity)=1.

Thus the best time to use information is not the time at which the state is
known most accurately.

### Consequence 2 — faster irreversibility causes earlier commitment

Holding the cue trajectory fixed,

    t*(beta)
      =
    log(1+alpha/beta)/alpha

is strictly decreasing in beta.

Two actors observing exactly the same environmental-information trajectory can
therefore commit at different times solely because their remaining recourse
decays at different rates.

For actors 1 and 2,

    Delta t
      =
    | log(1+alpha/beta_1)
      - log(1+alpha/beta_2) |
    / alpha.

This is the continuous-time analogue of the frozen Paper-2 asynchronous
information-use window.

## 4.5 Finite information-use window

Now compare the hump-shaped actionable-information value with a fixed positive
effective deadline cost D:

    use information iff
    K exp(-beta t)[1-exp(-alpha t)] > D,

where

    K=S Delta_q.

Because the left-hand side is zero at t=0, strictly positive at intermediate
times, and returns to zero as t -> infinity, the timing geometry is
non-monotone even though q(t) itself is monotone increasing.

Let G_max be the unique peak value.

Then:

- if D > G_max: information is never worth using;
- if D = G_max: there is one tangency time;
- if 0 < D < G_max: there are exactly two crossings

      t_- < t* < t_+,

  and information is worth using only for

      t_- < t < t_+.

Thus information can become worth using and later cease to be worth using
**while cue accuracy is still improving**.

For the equal-rate special case

    alpha=beta=lambda,

write

    x=exp(-lambda t).

Then

    G/K=x(1-x),

whose maximum is 1/4. If

    0 < D/K < 1/4,

the two crossings are

    x_early
      =
    [1+sqrt(1-4D/K)]/2,

    x_late
      =
    [1-sqrt(1-4D/K)]/2,

so

    t_-
      =
    -log(x_early)/lambda,

    t_+
      =
    -log(x_late)/lambda.

This is the strongest "Schroedinger's spring" consequence of the declared
reduced model:

> early in the journey, the box is too opaque; late in the journey, the box is
> clear but there is too little action left. Information matters only in the
> intermediate actionability window.

This is not a claim that generic non-monotone stopping regions are new. The
specific ecological contribution would be the mapping from seasonal cue
predictability and biological recourse loss into a testable finite-use window.

## 5. Linear direct waiting cost

Now let

    C(t)=c t,
    c>=0.

Define

    K=S Delta_q.

Then

    N(t)
      =
    K exp(-beta t)[1-exp(-alpha t)]
      - c t.

The derivative at the origin is

    N'(0)=K alpha-c.

Therefore:

- if c >= K alpha, immediate commitment is optimal;
- if 0<c<K alpha, the unique optimum lies strictly before the zero-cost peak;
- if c=0, the closed-form peak above is recovered.

So direct waiting cost and shrinking actionability push commitment in the same
direction: earlier.

## 6. Link to the merged r-adjusted threshold

The merged stagewise branch already proves

    V(q,r)=r V_A(q).

With fixed effective waiting cost D,

    wait iff r V_A(q) > D.

For r>0 and D<rR0,

    q_wait(r)
      =
    [B+D/r]/S.

Thus loss of actionability is equivalent, in the declared reduced model, to
inflating effective deadline cost from

    D

to

    D/r.

The continuous theorem says the same thing dynamically:

- q(t) generally rises;
- r(t) generally falls;
- D(t) may rise through direct waiting costs;
- optimal commitment occurs where marginal information gain no longer offsets
  lost actionability plus waiting cost.

## 7. Ecological interpretation

The theorem separates three quantities that are often collapsed into one date:

1. **cue-quality trajectory q(t)** — how well the actor can predict the later
   fitness-relevant state at stage t;
2. **retained actionability r(t)** — how much of the fully informed response is
   still implementable at stage t;
3. **waiting-cost trajectory C(t)** — direct costs accumulated by postponing
   commitment.

This allows two superficially opposite migration strategies to arise from one
principle:

- early relative to the resource wave -> slow progression / longer stopover;
- late relative to the resource wave -> fast progression / shorter stopover.

The biological content is not that one taxon has a universally high or low r.
Migration speed, stopover duration, flowering duration, emergence flexibility,
route choice and breeding delay are all candidate recourse mechanisms.

## 8. Existing source-backed evidence

The current prospective evidence receipt records:

- mule deer: early and late migrants use opposite movement/stopover corrections;
- bar-tailed godwits: earlier departure can be absorbed by longer later stopover;
- pink-footed geese: cue relevance changes along a route and progression is
  updated en route;
- plant-butterfly systems: local partners can have unequal thermal sensitivity;
- Viola-bee systems: flowering/activity duration can buffer overlap loss.

These sources establish the biological pieces, not natural estimates of q(t),
r(t), D_eff, or the exact t* formula.

## 9. Direct empirical test required

A strong natural test needs repeated stages for the same decision problem.

At each stage t estimate independently:

    q_t
      = predictive accuracy of the information available at stage t,

and

    r_t
      = retained response value/capacity relative to a declared fully
        actionable reference.

Then test whether observed commit/use behavior aligns with

    r_t V_A(q_t) - C_t,

or, in the exponential special case, whether systems with faster measured loss
of recourse commit earlier under comparable information-gain trajectories.

The current repository does **not** yet contain a natural system with q_t and
r_t jointly identified on this scale.

## 10. Claim boundary

Safe:

> In the declared PAYOFF-B reduced model, increasing cue quality and declining
> actionability produce an exact balance condition. Under exponential learning
> and exponential recourse loss, actionable information has a unique
> intermediate-time maximum and actors with faster loss of recourse commit
> earlier under the same cue trajectory.

Not licensed:

> This is a new general theorem of optimal stopping.

Not licensed:

> Real migrants follow exponential q(t) and r(t).

Not licensed:

> Migration speed, stopover duration or flowering duration is numerically equal
> to r.

Not licensed:

> Existing natural data directly validate the predicted t*.
