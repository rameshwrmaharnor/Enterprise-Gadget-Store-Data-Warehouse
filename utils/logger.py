"""
=========================================================
Enterprise Gadget Store Data Warehouse
Logger Utility

Author : Rameshwar Maharnor
=========================================================
"""

import logging
from pathlib import Path

from utils.config import config


class ProjectLogger:
    """
    Centralized Logger
    """

    def __init__(self):

        log_folder = Path(config["paths"]["logs"])
        log_folder.mkdir(parents=True, exist_ok=True)

        log_file = log_folder / "project.log"

        logging.basicConfig(
            level=getattr(logging, config["logging"]["level"]),
            format="%(asctime)s | %(levelname)-8s | %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger("EnterpriseGadgetStore")

    def get_logger(self):
        return self.logger


logger = ProjectLogger().get_logger()
