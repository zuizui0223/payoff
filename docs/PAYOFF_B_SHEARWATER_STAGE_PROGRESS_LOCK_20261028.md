# PAYOFF-B public shearwater experimental data: two-stage homing proxy

2026-10-28. Pre-GPS-outcome method. This is explicitly a secondary analysis
of the already published Pollonara et al. 2015 navigational experiment,
not a novel independently replicated experimental ecological claim.

The prechecked original Movebank CC0 source supplies 32 treatment-arm birds
(9 control, 9 magnet manipulation, 14 smell deprivation), but GPS was
originally fitted on 9/9/9; only 8/9/6 GPS records are available.
The preceding source-only measurement gate found 8/8/6 with continuous
0-12h and 12-24h observation windows.

Fixed endpoint: from first published GPS fix, measure homeward progress
per unit traveled distance in each 12h window. Use the midpoint of two
published study-colony coordinates at Pianosa (42.576 N, 10.0985 E).
Index = (great circle distance to the colony at window start minus
distance to colony at window end) divided by original GPS path length.
An index lies in [-1,+1], and late-minus-early positive is binary
source directional improvement, NOT proven feedback or return to home.

Predeclared restrictions: both windows passed original fixed GPS gate;
at least 6 GPS timestamps each, at least 20 km GPS path per segment,
no GPS step >100 km/h, first window starts ≥100 km from published
colony, late window starts ≥20 km from colony. Reject rather than relabel
unmeasurable GPS as a failed behavioral correction.

Original group missingness is nonrandom and instrument allocation is
different by treatment. Sharp, assumption-free bounds of the fraction
with positive late-minus-early change across ALL original subjects:
success/n <= population fraction <= (success + n - assessable)/n.
Bound each treatment-vs-control difference by opposing endpoints.
Report analogous bounds within the original nine GPS-equipped/group.
No experimental causal identification is asserted: treatment
randomization is unverified here, the group-assigned GPS/Argos
modalities are not exchangeable, and missingness cannot be assumed
ignorable.

The original paper already established olfactory/coastal navigation
effects. This metric is a measurement calibration and MAY overlap
the published route-effect endpoints. The first GPS fix is not a
certified release moment; the windows do not identify where/when
odour or coastline cues became available. No source bird ID, exact
GPS location/time, route, ring or individual outcome is exported.

Needed for PAYOFF-B novelty: new independent experiments measuring
predecision cue access, prospective feasible correction and later
phenological/fitness outcomes.
