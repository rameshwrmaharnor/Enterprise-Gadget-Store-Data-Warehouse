"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generate Products Dataset

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


class ProductGenerator:
    """
    Enterprise Product Dataset Generator
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

        self.total_rows = config["dataset"]["products"]

        logger.info("Loading Categories Dataset...")

        self.categories = pd.read_csv(
            self.output_folder / "categories.csv"
        )

        logger.info("Loading Suppliers Dataset...")

        self.suppliers = pd.read_csv(
            self.output_folder / "suppliers.csv"
        )

        self.brands = [

            "Apple",
            "Samsung",
            "Dell",
            "HP",
            "Lenovo",
            "Asus",
            "Acer",
            "Sony",
            "LG",
            "MSI",
            "Intel",
            "AMD",
            "Logitech",
            "Canon",
            "Epson",
            "JBL",
            "Boat",
            "Noise",
            "Realme",
            "Xiaomi"

        ]

        self.colors = [

            "Black",
            "White",
            "Silver",
            "Gray",
            "Blue",
            "Red",
            "Green",
            "Gold",
            "Pink",
            "Purple"

        ]

        self.materials = [

            "Plastic",
            "Metal",
            "Aluminium",
            "Carbon Fiber",
            "Glass"

        ]
        self.used_sku = set()
        self.used_barcode = set()

    def generate_sku(self):
        """
        Generate Unique SKU
        """

        while True:

            prefix = "".join(
                random.choices(
                    string.ascii_uppercase,
                    k=3
                )
            )

            number = random.randint(
                100000,
                999999
            )

            sku = f"{prefix}-{number}"

            if sku not in self.used_sku:

                self.used_sku.add(sku)

                return sku

    def generate_barcode(self):
        """
        Generate Unique Barcode
        """

        while True:

            barcode = "".join(
                random.choices(
                    string.digits,
                    k=13
                )
            )

            if barcode not in self.used_barcode:

                self.used_barcode.add(barcode)

                return barcode

    def generate_product_name(self, brand, category):
        """
        Generate Product Name
        """

        model = random.choice([
            "Pro",
            "Max",
            "Ultra",
            "Plus",
            "Prime",
            "Elite",
            "Air",
            "Neo",
            "Edge",
            "Vision"
        ])

        series = random.randint(100, 999)

        return f"{brand} {category} {model} {series}"

    def generate_dimensions(self):
        """
        Generate Product Dimensions
        """

        length = round(random.uniform(5, 60), 1)

        width = round(random.uniform(5, 60), 1)

        height = round(random.uniform(1, 20), 1)

        return f"{length} x {width} x {height} cm"

    def generate_weight(self):
        """
        Generate Product Weight
        """

        return round(random.uniform(0.10, 12.00), 2)

    def calculate_pricing(self):
        """
        Generate Cost, Selling Price,
        Profit Margin & Discount
        """

        cost = round(random.uniform(500, 200000), 2)

        margin = random.randint(10, 45)

        selling = round(cost * (1 + margin / 100), 2)

        discount = random.choice([0, 5, 10, 15, 20, 25])

        return cost, selling, margin, discount

    def build_products(self):
        """
        Generate Enterprise Products Dataset
        """

        logger.info("Generating Products Dataset...")

        products = []

        category_ids = self.categories["category_id"].tolist()
        category_names = dict(
            zip(
                self.categories["category_id"],
                self.categories["category_name"]
            )
        )

        supplier_ids = self.suppliers["supplier_id"].tolist()

        for i in range(1, self.total_rows + 1):

            category_id = random.choice(category_ids)

            supplier_id = random.choice(supplier_ids)

            category_name = category_names[category_id]

            brand = random.choice(self.brands)

            cost_price, selling_price, margin, discount = (
                self.calculate_pricing()
            )

            manufacture_date = self.fake.date_between(
                start_date="-5y",
                end_date="-30d"
            )

            launch_date = self.fake.date_between(
                start_date=manufacture_date,
                end_date="today"
            )

            products.append({

                "product_id": f"PRD{i:06}",

                "sku": self.generate_sku(),

                "barcode": self.generate_barcode(),

                "product_name": self.generate_product_name(
                    brand,
                    category_name
                ),

                "brand": brand,

                "category_id": category_id,

                "supplier_id": supplier_id,

                "color": random.choice(self.colors),

                "material": random.choice(self.materials),

                "warranty_months": random.choice(
                    [6, 12, 18, 24, 36]
                ),

                "manufacturing_cost": cost_price,

                "selling_price": selling_price,

                "profit_margin_percent": margin,

                "discount_percent": discount,

                "weight_kg": self.generate_weight(),

                "dimensions": self.generate_dimensions(),

                "stock_quantity": random.randint(0, 500),

                "reorder_level": random.randint(10, 80),

                "rating": round(
                    random.uniform(3.5, 5.0),
                    1
                ),

                "manufacture_date": manufacture_date,

                "launch_date": launch_date,

                "product_status": random.choice(
                    [
                        "Available",
                        "Discontinued",
                        "Out Of Stock"
                    ]
                ),

                "is_active": random.choice(
                    [True, True, True, False]
                ),

                "created_date": datetime.now().date()

            })

            if i % 10000 == 0:

                logger.info(f"{i:,} Products Generated...")

        df = pd.DataFrame(products)

        logger.info(
            f"Total Products Generated : {len(df):,}"
        )

        return df

    def validate_dataset(self, df: pd.DataFrame):
        """
        Validate Products Dataset
        """

        logger.info("Validating Products Dataset...")

        if df.empty:
            raise ValueError("Products dataset is empty.")

        if df["product_id"].duplicated().sum() > 0:
            raise ValueError("Duplicate Product IDs Found.")

        if df["sku"].duplicated().sum() > 0:
            raise ValueError("Duplicate SKU Found.")

        if df["barcode"].duplicated().sum() > 0:
            raise ValueError("Duplicate Barcode Found.")

        valid_categories = set(
            self.categories["category_id"]
        )

        invalid_categories = (
            ~df["category_id"].isin(valid_categories)
        ).sum()

        if invalid_categories > 0:
            raise ValueError(
                f"{invalid_categories} Invalid Category IDs Found."
            )

        valid_suppliers = set(
            self.suppliers["supplier_id"]
        )

        invalid_suppliers = (
            ~df["supplier_id"].isin(valid_suppliers)
        ).sum()

        if invalid_suppliers > 0:
            raise ValueError(
                f"{invalid_suppliers} Invalid Supplier IDs Found."
            )

        if len(df) != self.total_rows:
            raise ValueError(
                f"Expected {self.total_rows} rows "
                f"but generated {len(df)} rows."
            )

        logger.info("Products Dataset Validation Successful.")

    def save_dataset(self, df: pd.DataFrame):
        """
        Save Products Dataset
        """

        output_file = self.output_folder / "products.csv"

        df.to_csv(
            output_file,
            index=config["output"]["index"],
            encoding=config["output"]["encoding"]
        )

        logger.info(f"Dataset Saved : {output_file}")

        return output_file

    def generate_metadata(
        self,
        df: pd.DataFrame,
        output_file: Path
    ):
        """
        Generate Metadata JSON
        """

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        metadata = {

            "table_name": "products",

            "rows": len(df),

            "columns": len(df.columns),

            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "execution_time_seconds": execution_time,

            "file_name": output_file.name,

            "file_size_mb": round(
                output_file.stat().st_size /
                (1024 * 1024),
                2
            ),

            "columns_list": list(df.columns)

        }

        metadata_file = (
            self.log_folder /
            "products_metadata.json"
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

    def print_summary(self, df: pd.DataFrame):
        """
        Print Dataset Summary
        """

        execution_time = round(
            time.time() - self.start_time,
            2
        )

        print("\n" + "=" * 80)
        print(" Enterprise Gadget Store - Products Dataset")
        print("=" * 80)

        print(f"Rows Generated      : {len(df):,}")
        print(f"Columns             : {len(df.columns)}")
        print(f"Execution Time      : {execution_time} Seconds")
        print(f"Output File         : data/raw/products.csv")

        print("=" * 80)

        print("\nSample Records\n")

        print(df.head())

        print("\nTop 10 Brands\n")

        print(df["brand"].value_counts().head(10))

        print("\nTop 10 Categories\n")

        print(
            df.groupby("category_id")
              .size()
              .sort_values(ascending=False)
              .head(10)
        )

        print("\nTop 10 Suppliers\n")

        print(
            df.groupby("supplier_id")
              .size()
              .sort_values(ascending=False)
              .head(10)
        )

        print("\nAverage Selling Price")

        print(f"₹ {df['selling_price'].mean():,.2f}")

        print("\nAverage Manufacturing Cost")

        print(f"₹ {df['manufacturing_cost'].mean():,.2f}")

        print("\nAverage Profit Margin")

        print(f"{df['profit_margin_percent'].mean():.2f}%")

        print("\nAverage Product Rating")

        print(f"{df['rating'].mean():.2f}")

        print("\nTotal Stock Quantity")

        print(f"{df['stock_quantity'].sum():,}")

        inventory_value = (
            df["selling_price"] *
            df["stock_quantity"]
        ).sum()

        print("\nEstimated Inventory Value")

        print(f"₹ {inventory_value:,.2f}")

        print("\nProduct Status Distribution\n")

        print(df["product_status"].value_counts())

        print("\n" + "=" * 80)
        print("Products Dataset Generated Successfully")
        print("=" * 80)

    def run(self):
        """
        Execute Complete Product Generation Pipeline
        """

        try:

            logger.info("=" * 70)
            logger.info("Product Generation Started")
            logger.info("=" * 70)

            df = self.build_products()

            self.validate_dataset(df)

            output_file = self.save_dataset(df)

            self.generate_metadata(df, output_file)

            self.print_summary(df)

            logger.info("=" * 70)
            logger.info("Product Generation Completed Successfully")
            logger.info("=" * 70)

        except Exception as error:

            logger.exception(error)

            raise


def main():
    """
    Main Entry Point
    """

    generator = ProductGenerator()

    generator.run()


if __name__ == "__main__":

    main()
