'''E-cigarette PCA + ANN visualizes
render PCA of three e-cig (G6 / Juul / Blu) MS 
reference: https://www.kaggle.com/cyberzhg/sklearn-pca-svm/data
'''

import numpy as np, matplotlib.pyplot as plt, seaborn as sns
from matplotlib.colors import ListedColormap as LCmap
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier


COMPONENT_NUM = 2
RANOM_STATE = 0
CIGTOTAL = 3
HALO, JUUL, BLU, V2 = 1, 2, 3, 4
h = 0.02 # for mesh grid  


# helper function for rendering label
def getlabel(index):
	if index  % CIGTOTAL == 0:
		return 'G6'
	elif index % CIGTOTAL == 1: 
		return 'Juul'
	elif index % CIGTOTAL == 2: 
		return 'Blu'
	else: 
		return 'V2'


def getcolor(index):
	if index % CIGTOTAL == 0:
		return 'r'
	elif index % CIGTOTAL == 1: 
		return 'g'
	elif index % CIGTOTAL == 2: 
		return 'b'
	else:
		return 'orange'


# step 1: open files
with open('training.csv', 'r') as reader:
    train_label = []
    train_data = []
    for line in reader.readlines():
        data = list(map(float, line.rstrip().split(',')))
        train_label.append(data[0])
        train_data.append(data[1:])
print('Loaded ' + str(len(train_label)))

# step 2: PCA reduction + svm
print('PCA Reduction and CLF fitting...')
train_label = np.array(train_label)
train_data = np.array(train_data)
pca = PCA(n_components=COMPONENT_NUM, whiten=True)
pca.fit(train_data)
train_data = pca.transform(train_data)

kn_clf = KNeighborsClassifier().fit(train_data, train_label)
nb_clf = GaussianNB().fit(train_data, train_label)
lr_clf = LogisticRegression(solver='lbfgs').fit(train_data, train_label)
mlp_clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=RANOM_STATE).fit(train_data, train_label)
svm_clf = SVC(random_state=RANOM_STATE).fit(train_data, train_label)

# step 3: plot PCAs into 2D plot
# reference 1: https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
# ref 2: http://scikit-learn.org/0.17/auto_examples/svm/plot_iris.html


#for i in range(len(train_data[0]) - 1):
#	for j in range(i + 1, len(train_data[0])):
ind = 0
fig = plt.figure(figsize=(10,6))

#create mesh for plotting 
# create a mesh to plot in
x_min, x_max = train_data[:,0].min() - 1, train_data[:,0].max() + 1
y_min, y_max = train_data[:,1].min() - 1, train_data[:,1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))


# title for the plots
titles = ['K-Nearest Neighbour (KN)',
	'Gaussian Naive Bayes (NB)',
	'Logistic Regression (LR)',
	'Single Vector Machine (SVM)',
	'Artificial Neuron Network (ANN)']

for i, clf in enumerate((kn_clf, nb_clf, lr_clf, svm_clf, mlp_clf)):
	# Plot the decision boundary. For that, we will assign a color to each
	# point in the mesh [x_min, m_max]x[y_min, y_max].
	plt.subplot(2, 3, i + 1)
	plt.subplots_adjust(wspace=0.4, hspace=0.4)

	print(len(np.c_[xx.ravel(), yy.ravel()]))
	Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

	# Put the result into a color plot
	Z = Z.reshape(xx.shape)
	plt.contourf(xx, yy, Z, cmap=LCmap(('coral', 'olive', 'cornflowerblue', 'yellow')), alpha=0.8)
	plt.scatter(train_data[:, 0], train_data[:, 1], c=train_label, cmap=LCmap(('red', 'green', 'blue', 'orange')))

	plt.xlabel('1st component')
	plt.ylabel('2nd component')
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	plt.xticks(())
	plt.yticks(())
	plt.title(titles[i])

plt.show()

