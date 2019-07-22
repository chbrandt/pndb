import requests
from flask import request
from eve import Eve

app = Eve()

# @app.route('/centroid/<string:body>/<string:name>')
# def centroid_by_name(body, name):
#     url = '?'.join([request.url_root+'centroids',
#                     'where={"body":"'+body+'","name":"'+name+'"}'])
#     r = requests.get(url)
#     return r.json()

def on_fetched_resource(resource, response):
    # del(response['_links'])
    # del(response['_meta'])
    for doc in response['_items']:
        del(doc['_id'])
        del(doc['_created'])
        del(doc['_updated'])
        del(doc['_etag'])
app.on_fetched_resource += on_fetched_resource

def on_fetched_resource_lonlat(response):
    for doc in response['_items']:
        c = doc['location'].get('coordinates')
        doc['lon'] = c[0]
        doc['lat'] = c[1]
        del(doc['location'])
app.on_fetched_resource_centroid_ll += on_fetched_resource_lonlat


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
