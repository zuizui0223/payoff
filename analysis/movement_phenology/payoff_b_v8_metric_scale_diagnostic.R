#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# Outcome-informed diagnostic.
# This script MUST NOT be described as preregistered or confirmatory.
# It reuses the frozen V8 mapping and windows, but asks whether the
# correlation-based coordinate and day-scale forecast error tell the same story.

PRIMARY_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_primary.R"
if (!file.exists(PRIMARY_SCRIPT)) stop("Missing V8 primary script")
source(PRIMARY_SCRIPT, local = FALSE)

DIAG_BOOT_B <- 10000L
DIAG_SEED <- 20261005L
MIN_BIRD_YEARS_PER_WINDOW <- 6L

pair_window <- function(source_cell, target_cell, start_year, end_year) {
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

  z <- merge(source, target, by = "year", all = FALSE)
  z <- z[
    is.finite(z$year) &
      is.finite(z$source_greenup) &
      is.finite(z$target_greenup),
    ,
    drop = FALSE
  ]
  z <- z[!duplicated(z$year), , drop = FALSE]
  z <- z[order(z$year), , drop = FALSE]

  n <- nrow(z)
  if (n < MIN_PAIRS_PER_WINDOW) {
    return(c(
      n = n,
      rho = NA_real_,
      target_sd = NA_real_,
      target_rms = NA_real_,
      slope = NA_real_,
      r2 = NA_real_,
      rmse_in = NA_real_,
      explained_mse = NA_real_,
      loo_rmse = NA_real_,
      loo_null_rmse = NA_real_
    ))
  }

  fit_s <- lm(source_greenup ~ year, data = z)
  fit_t <- lm(target_greenup ~ year, data = z)
  x <- resid(fit_s)
  y <- resid(fit_t)

  if (!is.finite(sd(x)) || !is.finite(sd(y)) || sd(x) <= 0 || sd(y) <= 0) {
    return(c(
      n = n,
      rho = NA_real_,
      target_sd = NA_real_,
      target_rms = NA_real_,
      slope = NA_real_,
      r2 = NA_real_,
      rmse_in = NA_real_,
      explained_mse = NA_real_,
      loo_rmse = NA_real_,
      loo_null_rmse = NA_real_
    ))
  }

  mod <- lm(y ~ x)
  err <- resid(mod)

  loo_err <- rep(NA_real_, n)
  loo_null_err <- rep(NA_real_, n)

  for (j in seq_len(n)) {
    tr <- z[-j, , drop = FALSE]
    te <- z[j, , drop = FALSE]

    src_trend <- try(lm(source_greenup ~ year, data = tr), silent = TRUE)
    tgt_trend <- try(lm(target_greenup ~ year, data = tr), silent = TRUE)
    if (inherits(src_trend, "try-error") || inherits(tgt_trend, "try-error")) next

    xtr <- resid(src_trend)
    ytr <- resid(tgt_trend)
    if (!is.finite(sd(xtr)) || sd(xtr) <= 0) next

    anomaly_model <- try(lm(ytr ~ xtr), silent = TRUE)
    if (inherits(anomaly_model, "try-error")) next

    src_expected <- as.numeric(predict(src_trend, newdata = te))
    tgt_expected <- as.numeric(predict(tgt_trend, newdata = te))
    if (!is.finite(src_expected) || !is.finite(tgt_expected)) next

    x_hold <- te$source_greenup - src_expected
    anomaly_pred <- as.numeric(
      coef(anomaly_model)[1] + coef(anomaly_model)[2] * x_hold
    )
    if (!is.finite(anomaly_pred)) next

    pred_with_source <- tgt_expected + anomaly_pred
    loo_err[j] <- te$target_greenup - pred_with_source
    loo_null_err[j] <- te$target_greenup - tgt_expected
  }

  c(
    n = n,
    rho = cor(x, y),
    target_sd = sd(y),
    target_rms = sqrt(mean(y^2)),
    slope = unname(coef(mod)["x"]),
    r2 = summary(mod)$r.squared,
    rmse_in = sqrt(mean(err^2)),
    explained_mse = mean(y^2) - mean(err^2),
    loo_rmse = if (all(is.finite(loo_err))) sqrt(mean(loo_err^2)) else NA_real_,
    loo_null_rmse = if (all(is.finite(loo_null_err))) sqrt(mean(loo_null_err^2)) else NA_real_
  )
}

