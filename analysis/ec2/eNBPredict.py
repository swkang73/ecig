'''E-cigarette PCA + Naive Bayes Classifier
classifies e-cigarette mass scan into three e-cig (G6 / Juul / Blu)
reference: https://www.kaggle.com/cyberzhg/sklearn-pca-svm/data
'''
import numpy as np, csv
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler 
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB



COMPONENT_NUM = 20
RANOM_STATE = 0
CIGTOTAL = 4
HALO = 1
JUUL = 2
BLU = 3
V2 = 4


def getAns(index):
    if index % CIGTOTAL != 0:
        return index % CIGTOTAL
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

print('Reduction...')
train_label = np.array(train_label)
train_data = np.array(train_data)
'''pca = PCA(n_components=COMPONENT_NUM, whiten=True)
pca.fit(train_data)
train_data = pca.transform(train_data)'''
scaler = StandardScaler()
scaler.fit(train_data)
train_data = scaler.transform(train_data)
clf1 = GaussianNB()
clf2 = MultinomialNB()
clf3 = BernoulliNB()
clf1.fit(train_data, train_label)
clf2.fit(train_data, train_label)
clf3.fit(train_data, train_label)

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
test_data = scaler.transform(test_data)
predict1 = clf1.predict(test_data)
predict2 = clf2.predict(test_data)
predict3 = clf3.predict(test_data)
prob = clf1.predict_proba(test_data)


print('Saving...')
with open('different_nb_ss_predict.csv', 'w') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = ['Index', 'Actual', 'Gaussian P', 'Multinomial P', 'Bernoulli P'])
    writer.writeheader()

    count = 0
    for p1, p2, p3 in zip(predict1, predict2, predict3):
        count += 1
        writer.writerow({'Index': str(count), 'Actual': str(getAns(count)), 
            'Gaussian P': str(p1), 'Multinomial P': str(p2), 'Bernoulli P': str(p3)})


