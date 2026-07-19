"""
=========================================================
Enterprise Gadget Store Data Warehouse
Incremental Orders Pipeline

Author : Rameshwar Maharnor
=========================================================
"""

import time
import logging
import pandas as pd

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from utils.db_connection import engine

# =========================================================
# Logging
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s"
)

logger = logging.getLogger(__name__)

PIPELINE_NAME = "orders_pipeline"

# =========================================================
# Read Metadata
# =========================================================


def get_last_watermark():

    query = f"""

    SELECT last_loaded_value

    FROM incremental_metadata

    WHERE pipeline_name = '{PIPELINE_NAME}'

    """

    df = pd.read_sql(query, engine)

    if df.empty:

        raise Exception(
            "No Metadata Found For orders_pipeline"
        )

    return str(df.iloc[0]["last_loaded_value"])


# =========================================================
# Read Incremental Orders
# =========================================================

def read_incremental_orders(last_watermark):

    logger.info(
        f"Reading Orders Greater Than : {last_watermark}"
    )

    query = f"""

    SELECT *

    FROM silver_orders

    WHERE order_date > '{last_watermark}'

    ORDER BY order_date

    """

    df = pd.read_sql(query, engine)

    logger.info(
        f"Incremental Orders Read : {len(df):,}"
    )

    return df


# =========================================================
# Read Existing Orders
# =========================================================

def read_existing_orders():

    logger.info("Reading Existing Fact Orders...")

    query = """

    SELECT order_id

    FROM fact_orders

    """

    df = pd.read_sql(query, engine)

    logger.info(
        f"Existing Orders : {len(df):,}"
    )

    return df
# =========================================================
# Remove Existing Orders
# =========================================================


def remove_existing_orders(source_df, existing_df):

    logger.info("=" * 70)
    logger.info("Removing Existing Orders")
    logger.info("=" * 70)

    if source_df.empty:

        logger.info("No Incremental Records Found")

        return source_df

    if existing_df.empty:

        logger.info("Fact Table Empty")

        return source_df

    existing_orders = set(existing_df["order_id"])

    before = len(source_df)

    source_df = source_df[
        ~source_df["order_id"].isin(existing_orders)
    ].copy()

    after = len(source_df)

    logger.info(f"Before Duplicate Removal : {before:,}")

    logger.info(f"After Duplicate Removal  : {after:,}")

    logger.info(f"Duplicates Removed       : {before-after:,}")

    return source_df


# =========================================================
# Validate Incremental Data
# =========================================================

def validate_orders(df):

    logger.info("=" * 70)
    logger.info("Validating Incremental Orders")
    logger.info("=" * 70)

    if df.empty:

        logger.info("Nothing To Load")

        return df

    before = len(df)

    df = df.drop_duplicates(subset=["order_id"])

    logger.info(f"Duplicate Orders Removed : {before-len(df):,}")

    df = df.sort_values("order_date")

    df = df.reset_index(drop=True)

    logger.info(f"Orders Ready For Load : {len(df):,}")

    return df


# =========================================================
# Get Latest Watermark
# =========================================================

def get_new_watermark(df):

    if df.empty:

        return None

    latest = str(df["order_date"].max())

    logger.info(f"Latest Watermark : {latest}")

    return latest


# =========================================================
# Prepare Load Statistics
# =========================================================

def load_statistics(df):

    logger.info("=" * 70)

    logger.info("Incremental Statistics")

    logger.info("=" * 70)

    logger.info(f"Rows To Load : {len(df):,}")

    if not df.empty:

        logger.info(f"Minimum Order Date : {df['order_date'].min()}")

        logger.info(f"Maximum Order Date : {df['order_date'].max()}")

    logger.info("=" * 70)
# =========================================================
# Load Orders Into Fact Table
# =========================================================


def load_orders(df):

    if df.empty:

        logger.info("No New Orders To Load")

        return

    logger.info("=" * 70)
    logger.info("Loading Incremental Orders")
    logger.info("=" * 70)

    df.to_sql(

        "fact_orders",

        engine,

        if_exists="append",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(f"Orders Loaded : {len(df):,}")


# =========================================================
# Update Incremental Metadata
# =========================================================

def update_metadata(latest_watermark, rows_loaded):

    logger.info("=" * 70)
    logger.info("Updating Metadata")
    logger.info("=" * 70)

    if latest_watermark is None:

        logger.info("Watermark Not Updated")

        return

    query = text("""

        UPDATE incremental_metadata

        SET

            last_loaded_value = :watermark,

            rows_loaded = rows_loaded + :rows_loaded,

            last_run = NOW(),

            status = 'SUCCESS'

        WHERE pipeline_name = :pipeline

    """)

    with engine.begin() as conn:

        conn.execute(

            query,

            {

                "watermark": latest_watermark,

                "rows_loaded": int(rows_loaded),

                "pipeline": PIPELINE_NAME

            }

        )

    logger.info("Metadata Updated Successfully")


# =========================================================
# Log Summary
# =========================================================

def pipeline_summary(start_time, rows_loaded):

    logger.info("=" * 70)

    logger.info("PIPELINE SUMMARY")

    logger.info("=" * 70)

    logger.info(f"Pipeline        : {PIPELINE_NAME}")

    logger.info(f"Rows Loaded     : {rows_loaded:,}")

    logger.info(
        f"Execution Time  : {time.time()-start_time:.2f} Seconds"
    )

    logger.info("=" * 70)
# =========================================================
# Main Pipeline
# =========================================================


def run_incremental_orders():

    start = time.time()

    logger.info("=" * 70)
    logger.info("INCREMENTAL ORDERS PIPELINE")
    logger.info("=" * 70)

    try:

        # ---------------------------------------------
        # Read Watermark
        # ---------------------------------------------

        last_watermark = get_last_watermark()

        logger.info(
            f"Last Watermark : {last_watermark}"
        )

        # ---------------------------------------------
        # Read Incremental Orders
        # ---------------------------------------------

        incremental_df = read_incremental_orders(
            last_watermark
        )

        # ---------------------------------------------
        # Read Existing Orders
        # ---------------------------------------------

        existing_df = read_existing_orders()

        # ---------------------------------------------
        # Remove Existing Orders
        # ---------------------------------------------

        incremental_df = remove_existing_orders(

            incremental_df,

            existing_df

        )

        # ---------------------------------------------
        # Validate
        # ---------------------------------------------

        incremental_df = validate_orders(

            incremental_df

        )

        load_statistics(

            incremental_df

        )

        if incremental_df.empty:

            logger.info("=" * 70)

            logger.info(
                "No New Records Found."
            )

            logger.info("=" * 70)

            return

        # ---------------------------------------------
        # Load Fact Table
        # ---------------------------------------------

        load_orders(

            incremental_df

        )

        # ---------------------------------------------
        # Update Metadata
        # ---------------------------------------------

        latest_watermark = get_new_watermark(

            incremental_df

        )

        update_metadata(

            latest_watermark,

            len(incremental_df)

        )

        pipeline_summary(

            start,

            len(incremental_df)

        )

        logger.info("=" * 70)

        logger.info(
            "Incremental Orders Completed Successfully"
        )

        logger.info("=" * 70)

    except SQLAlchemyError as e:

        logger.exception(
            "Database Error"
        )

        raise e

    except Exception as e:

        logger.exception(
            "Pipeline Failed"
        )

        raise e


# =========================================================
# Execute
# =========================================================

if __name__ == "__main__":

    run_incremental_orders()
