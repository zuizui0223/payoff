#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC / OUTCOME-INFORMED DIAGNOSTIC.
# This analysis was designed after both the frozen V8 correlation result and
# the metric-scale information-value diagnostic were known.
#
# Question:
# Does change in decision-scale environmental information value
#
#   delta_G_CV = [MSE(no source) - MSE(source)]_late
#              - [MSE(no source) - MSE(source)]_early
#
# predict change in realized bird arrival-green-up mismatch?
#
# This is not preregistered and cannot replace the frozen rho-transfer test.

SOURCE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_metric_scale_diagnostic.R"
if (!file.exists(SOURCE_SCRIPT)) stop("Missing metric-scale diagnostic script")
source(SOURCE_SCRIPT, local = FALSE)

B <- 10000L
SEED <- 20261006L
PERM_B <- 2000L
MIN_YEARS <- 6L

# Pair-level decision-scale exposure.
g_pair <- unique(diag_pairs[, c(
  "pair_key",
  "delta_loo_value_mse",
  "loo_value_mse_early",
  "loo_value_mse_late"
)])
g_pair <- g_pair[is.finite(g_pair$delta_loo_value_mse), , drop = FALSE]

analysis <- merge(
  bird_rows,
  g_pair,
  by = "pair_key",
  all = FALSE,
  sort = FALSE
)

if (nrow(analysis) < 20) stop("Too few bird rows")
if (length(unique(analysis$pair_key)) < 20) stop("Too few unique pairs")
if (length(unique(analysis$species)) < 5) stop("Too few species")

# Standardize delta G across unique environmental pairs only.
g_mu <- mean(g_pair$delta_loo_value_mse)
g_sd <- sd(g_pair$delta_loo_value_mse)
if (!is.finite(g_sd) || g_sd <= 0) stop("Invalid delta-G SD")
analysis$z_delta_G <- (analysis$delta_loo_value_mse - g_mu) / g_sd

fit_beta <- function(df, outcome) {
  if (nrow(df) < 3 || length(unique(df$z_delta_G)) < 2) return(NA_real_)
  nsp <- table(df$species)
  w <- 1 / as.numeric(nsp[df$species])
  fit <- try(
    lm(df[[outcome]] ~ df$z_delta_G, weights = w),
    silent = TRUE
  )
  if (inherits(fit, "try-error")) return(NA_real_)
  unname(coef(fit)[2])
}

beta_log <- fit_beta(analysis, "delta_log")
beta_days <- fit_beta(analysis, "delta_abs_days")

# Pair bootstrap preserving all species rows carried by each environmental pair.
rows_by_pair <- split(analysis, analysis$pair_key)
pair_keys <- unique(analysis$pair_key)
P <- length(pair_keys)

set.seed(SEED)
boot_log <- rep(NA_real_, B)
boot_days <- rep(NA_real_, B)

for (b in seq_len(B)) {
  draw <- sample(pair_keys, P, replace = TRUE)
  zz <- do.call(rbind, lapply(seq_along(draw), function(i) {
    z <- rows_by_pair[[draw[i]]]
    z$bootstrap_draw <- i
    z
  }))
  boot_log[b] <- fit_beta(zz, "delta_log")
  boot_days[b] <- fit_beta(zz, "delta_abs_days")
}

ci_log <- as.numeric(quantile(boot_log[is.finite(boot_log)],
                              c(0.025, 0.975), names = FALSE))
ci_days <- as.numeric(quantile(boot_days[is.finite(boot_days)],
                               c(0.025, 0.975), names = FALSE))

# Fixed-arrival structural null:
# hold each species-target row at its 2002-2017 mean arrival date and let
# green-up vary exactly as observed. This preserves shared target-green-up
# geometry while removing temporal bird response.
bird0 <- dat[, c("species", "year", "cell", "arr_GAM_mean", "gr_mn")]
bird0$year <- as.integer(bird0$year)
bird0$cell <- as.numeric(as.character(bird0$cell))
bird0$arr_GAM_mean <- as.numeric(bird0$arr_GAM_mean)
bird0$gr_mn <- as.numeric(bird0$gr_mn)
bird0 <- bird0[
  is.finite(bird0$year) & is.finite(bird0$cell) &
    is.finite(bird0$arr_GAM_mean) & is.finite(bird0$gr_mn),
  ,
  drop = FALSE
]
bird0 <- unique(bird0)

