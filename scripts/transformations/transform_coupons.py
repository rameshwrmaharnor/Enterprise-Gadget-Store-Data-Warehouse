"""
=========================================================
Enterprise Gadget Store Data Warehouse
Coupons Silver Transformation

Author : Rameshwar Maharnor
=========================================================
"""

import time

import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class CouponTransformer:
    """
    Transform Bronze Coupons to Silver Coupons
    """

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "bronze_coupons"

        self.target_table = "silver_coupons"

        logger.info("=" * 70)
        logger.info("Coupon Transformation Started")
        logger.info("=" * 70)

    def transform(self):
        """
        Read and Clean Coupon Data
        """

        logger.info(
            "Reading Bronze Coupons..."
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

        # Clean text columns

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

        # Replace blanks with NULL

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
        Apply Coupon Business Rules
        """

        logger.info(
            "Applying Coupon Business Rules..."
        )

        # -----------------------------------------
        # Remove Duplicate Coupon IDs
        # -----------------------------------------

        if "coupon_id" in df.columns:

            df = df.drop_duplicates(
                subset=["coupon_id"]
            )

        # -----------------------------------------
        # Remove Duplicate Coupon Codes
        # -----------------------------------------

        if "coupon_code" in df.columns:

            df = df.drop_duplicates(
                subset=["coupon_code"]
            )

        # -----------------------------------------
        # Discount Type Validation
        # -----------------------------------------

        if "discount_type" in df.columns:

            valid_types = [

                "Flat",

                "Percentage"

            ]

            df = df[
                df["discount_type"].isin(
                    valid_types
                )
            ]

        # -----------------------------------------
        # Discount Value Validation
        # -----------------------------------------

        if (
            "discount_type" in df.columns and
            "discount_value" in df.columns
        ):

            df["discount_value"] = pd.to_numeric(

                df["discount_value"],

                errors="coerce"

            ).fillna(0)

            # Flat Discount

            flat_mask = (
                df["discount_type"] == "Flat"
            )

            df = df[
                (~flat_mask) |
                (df["discount_value"] > 0)
            ]

            # Percentage Discount

            percentage_mask = (
                df["discount_type"] == "Percentage"
            )

            df = df[
                (~percentage_mask) |
                (
                    df["discount_value"]
                    .between(1, 100)
                )
            ]

        # -----------------------------------------
        # Usage Validation
        # -----------------------------------------

        if (
            "usage_limit" in df.columns and
            "used_count" in df.columns
        ):

            df["usage_limit"] = pd.to_numeric(

                df["usage_limit"],

                errors="coerce"

            ).fillna(0)

            df["used_count"] = pd.to_numeric(

                df["used_count"],

                errors="coerce"

            ).fillna(0)

            df = df[
                df["used_count"] <=
                df["usage_limit"]
            ]

        # -----------------------------------------
        # Coupon Status Validation
        # -----------------------------------------

        if "coupon_status" in df.columns:

            valid_status = [

                "Active",

                "Expired",

                "Scheduled"

            ]

            df = df[
                df["coupon_status"].isin(
                    valid_status
                )
            ]

        logger.info(
            "Coupon Business Rules Applied."
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
        Load Silver Coupons
        """

        logger.info(
            "Loading Silver Coupons..."
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
            "Silver Coupons Loaded Successfully."
        )

    def validate(self):
        """
        Validate Silver Coupons
        """

        logger.info(
            "Validating Silver Coupons..."
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
        # Duplicate Coupon IDs
        # -----------------------------------------

        duplicate_id = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT coupon_id)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        duplicate_ids = int(
            duplicate_id.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Coupon IDs : {duplicate_ids}"
        )

        # -----------------------------------------
        # Duplicate Coupon Codes
        # -----------------------------------------

        duplicate_code = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT coupon_code)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        duplicate_codes = int(
            duplicate_code.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Coupon Codes : {duplicate_codes}"
        )

        # -----------------------------------------
        # Invalid Discount Values
        # -----------------------------------------

        invalid_discount = pd.read_sql(

            f"""
            SELECT COUNT(*) AS total
            FROM {self.target_table}
            WHERE discount_value <= 0
            """,

            engine

        )

        logger.info(
            f"Invalid Discounts : "
            f"{int(invalid_discount.iloc[0]['total'])}"
        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if duplicate_ids == 0 and duplicate_codes == 0:

            logger.info(
                "Coupon Validation Successful."
            )

        else:

            logger.warning(
                "Coupon Validation Completed with Warnings."
            )

    def run(self):
        """
        Execute Coupon Transformation Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Coupon Transformation Pipeline")
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
            f"Coupon Transformation Completed "
            f"in {execution_time} Seconds"
        )
        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    transformer = CouponTransformer()

    transformer.run()


if __name__ == "__main__":

    main()
