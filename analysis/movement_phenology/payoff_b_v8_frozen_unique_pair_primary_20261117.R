#!/usr/bin/env Rscript
# PAYOFF-B V8; CONTRACT AND METHOD FROZEN 2026-10-05.
# Primary changes in source-to-target green-up predictability, unique-pair
# resampling and equal-species exposure; no bird timing or fitness used.
options(stringsAsFactors=FALSE)
SOURCE_COMMIT <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL <- paste0("https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
                     SOURCE_COMMIT, "/data/final.rds")
EARLY <- 2002:2009
LATE <- 2010:2017
MIN_PAIRS <- 6L
B <- 10000L
SEED <- 20261005L
dir.create("outputs",recursive=TRUE,showWarnings=FALSE)

truthy <- function(x) toupper(as.character(x)) %in% c("TRUE","T","1")
hav <- function(a,b,c,d) {
  rad <- pi/180
  t <- sin((c-a)*rad/2)^2+cos(a*rad)*cos(c*rad)*
       sin((d-b)*rad/2)^2
  6371.0088*2*atan2(sqrt(t),sqrt(pmax(0,1-t)))
}
detrended_r <- function(x) {
  if (nrow(x)<MIN_PAIRS || length(unique(x$year))!=nrow(x)) return(NA_real_)
  src <- residuals(lm(source~year,data=x))
  tgt <- residuals(lm(target~year,data=x))
  if (!all(is.finite(src)) || !all(is.finite(tgt)) ||
      sd(src)<=0 || sd(tgt)<=0) return(NA_real_)
  cor(src,tgt)
}
pair_years <- function(green,src,tgt,years) {
  a <- green[green$cell==src & green$year %in% years,c("year","gr_mn")]
  b <- green[green$cell==tgt & green$year %in% years,c("year","gr_mn")]
  names(a)[2] <- "source"
  names(b)[2] <- "target"
  merge(a,b,by="year",all=FALSE)
}
incidence <- function(exposure,keys,species) {
  M <- matrix(0L,nrow=length(species),ncol=length(keys),
              dimnames=list(species,keys))
  ii <- match(exposure$species,species)
  jj <- match(exposure$pair_id,keys)
  if (anyNA(ii) || anyNA(jj)) stop("Original incidence pair/source drift")
  M[cbind(ii,jj)] <- 1L
  M
}
boots <- function(delta,M) {
  n <- length(delta)
  stopifnot(ncol(M)==n, n>1)
  set.seed(SEED)
  a <- numeric(B)
  b <- numeric(B)
  nj <- integer(B)
  for (j in seq_len(B)) {
    w <- tabulate(sample.int(n,n,replace=TRUE),nbins=n)
    a[j] <- sum(delta*w)/n
    denom <- as.vector(M%*%w)
    present <- denom>0L
    nj[j] <- sum(present)
    b[j] <- mean(as.vector(M%*%(delta*w))[present]/denom[present])
  }
  list(pair_ci=unname(quantile(a,c(.025,.975))),
       species_ci=unname(quantile(b,c(.025,.975))),
       mean_rep_species=mean(nj),min_rep_species=min(nj),
       all_species_fraction=mean(nj==nrow(M)))
}
if ("--synthetic-only" %in% commandArgs(trailingOnly=TRUE)) {
  x <- data.frame(year=2002:2009,source=c(4,2,1,7,3,5,9,8),
                  target=c(5,1,4,6,2,6,8,7))
  stopifnot(is.finite(detrended_r(x)))
  inc <- incidence(data.frame(species=c("A","B","B"),
                   pair_id=c("p1","p1","p2")), c("p1","p2"),c("A","B"))
  stopifnot(inc[1,1]==1L,inc[2,1]==1L,inc[1,2]==0L)
  cat("PAYOFF-B V8 synthetic algebra contracts: PASS\n")
  quit(status=0)
}

cache <- "outputs/amaral_final_20260926_pinned.rds"
if (!file.exists(cache)) download.file(SOURCE_URL,cache,mode="wb",quiet=FALSE)
if (file.info(cache)$size<1000) stop("Frozen original Amaral RDS missing")
raw <- readRDS(cache)
stopifnot(is.data.frame(raw))
required <- c("species","year","cell","cell_lat2","cell_lng",
              "gr_mn","mig_cell","breed_cell")
if (length(setdiff(required,names(raw))))
    stop(paste("Original source columns missing:",
               paste(setdiff(required,names(raw)),collapse=", ")))
cells <- unique(raw[,c("species","cell","cell_lat2","cell_lng",
                        "mig_cell","breed_cell")])
cells$cell <- as.numeric(as.character(cells$cell))
cells$cell_lat2 <- as.numeric(cells$cell_lat2)
cells$cell_lng <- as.numeric(cells$cell_lng)
cells$is_mig <- truthy(cells$mig_cell)
cells$is_breed <- truthy(cells$breed_cell)
target <- cells[cells$is_breed,c("species","cell","cell_lat2","cell_lng")]
target <- target[order(target$species,target$cell),]
mapping <- vector("list",nrow(target))
n <- 0L
for (i in seq_len(nrow(target))) {
  t <- target[i,]
  candidates <- cells[cells$species==t$species & cells$is_mig &
                      is.finite(cells$cell_lat2) & cells$cell_lat2<t$cell_lat2,
                      c("cell","cell_lat2","cell_lng")]
  if (!nrow(candidates)) next
  candidates$distance <- hav(candidates$cell_lat2,candidates$cell_lng,
                             t$cell_lat2,t$cell_lng)
  candidates <- candidates[order(candidates$distance,candidates$cell),]
  n <- n+1L
  mapping[[n]] <- data.frame(species=t$species,
                     source_cell=candidates$cell[1],
                     target_cell=t$cell,
                     distance_km=candidates$distance[1])
}
if (n==0) stop("Original route mapping unexpectedly empty")
mapping <- do.call(rbind,mapping[seq_len(n)])
green <- unique(raw[,c("year","cell","gr_mn")])
green$year <- as.integer(green$year)
green$cell <- as.numeric(as.character(green$cell))
green$gr_mn <- as.numeric(green$gr_mn)
green <- green[is.finite(green$year)&is.finite(green$cell)&
               is.finite(green$gr_mn),]
