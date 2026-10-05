#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

PRIMARY_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_downstream_transfer_primary.R"
CONTRACT <- "docs/PAYOFF_B_V8_MATCHED_BETWEEN_WITHIN_CONTRACT_20261005.md"

if (!file.exists(PRIMARY_SCRIPT)) stop("Missing frozen transfer primary script")
if (!file.exists(CONTRACT)) stop("Missing matched between-within contract")

source(PRIMARY_SCRIPT, local = FALSE)

B <- 10000L
SEED <- 20261005L

pair_rho <- unique(pairs[, c("pair_key", "rho_early", "rho_late")])
base <- merge(
  analysis,
  pair_rho,
  by = "pair_key",
  all.x = TRUE,
  sort = FALSE
)

# Unique-pair decomposition and fixed standardization constants.
up <- unique(base[, c("pair_key", "rho_early", "rho_late")])
up$rho_bar <- (up$rho_early + up$rho_late) / 2

between_mu <- mean(up$rho_bar)
between_sd <- sd(up$rho_bar)
if (!is.finite(between_sd) || between_sd <= 0) stop("Invalid between SD")
up$z_between <- (up$rho_bar - between_mu) / between_sd

pair_period <- rbind(
  data.frame(
    pair_key = up$pair_key,
    period = "EARLY",
    rho = up$rho_early,
    rho_bar = up$rho_bar
  ),
  data.frame(
    pair_key = up$pair_key,
    period = "LATE",
    rho = up$rho_late,
    rho_bar = up$rho_bar
  )
)
pair_period$rho_within <- pair_period$rho - pair_period$rho_bar
within_mu <- mean(pair_period$rho_within)
within_sd <- sd(pair_period$rho_within)
if (!is.finite(within_sd) || within_sd <= 0) stop("Invalid within SD")
pair_period$z_within <- (pair_period$rho_within - within_mu) / within_sd

# Period-specific standardization for simple matched summaries.
early_mu <- mean(up$rho_early)
early_sd <- sd(up$rho_early)
late_mu <- mean(up$rho_late)
late_sd <- sd(up$rho_late)
if (early_sd <= 0 || late_sd <= 0) stop("Invalid period rho SD")

# Build 2-period matched panel.
early_rows <- base
early_rows$period <- "EARLY"
early_rows$period_late <- 0
early_rows$mismatch <- early_rows$mean_mismatch_early
early_rows$rho <- early_rows$rho_early

late_rows <- base
late_rows$period <- "LATE"
late_rows$period_late <- 1
late_rows$mismatch <- late_rows$mean_mismatch_late
late_rows$rho <- late_rows$rho_late

panel <- rbind(early_rows, late_rows)
panel <- merge(
  panel,
  up[, c("pair_key", "z_between")],
  by = "pair_key",
  all.x = TRUE,
  sort = FALSE
)
panel <- merge(
  panel,
  pair_period[, c("pair_key", "period", "z_within")],
  by = c("pair_key", "period"),
  all.x = TRUE,
  sort = FALSE
)

# Simple-period coordinates.
early_rows$z_rho_period <- (early_rows$rho_early - early_mu) / early_sd
late_rows$z_rho_period <- (late_rows$rho_late - late_mu) / late_sd

fit_panel <- function(df) {
  X <- cbind(
    "(Intercept)" = 1,
    period_late = df$period_late,
    z_between = df$z_between,
    z_within = df$z_within
  )
  nn <- table(df$species)
  w <- 1 / as.numeric(nn[df$species])
  fit <- try(lm.wfit(X, df$mismatch, w = w), silent = TRUE)
  if (inherits(fit, "try-error")) return(c(between = NA_real_, within = NA_real_))
  c(
    between = unname(fit$coefficients["z_between"]),
    within = unname(fit$coefficients["z_within"])
  )
}

fit_period <- function(df, outcome) {
  X <- cbind("(Intercept)" = 1, z_rho_period = df$z_rho_period)
  nn <- table(df$species)
  w <- 1 / as.numeric(nn[df$species])
  fit <- try(lm.wfit(X, df[[outcome]], w = w), silent = TRUE)
  if (inherits(fit, "try-error")) return(NA_real_)
  unname(fit$coefficients["z_rho_period"])
}