early <- t(mapply(
  pair_window,
  pairs$source_cell,
  pairs$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
))
late <- t(mapply(
  pair_window,
  pairs$source_cell,
  pairs$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
))

diag_pairs <- pairs[, c(
  "pair_key", "source_cell", "target_cell",
  "source_target_distance_km", "rho_early", "rho_late", "delta_rho"
)]

metrics <- c(
  "target_sd", "target_rms", "slope", "r2", "rmse_in",
  "explained_mse", "loo_rmse", "loo_null_rmse"
)

for (m in metrics) {
  diag_pairs[[paste0(m, "_early")]] <- as.numeric(early[, m])
  diag_pairs[[paste0(m, "_late")]] <- as.numeric(late[, m])
  diag_pairs[[paste0("delta_", m)]] <-
    diag_pairs[[paste0(m, "_late")]] - diag_pairs[[paste0(m, "_early")]]
}

# The rho reconstruction must match the frozen primary output numerically.
rho_check_early <- max(abs(as.numeric(early[, "rho"]) - diag_pairs$rho_early))
rho_check_late <- max(abs(as.numeric(late[, "rho"]) - diag_pairs$rho_late))
if (!is.finite(rho_check_early) || !is.finite(rho_check_late) ||
    rho_check_early > 1e-10 || rho_check_late > 1e-10) {
  stop("Diagnostic rho reconstruction does not match frozen V8 primary")
}

# Coordinates for optional spatial summaries.
coord <- unique(cells[, c("cell", "cell_lat2", "cell_lng")])
coord <- coord[is.finite(coord$cell) & is.finite(coord$cell_lat2) &
                 is.finite(coord$cell_lng), , drop = FALSE]
coord <- coord[!duplicated(coord$cell), , drop = FALSE]

src_coord <- coord
names(src_coord) <- c("source_cell", "source_lat", "source_lng")
tgt_coord <- coord
names(tgt_coord) <- c("target_cell", "target_lat", "target_lng")
diag_pairs <- merge(diag_pairs, src_coord, by = "source_cell", all.x = TRUE)
diag_pairs <- merge(diag_pairs, tgt_coord, by = "target_cell", all.x = TRUE)
diag_pairs$mid_lat <- (diag_pairs$source_lat + diag_pairs$target_lat) / 2
diag_pairs$mid_lng <- (diag_pairs$source_lng + diag_pairs$target_lng) / 2
diag_pairs$block5 <- paste(
  floor((diag_pairs$mid_lat + 90) / 5),
  floor((diag_pairs$mid_lng + 180) / 5),
  sep = "_"
)
diag_pairs$block10 <- paste(
  floor((diag_pairs$mid_lat + 90) / 10),
  floor((diag_pairs$mid_lng + 180) / 10),
  sep = "_"
)

cluster_boot_mean <- function(df, value_col, cluster_col, B, seed) {
  keep <- is.finite(df[[value_col]]) & !is.na(df[[cluster_col]])
  dd <- df[keep, , drop = FALSE]
  cluster_id <- as.character(dd[[cluster_col]])
  clusters <- unique(cluster_id)
  if (length(clusters) < 2) return(c(low = NA_real_, high = NA_real_))
  by_cluster <- split(dd[[value_col]], cluster_id)

  set.seed(seed)
  out <- rep(NA_real_, B)
  for (b in seq_len(B)) {
    draw <- sample(clusters, length(clusters), replace = TRUE)
    vals <- unlist(by_cluster[draw], use.names = FALSE)
    out[b] <- mean(vals)
  }
  as.numeric(quantile(out, c(0.025, 0.975), na.rm = TRUE, names = FALSE))
}

pair_boot_mean <- function(x, B, seed) {
  x <- x[is.finite(x)]
  set.seed(seed)
  out <- replicate(B, mean(sample(x, length(x), replace = TRUE)))
  as.numeric(quantile(out, c(0.025, 0.975), names = FALSE))
}

