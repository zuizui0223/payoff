#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

PRIMARY_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_primary.R"
AUDIT_LOCK <- "docs/PAYOFF_B_V8_DEPENDENCE_QUALITY_AUDIT_LOCK_20261005.md"
SOURCE_COMMIT_EXPECTED <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
B <- 10000L
SEED <- 20261005L

if (!file.exists(PRIMARY_SCRIPT)) stop("Missing V8 primary script")
if (!file.exists(AUDIT_LOCK)) stop("Missing dependence-quality audit lock")

source(PRIMARY_SCRIPT, local = FALSE)

if (!identical(SOURCE_COMMIT, SOURCE_COMMIT_EXPECTED)) {
  stop("Unexpected Amaral source commit")
}

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

qci <- function(x) {
  x <- x[is.finite(x)]
  as.numeric(quantile(x, c(0.025, 0.975), names = FALSE))
}

cluster_boot_mean <- function(values, clusters, B = B, seed = SEED) {
  datx <- data.frame(value = values, cluster = as.character(clusters))
  datx <- datx[is.finite(datx$value) & !is.na(datx$cluster), , drop = FALSE]
  lev <- unique(datx$cluster)
  by_cluster <- split(datx$value, datx$cluster)
  set.seed(seed)
  out <- numeric(B)
  G <- length(lev)
  for (b in seq_len(B)) {
    sampled <- sample(lev, size = G, replace = TRUE)
    vals <- unlist(by_cluster[sampled], use.names = FALSE)
    out[b] <- mean(vals)
  }
  out
}

block_boot_mean <- function(values, blocks, B = B, seed = SEED) {
  cluster_boot_mean(values, blocks, B = B, seed = seed)
}

# ------------------------------------------------------------------
# A0 — original range-column semantics and geometry
# ------------------------------------------------------------------
source_code_url <- paste0(
  "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
  SOURCE_COMMIT,
  "/code/3_ModelPlots.R"
)
source_code_cache <- "outputs/amaral_3_ModelPlots_frozen.R"
if (!file.exists(source_code_cache)) {
  download.file(source_code_url, source_code_cache, mode = "wb", quiet = FALSE)
}
source_code_txt <- paste(readLines(source_code_cache, warn = FALSE), collapse = "\n")

mig_true_used_as_migratory <- (
  grepl('cond=list\\(mig_cell=T\\)', source_code_txt) &&
  grepl('Migratory cell', source_code_txt, fixed = TRUE)
)
breed_true_used_as_breeding <- grepl(
  'filter\\(breed_cell == T\\)',
  source_code_txt
)

cell_coords <- unique(cells[, c("cell", "cell_lat2", "cell_lng")])
cell_coords <- cell_coords[
  is.finite(cell_coords$cell) &
    is.finite(cell_coords$cell_lat2) &
    is.finite(cell_coords$cell_lng),
  ,
  drop = FALSE
]
# Cell coordinates should be unique by cell; defensively average exact duplicates.
cell_coords <- aggregate(
  cbind(cell_lat2, cell_lng) ~ cell,
  data = cell_coords,
  FUN = mean
)

pgeom <- pairs
si <- match(pgeom$source_cell, cell_coords$cell)
ti <- match(pgeom$target_cell, cell_coords$cell)
pgeom$source_lat <- cell_coords$cell_lat2[si]
pgeom$source_lon <- cell_coords$cell_lng[si]
pgeom$target_lat <- cell_coords$cell_lat2[ti]
pgeom$target_lon <- cell_coords$cell_lng[ti]
pgeom$source_strictly_south <- pgeom$source_lat < pgeom$target_lat
south_all <- all(pgeom$source_strictly_south, na.rm = FALSE)

a0 <- data.frame(
  source_code_mig_true_migratory = mig_true_used_as_migratory,
  source_code_breed_true_breeding = breed_true_used_as_breeding,
  primary_pairs = nrow(pgeom),
  all_source_lat_strictly_below_target = south_all,
  geometry_missing_n = sum(
    !is.finite(pgeom$source_lat) |
      !is.finite(pgeom$target_lat) |
      !is.finite(pgeom$source_lon) |
      !is.finite(pgeom$target_lon)
  )
)

