#!/usr/bin/env Rscript

# PAYOFF-B macro reanalysis of Amaral et al. (2025)
# Data DOI: 10.5061/dryad.ttdz08m6w
#
# Primary estimand:
# location of the minimum absolute bird-arrival / vegetation-greenup mismatch
# along log(bird migration-front speed / green-up-front speed).

suppressPackageStartupMessages({
  library(mgcv)
})

input_path <- Sys.getenv(
  "PAYOFF_AMARAL_FINAL_RDS",
  "external/amaral_2025/data/final.rds"
)
out_dir <- "outputs/movement_phenology"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

if (!file.exists(input_path)) {
  stop(
    paste0(
      "Missing ", input_path, ". Download the published Amaral et al. dataset ",
      "(doi:10.5061/dryad.ttdz08m6w) or set PAYOFF_AMARAL_FINAL_RDS."
    )
  )
}

dat0 <- as.data.frame(readRDS(input_path))

required <- c(
  "year", "cell", "species", "cell_lat2",
  "arr_GAM_mean", "gr_mn",
  "vArrMag", "vArrAng", "vGrMag", "vGrAng",
  "mig_cell", "breed_cell"
)
missing <- setdiff(required, names(dat0))
if (length(missing) > 0) {
  stop(paste("Missing required columns:", paste(missing, collapse = ", ")))
}

as_flag <- function(x) {
  if (is.logical(x)) {
    out <- x
  } else {
    out <- tolower(trimws(as.character(x))) %in% c("true", "t", "1", "yes")
  }
  out[is.na(out)] <- FALSE
  out
}

mig_flag <- as_flag(dat0$mig_cell)
breed_flag <- as_flag(dat0$breed_cell)

# Recompute signed lag from dates. The upstream generating code and data
# dictionary use opposite verbal signs for the stored lag field.
dat0$signed_lag <- dat0$arr_GAM_mean - dat0$gr_mn
dat0$abs_mismatch_days <- abs(dat0$signed_lag)
dat0$speed_ratio <- dat0$vArrMag / dat0$vGrMag
dat0$log_speed_ratio <- log(dat0$speed_ratio)
dat0$alignment <- cos(dat0$vArrAng - dat0$vGrAng)
dat0$vector_mismatch <- sqrt(
  pmax(0, 1 + dat0$speed_ratio^2 - 2 * dat0$speed_ratio * dat0$alignment)
)

# Within-cell green-up anomaly. This is recomputed from dates rather than
# inheriting the upstream transformed anomaly.
dat0$greenup_date_anom <- ave(
  dat0$gr_mn,
  dat0$cell,
  FUN = function(z) z - mean(z, na.rm = TRUE)
)

dat0$species <- factor(dat0$species)
dat0$year_f <- factor(dat0$year)
dat0$species_cell <- interaction(dat0$species, dat0$cell, drop = TRUE)
dat0$mig_flag <- factor(mig_flag)
dat0$breed_flag <- factor(breed_flag)

keep <- with(
  dat0,
  is.finite(abs_mismatch_days) &
    is.finite(vArrMag) & is.finite(vGrMag) &
    vArrMag > 0 & vGrMag > 0 &
    vArrMag <= 3000 & vGrMag <= 3000 &
    is.finite(log_speed_ratio) &
    is.finite(alignment) &
    is.finite(cell_lat2) &
    is.finite(greenup_date_anom)
)
dat <- droplevels(dat0[keep, , drop = FALSE])

if (nrow(dat) < 100) {
  stop("Too few complete observations after registered filters.")
}
if (length(unique(dat$species)) < 10) {
  stop("Too few species after registered filters.")
}

# bam() is used because the species:cell random-effect basis can be large.
m_gam <- bam(
  abs_mismatch_days ~
    s(log_speed_ratio, k = 7) +
    s(cell_lat2, k = 7) +
    s(greenup_date_anom, k = 7) +
    alignment +
    ti(log_speed_ratio, alignment, k = c(5, 5)) +
    mig_flag + breed_flag +
    s(species, bs = "re") +
    s(species_cell, bs = "re") +
    s(year_f, bs = "re"),
  data = dat,
  method = "fREML",
  discrete = TRUE
)

