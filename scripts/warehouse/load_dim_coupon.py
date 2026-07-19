"""
=========================================================
Enterprise Gadget Store Data Warehouse
Coupon Dimension Loader

Author : Rameshwar Maharnor
=========================================================
"""

from scripts.warehouse.dimension_loader import DimensionLoader


def main():

    loader = DimensionLoader(

        source_table="silver_coupons",

        target_table="dim_coupon",

        key_column="coupon_id",

        columns=[

            "coupon_id",
            "coupon_code",
            "coupon_name",
            "discount_type",
            "discount_value",
            "minimum_order_amount",
            "maximum_discount",
            "applicable_segment",
            "valid_from",
            "valid_to",
            "usage_limit",
            "used_count",
            "coupon_status",
            "is_active",
            "created_date"

        ]

    )

    loader.run()


if __name__ == "__main__":

    main()