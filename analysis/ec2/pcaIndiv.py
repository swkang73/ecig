'''pca comparing e-cigarettes
juul
Halo(G7)
Blu
'''

import csv, matplotlib.pyplot as plt, numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# constants
MZSTART = 15
MZEND = 400
INDEX = 1
NUMBER_OF_CIG = 3
NUMBER_OF_IONS = 8
# precursor ion list 
H3O = 19 #index 0
NO = 30 #index 1
O2 = 32 #index 2 pos, 3 neg
OH = 17 #index 4
O = 16 #index 5
NO2 = 46 #index 6
NO3 = 62 #index 7


files = [
# trial 1 
'mass-scan-pos-neg-4-13-18-4600-20180622-142124.csv', #g6
'mass-scan-pos-neg-4-13-18-4607-20180622-150245.csv', #juul
'mass-scan-pos-neg-4-13-18-4608-20180622-151114.csv', #blu
#trial 2
'mass-scan-pos-neg-4-13-18-4619-20180622-184858.csv', #g6
'mass-scan-pos-neg-4-13-18-4615-20180622-182527.csv', #juul
'mass-scan-pos-neg-4-13-18-4623-20180622-190449.csv', #blu
#trial 3
'mass-scan-pos-neg-4-13-18-4663-20180625-174200.csv', #g6
'mass-scan-pos-neg-4-13-18-4659-20180625-172435.csv', #juul
'mass-scan-pos-neg-4-13-18-4667-20180625-180620.csv', # blu
#trial 4
'mass-scan-pos-neg-4-13-18-4697-20180626-160732.csv', #g6
'mass-scan-pos-neg-4-13-18-4690-20180626-153051.csv', #juul
'mass-scan-pos-neg-4-13-18-4701-20180626-162915.csv', #blu
#trial 5
'mass-scan-pos-neg-4-13-18-4840-20180628-172915.csv', #g6
'mass-scan-pos-neg-4-13-18-4836-20180628-171152.csv', #juul
'mass-scan-pos-neg-4-13-18-4841-20180628-173842.csv', #blu
#trial 6
'mass-scan-pos-neg-4-13-18-4897-20180702-165302.csv', # g6
'mass-scan-pos-neg-4-13-18-4893-20180702-162712.csv', # juul
'mass-scan-pos-neg-4-13-18-5115-20180710-124320.csv', # blu
# trial 7
'mass-scan-pos-neg-4-13-18-5110-20180710-122638.csv', # g6
'mass-scan-pos-neg-4-13-18-5098-20180709-191303.csv', # juul
'mass-scan-pos-neg-4-13-18-5122-20180710-131215.csv' # blu
]

# comp arrays list of lists of lists
# first level: sample comp
# second level: different precursor ion measurements
comp = []

# helper functions 
# add label when in order of g6/juul/blu
def getlabel(index):
	if index % NUMBER_OF_CIG == 0:
		return 'G6 '+ str(index/3)
	elif index % NUMBER_OF_CIG == 1 :
		return 'Juul ' + str(index/3 + INDEX)
	else:
		return 'Blu ' + str(index/3 + INDEX)

def getcolor(index):
	if index % NUMBER_OF_IONS == 0:
		return 'red'
	elif index % NUMBER_OF_IONS == 1:
		return 'blue'
	elif index % NUMBER_OF_IONS == 2:
		return 'green'
	elif index % NUMBER_OF_IONS == 3:
		return 'purple'
	elif index % NUMBER_OF_IONS == 4:
		return 'orange'
	elif index % NUMBER_OF_IONS == 5:
		return 'brown'
	elif index % NUMBER_OF_IONS == 6:
		return 'olive'
	else:
		return 'magenta'

def getion(index):
	if index % NUMBER_OF_IONS == 0:
		return 'H3O+'
	elif index % NUMBER_OF_IONS == 1:
		return 'NO+'
	elif index % NUMBER_OF_IONS == 2:
		return 'O2+'
	elif index % NUMBER_OF_IONS == 3:
		return 'O2-'
	elif index % NUMBER_OF_IONS == 4:
		return 'OH-'
	elif index % NUMBER_OF_IONS == 5:
		return 'O-'
	elif index % NUMBER_OF_IONS == 6:
		return 'NO2-'
	else:
		return 'NO3-'

# import data from csv files 
for file in files:
	with open('p_e_' + file, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)
		data_H3O, data_NO, data_O2pos, data_O2neg, data_OH, data_O, data_NO2, data_NO3 = ([] for i in range(8))

		for line in csv_reader: 
			if(line[0]==str(H3O) and int(line[1]) < (MZEND + 1)):
				data_H3O.append(float(line[2]))
			elif(line[0]==str(NO) and int(line[1]) < (MZEND + 1)):
				data_NO.append(float(line[2]))
			elif(line[0]==str(O2) and int(line[1]) < (MZEND + 1)):
				if len(data_O2pos) < (MZEND - MZSTART + 1):
					data_O2pos.append(float(line[2]))
				else:
					data_O2neg.append(float(line[2]))
			elif(line[0]==str(O) and int(line[1]) < (MZEND + 1)):
				data_O.append(float(line[2]))
			elif(line[0]==str(OH) and int(line[1]) < (MZEND + 1)):
				data_OH.append(float(line[2]))
			elif(line[0]==str(NO2) and int(line[1]) < (MZEND + 1)):
				data_NO2.append(float(line[2]))
			elif(line[0]==str(NO3) and int(line[1]) < (MZEND + 1)):
				data_NO3.append(float(line[2]))

	comp.append([data_H3O, data_NO, data_O2pos, data_O2neg, data_OH, data_O, data_NO2, data_NO3])

# place to run PCA onto comp
Y = []
pca = PCA(n_components=2)

for sample in comp:
	std_sample = StandardScaler().fit_transform(sample)
	Y.append(pca.fit_transform(std_sample))

# rendering PCA data 
fig = plt.figure(figsize=(10,6))

i = INDEX
for y in Y:
	plt.scatter(y[:,0], y[:,1], marker='o', alpha=0.7, label=getlabel(i))
	i += INDEX
	
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('PCA analysis of 7 trials with more blowout processing')
plt.legend(loc=1)
plt.show()

