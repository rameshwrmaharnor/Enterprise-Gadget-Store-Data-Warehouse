"""
=========================================================
Enterprise Gadget Store Data Warehouse
Database Connection Utility

Author : Rameshwar Maharnor
=========================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from utils.config import config
from utils.logger import logger


class DatabaseConnection:
    """
    MySQL Database Connection
    """

    def __init__(self):

        db = config["database"]

        self.connection_string = (

            f"mysql+pymysql://"

            f"{db['username']}:{db['password']}"

            f"@{db['host']}:{db['port']}"

            f"/{db['database']}"

            f"?charset=utf8mb4"

        )

    def get_engine(self):

        try:

            engine = create_engine(

                self.connection_string,

                pool_pre_ping=True,
                pool_recycle=3600,
                future=True

            )

            logger.info(
                "MySQL Database Engine Created Successfully"
            )

            return engine

        except SQLAlchemyError as error:

            logger.error(error)

            raise


db = DatabaseConnection()

engine = db.get_engine()