# PAYOFF-B: independent goose route-stage calendar-versus-compensation source contract

Date: 2026-10-08
Status: **source-only design fixed before accessing focal stage-date association results**. The source study already published breeding outcomes, but this diagnostic does NOT use outcome labels or inspect breeding coefficients. Exploratory ecological audit, NOT a preregistered confirmation of PAYOFF-B.

## Source and support

Author's original 2024 publicly archived code/data: https://github.com/aschindler23/Schindler_etal_2024_ProcB , pinned commit 2171bcd36bf37022c8716e15c0f75412103b0f3f.
File spring_data.csv SHA256 under CRLF line ending 9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd, matches the Dryad v5 manifest. Source summary: 642 sub-season rows, 49 individuals, 107 complete six-stage bird-years. This corrects earlier Dryad bulk-download HOLD, which cannot block legitimate author GitHub raw data.

Sub-season event first_day:
- stage 2: first migration flight begins, departure from Ireland/Great Britain;
- stage 3: first spring staging in Iceland starts;
- stage 4: second half of Iceland staging begins;
- stage 5: second migration flight begins (exit staging Iceland);
- stage 6: early breeding starts (Greenland).

An event first_day is the start of an annotated stage, **not** a directly observed decision epoch or stationary stopover arrival exact to the instant.

## Prospective descriptive contrasts

For each individual-year (one row):
- A: stage3 first_day; D: stage5 first_day; B: stage6 first_day.
- Iceland-staging duration I=D-A (days), second-flight/prebreeding transition B-D (days).
- Calculate within-year centered pooled OLS slope beta_DA of D on A, and beta_IA of I on A. Their exact accounting identity is beta_IA = beta_DA - 1, independent of behavior.
- Quantify within-year SD(D)/SD(A) and year-specific SDs; this is a calendar-synchronization descriptor, NOT effective individual recourse.
- Compare the observed beta_DA with within-year shuffled departure dates (4000 permutations, fixed seed 20261008), preserving dates and annual spreads. This is an **associational no-pairing null**, not an intervention into biology, and repeated individuals weaken strict exchangeability.
- Perform 4000 bird-cluster bootstrap replicates to estimate a descriptive 95% interval for beta_DA and beta_IA. Resample birds, retaining all their observed years. Report cluster support and nonfinite draws. Also report leave-one-year-out betas, not select years based on results.
- Use exactly the full author-data panel if all id×year×stage keys are unique and all dates strictly ordered with I>0 and B>D.
- Neither breeding_outcome nor breeding_success will be read into the calendar audit's output, and no fitness association will be fitted on this branch.

## Interpretive restrictions

**Calendar-like schedule:** beta_DA near zero, D clustered relative to A, and beta_IA near -1 may arise simply because individuals depart Iceland around a shared date. This is observational calendar anchoring, **not proof** of a genetically fixed photoperiod clock. Negative stay/arrival covariance alone is NOT active closed-loop feedback.

**Responsive release:** beta_DA away from zero after correct year/individual dependence is compatible with conditional behavior but can also reflect common weather, varying forage, observer stage assignment and shared social effects. Cue innovation and independent action capacity remain unmeasured.

**No fitness inference:** even if fixed staging exit anchors timing, cannot determine whether an earlier bird deliberately waited, whether delays improve forage intake, whether earlier resources were better, or whether birth-success differences represent a causal cost of compensation. Feeding fraction and ODBA belong in a separately designed sensitivity; source authors already modeled them against breeding.

**No posthoc successes:** existing V7R goose fixed-calendar diagnostic and published migrations were already known. This is an external-system *replication of a mechanism alias*, not a prospective high-impact ecology result.

## Stop and integrity rules

Fail closed if source manifest SHA differs, source CSV dimensions or 6-stage grain drift, ID-year-stage duplicates appear, stage timing nonmonotonic, or more than 5% cluster-bootstrap replicates are inestimable. Preserve actual null/negative/ambiguous results. Do not tune the sample after stage outcomes.

A favorable biological interpretation requires independent logged cues before exit, independently measured correction feasible set and actual fitness success; none is present in this design.
