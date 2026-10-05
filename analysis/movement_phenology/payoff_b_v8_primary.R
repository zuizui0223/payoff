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
MIN_PAIRS_PER_WINDOW <- 6L

MIN_UNIQUE_PAIRS <- 100L
MIN_SPECIES <- 20L
MIN_SPECIES_WITH_3_PAIRS <- 15L

BOOT_B <- 10000L
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

detrended_rho <- function(source_cell, target_cell, start_year, end_year, green) {
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
  names(source)[2] <- "source_greenup"
  names(target)[2] <- "target_greenup"

  paired <- merge(source, target, by = "year", all = FALSE)
  paired <- paired[
    is.finite(paired$year) &
      is.finite(paired$source_greenup) &
      is.finite(paired$target_greenup),
  ]
  paired <- paired[!duplicated(paired$year), ]

  n <- nrow(paired)
  if (n < MIN_PAIRS_PER_WINDOW) {
    return(c(n = n, rho = NA_real_))
  }

  src_resid <- resid(lm(source_greenup ~ year, data = paired))
  tgt_resid <- resid(lm(target_greenup ~ year, data = paired))

  if (!is.finite(sd(src_resid)) || !is.finite(sd(tgt_resid)) ||
      sd(src_resid) <= 0 || sd(tgt_resid) <= 0) {
    return(c(n = n, rho = NA_real_))
  }

  c(n = n, rho = cor(src_resid, tgt_resid, method = "pearson"))
}

# Rebuild the frozen source-target mapping exactly as in the prior
# predictive-connectivity analysis.
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
    species = target$species,
    target_cell = target$cell,
    source_cell = source$cell,
    source_target_distance_km = source$distance_km
  )
}

mapping <- do.call(rbind, mapping[seq_len(map_n)])
if (is.null(mapping) || nrow(mapping) == 0) stop("No source-target mappings")

green <- unique(dat[, c("year", "cell", "gr_mn")])
green$year <- as.integer(green$year)
green$cell <- as.numeric(as.character(green$cell))
green$gr_mn <- as.numeric(green$gr_mn)
green <- green[
  is.finite(green$year) &
    is.finite(green$cell) &
    is.finite(green$gr_mn),
]

# Outcome-blind eligibility based only on paired-year counts.
window_count <- function(source_cell, target_cell, start_year, end_year) {
  source_years <- unique(green$year[
    green$cell == source_cell &
      green$year >= start_year &
      green$year <= end_year
  ])
  target_years <- unique(green$year[
    green$cell == target_cell &
      green$year >= start_year &
      green$year <= end_year
  ])
  length(intersect(source_years, target_years))
}

mapping$early_n_gate <- mapply(
  window_count,
  mapping$source_cell,
  mapping$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
)
mapping$late_n_gate <- mapply(
  window_count,
  mapping$source_cell,
  mapping$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
)
mapping$gate_eligible <- (
  mapping$early_n_gate >= MIN_PAIRS_PER_WINDOW &
  mapping$late_n_gate >= MIN_PAIRS_PER_WINDOW
)
eligible_map <- mapping[mapping$gate_eligible, ]
eligible_map$pair_key <- paste(
  eligible_map$source_cell,
  eligible_map$target_cell,
  sep = "->"
)

# Calculate each environmental pair exactly once.
pair_seed <- unique(eligible_map[, c(
  "pair_key", "source_cell", "target_cell", "source_target_distance_km"
)])
pair_seed <- pair_seed[order(pair_seed$source_cell, pair_seed$target_cell), ]

early_stats <- t(mapply(
  detrended_rho,
  pair_seed$source_cell,
  pair_seed$target_cell,
  MoreArgs = list(
    start_year = EARLY_START,
    end_year = EARLY_END,
    green = green
  )
))
late_stats <- t(mapply(
  detrended_rho,
  pair_seed$source_cell,
  pair_seed$target_cell,
  MoreArgs = list(
    start_year = LATE_START,
    end_year = LATE_END,
    green = green
  )
))

pair_seed$early_n <- as.integer(early_stats[, "n"])
pair_seed$late_n <- as.integer(late_stats[, "n"])
pair_seed$rho_early <- as.numeric(early_stats[, "rho"])
pair_seed$rho_late <- as.numeric(late_stats[, "rho"])
pair_seed$delta_rho <- pair_seed$rho_late - pair_seed$rho_early
pair_seed$primary_finite <- (
  is.finite(pair_seed$rho_early) &
  is.finite(pair_seed$rho_late) &
  is.finite(pair_seed$delta_rho)
)

pairs <- pair_seed[pair_seed$primary_finite, ]

# Species incidence is frozen by the original mapping but environmental outcomes
# are stored once per unique spatial pair.
incidence <- unique(eligible_map[, c("species", "pair_key")])
incidence <- incidence[incidence$pair_key %in% pairs$pair_key, ]

species_counts <- aggregate(
  pair_key ~ species,
  data = incidence,
  FUN = function(x) length(unique(x))
)
names(species_counts)[2] <- "eligible_unique_pairs"

