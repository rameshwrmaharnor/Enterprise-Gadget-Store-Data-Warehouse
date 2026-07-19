"""
=========================================================
Enterprise Gadget Store Data Warehouse
Categories Validation

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


def validate_categories():

    start = time.time()

    logger.info("=" * 70)
    logger.info("CATEGORY DATA VALIDATION")
    logger.info("=" * 70)

    logger.info("Reading Category Dimension...")

    df = pd.read_sql(

        "SELECT * FROM dim_category",

        engine

    )

    logger.info(f"Rows Read : {len(df):,}")
    # =====================================================
    # Duplicate Check
    # =====================================================

    duplicates = df["category_id"].duplicated().sum()

    logger.info("=" * 70)
    logger.info("Duplicate Validation")
    logger.info("=" * 70)

    logger.info(f"Duplicate Category IDs : {duplicates}")

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
    # Active Categories
    # =====================================================

    active = (

        df["is_active"] == 1

    ).sum()

    inactive = (

        df["is_active"] == 0

    ).sum()

    logger.info("=" * 70)
    logger.info("Category Status")
    logger.info("=" * 70)

    logger.info(f"Active Categories   : {active:,}")

    logger.info(f"Inactive Categories : {inactive:,}")
    # =====================================================
    # Statistics
    # =====================================================

    logger.info("=" * 70)
    logger.info("Summary")
    logger.info("=" * 70)

    logger.info(f"Total Categories : {len(df):,}")

    logger.info(

        f"Unique Categories : {df['category_name'].nunique():,}"

    )

    logger.info(

        f"Execution Time : {time.time()-start:.2f} Seconds"

    )

    logger.info("=" * 70)

    logger.info("Category Validation Completed Successfully")

    logger.info("=" * 70)


if __name__ == "__main__":

    validate_categories()
