import requests
from flask import request, render_template_string
from eve import Eve

app = Eve()

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


_SEARCH_PAGE_ = """
<!doctype html>
<html lang="en">
  <head>
  </head>
  <body>
    <div class="container">
      <h1>Search</h1>
      <form method="POST" action="search" class="form-inline">
        <input type="text" name="search_text" id="search_text">
        <button type="submit" class="btn btn-primary">Go</button>
      </form>
    </div>
    <div>
      {{ result }}
    </div>
  </body>
</html>
"""
@app.route('/search', methods=['GET','POST'])
def search():
    # if request.method == 'POST':
    #     text = request.form.search_text
    #     return render_template('search.html', result=text)
    return render_template_string(_SEARCH_PAGE_)


# @app.route('/centroid/<string:body>/<string:name>')
# def centroid_by_name(body, name):
#     url = '?'.join([request.url_root+'centroids',
#                     'where={"body":"'+body+'","name":"'+name+'"}'])
#     r = requests.get(url)
#     return r.json()


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
