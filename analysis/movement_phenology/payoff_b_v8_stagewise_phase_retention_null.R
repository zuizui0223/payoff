#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC / OUTCOME-INFORMED STAGEWISE PHASE-RETENTION STRUCTURAL NULL.
#
# Question:
# In the restricted stagewise subset, is year-specific source-to-target
# population phase retention distinguishable from environmental geometry alone?
#
# Observed local phase:
#   source_phase = source arrival - source green-up
#   target_phase = target arrival - target green-up
#
# We estimate within-route phase retention using:
#   target_phase ~ source_phase + unit FE + year FE
#
# separately by period.
#
# Structural null 1 (fixed arrival):
# hold source and target arrival fixed at the unit-period mean, allowing only
# green-up to vary. This preserves environmental geometry but removes
# year-specific bird timing.
#
# Structural null 2 (arrival permutation):
# within each unit-period, jointly permute the annual pair
# (source arrival, target arrival) relative to green-up years, preserving
# source-target front timing distributions while destroying year-specific
# alignment to green-up.
#
# This is population-front geometry, not individual feedback.

GATE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_admission_gate.R"
if (!file.exists(GATE_SCRIPT)) stop("Missing admission-gate script")
source(GATE_SCRIPT, local=FALSE)

BOOT_B <- 10000L
PERM_B <- 2000L
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
  "species","year","cell","arr_GAM_mean","gr_mn"
)]
d$year <- as.integer(d$year)
d$cell <- as.numeric(as.character(d$cell))
d$arr_GAM_mean <- as.numeric(d$arr_GAM_mean)
d$gr_mn <- as.numeric(d$gr_mn)

base <- d[
  is.finite(d$year) &
    is.finite(d$cell) &
    is.finite(d$arr_GAM_mean) &
    is.finite(d$gr_mn),
  ,
  drop=FALSE
]
base <- unique(base)

src <- base
names(src)[names(src)=="cell"] <- "source_cell"
names(src)[names(src)=="arr_GAM_mean"] <- "source_arrival"
names(src)[names(src)=="gr_mn"] <- "source_greenup"

tgt <- base
names(tgt)[names(tgt)=="cell"] <- "target_cell"
names(tgt)[names(tgt)=="arr_GAM_mean"] <- "target_arrival"
names(tgt)[names(tgt)=="gr_mn"] <- "target_greenup"