summary_rows <- list()
sr <- 0L
# Out-of-sample source value on the same loss scale as the theory.
# Under squared-error loss, information value is the reduction in held-out MSE:
#
#   G_CV = MSE(no source) - MSE(source informed).
#
# Positive values mean that the source cue reduces held-out prediction loss.
# RMSE differences are retained only as an intuitive day-scale companion.
diag_pairs$loo_mse_early <- diag_pairs$loo_rmse_early^2
diag_pairs$loo_mse_late <- diag_pairs$loo_rmse_late^2
diag_pairs$loo_null_mse_early <- diag_pairs$loo_null_rmse_early^2
diag_pairs$loo_null_mse_late <- diag_pairs$loo_null_rmse_late^2

diag_pairs$loo_value_mse_early <-
  diag_pairs$loo_null_mse_early - diag_pairs$loo_mse_early
diag_pairs$loo_value_mse_late <-
  diag_pairs$loo_null_mse_late - diag_pairs$loo_mse_late
diag_pairs$delta_loo_value_mse <-
  diag_pairs$loo_value_mse_late - diag_pairs$loo_value_mse_early

diag_pairs$loo_skill_rmse_early <-
  diag_pairs$loo_null_rmse_early - diag_pairs$loo_rmse_early
diag_pairs$loo_skill_rmse_late <-
  diag_pairs$loo_null_rmse_late - diag_pairs$loo_rmse_late
diag_pairs$delta_loo_skill_rmse <-
  diag_pairs$loo_skill_rmse_late - diag_pairs$loo_skill_rmse_early

for (m in metrics) {
  e <- diag_pairs[[paste0(m, "_early")]]
  l <- diag_pairs[[paste0(m, "_late")]]
  d <- diag_pairs[[paste0("delta_", m)]]
  ok <- is.finite(e) & is.finite(l) & is.finite(d)

  pci <- pair_boot_mean(d[ok], DIAG_BOOT_B, DIAG_SEED)
  sci <- cluster_boot_mean(
    diag_pairs[ok, ], paste0("delta_", m), "source_cell",
    DIAG_BOOT_B, DIAG_SEED + 1L
  )
  tci <- cluster_boot_mean(
    diag_pairs[ok, ], paste0("delta_", m), "target_cell",
    DIAG_BOOT_B, DIAG_SEED + 2L
  )
  b5ci <- cluster_boot_mean(
    diag_pairs[ok, ], paste0("delta_", m), "block5",
    DIAG_BOOT_B, DIAG_SEED + 3L
  )
  b10ci <- cluster_boot_mean(
    diag_pairs[ok, ], paste0("delta_", m), "block10",
    DIAG_BOOT_B, DIAG_SEED + 4L
  )

  sr <- sr + 1L
  summary_rows[[sr]] <- data.frame(
    metric = m,
    n_pairs = sum(ok),
    early_pair_mean = mean(e[ok]),
    late_pair_mean = mean(l[ok]),
    late_minus_early = mean(d[ok]),
    pair_ci_low_95 = pci[1],
    pair_ci_high_95 = pci[2],
    source_cluster_ci_low_95 = sci[1],
    source_cluster_ci_high_95 = sci[2],
    target_cluster_ci_low_95 = tci[1],
    target_cluster_ci_high_95 = tci[2],
    block5_ci_low_95 = b5ci[1],
    block5_ci_high_95 = b5ci[2],
    block10_ci_low_95 = b10ci[1],
    block10_ci_high_95 = b10ci[2]
  )
}
diag_summary <- do.call(rbind, summary_rows)

skill_ok <- is.finite(diag_pairs$loo_skill_rmse_early) &
  is.finite(diag_pairs$loo_skill_rmse_late) &
  is.finite(diag_pairs$delta_loo_skill_rmse)

