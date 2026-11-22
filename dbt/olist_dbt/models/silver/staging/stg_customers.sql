
{{
    config(
        materialized = 'table',
        engine = 'MergeTree()',
        order_by = 'customer_id'
    )
}}

SELECT
    assumeNotNull(nullIf(trimBoth(customer_id), ''))
        AS customer_id,

    nullIf(trimBoth(customer_unique_id), '')
        AS customer_unique_id,

    toUInt32OrNull(
        nullIf(trimBoth(customer_zip_code_prefix), '')
    ) AS customer_zip_code_prefix,

    lowerUTF8(
        nullIf(trimBoth(customer_city), '')
    ) AS customer_city,

    upperUTF8(
        nullIf(trimBoth(customer_state), '')
    ) AS customer_state

FROM {{ source('olist_bronze', 'bronze_customers') }}

WHERE
    nullIf(trimBoth(customer_id), '') IS NOT NULL
