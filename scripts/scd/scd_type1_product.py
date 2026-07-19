"""
=========================================================
Enterprise Gadget Store Data Warehouse
SCD Type 1 - Product Dimension
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


def run_scd_type1_product():

    start = time.time()

    logger.info("=" * 70)
    logger.info("SCD TYPE 1 - PRODUCT DIMENSION")
    logger.info("=" * 70)

    df = pd.read_sql("""

    SELECT
        product_id,
        sku,
        barcode,
        product_name,
        brand,
        category_id,
        supplier_id,
        color,
        material,
        warranty_months,
        manufacturing_cost,
        selling_price,
        profit_margin_percent,
        discount_percent,
        weight_kg,
        dimensions,
        stock_quantity,
        reorder_level,
        rating,
        manufacture_date,
        launch_date,
        product_status,
        is_active,
        created_date

    FROM silver_products

    """, engine)

    logger.info(f"Products Read : {len(df):,}")

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE dim_product"))

    df.to_sql(
        "dim_product",
        engine,
        if_exists="append",
        index=False,
        chunksize=10000,
        method="multi"
    )

    logger.info(f"Products Loaded : {len(df):,}")
    logger.info("SCD Type 1 Product Completed Successfully")
    logger.info(f"Execution Time : {time.time()-start:.2f} Seconds")


if __name__ == "__main__":
    run_scd_type1_product()
