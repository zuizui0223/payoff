#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC / OUTCOME-INFORMED STAGEWISE PHASE DIAGNOSTIC.
#
# Uses only source-target pairs for which the same species has >=6 annual
# population-front arrival estimates in BOTH source and target cells in BOTH
# periods.
#
# Local signed phase:
#
#   e = bird arrival - local mid-green-up.
#
# Route transformation:
#
#   e_target - e_source
#     =
#   (arrival_target - arrival_source)
#     -
#   (greenup_target - greenup_source).
#
# Negative values mean the population arrival front becomes earlier relative to
# local green-up between source and target.
#
# This is a population-front geometry diagnostic, NOT individual behavioral
# feedback and NOT a direct estimate of correction gain.

GATE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_admission_gate.R"
if (!file.exists(GATE_SCRIPT)) stop("Missing V8 admission-gate script")
source(GATE_SCRIPT, local = FALSE)

B <- 10000L
SEED <- 20261006L
MIN_YEARS <- 6L

eligible_map <- eligible
eligible_map$pair_key <- paste(
  eligible_map$source_cell,
  eligible_map$target_cell,
  sep="->"
)
map <- unique(eligible_map[,c(
  "species","source_cell","target_cell","pair_key"
)])

d <- dat[,c(
  "species","year","cell","arr_GAM_mean","arr_GAM_sd","gr_mn"
)]
d$year <- as.integer(d$year)
d$cell <- as.numeric(as.character(d$cell))
d$arr_GAM_mean <- as.numeric(d$arr_GAM_mean)
d$arr_GAM_sd <- as.numeric(d$arr_GAM_sd)
d$gr_mn <- as.numeric(d$gr_mn)

src <- d[
  is.finite(d$year) &
    is.finite(d$cell) &
    is.finite(d$arr_GAM_mean) &
    is.finite(d$gr_mn),
  c("species","year","cell","arr_GAM_mean","arr_GAM_sd","gr_mn"),
  drop=FALSE
]
src <- unique(src)
names(src)[3:6] <- c(
  "source_cell","source_arrival","source_arrival_sd","source_greenup"
)

tgt <- d[
  is.finite(d$year) &
    is.finite(d$cell) &
    is.finite(d$arr_GAM_mean) &
    is.finite(d$gr_mn),
  c("species","year","cell","arr_GAM_mean","arr_GAM_sd","gr_mn"),
  drop=FALSE
]
tgt <- unique(tgt)
names(tgt)[3:6] <- c(
  "target_cell","target_arrival","target_arrival_sd","target_greenup"
)

rows <- merge(
  map,src,
  by=c("species","source_cell"),
  all=FALSE,
  sort=FALSE
)
rows <- merge(
  rows,tgt,
  by=c("species","target_cell","year"),
  all=FALSE,
  sort=FALSE
)
rows <- rows[
  rows$year>=EARLY_START &
    rows$year<=LATE_END,
  ,
  drop=FALSE
]
rows <- unique(rows)

rows$source_phase <- rows$source_arrival - rows$source_greenup
rows$target_phase <- rows$target_arrival - rows$target_greenup
rows$phase_transform <- rows$target_phase - rows$source_phase
rows$front_lead <- rows$target_arrival - rows$source_arrival
rows$greenup_lead <- rows$target_greenup - rows$source_greenup
rows$period <- ifelse(rows$year<=EARLY_END,"early","late")

window_stats <- function(sp,source_cell,target_cell,period_name){
  z <- rows[
    rows$species==sp &
      rows$source_cell==source_cell &
      rows$target_cell==target_cell &
      rows$period==period_name,
    ,
    drop=FALSE
  ]
  z <- z[!duplicated(z$year),,drop=FALSE]
  c(
    n=nrow(z),
    source_phase=if(nrow(z)>0) mean(z$source_phase) else NA_real_,
    target_phase=if(nrow(z)>0) mean(z$target_phase) else NA_real_,
    phase_transform=if(nrow(z)>0) mean(z$phase_transform) else NA_real_,
    front_lead=if(nrow(z)>0) mean(z$front_lead) else NA_real_,
    greenup_lead=if(nrow(z)>0) mean(z$greenup_lead) else NA_real_,
    source_arrival_sd=if(nrow(z)>0) mean(z$source_arrival_sd,na.rm=TRUE) else NA_real_,
    target_arrival_sd=if(nrow(z)>0) mean(z$target_arrival_sd,na.rm=TRUE) else NA_real_
  )
}

early <- t(mapply(
  window_stats,
  map$species,map$source_cell,map$target_cell,
  MoreArgs=list(period_name="early")
))
late <- t(mapply(
  window_stats,
  map$species,map$source_cell,map$target_cell,
  MoreArgs=list(period_name="late")
))

