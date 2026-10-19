# PAYOFF-B Movebank — GBIF taxonomic source gate

2026-10-19. **Metadata-only, all 446 source packages; not an ecological effect test.**

Inputs are SHA256-pinned original DataCite child file metadata (831 child DOI
records; GitHub workflow 39204043835) and official Movebank DSpace parent
registry (446 parent packages, 444 parsed; workflow 39211112610).
Only taxonomic names are looked up using the public GBIF Backbone
species-match API. Accept a class only for EXACT species/subspecies matches
with >=90 confidence; ambiguous/unavailable names remain unresolved.

The archive's GPS sensor field alone misses some published GPS files:
Rotics et al. (2018) stork package lists Acceleration in the DSpace item
although its published child file has a GPS name and actual validated GPS
records. Therefore child-file GPS hints and sensor metadata are recorded as
two separate measurements. File names remain *hints* until content is read.

Do not treat published package counts, taxonomic names, archived locations,
shared papers or study IDs as independent biological replicates.
No animal route, decision-time environmental cue, behavioral correction,
survival or reproduction is estimated by this pipeline.

- GBIF species match: https://api.gbif.org/v1/species/match
- GBIF Backbone: https://doi.org/10.15468/39omei
