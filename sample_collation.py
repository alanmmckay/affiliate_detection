from helper_functions import JsonInterface
from urllib.parse import urlparse

json_handler = JsonInterface()
yes_info = json_handler.read_from_file('analysis_files/sample/affiliate_links.json')
no_info = json_handler.read_from_file('analysis_files/sample/non-affiliate_links.json')
info = json_handler.read_from_file('analysis_files/subset_info.json')

f = open('analysis_files/sample/affiliate_sample.txt','r')
yes_list = f.readlines()
f.close()

f = open('analysis_files/sample/non-affiliate_sample.txt','r')
no_list = f.readlines()
f.close()

yes_list = [i[:len(i)-1] for i in yes_list]
no_list = [i[:len(i)-1] for i in no_list]

count = 0
subcount = 0
sample_dict = dict()

for url in yes_list:
    origins = yes_info[url]
    if len(origins) > 1:
        subcount += len(origins) - 1
    for origin in origins:
        hostname = urlparse(origin).hostname
        try:
            sample_dict[hostname]
        except:
            sample_dict[hostname] = dict()

        try:
            sample_dict[hostname][origin]
        except:
            sample_dict[hostname][origin] = dict()
            sample_dict[hostname][origin]['visit_id'] = info[hostname][origin]['visit_id']
            sample_dict[hostname][origin]['anchors'] = dict()
        count+=1
        sample_dict[hostname][origin]['anchors'][url] = info[hostname][origin]['anchors'][url]


for url in no_list:
    origins = no_info[url]
    if len(origins) > 1:
        subcount += len(origins) - 1
    for origin in origins:
        hostname = urlparse(origin).hostname
        try:
            sample_dict[hostname]
        except:
            sample_dict[hostname] = dict()

        try:
            sample_dict[hostname][origin]
        except:
            sample_dict[hostname][origin] = dict()
            sample_dict[hostname][origin]['visit_id'] = info[hostname][origin]['visit_id']
            sample_dict[hostname][origin]['anchors'] = dict()
        count+=1
        sample_dict[hostname][origin]['anchors'][url] = info[hostname][origin]['anchors'][url]


print(count)
print(subcount)
json_handler.write_to_file('analysis_files/sample_info.json',sample_dict)
