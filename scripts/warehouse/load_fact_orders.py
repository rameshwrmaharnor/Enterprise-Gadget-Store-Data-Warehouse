"""
=========================================================
Enterprise Gadget Store Data Warehouse
Fact Orders Loader

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import time
import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class FactOrdersLoader:

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "silver_orders"

        self.target_table = "fact_orders"

        logger.info("=" * 70)
        logger.info("Fact Orders Loader Started")
        logger.info("=" * 70)
    def extract(self):
        """
        Extract Orders and Dimension Keys
        """

        logger.info(
            "Reading Silver Orders..."
        )

        orders = pd.read_sql(
            """
            SELECT *
            FROM silver_orders
            """,
            engine
        )

        logger.info(
            f"Orders Read : {len(orders):,}"
        )

        # -----------------------------------------
        # Customer Dimension
        # -----------------------------------------

        customers = pd.read_sql(
            """
            SELECT
                customer_key,
                customer_id
            FROM dim_customer
            """,
            engine
        )

        # -----------------------------------------
        # Coupon Dimension
        # -----------------------------------------

        coupons = pd.read_sql(
            """
            SELECT
                coupon_key,
                coupon_id
            FROM dim_coupon
            """,
            engine
        )

        # -----------------------------------------
        # Join Customer
        # -----------------------------------------

        orders = orders.merge(

            customers,

            how="left",

            on="customer_id"

        )

        # -----------------------------------------
        # Join Coupon
        # -----------------------------------------

        orders = orders.merge(

            coupons,

            how="left",

            on="coupon_id"

        )

        # -----------------------------------------
        # Generate Date Key
        # -----------------------------------------

        orders["order_date"] = pd.to_datetime(

            orders["order_date"],

            errors="coerce"

        )

        orders["date_key"] = (

            orders["order_date"]

            .dt.strftime("%Y%m%d")

            .fillna("19000101")

            .astype(int)

        )

        logger.info(
            "Dimension Mapping Completed."
        )

        return orders
    def transform(
        self,
        df
    ):
        """
        Transform Orders Fact
        """

        logger.info(
            "Transforming Fact Orders..."
        )

        # -----------------------------------------
        # Replace Missing Dimension Keys
        # -----------------------------------------

        df["customer_key"] = (

            df["customer_key"]

            .fillna(0)

            .astype(int)

        )

        df["coupon_key"] = (

            df["coupon_key"]

            .fillna(0)

            .astype(int)

        )

        # -----------------------------------------
        # Numeric Columns
        # -----------------------------------------

        numeric_columns = [

            "subtotal",

            "discount_amount",

            "tax_amount",

            "shipping_charge",

            "total_amount"

        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(

                df[column],

                errors="coerce"

            ).fillna(0)

        # -----------------------------------------
        # Select Fact Columns
        # -----------------------------------------

        df = df[

            [

                "order_id",

                "customer_key",

                "coupon_key",

                "date_key",

                "subtotal",

                "discount_amount",

                "tax_amount",

                "shipping_charge",

                "total_amount",

                "payment_method",

                "payment_status",

                "order_status",

                "delivery_type"

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
        Load Fact Orders
        """

        logger.info(
            "Loading Fact Orders..."
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
            "Fact Orders Loaded Successfully."
        )


    def validate(self):
        """
        Validate Fact Orders
        """

        logger.info(
            "Validating Fact Orders..."
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
        # Duplicate Orders
        # -----------------------------------------

        duplicate_orders = pd.read_sql(

            f"""
            SELECT

                COUNT(*) -
                COUNT(DISTINCT order_id)
                AS duplicates

            FROM {self.target_table}
            """,

            engine

        )

        duplicates = int(
            duplicate_orders.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Orders : {duplicates}"
        )

        # -----------------------------------------
        # Sales Summary
        # -----------------------------------------

        summary = pd.read_sql(

            f"""
            SELECT

                ROUND(SUM(total_amount),2)
                    AS total_sales,

                ROUND(AVG(total_amount),2)
                    AS average_order_value

            FROM {self.target_table}
            """,

            engine

        )

        logger.info(

            f"Total Sales : ₹ "

            f"{float(summary.iloc[0]['total_sales']):,.2f}"

        )

        logger.info(

            f"Average Order Value : ₹ "

            f"{float(summary.iloc[0]['average_order_value']):,.2f}"

        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if duplicates == 0:

            logger.info(
                "Fact Orders Validation Successful."
            )

        else:

            logger.warning(
                "Duplicate Orders Found."
            )
    def run(self):
        """
        Execute Fact Orders Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Fact Orders Pipeline")
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

            f"Fact Orders Completed "

            f"in {execution_time} Seconds"

        )

        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    loader = FactOrdersLoader()

    loader.run()


if __name__ == "__main__":

    main()