#!/usr/bin/env Rscript

# PAYOFF-B macro reanalysis of Amaral et al. (2025)
# Data DOI: 10.5061/dryad.ttdz08m6w
#
# Primary estimand:
# location of the minimum phenological mismatch along
# log(bird migration-front speed / green-up-front speed).
#
# Important: this is a tracking-performance analysis, not a direct fitness
# estimate and not an identity between observed front speed and PAYOFF-B m*tau.

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

# Recompute lag from dates because upstream code and metadata disagree about
# the verbal sign of the stored lag field.
dat0$signed_lag <- dat0$arr_GAM_mean - dat0$gr_mn
dat0$abs_mismatch_days <- abs(dat0$signed_lag)

dat0$log_animal_speed <- log(dat0$vArrMag)
dat0$log_environment_speed <- log(dat0$vGrMag)
dat0$log_speed_ratio <- dat0$log_animal_speed - dat0$log_environment_speed
dat0$speed_ratio <- exp(dat0$log_speed_ratio)
# Orthogonal log-speed coordinate: geometric-mean speed scale.
dat0$log_speed_scale <- (dat0$log_animal_speed + dat0$log_environment_speed) / 2

# Source generating code stores rad2deg() output in vArrAng/vGrAng despite a
# data-dictionary label of radians.
dat0$alignment <- cos((dat0$vArrAng - dat0$vGrAng) * pi / 180)
dat0$vector_mismatch <- sqrt(
  pmax(0, 1 + dat0$speed_ratio^2 - 2 * dat0$speed_ratio * dat0$alignment)
)

# Within-cell green-up anomaly, recomputed directly from dates.
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

# Species x cell baseline phase offset. This asks whether speed matching
# minimizes departures from a population's usual relative-arrival phase rather
# than forcing all species to arrive exactly at vegetation mid-greenup.
dat0$species_cell_n <- ave(
  dat0$signed_lag,
  dat0$species_cell,
  FUN = function(z) sum(is.finite(z))
)
dat0$baseline_lag <- ave(
  dat0$signed_lag,
  dat0$species_cell,
  FUN = function(z) mean(z, na.rm = TRUE)
)
dat0$lag_deviation <- dat0$signed_lag - dat0$baseline_lag
dat0$abs_lag_deviation <- abs(dat0$lag_deviation)

keep <- with(
  dat0,
  is.finite(abs_mismatch_days) &
    is.finite(vArrMag) & is.finite(vGrMag) &
    vArrMag > 0 & vGrMag > 0 &
    vArrMag <= 3000 & vGrMag <= 3000 &
    is.finite(log_speed_ratio) &
    is.finite(log_speed_scale) &
    is.finite(alignment) &
    is.finite(cell_lat2) &
    is.finite(greenup_date_anom)
)
dat <- droplevels(dat0[keep, , drop = FALSE])
dat_centered <- droplevels(
  dat[is.finite(dat$abs_lag_deviation) & dat$species_cell_n >= 8, , drop = FALSE]
)

if (nrow(dat) < 100 || nrow(dat_centered) < 100) {
  stop("Too few complete observations after registered filters.")
}
if (length(unique(dat$species)) < 10) {
  stop("Too few species after registered filters.")
}

common_formula_terms <- paste(
  "s(log_speed_scale, k = 7)",
  "s(cell_lat2, k = 7)",
  "s(greenup_date_anom, k = 7)",
  "alignment",
  "mig_flag + breed_flag",
  "s(species, bs = 're')",
  "s(species_cell, bs = 're')",
  "s(year_f, bs = 're')",
  sep = " + "
)

full_formula <- as.formula(paste(
  "abs_mismatch_days ~",
  "s(log_speed_ratio, k = 7) +",
  common_formula_terms,
  "+ ti(log_speed_ratio, alignment, k = c(5, 5))"
))
null_formula <- as.formula(paste(
  "abs_mismatch_days ~",
  common_formula_terms
))
centered_full_formula <- as.formula(paste(
  "abs_lag_deviation ~",
  "s(log_speed_ratio, k = 7) +",
  common_formula_terms,
  "+ ti(log_speed_ratio, alignment, k = c(5, 5))"
))
centered_null_formula <- as.formula(paste(
  "abs_lag_deviation ~",
  common_formula_terms
))

m_gam <- bam(
  full_formula, data = dat, method = "fREML", discrete = TRUE
)
m_null <- bam(
  null_formula, data = dat, method = "fREML", discrete = TRUE
)
m_centered_gam <- bam(
  centered_full_formula, data = dat_centered, method = "fREML", discrete = TRUE
)
m_centered_null <- bam(
  centered_null_formula, data = dat_centered, method = "fREML", discrete = TRUE
)

