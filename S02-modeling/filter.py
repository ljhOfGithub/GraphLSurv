# import pandas as pd
# import shutil
# import os

# # 读取CSV文件
# input_file = '/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA/data_split/tcga_brca/tcga_brca_path_full_ljh.csv'
# df = pd.read_csv(input_file)

# # 源文件夹和目标文件夹
# # source_folder = '/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA/feats-l1-s256-mrandom_be-n1000-color_norm/graph-knn-k6-t0'  # 你的源文件夹路径
# source_folder = '/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA/feats-l1-s256-mrandom_be-n1000-color_norm/h5_files'  # 你的源文件夹路径
# # destination_folder = '/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA/feats-l1-s256-mrandom_be-n1000-color_norm/graph-knn-k6-t0-part'  # 你的目标文件夹路径
# destination_folder = '/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA/feats-l1-s256-mrandom_be-n1000-color_norm/h5_files_part'  # 你的目标文件夹路径

# # 遍历每行数据，根据 pathology_id 列进行文件复制
# for index, row in df.iterrows():
#     # pathology_id = row['patient_id']
#     pathology_id = row['pathology_id']
#     h5_filename = f"{pathology_id}.h5"
    
#     source_path = os.path.join(source_folder, h5_filename)
#     destination_path = os.path.join(destination_folder, h5_filename)
    
#     if os.path.exists(source_path) and os.path.isfile(source_path):
#         shutil.copy(source_path, destination_path)
#         # print(f"复制文件 {h5_filename} 到 {destination_folder}")
#     # else:
#         # print("跳过")

import os
import shutil

input_file = '/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA/feats-l1-s256-mrandom_be-n1000-color_norm/patient_id.csv'
# 读取CSV文件，得到列表
with open(inputfile, 'r') as file:
    values_list = [line.strip() for line in file]

# 源文件夹和目标文件夹
# source_folder = '/path/to/source_folder'
source_folder = '/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA/feats-l1-s256-mrandom_be-n1000-color_norm/h5_files'  # 你的源文件夹路径

# destination_folder = '/path/to/destination_folder'
destination_folder = '/home/jupyter-ljh/data/mntdata/data0/LI_jihao/GraphLSurv-BRCA/feats-l1-s256-mrandom_be-n1000-color_norm/h5_files_part_part'  # 你的目标文件夹路径

# 遍历源文件夹中的文件
for filename in os.listdir(source_folder):
    # 获取文件名的前十位
    prefix = filename[:10]
    
    # 判断前十位是否在列表中
    if prefix in values_list:
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(destination_folder, filename)
        
        shutil.copy(source_path, destination_path)
        print(f"复制文件 {filename} 到 {destination_folder}")

print("操作已完成。")
