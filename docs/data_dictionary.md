# Enterprise Gadget Store Data Warehouse

## Dataset Overview

This project contains approximately **6.9 Million Records**.

---

# 1. Categories

Rows : 120

| Column | Data Type |
|----------|-----------|
| category_id | VARCHAR |
| category_name | VARCHAR |
| department | VARCHAR |
| description | TEXT |
| is_active | BOOLEAN |
| created_date | DATE |

---

# 2. Suppliers

Rows : 8,000

| Column | Data Type |
|----------|-----------|
| supplier_id | VARCHAR |
| supplier_name | VARCHAR |
| contact_person | VARCHAR |
| email | VARCHAR |
| phone | VARCHAR |
| city | VARCHAR |
| state | VARCHAR |
| country | VARCHAR |
| supplier_rating | DECIMAL |
| contract_type | VARCHAR |
| registration_date | DATE |
| is_active | BOOLEAN |

---

# 3. Products

Rows : 80,000

| Column | Data Type |
|----------|-----------|
| product_id | VARCHAR |
| product_name | VARCHAR |
| category_id | VARCHAR |
| supplier_id | VARCHAR |
| brand | VARCHAR |
| model | VARCHAR |
| color | VARCHAR |
| unit_price | DECIMAL |
| manufacturing_cost | DECIMAL |
| stock_quantity | INTEGER |
| warranty_months | INTEGER |
| weight | DECIMAL |
| created_date | DATE |
| is_active | BOOLEAN |

---

# 4. Customers

Rows : 250,000

| Column | Data Type |
|----------|-----------|
| customer_id | VARCHAR |
| first_name | VARCHAR |
| last_name | VARCHAR |
| gender | VARCHAR |
| email | VARCHAR |
| phone | VARCHAR |
| city | VARCHAR |
| state | VARCHAR |
| country | VARCHAR |
| pincode | VARCHAR |
| registration_date | DATE |

---

# 5. Coupons

Rows : 50,000

| Column | Data Type |
|----------|-----------|
| coupon_id | VARCHAR |
| coupon_code | VARCHAR |
| discount_percentage | INTEGER |
| valid_from | DATE |
| valid_to | DATE |
| is_active | BOOLEAN |

---

# 6. Orders

Rows : 2,000,000

| Column | Data Type |
|----------|-----------|
| order_id | VARCHAR |
| customer_id | VARCHAR |
| product_id | VARCHAR |
| coupon_id | VARCHAR |
| quantity | INTEGER |
| unit_price | DECIMAL |
| discount | DECIMAL |
| tax | DECIMAL |
| shipping_cost | DECIMAL |
| total_amount | DECIMAL |
| payment_status | VARCHAR |
| order_status | VARCHAR |
| order_date | DATE |

---

# 7. Payments

Rows : 2,000,000

| Column | Data Type |
|----------|-----------|
| payment_id | VARCHAR |
| order_id | VARCHAR |
| payment_method | VARCHAR |
| payment_date | DATE |
| payment_amount | DECIMAL |
| payment_status | VARCHAR |

---

# 8. Shipments

Rows : 2,000,000

| Column | Data Type |
|----------|-----------|
| shipment_id | VARCHAR |
| order_id | VARCHAR |
| courier_name | VARCHAR |
| tracking_number | VARCHAR |
| shipped_date | DATE |
| delivered_date | DATE |
| shipment_status | VARCHAR |

---

# 9. Inventory

Rows : 500,000

| Column | Data Type |
|----------|-----------|
| inventory_id | VARCHAR |
| product_id | VARCHAR |
| warehouse_name | VARCHAR |
| warehouse_city | VARCHAR |
| available_stock | INTEGER |
| reorder_level | INTEGER |
| last_updated | DATE |