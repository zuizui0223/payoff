# PAYOFF-B competitive-information extension

Date: **2026-10-07**  
Status: **prospective reduced-form extension; frozen PAYOFF-B manuscripts unchanged**

## 1. Why this extension exists

The current PAYOFF-B actionability theorem already separates:

- improving information quality through time;
- declining ability to act on that information;
- direct waiting cost.

That gives

[
N(t)=r(t)V_A(q(t))-C(t),
]

where (q(t)) is cue quality, (r(t)) is retained actionability and, above the canonical actionability boundary,

[
V_A(q)=S q-B.
]

A horse-racing / prediction-market analogy exposes a second way in which useful information can disappear even when the focal actor remains fully able to act:

> the information can become progressively incorporated into the choices or prices of other actors.

This is mechanistically different from irreversibility, but in a declared reduced form it enters the usable-value equation multiplicatively.

## 2. Competitive-information reduced form

Let

[
e(t)in[0,1]
]

be **retained information exclusivity**: the fraction of the focal information advantage that has not yet been absorbed by competitors or a market.

This is not claimed to be a universal market-efficiency parameter. It is a reduced-form weight for the part of focal information value that remains relatively exploitable.

Define

[
oxed{
N(t)=r(t)e(t)[S q(t)-B]-C(t)
}
]

whenever (q(t)>q_0=B/S).

Interpretation:

- (q(t)): how accurately the focal actor can infer the hidden state;
- (r(t)): how much state-contingent response capacity remains;
- (e(t)): how much of the focal informational advantage remains unabsorbed by others;
- (C(t)): direct cost of waiting.

The previous PAYOFF-B actionability model is recovered exactly by (e(t)=1).

A pure competitive-information case is obtained by (r(t)=1).

## 3. Competitive actionability-balance theorem

For differentiable paths,

[
rac{dN}{dt}
=
r e S q'
+
r' e [S q-B]
+
r e'[S q-B]
-
C'.
]

Any interior stationary point therefore satisfies

[
r e S q'
=
-r'e[S q-B]
-r e'[S q-B]
+C'.
]

With zero marginal waiting cost and positive (r,e,V_A),

