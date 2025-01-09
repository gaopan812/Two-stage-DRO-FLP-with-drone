# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:39:17 2024

@author: isgao
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体和字体大小  
plt.rcParams['font.family'] = 'Arial'  # 设置字体族  
plt.rcParams['font.size'] = 12  # 设置字体大小

Weight = np.arange(0, 6, 1)
Speed = np.arange(0,30,0.1)
#Distance = np.arange(1, 20, 5)
#print(len(Distance))

k1 = 0.8554
k2 = 0.3051
c1 = 2.8037
c2 = 0.3177
c4 = 0.0296
c5 = 0.0279
a = 10
g = 9.8
mtmb = 10.1
W = 1.5
mtmb = W


v_c = Speed

power_total = 500
meters = np.ones((1,len(Speed)))
for i in Weight:
    pc1 = ( (mtmb + i*0.453)*g - c5*(v_c*np.cos(a))**2 )**2 + (c4*v_c**2)**2
    P_c = (c1+c2) * ( pc1 )**0.75 + c4*(v_c)**3
    Y = power_total * 1000 /P_c*v_c
    meters = np.vstack((meters, Y))
print(meters[1:].shape)
    
fig, ax = plt.subplots(figsize=(8,6))
linestyles = ['-', '--', '-.', ':','solid', 'dashed']
for i,j in zip(Weight,linestyles):
   #print(i)
    ax.plot(Speed, meters[i+1,:], linestyle=j,linewidth=2,label=f'{i} lbs')
plt.title("Battery Capacity = 500kJ")
plt.xlabel("UNV Speed[m/s]")
plt.ylabel("UNV Range[meters]")
plt.legend(title='Payload Weight' ,loc='upper right')
plt.show()
plt.savefig('nonlinear_speed.pdf', dpi=600) 

  