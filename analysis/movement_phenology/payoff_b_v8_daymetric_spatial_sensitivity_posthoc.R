#!/usr/bin/env Rscript
# PAYOFF-B: second-stage POST-OUTCOME sensitivity for six already-opened
# exploratory V8 day-metric to bird-mismatch slopes.
#
# All four spatial/source-target bootstrap groupings and 22+72 deletions
# were fixed in docs/PAYOFF_B_V8_DAYMETRIC_SPATIAL_SENSITIVITY_LOCK_20261015.md
# AFTER the six first-stage slopes became known. NOT preregistered science.
options(stringsAsFactors=FALSE)

args <- commandArgs(trailingOnly=TRUE)
labels <- c("--original-joined","--original-slopes","--day-pairs","--output")
if (length(args)!=8L || !identical(args[c(1,3,5,7)],labels))
  stop("Use --original-joined CSV --original-slopes CSV --day-pairs CSV --output DIR")
opt <- setNames(args[c(2,4,6,8)],c("joined","slopes","pairs","output"))
for (filename in opt[c("joined","slopes","pairs")])
  if (!file.exists(filename)) stop("Missing immutable original source: ",filename)

bird <- read.csv(opt[["joined"]],check.names=FALSE)
orig <- read.csv(opt[["slopes"]],check.names=FALSE)
pairs <- read.csv(opt[["pairs"]],check.names=FALSE)

required <- function(df,cols,where) {
  missing <- setdiff(cols,names(df))
  if (length(missing)>0L) stop(where," missing: ",paste(missing,collapse=","))
}
xkeys <- c("delta_loo_rmse","delta_loo_value_mse")
ykeys <- c("observed","fixed_arrival","bird_increment")
predictors <- paste0("z_",xkeys)
responses <- c(observed="delta_log",fixed_arrival="delta_pseudo_mismatch",
               bird_increment="bird_increment")
required(bird,c("species","pair_key","target_cell",predictors,unname(responses)),
         "original joined bird rows")
required(orig,c("predictor","response","beta_per_original_eligible_pair_SD"),
         "original six slopes")
required(pairs,c("pair_key","source_cell","target_cell",
                 "target_lat","target_lng"),"original geographical pairs")
if (nrow(bird)!=150L || length(unique(bird$pair_key))!=72L ||
    length(unique(bird$species))!=22L ||
    nrow(pairs)!=166L || length(unique(pairs$pair_key))!=166L)
  stop("Original 166 environmental pairs / 72 eligible / 150 rows / 22 species changed")
if (nrow(orig)!=6L || anyDuplicated(paste(orig$predictor,orig$response))>0L)
  stop("Original six posthoc comparisons not uniquely present")

# Add only previously recorded geographical membership, never recomputing
# metrics from target physiology/arrival or constructing artificial coords.
meta <- pairs[c("pair_key","source_cell","target_cell","target_lat","target_lng")]
names(meta) <- c("pair_key","source_cell_geo","target_cell_geo",
                 "target_lat_geo","target_lng_geo")
z <- merge(bird,meta,by="pair_key",all.x=TRUE,sort=FALSE)
if (nrow(z)!=150L || length(unique(z$pair_key))!=72L ||
    length(unique(z$species))!=22L ||
    anyDuplicated(paste(z$species,z$target_cell,z$pair_key,sep="\r")))
  stop("Missing/duplicated original eligible row after geographical join")
if (any(as.character(z$target_cell)!=as.character(z$target_cell_geo)))
  stop("Original bird target-cell ID differs from environment-pair target ID")
if (any(!vapply(z[c(predictors,unname(responses),
                     "target_lat_geo","target_lng_geo")],
                 function(k)all(is.finite(k)),logical(1))))
  stop("Missing or nonfinite exact original environmental/biological coordinate")
if (any(z$target_lat_geo < -90 | z$target_lat_geo > 90 |
        z$target_lng_geo < -180 | z$target_lng_geo > 180))
  stop("Impossible original geographical coordinates")
