# ================================================================
# MongoDB
# -------
# Server
#
MONGO_HOST = 'mongodb+srv://planmap.nmnye.mongodb.net'
MONGO_PORT = 27017
# If there is one, user authentication.
#
MONGO_USERNAME = 'pndb'
MONGO_PASSWORD = 'pndb'
# Database for user authentication (if --auth mode is enabled)
#
MONGO_AUTH_SOURCE = 'admin'
# Database where data collection(s) to be served is(are)
#
MONGO_DBNAME = 'nomenclature'
# ================================================================

# ================================================================
# Results
# -------
# Disable results pagination (default is 25 documents)
#
PAGINATION = False
# Hypermedia as the Engine of Application State
#
HATEOAS = False
# URL prefix for (all) endpoints
#
URL_PREFIX='api'
# ================================================================


bodies_list = {
    'url': 'centroids/bodies',
    'datasource': {
        'source': 'centroids',
        'aggregation': {
            'pipeline': [
                {"$group": {"_id": "$body"}},
                {"$sort": {"_id": 1}},
                {"$project": {"_id": 0, "body": "$_id"}}
            ]
        },
    }
}

centroids_list = {
    'item_title': 'centroid',
    'url': 'centroids/<regex("[\w]+"):body>',
    'datasource': {
        'source': 'centroids',
        'projection': {'name': 1, 'body': 1, 'location': 1}
    }
}

centroid_get = {
    'item_title': 'centroid',
    'url': 'centroids/<regex("[\w]+"):body>/<regex("[\w ]+"):name>',
    'datasource': {
        'source': 'centroids',
        'projection': {'name': 1, 'body': 1, 'location': 1}
    }
}

centroid_lonlat_get = {
    'item_title': 'centroid',
    'url': 'centroids/<regex("[\w]+"):body>/<regex("[\w ]+"):name>/flat',
    'datasource': {
        'source': 'centroids',
        'projection': {'name': 1, 'body': 1, 'location': 1}
    }
}


DOMAIN = {
    'bodies_list': bodies_list,
    'centroids_list': centroids_list,
    'centroid': centroid_get,
    'centroid_ll': centroid_lonlat_get,
    'centroids': {
        'datasource': {
            'aggregation': {
                'pipeline': [
                    {"$match": {"$text": {"$search": "$value"}}},
                    # {"$group": {"_id": "$body"}},
                    {"$sort": {"body": 1, "name": 1}},
                    # {"$project": {"_id": 0, "body": "$_id"}}
                ]
            }
        }},
}
