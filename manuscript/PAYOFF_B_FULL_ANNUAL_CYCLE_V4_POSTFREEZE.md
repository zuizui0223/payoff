# When does seasonal timing correction rescue fitness across the annual cycle?

**PAYOFF-B Paper 2 — V4 field-corrected post-freeze draft**  
**Date:** 2026-10-03  
**Status:** conceptual correction after V3 science freeze; V2/V3 provenance and registered outcomes unchanged.

## Abstract

**Aim:** Migratory animals can correct seasonal timing errors after movement has
begun, but restoring calendar timing does not necessarily restore fitness. We
ask when within-season timing correction constitutes genuine fitness rescue
rather than merely shifting costs among annual-cycle stages.

**Context:** Full-annual-cycle migration ecology and movement ecology, with
carry-over effects and life-history fitness as the demographic framework and
global-change phenology as the environmental context.

**Methods:** We represent seasonal timing as a stagewise trajectory of signed
timing error, correction actions and remaining actionability. We distinguish
phase rescue from fitness rescue by embedding correction in a full-annual-cycle
fitness accounting. Natural evidence is used as bounded mechanistic anchors,
not as a claim that all components have been identified in one system.

**Results:** A timing correction is a fitness rescue only when the gain from
reducing downstream mistiming exceeds survival, energetic and carry-over costs.
Hence identical final timing can arise from biologically different pathways.
Mule deer provide a strong example of phase rescue through signed speed and
stopover adjustment. American redstarts show costly compensation: birds delayed
by about 10 d migrated about 43% faster but had lower annual survival. Hudsonian
godwits show a contrasting regime in which large timing deviations were erased
across the annual cycle without detected reductions in breeding success or
survival. Experimental staging delays in greater snow geese demonstrate that
timing/state perturbations can instead carry over to reproductive fitness.

**Main conclusion:** Final synchrony is not sufficient evidence of climate
adaptation. Climate-tracking ability must be evaluated from the timing
trajectory together with the vital-rate consequences of the actions used to
correct it.

**Keywords:** migration ecology; full annual cycle; carry-over effects;
phenology; movement ecology; fitness; climate change; timing

---

## 1. Introduction

Phenology is usually measured as a date: departure, arrival, flowering, laying
or emergence. For migratory animals, however, such dates are endpoints of a
sequence. An individual can depart early and wait later, depart late and
accelerate, skip a stopover, lengthen a stopover, alter route or delay
reproduction after arrival. The same final date can therefore arise from very
different annual-cycle trajectories.

This distinction is already central to migration ecology. Migrants use local
and internal cues to make decisions whose outcomes are realized in different
places and later times. Strategy, action and outcome are not equivalent, and
stopovers can provide information as well as fuel and safety. Carry-over
effects further show that the cost of one annual-cycle stage can appear in the
survival or reproductive performance of a later stage.

Recent empirical work makes the problem concrete. Migrating mule deer can begin
far ahead of or behind peak green-up and resynchronize en route by changing
movement rate and stopover use. American redstarts delayed at departure migrate
faster, but this compensation is associated with lower annual survival.
Hudsonian godwits can erase large timing deviations over the annual cycle
without detectable reductions in breeding success or survival. Experimental
delay or stress during spring staging in greater snow geese can instead reduce
later reproduction or survival.

These systems imply that two different questions are often conflated.

First:

> **Did the organism recover its seasonal timing?**

Second:

> **Did the organism recover its fitness?**

The first is a question about phase or calendar timing. The second is a
life-history question involving survival, reproduction and future reproductive
value.

This distinction matters for global change. An animal can look perfectly
synchronized at arrival after paying a substantial survival cost to get there.
Conversely, a large temporary timing deviation can be biologically unimportant
if a later stage absorbs it without a vital-rate penalty. Final timing alone is
therefore an incomplete measure of climate vulnerability.

The central question of PAYOFF-B V4 is:

> **When does correcting a seasonal timing error actually rescue fitness across
> the annual cycle?**