# ------------------------------------------------------------------
# A1 — absolute early/late connectivity
# ------------------------------------------------------------------
set.seed(SEED)
boot_early <- numeric(B)
boot_late <- numeric(B)
N <- nrow(pairs)
for (b in seq_len(B)) {
  ii <- sample.int(N, N, replace = TRUE)
  boot_early[b] <- mean(pairs$rho_early[ii])
  boot_late[b] <- mean(pairs$rho_late[ii])
}
early_ci <- qci(boot_early)
late_ci <- qci(boot_late)

a1 <- data.frame(
  n_pairs = N,
  mean_rho_early = mean(pairs$rho_early),
  median_rho_early = median(pairs$rho_early),
  early_ci_low_95 = early_ci[1],
  early_ci_high_95 = early_ci[2],
  mean_rho_late = mean(pairs$rho_late),
  median_rho_late = median(pairs$rho_late),
  late_ci_low_95 = late_ci[1],
  late_ci_high_95 = late_ci[2],
  mean_delta_rho = mean(pairs$delta_rho)
)

# ------------------------------------------------------------------
# A2 — exact cell-reuse dependence
# ------------------------------------------------------------------
source_counts <- table(pairs$source_cell)
target_counts <- table(pairs$target_cell)

# Undirected source-target graph connected components via union-find.
nodes <- sort(unique(c(pairs$source_cell, pairs$target_cell)))
parent <- seq_along(nodes)
names(parent) <- as.character(nodes)

find_root <- function(i) {
  while (parent[i] != i) {
    parent[i] <<- parent[parent[i]]
    i <- parent[i]
  }
  i
}
union_nodes <- function(a, b) {
  ia <- match(as.character(a), names(parent))
  ib <- match(as.character(b), names(parent))
  ra <- find_root(ia)
  rb <- find_root(ib)
  if (ra != rb) parent[rb] <<- ra
}
for (i in seq_len(nrow(pairs))) {
  union_nodes(pairs$source_cell[i], pairs$target_cell[i])
}
roots <- vapply(seq_along(nodes), find_root, integer(1))
component_sizes <- sort(table(roots), decreasing = TRUE)

source_boot <- cluster_boot_mean(
  pairs$delta_rho,
  pairs$source_cell,
  B = B,
  seed = SEED
)
target_boot <- cluster_boot_mean(
  pairs$delta_rho,
  pairs$target_cell,
  B = B,
  seed = SEED
)
source_ci <- qci(source_boot)
target_ci <- qci(target_boot)

y <- pairs$delta_rho
mu <- mean(y)
e <- y - mu
cluster_var_cr0 <- function(resid, cluster) {
  sums <- tapply(resid, as.character(cluster), sum)
  sum(sums^2) / length(resid)^2
}
v_source <- cluster_var_cr0(e, pairs$source_cell)
v_target <- cluster_var_cr0(e, pairs$target_cell)
v_pair <- sum(e^2) / length(e)^2
v_two_way <- max(0, v_source + v_target - v_pair)
se_two_way <- sqrt(v_two_way)
two_way_ci <- mu + c(-1, 1) * 1.96 * se_two_way

a2 <- data.frame(
  unique_source_cells = length(source_counts),
  unique_target_cells = length(target_counts),
  max_pairs_per_source = max(source_counts),
  max_pairs_per_target = max(target_counts),
  graph_components = length(component_sizes),
  largest_component_nodes = max(component_sizes),
  source_cluster_ci_low_95 = source_ci[1],
  source_cluster_ci_high_95 = source_ci[2],
  target_cluster_ci_low_95 = target_ci[1],
  target_cluster_ci_high_95 = target_ci[2],
  two_way_cr0_se = se_two_way,
  two_way_cr0_ci_low_95 = two_way_ci[1],
  two_way_cr0_ci_high_95 = two_way_ci[2]
)