if (nrow(unique(green[,c("year","cell")])) != nrow(green))
    stop("Original greenup cell-year has contradictory duplicates")
mapping$early_n <- mapply(function(a,b)
   nrow(pair_years(green,a,b,EARLY)),
   mapping$source_cell,mapping$target_cell)
mapping$late_n <- mapply(function(a,b)
   nrow(pair_years(green,a,b,LATE)),
   mapping$source_cell,mapping$target_cell)
eligible <- mapping[mapping$early_n>=MIN_PAIRS &
                    mapping$late_n>=MIN_PAIRS,]
eligible$pair_id <- paste(eligible$source_cell,eligible$target_cell,sep="|")
pairs <- unique(eligible[,c("pair_id","source_cell","target_cell")])
species <- sort(unique(eligible$species))
species_counts <- table(eligible$species)
cat("PAYOFF-B V8 PRE-OUTCOME SAMPLE REPRODUCTION\n")
cat("original mappings=",nrow(mapping)," eligible species-pair=",
    nrow(eligible)," unique physical pairs=",nrow(pairs),
    " species=",length(species)," species>=3=",
    sum(species_counts>=3),"\n",sep="")
# This admission check was frozen before any original rho was computed.
if (!(nrow(mapping)==842L && nrow(eligible)==393L &&
      nrow(pairs)==166L && length(species)==28L &&
      sum(species_counts>=3L)==26L))
    stop("Frozen V8 source admission differs; correlation outcomes unopened")

# Open environmental outcomes only after the exact source and sample gate.
pairs$early_rho <- NA_real_
pairs$late_rho <- NA_real_
pairs$early_n <- NA_integer_
pairs$late_n <- NA_integer_
for (i in seq_len(nrow(pairs))) {
  x <- pair_years(green,pairs$source_cell[i],pairs$target_cell[i],EARLY)
  y <- pair_years(green,pairs$source_cell[i],pairs$target_cell[i],LATE)
  pairs$early_rho[i] <- detrended_r(x)
  pairs$late_rho[i] <- detrended_r(y)
  pairs$early_n[i] <- nrow(x)
  pairs$late_n[i] <- nrow(y)
}
if (any(!is.finite(pairs$early_rho)) || any(!is.finite(pairs$late_rho)))
    stop("Undefined frozen q after pre-admission, no primary finding")
pairs$delta_rho <- pairs$late_rho-pairs$early_rho
M <- incidence(eligible,pairs$pair_id,species)
species_delta <- as.vector((M%*%pairs$delta_rho)/rowSums(M))
pair_delta_mean <- mean(pairs$delta_rho)
species_delta_mean <- mean(species_delta)
uncertainty <- boots(pairs$delta_rho,M)
supported <- pair_delta_mean<0 && uncertainty$pair_ci[2]<0 &&
             species_delta_mean<0 && uncertainty$species_ci[2]<0
status <- if (supported) "BROAD_DEGRADATION_SUPPORTED" else
                         "BROAD_DEGRADATION_NOT_SUPPORTED"

result <- data.frame(
 source_commit=SOURCE_COMMIT,years="2002-2017",
 early="2002-2009",late="2010-2017",min_pairs=MIN_PAIRS,
 n_mapping=nrow(mapping),n_species_pair=nrow(eligible),
 n_unique_spatial_pairs=nrow(pairs),n_species=length(species),
 n_species_with_three_pairs=sum(species_counts>=3L),
 early_pair_mean_rho=mean(pairs$early_rho),
 late_pair_mean_rho=mean(pairs$late_rho),
 pair_mean_delta_rho=pair_delta_mean,
 pair_boot_ci_low=uncertainty$pair_ci[1],
 pair_boot_ci_high=uncertainty$pair_ci[2],
 equal_species_mean_delta_rho=species_delta_mean,
 species_boot_ci_low=uncertainty$species_ci[1],
 species_boot_ci_high=uncertainty$species_ci[2],
 negative_pairs=sum(pairs$delta_rho<0),
 positive_to_nonpositive_pairs=sum(pairs$early_rho>0 &
                                  pairs$late_rho<=0),
 species_with_negative_exposure=sum(species_delta<0),
 bootstrap_unit="UNIQUE_SPATIAL_PAIR",
 bootstrap_n=B,bootstrap_seed=SEED,
 bootstrap_species_averaged=uncertainty$mean_rep_species,
 bootstrap_species_min=uncertainty$min_rep_species,
 bootstrap_all_species_present=uncertainty$all_species_fraction,
 status=status
)
write.csv(result,"outputs/payoff_b_v8_primary_summary.csv",row.names=FALSE)
write.csv(pairs,"outputs/payoff_b_v8_unique_spatial_pairs.csv",row.names=FALSE)
write.csv(data.frame(species=species,delta_rho=species_delta,
                     n_pair_exposures=rowSums(M)),
          "outputs/payoff_b_v8_species_exposure.csv",row.names=FALSE)
cat("\nPAYOFF-B V8 FROZEN PRIMARY ENVIRONMENTAL RESULT\n")
print(result,row.names=FALSE,digits=7)
cat("\nNo bird arrival, speed, fitness, cue perception or causal warming coefficient fitted.\n")