# Interpretable quadratic companion with the same repeated-measures structure.
m_quad <- bam(
  abs_mismatch_days ~
    log_speed_ratio + I(log_speed_ratio^2) +
    alignment +
    cell_lat2 +
    greenup_date_anom +
    mig_flag + breed_flag +
    s(species, bs = "re") +
    s(species_cell, bs = "re") +
    s(year_f, bs = "re"),
  data = dat,
  method = "fREML",
  discrete = TRUE
)

co <- coef(m_quad)
b1 <- unname(co[["log_speed_ratio"]])
b2 <- unname(co[["I(log_speed_ratio^2)"]])

quad_status <- if (is.finite(b2) && b2 > 0) "FINITE_MINIMUM" else "NO_CONVEX_MINIMUM"
q_star <- if (quad_status == "FINITE_MINIMUM") -b1 / (2 * b2) else NA_real_
u_star <- if (is.finite(q_star)) exp(q_star) else NA_real_

q_grid <- seq(
  as.numeric(quantile(dat$log_speed_ratio, 0.02, na.rm = TRUE)),
  as.numeric(quantile(dat$log_speed_ratio, 0.98, na.rm = TRUE)),
  length.out = 250
)

newdat <- data.frame(
  log_speed_ratio = q_grid,
  cell_lat2 = median(dat$cell_lat2, na.rm = TRUE),
  greenup_date_anom = 0,
  alignment = median(dat$alignment, na.rm = TRUE),
  mig_flag = factor(levels(dat$mig_flag)[1], levels = levels(dat$mig_flag)),
  breed_flag = factor(levels(dat$breed_flag)[1], levels = levels(dat$breed_flag)),
  species = factor(levels(dat$species)[1], levels = levels(dat$species)),
  species_cell = factor(levels(dat$species_cell)[1], levels = levels(dat$species_cell)),
  year_f = factor(levels(dat$year_f)[1], levels = levels(dat$year_f))
)

pred <- predict(
  m_gam,
  newdata = newdat,
  type = "link",
  se.fit = TRUE,
  exclude = c("s(species)", "s(species_cell)", "s(year_f)")
)

curve <- data.frame(
  log_speed_ratio = q_grid,
  speed_ratio = exp(q_grid),
  fit_abs_mismatch_days = as.numeric(pred$fit),
  se = as.numeric(pred$se.fit)
)
gam_i <- which.min(curve$fit_abs_mismatch_days)
gam_q_star <- curve$log_speed_ratio[gam_i]
gam_u_star <- curve$speed_ratio[gam_i]

summary_row <- data.frame(
  n_rows = nrow(dat),
  n_species = length(unique(dat$species)),
  n_years = length(unique(dat$year)),
  median_speed_ratio = median(dat$speed_ratio, na.rm = TRUE),
  median_alignment = median(dat$alignment, na.rm = TRUE),
  quadratic_status = quad_status,
  quadratic_q_star = q_star,
  quadratic_u_macro_star = u_star,
  gam_q_star = gam_q_star,
  gam_u_macro_star = gam_u_star,
  payoff_b_strong_reference = 1.0,
  payoff_b_weak_reference = 1.60611529880277
)

write.csv(
  summary_row,
  file.path(out_dir, "stage1_summary.csv"),
  row.names = FALSE
)
write.csv(
  curve,
  file.path(out_dir, "stage1_gam_curve.csv"),
  row.names = FALSE
)
saveRDS(m_gam, file.path(out_dir, "stage1_gam.rds"))
saveRDS(m_quad, file.path(out_dir, "stage1_quadratic.rds"))
capture.output(summary(m_gam), file = file.path(out_dir, "stage1_gam_summary.txt"))
capture.output(summary(m_quad), file = file.path(out_dir, "stage1_quadratic_summary.txt"))

message("Wrote PAYOFF-B movement–phenology Stage-1 outputs to ", out_dir)
