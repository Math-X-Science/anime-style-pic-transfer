import os
import sys
from tqdm import tqdm
# 获取当前脚本所在的目录的上级目录
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# 将上级目录添加到模块搜索路径中
sys.path.insert(0, parent_dir)

import torch as t
from torchvision import transforms
from PIL import Image
from model import Generator
from utils import load_config, find_latest_model
import shutil
from tools.common_config import *

IMG_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif']

# 加载模型
def load_model():

    args = load_config(parent_dir+"\\config.yaml")
    _, model_path = find_latest_model(args["result_dir"], args["dataset"])
    if model_path is None:
        raise FileNotFoundError("There is no model file in the directory. Is there no training done?")
    params = t.load(model_path)
    device = t.device("cuda" if args["cuda"] and t.cuda.is_available() else "cpu")
    genA2B = Generator(input_nc=3, output_nc=3, n_hiddens=args["ch"], n_resblocks=4, img_size=[640, 360],
                       light=args["light"]).to(device)
    genA2B.load_state_dict(params["genA2B"])
    genA2B.eval()
    return genA2B, device


# 图片转换函数
def transform_image(image, model, device):
    image_tensor = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=(.5, .5, .5), std=(.5, .5, .5))
    ])(image).unsqueeze(0).to(device)
    with t.no_grad():
        fake_image, _, _ = model.forward(image_tensor)
    fake_image = fake_image.squeeze(0).cpu().numpy()
    fake_image = ((fake_image + 1) / 2 * 255).astype("uint8")
    return Image.fromarray(fake_image.transpose(1, 2, 0))

if __name__ == "__main__":
    """
    input: workspace\\tmp\\input
    output: workspace\\tmp\\output 如果有就删掉
    """ 
    try:
        setting_json = read_config(sys.argv[1], webui=False)
    except Exception as e:
        print("Error: read config", e)
        exit(ERROR_READ_CONFIG)

    setting_config = SettingConfig(setting_json)

    # workspace path config
    workspace = setting_config.get_workspace_config()
        # 蒙版目录存在就删除
    if os.path.exists(workspace.output):
        shutil.rmtree(workspace.output)
    # 创建蒙版输出目录
    os.makedirs(workspace.output)
    # 加载模型
    gen_model, device = load_model()
    input_files = os.listdir(workspace.input)
    for file in tqdm(input_files):
        img = Image.open(workspace.input+"\\"+file)
        image = transform_image(image=img,model=gen_model,device=device)
        image = image.resize(img.size)
        image.save(str(workspace.output)+f"\\{file}")
