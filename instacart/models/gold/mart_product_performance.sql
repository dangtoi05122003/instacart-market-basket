{{ config(materialized='table') }}

SELECT
    d.product_id,
    d.product_name,
    d.aisle_name,
    d.department_name,
    COUNT(DISTINCT f.order_id) AS total_orders,
    COUNT(*) AS total_order_lines,
    AVG(CAST(f.reordered AS INT64)) AS reorder_rate
FROM {{ref('fact_order_products')}} f
JOIN {{ref('dim_products')}} d ON f.product_id = d.product_id
GROUP BY 1, 2, 3, 4