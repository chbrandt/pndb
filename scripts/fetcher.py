import os
import sys
import json
import urllib
import requests

_URL = 'https://astrocloud.wr.usgs.gov/dataset/data'

def get_webpage(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    return None

def parse_webpage(html):
    from lxml import etree
    print(html)
    parser = etree.XMLParser()
    root = etree.fromstring(html.replace('&','&amp;'))
    n_tree = root.xpath('//div[@id="datasetlist"][2]')[0]
    # host = n_tree.xpath('.//div[@id="datasetdetails"]/a')[0].get('href')
    host = '/'.join(_URL.split('/')[:-1])
    print(host)
    endpoints = []
    for e in n_tree.xpath('.//li'):
        body = e.text.strip()
        uri = e.xpath('./a[2]')[0].get('href')
        url = '/'.join([host, uri])
        print("Querying", body, url)
        endpoints.append((body, url))
    return endpoints

def query_wms(body, url):
    r = requests.get(url)
    if  r.ok:
        return json.loads(r.text)
    return None

def write_json(geojson, filename):
    with open(filename, 'w') as fout:
        json.dump(geojson, fout)

def pull_data(body, url, outdir):
    print("Querying", body, url)
    geojson = query_wms(body, url)
    filename = os.path.join(outdir, '.'.join([body,'geojson']))
    write_json(geojson, filename)
    return os.path.isfile(filename)

def run_parallel(endpoints, outdir):
    import multiprocessing as mp
    d = outdir

    output = mp.Queue
    procs = [mp.Process(target=pull_data, args=(b,u,d) for b,u in endpoints]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    results = [output.get() for p in procs]
    return results

def main(parallel=False):
    page_html = get_webpage(_URL)
    if not page_html:
        print('Deu ruim')
        return None

    wms_endpoints = parse_webpage(page_html)
    if not wms_endpoints:
        return None

    outdir = 'data_download'
    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    if parallel:
        results = run_parallel(wms_endpoints, outdir)
    else:
        results = [pull_data(body, url, outdir) for body,url in wms_endpoints]



if __name__ == "__main__":
    import sys
    if sys.argv[1]:
        msg = "{!s} will download all WMS (GeoJSON) features from {!s}".format(_URL)
        sys.exit(0)
    main()
