#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC / OUTCOME-INFORMED SOURCE-STAGE ACCESS DIAGNOSTIC.
#
# The frozen mapping chooses a lower-latitude migratory-range environmental
# source cell. This audit asks whether the same species' estimated migration
# front also reaches that source cell before the paired target cell.
#
# This improves the biological interpretation of the mapping from
# "southern environmental cell" to "earlier population-front stage proxy".
# It still does NOT establish that the same individuals traversed both cells.

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

arr <- dat[,c("species","year","cell","arr_GAM_mean","arr_GAM_sd","gr_mn")]
arr$year <- as.integer(arr$year)
arr$cell <- as.numeric(as.character(arr$cell))
arr$arr_GAM_mean <- as.numeric(arr$arr_GAM_mean)
arr$arr_GAM_sd <- as.numeric(arr$arr_GAM_sd)
arr$gr_mn <- as.numeric(arr$gr_mn)

src <- arr[
  is.finite(arr$year) &
    is.finite(arr$cell) &
    is.finite(arr$arr_GAM_mean) &
    is.finite(arr$gr_mn),
  c("species","year","cell","arr_GAM_mean","arr_GAM_sd","gr_mn"),
  drop=FALSE
]
src <- unique(src)
names(src)[3:6] <- c(
  "source_cell","source_arrival","source_arrival_sd","source_greenup"
)

tgt <- arr[
  is.finite(arr$year) &
    is.finite(arr$cell) &
    is.finite(arr$arr_GAM_mean) &
    is.finite(arr$gr_mn),
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

# Positive front lead means source front arrives before target front.
rows$front_lead_days <- rows$target_arrival - rows$source_arrival
rows$source_front_before_target <- rows$front_lead_days>0

# Signed environmental phase when migration front arrives at source.
# Negative means source bird front arrives before source mid-green-up.
rows$source_arrival_minus_greenup <-
  rows$source_arrival - rows$source_greenup

# Remaining interval from source green-up event to target arrival.
rows$source_greenup_to_target_arrival <-
  rows$target_arrival - rows$source_greenup

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
    front_lead=if(nrow(z)>0) mean(z$front_lead_days) else NA_real_,
    share_front_order=if(nrow(z)>0) mean(z$source_front_before_target) else NA_real_,
    source_phase=if(nrow(z)>0) mean(z$source_arrival_minus_greenup) else NA_real_,
    signal_to_target=if(nrow(z)>0) mean(z$source_greenup_to_target_arrival) else NA_real_,
    source_arrival_sd=if(nrow(z)>0) mean(z$source_arrival_sd,na.rm=TRUE) else NA_real_,
    target_arrival_sd=if(nrow(z)>0) mean(z$target_arrival_sd,na.rm=TRUE) else NA_real_
  )
}

early <- t(mapply(
  window_stats,
  map$species,
  map$source_cell,
  map$target_cell,
  MoreArgs=list(period_name="early")
))
late <- t(mapply(
  window_stats,
  map$species,
  map$source_cell,
  map$target_cell,
  MoreArgs=list(period_name="late")
))

units <- map
units$early_n <- as.integer(early[,"n"])
units$late_n <- as.integer(late[,"n"])

for(nm in c(
  "front_lead","share_front_order","source_phase","signal_to_target",
  "source_arrival_sd","target_arrival_sd"
)){
  units[[paste0(nm,"_early")]] <- as.numeric(early[,nm])
  units[[paste0(nm,"_late")]] <- as.numeric(late[,nm])
  units[[paste0("delta_",nm)]] <-
    units[[paste0(nm,"_late")]] - units[[paste0(nm,"_early")]]
}

analysis <- units[
  units$early_n>=MIN_YEARS &
    units$late_n>=MIN_YEARS &
    is.finite(units$front_lead_early) &
    is.finite(units$front_lead_late),
  ,
  drop=FALSE
]

if(nrow(analysis)<20) stop("Too few species-target-source units")
if(length(unique(analysis$pair_key))<20) stop("Too few unique pairs")
if(length(unique(analysis$species))<5) stop("Too few species")

pair_boot_mean <- function(x,B,seed){
  x <- x[is.finite(x)]
  set.seed(seed)
  out <- replicate(B,mean(sample(x,length(x),replace=TRUE)))
  as.numeric(quantile(out,c(.025,.975),names=FALSE))
}

# Pair collapse.
pair <- aggregate(
  cbind(
    front_lead_early,front_lead_late,delta_front_lead,
    share_front_order_early,share_front_order_late,delta_share_front_order,
    source_phase_early,source_phase_late,delta_source_phase,
    signal_to_target_early,signal_to_target_late,delta_signal_to_target,
    source_arrival_sd_early,source_arrival_sd_late,delta_source_arrival_sd,
    target_arrival_sd_early,target_arrival_sd_late,delta_target_arrival_sd
  ) ~ pair_key + source_cell + target_cell,
  data=analysis,
  FUN=mean
)

