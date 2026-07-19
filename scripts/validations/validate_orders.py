"""
=========================================================
Enterprise Gadget Store Data Warehouse
Orders Validation

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


def validate_orders():

    start = time.time()

    logger.info("=" * 70)
    logger.info("ORDER FACT VALIDATION")
    logger.info("=" * 70)

    logger.info("Reading Fact Orders...")

    df = pd.read_sql(

        "SELECT * FROM fact_orders",

        engine

    )

    logger.info(f"Rows Read : {len(df):,}")
    # =====================================================
    # Duplicate Validation
    # =====================================================

    duplicates = df["order_id"].duplicated().sum()

    logger.info("=" * 70)
    logger.info("Duplicate Validation")
    logger.info("=" * 70)

    logger.info(f"Duplicate Order IDs : {duplicates}")

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
    # Business Rule Validation
    # =====================================================

    negative_total = (df["total_amount"] < 0).sum()

    negative_tax = (df["tax_amount"] < 0).sum()

    negative_discount = (df["discount_amount"] < 0).sum()

    logger.info("=" * 70)
    logger.info("Business Validation")
    logger.info("=" * 70)

    logger.info(f"Negative Total Amount : {negative_total}")

    logger.info(f"Negative Tax Amount : {negative_tax}")

    logger.info(f"Negative Discount : {negative_discount}")

    logger.info(
        f"Unique Payment Methods : {df['payment_method'].nunique()}"
    )

    logger.info(
        f"Unique Order Status : {df['order_status'].nunique()}"
    )

    logger.info(
        f"Unique Delivery Types : {df['delivery_type'].nunique()}"
    )
    # =====================================================
    # Statistics
    # =====================================================

    logger.info("=" * 70)
    logger.info("Order Statistics")
    logger.info("=" * 70)

    logger.info(f"Total Orders : {len(df):,}")

    logger.info(
        f"Total Revenue : {df['total_amount'].sum():,.2f}"
    )

    logger.info(
        f"Average Order Value : {df['total_amount'].mean():,.2f}"
    )

    logger.info(
        f"Maximum Order Value : {df['total_amount'].max():,.2f}"
    )

    logger.info(
        f"Minimum Order Value : {df['total_amount'].min():,.2f}"
    )

    logger.info("=" * 70)

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )

    logger.info("=" * 70)

    logger.info("Order Validation Completed Successfully")

    logger.info("=" * 70)


if __name__ == "__main__":

    validate_orders()

