#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

PRIMARY_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_downstream_transfer_primary.R"
AUDIT_CONTRACT <- "docs/PAYOFF_B_V8_TRANSFER_STRUCTURAL_NULL_CONTRACT_20261005.md"

if (!file.exists(PRIMARY_SCRIPT)) stop("Missing frozen downstream transfer primary script")
if (!file.exists(AUDIT_CONTRACT)) stop("Missing frozen structural-null audit contract")

source(PRIMARY_SCRIPT, local = FALSE)

B <- 10000L
SEED <- 20261005L
PERM_B <- 2000L
PERM_SEED <- 20261005L

# Attach already-opened early/late environmental correlations.
pair_rho <- unique(pairs[, c("pair_key", "rho_early", "rho_late", "delta_rho")])
analysis2 <- merge(
  analysis,
  pair_rho[, c("pair_key", "rho_early", "rho_late")],
  by = "pair_key",
  all.x = TRUE,
  sort = FALSE
)

pair_eligible <- unique(analysis2[, c("pair_key", "rho_early", "rho_late", "delta_rho")])
rho_early_mu <- mean(pair_eligible$rho_early)
rho_early_sd <- sd(pair_eligible$rho_early)
if (!is.finite(rho_early_sd) || rho_early_sd <= 0) stop("Invalid rho_early SD")
analysis2$z_rho_early <- (analysis2$rho_early - rho_early_mu) / rho_early_sd

# Fisher-z change scale.
clamp <- function(x) pmax(-0.999, pmin(0.999, x))
pair_eligible$delta_z <- atanh(clamp(pair_eligible$rho_late)) -
  atanh(clamp(pair_eligible$rho_early))
delta_z_mu <- mean(pair_eligible$delta_z)
delta_z_sd <- sd(pair_eligible$delta_z)
if (!is.finite(delta_z_sd) || delta_z_sd <= 0) stop("Invalid delta_z SD")
pair_eligible$z_delta_z <- (pair_eligible$delta_z - delta_z_mu) / delta_z_sd
analysis2 <- merge(
  analysis2,
  pair_eligible[, c("pair_key", "z_delta_z")],
  by = "pair_key",
  all.x = TRUE,
  sort = FALSE
)

coef_weighted <- function(df, outcome, predictors) {
  X <- cbind("(Intercept)" = 1, as.matrix(df[, predictors, drop = FALSE]))
  y <- df[[outcome]]
  nn <- table(df$species)
  w <- 1 / as.numeric(nn[df$species])
  fit <- try(lm.wfit(X, y, w = w), silent = TRUE)
  if (inherits(fit, "try-error")) return(rep(NA_real_, length(predictors)))
  out <- fit$coefficients[predictors]
  as.numeric(out)
}

# A2 fixed-arrival structural-null outcome.
# Use only annual records that had finite arrival and green-up in the frozen bird table,
# preserving the exact biological observation support of the transfer sample.
row_key <- function(species, cell) paste(species, as.character(cell), sep = "__")
analysis2$row_key <- row_key(analysis2$species, analysis2$target_cell)

bird2 <- bird[
  bird$year >= EARLY_START & bird$year <= LATE_END,
  ,
  drop = FALSE
]
bird2$row_key <- row_key(bird2$species, bird2$cell)
bird2 <- bird2[bird2$row_key %in% analysis2$row_key, , drop = FALSE]

fixed_arr <- aggregate(arr_GAM_mean ~ row_key, data = bird2, FUN = mean)
names(fixed_arr)[2] <- "fixed_arrival"
bird2 <- merge(bird2, fixed_arr, by = "row_key", all.x = TRUE, sort = FALSE)
bird2$pseudo_mismatch_y <- log1p(abs(bird2$gr_mn - bird2$fixed_arrival))

pseudo_window <- function(k, start_year, end_year) {
  z <- bird2[
    bird2$row_key == k &
      bird2$year >= start_year &
      bird2$year <= end_year,
    ,
    drop = FALSE
  ]
  z <- z[!duplicated(z$year), , drop = FALSE]
  c(n = nrow(z), mean = if (nrow(z) > 0) mean(z$pseudo_mismatch_y) else NA_real_)
}

pe <- t(vapply(
  analysis2$row_key,
  function(k) pseudo_window(k, EARLY_START, EARLY_END),
  numeric(2)
))
pl <- t(vapply(
  analysis2$row_key,
  function(k) pseudo_window(k, LATE_START, LATE_END),
  numeric(2)
))
analysis2$pseudo_early_n <- as.integer(pe[, "n"])
analysis2$pseudo_late_n <- as.integer(pl[, "n"])
analysis2$pseudo_mismatch_early <- as.numeric(pe[, "mean"])
analysis2$pseudo_mismatch_late <- as.numeric(pl[, "mean"])
analysis2$delta_pseudo_mismatch <- analysis2$pseudo_mismatch_late -
  analysis2$pseudo_mismatch_early

