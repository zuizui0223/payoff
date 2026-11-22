#!/usr/bin/env Rscript
# Extract exactly five predeclared variables from SHA-pinned Adams 2025 RDS.
# This file is ephemeral in the CI runner and MUST NEVER be committed or uploaded.
args <- commandArgs(trailingOnly = TRUE)
if(length(args)!=2L) stop("RDS source and private CSV path required")
input <- args[[1]]
output <- args[[2]]
if (!file.exists(input) || file.info(input)$size > 3000000) stop("Unverified input size")
dat <- readRDS(input) # original .Rda is saveRDS format, verified via upstream sha256
if (!is.data.frame(dat)) stop("Original must be a data.frame")
cols <- c("site", "year", "spring_q50", "spring_mean_temp", "mean_greenup")
if (!all(cols %in% names(dat))) stop("Expected author variables absent")
if (nrow(dat) != 833L || length(unique(dat$site)) != 53L ||
    length(unique(dat$year)) != 16L) stop("Frozen source grain changed")
d <- dat[, cols, drop=FALSE]
if (any(duplicated(d[, c("site", "year")]))) stop("duplicate site-year in source")
dir.create(dirname(output), recursive=TRUE, showWarnings=FALSE)
write.csv(d, file=output, row.names=FALSE, na="")
cat("private site-year source verified: rows=",nrow(d),
    " sites=",length(unique(d$site)),
    " years=",length(unique(d$year)), "\n", sep="")