m_quad <- bam(
  abs_mismatch_days ~
    log_speed_ratio + I(log_speed_ratio^2) +
    log_speed_scale +
    alignment + cell_lat2 + greenup_date_anom +
    mig_flag + breed_flag +
    s(species, bs = "re") +
    s(species_cell, bs = "re") +
    s(year_f, bs = "re"),
  data = dat, method = "fREML", discrete = TRUE
)

m_centered_quad <- bam(
  abs_lag_deviation ~
    log_speed_ratio + I(log_speed_ratio^2) +
    log_speed_scale +
    alignment + cell_lat2 + greenup_date_anom +
    mig_flag + breed_flag +
    s(species, bs = "re") +
    s(species_cell, bs = "re") +
    s(year_f, bs = "re"),
  data = dat_centered, method = "fREML", discrete = TRUE
)

quadratic_receipt <- function(model) {
  sm <- summary(model)
  ptab <- sm$p.table
  b1 <- unname(coef(model)[["log_speed_ratio"]])
  b2 <- unname(coef(model)[["I(log_speed_ratio^2)"]])
  status <- if (is.finite(b2) && b2 > 0) "FINITE_MINIMUM" else "NO_CONVEX_MINIMUM"
  q_star <- if (status == "FINITE_MINIMUM") -b1 / (2 * b2) else NA_real_
  data.frame(
    status = status,
    beta_q = b1,
    beta_q_se = unname(ptab["log_speed_ratio", "Std. Error"]),
    beta_q_p = unname(ptab["log_speed_ratio", "Pr(>|t|)"]),
    beta_q2 = b2,
    beta_q2_se = unname(ptab["I(log_speed_ratio^2)", "Std. Error"]),
    beta_q2_p = unname(ptab["I(log_speed_ratio^2)", "Pr(>|t|)"]),
    q_star = q_star,
    u_star = if (is.finite(q_star)) exp(q_star) else NA_real_
  )
}

quad_raw <- quadratic_receipt(m_quad)
quad_centered <- quadratic_receipt(m_centered_quad)

q_grid <- seq(
  as.numeric(quantile(dat$log_speed_ratio, 0.02, na.rm = TRUE)),
  as.numeric(quantile(dat$log_speed_ratio, 0.98, na.rm = TRUE)),
  length.out = 300
)

prediction_frame <- function(source, q, alignment_ref) {
  data.frame(
    log_speed_ratio = q,
    log_speed_scale = median(source$log_speed_scale, na.rm = TRUE),
    cell_lat2 = median(source$cell_lat2, na.rm = TRUE),
    greenup_date_anom = 0,
    alignment = alignment_ref,
    mig_flag = factor(levels(source$mig_flag)[1], levels = levels(source$mig_flag)),
    breed_flag = factor(levels(source$breed_flag)[1], levels = levels(source$breed_flag)),
    species = factor(levels(source$species)[1], levels = levels(source$species)),
    species_cell = factor(levels(source$species_cell)[1], levels = levels(source$species_cell)),
    year_f = factor(levels(source$year_f)[1], levels = levels(source$year_f))
  )
}

predict_curve <- function(model, source, response, alignment_ref, q) {
  nd <- prediction_frame(source, q, alignment_ref)
  pr <- predict(
    model,
    newdata = nd,
    type = "link",
    se.fit = TRUE,
    exclude = c("s(species)", "s(species_cell)", "s(year_f)")
  )
  data.frame(
    response = response,
    alignment_ref = alignment_ref,
    log_speed_ratio = q,
    speed_ratio = exp(q),
    fit = as.numeric(pr$fit),
    se = as.numeric(pr$se.fit)
  )
}

align_median <- median(dat$alignment, na.rm = TRUE)
curves <- rbind(
  predict_curve(m_gam, dat, "raw_abs_lag", align_median, q_grid),
  predict_curve(m_gam, dat, "raw_abs_lag", 1.0, q_grid),
  predict_curve(
    m_centered_gam, dat_centered, "centered_abs_lag",
    median(dat_centered$alignment, na.rm = TRUE), q_grid
  ),
  predict_curve(m_centered_gam, dat_centered, "centered_abs_lag", 1.0, q_grid)
)

