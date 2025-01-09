from scripts.CCG_DRO_Wass import run_optimization
import pandas as pd

if __name__ == "__main__":
    # 调用函数并传入不同的参数值
    result = {}
    i = 0
    IJL, y, z, theta_list, sd_list, obj, time_cost = [], [], [], [], [], [], []
    for I, J in zip([6, 9, 12, 15], [3, 4, 5, 6]):
        for theta in [0.5, 1, 2, 4, 8]:
            for sd in range(5):
                temp_y, temp_z, temp_obj, temp_time = run_optimization(I, J, 40, sd, 0, theta, 300)
                IJL.append((I, J, J))
                theta_list.append(theta)
                sd_list.append(sd)
                y.append(temp_y.tolist())
                z.append(temp_z.tolist())
                obj.append(temp_obj)
                time_cost.append(temp_time)
                i += 1
                print(f'第{i}个问题求解结束！')
    result['(I,J,L)'] = IJL
    result['theta'] = theta_list
    result['sd'] = sd_list
    result['y'] = y
    result['z'] = z
    result['obj'] = obj
    result['time_cost'] = time_cost
    df = pd.DataFrame(result)
    df.to_excel('solutions/Wass_result.xlsx', index=False)