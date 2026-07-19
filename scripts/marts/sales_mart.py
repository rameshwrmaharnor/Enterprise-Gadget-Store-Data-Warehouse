"""
=========================================================
Enterprise Gadget Store Data Warehouse
Sales Mart Loader
=========================================================
"""

import time
import logging

from sqlalchemy import text

from utils.db_connection import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s"
)

logger = logging.getLogger(__name__)


def run_sales_mart():

    start = time.time()

    logger.info("=" * 70)
    logger.info("Creating Sales Mart")
    logger.info("=" * 70)

    sql_file = "sql/marts/create_sales_mart.sql"

    with open(sql_file, "r", encoding="utf-8") as file:
        sql = file.read()

    with engine.begin() as conn:

        for statement in sql.split(";"):

            statement = statement.strip()

            if statement:
                conn.execute(text(statement))

    logger.info("Sales Mart Created Successfully")
    logger.info(f"Execution Time : {time.time()-start:.2f} Seconds")


if __name__ == "__main__":
    run_sales_mart()
