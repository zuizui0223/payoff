# PAYOFF-B stage-handoff retention identity

Date: **2026-10-03**  
Status: **post-freeze descriptive bridge; frozen GEB V2 unchanged**

## 1. General serial timing identity

Let an upstream seasonal event occur at time

\[
T_0
\]

and a downstream event occur after interval

\[
W.
\]

By definition,

\[
T_1=T_0+W.
\]

For simple OLS with an intercept on the same observations,

\[
\beta_{T_1\sim T_0}
=
\frac{\operatorname{Cov}(T_1,T_0)}
{\operatorname{Var}(T_0)}
=
1+
\frac{\operatorname{Cov}(W,T_0)}
{\operatorname{Var}(T_0)}.
\]

Therefore

\[
\boxed{
\eta
=
1+\beta_{W\sim T_0}
}
\]

where

\[
\eta
=
\beta_{T_1\sim T_0}
\]

is **stage-to-stage timing retention**.

Define descriptive compensation fraction

\[
\boxed{
c
=
-\beta_{W\sim T_0}
=
1-\eta.
}
\]

## 2. Regimes

- \(\eta=1\): upstream timing variation passes downstream unchanged;
- \(0<\eta<1\): partial buffering;
- \(\eta=0\): complete buffering;
- \(\eta<0\): overcompensation / sign reversal;
- \(\eta>1\): downstream amplification.

This identity is descriptive.  It does **not** establish that shortening the
inter-event interval was a strategic or information-dependent decision.

## 3. Greater snow goose anchor

Bêty, Gauthier & Giroux (2003), *American Naturalist* 162:110–121,
DOI 10.1086/375680, tracked radio-marked greater snow goose females from the
spring staging area to Bylot Island.

Their Figure 5 reports the simple regression

\[
\text{prelaying duration}
=
0.099
-
0.53
\times
\text{arrival date},
\]

with \(R^2=0.55\) and \(P<0.001\).

Because

\[
\text{lay date}
=
\text{arrival date}
+
\text{prelaying duration},
\]

the exact same-sample simple-regression handoff implied by Figure 5 is

\[
\boxed{
\eta_{arrival\to lay}
=
1-0.53
=
0.47.
}
\]

Thus one day of later arrival is descriptively associated with only about
0.47 d of later laying in that simple stage-handoff representation: roughly
53% of upstream timing variation is absorbed by a shorter prelaying interval.

Table 2 of the source gives a separate multiple model for lay date controlling
premigration body condition:

\[
\hat\beta_{arrival}=0.45\pm0.09,
\qquad
P<0.001,
\]

and

\[
\hat\beta_{condition}=-1.18\pm0.56,
\qquad
P=0.04.
\]

The 0.45 multiple-model slope is close to, but not the same estimand as, the
0.47 simple handoff identity because the source models differ in covariates.

## 4. Why this is useful for the serial-clock model

The snow-goose result supplies a second ecological form of serial buffering:

\[
\text{arrival phase}
\rightarrow
\text{prelaying interval}
\rightarrow
\text{lay date}.
\]

It is not a route-wise Mikawa-Anjo controller.  The post-arrival stage includes
condition gain and reproductive optimization.  Its value is more general:

> **a timing error entering one life-history stage need not be transmitted
> one-for-one into the next stage.**

Thus the serial-clock concept applies beyond migration speed and stopover.

## 5. Causal boundary

Schroeder, Mitesser & Hinsch (2010) explicitly cautioned that correlations
among sequential timing decisions can arise mathematically and do not by
themselves prove strategic behavior.

Accordingly, PAYOFF-B may use

\[
\eta=0.47
\]

as a **descriptive stage-retention anchor**, but not as evidence that geese
actively estimated phase error and intentionally shortened prelaying by 0.53 d
per day of later arrival.

The source's independent condition effect and its unplanned condition
manipulation support physiological state dependence of lay timing, but they do
not convert the interval correlation into a route-feedback estimate.

## 6. Flycatcher experimental handoff anchor

Samplonius & Both (2017), *Journal of Animal Ecology*,
DOI 10.1111/1365-2656.12640, manipulated resident tit hatching phenology.

The manipulation did not detectably alter pied-flycatcher arrival timing.
Almost all males settled before manipulated tit hatching became observable and
male settlement showed no detectable treatment response, whereas later female
settlement did respond to the treatment.

This gives a different type of serial evidence:

\[
\text{early stage before cue visibility}
\rightarrow
\text{little/no treatment response},
\]

followed by

\[
\text{later decision after cue visibility}
\rightarrow
\text{treatment response}.
\]

The experiment therefore anchors the idea that information can become relevant
only at later stages, without identifying a developmental readiness clock.

## 7. Cross-system synthesis

Three natural systems now illustrate different serial handoffs.

### Mule deer

\[
\text{predeparture condition}
\rightarrow
\text{migration entry}
\rightarrow
\text{signed route correction}.
\]

### Greater snow goose

\[
\text{arrival}
\rightarrow
\text{condition-dependent prelaying}
\rightarrow
\text{lay date}.
\]

### Pied flycatcher

\[
\text{arrival / early settlement before cue visibility}
\rightarrow
\text{later settlement after cue visibility}.
\]

These are not three replications of the same controller parameter.

They support the broader ecological principle:

> **seasonal timing is staged; different mechanisms can govern successive
> transitions, and downstream stages can buffer or transform upstream timing
> error.**

## 8. Claim ceiling

Licensed:
- stage-to-stage timing retention can be quantified;
- Bêty 2003 implies a descriptive arrival-to-lay simple handoff retention of
  0.47;
- flycatcher manipulation shows stage-specific cue relevance;
- these patterns broaden the serial-clock concept beyond mule-deer migration.

Not licensed:
- Bêty's 0.47 is an active feedback gain;
- flycatcher arrival is a developmental readiness clock;
- all sequential timing correlations imply strategic control;
- the serial two-clock theorem is prospectively validated by either source.
