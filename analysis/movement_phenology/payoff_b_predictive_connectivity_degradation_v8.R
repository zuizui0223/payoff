#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

SOURCE_COMMIT <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL <- paste0(
  "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
  SOURCE_COMMIT,
  "/data/final.rds"
)

EARLY_YEARS <- 2002:2009
LATE_YEARS <- 2010:2017
MIN_PAIRS <- 6L
BOOT_MIXED <- 1000L
BOOT_SPECIES <- 10000L
SEED <- 20261005L

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
cache <- "outputs/amaral_final_v8_frozen.rds"
if (!file.exists(cache)) {
  download.file(SOURCE_URL, cache, mode = "wb", quiet = FALSE)
}

dat <- readRDS(cache)

required <- c(
  "species", "year", "cell", "cell_lat2", "cell_lng",
  "gr_mn", "mig_cell", "breed_cell"
)
missing <- setdiff(required, names(dat))
if (length(missing) > 0) {
  stop("Missing required V8 environmental fields: ", paste(missing, collapse = ", "))
}

# Guard against accidental use of bird-outcome variables.
forbidden_used <- c("arr_GAM_mean", "vArrMag", "AnomDGr")
# Their presence in the source object is allowed; the script never reads them.

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

detrended_rho <- function(year, origin, destination, min_pairs = MIN_PAIRS) {
  keep <- is.finite(year) & is.finite(origin) & is.finite(destination)
  year <- as.numeric(year[keep])
  origin <- as.numeric(origin[keep])
  destination <- as.numeric(destination[keep])
  if (length(year) < min_pairs) return(c(rho = NA_real_, n = length(year)))
  if (length(unique(year)) != length(year)) {
    stop("Duplicate year within one V8 source-target window")
  }
  ro <- resid(lm(origin ~ year))
  rd <- resid(lm(destination ~ year))
  if (sd(ro) <= 0 || sd(rd) <= 0) {
    return(c(rho = NA_real_, n = length(year)))
  }
  c(rho = cor(ro, rd), n = length(year))
}

# Rebuild the exact frozen source-target mapping from the prior broad analysis.
cells <- unique(dat[, c(
  "species", "cell", "cell_lat2", "cell_lng", "mig_cell", "breed_cell"
)])
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
    species = as.character(target$species),
    target_cell = as.numeric(target$cell),
    source_cell = as.numeric(source$cell),
    source_lat = as.numeric(source$cell_lat2),
    source_lon = as.numeric(source$cell_lng),
    target_lat = as.numeric(target$cell_lat2),
    target_lon = as.numeric(target$cell_lng),
    source_target_distance_km = as.numeric(source$distance_km)
  )
}
mapping <- do.call(rbind, mapping[seq_len(map_n)])
if (is.null(mapping) || nrow(mapping) == 0) stop("No frozen V8 source-target mappings")

# Environmental data only.
green <- unique(dat[, c("year", "cell", "gr_mn")])
green$year <- as.integer(green$year)
green$cell <- as.numeric(as.character(green$cell))
green$gr_mn <- as.numeric(green$gr_mn)
green <- green[is.finite(green$year) & is.finite(green$cell) & is.finite(green$gr_mn), ]

# Fail if the source object contains conflicting green-up values for a cell-year.
dup_key <- paste(green$cell, green$year, sep = "_")
if (anyDuplicated(dup_key)) {
  split_vals <- split(green$gr_mn, dup_key)
  conflict <- any(vapply(split_vals, function(x) length(unique(x)) > 1, logical(1)))
  if (conflict) stop("Conflicting green-up values within cell-year")
  green <- green[!duplicated(dup_key), ]
}

window_rho <- function(source_cell, target_cell, years_keep) {
  source <- green[
    green$cell == source_cell & green$year %in% years_keep,
    c("year", "gr_mn")
  ]
  target <- green[
    green$cell == target_cell & green$year %in% years_keep,
    c("year", "gr_mn")
  ]
  names(source)[2] <- "origin"
  names(target)[2] <- "destination"
  paired <- merge(source, target, by = "year", all = FALSE)
  detrended_rho(paired$year, paired$origin, paired$destination)
}

rows <- vector("list", nrow(mapping))
for (i in seq_len(nrow(mapping))) {
  er <- window_rho(mapping$source_cell[i], mapping$target_cell[i], EARLY_YEARS)
  lr <- window_rho(mapping$source_cell[i], mapping$target_cell[i], LATE_YEARS)
  rows[[i]] <- cbind(
    mapping[i, ],
    early_rho = unname(er["rho"]),
    early_n = as.integer(unname(er["n"])),
    late_rho = unname(lr["rho"]),
    late_n = as.integer(unname(lr["n"]))
  )
}
pair_all <- do.call(rbind, rows)

eligible <- pair_all[
  is.finite(pair_all$early_rho) &
    is.finite(pair_all$late_rho) &
    pair_all$early_n >= MIN_PAIRS &
    pair_all$late_n >= MIN_PAIRS,
]
eligible$delta_rho <- eligible$late_rho - eligible$early_rho
eligible$species <- as.character(eligible$species)

pair_count <- nrow(eligible)
species_counts <- table(eligible$species)
species_count <- length(species_counts)
species_ge3 <- sum(species_counts >= 3)

admission_pass <- (
  pair_count >= 100 &&
  species_count >= 20 &&
  species_ge3 >= 15
)

