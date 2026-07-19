USE enterprise_gadget_store;

DROP TABLE IF EXISTS incremental_metadata;

CREATE TABLE incremental_metadata (

    pipeline_name VARCHAR(100) PRIMARY KEY,

    source_table VARCHAR(100) NOT NULL,

    target_table VARCHAR(100) NOT NULL,

    watermark_column VARCHAR(100) NOT NULL,

    last_loaded_value VARCHAR(100),

    rows_loaded BIGINT DEFAULT 0,

    last_run DATETIME,

    status VARCHAR(30)

);

INSERT INTO incremental_metadata
VALUES
(
'orders_pipeline',
'silver_orders',
'fact_orders',
'order_date',
'1900-01-01',
0,
NOW(),
'INITIAL'
),
(
'payments_pipeline',
'silver_payments',
'fact_payments',
'payment_date',
'1900-01-01',
0,
NOW(),
'INITIAL'
),
(
'shipments_pipeline',
'silver_shipments',
'fact_shipments',
'dispatch_date',
'1900-01-01',
0,
NOW(),
'INITIAL'
),
(
'inventory_pipeline',
'silver_inventory',
'fact_inventory',
'last_restock_date',
'1900-01-01',
0,
NOW(),
'INITIAL'
);

SELECT * FROM incremental_metadata;