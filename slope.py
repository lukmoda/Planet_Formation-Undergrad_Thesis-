import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress, pearsonr



alpha = [0.5, 1., 1.5]
avplan = [3.38, 4.12, 5.12]

slope, intercept, r_value, p_value, std_err = linregress(alpha,avplan)
mn=np.min(alpha)
mx=np.max(alpha)
x1=np.linspace(mn,mx,500)
y1=slope*x1+intercept

print(pearsonr(alpha,avplan))

#print(slope, intercept, p_value)

plt.figure(8)
plt.scatter(alpha, avplan, color='black')
plt.title('Relation Slope-Number of Planets Formed')
plt.xlabel(r'$\alpha$')
plt.ylabel('Average Number of Planets Formed')
plt.plot(x1,y1,'-r', color='red')

plt.show()
