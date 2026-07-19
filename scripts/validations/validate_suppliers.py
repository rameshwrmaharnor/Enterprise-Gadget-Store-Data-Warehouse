"""
=========================================================
Enterprise Gadget Store Data Warehouse
Suppliers Validation

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


def validate_suppliers():

    start = time.time()

    logger.info("=" * 70)
    logger.info("SUPPLIER DATA VALIDATION")
    logger.info("=" * 70)

    logger.info("Reading Supplier Dimension...")

    df = pd.read_sql(

        "SELECT * FROM dim_supplier",

        engine

    )

    logger.info(f"Rows Read : {len(df):,}")
    # =====================================================
    # Duplicate Validation
    # =====================================================

    duplicates = df["supplier_id"].duplicated().sum()

    logger.info("=" * 70)
    logger.info("Duplicate Validation")
    logger.info("=" * 70)

    logger.info(f"Duplicate Supplier IDs : {duplicates}")

    # =====================================================
    # NULL Validation
    # =====================================================

    logger.info("=" * 70)
    logger.info("NULL Validation")
    logger.info("=" * 70)

    nulls = df.isnull().sum()

    for column, value in nulls.items():

        logger.info(f"{column:<30} : {value}")

    # =====================================================
    # Active Suppliers
    # =====================================================

    active = (df["is_active"] == 1).sum()

    inactive = (df["is_active"] == 0).sum()

    logger.info("=" * 70)
    logger.info("Supplier Status")
    logger.info("=" * 70)

    logger.info(f"Active Suppliers   : {active:,}")

    logger.info(f"Inactive Suppliers : {inactive:,}")
    # =====================================================
    # Business Validation
    # =====================================================

    invalid_credit = (

        df["credit_limit"] < 0

    ).sum()

    logger.info("=" * 70)
    logger.info("Business Validation")
    logger.info("=" * 70)

    logger.info(
        f"Negative Credit Limit : {invalid_credit}"
    )

    logger.info(
        f"Average Supplier Rating : {df['supplier_rating'].mean():.2f}"
    )

    logger.info(
        f"Unique Cities : {df['city'].nunique():,}"
    )

    logger.info(
        f"Unique States : {df['state'].nunique():,}"
    )

    logger.info("=" * 70)
    logger.info("Summary")
    logger.info("=" * 70)

    logger.info(f"Total Suppliers : {len(df):,}")

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )

    logger.info("=" * 70)
    logger.info("Supplier Validation Completed Successfully")
    logger.info("=" * 70)


if __name__ == "__main__":

    validate_suppliers()
