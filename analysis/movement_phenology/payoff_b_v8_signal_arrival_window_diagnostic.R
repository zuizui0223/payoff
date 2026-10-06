#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC / OUTCOME-INFORMED TEMPORAL-AVAILABILITY DIAGNOSTIC.
#
# Question:
# Is the frozen nonlocal source green-up signal temporally available before
# target arrival, and did the source-to-arrival lead window change between
# 2002-2009 and 2010-2017?
#
# This is NOT a direct measure of perception, actionability r(t), or actuator
# capacity. It is only a necessary temporal-order condition for the source
# signal to inform arrival timing.

PRIMARY_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_primary.R"
if (!file.exists(PRIMARY_SCRIPT)) stop("Missing V8 primary script")
source(PRIMARY_SCRIPT, local = FALSE)

B <- 10000L
SEED <- 20261006L
MIN_YEARS <- 6L

# Reconstruct source green-up by species-target mapping and join target arrival.
map <- unique(eligible_map[, c(
  "species", "target_cell", "source_cell", "pair_key"
)])
map <- map[map$pair_key %in% pairs$pair_key, , drop = FALSE]

bird <- dat[, c("species", "year", "cell", "arr_GAM_mean", "gr_mn")]
bird$year <- as.integer(bird$year)
bird$cell <- as.numeric(as.character(bird$cell))
bird$arr_GAM_mean <- as.numeric(bird$arr_GAM_mean)
bird$gr_mn <- as.numeric(bird$gr_mn)

target_arrival <- bird[
  is.finite(bird$year) &
    is.finite(bird$cell) &
    is.finite(bird$arr_GAM_mean),
  c("species", "year", "cell", "arr_GAM_mean"),
  drop = FALSE
]
target_arrival <- unique(target_arrival)
names(target_arrival)[3] <- "target_cell"

source_green <- green[, c("year", "cell", "gr_mn")]
names(source_green) <- c("year", "source_cell", "source_greenup")

rows <- merge(
  map,
  target_arrival,
  by = c("species", "target_cell"),
  all = FALSE,
  sort = FALSE
)
rows <- merge(
  rows,
  source_green,
  by = c("year", "source_cell"),
  all = FALSE,
  sort = FALSE
)
rows <- rows[
  rows$year >= EARLY_START &
    rows$year <= LATE_END &
    is.finite(rows$arr_GAM_mean) &
    is.finite(rows$source_greenup),
  ,
  drop = FALSE
]
rows <- unique(rows)

# Positive means source green-up occurred before target arrival.
rows$source_to_arrival_lead_days <- rows$arr_GAM_mean - rows$source_greenup
rows$source_before_arrival <- rows$source_to_arrival_lead_days > 0
rows$period <- ifelse(rows$year <= EARLY_END, "early", "late")

# Species-target window summaries.
window_summary <- function(sp, target_cell, period_name) {
  z <- rows[
    rows$species == sp &
      rows$target_cell == target_cell &
      rows$period == period_name,
    ,
    drop = FALSE
  ]
  z <- z[!duplicated(z$year), , drop = FALSE]
  c(
    n = nrow(z),
    mean_lead = if (nrow(z)>0) mean(z$source_to_arrival_lead_days) else NA_real_,
    median_lead = if (nrow(z)>0) median(z$source_to_arrival_lead_days) else NA_real_,
    share_before = if (nrow(z)>0) mean(z$source_before_arrival) else NA_real_
  )
}

units <- unique(map[, c("species","target_cell","source_cell","pair_key")])
early <- t(mapply(
  window_summary,
  units$species,
  units$target_cell,
  MoreArgs = list(period_name="early")
))
late <- t(mapply(
  window_summary,
  units$species,
  units$target_cell,
  MoreArgs = list(period_name="late")
))

units$early_n <- as.integer(early[,"n"])
units$late_n <- as.integer(late[,"n"])
units$lead_early <- as.numeric(early[,"mean_lead"])
units$lead_late <- as.numeric(late[,"mean_lead"])
units$delta_lead <- units$lead_late - units$lead_early
units$share_before_early <- as.numeric(early[,"share_before"])
units$share_before_late <- as.numeric(late[,"share_before"])
units$delta_share_before <- units$share_before_late - units$share_before_early

