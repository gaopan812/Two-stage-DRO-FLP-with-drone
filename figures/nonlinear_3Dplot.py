# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 20:58:18 2024

@author: isgao
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体和字体大小  
plt.rcParams['font.family'] = 'Arial'  # 设置字体族  
plt.rcParams['font.size'] = 10  # 设置字体大小
# Make data
Weight = np.arange(0, 5, 0.1)
Distance = np.arange(0, 10, 0.2)

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
kseta = 6.85

v_t = 10
v_l = 5
v_c = 15
tau_t = 50/v_t
tau_l = 50/v_l
P_t = k1*(mtmb + Weight) * g * (v_t/2 + np.sqrt((v_t/2)**2 + ((mtmb + Weight)*g/k2**2))) + c2 * ((mtmb + Weight))**1.5
P_t0 = k1*(mtmb) * g * (v_t/2 + np.sqrt((v_t/2)**2 + (mtmb*g/k2**2))) + c2 * (mtmb*g)**1.5

pc1 = ( (mtmb + Weight)*g - c5*(v_c*np.cos(a))**2 )**2 + (c4*v_c**2)**2
P_c = (c1+c2) * ( pc1 )**0.75 + c4*(v_c)**3

pc1_0 = ( (mtmb)*g - c5*(v_c*np.cos(a))**2 )**2 + (c4*v_c**2)**2 #不携带包裹
P_c0 = (c1+c2) * ( pc1_0 )**0.75 + c4*(v_c)**3

Weight, Distance = np.meshgrid(Weight, Distance)

Z = (tau_t*P_t + 1000*Distance/v_c*P_c + tau_l*P_t + tau_t*P_t0 + 1000*Distance/v_c*P_c0 + tau_l*P_t0)/1000

# Plot the surface
fig = plt.figure(figsize=(5,4))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(Weight, Distance, Z, cmap='viridis')

ax.set_xlabel('Weight[kg]')  
ax.set_ylabel('Distance[km]')
ax.set_zlabel('Power comsunption[kJ]')
plt.subplots_adjust(top=1.0,
                    bottom=0.0,
                    left=0.02,
                    right=0.91,
                    hspace=0.165,
                    wspace=0.2)
ax.view_init(elev=12, azim=-64);
plt.show()
#plt.savefig('output.pdf', dpi=600)
plt.savefig('nonlinear_3D.pdf', dpi=600)

