#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

PRIMARY_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_primary.R"
LOCK_DOC <- "docs/PAYOFF_B_V8_MANDATORY_SENSITIVITY_IMPLEMENTATION_LOCK_20261005.md"
if (!file.exists(PRIMARY_SCRIPT)) stop("Missing frozen V8 primary script")
if (!file.exists(LOCK_DOC)) stop("Missing V8 sensitivity implementation lock")

# Reconstruct the exact primary objects and result under the already-opened,
# frozen V8 implementation. The mandatory sensitivities below do not use bird
# timing, mismatch, speed, or fitness outcomes.
source(PRIMARY_SCRIPT, local = FALSE)

SENS_B <- 10000L
SENS_SEED <- 20261005L

metric_summary <- function(pair_df, metric_col, incidence_df, B = SENS_B, seed = SENS_SEED) {
  x <- pair_df[, c("pair_key", metric_col), drop = FALSE]
  names(x)[2] <- "metric"
  x <- x[is.finite(x$metric), , drop = FALSE]
  inc <- unique(incidence_df[, c("species", "pair_key"), drop = FALSE])
  inc <- inc[inc$pair_key %in% x$pair_key, , drop = FALSE]

  pair_mean <- mean(x$metric)
  spdat <- merge(inc, x, by = "pair_key", all = FALSE, sort = FALSE)
  spmeans <- aggregate(metric ~ species, data = spdat, FUN = mean)
  species_mean <- mean(spmeans$metric)

  pair_vals <- setNames(x$metric, x$pair_key)
  inc_by_pair <- split(inc$species, inc$pair_key)
  keys <- x$pair_key
  P <- length(keys)

  set.seed(seed)
  bp <- numeric(B)
  bs <- numeric(B)

  for (b in seq_len(B)) {
    sampled_keys <- sample(keys, size = P, replace = TRUE)
    bp[b] <- mean(pair_vals[sampled_keys])

    species_lists <- list()
    for (k in sampled_keys) {
      spp <- inc_by_pair[[k]]
      if (is.null(spp)) next
      val <- pair_vals[[k]]
      for (sp in spp) {
        species_lists[[sp]] <- c(species_lists[[sp]], val)
      }
    }
    spm <- vapply(species_lists, mean, numeric(1))
    bs[b] <- mean(spm)
  }

  list(
    n_pairs = nrow(x),
    n_species = nrow(spmeans),
    pair_mean = pair_mean,
    pair_ci = as.numeric(quantile(bp, c(0.025, 0.975), names = FALSE, na.rm = TRUE)),
    species_mean = species_mean,
    species_ci = as.numeric(quantile(bs, c(0.025, 0.975), names = FALSE, na.rm = TRUE)),
    species_means = spmeans,
    pair_boot = bp,
    species_boot = bs
  )
}

# S1: Fisher-z change.
clamp_rho <- function(x) pmax(-0.999, pmin(0.999, x))
s1_pairs <- pairs
s1_pairs$delta_z <- atanh(clamp_rho(s1_pairs$rho_late)) -
  atanh(clamp_rho(s1_pairs$rho_early))
s1 <- metric_summary(s1_pairs, "delta_z", incidence)

# S2: exact-complete 8-year windows.
s2_pairs <- pairs[pairs$early_n == 8L & pairs$late_n == 8L, , drop = FALSE]
s2_inc <- incidence[incidence$pair_key %in% s2_pairs$pair_key, , drop = FALSE]
s2 <- metric_summary(s2_pairs, "delta_rho", s2_inc)

# S3: target-cell equal weighting within species.
target_inc <- unique(merge(
  eligible_map[, c("species", "target_cell", "pair_key")],
  pairs[, c("pair_key", "delta_rho")],
  by = "pair_key",
  all = FALSE,
  sort = FALSE
))
target_cell_means <- aggregate(
  delta_rho ~ species + target_cell,
  data = target_inc,
  FUN = mean
)
target_species_means <- aggregate(
  delta_rho ~ species,
  data = target_cell_means,
  FUN = mean
)
s3_point <- mean(target_species_means$delta_rho)

# The frozen mapping is one source per species-target cell, so S3 has the same
# dependency-aware pair bootstrap as the primary equal-species exposure summary.
s3_ci <- species_ci
s3_identical_to_primary <- isTRUE(all.equal(
  s3_point,
  equal_species_mean,
  tolerance = 1e-12
))

