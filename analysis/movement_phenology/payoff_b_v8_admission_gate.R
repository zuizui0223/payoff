#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

SOURCE_COMMIT <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL <- paste0(
  "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
  SOURCE_COMMIT,
  "/data/final.rds"
)

EARLY_START <- 2002L
EARLY_END <- 2009L
LATE_START <- 2010L
LATE_END <- 2017L
MIN_PAIRS_PER_WINDOW <- 6L

GATE_MIN_PAIRS <- 100L
GATE_MIN_SPECIES <- 20L
GATE_MIN_SPECIES_WITH_3_PAIRS <- 15L

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
cache <- "outputs/amaral_final_frozen.rds"
if (!file.exists(cache)) {
  download.file(SOURCE_URL, cache, mode = "wb", quiet = FALSE)
}

dat <- readRDS(cache)

required <- c(
  "species", "year", "cell", "cell_lat2", "cell_lng",
  "gr_mn", "mig_cell", "breed_cell"
)
missing <- setdiff(required, names(dat))
if (length(missing) > 0) {
  stop("Missing required columns: ", paste(missing, collapse = ", "))
}

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

cells <- unique(dat[, c(
  "species", "cell", "cell_lat2", "cell_lng", "mig_cell", "breed_cell"
)])
cells$cell <- as.numeric(as.character(cells$cell))
cells$cell_lat2 <- as.numeric(cells$cell_lat2)
cells$cell_lng <- as.numeric(cells$cell_lng)
cells$is_mig <- truthy(cells$mig_cell)
cells$is_breed <- truthy(cells$breed_cell)

targets <- cells[cells$is_breed, c("species", "cell", "cell_lat2", "cell_lng")]
targets <- targets[order(targets$species, targets$cell), ]

mapping <- vector("list", nrow(targets))
map_n <- 0L

for (i in seq_len(nrow(targets))) {
  target <- targets[i, ]
  candidates <- cells[
    cells$species == target$species &
      cells$is_mig &
      is.finite(cells$cell_lat2) &
      cells$cell_lat2 < target$cell_lat2,
    c("cell", "cell_lat2", "cell_lng")
  ]
  if (nrow(candidates) == 0) next

  candidates$distance_km <- haversine_km(
    candidates$cell_lat2,
    candidates$cell_lng,
    target$cell_lat2,
    target$cell_lng
  )
  candidates <- candidates[order(candidates$distance_km, candidates$cell), ]
  source <- candidates[1, ]

  map_n <- map_n + 1L
  mapping[[map_n]] <- data.frame(
    species = target$species,
    target_cell = target$cell,
    source_cell = source$cell,
    source_target_distance_km = source$distance_km
  )
}

mapping <- do.call(rbind, mapping[seq_len(map_n)])
if (is.null(mapping) || nrow(mapping) == 0) stop("No source-target mappings")

green <- unique(dat[, c("year", "cell", "gr_mn")])
green$year <- as.integer(green$year)
green$cell <- as.numeric(as.character(green$cell))
green$gr_mn <- as.numeric(green$gr_mn)
green <- green[is.finite(green$year) & is.finite(green$cell) & is.finite(green$gr_mn), ]

count_window_pairs <- function(source_cell, target_cell, start_year, end_year) {
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
  names(source)[2] <- "source_greenup"
  names(target)[2] <- "target_greenup"
  paired <- merge(source, target, by = "year", all = FALSE)
  length(unique(paired$year))
}

mapping$early_n <- mapply(
  count_window_pairs,
  mapping$source_cell,
  mapping$target_cell,
  MoreArgs = list(start_year = EARLY_START, end_year = EARLY_END)
)
mapping$late_n <- mapply(
  count_window_pairs,
  mapping$source_cell,
  mapping$target_cell,
  MoreArgs = list(start_year = LATE_START, end_year = LATE_END)
)

mapping$eligible_both_windows <- (
  mapping$early_n >= MIN_PAIRS_PER_WINDOW &
  mapping$late_n >= MIN_PAIRS_PER_WINDOW
)

eligible <- mapping[mapping$eligible_both_windows, ]
species_pair_counts <- aggregate(
  target_cell ~ species,
  data = eligible,
  FUN = length
)
names(species_pair_counts)[2] <- "eligible_pairs"

pair_count <- nrow(eligible)
species_count <- length(unique(eligible$species))
species_with_3_pairs <- sum(species_pair_counts$eligible_pairs >= 3)

gate_pass <- (
  pair_count >= GATE_MIN_PAIRS &&
  species_count >= GATE_MIN_SPECIES &&
  species_with_3_pairs >= GATE_MIN_SPECIES_WITH_3_PAIRS
)

summary_row <- data.frame(
  source_commit = SOURCE_COMMIT,
  early_window = paste0(EARLY_START, "-", EARLY_END),
  late_window = paste0(LATE_START, "-", LATE_END),
  min_pairs_per_window = MIN_PAIRS_PER_WINDOW,
  frozen_mappings_total = nrow(mapping),
  eligible_pairs_both_windows = pair_count,
  eligible_species = species_count,
  species_with_at_least_3_pairs = species_with_3_pairs,
  gate_min_pairs = GATE_MIN_PAIRS,
  gate_min_species = GATE_MIN_SPECIES,
  gate_min_species_with_3_pairs = GATE_MIN_SPECIES_WITH_3_PAIRS,
  gate_status = ifelse(gate_pass, "PASS", "FAIL")
)

write.csv(
  mapping,
  "outputs/payoff_b_v8_admission_gate_pairs.csv",
  row.names = FALSE
)
write.csv(
  species_pair_counts,
  "outputs/payoff_b_v8_admission_gate_species.csv",
  row.names = FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_admission_gate_summary.csv",
  row.names = FALSE
)

cat("PAYOFF-B V8 ADMISSION GATE\n")
print(summary_row)
cat("\nNo early/late correlation or Delta-rho value was calculated by this script.\n")
