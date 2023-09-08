from helper_functions import DataInterface, SourceInterface
import os
import json
from urllib.parse import urlparse, parse_qsl

db_object = DataInterface("datadir/","/crawl-data.sqlite")
sources_object = SourceInterface()

source_list = os.listdir(sources_object.path)

info_dict = dict()


for f in source_list:
    sources_object.set_html_file(f)
    url = db_object.get_url_from_source(f)
    url_object = urlparse(url)
    hostname = url_object.hostname
    '''if hostname not in info_dict: #inefficient
        info_dict[hostname] = dict()'''
    try:
        info_dict[hostname]
    except:
        info_dict[hostname] = dict()

    info_dict[hostname][url] = dict()
    info_dict[hostname][url]['visit_id'] = sources_object.get_visit_id()
    info_dict[hostname][url]['anchors'] = dict()
    hrefs = sources_object.get_anchor_hrefs()
    for anchor in hrefs:
        info_dict[hostname][url]['anchors'][anchor] = dict()
        nurl_object = urlparse(anchor)
        if not nurl_object.hostname:
            nhostname = hostname
        else:
            nhostname = nurl_object.hostname
        info_dict[hostname][url]['anchors'][anchor]['domain'] = nhostname
        info_dict[hostname][url]['anchors'][anchor]['subdomain'] = nurl_object.path
        info_dict[hostname][url]['anchors'][anchor]['querystring'] = nurl_object.query
        info_dict[hostname][url]['anchors'][anchor]['queries'] = dict()
        queries = parse_qsl(nurl_object.query)
        for query in queries:
            if len(query) == 2:
                info_dict[hostname][url]['anchors'][anchor]['queries'][query[0]] = query[1]
            elif len(query) == 1:
                info_dict[hostname][url]['anchors'][anchor]['queries'][query[0]] = None
            else:
                raise Exception("Seem to have a query of length > 3")

f = open('analysis_files/info.json','w')
f.write(json.dumps(info_dict, indent = 4))
f.close()


