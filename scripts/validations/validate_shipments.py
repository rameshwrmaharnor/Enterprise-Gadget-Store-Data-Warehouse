"""
=========================================================
Enterprise Gadget Store Data Warehouse
Shipments Validation

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


def validate_shipments():

    start = time.time()

    logger.info("=" * 70)
    logger.info("SHIPMENT FACT VALIDATION")
    logger.info("=" * 70)

    logger.info("Reading Fact Shipments...")

    df = pd.read_sql(

        "SELECT * FROM fact_shipments",

        engine

    )

    logger.info(f"Rows Read : {len(df):,}")

    # =====================================================
    # Duplicate Validation
    # =====================================================

    duplicates = df["shipment_id"].duplicated().sum()

    logger.info("=" * 70)
    logger.info("Duplicate Validation")
    logger.info("=" * 70)

    logger.info(f"Duplicate Shipment IDs : {duplicates}")

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

    negative_cost = (df["shipping_cost"] < 0).sum()

    logger.info(f"Negative Shipping Cost : {negative_cost}")

    logger.info(
        f"Unique Shipping Status : {df['shipping_status'].nunique()}"
    )

    logger.info(
        f"Unique Courier Partners : {df['courier_partner'].nunique()}"
    )

    delivered = (

        df["shipping_status"] == "Delivered"

    ).sum()

    logger.info(
        f"Delivered Shipments : {delivered:,}"
    )

    # =====================================================
    # Shipment Statistics
    # =====================================================

    logger.info("=" * 70)
    logger.info("Shipment Statistics")
    logger.info("=" * 70)

    logger.info(f"Total Shipments : {len(df):,}")

    logger.info(
        f"Total Shipping Cost : {df['shipping_cost'].sum():,.2f}"
    )

    logger.info(
        f"Average Shipping Cost : {df['shipping_cost'].mean():,.2f}"
    )

    logger.info(
        f"Maximum Shipping Cost : {df['shipping_cost'].max():,.2f}"
    )

    logger.info(
        f"Minimum Shipping Cost : {df['shipping_cost'].min():,.2f}"
    )

    logger.info("=" * 70)

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )

    logger.info("=" * 70)

    logger.info("Shipment Validation Completed Successfully")

    logger.info("=" * 70)


if __name__ == "__main__":

    validate_shipments()
