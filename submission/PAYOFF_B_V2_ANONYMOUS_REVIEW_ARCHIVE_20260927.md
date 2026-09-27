# PAYOFF-B V2 anonymous reviewer archive — PREOUTCOME

Frozen: **2026-09-27**

Status: **PASS — anonymous code/data archive content ready**

The canonical information-coordination V2 reviewer archive has been built and
tested independently of the journal-facing manuscript package.

## Verified build

```text
workflow_run = 36311421594
head = 1f53201f4211f24a15256e7329232e340c52fe83
status = SUCCESS
artifact_id = 10928629032
artifact_sha256 = 3fa84755f482d63dc1523b18892bedb1b178d1701b7fde7deef410c8cbfaa74e
```

Inner deterministic archive:

```text
file = PAYOFF_B_V2_ANON_REVIEW_CODE_DATA_PREOUTCOME.zip
sha256 = da7fa4da41a6febaeb8c88bc00aeff55360673e782b9ae8e4348a2d7a049df21
files = 34
code_files = 17
```

## Anonymous-content gate

The bundle excludes:

- author names;
- email addresses;
- repository-owner identifiers;
- title-page / acknowledgement / funding metadata;
- publication-state bookkeeping;
- GitHub Actions workflow files;
- credential or secret material.

It contains the manuscript-facing theory and analysis code, frozen
registrations, frozen derived result receipts, theory notes and deterministic
figure builders.

## Aikens boundary

This is a **PREOUTCOME** reviewer archive.

The registered industrial-development phase-retention result is not included.
After that gate is adjudicated, the same builder is already connected to the
authenticated Aikens workflow and will regenerate the archive with the frozen
result JSON included.

## Remaining reviewer-link blocker

The archive bytes are ready.

What remains external is only to place the final regenerated ZIP at an
anonymous stable reviewer-access URL accepted for peer review.

A temporary GitHub Actions artifact is provenance, not the final stable reviewer
link.
