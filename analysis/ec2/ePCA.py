'''E-cigarette PCA visualizes
render PCA of three e-cig (G6 / Juul / Blu) MS 
reference: https://www.kaggle.com/cyberzhg/sklearn-pca-svm/data
'''

import numpy as np, matplotlib.pyplot as plt, seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

COMPONENT_NUM = 15
CIGTOTAL = 3
G6, JUUL, BLU = 1, 2, 3

# step 1: open files
with open('training.csv', 'r') as reader:
    train_label = []
    train_data = []
    for line in reader.readlines():
        data = list(map(float, line.rstrip().split(',')))
        train_label.append(data[0])
        train_data.append(data[1:])
print('Loaded ' + str(len(train_label)))

# step 2: PCA reduction 
print('Reduction...')
train_label = np.array(train_label)
train_data = np.array(train_data)
pca = PCA(n_components=COMPONENT_NUM, whiten=True)
pca.fit(train_data)
train_data = pca.transform(train_data)

# step 3: plot explained variance ratio
# helper function to add label
'''def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.03*height,
                '%.2f' % float(height),
                ha='center', va='bottom')

fig, ax = plt.subplots(1, figsize=(13, 6))
index = np.arange(COMPONENT_NUM)
Y = np.cumsum(pca.explained_variance_ratio_)
bar_width = 0.8
opacity = 0.4

rec = ax.bar(index, Y, bar_width, alpha=opacity, color='g')
ax.set_ylim(0., 1.2)
autolabel(rec)'''

def addLineLabel(plot, values):
	i = 0
	for val in values:
		plot.annotate('%.3f' % val, xy=(i, np.log10(val + 1)), ha='center')
		i += 1

plt.semilogy(pca.explained_variance_ratio_, '--o', label='explained variance ratio_');
plt.semilogy(pca.explained_variance_ratio_.cumsum(), '--o', label='cumulative explained variance ratio_');
#plt.ylim([10^3, 1])
addLineLabel(plt, pca.explained_variance_ratio_)
addLineLabel(plt, pca.explained_variance_ratio_.cumsum())

plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')
plt.title('cumulative variance explained up to 14 trials of E-cig measurements')
plt.legend(loc=3)
plt.show()

# step 4: plot PCAs into 2D plot
# reference: https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
'''def getcolor(index):
	if index % CIGTOTAL == 0:
		return 'r'
	elif index % CIGTOTAL == 1: 
		return 'b'
	else: 
		return 'g'

def getlabel(index):
	if index % CIGTOTAL == 0:
		return 'G6'
	elif index % CIGTOTAL == 1: 
		return 'Juul'
	else: 
		return 'Blu'

for i in range(len(train_data[0]) - 1):
	for j in range(i + 1, len(train_data[0])):
		ind = 0
		fig = plt.figure(figsize=(10,6))
		
		for Y in train_data:
			if ind < 3:
				plt.scatter(Y[i], Y[j], c=getcolor(ind), marker='o', alpha=0.8, label=getlabel(ind))
			else: plt.scatter(Y[i], Y[j], c=getcolor(ind), marker='o', alpha=0.8)
			ind += 1

		plt.title('PCA components of 3 ecigs from 14 measurements')
		plt.xlabel('No. %d Principal Component' % (i + 1))
		plt.ylabel('No. %d Principal Component' % (j + 1))
		plt.legend(loc=1)
		plt.show()
		fig.savefig('pca_%d_%d.png' % (i+1, j+1))'''

# step 5: plot PCAs heatmap
'''fig = plt.figure(figsize=(16,6))
ax = sns.heatmap(pca.components_, yticklabels=range(1, COMPONENT_NUM + 1), cmap='RdBu')
ax.set_ylabel('Number of PCs')
ax.set_xlabel('Feature Column Number')
plt.title('PCA plot of three e-cig for 14 measurements')
plt.tight_layout()
plt.show()
#fig.savefig('pca_heatmap_abg_14.png')'''
