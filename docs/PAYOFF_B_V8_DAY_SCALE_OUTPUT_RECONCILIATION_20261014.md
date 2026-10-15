# PAYOFF-B V8 — correction of a historical post hoc interval (2026-10-14)

**Classification:** SOURCE-DATA/OUTPUT RECONCILIATION ONLY; no new ecological hypothesis, no revised V8 preregistration, no refit of the previously executed statistical design.

During reintegration of the original 2026-10-05 metric-scale diagnostic into the Paper 2 manuscript, the original R source was recovered byte-identically (Git blob SHA a42b4d9f1a1792d647d6091e980754c428009ce1). The exact 2026-10-05 GitHub Actions artifact for the extended diagnostic (run 37389432690; artifact 11380965912; archive SHA256 18a8b34abd989f09d5fd98995bf43022b1efeccff2ab4cc744fa91f7d8970ed3) was recovered and compared against an independent re-execution of that unchanged R script on the exact pinned upstream RDS.

**The historical R output and re-executed R output agreed**, including source/bird row membership and bootstrap/sensitivity statistics. However, the earlier prose receipt docs/PAYOFF_B_V8_METRIC_SCALE_DIAGNOSTIC_RESULT_20261005.md reports a slightly different 95% pair interval for the improvement in source forecast skill expressed as a difference of held-out RMSE:

| Value | Earlier prose receipt | Archived R output and exact R re-execution |
|---|---:|---:|
| Mean delta of relative source LOYO RMSE skill (days) | +2.628 | +2.628143 |
| Pair bootstrap 2.5% limit (days) | +2.134 | **+2.131827** |
| Pair bootstrap 97.5% limit (days) | +3.202 | **+3.183949** |
| Source-cell cluster interval (days) | +1.593 to +3.826 | **+1.594704 to +3.806895** |
| Target-cell cluster interval (days) | +2.039 to +3.293 | **+2.048298 to +3.274045** |
| 5° block interval (days) | +1.748 to +3.666 | **+1.742083 to +3.656110** |
| 10° block interval (days) | +1.511 to +4.158 | **+1.520388 to +4.117361** |

The source paper's 10,000-draw squared-loss information-value interval is unchanged: delta G_CV +32.08175 days², pair-bootstrap CI +21.04010 to +46.79639 days².

The cause of the older prose mismatch has not been established. It may reflect an earlier diagnostic implementation or copying from a different source run, but **that explanation is not asserted without a verified execution record**. Scientific priority therefore goes to the recorded original extended run and the byte-identical re-execution, not a conflicting paraphrase.

The original historical prose is preserved unedited as provenance. The 2026-10-14 Supplementary Table S2, manuscript §4.1, and the independent verifier use the source-backed interval [+2.131827, +3.183949] days, shown at three decimals as [+2.132, +3.184]. The corrected interval still excludes zero and does not change any frozen V8 outcome or imply bird cognition, fitness or recourse.

**Important:** This is a post hoc, non-confirmatory, statistical forecast-skill diagnosis. The original V8 preregistered transfer of signed correlation change to bird matching remains NOT SUPPORTED; direct RMSE-change-to-bird matching transfer has not been separately identified.
