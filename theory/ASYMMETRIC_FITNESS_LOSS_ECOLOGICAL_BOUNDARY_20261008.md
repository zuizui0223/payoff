# PAYOFF-B ecological extension: asymmetric mismatch loss and risk-sensitive seasonal decisions

Date: 2026-10-08
Status: **prospective sensitivity / refutation of a symmetric payoff assumption**.
Base: PR #318 Paper-2 V4 fitness-target construct correction.
**No frozen V3, V7R, V8 or historical environmental results are reopened.**
No original winter-moth raw experiment, bird cues, or animal fitness outcome was fitted.

## Exact biological problem

PAYOFF-B currently uses a one-step symmetric quadratic correction loss,

    L(u) = kappa*u^2 + mu*(e-u)^2,

where phase error e must be the difference between an animal's event time and
the **fitness-optimal** event time. That equation implies equal loss for
fitness-centred timing errors of the same magnitude but opposite signs.
Nothing in V8's remote green-up mismatch, Ortega mule-deer route correction,
or the published goose energetics provides evidence for such symmetry.

The natural winter-moth example offers a direct challenge. Van Dis et al.
(2023; Proc R Soc B, DOI 10.1098/rspb.2023.0414) experimentally manipulated
hatching from 4 days before to 5 days after oak budburst. Survival × predicted
pupal weight (fecundity proxy) peaked at **two days after budburst**. Their
reported mean relative-fitness declines away from that peak were about
**14% per day on the earlier side**, versus about **6% per day on the later
side**, with strong nonlinearity (up to 32% per day at starvation extremes).
These are the *authors' findings*, not PAYOFF-B results.

Crucial provenance: the 14%/6% figures are *averages of relative fitness
changes across treatments*. They are not exact local log-fitness derivatives,
constant selection coefficients, nor measurements transferable from winter
moths to deer or geese. The inferred experimental optimum may differ under
natural host-switching, competition and predation in the wild.

## Decisive prior-art overlap (confirmed during review)

**Not a new ecological phenomenon.** Lof, Reed, McNamara & Visser
(2012), *Proceedings of the Royal Society B*, DOI
10.1098/rspb.2012.0431, specifically modelled *avian* reproduction under
environmental variance and asymmetric fitness curves. They already showed
that the optimal breeding reaction norm can shift away from the steeper side
of the fitness curve, causing an **adaptively mismatched** event despite
available environmental information. Visser & Gienapp (2019),
*Nature Ecology & Evolution*, DOI 10.1038/s41559-019-0880-8,
explicitly review optimal phenological mismatches arising from multiple
fitness components, skewed costs and early-season survival trade-offs.
Bauer et al. (2020) further reviewed uncertainty and information use in
migration decisions.

Accordingly PAYOFF-B MUST NOT claim priority for:
- timing that is optimal despite apparent resource mismatch;
- shifts of mean seasonal timing with forecast uncertainty under asymmetric
  selection;
- asymmetric early-versus-late losses changing timing decisions;
- treating total fitness as different from resource synchrony.

The current implementation is a **robustness and construct-validity check**
against an unjustified symmetric loss assumption in an existing PAYOFF-B
timer-controller, rather than a new independent theoretical mechanism.
Existing asymmetry literature is more ecologically developed than the
simple piecewise-linear toy used here.

## Existing mathematics, ecologically reinterpreted

Define fitness phase e=event date minus fitness-optimal event date (positive =
late). Correction u>0 advances the event, reducing e; u<0 delays it. A
posterior estimate e|information is approximated by N(m,s^2).

A piecewise-linear asymmetric loss with quadratic action cost is

    risk(u) =
      E[c_early*(u-e)_+ + c_late*(e-u)_+ | information]
      + (kappa/2)*u^2

for c_early,c_late>=0, kappa>=0, and actual feasible correction limits

    -max_delay <= u <= max_advance.

Here c_early penalizes ending too early (e-u<0); c_late penalizes ending too
late (e-u>0). The biological cost unit must eventually be actual fitness loss,
and kappa an independent cost of phenological adjustment, not a fitted
correlation coefficient.

For a continuous posterior CDF F_e and an interior optimum, the first-order
condition is exactly

    (c_early+c_late)*F_e(u*) + kappa*u* - c_late = 0.

If kappa=0 and both side costs are positive,

    F_e(u*)=c_late/(c_early+c_late).

That is the standard *asymmetric quantile / pinball loss* decision rule,
well established in statistics and inventory theory; PAYOFF-B claims **no
new mathematical theorem** here. With no observation uncertainty (s=0) and
kappa>0, the optimizer is the known-phase timing correction clipped to the
interval [-c_early/kappa, +c_late/kappa] and the physical response limits.

In the unconstrained zero-effort **Gaussian** special case,

    u* = posterior_mean + posterior_sd * Phi_inverse(q),
    q = c_late/(c_early+c_late).

