#!/usr/bin/env Rscript

# Post-result diagnostic ONLY. Outcome of the historical forecast-transfer
# audit was already opened before this diagnostic was written.
#
# Why: inverse early correlations among 44/166 pairs may be sample noise;
# a negative early fitted rho is NOT proof of a formerly useful inverse rule.
# This script reports historical leave-one-year-out forecast value and signed
# correlation stability, without accessing bird behavior or biological fitness.

options(stringsAsFactors = FALSE)

early_loyo_fold <- function(early, leave_idx, ridge_penalty = 1.0) {
  train <- early[-leave_idx, , drop = FALSE]
  test <- early[leave_idx, , drop = FALSE]
  if (nrow(train) < 6L || nrow(test) != 1L) return(NA_real_)
  year_mu <- mean(train$year)
  year_sd <- sd(train$year)
  src_mu <- mean(train$source_greenup)
  src_sd <- sd(train$source_greenup)
  tgt_sd <- sd(train$target_greenup)
  if (any(!is.finite(c(year_sd, src_sd, tgt_sd))) ||
      min(year_sd, src_sd, tgt_sd) < 1e-8) return(NA_real_)

  xe <- (train$year - year_mu) / year_sd
  xv <- (train$source_greenup - src_mu) / src_sd
  xo <- (test$year - year_mu) / year_sd
  xs <- (test$source_greenup - src_mu) / src_sd

  baseline_train <- cbind(intercept = 1, year = xe)
  cue_train <- cbind(intercept = 1, year = xe, origin = xv)
  baseline_test <- cbind(intercept = 1, year = xo)
  cue_test <- cbind(intercept = 1, year = xo, origin = xs)

  ridge <- function(X, y) {
    b <- solve(
      crossprod(X) +
        diag(c(0, rep(ridge_penalty, ncol(X)-1L)), nrow = ncol(X)),
      crossprod(X,y))
    as.numeric(b)
  }
  b0 <- ridge(baseline_train, train$target_greenup)
  b1 <- ridge(cue_train, train$target_greenup)
  pred0 <- as.numeric(baseline_test %*% b0)
  pred1 <- as.numeric(cue_test %*% b1)
  ((test$target_greenup - pred0)^2 -
    (test$target_greenup - pred1)^2) / (tgt_sd^2)
}

partial_early_correlation <- function(train) {
  if (nrow(train) < 6L) return(NA_real_)
  s <- residuals(lm(source_greenup ~ year, data = train))
  t <- residuals(lm(target_greenup ~ year, data = train))
  if (!is.finite(sd(s)) || !is.finite(sd(t)) ||
      sd(s) < 1e-12 || sd(t) < 1e-12) return(NA_real_)
  as.numeric(cor(s,t))
}

historical_validation <- function(paired) {
  early <- paired[paired$year %in% 2002:2009, , drop = FALSE]
  n <- nrow(early)
  if (n < 7L) {
    return(data.frame(
      historical_years = n,
      loyo_folds = 0L,
      early_loyo_mean = NA_real_,
      early_loyo_fraction_positive = NA_real_,
      early_sign_leaveone_fraction_negative = NA_real_,
      early_sign_leaveone_fraction_positive = NA_real_,
      early_sign_all_same_as_original = NA
    ))
  }
  fold <- vapply(seq_len(n),
    function(i) early_loyo_fold(early, i), numeric(1))
  rhos <- vapply(seq_len(n),
    function(i) partial_early_correlation(early[-i, , drop = FALSE]),
    numeric(1))
  if (any(!is.finite(fold)) || any(!is.finite(rhos))) {
    return(data.frame(
      historical_years = n, loyo_folds = 0L,
      early_loyo_mean = NA_real_,
      early_loyo_fraction_positive = NA_real_,
      early_sign_leaveone_fraction_negative = NA_real_,
      early_sign_leaveone_fraction_positive = NA_real_,
      early_sign_all_same_as_original = NA
    ))
  }
  reference <- partial_early_correlation(early)
  data.frame(
    historical_years = n,
    loyo_folds = n,
    early_loyo_mean = mean(fold),
    early_loyo_fraction_positive = mean(fold > 0),
    early_sign_leaveone_fraction_negative = mean(rhos < 0),
    early_sign_leaveone_fraction_positive = mean(rhos > 0),
    early_sign_all_same_as_original =
      all(sign(rhos) == sign(reference))
  )
}

