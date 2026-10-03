# PAYOFF-B V5 — buffer-limits novelty screen

Date: 2026-10-03  
Status: **prospective field-position screen; no V5 comparative outcome opened**

## 1. Field

Primary field:

- full-annual-cycle migration ecology;
- movement ecology;
- carry-over effects / seasonal interactions;
- global-change phenology as the environmental context.

The focal biological problem is **temporal buffering**: when a delay or advance
created at one annual-cycle stage is transmitted to the next stage, versus
absorbed before it reaches a fitness-relevant event.

## 2. Prior art that closes earlier PAYOFF-B novelty claims

The following are established and are not V5 novelty.

### En-route and annual-cycle schedule adjustment

Senner et al. (2014) followed Hudsonian godwits across complete annual cycles
and explicitly asked when timing deviations arise and disappear. They modelled
the rate of change of timing deviations between sequential annual-cycle stages
and linked them to breeding success and survival.

Carneiro et al. (2023) followed Icelandic whimbrels across seven years and
showed that stationary periods, especially wintering, can absorb earlier delays;
other transitions show domino effects.

Tree swallow and other full-annual-cycle studies show that seasonal timing
relationships can persist through several stages and then reset during long
stationary periods.

### Buffering as a recognized ecological concept

Weir & Phillimore (2024) define phenological buffering broadly and distinguish
mechanisms that:
1. reduce asynchrony;
2. reduce the fitness cost of asynchrony;
3. reduce aggregate interannual variance.

They explicitly argue that research should identify **the limits of buffers**.

### Annual-cycle timing synthesis already exists

Franklin et al. (2022) meta-analysed individual repeatability of migration
timing across 54 papers, 47 species and 177 effect sizes. This addresses
between-year consistency of the same annual event.

Wang et al. (2024) compiled tracking data from 186 bird species and used
phylogenetic SEMs to analyse timing of four major annual-cycle events and broad
carry-over paths.

These studies mean that V5 cannot claim novelty for:
- annual-cycle integration;
- carry-over effects;
- reset points existing;
- repeatability varying among stages;
- departure affecting arrival;
- stationary periods acting as buffers;
- the concept of a buffer limit.

## 3. Gap retained after the screen

The targeted searches did not identify a comparative synthesis whose primary
estimand is the **day-for-day transmission of a timing perturbation between
successive annual-cycle events**.

The distinction is:

- repeatability asks whether the same individual tends to be early/late in the
  same event across years;
- mean timing datasets ask when species/populations perform events;
- transition propagation asks how many days of an earlier timing deviation
  remain one stage later.

The V5 question is therefore:

> **Where in the annual cycle do migratory birds absorb temporal delays, and
> what predicts when those delays persist to fitness-relevant stages?**

This is a direct quantitative response to the existing field call to identify
the limits of phenological buffering.

## 4. Primary comparative estimand

For sequential annual-cycle events A and B measured in the same time units,
define the raw propagation slope

\[
d_{B}=a+\beta_{AB}d_{A}+\varepsilon ,
\]

where \(d_A\) and \(d_B\) are date deviations from the appropriate year /
population reference when such centering is available.

Interpretation:

- \(\beta_{AB}=1\): a one-day deviation is transmitted one-for-one;
- \(0<\beta_{AB}<1\): partial temporal buffering;
- \(\beta_{AB}=0\): complete statistical reset at that transition;
- \(\beta_{AB}<0\): over-correction / reversal;
- \(\beta_{AB}>1\): amplification.

V5 will call \(\beta_{AB}\) the **timing-propagation coefficient**.

This is a descriptive transition coordinate, not a direct physiological
parameter or control gain.

The display quantity

\[
B_{AB}=1-\beta_{AB}
\]

may be used as "buffering fraction" only when \(0\le\beta_{AB}\le1\).
Values outside this interval will be shown without clipping and interpreted as
reversal or amplification.

## 5. Why raw propagation is preferable to correlation

Correlation and repeatability depend strongly on variance among individuals and
measurement error. A high correlation does not imply one-for-one delay
propagation.

