# PAYOFF-B racing / prediction-market prior-art audit

Date: **2026-10-07**  
Status: **prospective novelty audit before outcome access**

## Question

Can horse-racing prediction provide a genuinely new empirical extension of PAYOFF-B, or is it better used as a boundary case / external stress test?

## Bottom line

**Do not create a racing novelty claim around information absorption, odds trajectories, or late informed wagering.**

Those mechanisms are already established in betting-market and prediction-market research.

The useful PAYOFF-B role is narrower:

1. horse racing offers repeated hidden-state prediction with a sharp deadline;
2. public odds provide an explicit collective forecast;
3. time-series odds reveal information aggregation through time;
4. unlike migration or phenology, physical actionability can be approximately held fixed until the wagering cutoff;
5. therefore racing can help separate **loss of actionability** from **loss of relative information advantage**.

This makes racing a useful negative-control / mechanism-separation system, **not a standalone novelty route**. The Green et al. (2019) diffusion result closes the broad standalone route.

## Closest prior art

### Figlewski 1979 — subjective information discounting

Stephen Figlewski, *Subjective Information and Market Efficiency in a Betting Market*, Journal of Political Economy 87(1):75–88.

The paper asks whether published professional handicapper forecasts contain information not already reflected in track odds. It finds substantial forecast information but reports that the betting market discounts almost all of it.

Collision:

- focal forecast versus market forecast;
- incremental information value after market absorption.

### Bird & McCrae 1987 — price paths and efficiency

Ron Bird & Michael McCrae, *Tests of the Efficiency of Racetrack Betting Using Bookmaker Odds*, Management Science 33(12):1552–1562.

The paper uses a sequence of prices during betting and tests whether odds movements can be exploited. It concludes that the market is efficient with respect to public odds movements and tipster information, while private information may still matter.

Collision:

- time-indexed information absorption;
- market efficiency through the betting period.

### Johnson, Jones & Tang 2006 — closing price is not the whole path

Johnnie E. V. Johnson, Owen Jones & Leilei Tang, *Exploring Decision Makers’ Use of Price Information in a Speculative Market*, Management Science 52(6):897–908.

The paper extracts predictors from time-indexed odds curves and reports that closing prices do not fully incorporate information in the price path.

Collision:

- path dependence of predictive information;
- insufficiency of the final price alone.

### Brown, Reade & Vaughan Williams 2019 — information arrival can reduce accuracy

Alasdair Brown, J. James Reade & Leighton Vaughan Williams, *When are prediction market prices most informative?*, International Journal of Forecasting 35(1):420–428.

Using Intrade and opinion-poll releases, the paper shows that an information event can initially reduce price efficiency because inexperienced traders respond first; experienced traders correct the market later.

Collision:

- prediction accuracy need not improve monotonically with more raw information;
- information diffusion and trader composition matter dynamically.

### Benter / two-stage forecast-combination tradition — hybrid predictor collision

William Benter's computerized handicapping work explicitly combines a
fundamental handicapping probability with the public's implied probability in a
second logit stage.  Later horse-racing forecasting work likewise combines
model-based forecasts with market odds and develops forecast-combination
methods for competitive events.

This collides directly with the implementation

    h_i(t)
      proportional to
    f_i ^ w_t * m_i(t) ^ (1-w_t).

The PAYOFF implementation is therefore **not a novel horse-racing prediction
architecture**.  It is a deliberately simple forecast-encompassing device used
to measure whether a fixed forecast retains incremental proper-score value over
a contemporaneous market forecast.

Directly occupied territory:

- combining a fundamental model with public implied probabilities;
- interpreting relative forecast weights;
- evaluating whether model forecasts add information beyond betting odds.

PAYOFF-specific use:

- fit the same combination at declared pre-race time slices;
- treat the time path of incremental forecast value as a descriptive proxy for
  competitive information absorption;
- compare that mechanism with ecological loss of actionability.

### Green, Sung, Ma & Johnson 2019 — direct diffusion-of-forecast-value collision

