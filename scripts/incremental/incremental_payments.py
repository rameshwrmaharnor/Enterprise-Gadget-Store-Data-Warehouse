"""
=========================================================
Enterprise Gadget Store Data Warehouse
Incremental Payments Pipeline

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

PIPELINE_NAME = "payments_pipeline"

# =========================================================
# Read Metadata
# =========================================================


def get_last_watermark():

    query = f"""

    SELECT last_loaded_value

    FROM incremental_metadata

    WHERE pipeline_name='{PIPELINE_NAME}'

    """

    df = pd.read_sql(query, engine)

    if df.empty:

        raise Exception(
            "No Metadata Found For payments_pipeline"
        )

    return str(df.iloc[0]["last_loaded_value"])


# =========================================================
# Read Incremental Payments
# =========================================================

def read_incremental_payments(last_watermark):

    logger.info(
        f"Reading Payments Greater Than : {last_watermark}"
    )

    query = f"""

    SELECT *

    FROM silver_payments

    WHERE payment_date > '{last_watermark}'

    ORDER BY payment_date

    """

    df = pd.read_sql(query, engine)

    logger.info(
        f"Incremental Payments Read : {len(df):,}"
    )

    return df


# =========================================================
# Read Existing Payments
# =========================================================

def read_existing_payments():

    logger.info("Reading Existing Fact Payments...")

    query = """

    SELECT payment_id

    FROM fact_payments

    """

    df = pd.read_sql(query, engine)

    logger.info(
        f"Existing Payments : {len(df):,}"
    )

    return df
# =========================================================
# Remove Existing Payments
# =========================================================


def remove_existing_payments(source_df, existing_df):

    logger.info("=" * 70)
    logger.info("Removing Existing Payments")
    logger.info("=" * 70)

    if source_df.empty:

        logger.info("No Incremental Records Found")

        return source_df

    if existing_df.empty:

        logger.info("Fact Table Empty")

        return source_df

    existing_payments = set(existing_df["payment_id"])

    before = len(source_df)

    source_df = source_df[
        ~source_df["payment_id"].isin(existing_payments)
    ].copy()

    after = len(source_df)

    logger.info(f"Before Duplicate Removal : {before:,}")

    logger.info(f"After Duplicate Removal  : {after:,}")

    logger.info(f"Duplicates Removed       : {before-after:,}")

    return source_df


# =========================================================
# Validate Incremental Payments
# =========================================================

def validate_payments(df):

    logger.info("=" * 70)
    logger.info("Validating Incremental Payments")
    logger.info("=" * 70)

    if df.empty:

        logger.info("Nothing To Load")

        return df

    before = len(df)

    df = df.drop_duplicates(
        subset=["payment_id"]
    )

    logger.info(
        f"Duplicate Payments Removed : {before-len(df):,}"
    )

    df = df.sort_values("payment_date")

    df = df.reset_index(drop=True)

    logger.info(
        f"Payments Ready For Load : {len(df):,}"
    )

    return df


# =========================================================
# Get Latest Watermark
# =========================================================

def get_new_watermark(df):

    if df.empty:

        return None

    latest = str(df["payment_date"].max())

    logger.info(
        f"Latest Watermark : {latest}"
    )

    return latest


# =========================================================
# Pipeline Statistics
# =========================================================

def load_statistics(df):

    logger.info("=" * 70)

    logger.info("Incremental Statistics")

    logger.info("=" * 70)

    logger.info(
        f"Rows To Load : {len(df):,}"
    )

    if not df.empty:

        logger.info(
            f"Minimum Payment Date : {df['payment_date'].min()}"
        )

        logger.info(
            f"Maximum Payment Date : {df['payment_date'].max()}"
        )

    logger.info("=" * 70)
# =========================================================
# Load Payments Into Fact Table
# =========================================================


def load_payments(df):

    if df.empty:

        logger.info("No New Payments To Load")

        return

    logger.info("=" * 70)
    logger.info("Loading Incremental Payments")
    logger.info("=" * 70)

    df.to_sql(

        "fact_payments",

        engine,

        if_exists="append",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(f"Payments Loaded : {len(df):,}")


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
# Pipeline Summary
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


def run_incremental_payments():

    start = time.time()

    logger.info("=" * 70)
    logger.info("INCREMENTAL PAYMENTS PIPELINE")
    logger.info("=" * 70)

    try:

        # ---------------------------------------------
        # Read Last Watermark
        # ---------------------------------------------

        last_watermark = get_last_watermark()

        logger.info(
            f"Last Watermark : {last_watermark}"
        )

        # ---------------------------------------------
        # Read Incremental Payments
        # ---------------------------------------------

        incremental_df = read_incremental_payments(
            last_watermark
        )

        # ---------------------------------------------
        # Read Existing Payments
        # ---------------------------------------------

        existing_df = read_existing_payments()

        # ---------------------------------------------
        # Remove Existing Records
        # ---------------------------------------------

        incremental_df = remove_existing_payments(

            incremental_df,

            existing_df

        )

        # ---------------------------------------------
        # Validate
        # ---------------------------------------------

        incremental_df = validate_payments(

            incremental_df

        )

        load_statistics(

            incremental_df

        )

        if incremental_df.empty:

            logger.info("=" * 70)
            logger.info("No New Payments Found.")
            logger.info("=" * 70)

            return

        # ---------------------------------------------
        # Load Fact Table
        # ---------------------------------------------

        load_payments(

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
        logger.info("Incremental Payments Completed Successfully")
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

    run_incremental_payments()
