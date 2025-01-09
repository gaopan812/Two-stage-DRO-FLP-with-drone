import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

import matplotlib

# 统一设置字体
plt.rcParams["font.family"] = 'Times New Roman'
 
# 分别设置mathtext公式的正体和斜体字体
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Times New Roman'  # 用于正常数学文本
matplotlib.rcParams['mathtext.it'] = 'Times New Roman:italic'  # 用于斜体数学文本
plt.rcParams.update({'font.size': 15})

df_33 = pd.read_excel('sensitivity/impact_radius.xlsx', sheet_name='33')
df_44 = pd.read_excel('sensitivity/impact_radius.xlsx', sheet_name='44')
df_55 = pd.read_excel('sensitivity/impact_radius.xlsx', sheet_name='55')
df_66 = pd.read_excel('sensitivity/impact_radius.xlsx', sheet_name='66')
x = np.arange(0.5, 8.1, 0.75)
# 创建一个标准的图形窗口,并设置其尺寸
fig = plt.figure(figsize=(8, 6))

# plt.grid()
# plt.plot(x, df_33['cost2'], marker = '*', label='(I,J,L)=(6,3,3)')
# plt.plot(x, df_44['cost2'], marker = '^', label='(I,J,L)=(9,4,4)')
# plt.plot(x, df_55['cost2'], marker = 'v', label='(I,J,L)=(12,5,5)')
# plt.plot(x, df_66['cost2'], marker = 's', label='(I,J,L)=(15,6,6)')
# plt.legend()
# plt.xlabel(r'Radius $\theta$', fontsize=18)
# plt.ylabel('Recourse cost', fontsize=18)

# # 设置x、y轴刻度字体大小
# plt.xticks(fontsize=18)
# plt.yticks(fontsize=18)

# plt.savefig('sensitivity/figures/radius_resourse.pdf', dpi=300)
# plt.show()

plt.grid()
plt.plot(x, df_33['obj'], marker = '*', label='(I,J,L)=(6,3,3)')
plt.plot(x, df_44['obj'], marker = '^', label='(I,J,L)=(9,4,4)')
plt.plot(x, df_55['obj'], marker = 'v', label='(I,J,L)=(12,5,5)')
plt.plot(x, df_66['obj'], marker = 's', label='(I,J,L)=(15,6,6)')
plt.legend()
plt.xlabel(r'Radius $\theta$', fontsize=18)
plt.ylabel('Total cost', fontsize=18)

# 设置x、y轴刻度字体大小
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

plt.savefig('sensitivity/figures/radius_total.pdf', dpi=300)
plt.show()