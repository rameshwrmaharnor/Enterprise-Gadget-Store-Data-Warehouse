"""
=========================================================
Enterprise Gadget Store Data Warehouse
Fact Shipments Loader

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import time

import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class FactShipmentsLoader:

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "silver_shipments"

        self.target_table = "fact_shipments"

        logger.info("=" * 70)
        logger.info("Fact Shipments Loader Started")
        logger.info("=" * 70)

    def extract(self):
        """
        Extract Shipments and Fact Orders
        """

        logger.info(
            "Reading Silver Shipments..."
        )

        shipments = pd.read_sql(
            """
            SELECT *
            FROM silver_shipments
            """,
            engine
        )

        logger.info(
            f"Shipments Read : {len(shipments):,}"
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

        shipments = shipments.merge(

            orders,

            how="left",

            on="order_id"

        )

        logger.info(
            "Order Mapping Completed."
        )

        return shipments

    def transform(
        self,
        df
    ):
        """
        Transform Shipment Fact
        """

        logger.info(
            "Transforming Fact Shipments..."
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
        # Shipping Cost
        # -----------------------------------------

        df["shipping_cost"] = pd.to_numeric(

            df["shipping_cost"],

            errors="coerce"

        ).fillna(0)

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
        # Select Fact Columns
        # -----------------------------------------

        df = df[

            [

                "shipment_id",

                "order_id",

                "date_key",

                "tracking_number",

                "courier_partner",

                "warehouse",

                "dispatch_date",

                "expected_delivery",

                "actual_delivery",

                "shipping_status",

                "shipping_cost"

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
        Load Fact Shipments
        """

        logger.info(
            "Loading Fact Shipments..."
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
            "Fact Shipments Loaded Successfully."
        )

    def validate(self):
        """
        Validate Fact Shipments
        """

        logger.info(
            "Validating Fact Shipments..."
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
        # Duplicate Shipment IDs
        # -----------------------------------------

        duplicate_df = pd.read_sql(

            f"""
            SELECT

                COUNT(*) -
                COUNT(DISTINCT shipment_id)

                AS duplicates

            FROM {self.target_table}
            """,

            engine

        )

        duplicates = int(
            duplicate_df.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Shipments : {duplicates}"
        )

        # -----------------------------------------
        # Shipping Summary
        # -----------------------------------------

        summary = pd.read_sql(

            f"""
            SELECT

                ROUND(
                    SUM(shipping_cost),2
                ) AS total_shipping_cost,

                ROUND(
                    AVG(shipping_cost),2
                ) AS average_shipping_cost

            FROM {self.target_table}
            """,

            engine

        )

        logger.info(

            f"Total Shipping Cost : ₹ "

            f"{float(summary.iloc[0]['total_shipping_cost']):,.2f}"

        )

        logger.info(

            f"Average Shipping Cost : ₹ "

            f"{float(summary.iloc[0]['average_shipping_cost']):,.2f}"

        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if duplicates == 0:

            logger.info(
                "Fact Shipments Validation Successful."
            )

        else:

            logger.warning(
                "Duplicate Shipments Found."
            )

    def run(self):
        """
        Execute Fact Shipments Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Fact Shipments Pipeline")
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

            f"Fact Shipments Completed "

            f"in {execution_time} Seconds"

        )

        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    loader = FactShipmentsLoader()

    loader.run()


if __name__ == "__main__":

    main()