The aim is not to claim that en-route compensation, cue updating or carry-over
effects are new. Those are established parts of migration ecology. The
contribution is to keep timing-state recovery and full-annual-cycle fitness
recovery as separate estimands and to make explicit what must be measured to
distinguish successful adaptation from costly compensation.

---

## 2. A stagewise timing and fitness framework

### 2.1 Timing error is a state that can change across stages

Let

[
e_t
]

be signed seasonal timing error at stage (t), measured relative to the
ecologically relevant target at that stage.

Positive error means late; negative error means early.

A correction action (u_t) can change the error:

[
e_{t+1}
=
phi_t(e_t-u_t)+w_t,
]

where (phi_t) is passive retention and (w_t) is movement of the ecological
target between stages.

This equation is not intended as a new movement theory. It is bookkeeping for
a familiar ecological fact: a delay at one stage may persist, disappear or
change sign at the next.

A proportional reduced representation gives

[
e_{t+1}=lambda_t e_t+w_t.
]

Thus (lambda_t) is a descriptive coordinate for how much timing error
persists through a stage. It is not by itself a physiological mechanism or a
measure of behavioral flexibility.

### 2.2 Correction depends on information and remaining opportunity

As migration proceeds, information about future conditions can improve while
opportunities to change the trajectory disappear.

Let (q(t)) describe information quality and (r(t)) retained actionability.
A reduced value of information is

[
N(t)=r(t)[Sq(t)-B]-C(t).
]

The exact form is secondary here. The ecological point is that better
information received later is useful only if a meaningful response is still
possible.

At the actuator level, write effective correction as

[
h_t=O_tg_t,
]

where (O_t) is the remaining opportunity to use a particular actuator and
(g_t) is the enacted correction gain.

This distinction prevents a common error: poor final tracking can reflect poor
information, little remaining opportunity, weak action, or some combination.

### 2.3 Phase rescue is not fitness rescue

Suppose correction (u) changes the residual phase error from (e_{in}) to
(e_{out}).

For a simple one-cycle representation, let

[
W(u)=S(u)R(e_{out}),
]

where (S(u)) is survival through the correction or migration stage and
(R(e_{out})) is subsequent reproductive output or reproductive value given
the residual timing error.

Correction is a **fitness rescue** only if

[
oxed{
W(u)>W(0).
}
]

Equivalently,

[
oxed{
Deltalog S+Deltalog R>0.
}
]

This is standard life-history accounting rather than a new theorem. Its role is
to prevent calendar recovery from being mistaken for adaptation.

For long-lived organisms or multi-stage annual cycles, (R) is replaced by
the appropriate continuation reproductive value. More generally,

[
V_t(s_t)
=
max_{u_t}
Eleft[
f_t(s_t,u_t)+V_{t+1}(s_{t+1})
ight],
]

where the state includes timing, condition and relevant environmental
information.

The current PAYOFF-B quadratic loss,

[
L(u)=kappa u^2+mu(e-u)^2,
]

can therefore be understood as a reduced approximation: the first term
summarizes fitness costs of correction and the second summarizes fitness loss
from residual mistiming. Neither term is a natural fitness parameter until
linked to vital rates.

### 2.4 Three biologically different outcomes can share similar final timing

A corrected timing trajectory can end in at least three regimes.

**Phase rescue with fitness rescue:** timing error is removed and no detectable
vital-rate debt remains.

**Phase rescue with fitness debt:** timing error is removed, but survival,
condition or later reproduction is reduced by the correction.

**No phase rescue:** timing error persists and carries into a fitness-relevant
stage.

These regimes cannot be distinguished from final arrival or breeding date
alone.

### 2.5 Interaction mismatch is a downstream extension

For interacting actors, timing correction can also alter relative synchrony.
If two actors enter with mean error (m_0) and initial difference
(Delta_0), and have stage-retention coefficients (lambda_1,lambda_2),

[
Delta_n
=
(lambda_1^n-lambda_2^n)m_0
+
rac{lambda_1^n+lambda_2^n}{2}Delta_0.
]

The identity remains useful, but it is not the main V4 novelty claim. It simply
shows that different correction trajectories can create or erase interaction
mismatch after the initial response.

