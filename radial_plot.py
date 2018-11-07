#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import numpy as np
import matplotlib.pyplot as plt
import re

def radial_profile(r, alpha):
	if r > 0.67 and r < 1.33:
		res = 0.4855*pow(r, alpha)
	elif r > 1.52 and r < 2.27:
		res = 0.7831*pow(r, alpha)
	elif r > 2.61 and r < 2.91:
		res = 0.4432*pow(r, alpha)
	elif r > 2.97 and r < 3.57:
		res = 0.2655*pow(r, alpha)
	else:
		res = pow(r, alpha)
	return(res) 

def radial_profile_normal(r, alpha):
	res = pow(r, alpha)
	return(res)  

def radial_profile_auto(r, beta, alpha):
	res = (1-beta)*pow(r, alpha)
	return(res)

y = []
rstart = []
rend = []
beta = []
depR = []

x = np.linspace (0.5, 4.5, 10000)

path = '/home/lucas/Área de Trabalho/Dropbox/Lucas/USP/Hawaii/Out/memb3g1.out'

with open(path) as arq:
	data = arq.readlines()

data[:] = [i for i in data if i != '\n'] #tirando as quebras de linha da lista

for k in range(5, len(data)): #loop nas linhas do arquivo

	#procura substring entre duas substrings, pega so o que esta dentro, tira os whitespaces e converte pra float
	start = float(re.search('starting at(.*)AU and', data[k]).group(1).replace(" ", "")) 
	end = float(re.search('ending at(.*)AU with', data[k]).group(1).replace(" ", ""))
	dep = float(re.search('rate of(.*)%', data[k]).group(1).replace(" ", ""))/100
		
   #append nos arrays finais
	rstart = np.append(rstart, start)
	rend = np.append(rend, end)
	beta = np.append(beta, dep)


#zippando numa 3-upla
zipped = zip(rstart, rend, beta)

cond = False

#atualizando os valores de y
for pos in x:
	for el in zipped:
		if pos > el[0] and pos < el[1]:
			if pos in depR:
				aux = aux*el[2]
			else:
				aux = radial_profile_auto(pos, el[2], -1.5)
				y = np.append(y, aux)
				depR = np.append(depR, pos)
	if pos not in depR:
		y = np.append(y, radial_profile_normal(pos, -1.5))	

plt.figure(1)
p0 = plt.plot(x,y, lw=4, c='red')
p1 = plt.plot(x, x**-1.5, lw=4, c='green')
plt.xlabel('r(AU)')
plt.ylabel('Radial Profile')
plt.legend((p1[0], p0[0]), (r'$r^{-3/2}$', 'Depletion Zone'))
plt.show()
