from scripts.SP import run_optimization
import pandas as pd

if __name__ == "__main__":
    # 调用函数并传入不同的参数值
    result = {}
    solved_num = 0
    IJL, sd_list, y, z, obj, time_cost = [], [], [], [], [], []
    for I, J in zip([6, 9, 12, 15], [3, 4, 5, 6]):
        for sd in range(5):
            temp_y, temp_z, temp_obj, temp_time = run_optimization(I, J, 40, sd=sd, fixed_cost=300)
            solved_num += 1
            print(f'{solved_num} SP solved!')
            IJL.append((I, J, J))
            sd_list.append(sd)
            y.append(temp_y.tolist())
            z.append(temp_z.tolist())
            obj.append(temp_obj)
            time_cost.append(temp_time)
    result['(I,J,L)'] = IJL
    result['sd'] = sd_list
    result['y'] = y
    result['z'] = z
    result['obj'] = obj
    result['time_cost'] = time_cost
    df = pd.DataFrame(result)
    df.to_excel('solutions/SP_result.xlsx', index=False)
