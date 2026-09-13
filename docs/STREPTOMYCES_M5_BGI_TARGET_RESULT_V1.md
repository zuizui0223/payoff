# Streptomyces M5_T0 primary BGI target result v1

Status: **TARGET OPENED UNDER FROZEN CALIBRATION; REGISTERED CLASS UNRESOLVED**.

The M5 BGI target (`SRR16954696`) was opened only after the six-control response-blind calibration qualified and the registered target-opening gate returned `target_opening_allowed = true`.

The frozen thresholds were:

```text
ABSENT  if ratio <= 0.000818710126322
PRESENT if ratio >= 0.40016549829
otherwise UNRESOLVED
```

Using the frozen nine-locus central-core median (`138.64988009592327x`), the primary BGI marker ratios were:

```text
SCO7662  0.0006117397433800187  -> ABSENT
SCO7350  0.0                    -> ABSENT
SCO7036  0.000997567299370736   -> UNRESOLVED
SCO3879  1.0833254422202168     -> PRESENT
```

`SCO7036` lies only about 1.218x above the frozen absence ceiling, but the registered rule has no near-threshold rescue clause. It is also about 401x below the presence floor. The result is therefore genuinely unresolved, not DEEP.

This is especially informative because the independent PacBio lane gives 0% coverage at `SCO7036` and corroborates the full DEEP pattern. That orthogonal evidence remains useful corroboration, but there was no pre-registered rule allowing PacBio to replace an unresolved primary BGI call after target opening. Doing so now would be post hoc rescue.

Consequences:

```text
M5 primary BGI class            UNRESOLVED
registered D class qualified    NO
qualified D-reference count     0
R2                              OPEN
physical stock access           UNCONFIRMED
72->120 h realization d         UNMEASURED
architecture-specific inference HARD CLOSED
```

The next permitted action is current material-access confirmation. If the archived M5_T0 material is available, an independent orthogonal material-genotyping assay must be prospectively registered before observing its outcome, alongside the matched 72->120 h realization assay. If material access is unavailable or declined, the frozen candidate queue advances to `W3_POST_DELETION`; the literature pool does not expand merely because M5 was unresolved.
