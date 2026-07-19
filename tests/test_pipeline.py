"""
=========================================================
Enterprise Gadget Store Data Warehouse
Pipeline Test

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
    "dim_coupon",
    "dim_date",

    "fact_orders",
    "fact_payments",
    "fact_shipments",
    "fact_inventory"

]


def test_pipeline():

    print("=" * 70)
    print("PIPELINE TEST")
    print("=" * 70)

    passed = 0

    failed = 0

    for table in TABLES:

        try:

            count = pd.read_sql(

                f"SELECT COUNT(*) total FROM {table}",

                engine

            ).iloc[0]["total"]

            print(f"{table:<25} {count:,}")

            passed += 1

        except Exception:

            print(f"{table:<25} FAILED")

            failed += 1

    print("=" * 70)

    print(f"Passed : {passed}")

    print(f"Failed : {failed}")

    print("=" * 70)


if __name__ == "__main__":

    test_pipeline()
