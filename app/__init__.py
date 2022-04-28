import requests
from flask import request, render_template_string, redirect, url_for
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

def on_aggregate(endpoint, pipeline):
    print(endpoint)
    print(pipeline)
# app.before_aggregation += on_aggregate


_SEARCH_PAGE_ = """
<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="icon" href="/docs/4.0/assets/img/favicons/favicon.ico">

  <title>Search</title>
  <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
  <link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
  <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script src="https://kit.fontawesome.com/ed097fe321.js"></script>
  <style>
    html, body {
            height: 100%;
            width: 100%;
        }
    </style>
</head>

<body>
  <div class="container" style="width:100%; height:100%">
    <div class="row text-right" style="height:50px; padding-right:5%; padding-top:10px">
      <button type="button" class="btn btn-default" style="border:0"
        data-toggle="modal" data-target="#info">
            <i class="far fa-question-circle fa-2x" style="color:gray"></i>
      </button>
    </div>
    <div class="col-md-6 col-md-offset-3">
      <div class="row">
        <div id="logo" class="text-center">
            <a href="{{hosturl}}">
          <img src="https://raw.githubusercontent.com/planmap-eu/storymaps/master/app/public/img/cr-logo.png" alt="" height="72">
            </a>
          <hr style="border:0" />
          <!--
            <h5><small>About</small></h5>
            -->
        </div>
        <form role="form" id="form-buscar" method="POST" action="/search">
          <div class="form-group">
            <div class="input-group">
              <input id="input" class="form-control" type="text" name="input" placeholder="Search for body or features, e.g. 'moon' or 'mars chaos'" required />
              <span class="input-group-btn">
                <button class="btn btn-success" type="submit">
                  <i class="glyphicon glyphicon-search" aria-hidden="true"></i> Search
                </button>
              </span>
            </div>
          </div>
        </form>
      </div>
      {% if results %}
      <div class="col-md-6 col-md-offset-2">
        <table class="table text-center">
          <thead>
            <tr>
              <th>Body</th>
              <th>Feature</th>
              <th style="text-align:right">Lon</th>
              <th style="text-align:right">Lat</th>
            <tr>
          </thead>
          <tbody>
            {% for result in results %}
            <tr>
              <th>{{result.0}}</th>
              <th>{{result.1}}</th>
              <th style="text-align:right">{{result.2}}</th>
              <th style="text-align:right">{{result.3}}</th>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      {% endif %}
    </div>
  </div>
  <!-- Modal -->
  <!-- From https://www.quackit.com/bootstrap/bootstrap_3/tutorial/bootstrap_modal.cfm -->
  <div class="modal fade" id="info" href="#info" tabindex="-1" role="dialog" aria-labelledby="modalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 class="modal-title" id="modalLabel">
            About PNDB
          </h4>
        </div>
        <div class="modal-body">
          <h5>API</h5>
          <p>Behind the Search page we are now there is a set of endpoints providing
          access to the whole content of the Planetary Nomenclature database.
          The endpoints are organized as follows:</p>
          <ul>
            <li>
                <tt>/api/centroids/bodies</tt>
                <ul><li>list of planets, moon, asteroids available;</li></ul>
                <p class="well well-sm">{{hosturl}}/api/centroids/bodies</p>
            </li>
            <li>
                <tt>/api/centroids/[body]</tt>
                <ul><li>list of features names for body <tt>[body]</tt>;</li></ul>
                <p class="well well-sm">{{hosturl}}/api/centroids/amalthea</p>
            </li>
            <li><tt>/api/centroids/[body]/[name]</tt>
                <ul><li>centroid (GeoJSON format) of feature <tt>[name]</tt>;</li></ul>
                <p class="well well-sm">{{hosturl}}/api/centroids/amalthea/pan</p>
            </li>
            <li><tt>/api/centroids/[body]/[name]/flat</tt>
                <ul><li>centroid (flat format: lat,lon) of feature <tt>[name]</tt>;</li></ul>
                <p class="well well-sm">{{hosturl}}/api/centroids/amalthea/pan/flat</p>
            </li>
          </ul>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</body>

<script>
    $(document).ready(function() {
      if(window.location.href.indexOf('#info') != -1) {
        $('#info').modal('show');
      }
    });
</script>

</html>"""
@app.route('/search', methods=['GET','POST'])
def search():
    hosturl = request.url_root[:-1]
    if request.method == 'POST':
        text = request.form.get('input', None)
        results = []
        if text:
            text_and = ' '.join(['\\"{}\\"'.format(s) for s in text.split()])
            agg_query = '"$value":"{!s}"'.format(text_and)
            agg_query = 'aggregate={'+agg_query+'}'
            url = request.url_root + 'api/centroids?' + agg_query
            r = requests.get(url)
            if r.status_code == 200:
                js = r.json()
                for d in js['_items']:
                    c = d['location'].get('coordinates')
                    results.append((d['body'],d['name'],c[0],c[1]))
        return render_template_string(_SEARCH_PAGE_, results=results, hosturl=hosturl)
    return render_template_string(_SEARCH_PAGE_, hosturl=hosturl)

@app.route('/')
def home_page():
    return redirect(url_for('search'))


