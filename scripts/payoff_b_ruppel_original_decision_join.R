#!/usr/bin/env Rscript
# Native base-R original 2023 Rüppel source join audit, *no* new fitted effect.
# The original public ZIP is SHA256 checked before this script is invoked.
# Only metric names and aggregate counts are emitted, never original IDs,
# coordinates, individual times, weather values or response rows.
args <- commandArgs(trailingOnly = TRUE)
if (length(args)!=2L) stop("Usage Rscript original_verified.zip output_metrics.csv")
zipfile <- args[1]
outpath <- args[2]
need <- c("data.Event.RData","flights.RData")
got <- utils::unzip(zipfile,list=TRUE)$Name
if (!all(need %in% got)) stop("Original RData input members absent")
local <- tempfile("payoff_b_Ruppel_2023_")
dir.create(local)
utils::unzip(zipfile,files=need,exdir=local)
a <- new.env(parent=baseenv())
b <- new.env(parent=baseenv())
load(file.path(local,"data.Event.RData"),envir=a)
load(file.path(local,"flights.RData"),envir=b)
if (!exists("data.Event",envir=a,inherits=FALSE) ||
    !exists("flights",envir=b,inherits=FALSE)) {
  stop("Original R data-frame object names not source faithful")
}
ev <- get("data.Event",envir=a)
fl <- get("flights",envir=b)
if (!is.data.frame(ev) || !is.data.frame(fl))
  stop("Original data are not data frames")
if (!all(c("motusTagID","status","time_abs","flightStart") %in% names(ev)))
  stop("Original at-risk source schema changed")
if (!all(c("motusTagID","flightStart","flightEnd","flightCat","landing",
           "u_start","v_start","c_start","u_end","v_end","c_end") %in% names(fl)))
  stop("Original flight source schema changed")
if (nrow(ev)!=1783 || nrow(fl)!=178) stop("Original source row counts changed")
ids_ev <- unique(as.character(ev$motusTagID[!is.na(ev$motusTagID)]))
ids_fl <- unique(as.character(fl$motusTagID[!is.na(fl$motusTagID)]))
id_overlap <- intersect(ids_ev,ids_fl)
flight_duplicate <- sum(duplicated(as.character(fl$motusTagID)))
status <- suppressWarnings(as.numeric(ev$status))
landing <- suppressWarnings(as.numeric(fl$landing))
event_ok <- !is.na(status) & status %in% c(0,1)
landing_ok <- !is.na(landing) & landing %in% c(0,1)
status1 <- as.character(ev$motusTagID[!is.na(status) & status==1])
count_event_by_bird <- table(status1)
n_multi_event_ids <- sum(count_event_by_bird > 1)
n_unique_event_ids <- length(unique(status1))
flight_start_ok <- !is.na(fl$flightStart)
flight_end_ok <- !is.na(fl$flightEnd)
positive_duration <- flight_start_ok & flight_end_ok & fl$flightEnd>fl$flightStart
weather_start_complete <- complete.cases(
    fl[,c("u_start","v_start","c_start")])
weather_end_complete <- complete.cases(
    fl[,c("u_end","v_end","c_end")])
flight_class <- as.character(fl$flightCat)
n_onshore <- sum(grepl("onshore",flight_class,ignore.case=TRUE),na.rm=TRUE)
n_offshore <- sum(grepl("offshore",flight_class,ignore.case=TRUE),na.rm=TRUE)
# Compare event day to departure-start day without attempting to infer
# which local vs UTC clock is biologically correct.
individual_event_days <- split(ev$time_abs[
  !is.na(status) & status==1
],status1)
matched_exact_day <- 0L
matched_pm1_day <- 0L
has_terminal_event_day <- 0L
for (i in seq_len(nrow(fl))) {
  key <- as.character(fl$motusTagID[i])
  if (!(key %in% names(individual_event_days)) || is.na(fl$flightStart[i])) next
  days <- individual_event_days[[key]]
  dd <- suppressWarnings(as.numeric(as.Date(fl$flightStart[i],tz="UTC") - as.Date(days)))
  if (any(!is.na(dd))) {
    has_terminal_event_day <- has_terminal_event_day + 1L
    if (any(dd==0,na.rm=TRUE)) matched_exact_day <- matched_exact_day + 1L
    if (any(abs(dd)<=1,na.rm=TRUE)) matched_pm1_day <- matched_pm1_day + 1L
  }
}
candidates <- list(
  original_event_rows=nrow(ev),
  original_flight_rows=nrow(fl),
  original_event_ID_count=length(ids_ev),
  original_flight_ID_count=length(ids_fl),
  original_ID_intersection_count=length(id_overlap),
  original_event_only_ID_count=length(setdiff(ids_ev,ids_fl)),
  original_flight_only_ID_count=length(setdiff(ids_fl,ids_ev)),
  original_duplicate_flight_ID_count=flight_duplicate,
  original_status_valid_0_or_1_count=sum(event_ok),
  original_status_missing_or_invalid_count=sum(!event_ok),
  original_at_risk_non_departure_days=sum(status==0,na.rm=TRUE),
  original_departure_event_rows=sum(status==1,na.rm=TRUE),
  original_IDs_with_at_least_one_departure_event=n_unique_event_ids,
  original_IDs_with_more_than_one_terminal_event=n_multi_event_ids,
  original_flight_landing_valid_0_or_1_count=sum(landing_ok),
  original_flight_landing_missing_or_invalid_count=sum(!landing_ok),
  original_observed_landing_events=sum(landing==1,na.rm=TRUE),
  original_observed_nonlanding_flights=sum(landing==0,na.rm=TRUE),
  original_route_onshore_label_count=n_onshore,
  original_route_offshore_label_count=n_offshore,
  original_route_label_missing_count=sum(is.na(flight_class)),
  original_flightStart_available=sum(flight_start_ok),
  original_flightEnd_available=sum(flight_end_ok),
  original_flightStart_before_end_count=sum(positive_duration),
  original_start_wind_cloud_all_present=sum(weather_start_complete),
  original_end_wind_cloud_all_present=sum(weather_end_complete),
  original_start_and_end_weather_all_present=sum(weather_start_complete&weather_end_complete),
  original_departure_event_UTCday_comparable=nrow(fl)-nrow(fl)+has_terminal_event_day,
  original_departure_event_same_UTCday=matched_exact_day,
  original_departure_event_within_UTC_plusminus1day=matched_pm1_day,
  original_key_merging_uses_coordinateless_motusTagID=TRUE,
  direct_q_wait_D_eff_r_t_and_fitness_estimable=FALSE,
  original_weather_three_decision_effects_novel_to_PAYOFF=FALSE
)
dir.create(dirname(outpath),recursive=TRUE,showWarnings=FALSE)
metrics <- names(candidates)
values <- vapply(candidates,as.character,"")
utils::write.csv(data.frame(metric=metrics,value=values,stringsAsFactors=FALSE),
                 outpath,row.names=FALSE)
cat(sprintf("ORIGINAL_RUPPEL_SOURCE_JOIN_AUDIT n_event=%d n_flights=%d n_sharedID=%d landings=%d\n",
            nrow(ev),nrow(fl),length(id_overlap),sum(landing==1,na.rm=TRUE)))