point <- fit_panel(panel)
beta_between <- point[["between"]]
beta_within <- point[["within"]]
contrast <- beta_within - beta_between
early_beta <- fit_period(early_rows, "mean_mismatch_early")
late_beta <- fit_period(late_rows, "mean_mismatch_late")

# Pair bootstrap.
keys <- unique(base$pair_key)
P <- length(keys)
panel_by_pair <- split(panel, panel$pair_key)
early_by_pair <- split(early_rows, early_rows$pair_key)
late_by_pair <- split(late_rows, late_rows$pair_key)

set.seed(SEED)
boot <- matrix(
  NA_real_,
  nrow = B,
  ncol = 5,
  dimnames = list(NULL, c("between", "within", "contrast", "early", "late"))
)

for (b in seq_len(B)) {
  sampled <- sample(keys, size = P, replace = TRUE)
  pchunks <- vector("list", length(sampled))
  echunks <- vector("list", length(sampled))
  lchunks <- vector("list", length(sampled))

  for (k in seq_along(sampled)) {
    pk <- sampled[k]

    pz <- panel_by_pair[[pk]]
    pz$bootstrap_draw <- k
    pchunks[[k]] <- pz

    ez <- early_by_pair[[pk]]
    ez$bootstrap_draw <- k
    echunks[[k]] <- ez

    lz <- late_by_pair[[pk]]
    lz$bootstrap_draw <- k
    lchunks[[k]] <- lz
  }

  pd <- do.call(rbind, pchunks)
  ed <- do.call(rbind, echunks)
  ld <- do.call(rbind, lchunks)

  bb <- fit_panel(pd)
  boot[b, "between"] <- bb[["between"]]
  boot[b, "within"] <- bb[["within"]]
  boot[b, "contrast"] <- bb[["within"]] - bb[["between"]]
  boot[b, "early"] <- fit_period(ed, "mean_mismatch_early")
  boot[b, "late"] <- fit_period(ld, "mean_mismatch_late")
}

ci <- function(x) {
  x <- x[is.finite(x)]
  as.numeric(quantile(x, c(0.025, 0.975), names = FALSE))
}

ci_between <- ci(boot[, "between"])
ci_within <- ci(boot[, "within"])
ci_contrast <- ci(boot[, "contrast"])
ci_early <- ci(boot[, "early"])
ci_late <- ci(boot[, "late"])

between_supported <- beta_between < 0 && ci_between[2] < 0
within_supported <- beta_within < 0 && ci_within[2] < 0
dissociation_supported <- (
  between_supported &&
  !within_supported &&
  ci_contrast[1] > 0
)

summary_row <- data.frame(
  matched_species_target_rows = nrow(base),
  matched_unique_spatial_pairs = length(unique(base$pair_key)),
  matched_species = length(unique(base$species)),
  beta_between = beta_between,
  between_ci_low_95 = ci_between[1],
  between_ci_high_95 = ci_between[2],
  beta_within = beta_within,
  within_ci_low_95 = ci_within[1],
  within_ci_high_95 = ci_within[2],
  contrast_within_minus_between = contrast,
  contrast_ci_low_95 = ci_contrast[1],
  contrast_ci_high_95 = ci_contrast[2],
  early_simple_beta = early_beta,
  early_ci_low_95 = ci_early[1],
  early_ci_high_95 = ci_early[2],
  late_simple_beta = late_beta,
  late_ci_low_95 = ci_late[1],
  late_ci_high_95 = ci_late[2],
  between_information_association = ifelse(
    between_supported, "SUPPORTED", "NOT_SUPPORTED"
  ),
  within_information_transfer = ifelse(
    within_supported, "SUPPORTED", "NOT_SUPPORTED"
  ),
  between_within_dissociation = ifelse(
    dissociation_supported, "SUPPORTED", "NOT_SUPPORTED"
  ),
  bootstrap_replicates = B,
  bootstrap_seed = SEED
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_matched_between_within_summary.csv",
  row.names = FALSE
)
write.csv(
  panel,
  "outputs/payoff_b_v8_matched_between_within_panel.csv",
  row.names = FALSE
)
write.csv(
  data.frame(replicate = seq_len(B), boot),
  "outputs/payoff_b_v8_matched_between_within_bootstrap.csv",
  row.names = FALSE
)

cat("\nPAYOFF-B V8 MATCHED BETWEEN-WITHIN INFORMATION ANALYSIS\n")
print(summary_row)
