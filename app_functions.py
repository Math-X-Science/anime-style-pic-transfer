import subprocess
import sys
from pathlib import Path
from tools.common_config import *
import shutil
from PIL import Image
import os
import logging
it_mode = INTERACTIVE_MODE_AUTO
base_dir = str(Path(os.path.realpath(__file__)).parent)
if base_dir == "D:\\program\\UGATIT-pytorch-app-master\\tools":
    print(base_dir)
    print("请以root_dir 作为工作目录执行脚本")
    quit()
config_name = "lm"
config_path = base_dir + "\\config\\runtime\\"  + config_name + ".txt"


def UGATIT_origin_bacground_transfer():
    print("[INFO] UGATIT_origin_bacground_transfer")
    """
    input: workspace\\tmp\\input_crop
    output: workspace\\tmp\\output_crop 如果有就删掉
    """ 
    path = Path(os.path.realpath(__file__)).parent
    config_root_dir = path / "config"
    setting_json = config_root_dir / "runtime" / "lm.txt"

    setting_config = SettingConfig(str(setting_json))

    # workspace path config
    workspace = setting_config.get_workspace_config()
    
    subprocess.run(['python','tools\\uga_pic_transfer.py', config_path, it_mode])

    files = os.listdir(str(path / "workspace" /workspace.output))
    output_image = Image.open(str(path / "workspace" / workspace.output /(files[0])))
    
    return output_image

def UGATIT_original_background_video_transfer():
    print("[INFO] UGATIT_original_background_video_transfer")
    """
    input: workspace\\video.mp4
    output: workspace\\output.video 如果有就删掉
    """ 
    path = Path(os.path.realpath(__file__)).parent
    config_root_dir = path / "config"
    setting_json = config_root_dir / "runtime" / "lm.txt"

    setting_config = SettingConfig(str(setting_json))

    # workspace path config
    workspace = setting_config.get_workspace_config()
    subprocess.run(['python','tools\\00_UGATIT_video_start.py', config_path, it_mode])
    return str(path/"workspace"/"output.mp4")


def SD_origin_background_transfer():
    print("[INFO] SD_origin_bacground_transfer")
    """
    input: workspace\\tmp\\input_crop
    output: workspace\\tmp\\output_crop 如果有就删掉
    """ 
    path = Path(os.path.realpath(__file__)).parent
    config_root_dir = path / "config"
    setting_json = config_root_dir / "runtime" / "lm.txt"

    setting_config = SettingConfig(str(setting_json))

    # workspace path config
    workspace = setting_config.get_workspace_config()

    subprocess.run(['python','tools\\animegan_pic_transfer.py', config_path, it_mode])
    files = os.listdir(str(path / "workspace" /workspace.output/"imgs"))
    output_image = Image.open(str(path / "workspace" / workspace.output / "imgs" /(files[0])))
    return output_image
def SD_origin_background_video_transfer():
    print("[INFO] UGATIT_original_background_video_transfer")
    """
    input: workspace\\video.mp4
    output: workspace\\output.video 如果有就删掉
    """ 
    path = Path(os.path.realpath(__file__)).parent
    config_root_dir = path / "config"
    setting_json = config_root_dir / "runtime" / "lm.txt"

    setting_config = SettingConfig(str(setting_json))

    # workspace path config
    workspace = setting_config.get_workspace_config()
    subprocess.run(['python','tools\\animegan_video_transfer.py', config_path, it_mode])
    return str(path/"workspace"/"output.mp4")
def identity(x, state):
    state += 1
    return x, state, state

def scale_process(text, w):
     if text == ("3:4"):
          return w*4/3
     return w*9/16


