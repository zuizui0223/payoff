#!/usr/bin/env Rscript
# Explicitly POST-OUTCOME EXPLORATORY transfer of day-unit environmental
# forecast-skill changes to the frozen bird mismatch response.
#
# Scientific coordinates fixed in:
# docs/PAYOFF_B_V8_DAYMETRIC_BIRD_TRANSFER_EXPLORATORY_LOCK_20261015.md
#
# The original V8 degradation and signed-rho-to-mismatch transfer tests remain
# frozen. This analysis does not identify animal information, recourse or fitness.
options(stringsAsFactors = FALSE)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 10L ||
    !identical(args[c(1,3,5,7,9)],
               c("--pairs","--birds","--transfer","--structural","--output"))) {
  stop("Usage: Rscript script.R --pairs P --birds B --transfer T --structural S --output DIR")
}
inp <- setNames(args[c(2,4,6,8,10)],c("pairs","birds","transfer","structural","output"))
for (p in inp[c("pairs","birds","transfer","structural")]) {
  if (!file.exists(p)) stop("Frozen source CSV absent: ",p)
}
pairs <- read.csv(inp[["pairs"]],check.names=FALSE)
birds <- read.csv(inp[["birds"]],check.names=FALSE)
transfer <- read.csv(inp[["transfer"]],check.names=FALSE)
structural <- read.csv(inp[["structural"]],check.names=FALSE)

require_cols <- function(d,cols,label) {
  missing <- setdiff(cols,names(d))
  if (length(missing)) stop(label,": missing frozen columns: ",paste(missing,collapse=","))
}
key <- c("species","target_cell","pair_key")
require_cols(pairs,c("pair_key","delta_loo_rmse","delta_loo_value_mse"),"166-pair day metrics")
require_cols(birds,c(key,"delta_log"),"150 bird rows")
require_cols(transfer,c(key,"delta_mismatch"),"original 150 registered bird rows")
require_cols(structural,c(key,"delta_pseudo_mismatch"),"original structural-null rows")

make_key <- function(x) do.call(paste,c(x[key],sep="\r"))
no_duplicate <- function(d,key_func,label) {
  if (anyDuplicated(key_func(d))) stop(label,": duplicated original join identity")
}
no_duplicate(pairs,function(d)d$pair_key,"environment")
no_duplicate(birds,make_key,"bird day scale")
no_duplicate(transfer,make_key,"original registered transfer")
no_duplicate(structural,make_key,"original fixed-arrival null")

if (nrow(pairs)!=166L || nrow(birds)!=150L ||
    nrow(transfer)!=150L || nrow(structural)!=150L ||
    length(unique(birds$pair_key))!=72L ||
    length(unique(birds$species))!=22L)
  stop("Frozen 166-pair / 150-bird / 72-pair / 22-species sample identity drift")

# Match the published bird-day response to frozen registered log mismatch and
# the originally frozen fixed-arrival structural-null response. No new bird
# selection is possible: unmatched/duplicated original rows stop the job.
joined <- merge(birds,transfer[c(key,"delta_mismatch")],
                by=key,all.x=TRUE,sort=FALSE)
joined <- merge(joined,structural[c(key,"delta_pseudo_mismatch")],
                by=key,all.x=TRUE,sort=FALSE)
joined <- merge(joined,pairs[c("pair_key","delta_loo_rmse",
                               "delta_loo_value_mse")],
                by="pair_key",all.x=TRUE,sort=FALSE)
if (nrow(joined)!=150L ||
    anyDuplicated(make_key(joined)) ||
    length(unique(joined$pair_key))!=72L ||
    length(unique(joined$species))!=22L)
  stop("Pair/species join altered frozen sample")
required <- c("delta_log","delta_mismatch","delta_pseudo_mismatch",
              "delta_loo_rmse","delta_loo_value_mse")
if (any(!vapply(joined[required],function(v)all(is.finite(v)),logical(1))))
  stop("Nonfinite / unjoined science records; no adaptive missing-row filtering")
if (max(abs(joined$delta_log-joined$delta_mismatch)) > 1e-8)
  stop("Posthoc bird log response differs from registered frozen bird response")
joined$bird_increment <- joined$delta_log - joined$delta_pseudo_mismatch

# Only the 72 unique eligible environmental pairs define the x scale.
eligible_pair <- pairs[pairs$pair_key %in% unique(birds$pair_key),]
if (nrow(eligible_pair)!=72L) stop("72 unique pair predictor scaling sample drift")
metrics <- c("delta_loo_rmse","delta_loo_value_mse")
for (m in metrics) {
  mu <- mean(eligible_pair[[m]])
  sig <- sd(eligible_pair[[m]])
  if (!is.finite(mu) || !is.finite(sig) || sig<=0)
    stop("Predictor variance missing: ",m)
  joined[[paste0("z_",m)]] <- (joined[[m]]-mu)/sig
}
responses <- c("observed"="delta_log","fixed_arrival"="delta_pseudo_mismatch",
               "bird_increment"="bird_increment")
