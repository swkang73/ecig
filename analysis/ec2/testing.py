'''File for data preprocessing script 
Convert raw ms files into testing data set 
'''
import numpy as np
import csv

# normal files
files = [
# trial 13
'mass-scan-pos-neg-4-13-18-5349-20180713-133558.csv', #g6
'mass-scan-pos-neg-4-13-18-5338-20180713-123434.csv', #juul
'mass-scan-pos-neg-4-13-18-5365-20180713-145957.csv', #blu
# trial 14
'mass-scan-pos-neg-4-13-18-5389-20180713-180718.csv', #g6
'mass-scan-pos-neg-4-13-18-5381-20180713-174608.csv', #juul
'mass-scan-pos-neg-4-13-18-5459-20180717-132436.csv', #blu
# trial 15
'mass-scan-pos-neg-4-13-18-5483-20180717-153032.csv', #g6
'mass-scan-pos-neg-4-13-18-5472-20180717-150119.csv', #juul
'mass-scan-pos-neg-4-13-18-5494-20180717-163402.csv', #blu
# trial 16
'mass-scan-pos-neg-4-13-18-5510-20180717-183911.csv', #g6
'mass-scan-pos-neg-4-13-18-5518-20180717-190359.csv', #juul
'mass-scan-pos-neg-4-13-18-5526-20180717-192615.csv', #blu
# trial 17
'mass-scan-pos-neg-4-13-18-5705-20180719-142921.csv', #g6
'mass-scan-pos-neg-4-13-18-5698-20180719-141026.csv', #juul
'mass-scan-pos-neg-4-13-18-5712-20180719-144848.csv', #blu
# trial 18
'mass-scan-pos-neg-4-13-18-5740-20180719-165941.csv', #g6
'mass-scan-pos-neg-4-13-18-5732-20180719-163750.csv', #juul
'mass-scan-pos-neg-4-13-18-5776-20180720-123822.csv', #blu
# trial 19
'mass-scan-pos-neg-4-13-18-5797-20180720-140937.csv', #g6
'mass-scan-pos-neg-4-13-18-5788-20180720-134552.csv', #juul
'mass-scan-pos-neg-4-13-18-5805-20180720-142933.csv', #blu
# trial 20
'mass-scan-pos-neg-4-13-18-5831-20180720-173328.csv', #g6
'mass-scan-pos-neg-4-13-18-5822-20180720-171116.csv', #juul
'mass-scan-pos-neg-4-13-18-5842-20180720-180147.csv' #blu
]

# Consts
IONS = ['19', '30', '32', '17', '16', '46', '62']
# precursor ion list 
H3O = 19 # index 0
NO = 30 # index 1
O2 = 32 # index 2 pos, 3 neg
OH = 17 # index 4
O = 16 # index 5
NO2 = 46 # index 6
NO3 = 62 # index 7
BEGINNING = 0 # first element 
INFOCOLS = 2 # precursor ion + m/z
MZEND = 400 # mz range max limit
# identifier 
GSIX = 1
JUUL = 2
BLU = 3

# write csv file
out_file = open('testing.csv', 'w')
writer = csv.writer(out_file)

# import normal group files
testingSet = []
for file in files:
	data = []
	with open('p_e_' + file, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)

		for line in csv_reader: 
			if line[0] in IONS and int(line[1]) < (MZEND + 1):
				data.append(float(line[INFOCOLS]))
		testingSet.append(data)

# file export
# each row total 3088 (1 label + 386 (15 to 385) * 8)
for a in testingSet:
	print(len(a))
	writer.writerow(a)
out_file.close()