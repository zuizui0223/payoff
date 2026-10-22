# PAYOFF-B: manipulated shearwater cue and telemetry source admission

2026-10-23. The frozen independent-taxon Movebank 446-package screening
includes public CC0 source 10.5441/001/1.tc76g560 (Calonectris diomedea).
This was selected after the earlier three-bird held-out-year physical-weather
prediction did not consistently improve over season and geography.

Unlike those purely observational source weather records, the original
Pollonara et al. 2015 experiment displaced Scopoli's shearwaters roughly
400 km and manipulated sensory access, comparing olfactory, magnetic and
control treatments. THIS EXPERIMENT AND ITS ORIGINAL NAVIGATION RESULTS ARE
PRIOR ART (paper DOI 10.1038/srep16486); a source readout is not an
independent novel PAYOFF-B confirmation.

The ORIGINAL CC0 Movebank source supplies:
- GPS 4,420,051 bytes, MD5 35679733d880e26a17ddd7c51b5637eb;
- Argos 44,019 bytes, MD5 7826b6457846cc9d6a1bb81dee65ca1f;
- reference 9,867 bytes, MD5 20a038104c926229690a8bcd11c365db;
- README 16,541 bytes, MD5 d45da171ce1445cb9a80f984c0050073.

Publisher reference has 32 deployment rows, with 9 controls, 9 magnetic
disruption subjects and 14 smell-deprived subjects. The original publisher
spells the latter source manipulation-comments as 'asnomic', NOT the common
'anosmic'. This alias is explicitly included in the SOURCE-ONLY arm mapping;
neither unknown treatments nor missing manipulation comments are silently
counted as controls.

Before calculating any ecological or game-theoretic effect, strictly
verify file bytes/MD5 and the original reference animal/tag-to-group join
to both GPS and Argos. Preserve original sensor-specific completeness and
observation gaps. Source gate: all three manipulated/control groups must
have valid GPS data, at least 12 registered original tracked animals, and
at least one track with 10+ valid events per arm; failing data are explicitly
NOT ADMITTED. Do not sum GPS and Argos animals as independent subjects.

Interpretation boundary: treatment assignment metadata alone does not
prove randomization or treatment efficacy. The original paper already
tested olfactory, visual-landmark and magnetic navigation. A NEW PAYOFF-B
experiment would need an independently registered question about remaining
feasible correction, actual cue availability before a course change, route
geometry, comparison to untreated controls, and held-out animals. The 2015
experiment is not a phenological departure/fitness test by itself.

Source data and nesting coordinates stay on transient CI storage; reports
contain only group-level source coverage and limits. No individual animals,
positions, exact release times or per-bird trajectories in artifacts.
