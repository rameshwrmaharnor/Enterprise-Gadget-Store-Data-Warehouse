"""
=========================================================
Enterprise Gadget Store Data Warehouse
Payment Mart Loader

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
# Read Payment Data
# =========================================================

def read_payment_data():

    logger.info("=" * 70)
    logger.info("Reading Payment Data")
    logger.info("=" * 70)

    query = """

    SELECT

        p.payment_id,

        p.order_id,

        p.date_key,

        p.transaction_id,

        p.payment_gateway,

        p.payment_method,

        p.payment_amount,

        p.payment_status,

        p.payment_date,

        p.bank_name,

        p.card_type,

        p.currency,

        o.customer_key,

        o.total_amount,

        c.customer_segment,

        c.state,

        c.country

    FROM fact_payments p

    LEFT JOIN fact_orders o

        ON p.order_id=o.order_id

    LEFT JOIN dim_customer c

        ON o.customer_key=c.customer_key

    """

    df = pd.read_sql(query, engine)

    logger.info(f"Rows Read : {len(df):,}")

    return df
# =========================================================
# Transform Payment Mart
# =========================================================

def transform_payment_data(df):

    logger.info("=" * 70)
    logger.info("Transforming Payment Mart")
    logger.info("=" * 70)

    numeric_cols = [

        "payment_amount",

        "total_amount"

    ]

    for col in numeric_cols:

        df[col] = df[col].fillna(0)

    # ============================================
    # Payment Success
    # ============================================

    df["payment_success"] = 0

    df.loc[

        df["payment_status"]=="Paid",

        "payment_success"

    ] = 1

    # ============================================
    # Payment Failure
    # ============================================

    df["payment_failure"] = 1 - df["payment_success"]

    # ============================================
    # Revenue Band
    # ============================================

    df["payment_band"] = "Low"

    df.loc[
        df["payment_amount"]>=10000,
        "payment_band"
    ]="Medium"

    df.loc[
        df["payment_amount"]>=50000,
        "payment_band"
    ]="High"

    df.loc[
        df["payment_amount"]>=100000,
        "payment_band"
    ]="Premium"

    logger.info(f"Rows Ready : {len(df):,}")

    return df
# =========================================================
# Load Payment Mart
# =========================================================

def load_payment_mart(df):

    logger.info("=" * 70)
    logger.info("Loading Payment Mart")
    logger.info("=" * 70)

    df.to_sql(

        "payment_mart",

        engine,

        if_exists="replace",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info("Payment Mart Loaded Successfully")


# =========================================================
# Validation
# =========================================================

def validate_payment_mart():

    logger.info("=" * 70)
    logger.info("Validating Payment Mart")
    logger.info("=" * 70)

    df=pd.read_sql(

        "SELECT * FROM payment_mart",

        engine

    )

    logger.info(f"Rows Loaded : {len(df):,}")

    logger.info(

        f"Total Revenue : {df['payment_amount'].sum():,.2f}"

    )

    logger.info(

        f"Successful Payments : {(df['payment_success']==1).sum():,}"

    )

    logger.info(

        f"Failed Payments : {(df['payment_failure']==1).sum():,}"

    )
# =========================================================
# Main
# =========================================================

def run_payment_mart():

    start=time.time()

    logger.info("="*70)
    logger.info("Creating Payment Mart")
    logger.info("="*70)

    df=read_payment_data()

    df=transform_payment_data(df)

    load_payment_mart(df)

    validate_payment_mart()

    logger.info("="*70)
    logger.info("Payment Mart Created Successfully")
    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )
    logger.info("="*70)


if __name__=="__main__":
 
    run_payment_mart()
