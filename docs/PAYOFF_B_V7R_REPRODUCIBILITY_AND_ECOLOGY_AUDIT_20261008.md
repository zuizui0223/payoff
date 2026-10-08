# PAYOFF-B V7R reproducibility and ecological audit

Date: 2026-10-08
Status: POST-OUTCOME AUDIT. The frozen 2026-10-07 result is preserved.

## Reproduction of the primary test

All four recovered Stage-3/ERA5 source archives have the retained SHA256
checksums. The dedicated V7R workflow originally failed because a pandas
namedtuple did not preserve the source column named lambda. This is now fixed
by retrieving columns by their names, with a regression test.

Source-to-result rerun:
- 10 transitions across three flyways
- 9 pre-existing lambda identities recovered within numerical precision
- beta_QR = +1.373337646185
- 2880 within-flyway permutations
- one-sided p = 0.569940992711

Primary decision remains NOT SUPPORTED.

## Explicit correction of the local one-step sensitivity

The archived diagnostic normalized local edge Q10-Q90 duration width by
the *maximum single-edge Q10-Q90 width within its flyway*:

    beta_QR = +0.024497731, p = 0.464769177.

The source-defined local sensitivity normalizes local duration width by
the *initial region's total remaining-route Q10-Q90 arrival window*:

    beta_QR = -0.012190381, p = 0.585213468.

The resulting difference is not rounding. Both metrics are now separately
reported by the source runner. Neither supports the hypothesized interaction.

The archived post-outcome receipt is not rewritten. Do not quote the archived
+0.0245 result as though it used the start-region denominator.

## Historical anomaly-slope sensitivity

Archived: beta_QR=+1.251975687, p=0.610898993.
Source rerun: beta_QR=+1.252008895, p=0.611940299.

The discrepancy is small and its historical origin is not fully identified.
Both results remain nonsignificant; preserve the two values rather than
silently replacing the old one.

The primary and the other inspected sensitivity paths reproduce, including
transition weighting, Q20-Q80 route-window definition, signed Pearson r,
r-squared, and ERA5 absolute correlation.

## Biological boundary

The response C=1-|lambda| is an observational phase-contraction score, not
a direct estimate of active correction gain. In the simplified PAYOFF model,
lambda=phi*(1-g), where phi is passive phase retention and g is active
feedback. Without independent phi, g cannot be recovered from lambda.

Exploratory direct actuator screens also do not establish the interaction:
- transition stopover gain: beta_QR=+0.441857, p_perm=0.750087
- weighted stopover gain: beta_QR=+0.232196, p_perm=0.767789
- ERA5-Q stopover gain: beta_QR=+0.774162, p_perm=0.593891
- 95-row incoming-phase x Q_forecast x R: estimate=-0.277659,
  p_perm=0.429712

Two contrasts illustrate the limits of a one-channel explanation:

Barents R1->R5: interregional phenology |r|=0.00238, lambda=-0.00857,
stopover_gain=0.787, n=10 transitions from 6 individuals.

Svalbard R2->R4: interregional phenology |r|=0.00148, lambda=-0.10632,
stopover_gain=0.589, n=16 transitions from 15 individuals.

Thus near-zero *historical interregional* forecastability can coexist with
strong phase contraction and signed stopover association. This does not prove
that geese used reliable local feedback cues or that behavioral action was
causally responsible for the contraction.

## Inference cautions

- Ten transition types give little independent support for a six-parameter
  model; permutations cannot manufacture independent replication.
- Permuting Q labels within flyway is exact enumeration, not proof of
  biological exchangeability. Shared climatic series and route geometry may
  violate exchangeability.
- Population-duration envelopes are observed group behaviors, not exogenous
  measurements of each bird's feasible actuator set.
- Individuals can contribute to multiple transitions, so estimated phase
  slopes and duration envelopes can share sampling variation.
- Historical cross-site environmental predictability is not necessarily
  the cue information the bird actually receives at a checkpoint.

## Stop rule and direction

Do not retune thresholds or re-open selected transitions to rescue the
failed positive forecast-predictability x generic-route-recourse prediction.

The next prospective biological test must distinguish independently:

1. forecast information available before commitment;
2. incoming mismatch before correction;
3. new local cue quality measured at the checkpoint;
4. signed behavioral action and independently estimated actionability;
5. downstream phase or fitness-relevant outcome.

Use genuinely untouched observations for this new test. The current archive
remains a non-confirmatory motivation, not evidence for a new substitution
mechanism.
