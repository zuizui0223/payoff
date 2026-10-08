# PAYOFF-B: can successful past experience become a liability?

Date: 2026-10-08. Status: PROSPECTIVE hypothesis and source audit, not new empirical evidence. Stacked on PR #314 and #311; V7R/V8 frozen outcomes unchanged.

## Question

Can a historically accurate migrant cue-to-spring forecast become inferior to a noisy but genuinely refreshed source after a climatic regime shift, EVEN IF cross-site spring correlation becomes stronger? This is a possible source-of-knowledge reversal, not evidence of maladaptation in any real species.

## Model: exactly specified toy counterexample

Earlier destination spring H_old = rho_0*X + sqrt(1-rho_0^2)*eps.
Later H_new = delta + rho_1*X + sqrt(1-rho_1^2)*eps, with X and eps independent standard normal.

Historical learned policy u_memory = rho_0*X.
Freshly calibrated hypothetical policy u_fresh = delta + rho_1*X + zeta, with independent forecast noise var(zeta)=sigma^2 and direct acquisition cost c>=0 in expected squared-timing-loss units.

Expected later policy losses:

    Loss_memory = 1 - rho_1^2 + delta^2 + (rho_1-rho_0)^2
    Loss_fresh = 1 - rho_1^2 + sigma^2 + c

The fresh policy becomes better if and only if:

    delta^2 + (rho_1-rho_0)^2 > sigma^2+c.

Earlier, in a stationary environment, memory is better by sigma^2+c if both sources had the same underlying calibration.

Synthetic witness: rho_0=.3, rho_1=.8, delta=1, sigma^2=.25, c=.10. Earlier experience advantage 0.35. After shift Loss_memory=1.61, Loss_fresh=.71, difference +0.90. Cross-site correlation rose; stale forecast still became worse.

This is elementary expected-loss and distribution-shift algebra, NOT novel Bayesian theory, observed animal behavior, or demographic fitness. Both decisions assume equal unrestricted action sets, no additional biological recourse differences and the stated quadratic loss. PR #314 models bounded action sets separately.

## Actual sources checked

Abrahms et al. 2021 Nature Communications 12:7326 (doi:10.1038/s41467-021-27626-5) follows 105 reintroduced whooping cranes across 16 years and already reports an ontogenetic transition from social to experiential learning, plus environmental migration-speed responses. Those effects are prior art, NOT payoff findings.

Original public code repository https://github.com/briana-abrahms/CraneMigrationSpeed has only README.md and crane_migration_speed_Github.r; the script reads crane_data.csv, which is NOT in that repository. Published movement-data archive DOI: https://doi.org/10.5441/001/1.t23vm852. The source-data package contents were not downloaded or audited here.

The original script models daily northward speed using snow depth, NDVI, bird age, social group experience, calendar day, individual/group/year effects. These variables are observational and can reflect immediate local effects, not only predictions about future destinations. Day-by-day environment annotation does not establish the exact date that a bird acquired destination-relevant information.

Teitelbaum et al. 2016 Nature Communications 7:12793 had already studied experience-driven new migration routes and shortstopping; this cannot be framed as a novel first discovery.

Jonzén et al. 2007 Proceedings B (https://pmc.ncbi.nlm.nih.gov/articles/PMC1685845/) already demonstrated that fitness-optimal arrival may undertrack a shifting food peak even with adequate information.

## Source-only feasibility gates and result

- Existing literature / age-by-group structure: PASS as a potential source for a follow-on study.
- Actual movebank event and social-group table: HOLD (DOI exists, but not retrieved and checked).
- Available origin/checkpoint forecast information before an irreversible behavioral choice: HOLD.
- Independent distant destination seasonal target with enough training and untouched year support: HOLD.
- Distinguishable usage of individual experience versus genuinely fresh group information: HOLD.
- Independently measured actionability, cost and fitness: HOLD.

In particular, DO NOT assign old memory to adult cranes or fresh information to young cranes purely on age: group leaders can share outdated knowledge and adults can update.

## Prospective biological discrimination

Freeze a historical window and later untouched seasons without reading behavioral responses. (1) Estimate historical-to-current calibration shift of destination phenology, testing intercept and slope rather than only signed correlation. (2) Estimate the independent, pre-action content of a social/checkpoint cue conditional on origin information. (3) Compare genuinely historical and freshly updated action predictions for the same individual, with observed action timing and direct local environment, photoperiod, group, age and individual effects. (4) Measure remaining physically feasible action, rather than estimating it from phase slopes. (5) Test whether a change in timing improved actual synchrony and, if possible, reproduction/survival.

Test competing nulls: no calibration drift, no conditional new cue, stale socially copied information, revised adult memory, zero recourse, fixed calendar, direct temperature/wind/forage forcing, and optimally costly undertracking. Failure to distinguish any decisive alternative caps interpretation. Merely observing an age interaction is not identifying evidence.

Novelty claim ceiling: a future real-data result could show WHEN experience-based timing cues reverse value under environmental change, with independent cue uptake and behavioral/fitness outcomes. This note does not yet demonstrate it and does not create another submission manuscript.
