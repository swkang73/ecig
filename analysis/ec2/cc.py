"""
Edited by sun woo kang for use on e-cig classification
==============================
Probability Calibration curves
==============================

When performing classification one often wants to predict not only the class
label, but also the associated probability. This probability gives some
kind of confidence on the prediction. This example demonstrates how to display
how well calibrated the predicted probabilities are and how to calibrate an
uncalibrated classifier.

The experiment is performed on an artificial dataset for binary classification
with 100.000 samples (1.000 of them are used for model fitting) with 20
features. Of the 20 features, only 2 are informative and 10 are redundant. The
first figure shows the estimated probabilities obtained with logistic
regression, Gaussian naive Bayes, and Gaussian naive Bayes with both isotonic
calibration and sigmoid calibration. The calibration performance is evaluated
with Brier score, reported in the legend (the smaller the better). One can
observe here that logistic regression is well calibrated while raw Gaussian
naive Bayes performs very badly. This is because of the redundant features
which violate the assumption of feature-independence and result in an overly
confident classifier, which is indicated by the typical transposed-sigmoid
curve.

Calibration of the probabilities of Gaussian naive Bayes with isotonic
regression can fix this issue as can be seen from the nearly diagonal
calibration curve. Sigmoid calibration also improves the brier score slightly,
albeit not as strongly as the non-parametric isotonic regression. This can be
attributed to the fact that we have plenty of calibration data such that the
greater flexibility of the non-parametric model can be exploited.

The second figure shows the calibration curve of a linear support-vector
classifier (LinearSVC). LinearSVC shows the opposite behavior as Gaussian
naive Bayes: the calibration curve has a sigmoid curve, which is typical for
an under-confident classifier. In the case of LinearSVC, this is caused by the
margin property of the hinge loss, which lets the model focus on hard samples
that are close to the decision boundary (the support vectors).

Both kinds of calibration can fix this issue and yield nearly identical
results. This shows that sigmoid calibration can deal with situations where
the calibration curve of the base classifier is sigmoid (e.g., for LinearSVC)
but not where it is transposed-sigmoid (e.g., Gaussian naive Bayes).
"""

# Author: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#         Jan Hendrik Metzen <jhm@informatik.uni-bremen.de>
# License: BSD Style.

import matplotlib.pyplot as plt, numpy as np

# prob
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
# preprocessing
from sklearn.preprocessing import StandardScaler 
from sklearn.decomposition import PCA
# classifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
# assess calibration 
from sklearn.metrics import (brier_score_loss, precision_score, recall_score,
                             f1_score)
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
#from sklearn.model_selection import train_test_split

RANDOM_STATE = 0
COMPONENT_NUM = 20
CIGTOTAL = 3
# convert to binary
G6 = 1 # true - 1
JUUL = 2 # false - 0
BLU = 3 # false - 0

# helper function that accepts list of prob list and return list of prob of right classification
def get_binary_prob(prob):
    binary_prob = []
    for i in range(len(prob)):
        binary_prob.append(float(prob[i][0]))
    return binary_prob

# helper function that converts e-cig classification (G6 / Juul / Blu) into binary classiciation (right / wrong)
def get_binary_ylabel(label):
    new_y = []
    print('ecig y value converted')
    for i, y in enumerate(label):
        if i % CIGTOTAL == 0:
            new_y.append(1) # right classification 
        else: new_y.append(0)
    return new_y


# Create dataset of classification task with many redundant and few
# informative features
with open('training.csv', 'r') as reader:
    train_label = []
    train_data = []
    for line in reader.readlines():
        data = list(map(float, line.rstrip().split(',')))
        train_label.append(data[0])
        train_data.append(data[1:])

print('Read testing data...')
with open('testing.csv', 'r') as reader:
    test_data = []
    for line in reader.readlines():
        pixels = list(map(float, line.rstrip().split(',')))
        test_data.append(pixels)

# get X_train, X_test, y_train, y_test
raw_X_train, raw_X_test = np.array(train_data), np.array(test_data)
# pca 
pca = PCA(n_components=COMPONENT_NUM, whiten=True)
pca.fit(raw_X_train)
pca_X_train, pca_X_test = pca.transform(raw_X_train), pca.transform(raw_X_test) 
# standard scaler
scaler = StandardScaler()
scaler.fit(raw_X_train)
scaled_X_train, scaled_X_test = scaler.transform(raw_X_train), scaler.transform(raw_X_test) 


y_train = np.array(train_label)
y_test = []
for index in range(len(test_data)):
    if (index + 1) % CIGTOTAL != 0:
        y_test.append((index + 1) % CIGTOTAL)
    else:
        y_test.append(BLU)  

f = open('ml_alg_comparison.txt', 'a')
def plot_calibration_curve(X_train, X_test, clf, name, fig_index, axis_1, axis_2):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    prob_pos = get_binary_prob(clf.predict_proba(X_test))
    y_test_label = get_binary_ylabel(y_test)


    clf_score = brier_score_loss(y_test_label, prob_pos, pos_label=1)
    f.write("%s:" % name)
    f.write("\tBrier: %1.3f" % (clf_score))
    f.write("\tPrecision: %1.3f" % precision_score(y_test, y_pred, average='macro'))
    f.write("\tRecall: %1.3f" % recall_score(y_test, y_pred, average='macro'))
    f.write("\tF1: %1.3f\n" % f1_score(y_test, y_pred, average='macro'))

    fraction_of_positives, mean_predicted_value = \
        calibration_curve(y_test_label, prob_pos, n_bins=10)

    axis_1.plot(mean_predicted_value, fraction_of_positives, "s-",
             label="%s (%1.3f)" % (name, clf_score))

    axis_2.hist(prob_pos, range=(0, 1), bins=10, label=name,
             histtype="step", lw=2)



# main drawing scripts
fig = plt.figure(figsize=(10, 10))
ax1 = plt.subplot2grid((3, 1), (0, 0), rowspan=2)
ax2 = plt.subplot2grid((3, 1), (2, 0))
ax1.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")

# Plot calibration curve for Gaussian naive bayes
plot_calibration_curve(pca_X_train, pca_X_test, LogisticRegression(solver='lbfgs'), "PCA + LR", 1, ax1, ax2)

# plot calibration curve for SS + artificial neural network 
plot_calibration_curve(scaled_X_train, scaled_X_test, MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=RANDOM_STATE), "SS + ANN", 2, ax1, ax2)

# Plot calibration curve for PCA + rbf SVC
plot_calibration_curve(pca_X_train, pca_X_test, SVC(random_state=RANDOM_STATE, probability=True), "PCA + SVC", 3, ax1, ax2)

# Plot calibration curve for random forest
plot_calibration_curve(raw_X_train, raw_X_test, RandomForestClassifier(max_features='sqrt', n_jobs=2, random_state=RANDOM_STATE), "Random Forest", 4, ax1, ax2)

# Plot calibration curve for k nearest neighbours
plot_calibration_curve(raw_X_train, raw_X_test, KNeighborsClassifier(), "k-NN", 5, ax1, ax2)

# Plot calibration curve for Gaussian naive bayes
plot_calibration_curve(pca_X_train, pca_X_test, GaussianNB(), "Gaussian NB", 6, ax1, ax2)

f.close()

ax1.set_ylabel("Fraction of positives")
ax1.set_ylim([-0.05, 1.05])
ax1.legend(loc="lower right")
ax1.set_title('Calibration plots  (reliability curve)')

ax2.set_xlabel("Mean predicted value")
ax2.set_ylabel("Count")
ax2.legend(loc="upper center", ncol=3)

#plt.tight_layout()
plt.show()

