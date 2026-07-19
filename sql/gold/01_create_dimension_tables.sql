-- ==========================================================
-- Enterprise Gadget Store Data Warehouse
-- Gold Layer - Dimension Tables
-- ==========================================================

USE enterprise_gadget_store;

-- ============================================
-- Category Dimension
-- ============================================

DROP TABLE IF EXISTS dim_category;

CREATE TABLE dim_category (

    category_key INT AUTO_INCREMENT PRIMARY KEY,

    category_id VARCHAR(30) NOT NULL UNIQUE,

    category_name VARCHAR(150),

    department VARCHAR(100),

    description TEXT,

    is_active BOOLEAN,

    created_date DATE

);

-- ============================================
-- Supplier Dimension
-- ============================================

DROP TABLE IF EXISTS dim_supplier;

CREATE TABLE dim_supplier (

    supplier_key INT AUTO_INCREMENT PRIMARY KEY,

    supplier_id VARCHAR(30) NOT NULL UNIQUE,

    supplier_name VARCHAR(200),

    company_type VARCHAR(100),

    city VARCHAR(100),

    state VARCHAR(100),

    country VARCHAR(100),

    supplier_rating DECIMAL(3,2),

    is_active BOOLEAN

);

-- ============================================
-- Product Dimension
-- ============================================

DROP TABLE IF EXISTS dim_product;

CREATE TABLE dim_product (

    product_key INT AUTO_INCREMENT PRIMARY KEY,

    product_id VARCHAR(30) NOT NULL UNIQUE,

    sku VARCHAR(50),

    barcode BIGINT,

    product_name VARCHAR(250),

    brand VARCHAR(100),

    category_id VARCHAR(30),

    supplier_id VARCHAR(30),

    color VARCHAR(50),

    material VARCHAR(100),

    selling_price DECIMAL(12,2),

    rating DECIMAL(3,2),

    product_status VARCHAR(50),

    is_active BOOLEAN

);

-- ============================================
-- Customer Dimension
-- ============================================

DROP TABLE IF EXISTS dim_customer;

CREATE TABLE dim_customer (

    customer_key INT AUTO_INCREMENT PRIMARY KEY,

    customer_id VARCHAR(30) NOT NULL UNIQUE,

    full_name VARCHAR(200),

    gender VARCHAR(20),

    city VARCHAR(100),

    state VARCHAR(100),

    country VARCHAR(100),

    customer_segment VARCHAR(50),

    preferred_payment VARCHAR(50),

    occupation VARCHAR(100),

    account_status VARCHAR(50),

    is_active BOOLEAN

);

-- ============================================
-- Coupon Dimension
-- ============================================

DROP TABLE IF EXISTS dim_coupon;

CREATE TABLE dim_coupon (

    coupon_key INT AUTO_INCREMENT PRIMARY KEY,

    coupon_id VARCHAR(30) NOT NULL UNIQUE,

    coupon_code VARCHAR(50),

    coupon_name VARCHAR(150),

    discount_type VARCHAR(50),

    discount_value DECIMAL(10,2),

    coupon_status VARCHAR(50),

    is_active BOOLEAN

);