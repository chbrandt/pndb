import requests
from flask import request
from eve import Eve

# def on_fetched_resource(resource, response):
#     # del(response['_links'])
#     del(response['_meta'])
#     # would result in an empty JSON document
#     # del(response['_items'])
#     for doc in response['_items']:
#         # doc['location'] = doc['location'].get('coordinates')
#         c = doc['location'].get('coordinates')
#         doc['lon'] = c[0]
#         doc['lat'] = c[1]
#         del(doc['location'])
#         del(doc['_id'])
#         del(doc['_created'])
#         del(doc['_updated'])
#         del(doc['_etag'])
#
app = Eve()
# app.on_fetched_resource += on_fetched_resource


@app.route('/centroid/<string:body>/<string:name>')
def centroid_by_name(body, name):
    url = '?'.join([request.url_root+'centroids',
                    'where={"body":"'+body+'","name":"'+name+'"}'])
    r = requests.get(url)
    return r.json()


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