curve_minimum <- function(df) {
  i <- which.min(df$fit)
  data.frame(
    response = df$response[i],
    alignment_ref = df$alignment_ref[i],
    q_star = df$log_speed_ratio[i],
    u_star = df$speed_ratio[i],
    fitted_minimum = df$fit[i]
  )
}
curve_groups <- split(
  curves,
  interaction(curves$response, curves$alignment_ref, drop = TRUE)
)
gam_minima <- do.call(rbind, lapply(curve_groups, curve_minimum))
row.names(gam_minima) <- NULL

checkpoint_u <- c(0.25, 0.375, 0.5, 0.75, 1.0, 1.60611529880277, 2.0, 4.0)
checkpoint_q <- log(checkpoint_u)
checkpoints <- do.call(
  rbind,
  list(
    predict_curve(m_gam, dat, "raw_abs_lag", 1.0, checkpoint_q),
    predict_curve(m_centered_gam, dat_centered, "centered_abs_lag", 1.0, checkpoint_q)
  )
)

smooth_receipt <- function(model, label) {
  sm <- summary(model)
  stab <- sm$s.table
  qrow <- grep("^s\\(log_speed_ratio", row.names(stab))
  tirow <- grep("^ti\\(log_speed_ratio", row.names(stab))
  data.frame(
    model = label,
    deviance_explained = sm$dev.expl,
    q_edf = if (length(qrow)) stab[qrow[1], "edf"] else NA_real_,
    q_p = if (length(qrow)) stab[qrow[1], ncol(stab)] else NA_real_,
    q_alignment_edf = if (length(tirow)) stab[tirow[1], "edf"] else NA_real_,
    q_alignment_p = if (length(tirow)) stab[tirow[1], ncol(stab)] else NA_real_
  )
}

gam_receipts <- rbind(
  smooth_receipt(m_gam, "raw_abs_lag"),
  smooth_receipt(m_centered_gam, "centered_abs_lag")
)

summary_row <- data.frame(
  n_rows = nrow(dat),
  n_centered_rows = nrow(dat_centered),
  n_species = length(unique(dat$species)),
  n_years = length(unique(dat$year)),
  median_signed_lag_days = median(dat$signed_lag, na.rm = TRUE),
  median_abs_mismatch_days = median(dat$abs_mismatch_days, na.rm = TRUE),
  median_speed_ratio = median(dat$speed_ratio, na.rm = TRUE),
  median_alignment = median(dat$alignment, na.rm = TRUE),
  raw_quadratic_status = quad_raw$status,
  raw_quadratic_u_star = quad_raw$u_star,
  centered_quadratic_status = quad_centered$status,
  centered_quadratic_u_star = quad_centered$u_star,
  delta_AIC_ratio_raw = AIC(m_null) - AIC(m_gam),
  delta_AIC_ratio_centered = AIC(m_centered_null) - AIC(m_centered_gam),
  payoff_b_strong_reference = 1.0,
  payoff_b_weak_reference = 1.60611529880277
)

write.csv(summary_row, file.path(out_dir, "stage1_summary.csv"), row.names = FALSE)
write.csv(curves, file.path(out_dir, "stage1_gam_curves.csv"), row.names = FALSE)
write.csv(gam_minima, file.path(out_dir, "stage1_gam_minima.csv"), row.names = FALSE)
write.csv(checkpoints, file.path(out_dir, "stage1_checkpoints.csv"), row.names = FALSE)
write.csv(
  cbind(response = "raw_abs_lag", quad_raw),
  file.path(out_dir, "stage1_quadratic_raw.csv"),
  row.names = FALSE
)
write.csv(
  cbind(response = "centered_abs_lag", quad_centered),
  file.path(out_dir, "stage1_quadratic_centered.csv"),
  row.names = FALSE
)
write.csv(gam_receipts, file.path(out_dir, "stage1_gam_receipts.csv"), row.names = FALSE)

saveRDS(m_gam, file.path(out_dir, "stage1_gam.rds"))
saveRDS(m_centered_gam, file.path(out_dir, "stage1_centered_gam.rds"))
saveRDS(m_quad, file.path(out_dir, "stage1_quadratic.rds"))
saveRDS(m_centered_quad, file.path(out_dir, "stage1_centered_quadratic.rds"))

capture.output(summary(m_gam), file = file.path(out_dir, "stage1_gam_summary.txt"))
capture.output(
  summary(m_centered_gam),
  file = file.path(out_dir, "stage1_centered_gam_summary.txt")
)
capture.output(summary(m_quad), file = file.path(out_dir, "stage1_quadratic_summary.txt"))
capture.output(
  summary(m_centered_quad),
  file = file.path(out_dir, "stage1_centered_quadratic_summary.txt")
)

message("Wrote PAYOFF-B movement–phenology Stage-1 outputs to ", out_dir)
