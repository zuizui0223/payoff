# PAYOFF-B Ortega mule-deer phase-variance funnel result

Date: **2026-10-03**  
Status: **post-freeze descriptive source-data audit; frozen GEB V2 unchanged**

## Source and analysis state

Source:

Ortega AC, Aikens EO, Merkle JA, Monteith KL, Kauffman MJ (2023).
*Migrating mule deer compensate en route for phenological mismatches.*
Nature Communications 14:2008.
DOI: 10.1038/s41467-023-37750-z.

Public Source Data file:

\`41467_2023_37750_MOESM4_ESM.xlsx\`

Verified SHA256:

\`2645420b74c8e2228eb555d14c755bba207c49ea72ecb2eff4c950892f743364\`

The analysis was frozen after schema inspection but before computing the full
continuous numerical summaries in
\`data/payoff_b_ortega_variance_funnel_contract_20261003.json\`.

This is not an independent discovery of mule-deer compensation: the source
paper already established bidirectional compensation and route-level
resynchronization.

## 1. Continuous start-to-end phase funnel

The Source Data sheet
\`Fig1a,b;Fig3;SFig2;STables1,6\` contains 152 animal-years with paired
\`DFP_Start\` and \`DFP_End\`.

Across all animal-years:

| quantity | start | end |
|---|---:|---:|
| mean signed Days-From-Peak | -3.70 d | +7.00 d |
| SD | 26.41 d | 13.17 d |
| variance | 697.27 d² | 173.53 d² |
| mean absolute phase error | 21.91 d | 11.12 d |

The variance ratio is

\[
\boxed{
\frac{\operatorname{Var}(DFP_{end})}
{\operatorname{Var}(DFP_{start})}
=
0.2489.
}
\]

A 10,000-replicate bootstrap clustered by the 72 individual deer gives

\[
95\%\ CI=0.1667\text{--}0.3617.
\]

Thus the end-of-migration phase distribution has about one quarter of the
start-of-migration variance in this descriptive reconstruction.

## 2. Year-centering does not remove the funnel

To remove year-specific shifts in the mean green-wave phase, start and end
values were separately centered within year.

The resulting variance ratio is

\[
0.2940
\]

with animal-cluster bootstrap

\[
95\%\ CI=0.2060\text{--}0.4049.
\]

The funnel is therefore not explained simply by pooling years with different
mean phenology.

## 3. Continuous phase retention

The whole-route OLS slope is

\[
\lambda=0.10734
\]

with animal-cluster bootstrap

\[
95\%\ CI=0.0126\text{--}0.2085.
\]

This reproduces the existing PAYOFF-B mule-deer phase-retention coordinate.

After year centering,

\[
\lambda_{within-year}=0.09316
\]

with a wider cluster-bootstrap interval

\[
-0.0115\text{--}0.1994.
\]

Mean retention and variance contraction are deliberately kept as different
estimands.

## 4. Individual improvement

Of 152 animal-years,

\[
107/152=70.4\%
\]

ended closer to peak green-up in absolute phase than they started.

Animal-cluster bootstrap:

\[
95\%\ CI=62.3\%\text{--}77.8\%.
\]

This is a descriptive paired individual statistic, not a controller
identification test.

## 5. Signed actuator responses

The Source Data sheet \`Fig4d,4e;SFig4\` provides movement-rate and stopover
summaries joined by \`id_yr\`.

### Movement rate

Across 152 animal-years,

\[
\frac{d\,speed}{d\,DFP_{start}}
=
+0.06834
\ \mathrm{km\,d^{-1}\ per\ phase\ day},
\]

with animal-cluster bootstrap

\[
95\%\ CI=+0.05541\text{--}+0.07999.
\]

After within-year centering:

\[
+0.08517
\]

with

\[
95\%\ CI=+0.07107\text{--}+0.09852.
\]

Later start phase is therefore associated with faster travel.

### Stopover use

Among 127 animal-years with non-missing stopover duration,

\[
\frac{d\,stopover}{d\,DFP_{start}}
=
-0.4919
\ \mathrm{d\ per\ phase\ day},
\]

with animal-cluster bootstrap

\[
95\%\ CI=-0.5694\text{--}-0.4117.
\]

After within-year centering:

\[
-0.6137
\]

with

\[
95\%\ CI=-0.7002\text{--}-0.5215.
\]

Later start phase is therefore associated with shorter stopover use.

These are descriptive continuous reproductions of the signed compensation
reported by Ortega et al., not new causal effects.

## 6. What this adds to PAYOFF-B

The useful new object for PAYOFF-B is not the existence of compensation, which
is prior art. It is that the same individual-level public dataset contains all
three observable pieces needed for a strong prospective controller test:

\[
e_{in}
\rightarrow
\text{signed actuator response}
\rightarrow
e_{out},
\]

and it shows a large population phase-variance funnel across the same journey.

This makes the mule-deer system the strongest current natural anchor for the
route-wise control architecture.

## 7. What remains unidentified

The observed funnel does **not** by itself identify:

- the animal's internal phase estimate;
- checkpoint information weight \(K\);
- developmental/readiness gate \(G\);
- decision gain \(g\);
- effective correction gain \(h=Gg\);
- passive phase retention \(\phi\);
- process innovation \(Q\);
- Paper-2 actionability \(r\);
- effective deadline cost \(D_{eff}\).

A direct test of the new phase-sense inverse requires an independent passive
baseline or actuator contrast and an independent estimate of process/measurement
innovation.

Alternative contributors to the funnel include regression to the mean from
phase measurement error, passive phase dynamics, selective route completion,
and changing environmental variance.

## 8. Licensed conclusion

> **The Ortega source data show a robust continuous phase-variance funnel
> together with oppositely signed speed and stopover responses to starting
> phase. This strongly motivates an individualized feedback representation,
> but does not by itself identify the latent information/control parameters.**
