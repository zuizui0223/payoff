# PAYOFF-B public Dryad website data access — original source result, 2026-11-17

**Source status: HOLD (original bytes unavailable). No ecological effect fitted and no field-level nesting, GDD or treatment table inspected.**

A second, **official public route** was tested after the Dryad API's earlier HTTP 401 on \`/api/v2/files/{id}/download\`. This route uses \`https://datadryad.org/downloads/file_stream/{official_file_id}\`, documented for public Dryad website download links, with the file ID, basename, file size, version ID and source SHA256 independently retrieved from the official anonymous Dryad metadata and version-file manifest. This was not an authentication bypass or invented private S3 link. The downloads were bounded to files of ≤250 KB. All requested original files failed with **HTTP 403**, content-type \`text/html\` on the connected Github Actions runner:

| Original independently published dataset | Official manifest filename | Manifest file ID | Manifest byte size | Website public download status |
|---|---|---:|---:|---|
| Boom et al. 2023 barnacle goose nesting and spring GDD, DOI 10.5061/dryad.m63xsj47x | \`1.NestLocationData.csv\` | 2635123 | 25,985 | **HTTP 403** |
| Boom et al. 2023 metadata / measurement definitions | \`README.md\` | 2635129 | 7,083 | **HTTP 403** |
| Seress et al. 2020 urban/forest great tit food-supplement experiment, DOI 10.5061/dryad.qbzkh18dj | \`Seress_JAE_food_exp_nestdata_2020.2.20.xlsx\` | 258454 | 21,173 | **HTTP 403** |

All three official file SHA256 values were obtained from published source manifest, **not verified from downloaded bytes** because no byte stream was admitted. Thus **neither 2023 goose nest outcomes nor 2020 great-tit experimental nesting records were opened**, and no new bird fitness/food treatment coefficients exist. Published effects are prior art regardless of their public metadata descriptions.

Verification: https://github.com/zuizui0223/payoff/actions/runs/44062162343, synthetic original digest/link tests 4/4 PASS, official source access failed gracefully. Code: \`scripts/payoff_b_dryad_official_public_stream_probe.py\`. Report artifact: \`outputs/public_dryad/official_website_original_schema.json\`.

### Consequence for the frozen V7 paper

The original Kölzsch et al. (2015) three-flyway Movebank 52,443 GPS fixes and 44 source bird IDs were already SHA256/MD5 verified. But its 1982–2011 historical stopover GDD spring anomalies Tables S2–S7 in publisher supplement \`jane12281-sup-0001-SuppInfo.docx\` and 16-region crosswalk remain unverified/unavailable. This is **different** from the 2023 Boom 2008–2020 nesting GDD table, and the 2023 data are currently also inaccessible as bytes. No valid source support exists to fit the registered V7 q × geometry-only urgency interaction or causal fitness payoff, and no register threshold has been changed.

**Main scientific work should not continue with further ungrounded source URL attempts, manual invented rows, or after-the-fact q substitution.** The narrow next permissible step is a legitimately shared complete original supplementary information file (or independently archived *exact* original region-year tables) and original region crosswalk, after which frozen V7 gate can be re-evaluated without modifying design.
