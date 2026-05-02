import yaml
import os
import glob
from pathlib import Path

class BaseGenerator:
    def __init__(self, path: Path):
        self.path = path
    def load_config_path(self):
        return glob.glob(os.path.join(self.path, "*.yml"))
    def load_file(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)