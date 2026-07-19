"""
=========================================================
Enterprise Gadget Store Data Warehouse
Configuration Loader

Author : Rameshwar Maharnor
=========================================================
"""

from pathlib import Path
import yaml


class Config:

    def __init__(self):

        project_root = Path(__file__).resolve().parent.parent

        config_file = project_root / "config" / "config.yaml"

        with open(config_file, "r", encoding="utf-8") as file:
            self._config = yaml.safe_load(file)

    def get(self):
        return self._config


config = Config().get()
