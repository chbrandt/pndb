# ================================================================
# MongoDB
# -------
# Server
#
MONGO_HOST = 'mongodb+srv://planmap-nmnye.mongodb.net'
MONGO_PORT = 27017
# If there is one, user authentication.
#
MONGO_USERNAME = 'planmap'
MONGO_PASSWORD = 'h2020'
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
# ================================================================


centroids = {
    'item_title': 'centroid',
    # 'url': 'centroid/<regex("[\w]+"):body>/<regex("[\w ]+"):name>',
    # 'url': 'centroid/<regex("[\w]+"):body>',
    'datasource': {
        'projection': {'name': 1, 'body': 1, 'location.coordinates': 1}
    }
}

# body = {
#     'item_title': 'body craters',
#     'url': 'centroid/<regex("[\w]+"):body>'
# }

DOMAIN = {
    'centroids': centroids
}
