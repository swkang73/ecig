'''human breath Logistic Regression Classifier
may or may not add PCA processing
classifies e-cigarette mass scan into three e-cig (G6 / Juul / Blu)
reference 1: http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
reference 2: http://scikit-learn.org/stable/modules/linear_model.html#logistic-regression
newton-cg: http://www.scipy-lectures.org/advanced/mathematical_optimization/#newton-and-quasi-newton-methods
lbfgs: limited memory (https://en.wikipedia.org/wiki/Limited-memory_BFGS)
'''

import os, csv, numpy as np, matplotlib.pyplot as plt, pandas as pd
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

RANOM_STATE = 0
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
'''pca = PCA(n_components=COMPONENT_NUM, whiten=True)
pca.fit(train_data)
train_data = pca.transform(train_data)'''
clf1 = LogisticRegression(solver='newton-cg')
clf2 = LogisticRegression(solver='sag')
clf3 = LogisticRegression(solver='saga')
clf4 = LogisticRegression(solver='lbfgs')
clf1.fit(train_data, train_label)
clf2.fit(train_data, train_label)
clf3.fit(train_data, train_label)
clf4.fit(train_data, train_label)

print('Read testing data...')
with open('testing.csv', 'r') as reader:
    test_data = []
    for line in reader.readlines():
        pixels = list(map(float, line.rstrip().split(',')))
        test_data.append(pixels)
print('Loaded ' + str(len(test_data)))

print('Predicting...')
test_data = np.array(test_data)
#test_data = pca.transform(test_data)
predict1 = clf1.predict(test_data)
predict2 = clf2.predict(test_data)
predict3 = clf3.predict(test_data)
predict4 = clf4.predict(test_data)
prob = clf1.predict_proba(test_data)

# save prediction
print('Saving...')
with open('lr_predict.csv', 'w') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = 
    	['Index', 'Actual', 'Newton-cg predict', 
    	'Sag predict', 'Saga predict', 'lbfgs predict'])
    writer.writeheader()

    count = 0
    for p1, p2, p3, p4 in zip(predict1, predict2, predict3, predict4):
        writer.writerow({'Index': str(count + 1), 
        	'Actual': str(getAns(count)),
        	'Newton-cg predict': str(p1),
        	'Sag predict': str(p2),
        	'Saga predict': str(p3),
        	'lbfgs predict': str(p4)
        	})
        count += 1




