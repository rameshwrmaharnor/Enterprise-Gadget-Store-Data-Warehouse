USE enterprise_gadget_store;

DROP TABLE IF EXISTS dim_product_history;

CREATE TABLE dim_product_history (

    product_history_key BIGINT AUTO_INCREMENT PRIMARY KEY,

    product_id VARCHAR(30),
    sku VARCHAR(100),
    barcode BIGINT,
    product_name VARCHAR(255),
    brand VARCHAR(100),
    category_id VARCHAR(30),
    supplier_id VARCHAR(30),
    color VARCHAR(100),
    material VARCHAR(100),
    warranty_months INT,
    manufacturing_cost DECIMAL(18,2),
    selling_price DECIMAL(18,2),
    profit_margin_percent INT,
    discount_percent INT,
    weight_kg DECIMAL(10,2),
    dimensions VARCHAR(100),
    stock_quantity BIGINT,
    reorder_level BIGINT,
    rating DECIMAL(5,2),
    manufacture_date DATE,
    launch_date DATE,
    product_status VARCHAR(50),
    is_active BOOLEAN,
    created_date DATE,

    effective_start_date DATE,
    effective_end_date DATE,
    is_current BOOLEAN,
    version_number INT

);

SELECT 'Product History Table Created Successfully' AS Status;