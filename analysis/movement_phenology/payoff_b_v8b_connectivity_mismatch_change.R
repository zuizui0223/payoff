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
MIN_ENV_PAIRS <- 6L
MIN_BIRD_YEARS <- 4L
MIN_PAIR_ROWS <- 100L
MIN_SPECIES <- 20L
MIN_SPECIES_3PAIRS <- 15L
BOOT_REPS <- 1000L
BOOT_SEED <- 20261005L

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
cache <- "outputs/amaral_final_frozen.rds"
if (!file.exists(cache)) {
  download.file(SOURCE_URL, cache, mode = "wb", quiet = FALSE)
}
dat <- readRDS(cache)

required <- c(
  "species", "year", "cell", "cell_lat2", "cell_lng",
  "arr_GAM_mean", "gr_mn", "mig_cell", "breed_cell"
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
  if (nrow(paired) < MIN_ENV_PAIRS) {
    return(list(rho = NA_real_, n = nrow(paired)))
  }
  if (length(unique(paired$year)) != nrow(paired)) {
    stop("Duplicate environmental year within source-target pair")
  }
  ro <- resid(lm(origin ~ year, data = paired))
  rd <- resid(lm(destination ~ year, data = paired))
  rho <- if (sd(ro) > 0 && sd(rd) > 0) cor(ro, rd) else NA_real_
  list(rho = rho, n = nrow(paired))
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

bird <- unique(dat[, c(
  "species", "year", "cell", "arr_GAM_mean", "gr_mn", "breed_cell"
)])
bird$year <- as.integer(bird$year)
bird$cell <- as.numeric(as.character(bird$cell))
bird$arr_GAM_mean <- as.numeric(bird$arr_GAM_mean)
bird$gr_mn <- as.numeric(bird$gr_mn)
bird <- bird[
  truthy(bird$breed_cell) &
    is.finite(bird$year) &
    is.finite(bird$cell) &
    is.finite(bird$arr_GAM_mean) &
    is.finite(bird$gr_mn),
]
bird$mismatch_log <- log1p(abs(bird$gr_mn - bird$arr_GAM_mean))

rows <- vector("list", nrow(mapping))
for (i in seq_len(nrow(mapping))) {
  m <- mapping[i, ]
  er <- window_rho(
    green, m$source_cell, m$target_cell, EARLY_START, EARLY_END
  )
  lr <- window_rho(
    green, m$source_cell, m$target_cell, LATE_START, LATE_END
  )

  br <- bird[
    bird$species == m$species &
      bird$cell == m$target_cell,
  ]
  early_bird <- br[
    br$year >= EARLY_START & br$year <= EARLY_END,
  ]
  late_bird <- br[
    br$year >= LATE_START & br$year <= LATE_END,
  ]

  early_m <- if (nrow(early_bird) >= MIN_BIRD_YEARS) {
    mean(early_bird$mismatch_log)
  } else NA_real_
  late_m <- if (nrow(late_bird) >= MIN_BIRD_YEARS) {
    mean(late_bird$mismatch_log)
  } else NA_real_

  rows[[i]] <- data.frame(
    species = m$species,
    target_cell = m$target_cell,
    source_cell = m$source_cell,
    source_target_distance_km = m$source_target_distance_km,
    early_env_n = er$n,
    late_env_n = lr$n,
    early_rho = er$rho,
    late_rho = lr$rho,
    delta_rho = lr$rho - er$rho,
    early_bird_n = nrow(early_bird),
    late_bird_n = nrow(late_bird),
    early_mismatch = early_m,
    late_mismatch = late_m,
    delta_mismatch = late_m - early_m
  )
}
all_rows <- do.call(rbind, rows)

eligible <- all_rows[
  is.finite(all_rows$early_rho) &
    is.finite(all_rows$late_rho) &
    all_rows$early_env_n >= MIN_ENV_PAIRS &
    all_rows$late_env_n >= MIN_ENV_PAIRS &
    is.finite(all_rows$early_mismatch) &
    is.finite(all_rows$late_mismatch) &
    all_rows$early_bird_n >= MIN_BIRD_YEARS &
    all_rows$late_bird_n >= MIN_BIRD_YEARS,
]

species_counts <- aggregate(target_cell ~ species, eligible, length)
names(species_counts)[2] <- "eligible_pairs"
species_n3 <- sum(species_counts$eligible_pairs >= 3)

gate <- data.frame(
  eligible_pairs = nrow(eligible),
  eligible_species = length(unique(eligible$species)),
  species_with_at_least_3_pairs = species_n3,
  min_bird_years_per_window = MIN_BIRD_YEARS,
  sd_delta_rho = sd(eligible$delta_rho),
  sd_delta_mismatch = sd(eligible$delta_mismatch),
  pair_gate = nrow(eligible) >= MIN_PAIR_ROWS,
  species_gate = length(unique(eligible$species)) >= MIN_SPECIES,
  species3_gate = species_n3 >= MIN_SPECIES_3PAIRS,
  predictor_variance_gate = is.finite(sd(eligible$delta_rho)) &&
    sd(eligible$delta_rho) > 0,
  response_variance_gate = is.finite(sd(eligible$delta_mismatch)) &&
    sd(eligible$delta_mismatch) > 0
)
gate$pass <- with(
  gate,
  pair_gate & species_gate & species3_gate &
    predictor_variance_gate & response_variance_gate
)

write.csv(all_rows, "outputs/payoff_b_v8b_all_pairs.csv", row.names = FALSE)
write.csv(eligible, "outputs/payoff_b_v8b_eligible_pairs.csv", row.names = FALSE)
write.csv(gate, "outputs/payoff_b_v8b_admission_gate.csv", row.names = FALSE)

if (!isTRUE(gate$pass[1])) {
  result <- data.frame(
    status = "NOT_ESTIMABLE",
    eligible_pairs = gate$eligible_pairs,
    eligible_species = gate$eligible_species,
    species_with_at_least_3_pairs = gate$species_with_at_least_3_pairs
  )
  write.csv(result, "outputs/payoff_b_v8b_primary_result.csv", row.names = FALSE)
  cat("PAYOFF-B V8b: ADMISSION GATE FAILED\n")
  print(gate)
  quit(status = 0)
}

eligible$species <- factor(eligible$species)
eligible$z_delta_rho <- as.numeric(scale(eligible$delta_rho))

if (!requireNamespace("nlme", quietly = TRUE)) stop("nlme is required")

fit <- nlme::lme(
  delta_mismatch ~ z_delta_rho,
  random = ~1 | species,
  data = eligible,
  method = "REML",
  na.action = na.fail,
  control = nlme::lmeControl(returnObject = TRUE)
)
tab <- summary(fit)$tTable
estimate <- unname(tab["z_delta_rho", "Value"])
se <- unname(tab["z_delta_rho", "Std.Error"])
p_two <- unname(tab["z_delta_rho", "p-value"])
ci_low <- estimate - 1.96 * se
ci_high <- estimate + 1.96 * se

species_summary <- aggregate(
  cbind(delta_rho, delta_mismatch) ~ species,
  data = eligible,
  FUN = mean
)
species_fit <- lm(delta_mismatch ~ delta_rho, data = species_summary)
species_slope <- unname(coef(species_fit)["delta_rho"])

set.seed(BOOT_SEED)
species_names <- unique(as.character(eligible$species))
boot_slopes <- rep(NA_real_, BOOT_REPS)
for (b in seq_len(BOOT_REPS)) {
  sampled <- sample(species_names, length(species_names), replace = TRUE)
  pieces <- vector("list", length(sampled))
  for (k in seq_along(sampled)) {
    sp <- sampled[k]
    tmp <- eligible[as.character(eligible$species) == sp, ]
    tmp$boot_species <- paste0(sp, "__", k)
    pieces[[k]] <- tmp
  }
  bd <- do.call(rbind, pieces)
  bd$boot_species <- factor(bd$boot_species)
  bd$z_delta_rho_boot <- as.numeric(scale(bd$delta_rho))
  bf <- try(
    nlme::lme(
      delta_mismatch ~ z_delta_rho_boot,
      random = ~1 | boot_species,
      data = bd,
      method = "REML",
      na.action = na.fail,
      control = nlme::lmeControl(returnObject = TRUE)
    ),
    silent = TRUE
  )
  if (!inherits(bf, "try-error")) {
    boot_slopes[b] <- as.numeric(nlme::fixed.effects(bf)["z_delta_rho_boot"])
  }
}
boot_slopes <- boot_slopes[is.finite(boot_slopes)]
if (length(boot_slopes) < 0.8 * BOOT_REPS) {
  stop("Fewer than 80% finite species-cluster bootstrap fits")
}
boot_ci <- as.numeric(quantile(
  boot_slopes,
  probs = c(0.025, 0.975),
  names = FALSE
))

supported <- (
  estimate < 0 &&
  boot_ci[2] < 0 &&
  is.finite(species_slope) &&
  species_slope < 0
)

result <- data.frame(
  status = ifelse(supported, "SUPPORTED", "NOT_SUPPORTED"),
  source_commit = SOURCE_COMMIT,
  early_window = paste0(EARLY_START, "-", EARLY_END),
  late_window = paste0(LATE_START, "-", LATE_END),
  eligible_pairs = nrow(eligible),
  eligible_species = length(species_names),
  species_with_at_least_3_pairs = species_n3,
  mixed_slope_per_1sd_delta_rho = estimate,
  mixed_se = se,
  mixed_ci_low_95 = ci_low,
  mixed_ci_high_95 = ci_high,
  mixed_p_two_sided = p_two,
  species_cluster_boot_ci_low = boot_ci[1],
  species_cluster_boot_ci_high = boot_ci[2],
  species_level_slope_raw_delta_rho = species_slope,
  mean_delta_rho = mean(eligible$delta_rho),
  mean_delta_mismatch = mean(eligible$delta_mismatch),
  bootstrap_finite_reps = length(boot_slopes),
  bootstrap_seed = BOOT_SEED
)

write.csv(
  species_summary,
  "outputs/payoff_b_v8b_species_summary.csv",
  row.names = FALSE
)
write.csv(
  result,
  "outputs/payoff_b_v8b_primary_result.csv",
  row.names = FALSE
)

cat("PAYOFF-B V8b PRIMARY RESULT\n")
print(gate)
print(result)
