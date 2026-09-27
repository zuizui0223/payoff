# PAYOFF-B information-deadline theorem

Date: **2026-09-27**  
Status: **exact result for the declared symmetric binary-cue decision model**

## Setup

Let the future seasonal state be normal or early, with

[
P(early)=\pi.
]

An actor can commit to a late or early seasonal action.

Define:

[
A=(1-\pi)C_F
]

as the prior expected loss of committing early, where (C_F) is the
false-early loss, and

[
L=\pi C_M
]

as the prior expected loss of committing late, where (C_M) is the
missed-early loss.

Let

[
S=A+L.
]

Before observing a cue, the Bayes-optimal action has risk

[
R_0=\min(A,L).
]

A later symmetric binary cue has state-classification accuracy (q\ge 1/2).
Waiting for that cue costs (D\ge0).

Ties are resolved in favour of immediate commitment, matching the implemented
PAYOFF-B decision rule.

---

## Proposition 1 — actionable-information threshold

The cue cannot change the Bayes-optimal action until

[
oxed{
q>q_0=\frac{\max(A,L)}{A+L}
}
]

and the value of waiting is exactly

[
oxed{
V(q)=
\max\left[
0,;
q(A+L)-\max(A,L)
\right].
}
]

### Proof sketch

Suppose the prior-optimal action is late, so (L\le A).

When the cue says early, the unnormalised expected losses are

[
(1-\pi)(1-q)C_F=A(1-q)
]

for switching early and

[
\pi q C_M=Lq
]

for remaining late.

The early action is preferred exactly when

[
A(1-q)<Lq
]

or

[
q>\frac{A}{A+L}.
]

When the cue says late, the prior late action remains optimal for every
(q\ge1/2). Therefore below the threshold both cue outcomes produce the same
action and information has zero behavioural value.

Above the threshold the actor follows the informative cue outcome. Errors occur
only when the cue is wrong, giving post-cue risk

[
(1-q)(A+L).
]

Subtracting this from prior risk (L) gives

[
V(q)=q(A+L)-A.
]

The prior-early case is symmetric and replaces (A) by (L), yielding the
unified expression above.

---

## Proposition 2 — exact waiting threshold

An actor waits for the future cue iff

[
V(q)>D.
]

If

[
D<R_0,
]

the exact cue-accuracy threshold is

[
oxed{
q_{wait}(D)
=
\frac{\max(A,L)+D}{A+L}.
}
]

The actor waits only for

[
q>q_{wait}(D).
]

If instead

[
oxed{D\ge R_0},
]

then even perfect information has insufficient value and the actor never waits:

[
q_{wait}=\varnothing.
]

This gives a formal ecological meaning to a hard decision deadline: the
opportunity cost of delay exceeds the maximum possible gain from learning the
true seasonal state.

---

## Theorem — information-induced desynchronization

Consider two otherwise identical interacting actors that will observe the same
future cue but have unequal waiting costs

[
D_1<D_2.
]

### Case I — both eventually wait

If

[
D_1<D_2<R_0,
]

then

[
q_1
=
\frac{\max(A,L)+D_1}{S}
]

and

[
q_2
=
\frac{\max(A,L)+D_2}{S},
]

with (q_1<q_2).

The system has three exact regimes:

[
q\le q_1:
\quad
commit\mid commit,
]

[
q_1<q\le q_2:
\quad
wait\mid commit,
]

[
q>q_2:
\quad
wait\mid wait.
]

Because the same cue is used by both actors, expected action mismatch is zero
in the first and third regimes but positive in the intermediate regime.

Hence a monotonic increase in cue reliability creates:

[
oxed{
shared\ ignorance
\rightarrow
asymmetric\ information\ use
\rightarrow
shared\ informed\ coordination.
}
]

The exact width of the desynchronization window is

[
oxed{
\Delta q
=
q_2-q_1
=
\frac{D_2-D_1}{A+L}.
}
]

This is the closed-form version of the previously simulated (q=0.82-0.93)
window.

### Case II — one actor never waits

If

[
D_1<R_0\le D_2,
]

then actor 1 eventually uses the cue but actor 2 never does.

The system enters an asymmetric-information regime at

[
q>q_1
]

and **does not re-synchronise even at (q=1)**.