if (max(abs(z$delta_log-z$delta_pseudo_mismatch-z$bird_increment))>1e-9)
  stop("Original observed minus fixed-arrival outcome algebra changed")

metrics <- xkeys
namesX <- predictors
namesY <- names(responses)
xmat <- as.matrix(z[namesX])
ymat <- as.matrix(z[unname(responses)])
storage.mode(xmat)<-"double"
storage.mode(ymat)<-"double"
slevel <- sort(unique(z$species))
species_idx <- match(z$species,slevel)
col_keys <- as.vector(outer(metrics,namesY,paste,sep="__"))

compute_six <- function(index) {
  if (length(index)<3L) return(rep(NA_real_,6L))
  present <- species_idx[index]
  counts <- tabulate(present,nbins=length(slevel))
  w <- 1/counts[present]
  X <- xmat[index,,drop=FALSE]
  Y <- ymat[index,,drop=FALSE]
  mx <- colSums(X*w)/sum(w)
  my <- colSums(Y*w)/sum(w)
  denom <- colSums(sweep(X,2,mx,"-")^2*w)
  if (any(!is.finite(denom)) || any(denom<1e-12))
    return(rep(NA_real_,6L))
  res <- matrix(NA_real_,nrow=2,ncol=3)
  for (j in 1:2) {
    residual_x <- X[,j]-mx[j]
    res[j,] <- colSums(sweep(Y,2,my,"-")*(w*residual_x))/denom[j]
  }
  as.vector(res)
}

point <- compute_six(seq_len(nrow(z)))
names(point)<-col_keys
if (any(!is.finite(point))) stop("Could not reproduce original all-sample slope")
for (j in seq_len(nrow(orig))) {
  nm <- paste(orig$predictor[j],orig$response[j],sep="__")
  if (!nm %in% names(point) ||
      abs(point[[nm]]-orig$beta_per_original_eligible_pair_SD[j])>1e-9)
    stop("Sensitivity point estimate drift from original opened six-slope result: ",nm)
}
for (prefix in metrics) {
  v <- point[paste(prefix,namesY,sep="__")]
  if (abs(v[1]-v[2]-v[3])>1e-10) stop("Original increment algebra failure")
}

# The target-grid blocks are frozen 5° and 10° equal-angle bins from
# the verified destination geographical coordinates.
spatial_block <- function(width) {
  paste(floor((z$target_lat_geo+90)/width),
        floor((z$target_lng_geo+180)/width),sep=":")
}
schemes <- list(
  source_cell=as.character(z$source_cell_geo),
  target_cell=as.character(z$target_cell_geo),
  target_grid_5deg=spatial_block(5),
  target_grid_10deg=spatial_block(10)
)

