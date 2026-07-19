USE enterprise_gadget_store;

-- =====================================================
-- Enterprise Gadget Store Data Warehouse
-- Gold Layer Indexes (Production Ready)
-- =====================================================

-- =====================================================
-- DIM_CATEGORY
-- =====================================================

DROP INDEX IF EXISTS idx_dim_category_category_id ON dim_category;
CREATE INDEX idx_dim_category_category_id
ON dim_category(category_id);

-- =====================================================
-- DIM_SUPPLIER
-- =====================================================

DROP INDEX IF EXISTS idx_dim_supplier_supplier_id ON dim_supplier;
CREATE INDEX idx_dim_supplier_supplier_id
ON dim_supplier(supplier_id);

-- =====================================================
-- DIM_PRODUCT
-- =====================================================

DROP INDEX IF EXISTS idx_dim_product_product_id ON dim_product;
CREATE INDEX idx_dim_product_product_id
ON dim_product(product_id);

DROP INDEX IF EXISTS idx_dim_product_category_id ON dim_product;
CREATE INDEX idx_dim_product_category_id
ON dim_product(category_id);

DROP INDEX IF EXISTS idx_dim_product_supplier_id ON dim_product;
CREATE INDEX idx_dim_product_supplier_id
ON dim_product(supplier_id);

-- =====================================================
-- DIM_CUSTOMER
-- =====================================================

DROP INDEX IF EXISTS idx_dim_customer_customer_id ON dim_customer;
CREATE INDEX idx_dim_customer_customer_id
ON dim_customer(customer_id);

DROP INDEX IF EXISTS idx_dim_customer_segment ON dim_customer;
CREATE INDEX idx_dim_customer_segment
ON dim_customer(customer_segment);

DROP INDEX IF EXISTS idx_dim_customer_state ON dim_customer;
CREATE INDEX idx_dim_customer_state
ON dim_customer(state);

-- =====================================================
-- DIM_COUPON
-- =====================================================

DROP INDEX IF EXISTS idx_dim_coupon_coupon_id ON dim_coupon;
CREATE INDEX idx_dim_coupon_coupon_id
ON dim_coupon(coupon_id);

DROP INDEX IF EXISTS idx_dim_coupon_code ON dim_coupon;
CREATE INDEX idx_dim_coupon_code
ON dim_coupon(coupon_code);

-- =====================================================
-- FACT_ORDERS
-- =====================================================

DROP INDEX IF EXISTS idx_fact_orders_order ON fact_orders;
CREATE INDEX idx_fact_orders_order
ON fact_orders(order_id);

DROP INDEX IF EXISTS idx_fact_orders_customer ON fact_orders;
CREATE INDEX idx_fact_orders_customer
ON fact_orders(customer_key);

DROP INDEX IF EXISTS idx_fact_orders_coupon ON fact_orders;
CREATE INDEX idx_fact_orders_coupon
ON fact_orders(coupon_key);

DROP INDEX IF EXISTS idx_fact_orders_date ON fact_orders;
CREATE INDEX idx_fact_orders_date
ON fact_orders(date_key);

DROP INDEX IF EXISTS idx_fact_orders_status ON fact_orders;
CREATE INDEX idx_fact_orders_status
ON fact_orders(order_status);

DROP INDEX IF EXISTS idx_fact_orders_payment_status ON fact_orders;
CREATE INDEX idx_fact_orders_payment_status
ON fact_orders(payment_status);

DROP INDEX IF EXISTS idx_fact_orders_customer_date ON fact_orders;
CREATE INDEX idx_fact_orders_customer_date
ON fact_orders(customer_key, date_key);

-- =====================================================
-- FACT_PAYMENTS
-- =====================================================

DROP INDEX IF EXISTS idx_fact_payments_payment ON fact_payments;
CREATE INDEX idx_fact_payments_payment
ON fact_payments(payment_id);

