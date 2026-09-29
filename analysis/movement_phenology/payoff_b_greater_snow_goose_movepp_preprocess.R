#!/usr/bin/env Rscript

# Frozen preprocessing for PAYOFF-B greater snow goose cue-uptake analysis.
#
# Input: Movebank-format GPS CSV for study 1442516400.
# Output:
#   1) automatic movepp staging habitats with shared south/mid/north context
#   2) individual x context-visit x day-at-risk skeleton
#
# No climate variable is read by this script.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3L) {
  stop(
    "usage: Rscript payoff_b_greater_snow_goose_movepp_preprocess.R ",
    "<raw_movebank.csv> <staging_contexts.csv> <day_risk.csv>"
  )
}
raw_path <- args[[1]]
contexts_path <- args[[2]]
risk_path <- args[[3]]

suppressPackageStartupMessages({
  library(movepp)
  library(sf)
})

pick_col <- function(nm, candidates) {
  hit <- candidates[candidates %in% nm]
  if (!length(hit)) return(NA_character_)
  hit[[1]]
}

raw <- read.csv(raw_path, stringsAsFactors = FALSE, check.names = FALSE)
nm <- names(raw)

id_col <- pick_col(nm, c(
  "individual_local_identifier",
  "individual-local-identifier",
  "individual_id",
  "individual-id"
))
time_col <- pick_col(nm, c("timestamp", "time"))
lon_col <- pick_col(nm, c("location_long", "location-long", "lon", "longitude"))
lat_col <- pick_col(nm, c("location_lat", "location-lat", "lat", "latitude"))
if (any(is.na(c(id_col, time_col, lon_col, lat_col)))) {
  stop("raw Movebank columns do not contain required id/time/lon/lat fields")
}

if ("visible" %in% nm) {
  keep_visible <- toupper(as.character(raw$visible)) %in% c("TRUE", "T", "1", "")
  raw <- raw[is.na(raw$visible) | keep_visible, , drop = FALSE]
}

dat <- data.frame(
  individual = as.character(raw[[id_col]]),
  time = as.POSIXct(raw[[time_col]], tz = "UTC"),
  lon = as.numeric(raw[[lon_col]]),
  lat = as.numeric(raw[[lat_col]]),
  stringsAsFactors = FALSE
)
dat <- dat[
  is.finite(dat$lon) & is.finite(dat$lat) &
  !is.na(dat$time) & nzchar(dat$individual),
  ,
  drop = FALSE
]
dat <- dat[order(dat$individual, dat$time), , drop = FALSE]
if (nrow(dat) < 1000L) stop("too few valid GPS fixes")

track <- st_as_sf(
  dat,
  coords = c("lon", "lat"),
  crs = 4326,
  remove = FALSE
)

# Frozen movepp chain.
g <- compute_step_speed(
  track,
  time_col = "time",
  individual_col = "individual",
  direction = "centered"
)
seg <- balm_segmentation(
  g,
  variable_col = "step_speed",
  individual_col = "individual",
  verbose = FALSE
)
stationary <- seg[
  !is.na(seg$cluster_type) & seg$cluster_type %in% c("LL", "LH"),
]
if (nrow(stationary) < 100L) stop("too few stationary/transient fixes")

hp <- detect_habitat_params(
  stationary,
  track = seg,
  individual_col = "individual",
  time_col = "time"
)
hab <- dbscan_habitats(
  stationary,
  individual_col = "individual",
  eps = hp$eps,
  minPts = hp$minPts
)
mpi <- compute_mpi(
  hab,
  individual_col = "individual",
  time_col = "time",
  verbose = FALSE
)
phs <- classify_phases(
  mpi,
  n_phases = 3,
  individual_col = "individual",
  fixed_stopover = "LH",
  phase_names = c("Wintering", "staging_stopover", "Breeding"),
  verbose = FALSE
)

if (!"staging_stopover" %in% as.character(unique(phs$phase))) {
  stop("automatic movepp classification did not resolve staging_stopover")
}
if (!"Breeding" %in% as.character(unique(phs$phase))) {
  stop("automatic movepp classification did not resolve Breeding")
}

