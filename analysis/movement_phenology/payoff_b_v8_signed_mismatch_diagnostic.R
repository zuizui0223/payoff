#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC / OUTCOME-INFORMED SIGNED-MISMATCH DIAGNOSTIC.
#
# The frozen bird mismatch endpoint used log1p(abs(greenup-arrival)).
# This diagnostic restores the sign:
#
#   signed_lag = arrival - target_greenup
#
# Positive = bird arrives after mid-green-up; negative = before.
#
# Purpose:
# determine whether stable absolute mismatch hides a directional shift in
# arrival relative to green-up, and decompose that shift into bird-arrival and
# target-green-up changes.
#
# This does not alter any frozen endpoint.

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
  sep = "->"
)

bird <- dat[, c(
  "species","year","cell","arr_GAM_mean","gr_mn"
)]
bird$year <- as.integer(bird$year)
bird$cell <- as.numeric(as.character(bird$cell))
bird$arr_GAM_mean <- as.numeric(bird$arr_GAM_mean)
bird$gr_mn <- as.numeric(bird$gr_mn)
bird <- bird[
  is.finite(bird$year) &
    is.finite(bird$cell) &
    is.finite(bird$arr_GAM_mean) &
    is.finite(bird$gr_mn),
  ,
  drop=FALSE
]
bird <- unique(bird)
bird$signed_lag <- bird$arr_GAM_mean - bird$gr_mn
bird$abs_lag <- abs(bird$signed_lag)

emap <- unique(eligible_map[,c(
  "species","target_cell","source_cell","pair_key"
)])

window_stats <- function(sp,target_cell,start_year,end_year){
  z <- bird[
    bird$species==sp &
      bird$cell==target_cell &
      bird$year>=start_year &
      bird$year<=end_year,
    ,
    drop=FALSE
  ]
  z <- z[!duplicated(z$year),,drop=FALSE]
  c(
    n=nrow(z),
    signed=if(nrow(z)>0) mean(z$signed_lag) else NA_real_,
    abs=if(nrow(z)>0) mean(z$abs_lag) else NA_real_,
    arrival=if(nrow(z)>0) mean(z$arr_GAM_mean) else NA_real_,
    greenup=if(nrow(z)>0) mean(z$gr_mn) else NA_real_,
    share_after=if(nrow(z)>0) mean(z$signed_lag>0) else NA_real_
  )
}

early <- t(mapply(
  window_stats,
  emap$species,
  emap$target_cell,
  MoreArgs=list(start_year=EARLY_START,end_year=EARLY_END)
))
late <- t(mapply(
  window_stats,
  emap$species,
  emap$target_cell,
  MoreArgs=list(start_year=LATE_START,end_year=LATE_END)
))

x <- emap
x$early_n <- as.integer(early[,"n"])
x$late_n <- as.integer(late[,"n"])
for(nm in c("signed","abs","arrival","greenup","share_after")){
  x[[paste0(nm,"_early")]] <- as.numeric(early[,nm])
  x[[paste0(nm,"_late")]] <- as.numeric(late[,nm])
  x[[paste0("delta_",nm)]] <-
    x[[paste0(nm,"_late")]] - x[[paste0(nm,"_early")]]
}

analysis <- x[
  x$early_n>=MIN_YEARS &
    x$late_n>=MIN_YEARS &
    is.finite(x$signed_early) &
    is.finite(x$signed_late),
  ,
  drop=FALSE
]

if(nrow(analysis)<20) stop("Too few eligible rows")
if(length(unique(analysis$pair_key))<20) stop("Too few pairs")
if(length(unique(analysis$species))<5) stop("Too few species")

# Bootstrap unique environmental pairs, carrying all species-target rows.
rows_by_pair <- split(analysis,analysis$pair_key)
pair_keys <- unique(analysis$pair_key)
P <- length(pair_keys)

stat_fun <- function(df,field){
  mean(df[[field]])
}
eq_species_fun <- function(df,field){
  a <- aggregate(df[[field]],list(species=df$species),mean)
  mean(a$x)
}

set.seed(SEED)
boot <- data.frame(
  delta_signed=rep(NA_real_,B),
  delta_abs=rep(NA_real_,B),
  delta_arrival=rep(NA_real_,B),
  delta_greenup=rep(NA_real_,B),
  eq_delta_signed=rep(NA_real_,B),
  eq_delta_abs=rep(NA_real_,B),
  eq_delta_arrival=rep(NA_real_,B),
  eq_delta_greenup=rep(NA_real_,B)
)

for(b in seq_len(B)){
  draw <- sample(pair_keys,P,replace=TRUE)
  zz <- do.call(rbind,lapply(seq_along(draw),function(i){
    z <- rows_by_pair[[draw[i]]]
    z$draw_id <- i
    z
  }))
  for(field in c("delta_signed","delta_abs","delta_arrival","delta_greenup")){
    boot[b,field] <- stat_fun(zz,field)
    boot[b,paste0("eq_",field)] <- eq_species_fun(zz,field)
  }
}

