"""
=========================================================
Enterprise Gadget Store Data Warehouse
Suppliers Silver Transformation

Author : Rameshwar Maharnor
=========================================================
"""

import time

import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class SupplierTransformer:
    """
    Transform Bronze Suppliers to Silver
    """

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "bronze_suppliers"

        self.target_table = "silver_suppliers"

        logger.info("=" * 70)
        logger.info("Supplier Transformation Started")
        logger.info("=" * 70)

    def transform(self):
        """
        Clean Supplier Data
        """

        logger.info(
            "Reading Bronze Suppliers..."
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

        # Trim spaces

        object_columns = df.select_dtypes(
            include="object"
        ).columns

        for column in object_columns:

            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
            )

        # Lowercase email

        if "email" in df.columns:

            df["email"] = (
                df["email"]
                .fillna("")
                .astype(str)
                .str.lower()
            )

        # Remove spaces from phone

        if "phone" in df.columns:

            df["phone"] = (
                df["phone"]
                .fillna("")
                .astype(str)
                .str.replace(" ", "", regex=False)
            )

        # Uppercase GST Number

        if "gst_number" in df.columns:

            df["gst_number"] = (
                df["gst_number"]
                .fillna("")
                .astype(str)
                .str.upper()
            )

        # Replace blank values

        df.replace(
            "",
            pd.NA,
            inplace=True
        )

        logger.info(
            "Supplier Cleaning Completed."
        )

        return df

    def load(self, df):
        """
        Load Silver Suppliers
        """

        logger.info(
            "Loading Silver Suppliers..."
        )

        df.to_sql(

            self.target_table,

            engine,

            if_exists="replace",

            index=False,

            method="multi",

            chunksize=5000

        )

        logger.info(
            "Silver Suppliers Loaded Successfully."
        )

    def validate(self):
        """
        Validate Silver Table
        """

        logger.info(
            "Validating Silver Suppliers..."
        )

        count = pd.read_sql(

            f"""
            SELECT COUNT(*) AS total
            FROM {self.target_table}
            """,

            engine

        )

        logger.info(

            f"Rows Loaded : "

            f"{int(count.iloc[0]['total']):,}"

        )

    def run(self):
        """
        Execute Supplier Transformation
        """

        df = self.transform()

        self.load(df)

        self.validate()

        execution_time = round(

            time.time() - self.start_time,

            2

        )

        logger.info("=" * 70)
        logger.info(
            f"Supplier Transformation Completed "
            f"in {execution_time} Seconds"
        )
        logger.info("=" * 70)


def main():

    transformer = SupplierTransformer()

    transformer.run()


if __name__ == "__main__":

    main()
