'''human breath Artificial Neural Network selection Classifier
either add PCA / standard scaler
classifies e-cigarette mass scan into three e-cig (G6 / Juul / Blu)
reference 1: http://scikit-learn.org/stable/modules/neural_networks_supervised.html
'''

import os, csv, numpy as np, matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier

COMPONENT_NUM = 20
RANDOM_STATE = 0
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

print('Neural network training...')
train_label = np.array(train_label)
train_data = np.array(train_data)
'''scaler = StandardScaler()
scaler.fit(train_data)
train_data = scaler.transform(train_data)'''
pca = PCA(n_components=COMPONENT_NUM, whiten=True)
pca.fit(train_data)
train_data = pca.transform(train_data)
# solver suitable for small scale classifier 
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=RANDOM_STATE)
# default: clf = MLPClassifier(solver='lbfgs', random_state=RANDOM_STATE)
clf.fit(train_data, train_label)



print('Read testing data...')
with open('testing_vaporfi2.csv', 'r') as reader:
    test_data = []
    for line in reader.readlines():
        pixels = list(map(float, line.rstrip().split(',')))
        test_data.append(pixels)
print('Loaded ' + str(len(test_data)))

print('Predicting...')
test_data = np.array(test_data)
test_data = pca.transform(test_data)
#test_data = scaler.transform(test_data)
predict = clf.predict(test_data)


# save prediction
print('Saving...')
with open('vpf2_ann_pca_predict.csv', 'w') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = 
    	['Index', 'Prediction', 'Actual'])
    writer.writeheader()

    count = 0
    for p in predict:
        writer.writerow({'Index': str(count + 1), 
        	'Prediction': str(p),
        	'Actual': str(getAns(count))})
        count += 1




