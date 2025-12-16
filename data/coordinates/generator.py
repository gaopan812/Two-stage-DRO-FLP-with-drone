import random
import pandas as pd
import sys
import os
current_path = os.getcwd()  # 获取当前工作目录路径

min_latitude = 47.518005
max_latitude = 47.734
min_longitude = -122.416737
max_longitude = -122.277348


def generate_random_point():
    latitude = random.uniform(min_latitude, max_latitude)
    longitude = random.uniform(min_longitude, max_longitude)
    return latitude, longitude


def main(facility_num, customer_num):
    filename = f"f{facility_num}_c{customer_num}.csv"
    full_file_path = os.path.join(current_path, filename)

    # 初始化 DataFrame
    columns = ["Type", "Latitude", "Longitude"]
    data = {
        "Type": [],
        "Latitude": [],
        "Longitude": []
    }

    # 添加设施数据
    for i in range(facility_num):
        point = generate_random_point()
        data["Type"].append("Facility")
        data["Latitude"].append(point[0])
        data["Longitude"].append(point[1])

    # 添加客户数据
    for i in range(customer_num):
        point = generate_random_point()
        data["Type"].append("Customer")
        data["Latitude"].append(point[0])
        data["Longitude"].append(point[1])

    # 创建 DataFrame
    df = pd.DataFrame(data, columns=columns)

    try:
        # 将 DataFrame 写入 CSV 文件
        df.to_csv(full_file_path, index=False)
        print(f"{facility_num} facilities and {customer_num} customers have been successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        facility_num = int(sys.argv[1])
        customer_num = int(sys.argv[2])
    else:
        print('请输入设施数量和客户数量')
        sys.exit(0) 

    main(facility_num, customer_num)
