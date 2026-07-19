"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generate Suppliers Dataset

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import json
import random
import string
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from faker import Faker

from utils.config import config
from utils.logger import logger


class SupplierGenerator:
    """
    Enterprise Supplier Dataset Generator
    """

    def __init__(self):

        self.fake = Faker("en_IN")

        random.seed(config["random_seed"])

        Faker.seed(config["random_seed"])

        self.start_time = time.time()

        self.output_folder = Path(config["paths"]["raw"])
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.log_folder = Path(config["paths"]["logs"])
        self.log_folder.mkdir(parents=True, exist_ok=True)

        self.total_rows = config["dataset"]["suppliers"]

        self.company_types = [

            "Private Limited",
            "Public Limited",
            "LLP",
            "Corporation",
            "Partnership"

        ]

        self.payment_terms = [

            "Net 15",
            "Net 30",
            "Net 45",
            "Net 60",
            "Advance"

        ]

        self.contract_types = [

            "Gold",
            "Silver",
            "Bronze"

        ]

        self.states = [

            "Maharashtra",
            "Gujarat",
            "Karnataka",
            "Delhi",
            "Tamil Nadu",
            "Telangana",
            "Punjab",
            "Rajasthan"

        ]

        self.cities = [

            "Mumbai",
            "Pune",
            "Nagpur",
            "Ahmedabad",
            "Surat",
            "Bengaluru",
            "Hyderabad",
            "Chennai",
            "Delhi",
            "Jaipur"

        ]

    def generate_gst(self):
        """
        Generate Indian GST Number
        """

        state_code = str(random.randint(10, 38)).zfill(2)

        pan = (
            random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_uppercase)
            + str(random.randint(1000, 9999))
            + random.choice(string.ascii_uppercase)
        )

        return f"{state_code}{pan}1Z5"

    def generate_pan(self):
        """
        Generate PAN Number
        """

        letters = "".join(random.choices(string.ascii_uppercase, k=5))

        numbers = random.randint(1000, 9999)

        last = random.choice(string.ascii_uppercase)

        return f"{letters}{numbers}{last}"

    def generate_supplier_name(self):
        """
        Generate Supplier Company Name
        """

        prefixes = [

            "Tech",
            "Global",
            "Prime",
            "Vision",
            "Smart",
            "Next",
            "Future",
            "Elite",
            "Dynamic",
            "Vertex"

        ]

        suffixes = [

            "Electronics",
            "Technologies",
            "Solutions",
            "Systems",
            "Supplies",
            "Components",
            "Industries",
            "Traders",
            "Enterprises",
            "Networks"

        ]

        company = (
            random.choice(prefixes)
            + " "
            + random.choice(suffixes)
        )

        return company

    def build_suppliers(self):
        """
        Generate Supplier Dataset
        """

        logger.info("Generating Suppliers Dataset...")

        suppliers = []

        for i in range(1, self.total_rows + 1):

            company_name = self.generate_supplier_name()

            suppliers.append({

                "supplier_id": f"SUP{i:05}",

                "supplier_name": company_name,

                "company_type": random.choice(self.company_types),

                "contact_person": self.fake.name(),

                "email": self.fake.company_email(),

                "phone": self.fake.phone_number(),

                "gst_number": self.generate_gst(),

                "pan_number": self.generate_pan(),

                "city": random.choice(self.cities),

                "state": random.choice(self.states),

                "country": "India",

                "supplier_rating": round(random.uniform(3.0, 5.0), 1),

                "payment_terms": random.choice(self.payment_terms),

                "contract_type": random.choice(self.contract_types),

                "credit_limit": random.randint(500000, 10000000),

                "registration_date": self.fake.date_between(
                    start_date="-10y",
                    end_date="today"
                ),

                "is_active": random.choice([True, True, True, True, False])

            })

            if i % 1000 == 0:
                logger.info(f"{i:,} Suppliers Generated...")

        df = pd.DataFrame(suppliers)

        logger.info(f"Total Suppliers Generated : {len(df):,}")

        return df

    def validate_dataset(self, df: pd.DataFrame):
        """
        Validate Supplier Dataset
        """

        logger.info("Validating Supplier Dataset...")

        if df.empty:
            raise ValueError("Supplier dataset is empty.")

        if df["supplier_id"].duplicated().sum() > 0:
            raise ValueError("Duplicate Supplier IDs Found.")

        if df["gst_number"].duplicated().sum() > 0:
            logger.warning("Duplicate GST Numbers Detected.")

        if df["pan_number"].duplicated().sum() > 0:
            logger.warning("Duplicate PAN Numbers Detected.")

        if len(df) != self.total_rows:
            raise ValueError(
                f"Expected {self.total_rows} rows but generated {len(df)} rows."
            )

        logger.info("Supplier Dataset Validation Successful.")

    def save_dataset(self, df: pd.DataFrame):
        """
        Save Supplier Dataset
        """

        output_file = self.output_folder / "suppliers.csv"

        df.to_csv(
            output_file,
            index=config["output"]["index"],
            encoding=config["output"]["encoding"]
        )

        logger.info(f"Dataset Saved : {output_file}")

        return output_file

    def generate_metadata(self, df: pd.DataFrame, output_file: Path):
        """
        Generate Metadata JSON
        """

        execution_time = round(time.time() - self.start_time, 2)

        metadata = {

            "table_name": "suppliers",

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

        metadata_file = self.log_folder / "suppliers_metadata.json"

        with open(metadata_file, "w", encoding="utf-8") as file:

            json.dump(metadata, file, indent=4)

        logger.info(f"Metadata Saved : {metadata_file}")

    def print_summary(self, df: pd.DataFrame):
        """
        Print Dataset Summary
        """

        execution_time = round(time.time() - self.start_time, 2)

        print("\n" + "=" * 70)
        print(" Enterprise Gadget Store - Suppliers Dataset")
        print("=" * 70)

        print(f"Rows Generated      : {len(df):,}")
        print(f"Columns             : {len(df.columns)}")
        print(f"Execution Time      : {execution_time} Seconds")
        print(f"Output File         : data/raw/suppliers.csv")

        print("=" * 70)

        print("\nSample Records\n")

        print(df.head())

        print("\nSupplier Distribution By Contract Type\n")

        print(df["contract_type"].value_counts())

        print("\nSupplier Distribution By Company Type\n")

        print(df["company_type"].value_counts())

        print("\nAverage Supplier Rating")

        print(round(df["supplier_rating"].mean(), 2))

        print("\nAverage Credit Limit")

        print(f"₹ {round(df['credit_limit'].mean(), 2):,.2f}")

        print("\nTop 10 States")

        print(df["state"].value_counts().head(10))

        print("\nTop 10 Cities")

        print(df["city"].value_counts().head(10))

        print("\n" + "=" * 70)
        print("Suppliers Dataset Generated Successfully")
        print("=" * 70)

    def run(self):
        """
        Execute Complete Supplier Generation Pipeline
        """

        try:

            logger.info("=" * 60)
            logger.info("Supplier Generation Started")
            logger.info("=" * 60)

            df = self.build_suppliers()

            self.validate_dataset(df)

            output_file = self.save_dataset(df)

            self.generate_metadata(df, output_file)

            self.print_summary(df)

            logger.info("=" * 60)
            logger.info("Supplier Generation Completed Successfully")
            logger.info("=" * 60)

        except Exception as error:

            logger.exception(error)

            raise


def main():
    """
    Main Entry Point
    """

    generator = SupplierGenerator()

    generator.run()


if __name__ == "__main__":

    main()
