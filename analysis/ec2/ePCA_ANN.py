'''E-cigarette PCA + ANN visualizes
render PCA of three e-cig (G6 / Juul / Blu) MS 
reference: https://www.kaggle.com/cyberzhg/sklearn-pca-svm/data
'''

import numpy as np, matplotlib.pyplot as plt, seaborn as sns
from matplotlib.colors import ListedColormap as LCmap
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier

COMPONENT_NUM = 2
RANOM_STATE = 0
CIGTOTAL = 3
G6, JUUL, BLU = 1, 2, 3
h = 0.02 # for mesh grid  

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
print('PCA Reduction and ANN fitting...')
train_label = np.array(train_label)
train_data = np.array(train_data)
pca = PCA(n_components=COMPONENT_NUM, whiten=True)
pca.fit(train_data)
train_data = pca.transform(train_data)

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=RANOM_STATE)
clf.fit(train_data, train_label)

# step 3: plot PCAs into 2D plot
# reference 1: https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
# ref 2: http://scikit-learn.org/0.17/auto_examples/svm/plot_iris.html

def getcolor(index):
	if index % CIGTOTAL == 0:
		return 'r'
	elif index % CIGTOTAL == 1: 
		return 'b'
	else: 
		return 'g'

def getlabel(index):
	if index  % CIGTOTAL == 0:
		return 'G6'
	elif index % CIGTOTAL == 1: 
		return 'Juul'
	else: 
		return 'Blu'

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


Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap=LCmap(('coral', 'cornflowerblue', 'olive')), alpha=0.8)
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())

# Plot also the training points
for idx, cl in enumerate(np.unique(train_label)):
	plt.scatter(train_data[train_label == cl, 0], train_data[train_label == cl, 1],
        c = LCmap(('red', 'blue', 'green'))(idx), label = getlabel(cl - 1))

plt.xlabel('1st Principal Component')
plt.ylabel('2nd Principal Component')
plt.legend(loc=1)
plt.xticks(())
plt.yticks(())
plt.title('E-cig classification of PCA + ANN up to 20 trials')

plt.show()
#fig.savefig('pca_%d_%d.png' % (i+1, j+1))

