# OSM data exploration

Compare the BikeNodePlanner loop networks (BNN) with OpenStreetMap (OSM) cycling networks, including spatial overlap, lighting, and surface information.

You have to have run all notebooks in from the folder `bikenwloops` to generate the BNN inputs before notebooks in this folder can be run.

## Contents

- **`one_region_analysis.ipynb`** — Analyse one region selected with `SAMPLE`. Includes overlap plots, surface percentages by length, interactive surface maps with topographic/satellite backgrounds, and optional imputation of short missing or unmatched surface segments where both neighbours agree.
- **`all_regions_analysis.ipynb`** — Earlier analysis organised into separate sections for all six regions, covering network overlap, lighting, and surfaces.
- **`network_plotting.py`** — Shared plotting functions imported by the single-region notebook.
- **`requirements.txt`** — Recorded Python dependency versions. The current single-region notebook's spatial-index `dwithin` queries require GeoPandas 1.0 or newer; the recorded GeoPandas 0.14.4 pin predates this usage.
- **`outputs/`** — Regional OSM network caches, saved plots, and cached background images. The shared Denmark OSM download is stored in `outputs/denmark/`.
- **`old_notebooks/`** — Previous exploratory notebooks kept for reference.

## Run one region

1. Open `one_region_analysis.ipynb` from this folder or the repository root.
2. Set `SAMPLE` to `bornholm` (Bornholm), `funen` (Fyn), `zealand` (Sjælland), `jutland` (Jylland), `longland` (Langeland), or `lollandfalster` (Lolland-Falster).
3. Choose the matching tolerance and extraction margin in the setup cell, then **Run All**. Run all cells again after changing regions.

Loop inputs must already exist at `../bikenwloops/data/input/<SAMPLE>/network/processed/` as `edges_slope.gpkg` and `nodes.gpkg`. The notebook downloads the Denmark OSM PBF if absent, extracts the selected region, and reuses its cached network on later runs. Internet access is needed for the initial OSM and background-image downloads.

Regional results are stored under `outputs/<SAMPLE>/`. Surface imputation is an optional, separate result; it preserves the original surface segments.

## Surface assignments

The single-region notebook defines explicit groups and stable map colours for raw surface tags. Existing project choices for `paved` and `unpaved` are preserved. Ambiguous tags use `other`; absent tags use `missing`, and stretches without a nearby OSM match use `unmatched`. These are project classifications rather than a general OSM standard. A previously unseen tag stops the analysis for review instead of silently becoming missing or using a fallback colour.

Each run writes `outputs/<SAMPLE>/surface_assignments.csv` with the observed OSM tags, their groups, colours, and edge counts. The six-region validation also records loop segment counts and lengths in these files, and writes `outputs/surface_validation_summary.csv`.
