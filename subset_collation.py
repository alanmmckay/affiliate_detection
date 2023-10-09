from helper_functions import JsonInterface
from urllib.parse import urlparse

json_handler = JsonInterface()
main_info = json_handler.read_from_file('analysis_files/info.json')

f = open('annotated_pages.txt','r')
annotated = [line.strip() for line in f.readlines()]
f.close()

annotated_json = dict()
for page in annotated:
    hostname = urlparse(page).hostname
    try:
        annotated_json[hostname]
    except:
        annotated_json[hostname] = dict()
    annotated_json[hostname][page] = main_info[hostname][page]
    for anchor in annotated_json[hostname][page]['anchors']:
        annotated_json[hostname][page]['anchors'][anchor]['redirects'] = dict()
        if annotated_json[hostname][page]['anchors'][anchor]['annotation'] == None:
            annotated_json[hostname][page]['anchors'][anchor]['annotation'] = "no"

json_handler.write_to_file('analysis_files/subset_info.json', annotated_json)

#To satisfy curiosity:
acount = 0
allcount = 0
for hostname in annotated_json:
    for url in annotated_json[hostname]:
        for anchor in annotated_json[hostname][url]['anchors']:
            if annotated_json[hostname][url]['anchors'][anchor]['annotation'] == 'yes':
                acount += 1
            allcount += 1

print(acount)
print(allcount)
print(acount/allcount)
