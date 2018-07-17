'''mass spectra
Visualizing ms for each precursors
ionlist below
'''
import csv
import matplotlib.pyplot as plt

files = [
'mass-scan-pos-neg-4-13-18-5235-20180712-134449.csv', #g6
'mass-scan-pos-neg-4-13-18-5229-20180712-132412.csv', #juul
'mass-scan-pos-neg-4-13-18-5250-20180712-150005.csv' #blu
]

# precursor ion list 
h3o = '19'
no = '30'
o2pos = '32'
o2neg = '32'
oh = '17'
o = '16'
no2 = '46'
no3 = '62'

# range of m/z
MZEND = 400
MZSTART = 15


def roundup(x):
	return x + x/10

# helper function to get label for ecig
def getlabel(filename):
	if filename == 'mass-scan-pos-neg-4-13-18-5235-20180712-134449.csv':
		return 'G6'
	elif filename == 'mass-scan-pos-neg-4-13-18-5229-20180712-132412.csv': #juul
		return 'Juul'
	else:
		return 'Blu'

for file in files:
	# extract files 
	X, H3O, NO, O2pos, O2neg, OH, O, NO2, NO3 = ([] for i in range(9))

	with open('p_e_' + file, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)

		for line in csv_reader:
			if(line[0]==h3o and int(line[1]) < (MZEND + 1)):
				X.append(int(line[1]))
				H3O.append(float(line[2]))
			elif(line[0]==no and int(line[1])< (MZEND + 1)):
				NO.append(float(line[2]))
			elif(line[0]==o2pos and int(line[1])< (MZEND + 1)):
				# distinguish pos and neg by the order of appearance in csv file
				if len(O2pos) < len(X):
					O2pos.append(float(line[2]))
				else:
					O2neg.append(float(line[2]))
			elif(line[0]==oh and int(line[1]) < (MZEND + 1)):
				OH.append(float(line[2]))
			elif(line[0]==o and int(line[1]) < (MZEND + 1)):
				O.append(float(line[2]))
			elif(line[0]==no2 and int(line[1]) < (MZEND + 1)):
				NO2.append(float(line[2]))
			elif(line[0]==no3 and int(line[1]) < (MZEND + 1)):
				NO3.append(float(line[2]))

	# plot H3O+ graph
	fig = plt.figure(figsize=(10,6))
	ax1 = fig.add_subplot(111)
	ylimit = roundup(max(H3O))

	ax1.plot(X, H3O, '-r')
	ax1.set_xlim([15,400])
	ax1.set_ylim([0, ylimit])
	ax1.margins(y=0)
	ax1.set_title(getlabel(file) + ' H3O+ measurement')
	ax1.set_xlabel('m/z')
	ax1.set_ylabel('ion count')
	plt.suptitle(file)
	plt.subplots_adjust(wspace=0.2, hspace=0.4)
	fig.savefig('ms_h2o_'+file+'.png')

	# plot NO+ graph
	fig = plt.figure(figsize=(10,6))
	ax2 = fig.add_subplot(111)
	ylimit = roundup(max(NO))

	ax2.plot(X, NO, '-b')
	ax2.set_xlim([15,400])
	ax2.set_ylim([0,ylimit])
	ax2.margins(y=0)
	ax2.set_title(getlabel(file) + ' NO+ measurement')
	ax2.set_xlabel('m/z')
	ax1.set_ylabel('ion count')
	plt.suptitle(file)
	plt.subplots_adjust(wspace=0.2, hspace=0.4)
	fig.savefig('ms_no_'+file+'.png')

	# plot O2+ graph
	fig = plt.figure(figsize=(10,6))
	ax3 = fig.add_subplot(111)
	ylimit = roundup(max(O2pos))

	ax3.plot(X, O2pos, '-g')
	ax3.set_xlim([15,400])
	ax3.set_ylim([0,ylimit])
	ax3.margins(y=0)
	ax3.set_title(getlabel(file) + ' O2+ measurement')
	ax3.set_xlabel('m/z')
	plt.suptitle(file)
	plt.subplots_adjust(wspace=0.2, hspace=0.4)
	fig.savefig('ms_o2pos_'+file+'.png')

	# plot O2- graph
	fig = plt.figure(figsize=(10,6))
	ax4 = fig.add_subplot(111)
	ylimit = roundup(max(O2neg))

	ax4.plot(X, O2neg, 'purple')
	ax4.set_xlim([15,400])
	ax4.set_ylim([0,ylimit])
	ax4.margins(y=0)
	ax4.set_title(getlabel(file) + ' O2- measurement')
	ax4.set_xlabel('m/z')
	plt.suptitle(file)
	plt.subplots_adjust(wspace=0.2, hspace=0.4)
	fig.savefig('ms_o2neg_'+file+'.png')

	# plot OH- graph
	fig = plt.figure(figsize=(10,6))
	ax5 = fig.add_subplot(111)
	ylimit = roundup(max(OH))

	ax5.plot(X, OH, 'orange')
	ax5.set_xlim([15,400])
	ax5.set_ylim([0,ylimit])
	ax5.margins(y=0)
	ax5.set_title(getlabel(file) + ' OH- measurement')
	ax5.set_xlabel('m/z')
	plt.suptitle(file)
	plt.subplots_adjust(wspace=0.2, hspace=0.4)
	fig.savefig('ms_oh_'+file+'.png')

	# plot O- graph
	fig = plt.figure(figsize=(10,6))
	ax6 = fig.add_subplot(111)
	ylimit = roundup(max(O))

	ax6.plot(X, O, 'brown')
	ax6.set_xlim([15,400])
	ax6.set_ylim([0,ylimit])
	ax6.margins(y=0)
	ax6.set_title(getlabel(file) + ' O- measurement')
	ax6.set_xlabel('m/z')
	plt.suptitle(file)
	plt.subplots_adjust(wspace=0.2, hspace=0.4)
	fig.savefig('ms_o_'+file+'.png')

	# plot NO2- graph
	fig = plt.figure(figsize=(10,6))
	ax7 = fig.add_subplot(111)
	ylim = roundup(max(NO2))

	ax7.plot(X, NO2, 'olive')
	ax7.set_xlim([MZSTART, MZEND])
	ax7.set_ylim([0, ylim])
	ax7.margins(y=0)
	ax7.set_title(getlabel(file) + ' NO2- measurement')
	ax7.set_xlabel('m/z')
	plt.suptitle(file)
	plt.subplots_adjust(wspace=0.2, hspace=0.4)
	fig.savefig('ms_no2_'+file+'.png')

	# plot NO3- graph
	fig = plt.figure(figsize=(10,6))
	ax8 = fig.add_subplot(111)
	ylimt = roundup(max(NO3))

	ax8.plot(X, NO3, 'magenta')
	ax8.set_xlim([MZSTART, MZEND])
	ax8.set_ylim([0, ylimt])
	ax8.margins(y=0)
	ax8.set_title(getlabel(file) + ' NO3- measurement')
	ax8.set_xlabel('m/z')
	plt.suptitle(file)
	plt.subplots_adjust(wspace=0.2, hspace=0.4)
	fig.savefig('ms_no3_'+file+'.png')

	plt.close()

