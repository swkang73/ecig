"""
Script for visualizing sample variability of tedlar bag breath sample 
through bar graph visualizing mean & std deviation
"""

import csv, matplotlib.pyplot as plt, numpy as np
from matplotlib.lines import Line2D    



# imported files
diffDaySamples = ['sv_7days.csv']

sameDaySamples = ['sv_5measurements.csv']

# constants
h3o = '19'
no = '30'
o2 = '32'
SAMPLESIZE = 4
IONS = [h3o, no, o2]
MZSTART = 15
MZEND = 400
COUNTSCALE = 10000
WIDTH = 1

# get Z data and its error
H3O, NO, O2 = ([] for i in range(3)) # Z1, Z2, Z3
eH3O, eNO, eO2 = ([] for i in range(3)) 

def getstd(array, samplemean):
	std = 0.0
	for var in array:
		dev = var - samplemean
		std += dev ** 2
	return std

for file in sameDaySamples:
	with open(file, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)

		# first loop to calculate mean
		for line in csv_reader:
			if line[0] in IONS and int(line[1]) >= MZSTART and int(line[1]) <= MZEND:
				mean = 0
				arr = []
				# variability for a week 
				for i in range(1,5):
					delta = (float(line[i + 2]) - float(line[2])) / COUNTSCALE
					mean += delta
					arr.append(delta)
				mean /= SAMPLESIZE
				if line[0]==h3o:
					H3O.append(mean / SAMPLESIZE)
					eH3O.append(getstd(arr, mean) / (SAMPLESIZE - 1))
				elif line[0]==no:
					NO.append(mean / SAMPLESIZE)
					eNO.append(getstd(arr, mean) / (SAMPLESIZE - 1))
				elif line[0]==o2:
					O2.append(mean / SAMPLESIZE)
					eO2.append(getstd(arr, mean) / (SAMPLESIZE - 1))

'''for file in diffDaySamples:
	with open(file, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)

		# first loop to calculate mean
		for line in csv_reader:
			if line[0] in IONS and int(line[1]) >= MZSTART and int(line[1]) <= MZEND:
				mean = 0
				arr = []
				# variability for a week 
				for i in range(1,7):
					delta = (float(line[i + 2]) - float(line[2])) / COUNTSCALE
					mean += delta
					arr.append(delta)
				mean /= SAMPLESIZE
				if line[0]==h3o:
					H3O.append(mean / SAMPLESIZE)
					eH3O.append(getstd(arr, mean) / (SAMPLESIZE - 1))
				elif line[0]==no:
					NO.append(mean / SAMPLESIZE)
					eNO.append(getstd(arr, mean) / (SAMPLESIZE - 1))
				elif line[0]==o2:
					O2.append(mean / SAMPLESIZE)
					eO2.append(getstd(arr, mean) / (SAMPLESIZE - 1))'''

# render bar plot 
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(111)
plt.bar(np.arange(MZSTART, MZEND + 1), NO, WIDTH, color='green', yerr=eNO)

# add line
line = Line2D([MZSTART, MZEND], [0., 0.], color='green', lw=0.8)
ax.add_line(line)

ax.set_xlim(MZSTART, MZEND)
plt.xlabel('m/z')
plt.ylabel('ion counts (10000)')
plt.title('max sample variabilities among same days using O2+')
plt.show()






