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
plt.rcParams.update({'font.size': 14})
# 获取当前工作目录
current_dir = os.getcwd()
path = os.path.join(current_dir, 'sensitivity/impact_capacity.xlsx')
df_sp = pd.read_excel(path, sheet_name='SP')
df_wass = pd.read_excel(path, sheet_name='Wass')
df_mad = pd.read_excel(path, sheet_name='MAD')
x = np.arange(30, 61, 5)
df_sp['capacity'] = np.repeat(x, 5)
df_wass['capacity'] = np.repeat(x, 5)
df_mad['capacity'] = np.repeat(x, 5)
sp = df_sp.groupby('capacity')['cost1'].mean()
wass = df_wass.groupby('capacity')['obj'].mean()
mad = df_mad.groupby('capacity')['obj'].mean()
# 创建一个标准的图形窗口,并设置其尺寸
fig = plt.figure(figsize=(8, 6))
ax=plt.gca()
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['left'].set_linewidth(1.5)
ax.spines['right'].set_linewidth(1.5)
ax.spines['top'].set_linewidth(1.5)
plt.grid(linestyle='-.')
plt.plot(x, sp, marker = 's', markersize = 10, linewidth=2,  label='SP')
plt.plot(x, wass, marker = '^', markersize = 10, linewidth=2,  label='Wass-DRO')
plt.plot(x, mad, marker = 'v', markersize = 10, linewidth=2,  label='MAD-DRO')
plt.legend()
plt.xlabel(r'Facility capacity $U$', fontsize=18)
plt.ylabel('First stage cost', fontsize=18)

# 设置x、y轴刻度字体大小
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.savefig('sensitivity/figures/cap_mean_first.pdf', dpi=300)

plt.show()