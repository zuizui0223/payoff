#!/usr/bin/env Rscript
# PAYOFF-B source-skill diagnostic: eBird-free satellite forest midgreenup only.
# Exploratory after 2026-11-17 +0.08057016 correlation was known.
# Source/geometry/parameters frozen before this new CV outcome:
# docs/PAYOFF_B_MODIS_OOS_FORECAST_SKILL_FREEZE_20261117.md
options(stringsAsFactors=FALSE)

SCRIPT_PRIMARY <- "analysis/movement_phenology/payoff_b_modis_only_geographic_synchrony_20261117.R"
N_BOOT <- 10000L
SEED <- 20261117L
MIN_CHRONO_LINKS <- 30L
MIN_CHRONO_SOURCES <- 15L

forecast_holdout <- function(df,method="forward") {
  df <- df[order(df$year),c("year","source","target")]
  if(nrow(df)!=8L || any(!is.finite(as.matrix(df))) ||
     length(unique(df$year))!=8L)
    stop("SOURCE_YEAR_SUPPORT_NOT_EIGHT_UNIQUE_YEARS")
  if(!(method %in% c("forward","loyo"))) stop("Unknown frozen validation")
  tests <- if (method=="forward") 6:8 else seq_len(8)
  total_base <- 0
  total_with_cue <- 0
  for(i in tests) {
    train <- if(method=="forward") df[seq_len(i-1L),] else df[-i,]
    test <- df[i,,drop=FALSE]
    fit0 <- lm(target~year,data=train)
    fit1 <- lm(target~year+source,data=train)
    if(fit0$rank!=2L || fit1$rank!=3L)
      stop("SOURCE_FIT_RANK_DEFICIENT")
    p0 <- as.numeric(predict(fit0,newdata=test))
    p1 <- as.numeric(predict(fit1,newdata=test))
    if(length(p0)!=1 || length(p1)!=1 ||
       !is.finite(p0) || !is.finite(p1))
      stop("SOURCE_PREDICTION_NONFINITE")
    total_base <- total_base + (test$target-p0)^2
    total_with_cue <- total_with_cue + (test$target-p1)^2
  }
  c(sse_without_source=as.numeric(total_base),
    sse_with_source=as.numeric(total_with_cue),
    n_holdout_years=length(tests))
}

skill_from_sse <- function(base,with) {
  if(length(base)!=length(with) || any(!is.finite(base)) ||
     any(!is.finite(with)) || sum(base)<=0)
    stop("UNDEFINED_HELDOUT_FORECAST_SKILL")
  1-sum(with)/sum(base)
}
score_period <- function(df,period,protocol) {
  ix <- df$window==period & df$protocol==protocol
  a <- df[ix,]
  if(!nrow(a)) stop("Missing source window/protocol")
  s <- skill_from_sse(a$base,a$plus_source)
  data.frame(window=period,protocol=protocol,
       n_spatial_pairs=nrow(a),
       heldout_years_per_pair=unique(a$n_holdout_years)[1],
       rmse_without_source_days=sqrt(mean(a$base/a$n_holdout_years)),
       rmse_with_source_days=sqrt(mean(a$plus_source/a$n_holdout_years)),
       skill=s,
       fraction_pairs_source_reduces_sse=mean(a$plus_source<a$base))
}

cluster_boot <- function(long,protocol,groups,eligible_indices) {
  # Bootstraps entire source cell groups with all their linked target pairs.
  d <- long[long$protocol==protocol & long$pair_idx %in% eligible_indices,]
  uu <- split(eligible_indices,as.character(groups[eligible_indices]))
  cells <- names(uu)
  if(length(cells)<2L)stop("Insufficient source-cell bootstrap groups")
  # Matrix rows = pair IDs in original chronological pair order.
  d <- d[order(d$pair_idx,d$window),]
  early <- d[d$window=="early",]
  late <- d[d$window=="late",]
  if(!identical(early$pair_idx,late$pair_idx))
    stop("Year-window paired predictions no longer align")
  mapped <- match(early$pair_idx,eligible_indices)
  early <- early[order(mapped),]
  late <- late[order(mapped),]
  stopifnot(length(early$pair_idx)==length(eligible_indices),
            identical(early$pair_idx,late$pair_idx))
  bygroup <- split(seq_along(eligible_indices),
                   as.character(groups[eligible_indices]))
  set.seed(SEED)
  be <- numeric(N_BOOT);bl <- numeric(N_BOOT);delta <- numeric(N_BOOT)
  for (j in seq_len(N_BOOT)) {
    chosen <- sample(names(bygroup),length(bygroup),replace=TRUE)
    idx <- unlist(bygroup[chosen],use.names=FALSE)
    s0 <- skill_from_sse(early$base[idx],early$plus_source[idx])
    s1 <- skill_from_sse(late$base[idx],late$plus_source[idx])
    be[j] <- s0;bl[j] <- s1;delta[j] <- s1-s0
  }
  list(
    groups=length(bygroup),resamples=N_BOOT,seed=SEED,
    early_ci=unname(quantile(be,c(.025,.975))),
    late_ci=unname(quantile(bl,c(.025,.975))),
    change_ci=unname(quantile(delta,c(.025,.975))),
    bootstrap_unit="COMPLETE_SOURCE_ENVIRONMENTAL_CELL_GROUP"
  )
}

