USE enterprise_gadget_store;

-- ==========================================================
-- Enterprise Gadget Store Data Warehouse
-- Gold Layer Analytical Views
-- ==========================================================

-- ==========================================================
-- 1. SALES SUMMARY VIEW
-- ==========================================================

DROP VIEW IF EXISTS vw_sales_summary;

CREATE VIEW vw_sales_summary AS
SELECT
    d.year,
    d.quarter,
    d.month_name,
    COUNT(f.order_id) AS total_orders,
    ROUND(SUM(f.subtotal),2) AS subtotal,
    ROUND(SUM(f.discount_amount),2) AS total_discount,
    ROUND(SUM(f.tax_amount),2) AS total_tax,
    ROUND(SUM(f.shipping_charge),2) AS total_shipping,
    ROUND(SUM(f.total_amount),2) AS total_sales,
    ROUND(AVG(f.total_amount),2) AS average_order_value
FROM fact_orders f
JOIN dim_date d
ON f.date_key = d.date_key
GROUP BY
d.year,
d.quarter,
d.month_name;

-- ==========================================================
-- 2. CUSTOMER SUMMARY VIEW
-- ==========================================================

DROP VIEW IF EXISTS vw_customer_summary;

CREATE VIEW vw_customer_summary AS
SELECT

customer_segment,

state,

country,

COUNT(*) AS total_customers,

SUM(loyalty_points) AS total_loyalty_points,

AVG(loyalty_points) AS average_loyalty_points

FROM dim_customer

GROUP BY

customer_segment,

state,

country;

-- ==========================================================
-- 3. PAYMENT SUMMARY VIEW
-- ==========================================================

DROP VIEW IF EXISTS vw_payment_summary;

CREATE VIEW vw_payment_summary AS
SELECT

payment_gateway,

payment_method,

payment_status,

COUNT(*) AS total_transactions,

ROUND(SUM(payment_amount),2) AS total_payment,

ROUND(AVG(payment_amount),2) AS average_payment

FROM fact_payments

GROUP BY

payment_gateway,

payment_method,

payment_status;

-- ==========================================================
-- 4. SHIPMENT SUMMARY VIEW
-- ==========================================================

DROP VIEW IF EXISTS vw_shipment_summary;

CREATE VIEW vw_shipment_summary AS
SELECT

courier_partner,

warehouse,

shipping_status,

COUNT(*) AS total_shipments,

ROUND(SUM(shipping_cost),2) AS total_shipping_cost,

ROUND(AVG(shipping_cost),2) AS average_shipping_cost

FROM fact_shipments

GROUP BY

courier_partner,

warehouse,

shipping_status;

-- ==========================================================
-- 5. INVENTORY SUMMARY VIEW
-- ==========================================================

DROP VIEW IF EXISTS vw_inventory_summary;

CREATE VIEW vw_inventory_summary AS
SELECT

warehouse,

reorder_status,

COUNT(*) AS total_products,

SUM(stock_quantity) AS stock_quantity,

SUM(available_stock) AS available_stock,

SUM(reserved_stock) AS reserved_stock,

SUM(damaged_stock) AS damaged_stock,

ROUND(SUM(inventory_value),2) AS inventory_value

FROM fact_inventory

GROUP BY

warehouse,

reorder_status;

-- ==========================================================
-- 6. PRODUCT SUMMARY VIEW
-- ==========================================================

DROP VIEW IF EXISTS vw_product_summary;

CREATE VIEW vw_product_summary AS
SELECT

brand,

product_status,

COUNT(*) AS total_products,

ROUND(AVG(selling_price),2) AS average_price,

ROUND(AVG(rating),2) AS average_rating,

SUM(stock_quantity) AS total_stock

FROM dim_product

GROUP BY

brand,

product_status;

-- ==========================================================
-- 7. SUPPLIER SUMMARY VIEW
-- ==========================================================

DROP VIEW IF EXISTS vw_supplier_summary;

CREATE VIEW vw_supplier_summary AS
SELECT

country,

state,

company_type,

COUNT(*) AS total_suppliers,

ROUND(AVG(supplier_rating),2) AS average_rating,

SUM(credit_limit) AS total_credit_limit

FROM dim_supplier

GROUP BY

country,

state,

company_type;

-- ==========================================================
-- VERIFY ALL VIEWS
-- ==========================================================

SHOW FULL TABLES
WHERE TABLE_TYPE='VIEW';

SELECT 'Gold Layer Views Created Successfully' AS Status;