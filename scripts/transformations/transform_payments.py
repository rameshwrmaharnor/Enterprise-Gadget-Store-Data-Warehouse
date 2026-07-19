"""
=========================================================
Enterprise Gadget Store Data Warehouse
Payments Silver Transformation

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import time
import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class PaymentTransformer:
    """
    Transform Bronze Payments to Silver Payments
    """

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "bronze_payments"

        self.target_table = "silver_payments"

        logger.info("=" * 70)
        logger.info("Payment Transformation Started")
        logger.info("=" * 70)

    def transform(self):
        """
        Read and Clean Payments
        """

        logger.info(
            "Reading Bronze Payments..."
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
        Apply Payment Business Rules
        """

        logger.info(
            "Applying Payment Business Rules..."
        )

        # -----------------------------------------
        # Remove Duplicate Payment IDs
        # -----------------------------------------

        if "payment_id" in df.columns:

            df = df.drop_duplicates(
                subset=["payment_id"]
            )

        # -----------------------------------------
        # Remove Duplicate Transaction IDs
        # -----------------------------------------

        if "transaction_id" in df.columns:

            df = df.drop_duplicates(
                subset=["transaction_id"]
            )

        # -----------------------------------------
        # Payment Amount Validation
        # -----------------------------------------

        if "payment_amount" in df.columns:

            df["payment_amount"] = pd.to_numeric(

                df["payment_amount"],

                errors="coerce"

            ).fillna(0)

            df = df[
                df["payment_amount"] > 0
            ]

        # -----------------------------------------
        # Payment Status Validation
        # -----------------------------------------

        if "payment_status" in df.columns:

            valid_status = [

                "Paid",

                "Pending",

                "Failed",

                "Refunded"

            ]

            df = df[
                df["payment_status"].isin(
                    valid_status
                )
            ]

        # -----------------------------------------
        # Payment Method Validation
        # -----------------------------------------

        if "payment_method" in df.columns:

            valid_methods = [

                "UPI",

                "Credit Card",

                "Debit Card",

                "Net Banking",

                "Cash On Delivery"

            ]

            df = df[
                df["payment_method"].isin(
                    valid_methods
                )
            ]

        logger.info(
            "Payment Business Rules Applied."
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
        Validate Order Foreign Key
        """

        logger.info(
            "Validating Order References..."
        )

        # -----------------------------------------
        # Read Valid Orders
        # -----------------------------------------

        orders = pd.read_sql(

            """
            SELECT order_id
            FROM silver_orders
            """,

            engine

        )

        valid_orders = set(
            orders["order_id"]
        )

        before = len(df)

        df = df[
            df["order_id"].isin(
                valid_orders
            )
        ]

        removed = before - len(df)

        logger.info(
            f"Invalid Orders Removed : {removed:,}"
        )

        logger.info(
            f"Remaining Payments : {len(df):,}"
        )

        return df

    def load(
        self,
        df
    ):
        """
        Load Silver Payments
        """

        logger.info(
            "Loading Silver Payments..."
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
            "Silver Payments Loaded Successfully."
        )

    def validate(self):
        """
        Validate Silver Payments
        """

        logger.info(
            "Validating Silver Payments..."
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
        # Duplicate Payment IDs
        # -----------------------------------------

        duplicate_payment = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT payment_id)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        payment_duplicates = int(
            duplicate_payment.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Payment IDs : "
            f"{payment_duplicates}"
        )

        # -----------------------------------------
        # Duplicate Transaction IDs
        # -----------------------------------------

        duplicate_transaction = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT transaction_id)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        transaction_duplicates = int(
            duplicate_transaction.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Transaction IDs : "
            f"{transaction_duplicates}"
        )

        # -----------------------------------------
        # Total Payment Amount
        # -----------------------------------------

        payment_summary = pd.read_sql(

            f"""
            SELECT
                ROUND(SUM(payment_amount),2)
                AS total_payment,
                ROUND(AVG(payment_amount),2)
                AS average_payment
            FROM {self.target_table}
            """,

            engine

        )

        total_payment = float(
            payment_summary.iloc[0]["total_payment"]
        )

        average_payment = float(
            payment_summary.iloc[0]["average_payment"]
        )

        logger.info(
            f"Total Payment Amount : "
            f"₹ {total_payment:,.2f}"
        )

        logger.info(
            f"Average Payment Amount : "
            f"₹ {average_payment:,.2f}"
        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if (
            payment_duplicates == 0
            and
            transaction_duplicates == 0
        ):

            logger.info(
                "Payment Validation Successful."
            )

        else:

            logger.warning(
                "Duplicate Payments Found."
            )

    def run(self):
        """
        Execute Payment Transformation Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Payment Transformation Pipeline")
        logger.info("=" * 70)

        # Read Bronze Payments
        df = self.transform()

        # Apply Business Rules
        df = self.apply_business_rules(df)

        # Validate Foreign Keys
        df = self.validate_foreign_keys(df)

        # Load into Silver
        self.load(df)

        # Validate Silver Table
        self.validate()

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        logger.info("=" * 70)
        logger.info(
            f"Payment Transformation Completed "
            f"in {execution_time} Seconds"
        )
        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    transformer = PaymentTransformer()

    transformer.run()


if __name__ == "__main__":

    main()