def save_image(image, resolution):
    """resolution: 选择的分辨率{360p, 480p, 720p, 1080p}"""
    pil_img = Image.fromarray(image.astype('uint8'))

    # 获取图片原始尺寸
    original_width, original_height = pil_img.size

    # 根据选择的分辨率计算新尺寸，保持宽高比
    if resolution == "240p":
        new_height = 240
        new_width = int(original_width * (240 / original_height))
    elif resolution == "720p":
        new_height = 720
        new_width = int(original_width * (720 / original_height))
    else:
        raise ValueError("Unsupported resolution")

    # 调整图片尺寸
    resized_img = pil_img.resize((new_width, new_height), Image.ANTIALIAS)

    # 确定保存路径
    path = Path(os.path.realpath(__file__)).parent
    config_root_dir = path / "config"
    setting_json = config_root_dir / "runtime" / "lm.txt"

    setting_config = SettingConfig(str(setting_json))

    # workspace path config
    workspace = setting_config.get_workspace_config()
    save_path = str(path / "workspace")

    if os.path.exists(save_path):
        shutil.rmtree(save_path)
        os.makedirs(save_path)
    else:
        os.makedirs(save_path)
    
    save_path = str(path / "workspace" / workspace.input)
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
        os.makedirs(save_path)
    else:
        os.makedirs(save_path)

    # 保存图片到指定路径，并按分辨率命名
    save_file = os.path.join(save_path, f"image_{resolution}.png")
    resized_img.save(save_file)

    return f"Image saved as {save_file}"


from moviepy.editor import VideoFileClip
def save_video(video, target_resolution='720p'):
    """保存原视频为origin.mp4，并重采样为目标分辨率的视频video.mp4"""
    
    # 确定保存路径
    path = Path(os.path.realpath(__file__)).parent
    config_root_dir = path / "config"
    setting_json = config_root_dir / "runtime" / "lm.txt"

    setting_config = SettingConfig(str(setting_json))

    # workspace path config
    workspace = setting_config.get_workspace_config()
    save_path = str(path / "workspace")

    if os.path.exists(save_path):
        shutil.rmtree(save_path)
        os.makedirs(save_path)
    else:
        os.makedirs(save_path)

    # 保存原视频为 origin.mp4
    origin_save_path = os.path.join(save_path, "origin.mp4")
    shutil.copy(video, origin_save_path)

    # 使用moviepy对视频进行重采样
    video_clip = VideoFileClip(origin_save_path)

    # 根据选择的分辨率设置目标高度
    if target_resolution == '240p':
        target_height = 240
    elif target_resolution == '720p':
        target_height = 720
    else:
        raise ValueError("Unsupported resolution. Choose '240p' or '720p'.")

    # 计算保持宽高比的目标宽度
    original_width, original_height = video_clip.size
    target_width = int(original_width * (target_height / original_height))

    # 调整视频尺寸并保存
    resized_clip = video_clip.resize((target_width, target_height))
    video_save_path = os.path.join(save_path, "video.mp4")
    resized_clip.write_videofile(video_save_path, codec='libx264')

    return f"Original video saved as {origin_save_path} and resampled video saved as {video_save_path}"
     

def error_prone_function(input_data):
    try:
        # ...可能会引发错误的代码...
        result = "Success!"
    except Exception as e:
        print(f"Error: {str(e)}")  # 打印错误到终端
        result = f"Error: {str(e)}"
    return result





def sepia(image, x, y, weight, scale):
    #w = x + weight
    #h = scale_process(scale, w)
    #box = (x, y, w, h)

    #img = Image.open(r"D:\pythonproject\UGATIT-pytorch-app-master\IMG.jpg")

    img = image
    pil_img = Image.fromarray(img.astype('uint8'))
    #cropped_image = pil_img.crop(box=box)
    cropped_image = pil_img

    return cropped_image

def p2p_model_choice(choosed_model):
    if choosed_model == "AnimeGANv3_Shinkai_37":
        output_img = SD_origin_background_transfer()
    
    return output_img

def v2v_model_choce(choosed_model):
    if choosed_model == "AnimeGANv3_Shinkai_37":
        SD_origin_background_video_transfer()
    
    path = Path(os.path.realpath(__file__)).parent
    return str(path/"workspace"/"output.mp4")