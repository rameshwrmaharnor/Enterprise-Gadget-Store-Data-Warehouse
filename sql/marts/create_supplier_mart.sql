USE enterprise_gadget_store;

-- =========================================================
-- Enterprise Gadget Store
-- Supplier Mart
-- =========================================================

DROP TABLE IF EXISTS supplier_mart;

CREATE TABLE supplier_mart (

    supplier_key BIGINT,

    supplier_id VARCHAR(30),

    supplier_name VARCHAR(255),

    company_type VARCHAR(100),

    contact_person VARCHAR(255),

    city VARCHAR(100),

    state VARCHAR(100),

    country VARCHAR(100),

    supplier_rating DECIMAL(5,2),

    payment_terms VARCHAR(100),

    contract_type VARCHAR(100),

    credit_limit DECIMAL(18,2),

    is_active BOOLEAN,

    total_products BIGINT,

    avg_price DECIMAL(18,2),

    total_stock BIGINT,

    inventory_cost DECIMAL(18,2),

    supplier_category VARCHAR(50),

    supplier_grade VARCHAR(20)

);

-- =========================================================
-- Performance Indexes
-- =========================================================

CREATE INDEX idx_supplier_mart_supplier
ON supplier_mart(supplier_id);

CREATE INDEX idx_supplier_mart_name
ON supplier_mart(supplier_name);

CREATE INDEX idx_supplier_mart_city
ON supplier_mart(city);

CREATE INDEX idx_supplier_mart_state
ON supplier_mart(state);

CREATE INDEX idx_supplier_mart_country
ON supplier_mart(country);

CREATE INDEX idx_supplier_mart_category
ON supplier_mart(supplier_category);

CREATE INDEX idx_supplier_mart_grade
ON supplier_mart(supplier_grade);

-- =========================================================
-- Validation
-- =========================================================

DESCRIBE supplier_mart;

SELECT
'Supplier Mart Created Successfully' AS Status;