"""
=========================================================
Enterprise Gadget Store Data Warehouse
Inventory Mart Loader

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


def read_inventory_data():

    logger.info("=" * 70)
    logger.info("Reading Inventory Data")
    logger.info("=" * 70)

    query = """

    SELECT

        i.inventory_id,

        i.product_key,

        p.product_name,

        p.brand,

        c.category_name,

        i.warehouse,

        i.stock_quantity,

        i.available_stock,

        i.reserved_stock,

        i.damaged_stock,

        i.reorder_level,

        i.reorder_status,

        i.last_restock_date,

        i.inventory_value,

        p.selling_price,

        p.manufacturing_cost,

        p.rating

    FROM fact_inventory i

    LEFT JOIN dim_product p

        ON i.product_key = p.product_key

    LEFT JOIN dim_category c

        ON p.category_id = c.category_id

    """

    df = pd.read_sql(query, engine)

    logger.info(f"Rows Read : {len(df):,}")

    return df
# =========================================================
# Transform Inventory Mart
# =========================================================


def transform_inventory_data(df):

    logger.info("=" * 70)
    logger.info("Transforming Inventory Mart")
    logger.info("=" * 70)

    # ===============================================
    # Fill NULL Values
    # ===============================================

    numeric_columns = [

        "stock_quantity",

        "available_stock",

        "reserved_stock",

        "damaged_stock",

        "reorder_level",

        "inventory_value",

        "selling_price",

        "manufacturing_cost",

        "rating"

    ]

    for col in numeric_columns:

        df[col] = df[col].fillna(0)

    # ===============================================
    # Inventory Status
    # ===============================================

    df["inventory_status"] = "Out of Stock"

    df.loc[
        df["available_stock"] > 0,
        "inventory_status"
    ] = "Available"

    df.loc[
        df["available_stock"] >= 100,
        "inventory_status"
    ] = "Healthy"

    df.loc[
        df["available_stock"] >= 500,
        "inventory_status"
    ] = "Excellent"

    # ===============================================
    # Stock Health
    # ===============================================

    df["stock_health"] = "Critical"

    df.loc[
        df["stock_quantity"] >= df["reorder_level"],
        "stock_health"
    ] = "Normal"

    df.loc[
        df["stock_quantity"] >=
        (df["reorder_level"] * 2),
        "stock_health"
    ] = "Good"

    # ===============================================
    # Inventory Value Band
    # ===============================================

    df["inventory_value_band"] = "Low"

    df.loc[
        df["inventory_value"] >= 100000,
        "inventory_value_band"
    ] = "Medium"

    df.loc[
        df["inventory_value"] >= 500000,
        "inventory_value_band"
    ] = "High"

    df.loc[
        df["inventory_value"] >= 1000000,
        "inventory_value_band"
    ] = "Premium"

    # ===============================================
    # Stock Utilization
    # ===============================================

    df["stock_utilization_percent"] = (

        df["available_stock"]

        /

        df["stock_quantity"].replace(0, 1)

    ) * 100

    df["stock_utilization_percent"] = (

        df["stock_utilization_percent"]

        .round(2)

    )

    logger.info(
        f"Inventory Mart Rows : {len(df):,}"
    )

    return df
# =========================================================
# Load Inventory Mart
# =========================================================


def load_inventory_mart(df):

    logger.info("=" * 70)
    logger.info("Loading Inventory Mart")
    logger.info("=" * 70)

    df.to_sql(

        "inventory_mart",

        engine,

        if_exists="replace",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(
        "Inventory Mart Loaded Successfully"
    )


# =========================================================
# Validate Inventory Mart
# =========================================================

def validate_inventory_mart():

    logger.info("=" * 70)
    logger.info("Validating Inventory Mart")
    logger.info("=" * 70)

    df = pd.read_sql(

        "SELECT * FROM inventory_mart",

        engine

    )

    logger.info(
        f"Rows Loaded : {len(df):,}"
    )

    duplicate_inventory = (

        df["inventory_id"]

        .duplicated()

        .sum()

    )

    logger.info(
        f"Duplicate Inventory IDs : {duplicate_inventory}"
    )

    total_inventory_value = round(

        df["inventory_value"].sum(),

        2

    )

    logger.info(
        f"Total Inventory Value : {total_inventory_value:,.2f}"
    )

    logger.info(
        "Inventory Mart Validation Successful"
    )


# =========================================================
# Create Performance Indexes
# =========================================================

def create_indexes():

    logger.info("=" * 70)
    logger.info("Creating Inventory Mart Indexes")
    logger.info("=" * 70)

    from sqlalchemy import text

    queries = [

        """

        CREATE INDEX idx_inventory_mart_inventory

        ON inventory_mart(inventory_id(30))

        """,

        """

        CREATE INDEX idx_inventory_mart_product

        ON inventory_mart(product_key)

        """,

        """

        CREATE INDEX idx_inventory_mart_brand

        ON inventory_mart(brand(50))

        """,

        """

        CREATE INDEX idx_inventory_mart_category

        ON inventory_mart(category_name(50))

        """

    ]

    with engine.begin() as conn:

        for query in queries:

            try:

                conn.execute(text(query))

            except Exception:

                pass

    logger.info(
        "Indexes Created Successfully"
    )


# =========================================================
# Pipeline Summary
# =========================================================

def pipeline_summary(start):

    logger.info("=" * 70)

    logger.info(
        "Inventory Mart Completed Successfully"
    )

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )

    logger.info("=" * 70)
# =========================================================
# Main Function
# =========================================================


def run_inventory_mart():

    start = time.time()

    logger.info("=" * 70)
    logger.info("Creating Inventory Mart")
    logger.info("=" * 70)

    try:

        # ------------------------------------------
        # Read Data
        # ------------------------------------------

        df = read_inventory_data()

        # ------------------------------------------
        # Transform Data
        # ------------------------------------------

        df = transform_inventory_data(df)

        # ------------------------------------------
        # Load Mart
        # ------------------------------------------

        load_inventory_mart(df)

        # ------------------------------------------
        # Validation
        # ------------------------------------------

        validate_inventory_mart()

        # ------------------------------------------
        # Create Indexes
        # ------------------------------------------

        create_indexes()

        # ------------------------------------------
        # Summary
        # ------------------------------------------

        pipeline_summary(start)

    except Exception as e:

        logger.exception(
            "Inventory Mart Failed"
        )

        raise e


# =========================================================
# Execute
# =========================================================

if __name__ == "__main__":

    run_inventory_mart()
