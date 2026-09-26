#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

SOURCE_COMMIT <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL <- paste0(
  "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
  SOURCE_COMMIT,
  "/data/final.rds"
)
WINDOW_YEARS <- 8L
MIN_PAIRS <- 6L

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
cache <- "outputs/amaral_final_frozen.rds"
if (!file.exists(cache)) {
  download.file(SOURCE_URL, cache, mode = "wb", quiet = FALSE)
}

dat <- readRDS(cache)

required <- c(
  "species", "year", "cell", "cell_lat2", "cell_lng",
  "arr_GAM_mean", "gr_mn", "vArrMag", "AnomDGr",
  "mig_cell", "breed_cell"
)
missing <- setdiff(required, names(dat))
if (length(missing) > 0) {
  stop("Missing required columns: ", paste(missing, collapse = ", "))
}

truthy <- function(x) {
  toupper(as.character(x)) %in% c("TRUE", "T", "1")
}

haversine_km <- function(lat1, lon1, lat2, lon2) {
  rad <- pi / 180
  p1 <- lat1 * rad
  p2 <- lat2 * rad
  dp <- (lat2 - lat1) * rad
  dl <- (lon2 - lon1) * rad
  a <- sin(dp / 2)^2 + cos(p1) * cos(p2) * sin(dl / 2)^2
  6371.0088 * 2 * atan2(sqrt(a), sqrt(pmax(0, 1 - a)))
}

detrended_rho <- function(year, origin, destination) {
  keep <- is.finite(year) & is.finite(origin) & is.finite(destination)
  year <- year[keep]
  origin <- origin[keep]
  destination <- destination[keep]
  if (length(year) < MIN_PAIRS) return(NA_real_)
  if (length(unique(year)) != length(year)) return(NA_real_)
  ro <- resid(lm(origin ~ year))
  rd <- resid(lm(destination ~ year))
  if (sd(ro) <= 0 || sd(rd) <= 0) return(NA_real_)
  cor(ro, rd)
}

cells <- unique(dat[, c("species", "cell", "cell_lat2", "cell_lng", "mig_cell", "breed_cell")])
cells$cell <- as.numeric(as.character(cells$cell))
cells$cell_lat2 <- as.numeric(cells$cell_lat2)
cells$cell_lng <- as.numeric(cells$cell_lng)
cells$is_mig <- truthy(cells$mig_cell)
cells$is_breed <- truthy(cells$breed_cell)

targets <- cells[cells$is_breed, c("species", "cell", "cell_lat2", "cell_lng")]
targets <- targets[order(targets$species, targets$cell), ]

mapping <- vector("list", nrow(targets))
map_n <- 0L
for (i in seq_len(nrow(targets))) {
  target <- targets[i, ]
  candidates <- cells[
    cells$species == target$species &
      cells$is_mig &
      is.finite(cells$cell_lat2) &
      cells$cell_lat2 < target$cell_lat2,
    c("cell", "cell_lat2", "cell_lng")
  ]
  if (nrow(candidates) == 0) next
  candidates$distance_km <- haversine_km(
    candidates$cell_lat2,
    candidates$cell_lng,
    target$cell_lat2,
    target$cell_lng
  )
  candidates <- candidates[order(candidates$distance_km, candidates$cell), ]
  source <- candidates[1, ]
  map_n <- map_n + 1L
  mapping[[map_n]] <- data.frame(
    species = target$species,
    target_cell = target$cell,
    source_cell = source$cell,
    source_lat = source$cell_lat2,
    source_lon = source$cell_lng,
    target_lat = target$cell_lat2,
    target_lon = target$cell_lng,
    source_target_distance_km = source$distance_km
  )
}
mapping <- do.call(rbind, mapping[seq_len(map_n)])
if (is.null(mapping) || nrow(mapping) == 0) stop("No source-target mappings")

green <- unique(dat[, c("year", "cell", "gr_mn")])
green$year <- as.integer(green$year)
green$cell <- as.numeric(as.character(green$cell))
green$gr_mn <- as.numeric(green$gr_mn)
green <- green[is.finite(green$gr_mn), ]

outcome <- dat[
  truthy(dat$breed_cell) &
    is.finite(as.numeric(dat$arr_GAM_mean)) &
    is.finite(as.numeric(dat$gr_mn)) &
    is.finite(as.numeric(dat$vArrMag)) &
    as.numeric(dat$vArrMag) > 0 &
    is.finite(as.numeric(dat$AnomDGr)),
  ]
outcome$year <- as.integer(outcome$year)
outcome$cell <- as.numeric(as.character(outcome$cell))
outcome$arr_GAM_mean <- as.numeric(outcome$arr_GAM_mean)
outcome$gr_mn <- as.numeric(outcome$gr_mn)
outcome$vArrMag <- as.numeric(outcome$vArrMag)
outcome$AnomDGr <- as.numeric(outcome$AnomDGr)

