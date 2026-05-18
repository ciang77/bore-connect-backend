import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

config_path = BASE_DIR / "config.yaml"


with open(config_path, "r", encoding="utf-8") as f:
    settings = yaml.safe_load(f)