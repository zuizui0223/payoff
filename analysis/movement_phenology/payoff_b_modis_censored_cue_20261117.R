#!/usr/bin/env Rscript
# PAYOFF-B negative phenological event information from censored observation.
# Post-open exploratory, not bird behavior. Frozen method:
# docs/PAYOFF_B_MODIS_CENSORED_CUE_FREEZE_20261117.md
options(stringsAsFactors=FALSE)
UPSTREAM <- "analysis/movement_phenology/payoff_b_modis_observable_cue_gate_20261117.R"
EXPECTED_BASE_EARLY <- 0.001605643
EXPECTED_BASE_LATE <- 0.220805535
EXPECTED_ORACLE_EARLY <- 0.7454488
EXPECTED_ORACLE_LATE <- 0.5993736
LEAD_DAYS <- 7L
REPORT_LAGS <- c(7L,0L)
B <- 10000L
SEED <- 20261117L

binary_fold <- function(dat,i,latency) {
  dat <- dat[order(dat$year),c("year","source","target")]
  if(nrow(dat)!=8L || i<6L || i>8L ||
     length(unique(dat$year))!=8L || any(!is.finite(as.matrix(dat))))
    stop("CENSORED_SOURCE_SUPPORT_NOT_ORIGINAL_EIGHT_YEARS")
  train <- dat[seq_len(i-1L),,drop=FALSE]
  test <- dat[i,,drop=FALSE]
  if(any(train$year>=test$year))stop("HELDOUT_YEAR_IN_TRAINING")
  base <- lm(target~year,data=train)
  if(base$rank!=2L)stop("SOURCE_BASELINE_TREND_NOT_IDENTIFIED")
  target_pred_train <- as.numeric(predict(base,newdata=train))
  target_pred_test <- as.numeric(predict(base,newdata=test))
  decision_train <- target_pred_train-LEAD_DAYS
  decision_test <- target_pred_test-LEAD_DAYS
  # Every source onset + reporting delay is objectively known in the
  # historical training data, but assumed observable in real time.
  # No held-out target onset in the event-status predictor.
  status_train <- as.integer(train$source+latency<=decision_train)
  status_test <- as.integer(test$source+latency<=decision_test)
  varying <- length(unique(status_train))>1L
  model_used <- FALSE
  q <- target_pred_test
  if(varying) {
    fitted <- data.frame(year=train$year,target=train$target,
                         event_seen=status_train)
    fit <- lm(target~year+event_seen,data=fitted)
    if(fit$rank==3L) {
      predicted <- predict(fit,newdata=data.frame(
             year=test$year,event_seen=status_test))
      if(length(predicted)!=1 || !is.finite(predicted))
         stop("CENSORED_CUE_PREDICTION_INVALID")
      q <- as.numeric(predicted)
      model_used <- TRUE
    }
  }
  # Held-out target appears ONLY in error/scoring and post-scoring timeline.
  realized_target <- as.numeric(test$target)
  out <- c(
    year=as.numeric(test$year),
    event_observed=status_test,
    train_event_status_varied=as.integer(varying),
    binary_model_used=as.integer(model_used),
    train_n_ever_observed=sum(status_train),
    hypothetical_decision_day=decision_test,
    source_event_day=as.numeric(test$source),
    target_true_day=realized_target,
    decision_before_true_target=as.integer(decision_test<realized_target),
    baseline_sq=(realized_target-target_pred_test)^2,
    binary_sq=(realized_target-q)^2,
    predicted_target_without_cue=target_pred_test,
    predicted_target_with_censored_cue=q
  )
  if(any(!is.finite(out)))stop("NONFINITE_OUT_OF_YEAR_SOURCE_CUE")
  out
}

if("--synthetic-only" %in% commandArgs(trailingOnly=TRUE)) {
  ex <- data.frame(year=2002:2009,
       source=c(70,120,75,130,72,88,90,84),
       target=c(116,119,120,118,126,124,130,129))
  p <- binary_fold(ex,6,7)
  changed <- ex
  changed$target[6] <- changed$target[6]+200
  p2 <- binary_fold(changed,6,7)
  for(k in c("event_observed","hypothetical_decision_day",
             "predicted_target_without_cue",
             "predicted_target_with_censored_cue")) {
    stopifnot(isTRUE(all.equal(p[[k]],p2[[k]])))
  }
  stopifnot(p[["baseline_sq"]]!=p2[["baseline_sq"]],
            p[["year"]]==2007,
            p[["train_event_status_varied"]] %in% 0:1,
            p[["event_observed"]] %in% 0:1)
  x2 <- ex
  x2$source[] <- 365
  always_missing <- binary_fold(x2,6,7)
  stopifnot(always_missing[["binary_model_used"]]==0,
      always_missing[["binary_sq"]]==always_missing[["baseline_sq"]])
  cat("PAYOFF-B right-censored phenology cue train/test contracts: PASS\n")
  quit(status=0)
}

