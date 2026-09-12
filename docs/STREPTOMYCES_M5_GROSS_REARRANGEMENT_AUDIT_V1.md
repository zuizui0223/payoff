# Streptomyces M5_T0 gross-rearrangement audit boundary v1

Status: **DESIGN NOTE / DOES NOT CLOSE R2**.

The direct-mu reference gate blocks only while gross secondary rearrangement remains **unresolved**. It does not require pretending that M5_T0 differs from M145 only by the registered right-arm deletion.

For M5_T0, the source study already makes additional terminal structure plausible. The public PacBio lane must therefore answer a descriptive structural question before the living-reference realization assay:

```text
what gross chromosome-scale events are present at T0,
and are they sufficiently enumerated that the D-realization receipt is not carrying an uncharacterized genome-wide change?
```

A later executable audit should use the exact M5_T0 PacBio run `SRR16954720` and combine:

```text
1. chromosome-wide depth segmentation;
2. left- and right-terminal retained/deleted boundaries;
3. long-read split-alignment / large-SV calls;
4. explicit cataloguing of any additional >=50 kb event.
```

The marker-class and gross-structure gates remain separate. The already observed four-locus PacBio pattern is strong DEEP_CLASS corroboration but does not by itself resolve whole-chromosome structure.

A structural audit may eventually return `gross_secondary_rearrangement_unresolved = false` only if its data-quality gate passes and every detected gross event is catalogued. This status does **not** mean `no secondary rearrangement`; it means `no gross rearrangement remains uncharacterized at the declared resolution`.

Even a closed structural audit does not establish current stock access, 72 h viability, 120 h measurability, same-context realization `d`, or a qualified D reference.
