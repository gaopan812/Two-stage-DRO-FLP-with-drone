# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:37:24 2024

@author: isgao
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体和字体大小  
plt.rcParams['font.family'] = 'Arial'  # 设置字体族  
plt.rcParams['font.size'] = 11  # 设置字体大小
# Make data
Weight = np.arange(0, 6, 0.2)
Distance = np.arange(1, 15, 3)
#Distance = 19.409464
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





fig, ax = plt.subplots(figsize=(8,6))
ydata = np.ones((1,len(Weight)))
for i in range(len(Distance)):
   #print(i)
   Z = (tau_t*P_t + 1000*Distance[i]/v_c*P_c + tau_l*P_t + tau_t*P_t0 + 1000*Distance[i]/v_c*P_c0 + tau_l*P_t0)/1000
   ydata = np.vstack((ydata,Z))
   ax.scatter(Weight, Z,label=f'{Distance[i]} km')

# =============================================================================
# 线性回归
# =============================================================================

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
for i in range(len(Distance)):
    X = Weight
    y = ydata[1:][i]
    #print(y)
    X_train, X_test, y_train, y_test = train_test_split(X.reshape(-1, 1), y.reshape(-1, 1), test_size=0.2,random_state=2024)
    model = LinearRegression(fit_intercept=False)
    model.fit(X_train, y_train)
    #print(model.coef_[0,0])
# # Predict Z values
    y_pred = model.predict(X.reshape(-1,1))
    #print(model.score(X_train,y_train))
    print(model.score(X_test,y_test))
# # Plot the surface
    ax.plot(Weight, y_pred)
    #print(model.coef_)
# # 获取截距和系数
# intercept = model.intercept_
# coefficients = 

# # 输出线性回归方程
# print("Linear Regression Equation:")
# equation = f"y = {intercept}"
# for i, coef in enumerate(coefficients):
#     equation += f" + {coef} * x{i+1}"
# print(equation)

ax.set_xlabel('Weight[kg]')  
ax.set_ylabel('Power comsunption[kJ]')
plt.legend()
plt.show()
#plt.savefig('output.pdf', dpi=600)
#plt.savefig('powerregresssion2.pdf', dpi=600)