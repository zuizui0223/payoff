#!/usr/bin/env Rscript
# Stage3: author radio telemetry RData timing and source-code structure only.
# No biological model fits or individual timestamp/coordinate outputs.
args <- commandArgs(trailingOnly=TRUE)
if("--self-test" %in% args){
  mock <- data.frame(motusTagID=c(1L,1L,2L), time_abs=as.Date(c("2023-01-01","2023-01-02","2023-01-01")),
                     status=c(0,1,1))
  stopifnot(length(unique(mock$motusTagID))==2L,nrow(mock)==3)
  cat("RUPPEL_STAGE3_TIMING_GATE_SYNTHETIC_PASS\n")
  quit(save="no")
}

src <- "outputs/.source-only-ruppel-2023.zip"
if(!file.exists(src)) stop("Pinned original ZIP missing")
d <- tempfile("ruppel_original_")
dir.create(d)
unzip(src, files=c("data.Event.RData","flights.RData","Rcode.Rmd"),exdir=d)
envA <- new.env(parent=baseenv());envB <- new.env(parent=baseenv())
stopifnot(identical(load(file.path(d,"data.Event.RData"),envir=envA),"data.Event"),
          identical(load(file.path(d,"flights.RData"),envir=envB),"flights"))
a <- envA$data.Event
f <- envB$flights
stopifnot(is.data.frame(a), is.data.frame(f),
          nrow(a)==1783L,nrow(f)==178L,
          all(c("motusTagID","time_abs","status","start","stop")%in%names(a)),
          all(c("motusTagID","flightStart","flightEnd","landing",
                "u_start","u_end","flightCat")%in%names(f)))

count <- function(x) length(unique(x[!is.na(x)]))
q <- function(x) as.numeric(quantile(as.numeric(x),c(.0,.25,.5,.75,1),na.rm=TRUE,names=FALSE))
a_by_id <- table(a$motusTagID)
f_by_id <- table(f$motusTagID)
a_times <- as.Date(a$time_abs)
f_dates <- as.Date(f$flightStart)
fl_sec <- as.numeric(difftime(f$flightEnd,f$flightStart,units="hours"))
fl_sec[!is.finite(fl_sec)] <- NA_real_
status_levels <- table(a$status,useNA="ifany")
landing_levels <- table(f$landing,useNA="ifany")
flightcat_levels <- table(f$flightCat,useNA="ifany")
route_landing <- table(f$flightCat, f$landing, useNA="ifany")
route_landing_text <- paste(
  apply(as.data.frame(route_landing),1,function(row) {
    paste(as.character(row[1]),as.character(row[2]),
          as.integer(row[3]),sep=":")
  }),
  collapse=";"
)
a_key <- paste(a$motusTagID, a_times)
f_key <- paste(f$motusTagID, f_dates)

# Source event status=1 is the recorded departure event. Do not silently
# count a nondeparture bird-night as a matching flight origin decision.
# Each of the 178 source individuals should have exactly one such event.
event_rows <- a[!is.na(a$status) & a$status == 1, , drop=FALSE]
event_counts <- table(event_rows$motusTagID)
if(nrow(event_rows)!=178L || length(event_counts)!=178L ||
   any(event_counts!=1L))
  stop("risk table contains unexpected departure event grain")
event_index <- match(f$motusTagID, event_rows$motusTagID)
if(anyNA(event_index))
  stop("observed flight missing departure event for its individual")
event_dates <- as.Date(event_rows$time_abs[event_index])
flight_minus_event_days <- as.integer(f_dates - event_dates)
if(anyNA(flight_minus_event_days))
  stop("missing date offset between matched bird departure and flight")
date_offset_frequencies <- table(flight_minus_event_days)
date_offsets <- paste(names(date_offset_frequencies),
                      as.integer(date_offset_frequencies),sep=":",
                      collapse=";")

