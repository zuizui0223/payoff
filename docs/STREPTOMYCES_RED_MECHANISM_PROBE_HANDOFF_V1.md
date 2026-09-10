# Streptomyces RED mechanism-probe handoff v1

Lane: **A mechanism-probe sublane only**.

This document converts the matched-S negative recovery into a focused prospective test programme. It does **not** certify a matched S architecture and does not change Lane G, Lane R, or E1.

## 1. Why RED/prodiginines are now the focused mediator

The 2025 caste-ratio study (*Factors that influence the caste ratio in a bacterial division of labour*, DOI `10.1098/rstb.2023.0267`) discusses endogenous prodigiosin/prodiginines as a candidate contributor to genome damage in aging colony regions and explicitly motivates testing prodiginine-deficient backgrounds.

The existing PAYOFF identifiability gate already shows that an observed mutant/specialist fraction cannot by itself identify the differentiation-generation rate `mu`. The useful next question is therefore narrower:

```text
Does removing RED/prodiginine biosynthesis reduce the direct generation rate
of terminal genomic specialists, after separating generation from
post-generation survival/realization?
```

## 2. Highest-priority probe A — M1141 versus M1142

Primary source:

```text
Gomez-Escribano & Bibb 2011, Microbial Biotechnology
DOI 10.1111/j.1751-7915.2010.00219.x
```

The published strain pedigree gives:

```text
M1141 = Δact
M1142 = Δact Δred
```

M1142 was produced in the sequential deletion series from the M1141 background, so the focal pair differs by removal of the RED biosynthetic cluster rather than by using unrelated strain backgrounds.

The same study reports that M1141–M1146 grew and sporulated as well as parental M145. This makes the pair much cleaner for a **mechanism test** than M145 versus ΔredD, where developmental timing is strongly shifted.

Why it is not matched S:

```text
direct terminal-specialist generation rate has not been measured;
post-generation specialist realization has not been matched;
the RED cluster itself is removed, so the relevant net functional output is
not automatically preserved;
both strains already share an ACT deletion background.
```

Status:

```text
M1141_VS_M1142_MECHANISM_PROBE_READY = TRUE
M1141_VS_M1142_MATCHED_S_CERTIFIED = FALSE
```

## 3. Highest-priority probe B — M145 versus redU single mutant

Primary source:

```text
Lu, San Roman & Gehring 2008, Journal of Bacteriology
DOI 10.1128/JB.00865-08
```

The `redU`/`SCO5883` single mutant is especially useful because the study reports:

```text
RED production: essentially abolished (<2% of WT on R2YE)
ACT: substantial production retained
aerial mycelium formation: no apparent defect
sporulation: no apparent defect
```

Thus gross morphological development is much better matched than in the `redD` null mutant.

Important caveat:

The authors could not complement the RED defect with their `redU` construct and note likely polar effects on downstream `redV`. Therefore this is a strong RED-biosynthesis probe, but not a perfectly isolated RedU-only perturbation.

Why it is not matched S:

```text
direct specialist-generation reduction is unmeasured;
post-generation realization is unmeasured;
RED output itself is removed;
possible redV polarity remains.
```

Status:

```text
M145_VS_redU_MECHANISM_PROBE_READY = TRUE
M145_VS_redU_MATCHED_S_CERTIFIED = FALSE
```

## 4. Why ΔredD is demoted to a developmental-pleiotropy control

Primary source:

```text
Tenconi et al. 2020, Antibiotics
DOI 10.3390/antibiotics9120847
```

The ΔredD strain M510 does remove prodiginine output, but it also accelerates aerial-hypha formation and mature-spore-chain formation and changes the timing of actinorhodin production and developmental-gene expression.

Therefore:

```text
M145_VS_M510_DELTA_redD_MECHANISM_PROBE_READY = FALSE
```

for the strict gross-development-matched probe gate. It remains useful as a mechanistically informative positive-control background.

## 5. What a successful mechanism-probe result would mean

Suppose a predeclared RED-deficient probe showed a lower directly measured terminal-specialist generation rate while post-generation realization was adequately controlled.

That would support:

```text
RED_PRODIGININE_CONTRIBUTES_TO_TERMINAL_SPECIALIST_GENERATION
```

It would **not** yet support:

```text
MATCHED_S_ARCHITECTURE_CERTIFIED
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED
```

because an S architecture additionally has to preserve the relevant net task and constitute a stable/heritable strategic unit matched to D.

## 6. What would falsify or weaken the RED mechanism route

The RED route should lose priority if either high-priority probe shows, under a matched measurement window:

```text
no reduction in direct terminal-specialist generation;
or
an apparent frequency reduction explained by post-generation survival/realization;
or
large baseline growth/sporulation differences that destroy the comparator match.
```

Agreement between the two mechanistically different RED-deficient probe systems would be stronger evidence than either alone because their major caveats differ:

```text
M1141/M1142 -> whole-cluster deletion / Δact shared background
redU        -> possible downstream redV polarity
```

## 7. Current status

```text
PROSPECTIVE_RED_MECHANISM_PROBES_RECOVERED = TRUE
READY_PROBE_COUNT = 2
DIRECT_GENERATION_SUPPRESSION_IDENTIFIED = FALSE
MATCHED_S_CERTIFIED = FALSE
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED = FALSE
```

This is the intended positive handoff from literature recovery to a focused A-lane mechanism test, without semantic promotion into the game lane.
