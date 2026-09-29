# Greater snow goose Figure 1 geometry recovery protocol

Date: **2026-09-29**  
Status: **pre-outcome sensitivity protocol; not primary geometry**

The focal GPS cue-uptake analysis remains blocked until the exact stopover
polygons used by Reséndiz-Infante & Gauthier (2024), or an exact source release
of those geometries, can be materialized.

The published paper nevertheless contains Figure 1, which maps the St. Lawrence,
Nunavik and Baffin staging regions. The paper states that these polygons were
built from tracking, survey and literature evidence and refined using vegetation
and elevation layers. It does not publish the underlying GIS vertices.

A raster trace of Figure 1 is therefore a **measurement-error sensitivity**, not
a substitute for the primary geometry.

## Frozen recovery procedure

1. Obtain the highest-resolution publisher raster of Figure 1.
2. Georeference it from visible graticule/coastline control points only.
3. Trace the three staging regions twice, independently and without GPS,
   predictive-connectivity values or model outcomes loaded.
4. Rasterize each trace to the native NARR grid.
5. Require Jaccard agreement >= 0.90 for every region before any sensitivity
   analysis is opened.
6. If the gate passes, evaluate four fixed geometry variants: trace A, trace B,
   their intersection core and their union envelope.

No variant may replace the source-polygon primary analysis. The point is to ask
whether any future behavioral result depends materially on plausible map
digitization error.

## Why this is necessary

The paper explicitly describes Arctic stopover regions as coarsely delimited
from tracked birds, aerial surveys and literature, then refined by habitat
layers. A visually reconstructed boundary cannot be treated as the original
GIS object.

This protocol preserves that distinction while ensuring that lack of a released
shapefile does not become an excuse for post-outcome hand drawing.
