{{config(materialized = 'table')}}

WITH products AS (
    SELECT * FROM {{ref('stg_products')}}
),
aisles AS (
    SELECT * FROM {{ref('stg_aisles')}}
),
departments AS (
    SELECT * FROM {{ref('stg_departments')}}
)
SELECT p.product_id, p.product_name, a.aisle_name, d.department_name
FROM products p
INNER JOIN aisles a ON p.aisle_id = a.aisle_id
INNER JOIN departments d ON p.department_id = d.department_id