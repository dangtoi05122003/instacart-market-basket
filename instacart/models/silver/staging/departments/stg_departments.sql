{{ config(materialized='view', alias = 'stg_departments') }}

SELECT
    CAST(department_id AS INT64) AS department_id,
    TRIM(department) AS department_name
FROM {{ source('gcs_staging', 'bronze_departments') }}