units <- map
units$early_n <- as.integer(early[,"n"])
units$late_n <- as.integer(late[,"n"])

for(nm in c(
  "source_phase","target_phase","phase_transform",
  "front_lead","greenup_lead","source_arrival_sd","target_arrival_sd"
)){
  units[[paste0(nm,"_early")]] <- as.numeric(early[,nm])
  units[[paste0(nm,"_late")]] <- as.numeric(late[,nm])
  units[[paste0("delta_",nm)]] <-
    units[[paste0(nm,"_late")]] - units[[paste0(nm,"_early")]]
}

analysis <- units[
  units$early_n>=MIN_YEARS &
    units$late_n>=MIN_YEARS &
    is.finite(units$source_phase_early) &
    is.finite(units$source_phase_late) &
    is.finite(units$target_phase_early) &
    is.finite(units$target_phase_late),
  ,
  drop=FALSE
]

if(nrow(analysis)<20) stop("Too few eligible units")
if(length(unique(analysis$pair_key))<20) stop("Too few unique pairs")
if(length(unique(analysis$species))<5) stop("Too few species")

pair <- aggregate(
  cbind(
    source_phase_early,source_phase_late,delta_source_phase,
    target_phase_early,target_phase_late,delta_target_phase,
    phase_transform_early,phase_transform_late,delta_phase_transform,
    front_lead_early,front_lead_late,delta_front_lead,
    greenup_lead_early,greenup_lead_late,delta_greenup_lead,
    source_arrival_sd_early,source_arrival_sd_late,delta_source_arrival_sd,
    target_arrival_sd_early,target_arrival_sd_late,delta_target_arrival_sd
  ) ~ pair_key + source_cell + target_cell,
  data=analysis,
  FUN=mean
)

sp <- aggregate(
  cbind(
    source_phase_early,source_phase_late,delta_source_phase,
    target_phase_early,target_phase_late,delta_target_phase,
    phase_transform_early,phase_transform_late,delta_phase_transform,
    front_lead_early,front_lead_late,delta_front_lead,
    greenup_lead_early,greenup_lead_late,delta_greenup_lead
  ) ~ species,
  data=analysis,
  FUN=mean
)

pair_boot_mean <- function(x,B,seed){
  x <- x[is.finite(x)]
  set.seed(seed)
  out <- replicate(B,mean(sample(x,length(x),replace=TRUE)))
  as.numeric(quantile(out,c(.025,.975),names=FALSE))
}

pt_ci <- pair_boot_mean(pair$delta_phase_transform,B,SEED)
sp_ci <- pair_boot_mean(pair$delta_source_phase,B,SEED+1L)
tp_ci <- pair_boot_mean(pair$delta_target_phase,B,SEED+2L)
front_ci <- pair_boot_mean(pair$delta_front_lead,B,SEED+3L)
wave_ci <- pair_boot_mean(pair$delta_greenup_lead,B,SEED+4L)

# Descriptive downstream attenuation of the between-period source-stage phase
# shift. For positive mean source shift:
#
#   A = 1 - delta_target_phase / delta_source_phase
#     = - delta_phase_transform / delta_source_phase.
#
# A between 0 and 1 means that part of the source-stage shift is not retained at
# the target stage. This is a descriptive transformation fraction, not a
# fitness-optimal correction fraction.
set.seed(SEED+5L)
atten_boot <- rep(NA_real_,B)
for(b in seq_len(B)){
  ix <- sample(seq_len(nrow(pair)),nrow(pair),replace=TRUE)
  ds <- mean(pair$delta_source_phase[ix])
  dt <- mean(pair$delta_target_phase[ix])
  if(is.finite(ds) && abs(ds)>1e-9){
    atten_boot[b] <- 1-dt/ds
  }
}
attenuation_fraction <-
  1-mean(pair$delta_target_phase)/mean(pair$delta_source_phase)
attenuation_ci <- as.numeric(quantile(
  atten_boot[is.finite(atten_boot)],
  c(.025,.975),
  names=FALSE
))

# Equal-species bootstrap via pair incidence.
pair_delta <- setNames(pair$delta_phase_transform,pair$pair_key)
inc <- unique(analysis[,c("species","pair_key")])
inc_by_pair <- split(inc$species,inc$pair_key)
keys <- pair$pair_key
set.seed(SEED+10L)
eq_boot <- rep(NA_real_,B)
for(b in seq_len(B)){
  draw <- sample(keys,length(keys),replace=TRUE)
  lists <- list()
  for(pk in draw){
    spp <- inc_by_pair[[pk]]
    val <- pair_delta[[pk]]
    for(ss in spp) lists[[ss]] <- c(lists[[ss]],val)
  }
  means <- vapply(lists,mean,numeric(1))
  eq_boot[b] <- mean(means)
}
eq_ci <- as.numeric(quantile(eq_boot,c(.025,.975),names=FALSE))

