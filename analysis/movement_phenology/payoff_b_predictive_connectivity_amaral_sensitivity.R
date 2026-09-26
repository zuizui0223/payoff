#!/usr/bin/env Rscript

options(stringsAsFactors = FALSE)

SOURCE_COMMIT <- "62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
SOURCE_URL <- paste0(
  "https://raw.githubusercontent.com/br-amaral/BirdMigrationSpeed/",
  SOURCE_COMMIT,
  "/data/final.rds"
)
MIN_PAIRS <- 6L

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
cache <- "outputs/amaral_final_frozen.rds"
if (!file.exists(cache)) {
  download.file(SOURCE_URL, cache, mode = "wb", quiet = FALSE)
}
dat <- readRDS(cache)

required <- c(
  "species", "year", "cell", "cell_lat2", "cell_lng",
  "arr_GAM_mean", "gr_mn", "vArrMag", "AnomDGr",
  "mig_cell", "breed_cell"
)
missing <- setdiff(required, names(dat))
if (length(missing) > 0) stop("Missing: ", paste(missing, collapse=", "))

truthy <- function(x) toupper(as.character(x)) %in% c("TRUE","T","1")
haversine_km <- function(lat1, lon1, lat2, lon2) {
  rad <- pi / 180
  p1 <- lat1 * rad
  p2 <- lat2 * rad
  dp <- (lat2-lat1) * rad
  dl <- (lon2-lon1) * rad
  a <- sin(dp/2)^2 + cos(p1)*cos(p2)*sin(dl/2)^2
  6371.0088 * 2 * atan2(sqrt(a), sqrt(pmax(0,1-a)))
}
rho_value <- function(year, origin, destination, detrend=TRUE) {
  keep <- is.finite(year) & is.finite(origin) & is.finite(destination)
  year <- year[keep]; origin <- origin[keep]; destination <- destination[keep]
  if (length(year) < MIN_PAIRS) return(NA_real_)
  if (detrend) {
    origin <- resid(lm(origin ~ year))
    destination <- resid(lm(destination ~ year))
  }
  if (sd(origin) <= 0 || sd(destination) <= 0) return(NA_real_)
  cor(origin, destination)
}

cells <- unique(dat[,c("species","cell","cell_lat2","cell_lng","mig_cell","breed_cell")])
cells$cell <- as.numeric(as.character(cells$cell))
cells$cell_lat2 <- as.numeric(cells$cell_lat2)
cells$cell_lng <- as.numeric(cells$cell_lng)
cells$is_mig <- truthy(cells$mig_cell)
cells$is_breed <- truthy(cells$breed_cell)

targets <- cells[cells$is_breed,c("species","cell","cell_lat2","cell_lng")]
targets <- targets[order(targets$species,targets$cell),]
mapping <- list()
for (i in seq_len(nrow(targets))) {
  target <- targets[i,]
  candidates <- cells[
    cells$species == target$species &
      cells$is_mig &
      is.finite(cells$cell_lat2) &
      cells$cell_lat2 < target$cell_lat2,
    c("cell","cell_lat2","cell_lng")
  ]
  if (nrow(candidates) == 0) next
  candidates$distance_km <- haversine_km(
    candidates$cell_lat2,candidates$cell_lng,target$cell_lat2,target$cell_lng
  )
  candidates <- candidates[order(candidates$distance_km,candidates$cell),]
  source <- candidates[1,]
  mapping[[length(mapping)+1L]] <- data.frame(
    species=target$species,target_cell=target$cell,source_cell=source$cell
  )
}
mapping <- do.call(rbind,mapping)

green <- unique(dat[,c("year","cell","gr_mn")])
green$year <- as.integer(green$year)
green$cell <- as.numeric(as.character(green$cell))
green$gr_mn <- as.numeric(green$gr_mn)
green <- green[is.finite(green$gr_mn),]

