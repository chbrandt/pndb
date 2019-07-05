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

def main():
    page_html = get_webpage(_URL)
    if not page_html:
        print('Deu ruim')
        return None
    wms_endpoints = parse_webpage(page_html)
    for body,url in wms_endpoints:
        print("About to query", body, url)
        geojson = query_wms(body, url)
        print("Query result", geojson)
        outdir = 'data_download'
        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        filename = os.path.join(outdir, '.'.join([body,'geojson']))
        write_json(geojson, filename)
