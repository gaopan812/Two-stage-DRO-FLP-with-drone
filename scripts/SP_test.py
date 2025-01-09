import pandas as pd
import numpy as np
import time
import os
from scripts.lin_reg_power_consumption_cof import regression_power_consumption
from scripts.generate_customer_demand_data_wass import generate_customer_demand_data_wass
from rsome import ro
from rsome import grb_solver as grb


def run_optimization(I, J,  U, yk, zk, Delta, sd):
    B = 3600  # 无人机电容量777wh
    C_l = 6  # 无人机最大荷载
    L = J
    f = 300 * np.ones(J)  # 站点的建设成本
    U = U * np.ones(J)  # 站点的容量

    # 定义数据路径
    data_path = "data/distances"

    # 构建文件路径
    file_path = os.path.join(data_path, f"f{J}_c{I}_distance.csv")

    try:
        distances = pd.read_csv(file_path, index_col=0)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {file_path} - {e}")
    c = 5 * distances.values.T
    phi = regression_power_consumption(J, I, distances)
    xihatsp, S = generate_customer_demand_data_wass(I, int(I/3), 10, 4, 20, sd=sd, Delta=Delta)
    obj_list = []
    for s in range(S):
        model = ro.Model()
        x = model.dvar((I, J, L))
        cost2 = sum((c * x[:, :, l]).sum() for l in range(L))
        model.min(f @ yk + cost2)  # objective
        # second stage
        model.st(sum(x[i, j, l] for i in range(I) for l in range(L)) <= U[j] * yk[j] for j in range(J) )
        model.st(sum(x[i, j, l] for j in range(J) for l in range(L)) >= xihatsp[s, i] for i in range(I) )
        model.st(sum(phi[i, j] * x[i, j, l] for i in range(I)) <= B * zk[j, l] for j in range(J) for l in range(L))
        model.st(x >= 0, x <= C_l)
        model.solve(solver=grb, display=False)
        if model.solution.status == 2:
            obj_list.append(round(model.get(), 3))
        else:
            obj_list.append('无解')
    return obj_list
