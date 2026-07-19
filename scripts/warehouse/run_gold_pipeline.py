"""
Gold Layer Pipeline Runner

Executes all Gold Dimension and Fact loaders sequentially.

Usage:
    python -m scripts.warehouse.run_gold_pipeline
"""

import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODULES = [
    "scripts.warehouse.load_dim_category",
    "scripts.warehouse.load_dim_supplier",
    "scripts.warehouse.load_dim_product",
    "scripts.warehouse.load_dim_customer",
    "scripts.warehouse.load_dim_coupon",
    "scripts.warehouse.load_dim_date",
    "scripts.warehouse.load_fact_orders",
    "scripts.warehouse.load_fact_payments",
    "scripts.warehouse.load_fact_shipments",
    "scripts.warehouse.load_fact_inventory",
]


def run_module(module_name: str):
    """Run a Python module and return True if successful."""
    print("=" * 70)
    print(f"Running: {module_name}")
    print("=" * 70)

    start = time.time()

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        cwd=PROJECT_ROOT
    )

    elapsed = time.time() - start

    if result.returncode == 0:
        print(f"SUCCESS : {module_name}")
        print(f"Time    : {elapsed:.2f} sec\n")
        return True

    print(f"FAILED  : {module_name}")
    print(f"Time    : {elapsed:.2f} sec\n")
    return False


def main():

    print("\n")
    print("=" * 70)
    print("ENTERPRISE GADGET STORE")
    print("GOLD LAYER PIPELINE")
    print("=" * 70)

    pipeline_start = time.time()

    success = 0
    failed = 0

    for module in MODULES:

        if run_module(module):
            success += 1
        else:
            failed += 1
            print("\nPipeline Stopped.\n")
            break

    total_time = time.time() - pipeline_start

    print("=" * 70)
    print("PIPELINE SUMMARY")
    print("=" * 70)
    print(f"Successful Modules : {success}")
    print(f"Failed Modules     : {failed}")
    print(f"Execution Time     : {total_time:.2f} seconds")

    if failed == 0:
        print("\nGold Layer Pipeline Completed Successfully.")
    else:
        print("\nGold Layer Pipeline Failed.")

    print("=" * 70)


if __name__ == "__main__":
    main()