component_df <- data.frame(
  component_rank = seq_along(component_sizes),
  n_cells = as.integer(component_sizes)
)

# ------------------------------------------------------------------
# A3 — coarse spatial-block dependence
# ------------------------------------------------------------------
pgeom$mid_lat <- (pgeom$source_lat + pgeom$target_lat) / 2
pgeom$mid_lon <- (pgeom$source_lon + pgeom$target_lon) / 2

make_block <- function(lat, lon, size) {
  paste(
    floor(lat / size),
    floor(lon / size),
    sep = "_"
  )
}
pgeom$block5 <- make_block(pgeom$mid_lat, pgeom$mid_lon, 5)
pgeom$block10 <- make_block(pgeom$mid_lat, pgeom$mid_lon, 10)

block5_boot <- block_boot_mean(
  pgeom$delta_rho,
  pgeom$block5,
  B = B,
  seed = SEED
)
block10_boot <- block_boot_mean(
  pgeom$delta_rho,
  pgeom$block10,
  B = B,
  seed = SEED
)
block5_ci <- qci(block5_boot)
block10_ci <- qci(block10_boot)

a3 <- data.frame(
  blocks_5deg = length(unique(pgeom$block5)),
  block5_ci_low_95 = block5_ci[1],
  block5_ci_high_95 = block5_ci[2],
  blocks_10deg = length(unique(pgeom$block10)),
  block10_ci_low_95 = block10_ci[1],
  block10_ci_high_95 = block10_ci[2]
)

# ------------------------------------------------------------------
# A4 — leave one calendar year out on exact-complete pairs
# ------------------------------------------------------------------
complete_pairs <- pairs[pairs$early_n == 8L & pairs$late_n == 8L, , drop = FALSE]
if (nrow(complete_pairs) == 0) stop("No exact-complete V8 pairs")

rho_window_omit <- function(source_cell, target_cell, start_year, end_year, omit_year) {
  source <- green[
    green$cell == source_cell &
      green$year >= start_year &
      green$year <= end_year &
      green$year != omit_year,
    c("year", "gr_mn")
  ]
  target <- green[
    green$cell == target_cell &
      green$year >= start_year &
      green$year <= end_year &
      green$year != omit_year,
    c("year", "gr_mn")
  ]
  names(source)[2] <- "source_greenup"
  names(target)[2] <- "target_greenup"
  paired <- merge(source, target, by = "year", all = FALSE)
  paired <- paired[
    is.finite(paired$year) &
      is.finite(paired$source_greenup) &
      is.finite(paired$target_greenup),
    ,
    drop = FALSE
  ]
  paired <- paired[!duplicated(paired$year), , drop = FALSE]
  if (nrow(paired) != 7L) return(NA_real_)
  sr <- residuals(lm(source_greenup ~ year, data = paired))
  tr <- residuals(lm(target_greenup ~ year, data = paired))
  if (sd(sr) <= 0 || sd(tr) <= 0) return(NA_real_)
  cor(sr, tr)
}

years_all <- EARLY_START:LATE_END
loo_year <- data.frame(
  omitted_year = years_all,
  n_pairs = NA_integer_,
  mean_delta_rho = NA_real_
)

for (k in seq_along(years_all)) {
  yy <- years_all[k]
  d <- complete_pairs
  if (yy <= EARLY_END) {
    d$rho_early_loo <- mapply(
      rho_window_omit,
      d$source_cell,
      d$target_cell,
      MoreArgs = list(
        start_year = EARLY_START,
        end_year = EARLY_END,
        omit_year = yy
      )
    )
    d$rho_late_loo <- d$rho_late
  } else {
    d$rho_early_loo <- d$rho_early
    d$rho_late_loo <- mapply(
      rho_window_omit,
      d$source_cell,
      d$target_cell,
      MoreArgs = list(
        start_year = LATE_START,
        end_year = LATE_END,
        omit_year = yy
      )
    )
  }
  d$delta_loo <- d$rho_late_loo - d$rho_early_loo
  keep <- is.finite(d$delta_loo)
  loo_year$n_pairs[k] <- sum(keep)
  loo_year$mean_delta_rho[k] <- mean(d$delta_loo[keep])
}

