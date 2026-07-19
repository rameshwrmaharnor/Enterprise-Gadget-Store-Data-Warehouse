"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generic Dimension Loader

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import time

import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class DimensionLoader:

    def __init__(
        self,
        source_table,
        target_table,
        key_column,
        columns
    ):

        self.start_time = time.time()

        self.source_table = source_table

        self.target_table = target_table

        self.key_column = key_column

        self.columns = columns

        logger.info("=" * 70)
        logger.info(
            f"Loading {target_table}"
        )
        logger.info("=" * 70)

    def extract(self):
        """
        Extract Dimension Data
        """

        logger.info(
            f"Reading {self.source_table}..."
        )

        query = f"""

        SELECT

        {",".join(self.columns)}

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
        Generic Dimension Transformation
        """

        logger.info(
            "Transforming Dimension..."
        )

        # -----------------------------------------
        # Remove Duplicate Business Keys
        # -----------------------------------------

        df = df.drop_duplicates(
            subset=[self.key_column]
        )

        # -----------------------------------------
        # Create Surrogate Key
        # -----------------------------------------

        surrogate_key = (
            self.target_table
            .replace("dim_", "")
            + "_key"
        )

        df.insert(

            0,

            surrogate_key,

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

        # -----------------------------------------
        # Replace Blank Values
        # -----------------------------------------

        df.replace(

            "",

            pd.NA,

            inplace=True

        )

        logger.info(
            f"Dimension Rows : {len(df):,}"
        )

        return df

    def load(self, df):

        logger.info(df.columns.tolist())
        logger.info(df.head())

        df.to_sql(
            self.target_table,
            con=engine,
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=5000
        )

    def validate(self):
        """
        Validate Dimension Table
        """

        logger.info(
            f"Validating {self.target_table}..."
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
        # Duplicate Business Keys
        # -----------------------------------------

        duplicate_df = pd.read_sql(

            f"""
            SELECT

                COUNT(*) -
                COUNT(DISTINCT {self.key_column})

                AS duplicates

            FROM {self.target_table}
            """,

            engine

        )

        duplicates = int(
            duplicate_df.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate {self.key_column} : {duplicates}"
        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if duplicates == 0:

            logger.info(
                f"{self.target_table} Validation Successful."
            )

        else:

            logger.warning(
                f"{self.target_table} Validation Failed."
            )

    def run(self):
        """
        Execute Complete Dimension ETL
        """

        logger.info("=" * 70)
        logger.info(
            f"Starting {self.target_table} Pipeline"
        )
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

            f"{self.target_table} Completed "

            f"in {execution_time} Seconds"

        )

        logger.info("=" * 70)
