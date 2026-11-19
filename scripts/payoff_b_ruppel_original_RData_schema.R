#!/usr/bin/env Rscript
# Native base-R source-only audit for original 2023 Rüppel Figshare RData.
# Requires exact original Figshare ZIP SHA256 verification by Python preflight.
# Emits column names/type/summary cardinalities only; NO original row values.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) {
  stop("Usage: Rscript source_audit.R original_sha_verified.zip output.csv")
}
orig_zip <- args[1]
output <- args[2]
needed <- c("data.Event.RData", "flights.RData")
available <- utils::unzip(orig_zip, list = TRUE)$Name
if (!all(needed %in% available)) {
  stop("Required source RData files missing from validated original ZIP")
}
tmp <- tempfile("payoff_b_original_2023_RData_")
dir.create(tmp)
on.exit(unlink(tmp, recursive = TRUE), add = TRUE)
utils::unzip(orig_zip, files = needed, exdir = tmp)
rows <- list()
counter <- 0L
scan_object <- function(x, label, source) {
  cl <- paste(class(x), collapse = ";")
  if (is.data.frame(x)) {
    fields <- names(x)
    for (field in fields) {
      v <- x[[field]]
      key <- grepl("(^id$|bird|individual|tag|ring)", field,
                   ignore.case = TRUE, perl = TRUE)
      counter <<- counter + 1L
      rows[[counter]] <<- data.frame(
        original_RData_file = source,
        original_R_object_path = label,
        original_R_object_class = cl,
        n_original_rows = nrow(x),
        n_original_columns = ncol(x),
        original_column_name = field,
        original_column_R_class = paste(class(v), collapse = ";"),
        n_nonmissing_column_values = sum(!is.na(v)),
        candidate_identifier_column = key,
        n_distinct_candidate_IDs = if (key)
          length(unique(as.character(v[!is.na(v)]))) else NA_integer_,
        original_ID_values_exported = FALSE,
        stringsAsFactors = FALSE, check.names = FALSE
      )
    }
  } else if (is.list(x)) {
    # For lists of frames, source-grain audit limited to one nested level.
    subnames <- names(x)
    if (is.null(subnames)) subnames <- as.character(seq_along(x))
    for (j in seq_along(x)) {
      if (is.data.frame(x[[j]])) {
        scan_object(x[[j]], paste0(label, "/", subnames[j]), source)
      }
    }
  }
}
for (member in needed) {
  en <- new.env(parent = baseenv())
  loaded <- load(file.path(tmp, member), envir = en)
  for (name in loaded) {
    obj <- get(name, envir = en, inherits = FALSE)
    scan_object(obj, name, member)
  }
}
if (length(rows) == 0L) {
  stop("Native R load succeeded but source RData contains no readable data frames")
}
out <- do.call(rbind, rows)
dir.create(dirname(output), recursive = TRUE, showWarnings = FALSE)
utils::write.csv(out, file = output, row.names = FALSE, na = "")
cat(sprintf("SOURCE_RDATA_NATIVE_R_SCHEMA_OK n_objects=%d n_column_fields=%d\n",
            length(unique(out$original_R_object_path)), nrow(out)))
