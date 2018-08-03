'''mass spectra
Visualizing ms for each precursors
ionlist below
'''
import csv
import matplotlib.pyplot as plt


V2 = [
'mass-scan-pos-neg-4-13-18-5923-20180726-131606.csv',
'mass-scan-pos-neg-4-13-18-5930-20180726-140538.csv',
'mass-scan-pos-neg-4-13-18-5938-20180726-145530.csv',
'mass-scan-pos-neg-4-13-18-5955-20180726-173918.csv',
'mass-scan-pos-neg-4-13-18-5970-20180727-124102.csv',
'mass-scan-pos-neg-4-13-18-5976-20180727-133614.csv',
'mass-scan-pos-neg-4-13-18-5982-20180727-143114.csv',
'mass-scan-pos-neg-4-13-18-5989-20180727-171215.csv',
'mass-scan-pos-neg-4-13-18-5994-20180727-174923.csv',
'mass-scan-pos-neg-4-13-18-6013-20180730-165438.csv',
'mass-scan-pos-neg-4-13-18-6017-20180730-171128.csv',
'mass-scan-pos-neg-4-13-18-6022-20180730-174656.csv',
'mass-scan-pos-neg-4-13-18-6030-20180730-182346.csv',
'mass-scan-pos-neg-4-13-18-6036-20180730-191118.csv',
'mass-scan-pos-neg-4-13-18-6040-20180730-195810.csv',
'mass-scan-pos-neg-4-13-18-6058-20180731-142515.csv',
'mass-scan-pos-neg-4-13-18-6062-20180731-160941.csv',
'mass-scan-pos-neg-4-13-18-6067-20180731-192220.csv',
'mass-scan-pos-neg-4-13-18-6073-20180731-195437.csv',
'mass-scan-pos-neg-4-13-18-6077-20180731-202749.csv'
]

Halo = [
'mass-scan-pos-neg-4-13-18-4600-20180622-142124.csv', # halo
'mass-scan-pos-neg-4-13-18-4619-20180622-184858.csv', # halo
'mass-scan-pos-neg-4-13-18-4663-20180625-174200.csv', # halo
'mass-scan-pos-neg-4-13-18-4697-20180626-160732.csv',# halo
'mass-scan-pos-neg-4-13-18-4840-20180628-172915.csv', # halo
'mass-scan-pos-neg-4-13-18-4897-20180702-165302.csv', # halo
'mass-scan-pos-neg-4-13-18-5110-20180710-122638.csv', # halo
'mass-scan-pos-neg-4-13-18-5166-20180711-143331.csv', # halo
'mass-scan-pos-neg-4-13-18-5187-20180711-181539.csv', # halo
'mass-scan-pos-neg-4-13-18-5235-20180712-134449.csv', #halo
'mass-scan-pos-neg-4-13-18-5265-20180712-172235.csv', #halo
'mass-scan-pos-neg-4-13-18-5305-20180712-200505.csv' #halo
]

Juul = [
'mass-scan-pos-neg-4-13-18-4607-20180622-150245.csv', # juul
'mass-scan-pos-neg-4-13-18-4615-20180622-182527.csv', # juul
'mass-scan-pos-neg-4-13-18-4659-20180625-172435.csv', # juul
'mass-scan-pos-neg-4-13-18-4690-20180626-153051.csv', #juul
'mass-scan-pos-neg-4-13-18-4836-20180628-171152.csv', # juul
'mass-scan-pos-neg-4-13-18-4893-20180702-162712.csv', # juul
'mass-scan-pos-neg-4-13-18-5098-20180709-191303.csv', # juul
'mass-scan-pos-neg-4-13-18-5160-20180711-141428.csv', # juul 
'mass-scan-pos-neg-4-13-18-5198-20180711-185413.csv', #juul
'mass-scan-pos-neg-4-13-18-5229-20180712-132412.csv', #juul
'mass-scan-pos-neg-4-13-18-5274-20180712-174609.csv', #juul
'mass-scan-pos-neg-4-13-18-5297-20180712-194355.csv' #juul
]

