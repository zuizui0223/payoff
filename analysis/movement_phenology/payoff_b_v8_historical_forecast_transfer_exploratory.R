#!/usr/bin/env Rscript

# PAYOFF-B historical forecast transfer: exploratory environmental-only audit.
#
# Why: a within-window correlation rise does NOT establish that a forecasting
# relationship learned in an earlier period predicts a later climate well.
#
# Frozen V8 source periods, source-target mapping and eligibility are reused.
# Nothing in this script uses bird arrival, observed behavioral decisions,
# mismatch, survival, reproductive outcomes or protected V8 hypotheses.
# Scores are post-outcome exploratory, not a new preregistered confirmation.

options(stringsAsFactors = FALSE)

EARLY_YEARS <- 2002:2009
LATE_YEARS <- 2010:2017
RIDGE_PENALTY <- 1.0
BOOT_REPS <- 2000L
BOOT_SEED <- 20261008L

# Every feature mean and SD, along with regression parameters, is estimated
# from the early training years. Never standardize with later data.
train_ridge <- function(x, y, penalty = RIDGE_PENALTY) {
  if (!is.matrix(x) || nrow(x) != length(y) || nrow(x) < 6L) {
    stop("Training data must be a >=6-row matrix with aligned target")
  }
  if (!is.finite(penalty) || penalty <= 0) {
    stop("Training-only ridge penalty must be positive and finite")
  }
  ridge <- diag(c(0, rep(penalty, ncol(x) - 1L)), nrow = ncol(x))
  beta <- solve(crossprod(x) + ridge, crossprod(x, y))
  as.numeric(beta)
}

forecast_pair <- function(paired) {
  early <- paired[paired$year %in% EARLY_YEARS, , drop = FALSE]
  late <- paired[paired$year %in% LATE_YEARS, , drop = FALSE]
  if (nrow(early) < 6L || nrow(late) < 6L) return(NULL)

  scale_training <- function(v) {
    z <- sd(v)
    if (!is.finite(z) || z < 1e-8) return(NULL)
    list(mu = mean(v), sd = z)
  }
  year_sc <- scale_training(early$year)
  src_sc <- scale_training(early$source_greenup)
  target_sc <- scale_training(early$target_greenup)
  if (is.null(year_sc) || is.null(src_sc) || is.null(target_sc)) return(NULL)

  year_early <- (early$year - year_sc$mu) / year_sc$sd
  year_late <- (late$year - year_sc$mu) / year_sc$sd
  source_early <- (early$source_greenup - src_sc$mu) / src_sc$sd
  source_late <- (late$source_greenup - src_sc$mu) / src_sc$sd

  baseline_train <- cbind(intercept = 1, year = year_early)
  baseline_test <- cbind(intercept = 1, year = year_late)
  cue_train <- cbind(intercept = 1, year = year_early, origin = source_early)
  cue_test <- cbind(intercept = 1, year = year_late, origin = source_late)

  b0 <- train_ridge(baseline_train, early$target_greenup)
  b1 <- train_ridge(cue_train, early$target_greenup)
  pred0 <- as.numeric(baseline_test %*% b0)
  pred1 <- as.numeric(cue_test %*% b1)
  e0 <- late$target_greenup - pred0
  e1 <- late$target_greenup - pred1

  # These outcomes are still geographically reconstructed environmental
  # series, not real-time information perceived by the birds.
  # Training-target-SD scales yield comparable dimensionless paired scores.
  improvement <- (e0^2 - e1^2) / (target_sc$sd^2)
  audit_rows <- data.frame(
    year = late$year,
    time_only_mse = e0^2,
    time_plus_origin_mse = e1^2,
    standardized_improvement = improvement,
    target = late$target_greenup,
    origin = late$source_greenup,
    prediction_time_only = pred0,
    prediction_origin_augmented = pred1,
    origin_augmented_signed_error = e1
  )
  list(
    score = data.frame(
      train_n = nrow(early),
      holdout_n = nrow(late),
      time_only_mse = mean(e0^2),
      time_plus_origin_mse = mean(e1^2),
      standardized_improvement = mean(improvement),
      time_only_mean_signed_error = mean(e0),
      augmented_mean_signed_error = mean(e1),
      train_target_sd = target_sc$sd,
      train_source_sd = src_sc$sd,
      train_year_trend = b0[2] / year_sc$sd,
      train_origin_coef_standardized = b1[3]
    ),
    annual = audit_rows
  )
}