# Fixed Bylot target coordinate from movement geometry only: median location
# of automatically classified Breeding points during 30 May-15 Jun.
all_date <- as.Date(phs$time, tz = "UTC")
all_year <- as.integer(format(all_date, "%Y"))
breed_start <- as.Date(sprintf("%04d-05-30", all_year))
breed_end <- as.Date(sprintf("%04d-06-15", all_year))
breed_target <- (
  as.character(phs$phase) == "Breeding" &
  all_date >= breed_start & all_date <= breed_end
)
breed_pts <- phs[breed_target, ]
if (nrow(breed_pts) < 20L) {
  stop("too few automatic Breeding points in frozen Bylot target window")
}
breed_co <- st_coordinates(breed_pts)
target_bylot_lon <- median(breed_co[, 1], na.rm = TRUE)
target_bylot_lat <- median(breed_co[, 2], na.rm = TRUE)

# Frozen spring window: 01 Apr through 15 Jun UTC.
pdate <- as.Date(phs$time, tz = "UTC")
pyear <- as.integer(format(pdate, "%Y"))
start <- as.Date(sprintf("%04d-04-01", pyear))
end <- as.Date(sprintf("%04d-06-15", pyear))
spring <- (
  as.character(phs$phase) == "staging_stopover" &
  pdate >= start & pdate <= end
)
stg <- phs[spring, ]
if (!nrow(stg)) stop("no spring staging_stopover fixes")

# Habitat summaries are individual-year specific even when a spatial DBSCAN
# cluster is revisited across years.
co <- st_coordinates(stg)
sdf <- st_drop_geometry(stg)
sdf$lon <- co[, 1]
sdf$lat <- co[, 2]
sdf$year <- as.integer(format(as.Date(sdf$time, tz = "UTC"), "%Y"))

key <- interaction(
  sdf$individual,
  sdf$year,
  sdf$cluster_id,
  drop = TRUE,
  lex.order = TRUE
)
split_rows <- split(seq_len(nrow(sdf)), key)
hab_rows <- lapply(split_rows, function(ii) {
  z <- sdf[ii, , drop = FALSE]
  data.frame(
    individual_id = as.character(z$individual[[1]]),
    year = as.integer(z$year[[1]]),
    cluster_id = as.integer(z$cluster_id[[1]]),
    centroid_lon = mean(z$lon, na.rm = TRUE),
    centroid_lat = mean(z$lat, na.rm = TRUE),
    first_time = format(min(z$time), tz = "UTC", usetz = TRUE),
    last_time = format(max(z$time), tz = "UTC", usetz = TRUE),
    n_staging_fixes = nrow(z),
    stringsAsFactors = FALSE
  )
})
habitats <- do.call(rbind, hab_rows)
if (nrow(habitats) < 3L) stop("fewer than three spring staging habitats")

# Shared route contexts: fixed k=3 on habitat-centroid latitude only.
# This is movement-geometry-only and is performed before any climate/q join.
set.seed(1L)
km <- kmeans(
  matrix(habitats$centroid_lat, ncol = 1L),
  centers = 3L,
  nstart = 100L
)
centers <- as.numeric(km$centers[, 1])
ord <- order(centers)
label_by_cluster <- rep(NA_character_, 3L)
label_by_cluster[ord] <- c(
  "southern_staging",
  "mid_arctic_staging",
  "northern_arctic_staging"
)
habitats$context <- label_by_cluster[km$cluster]

if (length(unique(habitats$context)) != 3L) {
  stop("shared route-context mapping did not produce three contexts")
}
habitats$target_bylot_lon <- target_bylot_lon
habitats$target_bylot_lat <- target_bylot_lat

# Map habitat summaries back to point rows for occupancy-bout construction.
map_key <- paste(
  habitats$individual_id,
  habitats$year,
  habitats$cluster_id,
  sep = "::"
)
context_lookup <- setNames(habitats$context, map_key)
centroid_lat_lookup <- setNames(habitats$centroid_lat, map_key)
centroid_lon_lookup <- setNames(habitats$centroid_lon, map_key)

skey <- paste(sdf$individual, sdf$year, sdf$cluster_id, sep = "::")
sdf$context <- unname(context_lookup[skey])
sdf$centroid_lat <- unname(centroid_lat_lookup[skey])
sdf$centroid_lon <- unname(centroid_lon_lookup[skey])