a4 <- data.frame(
  exact_complete_pairs = nrow(complete_pairs),
  loo_year_runs = nrow(loo_year),
  positive_runs = sum(loo_year$mean_delta_rho > 0, na.rm = TRUE),
  min_mean_delta_rho = min(loo_year$mean_delta_rho, na.rm = TRUE),
  max_mean_delta_rho = max(loo_year$mean_delta_rho, na.rm = TRUE)
)

# ------------------------------------------------------------------
# A5 — gr_ncell measurement-support audit
# ------------------------------------------------------------------
support <- unique(dat[, c("year", "cell", "gr_ncell")])
support$year <- as.integer(support$year)
support$cell <- as.numeric(as.character(support$cell))
support$gr_ncell <- as.numeric(support$gr_ncell)
support <- support[
  is.finite(support$year) &
    is.finite(support$cell) &
    is.finite(support$gr_ncell) &
    support$gr_ncell >= 0,
  ,
  drop = FALSE
]
# Average any repeated year-cell values defensively.
support <- aggregate(
  gr_ncell ~ year + cell,
  data = support,
  FUN = mean
)

mean_support_window <- function(cell_id, start_year, end_year) {
  z <- support[
    support$cell == cell_id &
      support$year >= start_year &
      support$year <= end_year,
    ,
    drop = FALSE
  ]
  if (nrow(z) == 0) return(NA_real_)
  mean(log1p(z$gr_ncell))
}

suppairs <- pairs
suppairs$source_support_early <- vapply(
  suppairs$source_cell,
  mean_support_window,
  numeric(1),
  start_year = EARLY_START,
  end_year = EARLY_END
)
suppairs$source_support_late <- vapply(
  suppairs$source_cell,
  mean_support_window,
  numeric(1),
  start_year = LATE_START,
  end_year = LATE_END
)
suppairs$target_support_early <- vapply(
  suppairs$target_cell,
  mean_support_window,
  numeric(1),
  start_year = EARLY_START,
  end_year = EARLY_END
)
suppairs$target_support_late <- vapply(
  suppairs$target_cell,
  mean_support_window,
  numeric(1),
  start_year = LATE_START,
  end_year = LATE_END
)

suppairs$source_support_change <- (
  suppairs$source_support_late - suppairs$source_support_early
)
suppairs$target_support_change <- (
  suppairs$target_support_late - suppairs$target_support_early
)
suppairs$mean_support_change <- (
  suppairs$source_support_change + suppairs$target_support_change
) / 2

keep_support <- is.finite(suppairs$mean_support_change) &
  is.finite(suppairs$delta_rho)
supp_fit <- suppairs[keep_support, , drop = FALSE]

support_cor <- if (nrow(supp_fit) >= 3) {
  cor(supp_fit$delta_rho, supp_fit$mean_support_change)
} else {
  NA_real_
}

support_sd <- sd(supp_fit$mean_support_change)
if (is.finite(support_sd) && support_sd > 0) {
  supp_fit$z_support_change <- (
    supp_fit$mean_support_change - mean(supp_fit$mean_support_change)
  ) / support_sd
  support_slope <- unname(
    coef(lm(delta_rho ~ z_support_change, data = supp_fit))["z_support_change"]
  )
} else {
  supp_fit$z_support_change <- NA_real_
  support_slope <- NA_real_
}

if (nrow(supp_fit) > 0) {
  rk <- rank(supp_fit$mean_support_change, ties.method = "first")
  supp_fit$support_quartile <- pmin(
    4L,
    pmax(1L, ceiling(4 * rk / nrow(supp_fit)))
  )
  quartile_means <- aggregate(
    delta_rho ~ support_quartile,
    data = supp_fit,
    FUN = mean
  )
  quartile_counts <- aggregate(
    delta_rho ~ support_quartile,
    data = supp_fit,
    FUN = length
  )
  names(quartile_counts)[2] <- "n_pairs"
  quartile_means <- merge(
    quartile_means,
    quartile_counts,
    by = "support_quartile",
    all = TRUE
  )
} else {
  quartile_means <- data.frame(
    support_quartile = integer(),
    delta_rho = numeric(),
    n_pairs = integer()
  )
}