skill_pair_ci <- pair_boot_mean(
  diag_pairs$delta_loo_skill_rmse[skill_ok],
  DIAG_BOOT_B,
  DIAG_SEED + 10L
)
skill_source_ci <- cluster_boot_mean(
  diag_pairs[skill_ok, ], "delta_loo_skill_rmse", "source_cell",
  DIAG_BOOT_B, DIAG_SEED + 11L
)
skill_target_ci <- cluster_boot_mean(
  diag_pairs[skill_ok, ], "delta_loo_skill_rmse", "target_cell",
  DIAG_BOOT_B, DIAG_SEED + 12L
)
skill_block5_ci <- cluster_boot_mean(
  diag_pairs[skill_ok, ], "delta_loo_skill_rmse", "block5",
  DIAG_BOOT_B, DIAG_SEED + 13L
)
skill_block10_ci <- cluster_boot_mean(
  diag_pairs[skill_ok, ], "delta_loo_skill_rmse", "block10",
  DIAG_BOOT_B, DIAG_SEED + 14L
)

# Primary post-hoc information-value summary on squared-loss scale.
value_ok <- is.finite(diag_pairs$loo_value_mse_early) &
  is.finite(diag_pairs$loo_value_mse_late) &
  is.finite(diag_pairs$delta_loo_value_mse)

value_pair_ci <- pair_boot_mean(
  diag_pairs$delta_loo_value_mse[value_ok],
  DIAG_BOOT_B,
  DIAG_SEED + 20L
)
value_source_ci <- cluster_boot_mean(
  diag_pairs[value_ok, ], "delta_loo_value_mse", "source_cell",
  DIAG_BOOT_B, DIAG_SEED + 21L
)
value_target_ci <- cluster_boot_mean(
  diag_pairs[value_ok, ], "delta_loo_value_mse", "target_cell",
  DIAG_BOOT_B, DIAG_SEED + 22L
)
value_block5_ci <- cluster_boot_mean(
  diag_pairs[value_ok, ], "delta_loo_value_mse", "block5",
  DIAG_BOOT_B, DIAG_SEED + 23L
)
value_block10_ci <- cluster_boot_mean(
  diag_pairs[value_ok, ], "delta_loo_value_mse", "block10",
  DIAG_BOOT_B, DIAG_SEED + 24L
)

forecast_skill_summary <- data.frame(
  n_pairs = sum(skill_ok),
  loo_value_mse_early_mean =
    mean(diag_pairs$loo_value_mse_early[value_ok]),
  loo_value_mse_late_mean =
    mean(diag_pairs$loo_value_mse_late[value_ok]),
  delta_loo_value_mse_mean =
    mean(diag_pairs$delta_loo_value_mse[value_ok]),
  value_pair_ci_low_95 = value_pair_ci[1],
  value_pair_ci_high_95 = value_pair_ci[2],
  value_source_cluster_ci_low_95 = value_source_ci[1],
  value_source_cluster_ci_high_95 = value_source_ci[2],
  value_target_cluster_ci_low_95 = value_target_ci[1],
  value_target_cluster_ci_high_95 = value_target_ci[2],
  value_block5_ci_low_95 = value_block5_ci[1],
  value_block5_ci_high_95 = value_block5_ci[2],
  value_block10_ci_low_95 = value_block10_ci[1],
  value_block10_ci_high_95 = value_block10_ci[2],
  loo_skill_rmse_early_mean =
    mean(diag_pairs$loo_skill_rmse_early[skill_ok]),
  loo_skill_rmse_late_mean =
    mean(diag_pairs$loo_skill_rmse_late[skill_ok]),
  delta_loo_skill_rmse_mean =
    mean(diag_pairs$delta_loo_skill_rmse[skill_ok]),
  rmse_pair_ci_low_95 = skill_pair_ci[1],
  rmse_pair_ci_high_95 = skill_pair_ci[2],
  rmse_source_cluster_ci_low_95 = skill_source_ci[1],
  rmse_source_cluster_ci_high_95 = skill_source_ci[2],
  rmse_target_cluster_ci_low_95 = skill_target_ci[1],
  rmse_target_cluster_ci_high_95 = skill_target_ci[2],
  rmse_block5_ci_low_95 = skill_block5_ci[1],
  rmse_block5_ci_high_95 = skill_block5_ci[2],
  rmse_block10_ci_low_95 = skill_block10_ci[1],
  rmse_block10_ci_high_95 = skill_block10_ci[2],
  share_source_better_early =
    mean(diag_pairs$loo_value_mse_early[value_ok] > 0),
  share_source_better_late =
    mean(diag_pairs$loo_value_mse_late[value_ok] > 0)
)

