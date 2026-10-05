# PAYOFF-B V8 — frozen sensitivity result

Date: **2026-10-05**  
Status: **OPPOSITE-DIRECTION PRIMARY RESULT ROBUST**

Primary result:
`docs/PAYOFF_B_V8_PREDICTIVE_CONNECTIVITY_DEGRADATION_RESULT_20261005.md`

Workflow:
- run `37281691204`
- artifact `11332508224`

## Prespecified sensitivities

All available mandatory sensitivities retained the positive early-to-late
change in signed predictive connectivity.

```text
FISHER_Z_MEAN_CHANGE = +0.729058
FISHER_Z_SE = 0.033910

EXACT_8_OF_8_PAIR_COUNT = 178
EXACT_8_OF_8_MEAN_DELTA_RHO = +0.391692

SPECIES_EQUAL_WEIGHT_MEAN_DELTA_RHO = +0.336355

RAW_UNDETRENDED_MEAN_CHANGE = +0.419293

ALT_7_YEAR_WINDOWS = 2002-2008 vs 2011-2017
ALT_7_YEAR_PAIR_COUNT = 260
ALT_7_YEAR_MEAN_DELTA_RHO = +0.332582

LOO_PAIR_MEAN_RANGE = [+0.341416, +0.377513]
LOO_SPECIES_MEAN_RANGE = [+0.313820, +0.381989]
```

No single species reverses the broad direction.

## Distance moderator

The prespecified geographic-distance sensitivity gave:

[
\widehat\beta_{distance}=+0.10798
]

per one SD of log source-target distance,
SE (=0.02485), (p=1.81\times10^{-5}).

Thus the observed strengthening was larger, not smaller, across more distant
frozen source-target mappings.

This is a secondary moderator and is not interpreted as a causal mechanism.

## Migration-distance-class sensitivity

No compatible migration-distance-class field was present under the frozen
source-column audit used by this executor. This sensitivity is therefore
recorded as **UNAVAILABLE**, not replaced by a new external trait source after
outcome access.

## Conclusion

The preregistered V8 degradation prediction is robustly unsupported.

The later period shows stronger source-to-target green-up covariation under:
- signed detrended rho;
- Fisher-z;
- complete 8/8 windows;
- raw undetrended correlation;
- alternative non-overlapping seven-year windows;
- species equal weighting;
- every leave-one-species-out analysis.

No V8 sensitivity is used to redefine the primary question.

The environmental strengthening itself is not promoted as a new generic
climate-synchrony discovery; increasing spatial synchrony of spring vegetation
phenology under climatic warming is already represented in the broader
phenology literature. The V8 value is the direct falsification of broad
predictive-connectivity degradation under the frozen migratory-route mapping.
