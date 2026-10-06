#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

# POSTHOC SOURCE-DEFINITION SENSITIVITY.
#
# The frozen V8 mapping uses the nearest lower-latitude migratory-range cell as
# the nonlocal environmental source for each breeding target.
#
# This audit asks whether the temporal increase in cross-validated forecast
# value is specific to that nearest source or is similarly present for the
# second- and third-nearest lower-latitude migratory cells.
#
# If rank 1 is not distinct from ranks 2-3, the environmental result should be
# interpreted as broader regional nonlocal forecast opportunity rather than a
# route-specific source property.

GATE_SCRIPT <- "analysis/movement_phenology/payoff_b_v8_admission_gate.R"
if (!file.exists(GATE_SCRIPT)) stop("Missing admission-gate script")
source(GATE_SCRIPT, local=FALSE)

B <- 5000L
SEED <- 20261006L
MAX_RANK <- 3L

# Build deterministic source ranks for every frozen breeding target.
targets_rank <- cells[
  cells$is_breed,
  c("species","cell","cell_lat2","cell_lng")
]
targets_rank <- targets_rank[order(targets_rank$species,targets_rank$cell),]

maps <- vector("list",nrow(targets_rank))
m_n <- 0L

for(i in seq_len(nrow(targets_rank))){
  target <- targets_rank[i,]
  candidates <- cells[
    cells$species==target$species &
      cells$is_mig &
      is.finite(cells$cell_lat2) &
      cells$cell_lat2<target$cell_lat2,
    c("cell","cell_lat2","cell_lng")
  ]
  if(nrow(candidates)<MAX_RANK) next

  candidates$distance_km <- haversine_km(
    candidates$cell_lat2,
    candidates$cell_lng,
    target$cell_lat2,
    target$cell_lng
  )
  candidates <- candidates[order(candidates$distance_km,candidates$cell),]
  candidates <- candidates[!duplicated(candidates$cell),,drop=FALSE]
  if(nrow(candidates)<MAX_RANK) next

  m_n <- m_n+1L
  maps[[m_n]] <- data.frame(
    species=target$species,
    target_cell=target$cell,
    source_r1=candidates$cell[1],
    source_r2=candidates$cell[2],
    source_r3=candidates$cell[3],
    distance_r1=candidates$distance_km[1],
    distance_r2=candidates$distance_km[2],
    distance_r3=candidates$distance_km[3]
  )
}

rank_map <- do.call(rbind,maps[seq_len(m_n)])
if(is.null(rank_map) || nrow(rank_map)==0) stop("No rank mappings")

# Cross-validated environmental forecast value for a source-target pair.
pair_cv <- function(source_cell,target_cell,start_year,end_year){
  src <- green[
    green$cell==source_cell &
      green$year>=start_year &
      green$year<=end_year,
    c("year","gr_mn"),
    drop=FALSE
  ]
  tgt <- green[
    green$cell==target_cell &
      green$year>=start_year &
      green$year<=end_year,
    c("year","gr_mn"),
    drop=FALSE
  ]
  names(src)[2] <- "source_greenup"
  names(tgt)[2] <- "target_greenup"
  z <- merge(src,tgt,by="year",all=FALSE)
  z <- z[
    is.finite(z$year) &
      is.finite(z$source_greenup) &
      is.finite(z$target_greenup),
    ,
    drop=FALSE
  ]
  z <- z[!duplicated(z$year),,drop=FALSE]
  z <- z[order(z$year),,drop=FALSE]
  n <- nrow(z)
  if(n<MIN_PAIRS_PER_WINDOW){
    return(c(n=n,rho=NA_real_,value=NA_real_))
  }

  sf0 <- lm(source_greenup~year,data=z)
  tf0 <- lm(target_greenup~year,data=z)
  x0 <- resid(sf0)
  y0 <- resid(tf0)
  if(!is.finite(sd(x0)) || sd(x0)<=0 || !is.finite(sd(y0)) || sd(y0)<=0){
    return(c(n=n,rho=NA_real_,value=NA_real_))
  }

  err_src <- rep(NA_real_,n)
  err_null <- rep(NA_real_,n)
  for(j in seq_len(n)){
    tr <- z[-j,,drop=FALSE]
    te <- z[j,,drop=FALSE]
    sf <- lm(source_greenup~year,data=tr)
    tf <- lm(target_greenup~year,data=tr)
    xtr <- resid(sf)
    ytr <- resid(tf)
    if(!is.finite(sd(xtr)) || sd(xtr)<=0) next
    mod <- lm(ytr~xtr)

    sx <- as.numeric(predict(sf,newdata=te))
    ty <- as.numeric(predict(tf,newdata=te))
    xh <- te$source_greenup-sx
    pred_anom <- as.numeric(coef(mod)[1]+coef(mod)[2]*xh)
    pred_src <- ty+pred_anom

    err_src[j] <- te$target_greenup-pred_src
    err_null[j] <- te$target_greenup-ty
  }
  if(!all(is.finite(err_src)) || !all(is.finite(err_null))){
    value <- NA_real_
  }else{
    value <- mean(err_null^2)-mean(err_src^2)
  }

  c(n=n,rho=cor(x0,y0),value=value)
}

