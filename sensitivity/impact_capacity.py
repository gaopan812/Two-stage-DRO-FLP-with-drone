import numpy as np
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))  # 将父级目录加入执行目录列表
from scripts.SP import run_optimization as sprun
from scripts.CCG_DRO_Wass import run_optimization as wassrun
from scripts.MAD_DRO import run_optimization as madrun

result = {}
sd_list, y, open_num, cost1, cost2, obj, time_cost = [], [], [], [], [], [], []
for cap in np.arange(30, 61, 5):
        for sd in range(5):
                temp_y, temp_z, temp_obj, temp_time = sprun(9, 4, cap, sd, 300)
                temp_y = temp_y.tolist()
                y.append(temp_y)
                sd_list.append(sd)
                open_num.append(sum(temp_y))
                cost1_ = sum(temp_y)*300
                cost1.append(cost1_)
                cost2.append(temp_obj - cost1_)
                obj.append(temp_obj)
                time_cost.append(temp_time)
result['sd'] = sd_list
result['y'] = y
result['open_num'] = open_num
result['cost1'] = cost1
result['cost2'] = cost2
result['obj'] = obj
result['time_cost'] = time_cost
df1 = pd.DataFrame(result)
result = {}
sd_list, y, open_num, cost1, cost2, obj, time_cost = [], [], [], [], [], [], []
for cap in np.arange(30, 61, 5):
        for sd in range(5):
                temp_y, temp_z, temp_obj, temp_time = wassrun(9, 4, cap, sd, 0, 1, 300)
                temp_y = temp_y.tolist()
                y.append(temp_y)
                sd_list.append(sd)
                open_num.append(sum(temp_y))
                cost1_ = sum(temp_y)*300
                cost1.append(cost1_)
                cost2.append(temp_obj - cost1_)
                obj.append(temp_obj)
                time_cost.append(temp_time)
result['sd'] = sd_list
result['y'] = y
result['open_num'] = open_num
result['cost1'] = cost1
result['cost2'] = cost2
result['obj'] = obj
result['time_cost'] = time_cost
df2 = pd.DataFrame(result)
result = {}
sd_list, y, open_num, cost1, cost2, obj, time_cost = [], [], [], [], [], [], []
for cap in np.arange(30, 61, 5):
        for sd in range(5):
                _, temp_y, temp_z, temp_obj, temp_time = madrun(9, 4, cap, sd, 0, 300)
                temp_y = temp_y.tolist()
                y.append(temp_y)
                sd_list.append(sd)
                open_num.append(sum(temp_y))
                cost1_ = sum(temp_y)*300
                cost1.append(cost1_)
                cost2.append(temp_obj - cost1_)
                obj.append(temp_obj)
                time_cost.append(temp_time)
result['sd'] = sd_list
result['y'] = y
result['open_num'] = open_num
result['cost1'] = cost1
result['cost2'] = cost2
result['obj'] = obj
result['time_cost'] = time_cost
df3 = pd.DataFrame(result)
with pd.ExcelWriter('sensitivity/impact_capacity.xlsx', engine='openpyxl') as writer:
    # 将每个DataFrame写入不同的工作表
    df1.to_excel(writer, sheet_name='SP', index=False)
    df2.to_excel(writer, sheet_name='Wass', index=False)
    df3.to_excel(writer, sheet_name='MAD', index=False)