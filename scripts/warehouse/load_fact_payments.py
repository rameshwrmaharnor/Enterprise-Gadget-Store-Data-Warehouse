"""
=========================================================
Enterprise Gadget Store Data Warehouse
Fact Payments Loader

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import time

import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class FactPaymentsLoader:

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "silver_payments"

        self.target_table = "fact_payments"

        logger.info("=" * 70)
        logger.info("Fact Payments Loader Started")
        logger.info("=" * 70)
    def extract(self):
        """
        Extract Payments and Dimension Keys
        """

        logger.info(
            "Reading Silver Payments..."
        )

        payments = pd.read_sql(
            """
            SELECT *
            FROM silver_payments
            """,
            engine
        )

        logger.info(
            f"Payments Read : {len(payments):,}"
        )

        # -----------------------------------------
        # Read Fact Orders
        # -----------------------------------------

        orders = pd.read_sql(
            """
            SELECT
                order_id,
                date_key
            FROM fact_orders
            """,
            engine
        )

        # -----------------------------------------
        # Merge Orders
        # -----------------------------------------

        payments = payments.merge(

            orders,

            how="left",

            on="order_id"

        )

        logger.info(
            "Fact Order Mapping Completed."
        )

        return payments
    def transform(
        self,
        df
    ):
        """
        Transform Payment Fact
        """

        logger.info(
            "Transforming Fact Payments..."
        )

        # -----------------------------------------
        # Missing Date Keys
        # -----------------------------------------

        df["date_key"] = (

            df["date_key"]

            .fillna(19000101)

            .astype(int)

        )

        # -----------------------------------------
        # Numeric Columns
        # -----------------------------------------

        numeric_columns = [

            "payment_amount"

        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(

                df[column],

                errors="coerce"

            ).fillna(0)

        # -----------------------------------------
        # Clean Text Columns
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

                "payment_id",

                "order_id",

                "date_key",

                "transaction_id",

                "payment_gateway",

                "payment_method",

                "payment_amount",

                "payment_status",

                "payment_date",

                "bank_name",

                "card_type",

                "currency"

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
        Load Fact Payments
        """

        logger.info(
            "Loading Fact Payments..."
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
            "Fact Payments Loaded Successfully."
        )


    def validate(self):
        """
        Validate Fact Payments
        """

        logger.info(
            "Validating Fact Payments..."
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
        # Duplicate Payment IDs
        # -----------------------------------------

        duplicate_df = pd.read_sql(

            f"""
            SELECT

                COUNT(*) -
                COUNT(DISTINCT payment_id)

                AS duplicates

            FROM {self.target_table}
            """,

            engine

        )

        duplicates = int(
            duplicate_df.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Payments : {duplicates}"
        )

        # -----------------------------------------
        # Payment Summary
        # -----------------------------------------

        summary = pd.read_sql(

            f"""
            SELECT

                ROUND(
                    SUM(payment_amount),2
                ) AS total_payment,

                ROUND(
                    AVG(payment_amount),2
                ) AS average_payment

            FROM {self.target_table}
            """,

            engine

        )

        logger.info(

            f"Total Payment Amount : ₹ "

            f"{float(summary.iloc[0]['total_payment']):,.2f}"

        )

        logger.info(

            f"Average Payment Amount : ₹ "

            f"{float(summary.iloc[0]['average_payment']):,.2f}"

        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if duplicates == 0:

            logger.info(
                "Fact Payments Validation Successful."
            )

        else:

            logger.warning(
                "Duplicate Payments Found."
            )
    def run(self):
        """
        Execute Fact Payments Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Fact Payments Pipeline")
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

            f"Fact Payments Completed "

            f"in {execution_time} Seconds"

        )

        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    loader = FactPaymentsLoader()

    loader.run()


if __name__ == "__main__":

    main()