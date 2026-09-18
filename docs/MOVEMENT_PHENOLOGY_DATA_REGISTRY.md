# Movement–phenology macro data registry

Status: 2026-09-18.

| Source | Role | Coverage | Key variables | Access / current use |
|---|---|---|---|---|
| Amaral et al. 2025 / Dryad 10.5061/dryad.ttdz08m6w | Stage-1 direct reanalysis | 55 eastern North American migratory bird species, 2002–2017 | bird front speed/direction, green-up speed/direction, arrival date, green-up date, traits | Primary immediate dataset. Published code/data. Automated file download may require Dryad API authentication; analysis script assumes a local copy of data/final.rds. |
| br-amaral/BirdMigrationSpeed | Provenance / code audit | Same study | generating code, metadata, small trait tables | Public GitHub source. Used to freeze variable definitions and upstream filters. |
| eBird Status and Trends | Stage-2 global bird front | Current Status release: 52-week full-annual-cycle products for 2,980 globally modelled bird species | weekly abundance, occurrence, proportion-population | Requires an eBird Status and Trends access key. Use 27 km first for the pilot, then 9/3 km sensitivity. Treat this as cross-sectional/typical-year timing, not an annual historical panel. |
| MODIS MCD12Q2 v6.1 | Stage-2 environmental front | Global, 500 m, yearly 2001–2024 | Greenup, MidGreenup, Maturity, Peak, Senescence, Dormancy, EVI2 amplitude | Preferred vegetation phenology product. |
| AVONET | Trait moderators | All extant bird species | HWI, body mass, ecology, geography | Open-data trait source aligned to eBird taxonomy. |
| BIRDBASE | Trait / movement-strategy moderators | 11,589 bird species | movement strategy plus broad ecological/life-history traits | Candidate current global movement-strategy source; verify release terms before redistribution. |
| Movebank Data Repository | Stage-3 individual validation | 396 curated archived datasets, nearly 18,000 animals and 260 species as of Jan 2026 | GPS trajectories, timestamps, taxa; environmental annotation possible | Public archived datasets are reusable under dataset-specific licenses. Build a candidate registry before bulk acquisition. |

## Stage-1 variable contract

From data/final.rds:

~~~text
year
cell
species
cell_lat2
arr_GAM_mean
gr_mn
NArr
vArrMag
vArrAng
NGr
vGrMag
vGrAng
mig_cell
breed_cell
HWI
Body_mass_g
winlat
~~~

Derived fields:

~~~text
animal_speed       = vArrMag
environment_speed  = vGrMag
speed_ratio        = animal_speed / environment_speed
log_speed_ratio    = log(speed_ratio)
alignment          = cos((vArrAng - vGrAng) * pi / 180)
vector_mismatch    = sqrt(1 + speed_ratio^2 - 2*speed_ratio*alignment)
signed_lag         = arr_GAM_mean - gr_mn
abs_mismatch_days  = abs(signed_lag)
species_cell       = interaction(species, cell)
~~~

## Source-quality notes

The generating code and data dictionary disagree on the verbal sign of lag. Recompute signed lag from dates. The data dictionary also labels vArrAng/vGrAng as radians, but code/1_GetEstimates.R explicitly applies rad2deg() before storing them; Stage 1 therefore treats these fields as degrees.

The velocity-generating code filters bird arrival estimates to VALID_GAM == TRUE, vegetation cells to gr_ncell > 10000, requires at least five neighbours for velocity estimation, and sets velocity values above 3000 km/day to missing. Preserve these source decisions and report any additional filter separately.

## Global-stage minimum viable pilot

Do not begin with all available eBird species. Pilot a stratified set of migratory species with strong weekly seasonal displacement and reliable reviewed products, across at least three flyway/region groups. The output of the pilot is a reproducible front-extraction algorithm; only then expand taxonomically.