BOOT_REPS <- 10000L
BOOT_SEED <- 20261015L
set.seed(BOOT_SEED)
all_sensitivity <- list()
family_status <- list()
draw_list <- list()
for (family in names(schemes)) {
  block_id <- schemes[[family]]
  if (anyNA(block_id) || any(!nzchar(block_id)))
    stop("Missing original cluster label in: ",family)
  members <- split(seq_len(nrow(z)),block_id)
  K <- length(members)
  draws <- matrix(NA_real_,nrow=BOOT_REPS,ncol=length(point),
                  dimnames=list(NULL,col_keys))
  if (K>=5L) {
    for (b in seq_len(BOOT_REPS)) {
      sampled <- sample.int(K,size=K,replace=TRUE)
      picked <- unlist(members[sampled],use.names=FALSE)
      draws[b,] <- compute_six(picked)
    }
  }
  invalid <- sum(!is.finite(draws[,1]))
  if (any(rowSums(!is.finite(draws)) %in% 1:5))
    stop("Partial invalid six-slope output in a bootstrap draw")
  status <- if(K<5L || invalid>BOOT_REPS*.05) "NOT_ESTIMABLE" else "ESTIMABLE"
  family_status[[family]] <- data.frame(
    scheme=family,n_clusters=K,draws=BOOT_REPS,invalid_draws=invalid,
    invalid_fraction=invalid/BOOT_REPS,status=status,
    original_150_rows_72_pairs_22_species=TRUE)
  for (nm in col_keys) {
    val <- if(status=="ESTIMABLE")
      as.numeric(quantile(draws[,nm],c(.025,.975),na.rm=TRUE,names=FALSE)) else c(NA_real_,NA_real_)
    part <- strsplit(nm,"__",fixed=TRUE)[[1]]
    all_sensitivity[[length(all_sensitivity)+1L]] <- data.frame(
      scheme=family,predictor=part[1],response=part[2],
      beta=unname(point[nm]),ci_low_95=val[1],ci_high_95=val[2],
      n_original_species_target=150L,n_original_environment_pairs=72L,
      n_boot_valid=BOOT_REPS-invalid,
      classification="POST_OUTCOME_EXPLORATORY_SPATIAL_SENSITIVITY",
      inference_status=status)
  }
  draw_list[[family]] <- data.frame(draw=seq_len(BOOT_REPS),
                                    scheme=family,draws,check.names=FALSE)
}
sensitivity <- do.call(rbind,all_sensitivity)
status <- do.call(rbind,family_status)

# Every leave-one-out value is reported as descriptive influence, NOT a
# candidate final model after choosing favorable exclusions.
deletion <- list()
for (group in c("species","pair_key")) {
  labels <- sort(unique(as.character(z[[group]])))
  for (name in labels) {
    remaining <- which(as.character(z[[group]])!=name)
    coeff <- compute_six(remaining)
    for (j in seq_along(col_keys)) {
      part <- strsplit(col_keys[j],"__",fixed=TRUE)[[1]]
      deletion[[length(deletion)+1L]] <- data.frame(
        omission_type=group,omitted_unit=name,
        predictor=part[1],response=part[2],
        beta=coeff[j],valid=is.finite(coeff[j]))
    }
  }
}
deletion <- do.call(rbind,deletion)
deleted_summary <- do.call(rbind,lapply(split(deletion,
  interaction(deletion$omission_type,deletion$predictor,deletion$response,drop=TRUE)),
  function(part) {
    actual <- part$beta[is.finite(part$beta)]
    data.frame(omission_type=part$omission_type[1],
      predictor=part$predictor[1],response=part$response[1],
      n_attempted=nrow(part),n_invalid=sum(!part$valid),
      min_beta=if(length(actual))min(actual) else NA_real_,
      max_beta=if(length(actual))max(actual) else NA_real_,
      fraction_positive=if(length(actual))mean(actual>0) else NA_real_)
  }))
expected_loo <- 22L*6L+72L*6L
if (nrow(deletion)!=expected_loo ||
    any(deleted_summary$n_attempted[deleted_summary$omission_type=="species"]!=22L) ||
    any(deleted_summary$n_attempted[deleted_summary$omission_type=="pair_key"]!=72L))
  stop("Exploratory LOYO sensitive omission record missing")

out <- opt[["output"]]
dir.create(out,recursive=TRUE,showWarnings=FALSE)
write.csv(sensitivity,file.path(out,"spatial_sensitivity_all_24_intervals.csv"),row.names=FALSE)
write.csv(status,file.path(out,"spatial_sensitivity_scheme_status.csv"),row.names=FALSE)
write.csv(deletion,file.path(out,"leave_one_unit_out_all_564_slopes.csv"),row.names=FALSE)
write.csv(deleted_summary,file.path(out,"leave_one_unit_out_summary.csv"),row.names=FALSE)
for (family in names(draw_list)) {
  write.csv(draw_list[[family]],
    file.path(out,paste0("bootstrap_",family,"_10000.csv")),row.names=FALSE)
}
cat("AFTER-SIX-OUTCOME EXPLORATORY GEOGRAPHICAL SENSITIVITY\n")
print(status)
print(sensitivity)
print(deleted_summary)