predictors <- paste0("z_",metrics)
spec_levels <- sort(unique(joined$species))
species_id <- match(joined$species,spec_levels)
x <- as.matrix(joined[predictors])
y <- as.matrix(joined[unname(responses)])
storage.mode(x)<-"double"
storage.mode(y)<-"double"
ylabels <- names(responses)

# Identical inverse-within-species weighted OLS with intercept at each
# cluster bootstrap replicate. Unique spatial pairs (NOT species rows) are
# the resampling units; standardized x is fixed from all 72 eligible pairs.
slopes <- function(row_id) {
  ids <- species_id[row_id]
  counts <- tabulate(ids,nbins=length(spec_levels))
  w <- 1/counts[ids]
  xx <- x[row_id,,drop=FALSE]
  yy <- y[row_id,,drop=FALSE]
  wx <- colSums(xx*w)/sum(w)
  wy <- colSums(yy*w)/sum(w)
  den <- colSums(sweep(xx,2,wx,"-")^2*w)
  if (any(!is.finite(den)) || any(den<1e-12))
    stop("Degenerate bootstrap x variance; cannot silently omit draw")
  ans <- matrix(NA_real_,nrow=length(predictors),ncol=length(ylabels),
                dimnames=list(metrics,ylabels))
  for (j in seq_along(predictors)) {
    x_center <- xx[,j]-wx[j]
    ans[j,] <- colSums(sweep(yy,2,wy,"-")*(w*x_center))/den[j]
  }
  ans
}
point <- slopes(seq_len(nrow(joined)))

ids <- sort(unique(joined$pair_key))
cluster_members <- split(seq_len(nrow(joined)),joined$pair_key)
if (length(cluster_members)!=72L) stop("Wrong bootstrap clustering unit")
B <- 10000L
seed <- 20261015L
set.seed(seed)
boots <- matrix(NA_real_,nrow=B,ncol=length(predictors)*length(ylabels))
cn <- as.vector(outer(metrics,ylabels,paste,sep="__"))
colnames(boots)<-cn
for (b in seq_len(B)) {
  sampled <- sample(ids,length(ids),replace=TRUE)
  rows <- unlist(cluster_members[sampled],use.names=FALSE)
  boots[b,] <- as.vector(slopes(rows))
}
if (any(!is.finite(boots))) stop("Nonfinite bootstrap result")

results <- do.call(rbind,lapply(seq_along(metrics),function(i) {
  do.call(rbind,lapply(seq_along(ylabels),function(j) {
    name <- paste(metrics[i],ylabels[j],sep="__")
    ci <- as.numeric(quantile(boots[,name],c(.025,.975),names=FALSE))
    beta <- point[i,j]
    data.frame(predictor=metrics[i],
      response=ylabels[j],
      beta_per_original_eligible_pair_SD=beta,
      ci_low_95=ci[1],ci_high_95=ci[2],
      ci_excludes_zero=(ci[1]>0 || ci[2]<0),
      n_species_target_rows=150L,n_environment_pairs=72L,n_species=22L,
      preregistered=FALSE,multiple_exploratory_tests=6L,
      classification="POST_OUTCOME_EXPLORATORY_NO_CAUSAL_CUE_OR_FITNESS")
  }))
}))
row.names(results)<-NULL

# The response subtraction identity also holds exactly in the regression
# coefficients (same sample, predictor and species weights).
for (m in metrics) {
  subset <- results[results$predictor==m,]
  beta <- function(label) subset$beta_per_original_eligible_pair_SD[subset$response==label]
  if (abs(beta("observed")-beta("fixed_arrival")-beta("bird_increment"))>1e-10)
    stop("Bird-specific incremental slope does not equal observed-minus-null")
}
dir.create(inp[["output"]],showWarnings=FALSE,recursive=TRUE)
write.csv(results,file.path(inp[["output"]],"day_metric_to_bird_exploratory_slopes.csv"),
          row.names=FALSE)
write.csv(joined,file.path(inp[["output"]],"day_metric_to_bird_exploratory_joined_rows.csv"),
          row.names=FALSE)
write.csv(as.data.frame(boots),file.path(inp[["output"]],"day_metric_to_bird_exploratory_bootstrap.csv"),
          row.names=FALSE)
status <- data.frame(
  status="POST_OUTCOME_EXPLORATORY_SIX_SLOPES_COMPLETE",
  n_environment_pairs_original=166L,
  n_environment_pairs_joined=72L,
  n_species_target_rows=150L,
  n_species=22L,
  n_pair_bootstrap=B,
  bootstrap_seed=seed,
  original_registered_transfer_modified=FALSE,
  direct_bird_cue_perception_identified=FALSE,
  biological_actionability_identified=FALSE,
  demographic_fitness_effect_identified=FALSE,
  outcome_informed=TRUE
)
write.csv(status,file.path(inp[["output"]],"day_metric_to_bird_exploratory_status.csv"),
          row.names=FALSE)
cat("EXPLORATORY DAY-METRIC TO BIRD-MISMATCH TRANSFER\n")
print(results)
print(status)
