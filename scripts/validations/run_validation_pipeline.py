"""
=========================================================
Enterprise Gadget Store Data Warehouse
Validation Pipeline

Author : Rameshwar Maharnor
=========================================================
"""

import subprocess
import time

VALIDATIONS = [

    "scripts.validations.validate_categories",

    "scripts.validations.validate_suppliers",

    "scripts.validations.validate_products",

    "scripts.validations.validate_customers",

    "scripts.validations.validate_orders",

    "scripts.validations.validate_payments",

    "scripts.validations.validate_shipments",

    "scripts.validations.validate_inventory"

]


def run_validation_pipeline():

    start = time.time()

    success = 0

    failed = 0

    print("=" * 70)
    print("ENTERPRISE GADGET STORE")
    print("VALIDATION PIPELINE")
    print("=" * 70)

    for validation in VALIDATIONS:

        print("=" * 70)
        print(f"Running : {validation}")
        print("=" * 70)

        module_start = time.time()

        result = subprocess.run(

            ["python", "-m", validation]

        )

        elapsed = time.time() - module_start

        if result.returncode == 0:

            success += 1

            print(f"SUCCESS : {validation}")

        else:

            failed += 1

            print(f"FAILED : {validation}")

        print(f"Execution Time : {elapsed:.2f} Seconds")
        print()

    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    print(f"Successful Validations : {success}")

    print(f"Failed Validations     : {failed}")

    print(f"Total Execution Time   : {time.time()-start:.2f} Seconds")

    print("=" * 70)

    if failed == 0:

        print("ALL VALIDATIONS PASSED SUCCESSFULLY")

    else:

        print("VALIDATION COMPLETED WITH ERRORS")

    print("=" * 70)


if __name__ == "__main__":

    run_validation_pipeline()
