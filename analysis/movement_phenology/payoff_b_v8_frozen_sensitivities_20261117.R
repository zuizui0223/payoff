#!/usr/bin/env Rscript
# PAYOFF-B V8: sensitivities defined in the 2026-10-05 V8 contract.
# Run AFTER the original primary result was opened and frozen in its ledger.
# Additional source-cell cluster bootstrap is explicitly POST-OPEN.
options(stringsAsFactors=FALSE)
primary <- "analysis/movement_phenology/payoff_b_v8_frozen_unique_pair_primary_20261117.R"
source(primary, local=FALSE)  # recompute frozen original, no changed filters
if (nrow(pairs)!=166L || abs(pair_delta_mean-0.3690225)>1e-5 ||
    abs(species_delta_mean-0.3363547)>1e-5 ||
    abs(result$pair_boot_ci_low[1]-0.2992332)>1e-5 ||
    abs(result$pair_boot_ci_high[1]-0.4373114)>1e-5) {
  stop("FROZEN 2026-11-17 PRIMARY NUMBERS CHANGED: DO NOT RUN SENSITIVITY")
}
cat("\nPAYOFF-B V8 post-primary sensitivities: original primary fully reproduced\n")
pair_ci_boot <- function(d,n=10000L,seed=20261005L) {
  if (length(d)<2L || any(!is.finite(d))) return(c(NA_real_,NA_real_))
  set.seed(seed)
  means <- replicate(n,mean(sample(d,length(d),replace=TRUE)))
  unname(quantile(means,c(.025,.975)))
}
metric_record <- function(name,delta,n,comment) {
  ci <- pair_ci_boot(delta)
  data.frame(name=name,n_unique_pairs=n,mean_delta_rho=mean(delta),
             ci_low=ci[1],ci_high=ci[2],
             negative_pair_fraction=mean(delta<0),
             classification=comment)
}

sens <- list()
# 1. Frozen Fisher-z, using predeclared ±0.999 numerical clamp.
clamp <- function(r) pmin(.999,pmax(-.999,r))
fz <- atanh(clamp(pairs$late_rho))-atanh(clamp(pairs$early_rho))
sens[[length(sens)+1L]] <- metric_record(
  "FISHER_Z_DELTA_SAME_166_PAIRS",fz,length(fz),
  "PRESPECIFIED_SCALE_CHANGE_NOT_PRIMARY"
)
# 2. Paired complete 8/8 years only.
complete <- pairs[pairs$early_n==8L & pairs$late_n==8L,]
if (nrow(complete)>1) {
  sens[[length(sens)+1L]] <- metric_record(
    "EXACT_8_OF_8_YEARS_BOTH_WINDOWS",complete$delta_rho,nrow(complete),
    "PRESPECIFIED_COMPLETE_CASE"
  )
}
# 3. Alternative 7-year non-overlapping windows, minimum paired years 6.
p7 <- pairs
p7$early7 <- NA_real_
p7$late7 <- NA_real_
p7$n_early7 <- integer(nrow(p7))
p7$n_late7 <- integer(nrow(p7))
for (i in seq_len(nrow(p7))) {
  a <- pair_years(green,p7$source_cell[i],p7$target_cell[i],2002:2008)
  b <- pair_years(green,p7$source_cell[i],p7$target_cell[i],2011:2017)
  p7$n_early7[i] <- nrow(a)
  p7$n_late7[i] <- nrow(b)
  p7$early7[i] <- detrended_r(a)
  p7$late7[i] <- detrended_r(b)
}
ok7 <- is.finite(p7$early7)&is.finite(p7$late7)&
       p7$n_early7>=MIN_PAIRS&p7$n_late7>=MIN_PAIRS
sens[[length(sens)+1L]] <- metric_record(
  "ALT_7_YEAR_2002_2008_VS_2011_2017",
  p7$late7[ok7]-p7$early7[ok7],sum(ok7),
  "PRESPECIFIED_ALTERNATE_WINDOW"
)
# 4. Undetrended correlations as negative control, not primary replacement.
raw_r <- function(x) {
  if (nrow(x)<MIN_PAIRS || sd(x$source)<=0 || sd(x$target)<=0)
    return(NA_real_)
  cor(x$source,x$target)
}
pr <- pairs
pr$rraw_early <- NA_real_
pr$rraw_late <- NA_real_
for (i in seq_len(nrow(pr))) {
  a <- pair_years(green,pr$source_cell[i],pr$target_cell[i],EARLY)
  b <- pair_years(green,pr$source_cell[i],pr$target_cell[i],LATE)
  pr$rraw_early[i] <- raw_r(a)
  pr$rraw_late[i] <- raw_r(b)
}
okraw <- is.finite(pr$rraw_early)&is.finite(pr$rraw_late)
sens[[length(sens)+1L]] <- metric_record(
  "UNDE-TRENDED_RHO_NEGATIVE_CONTROL",
  pr$rraw_late[okraw]-pr$rraw_early[okraw],sum(okraw),
  "PRESPECIFIED_UNDE-TRENDED_NOT_PRIMARY"
)
# 5. Source-to-target distance moderator: cell coordinates need
# a single original environmental centroid per unique cell.
coordinates <- unique(raw[,c("cell","cell_lat2","cell_lng")])
coordinates$cell <- as.numeric(as.character(coordinates$cell))
coordinates$cell_lat2 <- as.numeric(coordinates$cell_lat2)
coordinates$cell_lng <- as.numeric(coordinates$cell_lng)
# Original data can repeat the same cell/coords across taxa/years, but
# contradictory coordinates invalidate environmental distance inference.
if (anyDuplicated(coordinates$cell)) {
  stop("The same source cell has multiple coordinates; distance not admitted")
}
src <- match(pairs$source_cell,coordinates$cell)
tgt <- match(pairs$target_cell,coordinates$cell)
if (anyNA(src)||anyNA(tgt)) stop("No independently sourced cell centroid")
dist <- hav(coordinates$cell_lat2[src],coordinates$cell_lng[src],
            coordinates$cell_lat2[tgt],coordinates$cell_lng[tgt])
