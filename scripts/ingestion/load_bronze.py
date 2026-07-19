"""
=========================================================
Enterprise Gadget Store Data Warehouse
Bronze Layer Loader

Author : Rameshwar Maharnor
Version : 2.0.0
=========================================================
"""

import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from utils.config import config
from utils.db_connection import engine
from utils.logger import logger


class BronzeLoader:
    """
    Enterprise Bronze Layer Loader
    """

    def __init__(self):

        self.start_time = time.time()

        self.engine = engine

        self.inspector = inspect(self.engine)

        self.raw_folder = Path(
            config["paths"]["raw"]
        )

        self.log_folder = Path(
            config["paths"]["logs"]
        )

        self.log_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.batch_size = 10000

        self.datasets = {

            "categories": "categories.csv",

            "suppliers": "suppliers.csv",

            "products": "products.csv",

            "customers": "customers.csv",

            "coupons": "coupons.csv",

            "orders": "orders.csv",

            "payments": "payments.csv",

            "shipments": "shipments.csv",

            "inventory": "inventory.csv"

        }

        logger.info("=" * 70)
        logger.info("Bronze Loader Initialized")
        logger.info("=" * 70)

    def cleanup_tables(self):
        """
        Drop Existing Bronze Tables
        """

        logger.info("=" * 70)
        logger.info("Cleaning Bronze Tables...")
        logger.info("=" * 70)

        with self.engine.begin() as conn:

            for table in self.datasets.keys():

                table_name = f"bronze_{table}"

                conn.execute(
                    text(
                        f"DROP TABLE IF EXISTS {table_name}"
                    )
                )

                logger.info(
                    f"Dropped : {table_name}"
                )

        logger.info("Cleanup Completed.")

    def load_dataset(
        self,
        table_name,
        file_name
    ):
        """
        Load One CSV into Bronze Table
        """

        file_path = self.raw_folder / file_name

        if not file_path.exists():

            raise FileNotFoundError(
                f"{file_path} not found."
            )

        logger.info(
            f"Loading {file_name}..."
        )

        total_rows = 0

        chunk_number = 1

        for chunk in pd.read_csv(
            file_path,
            chunksize=self.batch_size
        ):

            mode = (
                "replace"
                if chunk_number == 1
                else "append"
            )

            chunk.to_sql(

                name=f"bronze_{table_name}",

                con=self.engine,

                if_exists=mode,

                index=False,

                method="multi",

                chunksize=1000

            )

            total_rows += len(chunk)

            logger.info(

                f"{table_name.upper()} | "

                f"Chunk {chunk_number} | "

                f"{len(chunk):,} Rows | "

                f"Total : {total_rows:,}"

            )

            chunk_number += 1

        logger.info(

            f"{table_name.upper()} Loaded "

            f"({total_rows:,} Rows)"

        )

        return total_rows

    def load_all_datasets(self):
        """
        Load All CSV Files into Bronze Layer
        """

        logger.info("=" * 70)
        logger.info("Loading All Bronze Datasets...")
        logger.info("=" * 70)

        summary = []

        for table_name, file_name in self.datasets.items():

            start = time.time()

            rows_loaded = self.load_dataset(
                table_name,
                file_name
            )

            elapsed = round(
                time.time() - start,
                2
            )

            summary.append({

                "table_name": f"bronze_{table_name}",

                "rows_loaded": rows_loaded,

                "load_time_seconds": elapsed

            })

        logger.info("=" * 70)
        logger.info("All Datasets Loaded Successfully")
        logger.info("=" * 70)

        return pd.DataFrame(summary)

    def validate_tables(self):
        """
        Validate Bronze Tables
        """

        logger.info("Validating Bronze Tables...")

        missing_tables = []

        with self.engine.connect() as conn:

            for table_name in self.datasets.keys():

                bronze_table = f"bronze_{table_name}"

                result = conn.execute(

                    text(

                        """
                        SELECT COUNT(*)
                        FROM information_schema.tables
                        WHERE table_schema = DATABASE()
                        AND table_name = :table
                        """

                    ),

                    {"table": bronze_table}

                )

                exists = result.scalar()

                if exists == 0:

                    missing_tables.append(
                        bronze_table
                    )

        if missing_tables:

            raise Exception(

                f"Missing Bronze Tables : {missing_tables}"

            )

        logger.info(
            "Bronze Validation Successful."
        )

    def generate_metadata(
        self,
        summary_df
    ):
        """
        Generate Bronze ETL Metadata
        """

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        metadata = {

            "layer": "bronze",

            "database": config["database"]["database"],

            "tables_loaded": len(summary_df),

            "total_rows_loaded": int(
                summary_df["rows_loaded"].sum()
            ),

            "execution_time_seconds": execution_time,

            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "tables": summary_df.to_dict(
                orient="records"
            )

        }

        metadata_file = (
            self.log_folder /
            "bronze_load_metadata.json"
        )

        with open(
            metadata_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

        logger.info(
            f"Metadata Saved : {metadata_file}"
        )

    def print_summary(
        self,
        summary_df
    ):
        """
        Print Bronze ETL Summary
        """

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        total_rows = int(
            summary_df["rows_loaded"].sum()
        )

        print("\n" + "=" * 90)
        print(" Enterprise Gadget Store - Bronze Layer")
        print("=" * 90)

        print(f"Datasets Loaded      : {len(summary_df)}")
        print(f"Total Rows Loaded    : {total_rows:,}")
        print(f"Execution Time       : {execution_time} Seconds")
        print(f"Database             : {config['database']['database']}")

        print("=" * 90)

        print("\nTable Summary\n")

        print(summary_df)

        print("\n" + "=" * 90)
        print("Bronze Layer Loaded Successfully")
        print("=" * 90)

    def run(self):
        """
        Execute Bronze ETL
        """

        try:

            logger.info("=" * 70)
            logger.info("Bronze ETL Started")
            logger.info("=" * 70)

            self.cleanup_tables()

            summary_df = self.load_all_datasets()

            self.validate_tables()

            self.generate_metadata(
                summary_df
            )

            self.print_summary(
                summary_df
            )

            logger.info("=" * 70)
            logger.info("Bronze ETL Completed Successfully")
            logger.info("=" * 70)

        except Exception as error:

            logger.exception(error)

            raise


def main():
    """
    Main Entry Point
    """

    loader = BronzeLoader()

    loader.run()


if __name__ == "__main__":

    main()
