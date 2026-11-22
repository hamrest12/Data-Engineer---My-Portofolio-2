
{{
    config(
        materialized = 'table',
        engine = 'MergeTree()',
        order_by = 'product_category_name'
    )
}}

SELECT
    assumeNotNull(
        nullIf(trimBoth(product_category_name), '')
    ) AS product_category_name,

    lowerUTF8(
        nullIf(trimBoth(product_category_name_english), '')
    ) AS product_category_name_english

FROM {{ source('olist_bronze', 'bronze_category_translation') }}

WHERE
    nullIf(trimBoth(product_category_name), '') IS NOT NULL
