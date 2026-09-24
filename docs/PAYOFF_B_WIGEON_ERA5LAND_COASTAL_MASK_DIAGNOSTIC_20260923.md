# PAYOFF-B wigeon ERA5-Land coastal-mask diagnostic

Frozen: **2026-09-23**

Status: **post-hoc diagnosis complete; coastal nearest-cell explanation not supported**.

The registered ERA5-Land calibration left 36 of 256 staging events without
finite January--July temperatures. All 36 requests returned HTTP 200, including
single-location retries.

Because several missing locations were coastal, we tested one narrow technical
hypothesis after the registered calibration had already failed:

> did `cell_selection=nearest` choose an ocean-masked ERA5-Land cell?

The diagnostic repeated only those 36 failed coordinate-year requests with the
same provider, ERA5-Land model, date window, temperature variable, GMT timezone
and disabled elevation downscaling, changing only:

```text
nearest -> land
```

Result:

```text
registered valid events:    220
registered missing events:   36

land-cell events recovered:   0 / 36
recovery fraction:            0.0
counterfactual coverage:      0.859375
```

Thus the simple coastal/ocean-cell explanation is **not supported**. The
missingness remains an unresolved provider/model response or availability issue
for those coordinate-year requests.

No replacement values are introduced and the frozen calibration remains:

```text
REGISTERED ERA5-Land CALIBRATION:
    FAIL
```

The useful evidence remains the 220 paired events and the explicitly labeled
measurement-error sensitivity analyses. This diagnostic cannot retroactively
satisfy the 90% coverage gate.
