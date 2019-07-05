# Planetary Nomenclature DB

Say you want to know the location of the Apollo crater, so that you can
check where is the famous crater in that map you wrote in the html/js turorial.
Well, by the time of this writing (July 2019) you either had to go to
Wikipedia -- which, by the way, you should anyway -- or you could go to
IAU/USGS planetary nomenclature page at https://planetarynames.wr.usgs.gov/,
which is OK.

But we can do better: we can build our own DB and provide it through a REST
interface, for example, that would allow to simply ask for a "name" in a
"body" and get its "location".

## Data
Data is provided by USGS through a series of WMS endpoints.
The endpoints, organized by body name, are listed in:
* https://astrocloud.wr.usgs.gov/dataset/data

More information, and also examples, about nomenclature can be found at:
* https://astrocloud.wr.usgs.gov/dataset/docs/index.html
