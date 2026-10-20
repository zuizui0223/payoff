# M5_T0 gross-structure audit v1 result note

The public PacBio run `SRR16954720` was processed against `NC_003888.3` with the frozen v1 chromosome-scale audit.

Observed central depth was adequate (`92.1028x` for M5; `178.524x` for the WT control). Sniffles2 wrote three M5 calls with `--minsvlen 50000` and zero WT calls; under the v1 parser, the size-qualified catalog contains one resolved `83,009 bp` duplication. The two BND calls do not carry a v1 size estimate and are therefore not promoted into the size-qualified catalog.

The audit remains fail-closed because the frozen terminal-boundary rule requires exact zero depth throughout the deleted-side bins. Small terminal mapping traces remain on both sides, so neither boundary qualifies under v1.

This result means **R2 is unresolved under v1**. It does not mean M5 is biologically negative, structurally clean, or already qualified. No threshold relaxation is licensed from the M5 result itself.
