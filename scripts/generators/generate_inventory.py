"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generate Inventory Dataset

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import json
import math
import random
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from utils.config import config
from utils.logger import logger


class InventoryGenerator:
    """
    Enterprise Inventory Dataset Generator
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

        self.total_rows = config["dataset"]["inventory"]

        self.batch_size = 100000

        logger.info(
            "Loading Products Dataset..."
        )

        self.products = pd.read_csv(

            self.output_folder / "products.csv",

            usecols=[
                "product_id",
                "selling_price"
            ]

        )

        self.product_ids = self.products["product_id"].tolist()

        self.product_price = dict(

            zip(

                self.products["product_id"],

                self.products["selling_price"]

            )

        )

        self.warehouses = [

            "Mumbai WH",
            "Pune WH",
            "Delhi WH",
            "Bengaluru WH",
            "Hyderabad WH",
            "Chennai WH"

        ]

    def generate_batch(
        self,
        batch_number,
        batch_size
    ):
        """
        Generate One Batch of Inventory
        """

        start = batch_number * self.batch_size

        end = min(
            start + batch_size,
            self.total_rows
        )

        inventory = []

        inventory_no = start + 1

        for _ in range(start, end):

            product_id = random.choice(
                self.product_ids
            )

            warehouse = random.choice(
                self.warehouses
            )

            stock_quantity = random.randint(
                20,
                1000
            )

            reserved_stock = random.randint(
                0,
                int(stock_quantity * 0.20)
            )

            damaged_stock = random.randint(
                0,
                int(stock_quantity * 0.05)
            )

            available_stock = (
                stock_quantity
                - reserved_stock
                - damaged_stock
            )

            reorder_level = random.randint(
                25,
                150
            )

            reorder_status = (
                "Yes"
                if available_stock <= reorder_level
                else "No"
            )

            last_restock_date = (
                datetime.now()
                - pd.Timedelta(
                    days=random.randint(1, 180)
                )
            ).date()

            inventory_value = round(
                stock_quantity
                * self.product_price[product_id],
                2
            )

            inventory.append({

                "inventory_id": f"INV{inventory_no:08}",

                "product_id": product_id,

                "warehouse": warehouse,

                "stock_quantity": stock_quantity,

                "available_stock": available_stock,

                "reserved_stock": reserved_stock,

                "damaged_stock": damaged_stock,

                "reorder_level": reorder_level,

                "reorder_status": reorder_status,

                "last_restock_date": last_restock_date,

                "inventory_value": inventory_value,

                "created_date": datetime.now().date()

            })

            inventory_no += 1

        return pd.DataFrame(inventory)

    def generate_inventory(self):
        """
        Generate Inventory Dataset in Batches
        """

        logger.info("=" * 70)
        logger.info("Generating Inventory in Batches...")
        logger.info("=" * 70)

        output_file = self.output_folder / "inventory.csv"

        # Delete existing file
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
        logger.info("Inventory Dataset Generated Successfully")
        logger.info("=" * 70)

        return output_file

    def validate_dataset(self, output_file):
        """
        Validate Inventory Dataset
        """

        logger.info("Validating Inventory Dataset...")

        df = pd.read_csv(
            output_file,
            nrows=1000
        )

        required_columns = [

            "inventory_id",
            "product_id",
            "warehouse",
            "stock_quantity",
            "available_stock",
            "reserved_stock",
            "damaged_stock",
            "reorder_level",
            "reorder_status",
            "last_restock_date",
            "inventory_value",
            "created_date"

        ]

        missing = set(required_columns) - set(df.columns)

        if missing:

            raise ValueError(
                f"Missing Columns : {missing}"
            )

        if (df["available_stock"] < 0).any():

            raise ValueError(
                "Available stock cannot be negative."
            )

        logger.info(
            "Inventory Dataset Validation Successful."
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

            "table_name": "inventory",

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
            "inventory_metadata.json"
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
        print(" Enterprise Gadget Store - Inventory Dataset")
        print("=" * 90)

        print(f"Rows Generated      : {self.total_rows:,}")
        print(f"Columns             : {len(df.columns)}")
        print(f"Execution Time      : {execution_time} Seconds")
        print(f"Batch Size          : {self.batch_size:,}")
        print(f"Output File         : data/raw/inventory.csv")

        print("=" * 90)

        print("\nSample Records\n")

        print(df)

        print("\nWarehouse Distribution\n")

        print(
            pd.read_csv(
                output_file,
                usecols=["warehouse"]
            )["warehouse"].value_counts()
        )

        print("\nReorder Status Distribution\n")

        print(
            pd.read_csv(
                output_file,
                usecols=["reorder_status"]
            )["reorder_status"].value_counts()
        )

        stock = pd.read_csv(
            output_file,
            usecols=["stock_quantity"]
        )["stock_quantity"]

        print("\nAverage Stock Quantity")
        print(round(stock.mean(), 2))

        print("\nMaximum Stock Quantity")
        print(stock.max())

        print("\nMinimum Stock Quantity")
        print(stock.min())

        inventory_value = pd.read_csv(
            output_file,
            usecols=["inventory_value"]
        )["inventory_value"]

        print("\nTotal Inventory Value")
        print(f"₹ {inventory_value.sum():,.2f}")

        print("\nAverage Inventory Value")
        print(f"₹ {inventory_value.mean():,.2f}")

        print("\nHighest Inventory Value")
        print(f"₹ {inventory_value.max():,.2f}")

        print("\nLowest Inventory Value")
        print(f"₹ {inventory_value.min():,.2f}")

        print("\n" + "=" * 90)
        print("Inventory Dataset Generated Successfully")
        print("=" * 90)

    def run(self):
        """
        Execute Complete Inventory Generation Pipeline
        """

        try:

            logger.info("=" * 70)
            logger.info("Inventory Generation Started")
            logger.info("=" * 70)

            output_file = self.generate_inventory()

            self.validate_dataset(output_file)

            self.generate_metadata(output_file)

            self.print_summary(output_file)

            logger.info("=" * 70)
            logger.info("Inventory Generation Completed Successfully")
            logger.info("=" * 70)

        except Exception as error:

            logger.exception(error)

            raise


def main():
    """
    Main Entry Point
    """

    generator = InventoryGenerator()

    generator.run()


if __name__ == "__main__":

    main()
