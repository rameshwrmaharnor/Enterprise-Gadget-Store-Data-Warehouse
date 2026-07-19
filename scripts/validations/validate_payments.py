"""
=========================================================
Enterprise Gadget Store Data Warehouse
Payments Validation

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


def validate_payments():

    start = time.time()

    logger.info("=" * 70)
    logger.info("PAYMENT FACT VALIDATION")
    logger.info("=" * 70)

    logger.info("Reading Fact Payments...")

    df = pd.read_sql(

        "SELECT * FROM fact_payments",

        engine

    )

    # =====================================================
    logger.info(f"Rows Read : {len(df):,}")
    # Duplicate Validation
    # =====================================================

    duplicates = df["payment_id"].duplicated().sum()

    logger.info("=" * 70)
    logger.info("Duplicate Validation")
    logger.info("=" * 70)

    logger.info(f"Duplicate Payment IDs : {duplicates}")

    # =====================================================
    # NULL Validation
    # =====================================================

    logger.info("=" * 70)
    logger.info("NULL Validation")
    logger.info("=" * 70)

    nulls = df.isnull().sum()

    for column, value in nulls.items():

        # =====================================================
        logger.info(f"{column:<35} : {value}")
    # Business Validation
    # =====================================================

    negative_amount = (df["payment_amount"] < 0).sum()

    logger.info("=" * 70)
    logger.info("Business Validation")
    logger.info("=" * 70)

    logger.info(f"Negative Payment Amount : {negative_amount}")

    logger.info(
        f"Successful Payments : {(df['payment_status'] == 'Paid').sum():,}"
    )

    logger.info(
        f"Failed Payments : {(df['payment_status'] != 'Paid').sum():,}"
    )

    logger.info(
        f"Unique Payment Methods : {df['payment_method'].nunique()}"
    )

    logger.info(
        f"Unique Gateways : {df['payment_gateway'].nunique()}"
    )    # =====================================================
    # Statistics
    # =====================================================

    logger.info("=" * 70)
    logger.info("Payment Statistics")
    logger.info("=" * 70)

    logger.info(f"Total Payments : {len(df):,}")

    logger.info(
        f"Total Payment Amount : {df['payment_amount'].sum():,.2f}"
    )

    logger.info(
        f"Average Payment : {df['payment_amount'].mean():,.2f}"
    )

    logger.info(
        f"Maximum Payment : {df['payment_amount'].max():,.2f}"
    )

    logger.info(
        f"Minimum Payment : {df['payment_amount'].min():,.2f}"
    )

    logger.info("=" * 70)

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )

    logger.info("=" * 70)

    logger.info("Payment Validation Completed Successfully")

    logger.info("=" * 70)


if __name__ == "__main__":

    validate_payments()