Lawrence Green, Ming-Chien Sung, Tiejun Ma & Johnnie E. V. Johnson,
*To what extent can new web-based technology improve forecasts? Assessing the
economic value of information derived from Virtual Globes and its rate of
diffusion in a financial market*, European Journal of Operational Research
278(1):226–239.

This is a stronger collision than the earlier audit recorded. Using a
horse-race betting market over an eighteen-year period, the paper asks whether
new geospatial information improves winning-probability forecasts, whether the
information creates temporary economic value, and how quickly that value
disappears as the market learns to use the same information.

The paper reports exactly the broad competitive-information pattern that a
standalone PAYOFF racing paper might otherwise try to claim:

    novel forecast information has value
        ->
    market participants learn / information diffuses
        ->
    market odds increasingly discount it
        ->
    the incremental opportunity disappears.

Directly occupied territory:

- forecast information with value beyond market prices;
- changing incremental value as information diffuses;
- rate of information diffusion through a horse-racing betting market;
- longitudinal disappearance of an informational edge.

Therefore **information-value decay through market diffusion is established
prior art**, not a PAYOFF-B empirical novelty.

The remaining PAYOFF use is mechanism contrast: Green et al. supply an
empirical example of value decay through diffusion while PAYOFF-B ecology asks
about value decay through lost biological actionability.

### Hanyu, Ishii, Otani & Teramoto 2026 — direct Japanese parimutuel collision

Hiroaki Hanyu, Shunsuke Ishii, Suguru Otani & Kazuhiro Teramoto, *Are Final Market Prices Sufficient for Information Aggregation? Evidence from Last-Minute Dynamics in Parimutuel Betting*, UTMD-149, revised 2026-08-21.

This is the closest current collision.

Using interim odds from Japanese central horse racing, they report that horses whose odds decline in the final five minutes earn higher realized returns than horses with similar final odds. Their two-period information model attributes late odds declines to informed bettors acting on private signals.

Directly occupied territory:

- interim Japanese horse-racing odds;
- last-minute information arrival;
- private-signal interpretation;
- path dependence conditional on final odds.

## What remains useful for PAYOFF-B

The prospective PAYOFF-B reduced form is

    N(t) = r(t) e(t) V_A(q(t)) - C(t),

where:

- q(t) = focal state-prediction quality;
- r(t) = retained biological / physical actionability;
- e(t) = retained differential information advantage;
- C(t) = waiting cost.

Racing supplies a system where the main decay can be placed in e(t), while ecological migration/phenology supplies systems where decay can be placed in r(t).

This yields a mechanism-comparison design:

    ecology:
        q rises, r falls, e approximately fixed/not market-defined

    competitive prediction:
        q may rise, r approximately fixed until cutoff, e falls as information is absorbed

The conceptual payoff is **not** that the mechanisms are the same. It is that the same observed shape — information becomes less useful before the event — can arise from distinct causal channels.

## Identification warning

Under the exponential reduced form,

    r(t)=exp(-beta t)
    e(t)=exp(-gamma t),

the optimum depends only on

    beta + gamma.

Therefore the time of peak usable information cannot by itself identify whether value disappeared because:

- the actor lost the ability to respond; or
- other actors absorbed the information.

Independent measurements are required.

This warning feeds directly back into ecological interpretation: a hump-shaped information-use curve is not evidence for biological irreversibility unless alternative loss-of-relative-information mechanisms are excluded.

## Recommendation

Keep this route on an exploratory branch.

Do not merge it into a frozen PAYOFF-B manuscript as a new empirical result.

Promotion is now limited to one route:

1. **PAYOFF validation / teaching route:** use racing as an external
   mechanism-separation or negative-control system for the general
   information-value geometry.

The broad **standalone racing novelty route is CLOSED** unless a later,
independently motivated question survives a new prior-art audit. The present
proper-score design may still be useful as a clean demonstration, but success
must not be described as discovering that markets absorb useful public
information.

No racing outcome should be opened to choose the time windows or the preferred
direction before the validation role is frozen.