Blu = [
'mass-scan-pos-neg-4-13-18-4608-20180622-151114.csv', # blu
'mass-scan-pos-neg-4-13-18-4667-20180625-180620.csv', # blu
'mass-scan-pos-neg-4-13-18-4701-20180626-162915.csv', # blu
'mass-scan-pos-neg-4-13-18-4841-20180628-173842.csv', # blu
'mass-scan-pos-neg-4-13-18-5115-20180710-124320.csv', # blu
'mass-scan-pos-neg-4-13-18-5122-20180710-131215.csv', # blu
'mass-scan-pos-neg-4-13-18-5171-20180711-145222.csv', # blu
'mass-scan-pos-neg-4-13-18-5204-20180711-191256.csv', #blu
'mass-scan-pos-neg-4-13-18-5250-20180712-150005.csv', #blu
'mass-scan-pos-neg-4-13-18-4623-20180622-190449.csv', # blu
'mass-scan-pos-neg-4-13-18-5288-20180712-191958.csv', #blu
'mass-scan-pos-neg-4-13-18-5313-20180712-202745.csv' #blu
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
	if filename in V2:
		return 'V2'
	elif filename in Juul:
		return 'Juul'
	elif filename in Blu:
		return 'Blu'
	else:
		return 'Halo'

def average(values):
	v_avg = []
	for v in values:
		v_avg.append(v/len(Blu))
	return v_avg


X, H3O, NO, O2pos, O2neg, OH, O, NO2, NO3 = ([] for i in range(9))
i = 0
# add everything up 
for file in Halo:
	# extract files 

	with open('ms/p_e_' + file, 'r') as csv_file:
		csv_reader = csv.reader(csv_file)

		if i == 0:
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

		else:
			for line in enumerate(csv_reader):
				if(line[0]==h3o and int(line[1]) < (MZEND + 1)):
					index = int(line[1]) - MZSTART
					H3O[index] += float(line[2])
				elif(line[0]==no and int(line[1])< (MZEND + 1)):
					index = int(line[1]) - MZSTART
					NO[index] += float(line[2])
				elif(line[0]==o2pos and int(line[1])< (MZEND + 1)):
					# distinguish pos and neg by the order of appearance in csv file
					if len(O2pos) < len(X):
						index = int(line[1]) - MZSTART
						O2pos[index] += float(line[2])
					else:
						index = int(line[1]) - MZSTART
						O2neg[index] += float(line[2])
				elif(line[0]==oh and int(line[1]) < (MZEND + 1)):
					index = int(line[1]) - MZSTART
					OH[index] += float(line[2])
				elif(line[0]==o and int(line[1]) < (MZEND + 1)):
					index = int(line[1]) - MZSTART
					O[index] += float(line[2])
				elif(line[0]==no2 and int(line[1]) < (MZEND + 1)):
					index = int(line[1]) - MZSTART
					NO2[index] += float(line[2])
				elif(line[0]==no3 and int(line[1]) < (MZEND + 1)):
					index = int(line[1]) - MZSTART
					NO3[index] += float(line[2])

	i += 1


H3O = average(H3O)
NO = average(NO)
O2pos = average(O2pos)
O2neg = average(O2neg)
OH = average(OH)
O = average(O)
NO2 = average(NO2)
NO3 = average(NO3)

# plot H3O+ graph
fig = plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(111)
ylimit = roundup(max(H3O))

ax1.plot(X, H3O, '-r')
ax1.set_xlim([15,400])
ax1.set_ylim([0, ylimit])
ax1.margins(y=0)
ax1.set_title(getlabel(file) + ' H3O+ average MS')
ax1.set_xlabel('m/z')
ax1.set_ylabel('ion count')
plt.subplots_adjust(wspace=0.2, hspace=0.4)
fig.savefig('ms_h2o_Halo.png')

# plot NO+ graph
fig = plt.figure(figsize=(10,6))
ax2 = fig.add_subplot(111)
ylimit = roundup(max(NO))

ax2.plot(X, NO, '-b')
ax2.set_xlim([15,400])
ax2.set_ylim([0,ylimit])
ax2.margins(y=0)
ax2.set_title(getlabel(file) + ' NO+ average MS')
ax2.set_xlabel('m/z')
ax1.set_ylabel('ion count')
plt.subplots_adjust(wspace=0.2, hspace=0.4)
fig.savefig('ms_no_Halopng')

# plot O2+ graph
fig = plt.figure(figsize=(10,6))
ax3 = fig.add_subplot(111)
ylimit = roundup(max(O2pos))

ax3.plot(X, O2pos, '-g')
ax3.set_xlim([15,400])
ax3.set_ylim([0,ylimit])
ax3.margins(y=0)
ax3.set_title(getlabel(file) + ' O2+ average MS')
ax3.set_xlabel('m/z')
plt.subplots_adjust(wspace=0.2, hspace=0.4)
fig.savefig('ms_o2pos_Halo.png')

# plot O2- graph
fig = plt.figure(figsize=(10,6))
ax4 = fig.add_subplot(111)
ylimit = roundup(max(O2neg))

ax4.plot(X, O2neg, 'purple')
ax4.set_xlim([15,400])
ax4.set_ylim([0,ylimit])
ax4.margins(y=0)
ax4.set_title(getlabel(file) + ' O2- average MS')
ax4.set_xlabel('m/z')
plt.subplots_adjust(wspace=0.2, hspace=0.4)
fig.savefig('ms_o2neg_Halo.png')

# plot OH- graph
fig = plt.figure(figsize=(10,6))
ax5 = fig.add_subplot(111)
ylimit = roundup(max(OH))

ax5.plot(X, OH, 'orange')
ax5.set_xlim([15,400])
ax5.set_ylim([0,ylimit])
ax5.margins(y=0)
ax5.set_title(getlabel(file) + ' OH- average MS')
ax5.set_xlabel('m/z')
plt.subplots_adjust(wspace=0.2, hspace=0.4)
fig.savefig('ms_oh_Halo.png')

# plot O- graph
fig = plt.figure(figsize=(10,6))
ax6 = fig.add_subplot(111)
ylimit = roundup(max(O))

ax6.plot(X, O, 'brown')
ax6.set_xlim([15,400])
ax6.set_ylim([0,ylimit])
ax6.margins(y=0)
ax6.set_title(getlabel(file) + ' O- average MS')
ax6.set_xlabel('m/z')
plt.subplots_adjust(wspace=0.2, hspace=0.4)
fig.savefig('ms_o_Halo.png')

# plot NO2- graph
fig = plt.figure(figsize=(10,6))
ax7 = fig.add_subplot(111)
ylim = roundup(max(NO2))

ax7.plot(X, NO2, 'olive')
ax7.set_xlim([MZSTART, MZEND])
ax7.set_ylim([0, ylim])
ax7.margins(y=0)
ax7.set_title(getlabel(file) + ' NO2- average MS')
ax7.set_xlabel('m/z')
plt.subplots_adjust(wspace=0.2, hspace=0.4)
fig.savefig('ms_no2_Halo.png')

# plot NO3- graph
fig = plt.figure(figsize=(10,6))
ax8 = fig.add_subplot(111)
ylimt = roundup(max(NO3))

ax8.plot(X, NO3, 'magenta')
ax8.set_xlim([MZSTART, MZEND])
ax8.set_ylim([0, ylimt])
ax8.margins(y=0)
ax8.set_title(getlabel(file) + ' NO3- average MS')
ax8.set_xlabel('m/z')
plt.subplots_adjust(wspace=0.2, hspace=0.4)
fig.savefig('ms_no3_Halo.png')

plt.close()
