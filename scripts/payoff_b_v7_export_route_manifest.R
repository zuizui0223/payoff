#!/usr/bin/env Rscript

# Export the V7 environmental-predictor route manifest from the public Nemes
# wide dataset. This script is intentionally outcome-blind.

options(stringsAsFactors = FALSE)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: payoff_b_v7_export_route_manifest.R OUTPUT.csv")
out <- args[[1]]
dir.create(dirname(out), recursive=TRUE, showWarnings=FALSE)

url <- "https://zenodo.org/records/10094686/files/nemes_et_al_bird_pheno_wide_2023.RDS?download=1"
tmp <- tempfile(fileext=".rds")
download.file(url, tmp, mode="wb", method="libcurl", quiet=FALSE)
d <- readRDS(tmp)
stopifnot(is.data.frame(d))

keep <- c(
  "motusTagID","species","year",
  "site_id_r1","lon_r1","lat_r1",
  "site_id_r2","lon_r2","lat_r2",
  "dist_km"
)

missing <- setdiff(keep, names(d))
if (length(missing)) stop("Missing route-manifest fields: ", paste(missing,collapse=", "))

manifest <- d[,keep,drop=FALSE]

# Hard guard: never export any timing-response or phenology-response field.
forbidden <- c("lag","detday","sos","ndvi","gw_rate","recovery")
bad <- names(manifest)[vapply(names(manifest), function(x) {
  any(vapply(forbidden, function(p) grepl(p,x,ignore.case=TRUE), logical(1)))
}, logical(1))]
if (length(bad)) stop("Forbidden outcome-like fields in manifest: ",paste(bad,collapse=", "))

write.csv(manifest,out,row.names=FALSE)

cat("ROUTE_MANIFEST_ROWS=",nrow(manifest),"\n",sep="")
cat("OUTCOME_COLUMNS_EXPORTED=FALSE\n")