[
oxed{
rac{S q'}{S q-B}
=
-rac{r'}{r}
-rac{e'}{e}
}
]

so the relative gain in focal information value is balanced by the **sum** of:

1. the relative rate of lost actionability;
2. the relative rate of lost information exclusivity.

This is the central bridge between the ecological and racing interpretations.

## 4. Exponential learning, irreversibility and diffusion

Let cue quality improve from the canonical actionability boundary as

[
q(t)
=
q_0+Delta_q[1-exp(-alpha t)],
]

with (alpha>0), and let

[
r(t)=exp(-eta t),
qquad
e(t)=exp(-gamma t),
]

with (eta,gammage0) and (eta+gamma>0).

Then, for (K=SDelta_q),

[
N(t)
=
Kexp[-(eta+gamma)t]
[1-exp(-alpha t)]
]

when (C(t)=0).

The unique interior maximum is

[
oxed{
t^*
=
rac{logleft(1+alpha/(eta+gamma)ight)}{alpha}.
}
]

### Corollary 1 — hazards add

Only the sum

[
eta+gamma
]

enters the closed-form optimum.

Faster biological irreversibility and faster competitive information diffusion therefore move the optimum earlier in exactly the same mathematical direction.

### Corollary 2 — ecological limit

If

[
gamma=0,
]

then

[
t^*
=
rac{log(1+alpha/eta)}{alpha},
]

which is exactly the existing PAYOFF-B actionability result.

### Corollary 3 — competitive-information limit

If

[
eta=0,qquad gamma>0,
]

then an interior optimum still exists:

[
t^*
=
rac{log(1+alpha/gamma)}{alpha}.
]

Thus useful information can peak before predictive accuracy peaks even when the focal actor loses no physical ability to act.

### Corollary 4 — identification alias

Timing of the value peak alone identifies only

[
eta+gamma,
]

not the separate mechanisms.

Therefore a natural dataset cannot infer “lost recourse” versus “information absorbed by others” from the timing optimum alone. Independent measurements of actionability and competitive information diffusion are required.

This is an important claim boundary for cross-system comparisons.

## 5. Why pari-mutuel horse racing is a useful boundary case

In a pari-mutuel system, an early displayed price is not generally a fixed price locked in by an early wager. The final pool determines the eventual payout.

Therefore the clean PAYOFF object is **not**:

> bet early to capture the early displayed odds.

With unchanged action sets, no transaction cost and the same final-pool settlement, waiting for weakly more information until the last feasible decision point is weakly preferred in the ordinary Bayes-decision sense.

The useful empirical object is instead the time path of **incremental predictive information relative to the market**.

Horse racing is therefore valuable because it separates:

- improving focal prediction;
- collective market learning;
- a sharp final action deadline.

## 6. Empirical estimands for racing

For race (r), horse (i), and pre-race time (t), define

[
p_{irt}
=
P(i	ext{ wins}mid I_t)
]

from a model restricted to information available by (t).

Let normalized market-implied win probability be

[
m_{irt}.
]

For each time slice, evaluate both distributions with the same proper scoring rule.

For multinomial log loss:

[
L_{m model}(t)
=
-rac{1}{R}
sum_r log p_{w_r r t},
]

[
L_{m market}(t)
=
-rac{1}{R}
sum_r log m_{w_r r t},
]

where (w_r) is the winner.

Define incremental predictive value over the contemporaneous market as

[
oxed{
Delta_{m market}(t)
=
L_{m market}(t)-L_{m model}(t).
}
]

Positive (Delta_{m market}) means the focal model predicts outcomes better than the contemporaneous market at that time.

The primary decoupling hypothesis is:

[
L_{m model}(t)
downarrow
]

as race time approaches, while

[
Delta_{m market}(t)
]

need not increase and may peak earlier or shrink toward zero.

In words:

> **a forecast can keep getting better while its incremental value over the collective forecast gets worse.**

This is the racing analogue of PAYOFF-B’s “information improves while actionability disappears.”

## 7. Prospective first test

Use fixed predeclared time slices, for example:

- 60 min before scheduled post;
- 30 min;
- 15 min;
- 10 min;
- 5 min;
- last available snapshot before close.

At every time slice:

1. use only covariates available by that time;
2. generate horse-level win probabilities that sum to one within race;
3. normalize contemporaneous win-market implied probabilities;
4. score model and market on the same held-out races;
5. estimate (L_{m model}(t)), (L_{m market}(t)), and (Delta_{m market}(t));
6. bootstrap by race, not by horse.

The primary test is **not betting profit**. It is the shape of predictive accuracy and incremental information value through time.

A later profitability analysis would require explicit treatment of takeout, final settlement odds, stake sizing, pool impact and transaction constraints.

## 8. Data feasibility boundary

JRA-VAN Data Lab publicly documents:

- real-time odds provision during wagering;
- time-series odds recorded at roughly 5–10 minute intervals;
- time-series support for win/place, bracket quinella and quinella records.

This is sufficient in principle for a prospective time-sliced prediction-versus-market test, subject to obtaining the Data Lab records and respecting its access conditions.

No racing outcome has been inspected or used to choose a preferred time window in this branch.

## 9. Relation back to PAYOFF-B

The general distinction is now:

[
	ext{information becomes unusable because}
]

[
oxed{
	ext{the actor can no longer respond}
}
]

or

[
oxed{
	ext{others have already absorbed the same information}.
}
]

Both can occur while raw predictive accuracy is still improving.

The strongest general headline licensed by the reduced model is:

> **Information is valuable only while it remains both actionable and differentially informative.**

The racing analogy therefore strengthens PAYOFF-B only if it is used as a mechanism-separation case, not as evidence that biological systems literally behave like betting markets.

## 10. Claim boundary

Safe:

> In the declared multiplicative reduced form, biological actionability loss and competitive information diffusion enter the timing optimum through additive relative hazards. Under exponential learning and exponential decay, only the sum of those hazards determines the closed-form optimum.

Safe:

> Pari-mutuel racing supplies a prospective empirical system in which prediction accuracy and incremental value over a collective forecast can be measured repeatedly before a sharp decision deadline.

Not licensed:

> The multiplicative exclusivity factor is a universal theorem of market microstructure.

Not licensed:

> Early betting in a pari-mutuel pool captures early displayed odds.

Not licensed:

> Better horse-race prediction implies positive betting returns.

Not licensed:

> A peak in empirical predictive advantage alone identifies the mechanism as market absorption rather than model misspecification, covariate timing or selection.
