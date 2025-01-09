import pandas as pd
from geopy.distance import distance
import sys

def main(facility_num, customer_num):
    # 根据点对数量动态生成文件名
    filename = f"f{facility_num}_c{customer_num}_distance.csv"

    columns = [f'c_{i}' for i in range(1, customer_num + 1)]
    index = [f'f_{i}' for i in range(1, facility_num + 1)]
    # 指定CSV文件路径
    csv_file_path = f"../coordinates/f{facility_num}_c{customer_num}.csv"

    # 使用pandas的read_csv函数读取CSV文件
    df = pd.read_csv(csv_file_path)

    # 访问坐标数据
    facilitys = df[df['Type'] == 'Facility'][['Latitude','Longitude']].values
    customers = df[df['Type'] == 'Customer'][['Latitude','Longitude']].values

    disframe = pd.DataFrame(columns=columns, index=index)
    for i in range(1, facility_num+1):
        for j in range(1, customer_num+1):
            point_a = facilitys[i-1]
            point_b = customers[j-1]
            disframe.iloc[i-1, j-1] = distance(point_a, point_b).kilometers
    disframe.to_csv(filename, index=True)

    print(f"distances of {facility_num} facilities and {customer_num} customers have been successfully written to {filename}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        facility_num = int(sys.argv[1])
        customer_num = int(sys.argv[2])
    else:
        print('请输入设施数量和客户数量')
        sys.exit(0) 

    main(facility_num, customer_num)