# Memoize by source-target-window.
memo <- new.env(parent=emptyenv())
get_cv <- function(source_cell,target_cell,start_year,end_year){
  key <- paste(source_cell,target_cell,start_year,end_year,sep="::")
  if(exists(key,envir=memo,inherits=FALSE)){
    return(get(key,envir=memo,inherits=FALSE))
  }
  val <- pair_cv(source_cell,target_cell,start_year,end_year)
  assign(key,val,envir=memo)
  val
}

# Calculate rank-specific values for every species-target row.
for(k in seq_len(MAX_RANK)){
  src_col <- paste0("source_r",k)

  e <- t(mapply(
    get_cv,
    rank_map[[src_col]],
    rank_map$target_cell,
    MoreArgs=list(start_year=EARLY_START,end_year=EARLY_END)
  ))
  l <- t(mapply(
    get_cv,
    rank_map[[src_col]],
    rank_map$target_cell,
    MoreArgs=list(start_year=LATE_START,end_year=LATE_END)
  ))

  rank_map[[paste0("n_early_r",k)]] <- as.integer(e[,"n"])
  rank_map[[paste0("n_late_r",k)]] <- as.integer(l[,"n"])
  rank_map[[paste0("rho_early_r",k)]] <- as.numeric(e[,"rho"])
  rank_map[[paste0("rho_late_r",k)]] <- as.numeric(l[,"rho"])
  rank_map[[paste0("delta_rho_r",k)]] <-
    rank_map[[paste0("rho_late_r",k)]] -
    rank_map[[paste0("rho_early_r",k)]]
  rank_map[[paste0("G_early_r",k)]] <- as.numeric(e[,"value"])
  rank_map[[paste0("G_late_r",k)]] <- as.numeric(l[,"value"])
  rank_map[[paste0("delta_G_r",k)]] <-
    rank_map[[paste0("G_late_r",k)]] -
    rank_map[[paste0("G_early_r",k)]]
}

# Common-target sample: all three ranks estimable in both windows.
common <- rep(TRUE,nrow(rank_map))
for(k in seq_len(MAX_RANK)){
  common <- common &
    rank_map[[paste0("n_early_r",k)]]>=MIN_PAIRS_PER_WINDOW &
    rank_map[[paste0("n_late_r",k)]]>=MIN_PAIRS_PER_WINDOW &
    is.finite(rank_map[[paste0("delta_G_r",k)]]) &
    is.finite(rank_map[[paste0("delta_rho_r",k)]])
}
common_map <- rank_map[common,,drop=FALSE]

if(nrow(common_map)<20) stop("Too few common rank-1/2/3 target rows")
if(length(unique(common_map$species))<5) stop("Too few common species")