outcome <- dat[
  truthy(dat$breed_cell) &
    is.finite(as.numeric(dat$arr_GAM_mean)) &
    is.finite(as.numeric(dat$gr_mn)) &
    is.finite(as.numeric(dat$vArrMag)) &
    as.numeric(dat$vArrMag) > 0 &
    is.finite(as.numeric(dat$AnomDGr)),
]
outcome$year <- as.integer(outcome$year)
outcome$cell <- as.numeric(as.character(outcome$cell))
outcome$arr_GAM_mean <- as.numeric(outcome$arr_GAM_mean)
outcome$gr_mn <- as.numeric(outcome$gr_mn)
outcome$vArrMag <- as.numeric(outcome$vArrMag)
outcome$AnomDGr <- as.numeric(outcome$AnomDGr)
outcome <- merge(
  outcome,mapping,
  by.x=c("species","cell"),
  by.y=c("species","target_cell"),
  all=FALSE
)

if (!requireNamespace("mgcv", quietly=TRUE)) stop("mgcv required")

run_setting <- function(window_years, detrend, transform_q=FALSE) {
  connectivity <- rep(NA_real_,nrow(outcome))
  for (i in seq_len(nrow(outcome))) {
    yr <- outcome$year[i]
    source <- green[
      green$cell == outcome$source_cell[i] &
        green$year >= yr-window_years & green$year < yr,
      c("year","gr_mn")
    ]
    target <- green[
      green$cell == outcome$cell[i] &
        green$year >= yr-window_years & green$year < yr,
      c("year","gr_mn")
    ]
    names(source)[2] <- "origin"; names(target)[2] <- "destination"
    paired <- merge(source,target,by="year",all=FALSE)
    if (nrow(paired) >= MIN_PAIRS) {
      connectivity[i] <- rho_value(
        paired$year,paired$origin,paired$destination,detrend=detrend
      )
    }
  }

  use <- outcome[is.finite(connectivity) & outcome$year >= 2010,]
  use$connectivity <- connectivity[is.finite(connectivity) & outcome$year >= 2010]
  if (transform_q) {
    use$connectivity <- 0.5 + asin(pmax(-1,pmin(1,use$connectivity)))/pi
  }
  use$primary_response <- log1p(abs(use$gr_mn-use$arr_GAM_mean))
  use$z_connectivity <- as.numeric(scale(use$connectivity))
  use$z_destination_greenup_anomaly <- as.numeric(scale(use$AnomDGr))
  use$z_bird_speed <- as.numeric(scale(log(use$vArrMag)))
  use$species <- factor(use$species)
  use$species_cell <- factor(paste(use$species,use$cell,sep="_"))
  use$year_factor <- factor(use$year)

  fit <- mgcv::gam(
    primary_response ~ z_connectivity +
      z_destination_greenup_anomaly + z_bird_speed +
      s(year_factor,bs="re") +
      s(species_cell,bs="re") +
      s(species,bs="re"),
    data=use,method="REML"
  )
  tab <- summary(fit)$p.table
  est <- unname(tab["z_connectivity","Estimate"])
  se <- unname(tab["z_connectivity","Std. Error"])
  data.frame(
    window_years=window_years,
    detrended=detrend,
    gaussian_q=transform_q,
    analysis_rows=nrow(use),
    species=length(unique(use$species)),
    coefficient=est,
    standard_error=se,
    ci_low_95=est-1.96*se,
    ci_high_95=est+1.96*se,
    p_value_two_sided=unname(tab["z_connectivity","Pr(>|t|)"]),
    direction_negative=est<0,
    ci_excludes_zero_negative=(est+1.96*se)<0
  )
}

settings <- list(
  c(6,1,0),
  c(8,1,0),
  c(10,1,0),
  c(8,0,0),
  c(8,1,1)
)

results <- do.call(rbind,lapply(settings,function(s) {
  run_setting(as.integer(s[1]),as.logical(s[2]),as.logical(s[3]))
}))
write.csv(
  results,
  "outputs/payoff_b_broad_predictive_connectivity_sensitivity.csv",
  row.names=FALSE
)
print(results)
