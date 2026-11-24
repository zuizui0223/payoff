#!/usr/bin/env Rscript
# Independent base-R audit of the exact q10/q50/q90/MODIS ordering classes.
# Reads immutable Figshare original RDS private to CI, emits only one aggregate row.
# No station identifiers, raw dates, locations or original records may be output.
args <- commandArgs(trailingOnly=TRUE)
if (length(args)!=2L) stop("original RDS and aggregate CSV required")
source <- args[[1]]
out <- args[[2]]
if (!file.exists(source) || file.info(source)$size > 3000000)
    stop("source is missing or oversized")
d <- readRDS(source)
fields <- c("site","year","spring_q10","spring_q50","spring_q90",
            "mean_greenup","spring_mean_temp")
if (!is.data.frame(d) || !all(fields %in% names(d)) ||
    nrow(d)!=833L || length(unique(d$site))!=53L ||
    length(unique(d$year))!=16L)
    stop("Original source provenance/shape gate failed")
p <- d[stats::complete.cases(d[,c("spring_q50","mean_greenup","spring_mean_temp")]),fields]
if (nrow(p)!=828L || length(unique(p$site))!=53L)
    stop("Parent PR415 complete-case source not reproduced")
if (any(duplicated(p[,c("site","year")])))
    stop("Original source site-year duplicated")
eps <- 1e-9
v <- stats::complete.cases(p[,c("spring_q10","spring_q50","spring_q90","mean_greenup")]) &
  p$spring_q10 >= 1 & p$spring_q10 <= 366 &
  p$spring_q50 >= 1 & p$spring_q50 <= 366 &
  p$spring_q90 >= 1 & p$spring_q90 <= 366 &
  p$mean_greenup >= 1 & p$mean_greenup <= 366
if(any(p$spring_q10[v] > p$spring_q50[v]+eps |
       p$spring_q50[v] > p$spring_q90[v]+eps))
    stop("nonmonotonic original passage quantiles")
q10 <- p$spring_q10[v]
q50 <- p$spring_q50[v]
q90 <- p$spring_q90[v]
g <- p$mean_greenup[v]
a <- g < q10-eps
b <- !a & g < q50-eps
c <- !a & !b & g <= q90+eps
e <- !a & !b & !c
row <- data.frame(
  original_rows=nrow(d),parent_complete=nrow(p),
  classified=length(g),unknown=sum(!v),
  before_q10=sum(a),q10_to_q50=sum(b),
  q50_to_q90=sum(c),after_q90=sum(e),
  at_least_7d_before_q10=sum(q10-g>=7-eps),
  at_least_7d_before_q50=sum(q50-g>=7-eps),
  greenup_before_q50=sum(g<q50-eps),
  source_sites=length(unique(p$site)),
  source_years=length(unique(p$year))
)
if(sum(as.numeric(row[1,c("before_q10","q10_to_q50","q50_to_q90","after_q90")]))!=row$classified)
    stop("exclusive classification partition failed")
dir.create(dirname(out),recursive=TRUE,showWarnings=FALSE)
utils::write.csv(row,out,row.names=FALSE)
cat("ORIGINAL_RDS_INDEPENDENT_R_AGGREGATES_CHECKED_ONLY\n")