# Fixed-panel source-target-year extraction, consistent with frozen V8.
pair_greenup <- function(source_cell, target_cell, green) {
  src <- green[green$cell == source_cell &
    green$year %in% c(EARLY_YEARS, LATE_YEARS),
    c("year", "gr_mn"), drop = FALSE]
  tgt <- green[green$cell == target_cell &
    green$year %in% c(EARLY_YEARS, LATE_YEARS),
    c("year", "gr_mn"), drop = FALSE]
  names(src)[2] <- "source_greenup"
  names(tgt)[2] <- "target_greenup"
  paired <- merge(src, tgt, by = "year", all = FALSE)
  paired <- paired[is.finite(paired$year) &
    is.finite(paired$source_greenup) &
    is.finite(paired$target_greenup), , drop = FALSE]
  # Replicate V8's first-year-with-duplicate convention; it is not a
  # species-replicated independent pair-year observation.
  paired[!duplicated(paired$year), , drop = FALSE]
}

self_test <- function() {
  # No climate or bird outcomes. One stable source relation and one deliberately
  # reversed relation; the same early fitted cue should help only in the first.
  years <- 2002:2017
  src <- rep(c(-1.0, 0.8, -0.6, 1.1), 4L)
  stable <- data.frame(
    year = years, source_greenup = src,
    target_greenup = 20 + 10 * src
  )
  reversed <- stable
  reversed$target_greenup[years %in% LATE_YEARS] <-
    20 - 10 * src[years %in% LATE_YEARS]
  a <- forecast_pair(stable)
  b <- forecast_pair(reversed)
  if (is.null(a) || is.null(b) ||
      a$score$standardized_improvement <= 0 ||
      b$score$standardized_improvement >= 0) {
    stop("Synthetic forecast-transfer regression test failed")
  }
  cat("SYNTHETIC SELF-TEST PASSED: stable relation benefited from cue;",
      "reversed relation penalized the frozen cue model.\n")
  invisible(TRUE)
}