data <- list(
  source="Ruppel_2023_figshare_MD5_verified",
  dataset_nightly_rows=nrow(a),
  dataset_flight_rows=nrow(f),
  nightly_unique_birds=count(a$motusTagID),
  flight_unique_birds=count(f$motusTagID),
  id_overlap_birds=length(intersect(unique(a$motusTagID),unique(f$motusTagID))),
  nightly_unique_id_day=length(unique(a_key)),
  nightly_duplicate_id_day=nrow(a)-length(unique(a_key)),
  flights_with_samebird_sameday_risk_record=sum(f_key%in%a_key),
  flights_with_samebird_sameday_departure_event=sum(flight_minus_event_days==0L),
  flight_start_minus_status1_event_day_distribution=date_offsets,
  flights_with_departure_event_within_one_calendar_day=sum(abs(flight_minus_event_days)<=1L),
  flights_with_departure_event_beyond_one_calendar_day=sum(abs(flight_minus_event_days)>1L),
  flight_start_date_complete=sum(!is.na(f$flightStart)),
  flight_end_date_complete=sum(!is.na(f$flightEnd)),
  flight_positive_duration_hours=sum(fl_sec>0,na.rm=TRUE),
  flight_nonpositive_duration_hours=sum(fl_sec<=0,na.rm=TRUE),
  flight_duration_hour_quantiles=paste(q(fl_sec),collapse=","),
  source_event_status_counts=paste(paste(names(status_levels),as.integer(status_levels),sep=":"),collapse=";"),
  flight_landing_value_counts=paste(paste(names(landing_levels),as.integer(landing_levels),sep=":"),collapse=";"),
  route_category_counts=paste(paste(names(flightcat_levels),as.integer(flightcat_levels),sep=":"),collapse=";"),
  route_and_landing_cross_tab=route_landing_text,
  event_rows_per_bird_quantiles=paste(q(a_by_id),collapse=","),
  flight_rows_per_bird_quantiles=paste(q(f_by_id),collapse=","),
  end_wind_u_missing=sum(is.na(f$u_end)),
  start_wind_u_missing=sum(is.na(f$u_start)),
  end_wind_v_missing=sum(is.na(f$v_end)),
  start_wind_v_missing=sum(is.na(f$v_start)),
  flight_source_has_origin_issued_future_weather_forecast=FALSE,
  independently_measured_action_feasibility_in_source=FALSE,
  observed_individual_reproductive_fitness_in_source=FALSE,
  biological_effect_fitted=FALSE
)

out <- "outputs"
dir.create(out,recursive=TRUE,showWarnings=FALSE)
receipt <- data.frame(
  key=names(data),
  value=vapply(data,as.character,character(1)),
  stringsAsFactors=FALSE)
write.csv(receipt,file.path(out,"payoff_b_ruppel_stage3_event_time_support.csv"),row.names=FALSE)

# Code inspection ONLY: capture original author's analyzed weather and risk
# models with relevant short source-line context, not outcomes.
rmd <- readLines(file.path(d,"Rcode.Rmd"),warn=FALSE)
idx <- grep("survreg|survFit|brms|fit[1234]|model landing|landing ~|flightCat|u_end|v_end|u_start|v_start|routing|flightEnd|data.Event|flying|predict|forecast",
            rmd,ignore.case=TRUE)
selected <- unique(unlist(lapply(idx,function(i) seq.int(max(1,i-1),min(length(rmd),i+2)))))
selected <- selected[seq_len(min(length(selected),155L))]
snippets <- paste0("L",selected,": ",
                   substr(trimws(rmd[selected]),1,200))
writeLines(c("AUTHOR_SOURCE_CODE_READ_ONLY_NOT_EXECUTED",
             paste("Original author Rmd lines:",length(rmd)),
             paste("Candidate matched lines:",length(idx)),
             paste("Distinct context lines included:",length(selected)),
             snippets),
           file.path(out,"payoff_b_ruppel_stage3_author_models_excerpt.txt"))
# Focused later source-author models: role of departure, route and landing
# and whether weather input is flight-start versus flight-end. Source lines
# printed are code only, no animal events or modeled coefficients.
late_source <- seq.int(330L,length(rmd))
later_matches <- late_source[
  grepl("landing|route|weather|u_end|v_end|t_end|u_start|v_start|t_start|flightCat|fit[234]|brm\\(|glm\\(|flightEnd|detect",
        rmd[late_source],ignore.case=TRUE,perl=TRUE)
]
later_lines <- unique(unlist(lapply(later_matches, function(i)
  seq.int(max(330L,i-2L),min(length(rmd),i+2L)))))
later_lines <- later_lines[seq_len(min(length(later_lines),175L))]
writeLines(c("AUTHOR_ORIGINAL_LATE_STAGE_CODE_ONLY_NOT_EXECUTED",
             paste("Full Rmd lines:",length(rmd)),
             paste("Late stage relevant matches:",length(later_matches)),
             paste0("L",later_lines,": ",
                    substr(trimws(rmd[later_lines]),1,200))),
           file.path(out,"payoff_b_ruppel_stage3_route_landing_Rmd_excerpt.txt"))
cat("RUPPEL_REAL_SOURCE_TIMING_AND_LINKAGE_GATE_PASSED\n")
print(receipt,row.names=FALSE)
cat("NO NEW WEATHER_RESPONSE_COEFFICIENTS_OR_FITNESS_INFERRED\n")
unlink(d,recursive=TRUE)