For fixed q and mean, the change in optimal timing with posterior
uncertainty is exactly d u*/d posterior_sd = Phi_inverse(q). This
uncertainty-dependent timing bias can otherwise look like a shift in the
fitness target itself. With only one uncertainty level, changing the
target offset and changing asymmetric loss can be observationally aliased.
Comparing prespecified information-precision conditions while independently
measuring the fitness curve could distinguish them under the declared
model. This is a standard quantile result, and **the general ecological
phenomenon is already explicitly modelled by Lof et al. (2012)**.

If c_early>c_late, the optimal posterior percentile is below 0.5. Thus a
posterior with mean zero and symmetric uncertainty need not induce action
u=0: a risk-sensitive animal can rationally choose a **negative correction**
(delay the event) to avoid the more damaging early tail. This is a
fitness-related directional bias, not evidence of slow or defective tracking.

## Transparent synthetic witness; *not* raw-data calibration

In a toy N(0,1 day^2) **fitness-centred** phase posterior with no action
penalty and large equal bounds:

    c_early : c_late = 14 : 6
    q = 6/(14+6) = 0.30
    u* = Phi_inverse(0.30) approximately -0.5244 days.

The numerical 14:6 ratio is **illustrative, inspired by the published
averaged experimental percentage changes**, not a fitted slope of the real
fitness surface. A symmetric 10:10 ratio would yield u*=0 in the same toy
belief state. In the original PAYOFF sign convention u<0 *delays* progress.
If an organism has already developmentally committed so that
max_delay=max_advance=0, the rational correction is zero in this stage even
though asymmetry remains; larvae do not undo hatching after emergence.

A second coordinate example: budburst r=0 is NOT the experimental fitness
peak for winter moth. With its experimentally estimated offset delta=+2
days, the fitness-centred phase for an event at budburst is e=-2 days.
A hypothetical *pre-event* fully informed and cost-free actor with feasible
delay could align the event to day+2 even though resource-marker mismatch
|r| increases from 0 to 2. This is a logical counterexample, **not a
measurement of adjustment behavior or fitness gain by moths**.

## New falsifiable predictions relative to PAYOFF-B's symmetric controller

1. **Risk-direction signature:** conditional on the same posterior mean phase
   and the same information precision, species/stages with a steeper fitness
   cost for too-early events should adopt later event timing than those with
   symmetric costs if timing remains adjustable. This requires measuring the
   side-specific fitness losses independently, not using observed timing to
   define the loss.
2. **Capacity interaction:** when the delaying/advancing correction window
   closes, the predicted timing bias disappears from *action* but not the
   asymmetric **fitness consequences** of error. Zero action need not be
   evidence of no signal.
3. **Information does not imply synchrony:** two interacting organisms with
   identical cue beliefs and physical action sets can select different timing
   corrections because their fitness-loss shapes differ. This is not
   coordination failure unless their payoffs include an explicitly measured
   interaction term.
4. **Source-phase guard:** fitting resource-centred r without an independently
   estimated fitness optimum offset delta cannot test the quantile rule.
   "Matched green-up" is not equivalent to "optimal timing".
5. **Wrong-model negative control:** symmetric quadratic timing feedback
   predicts correction proportional to posterior mean and equal signed
   response for +e versus -e. The asymmetric risk model can violate both.
   Compare their *held-out predictive* performance with independently measured
   loss curves rather than relabel existing data a success.

## Evidence gaps / prior art

- van Dis et al. (2023) already estimated the winter-moth fitness curve and
  its asymmetry. Their experiment did **not** test mobile animal checkpoint
  cue uptake, within-season control changes, or the PAYOFF-B timer-controller
  mechanism.
- Torstenson & Shaw (2025, *Oikos*, DOI 10.1111/oik.10862) already distinguish
  cue timing accuracy from fitness efficacy and study cue-type payoffs.
- Jonzén et al. (2007, *Proc R Soc B*) established optimal undertracking with
  full information and arrival costs.
- Aikens et al. (2021, *Ecology*) already report the competing green-up and
  offspring-development timing opportunities in mule deer.
- A purely Gaussian loss fit to environmental R² cannot recover c_early,
  c_late, optimum delta, actual feedback gain or demographic fitness.
- The original winter-moth data are deposited at
  https://doi.org/10.5061/dryad.m905qfv5p, original code at
  https://github.com/NEvanDis/WM_fitness. This branch uses **published
  figures/descriptions only**, not the original raw CSV.

## Implementation and testing

- src/asymmetric_phase_fitness_controller.py uses an exact analytic Gaussian
  expected hinge loss and bounded one-dimensional convex minimization.
- tests/test_asymmetric_phase_fitness_controller.py includes posterior
  quantile, early/late reversal, symmetric null, fitness-marker offset,
  bounds, quadratic effort, zero actionability, seeded Monte Carlo, a brute
  risk-grid cross-check, and fail-closed input validation.

Neither new model nor future experiments are a standalone high-impact ecology
paper now. The justified role is to make Paper 2's **ecological predictions**
honest under empirically measured fitness asymmetry rather than building the
conclusion on an untested symmetric fitness penalty.
