#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC MEASUREMENT-UNCERTAINTY AUDIT FOR THE STAGEWISE POPULATION-PHASE RESULT.
#
# The stagewise diagnostic uses posterior mean arrival dates. Arrival posterior
# SD is much larger in the early than late window. This audit asks whether the
# late-minus-early change in stagewise phase transformation remains negative
# after propagating reported arrival-date uncertainty and under inverse-variance
# weighting across years.
#
# This does NOT model covariance among cell-level arrival estimates and does NOT
# correct unknown bias. Independent Normal draws from reported posterior means
# and SDs are a transparent sensitivity approximation only.

GATE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_admission_gate.R"
if (!file.exists(GATE_SCRIPT)) stop("Missing V8 admission-gate script")
source(GATE_SCRIPT, local = FALSE)

SEED <- 20261006L
MC_B <- 5000L
BOOT_B <- 10000L
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

base <- d[
  is.finite(d$year) &
    is.finite(d$cell) &
    is.finite(d$arr_GAM_mean) &
    is.finite(d$arr_GAM_sd) &
    d$arr_GAM_sd > 0 &
    is.finite(d$gr_mn),
  c("species","year","cell","arr_GAM_mean","arr_GAM_sd","gr_mn"),
  drop=FALSE
]
base <- unique(base)

src <- base
names(src)[3:6] <- c(
  "source_cell","source_arrival","source_arrival_sd","source_greenup"
)
tgt <- base
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
rows$period <- ifelse(rows$year<=EARLY_END,"early","late")

# Freeze same eligibility as stagewise result.
count_unit <- aggregate(
  year ~ species + source_cell + target_cell + pair_key + period,
  data=rows,
  FUN=function(x) length(unique(x))
)
early_n <- count_unit[count_unit$period=="early",]
late_n <- count_unit[count_unit$period=="late",]
names(early_n)[names(early_n)=="year"] <- "early_n"
names(late_n)[names(late_n)=="year"] <- "late_n"
early_n$period <- NULL
late_n$period <- NULL

units <- merge(
  early_n,late_n,
  by=c("species","source_cell","target_cell","pair_key"),
  all=FALSE
)
units <- units[
  units$early_n>=MIN_YEARS &
    units$late_n>=MIN_YEARS,
  ,
  drop=FALSE
]
if(nrow(units)<20) stop("Too few eligible units")

rows$key <- paste(
  rows$species,rows$source_cell,rows$target_cell,sep="::"
)
units$key <- paste(
  units$species,units$source_cell,units$target_cell,sep="::"
)
rows <- rows[rows$key %in% units$key,,drop=FALSE]

# Helper: collapse unit-level deltas to environmental pair mean and equal species.
summarize_delta <- function(unit_df, value_col){
  pair <- aggregate(
    unit_df[[value_col]],
    list(pair_key=unit_df$pair_key),
    mean
  )
  names(pair)[2] <- "value"
  sp <- aggregate(
    unit_df[[value_col]],
    list(species=unit_df$species),
    mean
  )
  names(sp)[2] <- "value"
  c(
    pair_mean=mean(pair$value),
    equal_species_mean=mean(sp$value),
    pair_positive=sum(pair$value>0),
    pair_negative=sum(pair$value<0),
    species_positive=sum(sp$value>0),
    species_negative=sum(sp$value<0)
  )
}

# Posterior-mean baseline, reproduced directly.
mean_unit_stats <- function(rr){
  split_u <- split(rr,rr$key)
  out <- lapply(names(split_u),function(k){
    z <- split_u[[k]]
    ue <- units[units$key==k,,drop=FALSE]
    vals <- lapply(c("early","late"),function(pp){
      q <- z[z$period==pp,,drop=FALSE]
      source_phase <- q$source_arrival - q$source_greenup
      target_phase <- q$target_arrival - q$target_greenup
      mean(target_phase-source_phase)
    })
    data.frame(
      key=k,
      species=ue$species[1],
      pair_key=ue$pair_key[1],
      transform_early=vals[[1]],
      transform_late=vals[[2]],
      delta_transform=vals[[2]]-vals[[1]]
    )
  })
  do.call(rbind,out)
}

