#!/usr/bin/env Rscript

# Response-blind structural preflight for the frozen temporal-buffering bird
# holdout test. This script deliberately reads only year, species and cell.
# It must not inspect arrival timing, green-up timing, migration speed, mismatch
# or any derived tracking-performance response.

input_path <- Sys.getenv(
  "PAYOFF_AMARAL_FINAL_RDS",
  "external/amaral_2025/data/final.rds"
)
output_path <- commandArgs(trailingOnly = TRUE)
if (length(output_path) != 1) {
  stop("usage: temporal_buffering_bird_preflight.R OUTPUT_JSON")
}
if (!file.exists(input_path)) {
  stop("missing pinned Amaral final.rds")
}

dat <- as.data.frame(readRDS(input_path))
required <- c("year", "species", "cell")
missing <- setdiff(required, names(dat))
if (length(missing) > 0) {
  stop(paste("missing required columns:", paste(missing, collapse=", ")))
}

years <- sort(unique(dat$year[is.finite(dat$year)]))
n_years <- length(years)
n_cal <- floor(n_years / 2)
cal_years <- years[seq_len(n_cal)]
hold_years <- years[(n_cal + 1):n_years]

summarize_period <- function(d) {
  data.frame(
    n_rows = nrow(d),
    n_species = length(unique(d$species)),
    n_cells = length(unique(d$cell)),
    n_species_cells = length(unique(interaction(d$species, d$cell, drop=TRUE)))
  )
}

cal <- dat[dat$year %in% cal_years, c("year","species","cell"), drop=FALSE]
hold <- dat[dat$year %in% hold_years, c("year","species","cell"), drop=FALSE]

species_cal <- aggregate(
  year ~ species,
  data=cal,
  FUN=function(z) length(unique(z))
)
names(species_cal)[2] <- "n_years"
species_obs <- aggregate(
  cell ~ species,
  data=cal,
  FUN=length
)
names(species_obs)[2] <- "n_obs"
species_cells <- aggregate(
  cell ~ species,
  data=cal,
  FUN=function(z) length(unique(z))
)
names(species_cells)[2] <- "n_cells"
species_structural <- Reduce(
  function(x,y) merge(x,y,by="species",all=TRUE),
  list(species_obs,species_cells,species_cal)
)
species_structural$passes_count_gate <- with(
  species_structural,
  n_obs >= 60 & n_cells >= 5 & n_years >= 5
)

year_counts <- as.data.frame(table(dat$year), stringsAsFactors=FALSE)
names(year_counts) <- c("year","n_rows")
year_counts$year <- as.integer(as.character(year_counts$year))

payload <- list(
  status="RESPONSE_BLIND_PREFLIGHT",
  source_columns_read=c("year","species","cell"),
  unique_years=as.integer(years),
  n_unique_years=n_years,
  split_rule="first floor(n_unique_years/2) years calibration; remaining later years holdout",
  calibration_years=as.integer(cal_years),
  holdout_years=as.integer(hold_years),
  calibration=as.list(summarize_period(cal)[1,]),
  holdout=as.list(summarize_period(hold)[1,]),
  n_species_passing_structural_count_gate=sum(species_structural$passes_count_gate),
  structural_count_gate=list(
    min_observations=60,
    min_cells=5,
    min_years=5
  ),
  outcome_columns_inspected=FALSE
)

dir.create(dirname(output_path), recursive=TRUE, showWarnings=FALSE)

# Avoid an additional JSON dependency in the preflight.
json_string <- function(x) {
  if (is.null(x)) return("null")
  if (is.logical(x) && length(x)==1) return(tolower(as.character(x)))
  if (is.numeric(x) && length(x)==1) return(as.character(x))
  if (is.character(x) && length(x)==1) {
    return(paste0('"', gsub('"','\\\\"',x,fixed=TRUE), '"'))
  }
  if (is.atomic(x)) {
    return(paste0("[", paste(vapply(as.list(x), json_string, ""), collapse=","), "]"))
  }
  if (is.list(x) && !is.null(names(x))) {
    parts <- mapply(
      function(n,v) paste0('"',n,'":',json_string(v)),
      names(x), x, SIMPLIFY=TRUE, USE.NAMES=FALSE
    )
    return(paste0("{",paste(parts,collapse=","),"}"))
  }
  stop("unsupported JSON value")
}

writeLines(json_string(payload), output_path)
write.csv(year_counts, sub("\\.json$", "_year_counts.csv", output_path), row.names=FALSE)
write.csv(species_structural, sub("\\.json$", "_species_counts.csv", output_path), row.names=FALSE)

message("Wrote response-blind structural preflight to ", output_path)
