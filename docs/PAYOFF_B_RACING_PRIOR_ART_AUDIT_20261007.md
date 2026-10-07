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

This makes racing a useful negative-control / mechanism-separation system, not yet a standalone novelty route.

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

Promotion would require one of two things:

1. **PAYOFF validation route:** preregister racing as an external mechanism-separation test of the general information-value geometry; or
2. **prediction route:** define a genuinely distinct forecasting problem, such as whether a model’s standalone proper score keeps improving while its incremental proper-score advantage over the contemporaneous market peaks earlier, and demonstrate that this estimand is not already answered by the interim-odds literature.

No racing outcome should be opened to choose the time windows or the preferred direction before that distinction is frozen.
