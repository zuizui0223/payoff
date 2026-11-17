#!/usr/bin/env Rscript
# PAYOFF-B 2026-11-17; MODIS-only exploration; no eBird data.
# Source/pair rule frozen after prior eBird-conditioned V8 sign was opened:
# docs/PAYOFF_B_MODIS_ONLY_SPRING_COHERENCE_FREEZE_20261117.md
# NOT a confirmatory strengthening test or a bird response measurement.
options(stringsAsFactors=FALSE)
SOURCE_COMMIT <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL <- paste0("https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
                     SOURCE_COMMIT,"/data/for_green-up_dl.rds")
ORIGINAL_SHA256 <- "8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199"
EARLY <- 2002:2009
LATE <- 2010:2017
PIXEL_MIN <- 10000
MAX_DIST_KM <- 800
MIN_ANNUAL <- 6L
MIN_PAIRS <- 30L
MIN_SOURCES <- 15L
B <- 10000L
SEED <- 20261117L
dir.create("outputs",recursive=TRUE,showWarnings=FALSE)

hav <- function(a,b,c,d) {
  k <- pi/180
  z <- sin((c-a)*k/2)^2 + cos(a*k)*cos(c*k)*
       sin((d-b)*k/2)^2
  6371.0088*2*atan2(sqrt(z),sqrt(pmax(0,1-z)))
}
pair_period <- function(green,src,tgt,years) {
  a <- green[green$cell==src & green$year %in% years,
             c("year","gr_mn")]
  b <- green[green$cell==tgt & green$year %in% years,
             c("year","gr_mn")]
  names(a)[2] <- "source"
  names(b)[2] <- "target"
  merge(a,b,by="year")
}
rho <- function(series,detrend=TRUE,minimum=MIN_ANNUAL) {
  if (nrow(series)<minimum || length(unique(series$year))!=nrow(series))
    return(NA_real_)
  if (detrend) {
    a <- residuals(lm(source~year,data=series))
    b <- residuals(lm(target~year,data=series))
  } else {
    a <- series$source; b <- series$target
  }
  if (sd(a)<=0||sd(b)<=0) return(NA_real_)
  as.numeric(cor(a,b))
}
source_sha <- function(p) {
  a <- system2("sha256sum",p,stdout=TRUE)
  if(length(a)!=1)stop("No SHA256 validation available")
  strsplit(trimws(a[1]),"\\s+")[[1]][1]
}
if ("--synthetic-only" %in% commandArgs(trailingOnly=TRUE)) {
  d <- data.frame(year=2002:2009,
                  source=c(1,4,2,7,9,6,5,3),
                  target=c(2,3,1,8,7,5,4,6))
  stopifnot(is.finite(rho(d)),length(d$year)==8)
  stopifnot(is.finite(hav(55,-60,56,-59)),hav(55,-60,55,-60)==0)
  cat("MODIS-only R algebra source controls: PASS\n")
  quit(status=0)
}

path <- "outputs/modis_midgreenup_source_20261117.rds"
if (!file.exists(path)) download.file(SOURCE_URL,path,mode="wb",quiet=FALSE)
if (file.info(path)$size!=15579 || source_sha(path)!=ORIGINAL_SHA256)
  stop("Original MODIS-only source SHA256 or byte length drift")
dat <- readRDS(path)
needed <- c("year","cell","cell_lat","cell_lng","gr_mn","gr_ncell")
if (!is.data.frame(dat) || length(setdiff(needed,names(dat))))
  stop("Original satellite-only columns changed")
if (any(c("species","arr_GAM_mean","mig_cell","breed_cell") %in% names(dat)))
  stop("eBird-associated species/range fields in satellite-only source")
dat$year <- as.integer(as.character(dat$year))
dat$cell <- as.numeric(as.character(dat$cell))
dat$cell_lat <- as.numeric(dat$cell_lat)
dat$cell_lng <- as.numeric(dat$cell_lng)
dat$gr_mn <- as.numeric(dat$gr_mn)
dat$gr_ncell <- as.numeric(dat$gr_ncell)
if (any(!is.finite(dat$year)) || any(!is.finite(dat$cell)) ||
    any(duplicated(paste(dat$year,dat$cell,sep="|"))))
  stop("Source has invalid/duplicated cell-year")
