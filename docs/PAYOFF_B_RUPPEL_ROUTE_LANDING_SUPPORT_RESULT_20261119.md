# PAYOFF-B Rüppel 2023: original route × landing is too sparse for a separate recourse effect

**2026-11-19 — completed source-only, post-publication design audit.** Not a new biological regression, a causal migration mechanism or an independent published finding. This follows the frozen design at `docs/PAYOFF_B_RUPPEL_ROUTE_LANDING_SUPPORT_PREFIT_20261119.md`, committed before the original joint counts were opened.

## Original data and provenance

- Rüppel et al. (2023), *Royal Society Open Science*, DOI [10.1098/rsos.221420](https://doi.org/10.1098/rsos.221420). Public CC BY 4.0 original [Figshare 6403996](https://doi.org/10.6084/m9.figshare.c.6403996), `rsos221420_si_002.zip` **100,303 bytes**, independently recalculated original ZIP SHA256 **`0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6`**.
- Native R recovered original `data.Event` **1,783** departure at-risk rows and `flights` **178** first-flight rows, exactly the same **178** `motusTagID` identifiers, with no unmatched/duplicate individual flights. All 178 have ordered start/end times and full start/end wind/cloud fields. 175/178 terminal departure event dates match the UTC flight start day; all 178 within ±1 day.
- Existing source weather→departure/route/landing coefficients were already published in the original 2023 article. No new weather response model was fit.
- [GitHub Actions run 44546509558](https://github.com/zuizui0223/payoff/actions/runs/44546509558) **SUCCESS**, all source-only stages passed; 5 frozen synthetic cross-tab tests passed. Original produced artifact **14540384944**; downloaded aggregate-only artifact ZIP SHA256 **`0eb07b73b93d3487f350aca93ff26c4ac7c7556022f23b41b769e741d4970633`**. Raw animal IDs, coordinates, time stamps, weather or individual outcomes were not exported.

## Critical original 2×2 counts

| Original first-flight route | Observed landing = 1 | Observed no landing = 0 | Original first flights |
|---|---:|---:|---:|
| **coasting** | **21** | 133 | **154** |
| **sea-crossing** | **3** | 21 | **24** |
| **Total** | **24** | **154** | **178** |

The numerical coincidence **24 sea-crossers = 24 landings** did **not** mean they were the same birds. The actual overlap of sea-crossing and observed landing is **only 3 birds**. Descriptive landing fractions are **21/154=13.64%** for coastal flights and **3/24=12.50%** for sea crossings. These are **receiver-detected first-flight events**, not unbiased population probabilities, and no effect size, p-value or confidence interval is inferred from this post-publication source check.

Given fixed marginal totals, let \(x\) be sea-crossing and landing: the 2×2 cells are \(x, 24-x, 24-x,130+x\). The *pre-cross-tab* support gate required ≥5 observed landings and ≥5 observed nonlandings in **each** route, hence **\(5\leq x\leq19\)**. The observed **\(x=3\)** fails that source support condition. No threshold is relaxed and no route-specific weather→landing interaction is fitted. Its correct status is **`ROUTE_LANDING_MODIFIER_NOT_ESTIMABLE_UNDER_FROZEN_SUPPORT`**.

### Source concentration across original study systems

| Original year | Flights | Observed landings | Sea-crossing flights |
|---|---:|---:|---:|
| 2019 | 48 | 8 | 3 |
| 2020 | 68 | 11 | 9 |
| 2021 | 62 | 5 | 12 |

| Original taxon | Flights | Observed landings | Sea-crossing flights |
|---|---:|---:|---:|
| Garden Warbler | 66 | 5 | 15 |
| Greater Whitethroat (original label: Gr. Whitethroat) | 68 | 12 | 9 |
| Sedge Warbler | 44 | 7 | **0** |

**Sedge Warbler has no observed sea-crossing first flight** in this published subset. This means a genuine cross-species route-specific landing effect cannot be inferred across all three original taxa, even without the 3-landing-cell limitation. Years and species are correlated with route availability and the coastal Motus receiver network is more likely to detect flights near shore; the original paper explicitly cautions against interpreting the detected offshore proportion as unbiased.

## Consequence for PAYOFF-B's game-theoretical empirical bridge

This source **does** genuinely record a temporally linked sequence of at-risk departure nights, route choice and observed later landing per tracked bird, using original start/end meteorology. But it **does not identify** the proposed joint interaction **pre-decision information reliability \(q\) × remaining correction capacity \(r(t)\)**, or delayed strategy cost \(D_{eff}\), for the following independent reasons:

1. **Route×landing support fails** (3 observed offshore landings versus prespecified ≥5), so a new route-specific recourse modifier is not admissible without arbitrary pooling.
2. **End-flight meteorology is observed after departure**. It cannot be relabeled an earlier forecast. The separate historical issued GFS 2019–2021 archive `d084001`, DOI [10.5065/D65D8PWK](https://doi.org/10.5065/D65D8PWK), has been verified at provider-metadata level, but custom GRIB subsets require login and **no original issued forecast bytes have been retrieved**. An analyst's retrospective weather prediction is also not evidence the bird perceived that information.
3. **No final phenological target/partner/fitness** is recorded: observed coastal landing is not reproductive success, and detection is route dependent.

**Stop this source as a primary q×recourse biological validation.** It remains useful prior art for stepwise decisions and a method/source foundation, but not an independently confirmed PAYOFF-B information-constrained coordination trap. Further post-hoc hunting for a significance sign in these 178 birds would weaken the evidence.

## Reproduction

- Frozen protocol: `docs/PAYOFF_B_RUPPEL_ROUTE_LANDING_SUPPORT_PREFIT_20261119.md`.
- Native original 2×2 source cross-tab: `scripts/payoff_b_ruppel_original_route_landing_support.R`.
- Summary / year and species audit: `scripts/payoff_b_ruppel_route_landing_support_receipt.py`.
- Fixed test gates: `tests/test_payoff_b_ruppel_route_landing_support_receipt.py`.
- The source-hashed [draft PR #410](https://github.com/zuizui0223/payoff/pull/410) contains all audit code, source metadata and aggregate output contract. The code never commits original animal-by-night events or flight coordinates.
- Existing main manuscripts, theorem, V7 original q×geographic urgency gate and `main` are unchanged.

**Evidence classification:** a valid original-source **non-identification/negative source-support** result, nested in the already published Rüppel 2023 ecological data lineage; **not** a new natural effect and not an independent species replication.
