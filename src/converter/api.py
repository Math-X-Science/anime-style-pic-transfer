import subprocess
from pathlib import Path
import shutil
from PIL import Image
import os
from tqdm import tqdm

from converter.workflow.common_config import *
from converter._dataclss import ConfigParser, PathParser
from converter._typing import Resolution, Scale
from converter.core.onnx_infer import image_enforce

config_parser = ConfigParser()
path_parser = PathParser()
scale_list = list(Scale.__args__)


def animegan_picture_transfer(upscale: bool):
    # 如果./workspace/output目录存在，删除该目录
    if path_parser.output.exists():
        shutil.rmtree(path_parser.output)

    print("[INFO] ANimeGAN_picture_transfer")
    files = list(path_parser.input.glob("*.jpg"))
    if len(files) == 0:
        print("单张图片")
        # 单张图片
        image_enforce(
            input=str(path_parser.input_image),
            model_path=(path_parser.model_path),
            output=str(path_parser.output_image),
        )
    else:
        print("多张图片")
        for file in tqdm(files):
            image_enforce(
                input=str(file),
                model_path=(path_parser.model_path),
                output=str(path_parser.output),
            )

    output_image = Image.open(path_parser.output_image)
    if upscale:
        output_image = upscale_image(output_image, "4x")
    return output_image


def animegan_video_transfer():
    # subprocess.run(['python','tools\\animegan_video_transfer.py', config_path, it_mode])
    # return str(path/"workspace"/"output.mp4")
    return str(path_parser.output_video)


def save_image(image, resolution: Resolution):  # type:ignore
    # TODO: 后面考虑这image是啥。
    pil_img = Image.fromarray(image.astype("uint8"))  # type:ignore
    # 获取图片原始尺寸
    original_width, original_height = pil_img.size

    # 根据选择的分辨率计算新尺寸，保持宽高比
    if resolution == "240p":
        new_height = 240
        new_width = int(original_width * (240 / original_height))
    elif resolution == "720p":
        new_height = 720
        new_width = int(original_width * (720 / original_height))
    elif resolution == "1080p":
        new_height = 1080
        new_width = int(original_width * (1080 / original_height))
    else:
        raise ValueError("Unsupported resolution")

    # 调整图片尺寸
    resized_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # 确定保存路径
    workspace = path_parser.workspace

    if os.path.exists(workspace):
        shutil.rmtree(workspace)

    os.makedirs(workspace)

    save_path = path_parser.input
    if os.path.exists(save_path):
        shutil.rmtree(save_path)

    os.makedirs(save_path)

    # 保存图片到指定路径，并按分辨率命名
    save_file = path_parser.input_image
    resized_img.save(save_file)

    return f"Image saved as {save_file}"


from moviepy.editor import VideoFileClip


def save_video(video, target_resolution="720p"):
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
    if target_resolution == "240p":
        target_height = 240
    elif target_resolution == "720p":
        target_height = 720
    else:
        raise ValueError("Unsupported resolution. Choose '240p' or '720p'.")

    # 计算保持宽高比的目标宽度
    original_width, original_height = video_clip.size
    target_width = int(original_width * (target_height / original_height))

    # 调整视频尺寸并保存
    resized_clip = video_clip.resize((target_width, target_height))
    video_save_path = os.path.join(save_path, "video.mp4")
    resized_clip.write_videofile(video_save_path, codec="libx264")

    return f"Original video saved as {origin_save_path} and resampled video saved as {video_save_path}"


def upscale_image(image: Image.Image, scale: Scale):
    """将输入图片放大scale倍"""
    if scale not in ["2x", "4x", "8x"]:
        raise ValueError("Unsupported scale. Choose 2, 4, or 8.")
    if scale == "4x":
        execu = path_parser.realesr_excu
        # ./realesrgan-ncnn-vulkan.exe -i image_240p.png -o output.png -n realesr-animevideov3-x4
        # 保存 image 到./workspace/input/image.png
        # 保存 output 到./workspace/output/image.png
        # 检查 image 是否是 Image 实例, 如果是，就跳过
        subprocess.run(
            [
                str(execu),
                "-i",
                str(path_parser.output_image),
                "-o",
                str(path_parser.upscale_image),
                "-n",
                path_parser.realesr_model,
            ]
        )
        # 读取图片
        output_image = Image.open(str(path_parser.upscale_image))
        return output_image


def v2v_model_choce(choosed_model):
    if choosed_model == "AnimeGANv3_Shinkai_37":
        SD_origin_background_video_transfer()

    path = Path(os.path.realpath(__file__)).parent
    return str(path / "workspace" / "output.mp4")
