"""
=========================================================
Enterprise Gadget Store Data Warehouse
Supplier Mart Loader

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


# =========================================================
# Read Supplier Data
# =========================================================

def read_supplier_data():

    logger.info("=" * 70)
    logger.info("Reading Supplier Data")
    logger.info("=" * 70)

    query = """

    SELECT

        s.supplier_key,
        s.supplier_id,
        s.supplier_name,
        s.company_type,
        s.contact_person,
        s.city,
        s.state,
        s.country,
        s.supplier_rating,
        s.payment_terms,
        s.contract_type,
        s.credit_limit,
        s.is_active,

        COUNT(p.product_key) AS total_products,

        ROUND(AVG(p.selling_price),2) AS avg_price,

        ROUND(SUM(p.stock_quantity),2) AS total_stock,

        ROUND(SUM(p.manufacturing_cost),2) AS inventory_cost

    FROM dim_supplier s

    LEFT JOIN dim_product p

        ON s.supplier_id=p.supplier_id

    GROUP BY

        s.supplier_key,
        s.supplier_id,
        s.supplier_name,
        s.company_type,
        s.contact_person,
        s.city,
        s.state,
        s.country,
        s.supplier_rating,
        s.payment_terms,
        s.contract_type,
        s.credit_limit,
        s.is_active

    """

    df = pd.read_sql(query, engine)

    logger.info(f"Rows Read : {len(df):,}")

    return df
# =========================================================
# Transform Supplier Mart
# =========================================================


def transform_supplier_data(df):

    logger.info("=" * 70)
    logger.info("Transforming Supplier Mart")
    logger.info("=" * 70)

    numeric_columns = [

        "total_products",

        "avg_price",

        "total_stock",

        "inventory_cost",

        "supplier_rating"

    ]

    for col in numeric_columns:

        df[col] = df[col].fillna(0)

    # Supplier Category

    df["supplier_category"] = "Small"

    df.loc[
        df["total_products"] >= 5,
        "supplier_category"
    ] = "Medium"

    df.loc[
        df["total_products"] >= 10,
        "supplier_category"
    ] = "Large"

    df.loc[
        df["total_products"] >= 20,
        "supplier_category"
    ] = "Enterprise"

# ===============================================
# Supplier Grade
# ===============================================

    df["supplier_grade"] = "D"

    df.loc[
        df["supplier_rating"] >= 2.5,
        "supplier_grade"
    ] = "C"

    df.loc[
        df["supplier_rating"] >= 3.5,
        "supplier_grade"
    ] = "B"

    df.loc[
        df["supplier_rating"] >= 4.2,
        "supplier_grade"
    ] = "A"

    df.loc[
        df["supplier_rating"] >= 4.8,
        "supplier_grade"
    ] = "A+"

    logger.info(
        f"Supplier Mart Rows : {len(df):,}"
    )

    return df
# =========================================================
# Load Supplier Mart
# =========================================================


def load_supplier_mart(df):

    logger.info("=" * 70)
    logger.info("Loading Supplier Mart")
    logger.info("=" * 70)

    df.to_sql(

        "supplier_mart",

        engine,

        if_exists="replace",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(
        "Supplier Mart Loaded Successfully"
    )


# =========================================================
# Validation
# =========================================================

def validate_supplier_mart():

    logger.info("=" * 70)
    logger.info("Validating Supplier Mart")
    logger.info("=" * 70)

    df = pd.read_sql(

        "SELECT * FROM supplier_mart",

        engine

    )

    logger.info(f"Rows Loaded : {len(df):,}")

    logger.info(

        f"Total Suppliers : {df['supplier_id'].nunique():,}"

    )

    logger.info(

        f"Average Rating : {df['supplier_rating'].mean():.2f}"

    )
# =========================================================
# Main
# =========================================================


def run_supplier_mart():

    start = time.time()

    logger.info("="*70)
    logger.info("Creating Supplier Mart")
    logger.info("="*70)

    df = read_supplier_data()

    df = transform_supplier_data(df)

    load_supplier_mart(df)

    validate_supplier_mart()

    logger.info("="*70)
    logger.info("Supplier Mart Created Successfully")
    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )
    logger.info("="*70)


if __name__ == "__main__":

    run_supplier_mart()
