"""
=========================================================
Enterprise Gadget Store Data Warehouse
Date Dimension Loader

Author : Rameshwar Maharnor
=========================================================
"""

import pandas as pd

from scripts.warehouse.dimension_loader import DimensionLoader


def generate_date_dimension():

    # Generate dates from 2020 to 2035

    dates = pd.date_range(
        start="2020-01-01",
        end="2035-12-31",
        freq="D"
    )

    df = pd.DataFrame()

    df["date_key"] = dates.strftime("%Y%m%d").astype(int)

    df["full_date"] = dates

    df["day"] = dates.day

    df["month"] = dates.month

    df["month_name"] = dates.month_name()

    df["quarter"] = dates.quarter

    df["year"] = dates.year

    df["week"] = dates.isocalendar().week.astype(int)

    df["weekday"] = dates.day_name()

    df["is_weekend"] = dates.weekday >= 5

    return df


def main():

    from utils.db_connection import engine

    df = generate_date_dimension()

    df.to_sql(

        "dim_date",

        engine,

        if_exists="replace",

        index=False

    )

    print("dim_date Loaded Successfully")


if __name__ == "__main__":
    main()
