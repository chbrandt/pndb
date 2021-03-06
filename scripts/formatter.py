#!/usr/bin/env python

import json
import geopandas as gpd

def normalize_coordinates(lon, lat):
    assert -90 < lat < 90, "Expected latitude in [-90:90], got {!s} instead".format(lat)
    assert -180<=lon<=360, "Expected longitude in [-180:360], got {!s} instead".format(lon)
    if lon > 180:
        lon -= 360
    return [round(lon,3), round(lat,3)]

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
    try:
        doc = {
            'name': normalize_string(row['name']),
            'location': {
                'type': "Point",
                'coordinates':normalize_coordinates(point.x, point.y)
            }
            }
    except:
        doc = None
    return doc

def main(geojson):
    """
    Input:
     - geojson : string
        GeoJSON filename containing features-collection from USGS/WMS services
    """
    body = os.path.splitext(os.path.basename(geojson))[0]
    gdf = read_features(geojson)
    gs = gdf.apply(format_doc, axis=1)
    if gs.isnull().any():
        print("There are wrong coordinates in {!s} causing null entries in the output.".format(geojson))
        gs.dropna(inplace=True)
        if not len(gs):
            print("In fact, {!s} has no valid feature. Output is null.")
            return None
    docs = gs.to_list()

    # Add 'body' to each document
    for d in docs:
        d.update({'body': normalize_string(body)})

    return docs

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