if("--synthetic-only" %in% commandArgs(trailingOnly=TRUE)) {
  # Synthetic tests cover causal chronological split and no target leakage.
  example <- data.frame(year=2002:2009,
      source=c(99,101,98,102,97,103,96,104),
      target=c(105,106,102,109,100,108,101,111))
  a <- forecast_holdout(example,"forward")
  b <- forecast_holdout(example,"loyo")
  stopifnot(a[["n_holdout_years"]]==3,b[["n_holdout_years"]]==8,
            a[["sse_without_source"]]>=0,b[["sse_with_source"]]>=0)
  stopifnot(abs(skill_from_sse(c(1,2),c(2,3))-(1-5/3))<1e-12)
  cat("PAYOFF-B MODIS source forecast synthetic holdout contracts: PASS\n")
  quit(status=0)
}

# Reuses the exact already frozen SHA256-verified 104-pair geography.
# It does not read final.rds, bird ranges, eBird, or bird event outcomes.
base <- new.env(parent=globalenv())
sys.source(SCRIPT_PRIMARY,envir=base)
pairs <- base$pairs
green <- base$green
pair_period <- base$pair_period
if(nrow(pairs)!=104L || length(unique(pairs$source_cell))!=88L ||
   abs(mean(pairs$delta_rho)-0.08057016)>1e-7)
  stop("FROZEN_MODIS_SOURCE_OR_GEOGRAPHY_CHANGED")

# Strict physically upstream source event pre-target in every source year,
# assessed before any held-out model fits. It is NOT proof a migrant saw it.
prior16 <- integer(nrow(pairs))
matched <- integer(nrow(pairs))
for (i in seq_len(nrow(pairs))) {
  x <- pair_period(green,pairs$source_cell[i],pairs$target_cell[i],2002:2017)
  if(nrow(x)!=16L)stop("ORIGINAL_CHRONOLOGICAL_SUPPORT_NOT_16_YEARS")
  prior16[i] <- sum(x$source<x$target)
  matched[i] <- nrow(x)
}
eligible_chronological <- which(prior16==16L)
nchrono_sources <- length(unique(pairs$source_cell[eligible_chronological]))
cat("\nPAYOFF-B SOURCE EVENT CHRONOLOGY QA BEFORE CV FIT\n")
cat("all pairs:",nrow(pairs)," strict 16/16 earlier:",
    length(eligible_chronological)," unique strict source cells:",
    nchrono_sources," median prior 16y count:",median(prior16),"\n")

perpair <- list()
ix <- 0L
for (j in seq_len(nrow(pairs))) {
  for (whichwindow in c("early","late")) {
    years <- if(whichwindow=="early") 2002:2009 else 2010:2017
    x <- pair_period(green,pairs$source_cell[j],pairs$target_cell[j],years)
    if(nrow(x)!=8L) stop("FROZEN_8YEAR_CV_INPUT_NOT_COMPLETE")
    for (protocol in c("forward","loyo")) {
      fit <- forecast_holdout(x,protocol)
      ix <- ix+1L
      perpair[[ix]] <- data.frame(
        pair_idx=j,source_cell=pairs$source_cell[j],
        target_cell=pairs$target_cell[j],
        window=whichwindow,protocol=protocol,
        n_holdout_years=as.integer(fit[["n_holdout_years"]]),
        base=fit[["sse_without_source"]],
        plus_source=fit[["sse_with_source"]],
        chrono_all_16_source_before_target=(prior16[j]==16L),
        chrono_n_source_before_target=prior16[j]
      )
    }
  }
}
long <- do.call(rbind,perpair)
# Full 104 geographical pairs even when source event occurs too late in
# some years: mathematically environmental skill, NOT attainable cue.
sc <- do.call(rbind,lapply(c("forward","loyo"),function(protocol) {
  do.call(rbind,lapply(c("early","late"),
                function(y) score_period(long,y,protocol)))
}))
row.names(sc) <- NULL

