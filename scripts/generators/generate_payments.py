"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generate Payments Dataset

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


class PaymentGenerator:
    """
    Enterprise Payment Dataset Generator
    """

    def __init__(self):

        random.seed(config["random_seed"])

        self.start_time = time.time()

        self.output_folder = Path(config["paths"]["raw"])
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.log_folder = Path(config["paths"]["logs"])
        self.log_folder.mkdir(parents=True, exist_ok=True)

        self.total_rows = config["dataset"]["payments"]

        self.batch_size = 100000

        logger.info("Loading Orders Dataset...")

        self.orders = pd.read_csv(

            self.output_folder / "orders.csv",

            usecols=[
                "order_id",
                "total_amount",
                "payment_method",
                "payment_status",
                "order_date"
            ]

        )

        self.payment_gateways = [

            "Razorpay",
            "Stripe",
            "PayU",
            "PhonePe",
            "Google Pay",
            "Amazon Pay"

        ]

        self.banks = [

            "HDFC Bank",
            "ICICI Bank",
            "SBI",
            "Axis Bank",
            "Kotak Bank",
            "Punjab National Bank"

        ]

        self.card_types = [

            "Visa",
            "MasterCard",
            "RuPay",
            "American Express"

        ]
    def generate_transaction_id(self):
        """
        Generate Unique Transaction ID
        """

        return "TXN" + "".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=14
            )
        )

    def generate_batch(
        self,
        batch_number,
        batch_size
    ):
        """
        Generate One Batch of Payments
        """

        start = batch_number * self.batch_size

        end = min(
            start + batch_size,
            len(self.orders)
        )

        batch_orders = self.orders.iloc[start:end]

        payments = []

        payment_no = start + 1

        for row in batch_orders.to_dict("records"):

            order_date = pd.Timestamp(
                row["order_date"]
            )

            payment_date = order_date + pd.Timedelta(
                hours=random.randint(0, 72)
            )

            payments.append({

                "payment_id": f"PAY{payment_no:08}",

                "order_id": row["order_id"],

                "transaction_id": self.generate_transaction_id(),

                "payment_gateway": random.choice(
                    self.payment_gateways
                ),

                "payment_method": row["payment_method"],

                "payment_amount": row["total_amount"],

                "payment_status": row["payment_status"],

                "payment_date": payment_date,

                "bank_name": random.choice(
                    self.banks
                ),

                "card_type": random.choice(
                    self.card_types
                ),

                "currency": "INR",

                "created_date": datetime.now().date()

            })

            payment_no += 1

        return pd.DataFrame(payments)
    def generate_payments(self):
        """
        Generate Payments Dataset in Batches
        """

        logger.info("=" * 70)
        logger.info("Generating Payments in Batches...")
        logger.info("=" * 70)

        output_file = self.output_folder / "payments.csv"

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
        logger.info("Payments Dataset Generated Successfully")
        logger.info("=" * 70)

        return output_file
    def validate_dataset(self, output_file):
        """
        Validate Payments Dataset
        """

        logger.info("Validating Payments Dataset...")

        df = pd.read_csv(
            output_file,
            nrows=1000
        )

        required_columns = [

            "payment_id",
            "order_id",
            "transaction_id",
            "payment_gateway",
            "payment_method",
            "payment_amount",
            "payment_status",
            "payment_date",
            "bank_name",
            "card_type",
            "currency",
            "created_date"

        ]

        missing = set(required_columns) - set(df.columns)

        if missing:

            raise ValueError(
                f"Missing Columns : {missing}"
            )

        logger.info("Payments Dataset Validation Successful.")


    def generate_metadata(self, output_file):
        """
        Generate Metadata JSON
        """

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        metadata = {

            "table_name": "payments",

            "rows": self.total_rows,

            "columns": 12,

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
            "payments_metadata.json"
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
        print(" Enterprise Gadget Store - Payments Dataset")
        print("=" * 90)

        print(f"Rows Generated      : {self.total_rows:,}")
        print(f"Columns             : {len(df.columns)}")
        print(f"Execution Time      : {execution_time} Seconds")
        print(f"Batch Size          : {self.batch_size:,}")
        print(f"Output File         : data/raw/payments.csv")

        print("=" * 90)

        print("\nSample Records\n")

        print(df)

        print("\n" + "=" * 90)
        print("Payments Dataset Generated Successfully")
        print("=" * 90)


    def run(self):
        """
        Execute Complete Payment Generation Pipeline
        """

        try:

            logger.info("=" * 70)
            logger.info("Payment Generation Started")
            logger.info("=" * 70)

            output_file = self.generate_payments()

            self.validate_dataset(output_file)

            self.generate_metadata(output_file)

            self.print_summary(output_file)

            logger.info("=" * 70)
            logger.info("Payment Generation Completed Successfully")
            logger.info("=" * 70)

        except Exception as error:

            logger.exception(error)

            raise


def main():

    generator = PaymentGenerator()

    generator.run()


if __name__ == "__main__":

    main()
