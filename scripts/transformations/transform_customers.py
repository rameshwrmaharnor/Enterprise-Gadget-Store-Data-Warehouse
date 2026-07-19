"""
=========================================================
Enterprise Gadget Store Data Warehouse
Customers Silver Transformation

Author : Rameshwar Maharnor
=========================================================
"""

import time
import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class CustomerTransformer:
    """
    Transform Bronze Customers to Silver Customers
    """

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "bronze_customers"

        self.target_table = "silver_customers"

        logger.info("=" * 70)
        logger.info("Customer Transformation Started")
        logger.info("=" * 70)

    def transform(self):
        """
        Read and Clean Customer Data
        """

        logger.info(
            "Reading Bronze Customers..."
        )

        df = pd.read_sql(

            f"SELECT * FROM {self.source_table}",

            engine

        )

        logger.info(
            f"Rows Read : {len(df):,}"
        )

        # Remove duplicates

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

        # Replace blank strings

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
        Apply Customer Business Rules
        """

        logger.info(
            "Applying Customer Business Rules..."
        )

        # -----------------------------------------
        # Email Validation
        # -----------------------------------------

        if "email" in df.columns:

            df["email"] = (
                df["email"]
                .fillna("")
                .astype(str)
                .str.lower()
            )

            df = df[
                df["email"].str.contains(
                    "@",
                    na=False
                )
            ]

        # -----------------------------------------
        # Phone Validation
        # -----------------------------------------

        if "phone" in df.columns:

            df["phone"] = (
                df["phone"]
                .fillna("")
                .astype(str)
                .str.replace(
                    " ",
                    "",
                    regex=False
                )
            )

            df = df[
                df["phone"].str.len() >= 10
            ]

        # -----------------------------------------
        # Age Validation
        # -----------------------------------------

        if "age" in df.columns:

            df["age"] = pd.to_numeric(
                df["age"],
                errors="coerce"
            )

            df = df[
                df["age"].between(
                    18,
                    100
                )
            ]

        # -----------------------------------------
        # Annual Income
        # -----------------------------------------

        if "annual_income" in df.columns:

            df["annual_income"] = pd.to_numeric(
                df["annual_income"],
                errors="coerce"
            ).fillna(0)

            df = df[
                df["annual_income"] >= 0
            ]

        # -----------------------------------------
        # Loyalty Points
        # -----------------------------------------

        if "loyalty_points" in df.columns:

            df["loyalty_points"] = pd.to_numeric(
                df["loyalty_points"],
                errors="coerce"
            ).fillna(0)

            df = df[
                df["loyalty_points"] >= 0
            ]

        # -----------------------------------------
        # Customer Segment
        # -----------------------------------------

        if "customer_segment" in df.columns:

            valid_segments = [

                "Regular",

                "Silver",

                "Gold",

                "Platinum"

            ]

            df = df[
                df["customer_segment"].isin(
                    valid_segments
                )
            ]

        # -----------------------------------------
        # Account Status
        # -----------------------------------------

        if "account_status" in df.columns:

            valid_status = [

                "Active",

                "Inactive",

                "Blocked"

            ]

            df = df[
                df["account_status"].isin(
                    valid_status
                )
            ]

        # -----------------------------------------
        # Remove Duplicate Customer IDs
        # -----------------------------------------

        if "customer_id" in df.columns:

            df = df.drop_duplicates(
                subset=["customer_id"]
            )

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
        Load Silver Customers
        """

        logger.info(
            "Loading Silver Customers..."
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
            "Silver Customers Loaded Successfully."
        )

    def validate(self):
        """
        Validate Silver Customers
        """

        logger.info(
            "Validating Silver Customers..."
        )

        # -----------------------------------------
        # Row Count
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
        # Duplicate Customer IDs
        # -----------------------------------------

        duplicate_df = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT customer_id)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        duplicates = int(
            duplicate_df.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Customer IDs : {duplicates}"
        )

        # -----------------------------------------
        # Missing Email
        # -----------------------------------------

        missing_email = pd.read_sql(

            f"""
            SELECT COUNT(*) AS total
            FROM {self.target_table}
            WHERE email IS NULL
            """,

            engine

        )

        logger.info(
            f"Missing Emails : "
            f"{int(missing_email.iloc[0]['total'])}"
        )

        # -----------------------------------------
        # Missing Phone
        # -----------------------------------------

        missing_phone = pd.read_sql(

            f"""
            SELECT COUNT(*) AS total
            FROM {self.target_table}
            WHERE phone IS NULL
            """,

            engine

        )

        logger.info(
            f"Missing Phones : "
            f"{int(missing_phone.iloc[0]['total'])}"
        )

        if duplicates == 0:

            logger.info(
                "Customer Validation Successful."
            )

        else:

            logger.warning(
                "Duplicate Customer IDs Found."
            )

    def run(self):
        """
        Execute Customer Transformation Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Customer Transformation Pipeline")
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
            f"Customer Transformation Completed "
            f"in {execution_time} Seconds"
        )
        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    transformer = CustomerTransformer()

    transformer.run()


if __name__ == "__main__":

    main()
