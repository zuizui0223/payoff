# PAYOFF-B: red-knot randomized food-access original source result

**2026-11-20. Source only; no new biological effect fitted.** Original: Lameris et al. 2025, *Functional Ecology*, DOI 10.1111/1365-2435.70183. Public Figshare dataset DOI 10.6084/m9.figshare.28660718, original version 2, CC BY 4.0. Six, twelve and twenty-four hours daily food access were experimentally manipulated; changes in mass deposition, plumage and departure are already published prior art.

## Original source identity

- 4.combined_data.csv, provider file ID 53244101, 24,894 bytes, SHA256 755833eb13e241def834f12ea2c8d775ec643def807b23a4b3695ee7805e834f; 102 source bird-year records and 102 distinct BirdID.year values.
- 1.biometric_data.csv, provider ID 53244113, 2,336 repeated measurements; SHA256 a1f4f360b7413b8024b5f81229ae35d3b7c901e9c07ae33aba86f5c5439190c2.
- 6.statistical_analyses.R, provider ID 53244107, 1,430 lines; SHA256 07ba64cc5fe97ddb0af13763e6869303b99e67997a035c2f63af5628951d89fd.
- README.txt, provider ID 53244110, SHA256 d624be841db09cfb58cbe85fffaa39ae2262cbfbca60e68f196f8aef75155cbc.

All three small files used in the detailed audit passed independent SHA256 checks; public Figshare file metadata passed the provider MD5 check. The Motus raw ZIP exceeded the 8 MiB bounded source admission cap and was not downloaded.

## Original source record counts (not effect estimates)

| Year | Source bird-year rows | Release date present | Departure flag present | Departure date present |
|---|---:|---:|---:|---:|
| 2021 pilot | 14 | 0 | 0 | 0 |
| 2022 | 43 | 27 | 25 | 20 |
| 2023 | 45 | 33 | 28 | 25 |
| **Total** | **102** | **60** | **53** | **45** |

| Year | 6-h treatment source rows / dated departures | 12-h source rows / dated departures | 24-h source rows / dated departures |
|---|---:|---:|---:|
| 2021 | 5 / 0 | 5 / 0 | 4 / 0 |
| 2022 | 14 / 6 | 14 / 8 | 15 / 6 |
| 2023 | 15 / 9 | 15 / 8 | 15 / 8 |

These are original source **record-availability counts**, not departure success rates. Missing departure could be censorship or undetected movement. The original departure Julian field is present in 44 rows, one fewer than the full departure-date field. No arbitrary date fill or status substitution is performed. The initial parser miscounted literal NA strings as observations; corrected before final result and independently re-audited. The 102 derivative rows should not silently be equated to the 97 birds stated in the original paper without original model inclusion rules.

## Experimental independence and missing aviary crosswalk

In the published experiment, treatment was applied at aviary level. The 2021 pilot used one aviary per treatment and had no tracked postrelease departure; 2022 and 2023 used two aviaries per treatment. The source combined CSV lists original individual, year, treatment, release, departure, mass and plumage fields but **no explicit aviary/cage/enclosure assignment field**. A bounded original README and R-script text audit also found no authenticated individual-to-aviary crosswalk. That is **not proof the original published analysis was invalid**; it means a new independent aviary-clustered treatment inference cannot be reconstructed from these public derivative tables without additional source mapping.

**Gate: AVIARY_LEVEL_TREATMENT_EFFECT_REANALYSIS_NOT_ESTIMABLE.** Do not count 102 bird rows or 2,336 mass records as independent experimental treatment replicates; no new treatment beta, p-value or fitness effect has been fit.

## Ecological interpretation, evidence and limits

The original randomized feeding-access intervention demonstrates resource-dependent **physiological flexibility**, already reported by Lameris et al. The separate original Rüppel et al. 2023 Motus data show weather associations with departure/routing/landing, also prior art. They involve different birds, measurement contexts and decisions: a biological bridge from predecision *forecast observability q* jointly with *available action capacity r(t)* to behavior and partner fitness cannot be inferred by concatenating their results. The PAYOFF-B threshold q_wait(D_eff), network mismatch and natural causal recourse remain NOT_IDENTIFIED.

Original-source tests and reproducibility: Draft PR #411, the 2026-11-20 source freeze and aviary-source contracts, two source-only Python scripts and eleven source-integrity tests. SHA-verified GitHub Actions run 44660943443 succeeded, aggregate-only artifact ID 14595686528, downloaded ZIP SHA256 be47a55bec866579e03305877652c205a57cf05a1bc82e6a31063e816e4699ea. No animal IDs, locations or original rows committed. Frozen V2/V7 manuscripts and main unchanged.
