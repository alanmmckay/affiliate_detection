import json

f = open("analysis_files/subset_info.json","r")
data = f.read()
f.close()

data = json.loads(data)

#Create a parameter map
parameter_map = dict()

parameters_list = {}
parameter_counts = {1:dict()}


for hostname in data:
    for url in data[hostname]:
        for anchor in data[hostname][url]['anchors']:
            for query in data[hostname][url]['anchors'][anchor]["queries"]:
                try:
                    parameter_map[query]
                    old_count = parameters_list[query]
                    parameters_list[query] += 1
                except:
                    parameter_map[query] = dict()
                    parameter_map[query]['values'] = list()
                    parameter_map[query]['locations'] = dict()
                    parameters_list[query] = 1
                    old_count = 0

                try:
                    parameter_map[query]['locations'][url]
                except:
                    parameter_map[query]['locations'][url] = list()


                try:
                    parameter_counts[old_count + 1]
                except:
                    parameter_counts[old_count + 1] = dict()

                parameter_counts[old_count + 1][query] = True

                if old_count != 0:
                    del parameter_counts[old_count][query]

                parameter_map[query]['locations'][url].append(anchor)
                parameter_map[query]['values'].append(data[hostname][url]['anchors'][anchor]["queries"][query])


#print(json.dumps(parameters_list, indent = 4))
#sorted_parameters_list = sorted(parameters_list.items(), key=lambda x:x[1])
#print(sorted_parameters_list)

keys = list(parameter_counts.keys())
for key in keys:
    if len(parameter_counts[key]) == 0:
        del parameter_counts[key]

#print(json.dumps(parameter_counts,indent=4))

f = open('analysis_files/subset_p_map.json','w')
f.write(json.dumps(parameter_map, indent = 4))
f.close()

sorted_obj = sorted(parameters_list.items(), key = lambda x:x[1])
sorted_parameters_list = {val[0] : val[1] for val in reversed(sorted_obj)}

f = open('analysis_files/subset_parameters_list.json','w')
f.write(json.dumps(sorted_parameters_list, indent = 4))
f.close()