DROP INDEX IF EXISTS idx_fact_payments_order ON fact_payments;
CREATE INDEX idx_fact_payments_order
ON fact_payments(order_id);

DROP INDEX IF EXISTS idx_fact_payments_date ON fact_payments;
CREATE INDEX idx_fact_payments_date
ON fact_payments(date_key);

DROP INDEX IF EXISTS idx_fact_payments_gateway ON fact_payments;
CREATE INDEX idx_fact_payments_gateway
ON fact_payments(payment_gateway);

DROP INDEX IF EXISTS idx_fact_payments_method ON fact_payments;
CREATE INDEX idx_fact_payments_method
ON fact_payments(payment_method);

DROP INDEX IF EXISTS idx_fact_payments_status ON fact_payments;
CREATE INDEX idx_fact_payments_status
ON fact_payments(payment_status);

DROP INDEX IF EXISTS idx_fact_payments_order_date ON fact_payments;
CREATE INDEX idx_fact_payments_order_date
ON fact_payments(order_id, date_key);

-- =====================================================
-- FACT_SHIPMENTS
-- =====================================================

DROP INDEX IF EXISTS idx_fact_shipments_shipment ON fact_shipments;
CREATE INDEX idx_fact_shipments_shipment
ON fact_shipments(shipment_id);

DROP INDEX IF EXISTS idx_fact_shipments_order ON fact_shipments;
CREATE INDEX idx_fact_shipments_order
ON fact_shipments(order_id);

DROP INDEX IF EXISTS idx_fact_shipments_date ON fact_shipments;
CREATE INDEX idx_fact_shipments_date
ON fact_shipments(date_key);

DROP INDEX IF EXISTS idx_fact_shipments_status ON fact_shipments;
CREATE INDEX idx_fact_shipments_status
ON fact_shipments(shipping_status);

DROP INDEX IF EXISTS idx_fact_shipments_partner ON fact_shipments;
CREATE INDEX idx_fact_shipments_partner
ON fact_shipments(courier_partner);

DROP INDEX IF EXISTS idx_fact_shipments_order_date ON fact_shipments;
CREATE INDEX idx_fact_shipments_order_date
ON fact_shipments(order_id, date_key);

-- =====================================================
-- FACT_INVENTORY
-- =====================================================

DROP INDEX IF EXISTS idx_fact_inventory_inventory ON fact_inventory;
CREATE INDEX idx_fact_inventory_inventory
ON fact_inventory(inventory_id);

DROP INDEX IF EXISTS idx_fact_inventory_product ON fact_inventory;
CREATE INDEX idx_fact_inventory_product
ON fact_inventory(product_key);

DROP INDEX IF EXISTS idx_fact_inventory_productid ON fact_inventory;
CREATE INDEX idx_fact_inventory_productid
ON fact_inventory(product_id);

DROP INDEX IF EXISTS idx_fact_inventory_warehouse ON fact_inventory;
CREATE INDEX idx_fact_inventory_warehouse
ON fact_inventory(warehouse);

DROP INDEX IF EXISTS idx_fact_inventory_reorder ON fact_inventory;
CREATE INDEX idx_fact_inventory_reorder
ON fact_inventory(reorder_status);

DROP INDEX IF EXISTS idx_fact_inventory_product_warehouse ON fact_inventory;
CREATE INDEX idx_fact_inventory_product_warehouse
ON fact_inventory(product_key, warehouse);

-- =====================================================
-- VERIFY INDEXES
-- =====================================================

SHOW INDEX FROM dim_category;
SHOW INDEX FROM dim_supplier;
SHOW INDEX FROM dim_product;
SHOW INDEX FROM dim_customer;
SHOW INDEX FROM dim_coupon;

SHOW INDEX FROM fact_orders;
SHOW INDEX FROM fact_payments;
SHOW INDEX FROM fact_shipments;
SHOW INDEX FROM fact_inventory;

SELECT 'Gold Layer Indexes Created Successfully' AS Status;