if (!setequal(unique(dat$year),2002:2017))
  stop("MODIS source original calendar differs from frozen 16 years")
green <- dat[is.finite(dat$gr_mn)&dat$gr_mn>=1&dat$gr_mn<=366&
             is.finite(dat$gr_ncell)&dat$gr_ncell>PIXEL_MIN&
             is.finite(dat$cell_lat)&is.finite(dat$cell_lng),]
coord <- unique(green[,c("cell","cell_lat","cell_lng")])
if (anyDuplicated(coord$cell) || any(abs(coord$cell_lat)>90) ||
    any(abs(coord$cell_lng)>180))
  stop("Source cell geographic coordinates conflict")
count_window <- function(cell,years) {
  sum(green$cell==cell & green$year %in% years)
}
admitted <- coord[vapply(coord$cell,function(x)
    count_window(x,EARLY)>=MIN_ANNUAL && count_window(x,LATE)>=MIN_ANNUAL,
    logical(1)),]
admitted <- admitted[order(admitted$cell),]
pairs <- vector("list",nrow(admitted))
n <- 0L
for (i in seq_len(nrow(admitted))) {
  dest <- admitted[i,]
  candidates <- admitted[admitted$cell_lat<dest$cell_lat,]
  if(!nrow(candidates)) next
  candidates$d_km <- hav(candidates$cell_lat,candidates$cell_lng,
                         dest$cell_lat,dest$cell_lng)
  candidates <- candidates[is.finite(candidates$d_km)&
                           candidates$d_km<=MAX_DIST_KM,]
  if(!nrow(candidates)) next
  candidates <- candidates[order(candidates$d_km,candidates$cell),]
  n <- n+1L
  pairs[[n]] <- data.frame(
    target_cell=dest$cell,source_cell=candidates$cell[1],
    target_lat=dest$cell_lat,source_lat=candidates$cell_lat[1],
    source_target_km=candidates$d_km[1]
  )
}
if (!n) stop("No source-to-target satellite-only geographic links")
pairs <- do.call(rbind,pairs[seq_len(n)])
n_source <- length(unique(pairs$source_cell))
cat("MODIS-ONLY SOURCE GEOMETRY REPRODUCTION\n")
cat("source records:",nrow(dat)," original cells:",length(unique(dat$cell)),
    " valid geographic cells:",nrow(admitted),
    " geographic pairs:",nrow(pairs)," unique source cells:",n_source,"\n")
if(nrow(pairs)<MIN_PAIRS || n_source<MIN_SOURCES)
  stop("Post-open source-policy geographic-pair admission failed; NO_GO")

# Outcome is opened only after input SHA, purely geographic selection,
# minimum pair count and source provenance have passed.
pairs$early_rho <- NA_real_
pairs$late_rho <- NA_real_
pairs$early_n <- NA_integer_
pairs$late_n <- NA_integer_
pairs$early_raw <- NA_real_
pairs$late_raw <- NA_real_
pairs$early7 <- NA_real_
pairs$late7 <- NA_real_
for(i in seq_len(nrow(pairs))) {
  x <- pair_period(green,pairs$source_cell[i],pairs$target_cell[i],EARLY)
  y <- pair_period(green,pairs$source_cell[i],pairs$target_cell[i],LATE)
  pairs$early_n[i] <- nrow(x)
  pairs$late_n[i] <- nrow(y)
  pairs$early_rho[i] <- rho(x)
  pairs$late_rho[i] <- rho(y)
  pairs$early_raw[i] <- rho(x,detrend=FALSE)
  pairs$late_raw[i] <- rho(y,detrend=FALSE)
  pairs$early7[i] <- rho(pair_period(green,pairs$source_cell[i],
                           pairs$target_cell[i],2002:2008))
  pairs$late7[i] <- rho(pair_period(green,pairs$source_cell[i],
                           pairs$target_cell[i],2011:2017))
}
if (any(!is.finite(pairs$early_rho)) || any(!is.finite(pairs$late_rho)))
  stop("At least one admitted satellite pair correlation undefined")
