#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

SOURCE_COMMIT <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL <- paste0(
  "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
  SOURCE_COMMIT,
  "/data/final.rds"
)

EARLY_START <- 2002L
EARLY_END <- 2009L
LATE_START <- 2010L
LATE_END <- 2017L
MIN_PAIRS <- 6L
MIN_PAIR_ROWS <- 100L
MIN_SPECIES <- 20L
MIN_SPECIES_3PAIRS <- 15L
BOOT_REPS <- 4000L
BOOT_SEED <- 20261005L

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
cache <- "outputs/amaral_final_frozen.rds"
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

window_rho <- function(green, source_cell, target_cell, start_year, end_year) {
  source <- green[
    green$cell == source_cell &
      green$year >= start_year &
      green$year <= end_year,
    c("year", "gr_mn")
  ]
  target <- green[
    green$cell == target_cell &
      green$year >= start_year &
      green$year <= end_year,
    c("year", "gr_mn")
  ]
  names(source)[2] <- "origin"
  names(target)[2] <- "destination"
  paired <- merge(source, target, by = "year", all = FALSE)
  paired <- paired[
    is.finite(paired$year) &
      is.finite(paired$origin) &
      is.finite(paired$destination),
  ]
  if (nrow(paired) < MIN_PAIRS) {
    return(list(rho = NA_real_, n = nrow(paired), raw_rho = NA_real_))
  }
  if (length(unique(paired$year)) != nrow(paired)) {
    stop("Duplicate years in source-target green-up pairing")
  }
  raw_rho <- if (
    stats::sd(paired$origin) > 0 &&
      stats::sd(paired$destination) > 0
  ) {
    stats::cor(paired$origin, paired$destination)
  } else {
    NA_real_
  }
  ro <- stats::resid(stats::lm(origin ~ year, data = paired))
  rd <- stats::resid(stats::lm(destination ~ year, data = paired))
  rho <- if (stats::sd(ro) > 0 && stats::sd(rd) > 0) {
    stats::cor(ro, rd)
  } else {
    NA_real_
  }
  list(rho = rho, n = nrow(paired), raw_rho = raw_rho)
}

cells <- unique(dat[, c(
  "species", "cell", "cell_lat2", "cell_lng", "mig_cell", "breed_cell"
)])
cells$cell <- as.numeric(as.character(cells$cell))
cells$cell_lat2 <- as.numeric(cells$cell_lat2)
cells$cell_lng <- as.numeric(cells$cell_lng)
cells$is_mig <- truthy(cells$mig_cell)
cells$is_breed <- truthy(cells$breed_cell)

targets <- cells[
  cells$is_breed &
    is.finite(cells$cell_lat2) &
    is.finite(cells$cell_lng),
  c("species", "cell", "cell_lat2", "cell_lng")
]
targets <- targets[order(targets$species, targets$cell), ]

