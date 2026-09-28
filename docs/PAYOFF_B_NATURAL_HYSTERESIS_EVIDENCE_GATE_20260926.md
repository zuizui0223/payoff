# PAYOFF-B natural hysteresis evidence gate

Date: **2026-09-26**  
Status: **source-readiness audit; prevents empirical overclaiming**

## Direct-claim rule

Synthetic PAYOFF-B now predicts strict information-triggered timing hysteresis.
A natural dataset should not be called a direct test merely because it contains
phenology, climate and a long time series.

For the current 8-year predictive-connectivity coordinate, a direct natural
hysteresis analysis must support three temporally ordered regimes without using
the same years to define all of them:

    baseline information
    -> disrupted information
    -> recovered information.

The default readiness threshold is therefore three non-overlapping 8-year
blocks, or **24 years**, plus all of the following:

1. a cue or environmental state available before the focal commitment;
2. the later destination/resource state that cue is supposed to predict;
3. focal timing;
4. interacting partner/resource timing.

Interaction or demographic outcomes are highly valuable but are not a
substitute for the timing and information variables themselves.

This is a readiness criterion, not a claim that natural hysteresis must operate
on an eight-year biological timescale.

## Current empirical ladder

| system | span | what it contains | PAYOFF-B role | direct network hysteresis? |
|---|---:|---|---|---|
| Samplonius & Both manipulation | 2014–2015 | manipulated tit hatch timing + flycatcher arrival/settlement | decision-time information anchor | no |
| Dutch fatal competition | 2007–2016 | flycatcher arrival + tit phenology/density + mortality | interaction-timing consequence | no |
| broad migratory birds | 2002–2017 | source/destination green-up + arrival + speed | predictive-information test | no |
| wigeon | 2018–2020 outcomes | staging phase + historical route predictability | predictive-information / correction boundary | no |
| southern Sweden | 1969–2012 | resident and migrant laying phenology + spring temperature | long phenology contrast | no |
| Lund community | 1956–2012 | population dynamics + weather | long interaction-demography evidence | no |
| Dutch annual-cycle flycatchers | **1980–2015** | arrival, breeding, moult, African and Dutch temperature covariates | **best within-species information-timing candidate** | no partner timing |

No current candidate passes the full natural network-hysteresis gate.

## Why the 10-year Dutch competition series is not enough

The 2007–2016 study is excellent evidence that phenological synchrony changes
the ecological consequence of resident–migrant interaction. The paper reports
that spring temperature affected resident great-tit breeding phenology more
strongly than pied-flycatcher timing, and flycatcher mortality increased when
flycatcher arrival overlapped peak tit laying, especially at high tit density.

That is exactly the **interaction consequence** layer PAYOFF-B needs.

But ten annual points cannot independently estimate baseline, disruption and
recovery of an eight-year predictive relationship. Calling it hysteresis would
therefore use more mechanism than the data identify.

## Why the 44- and 57-year series still do not close the loop

The southern-Sweden data span 1969–2012 and contain laying dates for three
resident tit species and pied flycatchers. They establish a long resident–
migrant phenology contrast: tits advanced while flycatcher laying did not show
the same significant long-term response.

The 1956–2012 Lund series is even longer and supports negative effects of blue
and great tits on pied-flycatcher population dynamics.

Both pass the duration requirement, but neither archived design contains the
specific **pre-commitment remote information coordinate** required by the
current Bayesian mechanism.

Duration alone is therefore not enough.

## Best new candidate: Dutch annual-cycle data, 1980–2015

Tomotani et al. provide a 36-year pied-flycatcher annual-cycle dataset with
long-term male arrival estimates, female nest-building as an arrival proxy,
laying and hatching dates, and temperature covariates in the Netherlands and
Africa.

This passes the 24-year duration requirement for a **within-species**
information-timing test.

It is especially interesting because the published male arrival-to-breeding
interval is already non-monotone:

    shortened until around 2008
    -> lengthened after around 2008.

That reversal should not be relabelled hysteresis by itself. But it makes the
dataset the strongest current candidate for asking whether a change in
Africa-to-Netherlands environmental predictability precedes a change in the
arrival-to-breeding interval, and whether the timing state follows the same
path when predictability returns.

The archived focal Tomotani dataset itself lacks an interacting partner timing
series. However, an independent public Dryad archive now supplies same-site
Hoge Veluwe great-tit first-clutch phenology and caterpillar peak dates. This
removes the partner/resource variables as an intrinsic data-availability
blocker, but creates a stricter cross-source assembly requirement. The
registered source overlap now runs through 2015; after the fixed trailing-window
construction this yields a 1992–2015 primary history span of 24 annual
outcomes, matching the readiness threshold.

A prospective joined analysis is now frozen in
`data/payoff_b_hoge_veluwe_network_hysteresis_contract_20260927.json`.
It remains **PREOUTCOME** until the source files are materialized, hash-frozen,
and pass exact site/year/schema gates.

## Consequence for the paper

The empirical ladder is now explicit:

    predictive information
        broad birds: pooled positive association

    decision-time cue availability
        flycatcher manipulation: source-backed causal anchor

    post-error correction
        wigeon: registered connectivity interaction null

    interaction consequence
        tit-flycatcher synchrony: natural competition/mortality anchor

    long-term divergence
        Sweden / Lund: resident-migrant long-term contrasts

    network recovery hysteresis
        still prospective.

This is stronger than pretending one dataset verifies the whole mechanism.
Each empirical system identifies a different edge of the causal chain.

## Gate-A result — 2026-09-28

The source-readiness gate has now been executed without opening the joined
outcome.

Certified:

- fixed Ivory Coast cue, 1980–2015;
- Hoge Veluwe great-tit first-clutch source, 1973–2020;
- Hoge Veluwe caterpillar-peak source, 1985–2020.

The two Dryad files were recovered through a public Zenodo mirror only after
their bytes were verified against the authoritative Dryad SHA-256 digests.

The exact registered Tomotani migrant-timing archive resolves to
`Tomotani et al.zip` in the Marine Data Archive, but the current MDA landing
page exposes a sendmail request and a login route rather than an anonymous
download. Gate A therefore ends in:

```text
MIGRANT_SOURCE_ACCESS_BLOCKED
```

Gate B and Gate C remain closed. No cue–resource connectivity, network
breakpoint, resident–migrant mismatch or history coefficient has been opened.

See
`data/payoff_b_hoge_veluwe_source_gate_a_result_20260928.json`.

## Next execution target

The next data-analysis target is now the preregistered cross-source Hoge Veluwe
assembly, not a retuned version of the failed CV24C lane.

The frozen sequence is now:

    cue + resident + resource sources certified
    -> obtain exact registered Tomotani MDA archive
    -> certify migrant schema/year coverage
    -> only then test fixed African-cue / caterpillar-resource reversal
    -> only if that gate passes, open resident–migrant history test

The resident/resource series are independently sourced from the same Hoge
Veluwe system; they must not be inspected jointly with the migrant timing
outcome before the assembly contract is frozen.
