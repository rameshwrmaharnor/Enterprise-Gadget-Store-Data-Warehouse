"""
=========================================================
Enterprise Gadget Store Data Warehouse
Gold Layer - Customer Dimension

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import time

import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class CustomerDimension:

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "silver_customers"

        self.target_table = "dim_customer"

        logger.info("=" * 70)
        logger.info("Customer Dimension Started")
        logger.info("=" * 70)

    def extract(self):
        """
        Read Customer Dimension
        """

        logger.info(
            "Reading Silver Customers..."
        )

        query = f"""

        SELECT

            customer_id,

            first_name,

            last_name,

            gender,

            city,

            state,

            country,

            customer_segment,

            loyalty_points,

            account_status,

            created_date

        FROM {self.source_table}

        """

        df = pd.read_sql(

            query,

            engine

        )

        logger.info(

            f"Rows Read : {len(df):,}"

        )

        return df

    def transform(
        self,
        df
    ):
        """
        Transform Customer Dimension
        """

        logger.info(
            "Transforming Customer Dimension..."
        )

        # -----------------------------------------
        # Remove Duplicate Customers
        # -----------------------------------------

        df = df.drop_duplicates(
            subset=["customer_id"]
        )

        # -----------------------------------------
        # Create Surrogate Key
        # -----------------------------------------

        df.insert(

            0,

            "customer_key",

            range(
                1,
                len(df) + 1
            )

        )

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

        logger.info(
            f"Dimension Rows : {len(df):,}"
        )

        return df

    def load(
        self,
        df
    ):
        """
        Load Customer Dimension
        """

        logger.info(
            "Loading Customer Dimension..."
        )
        logger.info(df.head(10))

        logger.info(df.dtypes)

        logger.info(df["customer_key"].head(10).tolist())

        # Verify after loading
        check_df = pd.read_sql(
            f"""
            SELECT customer_key, customer_id
            FROM {self.target_table}
            LIMIT 10
            """,
            engine
        )

        logger.info("Data from MySQL after load:")
        logger.info("\n%s", check_df.to_string(index=False))

    def validate(self):
        """
        Validate Customer Dimension
        """

        logger.info(
            "Validating Customer Dimension..."
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
        # Duplicate Customer Keys
        # -----------------------------------------

        duplicate_keys = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT customer_key)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        duplicates = int(
            duplicate_keys.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Customer Keys : {duplicates}"
        )

        # -----------------------------------------
        # Duplicate Customer IDs
        # -----------------------------------------

        duplicate_ids = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT customer_id)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        duplicate_customer_ids = int(
            duplicate_ids.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Customer IDs : "
            f"{duplicate_customer_ids}"
        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if (
            duplicates == 0
            and
            duplicate_customer_ids == 0
        ):

            logger.info(
                "Customer Dimension Validation Successful."
            )

        else:

            logger.warning(
                "Customer Dimension Validation Failed."
            )

    def run(self):
        """
        Execute Customer Dimension Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Customer Dimension Pipeline")
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

            f"Customer Dimension Completed "

            f"in {execution_time} Seconds"

        )
        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    loader = CustomerDimension()

    loader.run()


if __name__ == "__main__":

    main()
