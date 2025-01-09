import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
import time
import os
from scripts.lin_reg_power_consumption_cof import regression_power_consumption
from scripts.generate_customer_demand_data_wass import generate_customer_demand_data_wass


class CCGOptimizationModel:
    def __init__(self, num_cus, num_fac, num_dro, num_sce, fix_cost, cap_u, trans_cost,
                 xi_bar, xi_lb, xi_hat, radius, phi_e):
        self.num_cus = num_cus
        self.num_fac = num_fac
        self.num_dro = num_dro
        self.num_sce = num_sce
        self.fix_cost = fix_cost  # 设施的建设成本
        self.cap_u = cap_u  # 设施的容量
        self.trans_cost = trans_cost  # 物品的运输成本
        self.xi_bar = xi_bar
        self.xi_hat = xi_hat
        self.xi_lb = xi_lb
        self.radius = radius
        self.phi_e = phi_e  # 能量消耗系数
        self.B = 3600  # 无人机电容量777wh
        self.C_l = 6  # 无人机最大荷载

        self.UB = np.inf
        self.LB = 0
        self.max_iter = 20
        # define master problem
        self.master_problem = gp.Model('master_problem')
        self.master_problem.Params.OutputFlag = 0
        self.master_problem.Params.LazyConstraints = 1
        self.y = self.master_problem.addMVar((self.num_fac,), vtype=GRB.BINARY, name='y')
        self.z = self.master_problem.addMVar((self.num_fac, self.num_dro), vtype=GRB.BINARY, name='z')
        self.sn = self.master_problem.addMVar((self.num_sce,), lb=0, name='sn')
        self.lamb = self.master_problem.addVar(name="lamb")
        self.master_problem.setObjective(self.fix_cost @ self.y
                                         + self.lamb * self.radius + (1 / self.num_sce) * self.sn.sum(),
                                         GRB.MINIMIZE)
        for j in range(self.num_fac):
            for l in range(self.num_dro):
                self.master_problem.addConstr(self.z[j, l] <= self.y[j])
        self.master_problem.addConstrs(self.z[:, l].sum() <= 1 for l in range(self.num_dro))
        self.master_problem.addConstr(np.sum(self.xi_bar * np.ones(self.num_cus)) <= self.cap_u @ self.y)

        # define sub problem
        self.Delta_z = np.zeros((self.num_sce, self.num_cus, self.num_cus))
        self.Delta_f = np.zeros((self.num_sce, self.num_cus, self.num_cus))
        for s in range(self.num_sce):
            self.Delta_z[s] = np.diag(self.xi_bar - self.xi_hat[s])
            self.Delta_f[s] = np.diag(self.xi_hat[s])
        self.obj = None
        self.sub_problem = gp.Model(f'sub_problem')
        self.sub_problem.Params.OutputFlag = 0
        self.pi_1 = self.sub_problem.addMVar((self.num_fac,), lb=0, name='pi_1')
        self.pi_2 = self.sub_problem.addMVar((self.num_cus,), lb=0, name='pi_2')
        self.pi_3 = self.sub_problem.addMVar((self.num_fac, self.num_dro), lb=0, name='pi_3')
        self.pi_4 = self.sub_problem.addMVar((self.num_cus, self.num_fac, self.num_dro), lb=0, name='pi_4')
        self.z_z = self.sub_problem.addMVar((self.num_cus,), vtype=GRB.BINARY, name='z_z')
        self.z_f = self.sub_problem.addMVar((self.num_cus,), vtype=GRB.BINARY, name='z_f')

        self.sub_problem.addConstrs(
            -self.pi_1[j] + self.pi_2[i] - self.phi_e[i, j] * self.pi_3[j, l] - self.pi_4[i, j, l]
            <= self.trans_cost[i, j]
            for i in range(self.num_cus) for j in range(self.num_fac) for l in range(self.num_dro))
        self.sub_problem.addConstr(self.z_z + self.z_f <= 1)

        self.delta_ = {}
        self.alpha_s = {}
        for s in range(self.num_sce):
            self.delta_[s] = self.Delta_z[s] @ self.z_z - self.Delta_f[s] @ self.z_f
            self.alpha_s[s] = self.Delta_z[s] @ self.z_z + self.Delta_f[s] @ self.z_f
        self.time_cost = None

    # define solve sub problem
    def solve_sub_problem(self, y_k, z_k, lamb_k):
        sn_obj = []
        xi_ = []
        alpha_ = []
        obj_without_s = (-(self.cap_u * y_k * self.pi_1).sum() - self.B * (z_k * self.pi_3).sum()
                        - self.C_l * self.pi_4.sum())
        for s in range(self.num_sce):
            self.obj = obj_without_s
            self.obj += self.pi_2 @ (self.xi_hat[s] + self.delta_[s]) - lamb_k * self.alpha_s[s].sum()
            self.sub_problem.setObjective(self.obj, GRB.MAXIMIZE)
            self.sub_problem.optimize()
            sn_obj.append(self.sub_problem.objval)
            xi_.append(self.xi_hat[s] + self.delta_[s].getValue())
            alpha_.append(self.delta_[s].getValue().sum())
        return sn_obj, xi_, alpha_
    # define the iterative method
    def optimize(self):
        x = {}
        iter_counter = 0
        start = time.time()
        while (self.UB - self.LB > 0.001) and (iter_counter < self.max_iter):
            self.master_problem.optimize()
            self.LB = self.master_problem.objVal
            #print(f'第{iter_counter}次迭代LB:', self.LB)
            y_k = self.y.X
            z_k = self.z.X
            lamb_k = self.lamb.X
            sn_obj, xi_, alpha_ = self.solve_sub_problem(y_k, z_k, lamb_k)
            self.UB = min(self.UB, self.fix_cost @ y_k + lamb_k * self.radius + np.mean(sn_obj))
            #print(f'第{iter_counter}次迭代UB:', self.UB)
            x[iter_counter] = self.master_problem.addMVar((self.num_sce, self.num_cus, self.num_fac, self.num_dro),
                                            lb=0, name=f'x_{iter_counter}')
            for s in range(self.num_sce):
                self.master_problem.addConstr(-x[iter_counter][s].sum(axis=0).sum(axis=1) >= -self.cap_u * self.y)
                self.master_problem.addConstr(x[iter_counter][s].sum(axis=1).sum(axis=1) >= xi_[s])
                for l in range(self.num_dro):
                    self.master_problem.addConstr(-(self.phi_e * x[iter_counter][s][:, :, l]).sum(axis=0) >=
                                                  -self.B * self.z[:, l])

                self.master_problem.addConstr(-x[iter_counter][s] >= -self.C_l)

                expr = (self.trans_cost * x[iter_counter][s].sum(2)).sum()
                self.master_problem.addConstr(expr - self.lamb * alpha_[s] <= self.sn[s])
            iter_counter += 1
        end = time.time()
        self.time_cost = round(end - start, 4)

    def return_result(self):

        return self.y.X, self.z.X, self.master_problem.objVal, self.time_cost


def run_optimization(I, J,  U, sd, delta, theta, fix_cost):
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

    # 创建实例并运行优化
    model = CCGOptimizationModel(I, J, L, S, f, U, c, 10, 0, xi_hat_sp, theta, phi)
    model.optimize()
    print(f"{I, J, L} Wass-DRO with radius {theta} solved!")
    result = model.return_result()
    return result