# Already source-verified nested analysis: pure MODIS only; reproduces
# exactly 104 geographic pairs, 88 source cells and the 624 prior forecasts.
ctx <- new.env(parent=globalenv())
sys.source(UPSTREAM,envir=ctx)
old <- ctx$period_summary
pairs <- ctx$pairs
green <- ctx$green
period_pair <- ctx$pair_period
old_rows <- ctx$d
if(nrow(pairs)!=104L||length(unique(pairs$source_cell))!=88L||
   nrow(old_rows)!=624L ||
   abs(old$available_lag7_skill[1]-EXPECTED_BASE_EARLY)>1e-6 ||
   abs(old$available_lag7_skill[2]-EXPECTED_BASE_LATE)>1e-6 ||
   abs(old$oracle_skill[1]-EXPECTED_ORACLE_EARLY)>1e-6 ||
   abs(old$oracle_skill[2]-EXPECTED_ORACLE_LATE)>1e-6)
    stop("PR396_TO_398_FROZEN_SOURCE_METRICS_DRIFT")

rawout <- vector("list",104L*2L*3L*length(REPORT_LAGS))
iout <- 0L
for(pair in seq_len(nrow(pairs))) {
  for(w in c("early","late")) {
    years <- if(w=="early")2002:2009 else 2010:2017
    d <- period_pair(green,pairs$source_cell[pair],pairs$target_cell[pair],years)
    if(nrow(d)!=8L)stop("INCORRECT_ORIGINAL_SOURCE_YEAR_SUPPORT")
    for(fold in 6:8) {
      for(lag in REPORT_LAGS) {
        prediction <- binary_fold(d,fold,lag)
        iout <- iout+1L
        rawout[[iout]] <- data.frame(
          pair_idx=pair,
          source_cell=pairs$source_cell[pair],
          target_cell=pairs$target_cell[pair],
          period=w,
          year=as.integer(prediction[["year"]]),
          lag_days=as.integer(lag),
          heldout_target_day=prediction[["target_true_day"]],
          source_onset_day=prediction[["source_event_day"]],
          hypothetical_decision_day=prediction[["hypothetical_decision_day"]],
          positive_source_event_as_of_deadline=as.logical(
            prediction[["event_observed"]]),
          training_status_variation=as.logical(
            prediction[["train_event_status_varied"]]),
          model_with_binary_cue_fitted=as.logical(
            prediction[["binary_model_used"]]),
          training_positive_events=prediction[["train_n_ever_observed"]],
          decision_actually_before_target=as.logical(
            prediction[["decision_before_true_target"]]),
          sse_baseline=prediction[["baseline_sq"]],
          sse_binary=prediction[["binary_sq"]]
        )
      }
    }
  }
}
o <- do.call(rbind,rawout)
if(nrow(o)!=1248L ||
   nrow(unique(o[,c("pair_idx","period","year","lag_days")]))!=1248L)
  stop("CENSORED_SOURCE_FOLD_KEY_DUPLICATE")
# Verify only comparator's baseline target values, not its positive result.
selected <- o[o$lag_days==7L,]
selected <- selected[order(selected$pair_idx,selected$period,selected$year),]
original <- old_rows[order(old_rows$pair_idx,old_rows$period,
                           old_rows$year),]
if(!identical(as.integer(selected$pair_idx),as.integer(original$pair_idx))||
   !identical(selected$period,original$period)||
   !identical(as.integer(selected$year),as.integer(original$year))||
   any(abs(selected$sse_baseline-original$sse_baseline)>1e-7))
  stop("CENSORED_SOURCE_BASELINE_NOT_SAME_AS_PR398")

