from scripts.SP_test import run_optimization
import pandas as pd
import numpy as np
df1 = pd.read_excel('solutions/Wass_result.xlsx')

if __name__ == "__main__":
    # 调用函数并传入不同的参数值
    result = {}
    i = 0
    IJL, sd_list, Delta_list, theta_list, y, z, obj, time_cost = [], [], [], [], [], [], [], []
    for I, J in zip([6, 9, 12, 15], [3, 4, 5, 6]):
        for Delta in np.arange(-0.2, 0.21, 0.05):
            for theta in [0.5, 1, 2, 4, 8]:
                for sd in range(5):
                    condition1 = (df1['(I,J,L)'] == str((I, J, J)))
                    condition2 = (df1['sd'] == sd)
                    condition3 = (df1['theta'] == theta)
                    yk = eval(df1.loc[condition1 & condition2 & condition3, 'y'].values[0])
                    zk = np.array(eval(df1.loc[condition1 & condition2 & condition3, 'z'].values[0]))
                    temp_obj = run_optimization(I, J, 40, yk, zk, Delta, sd+5)
                    for item in range(len(temp_obj)):
                        IJL.append((I, J, J))
                        sd_list.append(sd+5)
                        Delta_list.append(round(Delta,2))
                        theta_list.append(theta)
                        y.append(yk)
                        z.append(zk)
                        obj.append(temp_obj[item])
                    i += 1
                    print(f'{i} tests solved')
    result['(I,J,L)'] = IJL
    result['Delta'] = Delta_list
    result['theta'] = theta_list
    result['sd'] = sd_list
    result['y'] = y
    result['z'] = z
    result['obj'] = obj
    df = pd.DataFrame(result)
    df.to_excel('solutions/Wass_test_result.xlsx', index=False)
