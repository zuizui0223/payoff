# Streptomyces congener assay-scale handoff v1

Lane: **A task/mechanism separation sublane only**.

The congener candidates and their qualitative outcome map are already frozen before outcomes. This document advances the remaining pre-outcome scale problem without opening any `delta redG` or `delta redG + mcpG` outcome.

## 1. C1 task scale can be frozen now

The focal 2020 Streptomyces division-of-labour study used the ability of producing colonies to inhibit **Bacillus subtilis** as a direct external antibiotic-function readout. In the soft-agar overlay assay, inhibition-zone size was quantified with ImageJ, and the same functional readout was used while mutant frequency was experimentally varied.

For the congener programme the primary C1 task scale is therefore frozen as:

```text
B_SUBTILIS_SOFT_AGAR_INHIBITION_ZONE_AREA_MM2
```

with orientation:

```text
larger area = stronger external competitor inhibition = better focal task performance.
```

This is preferred over pigment concentration because the architecture question concerns maintained ecological function, not maintained colour or metabolite abundance.

The candidate outcomes were not used to select this scale.

## 2. Reproductive output remains a guardrail, not part of the scalar task

The same 2020 programme treats colony-wide spore production as a fitness/reproductive quantity and showed that increasing specialist fractions can increase antibiotic output while colony-wide spore production remains relatively intact until specialist frequencies become high.

Therefore:

```text
COLONY_SPORE_OUTPUT_CFU
```

is retained as a separate developmental/reproductive guardrail.

It is not averaged with inhibition-zone area into an arbitrary composite payoff. A congener candidate cannot rescue a poor task result by weighting spore output differently after outcomes are known, or vice versa.

## 3. Direct-mu has a semantic scale but not yet a fully frozen assay implementation

The registered two-state measurement model defines:

```text
mu = fraction entering the predeclared terminal-deletion state over a registered interval.
```

Thus the direct-mu semantic scale and direction are already frozen pre-outcome.

However, the primary marker panel, exact terminal/core dosage calibration, and sampling interval for the congener experiment are not yet frozen. Consequently direct-mu is not yet qualified for outcome opening even though its mathematical estimand is defined.

## 4. Genotoxicity must be qualified response-blind

The literature motivates prodiginines as possible DNA-damaging agents, but the relevant readout is not sufficiently system-invariant to choose a primary assay from congener outcomes. Published prodigiosin studies report context-dependent DNA effects, and Streptomyces DNA-damage response markers can themselves respond to broader chromosome-state perturbations.

Accordingly the programme does **not** freeze ROS abundance, pigment amount, or SOS/RecA/LexA activation alone as the primary genotoxicity outcome.

The primary assay class must be:

```text
DIRECT_DNA_LESION_OR_BREAK_READOUT_IN_STREPTOMYCES_COELICOLOR
```

and must first pass response-blind qualification using only controls.

### Required qualification

Before congener outcomes are opened, the chosen assay must demonstrate:

```text
response to a predeclared positive DNA-damage control;
negative-control specificity;
repeatability;
fixed unit and direction;
fixed sampling context;
independence from the direct-mu deletion-state outcome.
```

Mitomycin C is the natural positive-control class because DNA-damage sensitivity and DNA-damage responses to mitomycin C are established in Streptomyces. The exact concentration and qualification threshold remain to be fixed before use.

SOS/RecA/LexA response may be retained as **secondary corroboration**, not as the sole primary genotoxicity scale.

## 5. Current opening state

After this scale audit:

```text
candidate set frozen                    = TRUE
qualitative outcome map frozen          = TRUE
C1 task scale frozen                    = TRUE
direct-mu semantic scale frozen         = TRUE
genotoxicity primary scale qualified    = FALSE
direct-mu marker/window frozen          = FALSE
materiality thresholds frozen           = FALSE
uncertainty construction frozen         = FALSE
outcome opening allowed                 = FALSE
```

So this is progress in preregistration, not data analysis.

## 6. Architecture claim ceiling remains unchanged

No assay-scale choice implies that a matched shared/generalist architecture exists.

Current status remains:

```text
MATCHED_GENERALIST_SHARED_ARCHITECTURE_RECOVERED = FALSE
MATCHED_S_CERTIFIED = FALSE
ARCHITECTURE_MAPPING_CERTIFIED = FALSE
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_IDENTIFIED = FALSE
```

The RED two-probe programme and the congener C0 programme remain prospective until their predeclared measurement contracts are fully frozen and outcome data are subsequently collected or recovered.
