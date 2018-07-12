'''File for data preprocessing script 
Convert raw ms files into testing data set 
'''
import numpy as np
import csv

# normal files
files = [
# trial 9
'mass-scan-pos-neg-4-13-18-5187-20180711-181539.csv', #g6
'mass-scan-pos-neg-4-13-18-5198-20180711-185413.csv', #juul
'mass-scan-pos-neg-4-13-18-5204-20180711-191256.csv', #blu
# trial 10
'mass-scan-pos-neg-4-13-18-5235-20180712-134449.csv', #g6
'mass-scan-pos-neg-4-13-18-5229-20180712-132412.csv', #juul
'mass-scan-pos-neg-4-13-18-5250-20180712-150005.csv' #blu
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