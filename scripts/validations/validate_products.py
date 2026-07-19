"""
=========================================================
Enterprise Gadget Store Data Warehouse
Products Validation

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


def validate_products():

    start = time.time()

    logger.info("=" * 70)
    logger.info("PRODUCT DATA VALIDATION")
    logger.info("=" * 70)

    logger.info("Reading Product Dimension...")

    df = pd.read_sql(

        "SELECT * FROM dim_product",

        engine

    )

    logger.info(f"Rows Read : {len(df):,}")
    # =====================================================
    # Duplicate Validation
    # =====================================================

    duplicates = df["product_id"].duplicated().sum()

    logger.info("=" * 70)
    logger.info("Duplicate Validation")
    logger.info("=" * 70)

    logger.info(f"Duplicate Product IDs : {duplicates}")

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
    # Business Rules Validation
    # =====================================================

    negative_price = (df["selling_price"] < 0).sum()

    negative_cost = (df["manufacturing_cost"] < 0).sum()

    invalid_rating = (
        (df["rating"] < 0) |
        (df["rating"] > 5)
    ).sum()

    logger.info("=" * 70)
    logger.info("Business Rule Validation")
    logger.info("=" * 70)

    logger.info(f"Negative Selling Price      : {negative_price}")

    logger.info(f"Negative Manufacturing Cost : {negative_cost}")

    logger.info(f"Invalid Rating              : {invalid_rating}")

    active = (df["is_active"] == 1).sum()

    inactive = (df["is_active"] == 0).sum()

    logger.info(f"Active Products             : {active:,}")

    logger.info(f"Inactive Products           : {inactive:,}")
    # =====================================================
    # Summary
    # =====================================================

    logger.info("=" * 70)
    logger.info("Product Statistics")
    logger.info("=" * 70)

    logger.info(f"Total Products      : {len(df):,}")

    logger.info(
        f"Unique Brands       : {df['brand'].nunique():,}"
    )

    logger.info(
        f"Unique Categories   : {df['category_id'].nunique():,}"
    )

    logger.info(
        f"Average Price       : {df['selling_price'].mean():,.2f}"
    )

    logger.info(
        f"Average Rating      : {df['rating'].mean():.2f}"
    )

    logger.info("=" * 70)

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )

    logger.info("=" * 70)

    logger.info("Product Validation Completed Successfully")

    logger.info("=" * 70)


if __name__ == "__main__":

    validate_products()
