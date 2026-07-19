"""
=========================================================
Enterprise Gadget Store Data Warehouse
Incremental Pipeline Runner

Author : Rameshwar Maharnor
=========================================================
"""

import time
import subprocess

PIPELINES = [

    "scripts.incremental.incremental_orders",

    "scripts.incremental.incremental_payments",

    "scripts.incremental.incremental_shipments",

    "scripts.incremental.incremental_inventory"

]


def run_pipeline():

    start = time.time()

    success = 0

    failed = 0

    print("=" * 70)
    print("ENTERPRISE GADGET STORE")
    print("INCREMENTAL PIPELINE")
    print("=" * 70)

    for module in PIPELINES:

        print("=" * 70)
        print(f"Running : {module}")
        print("=" * 70)

        module_start = time.time()

        result = subprocess.run(

            ["python", "-m", module]

        )

        elapsed = time.time() - module_start

        if result.returncode == 0:

            success += 1

            print(f"SUCCESS : {module}")

        else:

            failed += 1

            print(f"FAILED : {module}")

        print(f"Time : {elapsed:.2f} Seconds\n")

    print("=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)
    print(f"Successful Modules : {success}")
    print(f"Failed Modules     : {failed}")
    print(f"Execution Time     : {time.time()-start:.2f} Seconds")
    print("=" * 70)

    if failed == 0:

        print("Incremental Pipeline Completed Successfully.")

    else:

        print("Incremental Pipeline Completed With Errors.")

    print("=" * 70)


if __name__ == "__main__":

    run_pipeline()
