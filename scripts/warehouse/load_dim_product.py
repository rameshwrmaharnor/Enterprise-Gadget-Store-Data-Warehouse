"""
=========================================================
Enterprise Gadget Store Data Warehouse
Product Dimension Loader

Author : Rameshwar Maharnor
=========================================================
"""

from scripts.warehouse.dimension_loader import DimensionLoader


def main():

    loader = DimensionLoader(

        source_table="silver_products",

        target_table="dim_product",

        key_column="product_id",

        columns=[

            "product_id",

            "sku",

            "barcode",

            "product_name",

            "brand",

            "category_id",

            "supplier_id",

            "color",

            "material",

            "warranty_months",

            "manufacturing_cost",

            "selling_price",

            "profit_margin_percent",

            "discount_percent",

            "weight_kg",

            "dimensions",

            "stock_quantity",

            "reorder_level",

            "rating",

            "manufacture_date",

            "launch_date",

            "product_status",

            "is_active",

            "created_date"

        ]

    )

    loader.run()


if __name__ == "__main__":

    main()
