from dataclasses import dataclass, field
from pathlib import Path

from converter.utils import load_config


@dataclass
class ConfigParser:
    ffmpeg: str = ""  # Provide a default value (or use field if needed)
    ffprobe: str = ""
    model: str = ""
    fps: int = 0  # Provide a default value (or use field if needed)
    workspace: dict[str, str] = field(
        default_factory=dict
    )  # Use default_factory correctly

    def __post_init__(self):
        config = load_config()
        self.ffmpeg = str(config.get("ffmpeg", ""))
        self.ffprobe = str(config.get("ffprobe", ""))
        self.model = str(config.get("model", ""))
        self.fps = int(config.get("fps", 24))  # Provide a default value
        self.workspace = config.get("workspace", {})


@dataclass
class PathParser:
    config = ConfigParser()
    ffmpeg: Path = Path(config.ffmpeg)
    ffprobe: Path = Path(config.ffprobe)
    model_path: Path = Path(config.model)
    workspace: Path = Path(config.workspace["path"])
    input: Path = Path(config.workspace["input"])
    output: Path = Path(config.workspace["output"])
    tmp: Path = Path(config.workspace["tmp"])
    input_image: Path = Path(config.workspace["input_image"])
    output_image: Path = Path(config.workspace["output_image"])
    input_video: Path = Path(config.workspace["input_video"])
    output_video: Path = Path(config.workspace["output_video"])