baseline_units <- mean_unit_stats(rows)
baseline_summary <- summarize_delta(baseline_units,"delta_transform")

# Inverse-variance weighted sensitivity.
# For each year, Var(target arrival - source arrival) is approximated by
# sd_target^2 + sd_source^2, ignoring covariance.
rows$transform_mean <-
  (rows$target_arrival - rows$target_greenup) -
  (rows$source_arrival - rows$source_greenup)
rows$transform_var <-
  rows$target_arrival_sd^2 + rows$source_arrival_sd^2
rows$ivw <- 1 / rows$transform_var

weighted_unit <- lapply(unique(rows$key),function(k){
  z <- rows[rows$key==k,,drop=FALSE]
  ue <- units[units$key==k,,drop=FALSE]
  wt <- function(q){
    sum(q$ivw*q$transform_mean)/sum(q$ivw)
  }
  e <- wt(z[z$period=="early",,drop=FALSE])
  l <- wt(z[z$period=="late",,drop=FALSE])
  data.frame(
    key=k,
    species=ue$species[1],
    pair_key=ue$pair_key[1],
    transform_early=e,
    transform_late=l,
    delta_transform=l-e
  )
})
weighted_unit <- do.call(rbind,weighted_unit)
weighted_summary <- summarize_delta(weighted_unit,"delta_transform")

# Pair-incidence bootstrap for weighted delta.
pair_boot_equal <- function(unit_df,B,seed){
  pair_value <- aggregate(
    delta_transform ~ pair_key,
    data=unit_df,
    FUN=mean
  )
  pv <- setNames(pair_value$delta_transform,pair_value$pair_key)
  inc <- unique(unit_df[,c("species","pair_key")])
  inc_by_pair <- split(inc$species,inc$pair_key)
  keys <- pair_value$pair_key

  set.seed(seed)
  pair_out <- rep(NA_real_,B)
  species_out <- rep(NA_real_,B)
  for(b in seq_len(B)){
    draw <- sample(keys,length(keys),replace=TRUE)
    pair_out[b] <- mean(pv[draw])
    lists <- list()
    for(pk in draw){
      spp <- inc_by_pair[[pk]]
      val <- pv[[pk]]
      for(ss in spp) lists[[ss]] <- c(lists[[ss]],val)
    }
    spm <- vapply(lists,mean,numeric(1))
    species_out[b] <- mean(spm)
  }
  list(
    pair_ci=as.numeric(quantile(pair_out,c(.025,.975),names=FALSE)),
    species_ci=as.numeric(quantile(species_out,c(.025,.975),names=FALSE))
  )
}

weighted_boot <- pair_boot_equal(weighted_unit,BOOT_B,SEED+1L)

# Posterior-normal Monte Carlo.
# Draw each annual source and target arrival independently from N(mean, sd),
# preserving observed green-up. Recompute period mean transforms within units,
# then pair/equal-species summaries.
row_n <- nrow(rows)
unit_keys <- unique(rows$key)
row_by_unit <- split(seq_len(row_n),rows$key)
unit_meta <- units[match(unit_keys,units$key),c("key","species","pair_key")]

set.seed(SEED)
mc_pair_mean <- rep(NA_real_,MC_B)
mc_species_mean <- rep(NA_real_,MC_B)
mc_pair_positive <- rep(NA_real_,MC_B)
mc_species_positive <- rep(NA_real_,MC_B)

