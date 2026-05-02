{{ config(materialized='view', alias = 'stg_order_products__train') }}

SELECT
    CAST(order_id AS INT64) AS order_id,
    CAST(product_id AS INT64) AS product_id,
    CAST(add_to_cart_order AS INT64) AS add_to_cart_order,
    CAST(reordered AS BOOL) AS reordered
FROM {{ source('gcs_staging', 'bronze_order_products__train') }}