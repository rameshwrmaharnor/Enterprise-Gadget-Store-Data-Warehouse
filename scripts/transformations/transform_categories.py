"""
=========================================================
Enterprise Gadget Store Data Warehouse
Categories Silver Transformation

Author : Rameshwar Maharnor
=========================================================
"""

import time

import pandas as pd

from utils.config import config
from utils.db_connection import engine
from utils.logger import logger


class CategoryTransformer:

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "bronze_categories"

        self.target_table = "silver_categories"

        logger.info("=" * 70)
        logger.info("Category Transformation Started")
        logger.info("=" * 70)

    def transform(self):
        """
        Transform Bronze Categories to Silver
        """

        logger.info(
            "Reading Bronze Categories..."
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

        # Remove leading/trailing spaces

        object_columns = df.select_dtypes(
            include="object"
        ).columns

        for column in object_columns:

            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
            )

        # Replace blank strings with NULL

        df.replace(

            "",

            pd.NA,

            inplace=True

        )

        logger.info(
            "Basic Cleaning Completed."
        )

        return df

    def load(self, df):
        """
        Load Silver Categories
        """

        logger.info(
            "Loading Silver Categories..."
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
            "Silver Categories Loaded."
        )

    def run(self):

        df = self.transform()

        self.load(df)

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        logger.info("=" * 70)
        logger.info(
            f"Completed in {execution_time} Seconds"
        )
        logger.info("=" * 70)


def main():

    transformer = CategoryTransformer()

    transformer.run()


if __name__ == "__main__":

    main()
