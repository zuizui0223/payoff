#!/usr/bin/env Rscript
options(stringsAsFactors=FALSE)

source("analysis/movement_phenology/payoff_b_v8_primary.R", local=FALSE)
source("analysis/movement_phenology/payoff_b_v8_transfer_helpers.R", local=FALSE)
if (!requireNamespace("sandwich", quietly=TRUE)) stop("sandwich package required")

m <- unique(eligible_map[,c("species","target_cell","source_cell","pair_key","source_target_distance_km")])
m <- m[m$pair_key %in% pairs$pair_key,]
y <- unique(dat[,c("species","year","cell","arr_GAM_mean","gr_mn")])
y$year <- as.integer(y$year)
y$cell <- as.numeric(as.character(y$cell))
y$arr_GAM_mean <- as.numeric(y$arr_GAM_mean)
y$gr_mn <- as.numeric(y$gr_mn)
y <- y[is.finite(y$year)&is.finite(y$cell)&is.finite(y$arr_GAM_mean)&is.finite(y$gr_mn),]

build_row <- function(i) {
  q <- m[i,]
  z <- y[y$species==q$species & y$cell==q$target_cell,]
  e <- z[z$year>=EARLY_START & z$year<=EARLY_END,]
  l <- z[z$year>=LATE_START & z$year<=LATE_END,]
  if(nrow(e)<MIN_PAIRS_PER_WINDOW || nrow(l)<MIN_PAIRS_PER_WINDOW) return(NULL)
  me <- log1p(abs(e$arr_GAM_mean-e$gr_mn))
  ml <- log1p(abs(l$arr_GAM_mean-l$gr_mn))
  data.frame(
    species=q$species,target_cell=q$target_cell,source_cell=q$source_cell,
    pair_key=q$pair_key,source_target_distance_km=q$source_target_distance_km,
    early_n=nrow(e),late_n=nrow(l),
    mismatch_early=mean(me),mismatch_late=mean(ml),
    delta_mismatch=mean(ml)-mean(me),
    target_shift_abs=abs(mean(l$gr_mn)-mean(e$gr_mn))
  )
}

out <- do.call(rbind, Filter(Negate(is.null), lapply(seq_len(nrow(m)),build_row)))
out <- merge(out,pairs[,c("pair_key","rho_early","rho_late","delta_rho")],
             by="pair_key",all.x=TRUE,sort=FALSE)
out <- out[is.finite(out$delta_rho)&is.finite(out$delta_mismatch)&is.finite(out$target_shift_abs),]
if(nrow(out)<50 || length(unique(out$species))<10 || length(unique(out$pair_key))<30)
  stop("Transfer outcome gate failed")

t1 <- metric_pair_boot(out)
out$z_delta_rho <- as.numeric(scale(out$delta_rho))
out$z_target_shift_abs <- as.numeric(scale(out$target_shift_abs))
out$species <- factor(out$species)
out$pair_key <- factor(out$pair_key)

fit <- lm(delta_mismatch ~ z_delta_rho + z_target_shift_abs + species,data=out)
t2 <- cluster_term(fit,out,"z_delta_rho")
fit_a <- lm(mismatch_late ~ mismatch_early + z_delta_rho + z_target_shift_abs + species,data=out)
ta <- cluster_term(fit_a,out,"z_delta_rho")

spp <- sort(unique(as.character(out$species)))
loo <- do.call(rbind,lapply(spp,function(sp){
  d <- out[as.character(out$species)!=sp,]
  d$species <- droplevels(d$species)
  sm <- aggregate(delta_mismatch~species,d,mean)
  f <- lm(delta_mismatch ~ z_delta_rho + z_target_shift_abs + species,data=d)
  data.frame(
    omitted_species=sp,rows=nrow(d),pairs=length(unique(d$pair_key)),
    equal_species_delta_mismatch=mean(sm$delta_mismatch),
    t2_ordinary_beta_delta_rho=unname(coef(f)["z_delta_rho"])
  )
}))

paradox <- t1$species_mean>0 && t1$species_ci[1]>0
transfer <- t2["estimate"]<0 && t2["high"]<0
summary <- data.frame(
  source_commit=SOURCE_COMMIT,early_window=paste0(EARLY_START,"-",EARLY_END),
  late_window=paste0(LATE_START,"-",LATE_END),
  eligible_species_target_rows=nrow(out),unique_spatial_pairs=length(unique(out$pair_key)),
  species=length(unique(out$species)),
  t1_row_mean_delta_mismatch=t1$row_mean,t1_row_ci_low_95=t1$row_ci[1],
  t1_row_ci_high_95=t1$row_ci[2],
  t1_equal_species_delta_mismatch=t1$species_mean,
  t1_equal_species_ci_low_95=t1$species_ci[1],
  t1_equal_species_ci_high_95=t1$species_ci[2],
  t1_strong_paradox_status=ifelse(paradox,"SUPPORTED","NOT_SUPPORTED"),
  t2_beta_z_delta_rho=t2["estimate"],t2_cluster_se=t2["se"],
  t2_ci_low_95=t2["low"],t2_ci_high_95=t2["high"],t2_df=t2["df"],
  t2_transfer_status=ifelse(transfer,"TRANSFER_SUPPORTED","TRANSFER_NOT_SUPPORTED"),
  ancova_beta_z_delta_rho=ta["estimate"],ancova_cluster_se=ta["se"],
  ancova_ci_low_95=ta["low"],ancova_ci_high_95=ta["high"],
  loo_equal_species_delta_min=min(loo$equal_species_delta_mismatch),
  loo_equal_species_delta_max=max(loo$equal_species_delta_mismatch),
  loo_equal_species_positive_n=sum(loo$equal_species_delta_mismatch>0),
  loo_t2_beta_min=min(loo$t2_ordinary_beta_delta_rho),
  loo_t2_beta_max=max(loo$t2_ordinary_beta_delta_rho),
  loo_t2_beta_negative_n=sum(loo$t2_ordinary_beta_delta_rho<0),
  bootstrap_replicates=10000L,bootstrap_seed=20261005L
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(out,"outputs/payoff_b_v8_environment_to_bird_transfer_rows.csv",row.names=FALSE)
write.csv(summary,"outputs/payoff_b_v8_environment_to_bird_transfer_summary.csv",row.names=FALSE)
write.csv(loo,"outputs/payoff_b_v8_environment_to_bird_transfer_loo.csv",row.names=FALSE)
write.csv(data.frame(replicate=seq_along(t1$row_boot),
  row_mean_delta_mismatch=t1$row_boot,
  equal_species_delta_mismatch=t1$species_boot),
  "outputs/payoff_b_v8_environment_to_bird_transfer_bootstrap.csv",row.names=FALSE)

cat("\nPAYOFF-B V8 ENVIRONMENT-TO-BIRD TRANSFER\n")
print(summary)
cat("\nNo migration-speed or fitness outcome was used.\n")
