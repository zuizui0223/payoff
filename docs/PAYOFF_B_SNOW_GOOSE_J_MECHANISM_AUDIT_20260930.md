# PAYOFF-B greater-snow-goose J-mechanism source audit

Date: **2026-09-30**  
Status: **published-mechanism audit; frozen row-level lane remains unopened**

## Source-access result

The 2026 Dryad dataset (DOI 10.5061/dryad.c2fqz61jr) is publicly indexed and
its metadata resolve 13 files, including the two preregistered table inputs.
However, automated file-byte access is currently blocked in the available
execution environment:

- Dryad API file download: HTTP 401;
- public front-end file stream: HTTP 403.

No table rows have been opened, the registered FED-only model has not been
fitted, and no coefficient has been seen. This is a **source-access failure**,
not an ecological null result.

## What is already known from the published experiment

The row-level lane was intended to ask whether captivity duration produces a
direct physiological burden even when deliberate fasting is excluded. The
published three-year experiment already constrains that mechanism strongly.

### Energetic/body-mass pathway

Legagneux et al. (2012) reported daily corrected mass change in FED females of

\[
-9.56 \pm 8.79\ {\rm g\,d^{-1}}
\]

(mean ± s.e.), much smaller than the fasting-group loss. In 2009 specifically,
the FED-group mean change was

\[
-15.4 \pm 6.9\ {\rm g},
\]

described as relatively stable.

Thus captivity carry-over effects do not require a large FED energetic-depletion
signal. The preregistered cond2 ~ cond1 + DaysInCap analysis could still be a
useful independent re-expression of the 2009 data, but it is no longer the only
source supporting or refuting the mechanism.

### Endocrine pathway

Grentzmann et al. (2025) found no clear captivity-duration ordering of
stress-induced CORT at release:

- Day 3 versus Day 2: \(\beta=4.97\), 95% CI \([-9.79,19.72]\);
- Day 4 versus Day 2: \(\beta=-4.85\), 95% CI \([-19.60,9.91]\).

This argues against a simple monotone "more days -> higher release CORT" mediator.

### Fitness / breeding pathway

Grandmont et al. (2023), in contrast, reported a negative effect of captivity
duration on subsequent detection at the Bylot breeding grounds:

\[
\beta=-0.049,\qquad
95\%\,CI=[-0.096,-0.001].
\]

Grentzmann et al. (2025) found first-year survival of FED birds similar to
controls (\(\beta_{\rm fed}=-0.24,\ 95\%\,CI=[-1.06,0.57]\)), while UNFED birds
showed the stronger survival penalty.

## PAYOFF-B interpretation

The evidence does **not** support collapsing direct waiting cost into one
physiological mediator.

A more defensible decomposition is

\[
J(\delta)
=
J_{\rm energetic}(\delta)
+
J_{\rm stress}(\delta)
+
J_{\rm opportunity}(\delta)
+
\cdots
\]

where components may differ in strength and persistence.

Current source-backed evidence is:

- strong deliberate-fasting energetic cost: yes, but excluded from the FED
  mechanistic lane;
- strong FED energetic deterioration: not established by published aggregate
  results;
- monotone release-CORT increase with captivity duration: not established;
- duration-dependent breeding suppression: supported in the published
  experiment;
- natural information-waiting \(J\): **not identified**.

Therefore the correct ecological lesson is not "J is body-condition loss".
It is:

> **A direct cost of waiting can survive downstream timing compensation even
> when no single measured physiological mediator shows a strong monotone
> duration response.**

This is compatible with the general effective-deadline theorem,

\[
D_{\rm eff}
=
J(\delta)
+
\min_c[K(c)+M(\delta-c)],
\]

but does not provide a numerical natural \(J\).

## Frozen next step

If authorized/public file bytes become accessible later, the already-merged
registration remains unchanged:

\[
cond2 \sim cond1 + DaysInCap
\]

within FED females only, with capture-group clustered uncertainty.

That future result will be interpreted as one **J-like energetic mechanism
test**, not as a test of natural \(J\), \(D_{\rm eff}\), or \(q_{\rm wait}\).
