import numpy as np
import math 
import matplotlib.pylab as plt
import random

num = 1
def radius_calc(mass): #calculates radius based on mass#
    dens = 2. #g/cm^3# 
    mass = mass * 2.e33	#converts Msun to g#
    radius = (3*mass)/(4*math.pi*dens)
    radius = np.power(radius, 1/3.)
    radius = radius * 6.68e-6 #converts cm to AU (actually is 10-14, but it wouldn't appear on the graph#				
    return radius

convert = lambda x: float(x.strip('m=') or -999) 						  #just to ignore m= string reading the file#
emb = str(raw_input("\nType the name of the file with embryo data (don't put .txt): "))
emb_data = np.genfromtxt(emb +'.txt', usecols = (0,1,2,3,4,5), skip_header=6, converters={1: convert})            #opening files and setting parameters#
m = len(emb_data)  #number of lines in table#
#plan = str(raw_input("\nType the name of the file with planetesimal data: "))
#plan_data = np.genfromtxt(plan, usecols = (0,1), skip_header=6, converters={1: convert})    
#n = len(plan_data)
print "\nType the maximum number of gaps: "
gaps = float(raw_input())
print "\nType the minimum and maximum values for the width of the gaps: "
mingap = float(raw_input())
maxgap = float(raw_input())
print "\nType the minimum and maximum values for the depletion rate (0 < beta < 1): "
betmin = float(raw_input())
betmax = float(raw_input())

mass = np.zeros(m/2)
a = np.zeros(m/2)
#aplan = np.zeros(n/2)					#initializing arrays of mass, a and e#
e = np.zeros(m/2) 
inc = np.zeros(m/2)
w = np.zeros(m/2)
om = np.zeros(m/2)
ta = np.zeros(m/2)

mass_e = np.zeros(m/2)
mass_old = np.zeros(m/2)



for i in range (0,m,2):
    mass[i/2] = emb_data[i,1]
    a[i/2] =  emb_data[i+1,0]        		   #read and allocate to arrays#
    e[i/2] = emb_data[i+1,1]
    inc[i/2] = emb_data[i+1,2] 
    w[i/2] = emb_data[i+1,3]
    om[i/2] = emb_data[i+1,4]
    ta[i/2] = emb_data[i+1,5]

#for k in range (0,m,2):
 #   aplan[k/2] =  plan_data[k+1,0]     		   #read planetesimal's positions#

mass_e = [x * 2.988e6 for x in mass]		   #converting from Msun to Mearth#
mass_old = list(mass_e)
b = np.zeros (m/2)
b = b+0.01
c = np.zeros (2000)                                 #just to plot embryos and planetesimals close to x axis...#
c = c+0.01					   
#radius = radius_calc(mass)
#x = np.zeros((360,m/2))                           #initializing matrices of x and y coordinates#
#y = np.zeros((360,m/2))

#plan = np.linspace(0.5,4.5,num=2000)            #evenly spaced list of 2000 planetesimals between 0.5 and 4.5 AU#
plan = [random.uniform(0.5, 4.5) for _ in xrange(2000)]    #random list of 2000 planetesimals between 0.5 and 4.5 AU#
     			
maxnum = 8	   			# maximum number of gaps#
gap = random.randint(1, gaps) 		#generates a random number of gaps between 1 and gaps#
width = np.zeros(gap) 			#list of widths of gaps#
position = np.zeros(gap) 		#list of inner (begin) postion of gaps#
outer = np.zeros(gap) 			#list of outer (end) position of gaps#
sumw = 0. 				#sum of the widths (must be < 4 AU)#

width[0] = random.uniform(mingap,maxgap)      #you can choose manually or using mingap and maxgap#
sumw = np.sum(width)
position[0] = random.uniform(0.5,4-maxgap)   #generating first gap with its features#
outer[0] = position[0]+width[0]

for i in range (1,gap):
    width[i] = random.uniform(mingap,maxgap)    
    sumw = np.sum(width)
    if sumw > 3.3: #close to 4 it gets weird# 
        width = width.resize(gap-i)		#resize the width and gap lists and exit loop#
	gap = gap-i
        break
    position[i] = random.uniform(0.5,4-maxgap)
    outer[i] = position[i]+width[i]
    for j in range (i,0, -1):		#compare new generated gap with each previous one#
        while outer[i]> position[j-1] and outer[i]< outer[j-1]:			#conditions of gaps within the same region of disk#
            position[i] = random.uniform(0.5,4-maxgap) 	  #generate another position and check again#
            outer[i] = position[i]+width[i]
	    	
        while position[i]>position[j-1] and position[i]<outer[j-1]:
            position[i] = random.uniform(0.5,4-maxgap) 	  #generate another position and check again#
            outer[i] = position[i]+width[i]
	    
        while position[i]>position[j-1] and outer[i]<outer[j-1]:
            position[i] = random.uniform(0.5,4-maxgap) 	  #generate another position and check again#
            outer[i] = position[i]+width[i]
	    
