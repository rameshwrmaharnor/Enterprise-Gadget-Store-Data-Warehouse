"""
=========================================================
Enterprise Gadget Store Data Warehouse
Master Pipeline

Author : Rameshwar Maharnor
=========================================================
"""

import subprocess
import time

MODULES = [

    # Gold Layer

    "scripts.warehouse.run_gold_pipeline",

    # SCD

    "scripts.scd.scd_type1_customer",

    "scripts.scd.scd_type2_customer",

    "scripts.scd.scd_type1_product",

    "scripts.scd.scd_type2_product",

    # Incremental

    "scripts.incremental.run_incremental_pipeline",

    # Data Marts

    "scripts.marts.run_marts_pipeline"

]


def run():

    start = time.time()

    success = 0

    failed = 0

    print("="*70)
    print("ENTERPRISE GADGET STORE")
    print("MASTER ETL PIPELINE")
    print("="*70)

    for module in MODULES:

        print("="*70)
        print(f"Running : {module}")
        print("="*70)

        t = time.time()

        result = subprocess.run(

            ["python", "-m", module]

        )

        elapsed = time.time()-t

        if result.returncode == 0:

            success += 1

            print("SUCCESS")

        else:

            failed += 1

            print("FAILED")

        print(f"Execution Time : {elapsed:.2f} Seconds\n")

    print("="*70)
    print("PROJECT SUMMARY")
    print("="*70)

    print(f"Successful Modules : {success}")

    print(f"Failed Modules : {failed}")

    print(f"Total Execution Time : {time.time()-start:.2f} Seconds")

    print("="*70)

    if failed == 0:

        print("PROJECT COMPLETED SUCCESSFULLY")

    else:

        print("PROJECT COMPLETED WITH ERRORS")

    print("="*70)


if __name__ == "__main__":

    run()
