# PAYOFF-B Greenland goose: individual timing consistency after year-centering

Date: 2026-10-08
Status: **POST-OUTCOME exploratory**: stage5 pair correlation and stage2–6 contrasts were inspected before this formal source test. This is NOT a preregistered ecological discovery and must not be presented as one. Frozen V7R, V8 and the original source study unchanged.

## Source and natural history
Schindler et al. 2024 author pinned source: aschindler23/Schindler_etal_2024_ProcB commit 2171bcd36bf37022c8716e15c0f75412103b0f3f; spring_data.csv SHA256 after CRLF conversion 9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd.

107 bird-years / 49 birds over five years; **30 birds appear in more than one year**, 19 once. Per-stage dates are start-of-annotated season, not GPS-derived instantaneous decision/arrival or observed information. Stage 3 is Iceland staging start; stage 5 is start of flight to Greenland. Pre-exposed exploratory within-year-centered pairwise correlations from 97 non-independent same-individual across-year pairs were approximately stage2 +0.506, stage3 +0.381, stage4 +0.291, stage5 +0.687, stage6 +0.316. These are descriptive, not independent n=97 test observations.

## Audit procedure, defined before running this *new* permutation and cluster CI
- Validate original source checksum, complete six stages and all 107 bird-years.
- For every stage 2–6, subtract that year's stage mean and divide by that year's stage SD. Standardization avoids interpreting lower departure variance as greater stability merely because of absolute scale differences.
- For every repeated individual, compute mean standardized residual-product over all pairs of that individual's observed years; **average equally across the 30 repeat-observed birds** rather than overweighting the individual with five years.
- Simultaneously shuffle the entire *5-dimensional stage-date residual vector* among observed bird IDs **within each year** 10,000 times (seed 20261008). This preserves actual year-specific distributions, cross-stage covariance, original bird-year patterns, and the fact that some birds are observed more years than others. This null removes only the relation between the bird's identifier and the repeated calendar residual.
- Show raw stage-specific descriptive Pearson correlations from the 97 overlapping within-bird year pairs, along with bird-equal standard-score product statistics.
- Report per-stage Monte Carlo p for positive identity persistence. Because all five stages were inspected, also report a max-over-five-stage permutation p for stage5, and a paired stage5-minus-stage3 contrast p. These are **post-selection exploratory** diagnostics, not prospective significance testing.
- Bird-equal bootstrap (10,000 draws over 30 repeat-observed birds) for stage5 product-statistic uncertainty. This does not capture year-to-year population or phylogenetic/environmental uncertainty.
- Preserve negative results and do not select an alternate stage, cutoff or model after receiving the output.

## Interpretation
Above-null same-individual stage5 schedule residual would reject only a **fully exchangeable bird-identity** description of annual departure offsets. It does NOT show that birds possess a biological chronotype, an internal photoperiod clock, information about Greenland spring, an intentional waiting strategy, or individual optimal reproductive payoffs. Stable route choice, migration origin, social group, leadership and observer stage segmentation can create the same pattern.

A stage5-versus-stage3 comparison cannot be read as within-individual adaptation because the two event processes have different biological stages and measurement errors. There is no observed stage-specific resource cue or independent feasible action set. Breeding success is intentionally absent from this identity-only audit.

This route remains a mechanistic *negative control* on claims that timing variance contraction and stopover duration are proof of active ecological feedback. Do not start another independent manuscript based on this source-only consistency statistic.

## Independent prior-art search (performed after preliminary correlations were already viewed)

- Franklin et al. (2022), Journal of Animal Ecology 91:1416–1430, DOI 10.1111/1365-2656.13697, meta-analysed 177 timing-repeatability effect sizes from 47 bird species. Individual repeatability of avian migration timing averaged ~0.414. Individual migration timing persistence is therefore broadly established, NOT a novel goose trait.
- Birds use individually consistent temperature cues to time their migration departure (2021), https://pmc.ncbi.nlm.nih.gov/articles/PMC8285904/, followed 48 Asian houbara across years, linking individually consistent departure cues to spring responsiveness. Repeatability is compatible with use of environmental information, NOT sufficient to label decisions as fixed internal clocks.
- A 2025 greylag goose departure-order study, DOI 10.1007/s00265-025-03637-w, also demonstrates repeatable individual/group departure behavior. Social structure is an important unmeasured alternative.

The apparent same-individual persistence in this Greenland white-fronted goose source must thus be read as a **source-specific stratified calendar diagnostic and a negative control on feedback inference**, not a new species-general mechanism.

Additional caveat: the stage-5 departure SD varies across the five calendar years; standardizing within each year is necessary. The 2021 source study demonstrates that stable individual *temperature thresholds* can generate stable seasonal order while dates still change between years, further invalidating the facile inference of innate fixed annual departure timing from repeatability alone.
