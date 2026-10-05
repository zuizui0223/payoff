#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

CONTRACT <- "docs/PAYOFF_B_V8_DOWNSTREAM_TRANSFER_CONTRACT_20261005.md"
PRIMARY_V8_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_primary.R"

if (!file.exists(CONTRACT)) stop("Missing frozen V8 transfer contract")
if (!file.exists(PRIMARY_V8_SCRIPT)) stop("Missing frozen V8 primary script")

# Reconstruct already-opened V8 environmental exposure exactly.
source(PRIMARY_V8_SCRIPT, local = FALSE)

TRANSFER_BOOT_B <- 10000L
TRANSFER_BOOT_SEED <- 20261005L
PRIOR_BETA_REFERENCE <- -0.0461786180645446
MIN_BIRD_YEARS_PER_WINDOW <- 6L

# Bird mismatch is the same scale as the frozen 2026-09-26 broad-bird analysis.
bird <- dat[, c(
  "species", "year", "cell", "arr_GAM_mean", "gr_mn"
)]
bird$year <- as.integer(bird$year)
bird$cell <- as.numeric(as.character(bird$cell))
bird$arr_GAM_mean <- as.numeric(bird$arr_GAM_mean)
bird$gr_mn <- as.numeric(bird$gr_mn)
bird <- bird[
  is.finite(bird$year) &
    is.finite(bird$cell) &
    is.finite(bird$arr_GAM_mean) &
    is.finite(bird$gr_mn),
  ,
  drop = FALSE
]
bird <- unique(bird)
bird$mismatch_y <- log1p(abs(bird$gr_mn - bird$arr_GAM_mean))

# Species-target-cell rows carrying the already-opened environmental exposure.
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

window_stats <- function(species, target_cell, start_year, end_year) {
  z <- bird[
    bird$species == species &
      bird$cell == target_cell &
      bird$year >= start_year &
      bird$year <= end_year,
    c("year", "mismatch_y", "gr_mn"),
    drop = FALSE
  ]
  z <- z[!duplicated(z$year), , drop = FALSE]
  c(
    n = nrow(z),
    mismatch_mean = if (nrow(z) > 0) mean(z$mismatch_y) else NA_real_,
    greenup_mean = if (nrow(z) > 0) mean(z$gr_mn) else NA_real_
  )
}

early <- t(mapply(
  window_stats,
  exposure_map$species,
  exposure_map$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
))
late <- t(mapply(
  window_stats,
  exposure_map$species,
  exposure_map$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
))

exposure_map$bird_early_n <- as.integer(early[, "n"])
exposure_map$bird_late_n <- as.integer(late[, "n"])
exposure_map$mean_mismatch_early <- as.numeric(early[, "mismatch_mean"])
exposure_map$mean_mismatch_late <- as.numeric(late[, "mismatch_mean"])
exposure_map$mean_greenup_early <- as.numeric(early[, "greenup_mean"])
exposure_map$mean_greenup_late <- as.numeric(late[, "greenup_mean"])

analysis <- exposure_map[
  exposure_map$bird_early_n >= MIN_BIRD_YEARS_PER_WINDOW &
    exposure_map$bird_late_n >= MIN_BIRD_YEARS_PER_WINDOW &
    is.finite(exposure_map$mean_mismatch_early) &
    is.finite(exposure_map$mean_mismatch_late) &
    is.finite(exposure_map$delta_rho),
  ,
  drop = FALSE
]

if (nrow(analysis) < 20) stop("Too few eligible species-target rows for transfer analysis")
if (length(unique(analysis$pair_key)) < 20) stop("Too few unique spatial pairs for transfer analysis")
if (length(unique(analysis$species)) < 5) stop("Too few species for transfer analysis")

analysis$delta_mismatch <- analysis$mean_mismatch_late - analysis$mean_mismatch_early
analysis$delta_greenup_mean <- analysis$mean_greenup_late - analysis$mean_greenup_early

# Standardize environmental change across eligible UNIQUE pairs only.
pair_exposure <- unique(analysis[, c("pair_key", "delta_rho")])
pair_mu <- mean(pair_exposure$delta_rho)
pair_sd <- sd(pair_exposure$delta_rho)
if (!is.finite(pair_sd) || pair_sd <= 0) stop("delta_rho has zero/invalid SD")
analysis$z_delta_rho <- (analysis$delta_rho - pair_mu) / pair_sd

