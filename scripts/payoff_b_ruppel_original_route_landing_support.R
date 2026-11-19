#!/usr/bin/env Rscript
# Original Rüppel 2023 route × landing support, no effect model.
# The ZIP is verified byte-for-byte against the original Figshare SHA by CI.
# Output ONLY aggregated year/species/route/landing counts; no original IDs,
# timestamps, coordinates or weather values.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) {
  stop("Usage: Rscript original_verified.zip output_group_counts.csv")
}
original <- args[1]
outpath <- args[2]
member <- "flights.RData"
if (!(member %in% utils::unzip(original,list=TRUE)$Name))
  stop("Published flights.RData member absent")
folder <- tempfile("payoff_b_original_2023_route_")
dir.create(folder)
on.exit(unlink(folder,recursive=TRUE),add=TRUE)
utils::unzip(original,files=member,exdir=folder)
e <- new.env(parent=baseenv())
loaded <- load(file.path(folder,member),envir=e)
if (!("flights" %in% loaded) || !is.data.frame(e$flights))
  stop("Original RData flights object is not an original source dataframe")
fl <- e$flights
needed <- c("motusTagID","speciesEN","year","flightCat","landing",
            "flightStart","flightEnd","u_start","v_start","c_start",
            "u_end","v_end","c_end")
if (!all(needed %in% names(fl)) || nrow(fl)!=178L)
  stop("Original flights row count/required source columns drifted")
route <- as.character(fl$flightCat)
if (anyNA(route) || !all(route %in% c("coasting","sea-crossing")))
  stop("Unexpected original author route categories")
land <- suppressWarnings(as.numeric(fl$landing))
if (anyNA(land) || !all(land %in% c(0,1)))
  stop("Original observed landing field is not 0/1 complete")
if (sum(route=="coasting")!=154L || sum(route=="sea-crossing")!=24L ||
    sum(land==1)!=24L || sum(land==0)!=154L)
  stop("Published original marginal route/landing counts changed")
years <- as.character(fl$year)
species <- as.character(fl$speciesEN)
if (anyNA(years) || anyNA(species) || length(unique(species))!=3L ||
    length(unique(years))!=3L || !all(unique(years) %in% c("2019","2020","2021")))
  stop("Original three-taxon 2019-2021 sampling support drift")
if (anyNA(fl$flightStart) || anyNA(fl$flightEnd) ||
    any(fl$flightStart>=fl$flightEnd))
  stop("Original flight start/end time ordering unverified")
for (field in c("u_start","v_start","c_start","u_end","v_end","c_end")) {
  if (anyNA(fl[[field]])) stop("Original weather start/end field incomplete")
}
if (anyDuplicated(as.character(fl$motusTagID))!=0L)
  stop("First-flight source is no longer one record per individual")

# Retain all zeros explicitly, especially small/sparse cells. No smoothing.
full <- expand.grid(
  species=sort(unique(species)),
  year=sort(unique(years)),
  route=c("coasting","sea-crossing"),
  landing=c(0L,1L),
  stringsAsFactors=FALSE
)
# Same source one bird → one flight; these are original flight counts only.
counts <- table(
  factor(species,levels=sort(unique(species))),
  factor(years,levels=sort(unique(years))),
  factor(route,levels=c("coasting","sea-crossing")),
  factor(land,levels=c(0L,1L))
)
full$count <- as.integer(counts)
full <- full[,c("species","year","route","landing","count")]
if (nrow(full)!=3L*3L*2L*2L || sum(full$count)!=178L)
  stop("Original flight cross-tab reconstruction failed")
dir.create(dirname(outpath),recursive=TRUE,showWarnings=FALSE)
utils::write.csv(full,outpath,row.names=FALSE,na="")
cat(sprintf("ORIGINAL_ROUTE_LANDING_SUPPORT original_flights=%d species=%d years=%d source_landing=%d\n",
            sum(full$count),length(unique(species)),length(unique(years)),
            sum(full$count[full$landing==1L])))
cat("ORIGINAL_LANDING_BY_ROUTE ",
    paste(sprintf("%s:%d/%d",
                  c("coasting","sea-crossing"),
                  c(sum(land==1&route=="coasting"),
                    sum(land==1&route=="sea-crossing")),
                  c(sum(land==0&route=="coasting"),
                    sum(land==0&route=="sea-crossing"))),collapse=";"),
    "\n",sep="")
