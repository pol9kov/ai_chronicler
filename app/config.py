import os
import yaml

class Config:
    _cfg = None

    @staticmethod
    def load():
        if Config._cfg is None:
            path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
            with open(path, "r", encoding="utf-8") as f:
                Config._cfg = yaml.safe_load(f)
        return Config._cfg