rmse_ok <- is.finite(diag_pairs$delta_rmse_in)
share_rmse_improved <- mean(diag_pairs$delta_rmse_in[rmse_ok] < 0)
loo_ok <- is.finite(diag_pairs$delta_loo_rmse)
share_loo_improved <- if (any(loo_ok)) {
  mean(diag_pairs$delta_loo_rmse[loo_ok] < 0)
} else {
  NA_real_
}

# Same bird eligibility as the frozen transfer lane, but report absolute mismatch
# in days as a post-hoc scale diagnostic in addition to the frozen log metric.
bird <- dat[, c("species", "year", "cell", "arr_GAM_mean", "gr_mn")]
bird$year <- as.integer(bird$year)
bird$cell <- as.numeric(as.character(bird$cell))
bird$arr_GAM_mean <- as.numeric(bird$arr_GAM_mean)
bird$gr_mn <- as.numeric(bird$gr_mn)
bird <- bird[
  is.finite(bird$year) & is.finite(bird$cell) &
    is.finite(bird$arr_GAM_mean) & is.finite(bird$gr_mn),
  ,
  drop = FALSE
]
bird <- unique(bird)
bird$abs_mismatch_days <- abs(bird$gr_mn - bird$arr_GAM_mean)
bird$log_mismatch <- log1p(bird$abs_mismatch_days)

exposure_map <- unique(eligible_map[, c(
  "species", "target_cell", "source_cell", "pair_key"
)])
exposure_map <- exposure_map[exposure_map$pair_key %in% pairs$pair_key, ]

bird_window <- function(species, target_cell, start_year, end_year) {
  z <- bird[
    bird$species == species &
      bird$cell == target_cell &
      bird$year >= start_year &
      bird$year <= end_year,
    ,
    drop = FALSE
  ]
  z <- z[!duplicated(z$year), , drop = FALSE]
  c(
    n = nrow(z),
    mean_abs_days = if (nrow(z) > 0) mean(z$abs_mismatch_days) else NA_real_,
    mean_log = if (nrow(z) > 0) mean(z$log_mismatch) else NA_real_
  )
}

be <- t(mapply(
  bird_window,
  exposure_map$species,
  exposure_map$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
))
bl <- t(mapply(
  bird_window,
  exposure_map$species,
  exposure_map$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
))

bird_rows <- exposure_map
bird_rows$early_n <- as.integer(be[, "n"])
bird_rows$late_n <- as.integer(bl[, "n"])
bird_rows$abs_days_early <- as.numeric(be[, "mean_abs_days"])
bird_rows$abs_days_late <- as.numeric(bl[, "mean_abs_days"])
bird_rows$log_early <- as.numeric(be[, "mean_log"])
bird_rows$log_late <- as.numeric(bl[, "mean_log"])

bird_rows <- bird_rows[
  bird_rows$early_n >= MIN_BIRD_YEARS_PER_WINDOW &
    bird_rows$late_n >= MIN_BIRD_YEARS_PER_WINDOW &
    is.finite(bird_rows$abs_days_early) &
    is.finite(bird_rows$abs_days_late),
  ,
  drop = FALSE
]
bird_rows$delta_abs_days <- bird_rows$abs_days_late - bird_rows$abs_days_early
bird_rows$delta_log <- bird_rows$log_late - bird_rows$log_early

species_abs <- aggregate(
  delta_abs_days ~ species,
  data = bird_rows,
  FUN = mean
)
species_log <- aggregate(
  delta_log ~ species,
  data = bird_rows,
  FUN = mean
)

# Pair bootstrap preserving all species rows attached to each sampled pair.
pair_keys_bird <- unique(bird_rows$pair_key)
rows_by_pair <- split(bird_rows, bird_rows$pair_key)
set.seed(DIAG_SEED)
boot_abs_row <- rep(NA_real_, DIAG_BOOT_B)
boot_abs_species <- rep(NA_real_, DIAG_BOOT_B)
boot_log_row <- rep(NA_real_, DIAG_BOOT_B)
boot_log_species <- rep(NA_real_, DIAG_BOOT_B)

