"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generate Orders Dataset

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import json
import random
import time
import math
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

from utils.config import config
from utils.logger import logger


class OrderGenerator:
    """
    Enterprise Orders Dataset Generator
    """

    def __init__(self):

        self.fake = Faker("en_IN")

        Faker.seed(config["random_seed"])

        random.seed(config["random_seed"])

        self.start_time = time.time()

        self.output_folder = Path(config["paths"]["raw"])
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.log_folder = Path(config["paths"]["logs"])
        self.log_folder.mkdir(parents=True, exist_ok=True)

        self.total_rows = config["dataset"]["orders"]

        self.batch_size = 100000

        logger.info("Loading Customers Dataset...")

        self.customers = pd.read_csv(
            self.output_folder / "customers.csv",
            usecols=["customer_id"]
        )

        logger.info("Loading Coupons Dataset...")

        self.coupons = pd.read_csv(
            self.output_folder / "coupons.csv",
            usecols=["coupon_id"]
        )

        self.customer_ids = self.customers["customer_id"].tolist()

        self.coupon_ids = self.coupons["coupon_id"].tolist()

        self.payment_methods = [

            "UPI",
            "Credit Card",
            "Debit Card",
            "Net Banking",
            "Cash On Delivery"

        ]

        self.payment_status = [

            "Paid",
            "Pending",
            "Failed",
            "Refunded"

        ]

        self.order_status = [

            "Delivered",
            "Shipped",
            "Processing",
            "Cancelled",
            "Returned"

        ]

        self.delivery_type = [

            "Standard",
            "Express"

        ]

    def calculate_order_values(self):
        """
        Generate Order Financial Values
        """

        subtotal = round(
            random.uniform(500, 250000),
            2
        )

        if random.random() < 0.30:

            discount = round(
                subtotal * random.uniform(0.05, 0.30),
                2
            )

        else:

            discount = 0

        taxable_amount = subtotal - discount

        tax = round(
            taxable_amount * 0.18,
            2
        )

        shipping = random.choice(
            [
                0,
                49,
                99,
                149,
                199
            ]
        )

        total = round(
            taxable_amount + tax + shipping,
            2
        )

        return (
            subtotal,
            discount,
            tax,
            shipping,
            total
        )

    def generate_batch(
        self,
        start_order,
        batch_size
    ):
        """
        Generate One Batch of Orders
        """

        orders = []

        for i in range(start_order, start_order + batch_size):

            subtotal, discount, tax, shipping, total = (
                self.calculate_order_values()
            )

            order_date = self.fake.date_time_between(
                start_date="-5y",
                end_date="now"
            )

            expected_delivery = (
                order_date +
                timedelta(days=random.randint(2, 10))
            )

            coupon = None

            if random.random() < 0.30:

                coupon = random.choice(
                    self.coupon_ids
                )

            orders.append({

                "order_id": f"ORD{i:08}",

                "customer_id": random.choice(
                    self.customer_ids
                ),

                "coupon_id": coupon,

                "order_date": order_date,

                "subtotal": subtotal,

                "discount_amount": discount,

                "tax_amount": tax,

                "shipping_charge": shipping,

                "total_amount": total,

                "payment_method": random.choice(
                    self.payment_methods
                ),

                "payment_status": random.choices(
                    [
                        "Paid",
                        "Pending",
                        "Failed",
                        "Refunded"
                    ],
                    weights=[88, 7, 3, 2],
                    k=1
                )[0],

                "order_status": random.choices(
                    [
                        "Delivered",
                        "Shipped",
                        "Processing",
                        "Cancelled",
                        "Returned"
                    ],
                    weights=[70, 15, 8, 5, 2],
                    k=1
                )[0],

                "delivery_type": random.choice(
                    self.delivery_type
                ),

                "expected_delivery": expected_delivery,

                "created_date": datetime.now().date()

            })

        return pd.DataFrame(orders)

    def generate_orders(self):
        """
        Generate Orders Dataset in Batches
        """

        logger.info("=" * 70)
        logger.info("Generating Orders in Batches...")
        logger.info("=" * 70)

        output_file = self.output_folder / "orders.csv"

        if output_file.exists():
            output_file.unlink()

        total_batches = math.ceil(
            self.total_rows / self.batch_size
        )

        start_order = 1

        for batch in range(total_batches):

            logger.info(
                f"Batch {batch + 1}/{total_batches} Started..."
            )

            df = self.generate_batch(
                start_order,
                self.batch_size
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

            start_order += self.batch_size

            del df

        logger.info("=" * 70)
        logger.info("Orders Dataset Generated Successfully")
        logger.info("=" * 70)

        return output_file

    def validate_dataset(self, output_file):
        """
        Validate Generated Orders Dataset
        """

        logger.info("Validating Orders Dataset...")

        df = pd.read_csv(output_file, nrows=1000)

        required_columns = [

            "order_id",
            "customer_id",
            "coupon_id",
            "order_date",
            "subtotal",
            "discount_amount",
            "tax_amount",
            "shipping_charge",
            "total_amount",
            "payment_method",
            "payment_status",
            "order_status",
            "delivery_type",
            "expected_delivery",
            "created_date"

        ]

        missing = set(required_columns) - set(df.columns)

        if missing:

            raise ValueError(
                f"Missing Columns : {missing}"
            )

        logger.info("Validation Successful.")

    def generate_metadata(self, output_file):
        """
        Generate Metadata JSON
        """

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        metadata = {

            "table_name": "orders",

            "rows": self.total_rows,

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
            "orders_metadata.json"
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
        print(" Enterprise Gadget Store - Orders Dataset")
        print("=" * 90)

        print(f"Rows Generated      : {self.total_rows:,}")
        print(f"Columns             : {len(df.columns)}")
        print(f"Execution Time      : {execution_time} Seconds")
        print(f"Batch Size          : {self.batch_size:,}")
        print(f"Output File         : data/raw/orders.csv")
        print(
            f"File Size           : {round(output_file.stat().st_size/(1024*1024), 2)} MB")

        print("=" * 90)

        print("\nSample Records\n")

        print(df)

        print("\nEstimated Statistics\n")

        print(f"Customers           : {len(self.customer_ids):,}")
        print(f"Coupons             : {len(self.coupon_ids):,}")
        print(f"Orders              : {self.total_rows:,}")
        print(f"Batches             : {self.total_rows // self.batch_size}")

        print("\nPayment Methods")

        print(pd.read_csv(
            output_file,
            usecols=["payment_method"]
        )["payment_method"].value_counts())

        print("\nOrder Status")

        print(pd.read_csv(
            output_file,
            usecols=["order_status"]
        )["order_status"].value_counts())

        print("\nPayment Status")

        print(pd.read_csv(
            output_file,
            usecols=["payment_status"]
        )["payment_status"].value_counts())

        print("\n" + "=" * 90)
        print("Orders Dataset Generated Successfully")
        print("=" * 90)

    def run(self):
        """
        Execute Complete Orders Generation Pipeline
        """

        try:

            logger.info("=" * 70)
            logger.info("Orders Generation Started")
            logger.info("=" * 70)

            output_file = self.generate_orders()

            self.validate_dataset(output_file)

            self.generate_metadata(output_file)

            self.print_summary(output_file)

            logger.info("=" * 70)
            logger.info("Orders Generation Completed Successfully")
            logger.info("=" * 70)

        except Exception as error:

            logger.exception(error)

            raise


def main():
    """
    Main Entry Point
    """

    generator = OrderGenerator()

    generator.run()


if __name__ == "__main__":

    main()
