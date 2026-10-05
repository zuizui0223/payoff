#!/usr/bin/env Rscript

# PAYOFF-B V7 Nemes schema-only probe.
#
# This script is deliberately forbidden from calculating any focal V7 outcome:
# no lag summaries, catch-up/recovery values, predictability values, or
# predictability-response associations are produced here.

options(stringsAsFactors = FALSE)

OUT <- file.path("outputs", "payoff_b_v7_nemes_schema")
dir.create(OUT, recursive = TRUE, showWarnings = FALSE)

wide_url <- "https://zenodo.org/records/10094686/files/nemes_et_al_bird_pheno_wide_2023.RDS?download=1"
long_url <- "https://zenodo.org/records/10094686/files/nemes_et_al_bird_pheno_long_2023.RDS?download=1"

wide_file <- file.path(OUT, "nemes_wide_2023.rds")
long_file <- file.path(OUT, "nemes_long_2023.rds")

download_safe <- function(url, dest) {
  download.file(url, destfile = dest, mode = "wb", quiet = FALSE, method = "libcurl")
  if (!file.exists(dest) || file.info(dest)$size <= 0) {
    stop("download failed or empty: ", url)
  }
}

download_safe(wide_url, wide_file)
download_safe(long_url, long_file)

wide <- readRDS(wide_file)
long <- readRDS(long_file)

if (!is.data.frame(wide) || !is.data.frame(long)) {
  stop("Expected both RDS objects to be data.frames")
}

pick_first <- function(nms, candidates = NULL, regex = NULL) {
  if (!is.null(candidates)) {
    z <- candidates[candidates %in% nms]
    if (length(z)) return(z[[1]])
  }
  if (!is.null(regex)) {
    z <- grep(regex, nms, ignore.case = TRUE, value = TRUE)
    if (length(z)) return(z[[1]])
  }
  NA_character_
}

count_unique_safe <- function(df, col) {
  if (is.na(col) || !col %in% names(df)) return(NA_integer_)
  length(unique(df[[col]][!is.na(df[[col]])]))
}

id_w <- pick_first(names(wide), c("motusTagID", "tagID", "animal_id", "animalID"), "motus|tag.*id|animal.*id")
sp_w <- pick_first(names(wide), c("species"), "^species$")
yr_w <- pick_first(names(wide), c("year", "tracking_year"), "year")

site1 <- pick_first(names(wide), c("site_id_r1", "receiver_id_r1", "site_r1"), "site.*r1|receiver.*r1")
site2 <- pick_first(names(wide), c("site_id_r2", "receiver_id_r2", "site_r2"), "site.*r2|receiver.*r2")

route_pairs <- NA_integer_
if (!is.na(site1) && !is.na(site2)) {
  ok <- !is.na(wide[[site1]]) & !is.na(wide[[site2]])
  route_pairs <- length(unique(paste(wide[[site1]][ok], wide[[site2]][ok], sep = " -> ")))
}

summary_rows <- data.frame(
  metric = c(
    "wide_rows",
    "wide_columns",
    "long_rows",
    "long_columns",
    "unique_individuals_wide",
    "unique_species_wide",
    "unique_years_wide",
    "unique_south_sites_wide",
    "unique_north_sites_wide",
    "unique_route_pairs_wide"
  ),
  value = c(
    nrow(wide),
    ncol(wide),
    nrow(long),
    ncol(long),
    count_unique_safe(wide, id_w),
    count_unique_safe(wide, sp_w),
    count_unique_safe(wide, yr_w),
    count_unique_safe(wide, site1),
    count_unique_safe(wide, site2),
    route_pairs
  )
)

write.csv(summary_rows, file.path(OUT, "schema_summary.csv"), row.names = FALSE)

column_audit <- function(df, source) {
  data.frame(
    source = source,
    column = names(df),
    class = vapply(df, function(x) paste(class(x), collapse = ";"), character(1)),
    nonmissing_n = vapply(df, function(x) sum(!is.na(x)), integer(1)),
    missing_n = vapply(df, function(x) sum(is.na(x)), integer(1)),
    stringsAsFactors = FALSE
  )
}

cols <- rbind(column_audit(wide, "wide"), column_audit(long, "long"))
write.csv(cols, file.path(OUT, "schema_columns.csv"), row.names = FALSE)

candidate_patterns <- c(
  "motus|tag.*id|animal.*id",
  "species",
  "year",
  "site|receiver",
  "lat|lon|long",
  "det.*day|detect.*day|date",
  "spring|best|ndvi",
  "dist|distance"
)

candidate <- cols[Reduce(`|`, lapply(candidate_patterns, function(p) {
  grepl(p, cols$column, ignore.case = TRUE)
})), , drop = FALSE]

# Schema only: candidate column metadata, never focal values.
write.csv(candidate, file.path(OUT, "schema_candidate_columns.csv"), row.names = FALSE)

required_presence <- data.frame(
  role = c(
    "individual_id",
    "species",
    "year",
    "south_site",
    "north_site",
    "coordinate_like_columns",
    "south_detection_day_like",
    "north_detection_day_like",
    "spring_onset_like",
    "distance_like"
  ),
  present = c(
    !is.na(id_w),
    !is.na(sp_w),
    !is.na(yr_w),
    !is.na(site1),
    !is.na(site2),
    any(grepl("lat|lon|long", names(wide), ignore.case = TRUE)),
    any(grepl("det.*day.*r1|day.*r1", names(wide), ignore.case = TRUE)),
    any(grepl("det.*day.*r2|day.*r2", names(wide), ignore.case = TRUE)),
    any(grepl("best|spring|ndvi", names(wide), ignore.case = TRUE)),
    any(grepl("dist|distance", names(wide), ignore.case = TRUE))
  )
)
write.csv(required_presence, file.path(OUT, "schema_required_presence.csv"), row.names = FALSE)

cat("V7_SCHEMA_ONLY=TRUE\n")
cat("FOCAL_OUTCOME_OPENED=FALSE\n")
cat("PREDICTABILITY_COMPUTED=FALSE\n")
cat("MODEL_FITTED=FALSE\n")
cat("output_dir=", OUT, "\n", sep = "")
