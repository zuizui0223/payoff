#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

CONTRACT <- "docs/PAYOFF_B_V8_PREDICTIVE_CONNECTIVITY_DEGRADATION_CONTRACT_20261005.md"
GATE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_admission_gate.R"
BOOTSTRAP_REPLICATES <- 10000L
BOOTSTRAP_SEED <- 20261005L

if (!file.exists(CONTRACT)) stop("Missing frozen V8 contract: ", CONTRACT)
if (!file.exists(GATE_SCRIPT)) stop("Missing frozen V8 admission-gate script: ", GATE_SCRIPT)

# Reconstruct the exact frozen source-target mapping and gate state.
# This script deliberately computes no alternative mapping or threshold.
source(GATE_SCRIPT, local = FALSE)

if (!isTRUE(gate_pass)) {
  stop("Frozen V8 admission gate did not pass; primary outcome must remain unopened.")
}

pair_key <- function(source_cell, target_cell) {
  paste(as.character(source_cell), as.character(target_cell), sep = "__")
}

eligible$pair_id <- pair_key(eligible$source_cell, eligible$target_cell)

incidence <- unique(eligible[, c(
  "pair_id", "species", "source_cell", "target_cell", "source_target_distance_km"
)])
incidence <- incidence[order(incidence$pair_id, incidence$species), ]

unique_pairs <- unique(eligible[, c(
  "pair_id", "source_cell", "target_cell", "source_target_distance_km"
)])
unique_pairs <- unique_pairs[order(unique_pairs$pair_id), ]

detrended_rho <- function(source_cell, target_cell, start_year, end_year) {
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
  paired <- merge(source, target, by = "year", all = FALSE)
  paired <- paired[order(paired$year), ]

  if (nrow(paired) < MIN_PAIRS_PER_WINDOW) return(NA_real_)

  source_fit <- lm(source_greenup ~ year, data = paired)
  target_fit <- lm(target_greenup ~ year, data = paired)
  source_resid <- residuals(source_fit)
  target_resid <- residuals(target_fit)

  if (!all(is.finite(source_resid)) || !all(is.finite(target_resid))) return(NA_real_)
  if (sd(source_resid) <= .Machine$double.eps) return(NA_real_)
  if (sd(target_resid) <= .Machine$double.eps) return(NA_real_)

  suppressWarnings(cor(source_resid, target_resid, method = "pearson"))
}

unique_pairs$rho_early <- mapply(
  detrended_rho,
  unique_pairs$source_cell,
  unique_pairs$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
)
unique_pairs$rho_late <- mapply(
  detrended_rho,
  unique_pairs$source_cell,
  unique_pairs$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
)
unique_pairs$delta_rho <- unique_pairs$rho_late - unique_pairs$rho_early
unique_pairs$primary_estimable <- is.finite(unique_pairs$delta_rho)

pair_results <- unique_pairs[unique_pairs$primary_estimable, ]
if (nrow(pair_results) == 0) stop("No V8 spatial pairs produced estimable primary outcomes.")

incidence_estimable <- merge(
  incidence[, c("pair_id", "species")],
  pair_results[, c("pair_id", "delta_rho")],
  by = "pair_id",
  all = FALSE,
  sort = FALSE
)

species_results <- aggregate(
  delta_rho ~ species,
  data = incidence_estimable,
  FUN = mean
)
names(species_results)[2] <- "mean_delta_rho"
species_pair_n <- aggregate(
  pair_id ~ species,
  data = incidence_estimable,
  FUN = function(x) length(unique(x))
)
names(species_pair_n)[2] <- "estimable_unique_pairs"
species_results <- merge(species_results, species_pair_n, by = "species", all.x = TRUE)
species_results <- species_results[order(species_results$species), ]

pair_mean <- mean(pair_results$delta_rho)
species_mean <- mean(species_results$mean_delta_rho)

set.seed(BOOTSTRAP_SEED)
boot_pair_mean <- numeric(BOOTSTRAP_REPLICATES)
boot_species_mean <- numeric(BOOTSTRAP_REPLICATES)

pair_boot_base <- pair_results[, c("pair_id", "delta_rho")]
incidence_base <- unique(incidence_estimable[, c("pair_id", "species")])

