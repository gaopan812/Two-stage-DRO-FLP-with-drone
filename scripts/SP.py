import os
import time
import pandas as pd
import numpy as np
from rsome import ro
from rsome import grb_solver as grb
from scripts.lin_reg_power_consumption_cof import regression_power_consumption
from scripts.generate_customer_demand_data_wass import generate_customer_demand_data_wass


def run_optimization(I, J,  U, sd, fixed_cost):
    B = 1000 * 3600 / 1000  # 无人机电容量777wh
    c_l = 6  # 无人机最大荷载
    L = J
    f = fixed_cost * np.ones(J)  # 站点的建设成本
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
    xihatsp, S = generate_customer_demand_data_wass(I, int(I/3), 10, 4, 10, sd=sd, Delta=0)
    model = ro.Model()
    y = model.dvar(J, 'B')
    z = model.dvar((J, L), 'B')
    x = model.dvar((I, J, L, S))

    expect = (1 / S) * sum((c * x[:, :, l, s]).sum() for l in range(L) for s in range(S))
    model.min(f @ y + expect)  # objective
    # first stage
    model.st(z[j, l] <= y[j] for j in range(J) for l in range(L))
    model.st(sum(z[j, l] for j in range(J)) <= 1 for l in range(L))
    # second stage
    model.st(sum(x[i, j, l, s] for i in range(I) for l in range(L)) <= U[j] * y[j] for j in range(J) for s in range(S))
    model.st(sum(x[i, j, l, s] for j in range(J) for l in range(L)) >= xihatsp[s, i] for i in range(I) for s in range(S))
    model.st(sum(phi[i, j] * x[i, j, l, s] for i in range(I)) <= B * z[j, l] for j in range(J) for l in range(L) for s in
             range(S))
    model.st(x >= 0, x <= c_l)
    start = time.time()
    model.solve(solver=grb,display=False)
    end = time.time()
    time_cost = round(end - start, 4)
    return y.get(), z.get(), round(model.get(), 3), time_cost