ci <- function(v) as.numeric(quantile(v,c(.025,.975),na.rm=TRUE,names=FALSE))

sp <- aggregate(
  cbind(
    signed_early,signed_late,delta_signed,
    abs_early,abs_late,delta_abs,
    arrival_early,arrival_late,delta_arrival,
    greenup_early,greenup_late,delta_greenup,
    share_after_early,share_after_late,delta_share_after
  ) ~ species,
  data=analysis,
  FUN=mean
)

pair <- aggregate(
  cbind(
    signed_early,signed_late,delta_signed,
    abs_early,abs_late,delta_abs,
    arrival_early,arrival_late,delta_arrival,
    greenup_early,greenup_late,delta_greenup,
    share_after_early,share_after_late,delta_share_after
  ) ~ pair_key + source_cell + target_cell,
  data=analysis,
  FUN=mean
)

summary_row <- data.frame(
  eligible_rows=nrow(analysis),
  unique_pairs=length(unique(analysis$pair_key)),
  species=length(unique(analysis$species)),

  signed_early=mean(analysis$signed_early),
  signed_late=mean(analysis$signed_late),
  delta_signed=mean(analysis$delta_signed),
  delta_signed_ci_low_95=ci(boot$delta_signed)[1],
  delta_signed_ci_high_95=ci(boot$delta_signed)[2],

  eq_signed_early=mean(sp$signed_early),
  eq_signed_late=mean(sp$signed_late),
  eq_delta_signed=mean(sp$delta_signed),
  eq_delta_signed_ci_low_95=ci(boot$eq_delta_signed)[1],
  eq_delta_signed_ci_high_95=ci(boot$eq_delta_signed)[2],

  abs_early=mean(analysis$abs_early),
  abs_late=mean(analysis$abs_late),
  delta_abs=mean(analysis$delta_abs),
  delta_abs_ci_low_95=ci(boot$delta_abs)[1],
  delta_abs_ci_high_95=ci(boot$delta_abs)[2],

  eq_abs_early=mean(sp$abs_early),
  eq_abs_late=mean(sp$abs_late),
  eq_delta_abs=mean(sp$delta_abs),
  eq_delta_abs_ci_low_95=ci(boot$eq_delta_abs)[1],
  eq_delta_abs_ci_high_95=ci(boot$eq_delta_abs)[2],

  arrival_early=mean(analysis$arrival_early),
  arrival_late=mean(analysis$arrival_late),
  delta_arrival=mean(analysis$delta_arrival),
  delta_arrival_ci_low_95=ci(boot$delta_arrival)[1],
  delta_arrival_ci_high_95=ci(boot$delta_arrival)[2],

  greenup_early=mean(analysis$greenup_early),
  greenup_late=mean(analysis$greenup_late),
  delta_greenup=mean(analysis$delta_greenup),
  delta_greenup_ci_low_95=ci(boot$delta_greenup)[1],
  delta_greenup_ci_high_95=ci(boot$delta_greenup)[2],

  eq_delta_arrival=mean(sp$delta_arrival),
  eq_delta_arrival_ci_low_95=ci(boot$eq_delta_arrival)[1],
  eq_delta_arrival_ci_high_95=ci(boot$eq_delta_arrival)[2],

  eq_delta_greenup=mean(sp$delta_greenup),
  eq_delta_greenup_ci_low_95=ci(boot$eq_delta_greenup)[1],
  eq_delta_greenup_ci_high_95=ci(boot$eq_delta_greenup)[2],

  share_after_early=mean(analysis$share_after_early),
  share_after_late=mean(analysis$share_after_late),
  species_positive_delta_signed=sum(sp$delta_signed>0),
  species_negative_delta_signed=sum(sp$delta_signed<0),
  pair_positive_delta_signed=sum(pair$delta_signed>0),
  pair_negative_delta_signed=sum(pair$delta_signed<0)
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  analysis,
  "outputs/payoff_b_v8_signed_mismatch_rows.csv",
  row.names=FALSE
)
write.csv(
  sp,
  "outputs/payoff_b_v8_signed_mismatch_species.csv",
  row.names=FALSE
)
write.csv(
  pair,
  "outputs/payoff_b_v8_signed_mismatch_pairs.csv",
  row.names=FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_signed_mismatch_summary.csv",
  row.names=FALSE
)
write.csv(
  boot,
  "outputs/payoff_b_v8_signed_mismatch_bootstrap.csv",
  row.names=FALSE
)

cat("\nPOSTHOC SIGNED ARRIVAL-GREENUP MISMATCH DIAGNOSTIC\n")
print(summary_row)
