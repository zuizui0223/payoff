#!/usr/bin/env Rscript
# PAYOFF-B observational opportunity vs actual available information
# Hypothetical event-available decision gate, NOT animal migratory behavior.
# Post-open exploratory contract committed before new result:
# docs/PAYOFF_B_MODIS_DECISION_TIME_OBSERVABILITY_FREEZE_20261117.md
options(stringsAsFactors=FALSE)

SCRIPT_ORACLE <- "analysis/movement_phenology/payoff_b_modis_oos_forecast_skill_20261117.R"
EXPECTED_ORACLE_EARLY <- 0.7454488
EXPECTED_ORACLE_LATE <- 0.5993736
LEAD_DAYS <- 7
PRIMARY_REPORT_DELAY_DAYS <- 7
SENSITIVITY_DELAY_DAYS <- 0
BOOT_N <- 10000L
BOOT_SEED <- 20261117L

predict_one <- function(dat,i,lead=LEAD_DAYS,
                        delay=PRIMARY_REPORT_DELAY_DAYS) {
  dat <- dat[order(dat$year),c("year","source","target")]
  if(nrow(dat)!=8L || i<6L || i>8L ||
     any(!is.finite(as.matrix(dat))) ||
     length(unique(dat$year))!=8L)
    stop("FROZEN_SOURCE_CHRONOLOGICAL_SUPPORT_FAILED")
  train <- dat[seq_len(i-1L),,drop=FALSE]
  test <- dat[i,,drop=FALSE]
  if(any(train$year>=test$year))stop("FUTURE_YEAR_IN_TRAINING")
  base <- lm(target~year,data=train)
  cue <- lm(target~year+source,data=train)
  if(base$rank!=2L || cue$rank!=3L)
    stop("TRAINING_SOURCE_PREDICTOR_RANK_DEFICIENT")
  p0 <- as.numeric(predict(base,newdata=test))
  p1 <- as.numeric(predict(cue,newdata=test))
  if(length(p0)!=1 || length(p1)!=1 || !all(is.finite(c(p0,p1))))
    stop("NONFINITE_SOURCE_FORECAST")
  query_day <- p0-lead
  observed <- as.numeric(test$source[1])
  target <- as.numeric(test$target[1])
  delayed <- observed+delay<=query_day
  instant <- observed<=query_day
  # The target must ONLY be used below to evaluate errors and retrospectively
  # flag hypothetical decisions that were later than true target green-up.
  result <- c(
    year=as.integer(test$year[1]),
    train_years=i-1L,
    source_greenup_day=observed,
    true_target_greenup_day=target,
    baseline_pred_target_day=p0,
    oracle_pred_target_day=p1,
    hypothetical_decision_day=query_day,
    delay_days=delay,
    event_available=as.numeric(delayed),
    event_available_instant=as.numeric(instant),
    decision_truly_precedes_target=as.numeric(query_day<target),
    source_truly_precedes_target=as.numeric(observed<target),
    base_sq=(target-p0)^2,
    oracle_sq=(target-p1)^2,
    gated_sq=(target-if(delayed)p1 else p0)^2,
    instant_sq=(target-if(instant)p1 else p0)^2
  )
  if(any(!is.finite(result)))stop("NONFINITE_SOURCE_EVENT_RESULT")
  result
}

if("--synthetic-only" %in% commandArgs(trailingOnly=TRUE)) {
  x <- data.frame(
    year=2002:2009,
    source=c(75,80,82,76,83,79,88,90),
    target=c(116,119,120,118,126,124,130,129)
  )
  a <- predict_one(x,6L,lead=7,delay=7)
  stopifnot(a[["train_years"]]==5,
            a[["event_available"]]<=a[["event_available_instant"]],
            a[["gated_sq"]]>=0)
  altered <- x
  altered$target[6] <- altered$target[6]+150
  b <- predict_one(altered,6L,lead=7,delay=7)
  stopifnot(identical(a[["event_available"]],b[["event_available"]]),
            identical(a[["hypothetical_decision_day"]],
                      b[["hypothetical_decision_day"]]),
            identical(a[["baseline_pred_target_day"]],
                      b[["baseline_pred_target_day"]]),
            a[["base_sq"]]!=b[["base_sq"]])
  cat("PAYOFF-B decision-time event gate synthetic chronology: PASS\n")
  quit(status=0)
}

# Re-run original full source/archive/geometry and frozen out-of-year oracle.
ctx <- new.env(parent=globalenv())
sys.source(SCRIPT_ORACLE,envir=ctx)
pairs <- ctx$pairs
green <- ctx$green
pair_period <- ctx$pair_period
sc <- ctx$sc
if(nrow(pairs)!=104L ||
   length(unique(pairs$source_cell))!=88L ||
   abs(mean(pairs$delta_rho)-0.08057016)>1e-7)
  stop("ORIGINAL_EBIRD_FREE_SATELLITE_GEOMETRY_DRIFT")
