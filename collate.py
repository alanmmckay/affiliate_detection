from helper_functions import DataInterface, SourceInterface, JsonInterface
import json
from urllib.parse import urlparse, parse_qsl
db_handler = DataInterface("datadir/","/crawl-data.sqlite")
sources_handler = SourceInterface()
json_handler = JsonInterface()

source_list = sources_handler.get_source_files()
info_dict = dict()
for f in source_list:
    sources_handler.set_html_file(f)
    url = db_handler.get_url_from_source(f)
    url_object = urlparse(url)
    hostname = url_object.hostname

    try:
        info_dict[hostname]
    except:
        info_dict[hostname] = dict()

    info_dict[hostname][url] = dict()
    info_dict[hostname][url]['visit_id'] = sources_handler.get_visit_id()
    info_dict[hostname][url]['anchors'] = dict()

    hrefs = sources_handler.get_anchor_hrefs()
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
        info_dict[hostname][url]['anchors'][anchor]['annotation'] = None

        queries = parse_qsl(nurl_object.query)
        for query in queries:
            if len(query) == 2:
                info_dict[hostname][url]['anchors'][anchor]['queries'][query[0]] = query[1]
            elif len(query) == 1:
                info_dict[hostname][url]['anchors'][anchor]['queries'][query[0]] = None
            else:
                #This should be an impossibility
                raise Exception("Seem to have a query of length > 3;")


json_handler.write_to_file('analysis_files/info.json', info_dict)