analysis <- units[
  units$early_n >= MIN_YEARS &
    units$late_n >= MIN_YEARS &
    is.finite(units$lead_early) &
    is.finite(units$lead_late),
  ,
  drop = FALSE
]

if (nrow(analysis) < 20) stop("Too few eligible species-target rows")
if (length(unique(analysis$pair_key)) < 20) stop("Too few unique pairs")
if (length(unique(analysis$species)) < 5) stop("Too few species")

pair_boot_mean <- function(x, B, seed) {
  x <- x[is.finite(x)]
  set.seed(seed)
  out <- replicate(B, mean(sample(x, length(x), replace = TRUE)))
  as.numeric(quantile(out, c(0.025, 0.975), names = FALSE))
}

cluster_boot_mean <- function(df, value_col, cluster_col, B, seed) {
  keep <- is.finite(df[[value_col]]) & !is.na(df[[cluster_col]])
  dd <- df[keep, , drop = FALSE]
  cluster_id <- as.character(dd[[cluster_col]])
  clusters <- unique(cluster_id)
  if (length(clusters) < 2) return(c(NA_real_, NA_real_))
  by_cluster <- split(dd[[value_col]], cluster_id)
  set.seed(seed)
  out <- rep(NA_real_, B)
  for (b in seq_len(B)) {
    draw <- sample(clusters, length(clusters), replace = TRUE)
    vals <- unlist(by_cluster[draw], use.names = FALSE)
    out[b] <- mean(vals)
  }
  as.numeric(quantile(out, c(0.025, 0.975), na.rm = TRUE, names = FALSE))
}

# Pair-level collapse because multiple species may share environmental pairs.
pair_lead <- aggregate(
  cbind(
    lead_early,
    lead_late,
    delta_lead,
    share_before_early,
    share_before_late,
    delta_share_before
  ) ~ pair_key + source_cell,
  data=analysis,
  FUN=mean
)
# Add target cell representative only when unique within pair.
pair_target <- aggregate(
  target_cell ~ pair_key,
  data=analysis,
  FUN=function(x) x[1]
)
pair_lead <- merge(pair_lead,pair_target,by="pair_key",all.x=TRUE,sort=FALSE)

# Coordinates / blocks.
coord <- unique(cells[, c("cell","cell_lat2","cell_lng")])
coord <- coord[!duplicated(coord$cell),,drop=FALSE]
src <- coord; names(src) <- c("source_cell","source_lat","source_lng")
tgt <- coord; names(tgt) <- c("target_cell","target_lat","target_lng")
pair_lead <- merge(pair_lead,src,by="source_cell",all.x=TRUE)
pair_lead <- merge(pair_lead,tgt,by="target_cell",all.x=TRUE)
pair_lead$mid_lat <- (pair_lead$source_lat+pair_lead$target_lat)/2
pair_lead$mid_lng <- (pair_lead$source_lng+pair_lead$target_lng)/2
pair_lead$block5 <- paste(
  floor((pair_lead$mid_lat+90)/5),
  floor((pair_lead$mid_lng+180)/5),
  sep="_"
)
pair_lead$block10 <- paste(
  floor((pair_lead$mid_lat+90)/10),
  floor((pair_lead$mid_lng+180)/10),
  sep="_"
)

lead_pair_ci <- pair_boot_mean(pair_lead$delta_lead,B,SEED)
lead_source_ci <- cluster_boot_mean(pair_lead,"delta_lead","source_cell",B,SEED+1L)
lead_target_ci <- cluster_boot_mean(pair_lead,"delta_lead","target_cell",B,SEED+2L)
lead_b5_ci <- cluster_boot_mean(pair_lead,"delta_lead","block5",B,SEED+3L)
lead_b10_ci <- cluster_boot_mean(pair_lead,"delta_lead","block10",B,SEED+4L)

# Equal-species sensitivity.
sp <- aggregate(
  cbind(
    lead_early,
    lead_late,
    delta_lead,
    share_before_early,
    share_before_late,
    delta_share_before
  ) ~ species,
  data=analysis,
  FUN=mean
)

