# PAYOFF-B Hoge Veluwe Gate-A source result

Date: **2026-09-28**  
Status: **PARTIAL PASS — migrant source access blocked; Gate B closed**

The registered source-readiness workflow completed successfully at run
`36367383611` without opening any joined biological outcome.

## Certified coordinates

Three of the four registered coordinates are now source-certified.

### Fixed Ivory Coast cue

- source-faithful 1980–2015 extension complete;
- 36 annual values;
- exact frozen 20-day window beginning 18 February;
- exact 3×3 coarse-grid Ivory Coast proxy;
- all 36 years retrieved through the registered ERDDAP route;
- annual CSV SHA256:
  `14cf9d5d249e582cf07079f3724b227a835acae95c297e3e8a1bac1bede5cc31`.

The cue-extension firewall confirms that no resource, resident, migrant,
connectivity, reversal or history outcome was opened.

### Great-tit resident timing source

Registered Dryad file:

`Tbl_Fitness_GT_HV_FirstClutches_CSNot0_YrLargerThan1973_IncludeIs1.xlsx`

Certified properties:

- Dryad DOI: `10.5061/dryad.f1vhhmgx6`;
- Dryad version: 5;
- Dryad file id: `1179758`;
- bytes: 81,281;
- Dryad-declared and computed SHA256 both:
  `a6a08800d95d5c25ffce7fcb87df5ac91fa36790a72f220e2d407c49b1dc5db2`;
- digest match: **PASS**;
- transport: Zenodo record 5730499 used only as a byte transport after
  Dryad individual/archive download routes failed; acceptance required exact
  equality to the Dryad-declared SHA256;
- sheet: `Tbl_Fitness_GT_HV_FirstClutches`;
- columns: `YearOfBreeding`, `LayDateApril`,
  `NumberRecruitsAllBroodsSummed`;
- year coverage: **1973–2020**, 48 unique years.

### Caterpillar resource source

Registered Dryad file:

`Tbl_PeakDate_Biomass_HVLim.xlsx`

Certified properties:

- Dryad DOI: `10.5061/dryad.f1vhhmgx6`;
- Dryad version: 5;
- Dryad file id: `1179760`;
- bytes: 9,412;
- Dryad-declared and computed SHA256 both:
  `9f113eb3f95d239ac31652c4083a159d82dacb61355b03fa2f355a2733a0b984`;
- digest match: **PASS**;
- transport: the same digest-verified Zenodo record 5730499 fallback;
- sheet: `tbl_PeakDate_Biomass_HVLim`;
- columns: `Year`, `MidDate`;
- year coverage: **1985–2020**, 35 unique years.

## Blocked coordinate

The registered Tomotani migrant-timing archive resolves to the Marine Data
Archive file:

`Tomotani et al.zip`

with file id:

`VLIZ_00000444_5dd3fba4f38f8`.

The public landing page exposes an MDA **sendmail request form** and an MDA
**login form**, but no anonymous file route. The workflow therefore terminates
this coordinate as:

`MIGRANT_SOURCE_ACCESS_BLOCKED`

rather than substituting another migrant timing series.

## Gate state

```text
registered source overlap = 1985–2015
registered history span  = 1992–2015 (24 years)

cue                    = CERTIFIED
great-tit timing       = CERTIFIED
caterpillar resource   = CERTIFIED
flycatcher timing      = ACCESS_BLOCKED

Gate A                 = PARTIAL PASS / BLOCKED
Gate B reversal test   = CLOSED
Gate C history test    = CLOSED
```

No cross-source join, focal-partner mismatch, cue-resource connectivity,
breakpoint search or history model has been run.

## Interpretation

This is now a narrow external-access blocker, not a design or data-availability
problem. The lane can continue only when the exact registered MDA archive is
obtained through an authorized access/request route. Until then, the natural
hysteresis result remains unopened.
