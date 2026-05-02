{{ config(materialized = 'view', alias = 'stg_products')}}

select 
    SAFE_CAST(product_id AS INT64) AS product_id,
    TRIM(product_name) AS product_name,
    SAFE_CAST(aisle_id AS INT64) AS aisle_id,
    SAFE_CAST(department_id AS INT64) AS department_id
FROM {{ source('gcs_staging', 'bronze_products') }}