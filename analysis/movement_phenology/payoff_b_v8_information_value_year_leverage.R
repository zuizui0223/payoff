#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

PRIMARY_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_primary.R"
if (!file.exists(PRIMARY_SCRIPT)) stop("Missing V8 primary script")
source(PRIMARY_SCRIPT, local = FALSE)

BOOT_B <- 10000L
SEED <- 20261006L

cv_value <- function(source_cell, target_cell, start_year, end_year, omit_year = NA_integer_) {
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

  if (is.finite(omit_year)) {
    z <- z[z$year != omit_year, , drop = FALSE]
  }

  n <- nrow(z)
  if (n < 6L) return(NA_real_)

  err_src <- rep(NA_real_, n)
  err_null <- rep(NA_real_, n)

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

    pred_src <- tgt_expected + anomaly_pred
    err_src[j] <- te$target_greenup - pred_src
    err_null[j] <- te$target_greenup - tgt_expected
  }

  if (!all(is.finite(err_src)) || !all(is.finite(err_null))) return(NA_real_)

  mean(err_null^2) - mean(err_src^2)
}

exact <- pairs[
  pairs$early_n == 8L &
    pairs$late_n == 8L,
  ,
  drop = FALSE
]

if (nrow(exact) != 58L) {
  stop("Expected 58 exact-complete pairs, found ", nrow(exact))
}

calc_delta <- function(omit_year = NA_integer_) {
  early_omit <- if (is.finite(omit_year) &&
                    omit_year >= EARLY_START && omit_year <= EARLY_END) {
    omit_year
  } else {
    NA_integer_
  }
  late_omit <- if (is.finite(omit_year) &&
                   omit_year >= LATE_START && omit_year <= LATE_END) {
    omit_year
  } else {
    NA_integer_
  }

  ge <- mapply(
    cv_value,
    exact$source_cell,
    exact$target_cell,
    MoreArgs = list(
      start_year = EARLY_START,
      end_year = EARLY_END,
      omit_year = early_omit
    )
  )
  gl <- mapply(
    cv_value,
    exact$source_cell,
    exact$target_cell,
    MoreArgs = list(
      start_year = LATE_START,
      end_year = LATE_END,
      omit_year = late_omit
    )
  )

  data.frame(
    pair_key = exact$pair_key,
    G_early = as.numeric(ge),
    G_late = as.numeric(gl),
    delta_G = as.numeric(gl - ge)
  )
}

pair_boot_ci <- function(x, B, seed) {
  x <- x[is.finite(x)]
  set.seed(seed)
  out <- replicate(B, mean(sample(x, length(x), replace = TRUE)))
  as.numeric(quantile(out, c(0.025, 0.975), names = FALSE))
}

base <- calc_delta()
base_ci <- pair_boot_ci(base$delta_G, BOOT_B, SEED)

rows <- list()
for (yr in EARLY_START:LATE_END) {
  z <- calc_delta(yr)
  ok <- is.finite(z$delta_G)
  ci <- pair_boot_ci(z$delta_G[ok], BOOT_B, SEED + yr)
  rows[[as.character(yr)]] <- data.frame(
    omitted_year = yr,
    n_pairs = sum(ok),
    mean_G_early = mean(z$G_early[ok]),
    mean_G_late = mean(z$G_late[ok]),
    mean_delta_G = mean(z$delta_G[ok]),
    median_delta_G = median(z$delta_G[ok]),
    positive_pair_fraction = mean(z$delta_G[ok] > 0),
    pair_ci_low_95 = ci[1],
    pair_ci_high_95 = ci[2]
  )
}

loo <- do.call(rbind, rows)

summary_row <- data.frame(
  n_exact_pairs = nrow(exact),
  baseline_mean_G_early = mean(base$G_early),
  baseline_mean_G_late = mean(base$G_late),
  baseline_mean_delta_G = mean(base$delta_G),
  baseline_pair_ci_low_95 = base_ci[1],
  baseline_pair_ci_high_95 = base_ci[2],
  year_omissions_positive = sum(loo$mean_delta_G > 0),
  year_omissions_ci_above_zero = sum(loo$pair_ci_low_95 > 0),
  minimum_omission_mean_delta_G = min(loo$mean_delta_G),
  maximum_omission_mean_delta_G = max(loo$mean_delta_G),
  minimum_omission_ci_low_95 = min(loo$pair_ci_low_95),
  bootstrap_replicates = BOOT_B,
  seed = SEED,
  status = "POSTHOC_YEAR_LEVERAGE_DIAGNOSTIC"
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(
  loo,
  "outputs/payoff_b_v8_information_value_year_leverage.csv",
  row.names = FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_information_value_year_leverage_summary.csv",
  row.names = FALSE
)

cat("\nPAYOFF-B V8 INFORMATION-VALUE YEAR LEVERAGE\n")
print(summary_row)
print(loo)
