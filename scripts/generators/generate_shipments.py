"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generate Shipments Dataset

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import json
import math
import random
import string
import time
from datetime import datetime

from pathlib import Path

import pandas as pd

from utils.config import config
from utils.logger import logger


class ShipmentGenerator:
    """
    Enterprise Shipment Dataset Generator
    """

    def __init__(self):

        random.seed(config["random_seed"])

        self.start_time = time.time()

        self.output_folder = Path(config["paths"]["raw"])
        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.log_folder = Path(config["paths"]["logs"])
        self.log_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.total_rows = config["dataset"]["shipments"]

        self.batch_size = 100000

        logger.info(
            "Loading Orders Dataset..."
        )

        self.orders = pd.read_csv(

            self.output_folder / "orders.csv",

            usecols=[
                "order_id",
                "order_date",
                "order_status"
            ]

        )

        self.couriers = [

            "Blue Dart",
            "Delhivery",
            "DTDC",
            "XpressBees",
            "Ekart",
            "India Post",
            "Shadowfax",
            "FedEx"

        ]

        self.warehouses = [

            "Mumbai WH",
            "Pune WH",
            "Delhi WH",
            "Bengaluru WH",
            "Hyderabad WH",
            "Chennai WH"

        ]

        self.shipping_status = [

            "Delivered",
            "In Transit",
            "Out For Delivery",
            "Returned",
            "Cancelled"

        ]

    def generate_tracking_number(self):
        """
        Generate Unique Tracking Number
        """

        return "TRK" + "".join(

            random.choices(

                string.ascii_uppercase +
                string.digits,

                k=14

            )

        )

    def generate_batch(
        self,
        batch_number,
        batch_size
    ):
        """
        Generate One Batch of Shipments
        """

        start = batch_number * self.batch_size

        end = min(

            start + batch_size,

            len(self.orders)

        )

        batch_orders = self.orders.iloc[start:end]

        shipments = []

        shipment_no = start + 1

        for row in batch_orders.to_dict("records"):

            order_date = pd.Timestamp(
                row["order_date"]
            )

            dispatch_date = order_date + pd.Timedelta(

                hours=random.randint(6, 48)

            )

            expected_delivery = dispatch_date + pd.Timedelta(

                days=random.randint(2, 7)

            )

            status = random.choices(

                [

                    "Delivered",
                    "In Transit",
                    "Out For Delivery",
                    "Returned",
                    "Cancelled"

                ],

                weights=[70, 15, 8, 5, 2],

                k=1

            )[0]

            if status == "Delivered":

                actual_delivery = expected_delivery + pd.Timedelta(

                    days=random.randint(-1, 2)

                )

            elif status == "Returned":

                actual_delivery = expected_delivery + pd.Timedelta(

                    days=random.randint(3, 7)

                )

            else:

                actual_delivery = pd.NaT

            shipments.append({

                "shipment_id": f"SHP{shipment_no:08}",

                "order_id": row["order_id"],

                "tracking_number": self.generate_tracking_number(),

                "courier_partner": random.choice(
                    self.couriers
                ),

                "warehouse": random.choice(
                    self.warehouses
                ),

                "dispatch_date": dispatch_date,

                "expected_delivery": expected_delivery,

                "actual_delivery": actual_delivery,

                "shipping_status": status,

                "shipping_cost": round(

                    random.uniform(40, 350),

                    2

                ),

                "created_date": datetime.now().date()

            })

            shipment_no += 1

        return pd.DataFrame(shipments)

    def generate_shipments(self):
        """
        Generate Shipments Dataset in Batches
        """

        logger.info("=" * 70)
        logger.info("Generating Shipments in Batches...")
        logger.info("=" * 70)

        output_file = self.output_folder / "shipments.csv"

        # Delete old file
        if output_file.exists():
            output_file.unlink()

        total_batches = math.ceil(
            self.total_rows / self.batch_size
        )

        for batch in range(total_batches):

            logger.info(
                f"Batch {batch + 1}/{total_batches} Started..."
            )

            current_batch = min(
                self.batch_size,
                self.total_rows - (batch * self.batch_size)
            )

            df = self.generate_batch(
                batch,
                current_batch
            )

            if batch == 0:

                df.to_csv(
                    output_file,
                    index=False,
                    mode="w"
                )

            else:

                df.to_csv(
                    output_file,
                    index=False,
                    mode="a",
                    header=False
                )

            logger.info(
                f"Batch {batch + 1} Completed "
                f"({len(df):,} Rows)"
            )

            del df

        logger.info("=" * 70)
        logger.info("Shipments Dataset Generated Successfully")
        logger.info("=" * 70)

        return output_file

    def validate_dataset(self, output_file):
        """
        Validate Shipments Dataset
        """

        logger.info("Validating Shipments Dataset...")

        df = pd.read_csv(
            output_file,
            nrows=1000
        )

        required_columns = [

            "shipment_id",
            "order_id",
            "tracking_number",
            "courier_partner",
            "warehouse",
            "dispatch_date",
            "expected_delivery",
            "actual_delivery",
            "shipping_status",
            "shipping_cost",
            "created_date"

        ]

        missing = set(required_columns) - set(df.columns)

        if missing:

            raise ValueError(
                f"Missing Columns : {missing}"
            )

        logger.info(
            "Shipments Dataset Validation Successful."
        )

    def generate_metadata(self, output_file):
        """
        Generate Metadata JSON
        """

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        metadata = {

            "table_name": "shipments",

            "rows": self.total_rows,

            "columns": 11,

            "batch_size": self.batch_size,

            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "execution_time_seconds": execution_time,

            "file_name": output_file.name,

            "file_size_mb": round(
                output_file.stat().st_size /
                (1024 * 1024),
                2
            )

        }

        metadata_file = (
            self.log_folder /
            "shipments_metadata.json"
        )

        with open(
            metadata_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

        logger.info(
            f"Metadata Saved : {metadata_file}"
        )

    def print_summary(self, output_file):
        """
        Print Dataset Summary
        """

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        df = pd.read_csv(
            output_file,
            nrows=5
        )

        print("\n" + "=" * 90)
        print(" Enterprise Gadget Store - Shipments Dataset")
        print("=" * 90)

        print(f"Rows Generated      : {self.total_rows:,}")
        print(f"Columns             : {len(df.columns)}")
        print(f"Execution Time      : {execution_time} Seconds")
        print(f"Batch Size          : {self.batch_size:,}")
        print(f"Output File         : data/raw/shipments.csv")

        print("=" * 90)

        print("\nSample Records\n")

        print(df)

        print("\nShipping Status Distribution\n")

        print(
            pd.read_csv(
                output_file,
                usecols=["shipping_status"]
            )["shipping_status"].value_counts()
        )

        print("\nCourier Partner Distribution\n")

        print(
            pd.read_csv(
                output_file,
                usecols=["courier_partner"]
            )["courier_partner"].value_counts()
        )

        print("\nWarehouse Distribution\n")

        print(
            pd.read_csv(
                output_file,
                usecols=["warehouse"]
            )["warehouse"].value_counts()
        )

        print("\nAverage Shipping Cost")

        shipping_cost = pd.read_csv(
            output_file,
            usecols=["shipping_cost"]
        )["shipping_cost"].mean()

        print(f"₹ {shipping_cost:,.2f}")

        print("\n" + "=" * 90)
        print("Shipments Dataset Generated Successfully")
        print("=" * 90)

    def run(self):
        """
        Execute Complete Shipment Generation Pipeline
        """

        try:

            logger.info("=" * 70)
            logger.info("Shipment Generation Started")
            logger.info("=" * 70)

            output_file = self.generate_shipments()

            self.validate_dataset(output_file)

            self.generate_metadata(output_file)

            self.print_summary(output_file)

            logger.info("=" * 70)
            logger.info("Shipment Generation Completed Successfully")
            logger.info("=" * 70)

        except Exception as error:

            logger.exception(error)

            raise


def main():
    """
    Main Entry Point
    """

    generator = ShipmentGenerator()

    generator.run()


if __name__ == "__main__":

    main()
