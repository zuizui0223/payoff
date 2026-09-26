#!/usr/bin/env Rscript

# Frozen split-sample test of PAYOFF-B temporal buffering in the Amaral et al.
# bird dataset. Scientific contract:
# data/payoff_b_temporal_buffering_bird_holdout_registration_20260925.json
#
# Do not retune split, thresholds, response, primary interaction, or support gate
# after reading the result.

suppressPackageStartupMessages({
  library(mgcv)
})

input_path <- Sys.getenv(
  "PAYOFF_AMARAL_FINAL_RDS",
  "external/amaral_2025/data/final.rds"
)
out_dir <- "outputs/temporal_buffering_bird_holdout"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

MIN_CAL_OBS <- 60L
MIN_CAL_CELLS <- 5L
MIN_CAL_YEARS <- 5L
MIN_BASELINE_OBS <- 3L
MIN_ELIGIBLE_SPECIES <- 15L
MIN_HOLDOUT_ROWS <- 1000L
MIN_HOLDOUT_YEARS <- 5L
MAX_SPEED <- 3000
MAX_P <- 0.05

if (!file.exists(input_path)) {
  stop("Missing pinned Amaral final.rds")
}

dat0 <- as.data.frame(readRDS(input_path))

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

as_flag <- function(x) {
  if (is.logical(x)) {
    out <- x
  } else {
    out <- tolower(trimws(as.character(x))) %in% c("true", "t", "1", "yes")
  }
  out[is.na(out)] <- FALSE
  out
}

# Chronological split frozen in the registration.
years <- sort(unique(dat0$year[is.finite(dat0$year)]))
n_years <- length(years)
n_cal <- floor(n_years / 2)
cal_years <- years[seq_len(n_cal)]
hold_years <- years[(n_cal + 1L):n_years]

# ----------------------------
# Calibration-only timing gain
# ----------------------------

cal <- dat0[
  dat0$year %in% cal_years &
    is.finite(dat0$arr_GAM_mean) &
    is.finite(dat0$gr_mn),
  ,
  drop = FALSE
]
cal$species <- as.character(cal$species)
cal$cell <- as.character(cal$cell)

arrival_base <- aggregate(
  arr_GAM_mean ~ species + cell,
  data = cal,
  FUN = mean
)
names(arrival_base)[names(arrival_base) == "arr_GAM_mean"] <- "arrival_baseline"

# Remove species replication before averaging the environmental baseline.
green_cell_year <- aggregate(
  gr_mn ~ cell + year,
  data = cal,
  FUN = mean
)
green_base <- aggregate(
  gr_mn ~ cell,
  data = green_cell_year,
  FUN = mean
)
names(green_base)[names(green_base) == "gr_mn"] <- "greenup_baseline"

cal <- merge(cal, arrival_base, by = c("species", "cell"), all.x = TRUE)
cal <- merge(cal, green_base, by = "cell", all.x = TRUE)
cal$arrival_anomaly <- cal$arr_GAM_mean - cal$arrival_baseline
cal$greenup_anomaly <- cal$gr_mn - cal$greenup_baseline

species_gain <- do.call(
  rbind,
  lapply(sort(unique(cal$species)), function(sp) {
    d <- cal[
      cal$species == sp &
        is.finite(cal$arrival_anomaly) &
        is.finite(cal$greenup_anomaly),
      ,
      drop = FALSE
    ]
    n_obs <- nrow(d)
    n_cells <- length(unique(d$cell))
    n_years_sp <- length(unique(d$year))
    count_gate <- (
      n_obs >= MIN_CAL_OBS &&
        n_cells >= MIN_CAL_CELLS &&
        n_years_sp >= MIN_CAL_YEARS
    )
    slope <- NA_real_
    slope_se <- NA_real_
    slope_p <- NA_real_
    if (count_gate && sd(d$greenup_anomaly, na.rm = TRUE) > 0) {
      fit <- tryCatch(
        lm(arrival_anomaly ~ greenup_anomaly, data = d),
        error = function(e) NULL
      )
      if (!is.null(fit)) {
        cf <- summary(fit)$coefficients
        if ("greenup_anomaly" %in% rownames(cf)) {
          slope <- unname(cf["greenup_anomaly", "Estimate"])
          slope_se <- unname(cf["greenup_anomaly", "Std. Error"])
          slope_p <- unname(cf["greenup_anomaly", "Pr(>|t|)"])
        }
      }
    }
    data.frame(
      species = sp,
      n_calibration = n_obs,
      n_calibration_cells = n_cells,
      n_calibration_years = n_years_sp,
      count_gate = count_gate,
      timing_gain = slope,
      timing_gain_se = slope_se,
      timing_gain_p = slope_p,
      eligible = count_gate && is.finite(slope),
      stringsAsFactors = FALSE
    )
  })
)
row.names(species_gain) <- NULL