haversine_km <- function(lon1, lat1, lon2, lat2) {
  rr <- pi / 180
  a <- sin((lat2-lat1)*rr/2)^2 +
    cos(lat1*rr)*cos(lat2*rr)*sin((lon2-lon1)*rr/2)^2
  6371.0088 * 2 * atan2(sqrt(a), sqrt(pmax(0, 1-a)))
}

# Full segmented track as plain data for verifying outward movement after a
# habitat bout.
segco <- st_coordinates(seg)
segdf <- st_drop_geometry(seg)
segdf$lon <- segco[, 1]
segdf$lat <- segco[, 2]
segdf <- segdf[order(segdf$individual, segdf$time), , drop = FALSE]

# A visit/bout is split when stationary points in the same habitat are
# separated by >48 h.  Only bouts with observable outward movement are retained.
risk_rows <- list()
rrn <- 0L

for (hk in unique(skey)) {
  z <- sdf[skey == hk, , drop = FALSE]
  z <- z[order(z$time), , drop = FALSE]
  if (!nrow(z)) next

  gap_h <- c(Inf, as.numeric(diff(z$time), units = "hours"))
  z$bout <- cumsum(gap_h > 48)

  for (bout_id in unique(z$bout)) {
    b <- z[z$bout == bout_id, , drop = FALSE]
    t0 <- min(b$time)
    t1 <- max(b$time)

    full <- segdf[
      segdf$individual == b$individual[[1]] &
      segdf$time > t1,
      ,
      drop = FALSE
    ]
    if (!nrow(full)) next

    next_fix <- full[1, , drop = FALSE]
    hours_to_next <- as.numeric(
      difftime(next_fix$time[[1]], t1, units = "hours")
    )
    if (!is.finite(hours_to_next) || hours_to_next > 24) next

    dist_next <- haversine_km(
      b$centroid_lon[[1]],
      b$centroid_lat[[1]],
      next_fix$lon[[1]],
      next_fix$lat[[1]]
    )
    outward <- (
      isTRUE(next_fix$cluster_type[[1]] == "HH") ||
      (is.finite(dist_next) && dist_next > as.numeric(hp$eps))
    )
    if (!outward) next

    # The bout split itself guarantees no same-habitat stationary return for
    # 48 h.  If a later bout begins <=48 h, it would not have been split.
    d0 <- as.Date(t0, tz = "UTC")
    d1 <- as.Date(t1, tz = "UTC")
    days <- seq(d0, d1, by = "day")
    if (!length(days)) next

    rrn <- rrn + 1L
    risk_rows[[rrn]] <- data.frame(
      individual_id = as.character(b$individual[[1]]),
      year = as.integer(b$year[[1]]),
      context = as.character(b$context[[1]]),
      cluster_id = as.integer(b$cluster_id[[1]]),
      visit_id = paste(
        b$individual[[1]], b$year[[1]], b$cluster_id[[1]], bout_id,
        sep = "::"
      ),
      date = as.character(days),
      calendar_doy = as.integer(format(days, "%j")),
      depart_next_24h = as.integer(days == max(days)),
      centroid_lon = as.numeric(b$centroid_lon[[1]]),
      centroid_lat = as.numeric(b$centroid_lat[[1]]),
      stringsAsFactors = FALSE
    )
  }
}

if (!length(risk_rows)) stop("no uncensored spring staging bouts")
risk <- do.call(rbind, risk_rows)

# Seasonal progression control: calendar day-of-year centered within the
# shared route context.  This is intentionally not "days since arrival".
ctx_mean_doy <- tapply(risk$calendar_doy, risk$context, mean)
risk$day_of_year_within_context <- (
  risk$calendar_doy - unname(ctx_mean_doy[risk$context])
)

dir.create(dirname(contexts_path), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(risk_path), recursive = TRUE, showWarnings = FALSE)
write.csv(habitats, contexts_path, row.names = FALSE)
write.csv(risk, risk_path, row.names = FALSE)

cat("PAYOFF-B greater snow goose movepp preprocessing\n")
cat("fixes:", nrow(track), "\n")
cat("automatic staging habitats:", nrow(habitats), "\n")
cat("contexts:", paste(sort(unique(habitats$context)), collapse = ", "), "\n")
cat("day-risk rows:", nrow(risk), "\n")
cat("departure events:", sum(risk$depart_next_24h), "\n")
cat("movepp eps_km:", as.numeric(hp$eps), "\n")
cat("movepp minPts:", as.integer(hp$minPts), "\n")
