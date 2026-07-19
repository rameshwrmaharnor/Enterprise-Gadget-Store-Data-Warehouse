"""
=========================================================
Enterprise Gadget Store Data Warehouse
Orders Silver Transformation

Author : Rameshwar Maharnor
=========================================================
"""

import time
import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class OrderTransformer:
    """
    Transform Bronze Orders to Silver Orders
    """

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "bronze_orders"

        self.target_table = "silver_orders"

        logger.info("=" * 70)
        logger.info("Order Transformation Started")
        logger.info("=" * 70)

    def transform(self):
        """
        Read and Clean Orders
        """

        logger.info(
            "Reading Bronze Orders..."
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

        # Replace blanks

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
        Apply Order Business Rules
        """

        logger.info(
            "Applying Order Business Rules..."
        )

        # Remove duplicate Order IDs

        if "order_id" in df.columns:

            df = df.drop_duplicates(
                subset=["order_id"]
            )

        # Subtotal Validation

        if "subtotal" in df.columns:

            df["subtotal"] = pd.to_numeric(

                df["subtotal"],

                errors="coerce"

            ).fillna(0)

            df = df[
                df["subtotal"] > 0
            ]

        # Discount Validation

        if "discount_amount" in df.columns:

            df["discount_amount"] = pd.to_numeric(

                df["discount_amount"],

                errors="coerce"

            ).fillna(0)

            df = df[
                df["discount_amount"] >= 0
            ]

        # Total Amount Validation

        if "total_amount" in df.columns:

            df["total_amount"] = pd.to_numeric(

                df["total_amount"],

                errors="coerce"

            ).fillna(0)

            df = df[
                df["total_amount"] > 0
            ]

        # Discount cannot exceed subtotal

        if (
            "subtotal" in df.columns and
            "discount_amount" in df.columns
        ):

            df = df[
                df["discount_amount"] <=
                df["subtotal"]
            ]

        # Order Status Validation

        if "order_status" in df.columns:

            valid_status = [

                "Processing",

                "Shipped",

                "Delivered",

                "Cancelled",

                "Returned"

            ]

            df = df[
                df["order_status"].isin(
                    valid_status
                )
            ]

        # Payment Status Validation

        if "payment_status" in df.columns:

            valid_payment = [

                "Paid",

                "Pending",

                "Failed",

                "Refunded"

            ]

            df = df[
                df["payment_status"].isin(
                    valid_payment
                )
            ]

        logger.info(
            "Business Rules Applied."
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
        Validate Customer and Coupon References
        """

        logger.info(
            "Validating Foreign Keys..."
        )

        # -----------------------------------------
        # Valid Customers
        # -----------------------------------------

        customers = pd.read_sql(

            """
            SELECT customer_id
            FROM silver_customers
            """,

            engine

        )

        valid_customers = set(
            customers["customer_id"]
        )

        before = len(df)

        df = df[
            df["customer_id"].isin(
                valid_customers
            )
        ]

        logger.info(

            f"Invalid Customers Removed : "

            f"{before - len(df):,}"

        )

        # -----------------------------------------
        # Valid Coupons
        # -----------------------------------------

        if "coupon_id" in df.columns:

            coupons = pd.read_sql(

                """
                SELECT coupon_id
                FROM silver_coupons
                """,

                engine

            )

            valid_coupons = set(

                coupons["coupon_id"]

            )

            before = len(df)

            df = df[

                df["coupon_id"].isna()

                |

                df["coupon_id"].isin(
                    valid_coupons
                )

            ]

            logger.info(

                f"Invalid Coupons Removed : "

                f"{before - len(df):,}"

            )

        logger.info(
            "Foreign Key Validation Completed."
        )

        logger.info(
            f"Remaining Orders : {len(df):,}"
        )

        return df

    def load(
        self,
        df
    ):
        """
        Load Silver Orders
        """

        logger.info(
            "Loading Silver Orders..."
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
            "Silver Orders Loaded Successfully."
        )

    def validate(self):
        """
        Validate Silver Orders
        """

        logger.info(
            "Validating Silver Orders..."
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
        # Duplicate Order IDs
        # -----------------------------------------

        duplicate_df = pd.read_sql(

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
            duplicate_df.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Order IDs : {duplicates}"
        )

        # -----------------------------------------
        # Total Sales Amount
        # -----------------------------------------

        sales_df = pd.read_sql(

            f"""
            SELECT
                ROUND(SUM(total_amount),2)
                AS total_sales
            FROM {self.target_table}
            """,

            engine

        )

        total_sales = float(
            sales_df.iloc[0]["total_sales"]
        )

        logger.info(
            f"Total Sales : ₹ {total_sales:,.2f}"
        )

        # -----------------------------------------
        # Average Order Value
        # -----------------------------------------

        avg_df = pd.read_sql(

            f"""
            SELECT
                ROUND(AVG(total_amount),2)
                AS average_order
            FROM {self.target_table}
            """,

            engine

        )

        average_order = float(
            avg_df.iloc[0]["average_order"]
        )

        logger.info(
            f"Average Order Value : ₹ {average_order:,.2f}"
        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if duplicates == 0:

            logger.info(
                "Order Validation Successful."
            )

        else:

            logger.warning(
                "Duplicate Orders Found."
            )

    def run(self):
        """
        Execute Order Transformation Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Order Transformation Pipeline")
        logger.info("=" * 70)

        # Read Bronze Orders
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
            f"Order Transformation Completed "
            f"in {execution_time} Seconds"
        )
        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    transformer = OrderTransformer()

    transformer.run()


if __name__ == "__main__":

    main()
