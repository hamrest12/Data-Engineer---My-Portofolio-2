
{{
    config(
        materialized = 'table',
        engine = 'MergeTree()',
        order_by = 'product_id'
    )
}}

SELECT
    assumeNotNull(nullIf(trimBoth(product_id), ''))
        AS product_id,

    nullIf(trimBoth(product_category_name), '')
        AS product_category_name,

    toUInt32OrNull(
        nullIf(trimBoth(product_name_lenght), '')
    ) AS product_name_length,

    toUInt32OrNull(
        nullIf(trimBoth(product_description_lenght), '')
    ) AS product_description_length,

    toUInt32OrNull(
        nullIf(trimBoth(product_photos_qty), '')
    ) AS product_photos_qty,

    toFloat64OrNull(
        nullIf(trimBoth(product_weight_g), '')
    ) AS product_weight_g,

    toFloat64OrNull(
        nullIf(trimBoth(product_length_cm), '')
    ) AS product_length_cm,

    toFloat64OrNull(
        nullIf(trimBoth(product_height_cm), '')
    ) AS product_height_cm,

    toFloat64OrNull(
        nullIf(trimBoth(product_width_cm), '')
    ) AS product_width_cm

FROM {{ source('olist_bronze', 'bronze_products') }}

WHERE
    nullIf(trimBoth(product_id), '') IS NOT NULL