if (!all(analysis2$pseudo_early_n >= MIN_BIRD_YEARS_PER_WINDOW) ||
    !all(analysis2$pseudo_late_n >= MIN_BIRD_YEARS_PER_WINDOW)) {
  stop("Fixed-arrival null changed the frozen transfer eligibility unexpectedly")
}

# Point estimates A1/A2/A4/A5.
a1_beta <- coef_weighted(
  analysis2,
  "delta_mismatch",
  c("z_delta_rho", "z_rho_early")
)[1]

a2_beta_null <- coef_weighted(
  analysis2,
  "delta_pseudo_mismatch",
  "z_delta_rho"
)[1]

a2_beta_observed <- coef_weighted(
  analysis2,
  "delta_mismatch",
  "z_delta_rho"
)[1]
a2_bird_increment <- a2_beta_observed - a2_beta_null

a4_cor <- cor(pair_eligible$rho_early, pair_eligible$delta_rho)

a5_beta <- coef_weighted(
  analysis2,
  "delta_mismatch",
  "z_delta_z"
)[1]

# Shared unique-pair bootstrap for A1/A2/A4/A5.
pair_keys <- unique(analysis2$pair_key)
P <- length(pair_keys)
rows_by_pair <- split(analysis2, analysis2$pair_key)
pair_table_by_key <- split(pair_eligible, pair_eligible$pair_key)

set.seed(SEED)
boot <- matrix(
  NA_real_,
  nrow = B,
  ncol = 6,
  dimnames = list(
    NULL,
    c(
      "a1_beta_baseline_rho",
      "a2_beta_observed",
      "a2_beta_fixed_null",
      "a2_bird_increment",
      "a4_cor_baseline_change",
      "a5_beta_fisher_z"
    )
  )
)

for (b in seq_len(B)) {
  sampled <- sample(pair_keys, size = P, replace = TRUE)

  chunks <- vector("list", length(sampled))
  pchunks <- vector("list", length(sampled))
  for (k in seq_along(sampled)) {
    z <- rows_by_pair[[sampled[k]]]
    z$bootstrap_draw <- k
    chunks[[k]] <- z

    pz <- pair_table_by_key[[sampled[k]]]
    pz$bootstrap_draw <- k
    pchunks[[k]] <- pz
  }
  bd <- do.call(rbind, chunks)
  bp <- do.call(rbind, pchunks)

  boot[b, "a1_beta_baseline_rho"] <- coef_weighted(
    bd,
    "delta_mismatch",
    c("z_delta_rho", "z_rho_early")
  )[1]
  bo <- coef_weighted(bd, "delta_mismatch", "z_delta_rho")[1]
  bn <- coef_weighted(bd, "delta_pseudo_mismatch", "z_delta_rho")[1]
  boot[b, "a2_beta_observed"] <- bo
  boot[b, "a2_beta_fixed_null"] <- bn
  boot[b, "a2_bird_increment"] <- bo - bn
  boot[b, "a4_cor_baseline_change"] <- suppressWarnings(
    cor(bp$rho_early, bp$delta_rho)
  )
  boot[b, "a5_beta_fisher_z"] <- coef_weighted(
    bd,
    "delta_mismatch",
    "z_delta_z"
  )[1]
}

ci <- function(x) {
  x <- x[is.finite(x)]
  as.numeric(quantile(x, c(0.025, 0.975), names = FALSE))
}

# A3 within-window arrival permutation null.
annual_list <- split(bird2, bird2$row_key)
base_rows <- analysis2
set.seed(PERM_SEED)
perm_beta <- rep(NA_real_, PERM_B)

for (b in seq_len(PERM_B)) {
  perm_delta <- rep(NA_real_, nrow(base_rows))

  for (i in seq_len(nrow(base_rows))) {
    z <- annual_list[[base_rows$row_key[i]]]
    ze <- z[z$year >= EARLY_START & z$year <= EARLY_END, , drop = FALSE]
    zl <- z[z$year >= LATE_START & z$year <= LATE_END, , drop = FALSE]

    ae <- sample(ze$arr_GAM_mean, size = nrow(ze), replace = FALSE)
    al <- sample(zl$arr_GAM_mean, size = nrow(zl), replace = FALSE)

    me <- mean(log1p(abs(ze$gr_mn - ae)))
    ml <- mean(log1p(abs(zl$gr_mn - al)))
    perm_delta[i] <- ml - me
  }

  pd <- base_rows
  pd$delta_perm_mismatch <- perm_delta
  perm_beta[b] <- coef_weighted(
    pd,
    "delta_perm_mismatch",
    "z_delta_rho"
  )[1]
}

