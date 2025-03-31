from __future__ import annotations

from pathlib import Path

from converter._dataclss import ConverterSetting, WorkspaceSetting
from converter.utils.config import load_settings_file, write_settings_file


class PathParser:
    converter_settings: ConverterSetting = load_settings_file(
        "converter.toml", ConverterSetting
    )
    workspace_settings: WorkspaceSetting = load_settings_file(
        "workspace.toml", WorkspaceSetting
    )

    ffmpeg: Path = Path(converter_settings.ffmpeg)
    ffprobe: Path = Path(converter_settings.ffprobe)
    model_path: Path = Path(converter_settings.model)
    realesr_excu: Path = Path(converter_settings.realesr_excu)
    realesr_model: Path = Path(converter_settings.realesr_model)

    workspace: Path = Path(workspace_settings.root)

    input: Path = workspace / workspace_settings.input
    output: Path = workspace / workspace_settings.output
    tmp: Path = workspace / workspace_settings.tmp
    input_image: Path = workspace / workspace_settings.input_image
    output_image: Path = workspace / workspace_settings.output_image
    upscale_image: Path = workspace / workspace_settings.upscale_image
    input_video: Path = workspace / workspace_settings.input_video
    output_video: Path = workspace / workspace_settings.output_video
