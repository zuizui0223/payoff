#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

PRIMARY_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_downstream_transfer_primary.R"
LOCK_DOC <- "docs/PAYOFF_B_V8_TRANSFER_SENSITIVITY_LOCK_20261005.md"

if (!file.exists(PRIMARY_SCRIPT)) stop("Missing frozen V8 transfer primary script")
if (!file.exists(LOCK_DOC)) stop("Missing transfer sensitivity lock")

# Reconstruct the frozen transfer sample and primary result.
source(PRIMARY_SCRIPT, local = FALSE)

B <- 10000L
SEED <- 20261005L

std_params <- function(x) c(mu = mean(x), sd = sd(x))
z_with <- function(x, pars) (x - pars[["mu"]]) / pars[["sd"]]

base_pars <- std_params(analysis$mean_mismatch_early)
green_pars <- std_params(analysis$delta_greenup_mean)
if (!is.finite(base_pars[["sd"]]) || base_pars[["sd"]] <= 0) stop("Invalid baseline mismatch SD")
if (!is.finite(green_pars[["sd"]]) || green_pars[["sd"]] <= 0) stop("Invalid delta-greenup SD")

analysis$z_baseline_mismatch <- z_with(analysis$mean_mismatch_early, base_pars)
analysis$z_delta_greenup <- z_with(analysis$delta_greenup_mean, green_pars)

coef_z <- function(df, extra_cols = character(0), equal_species = TRUE) {
  cols <- c("z_delta_rho", extra_cols)
  X <- cbind("(Intercept)" = 1, as.matrix(df[, cols, drop = FALSE]))
  y <- df$delta_mismatch
  if (equal_species) {
    nn <- table(df$species)
    w <- 1 / as.numeric(nn[df$species])
    fit <- try(lm.wfit(X, y, w = w), silent = TRUE)
  } else {
    fit <- try(lm.fit(X, y), silent = TRUE)
  }
  if (inherits(fit, "try-error")) return(NA_real_)
  out <- fit$coefficients["z_delta_rho"]
  if (length(out) == 0 || !is.finite(out)) return(NA_real_)
  unname(out)
}

species_collapse_beta <- function(df) {
  d1 <- aggregate(delta_mismatch ~ species, data = df, FUN = mean)
  d2 <- aggregate(z_delta_rho ~ species, data = df, FUN = mean)
  d <- merge(d1, d2, by = "species", all = FALSE)
  if (nrow(d) < 3 || length(unique(d$z_delta_rho)) < 2) return(NA_real_)
  unname(coef(lm(delta_mismatch ~ z_delta_rho, data = d))["z_delta_rho"])
}

overall_stats <- function(df) {
  row_mean <- mean(df$delta_mismatch)
  sp <- aggregate(delta_mismatch ~ species, data = df, FUN = mean)
  c(row_mean = row_mean, equal_species_mean = mean(sp$delta_mismatch))
}

# Point estimates.
desc_point <- overall_stats(analysis)
s1_beta <- coef_z(analysis, equal_species = FALSE)
s2_beta <- species_collapse_beta(analysis)
s3_beta <- coef_z(analysis, extra_cols = "z_baseline_mismatch", equal_species = TRUE)
s4_beta <- coef_z(analysis, extra_cols = "z_delta_greenup", equal_species = TRUE)
s5_beta <- coef_z(
  analysis,
  extra_cols = c("z_baseline_mismatch", "z_delta_greenup"),
  equal_species = TRUE
)

# Shared pair bootstrap for descriptive and S1-S5.
pair_keys <- unique(analysis$pair_key)
P <- length(pair_keys)
rows_by_pair <- split(analysis, analysis$pair_key)

set.seed(SEED)
boot <- matrix(
  NA_real_,
  nrow = B,
  ncol = 7,
  dimnames = list(
    NULL,
    c(
      "row_mean_delta_mismatch",
      "equal_species_mean_delta_mismatch",
      "s1_unweighted_beta",
      "s2_species_collapse_beta",
      "s3_baseline_beta",
      "s4_greenup_beta",
      "s5_both_beta"
    )
  )
)

