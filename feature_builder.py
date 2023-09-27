from helper_functions import JsonInterface, CsvInterface
import pandas as pd
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
import numpy as np

json_handler = JsonInterface()
csv_handler = CsvInterface()
parameter_dict = json_handler.read_from_file("analysis_files/subset_p_map.json")
info_dict = json_handler.read_from_file("analysis_files/subset_info.json")

def build_parameter_list(parameter_dict):
    parameter_list = list()
    for parameter in parameter_dict:
        parameter_list.append(parameter)
    return parameter_list

def build_url_map(info_dict):
    url_map = dict()
    for hostname in info_dict:
        for url in info_dict[hostname]:
            for anchor in info_dict[hostname][url]['anchors']:
                url_map[anchor] = url
    return url_map

def build_value_map(info_dict):
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

def build_head(parameter_list):
    header = "webpage_from_training_set, "
    for parameter in parameter_list:
        header += parameter + ", "
    header = header[0:len(header)-2] + "\n"
    return header

def build_row_dict(info_dict, parameter_list):
    site_dict = dict()
    for hostname in info_dict:
        for url in info_dict[hostname]:
            for anchor in info_dict[hostname][url]['anchors']:
                site_dict[anchor] = list()
                for parameter in parameter_list:
                    if parameter in info_dict[hostname][url]['anchors'][anchor]['queries']:
                        site_dict[anchor].append(1)
                    else:
                        site_dict[anchor].append(0)
                if info_dict[hostname][url]['anchors'][anchor]['annotation'] == 'yes':
                    site_dict[anchor].append(1)
                else:
                    site_dict[anchor].append(0)
    return site_dict

def build_col_dict(info_dict,parameter_list,url_map):
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
            if parameter in info_dict[hostname][url_map[url]]['anchors'][url]['queries']:
                col_dict[parameter].append(1)
            else:
                col_dict[parameter].append(0)
    return col_dict

def build_rows(row_dict):
    csv = str()
    for row in row_dict:
        csv += row + " , " + str(row_dict[row])[1:len(row_dict[row])-2] + "\n"
    return csv

'''
parameter_list = build_parameter_list(parameter_dict)
print(parameter_list)

url_map = build_url_map(info_dict)

col_dict = build_col_dict(info_dict, parameter_list, url_map)

frame = pd.DataFrame(col_dict)

print(frame)

y = frame['training_target']

h = frame['training_website_name']

X = frame.drop(['training_target','training_website_name'], axis = 1)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.50, random_state=0)

n_estimators = [int(x) for x in np.linspace(start = 10, stop = 80, num = 10)]
max_features = ['auto','sqrt']
max_depth = [2,4]
min_samples_split = [2, 5]
min_samples_leaf = [1,2]
bootstrap = [True, False]
#n_estimators and depth
param_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

rf_model = RandomForestClassifier(oob_score=True)


rf_grid = GridSearchCV(estimator = rf_model, param_grid = param_grid, cv = 5, verbose = 2, n_jobs = 4)
rf_grid.fit(X_train,y_train)



print(rf_grid.best_params_)

print (f'Train Accuracy - : {rf_grid.score(X_train,y_train):.3f}')
print (f'Test Accuracy - : {rf_grid.score(X_test,y_test):.3f}')

#print(type(rf_grid))
features = list()
fd = dict()
for i in range(0,len(X.columns)):
    if rf_grid.best_estimator_.feature_importances_[i] > 0:
        features.append((X.columns[i],rf_grid.best_estimator_.feature_importances_[i]))
        fd[rf_grid.best_estimator_.feature_importances_[i]] = X.columns[i]
print(features)

'''
'''
rf_model.fit(X_train,y_train)
print(rf_model.oob_score_)

print (f'Train Accuracy - : {rf_model.score(X_train,y_train):.3f}')
print (f'Test Accuracy - : {rf_model.score(X_test,y_test):.3f}')

print(X.columns)
print(rf_model.feature_importances_)


features = list()
for i in range(0,len(X.columns)):
    if rf_model.feature_importances_[i] > 0:
        features.append((X.columns[i],rf_model.feature_importances_[i]))

print(features)
'''


print(len(build_value_map(info_dict)))
