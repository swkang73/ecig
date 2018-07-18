'''E-cigarette Random Forest Classifier
classifies e-cigarette mass scan into three e-cig (G6 / Juul / Blu)
reference 1: https://chrisalbon.com/machine_learning/trees_and_forests/random_forest_classifier_example/
reference 2: http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
'''

import csv, numpy as np, matplotlib.pyplot as plt, pandas as pd
from sklearn.ensemble import RandomForestClassifier

MAX_FEATURES = 50
CIGTOTAL = 3
G6 = 1
JUUL = 2
BLU = 3

def getAns(index):
    if (index + 1) % CIGTOTAL != 0:
        return index % CIGTOTAL
    return BLU

print('Read training data...')
with open('training.csv', 'r') as reader:
    train_label = []
    train_data = []
    for line in reader.readlines():
        data = list(map(float, line.rstrip().split(',')))
        train_label.append(data[0])
        train_data.append(data[1:])
print('Loaded ' + str(len(train_label)))

print('RF Training...')
train_label = np.array(train_label)
train_data = np.array(train_data)
clf = RandomForestClassifier(max_features=MAX_FEATURES, n_jobs=2, random_state=0)
clf.fit(train_data, train_label)

print('Read testing data...')
with open('testing.csv', 'r') as reader:
    test_data = []
    for line in reader.readlines():
        pixels = list(map(float, line.rstrip().split(',')))
        test_data.append(pixels)
print('Loaded ' + str(len(test_data)))

print('Predicting...')
test_data = np.array(test_data)
predict = clf.predict(test_data)
prob = clf.predict_proba(test_data)

# see feature importance
'''index = 0
count = 0 
for imp in clf.feature_importances_:
	if imp != 0.:
       count += 1
       print('m/z: %d importance: %.4f' % (index, imp))
	index += 1
print('total number of features: %d' % count)'''


print('Saving...')
with open('rf_predict.csv', 'w') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = 
    	['Index', 'Prediction', 'Actual', 
    	'G6 prob', 'Juul prob', 'Blu prob'])
    writer.writeheader()

    count = 0
    for p in predict:
        writer.writerow({'Index': str(count), 
        	'Prediction': str(p), 
        	'Actual': str(getAns(count)),
        	'G6 prob': prob[count][0], 
        	'Juul prob': prob[count][1], 
        	'Blu prob': prob[count][2]})
        count += 1




