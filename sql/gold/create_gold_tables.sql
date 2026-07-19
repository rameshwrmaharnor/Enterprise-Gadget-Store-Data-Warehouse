USE enterprise_gadget_store;

-- =========================================================
-- Enterprise Gadget Store Data Warehouse
-- Gold Layer Tables
-- =========================================================

-- =========================================================
-- Drop Existing Tables
-- =========================================================

DROP TABLE IF EXISTS fact_inventory;
DROP TABLE IF EXISTS fact_shipments;
DROP TABLE IF EXISTS fact_payments;
DROP TABLE IF EXISTS fact_orders;

DROP TABLE IF EXISTS dim_coupon;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_supplier;
DROP TABLE IF EXISTS dim_category;
DROP TABLE IF EXISTS dim_date;

-- =========================================================
-- Dimension Tables
-- =========================================================

CREATE TABLE dim_category
LIKE silver_categories;

ALTER TABLE dim_category
COMMENT='Category Dimension';


CREATE TABLE dim_supplier
LIKE silver_suppliers;

ALTER TABLE dim_supplier
COMMENT='Supplier Dimension';


CREATE TABLE dim_product
LIKE silver_products;

ALTER TABLE dim_product
COMMENT='Product Dimension';


CREATE TABLE dim_customer
LIKE silver_customers;

ALTER TABLE dim_customer
COMMENT='Customer Dimension';


CREATE TABLE dim_coupon
LIKE silver_coupons;

ALTER TABLE dim_coupon
COMMENT='Coupon Dimension';


-- =========================================================
-- Date Dimension
-- =========================================================

CREATE TABLE dim_date (

    date_key INT PRIMARY KEY,

    full_date DATE,

    day INT,

    month INT,

    month_name VARCHAR(20),

    quarter INT,

    year INT,

    week INT,

    weekday VARCHAR(20),

    is_weekend BOOLEAN

);

-- =========================================================
-- Fact Tables
-- =========================================================

CREATE TABLE fact_orders
LIKE silver_orders;

ALTER TABLE fact_orders
COMMENT='Orders Fact';


CREATE TABLE fact_payments
LIKE silver_payments;

ALTER TABLE fact_payments
COMMENT='Payments Fact';


CREATE TABLE fact_shipments
LIKE silver_shipments;

ALTER TABLE fact_shipments
COMMENT='Shipments Fact';


CREATE TABLE fact_inventory
LIKE silver_inventory;

ALTER TABLE fact_inventory
COMMENT='Inventory Fact';

-- =========================================================
-- Performance Indexes
-- =========================================================

CREATE INDEX idx_orders_order
ON fact_orders(order_id);

CREATE INDEX idx_orders_customer
ON fact_orders(customer_key);

CREATE INDEX idx_orders_date
ON fact_orders(date_key);

CREATE INDEX idx_payments_order
ON fact_payments(order_id);

CREATE INDEX idx_shipments_order
ON fact_shipments(order_id);

CREATE INDEX idx_inventory_product
ON fact_inventory(product_key);

CREATE INDEX idx_customer_customer
ON dim_customer(customer_id);

CREATE INDEX idx_product_product
ON dim_product(product_id);

CREATE INDEX idx_supplier_supplier
ON dim_supplier(supplier_id);

-- =========================================================
-- Validation
-- =========================================================

SHOW TABLES LIKE 'dim%';

SHOW TABLES LIKE 'fact%';

SELECT
'Gold Layer Tables Created Successfully' AS Status;