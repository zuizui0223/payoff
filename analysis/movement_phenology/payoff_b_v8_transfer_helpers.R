metric_pair_boot <- function(d, B = 10000L, seed = 20261005L) {
  keys <- unique(as.character(d$pair_key))
  by_pair <- split(d[, c("species","delta_mismatch"), drop=FALSE], d$pair_key)
  set.seed(seed)
  br <- bs <- numeric(B)
  for (b in seq_len(B)) {
    ks <- sample(keys, length(keys), replace=TRUE)
    z <- do.call(rbind, lapply(seq_along(ks), function(i) {
      x <- by_pair[[ks[i]]]; x$draw <- i; x
    }))
    br[b] <- mean(z$delta_mismatch)
    sm <- aggregate(delta_mismatch ~ species, z, mean)
    bs[b] <- mean(sm$delta_mismatch)
  }
  list(
    row_mean=mean(d$delta_mismatch),
    species_mean=mean(aggregate(delta_mismatch ~ species, d, mean)$delta_mismatch),
    row_ci=unname(quantile(br,c(.025,.975))),
    species_ci=unname(quantile(bs,c(.025,.975))),
    row_boot=br, species_boot=bs
  )
}

cluster_term <- function(fit, d, term) {
  V <- sandwich::vcovCL(
    fit,
    cluster=data.frame(species=d$species, pair_key=d$pair_key),
    type="HC1",
    cadjust=TRUE
  )
  b <- unname(coef(fit)[term])
  se <- sqrt(V[term,term])
  df <- min(length(unique(d$species)), length(unique(d$pair_key))) - 1L
  q <- qt(.975,df)
  c(estimate=b,se=se,low=b-q*se,high=b+q*se,df=df)
}
