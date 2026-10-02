# Continuous information-actionability optimum

Date: **2026-10-02**  
Status: **prospective exact reduced-form theorem; frozen GEB Paper 2 unchanged**

## Ecological question

As a seasonal decision approaches, two things can happen at the same time:

1. environmental information becomes more accurate;
2. the set of useful downstream responses shrinks.

A long-distance migrant may learn more about destination spring as it moves
north, while simultaneously losing the ability to change route, stopover
duration, pace or settlement timing. A flowering plant can receive increasingly
relevant local thermal information while the remaining flowering window
shortens.

The relevant question is therefore not:

> how accurate is the cue?

but:

> how fast is useful information improving relative to how fast biological
> optionality is disappearing?

## 1. Bridge to the canonical Paper-2 information value

Use the existing binary loss structure

    A = (1-pi) C_F
    L = pi C_M
    S = A + L
    B = max(A,L)
    R0 = min(A,L).

Above the canonical cue-actionability boundary

    q0 = B/S,

the fully actionable information value is

    V_A(q) = S q - B.

Let

    r(t) in (0,1]

be a declared reduced-form retained-actionability weight, and let

    D(t) >= 0

be cumulative effective waiting cost.

Define net value of waiting until stage/time t as

    F(t)
      = r(t)[S q(t)-B] - D(t),

within the smooth region q(t)>q0.

## 2. Exact first-order balance

Differentiating,

    F'(t)
      = r'(t)[S q(t)-B]
        + r(t) S q'(t)
        - D'(t).

At any interior optimum t*,

    F'(t*) = 0.

Dividing by positive actionable information gives

    S q'(t*) / [S q(t*)-B]
      =
      -r'(t*) / r(t*)
      +
      D'(t*) /
      {r(t*)[S q(t*)-B]}.

Interpretation:

    relative information-gain rate
      =
    recourse-attrition rate
      +
    marginal waiting-cost burden.

This is the continuous-time counterpart of the discrete stagewise Bellman
result.

### Zero marginal waiting cost

If D'(t)=0,

    S q'(t) / [S q(t)-B]
      =
    -r'(t)/r(t).

So the optimum occurs when the percentage rate at which actionable information
is improving equals the percentage rate at which optionality is being lost.

This gives a precise form to the "Schroedinger's spring" intuition:

> waiting is useful while information is improving faster than biological
> options are disappearing; commitment becomes optimal after that balance
> reverses.

Generic continuous-time optimal stopping is established prior art. The
candidate ecological contribution is the exact specialization to the PAYOFF-B
information-deadline geometry and its actor-specific mismatch implications.

## 3. Closed-form exponential witness

Let information approach perfect accuracy exponentially from the canonical
actionability boundary:

    q(t)
      = q0
        + (1-q0)[1-exp(-alpha t)],

with alpha>0.

Let retained actionability decay exponentially:

    r(t)=exp(-beta t),

with beta>0.

Set D(t)=0.

Then

    F(t)
      =
      S(1-q0)
      exp(-beta t)
      [1-exp(-alpha t)].

The unique finite maximizer is

    t*
      =
      log(1+alpha/beta) / alpha.

At that time,

    exp(-alpha t*)
      =
      beta/(alpha+beta),

and therefore

    q*
      =
      q0
      + (1-q0) alpha/(alpha+beta),

    r*
      =
      [beta/(alpha+beta)]^(beta/alpha).

The maximum actionable information value is

    F(t*)
      =
      S(1-q0)
      [alpha/(alpha+beta)]
      [beta/(alpha+beta)]^(beta/alpha).

## 4. Comparative statics

The exact witness gives three immediate results.

### Faster information acquisition

Holding beta fixed, larger alpha moves useful information earlier and increases
the maximum actionable information available.

### Faster recourse loss

Holding alpha fixed, larger beta moves the optimal commitment time earlier and
reduces the maximum actionable information that can be exploited.