for (b in seq_len(DIAG_BOOT_B)) {
  draw <- sample(pair_keys_bird, length(pair_keys_bird), replace = TRUE)
  zz <- do.call(rbind, lapply(seq_along(draw), function(i) {
    x <- rows_by_pair[[draw[i]]]
    x$draw_id <- i
    x
  }))
  boot_abs_row[b] <- mean(zz$delta_abs_days)
  boot_log_row[b] <- mean(zz$delta_log)
  sa <- aggregate(delta_abs_days ~ species, data = zz, FUN = mean)
  sl <- aggregate(delta_log ~ species, data = zz, FUN = mean)
  boot_abs_species[b] <- mean(sa$delta_abs_days)
  boot_log_species[b] <- mean(sl$delta_log)
}

bird_summary <- data.frame(
  n_rows = nrow(bird_rows),
  n_pairs = length(unique(bird_rows$pair_key)),
  n_species = length(unique(bird_rows$species)),
  abs_days_early_unweighted = mean(bird_rows$abs_days_early),
  abs_days_late_unweighted = mean(bird_rows$abs_days_late),
  delta_abs_days_unweighted = mean(bird_rows$delta_abs_days),
  delta_abs_days_unweighted_ci_low_95 = quantile(boot_abs_row, 0.025),
  delta_abs_days_unweighted_ci_high_95 = quantile(boot_abs_row, 0.975),
  delta_abs_days_equal_species = mean(species_abs$delta_abs_days),
  delta_abs_days_equal_species_ci_low_95 = quantile(boot_abs_species, 0.025),
  delta_abs_days_equal_species_ci_high_95 = quantile(boot_abs_species, 0.975),
  delta_log_unweighted = mean(bird_rows$delta_log),
  delta_log_unweighted_ci_low_95 = quantile(boot_log_row, 0.025),
  delta_log_unweighted_ci_high_95 = quantile(boot_log_row, 0.975),
  delta_log_equal_species = mean(species_log$delta_log),
  delta_log_equal_species_ci_low_95 = quantile(boot_log_species, 0.025),
  delta_log_equal_species_ci_high_95 = quantile(boot_log_species, 0.975)
)

status <- data.frame(
  diagnostic_status = "POSTHOC_OUTCOME_INFORMED",
  frozen_primary_estimand = "detrended_source_target_Pearson_rho",
  rho_reconstruction_max_abs_diff_early = rho_check_early,
  rho_reconstruction_max_abs_diff_late = rho_check_late,
  share_pairs_lower_in_sample_rmse_late = share_rmse_improved,
  share_pairs_lower_loo_rmse_late = share_loo_improved,
  bootstrap_replicates = DIAG_BOOT_B,
  bootstrap_seed = DIAG_SEED
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(
  diag_pairs,
  "outputs/payoff_b_v8_metric_scale_pairs.csv",
  row.names = FALSE
)
write.csv(
  diag_summary,
  "outputs/payoff_b_v8_metric_scale_summary.csv",
  row.names = FALSE
)
write.csv(
  forecast_skill_summary,
  "outputs/payoff_b_v8_metric_scale_forecast_skill_summary.csv",
  row.names = FALSE
)
write.csv(
  bird_rows,
  "outputs/payoff_b_v8_metric_scale_bird_rows.csv",
  row.names = FALSE
)
write.csv(
  bird_summary,
  "outputs/payoff_b_v8_metric_scale_bird_summary.csv",
  row.names = FALSE
)
write.csv(
  status,
  "outputs/payoff_b_v8_metric_scale_status.csv",
  row.names = FALSE
)

cat("\nV8 POST-HOC METRIC-SCALE DIAGNOSTIC\n")
print(status)
cat("\nEnvironmental metrics:\n")
print(diag_summary)
cat("\nOut-of-sample source forecast skill:\n")
print(forecast_skill_summary)
cat("\nBird mismatch on day and frozen log scales:\n")
print(bird_summary)
