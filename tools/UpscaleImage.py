import subprocess
import sys
import os
import time
# 获取当前脚本所在的目录的上级目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
# 将上级目录添加到模块搜索路径中
sys.path.insert(0, parent_dir)
subprocess.run("RealESR-GAN\\anime_pic.bat", shell=True)