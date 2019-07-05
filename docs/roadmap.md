# Planetary Nomenclature DB: from download to (re)publish

0. Define DB (JSON document) schema to publish
1. Get WMS endpoints from https://astrocloud.wr.usgs.gov/dataset/data, `Nomenclature` section;
2. Download GeoJSON documents from WMS service for each body/item in the list;
3. Format GeoJSON features into PNDB (JSON) documents