for (b in seq_len(B)) {
  sampled <- sample(pair_keys, size = P, replace = TRUE)
  chunks <- vector("list", length(sampled))
  for (k in seq_along(sampled)) {
    z <- rows_by_pair[[sampled[k]]]
    z$bootstrap_draw <- k
    chunks[[k]] <- z
  }
  bd <- do.call(rbind, chunks)

  os <- overall_stats(bd)
  boot[b, "row_mean_delta_mismatch"] <- os[["row_mean"]]
  boot[b, "equal_species_mean_delta_mismatch"] <- os[["equal_species_mean"]]
  boot[b, "s1_unweighted_beta"] <- coef_z(bd, equal_species = FALSE)
  boot[b, "s2_species_collapse_beta"] <- species_collapse_beta(bd)
  boot[b, "s3_baseline_beta"] <- coef_z(
    bd,
    extra_cols = "z_baseline_mismatch",
    equal_species = TRUE
  )
  boot[b, "s4_greenup_beta"] <- coef_z(
    bd,
    extra_cols = "z_delta_greenup",
    equal_species = TRUE
  )
  boot[b, "s5_both_beta"] <- coef_z(
    bd,
    extra_cols = c("z_baseline_mismatch", "z_delta_greenup"),
    equal_species = TRUE
  )
}

ci_col <- function(x) {
  x <- x[is.finite(x)]
  as.numeric(quantile(x, c(0.025, 0.975), names = FALSE))
}

# S6 leave-one-species-out.
loo_species <- sort(unique(analysis$species))
loo <- data.frame(
  omitted_species = loo_species,
  beta_transfer = NA_real_
)
for (i in seq_along(loo_species)) {
  d <- analysis[analysis$species != loo_species[i], , drop = FALSE]
  loo$beta_transfer[i] <- coef_z(d, equal_species = TRUE)
}

# S7 exact-complete bird windows.
complete <- analysis[
  analysis$bird_early_n == 8L &
    analysis$bird_late_n == 8L,
  ,
  drop = FALSE
]

s7_beta <- NA_real_
s7_ci <- c(NA_real_, NA_real_)
s7_pair_n <- length(unique(complete$pair_key))
s7_species_n <- length(unique(complete$species))

if (nrow(complete) >= 3 && s7_pair_n >= 2 && s7_species_n >= 2) {
  pexp <- unique(complete[, c("pair_key", "delta_rho")])
  s7_mu <- mean(pexp$delta_rho)
  s7_sd <- sd(pexp$delta_rho)
  if (is.finite(s7_sd) && s7_sd > 0) {
    complete$z_delta_rho <- (complete$delta_rho - s7_mu) / s7_sd
    s7_beta <- coef_z(complete, equal_species = TRUE)

    keys7 <- unique(complete$pair_key)
    rows7 <- split(complete, complete$pair_key)
    P7 <- length(keys7)
    set.seed(SEED)
    b7 <- rep(NA_real_, B)
    for (b in seq_len(B)) {
      sampled <- sample(keys7, size = P7, replace = TRUE)
      chunks <- vector("list", length(sampled))
      for (k in seq_along(sampled)) {
        z <- rows7[[sampled[k]]]
        z$bootstrap_draw <- k
        chunks[[k]] <- z
      }
      bd <- do.call(rbind, chunks)
      b7[b] <- coef_z(bd, equal_species = TRUE)
    }
    s7_ci <- ci_col(b7)
  }
}

desc_row_ci <- ci_col(boot[, "row_mean_delta_mismatch"])
desc_sp_ci <- ci_col(boot[, "equal_species_mean_delta_mismatch"])
s1_ci <- ci_col(boot[, "s1_unweighted_beta"])
s2_ci <- ci_col(boot[, "s2_species_collapse_beta"])
s3_ci <- ci_col(boot[, "s3_baseline_beta"])
s4_ci <- ci_col(boot[, "s4_greenup_beta"])
s5_ci <- ci_col(boot[, "s5_both_beta"])