if (any(!is.finite(dist)) || any(dist<=0)) stop("Invalid positive source-target distance")
fit <- lm(pairs$delta_rho ~ log1p(dist))
distance_beta <- unname(coef(fit)[2])
distance_ci <- unname(confint(fit)[2,])
# Correlated links may make OLS uncertainty too narrow; descriptive only.
distance_summary <- data.frame(
  moderator="log1p_source_target_distance_km",
  beta_delta_rho_per_log_distance=distance_beta,
  nominal_ols_ci_low=distance_ci[1],
  nominal_ols_ci_high=distance_ci[2],
  pearson_cor=cor(log1p(dist),pairs$delta_rho),
  median_distance_km=median(dist),
  caution="DESCRIPTIVE_ONLY_SHARED_CELLS_MAY_CORRELATE"
)
# 6. Leave-one-species-out; a pair used by remaining species stays once.
loo <- lapply(species,function(s) {
  remaining <- eligible[eligible$species!=s,]
  keys <- unique(remaining$pair_id)
  d <- pairs$delta_rho[match(keys,pairs$pair_id)]
  data.frame(species_left_out=s,remaining_unique_pairs=length(keys),
     remaining_species=length(unique(remaining$species)),
     unique_pair_mean_delta=mean(d),
     equal_species_mean_delta=mean(species_delta[species!=s]))
})
loo <- do.call(rbind,loo)
# 7. Target-cell equal weighting within each species.
species_target <- aggregate(target_cell ~ species,
        data=eligible,FUN=function(v) length(v)==length(unique(v)))
if (!all(species_target$target_cell))
    stop("Original mapping includes repeated target-cell species exposures")
target_equal_species_mean <- species_delta_mean  # mathematically identical
# 8. Additional robustness, POST-OPEN: shared source-cell block resampling.
# Unlike unique-pair bootstrap, all pairs from one source cell travel together.
source_cells <- sort(unique(pairs$source_cell))
set.seed(SEED)
src_boot <- numeric(B)
for (k in seq_len(B)) {
  sampled <- sample(source_cells,length(source_cells),replace=TRUE)
  chosen <- unlist(lapply(sampled,function(s)
      which(pairs$source_cell==s)),use.names=FALSE)
  src_boot[k] <- mean(pairs$delta_rho[chosen])
}
source_block_ci <- unname(quantile(src_boot,c(.025,.975)))
source_block <- data.frame(
  block="SOURCE_CELL_CLUSTER_POST_OPEN",source_blocks=length(source_cells),
  n_links=nrow(pairs),observed_pair_mean_delta=pair_delta_mean,
  block_boot_ci_low=source_block_ci[1],
  block_boot_ci_high=source_block_ci[2],
  inferential_role="POST_OPEN_ROBUSTNESS_NOT_FROZEN_PRIMARY"
)
# Original primary pair-sample bootstrap does not always retain every species.
# Do NOT impute missing species, report the concern and fixed 28-species LOO.
summary <- do.call(rbind,sens)
write.csv(summary,"outputs/payoff_b_v8_frozen_sensitivity_summary.csv",row.names=FALSE)
write.csv(distance_summary,"outputs/payoff_b_v8_distance_moderator.csv",row.names=FALSE)
write.csv(loo,"outputs/payoff_b_v8_leave_one_species_out.csv",row.names=FALSE)
write.csv(source_block,"outputs/payoff_b_v8_postopen_source_cell_blocks.csv",row.names=FALSE)
cat("\nV8 SENSITIVITY RESULTS\n")
print(summary,row.names=FALSE,digits=6)
cat("\nV8 DISTANCE MODERATOR (descriptive)\n")
print(distance_summary,row.names=FALSE,digits=6)
cat("\nV8 LOO species unique-pair delta range:",
    range(loo$unique_pair_mean_delta),"\n")
cat("V8 LOO equal-species delta range:",
    range(loo$equal_species_mean_delta),"\n")
cat("V8 target-cell equal-weight mean:",target_equal_species_mean,"\n")
cat("V8 post-open source-cell bootstrap interval:",source_block_ci,
    "with ",length(source_cells),"source cells\n")
cat("Migration-distance CLASS: NOT_RUN if source metadata unavailable.\n")
cat("No change to preregistered primary V8 rejection of broad degradation.\n")
