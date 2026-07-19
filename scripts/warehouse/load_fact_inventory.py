"""
=========================================================
Enterprise Gadget Store Data Warehouse
Fact Inventory Loader

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import time

import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class FactInventoryLoader:

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "silver_inventory"

        self.target_table = "fact_inventory"

        logger.info("=" * 70)
        logger.info("Fact Inventory Loader Started")
        logger.info("=" * 70)

    def extract(self):
        """
        Extract Inventory and Product Dimension
        """

        logger.info(
            "Reading Silver Inventory..."
        )

        inventory = pd.read_sql(
            """
            SELECT *
            FROM silver_inventory
            """,
            engine
        )

        logger.info(
            f"Inventory Read : {len(inventory):,}"
        )

        # -----------------------------------------
        # Read Product Dimension
        # -----------------------------------------

        products = pd.read_sql(
            """
            SELECT

                product_key,

                product_id

            FROM dim_product
            """,
            engine
        )

        # -----------------------------------------
        # Merge Product Dimension
        # -----------------------------------------

        inventory = inventory.merge(

            products,

            how="left",

            on="product_id"

        )

        logger.info(
            "Product Mapping Completed."
        )

        return inventory

    def transform(
        self,
        df
    ):
        """
        Transform Inventory Fact
        """

        logger.info(
            "Transforming Fact Inventory..."
        )

        # -----------------------------------------
        # Missing Product Keys
        # -----------------------------------------

        df["product_key"] = (

            df["product_key"]

            .fillna(0)

            .astype(int)

        )

        # -----------------------------------------
        # Numeric Columns
        # -----------------------------------------

        numeric_columns = [

            "stock_quantity",

            "available_stock",

            "reserved_stock",

            "damaged_stock",

            "reorder_level",

            "inventory_value"

        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(

                df[column],

                errors="coerce"

            ).fillna(0)

        # -----------------------------------------
        # Clean String Columns
        # -----------------------------------------

        object_columns = df.select_dtypes(
            include="object"
        ).columns

        for column in object_columns:

            df[column] = (

                df[column]

                .fillna("")

                .astype(str)

                .str.strip()

            )

        # -----------------------------------------
        # Select Fact Columns
        # -----------------------------------------

        df = df[

            [

                "inventory_id",

                "product_key",

                "product_id",

                "warehouse",

                "stock_quantity",

                "available_stock",

                "reserved_stock",

                "damaged_stock",

                "reorder_level",

                "reorder_status",

                "last_restock_date",

                "inventory_value"

            ]

        ]

        logger.info(

            f"Fact Rows : {len(df):,}"

        )

        return df

    def load(
        self,
        df
    ):
        """
        Load Fact Inventory
        """

        logger.info(
            "Loading Fact Inventory..."
        )

        df.to_sql(

            self.target_table,

            con=engine,

            if_exists="replace",

            index=False,

            method="multi",

            chunksize=5000

        )

        logger.info(
            "Fact Inventory Loaded Successfully."
        )

    def validate(self):
        """
        Validate Fact Inventory
        """

        logger.info(
            "Validating Fact Inventory..."
        )

        # -----------------------------------------
        # Total Rows
        # -----------------------------------------

        row_count = pd.read_sql(

            f"""
            SELECT
                COUNT(*) AS total_rows
            FROM {self.target_table}
            """,

            engine

        )

        total_rows = int(
            row_count.iloc[0]["total_rows"]
        )

        logger.info(
            f"Rows Loaded : {total_rows:,}"
        )

        # -----------------------------------------
        # Duplicate Inventory IDs
        # -----------------------------------------

        duplicate_df = pd.read_sql(

            f"""
            SELECT

                COUNT(*) -
                COUNT(DISTINCT inventory_id)

                AS duplicates

            FROM {self.target_table}
            """,

            engine

        )

        duplicates = int(
            duplicate_df.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Inventory IDs : {duplicates}"
        )

        # -----------------------------------------
        # Inventory Summary
        # -----------------------------------------

        summary = pd.read_sql(

            f"""
            SELECT

                ROUND(
                    SUM(inventory_value),2
                ) AS total_inventory_value,

                ROUND(
                    AVG(inventory_value),2
                ) AS average_inventory_value

            FROM {self.target_table}
            """,

            engine

        )

        logger.info(

            f"Total Inventory Value : ₹ "

            f"{float(summary.iloc[0]['total_inventory_value']):,.2f}"

        )

        logger.info(

            f"Average Inventory Value : ₹ "

            f"{float(summary.iloc[0]['average_inventory_value']):,.2f}"

        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if duplicates == 0:

            logger.info(
                "Fact Inventory Validation Successful."
            )

        else:

            logger.warning(
                "Duplicate Inventory Records Found."
            )

    def run(self):
        """
        Execute Fact Inventory Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Fact Inventory Pipeline")
        logger.info("=" * 70)

        # Extract

        df = self.extract()

        # Transform

        df = self.transform(df)

        # Load

        self.load(df)

        # Validate

        self.validate()

        execution_time = round(

            time.time() - self.start_time,

            2

        )

        logger.info("=" * 70)

        logger.info(

            f"Fact Inventory Completed "

            f"in {execution_time} Seconds"

        )

        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    loader = FactInventoryLoader()

    loader.run()


if __name__ == "__main__":

    main()
