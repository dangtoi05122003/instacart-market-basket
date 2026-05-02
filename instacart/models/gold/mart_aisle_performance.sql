{{ config(materialized='table') }}

SELECT
    d.aisle_name,
    d.department_name,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM {{ ref('fact_order_products') }} f
JOIN {{ ref('dim_products') }} d
    ON f.product_id = d.product_id
GROUP BY 1,2