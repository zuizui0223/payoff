# Greater snow goose route-geometry public source screen

Date: **2026-09-30**  
Status: **public source screen exhausted; primary exact geometry still unavailable**

## Question

Can the three route-context polygons required by the frozen greater-snow-goose
GPS analysis be recovered exactly from public sources without using focal GPS,
climate outcomes or hand-drawn post hoc boundaries?

## Source result

Reséndiz-Infante & Gauthier (2024) describe how the route regions were created.

- The St. Lawrence Valley was delimited from eBird plus prior scientific
  studies and treated as one spring stopover.
- Nunavik and Baffin were delimited from satellite locations of 54 birds,
  aerial surveys and literature.
- Arctic polygons were defined around places where groups of tracked geese
  stayed more than two days.
- The three stopover polygons were subsequently refined using vegetation and
  elevation layers from Natural Resources Canada.
- The Bylot target was the south plain breeding colony.

The article therefore documents the **construction logic**, but not the exact
polygon vertices.

The article's data-availability statement says that original contributions are
included in the article/Supplementary Material and directs further inquiries to
the corresponding author. The public Supplementary Material located in this
screen contains migration-timing/analysis material but no exact GIS object for
the three stopover polygons.

Figure 1 publicly displays the three route regions, but it is a raster figure,
not the source GIS object.

## Frozen consequence

The primary geometry gate is now classified as:

```text
PUBLIC_SOURCE_SCREEN_EXHAUSTED_EXACT_SOURCE_POLYGONS_NOT_RELEASED
```

This is an **external source-availability state**, not a scientific result.

The primary cue-uptake / dual-use outcome must remain unopened until one of the
following becomes available:

1. the exact polygons used by the 2024 study;
2. an exact source-backed release of equivalent geometries from the study
   authors/source archive.

The following remain forbidden as primary geometry:

- hand-drawn polygons;
- approximate bounding boxes;
- polygons fitted to focal GPS points;
- climate-informed region tuning;
- Figure 1 raster digitization.

## Figure 1 sensitivity

The existing frozen sensitivity protocol remains valid:

1. georeference the highest-resolution Figure 1 raster using only
   graticules/coastline;
2. trace all three regions twice independently with focal GPS/outcomes absent;
3. require Jaccard >= 0.90 for every region;
4. evaluate trace A, trace B, intersection core and union envelope.

Passing that procedure would create a **measurement-error sensitivity only**.
It cannot promote the Figure-derived polygons to the primary analysis.

## Why not reconstruct from NARR results?

The paper extracted NARR temperatures over the route regions, but published
regional temperature summaries/correlations do not uniquely identify which
32-km cells comprised the original polygons. Reverse-engineering a boundary
from those outcomes would also make the geometry climate-informed, violating
the frozen context contract.

## Operational conclusion

The route semantics are scientifically clear; the exact primary GIS object is
not publicly materialized.

Therefore the snow-goose programme can continue with:

- theory;
- registration and executor testing;
- access/materialization tooling;
- Figure 1 sensitivity preparation;

but **not the focal GPS coefficient or threshold outcome**.

This converts a vague geometry blocker into a documented external dependency
and prevents future post-outcome boundary reconstruction.
