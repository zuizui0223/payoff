#!/usr/bin/env Rscript
# Inspect two Figshare RData files from original Adams et al. (2025).
# Only schema, aggregate rows, candidate year/site cardinality are exported.
# Never export station labels, observations, GPS, migration time values or IDs.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) {
  stop("Usage: Rscript payoff_b_radar_Rdata_grain_20261122.R DATA1995.rda DATA2003.rda OUT.csv")
}

out <- list()
make_record <- function(source, path, tab) {
  n <- nrow(tab)
  fields <- names(tab)
  search <- tolower(fields)
  y <- which(grepl("^(year|yr|year_[a-z0-9]+|spring_year)$", search))
  s <- which(grepl("(^station$|station_|_station$|radar|^site$|site_id)", search))
  year_field <- if(length(y)) fields[y[1]] else ""
  site_field <- if(length(s)) fields[s[1]] else ""
  years <- integer(0)
  site_count <- NA_integer_
  if (length(y) && n <= 1000000) {
    vals <- tab[[y[1]]]
    if (is.factor(vals)) vals <- as.character(vals)
    nums <- suppressWarnings(as.integer(as.character(vals)))
    years <- sort(unique(nums[!is.na(nums) & nums >= 1980 & nums <= 2030]))
  }
  if (length(s) && n <= 1000000) {
    vals <- tab[[s[1]]]
    site_count <- length(unique(vals[!is.na(vals)]))
  }
  data.frame(
    source=source, data_object=path,
    n_rows=n, n_cols=ncol(tab), class_name=class(tab)[1],
    col_names=paste(fields, collapse=";"),
    year_field=year_field, site_field=site_field,
    n_years=if(length(y)) length(years) else NA_integer_,
    min_year=if(length(years)) min(years) else NA_integer_,
    max_year=if(length(years)) max(years) else NA_integer_,
    n_sites=site_count, stringsAsFactors=FALSE
  )
}

inspect <- function(obj, source, path, depth = 0L) {
  if (is.data.frame(obj)) {
    out[[length(out) + 1L]] <<- make_record(source, path, obj)
    return(invisible(NULL))
  }
  if (is.matrix(obj)) {
    out[[length(out) + 1L]] <<- make_record(
      source, path, as.data.frame(obj, stringsAsFactors=FALSE))
    return(invisible(NULL))
  }
  if (is.list(obj) && depth < 3L) {
    if (length(obj) > 200L) {
      stop("RData list has too many nested elements")
    }
    nm <- names(obj)
    if (is.null(nm)) nm <- as.character(seq_along(obj))
    for (i in seq_along(obj)) {
      inspect(obj[[i]], source, paste0(path, "/", nm[[i]]), depth + 1L)
    }
  }
  invisible(NULL)
}

for (i in seq_len(2L)) {
  file <- args[[i]]
  if (!file.exists(file) || file.info(file)$size > 3000000) {
    stop("Original RData is missing or exceeded size cap")
  }
  env <- new.env(parent=baseenv())
  objs <- load(file, envir=env)
  for (objname in objs) {
    inspect(get(objname, envir=env, inherits=FALSE),
            basename(file), objname)
  }
}
if (!length(out)) {
  rows <- data.frame(
    source=character(), data_object=character(),
    n_rows=integer(), n_cols=integer(), class_name=character(),
    col_names=character(), year_field=character(), site_field=character(),
    n_years=integer(), min_year=integer(), max_year=integer(),
    n_sites=integer(), stringsAsFactors=FALSE)
} else {
  rows <- do.call(rbind, out)
}
dir.create(dirname(args[[3]]), showWarnings=FALSE, recursive=TRUE)
write.csv(rows, args[[3]], row.names=FALSE, na="")
cat("RDATA_SCHEMA_ONLY_TABLES=", nrow(rows), "\n", sep="")
