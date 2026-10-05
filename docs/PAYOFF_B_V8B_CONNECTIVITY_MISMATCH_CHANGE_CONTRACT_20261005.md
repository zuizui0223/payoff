# PAYOFF-B V8b prospective secondary contract — connectivity change and mismatch change

Date: **2026-10-05**

Status: **POST-V8-PRIMARY, PREOUTCOME SECONDARY**

## 1. Trigger and separation from V8 primary

V8 primary is frozen as **NOT_SUPPORTED_OPPOSITE_DIRECTION**:
source-to-target signed detrended green-up connectivity increased rather than
decreased between 2002–2009 and 2010–2017 under the frozen Amaral mapping.

The original V8 contract explicitly allowed a separate secondary analysis,
after the environmental result was frozen, asking whether route-level changes
in connectivity covary with changes in bird arrival–green-up mismatch.

V8b is that secondary analysis.

It does not alter or rescue the V8 degradation hypothesis.

## 2. Biological question

> **Do changes in cross-site spring predictability correspond to changes in how
> closely migratory birds track destination green-up?**

The ecological prediction inherited from the previously frozen broad-bird
information-axis result is:

- stronger predictive connectivity should be associated with smaller mismatch;
- therefore, increases in connectivity should tend to accompany decreases in
  arrival–green-up mismatch.

## 3. Frozen environmental predictor

Use exactly the V8 eligible source-target mappings and primary environmental
estimand:

[
\Delta\rho_{jp}
=
\rho^{late}_{jp}
-
\rho^{early}_{jp},
]

where:
- EARLY = 2002–2009;
- LATE = 2010–2017;
- rho is signed, detrended source-to-target green-up correlation;
- source-target geometry is the frozen Amaral mapping.

No source cell, window or environmental coordinate is redefined.

## 4. Bird response

For species j, breeding target cell p and year y, define the same mismatch
coordinate used in the frozen broad-bird analysis:

[
M_{jpy}
=
\log(1+|G_{py}-A_{jpy}|),
]

where:
- (G) is destination green-up day;
- (A) is estimated bird arrival day.

For each environmentally eligible V8 pair:

[
\Delta M_{jp}
=
\overline{M}^{late}_{jp}
-
\overline{M}^{early}_{jp}.
]

Interpretation:
- (Delta M<0): arrival–green-up mismatch decreased;
- (Delta M>0): mismatch increased.

A target cell must have at least **4 valid bird-mismatch years in each
8-year window**. This threshold is fixed before opening V8b results.

## 5. Primary estimand

The primary model is:

[
\Delta M_{jp}
=
\alpha
+
\beta_{\Delta\rho} z(\Delta\rho_{jp})
+
b_{species}
+
\epsilon_{jp}.
]

The focal coefficient is (eta_{Deltaho}).

### Directional prediction

[
oxed{
\beta_{\Delta\rho}<0
}
]

meaning that routes/cells with stronger increases in predictive connectivity
show larger decreases, or smaller increases, in arrival–green-up mismatch.

## 6. Admission gate

Do not fit the focal model unless:

- at least 100 V8-environmentally-eligible pairs also have sufficient bird
  mismatch data in both windows;
- at least 20 species contribute;
- at least 15 species contribute at least 3 target cells;
- SD of (Delta\rho) is >0;
- SD of (Delta M) is >0.

If the gate fails:

```text
V8B_PRIMARY = NOT_ESTIMABLE
```

No mismatch-year threshold is relaxed.

## 7. Primary uncertainty and support rule

Use a species-random-intercept model.

The focal slope is additionally evaluated by a species-cluster bootstrap.

V8b supports the directional secondary prediction only if:

1. the mixed-model slope is negative;
2. the species-cluster bootstrap 95% interval lies entirely below zero;
3. the species-level aggregate regression has the same negative direction.

Otherwise:

```text
V8B_CONNECTIVITY_MISMATCH_CHANGE = NOT_SUPPORTED
```

## 8. Mandatory sensitivities

After the primary V8b result is frozen:

1. raw absolute day mismatch instead of log1p mismatch;
2. require >=6 bird outcome years in each window;
3. equal-weight species means;
4. source-target distance as an additive covariate;
5. use Fisher-z connectivity change instead of raw-rho change;
6. leave-one-species-out;
7. signed arrival-minus-green-up change as a separate descriptive coordinate;
8. alternative 7-year windows 2002–2008 and 2011–2017.

No sensitivity replaces the primary result.

## 9. Interpretation boundary

Even a supported V8b association is not a causal test of information use.

The environmental predictor and mismatch response share destination green-up
data, so the analysis is interpreted as a route-level ecological
co-change, not as an instrumental or mechanistic causal estimate.

A supported result would license only:

> Route pairs with larger changes in cross-site spring predictability also
> showed directionally consistent changes in migratory arrival–green-up
> mismatch.

It would not prove:
- birds perceived the source cue;
- increased predictability caused the mismatch change;
- fitness improved;
- climate warming caused either change.

## 10. Novelty boundary

Prior work separately shows:
- bird arrival–green-up mismatch can change through time;
- bird sensitivity to green-up varies among species;
- cross-site climatic/phenological connectivity can matter for migration;
- spatial synchrony of spring vegetation phenology can itself change.

A targeted search did not identify a broad multi-species analysis directly
testing whether **temporal change in cross-site predictive connectivity**
covaries with **temporal change in migratory arrival–green-up mismatch** under
paired route mappings.

This is a search result, not a priority claim.

## 11. Outcome access

Before this contract is committed:

- do not calculate pair-level (Delta M);
- do not fit (Delta M\sim\Delta\rho);
- do not inspect the slope sign;
- do not alter the 4-year outcome threshold after seeing counts.

```text
V8B_CONTRACT = FROZEN_PREOUTCOME_SECONDARY
V8B_OUTCOME = UNOPENED
```
