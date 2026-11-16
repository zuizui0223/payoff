# PAYOFF-B: source-corrected measured caterpillar mass x hatch-window result — 2026-11-16

## Status: executable original-data work complete; strict source-corrected gate HOLD

The first original-mass exploratory receipt `https://github.com/zuizui0223/payoff/actions/runs/43883494767` met its pre-frozen gate on **143 site-years / 444 nests / 44 sites / 5 years (2014 and 2018–21)**. **Do not treat this as an independent robust general result**: source documentation proves that caterpillars were not weighed until 2017. A post-open original-source-year audit `https://github.com/zuizui0223/payoff/actions/runs/43884075695` established that accepted 2014 mass entries were entirely **structural zero inferred from original zero caterpillar counts** (975 branch rows), with 151 positive-count branches lacking mass, rather than measured mass. Hence the first five-year mass result is downgraded. The year-filter correction came **after that result was opened** and is reported transparently as post-open sensitivity, not retrospective preregistration.

The exact source measurement was `caterpillar.mass` in **grams per standardized 30-hit branch beating**; source count is `caterpillars` per same beating. EIDC DOI 10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3. Four source CSVs were content-SHA256 verified before fitting. The EIDC ZIP wrapper is non-reproducible and is not used as sole source-integrity gate. Censored source `<0.02` equals 0–0.02 grams per branch, both bounds were fit; undetected positive-count mass is not set to zero. Exact-source matching and full hatch to hatch+13 day support were required; no extrapolation beyond observed prey season or over >8 day gaps.

## Models (frozen before first mass outcome)

- A: site-year climate, geography, year, mean hatch day, mean clutch, prey seasonal peak count and signed peak-to-hatch gap.
- B: A + observed hatch-window **count per beating**.
- C0,C1: A + observed hatch-window **mass g per beating** (censoring lower, upper).
- D0,D1: B + original observed hatch-window **mass g per beating** (censoring lower, upper).

Outcome is original blue-tit `fledged/clutch` averaged over **unmanipulated nests per site-year**, equal site-year weights, with explicit full-year (LOYO) and full-site (LOSO) holdouts; fixed ridge=1 and training-only standardization. This is not a nest-level independent resource effect, causal mechanism, direct feeding, true energy uptake, or game-theory/information estimate.

### Original 5-year exploratory receipt (includes 2014 unweighed branches; not retained as mass validation)

| model | LOYO equal-year MSE | LOSO equal-site MSE |
|---|---:|---:|
| A | 0.044419 | 0.047133 |
| B count | 0.047008 | 0.048377 |
| C mass lower/upper | 0.043752 / 0.044031 | 0.046191 / 0.046451 |
| D count+mass lower/upper | 0.043523 / 0.043428 | 0.044318 / 0.044336 |

The original frozen 5-year exploratory gate passed, but the underlying 2014 inclusion means this is not the source-corrected conclusion.

### Corrected measurement-era sensitivity: **2018–21**, 138 site-years, 427 nests, 44 sites

| model | LOYO equal-year MSE | LOSO equal-site MSE |
|---|---:|---:|
| A | **0.051477** | 0.047927 |
| B count | 0.054442 | 0.049263 |
| C mass lower/upper | 0.052319 / 0.052822 | 0.047286 / 0.047593 |
| D count+mass lower/upper | **0.048473 / 0.048521** | **0.044941 / 0.044957** |

D adds meaningful predictive information beyond B in **both** heldout protocols and **both** censor bounds. All 4 heldout years (2018–21) showed D-versus-B improvement. However **C-alone fails versus A in full-year holdout**, so the stringent frozen gate requiring both C and D cannot be promoted to success after correcting the source-measurement period. **The narrow retained result is: source-observed count and mass together offer more out-of-year and out-of-site predictive information than count alone in this fixed model, not that mass alone universally improves prediction.**

### COVID sampling sensitivity excluding 2020 as well: **2018, 2019, 2021**, 116 site-years / 308 nests / 43 sites

| model | LOYO equal-year MSE | LOSO equal-site MSE |
|---|---:|---:|
| A | **0.066950** | 0.045964 |
| B count | 0.072149 | 0.047323 |
| C mass lower/upper | 0.070735 / 0.071025 | 0.043842 / 0.044036 |
| D count+mass lower/upper | 0.068911 / 0.068838 | **0.042571 / 0.042605** |

The **incremental D versus B** sign remains positive across both validation dimensions and both censor bounds; all 3 remaining year folds improve D versus B. Yet neither C nor D beats A in year-heldout MSE. We therefore must **not** claim a general improved resource-fitness predictor or direct mass-driven mismatch mechanism.

### Prey source quality receipts

The mass-source audit read **37,674 original branch-beating rows** and **6,735 original site-year-dates**. Exactly 6,372 dates meet >=80% source mass availability; 363 dates are excluded. Within rows: 30,289 numeric original mass values; 1,104 source left-censored `<0.02`; 5,783 zero-count/blank-mass structural zeros; 486 positive counts missing mass; 12 uncertain. Source-year validation: 2014–16 contain **no measured positive mass rows**; from 2017, measured mass exists. The source's larger Zenodo 2024/2026 reuses Scottish prey monitoring and is not a second independent replication.

## Mathematical / ecological connection (hypothesis, not yet causal)

Let N(t) denote standardized prey number per beating, M(t) standardized mass g per beating, and s(t)=M(t)/N(t) for N(t)>0. Equal number peaks can represent very different prey sizes and potential food amounts. The observed extra prediction from M conditional on N means the two source currencies are not interchangeable for a fitted reproductive response. It **does not establish** that body size, diet, energy assimilation or phenological mismatch caused the response; the models are additive, no causal prey-size interaction term was fitted.

The theoretical PAYOFF-B question is whether an organism's information/commitment/recourse constraints produce a loss of **realized interspecific resource payoff** even if spatial/phenological tracking and gross resource production remain possible. This dataset tests only the crude resource->reproduction observable bridge, *not* the remote cue information or strategic coordination components. Source-based nestling weights at first/second visit are a more proximal, independent future outcome to audit before making a resource-to-biomass growth mechanism claim, with exact nest/year ID and age/selection controls.

**Authoritative outputs:** 
- First original mass run: https://github.com/zuizui0223/payoff/actions/runs/43883494767 (6 synthetic tests and source-verified original fit).
- Source-measurement year + COVID sensitivity: https://github.com/zuizui0223/payoff/actions/runs/43884075695 (8 synthetic tests, source-year audit and 4 fixed panel variants).
- Previous count-only source-verified FAIL/HOLD: https://github.com/zuizui0223/payoff/actions/runs/43881619335 (19 synthetic tests + Scottish original source counts, 448 nests/143 siteyears).
