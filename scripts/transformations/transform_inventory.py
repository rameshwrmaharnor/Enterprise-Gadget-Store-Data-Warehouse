"""
=========================================================
Enterprise Gadget Store Data Warehouse
Inventory Silver Transformation

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import time
import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class InventoryTransformer:
    """
    Transform Bronze Inventory to Silver Inventory
    """

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "bronze_inventory"

        self.target_table = "silver_inventory"

        logger.info("=" * 70)
        logger.info("Inventory Transformation Started")
        logger.info("=" * 70)

    def transform(self):
        """
        Read and Clean Inventory
        """

        logger.info(
            "Reading Bronze Inventory..."
        )

        df = pd.read_sql(

            f"SELECT * FROM {self.source_table}",

            engine

        )

        logger.info(
            f"Rows Read : {len(df):,}"
        )

        # Remove duplicate rows

        df = df.drop_duplicates()

        # Clean string columns

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

        df.replace(
            "",
            pd.NA,
            inplace=True
        )

        logger.info(
            "Basic Cleaning Completed."
        )

        return df

    def apply_business_rules(
        self,
        df
    ):
        """
        Apply Inventory Business Rules
        """

        logger.info(
            "Applying Inventory Business Rules..."
        )

        # -----------------------------------------
        # Remove Duplicate Inventory IDs
        # -----------------------------------------

        if "inventory_id" in df.columns:

            df = df.drop_duplicates(
                subset=["inventory_id"]
            )

        # -----------------------------------------
        # Stock Quantity
        # -----------------------------------------

        if "stock_quantity" in df.columns:

            df["stock_quantity"] = pd.to_numeric(
                df["stock_quantity"],
                errors="coerce"
            ).fillna(0)

            df = df[
                df["stock_quantity"] >= 0
            ]

        # -----------------------------------------
        # Available Stock
        # -----------------------------------------

        if "available_stock" in df.columns:

            df["available_stock"] = pd.to_numeric(
                df["available_stock"],
                errors="coerce"
            ).fillna(0)

            df = df[
                df["available_stock"] >= 0
            ]

        if (
            "stock_quantity" in df.columns and
            "available_stock" in df.columns
        ):

            df = df[
                df["available_stock"] <=
                df["stock_quantity"]
            ]

        # -----------------------------------------
        # Reserved Stock
        # -----------------------------------------

        if "reserved_stock" in df.columns:

            df["reserved_stock"] = pd.to_numeric(
                df["reserved_stock"],
                errors="coerce"
            ).fillna(0)

            df = df[
                df["reserved_stock"] >= 0
            ]

        # -----------------------------------------
        # Reorder Level
        # -----------------------------------------

        if "reorder_level" in df.columns:

            df["reorder_level"] = pd.to_numeric(
                df["reorder_level"],
                errors="coerce"
            ).fillna(0)

            df = df[
                df["reorder_level"] >= 0
            ]

        # -----------------------------------------
        # Inventory Value
        # -----------------------------------------

        if "inventory_value" in df.columns:

            df["inventory_value"] = pd.to_numeric(
                df["inventory_value"],
                errors="coerce"
            ).fillna(0)

            df = df[
                df["inventory_value"] >= 0
            ]

        # -----------------------------------------
        # Warehouse Validation
        # -----------------------------------------

        if "warehouse" in df.columns:

            valid_warehouses = [

                "Mumbai WH",

                "Delhi WH",

                "Bengaluru WH",

                "Chennai WH",

                "Hyderabad WH",

                "Pune WH"

            ]

            df = df[
                df["warehouse"].isin(
                    valid_warehouses
                )
            ]

        logger.info(
            "Inventory Business Rules Applied."
        )

        logger.info(
            f"Remaining Rows : {len(df):,}"
        )

        return df

    def validate_foreign_keys(
        self,
        df
    ):
        """
        Validate Product Foreign Key
        """

        logger.info(
            "Validating Product References..."
        )

        products = pd.read_sql(

            """
            SELECT product_id
            FROM silver_products
            """,

            engine

        )

        valid_products = set(
            products["product_id"]
        )

        before = len(df)

        df = df[
            df["product_id"].isin(
                valid_products
            )
        ]

        removed = before - len(df)

        logger.info(
            f"Invalid Products Removed : {removed:,}"
        )

        logger.info(
            f"Remaining Inventory Rows : {len(df):,}"
        )

        return df

    def load(
        self,
        df
    ):
        """
        Load Silver Inventory
        """

        logger.info(
            "Loading Silver Inventory..."
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
            "Silver Inventory Loaded Successfully."
        )

    def validate(self):
        """
        Validate Silver Inventory
        """

        logger.info(
            "Validating Silver Inventory..."
        )

        # -----------------------------------------
        # Total Rows
        # -----------------------------------------

        row_count = pd.read_sql(

            f"""
            SELECT COUNT(*) AS total_rows
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

                ROUND(SUM(inventory_value),2)
                    AS total_inventory_value,

                ROUND(AVG(stock_quantity),2)
                    AS average_stock,

                MAX(stock_quantity)
                    AS max_stock,

                MIN(stock_quantity)
                    AS min_stock

            FROM {self.target_table}
            """,

            engine

        )

        logger.info(

            f"Total Inventory Value : ₹ "

            f"{float(summary.iloc[0]['total_inventory_value']):,.2f}"

        )

        logger.info(

            f"Average Stock : "

            f"{float(summary.iloc[0]['average_stock']):,.2f}"

        )

        logger.info(

            f"Maximum Stock : "

            f"{int(summary.iloc[0]['max_stock'])}"

        )

        logger.info(

            f"Minimum Stock : "

            f"{int(summary.iloc[0]['min_stock'])}"

        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if duplicates == 0:

            logger.info(
                "Inventory Validation Successful."
            )

        else:

            logger.warning(
                "Duplicate Inventory IDs Found."
            )

    def run(self):
        """
        Execute Inventory Transformation Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Inventory Transformation Pipeline")
        logger.info("=" * 70)

        # Read Bronze Inventory

        df = self.transform()

        # Apply Business Rules

        df = self.apply_business_rules(df)

        # Validate Product References

        df = self.validate_foreign_keys(df)

        # Load into Silver

        self.load(df)

        # Validate Loaded Data

        self.validate()

        execution_time = round(

            time.time() - self.start_time,

            2

        )

        logger.info("=" * 70)
        logger.info(

            f"Inventory Transformation Completed "

            f"in {execution_time} Seconds"

        )
        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    transformer = InventoryTransformer()

    transformer.run()


if __name__ == "__main__":

    main()
