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
BOOT_REPS_PAIR <- 2000L
BOOT_REPS_SPECIES <- 10000L
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

window_rho <- function(year, origin, destination, years) {
  keep <- is.finite(year) & is.finite(origin) & is.finite(destination) &
    year %in% years
  year <- year[keep]
  origin <- origin[keep]
  destination <- destination[keep]
  if (length(year) < MIN_PAIRS) return(c(rho = NA_real_, n = length(year)))
  if (length(unique(year)) != length(year)) {
    stop("Duplicate years within one source-target window")
  }
  ro <- resid(lm(origin ~ year))
  rd <- resid(lm(destination ~ year))
  if (sd(ro) <= 0 || sd(rd) <= 0) return(c(rho = NA_real_, n = length(year)))
  c(rho = cor(ro, rd), n = length(year))
}

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

rows <- vector("list", nrow(mapping))
row_n <- 0L
for (i in seq_len(nrow(mapping))) {
  mp <- mapping[i, ]
  source <- green[green$cell == mp$source_cell, c("year", "gr_mn")]
  target <- green[green$cell == mp$target_cell, c("year", "gr_mn")]
  names(source)[2] <- "source_greenup"
  names(target)[2] <- "target_greenup"
  paired <- merge(source, target, by = "year", all = FALSE)

  early <- window_rho(
    paired$year, paired$source_greenup, paired$target_greenup, EARLY_YEARS
  )
  late <- window_rho(
    paired$year, paired$source_greenup, paired$target_greenup, LATE_YEARS
  )

  row_n <- row_n + 1L
  rows[[row_n]] <- data.frame(
    species = mp$species,
    target_cell = mp$target_cell,
    source_cell = mp$source_cell,
    source_target_distance_km = mp$source_target_distance_km,
    early_rho = unname(early["rho"]),
    early_n = as.integer(early["n"]),
    late_rho = unname(late["rho"]),
    late_n = as.integer(late["n"])
  )
}
rows <- do.call(rbind, rows[seq_len(row_n)])
rows$delta_rho <- rows$late_rho - rows$early_rho

eligible <- rows[
  is.finite(rows$early_rho) &
    is.finite(rows$late_rho) &
    rows$early_n >= MIN_PAIRS &
    rows$late_n >= MIN_PAIRS,
]

species_tab <- aggregate(
  delta_rho ~ species,
  data = eligible,
  FUN = function(x) c(
    mean = mean(x),
    n_pairs = length(x)
  )
)
species_summary <- data.frame(
  species = species_tab$species,
  mean_delta_rho = species_tab$delta_rho[, "mean"],
  n_pairs = as.integer(species_tab$delta_rho[, "n_pairs"])
)

n_pairs <- nrow(eligible)
n_species <- nrow(species_summary)
n_species_ge3 <- sum(species_summary$n_pairs >= 3)

gate_pass <- (
  n_pairs >= 100 &&
  n_species >= 20 &&
  n_species_ge3 >= 15
)

write.csv(
  eligible,
  "outputs/payoff_b_v8_connectivity_degradation_pairs.csv",
  row.names = FALSE
)
write.csv(
  species_summary,
  "outputs/payoff_b_v8_connectivity_degradation_species.csv",
  row.names = FALSE
)

gate_row <- data.frame(
  source_commit = SOURCE_COMMIT,
  early_window = paste(range(EARLY_YEARS), collapse = "-"),
  late_window = paste(range(LATE_YEARS), collapse = "-"),
  min_pairs_per_window = MIN_PAIRS,
  eligible_pairs = n_pairs,
  eligible_species = n_species,
  species_with_at_least_3_pairs = n_species_ge3,
  admission_gate = ifelse(gate_pass, "PASS", "FAIL")
)

if (!gate_pass) {
  write.csv(
    gate_row,
    "outputs/payoff_b_v8_connectivity_degradation_result.csv",
    row.names = FALSE
  )
  cat("PAYOFF-B V8 ADMISSION GATE\n")
  print(gate_row)
  quit(status = 0)
}

if (!requireNamespace("nlme", quietly = TRUE)) {
  stop("nlme is required for the frozen pair-level mixed-intercept model")
}

