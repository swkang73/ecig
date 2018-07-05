'''day average
This file takes hourly hb measurements and 
produce into one file
'''
import csv
import numpy as np

pcIon = ['19', '30', '32', '16','17', '32','46','62']
files = ['mass-scan-pos-neg-4-13-18-4922-20180703-125755.csv',
'mass-scan-pos-neg-4-13-18-4923-20180703-131005.csv',
'mass-scan-pos-neg-4-13-18-4928-20180703-140035.csv',
'mass-scan-pos-neg-4-13-18-4929-20180703-142556.csv',
'mass-scan-pos-neg-4-13-18-4932-20180703-164247.csv',
'mass-scan-pos-neg-4-13-18-4933-20180703-171923.csv'
]

# input: file name, output: date from file name
def getDate(filename):
	return filename[31:39]

# open export file
out_file = open('p_e_' + getDate(files[0]) + '.csv', 'w')
writer = csv.writer(out_file)

# open import files
arr = []
index = 1
for file in files:
	in_file = open('p_e_' + file, 'r')
	reader = csv.reader(in_file)

	#if first file, add header 
	if file == files[0]:
		precursorIons = ['precursor ions']
		mz = ['mass to charge ratio']
		mzMeasurements = [index]
		for line in reader:
			if len(line) > 3:
				precursorIons += [line[0]]
				mz += [line[1]]
				mzMeasurements += [line[2]]
			else: 
				precursorIons += [line[0]]
				mz += [line[1]]
				mzMeasurements += ['']
		arr.append(precursorIons)
		arr.append(mz)
		arr.append(mzMeasurements)
	else:
		mzMeasurements = [index]
		for line in reader:
			if len(line) > 3: 
				mzMeasurements += [line[2]]
			else:
				mzMeasurements += ['']
		arr.append(mzMeasurements)
	index += 1

# transpose matrix
arr = np.transpose(arr)
for line in arr:
	writer.writerow(line)

out_file.close()