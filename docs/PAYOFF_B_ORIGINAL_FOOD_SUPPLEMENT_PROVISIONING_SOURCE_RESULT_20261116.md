# PAYOFF-B actual provisioning experimental-source discovery result (2026-11-16)

**Decision: HOLD — published Dryad metadata and all three original file names/checksums verified, but raw XLSX bytes were NOT accessible anonymously from the official Dryad file API (HTTP 401). No per-nest data joins, newly fitted effects or inferred videos.**

## Official source

- Dryad dataset: Seress, Sándor, Evans & Liker (2020), DOI **10.5061/dryad.qbzkh18dj**. Official dataset metadata was fetched as JSON from `https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.qbzkh18dj` (sha256 `20687451ef3688ef5520ee2fcf66dba75db5a51068bb1c9e13022c69b1284e90`). Metadata license CC0-1.0 and title match the published study.
- Dryad public versions endpoint exposed original `_embedded["stash:versions"][0]["_links"]["self"]["href"]` **/api/v2/versions/55996** (version 2). This source-provided version link is parsed, not guessed. Official file listing URL `https://datadryad.org/api/v2/versions/55996/files` (metadata SHA256 `5d530009ba6a68b61015d2e5ea122bf430a9e59d102c7b579d53743bc77b9c15`).
- Three original XLSX files (official verified *metadata*, not raw bytes):
  - Nest data: `Seress_JAE_food_exp_nestdata_2020.2.20.xlsx`, file ID 258454, 21,173 bytes, source SHA256 `cbfdc03cae11e27060d229c57c08438fff2803e7713caaee70eca62e5e7a7dc8`;
  - Ringing/body measurement: `Seress_JAE_food_exp_ringing_2020.2.20.xlsx`, file ID 258455, 134,567 bytes, source SHA256 `4a8a3d6b418aa138b2021665449fddc962e1e1474ad6366d4a3d7c2079b33514`;
  - Video/provisioning: `Seress_JAE_food_exp_vid_2020.2.20.xlsx`, file ID 258456, 122,844 bytes, source SHA256 `15fd9cfa3a9be34f44024c3cde17cba2a1a1619cb5cdfcc97820dc83bf1ab76a`.
- The API GET `/api/v2/files/{id}/download` returned **HTTP 401** on **all three files** from the public no-credentials GitHub Actions runner. This may reflect public API download access policy, not proof that no user can download from the website. No credentials were inferred or bypassed; no unofficial mirrors were substituted.
- Source audit code: `scripts/payoff_b_dryad_food_supplement_provisioning_probe.py`; source gate plan: `docs/PAYOFF_B_ORIGINAL_FOOD_SUPPLEMENT_PROVISIONING_SOURCE_GATE_20261116.md`. Synthetic-only tests check exact HAL version/file references and digest fail-close, but cannot verify inaccessible original XLSX sheets.

## Existing biological knowledge — prior art, NOT a novel PAYOFF-B outcome

Seress et al. (2020) *Journal of Animal Ecology*, DOI **10.1111/1365-2656.13211** experimentally provided nutrient-enhanced supplementary mealworms to great tit nestlings, with the supplement designed to cover approximately 40–50% of the supplemented brood's food requirements. Their reported comparison already found urban supplemented nestlings substantially improved size and survival compared with urban control, largely closing the city–forest control difference, while adult provisioning rate did not markedly change. This is established experimental evidence that **the quantity/quality of food delivered** can matter more than the *number of parental provisioning visits*. It is not newly estimated by us, and experimental provisioning is not equivalent to natural prey biomass/phenology.

Other already published relevant examples:
- Sinkovics et al. (2021), *Scientific Reports*, DOI 10.1038/s41598-021-03504-4: direct video analysis demonstrated that adult feeding frequency alone can miss prey size, food quality, and alternative prey differences. 2014–16 urban/forest comparisons of prey types and fledging response are in the paper; its original bird-level source availability is not independently verified here.
- Halliwell et al. (2024), *Dryad* DOI **10.5061/dryad.9p8cz8wqj** and linked paper: original published dataset lists **23,305 provisioning event rows** (timestamps and carer identity), **1,070 watch-level rows** (nest outcomes/effort), and **2,311 weighed chick rows**. This is long-tailed tit cooperative **within-brood coordination** and outcome data, not actual prey biomass. The authors already analyzed alternation/synchrony versus recruitment, predation and chick outcomes. We cannot claim to discover those known coordination effects.

## PAYOFF-B theory-to-ecology consequence

Scottish EIDC source-verified *observational* results in PR #392 found sampled-season mean caterpillar mass better predicts blue tit fledged/clutch than hatch-window mass, and no incremental effect of hatch timing once season mass was included; **strict phase-specificity gate HOLD**. The experimental Seress result supports the distinct broader proposition that resource **delivery/quality** can affect reproductive payoff, even when parental visit *frequency* is similar. These two results are from different ecosystems, species, times and designs. They **must not be pooled as if one empirical mediation chain**.

A legitimate further proof of the user's information–irreversibility–recourse game requires individual decision-time environmental cues, actual partner interaction/feeding events, subsequent adjustments and reproductive fitness. The two known public sources cover different subsets of that chain. Missing files, unavailable cues and source overlap remain explicit.

**Next available access step** is official Dryad public web download for the three named workbooks or a verified, licensed exact SHA256 original mirror; without that raw source, fail-close at metadata-level provenance, do not calculate a new intervention coefficient. Do not ask the user for passwords or use unauthorized API routes.
