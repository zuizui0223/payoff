#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC REPRESENTATIVENESS AUDIT FOR THE STAGEWISE SUBSET.
#
# The stagewise population-front analysis retains only source-target-species
# units with >=6 arrival estimates at BOTH source and target in BOTH periods.
# This script asks how the resulting unique-pair subset differs from the full
# environmental V8 pair network.
#
# No formal generalization test is intended. Standardized mean differences are
# descriptive selection diagnostics.

GATE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_admission_gate.R"
if (!file.exists(GATE_SCRIPT)) stop("Missing admission-gate script")
source(GATE_SCRIPT, local=FALSE)

MIN_YEARS <- 6L

eligible_map <- eligible
eligible_map$pair_key <- paste(
  eligible_map$source_cell,
  eligible_map$target_cell,
  sep="->"
)

# Rebuild unique environmental pair set.
pair_seed <- unique(eligible_map[,c(
  "pair_key","source_cell","target_cell","source_target_distance_km"
)])

# Environmental window statistics without bootstrap.
pair_window <- function(source_cell,target_cell,start_year,end_year){
  src <- green[
    green$cell==source_cell &
      green$year>=start_year &
      green$year<=end_year,
    c("year","gr_mn"),
    drop=FALSE
  ]
  tgt <- green[
    green$cell==target_cell &
      green$year>=start_year &
      green$year<=end_year,
    c("year","gr_mn"),
    drop=FALSE
  ]
  names(src)[2] <- "source_greenup"
  names(tgt)[2] <- "target_greenup"
  z <- merge(src,tgt,by="year",all=FALSE)
  z <- z[
    is.finite(z$year) &
      is.finite(z$source_greenup) &
      is.finite(z$target_greenup),
    ,
    drop=FALSE
  ]
  z <- z[!duplicated(z$year),,drop=FALSE]
  z <- z[order(z$year),,drop=FALSE]
  n <- nrow(z)
  if(n<MIN_PAIRS_PER_WINDOW){
    return(c(
      n=n,rho=NA_real_,target_sd=NA_real_,
      loo_value=NA_real_
    ))
  }

  src_fit <- lm(source_greenup~year,data=z)
  tgt_fit <- lm(target_greenup~year,data=z)
  x <- resid(src_fit)
  y <- resid(tgt_fit)
  if(!is.finite(sd(x)) || sd(x)<=0 || !is.finite(sd(y)) || sd(y)<=0){
    return(c(
      n=n,rho=NA_real_,target_sd=NA_real_,
      loo_value=NA_real_
    ))
  }

  loo_source_err <- rep(NA_real_,n)
  loo_null_err <- rep(NA_real_,n)
  for(j in seq_len(n)){
    tr <- z[-j,,drop=FALSE]
    te <- z[j,,drop=FALSE]
    sf <- lm(source_greenup~year,data=tr)
    tf <- lm(target_greenup~year,data=tr)
    xtr <- resid(sf)
    ytr <- resid(tf)
    if(!is.finite(sd(xtr)) || sd(xtr)<=0) next
    mod <- lm(ytr~xtr)
    sx <- as.numeric(predict(sf,newdata=te))
    ty <- as.numeric(predict(tf,newdata=te))
    xh <- te$source_greenup-sx
    ap <- as.numeric(coef(mod)[1]+coef(mod)[2]*xh)
    pred_source <- ty+ap
    loo_source_err[j] <- te$target_greenup-pred_source
    loo_null_err[j] <- te$target_greenup-ty
  }

  if(!all(is.finite(loo_source_err)) || !all(is.finite(loo_null_err))){
    value <- NA_real_
  }else{
    value <- mean(loo_null_err^2)-mean(loo_source_err^2)
  }

  c(
    n=n,
    rho=cor(x,y),
    target_sd=sd(y),
    loo_value=value
  )
}

early <- t(mapply(
  pair_window,
  pair_seed$source_cell,
  pair_seed$target_cell,
  MoreArgs=list(start_year=EARLY_START,end_year=EARLY_END)
))
late <- t(mapply(
  pair_window,
  pair_seed$source_cell,
  pair_seed$target_cell,
  MoreArgs=list(start_year=LATE_START,end_year=LATE_END)
))

pairs <- pair_seed
for(nm in c("rho","target_sd","loo_value")){
  pairs[[paste0(nm,"_early")]] <- as.numeric(early[,nm])
  pairs[[paste0(nm,"_late")]] <- as.numeric(late[,nm])
  pairs[[paste0("delta_",nm)]] <-
    pairs[[paste0(nm,"_late")]]-pairs[[paste0(nm,"_early")]]
}
pairs$early_n <- as.integer(early[,"n"])
pairs$late_n <- as.integer(late[,"n"])
pairs <- pairs[
  pairs$early_n>=MIN_PAIRS_PER_WINDOW &
    pairs$late_n>=MIN_PAIRS_PER_WINDOW &
    is.finite(pairs$rho_early) &
    is.finite(pairs$rho_late) &
    is.finite(pairs$loo_value_early) &
    is.finite(pairs$loo_value_late),
  ,
  drop=FALSE
]

