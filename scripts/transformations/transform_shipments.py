"""
=========================================================
Enterprise Gadget Store Data Warehouse
Shipments Silver Transformation

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import time
import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class ShipmentTransformer:
    """
    Transform Bronze Shipments to Silver Shipments
    """

    def __init__(self):

        self.start_time = time.time()

        self.source_table = "bronze_shipments"

        self.target_table = "silver_shipments"

        logger.info("=" * 70)
        logger.info("Shipment Transformation Started")
        logger.info("=" * 70)

    def transform(self):
        """
        Read and Clean Shipments
        """

        logger.info(
            "Reading Bronze Shipments..."
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
        Apply Shipment Business Rules
        """

        logger.info(
            "Applying Shipment Business Rules..."
        )

        # -----------------------------------------
        # Remove Duplicate Shipment IDs
        # -----------------------------------------

        if "shipment_id" in df.columns:

            df = df.drop_duplicates(
                subset=["shipment_id"]
            )

        # -----------------------------------------
        # Remove Duplicate Tracking Numbers
        # -----------------------------------------

        if "tracking_number" in df.columns:

            df = df.drop_duplicates(
                subset=["tracking_number"]
            )

        # -----------------------------------------
        # Shipping Cost Validation
        # -----------------------------------------

        if "shipping_cost" in df.columns:

            df["shipping_cost"] = pd.to_numeric(

                df["shipping_cost"],

                errors="coerce"

            ).fillna(0)

            df = df[
                df["shipping_cost"] >= 0
            ]

        # -----------------------------------------
        # Courier Partner Validation
        # -----------------------------------------

        if "courier_partner" in df.columns:

            valid_couriers = [

                "Blue Dart",

                "Delhivery",

                "DTDC",

                "Ekart",

                "FedEx",

                "India Post",

                "Shadowfax",

                "XpressBees"

            ]

            df = df[
                df["courier_partner"].isin(
                    valid_couriers
                )
            ]

        # -----------------------------------------
        # Shipping Status Validation
        # -----------------------------------------

        if "shipping_status" in df.columns:

            valid_status = [

                "Processing",

                "In Transit",

                "Out For Delivery",

                "Delivered",

                "Returned",

                "Cancelled"

            ]

            df = df[
                df["shipping_status"].isin(
                    valid_status
                )
            ]

        # -----------------------------------------
        # Delivery Date Validation
        # -----------------------------------------

        if (
            "shipment_date" in df.columns and
            "actual_delivery" in df.columns
        ):

            df["shipment_date"] = pd.to_datetime(

                df["shipment_date"],

                errors="coerce"

            )

            df["actual_delivery"] = pd.to_datetime(

                df["actual_delivery"],

                errors="coerce"

            )

            df = df[
                (
                    df["actual_delivery"].isna()
                )
                |
                (
                    df["actual_delivery"] >=
                    df["shipment_date"]
                )
            ]

        logger.info(
            "Shipment Business Rules Applied."
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
            f"Remaining Shipments : {len(df):,}"
        )

        return df

    def load(
        self,
        df
    ):
        """
        Load Silver Shipments
        """

        logger.info(
            "Loading Silver Shipments..."
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
            "Silver Shipments Loaded Successfully."
        )

    def validate(self):
        """
        Validate Silver Shipments
        """

        logger.info(
            "Validating Silver Shipments..."
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
        # Duplicate Shipment IDs
        # -----------------------------------------

        duplicate_shipment = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT shipment_id)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        shipment_duplicates = int(
            duplicate_shipment.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Shipment IDs : "
            f"{shipment_duplicates}"
        )

        # -----------------------------------------
        # Duplicate Tracking Numbers
        # -----------------------------------------

        duplicate_tracking = pd.read_sql(

            f"""
            SELECT
                COUNT(*) -
                COUNT(DISTINCT tracking_number)
                AS duplicates
            FROM {self.target_table}
            """,

            engine

        )

        tracking_duplicates = int(
            duplicate_tracking.iloc[0]["duplicates"]
        )

        logger.info(
            f"Duplicate Tracking Numbers : "
            f"{tracking_duplicates}"
        )

        # -----------------------------------------
        # Shipping Summary
        # -----------------------------------------

        summary = pd.read_sql(

            f"""
            SELECT
                ROUND(SUM(shipping_cost),2)
                    AS total_shipping_cost,

                ROUND(AVG(shipping_cost),2)
                    AS average_shipping_cost

            FROM {self.target_table}
            """,

            engine

        )

        total_shipping = float(
            summary.iloc[0]["total_shipping_cost"]
        )

        average_shipping = float(
            summary.iloc[0]["average_shipping_cost"]
        )

        logger.info(
            f"Total Shipping Cost : "
            f"₹ {total_shipping:,.2f}"
        )

        logger.info(
            f"Average Shipping Cost : "
            f"₹ {average_shipping:,.2f}"
        )

        # -----------------------------------------
        # Validation Result
        # -----------------------------------------

        if (
            shipment_duplicates == 0
            and
            tracking_duplicates == 0
        ):

            logger.info(
                "Shipment Validation Successful."
            )

        else:

            logger.warning(
                "Shipment Validation Completed with Warnings."
            )

    def run(self):
        """
        Execute Shipment Transformation Pipeline
        """

        logger.info("=" * 70)
        logger.info("Starting Shipment Transformation Pipeline")
        logger.info("=" * 70)

        # Read Bronze Shipments
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
            f"Shipment Transformation Completed "
            f"in {execution_time} Seconds"
        )
        logger.info("=" * 70)


def main():
    """
    Main Entry Point
    """

    transformer = ShipmentTransformer()

    transformer.run()


if __name__ == "__main__":

    main()