The fitness interpretation is actor- and interaction-specific: reducing one's
own environmental timing error can still alter synchrony with a partner, and
partner mismatch may feed back into (R(e)).

---

## 3. Natural evidence spans distinct fitness regimes

### 3.1 Mule deer: strong phase rescue, unresolved fitness rescue

Ortega et al. showed that Red Desert mule deer can begin migration far ahead of
or behind peak green-up and adjust movement speed and stopover use in the
direction expected to reduce that phase error.

The PAYOFF-B source-data reanalysis quantifies this funnel in 152 animal-years
from 72 adult females. Signed phase SD declined from 26.41 d at migration start
to 13.17 d at migration end; the end/start variance ratio was 0.249 and 0.294
after year centering. Mean absolute phase error declined from 21.91 d to
11.12 d.

Positive starting phase error was associated with faster movement and less
stopover use, with signs retained after year centering.

This is strong evidence for **phase rescue**.

It does not establish **fitness rescue** because the same analysis does not
measure whether the corrected trajectories improved survival, reproductive
success or lifetime reproductive value relative to the relevant uncorrected
counterfactual.

### 3.2 American redstarts: compensation with survival cost

Dossman et al. studied American redstarts that differed in relative spring
departure timing.

A roughly 10-d departure delay was associated with approximately 43% faster
migration. Delayed birds also had an estimated 6.3% decrease in apparent annual
survival.

Thus,

[
	ext{timing compensation}

eq
	ext{zero fitness cost}.
]

This system is particularly important because it shows that a correction that
looks adaptive in calendar time can move the cost into a different fitness
component.

However, the study does not estimate a complete net-fitness contrast in which
the recovered reproductive benefit and survival cost are jointly observed as a
single lifetime-fitness outcome for the same tracked individuals. It therefore
demonstrates fitness debt, not the sign of total lifetime fitness rescue.

### 3.3 Hudsonian godwits: timing deviations can disappear without detectable fitness debt

Senner et al. followed Hudsonian godwits across the annual cycle.

Individuals could become substantially early or late relative to population
timing, yet large deviations were erased at later stages. Arrival at the
nonbreeding site varied much more than subsequent departure, and individuals
late at one point did not necessarily remain late at breeding arrival.

Crucially, accumulated timing deviation and arrival timing were not associated
with detected reductions in breeding success or survival.

This system provides the contrasting case: large temporary timing deviations
can be absorbed without an observable fitness penalty.

It therefore warns against treating temporary calendar mismatch itself as
fitness loss.

### 3.4 Greater snow geese: annual-cycle perturbations can carry directly into fitness

Experimental manipulation of greater snow geese during spring staging provides
a different regime.

In a large field experiment, captivity duration during staging reduced later
reproductive success strongly in two of three years, with the effect partly
buffered under favorable breeding conditions.

More recent experimental/mark-recapture work in the same broader system shows
that migration-stage stress and food deprivation can also carry into survival.

These results demonstrate that apparently short perturbations at migration
stages can have downstream vital-rate consequences and that the magnitude of
fitness debt depends on later environmental conditions.

### 3.5 The empirical lesson

Together these systems do not support one universal rule such as "flexibility
is good" or "compensation is costly."

They show a biologically meaningful contrast:

[
oxed{
	ext{timing deviation}
ightarrow
	ext{correction}
ightarrow
	ext{timing outcome}
ightarrow
	ext{vital-rate outcome}
}
]

can terminate differently among systems.

The next comparative question is therefore not simply which species shifts its
date fastest, but which species can absorb timing error without paying a
survival or reproductive debt.

---

## 4. Position within ecology

### 4.1 Full-annual-cycle migration ecology is the primary field

Movement ecology already treats migration as a sequence of decisions
conditioned by environmental information, internal state, navigation and motion
capacity.

Full-annual-cycle ecology adds the key consequence: events and costs in one
stage can alter performance in later stages.

PAYOFF-B V4 sits at their intersection.

Its main variables should therefore be interpreted as annual-cycle states and
vital-rate consequences, not as abstract control parameters detached from
organismal biology.

