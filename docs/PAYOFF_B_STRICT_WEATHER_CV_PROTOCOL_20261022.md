# PAYOFF-B held-out prediction test: does prior physical weather add signal?

**Protocol locked 2026-10-22 after observing full descriptive source weather differences.**
This is a *new predictive method applied to previously opened data* and is
therefore **EXPLORATORY**, not a genuine untouched prospective confirmatory
test of PAYOFF-B. Negative predictive results will be reported unchanged.

## Data and outcome

Three original public CC0, exact-MD5-verified Movebank GPS sources:
Ciconia ciconia, Anser albifrons and Numenius arquata. Egyptian vulture is
NOT included, because the stricter all-original-fixes-in-stationary-area
source screen admitted only 9 same-grid-year-month northward days (<10
predeclared overlap threshold).

Repeat existing fixed Feb–May three-day-stationary source-risk eligibility,
then require every original GPS fix on each of three anchor days within
30km. Original strict eligible source risk-days: 1,110 stork (85 case/716
stay); 1,790 goose (93 case/1,324 stay); 1,778 curlew (42 case/1,585 stay).
The rest remain OTHER/CENSORED, never relabelled as controls.

Outcome is a future two-day GPS-labelled northward transition vs continued
stay, NOT directly observed migration intent. Source animal days overlap,
and no independence is assumed from the record count.

## Predictor sets compared with blocked *out-of-fold* scoring

BASELINE (prior source state only):
- sine and cosine of UTC day-of-year;
- latitude and cyclic longitude of stationary source centroid;
- natural log of consecutive *previously eligible* risk-day run length.

WEATHER-ADDED (baseline plus only physical predecision NASA POWER DAILY data):
- prior-day mean and 7-day anomaly of T2M, WS10M, V10M and
  ALLSKY_SFC_SW_DWN; prior day is calendar date of stationary anchor -1,
  7-day mean is anchor -2 through -8.
- A weather batch response includes future calendar dates for cost,
  but no event predictor may read those days; source date restrictions
  remain fail-closed.

Both models: fixed ordinary logistic regression, L2 penalty C=1,
training-set-only StandardScaler, lbfgs max_iter=1600, no case weights,
no under/oversampling, no hidden feature selection. Probabilities
predict a *two-day future GPS label*, not risk under randomized cue access.

PRIMARY exploratory evaluation: leave one entire ORIGINAL CALENDAR YEAR out
at a time within each taxon source. A fold needs >=12 training positive
days, >=60 training stay days; heldout >=20 days and >=1 positive. Require
>=3 admitted heldout years overall, >=15 source positive and >=100
source stay days evaluated. Report exact exclusion counts; no threshold
relaxation. The same animal appearing in different years is not removed;
this is a year-heldout temporal predictive test, not independent cohort
replication.

SECONDARY: 5-fold whole original ANIMAL-ID grouped holdout, requiring the
same fold admissibility. Repeated days of one animal cannot be in both train
and test. Shared year/month physical weather may remain correlated.

Use *overall out-of-fold* log loss and Brier score, not in-sample regression
coefficient signs, p-value hunting or naive daily independent bootstrap.
Incremental weather skill = baseline score MINUS baseline+weather score,
so positive means improved prediction on previously heldout source labels.
Report both skill metrics and per-source admitted/excluded year/group folds.
Do NOT pool taxa or source records as independent studies.

Interpretation ceiling: positive heldout weather skill means lagged
physical weather may contain incremental **predictive information** beyond
calendar/location/past-state baseline *in this recorded cohort*. It does
NOT mean birds perceive it, use forecasts, can alter their routes or benefit
in survival/breeding. A null or negative heldout skill undermines the claim
of useful additional predictive weather information for this defined
proxy outcome/model but cannot prove cue irrelevance or lack of adaptation.
New independent high-frequency cue+behaviour+fitness cohorts are needed
for the actual PAYOFF-B information×remaining-recourse ecological question.

Never export animal identities, site coordinates, original event dates,
raw bird GPS, weather samples or individual predicted probabilities.