# S4: geographic-distance moderator.
s4_pairs <- pairs[
  is.finite(pairs$source_target_distance_km) &
    pairs$source_target_distance_km >= 0,
  ,
  drop = FALSE
]
s4_pairs$z_log_distance <- as.numeric(scale(log1p(s4_pairs$source_target_distance_km)))
s4_fit <- lm(delta_rho ~ z_log_distance, data = s4_pairs)
s4_slope <- unname(coef(s4_fit)["z_log_distance"])
set.seed(SENS_SEED)
s4_boot <- numeric(SENS_B)
for (b in seq_len(SENS_B)) {
  ii <- sample.int(nrow(s4_pairs), nrow(s4_pairs), replace = TRUE)
  fit_b <- try(lm(delta_rho ~ z_log_distance, data = s4_pairs[ii, , drop = FALSE]), silent = TRUE)
  s4_boot[b] <- if (inherits(fit_b, "try-error")) NA_real_ else unname(coef(fit_b)["z_log_distance"])
}
s4_ci <- as.numeric(quantile(s4_boot, c(0.025, 0.975), names = FALSE, na.rm = TRUE))

# S5: migration-distance class from the same frozen Amaral source commit.
STOP_URL <- paste0(
  "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
  SOURCE_COMMIT,
  "/data/stopover_percent.csv"
)
stop_cache <- "outputs/amaral_stopover_percent_frozen.csv"
if (!file.exists(stop_cache)) {
  download.file(STOP_URL, stop_cache, mode = "wb", quiet = FALSE)
}
stop <- read.csv(stop_cache, check.names = FALSE, stringsAsFactors = FALSE)
required_stop <- c("Species name", "Migration distance (km)")
missing_stop <- setdiff(required_stop, names(stop))
if (length(missing_stop) > 0) {
  stop("Missing stopover source columns: ", paste(missing_stop, collapse = ", "))
}
dist_tab <- unique(stop[, required_stop])
names(dist_tab) <- c("species_name", "migration_distance_km")
dist_tab$species <- gsub(" ", "_", trimws(dist_tab$species_name), fixed = TRUE)
dist_tab$migration_distance_km <- as.numeric(dist_tab$migration_distance_km)
dist_tab <- dist_tab[is.finite(dist_tab$migration_distance_km), , drop = FALSE]
source_distance_median <- median(dist_tab$migration_distance_km)
dist_tab$distance_class <- ifelse(
  dist_tab$migration_distance_km <= source_distance_median,
  "SHORT",
  "LONG"
)
dist_tab <- unique(dist_tab[, c("species", "migration_distance_km", "distance_class")])

primary_sp <- merge(
  species_means,
  dist_tab,
  by = "species",
  all.x = TRUE,
  sort = FALSE
)
s5_available <- primary_sp[!is.na(primary_sp$distance_class), , drop = FALSE]
class_point <- aggregate(delta_rho ~ distance_class, data = s5_available, FUN = mean)
short_mean <- class_point$delta_rho[class_point$distance_class == "SHORT"]
long_mean <- class_point$delta_rho[class_point$distance_class == "LONG"]
s5_contrast <- if (length(short_mean) == 1 && length(long_mean) == 1) {
  long_mean - short_mean
} else {
  NA_real_
}

pair_vals <- setNames(pairs$delta_rho, pairs$pair_key)
inc_class <- merge(
  incidence,
  dist_tab[, c("species", "distance_class")],
  by = "species",
  all = FALSE,
  sort = FALSE
)
inc_class_by_pair <- split(
  inc_class[, c("species", "distance_class"), drop = FALSE],
  inc_class$pair_key
)
set.seed(SENS_SEED)
s5_boot <- rep(NA_real_, SENS_B)
for (b in seq_len(SENS_B)) {
  sampled_keys <- sample(pairs$pair_key, nrow(pairs), replace = TRUE)
  rows <- vector("list", length(sampled_keys))
  rr <- 0L
  for (k in sampled_keys) {
    z <- inc_class_by_pair[[k]]
    if (is.null(z) || nrow(z) == 0) next
    rr <- rr + 1L
    z$delta_rho <- pair_vals[[k]]
    z$draw <- rr
    rows[[rr]] <- z
  }
  if (rr == 0L) next
  bd <- do.call(rbind, rows[seq_len(rr)])
  spm <- aggregate(delta_rho ~ species + distance_class, data = bd, FUN = mean)
  cm <- aggregate(delta_rho ~ distance_class, data = spm, FUN = mean)
  sm <- cm$delta_rho[cm$distance_class == "SHORT"]
  lm_ <- cm$delta_rho[cm$distance_class == "LONG"]
  if (length(sm) == 1 && length(lm_) == 1) s5_boot[b] <- lm_ - sm
}
s5_ci <- as.numeric(quantile(s5_boot, c(0.025, 0.975), names = FALSE, na.rm = TRUE))

