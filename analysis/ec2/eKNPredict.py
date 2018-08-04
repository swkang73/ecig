'''human breath K Neighbor Classifier
may or may not add PCA processing
classifies e-cigarette mass scan into three e-cig (G6 / Juul / Blu)
reference 1: http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html#sklearn.neighbors.KNeighborsClassifier
'''

import os, csv, numpy as np, matplotlib.pyplot as plt, pandas as pd
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier

COMPONENT_NUM = 20
CIGTOTAL = 4
HALO = 1
JUUL = 2
BLU = 3
V2 = 4

def getAns(index):
    if (index + 1) % CIGTOTAL != 0:
        return (index + 1) % CIGTOTAL
    return V2

print('Read training data...')
with open('training.csv', 'r') as reader:
    train_label = []
    train_data = []
    for line in reader.readlines():
        data = list(map(float, line.rstrip().split(',')))
        train_label.append(data[0])
        train_data.append(data[1:])
print('Loaded ' + str(len(train_label)))

print('Reduction and training...')
train_label = np.array(train_label)
train_data = np.array(train_data)
#pca = PCA(n_components=COMPONENT_NUM, whiten=True)
#pca.fit(train_data)
#train_data = pca.transform(train_data)
clf = KNeighborsClassifier()
clf.fit(train_data, train_label)


print('Read testing data...')
with open('testing_vaporfi.csv', 'r') as reader:
    test_data = []
    for line in reader.readlines():
        pixels = list(map(float, line.rstrip().split(',')))
        test_data.append(pixels)
print('Loaded ' + str(len(test_data)))

print('Predicting...')
test_data = np.array(test_data)
#test_data = pca.transform(test_data)
predict = clf.predict(test_data)
prob = clf.predict_proba(test_data)

# save prediction
print('Saving...')
with open('vpf_kn_predict.csv', 'w') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = 
    	['Index', 'Actual', 'Prediction'])
    writer.writeheader()

    count = 0
    for p in predict:
        writer.writerow({'Index': str(count + 1), 
        	'Actual': str(getAns(count)),
        	'Prediction': str(p)
        	})
        count += 1




