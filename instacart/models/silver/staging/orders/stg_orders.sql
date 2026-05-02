{{ config(materialized = 'view', alias = 'stg_orders') }}

SELECT
    CAST(order_id AS INT64) AS order_id,
    CAST(user_id AS INT64) AS user_id,
    TRIM(eval_set) AS eval_set,
    CAST(order_number AS INT64) AS order_number,
    CAST(order_dow AS INT64) AS order_dow,
    CAST(order_hour_of_day AS INT64) AS order_hour_of_day,
    COALESCE(CAST(days_since_prior_order AS FLOAT64), 0) AS days_since_prior_order
FROM {{ source('gcs_staging', 'bronze_orders') }}