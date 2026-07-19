USE enterprise_gadget_store;

-- =========================================================
-- Enterprise Gadget Store
-- Inventory Mart
-- =========================================================

DROP TABLE IF EXISTS inventory_mart;

CREATE TABLE inventory_mart (

    inventory_id VARCHAR(30),

    product_key BIGINT,

    product_id VARCHAR(30),

    product_name VARCHAR(255),

    brand VARCHAR(100),

    category_name VARCHAR(100),

    warehouse VARCHAR(100),

    stock_quantity BIGINT,

    available_stock BIGINT,

    reserved_stock BIGINT,

    damaged_stock BIGINT,

    reorder_level BIGINT,

    inventory_value DECIMAL(18,2),

    selling_price DECIMAL(18,2),

    manufacturing_cost DECIMAL(18,2),

    rating DECIMAL(5,2),

    inventory_status VARCHAR(50),

    stock_health VARCHAR(50),

    inventory_value_band VARCHAR(50),

    stock_utilization_percent DECIMAL(10,2)

);

-- =========================================================
-- Performance Indexes
-- =========================================================

CREATE INDEX idx_inventory_inventory
ON inventory_mart(inventory_id);

CREATE INDEX idx_inventory_product
ON inventory_mart(product_id);

CREATE INDEX idx_inventory_brand
ON inventory_mart(brand);

CREATE INDEX idx_inventory_category
ON inventory_mart(category_name);

CREATE INDEX idx_inventory_warehouse
ON inventory_mart(warehouse);

CREATE INDEX idx_inventory_status
ON inventory_mart(inventory_status);

CREATE INDEX idx_inventory_health
ON inventory_mart(stock_health);

-- =========================================================
-- Validation
-- =========================================================

DESCRIBE inventory_mart;

SELECT
'Inventory Mart Created Successfully' AS Status;