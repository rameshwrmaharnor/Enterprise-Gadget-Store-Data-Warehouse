"""
=========================================================
Enterprise Gadget Store Data Warehouse
Customers Validation

Author : Rameshwar Maharnor
=========================================================
"""

import time
import logging
import pandas as pd

from utils.db_connection import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s"
)

logger = logging.getLogger(__name__)


def validate_customers():

    start = time.time()

    logger.info("=" * 70)
    logger.info("CUSTOMER DATA VALIDATION")
    logger.info("=" * 70)

    logger.info("Reading Customer Dimension...")

    df = pd.read_sql(

        "SELECT * FROM dim_customer",

        engine

    )

    logger.info(f"Rows Read : {len(df):,}")
    # =====================================================
    # Duplicate Validation
    # =====================================================

    duplicates = df["customer_id"].duplicated().sum()

    logger.info("=" * 70)
    logger.info("Duplicate Validation")
    logger.info("=" * 70)

    logger.info(f"Duplicate Customer IDs : {duplicates}")

    # =====================================================
    # NULL Validation
    # =====================================================

    logger.info("=" * 70)
    logger.info("NULL Validation")
    logger.info("=" * 70)

    nulls = df.isnull().sum()

    for column, value in nulls.items():

        logger.info(f"{column:<35} : {value}")
# =====================================================
# Business Validation
# =====================================================

    negative_points = (df["loyalty_points"] < 0).sum()

    active = (df["account_status"] == "Active").sum()

    inactive = (df["account_status"] != "Active").sum()

    logger.info("=" * 70)
    logger.info("Business Validation")
    logger.info("=" * 70)

    logger.info(f"Negative Loyalty Points : {negative_points}")

    logger.info(f"Active Customers : {active:,}")

    logger.info(f"Inactive Customers : {inactive:,}")
    # =====================================================
    # Statistics
    # =====================================================

    logger.info("=" * 70)
    logger.info("Customer Statistics")
    logger.info("=" * 70)

    logger.info(f"Total Customers : {len(df):,}")

    logger.info(
        f"Unique Cities : {df['city'].nunique():,}"
    )

    logger.info(
        f"Unique States : {df['state'].nunique():,}"
    )

    logger.info(
        f"Average Loyalty Points : {df['loyalty_points'].mean():,.2f}"
    )

    logger.info(
        f"Customer Segments : {df['customer_segment'].nunique()}"
    )

    logger.info("=" * 70)

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )

    logger.info("=" * 70)

    logger.info("Customer Validation Completed Successfully")

    logger.info("=" * 70)


if __name__ == "__main__":

    validate_customers()