mean_arrival <- aggregate(
  arr_GAM_mean ~ species + cell,
  data = bird0,
  FUN = mean
)
names(mean_arrival)[3] <- "arrival_fixed"
bird0 <- merge(
  bird0,
  mean_arrival,
  by = c("species", "cell"),
  all.x = TRUE,
  sort = FALSE
)
bird0$fixed_abs <- abs(bird0$gr_mn - bird0$arrival_fixed)
bird0$fixed_log <- log1p(bird0$fixed_abs)

fixed_window <- function(species, target_cell, start_year, end_year) {
  z <- bird0[
    bird0$species == species &
      bird0$cell == target_cell &
      bird0$year >= start_year &
      bird0$year <= end_year,
    ,
    drop = FALSE
  ]
  z <- z[!duplicated(z$year), , drop = FALSE]
  c(
    n = nrow(z),
    abs = if (nrow(z) > 0) mean(z$fixed_abs) else NA_real_,
    log = if (nrow(z) > 0) mean(z$fixed_log) else NA_real_
  )
}

fw_e <- t(mapply(
  fixed_window,
  analysis$species,
  analysis$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
))
fw_l <- t(mapply(
  fixed_window,
  analysis$species,
  analysis$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
))

analysis$fixed_early_n <- as.integer(fw_e[, "n"])
analysis$fixed_late_n <- as.integer(fw_l[, "n"])
analysis$fixed_delta_abs_days <-
  as.numeric(fw_l[, "abs"]) - as.numeric(fw_e[, "abs"])
analysis$fixed_delta_log <-
  as.numeric(fw_l[, "log"]) - as.numeric(fw_e[, "log"])

fixed_ok <- analysis$fixed_early_n >= MIN_YEARS &
  analysis$fixed_late_n >= MIN_YEARS &
  is.finite(analysis$fixed_delta_abs_days) &
  is.finite(analysis$fixed_delta_log)

fixed_analysis <- analysis[fixed_ok, , drop = FALSE]
beta_fixed_log <- fit_beta(fixed_analysis, "fixed_delta_log")
beta_fixed_days <- fit_beta(fixed_analysis, "fixed_delta_abs_days")

# Pair-bootstrap the observed-minus-fixed increment.
fixed_rows_by_pair <- split(fixed_analysis, fixed_analysis$pair_key)
fixed_keys <- unique(fixed_analysis$pair_key)
PF <- length(fixed_keys)

set.seed(SEED + 1L)
boot_increment_log <- rep(NA_real_, B)
boot_increment_days <- rep(NA_real_, B)

for (b in seq_len(B)) {
  draw <- sample(fixed_keys, PF, replace = TRUE)
  zz <- do.call(rbind, lapply(seq_along(draw), function(i) {
    z <- fixed_rows_by_pair[[draw[i]]]
    z$bootstrap_draw <- i
    z
  }))
  bo <- fit_beta(zz, "delta_log")
  bn <- fit_beta(zz, "fixed_delta_log")
  do <- fit_beta(zz, "delta_abs_days")
  dn <- fit_beta(zz, "fixed_delta_abs_days")
  boot_increment_log[b] <- bo - bn
  boot_increment_days[b] <- do - dn
}

increment_log <- beta_log - beta_fixed_log
increment_days <- beta_days - beta_fixed_days
increment_log_ci <- as.numeric(quantile(
  boot_increment_log[is.finite(boot_increment_log)],
  c(0.025, 0.975), names = FALSE
))
increment_days_ci <- as.numeric(quantile(
  boot_increment_days[is.finite(boot_increment_days)],
  c(0.025, 0.975), names = FALSE
))

# Within-window arrival permutation.
# Permute arrival dates within each species-target row and each period,
# preserving the period-specific arrival distribution while destroying
# year-specific alignment to green-up.
row_key <- paste(bird0$species, bird0$cell, sep = "::")
bird0$row_key <- row_key

analysis_keys <- unique(paste(analysis$species, analysis$target_cell, sep = "::"))
bird_perm_base <- bird0[bird0$row_key %in% analysis_keys, , drop = FALSE]