### 4.2 Global-change phenology is the environmental problem, not the primary method

Climate change alters the seasonal targets migrants are trying to track and can
change the reliability of cues across space.

Phenological mismatch research asks whether timing changes alter ecological
overlap and fitness. Reviews repeatedly emphasize that direct links from timing
to fitness and demography are much rarer than date-based evidence.

PAYOFF-B contributes by asking what happens between the initial timing error and
the eventual fitness endpoint.

### 4.3 Carry-over effects supply the fitness logic

The carry-over literature is directly concerned with whether events at one
stage leave effects on survival or reproduction at subsequent stages.

This is the correct language for correction costs.

A correction that improves arrival timing but reduces survival is not an
anomaly to be patched into a timing model; it is a carry-over trade-off.

### 4.4 Why ecologists care

This question matters for at least three reasons.

First, **mechanism**: final phenology does not tell us how an organism achieved
that date.

Second, **conservation**: stopover loss, habitat degradation or extreme events
may remove the stages at which timing errors can normally be absorbed.

Third, **prediction**: climate vulnerability depends not only on initial timing
plasticity, but on whether later correction is possible and whether correction
costs fall on survival or reproduction.

Recent global work also shows that the demographic association of migration
timing shifts is stage dependent, reinforcing the need for full-annual-cycle
rather than single-date interpretation.

---

## 5. What is and is not new

PAYOFF-B does **not** claim novelty for:

- remote environmental cues;
- stopovers as information sources;
- en-route timing compensation;
- carry-over effects;
- timing–fitness trade-offs;
- survival costs of accelerated migration;
- stage-specific phenological flexibility;
- the general idea that climate change can create mismatch.

The defensible contribution is narrower:

> **PAYOFF-B separates timing-state rescue from full-annual-cycle fitness rescue
> in one stagewise framework and makes explicit the data required to distinguish
> successful adaptation, costly compensation and unresolved fitness debt.**

This is an identification and synthesis contribution.

The pairwise interaction-mismatch decomposition remains a secondary theoretical
extension, not the ecological headline.

If a stronger empirical claim is desired, it requires a system in which the
same individuals provide incoming timing error, correction behavior, outgoing
timing error, survival and subsequent reproduction.

---

## 6. Direct empirical test

The decisive natural design is

[
e_{in}
ightarrow
u
ightarrow
e_{out}
ightarrow
S
ightarrow
R.
]

The same individuals must provide:

1. signed incoming timing error;
2. correction behavior;
3. outgoing timing error;
4. survival through or after correction;
5. subsequent reproductive performance;
6. physiological state / individual quality;
7. environmental conditions at the relevant stages.

Individual quality is essential because high-quality animals can both correct
more effectively and achieve higher fitness, creating an apparent compensation
benefit even when correction itself is not causal.

An experimental perturbation of timing or state, combined with biologging and
subsequent vital-rate monitoring, is the strongest design.

---

## 7. Conclusion

A migrant that arrives on time has not necessarily solved its seasonal
problem. It may have predicted conditions accurately, corrected an earlier
mistake at negligible cost, or paid a survival or reproductive debt to recover
the calendar.

Conversely, a large temporary timing deviation need not be biologically
important if later annual-cycle stages erase it without a vital-rate penalty.

The relevant question is therefore not simply

> **Did the organism catch up?**

but

> **Did catching up improve full-annual-cycle fitness?**

That distinction places seasonal timing inside the life history of the organism
rather than treating phenology as a sequence of isolated dates.

For global-change ecology, the consequence is practical: vulnerability cannot
be inferred from initial timing error or final synchrony alone. It depends on
where correction remains possible, what actions are used, and which vital rates
pay for those actions.

---

## Provenance note

V4 is a conceptual field correction made after the V3 science freeze. It does
not alter or reopen any preregistered empirical outcome. V2 and V3 remain
auditable provenance states. V4 changes the ecological positioning and fitness
bookkeeping because literature review showed that several claims previously
treated as candidate novelty are established migration-ecology prior art.
