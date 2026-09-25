# PAYOFF-B Aikens authentication blocker audit — 2026-09-24

## Result

The Aikens primary environment lane is no longer blocked by source identity,
manifest construction, source coverage, workflow plumbing, or anonymous
transport discovery.

The remaining blocker is **authentication only**.

The lambda outcome remains **unopened**.

## What is already resolved

The exact canonical source gate passes for:

- 64,539 GPS observations;
- 10,899 unique MODIS 250-m cells;
- 19,500 cell-years;
- 24 AppEEARS tasks;
- years 2005, 2006, 2008, 2009, 2010, 2015, 2016, 2017 and 2018;
- both preregistered development groups.

The exact-manifest artifact from workflow run `36014102013` confirms the
manifest/coverage gate but records:

```text
appeears_credentials_configured = false
network_submission_performed = false
lambda_outcome_opened = false
```

The live-smoke artifact from run `36014102064` records:

```text
status = SKIPPED_NO_APPEEARS_CREDENTIALS
network_submission_performed = false
lambda_outcome_opened = false
```

The anonymous S3 probe from run `36014101924` shows that both frozen MODIS
products require authenticated access:

- `MOD09Q1.061`: Requester Pays / authentication required;
- `MOD10A2.061`: authentication required.

Thus anonymous transport is not a valid substitute for the registered
AppEEARS/Earthdata route.

## What is still required

One of the workflow's already-declared authentication routes must be configured
in GitHub Actions secrets:

```text
APPEEARS_TOKEN
```

or

```text
EARTHDATA_USERNAME
EARTHDATA_PASSWORD
```

No other scientific change is required or permitted.

Once credentials are configured, the next authorized execution is:

```text
.github/workflows/payoff-b-aikens-appeears-full-extraction.yml
```

That workflow already freezes the exact manifest hash, the V061 primary
successor amendment, fixed 24-hour target selection, support thresholds, IRG
reconstruction lane, lambda fitting contract and preregistered contrast gate.

## Scientific stop rule

Do not change any of the following to work around the authentication blocker:

- hypothesis;
- phase coordinate;
- fixed 24-hour interval;
- support thresholds;
- significance threshold;
- environmental product pair;
- group definitions;
- lambda gate direction.

The correct state is:

```text
source gate = PASS
manifest gate = PASS
authentication = MISSING
environmental extraction = NOT RUN
lambda outcome = UNOPENED
```

This is a transport/credential blocker, not a negative scientific result and not
an estimability result.


## 2026-09-25 credential-only recheck

A network-free GitHub Actions preflight rechecked the current repository secret
state without submitting an AppEEARS task or opening any environmental value:

```text
workflow = payoff-b Aikens credential preflight
run = 36113621057
artifact = 10853764396
artifact_sha256 = 4dd3e148c57fdb96c5bb92a8d96236bf05f123c361be94bc8ea6f12f6b0df471
status = NOT_CONFIGURED
credential_route = none
network_submission_performed = false
environmental_values_opened = false
lambda_outcome_opened = false
```

Thus the 2026-09-24 diagnosis remains current on 2026-09-25: authentication is
still the only external execution blocker. No new scientific blocker was found
and no registered analysis setting was changed.

Machine receipt:

`data/payoff_b_aikens_credential_preflight_20260925.json`

## Machine-readable receipt

`data/payoff_b_aikens_auth_blocker_audit_20260924.json`
