import json
import geopandas as gpd

def normalize_coordinates(lon, lat):
    assert -90 < lat < 90, "Expected latitude in [-90:90], got {!s} instead".format(lat)
    assert -180< lon< 360, "Expected longitude in [-180:360], got {!s} instead".format(lon)
    if lon > 180:
        lon -= 360
    return [lon, lat]

def normalize_string(word):
    return word.lower()

def read_features(filename):
    """
    Read GeoJSON file into a GeoPandas dataframe
    """
    gdf = gpd.read_file(filename, driver="GeoJSON")
    return gdf

def format_doc(row):
    """
    Transform feature into doc.
    I.e, GeoPandas row into dictionary according to db schema
    """
    point = row.geometry.centroid
    doc = {
        'name': normalize_string(row['name']),
        'coordinates':normalize_coordinates(point.x, point.y)
        }
    return doc

def format_collection(body, docs):
    collection = {
        'body': normalize_string(body),
        'locations': docs
        }
    return collection

def main(geojson):
    """
    Input:
     - geojson : string
        GeoJSON filename containing features-collection from USGS/WMS services
    """
    body = os.path.splitext(os.path.basename(geojson))[0]
    gdf = read_features(geojson)
    docs = gdf.apply(format_doc, axis=1).to_list()
    collection = format_collection(body, docs)
    return collection

if __name__ == "__main__":
    import os
    import sys
    if len(sys.argv) == 1:
        print("Usage: {!s} <geojson>".format(os.path.basename(sys.argv[0])))
        sys.exit(1)

    filename = sys.argv[1]

    collection = main(filename)

    output = os.path.basename(filename)
    name,ext = os.path.splitext(output)
    output = os.path.join('data_format', '.'.join([name.lower(),'json']))
    with open(output, 'w') as fp:
        json.dump(collection, fp)
