import pandas as pd
import numpy as np
import time
import os
from scripts.lin_reg_power_consumption_cof import regression_power_consumption
from scripts.generate_customer_demand_data_wass import generate_customer_demand_data_wass
from scripts.generate_customer_demand_data_MAD import classification
from rsome import ro
from rsome import grb_solver as grb


def run_optimization(I, J,  U, yk, zk, Delta, sd):
    B = 1000 * 3600 / 1000  # 无人机电容量777wh
    C_l = 6  # 无人机最大荷载
    I = I
    J = J
    L = J
    sd = sd
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
    xihatsp, S = generate_customer_demand_data_wass(I, int(I/3), 10, 4, 10, sd=sd, Delta=Delta)
    event_num, counts, mu_mad, delta_mad = classification(xihatsp, I)
    model = ro.Model()
    x = model.dvar((I, J, L, event_num))

    expect = sum( (counts / S)[s] *(c * x[:, :, l, s]).sum() for l in range(L) for s in range(event_num))
    model.min(f @ yk + expect)  # objective
    # second stage
    model.st(sum(x[i, j, l, s] for i in range(I) for l in range(L)) <= U[j] * yk[j] for j in range(J) for s in range(event_num))
    model.st(sum(x[i, j, l, s] for j in range(J) for l in range(L)) >= mu_mad[s, i] for i in range(I) for s in range(event_num))
    model.st(sum(phi[i, j] * x[i, j, l, s] for i in range(I)) <= B * zk[j, l] for j in range(J) for l in range(L) for s in
             range(event_num))
    model.st(x >= 0, x <= C_l)
    start = time.time()
    model.solve(solver=grb, display=False)
    end = time.time()
    time_cost = round(end - start, 4)
    if model.solution.status == 2:
        return round(model.get(), 3), time_cost
    else:
        return '无解', time_cost


if __name__ == "__main__":
    run_optimization(6, 3, 3, 0)