b <- cluster_boot(long,"forward",pairs$source_cell,
                  seq_len(nrow(pairs)))
f_early <- sc[sc$window=="early"&sc$protocol=="forward","skill"]
f_late <- sc[sc$window=="late"&sc$protocol=="forward","skill"]
l_early <- sc[sc$window=="early"&sc$protocol=="loyo","skill"]
l_late <- sc[sc$window=="late"&sc$protocol=="loyo","skill"]
chrono_ok <- (length(eligible_chronological)>=MIN_CHRONO_LINKS &&
              nchrono_sources>=MIN_CHRONO_SOURCES)
if(chrono_ok) {
  strict <- cluster_boot(long,"forward",pairs$source_cell,
                         eligible_chronological)
  strict_early <- score_period(long[long$pair_idx %in%
                                    eligible_chronological,],"early","forward")
  strict_late <- score_period(long[long$pair_idx %in%
                                    eligible_chronological,],"late","forward")
} else {
  strict <- NULL;strict_early <- NULL;strict_late <- NULL
}
summary <- data.frame(
    source_kind="MODIS_MCD12Q2_ONLY_NO_EBIRD",
    source_sha256="8989bf98752cf23a6be237332e35c44abff5a39d2a00d5bd1f65cce732cf6199",
    n_geographic_pairs=nrow(pairs),
    n_source_blocks=length(unique(pairs$source_cell)),
    n_southern_event_prior_all_16=length(eligible_chronological),
    n_strict_prior_source_blocks=nchrono_sources,
    source_earlier_year_fraction=sum(prior16)/(16*nrow(pairs)),
    forward_early_skill=f_early,
    forward_late_skill=f_late,
    forward_skill_change=f_late-f_early,
    forward_early_ci_low=b$early_ci[1],
    forward_early_ci_high=b$early_ci[2],
    forward_late_ci_low=b$late_ci[1],
    forward_late_ci_high=b$late_ci[2],
    forward_skill_change_ci_low=b$change_ci[1],
    forward_skill_change_ci_high=b$change_ci[2],
    retrospective_loyo_early_skill=l_early,
    retrospective_loyo_late_skill=l_late,
    retrospective_loyo_skill_change=l_late-l_early,
    strict_prior_subset_gate=if(chrono_ok)
       "STRICT_SOURCE_BEFORE_DESTINATION_ESTIMABLE" else
       "NOT_ESTIMABLE_CHRONOLOGICAL_SOURCE",
    strict_early_skill=if(chrono_ok) strict_early$skill else NA_real_,
    strict_late_skill=if(chrono_ok) strict_late$skill else NA_real_,
    strict_skill_change=if(chrono_ok)
       strict_late$skill-strict_early$skill else NA_real_,
    strict_skill_change_ci_low=if(chrono_ok) strict$change_ci[1] else NA_real_,
    strict_skill_change_ci_high=if(chrono_ok) strict$change_ci[2] else NA_real_,
    source_cell_boot_n=N_BOOT,
    source_cell_boot_seed=SEED,
    result_status="POSTOPEN_EXPLORATORY_ENVIRONMENTAL_FORECAST_DIAGNOSTIC",
    bird_cue_use_or_fitness_tested=FALSE
)
write.csv(summary,"outputs/payoff_b_modis_oos_forecast_summary.csv",row.names=FALSE)
write.csv(sc,"outputs/payoff_b_modis_oos_forecast_protocol_scores.csv",
          row.names=FALSE)
write.csv(long,"outputs/payoff_b_modis_oos_forecast_pair_scores.csv",
          row.names=FALSE)
cat("\nPAYOFF-B SATELLITE-ONLY OUT-OF-YEAR FORECAST SKILL\n")
print(summary,row.names=FALSE,digits=7)
cat("\nHeldout errors by protocol and window (days squared):\n")
print(sc,row.names=FALSE,digits=7)
cat("\nNo eBird, bird species, movement, arrival time or fitness in fit.\n")
cat("Chronological satellite event order is not migrant cue access.\n")
