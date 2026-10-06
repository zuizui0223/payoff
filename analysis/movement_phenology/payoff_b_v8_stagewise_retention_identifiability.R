#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC IDENTIFIABILITY AUDIT FOR STAGEWISE PHASE-RETENTION SLOPES.
#
# Raw stagewise phase-retention regressions use source phase as a predictor:
#
#   target_phase ~ source_phase + unit FE + year FE.
#
# Source phase contains estimated source arrival date, whose posterior SD differs
# strongly between periods. Classical predictor measurement error attenuates
# slopes. This audit asks whether the latent within-period source-phase variance
# is even identifiable after accounting for the reported arrival uncertainty.
#
# Under independent classical predictor error with known variance Sigma_e:
#
#   E[x_obs' M x_obs]
#      =
#   x_true' M x_true + trace(M Sigma_e),
#
# where M residualizes unit and year fixed effects.
#
# Therefore a method-of-moments latent predictor sum of squares is:
#
#   SS_true_hat = x_obs' M x_obs - trace(M Sigma_e).
#
# If this is <= 0, an errors-in-variables corrected retention slope is not
# identified under this approximation.
#
# The approximation ignores covariance among posterior arrival estimates and
# does not claim the reported posterior SD is classical independent error. It is
# deliberately a stress test against overinterpreting raw retention slopes.

GATE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_admission_gate.R"
if (!file.exists(GATE_SCRIPT)) stop("Missing admission-gate script")
source(GATE_SCRIPT, local=FALSE)

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
    is.finite(d$arr_GAM_sd) &
    d$arr_GAM_sd>0 &
    is.finite(d$gr_mn),
  ,
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
rows$unit_id <- paste(
  rows$species,rows$source_cell,rows$target_cell,sep="::"
)

counts <- aggregate(
  year ~ unit_id + species + source_cell + target_cell + pair_key + period,
  data=rows,
  FUN=function(x) length(unique(x))
)
ce <- counts[counts$period=="early",]
cl <- counts[counts$period=="late",]
names(ce)[names(ce)=="year"] <- "early_n"
names(cl)[names(cl)=="year"] <- "late_n"
ce$period <- NULL
cl$period <- NULL
units <- merge(
  ce,cl,
  by=c("unit_id","species","source_cell","target_cell","pair_key"),
  all=FALSE
)
units <- units[
  units$early_n>=MIN_YEARS &
    units$late_n>=MIN_YEARS,
  ,
  drop=FALSE
]
rows <- rows[rows$unit_id %in% units$unit_id,,drop=FALSE]

rows$source_phase <- rows$source_arrival-rows$source_greenup
rows$target_phase <- rows$target_arrival-rows$target_greenup

# Fixed-arrival environmental null for comparison.
src_mu <- aggregate(
  source_arrival ~ unit_id + period,
  data=rows,FUN=mean
)
tgt_mu <- aggregate(
  target_arrival ~ unit_id + period,
  data=rows,FUN=mean
)
names(src_mu)[3] <- "source_arrival_fixed"
names(tgt_mu)[3] <- "target_arrival_fixed"
rows <- merge(rows,src_mu,by=c("unit_id","period"),all.x=TRUE,sort=FALSE)
rows <- merge(rows,tgt_mu,by=c("unit_id","period"),all.x=TRUE,sort=FALSE)
rows$source_phase_fixed <- rows$source_arrival_fixed-rows$source_greenup
rows$target_phase_fixed <- rows$target_arrival_fixed-rows$target_greenup

audit_period <- function(z){
  X <- model.matrix(~ factor(unit_id)+factor(year),data=z)
  qrX <- qr(X)
  Q <- qr.Q(qrX,complete=FALSE)
  h <- rowSums(Q^2)
  Mdiag <- 1-h

  # Residualize x and y on fixed effects.
  xfit <- lm.fit(X,z$source_phase)
  yfit <- lm.fit(X,z$target_phase)
  xr <- xfit$residuals
  yr <- yfit$residuals

  numerator <- sum(xr*yr)
  observed_ss <- sum(xr^2)
  expected_error_ss <- sum(Mdiag*(z$source_arrival_sd^2))
  latent_ss_hat <- observed_ss-expected_error_ss

  observed_beta <- numerator/observed_ss
  corrected_beta <- if(
    is.finite(latent_ss_hat) && latent_ss_hat>0
  ){
    numerator/latent_ss_hat
  }else{
    NA_real_
  }

  # Environmental fixed-arrival null.
  xf <- lm.fit(X,z$source_phase_fixed)$residuals
  yf <- lm.fit(X,z$target_phase_fixed)$residuals
  fixed_beta <- sum(xf*yf)/sum(xf^2)

  data.frame(
    n=nrow(z),
    units=length(unique(z$unit_id)),
    years=length(unique(z$year)),
    observed_beta=observed_beta,
    fixed_arrival_beta=fixed_beta,
    observed_source_residual_ss=observed_ss,
    expected_source_measurement_error_ss=expected_error_ss,
    latent_source_ss_hat=latent_ss_hat,
    error_to_observed_ss_ratio=expected_error_ss/observed_ss,
    eiv_corrected_beta=corrected_beta,
    eiv_identified=latent_ss_hat>0,
    mean_source_arrival_sd=mean(z$source_arrival_sd),
    mean_target_arrival_sd=mean(z$target_arrival_sd)
  )
}

early <- audit_period(rows[rows$period=="early",,drop=FALSE])
late <- audit_period(rows[rows$period=="late",,drop=FALSE])
early$period <- "early"
late$period <- "late"
summary_df <- rbind(early,late)

status <- data.frame(
  eligible_units=nrow(units),
  unique_pairs=length(unique(units$pair_key)),
  species=length(unique(units$species)),
  early_eiv_identified=early$eiv_identified,
  late_eiv_identified=late$eiv_identified,
  retention_mechanism_status=if(
    early$eiv_identified && late$eiv_identified
  ) "EIV_SLOPES_IDENTIFIABLE_UNDER_APPROXIMATION"
  else "RETENTION_SLOPE_NOT_FULLY_IDENTIFIABLE"
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  summary_df,
  "outputs/payoff_b_v8_stagewise_retention_identifiability_summary.csv",
  row.names=FALSE
)
write.csv(
  status,
  "outputs/payoff_b_v8_stagewise_retention_identifiability_status.csv",
  row.names=FALSE
)

cat("\nSTAGEWISE RETENTION IDENTIFIABILITY AUDIT\n")
print(summary_df)
print(status)
