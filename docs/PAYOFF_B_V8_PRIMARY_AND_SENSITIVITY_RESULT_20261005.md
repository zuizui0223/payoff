# PAYOFF-B V8 primary + mandatory-sensitivity result receipt — 2026-10-05

Status: **PRIMARY DEGRADATION HYPOTHESIS NOT SUPPORTED; OBSERVED CHANGE IS STRONGLY POSITIVE**

This receipt records the already-opened V8 environmental result and the
mandatory sensitivities executed under the postprimary implementation lock.
No bird timing, mismatch, migration-speed or fitness outcome is used here.

## Primary V8 result

Frozen comparison:
- early window: 2002–2009;
- late window: 2010–2017;
- detrended source-destination mid-green-up correlation;
- delta-rho = rho_late - rho_early;
- inferential unit: unique spatial source-target pair;
- dependency-aware pair bootstrap: 10,000 resamples, seed 20261005.

Finite sample:
- 166 unique spatial pairs;
- 28 species;
- 26 species with at least 3 pairs.

Observed result:
- unique-pair mean delta-rho = **+0.3690**;
- 95% pair-bootstrap interval = **+0.2984 to +0.4365**;
- equal-species exposure mean delta-rho = **+0.3364**;
- 95% dependency-aware bootstrap interval = **+0.2628 to +0.4312**;
- 26/28 species means are positive;
- 2/28 species means are negative.

Frozen primary status:

`V8_BROAD_DEGRADATION = NOT_SUPPORTED`

The preregistered claim that source-destination spring predictive connectivity
broadly weakened is therefore rejected under the frozen definition. The
opposite descriptive pattern is strong: the sampled source-destination
green-up relationships became more positively correlated between the two
periods.

This opposite direction does **not** retrospectively redefine the primary
hypothesis or support rule.

## Mandatory sensitivities

| sensitivity | result |
|---|---|
| Fisher-z scale | unique-pair mean delta-z = **+0.6543**, 95% CI **+0.5457 to +0.7594**; equal-species = **+0.6893**, CI **+0.5718 to +0.8421** |
| exact complete 8-year windows | 58 pairs / 21 species; mean delta-rho = **+0.4137**, CI **+0.2807 to +0.5419**; equal-species = **+0.3909**, CI **+0.2860 to +0.4853** |
| target-cell equal weighting | equal-species mean = **+0.3364**, CI **+0.2628 to +0.4312**; numerically identical to the primary equal-species exposure summary because the frozen mapping assigns one source to each species-target cell |
| source-target distance moderator | slope on standardized log1p distance = **+0.0247**, bootstrap 95% CI **-0.0375 to +0.0851**; no clear distance gradient |
| migration-distance class | **NOT ESTIMABLE** as a useful moderator: the frozen Amaral stopover-distance table overlaps only **2/28** V8 species (source-table median = 2930 km) |
| leave-one-species-out | all **28/28** omissions keep the unique-pair mean positive; range **+0.3547 to +0.4246**. All **28/28** omissions also keep the equal-species mean positive; range **+0.3138 to +0.3820** |
| raw undetrended correlation | unique-pair delta = **+0.4486**, CI **+0.3793 to +0.5165**; equal-species = **+0.3756**, CI **+0.3126 to +0.4716** |
| alternative 7-year windows | 96 pairs / 25 species; mean delta-rho = **+0.3993**, CI **+0.3030 to +0.4977**; equal-species = **+0.3318**, CI **+0.2349 to +0.4276** |
| positive-to-nonpositive sign reversal | **7/166 = 4.22%** |

## Robustness conclusion

The positive change is not an artefact of:
- the raw-r versus Fisher-z scale;
- incomplete 8-year windows;
- target-cell/species weighting;
- one influential species;
- year detrending;
- the exact 2009/2010 window split.

No clear evidence was found that the positive change varies with
source-target geographic distance.

The migration-distance-class sensitivity is underpowered by source coverage and
must not be interpreted as either positive or negative evidence.

## Licensed interpretation

The data support the following descriptive statement:

> Across the sampled source-destination spring relationships used by migratory
> bird species in the Amaral eastern-North-America system, interannual
> source-destination green-up coupling was stronger in the later period than in
> the earlier period under the frozen V8 definition.

The result does **not** by itself establish:
- anthropogenic climate change as the cause of the strengthening;
- that birds perceive or use the fitted correlations;
- that phenological mismatch improved;
- that migration fitness improved;
- that all environmental information became more reliable;
- a universal increase in climatic connectivity across migration systems.

## Consequence for the PAYOFF-B story

The original proposed headline — climate change is degrading the information
used to anticipate spring — is not supported by V8 and should be removed.

A different question is now empirically motivated but remains untested by V8:

> If environmental predictive connectivity strengthened, did migratory timing
> actually capitalize on that extra predictability?

That is a downstream environment-to-bird transfer question. It requires a
separate locked analysis and cannot be inferred from the environmental result
alone.

## Provenance

Primary workflow:
- run: 37285260343
- job: 111682534844
- artifact: 11334053847
- artifact SHA256: e54a2c835a33f6b99fad1de13add2cace7d7f6973d2c2355c46b0fed6a832ec0

Mandatory-sensitivity workflow:
- run: 37288778237
- job: 111693980867
- artifact: 11335287675
- artifact SHA256: c0d346d1caf3d1993e3d75c342b3cd5c9519affb700b7aa636f31c85954318d7
