import pandas as pd
import numpy as np
import time
import os
from scripts.lin_reg_power_consumption_cof import regression_power_consumption
from scripts.generate_customer_demand_data_wass import generate_customer_demand_data_wass
from scripts.generate_customer_demand_data_MAD import classification
from rsome import ro
from rsome import grb_solver as grb



def run_optimization(I, J, U, sd, delta, fix_cost):
    B = 1000 * 3600 / 1000  # 无人机电容量777wh
    C_l = 6  # 无人机最大荷载
    I = I
    J = J
    L = J
    sd = sd
    f = fix_cost * np.ones(J)  # 站点的建设成本
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
    xi_hat_sp, S = generate_customer_demand_data_wass(I, int(I/3), 10, 4, 10, sd=sd, Delta=delta)
    event_num, counts, mu_mad, delta_mad = classification(xi_hat_sp, I)
    start = time.time()
    model = ro.Model()
    xi = model.rvar(I)
    u = model.rvar(I)

    y = model.dvar(J, 'B')
    z = model.dvar((J, L), 'B')
    a = model.dvar(event_num)
    pi_1 = model.dvar((I, event_num))
    pi_2 = model.dvar((I, event_num))
    x = model.ldr((event_num, I, J, L))
    x.adapt(xi)  # x affinely adapts to xi
    x.adapt(u)  # x affinely adapts to u

    model.min(f @ y + a.sum() + sum(pi_1[:, s] @ mu_mad[s] + pi_2[:, s] @ delta_mad[s] for s in range(event_num)))
    # first stage
    model.st(z[:, l] <= y for l in range(L))
    model.st(sum(z[j, l] for j in range(J)) <= 1 for l in range(L))
    # second stage
    for s in range(event_num):
        Wset = (xi >= 0, xi <= 10, abs(xi - mu_mad[s]) <= u)
        model.st((a[s] + pi_1[:, s] @ xi + pi_2[:, s] @ u >=
                  (counts /S)[s] * sum((c * x[s, :, :, l]).sum() for l in range(L))).forall(Wset))
        model.st((sum(x[s, i, :, l] for i in range(I) for l in range(L)) <= U * y).forall(Wset))
        model.st((sum(x[s, :, j, l] for j in range(J) for l in range(L)) >= xi).forall(Wset))
        for l in range(L):
            model.st(((phi * x[s, :, :, l]).sum(axis=0) <= B * z[:, l]).forall(Wset))
        model.st((x[s] >= 0).forall(Wset))
        model.st((x[s] <= C_l).forall(Wset))
    model.solve(solver=grb, display=False)
    print('MAD-DRO solved!')
    end = time.time()
    time_cost = round(end - start, 4)
    return event_num, y.get(), z.get(), round(model.get(), 3), time_cost

