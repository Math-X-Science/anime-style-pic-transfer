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

    model_path: Path = Path(converter_settings.model)
    realesr_excu: Path = Path(converter_settings.realesr_excu)

    workspace: Path = Path(workspace_settings.root)

    input: Path = workspace / workspace_settings.input
    output: Path = workspace / workspace_settings.output
    tmp: Path = workspace / workspace_settings.tmp
    input_image: Path = workspace / workspace_settings.input_image
    output_image: Path = workspace / workspace_settings.output_image
    upscale_image: Path = workspace / workspace_settings.upscale_image
    input_video: Path = workspace / workspace_settings.input_video
    output_video: Path = workspace / workspace_settings.output_video

    def __init__(self):
        if not self.workspace.exists():
            self.workspace.mkdir(parents=True)
        if not self.model_path.exists():
            raise FileNotFoundError(f"model path not found at {self.model_path}")
        if not self.realesr_excu.exists():
            raise FileNotFoundError(
                f"realesr executable not found at {self.realesr_excu}"
            )