if ("--self-test" %in% commandArgs(trailingOnly = TRUE)) {
  self_test()
} else {
  frozen_primary <- "analysis/movement_phenology/payoff_b_v8_primary.R"
  if (!file.exists(frozen_primary)) stop("Missing frozen V8 input mapping")
  source(frozen_primary, local = FALSE)

  # Original V8 pair support is frozen; no species-specific adaptive filtering.
  if (nrow(pairs) != 166L ||
      length(unique(incidence$species)) != 28L) {
    stop("Frozen V8 environmental unit counts drifted unexpectedly")
  }

  loc <- unique(cells[, c("cell", "cell_lat2", "cell_lng")])
  loc <- loc[!duplicated(loc$cell), , drop = FALSE]

  pair_results <- vector("list", nrow(pairs))
  annual_results <- vector("list", nrow(pairs))
  for (i in seq_len(nrow(pairs))) {
    p <- pairs[i, , drop = FALSE]
    d <- pair_greenup(p$source_cell, p$target_cell, green)
    fit <- forecast_pair(d)
    if (is.null(fit)) next
    loc_i <- match(p$target_cell, loc$cell)
    if (is.na(loc_i)) stop("Missing source-defined target location")
    if (!is.finite(loc$cell_lat2[loc_i]) || !is.finite(loc$cell_lng[loc_i])) {
      stop("Nonfinite spatial pair location")
    }
    row <- cbind(
      p[, c("pair_key", "source_cell", "target_cell",
            "rho_early", "rho_late", "delta_rho"), drop = FALSE],
      target_lat = loc$cell_lat2[loc_i],
      target_lng = loc$cell_lng[loc_i],
      fit$score
    )
    ar <- cbind(pair_key = p$pair_key, fit$annual)
    pair_results[[i]] <- row
    annual_results[[i]] <- ar
  }
  scores <- do.call(rbind, Filter(Negate(is.null), pair_results))
  annual <- do.call(rbind, Filter(Negate(is.null), annual_results))
  if (is.null(scores) || nrow(scores) < 100L ||
      is.null(annual) || any(!is.finite(scores$standardized_improvement))) {
    stop("Insufficient source/target support in fixed V8 pair panel")
  }

  # Paired improvement on the unchanged holdout period; no inspection of any
  # bird response. Positive means old origin cue adds transferable skill.
  pair_mean <- mean(scores$standardized_improvement)
  pair_median <- median(scores$standardized_improvement)
  fraction_better <- mean(scores$standardized_improvement > 0)
  # Unique environmental spatial-pair bootstrap is presented as descriptive
  # diagnostic only: nearby cells share weather, so it is not causal or
  # effective-independent-sample inference.
  set.seed(BOOT_SEED)
  bootstrap_means <- replicate(
    BOOT_REPS,
    mean(sample(scores$standardized_improvement,
                size = nrow(scores), replace = TRUE))
  )
  pair_ci <- as.numeric(quantile(bootstrap_means, c(.025, .975)))

  # Spatial block sensitivity: dependence-aware exploratory test. The block
  # widths were set before opening the new forecast-transfer endpoint.
  spatial_block <- function(df, degrees) {
    paste(floor((df$target_lat + 90) / degrees),
          floor((df$target_lng + 180) / degrees), sep = ":")
  }
  resample_block <- function(df, degrees) {
    keys <- spatial_block(df, degrees)
    members <- split(df$standardized_improvement, keys)
    nb <- length(members)
    if (nb < 5L) return(c(blocks = nb, low = NA, high = NA))
    out <- replicate(BOOT_REPS, {
      sample_blocks <- sample(seq_along(members), size = nb, replace = TRUE)
      mean(unlist(members[sample_blocks], use.names = FALSE))
    })
    q <- quantile(out, c(.025, .975), names = FALSE)
    c(blocks = nb, low = q[1], high = q[2])
  }
  block_5 <- resample_block(scores, 5)
  block_10 <- resample_block(scores, 10)

  # Shared calendar years are a second dependence source. Show all eight
  # holdout years individually without using the n_pairs*n_years count as
  # independent evidence.
  yrs <- sort(unique(annual$year))
  annual_summary <- do.call(rbind, lapply(yrs, function(year) {
    z <- annual[annual$year == year, , drop = FALSE]
    data.frame(
      holdout_year = year,
      pairs = nrow(z),
      mean_standardized_improvement = mean(z$standardized_improvement),
      median_standardized_improvement = median(z$standardized_improvement),
      fraction_pairs_better = mean(z$standardized_improvement > 0)
    )
  }))
  if (!identical(as.integer(annual_summary$holdout_year),
                 as.integer(LATE_YEARS))) {
    stop("Later-year coverage changed; cannot silently omit holdout years")
  }

  # A correlation-to-skill association is NOT an estimate of bird forecast
  # uptake, even if a numerical signal is observed.
  link_cor <- cor(scores$delta_rho, scores$standardized_improvement)
  aggregate <- data.frame(
    status = "POST_OUTCOME_EXPLORATORY_ENVIRONMENT_ONLY",
    train_period = "2002-2009",
    untouched_holdout_period = "2010-2017",
    ridge_penalty = RIDGE_PENALTY,
    original_v8_unique_pairs = nrow(pairs),
    evaluated_unique_pairs = nrow(scores),
    mean_scaled_score_improvement = pair_mean,
    median_scaled_score_improvement = pair_median,
    fraction_pairs_positive_improvement = fraction_better,
    pair_boot_ci_low = pair_ci[1],
    pair_boot_ci_high = pair_ci[2],
    spatial_5degree_nblocks = block_5["blocks"],
    spatial_5degree_ci_low = block_5["low"],
    spatial_5degree_ci_high = block_5["high"],
    spatial_10degree_nblocks = block_10["blocks"],
    spatial_10degree_ci_low = block_10["low"],
    spatial_10degree_ci_high = block_10["high"],
    corr_rho_gain_vs_holdout_forecast_gain = link_cor,
    n_holdout_years = nrow(annual_summary),
    holdout_years_positive = sum(annual_summary$mean_standardized_improvement > 0),
    declared_claim_ceiling = "ENVIRONMENTAL_FORECAST_CALIBRATION_ONLY_NOT_BIRD_INFORMATION_OR_FITNESS"
  )

  dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
  write.csv(scores,
    "outputs/payoff_b_v8_exploratory_forecast_transfer_pairs.csv",
    row.names = FALSE)
  write.csv(annual,
    "outputs/payoff_b_v8_exploratory_forecast_transfer_pair_years.csv",
    row.names = FALSE)
  write.csv(annual_summary,
    "outputs/payoff_b_v8_exploratory_forecast_transfer_years.csv",
    row.names = FALSE)
  write.csv(aggregate,
    "outputs/payoff_b_v8_exploratory_forecast_transfer_summary.csv",
    row.names = FALSE)

  cat("\nPAYOFF_B_V8_HISTORICAL_FORECAST_TRANSFER_EXPLORATORY\n")
  print(aggregate, width = 200)
  cat("HOLDOUT_YEAR_SUMMARY\n")
  print(annual_summary, row.names = FALSE)
  cat("NO BIRD BEHAVIOR OR FITNESS ESTIMATED\n")
}
