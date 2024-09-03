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


# 定义一个函数来保存图片并按顺序命名
def save_image(image):
    pil_img = Image.fromarray(image.astype('uint8'))

    # 确定保存路径
    path = Path(os.path.realpath(__file__)).parent
    config_root_dir = path / "config"
    setting_json = config_root_dir / "runtime" / "lm.txt"

    setting_config = SettingConfig(str(setting_json))

    # workspace path config
    workspace = setting_config.get_workspace_config()
    save_path = str(path / "workspace" )

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
    pil_img.save(save_path+"\\image.png")

    return f"Image saved as {pil_img}"

def save_video(video):

    path = Path(os.path.realpath(__file__)).parent
    config_root_dir = path / "config"
    setting_json = config_root_dir / "runtime" / "lm.txt"

    setting_config = SettingConfig(str(setting_json))

    # workspace path config
    workspace = setting_config.get_workspace_config()
    save_path = str(path / "workspace" )

    if os.path.exists(save_path):
         shutil.rmtree(save_path)
         os.makedirs(save_path)
    else:
        os.makedirs(save_path)

    shutil.copy(video,save_path)
    files = os.listdir(save_path)
    for f in files:
        if ".mp4" in f :
            os.rename(str(path/"workspace"/f),str(path/"workspace"/"video.mp4"))

    
    return f"Image saved as {video} "

    


     

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