# Equal total weight for every species.
species_n <- table(analysis$species)
analysis$species_weight <- 1 / as.numeric(species_n[analysis$species])

fit_transfer <- function(df) {
  if (nrow(df) < 3 || length(unique(df$z_delta_rho)) < 2) return(NA_real_)
  nn <- table(df$species)
  ww <- 1 / as.numeric(nn[df$species])
  fit <- try(
    lm(delta_mismatch ~ z_delta_rho, data = df, weights = ww),
    silent = TRUE
  )
  if (inherits(fit, "try-error")) return(NA_real_)
  unname(coef(fit)["z_delta_rho"])
}

beta_transfer <- fit_transfer(analysis)
if (!is.finite(beta_transfer)) stop("Primary transfer coefficient not estimable")

# Unique-spatial-pair bootstrap. Each sampled pair carries all mapped rows.
set.seed(TRANSFER_BOOT_SEED)
pair_keys <- unique(analysis$pair_key)
P <- length(pair_keys)
rows_by_pair <- split(analysis, analysis$pair_key)
boot_beta <- rep(NA_real_, TRANSFER_BOOT_B)

for (b in seq_len(TRANSFER_BOOT_B)) {
  sampled_keys <- sample(pair_keys, size = P, replace = TRUE)
  draw_rows <- vector("list", length(sampled_keys))
  for (k in seq_along(sampled_keys)) {
    z <- rows_by_pair[[sampled_keys[k]]]
    z$bootstrap_draw <- k
    draw_rows[[k]] <- z
  }
  bd <- do.call(rbind, draw_rows)
  boot_beta[b] <- fit_transfer(bd)
}

boot_finite <- boot_beta[is.finite(boot_beta)]
if (length(boot_finite) < 0.95 * TRANSFER_BOOT_B) {
  stop("Fewer than 95% of transfer bootstrap replicates were estimable")
}
ci <- as.numeric(quantile(
  boot_finite,
  probs = c(0.025, 0.975),
  names = FALSE
))

transfer_supported <- beta_transfer < 0 && ci[2] < 0
prior_magnitude_excluded <- ci[1] > PRIOR_BETA_REFERENCE

summary_row <- data.frame(
  source_commit = SOURCE_COMMIT,
  early_window = paste0(EARLY_START, "-", EARLY_END),
  late_window = paste0(LATE_START, "-", LATE_END),
  eligible_species_target_rows = nrow(analysis),
  eligible_unique_spatial_pairs = length(unique(analysis$pair_key)),
  eligible_species = length(unique(analysis$species)),
  min_bird_years_per_window = MIN_BIRD_YEARS_PER_WINDOW,
  delta_rho_unique_pair_mean = pair_mu,
  delta_rho_unique_pair_sd = pair_sd,
  beta_transfer = beta_transfer,
  boot_ci_low_95 = ci[1],
  boot_ci_high_95 = ci[2],
  bootstrap_replicates = TRANSFER_BOOT_B,
  bootstrap_finite_replicates = length(boot_finite),
  bootstrap_seed = TRANSFER_BOOT_SEED,
  prior_beta_reference = PRIOR_BETA_REFERENCE,
  information_to_timing_transfer = ifelse(
    transfer_supported,
    "SUPPORTED",
    "NOT_SUPPORTED"
  ),
  prior_magnitude_transfer_excluded = ifelse(
    prior_magnitude_excluded,
    "YES",
    "NO"
  )
)

write.csv(
  summary_row,
  "outputs/payoff_b_v8_transfer_primary_summary.csv",
  row.names = FALSE
)
write.csv(
  analysis,
  "outputs/payoff_b_v8_transfer_primary_rows.csv",
  row.names = FALSE
)
write.csv(
  data.frame(
    replicate = seq_len(TRANSFER_BOOT_B),
    beta_transfer = boot_beta
  ),
  "outputs/payoff_b_v8_transfer_primary_bootstrap.csv",
  row.names = FALSE
)

cat("\nPAYOFF-B V8 DOWNSTREAM INFORMATION-TO-TIMING TRANSFER\n")
print(summary_row)
cat("\nPrimary direction: beta_transfer < 0.\n")
cat("No post-primary transfer sensitivity and no migration-speed change analysis was run.\n")
