from pathlib import Path

# ==========================================================
# Enterprise Gadget Store Data Warehouse
# Project Scaffolding Script
# Author : Rameshwar Maharnor
# ==========================================================

PROJECT_ROOT = Path.cwd()

FILES = [

    # Root Files
    "README.md",
    "requirements.txt",
    ".gitignore",
    ".env",
    "docker-compose.yml",
    "LICENSE",

    # Config
    "config/config.yaml",

    # Utils
    "utils/db_connection.py",
    "utils/config.py",
    "utils/logger.py",

    # Documentation
    "docs/architecture.md",
    "docs/data_dictionary.md",
    "docs/project_flow.md",

    # Tests
    "tests/test_connection.py",

    # -----------------------
    # Generator Scripts
    # -----------------------

    "scripts/generators/generate_categories.py",
    "scripts/generators/generate_suppliers.py",
    "scripts/generators/generate_products.py",
    "scripts/generators/generate_customers.py",
    "scripts/generators/generate_coupons.py",
    "scripts/generators/generate_orders.py",
    "scripts/generators/generate_payments.py",
    "scripts/generators/generate_shipments.py",
    "scripts/generators/generate_inventory.py",

    # -----------------------
    # Bronze
    # -----------------------

    "scripts/ingestion/load_bronze.py",

    # -----------------------
    # Validation
    # -----------------------

    "scripts/validations/validate_categories.py",
    "scripts/validations/validate_suppliers.py",
    "scripts/validations/validate_products.py",
    "scripts/validations/validate_customers.py",
    "scripts/validations/validate_orders.py",
    "scripts/validations/validate_payments.py",
    "scripts/validations/validate_shipments.py",
    "scripts/validations/validate_inventory.py",

    # -----------------------
    # Transformations
    # -----------------------

    "scripts/transformations/transform_categories.py",
    "scripts/transformations/transform_suppliers.py",
    "scripts/transformations/transform_products.py",
    "scripts/transformations/transform_customers.py",
    "scripts/transformations/transform_orders.py",
    "scripts/transformations/transform_payments.py",
    "scripts/transformations/transform_shipments.py",
    "scripts/transformations/transform_inventory.py",

    # -----------------------
    # Warehouse
    # -----------------------

    "scripts/warehouse/load_dim_category.py",
    "scripts/warehouse/load_dim_supplier.py",
    "scripts/warehouse/load_dim_product.py",
    "scripts/warehouse/load_dim_customer.py",
    "scripts/warehouse/load_dim_payment.py",
    "scripts/warehouse/load_dim_date.py",
    "scripts/warehouse/load_fact_sales.py",
    "scripts/warehouse/load_fact_inventory.py",

    # -----------------------
    # Marts
    # -----------------------

    "scripts/marts/load_sales_mart.py",
    "scripts/marts/load_customer_mart.py",
    "scripts/marts/load_supplier_mart.py",
    "scripts/marts/load_inventory_mart.py",
    "scripts/marts/load_payment_mart.py",

    # -----------------------
    # Orchestration
    # -----------------------

    "scripts/orchestration/run_pipeline.py",

    # -----------------------
    # SQL
    # -----------------------

    "sql/bronze/create_bronze_tables.sql",
    "sql/silver/create_silver_tables.sql",
    "sql/gold/create_gold_tables.sql",

    "sql/marts/create_sales_mart.sql",
    "sql/marts/create_customer_mart.sql",
    "sql/marts/create_supplier_mart.sql",
    "sql/marts/create_inventory_mart.sql",
    "sql/marts/create_payment_mart.sql",

    # Airflow

    ".github/workflows/ci.yml"
]

HEADER = '''"""
=========================================================
Enterprise Gadget Store Data Warehouse

Author : Rameshwar Maharnor

=========================================================
"""

'''

for file in FILES:

    path = PROJECT_ROOT / file

    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():

        path.touch()

        if path.suffix == ".py":
            path.write_text(HEADER)

print("=" * 60)
print("Enterprise Project Files Created Successfully")
print("=" * 60)
print("Total Files :", len(FILES))
print("=" * 60)