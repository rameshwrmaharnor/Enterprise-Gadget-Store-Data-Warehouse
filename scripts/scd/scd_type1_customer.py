"""
=========================================================
Enterprise Gadget Store Data Warehouse
SCD Type 1 - Customer Dimension
=========================================================
"""

import time
import logging
import pandas as pd

from sqlalchemy import text
from utils.db_connection import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s"
)

logger = logging.getLogger(__name__)


def run_scd_type1():

    start = time.time()

    logger.info("=" * 70)
    logger.info("SCD TYPE 1 - CUSTOMER DIMENSION")
    logger.info("=" * 70)

    logger.info("Reading Latest Customers From Silver Layer...")

    df = pd.read_sql("""

    SELECT

        customer_id,
        first_name,
        last_name,
        gender,
        city,
        state,
        country,
        customer_segment,
        loyalty_points,
        account_status,
        created_date

    FROM silver_customers

    """, engine)

    logger.info(f"Customers Read : {len(df):,}")

    logger.info("Refreshing Customer Dimension...")

    with engine.begin() as conn:

        conn.execute(text("TRUNCATE TABLE dim_customer"))

    df.to_sql(

        "dim_customer",

        engine,

        if_exists="append",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(f"Customers Loaded : {len(df):,}")

    logger.info("SCD Type 1 Completed Successfully")

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )


if __name__ == "__main__":
    run_scd_type1()
