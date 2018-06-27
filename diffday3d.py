"""
Script for visualizing sample variability of tedlar bag breath sample 
through 3d plot
"""

import csv, matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


# imported files
diffDaySamples = ['sv_7days.csv']

# constants
h3o = '19'
no = '30'
o2 = '32'
IONS = [h3o, no, o2]
MZSTART = 15
MZEND = 400
COUNTSCALE = 10000

# get X and Y
X = np.arange(1, 7)
Y = np.arange(MZSTART, MZEND + 1)
X, Y = np.meshgrid(X, Y)

# function to add label 
# add label in y direction for max pos & neg delta
def addlabel(axis, values):
	maxPosX, maxPosY, maxPosZ = (0.0 for i in range(3))
	maxNegX, maxNegY, maxNegZ = (0.0 for i in range(3))

	# find max pos / neg delta
	y = MZSTART
	for arr in values:
		x = 1
		for val in arr:
			if val > maxPosZ:
				maxPosX = x
				maxPosY = y
				maxPosZ = val
			elif val < maxNegZ:
				maxNegX = x
				maxNegY = y
				maxNegZ = val
			x += 1
		y += 1

	poslabel = '(%d, %f)' % (maxPosY, maxPosZ)
	neglabel = '(%d, %f)' % (maxNegY, maxNegZ)
	axis.text(maxPosX, maxPosY, maxPosZ, poslabel, 'y')
	axis.text(maxNegX, maxNegY, maxNegZ, neglabel, 'y')


# get Z data
H3O, NO, O2 = ([] for i in range(3)) # Z1, Z2, Z3

for file in diffDaySamples:
	with open(file, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)

		for line in csv_reader:
			if line[0] in IONS and int(line[1]) >= MZSTART and int(line[1]) <= MZEND:
				arr = []
				for i in range(1,7):
					val = float(line[i + 2]) - float(line[2])
					arr += [val/COUNTSCALE]
				if line[0]==h3o:
					H3O.append(arr)
				elif line[0]==no:
					NO.append(arr)
				elif line[0]==o2:
					O2.append(arr)
		

# render surface 3d plot
fig = plt.figure(figsize=(10,6))
ax = fig.gca(projection='3d')

# Plot the surface.
surf = ax.plot_surface(X, Y, np.array(O2), cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
#addlabel(ax, O2)


ax.set_ylim(MZSTART, MZEND)
fig.colorbar(surf, shrink=0.5, aspect=5, pad=0.05)

ax.set_xlabel('day')
ax.set_ylabel('m/z')
ax.set_zlabel('delta count (10000)')
ax.set_title('Sample variability over 7 days for O2+', pad=30.0, fontsize=15)

plt.show()






