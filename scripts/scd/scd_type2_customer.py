"""
=========================================================
Enterprise Gadget Store Data Warehouse
SCD Type 2 - Customer Dimension
=========================================================
Author : Rameshwar Maharnor
=========================================================
"""

import time
import logging
import pandas as pd

from utils.db_connection import engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s"
)

logger = logging.getLogger(__name__)


def run_scd_type2():

    start = time.time()

    logger.info("=" * 70)
    logger.info("SCD TYPE 2 - CUSTOMER DIMENSION")
    logger.info("=" * 70)

    # ---------------------------------------------------
    # Read Silver Customers
    # ---------------------------------------------------

    source_df = pd.read_sql("""

    SELECT
        customer_id,
        first_name,
        last_name,
        full_name,
        gender,
        date_of_birth,
        age,
        email,
        phone,
        address,
        city,
        state,
        country,
        pincode,
        registration_date,
        customer_segment,
        loyalty_points,
        preferred_payment,
        annual_income,
        lifetime_value,
        occupation,
        marital_status,
        email_verified,
        mobile_verified,
        last_login,
        marketing_opt_in,
        referral_source,
        device_type,
        account_status,
        is_active,
        created_date
    FROM silver_customers

    """, engine)

    logger.info(f"Silver Customers : {len(source_df):,}")

    # ---------------------------------------------------
    # Read Current History
    # ---------------------------------------------------

    history_df = pd.read_sql("""

    SELECT customer_id
    FROM dim_customer_history
    WHERE is_current = 1

    """, engine)

    logger.info(f"Current History : {len(history_df):,}")

    # ---------------------------------------------------
    # Find New Customers
    # ---------------------------------------------------

    new_customers = source_df[
        ~source_df["customer_id"].isin(history_df["customer_id"])
    ].copy()

    logger.info(f"New Customers : {len(new_customers):,}")

    if len(new_customers) == 0:

        logger.info("No New Customers Found")

        logger.info(
            f"Execution Time : {time.time()-start:.2f} Seconds"
        )

        return

    # ---------------------------------------------------
    # Add SCD Columns
    # ---------------------------------------------------

    today = pd.Timestamp.today().date()

    new_customers["effective_start_date"] = today

    new_customers["effective_end_date"] = pd.Timestamp("2099-12-31").date()

    new_customers["is_current"] = 1

    new_customers["version_number"] = 1

    # ---------------------------------------------------
    # Load History
    # ---------------------------------------------------

    new_customers.to_sql(

        "dim_customer_history",

        engine,

        if_exists="append",

        index=False,

        chunksize=10000,

        method="multi"

    )

    logger.info(f"Inserted : {len(new_customers):,}")

    logger.info("=" * 70)

    logger.info("STEP 2 COMPLETED SUCCESSFULLY")

    logger.info("=" * 70)

    logger.info(
        f"Execution Time : {time.time()-start:.2f} Seconds"
    )


if __name__ == "__main__":
    run_scd_type2()
