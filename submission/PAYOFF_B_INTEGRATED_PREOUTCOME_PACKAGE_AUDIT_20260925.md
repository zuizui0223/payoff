# PAYOFF-B integrated PREOUTCOME package audit — 2026-09-25

Status: **PASS — temporal-buffering PREOUTCOME working package**

## Source state

Validated reframe head:

`d44dbfa09024ee87a473e6d0d1c28538fdde0209`

Scientific state:

```text
PREOUTCOME_INTERNAL_READY
primary_conclusion = temporal buffering delays but does not permanently replace spatial tracking
final_submission_eligible = false
final_submission_blocker = registered Aikens fixed-24h lambda adjudication
```

## Package workflow

```text
workflow = Integrated PAYOFF-B PREOUTCOME package
run = 36118090547
status = PASS
artifact = payoff-b-integrated-tracking-preoutcome-package
artifact_id = 10856440257
artifact_sha256 = f9d7004081bc236bcdd86521c8bc07b46458366b2fd1edb0b88ce73451069e9d
```

Inner deterministic archive:

```text
file = PAYOFF_B_INTEGRATED_TRACKING_PREOUTCOME_PACKAGE.zip
bytes = 78615
sha256 = b5628da1383960bdbbb637960d78d4f9c71588269f0ddee3111be37bba3fffc8
manifest_sha256 = 3487e6f9ad489e4ff8aa98cb76460da11f05476e277831f97930b78c470ca4c1
file_count = 31
figure_count = 6
aikens_result_present = false
aikens_outcome_opened = false
```

## Hash-stability boundary

`PUBLICATION_STATUS.md` and
`PAYOFF_B_INTEGRATED_PREOUTCOME_READINESS_20260925.md` are deliberately
excluded from the ZIP. They audit the package from outside rather than being
embedded inside the object whose hash they report. This removes the previous
self-reference and makes the deterministic archive hash stable under later
audit/status updates.

## Manuscript state

The machine manuscript audit passes with:

```text
abstract_words = 198
main_text_words = 3699
keywords = 8
references = 21
uncited_references = 0
main_figures = 6
identity_leaks = 0
```

The anonymous main text SHA256 is
`61c99d8e46681db3daae259a72b9d8df25ce94f97c163d1a329c85575d672fe8`.

The generated Supporting Information SHA256 is
`c9600d30ed609261ddf3dbe056db4e5a19ebe97d565a4ae0c1ae3cb3bdf96feb`.

## Figure integrity

Only Figure 1 changes under the reframe:

```text
Figure 1 = 0f7917c86f2521ee435bb9e8178293e5f0b83733dc5f0eb8aec97a876ad441d3
Figures 2-6 = unchanged from the frozen pre-reframe quantitative set
```

This is an editorial / inferential hierarchy change, not a numerical reanalysis.

## Claim boundary

The package now treats:

1. finite temporal buffering followed by spatial re-entry as the primary
   synthetic mechanism;
2. low mismatch concealing latent spatial tracking demand as the ecological
   consequence within the declared synthetic landscapes;
3. the 55-species speed-rule rejection as the primary natural generality test;
4. direct migration systems as mechanistic decomposition;
5. “mismatch is an outcome, not a tracking architecture” as the inference
   consequence.

The package does **not** claim that latent spatial tracking demand has been
directly estimated across the natural datasets.

## Remaining blocker

There is no unresolved internal manuscript, figure, citation, provenance,
anonymity or packaging blocker.

The package remains PREOUTCOME because the registered Aikens fixed-24 h lambda
adjudication is still unopened.