early_old <- sc$skill[sc$window=="early"&sc$protocol=="forward"]
late_old <- sc$skill[sc$window=="late"&sc$protocol=="forward"]
if(length(early_old)!=1L||length(late_old)!=1L||
   abs(early_old-EXPECTED_ORACLE_EARLY)>1e-6||
   abs(late_old-EXPECTED_ORACLE_LATE)>1e-6)
  stop("FROZEN_ORACLE_OOS_SKILL_MISMATCH")

records <- vector("list",nrow(pairs)*2L*3L)
counter <- 0L
for(j in seq_len(nrow(pairs))) {
  for(period in c("early","late")) {
    years <- if(period=="early")2002:2009 else 2010:2017
    dat <- pair_period(green,pairs$source_cell[j],pairs$target_cell[j],years)
    if(nrow(dat)!=8L)stop("SATELLITE_SOURCE_PAIR_NOT_8_YEARS")
    for(i in 6:8) {
      pred <- predict_one(dat,i,lead=LEAD_DAYS,delay=PRIMARY_REPORT_DELAY_DAYS)
      counter <- counter+1L
      records[[counter]] <- data.frame(
        pair_idx=j,source_cell=pairs$source_cell[j],
        target_cell=pairs$target_cell[j],period=period,
        year=as.integer(pred[["year"]]),
        train_years=as.integer(pred[["train_years"]]),
        source_day=pred[["source_greenup_day"]],
        target_day=pred[["true_target_greenup_day"]],
        model0_pred_day=pred[["baseline_pred_target_day"]],
        oracle_pred_day=pred[["oracle_pred_target_day"]],
        decision_day=pred[["hypothetical_decision_day"]],
        available_lag7=as.logical(pred[["event_available"]]),
        available_lag0=as.logical(pred[["event_available_instant"]]),
        decision_actual_pre_target=as.logical(
          pred[["decision_truly_precedes_target"]]),
        source_actual_pre_target=as.logical(
          pred[["source_truly_precedes_target"]]),
        sse_baseline=pred[["base_sq"]],
        sse_oracle=pred[["oracle_sq"]],
        sse_available_lag7=pred[["gated_sq"]],
        sse_available_lag0=pred[["instant_sq"]]
      )
    }
  }
}
d <- do.call(rbind,records)
if(nrow(d)!=624L ||
   nrow(unique(d[,c("pair_idx","period","year")]))!=624L)
  stop("SOURCE_FOLD_LEAKAGE_OR_ROW_COUNT_DRIFT")

skill <- function(num,den) {
  if(any(!is.finite(c(num,den)))||den<=0)
    stop("UNDEFINED_PREDICTIVE_SKILL")
  1-num/den
}
period_summary <- do.call(rbind,lapply(c("early","late"),function(per) {
  x <- d[d$period==per,]
  baseline <- sum(x$sse_baseline)
  result <- data.frame(
    period=per,n_source_year_predictions=nrow(x),
    original_baseline_rmse_days=sqrt(mean(x$sse_baseline)),
    oracle_rmse_days=sqrt(mean(x$sse_oracle)),
    observed_event_lag7_rmse_days=sqrt(mean(x$sse_available_lag7)),
    observed_event_instant_rmse_days=sqrt(mean(x$sse_available_lag0)),
    oracle_skill=skill(sum(x$sse_oracle),baseline),
    available_lag7_skill=skill(sum(x$sse_available_lag7),baseline),
    available_instant_skill=skill(sum(x$sse_available_lag0),baseline),
    fraction_available_before_decision_lag7=mean(x$available_lag7),
    fraction_available_before_decision_lag0=mean(x$available_lag0),
    fraction_decisions_before_real_target=mean(x$decision_actual_pre_target),
    fraction_source_earlier_than_real_target=mean(x$source_actual_pre_target),
    hypothetical_lead_days=LEAD_DAYS,
    hypothetical_observation_latency_primary_days=PRIMARY_REPORT_DELAY_DAYS
  )
  result
}))
if(abs(period_summary$oracle_skill[1]-EXPECTED_ORACLE_EARLY)>1e-6||
   abs(period_summary$oracle_skill[2]-EXPECTED_ORACLE_LATE)>1e-6)
  stop("SOURCE_OOS_ORACLE_RECALCULATION_DRIFT")

pair_sse <- aggregate(
  cbind(sse_baseline,sse_oracle,sse_available_lag7,sse_available_lag0)~
    pair_idx+period,data=d,FUN=sum)