outcome <- merge(
  outcome,
  mapping,
  by.x = c("species", "cell"),
  by.y = c("species", "target_cell"),
  all = FALSE
)

connectivity <- rep(NA_real_, nrow(outcome))
training_n <- integer(nrow(outcome))

for (i in seq_len(nrow(outcome))) {
  yr <- outcome$year[i]
  source <- green[
    green$cell == outcome$source_cell[i] &
      green$year >= yr - WINDOW_YEARS &
      green$year < yr,
    c("year", "gr_mn")
  ]
  target <- green[
    green$cell == outcome$cell[i] &
      green$year >= yr - WINDOW_YEARS &
      green$year < yr,
    c("year", "gr_mn")
  ]
  names(source)[2] <- "origin"
  names(target)[2] <- "destination"
  paired <- merge(source, target, by = "year", all = FALSE)
  training_n[i] <- nrow(paired)
  if (nrow(paired) >= MIN_PAIRS) {
    connectivity[i] <- detrended_rho(
      paired$year,
      paired$origin,
      paired$destination
    )
  }
}

outcome$connectivity_rho <- connectivity
outcome$connectivity_training_n <- training_n
analysis <- outcome[
  is.finite(outcome$connectivity_rho) &
    outcome$year >= 2010,
]
if (nrow(analysis) < 100) stop("Fewer than 100 estimable outcome rows")

analysis$primary_response <- log1p(
  abs(analysis$gr_mn - analysis$arr_GAM_mean)
)
analysis$z_connectivity <- as.numeric(scale(analysis$connectivity_rho))
analysis$z_destination_greenup_anomaly <- as.numeric(scale(analysis$AnomDGr))
analysis$z_bird_speed <- as.numeric(scale(log(analysis$vArrMag)))
analysis$species <- factor(analysis$species)
analysis$species_cell <- factor(paste(analysis$species, analysis$cell, sep = "_"))
analysis$year_factor <- factor(analysis$year)

if (!requireNamespace("mgcv", quietly = TRUE)) {
  stop("mgcv is required")
}

fit <- mgcv::gam(
  primary_response ~
    z_connectivity +
    z_destination_greenup_anomaly +
    z_bird_speed +
    s(year_factor, bs = "re") +
    s(species_cell, bs = "re") +
    s(species, bs = "re"),
  data = analysis,
  method = "REML"
)

coef_table <- summary(fit)$p.table
if (!"z_connectivity" %in% rownames(coef_table)) {
  stop("z_connectivity coefficient missing from fitted model")
}

estimate <- unname(coef_table["z_connectivity", "Estimate"])
se <- unname(coef_table["z_connectivity", "Std. Error"])
p_value <- unname(coef_table["z_connectivity", "Pr(>|t|)"])
ci_low <- estimate - 1.96 * se
ci_high <- estimate + 1.96 * se
supported <- is.finite(estimate) && estimate < 0 && ci_high < 0

summary_row <- data.frame(
  source_commit = SOURCE_COMMIT,
  window_years = WINDOW_YEARS,
  min_training_pairs = MIN_PAIRS,
  analysis_rows = nrow(analysis),
  species = length(unique(analysis$species)),
  species_cells = length(unique(analysis$species_cell)),
  years = length(unique(analysis$year)),
  connectivity_mean = mean(analysis$connectivity_rho),
  connectivity_sd = sd(analysis$connectivity_rho),
  connectivity_min = min(analysis$connectivity_rho),
  connectivity_max = max(analysis$connectivity_rho),
  coefficient = estimate,
  standard_error = se,
  ci_low_95 = ci_low,
  ci_high_95 = ci_high,
  p_value_two_sided = p_value,
  registered_direction = "negative",
  support_status = ifelse(supported, "SUPPORTED", "NOT_SUPPORTED")
)

write.csv(
  summary_row,
  "outputs/payoff_b_broad_predictive_connectivity_result.csv",
  row.names = FALSE
)

analysis$cell_year <- factor(paste(analysis$cell, analysis$year, sep = "_"))
analysis$source_target_pair <- factor(
  paste(analysis$source_cell, analysis$cell, sep = "_")
)
audit_rows <- analysis[, c(
  "species", "year", "cell", "source_cell",
  "species_cell", "cell_year", "source_target_pair",
  "connectivity_rho", "connectivity_training_n",
  "primary_response", "gr_mn", "arr_GAM_mean", "vArrMag", "AnomDGr",
  "z_connectivity", "z_destination_greenup_anomaly", "z_bird_speed",
  "source_target_distance_km"
)]
write.csv(
  audit_rows,
  "outputs/payoff_b_broad_predictive_connectivity_rows.csv",
  row.names = FALSE
)

cat("PAYOFF-B BROAD PREDICTIVE CONNECTIVITY\n")
print(summary_row)