pairs$delta_rho <- pairs$late_rho-pairs$early_rho

# Resample complete shared-SOURCE cells, not each link independently.
set.seed(SEED)
source_groups <- split(seq_len(nrow(pairs)),pairs$source_cell)
source_names <- names(source_groups)
source_b <- numeric(B)
for (i in seq_len(B)) {
  groups <- sample(source_names,length(source_names),replace=TRUE)
  ix <- unlist(source_groups[groups],use.names=FALSE)
  source_b[i] <- mean(pairs$delta_rho[ix])
}
source_ci <- unname(quantile(source_b,c(.025,.975)))
# Pair-wise CI shown as an over-optimistic diagnostic only.
set.seed(SEED)
pair_boot <- replicate(B,mean(sample(pairs$delta_rho,
                          nrow(pairs),replace=TRUE)))
pair_ci <- unname(quantile(pair_boot,c(.025,.975)))

# Pixel coverage guard: original per-site-year good forest pixel counts are
# satellite measurement support, never an independent food/fitness variable.
coverage <- aggregate(gr_ncell~year,green,mean)
coverage_early <- mean(coverage$gr_ncell[coverage$year %in% EARLY])
coverage_late <- mean(coverage$gr_ncell[coverage$year %in% LATE])
stats <- function(d) {
  if (!length(d)||any(!is.finite(d)))return(c(n=0,mean=NA_real_))
  c(n=length(d),mean=mean(d))
}
d7 <- pairs$late7-pairs$early7
draw <- pairs$late_raw-pairs$early_raw
complete <- pairs$delta_rho[pairs$early_n==8 & pairs$late_n==8]
result <- data.frame(
 source_kind="MODIS_ONLY_NO_EBIRD",
 source_sha256=ORIGINAL_SHA256,
 source_commit=SOURCE_COMMIT,
 years="2002-2017",
 geographic_design="nearest_south_up_to_800km",
 original_environmental_cells=length(unique(dat$cell)),
 admitted_environmental_cells=nrow(admitted),
 geographic_pairs=nrow(pairs),
 unique_source_cells=n_source,
 min_good_forest_pixels=PIXEL_MIN,
 min_paired_years=MIN_ANNUAL,
 early_mean_rho=mean(pairs$early_rho),
 late_mean_rho=mean(pairs$late_rho),
 source_cell_block_mean_delta=mean(pairs$delta_rho),
 source_cell_boot_ci_low=source_ci[1],
 source_cell_boot_ci_high=source_ci[2],
 pair_boot_ci_low=pair_ci[1],
 pair_boot_ci_high=pair_ci[2],
 negative_pair_n=sum(pairs$delta_rho<0),
 exact_eight_year_pair_n=length(complete),
 exact_eight_year_delta_mean=mean(complete),
 alternative_seven_year_pairs=stats(d7)[["n"]],
 alternative_seven_year_delta_mean=stats(d7)[["mean"]],
 raw_undetrended_delta_mean=mean(draw),
 mean_good_pixels_early=coverage_early,
 mean_good_pixels_late=coverage_late,
 source_cell_bootstrap_n=B,
 source_cell_bootstrap_seed=SEED,
 post_open_exploratory_not_confirmatory=TRUE,
 actual_migrant_cues_or_fitness_measured=FALSE
)
write.csv(result,"outputs/payoff_b_modis_only_geographic_summary.csv",row.names=FALSE)
write.csv(pairs,"outputs/payoff_b_modis_only_geographic_pairs.csv",row.names=FALSE)
cat("\nPAYOFF-B MODIS ONLY PURE ENVIRONMENTAL COMPARISON\n")
print(result,row.names=FALSE,digits=7)
cat("\nNo bird response, species, arrival, eBird, actual interaction, or fitness used.\n")
