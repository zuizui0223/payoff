#!/usr/bin/env Rscript

# PAYOFF-B V7 USA-NPN source-coverage gate.
# Allowed: source spatial coverage counts only.
# Forbidden: historical phenology values, predictability, recovery, models.

options(stringsAsFactors = FALSE)

OUT <- file.path("outputs", "payoff_b_v7_usapn_source_gate")
dir.create(OUT, recursive = TRUE, showWarnings = FALSE)

wide_url <- "https://zenodo.org/records/10094686/files/nemes_et_al_bird_pheno_wide_2023.RDS?download=1"
wide_file <- file.path(OUT, "nemes_wide_2023.rds")

download.file(wide_url, wide_file, mode = "wb", method = "libcurl", quiet = FALSE)
wide <- readRDS(wide_file)
stopifnot(is.data.frame(wide))

required <- c("motusTagID","site_id_r1","site_id_r2","lon_r1","lat_r1","lon_r2","lat_r2")
missing <- setdiff(required, names(wide))
if (length(missing)) stop("Missing required columns: ", paste(missing, collapse=", "))

bbox <- list(
  south = 24.0625,
  north = 49.9375,
  west = -125.0208333333,
  east = -66.4791666666
)

inside_point <- function(lon, lat) {
  !is.na(lon) & !is.na(lat) &
    lon >= bbox$west & lon <= bbox$east &
    lat >= bbox$south & lat <= bbox$north
}

south_inside <- inside_point(wide$lon_r1, wide$lat_r1)
north_inside <- inside_point(wide$lon_r2, wide$lat_r2)
both_inside <- south_inside & north_inside

pair_key <- paste(wide$site_id_r1, wide$site_id_r2, sep=" -> ")

summary <- data.frame(
  metric = c(
    "total_individual_routes",
    "south_receivers_inside_prism_extent",
    "north_receivers_inside_prism_extent",
    "individual_routes_both_receivers_inside",
    "unique_route_pairs_total",
    "unique_route_pairs_both_receivers_inside",
    "species_both_receivers_inside"
  ),
  value = c(
    nrow(wide),
    sum(south_inside),
    sum(north_inside),
    sum(both_inside),
    length(unique(pair_key)),
    length(unique(pair_key[both_inside])),
    length(unique(as.character(wide$species[both_inside])))
  )
)

write.csv(summary, file.path(OUT, "source_coverage_summary.csv"), row.names=FALSE)

gate <- data.frame(
  criterion = c(
    "individual_routes_inside_at_least_50",
    "unique_route_pairs_inside_at_least_10",
    "species_inside_at_least_3"
  ),
  pass = c(
    sum(both_inside) >= 50,
    length(unique(pair_key[both_inside])) >= 10,
    length(unique(as.character(wide$species[both_inside]))) >= 3
  )
)
write.csv(gate, file.path(OUT, "source_coverage_gate.csv"), row.names=FALSE)

cat("V7_SOURCE_COVERAGE_ONLY=TRUE\n")
cat("HISTORICAL_PIXEL_VALUES_OPENED=FALSE\n")
cat("PREDICTABILITY_COMPUTED=FALSE\n")
cat("RECOVERY_OPENED=FALSE\n")
cat("MODEL_FITTED=FALSE\n")

if (!all(gate$pass)) quit(status=2)
