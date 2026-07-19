"""
=========================================================
Enterprise Gadget Store Data Warehouse
Sales Mart Loader

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
# Read Sales Data
# =========================================================

def read_sales_data():

    logger.info("=" * 70)
    logger.info("Reading Sales Data")
    logger.info("=" * 70)

    query = """

    SELECT

        o.order_id,
        o.customer_key,
        o.coupon_key,
        o.date_key,

        o.subtotal,
        o.discount_amount,
        o.tax_amount,
        o.shipping_charge,
        o.total_amount,

        o.payment_method,
        o.payment_status,
        o.order_status,
        o.delivery_type,

        c.customer_segment,
        c.state,
        c.country,

        d.year,
        d.quarter,
        d.month,
        d.month_name

    FROM fact_orders o

    LEFT JOIN dim_customer c

        ON o.customer_key=c.customer_key

    LEFT JOIN dim_date d

        ON o.date_key=d.date_key

    """

    df = pd.read_sql(query, engine)

    logger.info(f"Rows Read : {len(df):,}")

    return df
# =========================================================
# Transform Sales Mart
# =========================================================

def transform_sales_data(df):

    logger.info("=" * 70)
    logger.info("Transforming Sales Mart")
    logger.info("=" * 70)

    # =====================================================
    # Fill NULL Values
    # =====================================================

    numeric_columns = [

        "subtotal",

        "discount_amount",

        "tax_amount",

        "shipping_charge",

        "total_amount"

    ]

    for col in numeric_columns:

        df[col] = df[col].fillna(0)

    # =====================================================
    # Net Sales
    # =====================================================

    df["net_sales"] = (

        df["subtotal"]

        - df["discount_amount"]

        + df["tax_amount"]

        + df["shipping_charge"]

    )

    # =====================================================
    # Discount %
    # =====================================================

    df["discount_percent"] = (

        df["discount_amount"]

        /

        df["subtotal"].replace(0, 1)

    ) * 100

    df["discount_percent"] = (

        df["discount_percent"]

        .round(2)

    )

    # =====================================================
    # Sales Band
    # =====================================================

    df["sales_band"] = "Low"

    df.loc[
        df["total_amount"] >= 10000,
        "sales_band"
    ] = "Medium"

    df.loc[
        df["total_amount"] >= 50000,
        "sales_band"
    ] = "High"

    df.loc[
        df["total_amount"] >= 100000,
        "sales_band"
    ] = "Premium"

    # =====================================================
    # Order Size
    # =====================================================

    df["order_size"] = "Small"

    df.loc[
        df["total_amount"] >= 20000,
        "order_size"
    ] = "Medium"

    df.loc[
        df["total_amount"] >= 80000,
        "order_size"
    ] = "Large"

    # =====================================================
    # Payment Success Flag
    # =====================================================

    df["payment_success"] = 0

    df.loc[
        df["payment_status"] == "Paid",
        "payment_success"
    ] = 1

    logger.info(
        f"Sales Mart Rows : {len(df):,}"
    )

    return df
# =========================================================
# Load Sales Mart
# =========================================================

def load_sales_mart(df):

    logger.info("=" * 70)
    logger.info("Loading Sales Mart")
    logger.info("=" * 70)

    df.to_sql(

        "sales_mart",

        engine,

        if_exists="replace",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(
        "Sales Mart Loaded Successfully"
    )


# =========================================================
# Validation
# =========================================================

def validate_sales_mart():

    logger.info("=" * 70)
    logger.info("Validating Sales Mart")
    logger.info("=" * 70)

    df = pd.read_sql(

        "SELECT * FROM sales_mart",

        engine

    )

    logger.info(
        f"Rows Loaded : {len(df):,}"
    )

    logger.info(
        f"Total Revenue : {df['total_amount'].sum():,.2f}"
    )

    logger.info(
        f"Average Order Value : {df['total_amount'].mean():,.2f}"
    )

    logger.info(
        "Sales Mart Validation Successful"
    )
# =========================================================
# Main
# =========================================================

def run_sales_mart():

    start = time.time()

    logger.info("=" * 70)
    logger.info("Creating Sales Mart")
    logger.info("=" * 70)

    df = read_sales_data()

    df = transform_sales_data(df)

    load_sales_mart(df)

    validate_sales_mart()

    logger.info("=" * 70)
    logger.info("Sales Mart Created Successfully")
    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )
    logger.info("=" * 70)


# =========================================================
# Execute
# =========================================================

if __name__ == "__main__":

    run_sales_mart()