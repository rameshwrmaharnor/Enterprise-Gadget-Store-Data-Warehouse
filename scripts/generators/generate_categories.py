"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generate Categories Dataset

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

from utils.logger import logger
from utils.config import config
import pandas as pd
from pathlib import Path
from datetime import datetime
import time
import json
import random


class CategoryGenerator:
    """
    Enterprise Category Dataset Generator
    """

    def __init__(self):

        self.start_time = time.time()

        random.seed(config["random_seed"])

        self.output_folder = Path(config["paths"]["raw"])
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.log_folder = Path(config["paths"]["logs"])
        self.log_folder.mkdir(parents=True, exist_ok=True)

        self.total_rows = config["dataset"]["categories"]

        self.categories = {

            "Computers": [

                "Laptops",
                "Desktops",
                "Processors",
                "Motherboards",
                "RAM",
                "Graphics Cards",
                "SSD",
                "HDD",
                "Monitors",
                "Networking"

            ],

            "Accessories": [

                "Keyboard",
                "Mouse",
                "Headphones",
                "Webcam",
                "Speakers",
                "Power Bank",
                "Laptop Bag",
                "USB Hub",
                "HDMI Cable",
                "Chargers"

            ],

            "Gaming": [

                "Gaming Console",
                "Gaming Keyboard",
                "Gaming Mouse",
                "Gaming Chair",
                "Gaming Headset",
                "Game Controller",
                "Capture Card",
                "Streaming Camera",
                "RGB Lighting",
                "Gaming Desk"

            ],

            "Smart Devices": [

                "Smartphone",
                "Tablet",
                "Smart Watch",
                "Drone",
                "VR Headset",
                "Smart TV",
                "Smart Home",
                "Security Camera",
                "Printer",
                "Projector"

            ]

        }

    def build_categories(self):
        """
        Build Category Data
        """

        logger.info("Generating Category Dataset...")

        rows = []

        category_counter = 1

        for department, category_list in self.categories.items():

            for category in category_list:

                rows.append({

                    "category_id": f"CAT{category_counter:04}",

                    "category_name": category,

                    "department": department,

                    "description": f"{category} related electronic products",

                    "is_active": True,

                    "created_date": datetime.now().date()

                })

                category_counter += 1

        while len(rows) < self.total_rows:

            department = random.choice(list(self.categories.keys()))

            category = f"{department} Category {category_counter}"

            rows.append({

                "category_id": f"CAT{category_counter:04}",

                "category_name": category,

                "department": department,

                "description": "Auto Generated Category",

                "is_active": True,

                "created_date": datetime.now().date()

            })

            category_counter += 1

        df = pd.DataFrame(rows)

        logger.info(f"Generated {len(df)} Categories Successfully")

        return df

    def save_dataset(self, df: pd.DataFrame):
        """
        Save dataset to CSV
        """

        output_file = self.output_folder / "categories.csv"

        df.to_csv(
            output_file,
            index=config["output"]["index"],
            encoding=config["output"]["encoding"]
        )

        logger.info(f"Dataset Saved : {output_file}")

        return output_file

    def generate_metadata(self, df: pd.DataFrame, output_file: Path):
        """
        Generate metadata JSON
        """

        execution_time = round(time.time() - self.start_time, 2)

        metadata = {

            "table_name": "categories",

            "rows": len(df),

            "columns": len(df.columns),

            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "execution_time_seconds": execution_time,

            "file_name": output_file.name,

            "file_size_mb": round(
                output_file.stat().st_size / (1024 * 1024),
                2
            ),

            "columns_list": list(df.columns)

        }

        metadata_file = self.log_folder / "categories_metadata.json"

        with open(metadata_file, "w", encoding="utf-8") as file:

            json.dump(metadata, file, indent=4)

        logger.info(f"Metadata Saved : {metadata_file}")

    def validate_dataset(self, df: pd.DataFrame):
        """
        Basic Dataset Validation
        """

        logger.info("Validating Categories Dataset...")

        if df.empty:
            raise ValueError("Generated dataset is empty.")

        if df["category_id"].duplicated().sum() > 0:
            raise ValueError("Duplicate Category IDs found.")

        if df["category_name"].duplicated().sum() > 0:
            logger.warning("Duplicate Category Names detected.")

        if len(df) != self.total_rows:
            logger.warning(
                f"Expected {self.total_rows} rows, "
                f"Generated {len(df)} rows."
            )

        logger.info("Validation Completed Successfully.")

    def print_summary(self, df: pd.DataFrame):
        """
        Print Dataset Summary
        """

        execution_time = round(time.time() - self.start_time, 2)

        print("\n" + "=" * 65)
        print(" Enterprise Gadget Store - Categories Dataset")
        print("=" * 65)

        print(f"Rows Generated      : {len(df):,}")
        print(f"Columns             : {len(df.columns)}")
        print(f"Execution Time      : {execution_time} Seconds")
        print(f"Output File         : data/raw/categories.csv")

        print("=" * 65)

        print("\nSample Records\n")
        print(df.head())

        print("\nCategory Count By Department\n")
        print(df.groupby("department")["category_name"].count())

        print("\n" + "=" * 65)
        print("Categories Dataset Generated Successfully")
        print("=" * 65)

    def run(self):
        """
        Execute Complete Pipeline
        """

        try:

            logger.info("=" * 60)
            logger.info("Category Generation Started")
            logger.info("=" * 60)

            df = self.build_categories()

            self.validate_dataset(df)

            output_file = self.save_dataset(df)

            self.generate_metadata(df, output_file)

            self.print_summary(df)

            logger.info("=" * 60)
            logger.info("Category Generation Completed Successfully")
            logger.info("=" * 60)

        except Exception as error:

            logger.exception(error)

            raise


def main():
    """
    Main Entry Point
    """

    generator = CategoryGenerator()

    generator.run()


if __name__ == "__main__":

    main()