# Cross-unit phase retention slopes for descriptive stage-to-stage geometry.
ols_slope <- function(x,y){
  ok <- is.finite(x)&is.finite(y)
  x <- x[ok]; y <- y[ok]
  if(length(x)<3 || sd(x)<=0) return(NA_real_)
  unname(coef(lm(y~x))[2])
}
ret_early <- ols_slope(pair$source_phase_early,pair$target_phase_early)
ret_late <- ols_slope(pair$source_phase_late,pair$target_phase_late)
cor_early <- cor(
  pair$source_phase_early,pair$target_phase_early,use="complete.obs"
)
cor_late <- cor(
  pair$source_phase_late,pair$target_phase_late,use="complete.obs"
)

summary_row <- data.frame(
  eligible_units=nrow(analysis),
  unique_pairs=nrow(pair),
  species=length(unique(analysis$species)),

  source_phase_early=mean(pair$source_phase_early),
  source_phase_late=mean(pair$source_phase_late),
  delta_source_phase=mean(pair$delta_source_phase),
  delta_source_phase_ci_low_95=sp_ci[1],
  delta_source_phase_ci_high_95=sp_ci[2],

  target_phase_early=mean(pair$target_phase_early),
  target_phase_late=mean(pair$target_phase_late),
  delta_target_phase=mean(pair$delta_target_phase),
  delta_target_phase_ci_low_95=tp_ci[1],
  delta_target_phase_ci_high_95=tp_ci[2],

  phase_transform_early=mean(pair$phase_transform_early),
  phase_transform_late=mean(pair$phase_transform_late),
  delta_phase_transform=mean(pair$delta_phase_transform),
  delta_phase_transform_median=median(pair$delta_phase_transform),
  delta_phase_transform_ci_low_95=pt_ci[1],
  delta_phase_transform_ci_high_95=pt_ci[2],
  pairs_more_negative_transform=sum(pair$delta_phase_transform<0),
  pairs_more_positive_transform=sum(pair$delta_phase_transform>0),

  equal_species_transform_early=mean(sp$phase_transform_early),
  equal_species_transform_late=mean(sp$phase_transform_late),
  equal_species_delta_transform=mean(sp$delta_phase_transform),
  equal_species_delta_ci_low_95=eq_ci[1],
  equal_species_delta_ci_high_95=eq_ci[2],
  species_more_negative_transform=sum(sp$delta_phase_transform<0),
  species_more_positive_transform=sum(sp$delta_phase_transform>0),

  front_lead_early=mean(pair$front_lead_early),
  front_lead_late=mean(pair$front_lead_late),
  delta_front_lead=mean(pair$delta_front_lead),
  delta_front_lead_ci_low_95=front_ci[1],
  delta_front_lead_ci_high_95=front_ci[2],

  greenup_lead_early=mean(pair$greenup_lead_early),
  greenup_lead_late=mean(pair$greenup_lead_late),
  delta_greenup_lead=mean(pair$delta_greenup_lead),
  delta_greenup_lead_ci_low_95=wave_ci[1],
  delta_greenup_lead_ci_high_95=wave_ci[2],

  source_shift_attenuation_fraction=attenuation_fraction,
  source_shift_attenuation_ci_low_95=attenuation_ci[1],
  source_shift_attenuation_ci_high_95=attenuation_ci[2],

  phase_retention_slope_early=ret_early,
  phase_retention_slope_late=ret_late,
  phase_correlation_early=cor_early,
  phase_correlation_late=cor_late,

  source_arrival_sd_early=mean(pair$source_arrival_sd_early,na.rm=TRUE),
  source_arrival_sd_late=mean(pair$source_arrival_sd_late,na.rm=TRUE),
  target_arrival_sd_early=mean(pair$target_arrival_sd_early,na.rm=TRUE),
  target_arrival_sd_late=mean(pair$target_arrival_sd_late,na.rm=TRUE)
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  rows,
  "outputs/payoff_b_v8_stagewise_phase_year_rows.csv",
  row.names=FALSE
)
write.csv(
  analysis,
  "outputs/payoff_b_v8_stagewise_phase_units.csv",
  row.names=FALSE
)
write.csv(
  pair,
  "outputs/payoff_b_v8_stagewise_phase_pairs.csv",
  row.names=FALSE
)
write.csv(
  sp,
  "outputs/payoff_b_v8_stagewise_phase_species.csv",
  row.names=FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_stagewise_phase_summary.csv",
  row.names=FALSE
)

cat("\nPOSTHOC STAGEWISE PHASE TRANSITION DIAGNOSTIC\n")
print(summary_row)
