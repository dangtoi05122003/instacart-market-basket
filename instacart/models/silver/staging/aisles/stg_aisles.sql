{{ config(materialized='view', alias = 'stg_aisles') }}

SELECT
    CAST(aisle_id AS INT64) AS aisle_id,
    TRIM(aisle) AS aisle_name
FROM {{ source('gcs_staging', 'bronze_aisles') }}