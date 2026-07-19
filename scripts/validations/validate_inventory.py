"""
=========================================================
Enterprise Gadget Store Data Warehouse
Inventory Validation

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


def validate_inventory():

    start = time.time()

    logger.info("=" * 70)
    logger.info("INVENTORY FACT VALIDATION")
    logger.info("=" * 70)

    logger.info("Reading Fact Inventory...")

    df = pd.read_sql(

        "SELECT * FROM fact_inventory",

        engine

    )

    logger.info(f"Rows Read : {len(df):,}")

    # =====================================================
    # Duplicate Validation
    # =====================================================

    duplicates = df["inventory_id"].duplicated().sum()

    logger.info("=" * 70)
    logger.info("Duplicate Validation")
    logger.info("=" * 70)

    logger.info(f"Duplicate Inventory IDs : {duplicates}")

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

    logger.info("=" * 70)
    logger.info("Business Validation")
    logger.info("=" * 70)

    negative_stock = (df["stock_quantity"] < 0).sum()

    negative_available = (df["available_stock"] < 0).sum()

    negative_reserved = (df["reserved_stock"] < 0).sum()

    negative_damaged = (df["damaged_stock"] < 0).sum()

    logger.info(f"Negative Stock Quantity : {negative_stock}")

    logger.info(f"Negative Available Stock : {negative_available}")

    logger.info(f"Negative Reserved Stock : {negative_reserved}")

    logger.info(f"Negative Damaged Stock : {negative_damaged}")

    # =====================================================
    # Statistics
    # =====================================================

    logger.info("=" * 70)
    logger.info("Inventory Statistics")
    logger.info("=" * 70)

    logger.info(f"Total Inventory Records : {len(df):,}")

    logger.info(
        f"Total Stock Quantity : {df['stock_quantity'].sum():,.0f}"
    )

    logger.info(
        f"Available Stock : {df['available_stock'].sum():,.0f}"
    )

    logger.info(
        f"Reserved Stock : {df['reserved_stock'].sum():,.0f}"
    )

    logger.info(
        f"Damaged Stock : {df['damaged_stock'].sum():,.0f}"
    )

    logger.info(
        f"Average Stock Quantity : {df['stock_quantity'].mean():,.2f}"
    )

    logger.info("=" * 70)

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )

    logger.info("=" * 70)

    logger.info("Inventory Validation Completed Successfully")

    logger.info("=" * 70)


if __name__ == "__main__":

    validate_inventory()
