# PAYOFF-B greater snow goose raw-GPS access gate

Date: **2026-09-29**  
Status: **RAW_GPS_ACCESS_NOT_ESTABLISHED**

The preregistered cue-uptake analysis targets Movebank study **1442516400**
("Greater snow goose migration").

The public Migratory Bird Initiative study table exposes the study at
**summary** visibility and reports 2019–2023, 75 animals, 5,156,264 valid
locations and GPS sensors. That public summary is enough to define the
prospective sample frame but is not evidence that raw event data are
anonymously downloadable.

The independent Zenodo reproducibility archive
(DOI **10.5281/zenodo.20686134**) includes the analysis framework and
species-specific reproducibility materials, but explicitly does **not**
redistribute the Greater Snow Goose raw data; it instructs users to obtain
those data from Movebank.

Therefore the current status is deliberately neither `NOT_ESTIMABLE` nor
`NOT_SUPPORTED`.

```
PREOUTCOME_REGISTERED
    +
EXECUTION_CODE_READY
    +
RAW_GPS_ACCESS_NOT_ESTABLISHED
    ->
NO_OUTCOME_OPENED
```

Once an authorized Movebank export is available, the frozen pipeline is:

1. pinned `movepp` preprocessing;
2. geometry-only south/mid/north shared context assignment;
3. day-risk construction;
4. historical, strictly pre-outcome climate connectivity;
5. estimability gate;
6. primary cue × predictive-connectivity departure model;
7. only then the secondary frozen-grid threshold-like analysis.

No scientific claim may be changed because of the present access state.
