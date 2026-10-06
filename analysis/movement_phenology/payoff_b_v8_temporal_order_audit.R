#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

PRIMARY_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_primary.R"
if (!file.exists(PRIMARY_SCRIPT)) stop("Missing V8 primary script")
source(PRIMARY_SCRIPT, local = FALSE)

BOOT_B <- 10000L
SEED <- 20261006L

pair_lead <- function(source_cell, target_cell, start_year, end_year) {
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
  if (nrow(z) == 0) {
    return(c(
      n = 0,
      mean_lead_days = NA_real_,
      median_lead_days = NA_real_,
      fraction_source_earlier = NA_real_,
      min_lead_days = NA_real_,
      max_lead_days = NA_real_
    ))
  }

  # Positive lead means source green-up occurs earlier than target green-up.
  lead <- z$target_greenup - z$source_greenup
  c(
    n = length(lead),
    mean_lead_days = mean(lead),
    median_lead_days = median(lead),
    fraction_source_earlier = mean(lead > 0),
    min_lead_days = min(lead),
    max_lead_days = max(lead)
  )
}

early <- t(mapply(
  pair_lead,
  pairs$source_cell,
  pairs$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
))
late <- t(mapply(
  pair_lead,
  pairs$source_cell,
  pairs$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
))

out <- pairs[, c(
  "pair_key", "source_cell", "target_cell", "source_target_distance_km"
)]
for (m in c(
  "n", "mean_lead_days", "median_lead_days",
  "fraction_source_earlier", "min_lead_days", "max_lead_days"
)) {
  out[[paste0(m, "_early")]] <- as.numeric(early[, m])
  out[[paste0(m, "_late")]] <- as.numeric(late[, m])
}

out$mean_lead_all <- rowMeans(
  out[, c("mean_lead_days_early", "mean_lead_days_late")],
  na.rm = TRUE
)
out$source_earlier_both_window_means <-
  out$mean_lead_days_early > 0 & out$mean_lead_days_late > 0
out$source_earlier_majority_both <-
  out$fraction_source_earlier_early > 0.5 &
  out$fraction_source_earlier_late > 0.5
out$source_earlier_all_observed_years <-
  out$min_lead_days_early > 0 & out$min_lead_days_late > 0

# Coordinates / blocks for dependence-aware uncertainty.
coord <- unique(cells[, c("cell", "cell_lat2", "cell_lng")])
coord <- coord[
  is.finite(coord$cell) &
    is.finite(coord$cell_lat2) &
    is.finite(coord$cell_lng),
  ,
  drop = FALSE
]
coord <- coord[!duplicated(coord$cell), , drop = FALSE]
src <- coord
names(src) <- c("source_cell", "source_lat", "source_lng")
tgt <- coord
names(tgt) <- c("target_cell", "target_lat", "target_lng")
out <- merge(out, src, by = "source_cell", all.x = TRUE)
out <- merge(out, tgt, by = "target_cell", all.x = TRUE)
out$mid_lat <- (out$source_lat + out$target_lat) / 2
out$mid_lng <- (out$source_lng + out$target_lng) / 2
out$block5 <- paste(
  floor((out$mid_lat + 90) / 5),
  floor((out$mid_lng + 180) / 5),
  sep = "_"
)
out$block10 <- paste(
  floor((out$mid_lat + 90) / 10),
  floor((out$mid_lng + 180) / 10),
  sep = "_"
)

cluster_boot_mean <- function(df, value_col, cluster_col, B, seed) {
  keep <- is.finite(df[[value_col]]) & !is.na(df[[cluster_col]])
  dd <- df[keep, , drop = FALSE]
  cluster_id <- as.character(dd[[cluster_col]])
  clusters <- unique(cluster_id)
  by_cluster <- split(dd[[value_col]], cluster_id)
  set.seed(seed)
  vals <- rep(NA_real_, B)
  for (b in seq_len(B)) {
    draw <- sample(clusters, length(clusters), replace = TRUE)
    vals[b] <- mean(unlist(by_cluster[draw], use.names = FALSE))
  }
  as.numeric(quantile(vals, c(0.025, 0.975), names = FALSE))
}

