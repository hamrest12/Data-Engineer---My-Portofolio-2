
{{
    config(
        materialized = 'table',
        engine = 'MergeTree()',
        order_by = '(order_id, order_item_id)'
    )
}}

SELECT
    assumeNotNull(nullIf(trimBoth(toString(order_id)), ''))
        AS order_id,

    assumeNotNull(
        toUInt32OrNull(
            nullIf(trimBoth(toString(order_item_id)), '')
        )
    ) AS order_item_id,

    nullIf(trimBoth(toString(product_id)), '') AS product_id,

    nullIf(trimBoth(toString(seller_id)), '') AS seller_id,

    parseDateTimeBestEffortOrNull(
        nullIf(trimBoth(toString(shipping_limit_date)), '')
    ) AS shipping_limit_date,

    toFloat64OrNull(
        nullIf(trimBoth(toString(price)), '')
    ) AS price,

    toFloat64OrNull(
        nullIf(trimBoth(toString(freight_value)), '')
    ) AS freight_value

FROM {{ source('olist_bronze', 'bronze_order_items') }}

WHERE
    nullIf(trimBoth(toString(order_id)), '') IS NOT NULL
    AND toUInt32OrNull(
        nullIf(trimBoth(toString(order_item_id)), '')
    ) IS NOT NULL