eligible$species <- factor(eligible$species)
fit <- nlme::lme(
  delta_rho ~ 1,
  random = ~ 1 | species,
  data = eligible,
  method = "REML",
  na.action = na.omit,
  control = nlme::lmeControl(returnObject = TRUE)
)
pair_mixed_estimate <- unname(nlme::fixef(fit)[1])
pair_mixed_ci <- nlme::intervals(fit, which = "fixed")$fixed[1, c("lower", "upper")]

set.seed(BOOT_SEED)
species_levels <- levels(eligible$species)

boot_pair <- rep(NA_real_, BOOT_REPS_PAIR)
for (b in seq_len(BOOT_REPS_PAIR)) {
  sampled <- sample(species_levels, length(species_levels), replace = TRUE)
  pieces <- vector("list", length(sampled))
  for (k in seq_along(sampled)) {
    z <- eligible[eligible$species == sampled[k], , drop = FALSE]
    z$boot_species <- paste0(sampled[k], "__", k)
    pieces[[k]] <- z
  }
  bd <- do.call(rbind, pieces)
  bf <- try(
    nlme::lme(
      delta_rho ~ 1,
      random = ~ 1 | boot_species,
      data = bd,
      method = "REML",
      na.action = na.omit,
      control = nlme::lmeControl(returnObject = TRUE)
    ),
    silent = TRUE
  )
  if (!inherits(bf, "try-error")) {
    boot_pair[b] <- unname(nlme::fixef(bf)[1])
  }
}
boot_pair <- boot_pair[is.finite(boot_pair)]
if (length(boot_pair) < 0.9 * BOOT_REPS_PAIR) {
  stop("Too many failed species-cluster bootstrap mixed-model fits")
}
pair_boot_ci <- as.numeric(quantile(
  boot_pair,
  probs = c(0.025, 0.975),
  names = FALSE,
  type = 7
))

species_mean <- mean(species_summary$mean_delta_rho)
negative_species <- sum(species_summary$mean_delta_rho < 0)
positive_species <- sum(species_summary$mean_delta_rho > 0)
zero_species <- sum(species_summary$mean_delta_rho == 0)
sign_n <- negative_species + positive_species
sign_p <- if (sign_n > 0) {
  binom.test(
    negative_species,
    sign_n,
    p = 0.5,
    alternative = "greater"
  )$p.value
} else {
  NA_real_
}

set.seed(BOOT_SEED + 1L)
boot_species <- replicate(
  BOOT_REPS_SPECIES,
  mean(sample(
    species_summary$mean_delta_rho,
    n_species,
    replace = TRUE
  ))
)
species_boot_ci <- as.numeric(quantile(
  boot_species,
  probs = c(0.025, 0.975),
  names = FALSE,
  type = 7
))

supported <- (
  pair_mixed_estimate < 0 &&
  pair_boot_ci[2] < 0 &&
  negative_species > sign_n / 2 &&
  is.finite(sign_p) &&
  sign_p < 0.05
)

result <- data.frame(
  source_commit = SOURCE_COMMIT,
  early_window = paste(range(EARLY_YEARS), collapse = "-"),
  late_window = paste(range(LATE_YEARS), collapse = "-"),
  min_pairs_per_window = MIN_PAIRS,
  eligible_pairs = n_pairs,
  eligible_species = n_species,
  species_with_at_least_3_pairs = n_species_ge3,
  pair_mixed_estimate = pair_mixed_estimate,
  pair_mixed_ci_low = unname(pair_mixed_ci["lower"]),
  pair_mixed_ci_high = unname(pair_mixed_ci["upper"]),
  pair_species_cluster_boot_ci_low = pair_boot_ci[1],
  pair_species_cluster_boot_ci_high = pair_boot_ci[2],
  pair_bootstrap_successful_reps = length(boot_pair),
  species_mean_delta_rho = species_mean,
  species_boot_ci_low = species_boot_ci[1],
  species_boot_ci_high = species_boot_ci[2],
  negative_species = negative_species,
  positive_species = positive_species,
  zero_species = zero_species,
  sign_test_n = sign_n,
  sign_test_one_sided_p = sign_p,
  support_status = ifelse(
    supported,
    "SUPPORTED_BROAD_DEGRADATION",
    "NOT_SUPPORTED_BROAD_DEGRADATION"
  )
)

write.csv(
  result,
  "outputs/payoff_b_v8_connectivity_degradation_result.csv",
  row.names = FALSE
)

cat("PAYOFF-B V8 PREDICTIVE CONNECTIVITY DEGRADATION\n")
print(result)