Thus sufficiently different decision deadlines can make information asymmetry
persistent despite perfect cue reliability.

### Case III — neither waits

If

[
R_0\le D_1<D_2,
]

neither actor ever waits and cue improvement has no behavioural effect.

### Case IV — equal waiting costs

If

[
D_1=D_2,
]

the two actors cross their information-use threshold simultaneously and there
is no asynchronous-uptake window.

---

## Mismatch probability inside the asynchronous window

If the prior-optimal action is late, the committed actor remains late while the
waiting actor switches early when the cue says early. Therefore

[
M(q)
=
P(signal=early)
=
\pi q+(1-\pi)(1-q).
]

If the prior-optimal action is early,

[
M(q)
=
P(signal=late)
=
(1-\pi)q+\pi(1-q).
]

The overall mismatch curve is therefore exactly zero outside the asynchronous
uptake regime and positive inside it.

The curve can rise or fall within the window depending on (\pi), but the
system response is necessarily non-monotone whenever both actors eventually
wait and their delay costs differ.

---

## Canonical PAYOFF-B witness

For

[
\pi=0.4,\quad C_F=2,\quad C_M=1,
]

we have

[
A=1.2,\quad L=0.4,\quad S=1.6,
]

so

[
q_0=0.75
]

and

[
R_0=0.4.
]

With waiting costs

[
D_{low}=0.10,\quad D_{high}=0.30,
]

the exact thresholds are

[
q_{low}=0.8125
]

and

[
q_{high}=0.9375.
]

Therefore

[
\Delta q=0.125.
]

On the previously declared 0.01 grid this appears as

[
q=0.82-0.93.
]

At the first sampled asynchronous point,

[
M(0.82)
=
0.4(0.82)+0.6(0.18)
=
0.436,
]

exactly matching the numerical phase sweep.

---

## Comparative predictions

The theorem produces several direct predictions.

### 1. Deadline heterogeneity widens the mismatch window

For fixed state losses,

[
\frac{\partial \Delta q}
{\partial(D_2-D_1)}
=
\frac{1}{A+L}>0.
]

Species, sexes or guilds with more unequal opportunity costs of waiting should
remain asynchronously informed across a broader range of cue qualities.

### 2. Higher consequences of wrong timing can narrow asynchronous uptake

For a fixed absolute difference in waiting costs,

[
\Delta q
=
\frac{D_2-D_1}{A+L}.
]

Increasing the total expected penalty of a wrong seasonal action makes cue
quality valuable more quickly to both actors and compresses the interval
between their waiting thresholds.

This does **not** mean ecological costs are beneficial overall. It is a specific
prediction about synchrony of information uptake.

### 3. Hard deadlines prevent recovery

If one actor has

[
D\ge R_0,
]

then improving the cue all the way to perfect accuracy cannot induce that actor
to wait. Better environmental information alone cannot restore coordination.

### 4. Cue quality and cue use are different state variables

Two systems with the same cue reliability (q) can occupy different
information architectures because their waiting costs differ.

Therefore ecological models should distinguish:

[
information\ quality
\neq
information\ uptake.
]

---

## Information-acquisition coordination wedge

When a timing error also imposes losses on interaction partners, define the
private and joint values of waiting as

[
V_P(q)
]

and

[
V_J(q).
]

Whenever

[
V_J(q)>V_P(q),
]

there is an exact delay-cost interval

[
oxed{
D\in[V_P(q),V_J(q))
}
]

in which the individual rationally commits now but joint payoff would be larger
if it waited.

Thus coordination failure can arise **before** species choose their seasonal
actions: interacting organisms can under-invest in information acquisition
itself.

---

## Relation to existing literature

PAYOFF-B does not claim novelty for costly information acquisition, migration
under uncertain environmental cues, or climate-driven cue--driver
decoupling. Those ideas are established.

The specific contribution of this theorem is the ecological consequence of
**heterogeneous decision deadlines under a shared cue**:

> Monotonically improving environmental information can create a finite window
> of increased phenological mismatch because interacting organisms begin using
> the same information at different reliability thresholds.

The network model then supplies the next layer: a transient
information-induced desynchronization can be stored as a strict lower-payoff
timing regime after the original information asymmetry disappears.
