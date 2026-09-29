# Authorized Movebank fetch route for greater snow goose

Date: **2026-09-29**  
Status: **implementation ready; credentials and license acceptance remain user-controlled**

The preregistered greater-snow-goose cue-uptake lane is blocked because
unauthenticated Movebank study metadata return HTTP 401. This utility prepares
the authorized route without weakening the scientific contract.

## Script

`scripts/fetch_greater_snow_goose_movebank_authorized.py`

The script requires:

- `MOVEBANK_USERNAME`
- `MOVEBANK_PASSWORD`

and a user-selected `--output-dir`.

Default execution is **metadata only**. GPS events are requested only when the
operator explicitly supplies `--download-events`.

## License rule

The script never auto-accepts Movebank license terms.

If an event request returns a page containing `License Terms:`, the script:

1. saves the returned terms to `movebank_license_terms.html`;
2. records `LICENSE_TERMS_ACCEPTANCE_REQUIRED` in the manifest;
3. stops before writing any event CSV.

The operator must review and explicitly accept the study terms through
Movebank, then rerun the script. This deliberately differs from Movebank's
example Python wrapper, which demonstrates programmatic MD5 acceptance.

## Download gate

Before any event request, authenticated study metadata must report

`i_have_download_access=true`.

If this is not true, the script stops.

## Event files

When explicitly authorized, GPS events are downloaded per individual using GPS
sensor type 653 with at least:

- timestamp;
- latitude;
- longitude;
- visibility/outlier flag;
- stable individual local identifier;
- internal individual/deployment/tag IDs for the current fetch.

Each CSV receives a SHA-256 receipt in
`movebank_fetch_manifest.json`.

Raw files remain outside the Git repository unless a human explicitly moves
them. They must not be added to PAYOFF-B source control.

## Scientific boundary

Downloading authorized events does not open the focal statistical outcome by
itself. After download, the frozen sequence remains:

1. source-faithful movepp preprocessing;
2. source-backed route-context assignment;
3. historical NARR predictive-connectivity construction;
4. decision-day table construction;
5. preregistered estimability gate;
6. primary cue-uptake model;
7. secondary behavioral threshold only if the primary lane is estimable.

The direct (D\rightarrow q_{wait}) theorem remains untested unless clean
delay-cost and state-loss quantities are independently identified.
