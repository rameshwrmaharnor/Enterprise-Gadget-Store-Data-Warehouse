"""
=========================================================
Enterprise Gadget Store Data Warehouse
Data Quality Test

Author : Rameshwar Maharnor
=========================================================
"""

import pandas as pd
from utils.db_connection import engine


TABLES = [

    "dim_category",
    "dim_supplier",
    "dim_product",
    "dim_customer",
    "fact_orders",
    "fact_payments",
    "fact_shipments",
    "fact_inventory"

]


def test_quality():

    print("=" * 70)
    print("DATA QUALITY TEST")
    print("=" * 70)

    for table in TABLES:

        df = pd.read_sql(

            f"SELECT * FROM {table}",

            engine

        )

        print("=" * 70)

        print(table)

        print("=" * 70)

        print("Rows :", len(df))

        print("Columns :", len(df.columns))

        print("Null Values")

        print(df.isnull().sum())

        print()

    print("=" * 70)

    print("DATA QUALITY TEST COMPLETED")

    print("=" * 70)


if __name__ == "__main__":

    test_quality()
