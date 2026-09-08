# PAYOFF empirical frequency-game reanalysis priority v1

Status: frozen execution order for Lane A numerical recovery. Priority is based on ability to produce an auditable frequency-response result, not on how strongly a system resembles the upstream architecture mechanism.

## Ranking criteria

Each candidate is assessed on five dimensions:

```text
F — direct frequency manipulation/measurement
Y — common reproductive/fitness outcome for both alternatives
M — enough distinct frequency contexts for model falsification
D — numerical data availability/readiness
C — ecological/mechanistic proximity to SCH/BALANCE/BITA
```

`C` is intentionally not allowed to dominate the ranking. A mechanism-proximate study with inaccessible or non-comparable outcomes may be less useful for immediate PAYOFF game-layer validation than a cleaner analogue.

## Priority 1 — Arabidopsis halleri trichome dimorphism

Primary anchor: Sato & Kudoh 2017, DOI `10.1086/692603`; Dryad `10.5061/dryad.53k2d`.

Assessment:

```text
F: high       — mesocosm frequency conditions plus natural patch-frequency evidence
Y: high       — flower and clone production reported for both morphs
M: to verify  — exact experimental composition levels await workbook inspection
D: high       — public 806.91 KB workbook identified; field, mesocosm and README sheets reported
C: medium     — herbivore-mediated defense polymorphism, not floral mutualist-antagonist architecture
```

Why first:

The same morph pair exhibits rare-morph reproductive advantage with `Phaedon brassicae` present and no detected rare-morph advantage with beetles absent. This makes it unusually suitable for testing whether frequency feedback itself switches with ecological context.

Current blocker:

```text
Dryad public file bytes require an authenticated download session in current tooling.
```

Execution immediately after acquisition:

```text
inspect README and sheet structure
freeze exact composition levels
construct morph-relative reproductive margins
preserve beetle-present versus beetle-absent contexts
test interaction / no-refit affine holdouts if frequency support permits.
```

## Priority 2 — Dactylorhiza sambucina flower-colour polymorphism

Primary anchor: Gigord, Macnair & Smithson 2001, DOI `10.1073/pnas.111162598`.

Assessment:

```text
F: very high  — five manipulated frequencies at fixed density
Y: high       — male and female reproductive-success measures for the two morphs
M: very high  — p=0.1,0.3,0.5,0.7,0.9 gives explicit interior holdouts
D: medium-low — numerical array values not yet recovered; paper figures available
C: low-medium — pollinator-mediated deceptive-orchid colour polymorphism, no antagonist architecture bridge
```

Why second:

This is currently the cleanest known plant design for an observed-range no-refit test. Freeze the secant through `p=0.1` and `p=0.9`, then use `0.3,0.5,0.7` as holdouts for each reproductive component.

Current blocker:

```text
recover numerical array-level values or a trustworthy machine-readable source.
```

Figure digitization is exploratory fallback only and must use the 2004 corrected Fig. 3b labels.

## Priority 3 — Primula farinosa scape-height polymorphism

Primary sequence: Toräng et al. 2006; Toräng, Ehrlén & Ågren 2008; Ågren et al. 2013.

Assessment:

```text
F: high but heterogeneous — experimental composition effect plus natural frequency-dependent selection
Y: potentially high       — pollination, seed predation and longer-term fitness components
M: context dependent      — support varies among populations/years/experiments
D: medium                 — 2008 publisher reports Figshare research data; file contents not yet inspected
C: very high              — closest recovered mutualist-antagonist floral analogue
```

Why third:

It is biologically the closest current analogue to the upstream SCH setting but is analytically harder. Published frequency dependence changes sign across years and populations, so a global pooled `eta` would be especially vulnerable to Simpson-type averaging and loss of ecological context.

Current blocker:

```text
inspect supporting-data files and establish whether both morphs have commensurable outcomes across frequency contexts.
```

## Secondary pool — do not execute before the top three

### Arabidopsis halleri optimal-foraging follow-up

Sato, Ito & Kudoh, Functional Ecology, associated Dryad DOI `10.5061/dryad.pn088`, provides source code plus four CSV files for a natural-population herbivore-foraging/demography model that supports negative frequency-dependent selection and coexistence.

Use later as a process-level validation after the direct 2017 reproductive-data reanalysis. It is closer to finite-population/dynamic mechanism testing but would be premature before the simpler frequency-response layer is checked.

### Arabidopsis halleri regression-FDS methodology dataset

A later Dryad package (`10.5061/dryad.zs7h44jdv`) provides code/data for estimating frequency-dependent selection gradients across empirical systems and includes an *A. halleri* application.

Use as an independent methodological cross-check, not as a substitute for the original 2017 raw-data analysis.

## Stop rule for analogue expansion

Do not add more Lane A systems merely to make the literature list longer once the following are satisfied:

```text
one mechanism-proximate analogue
one clean multi-frequency falsification analogue
one public-data context-switch analogue.
```

Those three roles are already represented by Primula, Dactylorhiza and Arabidopsis halleri respectively.

Further literature search should resume only if one of these candidates fails data recovery or reveals a design-level obstruction.

## Architecture-specific search remains separate

The priority ranking above is for generic Lane A game-layer recovery.

A separate search must look for Lane P candidates in which alternatives can be justified *a priori* as shared/integrated versus differentiated/released architectures and where relative fitness is measured across their frequencies.

Until such a system is found:

```text
PAYOFF_ARCHITECTURE_FREQUENCY_FEEDBACK_NOT_YET_IDENTIFIED
```

remains unchanged.
