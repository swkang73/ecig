'''Validate sample size for naive bayes
This script draws empirical learning curve for predicting sample size needed to develop
learning algorithm for e-cig clasisfication

ref 1: algorithm paper 
https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/1472-6947-12-8 
'''

import csv, sys, numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB


CIGTOTAL = 3
G6 = 1
JUUL = 2
BLU = 3

# helper functions 
def getY(predicted, actual):
	if len(predicted) != len(actual):
		sys.exit("Empirical training error: number of prediction and actual label does not match")
	error = 0.
	for i in range(len(predicted)):
		if predicted[i] != actual[i]:
			error += 1.
	return ((len(predicted) - error) / len(predicted))


# step 1: see empirical learning curve 
print('Read training data...')
with open('training_all.csv', 'r') as reader:
    train_label = []
    train_data = []
    for line in reader.readlines():
        data = list(map(float, line.rstrip().split(',')))
        train_label.append(data[0])
        train_data.append(data[1:])
print('Loaded ' + str(len(train_label)))


print('Read testing data...')
with open('testing.csv', 'r') as reader:
    test_data = []
    for line in reader.readlines():
        pixels = list(map(float, line.rstrip().split(',')))
        test_data.append(pixels)
print('Loaded ' + str(len(test_data)))

print('Empirical learning curve for RF generated')
X, Y = ([] for i in range(2))

test_label = [train_label[i] for i in range(len(test_data))]
original_test_data = np.array(test_data) # same for every iteration
clf = GaussianNB()
for sample_size in range(1, len(train_label) / CIGTOTAL):
	# train with given sample size
	X.append(sample_size)
	train_subset_label = [ train_label[i] for i in range(3 * sample_size) ]
	train_subset_data = [ train_data[i] for i in range(3 * sample_size) ]
	train_subset_label = np.array(train_subset_label)
	train_subset_data = np.array(train_subset_data)
	clf.fit(train_subset_data, train_subset_label)
	
	# test the trained classifier
	predict = clf.predict(original_test_data)
	Y.append(getY(predict, test_label))

fig, ax = plt.subplots(1, figsize=(8,10))
ax.plot(X, Y)
plt.xticks(np.arange(1, len(train_label) / 3, 1.))
plt.xlabel('sample size')
plt.ylabel('accuracy')
plt.title('Empirical Gaussian NB learning curve for G6, Blu, and Juul')
plt.show()
	