admission <- data.frame(
  source_commit = SOURCE_COMMIT,
  early_window = "2002-2009",
  late_window = "2010-2017",
  min_pairs_per_window = MIN_PAIRS,
  frozen_mappings = nrow(mapping),
  eligible_pairs = pair_count,
  eligible_species = species_count,
  species_with_at_least_3_pairs = species_ge3,
  green_year_min = min(green$year),
  green_year_max = max(green$year),
  admission_pass = admission_pass
)
write.csv(admission, "outputs/payoff_b_v8_admission.csv", row.names = FALSE)
write.csv(pair_all, "outputs/payoff_b_v8_pair_windows_all.csv", row.names = FALSE)

if (!admission_pass) {
  result <- data.frame(
    status = "NOT_ESTIMABLE",
    support_status = "NOT_RUN_ADMISSION_FAILED"
  )
  write.csv(result, "outputs/payoff_b_v8_primary_result.csv", row.names = FALSE)
  cat("PAYOFF-B V8 ADMISSION FAILED\n")
  print(admission)
  quit(status = 0)
}

# Species-level means are frozen robustness units.
species_split <- split(eligible$delta_rho, eligible$species)
species_df <- data.frame(
  species = names(species_split),
  n_pairs = vapply(species_split, length, integer(1)),
  mean_delta_rho = vapply(species_split, mean, numeric(1)),
  median_delta_rho = vapply(species_split, median, numeric(1))
)
species_df <- species_df[order(species_df$species), ]
write.csv(species_df, "outputs/payoff_b_v8_species_change.csv", row.names = FALSE)

if (!requireNamespace("nlme", quietly = TRUE)) {
  stop("nlme is required for the frozen V8 mixed model")
}

fit <- nlme::lme(
  delta_rho ~ 1,
  random = ~1 | species,
  data = eligible,
  method = "REML",
  control = nlme::lmeControl(returnObject = TRUE)
)
mixed_estimate <- as.numeric(nlme::fixef(fit)[1])

# Species-cluster bootstrap of the mixed intercept.
set.seed(SEED)
species_ids <- sort(unique(eligible$species))
boot_mixed <- rep(NA_real_, BOOT_MIXED)
for (b in seq_len(BOOT_MIXED)) {
  sampled <- sample(species_ids, length(species_ids), replace = TRUE)
  pieces <- vector("list", length(sampled))
  for (k in seq_along(sampled)) {
    tmp <- eligible[eligible$species == sampled[k], c("delta_rho", "species")]
    tmp$boot_species <- paste0(sampled[k], "__", k)
    pieces[[k]] <- tmp
  }
  boot_dat <- do.call(rbind, pieces)
  boot_fit <- try(
    nlme::lme(
      delta_rho ~ 1,
      random = ~1 | boot_species,
      data = boot_dat,
      method = "REML",
      control = nlme::lmeControl(returnObject = TRUE)
    ),
    silent = TRUE
  )
  if (!inherits(boot_fit, "try-error")) {
    boot_mixed[b] <- as.numeric(nlme::fixef(boot_fit)[1])
  }
}
boot_mixed <- boot_mixed[is.finite(boot_mixed)]
if (length(boot_mixed) < 0.8 * BOOT_MIXED) {
  stop("Too many failed V8 mixed-model bootstrap fits")
}
mixed_ci <- as.numeric(quantile(boot_mixed, c(0.025, 0.975), na.rm = TRUE))

negative_species <- sum(species_df$mean_delta_rho < 0)
positive_species <- sum(species_df$mean_delta_rho > 0)
zero_species <- sum(species_df$mean_delta_rho == 0)
sign_n <- negative_species + positive_species
sign_p <- if (sign_n > 0) {
  binom.test(negative_species, sign_n, p = 0.5, alternative = "greater")$p.value
} else {
  NA_real_
}

set.seed(SEED + 1L)
boot_species_mean <- replicate(
  BOOT_SPECIES,
  mean(sample(species_df$mean_delta_rho, nrow(species_df), replace = TRUE))
)
species_mean <- mean(species_df$mean_delta_rho)
species_ci <- as.numeric(quantile(boot_species_mean, c(0.025, 0.975)))

support <- (
  mixed_estimate < 0 &&
  mixed_ci[2] < 0 &&
  negative_species > sign_n / 2 &&
  is.finite(sign_p) &&
  sign_p < 0.05
)

sign_reversals <- sum(
  eligible$early_rho > 0 & eligible$late_rho <= 0
)

result <- data.frame(
  status = "ESTIMABLE",
  eligible_pairs = pair_count,
  eligible_species = species_count,
  species_ge3_pairs = species_ge3,
  mixed_mean_delta_rho = mixed_estimate,
  mixed_boot_ci_low = mixed_ci[1],
  mixed_boot_ci_high = mixed_ci[2],
  mixed_boot_successes = length(boot_mixed),
  species_mean_delta_rho = species_mean,
  species_boot_ci_low = species_ci[1],
  species_boot_ci_high = species_ci[2],
  negative_species = negative_species,
  positive_species = positive_species,
  zero_species = zero_species,
  sign_test_n = sign_n,
  sign_test_p_one_sided = sign_p,
  positive_to_nonpositive_pair_reversals = sign_reversals,
  support_status = ifelse(support, "SUPPORTED", "NOT_SUPPORTED")
)
write.csv(result, "outputs/payoff_b_v8_primary_result.csv", row.names = FALSE)
write.csv(eligible, "outputs/payoff_b_v8_eligible_pairs.csv", row.names = FALSE)

cat("PAYOFF-B V8 PRIMARY RESULT\n")
print(admission)
print(result)