eligible_gain <- species_gain[species_gain$eligible, , drop = FALSE]
timing_gain_sd <- if (nrow(eligible_gain) > 1L) {
  sd(eligible_gain$timing_gain, na.rm = TRUE)
} else {
  NA_real_
}
timing_gain_mean <- if (nrow(eligible_gain) > 0L) {
  mean(eligible_gain$timing_gain, na.rm = TRUE)
} else {
  NA_real_
}

if (is.finite(timing_gain_sd) && timing_gain_sd > 0) {
  eligible_gain$z_timing_gain <- (
    eligible_gain$timing_gain - timing_gain_mean
  ) / timing_gain_sd
} else {
  eligible_gain$z_timing_gain <- NA_real_
}

write.csv(
  species_gain,
  file.path(out_dir, "temporal_buffering_timing_gain_species.csv"),
  row.names = FALSE
)

# ----------------------------
# Calibration phase baselines
# ----------------------------

cal$signed_lag <- cal$arr_GAM_mean - cal$gr_mn
lag_mean <- aggregate(
  signed_lag ~ species + cell,
  data = cal,
  FUN = mean
)
lag_n <- aggregate(
  signed_lag ~ species + cell,
  data = cal,
  FUN = length
)
names(lag_mean)[names(lag_mean) == "signed_lag"] <- "baseline_lag"
names(lag_n)[names(lag_n) == "signed_lag"] <- "baseline_n"
lag_base <- merge(lag_mean, lag_n, by = c("species", "cell"))
lag_base <- lag_base[
  lag_base$baseline_n >= MIN_BASELINE_OBS,
  ,
  drop = FALSE
]

# ----------------------------
# Holdout response and inputs
# ----------------------------

hold <- dat0[dat0$year %in% hold_years, , drop = FALSE]
hold$species <- as.character(hold$species)
hold$cell <- as.character(hold$cell)
hold <- merge(hold, lag_base, by = c("species", "cell"), all.x = TRUE)
hold <- merge(
  hold,
  eligible_gain[, c("species", "timing_gain", "z_timing_gain"), drop = FALSE],
  by = "species",
  all.x = TRUE
)
hold <- merge(hold, green_base, by = "cell", all.x = TRUE)

hold$signed_lag <- hold$arr_GAM_mean - hold$gr_mn
hold$lag_deviation_holdout <- hold$signed_lag - hold$baseline_lag
hold$abs_lag_deviation_holdout <- abs(hold$lag_deviation_holdout)
hold$log_animal_speed <- log(hold$vArrMag)
hold$log_environment_speed <- log(hold$vGrMag)
hold$log_speed_ratio <- hold$log_animal_speed - hold$log_environment_speed
hold$log_speed_scale <- (
  hold$log_animal_speed + hold$log_environment_speed
) / 2
hold$alignment <- cos((hold$vArrAng - hold$vGrAng) * pi / 180)
hold$greenup_date_anom_from_calibration <- hold$gr_mn - hold$greenup_baseline
hold$mig_flag <- factor(as_flag(hold$mig_cell))
hold$breed_flag <- factor(as_flag(hold$breed_cell))

keep <- with(
  hold,
  is.finite(abs_lag_deviation_holdout) &
    is.finite(vArrMag) & is.finite(vGrMag) &
    vArrMag > 0 & vGrMag > 0 &
    vArrMag <= MAX_SPEED & vGrMag <= MAX_SPEED &
    is.finite(log_speed_ratio) &
    is.finite(log_speed_scale) &
    is.finite(z_timing_gain) &
    is.finite(alignment) &
    is.finite(cell_lat2) &
    is.finite(greenup_date_anom_from_calibration) &
    is.finite(baseline_lag)
)
hold <- hold[keep, , drop = FALSE]
hold$species <- factor(hold$species)
hold$species_cell <- interaction(hold$species, hold$cell, drop = TRUE)
hold$year_f <- factor(hold$year)

holdout_count_by_year <- as.data.frame(table(hold$year), stringsAsFactors = FALSE)
names(holdout_count_by_year) <- c("year", "n_rows")
write.csv(
  holdout_count_by_year,
  file.path(out_dir, "temporal_buffering_holdout_counts_by_year.csv"),
  row.names = FALSE
)

n_holdout_rows <- nrow(hold)
n_holdout_species <- length(unique(hold$species))
n_holdout_years <- length(unique(hold$year))

