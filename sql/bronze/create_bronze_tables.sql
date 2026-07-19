USE enterprise_gadget_store;

-- =====================================================
-- ENTERPRISE GADGET STORE
-- Bronze Layer Tables
-- =====================================================

DROP TABLE IF EXISTS bronze_categories;
DROP TABLE IF EXISTS bronze_suppliers;
DROP TABLE IF EXISTS bronze_products;
DROP TABLE IF EXISTS bronze_customers;
DROP TABLE IF EXISTS bronze_coupons;
DROP TABLE IF EXISTS bronze_orders;
DROP TABLE IF EXISTS bronze_payments;
DROP TABLE IF EXISTS bronze_shipments;
DROP TABLE IF EXISTS bronze_inventory;

-- =====================================================
-- Categories
-- =====================================================

CREATE TABLE bronze_categories
AS
SELECT *
FROM enterprise_gadget_store_raw.categories
WHERE 1=0;

-- =====================================================
-- Suppliers
-- =====================================================

CREATE TABLE bronze_suppliers
AS
SELECT *
FROM enterprise_gadget_store_raw.suppliers
WHERE 1=0;

-- =====================================================
-- Products
-- =====================================================

CREATE TABLE bronze_products
AS
SELECT *
FROM enterprise_gadget_store_raw.products
WHERE 1=0;

-- =====================================================
-- Customers
-- =====================================================

CREATE TABLE bronze_customers
AS
SELECT *
FROM enterprise_gadget_store_raw.customers
WHERE 1=0;

-- =====================================================
-- Coupons
-- =====================================================

CREATE TABLE bronze_coupons
AS
SELECT *
FROM enterprise_gadget_store_raw.coupons
WHERE 1=0;

-- =====================================================
-- Orders
-- =====================================================

CREATE TABLE bronze_orders
AS
SELECT *
FROM enterprise_gadget_store_raw.orders
WHERE 1=0;

-- =====================================================
-- Payments
-- =====================================================

CREATE TABLE bronze_payments
AS
SELECT *
FROM enterprise_gadget_store_raw.payments
WHERE 1=0;

-- =====================================================
-- Shipments
-- =====================================================

CREATE TABLE bronze_shipments
AS
SELECT *
FROM enterprise_gadget_store_raw.shipments
WHERE 1=0;

-- =====================================================
-- Inventory
-- =====================================================

CREATE TABLE bronze_inventory
AS
SELECT *
FROM enterprise_gadget_store_raw.inventory
WHERE 1=0;

-- =====================================================
-- Validation
-- =====================================================

SHOW TABLES LIKE 'bronze%';

SELECT
'Bronze Layer Tables Created Successfully' AS Status;