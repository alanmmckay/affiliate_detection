from helper_functions import JsonInterface
import pandas as pd
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder
import numpy as np
import math

json_handler = JsonInterface()
parameter_dict = json_handler.read_from_file("analysis_files/subset_p_map.json")
info_dict = json_handler.read_from_file("analysis_files/subset_info.json")

def build_parameter_list(parameter_dict):
    """
        A function which receives a dictionary whose keys describe a parameter
        of the set and returns a list of these parameters. This is used to
        ensure an enforced ordering as the paramters are built into feature
        sets
    """
    parameter_list = list()
    for parameter in parameter_dict:
        parameter_list.append(parameter)
    return parameter_list


def build_url_map(info_dict):
    """
        A function which receives a dictionary formed through a crawl for the
        context of this project and returns a dictionary whose keys are the
        urls contained in each pages' anchor tags. The values for these keys
        are the urls which contain the anchor tags. This is used to allow
        easy navigation through dictionary formed through the crawl.
    """
    url_map = dict()
    for hostname in info_dict:
        for url in info_dict[hostname]:
            for anchor in info_dict[hostname][url]['anchors']:
                url_map[anchor] = url #Should consider a log of duplicates
    return url_map


def build_value_map(info_dict):
    """
        A function which receives a dictionary formed through a crawl for the
        context of this project and returns a dictionary whose keys are the
        values of query string parameters discovered through the crawl. A
        value of this dictionary's key set is some unique value to act as an
        encoding.
    """
    current = 1
    value_map = dict()
    for hostname in info_dict:
        for url in info_dict[hostname]:
            for anchor in info_dict[hostname][url]['anchors']:
                for query in info_dict[hostname][url]['anchors'][anchor]['queries']:
                    key = info_dict[hostname][url]['anchors'][anchor]['queries'][query]
                    try:
                        value_map[key]
                    except:
                        value_map[key] = current
                        current += 1
    return value_map


def build_row_dict(info_dict, parameter_list):
    """
        This function creates a dictionary such that each key is a URL from
        the initial crawl and the subsequent value list is that key's value
        for each parameter. This is currently being unused and needs to factor
        mapped values.
    """
    site_dict = dict()
    for hostname in info_dict:
        for url in info_dict[hostname]:
            for anchor in info_dict[hostname][url]['anchors']:
                site_dict[anchor] = list()
                for parameter in parameter_list:
                    queries = info_dict[hostname][url]['anchors'][anchor]['queries']
                    if parameter in queries:
                        site_dict[anchor].append(1)
                    else:
                        site_dict[anchor].append(0)
                if info_dict[hostname][url]['anchors'][anchor]['annotation'] == 'yes':
                    site_dict[anchor].append(1)
                else:
                    site_dict[anchor].append(0)
    return site_dict


def build_col_dict(info_dict,parameter_list,url_map):
    """
        A function which produces a dictionary whose keys are some query-string
        paramter and the values are a list where each entry (i) of the list is
        representative of the value for entity (i). An entity is some url from
        gathered for this project to classify for affiliate status.
    """
    col_dict = dict()
    col_dict['training_website_name'] = list()
    col_dict['training_target'] = list()
    for url in url_map:
        col_dict['training_website_name'].append(url)
        origin = url_map[url]
        hostname = urlparse(origin).hostname
        isaffiliate = info_dict[hostname][origin]['anchors'][url]['annotation']
        if isaffiliate == 'yes':
            col_dict['training_target'].append(1)
        else:
            col_dict['training_target'].append(0)
    for parameter in parameter_list:
        col_dict[parameter] = list()
        for url in url_map:
            hostname = urlparse(url_map[url]).hostname
            queries = info_dict[hostname][url_map[url]]['anchors'][url]['queries']
            if parameter in queries:
                col_dict[parameter].append(queries[parameter])
            else:
                col_dict[parameter].append(0)
        le = LabelEncoder()
        le.fit(col_dict[parameter])
        col_dict[parameter] = le.transform(col_dict[parameter])
    return col_dict