perm_finite <- perm_beta[is.finite(perm_beta)]
perm_interval <- as.numeric(quantile(
  perm_finite,
  c(0.025, 0.5, 0.975),
  names = FALSE
))
perm_le_obs <- mean(perm_finite <= a2_beta_observed)
perm_ge_obs <- mean(perm_finite >= a2_beta_observed)

a1_ci <- ci(boot[, "a1_beta_baseline_rho"])
a2_obs_ci <- ci(boot[, "a2_beta_observed"])
a2_null_ci <- ci(boot[, "a2_beta_fixed_null"])
a2_inc_ci <- ci(boot[, "a2_bird_increment"])
a4_ci <- ci(boot[, "a4_cor_baseline_change"])
a5_ci <- ci(boot[, "a5_beta_fisher_z"])

structural_explained <- (
  is.finite(a2_beta_null) &&
  a2_beta_null > 0 &&
  a2_inc_ci[1] <= 0 &&
  a2_inc_ci[2] >= 0
)

bird_increment_detected <- (
  (a2_inc_ci[2] < 0) || (a2_inc_ci[1] > 0)
)

summary_rows <- rbind(
  data.frame(
    audit = "A1_BASELINE_RHO_ADJUSTMENT",
    estimate = a1_beta,
    ci_low_95 = a1_ci[1],
    ci_high_95 = a1_ci[2],
    secondary = NA_real_,
    secondary_low = NA_real_,
    secondary_high = NA_real_,
    note = "coefficient on z_delta_rho adjusting z_rho_early"
  ),
  data.frame(
    audit = "A2_FIXED_ARRIVAL_NULL",
    estimate = a2_beta_null,
    ci_low_95 = a2_null_ci[1],
    ci_high_95 = a2_null_ci[2],
    secondary = a2_bird_increment,
    secondary_low = a2_inc_ci[1],
    secondary_high = a2_inc_ci[2],
    note = "estimate=fixed-arrival null beta; secondary=observed minus null beta"
  ),
  data.frame(
    audit = "A3_WITHIN_WINDOW_ARRIVAL_PERMUTATION",
    estimate = perm_interval[2],
    ci_low_95 = perm_interval[1],
    ci_high_95 = perm_interval[3],
    secondary = a2_beta_observed,
    secondary_low = perm_le_obs,
    secondary_high = perm_ge_obs,
    note = "estimate=null median; secondary=observed beta; secondary low/high=fractions perm <=/>= observed"
  ),
  data.frame(
    audit = "A4_BASELINE_CHANGE_COUPLING",
    estimate = a4_cor,
    ci_low_95 = a4_ci[1],
    ci_high_95 = a4_ci[2],
    secondary = NA_real_,
    secondary_low = NA_real_,
    secondary_high = NA_real_,
    note = "pair-level cor(rho_early, delta_rho)"
  ),
  data.frame(
    audit = "A5_FISHER_Z_TRANSFER",
    estimate = a5_beta,
    ci_low_95 = a5_ci[1],
    ci_high_95 = a5_ci[2],
    secondary = NA_real_,
    secondary_low = NA_real_,
    secondary_high = NA_real_,
    note = "equal-species transfer coefficient using standardized delta-z"
  )
)

status <- data.frame(
  observed_beta = a2_beta_observed,
  fixed_arrival_null_beta = a2_beta_null,
  bird_increment_beta = a2_bird_increment,
  bird_increment_ci_low_95 = a2_inc_ci[1],
  bird_increment_ci_high_95 = a2_inc_ci[2],
  structural_explained = ifelse(structural_explained, "YES", "NO"),
  bird_increment_detected = ifelse(bird_increment_detected, "YES", "NO"),
  permutation_replicates = PERM_B,
  permutation_seed = PERM_SEED,
  pair_bootstrap_replicates = B,
  pair_bootstrap_seed = SEED
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(
  summary_rows,
  "outputs/payoff_b_v8_transfer_structural_null_summary.csv",
  row.names = FALSE
)
write.csv(
  status,
  "outputs/payoff_b_v8_transfer_structural_null_status.csv",
  row.names = FALSE
)
write.csv(
  data.frame(replicate = seq_len(B), boot),
  "outputs/payoff_b_v8_transfer_structural_null_bootstrap.csv",
  row.names = FALSE
)
write.csv(
  data.frame(replicate = seq_len(PERM_B), beta = perm_beta),
  "outputs/payoff_b_v8_transfer_arrival_permutation.csv",
  row.names = FALSE
)
write.csv(
  analysis2,
  "outputs/payoff_b_v8_transfer_structural_null_rows.csv",
  row.names = FALSE
)

cat("\nPAYOFF-B V8 TRANSFER STRUCTURAL-NULL AUDIT\n")
print(summary_rows, row.names = FALSE)
cat("\nSTATUS\n")
print(status)
cat("\nNo migration-speed outcome was analyzed.\n")