# Pair bootstrap carrying incidence for equal species mean.
pair_delta <- setNames(pair_lead$delta_lead,pair_lead$pair_key)
inc2 <- unique(analysis[,c("species","pair_key")])
inc_by_pair <- split(inc2$species,inc2$pair_key)
keys <- pair_lead$pair_key
set.seed(SEED+10L)
sp_boot <- rep(NA_real_,B)
for(b in seq_len(B)){
  draw <- sample(keys,length(keys),replace=TRUE)
  lists <- list()
  for(pk in draw){
    spp <- inc_by_pair[[pk]]
    val <- pair_delta[[pk]]
    for(ss in spp) lists[[ss]] <- c(lists[[ss]],val)
  }
  means <- vapply(lists,mean,numeric(1))
  sp_boot[b] <- mean(means)
}
sp_ci <- as.numeric(quantile(sp_boot,c(.025,.975),names=FALSE))

summary_row <- data.frame(
  eligible_species_target_rows=nrow(analysis),
  eligible_unique_pairs=nrow(pair_lead),
  eligible_species=length(unique(analysis$species)),
  pair_mean_lead_early=mean(pair_lead$lead_early),
  pair_mean_lead_late=mean(pair_lead$lead_late),
  pair_mean_delta_lead=mean(pair_lead$delta_lead),
  pair_median_delta_lead=median(pair_lead$delta_lead),
  pair_positive_delta=sum(pair_lead$delta_lead>0),
  pair_negative_delta=sum(pair_lead$delta_lead<0),
  pair_ci_low_95=lead_pair_ci[1],
  pair_ci_high_95=lead_pair_ci[2],
  source_cluster_ci_low_95=lead_source_ci[1],
  source_cluster_ci_high_95=lead_source_ci[2],
  target_cluster_ci_low_95=lead_target_ci[1],
  target_cluster_ci_high_95=lead_target_ci[2],
  block5_ci_low_95=lead_b5_ci[1],
  block5_ci_high_95=lead_b5_ci[2],
  block10_ci_low_95=lead_b10_ci[1],
  block10_ci_high_95=lead_b10_ci[2],
  pair_mean_share_source_before_arrival_early=mean(pair_lead$share_before_early),
  pair_mean_share_source_before_arrival_late=mean(pair_lead$share_before_late),
  pairs_majority_source_before_early=sum(pair_lead$share_before_early>0.5),
  pairs_majority_source_before_late=sum(pair_lead$share_before_late>0.5),
  equal_species_lead_early=mean(sp$lead_early),
  equal_species_lead_late=mean(sp$lead_late),
  equal_species_delta_lead=mean(sp$delta_lead),
  equal_species_ci_low_95=sp_ci[1],
  equal_species_ci_high_95=sp_ci[2]
)

# Also report row-year availability, which is directly interpretable as the
# fraction of observed bird-years for which source green-up occurred first.
year_summary <- aggregate(
  cbind(source_to_arrival_lead_days,source_before_arrival) ~ period,
  data=rows[
    paste(rows$species,rows$target_cell,sep="::") %in%
      paste(analysis$species,analysis$target_cell,sep="::"),
    ,
    drop=FALSE
  ],
  FUN=mean
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  rows,
  "outputs/payoff_b_v8_signal_arrival_window_year_rows.csv",
  row.names=FALSE
)
write.csv(
  analysis,
  "outputs/payoff_b_v8_signal_arrival_window_units.csv",
  row.names=FALSE
)
write.csv(
  pair_lead,
  "outputs/payoff_b_v8_signal_arrival_window_pairs.csv",
  row.names=FALSE
)
write.csv(
  sp,
  "outputs/payoff_b_v8_signal_arrival_window_species.csv",
  row.names=FALSE
)
write.csv(
  summary_row,
  "outputs/payoff_b_v8_signal_arrival_window_summary.csv",
  row.names=FALSE
)
write.csv(
  year_summary,
  "outputs/payoff_b_v8_signal_arrival_window_year_summary.csv",
  row.names=FALSE
)

cat("\nPOSTHOC SOURCE-SIGNAL TO ARRIVAL TEMPORAL WINDOW\n")
print(summary_row)
cat("\nYear-level availability:\n")
print(year_summary)
