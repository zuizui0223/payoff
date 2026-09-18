#!/usr/bin/env Rscript

# Exploratory species-level moderators of PAYOFF-B movement–phenology matching.
# This script is explicitly secondary: it explains heterogeneity in the Stage-1
# species diagnostics and does not promote any trait association to a causal claim.

input_path <- Sys.getenv(
  "PAYOFF_AMARAL_FINAL_RDS",
  "external/amaral_2025/data/final.rds"
)
out_dir <- "outputs/movement_phenology"
vertices_path <- file.path(out_dir, "stage1_species_vertices.csv")

if (!file.exists(input_path)) stop(paste("Missing Stage-1 data:", input_path))
if (!file.exists(vertices_path)) stop(paste("Missing species vertices:", vertices_path))

dat0 <- as.data.frame(readRDS(input_path))
vertices <- read.csv(vertices_path, stringsAsFactors = FALSE)

needed <- c(
  "species", "cell", "year", "gr_mn", "arr_GAM_mean", "vArrAng", "vGrAng",
  "HWI", "Body_mass_g", "winlat", "sensi_mean", "Time", "Diet"
)
missing <- setdiff(needed, names(dat0))
if (length(missing) > 0L) {
  stop(paste("Missing trait columns:", paste(missing, collapse = ", ")))
}

first_non_missing <- function(x) {
  y <- x[!is.na(x)]
  if (length(y) == 0L) return(NA)
  y[1]
}

species_levels <- unique(as.character(dat0$species))

median_cell_sd <- function(values, cells) {
  ok <- is.finite(values) & !is.na(cells)
  values <- values[ok]
  cells <- cells[ok]
  if (length(values) == 0L) return(NA_real_)
  spl <- split(values, cells)
  sds <- vapply(
    spl,
    function(z) if (length(z) >= 4L) sd(z, na.rm = TRUE) else NA_real_,
    numeric(1)
  )
  sds <- sds[is.finite(sds)]
  if (length(sds) == 0L) NA_real_ else median(sds)
}

circular_concentration_deg <- function(angle_deg) {
  a <- angle_deg[is.finite(angle_deg)] * pi / 180
  if (length(a) == 0L) return(NA_real_)
  sqrt(mean(cos(a))^2 + mean(sin(a))^2)
}

species_geometry <- function(d) {
  alignment <- cos((d$vArrAng - d$vGrAng) * pi / 180)
  list(
    mean_alignment = if (any(is.finite(alignment))) mean(alignment[is.finite(alignment)]) else NA_real_,
    median_alignment = if (any(is.finite(alignment))) median(alignment[is.finite(alignment)]) else NA_real_,
    route_direction_concentration = circular_concentration_deg(d$vArrAng),
    greenup_direction_concentration = circular_concentration_deg(d$vGrAng),
    greenup_interannual_sd = median_cell_sd(d$gr_mn, d$cell),
    arrival_interannual_sd = median_cell_sd(d$arr_GAM_mean, d$cell)
  )
}

traits <- do.call(
  rbind,
  lapply(species_levels, function(sp) {
    d <- dat0[as.character(dat0$species) == sp, , drop = FALSE]
    g <- species_geometry(d)
    data.frame(
      species = sp,
      HWI = suppressWarnings(as.numeric(first_non_missing(d$HWI))),
      Body_mass_g = suppressWarnings(as.numeric(first_non_missing(d$Body_mass_g))),
      winlat = suppressWarnings(as.numeric(first_non_missing(d$winlat))),
      sensi_mean = suppressWarnings(as.numeric(first_non_missing(d$sensi_mean))),
      Time = as.character(first_non_missing(d$Time)),
      Diet = as.character(first_non_missing(d$Diet)),
      mean_alignment = g$mean_alignment,
      median_alignment = g$median_alignment,
      route_direction_concentration = g$route_direction_concentration,
      greenup_direction_concentration = g$greenup_direction_concentration,
      greenup_interannual_sd = g$greenup_interannual_sd,
      arrival_interannual_sd = g$arrival_interannual_sd,
      stringsAsFactors = FALSE
    )
  })
)

x <- merge(vertices, traits, by = "species", all.x = TRUE)
x$log_body_mass <- ifelse(
  is.finite(x$Body_mass_g) & x$Body_mass_g > 0,
  log(x$Body_mass_g),
  NA_real_
)
x$abs_winlat <- abs(x$winlat)
x$internal_finite_optimum <- with(
  x,
  is.finite(u_star) &
    beta_q2 > 0 &
    vertex_inside_5_95
)

write.csv(
  x,
  file.path(out_dir, "stage1_trait_species.csv"),
  row.names = FALSE
)

continuous <- c(
  "HWI",
  "log_body_mass",
  "abs_winlat",
  "sensi_mean",
  "mean_alignment",
  "route_direction_concentration",
  "greenup_direction_concentration",
  "greenup_interannual_sd",
  "arrival_interannual_sd"
)