summary_rows <- rbind(
  data.frame(
    result = "DESCRIPTIVE_UNWEIGHTED_MEAN_DELTA_MISMATCH",
    estimate = desc_point[["row_mean"]],
    ci_low_95 = desc_row_ci[1],
    ci_high_95 = desc_row_ci[2],
    n_rows = nrow(analysis),
    n_pairs = length(unique(analysis$pair_key)),
    n_species = length(unique(analysis$species)),
    note = "late-minus-early mean log1p absolute mismatch; negative=improvement"
  ),
  data.frame(
    result = "DESCRIPTIVE_EQUAL_SPECIES_MEAN_DELTA_MISMATCH",
    estimate = desc_point[["equal_species_mean"]],
    ci_low_95 = desc_sp_ci[1],
    ci_high_95 = desc_sp_ci[2],
    n_rows = nrow(analysis),
    n_pairs = length(unique(analysis$pair_key)),
    n_species = length(unique(analysis$species)),
    note = "species means averaged equally; negative=improvement"
  ),
  data.frame(
    result = "S1_UNWEIGHTED_ROW_TRANSFER",
    estimate = s1_beta,
    ci_low_95 = s1_ci[1],
    ci_high_95 = s1_ci[2],
    n_rows = nrow(analysis),
    n_pairs = length(unique(analysis$pair_key)),
    n_species = length(unique(analysis$species)),
    note = "unweighted species-target-cell regression"
  ),
  data.frame(
    result = "S2_EQUAL_SPECIES_COLLAPSE",
    estimate = s2_beta,
    ci_low_95 = s2_ci[1],
    ci_high_95 = s2_ci[2],
    n_rows = nrow(analysis),
    n_pairs = length(unique(analysis$pair_key)),
    n_species = length(unique(analysis$species)),
    note = "species-level mean delta-mismatch on mean z-delta-rho"
  ),
  data.frame(
    result = "S3_BASELINE_MISMATCH_COVARIATE",
    estimate = s3_beta,
    ci_low_95 = s3_ci[1],
    ci_high_95 = s3_ci[2],
    n_rows = nrow(analysis),
    n_pairs = length(unique(analysis$pair_key)),
    n_species = length(unique(analysis$species)),
    note = "equal-species weighted; adjusts early-window mismatch"
  ),
  data.frame(
    result = "S4_TARGET_GREENUP_SHIFT_COVARIATE",
    estimate = s4_beta,
    ci_low_95 = s4_ci[1],
    ci_high_95 = s4_ci[2],
    n_rows = nrow(analysis),
    n_pairs = length(unique(analysis$pair_key)),
    n_species = length(unique(analysis$species)),
    note = "equal-species weighted; adjusts late-minus-early target green-up mean"
  ),
  data.frame(
    result = "S5_BOTH_COVARIATES",
    estimate = s5_beta,
    ci_low_95 = s5_ci[1],
    ci_high_95 = s5_ci[2],
    n_rows = nrow(analysis),
    n_pairs = length(unique(analysis$pair_key)),
    n_species = length(unique(analysis$species)),
    note = "equal-species weighted; baseline mismatch + target green-up shift"
  ),
  data.frame(
    result = "S6_LOO_SPECIES_RANGE",
    estimate = min(loo$beta_transfer, na.rm = TRUE),
    ci_low_95 = max(loo$beta_transfer, na.rm = TRUE),
    ci_high_95 = sum(loo$beta_transfer > 0, na.rm = TRUE),
    n_rows = nrow(analysis),
    n_pairs = length(unique(analysis$pair_key)),
    n_species = nrow(loo),
    note = "estimate=min beta; ci_low=max beta; ci_high=count positive; full LOO table saved"
  ),
  data.frame(
    result = "S7_EXACT_COMPLETE_BIRD_WINDOWS",
    estimate = s7_beta,
    ci_low_95 = s7_ci[1],
    ci_high_95 = s7_ci[2],
    n_rows = nrow(complete),
    n_pairs = s7_pair_n,
    n_species = s7_species_n,
    note = "requires 8/8 finite mismatch years in both periods"
  )
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(
  summary_rows,
  "outputs/payoff_b_v8_transfer_sensitivity_summary.csv",
  row.names = FALSE
)
write.csv(
  loo,
  "outputs/payoff_b_v8_transfer_loo_species.csv",
  row.names = FALSE
)
write.csv(
  complete,
  "outputs/payoff_b_v8_transfer_complete_rows.csv",
  row.names = FALSE
)
write.csv(
  data.frame(replicate = seq_len(B), boot),
  "outputs/payoff_b_v8_transfer_sensitivity_bootstrap.csv",
  row.names = FALSE
)

cat("\nPAYOFF-B V8 DOWNSTREAM TRANSFER SENSITIVITIES\n")
print(summary_rows, row.names = FALSE)
cat("\nLOO positive coefficients: ", sum(loo$beta_transfer > 0, na.rm = TRUE),
    "/", nrow(loo), "\n", sep = "")
cat("LOO negative coefficients: ", sum(loo$beta_transfer < 0, na.rm = TRUE),
    "/", nrow(loo), "\n", sep = "")
cat("No migration-speed-change analysis was run.\n")
