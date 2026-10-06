#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC OBSERVABILITY-BOUNDARY AUDIT.
#
# The reconstructed environmental predictor is annual source-cell mid-green-up.
# This script asks where that realized event falls relative to the same species'
# estimated population-front arrival at source and target cells.
#
# It uses the same restricted source-stage eligibility as the population-front
# stage audit (>=6 paired annual arrival estimates at both cells in both periods).
#
# This does NOT establish individual exposure or cue perception.

GATE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_admission_gate.R"
if (!file.exists(GATE_SCRIPT)) stop("Missing V8 admission-gate script")
source(GATE_SCRIPT, local = FALSE)

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

# Freeze the same stagewise eligibility.
counts <- aggregate(
  year ~ species + source_cell + target_cell + pair_key + period,
  data=rows,
  FUN=function(x) length(unique(x))
)
e <- counts[counts$period=="early",]
l <- counts[counts$period=="late",]
names(e)[names(e)=="year"] <- "early_n"
names(l)[names(l)=="year"] <- "late_n"
e$period <- NULL
l$period <- NULL
units <- merge(
  e,l,
  by=c("species","source_cell","target_cell","pair_key"),
  all=FALSE
)
units <- units[
  units$early_n>=MIN_YEARS &
    units$late_n>=MIN_YEARS,
  ,
  drop=FALSE
]

key <- function(sp,s,t) paste(sp,s,t,sep="::")
rows$key <- key(rows$species,rows$source_cell,rows$target_cell)
units$key <- key(units$species,units$source_cell,units$target_cell)
rows <- rows[rows$key %in% units$key,,drop=FALSE]

# Event-order coordinates.
rows$source_greenup_minus_source_arrival <-
  rows$source_greenup - rows$source_arrival
rows$target_arrival_minus_source_greenup <-
  rows$target_arrival - rows$source_greenup

rows$source_event_before_source_arrival <-
  rows$source_greenup < rows$source_arrival
rows$source_event_between_front_stages <-
  rows$source_greenup >= rows$source_arrival &
  rows$source_greenup <= rows$target_arrival
rows$source_event_after_target_arrival <-
  rows$source_greenup > rows$target_arrival

period_summary <- lapply(c("early","late"),function(pp){
  z <- rows[rows$period==pp,,drop=FALSE]
  data.frame(
    period=pp,
    year_rows=nrow(z),
    mean_source_greenup_minus_source_arrival=
      mean(z$source_greenup_minus_source_arrival),
    mean_target_arrival_minus_source_greenup=
      mean(z$target_arrival_minus_source_greenup),
    fraction_source_event_before_source_arrival=
      mean(z$source_event_before_source_arrival),
    fraction_source_event_between_front_stages=
      mean(z$source_event_between_front_stages),
    fraction_source_event_after_target_arrival=
      mean(z$source_event_after_target_arrival)
  )
})
period_summary <- do.call(rbind,period_summary)

# Unit-level proportions, then pair/species summaries.
unit_summary <- lapply(unique(rows$key),function(k){
  z <- rows[rows$key==k,,drop=FALSE]
  u <- units[units$key==k,,drop=FALSE]
  out <- data.frame(
    species=u$species[1],
    source_cell=u$source_cell[1],
    target_cell=u$target_cell[1],
    pair_key=u$pair_key[1]
  )
  for(pp in c("early","late")){
    q <- z[z$period==pp,,drop=FALSE]
    out[[paste0("source_before_source_arrival_",pp)]] <-
      mean(q$source_event_before_source_arrival)
    out[[paste0("source_between_stages_",pp)]] <-
      mean(q$source_event_between_front_stages)
    out[[paste0("source_after_target_",pp)]] <-
      mean(q$source_event_after_target_arrival)
    out[[paste0("source_after_source_by_days_",pp)]] <-
      mean(q$source_greenup_minus_source_arrival)
    out[[paste0("source_before_target_by_days_",pp)]] <-
      mean(q$target_arrival_minus_source_greenup)
  }
  out
})
unit_summary <- do.call(rbind,unit_summary)

pair_summary <- aggregate(
  cbind(
    source_before_source_arrival_early,
    source_before_source_arrival_late,
    source_between_stages_early,
    source_between_stages_late,
    source_after_target_early,
    source_after_target_late,
    source_after_source_by_days_early,
    source_after_source_by_days_late,
    source_before_target_by_days_early,
    source_before_target_by_days_late
  ) ~ pair_key,
  data=unit_summary,
  FUN=mean
)

species_summary <- aggregate(
  cbind(
    source_before_source_arrival_early,
    source_before_source_arrival_late,
    source_between_stages_early,
    source_between_stages_late,
    source_after_target_early,
    source_after_target_late,
    source_after_source_by_days_early,
    source_after_source_by_days_late,
    source_before_target_by_days_early,
    source_before_target_by_days_late
  ) ~ species,
  data=unit_summary,
  FUN=mean
)

overall <- data.frame(
  eligible_units=nrow(unit_summary),
  unique_pairs=nrow(pair_summary),
  species=nrow(species_summary),

  pair_mean_fraction_source_before_source_arrival_early=
    mean(pair_summary$source_before_source_arrival_early),
  pair_mean_fraction_source_before_source_arrival_late=
    mean(pair_summary$source_before_source_arrival_late),

  pair_mean_fraction_source_between_stages_early=
    mean(pair_summary$source_between_stages_early),
  pair_mean_fraction_source_between_stages_late=
    mean(pair_summary$source_between_stages_late),

  pair_mean_source_after_source_by_days_early=
    mean(pair_summary$source_after_source_by_days_early),
  pair_mean_source_after_source_by_days_late=
    mean(pair_summary$source_after_source_by_days_late),

  pair_mean_source_before_target_by_days_early=
    mean(pair_summary$source_before_target_by_days_early),
  pair_mean_source_before_target_by_days_late=
    mean(pair_summary$source_before_target_by_days_late),

  species_mean_fraction_source_before_source_arrival_early=
    mean(species_summary$source_before_source_arrival_early),
  species_mean_fraction_source_before_source_arrival_late=
    mean(species_summary$source_before_source_arrival_late),

  species_mean_fraction_source_between_stages_early=
    mean(species_summary$source_between_stages_early),
  species_mean_fraction_source_between_stages_late=
    mean(species_summary$source_between_stages_late)
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  rows,
  "outputs/payoff_b_v8_source_event_observability_year_rows.csv",
  row.names=FALSE
)
write.csv(
  period_summary,
  "outputs/payoff_b_v8_source_event_observability_period.csv",
  row.names=FALSE
)
write.csv(
  unit_summary,
  "outputs/payoff_b_v8_source_event_observability_units.csv",
  row.names=FALSE
)
write.csv(
  pair_summary,
  "outputs/payoff_b_v8_source_event_observability_pairs.csv",
  row.names=FALSE
)
write.csv(
  species_summary,
  "outputs/payoff_b_v8_source_event_observability_species.csv",
  row.names=FALSE
)
write.csv(
  overall,
  "outputs/payoff_b_v8_source_event_observability_summary.csv",
  row.names=FALSE
)

cat("\nPOSTHOC SOURCE-EVENT OBSERVABILITY BOUNDARY\n")
print(period_summary)
print(overall)
