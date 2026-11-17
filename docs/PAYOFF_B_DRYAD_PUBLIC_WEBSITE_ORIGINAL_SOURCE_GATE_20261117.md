# PAYOFF-B official public Dryad website download-route check — 2026-11-17

**Source access only. No phenology, provisioning, treatment or breeding effect fitted.**

The old frozen original-source gates for Boom et al. (2023), Dryad DOI 10.5061/dryad.m63xsj47x, and Seress et al. (2020), Dryad DOI 10.5061/dryad.qbzkh18dj, both retrieved official dataset metadata, version and file manifests but received HTTP 401 for official **API** file download URLs. This did not establish that public source **website** downloads require access. The current public Dryad dataset page lists named files with direct public download links.

The public Dryad website link format \`https://datadryad.org/downloads/file_stream/{officialFileID}\` is documented in an independent Dryad-download integration and matches named public links (not an API token or private URL). We test this route strictly for files whose exact ID, filename, size, digest and DOI are first obtained from **official public Dryad API**. Do not attempt authentication bypass, construct hidden S3 URLs, scrape session tokens, or retry rate limiting indefinitely.

Original files needed to advance an ecological question:
- Boom et al. 2023 barnacle goose nest table, \`1.NestLocationData.csv\`, reported by the public Dryad README as individual×year nest location, breeding attempt, nesting success, GPS-derived arrival, same-year GDD jerk spring onset and mean GDD jerk. **These are prior authors' constructs and published spring-fitness associations are prior art**. Actual file bytes have not yet been seen by this project. If accessible, verify exact source SHA256 and source field/types, individual×year keys and quality before any new inference.
- Seress et al. 2020 experimental great tit nesting file \`Seress_JAE_food_exp_nestdata_2020.2.20.xlsx\`. Published food-supplement effects on urban nestlings are prior art, so this is only a candidate source for a *distinct* information/recourse test, not proof that food helps.

**Source gate:** only if original bytes match the official source manifest checksum and length may the column schema be inspected. Otherwise record HOLD and stop. Never use the file metadata's rows, names or public paper's aggregate coefficients as if analyzed original observations. Preserve study licensing.

Even if Boom source is accessible, the older 2015 Kölzsch V7 question (source 30-year spring predictability × independently geometry-defined urgency) remains under its **separate frozen admission**. The 2023 Boom table has spring history 2008–2020 and a different set of birds and endpoints; it cannot replace original 1982–2011 stopover S2–S7 data in the original V7 analysis.
