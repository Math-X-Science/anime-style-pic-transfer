from dataclasses import dataclass, field
from pathlib import Path

from converter.utils import load_config


@dataclass
class ConfigParser:
    ffmpeg: str = ""  # Provide a default value (or use field if needed)
    ffprobe: str = ""
    model: str = ""
    fps: int = 0  # Provide a default value (or use field if needed)
    realesr_excu: str = ""
    realesr_model: str = ""
    workspace: dict[str, str] = field(
        default_factory=dict
    )  # Use default_factory correctly

    def __post_init__(self):
        config = load_config()
        self.ffmpeg = str(config.get("ffmpeg", ""))
        self.ffprobe = str(config.get("ffprobe", ""))
        self.model = str(config.get("model", ""))
        self.realesr_excu = str(config.get("realesr_excu", ""))
        self.realesr_model = str(config.get("realesr_model", ""))
        self.fps = int(config.get("fps", 24))  # Provide a default value
        self.workspace = config.get("workspace", {})


@dataclass
class PathParser:
    config = ConfigParser()
    ffmpeg: Path = Path(config.ffmpeg)
    ffprobe: Path = Path(config.ffprobe)
    model_path: Path = Path(config.model)
    realesr_excu: Path = Path(config.realesr_excu)
    realesr_model: Path = Path(config.realesr_model)

    workspace: Path = Path(config.workspace["root"])

    input: Path = workspace / config.workspace["input"]
    output: Path = workspace / config.workspace["output"]
    tmp: Path = workspace / config.workspace["tmp"]
    input_image: Path = workspace / config.workspace["input_image"]
    output_image: Path = workspace / config.workspace["output_image"]
    upscale_image: Path = workspace / config.workspace["upscale_image"]
    input_video: Path = workspace / config.workspace["input_video"]
    output_video: Path = workspace / config.workspace["output_video"]
