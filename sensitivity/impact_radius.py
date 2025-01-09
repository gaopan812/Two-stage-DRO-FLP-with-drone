import numpy as np
import pandas as pd
import sys
from pathlib import Path
from joblib import Parallel, delayed, dump
sys.path.append(str(Path(__file__).resolve().parents[1]))  # 将父级目录加入执行目录列表
from scripts.CCG_DRO_Wass import run_optimization as wassrun
def compute_for_IJ(I, J, theta, sd):
    theta = theta
    sd = sd
    temp_y, temp_z, temp_obj, temp_time = wassrun(I, J, 40, sd, 0, theta, 300)
    temp_y = temp_y.tolist()
    cost1_ = sum(temp_y) * 300
    cost2 = temp_obj - cost1_
    return theta, sd, temp_y, sum(temp_y), cost1_, cost2, temp_obj
result = Parallel(n_jobs = 6)(delayed(compute_for_IJ)(I, J, theta, sd) 
                              for I, J in zip([6, 9, 12], [3, 4, 5]) for theta in np.arange(0.5, 8.1, 0.75) for sd in range(5) )


# try:
#     with pd.ExcelWriter('sensitivity/impact_radius.xlsx', engine='openpyxl') as writer:
#         # 将每个DataFrame写入不同的工作表
#         for i in range(3):
#             result[i].to_excel(writer, sheet_name=str(i*11 + 33), index=False)
# except Exception as e:
#     print(f"Error writing to Excel: {e}")
dump(result, 'sensitivity/impact_radius.joblib')