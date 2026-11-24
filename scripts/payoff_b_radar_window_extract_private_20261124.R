#!/usr/bin/env Rscript
# Source-authenticated Adams et al 2025 radar migration-window private extractor.
# The output contains original site-year rows and MUST NEVER be uploaded as CI
# artifact or committed. Only derived aggregation script publishes results.
args <- commandArgs(trailingOnly=TRUE)
if (length(args)!=2L) stop("Usage: Rscript <original_RDS> <ephemeral_CSV>")
source <- args[[1]]
if (!file.exists(source) || file.info(source)$size>3000000L)
    stop("Missing or oversized source")
dat <- readRDS(source)
if (!is.data.frame(dat)) stop("Original must be data.frame")
cols <- c("site","year","spring_q10","spring_q50","spring_q90",
          "mean_greenup","spring_mean_temp")
if (!all(cols %in% names(dat))) stop("Missing frozen source column")
if (nrow(dat)!=833 || length(unique(dat$site))!=53 ||
    length(unique(dat$year))!=16)
    stop("Original source grain changed")
if (any(duplicated(dat[,c("site","year")])))
    stop("Duplicate original site-year")
tmp <- dat[,cols,drop=FALSE]
dir.create(dirname(args[[2]]),showWarnings=FALSE,recursive=TRUE)
write.csv(tmp,args[[2]],row.names=FALSE,na="")
cat("MIGRATION_WINDOW_PRIVATE_SOURCE_READY n=",nrow(tmp),"\n",sep="")
