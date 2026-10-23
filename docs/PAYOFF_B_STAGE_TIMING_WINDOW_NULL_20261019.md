# PAYOFF-B stage-propagation: structural window-censoring null

Date: 2026-10-19. This is a mathematical/simulation diagnostic created
**before seeing the newly executed stork 53-season stage slope**. Its role is
to prevent misinterpretation of the already frozen pilot. The original
premodel lock is left unchanged.

## Model

Let entry timing X be independent of route-stage duration W and let
Y = X + W. Under unconstrained observation, the population regression
of Y on X is identically 1, because Cov(X,W)=0. Biological feedback
and active time correction are **absent** by construction.

However, observing a fixed window ending on calendar day T necessarily
conditions on Y <= T. That creates a negative conditional dependence
between X and W: later arrivals can enter the observed sample only if
their duration is shorter. Thus beta(Y ~ X | Y <= T) can fall below 1
even if no animal actively corrects its migration schedule.

A purely illustrative numerical example is fixed at:
- X independently uniform over days 61–106;
- W independently uniform over 10–45 days;
- selection Y <= day 120 (a stylized end-of-April window);
- 250,000 synthetic draws; fixed random seed 20261019;
- report full-population and window-conditioned OLS slopes.

These numbers are **not estimated from stork or other Movebank animal
tracks** and must not be called an observed effect or calibrated counterfactual.

## Consequence

The earlier stork pilot's registered beta <1 criterion, if satisfied,
would prove only descriptive contraction in the admitted observational
sample. It cannot identify adaptive phase correction, learning, information
use or timing flexibility. A censoring-aware design must compare matched
stage times with right-censored tracks explicitly and, ideally, observe
signed reactions to independently recorded cues.

The original frozen primary pilot result must be reported regardless of
this separate synthetic diagnostic; do not alter its inclusion thresholds.
