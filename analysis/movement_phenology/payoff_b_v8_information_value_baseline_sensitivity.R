#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC BASELINE SENSITIVITY.
# The primary metric-scale diagnostic defines source information value relative
# to a target-history linear-trend forecast. This script asks whether the same
# late-minus-early increase appears when the no-source baseline is instead a
# window-specific climatological mean and the source-informed model is built
# around mean anomalies rather than linear trends.

SOURCE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_metric_scale_diagnostic.R"
if (!file.exists(SOURCE_SCRIPT)) stop("Missing metric-scale diagnostic script")
source(SOURCE_SCRIPT, local = FALSE)

B <- 10000L
SEED <- 20261006L

clim_value <- function(source_cell, target_cell, start_year, end_year) {
  source <- green[
    green$cell == source_cell &
      green$year >= start_year &
      green$year <= end_year,
    c("year", "gr_mn"),
    drop = FALSE
  ]
  target <- green[
    green$cell == target_cell &
      green$year >= start_year &
      green$year <= end_year,
    c("year", "gr_mn"),
    drop = FALSE
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
    return(c(n = n, mse_null = NA_real_, mse_source = NA_real_, value = NA_real_))
  }

  err_null <- rep(NA_real_, n)
  err_source <- rep(NA_real_, n)

  for (j in seq_len(n)) {
    tr <- z[-j, , drop = FALSE]
    te <- z[j, , drop = FALSE]

    src_mu <- mean(tr$source_greenup)
    tgt_mu <- mean(tr$target_greenup)
    xtr <- tr$source_greenup - src_mu
    ytr <- tr$target_greenup - tgt_mu

    if (!is.finite(sd(xtr)) || sd(xtr) <= 0) next

    mod <- try(lm(ytr ~ xtr), silent = TRUE)
    if (inherits(mod, "try-error")) next

    xh <- te$source_greenup - src_mu
    pred_anom <- as.numeric(coef(mod)[1] + coef(mod)[2] * xh)
    if (!is.finite(pred_anom)) next

    pred_null <- tgt_mu
    pred_source <- tgt_mu + pred_anom

    err_null[j] <- te$target_greenup - pred_null
    err_source[j] <- te$target_greenup - pred_source
  }

  if (!all(is.finite(err_null)) || !all(is.finite(err_source))) {
    return(c(n = n, mse_null = NA_real_, mse_source = NA_real_, value = NA_real_))
  }

  mse_null <- mean(err_null^2)
  mse_source <- mean(err_source^2)

  c(
    n = n,
    mse_null = mse_null,
    mse_source = mse_source,
    value = mse_null - mse_source
  )
}

early <- t(mapply(
  clim_value,
  diag_pairs$source_cell,
  diag_pairs$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
))
late <- t(mapply(
  clim_value,
  diag_pairs$source_cell,
  diag_pairs$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
))

out <- diag_pairs[, c(
  "pair_key", "source_cell", "target_cell",
  "block5", "block10", "early_n_gate", "late_n_gate",
  "loo_value_mse_early", "loo_value_mse_late", "delta_loo_value_mse"
)]
out$clim_value_early <- as.numeric(early[, "value"])
out$clim_value_late <- as.numeric(late[, "value"])
out$delta_clim_value <- out$clim_value_late - out$clim_value_early
out$clim_null_mse_early <- as.numeric(early[, "mse_null"])
out$clim_null_mse_late <- as.numeric(late[, "mse_null"])
out$clim_source_mse_early <- as.numeric(early[, "mse_source"])
out$clim_source_mse_late <- as.numeric(late[, "mse_source"])

ok <- is.finite(out$clim_value_early) &
  is.finite(out$clim_value_late) &
  is.finite(out$delta_clim_value)

pair_ci <- pair_boot_mean(out$delta_clim_value[ok], B, SEED)
source_ci <- cluster_boot_mean(
  out[ok, ], "delta_clim_value", "source_cell", B, SEED + 1L
)
target_ci <- cluster_boot_mean(
  out[ok, ], "delta_clim_value", "target_cell", B, SEED + 2L
)
block5_ci <- cluster_boot_mean(
  out[ok, ], "delta_clim_value", "block5", B, SEED + 3L
)
block10_ci <- cluster_boot_mean(
  out[ok, ], "delta_clim_value", "block10", B, SEED + 4L
)