estimability_reasons <- character()
if (n_holdout_species < MIN_ELIGIBLE_SPECIES) {
  estimability_reasons <- c(
    estimability_reasons,
    paste0("eligible_holdout_species<", MIN_ELIGIBLE_SPECIES)
  )
}
if (n_holdout_rows < MIN_HOLDOUT_ROWS) {
  estimability_reasons <- c(
    estimability_reasons,
    paste0("holdout_rows<", MIN_HOLDOUT_ROWS)
  )
}
if (n_holdout_years < MIN_HOLDOUT_YEARS) {
  estimability_reasons <- c(
    estimability_reasons,
    paste0("holdout_years<", MIN_HOLDOUT_YEARS)
  )
}
if (!is.finite(timing_gain_sd) || timing_gain_sd <= 0) {
  estimability_reasons <- c(
    estimability_reasons,
    "timing_gain_sd_not_positive"
  )
}

primary_table <- data.frame(
  term = "I(log_speed_ratio^2):z_timing_gain",
  estimate = NA_real_,
  std_error = NA_real_,
  statistic = NA_real_,
  p_value = NA_real_,
  status = "NOT_ESTIMABLE",
  stringsAsFactors = FALSE
)
curves <- data.frame(
  z_timing_gain = numeric(),
  log_speed_ratio = numeric(),
  speed_ratio = numeric(),
  fit = numeric(),
  se = numeric()
)
curvature <- data.frame(
  z_timing_gain = c(-1, 1),
  implied_quadratic_curvature = NA_real_
)

fit_model <- NULL
if (length(estimability_reasons) == 0L) {
  formula_primary <- abs_lag_deviation_holdout ~
    log_speed_ratio +
    I(log_speed_ratio^2) +
    z_timing_gain +
    log_speed_ratio:z_timing_gain +
    I(log_speed_ratio^2):z_timing_gain +
    log_speed_scale +
    alignment +
    cell_lat2 +
    greenup_date_anom_from_calibration +
    mig_flag + breed_flag +
    s(species, bs = "re") +
    s(species_cell, bs = "re") +
    s(year_f, bs = "re")

  fit_model <- tryCatch(
    bam(
      formula_primary,
      data = hold,
      method = "fREML",
      discrete = TRUE
    ),
    error = function(e) {
      estimability_reasons <<- c(
        estimability_reasons,
        paste0("model_fit_error:", conditionMessage(e))
      )
      NULL
    }
  )
}

result_status <- "NOT_ESTIMABLE"
primary_term <- "I(log_speed_ratio^2):z_timing_gain"

if (!is.null(fit_model) && length(estimability_reasons) == 0L) {
  ptab <- summary(fit_model)$p.table
  term <- if (primary_term %in% rownames(ptab)) {
    primary_term
  } else {
    reverse_term <- "z_timing_gain:I(log_speed_ratio^2)"
    if (reverse_term %in% rownames(ptab)) reverse_term else NA_character_
  }

  if (is.na(term)) {
    estimability_reasons <- c(
      estimability_reasons,
      "primary_interaction_term_missing"
    )
  } else {
    estimate <- unname(ptab[term, "Estimate"])
    std_error <- unname(ptab[term, "Std. Error"])
    statistic <- unname(ptab[term, "t value"])
    p_value <- unname(ptab[term, "Pr(>|t|)"])

    if (is.finite(estimate) && is.finite(p_value)) {
      if (estimate < 0 && p_value < MAX_P) {
        result_status <- "PASS"
      } else if (estimate >= 0) {
        result_status <- "FAIL_WRONG_DIRECTION"
      } else {
        result_status <- "FAIL_INSUFFICIENT_SUPPORT"
      }
      primary_table <- data.frame(
        term = primary_term,
        estimate = estimate,
        std_error = std_error,
        statistic = statistic,
        p_value = p_value,
        status = result_status,
        stringsAsFactors = FALSE
      )

      co <- coef(fit_model)
      b2 <- unname(co[["I(log_speed_ratio^2)"]])
      b2t <- if (primary_term %in% names(co)) {
        unname(co[[primary_term]])
      } else {
        unname(co[["z_timing_gain:I(log_speed_ratio^2)"]])
      }
      curvature$implied_quadratic_curvature <- b2 + b2t * curvature$z_timing_gain

      q_grid <- seq(
        as.numeric(quantile(hold$log_speed_ratio, 0.02, na.rm = TRUE)),
        as.numeric(quantile(hold$log_speed_ratio, 0.98, na.rm = TRUE)),
        length.out = 200
      )
      predict_one <- function(z) {
        nd <- data.frame(
          log_speed_ratio = q_grid,
          z_timing_gain = z,
          log_speed_scale = median(hold$log_speed_scale, na.rm = TRUE),
          alignment = median(hold$alignment, na.rm = TRUE),
          cell_lat2 = median(hold$cell_lat2, na.rm = TRUE),
          greenup_date_anom_from_calibration = 0,
          mig_flag = factor(levels(hold$mig_flag)[1], levels = levels(hold$mig_flag)),
          breed_flag = factor(levels(hold$breed_flag)[1], levels = levels(hold$breed_flag)),
          species = factor(levels(hold$species)[1], levels = levels(hold$species)),
          species_cell = factor(levels(hold$species_cell)[1], levels = levels(hold$species_cell)),
          year_f = factor(levels(hold$year_f)[1], levels = levels(hold$year_f))
        )
        pr <- predict(
          fit_model,
          newdata = nd,
          type = "link",
          se.fit = TRUE,
          exclude = c("s(species)", "s(species_cell)", "s(year_f)")
        )
        data.frame(
          z_timing_gain = z,
          log_speed_ratio = q_grid,
          speed_ratio = exp(q_grid),
          fit = as.numeric(pr$fit),
          se = as.numeric(pr$se.fit)
        )
      }
      curves <- do.call(rbind, lapply(c(-1, 0, 1), predict_one))
    } else {
      estimability_reasons <- c(
        estimability_reasons,
        "primary_interaction_nonfinite"
      )
    }
  }
}