for(b in seq_len(MC_B)){
  src_draw <- rnorm(
    row_n,
    mean=rows$source_arrival,
    sd=rows$source_arrival_sd
  )
  tgt_draw <- rnorm(
    row_n,
    mean=rows$target_arrival,
    sd=rows$target_arrival_sd
  )
  transform_draw <-
    (tgt_draw - rows$target_greenup) -
    (src_draw - rows$source_greenup)

  unit_delta <- rep(NA_real_,length(unit_keys))
  for(i in seq_along(unit_keys)){
    ix <- row_by_unit[[unit_keys[i]]]
    pe <- rows$period[ix]=="early"
    pl <- rows$period[ix]=="late"
    unit_delta[i] <-
      mean(transform_draw[ix][pl]) -
      mean(transform_draw[ix][pe])
  }

  ud <- data.frame(
    species=unit_meta$species,
    pair_key=unit_meta$pair_key,
    delta_transform=unit_delta
  )
  sm <- summarize_delta(ud,"delta_transform")
  mc_pair_mean[b] <- sm[["pair_mean"]]
  mc_species_mean[b] <- sm[["equal_species_mean"]]
  mc_pair_positive[b] <- sm[["pair_positive"]]
  mc_species_positive[b] <- sm[["species_positive"]]
}

mc_summary <- data.frame(
  replicates=MC_B,
  pair_mean_median=median(mc_pair_mean),
  pair_mean_ci_low_95=quantile(mc_pair_mean,.025),
  pair_mean_ci_high_95=quantile(mc_pair_mean,.975),
  fraction_pair_mean_negative=mean(mc_pair_mean<0),
  equal_species_median=median(mc_species_mean),
  equal_species_ci_low_95=quantile(mc_species_mean,.025),
  equal_species_ci_high_95=quantile(mc_species_mean,.975),
  fraction_equal_species_negative=mean(mc_species_mean<0),
  pair_positive_count_median=median(mc_pair_positive),
  species_positive_count_median=median(mc_species_positive)
)

summary_row <- data.frame(
  eligible_units=nrow(units),
  unique_pairs=length(unique(units$pair_key)),
  species=length(unique(units$species)),
  baseline_pair_mean_delta=baseline_summary[["pair_mean"]],
  baseline_equal_species_delta=baseline_summary[["equal_species_mean"]],
  weighted_pair_mean_delta=weighted_summary[["pair_mean"]],
  weighted_pair_ci_low_95=weighted_boot$pair_ci[1],
  weighted_pair_ci_high_95=weighted_boot$pair_ci[2],
  weighted_equal_species_delta=weighted_summary[["equal_species_mean"]],
  weighted_equal_species_ci_low_95=weighted_boot$species_ci[1],
  weighted_equal_species_ci_high_95=weighted_boot$species_ci[2],
  mean_source_sd_early=mean(rows$source_arrival_sd[rows$period=="early"]),
  mean_source_sd_late=mean(rows$source_arrival_sd[rows$period=="late"]),
  mean_target_sd_early=mean(rows$target_arrival_sd[rows$period=="early"]),
  mean_target_sd_late=mean(rows$target_arrival_sd[rows$period=="late"])
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  baseline_units,
  "outputs/payoff_b_v8_stagewise_measurement_baseline_units.csv",
  row.names=FALSE
)
write.csv(
  weighted_unit,
  "outputs/payoff_b_v8_stagewise_measurement_weighted_units.csv",
  row.names=FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_stagewise_measurement_summary.csv",
  row.names=FALSE
)
write.csv(
  mc_summary,
  "outputs/payoff_b_v8_stagewise_measurement_mc_summary.csv",
  row.names=FALSE
)
write.csv(
  data.frame(
    replicate=seq_len(MC_B),
    pair_mean_delta=mc_pair_mean,
    equal_species_delta=mc_species_mean,
    pair_positive_count=mc_pair_positive,
    species_positive_count=mc_species_positive
  ),
  "outputs/payoff_b_v8_stagewise_measurement_mc_draws.csv",
  row.names=FALSE
)

cat("\nPOSTHOC STAGEWISE MEASUREMENT-UNCERTAINTY AUDIT\n")
print(summary_row)
cat("\nPosterior-normal Monte Carlo:\n")
print(mc_summary)
