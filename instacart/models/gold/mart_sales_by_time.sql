{{ config(materialized='table') }}

SELECT
    d.order_dow,
    d.order_hour_of_day,
    COUNT(DISTINCT d.order_id) AS total_orders,
    COUNT(*) AS total_items_sold
FROM {{ ref('dim_orders') }} d
LEFT JOIN {{ ref('fact_order_products') }} f
    ON d.order_id = f.order_id
GROUP BY 1, 2