#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

SOURCE_COMMIT <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL <- paste0(
  "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
  SOURCE_COMMIT,
  "/data/final.rds"
)
MIN_PAIRS <- 6L
BOOT_REPS <- 3000L
BOOT_SEED <- 20261005L

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
cache <- "outputs/amaral_final_frozen.rds"
if (!file.exists(cache)) {
  download.file(SOURCE_URL, cache, mode = "wb", quiet = FALSE)
}
dat <- readRDS(cache)

truthy <- function(x) {
  toupper(as.character(x)) %in% c("TRUE", "T", "1")
}

haversine_km <- function(lat1, lon1, lat2, lon2) {
  rad <- pi / 180
  p1 <- lat1 * rad
  p2 <- lat2 * rad
  dp <- (lat2 - lat1) * rad
  dl <- (lon2 - lon1) * rad
  a <- sin(dp / 2)^2 + cos(p1) * cos(p2) * sin(dl / 2)^2
  6371.0088 * 2 * atan2(sqrt(a), sqrt(pmax(0, 1 - a)))
}

window_stats <- function(green, source_cell, target_cell, start_year, end_year) {
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
  names(source)[2] <- "origin"
  names(target)[2] <- "destination"
  paired <- merge(source, target, by = "year", all = FALSE)
  paired <- paired[
    is.finite(paired$year) &
      is.finite(paired$origin) &
      is.finite(paired$destination),
  ]
  if (nrow(paired) < MIN_PAIRS) {
    return(list(rho = NA_real_, raw = NA_real_, n = nrow(paired)))
  }
  if (length(unique(paired$year)) != nrow(paired)) {
    stop("Duplicate year within source-target pair")
  }
  raw <- if (sd(paired$origin) > 0 && sd(paired$destination) > 0) {
    cor(paired$origin, paired$destination)
  } else NA_real_
  ro <- resid(lm(origin ~ year, data = paired))
  rd <- resid(lm(destination ~ year, data = paired))
  rho <- if (sd(ro) > 0 && sd(rd) > 0) cor(ro, rd) else NA_real_
  list(rho = rho, raw = raw, n = nrow(paired))
}

make_mapping <- function(dat) {
  cells <- unique(dat[, c(
    "species", "cell", "cell_lat2", "cell_lng", "mig_cell", "breed_cell"
  )])
  cells$cell <- as.numeric(as.character(cells$cell))
  cells$cell_lat2 <- as.numeric(cells$cell_lat2)
  cells$cell_lng <- as.numeric(cells$cell_lng)
  cells$is_mig <- truthy(cells$mig_cell)
  cells$is_breed <- truthy(cells$breed_cell)
  targets <- cells[
    cells$is_breed &
      is.finite(cells$cell_lat2) &
      is.finite(cells$cell_lng),
    c("species", "cell", "cell_lat2", "cell_lng")
  ]
  targets <- targets[order(targets$species, targets$cell), ]
  out <- vector("list", nrow(targets))
  k <- 0L
  for (i in seq_len(nrow(targets))) {
    t <- targets[i, ]
    candidates <- cells[
      cells$species == t$species &
        cells$is_mig &
        is.finite(cells$cell_lat2) &
        is.finite(cells$cell_lng) &
        cells$cell_lat2 < t$cell_lat2,
      c("cell", "cell_lat2", "cell_lng")
    ]
    if (nrow(candidates) == 0) next
    candidates$distance_km <- haversine_km(
      candidates$cell_lat2, candidates$cell_lng,
      t$cell_lat2, t$cell_lng
    )
    candidates <- candidates[order(candidates$distance_km, candidates$cell), ]
    src <- candidates[1, ]
    k <- k + 1L
    out[[k]] <- data.frame(
      species = as.character(t$species),
      target_cell = as.numeric(t$cell),
      source_cell = as.numeric(src$cell),
      distance_km = as.numeric(src$distance_km)
    )
  }
  do.call(rbind, out[seq_len(k)])
}

green <- unique(dat[, c("year", "cell", "gr_mn")])
green$year <- as.integer(green$year)
green$cell <- as.numeric(as.character(green$cell))
green$gr_mn <- as.numeric(green$gr_mn)
green <- green[
  is.finite(green$year) &
    is.finite(green$cell) &
    is.finite(green$gr_mn),
]
mapping <- make_mapping(dat)

calc_windows <- function(mapping, early_start, early_end, late_start, late_end) {
  out <- vector("list", nrow(mapping))
  for (i in seq_len(nrow(mapping))) {
    m <- mapping[i, ]
    e <- window_stats(
      green, m$source_cell, m$target_cell, early_start, early_end
    )
    l <- window_stats(
      green, m$source_cell, m$target_cell, late_start, late_end
    )
    out[[i]] <- data.frame(
      species = m$species,
      target_cell = m$target_cell,
      source_cell = m$source_cell,
      distance_km = m$distance_km,
      early_n = e$n,
      late_n = l$n,
      early_rho = e$rho,
      late_rho = l$rho,
      delta_rho = l$rho - e$rho,
      early_raw = e$raw,
      late_raw = l$raw,
      delta_raw = l$raw - e$raw
    )
  }
  x <- do.call(rbind, out)
  x[
    is.finite(x$early_rho) &
      is.finite(x$late_rho) &
      x$early_n >= MIN_PAIRS &
      x$late_n >= MIN_PAIRS,
  ]
}

