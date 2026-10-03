# PAYOFF-B mule-deer two-clock channel dissociation

Date: **2026-10-03**  
Status: **post-freeze source-data reproduction; frozen GEB V2 unchanged**

## Question

Does the same mule-deer system show functional separation between:

1. a predeparture physiological/readiness variable; and
2. signed post-departure phase correction?

The frozen analysis reuses the conservative readiness subset whose migration
began strictly after March 31, so March scaled IFBFat necessarily preceded
departure.

## Sample

The corrected Source Data parser reproduces all 152 actuator rows from the
validated Ortega workbook.

After joining March IFBFat, Days-From-Peak at migration start and actuator
summaries, the temporally safe sample contains

\[
62\ \text{animal-years from }40\ \text{deer}.
\]

Stopover duration is non-missing for 54 animal-years from 38 deer.

## Movement rate

The frozen model is

\[
speed
=
a
+
b_E\,DFP_{start}
+
b_F\,IFBFat
+
\epsilon.
\]

The continuous coefficients are

\[
b_E=+0.0742
\ \mathrm{km\,d^{-1}\ per\ phase\ day},
\]

with animal-cluster bootstrap

\[
95\%\ \mathrm{CI}=+0.0387\text{ to }+0.1028,
\]

whereas

\[
b_F=+0.322
\]

has

\[
95\%\ \mathrm{CI}=-0.049\text{ to }+0.739.
\]

After within-year residualization, the phase coefficient remains positive

\[
+0.1049
\quad
(95\%\ \mathrm{CI}=+0.0622\text{ to }+0.1441),
\]

while the IFBFat interval again includes zero.

Thus later phenological phase predicts faster subsequent movement after
accounting for March condition, whereas March condition does not have a
resolved independent speed coefficient.

## Stopover use

For stopover duration,

\[
b_E=-0.234
\ \mathrm{d\ stopover\ per\ phase\ day}
\]

with

\[
95\%\ \mathrm{CI}=-0.429\text{ to }-0.010.
\]

The IFBFat coefficient is

\[
b_F=-1.58
\]

with

\[
95\%\ \mathrm{CI}=-3.32\text{ to }+0.25.
\]

After within-year residualization,

\[
b_E=-0.357
\quad
(95\%\ \mathrm{CI}=-0.596\text{ to }-0.111),
\]

while the IFBFat interval remains unresolved.

Thus later phase predicts shorter subsequent stopover use after accounting for
March condition, whereas the condition coefficient again includes zero.

## Two-clock interpretation

The same natural population now shows a source-backed sequence:

\[
\text{March physiological condition}
\rightarrow
\text{migration-start timing}
\]

and, after migration begins,

\[
\text{signed phenological phase}
\rightarrow
\begin{cases}
\text{movement speed}\\
\text{stopover use}
\end{cases}.
\]

The downstream actuator coefficients remain aligned with signed phase after
including IFBFat, whereas IFBFat is unresolved in both actuator models.

This is consistent with **channel dissociation**:

- physiological state is associated with when migration begins;
- ecological phase error is associated with how migration is subsequently
  paced.

It strengthens the current mule-deer classification

\`\`\`text
TIMER = T3_CANDIDATE
DECISION = D2
HYBRID = H1_CANDIDATE
CHANNEL_DISSOCIATION = SUPPORTED
\`\`\`

## Why this is not H2

All speed and stopover observations used here occur **after migration has
started**. The focal readiness gate is therefore already open for all analyzed
actuator rows.

Consequently, a null or weak IFBFat coefficient in the post-departure models
cannot show that physiological readiness gates signed feedback. A valid H2
test needs observations spanning both sides of an independently measured gate,
or a readiness manipulation before the same decision opportunity.

The result therefore supports functional separation of two timing channels but
does not establish the multiplicative interaction \(G\times e\) in nature.

## Prior-art boundary

Ortega et al. already reported that nutritional condition weakly influenced
migration onset but did not influence how fast or slow deer migrated, and that
movement rate and stopover use were linked to position on the green wave.

PAYOFF-B does not claim discovery of that biology. The contribution is to place
those source-backed results inside an explicit two-clock identification
framework and to reproduce the channel separation using the temporally
conservative continuous Source Data subset.
