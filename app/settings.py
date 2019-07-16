MONGO_HOST = 'mongodb+srv://planmap-nmnye.mongodb.net'
MONGO_PORT = 27017

# Skip this block if your db has no auth. But it really should.
MONGO_USERNAME = 'planmap'
MONGO_PASSWORD = 'h2020'
# Name of the database on which the user can be authenticated,
# needed if --auth mode is enabled.
MONGO_AUTH_SOURCE = 'admin'

MONGO_DBNAME = 'nomenclature'

crater = {
    'hateoas': False,
    'item_title': 'crater centroid',
    'url': 'centroid/<regex("[\w]+"):body>/<regex("[\w ]+"):name>',
    'datasource': {
        'projection': {'name': 1, 'body': 1, 'location.coordinates': 1,
            '_id': 0, '_created': 0, '_updated': 0, '_etag': 0}
    }
}

# body = {
#     'item_title': 'body craters',
#     'url': 'centroid/<regex("[\w]+"):body>'
# }

DOMAIN = {
    'centroids': crater,
}
