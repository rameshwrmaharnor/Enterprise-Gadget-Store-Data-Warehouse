"""
=========================================================
Enterprise Gadget Store Data Warehouse
Database Connection Test

Author : Rameshwar Maharnor
=========================================================
"""

from sqlalchemy import text
from utils.db_connection import engine


def test_database_connection():

    print("=" * 70)
    print("DATABASE CONNECTION TEST")
    print("=" * 70)

    try:

        with engine.connect() as conn:

            result = conn.execute(text("SELECT 1"))

            print("Database Connected Successfully")

            print("Result :", result.scalar())

        print("=" * 70)
        print("TEST PASSED")
        print("=" * 70)

    except Exception as e:

        print("TEST FAILED")

        print(e)


if __name__ == "__main__":

    test_database_connection()
