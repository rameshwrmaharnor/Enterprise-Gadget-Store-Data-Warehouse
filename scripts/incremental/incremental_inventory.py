"""
=========================================================
Enterprise Gadget Store Data Warehouse
Incremental Inventory Pipeline

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

PIPELINE_NAME = "inventory_pipeline"

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
            "No Metadata Found For inventory_pipeline"
        )

    return str(df.iloc[0]["last_loaded_value"])


# =========================================================
# Read Incremental Inventory
# =========================================================

def read_incremental_inventory(last_watermark):

    logger.info(
        f"Reading Inventory Greater Than : {last_watermark}"
    )

    query = f"""

    SELECT *

    FROM silver_inventory

    WHERE last_restock_date > '{last_watermark}'

    ORDER BY last_restock_date

    """

    df = pd.read_sql(query, engine)

    logger.info(
        f"Incremental Inventory Read : {len(df):,}"
    )

    return df


# =========================================================
# Read Existing Inventory
# =========================================================

def read_existing_inventory():

    logger.info("Reading Existing Fact Inventory...")

    query = """

    SELECT inventory_id

    FROM fact_inventory

    """

    df = pd.read_sql(query, engine)

    logger.info(
        f"Existing Inventory : {len(df):,}"
    )

    return df
# =========================================================
# Remove Existing Inventory
# =========================================================


def remove_existing_inventory(source_df, existing_df):

    logger.info("=" * 70)
    logger.info("Removing Existing Inventory")
    logger.info("=" * 70)

    if source_df.empty:

        logger.info("No Incremental Records Found")

        return source_df

    if existing_df.empty:

        logger.info("Fact Table Empty")

        return source_df

    existing_inventory = set(existing_df["inventory_id"])

    before = len(source_df)

    source_df = source_df[
        ~source_df["inventory_id"].isin(existing_inventory)
    ].copy()

    after = len(source_df)

    logger.info(f"Before Duplicate Removal : {before:,}")

    logger.info(f"After Duplicate Removal  : {after:,}")

    logger.info(f"Duplicates Removed       : {before-after:,}")

    return source_df


# =========================================================
# Validate Incremental Inventory
# =========================================================

def validate_inventory(df):

    logger.info("=" * 70)
    logger.info("Validating Incremental Inventory")
    logger.info("=" * 70)

    if df.empty:

        logger.info("Nothing To Load")

        return df

    before = len(df)

    df = df.drop_duplicates(
        subset=["inventory_id"]
    )

    logger.info(
        f"Duplicate Inventory Removed : {before-len(df):,}"
    )

    df = df.sort_values("last_restock_date")

    df = df.reset_index(drop=True)

    logger.info(
        f"Inventory Ready For Load : {len(df):,}"
    )

    return df


# =========================================================
# Get Latest Watermark
# =========================================================

def get_new_watermark(df):

    if df.empty:

        return None

    latest = str(df["last_restock_date"].max())

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
            f"Minimum Restock Date : {df['last_restock_date'].min()}"
        )

        logger.info(
            f"Maximum Restock Date : {df['last_restock_date'].max()}"
        )

    logger.info("=" * 70)
# =========================================================
# Load Inventory Into Fact Table
# =========================================================


def load_inventory(df):

    if df.empty:

        logger.info("No New Inventory To Load")

        return

    logger.info("=" * 70)
    logger.info("Loading Incremental Inventory")
    logger.info("=" * 70)

    df.to_sql(

        "fact_inventory",

        engine,

        if_exists="append",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(f"Inventory Loaded : {len(df):,}")


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


def run_incremental_inventory():

    start = time.time()

    logger.info("=" * 70)
    logger.info("INCREMENTAL INVENTORY PIPELINE")
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
        # Read Incremental Inventory
        # ---------------------------------------------

        incremental_df = read_incremental_inventory(
            last_watermark
        )

        # ---------------------------------------------
        # Read Existing Inventory
        # ---------------------------------------------

        existing_df = read_existing_inventory()

        # ---------------------------------------------
        # Remove Existing Records
        # ---------------------------------------------

        incremental_df = remove_existing_inventory(

            incremental_df,

            existing_df

        )

        # ---------------------------------------------
        # Validate
        # ---------------------------------------------

        incremental_df = validate_inventory(

            incremental_df

        )

        load_statistics(

            incremental_df

        )

        if incremental_df.empty:

            logger.info("=" * 70)
            logger.info("No New Inventory Found.")
            logger.info("=" * 70)

            return

        # ---------------------------------------------
        # Load Fact Table
        # ---------------------------------------------

        load_inventory(

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
        logger.info("Incremental Inventory Completed Successfully")
        logger.info("=" * 70)

    except SQLAlchemyError as e:

        logger.exception("Database Error")

        raise e

    except Exception as e:

        logger.exception("Pipeline Failed")

        raise e


# =========================================================
# Execute
# =========================================================

if __name__ == "__main__":

    run_incremental_inventory()
