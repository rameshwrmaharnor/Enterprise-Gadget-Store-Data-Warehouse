"""
=========================================================
Enterprise Gadget Store Data Warehouse
Run All Data Marts

Author : Rameshwar Maharnor
=========================================================
"""

import subprocess
import time

PIPELINES = [

    "scripts.marts.load_sales_mart",

    "scripts.marts.load_customer_mart",

    "scripts.marts.load_inventory_mart",

    "scripts.marts.load_payment_mart",

    "scripts.marts.load_supplier_mart"

]


def run_pipeline():

    start = time.time()

    success = 0

    failed = 0

    print("=" * 70)
    print("ENTERPRISE GADGET STORE")
    print("DATA MART PIPELINE")
    print("=" * 70)

    for pipeline in PIPELINES:

        print("=" * 70)
        print(f"Running : {pipeline}")
        print("=" * 70)

        module_start = time.time()

        result = subprocess.run(

            ["python", "-m", pipeline]

        )

        elapsed = time.time() - module_start

        if result.returncode == 0:

            success += 1

            print(f"SUCCESS : {pipeline}")

        else:

            failed += 1

            print(f"FAILED : {pipeline}")

        print(f"Execution Time : {elapsed:.2f} Seconds\n")

    print("=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)
    print(f"Successful Modules : {success}")
    print(f"Failed Modules     : {failed}")
    print(f"Total Time         : {time.time()-start:.2f} Seconds")
    print("=" * 70)

    if failed == 0:

        print("All Data Marts Created Successfully.")

    else:

        print("Pipeline Completed With Errors.")

    print("=" * 70)


if __name__ == "__main__":

    run_pipeline()
