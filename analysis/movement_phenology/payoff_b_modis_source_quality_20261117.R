#!/usr/bin/env Rscript
# PAYOFF-B environmental-only MODIS MCD12Q2 source QA, 2026-11-17.
# NO eBird arrival, bird range labels, species_Grid or individual tracking.
# Pre-analysis field/calendar/quality audit; no source-target correlations.
options(stringsAsFactors=FALSE)
SOURCE_COMMIT <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL <- paste0(
  "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
  SOURCE_COMMIT,"/data/for_green-up_dl.rds"
)
dir.create("outputs",recursive=TRUE,showWarnings=FALSE)
cache <- "outputs/modis_midgreenup_source_20261117.rds"
if (!file.exists(cache)) download.file(SOURCE_URL,cache,mode="wb",quiet=FALSE)
if (!file.exists(cache) || file.info(cache)$size<1000)
  stop("Public MODIS source RDS not downloaded")
x <- readRDS(cache)
if (!is.data.frame(x)) stop("Original source not a tabular dataset")
required <- c("year","cell","cell_lat","cell_lng","gr_mn","gr_ncell")
missing <- setdiff(required,names(x))
if (length(missing)) stop(paste("Original MODIS-only columns missing:",
                                paste(missing,collapse=",")))
if ("species" %in% names(x) || "arr_GAM_mean" %in% names(x) ||
    "mig_cell" %in% names(x) || "breed_cell" %in% names(x))
    stop("STOP: source unexpectedly contains bird/eBird response fields")
x$year <- as.integer(as.character(x$year))
x$cell <- as.numeric(as.character(x$cell))
x$cell_lat <- as.numeric(x$cell_lat)
x$cell_lng <- as.numeric(x$cell_lng)
x$gr_mn <- as.numeric(x$gr_mn)
x$gr_ncell <- as.numeric(x$gr_ncell)
if (any(!is.finite(x$year)) || any(!is.finite(x$cell)))
    stop("Original MODIS source has nonfinite year/cell keys")
samekey <- paste(x$year,x$cell,sep="|")
duplicate_keys <- sum(duplicated(samekey))
present <- x[is.finite(x$gr_mn)&is.finite(x$cell_lat)&
              is.finite(x$cell_lng)&
              is.finite(x$gr_ncell)&x$gr_ncell>0,]
coord <- unique(present[,c("cell","cell_lat","cell_lng")])
conflicting_coords <- sum(duplicated(coord$cell))
bycell <- table(present$cell)
byyear <- table(present$year)
metric <- data.frame(
 source_commit=SOURCE_COMMIT,
 source_kind="MODIS_MCD12Q2_MIDGREENUP_FOREST_ONLY",
 source_file="data/for_green-up_dl.rds",
 source_raw_bytes=file.info(cache)$size,
 source_sha256=trimws(system2("sha256sum",cache,stdout=TRUE)),
 source_rows=nrow(x),
 source_year_min=min(x$year),
 source_year_max=max(x$year),
 source_distinct_years=length(unique(x$year)),
 source_cells=length(unique(x$cell)),
 source_duplicate_cell_year_rows=duplicate_keys,
 source_conflicting_cell_coordinates=conflicting_coords,
 valid_midgreenup_records=nrow(present),
 valid_cells=length(unique(present$cell)),
 valid_years=length(unique(present$year)),
 cell_years_min=min(as.numeric(bycell)),
 cell_years_max=max(as.numeric(bycell)),
 latitude_min=min(present$cell_lat),
 latitude_max=max(present$cell_lat),
 longitude_min=min(present$cell_lng),
 longitude_max=max(present$cell_lng),
 median_original_pixels=median(present$gr_ncell),
 min_original_pixels=min(present$gr_ncell),
 no_eBird_or_bird_data_fields=TRUE,
 environmental_delta_rho_not_computed=TRUE
)
write.csv(metric,"outputs/payoff_b_modis_source_quality.csv",row.names=FALSE)
cat("PAYOFF-B MODIS SOURCE PREOUTCOME FIELD QUALITY\n")
print(metric,row.names=FALSE)
cat("YEAR ROW FREQUENCIES:\n")
print(byyear)
if (duplicate_keys>0 || conflicting_coords>0)
    stop("MODIS cell-year or environmental coordinates inconsistent")
cat("No environmental correlations have been computed.\n")