Primary V5 synthesis therefore requires an unstandardized slope in common time
units, or individual-level data from which one can be estimated.

Standardized correlations are retained only in a separate secondary synthesis
and will never be converted into \(\beta_{AB}\).

## 6. Predeclared transition classes

Each effect is assigned before outcome modelling to one of:

1. active spring migration;
2. spring stopover / staging;
3. non-breeding stationary period;
4. arrival-to-breeding / pre-laying period;
5. breeding / post-breeding interval;
6. active autumn migration;
7. autumn stopover / staging;
8. other stationary annual-cycle interval.

Where an interval contains multiple biological processes and cannot be assigned
without ambiguity, it is coded MIXED and excluded from the primary
class-contrast analysis.

## 7. Primary hypotheses

### H1 — stationary-period buffering

Timing deviations propagate less strongly across adjustable stationary periods
than across active migration segments:

\[
\beta_{\rm stationary}<\beta_{\rm active}.
\]

This turns the qualitative "stationary periods can reset schedules" literature
into a cross-system quantitative test.

### H2 — available-time hypothesis

Within stationary transitions, longer available interval duration is associated
with weaker propagation:

\[
\frac{\partial \beta}{\partial T_{\rm available}}<0.
\]

This tests the biologically intuitive idea that time itself is a buffering
resource.

Duration must be reported or derivable from the same annual-cycle schedule. It
will not be imputed from species averages after seeing effect sizes.

### H3 — fitness-relevant persistence

A separate subset asks whether timing deviations that remain large at the last
transition before breeding are associated with stronger reproductive timing or
fitness consequences.

This is a secondary hypothesis because vital-rate outcomes are much less
consistently reported.

## 8. Fitness layer

Fitness is not inferred from timing recovery.

For studies reporting survival or reproduction, V5 separately extracts:
- survival / return effect associated with timing;
- breeding probability;
- laying / nest-initiation timing;
- hatching/fledging success;
- seasonal fecundity;
- population growth or abundance only when explicitly linked to the focal
  timing process.

A study is classified as an **end-to-end fitness-rescue design** only when the
same individuals provide:
1. incoming timing deviation;
2. a measured correction / buffering interval or action;
3. outgoing timing deviation;
4. subsequent survival or reproduction.

Individual quality/state adjustment is separately coded because quality can
generate apparent carry-over relationships.

## 9. Important exclusions

V5 will not:
- infer a controller from \(\beta\);
- equate \(\beta\) with behavioral plasticity;
- pool repeatability and propagation slopes;
- infer fitness rescue from a final date;
- use only studies showing successful buffering;
- reclassify an interval after inspecting its slope;
- treat a non-significant slope as proof of a biological reset without
  uncertainty;
- claim that stationary periods are always beneficial.

## 10. Why this is ecologically useful

The output is intended to answer a field question rather than produce another
abstract timing index:

> **Which parts of the annual cycle are actual opportunities to erase a delay,
> and which parts simply transmit that delay forward?**

That matters because conservation of a site can have a timing function in
addition to an energetic or spatial function. A high-quality non-breeding or
stopover site may preserve the temporal slack needed to prevent a disturbance
from reaching breeding or another fitness-sensitive stage.

The comparative map also provides a more direct basis for identifying systems
with few or weak buffers, the systems highlighted as especially important by
the current phenological-mismatch literature.

## 11. Novelty wording allowed before the corpus is built

Allowed:

> We conduct a prospective comparative synthesis of stage-to-stage timing
> propagation across migratory annual cycles, using a day-for-day propagation
> coefficient to identify where delays are transmitted, absorbed, reversed or
> amplified.

Not yet allowed:

- "first meta-analysis" without a completed systematic novelty search;
- "universal buffering law";
- "stationary periods are the main reset mechanism";
- any numerical comparative conclusion;
- any fitness-rescue conclusion.

## 12. Publication consequence

V4 remains useful provenance for the fitness distinction, but its conceptual
claim is too close to established carry-over and buffering literature to carry
PAYOFF-B as a standalone paper.

V5 therefore changes the project from a primarily conceptual paper to a
prospective comparative empirical synthesis.