from scripts.MAD_DRO import run_optimization
import pandas as pd


if __name__ == "__main__":
    # 调用函数并传入不同的参数值
    result = {}
    i = 0
    IJL, event_num_list, sd_list, y, z, obj, time_cost = [], [], [], [], [], [], []
    for I, J in zip([6, 9, 12, 15], [3, 4, 5, 6]):
        for sd in range(5):
            event_num, temp_y, temp_z, temp_obj, temp_time = run_optimization(I, J, 40, sd, 0)
            IJL.append((I, J, J))
            event_num_list.append(event_num)
            sd_list.append(sd)
            y.append(temp_y.tolist())
            z.append(temp_z.tolist())
            obj.append(temp_obj)
            time_cost.append(temp_time)
            i += 1
            print(f'第{i}个问题求解结束！')
    result['(I,J,L)'] = IJL
    result['event_num'] = event_num_list
    result['sd'] = sd_list
    result['y'] = y
    result['z'] = z
    result['obj'] = obj
    result['time_cost'] = time_cost
    df = pd.DataFrame(result)
    df.to_excel('solutions/MAD_result.xlsx', index=False)