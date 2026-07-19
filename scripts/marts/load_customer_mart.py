"""
=========================================================
Enterprise Gadget Store Data Warehouse
Customer Mart

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


def read_customer_data():

    logger.info("=" * 70)
    logger.info("Reading Customer Data")
    logger.info("=" * 70)

    query = """

    SELECT

        c.customer_key,

        c.customer_id,

        c.first_name,

        c.last_name,

        c.gender,

        c.city,

        c.state,

        c.country,

        c.customer_segment,

        c.loyalty_points,

        c.account_status,

        COUNT(o.order_id) AS total_orders,

        ROUND(SUM(o.total_amount),2) AS total_spent,

        ROUND(AVG(o.total_amount),2) AS average_order_value,

        MAX(o.total_amount) AS highest_order,

        MIN(o.total_amount) AS lowest_order

    FROM dim_customer c

    LEFT JOIN fact_orders o

        ON c.customer_key = o.customer_key

    GROUP BY

        c.customer_key,

        c.customer_id,

        c.first_name,

        c.last_name,

        c.gender,

        c.city,

        c.state,

        c.country,

        c.customer_segment,

        c.loyalty_points,

        c.account_status

    """

    df = pd.read_sql(query, engine)

    logger.info(f"Rows Read : {len(df):,}")

    return df
# =========================================================
# Clean Customer Mart
# =========================================================

def transform_customer_data(df):

    logger.info("=" * 70)
    logger.info("Transforming Customer Mart")
    logger.info("=" * 70)

    # Fill NULL Measures

    df["total_orders"] = df["total_orders"].fillna(0).astype(int)

    df["total_spent"] = df["total_spent"].fillna(0)

    df["average_order_value"] = df["average_order_value"].fillna(0)

    df["highest_order"] = df["highest_order"].fillna(0)

    df["lowest_order"] = df["lowest_order"].fillna(0)

    # ===============================================
    # Customer Value Classification
    # ===============================================

    df["customer_value"] = "Low"

    df.loc[
        df["total_spent"] >= 50000,
        "customer_value"
    ] = "Medium"

    df.loc[
        df["total_spent"] >= 200000,
        "customer_value"
    ] = "High"

    df.loc[
        df["total_spent"] >= 500000,
        "customer_value"
    ] = "Premium"

    # ===============================================
    # Customer Activity
    # ===============================================

    df["customer_activity"] = "Inactive"

    df.loc[
        df["total_orders"] >= 1,
        "customer_activity"
    ] = "Active"

    df.loc[
        df["total_orders"] >= 10,
        "customer_activity"
    ] = "Frequent"

    df.loc[
        df["total_orders"] >= 30,
        "customer_activity"
    ] = "VIP"

    # ===============================================
    # Ranking
    # ===============================================

    df["customer_rank"] = (

        df["total_spent"]

        .rank(

            ascending=False,

            method="dense"

        )

        .astype(int)

    )

    logger.info(
        f"Customer Mart Rows : {len(df):,}"
    )

    return df
# =========================================================
# Load Customer Mart
# =========================================================

def load_customer_mart(df):

    logger.info("=" * 70)
    logger.info("Loading Customer Mart")
    logger.info("=" * 70)

    df.to_sql(

        "customer_mart",

        engine,

        if_exists="replace",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(
        "Customer Mart Loaded Successfully"
    )


# =========================================================
# Validation
# =========================================================

def validate_customer_mart():

    logger.info("=" * 70)
    logger.info("Validating Customer Mart")
    logger.info("=" * 70)

    df = pd.read_sql(

        "SELECT * FROM customer_mart",

        engine

    )

    logger.info(
        f"Rows Loaded : {len(df):,}"
    )

    duplicate_customers = (

        df["customer_id"]

        .duplicated()

        .sum()

    )

    logger.info(
        f"Duplicate Customers : {duplicate_customers}"
    )

    logger.info(
        "Customer Mart Validation Successful"
    )


# =========================================================
# Pipeline Summary
# =========================================================

def pipeline_summary(start):

    logger.info("=" * 70)

    logger.info(
        "Customer Mart Completed Successfully"
    )

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )

    logger.info("=" * 70)
# =========================================================
# Main
# =========================================================

def run_customer_mart():

    start = time.time()

    logger.info("=" * 70)
    logger.info("Creating Customer Mart")
    logger.info("=" * 70)

    df = read_customer_data()

    df = transform_customer_data(df)

    load_customer_mart(df)

    validate_customer_mart()

    pipeline_summary(start)


# =========================================================
# Execute
# =========================================================

if __name__ == "__main__":

    run_customer_mart()