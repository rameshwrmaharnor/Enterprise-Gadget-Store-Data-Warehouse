"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generate Coupons Dataset

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

from utils.config import config
from utils.logger import logger


class CouponGenerator:
    """
    Enterprise Coupon Dataset Generator
    """

    def __init__(self):

        random.seed(config["random_seed"])

        self.start_time = time.time()

        self.output_folder = Path(config["paths"]["raw"])
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.log_folder = Path(config["paths"]["logs"])
        self.log_folder.mkdir(parents=True, exist_ok=True)

        self.total_rows = config["dataset"]["coupons"]

        self.discount_types = [

            "Percentage",
            "Flat"

        ]

        self.customer_segments = [

            "Regular",
            "Silver",
            "Gold",
            "Platinum"

        ]

        self.status = [

            "Active",
            "Expired",
            "Scheduled"

        ]

        self.used_codes = set()

    def generate_coupon_code(self):
        """
        Generate Unique Coupon Code
        """

        while True:

            prefix = random.choice([
                "WELCOME",
                "SAVE",
                "MEGA",
                "SUPER",
                "FESTIVE",
                "BIGSALE",
                "FLASH",
                "NEWUSER",
                "PREMIUM",
                "SMART"
            ])

            suffix = "".join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=6
                )
            )

            code = f"{prefix}_{suffix}"

            if code not in self.used_codes:

                self.used_codes.add(code)

                return code

    def generate_discount(self, discount_type):
        """
        Generate Discount Details
        """

        if discount_type == "Percentage":

            discount_value = random.choice(
                [5, 10, 15, 20, 25, 30, 40, 50]
            )

            maximum_discount = random.choice(
                [250, 500, 750, 1000, 1500, 2000]
            )

        else:

            discount_value = random.choice(
                [100, 200, 300, 500, 750, 1000, 1500]
            )

            maximum_discount = discount_value

        return discount_value, maximum_discount

    def generate_validity(self):
        """
        Generate Coupon Validity
        """

        start_date = datetime.strptime(
            "2024-01-01",
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            "2028-12-31",
            "%Y-%m-%d"
        ).date()

        valid_from = start_date + pd.to_timedelta(
            random.randint(0, 1200),
            unit="D"
        )

        valid_to = valid_from + pd.to_timedelta(
            random.randint(15, 180),
            unit="D"
        )

        return valid_from, valid_to

    def build_coupons(self):
        """
        Generate Enterprise Coupons Dataset
        """

        logger.info("Generating Coupons Dataset...")

        coupons = []

        for i in range(1, self.total_rows + 1):

            discount_type = random.choice(
                self.discount_types
            )

            discount_value, maximum_discount = (
                self.generate_discount(
                    discount_type
                )
            )

            valid_from, valid_to = (
                self.generate_validity()
            )

            usage_limit = random.choice(
                [
                    100,
                    250,
                    500,
                    1000,
                    5000,
                    10000
                ]
            )

            used_count = random.randint(
                0,
                usage_limit
            )

            coupons.append({

                "coupon_id": f"CPN{i:06}",

                "coupon_code": self.generate_coupon_code(),

                "coupon_name": f"Coupon {i}",

                "discount_type": discount_type,

                "discount_value": discount_value,

                "minimum_order_amount": random.choice(
                    [
                        500,
                        1000,
                        1500,
                        2000,
                        3000,
                        5000,
                        10000
                    ]
                ),

                "maximum_discount": maximum_discount,

                "applicable_segment": random.choice(
                    self.customer_segments
                ),

                "valid_from": valid_from,

                "valid_to": valid_to,

                "usage_limit": usage_limit,

                "used_count": used_count,

                "coupon_status": random.choice(
                    self.status
                ),

                "is_active": random.choices(
                    [True, False],
                    weights=[85, 15],
                    k=1
                )[0],

                "created_date": datetime.now().date()

            })

            if i % 10000 == 0:

                logger.info(
                    f"{i:,} Coupons Generated..."
                )

        df = pd.DataFrame(coupons)

        logger.info(
            f"Total Coupons Generated : {len(df):,}"
        )

        return df

    def validate_dataset(self, df: pd.DataFrame):
        """
        Validate Coupons Dataset
        """

        logger.info("Validating Coupons Dataset...")

        if df.empty:
            raise ValueError("Coupon dataset is empty.")

        if df["coupon_id"].duplicated().sum() > 0:
            raise ValueError("Duplicate Coupon IDs Found.")

        if df["coupon_code"].duplicated().sum() > 0:
            raise ValueError("Duplicate Coupon Codes Found.")

        if len(df) != self.total_rows:
            raise ValueError(
                f"Expected {self.total_rows:,} rows "
                f"but generated {len(df):,} rows."
            )

        logger.info("Coupons Dataset Validation Successful.")

    def save_dataset(self, df: pd.DataFrame):
        """
        Save Coupons Dataset
        """

        output_file = self.output_folder / "coupons.csv"

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

            "table_name": "coupons",

            "rows": len(df),

            "columns": len(df.columns),

            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "execution_time_seconds": execution_time,

            "file_name": output_file.name,

            "file_size_mb": round(
                output_file.stat().st_size / (1024 * 1024),
                2
            ),

            "columns_list": list(df.columns)

        }

        metadata_file = (
            self.log_folder /
            "coupons_metadata.json"
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
        print(" Enterprise Gadget Store - Coupons Dataset")
        print("=" * 80)

        print(f"Rows Generated      : {len(df):,}")
        print(f"Columns             : {len(df.columns)}")
        print(f"Execution Time      : {execution_time} Seconds")
        print(f"Output File         : data/raw/coupons.csv")

        print("=" * 80)

        print("\nSample Records\n")

        print(df.head())

        print("\nDiscount Type Distribution\n")

        print(df["discount_type"].value_counts())

        print("\nApplicable Customer Segments\n")

        print(df["applicable_segment"].value_counts())

        print("\nCoupon Status Distribution\n")

        print(df["coupon_status"].value_counts())

        print("\nActive Coupons")

        print(df["is_active"].value_counts())

        print("\nAverage Discount Value")

        print(round(df["discount_value"].mean(), 2))

        print("\nAverage Minimum Order Amount")

        print(f"₹ {df['minimum_order_amount'].mean():,.2f}")

        print("\nAverage Maximum Discount")

        print(f"₹ {df['maximum_discount'].mean():,.2f}")

        print("\nAverage Usage Limit")

        print(round(df["usage_limit"].mean(), 2))

        print("\nAverage Used Count")

        print(round(df["used_count"].mean(), 2))

        print("\nTop 10 Highest Discount Coupons\n")

        print(
            df.sort_values(
                by="discount_value",
                ascending=False
            )[[
                "coupon_code",
                "discount_type",
                "discount_value"
            ]].head(10)
        )

        print("\n" + "=" * 80)
        print("Coupons Dataset Generated Successfully")
        print("=" * 80)

    def run(self):
        """
        Execute Complete Coupon Generation Pipeline
        """

        try:

            logger.info("=" * 70)
            logger.info("Coupon Generation Started")
            logger.info("=" * 70)

            df = self.build_coupons()

            self.validate_dataset(df)

            output_file = self.save_dataset(df)

            self.generate_metadata(
                df,
                output_file
            )

            self.print_summary(df)

            logger.info("=" * 70)
            logger.info("Coupon Generation Completed Successfully")
            logger.info("=" * 70)

        except Exception as error:

            logger.exception(error)

            raise


def main():
    """
    Main Entry Point
    """

    generator = CouponGenerator()

    generator.run()


if __name__ == "__main__":

    main()
