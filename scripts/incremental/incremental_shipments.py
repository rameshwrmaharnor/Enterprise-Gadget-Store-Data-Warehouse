"""
=========================================================
Enterprise Gadget Store Data Warehouse
Incremental Shipments Pipeline

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

PIPELINE_NAME = "shipments_pipeline"

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
            "No Metadata Found For shipments_pipeline"
        )

    return str(df.iloc[0]["last_loaded_value"])


# =========================================================
# Read Incremental Shipments
# =========================================================

def read_incremental_shipments(last_watermark):

    logger.info(
        f"Reading Shipments Greater Than : {last_watermark}"
    )

    query = f"""

    SELECT *

    FROM silver_shipments

    WHERE dispatch_date > '{last_watermark}'

    ORDER BY dispatch_date

    """

    df = pd.read_sql(query, engine)

    logger.info(
        f"Incremental Shipments Read : {len(df):,}"
    )

    return df


# =========================================================
# Read Existing Shipments
# =========================================================

def read_existing_shipments():

    logger.info("Reading Existing Fact Shipments...")

    query = """

    SELECT shipment_id

    FROM fact_shipments

    """

    df = pd.read_sql(query, engine)

    logger.info(
        f"Existing Shipments : {len(df):,}"
    )

    return df
# =========================================================
# Remove Existing Shipments
# =========================================================


def remove_existing_shipments(source_df, existing_df):

    logger.info("=" * 70)
    logger.info("Removing Existing Shipments")
    logger.info("=" * 70)

    if source_df.empty:

        logger.info("No Incremental Records Found")

        return source_df

    if existing_df.empty:

        logger.info("Fact Table Empty")

        return source_df

    existing_shipments = set(existing_df["shipment_id"])

    before = len(source_df)

    source_df = source_df[
        ~source_df["shipment_id"].isin(existing_shipments)
    ].copy()

    after = len(source_df)

    logger.info(f"Before Duplicate Removal : {before:,}")

    logger.info(f"After Duplicate Removal  : {after:,}")

    logger.info(f"Duplicates Removed       : {before-after:,}")

    return source_df


# =========================================================
# Validate Incremental Shipments
# =========================================================

def validate_shipments(df):

    logger.info("=" * 70)
    logger.info("Validating Incremental Shipments")
    logger.info("=" * 70)

    if df.empty:

        logger.info("Nothing To Load")

        return df

    before = len(df)

    df = df.drop_duplicates(
        subset=["shipment_id"]
    )

    logger.info(
        f"Duplicate Shipments Removed : {before-len(df):,}"
    )

    df = df.sort_values("dispatch_date")

    df = df.reset_index(drop=True)

    logger.info(
        f"Shipments Ready For Load : {len(df):,}"
    )

    return df


# =========================================================
# Get Latest Watermark
# =========================================================

def get_new_watermark(df):

    if df.empty:

        return None

    latest = str(df["dispatch_date"].max())

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
            f"Minimum Dispatch Date : {df['dispatch_date'].min()}"
        )

        logger.info(
            f"Maximum Dispatch Date : {df['dispatch_date'].max()}"
        )

    logger.info("=" * 70)
# =========================================================
# Load Shipments Into Fact Table
# =========================================================


def load_shipments(df):

    if df.empty:

        logger.info("No New Shipments To Load")

        return

    logger.info("=" * 70)
    logger.info("Loading Incremental Shipments")
    logger.info("=" * 70)

    df.to_sql(

        "fact_shipments",

        engine,

        if_exists="append",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(f"Shipments Loaded : {len(df):,}")


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


def run_incremental_shipments():

    start = time.time()

    logger.info("=" * 70)
    logger.info("INCREMENTAL SHIPMENTS PIPELINE")
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
        # Read Incremental Shipments
        # ---------------------------------------------

        incremental_df = read_incremental_shipments(
            last_watermark
        )

        # ---------------------------------------------
        # Read Existing Shipments
        # ---------------------------------------------

        existing_df = read_existing_shipments()

        # ---------------------------------------------
        # Remove Existing Records
        # ---------------------------------------------

        incremental_df = remove_existing_shipments(

            incremental_df,

            existing_df

        )

        # ---------------------------------------------
        # Validate
        # ---------------------------------------------

        incremental_df = validate_shipments(

            incremental_df

        )

        load_statistics(

            incremental_df

        )

        if incremental_df.empty:

            logger.info("=" * 70)
            logger.info("No New Shipments Found.")
            logger.info("=" * 70)

            return

        # ---------------------------------------------
        # Load Fact Table
        # ---------------------------------------------

        load_shipments(

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
        logger.info("Incremental Shipments Completed Successfully")
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

    run_incremental_shipments()