for (b in seq_len(BOOTSTRAP_REPLICATES)) {
  draw_index <- sample.int(nrow(pair_boot_base), nrow(pair_boot_base), replace = TRUE)
  sampled <- pair_boot_base[draw_index, , drop = FALSE]
  sampled$draw_id <- seq_len(nrow(sampled))

  boot_pair_mean[b] <- mean(sampled$delta_rho)

  sampled_incidence <- merge(
    sampled,
    incidence_base,
    by = "pair_id",
    all.x = TRUE,
    sort = FALSE
  )
  sp <- aggregate(
    delta_rho ~ species,
    data = sampled_incidence,
    FUN = mean
  )
  boot_species_mean[b] <- mean(sp$delta_rho)
}

pair_ci <- unname(quantile(boot_pair_mean, probs = c(0.025, 0.975), na.rm = TRUE))
species_ci <- unname(quantile(boot_species_mean, probs = c(0.025, 0.975), na.rm = TRUE))

pair_support <- is.finite(pair_mean) && pair_mean < 0 && pair_ci[2] < 0
species_support <- is.finite(species_mean) && species_mean < 0 && species_ci[2] < 0
broad_support <- pair_support && species_support

species_negative_n <- sum(species_results$mean_delta_rho < 0, na.rm = TRUE)
species_total_n <- nrow(species_results)
species_negative_fraction <- species_negative_n / species_total_n
sign_reversal_n <- sum(
  pair_results$rho_early > 0 & pair_results$rho_late <= 0,
  na.rm = TRUE
)

summary_row <- data.frame(
  contract = CONTRACT,
  source_commit = SOURCE_COMMIT,
  early_window = paste0(EARLY_START, "-", EARLY_END),
  late_window = paste0(LATE_START, "-", LATE_END),
  admitted_species_by_pair_rows = nrow(eligible),
  admitted_unique_spatial_pairs = nrow(unique_pairs),
  primary_estimable_unique_spatial_pairs = nrow(pair_results),
  primary_estimable_species = species_total_n,
  pair_mean_delta_rho = pair_mean,
  pair_boot_ci_low = pair_ci[1],
  pair_boot_ci_high = pair_ci[2],
  equal_species_mean_delta_rho = species_mean,
  equal_species_boot_ci_low = species_ci[1],
  equal_species_boot_ci_high = species_ci[2],
  species_negative_n = species_negative_n,
  species_total_n = species_total_n,
  species_negative_fraction = species_negative_fraction,
  positive_to_nonpositive_sign_reversals = sign_reversal_n,
  bootstrap_unit = "UNIQUE_SPATIAL_PAIR",
  bootstrap_replicates = BOOTSTRAP_REPLICATES,
  bootstrap_seed = BOOTSTRAP_SEED,
  pair_support = pair_support,
  equal_species_support = species_support,
  V8_BROAD_DEGRADATION = ifelse(
    broad_support,
    "SUPPORTED",
    "NOT_SUPPORTED"
  )
)

boot_out <- data.frame(
  replicate = seq_len(BOOTSTRAP_REPLICATES),
  pair_mean_delta_rho = boot_pair_mean,
  equal_species_mean_delta_rho = boot_species_mean
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(
  unique_pairs,
  "outputs/payoff_b_v8_primary_spatial_pairs_all.csv",
  row.names = FALSE
)
write.csv(
  pair_results,
  "outputs/payoff_b_v8_primary_spatial_pairs_estimable.csv",
  row.names = FALSE
)
write.csv(
  incidence,
  "outputs/payoff_b_v8_primary_species_pair_incidence.csv",
  row.names = FALSE
)
write.csv(
  species_results,
  "outputs/payoff_b_v8_primary_species_summary.csv",
  row.names = FALSE
)
write.csv(
  boot_out,
  "outputs/payoff_b_v8_primary_bootstrap.csv",
  row.names = FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_primary_summary.csv",
  row.names = FALSE
)

cat("\nPAYOFF-B V8 PRIMARY ENVIRONMENTAL RESULT\n")
print(summary_row)
cat("\nPrimary support rule: both the unique-pair and equal-species means must be negative and both 95% dependency-aware bootstrap intervals must exclude zero.\n")
cat("No mandatory sensitivity and no bird mismatch consequence analysis was run in this script.\n")