if (length(estimability_reasons) > 0L) {
  result_status <- "NOT_ESTIMABLE"
  primary_table$status <- result_status
}

write.csv(
  primary_table,
  file.path(out_dir, "temporal_buffering_holdout_primary.csv"),
  row.names = FALSE
)
write.csv(
  curvature,
  file.path(out_dir, "temporal_buffering_holdout_curvature.csv"),
  row.names = FALSE
)
write.csv(
  curves,
  file.path(out_dir, "temporal_buffering_holdout_curves.csv"),
  row.names = FALSE
)

if (!is.null(fit_model)) {
  capture.output(
    summary(fit_model),
    file = file.path(out_dir, "temporal_buffering_holdout_model_summary.txt")
  )
}

# Minimal dependency-free JSON serialization for the machine receipt.
json_value <- function(x) {
  if (is.null(x)) return("null")
  if (length(x) == 1L && is.na(x)) return("null")
  if (is.logical(x) && length(x) == 1L) return(tolower(as.character(x)))
  if (is.numeric(x) && length(x) == 1L) {
    if (!is.finite(x)) return("null")
    return(format(x, digits = 16, scientific = FALSE, trim = TRUE))
  }
  if (is.character(x) && length(x) == 1L) {
    y <- gsub("\\\\", "\\\\\\\\", x)
    y <- gsub('"', '\\\\"', y, fixed = TRUE)
    return(paste0('"', y, '"'))
  }
  if (is.atomic(x)) {
    return(
      paste0(
        "[",
        paste(vapply(as.list(x), json_value, ""), collapse = ","),
        "]"
      )
    )
  }
  if (is.list(x) && !is.null(names(x))) {
    parts <- mapply(
      function(n, v) paste0('"', n, '":', json_value(v)),
      names(x), x,
      SIMPLIFY = TRUE,
      USE.NAMES = FALSE
    )
    return(paste0("{", paste(parts, collapse = ","), "}"))
  }
  stop("Unsupported JSON value")
}

receipt <- list(
  registration_id = "payoff_b_temporal_buffering_bird_holdout_v1_20260925",
  status = result_status,
  outcome_opened = TRUE,
  split = list(
    calibration_years = as.integer(cal_years),
    holdout_years = as.integer(hold_years)
  ),
  calibration = list(
    n_species_timing_gain_eligible = nrow(eligible_gain),
    timing_gain_mean = timing_gain_mean,
    timing_gain_sd = timing_gain_sd
  ),
  holdout = list(
    n_rows = n_holdout_rows,
    n_species = n_holdout_species,
    n_years = n_holdout_years
  ),
  estimability_reasons = estimability_reasons,
  primary = list(
    term = primary_term,
    estimate = primary_table$estimate[1],
    std_error = primary_table$std_error[1],
    statistic = primary_table$statistic[1],
    p_value = primary_table$p_value[1],
    expected_direction = "negative",
    max_p_value = MAX_P
  ),
  retuning_permitted = FALSE
)

writeLines(
  json_value(receipt),
  file.path(out_dir, "temporal_buffering_bird_holdout_result.json")
)

cat("PAYOFF-B temporal-buffering bird holdout\n")
cat("status:", result_status, "\n")
cat("calibration years:", paste(cal_years, collapse = ","), "\n")
cat("holdout years:", paste(hold_years, collapse = ","), "\n")
cat("eligible timing-gain species:", nrow(eligible_gain), "\n")
cat("holdout rows:", n_holdout_rows, "\n")
cat("holdout species:", n_holdout_species, "\n")
cat("holdout years:", n_holdout_years, "\n")
if (length(estimability_reasons)) {
  cat("estimability reasons:", paste(estimability_reasons, collapse = ";"), "\n")
}
print(primary_table)
