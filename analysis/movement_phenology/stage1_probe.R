#!/usr/bin/env Rscript

# Fast Stage-1 empirical probe for the PAYOFF-B movement–phenology programme.
# Uses only base R so it can run reproducibly in CI on the published final.rds.
#
# This probe is descriptive / diagnostic. It is not the final inferential model.

input_path <- Sys.getenv(
  "PAYOFF_AMARAL_FINAL_RDS",
  "external/amaral_2025/data/final.rds"
)
out_dir <- "outputs/movement_phenology"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

if (!file.exists(input_path)) {
  stop(paste("Missing Stage-1 data:", input_path))
}

dat0 <- readRDS(input_path)

required <- c(
  "year", "cell", "species", "cell_lat2",
  "arr_GAM_mean", "gr_mn",
  "vArrMag", "vArrAng", "vGrMag", "vGrAng",
  "mig_cell", "breed_cell"
)
missing <- setdiff(required, names(dat0))
if (length(missing) > 0L) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

dat <- as.data.frame(dat0[, required])

dat$signed_lag <- dat$arr_GAM_mean - dat$gr_mn
dat$abs_mismatch_days <- abs(dat$signed_lag)
dat$speed_ratio <- dat$vArrMag / dat$vGrMag
dat$log_speed_ratio <- log(dat$speed_ratio)
dat$alignment <- cos(dat$vArrAng - dat$vGrAng)
dat$vector_mismatch <- sqrt(
  pmax(0, 1 + dat$speed_ratio^2 - 2 * dat$speed_ratio * dat$alignment)
)

dat$range_type <- ifelse(
  dat$mig_cell & dat$breed_cell, "both",
  ifelse(dat$mig_cell, "mig", ifelse(dat$breed_cell, "breed", "other"))
)

keep <- with(
  dat,
  is.finite(abs_mismatch_days) &
    is.finite(vArrMag) &
    is.finite(vGrMag) &
    vArrMag > 0 &
    vGrMag > 0 &
    vArrMag <= 3000 &
    vGrMag <= 3000 &
    is.finite(log_speed_ratio) &
    is.finite(alignment) &
    is.finite(cell_lat2)
)
dat <- dat[keep, , drop = FALSE]

if (nrow(dat) < 100L) stop("Too few complete observations after registered filters.")

# Winsorization is not used for the registered model. For the diagnostic curve,
# trim only to the central 98% of q so a few extreme ratios do not determine bins.
qlo <- unname(quantile(dat$log_speed_ratio, 0.01, na.rm = TRUE))
qhi <- unname(quantile(dat$log_speed_ratio, 0.99, na.rm = TRUE))
curve_dat <- dat[dat$log_speed_ratio >= qlo & dat$log_speed_ratio <= qhi, , drop = FALSE]

# Model A: pooled quadratic with species, year, and cell controls.
# It estimates the shape of mismatch along log speed ratio without calling the
# vertex an evolutionary optimum.
m_quad <- lm(
  abs_mismatch_days ~
    log_speed_ratio + I(log_speed_ratio^2) +
    alignment + scale(cell_lat2) +
    factor(range_type) +
    factor(species) + factor(year) + factor(cell),
  data = curve_dat
)

co <- coef(m_quad)
b1 <- unname(co[["log_speed_ratio"]])
b2 <- unname(co[["I(log_speed_ratio^2)"]])
finite_min <- is.finite(b1) && is.finite(b2) && b2 > 0
q_star <- if (finite_min) -b1 / (2 * b2) else NA_real_
u_star <- if (is.finite(q_star)) exp(q_star) else NA_real_

# Model B: geometry-aware mismatch model. If the movement and phenology wave
# align perfectly in both speed and direction, vector_mismatch is zero by
# construction; here we ask whether observed date mismatch increases with it.
m_vector <- lm(
  abs_mismatch_days ~
    vector_mismatch + scale(cell_lat2) +
    factor(range_type) +
    factor(species) + factor(year) + factor(cell),
  data = curve_dat
)

vector_beta <- unname(coef(m_vector)[["vector_mismatch"]])

# Descriptive decile curve, useful even if the quadratic shape is inadequate.
breaks <- unique(quantile(
  curve_dat$log_speed_ratio,
  probs = seq(0, 1, by = 0.1),
  na.rm = TRUE
))
curve_dat$q_bin <- cut(
  curve_dat$log_speed_ratio,
  breaks = breaks,
  include.lowest = TRUE,
  ordered_result = TRUE
)

bin_levels <- levels(curve_dat$q_bin)
binned <- do.call(
  rbind,
  lapply(bin_levels, function(z) {
    x <- curve_dat[curve_dat$q_bin == z, , drop = FALSE]
    data.frame(
      q_bin = z,
      n = nrow(x),
      median_q = median(x$log_speed_ratio, na.rm = TRUE),
      median_speed_ratio = median(x$speed_ratio, na.rm = TRUE),
      mean_abs_mismatch_days = mean(x$abs_mismatch_days, na.rm = TRUE),
      median_abs_mismatch_days = median(x$abs_mismatch_days, na.rm = TRUE),
      mean_alignment = mean(x$alignment, na.rm = TRUE)
    )
  })
)

min_bin <- binned[which.min(binned$mean_abs_mismatch_days), , drop = FALSE]

summary_row <- data.frame(
  n_rows = nrow(dat),
  n_rows_central98 = nrow(curve_dat),
  n_species = length(unique(dat$species)),
  n_years = length(unique(dat$year)),
  n_cells = length(unique(dat$cell)),
  q_01 = qlo,
  q_99 = qhi,
  median_speed_ratio = median(dat$speed_ratio, na.rm = TRUE),
  median_alignment = median(dat$alignment, na.rm = TRUE),
  quadratic_beta_linear = b1,
  quadratic_beta_squared = b2,
  quadratic_finite_minimum = finite_min,
  quadratic_q_star = q_star,
  quadratic_u_macro_star = u_star,
  q_star_inside_central98 = is.finite(q_star) && q_star >= qlo && q_star <= qhi,
  vector_mismatch_beta = vector_beta,
  min_bin_speed_ratio = min_bin$median_speed_ratio,
  min_bin_mean_abs_mismatch_days = min_bin$mean_abs_mismatch_days,
  payoff_b_strong_reference = 1.0,
  payoff_b_weak_reference = 1.60611529880277
)

write.csv(
  summary_row,
  file.path(out_dir, "stage1_probe_summary.csv"),
  row.names = FALSE
)
write.csv(
  binned,
  file.path(out_dir, "stage1_probe_deciles.csv"),
  row.names = FALSE
)

capture.output(
  summary(m_quad),
  file = file.path(out_dir, "stage1_probe_quadratic_summary.txt")
)
capture.output(
  summary(m_vector),
  file = file.path(out_dir, "stage1_probe_vector_summary.txt")
)

cat("PAYOFF-B movement–phenology Stage-1 probe\n")
print(summary_row)
