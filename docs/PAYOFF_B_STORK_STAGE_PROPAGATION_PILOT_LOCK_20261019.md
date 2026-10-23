# PAYOFF-B pre-fit pilot: stagewise phenological timing propagation in white storks

Date: 2026-10-19. Status: **LOCKED BEFORE ANY WITHIN-YEAR T20→T80 REGRESSION**.

Source: Rotics et al. (2018), DOI 10.5441/001/1.v8d24552
(article: 10.1111/1365-2656.12898); original GPS checksum
bda2ebd2441316b2e2fd9e9578d7d0b4.

**Biological object:** observational propagation of relative spring northward
movement timing along a route, not actual breeding arrival or cognitive
environmental information. This is a *source calibration* for a future
cross-study macroecological question, not a novel confirmatory reanalysis
of the original Rotics paper's departure, arrival, speed or fecundity results.

## What was known before this registration

Original full 2012–2016 stork GPS with 1,207,130 events links to 91 breeding
animal-years. An outcome-blind latitude geometry screen admitted exactly
53 animal-years (27 individuals; 15 repeat individuals) with first 20% and
80% northward-progress crossings in March-April. It reported marginal
median passage times and the median 20%-80% span (22 days), but it did
**not** calculate covariance, regression, variance-retention, or a bird
reproductive endpoint. This is the actual inference novelty boundary.

## Frozen estimand, dataset and test

- Preserve *exactly* the 53 originally admitted animal-years from the frozen
  source-only latitude screen; do not change thresholds or drop unusual
  seasons after seeing slope.
- Each date is normalized to a **365-day calendar** (subtract one day
  for leap-year March-April dates after February 29). Thus 2012 and 2016
  are not automatically misaligned by calendar coding.
- X = day of crossing 20% of the declared northward latitude progress.
- Y = day of crossing 80% of the same trajectory.
- Fit Y ~ X + calendar-year fixed effects, with an intercept. The primary
  descriptive phase-propagation slope is beta_X.
- Retain original units (days/day). beta_X <1 is **temporal compression**
  of *observed route-stage timing variation* under this proxy definition.
  beta_X >=1 is no compression or amplification.
- Cluster-bootstrap animals with replacement (2,500 iterations,
  fixed random seed 20261019), retaining every year for a sampled animal;
  report unweighted 95% percentile interval.
- Admission: >=40 animal-years, >=20 distinct animals and >=4 observation years,
  and finite nonsingular year-FE design. Otherwise NOT_ESTIMABLE; no
  threshold relaxing.
- A one-sided directional pilot support label is allowed only if the observed
  slope <1 and **bootstrap 95% upper bound <1**. All other outcomes are
  NOT_SUPPORTED or NOT_ESTIMABLE, not rescued by secondary metrics.

## Prespecified diagnostics and negative controls

1. Repeated-animal-only within-individual centered X/Y slope, if at least
   10 animals have 2+ admitted years. This is descriptive and not a
   separate confirmatory test.
2. Leave-one-animal-out slope range for every admitted individual.
3. Within-year shuffled X (1,000 permutations) as a *model calculation*
   null, not a biological randomization experiment.
4. Refit using raw leap-year DOY to quantify and disclose the calendar
   correction effect, not to select a favorable version.
5. Report per-year admitted counts and per-year X/Y quantiles; do not select
   dates/windows after fitting.

## Biological claim ceiling

Even a supported beta_X <1 does NOT identify:
- active phase feedback (passive phase dynamics and selective arrival remain);
- compensation cost, stage opportunity, or recourse;
- environmental cue reliability or cue use;
- complete breeding arrival or arrival-greenup mismatch;
- survival/reproductive fitness rescue;
- a novel ecological result beyond prior migration-stage timing literature.

The chosen 20%/80% checkpoints use the individual's eventual spring
latitude distribution, so the timing variable is retrospective, not
an information signal available at the first checkpoint. Restriction to
March-April can produce left/right censoring. A result is therefore
**pilot descriptive stage timing**, requiring replication in genuinely
independent species/studies and cue chronology before theory promotion.

Under no circumstances should fledgling counts be joined to this pilot
after seeing the timing slope without a separate study design and novelty
audit. Keep V7/V8 registered nulls unchanged.