# S6: leave-one-species-out, retaining a pair if another species still uses it.
loo_species <- sort(unique(incidence$species))
loo <- data.frame(
  omitted_species = loo_species,
  remaining_unique_pairs = NA_integer_,
  pair_mean_delta_rho = NA_real_,
  equal_species_mean_delta_rho = NA_real_
)
for (i in seq_along(loo_species)) {
  sp <- loo_species[i]
  inc2 <- incidence[incidence$species != sp, , drop = FALSE]
  keys2 <- unique(inc2$pair_key)
  p2 <- pairs[pairs$pair_key %in% keys2, , drop = FALSE]
  sd2 <- merge(
    inc2,
    p2[, c("pair_key", "delta_rho")],
    by = "pair_key",
    all = FALSE,
    sort = FALSE
  )
  sm2 <- aggregate(delta_rho ~ species, data = sd2, FUN = mean)
  loo$remaining_unique_pairs[i] <- nrow(p2)
  loo$pair_mean_delta_rho[i] <- mean(p2$delta_rho)
  loo$equal_species_mean_delta_rho[i] <- mean(sm2$delta_rho)
}

# S7: raw undetrended negative-control coordinate.
raw_rho <- function(source_cell, target_cell, start_year, end_year, green) {
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
  paired <- paired[
    is.finite(paired$year) &
      is.finite(paired$source_greenup) &
      is.finite(paired$target_greenup),
    ,
    drop = FALSE
  ]
  paired <- paired[!duplicated(paired$year), , drop = FALSE]
  if (nrow(paired) < MIN_PAIRS_PER_WINDOW) return(NA_real_)
  if (sd(paired$source_greenup) <= 0 || sd(paired$target_greenup) <= 0) return(NA_real_)
  cor(paired$source_greenup, paired$target_greenup, method = "pearson")
}
s7_pairs <- pairs
s7_pairs$rho_raw_early <- mapply(
  raw_rho,
  s7_pairs$source_cell,
  s7_pairs$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END, green = green)
)
s7_pairs$rho_raw_late <- mapply(
  raw_rho,
  s7_pairs$source_cell,
  s7_pairs$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END, green = green)
)
s7_pairs$delta_rho_raw <- s7_pairs$rho_raw_late - s7_pairs$rho_raw_early
s7 <- metric_summary(s7_pairs, "delta_rho_raw", incidence)

# S8: alternative 7-year non-overlapping windows, independently applying >=6.
ALT_EARLY_START <- 2002L
ALT_EARLY_END <- 2008L
ALT_LATE_START <- 2011L
ALT_LATE_END <- 2017L

alt_map <- mapping
alt_map$early_n_alt <- mapply(
  window_count,
  alt_map$source_cell,
  alt_map$target_cell,
  MoreArgs = list(start_year = ALT_EARLY_START, end_year = ALT_EARLY_END)
)
alt_map$late_n_alt <- mapply(
  window_count,
  alt_map$source_cell,
  alt_map$target_cell,
  MoreArgs = list(start_year = ALT_LATE_START, end_year = ALT_LATE_END)
)
alt_map <- alt_map[
  alt_map$early_n_alt >= MIN_PAIRS_PER_WINDOW &
    alt_map$late_n_alt >= MIN_PAIRS_PER_WINDOW,
  ,
  drop = FALSE
]
alt_map$pair_key <- paste(alt_map$source_cell, alt_map$target_cell, sep = "->")
alt_pair_seed <- unique(alt_map[, c(
  "pair_key", "source_cell", "target_cell", "source_target_distance_km"
)])
alt_pair_seed <- alt_pair_seed[order(alt_pair_seed$source_cell, alt_pair_seed$target_cell), ]

