# PAYOFF-B information-value / actionability bridge — 2026-10-06

Status: **POSTHOC EXACT REFRAMING; GENERIC DECISION THEORY IS PRIOR ART**

## Purpose

The frozen V8 primary analysis used detrended Pearson correlation as its
prespecified environmental coordinate. The later metric-scale diagnostic showed
that standardized coupling, absolute prediction risk and the value of adding a
source cue need not move together.

This note replaces correlation as the theoretical information object with
decision-scale expected-loss reduction.

## 1. General information value

Let L0(t) be the minimum expected loss at stage t without the focal
environmental information and L1(t) the minimum expected loss with that
information.

Define:

    G(t) = L0(t) - L1(t).

G(t) is the decision-scale value of information at that stage.

Let r(t) in [0,1] be retained actionability and C(t) direct waiting cost.

Then:

    N(t) = r(t) G(t) - C(t).

Any differentiable interior optimum satisfies:

    r G' = -r' G + C'.

With zero direct marginal waiting cost:

    G'/G = -r'/r.

This is the general information-value / actionability balance.

The prior binary-cue model is recovered by setting:

    G(t) = S q(t) - B.

Thus the existing t* result is a special case, not a competing theory.

## 2. Gaussian timing target under squared loss

Let Y be a centered future timing target and X a centered source cue.

Under the population optimal linear predictor and squared-error loss:

    baseline risk = Var(Y) = sigma_Y^2

    residual risk = Var(Y | linear X)
                  = sigma_Y^2 (1 - rho^2)

    information value = sigma_Y^2 rho^2.

Therefore:

    baseline risk = information value + residual risk.

This is ordinary linear prediction algebra, not a new statistical theorem.

## 3. Scale-reversal condition

Compare two periods 1 and 2.

Information value increases when:

    sigma_2^2 rho_2^2 > sigma_1^2 rho_1^2.

Residual absolute uncertainty also increases when:

    sigma_2^2 (1-rho_2^2)
      >
    sigma_1^2 (1-rho_1^2).

Thus stronger correlation can coexist with larger residual uncertainty if
target variance grows sufficiently.

For rho_2 > rho_1, residual risk increases whenever:

    sigma_2 / sigma_1
      >
    sqrt[(1-rho_1^2)/(1-rho_2^2)].

The ecological interpretation is:

> a more variable future can make nonlocal information more valuable while
> simultaneously leaving more absolute uncertainty unresolved.

This is the exact scale boundary exposed by the V8 diagnostic.

## 4. Why correlation is not the ecological quantity of interest

Correlation answers:

> What fraction of standardized variation is shared?

Decision-scale information value answers:

> How much expected loss can be removed by observing the source cue?

Residual prediction risk answers:

> How much uncertainty remains after using the cue?

These quantities should not be conflated.

A system can have:
- low rho but low absolute uncertainty;
- high rho but high absolute residual uncertainty;
- increasing rho and increasing residual uncertainty;
- increasing rho and increasing information value.

## 5. Empirical counterpart

The posthoc V8 diagnostic estimates an out-of-sample analogue:

    G_CV
      =
    MSE(target-trend-only)
      -
    MSE(source-informed).

This matches the squared-loss theoretical definition better than an RMSE
difference.

Across the 166 V8 spatial pairs, the diagnostic reconstruction gives:

- early mean G_CV = about -16.1 d^2;
- late mean G_CV = about +16.0 d^2;
- late-minus-early change = about +32.1 d^2.

The increase is positive under:
- pair bootstrap;
- source-cell clustering;
- target-cell clustering;
- 5-degree spatial blocks;
- 10-degree spatial blocks.

In the 58 exact 8/8-year pairs:
- early mean G_CV = about -2.66 d^2;
- late mean G_CV = about +25.64 d^2;
- change = about +28.30 d^2;
- all dependence-aware intervals remain positive.

These are posthoc diagnostics and cannot replace the preregistered V8 primary
endpoint.

## 6. Ecological architecture

The revised seasonal sequence is:

    environmental state variability
        -> information value G(t)
        -> retained actionability r(t)
        -> enacted correction
        -> realized timing.

The source cue need not reduce all uncertainty to be valuable.

Likewise, high information value does not guarantee improved realized timing:
the organism must perceive the information and retain an actuator capable of
changing the relevant outcome.

## 7. Relation to prediction and correction

Upstream prediction and downstream correction are partially substitutable ways
to reduce inherited timing error.

But they are not fully substitutable when new error is generated after
commitment.

With post-entry innovation Q:

    V_(k+1) = lambda^2 V_k + Q.

Improved upstream forecast value can reduce V_0, whereas downstream correction
is required to suppress errors generated later.

This is the conceptual bridge between:
- the bird environmental-information analysis; and
- the mule-deer phase-correction anchor.

The paper must not claim that the birds themselves used the reconstructed
source cue or that their stable mismatch was caused by downstream correction.

## 8. Novelty boundary

Do not claim novelty for:
- expected value of information;
- variance decomposition;
- optimal linear prediction;
- feedforward/feedback control;
- optimal stopping;
- the fact that environmental variability affects forecast value.

The candidate ecological contribution is narrower:

> seasonal tracking should distinguish the decision-scale value of information
> from residual uncertainty and from retained actionability; the same seasonal
> system can move in opposite directions on those axes.

The V8 system supplies a natural empirical example of that separation, while
mule deer supply an independent natural example of signed downstream
correction.