a5 <- data.frame(
  support_pairs_finite = nrow(supp_fit),
  mean_source_support_early = mean(suppairs$source_support_early, na.rm = TRUE),
  mean_source_support_late = mean(suppairs$source_support_late, na.rm = TRUE),
  mean_target_support_early = mean(suppairs$target_support_early, na.rm = TRUE),
  mean_target_support_late = mean(suppairs$target_support_late, na.rm = TRUE),
  mean_pair_support_change = mean(suppairs$mean_support_change, na.rm = TRUE),
  cor_delta_rho_support_change = support_cor,
  slope_delta_rho_on_z_support_change = support_slope
)

# ------------------------------------------------------------------
# A6 — locked interpretation
# ------------------------------------------------------------------
dependence_robust <- (
  is.finite(source_ci[1]) && source_ci[1] > 0 &&
  is.finite(target_ci[1]) && target_ci[1] > 0 &&
  is.finite(block5_ci[1]) && block5_ci[1] > 0 &&
  is.finite(block10_ci[1]) && block10_ci[1] > 0 &&
  all(is.finite(loo_year$mean_delta_rho)) &&
  all(loo_year$mean_delta_rho > 0)
)

status <- data.frame(
  A0_range_semantics_pass = (
    mig_true_used_as_migratory &&
    breed_true_used_as_breeding &&
    south_all
  ),
  dependence_robust_for_falsification_use = ifelse(
    dependence_robust,
    "YES",
    "NO"
  ),
  source_cluster_lower = source_ci[1],
  target_cluster_lower = target_ci[1],
  block5_lower = block5_ci[1],
  block10_lower = block10_ci[1],
  loo_year_positive = sum(loo_year$mean_delta_rho > 0),
  loo_year_total = nrow(loo_year)
)

write.csv(a0, "outputs/payoff_b_v8_audit_A0_semantics.csv", row.names = FALSE)
write.csv(a1, "outputs/payoff_b_v8_audit_A1_absolute_rho.csv", row.names = FALSE)
write.csv(a2, "outputs/payoff_b_v8_audit_A2_cell_dependence.csv", row.names = FALSE)
write.csv(component_df, "outputs/payoff_b_v8_audit_A2_components.csv", row.names = FALSE)
write.csv(a3, "outputs/payoff_b_v8_audit_A3_spatial_blocks.csv", row.names = FALSE)
write.csv(loo_year, "outputs/payoff_b_v8_audit_A4_loo_year.csv", row.names = FALSE)
write.csv(a4, "outputs/payoff_b_v8_audit_A4_loo_year_summary.csv", row.names = FALSE)
write.csv(supp_fit, "outputs/payoff_b_v8_audit_A5_support_pairs.csv", row.names = FALSE)
write.csv(a5, "outputs/payoff_b_v8_audit_A5_support_summary.csv", row.names = FALSE)
write.csv(quartile_means, "outputs/payoff_b_v8_audit_A5_support_quartiles.csv", row.names = FALSE)
write.csv(status, "outputs/payoff_b_v8_dependence_quality_audit_status.csv", row.names = FALSE)

cat("\nPAYOFF-B V8 DEPENDENCE + MEASUREMENT-QUALITY AUDIT\n")
cat("\nA0 semantics\n")
print(a0)
cat("\nA1 absolute rho\n")
print(a1)
cat("\nA2 cell dependence\n")
print(a2)
cat("\nA3 spatial blocks\n")
print(a3)
cat("\nA4 leave-one-year-out\n")
print(a4)
cat("\nA5 measurement support\n")
print(a5)
print(quartile_means)
cat("\nA6 status\n")
print(status)
