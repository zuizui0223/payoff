#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

PRIMARY_V8_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_primary.R"
CONTRACT <- "docs/PAYOFF_B_V8_ACTUATOR_BRIDGE_CONTRACT_20261005.md"

if (!file.exists(PRIMARY_V8_SCRIPT)) stop("Missing frozen V8 primary script")
if (!file.exists(CONTRACT)) stop("Missing actuator bridge contract")

source(PRIMARY_V8_SCRIPT, local = FALSE)

B <- 10000L
SEED <- 20261005L
MIN_SPEED_YEARS <- 6L

speed <- dat[, c("species", "year", "cell", "vArrMag")]
speed$year <- as.integer(speed$year)
speed$cell <- as.numeric(as.character(speed$cell))
speed$vArrMag <- as.numeric(speed$vArrMag)
speed <- speed[
  is.finite(speed$year) &
    is.finite(speed$cell) &
    is.finite(speed$vArrMag) &
    speed$vArrMag > 0,
  ,
  drop = FALSE
]
speed <- unique(speed)
speed$log_speed <- log(speed$vArrMag)

exposure_map <- unique(eligible_map[, c(
  "species", "target_cell", "source_cell", "pair_key"
)])
exposure_map <- merge(
  exposure_map,
  pairs[, c("pair_key", "delta_rho")],
  by = "pair_key",
  all = FALSE,
  sort = FALSE
)

window_speed <- function(species, target_cell, start_year, end_year) {
  z <- speed[
    speed$species == species &
      speed$cell == target_cell &
      speed$year >= start_year &
      speed$year <= end_year,
    c("year", "log_speed"),
    drop = FALSE
  ]
  z <- z[!duplicated(z$year), , drop = FALSE]
  c(
    n = nrow(z),
    mean_log_speed = if (nrow(z) > 0) mean(z$log_speed) else NA_real_
  )
}

early <- t(mapply(
  window_speed,
  exposure_map$species,
  exposure_map$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
))
late <- t(mapply(
  window_speed,
  exposure_map$species,
  exposure_map$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
))

exposure_map$speed_early_n <- as.integer(early[, "n"])
exposure_map$speed_late_n <- as.integer(late[, "n"])
exposure_map$mean_log_speed_early <- as.numeric(early[, "mean_log_speed"])
exposure_map$mean_log_speed_late <- as.numeric(late[, "mean_log_speed"])

analysis <- exposure_map[
  exposure_map$speed_early_n >= MIN_SPEED_YEARS &
    exposure_map$speed_late_n >= MIN_SPEED_YEARS &
    is.finite(exposure_map$mean_log_speed_early) &
    is.finite(exposure_map$mean_log_speed_late) &
    is.finite(exposure_map$delta_rho),
  ,
  drop = FALSE
]

admission_rows <- nrow(analysis)
admission_pairs <- length(unique(analysis$pair_key))
admission_species <- length(unique(analysis$species))

if (
  admission_rows < 20 ||
  admission_pairs < 20 ||
  admission_species < 5
) {
  dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
  status_row <- data.frame(
    eligible_species_target_rows = admission_rows,
    eligible_unique_spatial_pairs = admission_pairs,
    eligible_species = admission_species,
    min_speed_years_per_window = MIN_SPEED_YEARS,
    actuator_bridge_status = "NOT_ESTIMABLE"
  )
  write.csv(
    status_row,
    "outputs/payoff_b_v8_actuator_bridge_summary.csv",
    row.names = FALSE
  )
  cat("\nPAYOFF-B V8 ACTUATOR BRIDGE\n")
  print(status_row)
  cat("\nFrozen admission thresholds were not relaxed; speed-change coefficients were not computed.\n")
  quit(save = "no", status = 0)
}

analysis$delta_log_speed <- (
  analysis$mean_log_speed_late - analysis$mean_log_speed_early
)