calc_permuted_rows <- function(df, seed) {
  set.seed(seed)
  z <- df
  z$period <- ifelse(
    z$year >= EARLY_START & z$year <= EARLY_END,
    "early",
    ifelse(z$year >= LATE_START & z$year <= LATE_END, "late", NA_character_)
  )
  z <- z[!is.na(z$period), , drop = FALSE]
  group <- paste(z$row_key, z$period, sep = "::")
  split_idx <- split(seq_len(nrow(z)), group)
  perm_arr <- z$arr_GAM_mean
  for (ix in split_idx) {
    perm_arr[ix] <- sample(z$arr_GAM_mean[ix], length(ix), replace = FALSE)
  }
  z$perm_abs <- abs(z$gr_mn - perm_arr)
  z$perm_log <- log1p(z$perm_abs)

  out <- vector("list", nrow(analysis))
  for (i in seq_len(nrow(analysis))) {
    sp <- analysis$species[i]
    cell <- analysis$target_cell[i]
    zz <- z[z$species == sp & z$cell == cell, , drop = FALSE]
    e <- zz[zz$period == "early", , drop = FALSE]
    l <- zz[zz$period == "late", , drop = FALSE]
    if (nrow(e) < MIN_YEARS || nrow(l) < MIN_YEARS) next
    out[[i]] <- data.frame(
      species = sp,
      pair_key = analysis$pair_key[i],
      z_delta_G = analysis$z_delta_G[i],
      delta_perm_log = mean(l$perm_log) - mean(e$perm_log),
      delta_perm_abs = mean(l$perm_abs) - mean(e$perm_abs)
    )
  }
  do.call(rbind, out)
}

perm_beta_log <- rep(NA_real_, PERM_B)
perm_beta_days <- rep(NA_real_, PERM_B)

for (b in seq_len(PERM_B)) {
  pp <- calc_permuted_rows(bird_perm_base, SEED + 1000L + b)
  if (is.null(pp) || nrow(pp) < 3) next
  names(pp)[names(pp) == "delta_perm_log"] <- "delta_log"
  names(pp)[names(pp) == "delta_perm_abs"] <- "delta_abs_days"
  perm_beta_log[b] <- fit_beta(pp, "delta_log")
  perm_beta_days[b] <- fit_beta(pp, "delta_abs_days")
}

perm_log_f <- perm_beta_log[is.finite(perm_beta_log)]
perm_days_f <- perm_beta_days[is.finite(perm_beta_days)]

summary_row <- data.frame(
  diagnostic_status = "POSTHOC_OUTCOME_INFORMED",
  bird_rows = nrow(analysis),
  unique_pairs = length(unique(analysis$pair_key)),
  species = length(unique(analysis$species)),
  delta_G_pair_mean = g_mu,
  delta_G_pair_sd = g_sd,
  beta_log = beta_log,
  beta_log_ci_low_95 = ci_log[1],
  beta_log_ci_high_95 = ci_log[2],
  beta_days = beta_days,
  beta_days_ci_low_95 = ci_days[1],
  beta_days_ci_high_95 = ci_days[2],
  beta_fixed_log = beta_fixed_log,
  beta_fixed_days = beta_fixed_days,
  bird_increment_log = increment_log,
  bird_increment_log_ci_low_95 = increment_log_ci[1],
  bird_increment_log_ci_high_95 = increment_log_ci[2],
  bird_increment_days = increment_days,
  bird_increment_days_ci_low_95 = increment_days_ci[1],
  bird_increment_days_ci_high_95 = increment_days_ci[2],
  perm_log_median = median(perm_log_f),
  perm_log_low_95 = quantile(perm_log_f, 0.025),
  perm_log_high_95 = quantile(perm_log_f, 0.975),
  perm_log_fraction_le_observed = mean(perm_log_f <= beta_log),
  perm_days_median = median(perm_days_f),
  perm_days_low_95 = quantile(perm_days_f, 0.025),
  perm_days_high_95 = quantile(perm_days_f, 0.975),
  perm_days_fraction_le_observed = mean(perm_days_f <= beta_days),
  bootstrap_replicates = B,
  permutation_replicates = PERM_B,
  seed = SEED
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(
  analysis,
  "outputs/payoff_b_v8_information_value_transfer_rows.csv",
  row.names = FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_information_value_transfer_summary.csv",
  row.names = FALSE
)
write.csv(
  data.frame(
    replicate = seq_len(B),
    beta_log = boot_log,
    beta_days = boot_days,
    bird_increment_log = boot_increment_log,
    bird_increment_days = boot_increment_days
  ),
  "outputs/payoff_b_v8_information_value_transfer_bootstrap.csv",
  row.names = FALSE
)
write.csv(
  data.frame(
    replicate = seq_len(PERM_B),
    beta_log = perm_beta_log,
    beta_days = perm_beta_days
  ),
  "outputs/payoff_b_v8_information_value_transfer_permutation.csv",
  row.names = FALSE
)

cat("\nPOSTHOC INFORMATION-VALUE TO BIRD-TRACKING TRANSFER\n")
print(summary_row)
