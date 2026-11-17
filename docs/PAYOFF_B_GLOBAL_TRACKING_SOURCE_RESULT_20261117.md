# PAYOFF-B source-gated 2026 global bird-tracking result — 2026-11-17

**Decision:** PASS official Zenodo source authenticity; **NO_GO_DIRECT_INFORMATION_X_RECOURSE_TEST from these four CSVs alone**. No new timing or migration coefficient fitted, no original bird phenology/migration effect inferred.

## Original provenance (official Zenodo records)

The journal paper Brlík et al. 2026 (DOI 10.1038/s41559-026-03208-w, published 27 October 2026) cites dataset concept DOI **10.5281/zenodo.18175801**. Official Zenodo REST API confirms concept DOI 10.5281/zenodo.18175801, exact v3 record DOI **10.5281/zenodo.19821864**. All four CSV source files downloaded via official public record file URLs, matched original manifest MD5, and independently hashed SHA256:

| Exact v3 filename | Rows | source SHA256 |
|---|---:|---|
| dat1_2026-04-27.csv | 2,314 | def7dc6ab018b5ca5156fce0e6a0af4f3476c7af9ef7aeba2362fa79e58affde |
| dat2_2026-04-27.csv | 2,019 | 66fce7908b29896e76272f499a8ee460246843e9e3b302c69a4a5c8320a97021 |
| dat3_2026-04-27.csv | 1,918 | 46e26124a65e8b4f7fcb5e839a57a62517ba01d7b8cef3d867dad774850418cf |
| dat4_2026-04-27.csv | 1,989 | 7d4c70a65987b64c3a4f60b0b65c1f47c1b25a88c14be5249d77187b3f75df9e |

These are **four analysis tables / sensitivity variants**, not independent individuals or four new research datasets; do not sum the rows to report total migrations.

## Actual original columns

All files include source bird/study identifiers (id.ind, id.study, species), year, event timing fields (doy.dep.br, doy.arr.nbr, doy.dep.nbr, doy.arr.br), inferred duration/distance variables, seasons and trait/taxonomy metadata. Source event dates include cumulative day-of-year values >365, consistent with year-crossing annual cycles; do not reinterpret those as invalid ordinary DOY.

**Missing from all four CSV schemas:** actual stopover GPS coordinates or route-site geography; independent local environmental cue time series; independently observed destination spring conditions; direct individual nesting/fledging/survival outcomes. Also, no realized migration feedback "availability/number of opportunities" variable independent of movement duration or route adjustment.

Therefore:
- The paper's already published findings — partial compensation for late departures, autumn/spring temporal links and a nonbreeding-season reset — remain **prior art**.
- Any new same-source finding on compensation/arrival timing would reuse published source and not establish PAYOFF-B's hypothesized information limitation.
- **V7-type cue predictability q × remaining route opportunity U cannot be fit** without external source-year-by-location climate and GPS checkpoints, even though the event timing rows are real.
- No eBird occurrence data were retrieved or used in this audit.

**Next source:** Boom et al. 2023 GPS-based barnacle goose reproduction dataset, Dryad DOI 10.5061/dryad.m63xsj47x, is the alternative candidate because the paper reports bird ID, nest locations and breeding propensity/success. Source availability and actual join columns must be verified before any payoff outcome analysis. That source's published effect of local spring timing on breeding is itself prior art.

**Workflow:** https://github.com/zuizui0223/payoff/actions/runs/44005503419, three synthetic tests and original Zenodo source audit passed.
