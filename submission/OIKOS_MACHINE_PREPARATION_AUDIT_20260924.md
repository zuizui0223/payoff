# Oikos machine-preparation audit — PAYOFF-B tracking theory

Audited: **2026-09-24**

Branch:

`feature/payoff-b-migration-phenology-20260919`

Audited HEAD:

`2df627ecce2f27d884f617d7b0e2898b10fcfb68`

Canonical successful PR workflow run:

`35999337326`

Workflow conclusion: **success**

## CI status

The complete repository workflow finished successfully at the audited HEAD.

In particular:

- `pytest -q`: PASS;
- frozen figure-data generation: PASS;
- six SVG figure rendering: PASS;
- submission-package builder: PASS;
- anonymous code/data review-bundle builder: PASS;
- all later smoke steps in the repository workflow: PASS.

The immediately preceding push run at the same HEAD completed every scientific
and packaging step successfully before concurrency handed control to the PR run;
the PR run is the canonical green receipt.

## Canonical artifacts

### Main submission package

GitHub artifact:

- name: `payoff-b-tracking-theory-submission-package`;
- artifact ID: `10807716748`;
- outer artifact SHA256:
  `b5a24ef5dd044a89e047f950057342263cd8589699d369728f349752a007be18`.

Deterministic inner archive:

- file: `PAYOFF_B_TRACKING_SUBMISSION_PACKAGE.zip`;
- SHA256:
  `062262cafba85c7957094173075964aa0e3d5d2ac775da3335724aaafd4f17da`;
- payload files: **40**;
- rendered SVG figures: **6**;
- per-file manifest hash mismatches: **0**.

Archive receipt:

- package-manifest SHA256:
  `277e1be119f59f98b349e267068929b9099c461c654621924d7505a5f93374dc`;
- fixed archive timestamp: `2026-09-24T00:00:00`.

The same deterministic inner archive SHA256 was independently produced by the
same-HEAD push run, confirming byte-stable packaging across workflow events.

### Anonymous synthetic code/data review bundle

GitHub artifact:

- name: `payoff-b-tracking-theory-anonymous-review-bundle`;
- artifact ID: `10807746767`;
- outer artifact SHA256:
  `f90c0515b0c2d4e5c7b94502075e6bc51d4dc5f07de43568b4c4bbe17f001896`.

Deterministic inner archive:

- file: `OIKOS_TRACKING_ANON_CODE_DATA.zip`;
- SHA256:
  `d75d914ff2e05d25a4fa571d8a48b0dec5bd3d34416132a7ab2eccaf67fa9d4a`;
- payload files: **58**;
- Python code files: **41**;
- third-party import roots detected: **none**;
- per-file manifest hash mismatches: **0**.

Anonymity / evidence-lane audit:

- empirical-programme paths: **0**;
- author-name tokens: **0**;
- repository-owner tokens: **0**;
- email-address matches: **0**.

The same deterministic inner archive SHA256 was independently produced by the
same-HEAD push run.

### Main figures

GitHub artifact:

- name: `payoff-b-tracking-theory-figures`;
- artifact ID: `10807602200`;
- outer artifact SHA256:
  `4578897d632fa64d237b05b6c786238a4824ff57f7d1cb06ff3ec63c565103c1`.

The scientific figure-content audit remains governed by
`submission/PAYOFF_B_TRACKING_FIGURE_VISUAL_AUDIT.md`.

## RTF rendering audit

The generated RTF files were rendered through LibreOffice to PDF and visually
inspected after the final first-page layout repair.

### Anonymous main text

File:

`OIKOS_TRACKING_ANON_MAIN_TEXT.rtf`

Rendered PDF:

- pages: **27**;
- page size: US Letter;
- page numbers: present;
- continuous line numbers: present;
- body text: double spaced;
- title + complete 295-word abstract + keywords: contained on page 1;
- Introduction: begins on page 2;
- author names / affiliations: absent;
- internal claim-freeze and prior-art file paths: absent;
- References, AI-use statement and Figure legends: present;
- clipped or overlapping text: not observed.

The final page contains the concluding lines of the Figure 6 legend; it is not
an empty trailing page.

### Supporting Information

File:

`OIKOS_TRACKING_SUPPORTING_INFORMATION.rtf`

Rendered PDF:

- pages: **10**;
- page numbers: present;
- sections S1–S8: present;
- frozen provenance and claim boundary: present;
- clipped or overlapping text: not observed.

## Current submission boundary

The synthetic theory is mechanically ready for Oikos initial-submission
assembly.

Remaining inputs are human/administrative metadata that cannot be safely
inferred from the scientific repository:

- final author list and order;
- affiliations and corresponding-author details;
- ORCID;
- funding;
- competing interests;
- ethics statement if required;
- acknowledgments;
- CRediT roles;
- final portal entry/upload actions.

No additional synthetic simulation is licensed by this audit.