summary_row <- data.frame(
  baseline = "window_mean_climatology",
  n_pairs = sum(ok),
  early_mean_value = mean(out$clim_value_early[ok]),
  late_mean_value = mean(out$clim_value_late[ok]),
  delta_mean_value = mean(out$delta_clim_value[ok]),
  median_delta_value = median(out$delta_clim_value[ok]),
  trimmed10_delta_value = mean(out$delta_clim_value[ok], trim = 0.10),
  positive_pairs = sum(out$delta_clim_value[ok] > 0),
  negative_pairs = sum(out$delta_clim_value[ok] < 0),
  pair_ci_low_95 = pair_ci[1],
  pair_ci_high_95 = pair_ci[2],
  source_cluster_ci_low_95 = source_ci[1],
  source_cluster_ci_high_95 = source_ci[2],
  target_cluster_ci_low_95 = target_ci[1],
  target_cluster_ci_high_95 = target_ci[2],
  block5_ci_low_95 = block5_ci[1],
  block5_ci_high_95 = block5_ci[2],
  block10_ci_low_95 = block10_ci[1],
  block10_ci_high_95 = block10_ci[2],
  cor_delta_with_trend_baseline =
    cor(out$delta_clim_value[ok], out$delta_loo_value_mse[ok])
)

exact <- out[
  ok &
    out$early_n_gate == 8L &
    out$late_n_gate == 8L,
  ,
  drop = FALSE
]
exact_ci <- pair_boot_mean(exact$delta_clim_value, B, SEED + 10L)

exact_summary <- data.frame(
  n_pairs = nrow(exact),
  early_mean_value = mean(exact$clim_value_early),
  late_mean_value = mean(exact$clim_value_late),
  delta_mean_value = mean(exact$delta_clim_value),
  positive_pairs = sum(exact$delta_clim_value > 0),
  negative_pairs = sum(exact$delta_clim_value < 0),
  pair_ci_low_95 = exact_ci[1],
  pair_ci_high_95 = exact_ci[2]
)

inc <- merge(
  incidence,
  out[, c("pair_key", "clim_value_early", "clim_value_late", "delta_clim_value")],
  by = "pair_key",
  all = FALSE,
  sort = FALSE
)
sp <- aggregate(
  cbind(clim_value_early, clim_value_late, delta_clim_value) ~ species,
  data = inc,
  FUN = mean
)

pair_val <- setNames(out$delta_clim_value, out$pair_key)
inc_by_pair <- split(incidence$species, incidence$pair_key)
pair_keys <- out$pair_key[ok]

set.seed(SEED + 20L)
sp_boot <- rep(NA_real_, B)
for (b in seq_len(B)) {
  draw <- sample(pair_keys, length(pair_keys), replace = TRUE)
  lists <- list()
  for (pk in draw) {
    spp <- inc_by_pair[[pk]]
    val <- pair_val[[pk]]
    for (ss in spp) lists[[ss]] <- c(lists[[ss]], val)
  }
  spm <- vapply(lists, mean, numeric(1))
  sp_boot[b] <- mean(spm)
}
sp_ci <- as.numeric(quantile(sp_boot, c(0.025, 0.975), names = FALSE))

species_summary <- data.frame(
  n_species = nrow(sp),
  early_equal_species_mean = mean(sp$clim_value_early),
  late_equal_species_mean = mean(sp$clim_value_late),
  delta_equal_species_mean = mean(sp$delta_clim_value),
  positive_species = sum(sp$delta_clim_value > 0),
  negative_species = sum(sp$delta_clim_value < 0),
  ci_low_95 = sp_ci[1],
  ci_high_95 = sp_ci[2]
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(
  out,
  "outputs/payoff_b_v8_information_value_baseline_pairs.csv",
  row.names = FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_information_value_baseline_summary.csv",
  row.names = FALSE
)
write.csv(
  exact_summary,
  "outputs/payoff_b_v8_information_value_baseline_exact.csv",
  row.names = FALSE
)
write.csv(
  sp,
  "outputs/payoff_b_v8_information_value_baseline_species.csv",
  row.names = FALSE
)
write.csv(
  species_summary,
  "outputs/payoff_b_v8_information_value_baseline_species_summary.csv",
  row.names = FALSE
)

cat("\nPOSTHOC INFORMATION-VALUE BASELINE SENSITIVITY\n")
print(summary_row)
cat("\nExact-complete subset:\n")
print(exact_summary)
cat("\nEqual-species sensitivity:\n")
print(species_summary)
