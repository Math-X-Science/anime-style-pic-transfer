from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field


class ConverterSetting(BaseModel):
    as_package: Annotated[bool, Field(default=False)]
    ffmpeg: Annotated[str, Field(default="ffmpeg")]
    ffprobe: Annotated[str, Field(default="ffprobe")]
    fps: Annotated[int, Field(default=24)]
    model: Annotated[str, Field(default="./models/AnimeGANv3_Shinkai_37.onnx")]
    realesr_excu: Annotated[str, Field(default="./realesrgan/realesrgan-ncnn-vulkan")]
    realesr_model: Annotated[str, Field(default="realesrgan-x4plus-anime")]


class WorkspaceSetting(BaseModel):
    root: Annotated[str, Field(default="./workspace")]
    input: Annotated[str, Field(default="input")]
    output: Annotated[str, Field(default="output")]
    tmp: Annotated[str, Field(default="tmp")]
    input_video: Annotated[str, Field(default="input_video.mp4")]
    output_video: Annotated[str, Field(default="output_video.mp4")]
    input_image: Annotated[str, Field(default="input_image.jpg")]
    output_image: Annotated[str, Field(default="output_image.jpg")]
    upscale_image: Annotated[str, Field(default="upscale_image.jpg")]
