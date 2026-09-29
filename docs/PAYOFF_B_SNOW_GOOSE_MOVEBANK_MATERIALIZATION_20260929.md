# PAYOFF-B Greater Snow Goose Movebank materialization

Date: **2026-09-29**  
Role: **operational data access only; no scientific outcome fitting**

## Why this is separate from the science workflow

The greater-snow-goose cue-uptake analysis is already frozen at:

`freeze/payoff-b-snow-goose-preoutcome-v2-20260929`

Raw Movebank access is an operational dependency. It must not change the
registered model, route contexts, climate definition, estimability gate or
threshold rule.

An unauthenticated study-metadata probe returned HTTP 401, so an authenticated
Movebank account/session is required before event-data access can be tested.

## License handling

Movebank can require users to read and accept study-specific license terms
before the first download. The PAYOFF-B materializer **never accepts terms
automatically**.

Before running it:

1. sign in to Movebank with the authorized account;
2. initiate the study download in Movebank and read/accept any required terms;
3. obtain an API token using Movebank's documented token flow;
4. place that token in the local environment as `MOVEBANK_API_TOKEN`.

Do not paste a password or token into the repository, an issue, a PR, or chat.

## Local-only raw download

Run from a protected local environment and choose a directory **outside** the
Git checkout:

```bash
export MOVEBANK_API_TOKEN='...'
python scripts/payoff_b_greater_snow_goose_movebank_materialize.py \
  --output-dir /path/to/protected/snow_goose_raw
```

The script requests GPS sensor type 653 for study 1442516400, one complete
calendar year at a time for 2019–2023.

Every year is stored separately and recorded in a nonraw manifest with:

- row count;
- byte count;
- SHA-256;
- returned column header;
- requested timestamp bounds.

The raw CSVs are **never** intended for Git, GitHub Actions artifacts, or other
redistribution surfaces.

## Fail-closed behavior

The run stops without silently changing scope when:

- the API token is missing;
- Movebank returns HTTP failure;
- study license terms are returned instead of data;
- the response lacks required event columns;
- a year contains zero GPS events.

If license terms are returned, accept them through the authorized Movebank
interface and rerun. The script does not perform legal acceptance on the
user's behalf.

## What happens after download

Successful raw materialization means only that movement events are locally
available. It does not open the cue-uptake coefficient.

The next scientific gate remains:

1. materialize the exact/source-released St. Lawrence, Nunavik and Baffin
   route polygons;
2. run the frozen `movepp` preprocessing;
3. construct the frozen NARR decision-day / historical-q table;
4. run the executor bound to the v2 preoutcome freeze.

Until the source geometry gate is satisfied, the focal behavioral result stays
unopened.
