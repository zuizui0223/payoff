# Svalbard barnacle-goose phenology calibration receipt

Status: environmental reconstruction contract for the direct Svalbard controller analysis.

## Why calibration is required

The public-GPS reconstruction recovers the expected four broad Svalbard-flyway regions:

~~~text
R1  Scotland / Solway Firth       ~54.95 N,  -3.33 E
R2  southern Norway / Helgeland   ~66.33 N,  12.21 E
R3  northern Norway / Vesterålen  ~69.20 N,  16.06 E
R4  Svalbard                      ~77.60 N,  15.44 E
~~~

A reproducible modern environmental reconstruction uses NASA POWER daily T2M and the van-Wijk-style GDD-jerk transform.

The logistic GDD fits themselves are excellent:

~~~text
minimum annual fit R2 across regions > 0.99
~~~

but the 1982–2011 absolute mean onset from POWER is biased at high latitude.

Raw reconstructed means:

~~~text
R1  81.89
R2  84.00
R3  99.86
R4 133.15
~~~

The original Kölzsch et al. study reports:

~~~text
Scotland mean onset     26 March  ~ DOY 85
Svalbard mean onset     16 June   ~ DOY 167
~~~

Therefore raw POWER differs by only about -3 days at R1 but by about -34 days at R4.

This is a data-source calibration problem, not a failure of the numerical sigmoid/GDD implementation.

## Registered solution

Use POWER only for **annual anomalies**, not for absolute regional phase:

\[
A_{r,y}
=
T^{POWER}_{r,y}
-
\overline{T}^{POWER}_{r,1982:2011}.
\]

Then reconstruct annual onset as

\[
T^{cal}_{r,y}
=
\mu^{anchor}_r
+
A_{r,y}.
\]

This preserves year-to-year timing information while removing region-specific absolute bias.

## Mean-onset anchors

### Explicit article anchors

~~~text
R1 Scotland  = DOY 85
R4 Svalbard  = DOY 167
~~~

These correspond to the article's explicit mean dates.

### Norwegian anchors

The Wiley supplement containing exact Table S1 values is currently blocked to automated download by HTTP 403.

The main article Figure 3 provides the 30-year onset boxplots. Conservative visual central readings are registered as:

~~~text
R2 southern Norway = DOY 118
R3 northern Norway = DOY 130
~~~

These are **not treated as exact published table values**.

Sensitivity is mandatory:

~~~text
R2 = 113, 118, 123
R3 = 125, 130, 135
~~~

for all 3 x 3 = 9 combinations.

No result depending on a particular Norwegian anchor is licensed unless its qualitative sign survives this grid.

## What is anchor-invariant or nearly anchor-invariant

Within one fixed origin region, adding a constant offset to onset shifts all phase errors equally.

Therefore the slope of

\[
\log c_{animal}
\sim
E
\]

is insensitive to a pure phase-origin shift.

This **behavioral speed gain** is the most robust controller quantity.

By contrast,

\[
u = c_{animal}/c_{environment}
\]

also uses between-region environmental propagation speed, so its magnitude can depend on anchor differences. Relative-speed gain is therefore reported with the full anchor-sensitivity grid.

Stable phase \(E_*\) and correction distance \(\ell\) are not promoted unless the environmental calibration is sufficiently constrained.

## Independent checks

The original article states that on the Svalbard route:

~~~text
all consecutive onset correlations were high:
  0.45 < r < 0.81

southern -> northern Norway:
  proportionality index s = 0.85

northern Norway -> Svalbard:
  proportionality index s = 0.48
~~~

The POWER-anomaly reconstruction is used as a modern proxy, not an asserted reproduction of those historical ECA/NOAA correlations.

## Interpretation ceiling

Licensed:

- POWER GDD jerk can supply annual anomaly structure;
- absolute high-latitude POWER onset needs calibration;
- explicit article means anchor Scotland and Svalbard;
- figure-derived Norwegian means can be used only with registered sensitivity;
- behavioral-speed feedback is prioritized over absolute controller equilibrium.

Not licensed:

- claiming R2=118 or R3=130 as exact Table S1 values;
- claiming the POWER reconstruction reproduces the original climate dataset;
- promoting \(E_*\) or \(\ell\) from Svalbard geese without sensitivity support.

If the exact supplementary Table S1/S2–S7 becomes accessible, it supersedes the figure-derived anchor grid.