# Stagewise availability subset: reproduce the stagewise script exactly by
# requiring same-year source and target rows with finite arrival AND green-up.
arr <- dat[,c("species","year","cell","arr_GAM_mean","gr_mn")]
arr$year <- as.integer(arr$year)
arr$cell <- as.numeric(as.character(arr$cell))
arr$arr_GAM_mean <- as.numeric(arr$arr_GAM_mean)
arr$gr_mn <- as.numeric(arr$gr_mn)
arr <- arr[
  is.finite(arr$year) &
    is.finite(arr$cell) &
    is.finite(arr$arr_GAM_mean) &
    is.finite(arr$gr_mn),
  ,
  drop=FALSE
]
arr <- unique(arr)

unit_map <- unique(eligible_map[,c(
  "species","pair_key","source_cell","target_cell"
)])

src_arr <- arr
names(src_arr)[names(src_arr)=="cell"] <- "source_cell"
names(src_arr)[names(src_arr)=="arr_GAM_mean"] <- "source_arrival"
names(src_arr)[names(src_arr)=="gr_mn"] <- "source_greenup"

tgt_arr <- arr
names(tgt_arr)[names(tgt_arr)=="cell"] <- "target_cell"
names(tgt_arr)[names(tgt_arr)=="arr_GAM_mean"] <- "target_arrival"
names(tgt_arr)[names(tgt_arr)=="gr_mn"] <- "target_greenup"

stage_rows <- merge(
  unit_map,
  src_arr[,c("species","year","source_cell","source_arrival","source_greenup")],
  by=c("species","source_cell"),
  all=FALSE,
  sort=FALSE
)
stage_rows <- merge(
  stage_rows,
  tgt_arr[,c("species","year","target_cell","target_arrival","target_greenup")],
  by=c("species","target_cell","year"),
  all=FALSE,
  sort=FALSE
)
stage_rows <- stage_rows[
  stage_rows$year>=EARLY_START &
    stage_rows$year<=LATE_END,
  ,
  drop=FALSE
]
stage_rows$period <- ifelse(stage_rows$year<=EARLY_END,"early","late")

stage_counts <- aggregate(
  year ~ species + pair_key + source_cell + target_cell + period,
  data=stage_rows,
  FUN=function(x) length(unique(x))
)
se <- stage_counts[stage_counts$period=="early",]
sl <- stage_counts[stage_counts$period=="late",]
names(se)[names(se)=="year"] <- "early_n"
names(sl)[names(sl)=="year"] <- "late_n"
se$period <- NULL
sl$period <- NULL

stage_units <- merge(
  se,sl,
  by=c("species","pair_key","source_cell","target_cell"),
  all=FALSE
)
stage_units <- stage_units[
  stage_units$early_n>=MIN_YEARS &
    stage_units$late_n>=MIN_YEARS,
  ,
  drop=FALSE
]
stage_keys <- unique(stage_units$pair_key)
pairs$stage_subset <- pairs$pair_key %in% stage_keys

smd <- function(a,b){
  a <- a[is.finite(a)]
  b <- b[is.finite(b)]
  if(length(a)<2 || length(b)<2) return(NA_real_)
  pooled <- sqrt(
    ((length(a)-1)*var(a)+(length(b)-1)*var(b)) /
      (length(a)+length(b)-2)
  )
  if(!is.finite(pooled) || pooled<=0) return(NA_real_)
  (mean(a)-mean(b))/pooled
}

metric_names <- c(
  "source_target_distance_km",
  "rho_early","rho_late","delta_rho",
  "target_sd_early","target_sd_late","delta_target_sd",
  "loo_value_early","loo_value_late","delta_loo_value"
)

summary_list <- lapply(metric_names,function(nm){
  a <- pairs[[nm]][pairs$stage_subset]
  b <- pairs[[nm]][!pairs$stage_subset]
  data.frame(
    metric=nm,
    stage_n=sum(is.finite(a)),
    stage_mean=mean(a,na.rm=TRUE),
    stage_median=median(a,na.rm=TRUE),
    excluded_n=sum(is.finite(b)),
    excluded_mean=mean(b,na.rm=TRUE),
    excluded_median=median(b,na.rm=TRUE),
    standardized_mean_difference=smd(a,b)
  )
})
summary_df <- do.call(rbind,summary_list)

status <- data.frame(
  full_pairs=nrow(pairs),
  stage_pairs=sum(pairs$stage_subset),
  excluded_pairs=sum(!pairs$stage_subset),
  stage_species=length(unique(stage_units$species)),
  stage_units=nrow(stage_units),
  note="descriptive_subset_selection_audit"
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  pairs,
  "outputs/payoff_b_v8_stagewise_subset_pairs.csv",
  row.names=FALSE
)
write.csv(
  summary_df,
  "outputs/payoff_b_v8_stagewise_subset_summary.csv",
  row.names=FALSE
)
write.csv(
  stage_units,
  "outputs/payoff_b_v8_stagewise_subset_units.csv",
  row.names=FALSE
)
write.csv(
  status,
  "outputs/payoff_b_v8_stagewise_subset_status.csv",
  row.names=FALSE
)

cat("\nPOSTHOC STAGEWISE SUBSET REPRESENTATIVENESS AUDIT\n")
print(status)
print(summary_df)
