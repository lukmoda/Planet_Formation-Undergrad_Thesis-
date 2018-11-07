#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import numpy as np
import matplotlib.pyplot as plt
import re
import glob

m = []
a = []
wmf = []
ecc = []
plan = []

path = '/home/lucas/Área de Trabalho/Dropbox/Lucas/USP/Hawaii/Final/Half/*.txt'
files = glob.glob(path) #lista com todos os arquivos

for name in files:
	with open(name) as arq:
		data = arq.readlines()

	data[:] = [i for i in data if i != '\n'] #tirando as quebras de linha da lista
	plan = np.append(plan, len(data)) #numero de planeta formados	

	for k in range(len(data)): #loop nas linhas de cada arquivo

		#procura substring entre duas substrings, pega so o que esta dentro, tira os whitespaces e converte pra float
		resm = float(re.search('=(.*)Earth', data[k]).group(1).replace(" ", "")) 
		resa = float(re.search('at(.*)AU', data[k]).group(1).replace(" ", ""))
		reswmf = float(re.search('of(.*)and', data[k]).group(1).replace(" ", ""))
		resecc = float(re.search('ecc(.*)', data[k]).group(1).replace(" ", ""))

      #append nos arrays finais
		m = np.append(m, resm)
		a = np.append(a, resa)
		wmf = np.append(wmf, reswmf)
		ecc = np.append(ecc, resecc)

#a = a[~np.isnan(a)]

a[np.isnan(a)] = 10.

plt.figure(1)
plt.hist(wmf, bins=50, color='blue')
plt.title('Water Mass Fraction Distribution')
plt.xlabel('Water Mass Fraction')
plt.ylabel('Frequency')

plt.figure(2)
plt.hist(wmf, bins=200, color='blue')
plt.title('Water Mass Fraction Distribution (Zoom)')
plt.xlabel('Water Mass Fraction')
plt.ylabel('Frequency')
plt.xlim([0.001, 0.003])
plt.ylim([0, 20])

plt.figure(3)
plt.hist(m, bins=50, color='green')
plt.title('Mass Distribution')
plt.xlabel('Mass (Earth Masses)')
plt.ylabel('Frequency')

plt.figure(4)
plt.hist(a, bins=50, color='black')
plt.title('Semi-major Axis Distribution')
plt.xlabel('Semi-major Axis (AU)')
plt.ylabel('Frequency')
plt.xlim([0,5])

plt.figure(5)
plt.hist(a, bins=200, color='black')
plt.title('Semi-major Axis Distribution (Zoom)')
plt.xlabel('Semi-major Axis (AU)')
plt.ylabel('Frequency')
plt.xlim([0.9, 1.6])
plt.ylim([0, 15])

plt.figure(6)
plt.hist(ecc, bins=50, color='red')
plt.title('Eccentricity Distribution')
plt.xlabel('Eccentricity')
plt.ylabel('Frequency')

plt.figure(7)
plt.hist(plan, bins=len(np.unique(plan)), color='orange')
plt.title('Number of Planets Formed Distribution')
plt.xlabel('Number of Planets')
plt.ylabel('Frequency')
plt.axvline(x=np.mean(plan), color='black')


alpha = [0.5, 1., 1.5]
avplan = [3.38, 4.12, 5.12]

plt.figure(8)
plt.plot(alpha, avplan, color='black')
plt.title('Relation Slope-Number of Planets Formed')
plt.xlabel('Slope')
plt.ylabel('Average Number of Planets Formed')

plt.show()

#for i in range(len(m)):
#	if a[i] > 1.4 and a[i] < 1.6: #and m[i] > 0.9 and m[i] < 1.1:
#		print(m[i], a[i])

g1 = 0.
g2 = 0.
g3 = 0.
g4 = 0.
g5 = 0.
g6 = 0.

#for i in range(len(m)):
#	if m[i] <= 0.05:
#		g1 = g1+1
#	elif m[i] > 0.05 and m[i] <= 0.15:
#		g2 = g2+1
#	elif m[i] > 0.15 and m[i] <= 0.7:
#		g3 = g3+1
#	elif m[i] > 0.7 and m[i] <= 0.9:
#		g4 = g4+1
#	elif m[i] > 0.9 and m[i] <= 1.1:
#		g5= g5+1
#	elif m[i] > 1.1:
#		g6 = g6+1

#for i in range(len(wmf)):
#	if wmf[i] <= 0.001:
#		g1 = g1+1
#	elif wmf[i] > 0.001 and wmf[i] <= 0.003:
#		g2 = g2+1
#	elif wmf[i] > 0.003 and wmf[i] <= 0.03:
#		g3 = g3+1
#	elif wmf[i] > 0.03 and wmf[i] < 0.05:
#		g4 = g4+1
#	elif wmf[i] == 0.05:
#		g5 = g5+1

#for i in range(len(ecc)):
#	if ecc[i] <=0.1:
#		g1 = g1+1
#	elif ecc[i] > 0.1 and ecc[i] <= 0.2:
#		g2 = g2+1
#	elif ecc[i] > 0.2:
#		g3 = g3+1

for i in range(len(a)):
	if a[i] < 0.9:
		g1 = g1+1
	elif a[i] >= 0.9 and a[i] <= 1.1:
		g2 = g2+1
	elif a[i] > 1.1 and a[i] < 1.4:
		g3 = g3+1
	elif a[i] >= 1.4 and a[i] <= 1.6:
		g4 = g4+1
	elif a[i] > 1.6 and a[i] < 2.5:
		g5 = g5+1
	elif a[i] >= 2.5:
		g6 = g6+1

print (g1/len(a)*100, g2/len(a)*100, g3/len(a)*100, g4/len(a)*100, g5/len(a)*100, g6/len(a)*100, np.mean(plan))

