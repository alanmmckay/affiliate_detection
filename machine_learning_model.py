import math
import numpy as np
import pandas as pd
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn.dummy import DummyClassifier


from helper_functions import JsonInterface
from feature_builder import build_parameter_list,build_url_map,build_value_map,build_col_dict

json_handler = JsonInterface()
parameter_dict = json_handler.read_from_file("analysis_files/subset_p_map.json")
info_dict = json_handler.read_from_file("analysis_files/subset_info.json")

parameter_list = build_parameter_list(parameter_dict)
value_map = build_value_map(info_dict)
url_map = build_url_map(info_dict)
col_dict = build_col_dict(info_dict, parameter_list, url_map,value_map)

frame = pd.DataFrame(col_dict)

oe = OrdinalEncoder()
oe.fit(frame[parameter_list])
frame[parameter_list] = oe.transform(frame[parameter_list])

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
#label studio


#regular random forest:
#{'bootstrap': True, 'max_depth': 10, 'max_features': 'log2', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 10, 'oob_score': False}
grid_res = {'bootstrap': True, 'max_depth': 31, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 5, 'n_estimators': 10, 'oob_score': True}
rf_model = RandomForestClassifier(bootstrap = grid_res['bootstrap'], max_depth = grid_res['max_depth'], max_features = grid_res["max_features"], min_samples_leaf = grid_res['min_samples_leaf'], min_samples_split = grid_res['min_samples_split'], n_estimators = grid_res['n_estimators'], oob_score = grid_res['oob_score'])
rf_model.fit(X_train,y_train)
#print(rf_model.oob_score_)
print (f'Train Accuracy - : {rf_model.score(X_train,y_train):.3f}')
print (f'Test Accuracy - : {rf_model.score(X_test,y_test):.3f}')

print(f'Train precision - : {precision_score(y_train,rf_model.predict(X_train)):.3f}')
print(f'Test precision - : {precision_score(y_test,rf_model.predict(X_test)):.3f}')

print(f'Train recall - : {recall_score(y_train,rf_model.predict(X_train)):.3f}')
print(f'Test recall - : {recall_score(y_test,rf_model.predict(X_test)):.3f}')

print(f'Train f1score - : {f1_score(y_train,rf_model.predict(X_train)):.3f}')
print(f'Test f1score - : {f1_score(y_test,rf_model.predict(X_test)):.3f}')

#print(X.columns)
#print(rf_model.feature_importances_)
features = list()
for i in range(0,len(X.columns)):
    if rf_model.feature_importances_[i] > 0:
        features.append((X.columns[i],rf_model.feature_importances_[i]))
#print(features)

#majority class - stupidest classifier that has learned nothing - base rate fallacy
#build intuition

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
'''
for tree in rf_model.estimators_:
    dotdata = export_graphviz(tree,feature_names = X.columns, filled = True, rounded = True)
    f = open('tree'+str(count)+'.dot','w')
    f.write(dotdata)
    f.close()
    os.system('dot -Tpng tree'+str(count)+'.dot -o tree'+str(count)+'.png')
    os.system('rm tree'+str(count)+'.dot')
    count += 1
'''
strategies = ['most_frequent', 'stratified', 'uniform']

test_scores = {}
for s in strategies:
	if s =='constant':
		continue
	else:
		dclf = DummyClassifier(strategy = s, random_state = 0)
	dclf.fit(X_train, y_train)
	score = dclf.score(X_test, y_test)
	test_scores[s] = score

strategies.append('rf_model')
test_scores['rf_model'] = rf_model.score(X_test,y_test)
print(test_scores)
