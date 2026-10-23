# PAYOFF-B experimental shearwater sensor-dependent observation gate

2026-10-23. Original public CC0 Calonectris diomedea (Pollonara et al. 2015,
DOI 10.5441/001/1.tc76g560) contains 32 reference subjects: control 9,
magnetically disrupted 9, olfactory deprived 14. Original GPS connects to
8, 9 and 6 subjects, respectively. Five additional Argos subject labels are
only in the olfactory-deprived arm in original 147 valid Argos locations.

This analysis checks whether original modality selection is dependent on
experimental treatment, which could bias naive comparisons of continuous
route efficiency or correction timing. GPS and Argos must NOT be pooled
as equivalent tracking records, and labels for the same animals must not
be double counted.

All original GPS/Argos/README/reference files are downloaded after exact
published MD5 and byte-length check; original bird, site and release
identifiers are held only in transient runner memory. Compute observed
source animals per treatment, whether the same bird appears in both
sensor streams, 10-fix minimum and continuous 24h sampled trajectory
segments defined with no adjacent gap greater than 6h. A fixed gate
requires at least 5 GPS subjects per treatment with a 24h contiguous
segment for a later stage-by-stage source geometry audit. Failure is not
fixed by including Argos as if it had GPS resolution.

This is published-source measurement QA, not a new experiment, causal
olfactory rescue claim, homeward route decision, migration phenology or
fitness effect. The original publication has already analysed the
olfaction/topography result, initial orientation, route efficiency and
coastal decision points. A novel PAYOFF-B mechanism must be specified
separately and checked on an untouched cohort, not relabel those published
effects as discovery.