alt_early <- t(mapply(
  detrended_rho,
  alt_pair_seed$source_cell,
  alt_pair_seed$target_cell,
  MoreArgs = list(
    start_year = ALT_EARLY_START,
    end_year = ALT_EARLY_END,
    green = green
  )
))
alt_late <- t(mapply(
  detrended_rho,
  alt_pair_seed$source_cell,
  alt_pair_seed$target_cell,
  MoreArgs = list(
    start_year = ALT_LATE_START,
    end_year = ALT_LATE_END,
    green = green
  )
))
alt_pair_seed$rho_early_alt <- as.numeric(alt_early[, "rho"])
alt_pair_seed$rho_late_alt <- as.numeric(alt_late[, "rho"])
alt_pair_seed$delta_rho_alt <- alt_pair_seed$rho_late_alt - alt_pair_seed$rho_early_alt
s8_pairs <- alt_pair_seed[is.finite(alt_pair_seed$delta_rho_alt), , drop = FALSE]
s8_inc <- unique(alt_map[, c("species", "pair_key")])
s8_inc <- s8_inc[s8_inc$pair_key %in% s8_pairs$pair_key, , drop = FALSE]
s8 <- metric_summary(s8_pairs, "delta_rho_alt", s8_inc)

# Prespecified descriptive sign reversal.
sign_reversal_n <- sum(pairs$rho_early > 0 & pairs$rho_late <= 0, na.rm = TRUE)
sign_reversal_fraction <- sign_reversal_n / nrow(pairs)

