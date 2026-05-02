{{config(materialized='table')}}

WITH prior AS (
    SELECT * FROM {{ref('stg_order_products__prior')}}
),
train AS(
    SELECT * FROM {{ ref('stg_order_products__train')}}
),
union_data  AS (
    SELECT * FROM prior
    UNION ALL
    SELECT * FROM train
)
SELECT
    order_id,
    product_id,
    add_to_cart_order,
    reordered
FROM union_data