score <- function(d) {
  if(!nrow(d)||sum(d$sse_baseline)<=0)stop("INVALID_ORIGINAL_CV_BASELINE")
  1-sum(d$sse_binary)/sum(d$sse_baseline)
}
summary <- do.call(rbind,lapply(REPORT_LAGS,function(lag) {
  do.call(rbind,lapply(c("early","late"),function(window) {
    sub <- o[o$lag_days==lag & o$period==window,]
    total_gain <- sum(sub$sse_baseline-sub$sse_binary)
    prior <- sub$decision_actually_before_target
    data.frame(
      lag_days=lag,period=window,n_source_years=nrow(sub),
      event_positive_n=sum(sub$positive_source_event_as_of_deadline),
      event_negative_n=sum(!sub$positive_source_event_as_of_deadline),
      training_variation_folds=sum(sub$training_status_variation),
      binary_model_fitted_folds=sum(sub$model_with_binary_cue_fitted),
      binary_model_fallback_folds=sum(!sub$model_with_binary_cue_fitted),
      source_status_only_binary_skill=score(sub),
      baseline_rmse_days=sqrt(mean(sub$sse_baseline)),
      binary_rmse_days=sqrt(mean(sub$sse_binary)),
      n_decision_before_actual_target=sum(prior),
      n_decision_after_actual_target=sum(!prior),
      retrospective_gain_before_target_as_fraction_all_baseline=
        sum((sub$sse_baseline-sub$sse_binary)[prior])/sum(sub$sse_baseline),
      retrospective_gain_after_target_as_fraction_all_baseline=
        sum((sub$sse_baseline-sub$sse_binary)[!prior])/sum(sub$sse_baseline),
      total_sse_gain=total_gain
    )
  }))
}))
row.names(summary) <- NULL

# Preserve complete environmental source-cell clusters and paired periods.
pair_rows <- aggregate(cbind(sse_baseline,sse_binary)~
          pair_idx+source_cell+period+lag_days,data=o,sum)
groups <- split(seq_len(nrow(pairs)),as.character(pairs$source_cell))
set.seed(SEED)
summaries <- list()
for(lag in REPORT_LAGS) {
  a <- pair_rows[pair_rows$lag_days==lag&pair_rows$period=="early",]
  b <- pair_rows[pair_rows$lag_days==lag&pair_rows$period=="late",]
  a <- a[order(a$pair_idx),]
  b <- b[order(b$pair_idx),]
  if(!identical(a$pair_idx,b$pair_idx)||
     !identical(as.integer(a$pair_idx),seq_len(nrow(pairs))))
     stop("SOURCE_CENSORED_CLUSTER_PAIR_MISALIGNMENT")
  s0 <- numeric(B);s1 <- numeric(B);diffs <- numeric(B)
  for(k in seq_len(B)) {
    sample_cells <- sample(names(groups),length(groups),replace=TRUE)
    ix <- unlist(groups[sample_cells],use.names=FALSE)
    skill0 <- 1-sum(a$sse_binary[ix])/sum(a$sse_baseline[ix])
    skill1 <- 1-sum(b$sse_binary[ix])/sum(b$sse_baseline[ix])
    s0[k] <- skill0
    s1[k] <- skill1
    diffs[k] <- skill1-skill0
  }
  cfun <- function(v) unname(quantile(v,c(.025,.975)))
  ce <- cfun(s0);cl <- cfun(s1);cd <- cfun(diffs)
  observation <- summary[summary$lag_days==lag,]
  if(nrow(observation)!=2L)stop("SOURCE_CENSORED_PERIOD_STATUS")
  summaries[[as.character(lag)]] <- data.frame(
    lag_days=lag,
    early_skill=observation$source_status_only_binary_skill[observation$period=="early"],
    late_skill=observation$source_status_only_binary_skill[observation$period=="late"],
    early_ci_low=ce[1],early_ci_high=ce[2],
    late_ci_low=cl[1],late_ci_high=cl[2],
    change=diff(observation$source_status_only_binary_skill),
    change_ci_low=cd[1],change_ci_high=cd[2],
    source_environment_cell_blocks=length(groups),
    bootstrap_replicates=B,
    bootstrap_seed=SEED,
    status="POSTOPEN_HYPOTHETICAL_CENSORED_EVENT_INFORMATION"
  )
}
boot <- do.call(rbind,summaries)
write.csv(o,"outputs/payoff_b_modis_censored_cue_folds.csv",row.names=FALSE)
write.csv(summary,"outputs/payoff_b_modis_censored_cue_periods.csv",row.names=FALSE)
write.csv(boot,"outputs/payoff_b_modis_censored_cue_bootstrap.csv",row.names=FALSE)
cat("\nPAYOFF-B ORIGINAL SATELLITE RIGHT-CENSORED PHENOLOGY CUE TEST\n")
print(summary,row.names=FALSE,digits=7)
cat("\nSOURCE CELL BOOTSTRAP (same 88 original source blocks)\n")
print(boot,row.names=FALSE,digits=7)
cat("\nATTENTION: Censored source event observed only under hypothetical monitoring;\n")
cat("MODIS midgreenup is not a known real-time product. Retrospective event-time validity is NOT a usable decision rule.\n")
cat("No bird cue uptake, recourse, migration, fitness, eBird or causal climate test.\n")
