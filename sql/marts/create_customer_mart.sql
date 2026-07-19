USE enterprise_gadget_store;

-- =========================================================
-- Enterprise Gadget Store
-- Customer Mart
-- =========================================================

DROP TABLE IF EXISTS customer_mart;

CREATE TABLE customer_mart (

    customer_key BIGINT,

    customer_id VARCHAR(30),

    full_name VARCHAR(255),

    gender VARCHAR(20),

    city VARCHAR(100),

    state VARCHAR(100),

    country VARCHAR(100),

    customer_segment VARCHAR(100),

    loyalty_points BIGINT,

    account_status VARCHAR(50),

    total_orders BIGINT,

    total_spent DECIMAL(18,2),

    average_order_value DECIMAL(18,2),

    highest_order DECIMAL(18,2),

    lowest_order DECIMAL(18,2),

    first_order_date DATE,

    last_order_date DATE,

    customer_type VARCHAR(50)

);

-- =========================================================
-- Indexes
-- =========================================================

CREATE INDEX idx_customer_mart_customer
ON customer_mart(customer_id);

CREATE INDEX idx_customer_mart_segment
ON customer_mart(customer_segment);

CREATE INDEX idx_customer_mart_state
ON customer_mart(state);

CREATE INDEX idx_customer_mart_country
ON customer_mart(country);

CREATE INDEX idx_customer_mart_status
ON customer_mart(account_status);

-- =========================================================
-- Validation
-- =========================================================

DESCRIBE customer_mart;

SELECT
'Customer Mart Created Successfully' AS Status;