"""
=========================================================
Enterprise Gadget Store Data Warehouse
Load Gold Dimension - Category
=========================================================
"""

import time
import pandas as pd

from utils.db_connection import engine
from utils.logger import logger


class CategoryDimensionLoader:

    def __init__(self):

        self.start = time.time()

    def run(self):

        logger.info("=" * 70)
        logger.info("Loading Category Dimension")
        logger.info("=" * 70)

        df = pd.read_sql("""

            SELECT

                category_id,
                category_name,
                department,
                description,
                is_active,
                created_date

            FROM silver_categories

        """, engine)

        logger.info(f"Rows Read : {len(df):,}")

        df["created_date"] = pd.to_datetime(
            df["created_date"],
            errors="coerce"
        )

        df.to_sql(

            "dim_category",

            engine,

            if_exists="append",

            index=False,

            method="multi",

            chunksize=5000

        )

        logger.info("Category Dimension Loaded Successfully")

        logger.info(
            f"Execution Time : "
            f"{round(time.time()-self.start, 2)} sec"
        )


def main():

    CategoryDimensionLoader().run()


if __name__ == "__main__":

    main()
