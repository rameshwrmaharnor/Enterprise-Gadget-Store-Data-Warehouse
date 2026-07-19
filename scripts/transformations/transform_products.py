"""
=========================================================
Enterprise Gadget Store Data Warehouse
Products Silver Transformation

Author : Rameshwar Maharnor
=========================================================
"""

import time
import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class ProductTransformer:
    """
    Transform Bronze Products to Silver Products
    """

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "bronze_products"

        self.target_table = "silver_products"

        logger.info("=" * 70)
        logger.info("Product Transformation Started")
        logger.info("=" * 70)
    def transform(self):
        """
        Clean Products Dataset
        """

        logger.info(
            "Reading Bronze Products..."
        )

        df = pd.read_sql(

            f"SELECT * FROM {self.source_table}",

            engine

        )

        logger.info(
            f"Rows Read : {len(df):,}"
        )

        # Remove duplicate products

        df = df.drop_duplicates()

        # Clean all string columns

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

        # Replace blank values

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
        Apply Enterprise Business Rules
        """

        logger.info(
            "Applying Business Rules..."
        )

        # -------------------------------------------------
        # Selling Price Validation
        # -------------------------------------------------

        if "selling_price" in df.columns:

            df["selling_price"] = (
                pd.to_numeric(
                    df["selling_price"],
                    errors="coerce"
                )
                .fillna(0)
            )

            df = df[
                df["selling_price"] > 0
            ]

        # -------------------------------------------------
        # Cost Price Validation
        # -------------------------------------------------

        if "cost_price" in df.columns:

            df["cost_price"] = (
                pd.to_numeric(
                    df["cost_price"],
                    errors="coerce"
                )
                .fillna(0)
            )

            df = df[
                df["cost_price"] > 0
            ]

        # -------------------------------------------------
        # MRP Validation
        # -------------------------------------------------

        if (
            "mrp" in df.columns and
            "selling_price" in df.columns
        ):

            df["mrp"] = pd.to_numeric(
                df["mrp"],
                errors="coerce"
            )

            df = df[
                df["mrp"] >= df["selling_price"]
            ]

        # -------------------------------------------------
        # Selling Price >= Cost Price
        # -------------------------------------------------

        if (
            "selling_price" in df.columns and
            "cost_price" in df.columns
        ):

            df = df[
                df["selling_price"] >=
                df["cost_price"]
            ]

        # -------------------------------------------------
        # Rating Validation
        # -------------------------------------------------

        if "rating" in df.columns:

            df["rating"] = (
                pd.to_numeric(
                    df["rating"],
                    errors="coerce"
                )
                .fillna(0)
            )

            df = df[
                df["rating"].between(
                    0,
                    5
                )
            ]

        # -------------------------------------------------
        # Stock Validation
        # -------------------------------------------------

        if "stock_quantity" in df.columns:

            df["stock_quantity"] = (
                pd.to_numeric(
                    df["stock_quantity"],
                    errors="coerce"
                )
                .fillna(0)
            )

            df = df[
                df["stock_quantity"] >= 0
            ]

        # -------------------------------------------------
        # Discount Validation
        # -------------------------------------------------

        if "discount_percentage" in df.columns:

            df["discount_percentage"] = (
                pd.to_numeric(
                    df["discount_percentage"],
                    errors="coerce"
                )
                .fillna(0)
            )

            df = df[
                df["discount_percentage"]
                .between(0, 90)
            ]

        logger.info(
            "Business Rules Applied."
        )

        logger.info(
            f"Remaining Rows : {len(df):,}"
        )

        return df
    def load(
        self,
        df
    ):
        """
        Load Cleaned Products into Silver Layer
        """

        logger.info(
            "Loading Silver Products..."
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
            "Silver Products Loaded Successfully."
        )


    def validate(self):
        """
        Validate Silver Products
        """

        logger.info(
            "Validating Silver Products..."
        )

        count_df = pd.read_sql(

            f"""
            SELECT COUNT(*) AS total_rows
            FROM {self.target_table}
            """,

            engine

        )

        total_rows = int(
            count_df.iloc[0]["total_rows"]
        )

        logger.info(
            f"Rows Loaded : {total_rows:,}"
        )

        duplicate_df = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT product_id)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        duplicates = int(
            duplicate_df.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Product IDs : {duplicates}"
        )

        if duplicates == 0:

            logger.info(
                "Validation Successful."
            )

        else:

            logger.warning(
                "Duplicate Product IDs Found."
            )
    def run(self):
        """
        Execute Product Transformation
        """

        logger.info("=" * 70)
        logger.info("Starting Product Transformation Pipeline")
        logger.info("=" * 70)

        df = self.transform()

        df = self.apply_business_rules(df)

        self.load(df)

        self.validate()

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        logger.info("=" * 70)
        logger.info(
            f"Product Transformation Completed "
            f"in {execution_time} Seconds"
        )
        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    transformer = ProductTransformer()

    transformer.run()


if __name__ == "__main__":

    main()