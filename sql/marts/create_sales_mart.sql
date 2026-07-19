USE enterprise_gadget_store;

-- ============================================================
-- Enterprise Gadget Store Data Warehouse
-- Sales Mart
-- ============================================================

DROP TABLE IF EXISTS sales_mart;

CREATE TABLE sales_mart AS

SELECT

    fo.order_id,

    dd.full_date,
    dd.year,
    dd.quarter,
    dd.month,
    dd.month_name,

    dc.customer_key,
    dc.customer_id,
    dc.customer_segment,
    dc.city,
    dc.state,
    dc.country,

    dcp.coupon_code,
    dcp.coupon_name,

    fo.subtotal,
    fo.discount_amount,
    fo.tax_amount,
    fo.shipping_charge,
    fo.total_amount,

    fo.payment_method,
    fo.payment_status,
    fo.order_status,
    fo.delivery_type

FROM fact_orders fo

LEFT JOIN dim_customer dc
ON fo.customer_key = dc.customer_key

LEFT JOIN dim_coupon dcp
ON fo.coupon_key = dcp.coupon_key

LEFT JOIN dim_date dd
ON fo.date_key = dd.date_key;


-- ============================================================
-- VALIDATION
-- ============================================================

SELECT COUNT(*) AS Total_Rows
FROM sales_mart;

SELECT
SUM(total_amount) AS Total_Sales
FROM sales_mart;

SELECT
AVG(total_amount) AS Average_Order_Value
FROM sales_mart;

-- ============================================================
-- COMPLETED
-- ============================================================

SELECT 'Sales Mart Created Successfully' AS Status;