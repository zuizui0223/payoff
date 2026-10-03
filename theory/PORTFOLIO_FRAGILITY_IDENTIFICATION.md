# PAYOFF-B portfolio-fragility identification triangle

Date: **2026-10-03**  
Status: **post-freeze empirical-identification extension; frozen GEB V2 unchanged**

## 1. Why a before/after timing change is not enough

The clock-portfolio theorem predicts that loss of usable downstream correction
opportunity can inflate final timing error, especially for feedback-heavy
strategies.

A natural before/after increase in mismatch does not identify that mechanism.
Three distinct processes must be separated:

1. **effective opportunity loss** — how much usable correction capacity was
   actually removed;
2. **substitution/rerouting** — whether alternative opportunities replaced the
   lost one;
3. **selection/reweighting** — whether the perturbation changed which timing
   phenotypes survived or remained observed.

The direct portfolio-fragility estimand is within-individual or otherwise
counterfactually matched change after independently defined opportunity loss.

## 2. Selection-fragility variance identity

Let \(E_i\) be individual \(i\)'s counterfactual baseline final phase error and
\(D_i\) its perturbation-induced within-individual change.

Let normalized weights \(w_i\) describe the composition of the observed
post-perturbation population.

Then post-perturbation error is

\[
E_i'=E_i+D_i.
\]

The observed variance change is exactly

\[
\boxed{
\operatorname{Var}_w(E+D)-\operatorname{Var}(E)
=
\left[
\operatorname{Var}_w(E)-\operatorname{Var}(E)
\right]
+
\operatorname{Var}_w(D)
+
2\operatorname{Cov}_w(E,D).
}
\]

The first bracket is a **selection/reweighting component**. The remaining terms
are the within-individual perturbation component in the post-perturbation
weighted population.

Therefore population variance can change even when every individual's timing
response is zero.

Conversely, genuine within-individual fragility can be partly hidden if
selection removes the individuals with the largest baseline errors.

## 3. Natural anchors define the three identification hazards

### Direct opportunity restriction — piping plover after Hurricane Dorian

Sweeney et al. (2026) use 2016–2023 Ocracoke Island mark-resighting data and
remote-sensing habitat change to study a storm-driven reduction in stopover
habitat. The public Dryad dataset contains annual encounter histories,
individual IDs and morphometrics; the study reports reduced stopover duration
after habitat loss.

This is a strong **opportunity-loss anchor** because the habitat perturbation is
external to individual timing behavior.

It is not a direct portfolio-fragility test because the public dataset contains
no downstream destination/breeding timing endpoint on the same phase
coordinate.

### Opportunity substitution — pink-footed goose after Filsø flooding

Published geese that lost use of the restored/flooded Filsø staging area
shifted to alternative staging areas without a detectable subsequent body-
condition penalty.

This shows

\[
\text{named-site loss}
\ne
\text{effective opportunity loss}.
\]

The portfolio variable \(\omega\) must quantify retained **usable correction
capacity after substitution**, not raw site count or habitat area alone.

### Selection/reweighting — great knot under Yellow Sea habitat deterioration

A 13-year great-knot dataset documents lower apparent survival of late-arriving,
low-fuel individuals during a period of staging-habitat loss/deterioration,
together with population-level advancement of mean arrival date and increased
fuel load.

This demonstrates a major confound for clock-portfolio inference:

> a disturbed population can appear to change its migration-timing phenotype
> because vulnerable phenotypes disappear, not because surviving individuals
> changed their own clock portfolio.

## 4. Identification triangle

A defensible direct test therefore requires all three corners:

### A. Independent opportunity loss

Define the perturbation without using the downstream timing outcome.

### B. Within-individual or matched timing change

Estimate \(D_i\) from repeated individuals, experimentally matched cohorts or a
design that reconstructs counterfactual timing.

### C. Composition stability or explicit selection model

Track survival/observation so changes in the sampled phenotype distribution are
not silently interpreted as behavioral fragility.

If any corner is missing, the result is an anchor or supporting mechanism, not
a direct test of the portfolio-fragility theorem.

## 5. Implication for the exact clock-portfolio prediction

The theorem

\[
\frac{V_{\rm disrupted}}{V^*}
=
\exp[(1-\omega)s_{\rm feedback}P]
\]

refers to timing variance for the relevant biological architecture under an
opportunity perturbation.

In natural data, raw population variance can only be mapped to that quantity
after ruling out or modelling reweighting and after defining \(\omega\) from
effective usable opportunity.

Thus:
- raw habitat-area loss is not \((1-\omega)\);
- before/after population variance is not automatically within-individual
  fragility;
- loss-induced phenotype selection is not controller adaptation.

## 6. Preferred future design

The strongest design is a repeated-individual natural experiment:

1. estimate historical entry error and correction architecture before the
   perturbation;
2. quantify externally caused loss of usable downstream opportunity;
3. follow the same individuals after the perturbation;
4. measure final phase error on the same coordinate;
5. record survival/observation to detect selective disappearance.

This simultaneously handles substitution and selection.

## 7. Novelty boundary

Selection bias, habitat substitution and repeated-individual designs are
standard ecological ideas.

PAYOFF-B should claim only the synthesis:

> **clock-portfolio fragility is a within-architecture response to lost
> correction opportunity and must be distinguished from both ecological
> substitution and perturbation-driven selection of timing phenotypes.**

The public piping-plover and great-knot datasets strengthen the identification
framework but do not directly validate the portfolio-fragility equation.
