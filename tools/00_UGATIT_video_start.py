import subprocess
import sys
import os
import time
# 获取当前脚本所在的目录的上级目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
# 将上级目录添加到模块搜索路径中
sys.path.insert(0, parent_dir)
from tools.common_config import *

def count_time(run_scrit_name,config_path,it_mode):
    start_time = time.time()
    subprocess.run(['python', f'{run_scrit_name}', config_path, it_mode])
    end_time = time.time()
    print(f"用时{end_time-start_time}s")


print("0.拆分视频 \n1. 创建蒙版\n2. 裁切图像\n3. 批量图生图\n4. 与帧图像融合 \n5.合成视频")
it_mode = INTERACTIVE_MODE_AUTO


base_dir = os.path.realpath("")
if base_dir == "D:\\program\\UGATIT-pytorch-app-master\\tools":
    print(base_dir)
    print("请以root_dir 作为工作目录执行脚本")
    quit()
config_name = "lm"
config_path = base_dir + "\\config\\runtime\\"  + config_name + ".txt"

start_time = time.time()
count_time( 'tools\\05_UGATIT_BatchImg2Img.py', config_path, it_mode)
end_time = time.time()
print(f"总计用时{end_time-start_time}")