position = sorted(position, key=float)    		#putting in ascending order#
outer = sorted(outer, key=float) 
beta = np.zeros(gap)
for i in range (0,gap):
    beta[i] = random.uniform(betmin,betmax)    #randomly generates a beta value between betmin and betmax#
    for j in range (0, m/2):
        if a[j] > position[i] and a[j] < outer[i]:
            mass_e[j] = (1-beta[i]) * mass_e[j]	 #take out mass from each embryo that is in the depletion zone by a factor of beta#
	    mass[j] = (1-beta[i]) * mass[j] 


print '\ngaps = ', gap
print '\nwidths = ', width
print '\nsum of widths = ', sumw
print '\ninner positions = ', position
print '\nouter positions = ', outer
print '\ndepletion rates = \n', beta

#for j in range (0,m/2):
#	aux = (radius[j])/5
 #       for i in range(0,360):
  #          x[i][j] = (radius[j]*np.cos(np.deg2rad(i))) + a[j]  	#polar coordinates#
   #         y[i][j] = (radius[j]*np.sin(np.deg2rad(i)) + e[j]) + aux


#plotting# 

plt.figure(1)
plt.subplot(2,1,1)
plt.xlabel('Semimajor Axis (AU)')
plt.ylabel('Eccentricity')
plt.title('Initial Disk')
axes = plt.gca()
axes.set_xlim([0,5])
axes.set_ylim([0,0.2])
plt.scatter(a, b, s=400, edgecolors='none', color=(0.2,0.1,0.8)) #embryos#
plt.scatter(plan, c, s=30, color=(0.6,0.9,0), edgecolors='none', alpha=0.8) #planetesimals#

plt.subplot(2,2,3)
plt.xlabel('Semimajor Axis (AU)')
plt.ylabel('Earth Mass')
plt.title('Initial Disk')
axes = plt.gca()
axes.set_xlim([0,5])
axes.set_yscale('log')
axes.set_ylim([0.001,1])
plt.scatter(a, mass_old, s=50, edgecolors='none', color=(0.2,0.1,0.8)) #embryos#

plt.subplot(2,2,4)
plt.xlabel('Semimajor Axis (AU)')
plt.ylabel('Earth Mass')
plt.title('Depleted Disk')
axes = plt.gca()
axes.set_xlim([0,5])
axes.set_yscale('log')
axes.set_ylim([0.001,1])
plt.scatter(a, mass_e, s=50, edgecolors='none', color=(0.2,0.1,0.8)) #embryos#

plt.show()

#writing output file with parameters used and gaps produced#

result = open(emb+'.out','w') 
 
result.write('Number of Embryos = %s'% m)
result.write('\nNumber of Gaps = %s'% gap)
result.write('\nMinimum and Maximum width of gaps = %s'% mingap)
result.write(' and %s'% maxgap)
result.write('\nMinimum and Maximum depletion rates = %s'%betmin)
result.write (' and %s'% betmax)
result.write('\n%.2f'% sumw)
result.write(' AU has depleted material')
result.write(' (%.1f'%((sumw/4.)*100))
result.write(' % of the disk)')
result.write ('\n')
for i in range (0, gap):
    j = i+1
    result.write('\nGap number %d'% j)
    result.write(' has a width of %.2f'% (outer[i]-position[i]))
    result.write(' AU, starting at %.2f'% position[i])
    result.write(' AU and ending at %.2f'% outer[i])
    result.write(' AU')
    result.write(' with a depletion rate of %.2f'%(beta[i]*100))
    result.write(' %')

result.close() 

f = open(emb+'.in','w') 

f.write(')O+_06 Small-body initial data  (WARNING: Do not delete this line!!)')
f.write('\n) Lines beginning with ) are ignored.')
f.write('\n)---------------------------------------------------------------------')
f.write('\n style (Cartesian, Asteroidal, Cometary) = Ast')
f.write('\n epoch (in days) = 0.')
f.write('\n)---------------------------------------------------------------------')

for i in range (0, m/2):
    f.write('\n %-8s'% num)
    f.write(' m=%-10.6e'% mass[i])
    f.write('  r= 1.0000  d= 2.0000')
    f.write('\n %-10.6f'% a[i])
    f.write('%-12.7f'% e[i])
    f.write('   %-8.4f'% inc[i])
    f.write('%-10.4f'% w[i])
    f.write('%-10.4f'% om[i])
    f.write('%-10.4f'% ta[i])
    f.write(' 0  0  0')
    num = num + 1

f.close() 