fit_linear <- function(response, trait, data) {
  d <- data[
    is.finite(data[[response]]) & is.finite(data[[trait]]),
    ,
    drop = FALSE
  ]
  if (nrow(d) < 12L || sd(d[[trait]]) == 0) return(NULL)
  z <- as.numeric(scale(d[[trait]]))
  fit <- lm(d[[response]] ~ z)
  cf <- summary(fit)$coefficients
  data.frame(
    response = response,
    trait = trait,
    model = "linear_per_trait_sd",
    n = nrow(d),
    estimate = unname(cf["z", "Estimate"]),
    std_error = unname(cf["z", "Std. Error"]),
    statistic = unname(cf["z", "t value"]),
    p_value = unname(cf["z", "Pr(>|t|)"]),
    effect_scale = "response_units_per_1SD_trait",
    stringsAsFactors = FALSE
  )
}

fit_logistic <- function(trait, data) {
  d <- data[
    !is.na(data$internal_finite_optimum) & is.finite(data[[trait]]),
    ,
    drop = FALSE
  ]
  if (
    nrow(d) < 20L ||
    sd(d[[trait]]) == 0 ||
    length(unique(d$internal_finite_optimum)) < 2L
  ) return(NULL)
  z <- as.numeric(scale(d[[trait]]))
  fit <- suppressWarnings(glm(
    as.integer(d$internal_finite_optimum) ~ z,
    family = binomial()
  ))
  cf <- summary(fit)$coefficients
  if (!("z" %in% rownames(cf))) return(NULL)
  data.frame(
    response = "internal_finite_optimum",
    trait = trait,
    model = "logistic_per_trait_sd",
    n = nrow(d),
    estimate = exp(unname(cf["z", "Estimate"])),
    std_error = unname(cf["z", "Std. Error"]),
    statistic = unname(cf["z", "z value"]),
    p_value = unname(cf["z", "Pr(>|z|)"]),
    effect_scale = "odds_ratio_per_1SD_trait",
    stringsAsFactors = FALSE
  )
}

fit_vertex <- function(trait, data) {
  d <- data[
    data$internal_finite_optimum &
      is.finite(data$u_star) &
      data$u_star > 0 &
      is.finite(data[[trait]]),
    ,
    drop = FALSE
  ]
  if (nrow(d) < 8L || sd(d[[trait]]) == 0) return(NULL)
  z <- as.numeric(scale(d[[trait]]))
  fit <- lm(log(d$u_star) ~ z)
  cf <- summary(fit)$coefficients
  data.frame(
    response = "log_internal_u_star",
    trait = trait,
    model = "linear_per_trait_sd",
    n = nrow(d),
    estimate = unname(cf["z", "Estimate"]),
    std_error = unname(cf["z", "Std. Error"]),
    statistic = unname(cf["z", "t value"]),
    p_value = unname(cf["z", "Pr(>|t|)"]),
    effect_scale = "log_u_star_per_1SD_trait",
    stringsAsFactors = FALSE
  )
}

rows <- list()
for (trait in continuous) {
  rows[[length(rows) + 1L]] <- fit_linear("beta_q2", trait, x)
  rows[[length(rows) + 1L]] <- fit_logistic(trait, x)
  rows[[length(rows) + 1L]] <- fit_vertex(trait, x)
}
rows <- rows[!vapply(rows, is.null, logical(1))]

if (length(rows) > 0L) {
  assoc <- do.call(rbind, rows)
} else {
  assoc <- data.frame(
    response = character(),
    trait = character(),
    model = character(),
    n = integer(),
    estimate = numeric(),
    std_error = numeric(),
    statistic = numeric(),
    p_value = numeric(),
    effect_scale = character()
  )
}

assoc <- assoc[order(assoc$p_value), , drop = FALSE]
assoc$fdr_bh <- p.adjust(assoc$p_value, method = "BH")

write.csv(
  assoc,
  file.path(out_dir, "stage1_trait_moderator_associations.csv"),
  row.names = FALSE
)

summary_row <- data.frame(
  n_species_with_vertices = nrow(x),
  n_internal_finite_optima = sum(x$internal_finite_optimum, na.rm = TRUE),
  n_HWI = sum(is.finite(x$HWI)),
  n_body_mass = sum(is.finite(x$log_body_mass)),
  n_abs_winlat = sum(is.finite(x$abs_winlat)),
  n_sensi_mean = sum(is.finite(x$sensi_mean)),
  n_mean_alignment = sum(is.finite(x$mean_alignment)),
  n_route_direction_concentration = sum(is.finite(x$route_direction_concentration)),
  n_greenup_interannual_sd = sum(is.finite(x$greenup_interannual_sd)),
  smallest_p = if (nrow(assoc)) min(assoc$p_value, na.rm = TRUE) else NA_real_,
  smallest_fdr_bh = if (nrow(assoc)) min(assoc$fdr_bh, na.rm = TRUE) else NA_real_
)

write.csv(
  summary_row,
  file.path(out_dir, "stage1_trait_moderator_summary.csv"),
  row.names = FALSE
)

cat("PAYOFF-B Stage-1 trait moderator summary\n")
print(summary_row)
if (nrow(assoc)) print(head(assoc, 10))
