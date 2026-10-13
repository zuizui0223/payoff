# AmNat Paper 2: frozen V8 row-output restoration

Date: 2026-10-13. Status: PRE-RECOVERY, INTERNAL SCIENTIFIC AUDIT ONLY. No new
hypotheses, published results, independent raw-data R-bootstrap reruns,
or anonymous reviewer package are asserted.

## Purpose

PR #327 and PR #328 render frozen *summary* estimates, not actual spatial-pair
or individual points. The original 2026-10-05 GitHub Actions artifacts remain
unexpired and contain the actual 166 environmental-pair rows, 150
species-target transfer rows and the paired structural-null audit results.
Recover those exact original output files instead of inventing data points.

## Pinned origins

Upstream bird data: Amaral et al. BirdMigrationSpeed, Git commit
62c58d77c2028bd863dfe3697b0d9cf29ceaeab0; file data/final.rds;
Git blob SHA1 f1c9e63a377bb96152c573081e7c482cfe49ebc3;
7,250,107 bytes; Dryad DOI https://doi.org/10.5061/dryad.ttdz08m6w.

Frozen original GitHub Actions artifacts (exact ID and ZIP SHA-256):
- V8 primary environment, run 37285260343, artifact 11334053847,
  e54a2c835a33f6b99fad1de13add2cace7d7f6973d2c2355c46b0fed6a832ec0
- Transfer rows/bootstrap, run 37289801143, artifact 11336345852,
  046b3221feef75f77be63fcf37ef887101f801c8b1f62e32b41d6bc454466327
- Structural-null/permutation, run 37291407274, artifact 11337415962,
  54b260d19383aa7fee862ef3023e0a1080f218ef1dd3ed7257a52318019af360

Immutable manifest:
data/payoff_b_v8_row_archive_provenance_20261013.json.
Original frozen R scripts and all V7R/V8 outcome decisions remain untouched.

## Recovered-row audit contract

scripts/audit_payoff_b_v8_restored_rows.py verifies:
- Exactly 166 distinct spatial pairs and 28 species; early/late Pearson
  correlations and their signed difference; mean change +0.3690.
- Original 10,000 pair and equal-species bootstrap draws, using the
  standard R type-7 percentile interpolation.
- Exactly 150 bird species-target rows, 72 environmental pairs and
  22 species; independently recomputed inverse-within-species-weighted
  transfer coefficient +0.06243969 and its original 10,000 bootstrap draws.
- Fixed-arrival null coefficient +0.04742 and observed-minus-null
  increment +0.01502, with its original 10,000 bootstrap draws.
- Original 2,000 within-window bird-arrival permutations, including their
  median and central range.
- Every recovered CSV SHA256, and the source final.rds byte size, Git blob
  SHA1 and SHA256 (temporary input only, not re-uploaded).

All targets are locked before recovery. A missing or changed artifact,
missing original row, changed statistical inference unit, or estimate/CI
drift causes a failed gate, not an adaptive re-analysis.

## Interpretive and anonymization limits

The recovery does not rerun original R scripts from final.rds. It
independently rechecks numeric arithmetic from *original archived rows and
bootstrap draws*. Its internal artifact contains unmodified outputs and
GitHub-specific filename and run metadata; it is not anonymized or ready
to upload as a reviewer archive. Dataset reuse/distribution rights,
independent R replay, final source-grounded point-level figures and the
anonymous data/code packet remain separate gates.

Registered environmental broad degradation: NOT SUPPORTED; observed mean
change positive. Registered negative bird mismatch transfer: NOT SUPPORTED.
Fixed-arrival null explains the apparent positive transfer direction,
without showing a causal adverse bird response. Neither perceived forecast
quality nor demographic fitness is identified.