# Rank summaries, both row mean and equal species.
summaries <- list()
for(k in seq_len(MAX_RANK)){
  dG <- common_map[[paste0("delta_G_r",k)]]
  dr <- common_map[[paste0("delta_rho_r",k)]]
  spG <- aggregate(
    common_map[[paste0("delta_G_r",k)]],
    list(species=common_map$species),
    mean
  )
  names(spG)[2] <- "value"
  spr <- aggregate(
    common_map[[paste0("delta_rho_r",k)]],
    list(species=common_map$species),
    mean
  )
  names(spr)[2] <- "value"

  summaries[[k]] <- data.frame(
    source_rank=k,
    n_species_target_rows=nrow(common_map),
    species=length(unique(common_map$species)),
    mean_distance_km=mean(common_map[[paste0("distance_r",k)]]),
    mean_delta_G=mean(dG),
    median_delta_G=median(dG),
    positive_delta_G=sum(dG>0),
    equal_species_delta_G=mean(spG$value),
    mean_delta_rho=mean(dr),
    equal_species_delta_rho=mean(spr$value)
  )
}
summary_df <- do.call(rbind,summaries)

# Paired rank-1 minus alternative-rank contrasts on same species-target rows.
paired <- data.frame(
  species=common_map$species,
  target_cell=common_map$target_cell,
  r1_minus_r2_G=common_map$delta_G_r1-common_map$delta_G_r2,
  r1_minus_r3_G=common_map$delta_G_r1-common_map$delta_G_r3,
  r1_minus_r2_rho=common_map$delta_rho_r1-common_map$delta_rho_r2,
  r1_minus_r3_rho=common_map$delta_rho_r1-common_map$delta_rho_r3
)

# Equal-species bootstrap by resampling species-target rows, carrying all
# paired rank values. This is descriptive and does not model spatial dependence.
set.seed(SEED)
boot <- data.frame(
  r1_minus_r2_G=rep(NA_real_,B),
  r1_minus_r3_G=rep(NA_real_,B)
)
N <- nrow(paired)
for(b in seq_len(B)){
  ix <- sample(seq_len(N),N,replace=TRUE)
  z <- paired[ix,,drop=FALSE]
  s2 <- aggregate(r1_minus_r2_G~species,data=z,FUN=mean)
  s3 <- aggregate(r1_minus_r3_G~species,data=z,FUN=mean)
  boot$r1_minus_r2_G[b] <- mean(s2$r1_minus_r2_G)
  boot$r1_minus_r3_G[b] <- mean(s3$r1_minus_r3_G)
}
ci <- function(x) as.numeric(quantile(x,c(.025,.975),names=FALSE))

paired_summary <- data.frame(
  common_rows=nrow(common_map),
  common_species=length(unique(common_map$species)),
  equal_species_r1_minus_r2_G=
    mean(aggregate(r1_minus_r2_G~species,data=paired,FUN=mean)$r1_minus_r2_G),
  r1_minus_r2_ci_low_95=ci(boot$r1_minus_r2_G)[1],
  r1_minus_r2_ci_high_95=ci(boot$r1_minus_r2_G)[2],
  equal_species_r1_minus_r3_G=
    mean(aggregate(r1_minus_r3_G~species,data=paired,FUN=mean)$r1_minus_r3_G),
  r1_minus_r3_ci_low_95=ci(boot$r1_minus_r3_G)[1],
  r1_minus_r3_ci_high_95=ci(boot$r1_minus_r3_G)[2]
)

dir.create("outputs",showWarnings=FALSE,recursive=TRUE)
write.csv(
  common_map,
  "outputs/payoff_b_v8_source_rank_common_rows.csv",
  row.names=FALSE
)
write.csv(
  summary_df,
  "outputs/payoff_b_v8_source_rank_summary.csv",
  row.names=FALSE
)
write.csv(
  paired,
  "outputs/payoff_b_v8_source_rank_paired.csv",
  row.names=FALSE
)
write.csv(
  paired_summary,
  "outputs/payoff_b_v8_source_rank_paired_summary.csv",
  row.names=FALSE
)
write.csv(
  boot,
  "outputs/payoff_b_v8_source_rank_bootstrap.csv",
  row.names=FALSE
)

cat("\nPOSTHOC SOURCE-RANK SENSITIVITY\n")
print(summary_df)
print(paired_summary)