rows <- merge(
  map,
  src[,c("species","year","source_cell","source_arrival","source_greenup")],
  by=c("species","source_cell"),
  all=FALSE,
  sort=FALSE
)
rows <- merge(
  rows,
  tgt[,c("species","year","target_cell","target_arrival","target_greenup")],
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
rows$period <- ifelse(rows$year<=EARLY_END,"early","late")
rows$unit_id <- paste(
  rows$species,rows$source_cell,rows$target_cell,sep="::"
)

# Same eligibility as stagewise result.
counts <- aggregate(
  year ~ unit_id + species + source_cell + target_cell + pair_key + period,
  data=rows,
  FUN=function(x) length(unique(x))
)
ce <- counts[counts$period=="early",]
cl <- counts[counts$period=="late",]
names(ce)[names(ce)=="year"] <- "early_n"
names(cl)[names(cl)=="year"] <- "late_n"
ce$period <- NULL
cl$period <- NULL
units <- merge(
  ce,cl,
  by=c("unit_id","species","source_cell","target_cell","pair_key"),
  all=FALSE
)
units <- units[
  units$early_n>=MIN_YEARS &
    units$late_n>=MIN_YEARS,
  ,
  drop=FALSE
]
rows <- rows[rows$unit_id %in% units$unit_id,,drop=FALSE]

rows$source_phase <- rows$source_arrival - rows$source_greenup
rows$target_phase <- rows$target_arrival - rows$target_greenup

# Fixed-arrival null: unit-period mean arrival.
mu_source <- aggregate(
  source_arrival ~ unit_id + period,
  data=rows,
  FUN=mean
)
mu_target <- aggregate(
  target_arrival ~ unit_id + period,
  data=rows,
  FUN=mean
)
names(mu_source)[3] <- "source_arrival_fixed"
names(mu_target)[3] <- "target_arrival_fixed"
rows <- merge(rows,mu_source,by=c("unit_id","period"),all.x=TRUE,sort=FALSE)
rows <- merge(rows,mu_target,by=c("unit_id","period"),all.x=TRUE,sort=FALSE)
rows$source_phase_fixed <- rows$source_arrival_fixed - rows$source_greenup
rows$target_phase_fixed <- rows$target_arrival_fixed - rows$target_greenup

fit_retention <- function(df,source_col,target_col,weights=NULL){
  z <- df[
    is.finite(df[[source_col]]) &
      is.finite(df[[target_col]]),
    ,
    drop=FALSE
  ]
  if(nrow(z)<20 || length(unique(z$unit_id))<3) return(NA_real_)
  z$source_x <- z[[source_col]]
  z$target_y <- z[[target_col]]
  if(is.null(weights)){
    fit <- try(
      lm(target_y ~ source_x + factor(unit_id) + factor(year),data=z),
      silent=TRUE
    )
  }else{
    z$w <- weights[match(rownames(z),rownames(df))]
    fit <- try(
      lm(
        target_y ~ source_x + factor(unit_id) + factor(year),
        data=z,weights=w
      ),
      silent=TRUE
    )
  }
  if(inherits(fit,"try-error")) return(NA_real_)
  unname(coef(fit)["source_x"])
}

estimate_period <- function(df,source_col,target_col){
  c(
    early=fit_retention(
      df[df$period=="early",,drop=FALSE],
      source_col,target_col
    ),
    late=fit_retention(
      df[df$period=="late",,drop=FALSE],
      source_col,target_col
    )
  )
}

obs <- estimate_period(rows,"source_phase","target_phase")
fix <- estimate_period(rows,"source_phase_fixed","target_phase_fixed")

# Pair bootstrap via frequency weights. Preserve all rows in each environmental
# pair and duplicated sampling through integer weights.
pair_keys <- unique(rows$pair_key)
P <- length(pair_keys)

fit_retention_weighted <- function(df,source_col,target_col,pair_counts){
  z <- df[
    is.finite(df[[source_col]]) &
      is.finite(df[[target_col]]),
    ,
    drop=FALSE
  ]
  z$source_x <- z[[source_col]]
  z$target_y <- z[[target_col]]
  z$w <- as.numeric(pair_counts[z$pair_key])
  z <- z[is.finite(z$w) & z$w>0,,drop=FALSE]
  if(nrow(z)<20) return(NA_real_)
  fit <- try(
    lm(
      target_y ~ source_x + factor(unit_id) + factor(year),
      data=z,weights=w
    ),
    silent=TRUE
  )
  if(inherits(fit,"try-error")) return(NA_real_)
  unname(coef(fit)["source_x"])
}

set.seed(SEED)
boot <- data.frame(
  obs_early=rep(NA_real_,BOOT_B),
  obs_late=rep(NA_real_,BOOT_B),
  fixed_early=rep(NA_real_,BOOT_B),
  fixed_late=rep(NA_real_,BOOT_B)
)

for(b in seq_len(BOOT_B)){
  draw <- sample(pair_keys,P,replace=TRUE)
  cnt <- table(factor(draw,levels=pair_keys))
  cnt <- as.numeric(cnt)
  names(cnt) <- pair_keys
  for(pp in c("early","late")){
    z <- rows[rows$period==pp,,drop=FALSE]
    boot[b,paste0("obs_",pp)] <- fit_retention_weighted(
      z,"source_phase","target_phase",cnt
    )
    boot[b,paste0("fixed_",pp)] <- fit_retention_weighted(
      z,"source_phase_fixed","target_phase_fixed",cnt
    )
  }
}

boot$obs_minus_fixed_early <- boot$obs_early-boot$fixed_early
boot$obs_minus_fixed_late <- boot$obs_late-boot$fixed_late
boot$delta_obs <- boot$obs_late-boot$obs_early
boot$delta_fixed <- boot$fixed_late-boot$fixed_early
boot$delta_difference <- boot$delta_obs-boot$delta_fixed

qci <- function(x){
  as.numeric(quantile(x[is.finite(x)],c(.025,.975),names=FALSE))
}

# Arrival permutation null, jointly permuting source/target arrivals within
# unit-period relative to green-up years.
groups <- split(seq_len(nrow(rows)),paste(rows$unit_id,rows$period,sep="::"))
set.seed(SEED+1000L)
perm <- data.frame(
  early=rep(NA_real_,PERM_B),
  late=rep(NA_real_,PERM_B)
)

for(b in seq_len(PERM_B)){
  z <- rows
  s_arr <- z$source_arrival
  t_arr <- z$target_arrival
  for(ix in groups){
    ord <- sample(seq_along(ix),length(ix),replace=FALSE)
    s_arr[ix] <- z$source_arrival[ix][ord]
    t_arr[ix] <- z$target_arrival[ix][ord]
  }
  z$source_phase_perm <- s_arr-z$source_greenup
  z$target_phase_perm <- t_arr-z$target_greenup
  p <- estimate_period(z,"source_phase_perm","target_phase_perm")
  perm$early[b] <- p[["early"]]
  perm$late[b] <- p[["late"]]
}
perm$delta <- perm$late-perm$early

summary_row <- data.frame(
  eligible_units=nrow(units),
  unique_pairs=length(unique(rows$pair_key)),
  species=length(unique(rows$species)),

  observed_retention_early=obs[["early"]],
  observed_retention_late=obs[["late"]],
  observed_delta=obs[["late"]]-obs[["early"]],

  fixed_retention_early=fix[["early"]],
  fixed_retention_late=fix[["late"]],
  fixed_delta=fix[["late"]]-fix[["early"]],

  observed_minus_fixed_early=obs[["early"]]-fix[["early"]],
  obs_minus_fixed_early_ci_low_95=qci(boot$obs_minus_fixed_early)[1],
  obs_minus_fixed_early_ci_high_95=qci(boot$obs_minus_fixed_early)[2],

  observed_minus_fixed_late=obs[["late"]]-fix[["late"]],
  obs_minus_fixed_late_ci_low_95=qci(boot$obs_minus_fixed_late)[1],
  obs_minus_fixed_late_ci_high_95=qci(boot$obs_minus_fixed_late)[2],

  delta_difference=(obs[["late"]]-obs[["early"]]) -
    (fix[["late"]]-fix[["early"]]),
  delta_difference_ci_low_95=qci(boot$delta_difference)[1],
  delta_difference_ci_high_95=qci(boot$delta_difference)[2],

  perm_early_median=median(perm$early,na.rm=TRUE),
  perm_early_low_95=qci(perm$early)[1],
  perm_early_high_95=qci(perm$early)[2],
  perm_fraction_early_le_observed=mean(perm$early<=obs[["early"]],na.rm=TRUE),

  perm_late_median=median(perm$late,na.rm=TRUE),
  perm_late_low_95=qci(perm$late)[1],
  perm_late_high_95=qci(perm$late)[2],
  perm_fraction_late_le_observed=mean(perm$late<=obs[["late"]],na.rm=TRUE),

  perm_delta_median=median(perm$delta,na.rm=TRUE),
  perm_delta_low_95=qci(perm$delta)[1],
  perm_delta_high_95=qci(perm$delta)[2],
  perm_fraction_delta_le_observed=mean(
    perm$delta <= (obs[["late"]]-obs[["early"]]),
    na.rm=TRUE
  ),

  bootstrap_replicates=BOOT_B,
  permutation_replicates=PERM_B,
  seed=SEED
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  rows,
  "outputs/payoff_b_v8_stagewise_retention_rows.csv",
  row.names=FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_stagewise_retention_summary.csv",
  row.names=FALSE
)
write.csv(
  boot,
  "outputs/payoff_b_v8_stagewise_retention_bootstrap.csv",
  row.names=FALSE
)
write.csv(
  perm,
  "outputs/payoff_b_v8_stagewise_retention_permutation.csv",
  row.names=FALSE
)

cat("\nPOSTHOC STAGEWISE PHASE-RETENTION STRUCTURAL NULL\n")
print(summary_row)
