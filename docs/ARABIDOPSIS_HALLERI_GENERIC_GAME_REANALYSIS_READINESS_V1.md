# Arabidopsis halleri generic frequency-game reanalysis readiness v1

Status: high-priority public-data reanalysis handoff for herbivore-mediated frequency-dependent reproduction.

This system is a **generic two-morph frequency-game analogue**, not a PAYOFF shared-versus-differentiated architecture validation.

## Primary study and public data

Sato & Kudoh (2017), *The American Naturalist* 190:E67–E77, DOI `10.1086/692603`, studied a genetically based hairy versus glabrous trichome dimorphism in *Arabidopsis halleri* subsp. *gemmifera*.

The published field and mesocosm results establish:

```text
natural patches:
    morph frequency covaried with herbivore damage and rare morphs increased locally between survey years;

mesocosm with Phaedon brassicae present:
    rare-morph advantage occurred in defense-related outcomes and reproduction;

mesocosm without P. brassicae:
    rare-morph advantage was not detected;
    glabrous plants had higher reproduction regardless of frequency condition.
```

This makes the system particularly useful for testing **context-dependent frequency feedback**, including a predicted transition from nonzero frequency dependence under the specialist herbivore to a frequency-independent or much weaker response when that herbivore is absent.

The complete study data are archived in Dryad under DOI `10.5061/dryad.53k2d` as

```text
SatoKudoh_AmNatData.xls
```

and the Dryad record states that the workbook contains separate field-survey, mesocosm-experiment, and README sheets.

## Current acquisition state

The public Dryad metadata and file identity are recoverable, but the current Dryad file-download endpoint requires an authenticated download session in the tooling available here. Therefore:

```text
ARABIDOPSIS_HALLERI_PUBLIC_DATASET_METADATA_RECOVERED
ARABIDOPSIS_HALLERI_RAW_FILE_BYTES_NOT_YET_ACQUIRED_IN_CURRENT_SESSION
```

No numerical result is inferred from the abstract or metadata in place of the raw workbook.

## Prospective generic game analysis

Let the two morphs be

```text
H = hairy
G = glabrous.
```

For a reproductive outcome on a common scale define

```text
Delta(p)=fitness_H(p)-fitness_G(p),
```

where `p` is the hairy-morph frequency or the exact composition variable used in the mesocosm data.

The analysis must preserve the beetle treatment as a context variable rather than pooling it away:

```text
Delta_beetle(p)
Delta_no_beetle(p).
```

The main analogue question is whether the frequency-response slope changes with herbivore context.

A simple prospective interaction model is

```text
Delta(p, H)=alpha + beta_p p + beta_H H + beta_pH p H,
```

where `H` denotes the declared beetle context.

This model is only an empirical screen. If enough distinct composition levels are present, PAYOFF's stronger no-refit procedure should be used: freeze a line on designated training frequencies and reserve interior frequency settings as holdouts.

## Priority outcomes

Reproductive outcomes take priority over damage-only measures because PAYOFF's empirical frequency layer targets a relative fitness/reproductive margin.

Preferred order:

```text
1. flower production
2. clone production
3. a preregistered joint reproductive index only if biologically justified
4. leaf damage and herbivore abundance as mechanism-supporting secondary outcomes.
```

Do not silently convert leaf damage into fitness.

## Frozen adjudication questions after data acquisition

```text
1. What exact morph-frequency/composition levels were experimentally used?
2. Are both morphs represented on one common reproductive scale at each composition?
3. Are there enough distinct frequency settings for a no-refit interior holdout?
4. Does the beetle-present treatment show a strict frequency-response reversal in relative reproduction?
5. Is the frequency slope absent, weaker, or opposite when beetles are absent?
6. Does one pooled affine law fail because herbivore context changes the response?
7. Are individual/mesocosm identifiers available for correct dependence and uncertainty handling?
```

These questions are frozen before workbook inspection.

## Allowed claims if successful

Potential Lane A claims include:

```text
A_HERBIVORE_DEPENDENT_FREQUENCY_FEEDBACK_NUMERICALLY_RECOVERED
A_REPRODUCTIVE_RARE_MORPH_ADVANTAGE_NUMERICALLY_RECOVERED
A_CONTEXT_INTERACTION_IN_FREQUENCY_RESPONSE_RECOVERED
A_OBSERVED_RANGE_AFFINE_RESPONSE_COMPATIBLE_OR_REJECTED_BY_HOLDOUT
```

A particularly valuable result would be the same genetic morph pair showing a nonzero frequency-feedback response with the specialist herbivore and loss of that response without it. That would directly demonstrate that PAYOFF-like feedback can be an ecological state variable rather than a fixed property of the alternatives.

## Forbidden promotions

Even a successful numerical reanalysis does not establish:

```text
that hairy/glabrous are shared versus differentiated architectures;
SCH conflict load L;
BITA recovery R;
architecture cost K;
phi=sL-K;
PAYOFF architecture eta;
finite-population Moran process validity;
historical architecture splitting.
```

The trichome system is therefore an empirical test of frequency-game transportability and context dependence, not of the architecture bridge.

## Current readiness labels

```text
ARABIDOPSIS_HALLERI_PRIMARY_FREQUENCY_FEEDBACK_EVIDENCE_RECOVERED
ARABIDOPSIS_HALLERI_PUBLIC_DRYAD_WORKBOOK_IDENTIFIED
ARABIDOPSIS_HALLERI_FIELD_AND_MESOCOSM_SHEETS_REPORTED
ARABIDOPSIS_HALLERI_BEETLE_CONTEXT_CONTRAST_RECOVERED
ARABIDOPSIS_HALLERI_GENERIC_GAME_REANALYSIS_PREDECLARED
ARABIDOPSIS_HALLERI_RAW_FILE_BYTES_NOT_YET_ACQUIRED_IN_CURRENT_SESSION
ARABIDOPSIS_HALLERI_ARCHITECTURE_MAPPING_NOT_ESTABLISHED
```
