from eve import Eve
app = Eve()

def on_fetched_resource(resource, response):
    # del(response['_links'])
    del(response['_meta'])
    # would result in an empty JSON document
    # del(response['_items'])
    for doc in response['_items']:
        # doc['location'] = doc['location'].get('coordinates')
        c = doc['location'].get('coordinates')
        doc['lon'] = c[0]
        doc['lat'] = c[1]
        del(doc['location'])
        del(doc['_id'])
        del(doc['_created'])
        del(doc['_updated'])
        del(doc['_etag'])

app = Eve()
app.on_fetched_resource += on_fetched_resource

if __name__ == '__main__':
    app.run(debug=True)
