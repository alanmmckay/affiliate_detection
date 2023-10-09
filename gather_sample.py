from helper_functions import JsonInterface

json_handler = JsonInterface()

info_dict = json_handler.read_from_file('analysis_files/subset_info.json')

yes_map = dict()
yes_list = list()
no_map = dict()
no_list = list()
for hostname in info_dict:
    for site in info_dict[hostname]:
        anchors = info_dict[hostname][site]['anchors']
        for anchor in anchors:
            protocol = anchor[0:8]
            if protocol[0:7] == 'http://' or protocol[0:8] == 'https://':
                if anchors[anchor]['annotation'] == 'yes':
                    try:
                        yes_map[anchor]
                    except:
                        yes_map[anchor] = list()
                        yes_list.append(anchor)
                    yes_map[anchor].append(site)
                else:
                    try:
                        no_map[anchor]
                    except:
                        no_map[anchor] = list()
                        no_list.append(anchor)
                    no_map[anchor].append(site)

print(len(yes_list))
print(len(no_list))

def list_to_str(lst):
    retrn_str = str()
    lst.sort()
    for item in lst:
        retrn_str += item + '\n'
    return retrn_str

f = open('analysis_files/sample/affiliate_links.txt','w')
f.write(list_to_str(yes_list))
f.close()

f = open('analysis_files/sample/non-affiliate_links.txt','w')
f.write(list_to_str(no_list))
f.close()

json_handler.write_to_file('analysis_files/sample/affiliate_links.json',yes_map)
json_handler.write_to_file('analysis_files/sample/non-affiliate_links.json',no_map)

import random

random.seed(48)

f = open('analysis_files/sample/affiliate_sample.txt','w')
yes_sample = random.sample(yes_list,500)
print(len(yes_sample))
f.write(list_to_str(yes_sample))
f.close()

random.seed(48)

f = open("analysis_files/sample/non-affiliate_sample.txt",'w')
no_sample = random.sample(no_list,500)
print(len(no_sample))
f.write(list_to_str(no_sample))
f.close()
