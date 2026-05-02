WITH user_stats AS (
    SELECT
        o.user_id,
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(f.product_id) AS total_items_bought,
        AVG(o.days_since_prior_order) AS avg_days_between_orders,
        SAFE_DIVIDE(SUM(CAST(f.reordered AS INT64)), 
        COUNT(f.product_id)) AS reorder_rate,
        SAFE_DIVIDE(COUNT(f.product_id), COUNT(DISTINCT o.order_id)) AS avg_basket_size
    FROM {{ ref('dim_orders') }} o
    LEFT JOIN {{ ref('fact_order_products') }} f ON o.order_id = f.order_id
    GROUP BY 1
)
SELECT *,
    CASE
        WHEN total_orders >= 20 THEN 'VIP'
        WHEN total_orders >= 10 THEN 'Regular'
        WHEN total_orders >= 5 THEN 'Active'
        ELSE 'New'
    END AS user_segment
FROM user_stats