synthetic_check <- function() {
  y <- 2002:2017
  x <- rep(c(-1, 0.8, -0.6, 1.1), 4L)
  d <- data.frame(year = y, source_greenup = x,
                  target_greenup = c(20-10*x[1:8],
                                     20+10*x[9:16]))
  v <- historical_validation(d)
  if (v$loyo_folds != 8 || v$early_loyo_mean <= 0 ||
      v$early_sign_leaveone_fraction_negative != 1) {
    stop("Negative early trained relationship fails self-check")
  }
  cat("HISTORICAL_LOYO_SYNTHETIC_TEST_PASSED\n")
}

if ("--self-test" %in% commandArgs(trailingOnly = TRUE)) {
  synthetic_check()
} else {
  source("analysis/movement_phenology/payoff_b_v8_historical_forecast_transfer_exploratory.R",
         local = FALSE)

  if (nrow(scores) != 166L || nrow(pairs) != 166L)
    stop("Prior environmental-only V8 result drifted from 166 pairs")
  out <- vector("list", nrow(scores))
  for (i in seq_len(nrow(scores))) {
    row <- scores[i, , drop = FALSE]
    src <- row$source_cell
    tgt <- row$target_cell
    paired <- pair_greenup(src, tgt, green)
    v <- historical_validation(paired)
    out[[i]] <- cbind(row[, c("pair_key","rho_early","rho_late","delta_rho",
                              "train_n","standardized_improvement")],
                      v)
  }
  panel <- do.call(rbind, out)
  panel$sign_class <- ifelse(panel$rho_early < 0 & panel$rho_late > 0,
                           "negative_to_positive",
                           ifelse(panel$rho_early > 0 & panel$rho_late > 0,
                                  "positive_to_positive",
                                  ifelse(panel$rho_early > 0 & panel$rho_late < 0,
                                         "positive_to_negative",
                                         "negative_to_negative")))
  valid <- panel[is.finite(panel$early_loyo_mean), , drop = FALSE]
  flip <- valid[valid$sign_class == "negative_to_positive", , drop = FALSE]
  sign_stable <- flip$early_sign_leaveone_fraction_negative >= 0.75
  old_useful <- flip$early_loyo_mean > 0
  late_harmful <- flip$standardized_improvement < 0

  summary <- data.frame(
    status = "POST_RESULT_EXPLORATORY_SIGN_STABILITY",
    total_fixed_pairs = nrow(panel),
    loyo_estimable_pairs = nrow(valid),
    loyo_not_estimable_pairs = nrow(panel) - nrow(valid),
    negative_to_positive_pairs_all = sum(panel$sign_class == "negative_to_positive"),
    negative_to_positive_pairs_loyo = nrow(flip),
    flip_pairs_early_loyo_positive = sum(old_useful),
    flip_pairs_early_negative_in_at_least_75_percent_of_loo = sum(sign_stable),
    flip_pairs_late_historical_cue_harmful = sum(late_harmful),
    flip_pairs_all_three = sum(old_useful & sign_stable & late_harmful),
    # This is a *screening count*. The LOO correlated folds are not
    # independent, and selection on apparent sign change biases the panel.
    scientific_claim = "NO_CONFIRMED_BEHAVIORAL_MEMORY_REVERSAL"
  )

  group_summary <- do.call(rbind, lapply(sort(unique(panel$sign_class)), function(group) {
    dd <- panel[panel$sign_class == group, , drop = FALSE]
    ll <- dd[is.finite(dd$early_loyo_mean), , drop = FALSE]
    data.frame(
      sign_class = group,
      total_pairs = nrow(dd),
      loyo_pairs = nrow(ll),
      old_loyo_fraction_positive = if(nrow(ll)>0) mean(ll$early_loyo_mean>0) else NA_real_,
      old_loyo_median_gain = if(nrow(ll)>0) median(ll$early_loyo_mean) else NA_real_,
      late_historical_gain_median = median(dd$standardized_improvement)
    )
  }))

  dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
  write.csv(panel,"outputs/payoff_b_v8_exploratory_early_loyo_pairs.csv",
            row.names = FALSE)
  write.csv(summary,"outputs/payoff_b_v8_exploratory_early_loyo_summary.csv",
            row.names = FALSE)
  write.csv(group_summary,"outputs/payoff_b_v8_exploratory_early_loyo_sign_groups.csv",
            row.names = FALSE)
  cat("\nPOST_RESULT_EARLY_RHO_SIGN_STABILITY_AUDIT\n")
  print(summary, width=200)
  cat("\nSIGN_GROUPS\n")
  print(group_summary, row.names=FALSE)
  cat("No cue uptake, learned policy, survival or reproductive outcome observed.\n")
}
