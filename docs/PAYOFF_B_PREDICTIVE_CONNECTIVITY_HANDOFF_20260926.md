# PAYOFF-B predictive connectivity — empirical handoff

Frozen: **2026-09-26**  
Status: **new information-axis analysis frozen before outcome fitting**

## Why this is the next test

The Bayesian extension predicts that a migrant needs not only movement or timing capacity, but information available **before commitment** that predicts the later seasonal state.

The empirical quantity is therefore **predictive connectivity**: how well an environmental state observable earlier along a route predicts the state realized later at the destination.

The primary coordinate is signed rho between origin and destination seasonal-state anomalies.

## Preventing a trivial climate-trend result

Two sites can correlate simply because both warm through time. That is not the interannual information required by the Bayesian game. For every connectivity estimate we therefore:

1. use only observations available before the focal outcome year;
2. regress origin seasonal state on year;
3. regress destination seasonal state on year separately;
4. correlate the two residual series.

Signed residual rho is primary. Negative correlations remain negative.

As a secondary theoretical bridge only, centered bivariate-Gaussian residuals imply same-sign binary cue agreement q = 1/2 + asin(rho)/pi. rho remains the empirical estimand.

## Lane A — wigeon mechanistic bridge

The existing wigeon programme has 256 staging events and 224 consecutive transitions with POWER and source-faithful ERA5 phase reconstructions.

For each staging segment, use the median event coordinate only to define a route location. Reconstruct annual ERA5 TGS onset for **2000–2017**, before the 2018–2020 tracking outcomes. For every ordered consecutive segment pair, separately detrend origin and destination TGS onset on year and correlate residuals.

The TGS transform remains the frozen January–July cumulative-minimum 5 C rule.

Registered model:

    phase_change ~ origin_phase * z_connectivity
                 + z_progress + z_endpoint
                 + z_progress:z_endpoint + C(year)

with individual-clustered uncertainty.

The directional prediction is **origin_phase:z_connectivity < 0**: higher predictive connectivity should strengthen phase correction and reduce phase retention.

This lane is a retrospective mechanistic bridge, not an untouched independent confirmation, because the basic wigeon lambda result is already known. The new connectivity interaction has not been fitted at this freeze.

## Lane B — 55-species broad test

The generality test uses the frozen Amaral source commit 62c58d77c2028bd863dfe3697b0d9cf29ceaeab0: 55 eastern North American migratory bird species over 2002–2017.

For each species and breeding-range target cell:

1. identify species cells marked migratory-range;
2. retain those strictly south of the target;
3. select the geographically nearest one;
4. break exact distance ties by numeric cell ID.

Pairing uses spatial/range metadata, never mismatch.

For outcome year t, predictive connectivity uses the preceding eight calendar years [t-8,t-1], requiring at least six paired years. The focal year t is never included. Source and target green-up series are separately detrended before rho is calculated.

Primary response:

    log(1 + abs(green-up day - bird arrival day))

Primary prediction: **z_connectivity coefficient < 0**. Stronger pre-existing route predictive connectivity should be associated with smaller realized arrival–green-up mismatch.

Support requires a negative estimate whose two-sided 95% interval excludes zero. A null remains a null: source-cell definition, 8-year window and primary response are frozen here.

## What this can and cannot establish

If either natural-data lane supports the registered direction, PAYOFF-B gains a positive empirical information-axis result in addition to the existing rejection of one universal speed ratio.

Neither lane alone demonstrates full hysteresis. The current hysteresis result remains synthetic until a system with observed deterioration and subsequent recovery of predictive connectivity is analyzed.

Evidence chain:

    partial-information game
    -> topology-dependent timing hysteresis
    -> natural predictive-connectivity effect
    -> future direct hysteresis test

The frozen 55-species speed-ratio result and all Aikens registrations remain unchanged.