pair_exp <- unique(analysis[, c("pair_key", "delta_rho")])
rho_mu <- mean(pair_exp$delta_rho)
rho_sd <- sd(pair_exp$delta_rho)
if (!is.finite(rho_sd) || rho_sd <= 0) stop("Invalid delta-rho SD")
analysis$z_delta_rho <- (analysis$delta_rho - rho_mu) / rho_sd

fit_weighted <- function(df, formula_type = "primary") {
  if (nrow(df) < 3) return(NA_real_)
  nn <- table(df$species)
  w <- 1 / as.numeric(nn[df$species])

  if (formula_type == "primary") {
    X <- cbind("(Intercept)" = 1, z_delta_rho = df$z_delta_rho)
  } else if (formula_type == "baseline") {
    X <- cbind(
      "(Intercept)" = 1,
      z_delta_rho = df$z_delta_rho,
      z_baseline_speed = df$z_baseline_speed
    )
  } else {
    stop("Unknown formula_type")
  }

  fit <- try(lm.wfit(X, df$delta_log_speed, w = w), silent = TRUE)
  if (inherits(fit, "try-error")) return(NA_real_)
  unname(fit$coefficients["z_delta_rho"])
}

fit_unweighted <- function(df) {
  fit <- try(lm(delta_log_speed ~ z_delta_rho, data = df), silent = TRUE)
  if (inherits(fit, "try-error")) return(NA_real_)
  unname(coef(fit)["z_delta_rho"])
}

fit_species_collapse <- function(df) {
  sp <- aggregate(
    cbind(delta_log_speed, z_delta_rho) ~ species,
    data = df,
    FUN = mean
  )
  if (nrow(sp) < 3 || sd(sp$z_delta_rho) <= 0) return(NA_real_)
  unname(coef(lm(delta_log_speed ~ z_delta_rho, data = sp))["z_delta_rho"])
}

beta <- fit_weighted(analysis, "primary")

keys <- unique(analysis$pair_key)
P <- length(keys)
by_pair <- split(analysis, analysis$pair_key)

bootstrap_coef <- function(fitter, B = B, seed = SEED) {
  set.seed(seed)
  out <- rep(NA_real_, B)
  for (b in seq_len(B)) {
    sampled <- sample(keys, size = P, replace = TRUE)
    chunks <- vector("list", length(sampled))
    for (k in seq_along(sampled)) {
      z <- by_pair[[sampled[k]]]
      z$bootstrap_draw <- k
      chunks[[k]] <- z
    }
    bd <- do.call(rbind, chunks)
    out[b] <- fitter(bd)
  }
  out
}

boot_primary <- bootstrap_coef(function(df) fit_weighted(df, "primary"))
ci <- function(x) as.numeric(quantile(x[is.finite(x)], c(0.025, 0.975), names = FALSE))
ci_primary <- ci(boot_primary)

# Diagnostics.
beta_unweighted <- fit_unweighted(analysis)
boot_unweighted <- bootstrap_coef(fit_unweighted)
ci_unweighted <- ci(boot_unweighted)

beta_species <- fit_species_collapse(analysis)
boot_species <- bootstrap_coef(fit_species_collapse)
ci_species <- ci(boot_species)

baseline_mu <- mean(analysis$mean_log_speed_early)
baseline_sd <- sd(analysis$mean_log_speed_early)
analysis$z_baseline_speed <- (
  analysis$mean_log_speed_early - baseline_mu
) / baseline_sd
by_pair <- split(analysis, analysis$pair_key)
beta_baseline <- fit_weighted(analysis, "baseline")
boot_baseline <- bootstrap_coef(function(df) fit_weighted(df, "baseline"))
ci_baseline <- ci(boot_baseline)

loo_species <- sort(unique(analysis$species))
loo <- data.frame(
  omitted_species = loo_species,
  beta = NA_real_
)
for (i in seq_along(loo_species)) {
  d <- analysis[analysis$species != loo_species[i], , drop = FALSE]
  loo$beta[i] <- fit_weighted(d, "primary")
}

