USE enterprise_gadget_store;

-- =========================================================
-- Enterprise Gadget Store
-- Payment Mart
-- =========================================================

DROP TABLE IF EXISTS payment_mart;

CREATE TABLE payment_mart (

    payment_id VARCHAR(30),

    order_id VARCHAR(30),

    date_key INT,

    transaction_id VARCHAR(100),

    payment_gateway VARCHAR(100),

    payment_method VARCHAR(50),

    payment_amount DECIMAL(18,2),

    payment_status VARCHAR(50),

    payment_date DATETIME,

    bank_name VARCHAR(100),

    card_type VARCHAR(50),

    currency VARCHAR(20),

    customer_key BIGINT,

    customer_segment VARCHAR(100),

    state VARCHAR(100),

    country VARCHAR(100),

    payment_success BOOLEAN,

    payment_failure BOOLEAN,

    payment_band VARCHAR(30)

);

-- =========================================================
-- Performance Indexes
-- =========================================================

CREATE INDEX idx_payment_payment
ON payment_mart(payment_id);

CREATE INDEX idx_payment_order
ON payment_mart(order_id);

CREATE INDEX idx_payment_customer
ON payment_mart(customer_key);

CREATE INDEX idx_payment_gateway
ON payment_mart(payment_gateway);

CREATE INDEX idx_payment_method
ON payment_mart(payment_method);

CREATE INDEX idx_payment_status
ON payment_mart(payment_status);

CREATE INDEX idx_payment_date
ON payment_mart(payment_date);

-- =========================================================
-- Validation
-- =========================================================

DESCRIBE payment_mart;

SELECT
'Payment Mart Created Successfully' AS Status;