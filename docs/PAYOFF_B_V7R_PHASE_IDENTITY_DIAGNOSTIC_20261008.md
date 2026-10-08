# PAYOFF-B V7R: post-outcome kinematic decomposition of phase retention

Date: **2026-10-08**  
Status: **DESCRIPTIVE POST-OUTCOME DIAGNOSTIC — NOT A NEW HYPOTHESIS TEST**

## Why this audit exists

The frozen V7R primary result was not supported:

- 10 migration transition types across Greenland, Svalbard and Barents flyways
- \(\widehat\beta_{QR}=+1.373337646\)
- 2,880 within-flyway Q permutations
- one-sided \(p=0.569940993\)

The registered response was

\[
C_e=1-|\lambda_e|,
\]

where \(\lambda_e\) is the OLS slope from incoming phase error to subsequent
arrival phase error.

This is an **observed phase-retention** measure. It does not identify a
behavioral correction gain.

The following identity separates three sources of observed phase change without
using the Q×R result to select routes or change the original outcome.

## Exact kinematic identity

For a fixed pair of regions \(j\to k\), define:

- \(A_j\), \(A_k\): observed arrival dates
- \(S_j\), \(S_k\): seasonal onset coordinates at those regions
- \(e_j=A_j-S_j\), \(e_k=A_k-S_k\): arrival phase errors
- \(d_\mathrm{stop}\): time spent at origin
- \(d_\mathrm{transit}\): time travelling to destination

Given the observed transition chronology,

\[
A_k=A_j+d_\mathrm{stop}+d_\mathrm{transit}.
\]

Therefore:

\[
e_k=e_j+d_\mathrm{stop}+d_\mathrm{transit}+(S_j-S_k).
\]

Taking the OLS slope with intercept against \(e_j\) gives the exact identity:

\[
\boxed{
\lambda_{jk}
=
1
+
b_{\mathrm{stop},jk}
+
b_{\mathrm{transit},jk}
+
b_{\mathrm{season},jk}
}
\]

with each \(b\) the observed within-transition OLS slope of that term against
origin phase error.

**This is algebra / covariance bookkeeping, not causal identification.**

In the Greenland and Barents Stage-3 anomaly construction, regional constant
phenology anchors affect regression intercepts, not these fixed-transition
slopes.

## Source fidelity

The audit uses exactly the two frozen Stage-3 tracking archives:

- Greenland+Barents: SHA256
  \`8e720be44e0ef2e3e497786c9241c6625b4b14c46506fbb30ea027dcdf36749f\`
- Svalbard: SHA256
  \`29558f9b8b43a7375b3922118a77b74464558f4869a7722472570a32745f2856\`

There are ten admitted edges under the pre-existing V7R criterion of at least
five observed transition rows. None has been added, dropped or relabelled to
optimize the decomposition.

Reconstruction:

- maximum absolute identity error per individual-transition: below
  \(5\times10^{-14}\) days;
- maximum absolute regression-slope identity error: below
  \(6\times10^{-16}\);
- all ten reconstructed values agree with the archived \(\lambda\) values.

## Components by transition

All numbers below are slopes; the observed \(\lambda\) is
\(1+b_{\mathrm{stop}}+b_{\mathrm{transit}}+b_{\mathrm{season}}\).

| Flyway | Edge | n | b_stop | b_transit | b_season | lambda |
|---|---|---:|---:|---:|---:|---:|
| Barents | R1→R2 | 12 | −0.5915 | +0.0069 | +0.0786 | +0.4941 |
| Barents | R1→R5 | 10 | −0.7870 | +0.0194 | −0.2410 | −0.0086 |
| Barents | R2→R3 | 6 | −0.3320 | −0.0064 | −0.1232 | +0.5384 |
| Barents | R3→R5 | 6 | −0.2205 | +0.0492 | −0.6041 | +0.2245 |
| Barents | R4→R5 | 7 | +0.0903 | −0.1095 | +0.2685 | +1.2492 |
| Barents | R5→R7 | 7 | −0.5105 | −0.0850 | +0.4283 | +0.8329 |
| Greenland | R1→R2 | 7 | +0.2722 | −0.7607 | −1.5914 | −1.0799 |
| Greenland | R2→R3 | 6 | −0.5242 | −0.0170 | −0.3281 | +0.1307 |
| Svalbard | R1→R2 | 18 | −0.9102 | +0.0415 | −0.0609 | +0.0704 |
| Svalbard | R2→R4 | 16 | −0.5890 | +0.0152 | −0.5325 | −0.1063 |

Across ten focal transitions, the stopover slope is negative in 8 and the
interregional-season slope is negative in 7.

## What becomes biologically more precise

### Low environmental forecastability does not identify zero correction

The V7R Q coordinate is historical cross-region predictability:

\[
Q_{jk}=|\operatorname{corr}(S_j,S_k)|.
\]

For two striking examples, published into the previously opened V7R result:

- Barents R1→R5: \(Q=0.00238\), \(\lambda=-0.00857\)
- Svalbard R2→R4: \(Q=0.00148\), \(\lambda=-0.10632\)

The new identity clarifies that their near-zero phase retention involves both a
negative stopover-duration covariance and an interregional seasonal covariance.
They do **not** uniquely demonstrate reaction to local cue information.

### Flight/transit speed is not the sole route for temporal convergence

Transit-duration contributions are positive on five links and negative on five.
Strong phase contraction in the examples above is associated descriptively with
stopover-duration relationships and seasonal differences rather than a uniquely
large signed transit component.

### An observed stopover slope is still not a feedback-control coefficient

If departure happens on a nearly fixed calendar date, earlier arrivals will
wait longer. This alone can produce a strong negative regression of stopover
duration on arrival phase, even without any active use of phenological cues.

To call a stopover slope "reactive correction", a subsequent design must
separate cue perception from the calendar schedule and other drivers.

## Critical claim boundary

Do not claim:

- \(b_{\rm stop}\) is a causal feedback gain;
- \(b_{\rm season}\) is purely stochastic rather than potentially linked to
  geography, onset estimation, or shared climate history;
- this descriptive decomposition rescues the failed V7R Q×R interaction;
- this elementary kinematic identity is a novel mathematical theorem.

Safe:

> The ten focal barnacle-goose transitions exhibit heterogeneous observed
> phase retention that decomposes exactly into covariances with origin
> stopover duration, transit duration, and interregional spring timing. The
> decomposition demonstrates why phase contraction cannot be interpreted as
> active correction without further identification.

## Reproducibility

Implementation:

- \`src/v7r_phase_identity.py\`
- \`scripts/audit_v7r_phase_identity.py\`
- \`tests/test_v7r_phase_identity.py\`

Run the script on the two source archives and retain its CSV and JSON
diagnostics separately from the frozen V7R primary result.

The next confirmatory test must use an independent/untouched natural system
with pre-commitment information, perceived incoming phase, actual local cues,
observable feasible action and downstream consequences. The already exposed
V7R panel must not be repurposed as a fresh confirmation of forecast–correction
substitution.
