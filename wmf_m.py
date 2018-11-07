import numpy as np
import matplotlib.pylab as plt
import matplotlib
from matplotlib.ticker import AutoMinorLocator
import re


convert = lambda x: float(x.strip('m=') or -999)  					#just to ignore m= string reading the file#
emb_data = np.genfromtxt('big.in', usecols = (0,1), skip_header=12, converters={1: convert})            #opening files and setting 
m = len(emb_data)  #number of lines in table#
plan_data = np.genfromtxt('small.in', usecols = (0,1), skip_header=5, converters={1: convert})            #opening files and setting 
p = len(plan_data)

#initializing arrays

for j in range (0,6):
	
	#read and allocate to arrays
	
	mass_emb = np.zeros(m/2) 			#array of embryo masses
	a_emb = np.zeros(m/2) 				#array of embryo semi-major axis
	mass_plan = np.zeros(p/2) 			#array of planetesimal masses
	a_plan = np.zeros(p/2) 				#array of planetesimal semi-major axis
	wmf_emb = np.zeros(m/2) 			#water mass fraction of embryos
	wmf_plan = np.zeros(p/2) 			#water mass fraction of planetesimals
	label_emb = np.zeros(m/2)				#color labels array
	label_plan = np.zeros(p/2)
	EMa = np.zeros(m/2) 					#array of semi-major axis at snapchot time
	EMm = np.zeros(m/2) 					#array of masses at snapchot time
	Pa = np.zeros(p/2) 					#array of semi-major axis at snapchot time (planetesimals)
	Pm = np.zeros(p/2)					#array of mass at snapchot time (planetesimals)


	if j == 1:
		ltime = 1000	
		tsnap = 1000000
	elif j == 2:
		ltime = 5000
		tsnap = 5000000
	elif j == 3:
		ltime = 50000
		tsnap = 50000000
	elif j == 4:
		ltime = 100000
		tsnap = 100000000
	elif j == 5:
		ltime = 200000
		tsnap = 200000000

	#embryos
	for i in range (0,m,2):
		 mass_emb[i/2] = emb_data[i,1]
		 a_emb[i/2] =  emb_data[i+1,0]        		  

	#planetesimals
	for i in range (0,p,2):
		 mass_plan[i/2] = plan_data[i,1]
		 a_plan[i/2] =  plan_data[i+1,0]  
	 

	#giving wmf based on semi-major axis and attributing labels

	#embryos
	for i in range (0,m/2):
		if a_emb[i] < 2.:
			wmf_emb[i] = 0. 
			label_emb[i] = 0
		elif 2. <= a_emb[i] <= 2.5:
			wmf_emb[i] = 0.001
			label_emb[i] = 1
		else:
			wmf_emb[i] = 0.05
			label_emb[i] = 2

	#planetesimals
	for i in range (0,p/2):
		if a_plan[i] < 2.:
			wmf_plan[i] = 0. 
			label_plan[i] = 0
		elif 2. <= a_plan[i] <= 2.5:
			wmf_plan[i] = 0.001
			label_plan[i] = 1
		else:
			wmf_plan[i] = 0.05
			label_plan[i] = 2
	
	if j == 0:
		plt.figure(1)
		fig, axes = plt.subplots(ncols=2, nrows=4, sharex= True, sharey=True)
		ax1 = axes[0,0]
		ax2 = axes[0,1]
		ax3 = axes[1,0]
		ax4 = axes[1,1]
		ax5 = axes[2,0]
		ax6 = axes[2,1]	
		ax7 = axes[3,0]
		ax8 = axes[3,1]	
		plt.title('')	
		plt.yscale('log')
		ax = plt.gca()
		ax.autoscale_view()
		left = .05 
		bottom = .05
		right = 1-left 
		top = 1-bottom 
		axes[0,0].set_ylabel('Mass')
		axes[1,0].set_ylabel('Mass')
		axes[2,0].set_ylabel('Mass')
		axes[2,0].set_xlabel('Semimajor Axis (AU)')
		axes[2,1].set_xlabel('Semimajor Axis (AU)')
		axes[3,0].axis('off')
		axes[3,1].axis('off')
		fig.subplots_adjust(hspace=0, wspace=0)
		#ax5.xticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
		plt.xticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5])
		ax5.xaxis.set_minor_locator(AutoMinorLocator(5))
		ax6.xaxis.set_minor_locator(AutoMinorLocator(5))
		plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=True)
		cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", "orange","blue"])
		ax1.scatter(a_emb,mass_emb, s=100, edgecolors='none', c=label_emb, cmap=cmap)
		ax1.scatter(a_plan,mass_plan, s=5, edgecolors='none', c=label_plan, cmap=cmap)
		ax1.text(right, top, '0 Myr',
        			horizontalalignment='right',
       			verticalalignment='top',
        			transform=ax1.transAxes)
		#clb = plt.colorbar(cl, orientation ='horizontal')
		#clb.set_label('Water Mass Fraction')
		#clb.set_ticks([0,max(label)/2,max(label)])
		#clb.set_ticklabels(['0','0.01','0.05'])

	#getting current semi-major axis and mass for each embryo at snapchot time

	if j !=0:
		for i in range (1,m/2+1):
			EM = np.genfromtxt('EM' + str(i) + '.aei', usecols=(1,7), skip_header=4)            #opening files and setting 
			n = len(EM) 				 #number of lines in table#
			if n >ltime:
				EMa[i-1] = EM[ltime,0]
				EMm[i-1] = EM[ltime,1]
			else:
				EMa[i-1] = 0.
				EMm[i-1] = 0.
			if EMa[i-1] >= 5.:      #excluding embryos further than 5 AU
				EMa[i-1] = np.nan

		# setting 0 values to 'nan' to avoid plotting zeros

		EMa[EMa == 0] = np.nan
		EMm[EMm == 0] = np.nan


		#updating the wmf based on the info.out file

		info = np.genfromtxt('info.out', dtype='string', delimiter=[60], skip_header=39, skip_footer=8)

		k = len(info)
		index_e = ''
		index_p = ''
		index_e2 = ''
		time = ''
		pbool = False
		count = 0

		for i in range (0,k):
	
			if re.search('JUPITER', info[i]) != None or re.search('SATURN', info[i]) != None or re.search('collided', info[i]) != None or re.search('ejected', info[i]) != None:
				continue

			for char in info[i]:
				if char.isdigit() and count < 8:
					index_e = index_e + char
				if count > 8 and count < 28:
					if char == 'P':
						pbool = True
					if char.isdigit() and pbool == True:
						index_p = index_p + char
					elif char.isdigit() and pbool == False:
						index_e2 = index_e2 + char
				if count > 30:
					if char.isdigit():
						time = time + char
				count = count + 1

			if pbool == True:
				wmf_emb[int(index_e)-1] = (mass_emb[int(index_e)-1] * wmf_emb[int(index_e)-1] + mass_plan[int(index_p)-1] * wmf_plan[int(index_p)-1]) / (mass_emb[int(index_e)-1] + mass_plan[int(index_p)-1])
				mass_emb[int(index_e)-1] = mass_emb[int(index_e)-1] + mass_plan[int(index_p)-1]
			elif pbool == False:
				if mass_emb[int(index_e)-1] > mass_emb[int(index_e2)-1]: 
					wmf_emb[int(index_e)-1] = (mass_emb[int(index_e)-1] * wmf_emb[int(index_e)-1] + mass_emb[int(index_e2)-1] * wmf_emb[int(index_e2)-1]) / (mass_emb[int(index_e)-1] + mass_emb[int(index_e2)-1])
					mass_emb[int(index_e)-1] = mass_emb[int(index_e)-1] + mass_emb[int(index_e2)-1]
				elif mass_emb[int(index_e)-1] < mass_emb[int(index_e2)-1]:
					wmf_emb[int(index_e2)-1] = (mass_emb[int(index_e2)-1] * wmf_emb[int(index_e2)-1] + mass_emb[int(index_e)-1] * wmf_emb[int(index_e)-1]) / (mass_emb[int(index_e2)-1] + mass_emb[int(index_e)-1])
					mass_emb[int(index_e2)-1] = mass_emb[int(index_e2)-1] + mass_emb[int(index_e)-1] 
	
			if int(time)/1000 >= tsnap:
				break

			index_e = ''
			index_p = ''
			index_e2 = ''	
			time = ''	
			count = 0
			pbool = False

		#atualization of labels based on new wmf

		for i in range (0,m/2):
			if wmf_emb[i] < 0.00001: 
				label_emb[i] = 0
			elif wmf_emb[i] > 0.00001 and wmf_emb[i] < 0.0001:
				label_emb[i] = 1
			elif wmf_emb[i] > 0.0001 and wmf_emb[i] < 0.001:
				label_emb[i] = 2
			elif wmf_emb[i] > 0.001 and wmf_emb[i] < 0.01:
				label_emb[i] = 3
			elif wmf_emb[i] > 0.01 and wmf_emb[i] < 0.02:
				label_emb[i] = 4
			elif wmf_emb[i] > 0.02 and wmf_emb[i] < 0.03:
				label_emb[i] = 5
			elif wmf_emb[i] > 0.03 and wmf_emb[i] < 0.05:
				label_emb[i] = 6
			else:
				label_emb[i] = 7

		for i in range (1,p/2+1):
			P = np.genfromtxt('P' + str(i) + '.aei', usecols=(1,7), skip_header=4)            #opening files and setting 
			v = len(P) 				 #number of lines in table#
			if v >ltime:
				Pa[i-1] = P[ltime,0]
				Pm[i-1] = P[ltime,1]
			else:
				Pa[i-1] = 0.
				Pm[i-1] = 0.
			if Pa[i-1] >= 5.:      #excluding embryos further than 5 AU
				Pa[i-1] = np.nan

		# setting 0 values to 'nan' to avoid plotting zeros

		Pa[Pa == 0] = np.nan
		Pm[Pm == 0] = np.nan			  		
		#plotting

		if j == 1:
			cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", (1,0.4,0.4), (1,0.5,0), "yellow", (0.25,1,0.5), "green", (0.4, 0.8, 1), "blue"])
			ax2.scatter(EMa,EMm, s=100, edgecolors='none', c=label_emb, cmap=cmap)
			ax2.scatter(Pa,Pm, s=5, edgecolors='none', c=label_plan, cmap=cmap)
			ax2.text(right, top, '10 Myr',
        			horizontalalignment='right',
       			verticalalignment='top',
        			transform=ax2.transAxes)
		elif j == 2:
			cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", (1,0.4,0.4), (1,0.5,0), "yellow", (0.25,1,0.5), "green", (0.4, 0.8, 1), "blue"])
			ax3.scatter(EMa,EMm, s=100, edgecolors='none', c=label_emb, cmap=cmap)
			ax3.scatter(Pa,Pm, s=5, edgecolors='none', c=label_plan, cmap=cmap)
			ax3.text(right, top, '50 Myr',
        			horizontalalignment='right',
       			verticalalignment='top',
        			transform=ax3.transAxes)
		elif j == 3:
			cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", (1,0.4,0.4), (1,0.5,0), "yellow", (0.25,1,0.5), "green", (0.4, 0.8, 1), "blue"])
			ax4.scatter(EMa,EMm, s=100, edgecolors='none', c=label_emb, cmap=cmap)
			ax4.scatter(Pa,Pm, s=5, edgecolors='none', c=label_plan, cmap=cmap)
			ax4.text(right, top, '500 Myr',
        			horizontalalignment='right',
       			verticalalignment='top',
        			transform=ax4.transAxes)
		elif j == 4:
			cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", (1,0.4,0.4), (1,0.5,0), "yellow", (0.25,1,0.5), "green", (0.4, 0.8, 1), "blue"])
			ax5.scatter(EMa,EMm, s=100, edgecolors='none', c=label_emb, cmap=cmap)
			ax5.scatter(Pa,Pm, s=5, edgecolors='none', c=label_plan, cmap=cmap)
			ax5.text(right, top, '1 Gyr',
        			horizontalalignment='right',
       			verticalalignment='top',
        			transform=ax5.transAxes)
		elif j == 5:
			cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", (1,0.4,0.4), (1,0.5,0), "yellow", (0.25,1,0.5), "green", (0.4, 0.8, 1), "blue"])
			cl = ax6.scatter(EMa,EMm, s=100, edgecolors='none', c=label_emb, cmap=cmap)
			ax6.scatter(Pa,Pm, s=5, edgecolors='none', c=label_plan, cmap=cmap)
			ax6.text(right, top, '2 Gyr',
        			horizontalalignment='right',
       			verticalalignment='top',
        			transform=ax6.transAxes)
			#cb_ax = fig.add_axes([0, 0, 1, 0.02])
			cb_ax = fig.add_subplot(22,1,20)
			clb = plt.colorbar(cl, cax=cb_ax, orientation ='horizontal')
			clb.set_label('Water Mass Fraction')
			clb.set_ticks([0, max(label_emb)-6, max(label_emb)-5, max(label_emb)-4, max(label_emb)-3, max(label_emb)-2, max(label_emb)-1, max(label_emb)])
			clb.set_ticklabels(['0', '0.00001', '0.0001', '0.001', '0.01','0.02', '0.03', '0.05'])


plt.show()
