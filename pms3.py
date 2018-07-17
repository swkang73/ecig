'''process mass spectra
This file clears out blown out precursor ions and its derivatives
to get measurement of sample
'''
import csv 

O2 = '32'
pcIon = ['19', '30', '32','17', '32', '16', '46', '62'] 
bwIon = {'19': ['19', '37', '45', '55', '73', '75', '93', '119', '149', '185', '241'],
'30': ['61', '91', '92', '93', '165', '185', '257'],
'32n': ['34', '50', '59', '91', '124', '125', '126', '183', '216'], #neg
'32p': ['31', '37', '44', '45', '60', '61', '93', '185', '227'], # pos
'46': ['137', '138', '139'],
'62': ['154'],
'17': ['35', '59', '89', '91', '92', '135', '183', '184', '185'],
'16': ['71', '91', '183']
}

files = [
# trial 10
'mass-scan-pos-neg-4-13-18-5235-20180712-134449.csv', #g6
'mass-scan-pos-neg-4-13-18-5229-20180712-132412.csv', #juul
'mass-scan-pos-neg-4-13-18-5250-20180712-150005.csv' #blu
]

O2POSEND = 1160

def msfilter(file): 
	in_file = open(file, 'r')
	reader = csv.reader(in_file)
	out_file = open('p_' + file, 'w')
	writer = csv.writer(out_file)

	i = 0 # to separate o2+ from o2- 
	for line in reader:
		if line[0] in pcIon and line[1] in pcIon:
			line[2] = 0.
		elif line[0] == O2:
			if i < O2POSEND:
				if line[1] in bwIon['32p']:
					line[2] = 0.
			else:
				if line[1] in bwIon['32n']:
					line[2] = 0.
		elif line[0] in pcIon and line[1] in bwIon[line[0]]:
			line[2] = 0.
		# treat O2 specially since same mass but diff blowout 
		writer.writerow(line)
		i += 1

	in_file.close()
	out_file.close()

for file in files:
	file = 'e_' + file
	msfilter(file)