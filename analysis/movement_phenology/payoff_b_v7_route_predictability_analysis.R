#!/usr/bin/env Rscript

# PAYOFF-B V7 focal analysis.
# DO NOT RUN until:
# 1) Nemes schema gate is frozen PASS;
# 2) USA-NPN/BEST source gate is frozen PASS;
# 3) route-predictability file has been built outcome-blind and receipted.

options(stringsAsFactors = FALSE)

suppressPackageStartupMessages({
  library(lme4)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop("usage: payoff_b_v7_route_predictability_analysis.R NEMES_WIDE.rds PREDICTABILITY.csv OUTPUT_DIR")
}
wide_path <- args[[1]]
pred_path <- args[[2]]
out_dir <- args[[3]]
dir.create(out_dir, recursive=TRUE, showWarnings=FALSE)

d <- readRDS(wide_path)
p <- read.csv(pred_path, stringsAsFactors=FALSE)
stopifnot(is.data.frame(d), is.data.frame(p))

required_d <- c(
  "motusTagID","species","year","site_id_r1","site_id_r2",
  "lag_best_act_r1","lag_best_act_r2","dist_km","gw_rate_best_act"
)
required_p <- c(
  "motusTagID","year","site_id_r1","site_id_r2",
  "predictability_pearson","predictability_spearman","historical_n",
  "predictability_common_pearson","predictability_common_spearman",
  "common_historical_n","source"
)
miss_d <- setdiff(required_d,names(d))
miss_p <- setdiff(required_p,names(p))
if(length(miss_d)) stop("missing Nemes columns: ",paste(miss_d,collapse=", "))
if(length(miss_p)) stop("missing predictability columns: ",paste(miss_p,collapse=", "))

d$year <- as.character(d$year)
p$year <- as.character(p$year)

m <- merge(
  d,
  p,
  by=c("motusTagID","year","site_id_r1","site_id_r2"),
  all=FALSE,
  suffixes=c("","_pred")
)

m$recovery <- m$lag_best_act_r1 - m$lag_best_act_r2
m$species <- factor(m$species)
m$year_f <- factor(m$year)
m$site1_f <- factor(m$site_id_r1)
m$site2_f <- factor(m$site_id_r2)

z <- function(x) as.numeric(scale(x))
m$dist_z <- z(m$dist_km)
m$greenwave_z <- z(m$gw_rate_best_act)

complete_primary <- with(m,
  is.finite(recovery) &
  is.finite(predictability_pearson) &
  historical_n >= 20 &
  is.finite(lag_best_act_r1) &
  is.finite(dist_z) &
  is.finite(greenwave_z)
)
a <- m[complete_primary,,drop=FALSE]

if(nrow(a) < 50) stop("primary completeness gate failed: n<50")
if(length(unique(a$species)) < 3) stop("primary completeness gate failed: <3 species")

fit_formula <- recovery ~ predictability_pearson + lag_best_act_r1 +
  dist_z + greenwave_z + species + year_f +
  (1|site1_f) + (1|site2_f)

fit <- lmer(fit_formula, data=a, REML=FALSE)

extract_term <- function(model, term, label, n) {
  cf <- coef(summary(model))
  if(!term %in% rownames(cf)) stop("term missing from model: ",term)
  est <- cf[term,"Estimate"]
  se <- cf[term,"Std. Error"]
  data.frame(
    analysis=label,
    term=term,
    n=n,
    estimate=est,
    se=se,
    lcl=est-1.96*se,
    ucl=est+1.96*se,
    singular=isSingular(model,tol=1e-4),
    stringsAsFactors=FALSE
  )
}

results <- list(
  extract_term(fit,"predictability_pearson","PRIMARY_PREOUTCOME_PEARSON",nrow(a))
)

# Mandatory rank-predictability sensitivity.
b <- a[is.finite(a$predictability_spearman),,drop=FALSE]
if(nrow(b) >= 50) {
  f <- lmer(update(fit_formula, . ~ . - predictability_pearson + predictability_spearman),
            data=b, REML=FALSE)
  results[[length(results)+1]] <- extract_term(
    f,"predictability_spearman","SENSITIVITY_SPEARMAN",nrow(b)
  )
}

# Mandatory common-window Pearson sensitivity.
c <- m[
  is.finite(m$recovery) &
  is.finite(m$predictability_common_pearson) &
  m$common_historical_n >= 20 &
  is.finite(m$lag_best_act_r1) &
  is.finite(m$dist_z) &
  is.finite(m$greenwave_z),
  ,drop=FALSE
]
if(nrow(c) >= 50 && length(unique(c$species)) >= 3) {
  f <- lmer(
    recovery ~ predictability_common_pearson + lag_best_act_r1 +
      dist_z + greenwave_z + species + year_f +
      (1|site1_f) + (1|site2_f),
    data=c, REML=FALSE
  )
  results[[length(results)+1]] <- extract_term(
    f,"predictability_common_pearson","SENSITIVITY_COMMON_WINDOW",nrow(c)
  )
}

# Leave-one-species-out fits; no species is reweighted or removed based on result.
for(sp in levels(a$species)) {
  zdat <- a[as.character(a$species) != sp,,drop=FALSE]
  zdat$species <- droplevels(zdat$species)
  if(nrow(zdat) < 40 || length(unique(zdat$species)) < 2) next
  f <- try(lmer(fit_formula,data=zdat,REML=FALSE),silent=TRUE)
  if(inherits(f,"try-error")) next
  results[[length(results)+1]] <- extract_term(
    f,"predictability_pearson",paste0("LOO_SPECIES_",sp),nrow(zdat)
  )
}

res <- do.call(rbind,results)
write.csv(res,file.path(out_dir,"v7_model_coefficients.csv"),row.names=FALSE)

primary <- res[res$analysis=="PRIMARY_PREOUTCOME_PEARSON",,drop=FALSE]
classification <- if(primary$lcl > 0) {
  "SUPPORTED_POSITIVE"
} else if(primary$ucl < 0) {
  "SUPPORTED_WRONG_DIRECTION"
} else {
  "INSUFFICIENT_SUPPORT"
}

summary <- data.frame(
  metric=c(
    "analysis_n",
    "species_n",
    "south_sites_n",
    "north_sites_n",
    "route_pairs_n",
    "primary_estimate",
    "primary_lcl",
    "primary_ucl",
    "primary_singular",
    "classification"
  ),
  value=c(
    nrow(a),
    length(unique(a$species)),
    length(unique(a$site_id_r1)),
    length(unique(a$site_id_r2)),
    length(unique(paste(a$site_id_r1,a$site_id_r2,sep=" -> "))),
    primary$estimate,
    primary$lcl,
    primary$ucl,
    primary$singular,
    classification
  ),
  stringsAsFactors=FALSE
)
write.csv(summary,file.path(out_dir,"v7_primary_summary.csv"),row.names=FALSE)

# No individual-level rows are written to the result artifact.
cat("V7_OUTCOME_OPENED=TRUE\n")
cat("V7_CLASSIFICATION=",classification,"\n",sep="")
