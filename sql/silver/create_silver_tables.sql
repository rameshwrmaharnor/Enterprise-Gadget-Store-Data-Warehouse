USE enterprise_gadget_store;

-- =====================================================
-- Enterprise Gadget Store
-- Silver Layer Tables
-- =====================================================

DROP TABLE IF EXISTS silver_categories;
DROP TABLE IF EXISTS silver_suppliers;
DROP TABLE IF EXISTS silver_products;
DROP TABLE IF EXISTS silver_customers;
DROP TABLE IF EXISTS silver_coupons;
DROP TABLE IF EXISTS silver_orders;
DROP TABLE IF EXISTS silver_payments;
DROP TABLE IF EXISTS silver_shipments;
DROP TABLE IF EXISTS silver_inventory;

-- =====================================================
-- Categories
-- =====================================================

CREATE TABLE silver_categories
LIKE bronze_categories;

ALTER TABLE silver_categories
COMMENT='Cleaned Category Data';

-- =====================================================
-- Suppliers
-- =====================================================

CREATE TABLE silver_suppliers
LIKE bronze_suppliers;

ALTER TABLE silver_suppliers
COMMENT='Cleaned Supplier Data';

-- =====================================================
-- Products
-- =====================================================

CREATE TABLE silver_products
LIKE bronze_products;

ALTER TABLE silver_products
COMMENT='Cleaned Product Data';

-- =====================================================
-- Customers
-- =====================================================

CREATE TABLE silver_customers
LIKE bronze_customers;

ALTER TABLE silver_customers
COMMENT='Cleaned Customer Data';

-- =====================================================
-- Coupons
-- =====================================================

CREATE TABLE silver_coupons
LIKE bronze_coupons;

ALTER TABLE silver_coupons
COMMENT='Cleaned Coupon Data';

-- =====================================================
-- Orders
-- =====================================================

CREATE TABLE silver_orders
LIKE bronze_orders;

ALTER TABLE silver_orders
COMMENT='Cleaned Order Data';

-- =====================================================
-- Payments
-- =====================================================

CREATE TABLE silver_payments
LIKE bronze_payments;

ALTER TABLE silver_payments
COMMENT='Cleaned Payment Data';

-- =====================================================
-- Shipments
-- =====================================================

CREATE TABLE silver_shipments
LIKE bronze_shipments;

ALTER TABLE silver_shipments
COMMENT='Cleaned Shipment Data';

-- =====================================================
-- Inventory
-- =====================================================

CREATE TABLE silver_inventory
LIKE bronze_inventory;

ALTER TABLE silver_inventory
COMMENT='Cleaned Inventory Data';

-- =====================================================
-- Validation
-- =====================================================

SHOW TABLES LIKE 'silver%';

SELECT
'Silver Layer Tables Created Successfully' AS Status;