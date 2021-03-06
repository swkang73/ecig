'''Endometriosis Classifier
reference: https://www.kaggle.com/cyberzhg/sklearn-pca-svm/data
'''
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC

COMPONENT_NUM = 10

print('Read training data...')
with open('training.csv', 'r') as reader:
    train_label = []
    train_data = []
    for line in reader.readlines():
        data = list(map(float, line.rstrip().split(',')))
        train_label.append(data[0])
        train_data.append(data[1:])
print('Loaded ' + str(len(train_label)))

print('Reduction...')
train_label = np.array(train_label)
train_data = np.array(train_data)
pca = PCA(n_components=COMPONENT_NUM, whiten=True)
pca.fit(train_data)
train_data = pca.transform(train_data)

print('Train SVM...')
svc = SVC()
svc.fit(train_data, train_label)

print('Read testing data...')
with open('testing.csv', 'r') as reader:
    test_data = []
    for line in reader.readlines():
        pixels = list(map(float, line.rstrip().split(',')))
        test_data.append(pixels)
print('Loaded ' + str(len(test_data)))

print('Predicting...')
test_data = np.array(test_data)
test_data = pca.transform(test_data)
predict = svc.predict(test_data)

print('Saving...')
with open('predict.csv', 'w') as writer:
    writer.write('"Index","Label"\n')
    count = 0
    for p in predict:
        count += 1
        writer.write(str(count) + ',"' + str(p) + '"\n')

