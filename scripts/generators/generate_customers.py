"""
=========================================================
Enterprise Gadget Store Data Warehouse
Generate Customers Dataset

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

import json
import random
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from faker import Faker

from utils.config import config
from utils.logger import logger


class CustomerGenerator:
    """
    Enterprise Customer Dataset Generator
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

        self.total_rows = config["dataset"]["customers"]

        self.customer_segments = [

            "Regular",
            "Silver",
            "Gold",
            "Platinum"

        ]

        self.payment_methods = [

            "UPI",
            "Credit Card",
            "Debit Card",
            "Net Banking",
            "Cash On Delivery"

        ]

        self.device_types = [

            "Android",
            "iPhone",
            "Web",
            "Tablet"

        ]

        self.occupations = [

            "Software Engineer",
            "Doctor",
            "Teacher",
            "Business",
            "Student",
            "Government Employee",
            "Lawyer",
            "Engineer",
            "Designer",
            "Consultant"

        ]

        self.referral_sources = [

            "Google",
            "Facebook",
            "Instagram",
            "LinkedIn",
            "Friend",
            "Advertisement",
            "Direct"

        ]
    def generate_segment(self):
        """
        Generate Customer Segment
        Business Distribution
        """

        return random.choices(

            [
                "Regular",
                "Silver",
                "Gold",
                "Platinum"
            ],

            weights=[50, 30, 15, 5],

            k=1

        )[0]


    def generate_age(self):
        """
        Generate Customer Age
        """

        return random.randint(18, 65)


    def generate_income(self, segment):
        """
        Generate Annual Income
        """

        if segment == "Platinum":

            return random.randint(2500000, 10000000)

        elif segment == "Gold":

            return random.randint(1200000, 2500000)

        elif segment == "Silver":

            return random.randint(600000, 1200000)

        else:

            return random.randint(200000, 600000)


    def generate_loyalty_points(self, segment):
        """
        Generate Loyalty Points
        """

        if segment == "Platinum":

            return random.randint(15000, 50000)

        elif segment == "Gold":

            return random.randint(6000, 15000)

        elif segment == "Silver":

            return random.randint(2000, 6000)

        else:

            return random.randint(0, 2000)


    def generate_lifetime_value(self, segment):
        """
        Generate Customer Lifetime Value
        """

        if segment == "Platinum":

            return round(random.uniform(500000, 2500000), 2)

        elif segment == "Gold":

            return round(random.uniform(150000, 500000), 2)

        elif segment == "Silver":

            return round(random.uniform(50000, 150000), 2)

        else:

            return round(random.uniform(1000, 50000), 2)
    def build_customers(self):
        """
        Generate Enterprise Customers Dataset
        """

        logger.info("Generating Customers Dataset...")

        customers = []

        for i in range(1, self.total_rows + 1):

            gender = random.choice(["Male", "Female"])

            if gender == "Male":

                first_name = self.fake.first_name_male()

            else:

                first_name = self.fake.first_name_female()

            last_name = self.fake.last_name()

            full_name = f"{first_name} {last_name}"

            age = self.generate_age()

            dob = self.fake.date_of_birth(
                minimum_age=18,
                maximum_age=65
            )

            segment = self.generate_segment()

            annual_income = self.generate_income(segment)

            loyalty_points = self.generate_loyalty_points(segment)

            lifetime_value = self.generate_lifetime_value(segment)

            registration_date = self.fake.date_between(
                start_date="-8y",
                end_date="today"
            )

            last_login = self.fake.date_between(
                start_date=registration_date,
                end_date="today"
            )

            customers.append({

                "customer_id": f"CUS{i:07}",

                "first_name": first_name,

                "last_name": last_name,

                "full_name": full_name,

                "gender": gender,

                "date_of_birth": dob,

                "age": age,

                "email": self.fake.email(),

                "phone": self.fake.phone_number(),

                "address": self.fake.address().replace("\n", ", "),

                "city": self.fake.city(),

                "state": self.fake.state(),

                "country": "India",

                "pincode": self.fake.postcode(),

                "registration_date": registration_date,

                "customer_segment": segment,

                "loyalty_points": loyalty_points,

                "preferred_payment": random.choice(
                    self.payment_methods
                ),

                "annual_income": annual_income,

                "lifetime_value": lifetime_value,

                "occupation": random.choice(
                    self.occupations
                ),

                "marital_status": random.choice(
                    [
                        "Single",
                        "Married"
                    ]
                ),

                "email_verified": random.choices(
                    [True, False],
                    weights=[95, 5],
                    k=1
                )[0],

                "mobile_verified": random.choices(
                    [True, False],
                    weights=[97, 3],
                    k=1
                )[0],

                "last_login": last_login,

                "marketing_opt_in": random.choices(
                    [True, False],
                    weights=[65, 35],
                    k=1
                )[0],

                "referral_source": random.choice(
                    self.referral_sources
                ),

                "device_type": random.choice(
                    self.device_types
                ),

                "account_status": random.choices(
                    [
                        "Active",
                        "Inactive",
                        "Blocked"
                    ],
                    weights=[92, 6, 2],
                    k=1
                )[0],

                "is_active": True,

                "created_date": datetime.now().date()

            })

            if i % 25000 == 0:

                logger.info(f"{i:,} Customers Generated...")

        df = pd.DataFrame(customers)

        logger.info(
            f"Total Customers Generated : {len(df):,}"
        )

        return df
    def validate_dataset(self, df: pd.DataFrame):
        """
        Validate Customers Dataset
        """

        logger.info("Validating Customers Dataset...")

        if df.empty:
            raise ValueError("Customer dataset is empty.")

        if df["customer_id"].duplicated().sum() > 0:
            raise ValueError("Duplicate Customer IDs Found.")

        if df["email"].duplicated().sum() > 0:
            logger.warning("Duplicate Email IDs Detected.")

        if df["phone"].duplicated().sum() > 0:
            logger.warning("Duplicate Phone Numbers Detected.")

        if len(df) != self.total_rows:
            raise ValueError(
                f"Expected {self.total_rows:,} rows "
                f"but generated {len(df):,} rows."
            )

        logger.info("Customers Dataset Validation Successful.")


    def save_dataset(self, df: pd.DataFrame):
        """
        Save Customers Dataset
        """

        output_file = self.output_folder / "customers.csv"

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

            "table_name": "customers",

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
            "customers_metadata.json"
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

        print("\n" + "=" * 90)
        print(" Enterprise Gadget Store - Customers Dataset")
        print("=" * 90)

        print(f"Rows Generated      : {len(df):,}")
        print(f"Columns             : {len(df.columns)}")
        print(f"Execution Time      : {execution_time} Seconds")
        print(f"Output File         : data/raw/customers.csv")

        print("=" * 90)

        print("\nSample Records\n")

        print(df.head())

        print("\nCustomer Segment Distribution\n")

        print(df["customer_segment"].value_counts())

        print("\nGender Distribution\n")

        print(df["gender"].value_counts())

        print("\nAccount Status Distribution\n")

        print(df["account_status"].value_counts())

        print("\nPreferred Payment Methods\n")

        print(df["preferred_payment"].value_counts())

        print("\nDevice Type Distribution\n")

        print(df["device_type"].value_counts())

        print("\nReferral Sources\n")

        print(df["referral_source"].value_counts())

        print("\nTop 10 States\n")

        print(df["state"].value_counts().head(10))

        print("\nTop 10 Cities\n")

        print(df["city"].value_counts().head(10))

        print("\nAverage Annual Income")

        print(f"₹ {df['annual_income'].mean():,.2f}")

        print("\nAverage Customer Lifetime Value")

        print(f"₹ {df['lifetime_value'].mean():,.2f}")

        print("\nAverage Loyalty Points")

        print(round(df["loyalty_points"].mean(), 2))

        print("\nMarketing Opt-In")

        print(df["marketing_opt_in"].value_counts())

        print("\nVerified Email Accounts")

        print(df["email_verified"].value_counts())

        print("\nVerified Mobile Numbers")

        print(df["mobile_verified"].value_counts())

        print("\n" + "=" * 90)
        print("Customers Dataset Generated Successfully")
        print("=" * 90)
    def run(self):
        """
        Execute Complete Customer Generation Pipeline
        """

        try:

            logger.info("=" * 70)
            logger.info("Customer Generation Started")
            logger.info("=" * 70)

            df = self.build_customers()

            self.validate_dataset(df)

            output_file = self.save_dataset(df)

            self.generate_metadata(
                df,
                output_file
            )

            self.print_summary(df)

            logger.info("=" * 70)
            logger.info("Customer Generation Completed Successfully")
            logger.info("=" * 70)

        except Exception as error:

            logger.exception(error)

            raise


def main():
    """
    Main Entry Point
    """

    generator = CustomerGenerator()

    generator.run()


if __name__ == "__main__":

    main()