finite_pair_count <- nrow(pairs)
finite_species_count <- length(unique(incidence$species))
finite_species_with_3 <- sum(species_counts$eligible_unique_pairs >= 3)

if (
  finite_pair_count < MIN_UNIQUE_PAIRS ||
  finite_species_count < MIN_SPECIES ||
  finite_species_with_3 < MIN_SPECIES_WITH_3_PAIRS
) {
  status <- data.frame(
    source_commit = SOURCE_COMMIT,
    finite_unique_pairs = finite_pair_count,
    finite_species = finite_species_count,
    species_with_at_least_3_pairs = finite_species_with_3,
    primary_status = "NOT_ESTIMABLE_AFTER_FINITE_RHO_CHECK"
  )
  write.csv(
    status,
    "outputs/payoff_b_v8_primary_status.csv",
    row.names = FALSE
  )
  stop("V8 finite-rho gate failed; primary support result not computed")
}

pair_delta <- setNames(pairs$delta_rho, pairs$pair_key)

species_delta <- merge(
  incidence,
  pairs[, c("pair_key", "delta_rho")],
  by = "pair_key",
  all.x = TRUE,
  all.y = FALSE
)
species_means <- aggregate(
  delta_rho ~ species,
  data = species_delta,
  FUN = mean
)

pair_mean <- mean(pairs$delta_rho)
equal_species_mean <- mean(species_means$delta_rho)
negative_species <- sum(species_means$delta_rho < 0)
positive_species <- sum(species_means$delta_rho > 0)
zero_species <- sum(species_means$delta_rho == 0)

# Dependency-aware bootstrap: resample unique spatial pairs, preserving the
# full species-incidence set of each sampled pair.
set.seed(BOOT_SEED)
pair_boot <- numeric(BOOT_B)
species_boot <- numeric(BOOT_B)

incidence_by_pair <- split(incidence$species, incidence$pair_key)
pair_keys <- pairs$pair_key
P <- length(pair_keys)

for (b in seq_len(BOOT_B)) {
  sampled_keys <- sample(pair_keys, size = P, replace = TRUE)
  sampled_delta <- pair_delta[sampled_keys]
  pair_boot[b] <- mean(sampled_delta)

  species_value_lists <- list()
  for (k in seq_along(sampled_keys)) {
    pk <- sampled_keys[k]
    spp <- incidence_by_pair[[pk]]
    val <- pair_delta[[pk]]
    for (sp in spp) {
      species_value_lists[[sp]] <- c(species_value_lists[[sp]], val)
    }
  }

  sp_means <- vapply(species_value_lists, mean, numeric(1))
  species_boot[b] <- mean(sp_means)
}

pair_ci <- as.numeric(quantile(pair_boot, c(0.025, 0.975), names = FALSE))
species_ci <- as.numeric(quantile(species_boot, c(0.025, 0.975), names = FALSE))

supported <- (
  pair_mean < 0 &&
  pair_ci[2] < 0 &&
  equal_species_mean < 0 &&
  species_ci[2] < 0
)

summary_row <- data.frame(
  source_commit = SOURCE_COMMIT,
  early_window = paste0(EARLY_START, "-", EARLY_END),
  late_window = paste0(LATE_START, "-", LATE_END),
  finite_unique_spatial_pairs = finite_pair_count,
  finite_species = finite_species_count,
  species_with_at_least_3_pairs = finite_species_with_3,
  pair_mean_delta_rho = pair_mean,
  pair_boot_ci_low_95 = pair_ci[1],
  pair_boot_ci_high_95 = pair_ci[2],
  equal_species_mean_delta_rho = equal_species_mean,
  species_boot_ci_low_95 = species_ci[1],
  species_boot_ci_high_95 = species_ci[2],
  negative_species_means = negative_species,
  positive_species_means = positive_species,
  zero_species_means = zero_species,
  bootstrap_replicates = BOOT_B,
  bootstrap_seed = BOOT_SEED,
  primary_support_status = ifelse(supported, "SUPPORTED", "NOT_SUPPORTED")
)

write.csv(
  summary_row,
  "outputs/payoff_b_v8_primary_summary.csv",
  row.names = FALSE
)
write.csv(
  pairs,
  "outputs/payoff_b_v8_primary_unique_pairs.csv",
  row.names = FALSE
)
write.csv(
  species_means,
  "outputs/payoff_b_v8_primary_species_means.csv",
  row.names = FALSE
)
write.csv(
  incidence,
  "outputs/payoff_b_v8_primary_pair_species_incidence.csv",
  row.names = FALSE
)
write.csv(
  data.frame(
    replicate = seq_len(BOOT_B),
    pair_mean = pair_boot,
    equal_species_mean = species_boot
  ),
  "outputs/payoff_b_v8_primary_bootstrap.csv",
  row.names = FALSE
)

cat("PAYOFF-B V8 PRIMARY ENVIRONMENTAL ANALYSIS\n")
print(summary_row)
