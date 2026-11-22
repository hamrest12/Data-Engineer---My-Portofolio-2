
{{
    config(
        materialized = 'table',
        schema = 'olist_gold',
        engine = 'MergeTree()',
        order_by = 'order_id'
    )
}}

SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,

    shipping_limit_date,

    price,
    freight_value,

    price + freight_value AS total_item_value

FROM {{ ref('stg_order_items') }}