### Neither "wait as long as possible" nor "act as early as possible" is general

For alpha,beta>0:

    F(0)=0,

and

    lim_{t->infinity} F(t)=0.

Therefore the optimum is interior.

The state is poorly known at the start, but perfectly known information arriving
after all actionability has disappeared is also worthless.

## 5. Canonical numerical witness

For the current Paper-2 loss scale

    pi=0.4,
    C_F=2,
    C_M=1,

we have

    A=1.2,
    L=0.4,
    S=1.6,
    B=1.2,
    q0=0.75.

If

    alpha=1,
    beta=1,

then

    t*=log(2),
    q*=0.875,
    r*=0.5,

and

    F(t*)=0.10.

Thus the best decision occurs with an imperfect cue and only half the declared
initial actionability remaining.

## 6. Two-actor implication

Suppose two interacting actors observe the same q(t) but have different
recourse-loss functions r_1(t), r_2(t) and/or waiting-cost paths D_1(t),D_2(t).

Their interior commitment conditions are

    S q'/(S q-B)
      =
      -r_i'/r_i
      + D_i'/{r_i(S q-B)}.

Unless the right-hand sides are identical, the optimal commitment times need
not match.

Therefore a shared improving environmental cue can create **asynchronous
commitment solely from different rates of losing optionality**, even when both
actors receive the same information trajectory.

This is the continuous-time analogue of the current Paper-2 asynchronous cue
uptake window.

## 6.5 Exact pairwise desynchronization under one shared cue trajectory

Let two interacting actors experience the same information-improvement rate
alpha but lose recourse at rates beta_1 and beta_2.

Then

    t_i*
      = log(1+alpha/beta_i) / alpha,

and therefore

    Delta t*
      =
      | log[(1+alpha/beta_1)/(1+alpha/beta_2)] |
      / alpha.

Their cue accuracies at commitment are

    q_i*
      =
      q0 + (1-q0) alpha/(alpha+beta_i).

Hence beta_1 != beta_2 gives both:

1. different optimal commitment times;
2. different cue accuracies at commitment.

The actor losing recourse faster commits earlier and accepts a less accurate
cue.

This produces stagewise seasonal desynchronization **without different cue
trajectories**. Heterogeneity in the rate of losing optionality is sufficient.

This is the continuous-time analogue of the frozen Paper-2 result that
heterogeneous effective deadlines create a finite asynchronous-uptake window.

## 7. Empirical identification boundary

The theorem does not license interpreting arbitrary biological measurements as
r(t).

A natural test needs:

1. a prespecified cue-quality trajectory q(t), or an externally calibrated
   monotone information score;
2. a prespecified biological mapping from remaining route/timing/phenological
   options to retained actionability r(t);
3. cumulative and marginal waiting costs D(t), if non-negligible;
4. observed commitment or actuator switching times.

The current repository does not yet contain one natural system in which all four
are identified on a common scale.

Strong component evidence exists:

- mule deer: signed speed/stopover recourse;
- godwits: early-departure timing can be absorbed by later stopover;
- pink-footed geese: cue relevance changes along the route;
- greater snow goose: preregistered route-level cue-uptake and downstream
  transit-compression lanes exist but focal event data remain access-blocked;
- plant-pollinator systems: partner response sensitivities and phenological
  window widths can differ, but neither should be relabelled as r without an
  explicit model.

## 8. Claim boundary

Allowed:

> In the declared reduced model, optimal commitment balances the relative gain
> in useful environmental information against the rate at which biological
> recourse is lost and the marginal cost of waiting.

Allowed:

> Even perfectly improving information need not justify waiting to the latest
> possible decision time.

Avoid:

> This first-order condition is a new theorem of generic optimal stopping.

Avoid:

> Migration distance, remaining route distance, stopover duration or flowering
> duration is itself the retained-actionability variable r.

Avoid:

> Existing natural data directly validate the full continuous q(t)-r(t)
> trajectory.