# Species collapse.
sp <- aggregate(
  cbind(
    front_lead_early,front_lead_late,delta_front_lead,
    share_front_order_early,share_front_order_late,delta_share_front_order,
    source_phase_early,source_phase_late,delta_source_phase,
    signal_to_target_early,signal_to_target_late,delta_signal_to_target
  ) ~ species,
  data=analysis,
  FUN=mean
)

front_ci <- pair_boot_mean(pair$delta_front_lead,B,SEED)
source_phase_ci <- pair_boot_mean(pair$delta_source_phase,B,SEED+1L)
signal_target_ci <- pair_boot_mean(pair$delta_signal_to_target,B,SEED+2L)

# Equal-species bootstrap through pair incidence.
pair_delta <- setNames(pair$delta_front_lead,pair$pair_key)
inc <- unique(analysis[,c("species","pair_key")])
inc_by_pair <- split(inc$species,inc$pair_key)
keys <- pair$pair_key
set.seed(SEED+10L)
sp_boot <- rep(NA_real_,B)
for(b in seq_len(B)){
  draw <- sample(keys,length(keys),replace=TRUE)
  lists <- list()
  for(pk in draw){
    ss <- inc_by_pair[[pk]]
    val <- pair_delta[[pk]]
    for(spp in ss) lists[[spp]] <- c(lists[[spp]],val)
  }
  means <- vapply(lists,mean,numeric(1))
  sp_boot[b] <- mean(means)
}
sp_ci <- as.numeric(quantile(sp_boot,c(.025,.975),names=FALSE))

summary_row <- data.frame(
  eligible_units=nrow(analysis),
  unique_pairs=nrow(pair),
  species=length(unique(analysis$species)),

  front_lead_early=mean(pair$front_lead_early),
  front_lead_late=mean(pair$front_lead_late),
  delta_front_lead=mean(pair$delta_front_lead),
  delta_front_lead_ci_low_95=front_ci[1],
  delta_front_lead_ci_high_95=front_ci[2],
  pairs_source_front_before_target_majority_early=
    sum(pair$share_front_order_early>0.5),
  pairs_source_front_before_target_majority_late=
    sum(pair$share_front_order_late>0.5),
  pair_mean_share_order_early=mean(pair$share_front_order_early),
  pair_mean_share_order_late=mean(pair$share_front_order_late),

  equal_species_front_lead_early=mean(sp$front_lead_early),
  equal_species_front_lead_late=mean(sp$front_lead_late),
  equal_species_delta_front_lead=mean(sp$delta_front_lead),
  equal_species_delta_ci_low_95=sp_ci[1],
  equal_species_delta_ci_high_95=sp_ci[2],

  source_phase_early=mean(pair$source_phase_early),
  source_phase_late=mean(pair$source_phase_late),
  delta_source_phase=mean(pair$delta_source_phase),
  delta_source_phase_ci_low_95=source_phase_ci[1],
  delta_source_phase_ci_high_95=source_phase_ci[2],

  signal_to_target_early=mean(pair$signal_to_target_early),
  signal_to_target_late=mean(pair$signal_to_target_late),
  delta_signal_to_target=mean(pair$delta_signal_to_target),
  delta_signal_to_target_ci_low_95=signal_target_ci[1],
  delta_signal_to_target_ci_high_95=signal_target_ci[2],

  source_arrival_sd_early=mean(pair$source_arrival_sd_early,na.rm=TRUE),
  source_arrival_sd_late=mean(pair$source_arrival_sd_late,na.rm=TRUE),
  target_arrival_sd_early=mean(pair$target_arrival_sd_early,na.rm=TRUE),
  target_arrival_sd_late=mean(pair$target_arrival_sd_late,na.rm=TRUE),

  species_positive_delta_front=sum(sp$delta_front_lead>0),
  species_negative_delta_front=sum(sp$delta_front_lead<0),
  pairs_positive_delta_front=sum(pair$delta_front_lead>0),
  pairs_negative_delta_front=sum(pair$delta_front_lead<0)
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  rows,
  "outputs/payoff_b_v8_source_stage_access_year_rows.csv",
  row.names=FALSE
)
write.csv(
  analysis,
  "outputs/payoff_b_v8_source_stage_access_units.csv",
  row.names=FALSE
)
write.csv(
  pair,
  "outputs/payoff_b_v8_source_stage_access_pairs.csv",
  row.names=FALSE
)
write.csv(
  sp,
  "outputs/payoff_b_v8_source_stage_access_species.csv",
  row.names=FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_source_stage_access_summary.csv",
  row.names=FALSE
)

cat("\nPOSTHOC SOURCE-STAGE ACCESS DIAGNOSTIC\n")
print(summary_row)
