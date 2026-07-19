"""
=========================================================
Enterprise Gadget Store Data Warehouse
Supplier Dimension Loader

Author : Rameshwar Maharnor
Version : 1.0.0
=========================================================
"""

from scripts.warehouse.dimension_loader import DimensionLoader


def main():

    loader = DimensionLoader(

        source_table="silver_suppliers",

        target_table="dim_supplier",

        key_column="supplier_id",

        columns=[

            "supplier_id",
            "supplier_name",
            "company_type",
            "contact_person",
            "email",
            "phone",
            "gst_number",
            "pan_number",
            "city",
            "state",
            "country",
            "supplier_rating",
            "payment_terms",
            "contract_type",
            "credit_limit",
            "registration_date",
            "is_active"

        ]

    )

    loader.run()


if __name__ == "__main__":

    main()
