# PAYOFF-B mule-deer parameterization readiness receipt

Frozen: 2026-09-20

Status: **named system identified; calibration not yet licensed**.

This receipt evaluates whether the public data associated with Ortega et al.
(2023), *Migrating mule deer compensate en route for phenological mismatches*,
are sufficient to populate the PAYOFF-B migration-phenology model without
inventing parameters.

Primary article:

- Ortega, A. C. et al. 2023. Nature Communications 14:2008.
- DOI: 10.1038/s41467-023-37750-z.

Primary public dataset:

- Dryad DOI: 10.5061/dryad.8kprr4xsj.
- public file listing:
  - `Ortega_et_al_2023_Data.csv` (19.34 KB);
  - `README.md` (1.97 KB).
- the article also exposes a 614.3 KB Source Data XLSX.

## 1. Verified study scale

The article reports:

- 72 adult female mule deer;
- 152 animal-years;
- long-distance spring migrations of 134-293 km;
- GPS fixes every 1-2 h for 2014-2020 animals and every 3 h for a subset from
  2011-2013;
- migration starts ranging from about 70 days ahead to 52 days behind peak
  green-up;
- strong compensation during migration through movement-rate and stopover
  adjustment.

These observations make the system highly relevant to a movement-phenology
tracking model.

## 2. What the current public summary does identify

The published design supports the qualitative statement

    phase mismatch
    -> movement / stopover adjustment
    -> reduced mismatch by migration end.

The article reports that late migrants moved about 2.5 times faster and spent
about 72% less time on stopovers than early migrants.

This is direct evidence for state-dependent movement adjustment.

It is **not yet** the same estimand as the PAYOFF-B heritable tracking-rate
parameters.

## 3. Direct PAYOFF-B parameter status

### Migration rate m

Current status:

    NOT YET IDENTIFIED.

The movement layer now supports both symmetric and directional one-step
kernels on a fixed decision interval.

For a symmetric kernel the direct inverse uses component second moments with
negligible directional drift. For a directional kernel the raw GPS steps can
identify

    E[Delta x], E[Delta y],
    E[Delta x^2], E[Delta y^2]

after projection onto the declared climate axis, together with patch spacing d.

These moments identify migration rate, x/y movement weights, and x/y directional
biases under the declared biased nearest-neighbor kernel.

The article summary reports movement-rate contrasts, not the fixed-interval
projected step moments required by either exact inverse. Raw GPS trajectories or
an interval-level source table are therefore still required.

### x/y anisotropy

Current status:

    NOT YET IDENTIFIED.

The current exact map uses projected component second moments for the x/y
weights and projected component means for directional bias.

Route-level migration distance or group-average speed cannot substitute for
those fixed-interval moments.

### Climate-coordinate velocity v

Current status:

    NOT YET IDENTIFIED.

PAYOFF-B uses

    v = g c,

where g is the spatial environmental gradient and c is environmental-wave
speed on the same declared spatial/time scale.

The article demonstrates a propagating green wave and calculates Days-From-Peak
at GPS locations, but the summary values alone do not provide one frozen
route-level pair (g,c) in the model's units.

### Phenology response rate h

Current status:

    NOT YET IDENTIFIED ON THE MODEL TIME SCALE.

Published group summaries show strong phase compression, but that compression
is produced in part by movement-speed and stopover adjustment and therefore is
not automatically the independent timing-axis parameter h.

Several group means also cross zero between migration start and end. A sign
reversal is incompatible with the simple one-step monotone timing-axis inverse

    e_after = exp(-h) e_before.

For the late-migrant group, the published means move from about 20 days behind
peak IRG at migration start to about 11 days behind at migration end. The
whole-route ratio 11/20 is monotone, but it spans an entire migration rather
than one frozen decision interval. It therefore must not be inserted directly
as a per-generation PAYOFF-B h.

Individual or interval-level residual transitions are required, and h is only
licensed if the timing contribution is independently separated from movement
and other tracking pathways.

### Phenology limit z_max

Current status:

    NOT YET IDENTIFIED.

The observed range of starting phase errors is not the same object as the
maximum biologically feasible timing adjustment. A predeclared support for
realized timing shifts is required.

## 4. Fitness terms

The public movement summary does not identify:

- baseline low-density growth;
- abiotic mismatch strength A;
- interaction mismatch strength I;
- migration architecture cost c_m;
- phenology architecture cost c_h;
- joint cost c_mh.

The article reports foraging mismatch and movement behavior, not a common
low-density fitness scale under the orthogonal matched-contrast design required
by the exact PAYOFF-B inverse.

These terms must remain unfilled unless an independent fitness proxy and
matched contrasts are justified.

## 5. Data-ingestion blocker in the current environment

The Dryad landing page and file metadata are publicly accessible. The public
individual-file links resolve to:

    Ortega_et_al_2023_Data.csv
        Dryad file_stream ID 2189257

    README.md
        Dryad file_stream ID 2189258.

Direct retrieval of the CSV through the web tool returns HTTP 403, and the
container has no working external DNS path for a direct requests/curl fallback.
Therefore the current blocker is transport-level access to the public file,
not uncertainty about which file to ingest.

The Nature/PMC article also advertises a Source Data XLSX, but that file has not
yet been ingested into the repository.

Therefore the current stop is a **data-ingestion boundary**, not an inference
failure.

## 6. Next licensed step after file ingestion

Once the public source file is available locally:

0. run `python scripts/inspect_mule_deer_source_csv.py <csv>` and stop if the
   table is only animal-year summary grain;
1. inspect the README and column definitions;
2. determine whether records are animal-year summaries or interval-level
   movements;
3. freeze one decision interval;
4. project coordinates into declared metric x/y units;
5. rotate steps into climate-axis and transverse components;
6. estimate fixed-interval component means and second moments;
7. audit the symmetric kernel and, when directional drift is present, the
   directional kernel;
8. construct interval-level Days-From-Peak residual transitions;
9. treat phase compression as a movement/controller diagnostic unless the
   timing axis is independently isolated;
10. estimate route-specific green-wave speed and environmental gradient in
    compatible units;
11. run the interval and directional parameterization CLIs;
12. leave fitness terms unfilled unless matched growth contrasts are available.

## 7. Claim boundary

The mule-deer system is an empirical motivation and a candidate calibration
system.

This receipt does **not** claim that:

- the current PAYOFF-B movement kernel fits mule-deer GPS steps;
- published group-average phase compression identifies h;
- a 2.5-fold movement-speed contrast identifies migration rate m;
- green-wave surfing identifies interaction strength;
- the synthetic persistence frontier predicts mule-deer persistence.

The correct current status is:

    PUBLIC_SYSTEM_IDENTIFIED
    DIRECT_TRACKING_CALIBRATION_PENDING_SOURCE_FILE_INGESTION
    FITNESS_PARAMETERIZATION_NOT_IDENTIFIED