pair_early <- pair_sse[pair_sse$period=="early",]
pair_late <- pair_sse[pair_sse$period=="late",]
pair_early <- pair_early[order(pair_early$pair_idx),]
pair_late <- pair_late[order(pair_late$pair_idx),]
if(!identical(pair_early$pair_idx,pair_late$pair_idx)||
   !identical(pair_early$pair_idx,seq_len(nrow(pairs))))
  stop("SOURCE_SOURCECELL_BOOTSTRAP_PAIR_MISALIGNMENT")
groups <- split(seq_len(nrow(pairs)),as.character(pairs$source_cell))
if(length(groups)!=88L)stop("FROZEN_GROUPING_SUPPORT_MISMATCH")
set.seed(BOOT_SEED)
boot_early <- numeric(BOOT_N)
boot_late <- numeric(BOOT_N)
boot_change <- numeric(BOOT_N)
boot_lag0_change <- numeric(BOOT_N)
for(b in seq_len(BOOT_N)) {
  selected <- sample(names(groups),length(groups),replace=TRUE)
  ix <- unlist(groups[selected],use.names=FALSE)
  s0 <- skill(sum(pair_early$sse_available_lag7[ix]),
              sum(pair_early$sse_baseline[ix]))
  s1 <- skill(sum(pair_late$sse_available_lag7[ix]),
              sum(pair_late$sse_baseline[ix]))
  boot_early[b] <- s0
  boot_late[b] <- s1
  boot_change[b] <- s1-s0
  i0 <- skill(sum(pair_early$sse_available_lag0[ix]),
              sum(pair_early$sse_baseline[ix]))
  i1 <- skill(sum(pair_late$sse_available_lag0[ix]),
              sum(pair_late$sse_baseline[ix]))
  boot_lag0_change[b] <- i1-i0
}
ci <- function(x) unname(quantile(x,c(.025,.975)))
int_early <- ci(boot_early)
int_late <- ci(boot_late)
int_delta <- ci(boot_change)
int_lag0 <- ci(boot_lag0_change)
result <- data.frame(
  source_kind="MODIS_ONLY_POSTOPEN_HYPOTHETICAL_OBSERVATION",
  prior_satellite_source_sha256="8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199",
  n_physical_pairs=nrow(pairs),
  n_source_cell_blocks=length(groups),
  n_test_predictions=nrow(d),
  primary_lead_days=LEAD_DAYS,
  primary_assumed_reporting_lag_days=PRIMARY_REPORT_DELAY_DAYS,
  early_oracle_skill=period_summary$oracle_skill[1],
  late_oracle_skill=period_summary$oracle_skill[2],
  early_gated_skill=period_summary$available_lag7_skill[1],
  late_gated_skill=period_summary$available_lag7_skill[2],
  gated_skill_change=diff(period_summary$available_lag7_skill),
  gated_skill_early_ci_low=int_early[1],
  gated_skill_early_ci_high=int_early[2],
  gated_skill_late_ci_low=int_late[1],
  gated_skill_late_ci_high=int_late[2],
  gated_skill_change_ci_low=int_delta[1],
  gated_skill_change_ci_high=int_delta[2],
  early_event_available_fraction=period_summary$fraction_available_before_decision_lag7[1],
  late_event_available_fraction=period_summary$fraction_available_before_decision_lag7[2],
  early_actual_decision_before_target_fraction=period_summary$fraction_decisions_before_real_target[1],
  late_actual_decision_before_target_fraction=period_summary$fraction_decisions_before_real_target[2],
  early_instant_notice_skill=period_summary$available_instant_skill[1],
  late_instant_notice_skill=period_summary$available_instant_skill[2],
  instant_notice_change=diff(period_summary$available_instant_skill),
  instant_notice_change_ci_low=int_lag0[1],
  instant_notice_change_ci_high=int_lag0[2],
  bootstrap_source_cell_repeats=BOOT_N,bootstrap_seed=BOOT_SEED,
  source_event_completion_is_NOT_measured_real_time_observability=TRUE,
  bird_information_access_tested=FALSE,
  biological_fitness_tested=FALSE,
  result_status="HYPOTHETICAL_AVAILABILITY_GATE_EXPLORATORY"
)
dir.create("outputs",recursive=TRUE,showWarnings=FALSE)
write.csv(result,"outputs/payoff_b_modis_decision_time_gate_result.csv",row.names=FALSE)
write.csv(period_summary,"outputs/payoff_b_modis_decision_time_period_scores.csv",
          row.names=FALSE)
write.csv(d,"outputs/payoff_b_modis_decision_time_year_scores.csv",
          row.names=FALSE)
cat("\nPAYOFF-B MODIS HYPOTHETICAL PRE-DECISION AVAILABLE CUE RESULT\n")
print(result,row.names=FALSE,digits=7)
cat("\nPERIOD SCORES\n")
print(period_summary,row.names=FALSE,digits=7)
cat("\nNo bird state, eBird, GPS, fitness, real-time MODIS signal or migration-route actionability was measured.\n")