mapping <- vector("list", nrow(targets))
map_n <- 0L
for (i in seq_len(nrow(targets))) {
  target <- targets[i, ]
  candidates <- cells[
    cells$species == target$species &
      cells$is_mig &
      is.finite(cells$cell_lat2) &
      is.finite(cells$cell_lng) &
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
if (map_n == 0L) stop("No source-target mappings")
mapping <- do.call(rbind, mapping[seq_len(map_n)])

green <- unique(dat[, c("year", "cell", "gr_mn")])
green$year <- as.integer(green$year)
green$cell <- as.numeric(as.character(green$cell))
green$gr_mn <- as.numeric(green$gr_mn)
green <- green[
  is.finite(green$year) &
    is.finite(green$cell) &
    is.finite(green$gr_mn),
]

rows <- vector("list", nrow(mapping))
for (i in seq_len(nrow(mapping))) {
  m <- mapping[i, ]
  early <- window_rho(
    green, m$source_cell, m$target_cell, EARLY_START, EARLY_END
  )
  late <- window_rho(
    green, m$source_cell, m$target_cell, LATE_START, LATE_END
  )
  rows[[i]] <- data.frame(
    species = m$species,
    target_cell = m$target_cell,
    source_cell = m$source_cell,
    source_lat = m$source_lat,
    source_lon = m$source_lon,
    target_lat = m$target_lat,
    target_lon = m$target_lon,
    source_target_distance_km = m$source_target_distance_km,
    early_n = early$n,
    late_n = late$n,
    early_rho = early$rho,
    late_rho = late$rho,
    delta_rho = late$rho - early$rho,
    early_raw_rho = early$raw_rho,
    late_raw_rho = late$raw_rho,
    delta_raw_rho = late$raw_rho - early$raw_rho
  )
}
all_rows <- do.call(rbind, rows)

eligible <- all_rows[
  is.finite(all_rows$early_rho) &
    is.finite(all_rows$late_rho) &
    all_rows$early_n >= MIN_PAIRS &
    all_rows$late_n >= MIN_PAIRS,
]

species_counts <- aggregate(
  target_cell ~ species,
  data = eligible,
  FUN = length
)
names(species_counts)[2] <- "eligible_pairs"
species_n3 <- sum(species_counts$eligible_pairs >= 3)

gate <- data.frame(
  eligible_pairs = nrow(eligible),
  eligible_species = length(unique(eligible$species)),
  species_with_at_least_3_pairs = species_n3,
  min_pairs_per_window = MIN_PAIRS,
  pair_gate = nrow(eligible) >= MIN_PAIR_ROWS,
  species_gate = length(unique(eligible$species)) >= MIN_SPECIES,
  species3_gate = species_n3 >= MIN_SPECIES_3PAIRS
)
gate$pass <- gate$pair_gate & gate$species_gate & gate$species3_gate

write.csv(
  all_rows,
  "outputs/payoff_b_v8_all_mapped_pairs.csv",
  row.names = FALSE
)
write.csv(
  eligible,
  "outputs/payoff_b_v8_eligible_pairs.csv",
  row.names = FALSE
)
write.csv(
  gate,
  "outputs/payoff_b_v8_admission_gate.csv",
  row.names = FALSE
)

if (!isTRUE(gate$pass[1])) {
  result <- data.frame(
    status = "NOT_ESTIMABLE",
    source_commit = SOURCE_COMMIT,
    early_window = paste0(EARLY_START, "-", EARLY_END),
    late_window = paste0(LATE_START, "-", LATE_END),
    eligible_pairs = gate$eligible_pairs,
    eligible_species = gate$eligible_species,
    species_with_at_least_3_pairs = gate$species_with_at_least_3_pairs
  )
  write.csv(
    result,
    "outputs/payoff_b_v8_primary_result.csv",
    row.names = FALSE
  )
  cat("PAYOFF-B V8: ADMISSION GATE FAILED\n")
  print(gate)
  quit(status = 0)
}

eligible$species <- factor(eligible$species)

if (!requireNamespace("nlme", quietly = TRUE)) {
  stop("nlme is required")
}

mixed <- nlme::lme(
  delta_rho ~ 1,
  random = ~1 | species,
  data = eligible,
  method = "REML",
  na.action = na.fail,
  control = nlme::lmeControl(returnObject = TRUE)
)
mixed_intercept <- as.numeric(nlme::fixed.effects(mixed)[1])
mixed_se <- sqrt(diag(stats::vcov(mixed)))[1]
mixed_ci_low <- mixed_intercept - 1.96 * mixed_se
mixed_ci_high <- mixed_intercept + 1.96 * mixed_se

pair_mean <- mean(eligible$delta_rho)

species_summary <- aggregate(
  delta_rho ~ species,
  data = eligible,
  FUN = mean
)
species_summary <- species_summary[order(species_summary$species), ]
n_negative <- sum(species_summary$delta_rho < 0)
n_positive <- sum(species_summary$delta_rho > 0)
n_zero <- sum(species_summary$delta_rho == 0)
sign_n <- n_negative + n_positive
sign_p <- if (sign_n > 0) {
  stats::binom.test(
    n_negative,
    sign_n,
    p = 0.5,
    alternative = "greater"
  )$p.value
} else {
  NA_real_
}
species_mean <- mean(species_summary$delta_rho)

set.seed(BOOT_SEED)
sp_names <- unique(as.character(eligible$species))
boot_mean <- rep(NA_real_, BOOT_REPS)
for (b in seq_len(BOOT_REPS)) {
  sampled <- sample(sp_names, length(sp_names), replace = TRUE)
  idx <- unlist(
    lapply(sampled, function(sp) which(as.character(eligible$species) == sp)),
    use.names = FALSE
  )
  boot_mean[b] <- mean(eligible$delta_rho[idx])
}
boot_mean <- boot_mean[is.finite(boot_mean)]
if (length(boot_mean) < BOOT_REPS * 0.95) {
  stop("Too few finite cluster-bootstrap replicates")
}
boot_ci <- as.numeric(stats::quantile(
  boot_mean,
  probs = c(0.025, 0.975),
  names = FALSE,
  type = 7
))

direction_consistent <- (
  mixed_intercept < 0 &&
  species_mean < 0 &&
  n_negative > n_positive
)

supported <- (
  pair_mean < 0 &&
  boot_ci[2] < 0 &&
  n_negative > n_positive &&
  is.finite(sign_p) &&
  sign_p < 0.05 &&
  direction_consistent
)

result <- data.frame(
  status = ifelse(supported, "SUPPORTED", "NOT_SUPPORTED"),
  source_commit = SOURCE_COMMIT,
  early_window = paste0(EARLY_START, "-", EARLY_END),
  late_window = paste0(LATE_START, "-", LATE_END),
  eligible_pairs = nrow(eligible),
  eligible_species = length(sp_names),
  species_with_at_least_3_pairs = species_n3,
  pair_mean_delta_rho = pair_mean,
  species_cluster_boot_ci_low = boot_ci[1],
  species_cluster_boot_ci_high = boot_ci[2],
  mixed_intercept_delta_rho = mixed_intercept,
  mixed_intercept_se = mixed_se,
  mixed_ci_low_95 = mixed_ci_low,
  mixed_ci_high_95 = mixed_ci_high,
  species_equal_weight_mean_delta_rho = species_mean,
  species_negative = n_negative,
  species_positive = n_positive,
  species_zero = n_zero,
  species_sign_test_p_one_sided = sign_p,
  direction_consistent = direction_consistent,
  bootstrap_reps = length(boot_mean),
  bootstrap_seed = BOOT_SEED
)

write.csv(
  species_summary,
  "outputs/payoff_b_v8_species_summary.csv",
  row.names = FALSE
)
write.csv(
  result,
  "outputs/payoff_b_v8_primary_result.csv",
  row.names = FALSE
)

cat("PAYOFF-B V8 PRIMARY RESULT\n")
print(gate)
print(result)