pair_boot <- function(x, B, seed) {
  x <- x[is.finite(x)]
  set.seed(seed)
  vals <- replicate(B, mean(sample(x, length(x), replace = TRUE)))
  as.numeric(quantile(vals, c(0.025, 0.975), names = FALSE))
}

summary_window <- function(df, suffix, seed_offset) {
  lead_col <- paste0("mean_lead_days_", suffix)
  frac_col <- paste0("fraction_source_earlier_", suffix)
  ok <- is.finite(df[[lead_col]]) & is.finite(df[[frac_col]])
  dd <- df[ok, , drop = FALSE]

  pci <- pair_boot(dd[[lead_col]], BOOT_B, SEED + seed_offset)
  sci <- cluster_boot_mean(
    dd, lead_col, "source_cell", BOOT_B, SEED + seed_offset + 1L
  )
  tci <- cluster_boot_mean(
    dd, lead_col, "target_cell", BOOT_B, SEED + seed_offset + 2L
  )
  b5 <- cluster_boot_mean(
    dd, lead_col, "block5", BOOT_B, SEED + seed_offset + 3L
  )
  b10 <- cluster_boot_mean(
    dd, lead_col, "block10", BOOT_B, SEED + seed_offset + 4L
  )

  data.frame(
    window = suffix,
    n_pairs = nrow(dd),
    pair_mean_lead_days = mean(dd[[lead_col]]),
    pair_median_lead_days = median(dd[[lead_col]]),
    pair_mean_fraction_source_earlier = mean(dd[[frac_col]]),
    pair_fraction_positive_mean_lead = mean(dd[[lead_col]] > 0),
    pair_fraction_majority_years_source_earlier = mean(dd[[frac_col]] > 0.5),
    pair_ci_low_95 = pci[1],
    pair_ci_high_95 = pci[2],
    source_cluster_ci_low_95 = sci[1],
    source_cluster_ci_high_95 = sci[2],
    target_cluster_ci_low_95 = tci[1],
    target_cluster_ci_high_95 = tci[2],
    block5_ci_low_95 = b5[1],
    block5_ci_high_95 = b5[2],
    block10_ci_low_95 = b10[1],
    block10_ci_high_95 = b10[2]
  )
}

window_summary <- rbind(
  summary_window(out, "early", 10L),
  summary_window(out, "late", 20L)
)

joint_summary <- data.frame(
  n_pairs = nrow(out),
  mean_lead_all_pair_mean = mean(out$mean_lead_all, na.rm = TRUE),
  positive_mean_lead_both_windows =
    sum(out$source_earlier_both_window_means, na.rm = TRUE),
  majority_source_earlier_both_windows =
    sum(out$source_earlier_majority_both, na.rm = TRUE),
  source_earlier_all_observed_years =
    sum(out$source_earlier_all_observed_years, na.rm = TRUE),
  fraction_positive_mean_lead_both_windows =
    mean(out$source_earlier_both_window_means, na.rm = TRUE),
  fraction_majority_source_earlier_both_windows =
    mean(out$source_earlier_majority_both, na.rm = TRUE),
  fraction_source_earlier_all_observed_years =
    mean(out$source_earlier_all_observed_years, na.rm = TRUE),
  status = "POSTHOC_TEMPORAL_ORDER_AUDIT"
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(
  out,
  "outputs/payoff_b_v8_temporal_order_pairs.csv",
  row.names = FALSE
)
write.csv(
  window_summary,
  "outputs/payoff_b_v8_temporal_order_window_summary.csv",
  row.names = FALSE
)
write.csv(
  joint_summary,
  "outputs/payoff_b_v8_temporal_order_joint_summary.csv",
  row.names = FALSE
)

cat("\nPAYOFF-B V8 TEMPORAL ORDER AUDIT\n")
print(window_summary)
print(joint_summary)