complete <- analysis[
  analysis$speed_early_n == 8L &
    analysis$speed_late_n == 8L,
  ,
  drop = FALSE
]
beta_complete <- NA_real_
ci_complete <- c(NA_real_, NA_real_)
complete_pairs <- length(unique(complete$pair_key))
complete_species <- length(unique(complete$species))

if (
  nrow(complete) >= 3 &&
  complete_pairs >= 3 &&
  complete_species >= 2
) {
  cp <- unique(complete[, c("pair_key", "delta_rho")])
  cmu <- mean(cp$delta_rho)
  csd <- sd(cp$delta_rho)
  if (is.finite(csd) && csd > 0) {
    complete$z_delta_rho <- (complete$delta_rho - cmu) / csd
    beta_complete <- fit_weighted(complete, "primary")

    complete_keys <- unique(complete$pair_key)
    complete_P <- length(complete_keys)
    complete_by_pair <- split(complete, complete$pair_key)
    set.seed(SEED)
    boot_complete <- rep(NA_real_, B)
    for (b in seq_len(B)) {
      sampled <- sample(complete_keys, size = complete_P, replace = TRUE)
      chunks <- vector("list", length(sampled))
      for (k in seq_along(sampled)) {
        z <- complete_by_pair[[sampled[k]]]
        z$bootstrap_draw <- k
        chunks[[k]] <- z
      }
      bd <- do.call(rbind, chunks)
      boot_complete[b] <- fit_weighted(bd, "primary")
    }
    ci_complete <- ci(boot_complete)
  }
}

summary_row <- data.frame(
  eligible_species_target_rows = nrow(analysis),
  eligible_unique_spatial_pairs = length(unique(analysis$pair_key)),
  eligible_species = length(unique(analysis$species)),
  mean_delta_log_speed_unweighted = mean(analysis$delta_log_speed),
  beta_primary = beta,
  primary_ci_low_95 = ci_primary[1],
  primary_ci_high_95 = ci_primary[2],
  primary_interval_excludes_zero = ifelse(
    ci_primary[1] > 0 || ci_primary[2] < 0,
    "YES", "NO"
  ),
  beta_unweighted = beta_unweighted,
  unweighted_ci_low_95 = ci_unweighted[1],
  unweighted_ci_high_95 = ci_unweighted[2],
  beta_equal_species_collapse = beta_species,
  species_ci_low_95 = ci_species[1],
  species_ci_high_95 = ci_species[2],
  beta_adjust_baseline_speed = beta_baseline,
  baseline_ci_low_95 = ci_baseline[1],
  baseline_ci_high_95 = ci_baseline[2],
  loo_min_beta = min(loo$beta, na.rm = TRUE),
  loo_max_beta = max(loo$beta, na.rm = TRUE),
  loo_negative_n = sum(loo$beta < 0, na.rm = TRUE),
  loo_positive_n = sum(loo$beta > 0, na.rm = TRUE),
  complete_rows = nrow(complete),
  complete_unique_pairs = complete_pairs,
  complete_species = complete_species,
  beta_complete = beta_complete,
  complete_ci_low_95 = ci_complete[1],
  complete_ci_high_95 = ci_complete[2],
  bootstrap_replicates = B,
  bootstrap_seed = SEED
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(summary_row, "outputs/payoff_b_v8_actuator_bridge_summary.csv", row.names = FALSE)
write.csv(analysis, "outputs/payoff_b_v8_actuator_bridge_rows.csv", row.names = FALSE)
write.csv(loo, "outputs/payoff_b_v8_actuator_bridge_loo.csv", row.names = FALSE)
write.csv(
  data.frame(replicate = seq_len(B), beta = boot_primary),
  "outputs/payoff_b_v8_actuator_bridge_bootstrap.csv",
  row.names = FALSE
)

cat("\nPAYOFF-B V8 ACTUATOR BRIDGE\n")
print(summary_row)
