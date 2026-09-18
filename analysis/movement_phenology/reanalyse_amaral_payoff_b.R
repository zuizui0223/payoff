#!/usr/bin/env Rscript

# PAYOFF-B macro reanalysis of Amaral et al. (2025)
# Data DOI: 10.5061/dryad.ttdz08m6w

suppressPackageStartupMessages({
  library(dplyr)
  library(mgcv)
  library(readr)
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
      "Missing ", input_path, ". Download Amaral et al. (2025) Dryad package ",
      "(doi:10.5061/dryad.ttdz08m6w) and set PAYOFF_AMARAL_FINAL_RDS if needed."
    )
  )
}

dat0 <- readRDS(input_path)

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

dat <- dat0 %>%
  mutate(
    signed_lag = arr_GAM_mean - gr_mn,
    abs_mismatch_days = abs(signed_lag),
    speed_ratio = vArrMag / vGrMag,
    log_speed_ratio = log(speed_ratio),
    alignment = cos(vArrAng - vGrAng),
    vector_mismatch = sqrt(
      pmax(0, 1 + speed_ratio^2 - 2 * speed_ratio * alignment)
    ),
    species = factor(species),
    year_f = factor(year),
    species_cell = interaction(species, cell, drop = TRUE),
    range_type = case_when(
      mig_cell & breed_cell ~ "both",
      mig_cell ~ "mig",
      breed_cell ~ "breed",
      TRUE ~ "other"
    ),
    range_type = factor(range_type)
  ) %>%
  filter(
    is.finite(abs_mismatch_days),
    is.finite(vArrMag), is.finite(vGrMag),
    vArrMag > 0, vGrMag > 0,
    vArrMag <= 3000, vGrMag <= 3000,
    is.finite(log_speed_ratio),
    is.finite(alignment),
    is.finite(cell_lat2)
  )

if (nrow(dat) < 100) {
  stop("Too few complete observations after registered filters.")
}

m_gam <- gam(
  abs_mismatch_days ~
    s(log_speed_ratio, k = 7) +
    s(cell_lat2, k = 7) +
    alignment +
    ti(log_speed_ratio, alignment, k = c(5, 5)) +
    range_type +
    s(species, bs = "re") +
    s(species_cell, bs = "re") +
    s(year_f, bs = "re"),
  data = dat,
  method = "REML"
)

m_quad <- gam(
  abs_mismatch_days ~
    log_speed_ratio + I(log_speed_ratio^2) +
    alignment +
    cell_lat2 +
    range_type +
    s(species, bs = "re") +
    s(species_cell, bs = "re") +
    s(year_f, bs = "re"),
  data = dat,
  method = "REML"
)

co <- coef(m_quad)
b1 <- unname(co[["log_speed_ratio"]])
b2 <- unname(co[["I(log_speed_ratio^2)"]])

quad_status <- if (is.finite(b2) && b2 > 0) "FINITE_MINIMUM" else "NO_CONVEX_MINIMUM"
q_star <- if (quad_status == "FINITE_MINIMUM") -b1 / (2 * b2) else NA_real_
u_star <- if (is.finite(q_star)) exp(q_star) else NA_real_

summary_row <- tibble(
  n_rows = nrow(dat),
  n_species = n_distinct(dat$species),
  n_years = n_distinct(dat$year),
  median_speed_ratio = median(dat$speed_ratio, na.rm = TRUE),
  median_alignment = median(dat$alignment, na.rm = TRUE),
  quadratic_status = quad_status,
  quadratic_q_star = q_star,
  quadratic_u_macro_star = u_star,
  payoff_b_strong_reference = 1.0,
  payoff_b_weak_reference = 1.60611529880277
)

write_csv(summary_row, file.path(out_dir, "stage1_summary.csv"))
saveRDS(m_gam, file.path(out_dir, "stage1_gam.rds"))
saveRDS(m_quad, file.path(out_dir, "stage1_quadratic.rds"))

q_grid <- seq(
  quantile(dat$log_speed_ratio, 0.02, na.rm = TRUE),
  quantile(dat$log_speed_ratio, 0.98, na.rm = TRUE),
  length.out = 250
)

newdat <- data.frame(
  log_speed_ratio = q_grid,
  cell_lat2 = median(dat$cell_lat2, na.rm = TRUE),
  alignment = median(dat$alignment, na.rm = TRUE),
  range_type = levels(dat$range_type)[1],
  species = levels(dat$species)[1],
  species_cell = levels(dat$species_cell)[1],
  year_f = levels(dat$year_f)[1]
)

pred <- predict(
  m_gam,
  newdata = newdat,
  type = "link",
  se.fit = TRUE,
  exclude = c("s(species)", "s(species_cell)", "s(year_f)")
)

curve <- tibble(
  log_speed_ratio = q_grid,
  speed_ratio = exp(q_grid),
  fit_abs_mismatch_days = as.numeric(pred$fit),
  se = as.numeric(pred$se.fit)
)

write_csv(curve, file.path(out_dir, "stage1_gam_curve.csv"))
capture.output(summary(m_gam), file = file.path(out_dir, "stage1_gam_summary.txt"))
capture.output(summary(m_quad), file = file.path(out_dir, "stage1_quadratic_summary.txt"))

message("Wrote PAYOFF-B movement–phenology Stage-1 outputs to ", out_dir)
