# Phase–velocity decomposition of temporal buffering

Frozen as a **post-readout mechanistic interpretation** on 2026-09-25.

This note does not retroactively redefine the registered bird holdout test and
is **not a preregistered prediction**. It explains why the failed
temporal-substitution prediction is structurally plausible in a moving
environmental wave.

## 1. Minimal moving-front identity with a dynamic timing shift

Let the environmental front move as

\[
E(t)=E_0+v_E t,
\]

and represent the organism's baseline spatial front by speed \(v_A\). Let
\(z(t)\) be a schedule displacement, measured in units of time, relative to
that baseline trajectory:

\[
A(t)=A_0+v_A[t+z(t)].
\]

Then

\[
e(t)=E(t)-A(t)
=(E_0-A_0)+(v_E-v_A)t-v_A z(t).
\]

A **static** timing shift changes phase,

\[
\frac{\partial e}{\partial z}=-v_A.
\]

But when timing itself keeps changing,

\[
\frac{de}{dt}=v_E-v_A-v_A\dot z(t).
\]

Thus dynamic timing adjustment can contribute a temporary effective velocity
correction. To hold mismatch constant despite \(v_E\neq v_A\), timing would
have to change at

\[
\dot z^*
=
\frac{v_E-v_A}{v_A}
=
\frac{1-u}{u},
\]

where \(u=v_A/v_E\).

This is elementary kinematics, not a claim of mathematical novelty. It resolves
the apparent tension between the local substitution null and the explicit
landscape: timing can transiently compensate velocity mismatch, but doing so
requires continually spending temporal displacement.

## 2. Capacity turns time warping into a finite buffer

If schedule displacement is bounded,

\[
|z(t)|\le z_{\max},
\]

a non-zero compensating \(\dot z^*\) cannot be sustained indefinitely. Starting
from the center of the available timing range, the longest idealized interval
of perfect compensation is

\[
T_{\rm buffer}
=
\frac{z_{\max}}{|\dot z^*|}
=
\frac{v_A z_{\max}}{|v_E-v_A|}
=
\frac{u z_{\max}}{|1-u|}.
\]

Hence:

- **timing gain** controls how strongly schedule displacement responds;
- **timing capacity** \(z_{\max}\) controls how long that response can continue;
- **movement speed** determines the baseline spatial propagation rate;
- sustained speed mismatch consumes the timing budget until movement or another
  spatial actuator must take over.

The explicit-landscape result is therefore not merely “phase versus velocity.”
It is **bounded time warping**: phenology can generate a temporary effective
velocity correction, but finite capacity forces spatial tracking to re-enter.

## 3. Why the bird holdout substitution prediction failed

The registered bird holdout treated species timing responsiveness as a possible
substitute for movement-speed matching.

The result was

\[
\beta_{q^2\times h}=+0.0351\pm0.0289,\qquad p=0.225,
\]

opposite to the registered negative prediction. The secondary descriptive
timing-responsiveness main effect was

\[
\beta_h=-0.300\pm0.105,\qquad p=0.0043.
\]

The failed substitution test exposes a distinction the registration
deliberately did not make: **responsiveness is not capacity**.

The calibration slope is gain-like: it measures how strongly arrival timing
moves with green-up. It does not measure the remaining timing range
\(z_{\max}\), nor the amount of temporal budget left unused. High timing gain can
therefore lower average phase error without implying that a species can sustain
a compensating \(\dot z(t)\) for longer.

\[
\text{timing gain}
\rightarrow
\text{current phase correction},
\]

\[
\text{timing capacity}
\rightarrow
\text{duration of temporal buffering},
\]

\[
\text{movement speed}
\rightarrow
\text{baseline spatial propagation}.
\]

Therefore

\[
\text{better timing responsiveness}
\not\Rightarrow
\text{weaker speed dependence}.
\]

This gain–capacity distinction is the main mechanistic lesson of the failed
holdout test.

## 4. Independent consistency with the Amaral source analysis

The original Amaral et al. analysis independently treated bird migration speed
as environmentally responsive.

Its published Table 1 reports:

\[
\beta_{\rm greenup\ date}=-0.549
\quad
(95\%\,{\rm CI}=-0.770,-0.327),
\]

and

\[
\beta_{\rm greenup\ speed}=+0.088
\quad
(95\%\,{\rm CI}=+0.041,+0.134)
\]

for bird migration speed.

Its species-sensitivity term in the migration-speed model was

\[
\beta_{\rm sensitivity}=+0.119
\quad
(95\%\,{\rm CI}=-0.034,+0.203).
\]

The last estimate is uncertain, but importantly it is not a negative association
supporting a simple timing-for-speed tradeoff.

This is not a new PAYOFF confirmatory result. It is prior-source consistency:
the source study itself does not suggest that greater phenological sensitivity
removes movement-speed adjustment.

## 5. Revised ecological architecture

The useful hierarchy is therefore:

\`\`\`text
environmental forcing
    |
    +-- timing gain
    |       -> how strongly phase is corrected now
    |
    +-- timing capacity / temporal budget
    |       -> how long dynamic timing can offset propagation mismatch
    |
    +-- movement speed / route progression
            -> baseline spatial propagation
\`\`\`

Stopover and route-stage changes can redistribute both schedule and effective
progression locally.

This predicts that a species can be highly phenologically responsive, maintain
low current mismatch, and still remain strongly dependent on spatial transport
because high gain does not imply large remaining capacity.

## 6. Claim boundary

Licensed:

- a static timing shift changes phase, while changing timing through time can
  transiently alter effective mismatch drift;
- bounded timing capacity converts that dynamic correction into a finite buffer;
- timing responsiveness (gain) is not the same quantity as remaining timing
  capacity;
- the failed bird holdout substitution test is consistent with this
  gain–capacity–propagation decomposition;
- timing responsiveness may improve average tracking without eliminating
  movement-speed dependence.

Not licensed:

- claiming that the post-readout identity was a preregistered prediction;
- claiming empirical support for a positive timing × movement synergy from the
  unsupported positive interaction;
- treating \(T_{\rm buffer}\), timing capacity, or remaining temporal budget as
  empirically estimated natural quantities in the current bird dataset;
- claiming all natural migration systems follow exactly this linear-front
  time-warp model.

## 6. Claim boundary

Licensed:

- timing and speed are structurally non-equivalent in the minimal moving-front
  representation because they alter intercept and drift respectively;
- bounded timing can buy a finite amount of time under non-zero speed mismatch;
- the failed bird holdout substitution test is consistent with this
  phase–velocity division of labor;
- timing responsiveness may improve average tracking without eliminating
  movement-speed dependence.

Not licensed:

- claiming that the post-readout identity was a preregistered prediction;
- claiming empirical support for a positive timing × movement synergy from the
  unsupported positive interaction;
- treating \(T_{\rm buffer}\) as an empirically estimated natural value in the
  current bird dataset;
- claiming all natural migration systems follow exactly this linear-front model.
