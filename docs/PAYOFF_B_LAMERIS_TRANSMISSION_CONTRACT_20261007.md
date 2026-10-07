# PAYOFF-B temporal rescue transmission — Lameris source contract

Date: **2026-10-07**  
Status: **SOURCE-DEFINED BEFORE MENDELEY ROW-LEVEL REANALYSIS**

## 1. Dataset

Lameris et al. 2018:

> Arctic geese tune migration to a warming climate but still suffer from a
> phenological mismatch.

Public data:

- Mendeley Data DOI 10.17632/wkv96vcvnj.1
- licence: CC BY 4.0
- data repository description states that migration/reproduction timing,
  snowmelt/plant phenology and reproduction data are included.

The paper's Data and Software Availability lists six components:

1. snow cover and food peak timing;
2. migration and reproduction timing;
3. clutch size;
4. gosling survival;
5. stable isotopes in eggs;
6. GPS tracks and time budgets for spring 2015.

The current API endpoint requires authentication. No row-level Mendeley outcome
has been opened in this branch.

## 2. Published facts treated as prior knowledge

Published results already establish:

- departure from temperate North Sea/Baltic sites did not advance with earlier
  Arctic snowmelt;
- migration after the Baltic accelerated under earlier snowmelt;
- arrival advanced by about 0.51 d per day shift in snowmelt;
- lay date advanced by about 0.35 d per day shift in snowmelt;
- earlier-arriving 2015 birds spent longer pre-breeding after reducing Arctic
  stopover time;
- longer pre-breeding was associated with greater local-resource use in eggs;
- mismatch was associated with lower gosling survival.

These are prior art and cannot become PAYOFF-B discoveries.

## 3. Primary individual-level estimand

Restrict to tracked birds for which all are available:

- individual identifier;
- year;
- Baltic departure date;
- breeding-site arrival date;
- lay date.

Define:

[
M_i
=
A_i-B_i
]

as migration duration from Baltic departure to breeding arrival.

Define:

[
P_i
=
L_i-A_i
]

as pre-breeding duration.

Fit the year-fixed-effect model:

[
P_i
=
alpha_{m year}
+
eta_M M_i
+
epsilon_i.
]

Primary reported quantity:

[
oxed{
	au=1+eta_M.
}
]

The primary goal is estimation, not rediscovery of a negative association.

## 4. Admission gate

Primary individual transmission is estimable only if:

- at least 20 complete individuals;
- at least 3 years;
- at least 2 years contain >=5 complete individuals;
- both M and P vary within year;
- no row is reconstructed from annual means.

If the gate fails:

    TEMPORAL_TRANSMISSION_PRIMARY = NOT_ESTIMABLE.

## 5. Individual-quality guard

Where repeated individuals occur across years, report:

1. year fixed effects;
2. individual-cluster bootstrap;
3. repeated-individual fixed-effect sensitivity if support permits.

A causal claim is not licensed because high-quality individuals may migrate
quickly and breed quickly for reasons unrelated to debt transfer.

## 6. Actuator-specific secondary analysis

For PTT/GPS years with direct Arctic stopover duration:

[
S_i
=
	ext{total Arctic stopover days between Baltic departure and arrival}.
]

Fit

[
P_i
=
alpha_{m year}
+
eta_S S_i
+
epsilon_i.
]

Prediction from state-debt transfer:

[
eta_S<0.
]

Less time invested at Arctic stopovers should be associated with more time
needed after arrival before laying.

This relationship is qualitatively published already; the reanalysis quantifies
its magnitude and transmission consequences.

## 7. 2015 mechanism subset

For 2015 GPS birds with time budgets and stable-isotope information, evaluate:

    Arctic stopover time
      ->
    pre-breeding duration
      ->
    grazing / local-resource reliance.

This is a mechanism check for resource debt, not a new discovery claim.

## 8. Fitness endpoint boundary

Gosling survival is available for 110 families across 2003–2007 and 2015, but
the paper analyzes survival through family/year mismatch rather than a complete
same-individual migration-to-survival chain.

Therefore do not claim same-individual end-to-end fitness closure unless file
identifiers explicitly permit a valid join.

If individual linkage is absent, gosling survival remains a downstream
population/family-level fitness anchor only.

## 9. Published aggregate transmission anchor

Before row-level access, the reported environmental slopes imply the
descriptive ratio:

[
	au_{m snow}
=
0.35/0.51
=
0.686.
]

Interpretation:

> roughly 69% of the arrival-date response to snowmelt is visible in the
> lay-date response at the published aggregate slope level.

Do not attach a confidence interval to this ratio without the covariance of the
two slope estimates or row-level refitting.

## 10. Stop rule

Do not redefine Baltic departure, arrival, or lay date after inspecting the
row-level transmission coefficient.

Do not replace the primary M-to-P transmission with whichever stopover or
resource metric produces the strongest result.