primary <- calc_windows(mapping, 2002L, 2009L, 2010L, 2017L)

cluster_boot_ci <- function(x, reps = BOOT_REPS) {
  set.seed(BOOT_SEED)
  spp <- unique(x$species)
  vals <- replicate(reps, {
    samp <- sample(spp, length(spp), replace = TRUE)
    idx <- unlist(lapply(samp, function(sp) which(x$species == sp)))
    mean(x$delta_rho[idx])
  })
  as.numeric(quantile(vals, c(0.025, 0.975), names = FALSE))
}

clamp <- function(x) pmax(-0.999, pmin(0.999, x))
primary$delta_fisher_z <-
  atanh(clamp(primary$late_rho)) - atanh(clamp(primary$early_rho))

exact8 <- primary[primary$early_n == 8 & primary$late_n == 8, ]
alt7 <- calc_windows(mapping, 2002L, 2008L, 2011L, 2017L)

species_primary <- aggregate(delta_rho ~ species, primary, mean)

if (!requireNamespace("nlme", quietly = TRUE)) stop("nlme is required")
primary$z_log_distance <- as.numeric(scale(log1p(primary$distance_km)))
dist_fit <- nlme::lme(
  delta_rho ~ z_log_distance,
  random = ~1 | species,
  data = primary,
  method = "REML",
  na.action = na.fail,
  control = nlme::lmeControl(returnObject = TRUE)
)
dist_tab <- summary(dist_fit)$tTable
distance_est <- unname(dist_tab["z_log_distance", "Value"])
distance_se <- unname(dist_tab["z_log_distance", "Std.Error"])
distance_p <- unname(dist_tab["z_log_distance", "p-value"])

loo <- lapply(unique(primary$species), function(sp) {
  sub <- primary[primary$species != sp, ]
  data.frame(
    left_out_species = sp,
    pair_mean_delta_rho = mean(sub$delta_rho),
    species_equal_weight_mean = mean(
      aggregate(delta_rho ~ species, sub, mean)$delta_rho
    )
  )
})
loo <- do.call(rbind, loo)

candidate_mig_cols <- c(
  "migDist", "mig_dist", "migration_distance", "migrationDist",
  "MigDist", "migDistance", "migration_distance_km"
)
mig_cols <- intersect(candidate_mig_cols, names(dat))

summary <- data.frame(
  sensitivity = c(
    "primary_fisher_z",
    "exact_complete_8year",
    "species_equal_weight",
    "distance_moderator",
    "raw_undetrended_negative_control",
    "alternative_7year_windows",
    "leave_one_species_out_pair_mean",
    "leave_one_species_out_species_mean",
    "migration_distance_class_availability"
  ),
  estimate = c(
    mean(primary$delta_fisher_z),
    ifelse(nrow(exact8) > 0, mean(exact8$delta_rho), NA_real_),
    mean(species_primary$delta_rho),
    distance_est,
    mean(primary$delta_raw, na.rm = TRUE),
    mean(alt7$delta_rho),
    min(loo$pair_mean_delta_rho),
    min(loo$species_equal_weight_mean),
    length(mig_cols)
  ),
  secondary = c(
    sd(primary$delta_fisher_z) / sqrt(nrow(primary)),
    nrow(exact8),
    nrow(species_primary),
    distance_se,
    sum(is.finite(primary$delta_raw)),
    nrow(alt7),
    max(loo$pair_mean_delta_rho),
    max(loo$species_equal_weight_mean),
    ifelse(length(mig_cols) > 0, paste(mig_cols, collapse = ";"), "NONE")
  ),
  p_value = c(
    NA,
    NA,
    NA,
    distance_p,
    NA,
    NA,
    NA,
    NA,
    NA
  )
)

write.csv(
  summary,
  "outputs/payoff_b_v8_sensitivity_summary.csv",
  row.names = FALSE
)
write.csv(
  exact8,
  "outputs/payoff_b_v8_exact8_pairs.csv",
  row.names = FALSE
)
write.csv(
  alt7,
  "outputs/payoff_b_v8_alt7_pairs.csv",
  row.names = FALSE
)
write.csv(
  loo,
  "outputs/payoff_b_v8_leave_one_species_out.csv",
  row.names = FALSE
)

cat("PAYOFF-B V8 SENSITIVITIES\n")
print(summary)
cat("\nPRIMARY CLUSTER BOOT CI RECHECK\n")
print(cluster_boot_ci(primary))
