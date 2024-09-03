import subprocess
import os
import sys
# 获取当前脚本所在的目录的上级目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
# 将上级目录添加到模块搜索路径中
sys.path.insert(0, parent_dir)
import torch
import shutil

from tools.common_config import *


if __name__ == '__main__':
    ffmpeg_path = os.path.join('.', 'ffmpeg-master-latest-win64-gpl-shared', 'bin', 'ffmpeg.exe')
    if len(sys.argv) < 2:
        print("Params: <runtime-config.json>")
        exit(ERROR_PARAM_COUNT)

    it_mode = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        setting_json = read_config(sys.argv[1], webui=False)
    except Exception as e:
        print("Error: read config", e)
        exit(ERROR_READ_CONFIG)

    setting_config = SettingConfig(setting_json)

    # workspace path config
    workspace = setting_config.get_workspace_config()

    # 检查参数
    video_config = setting_config.get_video()
    if is_empty(video_config.get_input()):
        print("Error: no 'video' in config")
        exit(ERROR_NO_VIDEO)
    video_file = os.path.join(workspace.root, video_config.get_input())
    if os.path.exists(video_file) is False:
        print("Error: video file not exists", video_file)
        exit(ERROR_NO_VIDEO)

    # 帧目录存在就删除
    if os.path.exists(workspace.input):
        shutil.rmtree(workspace.input)
    # 创建帧输出目录
    os.makedirs(workspace.input)

    # 定义帧率（这里设置为每秒截取15帧）
    fps = video_config.get_fps()

    # 设置Torch不使用图形界面显示
    os.environ["PYTORCH_JIT"] = "1"

    # 使用CUDA进行加速
    torch.set_grad_enabled(False)

    # 使用 ffmpeg 命令行工具截取视频帧，并将其保存为图片
    subprocess.call([
        ffmpeg_path, "-i", video_file,
        "-vf", "fps=" + str(8),
        os.path.join(workspace.input, "%05d.png")
    ])

    print("\n\n视频转帧步骤已完成！帧率为： " + str(8))

    if it_mode is None:
        it_mode = setting_config.get_interactive_mode()
    if it_mode == INTERACTIVE_MODE_INPUT:
        choice = input("\n是否直接开始下一步，将视频帧输出为蒙版？\n1. 是\n2. 否\n请输入你的选择：")
        if choice != "1":
            exit(0)