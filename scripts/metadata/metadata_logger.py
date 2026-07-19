"""
=========================================================
Enterprise Gadget Store Data Warehouse
Metadata Logger

Author : Rameshwar Maharnor
=========================================================
"""

import logging
from datetime import datetime

import pandas as pd

from sqlalchemy import text

from utils.db_connection import engine


logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)-8s | %(message)s"

)

logger = logging.getLogger(__name__)


# =========================================================
# Create Metadata Table
# =========================================================

def create_metadata_table():

    query = """

    CREATE TABLE IF NOT EXISTS etl_metadata(

        metadata_id BIGINT AUTO_INCREMENT PRIMARY KEY,

        pipeline_name VARCHAR(100),

        layer_name VARCHAR(50),

        source_table VARCHAR(100),

        target_table VARCHAR(100),

        rows_processed BIGINT,

        start_time DATETIME,

        end_time DATETIME,

        execution_time DOUBLE,

        status VARCHAR(30),

        remarks TEXT

    )

    """

    with engine.begin() as conn:

        conn.execute(text(query))

    logger.info("Metadata Table Ready")


# =========================================================
# Insert Metadata
# =========================================================

def insert_metadata(

    pipeline_name,

    layer_name,

    source_table,

    target_table,

    rows_processed,

    start_time,

    end_time,

    status,

    remarks=""

):

    execution_time = (

        end_time-start_time

    ).total_seconds()

    query = text("""

    INSERT INTO etl_metadata(

        pipeline_name,

        layer_name,

        source_table,

        target_table,

        rows_processed,

        start_time,

        end_time,

        execution_time,

        status,

        remarks

    )

    VALUES(

        :pipeline_name,

        :layer_name,

        :source_table,

        :target_table,

        :rows_processed,

        :start_time,

        :end_time,

        :execution_time,

        :status,

        :remarks

    )

    """)

    with engine.begin() as conn:

        conn.execute(

            query,

            {

                "pipeline_name": pipeline_name,

                "layer_name": layer_name,

                "source_table": source_table,

                "target_table": target_table,

                "rows_processed": rows_processed,

                "start_time": start_time,

                "end_time": end_time,

                "execution_time": execution_time,

                "status": status,

                "remarks": remarks

            }

        )

    logger.info("Metadata Logged Successfully")


# =========================================================
# Read Metadata
# =========================================================

def read_metadata():

    df = pd.read_sql(

        "SELECT * FROM etl_metadata ORDER BY metadata_id DESC",

        engine

    )

    return df


# =========================================================
# Demo
# =========================================================

if __name__ == "__main__":

    create_metadata_table()

    insert_metadata(

        pipeline_name="Gold Pipeline",

        layer_name="Gold",

        source_table="silver_orders",

        target_table="fact_orders",

        rows_processed=1868465,

        start_time=datetime.now(),

        end_time=datetime.now(),

        status="SUCCESS",

        remarks="Initial Load"

    )

    print(read_metadata())
