USE enterprise_gadget_store;

DROP TABLE IF EXISTS dim_customer_history;

CREATE TABLE dim_customer_history (

    customer_history_key BIGINT AUTO_INCREMENT PRIMARY KEY,

    customer_id VARCHAR(30) NOT NULL,

    first_name VARCHAR(100),

    last_name VARCHAR(100),

    full_name VARCHAR(250),

    gender VARCHAR(20),

    date_of_birth DATE,

    age INT,

    email VARCHAR(255),

    phone VARCHAR(30),

    address TEXT,

    city VARCHAR(100),

    state VARCHAR(100),

    country VARCHAR(100),

    pincode VARCHAR(20),

    registration_date DATE,

    customer_segment VARCHAR(100),

    loyalty_points BIGINT,

    preferred_payment VARCHAR(100),

    annual_income BIGINT,

    lifetime_value DECIMAL(18,2),

    occupation VARCHAR(100),

    marital_status VARCHAR(50),

    email_verified BOOLEAN,

    mobile_verified BOOLEAN,

    last_login DATE,

    marketing_opt_in BOOLEAN,

    referral_source VARCHAR(100),

    device_type VARCHAR(100),

    account_status VARCHAR(50),

    is_active BOOLEAN,

    created_date DATE,

    -- SCD TYPE 2 COLUMNS

    effective_start_date DATE NOT NULL,

    effective_end_date DATE NOT NULL,

    is_current BOOLEAN NOT NULL DEFAULT TRUE,

    version_number INT NOT NULL DEFAULT 1

);

SELECT 'Customer History Table Created Successfully' AS Status;