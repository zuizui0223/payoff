# PAYOFF-B mule-deer readiness result

Date: **2026-10-03**  
Status: **post-freeze source-data analysis; frozen GEB V2 unchanged**

## Question

Can the Ortega mule-deer system supply evidence for the
**developmental/physiological readiness clock** in the same population that
already supplies strong signed decision-feedback evidence?

The source article states that nutritional condition was measured as
**% scaled IFBFat in March** and was included in the model for timing of spring
migration.  The public Source Data workbook contains both that physiological
measure and migration timing by animal-year.

Because the workbook does not provide exact March capture dates, the analysis
was frozen before outcome inspection to use only animal-years whose spring
migration began **strictly after March 31**.  In those rows, any March
measurement necessarily preceded migration start.

## Source

Ortega et al. (2023), *Nature Communications* 14:2008.  
DOI: 10.1038/s41467-023-37750-z.

Verified Source Data SHA256:

\`2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364\`

Relevant sheets:

- readiness: \`SFig1\`
- raw migration timing: \`Fig1a,b;Fig3;SFig2;STables1,6\`

## Temporal-order gate

The readiness sheet contains **93** joinable animal-years with
\`scaledIFBFat\` and standardized migration start.

After requiring raw \`DOY_Start\` to occur after March 31 of that year:

\[
n=62\ \text{animal-years},
\qquad
40\ \text{individual deer}.
\]

Thirty-one animal-years were excluded because migration began during or before
March, so temporal ordering relative to the unspecified March capture day could
not be guaranteed.

## Primary result

In the temporally safe subset,

\[
\frac{d\,\text{standardized migration start}}
{d\,\text{scaled IFBFat}}
=
-3.971
\ \text{d per IFBFat unit}.
\]

A 10,000-replicate bootstrap clustered by animal gives

\[
95\%\ \mathrm{CI}
=
[-6.305,\,-0.686].
\]

Thus higher March nutritional condition is associated with earlier subsequent
spring-migration initiation in this conservative subset.

The ordinary Pearson association is

\[
r=-0.337.
\]

## Robustness and caveats

All 40 leave-one-animal-out fits retain a negative slope:

\[
-4.80
\le
\hat\beta_{\mathrm{LOAO}}
\le
-3.43.
\]

However, the sensitivity that additionally residualizes both IFBFat and start
timing by year gives

\[
\hat\beta_{\mathrm{year-FE}}
=
-2.138,
\]

with cluster-bootstrap

\[
95\%\ \mathrm{CI}
=
[-6.894,\,+1.579].
\]

The Spearman sensitivity is also weaker:

\[
\rho=-0.274,
\qquad
95\%\ \mathrm{bootstrap}
=
[-0.521,\,+0.001].
\]

The readiness association is therefore robust in the frozen primary slope and
leave-one-animal-out analysis, but it should **not** be described as invariant
to every year-structure or rank-based sensitivity.

## Two-clock interpretation

The same mule-deer population already supplies D2-level evidence for the
decision clock:

- incoming signed Days-From-Peak error;
- later phase -> faster movement;
- later phase -> shorter stopovers;
- bidirectional compensation in the source study;
- strong start-to-end phase-variance contraction.

The new analysis adds a temporally prior internal physiological state:

\[
\text{March IFBFat}
\rightarrow
\text{migration-start timing}.
\]

Under the predeclared evidence grades, this licenses

\`\`\`text
TIMER = T3_CANDIDATE
DECISION = D2
HYBRID = H1_CANDIDATE
\`\`\`

for mule deer.

This is the first current PAYOFF-B natural system in which evidence for a
pre-event physiological readiness variable and signed downstream behavioral
correction coexist in the same population.

## What is not established

The analysis does **not** show that:

- IFBFat is a molecular clock;
- IFBFat is itself the readiness gate \(G\);
- readiness directly gates the phase-to-action slope;
- \(G,K,g,\phi,Q\) are separately identified;
- the two clocks have been jointly estimated at the same route checkpoint.

In particular, **H2 is not licensed**.  H2 requires a separate test showing
that signed feedback depends on independently measured readiness, for example a
predeclared phase-error × readiness interaction with the relevant actuator
available on both sides of the gate.

## Licensed conclusion

> **In a temporally conservative subset of the Ortega mule-deer source data,
> March nutritional condition predicts subsequent migration-start timing, while
> the same population independently exhibits signed en-route correction.
> This supports a candidate hybrid architecture in which physiological
> readiness and decision feedback coexist, but does not yet show that readiness
> gates the feedback controller.**