def build_csv_head(parameter_list):
    header = "webpage_from_training_set, "
    for parameter in parameter_list:
        header += parameter + ", "
    header = header[0:len(header)-2] + "\n"
    return header


def build_csv_rows(row_dict):
    csv = str()
    for row in row_dict:
        csv += row + " , " + str(row_dict[row])[1:len(row_dict[row])-2] + "\n"
    return csv


parameter_list = build_parameter_list(parameter_dict)
value_map = build_value_map(info_dict)
url_map = build_url_map(info_dict)
col_dict = build_col_dict(info_dict, parameter_list, url_map)

frame = pd.DataFrame(col_dict)
y = frame['training_target']
h = frame['training_website_name']
X = frame.drop(['training_target','training_website_name'], axis = 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=0)

n_estimators = [int(x) for x in np.linspace(start = 10, stop = 80, num = 10)]
max_features = ['sqrt','log2']
max_depth = [2,4] + [int(x) for x in np.linspace(start = 6, stop = len(parameter_list)//2, num = 8)]
min_samples_split = [2, 5] + [round(math.log(len(parameter_list))/math.log(2))]
min_samples_leaf = [1,2] + [round(math.log(len(parameter_list))/math.log(2))]
bootstrap = [True, False]
oob_score = [True, False]
#n_estimators and depth
param_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap,
               'oob_score': oob_score}



#regular random forest:
#{'bootstrap': True, 'max_depth': 10, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 10, 'oob_score': False}
rf_model = RandomForestClassifier(bootstrap = True, max_depth = 10, max_features = 'log2', min_samples_leaf = 1, min_samples_split = 2, n_estimators = 10, oob_score = False)
rf_model.fit(X_train,y_train)
#print(rf_model.oob_score_)
print (f'Train Accuracy - : {rf_model.score(X_train,y_train):.3f}')
print (f'Test Accuracy - : {rf_model.score(X_test,y_test):.3f}')
#print(X.columns)
#print(rf_model.feature_importances_)
features = list()
for i in range(0,len(X.columns)):
    if rf_model.feature_importances_[i] > 0:
        features.append((X.columns[i],rf_model.feature_importances_[i]))
#print(features)


'''
#grid search random forest:
rf_model = RandomForestClassifier()
rf_grid = GridSearchCV(estimator = rf_model, param_grid = param_grid, cv = 5, verbose = 2, n_jobs = 4)
rf_grid.fit(X_train,y_train)

print(rf_grid.best_params_)

print (f'Train Accuracy - : {rf_grid.score(X_train,y_train):.3f}')
print (f'Test Accuracy - : {rf_grid.score(X_test,y_test):.3f}')

features = list()
fd = dict()
for i in range(0,len(X.columns)):
    if rf_grid.best_estimator_.feature_importances_[i] > 0:
        features.append((X.columns[i],rf_grid.best_estimator_.feature_importances_[i]))
        fd[rf_grid.best_estimator_.feature_importances_[i]] = X.columns[i]
print(features)
'''

rank_dict = dict()
for feature in features:
    rank_dict[float(feature[1])] = feature[0]
    #rank_dict[features[int(feature[1])]] = feature[0]

rank_dict = sorted(rank_dict.items())

json_handler.write_to_file("rankings.json",rank_dict)

from sklearn.tree import export_graphviz
import os
count = 0
for tree in rf_model.estimators_:
    dotdata = export_graphviz(tree,feature_names = X.columns, filled = True, rounded = True)
    f = open('tree'+str(count)+'.dot','w')
    f.write(dotdata)
    f.close()
    os.system('dot -Tpng tree'+str(count)+'.dot -o tree'+str(count)+'.png')
    os.system('rm tree'+str(count)+'.dot')
    count += 1