summary_rows <- rbind(
  data.frame(
    sensitivity = "S1_FISHER_Z",
    n_pairs = s1$n_pairs,
    n_species = s1$n_species,
    estimate = s1$pair_mean,
    ci_low_95 = s1$pair_ci[1],
    ci_high_95 = s1$pair_ci[2],
    secondary_estimate = s1$species_mean,
    secondary_ci_low_95 = s1$species_ci[1],
    secondary_ci_high_95 = s1$species_ci[2],
    note = "estimate=unique-pair mean delta-z; secondary=equal-species mean"
  ),
  data.frame(
    sensitivity = "S2_EXACT_COMPLETE_8Y",
    n_pairs = s2$n_pairs,
    n_species = s2$n_species,
    estimate = s2$pair_mean,
    ci_low_95 = s2$pair_ci[1],
    ci_high_95 = s2$pair_ci[2],
    secondary_estimate = s2$species_mean,
    secondary_ci_low_95 = s2$species_ci[1],
    secondary_ci_high_95 = s2$species_ci[2],
    note = "delta-rho among pairs with 8/8 years in both primary windows"
  ),
  data.frame(
    sensitivity = "S3_TARGET_CELL_EQUAL_SPECIES",
    n_pairs = nrow(pairs),
    n_species = nrow(target_species_means),
    estimate = s3_point,
    ci_low_95 = s3_ci[1],
    ci_high_95 = s3_ci[2],
    secondary_estimate = as.numeric(s3_identical_to_primary),
    secondary_ci_low_95 = NA_real_,
    secondary_ci_high_95 = NA_real_,
    note = "estimate=target-cell equal-weighted species mean; secondary=1 if numerically identical to primary equal-species mean"
  ),
  data.frame(
    sensitivity = "S4_LOG_DISTANCE_MODERATOR",
    n_pairs = nrow(s4_pairs),
    n_species = length(unique(incidence$species)),
    estimate = s4_slope,
    ci_low_95 = s4_ci[1],
    ci_high_95 = s4_ci[2],
    secondary_estimate = NA_real_,
    secondary_ci_low_95 = NA_real_,
    secondary_ci_high_95 = NA_real_,
    note = "slope of delta-rho on z(log1p(source-target km))"
  ),
  data.frame(
    sensitivity = "S5_MIGRATION_DISTANCE_CLASS",
    n_pairs = nrow(pairs),
    n_species = nrow(s5_available),
    estimate = s5_contrast,
    ci_low_95 = s5_ci[1],
    ci_high_95 = s5_ci[2],
    secondary_estimate = source_distance_median,
    secondary_ci_low_95 = sum(s5_available$distance_class == "SHORT"),
    secondary_ci_high_95 = sum(s5_available$distance_class == "LONG"),
    note = "estimate=equal-species LONG-minus-SHORT delta-rho; secondary=source-table median km; secondary CI fields store SHORT/LONG species counts"
  ),
  data.frame(
    sensitivity = "S6_LOO_SPECIES",
    n_pairs = nrow(pairs),
    n_species = length(loo_species),
    estimate = min(loo$pair_mean_delta_rho),
    ci_low_95 = max(loo$pair_mean_delta_rho),
    ci_high_95 = sum(loo$pair_mean_delta_rho > 0),
    secondary_estimate = min(loo$equal_species_mean_delta_rho),
    secondary_ci_low_95 = max(loo$equal_species_mean_delta_rho),
    secondary_ci_high_95 = sum(loo$equal_species_mean_delta_rho > 0),
    note = "estimate/min + ci_low/max + ci_high/count positive for pair means; secondary fields analogous for equal-species means"
  ),
  data.frame(
    sensitivity = "S7_RAW_UNDETRENDED",
    n_pairs = s7$n_pairs,
    n_species = s7$n_species,
    estimate = s7$pair_mean,
    ci_low_95 = s7$pair_ci[1],
    ci_high_95 = s7$pair_ci[2],
    secondary_estimate = s7$species_mean,
    secondary_ci_low_95 = s7$species_ci[1],
    secondary_ci_high_95 = s7$species_ci[2],
    note = "negative-control delta raw correlation"
  ),
  data.frame(
    sensitivity = "S8_ALT_7Y_WINDOWS",
    n_pairs = s8$n_pairs,
    n_species = s8$n_species,
    estimate = s8$pair_mean,
    ci_low_95 = s8$pair_ci[1],
    ci_high_95 = s8$pair_ci[2],
    secondary_estimate = s8$species_mean,
    secondary_ci_low_95 = s8$species_ci[1],
    secondary_ci_high_95 = s8$species_ci[2],
    note = "2002-2008 versus 2011-2017, >=6 paired years"
  ),
  data.frame(
    sensitivity = "SIGN_REVERSAL_DESCRIPTIVE",
    n_pairs = nrow(pairs),
    n_species = length(unique(incidence$species)),
    estimate = sign_reversal_n,
    ci_low_95 = sign_reversal_fraction,
    ci_high_95 = NA_real_,
    secondary_estimate = NA_real_,
    secondary_ci_low_95 = NA_real_,
    secondary_ci_high_95 = NA_real_,
    note = "estimate=count early rho>0 to late rho<=0; ci_low field=fraction"
  )
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(summary_rows, "outputs/payoff_b_v8_mandatory_sensitivity_summary.csv", row.names = FALSE)
write.csv(s1_pairs, "outputs/payoff_b_v8_s1_fisher_z_pairs.csv", row.names = FALSE)
write.csv(s2_pairs, "outputs/payoff_b_v8_s2_complete_pairs.csv", row.names = FALSE)
write.csv(target_species_means, "outputs/payoff_b_v8_s3_target_species_means.csv", row.names = FALSE)
write.csv(s4_pairs, "outputs/payoff_b_v8_s4_distance_pairs.csv", row.names = FALSE)
write.csv(primary_sp, "outputs/payoff_b_v8_s5_migration_distance_species.csv", row.names = FALSE)
write.csv(loo, "outputs/payoff_b_v8_s6_loo_species.csv", row.names = FALSE)
write.csv(s7_pairs, "outputs/payoff_b_v8_s7_raw_pairs.csv", row.names = FALSE)
write.csv(s8_pairs, "outputs/payoff_b_v8_s8_alt7_pairs.csv", row.names = FALSE)

cat("\nPAYOFF-B V8 MANDATORY SENSITIVITIES\n")
print(summary_rows, row.names = FALSE)
cat("\nS5 source migration-distance median (km): ", source_distance_median, "\n", sep = "")
cat("S5 V8 species with distance: ", nrow(s5_available), "/", nrow(primary_sp), "\n", sep = "")
cat("Primary sign reversals + to <=0: ", sign_reversal_n, "/", nrow(pairs), "\n", sep = "")
cat("No bird timing, mismatch, speed, or fitness outcome was analyzed.\n")
